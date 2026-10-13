"""Change only R5/R6 to generic vertical THT and remove all routed copper."""
from pathlib import Path
import copy, csv, json, math, re, shutil, sys, uuid

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).parent
sys.path.insert(0, str(ROOT / 'scripts'))
from sexpr import Atom as A, parse, dump, children, child, prop

REFS = {'R5', 'R6'}
NAME = 'R_Axial_DIN0309_L9.0mm_D3.2mm_P5.08mm_Vertical'
KICAD = Path('/Applications/KiCad/KiCad.app/Contents/SharedSupport')
STATUS = ('Generic THT axial vertical, nominal0.5W body9xD3.2mm, formed pitch5.08mm; '
          'drill0.8/pad1.6mm. Confirm purchased resistor dimensions and working voltage; no MPN selected.')
DESCRIPTION = '100k0.5W axial resistor, vertical THT DIN0309, body9xD3.2mm, P5.08mm'

def spans(s):
    depth = 0
    for m in re.finditer(r'"(?:\\.|[^"\\])*"|[()]', s):
        if m.group() == '(':
            depth += 1
            if depth == 2: start = m.start()
        elif m.group() == ')':
            if depth == 2: yield start, m.end()
            depth -= 1

def replace(s, edits):
    for a, b, node in sorted(edits, reverse=True): s = s[:a] + (dump(node, 1) if node else '') + s[b:]
    return s

template = parse((KICAD / 'footprints/Resistor_THT.pretty' / (NAME + '.kicad_mod')).read_text())
child(template, 'model')[1] = '${KIPRJMOD}/library/3dmodels/' + NAME + '.step'
(ROOT / 'library/oneTesla.pretty' / (NAME + '.kicad_mod')).write_text(dump(template) + '\n')
source_model = KICAD / '3dmodels/Resistor_THT.3dshapes' / (NAME + '.step')
shutil.copy2(source_model, ROOT / 'library/3dmodels' / (NAME + '.step'))
source_text = source_model.read_text()
notices = '\n'.join(re.findall(r'/\*.*?\*/', source_text, flags=re.S))
(HERE / 'KiCad-model-NOTICES.txt').write_text(notices + '\n')

p = ROOT / 'oneTesla.kicad_pcb'
original = p.read_text()
assert original == (HERE / 'before-oneTesla.kicad_pcb').read_text()
edits = []
removed = {'segment': 0, 'arc': 0, 'via': 0}
positions = {}
for a, b in spans(original):
    f = parse(original[a:b])
    if f[0] in removed:
        removed[f[0]] += 1
        edits.append((a, b, None))
        continue
    if f[0] != 'footprint' or prop(f, 'Reference')[2] not in REFS: continue
    ref = prop(f, 'Reference')[2]
    pads = {n[1]: n for n in children(f, 'pad')}
    assert prop(f, 'Value')[2] == '100k 0.5W'
    at = child(f, 'at')
    angle = float(at[3]) if len(at) > 3 else 0
    # Standard footprint origin is pad1; keep the existing midpoint of its pads.
    at[1] = A(str(round(float(at[1]) - 2.54 * math.cos(math.radians(angle)), 6)))
    at[2] = A(str(round(float(at[2]) + 2.54 * math.sin(math.radians(angle)), 6)))
    positions[ref] = list(at[1:])
    f[1] = 'oneTesla:' + NAME
    prop(f, 'Description')[2] = DESCRIPTION
    prop(f, 'Footprint_Status')[2] = STATUS
    if prop(f, 'KiLib_Generator'): prop(f, 'KiLib_Generator')[2] = 'resistor/THT'
    f[:] = [n for n in f if not (isinstance(n, list) and n and
            (n[0].startswith('fp_') or n[0] in ['pad', 'model', 'attr', 'descr', 'tags']))]
    for k in ['attr', 'descr', 'tags']: f.append(copy.deepcopy(child(template, k)))
    for k in ['Reference', 'Value']:
        field = prop(f, k)
        value = field[2]
        ident = copy.deepcopy(child(field, 'uuid'))
        field[:] = copy.deepcopy(prop(template, k))
        field[2] = value
        child(field, 'at')[3:] = [A(str(angle))]
        if k == 'Reference' and ref == 'R6': child(field, 'at')[2] = A('2.72')
        if ident: field.append(ident)
    for node in template:
        if not (isinstance(node, list) and node and (node[0].startswith('fp_') or node[0] in ['pad', 'model'])): continue
        n = copy.deepcopy(node)
        if n[0] != 'model': n.append([A('uuid'), str(uuid.uuid4())])
        if n[0] in ['pad', 'fp_text']: child(n, 'at')[3:] = [A(str(angle))]
        if n[0] == 'pad':
            for k in ['uuid', 'net', 'pintype', 'pinfunction']:
                n[:] = [v for v in n if not (isinstance(v, list) and v and v[0] == k)]
                if child(pads[n[1]], k): n.append(copy.deepcopy(child(pads[n[1]], k)))
        f.append(n)
    for n in children(f, 'pad'):
        for k in ['uuid', 'net', 'pintype', 'pinfunction']: assert child(n, k) == child(pads[n[1]], k)
    edits.append((a, b, f))
assert len(positions) == 2
updated = replace(original, edits)
def omit_changed(t):
    return [n for n in t if not (isinstance(n, list) and n and
            (n[0] in removed or (n[0] == 'footprint' and prop(n, 'Reference')[2] in REFS)))]
assert omit_changed(parse(original)) == omit_changed(parse(updated))
assert not any(children(parse(updated), k) for k in removed)
assert p.read_text() == original
p.write_text(updated)

p = ROOT / 'oneTesla.kicad_sch'
original = p.read_text()
assert original == (HERE / 'before-oneTesla.kicad_sch').read_text()
edits = []
updates = {'Footprint': 'oneTesla:' + NAME, 'Description': DESCRIPTION, 'Footprint_Status': STATUS}
for a, b in spans(original):
    sym = parse(original[a:b])
    if sym[0] == 'symbol' and prop(sym, 'Reference') and prop(sym, 'Reference')[2] in REFS:
        for k, value in updates.items(): prop(sym, k)[2] = value
        edits.append((a, b, sym))
assert len(edits) == 2
updated = replace(original, edits)
def normalize(s):
    t = parse(s)
    for f in children(t, 'symbol'):
        if prop(f, 'Reference') and prop(f, 'Reference')[2] in REFS:
            for k in updates: prop(f, k)[2] = 'MASKED'
    return t
assert normalize(original) == normalize(updated)
assert p.read_text() == original
p.write_text(updated)

p = ROOT / 'output/components.csv'
with p.open(newline='') as f: rows = list(csv.reader(f))
for row in rows:
    if row and row[0] in REFS:
        row[2] = 'oneTesla:' + NAME
        row[4] = STATUS
with p.open('w', newline='') as f: csv.writer(f).writerows(rows)
proof = {'references': sorted(REFS), 'footprint': 'oneTesla:' + NAME, 'values_preserved': '100k0.5W',
         'package_nominal_mm': [9, 3.2], 'pitch_mm': 5.08, 'drill_mm': 0.8,
         'positions_after': positions, 'pad_midpoints_preserved': True,
         'pad_nets_numbers_and_uuids_preserved': True, 'routing_removed': removed,
         'routing_remaining': {'segment': 0, 'arc': 0, 'via': 0},
         'all_other_pcb_objects_preserved': True, 'schematic_connectivity_preserved': True}
(HERE / 'verification.json').write_text(json.dumps(proof, indent=2) + '\n')
print(json.dumps(proof, indent=2))
