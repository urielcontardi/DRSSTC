# Contorno de 100 × 100 mm

Aplicado no arquivo principal `oneTesla.kicad_pcb`: retângulo fechado na camada Edge.Cuts, de (31,375;27,05) a (131,375;127,05)mm. A largura permanece100mm e a altura passa de150 para100mm. Canto superior esquerdo, UUID e bloqueio do contorno preservados.

A comparação estrutural confirma que somente o contorno mudou. Todos os footprints, posições, rotações, pads, redes, trilhas, zonas e quatro furos de fixação foram preservados. O esquemático também permanece idêntico.

**O layout ainda precisa ser reorganizado para caber no novo contorno.** FB1, T3, D1/D2, P1, R1, CPR1, parte da área mecânica de IC4 e os dois furos inferiores ultrapassam a nova borda inferior. O pequeno excesso da caixa de J1 na borda superior já existia e inclui a espessura do traço; FB1 também tem projeção lateral de conector.

O KiCad confirmou dimensões nominais de100×100mm e renderizou o contorno fechado. A caixa que inclui a espessura do traço de0,05mm mede100,05×100,05mm; isso não altera a dimensão nominal do contorno. O DRC atual registra28 ocorrências e93 conexões pendentes; a placa não está pronta para fabricação com os componentes fora da nova área.

Backup, conferência geométrica, relatório DRC e prévia estão nesta pasta. Foi oferecida ao usuário a opção de reorganizar componentes e furos; sem resposta durante esta execução, foi aplicada somente a alteração explicitamente pedida no contorno.
