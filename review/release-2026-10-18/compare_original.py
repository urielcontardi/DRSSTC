from pathlib import Path
import sys, json, xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts'))
from sexpr import parse,child,children
s=ET.parse(ROOT/'misc/driver.sch').getroot().find('.//schematic')
parts={p.get('name'):p for p in s.findall('./parts/part')}
libs={l.get('name'):l for l in s.findall('./libraries/library')}
rename={'U$7':'Q1','U$8':'Q2','U$2':'T3','U$6':'FB1','B1':'D4','CPRI':'CPR1'}
custom={'T1':{'1':'1','10':'2','3':'3','4':'4','7':'5','8':'6'},'U$2':{'P$1':'1','P$2':'2'},'U$6':{'OUT':'1','GND':'2','V+':'3'},'U$7':{'G':'1','C':'2','E':'3'},'U$8':{'G':'1','C':'2','E':'3'},'B1':{'+':'1','AC1':'2','AC2':'3','-':'4'}}
refs={'IC1','IC2','IC3','IC4','T1','U$2','U$6','U$7','U$8','B1','CPRI','C11','C12','R1','R2','R3','R4','R5','R6','D1','D2','Z1','Z2','C1','C2','C3','C4','C5','C6','C8','C9'}
custom.update({'D1':{'C':'1','A':'2'},'D2':{'C':'1','A':'2'},'C8':{'+':'1','-':'2'},'C9':{'+':'1','-':'2'},'C11':{'+':'1','-':'2'},'C12':{'+':'1','-':'2'},'C1':{'1':'2','2':'1'},'C4':{'1':'2','2':'1'},'R5':{'1':'2','2':'1'},'R6':{'1':'2','2':'1'},'Z1':{'C':'1','A':'2'},'Z2':{'C':'1','A':'2'},'CPRI':{'P$1':'1','P$2':'2'},'B1':{'+':'1','AC1':'3','AC2':'2','-':'4'}})
original={}
for n in s.findall('./sheets/sheet/nets/net'):
 out=original.setdefault(n.get('name'),set())
 for x in n.findall('.//pinref'):
  ref=x.get('part')
  if ref not in refs:continue
  p=parts[ref];ds=libs[p.get('library')].find('./devicesets/deviceset[@name="'+p.get('deviceset')+'"]')
  dev=ds.find('./devices/device[@name="'+p.get('device')+'"]')
  pin=next(c.get('pad') for c in dev.findall('./connects/connect') if c.get('gate')==x.get('gate') and c.get('pin')==x.get('pin'))
  pin=custom.get(ref,{}).get(pin,pin)
  # Passive two-terminal parts may be reversed without changing function.
  out.add((rename.get(ref,ref),pin))
current={}
for n in children(child(parse((ROOT/'review/release-2026-10-18/current.net').read_text()),'nets'),'net'):
 current[child(n,'name')[1]]={(child(x,'ref')[1],child(x,'pin')[1]) for x in children(n,'node')}
selected={rename.get(r,r) for r in refs}
result=[]
for net,pins in original.items():
 if not pins:continue
 hits=sorted(((len(pins&v),k,v) for k,v in current.items()),key=lambda x:x[0],reverse=True)
 score,name,v=hits[0]
 if not score:name,v='NO_MATCH',set()
 result.append({'original_net':net,'current_net':name,'original_pins':sorted(pins),'only_original':sorted(pins-v),'only_current_selected':sorted({p for p in v-pins if p[0] in selected})})
print(json.dumps(result,indent=2))
