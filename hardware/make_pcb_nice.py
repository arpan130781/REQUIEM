import uuid

def make_uuid(): return str(uuid.uuid4())

out = []
out.append('(kicad_pcb (version 20230121) (generator pcbnew)')
out.append('  (general (thickness 1.6))')
out.append('  (paper "A4")')
out.append('  (title_block (title "Defence AI-ANC System PCB") (rev "v1.0") (company "Defence AI Systems"))')

# Layers
out.append('''
  (layers
    (0 "F.Cu" signal)
    (1 "In1.Cu" power)
    (2 "In2.Cu" power)
    (31 "B.Cu" signal)
    (36 "B.SilkS" user)
    (37 "F.SilkS" user)
    (38 "B.Mask" user)
    (39 "F.Mask" user)
    (44 "Edge.Cuts" user)
  )
''')

# Board Outline
out.append('  (gr_rect (start 0 0) (end 160 100) (layer "Edge.Cuts") (stroke (width 0.1) (type solid)) (fill none))')

# Mounting holes
for x, y in [(4, 4), (156, 4), (4, 96), (156, 96)]:
    out.append(f'''
  (footprint "MountingHole:MountingHole_3.2mm_M3" (layer "F.Cu") (at {x} {y})
    (pad "1" np_thru_hole circle (at 0 0) (size 3.2 3.2) (drill 3.2) (layers "*.Cu" "*.Mask"))
  )''')

# Function to place ICs
def place_ic(ref, pkg, val, x, y, rot=0):
    uid = make_uuid()
    out.append(f'''
  (footprint "{pkg}" (layer "F.Cu") (at {x} {y} {rot}) (attr smd)
    (fp_text reference "{ref}" (at 0 -1.5) (layer "F.SilkS") (effects (font (size 1 1) (thickness 0.15))))
    (fp_text value "{val}" (at 0 1.5) (layer "F.Fab") (effects (font (size 1 1) (thickness 0.15))))
    (fp_rect (start -3 -3) (end 3 3) (layer "F.SilkS") (stroke (width 0.15) (type solid)) (fill none))
  )''')

# MCU CORE
out.append('  (gr_rect (start 50 10) (end 110 50) (layer "F.SilkS") (stroke (width 0.1) (type dash)) (fill none))')
out.append('  (gr_text "MCU CORE" (at 80 15) (layer "F.SilkS") (effects (font (size 2 2) (thickness 0.3))))')
place_ic("U1", "Package_QFP:LQFP-144_20x20mm_P0.5mm", "STM32H755ZIT6", 80, 35)

# AI NPU
out.append('  (gr_rect (start 110 10) (end 150 50) (layer "F.SilkS") (stroke (width 0.1) (type dash)) (fill none))')
out.append('  (gr_text "AI NPU" (at 130 15) (layer "F.SilkS") (effects (font (size 2 2) (thickness 0.3))))')
place_ic("U2", "Package_BGA:BGA-144_10x10mm_P0.8mm", "Kendryte K210", 130, 30)
place_ic("U13", "Package_SO:SOIC-8_3.9x4.9mm_P1.27mm", "W25Q128", 140, 42)
place_ic("U14", "Package_SO:TSOP-II-54_10.16x22.22mm_P0.8mm", "IS42S32200L", 120, 42)

# AUDIO FRONT-END
out.append('  (gr_rect (start 10 10) (end 50 50) (layer "F.SilkS") (stroke (width 0.1) (type dash)) (fill none))')
out.append('  (gr_text "AUDIO INPUT" (at 30 15) (layer "F.SilkS") (effects (font (size 2 2) (thickness 0.3))))')
place_ic("MK1", "Sensor_Audio:Microphone_MEMS_4x3mm", "ICS-40300", 20, 25)
place_ic("MK2", "Sensor_Audio:Microphone_MEMS_4x3mm", "ICS-40300", 40, 25)
place_ic("U4", "Package_SO:SOIC-8_3.9x4.9mm_P1.27mm", "INA217", 30, 32)
place_ic("U18", "Package_SO:SOIC-8_3.9x4.9mm_P1.27mm", "MAX7401", 30, 40)
place_ic("U5", "Package_QFP:TQFP-64_10x10mm_P0.5mm", "ADS1274", 30, 48)

# OUTPUT STAGE
out.append('  (gr_rect (start 110 50) (end 150 85) (layer "F.SilkS") (stroke (width 0.1) (type dash)) (fill none))')
out.append('  (gr_text "AUDIO OUT" (at 130 55) (layer "F.SilkS") (effects (font (size 2 2) (thickness 0.3))))')
place_ic("U3", "Package_SO:SSOP-28_5.3x10.2mm_P0.65mm", "CS4270", 120, 65)
place_ic("U10", "Package_SO:SSOP-28_5.3x10.2mm_P0.65mm", "PCM1794A", 120, 75)
place_ic("U9", "Package_DFN_QFN:QFN-56-1EP_8x8mm_P0.5mm_EP6.1x6.1mm", "TPA3255", 140, 70)

# POWER
out.append('  (gr_rect (start 10 50) (end 70 85) (layer "F.SilkS") (stroke (width 0.1) (type dash)) (fill none))')
out.append('  (gr_text "POWER" (at 40 55) (layer "F.SilkS") (effects (font (size 2 2) (thickness 0.3))))')
place_ic("U6", "Package_DFN_QFN:QFN-48-1EP_7x7mm_P0.5mm_EP5.15x5.15mm", "TPS65217", 30, 70)
place_ic("U7", "Package_TO_SOT_SMD:SOT-223-3_TabPin2", "TLV1117-33", 50, 70)
place_ic("U8", "Package_TO_SOT_SMD:SOT-223-3_TabPin2", "TLV1117-18", 60, 70)
place_ic("J4", "Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical", "PWR_IN", 20, 78)

# COMMS & SENSORS
out.append('  (gr_rect (start 70 50) (end 110 85) (layer "F.SilkS") (stroke (width 0.1) (type dash)) (fill none))')
out.append('  (gr_text "COMMS / SENSORS" (at 90 55) (layer "F.SilkS") (effects (font (size 1.5 1.5) (thickness 0.2))))')
place_ic("U11", "Package_SO:SOIC-8_3.9x4.9mm_P1.27mm", "SP3485", 80, 65)
place_ic("U12", "Package_SO:SOIC-8_3.9x4.9mm_P1.27mm", "TCAN1044", 95, 65)
place_ic("U15", "Package_LGA:LGA-14_2.5x3mm_P0.5mm", "ICM-42688", 80, 75)
place_ic("U16", "Package_LGA:LGA-10_2x2mm_P0.5mm", "BMP388", 95, 75)

# Labels
out.append('  (gr_text "DEFENCE AI-ANC SYSTEM v1.0" (at 80 92) (layer "F.SilkS") (effects (font (size 2.5 2.5) (thickness 0.5) (bold yes))))')
out.append('  (gr_text "MIL-STD-810H | IP67 | -40C to +85C | ITAR CONTROLLED" (at 80 95) (layer "F.SilkS") (effects (font (size 1.2 1.2) (thickness 0.2))))')

# Zones
out.append('''
  (zone (net 0) (net_name "") (layer "In1.Cu") (hatch edge 0.5)
    (polygon (pts (xy 2 2) (xy 158 2) (xy 158 98) (xy 2 98)))
  )
  (zone (net 0) (net_name "") (layer "In2.Cu") (hatch edge 0.5)
    (polygon (pts (xy 2 2) (xy 158 2) (xy 158 98) (xy 2 98)))
  )
''')

out.append(')')

with open('/Users/arpankailashgupta/Desktop/kicad/defence_anc.kicad_pcb', 'w') as f:
    f.write("\n".join(out))
