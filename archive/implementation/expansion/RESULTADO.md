# Ampliação autorizada — revisão geométrica implementada

Base: 028ef6e. Branch: fix/cad-review-20261007. Sem push. Esta entrega substitui os bloqueios de tamanho da placa, colisão C11/C12 e passo impossível de R1 do relatório anterior, mas NÃO aprova fabricação ou energização.

## Mudanças

- Placa: **106,045 × 106,045 → 145 × 108,045 mm**. Coordenadas do contorno: x=0…145; y=-2…106,045. Crescimento de38,955 mm à direita e2 mm para cima; origem dos componentes preservada.
- **Todos os furos de montagem/chassis preservados**, incluindo NPTHs dos conectores, furos dos IGBTs e J2. Sem novos furos de suporte. O balanço mecânico da nova região à direita precisa ser conferido; não inventamos suporte ou enclosure.
- C12: (66,675;31,75) → **(125;25)**. C11: (92,71;31,75) → **(125;60)**. Diâmetro30, passo10,16 e polaridade preservados. Distância entre centros35 mm: **5 mm livres entre os corpos**, e5 mm do corpo à borda direita. MPN, altura, tolerâncias, ripple e vida útil continuam pendentes.
- R1: corpo25 ×6,4 mantido; passo22,86 → **30,48 mm**, com2,74 mm nominais de extensão de terminal por lado. Novo modelo **R_L25_P30.48_Provisional**, origem/posição mantidas. Pads ficaram em(11,43;101,6) e(11,43;71,12); ligações refeitas. Courtyard existente cobre ambos os pads. Esta escolha geométrica convencional não verifica dobra de terminal, temperatura ou MPN.
- R5: (79,375;20,32) → **(79,375;27,94)**. R6: (98,425;16,51) → **(98,425;27,94)**. Saíram da região ocupada pela ponte; corpos, pads e nets preservados, derivações DC_MID refeitas.
- Planos DC_PLUS/B.Cu e DC_MINUS/F.Cu ampliados até x142. Ponto médio reroteado: ligação do banco e retorno de C11 até JPRT1 por F.Cu, removendo o antigo corte longitudinal do plano positivo por B.Cu. Largura existente2,54 mm preservada; derivações dos resistores permanecem0,4064 mm. **7 vias antes e depois; nenhuma adicionada.**
- Campo Footprint_Status do esquema/PCB atualizado. Nenhum valor elétrico, componente selecionado, net, fase do GDT ou topologia funcional alterado.

- Serigrafia: hachuras sobre pads de seis eletrolíticos substituídas por sinal negativo explícito; contornos e sinais positivos preservados. Três modelos locais e instâncias sincronizados. Pictograma deslocado30 mm à direita e15 mm abaixo, sem apagar avisos. Ainda restam colisões de serigrafia, inclusive primitivas gráficas.

## Verificação final

KiCad10.0.6: refill salvo, DRC/paridade nativos, ERC, netlist e exportações executados sobre os arquivos editados. Conferidos topo, fundo e montagem após o último reposicionamento de R5/R6.

| Verificação | 028ef6e | Atual |
|---|---:|---:|
| DRC reportado |509|363|
| Paridade |11|11|
| Conexões pendentes |0|0|
| Curtos / clearance / trilhas cruzadas |0|0|
| Erros de furo / alívio térmico |0|0|
| Cobre próximo da borda |1|0|
| Courtyards sobrepostos |39|27|
| PTH dentro de courtyard |25|17|
| ERC |2|2|

A margem geométrica cobre–borda de J2 agora atende à regra existente porque o contorno cresceu; o furo não foi movido. Isso não verifica ligação PE, corrente de falha ou isolação de rede.

As duas ocorrências ERC continuam entradas AC de PS1 sem power_output. Netlist final idêntica à anterior por referência/pino; mapa pad–net idêntico; 48 instâncias preservadas. Nenhuma regra/exclusão foi relaxada. Contagens são ocorrências reportadas, não um índice de segurança.

Provas: **invariants.json**, **drc-final.json**, **erc-final.json**, **final.net**, **cobertura.csv** (48 instâncias), **top/bottom/assembly.svg e .png**, **before-after.png**. Arquivos drc-1/2 registram iterações, não são o estado final. expand_board.py é histórico de migração inicial, não gerador idempotente da versão final; tem guarda contra reaplicação.

## O que ainda falta — sem reutilizar o bloqueio de tamanho já removido

1. **Peças reais:** códigos/datasheets de C11/C12/R1, ponte D4, clipes F1, IEC J1, TO92 IC6, terminais e magnetismos. Acomodar um envelope não confirma o componente comprado. Não foram trocados os capacitores por menores.
2. **Mecânica:** módulo PS1, cabo óptico, dissipador, cabeças de parafusos e suportes do novo espaço à direita. Persistem interferências no conjunto PS1/J1/fixação e na região compacta de baixa tensão. Os27 overlaps não foram ignorados. Sua resolução final exige envelopes/montagem corretos; alguns ainda demandam trabalho de placement, não apenas informação externa.
3. **Potência/isolação:** tensão máxima de rede, corrente RMS/pico, frequência/pulsos, cobre/plating, norma, CTI/poluição/altitude/coating e condições térmicas. A ampliação muda a área e a indutância do loop de potência: não foi demonstrado que o novo trajeto é adequado para comutação. Dimensionar barramento, gate loops, snubber e térmica continua necessário; largura herdada não é corrente nominal certificada.
4. **Limpeza CAD restante:**22 diferenças entre footprints embarcados e biblioteca,7 questões de biblioteca,11 de paridade, serigrafia e outras interferências documentadas. Não alegamos que todas dependem de BOM; são trabalho remanescente da revisão completa. Esta etapa conclui a ampliação e as correções geométricas descritas, não o layout inteiro.

**Resultado: C11/C12 cabem sem colisão entre si e R1 deixou de ter geometria impossível. Layout ainda não liberado para fabricação/energização.**
