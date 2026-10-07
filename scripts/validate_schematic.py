"""Validate KiCad's exported connectivity against the reference circuit and pad numbers.
Run after `kicad-cli sch export netlist oneTesla.kicad_sch -o output/oneTesla.net`.
"""
from pathlib import Path
from collections import defaultdict
from sexpr import parse,child,children,prop
import json
ROOT=Path(__file__).resolve().parents[1]
netlist=parse((ROOT/'output/oneTesla.net').read_text())
nets={};by_pin={}
for n in children(child(netlist,'nets'),'net'):
 name=child(n,'name')[1].removeprefix('/')
 members={(child(x,'ref')[1],child(x,'pin')[1]) for x in children(n,'node')}
 nets[name]=members
 for p in members:by_pin[p]=name
# Explicit reference topology, independent of the placement/generator's helpers.
# Aux supply is the HLK module (PS1) since the T2/D3/IC5 removal; several logic
# nets are anonymous in the current sheet and are keyed by their Net-(...) name.
reference={
 'Net-(D1-K)':'D1:1 D2:2 IC1:1 R1:2 R3:1',
 'Net-(IC2A-C)':'IC1:4 IC1:5 IC2:3 IC4:2',
 'Net-(IC3-IN)':'IC1:6 IC3:2',
 'Net-(IC1-Pad13)':'IC1:13 R2:2 R3:2',
 'DRIVE_ENABLE':'IC2:6 IC3:3 IC4:3',
 'OPTICAL_OUT':'FB1:1 R2:1',
 'GATE_H':'Q1:1 T1:3',
 'GATE_L':'Q2:1 T1:5',
 'SW_NODE':'CPR1:1 Q1:3 Q2:2 T1:4 Z1:2 Z2:1',
 'DC_PLUS':'C12:1 D4:1 Q1:2 R5:1 Z1:1',
 'DC_MINUS':'C11:2 D4:4 Q2:3 R6:2 T1:6 Z2:2',
 'DC_MID':'C11:1 C12:2 J110:2 P2:1 R5:2 R6:1',
 'Net-(CPR1-Pad2)':'CPR1:2 P1:1',
 'AC_L':'F1:1 J1:1',
 'AC_L_FUSED':'D4:2 F1:2 PS1:1',
 'AC_N':'D4:3 J1:2 J110:1 PS1:2',
 'PE':'J1:3 J2:1',
 '+15V':'C5:1 C6:1 C8:1 C10:1 C13:1 IC3:1 IC3:8 IC4:1 IC4:8 IC6:3 PS1:4',
 '+5V':'C1:1 C2:1 C3:1 C9:1 D2:1 FB1:3 FB1:4 IC1:14 IC2:2 IC2:4 IC2:10 IC2:13 IC2:14 IC6:1',
 'GND':'C1:2 C2:2 C3:2 C5:2 C6:2 C8:2 C9:2 C10:2 C13:2 D1:2 FB1:2 IC1:7 IC1:9 IC1:11 IC2:7 IC2:11 IC2:12 IC3:4 IC3:5 IC4:4 IC4:5 IC6:2 PS1:3 T3:2',
}
for name,s in reference.items():
 want={tuple(x.split(':')) for x in s.split()}
 assert nets.get(name)==want,(name,'missing',want-nets.get(name,set()),'extra',nets.get(name,set())-want)
for group in ['T3:1 R1:1','IC1:2 IC1:3','IC3:6 IC3:7 R4:1','IC4:6 IC4:7 C4:1','R4:2 T1:1','C4:2 T1:2','IC1:12 IC2:1']:
 members={tuple(p.split(':')) for p in group.split()}
 n=by_pin[next(iter(members))];assert nets[n]==members,(group,nets[n])
for p in ['IC1:8','IC1:10','IC2:5','IC2:8','IC2:9','FB1:5','FB1:8']:
 t=tuple(p.split(':'));assert by_pin[t].startswith('unconnected-'),p
assert by_pin['IC3','7']!=by_pin['IC4','7']
assert len({by_pin['Q2','3'],by_pin['IC3','4'],by_pin['J1','3']})==3
sch=parse((ROOT/'oneTesla.kicad_sch').read_text());sympins=defaultdict(set);fpmap={}
embedded={s[1]:s for s in children(child(sch,'lib_symbols'),'symbol')}
for s in children(sch,'symbol'):
 ref=prop(s,'Reference')[2]
 if ref.startswith('#'):continue
 unit=int(child(s,'unit')[1]);lib=embedded[child(s,'lib_id')[1]]
 for u in children(lib,'symbol'):
  suffix=u[1].rsplit('_',2)
  if len(suffix)==3 and int(suffix[1]) in [0,unit]:
   sympins[ref]|={child(p,'number')[1] for p in children(u,'pin')}
 fpmap[ref]=prop(s,'Footprint')[2]
for ref,fp in fpmap.items():
 assert fp.startswith('oneTesla:'),(ref,fp)
 p=ROOT/'library/oneTesla.pretty'/(fp.split(':')[1]+'.kicad_mod')
 assert p.exists(),p
 pads={x[1] for x in children(parse(p.read_text()),'pad') if x[1]}
 want=sympins[ref]
 if ref=='FB1':want={x for x in want if x not in ('5','8')}  # retencoes 5/8 viraram furos NPTH
 assert pads==want,(ref,fp,'pads',pads,'pins',want)
assert len(fpmap)==41,len(fpmap)
assert sympins['IC1']=={str(n) for n in range(1,15)}
assert sympins['IC2']=={str(n) for n in range(1,15)}
assert sympins['IC3']=={str(n) for n in range(1,9)}
assert sympins['IC4']=={str(n) for n in range(1,9)}
r=json.loads((ROOT/'output/erc.json').read_text())
v=[v for s in r['sheets'] for v in s['violations']]
# Expected: PS1 (HLK module) AC inputs are power_input pins with no power_output
# driver on the mains nets — inherent to the module swap, documented in the README.
assert all(x['type']=='power_pin_not_driven' and 'PS1' in x['items'][0]['description'] for x in v),v
assert len(v)==2,v
result=f'PASS: {len(reference)} reference nets and 7 direct connections.\nPASS: all unused outputs explicitly NC; isolated domains remain separate.\nPASS: {len(fpmap)} physical references with existing local footprints; symbol pins match every pad.\nPASS: all 14/14/8/8 IC pins represented.\nPASS: KiCad {r["kicad_version"]} ERC: only the 2 expected PS1 power_pin_not_driven notes.\nFootprint dimensions marked CONFIRMAR/PROVISORIO still require physical verification.\n'
(ROOT/'output/validation.txt').write_text(result);print(result)
