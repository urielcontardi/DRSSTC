# Footprint snap-in Ø30,3 × 40,5 mm, passo 9 mm

Criado na biblioteca local: `CP_SnapIn_D30.3_H40.5_P9.00_ReviewPending`. Pad 1 positivo retangular, pad 2 negativo circular; centros ±4,5 mm. Corpo F.Fab Ø30,3, silk Ø30,54 e courtyard Ø30,8 mm. Furos Ø2 mm/pads Ø4 mm mantidos como provisórios: a seção dos terminais snap-in exige o desenho da peça. Não foi associado modelo 3D antigo de dimensões incorretas.

**Ainda não aplicado ao projeto ativo.** O usuário informou 10000µF/250V, enquanto o circuito usa 1000µF/200V. Pergunta pendente sobre capacitância real e identificação/link da peça. Aumento de dez vezes não é mera troca de footprint; exige avaliar carga, partida, retificador e fusível.

Estudo mecânico em `mechanical-preview.kicad_pcb`, sem modificar a raiz. Essa cópia não é de fabricação: não foi reroteada, não altera os valores elétricos anteriores e não resolve as interferências.

Nas posições atuais, os centros de C11/C12 distam 25,995 mm. Corpos de Ø30,3 mm se sobrepõem **4,305 mm**. C11 também ultrapassa a borda direita em **1,525 mm**. É necessário reposicionar componentes e rever cobre, não apenas mudar os passos. Medições em `geometry.json`.

A biblioteca geométrica está preparada. A seleção elétrica e o layout dependem da resposta sobre a peça; nenhuma aprovação para fabricação.
