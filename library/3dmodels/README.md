# Modelos 3D

Guarde aqui os modelos STEP (`.stp`/`.step`) dos componentes do projeto.
Nos footprints do KiCad, use caminhos relativos ao projeto:

```text
${KIPRJMOD}/library/3dmodels/2EDGRC-5.08-02P.stp
```

## R1 e IC6

`vishay_AC05.step` está associado a R1, Vishay AC05 1k/5W. O footprint usa corpo18×Ø7,5mm, furos1,2mm e passo de montagem23,4mm para formar os terminais como no STEP. Modelo em escala1, rotaçãoX=-90°, offset0; corpo elevado3,75mm sobre a placa. [Conferência](../../implementation/ac05-r1/RESULTADO.md).

`TO-220-3_Vertical.step` é a cópia local do modelo padrão KiCad associada a IC6/L7805CV, com pinagem1IN/2GND/3OUT. [Conferência](../../implementation/7805-to220/RESULTADO.md).

## Entrada AC — J1

Componente aplicado: **borne plugável macho 2EDGRC-5.08-02P, 90°, 2 pinos**.
J1 recebe L/N; a entrada externa de PE fica diretamente em J2/CHASSIS.

| Arquivo | Identificação no STEP | Uso previsto |
| --- | --- | --- |
| `2EDGRC-5.08-02P.stp` | 2EDGRC-5.08-02P; corpo e duas instâncias de terminal; unidades em mm | Modelo associado a J1 no footprint local e no PCB |

O nome comercial informado é **2EDGRC-5.0**; o arquivo identifica a versão
**5.08**. O footprint usa 5,08 mm; confirmar o passo da peça comprada.
O modelo foi preservado como recebido, sem escala ou alteração de geometria.

O footprint local é
`oneTesla:TerminalBlock_2EDGRC-5.08_1x02_P5.08mm_Horizontal`.
Pinagem definida pelo projeto: **1 = L, 2 = N**. Origem no pad 1;
pad 2 em `(5.08, 0)` mm. O STEP tem os terminais em `x = ±2.54` mm:
o vínculo 3D usa deslocamento `(2.54, 0, 0)` mm, escala 1 e rotação 0.
A boca do borne aponta para a borda superior do PCB.

O envelope foi extraído da montagem STEP: corpo com 11,4 mm de largura,
12,1 mm de profundidade e 8,2 mm de altura; terminais quadrados de 1 mm.
Furos de 1,6 mm e pads de 3,2 mm são escolhas de layout para esses terminais,
pendentes de conferência com a peça comprada. O STEP não traz o sufixo
completo nem especificações elétricas. Referência da família:
[DEGSON 2EDGRC-5.08-02P](https://www.degson.com/content/details_552_882388.html?lang=en).

Uma eventual versão de 3 pinos exige outro footprint e outro STEP.

## Porta-fusível — F1

Footprint `oneTesla:Fuseholder_Idall_AS-06_5x20mm_P20.20mm_Horizontal`:
Idall AS-06 5x20mm, dois terminais, passo 20,2mm, envelope 26 × 9,6mm.
Furos de 1,8mm e pads de 3,2mm são escolhas de layout para terminais de
1,3 ±0,1 × 0,4mm. Fonte: desenho 0179 da Idall, copiado em
`implementation/fuse-as06/idall-0179-drawing.jpg`.

Modelo recebido `Fuse Holder.stp`, preservado intacto, associado por
`${KIPRJMOD}/library/3dmodels/Fuse Holder.stp`, escala 1, rotação KiCad
(-90, 0, 0)°, offset (-7,167784602; 22,768333249; -8,10222232)mm.
O modelo usa unidades STEP em metros, convertidas automaticamente pelo KiCad.

**O STEP é uma referência visual aproximada:** seus terminais estão a
22,5mm, enquanto o desenho do AS-06 indica 20,2 ±0,3mm. A geometria não
foi deformada para aparentar encaixe; não usar esse STEP para definir a
furação. Pré-visualizações superior e inferior estão em
`implementation/fuse-as06/`.
