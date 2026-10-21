# Porta-fusível F1 — Idall AS-06 5x20mm

Substituído o footprint incorreto de quatro furos/clipes Littelfuse pelo
footprint local `oneTesla:Fuseholder_Idall_AS-06_5x20mm_P20.20mm_Horizontal`.
Associação atualizada em F1 no esquemático, no PCB e nos defaults do
símbolo Fuse da biblioteca local/cache. O valor 4A/250VAC foi mantido.

Fonte: [Idall 0179 — AS-06](https://idall.com.br/fusivel-porta-fusivel/0179-porta-fusivel-as-06-5x20),
[desenho original](https://idall.com.br/image/catalog/Produtos/Porta-Fusivel/0179-D.jpg),
cópia local `idall-0179-drawing.jpg`.

- Corpo 26 × 9,6mm; courtyard 27,4 × 11mm.
- Dois pads: 1 em (+10,1; 0)mm = /AC_L; 2 em (-10,1; 0)mm = /AC_L_FUSED.
- Passo 20,2 ±0,3mm do desenho. Furos de 1,8mm/pads de 3,2mm selecionados
  para terminais de 1,3 ±0,1 × 0,4mm, com margem de montagem.
- Posição/rotação de F1 e todos os demais itens do PCB preservados.
- STEP fornecido associado por `${KIPRJMOD}/library/3dmodels/Fuse Holder.stp`.

## Limitação do STEP fornecido

O STEP contém dois sólidos, com terminais de 0,5 × 1,5mm cujos centros
estão a **22,5mm**, diferente dos **20,2mm** do AS-06 documentado.
O footprint segue o componente solicitado; o STEP fica como referência
visual aproximada, sem deformação. Rotação KiCad (-90, 0, 0)°, offset
(-7,167784602; 22,768333249; -8,10222232)mm e escala 1 centralizam os
terminais e colocam a base sobre a PCB. A vista inferior mostra o desvio.

## Conferência

Netlists antes/depois idênticas. Outras instâncias do esquema e outros
itens da PCB idênticos aos arquivos recebidos nesta etapa. ERC nativo:
duas notas `power_pin_not_driven` já existentes em PS1. O esquema recebido
voltou a usar IEC C6 em J1; essa instância foi preservada nesta troca de F1.

Evidências: `verification.json`, `final.net`, `erc.json`, footprint SVG,
`preview-3d.png` e `preview-bottom.png`. `preview.kicad_pcb` é uma placa
isolada somente para visualizar F1; não substitui o PCB principal.
