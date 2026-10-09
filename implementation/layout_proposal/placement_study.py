"""Non-production placement study. Run with KiCad 10 pcbnew in a container.

This moves footprints without moving/rerouting their copper. The output PCB is
only for mechanical spacing review; it must never replace oneTesla.kicad_pcb
until routing and native checks are completed.
"""
from pathlib import Path
import json
import re
import pcbnew

root = Path('/work')
board = pcbnew.LoadBoard(str(root / 'oneTesla.kicad_pcb'))
targets = {
    'J1': (135, -3.429),
    'J110': (105, 13),
    'C12': (165, 25), 'C11': (165, 60),
    'Q1': (86.9455, 45.985), 'Q2': (86.9455, 63.765),
    'H4': (106.186, 51.435), 'H2': (106.186, 69.215),
    'Z1': (118.105, 48.895), 'Z2': (118.105, 70.31),
    'T1': (63.325, 58.42), 'R4': (52.705, 80),
    'C8': (53.815, 38.1), 'C13': (43.815, 82),
    'CPR1': (65, 115), 'T3': (23.5, 112),
    'P1': (47, 142), 'P2': (18, 142),
    'JPRT2': (88.9, 141),
}
for f in board.GetFootprints():
    if f.GetReference() in targets:
        x, y = targets[f.GetReference()]
        f.SetPosition(pcbnew.VECTOR2I(round(x*1e6), round(y*1e6)))

corners = [(-7, -18), (185, -18), (185, 155), (-7, 155)]
edges = [g for g in board.GetDrawings() if g.GetLayer() == pcbnew.Edge_Cuts]
assert len(edges) == 4
for g in edges:
    board.Remove(g)
for a, b in zip(corners, corners[1:] + corners[:1]):
    g = pcbnew.PCB_SHAPE(board)
    g.SetShape(pcbnew.SHAPE_T_SEGMENT)
    g.SetStart(pcbnew.VECTOR2I(round(a[0]*1e6), round(a[1]*1e6)))
    g.SetEnd(pcbnew.VECTOR2I(round(b[0]*1e6), round(b[1]*1e6)))
    g.SetLayer(pcbnew.Edge_Cuts)
    g.SetWidth(0)
    board.Add(g)

def rect(f):
    b = f.GetCourtyard(pcbnew.F_CrtYd).BBox()
    return (b.GetX(), b.GetY(), b.GetRight(), b.GetBottom())

parts = [f for f in board.GetFootprints() if f.GetCourtyard(pcbnew.F_CrtYd).OutlineCount()]
hits = []
for i, a in enumerate(parts):
    x1,y1,x2,y2 = rect(a)
    for b in parts[i+1:]:
        u1,v1,u2,v2 = rect(b)
        dx,dy = min(x2,u2)-max(x1,u1), min(y2,v2)-max(y1,v1)
        if dx > 0 and dy > 0:
            hits.append((a.GetReference(),b.GetReference(),round(dx/1e6,3),round(dy/1e6,3)))

out = root / 'implementation/layout_proposal'
out.mkdir(exist_ok=True)
study_path = out / 'placement-study.kicad_pcb'
pcbnew.SaveBoard(str(study_path), board)

# pcbnew 10 reassigns seven track net names when saving this moved-footprint
# study. Preserve the source net on every unchanged copper item by UUID.
item_pattern = re.compile(r'\((?:segment|via)\n.*?\n\t\)', re.S)
net_pattern = re.compile(r'\(net "[^"]*"\)')
uuid_pattern = re.compile(r'\(uuid "([^"]+)"\)')
def copper_blocks(source):
    result = {}
    for m in item_pattern.finditer(source):
        u = uuid_pattern.search(m.group())
        n = net_pattern.search(m.group())
        assert u and n
        result[u.group(1)] = n.group()
    return result

source_nets = copper_blocks((root / 'oneTesla.kicad_pcb').read_text())
study_text = study_path.read_text()
assert set(source_nets) == set(copper_blocks(study_text))
def keep_net(m):
    block = m.group()
    uuid = uuid_pattern.search(block).group(1)
    return net_pattern.sub(source_nets[uuid], block, count=1)
study_text = item_pattern.sub(keep_net, study_text)
assert source_nets == copper_blocks(study_text)
study_path.write_text(study_text)
(out / 'bbox-overlaps.json').write_text(json.dumps(hits,indent=2))
print(json.dumps({'moved': len(targets), 'bbox_overlaps': hits},indent=2))
