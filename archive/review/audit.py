"""Read-only audit of source; output only under review. Uses repository sexpr reader."""
from pathlib import Path
import sys,json,csv,math,collections,xml.etree.ElementTree as ET,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from sexpr import parse,child,children,prop
OUT=ROOT/'review'; b=parse((ROOT/'oneTesla.kicad_pcb').read_text()); drc=json.loads((OUT/'evidence/drc.json').read_text())
def val(x,k,default=''):
 n=child(x,k);return n[1] if n and len(n)>1 else default
def pr(x,k):
 n=prop(x,k);return n[2] if n else ''
def wr(name,rows):
 if not rows:return
 with (OUT/name).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def padinfo(f):
 out=[]
 for p in children(f,'pad'):
  at=child(p,'at');size=child(p,'size');d=child(p,'drill');n=child(p,'net')
  out.append(dict(num=str(p[1]),tipo=str(p[2]),forma=str(p[3]),x=float(at[1]),y=float(at[2]),sx=float(size[1]),sy=float(size[2]),furo=' '.join(format(float(q),'.8g') if str(q).replace('.','',1).isdigit() else str(q) for q in d[1:]) if d else '',rede=str(n[-1]) if n else ''))
 return out
def layers(f):return collections.Counter(str(val(x,'layer')) for x in f if isinstance(x,list))
def nets(file):
 t=parse(file.read_text());out={}
 for n in children(child(t,'nets'),'net'):
  for p in children(n,'node'):out[(str(val(p,'ref')),str(val(p,'pin')))]=str(val(n,'name'))
 return out
expected=nets(OUT/'evidence/oneTesla.net');sch=parse((ROOT/'oneTesla.kicad_sch').read_text());syms={pr(s,'Reference'):s for s in children(sch,'symbol') if not pr(s,'Reference').startswith('#')}
rows=[];placed=[];matches=[];used=set();pts=[]
for i,f in enumerate(children(b,'footprint')):
 ref=pr(f,'Reference');key=ref or 'SEM_REF_'+str(i+1);uid=str(val(f,'uuid'));at=child(f,'at');a=float(at[3]) if len(at)>3 else 0;x,y=map(float,at[1:3]);pads=padinfo(f);used.add(str(f[1]));ll=layers(f)
 issues=[v for v in drc['violations']+drc['schematic_parity'] if any(str(z['uuid'])==uid for z in v['items']) or any(str(z['uuid']) in [str(val(p,'uuid')) for p in children(f,'pad')] for z in v['items'])]
 check=[]
 for p in pads:
  if p['num'] and (ref,p['num']) in expected and expected[(ref,p['num'])]!=p['rede']:check.append(p['num']+': '+p['rede']+' != '+expected[(ref,p['num'])])
  ang=math.radians(a);p['bx']=x+p['x']*math.cos(ang)+p['y']*math.sin(ang);p['by']=y-p['x']*math.sin(ang)+p['y']*math.cos(ang)
  pts.append(dict(ref=key,**p))
 source=ROOT/'library'/ (str(f[1]).split(':')[0]+'.pretty')/(str(f[1]).split(':')[-1]+'.kicad_mod')
 geom='biblioteca ausente'
 if source.exists():
  lp=padinfo(parse(source.read_text()));strip=lambda ps:sorted([json.dumps({k:v for k,v in p.items() if k not in ('rede','bx','by')},sort_keys=True) for p in ps]);geom='igual' if strip(lp)==strip(pads) else 'DIFERENTE (inspecionar geometria/rotação)'
 row=dict(referencia=key,valor=pr(f,'Value'),footprint=str(f[1]),x_mm=x,y_mm=y,rot_graus=a,pads=json.dumps(pads,ensure_ascii=False),passos_mm='; '.join(f"{u['num']}-{v['num']}:{math.hypot(u['x']-v['x'],u['y']-v['y']):.4f}" for u,v in zip(pads,pads[1:]) if u['num'] and v['num']),mapeamento='; '.join(check) or ('redes dos pads presentes conferem com netlist' if ref in syms else 'extra PCB; sem símbolo'),polaridade='Conferir pad1/marcação e datasheet; ver relatório por família',courtyard=str(ll.get('F.CrtYd',0))+' elementos; '+str(sum(v['type']=='courtyards_overlap' for v in issues))+' colisões DRC',serigrafia=str(sum(v['type'] in ('silk_overlap','silk_over_copper','silk_edge_clearance') for v in issues))+' ocorrências DRC associadas',geometria_biblioteca=geom,encaixe='PENDENTE peça exata/tolerâncias; ver achados',status_esquema=pr(syms.get(ref,[]),'Footprint_Status'),notas_esquema=pr(syms.get(ref,[]),'Assembly_Notes'),drc='; '.join(sorted(set(v['type'] for v in issues))),uuid=uid)
 rows.append(row);placed.append(dict(ref=key,footprint=str(f[1]),x=x,y=y,rot=a,pads=pads))
wr('cobertura-pcb.csv',rows);wr('pads.csv',pts)
librows=[]
for p in sorted((ROOT/'library').glob('*.pretty/*.kicad_mod')):
 f=parse(p.read_text());name=p.parent.stem+':'+p.stem;ll=layers(f);pp=padinfo(f)
 librows.append(dict(arquivo=str(p.relative_to(ROOT)),uso='PCB' if name in used else 'NÃO USADO no PCB atual',pads=json.dumps(pp,ensure_ascii=False),courtyard_elementos=ll.get('F.CrtYd',0),silk_elementos=ll.get('F.SilkS',0),fabricacao_elementos=ll.get('F.Fab',0),validacao='geometria inventariada; MPN/datasheet/encaixe não aprovado',descricao=val(f,'descr')))
wr('cobertura-bibliotecas.csv',librows)
inv=[]
for p in sorted(ROOT.rglob('*')):
 if p.is_file() and '.git' not in p.parts and 'review' not in p.parts:
  inv.append(dict(arquivo=str(p.relative_to(ROOT)),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
wr('inventario.csv',inv)
viol=[]
for cat in ['violations','unconnected_items','schematic_parity']:
 for v in drc[cat]:viol.append(dict(categoria=cat,tipo=v['type'],severidade=v['severity'],descricao=v['description'],itens=json.dumps(v['items'],ensure_ascii=False)))
wr('drc-itens.csv',viol)
comparisons={}
for p in (OUT/'evidence').glob('*.net'):
 nn=nets(p);diff=[dict(ref=k[0],pin=k[1],base=v,outro=nn.get(k,'AUSENTE')) for k,v in expected.items() if nn.get(k)!=v];comparisons[p.name]=dict(pinos=len(nn),diferencas=diff,extras=[list(k)+[v] for k,v in nn.items() if k not in expected])
(OUT/'evidence/netlist-differences.json').write_text(json.dumps(comparisons,indent=2))
eagle=ET.parse(ROOT/'misc/driver.brd').getroot();erows=[]
for e in eagle.findall('.//board/elements/element'):
 pkg=eagle.find('.//board/libraries/library[@name="'+e.attrib['library']+'"]/packages/package[@name="'+e.attrib['package']+'"]')
 erows.append(dict(referencia=e.attrib['name'],valor=e.attrib.get('value',''),library=e.attrib['library'],package=e.attrib['package'],x=e.attrib['x'],y=e.attrib['y'],rot=e.attrib.get('rot','R0'),pads=json.dumps([p.attrib for p in pkg if p.tag in ('pad','smd','hole')]),cobertura='geometria/pinagem inventariadas; original legado; não liberar fabricação; sem DRC Eagle'))
wr('cobertura-eagle.csv',erows)
summary=dict(arquivos=len(inv),footprints_pcb=len(rows),referencias_esquema=len(syms),footprints_biblioteca=len(librows),usados_biblioteca=sum(x['uso']=='PCB' for x in librows),eagle_elementos=len(erows),mapeamento_erros=[r['referencia'] for r in rows if '!='in r['mapeamento']],segmentos=len(children(b,'segment')),vias=len(children(b,'via')),zonas=len(children(b,'zone')),regras=json.loads((ROOT/'oneTesla.kicad_pro').read_text())['board']['design_settings'].get('rules'),netclasses=json.loads((ROOT/'oneTesla.kicad_pro').read_text()).get('net_settings'))
(OUT/'evidence/summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2));(OUT/'evidence/placed.json').write_text(json.dumps(placed,indent=2))
