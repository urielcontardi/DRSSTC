"""Reserve envelopes, not manufacturer CAD of a user's unspecified cable/plug."""
from pathlib import Path
import json
import cadquery as cq
R=Path(__file__).resolve().parent;O=R/'exports'
parts={n:cq.importers.importStep(str(O/(n+'.step'))).val() for n in ['01_lower_tray','02_upper_sleeve']}
probes={'straight_plug_approach_10x7p6':cq.Solid.makeBox(40,10,7.6,cq.Vector(-46.4,23.35,1.295)), 'rear_latch_finger_10x15':cq.Solid.makeBox(20.2,10,15,cq.Vector(-29,23.35,8))}
checks=[]
for name,probe in probes.items():
 for part,shape in parts.items():
  vol=max(0,probe.intersect(shape).Volume());checks.append(dict(probe=name,part=part,overlap_mm3=vol));assert vol<.02,(name,part,vol)
(O/'fiber-access-verification.json').write_text(json.dumps(dict(status='reserved approach and latch finger envelopes; actual plug fit remains a physical check',checks=checks,failures=[]),indent=2)+'\n')
print('Fiber approach and latch reach envelopes clear')
