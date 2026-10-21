# Ocorrências do DRC após arredondamento

41 ocorrências; zero conexões faltando. São erros/avisos CAD, incluindo múltiplas ocorrências sobre uma mesma região.

Prioridades para revisão: FB1 tem quatro anéis de 0,20 mm frente à regra de fabricação de 0,25 mm; as sobreposições de montagem exigem conferir envelopes, altura e componentes opcionais, pois sobreposição de courtyard não prova colisão física. Serigrafia pode sair cortada/ilegível. Pontas de trilha/via não equivalem a redes sem conexão: o DRC final não aponta conexões faltando. Nenhuma dessas ocorrências foi ocultada ou alterada nesta etapa.

## Anel de cobre dos pads PTH — 4

- Annular width (rule 'PTH annular ring JLCPCB recomendado 1oz' min annular width 0.2500 mm; actual 0.2000 mm): PTH pad 1 [/OPTICAL_OUT] of FB1 em (41.105; 102.51) mm.
- Annular width (rule 'PTH annular ring JLCPCB recomendado 1oz' min annular width 0.2500 mm; actual 0.2000 mm): PTH pad 2 [GND] of FB1 em (41.105; 99.97) mm.
- Annular width (rule 'PTH annular ring JLCPCB recomendado 1oz' min annular width 0.2500 mm; actual 0.2000 mm): PTH pad 3 [+5V] of FB1 em (41.105; 97.43) mm.
- Annular width (rule 'PTH annular ring JLCPCB recomendado 1oz' min annular width 0.2500 mm; actual 0.2000 mm): PTH pad 4 [+5V] of FB1 em (41.105; 94.89) mm.

## Sobreposição de áreas de montagem (courtyards) — 10

- Courtyards overlap: Footprint Q2 em (106.625; 92.75) mm; Footprint Z2 em (112.75; 97.0) mm.
- Courtyards overlap: Footprint C11 em (117.75; 56.0) mm; Footprint J110 em (104.5; 37.84) mm.
- Courtyards overlap: Footprint J110 em (104.5; 37.84) mm; Footprint C12 em (91.755; 56.0) mm.
- Courtyards overlap: Footprint REF** em (37.375; 33.05) mm; Footprint PS1 em (58.7; 30.8675) mm.
- Courtyards overlap: Footprint P1 em (125.5; 110.6) mm; Footprint CPR1 em (98.9; 116.4) mm.
- Courtyards overlap: Footprint Q1 em (106.575; 73.8) mm; Footprint Z1 em (112.75; 78.25) mm.
- Courtyards overlap: Footprint R1 em (42.25; 117.75) mm; Footprint REF** em (37.375; 121.05) mm.
- Courtyards overlap: Footprint Z1 em (112.75; 78.25) mm; Footprint Z2 em (112.75; 97.0) mm.
- Courtyards overlap: Footprint CPR1 em (98.9; 116.4) mm; Footprint REF** em (125.375; 121.05) mm.
- Courtyards overlap: Footprint CPR1 em (98.9; 116.4) mm; Footprint Z2 em (112.75; 97.0) mm.

## Pad metalizado dentro da área de montagem de outro componente — 4

- PTH inside courtyard: PTH pad 2 [/DC_MINUS] of Z2 em (112.75; 104.366) mm; Footprint Q2 em (106.625; 92.75) mm.
- PTH inside courtyard: PTH pad 1 [Net-(CPR1-Pad2)] of P1 em (125.5; 110.6) mm; Footprint CPR1 em (98.9; 116.4) mm.
- PTH inside courtyard: PTH pad 1 [/DC_PLUS] of Z1 em (112.75; 70.884) mm; Footprint Q1 em (106.575; 73.8) mm.
- PTH inside courtyard: PTH pad 2 [/SW_NODE] of Z1 em (112.75; 85.616) mm; Footprint Q1 em (106.575; 73.8) mm.

## Furo não metalizado dentro da área de montagem de componente — 2

- NPTH inside courtyard: NPTH pad of REF** em (37.375; 121.05) mm; Footprint R1 em (42.25; 117.75) mm.
- NPTH inside courtyard: NPTH pad of REF** em (125.375; 121.05) mm; Footprint CPR1 em (98.9; 116.4) mm.

## Ponta de trilha sem conexão — 1

- Track has unconnected end: Track [+5V] on B.Cu, length 0.1750 mm em (64.25; 82.75) mm.

## Via conectada em apenas uma face ou sem conexão — 1

- Via is not connected or connected on only one layer: Via [Net-(IC2A-C)] on F.Cu - B.Cu em (62.5; 83.25) mm.

## Serigrafia cortada pela borda da placa — 12

- Silkscreen clipped by board edge: Rectangle on Edge.Cuts em (31.375; 27.05) mm; Segment of FB1 on F.Silkscreen em (31.405; 93.6) mm.
- Silkscreen clipped by board edge: Rectangle on Edge.Cuts em (31.375; 27.05) mm; Segment of FB1 on F.Silkscreen em (31.405; 94.7) mm.
- Silkscreen clipped by board edge: Rectangle on Edge.Cuts em (31.375; 27.05) mm; Segment of FB1 on F.Silkscreen em (31.405; 95.9) mm.
- Silkscreen clipped by board edge: Rectangle on Edge.Cuts em (31.375; 27.05) mm; Segment of FB1 on F.Silkscreen em (31.405; 97.1) mm.
- Silkscreen clipped by board edge: Rectangle on Edge.Cuts em (31.375; 27.05) mm; Segment of FB1 on F.Silkscreen em (31.405; 98.3) mm.
- Silkscreen clipped by board edge: Rectangle on Edge.Cuts em (31.375; 27.05) mm; Segment of FB1 on F.Silkscreen em (31.405; 99.5) mm.
- Silkscreen clipped by board edge: Rectangle on Edge.Cuts em (31.375; 27.05) mm; Segment of FB1 on F.Silkscreen em (31.405; 100.7) mm.
- Silkscreen clipped by board edge: Rectangle on Edge.Cuts em (31.375; 27.05) mm; Segment of FB1 on F.Silkscreen em (31.405; 101.9) mm.
- Silkscreen clipped by board edge: Rectangle on Edge.Cuts em (31.375; 27.05) mm; Segment of FB1 on F.Silkscreen em (31.405; 103.1) mm.
- Silkscreen clipped by board edge: Rectangle on Edge.Cuts em (31.375; 27.05) mm; Segment of FB1 on F.Silkscreen em (35.445; 103.81) mm.
- Silkscreen clipped by board edge: Rectangle on Edge.Cuts em (31.375; 27.05) mm; Segment of FB1 on F.Silkscreen em (35.565; 93.54) mm.
- Silkscreen clipped by board edge: Rectangle on Edge.Cuts em (31.375; 27.05) mm; Polygon of PS1 on F.Silkscreen em (59.45; 26.3675) mm.

## Serigrafia sobre abertura da máscara — 6

- Silkscreen clipped by solder mask: Footprint text of Z2 (K) em (107.75; 90.5) mm; PTH pad 1 [/GATE_L] of Q2 em (106.625; 92.75) mm.
- Silkscreen clipped by solder mask: Footprint text of Z1 (K) em (107.75; 71.75) mm; PTH pad 1 [/GATE_H] of Q1 em (106.575; 73.8) mm.
- Silkscreen clipped by solder mask: Segment of Q2 on F.Silkscreen em (109.515; 90.34) mm; PTH pad 1 [/SW_NODE] of Z2 em (112.75; 89.634) mm.
- Silkscreen clipped by solder mask: Segment of Q1 on F.Silkscreen em (109.465; 87.11) mm; PTH pad 2 [/SW_NODE] of Z1 em (112.75; 85.616) mm.
- Silkscreen clipped by solder mask: Segment of Q1 on F.Silkscreen em (109.465; 71.39) mm; PTH pad 1 [/DC_PLUS] of Z1 em (112.75; 70.884) mm.
- Silkscreen clipped by solder mask: Reference field of REF** em (126.765; 114.4) mm; PTH pad 2 [Net-(CPR1-Pad2)] of CPR1 em (128.11; 116.4) mm.

## Sobreposição de serigrafia — 1

- Silkscreen clearance: Segment of R6 on B.Silkscreen em (116.3; 62.75) mm; Reference field of R6 em (118.5; 63.2) mm.
