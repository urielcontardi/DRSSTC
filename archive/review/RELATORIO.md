# Auditoria independente DRSSTC / oneTeslaTS

Data: 07/10/2026. Fonte: commit **f4da80c517a5edeefd3d4267e3aca7924727bbe4**.
Repositório: https://github.com/urielcontardi/DRSSTC. Clone recuperado da execução anterior, inicialmente limpo; nenhum arquivo de projeto alterado. Artefatos desta auditoria somente em review/. Sem push/PR.

## Parecer

**Não liberar esta revisão para fabricação ou energização.** A suspeita de layout ruim procede, mas não se resume a estética: há um footprint comprovadamente incompatível com o componente selecionado (FB1), perda sistemática de coerência mecânica ao adaptar pads de outro projeto, capacitores D30 que não cabem lado a lado e distâncias rede–PE submilimétricas. “Zero não conectados” é verdadeiro, porém não significa placa correta ou segura.

O problema central é tratar o cobre da placa antiga como referência mecânica definitiva. O script scripts/pcb_patch_footprints.py, linhas 4–5 e 116 em diante, declara e implementa a troca de pads mantendo silk/fab/courtyard. Esses desenhos **não são apenas cosméticos**: representam corpo, polaridade, montagem e exclusão mecânica. Também houve troca de componente real, particularmente IFD95 → HFBR, sem trocar a geometria correspondente.

## Escopo, método e limites honestos

- 166 arquivos originais versionados inventariados com SHA-256 em inventario.csv.
- 2 placas: oneTesla.kicad_pcb e misc/driver.brd (Eagle original).
- 5 esquemas KiCad: principal, revisado e três snapshots misc; mais misc/driver.sch Eagle.
- PCB atual: **48 instâncias de footprint**, sendo 41 referências do esquema + JPRT1/JPRT2 + 5 furos sem referência; 205 segmentos, 7 vias, 6 zonas; 2 camadas, espessura declarada 1,6 mm, contorno ~106,045 mm quadrado.
- **135 arquivos .kicad_mod**: 31 oneTesla e 104 Resistor_THT. 24 modelos locais usados pelo PCB; 111 não usados (7 oneTesla + 104 resistores), separados em cobertura-bibliotecas.csv. Três nomes de footprints adicionais existem apenas embutidos no PCB (furos e anéis).
- Eagle: 51 elementos inventariados individualmente em cobertura-eagle.csv; importação nativa KiCad, DRC e inspeção visual da vista superior executados.
- Cada uma das 48 instâncias tem linha própria em cobertura-pcb.csv, com referência, valor, posição, pads, furação, passos, rede, polaridade, encaixe, courtyard, silk e achados. pads.csv detalha coordenadas locais e absolutas. Todas as 41 geometrias de pads locais/embutidos coincidem após normalizar ordem e números; isso **não valida o desenho do footprint**.
- Usado KiCad **10.0.6**, já instalado na imagem local kicad-web:local. Contêiner descartável, sem rede, projeto montado read-only e apenas review gravável. Não foi iniciado/alterado o desktop KiCad do usuário. DRC com refill apenas em memória, sem --save-board. Não executados geradores destrutivos do repositório.
- Exportações SVG nativas top/bottom/assembly e Eagle convertidas a PNG com librsvg; todas essas vistas foram efetivamente inspecionadas. A serigrafia deslocada, capacitores sobrepostos, linha PE periférica e desvios longos de potência são visíveis nas imagens.
- Datasheets obtidos e comparados: TI UCC37321, onsemi FGA60N65SMD, Broadcom HFBR-0500ETZ, CDE 940; Hi-Link PDF local p11. Não foram inventados MPNs para passivos, conectores ou magnetismos.
- **Não é aprovação completa de cada peça física.** Todos os footprints foram cobertos geometricamente; os 111 não usados não receberam comparação individual com fabricante. Faltam BOM comprável/peças, CAD do dissipador/enclosure, normas aplicáveis e parâmetros elétricos. ERC nativo do esquema Eagle não executado; DRC do Eagle é sobre importação, não validação no Eagle. Não há Gerbers/Excellon/STEP/BOM de produção versionados para auditar um lote de fabricação.

## Resultados nativos reproduzidos

### PCB atual

DRC: **529 violações + 56 questões de paridade, 0 itens não conectados**. Total: 87 erros e 498 avisos.

| Classe | Quantidade |
|---|---:|
| silk_overlap / silk_over_copper | 199 / 199 |
| courtyards_overlap | 45 |
| pth_inside_courtyard / npth_inside_courtyard | 34 / 5 |
| hole_clearance / copper_edge_clearance | 2 / 1 |
| silk_edge_clearance | 14 |
| lib_footprint_mismatch / lib_footprint_issues | 23 / 7 |
| paridade: campo Footprint_Status ausente | 41 |
| paridade: extras / refs vazias duplicadas | 7 / 4 |
| paridade: FB1 pinos 5/8 sem pads elétricos | 2 |
| paridade: Z1/Z2 DNP divergente | 2 |

Os 23 mismatches não devem ser descartados em bloco nem interpretados como 23 pinagens erradas: os pads conferem nas 41 referências. Há diferenças de propriedades/gráficos. As colisões courtyard incluem artefatos do desenho deslocado e problemas reais de corpo — precisam ser corrigidas, não silenciadas indiscriminadamente. A execução atual não reproduziu os três slivers mencionados no README.

### Esquemas

- oneTesla: 2 power_pin_not_driven em PS1.1/2. Alimentação AC não tem power_output; não é validação de isolamento ou fusível.
- oneTesla-revisado: 0 ERC, mas **não é esquema equivalente ao PCB**: ainda tem T2/D3/IC5/C7 e RAW_DC; IC1.12 está NC e IC2.1 recebe RESET_MIX diretamente. No principal, IC1.12 dirige IC2.1. Esta é diferença de função, não só nomes.
- before-compact e saved-old-copy: 132 ERC cada (principalmente bibliotecas/links não resolvidos).
- before-replication: 84 ERC, incluindo 35 pinos não conectados, 11 não dirigidos, 9 alimentações não dirigidas. Não presumir que snapshots sejam fabricáveis.

As netlists nativas estão em evidence/*.net; netlist-differences.json lista diferenças de nomes/pinos e também renomeações que não são alterações topológicas. Comparação pad→net do PCB atual com o esquema principal: nenhum conflito entre os pads presentes. FB1.5/.8 deliberadamente viraram NPTH sem numeração, permanecendo o aviso de paridade.

### Eagle original

Importação em evidence/eagle-import.kicad_pcb, não substituir a fonte. DRC da importação: 180 violações, 0 não conectados. Inclui 12 hole_clearance, 9 shorting_items, 4 hole_to_hole, 2 copper_edge_clearance, 1 clearance. Vários “curtos” são objetos NPTH sem rede após importação, e furos duplicados do dissipador; **não afirmar nove curtos físicos independentes**. Mesmo assim, demonstra que copiar a geometria antiga não elimina problemas. A vista nativa evidencia eletrolíticos EB25D e receptor IFD95, diferentes dos modelos nomeados atualmente.

## Achados priorizados

### F01 — P0 fabricação: FB1 não é footprint HFBR-2521ETZ

Evidência: scripts/pcb_patch_footprints.py **39–45**, que usa explicitamente IFD95 e “RL pad4 best-guess continuation”; cobertura-pcb.csv FB1; Broadcom AV02-3283EN p4/p11.

- Footprint elétrico tem passo **1,905 mm**, quatro pads na ordem espacial **3–1–2–4**.
- Desenho Broadcom: terminais em **2,54 mm**; corpo/retenções também precisam seguir a variante correta.
- Os nomes 1 OUT / 2 GND / 3 VCC / 4 RL estão coerentes no esquema, mas isso não corrige as coordenadas físicas. Pinos 5/8 são retenções e não devem ser conectados eletricamente segundo o fabricante.
- Local: FB1 origem (10,160; 63,500) mm. A placa pode estar perfeita em netlist e receber o componente errado ou não aceitar inserção.

Correção proposta: decidir se a peça será HFBR-2521ETZ ou IFD95 real; usar desenho exato e então reposicionar/rerotear, não deformar footprint para caber no cobre antigo.

### F02 — P0 fabricação: pads modificados, corpos/polaridades/nomes não acompanhados

Evidência direta: scripts/pcb_patch_footprints.py 17–30, 35–45, 74–105; gráficos efetivos em assembly.png e arquivos locais.

- **R1:** nome/corpo axial L25 P30,48; pads agora em ±11,43 (pitch **22,86**). F.Fab continua de x2,74 a27,74, centro15,24, enquanto par de pads está centrado em0. Corpo25 é maior que distância22,86 entre furos: não serve como montagem axial horizontal convencional daquela peça. Não é apenas erro de texto.
- **R5/R6:** nome P12,70, pads P10,16, corpo não recentrado.
- **C8/C9/C13:** nome P3,50, pads P2,54, círculo permanece centrado x1,75. **C10:** nome P5, pads P3,556, círculo centrado x2,5. Valor real de C10 no esquema/PCB é 680u 35V, mas texto legado de fabricação mostra 100u 10V; não comprar pelo texto velho.
- **C11/C12:** nome P10, pads P10,16 centrados em0, círculo permanece centrado x5. A faixa de polaridade/courtyard desloca junto, tornando montagem enganosa.
- **P1/P2:** chamados “M6”, mas furo **2,2 mm**, pad4: corresponde à intenção de soldar fio, não passagem de parafuso M6. Definir terminal e esforço mecânico; apagar envelope genérico não resolve retenção.
- **T1:** footprint genérico tem courtyard local x±7; pads em x−9,017 e +8,763 ficam fora dele. Corpo e posição não descrevem o transformador real.
- **F1:** pads recentrados em ±5,08/±10,16, mas desenho do clipe permanece no sistema antigo. Não comprova montagem Littelfuse citada no nome.
- **IC6:** nome TO-92_Inline, pads triangulares. Confirmar fabricante/sufixo 78L05, vista, pinagem e conformação; não assumir todos os 78L05 idênticos.
- **D4:** nome Vishay KBU, porém pads seguem GBU4S antigo. AC2/3 permutados não é por si só defeito elétrico; o modelo mecânico exato continua pendente.

Restaurar footprints a partir das peças, incluindo fab/courtyard/polaridade, só depois refazer placement. Renomear geometrias personalizadas para não se passarem por padrões KiCad.

### F03 — P0 fabricação: C11 e C12 D30 não cabem

Origens/pontos médios dos pads (92,710;31,750) e (66,675;31,750): distância **26,035 mm**. Corpos declarados Ø30 deixam sobreposição nominal **3,965 mm**, mesmo corrigindo o deslocamento de5 mm. O desenho atual de C11 chega x112,710, além da borda106,045. Se o corpo fosse recentrado nos terminais, ainda chega x107,710. O Eagle original usa **EB25D**, não D30.

Não diagnosticar automaticamente que peças físicas já compradas colidem: MPN não fornecido. Diagnóstico certo é que **os corpos especificados pelos footprints atuais são incompatíveis com placement**. Escolher capacitor de diâmetro/tensão/ripple adequados ou aumentar espaçamento; não reduzir círculo para calar DRC sem selecionar peça real.

### F04 — P0 rede: cobre invade furo de J1

DRC hole_clearance: **0,0000 mm** entre /AC_L F.Cu (segmento de74,930;3,810 a53,975;3,810, largura2,54) e NPTH J1 centro **(59,205;6,071), Ø3 mm**. A distância geométrica centro-linha2,261 menos raio1,5 menos meia-largura1,27 resulta −0,509 mm: cobre entra no envelope de furação. Não é aceitável apenas por estar no original; pode ser removido pelo furo ou exposto ao fixador.

Segundo problema: FB1 retenção em(2,540;66,040), /OPTICAL_OUT: **0,2413 mm** versus regra0,25. Menor gravidade que J1, mas precisa ajuste de footprint correto primeiro.

### F05 — P0 segurança: domínio PE inadequadamente tratado

Medições de bordas de segmentos coplanares, não de máscara, registradas em clearance-samples.txt:

- **/AC_L_FUSED–PE =0,290 mm** em B.Cu, junto a(95,25;3,81), PE de(93;2) a(99,5;2).
- **/AC_L–PE =0,440 mm** em F.Cu: rede em y3,81, PE em y1,85.
- PE tem aproximadamente **88,58 mm** somados de trilhas, largura **0,5/0,6 mm**, duas vias Ø0,6 (pads1,3) em(93;2) e(99,5;2).
- J2 pad de PE em(102,362;2,7559), cobre a **0,2059 mm** da borda; regra do projeto exige0,5.

Essas distâncias são fatos de geometria e motivo para **bloquear liberação**, não uma certificação numérica de uma norma específica. Dimensionamento de clearance/creepage depende da tensão de trabalho e transientes, categoria de sobretensão, poluição, CTI/material, altitude, coating e norma do produto. PE precisa suportar falta e esforços mecânicos até a proteção atuar; I²t do fusível/rede e espessura de cobre não estão definidos. Separar nets PE/GND não prova proteção. Recomenda-se bonding de chassis dedicado robusto e arquitetura de aterramento explicitamente projetada, em vez de depender desta linha/vias sem qualificação.

### F06 — P1 desempenho/robustez: loop primário longo e gargalos

- P2 → DC_MID contorna a borda inferior, sobe pela direita até C11/C12, com trilhas2,54 mm. A soma de todos os segmentos DC_MID é231,8 mm (inclui ramificações; **não equivale ao comprimento de um único loop**).
- Há troca de camada através de **uma via Ø0,6 por transição**, em(84;97,045) e(94;97,045), trecho F.Cu10 mm entre elas. Isso participa do caminho de corrente do primário e exige dimensionamento; não inferir capacidade em ampères sem cobre/plating/ondas/duty.
- CPR1.2/P1 possui75,63 mm somados de trilhas2,54. O retorno do tanque não segue de perto toda a ida. Risco de indutância parasita, overshoot e emissão, qualitativo; não foi calculado nH nem simulada corrente.
- Gates H/L têm trilhas **0,4064 mm** e comprimentos aproximados26,18 /21,66 mm; retornos pelos nós emitter/pours não constituem par estreito/Kelvin demonstrado em toda extensão. O SW_NODE tem área de cobre extensa perto dos secundários do GDT; considerar capacitância parasita e ruído de modo comum.
- C5/C6 e C8/C13 ficam próximos dos drivers, aspecto positivo; mas TI pede capacitor de baixo ESR/ESL entre VDD8/PGND5 e separado entre VDD1/AGND4, ligação AGND–PGND curta/larga. A escolha THT1u + eletrolítico e soquete não comprova a impedância de pulso requerida. Não afirmar instabilidade sem medição.
- Z1/Z2 são TVS entre coletor/emissor, **não clamps gate-emitter**. Confirmar VGE ±20 V, overshoot, saturação do GDT, deadtime/fase e corrente máxima em ensaios limitados antes de barramento pleno.

Reorganizar primeiro o loop C11/C12–meia ponte–CPR1–primário, encurtar retorno e evitar vias únicas de potência. Selecionar stackup/cobre e calcular perdas RMS/pulsadas; só então fixar larguras/vias.

### F07 — P1 mecânica: PS1/IEC/fixações e tolerâncias

PS1(44,25;22), rot180°, envelope de referência47,5×28,5; desenho Hi-Link local p11 confirma42,5 entre colunas,7,8 AC,22,6 DC e funções1/2 AC,3−Vo,4+Vo. Orientação adotada é coerente com a vista superior.

Porém o envelope é explicitamente referência da série com caixa; não prova BL adquirido. Courtyard conflita J1 e furo de canto(3,8735;2,3495). Borda direita nominal x46,75 coincide quase com extremidade do pad L de J1 x47,205; a geometria exata merece controle 3D, não a hipótese “BL provavelmente menor”. Furo1,1 para terminal0,8±0,2 deixa pouca folga no extremo; tolerância dimensional/pitch±1 mm do fabricante demanda amostra/gabarito. Arruelas/standoffs não podem invadir placa aberta do módulo.

Q1/Q2: passo5,45 confirmado onsemi; terminal máximo1,2×0,75 tem diagonal~1,415 mm versus furo1,4986 nominal (margem diametral~0,084 antes de tolerâncias de furo/acabamento). Pode montar, mas precisa tolerância real. Fab15,5 mm de largura é menor que máximo16,2 do corpo. Furo do dissipador é objeto separadoØ5,5; centro está~0,4405 mm afastado do centro de furo representado no F.Fab após transformação. Validar dobra, plano de apoio, isoladores, parafusos/torque e dissipador, não só pitch.

### F08 — P1 documentação/produção: DNP e múltiplas fontes contraditórias

Z1/Z2 DNP no esquema, não DNP no PCB. Os 41 campos Footprint_Status ausentes do PCB perdem os avisos na passagem para montagem. Sete footprints extras não têm biblioteca/símbolo; cinco referências vazias dão quatro avisos de duplicidade, **não cinco componentes sobrepostos no mesmo ponto**. Bibliotecas e arquivos “revisado” têm que receber uma definição inequívoca de qual revisão é vigente. README contém valores/passos antigos (CPR1 citado57,5, real58,42; C10 texto antigo etc.). Corrigir após decisão técnica, sem simplesmente apagar histórico.

## Avaliação elétrica e térmica condicionada

Topologia atual coerente no nível de nets: fusível em L antes de PS1/ponte; J110 conecta N ao ponto médio para dobrador; capacitores C11/C12 em série; CPR1 em série com primário P1/P2; T3 é secundário CT; lógica isolada GND, DC_MINUS e PE são nets distintas. UCC37321 OUT6/7 e VDD1/8 unidos, G1/C2/E3 IGBT corretos. Fase do GDT **não verificada** por ERC/netlist.

Não há regra HV específica: oneTesla.kicad_pro linha143 min_clearance0, linha498 clearance Default0,2 mm, linha521 sem padrões de netclass. Zonas de potência têm clearance0,6096 e lógica0,4. Não há budget de isolamento/creepage por domínio. Assim DRC sem erros de clearance **não prova isolamento de rede**. Medições acima são amostras só de segmentos retos, não mínimo global pad/pour ou caminho 3D.

Para C11/C12 1000u/200V, tensão nominal por capacitor no dobrador depende da rede e tolerância/balanceamento; não tratar “110” como equivalente a qualquer tensão127/alta linha sem cálculo. R5/R6 100k0,5W: a200V dissipa0,4W cada, pouca margem térmica; tau nominal RC=100s por capacitor, tensão residual depende de tensão inicial e tolerância/falha do bleeder. “Esperar5min” impresso não substitui medição e procedimento seguro de descarga.

IC6 perde aproximadamente(15−5)×I5V; sem carga exata/ambiente não concluir temperatura aceitável. F1 precisa tipo rápido/lento, I²t, capacidade de interrupção e rating da fonte de rede, não só4A250V. Ponte D4, capacitores ripple e dissipador não dimensionados no repo. Q1/Q2 ratings de datasheet não são garantia de capacidade da bobina. CDE940C30S68K-F confirma corpo46×19, fio1 mm,3000Vdc/500Vac da série; o pitch58,42 é dobra escolhida. Limites AC, frequência, dV/dt e corrente RMS devem ser conferidos para onda real, não deduzidos do “3kV”.

## Footprints não usados

Os sete oneTesla não usados são enumerados em cobertura-bibliotecas.csv (uso NÃO USADO): SOP14, DIP8 sem soquete, EI30, ponte DIP4 e diodos SMA/SMB/SMC. São reserva de biblioteca, não falhas de placement atual. Os nomes MUR460C/1N5819 genéricos não autorizam troca automática entre THT/SMD; fabricante/sufixo da compra tem que definir encapsulamento. Os104 resistores Resistor_THT receberam inventário de pads/furos/courtyard/silk/fab, **não homologação individual contra fabricantes**. Não foram modificados.

## Ordem recomendada de correção — nenhuma aplicada nesta auditoria

1. Congelar esquema principal e BOM com MPN, datasheet e peça real de magnetismos/conectores/soquetes/capacitores/fusível.
2. Corrigir FB1 e todos os footprints alterados por matching de cobre; reconstruir corpo, pad1, polarity, courtyard e 3D coerentes. Conferir impressão1:1 com peças.
3. Rever dimensões da placa/placement C11/C12, PS1/J1, dissipadores e terminais. Resolver colisões reais antes de silk.
4. Definir rede/PE/bonding e regras HV segundo ambiente/norma; refazer J1 e separações rede–PE, incluindo caminho de falta.
5. Refazer loops de potência e gates com retorno próximo; dimensionar cobre/vias a partir de corrente/pulsos e limite térmico.
6. Sincronizar DNP/campos/referências extras, remover ambiguidades históricas do fluxo de fabricação; gerar Gerber/drill/BOM/assembly somente após aprovação.
7. Reexecutar DRC/ERC/paridade e conferir CAM independente. Depois testes de bancada progressivos de baixa energia e instrumentação apropriada por profissional habilitado. Auditoria CAD não autoriza energização de DRSSTC.

## Evidências e reprodução

Arquivos centrais: cobertura-pcb.csv, cobertura-bibliotecas.csv, cobertura-eagle.csv, pads.csv, drc-itens.csv, inventario.csv. evidence/drc.json conserva posições e UUIDs; evidence/top.png, bottom.png, assembly.png, eagle-top.png são vistas inspecionadas. PDF/fontes externas podem ter copyright; guardadas para rastreabilidade técnica, não redistribuídas remotamente.

Com KiCad10.0.6:

```sh
kicad-cli pcb drc oneTesla.kicad_pcb -o review/evidence/drc.json --format json --all-track-errors --schematic-parity --severity-all --refill-zones
kicad-cli sch erc oneTesla.kicad_sch -o review/evidence/erc-oneTesla.json --format json
kicad-cli sch export netlist oneTesla.kicad_sch -o review/evidence/oneTesla.net
PYTHONDONTWRITEBYTECODE=1 python3 review/audit.py
PYTHONDONTWRITEBYTECODE=1 python3 review/annotate.py
```

Não usar --save-board nem scripts/build_* / pcb_patch_footprints.py para apenas validar. Os scripts de auditoria são auxiliares de inventário; DRC/ERC/netlists vêm do KiCad, não de parser caseiro. O leitor sexpr existente só complementou medidas/CSV depois da descoberta e uso das ferramentas nativas.

Fontes primárias acessadas em07/10/2026:
- https://docs.broadcom.com/doc/AV02-3283EN (p4 mecânica e p11 HFBR25x1, evidence/hfbr.pdf)
- https://www.ti.com/lit/ds/symlink/ucc37321.pdf (pinagem, layout e PDIP P, evidence/ucc37321.pdf)
- https://www.onsemi.com/pdf/datasheet/fga60n65smd-d.pdf (CASE340BZ, evidence/fga60n65smd.pdf)
- https://www.cde.com/resources/catalogs/940C.pdf (940C30S68K-F, evidence/cde940.pdf)
- misc/HLK-15W-BL_V1.0.pdf p11 (evidence/hlk-mechanical.png)
- Tentativa Vishay KBU não recuperou PDF; não considerada validação.


## Fechamento da retomada e bloqueio da homologação completa

A retomada preservou o clone e os artefatos anteriores. Foram reinspecionadas as quatro vistas PNG (topo, fundo, montagem e Eagle), o desenho mecânico Broadcom e as tabelas de medidas. DRC e ERC do principal foram repetidos em contêiner sem rede, projeto somente leitura: **529 violações, 56 questões de paridade, 0 não conectados; ERC 2**. Resultados: evidence/drc-recovery.json e evidence/erc-recovery.json. Os SHA-256 dos **166 arquivos originais** continuam idênticos a inventario.csv.

A anotação individual escrita mas ainda não executada foi aplicada: cobertura-pcb.csv contém conclusões específicas para todas as referências, também legíveis em COBERTURA.md. checagem-bibliotecas.csv acrescenta checagens básicas de anel nominal, presença de F.Fab/F.CrtYd para **135/135 modelos**, incluindo os não usados. Isso não substitui comparação com uma peça.

### Matriz de encerramento honesto

| Item solicitado | Executado | O que impede aprovação completa |
|---|---|---|
| PCB KiCad atual | DRC/paridade, geometria 48/48, netlist, inspeção das duas faces/montagem | Achados F01–F08; MPNs e tolerâncias ausentes |
| Eagle legado | Inventário 51/51, importação KiCad, DRC e vista superior | Sem ERC/DRC no Eagle original; peças legadas não homologadas individualmente |
| Bibliotecas | Inventário e checagens básicas 135/135; 24 modelos usados com análise por referência | 111 modelos não usados sem associação exata a peças; não é possível verificar datasheet de componente não selecionado |
| Esquemas KiCad | ERC dos cinco arquivos e comparação das netlists | Revisões divergem funcionalmente; designar fonte de fabricação |
| Isolação HV/PE | Geometria e falhas locais identificadas | Rede máxima, transientes, norma, altitude, poluição, CTI/coating e bonding sem especificação suficiente |
| Corrente, comutação e temperatura | Caminhos, vias, loops e riscos qualitativos | Frequência, corrente de pico/RMS, duração/repetição dos pulsos, cobre/plating, ambiente e dissipador |
| Mecânica final | Envelopes e conflitos CAD | MPNs, amostras, tolerâncias da fábrica, magnetismos e conjunto dissipador/enclosure |

**Resultado entregue: relatório de revisão CAD com cobertura e bloqueios, não homologação integral de todas as peças.** Para encerrar a parte física solicitada, fornecer BOM comprável (fabricante + código completo + variante), desenhos/bobinagem de T1/T3, modelos dos terminais/IEC/clipes/soquetes, peças C11/C12 e dados operacionais acima. Não escolher substitutos implicitamente. Sem isso, não há base para declarar pinagem/pitch/drill/polaridade de cada peça real confirmados. Nenhum erro encontrado exige energizar a placa para ser demonstrado.

Não foi aplicado patch à placa, ao esquema ou às bibliotecas; não houve push, PR, alteração no Gateway nem certificação de segurança.
