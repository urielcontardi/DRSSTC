# Entrada PE ligada ao GND do controle — 18/10/2026

Aplicado ao esquema, PCB e documentação, por solicitação do usuário. C9 mantém a seleção confirmada: 10µF/100V cerâmico X7R 1210, símbolo não polarizado; os campos descritivos de C9/J2 ficam ocultos para não sobrepor o esquema.

## Onde ligar o fio terra

**Terra de proteção (PE, verde/amarelo) da tomada → ponto dedicado de aterramento do chassis metálico → derivação para J2.** O chassis recebe sua ligação própria: sua proteção não deve depender da continuidade da trilha da PCB. Fixar mecanicamente os fios e prover alívio de tração para a ligação soldada.

**J2 pertence ao GND do controle**, o mesmo nó que PS1.3 (-Vo), GND de IC1/IC2 e GND dos drivers IC3/IC4. Recupera a ligação PE–GND encontrada nos arquivos Eagle originais, onde IEC.G pertence a GND.

**Nunca ligar PE a DC_MINUS, DC_MID, DC_PLUS, SW_NODE ou aos terminais do primário.** DC_MINUS é o negativo do barramento retificado; DC_MID é o ponto médio dos capacitores. Nenhum deles é terra de proteção. O transformador de gate mantém a separação entre os drivers e a meia ponte. J1 continua sendo somente fase/neutro, sem pino de terra.

## Geometria aplicada

- J2 em **(34,3;39,0) mm**, na lateral esquerda, abaixo do furo superior esquerdo e ao lado de PS1. É ponto para fio soldado, **não parafuso M3**.
- Footprint local `oneTesla:PE_Control_GND_WirePad_D4.0mm_Drill2.2mm`: pad PTH Ø4 mm/furo Ø2,2 mm, courtyard Ø5,2 mm.
- Frente: referência J2 e texto `PE / TERRA`. Verso: `J2 PE - GND CONTROLE`.
- Três segmentos B.Cu de 2 mm ligam o pad à saída GND de PS1, pela lateral esquerda e região da saída isolada. Não há ligação ao barramento de potência.
- Esquema: J2 ligado à rede GND; valor `PE / GND CONTROLE`; nota visível indicando chassis + J2 e proibindo ligação aos nós de potência.
- Textos anteriores de J1 sobre PE separado foram corrigidos no esquema e PCB. Branding existente preservado.

## Validação

- DRC KiCad 10.0.7 com refill, todos os erros de trilha e paridade: **18 ocorrências de montagem anteriores, zero conexões faltando, nenhum novo erro de clearance, curto, furação ou serigrafia**. Não foram relaxadas regras nem adicionadas exclusões.
- Paridade: **22 avisos**, todos de campos preexistentes ou furos mecânicos genéricos. J2 não está mais ausente; divergência C9 resolvida.
- ERC: 4 ocorrências anteriores (2 alimentação AC de PS1 e 2 rótulos local/global); aviso de PE isolado eliminado.
- Validador do esquema atualizado para exigir J2 no GND do controle e manter DC_MINUS e DC_MID separados. PASS em 20 redes de referência, sete ligações diretas e 42 referências físicas.
- Comparação das netlists: única mudança de conectividade é J2.1 de /PE isolado para GND. Demais redes preservadas.
- Comparação estrutural do PCB: todos os pads, footprints, trilhas, vias, contorno e regras/contornos de zonas existentes preservados; somente nota de montagem de J1 atualizada. Acrescentados J2, três segmentos e identificação. Zonas recalculadas.
- Inspeção visual de `top.png` e `schematic-detail.png`: identificação legível e esquema sem sobreposição dos campos descritivos.

Relatórios em `drc-final.json`, `erc-after.json`, `verification.json`; netlist em `after.net`. Backups antes da alteração nesta pasta. `apply.py` e `finish.py` registram estágios intermediários, não são um gerador da revisão final.

Esta alteração fecha a entrada de terra na PCB; não libera a fabricação integral nem substitui a conferência da ligação real do chassis e das demais pendências da revisão.
