from pathlib import Path
import sys,csv
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from sexpr import *
root=Path(__file__).resolve().parents[1]
s=parse((root/'oneTesla.kicad_sch').read_text())
rows={r['referencia']:r for r in csv.DictReader((root/'review/cobertura-pcb.csv').open())}
for sym in children(s,'symbol'):
 ref=prop(sym,'Reference')[2]
 if ref in rows:
  st=prop(sym,'Footprint_Status')
  if st:st[2]='REVIEW: '+rows[ref]['encaixe']
  if ref=='FB1':st[2]='HFBR-2521ETZ: geometria Broadcom AV02-3283EN p4, pitch 2.54 mm; 1 OUT/2 GND/3 VCC/4 RL; retencoes 5/8 NC. Layout em revisao.'
(root/'oneTesla.kicad_sch').write_text(dump(s)+chr(10))
print('41 referências: estado de revisão explícito; nenhum fio, símbolo elétrico ou net alterado')
