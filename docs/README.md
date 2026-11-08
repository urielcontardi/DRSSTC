# Documentação técnica

| Conteúdo | Referência |
| --- | --- |
| Caderno HTML com cálculos, guia do secundário e visualizador offline | [Caderno do projeto](project/PROJECT-DRSSTC.html) |
| Projeto das bobinas, hipóteses e faixa de sintonia | [COILS.md](design/COILS.md) |
| Estudo do condutor primário | [PRIMARY-CONDUCTOR.md](design/PRIMARY-CONDUCTOR.md) |
| Entradas reproduzíveis dos cálculos | [resonator-inputs.json](design/resonator-inputs.json) |
| Resultados dos cálculos | [resonator-results.json](design/resonator-results.json) |
| Referências originais, manuais, datasheets e arquivos Eagle | [reference/](reference/) |
| Fontes e montagem do gabinete | [Índice mecânico](../mechanical/README.md) |
| Exportações da PCB | [Gerbers, relatórios e STEP](../hardware/pcb/exports/) |

O caderno é gerado a partir de `project/document.template.html` pelo script
`build_project_document.py`. Comandos e dependências estão no
[guia de ferramentas](../scripts/README.md).

`project/assets/` contém cópias de referências e dados para uso offline.
Esses arquivos fazem parte da distribuição do caderno; mantenha sua geração
sincronizada com as fontes. O gerador usa os dados de visualização em `project/viewer/`, sem depender de
ZIPs ou revisões anteriores. O ZIP offline é gerado em `output/`.
