from pathlib import Path
import sys,uuid
r=Path(__file__).resolve().parents[1];sys.path.insert(0,str(r/'scripts'));from sexpr import *
b=parse((r/'oneTesla.kicad_pcb').read_text());s=parse((r/'oneTesla.kicad_sch').read_text());sy={prop(x,'Reference')[2]:x for x in children(s,'symbol')}
for f in children(b,'footprint'):
 ref=prop(f,'Reference')[2]
 if ref=='FB1':
  for p in children(f,'pad'):
   a=child(p,'at')
   if len(a)>3:a[3]=0 # pad rotation is relative to footprint in this file format
 if ref in sy:
  for key in ['Datasheet','Description']:
   src=prop(sy[ref],key)
   if src:
    p=prop(f,key)
    if p:p[2]=src[2]
for t in list(children(b,'segment')):
 net=child(t,'net')[1];a=child(t,'start');z=child(t,'end');layer=child(t,'layer')[1]
 if net=='Net-(D1-K)' and layer=='B.Cu' and min(float(a[2]),float(z[2]))>=61.595:b.remove(t)
 if net=='GND' and layer=='B.Cu' and max(float(a[1]),float(z[1]))<=20 and min(float(a[2]),float(z[2]))>=59.055:b.remove(t)
 if net=='+5V' and layer=='B.Cu':
  for pt in [a,z]:
   if abs(float(pt[1])-24.2)<.0001:pt[1]=24.15

def route(net,pts,layer='F.Cu'):
 for a,z in zip(pts,pts[1:]):b.append([Atom('segment'),[Atom('start'),*a],[Atom('end'),*z],[Atom('width'),.4064],[Atom('layer'),layer],[Atom('net'),net],[Atom('uuid'),str(uuid.uuid4())]])
route('Net-(D1-K)',[(11.43,74.93),(10,74.93),(10,60.32),(21.595,60.32),(22.86,59.055)])
route('GND',[(20,69.76),(17,69.76),(17,62.9),(12.8,62.9),(12.8,59.055),(15.24,59.055)],'B.Cu')
(r/'oneTesla.kicad_pcb').write_text(dump(b)+chr(10))
