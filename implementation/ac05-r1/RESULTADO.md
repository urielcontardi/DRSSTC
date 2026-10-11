# R1 — Vishay AC05 1k/5W

Aplicado no esquema e no PCB com o footprint local `oneTesla:R_Axial_Vishay_AC05_L18.0mm_D7.5mm_P23.40mm_Horizontal` e o modelo `${KIPRJMOD}/library/3dmodels/vishay_AC05.step`.

O footprint anterior era provisório, com corpo 25 × 6,4mm e passo 30,48mm. O [desenho Vishay 28730, página 10](https://www.vishay.com/docs/28730/ac_ac-at_ac-ni.pdf) especifica para AC05 corpo máximo 18 × Ø7,5mm e fio Ø0,8 ±0,03mm. O novo F.Fab representa esse corpo; a serigrafia também envolve as pequenas extensões de cimento presentes no STEP. Pads Ø2,4mm e furos Ø1,2mm são escolhas de layout.

**O passo de montagem escolhido é 23,4mm**, medido entre os eixos dos terminais dobrados do STEP fornecido. É necessário formar os terminais axiais para esse passo. Não é um passo fixo de toda a série AC05: as variantes pré-formadas EK do fabricante usam 22,5 ou 25,4mm. O STEP foi mantido em escala 1, com rotação KiCad X = -90°, sem deslocamento, deixando a base do corpo aproximadamente 3,75mm acima da face superior do PCB.

Valor 1k/5W, redes dos pads, centro, orientação e UUID do componente foram preservados. O modelo foi carregado pelo KiCad e renderizado em [preview-3d.png](preview-3d.png); a placa de prévia é apenas uma amostra mecânica isolada.

Conferência final em [verification.json](verification.json): todas as 41 associações de footprint e os 130 pads numerados do PCB coincidem com o esquema. A pinagem de IC6 é 1 = +15V, 2 = GND, 3 = +5V. O HLK continua com as dimensões e posições dos quatro pads conferidas contra o desenho fornecido. A revisão de R1 não alterou redes; a única diferença de conectividade nesta etapa foi restaurar J1 de dois pinos e remover J1.3 de PE, com entrada PE externa em J2.

ERC final: duas notas esperadas `power_pin_not_driven` nas entradas AC de PS1 e uma `isolated_pin_label` para PE externo em J2. O caminho 3D antigo de FB1 não existe na instalação atual; todos os modelos locais solicitados para J1, F1, R1 e IC6 foram encontrados. DIP16 não foi associado porque IC1/IC2 são DIP14 e IC3/IC4 são DIP8.

Esta conferência verifica componentes e associações. O PCB atual ainda não tem roteamento nem contorno da placa definidos.
