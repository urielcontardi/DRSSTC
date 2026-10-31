"""Validate exported binary STLs without extra dependencies."""
from pathlib import Path
from collections import Counter, defaultdict
import struct, json, hashlib
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'exports';PRINT=OUT/'print'
results=[]
for path in sorted(PRINT.rglob('*.stl')):
    raw=path.read_bytes();n=struct.unpack_from('<I',raw,80)[0]
    assert len(raw)==84+50*n,(path,'not binary STL or corrupt triangle count')
    vertices={};coords=[];edges=Counter();directions=Counter();parent=[];volume=0
    def find(i):
        while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
        return i
    def union(a,b):
        a,b=find(a),find(b)
        if a!=b:parent[b]=a
    for i in range(n):
        t=struct.unpack_from('<12fH',raw,84+50*i);p=[t[j:j+3] for j in (3,6,9)];ids=[]
        for v in p:
            key=tuple(round(x,6) for x in v)
            if key not in vertices:vertices[key]=len(coords);coords.append(v);parent.append(len(parent))
            ids.append(vertices[key])
        assert len(set(ids))==3,(path,'degenerate triangle after 1e-6 mm vertex weld')
        union(ids[0],ids[1]);union(ids[1],ids[2])
        for a,b in zip(ids,ids[1:]+ids[:1]):
            edges[tuple(sorted((a,b)))]+=1;directions[tuple(sorted((a,b)))]+=1 if a<b else -1
        a,b,c=p
        volume+=(a[0]*(b[1]*c[2]-b[2]*c[1])+a[1]*(b[2]*c[0]-b[0]*c[2])+a[2]*(b[0]*c[1]-b[1]*c[0]))/6
    bad=sum(v!=2 for v in edges.values());winding=sum(v!=0 for v in directions.values());components=len({find(i) for i in range(len(coords))})
    if bad or winding or components!=1:
        print(path.name,'bad edges',bad,'winding',winding,'components',components,[(count,[coords[i] for i in e]) for e,count in edges.items() if count!=2][:4])
    assert volume>0,(path,'negative or zero signed volume',volume)
    mn=[min(v[k] for v in coords) for k in range(3)];mx=[max(v[k] for v in coords) for k in range(3)]
    assert all(x>=-1e-4 for x in mn),(path,'not in positive print coordinates',mn)
    assert abs(mn[2])<1e-4,(path,'not on print bed',mn[2])
    results.append(dict(file=str(path.relative_to(PRINT)),triangles=n,vertices=len(coords),connected_components=components,watertight=bad==0,consistent_winding=winding==0,signed_volume_mm3=volume,dimensions_mm=[round(mx[k]-mn[k],4) for k in range(3)],bed_z_mm=mn[2],sha256=hashlib.sha256(raw).hexdigest()))
passed=all(r['watertight'] and r['consistent_winding'] and r['connected_components']==1 for r in results)
report=dict(status='PASS' if passed else 'FAIL',units='mm',vertex_weld_tolerance_mm=1e-6,files=results)
(OUT/'stl-verification.json').write_text(json.dumps(report,indent=2)+'\n')
assert passed,'See stl-verification.json for failed files'
print(f'{len(results)} individual STLs: watertight, single connected mesh, outward winding, Z=0.')
