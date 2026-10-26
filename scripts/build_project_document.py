"""Build an offline project notebook with the verified PCB mesh and calculations.

Run: python3 -B scripts/build_project_document.py
The archived case ZIP supplies only the existing PCB tessellation/renderer.
No removed mechanical files are restored.
"""
from pathlib import Path
import base64,hashlib,html,json,shutil,subprocess,tempfile,zipfile,sys

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/project'
ASSETS=OUT/'assets'
ASSETS.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(ROOT/'scripts'))
from sexpr import parse,children,prop

result=json.loads((ROOT/'docs/design/resonator-results.json').read_text())
inputs=json.loads((ROOT/'docs/design/resonator-inputs.json').read_text())
step=ROOT/'production/pcb/2026-10-20-3d/ARCSTRIKE-PCB-complete.step'
archive=ROOT/'production/case/v1/ARCSTRIKE-case-v1-CONCEPT.zip'
with zipfile.ZipFile(archive) as z:
    assert hashlib.sha256(z.read('case-v1/reference/ARCSTRIKE-PCB-complete.step')).digest()==hashlib.sha256(step.read_bytes()).digest(), 'PCB mesh source no longer matches STEP; re-tessellate before publishing.'
    old=z.read('case-v1/exports/case-viewer.html').decode()
    meshes=json.JSONDecoder().raw_decode(old.split('const data=',1)[1])[0]
    pcb=next(m for m in meshes if m['name']=='pcb_reference')
    renderer=z.read('case-v1/viewer.js').decode()
    preview=z.read('case-v1/render_preview.cjs').decode()

# Keep exact geometry. Colors below illustrate material categories only.
palette={'Board and substrate':(.10,.38,.24),'Terminals and metal surfaces':(.72,.76,.79),
 'DC bus capacitors':(.10,.12,.14),'Component bodies':(.19,.23,.27),
 'Resonant capacitor CPR1':(.55,.32,.16)}
groups={name:dict(name=name,color=color,positions=[],kind='reference') for name,color in palette.items()}
a=pcb['positions']
for i in range(0,len(a),9):
    tri=a[i:i+9];x=sum(tri[0::3])/3;y=sum(tri[1::3])/3;zz=sum(tri[2::3])/3
    zmin=min(tri[2::3]);zmax=max(tri[2::3])
    if zmin>=-.08 and zmax<=1.525:name='Board and substrate'
    elif zmax<1.7:name='Terminals and metal surfaces'
    elif zz>41.9:name='Terminals and metal surfaces'
    elif zz>1.8 and any((x-cx)**2+(y-71.05)**2<15.3**2 for cx in (84.125,53.13)):name='DC bus capacitors'
    elif zz>2 and abs(x-67.525)<23.2 and abs(y-10.65)<9.6:name='Resonant capacitor CPR1'
    elif zz<-.1:name='Component bodies' if zz> -4.9 else 'Terminals and metal surfaces'
    else:name='Component bodies'
    groups[name]['positions'].extend(tri)
data=list(groups.values())
assert sum(len(g['positions']) for g in data)==len(a)

# Adapt the previously tested CPU depth-buffer renderer to a document panel.
renderer=renderer.replace('const d=1,w=innerWidth,h=innerHeight;',
 'const rect=canvas.getBoundingClientRect?canvas.getBoundingClientRect():{width:innerWidth,height:innerHeight};const d=1,w=Math.max(1,Math.round(rect.width)),h=Math.max(1,Math.round(rect.height));')
renderer=renderer.replace('w*(w>700?.59:.54)','w*.5').replace('(140+exp*1.3)','(95+exp*1.3)').replace('*exp-30-exp*.4','*exp-17-exp*.4')
payload=json.dumps(data,separators=(',',':'))
with tempfile.TemporaryDirectory(prefix='arcstrike-notebook-') as temp:
    temp=Path(temp);(temp/'exports').mkdir()
    (temp/'viewer.js').write_text(renderer)
    (temp/'render_preview.cjs').write_text(preview)
    (temp/'exports/viewer_meshes.json').write_text(payload)
    subprocess.run(['node',str(temp/'render_preview.cjs')],check=True)
    shutil.copy2(temp/'exports/case-preview.png',ASSETS/'pcb-preview.png')

board=parse((ROOT/'hardware/pcb/oneTesla.kicad_pcb').read_text())
models=0;components={}
for f in children(board,'footprint'):
    ref=prop(f,'Reference');value=prop(f,'Value')
    if children(f,'model'):models+=1
    if ref and value:components[ref[2]]=value[2]
selection=['Q1','Q2','CPR1','C11','C12','PS1','IC3','IC4','T1','T3','FB1','J1','J2']
functions={'Q1':'Half-bridge IGBT','Q2':'Half-bridge IGBT','CPR1':'Primary tank capacitor',
 'C11':'DC bus capacitor','C12':'DC bus capacitor','PS1':'Auxiliary power supply',
 'IC3':'Gate driver','IC4':'Gate driver','T1':'Gate drive transformer',
 'T3':'Feedback current transformer','FB1':'Optical receiver','J1':'AC L/N input','J2':'PE / control GND input'}
rows=''.join(f'<tr><td><code>{ref}</code></td><td>{html.escape(components[ref])}</td><td>{functions[ref]}</td></tr>' for ref in selection)
def fmt(v,n=2):return f'{v:,.{n}f}'
tap_rows=''.join('<tr'+(' class="selected"' if r['turns']==6 else '')+f'><td>{fmt(r["turns"],1)}</td><td>{fmt(r["coil_uh"],3)}</td><td>{fmt(r["total_uh"],3)}</td><td>{fmt(r["frequency_khz"],2)}</td></tr>' for r in result['primary']['turns_table'])
sensitivity=''.join(f'<tr><td>{r["extra_pf"]}</td><td>{fmt(r["total_pf"],2)}</td><td>{fmt(r["secondary_khz"],2)}</td><td>{fmt(r["primary_target_khz"],2)}</td></tr>' for r in result['capacitance_sensitivity'])
coupling=''.join(f'<tr><td>{r["gap_from_primary_plane_to_secondary_winding_start_mm"]} mm</td><td>{fmt(r["k_estimate"],3)}</td></tr>' for r in result['coupling_geometry_estimates'])
for source,dest in [(step,'PCB-complete.step'),(ROOT/'docs/design/COILS.md','COILS.md'),
 (ROOT/'docs/design/resonator-inputs.json','inputs.json'),(ROOT/'docs/design/resonator-results.json','results.json'),
 (ROOT/'docs/reference/oneTeslaTS_User_Manual.pdf','oneTeslaTS-manual.pdf'),
 (ROOT/'docs/reference/oneTeslaTS_Parts.pdf','original-parts-list.pdf')]:shutil.copy2(source,ASSETS/dest)

template=(ROOT/'docs/project/document.template.html').read_text()
fallback='data:image/png;base64,'+base64.b64encode((ASSETS/'pcb-preview.png').read_bytes()).decode()
tokens={'__COMPONENT_ROWS__':rows,'__TAP_ROWS__':tap_rows,'__SENSITIVITY_ROWS__':sensitivity,
 '__COUPLING_ROWS__':coupling,'__MODEL_COUNT__':str(models),'__PCB_IMAGE__':fallback,
 '__RESULTS__':json.dumps(result,separators=(',',':')),'__INPUTS__':json.dumps(inputs,separators=(',',':')),
 '__VIEWER_CODE__':renderer.replace('__MESH_DATA__',payload)}
for key,value in tokens.items():template=template.replace(key,value)
assert not any(k in template for k in tokens)
(OUT/'PROJECT-DRSSTC.html').write_text(template)
manifest=dict(schema_version=1,pcb_step_sha256=hashlib.sha256(step.read_bytes()).hexdigest(),
 calculation_inputs_sha256=hashlib.sha256((ROOT/'docs/design/resonator-inputs.json').read_bytes()).hexdigest(),
 triangle_count=len(a)//9,footprints_with_3d=models,mesh_geometry_unchanged=True,
 viewer='Canvas 2D software depth buffer; static PNG fallback; no WebGL/CDN',
 files={str(p.relative_to(OUT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in OUT.rglob('*') if p.is_file() and p.name not in ('manifest.json','document.template.html')})
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
package=ROOT/'production/documentation/2026-10-22/ARCSTRIKE-documentation.zip'
package.parent.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(package,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for p in OUT.rglob('*'):
        if p.is_file() and p.name!='document.template.html':z.write(p,p.relative_to(OUT))
print(f'HTML generated: {models} footprints with 3D; {len(a)//9} unchanged triangles; package {package.stat().st_size} bytes.')
