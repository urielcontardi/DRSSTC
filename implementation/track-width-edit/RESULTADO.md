# Larguras editadas no PCB — 2026-10-13

Aplicado ao arquivo ativo `oneTesla.kicad_pcb`, após a revisão registrada em `implementation/track-width-review/`.

- **IC3 OUT → R4:** os oito segmentos da rede `Net-(IC3-OUT-Pad6)` foram ampliados de **0,50 para 1,00 mm**, incluindo a ligação entre os pinos 6/7. Largura agora consistente com os demais trechos do acionamento primário do GDT. Comprimento total preservado: 29,26 mm.
- Sinais de 0,25–0,50 mm, +5V de 0,50–1 mm, +15V de 1–2 mm e gates de 2 mm preservados: não precisam de aumento pela revisão realizada.
- Caminhos de potência de 2–3 mm preservados. A largura final depende da corrente RMS, bursts e cobre da encomenda; não há aprovação térmica dessa etapa.

## Verificação

Conferência estrutural confirma exatamente oito alterações de largura. Redes, UUIDs, coordenadas, camadas, vias, footprints e demais segmentos preservados.

DRC KiCad 10 antes/depois: **37 violações e 31 conexões pendentes**, sem novas violações. O DRC escolheu outros segmentos representativos para duas conexões pendentes de /SW_NODE e +5V; as redes e a quantidade de pendências permanecem iguais. Relatórios completos nesta pasta. Backup do PCB imediatamente anterior à edição em `before-oneTesla.kicad_pcb`.

**Pendências existentes:** curto /DC_MINUS ↔ /DC_MID no pad 2 de J110, retornos de GND sem roteamento/plano, demais conexões pendentes e problemas mecânicos/serigrafia. Não liberar para fabricação até resolver as pendências. A revisão anterior documenta os detalhes e as referências técnicas.
