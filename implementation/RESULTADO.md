# Implementação da revisão DRSSTC — parcial, não fabricar

Branch local: **fix/cad-review-20261007**. Base preservada: **60c237c** (projeto original f4da80c + auditoria). Sem push. A interrupção do provedor deixou uma etapa de roteamento não validada; ela foi recuperada, corrigida e verificada. O checkpoint interrompido fica em checkpoint/interrupted.kicad_pcb, exclusivamente histórico: NÃO usar para fabricação.

## Alterações efetivamente aplicadas

1. **Esquema:** revisão por referência incorporada nos campos Footprint_Status; referências dos seis modelos personalizados corrigidas. Nenhuma topologia, tensão nominal, valor elétrico, fase do GDT ou função lógica alterada. Não foram adicionados power flags para maquiar o ERC.
2. **HFBR-2521ETZ:** substituída geometria IFD95 improvisada por geometria KiCad HFBR-252x, confrontada com Broadcom AV02-3283EN pp4/11. Passo 2,54 mm, pads1–4 nas posições reais, retenção6 do modelo genérico renomeada8; pads5/8 PTH com nets NC individuais, sem conexão a GND. Furos1,4/pads são escolha do modelo nativo, não tolerância de fabricação certificada. Receptor reposicionado em (34;76), 90°, e redes OUT/+5V/GND reroteadas. Removidos antigos stubs e ajustada a zona +5V da área desocupada. Nenhum novo via.
3. **Corpos/polaridades:** C8/C9/C10/C11/C12/C13, R1/R5/R6, Z1/Z2 usam seis modelos personalizados com o corpo recentrado em relação aos pads reais. Pad1 dos eletrolíticos retangular; nomes indicam o passo real e a pendência. Não reduzimos o diâmetro dos capacitores para esconder a colisão. Modelos 3D antigos incompatíveis foram retirados desses modelos novos, não substituídos por peças inventadas. Valores e referências de montagem dos capacitores foram reposicionados para não sugerir o valor do vizinho.
4. **Entrada AC:** trilha AC_L mantida em2,54 mm e desviada do NPTH de J1. Trecho superior PE deslocado para y0,8 sem reduzir largura. Derivação auxiliar AC_L_FUSED de0,5 mm transferida para B.Cu entre pads PTH existentes de F1/PS1; sem novos vias. Eliminada a invasão de cobre no furo. A menor separação rede–PE continua inadequadamente especificada: isto NÃO aprova isolamento nem bonding.
5. **Paridade:** DNP de Z1/Z2 sincronizado, campos Footprint_Status/Assembly_Notes/Datasheet/Description transferidos ao PCB. Validador ajustado para exigir também os pads5/8 reais do HFBR, em vez de dispensá-los.
6. Contorno da placa, pontos de montagem, redes dos pads elétricos preexistentes e topologia preservados. Eagle e snapshots históricos não editados.

## Verificação nativa final — KiCad10.0.6

| Verificação | Antes | Depois |
|---|---:|---:|
| Violações DRC reportadas |529|509|
| Questões de paridade |56|11|
| Conexões pendentes |0|0|
| Erros + avisos (DRC/paridade) |87 + 498|69 + 451|
| Hole clearance |2|0|
| Curtos / trilhas cruzadas / clearance de cobre |0 / 0 / 0|0 / 0 / 0|
| Courtyards sobrepostos |45|39|
| ERC principal |2|2|

As duas ocorrências ERC continuam PS1.1/2 power_pin_not_driven. A contagem é a saída reportada pelo KiCad, não métrica de segurança nem garantia de que todos os problemas físicos foram resolvidos. Não foram relaxadas regras, adicionadas exclusões DRC/ERC nem suprimidos courtyards.

- Netlist nativa final **idêntica** à base, por grupos de referência/pino.
- Todos os pads elétricos anteriores preservam suas nets; apenas retenções NC5/8 foram acrescentadas.
- Validador passou nas20 redes de referência,7 ligações diretas e41 componentes, incluindo todos os pinos dos CIs.
- Contorno Edge.Cuts comparado estruturalmente e preservado.
- Refill salvo, DRC/paridade executados novamente; SVGs nativos de topo/fundo/montagem convertidos e inspecionados após os últimos ajustes.
- QA paralelo foi interrompido pelo mesmo limite do provedor, sem parecer final. Sua inspeção parcial confirmou topologia preservada; NÃO é apresentado como aprovação independente final.

Evidências: evidence/drc-final.json, final-erc.json, final-oneTesla.net, final-validation.txt, invariants.txt, top/bottom/assembly.svg e .png, before-after.png. A comparação visual mantém a mesma placa e mostra alterações reais; não é simulação 3D.

## Cobertura e limites por peça

cobertura-final.csv tem **48/48 instâncias do PCB**, com pads/nets atuais e estado individual. A auditoria anterior preservada em ../review contém135/135 modelos originais inventariados e checados geometricamente,51/51 elementos Eagle e todos os esquemas. Foram acrescentados seis modelos personalizados, totalizando141 arquivos de biblioteca. Isso NÃO significa141 peças homologadas contra fabricante. As peças não identificadas continuam não identificadas; a revisão não inventa MPN.

## Decisões exatas que bloqueiam o restante do layout

1. **C11/C12:** selecionar fabricante/código completo, diâmetro/altura/passo, tensão e ripple. Corpos D30 ainda se sobrepõem3,965 mm e C11 ultrapassa o contorno mesmo recentrado. É necessário decidir entre peças adequadas menores ou rearranjo/ampliação autorizada da placa com dimensões do enclosure. Não alterar outline às cegas.
2. **R1:** peça axial de corpo25 mm não cabe horizontalmente entre furos22,86 mm. Modelo renomeado INCOMPATIBLE, não aprovado. Informar MPN/encapsulamento/montagem; só então definir pads/posição e dissipação.
3. **IEC, PS1 e PE:** código real de J1, dimensões do módulo BL aberto, montagem de J2 e chassis. J2 ainda tem cobre a0,2059 mm da borda, contra regra0,5; não deslocamos um furo de chassis sem desenho mecânico. Persistem conflitos PS1/J1/fixação. Entrada/PE exige arquitetura de proteção, não apenas mover trilhas.
4. **D4/F1/IC6/P1/P2/T1/T3:** códigos completos e desenhos. Ponte KBU selecionada sobre geometria GBU herdada; clipes não confirmados; TO92 depende fabricante/conformação; terminal chamado M6 usa furo2,2; magnetismos sem bobinagem/core/isolação mecânica confirmados. Nenhuma troca de topologia ou componente implícita.
5. **Potência e isolamento:** rede máxima e tolerância (110/127/220), corrente RMS/pico, frequência, duração/repetição dos pulsos, cobre/plating, ambiente/altitude/poluição/CTI/coating, norma e dissipador. Sem isso não fechar isolamento HV, loop de potência, vias e orçamento térmico. Gargalos DC_MID e loops de potência/gate do relatório original permanecem pendentes; não foram declarados dimensionados.
6. Depois dessas decisões: placement definitivo, reroteamento de potência, cleanup de serigrafia, solução dos39 overlaps de courtyard,22 diferenças de biblioteca e demais pendências. Cinco furos sem referência e JPRT1/2 continuam explicando as11 questões de paridade (4 duplicidades +7 extras); não foram escondidos com exclusões.

**Estado final: melhorias locais reais e verificadas, mas layout completo ainda não concluído e não liberado para fabricar/energizar.** O primeiro desbloqueio útil é confirmar os MPNs de C11/C12 e R1 e o envelope mecânico permitido; isso determina o placement, antes de polir trilhas e silk sobre corpos que ainda não cabem.

## Reversibilidade e reprodução

Os commits separam esquema e biblioteca; o commit final salva PCB/evidências. O histórico implementation/*stage*.py, pcb_refine.py e mains_local.py registra etapas intermediárias, NÃO é pipeline idempotente nem deve ser executado novamente sobre a placa final. Algumas etapas intermediárias falharam e seus DRCs ficam para transparência. Fonte de verdade desta entrega: arquivos CAD versionados no commit final + evidence/drc-final.json. O gerador legado scripts/pcb_patch_footprints.py recria os footprints errados e NÃO deve ser usado nesta revisão.

Para repetir sem gerar novamente o projeto: kicad-cli sch export netlist, sch erc, pcb drc --all-track-errors --schematic-parity --severity-all --refill-zones; ver comandos completos e ferramentas no relatório anterior. Não usar geradores build_* para validar.
