from pathlib import Path
import sys,re,copy,uuid
sys.path.insert(0,str(Path('scripts').resolve()))
from sexpr import *
root=Path('implementation/fb1-silkscreen');p=Path('oneTesla.kicad_pcb');s=p.read_text();b=parse(s);old=parse((root/'before-oneTesla.kicad_pcb').read_text())
def ref(f):return prop(f,'Reference')[2]
def silk(n):return child(n,'layer')==['layer','F.SilkS']
def replace_nodes(s,tag,fn):
 spans=[];stack=[]
 for t in re.finditer(r'\(|\)|"(?:\\.|[^"\\])*"|[^\s()]+',s):
  if t.group()=='(':stack.append(t.start())
  elif t.group()==')':
   a=stack.pop()
   if re.match(r'\('+tag+r'\s',s[a:t.end()]):
    n=parse(s[a:t.end()]);result=fn(n)
    if result is not None:spans.append((a,t.end(),result))
 for a,z,new in sorted(spans,reverse=True):s=s[:a]+new+s[z:]
 return s
originals={ref(f):f for f in children(old,'footprint')}
updated={}
for f in children(b,'footprint'):
 r=ref(f)
 if r in ['Q1','Q2']:
  # Common breaks in the body outline clear adjacent TVS pads on either IGBT.
  lines=[]
  for n in children(originals[r],'fp_line'):
   if not silk(n):continue
   a=child(n,'start');z=child(n,'end')
   if float(a[1])==float(z[1]) and float(a[1]) in [-2.41,13.31] and float(a[2])==-2.89 and float(z[2])==-23.11:
    nn=copy.deepcopy(n);child(nn,'end')[2]=Atom('-4');lines.append(nn)
    nn=copy.deepcopy(n);child(nn,'start')[2]=Atom('-8');child(nn,'uuid')[1]=str(uuid.uuid4());lines.append(nn)
   else:lines.append(copy.deepcopy(n))
  f[:]=[n for n in f if not (isinstance(n,list) and n and n[0]=='fp_line' and silk(n))]+lines
  updated[r]=f
 if r=='FB1':
  child(prop(f,'Reference'),'at')[1:]=[Atom('11.5'),Atom('-2.5'),Atom('0')];updated[r]=f
s=replace_nodes(s,'footprint',lambda f:dump(updated[ref(f)],1) if ref(f) in updated else None)
remove={'bbc751e8-54b9-4c55-8d17-4a26d6531728','5f1656f8-1238-4c43-ba35-bdfe04c83b6e'}
s=replace_nodes(s,'(?:segment|via)',lambda n:'' if child(n,'uuid')[1] in remove else None)
p.write_text(s)
# Sync only silk graphics to library; keep canonical pad rotations and fabrication geometry.
newboard=parse(s);fmap={ref(f):f for f in children(newboard,'footprint')}
for filename,r,kinds in [('Q_TO3P_ImportedPads_ReviewPending.kicad_mod','Q1',{'fp_line'}),('HFBR-2521ETZ.kicad_mod','FB1',{'fp_line','fp_arc'}),('HLK-15M15BL.kicad_mod','PS1',{'fp_poly'})]:
 lib=Path('library/oneTesla.pretty')/filename;n=parse(lib.read_text());source=fmap[r]
 n[:]=[x for x in n if not(isinstance(x,list) and x and x[0] in kinds and silk(x))]+[copy.deepcopy(x) for x in source if isinstance(x,list) and x and x[0] in kinds and silk(x)]
 lib.write_text(dump(n)+'\n')
print('Common silk outlines synced; redundant +5V segment and single-layer via removed.')
