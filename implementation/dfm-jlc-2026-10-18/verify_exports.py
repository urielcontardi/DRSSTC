"""Read the exported Gerber/Excellon text independently of pcbnew."""
import re,json
from pathlib import Path
root=Path('production/2026-10-18-dfm/gerbers');evidence=Path('implementation/dfm-jlc-2026-10-18')
expected={(round(v['x'],3),round(-v['y'],3)) for v in json.loads((evidence/'geometry-final.json').read_text())['vias']}
result={}
for name in ['oneTesla-F_Cu.gtl','oneTesla-B_Cu.gbl']:
 text=(root/name).read_text();aps={int(n):float(d) for n,d in re.findall(r'%ADD(\d+)C,([\d.]+)\*%',text)};active=None;found=set()
 for line in text.splitlines():
  m=re.fullmatch(r'D(\d+)\*',line)
  if m:active=int(m[1])
  m=re.fullmatch(r'X(-?\d+)Y(-?\d+)D03\*',line)
  if m and active in aps and aps[active]>=.7:
   found.add(tuple(round(int(v)/1e6,3) for v in m.groups()))
 assert expected<=found,(name,expected-found)
 result[name]={'via_flashes_checked':len(expected),'minimum_via_diameter_mm':.7}
text=(root/'oneTesla-PTH.drl').read_text();tools={int(n):float(d) for n,d in re.findall(r'T(\d+)C([\d.]+)',text)};active=None;holes=set()
for line in text.splitlines():
 m=re.fullmatch(r'T(\d+)',line)
 if m:active=int(m[1])
 m=re.fullmatch(r'X(-?[\d.]+)Y(-?[\d.]+)',line)
 if m and tools.get(active)==.3:holes.add(tuple(round(float(v),3) for v in m.groups()))
assert expected==holes,(expected-holes,holes-expected)
result['drill']={'via_drills_checked':len(holes),'diameter_mm':.3}
(evidence/'export-verification.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
