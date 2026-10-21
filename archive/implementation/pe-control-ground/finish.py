import pcbnew
b=pcbnew.LoadBoard('oneTesla.kicad_pcb')
def pt(x,y):return pcbnew.VECTOR2I(pcbnew.FromMM(x),pcbnew.FromMM(y))
f=next(f for f in b.GetFootprints() if f.GetReference()=='J2');f.SetPosition(pt(35.5,39.5));f.Reference().SetPosition(pt(35.25,42.7));f.Reference().SetTextAngle(pcbnew.EDA_ANGLE(90,pcbnew.DEGREES_T))
t=pcbnew.PCB_TRACK(b);t.SetStart(pt(35.5,39.5));t.SetEnd(pt(35.5,68));t.SetWidth(pcbnew.FromMM(2));t.SetLayer(pcbnew.B_Cu);t.SetNet(b.FindNet('GND'));b.Add(t)
for d in b.GetDrawings():
 if d.GetClass()=='PCB_TEXT' and d.GetText()=='TERRA / PE':d.SetPosition(pt(35.25,48.5));d.SetText('PE / TERRA')
 if d.GetClass()=='PCB_TEXT' and d.GetText()=='GND CONTROLE':
  d.SetPosition(pt(47.5,39.5));d.SetText('J2 PE - GND CONTROLE');d.SetTextAngle(pcbnew.EDA_ANGLE(0,pcbnew.DEGREES_T));d.SetLayer(pcbnew.B_SilkS);d.SetMirrored(True)
pcbnew.ZONE_FILLER(b).Fill(b.Zones());pcbnew.SaveBoard('oneTesla.kicad_pcb',b)
