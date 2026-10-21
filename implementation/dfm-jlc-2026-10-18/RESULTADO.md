# Correções DFM — 18/10/2026

Aplicadas ao projeto ativo, preservando como ponto de partida as alterações que já existiam na PCB. Backups `before-*` nesta pasta. Não houve alteração das redes dos pads; comparação automatizada antes/depois passou.

## Regras persistentes

- Via: diâmetro mínimo 0,70 mm; furo mantido em 0,30 mm; anel mínimo 0,20 mm.
- Pad PTH: regra existente de anel mínimo 0,25 mm preservada.
- Distância física pad–pad mínima 0,20 mm, inclusive entre redes iguais, em `oneTesla.kicad_dru`.
- Serigrafia: clearance 0,15 mm, altura de texto 1 mm e espessura 0,15 mm. Defaults atualizados; desenhos existentes ajustados.
- Máscara para cobre vizinho: 0,09 mm. Clearance elétrico geral existente de 0,20 mm preservado.

Esses valores são escolhas de projeto para este pacote de duas camadas/1 oz. Fonte de capacidade consultada: https://jlcpcb.com/capabilities/Capabilities. O clearance geral não dimensiona isolamento elétrico do circuito.

## Localização e correções

1. **Anéis das vias:** 14 vias de 0,50/0,30 mm tinham anel de 0,10 mm. As 21 vias foram padronizadas em 0,70/0,30 mm, incluindo as que tinham 0,60 mm. Localizações e diâmetros anteriores em `changes.json`. Cinco vias tiveram pequenos deslocamentos, acompanhados pelos endpoints de suas trilhas, para manter o clearance de cobre após o aumento; posições finais em `geometry-final.json`.
2. **Pads próximos/sobrepostos:** a nova regra identificou JCT1.2, em (69,545;113,100), sobreposto a CPR1.1, em (69,690;116,400). Ambos pertencem a `/SW_CT`; o DRC elétrico usual não tratava isso como curto. JCT1 foi deslocado 1 mm para cima, mantendo passo, furos e redes. JCT1.2 ficou em (69,545;112,100), com distância nominal entre bordas dos pads de aproximadamente 0,302 mm. Foram ajustados os endpoints de trilha afetados. O afastamento também separa as aberturas de máscara desse par nas duas faces.
3. **Serigrafia:** textos com traço fino e altura insuficiente foram ajustados; referências próximas a pads/furos foram reposicionadas. Os contornos foram recortados onde invadiam pads, furos, textos, contornos vizinhos ou a margem da placa. O recorte considera também os furos das vias, mesmo quando tentados. As mudanças de posição não alteram peças ou redes.
4. **Biblioteca:** 18 variantes locais de serigrafia específicas deste layout foram salvas em `library/oneTesla.pretty`, com sufixo `_DFM_<referência>`, mantendo os pads das respectivas peças. Os campos de footprint no esquema foram sincronizados. Não há divergência de footprint com a biblioteca no DRC final. Os modelos genéricos anteriores foram preservados.

O PDF JLCDFM contém capturas representativas, sem coordenadas ou relação completa das ocorrências. O par JCT1/CPR1 é o conflito físico pad–pad identificado na geometria local; **a associação exata com a medida de 0,03 mm do portal ainda precisa ser confirmada ao reanalisar o novo ZIP**. Não se presume que as contagens do portal correspondam uma a uma ao DRC KiCad.

## Verificação final

- KiCad 10.0.7: DRC com zonas recalculadas, todas as severidades, todos os erros de trilha e paridade.
- **0 violações de cobre, anel, diâmetro de via, espessura/altura de texto, máscara ou serigrafia; 0 conexões pendentes.**
- **20 ocorrências mecânicas restantes:** 11 sobreposições de courtyard, 7 PTH e 2 NPTH dentro de courtyards. Não foram ocultadas ou excluídas.
- **21 avisos de paridade restantes:** 16 divergências de campos, 3 footprints extras e 2 referências duplicadas dos furos `REF**`. O esquema/valores e a montagem ainda exigem revisão própria.
- Verificação suplementar `scripts/validate_dfm.py`: **0 ocorrências**, verificando separação física dos pads, anéis das 21 vias e distância da serigrafia aos pads e furos de componentes/vias. Essa checagem cobre casos que o DRC nativo não representa da mesma maneira.
- Inspeção visual do PDF de serigrafia/máscara/contorno em `preview.pdf`.
- Leitura independente dos Gerbers/Excellon exportados: as 21 vias aparecem com diâmetro de cobre mínimo de 0,70 mm nas duas faces, alinhadas aos 21 furos de 0,30 mm. Evidência em `export-verification.json`.
- ZIP validado e hashes registrados em `production/2026-10-18-dfm/manifest.json`.

Os scripts de correção nesta pasta registram os passos desta intervenção e **não devem ser reexecutados em sequência sobre a placa já corrigida**. O verificador em `scripts/validate_dfm.py` é somente leitura da PCB e pode ser repetido com o Python incluído no KiCad:

```sh
/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/Current/bin/python3 scripts/validate_dfm.py oneTesla.kicad_pcb /tmp/arcstrike-dfm.json
```

## Reanálise necessária no portal

Novo pacote: `production/2026-10-18-dfm/ARCSTRIKE-PCB-prototipo-DFM.zip`.

A categoria THT–SMD do PDF mostra 1,05 mm e contagens de perigo/aviso, mas não informa limiares nem coordenadas. Não foi imposto um afastamento genérico de 1,05 mm a todas as vias/SMDs. A geometria passou pelo clearance de cobre, pela regra física pad–pad e pela auditoria adicional descritos acima. As duas aberturas compostas de máscara e as ocorrências do portal devem ser conferidas na nova análise; não há novo resultado JLCDFM disponível nesta sessão.

O pacote é para reanálise DFM. As pendências mecânicas/de paridade e as validações elétricas da revisão de liberação continuam abertas; este trabalho não constitui aprovação geral de fabricação.
