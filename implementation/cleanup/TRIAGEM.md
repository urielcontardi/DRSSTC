# Triagem reproduzível do checkpoint KiCad

Gerado de `drc-current.json` e `erc-current.json` por `triage_drc.py`.
Os hashes do PCB e esquema foram comparados a `native-proof.json`.
**Isto não reexecuta KiCad, não valida peças/envelopes e não libera fabricação.**

- DRC: **84** ocorrências; conexões pendentes: **0**.
- Paridade: **2**; ERC: **2**.
- Tipos DRC: `courtyards_overlap` 22, `npth_inside_courtyard` 4, `pth_inside_courtyard` 16, `silk_edge_clearance` 3, `silk_over_copper` 17, `silk_overlap` 22.

## Grupos de interferência

Uma ocorrência pertence a um grupo; grupos ligados por uma mesma referência são unidos.
A contagem inclui silk, furos e courtyard e **não** mede a gravidade elétrica.

| Referências ligadas | Ocorrências | Tipos |
|---|---:|---|
| C13, C6, CPR1, H2, H4, IC3, IC4, JPRT1, P1, P2, Q1, Q2, R1, R4, T1, T3, Z1, Z2 | 59 | courtyards_overlap: 18, npth_inside_courtyard: 2, pth_inside_courtyard: 15, silk_over_copper: 12, silk_overlap: 12 |
| F1, H3, J1, PS1 | 15 | courtyards_overlap: 2, npth_inside_courtyard: 2, pth_inside_courtyard: 1, silk_edge_clearance: 3, silk_over_copper: 3, silk_overlap: 4 |
| D4, J110 | 6 | courtyards_overlap: 1, silk_overlap: 5 |
| C5, C8 | 4 | courtyards_overlap: 1, silk_over_copper: 2, silk_overlap: 1 |

## Paridade e ERC

- Paridade `extra_footprint`: JPRT1.
- Paridade `extra_footprint`: JPRT2.
- ERC `power_pin_not_driven`: Symbol PS1 Pin 1 [AC, Power input, Line].
- ERC `power_pin_not_driven`: Symbol PS1 Pin 2 [AC, Power input, Line].

Pendências de componente, potência, isolamento e envelope físico permanecem em `FECHAMENTO.md`.
