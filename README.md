# ARCSTRIKE / DRSSTC

KiCad electronics, resonator calculations, and a concept enclosure for a dual-resonant solid-state Tesla coil.

## Quick access

| Task | File |
| --- | --- |
| Edit the schematic and PCB in KiCad | [oneTesla.kicad_pro](hardware/pcb/oneTesla.kicad_pro) |
| Read the project notebook | [Project notebook](docs/project/PROJECT-DRSSTC.html) |
| Review the coil calculations | [Coil design](docs/design/COILS.md) |
| Import the assembled PCB into CAD | [Complete PCB — STEP](production/pcb/2026-10-20-3d/ARCSTRIKE-PCB-complete.step) |
| Download enclosure STEP, STLs, viewer, and source files | [Enclosure v1 package](production/case/v1/ARCSTRIKE-case-v1-CONCEPT.zip) |
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

The enclosure ZIP includes its source files and viewer. There is no separate
`mechanical/` working directory. The enclosure is a concept with unverified
mounting dimensions and tolerances; consult the README inside the package.

## Indexes

- [Documentation](docs/README.md)
- [Deliverables](production/README.md)
- [Tools and commands](scripts/README.md)
- [Electronics project](hardware/pcb/README.md)

Deliverables represent the revisions named in their directories. They are not
updated automatically when the active PCB changes.
