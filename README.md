# ARCSTRIKE / DRSSTC

KiCad electronics, resonator calculations, and a concept enclosure for a dual-resonant solid-state Tesla coil.

## Quick access

| Task | File |
| --- | --- |
| Print the latest enclosure — 14 unique STLs, quantities in filenames | [PARA-IMPRIMIR](PARA-IMPRIMIR/) |
| Edit the schematic and PCB in KiCad | [oneTesla.kicad_pro](hardware/pcb/oneTesla.kicad_pro) |
| Read the project notebook | [Project notebook](docs/project/PROJECT-DRSSTC.html) |
| Review the coil calculations | [Coil design](docs/design/COILS.md) |
| Import the assembled PCB into CAD | [Complete PCB — STEP](production/pcb/2026-10-20-3d/ARCSTRIKE-PCB-complete.step) |
| Review integrated enclosure and coils | [Enclosure v5 source and instructions](mechanical/case-v5/README.md) |
| Open enclosure in SolidCraft | [Assembly v5](mechanical/case-v5/ARCSTRIKE-assembly.sc) |
| Download enclosure STEP, STLs, viewer, and source files | [Enclosure v5 package](production/case/v5/ARCSTRIKE-case-v5-ASSEMBLY.zip) |
| Download the offline notebook and references | [Documentation package](production/documentation/2026-10-22/ARCSTRIKE-documentation.zip) |

## Directory structure

| Directory | Contents |
| --- | --- |
| `hardware/pcb/` | Active KiCad project, schematic, PCB, rules, and local libraries |
| `docs/design/` | Design inputs, calculations, and results |
| `docs/project/` | Offline HTML notebook, template, and assets |
| `docs/reference/` | Manuals, datasheets, and original Eagle reference files |
| `production/` | Deliverables and exports organized by type and revision |
| `scripts/` | Calculation, generation, extraction, and validation tools |
| `output/` | Temporary tool output; ignored by Git |

Open the KiCad project in `hardware/pcb/`. Its libraries stay alongside it,
preserving `${KIPRJMOD}/library/...` references. Run scripts from the repository root.

The current enclosure source is in `mechanical/case-v5/`. The ZIP includes its
source files, SolidCraft assembly, STEP, STLs and offline viewer. This is a
mechanical concept with unverified physical fits, fasteners, thermal and
electrical behavior; consult its README.

## Indexes

- [Documentation](docs/README.md)
- [Deliverables](production/README.md)
- [Tools and commands](scripts/README.md)
- [Electronics project](hardware/pcb/README.md)

Deliverables represent the revisions named in their directories. They are not
updated automatically when the active PCB changes.
