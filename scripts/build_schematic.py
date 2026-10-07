"""Rebuild the oneTeslaTS main board from the supplied schematic and manual.
Run from the project root. Uses only Python's standard library and installed KiCad assets.
"""
from pathlib import Path
from copy import deepcopy
import math,uuid,csv
from sexpr import Atom as A, parse,dump,child,children,prop
ROOT=Path(__file__).resolve().parents[1]
SHARED=Path('/Applications/KiCad/KiCad.app/Contents/SharedSupport')
LIB=ROOT/'library/oneTesla.kicad_sym'
existing=parse(LIB.read_text())
orig={s[1]:s for s in children(existing,'symbol')}
uid=lambda:str(uuid.uuid4())
def E(k,*xs):return [A(k),*[A(str(x)) if not isinstance(x,(list,str)) else x for x in xs]]
def N(k,*xs):return [A(k),*[A(str(x)) for x in xs]]
def effects(size=1.27,justify=None):
 e=E('effects',E('font',N('size',size,size)))
 if justify:e.append(N('justify',*justify.split()))
 return e
def property_(key,value,x=0,y=0,hide=False,justify=None,size=1.27):
 p=E('property',key,value,N('at',x,y,0),effects(size,justify))
 if hide:p.append(N('hide','yes'))
 return p
cache={}
def standard(lib,name):
 if lib not in cache:
  cache[lib]={s[1]:s for s in children(parse((SHARED/'symbols'/(lib+'.kicad_sym')).read_text()),'symbol')}
 s=deepcopy(cache[lib][name]); ext=child(s,'extends')
 if ext:
  base=standard(lib,ext[1]);s.remove(ext)
  base[1]=name
  for u in children(base,'symbol'):u[1]=u[1].replace(ext[1]+'_',name+'_',1)
  for p in children(s,'property'):
   old=prop(base,p[1])
   if old:base.remove(old)
   base.append(p)
  s=base
 return s
symbols={};footprints={};statuses={}
def register(name,s,fp=None):
 s=deepcopy(s);old=s[1];s[1]=name
 prop(s,'Value')[2]=name
 for u in children(s,'symbol'):u[1]=u[1].replace(old+'_',name+'_',1)
 if fp is not None:prop(s,'Footprint')[2]=fp
 symbols[name]=s
 return name
def std(name,lib,orig,fp=None):return register(name,standard(lib,orig),fp)
def copyfp(lib,name,status='Pacote padronizado; conferir componente adquirido'):
 src=SHARED/'footprints'/(lib+'.pretty')/(name+'.kicad_mod')
 assert src.exists(),src
 (ROOT/'library/oneTesla.pretty'/src.name).write_text(src.read_text())
 out='oneTesla:'+name;statuses[out]=status
 return out
def customfp(name,pads,w,h,status,origin=(0,0)):
 f=E('footprint',name,N('version',20260206),E('generator','pcbnew'),E('layer','F.Cu'),E('descr',status),N('attr','through_hole'))
 f += [E('property','Reference','REF**',N('at',0,-h/2-2,0),E('layer','F.SilkS'),effects(1)),E('property','Value',name,N('at',0,h/2+2,0),E('layer','F.Fab'),effects(1))]
 for layer,add,width in [('F.SilkS',0,0.15),('F.Fab',0,0.1),('F.CrtYd',0.5,0.05)]:
  xmin,xmax,ymin,ymax=-w/2,w/2,-h/2,h/2
  if layer=='F.CrtYd':
   xmin=min(xmin,*[x-size/2 for _,x,y,drill,size in pads]);xmax=max(xmax,*[x+size/2 for _,x,y,drill,size in pads])
   ymin=min(ymin,*[y-size/2 for _,x,y,drill,size in pads]);ymax=max(ymax,*[y+size/2 for _,x,y,drill,size in pads])
  f.append(E('fp_rect',N('start',xmin-add,ymin-add),N('end',xmax+add,ymax+add),E('stroke',N('width',width),N('type','default')),E('fill',A('none')),E('layer',layer)))
 for num,x,y,drill,size in pads:
  f.append(E('pad',str(num),A('thru_hole'),A('rect' if str(num)=='1' else 'circle'),N('at',x,y),N('size',size,size),N('drill',drill),E('layers','*.Cu','*.Mask')))
 (ROOT/'library/oneTesla.pretty'/(name+'.kicad_mod')).write_text(dump(f)+'\n')
 statuses['oneTesla:'+name]=status
 return 'oneTesla:'+name
def box(name,reference,value,pins,fp='',description='',datasheet='',w=7.62,h=10.16):
 s=E('symbol',name,N('pin_names'),N('exclude_from_sim','no'),N('in_bom','yes'),N('on_board','yes'))
 s += [property_('Reference',reference,0,h+2.54),property_('Value',value,0,h+5.08),property_('Footprint',fp,hide=True),property_('Datasheet',datasheet,hide=True),property_('Description',description,hide=True)]
 u=E('symbol',name+'_0_1',E('rectangle',N('start',-w,h),N('end',w,-h),E('stroke',N('width',0.254),N('type','default')),E('fill',N('type','background'))))
 s.append(u);u=E('symbol',name+'_1_1')
 for num,pname,x,y,ang,ptype in pins:
  u.append(E('pin',A(ptype),A('line'),N('at',x,y,ang),N('length',2.54),E('name',pname,effects(1)),E('number',str(num),effects(1))))
 s.append(u);symbols[name]=s
 return name
DIP14=copyfp('Package_DIP','DIP-14_W7.62mm_Socket_LongPads','DIP-14, passo 2.54 mm, fileiras 7.62 mm: confirmado pelo layout e soquetes do manual')
DIP8=copyfp('Package_DIP','DIP-8_W7.62mm_Socket_LongPads','DIP-8, passo 2.54 mm, fileiras 7.62 mm: confirmado pelo layout e soquetes do manual')
register('74HCT14',orig['74HCT14'],DIP14);register('74HCT74',orig['74HCT74'],DIP14)
box('UCC37321','IC','UCC37321P',[
 (1,'VDD',-5.08,17.78,270,'power_in'),
 (8,'VDD',5.08,17.78,270,'power_in'),
 (2,'IN',-15.24,5.08,0,'input'),
 (3,'EN',-15.24,-5.08,0,'input'),
 (7,'OUT',15.24,2.54,180,'output'),
 (6,'OUT',15.24,-2.54,180,'passive'),
 (4,'AGND',-5.08,-17.78,90,'power_in'),
 (5,'PGND',5.08,-17.78,90,'power_in'),
],DIP8,datasheet=prop(orig['UCC37321'],'Datasheet')[2],w=10.16,h=12.7)
child(symbols['UCC37321'],'pin_names').append(N('offset',1.016))
child(prop(symbols['UCC37321'],'Reference'),'at')[:]=N('at',0,30.48,0)
child(prop(symbols['UCC37321'],'Value'),'at')[:]=N('at',0,27.94,0)
for u in children(symbols['UCC37321'],'symbol'):
 for p in children(u,'pin'):child(p,'length')[1]=A('5.08')
children(symbols['UCC37321'],'symbol')[0].append(E('text','INV',N('at',0,0,0),effects(1.27)))
# OUT6 and OUT7 are two legs of the same physical output stage, explicitly joined per TI.
# Model the extra leg as passive to retain output-short checking for separate drivers.
for u in children(symbols['UCC37321'],'symbol'):
 for p in children(u,'pin'):
  if child(p,'number')[1]=='6':p[1]=A('passive')
for name in ['74HCT14','74HCT74']:
 f=prop(symbols[name],'ki_fp_filters')
 if f:f[2]='DIP-14*'
prop(symbols['UCC37321'],'Description')[2]='UCC37321: OUT6/7 are duplicate legs of one output stage; connect externally, per TI SLUS504I.'
RF=copyfp('Resistor_THT','R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal')
RFH=copyfp('Resistor_THT','R_Axial_DIN0309_L9.0mm_D3.2mm_P10.16mm_Horizontal') if (SHARED/'footprints/Resistor_THT.pretty/R_Axial_DIN0309_L9.0mm_D3.2mm_P10.16mm_Horizontal.kicad_mod').exists() else copyfp('Resistor_THT','R_Axial_DIN0309_L9.0mm_D3.2mm_P12.70mm_Horizontal')
RFP=copyfp('Resistor_THT','R_Axial_Power_L25.0mm_W6.4mm_P30.48mm')
CF=copyfp('Capacitor_THT','C_Disc_D7.5mm_W2.5mm_P5.00mm')
CP100=copyfp('Capacitor_THT','CP_Radial_D8.0mm_P3.50mm')
CP680=copyfp('Capacitor_THT','CP_Radial_D12.5mm_P5.00mm')
CP1000=copyfp('Capacitor_THT','CP_Radial_D30.0mm_P10.00mm_SnapIn','Selecao D30/P10 snap-in; medir capacitores 1000uF adquiridos antes do PCB')
DF=copyfp('Diode_THT','D_DO-35_SOD27_P7.62mm_Horizontal','1N4148 DO-35 THT: confirmado; passo selecionado 7.62 mm')
TVSF=copyfp('Diode_THT','D_DO-201AD_P15.24mm_Horizontal')
QF=copyfp('Package_TO_SOT_THT','TO-3P-3_Horizontal_TabDown','FGA60N65SMD TO-3P-3: G1 C2 E3, passo 5.45 mm; conferir altura das pernas dobradas para dissipador')
REGF=copyfp('Package_TO_SOT_THT','TO-92_Inline','78L05/78L15 TO-92: OUT1 GND2 IN3; conferir fabricante e sufixo adquirido')
BRLOW=copyfp('Diode_THT','Diode_Bridge_DIP-4_W7.62mm_P5.08mm','DF005M DIP-4 proposto: +1 -2 AC3 AC4; confirmar codigo real da ponte pequena')
BRHI=copyfp('Diode_THT','Diode_Bridge_Vishay_KBU','KBU6G proposto: +1 AC2 AC3 -4, passo 5.08 mm; confirmar codigo real da ponte 6A')
FUSEF=copyfp('Fuse','Fuseholder_Clip-5x20mm_Littelfuse_111_Inline_P20.00x5.00mm_D1.05mm_Horizontal','Clipes para fusivel 5x20 mm propostos; confirmar modelo real e passo')
std('R','Device','R',RF);std('C','Device','C',CF);std('C_Polarized','Device','C_Polarized',CP100)
std('1N4148','Device','D',DF);std('1.5KE510CA','Device','D_TVS',TVSF)
std('FGA60N65SMD','Device','Q_NIGBT_GCE',QF);prop(symbols['FGA60N65SMD'],'Datasheet')[2]='https://www.onsemi.com/pdf/datasheet/fga60n65smd-d.pdf';std('78L05','Regulator_Linear','L78L05_TO92',REGF);std('78L15','Regulator_Linear','L78L15_TO92',REGF)
std('DF005M','Diode_Bridge','DF005M',BRLOW);std('KBU6G','Diode_Bridge','KBU6G',BRHI)
# FGA60N65SMD includes a co-packaged antiparallel diode (anode E, cathode C).
qbody=children(symbols['FGA60N65SMD'],'symbol')[0]
for pts,fill in [([(2.54,3.81),(6.35,3.81),(6.35,1.27)],'none'), ([(5.08,1.27),(7.62,1.27)],'none'), ([(5.08,-1.27),(7.62,-1.27),(6.35,1.27),(5.08,-1.27)],'none'), ([(6.35,-1.27),(6.35,-3.81),(2.54,-3.81)],'none')]:
 qbody.append(E('polyline',E('pts',*[N('xy',*pt) for pt in pts]),E('stroke',N('width',0.254),N('type','default')),E('fill',N('type',fill))))
prop(symbols['FGA60N65SMD'],'Description')[2]='FGA60N65SMD, TO-3P-3, G1 C2 E3, with co-packaged antiparallel diode (E anode, C cathode).'
std('Fuse','Device','Fuse',FUSEF)
JUMPF=customfp('J110_WireLink_P10.16mm',[(1,-5.08,0,1.5,4),(2,5.08,0,1.5,4)],14,6,'Jumper de fio P10.16 mm estimado do layout; confirmar dimensoes')
std('Jumper','Jumper','Jumper_2_Open',JUMPF)
GDTF=customfp('GDT_6Pin_CONFIRMAR',[(1,-4.445,-8.89,1.2,3),(2,4.445,8.89,1.2,3),(3,4.445,-8.89,1.2,3),(4,-4.445,0,1.2,3),(5,4.445,0,1.2,3),(6,-4.445,8.89,1.2,3)],13,22,'PROVISORIO: bobina GDT 6 pinos, grade 8.89 mm estimada do layout; confirmar medidas, pares e fase com a peca')
std('GDT','Device','Transformer_1P_2S',GDTF)
# Explicit required winding polarity: the two gate-to-emitter voltages must be opposite.
g=children(symbols['GDT'],'symbol')[0]
for x,y in [(-4.445,6.35),(4.445,11.43),(4.445,-11.43)]:
 g.append(E('circle',N('center',x,y),N('radius',0.508),E('stroke',N('width',0),N('type','default')),E('fill',N('type','outline'))))
prop(symbols['GDT'],'Description')[2]='GDT 1:1:1: dotted pins 1,3,6. Secondary gate/emitter voltages are opposite. Physical winding/pin numbering must be verified.'
LINEF=customfp('EI30_12VAC_CONFIRMAR',[(1,-10.16,-10.16,1,2.4),(2,10.16,-10.16,1,2.4),(3,5.08,10.16,1,2.4),(4,-5.08,10.16,1,2.4)],33,29,'PROVISORIO: EI30/12.5, grade inferida do layout; confirmar tensao primaria, medidas e pinagem')
std('LineTransformer','Device','Transformer_1P_1S',LINEF)
CTF=customfp('CT_1_300_P12.70mm_CONFIRMAR',[(1,0,-6.35,1,2.5),(2,0,6.35,1,2.5)],10,20,'PROVISORIO: CT 1:300 com 2 pinos do secundario, P12.70 estimado do layout; primario passa pelo nucleo fora dos pads; confirmar polaridade')
ct=box('CT_1_300','T','1:300',[(1,'S1',10.16,5.08,180,'passive'),(2,'S2',10.16,-5.08,180,'passive')],CTF,'Transformador de corrente 1:300; primario externo passa pelo nucleo',w=7.62,h=7.62)
symbols[ct].append(E('symbol',ct+'_0_0',E('text','CT / 1:300',N('at',0,0,0),effects(1))))
# Broadcom HFBR-2521ETZ. Copy the standard package but correct retention pin 6 to manufacturer pin 8.
hf=deepcopy(parse((SHARED/'footprints/OptoDevice.pretty/AGILENT_HFBR-252x.kicad_mod').read_text()))
hf[1]='HFBR-2521ETZ'
prop(hf,'Value')[2]='HFBR-2521ETZ'
for p in children(hf,'pad'):
 if p[1]=='6':p[1]='8'
(ROOT/'library/oneTesla.pretty/HFBR-2521ETZ.kicad_mod').write_text(dump(hf)+'\n')
HF='oneTesla:HFBR-2521ETZ';statuses[HF]='HFBR-2521ETZ pad 1 OUT,2 GND,3 VCC,4 RL,5/8 retencao NC; variante selecionada, confirmar receptor do kit'
box('HFBR-2521ETZ','FB','HFBR-2521ETZ',[(1,'OUT',12.7,2.54,180,'open_collector'),(2,'GND',0,-12.7,90,'power_in'),(3,'VCC',0,12.7,270,'power_in'),(4,'RL',-12.7,2.54,0,'passive'),(5,'NC',-12.7,-5.08,0,'no_connect'),(8,'NC',12.7,-5.08,180,'no_connect')],HF,'Receptor optico com pull-up interno de 1k entre RL e OUT; RL ligado a +5V','https://docs.broadcom.com/doc/AV02-3283EN',w=10.16,h=10.16)
IECF=customfp('IEC_C6_CONFIRMAR',[(1,-7.62,0,1.6,4),(2,7.62,0,1.6,4),(3,0,0,1.6,4)],27,18,'PROVISORIO: entrada IEC C6; geometria e numeracao propostas, confirmar fabricante, L/N/PE e fixacao')
box('IEC_C6','J','IEC C6',[(1,'L',10.16,5.08,180,'passive'),(2,'N',10.16,0,180,'passive'),(3,'PE',10.16,-5.08,180,'passive')],IECF,w=7.62,h=10.16)
TERMF=customfp('Primary_Terminal_M6_CONFIRMAR',[(1,0,0,6.5,10),(1,0,-7.62,2.5,5)],13,22,'PROVISORIO: terminal M6 e pad de solda no mesmo net; confirmar terminal mecanico, furo e afastamento')
std('Terminal','Connector','TestPoint',TERMF)
customfp('Chassis_PE_M3',[(1,0,0,3.2,7)],9,9,'Ponto PE/chassis M3 proposto; conferir fixacao e continuidade do chassis')
CPRF=customfp('CDE_940C30S68K_F_CONFIRMAR',[(1,-28.75,0,1.3,4),(2,28.75,0,1.3,4)],46,19,'PROVISORIO: CDE 940C30S68K-F 68nF/3000V, P57.5 selecionado pela familia/layout; confirmar desenho mecanico da peca')
std('ResonantCap','Device','C',CPRF)
for name in ['GND','+5V','+15V','PWR_FLAG']:std(name,'power',name)
# Preserve existing SOP and DIP custom assets; add consistent THT symbol defaults.
# Retain the separately added power components when rebuilding the initial library.
for name in ['HLK-15M15BL', 'MUR460C', 'SMBJ18A', '1N5819']:
 if name in orig:
  symbols[name] = deepcopy(orig[name])
newlib=E('kicad_symbol_lib',N('version',20231120),E('generator','kicad_symbol_editor'),E('generator_version','10.0'),*symbols.values())
LIB.write_text(dump(newlib)+'\n')
# Compact A3 sheet. Coordinates are millimeters; electrical endpoints are on a 1.27mm grid.
root_id='38e9e92e-0807-45b3-a56d-ef1f03ff1cd0'
sch=E('kicad_sch',N('version',20260306),E('generator','eeschema'),E('generator_version','10.0'),E('uuid',root_id),E('paper','A3'),E('title_block',E('title','oneTeslaTS - Placa principal / Main board'),E('date','2026-10-04'),E('rev','1.1'),E('company','Replica a partir das referencias em misc'),E('comment',A('1'),'THT / DIP | Logica, drivers, meia ponte e fonte'),E('comment',A('2'),'Footprints CONFIRMAR: validar medidas e pinagem antes do PCB')))
libs=E('lib_symbols')
for name,s in symbols.items():
 s=deepcopy(s);s[1]='oneTesla:'+name;libs.append(s)
sch.append(libs)
placed={};powern=0;expected={};records=[]
def pins_for(name,unit):
 out=[]
 for u in children(symbols[name],'symbol'):
  fields=u[1].rsplit('_',2)
  if len(fields)==3 and int(fields[1]) in [0,unit]:out+=children(u,'pin')
 return out
def put(name,ref,value,x,y,angle=0,unit=1,fp=None,dnp=False,note='',refpos=None,valpos=None,field_justify=None):
 x=round(x,4);y=round(y,4)
 fp=prop(symbols[name],'Footprint')[2] if fp is None else fp
 s=E('symbol',E('lib_id','oneTesla:'+name),N('at',x,y,angle),N('unit',unit),N('body_style',1),N('exclude_from_sim','no'),N('in_bom','no' if ref.startswith('#') else 'yes'),N('on_board','no' if ref.startswith('#') else 'yes'),N('dnp','yes' if dnp else 'no'),E('uuid',uid()))
 side_fields=name in ['R','C','C_Polarized','ResonantCap','1N4148','1.5KE510CA'] and not (angle in (90,270) and name in ['R','C','C_Polarized','ResonantCap'])
 if refpos is None:
  if side_fields:refpos=(x+5.08,y-2.54)
  else:refpos=(x,y-{'UCC37321':30.48,'HFBR-2521ETZ':25.4,'GDT':16.51,'CT_1_300':13.97,'LineTransformer':16.51,'IEC_C6':13.97}.get(name,8.89))
 if valpos is None:valpos=(refpos[0],refpos[1]+2.54)
 if ref.startswith('#'):refpos=(x,y);valpos=(x,y-2.54 if name.startswith('+') else y+2.54)
 if refpos[0]==x and refpos[1]<y-5.08:side_fields=False
 justify=field_justify or ('left' if side_fields else None)
 s += [property_('Reference',ref,*refpos,hide=ref.startswith('#'),justify=justify),property_('Value',value,*valpos,hide=ref.startswith('#') and name=='PWR_FLAG',justify=justify),property_('Footprint',fp,x,y,True),property_('Datasheet',prop(symbols[name],'Datasheet')[2],x,y,True)]
 if note:s.append(property_('Assembly_Notes',note,x,y,True))
 if fp:s.append(property_('Footprint_Status',statuses.get(fp,''),x,y,True))
 pinmap={}
 for p in pins_for(name,unit):
  num=child(p,'number')[1];px,py,pa=map(float,child(p,'at')[1:]);r=math.radians(angle)
  xx=x+px*math.cos(r)-py*math.sin(r);yy=y-px*math.sin(r)-py*math.cos(r)
  pinmap[num]=(round(xx,4),round(yy,4),(pa+angle)%360)
  s.append(E('pin',num,E('uuid',uid())))
 s.append(E('instances',E('project','oneTesla',E('path','/'+root_id,E('reference',ref),N('unit',unit)))))
 # KiCad stores field angles relative to the symbol rotation. Keep rotated passive fields horizontal.
 if angle in (90,270):
  for p in children(s,'property'):
   child(p,'at')[3]=A('90')
 sch.append(s);placed[(ref,unit)]={'s':s,'pins':pinmap,'name':name}
 if not ref.startswith('#') and not any(r['Reference']==ref for r in records):records.append({'Reference':ref,'Value':value,'Footprint':fp,'DNP':dnp,'Footprint_Status':statuses.get(fp,''),'Assembly_Notes':note})
 return ref,unit
def at(item,pin):return placed[item]['pins'][str(pin)][:2]
def wire(*points):
 for p,q in zip(points,points[1:]):
  if p==q:continue
  assert p[0]==q[0] or p[1]==q[1],(p,q)
  sch.append(E('wire',E('pts',N('xy',*p),N('xy',*q)),E('stroke',N('width',0),N('type','default')),E('uuid',uid())))
def junction(p):sch.append(E('junction',N('at',*p),N('diameter',0),N('color',0,0,0,0),E('uuid',uid())))
def label(net,p,ang=0,justify='left bottom'):sch.append(E('label',net,N('at',*p,ang),effects(1.27,justify),E('uuid',uid())))
def net(item,pin,name,length=5.08):
 p=at(item,pin);angle=placed[item]['pins'][str(pin)][2];r=math.radians(angle)
 q=(round(p[0]-length*math.cos(r),4),round(p[1]+length*math.sin(r),4))
 wire(p,q);label(name,q,0,'right bottom' if angle==0 else 'left bottom')
 if not item[0].startswith('#'):expected[(item[0],str(pin))]=name
 return q
def power(item,pin,name,length=5.08):
 global powern
 p=at(item,pin)
 q=(p[0],round(p[1]+(length if name=='GND' else -length),4))
 wire(p,q);powern+=1;put(name,'#PWR'+str(powern).zfill(3),name,*q)
 if not item[0].startswith('#'):expected[(item[0],str(pin))]=name
 return q
def nc(item,pin):
 sch.append(E('no_connect',N('at',*at(item,pin)),E('uuid',uid())))
 if not item[0].startswith('#'):expected[(item[0],str(pin))]=None

def text_(s,x,y,size=1.5,bold=False):
 ef=effects(size,'left top')
 if bold:child(ef,'font').append(N('bold','yes'))
 sch.append(E('text',s,N('at',x,y,0),ef,E('uuid',uid())))
def section(s,x,y,w):
 text_(s,x,y,2.2,True)
 sch.append(E('polyline',E('pts',N('xy',x,y+7.62),N('xy',x+w,y+7.62)),E('stroke',N('width',0.3),N('type','default')),E('fill',N('type','none')),E('uuid',uid())))
section('01  REALIMENTACAO E CONTROLE',17.78,19.05,137.16)
section('02  DRIVERS DE GATE',166.37,19.05,129.54)
section('03  MEIA PONTE',307.34,19.05,99.06)
section('04  ENTRADA AC E FONTE',17.78,183,218.44)
section('05  PORTAS LIVRES',245.11,190.5,161.29)
# Feedback and optical control.
t3=put('CT_1_300','T3','1:300',24.13,55.88,note='Primario: fio do circuito ressonante atravessa o nucleo. Verificar sentido para realimentacao positiva.')
r1=put('R','R1','1k 5W',46.99,50.8,90,fp=RFP)
a=put('74HCT14','IC1','74HCT14',76.2,50.8,unit=1)
b=put('74HCT14','IC1','74HCT14',101.6,50.8,unit=2)
wire(at(t3,1),at(r1,1));power(t3,2,'GND')
wire(at(r1,2),(60.96,50.8),at(a,1));wire(at(a,2),at(b,3));junction((60.96,50.8))
d2=put('1N4148','D2','1N4148',60.96,38.1,270)
d1=put('1N4148','D1','1N4148',60.96,64.77,270)
wire(at(d2,2),(60.96,50.8));wire((60.96,50.8),at(d1,1));power(d2,1,'+5V',3.81);power(d1,2,'GND',1.27)
label('CT_SIGNAL',(60.96,57.15))
ff=put('74HCT74','IC2','74HCT74',137.16,50.8,unit=1,refpos=(148.59,35.56),valpos=(148.59,38.1))
wire(at(b,4),at(ff,3));label('FEEDBACK',(110.49,50.8))
power(ff,2,'+5V',7.62);power(ff,4,'+5V',7.62);net(ff,1,'RESET_MIX');nc(ff,5);net(ff,6,'DRIVE_ENABLE')
fb=put('HFBR-2521ETZ','FB1','HFBR-2521ETZ',27.94,102.87)
power(fb,3,'+5V');power(fb,4,'+5V');power(fb,2,'GND');nc(fb,5);nc(fb,8)
r2=put('R','R2','1k',62.23,100.33,90)
wire(at(fb,1),at(r2,1));label('OPTICAL_OUT',(40.64,100.33))
r3=put('R','R3','10k',62.23,85.09,90);net(r3,1,'CT_SIGNAL')
u=put('74HCT14','IC1','74HCT14',104.14,100.33,unit=6)
wire(at(r2,2),(78.74,100.33),at(u,13));wire(at(r3,2),(78.74,85.09),(78.74,100.33));junction((78.74,100.33));label('RESET_MIX',(78.74,85.09));nc(u,12)
c1=put('C','C1','1u',44.45,119.38);power(c1,1,'+5V');power(c1,2,'GND')
for ref,name,unit,x,y,cpref,cx in [('IC1','74HCT14',7,76.2,138.43,'C2',88.9),('IC2','74HCT74',3,121.92,138.43,'C3',137.16)]:
 u=put(name,ref,name,x,y,unit=unit,refpos=(x,113.03),valpos=(x,115.57));power(u,14,'+5V');power(u,7,'GND')
 c=put('C',cpref,'1u',cx,y);power(c,1,'+5V');power(c,2,'GND')
text_('T3: o fio do primario atravessa o nucleo.',17.78,166.37,1.27)
# Gate drivers; separate input/output/rail groups.
inv=put('74HCT14','IC1','74HCT14',184.15,40.64,unit=3);net(inv,5,'FEEDBACK');net(inv,6,'FEEDBACK_INV')
u3=put('UCC37321','IC3','UCC37321P',203.2,76.2)
u4=put('UCC37321','IC4','UCC37321P',203.2,137.16)
for u,signal in [(u3,'FEEDBACK_INV'),(u4,'FEEDBACK')]:
 net(u,2,signal);net(u,3,'DRIVE_ENABLE')
 for a,b,rail,direction in [(1,8,'+15V',-1),(4,5,'GND',1)]:
  pa,pb=at(u,a),at(u,b);y=round(pa[1]+direction*5.08,4);x=round((pa[0]+pb[0])/2,4)
  wire(pa,(pa[0],y),(x,y),(pb[0],y),pb);junction((x,y))
  powern+=1;put(rail,'#PWR'+str(powern).zfill(3),rail,x,y)
 p6,p7=at(u,6),at(u,7);x=round(p6[0]+5.08,4)
 wire(p7,(x,p7[1]),(x,p6[1]),p6);junction((x,p7[1]))
r4=put('R','R4','3R3',241.3,73.66,90)
c4=put('C','C4','1u',241.3,134.62,90)
wire((223.52,73.66),at(r4,1));wire((223.52,134.62),at(c4,1))
t1=put('GDT','T1','1:1:1',274.32,101.6,note='Pontos em 1/3/6 indicam a fase eletrica exigida (gates opostos); validar bobinas, numeros fisicos e fase da peca.')
wire(at(r4,2),(251.46,73.66),(251.46,96.52),at(t1,1));wire(at(c4,2),(251.46,134.62),(251.46,106.68),at(t1,2))
for pin,n in [(3,'GATE_H'),(4,'SW_NODE'),(5,'GATE_L'),(6,'DC_MINUS')]:net(t1,pin,n)
# Local decoupling banks for IC3 and IC4, shared short rails.
for ceramic,electrolytic,y in [('C5','C8',45.72),('C6','C7',162.56)]:
 ca=put('C',ceramic,'1u',241.3,y)
 cb=put('C_Polarized',electrolytic,'100u 25V',264.16,y)
 for pin,rail,ry in [(1,'+15V',round(y-8.89,4)),(2,'GND',round(y+8.89,4))]:
  pa,pb=at(ca,pin),at(cb,pin);mid=(252.73,ry)
  wire(pa,(pa[0],ry),mid,(pb[0],ry),pb);junction(mid)
  powern+=1;put(rail,'#PWR'+str(powern).zfill(3),rail,*mid)
# Half bridge and split DC bus.
q1=put('FGA60N65SMD','Q1','FGA60N65SMD',322.58,55.88,refpos=(334.01,46.99),valpos=(334.01,49.53),field_justify='left')
q2=put('FGA60N65SMD','Q2','FGA60N65SMD',322.58,101.6,refpos=(334.01,92.71),valpos=(334.01,95.25),field_justify='left')
net(q1,1,'GATE_H');net(q2,1,'GATE_L')
wire(at(q1,3),(325.12,78.74),at(q2,2));junction((325.12,78.74));label('SW_NODE',(325.12,78.74))
z1=put('1.5KE510CA','Z1','1.5KE510CA',350.52,55.88,270,dnp=True,refpos=(346.71,53.34),valpos=(346.71,55.88),field_justify='right',note='Opcional / DNP, como informado no manual, etapa 6. Nao incluido no kit.')
z2=put('1.5KE510CA','Z2','1.5KE510CA',350.52,101.6,270,dnp=True,refpos=(346.71,99.06),valpos=(346.71,101.6),field_justify='right',note='Opcional / DNP, como informado no manual, etapa 6. Nao incluido no kit.')
c12=put('C_Polarized','C12','1000u 200V',363.22,55.88,fp=CP1000)
c11=put('C_Polarized','C11','1000u 200V',363.22,101.6,fp=CP1000)
r5=put('R','R5','100k 0.5W',394.97,55.88,fp=RFH,refpos=(394.97,46.99),valpos=(394.97,49.53))
r6=put('R','R6','100k 0.5W',394.97,101.6,fp=RFH,refpos=(394.97,92.71),valpos=(394.97,95.25))
wire(at(q1,2),(325.12,40.64),(350.52,40.64),(363.22,40.64),(394.97,40.64))
for u in [z1,c12,r5]:wire(at(u,1),(at(u,1)[0],40.64))
junction((350.52,40.64));junction((363.22,40.64));label('DC_PLUS',(325.12,40.64))
wire(at(c12,2),(363.22,78.74),at(c11,1));wire(at(r5,2),(394.97,78.74),at(r6,1));wire((363.22,78.74),(394.97,78.74))
junction((363.22,78.74));junction((394.97,78.74));label('DC_MID',(374.65,78.74))
wire(at(q2,3),(325.12,120.65),(350.52,120.65),(363.22,120.65),(394.97,120.65))
for u in [z2,c11,r6]:wire(at(u,2),(at(u,2)[0],120.65))
junction((350.52,120.65));junction((363.22,120.65));label('DC_MINUS',(325.12,120.65))
wire(at(z1,2),(350.52,71.12),(325.12,71.12));junction((325.12,71.12))
wire(at(z2,1),(350.52,86.36),(325.12,86.36));junction((325.12,86.36))
cpr=put('ResonantCap','CPR1','68n 3kV',340.36,78.74,90,refpos=(340.36,65.405),valpos=(340.36,67.945),note='CDE 940C30S68K-F, 0.068uF/3000V, conforme layout. Confirmar mecanica.')
wire((325.12,78.74),at(cpr,1));net(cpr,2,'PRIMARY_CAP')
p1=put('Terminal','P1','PRIMARIO A',340.36,139.7);net(p1,1,'PRIMARY_CAP')
p2=put('Terminal','P2','PRIMARIO B',386.08,139.7);net(p2,1,'DC_MID')
text_('Primario externo entre P1 e P2.\nZ1/Z2: TVS opcionais (DNP).',310,163.83,1.27)
# AC entry and isolated supply.
jac=put('IEC_C6','J1','IEC C6',25.4,209.55)
f1=put('Fuse','F1','4A/250VAC',58.42,204.47,90,note='Lista do kit: 4A. Serigrafia antiga menciona 10A; nao assumir 10A como valor do kit.')
wire(at(jac,1),at(f1,1));label('AC_L',(40.64,204.47));net(f1,2,'AC_L_FUSED')
net(jac,2,'AC_N');net(jac,3,'PE')
pe=put('Terminal','J2','PE/CHASSIS',58.42,222.25,fp='oneTesla:Chassis_PE_M3',note='Ponto explicito de ligacao PE ao chassis; inferido da trilha de terra e fixacao do layout.');net(pe,1,'PE')
d4=put('KBU6G','D4','KBU6G',111.76,208.28,90,refpos=(142.24,198.12),valpos=(142.24,200.66),note='Familia KBU selecionada pela ponte linear do layout; confirmar codigo da peca.')
for pin,n in [(1,'DC_PLUS'),(2,'AC_L_FUSED'),(3,'AC_N'),(4,'DC_MINUS')]:net(d4,pin,n)
j110=put('Jumper','J110','Jumper 110V',177.8,204.47,note='Liga AC_N ao ponto medio dos capacitores para dobrador em 110V. Manter aberto para 220V.')
net(j110,1,'AC_N');net(j110,2,'DC_MID')
text_('J110: fechado em 110V; aberto em 220V.',124.46,222.25,1.27)
t2=put('LineTransformer','T2','12VAC 1.2VA',30.48,251.46,note='Layout informa 12VAC/1.2VA. Primario 110 ou 220VAC conforme versao; confirmar regulacao para rail 15V.')
net(t2,1,'AC_L');net(t2,2,'AC_N');net(t2,4,'AUX_AC1');net(t2,3,'AUX_AC2')
d3=put('DF005M','D3','DF005M',78.74,251.46,refpos=(96.52,245.11),valpos=(96.52,247.65),note='Ponte pequena DIP-4 selecionada. Confirmar codigo e pinagem da peca.')
for pin,n in [(1,'RAW_DC'),(2,'GND'),(3,'AUX_AC2'),(4,'AUX_AC1')]:net(d3,pin,n)
c10=put('C_Polarized','C10','680u 35V',109.22,264.16,fp=CP680);net(c10,1,'RAW_DC');power(c10,2,'GND')
ic5=put('78L15','IC5','78L15',142.24,251.46);net(ic5,3,'RAW_DC');power(ic5,2,'GND');net(ic5,1,'+15V')
ic6=put('78L05','IC6','78L05',193.04,251.46);net(ic6,3,'RAW_DC');power(ic6,2,'GND');net(ic6,1,'+5V')
c9=put('C_Polarized','C9','100u 10V',215.9,264.16,fp=CP100);power(c9,1,'+5V');power(c9,2,'GND')
for name,x in [('RAW_DC',142.24),('GND',193.04)]:
 fl=put('PWR_FLAG','#FLG'+str(1 if name=='RAW_DC' else 2).zfill(2),'PWR_FLAG',x,276.86);net(fl,1,name)
# Defined levels on every unused input, explicit NC outputs.
for unit,x,inp,out in [(4,251.46,9,8),(5,289.56,11,10)]:
 u=put('74HCT14','IC1','74HCT14',x,213.36,unit=unit);net(u,inp,'GND');nc(u,out)
f2=put('74HCT74','IC2','74HCT74',260.35,251.46,unit=2,refpos=(270.51,240.03),valpos=(270.51,242.57))
power(f2,10,'+5V',7.62);net(f2,13,'+5V')
for p in [11,12]:net(f2,p,'GND')
for p in [8,9]:nc(f2,p)
sch.append(E('sheet_instances',E('path','/',E('page','1'))));sch.append(N('embedded_fonts','no'))
(ROOT/'oneTesla.kicad_sch').write_text(dump(sch)+'\n')
with (ROOT/'output/components.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(records[0]));w.writeheader();w.writerows(records)
print('Generated',len(records),'physical component references,',len(placed),'symbol units; all footprints local.')
