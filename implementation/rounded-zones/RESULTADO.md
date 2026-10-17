# Arredondamento das zonas — 17/10/2026

Aplicado `smoothing fillet`, raio de 1 mm, às cinco zonas existentes: GND, DC_MINUS, DC_PLUS, DC_MID e SW_NODE. O KiCad recalculou e salvou o preenchimento. São arredondamentos dos contornos definidos das zonas; os recortes impostos por pads, trilhas e afastamentos continuam seguindo sua geometria.

Redes, prioridades, clearances, camadas, contornos-base, footprints, trilhas e vias preservados. Nenhuma alteração nas regras elétricas ou no esquema nesta etapa. O backup antes da edição está em `before-oneTesla.kicad_pcb`.

DRC nativo após refill: **41 ocorrências, zero conexões faltando**. Comparação por tipo, descrição e UUID confirma que são exatamente as mesmas ocorrências da etapa anterior; nenhum novo erro foi introduzido pelo arredondamento.

| Grupo | Ocorrências | Regiões principais |
| --- | --- | --- |
| Anel PTH menor que a regra de fabricação | 4 | FB1: pads 1–4 têm 0,20 mm; regra pede 0,25 mm |
| Courtyards sobrepostos | 10 | Q1/Z1, Q2/Z2, C11/J110, C12/J110, PS1/furo, P1/CPR1, R1/furo, Z1/Z2, CPR1/furo e CPR1/Z2 |
| Pad PTH dentro de courtyard de outro componente | 4 | Z1/Q1, Z2/Q2 e P1/CPR1 |
| Furo NPTH dentro de courtyard | 2 | R1/furo e CPR1/furo |
| Serigrafia cortada pela borda | 12 | FB1 e PS1 |
| Serigrafia sobre abertura da máscara | 6 | Q1, Q2, Z1, Z2 e referência de furo junto de CPR1 |
| Serigrafia sobreposta | 1 | R6 |
| Ponta de trilha | 1 | +5V, B.Cu, trecho de 0,175 mm perto de (64,25;82,75) mm |
| Via pendente ou conectada em apenas uma face | 1 | Net-(IC2A-C), (62,5;83,25) mm |

Detalhamento com posição de cada item em `VIOLACOES.md`. Sobreposição de courtyard é indicação de envelope de montagem, não confirmação de colisão física entre corpos; precisa considerar alturas, montagem e TVS opcionais. Não foram movidos componentes para resolver esses apontamentos nesta etapa.

Prévia do verso: `after-B_Cu.png` e `after-B_Cu.svg`; comparação antes em `before-B_Cu.png` e `before-B_Cu.svg`.

Referência de implementação: [KiCad — zone fill settings](https://dev-docs.kicad.org/en/file-formats/sexpr-intro/), parâmetros nativos `smoothing fillet` e `radius`.
