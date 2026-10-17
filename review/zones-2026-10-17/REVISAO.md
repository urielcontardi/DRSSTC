# Revisão de zonas e isolamento — 17/10/2026

Revisão do arquivo ativo `oneTesla.kicad_pcb`, com as alterações existentes do usuário preservadas. Nenhuma alteração aplicada ao PCB, projeto ou regras ativos. Os arquivos `priority-only` e `screening` nesta pasta são experimentos de diagnóstico, não versões de fabricação.

## Resultado

Há um conflito confirmado de prioridade que fragmenta SW_NODE. Além disso, o projeto atual tem somente a classe Default, com clearance de 0,20 mm: as classes de potência descritas em `implementation/j110-jlcpcb/RESULTADO.md` não existem no arquivo ativo. O clearance local de todas as zonas é 0,50 mm. Isso permite preenchimento próximo demais para tomar o DRC atual como validação de isolamento do barramento.

A regra personalizada de 6,4 mm de clearance e creepage potência–controle ainda existe em `oneTesla.kicad_dru`. Ela cobre gates como domínio de potência, mas exclui objetos com net vazia da condição. Não substitui uma revisão de fixadores, dissipador, ferragens, cobre sem net ou da isolação física dos transformadores.

## Zonas e prioridades

| Zona | Camada | Prioridade atual | Avaliação |
| --- | --- | --- | --- |
| GND | F.Cu e B.Cu | 0 implícita | Restrita à lógica. Preservar barreira com potência; não unir a DC_MINUS. |
| DC_MINUS | F.Cu | 1 | Não disputa prioridade com DC_PLUS em B.Cu. Rever extensão do plano e retorno de potência. |
| SW_NODE | B.Cu | 2 | Inteiramente dentro do contorno de DC_PLUS. Prioridade insuficiente fragmenta a conexão. |
| DC_PLUS | B.Cu | 3 | Plano amplo; precisa abrir espaço para SW_NODE e DC_MID e respeitar regras por tensão. |
| DC_MID | B.Cu | 4 | Correto prevalecer sobre DC_PLUS onde há sobreposição; não confundir com GND. |

Teste isolado: elevar SW_NODE de 2 para 5, mantendo todo o restante, reduz as conexões faltando de quatro para uma. As três ocorrências internas da zona desaparecem. A restante é CPR1.1 em (69,69;116,40) mm até a trilha SW_NODE que termina em (72,50;122,75) mm. Prioridade não resolve esse trecho não roteado.

A hierarquia 0/1/5/3/4 funciona no teste de conectividade, mas preferência de cobre não define isolamento. Para um layout final, delimitar explicitamente a região de SW_NODE e restringir sua área ao caminho de corrente necessário; uma grande ilha com alto dv/dt aumenta acoplamento capacitivo. Preservar retorno curto entre gates e seus respectivos emissores, com conexão Kelvin quando viável.

Todas as zonas de potência usam conexão sólida aos pads. Isso evita spokes térmicos como gargalo, mas não comprova capacidade de corrente. O GND usa alívio térmico com gap e spokes de 0,50 mm. A espessura mínima de preenchimento de 0,25 mm também não garante largura adequada de um caminho de potência. Corrente RMS/pico, duração/repetição dos pulsos e cobre real precisam dimensionar os estrangulamentos.

## Tensões de projeto e critérios

Hipóteses pendentes de confirmação: operação em 127 e 220 Vac, altitude até 2.000 m, placa sem revestimento qualificado. Poluição, CTI do laminado, categoria de sobretensão e norma de produto ainda não foram definidos. Os números abaixo são critérios preliminares de revisão, não requisitos normativos fechados.

| Relação elétrica | Tensão relevante | Tratamento recomendado |
| --- | --- | --- |
| L–N e entrada da ponte | Rede RMS e surtos da instalação | Meta inicial de layout de 3 mm; validar clearance por impulso e creepage pela tensão de trabalho/material. |
| DC_PLUS–DC_MINUS | Cerca de 311 Vdc em 220 Vac retificado; cerca de 359 Vdc em 127 Vac dobrado | Usar envelope inicial de 400 Vdc para comparar layout; não representa limite de overshoot. |
| SW_NODE–rails e coletor–gate | Excursão próxima ao barramento, mais overshoot | Aplicar critério do barramento; minimizar laços e área de comutação. |
| GATE_H–SW_NODE e GATE_L–DC_MINUS | Tensão gate–emissor, não o barramento inteiro | Regra funcional específica; 0,5 mm como meta inicial, condicionada à tensão real de drive/transientes. |
| Qualquer potência/gate–lógica isolada | Tensão de modo comum e transientes | Manter 6,4 mm como meta existente e reavaliar o requisito de isolamento reforçado. Não reduzir por conveniência. |
| Net-(CPR1-Pad2) e conexão do tanque | Tensão ressonante ainda não especificada | Critério separado. Rating de 3 kV do capacitor não informa tensão operacional nem espaçamento necessário. |

Com +10% de rede, 220 Vac retificado dá aproximadamente 342 Vdc; 127 Vac dobrado dá aproximadamente 395 Vdc, sem considerar quedas, ripple ou overshoot. No segundo caso cada capacitor de 200 V pode ficar perto de 198 V mesmo com divisão ideal: margem insuficiente para presumir adequação sem revisar tolerâncias, desequilíbrio e alimentação máxima. J110 fechado em 220 Vac produziria aproximadamente 622 Vdc nominal; a configuração do jumper exige prevenção clara de montagem/operação incorreta.

Clearance é o caminho pelo ar; creepage é o caminho pela superfície. Máscara de solda comum não deve ser creditada automaticamente como isolamento qualificado. Um slot pode aumentar creepage, mas não garante aumentar clearance. Cobre em faces opostas exige também avaliar isolamento através do laminado, bordas, furos metalizados e componentes que atravessam a barreira.

As referências primárias explicam por que não existe uma distância única baseada só em volts:

- TI, creepage e clearance: https://www.ti.com/video/6146024211001
- Analog Devices, CTI e tensão de trabalho: https://www.analog.com/en/resources/technical-articles/comparative-tracking-index-and-working-voltage.html — exemplo de 400 Vrms, poluição 2 e grupo III requer 4 mm de creepage para isolamento básico. O exemplo não equivale à certificação deste circuito DC pulsado nem de sua barreira reforçada.

## Medições e teste de afastamento

DRC KiCad nativo, com refill em memória, sem `--save-board`:

- Placa atual: 44 violações e quatro conexões faltando; nenhuma ocorrência de clearance pelas regras atuais. Isso não valida isolamento em alta tensão.
- Cópia com apenas SW_NODE prioridade 5: uma conexão faltando; três desconexões da zona eliminadas.
- Cópia com SW_NODE prioridade 5 e classe Rede_Barramento de 3 mm: 37 ocorrências de clearance e duas conexões faltando. São ocorrências do DRC, incluindo pares repetidos por camada, não 37 defeitos únicos. Não houve ocorrência da regra potência–controle de 6,4 mm neste ensaio.

| Região/par | Distância medida pelo DRC | Interpretação |
| --- | --- | --- |
| AC_N em J110–trilha AC_L | 1,380 mm | Abaixo da meta preliminar de 3 mm; rerotear entrada AC. |
| AC_N–pads de F1 | 1,780 mm | Abaixo da meta; afastar trilha do neutro dos pads do fusível. |
| J1 L–N, pads | 1,880 mm | O footprint atual não comporta 3 mm entre pads. Rever borne/footprint com a peça real. |
| D4, pads adjacentes | 2,280 mm | Rever encapsulamento e critério específico; não diminuir pads sem conferir furo e anel. |
| D4, pad–trilha próxima | 2,180 mm | Roteamento pode piorar a separação já limitada do encapsulamento. |
| Q1 coletor DC_PLUS–trilha SW_NODE | 2,354 mm | Abaixo da meta de barramento. |
| Q1/Q2 gate–coletor | 1,950 mm | Pode haver quase todo o barramento entre esses terminais. Limitação do footprint precisa avaliação específica. |
| Q1/Q2 coletor–emissor | 2,950 mm | Ligeiramente abaixo da meta de 3 mm; confirmar critério antes de mexer em pads. |
| Q1 SW_NODE–trilha DC_MINUS | 2,398 mm | Abaixo da meta do barramento. |
| T1 GATE_L–DC_MINUS, pad–trilha | 1,495 mm | É gate–emissor de baixa tensão diferencial; não classificar automaticamente como falha de isolamento de 400 V. |
| T1 pares de cada secundário | 2,880 mm | Também gate–emissor; regra específica evita falsos conflitos de 3 mm. |

A regra genérica de 3 mm é útil para triagem, mas deve ser refinada por pares de redes. Ela superestima o requisito entre gate e seu próprio emissor e pode subestimar a necessidade do tanque ou da barreira de proteção. Na cópia, o clearance maior também interrompe uma conexão DC_MINUS: regras novas exigem reroteamento, não apenas refill.

Os totais das cópias incluem 40 avisos adicionais de biblioteca pela localização do projeto de teste sem tabelas locais. Eles não são defeitos novos no cobre; comparar os tipos relevantes e os relatórios JSON. Os experimentos não devem substituir o projeto ativo.

## Encaminhamento

1. Corrigir SW_NODE para prioridade 5 e fechar sua ligação até CPR1 em uma revisão de layout.
2. Recuperar regras por domínio e por pares: barramento, gate–emissor, barreira lógica e tanque ressonante. Expor conflitos, sem exclusões genéricas.
3. Rerotear entrada AC e pontos listados; selecionar conectores/encapsulamentos que comportem o critério final. Não resolver limitações físicas apenas reduzindo clearance no software.
4. Reavaliar isolação de T1/T3, dissipadores, fixadores e o tanque. Conferir se PE/chassis existe na montagem real: nesta placa não foi encontrado pad com net PE nomeada.
5. Confirmar rede máxima, transientes, altitude, poluição, CTI e norma; definir corrente/pulsos antes de dimensionar planos, trilhas e vias. Repetir DRC com refill depois do reroteamento.

Resultado: revisão CAD com conflito de prioridade confirmado e pontos de afastamento quantificados. A placa ainda não tem base suficiente para liberação de fabricação ou validação elétrica de alta tensão.
