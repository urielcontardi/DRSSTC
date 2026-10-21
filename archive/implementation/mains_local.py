from pathlib import Path
import sys,uuid
r=Path(__file__).resolve().parents[1];sys.path.insert(0,str(r/'scripts'));from sexpr import *
b=parse((r/'oneTesla.kicad_pcb').read_text())
# Existing track widths preserved. Local corridor only; this is NOT an HV spacing qualification.
for t in children(b,'segment'):
 net=child(t,'net')[1];layer=child(t,'layer')[1]
 if net=='/PE' and layer=='F.Cu':
  for key in ['start','end']:
   p=child(t,key)
   if abs(float(p[2])-1.85)<1e-5:p[2]=.8
 if net=='/AC_L' and child(t,'uuid')[1] in ['615d7c44-1408-4cb0-939b-49592ee98d27','c39085b6-ca67-4b74-b1a6-a57dab2689fc']:
  for key in ['start','end']:
   p=child(t,key)
   if abs(float(p[2])-3.81)<1e-5:p[2]=2.8
b.append([Atom('segment'),[Atom('start'),74.93,3.81],[Atom('end'),74.93,2.8],[Atom('width'),2.54],[Atom('layer'),'F.Cu'],[Atom('net'),'/AC_L'],[Atom('uuid'),str(uuid.uuid4())]])
(r/'oneTesla.kicad_pcb').write_text(dump(b)+chr(10))
