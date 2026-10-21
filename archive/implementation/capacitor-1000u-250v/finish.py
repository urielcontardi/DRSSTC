import pcbnew
b=pcbnew.LoadBoard('oneTesla.kicad_pcb')
def pt(x,y):return pcbnew.VECTOR2I(pcbnew.FromMM(x),pcbnew.FromMM(y))
f=next(f for f in b.GetFootprints() if f.GetReference()=='C11');f.SetPosition(pt(126,55.4));f.Reference().SetPosition(pt(126,46.5))
p=next(f for f in b.GetFootprints() if f.GetReference()=='P2');p.SetPosition(pt(135,31.5));p.Reference().SetPosition(pt(139,31.5))
changes={(121.5,56.2):(121.5,55.4),(130.5,56.2):(130.5,55.4),(125.7,61):(124.9,61),(114,56.2):(114,55.4),(122.5,57.2):(122.5,56.4)}
for t in b.GetTracks():
 for get,setter in [(t.GetStart,t.SetStart),(t.GetEnd,t.SetEnd)]:
  p=get();a=(round(pcbnew.ToMM(p.x),5),round(pcbnew.ToMM(p.y),5))
  if a in changes:setter(pt(*changes[a]))
for a,z in zip([(135,31.5),(135,44.5),(127,52.5),(121.5,55.4)],[(135,44.5),(127,52.5),(121.5,55.4)]):
 t=pcbnew.PCB_TRACK(b);t.SetStart(pt(*a));t.SetEnd(pt(*z));t.SetWidth(pcbnew.FromMM(3));t.SetLayer(pcbnew.F_Cu);t.SetNet(b.FindNet('/DC_MID'));b.Add(t)
pcbnew.ZONE_FILLER(b).Fill(b.Zones());pcbnew.SaveBoard('oneTesla.kicad_pcb',b)
