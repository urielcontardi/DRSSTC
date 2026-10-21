"""One-shot migration from 028ef6e; never a general board generator."""
from pathlib import Path
import sys,uuid,copy
r=Path(__file__).resolve().parents[1];sys.path.insert(0,str(r/'scripts'));from sexpr import *
b=parse((r/'oneTesla.kicad_pcb').read_text());s=parse((r/'oneTesla.kicad_sch').read_text())
assert any(prop(f,'Reference')[2]=='R1' and str(f[1]).endswith('R_L25_P22.86_INCOMPATIBLE') for f in children(b,'footprint')), 'Migration already applied or incompatible baseline; stop without writing.'
for g in b:
 if isinstance(g,list) and child(g,'layer') and child(g,'layer')[1]=='Edge.Cuts':
  for k in ['start','end']:
   p=child(g,k)
   if p:
    if float(p[1])==106.045:p[1]=145
    if float(p[2])==0:p[2]=-2
# The selected D30 envelopes are unchanged; spacing is an assembly allocation, not HV qualification.
for f in children(b,'footprint'):
 ref=prop(f,'Reference')[2]
 if ref in ['C11','C12']:
  child(f,'at')[1:3]=[125,60 if ref=='C11' else 25]
 if ref=='R1':
  f[1]='oneTesla:R_L25_P30.48_Provisional'
  for p in children(f,'pad'):child(p,'at')[1]=-15.24 if p[1]=='1' else 15.24
  if prop(f,'Footprint_Status'):prop(f,'Footprint_Status')[2]='PROVISIONAL body25mm; lead spacing30.48mm (2.74mm each side). Confirm exact MPN, lead forming and thermal clearance.'
for z in children(b,'zone'):
 if child(z,'net')[1] in ['/DC_PLUS','/DC_MINUS']:
  for xy in children(child(child(z,'polygon'),'pts'),'xy'):
   if float(xy[1])==104.14:xy[1]=142
# Remove former capacitor-to-capacitor top trace; replace the absent PTH interlayer links explicitly.
for t in list(children(b,'segment')):
 if child(t,'uuid')[1] in ['143f1bef-cd67-4d0f-be97-a9fd5c9f1c89','28790596-c002-4c43-bb70-da54eb20d2f7']:b.remove(t)
 # R1 pin2 track follows new lead position, avoiding an obsolete stub.
 if child(t,'net')[1]=='Net-(D1-K)':
  for k in ['start','end']:
   p=child(t,k)
   if float(p[2])==74.93 and float(p[1]) in [10,11.43]:p[2]=71.12
 # Pin1 circuit lead moved downward. Keep old horizontal segment and add short perpendicular approach.
def route(net,pts,layer,width):
 for a,z in zip(pts,pts[1:]):b.append([Atom('segment'),[Atom('start'),*a],[Atom('end'),*z],[Atom('width'),width],[Atom('layer'),layer],[Atom('net'),net],[Atom('uuid'),str(uuid.uuid4())]])
route('/DC_MID',[(71.755,31.75),(110,31.75),(110,18),(130.08,18),(130.08,25)],'B.Cu',2.54)
route('/DC_MID',[(130.08,25),(130.08,30),(116,30),(116,60),(119.92,60)],'F.Cu',2.54)
f=next(f for f in children(b,'footprint') if prop(f,'Reference')[2]=='R1');pn=next(p for p in children(f,'pad') if p[1]=='1');net=child(pn,'net')[1]
route(net,[(11.43,97.79),(11.43,101.6)],'F.Cu',.4064)
# Library model: preserve body/polarity/courtyard; widen courtyard to include new pads if necessary.
p=r/'library/oneTesla.pretty/R_L25_P22.86_INCOMPATIBLE.kicad_mod';t=parse(p.read_text());t[1]='R_L25_P30.48_Provisional';prop(t,'Value')[2]=t[1]
for pad in children(t,'pad'):child(pad,'at')[1]=-15.24 if pad[1]=='1' else 15.24
child(t,'descr')[1]='Provisional axial power resistor body25x6.4; P30.48, drill1.3; 2.74mm lead allowance per side. Exact part and heat dissipation unqualified.'
(r/'library/oneTesla.pretty/R_L25_P30.48_Provisional.kicad_mod').write_text(dump(t)+chr(10))
for sym in children(s,'symbol'):
 if prop(sym,'Reference')[2]=='R1':
  prop(sym,'Footprint')[2]='oneTesla:R_L25_P30.48_Provisional'
  prop(sym,'Footprint_Status')[2]=prop(f,'Footprint_Status')[2]
(r/'oneTesla.kicad_pcb').write_text(dump(b)+chr(10));(r/'oneTesla.kicad_sch').write_text(dump(s)+chr(10))
print('Outline145 x108.045; C12(125,25), C11(125,60); R1P30.48; no mounting hole moved')
