# Contorno da placa e quatro furos M3

Aplicado diretamente em `oneTesla.kicad_pcb`, mantendo os 41 componentes existentes, posições, rotações, pads, redes e demais objetos originais.

- Placa retangular: **110 × 160mm**, contorno fechado na camada `Edge.Cuts`, de (-102, 13) a (8, 173)mm.
- Quatro furos **Ø3,2mm NPTH**, sem metalização, para parafusos M3.
- Centros a **5mm das duas bordas adjacentes**; malha entre centros de **100 × 150mm**.
- H1 = (-97, 18); H2 = (3, 18); H3 = (-97, 168); H4 = (3, 168)mm.
- Footprint local `oneTesla:MountingHole_3.2mm_M3`, cópia do padrão KiCad, com área mecânica Ø6,4mm e courtyard Ø6,9mm. A menor folga entre esse courtyard e as caixas dos componentes é 1,111mm, junto de J2.
- H1–H4 foram adicionados só ao PCB, bloqueados e excluídos da BOM e dos arquivos de posição. Ao sincronizar pelo esquema, manter desmarcada a opção de excluir footprints sem símbolos.

Conferência em [verification.json](verification.json): o KiCad extrai um único contorno fechado válido; toda a geometria dos componentes está dentro da placa; furos e área de montagem não colidem com os componentes. A comparação do arquivo confirma que todos os objetos originais foram preservados, com oito objetos adicionados: quatro segmentos de contorno e quatro footprints mecânicos.

Prévia: [vista superior](pcb-top.png), [layout vetorial](layout.svg). Não foi necessário mover componentes.

O DRC completo não pôde ser concluído: a CLI do KiCad encerra com código133 e erro Swift `Array index out of range`, tanto na placa anterior quanto na versão com contorno, inclusive fora das configurações do projeto. A extração nativa do contorno, a renderização e as verificações geométricas passaram. A placa continua sem roteamento; esta alteração define apenas o contorno e a fixação.
