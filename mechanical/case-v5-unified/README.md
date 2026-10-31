# Tampa e plataforma unificadas — reposição compatível com a case v5

**Imprimir somente `04_tampa_e_plataforma_unificadas__1x.stl`.**
Ela substitui as antigas `04_tampa__1x.stl` e `05_plataforma__1x.stl`.
Todas as outras peças da case v5 podem ser aproveitadas como já foram impressas.
O suporte do fio primário continua pendente.

## Compatibilidade

- Mesmo envelope externo das duas peças montadas: 180 × 180 mm, espessura máxima de 10 mm.
- Mesma guia inferior de encaixe nas laterais da caixa.
- Mesmos quatro parafusos M3×10 para fixação na caixa, com cabeças e acessos nas posições anteriores.
- Mesmo apoio do tubo em Z=52 mm, mesma abertura Ø60,6 mm e mesma posição da abraçadeira impressa.
- Mesmos furos da abraçadeira e da interface reservada ao futuro holder do primário.
- Mesmas passagens dos fios e mesma altura final do conjunto.

As únicas mudanças internas são a remoção dos furos da antiga união M4 e o
reposicionamento das quatro porcas M3 da abraçadeira para o lado inferior.
A fonte reconstrói a v5 sem modificar ou reexportar suas outras peças. O relatório
registra os hashes dos STLs restantes e verifica diferenças fora dessas regiões.

## Ferragens

- Manter os quatro M3×10 e respectivas porcas que fixam a tampa nas laterais.
- Para a abraçadeira inferior do secundário: usar **quatro M3×16** no lugar dos antigos M3×8, reaproveitando as mesmas quatro porcas M3.
- Os quatro M4×10 e quatro porcas M4 que uniam tampa e plataforma deixam de ser necessários.
- O parafuso M4 do toroide e todas as outras ferragens permanecem como antes.

Os alojamentos M3 agora ficam por baixo, com 2,6 mm de profundidade. São acessíveis
antes de fechar a caixa, sem exigir cola nem novos componentes impressos.

## Montagem

1. Colocar as quatro porcas M3 nos alojamentos inferiores correspondentes à abraçadeira. Uma fita temporária sobre as aberturas pode segurá-las durante a montagem.
2. Posicionar a abraçadeira já impressa na face superior e apertar os quatro M3×16. Retirar a fita temporária.
3. Encaixar a peça unificada nas laterais já impressas e prender com os mesmos quatro M3×10 da tampa. Os acessos para a chave Allen foram preservados.
4. Montar o tubo e o restante do conjunto como no guia da v5.

Os M3×16 terminam em Z=44 mm: permanecem acima do envelope máximo da PCB
(Z=42,095 mm). Não usar parafusos mais longos sem nova conferência.

## Impressão

O STL já está em milímetros, com a face circular maior voltada para o leito,
coordenadas positivas e Z=0. Nessa orientação, usar suportes locais sob os
quatro cantos da parte quadrada, que avançam um pouco além do disco circular.
Não preencher os alojamentos abertos das porcas com suportes desnecessários.
Manter o material e a compensação dimensional usados nas peças já impressas.

O CAD verifica sólido único e interferências com a montagem v5. A malha STL
é verificada quanto a fechamento, orientação das faces e componente conectado
único. A compatibilidade física ainda depende das tolerâncias da impressão.

## Arquivos

- `exports/04_tampa_e_plataforma_unificadas__1x.stl`: única peça nova para imprimir.
- `exports/04_tampa_e_plataforma_unificadas.step`: componente CAD unificado.
- `exports/ARCSTRIKE-v5-tampa-unificada.step`: montagem completa com a substituição e ferragens corrigidas.
- `ARCSTRIKE-tampa-unificada.sc`: montagem completa para abrir no SolidCraft.
- `exports/verification.json`: compatibilidade e interferências.
- `exports/stl-verification.json`: validação da malha.

```sh
uv run --with cadquery python mechanical/case-v5-unified/build.py
python3 mechanical/case-v5-unified/verify_stls.py
```
