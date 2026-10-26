"""Reproducible preliminary coil calculations; stdlib only, no PCB changes."""
from pathlib import Path
import csv,json,math

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/design'
p=json.loads((OUT/'resonator-inputs.json').read_text())
s,t,b,c=p['secondary'],p['topload'],p['primary'],p['constants']

def frequency(l_h,c_f):return 1/(2*math.pi*math.sqrt(l_h*c_f))
def primary(turns,leads=True):
    first_radius=(b['inner_clear_diameter_mm']+b['finished_wire_diameter_assumed_mm'])/2
    radius=(first_radius+(turns-1)*b['radial_pitch_mm']/2)/25.4
    width=((turns-1)*b['radial_pitch_mm']+b['finished_wire_diameter_assumed_mm'])/25.4
    coil_uh=radius**2*turns**2/(8*radius+11*width)
    total_uh=coil_uh+(b['lead_inductance_assumed_uh'] if leads else 0)
    return dict(turns=turns,coil_uh=coil_uh,total_uh=total_uh,
                frequency_khz=frequency(total_uh*1e-6,b['capacitor_nf']*1e-9)/1000)

n=s['turns'];height=n*s['winding_pitch_mm']
# Centerline diameter includes one finished wire diameter.
diameter=s['tube_outer_diameter_mm']+s['finished_wire_diameter_assumed_mm']
r=diameter/2
ls_uh=(r/25.4)**2*n*n/(9*r/25.4+10*height/25.4)
hm,rm=height/1000,r/1000
# Empirical fit cited by Skeldon et al. (2000); dimensions in meters.
cs_pf=11.26*hm+16*rm+76.4*rm**1.5/math.sqrt(hm)
# Bert Pool toroid fit, as reproduced by Denicolai; dimensions in inches.
d1=t['outer_diameter_proposed_mm']/25.4;d2=t['minor_diameter_proposed_mm']/25.4
ct_pf=1.4*(1.2781-d2/d1)*math.sqrt(math.pi*d2*(d1-d2))
total_pf=cs_pf+ct_pf+t['extra_capacitance_assumed_pf']
fs=frequency(ls_uh*1e-6,total_pf*1e-12)
target=fs*b['cold_frequency_ratio_assumed']
lp_target_uh=1/((2*math.pi*target)**2*b['capacitor_nf']*1e-9)*1e6
low,high=3.0,12.0
for _ in range(70):
    mid=(low+high)/2
    if primary(mid)['total_uh']<lp_target_uh:low=mid
    else:high=mid
ntarget=(low+high)/2
wire_m=n*math.hypot(math.pi*diameter/1000,s['winding_pitch_mm']/1000)
area=math.pi*s['copper_diameter_mm']**2/4
rdc=c['copper_resistivity_ohm_mm2_per_m_at_20C']*wire_m/area
mass=wire_m*area*c['copper_density_g_per_cm3']
physical=b['physical_turns']
primary_length_m=sum(2*math.pi*((b['inner_clear_diameter_mm']+b['finished_wire_diameter_assumed_mm'])/2+j*b['radial_pitch_mm'])/1000 for j in range(physical))

def mutual_sheet(np,gap_mm,steps=512):
    """Neumann integral: concentric primary rings and uniform secondary sheet.

    Quasi-static geometry estimate; ignores helical leads, dielectric and
    the nonuniform resonant current distribution. Not a field simulation.
    """
    mu0=4*math.pi*1e-7;rs=r/1000;length=height/1000;gap=gap_mm/1000;result=0
    for j in range(np):
        rp=((b['inner_clear_diameter_mm']+b['finished_wire_diameter_assumed_mm'])/2+j*b['radial_pitch_mm'])/1000
        integral=0;dx=2*math.pi/steps
        for i in range(steps+1):
            phi=i*dx;cos=math.cos(phi)
            q=math.sqrt(rp*rp+rs*rs-2*rp*rs*cos)
            value=cos*(math.asinh((gap+length)/q)-math.asinh(gap/q))
            integral+=(1 if i in (0,steps) else 4 if i%2 else 2)*value
        result+=mu0*rp*rs*n/(2*length)*integral*dx/3
    return result

coupling=[]
for gap in (0,10,20,30):
    mutual=mutual_sheet(7,gap)
    k=mutual/math.sqrt(primary(7)['total_uh']*1e-6*ls_uh*1e-6)
    coupling.append(dict(gap_from_primary_plane_to_secondary_winding_start_mm=gap,mutual_uh=mutual*1e6,k_estimate=k))

rows=[primary(n) for n in (5,6,6.5,7,7.5,8)]
sensitivity=[]
for extra in (0,1,2,3):
    cap=cs_pf+ct_pf+extra
    f=frequency(ls_uh*1e-6,cap*1e-12)
    sensitivity.append(dict(extra_pf=extra,total_pf=cap,secondary_khz=f/1000,primary_target_khz=.9*f/1000))
result=dict(status=p['status'],source_capacitor='CPR1, 68n 3kV in active schematic',
 secondary=dict(turns=n,winding_height_mm=height,centerline_diameter_mm=diameter,
 inductance_mh=ls_uh/1000,self_capacitance_pf=cs_pf,wire_length_m=wire_m,
 wire_length_with_10_percent_margin_m=wire_m*1.1,dc_resistance_ohm_at_20C=rdc,copper_mass_g=mass),
 topload=dict(capacitance_pf=ct_pf,total_lumped_capacitance_pf=total_pf),
 tuning=dict(secondary_khz=fs/1000,primary_target_khz=target/1000,
 target_tank_inductance_uh=lp_target_uh,target_fractional_turns_approx=ntarget,
 target_surge_impedance_ohm=math.sqrt(lp_target_uh*1e-6/(b['capacitor_nf']*1e-9))),
 primary=dict(physical_turns=physical,outer_envelope_diameter_mm=b['inner_clear_diameter_mm']+2*b['finished_wire_diameter_assumed_mm']+2*(physical-1)*b['radial_pitch_mm'],
 wire_length_m=primary_length_m,turns_table=rows),
 coupling_geometry_estimates=coupling,capacitance_sensitivity=sensitivity,
 limitations=['actual wire finished diameter unknown','topload is proposed, not measured',
 'lumped capacitances only; mutual electrostatic shielding not solved',
 'primary leads assumed, not measured','current, pulse width, losses, protection and spark length not specified',
 'no high-power commissioning authorization from these calculations'])
(OUT/'resonator-results.json').write_text(json.dumps(result,indent=2)+'\n')
for filename,table in [('primary-taps.csv',rows),('capacitance-sensitivity.csv',sensitivity)]:
    with (OUT/filename).open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(table[0]));writer.writeheader();writer.writerows(table)
assert abs(frequency(lp_target_uh*1e-6,68e-9)-target)<1e-6
assert all(rows[i]['frequency_khz']>rows[i+1]['frequency_khz'] for i in range(len(rows)-1))
assert all(0<row['k_estimate']<1 for row in coupling)
print(json.dumps(result,indent=2))
