from pathlib import Path
import sys,re,math,copy,uuid
sys.path.insert(0,str(Path('scripts').resolve()))
from sexpr import parse,children,child,prop,dump,Atom
P=Path('oneTesla.kicad_pcb');text=P.read_text();board=parse(text);edits={}
def put(node,new=None):edits[child(node,'uuid')[1]]=[node] if new is None else new

def world(f,p):
 a=child(f,'at');t=math.radians(float(a[3]) if len(a)>3 else 0);x,y=map(float,p)
 return (float(a[1])+x*math.cos(t)+y*math.sin(t),float(a[2])-x*math.sin(t)+y*math.cos(t))
def local(f,p):
 a=child(f,'at');t=math.radians(float(a[3]) if len(a)>3 else 0);x,y=p[0]-float(a[1]),p[1]-float(a[2])
 return (x*math.cos(t)-y*math.sin(t),x*math.sin(t)+y*math.cos(t))
def setxy(node,key,p):child(node,key)[1:]=[Atom(f'{v:.6f}'.rstrip('0').rstrip('.') if v else '0') for v in p]
def interp(a,b,t):return (a[0]+(b[0]-a[0])*t,a[1]+(b[1]-a[1])*t)
def cliprect(a,b):
 lo,hi=0.,1.
 for v,d,mn,mx in [(a[0],b[0]-a[0],31.575,131.175),(a[1],b[1]-a[1],27.25,126.85)]:
  if abs(d)<1e-10:
   if not mn<=v<=mx:return None
  else:
   u,w=sorted([(mn-v)/d,(mx-v)/d]);lo=max(lo,u);hi=min(hi,w)
 if hi-lo<1e-6:return None
 return interp(a,b,lo),interp(a,b,hi)
# Circular pads of Z1/Z2, expanded for 0.15 mm silk separation and 0.06 mm half stroke.
circles=[]
for f in children(board,'footprint'):
 if prop(f,'Reference')[2] in ['Z1','Z2']:
  for p in children(f,'pad'):circles.append((world(f,child(p,'at')[1:3]),float(child(p,'size')[1])/2+.25))
for f in children(board,'footprint'):
 ref=prop(f,'Reference')[2]
 if ref=='FB1':
  for p in children(f,'pad'):
   if p[1] in ['1','2','3','4']:child(p,'size')[1]=Atom('2');put(p)
  r=prop(f,'Reference');setxy(r,'at',(10,-5.5,90));put(r)
  for n in children(f,'fp_line'):
   if child(n,'layer')[1]!='F.SilkS':continue
   a=world(f,child(n,'start')[1:3]);b=world(f,child(n,'end')[1:3]);clipped=cliprect(a,b)
   if clipped is None:put(n,[])
   elif any(abs(v-w)>1e-6 for p,q in zip((a,b),clipped) for v,w in zip(p,q)):
    setxy(n,'start',local(f,clipped[0]));setxy(n,'end',local(f,clipped[1]));put(n)
  for n in children(f,'fp_arc'):
   if child(n,'layer')[1]=='F.SilkS' and all(world(f,child(n,k)[1:3])[0]<31.575 for k in ['start','mid','end']):put(n,[])
 if ref in ['Q1','Q2']:
  for n in children(f,'fp_line'):
   if child(n,'layer')[1]!='F.SilkS':continue
   a=world(f,child(n,'start')[1:3]);b=world(f,child(n,'end')[1:3]);dx,dy=b[0]-a[0],b[1]-a[1];aa=dx*dx+dy*dy;intervals=[(0.,1.)]
   for c,r in circles:
    ox,oy=a[0]-c[0],a[1]-c[1];bb=2*(ox*dx+oy*dy);cc=ox*ox+oy*oy-r*r;disc=bb*bb-4*aa*cc
    if disc<=0 or aa==0:continue
    u,v=sorted([(-bb-math.sqrt(disc))/(2*aa),(-bb+math.sqrt(disc))/(2*aa)])
    new=[]
    for lo,hi in intervals:
     if v<=lo or u>=hi:new.append((lo,hi));continue
     if u>lo:new.append((lo,min(u,hi)))
     if v<hi:new.append((max(v,lo),hi))
    intervals=new
   if intervals!=[(0.,1.)]:
    nodes=[]
    for j,(lo,hi) in enumerate(intervals):
     if (hi-lo)*math.sqrt(aa)<.15:continue
     nn=copy.deepcopy(n);setxy(nn,'start',local(f,interp(a,b,lo)));setxy(nn,'end',local(f,interp(a,b,hi)))
     if j:child(nn,'uuid')[1]=str(uuid.uuid4())
     nodes.append(nn)
    put(n,nodes)
 if ref in ['Z1','Z2']:
  for n in children(f,'fp_text'):
   if n[2]=='K' and child(n,'layer')[1]=='F.SilkS':setxy(n,'at',(-7.75,-3.25,90));put(n)
 if ref=='PS1':
  for n in children(f,'fp_poly'):
   if child(n,'layer')[1]=='F.SilkS':
    for xy in children(child(n,'pts'),'xy'):xy[1]=Atom(str(float(xy[1])+1.5))
    put(n)
 if ref=='REF**':
  n=prop(f,'Reference')
  if child(n,'hide') is None:n.append([Atom('hide'),Atom('yes')])
  put(n)
 if ref=='R6':
  n=prop(f,'Reference');setxy(n,'at',(0,3.0,0));put(n)
# Replace only individual nodes by UUID; leave every other byte untouched.
def apply(text,edits):
 stack=[];spans=[]
 for t in re.finditer(r'\(|\)|"(?:\\.|[^"\\])*"|[^\s()]+',text):
  v=t.group()
  if v=='(':stack.append(t.start())
  elif v==')':
   start=stack.pop();chunk=text[start:t.end()]
   if re.match(r'\((?:pad|fp_line|fp_arc|fp_text|fp_poly|property)\s',chunk):
    n=parse(chunk);u=child(n,'uuid')
    if u and u[1] in edits:spans.append((start,t.end(),edits[u[1]]))
 for a,b,nodes in sorted(spans,reverse=True):text=text[:a]+'\n\t\t'.join(dump(n,2) for n in nodes)+text[b:]
 assert len(spans)==len(edits),(len(spans),len(edits))
 return text
P.write_text(apply(text,edits));print('PCB nodes adjusted:',len(edits))
lib=Path('library/oneTesla.pretty/HFBR-2521ETZ.kicad_mod');s=lib.read_text();e={}
for p in children(parse(s),'pad'):
 if p[1] in ['1','2','3','4']:child(p,'size')[1]=Atom('2');e[child(p,'uuid')[1]]=[p]
lib.write_text(apply(s,e));print('Library pads adjusted:',len(e))
