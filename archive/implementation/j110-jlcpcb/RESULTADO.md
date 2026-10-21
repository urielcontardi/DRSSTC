# J110 e regras de fabricação — 2026-10-13

Aplicado ao projeto ativo, preservando as edições existentes do usuário.

## Jumper de 110 V

- Novo footprint local `oneTesla:J110_WireLink_P15.24mm`, atualizado no PCB, esquema e símbolo local.
- Passo ampliado de 10,16 para 15,24 mm; pads Ø4 mm e furos Ø2,2 mm preservados. Distância livre entre pads: 11,24 mm.
- Pad 1 /AC_N permanece em (104,5;30,22) mm. Pad 2 /DC_MID passa de (104,5;40,38) para (104,5;45,46) mm. Centro do footprint: (104,5;37,84) mm, rotação −90°.
- Endpoint da trilha /DC_MID ajustado para acompanhar o pad 2. Mesmas redes, quantidade de trilhas e componentes. O footprint antigo foi preservado para compatibilidade com arquivos históricos.

## Regras aplicadas

Base de fabricação: FR4, duas camadas, cobre de 1 oz, contorno fresado, placa de 1,6 mm. Para outra espessura de cobre, revisar as regras e a capacidade de corrente.

| Parâmetro | Valor configurado |
| --- | --- |
| Largura mínima de trilha / clearance geral | 0,20 / 0,20 mm |
| Distância cobre–borda | 0,50 mm |
| Cobre–furo | 0,35 mm |
| Distância entre bordas dos furos | 0,45 mm |
| Via mínima / furo mínimo | 0,60 / 0,30 mm |
| Anel mínimo da via / pad PTH | 0,15 / 0,25 mm |
| Serigrafia–pad | 0,15 mm |
| Altura / espessura mínima de texto | 1,00 / 0,15 mm |
| Máscara–cobre vizinho | 0,09 mm |
| Expansão da máscara | 0 mm, abertura 1:1 existente |

Defaults de desenho e listas de larguras/vias também configurados. Regras se aplicam ao DRC e a edições futuras; não corrigem automaticamente toda a geometria existente. Anel PTH em regra personalizada; demais limites gerais no `.kicad_pro`.

Fonte consultada em 2026-10-13: [capacidades oficiais da JLCPCB](https://jlcpcb.com/capabilities/pcb-capabilities). Os valores adotados são escolhas de projeto, em geral com margem sobre os limites de fabricação. Não constituem validação elétrica.

## Metas preliminares de espaçamento elétrico

Classe `Rede_Barramento`: /AC_L, /AC_L_FUSED, /AC_N, /DC_PLUS, /DC_MID, /DC_MINUS, /SW_NODE e Net-(CPR1-Pad2), com clearance de 3 mm. Classe `Gates_Potencia`: /GATE_H e /GATE_L, com clearance de 0,5 mm. Entre classes prevalece o maior clearance.

Regra explícita no `oneTesla.kicad_dru`: 6,4 mm de clearance e creepage entre essas redes de potência (incluindo gates) e todas as demais redes nomeadas de controle. Os três domínios GND, DC_MINUS e chassis continuam separados. Nenhuma exclusão de DRC foi adicionada.

Esses valores são metas preliminares para revisão do layout, não exigências da JLCPCB nem declaração de conformidade. A tensão pulsada do circuito ressonante, sobretensões, altitude, poluição, CTI do laminado e norma aplicável precisam definir os valores finais. Referência: [TI — creepage e clearance](https://www.ti.com/video/6146024211001). A largura sugerida de trilha da classe de potência (1 mm) é apenas um preset; não dimensiona o caminho de corrente do primário.

## Verificação e impedimentos de produção

DRC nativo KiCad 10 executado antes e depois, incluindo leitura válida das regras personalizadas. Geometria do jumper, redes e contagens de componentes/trilhas conferidas.

- Antes: 29 violações e 81 conexões sem roteamento.
- Depois: 76 violações e 81 conexões sem roteamento. O aumento expõe conflitos pelas regras mais exigentes.
- Relatórios completos: `drc-before.json` e `drc-after.json` nesta pasta. Backups do PCB/projeto guardam o estado anterior à alteração.
- Há espaçamentos inferiores à meta de 3 mm em J1, D4, Q1/Q2, T1, Z1/Z2 e trilhas da entrada AC. Não foram criadas exceções para ocultá-los.
- FB1 possui quatro anéis PTH de 0,20 mm, abaixo da recomendação adotada de 0,25 mm.
- Persistem sobreposições mecânicas (PS1/furo, Q1/Q2/TVS, CPR1/P1/furo); o envelope retangular ampliado de J110 também aponta sobreposição com C12 e deve ser conferido na montagem.
- Persistem problemas de máscara e serigrafia, além dos footprints provisórios já documentados no README.

**Ainda não liberar para fabricação.** É necessário concluir o roteamento, resolver os conflitos mecânicos e elétricos e confirmar as peças provisórias antes de exportar os arquivos finais de produção.

Para repetir: `/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli pcb drc oneTesla.kicad_pcb -o implementation/j110-jlcpcb/drc-after.json --format json`.
