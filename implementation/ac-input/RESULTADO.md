# Entrada AC — borne 2EDGRC, 2026-10-11

J1 foi substituído por **2EDGRC-5.08-02P macho 90°, 2 pinos** no
esquemático e no PCB, usando o STEP fornecido. **1 = L, 2 = N**;
PE entra externamente direto em **J2/CHASSIS**, separado de GND e DC_MINUS.

## Alterações

- Símbolo local `oneTesla:AC_Input_2EDGRC_2P`, com dois pinos; removidos
  o pino PE do antigo IEC e seu ramal de fio/rótulo no esquema.
- Footprint local `TerminalBlock_2EDGRC-5.08_1x02_P5.08mm_Horizontal`:
  passo 5,08 mm, furos selecionados de 1,6 mm, pads de 3,2 mm. O STEP
  contém terminais quadrados de 1 mm e corpo de 11,4 × 12,1 × 8,2 mm.
- J1 na posição `(54.625, 11.071)` mm, com a boca voltada para a borda
  superior. Pad N preserva a posição anterior; trilhas de L e ramal N
  adaptados. Furos de fixação do IEC e cobre PE que ia até J1 removidos.
- STEP guardado em `library/3dmodels/` e associado na biblioteca e no PCB
  via `${KIPRJMOD}/library/3dmodels/2EDGRC-5.08-02P.stp`, com deslocamento
  X de 2,54 mm, escala 1 e rotação 0. O arquivo STEP permaneceu inalterado.
- Legenda 110V reposicionada; notas de montagem de J1/J2 atualizadas.
  Validador atualizado para dois pinos de J1 e PE externo em J2.

## Verificação

KiCad 10.0.5 nativo: zonas preenchidas, netlist/PDF exportados, ERC,
DRC com paridade e renderização 3D. Arquivos finais na raiz do projeto.

| Verificação | Resultado |
| --- | --- |
| Netlist | A única mudança de membros das redes é a remoção de J1.3 de PE |
| Outras peças | Posições, geometria dos pads e redes preservadas |
| Conexões abertas | **0** |
| Curto, afastamento de cobre, furo/cobre e cobre/borda no DRC | **0** |
| DRC | **73** ocorrências, contra 84 antes; todas de silk/courtyard |
| Paridade | Apenas footprints extras JPRT1/JPRT2, já existentes |
| ERC | 2 notas PS1 `power_pin_not_driven` + 1 `isolated_pin_label` em PE |

A nota de PE indica que J2 é o único pino da placa nessa rede, pois o fio
de proteção chega externamente. Não foram adicionados power flags,
exclusões ou relaxamentos de regras.

Evidências: `invariants.json`, `final.net`, `validation.txt`, `erc.json`,
`drc-before.json`, `drc.json` e `pcb-3d.png`. O PDF atualizado fica em
`output/oneTesla-schematic.pdf`.

## Conferência da peça

O anúncio informado cita **5,0 mm**, enquanto o STEP é **5,08 mm**.
O projeto segue o STEP; confirmar passo, sufixo, furação e especificações
da peça comprada. Furos/pads são escolhas de layout, não dados certificados
pelo STEP. A variante de 3 pinos exigiria outro footprint/modelo.
As demais pendências mecânicas e elétricas do projeto continuam registradas
nos relatórios anteriores; esta troca não constitui aprovação de fabricação.
