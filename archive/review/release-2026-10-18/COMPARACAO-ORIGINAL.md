# Comparação com o oneTeslaTS original

Fontes examinadas diretamente: `misc/driver.sch`, `misc/driver.brd`, `misc/schematic_ref.png`, `misc/layout_ref.png`, página 49 renderizada do manual e texto das etapas 6/7 e lista de peças do manual. Projeto atual preservado.

## Conectividade

`compare_original.py` lê o XML Eagle, resolve gate/pino para pad físico e compara com a netlist atual exportada nativamente. `net-comparison.json` registra o resultado. A comparação é restrita aos componentes comuns listados no script; não cobre integralmente a nova fonte ou os conectores. Normaliza inversões de componentes passivos e os dois AC intercambiáveis da ponte. Não verifica fases magnéticas.

Das 25 redes não vazias comparadas, 22 têm exatamente os mesmos conjuntos de pinos selecionados após a normalização. As três diferenças são explicáveis:

- IC2.10/13: GND no original, +5V no atual. São PRE/CLR ativos em nível baixo da metade não utilizada. A alteração evita manter ambas as entradas assíncronas ativas; não modifica a metade usada no controle. IC2.11/12 continuam em GND e saídas sem uso.
- FB1.4 ligado a +5V no atual. O original usa receptor de três terminais IF-D95; o HFBR-2521ETZ atual tem pino adicional RL. A troca exige a pinagem específica do receptor, não copiar o footprint original.
- CPR1.1 deixa SW_NODE e passa a SW_CT, com JCT1 entre as redes. Isso representa explicitamente o fio pelo núcleo de T3. No Eagle ambos pads do jumper pertencem nominalmente ao mesmo sinal N$14; a passagem física pelo CT é exigida no manual, página 21 do PDF.

Não apareceu inversão de conectividade no núcleo funcional comparado: clamps do CT, cadeia Schmitt, flip-flop ativo, enables, saídas dos dois drivers, primário de T1, conexões gate/emissor e barramento. Isso não comprova fase do transformador real nem comportamento transitório.

## O que muda na interpretação do DRC

- O Eagle tem classe default, afastamentos gerais de 8 mil (0,2032 mm), e zonas POS/NEG/N$14 com isolate de 24 mil (0,6096 mm). Portanto os 0,20/0,6096 mm atuais têm origem concreta. Não encontrei requisito original de 3 mm universal ou 6,4 mm universal. Sua ausência, isoladamente, não demonstra erro de cópia.
- POS em Bottom e NEG em Top já são do original. DC_MID como zona adicional e o novo posicionamento são adaptações.
- Z1/Z2 são opcionais e não fornecidos no kit (manual, PDF página 22). Ambos estão DNP no esquema E na PCB atual, confirmado diretamente nos arquivos. Os avisos envolvendo seus corpos não impedem a montagem da variante sem TVS. Não apagar footprints nem courtyards para mascarar o resultado.
- Q1/Q2 foram concebidos para montagem com pernas dobradas, presos ao dissipador e isolados por sil-pad (manual, PDF página 23). Courtyard convencional sozinho não decide colisão nesse arranjo. É necessário conferir o conjunto mecânico real, principalmente porque a placa foi reposicionada/reduzida.

## Mudanças que precisam de validação própria

1. **Fonte:** original T2 → D3 → aproximadamente +24V → reguladores 15V/5V; atual HLK de 15V → drivers e 7805. O fusível agora também protege a derivação do HLK. A topologia faz sentido, mas margem da alimentação dos drivers, ruído, desacoplamento e capacidade térmica do 7805 dependem das peças e carga reais. Não transportar o problema térmico do 78L05 original diretamente para o DPAK atual.
2. **PE:** original liga explicitamente IEC.G a GND no esquema e na PCB. A adaptação separou GND lógico e PE e removeu o IEC. Isso é uma alteração de arquitetura, não simples renomeação. J2 continua apenas no esquema. Definir conexão real de chassis/PE e a referência desejada do controle; não unir PE a GND automaticamente para imitar o original, nem presumir que os furos NPTH realizam essa função.
3. **C9:** leitura direta atual: esquema **100u 35V / CP_Elec_8x10**, PCB **10u 100V / C_1210_3225Metric**. O original tem C9 eletrolítico no rail de 5V; `driver.sch` não define seu valor. A comparação histórica não determina qual peça atual deve prevalecer. Resolver a divergência antes de BOM/montagem. Corrige a descrição invertida/incompleta do primeiro relatório.
4. **R5/R6 SMD:** cada resistor de 100k dissipa aproximadamente 0,324W a 180V e 0,392W a 198V. O valor/potência nominal de 0,5W vem do original, mas MPN, tensão de trabalho e derating do 2512 atual ainda precisam fechar; potência nominal sozinha não qualifica a substituição.
5. **127V versus 110V:** o manual manda fechar J110 em 110V e omiti-lo em 220V. Não especifica operação irrestrita em 127V. A hipótese de 127V +10% resulta em cerca de 198V por capacitor ideal de 200V; esse risco não é resolvido pela referência ao kit de 110V. O original consultado não confirma rating de 200V para os capacitores atuais.
6. **Mecânica:** continuam dependentes de medidas reais os conjuntos PS1/furo, R1/furo, CPR1/furo/terminais e J110/C11/C12. JCT1 foi acrescentado para recuperar a função física do jumper original. Conferir fio passando uma vez no CT e a fase de realimentação.

## Parecer revisado

O núcleo do esquema é coerente com o oneTeslaTS na comparação realizada. Não há base para condenar os afastamentos ou todos os overlaps apenas por contagem DRC. A referência original reduz parte das suspeitas, especialmente TVS DNP e montagem dos IGBTs.

Ainda não liberar esta adaptação: fechar C9, arquitetura PE/GND/chassis, faixa de rede e margem dos capacitores, qualificação das peças SMD e interferências mecânicas da nova placa. Os 18 apontamentos geométricos não são 18 colisões físicas comprovadas. O DRC atual com zero desconexões valida continuidade sob suas regras, não as modificações mecânicas/elétricas acima. Não foram feitos ensaios, análise normativa completa ou aprovação de Gerbers.
