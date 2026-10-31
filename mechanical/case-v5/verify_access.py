"""Check a short coaxial driver envelope at each head, honoring preassembly order."""
from pathlib import Path
import json,math
import cadquery as cq
ROOT=Path(__file__).resolve().parent;OUT=ROOT/'exports'
v=json.loads((OUT/'verification.json').read_text());assert not v['failures']
printed={p['name']:cq.importers.importStep(str(OUT/(p['name']+'.step'))).val() for p in v['printed_parts']}
pcb=cq.importers.importStep(str(ROOT/'reference/ARCSTRIKE-PCB-complete.step')).val().translate((-31.375,127.05,0))
top=52+280
tube=cq.Solid.makeCylinder(30,280,cq.Vector(50,50,52)).cut(cq.Solid.makeCylinder(28.5,282,cq.Vector(50,50,51)))
toroid=cq.Solid.makeTorus(55,20,cq.Vector(50,50,top+20),cq.Vector(0,0,1))
def overlap(a,b):
 x,y=a.BoundingBox(),b.BoundingBox()
 if any(min(getattr(x,k+'max'),getattr(y,k+'max'))-max(getattr(x,k+'min'),getattr(y,k+'min'))<1e-5 for k in 'xyz'):return 0
 return max(0,a.intersect(b).Volume())
checks=[];fail=[]
for j in v['joints']:
 d=int(j['screw'][1]);head_h=d;axis=cq.Vector(*j['axis']);seat=cq.Vector(*j['seat']);start=seat-axis.multiply(head_h+.15)
 tool=cq.Solid.makeCylinder(1.8 if d==3 else 2.2,25,start,axis.multiply(-1))
 refs={**printed,'PCB':pcb,'tube':tube}
 if j['name'].startswith('Cradle_'):
  refs={k:s for k,s in refs.items() if not k.startswith('08_adjustable_heatsink_finger_')}
 # These four screws and the bottom M4 are tightened on the table before the toroid/tube is fitted.
 stage='top module preassembly' if j['name'].startswith('Top_cap_') or j['name']=='Toroid' else ('cradle before heatsink and sliding fingers' if j['name'].startswith('Cradle_') else 'assembly sequence')
 if stage!='top module preassembly':refs['toroid']=toroid
 for name,s in refs.items():
  vol=overlap(tool,s);checks.append(dict(joint=j['name'],stage=stage,reference=name,overlap_mm3=vol))
  if vol>.02:fail.append(checks[-1])
(OUT/'tool-access-verification.json').write_text(json.dumps(dict(driver_length_mm=25,M3_driver_diameter_mm=3.6,M4_driver_diameter_mm=4.4,checks=checks,failures=fail),indent=2)+'\n')
print('Driver checks:',len(checks),'failures:',fail)
assert not fail,fail
