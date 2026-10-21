# C9 cerâmico em 1210

Substituído C9 de100µF/35V eletrolítico por **10µF/100V MLCC X7R, tolerância10%, SMD1210**. Footprint local padrão KiCad `oneTesla:C_1210_3225Metric`, corpo nominal3,2×2,5mm, com modelo STEP genérico local. Não foi fixado um MPN; a especificação corresponde à opção X7R1210 apresentada pelo usuário.

Esquemático atualizado para `oneTesla:C` não polarizado, com mesmos números, posições e UUIDs dos pinos. Na PCB, pad1 continua+5V e pad2GND; UUIDs dos pads preservados. Símbolo anterior e novo têm pinos nas mesmas coordenadas, sem mudar fios ou conectividade.

Posição atual de C9(39,15;95,3)mm, rotação180°, referência e ocultação do valor preservadas. Demais componentes, lados da placa, posições, contorno100×100mm e furos não foram alterados. Não foram adicionadas trilhas ou vias.

Conferidos34 redes e130 conexões idênticas antes/depois; nenhum novo diagnóstico DRC. A posição atual foi preservada: ao concluir o layout, colocar C9 próximo de OUT/GND de IC6 e conferir a resposta da linha5V sob a carga real. A troca não constitui validação elétrica em bancada.

Backup, relatórios, netlists e `verification.json` nesta pasta. Avisos de licença do STEP copiado em `KiCad-model-NOTICES.txt`.
