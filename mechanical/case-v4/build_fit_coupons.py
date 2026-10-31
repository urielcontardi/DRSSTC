from pathlib import Path
import cadquery as cq
import math
OUT=Path(__file__).resolve().parent/'exports'/'print';OUT.mkdir(parents=True,exist_ok=True)
def box(x,y,z,dx,dy,dz):return cq.Solid.makeBox(dx,dy,dz,cq.Vector(x,y,z))
def cyl(x,y,z,r,h):return cq.Solid.makeCylinder(r,h,cq.Vector(x,y,z))
def hx(x,y,z,af,h):
    r=af/math.sqrt(3);w=cq.Wire.makePolygon([cq.Vector(x+r*math.cos(i*math.pi/3),y+r*math.sin(i*math.pi/3),z) for i in range(6)],close=True)
    return cq.Solid.extrudeLinear(w,[],cq.Vector(0,0,h))
def save(name,s):
    assert s.isValid() and len(s.Solids())==1
    cq.exporters.export(s,str(OUT/(name+'.stl')),tolerance=.06)
# Counterbores on top; nuts load from the bottom, as on the lid/module joints.
s=box(0,0,0,32,16,10)
s=s.cut(cyl(8,8,-1,1.7,12),hx(8,8,-.01,5.8,2.61),cyl(8,8,6.6,3.2,4))
s=s.cut(cyl(24,8,-1,2.25,12),hx(24,8,-.01,7.4,3.51),cyl(24,8,5.6,4,5))
save('90_coupon_M3_M4',s)
s=box(0,0,0,24,16,4).fuse(box(3,3,4,18,10,1.6).cut(box(4.8,4.8,3.9,14.4,6.4,2)))
save('91_coupon_tongue',s)
s=box(0,0,0,24,16,4)
pocket=box(2.75,2.75,2.1,18.5,10.5,2).cut(box(5.05,5.05,2,13.9,5.9,3))
save('92_coupon_groove',s.cut(pocket))
save('93_coupon_tube_60p6',cyl(34.3,34.3,0,34.3,6).cut(cyl(34.3,34.3,-1,30.3,8)))
print('4 fit coupons exported')
