"""Replace C9 only with a nonpolar 10uF/100V MLCC in standard 1210."""
from pathlib import Path
import copy, csv, json, re, shutil, sys, uuid

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).parent
sys.path.insert(0, str(ROOT / 'scripts'))
from sexpr import Atom as A, parse, dump, children, child, prop

NAME = 'C_1210_3225Metric'
VALUE = '10u 100V'
DESCRIPTION = 'MLCC10uF100V10%X7R1210, nonpolar; generic standard footprint'
STATUS = '10uF100V10%X7R1210 selected; standard3225 footprint; no manufacturer-specific3D model.'
KICAD = Path('/Applications/KiCad/KiCad.app/Contents/SharedSupport')

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
    for a, b, n in sorted(edits, reverse=True): s = s[:a] + dump(n, 1) + s[b:]
    return s

template = parse((KICAD / 'footprints/Capacitor_SMD.pretty' / (NAME + '.kicad_mod')).read_text())
child(template, 'model')[1] = '${KIPRJMOD}/library/3dmodels/' + NAME + '.step'
(ROOT / 'library/oneTesla.pretty' / (NAME + '.kicad_mod')).write_text(dump(template) + '\n')
src = KICAD / '3dmodels/Capacitor_SMD.3dshapes' / (NAME + '.step')
shutil.copy2(src, ROOT / 'library/3dmodels' / (NAME + '.step'))
(HERE / 'KiCad-model-NOTICES.txt').write_text('\n'.join(re.findall(r'/\*.*?\*/', src.read_text(), re.S)) + '\n')

p = ROOT / 'oneTesla.kicad_pcb'; original = p.read_text()
assert original == (HERE / 'before-oneTesla.kicad_pcb').read_text()
edits = []
for a, b in spans(original):
    f = parse(original[a:b])
    if f[0] != 'footprint' or prop(f, 'Reference')[2] != 'C9': continue
    assert f[1] == 'oneTesla:CP_Elec_8x10' and prop(f, 'Value')[2] == '100u 35V'
    pads = {n[1]: n for n in children(f, 'pad')}
    assert child(pads['1'], 'net')[1] == '+5V' and child(pads['2'], 'net')[1] == 'GND'
    angle = child(f, 'at')[3] if len(child(f, 'at')) > 3 else A('0')
    f[1] = 'oneTesla:' + NAME
    prop(f, 'Value')[2] = VALUE
    prop(f, 'Description')[2] = DESCRIPTION
    prop(f, 'Footprint_Status')[2] = STATUS
    prop(f, 'KiLib_Generator')[2] = 'capacitor/SMD'
    prop(f, 'ki_fp_filters')[2] = 'C_*'
    f[:] = [n for n in f if not (isinstance(n, list) and n and
            (n[0].startswith('fp_') or n[0] in ['pad', 'model', 'attr', 'descr', 'tags']))]
    for key in ['attr', 'descr', 'tags']: f.append(copy.deepcopy(child(template, key)))
    for node in template:
        if not (isinstance(node, list) and node and (node[0].startswith('fp_') or node[0] in ['pad', 'model'])): continue
        n = copy.deepcopy(node)
        if n[0] != 'model': n.append([A('uuid'), str(uuid.uuid4())])
        if n[0] in ['pad', 'fp_text']: child(n, 'at')[3:] = [angle]
        if n[0] == 'pad':
            for key in ['uuid', 'net', 'pintype', 'pinfunction']:
                n[:] = [v for v in n if not (isinstance(v, list) and v and v[0] == key)]
                if child(pads[n[1]], key): n.append(copy.deepcopy(child(pads[n[1]], key)))
        f.append(n)
    for n in children(f, 'pad'):
        for key in ['uuid', 'net', 'pintype', 'pinfunction']: assert child(n, key) == child(pads[n[1]], key)
    assert child(prop(f, 'Value'), 'hide')[1] == 'yes'
    edits.append((a, b, f))
assert len(edits) == 1
updated = replace(original, edits)
def omit(s):
    return [n for n in parse(s) if not (isinstance(n, list) and n and n[0] == 'footprint' and prop(n, 'Reference')[2] == 'C9')]
assert omit(original) == omit(updated)
assert p.read_text() == original; p.write_text(updated)

p = ROOT / 'oneTesla.kicad_sch'; original = p.read_text()
assert original == (HERE / 'before-oneTesla.kicad_sch').read_text()
lib = child(parse(original), 'lib_symbols')
def pin_geometry(name):
    sym = next(s for s in children(lib, 'symbol') if s[1] == name)
    return sorted((str(child(p, 'number')[1]), list(child(p, 'at')[1:])) for u in children(sym, 'symbol') for p in children(u, 'pin'))
assert pin_geometry('oneTesla:C') == pin_geometry('oneTesla:C_Polarized')
edits = []
updates = {'Value': VALUE, 'Footprint': 'oneTesla:' + NAME, 'Description': DESCRIPTION, 'Footprint_Status': STATUS}
for a, b in spans(original):
    f = parse(original[a:b])
    if f[0] == 'symbol' and prop(f, 'Reference') and prop(f, 'Reference')[2] == 'C9':
        assert child(f, 'lib_id')[1] == 'oneTesla:C_Polarized'
        child(f, 'lib_id')[1] = 'oneTesla:C'
        for key, value in updates.items(): prop(f, key)[2] = value
        edits.append((a, b, f))
assert len(edits) == 1
updated = replace(original, edits)
def normalize(s):
    t = parse(s)
    for f in children(t, 'symbol'):
        if prop(f, 'Reference') and prop(f, 'Reference')[2] == 'C9':
            child(f, 'lib_id')[1] = 'MASKED'
            for key in updates: prop(f, key)[2] = 'MASKED'
    return t
assert normalize(original) == normalize(updated)
assert p.read_text() == original; p.write_text(updated)

p = ROOT / 'output/components.csv'
with p.open(newline='') as f: rows = list(csv.reader(f))
for row in rows:
    if row and row[0] == 'C9': row[1:3] = [VALUE, 'oneTesla:' + NAME]; row[4] = STATUS
with p.open('w', newline='') as f: csv.writer(f).writerows(rows)
proof = {'reference': 'C9', 'value': VALUE, 'dielectric': 'X7R', 'tolerance_percent': 10,
         'footprint': 'oneTesla:' + NAME, 'symbol_nonpolar': True, 'symbol_pin_geometry_preserved': True,
         'pad_numbers_nets_and_uuids_preserved': True, 'value_remains_hidden_in_pcb': True,
         'position_rotation_and_reference_label_preserved': True, 'other_board_objects_unchanged': True,
         'schematic_other_data_unchanged': True, 'model': 'generic_KiCad_1210'}
(HERE / 'verification.json').write_text(json.dumps(proof, indent=2) + '\n')
print(json.dumps(proof, indent=2))
