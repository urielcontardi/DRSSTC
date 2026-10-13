# Autorroteamento — 2026-10-11

Resultado para revisão: `../../oneTesla-autorouted.kicad_pcb`, com projeto `../../oneTesla-autorouted.kicad_pro`. A placa e o projeto principais não foram alterados.

Freerouting 2.5.0, duas camadas, 30 passes máximos, afunilamento automático desabilitado, distância à borda 0,5 mm e distância a furos 0,25 mm. DSN exportado pelo KiCad 10.0.5; SES importado pelo KiCad. Somente os segmentos de roteamento foram acrescentados ao conteúdo original: componentes, quatro furos, pads, redes, contorno e modelos preservados exatamente. As referências repetidas REF** dos furos receberam identificadores únicos apenas na exportação/importação; os nomes originais foram preservados no resultado.

- Ligações pendentes no DRC do KiCad: **96 → 0**.
- Resultado: **241 segmentos**, **0 vias**, trilhas de **0,2 mm**.
- DRC: **15 ocorrências antes e depois**, idênticas individualmente; nenhuma nova ocorrência.
- Pendências anteriores: 4 PTH dentro de courtyard, 1 NPTH dentro de courtyard (furo superior esquerdo sob PS1), 3 sobreposições de courtyards, 4 silk sobre cobre, 2 sobreposições de silk e 1 diferença de footprint de biblioteca.

Este é um rascunho geométrico de roteamento. O projeto possui apenas a classe genérica Default: largura 0,2 mm e clearance 0,2 mm, usados também nas redes de potência. Correntes, pulsos, isolamento de rede/alta tensão, trajetos de retorno e largura das trilhas de potência ainda precisam ser dimensionados antes de fabricação. Não foram criadas regras que presumam esses requisitos.

`verification.json` registra as invariantes e hashes; `drc-before.json` e `drc-after.json` contêm as verificações nativas feitas com o contexto de bibliotecas da raiz do projeto. `oneTesla.dsn`, `oneTesla.ses` e `freerouting-result.json` preservam entrada, saída e parâmetros do autorroteador; `layout.svg` é a prévia das duas camadas com silk e contorno.
