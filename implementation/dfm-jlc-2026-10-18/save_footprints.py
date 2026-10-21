import pcbnew as p,json
from pathlib import Path
b=p.LoadBoard('oneTesla.kicad_pcb');d=json.loads(Path('implementation/dfm-jlc-2026-10-18/drc-pass4.json').read_text());ids={v['items'][0]['uuid'] for v in d['violations'] if v['type']=='lib_footprint_mismatch'};mapping=json.loads(Path('implementation/dfm-jlc-2026-10-18/footprint-variants.json').read_text())
for f in b.GetFootprints():
 if f.m_Uuid.AsString() not in ids:continue
 old=str(f.GetFPID().GetLibItemName());name=old if '_DFM_' in old else old+'_DFM_'+f.GetReference();f.SetFPID(p.LIB_ID('oneTesla',name));c=p.FOOTPRINT(f)
 p.PCB_IO_KICAD_SEXPR().FootprintSave(str(Path('library/oneTesla.pretty').resolve()),c)
 mapping[f.GetReference()]={'old':mapping.get(f.GetReference(),{}).get('old','oneTesla:'+old),'new':'oneTesla:'+name}
p.SaveBoard('oneTesla.kicad_pcb',b)
Path('implementation/dfm-jlc-2026-10-18/footprint-variants.json').write_text(json.dumps(mapping,indent=2));print('Saved',len(mapping),'layout-specific silk variants')
