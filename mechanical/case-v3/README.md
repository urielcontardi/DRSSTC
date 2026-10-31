# ARCSTRIKE — case v3 compacta

Revisão da v2 com base da eletrônica menor e plataforma circular para o primário.
Mantém a PCB STEP de produção, dissipador, primário, secundário e toroide da v2.

## Resultado

| Medida | v2 | v3 |
| --- | --- | --- |
| Corpo com pés | 196 × 196 × 97 mm | 130 × 130 × 94 mm |
| Volume do envelope da caixa | 3,73 litros | 1,59 litros |
| Plataforma do primário | quadrada 180 × 180 mm | circular Ø180 mm |
| Largura máxima do conjunto | 196 mm | 180 mm |
| Altura total | 417 mm | 414 mm |

A caixa tem aproximadamente 57% menos volume externo e 56% menos área de base.
Isso descreve o corpo eletrônico: a plataforma circular continua a determinar
uma largura máxima de 180 mm. O primário de Ø176 mm limita a redução dessa largura.

Cantos externos com raio de 8 mm, borda da plataforma suavizada, três rasgos
longos arredondados em cada lateral e acabamento grafite. A plataforma mantém
os quatro pentes, o colar do tubo e quatro fixações M4 sobre quadrado de 80 mm.
O primário fica saliente em relação ao corpo, apoiado pela plataforma de 4 mm;
a rigidez desse balanço precisa ser conferida com o material e a carga reais.

O teto desceu 3 mm. O componente mais alto da PCB termina em Z=42,095 mm;
a tampa começa em Z=46 mm, com folga geométrica nominal de 3,905 mm.
A PCB usa três furos existentes e deixa o ponto PE disponível.
Os acessos C14 e fibra foram preservados; a janela de fibra fica mais próxima
do receptor que na v2, mas o cabo/plugue físico ainda precisa ser conferido.

Secundário: tubo Ø60 × 280 mm, parede assumida de 1,5 mm, enrolamento representado
por envelope de 213,36 mm para 1.500 espiras. Toroide Ø150 × 40 mm com disco central.
Primário: oito revoluções contínuas, Ø90 mm livre inicial, tubo de cobre recozido nu Ø3 mm, parede 0,5 mm, e passo
radial de 5 mm, chegando a Ø176 mm. O enrolamento inicia 18 mm acima do primário.
O Ø166 mm dos cálculos preliminares aproxima oito voltas por anéis; a geometria
contínua final requer recálculo/medição da indutância e ajuste do tap.

## Arquivos

- `ARCSTRIKE-assembly.sc`: montagem para abrir no SolidCraft, com corpos importados do STEP.
- `assembly-solidcraft.png`: vista completa, renderizada no SolidCraft.
- `interior-solidcraft.png`: corte para revisão da eletrônica.
- `lid-parametric.sc`: tampa com histórico nativo editável e 12 features.
- `solidcraft-lid.json`: script para reconstruir a tampa no SolidCraft.
- `exports/ARCSTRIKE-case-v3-CONCEPT.step`: montagem CAD completa.
- `exports/01...07*.stl`: sete conjuntos de peças impressas, incluindo quatro pés separados.
- `exports/case-viewer.html`: visualizador offline com rotação, seleção e vista explodida.
- `exports/verification.json`: verificações de interseção e comparação de dimensões.
- `solidcraft-verification.json`: volume analítico e medido da tampa, com saúde da timeline.

O restante da fonte paramétrica é `build.py` + `parameters.json`, usando CadQuery.
O arquivo `.sc` da montagem é uma importação; os parâmetros do gerador não viram
features nativas do SolidCraft. A tampa tem seu próprio histórico nativo.

## Validação e pendências

O gerador verifica sólidos válidos e interseções de peças impressas com PCB,
dissipador, C14, tubo, primário e toroide, além dos pares de peças impressas.
Interseções superiores a 0,02 mm³ reprovam o build. O teste geométrico não
valida ferramentas de montagem, aquecimento, esforços ou isolação elétrica.

Conceito para revisão e protótipo de encaixe. Medir tubo, esmalte e toroide;
selecionar parafusos/inserts, trava do secundário, retenção do dissipador,
isoladores dos IGBTs e fixação/conexão do toroide. A tampa superior tem plugue e
flange, mas não tem trava dimensionada. C14 no STEP usa envelope reconstruído
do STL fornecido. Chicotes e ferragens não estão modelados. Conferir tolerâncias,
material de impressão, temperatura e isolação antes de fabricar para operação.

## Regenerar na raiz do repositório

```sh
uv run --with cadquery python mechanical/case-v3/build.py
/Applications/SolidCraft.app/Contents/MacOS/solidcraft-cli run mechanical/case-v3/solidcraft-lid.json --save mechanical/case-v3/lid-parametric.sc --out mechanical/case-v3/lid-solidcraft.step
/Applications/SolidCraft.app/Contents/MacOS/solidcraft-cli bench-open mechanical/case-v3/exports/ARCSTRIKE-case-v3-CONCEPT.step --save mechanical/case-v3/ARCSTRIKE-assembly.sc
```

## Condutor definido para o holder

Tubo de cobre recozido nu Ø3 × 0,5 mm (Øinterno 2 mm); peça contínua de 4 m.
Canais Ø3,6 mm com 0,3 mm de folga radial nominal, passo radial de 5 mm.
A espiral CAD representa o envelope externo do tubo, sem modelar o furo interno.
A geometria externa é a mesma do export anterior. Ver [justificativa](PRIMARY-CONDUCTOR.md).
O cupom `exports/08_primary_fit_coupon.stl` permite conferir encaixe antes de imprimir a plataforma.
