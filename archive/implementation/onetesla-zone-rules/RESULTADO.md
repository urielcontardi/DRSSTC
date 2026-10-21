# Zonas e regras revistas pela referência oneTeslaTS — 17/10/2026

Aplicado ao PCB/projeto ativos. Esta configuração substitui a etapa `implementation/hv-zone-rules`; os números de 3 mm e 6,4 mm daquela etapa foram removidos. Referência: `misc/driver.brd` e leitura do manual registrada em `review/onetesla-context/CONTEXTO.md`.

## Configuração final

| Zona | Camada | Clearance local | Prioridade |
| --- | --- | --- | --- |
| GND | F.Cu e B.Cu | 0,20 mm | 0 implícita |
| DC_MINUS | F.Cu | 0,6096 mm | 1 |
| DC_PLUS | B.Cu | 0,6096 mm | 2 |
| DC_MID | B.Cu | 0,6096 mm | 3 |
| SW_NODE | B.Cu | 0,6096 mm | 5 |

0,6096 mm corresponde ao `isolate` explícito das zonas POS, NEG e N$14 do Eagle. DC_MID não tinha zona no original; usa o mesmo afastamento das outras zonas de potência nesta adaptação. Conexão sólida aos pads de potência e alívio térmico do GND preservados. Contornos, camadas, espessura mínima e demais parâmetros de preenchimento preservados.

Default permanece em 0,20 mm, agora também como mínimo global. O Eagle usa 8 mil (0,2032 mm); preservamos o valor métrico de 0,20 mm já usado pelo roteamento da adaptação. Um ensaio exato com 0,2032 mm apontou quatro ocorrências na lógica de 0,2000–0,2017 mm; não foi necessário rerotear por essa diferença de conversão. GND usa os 0,20 mm gerais; o original não define isolate especial para GND.

Removidas todas as regras elétricas personalizadas de 3 mm, 6,4 mm e gate–emissor de 0,5 mm criadas na etapa anterior, incluindo os requisitos de creepage sem dimensionamento. A regra de fabricação de anel PTH mínimo de 0,25 mm foi preservada. Não foram criadas classes HV nem exclusões de DRC. As demais regras existentes de fabricação foram preservadas.

A hierarquia mantém a correção comprovada de SW_NODE prevalecendo sobre DC_PLUS. DC_MID também prevalece sobre DC_PLUS; DC_MINUS está em outra camada. Esse arranjo não altera as funções elétricas dos planos.

## Validação

Refill e DRC nativos KiCad, com `--all-track-errors --refill-zones --save-board` no resultado final:

- Antes: 85 violações e zero conexões faltando.
- Final: **41 violações e zero conexões faltando**.
- **Zero ocorrências de clearance, creepage ou curto nas regras finais.** Não há mais regra especial de creepage; a ausência de ocorrência desse tipo não é uma verificação de isolamento superficial.
- Zonas de potência terminam com um polígono preenchido cada; GND tem cinco polígonos somando as duas faces, sem conexão faltando apontada pelo DRC.
- As 41 ocorrências restantes são serigrafia (19), courtyards/furos (16), anéis PTH (4), ponta de trilha (1) e via pendente (1).

Comparação estrutural entre backup desta etapa e placa final: footprints, trilhas, vias, linhas/arcos de desenho e contornos das zonas preservados. Nenhum componente movido, nenhuma trilha adicionada ou removida nesta etapa. As conexões de CPR1 e DC_MINUS feitas na etapa anterior continuam presentes.

Backups `before-oneTesla.*` e relatórios `drc-before.json`, `drc-after.json` (ensaio de 0,2032 mm) e `drc-final.json` nesta pasta.

Esta revisão reproduz a referência do oneTesla para as zonas, com as adaptações explicitadas. Não constitui certificação de isolamento ou aprovação de fabricação; permanecem as 41 ocorrências do DRC e as diferenças mecânicas/elétricas em relação ao kit original.
