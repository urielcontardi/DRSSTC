# Contexto do oneTeslaTS — fontes originais locais

Leitura em 17/10/2026. Este documento corrige a base da revisão anterior; não altera PCB, esquema ou regras.

## Fontes efetivamente examinadas

- `misc/oneTeslaTS_User_Manual.pdf`: manual v1.8, ©2019, 49 páginas de arquivo. Texto integral extraído em `manual-parts.txt`. Páginas 21, 22, 46, 47 e 49 também renderizadas para conferir figuras. A numeração impressa difere da página do PDF.
- `misc/oneTeslaTS_Parts.pdf`: lista original do kit, uma página.
- `misc/driver.brd`: Eagle 6.5.0; leitura XML direta das zonas, regras e contatos de potência. Evidência em `eagle-reference.json`.
- `misc/driver.sch`: contatos e ligações do esquema original.
- `scripts/build_pcb.py`, `scripts/build_schematic.py`, README e arquivos ativos: conferência das adaptações e renomeações, sem executar os geradores.

## Arquitetura documentada

É o oneTeslaTS, uma DRSSTC com meia ponte de dois IGBTs, capacitor do primário e primário na placa do ressonador. Há interrupter externo por fibra óptica, lógica 74HCT14/74HCT74, dois UCC37321 e transformador de gate T1. T3 é CT de realimentação 1:300; seus dois terminais elétricos são o secundário, enquanto o condutor de potência atravessa o núcleo.

O manual separa a montagem/teste da lógica da montagem de potência. As páginas 46–47 do PDF mostram os sinais de drive e a corrente oscilatória crescente durante cada pulso. A indicação de 1000 Hz na página 37 é ajuste do interrupter, não especificação da frequência ressonante de comutação.

Na página 21, J110 é instalado para 110 V e omitido para 220 V. A topologia permite dobrador na configuração de baixa tensão e retificação sem dobrador na outra configuração. O manual não deve ser interpretado como especificação explícita para toda a faixa da rede brasileira de 127 V.

C11/C12 são capacitores de barramento de 1000 µF. R5/R6 são bleeders de 100 kΩ/0,5 W. CPRI é o capacitor do tanque primário; a imagem da placa na página 49 identifica CDE 940C30S68K-F e 0,068 µF/3000 V. Esse é o rating do componente, não uma medição de tensão operacional.

Z1/Z2 são TVS opcionais coletor–emissor e não vêm no kit. O manual exige isolação dos IGBTs em relação ao dissipador com sil-pad. A lista indica fusível de 4 A, enquanto imagens/textos do manual ainda citam 10 A: há divergência documental, não autorização para trocar o valor atual.

## Zonas originais: fatos extraídos do Eagle

| Sinal original | Equivalente atual | Camada Eagle | Isolate explícito | Conexão térmica | Rank explícito |
| --- | --- | --- | --- | --- | --- |
| POS | DC_PLUS | 16 / Bottom | 0,6096 mm | desativada, sólida | 2 |
| NEG | DC_MINUS | 1 / Top | 0,6096 mm | desativada, sólida | 2 |
| N$14 | SW_NODE | 16 / Bottom | 0,6096 mm | desativada, sólida | ausente |
| GND | GND | 16 / Bottom | ausente | ausente | ausente |
| +5V | +5V | 1 / Top | ausente | ausente | ausente |
| +15V | +15V | 1 / Top | ausente | ausente | ausente |

Todas essas zonas usam `width=0.4064` mm no Eagle. A ausência de isolate explícito nas zonas de lógica não autoriza atribuir 0,6096 mm a elas: dependem das regras padrão. Existe somente a classe `default` no original, sem distâncias especiais por classe.

As regras gerais wire–wire, wire–pad, pad–pad e similares são 8 mil = 0,2032 mm. `mdCopperDimension` é 40 mil = 1,016 mm e `msWidth` é 10 mil = 0,254 mm. São parâmetros reais do arquivo de referência, não uma certificação normativa do equipamento.

O original tem planos amplos POS/NEG em faces opostas e uma zona localizada SW_NODE em Bottom. Não há zona DC_MID no Eagle original: a zona DC_MID da placa atual é uma adaptação posterior. Por isso a hierarquia de todas as zonas atuais não pode ser atribuída ao projeto original.

**Consequência:** 3 mm universais entre todas as redes de potência e 6,4 mm para o tanque não vieram do oneTesla. A distância de 6,4 mm potência–controle já existia nesta adaptação antes desta sessão de regras; também não é especificação encontrada no original. O afastamento original de 0,6096 mm é a referência concreta para reproduzir as zonas de potência; a segurança e as distâncias das modificações ainda exigem avaliação própria, especialmente na barreira com lógica, fonte, fixações e conectores.

## Atenção à renomeação P1/P2

No original, o manual (página 21 do PDF) manda passar um jumper entre P1/P2 pelo núcleo de T3. A página 22 identifica JPRI como os dois pontos mecânicos que conduzem corrente até o primário na placa superior.

O Eagle coloca P1 e P2 nominalmente em N$14 junto da meia ponte e CPRI. Não se deve inferir que isso permite substituir o jumper que atravessa o CT por uma conexão direta de cobre: a montagem física faz parte da realimentação.

Na adaptação KiCad atual, P1 e P2 foram reutilizados como terminais do primário externo:

- P1: `Net-(CPR1-Pad2)`.
- P2: `/DC_MID`.
- CPR1.1: `/SW_NODE`; CPR1.2: `Net-(CPR1-Pad2)`.
- T3: `Net-(T3-S1)` e `GND`, somente secundário do CT.

Logo, aplicar literalmente as instruções de P1/P2 do manual aos nomes da adaptação pode ligar coisas erradas. O condutor do circuito primário precisa atravessar T3 conforme a topologia e a fase apropriadas; isso não é provado pela continuidade elétrica no DRC. O gerador local explicita o primário externo entre os P1/P2 atuais, enquanto `build_pcb.py` contém mapeamentos dos nomes e exceções de net para esses pads.

## O que mudou nesta adaptação

- Fonte auxiliar com T2/D3/regulador de 15 V substituída por PS1 HLK-15M15BL, saída 15 V; regulador de 5 V mantido em outra versão de encapsulamento.
- Placa e posicionamento modificados; conectores, vários encapsulamentos e montagem de capacitores também foram alterados.
- P1/P2 passam a ser terminais do primário externo em lugar do jumper de CT do original.
- Zonas e prioridades atuais não são cópia literal do Eagle, inclusive DC_MID adicional e GND em duas faces.

Essas mudanças devem ser avaliadas como mudanças no oneTeslaTS, preservando o contexto do kit original, em vez de tratar o circuito como um inversor genérico sem referência.

## Correção da análise anterior

A ressonância existe e está explicitamente documentada; o erro não foi reconhecer o tanque, mas escolher 6,4 mm sem obter tensão ou requisito que sustentasse o número. O manual não fornece uma tabela numérica de tensão máxima do tanque/clearance/creepage para justificar a regra criada.

Da mesma forma, as ocorrências de DRC provocadas por 3 mm não demonstram defeitos do projeto original. Elas demonstram incompatibilidade entre uma meta escolhida nesta revisão e a geometria existente. A correção da sobreposição/prioridade de SW_NODE deve ser separada da imposição desses limites.

Nesta leitura não foram feitas novas alterações ao projeto ativo. Também foi observado que o `.kicad_pro` ativo voltou a conter apenas Default de 0,20 mm, enquanto as regras personalizadas da etapa anterior continuam no `.kicad_dru`: não presumir que o estado do relatório anterior permanece integralmente carregado/salvo no editor.
