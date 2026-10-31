"""Parametric enclosure concept. Reference PCB is the repository's complete KiCad STEP.

Run: uv run --with cadquery python case-v3/build.py
STLs are fit prototypes; electrical, thermal and winding design is unvalidated.
"""
from pathlib import Path
import json, math, struct
import cadquery as cq
from OCP.BRepBuilderAPI import BRepBuilderAPI_Sewing

ROOT = Path(__file__).resolve().parent
P = json.loads((ROOT / 'parameters.json').read_text())
OUT = ROOT / 'exports'
OUT.mkdir(exist_ok=True)
W = P['wall_mm']
M = P['inside_margin_mm']
lo, hi = -M-W, 100+M+W
inside_lo, inside_hi = -M, 100+M
lid_z = P['lid_bottom_z_mm']
bottom = P['bottom_z_mm']
parts = []

def box(x,y,z,dx,dy,dz):
    return cq.Solid.makeBox(dx,dy,dz,cq.Vector(x,y,z))

def cyl(x,y,z,r,h,direction=(0,0,1)):
    return cq.Solid.makeCylinder(r,h,cq.Vector(x,y,z),cq.Vector(*direction))

def rounded_box(x,y,z,dx,dy,dz,r):
    return cq.Workplane('XY').box(dx,dy,dz,centered=(False,False,False)).edges('|Z').fillet(r).val().translate((x,y,z))

def shell(z,h):
    return rounded_box(lo,lo,z,hi-lo,hi-lo,h,P['corner_radius_mm']).cut(
        rounded_box(inside_lo,inside_lo,z-1,inside_hi-inside_lo,inside_hi-inside_lo,h+2,P['corner_radius_mm']-W))

def add(name,shape,color,kind='printed'):
    assert shape.isValid(), name
    assert shape.Volume()>0, name
    parts.append(dict(name=name,shape=shape,color=color,kind=kind))
    if kind=='printed':
        cq.exporters.export(shape,str(OUT/f'{name}.stl'),tolerance=0.12,angularTolerance=0.15)
        cq.exporters.export(shape,str(OUT/f'{name}.step'))

# Exported KiCad board bottom is Z=0, model datum/top is Z=1.595.
pcb = cq.importers.importStep(str(ROOT/'reference/ARCSTRIKE-PCB-complete.step')).val().translate((-31.375,127.05,0))
add('pcb_reference',pcb,(0.10,0.40,0.24),'reference')

# The supplied STL is 19 axis-aligned boxes: one 5 mm base + 18 fins.
# Recover exact boxes, validate every triangle lies on their surfaces.
raw = (ROOT/'reference/heatsink_100x100.stl').read_bytes()
triangles = struct.unpack_from('<I',raw,80)[0]
assert triangles==228 and len(raw)==84+50*triangles
blocks=[]
for start in range(0,triangles,12):
    verts=[]
    for i in range(start,start+12):
        t=struct.unpack_from('<12fH',raw,84+50*i)
        verts.extend((t[3:6],t[6:9],t[9:12]))
    mn=[min(v[k] for v in verts) for k in range(3)]
    mx=[max(v[k] for v in verts) for k in range(3)]
    assert all(all(abs(v[k]-mn[k])<1e-5 or abs(v[k]-mx[k])<1e-5 for k in range(3)) for v in verts)
    blocks.append(box(*mn,*(mx[k]-mn[k] for k in range(3))))
sink = blocks[0].fuse(*blocks[1:]).clean()
assert sink.isValid() and len(sink.Solids())==1
# Real metal face of Q1/Q2 = 1.595 - 6.6 = -5.005 mm.
sink_top = 1.595-6.6-P['thermal_pad_nominal_mm']
sink = sink.rotate((50,50,0),(50,51,0),180).translate((0,0,sink_top))
add('heatsink_reference',sink,(0.65,0.69,0.74),'reference')
assert abs(sink.BoundingBox().center.x-50)<1e-6
assert abs(sink.BoundingBox().center.y-50)<1e-6
cq.exporters.export(sink,str(OUT/'heatsink_aligned.step'))

# Lower ventilated tray. Bottom rails are clear of fins except support ledges.
base = shell(bottom,-bottom)
floor = rounded_box(lo,lo,bottom,hi-lo,hi-lo,3,P['corner_radius_mm'])
for x in range(-5,106,10):
    floor = floor.cut(box(x,0,bottom-1,6,100,5))
base=base.fuse(floor)
# Fins rest on two 2 mm wide end rails; no new heatsink holes are assumed.
sink_bottom=sink_top-30
for y in (-2,98):
    rail=box(-M,y,sink_bottom-2,100+2*M,4,2)
    base=base.fuse(rail)
# Positive lateral location; 0.4 mm fit allowance on each side.
for x in (-2.4,100.4):
    base=base.fuse(box(x,35,sink_bottom-2,2,30,5))
    base=base.fuse(box(min(x,-M) if x<0 else 100.4,47,sink_bottom-2,
                       (x+2+M) if x<0 else M-0.4,6,2))
for y in (-2.4,100.4):
    base=base.fuse(box(40,y,sink_bottom,20,2,4))
# Three existing mechanical holes. J2/PE (6,6) deliberately left accessible.
mounts=[(6,94),(94,94),(94,6)]
for x,y in mounts:
    armx=inside_lo if x<50 else 90
    base=base.fuse(box(armx,y-3,-4,(6-inside_lo+6 if x<50 else inside_hi-90),6,4))
    base=base.cut(cyl(x,y,-5,1.4,6))
# Relief around copper next to the bottom-right mounting hole.
base=base.cut(box(95.2,8.2,-0.25,3.2,1.2,0.3))
# Short M3 lid/sleeve fasteners, separate from PCB fasteners.
corners=[(lo+6,lo+6),(lo+6,hi-6),(hi-6,lo+6),(hi-6,hi-6)]
for x,y in corners:
    base=base.fuse(cyl(x,y,-8,5,8))
    base=base.cut(cyl(x,y,-7,1.4,8))
    base=base.cut(cyl(x,y,bottom-1,1.4,5))
# Port access spans the seam; no cut through PCB.
fiber_cut=box(lo-1,P['fiber_window_y_mm']-8,P['fiber_window_bottom_z_mm'],W+2,16,14)
base=base.cut(fiber_cut).clean()
add('01_lower_tray',base,(0.12,0.15,0.19))
feet=[]
for x,y in corners:
    feet.append(cyl(x,y,bottom-4,5,4).cut(cyl(x,y,bottom-5,1.7,6)))
add('06_separate_feet',cq.Compound.makeCompound(feet),(0.16,0.22,0.30))

upper=shell(0,lid_z)
for x,y in corners:
    upper=upper.fuse(cyl(x,y,0,5,4),cyl(x,y,lid_z-8,5,8))
    upper=upper.cut(cyl(x,y,-1,1.7,6),cyl(x,y,lid_z-7,1.4,8))
upper=upper.cut(fiber_cut)
# Connector lives in a replaceable plate, dimensioned from supplied STL.
upper=upper.cut(box(24,inside_hi-1,6,44,W+2,30))
for x in (21,71):
    for z in (7,35):upper=upper.cut(cyl(x,inside_hi-1,z,1.7,W+3,(0,1,0)))
# Three long capsule vents give a quieter outline and larger open area.
for side,start,length in [(lo-1,45,58),(inside_hi-1,5,98)]:
    for z in (24,31,38):
        vent=box(side,start+1.5,z-1.5,W+2,length-3,3)
        vent=vent.fuse(cyl(side,start+1.5,z,1.5,W+2,(1,0,0)),
                       cyl(side,start+length-1.5,z,1.5,W+2,(1,0,0)))
        upper=upper.cut(vent)
add('02_upper_sleeve',upper.clean(),(0.19,0.23,0.28))
blank=box(18,hi,3,56,3,36)
for x in (21,71):
    for z in (7,35):blank=blank.cut(cyl(x,hi-1,z,1.7,5,(0,1,0)))
# Rear housing 26 x 18 mm, 0.3 mm clearance per side. Flange holes 42 mm apart.
blank=blank.cut(box(46-13.3,hi-1,21-9.3,26.6,5,18.6))
for x in (25,67):blank=blank.cut(cyl(x,hi-1,21,1.7,5,(0,1,0)))
add('03_C14_inlet_plate',blank,(0.16,0.22,0.30))

def stl_solid(path):
    data=path.read_bytes()
    sewing=BRepBuilderAPI_Sewing(1e-5)
    for i in range(struct.unpack_from('<I',data,80)[0]):
        t=struct.unpack_from('<12fH',data,84+50*i)
        points=[cq.Vector(*t[j:j+3]) for j in (3,6,9)]
        wire=cq.Wire.makePolygon(points,close=True)
        sewing.Add(cq.Face.makeFromWires(wire).wrapped)
    sewing.Perform()
    shape=cq.Shape.cast(sewing.SewedShape())
    solids=[cq.Solid.makeSolid(s).fix().clean().fix() for s in shape.Shells()]
    # The supplied housing shell is closed but self-inconsistent in BRep.
    # Keep its six valid contact solids and use a dimensioned housing envelope
    # in STEP. The browser viewer uses the exact original STL for the C14.
    if not all(s.isValid() for s in solids):
        assert len(solids)==7 and all(s.isValid() for s in solids[1:])
        flange=box(-25,-11,-3,50,22,3)
        for x in (-21,21):flange=flange.cut(cyl(x,0,-4,1.6,5))
        housing=flange.fuse(box(-13,-9,-17,26,18,14),box(-15.5,-11,0,31,22,2))
        housing=housing.cut(box(-11.5,-7,-14,23,14,17))
        housing=housing.fuse(box(-9.25,-7.5,-18.6,18.5,15.1,4))
        assert housing.isValid()
        solids=[housing,*solids[1:]]
    assert solids and all(s.isValid() for s in solids)
    return cq.Compound.makeCompound(solids)

c14=stl_solid(ROOT/'reference/C14-Socket-v8.stl')
c14=c14.rotate((0,0,0),(1,0,0),-90).translate((46,hi+6,21))
add('C14_reference',c14,(0.13,0.14,0.16),'reference')

lid=rounded_box(lo,lo,lid_z,hi-lo,hi-lo,P['lid_thickness_mm'],P['corner_radius_mm'])
for x,y in corners:
    lid=lid.cut(cyl(x,y,lid_z-1,1.7,6))
# Replaceable coil support interface, 4 M4 holes on 80 mm square.
for x in (10,90):
    for y in (10,90):lid=lid.cut(cyl(x,y,lid_z-1,2.2,6))
# Isolated primary wire passages; cable sleeves still to select.
for x in (34,66):lid=lid.cut(cyl(x,20,lid_z-1,3,6))
add('04_structural_lid',lid,(0.12,0.15,0.19))

# Removable deck with spiral combs; electrical dimensions from docs/design/COILS.md.
support_z=lid_z+P['lid_thickness_mm']
sec_r=(P['secondary_tube_od_mm']+0.6)/2
plate=cq.Workplane('XY').circle(P['resonator_deck_diameter_mm']/2).extrude(4).edges().fillet(0.6).val().translate((50,50,support_z))
for x in (10,90):
    for y in (10,90):plate=plate.cut(cyl(x,y,support_z-1,2.2,6))
# Tube seats on the lid; a center passage routes the secondary base lead.
plate=plate.cut(cyl(50,50,support_z-1,sec_r,6))
collar=cyl(50,50,support_z+4,sec_r+4,18).cut(cyl(50,50,support_z+3,sec_r,20))
# Split collar accepts a clamp; clamp hardware remains to select.
collar=collar.cut(box(49,50,support_z+3,2,40,20))
plate=plate.fuse(collar)
primary_z=support_z+12
first_r=(P['primary_inner_diameter_mm']+P['primary_wire_diameter_mm'])/2
# The Archimedean spiral reaches centerline R=86.5 after eight turns.
# Four combs follow the spiral's quarter-turn radial offsets.
for quadrant in range(4):
    comb=box(90,46,support_z+4,47,8,8)
    for turn in range(P['primary_turns']+(1 if quadrant==0 else 0)):
        radius=first_r+(turn+quadrant/4)*P['primary_pitch_mm']
        comb=comb.cut(cyl(50+radius,41,primary_z,P['primary_holder_groove_diameter_mm']/2,18,(0,1,0)))
    comb=comb.rotate((50,50,0),(50,50,1),quadrant*90)
    plate=plate.fuse(comb)
for x in (34,66):plate=plate.cut(cyl(x,20,support_z-1,3,8))
add('05_resonator_deck',plate.clean(),(0.15,0.18,0.22))
# Tube rests on lid; axial adjustment shims are not yet designed.
tube_z=support_z
h=P['secondary_tube_height_mm']
tube=cyl(50,50,tube_z,30,h).cut(cyl(50,50,tube_z-1,28.5,h+2))
add('secondary_tube_60x280',tube,(0.75,0.69,0.58),'reference')
winding=cyl(50,50,tube_z+30,30.14224,P['secondary_winding_height_mm']).cut(cyl(50,50,tube_z+29,30,P['secondary_winding_height_mm']+2))
add('secondary_1500_turns_envelope',winding,(0.72,0.29,0.09),'reference')
# Sweep the full eight-turn spiral; reference only, never an STL to print.
points=[]
for i in range(161):
    turns=8*i/160
    radius=first_r+P['primary_pitch_mm']*turns
    angle=turns*2*math.pi
    points.append(cq.Vector(50+radius*math.cos(angle),50+radius*math.sin(angle),primary_z))
path=cq.Wire.assembleEdges([cq.Edge.makeSpline(points)])
tangent=points[1]-points[0]
profile=cq.Workplane(cq.Plane(origin=points[0],normal=tangent)).circle(P['primary_wire_diameter_mm']/2)
primary=profile.sweep(cq.Workplane(obj=path),isFrenet=True).val()
add('primary_8_turns_reference',primary,(0.88,0.42,0.13),'reference')
# Toroid bottom at tube top, diameter 150 mm and section 40 mm.
toroid_z=tube_z+h+20
toroid=cq.Solid.makeTorus(55,20,cq.Vector(50,50,toroid_z),cq.Vector(0,0,1))
toroid=toroid.fuse(cyl(50,50,toroid_z-1,55,2)).clean()
add('toroid_150x40',toroid,(0.76,0.79,0.82),'reference')
cap=cyl(50,50,tube_z+h,32,3).fuse(cyl(50,50,tube_z+h-5,28.2,5),cyl(50,50,tube_z+h+3,5,16))
add('07_top_cap_concept',cap,(0.12,0.15,0.19))

assembly=cq.Assembly(name='ARCSTRIKE_case_v3_CONCEPT')
for part in parts:
    assembly.add(part['shape'],name=part['name'],color=cq.Color(*part['color']))
assembly.export(str(OUT/'ARCSTRIKE-case-v3-CONCEPT.step'),exportType='STEP')

# Check actual solids, not only bounding boxes, for mechanical intersections.
checks=[]
printed=[p for p in parts if p['kind']=='printed']
for part in printed:
    for name,ref in [('PCB',pcb),('heatsink',sink),('C14',c14),('secondary',tube),('primary',primary),('toroid',toroid)]:
        volume=part['shape'].intersect(ref).Volume()
        if volume>=0.02:
            overlap=part['shape'].intersect(ref)
            for s in overlap.Solids():
                bb=s.BoundingBox()
                print('COLLISION',part['name'],name,s.Volume(),(bb.xmin,bb.xmax,bb.ymin,bb.ymax,bb.zmin,bb.zmax),flush=True)
        checks.append(dict(part=part['name'],reference=name,overlap_mm3=volume))
        assert volume<0.02,(part['name'],name,volume)
for a in printed:
    for b in printed:
        if a['name']>=b['name']:continue
        volume=a['shape'].intersect(b['shape']).Volume()
        checks.append(dict(part=a['name'],reference=b['name'],overlap_mm3=volume))
        assert volume<0.02,(a['name'],b['name'],volume)
checks.append(dict(part='PCB',reference='heatsink',overlap_mm3=pcb.intersect(sink).Volume()))
assert checks[-1]['overlap_mm3']<0.02
checks.append(dict(part='PCB',reference='C14',overlap_mm3=pcb.intersect(c14).Volume()))
assert checks[-1]['overlap_mm3']<0.02
report=dict(status='CONCEPT, not released for final printing or energizing',
 dimensions_mm=dict(case=[hi-lo,hi-lo,lid_z+P['lid_thickness_mm']-bottom+4],assembly_height=toroid_z+20-bottom+4, secondary=[60,280],toroid=[150,40],primary_outer_diameter=176,resonator_deck_diameter=180,body_corner_radius=8,pcb_to_lid_vertical_gap=lid_z-pcb.BoundingBox().zmax,
                    pcb=[100,100],heatsink=[100,100,30]),
 coordinate_system='PCB XY 0..100; PCB bottom Z=0; component datum Z=1.595',
 sink_top_z_mm=sink_top,heatsink_center_xy_mm=[50,50],
 mounting_holes_xy_mm=mounts,PE_hole_left_free_xy_mm=[6,6],
 comparison_v2=dict(body_footprint_reduction_percent=100*(1-(hi-lo)**2/196**2),body_envelope_reduction_percent=100*(1-(hi-lo)**2*(lid_z+P['lid_thickness_mm']-bottom+4)/(196**2*97)),overall_width_reduction_percent=100*(1-180/196)),
 checks=checks,pending=['tube OD and enamel pitch measurements',
 'thermal isolators and insulated fasteners','sink retention/clamping hardware',
 'optical connector/cable fit','thermal and electrical validation','print tolerances/material'])
(OUT/'verification.json').write_text(json.dumps(report,indent=2))

# Standalone interactive browser viewer: no internet or external dependencies.
meshes=[]
for part in parts:
    pos=[]
    if part['name']=='C14_reference':
        raw=(ROOT/'reference/C14-Socket-v8.stl').read_bytes()
        for i in range(struct.unpack_from('<I',raw,80)[0]):
            t=struct.unpack_from('<12fH',raw,84+50*i)
            for j in (3,6,9):
                x,y,z=t[j:j+3]
                pos.extend(round(t,3) for t in (x+46,z+hi+6,-y+21))
    else:
        vertices,faces=part['shape'].tessellate(0.30,0.25)
        for face in faces:
            for idx in face:
                v=vertices[idx];pos.extend(round(t,3) for t in (v.x,v.y,v.z))
    meshes.append(dict(name=part['name'],positions=pos,color=part['color'],kind=part['kind']))
(OUT/'viewer_meshes.json').write_text(json.dumps(meshes,separators=(',',':')))
import runpy
runpy.run_path(str(ROOT/'build_viewer.py'))
print(json.dumps(report,indent=2))
