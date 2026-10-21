"""Turn the native KiCad checkpoint reports into a reproducible collision map.

This is report analysis, not a KiCad DRC run or a manufacturing release check.
It refuses to analyze reports against a board/schematic changed since the
checkpoint proof was recorded.
"""

from collections import Counter, defaultdict
from hashlib import sha256
import json
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "implementation/cleanup"
REF = re.compile(r"\b(?:Footprint|pad(?: \d+)?(?: \[[^]]*\])? of|of|Symbol) ([A-Z][A-Z0-9]*\d+)\b")


def load(name):
    return json.loads((EVIDENCE / name).read_text())


def check_checkpoint(proof):
    for name in ("oneTesla.kicad_pcb", "oneTesla.kicad_sch"):
        actual = sha256((ROOT / name).read_bytes()).hexdigest()
        if actual != proof["sha256"][name]:
            raise ValueError(f"{name} changed since native-proof.json; rerun KiCad before triage")
    for current, original in (("drc-current.json", "drc-final.json"),
                              ("erc-current.json", "erc-final.json")):
        current_report, original_report = load(current), load(original)
        current_report.pop("date", None)
        original_report.pop("date", None)
        if current_report != original_report:
            raise ValueError(f"{current} differs from {original}; report/proof pairing is unknown")
    drc = load("drc-current.json")
    if len(drc["violations"]) != proof["drc_count"] or len(drc["schematic_parity"]) != proof["parity"]:
        raise ValueError("DRC/parity counts differ from native-proof.json")
    return drc, load("erc-current.json")


def references(violation):
    refs = set()
    for item in violation["items"]:
        found = REF.search(item["description"])
        if found:
            refs.add(found.group(1))
    return tuple(sorted(refs))


def groups(violations):
    """Connected components of the footprint-interference graph."""
    parent = {}

    def find(ref):
        parent.setdefault(ref, ref)
        if parent[ref] != ref:
            parent[ref] = find(parent[ref])
        return parent[ref]

    for violation in violations:
        refs = references(violation)
        for ref in refs:
            find(ref)
        for ref in refs[1:]:
            parent[find(ref)] = find(refs[0])

    members = defaultdict(set)
    for ref in parent:
        members[find(ref)].add(ref)
    result = []
    for refs in members.values():
        entries = [v for v in violations if set(references(v)) & refs]
        result.append((tuple(sorted(refs)), Counter(v["type"] for v in entries)))
    return sorted(result, key=lambda row: (-sum(row[1].values()), row[0]))


def render(drc, erc):
    violations = drc["violations"]
    erc_violations = [v for sheet in erc["sheets"] for v in sheet["violations"]]
    counts = Counter(v["type"] for v in violations)
    unresolved = [v for v in violations if not references(v)]
    if unresolved:
        raise ValueError(f"{len(unresolved)} DRC entries could not be assigned to a component")
    clusters = groups(violations)
    if sum(sum(c.values()) for _, c in clusters) != len(violations):
        raise ValueError("collision graph duplicated or lost DRC entries")
    lines = [
        "# Triagem reproduzível do checkpoint KiCad",
        "",
        "Gerado de `drc-current.json` e `erc-current.json` por `triage_drc.py`.",
        "Os hashes do PCB e esquema foram comparados a `native-proof.json`.",
        "**Isto não reexecuta KiCad, não valida peças/envelopes e não libera fabricação.**",
        "",
        f"- DRC: **{len(violations)}** ocorrências; conexões pendentes: **{len(drc['unconnected_items'])}**.",
        f"- Paridade: **{len(drc['schematic_parity'])}**; ERC: **{len(erc_violations)}**.",
        "- Tipos DRC: " + ", ".join(f"`{kind}` {count}" for kind, count in sorted(counts.items())) + ".",
        "",
        "## Grupos de interferência",
        "",
        "Uma ocorrência pertence a um grupo; grupos ligados por uma mesma referência são unidos.",
        "A contagem inclui silk, furos e courtyard e **não** mede a gravidade elétrica.",
        "",
        "| Referências ligadas | Ocorrências | Tipos |",
        "|---|---:|---|",
    ]
    for refs, kinds in clusters:
        types = ", ".join(f"{kind}: {number}" for kind, number in sorted(kinds.items()))
        lines.append(f"| {', '.join(refs)} | {sum(kinds.values())} | {types} |")
    lines += ["", "## Paridade e ERC", ""]
    for v in drc["schematic_parity"]:
        lines.append(f"- Paridade `{v['type']}`: {', '.join(references(v)) or v['description']}.")
    for v in erc_violations:
        lines.append(f"- ERC `{v['type']}`: {', '.join(item['description'] for item in v['items'])}.")
    lines += ["", "Pendências de componente, potência, isolamento e envelope físico permanecem em `FECHAMENTO.md`.", ""]
    return "\n".join(lines)


def main():
    try:
        drc, erc = check_checkpoint(load("native-proof.json"))
        output = render(drc, erc)
    except (KeyError, ValueError, OSError) as error:
        print(f"Triagem recusada: {error}", file=sys.stderr)
        return 1
    (EVIDENCE / "TRIAGEM.md").write_text(output)
    print(f"Wrote {EVIDENCE / 'TRIAGEM.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
