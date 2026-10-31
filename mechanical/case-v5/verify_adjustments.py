"""Conservative adjustment checks; solid occupied box avoids relying on a fin pattern."""
from pathlib import Path
import json
import cadquery as cq
R=Path(__file__).resolve().parent;O=R/'exports'
v=json.loads((O/'verification.json').read_text())
base=cq.importers.importStep(str(O/'01_lower_tray.step')).val()
pcb=cq.importers.importStep(str(R/'reference/ARCSTRIKE-PCB-complete.step')).val().translate((-31.375,127.05,0))
fingers=[cq.importers.importStep(str(O/f'08_adjustable_heatsink_finger_{i+1}.step')).val() for i in range(4)]
cradle=cq.importers.importStep(str(O/'13_universal_heatsink_cradle.step')).val()
top=-5.305
checks=[];fail=[]
def overlap(a,b):
 x,y=a.BoundingBox(),b.BoundingBox()
 if any(min(getattr(x,k+'max'),getattr(y,k+'max'))-max(getattr(x,k+'min'),getattr(y,k+'min'))<1e-5 for k in 'xyz'):return 0
 return max(0,a.intersect(b).Volume())
def ck(label,a,name,b):
 vol=overlap(a,b);d=dict(case=label,reference=name,overlap_mm3=vol);checks.append(d)
 if vol>.02:fail.append(d)
for w in (96,100,104,108,112):
 for length in (96,100,104,108,112):
  env=cq.Solid.makeBox(w,length,25,cq.Vector(50-w/2,50-length/2,top-25))
  label=f'W{w}_L{length}'
  ck(label,env,'base',base);ck(label,env,'PCB',pcb)
  ds=[((104-w)/2,0,0),(-(104-w)/2,0,0),(0,(100-length)/2,0),(0,-(100-length)/2,0)]
  for i,(f,d) in enumerate(zip(fingers,ds)):
   f=f.translate(d)
   for name,ref in [('base',base),('PCB',pcb),('sink occupied box',env)]:ck(label+f'_finger{i+1}',f,name,ref)
for height in (20,25,30):
 c=cradle.translate((0,0,25-height));env=cq.Solid.makeBox(104,100,height,cq.Vector(-2,0,top-height))
 for name,ref in [('base',base),('PCB',pcb),('sink occupied box',env)]:ck(f'H{height}_cradle',c,name,ref)
(O/'adjustment-verification.json').write_text(json.dumps(dict(status='conservative box and clamp endpoints; no thermal qualification',checks=checks,failures=fail),indent=2)+'\n')
print('Adjustment checks',len(checks),'failures',fail)
assert not fail,fail
