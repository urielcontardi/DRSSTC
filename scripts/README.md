# Tools

Run commands from the repository root.

| File | Purpose |
| --- | --- |
| `sexpr.py` | KiCad S-expression parsing and serialization helpers |
| `pcb_extract.py` | Extract components and geometry into `output/` |
| `validate_schematic.py` | Check previously exported netlist and ERC data |
| `validate_dfm.py` | Supplemental geometry checks using KiCad Python |
| `pcb_refill.py` | Refill copper zones in the specified PCB |
| `calculate_resonator.py` | Calculate coils from inputs in `docs/design/` |
| `build_project_document.py` | Build the HTML notebook and its delivery package |
| `models3d/` | Generate adjusted component models |

Generate 3D models:

```sh
uv run --with cadquery python scripts/models3d/capacitor_snapin.py
uv run --with cadquery python scripts/models3d/igbt_bottom.py
uv run --with cadquery python scripts/models3d/bridge_trimmed.py
```

Models are written to `hardware/pcb/library/3dmodels/`. The bridge generator
uses a local KiCad installation reference, as specified in the source.
Enclosure source files and instructions are in the
[enclosure v1 package](../production/case/v1/ARCSTRIKE-case-v1-CONCEPT.zip).

The active project is `hardware/pcb/oneTesla.kicad_pro`. Create `output/`
before exporting temporary data:

```sh
mkdir -p output
kicad-cli sch export netlist hardware/pcb/oneTesla.kicad_sch -o output/oneTesla.net
kicad-cli sch erc hardware/pcb/oneTesla.kicad_sch --format json -o output/erc.json
python3 -B scripts/validate_schematic.py
```

Rebuild the calculations and notebook:

```sh
python3 -B scripts/calculate_resonator.py
python3 -B scripts/build_project_document.py
```

The notebook builder requires Python and Node.js. It reuses the PCB mesh from
the enclosure package and checks its source STEP hash before rendering.
