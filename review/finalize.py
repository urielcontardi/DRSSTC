from pathlib import Path
import csv,json,hashlib
p=Path(__file__).resolve().parent
rows=list(csv.DictReader((p/'cobertura-pcb.csv').open()))
lines=['# Cobertura por referência — PCB atual','','48/48 instâncias inventariadas e anotadas. **Cobertura não significa aprovação da peça.** Pinagem, passo e furo estão nos CSV.','','| Referência | Valor | Polaridade/pinagem | Encaixe e pendências |','|---|---|---|---|']
for r in sorted(rows,key=lambda x:x['referencia']):
 lines.append('| '+' | '.join(r[k].replace('|','/').replace(chr(10),' ') for k in ['referencia','valor','polaridade','encaixe'])+' |')
(p/'COBERTURA.md').write_text(chr(10).join(lines)+chr(10))
lib=list(csv.DictReader((p/'cobertura-bibliotecas.csv').open()))
checks=[]
for r in lib:
 pads=json.loads(r['pads']);issues=[];rings=[]
 for x in pads:
  if x['tipo']=='thru_hole':
   try:d=float(x['furo']);ring=(min(x['sx'],x['sy'])-d)/2;rings.append(ring)
   except ValueError:issues.append('furo não circular: conferir manualmente');continue
   if ring<=0:issues.append('pad '+x['num']+' sem anel positivo')
 if not int(r['courtyard_elementos']):issues.append('sem F.CrtYd')
 if not int(r['fabricacao_elementos']):issues.append('sem F.Fab')
 checks.append({'arquivo':r['arquivo'],'uso':r['uso'],'numero_pads':len(pads),'anel_nominal_min_mm':round(min(rings),4) if rings else 'N/A','checagens_basicas':'; '.join(issues) or 'sem anomalia nas checagens básicas','limite':'Não verifica tolerâncias, anel efetivo após fabricação, encaixe ou pinagem contra MPN'})
with (p/'checagem-bibliotecas.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=checks[0].keys());w.writeheader();w.writerows(checks)
print('Bibliotecas:',len(checks),'Alertas:',[(r['arquivo'],r['checagens_basicas']) for r in checks if r['checagens_basicas']!='sem anomalia nas checagens básicas'])
report=p/'RELATORIO.md'
s=report.read_text().replace('Clone novo, inicialmente limpo; nenhum arquivo de projeto alterado.','Clone recuperado da execução anterior, inicialmente limpo; nenhum arquivo de projeto alterado.')
marker='## Fechamento da retomada e bloqueio da homologação completa'
if marker not in s:
 s+='''

## Fechamento da retomada e bloqueio da homologação completa

A retomada preservou o clone e os artefatos anteriores. Foram reinspecionadas as quatro vistas PNG (topo, fundo, montagem e Eagle), o desenho mecânico Broadcom e as tabelas de medidas. DRC e ERC do principal foram repetidos em contêiner sem rede, projeto somente leitura: **529 violações, 56 questões de paridade, 0 não conectados; ERC 2**. Resultados: evidence/drc-recovery.json e evidence/erc-recovery.json. Os SHA-256 dos **166 arquivos originais** continuam idênticos a inventario.csv.

A anotação individual escrita mas ainda não executada foi aplicada: cobertura-pcb.csv contém conclusões específicas para todas as referências, também legíveis em COBERTURA.md. checagem-bibliotecas.csv acrescenta checagens básicas de anel nominal, presença de F.Fab/F.CrtYd para **135/135 modelos**, incluindo os não usados. Isso não substitui comparação com uma peça.

### Matriz de encerramento honesto

| Item solicitado | Executado | O que impede aprovação completa |
|---|---|---|
| PCB KiCad atual | DRC/paridade, geometria 48/48, netlist, inspeção das duas faces/montagem | Achados F01–F08; MPNs e tolerâncias ausentes |
| Eagle legado | Inventário 51/51, importação KiCad, DRC e vista superior | Sem ERC/DRC no Eagle original; peças legadas não homologadas individualmente |
| Bibliotecas | Inventário e checagens básicas 135/135; 24 modelos usados com análise por referência | 111 modelos não usados sem associação exata a peças; não é possível verificar datasheet de componente não selecionado |
| Esquemas KiCad | ERC dos cinco arquivos e comparação das netlists | Revisões divergem funcionalmente; designar fonte de fabricação |
| Isolação HV/PE | Geometria e falhas locais identificadas | Rede máxima, transientes, norma, altitude, poluição, CTI/coating e bonding sem especificação suficiente |
| Corrente, comutação e temperatura | Caminhos, vias, loops e riscos qualitativos | Frequência, corrente de pico/RMS, duração/repetição dos pulsos, cobre/plating, ambiente e dissipador |
| Mecânica final | Envelopes e conflitos CAD | MPNs, amostras, tolerâncias da fábrica, magnetismos e conjunto dissipador/enclosure |

**Resultado entregue: relatório de revisão CAD com cobertura e bloqueios, não homologação integral de todas as peças.** Para encerrar a parte física solicitada, fornecer BOM comprável (fabricante + código completo + variante), desenhos/bobinagem de T1/T3, modelos dos terminais/IEC/clipes/soquetes, peças C11/C12 e dados operacionais acima. Não escolher substitutos implicitamente. Sem isso, não há base para declarar pinagem/pitch/drill/polaridade de cada peça real confirmados. Nenhum erro encontrado exige energizar a placa para ser demonstrado.

Não foi aplicado patch à placa, ao esquema ou às bibliotecas; não houve push, PR, alteração no Gateway nem certificação de segurança.
'''
report.write_text(s)
manifest=[]
for f in sorted(p.rglob('*')):
 if f.is_file() and f.name!='SHA256SUMS':manifest.append(hashlib.sha256(f.read_bytes()).hexdigest()+'  '+str(f.relative_to(p)))
(p/'SHA256SUMS').write_text(chr(10).join(manifest)+chr(10))
