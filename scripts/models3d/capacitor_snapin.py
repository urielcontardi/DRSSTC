"""Generic mechanical envelope, not manufacturer CAD. Dimensions supplied by user."""
from pathlib import Path
import cadquery as cq

ROOT = Path(__file__).resolve().parents[2]
for pitch in (9.0, 10.0):
    name = f'Visual_CP_D30.3_H40.5_P{pitch:.2f}'
    assembly = cq.Assembly(name=name)
    silver = cq.Color(0.72, 0.74, 0.76)
    assembly.add(cq.Solid.makeCylinder(15.15, 40.3, cq.Vector(0, 0, 0.1)),
                 name='sleeve', color=cq.Color(0.07, 0.08, 0.09))
    for label, z in [('bottom', 0), ('top', 40.4)]:
        assembly.add(cq.Solid.makeCylinder(14.8, 0.1, cq.Vector(0, 0, z)),
                     name=label, color=silver)
    for i, x in enumerate((-pitch / 2, pitch / 2)):
        assembly.add(cq.Solid.makeCylinder(0.6, 3.1, cq.Vector(x, 0, -3)),
                     name=f'provisional_terminal_{i+1}', color=silver)
    path = ROOT / 'hardware/pcb/library' / '3dmodels' / f'{name}.step'
    assembly.export(str(path), exportType='STEP')
    shape = cq.importers.importStep(str(path)).val()
    assert shape.isValid()
    box = shape.BoundingBox()
    assert abs(box.xlen - 30.3) < 1e-6
    assert abs(box.ylen - 30.3) < 1e-6
    assert abs(box.zmax - 40.5) < 1e-6
    print(f'{path.name}: valid; D30.3 x H40.5 mm; pitch {pitch} mm')
