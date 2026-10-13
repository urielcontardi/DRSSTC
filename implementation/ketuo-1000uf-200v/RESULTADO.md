# C11/C12 — Ketuo 1000 µF / 200 V

Aplicado na placa principal e no esquemático: corpo nominal **Ø25 × 45 mm**, conforme imagem fornecida pelo usuário. O envelope anterior era Ø30 mm; a redução libera 2,5 mm ao redor de cada capacitor, mantendo as posições.

Footprint local: `oneTesla:CP_D25_H45_P10.16_ReviewPending`. STEP local: `library/3dmodels/Visual_CP_D25_H45_P10.16.step`.

O passo dos terminais **não está informado na imagem**. Foram preservados provisoriamente o passo atual de **10,16 mm**, os furos Ø2 mm e os pads Ø4 mm. O modelo 3D representa o corpo nominal e terminais genéricos; não é CAD do fabricante nem confirma o encaixe da peça. A faixa negativa do invólucro não está representada no modelo genérico; a polaridade está indicada nos pads e na serigrafia.

- C11: (113,17; 67,25) mm, pad1 `/DC_MID`, pad2 `/DC_MINUS`.
- C12: (80,875; 67,3) mm, pad1 `/DC_PLUS`, pad2 `/DC_MID`.
- Valores 1000 µF/200 V, posições, pads, furos, redes e UUIDs dos pads preservados.
- Todos os demais objetos da PCB e toda a conectividade do esquema preservados.
- Placa `oneTesla-autorouted.kicad_pcb` preservada por comparação SHA-256.
- DRC físico: **22 → 22**, sem ocorrências novas; conexões pendentes: **93 → 93**. O arquivo de backup, fora do contexto do projeto, gerou 40 avisos de biblioteca adicionais, separados da comparação física.
- STEP gerado e reimportado com sucesso; corpo nominal Ø25 mm e topo a 45 mm do plano da placa.

Conferência em `verification.json`; relatórios nativos em `drc-before.json` e `drc-after.json`.
