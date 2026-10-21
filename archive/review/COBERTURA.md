# Cobertura por referência — PCB atual

48/48 instâncias inventariadas e anotadas. **Cobertura não significa aprovação da peça.** Pinagem, passo e furo estão nos CSV.

| Referência | Valor | Polaridade/pinagem | Encaixe e pendências |
|---|---|---|---|
| C1 | 1u | Não polarizados no símbolo | Disco P5, furos/pads inventariados; dielétrico/tensão/ESL/MPN desconhecidos; C4 deve suportar corrente do GDT |
| C10 | 680u 35V | Pad1 positivo +15 V; valor 680u 35V na fonte, fab mantém texto antigo 100u 10V | Pendente MPN: pitch real 3.556 versus nome 5; corpo/silk deslocados 2.5 mm; F02 |
| C11 | 1000u 200V | Pad1 positivo confere com netlist; serigrafia deslocada 5 mm | REPROVADO envelope D30: centros distam 26.035 mm, sobreposição 3.965 mm; F03. Pitch 10.16, MPN desconhecido |
| C12 | 1000u 200V | Pad1 positivo confere com netlist; serigrafia deslocada 5 mm | REPROVADO envelope D30: centros distam 26.035 mm, sobreposição 3.965 mm; F03. Pitch 10.16, MPN desconhecido |
| C13 | 100u 25V | Pad1 positivo confere; corpo/silk deslocados em relação ao par de pads | Pendente MPN: pitch real 2.54 versus nome 3.50; F02. C9 em +5 V; C8/C13 em +15 V |
| C2 | 1u | Não polarizados no símbolo | Disco P5, furos/pads inventariados; dielétrico/tensão/ESL/MPN desconhecidos; C4 deve suportar corrente do GDT |
| C3 | 1u | Não polarizados no símbolo | Disco P5, furos/pads inventariados; dielétrico/tensão/ESL/MPN desconhecidos; C4 deve suportar corrente do GDT |
| C4 | 1u | Não polarizados no símbolo | Disco P5, furos/pads inventariados; dielétrico/tensão/ESL/MPN desconhecidos; C4 deve suportar corrente do GDT |
| C5 | 1u | Não polarizados no símbolo | Disco P5, furos/pads inventariados; dielétrico/tensão/ESL/MPN desconhecidos; C4 deve suportar corrente do GDT |
| C6 | 1u | Não polarizados no símbolo | Disco P5, furos/pads inventariados; dielétrico/tensão/ESL/MPN desconhecidos; C4 deve suportar corrente do GDT |
| C8 | 100u 25V | Pad1 positivo confere; corpo/silk deslocados em relação ao par de pads | Pendente MPN: pitch real 2.54 versus nome 3.50; F02. C9 em +5 V; C8/C13 em +15 V |
| C9 | 100u 10V | Pad1 positivo confere; corpo/silk deslocados em relação ao par de pads | Pendente MPN: pitch real 2.54 versus nome 3.50; F02. C9 em +5 V; C8/C13 em +15 V |
| CPR1 | 68n 3kV | Não polarizado | CDE 940C30S68K-F: corpo 46x19 e fio 1 mm conferem catálogo; P58.42 é dobra escolhida, não pitch de fábrica; furo1.4; ensaio RMS/dVdt obrigatório |
| D1 | 1N4148 | Pad1 K, pad2 A; netlist coerente clamp inferior/superior | DO35 P7.62 genérico; conferir MPN e faixa de cátodo na montagem |
| D2 | 1N4148 | Pad1 K, pad2 A; netlist coerente clamp inferior/superior | DO35 P7.62 genérico; conferir MPN e faixa de cátodo na montagem |
| D4 | KBU6G | +1, AC2/3, -4; troca entre AC não altera ponte | KBU6G fabricante indefinido; pads seguem GBU4S original P5.08, não confirma KBU escolhido; desenho Vishay não recuperado; F02 |
| F1 | 4A/250VAC | Não polarizado; duas ilhas por terminal compartilhadas corretamente | Pads ±5.08/±10.16, furos1.1938; fab herdado deslocado; clipe Littelfuse exato não comprovado; tipo/I²t/capacidade interrupção pendentes |
| FB1 | HFBR-2521ETZ | 1 OUT, 2 GND, 3 VCC, 4 RL coerentes eletricamente; retenções 5/8 NC | REPROVADO HFBR-2521ETZ: pitch 1.905 versus 2.54 mm datasheet; ordem espacial 3-1-2-4 adaptada de IFD95; F01 |
| IC1 | 74HCT14 | DIP pad1 retangular e numeração padrão; alimentação/netlist conferem | DIP14 P2.54 W7.62; furo0.8128 pad1.6; MPN/sufixo e soquete exatos desconhecidos; LongPads no nome não corresponde ao pad real |
| IC2 | 74HCT74 | DIP pad1 retangular e numeração padrão; alimentação/netlist conferem | DIP14 P2.54 W7.62; furo0.8128 pad1.6; MPN/sufixo e soquete exatos desconhecidos; LongPads no nome não corresponde ao pad real |
| IC3 | UCC37321P | UCC37321: VDD1/8, IN2, EN3, GND4/5, OUT6/7 conferem datasheet e netlist | PDIP8 P2.54 W7.62 coerente; soquete exato pendente; TI recomenda desacoplamento em ambos pares VDD/GND, não comprovado nesta geometria |
| IC4 | UCC37321P | UCC37321: VDD1/8, IN2, EN3, GND4/5, OUT6/7 conferem datasheet e netlist | PDIP8 P2.54 W7.62 coerente; soquete exato pendente; TI recomenda desacoplamento em ambos pares VDD/GND, não comprovado nesta geometria |
| IC6 | 78L05 | OUT1/GND2/IN3 conforme símbolo, fabricante não definido | REVISAR: footprint chamado Inline tem pads triangulares; fabricante/sufixo 78L05 e conformação das pernas obrigatórios |
| J1 | IEC C6 | L1/N2/PE3 lógico; conferir vista e part number real | IEC C6 sem MPN; trilha de rede invade furo mecânico F04; colisão PS1/F1 |
| J110 | Jumper 110V | Não polarizado; AC_N para DC_MID apenas modo110 | P10.16 furo2.2; jumper deve ter corrente/isolação especificados e intertravamento/rotulagem; nunca selecionar fechado em220 |
| J2 | PE/CHASSIS | PE distinto de GND e DC_MINUS | Furo3.2 M3 pad5.1; cobre só0.2059 da borda; resistência/torque/arruela/bonding não definidos; F05 |
| JPRT1 |  | JPRT1 DC_MID; JPRT2 saída CPR1 | Extras PCB sem símbolo nem footprint biblioteca; anel D6 furo3.81; retenção/corrente/uso devem ser documentados |
| JPRT2 |  | JPRT1 DC_MID; JPRT2 saída CPR1 | Extras PCB sem símbolo nem footprint biblioteca; anel D6 furo3.81; retenção/corrente/uso devem ser documentados |
| P1 | PRIMARIO A | P1 capacitor primário; P2 DC_MID conforme netlist | Nome M6 incompatível com furo2.2: geometria para fio, não para parafuso M6; corpo genérico interfere CT; F02 |
| P2 | PRIMARIO B | P1 capacitor primário; P2 DC_MID conforme netlist | Nome M6 incompatível com furo2.2: geometria para fio, não para parafuso M6; corpo genérico interfere CT; F02 |
| PS1 | HLK-15M15BL | AC1/2, -Vo3, +Vo4 conferem vista superior Hi-Link p11 | Pitch42.5/7.8/22.6 confere desenho de referência; furo1.1 versus terminal0.8±0.2 e pitch±1 exigem peça real; colisão IEC/fixação F07 |
| Q1 | FGA60N65SMD | FGA60N65SMD G1/C2/E3 confere | Pitch5.45 confere onsemi; furo1.4986 perto do envelope diagonal máx ~1.415 do terminal; dobra/dissipador/furo5.5 no PCB separados e pendentes; corpo fab15.5 não cobre máx16.2 |
| Q2 | FGA60N65SMD | FGA60N65SMD G1/C2/E3 confere | Pitch5.45 confere onsemi; furo1.4986 perto do envelope diagonal máx ~1.415 do terminal; dobra/dissipador/furo5.5 no PCB separados e pendentes; corpo fab15.5 não cobre máx16.2 |
| R1 | 1k 5W | Não polarizado | REPROVADO envelope: corpo declarado 25 mm, furos distam 22.86 mm; silk/fab deslocados 15.24 mm; F02 |
| R2 | 1k | Não polarizado | DIN0207 P7.62 coerente genericamente; conferir potência/tolerância/corpo MPN; R4 amortecimento GDT depende de ensaio |
| R3 | 10k | Não polarizado | DIN0207 P7.62 coerente genericamente; conferir potência/tolerância/corpo MPN; R4 amortecimento GDT depende de ensaio |
| R4 | 3R3 | Não polarizado | DIN0207 P7.62 coerente genericamente; conferir potência/tolerância/corpo MPN; R4 amortecimento GDT depende de ensaio |
| R5 | 100k 0.5W | Não polarizado | Pendente MPN 0.5 W: pitch real 10.16, nome 12.70; fab/silk não recentrados; F02 |
| R6 | 100k 0.5W | Não polarizado | Pendente MPN 0.5 W: pitch real 10.16, nome 12.70; fab/silk não recentrados; F02 |
| SEM_REF_10 |  | NPTH não polarizado | Furo mecânico sem referência/lib; conferir arruela/dissipador/standoff e isolamento |
| SEM_REF_20 |  | NPTH não polarizado | Furo mecânico sem referência/lib; conferir arruela/dissipador/standoff e isolamento |
| SEM_REF_25 |  | NPTH não polarizado | Furo mecânico sem referência/lib; conferir arruela/dissipador/standoff e isolamento |
| SEM_REF_35 |  | NPTH não polarizado | Furo mecânico sem referência/lib; conferir arruela/dissipador/standoff e isolamento |
| SEM_REF_37 |  | NPTH não polarizado | Furo mecânico sem referência/lib; conferir arruela/dissipador/standoff e isolamento |
| T1 | 1:1:1 | Pares1-2/3-4/5-6 conforme netlist; fase não validada | P0584 original renumerado; pads fora de courtyard genérico; bobinagem/fase/isolações/core/volt-segundo desconhecidos |
| T3 | 1:300 | Secundário CT1/2; primário externo sem pad | P12.7 furo1.27; dimensões/core/relação real/fase/burden/isolação desconhecidos; corpo genérico conflita P1/P2 |
| Z1 | 1.5KE510CA | 1.5KE510CA bidirecional; não exigir cátodo elétrico apesar do K desenhado | DNP no esquema mas não no PCB; F08. Pitch real14.732, nome15.24; TVS não substitui clamp gate-emitter |
| Z2 | 1.5KE510CA | 1.5KE510CA bidirecional; não exigir cátodo elétrico apesar do K desenhado | DNP no esquema mas não no PCB; F08. Pitch real14.732, nome15.24; TVS não substitui clamp gate-emitter |
