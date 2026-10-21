# ARCSTRIKE / DRSSTC

Projeto eletrônico KiCad e estudo mecânico da case para impressão 3D.

## Abrir o projeto

| Objetivo | Arquivo |
| --- | --- |
| Editar PCB e esquema no KiCad | [oneTesla.kicad_pro](oneTesla.kicad_pro) |
| Abrir todo o conjunto no Fusion 360 | [Case + PCB + dissipador + C14 — STEP](mechanical/case-v1/exports/ARCSTRIKE-case-v1-CONCEPT.step) |
| Abrir somente a PCB montada | [PCB completa — STEP](production/pcb/2026-10-20-3d/ARCSTRIKE-PCB-completa.step) |
| Ver a case no navegador | [Visualizador offline](mechanical/case-v1/exports/visualizar-case.html) |
| Ver uma imagem da case | [Prévia PNG](mechanical/case-v1/exports/previa-case.png) |
| Obter STLs, STEP e fontes da case | [Pacote da case v1](production/case/v1/ARCSTRIKE-case-v1-CONCEITO.zip) |

A case é um estudo mecânico. O suporte das bobinas tem medidas provisórias;
as fixações térmicas, tolerâncias de impressão e montagem ainda precisam de
conferência. Veja [as medidas e pendências](mechanical/case-v1/README.md).

## Pastas

| Pasta | Conteúdo |
| --- | --- |
| `library/` | Símbolos, footprints e modelos 3D usados pelo projeto ativo |
| `mechanical/` | Fontes paramétricas, referências e peças da case |
| `production/pcb/` | Gerbers, furação, ZIPs e STEP da PCB, separados por revisão |
| `production/case/` | Pacotes de entrega da case |
| `scripts/` | Ferramentas de extração, validação e geração |
| `scripts/models3d/` | Geradores atuais dos modelos ajustados de IGBT, ponte e capacitores |
| `docs/reference/` | Manuais, datasheets e arquivos Eagle de referência |
| `archive/` | Experimentos, auditorias, versões anteriores e backups |
| `output/` | Resultados temporários de ferramentas; ignorados pelo Git |

Os arquivos ativos `oneTesla.kicad_*`, `fp-lib-table` e `sym-lib-table` ficam
na raiz. Essa posição preserva as referências `${KIPRJMOD}/library/...`.
Abra o projeto por `oneTesla.kicad_pro`.

## Documentação

- [Índice da documentação](docs/README.md)
- [Case e impressão 3D](mechanical/case-v1/README.md)
- [Pacotes de entrega](production/README.md)
- [Ferramentas e comandos](scripts/README.md)
- [Histórico técnico anterior](archive/PROJECT_HISTORY.md)
- [Mapa da reorganização de arquivos](docs/organization-map.json)

`.git/` e `.history/` são metadados locais. Os snapshots de auditoria e
pacotes de fabricação registram a condição de suas respectivas datas;
não são automaticamente atualizados quando a PCB ativa muda.
