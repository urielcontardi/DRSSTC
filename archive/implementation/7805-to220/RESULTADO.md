# IC6 — L7805CV em TO-220

O antigo 78L05 TO-92 foi substituído por L7805CV no esquema e no PCB. Símbolo local `oneTesla:L7805`, footprint `oneTesla:TO-220-3_Vertical` e modelo `${KIPRJMOD}/library/3dmodels/TO-220-3_Vertical.step`.

Pinagem conforme [ST L78, página 3](https://www.st.com/resource/en/datasheet/l78.pdf): **1 IN = +15V, 2 GND, 3 OUT = +5V**; aba metálica ligada a GND. Como o 78L05 anterior tinha OUT1/GND2/IN3, os pinos 1/3 foram remapeados no símbolo e nas redes dos pads. A posição absoluta do pad GND foi preservada. O footprint padrão KiCad usa passo 2,54mm e furos de 1,1mm.

[verification.json](verification.json) registra a comparação dos netlists antes/depois: apenas os pinos 1/3 de IC6 mudaram de número, mantendo a alimentação de entrada/saída. Os demais footprints foram preservados nessa troca. A conferência final conjunta está em [R1](../ac05-r1/verification.json).
