# Entrada AC atual — 2EDGRC-5.08-02P

J1 atualizado no esquemático e PCB atual para o borne de dois pinos:
**1 = L (/AC_L), 2 = N (/AC_N)**. PE entra externamente em J2/CHASSIS.
Símbolo local `oneTesla:AC_Input_2EDGRC_2P`, com footprint associado
`oneTesla:TerminalBlock_2EDGRC-5.08_1x02_P5.08mm_Horizontal`.

Footprint THT: passo 5,08 mm, furos selecionados de 1,6 mm, pads de 3,2 mm,
contornos F.Fab/F.SilkS/F.CrtYd e identificação L/N. Modelo associado no
footprint e no PCB por `${KIPRJMOD}/library/3dmodels/2EDGRC-5.08-02P.stp`,
offset X 2,54 mm, escala 1, rotação 0. O STEP foi mantido intacto.

Conferência por netlist nativa: única alteração elétrica é a remoção de
J1.3 da rede PE. Todos os demais itens do PCB foram preservados, incluindo
posições e pads das outras peças. O PCB recebido nesta etapa está sem
trilhas e sem contorno fechado; não foi feito roteamento nesta troca.

ERC nativo KiCad 10.0.5: duas notas preexistentes `power_pin_not_driven`
nos pinos AC de PS1 e uma `isolated_pin_label` em PE, pois J2 é o único
pino da placa nessa rede. Nenhuma regra ou exclusão foi alterada.

Evidências desta etapa: `verification.json`, `final.net`, `erc.json`,
`pcb-3d.png` e SVG em `footprint/`. PDF atualizado em
`output/oneTesla-schematic.pdf`. Os relatórios no diretório pai descrevem
um layout anterior e não representam o PCB atual.

Furos e pads são escolhas de layout a conferir com a peça física.
