# Revisão final minuciosa — arquivos salvos em 18/10/2026

**Resultado: não encontrei curto, ligação faltando ou divergência elétrica esquema–PCB nas verificações realizadas. A fabricação da PCB nua como protótipo continua tecnicamente plausível; isso não equivale à liberação do equipamento para operação em potência.** Há pontos concretos de margem, documentação e montagem descritos abaixo. Nenhum arquivo CAD ativo, regra ou ZIP do Desktop foi alterado nesta auditoria.

## Escopo e evidência

Fontes: `oneTesla.kicad_sch`, `.kicad_pcb`, `.kicad_pro`, `.kicad_dru`, bibliotecas locais, Eagle original em `misc/driver.sch`/`driver.brd`, manual original e datasheets. A versão auditada foi congelada em `input.*`; hashes em `source-hashes.json`. A igualdade dos arquivos ativos com as cópias foi conferida após as verificações.

Executados KiCad CLI 10.0.7 ERC, DRC com refill em memória, todos os erros de trilha e paridade, exportação de netlist, Gerbers e Excellon. Não foi usado `--save-board`. Inspeção de frente/verso com fabricação, máscara e cobre; inventário das 42 referências físicas e de todos os pads, vias e trilhas.

| Verificação | Resultado |
|---|---:|
| Conexões faltando na PCB | 0 |
| Curtos, clearance de cobre, anel PTH, máscara e furação reportados pelas regras atuais | 0 |
| Ocorrências de montagem | 19: 10 courtyards, 7 PTH e 2 NPTH em courtyard |
| Ocorrências de serigrafia | 15: 14 overlaps e 1 borda |
| Paridade | 21: 16 campos descritivos, 3 furos mecânicos extras, 2 referências mecânicas repetidas |
| ERC | 2 erros de modelagem da entrada AC de PS1 e 2 avisos de rótulos local/global |
| Validador independente local | PASS: 20 redes, 7 ligações diretas, 42 referências |

Os 2 ERC de PS1 decorrem de entradas `power_input` alimentadas pelo conector passivo de rede, sem símbolo `power_output`. Não demonstram ausência física da rede AC. Os rótulos GND/+5V foram conferidos pela netlist; não há indicação de domínios duplicados ou separados por esses avisos.

## Achados que merecem ação antes da operação

### F01 — Margem da alimentação dos drivers

IC3/IC4 são UCC37321P ligados diretamente ao rail de PS1 HLK-15M15BL. A TI especifica alimentação recomendada de até **15 V**, com máximo absoluto de **16 V**. A Hi-Link publica **15,0 ±0,3 V** em plena carga e overshoot de chaveamento de até **5%** na condição indicada em seu documento. Portanto a alimentação selecionada não garante permanecer na faixa recomendada em todos os casos. Isso **não prova** que os drivers serão danificados, nem que a soma dos extremos ocorre simultaneamente; mostra ausência de margem garantida.

Antes de liberar operação, definir uma solução de alimentação com margem e verificar o rail nos pinos dos drivers durante partida e bursts. É assunto de projeto/ensaio, não um curto de PCB encontrado pelo DRC.

Fontes: [TI UCC37321, §§7.1/7.3](https://www.ti.com/lit/ds/symlink/ucc37321.pdf), [Hi-Link, saída 15 V](https://www.hlktech.net/index.php?cateid=733&id=1408).

### F02 — Ponte D4 de 400 V no dobrador de 127 V

O CAD especifica **KBU6G**, de **400 V VRRM**. No modo dobrador, os diodos associados à entrada de fase podem bloquear aproximadamente o barramento total: **359 V** em 127 Vac nominal. Num cenário ilustrativo de +10%, o cálculo ideal resulta em **395 V**, antes de transientes. +10% é uma hipótese de análise; não é medição da tomada nem afirmação sobre o limite regulamentar local.

A ponte não está demonstradamente acima do rating em condição nominal, mas a margem é pequena. Recomendo selecionar uma versão de maior tensão, por exemplo KBU6J de 600 V ou KBU6M de 1000 V, conferindo fabricante, pinagem e encapsulamento da peça comprada. A própria família Vishay oferece essas variantes; isso tende a ser uma decisão de componente, sem necessidade de mudar a PCB quando a geometria é a mesma.

Fonte: [Vishay KBU6](https://www.vishay.com/docs/98732/kbu6.pdf).

### F03 — Capacitores de compra e valor ainda escrito no CAD

Os footprints de C11/C12 estão corretos para a geometria escolhida: **Ø30,3 × 40,5 mm, passo 10 mm, quatro furos acabados de Ø2 mm e pads Ø4 mm**. Pad 1 positivo de C12 vai a DC_PLUS; pad 1 positivo de C11 vai a DC_MID. Os negativos vão respectivamente a DC_MID e DC_MINUS.

Os valores do esquema e PCB continuam **1000u 200V**. Isso foi preservado quando o usuário restringiu a alteração apenas ao footprint. Para a compra planejada de **1000µF/250V**, a lista de materiais precisa refletir 250 V, evitando aquisição ou montagem involuntária de 200 V. Essa diferença documental não altera os Gerbers.

C11/C12 têm 30,995 mm entre centros e aproximadamente **0,695 mm entre os corpos nominais**; C11 fica aproximadamente **0,725 mm para dentro da borda direita**. O usuário já confirmou o encaixe em relação a J110/Q1; essa aceitação foi preservada, sem reposicionar peças ou reduzir courtyards. A geometria nominal não inclui tolerância de uma marca ainda não identificada.

### F04 — Furo superior esquerdo sob o envelope de PS1

O furo NPTH em **(37,375;33,05) mm** fica dentro do envelope modelado de PS1, aproximadamente x=31,50…60,00 e y=28,37…75,87 mm. Se houver parafuso, porca ou cabeça acima da PCB nesse furo, a montagem precisa ser confrontada com o módulo real; não se deve presumir que o acesso ao furo estará livre.

O documento local Hi-Link p.11 usa o envelope de referência da versão com caixa, e admite tolerâncias de dimensões e passos. Isso torna o resultado uma interferência confirmada **no envelope CAD**, não prova de colisão com toda variante BL possível. Se o furo não for utilizado, documentar quais pontos realmente sustentam a montagem. Não movi esse furo ou PS1.

### F05 — Desacoplamento e laços de acionamento precisam de ensaio

O esquema tem 1µF SMD e 100µF por região de driver. A TI recomenda desacoplamento cerâmico de 100nF, capacitância maior próxima e conexões curtas de alimentação, terras e saídas. Não há capacitores locais separados de 100nF para ambos os pares de alimentação/terra conforme o exemplo do fabricante. Isso é uma diferença em relação à orientação de layout, não demonstração de oscilação ou falha.

No arquivo atual, a rede IC3 OUT→R4 soma **24,276 mm**, com trechos de **0,5/1 mm**; IC4 OUT→C4 soma **8,141 mm**, de **0,5 mm**. São somas dos segmentos das redes, incluindo ramais, não indutâncias calculadas. A validação precisa observar alimentação e gate–emissor sob as condições de operação. A meia ponte e o GDT não foram validados por simulação dinâmica ou osciloscópio nesta revisão.

Fonte: [TI UCC37321, §§10/11](https://www.ti.com/lit/ds/symlink/ucc37321.pdf).

## Conectividade e pinagens conferidas

- **Entrada AC:** J1.1→F1.1; F1.2→D4.2/PS1.1; J1.2→D4.3/PS1.2/J110.1. PS1 fica depois do fusível. J1 tem somente L/N.
- **PE:** J2.1 pertence a GND do controle e ao -Vo de PS1. Não há união elétrica a DC_MINUS/DC_MID. J2 é PTH Ø3,2 mm/cobre Ø7 mm no furo inferior esquerdo, com ligação de cobre ao plano GND. A continuidade pelo olhal, parafuso e chassis depende do contato metálico real; o DRC não mede resistência mecânica.
- **Fonte/regulador:** PS1.3→GND, PS1.4→+15V; MC7805BDTRKG: IN1, GND2/tab, OUT3 corretos. C9 está sincronizado em 10µF/100V MLCC1210 não polarizado. Dissipação de IC6 depende da carga real.
- **Receptor:** HFBR-2521ETZ: OUT1/GND2/VCC3/RL4 corretos; RL em +5V; retenções 5/8 NC. Passo 2,54 mm e fileiras 7,62 mm conferidos com [Broadcom](https://docs.broadcom.com/doc/AV02-3283EN).
- **Lógica:** cadeia 74HCT14, metade ativa do 74HCT74 e enables mantêm a topologia original. PRE/CLR da metade não usada foram desativados em +5V; saídas não usadas marcadas NC.
- **Drivers:** VDD1/8, IN2, EN3, GND4/5, OUT6/7 corretos; saídas 6/7 de cada driver estão unidas externamente, sem união entre os dois drivers.
- **IGBTs:** G1/C2/E3 coerentes; Q1 coletor em DC_PLUS, emissor em SW_NODE; Q2 coletor em SW_NODE, emissor em DC_MINUS. Gate alto retorna a SW_NODE e gate baixo a DC_MINUS. Fase e isolamento dos enrolamentos de T1 continuam dependentes da peça real.
- **CT/primário:** JCT1.1→SW_NODE; JCT1.2→SW_CT→CPR1.1. Não existe curto reportado entre essas redes. O jumper deve atravessar uma vez o núcleo de T3. T3.1/2 são somente secundário do CT; fase e relação física não são provadas pelo CAD.
- **Tanque:** CPR1.2→P1 e P2→DC_MID. Os valores/topologia do tanque conferem com a referência, mas corrente RMS, dV/dt e regime de bursts não estão dimensionados nesta auditoria.

Comparação direta com o Eagle original: **25 redes de componentes comuns, 22 equivalentes após normalizar renumerações e inversões de passivos**. As outras três refletem as mudanças já documentadas de IC2.10/13, pino RL do novo receptor e separação SW_NODE/SW_CT pelo jumper. A nova fonte e PE também foram conferidos pela netlist completa atual. Detalhes em `original-net-comparison.json` e cobertura das 42 referências em `coverage.csv`.

## Montagem e componentes ainda dependentes de seleção

Z1/Z2 continuam **DNP no esquema e PCB**, como opcionais do original. Seus overlaps não devem ser tratados como colisões da variante sem TVS. Os avisos de JCT1/CPR1 e P1/CPR1 envolvem envelopes dos terminais/fio; o furo inferior direito também invade o courtyard de CPR1. J2/R1 mantém a interferência conservadora de courtyard já documentada, com cerca de 1,22 mm entre corpo nominal de R1 e olhal/arruela Ø7 mm. Nenhum envelope foi apagado para zerar a contagem.

R5/R6 continuam 100kΩ/0,5W em 2512, sem MPN fechado. Em 127 V nominal dobrado cada um dissipa aproximadamente **0,323 W**; no cenário +10%, aproximadamente **0,390 W**. Conferir tensão de trabalho e derating da peça selecionada. C4 de 1µF, em série com o GDT, também precisa de peça adequada à tensão e corrente AC, não apenas valor nominal. T1/T3 mantêm seleção/dimensões/fase a confirmar fisicamente.

Todos os modelos 3D referenciados foram localizados, resolvendo também a variável de biblioteca do KiCad. Modelos genéricos não certificam dimensões da peça comprada.

## Regras, isolamento e fabricação

O projeto ativo mantém Default/mínimo de 0,20 mm e clearance local de 0,6096 mm nas zonas de potência. Esses números têm referência no Eagle original. Não foi aplicada uma distância universal de 3 mm/6,4 mm como critério de reprovação.

Para localizar pontos próximos entre potência e controle, foi executada **somente numa cópia** uma busca DRC com raio de 6,4 mm. Esse número é de triagem, não requisito normativo. A menor separação reportada foi **2,05 mm** entre a trilha SW_NODE em B.Cu, y=124 mm, e T3.1, em (58,75;119,45) mm. O Eagle também passa N$14 perto do secundário do CT. Portanto o resultado não demonstra por si um defeito novo, mas limita qualquer alegação de isolamento garantido para a adaptação. Não houve análise normativa completa de creepage, impulsos, CTI, altitude ou enrolamentos.

A PCB é de duas camadas, contorno geométrico fechado **100 × 100 mm**, stackup configurado de **1,6 mm/35µm**. Há **92 furos/rasgos metalizados**, incluindo quatro Ø2 mm de C11/C12 e um Ø3,2 mm de J2, mais três NPTH Ø3,2 mm. F1 usa dois rasgos metalizados **4,4 × 1,8 mm** no Excellon roteado.

Vias: 14 de Ø0,5/furo0,3 e 7 de Ø0,6/furo0,3 mm. A diferença diâmetro–furo de 0,20 mm das menores está acima do mínimo/preferido publicado pela JLCPCB para vias; não confundir com a regra distinta de anel PTH de componente. Trilhas mínimas de 0,20 mm e slots de 1,8 mm são compatíveis com a capacidade publicada para FR4 de 1oz. Isso é uma conferência básica de fabricação, não aprovação térmica das trilhas de potência. Fonte: [JLCPCB capacidades](https://jlcpcb.com/capabilities/pcb-capabilities).

## ZIP do Desktop

Comparados os Gerbers/Excellon regenerados agora com `/Users/urielcontardi/Desktop/ARCSTRIKE-PCB-prototipo.zip`, desconsiderando carimbos de data:

- **Cobre, máscaras, contorno e furação são iguais.**
- Somente **F.Silkscreen difere**, devido à posição do texto PS1 alterada depois do último commit/exportação.
- O ZIP do Desktop não foi sobrescrito. Arquivos atuais de conferência estão em `gerbers/`; resultado em `desktop-zip-comparison.json`.

## Parecer final

**Não encontrei erro de conectividade que, por si, obrigue refazer a PCB.** A conclusão anterior de protótipo de PCB nua permanece nesse escopo. Para operação em potência, fechar principalmente a margem da fonte dos UCC, o rating de D4, a compra efetiva de capacitores de 250 V, a montagem no furo coberto por PS1 e a seleção/fase dos transformadores. Esta auditoria não homologa isolamento, dissipação ou comportamento dinâmico do conjunto.
