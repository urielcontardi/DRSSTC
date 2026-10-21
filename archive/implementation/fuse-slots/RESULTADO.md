# F1 com margem para terminais inclinados — 17/10/2026

Aplicado um footprint de montagem tolerante em lugar dos dois furos circulares de passo 20,2 mm. A alteração atende à solicitação de margem, sem assumir que a cota de 24,5 mm do desenho seja o passo dos terminais na PCB.

## Geometria

- Dois rasgos **metalizados de 4,4 × 1,8 mm**, alinhados ao comprimento do porta-fusível.
- Centros dos rasgos separados por **22,35 mm**, a média da faixa de acomodação escolhida (20,2–24,5 mm). Isso é uma escolha desta adaptação, não uma cota confirmada do fabricante.
- Pads de **6,0 × 3,2 mm**, com anel nominal mínimo de **0,70 mm** ao redor dos slots.
- Corpo F.Fab de 26 × 9,6 mm preservado; courtyard ampliado para conter os pads. Contorno de serigrafia aberto junto aos rasgos.
- Posição de F1, valor 4 A/250 VAC, números dos pads e redes AC_L/AC_L_FUSED preservados. Trilhas não foram movidas.
- Nova biblioteca: `Fuseholder_Idall_AS-06_5x20mm_Slotted_P22.35mm.kicad_mod`. Associação atualizada no PCB, esquema, cache e default do símbolo Fuse da biblioteca local. O footprint anterior continua disponível como histórico/alternativa.
- STEP mantido como referência visual aproximada; ele não define a furação.

Para o terminal máximo desenhado de 1,4 × 0,4 mm, a diagonal é aproximadamente 1,456 mm. Usando essa diagonal como envelope circular conservador, o centro do terminal pode deslocar-se cerca de ±1,472 mm ao longo de cada slot. A faixa alvo 20,2–24,5 mm exige ±1,075 mm por terminal, deixando aproximadamente **0,40 mm de margem adicional por terminal** nesse sentido, antes das tolerâncias da fabricação e da peça. Não é garantia de encaixe para dimensões fora da faixa adotada.

## Verificação

- Netlists nativas anterior/posterior idênticas em todas as redes e pinos.
- DRC depois do refill: **18 ocorrências de montagem, zero conexões faltando**, sem novos erros de clearance, anel PTH, serigrafia ou curto.
- Exportação Excellon conferida: o arquivo `drill-check/oneTesla-PTH.drl` contém os dois slots como **furos metalizados**, ferramenta de 1,8 mm e percurso longitudinal de 2,6 mm (comprimento total 4,4 mm). Coordenadas dos percursos: X72,425–75,025 e X94,775–97,375, Y35,1 mm.
- Os arquivos de furação em `drill-check` são evidência desta verificação, não um pacote de fabricação liberado.
- Comparação estrutural confirma que os demais pads, todas as trilhas/vias e as configurações de zonas foram preservados.

Prévia: `slot-detail.png`. Backups, DRCs e netlists nesta pasta. `apply.py` registra a edição e não deve ser reaplicado à placa atual.
