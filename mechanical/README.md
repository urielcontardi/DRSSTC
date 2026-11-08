# Projeto mecânico

A montagem atual combina a **base v5** com a **tampa unificada**.
Para imprimir, use a [seleção atual de STLs](../production/case/v5-unified/print/),
com quantidades nos nomes dos arquivos.

| Revisão | Finalidade | Estado |
| --- | --- | --- |
| [v5 unificada](case-v5-unified/README.md) | Tampa e plataforma em uma peça; reutiliza as demais peças v5 | Atual, depende das fontes v5 |
| [v5](case-v5/README.md) | Base com berço de dissipador ajustável e acesso à fibra | Base da montagem atual |
| [v4](case-v4/README.md) | Encaixes guiados, porcas cativas e retenção do dissipador | Histórico |
| [v3](case-v3/README.md) | Gabinete compacto com plataforma circular | Histórico |
| [v2](case-v2/README.md) | Integração do gabinete e ressonador | Histórico |
| [v1 — pacote](../production/case/v1/ARCSTRIKE-case-v1-CONCEPT.zip) | Conceito inicial; fontes dentro do pacote | Histórico |

## Convenções dos arquivos

- `build.py` e `parameters.json`, quando presente: geometria paramétrica e entradas.
- `reference/`: componentes de referência necessários à reconstrução.
- `exports/`: STEP, STLs, visualizadores e relatórios da revisão.
- `verify_*.py`: verificações geométricas, de acesso ou de malha.
- `.sc`: montagens para SolidCraft; os arquivos `.plain.sc` são variantes existentes.

Os diretórios de revisão mantêm seus caminhos para preservar dependências entre
fontes e referências. Exportações, imagens, relatórios e pacotes são mantidos
quando servem à inspeção ou ao uso sem instalar as ferramentas CAD.
Backups `.bak` e caches de execução não são versionados.

## Reconstrução atual

Execute na raiz do repositório:

```sh
uv run --with cadquery python mechanical/case-v5-unified/build.py
python3 -B mechanical/case-v5-unified/verify_stls.py
```

Para reconstruir a base, os cupons e as verificações completas, siga o
[guia v5](case-v5/README.md). A reconstrução da tampa usa as fontes v5 e os
STLs da seleção atual para registrar os hashes das peças preservadas.

Os relatórios CAD não substituem a validação física. Os guias de cada revisão
documentam os limites e as pendências de montagem.
