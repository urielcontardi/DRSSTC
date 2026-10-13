"""Change only the five ceramic supply-bypass capacitor footprints."""
from pathlib import Path
import copy, hashlib, json, math, re, shutil, sys, uuid
ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).parent
sys.path.insert(0,str(ROOT/'scripts'))
from sexpr import Atom as A, parse, dump, child, children, prop
REFS={'C1','C2','C3','C5','C6'}
NAME='C_0805_2012Metric_Pad1.18x1.45mm_HandSolder'
KICAD=Path('/Applications/KiCad/KiCad.app/Contents/SharedSupport')

def spans(s):
    depth=0
    for m in re.finditer(r'"(?:\\.|[^"\\])*"|[()]',s):
        if m.group()=='(':
            depth+=1
            if depth==2:a=m.start()
        elif m.group()==')':
            if depth==2:yield a,m.end()
            depth-=1
def replace(s,changes):
    for a,b,n in sorted(changes,reverse=True):s=s[:a]+dump(n,1)+s[b:]
    return s
def omit(t):
    return [v for v in t if not(isinstance(v,list) and v and v[0]=='footprint' and prop(v,'Reference')[2] in REFS)]

template=parse((KICAD/'footprints/Capacitor_SMD.pretty'/f'{NAME}.kicad_mod').read_text())
child(template,'model')[1]='${KIPRJMOD}/library/3dmodels/C_0805_2012Metric.step'
model=ROOT/'library/3dmodels/C_0805_2012Metric.step'
shutil.copy2(KICAD/'3dmodels/Capacitor_SMD.3dshapes/C_0805_2012Metric.step',model)
(ROOT/'library/oneTesla.pretty'/f'{NAME}.kicad_mod').write_text(dump(template)+'\n')

p=ROOT/'oneTesla.kicad_pcb';original=p.read_text()
assert original==(HERE/'before-oneTesla.kicad_pcb').read_text(),'Concurrent PCB edit; rebase first'
changes=[]
centers={}
for a,b in spans(original):
    f=parse(original[a:b])
    if f[0]!='footprint' or prop(f,'Reference')[2] not in REFS:continue
    ref=prop(f,'Reference')[2];old=copy.deepcopy(f)
    pads={pad[1]:pad for pad in children(f,'pad')}
    assert set(pads)=={'1','2'} and prop(f,'Value')[2]=='1u'
    assert {str(child(pad,'net')[1]) for pad in pads.values()} in [{'+5V','GND'},{'+15V','GND'}]
    at=child(f,'at');angle=float(at[3]) if len(at)>3 else 0
    cx=sum(float(child(pad,'at')[1]) for pad in pads.values())/2
    cy=sum(float(child(pad,'at')[2]) for pad in pads.values())/2
    rad=math.radians(angle)
    at[1]=A(str(round(float(at[1])+cx*math.cos(rad)+cy*math.sin(rad),6)))
    at[2]=A(str(round(float(at[2])-cx*math.sin(rad)+cy*math.cos(rad),6)))
    centers[ref]=[str(v) for v in at[1:]]
    f[1]='oneTesla:'+NAME
    f[:]=[n for n in f if not(isinstance(n,list) and n and (n[0].startswith('fp_') or n[0] in ['pad','model','point','attr','descr','tags']))]
    for key in ['attr','descr','tags']:
        f.append(copy.deepcopy(child(template,key)))
    for key in ['Reference','Value']:
        field=prop(f,key);value=field[2]
        field[:]=copy.deepcopy(prop(template,key));field[2]=value
        child(field,'at')[:]=[A('at'),*child(field,'at')[1:3],A(str(angle))]
        if ref=='C6' and key=='Reference':child(field,'at')[2]=A('1.68')
        field.append([A('uuid'),str(uuid.uuid4())])
    for key in ['Description','Footprint_Status']:
        if prop(f,key):prop(f,key)[2]='SMD 0805, hand-solder pads; original 1u value and connections preserved.'
    if prop(f,'KiLib_Generator'):prop(f,'KiLib_Generator')[2]='SMD_2terminal_chip_molded'
    for node in template:
        if not(isinstance(node,list) and node and (node[0].startswith('fp_') or node[0] in ['pad','model'])):continue
        n=copy.deepcopy(node)
        if n[0]!='model':
            n[:]=[v for v in n if not(isinstance(v,list) and v[0]=='uuid')]
            n.append([A('uuid'),str(uuid.uuid4())])
        if n[0]=='pad':
            pad=pads[n[1]]
            child(n,'at')[:]=[A('at'),*child(n,'at')[1:3],A(str(angle))]
            for key in ['uuid','net','pintype','pinfunction']:
                n[:]=[v for v in n if not(isinstance(v,list) and v[0]==key)]
                if child(pad,key):n.append(copy.deepcopy(child(pad,key)))
        elif n[0]=='fp_text':
            child(n,'at')[:]=[A('at'),*child(n,'at')[1:3],A(str(angle))]
        f.append(n)
    for pad in children(f,'pad'):
        for key in ['uuid','net','pintype','pinfunction']:assert child(pad,key)==child(pads[pad[1]],key)
    changes.append((a,b,f))
assert len(changes)==5
updated=replace(original,changes)
assert omit(parse(original))==omit(parse(updated))
assert p.read_text()==original
p.write_text(updated)

p=ROOT/'oneTesla.kicad_sch';original=p.read_text()
assert original==(HERE/'before-oneTesla.kicad_sch').read_text(),'Concurrent schematic edit'
changes=[]
for a,b in spans(original):
    sym=parse(original[a:b])
    if sym[0]=='symbol' and prop(sym,'Reference') and prop(sym,'Reference')[2] in REFS:
        prop(sym,'Footprint')[2]='oneTesla:'+NAME
        if prop(sym,'Footprint_Status'):prop(sym,'Footprint_Status')[2]='SMD 0805; pads for hand soldering.'
        changes.append((a,b,sym))
assert len(changes)==5
updated=replace(original,changes)
def strip_changed_properties(t):
    t=copy.deepcopy(t)
    for sym in children(t,'symbol'):
        if prop(sym,'Reference') and prop(sym,'Reference')[2] in REFS:
            for key in ['Footprint','Footprint_Status']:
                if prop(sym,key):prop(sym,key)[2]='IGNORED'
    return t
assert strip_changed_properties(parse(original))==strip_changed_properties(parse(updated))
assert p.read_text()==original
p.write_text(updated)
assert hashlib.sha256((ROOT/'oneTesla-autorouted.kicad_pcb').read_bytes()).hexdigest()==(HERE/'autorouted.sha256').read_text().strip()
proof={'target':'oneTesla.kicad_pcb','references':sorted(REFS),'footprint':'oneTesla:'+NAME,
       'values_unchanged':True,'pad_numbers_nets_functions_uuids_preserved':True,
       'body_centers_and_rotations_preserved':centers,'all_other_board_objects_unchanged':True,
       'schematic_only_five_footprint_associations_and_status_updated':True,'autorouted_unchanged':True}
(HERE/'verification.json').write_text(json.dumps(proof,indent=2)+'\n')
print(json.dumps(proof,indent=2))
