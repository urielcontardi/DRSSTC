"""Nominal visual envelope only, from Bourns PWR8030 dimensional drawing."""
from pathlib import Path
import cadquery as cq

out = Path(__file__).resolve().parents[2]/'library/3dmodels/Visual_Bourns_PWR8030.step'
assembly = cq.Assembly(name='PWR8030_nominal_envelope')
body = cq.Workplane('XY').box(20.8,7.6,7.5,centered=(True,True,False)).translate((0,0,.3))
assembly.add(body,name='ceramic_body',color=cq.Color(.88,.87,.81))
for side in [-1,1]:
    terminal = cq.Workplane('XY').box(3,4.8,.3,centered=(True,True,False)).translate((side*8.9,0,0))
    assembly.add(terminal,name='terminal_'+str(side).replace('-','minus'),color=cq.Color(.67,.68,.7))
assembly.export(str(out))
model=cq.importers.importStep(str(out))
assert all(s.isValid() for s in model.solids().vals())
b=model.val().BoundingBox()
assert abs(b.xlen-20.8)<.001 and abs(b.ylen-7.6)<.001 and abs(b.zlen-7.8)<.001
print(out, 'valid STEP', (b.xlen,b.ylen,b.zlen))
