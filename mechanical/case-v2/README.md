# ARCSTRIKE — case v2, conceito integrado

Case dimensionada sobre a PCB STEP real de 100 × 100 mm, dissipador de
100 × 100 × 30 mm e geometria proposta em `docs/design/COILS.md`.

Abra `ARCSTRIKE-assembly.sc` no SolidCraft ou `exports/case-viewer.html`
no navegador. A montagem `.sc` importa os corpos do STEP; seu histórico é de
importação. A tampa `lid-parametric.sc` tem histórico nativo editável com 11
features, gerado pelo script `solidcraft-lid.json`. A fonte paramétrica do
restante da montagem é `build.py` com `parameters.json` (CadQuery).

## Dimensões e peças

- Corpo: 196 × 196 × 93 mm; 97 mm com os pés. O adaptador C14 se projeta além do corpo.
- Altura total: 417 mm, dos pés ao topo do toroide.
- Secundário: tubo Ø60 × 280 mm, parede assumida de 1,5 mm.
- Enrolamento: envelope de 1.500 espiras, 213,36 mm de altura, início a 30 mm da base do tubo. Não são 1.500 fios modelados individualmente.
- Toroide: Ø150 mm, seção circular Ø40 mm, com disco metálico central de apoio representado como referência.
- Primário: espiral contínua de oito voltas, Ø90 mm livre inicial, condutor Ø3 mm e passo radial de 5 mm. Diâmetro externo máximo de 176 mm.
- Plataforma removível de 180 × 180 mm com quatro pentes de apoio e colar fendido Ø60,6 mm.
- Bandeja inferior ventilada, laterais removíveis, placa C14, tampa, plataforma, pés e tampa superior do tubo em STLs separados.

O Ø166 mm do cálculo anterior descreve oito anéis com sete intervalos radiais.
Uma espiral contínua de oito revoluções soma oito avanços de 5 mm e chega a
Ø176 mm. As indutâncias anteriores não são validação da espiral CAD; a geometria
final precisa de recálculo/medição e ajuste do tap.

O plano do primário fica em Z=65 mm. O enrolamento começa em Z=83 mm,
18 mm acima dele, dentro da faixa de posicionamento estudada. O tubo assenta
na tampa em Z=53 mm. Não há ajuste axial por mecanismo nesta revisão.

A PCB usa três furos existentes; o ponto PE fica livre. A janela óptica está
recuada em relação ao receptor e precisa ser verificada com o cabo real.
O C14 usa o envelope reconstruído do STL original, não CAD do fabricante.
Os caminhos de cabos são passagens geométricas; chicotes não foram modelados.

## Verificação e limites

`exports/verification.json` registra interseções entre peças impressas, PCB,
dissipador, C14, tubo, primário e toroide, além dos pares de peças impressas.
O limite de aceitação geométrico é 0,02 mm³. `solidcraft-verification.json`
registra o volume analítico da tampa, a medição independente do SolidCraft e
as features sem erros/avisos.

Conceito para revisão e protótipo de encaixe. Conferir o diâmetro externo e
interno do tubo comprado, esmalte do fio, toroide e tolerâncias de impressão.
Selecionar fixação do colar, parafusos/inserts, retenção do dissipador,
isoladores dos IGBTs e fixação do toroide; não estão detalhados nesta revisão.
A tampa superior tem flange e plugue sem interferência nominal no tubo, mas
não possui trava/parafuso de retenção dimensionado.

Não há validação térmica, estrutural ou de isolação elétrica. As aberturas de
ventilação e ausência de colisão não estabelecem segurança de operação.
O disco do toroide é condutor; conexão ao terminal do secundário e ferragens
permanecem por projetar. O secundário e o primário ficam expostos, como na
configuração vertical prevista no projeto.

## Regenerar

Na raiz do repositório:

```sh
uv run --with cadquery python mechanical/case-v2/build.py
/Applications/SolidCraft.app/Contents/MacOS/solidcraft-cli run mechanical/case-v2/solidcraft-lid.json --save mechanical/case-v2/lid-parametric.sc --out mechanical/case-v2/lid-solidcraft.step
/Applications/SolidCraft.app/Contents/MacOS/solidcraft-cli bench-open mechanical/case-v2/exports/ARCSTRIKE-case-v2-CONCEPT.step --save mechanical/case-v2/ARCSTRIKE-assembly.sc
```

SolidCraft instalado: 0.27.1. Documentação consultada em 30/10/2026:
[scripts](https://github.com/tangency-labs/solidcraft/blob/main/docs/scripts.md),
[MCP](https://github.com/tangency-labs/solidcraft/blob/main/docs/mcp.md) e
[guia de modelagem](https://github.com/tangency-labs/solidcraft/blob/main/skills/solidcraft-modeling/SKILL.md).
