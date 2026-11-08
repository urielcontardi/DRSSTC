# Manutenção do projeto

## Onde alterar

| Conteúdo | Local |
| --- | --- |
| Esquemático, layout e bibliotecas | `hardware/pcb/` |
| Geometria e parâmetros do gabinete | `mechanical/<revisão>/` |
| Entradas e resultados do ressonador | `docs/design/` |
| Caderno técnico | `docs/project/document.template.html` e seu gerador em `scripts/` |
| Entregáveis identificados por revisão | `production/` |
| Experimentos e arquivos temporários | `output/` (ignorado) |

Preserve os caminhos relativos das bibliotecas KiCad e as referências entre
revisões mecânicas. Não remova modelos ou footprints apenas por não aparecerem
na montagem atual: podem ser dependências das fontes ou revisões anteriores.

## Antes de registrar uma alteração

1. Execute a validação correspondente à mudança; consulte os guias da PCB,
   da revisão mecânica ou das ferramentas.
2. Revise os arquivos gerados e os relatórios. Registre fontes e exportações
   correspondentes quando atualizar uma revisão.
3. Atualize os índices e links ao mover arquivos ou definir uma nova revisão atual.
4. Execute `git diff --check` e confira `git status --short` antes do commit.

Mantenha backups do editor, caches Python, ambientes locais e saídas temporárias
fora do Git. Arquivos CAD, STLs, imagens de inspeção e pacotes de entrega são
artefatos úteis quando têm função documentada.

Pacotes históricos ZIP e manifests de hashes representam entregas específicas.
Publique uma nova revisão quando houver mudanças de fabricação; mantenha os
pacotes e seus manifests consistentes. Preserve os avisos de origem e licença
junto aos modelos de terceiros.
