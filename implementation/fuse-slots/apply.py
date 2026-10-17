from pathlib import Path
import sys,re,copy,uuid
sys.path.insert(0,str(Path('scripts').resolve()))
from sexpr import *
OLD='Fuseholder_Idall_AS-06_5x20mm_P20.20mm_Horizontal'
NEW='Fuseholder_Idall_AS-06_5x20mm_Slotted_P22.35mm'
DESC='AS-06 5x20; corpo26x9.6; slots metalizados4.4x1.8 ao longo do passo; centros22.35; faixa de montagem20.2 a24.5 com folga. Faixa de adaptacao, nao especificacao do fabricante.'
NOTES='Montagem tolerante: terminais acomodados em slots metalizados4.4x1.8mm, centros22.35mm. Acomodar passo20.2 a24.5mm com folga. 1 AC_L, 2 AC_L_FUSED. Fusivel4A/250VAC mantido. STEP apenas referencia visual.'
STATUS='Adaptacao de montagem AS-06: pad6.0x3.2, slot4.4x1.8, anel minimo0.7mm; centros22.35mm. Faixa20.2-24.5 nao e cota confirmada da peca; montagem com terminais inclinados.'
def U():return str(uuid.uuid4())
def change(f,board=False):
 f[1]=('oneTesla:' if board else '')+NEW
 child(f,'descr')[1]=DESC
 if child(f,'tags'):child(f,'tags')[1]='Idall AS-06 slotted plated 5x20 assembly tolerance'
 for name,val in [('Description',DESC),('Assembly_Notes',NOTES),('Footprint_Status',STATUS)]:
  n=prop(f,name)
  if n:n[2]=val
 for p in children(f,'pad'):
  assert p[1] in ['1','2'];child(p,'at')[1]=Atom('11.175' if p[1]=='1' else '-11.175')
  child(p,'size')[1:]=[Atom('6'),Atom('3.2')];child(p,'drill')[1:]=[Atom('oval'),Atom('4.4'),Atom('1.8')]
  if p[1]=='2':p[3]=Atom('oval')
 # Courtyard encloses copper pad ends; silk is open next to elongated pads.
 additions=[];remove=[]
 for n in children(f,'fp_rect'):
  layer=child(n,'layer')[1]
  if layer=='F.CrtYd':child(n,'start')[1]=Atom('-14.75');child(n,'end')[1]=Atom('14.75')
  if layer=='F.SilkS':
   remove.append(n)
   lines=[((-13.15,-4.95),(13.15,-4.95)),((-13.15,4.95),(13.15,4.95))]
   for x in [-13.15,13.15]:lines.extend([((x,-4.95),(x,-1.9)),((x,1.9),(x,4.95))])
   for a,b in lines:
    additions.append(parse(f'(fp_line (start {a[0]} {a[1]}) (end {b[0]} {b[1]}) (stroke (width 0.12) (type solid)) (layer "F.SilkS") (uuid "{U()}"))'))
 for n in remove:f.remove(n)
 f.extend(additions);return f
lib=Path('library/oneTesla.pretty')
fp=change(parse((lib/(OLD+'.kicad_mod')).read_text()));(lib/(NEW+'.kicad_mod')).write_text(dump(fp)+'\n')
# Replace only the placed footprint, keeping all other board items unchanged.
p=Path('oneTesla.kicad_pcb');s=p.read_text();start=s.index('(footprint "oneTesla:'+OLD+'"');depth=0
for t in re.finditer(r'\(|\)|"(?:\\.|[^"\\])*"|[^\s()]+',s[start:]):
 if t.group()=='(':depth+=1
 elif t.group()==')':
  depth-=1
  if depth==0:end=start+t.end();break
f=change(parse(s[start:end]),True);p.write_text(s[:start]+dump(f,1)+s[end:])
# Update the selected instance and cached default footprint association.
p=Path('oneTesla.kicad_sch');s=p.read_text();b=parse(s);f=next(n for n in children(b,'symbol') if prop(n,'Reference')[2]=='F1');uid=child(f,'uuid')[1]
prop(f,'Footprint')[2]='oneTesla:'+NEW
for name,val in [('Description',DESC),('Assembly_Notes',NOTES),('Footprint_Status',STATUS)]:prop(f,name)[2]=val
stack=[];found=[]
for t in re.finditer(r'\(|\)|"(?:\\.|[^"\\])*"|[^\s()]+',s):
 if t.group()=='(':stack.append(t.start())
 elif t.group()==')':
  a=stack.pop()
  if re.match(r'\(symbol\s',s[a:t.end()]):
   n=parse(s[a:t.end()]);u=child(n,'uuid')
   if u and u[1]==uid:found.append((a,t.end()))
assert len(found)==1;a,z=found[0];s=s[:a]+dump(f,1)+s[z:];s=s.replace('oneTesla:'+OLD,'oneTesla:'+NEW);p.write_text(s)
print('F1: slots 4.4x1.8 mm, pads 6x3.2 mm; pad centres at +/-11.175 mm. Nets, holes of other components and tracks unchanged.')
