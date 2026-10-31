"""Alternative height shims. Print four equal stacks; selected nominal stack is 4+1 mm."""
from pathlib import Path
import cadquery as cq
out=Path(__file__).resolve().parent/'exports'/'print'/'spare-shims';out.mkdir(parents=True,exist_ok=True)
for t in (.5,1,2,4,8):
 s=cq.Solid.makeCylinder(6,t).cut(cq.Solid.makeCylinder(1.7,t+2,cq.Vector(0,0,-1)))
 s=s.translate((6,6,0));assert s.isValid()
 cq.exporters.export(s,str(out/f'shim_{str(t).replace(".","p")}mm_PRINT_4_PER_LAYER.stl'))
print('5 spare shim sizes exported')
