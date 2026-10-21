"""Apply 3D models to the MAIN board and matching local footprints only."""
from pathlib import Path
import copy
import hashlib
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
from sexpr import parse, children, child, prop

MODELS = {
    'CP_D8_P2.54_ReviewPending': ('Visual_CP_D8_P2.54.step', (0, 0, 0)),
    'CP_D12.5_P3.556_ReviewPending': ('Visual_CP_D12.5_P3.556.step', (0, 0, 0)),
    'CP_D30_P10.16_ReviewPending': ('Visual_CP_D30_P10.16.step', (0, 0, 0)),
    'R_L9_P10.16_ReviewPending': ('Visual_R_L9_P10.16.step', (0, 0, 0)),
    'D_DO201AD_P14.732_ReviewPending': ('Visual_TVS_DO201AD_P14.732.step', (0, 0, 0)),
    'Q_TO3P_ImportedPads_ReviewPending': ('Visual_FGA60N65SMD_Horizontal_P5.45.step', (0, 0, 0)),
    'CDE_940C30S68K_F_CONFIRMAR': ('Visual_CDE_940C30S68K_F_P58.42.step', (0, 0, 0)),
    'HLK-15M15BL': ('Catalog_HLK15M_Cased.step', (21.25, -3.9, 0)),
    'HFBR-2521ETZ': ('Catalog_HFBR-2521ETZ.step', (3.81, 3.945263198426088, 0)),
}


def spans(text, target_depth=2):
    depth = 0
    start = 0
    for match in re.finditer(r'"(?:\\.|[^"\\])*"|[()]', text):
        if match.group() == '(':
            depth += 1
            if depth == target_depth:
                start = match.start()
        elif match.group() == ')':
            if depth == target_depth:
                yield start, match.end()
            depth -= 1


def model_block(name, offset, indent):
    x, y, z = offset
    rotation = 180 if name == 'Catalog_HFBR-2521ETZ.step' else 0
    nested = indent + ('  ' if indent.startswith(' ') else '\t')
    return (f'{indent}(model "${{KIPRJMOD}}/library/3dmodels/{name}"\n'
            f'{nested}(offset (xyz {x} {y} {z}))\n'
            f'{nested}(scale (xyz 1 1 1))\n'
            f'{nested}(rotate (xyz 0 0 {rotation}))\n'
            f'{indent})\n')


def add_model(text, model, indent):
    node = parse(text)
    name, offset = model
    assert (ROOT / 'library/3dmodels' / name).is_file()
    existing = children(node, 'model')
    if existing:
        assert len(existing) == 1
        if existing[0][1] != '${KIPRJMOD}/library/3dmodels/' + name:
            assert name == 'Catalog_HFBR-2521ETZ.step'
            assert existing[0][1] == '${KICAD10_3DMODEL_DIR}/OptoDevice.3dshapes/AGILENT_HFBR-252x.step'
        matches = [(a, b) for a, b in spans(text) if parse(text[a:b])[0] == 'model']
        assert len(matches) == 1
        a, b = matches[0]
        return text[:a] + model_block(name, offset, indent)[len(indent):].rstrip() + text[b:]
    end = text.rfind(')')
    line_start = text.rfind('\n', 0, end) + 1
    insertion = line_start if not text[line_start:end].strip() else end
    return text[:insertion] + model_block(name, offset, indent) + text[insertion:]


def without_models(tree):
    result = copy.deepcopy(tree)
    nodes = children(result, 'footprint') if result[0] == 'kicad_pcb' else [result]
    for node in nodes:
        node[:] = [v for v in node if not (isinstance(v, list) and v and v[0] == 'model')]
    return result


proof = []
for board_name in ['oneTesla.kicad_pcb']:
    path = ROOT / board_name
    text = path.read_text()
    original = text
    edits = []
    refs = []
    for start, end in spans(text):
        node = parse(text[start:end])
        if node[0] != 'footprint':
            continue
        name = str(node[1]).split(':')[-1]
        if name in MODELS:
            edits.append((start, end, add_model(text[start:end], MODELS[name], '\t\t')))
            refs.append(prop(node, 'Reference')[2])
    for start, end, replacement in reversed(edits):
        text = text[:start] + replacement + text[end:]
    assert len(refs) == 15
    assert without_models(parse(original)) == without_models(parse(text))
    baseline = (Path('/private/tmp') / ('oneTesla-models3d-before-' + board_name)).read_text()
    initial_snapshot_matches = without_models(parse(baseline)) == without_models(parse(text))
    # Preserve concurrent user edits: the strict invariant above compares this
    # operation's actual input and output, not an older snapshot of the board.
    assert path.read_text() == original, 'Board changed while processing; retry'
    path.write_text(text)
    proof.append(dict(board=board_name, added_models=[r for r in refs if r != 'FB1'],
                      repaired_models=['FB1'], model_changes_only=True,
                      initial_snapshot_matches=initial_snapshot_matches,
                      sha256=hashlib.sha256(text.encode()).hexdigest()))

for name, model in MODELS.items():
    path = ROOT / 'library/oneTesla.pretty' / (name + '.kicad_mod')
    original = path.read_text()
    text = add_model(original, model, '  ')
    assert without_models(parse(original)) == without_models(parse(text))
    path.write_text(text)

(ROOT / 'implementation/models3d/verification.json').write_text(json.dumps(proof, indent=2) + '\n')
print(json.dumps(proof, indent=2))
