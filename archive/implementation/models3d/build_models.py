"""Build explicitly provisional 3D visuals without modifying PCB geometry.

Run with CadQuery 2.8. Downloaded catalog STEP originals are retained separately.
Dimensions and sources are recorded in sources.json; no electrical part is selected.
"""
from pathlib import Path
import json
import math
import cadquery as cq

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'library' / '3dmodels'
KICAD = Path('/Applications/KiCad/KiCad.app/Contents/SharedSupport/3dmodels')
OUT.mkdir(exist_ok=True)
SILVER = cq.Color(0.72, 0.74, 0.76)
BLACK = cq.Color(0.07, 0.08, 0.09)
sources = []


def cylinder(radius, start, end):
    vector = cq.Vector(end).sub(cq.Vector(start))
    return cq.Solid.makeCylinder(radius, vector.Length, cq.Vector(start), vector.normalized())


def save(name, pieces, refs, note, source):
    assembly = cq.Assembly(name=name)
    for i, (shape, color) in enumerate(pieces):
        assert shape.isValid(), (name, i)
        assembly.add(shape, name=f'part_{i}', color=color)
    path = OUT / (name + '.step')
    assembly.export(str(path), exportType='STEP')
    readback = cq.importers.importStep(str(path)).val()
    assert readback.isValid() and readback.Volume() > 0
    box = readback.BoundingBox()
    sources.append(dict(file=path.name, references=refs, status='visual_approximation',
                        note=note, source=source,
                        bounds_mm=[box.xmin, box.ymin, box.zmin,
                                   box.xmax, box.ymax, box.zmax]))


def radial(name, diameter, pitch, library_name, refs):
    src = KICAD / 'Capacitor_THT.3dshapes' / library_name
    original = cq.importers.importStep(str(src)).val()
    height = original.BoundingBox().zmax
    # Retain the generic KiCad body geometry and height. Re-form only its leads.
    source_pitch = float(library_name.split('_P')[1].split('mm')[0])
    original = original.translate((-source_pitch / 2, 0, 0))
    body = original.intersect(cq.Solid.makeBox(100, 100, height - 0.45, cq.Vector(-50, -50, 0.3)))
    parts = [(body, BLACK)]
    for x in [-pitch / 2, pitch / 2]:
        parts.append((cylinder(0.3 if diameter < 20 else 0.6,
                               (x, 0, -3), (x, 0, 0.6)), SILVER))
    parts.append((cylinder(diameter / 2 - 0.2, (0, 0, height - 0.15),
                          (0, 0, height)), SILVER))
    save(name, parts, refs,
         f'Generic D{diameter} body, H{height:.3f} from KiCad; formed lead pitch {pitch}. '
         'Actual capacitor MPN/height and snap-in details are unconfirmed.',
         f'https://gitlab.com/kicad/libraries/kicad-packages3D/-/blob/master/Capacitor_THT.3dshapes/{library_name}')


radial('Visual_CP_D8_P2.54', 8, 2.54, 'CP_Radial_D8.0mm_P2.50mm.step', ['C8', 'C9', 'C13'])
radial('Visual_CP_D12.5_P3.556', 12.5, 3.556, 'CP_Radial_D12.5mm_P5.00mm.step', ['C10'])
radial('Visual_CP_D30_P10.16', 30, 10.16, 'CP_Radial_D30.0mm_P10.00mm_SnapIn.step', ['C11', 'C12'])

for name, folder, library_name, length, pitch, radius, refs, color in [
    ('Visual_R_L9_P10.16', 'Resistor_THT.3dshapes',
     'R_Axial_DIN0309_L9.0mm_D3.2mm_P12.70mm_Horizontal.step', 9, 10.16, 0.3, ['R5', 'R6'], cq.Color(0.65, 0.52, 0.34)),
    ('Visual_TVS_DO201AD_P14.732', 'Diode_THT.3dshapes',
     'D_DO-201AD_P15.24mm_Horizontal.step', 9.5, 14.732, 0.5, ['Z1', 'Z2'], BLACK),
]:
    source_pitch = float(library_name.split('_P')[1].split('mm')[0])
    original = cq.importers.importStep(str(KICAD / folder / library_name)).val().translate((-source_pitch / 2, 0, 0))
    body = original.intersect(cq.Solid.makeBox(length, 40, 40, cq.Vector(-length / 2, -20, -10)))
    height = (body.BoundingBox().zmin + body.BoundingBox().zmax) / 2
    parts = [(body, color)]
    for sign in [-1, 1]:
        x = sign * pitch / 2
        parts += [(cylinder(radius, (sign * length / 2, 0, height), (x, 0, height)), SILVER),
                  (cylinder(radius, (x, 0, -3), (x, 0, height)), SILVER)]
    save(name, parts, refs,
         'Generic KiCad body with re-formed leads at the existing footprint pitch; '
         'not an exact manufacturer model. TVS polarity marking is not represented.',
         f'https://gitlab.com/kicad/libraries/kicad-packages3D/-/blob/master/{folder}/{library_name}')

# The catalog model is vertical. Preserve its case, but replace straight leads
# with an explicitly provisional horizontal mounting form matching the PCB.
original = cq.importers.importStep(str(OUT / 'Catalog_FGA60N65SMD_Vertical.step')).val()
case_region = cq.Solid.makeBox(60, 60, 30, cq.Vector(-30, -30, -19.9))
pieces = []
for i, solid in enumerate(original.Solids()):
    body = solid.intersect(case_region)
    if body.Volume() > 0:
        # KiCad model +Y maps to footprint -Y: extend toward the Fab body.
        body = body.rotate((0, 0, 0), (1, 0, 0), -90).translate((5.45, 23, 2.5))
        pieces.append((body, BLACK if i == 2 else SILVER))
for x in [0, 5.45, 10.9]:
    pieces += [(cq.Solid.makeBox(1, 3.4, 0.65, cq.Vector(x - 0.5, -0.3, 3.35)), SILVER),
               (cq.Solid.makeBox(1, 0.65, 6.5, cq.Vector(x - 0.5, -0.325, -2.5)), SILVER)]
save('Visual_FGA60N65SMD_Horizontal_P5.45', pieces, ['Q1', 'Q2'],
     'Case from catalog FGA60N65SMD STEP. Horizontal lead bend and mounting height are provisional; '
     'not a manufacturer-qualified bent-lead/heatsink assembly.',
     'https://easyeda.com/api/products/C444004/components?version=6.4.19.5')

# This simple envelope is generated from the manufacturer drawing, not found CAD.
parts = [(cylinder(9.5, (-23, 0, 9.75), (23, 0, 9.75)), cq.Color(0.35, 0.22, 0.14))]
for sign in [-1, 1]:
    x = sign * 29.21
    parts += [(cylinder(0.5, (sign * 23, 0, 9.75), (x, 0, 9.75)), SILVER),
              (cylinder(0.5, (x, 0, -3), (x, 0, 9.75)), SILVER)]
save('Visual_CDE_940C30S68K_F_P58.42', parts, ['CPR1'],
     'Generated visual envelope from manufacturer D19 x L46 drawing, wire D1; '
     'formed pitch 58.42 from existing PCB. Body lift and lead bends are provisional; '
     'not a downloaded manufacturer model.', 'https://www.cde.com/resources/catalogs/940C.pdf')

(ROOT / 'implementation/models3d/sources.json').write_text(json.dumps(sources, indent=2) + '\n')
print('Generated and re-imported', len(sources), 'valid STEP visuals.')
