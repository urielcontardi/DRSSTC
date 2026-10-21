"""Supplement KiCad DRC with physical pad gaps and ink-to-hole checks.
Run with KiCad's bundled Python: validate_dfm.py BOARD OUTPUT_JSON.
"""
import sys,json,math
from pathlib import Path
import pcbnew as p
b=p.LoadBoard(sys.argv[1]);mm=p.FromMM;err=mm(.001);issues=[]
def coll(a,c,d=0):return a.BBox(d).Intersects(c.BBox()) and a.Collide(c,d)
def padpoly(a,layer):
 q=p.SHAPE_POLY_SET();a.TransformShapeToPolygon(q,layer,0,err,p.ERROR_OUTSIDE);return q
def ident(n):
 pos=n.GetPosition();return dict(uuid=n.m_Uuid.AsString(),x=p.ToMM(pos.x),y=p.ToMM(pos.y))
pads=[(f,a) for f in b.GetFootprints() for a in f.Pads()]
for i,(f,a) in enumerate(pads):
 if a.GetAttribute()==p.PAD_ATTRIB_NPTH:continue
 for g,c in pads[i+1:]:
  if c.GetAttribute()==p.PAD_ATTRIB_NPTH or (a.GetPosition()-c.GetPosition()).EuclideanNorm()>mm(12):continue
  layers=[l for l in [p.F_Cu,p.B_Cu] if a.IsOnLayer(l) and c.IsOnLayer(l)]
  if any(coll(padpoly(a,l),padpoly(c,l),mm(.199)) for l in layers):issues.append(dict(kind='physical_pad_gap',a=f.GetReference()+'.'+a.GetNumber(),b=g.GetReference()+'.'+c.GetNumber(),**ident(a)))
ob={p.F_SilkS:[],p.B_SilkS:[]}
for f,a in pads:
 for layer,mask,cu in [(p.F_SilkS,p.F_Mask,p.F_Cu),(p.B_SilkS,p.B_Mask,p.B_Cu)]:
  q=p.SHAPE_POLY_SET()
  if a.IsOnLayer(mask):a.TransformShapeToPolygon(q,cu,0,err,p.ERROR_OUTSIDE)
  elif a.GetDrillSize().x:a.TransformHoleToPolygon(q,0,err,p.ERROR_OUTSIDE)
  if q.OutlineCount():ob[layer].append((f.GetReference()+'.'+a.GetNumber(),q))
vias=[]
for a in b.GetTracks():
 if not isinstance(a,p.PCB_VIA):continue
 ring=(a.GetWidth(p.F_Cu)-a.GetDrillValue())/2;vias.append(dict(ring_mm=p.ToMM(ring),**ident(a)))
 if ring<mm(.2)-1:issues.append(dict(kind='via_annular_ring',**ident(a)))
 q=p.SHAPE_POLY_SET();q.NewOutline();pos=a.GetPosition();radius=a.GetDrillValue()/2
 for i in range(48):
  ang=2*math.pi*i/48;q.Append(round(pos.x+radius*math.cos(ang)),round(pos.y+radius*math.sin(ang)))
 for layer in ob:ob[layer].append(('via hole '+a.m_Uuid.AsString(),q))
ink=[(None,n) for n in b.GetDrawings()]
for f in b.GetFootprints():ink.extend((f,n) for n in list(f.GraphicalItems())+[f.Reference(),f.Value()])
for f,n in ink:
 if n.GetLayer() not in ob:continue
 q=p.SHAPE_POLY_SET()
 if isinstance(n,p.PCB_TEXT):
  if not n.IsVisible():continue
  n.TransformTextToPolySet(q,0,err,p.ERROR_OUTSIDE)
 elif isinstance(n,p.PCB_SHAPE):n.TransformShapeToPolygon(q,n.GetLayer(),0,err,p.ERROR_OUTSIDE)
 else:continue
 for name,o in ob[n.GetLayer()]:
  if coll(q,o,mm(.149)):issues.append(dict(kind='silk_pad_or_hole',ref=f.GetReference() if f else '',obstacle=name,**ident(n)))
result=dict(board=str(Path(sys.argv[1]).resolve()),vias=vias,issues=issues)
Path(sys.argv[2]).write_text(json.dumps(result,indent=2));print('Supplemental DFM:',len(issues),'issues;',len(vias),'vias checked')
sys.exit(bool(issues))
