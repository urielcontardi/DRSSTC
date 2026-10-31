"""Three open seats to check the selected 3 mm OD copper tube against the printer."""
from pathlib import Path
import cadquery as cq
out=Path(__file__).resolve().parent/'exports'
s=cq.Solid.makeBox(30,16,8)
for x,d in [(7,3.2),(15,3.4),(23,3.6)]:
    s=s.cut(cq.Solid.makeCylinder(d/2,18,cq.Vector(x,-1,8),cq.Vector(0,1,0)))
assert s.isValid() and len(s.Solids())==1
for ext in ['stl','step']:cq.exporters.export(s,str(out/f'08_primary_fit_coupon.{ext}'))
print('Fit coupon: 30 × 16 × 8 mm; grooves left to right: 3.2, 3.4, 3.6 mm')
