"""Rebuild the offline viewer without regenerating CAD. Stdlib only."""
from pathlib import Path
import base64, json, math, shutil, subprocess

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'exports'
raw=(OUT/'viewer_meshes.json').read_text()
meshes=json.loads(raw)
if shutil.which('node'):
    subprocess.run(['node',str(ROOT/'render_preview.cjs')],check=True)

# An embedded SVG is visible even when scripts are blocked by a file preview.
w,h=1600,1000
ca,sa=math.cos(2.46),math.sin(2.46)
cb,sb=math.cos(1.02),math.sin(1.02)
scale=h/530
polygons=[]
for m in meshes:
    if m['kind']=='placeholder':continue
    a=m['positions']
    for i in range(0,len(a),9):
        projected=[]
        for j in (i,i+3,i+6):
            x,y,z=a[j]-50,a[j+1]-50,a[j+2]-160
            rx,ry=ca*x-sa*y,sa*x+ca*y
            projected.append((w*.59+rx*scale,h*.5-(cb*ry+sb*z)*scale,-sb*ry+cb*z))
        p,q,r=projected
        if abs((q[0]-p[0])*(r[1]-p[1])-(q[1]-p[1])*(r[0]-p[0]))<2:continue
        ax,ay,az=(a[i+3+k]-a[i+k] for k in range(3))
        bx,by,bz=(a[i+6+k]-a[i+k] for k in range(3))
        nx,ny,nz=ay*bz-az*by,az*bx-ax*bz,ax*by-ay*bx
        length=math.sqrt(nx*nx+ny*ny+nz*nz) or 1
        shade=.42+min(19,round(7+8*abs(nz/length)+3*abs(nx/length)))*.028
        color=','.join(str(round(c*255*shade)) for c in m['color'])
        pts=' '.join(f'{x:.1f},{y:.1f}' for x,y,z in projected)
        polygons.append((sum(v[2] for v in projected)/3,f'<polygon points="{pts}" fill="rgb({color})"/>'))
polygons.sort(key=lambda p:p[0])
svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}"><rect width="1600" height="1000" fill="#111820"/>'+''.join(p[1] for p in polygons)+'</svg>'
(OUT/'case-preview.svg').write_text(svg)
fallback='data:image/svg+xml;base64,'+base64.b64encode(svg.encode()).decode()
if (OUT/'case-preview.png').exists():
    fallback='data:image/png;base64,'+base64.b64encode((OUT/'case-preview.png').read_bytes()).decode()
template=(ROOT/'viewer.template.html').read_text()
script=(ROOT/'viewer.js').read_text().replace('__MESH_DATA__',raw)
html=template.replace('__STATIC_PREVIEW__',fallback).replace('__VIEWER_SCRIPT__',script)
assert '__MESH_DATA__' not in html and '__STATIC_PREVIEW__' not in html
(OUT/'case-viewer.html').write_text(html)
print(f'Viewer Canvas 2D + embedded static preview: {len(polygons)} preview triangles.')
