"""Bottom IGBT: metal outward, below 1.6 mm PCB; provisional bent leads."""
from pathlib import Path
import cadquery as cq

root = Path(__file__).resolve().parents[2]
folder = root / 'library/3dmodels'
source = cq.importers.importStep(str(folder / 'Visual_FGA60N65SMD_Horizontal_P5.45.step')).val()
assembly = cq.Assembly(name='IGBT_horizontal_bottom_P5_45')
solids = source.Solids()
body = max(solids, key=lambda s: s.Volume())
for i, solid in enumerate(solids):
    # Preserve the case's metal-down orientation, placing its plastic top
    # against the underside of the board. Re-form vertical pins through PCB.
    if i >= 3 and i % 2 == 0:
        x = (i - 4) / 2 * 5.45
        mirrored = cq.Solid.makeBox(1, 0.65, 4.15, cq.Vector(x - 0.5, -0.325, -3.25))
    else:
        mirrored = solid.translate((0, 0, -6.6))
    assert mirrored.isValid()
    assembly.add(mirrored, name=f'part_{i}',
                 color=cq.Color(0.07, 0.08, 0.09) if solid is body else cq.Color(0.72, 0.74, 0.76))
out = folder / 'Visual_FGA60N65SMD_Horizontal_Bottom_P5.45.step'
assembly.export(str(out), exportType='STEP')
result = cq.importers.importStep(str(out)).val()
assert result.isValid()
a, b = source.BoundingBox(), result.BoundingBox()
for before, after in [(a.xmin, b.xmin), (a.xmax, b.xmax), (a.ymin, b.ymin),
                      (a.ymax, b.ymax), (solids[2].BoundingBox().zmin - 6.6, b.zmin), (0.9, b.zmax)]:
    assert abs(before - after) < 1e-6
metal = result.Solids()[1].BoundingBox()
assert abs(metal.zmin + 6.6) < 1e-6 and metal.zmax < -4.9
print('Valid bottom IGBT STEP; metal outward at Z=-6.6; pins reach Z=0.9 mm.')
