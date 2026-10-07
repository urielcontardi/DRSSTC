"""Extract components, nets and footprint pad geometry into output/pcb-data.json."""
import json, re, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from sexpr import parse, children, child, prop

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def fnum(x):
    s = str(x)
    return s

# --- schematic: components ---
tree = parse(open(os.path.join(ROOT, 'oneTesla.kicad_sch')).read())
comps = {}
for sym in children(tree, 'symbol'):
    if not child(sym, 'lib_id'):
        continue
    r = prop(sym, 'Reference')
    ref = r[2] if r else '?'
    if ref.startswith('#'):
        continue
    if ref in comps:  # multi-unit: keep first
        continue
    v = prop(sym, 'Value'); f = prop(sym, 'Footprint')
    dnp_node = child(sym, 'dnp')
    dnp = dnp_node is not None and len(dnp_node) > 1 and str(dnp_node[1]) == 'yes'
    fps_ = prop(sym, 'Footprint_Status'); an = prop(sym, 'Assembly_Notes')
    comps[ref] = {
        'value': v[2] if v else '',
        'footprint': (f[2] if f else '').replace('oneTesla:', ''),
        'dnp': dnp,
        'status': fps_[2] if fps_ else '',
        'notes': an[2] if an else '',
    }

# --- netlist: net -> [(ref, pin)] ---
net_tree = parse(open(os.path.join(ROOT, 'output/oneTesla.net')).read())
nets = {}
for n in children(net_tree, 'nets')[0] if children(net_tree, 'nets') else []:
    pass
# KiCad legacy netlist: (export (components ...) (nets (net (code)(name)(node ...))...))
def find(v, k):
    if isinstance(v, list):
        if v and v[0] == k:
            return v
        for x in v:
            r = find(x, k)
            if r is not None:
                return r
    return None
nets_node = find(net_tree, 'nets')
for net in children(nets_node, 'net'):
    name = child(net, 'name')[1]
    nodes = []
    for node in children(net, 'node'):
        ref = child(node, 'ref')[1]
        pin = child(node, 'pin')[1]
        nodes.append([ref, str(pin)])
    nets[name] = nodes

# --- footprints: pad geometry ---
fp_dir = os.path.join(ROOT, 'library', 'oneTesla.pretty')
fps = {}
need = {c['footprint'] for c in comps.values()}
for fn in os.listdir(fp_dir):
    if not fn.endswith('.kicad_mod'):
        continue
    name = fn[:-10]
    if name not in need:
        continue
    ft = parse(open(os.path.join(fp_dir, fn)).read())
    pads = []
    for p in children(ft, 'pad'):
        num = str(p[1])
        ptype = p[2]  # thru_hole / smd / np_thru_hole
        shape = p[3]
        at = child(p, 'at')
        size = child(p, 'size')
        drill = child(p, 'drill')
        pads.append({
            'num': num, 'type': str(ptype), 'shape': str(shape),
            'x': float(at[1]), 'y': float(at[2]),
            'rot': float(at[3]) if len(at) > 3 else 0.0,
            'sx': float(size[1]), 'sy': float(size[2]),
            'drill': float(drill[1]) if drill and len(drill) > 1 else 0.0,
        })
    fps[name] = {'pads': pads}

out = {'components': comps, 'nets': nets, 'footprints': fps}
with open(os.path.join(ROOT, 'output', 'pcb-data.json'), 'w') as f:
    json.dump(out, f, indent=1)

# refresh components.csv for the current schematic
import csv
def ckey(r):
    import re
    m = re.match(r'([A-Za-z]+)(\d+)', r)
    return (m.group(1), int(m.group(2))) if m else (r, 0)
with open(os.path.join(ROOT, 'output', 'components.csv'), 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['Reference', 'Value', 'Footprint', 'DNP', 'Footprint_Status', 'Assembly_Notes'])
    for ref in sorted(comps, key=ckey):
        c = comps[ref]
        w.writerow([ref, c['value'], 'oneTesla:' + c['footprint'], c['dnp'], c['status'], c['notes']])
missing_fp = [r for r, c in comps.items() if c['footprint'] not in fps]
print(len(comps), 'components,', len(nets), 'nets,', len(fps), 'footprints')
print('missing footprints:', missing_fp)
# sanity: every net node ref exists
bad = [(n, r) for n, nodes in nets.items() for r, p in nodes if r not in comps]
print('unknown refs in nets:', bad)
