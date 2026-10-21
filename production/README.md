# Pacotes de entrega

## PCB

- [`pcb/2026-10-18/`](pcb/2026-10-18/): pacote anterior de Gerbers/furação,
  DRC e manifesto de arquivos.
- [`pcb/2026-10-18-dfm/`](pcb/2026-10-18-dfm/): revisão para reanálise DFM;
  consultar a README dessa pasta para as pendências.
- [`pcb/2026-10-20-3d/ARCSTRIKE-PCB-completa.step`](pcb/2026-10-20-3d/ARCSTRIKE-PCB-completa.step):
  PCB montada com os modelos de IGBT e ponte ajustados.

Os Gerbers e ZIPs anteriores foram movidos sem alterar seu conteúdo. As
chaves de caminhos do manifesto DFM foram ajustadas; os hashes registrados
foram preservados. Os hashes da PCB/esquema nesses manifestos correspondem
à captura daquela revisão, não necessariamente ao projeto ativo atual.

## Case

- [`case/v1/ARCSTRIKE-case-v1-CONCEITO.zip`](case/v1/ARCSTRIKE-case-v1-CONCEITO.zip):
  conjunto STEP, STLs, visualizador e fontes da primeira proposta da case.
- As fontes de trabalho ficam em [`mechanical/case-v1/`](../mechanical/case-v1/).

O STEP de todo o conjunto está em
[`mechanical/case-v1/exports/ARCSTRIKE-case-v1-CONCEPT.step`](../mechanical/case-v1/exports/ARCSTRIKE-case-v1-CONCEPT.step).
O suporte das bobinas ainda usa medidas provisórias.
