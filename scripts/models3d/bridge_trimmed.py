"""KBU visual with leads trimmed 1 mm below the 1.6 mm PCB."""
from pathlib import Path
import cadquery as cq

root = Path(__file__).resolve().parents[2]
source = Path('/Applications/KiCad/KiCad.app/Contents/SharedSupport/3dmodels/Diode_THT.3dshapes/Diode_Bridge_Vishay_KBU.step')
shape = cq.importers.importStep(str(source)).val()
assembly = cq.Assembly(name='KBU_trimmed_leads')
body = shape.intersect(cq.Solid.makeBox(100, 100, 100, cq.Vector(-40, -40, 0)))
leads = shape.intersect(cq.Solid.makeBox(100, 100, 2.6, cq.Vector(-40, -40, -2.6)))
assembly.add(body, name='body', color=cq.Color(0.07, 0.08, 0.09))
assembly.add(leads, name='trimmed_leads', color=cq.Color(0.72, 0.74, 0.76))
out = root / 'hardware/pcb/library/3dmodels/Visual_Diode_Bridge_Vishay_KBU_Trimmed.step'
assembly.export(str(out), exportType='STEP')
result = cq.importers.importStep(str(out)).val()
assert result.isValid()
a, b = shape.BoundingBox(), result.BoundingBox()
for before, after in [(a.xmin,b.xmin), (a.xmax,b.xmax), (a.ymin,b.ymin),
                      (a.ymax,b.ymax), (a.zmax,b.zmax), (-2.6,b.zmin)]:
    assert abs(before-after) < 1e-6
print('Valid STEP: body unchanged; leads end at -2.6 mm (1 mm below PCB).')
