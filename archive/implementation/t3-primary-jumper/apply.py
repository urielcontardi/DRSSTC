from pathlib import Path
import sys,copy,re,uuid
sys.path.insert(0,str(Path('scripts').resolve()))
from sexpr import *
def U():return str(uuid.uuid4())
def replace_uuid(s,changes):
 stack=[];spans=[]
 for t in re.finditer(r'\(|\)|"(?:\\.|[^"\\])*"|[^\s()]+',s):
  if t.group()=='(':stack.append(t.start())
  elif t.group()==')':
   a=stack.pop();chunk=s[a:t.end()]
   if re.match(r'\((?:symbol|wire|footprint|segment)\s',chunk):
    n=parse(chunk);u=child(n,'uuid')
    if u and u[1] in changes:spans.append((a,t.end(),changes[u[1]]))
 for a,z,n in sorted(spans,reverse=True):s=s[:a]+(dump(n,1) if n is not None else '')+s[z:]
 assert len(spans)==len(changes),(len(spans),len(changes))
 return s
schpath=Path('oneTesla.kicad_sch');s=schpath.read_text();sch=parse(s)
j=copy.deepcopy(next(x for x in children(sch,'symbol') if prop(x,'Reference')[2]=='J110'))
symuuid=U();child(j,'uuid')[1]=symuuid
oldat=list(map(float,child(j,'at')[1:3]));at=(303.53,97.79);child(j,'at')[1:3]=[Atom(str(v)) for v in at]
for p in children(j,'property'):
 xy=child(p,'at');xy[1]=Atom(str(round(float(xy[1])+at[0]-oldat[0],6)));xy[2]=Atom(str(round(float(xy[2])+at[1]-oldat[1],6)))
for p in children(j,'pin'):child(p,'uuid')[1]=U()
prop(j,'Reference')[2]='JCT';prop(j,'Value')[2]='FIO PELO T3';prop(j,'Footprint')[2]='oneTesla:CT_Primary_WireLink_P21.59mm'
prop(j,'Assembly_Notes')[2]='Obrigatorio: fio de potencia entre pads 1 e 2 atravessando uma vez o nucleo de T3. Sem trilha de cobre em paralelo. Sentido de fase a confirmar na montagem.'
prop(j,'Footprint_Status')[2]='Pads D4/furo2.2, P21.59, posicionados dos dois lados de T3; conferir montagem fisica e bitola do fio.'
project=child(child(j,'instances'),'project');path=child(project,'path');child(path,'reference')[1]='JCT'
wire=next(w for w in children(sch,'wire') if child(w,'uuid')[1]=='3abee602-7bbf-4220-8195-32823416e8e5');child(child(wire,'pts'),'xy')
children(child(wire,'pts'),'xy')[1][1:]=[Atom('298.45'),Atom('97.79')]
s=replace_uuid(s,{child(wire,'uuid')[1]:wire})
extra=dump(j,1)+'\n'+f'''(label "SW_CT" (at 308.61 97.79 90) (effects (font (size 1.0 1.0)) (justify left bottom)) (uuid "{U()}"))'''
s=s.rstrip();schpath.write_text(s[:-1]+'\n'+extra+'\n)\n')
# Library: separate solder pads, no copper bridge; assembly path belongs to F.Fab.
fpname='CT_Primary_WireLink_P21.59mm'
fp=f'''(footprint "{fpname}" (version 20260206) (generator "pcbnew") (layer "F.Cu")
 (descr "Fio de potencia obrigatorio pelo nucleo de T3; pads separados, sem cobre em paralelo; passo21.59 D4 furo2.2")
 (attr through_hole)
 (property "Reference" "REF**" (at 0 12 0) (layer "F.SilkS") (effects (font (size 1 1) (thickness 0.15))))
 (property "Value" "FIO PELO T3" (at 0 0 0) (layer "F.Fab") (effects (font (size 1 1) (thickness 0.15))))
 (fp_line (start -8.5 0) (end 8.5 0) (stroke (width 0.15) (type dash)) (layer "F.Fab"))
'''
for n,x in [(1,-10.795),(2,10.795)]:
 fp+=f'''(pad "{n}" thru_hole circle (at {x} 0) (size 4 4) (drill 2.2) (layers "*.Cu" "*.Mask") (remove_unused_layers no))
 (fp_circle (center {x} 0) (end {x+2.5} 0) (stroke (width 0.05) (type solid)) (fill none) (layer "F.CrtYd"))
'''
fp+=')\n';Path('library/oneTesla.pretty/'+fpname+'.kicad_mod').write_text(fp)
boardfp=parse(fp);boardfp[1]='oneTesla:'+fpname
boardfp.insert(3,[Atom('at'),Atom('58.75'),Atom('113.1')]);boardfp.insert(4,[Atom('uuid'),U()]);boardfp.append([Atom('path'),'/'+child(sch,'uuid')[1]+'/'+symuuid]);prop(boardfp,'Reference')[2]='JCT'
for n in boardfp:
 if isinstance(n,list) and n and n[0] in ['property','pad','fp_line','fp_circle']:n.append([Atom('uuid'),U()])
for p in children(boardfp,'pad'):
 p.append([Atom('net'),'/SW_NODE' if p[1]=='1' else '/SW_CT']);p.append([Atom('pinfunction'),'A' if p[1]=='1' else 'B']);p.append([Atom('pintype'),'passive'])
p=Path('oneTesla.kicad_pcb');s=p.read_text();b=parse(s);changes={}
for t in children(b,'segment'):
 u=child(t,'uuid')[1]
 if u in ['460115e0-703a-420a-97f3-0429c7a06468','a849c3ce-86a0-4510-a4cd-807ba130cb00']:changes[u]=None
 if u=='cefd661a-fd2d-4f25-936d-3af57a19e0c2':child(t,'end')[1:]=[Atom('50.455'),Atom('122.75')];changes[u]=t
for f in children(b,'footprint'):
 if prop(f,'Reference')[2]=='CPR1':
  p1=next(p for p in children(f,'pad') if p[1]=='1');child(p1,'net')[1]='/SW_CT';changes[child(f,'uuid')[1]]=f
s=replace_uuid(s,changes)
extra=dump(boardfp,1)+'\n'
paths=[('/SW_NODE',[(50.455,122.75),(50.455,115.6),(47.955,113.1)]),('/SW_CT',[(69.545,113.1),(69.69,113.245),(69.69,116.4)])]
for net,pts in paths:
 for a,z in zip(pts,pts[1:]):extra+=f'(segment (start {a[0]} {a[1]}) (end {z[0]} {z[1]}) (width 2.5) (layer "B.Cu") (net "{net}") (uuid "{U()}"))\n'
s=s.rstrip();Path('oneTesla.kicad_pcb').write_text(s[:-1]+'\n'+extra+')\n')
print('JCT representado no esquema e PCB. SW_NODE chega ao pad esquerdo; SW_CT sai do pad direito para CPR1. Sem cobre entre os pads.')
