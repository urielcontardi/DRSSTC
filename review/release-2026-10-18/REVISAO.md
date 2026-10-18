# Revisão para fabricação — 18/10/2026

Parecer: **não liberar a fabricação nesta revisão**.

Fontes: oneTesla.kicad_sch, oneTesla.kicad_pcb, projeto e regras da raiz. Nenhuma alteração nos arquivos CAD. Relatórios antigos foram usados como contexto, não como resultado atual.

Executado KiCad CLI nativo com `pcb drc --refill-zones --all-track-errors --schematic-parity --severity-all --format json` (sem salvar a placa) e `sch erc --severity-all --format json`. Evidências: drc.json e erc.json nesta pasta.

## Resultado atual

- Zero itens desconectados; nenhum curto ou violação de clearance reportado pelas regras atuais.
- 18 erros geométricos: 11 sobreposições de courtyard, 5 PTH e 2 NPTH em courtyard de outra peça.
- 26 avisos de paridade. Muitos são campos descritivos ou furos mecânicos, mas C9 e J2 exigem resolução funcional/documental.
- ERC: 2 erros de alimentação não dirigida nos terminais AC de PS1 e 3 avisos (+5V/GND local/global e PE isolado). Os erros de PS1 são compatíveis com a modelagem da entrada de rede; não demonstram, por si, falha da alimentação real.

## Bloqueios para liberação

1. **Isolamento não validado:** clearance Default e mínimo global de 0,20 mm; zonas de potência com afastamento local de 0,6096 mm. O .kicad_dru contém somente regra de anel PTH. Não há regra específica de isolamento potência–controle ou creepage por tensão. Reproduzir distâncias do Eagle não comprova isolamento nesta adaptação. Definir tensão máxima, transientes, material/ambiente e critérios por domínio; conferir distâncias reais, transformadores e ferragens. Referência conceitual: https://www.analog.com/en/resources/technical-articles/comparative-tracking-index-and-working-voltage.html
2. **PE/chassis:** J2 existe no esquema, mas falta na PCB segundo a paridade. Definir e documentar o ponto real de conexão externa ao chassis; não interpretar os furos REF** como aterramento de proteção.
3. **C9 inconsistente:** esquema pede 10u 100V, mas aponta para CP_Elec_8x10; PCB usa C_1210_3225Metric e valor textual C9. Escolher a peça final e sincronizar valor, footprint e documentação antes de gerar BOM/montagem.
4. **Montagem:** revisar Q1/Z1, Q2/Z2, Z1/Z2, J110/C11/C12, JCT1/CPR1, P1/CPR1, PS1/furo superior esquerdo, R1/furo inferior esquerdo e CPR1/furo inferior direito. Courtyard sobreposto não prova colisão de corpos: validar peças, terminais dobrados, fio e acesso de ferramentas. Z1/Z2 opcionais podem reduzir conflitos quando ausentes, mas isso precisa constar da configuração de montagem.
5. **Peças provisórias:** T1/T3 e outros footprints continuam CONFIRMAR/ReviewPending. C11/C12 têm corpo nominal Ø25 × 45 mm, mas passo de 10,16 mm ainda provisório. C8/C10/C13 usam envelope genérico. Conferir peças físicas, passo, diâmetro dos terminais e envelopes de dissipador/isoladores.
6. **Margem do barramento:** para a hipótese de rede 127 Vac em dobrador, cada capacitor recebe idealmente aproximadamente 127√2 = 180 V; com +10%, aproximadamente 198 V. C11/C12 são de 200 V: quase nenhuma margem nessa hipótese, antes de desequilíbrio e transientes. Confirmar faixa real de alimentação e rever ratings. J110 fechado em 220 Vac daria aproximadamente 622 V no barramento ideal: seleção deve ser inequívoca.
7. **Potência e acionamento:** faltam dados finais de corrente RMS/pico, bursts e cobre para aprovação térmica. Confirmar fase e isolamento de T1/T3. JCT1 deve atravessar uma vez o núcleo de T3; conectividade CAD não verifica isso. Revisar desacoplamento e retorno dos UCC37321 conforme datasheet, incluindo ambos pares de alimentação/terra: https://www.ti.com/lit/ds/symlink/ucc37321.pdf

## Condição de fechamento

Resolver C9 e PE, validar montagem com peças reais, fechar critérios elétricos/térmicos e ajustar layout onde necessário. Repetir ERC/DRC/paridade e inspecionar Gerbers, máscara, contorno e arquivos de furação finais. Nenhum pacote Gerber foi gerado ou aprovado nesta revisão. Esta auditoria CAD não substitui validação funcional, térmica ou de isolamento em bancada.
