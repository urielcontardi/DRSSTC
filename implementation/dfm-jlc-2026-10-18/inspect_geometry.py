import pcbnew as p,json
b=p.LoadBoard('oneTesla.kicad_pcb'); mm=p.FromMM
pads=[]
for f in b.GetFootprints():
 for pad in f.Pads():
  if pad.GetAttribute()==p.PAD_ATTRIB_NPTH or not (pad.IsOnLayer(p.F_Cu) or pad.IsOnLayer(p.B_Cu)):continue
  poly=p.SHAPE_POLY_SET();pad.TransformShapeToPolygon(poly,p.F_Cu,0,mm(.001),p.ERROR_OUTSIDE)
  pads.append((f.GetReference(),pad,poly))
for i,(r,a,pa) in enumerate(pads):
 for s,c,pc in pads[i+1:]:
  if not any(a.IsOnLayer(l) and c.IsOnLayer(l) for l in [p.F_Cu,p.B_Cu]):continue
  if (a.GetPosition()-c.GetPosition()).EuclideanNorm()>mm(10):continue
  if pa.Collide(pc,mm(.20)):
   print('PAD GAP',r,a.GetNumber(),s,c.GetNumber(),a.GetNetname(),c.GetNetname(), 'overlap',pa.Collide(pc,0))
