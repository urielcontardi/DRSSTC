# IC6 — onsemi MC7805BDTRKG em DPAK

IC6 foi substituído no esquema e na PCB principal por MC7805BDTRKG, footprint `oneTesla:TO-252-3_TabPin2` e STEP local. Conforme a tabela de pedidos do [datasheet onsemi MC7800](https://www.onsemi.com/download/data-sheet/pdf/mc7800-d.pdf), página 21, **MC7805BDTRKG é DPAK/TO-252**. O título do anúncio que cita TO-263 conflita com esse código; a seleção segue o código informado. A versão D2PAK/TO-263 usa o código MC7805BD2TR4G.

Pinagem preservada: 1 IN/+15V, 2 GND, 3 OUT/+5V; aba no pino2/GND. UUIDs originais dos pads preservados, com uma ilha adicional2/GND e aberturas de pasta do padrão KiCad. Posição do footprint (49,0;87,1)mm, rotação -90°, ajustada ao espaço disponível. O cobre para dissipação deve ser definido no roteamento final; a troca de footprint não dimensiona a dissipação térmica.

C10 continua 680 µF/35 V. Esse valor foi herdado do antigo filtro da alimentação retificada, substituída pelo módulo Hi-Link; hoje está no barramento +15V junto aos drivers, não serve apenas ao 7805. Para o regulador isoladamente, o datasheet apresenta 0,33 µF na entrada e saída opcional para resposta transitória (se instalada, evitar valores abaixo de0,1 µF). Os capacitores do barramento devem considerar os pulsos dos drivers, ripple e resposta da fonte; nenhuma redução de capacitância foi aplicada nesta troca.

Verificação conjunta com C8/C9/C13: netlist idêntica, 17 trilhas preservadas, PCB autorouted inalterada. DRC 23 → 22, nenhuma nova ocorrência física. 92 → 93 conexões não roteadas, devido à ilha GND adicional do footprint DPAK, ainda sem roteamento.

[verification.json](verification.json) · [preview.png](preview.png)
