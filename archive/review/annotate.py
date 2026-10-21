from pathlib import Path
import csv
p=Path(__file__).resolve().parent
rows=list(csv.DictReader((p/'cobertura-pcb.csv').open()))
notes={}
def add(refs,pol,fit):
 for r in refs.split():notes[r]=(pol,fit)
add('FB1','1 OUT, 2 GND, 3 VCC, 4 RL coerentes eletricamente; retenções 5/8 NC','REPROVADO HFBR-2521ETZ: pitch 1.905 versus 2.54 mm datasheet; ordem espacial 3-1-2-4 adaptada de IFD95; F01')
add('R1','Não polarizado','REPROVADO envelope: corpo declarado 25 mm, furos distam 22.86 mm; silk/fab deslocados 15.24 mm; F02')
add('R5 R6','Não polarizado','Pendente MPN 0.5 W: pitch real 10.16, nome 12.70; fab/silk não recentrados; F02')
add('R2 R3 R4','Não polarizado','DIN0207 P7.62 coerente genericamente; conferir potência/tolerância/corpo MPN; R4 amortecimento GDT depende de ensaio')
add('C11 C12','Pad1 positivo confere com netlist; serigrafia deslocada 5 mm','REPROVADO envelope D30: centros distam 26.035 mm, sobreposição 3.965 mm; F03. Pitch 10.16, MPN desconhecido')
add('C8 C9 C13','Pad1 positivo confere; corpo/silk deslocados em relação ao par de pads','Pendente MPN: pitch real 2.54 versus nome 3.50; F02. C9 em +5 V; C8/C13 em +15 V')
add('C10','Pad1 positivo +15 V; valor 680u 35V na fonte, fab mantém texto antigo 100u 10V','Pendente MPN: pitch real 3.556 versus nome 5; corpo/silk deslocados 2.5 mm; F02')
add('C1 C2 C3 C4 C5 C6','Não polarizados no símbolo','Disco P5, furos/pads inventariados; dielétrico/tensão/ESL/MPN desconhecidos; C4 deve suportar corrente do GDT')
add('CPR1','Não polarizado','CDE 940C30S68K-F: corpo 46x19 e fio 1 mm conferem catálogo; P58.42 é dobra escolhida, não pitch de fábrica; furo1.4; ensaio RMS/dVdt obrigatório')
add('IC1 IC2','DIP pad1 retangular e numeração padrão; alimentação/netlist conferem','DIP14 P2.54 W7.62; furo0.8128 pad1.6; MPN/sufixo e soquete exatos desconhecidos; LongPads no nome não corresponde ao pad real')
add('IC3 IC4','UCC37321: VDD1/8, IN2, EN3, GND4/5, OUT6/7 conferem datasheet e netlist','PDIP8 P2.54 W7.62 coerente; soquete exato pendente; TI recomenda desacoplamento em ambos pares VDD/GND, não comprovado nesta geometria')
add('IC6','OUT1/GND2/IN3 conforme símbolo, fabricante não definido','REVISAR: footprint chamado Inline tem pads triangulares; fabricante/sufixo 78L05 e conformação das pernas obrigatórios')
add('Q1 Q2','FGA60N65SMD G1/C2/E3 confere','Pitch5.45 confere onsemi; furo1.4986 perto do envelope diagonal máx ~1.415 do terminal; dobra/dissipador/furo5.5 no PCB separados e pendentes; corpo fab15.5 não cobre máx16.2')
add('D1 D2','Pad1 K, pad2 A; netlist coerente clamp inferior/superior','DO35 P7.62 genérico; conferir MPN e faixa de cátodo na montagem')
add('D4','+1, AC2/3, -4; troca entre AC não altera ponte','KBU6G fabricante indefinido; pads seguem GBU4S original P5.08, não confirma KBU escolhido; desenho Vishay não recuperado; F02')
add('Z1 Z2','1.5KE510CA bidirecional; não exigir cátodo elétrico apesar do K desenhado','DNP no esquema mas não no PCB; F08. Pitch real14.732, nome15.24; TVS não substitui clamp gate-emitter')
add('PS1','AC1/2, -Vo3, +Vo4 conferem vista superior Hi-Link p11','Pitch42.5/7.8/22.6 confere desenho de referência; furo1.1 versus terminal0.8±0.2 e pitch±1 exigem peça real; colisão IEC/fixação F07')
add('J1','L1/N2/PE3 lógico; conferir vista e part number real','IEC C6 sem MPN; trilha de rede invade furo mecânico F04; colisão PS1/F1')
add('J2','PE distinto de GND e DC_MINUS','Furo3.2 M3 pad5.1; cobre só0.2059 da borda; resistência/torque/arruela/bonding não definidos; F05')
add('P1 P2','P1 capacitor primário; P2 DC_MID conforme netlist','Nome M6 incompatível com furo2.2: geometria para fio, não para parafuso M6; corpo genérico interfere CT; F02')
add('J110','Não polarizado; AC_N para DC_MID apenas modo110','P10.16 furo2.2; jumper deve ter corrente/isolação especificados e intertravamento/rotulagem; nunca selecionar fechado em220')
add('F1','Não polarizado; duas ilhas por terminal compartilhadas corretamente','Pads ±5.08/±10.16, furos1.1938; fab herdado deslocado; clipe Littelfuse exato não comprovado; tipo/I²t/capacidade interrupção pendentes')
add('T1','Pares1-2/3-4/5-6 conforme netlist; fase não validada','P0584 original renumerado; pads fora de courtyard genérico; bobinagem/fase/isolações/core/volt-segundo desconhecidos')
add('T3','Secundário CT1/2; primário externo sem pad','P12.7 furo1.27; dimensões/core/relação real/fase/burden/isolação desconhecidos; corpo genérico conflita P1/P2')
add('JPRT1 JPRT2','JPRT1 DC_MID; JPRT2 saída CPR1','Extras PCB sem símbolo nem footprint biblioteca; anel D6 furo3.81; retenção/corrente/uso devem ser documentados')
for r in rows:
 r['polaridade'],r['encaixe']=notes.get(r['referencia'],('NPTH não polarizado','Furo mecânico sem referência/lib; conferir arruela/dissipador/standoff e isolamento'))
with (p/'cobertura-pcb.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
