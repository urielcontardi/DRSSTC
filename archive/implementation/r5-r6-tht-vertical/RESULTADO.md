# R5/R6 verticais e remoção das trilhas

Aplicado no PCB principal e sincronizado no esquema: **R5 e R6 THT verticais**, mantendo **100kΩ/0,5W**. Footprint padrão KiCad DIN0309, corpo nominal9×Ø3,2mm, passo5,08mm, furosØ0,8mm e padsØ1,6mm. Footprint e STEP copiados para as bibliotecas locais do projeto; nenhuma marca ou MPN foi selecionada. Dimensões, potência e tensão de trabalho do resistor comprado ainda precisam corresponder à aplicação.

O ponto médio entre os pads foi preservado. A origem do footprint padrão fica no pad1: R5 em(97,4;55,64)mm/90° e R6 em(67,875;46,18)mm/−90°. Números, redes e UUIDs dos pads preservados. Ambos cabem na montagem vertical sem novas colisões no DRC. Referência de R6 posicionada no lado livre para evitar proximidade com D4.

**Todas as17 trilhas de cobre foram removidas.** Restam zero segmentos, arcos de cobre ou vias. Não havia zonas de cobre. Os fios e conexões do esquemático foram preservados.

Comparação final:

- 34 redes e130 conexões idênticas antes/depois.
- Somente R5/R6 e os17 segmentos mudaram na PCB; demais footprints, contorno100×100mm e furos preservados.
- DRC:28→26 ocorrências, sem ocorrências novas; desapareceram os dois avisos de trilhas pendentes.
- Conexões físicas pendentes:97 após a remoção do cobre, como esperado numa PCB sem roteamento.
- Mantém-se a pendência anterior de reorganizar os componentes e furos que estão fora do contorno100×100mm.

Conferência em `verification.json`, netlists e relatórios DRC nesta pasta; prévia em `preview.png`. Licença do modelo copiado preservada em `KiCad-model-NOTICES.txt` e no próprio STEP.
