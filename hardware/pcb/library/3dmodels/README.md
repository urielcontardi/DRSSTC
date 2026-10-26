# 3D models

Component STEP models are stored here. Use project-relative paths in KiCad:

```text
${KIPRJMOD}/library/3dmodels/2EDGRC-5.08-02P.stp
```

`Catalog_*.step` files are catalog models; `Visual_*.step` files are generated or
adapted approximations. Read the source and license notices in this directory.
Models do not identify a BOM manufacturer or part number unless explicitly stated.
T1/T3 and the J110 wire link have no model.

## Active assembly

R1–R6 and IC1/IC2 use the models of their SMD footprints. IC6/L7805CV uses
`TO-220-3_Vertical.step`: pins 1 IN, 2 GND, 3 OUT.
`Visual_Bourns_PWR8030.step` is a nominal 20.8 × 7.6 × 7.8 mm visual envelope.
The 1206/2512 resistors and SOP-14 use local copies of standard KiCad models.

## AC input — J1

The selected connector is a 2EDGRC-5.08-02P, right-angle, two-pin male pluggable
terminal block. J1 carries L/N; external PE connects directly to J2/CHASSIS.
The supplied model identifies 5.08 mm pitch, although the commercial name was
reported as 2EDGRC-5.0. Confirm the purchased part's actual pitch.

The STEP is preserved without scaling. Pin 1 is L and pin 2 is N. The footprint
origin is pad 1, with pad 2 at (5.08, 0) mm. STEP terminals lie at x = ±2.54 mm;
the 3D link uses a (2.54, 0, 0) mm offset, unit scale, and zero rotation.
The connector opening faces the upper PCB edge.

The STEP envelope is 11.4 × 12.1 × 8.2 mm with 1 mm square terminals.
The selected 1.6 mm drills and 3.2 mm pads require physical verification.
The STEP does not establish the complete suffix or electrical ratings.
[Family reference](https://www.degson.com/content/details_552_882388.html?lang=en).
A three-pin version requires a different footprint and STEP.

## Fuse holder — F1

The Idall AS-06 5×20 mm reference drawing specifies 20.2 ±0.3 mm pitch and a
26 × 9.6 mm body. See the [Idall drawing](../../../../docs/reference/idall-0179-drawing.jpg).
The active slotted adaptation uses 22.35 mm pad centers and 4.4 × 1.8 mm plated
slots to accommodate a wider lead-spacing range; this is a layout adaptation,
not a confirmed manufacturer dimension. Verify actual fit.

`Fuse Holder.stp` is preserved as supplied. Its KiCad link uses unit scale,
(-90, 0, 0)° rotation and (-7.167784602, 22.768333249, -8.10222232) mm offset.
STEP units are meters, converted automatically by KiCad.
The model has 22.5 mm terminal pitch and is only a visual reference;
do not use it to determine drilling.

## C11/C12 — visual envelope

`Visual_CP_D25_H45_P10.16.step` is a generic 25 × 45 mm envelope based on the
user-supplied image, with provisional 10.16 mm lead pitch. It does not confirm
actual lead spacing or snap-in terminal geometry. Check the active PCB's
individual model links and the purchased parts before approving the assembly.
