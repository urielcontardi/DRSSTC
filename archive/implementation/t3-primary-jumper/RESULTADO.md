# Passagem obrigatória do primário por T3 — 17/10/2026

Corrigida a ligação direta entre SW_NODE e CPR1 que havia sido adicionada na etapa de regras. A continuidade elétrica daquela ligação eliminava a passagem física pelo sensor de corrente. DRC sem conexões faltando não demonstrava a função de medição de T3.

## Caminho atual

`Meia ponte / SW_NODE → JCT1.1 → fio atravessando T3 → JCT1.2 / SW_CT → CPR1.1`

O jumper JCT1 é obrigatório: seu fio deve atravessar **uma vez o núcleo de T3**, como a montagem P1/P2 do oneTeslaTS original. Os dois pads de T3 continuam sendo somente o secundário do sensor; o fio de potência não é conectado a eles. P1/P2 da adaptação atual continuam como terminais do primário externo, sem mudança de suas redes.

## Alterações aplicadas

- Removidas as duas trilhas que tinham sido acrescentadas diretamente entre o final SW_NODE e CPR1.
- Criado `JCT1`, representado no esquema e na placa por dois pads separados. Biblioteca local nova: `CT_Primary_WireLink_P21.59mm.kicad_mod`.
- Centro do jumper coincide com o centro de T3: (58,75;113,10) mm. Pads em (47,955;113,10) e (69,545;113,10) mm, passo de 21,59 mm, diâmetro de cobre de 4 mm e furo de 2,2 mm. O passo corresponde à separação dos pads P1/P2 do Eagle original. O corpo de T3 continua provisório; conferir a montagem com o núcleo real e o fio adquirido.
- Caminho SW_NODE inferior estendido até o pad esquerdo. Pad direito ligado a CPR1.1 pela nova rede `/SW_CT`.
- As duas redes ficam separadas no cobre e no esquema; somente o fio montado em JCT1 as une. Não existe trilha nem zona em paralelo entre os pads.
- Linha tracejada e texto `FIO PELO T3` em F.Fab mostram a montagem do fio; não são cobre. A referência JCT1 está na serigrafia.
- Atualizadas a referência de conectividade e a contagem de componentes de `scripts/validate_schematic.py` para o novo jumper. O gerador histórico `build_schematic.py` não foi executado e não deve ser usado para recriar esta revisão.
- Nenhum componente existente foi movido. Pads de FB1, serigrafia corrigida e fillets das zonas foram preservados.

## Verificação

`verify.py` confere as netlists exportadas nativamente pelo KiCad:

- `/SW_NODE`: JCT1.1, Q1.3, Q2.2, T1.4, Z1.2 e Z2.1.
- `/SW_CT`: exclusivamente JCT1.2 e CPR1.1.
- Todas as demais redes permanecem idênticas à netlist anterior.
- Secundário de T3 e terminais P1/P2 preservados.
- Refill/DRC nativo: **zero curtos, zero violações de clearance e zero conexões faltando na PCB**. Isso verifica o roteamento até os pads; a montagem e a fase magnética do fio precisam seguir a montagem correta do CT.
- ERC: mesmos dois erros de alimentação AC do PS1 e três avisos anteriores (+5V/GND local/global e PE isolado), sem novo problema elétrico associado ao jumper. A cópia de backup em subpasta também produz avisos de bibliotecas por não ter suas tabelas no mesmo diretório; esses avisos de localização foram separados na comparação.
- Permanecem **18 ocorrências de montagem**: as 16 anteriores e duas novas relativas ao pad direito de JCT1 dentro do envelope de montagem de CPR1 (sobreposição de courtyard e PTH no courtyard). O pad fica ao lado do terminal esquerdo do capacitor, fora do corpo nominal, com cobre da mesma rede; a montagem física dos terminais/fio precisa ser conferida.
- A checagem adicional de paridade aponta **26 divergências anteriores** de campos, C9, J2 ausente e referências mecânicas genéricas. Nenhum apontamento de paridade envolve JCT1; não foram corrigidos itens fora desta alteração.

Inspeção visual feita em `jumper-detail.png` e `schematic-detail.png`. O desenho evidencia a interrupção do caminho de cobre sob o núcleo; a indicação tracejada pertence à fabricação/montagem.

Backups `before-oneTesla.kicad_pcb` e `before-oneTesla.kicad_sch`, netlists anterior/posterior, DRC e ERC nesta pasta. `apply.py` é registro da edição, não ferramenta para reaplicar na placa atual. `verify.py` é a verificação reproduzível sobre os artefatos exportados.
