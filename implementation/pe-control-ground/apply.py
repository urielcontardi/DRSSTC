"""Record of the PE connection change; run once using KiCad Python."""
from pathlib import Path
import re, json, uuid, sys
import pcbnew
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts'))
from sexpr import parse, children, child, prop

name='PE_Control_GND_WirePad_D4.0mm_Drill2.2mm'
src=(ROOT/'library/oneTesla.pretty/Primary_WirePad_D4.0mm_Drill2.2mm.kicad_mod').read_text()
src=src.replace('Primary_WirePad_D4.0mm_Drill2.2mm',name)
src=src.replace('Ponto de solda direta do fio do primario: um pad circularD4mm, furo metalizadoD2.2mm; sem borne ou parafuso.', 'Entrada do fio PE: pad de solda D4/furo2.2 ligado ao GND do controle. Chassis deve receber PE por ligacao externa dedicada; nunca ligar ao barramento de potencia.')
(ROOT/'library/oneTesla.pretty'/f'{name}.kicad_mod').write_text(src)

path=ROOT/'oneTesla.kicad_sch';text=path.read_text()
start=text.rfind('\n\t(symbol\n',0,text.index('(property "Reference" "J2"'))
end=text.index('\n\t(symbol\n',start+1);block=text[start:end]
notes='PE da tomada: ligar primeiro ao ponto dedicado do chassis metalico; derivar fio para J2, soldado com alivio de tracao. J2 ligado ao GND do controle (PS1 -Vo). Nunca ligar PE a DC_MINUS, DC_MID ou SW_NODE. J1 somente L/N.'
fields={'Value':'PE / GND CONTROLE','Footprint':'oneTesla:'+name,'Description':'Entrada de terra de protecao ligada ao GND do controle, conforme topologia original oneTeslaTS.','Assembly_Notes':notes,'Footprint_Status':'Pad de solda D4mm, furo PTH2.2mm; sem parafuso. Fio PE com alivio de tracao externo.'}
for key,value in fields.items():
 block,n=re.subn(r'(\(property "'+key+r'" )"(?:\\.|[^"\\])*"',lambda m:m[1]+json.dumps(value),block)
 assert n==1
text=text[:start]+block+text[end:]
assert text.count('(label "PE"')==1
text=text.replace('(label "PE"','(label "GND"')
text=text.replace('1 = L; 2 = N. PE externo em J2/CHASSIS, separado de GND e DC_MINUS.', '1 = L; 2 = N. PE externo ao chassis e J2/GND CONTROLE; nunca a DC_MINUS ou DC_MID.')
extra='''
  (text "TERRA / PE: chassis metalico + J2 (GND CONTROLE).\\nNunca ligar a DC_MINUS, DC_MID ou SW_NODE."
    (at 18 235 0)
    (effects (font (size 1.0 1.0)) (justify left top))
    (uuid "'''+str(uuid.uuid4())+'''"))
'''
text=text.rstrip()[:-1]+extra+')\n';path.write_text(text)

board=pcbnew.LoadBoard(str(ROOT/'oneTesla.kicad_pcb'))
assert not any(f.GetReference()=='J2' for f in board.GetFootprints())
sch=parse(text);sym=next(s for s in children(sch,'symbol') if prop(s,'Reference')[2]=='J2')
fp=pcbnew.FootprintLoad(str(ROOT/'library/oneTesla.pretty'),name)
fp.SetReference('J2');fp.SetValue(fields['Value']);fp.Value().SetVisible(False)
fp.SetFPID(pcbnew.LIB_ID('oneTesla',name))
fp.SetPath(pcbnew.KIID_PATH('/38e9e92e-0807-45b3-a56d-ef1f03ff1cd0/'+str(child(sym,'uuid')[1])))
fp.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(35.5),pcbnew.FromMM(68)))
for key in ['Description','Assembly_Notes','Footprint_Status']:
 field=pcbnew.PCB_FIELD(fp,pcbnew.FIELD_T_DESCRIPTION if key=='Description' else pcbnew.FIELD_T_USER,key)
 field.SetText(fields[key]);field.SetVisible(False);fp.Add(field)
for p in fp.Pads():p.SetNet(board.FindNet('GND'));p.SetLocalZoneConnection(pcbnew.ZONE_CONNECTION_FULL)
board.Add(fp)
def point(x,y):return pcbnew.VECTOR2I(pcbnew.FromMM(x),pcbnew.FromMM(y))
# Route only in the isolated output area, away from the AC pins at y=30.87.
for a,z in [((35.5,68),(60.7325,68)),((60.7325,68),(66.1,73.3675))]:
 t=pcbnew.PCB_TRACK(board);t.SetStart(point(*a));t.SetEnd(point(*z));t.SetWidth(pcbnew.FromMM(2));t.SetLayer(pcbnew.B_Cu);t.SetNet(board.FindNet('GND'));board.Add(t)
for label,x,y in [('TERRA / PE',35.5,55.5),('GND CONTROLE',37.5,55.5)]:
 t=pcbnew.PCB_TEXT(board);t.SetText(label);t.SetPosition(point(x,y));t.SetTextAngle(pcbnew.EDA_ANGLE(90,pcbnew.DEGREES_T));t.SetTextSize(point(0.9,0.9));t.SetTextThickness(pcbnew.FromMM(0.15));t.SetLayer(pcbnew.F_SilkS);board.Add(t)
pcbnew.ZONE_FILLER(board).Fill(board.Zones())
pcbnew.SaveBoard(str(ROOT/'oneTesla.kicad_pcb'),board)
print('J2 placed at (35.5,68) mm, GND/control; two B.Cu tracks added to PS1.3; zones refilled.')
