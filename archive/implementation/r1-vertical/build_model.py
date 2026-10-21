"""Retain the supplied AC05 body; form provisional vertical mounting leads."""
from pathlib import Path
import json
import cadquery as cq

ROOT = Path(__file__).resolve().parents[2]
original = cq.importers.importStep(str(ROOT / 'library/3dmodels/vishay_AC05.step')).val()
body = original.rotate((0, 0, 0), (0, 1, 0), -90).translate((-5.08, -7.5, 13))
bottom = cq.Solid.makeCylinder(0.4, 7, cq.Vector(-5.08, 0, -3))
points = [cq.Vector(*p) for p in [(-5.08, 0, 23), (-5.08, 0, 25),
          (-4.08, 0, 26), (4.08, 0, 26), (5.08, 0, 25), (5.08, 0, -3)]]
edges = [cq.Edge.makeLine(points[0], points[1]),
         cq.Edge.makeThreePointArc(points[1], cq.Vector(-4.78710678, 0, 25.70710678), points[2]),
         cq.Edge.makeLine(points[2], points[3]),
         cq.Edge.makeThreePointArc(points[3], cq.Vector(4.78710678, 0, 25.70710678), points[4]),
         cq.Edge.makeLine(points[4], points[5])]
path = cq.Wire.assembleEdges(edges)
upper = cq.Workplane('XY', origin=points[0].toTuple()).circle(0.4).sweep(path).val()
assembly = cq.Assembly(name='Visual_Vishay_AC05_Vertical_P10_16')
for name, shape, color in [('supplied_body', body, cq.Color(0.38, 0.65, 0.08)),
                           ('lower_lead', bottom, cq.Color(0.75, 0.76, 0.78)),
                           ('formed_upper_lead', upper, cq.Color(0.75, 0.76, 0.78))]:
    assert shape.isValid() and shape.Volume() > 0
    assembly.add(shape, name=name, color=color)
filename = ROOT / 'library/3dmodels/Visual_Vishay_AC05_Vertical_P10.16.step'
assembly.export(str(filename), exportType='STEP')
readback = cq.importers.importStep(str(filename)).val()
assert readback.isValid() and readback.Volume() > 0
b = readback.BoundingBox()
(Path(__file__).parent / 'model.json').write_text(json.dumps(dict(
    file=filename.name, body_source='library/3dmodels/vishay_AC05.step',
    lead_diameter_mm=0.8, pitch_mm=10.16, minimum_body_gap_mm=3,
    height_mm=b.zmax, bounds_mm=[b.xmin,b.ymin,b.zmin,b.xmax,b.ymax,b.zmax],
    status='Original body; generated formed leads. Assembly requires mechanical/thermal verification.'
),indent=2)+'\n')
print('STEP valid; maximum height',b.zmax,'mm')
