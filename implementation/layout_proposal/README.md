# Estudo de posicionamento — NÃO fabricar

Este diretório contém uma proposta mecânica **não roteada** para a placa `oneTesla`. A fonte de produção continua sendo `../../oneTesla.kicad_pcb`, sem alterações neste commit. Não exportar Gerbers do estudo nem energizá-lo.

## Entregáveis

- `placement-study.kicad_pcb`: 19 footprints reposicionados e contorno expandido de modo provisório para `(-7,-18)` a `(185,155)` mm. A topologia dos pads no arquivo e os segmentos/vias originais foram preservados; as trilhas **não acompanharam** os pads movidos.
- `assembly.png`: inspeção visual do novo agrupamento. O arquivo do PCB, não a imagem, é a referência geométrica.
- `placement_study.py`: geração reproduzível a partir da fonte da raiz. O script restaura explicitamente as redes serializadas das trilhas por UUID após salvar, pois o pcbnew 10 reassocia sete delas ao mover footprints.
- `drc-placement-study.json`: DRC nativo do KiCad 10.0.6 com paridade, todas as severidades, erros de trilha e refill de zonas, usando cópia do esquema, projeto e bibliotecas locais. A execução do DRC não salvou o PCB do estudo.

## Resultado verificado

| Checagem | Fonte atual | Estudo |
|---|---:|---:|
| Footprints/pads | 48 / 142 | 48 / 142 |
| Segmentos e vias / zonas | 220 / 6 | 220 / 6 |
| Courtyards sobrepostos no DRC | 22 | 0 |
| Violações totais do DRC | 84 | 130 |
| Itens sem conexão | 0 | 34 |
| Curtos | 0 | 10 |
| Paridade esquemático-PCB | 2 | 2 |

O DRC do estudo inclui 74 sobreposições de silk, 23 pontas de trilha soltas, 10 pontes de máscara entre redes, 7 violações de distância a furos, 3 furos NPTH dentro de courtyards, 1 clearance de cobre, 1 silk sobre cobre e 1 ilha de cobre. Os 2 itens de paridade são os `JPRT1/JPRT2` já presentes na fonte; o ERC anterior da fonte aponta 2 `power_pin_not_driven` em PS1. Os três NPTH remanescentes são H2/H4 na área de Q1/Q2 e H3 na área de PS1: podem ser furos de fixação intencionais e não devem ser deslocados sem validar a montagem.

## Bloqueios para substituir o PCB da raiz

1. Rerotear as conexões dos 19 footprints movidos, eliminar os curtos, limpar as 34 desconexões e repetir refill/DRC. O cobre antigo sobre pads novos é o principal risco elétrico imediato.
2. Confirmar contorno, fixações, dissipadores e envelopes físicos da placa e do gabinete. A ampliação é uma hipótese de espaço, não especificação mecânica aprovada.
3. Confirmar os PNs/footprints ainda provisórios listados em `../COMPONENTES_E_FONTES.md`, especialmente IEC, clipes, capacitores C11/C12, transformadores e terminais. O furo de 2,2 mm do CAD para `Primary_Terminal_M6` não comprova compatibilidade com terminal M6.
4. Após roteamento, repetir ERC, exportar e comparar netlist, executar DRC com paridade e `--refill-zones --save-board`, verificar isolamento/correntes e inspecionar visualmente cobre, máscaras, montagem e bordas. Apenas DRC zerado não libera fabricação ou operação de alta tensão.

## Reprodução da checagem

O PCB do estudo precisa ser copiado com nome `oneTesla.kicad_pcb` para uma pasta de teste contendo `oneTesla.kicad_pro`, `oneTesla.kicad_sch`, `fp-lib-table`, `sym-lib-table` e `library/` da raiz. No KiCad 10.0.6:

```sh
kicad-cli pcb drc --all-track-errors --schematic-parity --severity-all --refill-zones --format json -o drc.json oneTesla.kicad_pcb
```

O relatório anterior da fonte está em `../cleanup/drc-current.json`; não se trata de um DRC novo da fonte neste estudo.
