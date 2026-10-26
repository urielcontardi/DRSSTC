# ARCSTRIKE — DFM reassessment package

Generated from the revised PCB on October 18, 2026 using KiCad 10.0.7.
Two layers, 100 × 100 mm, 1.6 mm board thickness, 35 µm copper.
The ZIP contains Gerbers, the job file, and PTH/NPTH drill files with routed slots.

Changes include 21 vias with 0.70/0.30 mm diameter/drill, JCT1/CPR1 separation,
nominal 0.15 mm minimum silkscreen strokes with pad/hole clearance, and tighter rules.

Recorded DRC: zero copper/silkscreen violations and zero unconnected items.
There are 20 mechanical findings and 21 parity warnings. Supplemental geometry
checks found zero issues; exported copper and drilling for all 21 vias were checked.

Outstanding mechanical findings: 11 courtyard overlaps, 7 PTH holes and 2 NPTH
holes inside courtyards. Parity warnings: 16 field differences, 3 extra footprints,
and 2 duplicate `REF**` mounting-hole references.

This package requires JLCDFM reassessment; no new portal result is available.
It is not general manufacturing approval. It represents the October 18 revision
and is not automatically updated when the active PCB changes.
