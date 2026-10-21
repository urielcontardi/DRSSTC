"""Generic visual envelope from user image; terminal dimensions remain provisional."""
from pathlib import Path
import cadquery as cq

out = Path(__file__).resolve().parents[2] / 'library/3dmodels/Visual_CP_D25_H45_P10.16.step'
assembly = cq.Assembly(name='Ketuo_1000u_200V_D25_H45_provisional_leads')
black = cq.Color(0.08, 0.09, 0.08)
silver = cq.Color(0.7, 0.72, 0.74)
body = cq.Solid.makeCylinder(12.5, 44.8, cq.Vector(0, 0, 0.1))
assembly.add(body, name='nominal_body', color=black)
for name, z in [('top', 44.9), ('bottom', 0)]:
    assembly.add(cq.Solid.makeCylinder(12.1, 0.1, cq.Vector(0, 0, z)), name=name, color=silver)
for i, x in enumerate([-5.08, 5.08]):
    assembly.add(cq.Solid.makeCylinder(0.6, 3, cq.Vector(x, 0, -3)), name=f'provisional_lead_{i}', color=silver)
assembly.export(str(out), exportType='STEP')
shape = cq.importers.importStep(str(out)).val()
assert shape.isValid()
b = shape.BoundingBox()
assert abs(b.xlen - 25) < 1e-6 and abs(b.ylen - 25) < 1e-6 and abs(b.zmax - 45) < 1e-6
print('Valid STEP: body D25 x H45; provisional P10.16 leads; no manufacturer CAD claim.')
