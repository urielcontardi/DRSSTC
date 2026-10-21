# D1/D2 — 1N4148WS

D1 e D2 na placa principal e no esquema passaram de 1N4148 THT para **1N4148WS**, footprint local `oneTesla:D_SOD-323_HandSoldering`, com STEP local. O sufixo WS em SOD-323 foi conferido no [datasheet de referência](https://www.vishay.com/docs/86455/1n4148ws.pdf); nenhum fabricante específico foi atribuído à BOM.

Pad 1 é cátodo e pad 2 é ânodo. Mantidos os centros dos corpos, as rotações, as redes, as funções e os UUIDs dos pads. D1: K na rede Net-(D1-K), A em GND; D2: K em +5V, A na rede Net-(D1-K). Todas as demais geometrias e a placa autorouted foram preservadas.

Netlist idêntica, 34 redes e 130 conexões. DRC sem novas ocorrências; valores numéricos em [verification.json](verification.json). Prévia: [preview.png](preview.png).
