# Componentes e fontes para a revisão do layout

Levantamento em 2026-10-08 do esquema `oneTesla.kicad_sch`, das notas em
`review/` e dos arquivos de fabricante. **Um valor no esquema não é um PN de
compra.** Esta tabela distingue peças nomeadas de geometrias ainda genéricas.
Nenhuma peça alternativa foi selecionada para compra ou aprovada para fabricar.

| Referências | Identificação no esquema | Fonte mecânica | Situação do footprint/layout |
|---|---|---|---|
| PS1 | HLK-15M15BL | [Hi-Link, página do produto](https://www.hlktech.net/index.php?cateid=733&id=1408); `misc/HLK-15W-BL_V1.0.pdf` | Modelo identificado; o próprio desenho informa tolerância de ±1 mm no espaçamento dos pinos. Envelope e interferência com IEC/fusível precisam ser revisados, mas não é uma peça sem datasheet. |
| Q1/Q2 | FGA60N65SMD | [onsemi, datasheet e desenho TO-3P](https://www.onsemi.com/download/data-sheet/pdf/fga60n65smd-d.pdf) | PN identificado; passo de 5,45 mm. O corpo máximo de 16,2 mm e a montagem horizontal/dissipador devem ser representados; o footprint atual é importado e está marcado `ReviewPending`. |
| FB1 | HFBR-2521ETZ | [Broadcom, família HFBR-0500ETZ](https://docs.broadcom.com/doc/AV02-3283EN) | PN e pinagem identificados; biblioteca local já revisada, mas isso não resolve as outras colisões do layout. |
| CPR1 | 940C30S68K-F | [Cornell Dubilier, série 940C](https://www.cde.com/resources/catalogs/940C.pdf) | PN identificado: corpo Ø19 × 46 mm, fio Ø1 mm. Passo da dobra dos terminais na PCB não é uma dimensão de fábrica e a montagem junto a P1/P2/T3 precisa ser redesenhada. |
| D4 | KBU6G | [Vishay, KBU6G](https://www.vishay.com/docs/98732/kbu6.pdf) | O esquema nomeia a família/variante, mas o footprint preserva pads da ponte GBU importada. Conferir ordem e espaçamento do fabricante escolhido antes de alterar pads/roteamento. |
| F1 | Fusível 4 A/250 VAC; clipes 5 × 20 mm | [Littelfuse, clipes série 111](https://www.littelfuse.com/assetdocs/littelfuse_fuse_clip_111_datasheet?assetguid=b1ca8750-5406-48d2-b921-b86728e90adf) | A série 111 é uma opção documentada, não um PN de clipe escolhido. O valor do fusível não define seu suporte, capacidade de interrupção ou envelope de montagem. |
| C11/C12 | 1000 µF, 200 V | [Chemi-Con ESMQ201VSN102MR30S](https://www.chemi-con.co.jp/en/products/detail-condenser.php?part_number=ESMQ201VSN102MR30S), candidato | Sem PN no esquema. O candidato tem corpo Ø30 mm e terminais a 10,00 mm; o footprint atual é 10,16 mm. Não tratá-los como equivalentes sem adaptar o footprint ao PN selecionado. |
| R1 | 1 kΩ, 5 W cerâmico | `misc/oneTeslaTS_Parts.pdf` | Sem PN de fabricante. Corpo de 25 mm e passo de 30,48 mm no CAD são provisórios. |
| J1, P1/P2, T1/T3 | IEC C6, terminais do primário, GDT e CT | `misc/oneTeslaTS_Parts.pdf`; `misc/oneTeslaTS_User_Manual.pdf` | Não há PN mecânico único no esquema/lista. Transformadores podem ser bobinados para o projeto; dimensões, montagem, fase e terminais precisam ser definidos. O nome `Primary_Terminal_M6` não corresponde ao furo de 2,2 mm no CAD. |

## Consequência para a próxima iteração

É possível trabalhar **já** com os desenhos identificados de PS1, Q1/Q2,
FB1 e CPR1 e com envelopes conservadores para propor novo posicionamento.
O levantamento anterior tratou peças identificadas e peças genéricas como
se tivessem a mesma falta de informação; isso foi impreciso. C11/C12, R1,
conector IEC, clipes, transformadores e terminais ainda exigem PN selecionado
ou uma hipótese de montagem explicitamente provisória. Depois de mover
footprints será necessário refazer trilhas e zonas e repetir DRC, paridade,
ERC e inspeção visual no CAD salvo. A placa atual não está liberada.
