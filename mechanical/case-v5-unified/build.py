"""One-piece replacement for v5 lid + deck; all previously printed parts retained."""
from pathlib import Path
import json,math,hashlib
import cadquery as cq
HERE=Path(__file__).resolve().parent
V5=HERE.parent/'case-v5'
OUT=HERE/'exports';OUT.mkdir(exist_ok=True)
# Reconstruct the exact v5 assembly, suppressing all original print/part exports.
source=(V5/'build.py').read_text().split('# Actual models and counts')[0]
source=source.replace("ROOT=Path(__file__).resolve().parent",'ROOT=Path('+repr(str(V5))+')')
source=source.replace("OUT=ROOT/'exports'; OUT.mkdir(exist_ok=True)",'OUT=Path('+repr(str(OUT))+'); OUT.mkdir(exist_ok=True)')
source=source.replace("    if kind=='printed':\n        cq.exporters.export", "    if False:\n        cq.exporters.export")
ctx={'__file__':str(V5/'build.py'),'__name__':'v5_geometry_reference'}
exec(compile(source,str(V5/'build.py'),'exec'),ctx)
box,cyl,hx,rounded_box,joint_groove=(ctx[n] for n in ['box','cyl','hexz','rounded_box','joint_groove'])
old_parts=ctx['parts'];old_hardware=ctx['hardware'];corners=ctx['corners']
old_lid=next(p['shape'] for p in old_parts if p['name']=='04_structural_lid')
old_deck=next(p['shape'] for p in old_parts if p['name']=='05_modular_deck_NO_WIRE_HOLDER')
# Preserve external dimensions, sleeve joint and all non-retired interfaces.
merged=rounded_box(-20,-20,46,140,140,6,8).cut(joint_groove(46))
deck=cq.Workplane('XY').circle(90).extrude(4).edges().fillet(.6).val().translate((50,50,52))
merged=merged.fuse(deck)
merged=merged.cut(cyl(50,50,52,30.3,5))
for x,y in corners:
    merged=merged.cut(cyl(x,y,45,1.7,12),cyl(x,y,48.6,3.2,3.4),cyl(x,y,52,3.5,5))
# Shallow underside hex pockets are easy to load; use M3x16 in the same printed clamp.
mounts=ctx['lower_mounts']
for x,y in mounts:
    merged=merged.cut(cyl(x,y,45,1.7,12),hx(x,y,45.99,5.8,2.61))
for x,y in [(125,50),(50,125),(-25,50),(50,-25)]:
    merged=merged.cut(cyl(x,y,51,1.7,6),hx(x,y,51.99,5.8,2.61))
for x in (34,66):merged=merged.cut(cyl(x,20,45,3,12))
merged=merged.clean()
assert merged.isValid() and len(merged.Solids())==1
cq.exporters.export(merged,str(OUT/'04_tampa_e_plataforma_unificadas.step'))
printed=merged.rotate((0,0,0),(1,0,0),180)
bb=printed.BoundingBox();printed=printed.translate((-bb.xmin,-bb.ymin,-bb.zmin))
cq.exporters.export(printed,str(OUT/'04_tampa_e_plataforma_unificadas__1x.stl'),tolerance=.08,angularTolerance=.12)
# All other parts and fasteners remain in their v5 positions; only the four
# joining M4x10 bolts and their four M4 nuts are retired.
retired={'04_structural_lid','05_modular_deck_NO_WIRE_HOLDER'}
kept_parts=[p for p in old_parts if p['name'] not in retired]
kept_hw=[h for h in old_hardware if not h['name'].startswith(('Deck_','Lower_collar_flange_'))]
new_hw=[]
for i,(x,y) in enumerate(mounts):
    new_hw.append(dict(name=f'Lower_collar_flange_{i+1}_bolt',shape=ctx['bolt'](3,16,(x,y,60)),item='M3x16 DIN912'))
    new_hw.append(dict(name=f'Lower_collar_flange_{i+1}_nut',shape=ctx['nut'](3,(x,y,46.1)),item='M3 DIN934'))
kept_hw+=new_hw
checks=[]
def overlap(a,b):
    x,y=a.BoundingBox(),b.BoundingBox()
    if any(min(getattr(x,k+'max'),getattr(y,k+'max'))-max(getattr(x,k+'min'),getattr(y,k+'min'))<1e-5 for k in 'xyz'):return 0
    return max(0,a.intersect(b).Volume())
for p in kept_parts+kept_hw:
    vol=overlap(merged,p['shape']);checks.append(dict(reference=p['name'],overlap_mm3=vol));assert vol<.02,(p['name'],vol)
for h in new_hw:
    for p in kept_parts+kept_hw:
        if p is h:continue
        vol=overlap(h['shape'],p['shape']);checks.append(dict(part=h['name'],reference=p['name'],overlap_mm3=vol));assert vol<.02,(h['name'],p['name'],vol)
# Differences must be confined to the retired M4 holes and M3 nut loading wells.
allowed=[]
for x,y in ctx['flange_mounts']+mounts:allowed.append(box(x-5,y-5,45,10,10,13))
zone=cq.Compound.makeCompound(allowed)
old=old_lid.fuse(old_deck).clean()
added=merged.cut(old);removed=old.cut(merged)
assert added.cut(zone).Volume()<.02,'Unexpected added material outside approved changes'
assert removed.cut(zone).Volume()<.02,'An existing mating interface changed'
# Record source meshes to make compatibility traceable to the already printed set.
source_hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (HERE.parents[1]/'production/case/v5-unified/print').glob('*.stl') if not p.name.startswith(('04_','05_'))}
report=dict(status='PASS: replacement compatible with unchanged v5 parts in CAD',dimensions_mm=[180,180,10],bottom_z_mm=46,top_z_mm=56,tube_seat_z_mm=52,print_rotation_x_deg=180,printed_parts_replaced=['04_tampa__1x.stl','05_plataforma__1x.stl'],other_printed_parts_modified=[],retired_hardware={'M4x10 DIN912':4,'M4 DIN934':4},clamp_hardware_change='Replace 4 x M3x8 with 4 x M3x16; reuse the same 4 x M3 DIN934 nuts',nut_loading_well_depth_mm=2.6,checks=checks,added_volume_mm3=added.Volume(),removed_volume_mm3=removed.Volume(),allowed_change_regions='only former lid/deck M4 joint and relocation of M3 clamp nuts to the underside',unchanged_print_file_sha256=source_hashes)
(OUT/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
assembly=cq.Assembly(name='ARCSTRIKE_v5_UNIFIED_LID_REPLACEMENT')
for p in kept_parts:assembly.add(p['shape'],name=p['name'],color=cq.Color(*p['color']))
assembly.add(merged,name='04_unified_lid_and_deck',color=cq.Color(.12,.15,.19))
assembly.add(cq.Compound.makeCompound([h['shape'] for h in kept_hw]),name='hardware_fasteners',color=cq.Color(.64,.66,.69))
assembly.export(str(OUT/'ARCSTRIKE-v5-tampa-unificada.step'),exportType='STEP')
print('PASS:',len(checks),'interference checks; retained mating geometry unchanged; one printable solid.',flush=True)
