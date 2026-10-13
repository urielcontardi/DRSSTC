"""Resize only C11/C12 body envelopes; preserve their current unconfirmed holes."""
from pathlib import Path
import copy, csv, hashlib, json, re, sys

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).parent
sys.path.insert(0, str(ROOT / 'scripts'))
from sexpr import Atom as A, parse, dump, child, children, prop

REFS = {'C11', 'C12'}
NAME = 'CP_D25_H45_P10.16_ReviewPending'
MODEL = '${KIPRJMOD}/library/3dmodels/Visual_CP_D25_H45_P10.16.step'
STATUS = ('Ketuo 1000uF 200V, body D25 x H45mm from user image. '
          'Existing P10.16mm, drill2mm and pad4mm preserved provisionally; '
          'actual terminal pitch and section NOT confirmed.')

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
    for a, b, node in sorted(edits, reverse=True):
        s = s[:a] + dump(node, 1) + s[b:]
    return s

def without_targets(tree):
    return [n for n in tree if not (isinstance(n, list) and n and
            n[0] == 'footprint' and prop(n, 'Reference')[2] in REFS)]

p = ROOT / 'oneTesla.kicad_pcb'
original = p.read_text()
assert original == (HERE / 'before-oneTesla.kicad_pcb').read_text()
edits = []
proof = {}
for a, b in spans(original):
    f = parse(original[a:b])
    if f[0] != 'footprint' or prop(f, 'Reference')[2] not in REFS: continue
    old = copy.deepcopy(f)
    ref = prop(f, 'Reference')[2]
    assert f[1] == 'oneTesla:CP_D30_P10.16_ReviewPending'
    f[1] = 'oneTesla:' + NAME
    child(f, 'descr')[1] = STATUS
    child(f, 'tags')[1] = 'Ketuo electrolytic 1000uF 200V D25 H45 P10.16 provisional'
    prop(f, 'Description')[2] = 'Ketuo 1000uF 200V, nominal body diameter25mm height45mm'
    prop(f, 'Footprint_Status')[2] = STATUS
    for field in ['Reference', 'Value']:
        at = child(prop(f, field), 'at')
        at[1:3] = [A(str(round(float(v) * 25 / 30, 6))) for v in at[1:3]]
    if ref == 'C11':
        child(prop(f, 'Reference'), 'at')[1] = A('13.6')
    for node in f:
        if not (isinstance(node, list) and node and node[0].startswith('fp_')): continue
        for key in ['start', 'end', 'center', 'mid']:
            point = child(node, key)
            if point:
                point[1:3] = [A(str(round(float(v) * 25 / 30, 6))) for v in point[1:3]]
        # Keep original silk/courtyard margin widths around the reduced body.
        if node[0] == 'fp_circle':
            layer = child(node, 'layer')[1]
            radius = {'F.Fab': '12.5', 'F.SilkS': '12.62', 'F.CrtYd': '12.75'}[layer]
            child(node, 'end')[1:3] = [A(radius), A('0')]
    child(f, 'model')[1] = MODEL
    assert children(f, 'pad') == children(old, 'pad')
    assert child(f, 'at') == child(old, 'at')
    assert prop(f, 'Value') == prop(old, 'Value') or prop(f, 'Value')[2] == prop(old, 'Value')[2]
    proof[ref] = {'position': list(child(f, 'at')[1:]), 'pads_unchanged': True,
                  'body_mm': [25, 45], 'pitch_mm_provisional': 10.16}
    edits.append((a, b, f))
assert len(edits) == 2
updated = replace(original, edits)
assert without_targets(parse(original)) == without_targets(parse(updated))

# Export the same geometry to the local library, removing instance-only metadata.
template = copy.deepcopy(edits[0][2])
template[1] = NAME
remove = {'uuid', 'at', 'path', 'sheetname', 'sheetfile', 'units'}
template[:] = [n for n in template if not (isinstance(n, list) and n and n[0] in remove)]
template.insert(2, [A('version'), A('20260206')])
template.insert(3, [A('generator'), 'pcbnew'])
def strip_instance(node):
    if not isinstance(node, list): return
    node[:] = [v for v in node if not (isinstance(v, list) and v and v[0] in ['uuid', 'net', 'pintype', 'pinfunction'])]
    for v in node: strip_instance(v)
strip_instance(template)
prop(template, 'Reference')[2] = 'REF**'
prop(template, 'Value')[2] = NAME
(ROOT / 'library/oneTesla.pretty' / (NAME + '.kicad_mod')).write_text(dump(template) + '\n')
assert p.read_text() == original
p.write_text(updated)

p = ROOT / 'oneTesla.kicad_sch'
original = p.read_text()
assert original == (HERE / 'before-oneTesla.kicad_sch').read_text()
edits = []
for a, b in spans(original):
    s = parse(original[a:b])
    if s[0] == 'symbol' and prop(s, 'Reference') and prop(s, 'Reference')[2] in REFS:
        prop(s, 'Footprint')[2] = 'oneTesla:' + NAME
        prop(s, 'Footprint_Status')[2] = STATUS
        edits.append((a, b, s))
assert len(edits) == 2
updated = replace(original, edits)
def masked(s):
    t = parse(s)
    for sym in children(t, 'symbol'):
        if prop(sym, 'Reference') and prop(sym, 'Reference')[2] in REFS:
            for k in ['Footprint', 'Footprint_Status']: prop(sym, k)[2] = 'MASKED'
    return t
assert masked(original) == masked(updated)
assert p.read_text() == original
p.write_text(updated)

p = ROOT / 'output/components.csv'
with p.open(newline='') as f:
    rows = list(csv.reader(f))
for row in rows:
    if row and row[0] in REFS:
        row[2] = 'oneTesla:' + NAME
        row[4] = STATUS
with p.open('w', newline='') as f: csv.writer(f).writerows(rows)
assert hashlib.sha256((ROOT / 'oneTesla-autorouted.kicad_pcb').read_bytes()).hexdigest() == (HERE / 'autorouted.sha256').read_text().strip()
proof['all_other_pcb_objects_unchanged'] = True
proof['schematic_connectivity_unchanged'] = True
proof['autorouted_unchanged'] = True
(HERE / 'verification.json').write_text(json.dumps(proof, indent=2) + '\n')
print(json.dumps(proof, indent=2))
