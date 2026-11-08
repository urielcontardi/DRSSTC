# Manutenção

Mantenha apenas o estado atual do projeto na árvore. Use commits, tags e o
histórico do Git para consultar revisões anteriores; não crie pastas por versão
nem mantenha ZIPs históricos no repositório.

| Conteúdo | Local |
| --- | --- |
| Esquemático, layout e bibliotecas | `hardware/pcb/` |
| Gerbers, DRC e montagem STEP da PCB | `hardware/pcb/exports/` |
| Geometria e parâmetros do gabinete | `mechanical/` |
| Montagem STEP, componentes e relatórios | `mechanical/exports/` |
| STLs com quantidades nos nomes | `mechanical/print/` |
| Cálculos e documentação | `docs/` |
| ZIPs gerados e resultados temporários | `output/` (ignorado) |

Antes de fazer commit:

1. Execute as verificações correspondentes à mudança, conforme o guia da área.
2. Confira as fontes, exportações e relatórios afetados.
3. Atualize links e scripts ao mover arquivos.
4. Execute `git diff --check` e revise `git status --short`.

Preserve os caminhos relativos das bibliotecas KiCad e os avisos de origem dos
modelos de terceiros. Backups do editor, caches e ambientes locais ficam fora do Git.
