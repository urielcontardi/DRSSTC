# oneTeslaTS — esquemático da placa principal

Abra `oneTesla.kicad_pro` no KiCad 10 e depois o editor de esquemas, ou abra diretamente `oneTesla.kicad_sch`. A folha A3 contém a placa principal completa, organizada em cinco blocos compactos. Os capacitores de desacoplamento ficam junto aos respectivos CIs; referências e valores usam fonte de 1,27 mm, espaçamento de 2,54 mm e alinhamento consistente. Os valores visíveis foram abreviados (por exemplo, `3R3`, `1u` e `100u 25V`); encapsulamentos e observações de montagem permanecem nos campos dos componentes. O UCC37321P usa um bloco retangular com entradas à esquerda, saídas à direita e alimentação/terra acima e abaixo. Para visualizar sem o KiCad, use `output/oneTesla-schematic.pdf`.

O esquema tem 41 referências físicas: IC1–IC4, IC6, FB1, T1, T3, R1–R6, C1–C6, C8–C13, CPR1, D1, D2, D4, Q1–Q2, Z1–Z2, F1, J110, J1, J2, P1, P2 e PS1. A fonte auxiliar original com transformador (T2 + D3 + IC5/78L15 + C7) foi substituída pelo módulo AC/DC **PS1 (HLK-15M15BL, 15V/1A)**, com C13 na saída de 15V; C10 passou a filtrar o rail de 15V e IC6 (78L05) é alimentado por +15V. Z1/Z2 são TVS opcionais, marcados como DNP. J1 corresponde ao J_AC do original; o nome foi adaptado para a anotação do KiCad. J2 representa explicitamente a ligação de proteção PE/chassis que aparece no layout. A placa do SD interrupter externo não faz parte desta etapa. O layout do PCB está documentado na seção **PCB** abaixo.

Todos os símbolos e footprints usados são locais, em `library/oneTesla.kicad_sym` e `library/oneTesla.pretty`. Não é preciso instalar bibliotecas adicionais. Os arquivos SOP existentes foram preservados; IC1 e IC2 foram associados a DIP-14 com soquete, e IC3/IC4 a DIP-8 com soquete, conforme o manual e o layout.

## Referências e decisões

- `misc/schematic_ref.png`: conexões do CT, diodas de proteção, Schmitt triggers, flip-flop, drivers, GDT e meia ponte.
- `misc/layout_ref.png`: encapsulamentos, referências, alimentação e componentes que não aparecem na imagem parcial do esquema.
- `misc/oneTeslaTS_User_Manual.pdf`, páginas 17–23 do arquivo, etapas 4–7: valores, orientação de montagem, alimentação e TVS opcionais. A página 48 identifica o FGA60N65SMD.
- `misc/oneTeslaTS_Parts.pdf`: quantidades, R1 de 1k/5W, resistores bleeder de 100k/0,5W e fusível de 4A. A serigrafia antiga cita 10A; o esquema usa os 4A da lista do kit.
- [TI UCC37321, SLUS504I](https://www.ti.com/lit/ds/symlink/ucc37321.pdf): alimentação 1/8, terra 4/5, enable 3 e saídas 6/7. Os pinos 6/7 foram ligados externamente. O pino 7 mantém o tipo `output`; o 6 é `passive`, pois ambos são pernas da mesma saída. Isso permite ERC sem desabilitar a regra de curtos entre saídas distintas.
- [onsemi FGA60N65SMD](https://www.onsemi.com/pdf/datasheet/fga60n65smd-d.pdf): TO-3P, G1/C2/E3. Footprint horizontal, aba para baixo, passo 5,45mm.
- [Broadcom HFBR-0500ETZ, AV02-3283EN](https://docs.broadcom.com/doc/AV02-3283EN): selecionado HFBR-2521ETZ com OUT1/GND2/VCC3/RL4. RL está em +5V para usar o pull-up interno. Os pinos de retenção 5/8 estão NC conforme essa variante. A cópia local do footprint corrige a numeração do segundo pino de retenção de 6 para 8.

A fonte auxiliar era, na placa original, T2 -> D3 -> C10 -> RAW_DC (+24V), com IC5 (78L15) gerando +15V e IC6 (78L05) gerando +5V. Nesta revisão ela usa o módulo **HLK-15M15BL**: rede AC (pós-fusível, /AC_L_FUSED e /AC_N) -> PS1 -> +15V (C13/C10) -> IC6 (78L05) -> +5V. O rail RAW_DC e o regulador de 15V deixaram de existir.

J110 liga AC_N a DC_MID: fechado para a configuração dobradora de 110V, aberto para 220V. O módulo HLK aceita 85–265VAC, então a mesma placa atende ambas as tensões de rede. A derivação para PS1 fica depois do fusível (topologia /AC_L -> F1 -> /AC_L_FUSED), diferente da placa original, onde o fusível vinha depois da derivação para T2.

GND da fonte isolada, DC_MINUS do barramento de potência e PE são três redes distintas. P1/P2 recebem a bobina primária externa, em série com CPR1 de 68nF/3kV. O fio do primário atravessa o núcleo de T3; os dois pads de T3 são apenas o secundário do CT.

T1 tem pontos de fase nos pinos **1, 3 e 6**: os dois secundários devem gerar tensões gate/emitter opostas. A numeração física e os pares de enrolamentos ainda devem ser confirmados no transformador real. O ERC não verifica polaridade magnética.

## Footprints e pendências

Cada componente tem os campos `Footprint_Status` e, quando necessário, `Assembly_Notes`. A lista completa está em `output/components.csv`.

| Componentes | Situação |
| --- | --- |
| IC1/IC2 | DIP-14, fileiras 7,62mm e passo 2,54mm; soquete conforme original. |
| IC3/IC4 | UCC37321P em DIP-8, fileiras 7,62mm e passo 2,54mm; soquete conforme original. |
| Q1/Q2 | TO-3P-3 horizontal, passo 5,45mm e pinagem do FGA60N65SMD; conferir altura das pernas dobradas em relação ao dissipador. |
| D1/D2 | 1N4148 DO-35 THT; passo selecionado 7,62mm. |
| IC5/IC6 | 78L15/78L05 TO-92, OUT1/GND2/IN3; conferir fabricante/sufixo antes de comprar. |
| FB1 | HFBR-2521ETZ selecionado; conferir o receptor real. Outras variantes HFBR/AFBR podem diferir no pino 4 e nos pinos de retenção. |
| R1–R6, C1–C10, Z1/Z2 | Footprints THT padronizados selecionados; conferir corpo, passo, tensão e potência das peças adquiridas. |
| C11/C12 | 1000uF, tensão nominal selecionada de pelo menos 200V; snap-in D30/P10 proposto. Confirmar diâmetro, passo e altura. |
| D3/D4 | DF005M DIP-4 / KBU6G linear selecionados por formato e especificações da lista; confirmar os códigos reais e a ordem dos terminais. |
| F1 | Clipes 5x20mm selecionados; confirmar o modelo dos clipes e os passos de seus furos. |
| T1/T2/T3 | Footprints personalizados **provisórios**, estimados do layout. Confirmar dimensões, pares de pinos, tensão e fase com as peças. |
| J1/P1/P2/J110/J2 | IEC, terminais e ligação PE com geometria proposta; conferir modelos, fixações, furos e numeração. |
| CPR1 | Footprint personalizado **provisório**, CDE 940C30S68K-F, passo selecionado 57,5mm. Confirmar desenho mecânico da peça. |

A existência de todos os footprints e a correspondência entre números dos pinos e dos pads foram verificadas. Isso **não confirma medidas físicas de peças não identificadas**. Os footprints marcados `CONFIRMAR` e os modelos selecionados da tabela precisam dessa conferência antes de usar o projeto para fabricar uma placa.

## Componentes de alimentação adicionados

Disponíveis no seletor de símbolos da biblioteca local `oneTesla`, com footprint associado:

| Símbolo | Footprint local | Pinagem |
| --- | --- | --- |
| `oneTesla:HLK-15M15BL` | `oneTesla:HLK-15M15BL` | 1/2 AC, 3 −Vo, 4 +Vo; saída 15V/1A. |
| `oneTesla:MUR460C` | `oneTesla:D_SMC` | SMC/DO-214AB; 1 cátodo, 2 ânodo. |
| `oneTesla:SMBJ18A` | `oneTesla:D_SMB` | SMB/DO-214AA; TVS **unidirecional**, 1 cátodo, 2 ânodo. |
| `oneTesla:1N5819` | `oneTesla:D_SMA` | Versão SMD SMA/DO-214AC; Schottky, 1 cátodo, 2 ânodo. |

O HLK segue a página 11 do [datasheet Hi-Link 15W-BL V1.0](misc/HLK-15W-BL_V1.0.pdf), disponibilizado na [página do componente na LCSC](https://www.lcsc.com/product-detail/C53122331.html). O desenho do fabricante usa **47,5 × 28,5 × 22mm como referência do módulo com caixa da mesma série**. O footprint reserva esse envelope para a versão BL de placa aberta; inclui serigrafia, contorno de fabricação, courtyard e indicação do pino 1. Furos de 1,1mm conforme o desenho, para terminais de 0,8mm ±0,2mm; pads de 2,5mm são uma escolha de layout. O courtyard tem margem de 1mm em torno do envelope nominal.

Coordenadas dos pads em mm, **vista superior da PCB**, com origem no pino 1:

| Pad | X | Y | Função |
| --- | --- | --- | --- |
| 1 | 0 | 0 | AC |
| 2 | 0 | 7,8 | AC |
| 3 | 42,5 | −7,4 | −Vo |
| 4 | 42,5 | 15,2 | +Vo |

São 42,5mm entre colunas, 7,8mm entre os terminais AC e 22,6mm entre os terminais DC. O fabricante informa tolerância de **±1mm nas dimensões e no espaçamento dos pinos** e pede conferência com a peça real antes de desenhar a placa; conferir especialmente a furação antes de fabricar.

Os três footprints SMD são cópias dos padrões do KiCad 10, com faixa de cátodo junto ao pad 1. Referências: [MUR460C World, SMC/4A/600V](https://www.worldgj.com/uploads/file/20251222/988858e88ba65bb483179d9af14a7299.pdf), [SMBJ18A AOS, SMB/18V/600W](https://www.aosmd.com/products/tvs/high-power-tvs/smbj18a), [1N5819 KEXIN, SMA/1A/40V](https://datasheet.lcsc.com/lcsc/1912111437_KEXIN-1N5819_C437199.pdf). Conferir o encapsulamento do fornecedor escolhido. O SMBJ18A usa o gráfico de TVS unidirecional; não o de TVS bidirecional dos componentes com sufixo CA.

Pré-visualizações SVG dos quatro símbolos e footprints, exportadas pelo KiCad, e conferência de pinos/pads estão em `output/power-components/`. O gerador do esquema inicial preserva esses quatro símbolos ao recriar a biblioteca.

## Verificação

`output/validation.txt` contém o resultado; `output/erc.json` é o relatório nativo do KiCad. A verificação cobre 20 redes de referência e sete conexões diretas, entradas/saídas livres, separação dos três domínios, todas as unidades dos CIs e correspondência completa dos pinos/pads. O ERC termina com **2 notas esperadas**: `power_pin_not_driven` nos pinos 1/2 do PS1 — os pinos AC do módulo HLK são `power_input` e a rede AC não tem pino `power_output` dirigindo; é inerente à troca pelo módulo e não indica erro de conexão.

Para repetir as verificações depois de editar o esquema:

```sh
kicad-cli sch export netlist oneTesla.kicad_sch -o output/oneTesla.net
kicad-cli sch erc oneTesla.kicad_sch -o output/erc.json --format json
python3 scripts/validate_schematic.py
kicad-cli sch export pdf oneTesla.kicad_sch -o output/oneTesla-schematic.pdf
```

`python3 scripts/build_schematic.py` recria o esquema inicial desta entrega e as bibliotecas locais, **sobrescrevendo edições posteriores nesses arquivos**; não o execute para apenas validar. O esquema anterior a esta reconstrução permanece no histórico do git.

## PCB

`oneTesla.kicad_pcb` é uma **réplica de 2 camadas** da placa driver original do oneTeslaTS, adaptada ao esquemático atual (fonte HLK, PE separado, PRE/CLR do 74HCT74 em +5V). A geometria vem dos arquivos Eagle originais publicados pelo autor (`misc/driver.brd`, de [bayley/oneteslats](https://github.com/bayley/oneteslats)): posições e rotações dos componentes, trilhas, vias, pours, outline (106,045 × 106,045 mm), furos e a serigrafia vetorial (logo oneTeslaTS, avisos) foram importados diretamente do `.brd`. As redes do cobre original foram reatribuídas às redes do esquemático atual via os contactrefs (pino a pino); o alinhamento de cada footprint foi verificado automaticamente (pad contra pad, rede contra rede, desvio máximo 0,04 mm).

**Adaptações em relação à placa original**

- Fonte auxiliar: T2, D3, IC5 (78L15) e C7 removidos com o cobre associado (+24V, AUX_AC1/2 e o ramal GND/PE da área). **PS1 (HLK-15M15BL)** ocupa o antigo lugar do T2, com os pinos AC à direita; C13 ocupa o antigo lugar de C7 (cada pad no seu pour: +15V e GND). Roteamento novo: /AC_L_FUSED e /AC_N até o PS1, +15V do PS1.4 subindo pela borda esquerda até C10/IC6.3 e ao pour dos drivers, GND do PS1.3 ao pour lógico.
- **PE separado de GND**: o fio original IEC.G→GND e o pad de canto superior direito foram separados; J2 (Chassis_PE_M3) fica no pad de canto (era o ponto de aterramento original) e um fio /PE novo liga J1.3 ao J2. O standoff U$13 (co-localizado com J2) foi omitido.
- **Primário**: P1 (pad direito, como na serigrafia original) = nó CPR1.2; P2 (pad esquerdo) = /DC_MID. Os anéis JPRT originais foram mantidos como terminais (JPRT1 em /DC_MID, JPRT2 no nó CPR1.2). As trilhas de fundo entre P1/P2/CPR1/JPRT foram refeitas para a nova topologia (o fio SW_NODE da CPR1.1 foi preservado; um salto por vias leva /DC_MID de P2 ao anel).
- **74HCT74**: na placa original, os pinos 10 e 13 (PRE/CLR) estavam em GND; no esquemático atual estão em +5V — dois links novos ligam IC2.13 e IC2.10 à rede de +5V.
- **Fusível**: as garras internas (tangs) ganharam jumpers do mesmo net dos clipes (na original eram ilhas sem net).
- GND de T3 confirmado no ramal original do CT; IC6.2 ligado por fio ao C9.2 (o bolsão do pour ficava isolado).

**Footprints**: a biblioteca local foi alinhada à geometria comprovada da placa original (`scripts/pcb_patch_footprints.py`): passos/posições de pads de R1, R5/R6, C8/C9/C10/C13, C11/C12, Z1/Z2, CPR1, T1 (GDT), FB1, J1 (IEC), F1 (ordem dos clipes), D4 (ordem dos pinos AC), P1/P2, J110, IC6 (TO-92 triangular), DIP-8/DIP-14 (pads padrão 1,6 mm, não long pads), furos NPTH de retenção do FB1 e do TO-3P. As notas `CONFIRMAR`/`PROVISORIO` continuam valendo — os footprints espelham a placa original, o que não confirma as peças compradas.

**Verificação do PCB** (`output/drc.json`): **0 itens não conectados**. Restam, por escolha consciente: `hole_clearance` ×2 e `copper_edge_clearance` ×1 presentes na geometria original (trilha /AC_L sobre o furo do IEC, trilha /OPTICAL_OUT junto ao furo de retenção, pad J2 a 0,2 mm da borda); 3 ilhas same-net no pour SW_NODE (slivers que o preenchimento original também gera); e ruído cosmético esperado (silk sobre cobre nos logos, courtyards sobrepostos, `lib_footprint_mismatch` por os footprints embutidos levarem Reference/Value reais).

**Mecânico — conferir antes de fabricar**: o envelope do HLK no footprint é o da série com caixa (47,5 × 28,5 mm); na posição atual a lateral do módulo fica a ~0,2 mm dos pads de solda do conector IEC. Medir o módulo BL real (provavelmente ~44 × 24 mm) e, se necessário, deslocar PS1 ~1 mm para dentro. A versão BL de placa aberta não deve ultrapassar os pads do IEC.

**Regenerar o PCB do zero** (sobrescreve `oneTesla.kicad_pcb`):

```sh
python3 scripts/pcb_patch_footprints.py   # alinha a biblioteca à geometria original
python3 scripts/pcb_extract.py            # componentes/redes do esquemático -> output/pcb-data.json
python3 scripts/build_pcb.py              # gera o .kicad_pcb (placement verificado + cobre)
/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/Current/bin/python3 scripts/pcb_refill.py oneTesla.kicad_pcb
kicad-cli pcb drc oneTesla.kicad_pcb -o output/drc.json --format json
```
