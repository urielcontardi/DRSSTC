import pcbnew as p,json
from pathlib import Path
b=p.LoadBoard('oneTesla.kicad_pcb');mm=p.FromMM
changes=[]
for t in b.GetTracks():
 if isinstance(t,p.PCB_VIA) and t.GetWidth()<mm(.7):
  changes.append(dict(kind='via',uuid=str(t.m_Uuid.AsString()),x=p.ToMM(t.GetPosition().x),y=p.ToMM(t.GetPosition().y),old=p.ToMM(t.GetWidth()),new=.7));t.SetWidth(mm(.7))
for f in b.GetFootprints():
 if f.GetReference()=='JCT1':
  old=[p.VECTOR2I(a.GetPosition()) for a in f.Pads()];delta=p.VECTOR2I(0,-mm(1));f.Move(delta)
  for t in b.GetTracks():
   if isinstance(t,p.PCB_VIA):continue
   if any(t.GetStart()==a for a in old):t.SetStart(t.GetStart()+delta)
   if any(t.GetEnd()==a for a in old):t.SetEnd(t.GetEnd()+delta)
  changes.append(dict(kind='footprint',ref='JCT1',move_y=-1))
texts=list(b.GetDrawings())
for f in b.GetFootprints():texts+=list(f.GraphicalItems())+[f.Reference(),f.Value()]
for t in texts:
 if t.GetLayer() not in [p.F_SilkS,p.B_SilkS]:continue
 if isinstance(t,p.PCB_TEXT):
  t.SetTextThickness(max(t.GetTextThickness(),mm(.15)))
  size=t.GetTextSize();t.SetTextSize(p.VECTOR2I(max(size.x,mm(1)),max(size.y,mm(1))))
 elif isinstance(t,p.PCB_SHAPE):t.SetWidth(max(t.GetWidth(),mm(.15)))
p.SaveBoard('oneTesla.kicad_pcb',b)
Path('implementation/dfm-jlc-2026-10-18/changes.json').write_text(json.dumps(changes,indent=2))
print('Changed',len(changes),'copper items; silk thickness normalized')
