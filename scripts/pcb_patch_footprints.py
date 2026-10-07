"""Align local footprints to the original driver.brd pad geometry (réplica fiel).

Edits library/oneTesla.pretty/*.kicad_mod in place, idempotently.
Every change is a pad position/drill edit so pads land exactly on the
original board's copper; silk/courtyard cosmetics are left as-is.
Coordinates here are in KiCad convention (y-down), i.e. Eagle (x,-y).
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from sexpr import parse, children, child, dump, Atom

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FP = os.path.join(ROOT, 'library', 'oneTesla.pretty')

# name -> list of pads: (num, x, y, drill, size_x, size_y, shape, np)
PATCH = {
 'R_Axial_Power_L25.0mm_W6.4mm_P30.48mm': [
    ('1', -11.43, 0, 1.3, 2.4, 2.4, 'circle', False), ('2', 11.43, 0, 1.3, 2.4, 2.4, 'circle', False)],
 'R_Axial_DIN0309_L9.0mm_D3.2mm_P12.70mm_Horizontal': [
    ('1', -5.08, 0, 0.8128, 1.6, 1.6, 'circle', False), ('2', 5.08, 0, 0.8128, 1.6, 1.6, 'circle', False)],
 'CP_Radial_D8.0mm_P3.50mm': [
    ('1', -1.27, 0, 0.8128, 1.6, 1.6, 'circle', False), ('2', 1.27, 0, 0.8128, 1.6, 1.6, 'circle', False)],
 'CP_Radial_D12.5mm_P5.00mm': [
    ('1', -1.778, 0, 0.8128, 1.8, 1.8, 'circle', False), ('2', 1.778, 0, 0.8128, 1.8, 1.8, 'circle', False)],
 'D_DO-201AD_P15.24mm_Horizontal': [
    ('1', -7.366, 0, 1.1, 3.0, 3.0, 'circle', False), ('2', 7.366, 0, 1.1, 3.0, 3.0, 'circle', False)],
 'CDE_940C30S68K_F_CONFIRMAR': [
    ('1', -29.21, 0, 1.4, 4.0, 4.0, 'circle', False), ('2', 29.21, 0, 1.4, 4.0, 4.0, 'circle', False)],
 'CP_Radial_D30.0mm_P10.00mm_SnapIn': [
    ('1', -5.08, 0, 2.0, 4.0, 4.0, 'circle', False), ('2', 5.08, 0, 2.0, 4.0, 4.0, 'circle', False)],
 'CT_1_300_P12.70mm_CONFIRMAR': [
    ('1', 0, -6.35, 1.27, 2.5, 2.5, 'circle', False), ('2', 0, 6.35, 1.27, 2.5, 2.5, 'circle', False)],
 # GDT: pads at the original P0584 positions (Eagle y flipped); nets verified
 # 1=E1 AA, 2=E10 AB, 3=E3 GATE_H, 4=E4 SW_NODE, 5=E7 GATE_L, 6=E8 DC_MINUS
 'GDT_6Pin_CONFIRMAR': [
    ('1', -9.017, -4.572, 1.016, 2.2, 2.2, 'rect', False), ('2', -9.017, 4.445, 1.016, 2.2, 2.2, 'circle', False),
    ('3', 3.683, -4.445, 1.016, 2.2, 2.2, 'circle', False),  ('4', 8.763, -4.445, 1.016, 2.2, 2.2, 'circle', False),
    ('5', 8.763, 4.445, 1.016, 2.2, 2.2, 'circle', False),   ('6', 3.683, 4.445, 1.016, 2.2, 2.2, 'circle', False)],
 # HFBR: pads 1-4 at original IFD95 row (1.905 pitch), RL pad4 best-guess continuation;
 # center hole d3.2 and retention HOLES (no copper, as in the original) d1.651.
 'HFBR-2521ETZ': [
    ('3', -1.905, -5.08, 0.8, 1.5, 1.5, 'rect', False), ('1', 0.0, -5.08, 0.8, 1.5, 1.5, 'circle', False),
    ('2', 1.905, -5.08, 0.8, 1.5, 1.5, 'circle', False), ('4', 3.81, -5.08, 0.8, 1.5, 1.5, 'circle', False),
    ('', -2.54, -7.62, 1.651, 1.651, 1.651, 'circle', True), ('', 2.54, -7.62, 1.651, 1.651, 1.651, 'circle', True),
    ('', 0.0, 0.0, 3.2, 3.2, 3.2, 'circle', True)],
 # DIP sockets: original pads are standard (~1.6mm), not 2.4mm long pads
 'DIP-14_W7.62mm_Socket_LongPads': [
    ('1', 0.0, 0.0, 0.8128, 1.6, 1.6, 'rect', False), ('2', 0.0, 2.54, 0.8128, 1.6, 1.6, 'circle', False),
    ('3', 0.0, 5.08, 0.8128, 1.6, 1.6, 'circle', False), ('4', 0.0, 7.62, 0.8128, 1.6, 1.6, 'circle', False),
    ('5', 0.0, 10.16, 0.8128, 1.6, 1.6, 'circle', False), ('6', 0.0, 12.7, 0.8128, 1.6, 1.6, 'circle', False),
    ('7', 0.0, 15.24, 0.8128, 1.6, 1.6, 'circle', False), ('8', 7.62, 15.24, 0.8128, 1.6, 1.6, 'circle', False),
    ('9', 7.62, 12.7, 0.8128, 1.6, 1.6, 'circle', False), ('10', 7.62, 10.16, 0.8128, 1.6, 1.6, 'circle', False),
    ('11', 7.62, 7.62, 0.8128, 1.6, 1.6, 'circle', False), ('12', 7.62, 5.08, 0.8128, 1.6, 1.6, 'circle', False),
    ('13', 7.62, 2.54, 0.8128, 1.6, 1.6, 'circle', False), ('14', 7.62, 0.0, 0.8128, 1.6, 1.6, 'circle', False)],
 'DIP-8_W7.62mm_Socket_LongPads': [
    ('1', 0.0, 0.0, 0.8128, 1.6, 1.6, 'rect', False), ('2', 0.0, 2.54, 0.8128, 1.6, 1.6, 'circle', False),
    ('3', 0.0, 5.08, 0.8128, 1.6, 1.6, 'circle', False), ('4', 0.0, 7.62, 0.8128, 1.6, 1.6, 'circle', False),
    ('5', 7.62, 7.62, 0.8128, 1.6, 1.6, 'circle', False), ('6', 7.62, 5.08, 0.8128, 1.6, 1.6, 'circle', False),
    ('7', 7.62, 2.54, 0.8128, 1.6, 1.6, 'circle', False), ('8', 7.62, 0.0, 0.8128, 1.6, 1.6, 'circle', False)],
 # IEC C6: H/N/G row + mounting holes, original IEC320/C6 geometry (y flipped)
 'IEC_C6_CONFIRMAR': [
    ('1', -7.0, 14.5, 1.5, 3.0, 3.0, 'rect', False), ('2', 7.0, 14.5, 1.5, 3.0, 3.0, 'circle', False),
    ('3', 0.0, 14.5, 1.5, 3.0, 3.0, 'circle', False),
    ('', -6.5, 9.5, 3.0, 3.0, 3.0, 'circle', True), ('', 6.5, 9.5, 3.0, 3.0, 3.0, 'circle', True)],
 # Primary terminal: original 12AWG single octagon pad
 'Primary_Terminal_M6_CONFIRMAR': [
    ('1', 0.0, 0.0, 2.2, 4.0, 4.0, 'circle', False)],
 'J110_WireLink_P10.16mm': [
    ('1', -5.08, 0.0, 2.2, 4.0, 4.0, 'circle', False), ('2', 5.08, 0.0, 2.2, 4.0, 4.0, 'circle', False)],
 # Fuse clips: original FUSE1 inline 4 pads; pad2 lands on the /AC_L_FUSED side (x<0)
 'Fuseholder_Clip-5x20mm_Littelfuse_111_Inline_P20.00x5.00mm_D1.05mm_Horizontal': [
    ('2', -10.16, 0.0, 1.1938, 2.5, 2.5, 'circle', False), ('2', -5.08, 0.0, 1.1938, 2.5, 2.5, 'circle', False),
    ('1', 5.08, 0.0, 1.1938, 2.5, 2.5, 'circle', False), ('1', 10.16, 0.0, 1.1938, 2.5, 2.5, 'rect', False)],
 # TO-92: original triangle arrangement (y flipped), not inline
 'TO-92_Inline': [
    ('1', -1.27, 0.0, 0.8128, 1.6, 1.6, 'rect', False), ('2', 0.0, -1.905, 0.8128, 1.6, 1.6, 'circle', False),
    ('3', 1.27, 0.0, 0.8128, 1.6, 1.6, 'circle', False)],
 # TO-3P: drop the NPTH tab hole (heatsink holes d5.5 live at board level, as in the original)
 'TO-3P-3_Horizontal_TabDown': [
    ('1', 0.0, 0.0, 1.4986, 2.5, 4.5, 'rect', False), ('2', 5.45, 0.0, 1.4986, 2.5, 4.5, 'circle', False),
    ('3', 10.9, 0.0, 1.4986, 2.5, 4.5, 'circle', False)],
 'Chassis_PE_M3': [
    ('1', 0.0, 0.0, 3.2, 5.1, 5.1, 'circle', False)],
 # KBU: original GBU4S pin order is +, AC1(/AC_N), AC2(/AC_L_FUSED), - along +x;
 # swap pads 2/3 vs the generic KiCad KBU order so nets land on the right copper
 'Diode_Bridge_Vishay_KBU': [
    ('1', 0.0, 0.0, 1.4986, 2.8, 2.8, 'rect', False), ('3', 5.08, 0.0, 1.4986, 2.8, 2.8, 'circle', False),
    ('2', 10.16, 0.0, 1.4986, 2.8, 2.8, 'circle', False), ('4', 15.24, 0.0, 1.4986, 2.8, 2.8, 'circle', False)],
}

def pad_nodes(tree):
    return children(tree, 'pad')

def set_prop_list(node, key, values):
    n = child(node, key)
    if n is None:
        node.append([key] + values)
        return
    del n[1:]
    n.extend(values)

def patch_file(path, pads):
    tree = parse(open(path).read())
    nodes = pad_nodes(tree)
    # wipe existing pads, append new ones (keeps silk/fab/courtyard)
    for n in nodes:
        tree.remove(n)
    for num, x, y, drill, sx, sy, shape, npth in pads:
        node = [Atom('pad'), num, Atom('np_thru_hole' if npth else 'thru_hole'), Atom(shape),
                [Atom('at'), round(x, 4), round(y, 4)], [Atom('size'), sx, sy],
                [Atom('drill'), drill], [Atom('layers'), '*.Cu', '*.Mask']]
        if not npth:
            node.append([Atom('remove_unused_layers'), Atom('no')])
        tree.append(node)
    with open(path, 'w') as f:
        f.write(dump(tree) + '\n')

def main():
    for name, pads in PATCH.items():
        path = os.path.join(FP, name + '.kicad_mod')
        patch_file(path, pads)
        print('patched', name, f'({len(pads)} pads)')

if __name__ == '__main__':
    main()
