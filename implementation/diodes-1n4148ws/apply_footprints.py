"""Replace the two THT signal diodes with 1N4148WS SOD-323."""
from pathlib import Path
import copy, hashlib, json, math, re, shutil, sys, uuid
ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).parent
sys.path.insert(0,str(ROOT/'scripts'))
from sexpr import Atom as A, parse, dump, child, children, prop
REFS={'D1','D2'}
NAME='D_SOD-323_HandSoldering'
URL='https://www.vishay.com/docs/86455/1n4148ws.pdf'
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

template=parse((KICAD/'footprints/Diode_SMD.pretty'/f'{NAME}.kicad_mod').read_text())
child(template,'model')[1]='${KIPRJMOD}/library/3dmodels/D_SOD-323.step'
model=ROOT/'library/3dmodels/D_SOD-323.step'
shutil.copy2(KICAD/'3dmodels/Diode_SMD.3dshapes/D_SOD-323.step',model)
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
    assert set(pads)=={'1','2'} and prop(f,'Value')[2]=='1N4148'
    assert child(pads['1'],'pinfunction')[1]=='K_1' and child(pads['2'],'pinfunction')[1]=='A_2'
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
        field=prop(f,key);value='1N4148WS' if key=='Value' else field[2]
        field[:]=copy.deepcopy(prop(template,key));field[2]=value
        child(field,'at')[:]=[A('at'),*child(field,'at')[1:3],A(str(angle))]
        if key=='Reference':child(field,'at')[2]=A('1.85')
        field.append([A('uuid'),str(uuid.uuid4())])
    for key in ['Description','Footprint_Status']:
        if prop(f,key):prop(f,key)[2]='1N4148WS, SOD-323; pad1=cathode, pad2=anode; hand-solder pads.'
    if prop(f,'KiLib_Generator'):prop(f,'KiLib_Generator')[2]='diode/SMD'
    prop(f,'Datasheet')[2]=URL
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
assert len(changes)==2
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
        prop(sym,'Value')[2]='1N4148WS'
        prop(sym,'Datasheet')[2]=URL
        if prop(sym,'Footprint_Status'):prop(sym,'Footprint_Status')[2]='1N4148WS in SOD-323; 1=cathode/2=anode; pads for hand soldering.'
        changes.append((a,b,sym))
assert len(changes)==2
updated=replace(original,changes)
def strip_changed_properties(t):
    t=copy.deepcopy(t)
    for sym in children(t,'symbol'):
        if prop(sym,'Reference') and prop(sym,'Reference')[2] in REFS:
            for key in ['Footprint','Footprint_Status','Value','Datasheet']:
                if prop(sym,key):prop(sym,key)[2]='IGNORED'
    return t
assert strip_changed_properties(parse(original))==strip_changed_properties(parse(updated))
assert p.read_text()==original
p.write_text(updated)
assert hashlib.sha256((ROOT/'oneTesla-autorouted.kicad_pcb').read_bytes()).hexdigest()==(HERE/'autorouted.sha256').read_text().strip()
proof={'target':'oneTesla.kicad_pcb','references':sorted(REFS),'footprint':'oneTesla:'+NAME,
       'values_updated':'1N4148WS','pad_numbers_nets_functions_uuids_preserved':True,
       'body_centers_and_rotations_preserved':centers,'all_other_board_objects_unchanged':True,
       'schematic_only_two_diode_values_footprints_datasheets_and_status_updated':True,'autorouted_unchanged':True}
(HERE/'verification.json').write_text(json.dumps(proof,indent=2)+'\n')
print(json.dumps(proof,indent=2))
