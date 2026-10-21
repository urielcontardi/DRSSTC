# C8/C9/C13 — Capxon 100 µF/35 V SMD

Aplicados no esquema e na PCB principal: 100 µF/35 V, footprint local padrão `oneTesla:CP_Elec_8x10`, com STEP local. O usuário autorizou um footprint genérico sem código/medidas da peça; Ø8 × 10mm é uma suposição de layout, não uma dimensão confirmada do capacitor comprado.

Pad1 positivo: C8/C13 em +15V e C9 em +5V; pad2 negativo em GND. Mantidos números, redes, funções e UUIDs dos pads. C8 foi deslocado -0,5mm em X/-0,9mm em Y e C13 -0,7mm em Y para liberar os pads/courtyards. C9 mantém o centro original. Outros capacitores, inclusive C10, permanecem inalterados.

A troca foi validada junto com IC6 em DPAK. Netlist idêntica (34 redes/130 conexões), todas as 17 trilhas originais preservadas e nenhum objeto fora de C8/C9/C13/IC6 alterado. Placa autorouted idêntica por SHA-256. DRC físico: 23 → 22 ocorrências, nenhuma nova. Não roteados: 92 → 93 porque o footprint do regulador contém duas ilhas GND separadas (terminal e aba); o roteamento permanece pendente.

[verification.json](verification.json) · [preview.png](preview.png)
