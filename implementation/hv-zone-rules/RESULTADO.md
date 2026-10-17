# Regras de tensão e zonas aplicadas — 17/10/2026

Alterados os arquivos ativos `oneTesla.kicad_pro`, `oneTesla.kicad_dru` e `oneTesla.kicad_pcb`. Backups do estado encontrado nesta execução estão nesta pasta. As alterações anteriores do usuário foram preservadas.

## Configuração

| Relação | Clearance | Creepage |
| --- | --- | --- |
| Redes de potência distintas, incluindo gate–coletor | 3 mm | 3 mm |
| Potência–controle e potência–cobre sem net | 6,4 mm | 6,4 mm |
| GATE_H–SW_NODE, somente este par | 0,5 mm | 0,5 mm |
| GATE_L–DC_MINUS, somente este par | 0,5 mm | 0,5 mm |
| Net-(CPR1-Pad2)–outras redes | 6,4 mm provisórios | 6,4 mm provisórios |

Criadas as classes Rede_Barramento (sete redes), Gates_Potencia (duas redes) e Tanque_Ressonante (uma rede). Default permanece em 0,20 mm, também definido como mínimo global. As regras por nome de rede protegem os limites críticos mesmo se uma associação de classe for perdida. As exceções específicas de gate–emissor ficam por último, conforme a precedência do KiCad, e não se aplicam a gate–coletor ou à lógica.

Os valores são metas preliminares para 127/220 Vac e envelope de barramento de 400 Vdc, sem revestimento qualificado, altitude até 2.000 m. Não são uma declaração de conformidade. A reserva de 6,4 mm do tanque não representa dimensionamento para 3 kV: depende da tensão ressonante e dos transientes ainda não especificados. Larguras e correntes não foram dimensionadas por essas classes; os presets herdados não constituem capacidade de corrente.

SW_NODE está com prioridade 5. As outras prioridades encontradas nesta execução foram preservadas: GND 0, DC_MINUS 1, DC_PLUS 2 e DC_MID 3. Zonas recalculadas e salvas pelo KiCad nativo. SW_NODE termina com um único polígono preenchido, conectado.

Fechada a ligação SW_NODE até CPR1.1 com dois segmentos de 2,5 mm em B.Cu. Reconectado o retorno DC_MINUS interrompido pelo maior afastamento do preenchimento, com quatro segmentos de 0,5 mm em F.Cu até Q2.3. Esse retorno é a conexão do drive/emissor; não substitui o dimensionamento do caminho principal de potência ou a otimização do laço de gate.

## Verificação

DRC KiCad nativo com `--all-track-errors --refill-zones`; no resultado final também `--save-board`:

- Estado encontrado nesta execução: 42 violações, uma conexão faltando.
- Após regras e refill, antes das reconexões: 86 violações, duas conexões faltando.
- Final: **85 violações, zero conexões faltando**, incluindo **29 de clearance e 14 de creepage**.
- Nenhuma nova ocorrência de clearance, creepage, curto ou cobre–borda foi introduzida pelas seis trilhas de reconexão em relação ao resultado com as regras já aplicadas.
- Comparação estrutural confirma que footprints, vias e todas as trilhas anteriores estão preservados.

O aumento de violações expõe afastamentos que antes passavam com Default 0,20 mm. Permanecem limitações físicas em J1, D4, Q1/Q2 e roteamento da entrada AC. Não foram criadas exclusões para ocultá-las. As demais ocorrências finais são serigrafia, courtyards, anéis PTH e pontas de trilha/via existentes.

Os JSON `drc-before.json`, `drc-after.json` e `drc-final.json` conservam as posições e UUIDs. As distâncias detalhadas e as hipóteses elétricas estão em `review/zones-2026-10-17/REVISAO.md`; seus totais antigos não representam este estado final.

Próxima etapa física: rerotear os pontos abaixo da meta e revisar conectores/encapsulamentos onde o próprio passo limita a distância. Não liberar fabricação enquanto esses conflitos e o dimensionamento de isolamento estiverem pendentes.

Referências consultadas:

- [KiCad 10 — regras e precedência](https://docs.kicad.org/10.0/en/pcbnew/pcbnew.html#custom-design-rules).
- [Analog Devices — CTI, tensão e creepage](https://www.analog.com/en/resources/technical-articles/comparative-tracking-index-and-working-voltage.html). O exemplo de isolamento básico em 400 Vrms não é uma homologação desta placa DC pulsada.
