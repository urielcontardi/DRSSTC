from pathlib import Path
import subprocess,sys,json,hashlib
r=Path(__file__).resolve().parents[2];sys.path.insert(0,str(r/'scripts'));from sexpr import *
b=parse((r/'oneTesla.kicad_pcb').read_text());a=parse(subprocess.check_output(['git','show','028ef6e:oneTesla.kicad_pcb'],cwd=r,text=True));old={child(f,'uuid')[1]:f for f in children(a,'footprint')};changes=[]
assert len(children(b,'footprint'))==len(old)
for f in children(b,'footprint'):
 o=old[child(f,'uuid')[1]];ref=prop(f,'Reference')[2]
 assert {p[1]:child(p,'net')[1] for p in children(o,'pad') if child(p,'net')}=={p[1]:child(p,'net')[1] for p in children(f,'pad') if child(p,'net')}
 if child(o,'at')!=child(f,'at'):changes.append(ref)
 if ref not in ['C11','C12','R5','R6']:assert child(o,'at')==child(f,'at')
 if ref!='R1':assert [(p[1],child(p,'at'),child(p,'drill')) for p in children(o,'pad')]==[(p[1],child(p,'at'),child(p,'drill')) for p in children(f,'pad')]
assert set(changes)=={'C11','C12','R5','R6'}
pts=[]
for g in b:
 if isinstance(g,list) and child(g,'layer') and child(g,'layer')[1]=='Edge.Cuts':
  for key in ['start','end']:
   v=child(g,key)
   if v:pts.append(tuple(float(q) for q in v[1:3]))
assert (min(x for x,y in pts),max(x for x,y in pts),min(y for x,y in pts),max(y for x,y in pts))==(0,145,-2,106.045)
def nets(p):
 t=parse((r/p).read_text());return {child(n,'name')[1]:sorted((child(v,'ref')[1],child(v,'pin')[1]) for v in children(n,'node')) for n in children(child(t,'nets'),'net')}
assert nets('implementation/evidence/final-oneTesla.net')==nets('implementation/expansion/final.net')
x=json.loads((r/'implementation/expansion/drc-final.json').read_text());assert not x['unconnected_items'];assert not [v for v in x['violations'] if v['type'] in ['shorting_items','clearance','tracks_crossing','starved_thermal','hole_clearance','copper_edge_clearance']]
paths=['oneTesla.kicad_pcb','oneTesla.kicad_sch','implementation/expansion/drc-final.json','implementation/expansion/final.net']
proof='PASS: dimensions145x108.045; mounting holes unchanged; pad nets identical; netlist identical; zero shorts/clearance/crossings/unconnected/thermal/hole/edge errors.'+chr(10)+chr(10).join(hashlib.sha256((r/p).read_bytes()).hexdigest()+' '+p for p in paths)+chr(10)
(r/'implementation/expansion/final-proof.txt').write_text(proof);print(proof)
