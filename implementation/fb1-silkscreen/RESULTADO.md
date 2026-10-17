# Pads de FB1, serigrafia e sobras de roteamento — 17/10/2026

Aplicado ao PCB ativo e às bibliotecas locais correspondentes, preservando as edições existentes.

## Alterações

- FB1, pads 1–4: tamanho de 1,8 × 2,6 para **2,0 × 2,6 mm**. Furos de **1,4 mm**, centros, números e nets preservados. Anel mínimo nominal passa de 0,20 para **0,30 mm**, acima da regra existente de 0,25 mm. Pads de retenção 5/8 preservados. Alteração também aplicada à biblioteca `HFBR-2521ETZ.kicad_mod`.
- FB1: contorno de serigrafia recortado no limite útil da placa, preservando a geometria de fabricação; referência reposicionada dentro da placa. As partes do receptor que avançam além da borda continuam representadas no F.Fab/3D; não foi movido o componente.
- PS1: triângulo de identificação do pino 1 deslocado para dentro da placa.
- Q1/Q2: contornos de serigrafia interrompidos junto aos pads dos TVS Z1/Z2, com folga; geometria de fabricação e montagem preservada.
- Z1/Z2: marcações de cátodo `K` reposicionadas em áreas livres.
- R6: referência afastada do contorno do resistor.
- Ocultadas as referências genéricas `REF**` dos quatro furos de montagem; não são identificadores úteis de montagem e uma delas invadia o pad de CPR1.
- Sincronizadas as alterações de gráficos nas bibliotecas locais de FB1, Q1/Q2 e PS1 para evitar divergência com os footprints colocados. Os recortes de FB1 e PS1 atendem ao posicionamento junto da borda desta placa.
- Removido o segmento redundante +5V, UUID `bbc751e8-54b9-4c55-8d17-4a26d6531728`, de 0,175 mm em B.Cu. Ele estava inteiramente sobre outro segmento +5V, que permanece.
- Removida a via `5f1656f8-1238-4c43-ba35-bdfe04c83b6e`, net `Net-(IC2A-C)`, em (62,5;83,25) mm. Os dois segmentos ligados a ela já se encontram em B.Cu no mesmo ponto e foram preservados; não havia conexão na outra face que exigisse transição.

As cinco zonas continuam com o arredondamento de 1 mm, mesmas prioridades e afastamentos da etapa anterior. Nenhuma mudança no esquema, pinagem ou posição dos componentes.

## Validação

Refill e DRC nativos KiCad com `--all-track-errors --refill-zones --save-board`:

| Verificação | Antes | Final |
| --- | ---: | ---: |
| Total de ocorrências | 41 | **16** |
| Anel PTH | 4 | **0** |
| Serigrafia (todos os tipos) | 19 | **0** |
| Ponta de trilha / via pendente | 2 | **0** |
| Divergência com biblioteca local | 0 | **0** |
| Conexões faltando | 0 | **0** |
| Clearance / curtos | 0 | **0** |

Permanecem somente as **16 ocorrências de montagem** já existentes: 10 sobreposições de courtyard, quatro pads PTH dentro de courtyard de outro componente e dois furos NPTH dentro de courtyard. Nenhuma exclusão de DRC ou redução de regra foi adicionada.

Comparação estrutural confirma que os demais pads, trilhas e vias estão preservados; somente os quatro tamanhos de pads e os dois itens redundantes de roteamento listados acima mudaram no cobre. Furos, nets e posições de todos os pads foram preservados. As zonas mantêm contornos-base, prioridades, clearances e fillet; preenchimento recalculado.

Prévia inspecionada: `front.png`; relatório completo: `drc-final.json`. Backups da placa e das três bibliotecas alteradas nesta pasta. `adjust.py` e `finish.py` são registros de execução desta edição, não ferramentas para repetir sobre a placa atual.
