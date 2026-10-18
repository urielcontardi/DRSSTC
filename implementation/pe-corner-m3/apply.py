"""Replace only the selected lower-left mounting hole and previous J2."""
from pathlib import Path
import re,json,sys
import pcbnew
ROOT=Path(__file__).resolve().parents[2]
name='PE_GND_Control_M3_D7.0mm'
notes='PE da tomada ao ponto dedicado do chassis e ao terminal olhal no parafuso M3 de J2. J2 ligado ao GND do controle, nunca DC_MINUS/DC_MID. Contato metalico firme no cobre exposto; arruela/olhal ate D7mm, sem isolante entre contato e cobre; fixar cabo contra tracao.'
status='Furo de fixacao da quina inferior esquerda reutilizado: (37.375,121.05)mm; PTH3.2mm, pad D7mm, olhal/arruela ate D7mm.'
p=ROOT/'oneTesla.kicad_sch';s=p.read_text();i=s.index('(property "Reference" "J2"');a=s.rfind('\n\t(symbol\n',0,i);z=s.index('\n\t(symbol\n',i);block=s[a:z]
for key,val in {'Footprint':'oneTesla:'+name,'Assembly_Notes':notes,'Footprint_Status':status}.items():
 block,n=re.subn(r'(\(property "'+key+r'" )"(?:\\.|[^"\\])*"',lambda m:m[1]+json.dumps(val),block);assert n==1
s=s[:a]+block+s[z:];p.write_text(s)
b=pcbnew.LoadBoard(str(ROOT/'oneTesla.kicad_pcb'))
old=next(f for f in b.GetFootprints() if f.GetReference()=='J2')
hole=next(f for f in b.GetFootprints() if f.GetReference()=='REF**' and abs(pcbnew.ToMM(f.GetPosition().x)-37.375)<.001 and abs(pcbnew.ToMM(f.GetPosition().y)-121.05)<.001)
f=pcbnew.FootprintLoad(str(ROOT/'library/oneTesla.pretty'),name);f.SetFPID(pcbnew.LIB_ID('oneTesla',name));f.SetReference('J2');f.SetValue(old.GetValue());f.Value().SetVisible(False);f.SetPosition(hole.GetPosition());f.SetPath(old.GetPath());f.SetUuid(old.m_Uuid)
for pad in f.Pads():pad.SetNet(b.FindNet('GND'))
for key,val in {'Assembly_Notes':notes,'Footprint_Status':status}.items():
 field=pcbnew.PCB_FIELD(f,pcbnew.FIELD_T_USER,key);field.SetText(val);field.SetVisible(False);f.Add(field)
b.Remove(old);b.Remove(hole);b.Add(f)
def pt(x,y):return pcbnew.VECTOR2I(pcbnew.FromMM(x),pcbnew.FromMM(y))
for a,z in [((37.375,121.05),(34.5,118.175)),((34.5,118.175),(34.5,106.5))]:
 t=pcbnew.PCB_TRACK(b);t.SetStart(pt(*a));t.SetEnd(pt(*z));t.SetWidth(pcbnew.FromMM(2));t.SetLayer(pcbnew.B_Cu);t.SetNet(b.FindNet('GND'));b.Add(t)
pcbnew.ZONE_FILLER(b).Fill(b.Zones());pcbnew.SaveBoard(str(ROOT/'oneTesla.kicad_pcb'),b)
print('J2 now shares the original lower-left M3 fixing hole. Other footprints and tracks preserved; GND extended with two segments.')
