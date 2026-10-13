# R1/R4 THT e C10 de 100 µF

Aplicado no PCB principal `oneTesla.kicad_pcb` e sincronizado no esquema:

| Referência | Resultado |
| --- | --- |
| R1 | 1kΩ/5W, THT vertical, footprint anterior `R_Axial_Vishay_AC05_L18.0mm_D7.5mm_P10.16mm_Vertical`; modelo STEP local anterior. |
| R4 | 3R3, THT axial DIN0207, corpo6,3×Ø2,5mm, passo7,62mm; footprint anterior restaurado. |
| C10 | 680µF → 100µF, tensão35V; mesmo footprint SMD genérico Ø8×10mm de C8/C9/C13, modelo STEP local. Dimensões Capxon continuam assumidas. |

R1 mantém a posição que ocupava como SMD: (44,5;151,0)mm, rotação90°. A posição anterior de sua montagem vertical conflita com FB1 e a serigrafia do furo após as alterações recentes de layout. R4 recupera a origem anterior (76,4;94,08)mm, com o mesmo centro físico do corpo e rotação−90°. C10 mantém o centro (38,625;86,55)mm, pino1 positivo em+15V e pino2 emGND.

O [datasheet Hi-Link 15W-BL](../../misc/HLK-15W-BL_V1.0.pdf), seção8, recomenda um eletrolítico externo de100–220µF na saída do módulo. Para15V, seção5.5, especifica ripple/ruído até100mVpp, medido com10µF+0,1µF na carga e banda20MHz. A fonte não zera o ripple nem substitui os capacitores locais dos drivers. C8 e C13 permanecem100µF cada em+15V; com C10 de100µF, são300µF eletrolíticos externos distribuídos nessa linha, além dos cerâmicos existentes.

A redução é uma escolha de projeto coerente com a nova fonte, ainda sujeita à medição dos transientes de15V sob o acionamento real do GDT. Não foi feita validação elétrica em bancada ou simulação do controle da fonte. O [datasheet TI UCC37321](https://www.ti.com/lit/ds/symlink/ucc37321.pdf), seção10, trata separadamente o desacoplamento cerâmico próximo aos pinos de alimentação.

Conferências finais:

- **34 redes / 130 conexões** preservadas integralmente.
- Pinos, redes e UUIDs dos pads dos três componentes preservados.
- Todos os demais objetos da PCB, incluindo17 trilhas, contorno e quatro furos, preservados.
- DRC: **22 → 22**, sem ocorrências novas; conexões pendentes: **93 → 93**.
- Removidos a pedido: `oneTesla-autorouted.kicad_pcb`, `.kicad_pro` e `.kicad_prl`. Arquivos de evidência de etapas anteriores não são placas ativas.

Relatórios nativos, netlists e comparação estão nesta pasta.
