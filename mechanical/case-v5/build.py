"""Assembly prototype with captive standard nuts and separate, oriented print files.
Run from repository root: uv run --with cadquery python mechanical/case-v5/build.py
"""
from pathlib import Path
import json, math, struct, csv, runpy
from collections import Counter
import cadquery as cq
from OCP.BRepBuilderAPI import BRepBuilderAPI_Sewing
ROOT=Path(__file__).resolve().parent
P=json.loads((ROOT/'parameters.json').read_text())
OUT=ROOT/'exports'; OUT.mkdir(exist_ok=True)
PRINT=OUT/'print'; PRINT.mkdir(exist_ok=True)
W=P['wall_mm']; M=P['inside_margin_mm']
lo,hi=-M-W,100+M+W
inside_lo,inside_hi=-M,100+M
body=hi-lo
bottom=P['bottom_z_mm']; lid_z=P['lid_bottom_z_mm']; lid_t=P['lid_thickness_mm']
parts=[]; hardware=[]; joints=[]
colors={'body':(.12,.15,.19),'sleeve':(.19,.23,.28),'accent':(.75,.41,.12)}
def box(x,y,z,dx,dy,dz):return cq.Solid.makeBox(dx,dy,dz,cq.Vector(x,y,z))
def cyl(x,y,z,r,h,direction=(0,0,1)):return cq.Solid.makeCylinder(r,h,cq.Vector(x,y,z),cq.Vector(*direction))
def rounded_box(x,y,z,dx,dy,dz,r):
    return cq.Workplane('XY').box(dx,dy,dz,centered=(False,False,False)).edges('|Z').fillet(r).val().translate((x,y,z))
def prism_x(x,y,z,wy,hz,length,r):
    return rounded_box(0,0,0,hz,wy,length,r).rotate((0,0,0),(0,1,0),90).translate((x,y,z+hz))
def shell(z,h):return rounded_box(lo,lo,z,hi-lo,hi-lo,h,8).cut(rounded_box(inside_lo,inside_lo,z-1,inside_hi-inside_lo,inside_hi-inside_lo,h+2,5))
def hexz(x,y,z,af,h):
    r=af/math.sqrt(3)
    pts=[cq.Vector(x+r*math.cos(i*math.pi/3),y+r*math.sin(i*math.pi/3),z) for i in range(6)]
    return cq.Solid.extrudeLinear(cq.Wire.makePolygon(pts,close=True),[],cq.Vector(0,0,h))
def hexx(x,y,z,af,h):return hexz(0,0,0,af,h).rotate((0,0,0),(0,1,0),90).translate((x,y,z))
def hexy(x,y,z,af,h):return hexz(0,0,0,af,h).rotate((0,0,0),(1,0,0),-90).translate((x,y,z))
def side_nut_slot(shape,x,y,z,af=5.8,h=2.6,inward=True):
    shape=shape.cut(hexz(x,y,z,af,h))
    direction=1 if x<50 else -1
    if not inward:direction=-direction
    return shape.cut(box(x if direction>0 else x-10,y-af/2,z,10,af,h))
def joint_lip(z):
    return rounded_box(inside_lo-.2,inside_lo-.2,z,body-2*W+.4,body-2*W+.4,1.6,5.2).cut(rounded_box(inside_lo+1.6,inside_lo+1.6,z-1,body-2*W-3.2,body-2*W-3.2,3.6,3.4))
def joint_groove(z):
    return rounded_box(inside_lo-.45,inside_lo-.45,z-.01,body-2*W+.9,body-2*W+.9,1.92,5.45).cut(rounded_box(inside_lo+1.85,inside_lo+1.85,z-1,body-2*W-3.7,body-2*W-3.7,4,3.15))
def add(name,shape,color,kind='printed',rx=0):
    shape=shape.clean()
    assert shape.isValid() and shape.Volume()>0,name
    if kind=='printed':assert len(shape.Solids())==1,(name,'disconnected printed bodies',len(shape.Solids()))
    part=dict(name=name,shape=shape,color=color,kind=kind,print_rx=rx);parts.append(part)
    if kind=='printed':
        cq.exporters.export(shape,str(OUT/f'{name}.step'))
        oriented=shape.rotate((0,0,0),(1,0,0),rx) if rx else shape
        b=oriented.BoundingBox();oriented=oriented.translate((-b.xmin,-b.ymin,-b.zmin))
        cq.exporters.export(oriented,str(PRINT/f'{name}.stl'),tolerance=.08,angularTolerance=.12)
    return part
# Standard hardware envelopes, unthreaded shafts; head includes Allen recess.
def bolt(d,length,seat,axis=(0,0,-1)):
    head_d,head_h,key={3:(5.5,3,2.5),4:(7,4,3)}[d]
    s=cyl(0,0,-length,d/2,length).fuse(cyl(0,0,0,head_d/2,head_h))
    s=s.cut(hexz(0,0,head_h-1.6,key,2))
    if axis==(1,0,0):s=s.rotate((0,0,0),(0,1,0),-90)
    elif axis==(0,-1,0):s=s.rotate((0,0,0),(1,0,0),-90)
    elif axis==(0,0,1):s=s.rotate((0,0,0),(1,0,0),180)
    elif axis!=(0,0,-1):raise ValueError(axis)
    return s.translate(seat)
def nut(d,origin,axis='z'):
    af,h={3:(5.5,2.4),4:(7,3.2)}[d]
    s=hexz(0,0,0,af,h).cut(cyl(0,0,-1,(d+.02)/2,h+2))
    if axis=='x':s=s.rotate((0,0,0),(0,1,0),90)
    if axis=='y':s=s.rotate((0,0,0),(1,0,0),-90)
    return s.translate(origin)
def hw(label,shape,item):
    assert shape.isValid(),label
    hardware.append(dict(name=label,shape=shape,item=item))
def screw_joint(label,d,length,seat,nut_origin,axis=(0,0,-1),nut_axis='z'):
    hw(label+'_bolt',bolt(d,length,seat,axis),f'M{d}x{length} DIN912')
    hw(label+'_nut',nut(d,nut_origin,nut_axis),f'M{d} DIN934')
    joints.append(dict(name=label,screw=f'M{d}x{length}',seat=seat,nut_origin=nut_origin,axis=axis))
exec(compile((ROOT/'reference_geometry.py').read_text(),str(ROOT/'reference_geometry.py'),'exec'))
corners=[(lo+6,lo+6),(lo+6,hi-6),(hi-6,lo+6),(hi-6,hi-6)]
mounts=[(6,94),(94,94),(94,6)]
# Wide rounded finger well, plus a rear shield around the receiver housing.
fy=28.35
fiber_cut=prism_x(lo-1,fy-16,.2,32,28.8,7,3)
fiber_outer=prism_x(lo,fy-18,-1.8,36,32.8,-6.8-lo,4)
fiber_inner=prism_x(lo-1,fy-16,.2,32,28.8,-5.8-(lo-1),3)
fiber_duct=fiber_outer.cut(fiber_inner)
mask=prism_x(-6.8,fy-18,-1.8,36,32.8,2,4).cut(box(-7.8,fy-9,.2,4,18,17))
fiber_duct=fiber_duct.fuse(mask)
fiber_lower=fiber_duct.intersect(box(lo-1,0,bottom,30,60,-bottom))
fiber_upper=fiber_duct.intersect(box(lo-1,0,0,30,60,lid_z))
sink_bottom=sink_top-P["heatsink_nominal_height_mm"]
# Tray, fin end rails, three PCB shelves, and accessible nut pockets.
base=shell(bottom,-bottom).fuse(rounded_box(lo,lo,bottom,body,body,3,8))
for x in range(-5,106,10):base=base.cut(box(x,0,bottom-1,6,100,5))
# The cradle supports from below on crossed flat bars, independent of fin spacing.
cradle_baseline=sink_top-P['heatsink_height_max_mm']-6
P['heatsink_shim_stack_mm']=P['heatsink_height_max_mm']-P['heatsink_nominal_height_mm']
assert 0<=P['heatsink_shim_stack_mm']<=10
remaining=P['heatsink_shim_stack_mm'];shim_stack=[]
for t in (8,4,2,1,.5):
    while remaining>=t-1e-8:shim_stack.append(t);remaining-=t
assert abs(remaining)<1e-7,'Use height increments of 0.5 mm or measure a custom shim'
cradle_z=cradle_baseline+P['heatsink_shim_stack_mm']
cradle_bolt_length=2*math.ceil((8+P['heatsink_shim_stack_mm'])/2)
cradle=box(-5,43,cradle_z,110,14,6).fuse(box(43,-5,cradle_z,14,110,6))
cradle_mounts=[(0,50),(100,50),(50,0),(50,100)]
for i,(x,y) in enumerate(cradle_mounts):
    base=base.fuse(cyl(x,y,bottom+3,6,cradle_baseline-(bottom+3)))
    # Join tangent front/rear cylinders with a finite web for manifold STL export.
    if x==50:
        web_y=-6.5 if y==0 else 105.5
        base=base.fuse(box(49,web_y,bottom+3,2,1,cradle_baseline-(bottom+3)))
    base=base.cut(cyl(x,y,bottom-1,1.7,20))
    base=side_nut_slot(base,x,y,bottom+3.0)
    cradle=cradle.cut(cyl(x,y,cradle_z-1,1.7,8),cyl(x,y,cradle_z+2.6,3.2,4))
    z=cradle_baseline
    for t in shim_stack:
        shim=cyl(x,y,z,6,t).cut(cyl(x,y,z-.1,1.7,t+.2))
        add(f'12_shim_{t}mm_{i+1}',shim,colors['accent']);z+=t
    screw_joint(f'Cradle_{i+1}',3,cradle_bolt_length,(x,y,cradle_z+2.6),(x,y,bottom+3.1))
add('13_universal_heatsink_cradle',cradle,colors['body'])
for x,y in mounts:
    ax=inside_lo if x<50 else 90
    width=6 if (x,y)==(94,6) else 10
    base=base.fuse(box(ax,y-width/2,-4.8,6-inside_lo+6 if x<50 else inside_hi-90,width,4.8),cyl(x,y,-4.8,4.5,4.8))
    if (x,y)==(6,94):
        # The reference HLK body covers this hole from Z=2.095: locate from below.
        base=base.fuse(cyl(x,y,0,1.4,1.2))
        continue
    base=base.cut(cyl(x,y,-5,1.7,6))
    base=side_nut_slot(base,x,y,-3.9)
    # Nylon washer is modeled as an actual printed part, 0.6 mm thick.
    washer=cyl(x,y,1.595,3,.6).cut(cyl(x,y,1.5,1.7,.8))
    add(f'09_pcb_washer_{len([p for p in parts if p["name"].startswith("09_")])+1}',washer,(.85,.85,.78))
    screw_joint(f'PCB_{x}_{y}',3,6,(x,y,2.195),(x,y,-3.8))
base=base.cut(box(95.2,8.2,-.25,3.2,1.2,.3),box(94.5,9,-.2,3,2.5,.3))
for i,(x,y) in enumerate(corners):
    base=base.fuse(cyl(x,y,-8,5,8),cyl(x,y,bottom+3,5,5))
    base=base.cut(cyl(x,y,-8.1,1.7,8.2),cyl(x,y,bottom-1,1.7,10))
    base=side_nut_slot(base,x,y,-5.2)
    base=side_nut_slot(base,x,y,bottom+4.2)
    foot=cyl(x,y,bottom-4,5,4).cut(cyl(x,y,bottom-5,1.7,6),cyl(x,y,bottom-4.1,3.2,3.3))
    add(f'06_foot_{i+1}',foot,(.13,.16,.19))
    screw_joint(f'Foot_{i+1}',3,8,(x,y,bottom-.8),(x,y,bottom+4.3),axis=(0,0,1))
# Four slotted fingers locate and retain the flat upper outside edges.
# They do not match, enter, or drill the fins. Nominal shifts fit 104 x 100 mm.
for i,(angle,shift) in enumerate([(0,0),(180,0),(90,2),(270,2)]):
    def place(shape,offset=0):
        placed=shape.translate((offset,0,0)).rotate((50,50,0),(50,50,1),angle)
        return placed.translate((0,20,0)) if angle in (0,180) else placed
    rad=math.radians(angle)
    x=50-60.5*math.cos(rad);y=50-60.5*math.sin(rad)+(20 if angle in (0,180) else 0)
    post=cyl(-10.5,50,bottom+3,4.5,sink_top-(bottom+3)).fuse(box(inside_lo,47,bottom+3,-10.5-inside_lo,6,sink_top-(bottom+3)))
    post=post.cut(box(-7.85,43.5,sink_top-2.3,3,13,2.5))
    base=base.fuse(place(post))
    base=base.cut(cyl(x,y,sink_top-9,1.7,11))
    base=side_nut_slot(base,x,y,sink_top-5.8)
    finger=box(-19,44,sink_top,19,12,3).fuse(box(-3.6,44,sink_top-2,1.2,12,2))
    slot=box(-14.5,48.3,sink_top-1,8,3.4,5).fuse(cyl(-14.5,50,sink_top-1,1.7,5),cyl(-6.5,50,sink_top-1,1.7,5))
    finger=place(finger.cut(slot),shift)
    add(f'08_adjustable_heatsink_finger_{i+1}',finger,colors['accent'],rx=180)
    screw_joint(f'Heatsink_{i+1}',3,10,(x,y,sink_top+3),(x,y,sink_top-5.7))
# Slots let the adjustable fingers travel without hitting the case wall.
for axis in (0,1):
    for sign in (-1,1):
        x=(lo-1 if sign<0 else inside_hi-2) if axis==0 else 44
        y=64 if axis==0 else (lo-1 if sign<0 else inside_hi-2)
        base=base.cut(box(x,y,sink_top-.25,6 if axis==0 else 12,12 if axis==0 else 6,3.5))
base=base.fuse(joint_lip(0)).cut(fiber_cut)
for x,y in corners:base=base.cut(cyl(x,y,-8.1,1.7,10))
base=base.cut(box(lo-1,fy-18.3,0,7,36.6,1.9)).fuse(fiber_lower)
add('01_lower_tray',base,colors['body'])
# Sleeve: matching seam groove, top tongue, lower clamping screws, upper nuts.
upper=shell(0,lid_z)
for i,(x,y) in enumerate(corners):
    upper=upper.fuse(cyl(x,y,0,5,4),cyl(x,y,lid_z-8,5,8))
upper=upper.cut(joint_groove(0)).fuse(joint_lip(lid_z)).cut(fiber_cut)
for i,(x,y) in enumerate(corners):
    upper=upper.cut(cyl(x,y,-1,1.7,6),cyl(x,y,4,3.2,4),cyl(x,y,lid_z-9,1.7,13))
    upper=side_nut_slot(upper,x,y,40)
    screw_joint(f'Sleeve_{i+1}',3,10,(x,y,4),(x,y,-5.1))
# Rear connector aperture and localized reliefs for the inlet's nut bosses.
upper=upper.cut(box(24,inside_hi-1,6,44,5,30),box(20,inside_hi-2,16,52,7,10))
for x in (21,71):
    for z in (7,35):
        upper=upper.fuse(box(x-4,inside_hi-4,z-4,8,7,8))
        upper=upper.cut(hexy(x,inside_hi-4.1,z,5.8,2.8),cyl(x,inside_hi-5,z,1.7,12,(0,1,0)))
        screw_joint(f'Adapter_{x}_{z}',3,10,(x,hi+3,z),(x,inside_hi-3.9,z),axis=(0,-1,0),nut_axis='y')
for side,start,length in [(lo-1,50,53),(inside_hi-1,5,98)]:
    for z in (24,31,38):
        cut=box(side,start+1.5,z-1.5,5,length-3,3).fuse(cyl(side,start+1.5,z,1.5,5,(1,0,0)),cyl(side,start+length-1.5,z,1.5,5,(1,0,0)))
        upper=upper.cut(cut)
upper=upper.fuse(fiber_upper)
add('02_upper_sleeve',upper,colors['sleeve'])
blank=box(18,hi,3,56,3,36)
for x in (21,71):
    for z in (7,35):blank=blank.cut(cyl(x,hi-1,z,1.7,5,(0,1,0)))
blank=blank.cut(box(32.7,hi-1,11.7,26.6,5,18.6))
for x in (25,67):
    blank=blank.fuse(box(x-4,hi-4,17,8,4,8))
    blank=blank.cut(hexy(x,hi-4.1,21,5.8,2.8),cyl(x,hi-5,21,1.7,10,(0,1,0)))
    screw_joint(f'C14_{x}',3,10,(x,hi+6,21),(x,hi-3.9,21),axis=(0,-1,0),nut_axis='y')
add('03_C14_inlet_plate',blank,colors['body'],rx=-90)
# Lid has 6 mm thickness so socket heads can be recessed with 2.6 mm material below.
lid=rounded_box(lo,lo,lid_z,body,body,lid_t,8).cut(joint_groove(lid_z))
for i,(x,y) in enumerate(corners):
    lid=lid.cut(cyl(x,y,45,1.7,8),cyl(x,y,48.6,3.2,4))
    screw_joint(f'Lid_{i+1}',3,10,(x,y,48.6),(x,y,40.1))
deck_z=lid_z+lid_t
flange_mounts=[(10,10),(10,90),(90,10),(90,90)]
lower_mounts=[(50+sx*40/math.sqrt(2),50+sy*40/math.sqrt(2)) for sx in (-1,1) for sy in (-1,1)]
for x,y in flange_mounts:lid=lid.cut(cyl(x,y,45,2.25,8),hexz(x,y,45.99,7.4,3.51))
for x,y in lower_mounts:lid=lid.cut(cyl(x,y,51,2,2))
for x in (34,66):lid=lid.cut(cyl(x,20,45,3,8))
add('04_structural_lid',lid,colors['body'],rx=180)
deck=cq.Workplane('XY').circle(90).extrude(4).edges().fillet(.6).val().translate((50,50,deck_z))
deck=deck.cut(cyl(50,50,deck_z-1,30.3,6))
for x,y in corners:deck=deck.cut(cyl(x,y,deck_z-1,3.5,6))
for i,(x,y) in enumerate(flange_mounts):
    deck=deck.cut(cyl(x,y,deck_z-1,2.25,6))
    screw_joint(f'Deck_{i+1}',4,10,(x,y,deck_z+4),(x,y,46.15))
for i,(x,y) in enumerate(lower_mounts):
    deck=deck.cut(cyl(x,y,deck_z-1,1.7,6),hexz(x,y,deck_z-.01,5.8,2.61))
    screw_joint(f'Lower_collar_flange_{i+1}',3,8,(x,y,deck_z+8),(x,y,deck_z+.1))
for x,y in [(125,50),(50,125),(-25,50),(50,-25)]:
    deck=deck.cut(cyl(x,y,deck_z-1,1.7,6),hexz(x,y,deck_z-.01,5.8,2.61))
for x in (34,66):deck=deck.cut(cyl(x,20,deck_z-1,3,6))
add('05_modular_deck_NO_WIRE_HOLDER',deck,colors['body'],rx=180)
# Parametric split clamp. The flange mounts independently of any primary wire.
def tube_clamp(z,flange_radius=45,bolt_circle=40,upper=False):
    a=cyl(50,50,z,flange_radius,4).fuse(cyl(50,50,z+4,34.3,18))
    a=a.fuse(box(42,80,z+8,7,14,10),box(51,80,z+8,7,14,10))
    a=a.cut(cyl(50,50,z-1,30.3,24),box(49,50,z+4,2,48,20))
    a=a.cut(cyl(41,88,z+13,1.7,18,(1,0,0)),hexx(55.3,88,z+13,5.8,2.8))
    for sx in (-1,1):
        for sy in (-1,1):
            x=50+sx*bolt_circle/math.sqrt(2);y=50+sy*bolt_circle/math.sqrt(2)
            a=a.cut(cyl(x,y,z-1,1.7,6))
            if upper:
                # Radial side loading of nuts, in the flange above the split collar.
                pocket=hexz(x,y,z+1.4,5.8,2.61)
                angle=math.atan2(y-50,x-50)*180/math.pi
                slot=box(0,-2.9,z+1.4,12,5.8,2.61).rotate((0,0,0),(0,0,1),angle).translate((x,y,0))
                a=a.cut(pocket,slot)
    return a
lower=tube_clamp(deck_z+4)
add('07_secondary_base_clamp',lower,colors['body'])
screw_joint('Lower_collar_pinch',3,16,(42,88,deck_z+17),(55.4,88,deck_z+17),axis=(1,0,0),nut_axis='x')
tube_z=deck_z; tube_top=tube_z+280
# Reference envelopes; primary and its holder deliberately omitted.
tube=cyl(50,50,tube_z,30,280).cut(cyl(50,50,tube_z-1,28.5,282))
add('secondary_tube_60x280',tube,(.75,.69,.58),'reference')
winding=cyl(50,50,tube_z+30,30.14224,213.36).cut(cyl(50,50,tube_z+29,30,215.36))
add('secondary_1500_turns_envelope',winding,(.72,.29,.09),'reference')
upper_clamp=tube_clamp(0,40,35,True).rotate((50,50,0),(51,50,0),180).translate((0,0,tube_top))
add('10_secondary_top_clamp',upper_clamp,colors['body'],rx=180)
screw_joint('Upper_collar_pinch',3,16,(42,12,tube_top-13),(55.4,12,tube_top-13),axis=(1,0,0),nut_axis='x')
cap=cyl(50,50,tube_top,40,4).fuse(cyl(50,50,tube_top+4,7,15))
cap=cap.cut(cyl(50,50,tube_top-1,2.25,22),cyl(60,50,tube_top-1,1.5,6))
for i,(sx,sy) in enumerate([(a,b) for a in (-1,1) for b in (-1,1)]):
    x=50+sx*35/math.sqrt(2);y=50+sy*35/math.sqrt(2)
    cap=cap.cut(cyl(x,y,tube_top-1,1.7,6))
    screw_joint(f'Top_cap_{i+1}',3,8,(x,y,tube_top+4),(x,y,tube_top-3.9))
add('11_topload_pedestal',cap,colors['body'])
toroid_z=tube_top+20
toroid=cq.Solid.makeTorus(55,20,cq.Vector(50,50,toroid_z),cq.Vector(0,0,1)).fuse(cyl(50,50,toroid_z-1,55,2)).cut(cyl(50,50,tube_top+17,2.25,8))
add('toroid_150x40_center_M4',toroid,(.76,.79,.82),'reference')
# M4 washers, one below the pedestal roof and one above the conductive center disk.
for label,z in [('lower',tube_top-.8),('upper',tube_top+21)]:
    hw('Toroid_washer_'+label,cyl(50,50,z,4.5,.8).cut(cyl(50,50,z-.1,2.15,1)), 'M4 washer 4.3x9x0.8')
screw_joint('Toroid',4,30,(50,50,tube_top-.8),(50,50,tube_top+21.8),axis=(0,0,1))
# Actual models and counts are kept separate from printable geometry.
add('hardware_fasteners',cq.Compound.makeCompound([h['shape'] for h in hardware]),(.64,.66,.69),'hardware')
assembly=cq.Assembly(name='ARCSTRIKE_case_v5_ASSEMBLY_PROTOTYPE')
for p in parts:assembly.add(p['shape'],name=p['name'],color=cq.Color(*p['color']))
assembly.export(str(OUT/'ARCSTRIKE-case-v5-ASSEMBLY.step'),exportType='STEP')
print('CAD exported; checking interference...',flush=True)
# Skip disjoint bounding boxes before expensive exact booleans.
def overlap(a,b):
    x=a.BoundingBox();y=b.BoundingBox()
    if any(min(getattr(x,k+'max'),getattr(y,k+'max'))-max(getattr(x,k+'min'),getattr(y,k+'min'))<1e-5 for k in 'xyz'):return 0.0
    return max(0,a.intersect(b).Volume())
checks=[];failures=[]
def check(a,sa,b,sb):
    v=overlap(sa,sb);checks.append(dict(part=a,reference=b,overlap_mm3=v))
    if v>.02:failures.append(checks[-1]);print('COLLISION',a,b,v,flush=True)
printed=[p for p in parts if p['kind']=='printed']
references=[p for p in parts if p['kind']=='reference']
for i,p in enumerate(printed):
    for q in printed[i+1:]+references:check(p['name'],p['shape'],q['name'],q['shape'])
for i,h in enumerate(hardware):
    for p in printed+references:check(h['name'],h['shape'],p['name'],p['shape'])
    for q in hardware[i+1:]:check(h['name'],h['shape'],q['name'],q['shape'])
check('PCB',pcb,'heatsink',sink);check('PCB',pcb,'C14',c14)
report=dict(status='ASSEMBLY / PRINT-FIT PROTOTYPE; not electrically or thermally qualified',primary_holder='DEFERRED BY USER: no conductor selected; modular interface only',dimensions_mm=dict(body_with_feet=[body,body,lid_z+lid_t-bottom+4],overall_height=toroid_z+20-bottom+4,deck_diameter=180,pcb_to_lid_vertical_gap=lid_z-pcb.BoundingBox().zmax),fiber_access=dict(opening_width_mm=32,opening_height_mm=28.8,entry_corner_radius_mm=3,rear_receiver_window_mm=[18,17],receiver_face_x_mm=-6.3,side_wall_x_mm=lo,receiver_recess_mm=-6.3-lo),heatsink_cradle=dict(nominal_envelope=[104,100,25],plan_range_mm=[96,112],height_range_mm=[20,30],shim_stack_nominal_mm=5,profile_source="user dimensioned drawing; adjustable cradle retained",fin_count=13,fin_pitch_mm=8,fin_thickness_mm=1.6,base_thickness_mm=5),interfaces=dict(tongue_height=1.6,tongue_thickness=1.8,groove_depth=1.9,groove_side_clearance=.25,M3_clearance=3.4,M3_nut_pocket_AF=5.8,M3_nut_pocket_height=2.6,M4_clearance=4.5,M4_nut_pocket_AF=7.4,M4_nut_pocket_height=3.5,tube_socket_diameter=60.6,nominal_pinch_gap=2),printed_parts=[dict(name=p['name'],solids=len(p['shape'].Solids()),print_rotation_x=p['print_rx']) for p in printed],joints=joints,hardware_counts=dict(Counter(h['item'] for h in hardware)),checks=checks,failures=failures)
(OUT/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
with (OUT/'hardware-BOM.csv').open('w',newline='') as f:
    w=csv.writer(f);w.writerow(['item','quantity']);w.writerows(report['hardware_counts'].items())
assert not failures,failures
# Assemble the standalone viewer from tessellations. Hardware has one checkbox.
meshes=[]
for part in parts:
    vertices,faces=part['shape'].tessellate(.3,.25);pos=[]
    for face in faces:
        for i in face:pos.extend(round(t,3) for t in vertices[i].toTuple())
    meshes.append(dict(name=part['name'],positions=pos,color=part['color'],kind=part['kind']))
(OUT/'viewer_meshes.json').write_text(json.dumps(meshes,separators=(',',':')))
runpy.run_path(str(ROOT/'build_viewer.py'))
print(json.dumps({k:v for k,v in report.items() if k!='checks'},indent=2));print('PASS:',len(checks),'interference checks',flush=True)
