"""Use the DPAK package specified by the exact MC7805BDTRKG order code."""
from pathlib import Path
import copy, hashlib, json, re, shutil, sys, uuid
ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).parent
sys.path.insert(0,str(ROOT/'scripts'))
from sexpr import Atom as A, parse, dump, child, children, prop
KICAD=Path('/Applications/KiCad/KiCad.app/Contents/SharedSupport')
NAME='TO-252-3_TabPin2'
URL='https://www.onsemi.com/download/data-sheet/pdf/mc7800-d.pdf'
UPDATES={'Value':'MC7805BDTRKG','Datasheet':URL,
 'Description':'onsemi MC7805BDTRKG 5V regulator; DPAK/TO-252; pin1 input, pin2/tab ground, pin3 output.',
 'Footprint_Status':'DPAK/TO-252 per onsemi MC7800 ordering table; MC7805BDTRKG is not TO-263/D2PAK.',
 'Assembly_Notes':'1=+15V, 2/tab=GND, 3=+5V. Provide appropriate ground copper for heat dissipation in final routing.',
 'ki_fp_filters':'TO-252-3_TabPin2','KiLib_Generator':'package/TO_SOT/SMD'}
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
    for a,b,node in sorted(changes,reverse=True):s=s[:a]+dump(node,1)+s[b:]
    return s
def without_ic6(t):
    return [n for n in t if not(isinstance(n,list) and n and n[0]=='footprint' and prop(n,'Reference')[2]=='IC6')]
template=parse((KICAD/'footprints/Package_TO_SOT_SMD.pretty'/f'{NAME}.kicad_mod').read_text())
child(template,'model')[1]='${KIPRJMOD}/library/3dmodels/'+NAME+'.step'
shutil.copy2(KICAD/'3dmodels/Package_TO_SOT_SMD.3dshapes'/f'{NAME}.step',ROOT/'library/3dmodels'/f'{NAME}.step')
(ROOT/'library/oneTesla.pretty'/f'{NAME}.kicad_mod').write_text(dump(template)+'\n')
p=ROOT/'oneTesla.kicad_pcb';original=p.read_text()
assert original==(HERE/'before-oneTesla.kicad_pcb').read_text()
changes=[];pad_proof={}
for a,b in spans(original):
    fp=parse(original[a:b])
    if fp[0]!='footprint' or prop(fp,'Reference')[2]!='IC6':continue
    old=copy.deepcopy(fp);pads={pad[1]:pad for pad in children(old,'pad')}
    assert {k:str(child(v,'net')[1]) for k,v in pads.items()}=={'1':'+15V','2':'GND','3':'+5V'}
    fp[1]='oneTesla:'+NAME
    child(fp,'at')[:]=[A('at'),A('49.0'),A('87.1'),A('-90')]
    fp[:]=[n for n in fp if not(isinstance(n,list) and n and (n[0].startswith('fp_') or n[0] in ['pad','point','model','attr','descr','tags']))]
    for key in ['attr','descr','tags']:
        if child(template,key):fp.append(copy.deepcopy(child(template,key)))
    for key in ['Reference','Value']:
        field=prop(fp,key);value=field[2];old_uuid=child(field,'uuid')[1]
        field[:]=copy.deepcopy(prop(template,key));field[2]=value
        field[:]=[n for n in field if not(isinstance(n,list) and n[0]=='uuid')]
        field.append([A('uuid'),old_uuid])
        child(field,'at')[:]=[A('at'),*child(field,'at')[1:3],A('-90')]
        if key=='Reference':child(field,'at')[:]=[A('at'),A('6.5'),A('0'),A('0')]
    for key,value in UPDATES.items():
        if prop(fp,key):prop(fp,key)[2]=value
    for node in template:
        if not(isinstance(node,list) and node and (node[0].startswith('fp_') or node[0] in ['pad','model'])):continue
        n=copy.deepcopy(node)
        if n[0]!='model':
            n[:]=[v for v in n if not(isinstance(v,list) and v[0]=='uuid')]
            n.append([A('uuid'),str(uuid.uuid4())])
        if n[0] in ['pad','fp_text']:
            local=float(child(n,'at')[3]) if len(child(n,'at'))>3 else 0
            child(n,'at')[:]=[A('at'),*child(n,'at')[1:3],A(str(local-90))]
        if n[0]=='pad' and n[1]:
            oldpad=pads[n[1]]
            for key in ['net','pinfunction','pintype']:
                if child(oldpad,key):n.append(copy.deepcopy(child(oldpad,key)))
            # The original GND UUID belongs to the large tab, not the extra lead pad.
            if n[1]!='2' or float(child(n,'size')[1])>5:
                child(n,'uuid')[1]=child(oldpad,'uuid')[1]
            assert child(n,'net')==child(oldpad,'net')
        fp.append(n)
    uuids=[child(n,'uuid')[1] for n in children(fp,'pad')]
    assert len(uuids)==len(set(uuids))
    for number,oldpad in pads.items():
        assert any(child(n,'uuid')==child(oldpad,'uuid') and child(n,'net')==child(oldpad,'net') for n in children(fp,'pad') if n[1]==number)
        pad_proof[number]=str(child(oldpad,'net')[1])
    changes.append((a,b,fp))
assert len(changes)==1
updated=replace(original,changes)
assert without_ic6(parse(original))==without_ic6(parse(updated))
assert p.read_text()==original;p.write_text(updated)
p=ROOT/'oneTesla.kicad_sch';original=p.read_text();assert original==(HERE/'before-oneTesla.kicad_sch').read_text()
changes=[]
for a,b in spans(original):
    sym=parse(original[a:b])
    if sym[0]=='symbol' and prop(sym,'Reference') and prop(sym,'Reference')[2]=='IC6':
        prop(sym,'Footprint')[2]='oneTesla:'+NAME
        for key,value in UPDATES.items():
            if prop(sym,key):prop(sym,key)[2]=value
        changes.append((a,b,sym))
assert len(changes)==1
updated=replace(original,changes)
def normalize(t):
    t=copy.deepcopy(t)
    for sym in children(t,'symbol'):
        if prop(sym,'Reference') and prop(sym,'Reference')[2]=='IC6':
            for key in ['Footprint',*UPDATES]:
                if prop(sym,key):prop(sym,key)[2]='IGNORED'
    return t
assert normalize(parse(original))==normalize(parse(updated))
assert p.read_text()==original;p.write_text(updated)
assert hashlib.sha256((ROOT/'oneTesla-autorouted.kicad_pcb').read_bytes()).hexdigest()==(HERE/'autorouted.sha256').read_text().strip()
proof={'reference':'IC6','mpn':'MC7805BDTRKG','package':'DPAK/TO-252','footprint':'oneTesla:'+NAME,
       'pin_nets':pad_proof,'tab_number':'2','tab_net':'GND','original_pad_uuids_preserved':True,
       'other_board_objects_unchanged':True,'schematic_electrical_geometry_unchanged':True,'autorouted_unchanged':True,
       'position_after_mm':[49.0,87.1],'rotation_after_deg':-90,
       'source':URL,'retailer_TO263_description_conflicts_with_exact_part_code':True}
(HERE/'verification.json').write_text(json.dumps(proof,indent=2)+'\n')
print(json.dumps(proof,indent=2))
