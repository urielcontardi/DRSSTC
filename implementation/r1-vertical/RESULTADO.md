# PCB principal: modelos 3D e R1 vertical

Arquivo aplicado: **`oneTesla.kicad_pcb`**. Os vínculos 3D de 14 componentes foram reaplicados ao conteúdo atual da placa, e o vínculo quebrado de FB1 foi corrigido. Os 35 componentes associados agora têm arquivos existentes. As aproximações e fontes permanecem documentadas em [modelos 3D](../models3d/RESULTADO.md).

As associações adicionadas por engano a `oneTesla-autorouted.kicad_pcb` foram revertidas para as associações anteriores àquela etapa, preservando toda a geometria e as 241 trilhas dessa cópia. Seu R1 continua horizontal. Os scripts de aplicação de modelos agora apontam apenas para o PCB principal.

## R1 de 1 kΩ / 5 W

- Novo footprint local: `oneTesla:R_Axial_Vishay_AC05_L18.0mm_D7.5mm_P10.16mm_Vertical`.
- Centro e orientação mantidos em `(53.3, 161.2)` mm, 180°; passo reduzido de 23,4 para **10,16 mm**.
- Pads 1/2 mantêm redes, UUIDs, diâmetro de 2,4 mm e furo de 1,2 mm. O corpo fica sobre o pad 1; o terminal superior retorna pelo lado até o pad 2.
- Corpo original de `vishay_AC05.step` reorientado; terminais Ø0,8 mm gerados para a montagem. Folga mínima visual de **3 mm** sob o corpo e altura máxima de **26,4 mm**. Dobra, folga e passo são escolhas de montagem, não uma variante pré-formada certificada pelo fabricante. [Dimensões extraídas](model.json).
- Footprint e instruções de montagem de R1 sincronizados no esquemático, sem alteração de fios ou conectividade.

R1 já estava sem trilhas conectadas no PCB principal; nenhum trecho precisou ser refeito. As 17 trilhas existentes, todos os demais componentes, o contorno e os quatro furos foram preservados. A montagem deve ser conferida com o resistor adquirido e quanto à dissipação real; a [Vishay](https://www.vishay.com/docs/28730/ac_ac-at_ac-ni.pdf) especifica redução da potência com a temperatura e afastamento térmico dos componentes vizinhos.

## Validação

Comparação estrutural em [verification.json](verification.json): somente a geometria/associação de R1 mudou, além dos blocos de modelos 3D dos componentes já previstos. O esquema mudou apenas nos quatro campos de R1 referentes ao footprint e montagem. STEP reimportado e validado; PCB renderizado pelo KiCad 10 e [prévia inspecionada](preview.png).

DRC antes/depois: **20 ocorrências e 92 conexões pendentes em ambos**, sem novas ocorrências por tipo e UUID dos itens envolvidos. O PCB principal continua parcialmente roteado. Relatórios [antes](drc-before.json) e [depois](drc-after.json).

Para carregar esta revisão, reabra `oneTesla.kicad_pcb` a partir do arquivo salvo; uma janela antiga pode conter uma versão anterior em memória.
