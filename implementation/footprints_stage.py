from pathlib import Path
import sys,copy,uuid,json
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root/'scripts'))
from sexpr import *
lib=root/'library/oneTesla.pretty'
# Recenter complete non-pad geometry around the actual pad pair. Dimensions unchanged.
changes={
'CP_Radial_D8.0mm_P3.50mm':(1.75,'CP_D8_P2.54_ReviewPending'),
'CP_Radial_D12.5mm_P5.00mm':(2.5,'CP_D12.5_P3.556_ReviewPending'),
'CP_Radial_D30.0mm_P10.00mm_SnapIn':(5,'CP_D30_P10.16_ReviewPending'),
'R_Axial_Power_L25.0mm_W6.4mm_P30.48mm':(15.24,'R_L25_P22.86_INCOMPATIBLE'),
'R_Axial_DIN0309_L9.0mm_D3.2mm_P12.70mm_Horizontal':(6.35,'R_L9_P10.16_ReviewPending'),
'D_DO-201AD_P15.24mm_Horizontal':(7.62,'D_DO201AD_P14.732_ReviewPending')}
def shift(node,dx):
 if not isinstance(node,list):return
 if node and node[0] in ['at','start','end','mid','center','xy'] and len(node)>2:node[1]=round(float(node[1])-dx,6)
 else:
  for n in node:shift(n,dx)
def fresh(node):
 if not isinstance(node,list):return
 if node and node[0]=='uuid':node[1]=str(uuid.uuid4())
 else:
  for n in node:fresh(n)
for old,(dx,new) in changes.items():
 t=parse((lib/(old+'.kicad_mod')).read_text());t[1]=new
 for n in list(t):
  if isinstance(n,list):
   if str(n[0]).startswith('fp_') or n[0]=='property':shift(n,dx)
   if n[0]=='model':t.remove(n) # stale 3D cannot represent altered lead geometry
 if prop(t,'Value'):prop(t,'Value')[2]=new
 if child(t,'descr'):child(t,'descr')[1]='Custom review geometry; original body retained/recentered; actual pitch in name; exact MPN NOT qualified.'
 if old.startswith('CP_'):
  for pad in children(t,'pad'):
   if pad[1]=='1':pad[3]=Atom('rect')
 (lib/(new+'.kicad_mod')).write_text(dump(t)+chr(10))
# Native KiCad HFBR model, mechanically checked against Broadcom pp4/11.
t=parse((root/'implementation/evidence/HFBR-upstream.kicad_mod').read_text());t[1]='HFBR-2521ETZ'
for pad in children(t,'pad'):
 if pad[1]=='6':pad[1]='8' # manufacturer retaining pin designation
child(t,'descr')[1]='Broadcom HFBR-2521ETZ horizontal; AV02-3283EN pp4/11; pitch 2.54; retaining pins 5/8 electrically NC. KiCad native HFBR-252x geometry.'
prop(t,'Value')[2]='HFBR-2521ETZ'
(lib/'HFBR-2521ETZ.kicad_mod').write_text(dump(t)+chr(10))
s=parse((root/'oneTesla.kicad_sch').read_text())
for sym in children(s,'symbol'):
 p=prop(sym,'Footprint')
 if p and p[2].startswith('oneTesla:') and p[2].split(':')[1] in changes:p[2]='oneTesla:'+changes[p[2].split(':')[1]][1]
(root/'oneTesla.kicad_sch').write_text(dump(s)+chr(10))
(root/'implementation/evidence/footprint-changes.json').write_text(json.dumps(changes,indent=2))
print('6 custom models recentered; HFBR corrected; remaining exact parts NOT assumed')
