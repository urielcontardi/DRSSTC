> STATUS: escolha do condutor adiada pelo usuário. Esta nota registra uma alternativa anterior; não é especificação ativa da case v4.

# Primário: condutor escolhido e dimensionamento do holder

Decisão de projeto em 30/10/2026: **tubo de cobre recozido nu, Øexterno 3,0 mm,
parede 0,5 mm, Øinterno 2,0 mm**. Usar uma peça contínua de 4 m, sem emendas na
espiral. É a especificação para fechar o holder da case v3. Substitui a hipótese
anterior de fio isolado de 2,5 mm² com Øexterno estimado de 3 mm.

Esta é uma seleção do condutor e da interface mecânica, não uma certificação
de corrente/potência. O projeto não estabelece corrente medida, duração e
repetição dos pulsos nem temperatura admissível do holder.

## Justificativa

O tanque de 68 nF tem frequência inicial calculada de 233,44 kHz. Para cobre a
20 °C, usando ρ = 1,7241e-8 Ω·m e μ = μ0:

```
δ = sqrt[ρ / (π f μ0)] = 0,1368 mm
parede / δ = 0,5 / 0,1368 = 3,66
área de cobre = π/4 × (3² − 2²) = 3,927 mm²
Rdc por metro = 0,017241 / 3,927 = 4,390 mΩ/m
```

A corrente de alta frequência se concentra perto da superfície. A parede de
0,5 mm supera três profundidades de penetração nesta condição; usar tubo permite
preservar a superfície externa de Ø3 mm sem o peso de uma barra maciça.
Isso não torna o tubo melhor eletricamente que uma barra de cobre de mesmo
Øexterno: ambos têm perdas por efeito pelicular semelhantes neste regime.
Comparado ao cobre maciço equivalente à área antiga de 2,5 mm² (Ø1,784 mm),
a superfície externa de Ø3 mm reduz a estimativa de resistência por efeito
pelicular em aproximadamente 40%, para condutores isolados com igual comprimento.
A rigidez e o diâmetro comercial definido também favorecem o posicionamento e o tap.

A espiral contínua CAD, r = 46,5 + 5 × voltas [mm], com oito revoluções, tem
3,3429 m de comprimento e Øexterno de 176 mm. Quatro metros deixam cerca de
0,66 m para ligações e manuseio. Terminais e conexões devem ser selecionados
para o tubo; não esmagar a parede de 0,5 mm sob um parafuso sem solução de contato.

Estimativa de alta frequência para condutor isolado:

```
Rac / metro ≈ ρ / (π D δ) = 13,37 mΩ/m
Rac na espiral completa ≈ 44,7 mΩ
P ≈ Irms² × Rac
```

Por exemplo, 10 A RMS dariam cerca de 4,47 W e 20 A RMS, 17,9 W **nesse modelo**.
São estimativas de perdas, não correntes liberadas para operação. Não incluem
proximidade entre espiras, conexões, aquecimento, deformação da espiral ou a
forma real das rajadas. Irms aqui deve ser calculada sobre o tempo completo,
incluindo os intervalos desligados. Corrente de pico não substitui RMS.
A área DC de 3,927 mm², isoladamente, também não determina a corrente admissível.

## Holder definido

| Característica | Valor |
| --- | --- |
| Condutor alojado | Tubo nu Ø3,0 mm |
| Diâmetro nominal dos canais semicirculares | 3,6 mm |
| Folga radial nominal | 0,30 mm por lado |
| Profundidade do berço a partir da superfície superior | 1,8 mm |
| Passo radial entre centros | 5,0 mm |
| Vão nominal entre superfícies de cobre | 2,0 mm |
| Nervura nominal entre canais do holder | 1,4 mm |
| Plataforma da case v3 | Ø180 mm |

Os quatro pentes acompanham o avanço angular da espiral. O extremo final do
primário tem um canal adicional no primeiro pente. A folga de 0,3 mm por lado
permite acomodar tolerância, impressão e a pequena variação de raio ao atravessar
a largura de cada pente. O suporte é um berço aberto; não é uma trava por pressão.
Retenção adicional deve ser não condutora e não pode criar uma espira em curto.

O vão de 2 mm entre tubos nus é geométrico; não há ensaio de suportabilidade
elétrica que o qualifique para a tensão real do tanque. A escolha do diâmetro
não resolve essa validação. Preservar ajuste do tap e a extremidade não utilizada
aberta; conferir sintonia após a montagem.

O cupom `08_primary_fit_coupon.stl` contém três berços, da esquerda para a direita,
Ø3,2 / Ø3,4 / Ø3,6 mm, com as mesmas condições de impressão do holder. O canal de
Ø3,6 mm é o adotado. Conferir nele uma amostra do tubo e verificar que se acomoda
sem força e sem esmagamento antes de imprimir o suporte completo. A tolerância
real do tubo comprado e da impressora não é conhecida a partir do CAD.

## Referências

- [West Coast Magnetics — Winding losses / skin depth](https://www.wcmagnetics.com/resource/winding-losses-in-high-frequency-transformers-magnetics2009/): concentração de corrente na superfície, fórmula da profundidade de penetração e efeito de proximidade. Cálculos e escolha do tubo acima são decisões deste projeto.
- [Bengs Modellbau — tubo de cobre mole](https://www.bengs-modellbau.de/en/Copper-tube-soft/5014): exemplo de especificação comercial 3 × 0,5 mm, fornecida em comprimento contínuo. Não é uma exigência de fornecedor ou uma corrente nominal para Tesla coils.
- `resonator-inputs.json`, `resonator-results.json` e esquema ativo: frequência/CPR1 do projeto; a indutância por anéis do cálculo preliminar não é uma simulação da espiral contínua CAD.

Os valores reproduzíveis estão em `primary-conductor-selection.json`.
