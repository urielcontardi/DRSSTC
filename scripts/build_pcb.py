"""Generate oneTesla.kicad_pcb: faithful 2-layer replica of the original
oneTeslaTS driver board (misc/driver.brd), adapted to the CURRENT schematic
(HLK-15M15BL aux supply instead of T2/D3/IC5, PE separated, P1/P2 primary pads).

Pipeline:
  1. footprints (already patched by pcb_patch_footprints.py) placed on the
     original Eagle element coordinates; rotation found by pad/net matching
  2. copper (wires/vias/polygons) from the original board, grouped by Eagle
     signal -> mapped to KiCad nets; aux-area surgery applied
  3. new copper for PS1/C13/J2, PE wire, primary-loop rewiring
  4. outline, mounting holes, silkscreen (incl. vector logos)

Coordinate space: KiCad y-down, board (0,0)-(106.045,106.045).
Eagle (ex,ey) -> KiCad (ex, BOARD_H - ey).
"""
import json, math, os, sys, uuid as uuidlib
sys.path.insert(0, os.path.dirname(__file__))
from sexpr import parse, children, child, dump, Atom

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOARD_H = 106.045
FY = lambda y: BOARD_H - y  # eagle y -> kicad y

data = json.load(open(os.path.join(ROOT, 'output/pcb-data.json')))
eagle = json.load(open(os.path.join(ROOT, 'output/eagle-board.json')))

COMPS = data['components']
NETS = data['nets']
FP_DIR = os.path.join(ROOT, 'library', 'oneTesla.pretty')

# ---------- net index ----------
net_names = sorted(NETS.keys())
net_idx = {n: i + 1 for i, n in enumerate(net_names)}
def nid(name): return net_idx[name]

# ref,pin -> net
pinnet = {}
for n, nodes in NETS.items():
    for ref, pin in nodes:
        pinnet[(ref, str(pin))] = n

# ---------- eagle signal -> kicad net ----------
SIG2NET = {
 'N$3': 'Net-(D1-K)', '+5V': '+5V', 'N$18': '/GATE_H', 'N$16': 'Net-(IC1-Pad13)',
 'N$15': '/OPTICAL_OUT', 'N$1': 'Net-(T3-S1)', 'N$2': '/GATE_L', 'NEG': '/DC_MINUS',
 '+15V': '+15V', 'HOT': '/AC_L', 'NTRL': '/AC_N', 'POS': '/DC_PLUS', 'N$14': '/SW_NODE',
 'N$17': '/AC_L_FUSED', 'N$22': 'Net-(CPR1-Pad2)', 'N': '/DC_MID', 'N$11': 'Net-(IC3-OUT-Pad6)',
 'N$13': 'Net-(C4-Pad1)', 'N$19': 'Net-(IC2A-C)', 'N$23': 'Net-(T1-AA)', 'N$24': 'Net-(T1-AB)',
 'N$25': '/DRIVE_ENABLE', 'N$4': 'Net-(IC3-IN)', 'N$5': 'Net-(IC1-Pad2)',
 'N$6': 'Net-(IC2A-~{R})', 'GND': 'GND',
}
SIG_DELETE = {'+24V', 'N$21', 'N$9'}

# wires to delete, per signal, identified by endpoints (eagle coords, unordered)
def W(x1, y1, x2, y2): return frozenset([(round(x1, 2), round(y1, 2)), (round(x2, 2), round(y2, 2))])
WIRE_DELETE = {
 'GND': [W(37.47,71.75,37.47,83.19), W(37.47,83.19,41.91,87.63), W(41.91,87.63,43.18,87.63),
         W(43.18,87.63,48.26,87.63), W(48.26,87.63,50.80,87.63), W(50.80,87.63,52.70,89.53),
         W(52.70,89.53,52.70,94.97),
         W(102.36,103.29,100.75,104.74), W(100.75,104.74,46.35,104.78),
         W(46.35,104.78,43.18,101.60), W(43.18,101.60,43.18,87.63)],
 'N$14': [W(19.68,14.61,41.27,14.61),  # inner-layer L2 leftover
          W(19.68,14.61,19.68,11.43), W(19.68,11.43,26.67,4.45), W(26.67,4.45,27.30,4.45),
          W(27.94,4.45,27.30,4.45), W(32.38,4.45,27.94,4.45), W(53.34,4.45,32.38,4.45),
          W(64.14,15.24,53.34,4.45), W(41.27,14.61,39.37,16.51), W(39.37,16.51,39.37,19.68),
          W(64.14,15.24,64.14,33.66)],  # re-added trimmed below (starts at 19.685)
 'HOT': [W(45.70,94.97,19.33,94.97), W(19.33,94.97,13.97,100.33), W(13.97,100.33,13.97,101.60)],  # dead T2 stub
 '+5V': [W(21.59,63.5,21.59,64.77)],  # redundant stub doubling the IC2.4 link
 'NTRL': [W(48.26,101.6,34.29,101.6)],  # dead T2 neutral tap (PS1.2 joins at 48.26)
}
VIA_DELETE = {'GND': [(43.18, 87.63), (102.362, 103.2891)]}  # 2nd becomes J2 pad

# ---------- element mapping ----------
# kicad ref -> eagle element name
EL_MAP = {'Q1': 'U$7', 'Q2': 'U$8', 'T3': 'U$2', 'FB1': 'U$6', 'D4': 'B1',
          'CPR1': 'CPRI', 'J1': 'U$10', 'P1': 'P2', 'P2': 'P1'}
EL_DELETE = {'U$9', 'D3', 'IC5', 'C7'}
# eagle elements that are mechanical (handled specially, not from schematic)
EL_MECH = {'U$1', 'U$3', 'U$4', 'U$5', 'U$12', 'U$13', 'U$14', 'U$15', 'P3', 'P4'}

# my pads allowed to have no eagle counterpart (extra pins vs original)
EXTRA_PADS_OK = {('FB1', '4'), ('FB1', '5'), ('FB1', '8')}
# pads whose eagle signal is intentionally obsolete (schematic changed):
# pair by geometry only, never compare nets
SKIP_NET_CHECK = {('P1', '1'), ('P2', '1'), ('J1', '3'), ('C10', '1'), ('IC6', '3')}

# ---------- load footprints ----------
def load_fp(name):
    return parse(open(os.path.join(FP_DIR, name + '.kicad_mod')).read())

fp_trees = {}
fp_pads = {}
for ref, c in COMPS.items():
    fn = c['footprint']
    if fn not in fp_trees:
        t = load_fp(fn)
        fp_trees[fn] = t
        pads = []
        for p in children(t, 'pad'):
            at = child(p, 'at')
            size = child(p, 'size')
            drill = child(p, 'drill')
            pads.append({'num': str(p[1]), 'x': float(at[1]), 'y': float(at[2]),
                         'sx': float(size[1]), 'sy': float(size[2]),
                         'drill': float(drill[1]) if drill and len(drill) > 1 else 0.0,
                         'np': str(p[2]) == 'np_thru_hole'})
        fp_pads[fn] = pads

# ---------- eagle element pads (global, flipped) ----------
epk = json.load(open(os.path.join(ROOT, 'output/eagle-packages.json')))
elements = {e['name']: e for e in eagle['elements']}

def rot_pt(x, y, deg):
    r = math.radians(deg)
    c, s = math.cos(r), math.sin(r)
    return (x * c - y * s, x * s + y * c)

def eagle_el_pads(elname):
    """signal pads of an eagle element: list of (padname, kx, ky, signal) in KiCad space"""
    e = elements[elname]
    pkg = epk[e['package']]
    theta = float(e['rot'][1:]) if e['rot'] != 'R0' else 0.0
    out = []
    # pad -> signal
    pad2sig = {}
    for sname, s in eagle['signals'].items():
        for cr in s['contactrefs']:
            if cr[0] == elname:
                pad2sig[cr[1]] = sname
    for p in pkg['pads']:
        dx, dy = rot_pt(p['x'], p['y'], theta)
        gx, gy = e['x'] + dx, e['y'] + dy
        out.append({'name': p['name'], 'kx': gx, 'ky': FY(gy), 'sig': pad2sig.get(p['name']),
                    'drill': p['drill']})
    return out

# ---------- placement search ----------
def place_element(ref, elname):
    """find (pos, rot) so my footprint pads land on the eagle pads with matching nets"""
    e = elements[elname]
    fn = COMPS[ref]['footprint']
    mypads = [p for p in fp_pads[fn] if not p['np']]
    epads = [p for p in eagle_el_pads(elname) if p['sig']]
    theta = float(e['rot'][1:]) if e['rot'] != 'R0' else 0.0
    rho_el = (-theta) % 360
    best = None
    for delta in (0, 90, 180, 270):
        rho = (rho_el + delta) % 360
        tp = [(p['num'], *rot_pt(p['x'], p['y'], rho)) for p in mypads]
        t0x, t0y = e['x'], FY(e['y'])
        # refine translation by net-compatible pairing until it settles.
        # skip/unconnected pads are excluded here (verified geometrically at
        # scoring); assignment is confident-first so duplicate-net pads
        # (fuse tangs etc.) can't steal pads from the true pair.
        for it in range(25):
            radius = 20.0 if it == 0 else 9.0
            cands = []
            for num, dx, dy in tp:
                bx, by = t0x + dx, t0y + dy
                net = pinnet.get((ref, num))
                skip = (ref, num) in SKIP_NET_CHECK or (net or '').startswith('unconnected-')
                if skip:
                    continue
                best_c = None
                for q in epads:
                    if SIG2NET.get(q['sig']) != net:
                        continue
                    d = math.hypot(bx - q['kx'], by - q['ky'])
                    if d < radius and (best_c is None or d < best_c[0]):
                        best_c = (d, q)
                if best_c:
                    cands.append((best_c[0], num, dx, dy, best_c[1]))
            cands.sort(key=lambda c: c[0])
            pairs, used = [], set()
            for d, num, dx, dy, q in cands:
                if q['name'] in used:
                    continue
                used.add(q['name'])
                pairs.append((dx, dy, q))
            if not pairs:
                break
            mx = sum(q['kx'] - (t0x + dx) for dx, _, q in pairs) / len(pairs)
            my = sum(q['ky'] - (t0y + dy) for _, dy, q in pairs) / len(pairs)
            t0x += mx
            t0y += my
            if abs(mx) < 0.005 and abs(my) < 0.005:
                break
        # score
        matched, mism, dist = 0, 0, 0.0
        covered = set()
        matched_nets = set()
        rows = []
        for num, dx, dy in tp:
            bx, by = t0x + dx, t0y + dy
            net = pinnet.get((ref, num))
            skip = (ref, num) in SKIP_NET_CHECK or (net or '').startswith('unconnected-')
            cand = sorted(((math.hypot(bx - q['kx'], by - q['ky']), q) for q in epads), key=lambda c: c[0])
            hit = None
            if cand and cand[0][0] <= 0.35:
                q = cand[0][1]
                covered.add(q['name'])
                dist = max(dist, cand[0][0])
                if skip or SIG2NET.get(q['sig']) == net:
                    hit = net
            rows.append((num, net, hit))
        for num, net, hit in rows:
            if hit is not None:
                matched += 1
                matched_nets.add(hit)
        for num, net, hit in rows:
            if hit is None and net and (ref, num) not in EXTRA_PADS_OK \
               and not (net or '').startswith('unconnected-') and net not in matched_nets:
                mism += 1
        uncovered = [q['name'] for q in epads if q['name'] not in covered]
        score = (mism + len(uncovered), -matched, dist)
        if best is None or score < best[0]:
            best = (score, rho, t0x, t0y, uncovered, dist)
    score, rho, px, py, uncovered, dist = best
    status = 'OK' if score[0] == 0 else 'FAIL'
    print(f"  {ref:5s} <- {elname:5s} rot={rho:3.0f} pos=({px:7.3f},{py:7.3f}) maxdev={dist:.3f} "
          f"score={score} {status}{' uncovered:' + str(uncovered) if uncovered else ''}")
    return px, py, rho, status == 'OK'

print('=== placements ===')
placements = {}
fails = []
for ref in COMPS:
    if ref in ('PS1', 'C13', 'J2', 'J110'):
        continue
    elname = EL_MAP.get(ref, ref)
    px, py, rho, ok = place_element(ref, elname)
    placements[ref] = (px, py, rho)
    if not ok:
        fails.append(ref)
# manual placements (KiCad coords)
placements['J110'] = (73.025, FY(95.25), 180.0)  # pad1 lands on /AC_N copper (P4), pad2 on /DC_MID (P3)
placements['PS1'] = (44.25, 22.0, 180.0)         # T2 slot; AC pins right, DC pins at x=1.75
placements['C13'] = (43.815, FY(48.26), 0.0)     # old C7 spot: +15V/GND pours on each pad
placements['J2'] = (102.362, FY(103.2891), 0.0)
print('manual: J110', placements['J110'], ' PS1', placements['PS1'], ' C13', placements['C13'], ' J2', placements['J2'])
if fails:
    print('!! ALIGNMENT FAILURES:', fails)

# ---------- copper: wires ----------
def wire_key(w):
    return W(w['x1'], w['y1'], w['x2'], w['y2'])

segments = []   # (x1,y1,x2,y2,width,layer,net)  KiCad space
for sname, s in eagle['signals'].items():
    if sname in SIG_DELETE:
        continue
    net = SIG2NET[sname]
    dels = set(WIRE_DELETE.get(sname, []))
    for w in s['wires']:
        if wire_key(w) in dels:
            continue
        if w['layer'] == 1:
            layer = 'F.Cu'
        elif w['layer'] == 16:
            layer = 'B.Cu'
        else:
            continue  # drop inner-layer leftovers
        segments.append((w['x1'], FY(w['y1']), w['x2'], FY(w['y2']), w['width'], layer, net))

vias = []       # (x,y,drill,size,net)
for sname, s in eagle['signals'].items():
    if sname in SIG_DELETE:
        continue
    net = SIG2NET[sname]
    for v in s['vias']:
        if (v['x'], v['y']) in VIA_DELETE.get(sname, []):
            continue
        size = v['diameter'] or 1.5
        vias.append((v['x'], FY(v['y']), v['drill'], size, net))

# ---------- new copper (KiCad coords) ----------
def seg(x1, y1, x2, y2, w, layer, net):
    segments.append((x1, y1, x2, y2, w, layer, net))
def via(x, y, net, drill=0.6, size=1.3):
    vias.append((x, y, drill, size, net))

NEW = [
 # SW_NODE: CPR1.1 to the Q2 collector feed
 ((39.37, FY(19.685)), (64.14, FY(19.685)), 2.54, 'B.Cu', '/SW_NODE'),
 # CPR1.2 net: P1 pad down and across to the N$22 junction
 ((41.275, FY(14.605)), (41.275, FY(12.0)), 2.54, 'B.Cu', 'Net-(CPR1-Pad2)'),
 ((41.275, FY(12.0)), (88.9, FY(12.0)), 2.54, 'B.Cu', 'Net-(CPR1-Pad2)'),
 ((88.9, FY(12.0)), (88.9, FY(15.24)), 2.54, 'B.Cu', 'Net-(CPR1-Pad2)'),
 # DC_MID: P2 pad along the bottom, L1 hop over the N$22 vertical, to ring P$1
 ((19.685, FY(14.605)), (19.685, FY(5.5)), 2.54, 'B.Cu', '/DC_MID'),
 ((19.685, FY(5.5)), (84.0, FY(5.5)), 2.54, 'B.Cu', '/DC_MID'),
 ((84.0, FY(5.5)), (84.0, FY(9.0)), 2.54, 'B.Cu', '/DC_MID'),
 ((84.0, FY(9.0)), (94.0, FY(9.0)), 2.54, 'F.Cu', '/DC_MID'),
 ((94.0, FY(9.0)), (101.6, FY(11.43)), 2.54, 'B.Cu', '/DC_MID'),
 # AC_L_FUSED to PS1.1 along the top edge (coords: KiCad space)
 ((44.25, 22.0), (40.5, 22.0), 0.5, 'F.Cu', '/AC_L_FUSED'),
 ((40.5, 22.0), (40.5, 0.75), 0.5, 'F.Cu', '/AC_L_FUSED'),
 ((40.5, 0.75), (95.25, 0.75), 0.5, 'F.Cu', '/AC_L_FUSED'),
 ((95.25, 0.75), (95.25, 3.81), 0.5, 'F.Cu', '/AC_L_FUSED'),
 # AC_N: PS1.2 to the neutral net (old T2 branch point at (34.29,4.445));
 # jog clears the IEC mounting hole d3.0 at (46.205,6.071)
 ((44.25, 14.2), (43.0, 14.2), 0.41, 'B.Cu', '/AC_N'),
 ((43.0, 14.2), (43.0, 4.445), 0.41, 'B.Cu', '/AC_N'),
 ((43.0, 4.445), (44.2, 3.5), 0.41, 'B.Cu', '/AC_N'),
 ((44.2, 3.5), (48.26, 3.5), 0.41, 'B.Cu', '/AC_N'),
 ((48.26, 3.5), (48.26, 4.445), 0.41, 'B.Cu', '/AC_N'),
 # GND: PS1.3 down into the logic pour; IC6.2 bridge to C9.2 (pour pocket)
 ((1.75, 29.4), (1.75, 33.0), 1.0, 'B.Cu', 'GND'),
 ((1.905, 50.8), (7.62, 50.8), 0.5, 'B.Cu', 'GND'),
 # +15V: PS1.4 up the left edge (jog around the PS1.3 pad); C10.+ / IC6.3 / driver pour
 ((1.75, 6.8), (1.75, 26.0), 0.8, 'F.Cu', '+15V'),
 ((1.75, 26.0), (3.9, 28.6), 0.8, 'F.Cu', '+15V'),
 ((3.9, 28.6), (3.9, 32.385), 0.8, 'F.Cu', '+15V'),
 ((3.9, 32.385), (4.57, 32.385), 0.8, 'F.Cu', '+15V'),
 # +5V: FB1.3 (VCC) thermal spoke into the pour body (above the NPTHs)
 ((5.08, 65.405), (5.08, 66.3), 0.5, 'F.Cu', '+5V'),
 ((5.08, 66.3), (12.0, 66.3), 0.5, 'F.Cu', '+5V'),
 ((4.57, 43.815), (4.57, 49.53), 0.8, 'F.Cu', '+15V'),
 ((3.81, 49.53), (4.57, 49.53), 0.8, 'F.Cu', '+15V'),
 ((4.57, 43.815), (4.57, 32.385), 0.8, 'F.Cu', '+15V'),
 ((4.57, 32.385), (36.5, 32.385), 0.8, 'F.Cu', '+15V'),
 ((36.5, 32.385), (36.5, 40.0), 0.8, 'F.Cu', '+15V'),
 ((36.5, 40.0), (38.1, 40.0), 0.8, 'F.Cu', '+15V'),
 # +5V: IC2.13 / IC2.10 (PRE/CLR now on +5V; were GND in the original)
 ((19.05, 34.925), (21.59, 34.925), 0.4064, 'F.Cu', '+5V'),
 ((29.21, 34.925), (29.21, 33.2), 0.4064, 'F.Cu', '+5V'),
 ((29.21, 33.2), (21.59, 33.2), 0.4064, 'F.Cu', '+5V'),
 ((21.59, 33.2), (21.59, 34.925), 0.4064, 'F.Cu', '+5V'),
 # PE: J1.3 down past PS1.2, along the top edge, B.Cu hop under the N$17 drop, to J2
 ((52.705, 11.071), (49.0, 16.0), 0.6, 'F.Cu', '/PE'),
 ((49.0, 16.0), (42.0, 16.0), 0.6, 'F.Cu', '/PE'),
 ((42.0, 16.0), (42.0, 1.85), 0.6, 'F.Cu', '/PE'),
 ((42.0, 1.85), (93.0, 1.85), 0.5, 'F.Cu', '/PE'),
 ((93.0, 1.85), (93.0, 2.0), 0.5, 'F.Cu', '/PE'),
 ((93.0, 2.0), (99.5, 2.0), 0.5, 'B.Cu', '/PE'),
 ((99.5, 2.0), (102.36, 2.0), 0.5, 'F.Cu', '/PE'),
 ((102.36, 2.0), (102.362, 2.756), 0.5, 'F.Cu', '/PE'),
 # SW_NODE: trimmed Q2 collector feed (bottom part deleted with the stubs)
 ((64.14, 86.36), (64.14, 72.385), 2.54, 'B.Cu', '/SW_NODE'),
 # fuse clip tangs (same net as their clip pad; no copper in the original)
 ((74.93, 3.81), (80.01, 3.81), 1.0, 'F.Cu', '/AC_L'),
 ((90.17, 3.81), (95.25, 3.81), 1.0, 'F.Cu', '/AC_L_FUSED'),
]
for (x1, y1), (x2, y2), w, layer, net in NEW:
    seg(x1, y1, x2, y2, w, layer, net)
via(84.0, FY(9.0), '/DC_MID')
via(94.0, FY(9.0), '/DC_MID')
via(93.0, 2.0, '/PE')
via(99.5, 2.0, '/PE')

# ---------- collision check: new wires vs everything ----------
def seg_seg_dist(a, b, c, d):
    def pt_seg(p, s, e):
        vx, vy = e[0] - s[0], e[1] - s[1]
        L2 = vx * vx + vy * vy
        if L2 == 0: return math.hypot(p[0] - s[0], p[1] - s[1])
        t = max(0, min(1, ((p[0] - s[0]) * vx + (p[1] - s[1]) * vy) / L2))
        return math.hypot(p[0] - s[0] - t * vx, p[1] - s[1] - t * vy)
    def ccw(A, B, C): return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])
    if ccw(a, c, d) != ccw(b, c, d) and ccw(a, b, c) != ccw(a, b, d):
        return 0.0
    return min(pt_seg(a, c, d), pt_seg(b, c, d), pt_seg(c, a, b), pt_seg(d, a, b))

print('=== new-wire collision check ===')
nnew = len(NEW)
collisions = 0
for i, ((x1, y1), (x2, y2), w, layer, net) in enumerate(NEW):
    base = len(segments) - nnew
    for j in range(base):
        ax1, ay1, ax2, ay2, aw, alayer, anet = segments[j]
        if alayer != layer or anet == net:
            continue
        d = seg_seg_dist((x1, y1), (x2, y2), (ax1, ay1), (ax2, ay2))
        if d < (w + aw) / 2 + 0.1:
            print(f"  COLLIDE {net} ({x1:.2f},{y1:.2f})-({x2:.2f},{y2:.2f}) vs {anet} ({ax1},{ay1})-({ax2},{ay2}) d={d:.2f}")
            collisions += 1
print(f'  {collisions} wire-wire collisions')

# pad collisions for new wires (both layers for THT pads)
pad_points = []  # (x,y,r,net,ref,num)
for ref, (px, py, rho) in placements.items():
    fn = COMPS[ref]['footprint']
    for p in fp_pads[fn]:
        if p['np']:
            continue
        dx, dy = rot_pt(p['x'], p['y'], rho)
        net = pinnet.get((ref, p['num']))
        pad_points.append((px + dx, py + dy, max(p['sx'], p['sy']) / 2, net, ref, p['num']))
npad_coll = 0
for (x1, y1), (x2, y2), w, layer, net in NEW:
    for (px, py, pr, pnet, ref, num) in pad_points:
        if pnet == net:
            continue
        d = seg_seg_dist((px, py), (px, py), (x1, y1), (x2, y2))
        if d < pr + w / 2 + 0.1:
            print(f"  PAD-COLLIDE {net} wire vs {ref}.{num} ({pnet}) at ({px:.2f},{py:.2f}) d={d:.2f}")
            npad_coll += 1
print(f'  {npad_coll} wire-pad collisions')

# ---------- zones ----------
ZONES = []
zone_map = [('+5V', 1, '+5V', 0.4, True), ('GND', 16, 'GND', 0.4, True),
            ('+15V', 1, '+15V', 0.4, True), ('POS', 16, '/DC_PLUS', 0.6096, False),
            ('NEG', 1, '/DC_MINUS', 0.6096, False), ('N$14', 16, '/SW_NODE', 0.6096, False)]
for sname, layer, net, clearance, thermals in zone_map:
    for p in eagle['signals'][sname]['polys']:
        assert p['layer'] == layer
        pts = [(x, FY(y)) for x, y, c in p['verts']]
        ZONES.append({'net': net, 'layer': 'F.Cu' if layer == 1 else 'B.Cu',
                      'pts': pts, 'clearance': clearance, 'thermals': thermals})

# ---------- emit .kicad_pcb ----------
U = lambda: str(uuidlib.uuid4())
out = []
A = out.append
A('(kicad_pcb (version 20240108) (generator "build_pcb.py")')
A('(general (thickness 1.6) (legacy_teardrops no))')
A('(paper "A4")')
A('''(layers
  (0 "F.Cu" signal)
  (31 "B.Cu" signal)
  (32 "B.Adhes" user "B.Adhesive")
  (33 "F.Adhes" user "F.Adhesive")
  (34 "B.Paste" user)
  (35 "F.Paste" user)
  (36 "B.SilkS" user "B.Silkscreen")
  (37 "F.SilkS" user "F.Silkscreen")
  (38 "B.Mask" user)
  (39 "F.Mask" user)
  (40 "Dwgs.User" user "User.Drawings")
  (41 "Cmts.User" user "User.Comments")
  (42 "Eco1.User" user "User.Eco1")
  (43 "Eco2.User" user "User.Eco2")
  (44 "Edge.Cuts" user)
  (45 "Margin" user)
  (46 "B.CrtYd" user "B.Courtyard")
  (47 "F.CrtYd" user "F.Courtyard")
  (48 "B.Fab" user)
  (49 "F.Fab" user)
  (50 "User.1" user)
  (51 "User.2" user)
  (52 "User.3" user)
  (53 "User.4" user)
  (54 "User.5" user)
  (55 "User.6" user)
  (56 "User.7" user)
  (58 "User.9" user))''')
A('(setup (pad_to_mask_clearance 0))')
A('(net 0 "")')
for n in net_names:
    A(f'(net {nid(n)} "{n}")')

# footprints
def emit_footprint(ref):
    c = COMPS[ref]
    fn = c['footprint']
    t = fp_trees[fn]
    px, py, rho = placements[ref]
    # KiCad's (at .. angle) rotates opposite to our rot_pt; negate.
    ang = (-rho) % 360
    lines = []
    lines.append(f'(footprint "oneTesla:{fn}" (layer "F.Cu") (uuid {U()})')
    lines.append(f'  (at {px:.4f} {py:.4f} {ang:g})')
    for node in t[1:]:
        if not isinstance(node, list):
            continue
        if node[0] == 'pad':
            num = str(node[1])
            net = pinnet.get((ref, num))
            node = [x for x in node if not (isinstance(x, list) and x and x[0] == 'net')]
            if net:
                node.append([Atom('net'), nid(net), net])
            lines.append('  ' + dump(node).replace('\n', ' '))
        elif node[0] == 'property':
            if node[1] == 'Reference':
                node[2] = ref
            elif node[1] == 'Value':
                node[2] = COMPS[ref]['value']
            lines.append('  ' + dump(node).replace('\n', ' '))
        else:
            lines.append('  ' + dump(node).replace('\n', ' '))
    lines.append(')')
    return '\n'.join(lines)

for ref in sorted(placements, key=lambda r: (r.rstrip('0123456789'), int('0' + ''.join(ch for ch in r if ch.isdigit()) or '0'))):
    if COMPS[ref]['dnp']:
        # Z1/Z2 DNP: still place (kit option, pads on the original board)
        pass
    A(emit_footprint(ref))

# ring terminals (original 2STANDOFFS pads): P$1 /DC_MID, P$2 CPR1.2-net
def ring(x_e, y_e, net, name):
    return (f'(footprint "oneTesla:Ring_D6_D3.81" (layer "F.Cu") (uuid {U()})\n'
            f'  (at {x_e:.4f} {FY(y_e):.4f} 0)\n'
            f'  (property "Reference" "{name}" (at 0 -4.5 0) (layer "F.SilkS") (uuid {U()})\n'
            f'    (effects (font (size 1.27 1.27) (thickness 0.19))))\n'
            f'  (pad "1" thru_hole circle (at 0 0) (size 6.0 6.0) (drill 3.81)\n'
            f'    (layers "*.Cu" "*.Mask") (net {nid(net)} "{net}") (uuid {U()})))')
A(ring(101.6, 11.43, '/DC_MID', 'JPRT1'))
A(ring(88.9, 3.81, 'Net-(CPR1-Pad2)', 'JPRT2'))

# mounting holes: 4 standoffs d4.0, 2 heatsink d5.5
def nth(x, y, d, name=''):
    return (f'(footprint "oneTesla:MountingHole_D{d}" (layer "F.Cu") (uuid {U()})\n'
            f'  (at {x:.4f} {y:.4f} 0)\n'
            f'  (pad "" np_thru_hole circle (at 0 0) (size {d} {d}) (drill {d}) (layers "*.Cu" "*.Mask") (uuid {U()})))')
for e in eagle['elements']:
    if e['name'] in ('U$12', 'U$14', 'U$15'):  # U$13 co-located with the J2 chassis pad
        A(nth(e['x'], FY(e['y']), 4.0))
for h in eagle['plain']['holes']:
    A(nth(h['x'], FY(h['y']), h['drill']))

# tracks
for (x1, y1, x2, y2, w, layer, net) in segments:
    A(f'(segment (start {x1:.4f} {y1:.4f}) (end {x2:.4f} {y2:.4f}) (width {w}) (layer "{layer}") (net {nid(net)}) (uuid {U()}))')
for (x, y, drill, size, net) in vias:
    A(f'(via (at {x:.4f} {y:.4f}) (size {size}) (drill {drill}) (layers "F.Cu" "B.Cu") (net {nid(net)}) (uuid {U()}))')

# zones
for z in ZONES:
    pts = ' '.join(f'(xy {x:.4f} {y:.4f})' for x, y in z['pts'])
    connect = '(connect_pads (clearance %.4f))' % z['clearance'] if z['thermals'] else \
              '(connect_pads yes (clearance %.4f))' % z['clearance']
    A(f'''(zone (net {nid(z['net'])}) (net_name "{z['net']}") (layer "{z['layer']}") (uuid {U()})
  (hatch edge 0.5)
  {connect}
  (min_thickness 0.25)
  (fill yes (thermal_gap 0.4) (thermal_bridge_width 0.7))
  (polygon (pts {pts})))''')

# outline
for (x1, y1, x2, y2) in [(0, 0, 106.045, 0), (106.045, 0, 106.045, 106.045),
                          (106.045, 106.045, 0, 106.045), (0, 106.045, 0, 0)]:
    A(f'(gr_line (start {x1} {y1}) (end {x2} {y2}) (layer "Edge.Cuts") (width 0.05) (uuid {U()}))')

# ---------- silkscreen: original texts + vector logos ----------
import xml.etree.ElementTree as ET
_brd = ET.parse(os.path.join(ROOT, 'misc', 'driver.brd')).getroot()

def el_transform(e):
    theta = float(e['rot'][1:]) if e['rot'] != 'R0' else 0.0
    return e['x'], e['y'], theta

def xf_pt(ex, ey, theta, px, py):
    dx, dy = rot_pt(px, py, theta)
    return ex + dx, ey + dy

SILK_TEXT_EDITS = {
    'Replace with 250V 10A fuse only': 'Replace with 250V 4A fuse only',  # kit parts list: 4A
}
def emit_text(txt, gx, gy, size, rot_deg_e, layer, ratio=8):
    txt = SILK_TEXT_EDITS.get(txt, txt)
    kx, ky = gx, FY(gy)
    ang = (-rot_deg_e) % 360
    th = max(0.1, size * (ratio or 8) / 100.0)
    A(f'(gr_text "{txt}" (at {kx:.4f} {ky:.4f} {ang:g}) (layer "{layer}") (uuid {U()})'
      f' (effects (font (size {size} {size}) (thickness {th:.3f}))))')

# plain texts (skip component designators; footprints carry refs)
SKIP_TEXTS = {'FB1', 'T1', 'T2', 'D4', 'Q1', 'Q2', 'CPRI', 'JPRI', 'T3', 'P1', 'P2'}
for t in eagle['plain']['texts']:
    if t['text'] in SKIP_TEXTS:
        continue
    layer = {21: 'F.SilkS', 25: 'F.SilkS', 51: 'F.Fab'}.get(t['layer'])
    if not layer:
        continue
    rot_e = float((t.get('rot') or 'R0')[1:])
    emit_text(t['text'], t['x'], t['y'], t['size'], rot_e, layer, int(t.get('ratio') or 8))

# logo packages: rectangles + texts
for lib in _brd.find('drawing/board/libraries'):
    ps = lib.find('packages')
    if ps is None:
        continue
    for pkg in ps:
        pname = pkg.get('name')
        if pname not in ('LOGO', 'TSLOGO', 'WARNING'):
            continue
        elname = {'LOGO': 'U$1', 'TSLOGO': 'U$4', 'WARNING': 'U$3'}[pname]
        ex, ey, theta = el_transform(elements[elname])
        for rect in pkg.findall('rectangle'):
            if rect.get('layer') != '21':
                continue
            x1, y1 = xf_pt(ex, ey, theta, float(rect.get('x1')), float(rect.get('y1')))
            x2, y2 = xf_pt(ex, ey, theta, float(rect.get('x2')), float(rect.get('y2')))
            A(f'(gr_rect (start {x1:.4f} {FY(y1):.4f}) (end {x2:.4f} {FY(y2):.4f})'
              f' (layer "F.SilkS") (width 0) (fill yes) (uuid {U()}))')
        for tx in pkg.findall('text'):
            if tx.get('layer') != '21' or (tx.text or '').endswith('.bmp'):
                continue
            gx, gy = xf_pt(ex, ey, theta, float(tx.get('x')), float(tx.get('y')))
            trot = float((tx.get('rot') or 'R0')[1:]) + theta
            emit_text(tx.text, gx, gy, float(tx.get('size')), trot, 'F.SilkS', int(tx.get('ratio') or 8))

# silk: standoff circles
for e in eagle['elements']:
    if e['name'] in ('U$12', 'U$13', 'U$14', 'U$15'):
        A(f'(gr_circle (center {e["x"]:.4f} {FY(e["y"]):.4f}) (end {e["x"]+3.175:.4f} {FY(e["y"]):.4f}) (layer "F.SilkS") (width 0.15) (fill no) (uuid {U()}))')
# silk: J110 marks (plain L21 wires)
for w in eagle['plain']['wires']:
    if w['layer'] == 21:
        A(f'(gr_line (start {w["x1"]:.4f} {FY(w["y1"]):.4f}) (end {w["x2"]:.4f} {FY(w["y2"]):.4f}) (layer "F.SilkS") (width {w["width"]}) (uuid {U()}))')
A(')')

with open(os.path.join(ROOT, 'oneTesla.kicad_pcb'), 'w') as f:
    f.write('\n'.join(out) + '\n')
print('=== wrote oneTesla.kicad_pcb ===')
print(f'{len(placements)} footprints, {len(segments)} segments, {len(vias)} vias, {len(ZONES)} zones')
