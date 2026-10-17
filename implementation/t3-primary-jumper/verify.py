"""Check the CT primary path using KiCad-exported connectivity and DRC."""
from pathlib import Path
import json,sys,collections
sys.path.insert(0,str(Path('scripts').resolve()))
from sexpr import *
p=Path(__file__).resolve().parent

def nets(name):
 b=parse((p/name).read_text())
 return {child(n,'name')[1]:{(child(x,'ref')[1],child(x,'pin')[1]) for x in children(n,'node')} for n in children(child(b,'nets'),'net')}
a,b=nets('before.net'),nets('after.net')
assert b['/SW_CT']=={('CPR1','1'),('JCT1','2')}
assert b['/SW_NODE']==(a['/SW_NODE']-{('CPR1','1')})|{('JCT1','1')}
assert set(b)==set(a)|{'/SW_CT'}
for n in a:
 if n!='/SW_NODE':assert a[n]==b[n],n
pcb=parse(Path('oneTesla.kicad_pcb').read_text());fp={prop(f,'Reference')[2]:f for f in children(pcb,'footprint')}
assert child(fp['T3'],'at')[1:3]==child(fp['JCT1'],'at')[1:3]
assert child(next(x for x in children(fp['CPR1'],'pad') if x[1]=='1'),'net')[1]=='/SW_CT'
assert [(x[1],child(x,'net')[1]) for x in children(fp['JCT1'],'pad')]==[('1','/SW_NODE'),('2','/SW_CT')]
for ref in ['T3','P1','P2']:
 old=parse((p/'before-oneTesla.kicad_pcb').read_text());oldfp=next(f for f in children(old,'footprint') if prop(f,'Reference')[2]==ref)
 assert children(oldfp,'pad')==children(fp[ref],'pad')
d=json.loads((p/'drc-final.json').read_text())
assert not d['unconnected_items']
assert all(v['type'] not in ['clearance','creepage','shorting_items','lib_footprint_mismatch','silk_overlap','silk_over_copper','annular_width'] for v in d['violations'])
assert not any(any('JCT1' in i['description'] for i in v['items']) for v in d['schematic_parity'])
def erc(name):
 d=json.loads((p/name).read_text())
 return collections.Counter(v['type'] for s in d['sheets'] for v in s['violations'] if v['type'] not in ['lib_symbol_issues','footprint_link_issues'])
assert erc('erc-before.json')==erc('erc-after.json')
print('PASS: native netlists separated by JCT1; all other nets unchanged.')
print('PASS: T3 secondary and external primary terminals unchanged; jumper pads straddle T3.')
print('PASS: no missing connections, shorts or new electrical DRC/ERC defects; JCT1 matches schematic.')
print('Assembly still requires a real wire passing once through T3; CAD continuity does not verify magnetic phase.')
