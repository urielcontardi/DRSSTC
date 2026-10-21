# Ferramentas

Executar os comandos a partir da raiz do repositório.

| Arquivo | Função |
| --- | --- |
| `sexpr.py` | Leitura/escrita auxiliar do formato KiCad |
| `pcb_extract.py` | Extrai componentes e geometria para `output/` |
| `validate_schematic.py` | Confere netlist/ERC previamente exportados |
| `validate_dfm.py` | Verificação suplementar de geometria, com Python do KiCad |
| `pcb_refill.py` | Recalcula as zonas do arquivo PCB indicado |
| `pcb_patch_footprints.py` | Ferramenta da construção original dos footprints |
| `build_schematic.py`, `build_pcb.py` | Geradores da reconstrução original; não reproduzem todas as edições manuais posteriores |
| `models3d/` | Geradores atuais dos modelos ajustados |

Para os modelos 3D:

```sh
uv run --with cadquery python scripts/models3d/capacitor_snapin.py
uv run --with cadquery python scripts/models3d/igbt_bottom.py
uv run --with cadquery python scripts/models3d/bridge_trimmed.py
```

Os scripts escrevem em `library/3dmodels/`. A geração da ponte usa uma referência
local da instalação do KiCad, conforme indicado no código.

Para regenerar a case e suas prévias, ver
[`mechanical/case-v1/README.md`](../mechanical/case-v1/README.md).
Os scripts de intervenções antigas ficam em
[`archive/implementation/`](../archive/implementation/).
