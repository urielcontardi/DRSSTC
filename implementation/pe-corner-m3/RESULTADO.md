# J2 no furo de fixação inferior esquerdo

Aplicado a pedido do usuário: o furo da quina em **(37,375;121,05) mm** agora é o ponto J2, ligado ao **GND do controle**.

- Mantida a posição e o diâmetro acabado de **3,2 mm para parafuso M3**. Convertido de NPTH para PTH, com **cobre exposto Ø7 mm nas duas faces**.
- Reutilizar o parafuso com terminal olhal M3 e arruela de até Ø7 mm. Garantir contato metálico firme com o anel de cobre, sem material isolante entre contato e cobre; aliviar a tração do fio. O parafuso/ponto pode participar da ligação do chassis se houver continuidade metálica real; não presumir que espaçador plástico ou superfície pintada aterra o chassis.
- Texto `PE/GND` e referência J2 na serigrafia. O antigo pad separado de J2 foi removido, não há segundo ponto de furação para o terra.
- Acrescentadas somente duas trilhas B.Cu de 2 mm, pela lateral esquerda, até o plano GND do controle.
- Footprint associado e notas de montagem de J2 atualizados no esquemático. DC_MINUS e DC_MID continuam separados do GND.

Nenhum outro footprint, pad, trilha existente, via, contorno ou furo foi reposicionado ou alterado. Zonas recalculadas, sem relaxar regras. Prova estrutural em `verification.json`.

DRC atual: **zero conexões faltando** (antes havia uma de J2); total de ocorrências **36 → 34**. Não há novo curto, clearance de cobre, furação ou serigrafia associado à alteração. Permanecem os envelopes de montagem de R1 na região do furo: o antigo NPTH dentro do courtyard passa a PTH dentro do mesmo courtyard. Com corpo nominal de R1 Ø7,5 mm centrado no pad 1, a distância entre centros é aproximadamente 8,47 mm; um olhal/arruela de Ø7 mm deixa aproximadamente 1,22 mm até esse corpo nominal. Não foram encolhidos courtyards para ocultar a ocorrência.

Prévia da montagem: `detail.png`. Backups e relatórios antes/depois nesta pasta. As outras ocorrências do projeto atual não foram corrigidas nesta alteração.
