"""Refill all zones in oneTesla.kicad_pcb and save (runs under KiCad's python)."""
import sys
import pcbnew

path = sys.argv[1] if len(sys.argv) > 1 else 'oneTesla.kicad_pcb'
board = pcbnew.LoadBoard(path)
filler = pcbnew.ZONE_FILLER(board)
filler.Fill(board.Zones())
board.Save(path)
print('zones refilled and saved:', path)
