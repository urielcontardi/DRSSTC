# Primary and secondary coils — preliminary design

Proposed metric design: 60 mm secondary tube, 1,500 turns of AWG 36 enameled
copper (0.127 mm bare diameter), 150 × 40 mm toroid, and an eight-turn flat
primary with an adjustable tap initially around 6–6.5 turns. This is a calculated
adaptation, with dimensions and operating limits still requiring verification.

The purchased tube is 1,000 mm long. A 280 mm section is proposed, assuming
60 mm actual outside diameter. Confirm the tube, finished wire diameter, and
mounting before cutting. With 0.14224 mm winding pitch, the winding is 213.36 mm
high, leaving 30 mm below and 36.64 mm above it.

The assumed finished wire diameter comes from Remington AWG 36 single-build
36SNS (0.0056 inches overall), rather than a measurement of the purchased wire.
At 0.1524 mm overall diameter, 1,500 turns would occupy 228.60 mm and require
new tuning calculations.
[Wire reference](https://www.remingtonindustries.com/content/Polyurethane%20Magnet%20Wire%20Data%20Sheet.pdf).

## Confirmed references

- Active schematic: `hardware/pcb/oneTesla.kicad_sch`. CPR1 is 68 nF / 3 kV,
  CDE 940C30S68K-F; the external primary connects between P1/P2. Bus electrolytics
  are separate from the resonant capacitor used in these calculations.
- The local oneTeslaTS manual, PDF page 30, gives approximately 750 Ω for the
  original secondary. It shows a PCB spiral primary without all dimensions
  required to reproduce it as a wire spiral.
- The manufacturer describes the TS secondary as 2.5 inches in diameter,
  6.75 inches long, wound with 38.5 AWG wire. This establishes a reference scale,
  rather than a complete dimensioned drawing.
- The generic tutorial's six-turn AWG 14 primary and ten-inch secondary describe
  another model; those dimensions are not applied to this PCB.

## Geometry and assumptions

| Item | Value | Status |
| --- | --- | --- |
| Secondary tube | 60 mm actual OD; proposed length 280 mm | Verify on purchased tube |
| Secondary copper | 0.127 mm bare diameter, one layer | AWG 36 selected; finished diameter unconfirmed |
| Finished diameter and axial pitch | 0.14224 mm | Assumed from reference wire |
| Secondary turns | 1,500 | Proposed |
| Winding height | 213.36 mm | Calculated |
| Toroid | 150 mm OD; 40 mm circular section | Proposed, not a confirmed kit dimension |
| Additional capacitance | 1 pF | Assumed; sensitivity shown below |
| Primary | Single-layer flat spiral | Proposed |
| Primary clear inside diameter | 90 mm | Proposed |
| Primary conductor | 2.5 mm² copper, assumed 3 mm insulated diameter | Geometry only; current/duty unverified |
| Radial center-to-center pitch | 5 mm | Nominal 2 mm insulation-to-insulation gap |
| Physical primary turns | 8 | Adjustable connection |
| Lead inductance | 0.30 µH | Assumed, not measured |
| Initial isolated frequency ratio | fp = 0.90 fs | Adjustable starting point |

Tube trade size is not necessarily its outside diameter. The toroid height,
mounting, and electrical insulation remain to be designed.

## Secondary calculations

The wire centerline diameter is 60 + 0.14224 = **60.14224 mm**.

```text
h = N × pitch = 1500 × 0.14224 = 213.36 mm
r = 60.14224 / 2 = 30.07112 mm

Wheeler single-layer solenoid formula:
Ls[µH] = r² N² / {25.4 (9r + 10h)}    [r,h in mm]
Ls = 33,317.33 µH = 33.317 mH

Copper length ≈ N × π × mean diameter = 283.41 m
Copper area = π × 0.127² / 4 = 0.012668 mm²
Rdc at 20 °C = 0.017241 × length / area = 385.73 Ω
Copper mass = length[m] × area[mm²] × 8.96 = 32.17 g
```

Allow about **315 m of wire**; the calculated length with 10% margin is 311.76 m.
Copper mass excludes the tube, varnish, caps, toroid, and mounting hardware.
The manual's 750 Ω is not a universal tuning criterion for a different wire size.
DC resistance does not determine high-frequency skin and proximity losses.

Self-capacitance, using the empirical approximation reproduced by Skeldon et al.:

```text
Cs[pF] = 11.26h + 16r + 76.4r^(3/2)/sqrt(h)    [h,r in meters]
Cs ≈ 3.746 pF
```

Toroid approximation attributed to Bert Pool and reproduced by Denicolai:

```text
Ct[pF] = 1.4 (1.2781 - d/D) sqrt[πd(D-d)]      [D,d in inches]
Ct ≈ 6.554 pF
Ctotal ≈ 3.746 + 6.554 + 1.000 = 11.300 pF
fs = 1 / (2π sqrt[Ls Ctotal]) ≈ 259.38 kHz
```

This lumped model does not solve mutual electrostatic shielding, support and
PVC dielectric effects, or distributed secondary current. Measure the final
frequency with the toroid installed.

## Primary calculations

Initial target: fp ≈ 0.9 × 259.38 = **233.44 kHz**. This starting offset allows
for the tendency of a loaded secondary's frequency to decrease; its actual
value requires experimental adjustment.

```text
Lp total = 1 / [(2πfp)² Cp]
Cp = 68 nF
Target total Lp ≈ 6.836 µH
Assumed lead inductance = 0.300 µH
Target spiral Lp ≈ 6.536 µH
Z0 = sqrt(Lp total / Cp) ≈ 10.03 Ω
```

Z0 is the tank's characteristic impedance, rather than its loss resistance.
For the proposed flat spiral:

```text
First turn centerline radius = (90 + 3)/2 = 46.5 mm
Mean radius = 46.5 + (N-1) × 5/2
Full radial width = (N-1) × 5 + 3 mm
Lp[µH] = mean_radius² N² / {25.4 (8mean_radius + 11width)}
```

| Approximate active turns | Spiral L (µH) | Total L including assumed leads (µH) | fp with 68 nF (kHz) |
| --- | --- | --- | --- |
| 5 | 4.457 | 4.757 | 279.84 |
| 6 | 6.325 | 6.625 | 237.12 |
| 6.5 | 7.386 | 7.686 | 220.15 |
| 7 | 8.534 | 8.834 | 205.35 |
| 7.5 | 9.770 | 10.070 | 192.33 |
| 8 | 11.097 | 11.397 | 180.78 |

The nominal target is approximately **6.10 turns**. This precision is numerical;
fractional turns interpolate the model rather than exactly locating a physical
clamp. Actual leads, geometry, capacitor tolerance, and measurement determine the tap.

Use eight physical turns with adjustment around 5.5–8 turns, initially about
6.1 turns. The unused end must not form a closed, shorted turn. Its parasitic
effects are not included. The full spiral is approximately 166 mm OD and
3.22 m long; allow about 4 m including leads. The geometric radial gap to the
secondary is about 14.9 mm, without electrical insulation validation.

The primary exceeds a 130–136 mm enclosure footprint. Enlarge its support or
recalculate the spiral geometry before mechanical integration.

## Coupling and sensitivity

A magnetostatic Neumann integral, approximating the primary as coplanar rings
and the secondary as a uniform sheet, gives the following for seven primary turns:

| Secondary winding start above the primary plane | Estimated geometric k |
| --- | --- |
| 0 mm | 0.156 |
| 10 mm | 0.126 |
| 20 mm | 0.101 |
| 30 mm | 0.080 |

This is a positioning estimate, without a complete resonant-current or electric-field
solution. An axial adjustment range of 10–30 mm allows investigation of this region.
The manufacturer's example k≈0.15 is a reference, not a universal requirement.

| Assumed additional capacitance | Estimated fs (kHz) | Target fp = 0.9fs (kHz) |
| --- | --- | --- |
| 0 pF | 271.68 | 244.51 |
| 1 pF | 259.38 | 233.44 |
| 2 pF | 248.61 | 223.75 |
| 3 pF | 239.08 | 215.18 |

This is a one-variable sensitivity sweep, not a statistical confidence interval.
Actual wire pitch changes winding height; the K capacitor tolerance is ±10%.
Leads and surroundings also shift frequency. Coupling produces two normal modes,
so isolated LC frequencies do not fully describe operation.

## Required measurements

1. Confirm the tube, finished wire diameter, and toroid before fixing the supports.
2. Measure secondary resonance with the toroid installed, using low-signal excitation
   and leaving the power bridge unpowered.
3. Measure tank L/C or resonance including the actual leads, then adjust the primary tap.
4. Establish peak current, pulse width, thermal losses, protection, and IGBT switching.
   CPR1's 3 kV DC rating alone does not establish AC voltage or RMS current capability.
   The proposed 2.5 mm² primary conductor has not been thermally validated.

These calculations do not specify admissible power, output voltage, spark length,
interrupter settings, or assembly insulation. They do not authorize direct mains testing.

## Sources and reproduction

- Active schematic: `hardware/pcb/oneTesla.kicad_sch`, CPR1; local manual, PDF page 30.
- [Original TS secondary](https://onetesla.com/products/replacement-parts/ts-replacement-parts/ts-secondary-inductor)
- [Resonator design](https://onetesla.com/tutorials/resonator-design)
- [Tesla coil tuning](https://onetesla.com/tutorials/tesla-coil-tuning)
- [H. A. Wheeler (1928), Simple Inductance Formulas for Radio Coils](https://physlab-wiki.com/_media/phylabs/lab_courses/phys-120_130-wiki-home/winter-experiments/simple_inductance_formulas_for_radio_coils.pdf)
- [Skeldon et al. (2000), Development of a portable Tesla coil apparatus, p. 133](https://hotstreamer.deanostoybox.com/temp/Old2002Files/2002-02/Colapsed%20coil.pdf)
- [Marco Denicolai (2001), Tesla Transformer for Experimentation and Research, section 4.3, p. 26](https://www.eltem.fi/lthesis.pdf)

Proposed dimensions are explicit choices for this preliminary design, not
specifications attributed to these sources.

```sh
python3 -B scripts/calculate_resonator.py
```

Input: `docs/design/resonator-inputs.json`. Outputs: `resonator-results.json`,
`primary-taps.csv`, and `capacitance-sensitivity.csv` in the same directory.
