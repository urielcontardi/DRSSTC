"""Change only R1 in the main PCB and its schematic; undo autorouted 3D edits."""
from pathlib import Path
import copy
import hashlib
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).parent
sys.path.insert(0, str(ROOT / 'scripts'))
from sexpr import Atom as A, parse, dump, children, child, prop

NAME = 'R_Axial_Vishay_AC05_L18.0mm_D7.5mm_P10.16mm_Vertical'
DESCRIPTION = 'Vishay AC05 1k 5W vertical; body18xD7.5mm; formed pitch10.16mm; drill1.2mm/pad2.4mm.'
STATUS = 'Vertical manual forming P10.16mm; nominal body18xD7.5mm; verify purchased resistor and thermal clearance.'
NOTES = 'Vertical body above pad1; body clearance >=3mm in STEP; assembly height26.4mm; formed upper lead D0.8mm; no fixed factory mounting pitch.'


def spans(text, target_depth=2):
    depth = 0
    for m in re.finditer(r'"(?:\\.|[^"\\])*"|[()]', text):
        if m.group() == '(':
            depth += 1
            if depth == target_depth:
                start = m.start()
        elif m.group() == ')':
            if depth == target_depth:
                yield start, m.end()
            depth -= 1


def strip_models(node):
    node = copy.deepcopy(node)
    for fp in children(node, 'footprint'):
        fp[:] = [v for v in fp if not (isinstance(v, list) and v and v[0] == 'model')]
    return node


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_checked(path, original, updated):
    assert path.read_text() == original, 'Concurrent file change; retry with current file'
    path.write_text(updated)


footprint_text = f'''(footprint "{NAME}"
  (version 20260206)
  (generator "pcbnew")
  (layer "F.Cu")
  (descr "{DESCRIPTION}")
  (tags "Vishay AC05 resistor axial vertical 5W P10.16 manual forming")
  (property "Reference" "REF**" (at 0 -5.8) (layer "F.SilkS")
    (effects (font (size 1 1) (thickness 0.15))))
  (property "Value" "AC05 1k 5W" (at 0 5.8) (layer "F.Fab")
    (effects (font (size 1 1) (thickness 0.15))))
  (property "Datasheet" "https://www.vishay.com/docs/28730/ac_ac-at_ac-ni.pdf"
    (at 0 0) (layer "F.Fab") (hide yes) (effects (font (size 1 1))))
  (attr through_hole)
  (fp_circle (center -5.08 0) (end -1.33 0)
    (stroke (width 0.1) (type default)) (fill no) (layer "F.Fab"))
  (fp_line (start -5.08 0) (end 5.08 0)
    (stroke (width 0.1) (type default)) (layer "F.Fab"))
  (fp_circle (center -5.08 0) (end -1.18 0)
    (stroke (width 0.12) (type default)) (fill no) (layer "F.SilkS"))
  (fp_line (start -1.18 0) (end 3.76 0)
    (stroke (width 0.12) (type default)) (layer "F.SilkS"))
  (fp_rect (start -9.58 -4.5) (end 6.78 4.5)
    (stroke (width 0.05) (type default)) (fill no) (layer "F.CrtYd"))
  (fp_text user "${{REFERENCE}}" (at -5.08 0) (layer "F.Fab")
    (effects (font (size 1 1) (thickness 0.15))))
  (pad "1" thru_hole circle (at -5.08 0) (size 2.4 2.4) (drill 1.2)
    (layers "*.Cu" "*.Mask") (remove_unused_layers no))
  (pad "2" thru_hole circle (at 5.08 0) (size 2.4 2.4) (drill 1.2)
    (layers "*.Cu" "*.Mask") (remove_unused_layers no))
  (model "${{KIPRJMOD}}/library/3dmodels/Visual_Vishay_AC05_Vertical_P10.16.step"
    (offset (xyz 0 0 0)) (scale (xyz 1 1 1)) (rotate (xyz 0 0 0)))
)
'''
template = parse(footprint_text)
assert (ROOT / 'library/3dmodels/Visual_Vishay_AC05_Vertical_P10.16.step').is_file()

# Revert only the model changes made to the secondary board in the earlier task.
secondary = ROOT / 'oneTesla-autorouted.kicad_pcb'
old = secondary.read_text()
(HERE / 'autorouted-before.kicad_pcb').write_text(old)
baseline = parse(Path('/private/tmp/oneTesla-models3d-before-oneTesla-autorouted.kicad_pcb').read_text())
original_models = {child(f, 'uuid')[1]: children(f, 'model') for f in children(baseline, 'footprint')}
secondary_text = old
for start, end in reversed(list(spans(old))):
    fp = parse(old[start:end])
    if fp[0] != 'footprint':
        continue
    wanted = original_models[child(fp, 'uuid')[1]]
    if children(fp, 'model') == wanted:
        continue
    block = old[start:end]
    for a, b in reversed(list(spans(block))):
        if parse(block[a:b])[0] == 'model':
            block = block[:a] + block[b:]
    at = block.rfind(')')
    block = block[:at] + '\n' + ''.join(dump(m) + '\n' for m in wanted) + block[at:]
    secondary_text = secondary_text[:start] + block + secondary_text[end:]
assert strip_models(parse(old)) == strip_models(parse(secondary_text))
write_checked(secondary, old, secondary_text)

# Only R1 may change mechanically; all other footprints may change models only.
board = ROOT / 'oneTesla.kicad_pcb'
original = board.read_text()
before = parse(original)
hits = [(a,b,parse(original[a:b])) for a,b in spans(original)
        if parse(original[a:b])[0] == 'footprint' and prop(parse(original[a:b]),'Reference')[2] == 'R1']
assert len(hits) == 1
start,end,r1 = hits[0]
assert str(r1[1]).endswith('_P23.40mm_Horizontal')
r1[1] = 'oneTesla:' + NAME
child(r1, 'descr')[1] = DESCRIPTION
child(r1, 'tags')[1] = child(template, 'tags')[1]
for key, value in [('Description', DESCRIPTION), ('Footprint_Status', STATUS), ('Assembly_Notes', NOTES)]:
    prop(r1, key)[2] = value
for key,y in [('Reference',-5.8), ('Value',5.8)]:
    p=child(prop(r1,key),'at'); p[1]=A('0'); p[2]=A(str(y))
graphics = {'fp_rect','fp_line','fp_circle','fp_text','model'}
r1[:] = [v for v in r1 if not (isinstance(v,list) and v and v[0] in graphics)]
for p in children(r1,'pad'):
    child(p,'at')[1]=A('-5.08' if p[1]=='1' else '5.08')
for node in template:
    if isinstance(node,list) and node and node[0] in graphics:
        r1.append(copy.deepcopy(node))
updated = original[:start] + dump(r1,1) + original[end:]
after = parse(updated)
def omit_r1(t):
    t=strip_models(t)
    t[:] = [v for v in t if not (isinstance(v,list) and v and v[0]=='footprint' and prop(v,'Reference')[2]=='R1')]
    return t
assert omit_r1(before) == omit_r1(after)
base = parse((HERE / 'before.kicad_pcb').read_text())
assert omit_r1(base) == omit_r1(after)
before_r1=next(f for f in children(before,'footprint') if prop(f,'Reference')[2]=='R1')
for a,b in zip(children(before_r1,'pad'),children(r1,'pad')):
    assert child(a,'net')==child(b,'net') and child(a,'uuid')==child(b,'uuid')
assert child(before_r1,'at')==child(r1,'at')
write_checked(board,original,updated)
(ROOT / 'library/oneTesla.pretty' / (NAME+'.kicad_mod')).write_text(footprint_text)

# Keep the schematic's R1 association and assembly instructions in sync.
schematic=ROOT / 'oneTesla.kicad_sch'
original=schematic.read_text()
(HERE / 'before.kicad_sch').write_text(original)
updates={'Footprint':'oneTesla:'+NAME, 'Description':DESCRIPTION,
         'Footprint_Status':STATUS, 'Assembly_Notes':NOTES}
edited=[]
for start,end in spans(original):
    sym=parse(original[start:end])
    if sym[0]=='symbol' and prop(sym,'Reference') and prop(sym,'Reference')[2]=='R1':
        block=original[start:end]
        for a,b in reversed(list(spans(block))):
            p=parse(block[a:b])
            if p[0]=='property' and p[1] in updates:
                p[2]=updates[p[1]]
                block=block[:a]+dump(p,2)+block[b:]
        edited.append((start,end,block))
assert len(edited)==1
updated=original
for a,b,block in edited:updated=updated[:a]+block+updated[b:]
def normalize_sch(t):
    t=copy.deepcopy(t)
    for s in children(t,'symbol'):
        if prop(s,'Reference') and prop(s,'Reference')[2]=='R1':
            for k in updates:prop(s,k)[2]='IGNORED'
    return t
assert normalize_sch(parse(original))==normalize_sch(parse(updated))
write_checked(schematic,original,updated)

proof=dict(target_board=board.name, r1_center_and_rotation_preserved=True,
           r1_nets_and_pad_uuids_preserved=True, other_components_geometry_unchanged=True,
           tracks_zones_outline_and_four_holes_unchanged=True,
           r1_preexisting_tracks=0, pitch_before_mm=23.4,pitch_after_mm=10.16,
           autorouted_models_restored=True,autorouted_geometry_unchanged=True,
           schematic_only_r1_metadata_changed=True,
           sha256={p.name:digest(p) for p in [board,secondary,schematic]})
(HERE / 'verification.json').write_text(json.dumps(proof,indent=2)+'\n')
print(json.dumps(proof,indent=2))
