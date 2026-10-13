# Modelos 3D adicionados

Aplicados ao **PCB principal `oneTesla.kicad_pcb`** e aos nove footprints locais correspondentes: **14 componentes antes sem modelo, mais o vínculo quebrado de FB1 corrigido**. Os 35 componentes que possuem vínculos agora apontam para arquivos existentes. [Prévia do PCB principal](preview.png).

Correção de destino: as associações adicionadas à cópia autorroteada foram revertidas, preservando suas trilhas e posições. O script agora aplica modelos apenas ao PCB principal. R1 também passou à montagem vertical: [resultado e validação atuais](../r1-vertical/RESULTADO.md).

| Referências | Modelo aplicado | Fidelidade |
| --- | --- | --- |
| FB1 | HFBR-2521ETZ do catálogo EasyEDA | Mesmo código; alinhados os quatro terminais elétricos. A fileira dos dois pinos de retenção no STEP está a 7,70 mm, frente a 7,62 mm no footprint. |
| Q1, Q2 | Corpo FGA60N65SMD do catálogo, adaptado à montagem horizontal | Corpo de catálogo; dobra e altura dos terminais são aproximações. |
| PS1 | Família encapsulada HLK-15M do catálogo | Aproximação visual; não confirma a versão BL. Não foi usado o modelo de 3 W presente na pasta. |
| C8, C9, C13 | Capacitor radial Ø8 mm, passo 2,54 mm | Genérico KiCad, terminais adaptados; altura provisória de 8 mm. |
| C10 | Capacitor radial Ø12,5 mm, passo 3,556 mm | Genérico KiCad, terminais adaptados; altura provisória de 12,5 mm. |
| C11, C12 | Capacitor radial Ø30 mm, passo 10,16 mm | Genérico KiCad, terminais adaptados; altura provisória de 30 mm. |
| R5, R6 | Resistor axial L9 × Ø3,2 mm, passo 10,16 mm | Genérico KiCad adaptado. |
| Z1, Z2 | TVS DO-201AD, passo 14,732 mm | Genérico KiCad adaptado, sem indicação de polaridade. |
| CPR1 | Envelope CDE 940C30S68K-F Ø19 × L46 mm, passo formado 58,42 mm | Gerado a partir do desenho CDE; altura e dobras provisórias. |

**Ainda sem modelo:** T1 e T3, sem geometria confiável identificada; J110, jumper de fio sem forma de montagem definida. P1/P2 são pontos de solda; os quatro furos também não precisam de corpo 3D. Os modelos novos aproximados não certificam encaixe mecânico nem eliminam interferências existentes no posicionamento.

## Conferência

As alterações realizadas por `apply_models.py` preservam integralmente a árvore do PCB quando os blocos `model` são removidos da comparação. Pads, furos, contorno, posições, redes e trilhas não são alterados por esse script. O PCB principal foi salvo externamente com alterações de layout entre aplicações; a correção preservou o conteúdo atual, comparando a entrada com a saída. Por isso `initial_snapshot_matches` é falso no PCB principal. A alteração posterior de R1 e dos seus campos no esquemático está documentada separadamente em `implementation/r1-vertical`.

Os sete STEP genéricos gerados foram reimportados e tiveram sólidos/volume validados. O PCB principal foi renderizado pelo KiCad 10 e a prévia foi inspecionada. Auditoria de arquivos associados em [audit.json](audit.json); prova da aplicação dos modelos em [verification.json](verification.json). DRC e prova final, incluindo R1 vertical, em [r1-vertical](../r1-vertical/RESULTADO.md).

Z1/Z2 já estão marcados como DNP no PCB: seus modelos estão associados, mas a renderização padrão do KiCad omite esses componentes. Essa marcação foi preservada.

## Fontes

- Modelos de catálogo: JLCEDA/EasyEDA Official Library — [EasyEDA](https://easyeda.com), [JLCEDA](https://lceda.cn). Códigos, URLs e hashes dos arquivos originais em [catalog-sources.json](catalog-sources.json).
- Modelos genéricos: biblioteca [KiCad packages3D](https://gitlab.com/kicad/libraries/kicad-packages3D). Arquivos e dimensões em [sources.json](sources.json), avisos de licença em `library/3dmodels/KiCad-derived-models-NOTICES.txt`.
- Envelope de CPR1: [desenho da série CDE 940C](https://www.cde.com/resources/catalogs/940C.pdf).

Os arquivos `Catalog_*.step` mantêm os downloads originais; `Visual_*.step` identificam explicitamente os modelos gerados/adaptados. Caminhos de associação usam `${KIPRJMOD}/library/3dmodels`.
