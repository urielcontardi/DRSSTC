import pcbnew as p,math,json
from pathlib import Path
b=p.LoadBoard('oneTesla.kicad_pcb');mm=p.FromMM;err=mm(.002);clear=mm(.18)
logs=[]
def poly(n):
 q=p.SHAPE_POLY_SET()
 if isinstance(n,p.PCB_TEXT):n.TransformTextToPolySet(q,0,err,p.ERROR_OUTSIDE)
 else:n.TransformShapeToPolygon(q,n.GetLayer(),0,err,p.ERROR_OUTSIDE)
 return q
def coll(a,b):
 return a.BBox().Intersects(b.BBox()) and a.Collide(b,0)
def inflate(q,d):
 z=q.CloneDropTriangulation();z.Inflate(d,p.CORNER_STRATEGY_ROUND_ALL_CORNERS,err);return z
ob={p.F_SilkS:[],p.B_SilkS:[]}
for f in b.GetFootprints():
 for pad in f.Pads():
  for layer,mask,cu in [(p.F_SilkS,p.F_Mask,p.F_Cu),(p.B_SilkS,p.B_Mask,p.B_Cu)]:
   q=p.SHAPE_POLY_SET()
   if pad.IsOnLayer(mask):pad.TransformShapeToPolygon(q,cu,0,err,p.ERROR_OUTSIDE)
   elif pad.GetDrillSize().x:pad.TransformHoleToPolygon(q,0,err,p.ERROR_OUTSIDE)
   if q.OutlineCount():ob[layer].append(inflate(q,clear))
# Keep ink clear of via drill mouths, including tented vias.
for via in b.GetTracks():
 if not isinstance(via,p.PCB_VIA):continue
 q=p.SHAPE_POLY_SET();q.NewOutline();pos=via.GetPosition();radius=via.GetDrillValue()/2
 for i in range(32):
  a=2*math.pi*i/32;q.Append(round(pos.x+radius*math.cos(a)),round(pos.y+radius*math.sin(a)))
 for layer in ob:ob[layer].append(inflate(q,clear))
# Keep labels inside the outline and away from every exposed pad and drilled hole.
texts=[];graphics=[]
for n in b.GetDrawings():
 if n.GetLayer() in ob:(texts if isinstance(n,p.PCB_TEXT) else graphics).append((None,n))
for f in b.GetFootprints():
 for n in list(f.GraphicalItems())+[f.Reference(),f.Value()]:
  if n.GetLayer() in ob and (not isinstance(n,p.PCB_TEXT) or n.IsVisible()):
   (texts if isinstance(n,p.PCB_TEXT) else graphics).append((f,n))
def inside(q):
 bb=q.BBox();return bb.GetX()>mm(31.60) and bb.GetY()>mm(27.275) and bb.GetRight()<mm(131.15) and bb.GetBottom()<mm(126.825)
textobs={k:[] for k in ob}
offsets=[(0,0)]+sorted([(i*.25,j*.25) for i in range(-24,25) for j in range(-24,25) if i or j],key=lambda t:t[0]**2+t[1]**2)
for f,n in texts:
 print("Label",n.GetText(),flush=True)
 layer=n.GetLayer();old=p.VECTOR2I(n.GetPosition());found=False
 for dx,dy in offsets:
  n.SetPosition(old+p.VECTOR2I(mm(dx),mm(dy)));q=poly(n)
  if inside(q) and not any(coll(q,o) for o in ob[layer]+textobs[layer]):found=True;break
 if not found:n.SetPosition(old);raise RuntimeError('No label position: '+n.GetText())
 if dx or dy:logs.append(dict(text=n.GetText(),ref=f.GetReference() if f else '',dx=dx,dy=dy))
 textobs[layer].append(inflate(q,clear))
# Clip only the obstructed portions of footprint outlines, keeping all text.
prior={k:[] for k in ob}
for f,n in graphics:
 if not isinstance(n,p.PCB_SHAPE):continue
 layer=n.GetLayer();q=poly(n);original=q.CloneDropTriangulation();owner=f.GetReference() if f else 'board'
 blockers=ob[layer]+textobs[layer]+[x for name,x in prior[layer] if name!=owner]
 clipped=False
 for o in blockers:
  if coll(q,o):q.BooleanSubtract(o);clipped=True
 # Trim board edge violations too.
 boundary=p.SHAPE_POLY_SET();boundary.NewOutline()
 for x,y in [(31.60,27.275),(131.15,27.275),(131.15,126.825),(31.60,126.825)]:boundary.Append(mm(x),mm(y))
 if not inside(q):q.BooleanIntersection(boundary);clipped=True
 if clipped:
  logs.append(dict(graphic=n.m_Uuid.AsString(),ref=owner))
  if not q.OutlineCount():
   (f.Remove if f else b.Remove)(n);continue
  # New polygons use board coordinates; adding through footprint API converts them.
  new=p.PCB_SHAPE(f if f else b);new.SetLayer(layer);new.SetShape(p.SHAPE_T_POLY);new.SetFilled(True);new.SetWidth(0);new.SetPolyShape(q)
  (f.Add if f else b.Add)(new);(f.Remove if f else b.Remove)(n)
 prior[layer].append((owner,inflate(q,clear)))
p.SaveBoard('oneTesla.kicad_pcb',b)
Path('implementation/dfm-jlc-2026-10-18/silk-changes.json').write_text(json.dumps(logs,indent=2));print('Silk edits:',len(logs))
