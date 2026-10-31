# ARCSTRIKE — case v4 para protótipo de montagem

Revisão mecânica da case compacta, com encaixes guiados, alojamentos para porcas
sextavadas, cabeças de parafusos e acesso para chave Allen. A plataforma do
primário é modular e vem **sem pentes para fio**. A escolha do condutor está
pendente por instrução do usuário; nenhuma recomendação anterior a fixa nesta revisão.

Corpo 130 × 130 × 96 mm com pés; plataforma Ø180 mm; altura total 416 mm.
A tampa passou de 4 para 6 mm para acomodar cabeças de parafusos rebaixadas.

Abra `ARCSTRIKE-assembly.sc` no SolidCraft ou `exports/case-viewer.html` no navegador.
`exports/ARCSTRIKE-case-v4-ASSEMBLY.step` inclui PCB, dissipador, conector, tubo,
toroide e ferragens em posição de montagem. Os parafusos têm cabeça com encaixe
Allen e haste nominal; as roscas helicoidais são omitidas. As porcas têm sextavado
e furo. **Ferragens, PCB, dissipador, tubo e toroide não são peças para imprimir.**

## Arquivos para imprimir

Use somente os STLs em `exports/print/`. Estão separados, com a orientação de
impressão sugerida aplicada, apoiados em Z=0 e dentro da origem XY positiva.
A fonte continua em coordenadas de montagem para manter referências e verificações.

- `01_lower_tray`: bandeja, apoio do dissipador, dois apoios parafusados da PCB e um pino localizador.
- `02_upper_sleeve`: laterais com encaixe inferior e guia superior.
- `03_C14_inlet_plate`: placa do conector e alojamentos de porcas.
- `04_structural_lid`: tampa de 6 mm, rebaixos das cabeças e porcas M4 da plataforma.
- `05_modular_deck_NO_WIRE_HOLDER`: plataforma circular sem pentes, com furos de acesso aos parafusos da tampa e interface para um holder futuro.
- `06_foot_1` a `06_foot_4`: quatro pés, parafusos rebaixados por baixo.
- `07_secondary_base_clamp`: abraçadeira fendida do tubo, removível da plataforma.
- `08_heatsink_clamp_1` e `_2`: grampos laterais independentes do dissipador.
- `09_pcb_washer_1` e `_2`: arruelas não condutoras de 0,6 mm; podem ser substituídas por arruelas equivalentes com a mesma espessura e envelope.
- `10_secondary_top_clamp`: abraçadeira superior, flange com porcas carregadas radialmente.
- `11_topload_pedestal`: tampa e pedestal do toroide, com passagem M4 e passagem de 3 mm para o fio superior do secundário.
- `90...93_coupon_*`: quatro cupons de encaixe; imprimir antes das peças grandes.

As abraçadeiras do tubo usam furos de Ø60,6 mm e uma fenda nominal de 2 mm para
ajuste por aperto. São dimensionadas para tubo Ø60 mm; o tubo real deve passar
pelo cupom `93_coupon_tube_60p6`. O CAD assume parede de 1,5 mm.

## Encaixes e ferragens

Bandeja/laterais e laterais/tampa usam língua de 1,6 mm de altura e 1,8 mm de
espessura, com folga lateral de 0,25 mm e folga axial de aproximadamente 0,3 mm.
Os encaixes alinham as peças; os parafusos fornecem a retenção.

Passagens M3: Ø3,4 mm; porcas DIN 934 M3: alojamento AF5,8 × 2,6 mm.
Passagens M4: Ø4,5 mm; porcas DIN 934 M4: alojamento AF7,4 × 3,5 mm.
Usar porcas sextavadas comuns, sem flange e sem trava de nylon; essas versões
possuem outro envelope. As porcas entram por baixo ou por canais laterais
acessíveis na sequência abaixo. O projeto não depende de inserts ou rosca
impressa. Comprar parafusos Allen de cabeça cilíndrica DIN 912/ISO 4762.

Quantidades e comprimentos exatos: `exports/hardware-BOM.csv`, gerado da mesma
lista de ferragens representadas no 3D. Não substituir por parafusos mais longos:
a folga junto à PCB, conector e dissipador é limitada. Chaves Allen de 2,5 mm
para M3 e de 3 mm para M4. Aperto leve no plástico; torque não foi qualificado.

## Sequência de montagem

1. Imprimir os quatro cupons. Conferir as porcas e parafusos reais e o tubo.
   Encaixar o cupom macho no canal do cupom fêmea, virando uma das peças.
   Se não houver encaixe deslizante sem força, ajustar compensação dimensional
   no slicer ou parâmetros antes de imprimir as peças grandes.
2. Imprimir e limpar as peças. Remover suportes e rebarbas dos canais de porcas,
   furos e guias; os alojamentos devem aceitar as porcas sem deformar a peça.
3. Inserir nas laterais internas da bandeja as porcas dos pés e da emenda.
   Instalar quatro pés com M3×8 a partir de baixo. As cabeças ficam rebaixadas.
4. Inserir as duas porcas dos grampos do dissipador antes de colocá-lo. Assentar
   as aletas nos dois trilhos de fundo e nos localizadores. Colocar os grampos
   nas posições distintas esquerda/direita e prender com dois M3×10.
   Os grampos retêm o dissipador no gabinete e não substituem a montagem térmica
   e os isoladores necessários entre dissipador e IGBTs.
5. Colocar as duas porcas dos apoios da PCB. Assentar a placa no pino de Ø2,8 mm
   no ponto (6,94) e nos apoios de (94,94) e (94,6). Usar duas arruelas de 0,6 mm
   e dois M3×6. O pino termina em Z=1,2 mm dentro do furo: o componente HLK do
   STEP cobre esse ponto a partir de Z=2,095 mm e impede cabeça/porca por cima.
   O ponto (6,6) permanece disponível para PE, sem fixador plástico.
6. Pré-montar o C14 na placa adaptadora: duas porcas nos alojamentos traseiros
   e dois M3×10 a partir da face externa do C14. Inserir quatro porcas na parede
   traseira das laterais e montar o adaptador com quatro M3×10, também por fora.
   Fazer as conexões elétricas próprias do projeto antes de fechar as laterais.
7. Assentar as laterais na língua da bandeja, alinhando o acesso da fibra.
   Instalar os quatro M3×10 da emenda, acessíveis pelo topo nos cantos internos.
   Inserir as quatro porcas superiores das laterais em seus canais internos.
8. Pré-montar o módulo superior: colocar quatro porcas M3 por baixo da plataforma
   nos furos diagonais a raio de 40 mm. Fixar a abraçadeira inferior com quatro
   M3×8. Deixar o M3×16 transversal e sua porca frouxos para receber o tubo.
9. Colocar quatro porcas M4 por baixo da tampa. Unir tampa e plataforma com quatro
   M4×10. Levar o conjunto ao gabinete e encaixar a guia superior das laterais.
   Fixar a tampa com quatro M3×10, passando a chave e as cabeças pelos furos de
   Ø7 mm da plataforma. Assim, a plataforma não bloqueia o acesso aos parafusos.
10. Inserir o tubo pela abraçadeira inferior e pela plataforma até assentar na
    tampa. Apertar gradualmente o M3×16 transversal; não esmagar o tubo nem
    forçar o fechamento completo da fenda.
11. Pré-montar o topo fora do tubo: quatro porcas M3 entram pelos canais radiais
    da flange da abraçadeira superior; prender o pedestal com quatro M3×8.
    Passar M4×30 e uma arruela 4,3×9×0,8 mm por baixo do pedestal. Assentar o
    toroide no pedestal e prender por cima com outra arruela e porca M4.
    O disco central do toroide precisa de furo passante Ø4,5 mm; se não existir,
    é necessário fazê-lo no disco metálico real. Não furar a parte curva por este guia.
12. Assentar o módulo superior no tubo e apertar seu M3×16 transversal. O colar
    ocupa os 22 mm superiores sem enrolamento. Rotear o terminal superior pela
    passagem prevista e conectá-lo ao ponto condutor apropriado do toroide.
    A conexão elétrica e sua isolação não são verificadas pelo desenho mecânico.

O tubo e a PCB não precisam ser furados para essas fixações da case. O conector,
dissipador e tubo precisam coincidir com os modelos de referência. Para manutenção,
retirar primeiro o conjunto do secundário/toroide e os fixadores da tampa;
a sequência inversa dá acesso aos parafusos das laterais e à eletrônica.

## Plataforma do primário: decisão pendente

A plataforma reserva quatro furos M3 em raio de 75 mm nos eixos X/Y, com
alojamentos de porca por baixo. Esses quatro pontos são a interface do holder
futuro; os parafusos e porcas desse holder não entram na BOM desta revisão.
A passagem do primário para a caixa tem dois furos de Ø6 mm em (34,20)/(66,20).
A geometria do fio e dos pentes foi retirada da montagem para não congelar uma
bitola. Também não foram criadas ferragens em laço ao redor do secundário.

## Impressão e limites de validação

Sugestão inicial para protótipo de encaixe: bico 0,4 mm, camada 0,2 mm, quatro
perímetros e 30–40% de preenchimento. Nas abraçadeiras e grampos, seis perímetros
com mais preenchimento. PETG permite testar encaixes; adequação térmica do
material perto do dissipador/primário requer medição, e PLA não é uma liberação
para operação. As arruelas de 0,6 mm requerem três camadas de 0,2 mm.

Orientações dos STLs já estão aplicadas. Bandeja: fundo no leito, com suportes
locais sob os apoios internos da PCB. Laterais: na vertical. Plataforma e tampa:
face com alojamentos de porca voltada para cima; usar suportes removíveis nos
rebaixos e guias quando indicado pelo slicer. Placa C14: deitada, com suportes
sob saliências traseiras. Abraçadeira superior: flange no leito, corpo voltado
para cima. Pedestal: disco no leito e pilar para cima. Verificar pontes nas
janelas de porcas e acesso para remoção de suportes antes de fatiar.

A verificação final passou em 4.740 testes de interseção, 698 testes do envelope
local da chave Allen e 37 verificações de engajamento nominal das porcas.
`tool-access-verification.json` usa envelope de 25 mm junto às cabeças, com
pré-montagem do topo antes de instalar o toroide. O comprimento total de uma
ferramenta específica e tolerâncias de rosca não são simulados.

`verification.json` registra válidos sólidos únicos por peça, interseções entre
peças impressas, referências e ferragens, além de ferragens entre si. O limite
é 0,02 mm³. Folgas, acesso e ordem de montagem foram definidos no CAD; não houve
impressão física, teste de torque/carga, ensaio térmico ou de isolação.
O posicionamento e os pinos dos IGBTs no STEP de origem são provisórios; sua
montagem térmica elétrica continua sujeita às peças reais. Isso não impede o
protótipo de encaixe da case, mas impede declarar o equipamento pronto para energizar.

## Fontes e reconstrução

Fonte paramétrica: `build.py`, `reference_geometry.py`, `parameters.json`.
A montagem `.sc` é uma importação do STEP, não uma timeline nativa de todas as peças.

```sh
uv run --with cadquery python mechanical/case-v4/build.py
uv run --with cadquery python mechanical/case-v4/build_fit_coupons.py
/Applications/SolidCraft.app/Contents/MacOS/solidcraft-cli bench-open mechanical/case-v4/exports/ARCSTRIKE-case-v4-ASSEMBLY.step --save mechanical/case-v4/ARCSTRIKE-assembly.sc
```

Dimensões de referência para ferragens:
[DIN 912 M3](https://www.accu.co.uk/metric-cap-head-screws/250416-SSCF-M3-8-A2-R360),
[DIN 934 M4](https://www.accu.co.uk/hexagon-nuts/7890-HPN-M4-A2).
As compras não precisam ser desses fornecedores; conferir o envelope dimensional.
