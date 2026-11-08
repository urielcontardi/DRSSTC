# ARCSTRIKE

Projeto de uma **DRSSTC — bobina de Tesla de estado sólido com dupla ressonância**.
Reúne eletrônica em KiCad, cálculos do ressonador, gabinete paramétrico e arquivos
para fabricação e impressão 3D.

![Montagem mecânica da case v5](mechanical/case-v5/assembly-solidcraft.png)

**Revisão mecânica atual:** case v5 com tampa e plataforma unificadas.
O projeto está em fase de protótipo: encaixes físicos, comportamento térmico e
isolação elétrica ainda precisam de validação. O suporte do fio primário está pendente.

## Comece aqui

| Objetivo | Acesso |
| --- | --- |
| Imprimir o gabinete atual | [STLs — 13 modelos, 26 peças](production/case/v5-unified/print/) |
| Atualizar uma case v5 já impressa | [Tampa unificada e alterações de ferragens](mechanical/case-v5-unified/README.md) |
| Consultar a montagem da base v5 | [Guia mecânico e lista de ferragens](mechanical/case-v5/README.md) |
| Editar a eletrônica | [Projeto KiCad](hardware/pcb/oneTesla.kicad_pro) · [Guia da PCB](hardware/pcb/README.md) |
| Consultar os cálculos | [Projeto das bobinas](docs/design/COILS.md) |
| Explorar a documentação offline | [Caderno HTML](docs/project/PROJECT-DRSSTC.html) |
| Importar a montagem atual em CAD | [STEP com tampa unificada](mechanical/case-v5-unified/exports/ARCSTRIKE-v5-tampa-unificada.step) |
| Consultar pacotes e revisões | [Entregáveis](production/README.md) |

Para uma case v5 já impressa, somente a tampa unificada precisa ser impressa.
Ela substitui as peças 04 e 05; a abraçadeira inferior passa a usar quatro
M3×16. Consulte o guia antes de montar. Os ZIPs da v5 original conservam a
tampa e a plataforma separadas.

## Organização

```text
hardware/pcb/       Projeto KiCad e bibliotecas locais
mechanical/         Fontes CAD, parâmetros e verificações por revisão
production/         Pacotes de entrega, Gerbers, STEP e seleção de impressão
docs/               Cálculos, caderno do projeto e referências técnicas
scripts/            Ferramentas de geração, cálculo e validação
output/             Resultados temporários locais (fora do Git)
```

As fontes editáveis ficam em `hardware/` e `mechanical/`. Os entregáveis em
`production/` representam a revisão indicada no caminho e não se atualizam
quando as fontes mudam. Revisões mecânicas anteriores permanecem disponíveis
para rastreabilidade; o [índice mecânico](mechanical/README.md) identifica cada uma.

## Ferramentas e reprodução

Execute os comandos na raiz do repositório. Use Python 3 para os cálculos,
KiCad para a eletrônica e CadQuery via `uv` para os modelos paramétricos.
O caderno HTML também usa Node.js; as montagens `.sc` abrem no SolidCraft.

```sh
# Recalcular o ressonador
python3 -B scripts/calculate_resonator.py

# Verificar a malha da tampa unificada
python3 -B mechanical/case-v5-unified/verify_stls.py

# Reconstruir a tampa e a montagem atual (requer uv e CadQuery)
uv run --with cadquery python mechanical/case-v5-unified/build.py
```

Os comandos de reconstrução escrevem nos diretórios de exportação. Confira o
diff e os relatórios antes de atualizar entregáveis. Mantenha as bibliotecas
junto ao projeto KiCad para preservar os caminhos `${KIPRJMOD}/library/...`.

## Documentação

- [Índice técnico e referências](docs/README.md)
- [Revisões e reconstrução mecânica](mechanical/README.md)
- [Pacotes de fabricação e impressão](production/README.md)
- [Ferramentas e comandos de validação](scripts/README.md)
- [Convenções para manutenção](CONTRIBUTING.md)
