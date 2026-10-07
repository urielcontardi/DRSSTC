from pathlib import Path
import sys,json,copy,uuid
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root/'scripts'))
from sexpr import *
b=parse((root/'oneTesla.kicad_pcb').read_text());s=parse((root/'oneTesla.kicad_sch').read_text());changes=json.loads((root/'implementation/evidence/footprint-changes.json').read_text())
syms={prop(x,'Reference')[2]:x for x in children(s,'symbol')}
def uid():return str(uuid.uuid4())
def fresh(n):
 if not isinstance(n,list):return
 if n and n[0]=='uuid':n[1]=uid()
 else:
  for v in n:fresh(v)
for f in list(children(b,'footprint')):
 ref=prop(f,'Reference')[2];old=str(f[1]).split(':')[-1]
 new=changes[old][1] if old in changes else old
 if old in changes or ref=='FB1':
  t=parse((root/'library/oneTesla.pretty'/(new+'.kicad_mod')).read_text());t[1]='oneTesla:'+new
  # Preserve placement, identity, schematic path and actual pin nets.
  for key in ['at','uuid','path','sheetname','sheetfile']:
   n=child(f,key)
   if n:
    prev=child(t,key)
    if prev:t.remove(prev)
    t.append(copy.deepcopy(n))
  if ref=='FB1':child(t,'at')[1:]=[20,72.3,90]
  angle=float(child(t,'at')[3]) if len(child(t,'at'))>3 else 0
  oldpads={p[1]:p for p in children(f,'pad') if p[1]}
  for p in children(t,'pad'):
   net=child(oldpads.get(p[1],[]),'net')
   if net:p.append(copy.deepcopy(net))
   elif ref=='FB1' and p[1] in ['5','8']:
    # Unique unconnected nets agree with the schematic, never bonded to GND.
    fromnet='unconnected-(FB1-NC-Pad'+p[1]+')'
    # Get exact native net name, not an invented electrical connection.
    nt=parse((root/'implementation/evidence/schematic.net').read_text())
    for netnode in children(child(nt,'nets'),'net'):
     if any(child(n,'ref')[1]=='FB1' and child(n,'pin')[1]==p[1] for n in children(netnode,'node')):fromnet=child(netnode,'name')[1]
    p.append([Atom('net'),fromnet])
   at=child(p,'at')
   if len(at)<4:at.append(angle)
   else:at[3]=float(at[3])+angle
   fresh(p)
  for key in ['Reference','Value']:
   prop(t,key)[2]=prop(f,key)[2]
  for n in t:
   if isinstance(n,list) and str(n[0]).startswith('fp_'):fresh(n)
  b[b.index(f)]=t;f=t
 if ref in syms:
  if ref in ['Z1','Z2']:
   attr=child(f,'attr')
   if Atom('dnp') not in attr:attr.append(Atom('dnp'))
  for key in ['Footprint_Status','Assembly_Notes']:
   src=prop(syms[ref],key)
   if src:
    prev=prop(f,key)
    if prev:f.remove(prev)
    f.append([Atom('property'),key,src[2],[Atom('at'),0,0,0],[Atom('layer'),'F.Fab'],[Atom('hide'),Atom('yes')],[Atom('effects'),[Atom('font'),[Atom('size'),1,1],[Atom('thickness'),0.15]]]])
# Remove only obsolete optical routing and the isolated +5 V stubs for old receiver.
for t in list(children(b,'segment')):
 net=child(t,'net')[1];a=child(t,'start');z=child(t,'end')
 if net=='/OPTICAL_OUT' or (net=='+5V' and max(float(a[1]),float(z[1]))<=12 and min(float(a[2]),float(z[2]))>=60):b.remove(t)
def route(net,pts,layer='F.Cu',width=.4064):
 for a,z in zip(pts,pts[1:]):b.append([Atom('segment'),[Atom('start'),*a],[Atom('end'),*z],[Atom('width'),width],[Atom('layer'),layer],[Atom('net'),net],[Atom('uuid'),uid()]])
route('/OPTICAL_OUT',[(20,72.3),(27.5,72.3),(27.5,63.695),(25.4,61.595)])
route('+5V',[(20,67.22),(20,64.68)])
route('+5V',[(20,64.68),(24.2,64.68),(24.2,57),(9.485,57),(9.485,56.515)],'B.Cu')
route('GND',[(20,69.76),(18,69.76),(18,63.6),(15.24,60.84),(15.24,59.055)],'B.Cu')
(root/'oneTesla.kicad_pcb').write_text(dump(b)+chr(10))
print('PCB: corrected footprints, DNP/fields, FB1 placement and routing; outline preserved')
