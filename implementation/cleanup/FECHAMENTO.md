# Fechamento da revisão KiCad — 2026-10-08

**Estado: parcial; não fabricar nem energizar.** Branch `fix/cad-review-20261007`, base `7ac4dfd`. O PCB e esquema na raiz são as fontes CAD deste checkpoint. `canonical*`, `circle-test*` e relatórios `drc-1` a `drc-6` são históricos de teste, não fontes de fabricação. Scripts de estágios anteriores não são pipeline idempotente.

## Alterações recuperadas

- Corrigidas as bibliotecas locais para equivalência com footprints embutidos; modelos ausentes de furos/terminais restaurados. As 20 diferenças anteriores eram orientação equivalente de pads circulares/quadrados, sem mudança física de cobre.
- C9/C10 e R2 separados de corpos adjacentes, sem encolher F.Fab/courtyard. Roteamento salvo e zonas preenchidas. Referências e textos de silk reorganizados parcialmente.
- Q1/Q2 no esquema apontam para `Q_TO3P_ImportedPads_ReviewPending`: geometria importada, **não** confirmação de encapsulamento/MPN.
- Prova nativa `native-proof.json`: 48 identidades, pads/nets/furos, vias, contorno e furos de montagem preservados; apenas C9, C10 e R2 mudaram de posição. `structural-proof.txt` atesta conectividade pino-rede sem alteração.

## Verificação na última gravação

KiCad CLI 10.0.6, contêiner `kicad-web:local`, entrada montada read-only, saídas em `implementation/cleanup`. Comandos: `sch erc --format json`, `sch export netlist`, `pcb drc --all-track-errors --schematic-parity --severity-all --refill-zones --format json`.

| Checagem | Resultado |
|---|---:|
| DRC | 84 violações (antes desta limpeza: 363) |
| Courtyards sobrepostos | 22 |
| PTH/NPTH dentro de courtyard vizinho | 16 / 4 |
| Silk overlap / silk sobre máscara-cobre / silk-borda | 22 / 17 / 3 |
| Curtos, clearance de cobre, hole-clearance e conexões pendentes | 0 reportados |
| Paridade | 2 `extra_footprint`: JPRT1/JPRT2 |
| ERC | 2 `power_pin_not_driven` em PS1; sem alteração de topologia |

`net-current.net` difere de `final.net` somente no carimbo `date` do exportador; o diff textual não mostra outras alterações. Relatórios atuais: `erc-current.json`, `drc-current.json`, `net-current.net`. Plots pós-ajuste: `top.png`, `bottom.png`, `assembly.png`, `before-after.png`. A contagem DRC é ocorrência reportada, não índice de segurança. Regras e exclusões não foram relaxadas.

## Retomada e triagem — 2026-10-08

Checkpoint `87aa19d` inspecionado sem editar o PCB ou esquema. O arquivo `drc-current.json` contém 84 violações: 22 courtyards sobrepostos, 16 PTH e 4 NPTH dentro de courtyard vizinho, 22 overlaps de silk, 17 silk sobre abertura de máscara e 3 silk-borda. A paridade registra JPRT1/JPRT2 como footprints extras; não há itens desconectados. Os arquivos de prova nativa e estrutural continuam vinculados aos hashes do checkpoint (ver `native-proof.json`). Esta retomada é uma triagem dos relatórios existentes, **não** uma nova execução de KiCad nem uma nova prova elétrica.

- C5/C8, C6/C13, IC3/C13 e J110/D4 são colisões localizadas, porém envolvem courtyards/corpos e, em dois pares, silk sobre pads. Mover footprints requer avaliação de espaço, trilhas e zonas; apagar somente círculos/segmentos de silk esconderia a posição física.
- P1/P2/T3/CPR1, Q1/Q2/Z1/Z2/T1, PS1/J1/F1/H3 e furos H2/H4 envolvem envelopes ou fixações interdependentes. Não há correção geométrica independente demonstrada que preserve dimensões, placement elétrico e roteamento.
- As 3 ocorrências silk-borda são contornos de PS1/J1; não justificam alterar borda da placa nem apagar contorno sem confirmar encaixe mecânico.

**Resultado desta retomada:** nenhuma alteração CAD verificavelmente segura identificada; contagens e bloqueios do checkpoint permanecem. Antes de uma nova iteração de placement, confirmar componentes e envelopes físicos listados abaixo.

## Bloqueios reais

1. Colisões físicas envolvem P1/P2, CPR1, Q1/Q2, Z1/Z2, T3, PS1/J1 e H2-H4. Mover essas peças agora exigiria rever trilhas e confirmar dimensões/envelope do conjunto. Não se deve apagar courtyards/corpos ou silk de posição para ocultá-las.
2. Confirmar MPN e desenho de C11/C12, R1, Q1/Q2, J1, PS1, D4/F1, T1/T3, terminais e dissipadores, além do envelope da placa/chassis. Footprints `ReviewPending`/`CONFIRMAR` não estão homologados.
3. Especificar rede de entrada, corrente/pulsos, isolamento e PE/terra de proteção, capacidade térmica e mecânica. DRC sem curto não aprova isolamento de rede/HV ou corrente.
4. JPRT1/JPRT2 exigem decisão funcional/documental: footprint só de placa ou componentes esquemáticos. Mantidos para não inventar topologia.
5. PS1: os 2 ERC requerem decisão sobre fonte/pinos; não adicionar `PWR_FLAG` só para zerar avisos.

Próxima etapa após dados de peças/envelope: placement físico, reroteamento completo da área afetada, refill, ERC/DRC/paridade, netlist e inspeção visual finais. Nenhum Gerber de fabricação é aprovado neste estado.
