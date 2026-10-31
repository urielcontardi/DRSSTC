# Exported KiCad board bottom is Z=0, model datum/top is Z=1.595.
pcb = cq.importers.importStep(str(ROOT/'reference/ARCSTRIKE-PCB-complete.step')).val().translate((-31.375,127.05,0))
add('pcb_reference',pcb,(0.10,0.40,0.24),'reference')

# Profile from the user's dimensioned drawing: 104 wide, 25 high, 5 base,
# 13 fins at 8 mm pitch, 1.6 mm thickness, 4 mm end-center offset.
# Length 100 mm from user's description. R0.8 fin crowns approximate the sketch.
sink_top=1.595-6.6-P['thermal_pad_nominal_mm']
sw,sl,sh=(P['heatsink_nominal_width_mm'],P['heatsink_nominal_length_mm'],P['heatsink_nominal_height_mm'])
pts=[cq.Vector(x,0,z) for x,z in [(0,0),(104,0),(104,3.5),(102.5,5),(1.5,5),(0,3.5)]]
profile=cq.Wire.makePolygon(pts,close=True)
sink=cq.Solid.extrudeLinear(profile,[],cq.Vector(0,100,0))
for i in range(13):
    xc=4+i*8
    fin=box(xc-.8,0,5,1.6,100,19.2).fuse(cyl(xc,0,24.2,.8,100,(0,1,0)))
    sink=sink.fuse(fin)
sink=sink.clean().rotate((52,50,0),(52,51,0),180).translate((-2,0,sink_top))
if (sw,sl,sh)!=(104,100,25):
    sink=box(50-sw/2,50-sl/2,sink_top-sh,sw,sl,sh)
assert sink.isValid() and len(sink.Solids())==1
add('heatsink_104x100x25_drawing_reference',sink,(.55,.59,.64),'reference')
# This conservative full box is used separately for adjustable-bay checks.
sink_envelope=box(-2,0,sink_top-25,104,100,25)
cq.exporters.export(sink,str(OUT/'heatsink-104x100x25-drawing.step'))


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
