# ARCSTRIKE — estudo mecânico da case v1

Conjunto baseado no STEP do Desktop e nos STLs fornecidos pelo usuário.
Esta é uma versão para revisão e protótipo de encaixe. As bobinas e a fixação
térmica ainda precisam de medidas/peças reais antes da impressão definitiva.

## Arquivos

- `exports/visualizar-case.html`: visualizador 3D offline com giro, zoom,
  seleção das peças e vista explodida. Usa Canvas 2D, sem depender de WebGL.
  Abrir no navegador. Se scripts estiverem bloqueados, exibe uma imagem estática.
- `exports/previa-case.png`: prévia da case montada, independente de navegador.
- `exports/ARCSTRIKE-case-v1-CONCEPT.step`: conjunto CAD completo.
- `exports/01_lower_tray.stl`: bandeja inferior ventilada.
- `exports/02_upper_sleeve.stl`: laterais superiores removíveis.
- `exports/03_C14_inlet_plate.stl`: adaptador lateral da tomada fornecida.
- `exports/04_structural_lid.stl`: tampa com interface para suporte das bobinas.
- `exports/05_coil_support_PLACEHOLDER.stl`: suporte provisório, medidas pendentes.
- `exports/06_separate_feet.stl`: quatro pés separados.
- `exports/verification.json`: medidas e verificação de colisões.
- `reference/`: cópias preservadas dos três arquivos fornecidos.

## Medidas e montagem propostas

PCB 100 × 100 mm, centro XY=(50,50). Dissipador 100 × 100 × 30 mm,
base de 5 mm e 18 aletas de 2 mm. Os 19 blocos do STL foram reconstruídos
nas medidas originais e unidos em um sólido válido, sem suavização da forma.
A face plana fica voltada aos IGBTs; aletas para baixo. Desvio entre centros:
zero nos dois eixos.

Case 130 × 130 mm; corpo da base até o topo da tampa: 93 mm. Com pés: 97 mm.
Suporte superior provisório acrescenta 28 mm. O tubo ilustrativo não integra
a medida da case.

Datum: fundo da PCB em Z=0; referência dos componentes exportados pelo
KiCad em Z=1,595 mm. Face metálica dos IGBTs em Z=-5,005 mm. Interface
térmica nominal de 0,3 mm reservada: topo do dissipador Z=-5,305 mm,
fundo Z=-35,305 mm. A espessura real da interface precisa ser confirmada.

Os três furos mecânicos existentes usados são (6,94), (94,94), (94,6),
passo 88 mm. O furo J2/PE em (6,6) fica livre para a ligação de terra;
não é tratado como um quarto ponto de apoio plástico. Há alívio para
terminal e cobre próximos ao apoio de (94,6).

A C14 fica na lateral traseira (Y positivo), alinhada ao lado de J1.
No STL: flange aproximadamente 50 × 22 mm; corpo traseiro 26 × 18 mm;
furos Ø3,2 mm com entrecentros de 42 mm. Recorte proposto 26,6 × 18,6 mm,
folga de 0,3 mm por lado; furos impressos Ø3,4 mm. A placa adaptadora é
removível. Conferir a tomada física e terminais com os conectores do cabo.

O STL da C14 contém uma carcaça com malha inconsistente ao converter para
sólido BRep. O HTML mostra a malha original exata. O STEP usa um envelope
analítico simplificado da carcaça e os seis contatos válidos reconstruídos
da malha; esse envelope não é CAD exato do fabricante.

A janela da fibra é 16 × 14 mm, na lateral esquerda, centrada em Y=28,35 mm.
É uma janela de acesso ao receptor, não um engate óptico impresso. O centro
e a folga devem ser conferidos com o plugue real; o receptor está recuado
da parede. A janela atravessa a junção entre base e lateral.

Tampa com quatro furos M4 em quadrado de 80 mm e duas passagens Ø6 mm
para fios do primário. Suporte provisório: tubo secundário Ø32 mm,
alojamento Ø32,6; forma do primário com diâmetro interno 54 mm e altura
24 mm. São placeholders, não dimensões elétricas selecionadas. Faltam
as medidas reais, retenção do tubo, bitola e número de espiras, distância
entre bobinas e posição/forma do terminal de alta tensão.

## Impressão e pendências

Paredes de 3 mm e tampa de 4 mm. Base e laterais devem ser impressas com
o plano da junção/horizontal na orientação escolhida no fatiador. Os braços
de apoio, trilhos do dissipador e alojamentos superiores podem precisar de
suporte local; conferir no fatiador. Pés separados evitam uma ponte larga
sob o piso. Para o adaptador C14, apoiar a face plana maior na mesa.

Furos piloto Ø2,8 mm nas junções M3 são uma proposta para validar num
cupom impresso. Não há rosca CAD nem alojamento dimensionado de inserto.
Escolher parafusos/inserto e validar a resistência da tampa com a massa
real das bobinas. Não imprimir o suporte provisório como peça final.

A bandeja apoia o dissipador nas extremidades das aletas e tem localização
lateral com 0,4 mm de folga nominal. A retenção vertical e os parafusos de
fixação dos IGBTs ao dissipador ainda não estão dimensionados. Não foram
inventados furos no dissipador fornecido.

Material de impressão, temperaturas, ventilação, isolamento da montagem,
aterramento e distâncias elétricas exigem validação com o conjunto real.
Nenhuma classificação térmica ou de segurança é atribuída à case.
O datasheet do componente do projeto é:
https://www.onsemi.com/download/data-sheet/pdf/fga60n65smd-d.pdf
Conferir também o encapsulamento exato comprado; a referência 3D existente
dos IGBTs tem dobras e alturas provisórias.

## Regenerar

Editar `parameters.json` e executar:

```sh
uv run --with cadquery python mechanical/case-v1/build.py
```

O teste compara sólidos da case com PCB/componentes, dissipador e C14,
e compara as peças impressas entre si. Ausência de colisão geométrica
não valida montagem, acesso de ferramentas, aquecimento ou isolamento.

Para regenerar apenas o HTML, usar `python3 mechanical/case-v1/build_viewer.py`.
Se Node estiver disponível, ele também renderiza a prévia PNG com o mesmo
renderizador do navegador. `node mechanical/case-v1/render_preview.cjs inside`
gera uma prévia adicional do interior.
