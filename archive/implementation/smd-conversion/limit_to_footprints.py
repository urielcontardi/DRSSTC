"""Limit the conversion to footprint associations and mechanical information."""
from pathlib import Path
import copy, re, sys, subprocess, csv, io
ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).parent
sys.path.insert(0,str(ROOT/'scripts'))
from sexpr import Atom as A, parse, dump, child, children, prop
refs={'R1','R2','R3','R4','R5','R6','IC1','IC2'}
def spans(s):
    depth=0
    for m in re.finditer(r'"(?:\\.|[^"\\])*"|[()]',s):
        if m.group()=='(':
            depth+=1
            if depth==2:a=m.start()
        elif m.group()==')':
            if depth==2:yield a,m.end()
            depth-=1
def replace(s,changes):
    for a,b,n in sorted(changes,reverse=True):s=s[:a]+dump(n,1)+s[b:]
    return s
board=ROOT/'oneTesla.kicad_pcb';original=board.read_text()
old=parse((HERE/'before-oneTesla.kicad_pcb').read_text())
oldfps={prop(f,'Reference')[2]:f for f in children(old,'footprint')}
footprints={};changes=[]
for a,b in spans(original):
    f=parse(original[a:b])
    if f[0]!='footprint' or prop(f,'Reference')[2] not in refs:continue
    ref=prop(f,'Reference')[2];footprints[ref]=f[1]
    geometrical={key:copy.deepcopy(prop(f,key)) for key in ['Reference','Value']}
    f[:]=[n for n in f if not(isinstance(n,list) and n[0]=='property')]
    for p in children(oldfps[ref],'property'):
        p=copy.deepcopy(p)
        if p[1] in geometrical:
            value=p[2];p=geometrical[p[1]];p[2]=value
        elif p[1]=='Description':p[2]='SMD footprint: '+f[1]
        elif p[1]=='Footprint_Status':p[2]='SMD footprint: '+f[1]+'; component value unchanged.'
        elif p[1]=='Assembly_Notes':p[2]='SMD land pattern; original circuit and nominal component value preserved.'
        elif p[1]=='KiLib_Generator':p[2]='package/gullwing' if ref.startswith('IC') else 'resistor/SMD'
        elif p[1]=='ki_fp_filters':p[2]='SOIC-14* SOP-14*' if ref.startswith('IC') else 'R_*'
        elif p[1]=='Datasheet' and ref=='R1':p[2]=''
        f.append(p)
    changes.append((a,b,f))
assert board.read_text()==original
board.write_text(replace(original,changes))

def update_symbol(sym,ref):
    prop(sym,'Footprint')[2]=footprints[ref]
    if prop(sym,'ki_fp_filters') and ref.startswith('IC'):prop(sym,'ki_fp_filters')[2]='SOIC-14* SOP-14*'
    # Existing mounting notes must describe the changed footprint.
    for key in ['Description','Footprint_Status','Assembly_Notes']:
        if prop(sym,key):prop(sym,key)[2]='SMD footprint: '+footprints[ref]
    if ref=='R1' and prop(sym,'Datasheet'):prop(sym,'Datasheet')[2]=''
    return sym

for file,backup in [('oneTesla.kicad_sch','before-oneTesla.kicad_sch'),('library/oneTesla.kicad_sym','before-oneTesla.kicad_sym')]:
    p=ROOT/file;current=p.read_text();s=(HERE/backup).read_text();changes=[]
    for a,b in spans(s):
        node=parse(s[a:b])
        if file.endswith('.kicad_sch'):
            if node[0]=='symbol' and prop(node,'Reference') and prop(node,'Reference')[2] in refs:
                changes.append((a,b,update_symbol(node,prop(node,'Reference')[2])))
            elif node[0]=='lib_symbols':
                for sym in children(node,'symbol'):
                    key={'oneTesla:74HCT14':'IC1','oneTesla:74HCT74':'IC2'}.get(sym[1])
                    if key:update_symbol(sym,key)
                changes.append((a,b,node))
        elif node[0]=='symbol' and node[1] in ['74HCT14','74HCT74']:
            changes.append((a,b,update_symbol(node,'IC1' if node[1]=='74HCT14' else 'IC2')))
    assert p.read_text()==current
    p.write_text(replace(s,changes))

# Keep the listing consistent with the original nominal values.
s=(ROOT/'output/components.csv').read_text()
rows=list(csv.DictReader(io.StringIO(s)));fields=list(rows[0]);out=io.StringIO()
for row in rows:
    if row['Reference'] in refs:
        ref=row['Reference'];row['Footprint']=footprints[ref]
        row['Value']=prop(oldfps[ref],'Value')[2]
        for key in ['Footprint_Status','Assembly_Notes']:
            row[key]='SMD footprint: '+footprints[ref]
w=csv.DictWriter(out,fieldnames=fields);w.writeheader();w.writerows(rows)
(ROOT/'output/components.csv').write_text(out.getvalue())
print('Limited to SMD footprints; original values preserved; no manufacturer/MPN assignments.')
