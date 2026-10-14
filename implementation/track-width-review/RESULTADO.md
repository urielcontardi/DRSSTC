# Revisão das larguras de trilha — 2026-10-13

Revisão do `oneTesla.kicad_pcb` salvo após o roteamento do usuário. PCB, projeto e esquema preservados nesta revisão. Inventário completo e hash do PCB em `inventory.json`; relatório nativo do KiCad 10 em `drc.json`.

Largura é a dimensão configurada no roteador. Espessura é a altura do cobre, definida na fabricação. As recomendações abaixo assumem cobre externo de 1 oz (~35 µm); não há validação térmica sem corrente RMS, regime de pulsos, temperatura ambiente e cobre final confirmado.

## Parecer sobre as larguras existentes

| Circuito/rede | Largura medida | Parecer |
| --- | --- | --- |
| Sinais lógicos dos 74HCT | 0,25–0,50 mm | Adequadas como ponto de partida para as correntes de sinal; manter trajetos curtos e retorno próximo. |
| /OPTICAL_OUT | 0,50 mm | Não exige aumento por largura. |
| +5V | 0,50–1,00 mm | Não exige aumento para alimentar os CIs lógicos/receptor. Há conexões pendentes; verificar continuidade antes de energizar. |
| +15V | 1,00–2,00 mm | Boa base de largura, mas alimentação dos drivers ainda tem ligações pendentes. Os loops de desacoplamento e retorno precisam ser concluídos. |
| IC3 OUT → R4, Net-(IC3-OUT-Pad6) | 0,50 mm; soma dos segmentos 29,26 mm | Trecho mais estreito do acionamento primário. Recomendo refazer mais curto, com 1–2 mm onde possível, incluindo a união dos pinos 6/7; meta de layout, não limite universal do datasheet. |
| IC4 OUT → C4, Net-(C4-Pad1) | 1,00 mm; soma 8,23 mm | Base razoável; manter curto e com retorno próximo. |
| R4 → T1, Net-(T1-AA) | 1,00 mm; soma 5,54 mm | Base razoável; avaliar junto ao loop completo do primário do GDT. |
| C4 → T1, Net-(T1-AB) | 1,00 mm; soma 6,49 mm | Base razoável; avaliar junto ao loop completo do primário do GDT. |
| /GATE_H e /GATE_L | 2,00 mm | Não vejo necessidade de aumentar por largura nesta revisão; proximidade dos retornos e área de loop são essenciais. |
| Entrada AC | 3,00 mm | Não reduzir. Confirmar capacidade térmica para corrente RMS de entrada e forma de onda da retificação. |
| /DC_PLUS, /DC_MINUS | 2,00–3,00 mm | Não aprovadas termicamente nesta revisão; distinguir derivações de gate/bleeders dos caminhos principais de corrente. |
| /DC_MID | 3,00 mm | Não aprovada para corrente do primário sem análise de RMS/pulsos. |
| /SW_NODE | 2,00 mm | Caminho de comutação merece análise própria; não assumir que 2 mm basta para a corrente ressonante. Ainda falta ligação até CPR1. |
| CPR1 → P1, Net-(CPR1-Pad2) | 3,00 mm; soma 6,88 mm | Caminho do primário; capacidade depende de corrente RMS, duração/repetição dos bursts e aquecimento. |
| Retorno GND | Nenhuma trilha ou zona | Não é possível aprovar a alimentação/acionamento sem o retorno. Concluir GND, considerando os loops dos drivers e a separação da potência. |

Os comprimentos acima são somas dos segmentos por rede, incluindo ramais; não são necessariamente o comprimento de um único caminho elétrico.

O [datasheet TI UCC37321, §§10–11](https://www.ti.com/lit/ds/symlink/ucc37321.pdf) informa capacidade de pico de 9 A e destaca proximidade da carga, desacoplamento e roteamento dos retornos. Esse pico nominal não é corrente contínua da trilha. A largura sozinha não resolve indutância, ringing ou desacoplamento inadequado. O datasheet recomenda 100 nF junto à alimentação, acompanhado de capacitância maior, e ligação externa entre os pinos de alimentação e entre AGND/PGND.

## Problemas detectados que impedem aprovação

1. **Curto /DC_MINUS ↔ /DC_MID:** trilha B.Cu iniciando em (73,4;47,14) mm, UUID `0b7d96f4-5957-4b3b-b345-1c519a47c57b`, passa pelo pad 2 de J110 em (104,5;45,46) mm. O DRC acusa curto e ponte de abertura da máscara na mesma região. É necessário desviar a trilha preservando a largura e o clearance; afinar somente esse trecho não é uma solução de isolamento validada.
2. **31 conexões pendentes**, com grande parte envolvendo GND. Não há zona de cobre no arquivo atual. +5V, +15V e barramento também têm conexões pendentes. As larguras adequadas não tornam essas redes conectadas.
3. **Regras gerais mudaram desde a etapa anterior:** projeto atual tem clearance global mínimo 0, classe Default com 0,20 mm de clearance, vias mínimas de 0,50/0,30 mm e anel mínimo de 0,10 mm. As classes Rede_Barramento/Gates_Potencia não estão mais no `.kicad_pro`; permanece a regra personalizada de separação potência/controle no `.kicad_dru`. Portanto, a ausência de erros de clearance não comprova cumprimento da meta anterior de 3 mm entre redes de potência.
4. Seis vias de sinal medem Ø0,50 mm/furo Ø0,30 mm (anel radial de 0,10 mm), abaixo da meta conservadora anterior de Ø0,60/0,30 mm. São sinais, não vias de potência; adotar 0,60/0,30 mm onde houver espaço dá margem de fabricação, mas exige verificar clearance após aumentar.
5. DRC atual: **37 violações**, incluindo curto, conflitos de montagem, quatro anéis PTH do FB1 inferiores à recomendação adotada e problemas de máscara/serigrafia. Nenhuma exclusão foi adicionada nesta revisão.

As capacidades de fabricação da [JLCPCB](https://jlcpcb.com/capabilities/pcb-capabilities) não substituem dimensionamento de corrente e isolamento elétrico. Para fechar a aprovação das trilhas de potência, faltam corrente RMS/estimativa de pico do primário, duração e repetição máximas dos bursts e cobre final da encomenda.

**Conclusão:** sinais e +5V não precisam ser engrossados. Priorizar o curto de J110, os retornos/conexões pendentes e o trecho de 0,50 mm na saída do IC3. A etapa de potência permanece sem aprovação térmica.
