# Exported KiCad board bottom is Z=0, model datum/top is Z=1.595.
pcb = cq.importers.importStep(str(ROOT/'reference/ARCSTRIKE-PCB-complete.step')).val().translate((-31.375,127.05,0))
add('pcb_reference',pcb,(0.10,0.40,0.24),'reference')

# The supplied STL is 19 axis-aligned boxes: one 5 mm base + 18 fins.
# Recover exact boxes, validate every triangle lies on their surfaces.
raw = (ROOT/'reference/heatsink_100x100.stl').read_bytes()
triangles = struct.unpack_from('<I',raw,80)[0]
assert triangles==228 and len(raw)==84+50*triangles
blocks=[]
for start in range(0,triangles,12):
    verts=[]
    for i in range(start,start+12):
        t=struct.unpack_from('<12fH',raw,84+50*i)
        verts.extend((t[3:6],t[6:9],t[9:12]))
    mn=[min(v[k] for v in verts) for k in range(3)]
    mx=[max(v[k] for v in verts) for k in range(3)]
    assert all(all(abs(v[k]-mn[k])<1e-5 or abs(v[k]-mx[k])<1e-5 for k in range(3)) for v in verts)
    blocks.append(box(*mn,*(mx[k]-mn[k] for k in range(3))))
sink = blocks[0].fuse(*blocks[1:]).clean()
assert sink.isValid() and len(sink.Solids())==1
# Real metal face of Q1/Q2 = 1.595 - 6.6 = -5.005 mm.
sink_top = 1.595-6.6-P['thermal_pad_nominal_mm']
sink = sink.rotate((50,50,0),(50,51,0),180).translate((0,0,sink_top))
add('heatsink_reference',sink,(0.65,0.69,0.74),'reference')
assert abs(sink.BoundingBox().center.x-50)<1e-6
assert abs(sink.BoundingBox().center.y-50)<1e-6
cq.exporters.export(sink,str(OUT/'heatsink_aligned.step'))


def stl_solid(path):
    data=path.read_bytes()
    sewing=BRepBuilderAPI_Sewing(1e-5)
    for i in range(struct.unpack_from('<I',data,80)[0]):
        t=struct.unpack_from('<12fH',data,84+50*i)
        points=[cq.Vector(*t[j:j+3]) for j in (3,6,9)]
        wire=cq.Wire.makePolygon(points,close=True)
        sewing.Add(cq.Face.makeFromWires(wire).wrapped)
    sewing.Perform()
    shape=cq.Shape.cast(sewing.SewedShape())
    solids=[cq.Solid.makeSolid(s).fix().clean().fix() for s in shape.Shells()]
    # The supplied housing shell is closed but self-inconsistent in BRep.
    # Keep its six valid contact solids and use a dimensioned housing envelope
    # in STEP. The browser viewer uses the exact original STL for the C14.
    if not all(s.isValid() for s in solids):
        assert len(solids)==7 and all(s.isValid() for s in solids[1:])
        flange=box(-25,-11,-3,50,22,3)
        for x in (-21,21):flange=flange.cut(cyl(x,0,-4,1.6,5))
        housing=flange.fuse(box(-13,-9,-17,26,18,14),box(-15.5,-11,0,31,22,2))
        housing=housing.cut(box(-11.5,-7,-14,23,14,17))
        housing=housing.fuse(box(-9.25,-7.5,-18.6,18.5,15.1,4))
        assert housing.isValid()
        solids=[housing,*solids[1:]]
    assert solids and all(s.isValid() for s in solids)
    return cq.Compound.makeCompound(solids)

c14=stl_solid(ROOT/'reference/C14-Socket-v8.stl')
c14=c14.rotate((0,0,0),(1,0,0),-90).translate((46,hi+6,21))
add('C14_reference',c14,(0.13,0.14,0.16),'reference')
