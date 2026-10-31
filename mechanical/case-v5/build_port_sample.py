"""Crop the actual assembled side wall to test the fiber connector's reach and latch."""
from pathlib import Path
import cadquery as cq
R=Path(__file__).resolve().parent;O=R/'exports'
a=cq.importers.importStep(str(O/'01_lower_tray.step')).val()
b=cq.importers.importStep(str(O/'02_upper_sleeve.step')).val()
s=a.fuse(b).intersect(cq.Solid.makeBox(16,40,34,cq.Vector(-20,8.35,-2)))
assert s.isValid() and len(s.Solids())==1
s=s.rotate((0,0,0),(0,1,0),-90);bb=s.BoundingBox();s=s.translate((-bb.xmin,-bb.ymin,-bb.zmin))
cq.exporters.export(s,str(O/'print/94_fiber_access_sample.stl'),tolerance=.08)
print('Fiber access sample exported from actual assembled walls')
