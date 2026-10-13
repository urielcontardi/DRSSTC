# Atualização dos footprints para SMD

Aplicada em `oneTesla.kicad_pcb` e nas associações do esquema/biblioteca local.

| Referência | Footprint |
| --- | --- |
| R1 | SMD de potência 5 W, padrão PWR8030, corpo 20,8 × 7,6mm |
| R2/R3 | 1206 |
| R4 | 2512 |
| R5/R6 | 2512, land pattern HV12 |
| IC1/IC2 | SOP-14 estreito, 3,9 × 8,7mm; passo 1,27mm |

Valores originais e circuito preservados. Nenhum fabricante/MPN foi atribuído aos componentes. Os documentos em `sources/` servem de referência dimensional para os footprints; não representam uma qualificação de compra.

R1 foi deslocado para (44,5; 151,0)mm para caber sem sobrepor o furo de fixação. Os demais componentes mantêm a posição do corpo; os CIs e R2/R3/R4 tiveram a origem recentrada. Modelos 3D acompanham os novos footprints; o de R1 é um envelope visual nominal.

Verificação: as 34 redes e 130 conexões são idênticas; números dos pads, redes, funções e UUIDs foram preservados. Todos os demais objetos do PCB, inclusive 17 trilhas, contorno e quatro furos, são idênticos ao backup. `oneTesla-autorouted.kicad_pcb` permanece idêntico por SHA-256.

DRC passou de 29 para 23 ocorrências, sem novas ocorrências; continuam as 92 conexões não roteadas já existentes. ERC mantém as mesmas três ocorrências (duas entradas AC de PS1 sem driver e label PE isolada).

Prévia: [preview.png](preview.png). Conferência: [structural-verification.json](structural-verification.json).
