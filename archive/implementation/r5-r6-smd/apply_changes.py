from pathlib import Path
import sys, copy, csv, json, math, re, uuid
ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).parent
sys.path.insert(0, str(ROOT / 'scripts'))
from sexpr import Atom as A, parse, dump, children, child, prop
REFS = {'R5', 'R6'}
NAME = 'R_Uniroyal_HV12_2512_P6.60mm'
FP = 'oneTesla:' + NAME
DESC = '100k 0.5W resistor, SMD 2512, pad pitch 6.60mm'
STATUS = 'SMD 2512 land pattern, 6.60mm pad pitch; value100k0.5W preserved; no MPN selected.'
template = parse((ROOT / 'library/oneTesla.pretty' / (NAME + '.kicad_mod')).read_text())

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
    for a,b,n in sorted(edits, reverse=True): s = s[:a] + dump(n,1) + s[b:]
    return s

def outside_targets(s, typ):
    t = parse(s)
    return [n for n in t if not (isinstance(n,list) and n and n[0] == typ and prop(n,'Reference') and prop(n,'Reference')[2] in REFS)]

pcb = ROOT / 'oneTesla.kicad_pcb'
sch = ROOT / 'oneTesla.kicad_sch'
originals = {p: p.read_text() for p in (pcb, sch)}
for p,s in originals.items(): (HERE / ('before-' + p.name)).write_text(s)
edits = []
proof = {}
for a,b in spans(originals[pcb]):
    f = parse(originals[pcb][a:b])
    if f[0] != 'footprint' or prop(f,'Reference')[2] not in REFS: continue
    ref = prop(f,'Reference')[2]
    assert child(f,'layer')[1] == 'F.Cu'
    assert prop(f,'Value')[2] == '100k 0.5W'
    old = copy.deepcopy(f)
    pads = {n[1]: n for n in children(f,'pad')}
    at = child(f,'at')
    ang = float(at[3]) if len(at)>3 else 0.0
    # Align the centered SMD origin with the midpoint of the former THT pads.
    assert [float(x) for x in child(pads['1'],'at')[1:3]] == [0,0]
    assert [float(x) for x in child(pads['2'],'at')[1:3]] == [5.08,0]
    at[1] = A(str(round(float(at[1]) + 2.54*math.cos(math.radians(ang)),6)))
    at[2] = A(str(round(float(at[2]) - 2.54*math.sin(math.radians(ang)),6)))
    f[1] = FP
    prop(f,'Description')[2] = DESC
    prop(f,'Footprint_Status')[2] = STATUS
    prop(f,'KiLib_Generator')[2] = 'SMD_2terminal_chip_molded'
    # Keep existing text positions in board coordinates and preserve hidden values.
    for field in children(f,'property'):
        if child(field,'at'):
            child(field,'at')[1] = A(str(round(float(child(field,'at')[1])-2.54,6)))
    f[:] = [n for n in f if not (isinstance(n,list) and n and (n[0].startswith('fp_') or n[0] in {'pad','model','attr','descr','tags'}))]
    for key in ['descr','tags','attr']:
        if child(template,key): f.append(copy.deepcopy(child(template,key)))
    for node in template:
        if not (isinstance(node,list) and node and (node[0].startswith('fp_') or node[0] in {'pad','model'})): continue
        n = copy.deepcopy(node)
        if n[0] != 'model': n.append([A('uuid'),str(uuid.uuid4())])
        if n[0] in {'pad','fp_text'}: child(n,'at')[3:] = [A(str(ang))]
        if n[0] == 'pad':
            for key in ['uuid','net','pintype','pinfunction']:
                n[:] = [v for v in n if not (isinstance(v,list) and v and v[0] == key)]
                if child(pads[n[1]],key): n.append(copy.deepcopy(child(pads[n[1]],key)))
        f.append(n)
    for n in children(f,'pad'):
        assert n[2] == 'smd' and child(n,'drill') is None
        for key in ['uuid','net','pintype','pinfunction']: assert child(n,key) == child(pads[n[1]],key)
    assert child(prop(f,'Value'),'hide') == child(prop(old,'Value'),'hide')
    assert child(f,'uuid') == child(old,'uuid')
    proof[ref] = {'footprint':FP,'value':prop(f,'Value')[2], 'old_origin':list(child(old,'at')[1:]), 'new_center':list(at[1:]), 'pad_nets':{p[1]:child(p,'net')[1:] for p in children(f,'pad')}}
    edits.append((a,b,f))
assert len(edits) == 2
updated_pcb = replace(originals[pcb],edits)
assert outside_targets(originals[pcb],'footprint') == outside_targets(updated_pcb,'footprint')
edits = []
updates = {'Footprint':FP,'Description':DESC,'Footprint_Status':STATUS}
for a,b in spans(originals[sch]):
    sym = parse(originals[sch][a:b])
    if sym[0] == 'symbol' and prop(sym,'Reference') and prop(sym,'Reference')[2] in REFS:
        for key,value in updates.items(): prop(sym,key)[2] = value
        edits.append((a,b,sym))
assert len(edits) == 2
updated_sch = replace(originals[sch],edits)
def normalize(s):
    t = parse(s)
    for sym in children(t,'symbol'):
        if prop(sym,'Reference') and prop(sym,'Reference')[2] in REFS:
            for key in updates: prop(sym,key)[2] = 'MASKED'
    return t
assert normalize(originals[sch]) == normalize(updated_sch)
for p,s in originals.items(): assert p.read_text() == s, 'Concurrent edit detected'
pcb.write_text(updated_pcb)
sch.write_text(updated_sch)
p = ROOT / 'output/components.csv'
with p.open(newline='') as f: rows = list(csv.reader(f))
for row in rows:
    if row and row[0] in REFS: row[2],row[4],row[5] = FP,STATUS,'SMD footprint: ' + FP
with p.open('w',newline='') as f: csv.writer(f).writerows(rows)
proof.update({'all_other_pcb_objects_preserved':True,'schematic_connectivity_preserved':True,'pad_uuids_and_nets_preserved':True,'hidden_values_preserved':True,'former_pad_midpoints_preserved':True})
(HERE / 'verification.json').write_text(json.dumps(proof,indent=2)+'\n')
(HERE / 'RESULTADO.md').write_text('# R5 e R6 em SMD\n\nR5 e R6 convertidos para o footprint local SMD2512 anteriormente usado, com passo entre pads de6,60mm. Valores100kΩ/0,5W e conexões preservados. Esquema sincronizado. Centros alinhados ao ponto médio dos antigos pads THT e orientação preservada. Valores continuam ocultos na PCB. Nenhum outro objeto da PCB foi alterado, incluindo furos e roteamento.\n\nConferência estrutural em `verification.json`; backups anteriores à troca nesta pasta. Nenhum MPN foi atribuído.\n')
print(json.dumps(proof,indent=2))
