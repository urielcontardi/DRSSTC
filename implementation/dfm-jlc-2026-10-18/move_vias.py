import pcbnew as p
b=p.LoadBoard('oneTesla.kicad_pcb')
moves={(47.25,88.0):(47.4,88.15),(64.325,81.25):(64.55,81.25),(66.75,89.5):(66.75,89.35),(45.76219,85.4):(45.85,85.6),(63.875,87.25):(64.0,87.25)}
for t in list(b.GetTracks()):
 if not isinstance(t,p.PCB_VIA):continue
 old=p.VECTOR2I(t.GetPosition());key=tuple(round(p.ToMM(x),5) for x in [old.x,old.y])
 if key not in moves:continue
 new=p.VECTOR2I(*[p.FromMM(x) for x in moves[key]])
 for s in b.GetTracks():
  if isinstance(s,p.PCB_VIA) or s.GetNetCode()!=t.GetNetCode():continue
  if s.GetStart()==old:s.SetStart(new)
  if s.GetEnd()==old:s.SetEnd(new)
 t.SetPosition(new)
p.SaveBoard('oneTesla.kicad_pcb',b)
