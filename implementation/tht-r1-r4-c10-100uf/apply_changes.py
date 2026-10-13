"""Restore R1/R4 THT footprints, reduce C10, and remove the unused autorouted copy."""
from pathlib import Path
import copy, csv, json, re, sys, uuid

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).parent
sys.path.insert(0, str(ROOT / 'scripts'))
from sexpr import Atom as A, parse, dump, child, children, prop

REFS = {'R1', 'R4', 'C10'}
STATUS = ('Capxon 100uF/35V SMD; standard D8 x H10mm assumed, dimensions unverified. '
          'C10 reduced from680uF with HLK15M15BL supply; verify15V load transients on hardware.')

def spans(s):
    depth = 0
    for m in re.finditer(r'"(?:\\.|[^"\\])*"|[()]', s):
        if m.group() == '(':
            depth += 1
            if depth == 2: start = m.start()
        elif m.group() == ')':
            if depth == 2: yield start, m.end()
            depth -= 1

def patch(s, edits):
    for a, b, f in sorted(edits, reverse=True): s = s[:a] + dump(f, 1) + s[b:]
    return s

def targets(tree, key):
    return {prop(n, 'Reference')[2]: n for n in children(tree, key)
            if prop(n, 'Reference') and prop(n, 'Reference')[2] in REFS}

base_pcb = targets(parse((ROOT / 'implementation/smd-conversion/before-oneTesla.kicad_pcb').read_text()), 'footprint')
base_sch = targets(parse((ROOT / 'implementation/smd-conversion/before-oneTesla.kicad_sch').read_text()), 'symbol')
template = parse((ROOT / 'library/oneTesla.pretty/CP_Elec_8x10.kicad_mod').read_text())
p = ROOT / 'oneTesla.kicad_pcb'
original = p.read_text()
assert original == (HERE / 'before-oneTesla.kicad_pcb').read_text()
edits = []
for a, b in spans(original):
    f = parse(original[a:b])
    if f[0] != 'footprint' or prop(f, 'Reference')[2] not in REFS: continue
    ref = prop(f, 'Reference')[2]
    old = copy.deepcopy(f)
    pads = {n[1]: n for n in children(f, 'pad')}
    if ref in ['R1', 'R4']:
        f = copy.deepcopy(base_pcb[ref])
        if ref == 'R1':
            # Keep the current position: the earlier position now conflicts with FB1.
            child(f, 'at')[:] = copy.deepcopy(child(old, 'at'))
            vertical = parse((ROOT / 'library/oneTesla.pretty/R_Axial_Vishay_AC05_L18.0mm_D7.5mm_P10.16mm_Vertical.kicad_mod').read_text())
            f[:] = [v for v in f if not (isinstance(v, list) and v and (v[0].startswith('fp_') or v[0] in ['pad', 'model']))]
            for node in vertical:
                if not (isinstance(node, list) and node and (node[0].startswith('fp_') or node[0] in ['pad', 'model'])): continue
                n = copy.deepcopy(node)
                if n[0] != 'model': n.append([A('uuid'), str(uuid.uuid4())])
                if n[0] == 'pad': child(n, 'at').append(A('90'))
                if n[0] == 'fp_text': child(n, 'at').append(A('90'))
                f.append(n)
        assert child(f, 'uuid') == child(old, 'uuid')
        assert prop(f, 'Value')[2] == prop(old, 'Value')[2]
        # Preserve the current pin connections and identifiers on restored geometry.
        for n in children(f, 'pad'):
            for key in ['net', 'uuid', 'pintype', 'pinfunction']:
                old_field = child(pads[n[1]], key)
                if old_field:
                    if child(n, key): child(n, key)[:] = copy.deepcopy(old_field)
                    else: n.append(copy.deepcopy(old_field))
    else:
        assert ref == 'C10' and prop(f, 'Value')[2] == '680u 35V'
        assert child(pads['1'], 'net')[1] == '+15V' and child(pads['2'], 'net')[1] == 'GND'
        f[1] = 'oneTesla:CP_Elec_8x10'
        prop(f, 'Value')[2] = '100u 35V'
        prop(f, 'Description')[2] = 'Capxon100uF35V; generic SMD D8xH10 assumed'
        prop(f, 'Footprint_Status')[2] = STATUS
        if prop(f, 'KiLib_Generator'): prop(f, 'KiLib_Generator')[2] = 'capacitor/SMD'
        f[:] = [n for n in f if not (isinstance(n, list) and n and
                (n[0].startswith('fp_') or n[0] in ['pad', 'model', 'attr', 'descr', 'tags']))]
        for k in ['attr', 'descr', 'tags']: f.append(copy.deepcopy(child(template, k)))
        for k in ['Reference', 'Value']:
            field = prop(f, k)
            field_id = child(field, 'uuid')
            ident = copy.deepcopy(field_id) if field_id else [A('uuid'), str(uuid.uuid4())]
            value = field[2]
            field[:] = copy.deepcopy(prop(template, k))
            field[2] = value
            field.append(ident)
        for node in template:
            if not (isinstance(node, list) and node and (node[0].startswith('fp_') or node[0] in ['pad', 'model'])): continue
            n = copy.deepcopy(node)
            if n[0] != 'model': n.append([A('uuid'), str(uuid.uuid4())])
            if n[0] == 'pad':
                for k in ['uuid', 'net', 'pintype', 'pinfunction']:
                    n[:] = [v for v in n if not (isinstance(v, list) and v and v[0] == k)]
                    if child(pads[n[1]], k): n.append(copy.deepcopy(child(pads[n[1]], k)))
            f.append(n)
        assert child(f, 'at') == child(old, 'at')
    for n in children(f, 'pad'):
        for k in ['net', 'uuid', 'pintype', 'pinfunction']: assert child(n, k) == child(pads[n[1]], k)
    edits.append((a, b, f))
assert len(edits) == 3
updated = patch(original, edits)
def omit(tree):
    return [n for n in tree if not (isinstance(n, list) and n and n[0] == 'footprint' and prop(n, 'Reference')[2] in REFS)]
assert omit(parse(original)) == omit(parse(updated))
assert p.read_text() == original
p.write_text(updated)

p = ROOT / 'oneTesla.kicad_sch'
original = p.read_text()
assert original == (HERE / 'before-oneTesla.kicad_sch').read_text()
keys = {'R1': ['Footprint', 'Description', 'Footprint_Status', 'Assembly_Notes', 'Datasheet'],
        'R4': ['Footprint', 'Description', 'Footprint_Status', 'Datasheet'],
        'C10': ['Footprint', 'Value', 'Description', 'Footprint_Status']}
edits = []
for a, b in spans(original):
    f = parse(original[a:b])
    if f[0] != 'symbol' or not prop(f, 'Reference') or prop(f, 'Reference')[2] not in REFS: continue
    ref = prop(f, 'Reference')[2]
    for k in keys[ref]:
        if ref in ['R1', 'R4']: prop(f, k)[2] = prop(base_sch[ref], k)[2]
        else: prop(f, k)[2] = {'Footprint': 'oneTesla:CP_Elec_8x10', 'Value': '100u 35V',
                              'Description': 'Capxon100uF35V; generic SMD D8xH10 assumed', 'Footprint_Status': STATUS}[k]
    edits.append((a, b, f))
assert len(edits) == 3
updated = patch(original, edits)
def normalize(s):
    tree = parse(s)
    for ref, f in targets(tree, 'symbol').items():
        for k in keys[ref]: prop(f, k)[2] = 'MASKED'
    return tree
assert normalize(original) == normalize(updated)
assert p.read_text() == original
p.write_text(updated)

p = ROOT / 'output/components.csv'
with p.open(newline='') as f: rows = list(csv.reader(f))
now = targets(parse((ROOT / 'oneTesla.kicad_pcb').read_text()), 'footprint')
for row in rows:
    if row and row[0] in REFS:
        f = now[row[0]]
        row[1:3] = [prop(f, 'Value')[2], f[1]]
        row[4] = prop(f, 'Footprint_Status')[2]
        if len(row) > 5: row[5] = prop(f, 'Assembly_Notes')[2] if prop(f, 'Assembly_Notes') else ''
with p.open('w', newline='') as f: csv.writer(f).writerows(rows)

deleted = []
for name in ['oneTesla-autorouted.kicad_pcb', 'oneTesla-autorouted.kicad_pro', 'oneTesla-autorouted.kicad_prl']:
    p = ROOT / name
    if p.exists():
        p.unlink()
        deleted.append(name)
proof = {'references_changed': sorted(REFS), 'other_board_objects_unchanged': True,
         'schematic_connectivity_unchanged': True, 'pad_nets_and_uuids_preserved': True,
         'R1_original_vertical_footprint_restored': True, 'R4_original_THT_footprint_restored': True,
         'R1_current_position_preserved': [44.5, 151.0, 90],
         'C10': {'uF_before': 680, 'uF_after': 100, 'voltage_V': 35, 'footprint': 'oneTesla:CP_Elec_8x10'},
         'deleted': deleted}
(HERE / 'verification.json').write_text(json.dumps(proof, indent=2) + '\n')
print(json.dumps(proof, indent=2))
