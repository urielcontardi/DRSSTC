"""Apply selected capacitor envelopes; preserve unrelated circuits and mounting holes."""
from pathlib import Path
import sys,re,json,copy
import pcbnew
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'scripts'))
from sexpr import parse,children,child,prop
name='CP_SnapIn_D30.3_H40.5_P9.00_ReviewPending'
status='1000uF 250V snap-in; D30.3 x H40.5mm, P9mm informados pelo usuario. MPN e secao dos terminais nao fornecidos; pad4/furo2mm a confirmar na peca.'
path=ROOT/'oneTesla.kicad_sch';text=path.read_text()
for ref in ['C11','C12']:
 i=text.index('(property "Reference" "'+ref+'"');a=text.rfind('\n\t(symbol\n',0,i);z=text.index('\n\t(symbol\n',i);block=text[a:z]
 for key,val in {'Value':'1000u 250V','Footprint':'oneTesla:'+name,'Description':status,'Footprint_Status':status}.items():
  block,n=re.subn(r'(\(property "'+key+r'" )"(?:\\.|[^"\\])*"',lambda m:m[1]+json.dumps(val),block);assert n==1
 text=text[:a]+block+text[z:]
path.write_text(text)
board=pcbnew.LoadBoard(str(ROOT/'oneTesla.kicad_pcb'))
def pt(x,y):return pcbnew.VECTOR2I(pcbnew.FromMM(x),pcbnew.FromMM(y))
def field(fp,k,value):
 f=fp.GetField(k)
 if f is None:
  f=pcbnew.PCB_FIELD(fp,pcbnew.FIELD_T_DESCRIPTION if k=='Description' else pcbnew.FIELD_T_USER,k);fp.Add(f)
 f.SetText(value);f.SetVisible(False)
created=[]
original_footprints=list(board.GetFootprints())
for old in original_footprints:
 ref=old.GetReference()
 if ref not in ['C11','C12']:continue
 f=pcbnew.FootprintLoad(str(ROOT/'library/oneTesla.pretty'),name);f.SetFPID(pcbnew.LIB_ID('oneTesla',name))
 f.SetReference(ref);f.SetValue('1000u 250V');f.Value().SetVisible(False);f.SetPath(old.GetPath());f.SetUuid(old.m_Uuid)
 x=126 if ref=='C11' else 94.75
 f.SetPosition(pt(x,56.2));f.Reference().SetPosition(pt(x,47.0));f.Reference().SetTextAngle(pcbnew.EDA_ANGLE(0,pcbnew.DEGREES_T))
 for p in f.Pads():
  source=next(q for q in old.Pads() if q.GetNumber()==p.GetNumber());p.SetNet(source.GetNet());p.SetUuid(source.m_Uuid)
 for k in ['Description','Footprint_Status']:field(f,k,status)
 board.Remove(old);board.Add(f);created.append(f)

j=next(f for f in board.GetFootprints() if f.GetReference()=='J110');j.SetPosition(pt(137,85));j.Reference().SetPosition(pt(137,72));j.Reference().SetTextAngle(pcbnew.EDA_ANGLE(0,pcbnew.DEGREES_T))
# Preserve left, top and bottom extents; extend only the right edge by 11 mm.
for d in board.GetDrawings():
 if d.GetLayer()!=pcbnew.Edge_Cuts:continue
 for getter,setter in [(d.GetStart,d.SetStart),(d.GetEnd,d.SetEnd)]:
  p=getter()
  if p.x==pcbnew.FromMM(131.375):setter(pt(142.375,pcbnew.ToMM(p.y)))

remove={'3269a46d-fbcf-4139-b0fd-ca714e246b2a','3739dc8a-1412-423f-bd85-ce86916c7740','1d90c462-2520-4521-8b98-456bf277a053','05504d55-62ea-419e-94f1-dd22fd690bfd','8f667199-5ddb-4754-ab33-e44f7e379c0e'}
for t in list(board.GetTracks()):
 if t.m_Uuid.AsString() in remove:board.Remove(t)
def route(net,layer,points,width=3):
 for a,z in zip(points,points[1:]):
  t=pcbnew.PCB_TRACK(board);t.SetStart(pt(*a));t.SetEnd(pt(*z));t.SetWidth(pcbnew.FromMM(width));t.SetLayer(layer);t.SetNet(board.FindNet(net));board.Add(t)
route('/DC_PLUS',pcbnew.B_Cu,[(89.2,61),(90.25,59.95),(90.25,56.2)])
route('/DC_MINUS',pcbnew.B_Cu,[(121.8,61),(125.7,61),(130.5,56.2)])
route('/DC_MID',pcbnew.B_Cu,[(121.5,56.2),(114,56.2)])
route('/DC_MID',pcbnew.F_Cu,[(121.5,56.2),(122.5,57.2),(122.5,87.5),(127.62,92.62),(137,92.62)])
route('/AC_N',pcbnew.B_Cu,[(117.5,38.05),(119.05,36.5),(134,36.5),(137,39.5),(137,77.38)])
pcbnew.ZONE_FILLER(board).Fill(board.Zones());pcbnew.SaveBoard(str(ROOT/'oneTesla.kicad_pcb'),board)
print('C11/C12 1000uF250V D30.3 H40.5 P9; C12 (94.75,56.2), C11 (126,56.2); PCB111x100; J110 (137,85). Mounting holes and remaining footprints preserved.')
