Modelo 3D atualizado em 2026-10-20

Adicionados modelos STEP genéricos com corpo Ø30,3 × 40,5 mm e terminais
com passos de 9 e 10 mm. Dimensões do corpo informadas pelo usuário;
terminais cilíndricos Ø1,2 × 3 mm são apenas aproximações visuais.
Não são modelos CAD do fabricante nem validam a especificação elétrica.

C11 e C12 na PCB ativa agora referenciam o STEP de passo 10 mm,
correspondente aos pads existentes. As duas variantes da biblioteca local
(9 e 10 mm), incluindo a variante DFM de C12, também referenciam STEP.
O passo 9 mm informado não foi aplicado aos furos/trilhas da PCB.
Os valores elétricos existentes foram preservados.

Validação: sólidos reimportados com CadQuery, geometria válida e dimensões
conferidas; exportação STEP pelo KiCad de C11/C12 concluída. Comparação
estrutural antes/depois confirmou alteração somente das referências 3D.

Regerar: `uv run --with cadquery python scripts/models3d/capacitor_snapin.py`
