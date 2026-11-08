# ARCSTRIKE

Projeto de uma **DRSSTC — bobina de Tesla de estado sólido com dupla ressonância**.
Eletrônica em KiCad, cálculos do ressonador e gabinete paramétrico com tampa e
plataforma unificadas.

**Estado:** protótipo de montagem. Encaixes físicos, comportamento térmico e
isolação elétrica ainda precisam de validação. O suporte do fio primário está pendente.

## Comece aqui

| Objetivo | Arquivo |
| --- | --- |
| Editar a eletrônica | [Projeto KiCad](hardware/pcb/oneTesla.kicad_pro) |
| Imprimir o gabinete | [STLs e quantidades](mechanical/print/) |
| Montar o gabinete | [Guia de montagem](mechanical/README.md) · [Ferragens](mechanical/exports/hardware-BOM.csv) |
| Abrir a montagem em CAD | [STEP](mechanical/exports/ASSEMBLY.step) · [SolidCraft](mechanical/ASSEMBLY.sc) |
| Consultar os cálculos | [Projeto das bobinas](docs/design/COILS.md) |
| Explorar a documentação offline | [Caderno HTML](docs/project/PROJECT-DRSSTC.html) |

## Estrutura

```text
hardware/pcb/    Projeto KiCad, bibliotecas e exportações da PCB
mechanical/      Gabinete atual: fontes, impressão, montagem e verificações
docs/            Cálculos, caderno técnico e referências
scripts/         Ferramentas da PCB e da documentação
```

O repositório mantém uma única versão de cada projeto. Revisões anteriores são
consultadas no histórico do Git. Os arquivos exportados ficam junto das fontes:
`hardware/pcb/exports/` e `mechanical/exports/`. Os STLs para impressão ficam
em `mechanical/print/`, com as quantidades nos nomes.

## Reprodução

Execute na raiz do repositório:

```sh
# Recalcular o ressonador (Python 3)
python3 -B scripts/calculate_resonator.py

# Reconstruir o gabinete atual (uv e CadQuery)
uv run --with cadquery python mechanical/build.py

# Verificar todas as malhas de impressão
python3 -B mechanical/verify_stls.py

# Gerar o caderno e seu ZIP offline (Python 3 e Node.js)
python3 -B scripts/build_project_document.py
```

ZIPs gerados e resultados temporários vão para `output/`, fora do Git.
A reconstrução CAD atualiza os arquivos exportados; revise os relatórios e o
diff antes do commit. Os Gerbers existentes documentam a exportação indicada
no [guia da PCB](hardware/pcb/exports/README.md).

## Documentação

- [Eletrônica e bibliotecas KiCad](hardware/pcb/README.md)
- [Montagem e impressão do gabinete](mechanical/README.md)
- [Índice técnico](docs/README.md)
- [Ferramentas e validação](scripts/README.md)
- [Convenções para manutenção](CONTRIBUTING.md)
