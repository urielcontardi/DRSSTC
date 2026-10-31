# ARCSTRIKE — case v5 para protótipo de montagem

Revisão mecânica da case compacta, agora com berço de dissipador ajustável, com encaixes guiados, alojamentos para porcas
sextavadas, cabeças de parafusos e acesso para chave Allen. A plataforma do
primário é modular e vem **sem pentes para fio**. A escolha do condutor está
pendente por instrução do usuário; nenhuma recomendação anterior a fixa nesta revisão.

Corpo 140 × 140 × 104 mm com pés; plataforma Ø180 mm; altura total 424 mm.
A tampa passou de 4 para 6 mm para acomodar cabeças de parafusos rebaixadas.

Abra `ARCSTRIKE-assembly.sc` no SolidCraft ou `exports/case-viewer.html` no navegador.
`exports/ARCSTRIKE-case-v5-ASSEMBLY.step` inclui PCB, dissipador, conector, tubo,
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
- `08_adjustable_heatsink_finger_1` a `_4`: quatro presilhas com rasgos de regulagem e batentes laterais.
- `12_shim_4mm_*` e `12_shim_1mm_*`: quatro pilhas iguais de calços, para a altura nominal de 25 mm.
- `13_universal_heatsink_cradle`: berço removível com duas travessas cruzadas.
- `spare-shims/`: calços alternativos de 0,5 / 1 / 2 / 4 / 8 mm, para outras alturas.
- `09_pcb_washer_1` e `_2`: arruelas não condutoras de 0,6 mm; podem ser substituídas por arruelas equivalentes com a mesma espessura e envelope.
- `10_secondary_top_clamp`: abraçadeira superior, flange com porcas carregadas radialmente.
- `11_topload_pedestal`: tampa e pedestal do toroide, com passagem M4 e passagem de 3 mm para o fio superior do secundário.
- `90...93_coupon_*`: cupons dos encaixes, porcas e tubo.
- `94_fiber_access_sample`: amostra da porta de fibra com o mesmo rebaixo e anteparo da case; conferir o plugue real antes das peças grandes.

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

1. Imprimir os cupons e a amostra do acesso à fibra. Conferir as porcas e parafusos reais e o tubo.
   Encaixar o cupom macho no canal do cupom fêmea, virando uma das peças.
   Se não houver encaixe deslizante sem força, ajustar compensação dimensional
   no slicer ou parâmetros antes de imprimir as peças grandes.
2. Imprimir e limpar as peças. Remover suportes e rebarbas dos canais de porcas,
   furos e guias; os alojamentos devem aceitar as porcas sem deformar a peça.
3. Inserir nas laterais internas da bandeja as porcas dos pés e da emenda.
   Instalar quatro pés com M3×8 a partir de baixo. As cabeças ficam rebaixadas.
4. Inserir quatro porcas dos apoios do berço e quatro porcas das presilhas.
   Empilhar 4+1 mm de calços em cada apoio, para o dissipador de 25 mm de altura.
   Colocar o berço e prender com quatro M3×14, com cabeças rebaixadas. Assentar
   as aletas para baixo sobre as travessas e deixar a face plana voltada para
   os IGBTs. Colocar as quatro presilhas nas posições do modelo, introduzir seus
   M3×10 e ajustar os rasgos para os batentes ficarem próximos às bordas reais.
   Apertar alternadamente e sem esmagar as aletas. Não há furos no dissipador.
   O berço não precisa coincidir com o passo das aletas. Para outras alturas,
   usar a tabela abaixo; os quatro apoios sempre recebem pilhas iguais.
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

A revisão passou em 7.247 testes de interseção, 359 testes de regulagem,
1.269 testes do acesso local da chave, quatro testes de passagem/acesso da fibra
e 43 verificações de engajamento nominal de porcas.
`tool-access-verification.json` usa envelope de 25 mm junto às cabeças, com
pré-montagem do topo antes de instalar o toroide. O comprimento total de uma
ferramenta específica e tolerâncias de rosca não são simulados.

`verification.json` registra válidos sólidos únicos por peça, interseções entre
peças impressas, referências e ferragens, além de ferragens entre si. O limite
é 0,02 mm³. Folgas, acesso e ordem de montagem foram definidos no CAD; não houve
impressão física, teste de torque/carga, ensaio térmico ou de isolação.
O posicionamento e os pinos dos IGBTs no STEP de origem são provisórios; sua
montagem térmica e elétrica continua sujeita às peças reais. Isso não impede o
protótipo de encaixe da case, mas impede declarar o equipamento pronto para energizar.

## Fontes e reconstrução

Fonte paramétrica: `build.py`, `reference_geometry.py`, `parameters.json`.
A montagem `.sc` é uma importação do STEP, não uma timeline nativa de todas as peças.

```sh
uv run --with cadquery python mechanical/case-v5/build.py
uv run --with cadquery python mechanical/case-v5/build_fit_coupons.py
uv run --with cadquery python mechanical/case-v5/build_spare_shims.py
uv run --with cadquery python mechanical/case-v5/build_port_sample.py
uv run --with cadquery python mechanical/case-v5/verify_adjustments.py
uv run --with cadquery python mechanical/case-v5/verify_access.py
uv run --with cadquery python mechanical/case-v5/verify_fiber_access.py
/Applications/SolidCraft.app/Contents/MacOS/solidcraft-cli bench-open mechanical/case-v5/exports/ARCSTRIKE-case-v5-ASSEMBLY.step --save mechanical/case-v5/ARCSTRIKE-assembly.sc
```

Dimensões de referência para ferragens:
[DIN 912 M3](https://www.accu.co.uk/metric-cap-head-screws/250416-SSCF-M3-8-A2-R360),
[DIN 934 M4](https://www.accu.co.uk/hexagon-nuts/7890-HPN-M4-A2).
As compras não precisam ser desses fornecedores; conferir o envelope dimensional.

## Dissipador: desenho de referência e regulagem

A imagem fornecida está em `reference/heatsink-profile-user.png`. O novo modelo
usa largura de 104 mm, comprimento de 100 mm, altura de 25 mm, base de 5 mm,
13 aletas de 1,6 mm e passo de 8 mm, com centro das aletas externas a 4 mm da
borda e chanfros laterais de 1,5×45°. O arredondamento R0,8 no topo das aletas
aproxima o desenho: não foi fornecido raio cotado nem CAD do fabricante.

O suporte continua independente desse perfil: duas travessas cruzadas recebem
as pontas das aletas; quatro presilhas regulam as bordas externas da base.
Nenhum dente, rasgo ou furo de fixação precisa coincidir com uma aleta.
A caixa aumentou 10 mm de largura/comprimento e 8 mm de altura para deixar
espaço à regulagem, mantendo a plataforma superior de Ø180 mm.

A faixa mecânica reservada é 96–112 mm nos eixos X/Y e 20–30 mm de altura.
A face térmica deve cobrir os IGBTs reais e ser plana; encaixar na faixa mecânica
não estabelece essa cobertura nem eficiência térmica. Pequenos trechos das
presilhas podem se projetar até 3 mm pelos rasgos laterais nos ajustes extremos.
Há batentes de 1,2 mm de espessura e 2 mm de profundidade junto às bordas.
Não apertar uma presilha sobre soldas, terminais ou uma aleta isolada.

Ajustar o berço para manter a face superior do metal em Z=-5,305 mm:

**Altura da pilha de calços = 30 mm − altura real do dissipador.**

| Altura real do dissipador | Pilha em cada um dos 4 apoios | Parafusos do berço |
| --- | --- | --- |
| 30 mm | sem calço | 4 × M3×8 |
| 28 mm | 2 mm | 4 × M3×10 |
| 26 mm | 4 mm | 4 × M3×12 |
| 25 mm | 4+1 mm | 4 × M3×14, incluídos na BOM nominal |
| 24 mm | 4+2 mm | 4 × M3×14 |
| 22 mm | 8 mm | 4 × M3×16 |
| 20 mm | 8+2 mm | 4 × M3×18 |

Os calços alternativos ficam em `print/spare-shims/`. Imprimir quatro unidades
de cada espessura usada em uma camada da pilha. A versão de 0,5 mm exige uma
altura de camada compatível, por exemplo 0,25 mm. A BOM do modelo corresponde
à pilha nominal de 5 mm. Se mudar a altura, mudar também os quatro parafusos
conforme a tabela e conferir a folga da ponta em relação ao fundo/pés.
A escolha fina dos calços depende da medida real e do ajuste físico, não só da
altura aproximada do anúncio. Não forçar a placa para compensar erro de altura.

## Fibra: acesso para inserir e soltar o conector

A abertura externa passa a 32 × 28,8 mm, com cantos arredondados e um rebaixo
até a frente do receptor. Um pequeno túnel com anteparo traseiro cerca a região
do receptor e limita acesso lateral ao restante da PCB. O anteparo tem abertura
18 × 17 mm; não é um adaptador óptico nem um mecanismo de trava impresso.
A conexão continua diretamente no HFBR da placa, sem extensão óptica ou mudança
na PCB. O receptor fica aproximadamente 13,7 mm recuado em relação à parede
externa; a boca larga permite aproximar os dedos e pressionar a alavanca do plugue.
As janelas de ventilação esquerdas foram afastadas dessa porta.

A amostra `94_fiber_access_sample.stl` permite conferir o plugue, a trava e a
pegada antes de imprimir a bandeja/laterais. A peça inclui a profundidade real
da porta e o anteparo, em orientação de impressão com a boca sobre o leito.
O plugue real não foi fornecido. Os testes de passagem usam volumes de reserva,
não equivalem a uma verificação com CAD do conector específico.

Para conectores HFBR-4503Z/4513Z, pressionar a parte traseira da alavanca antes
de puxar o corpo. Em conectores sem trava, puxar o corpo com cuidado. Evitar
puxar pelo cabo ou forçar uma dobra de 90° na saída. A Broadcom especifica raio
mínimo de 35 mm para curvatura de longo prazo do cabo POF dessa família;
consultar o cabo efetivamente usado se for outro modelo.
[Conectores e cabo Versatile Link — Broadcom](https://docs.broadcom.com/doc/AV02-1508EN).

## Pasta simplificada de impressão

Na raiz do repositório, `PARA-IMPRIMIR/` contém somente 14 modelos diferentes
necessários à montagem nominal, com as quantidades nos nomes. São 27 peças
físicas contando as repetições. `ARCSTRIKE-case-v5-PRINT.zip` contém essa pasta,
sem cupons nem calços alternativos. O pacote ASSEMBLY conserva os arquivos
completos, alternativas e cupons.

Os 37 STLs completos passaram na checagem de malha fechada, componente único,
orientação das faces e apoio em Z=0. O relatório é `exports/stl-verification.json`.
