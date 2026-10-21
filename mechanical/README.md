# Mecânica

[`case-v1/`](case-v1/) reúne todo o trabalho da primeira proposta:

- `reference/`: cópias dos STLs do dissipador/C14 e STEP da PCB usados no estudo.
- `exports/`: conjunto STEP, peças STEP/STL, prévias e relatório de colisões.
- `parameters.json`: dimensões parametrizadas e placeholders das bobinas.
- `build.py`: geração CAD com CadQuery.
- `build_viewer.py`, `viewer.js`, `viewer.template.html`, `render_preview.cjs`:
  geração da visualização offline sem WebGL e das imagens PNG.
- `README.md`: medidas, instruções e pendências de montagem/impressão.

Para abrir o conjunto no Fusion 360, usar
[`ARCSTRIKE-case-v1-CONCEPT.step`](case-v1/exports/ARCSTRIKE-case-v1-CONCEPT.step).
Os STLs separados são destinados ao fatiador.

O pacote para compartilhar está em
[`production/case/v1/`](../production/case/v1/).
