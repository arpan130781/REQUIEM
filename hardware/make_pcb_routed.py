import uuid

def make_uuid(): return str(uuid.uuid4())

out = []
out.append('(kicad_pcb (version 20230121) (generator pcbnew)')
out.append('  (general (thickness 1.6))')
out.append('  (paper "A4")')
out.append('  (title_block (title "Defence AI-ANC System PCB") (rev "v1.0") (company "Defence AI Systems"))')

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

# Board Outline & Mounting holes
out.append('  (gr_rect (start 0 0) (end 160 100) (layer "Edge.Cuts") (stroke (width 0.1) (type solid)) (fill none))')
for x, y in [(4, 4), (156, 4), (4, 96), (156, 96)]:
    out.append(f'  (footprint "MountingHole:MountingHole_3.2mm_M3" (layer "F.Cu") (at {x} {y}) (pad "1" np_thru_hole circle (at 0 0) (size 3.2 3.2) (drill 3.2) (layers "*.Cu" "*.Mask")))')

def place_ic(ref, pkg, val, x, y, rot=0, w=3, h=3):
    # Hide the default value (which goes to F.Fab), and put our own readable name on SilkS!
    out.append(f'''
  (footprint "{pkg}" (layer "F.Cu") (at {x} {y} {rot}) (attr smd)
    (fp_text reference "{ref}" (at 0 -2.5) (layer "F.SilkS") (effects (font (size 1 1) (thickness 0.15))))
    (fp_text value "{val}" (at 0 2.5) (layer "F.SilkS") (effects (font (size 1 1) (thickness 0.15))))
    (fp_rect (start -{w} -{h}) (end {w} {h}) (layer "F.SilkS") (stroke (width 0.15) (type solid)) (fill none))
  )''')

# ----- ZONES & COMPONENTS -----

# MCU CORE (50 to 110)
out.append('  (gr_rect (start 50 10) (end 110 50) (layer "F.SilkS") (stroke (width 0.1) (type dash)) (fill none))')
out.append('  (gr_text "MCU CORE" (at 80 14) (layer "F.SilkS") (effects (font (size 2 2) (thickness 0.3))))')
place_ic("U1", "Package_QFP:LQFP-144_20x20mm_P0.5mm", "STM32 MCU", 80, 30, w=4, h=4)

# AI NPU (110 to 150)
out.append('  (gr_rect (start 110 10) (end 150 50) (layer "F.SilkS") (stroke (width 0.1) (type dash)) (fill none))')
out.append('  (gr_text "AI NPU" (at 130 14) (layer "F.SilkS") (effects (font (size 2 2) (thickness 0.3))))')
place_ic("U2", "Package_BGA:BGA-144_10x10mm_P0.8mm", "K210 AI Chip", 130, 25, w=4, h=4)
place_ic("U14", "Package_SO:TSOP-II-54_10.16x22.22mm_P0.8mm", "SDRAM", 125, 42)
place_ic("U13", "Package_SO:SOIC-8_3.9x4.9mm_P1.27mm", "Flash", 140, 42)

# AUDIO INPUT (10 to 50)
out.append('  (gr_rect (start 10 10) (end 50 50) (layer "F.SilkS") (stroke (width 0.1) (type dash)) (fill none))')
out.append('  (gr_text "AUDIO INPUT" (at 30 14) (layer "F.SilkS") (effects (font (size 2 2) (thickness 0.3))))')
place_ic("MK1", "Sensor_Audio:Microphone_MEMS_4x3mm", "Primary Mic", 20, 25, w=2, h=1.5)
place_ic("MK2", "Sensor_Audio:Microphone_MEMS_4x3mm", "Ref Mic", 20, 38, w=2, h=1.5)
place_ic("U4", "Package_SO:SOIC-8_3.9x4.9mm_P1.27mm", "Pre-Amp", 32, 31.5)
place_ic("U18", "Package_SO:SOIC-8_3.9x4.9mm_P1.27mm", "Filter", 42, 31.5)
place_ic("U5", "Package_QFP:TQFP-64_10x10mm_P0.5mm", "ADC 24-bit", 42, 43, w=3.5, h=3.5)

# AUDIO OUT (110 to 150)
out.append('  (gr_rect (start 110 50) (end 150 85) (layer "F.SilkS") (stroke (width 0.1) (type dash)) (fill none))')
out.append('  (gr_text "AUDIO OUT" (at 130 55) (layer "F.SilkS") (effects (font (size 2 2) (thickness 0.3))))')
place_ic("U3", "Package_SO:SSOP-28_5.3x10.2mm_P0.65mm", "Codec", 120, 65)
place_ic("U10", "Package_SO:SSOP-28_5.3x10.2mm_P0.65mm", "DAC", 120, 76)
place_ic("U9", "Package_DFN_QFN:QFN-56-1EP_8x8mm_P0.5mm_EP6.1x6.1mm", "315W Amp", 140, 70, w=3.5, h=3.5)

# POWER (10 to 70)
out.append('  (gr_rect (start 10 50) (end 70 85) (layer "F.SilkS") (stroke (width 0.1) (type dash)) (fill none))')
out.append('  (gr_text "POWER" (at 40 55) (layer "F.SilkS") (effects (font (size 2 2) (thickness 0.3))))')
place_ic("J4", "Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical", "PWR IN", 20, 65)
place_ic("U6", "Package_DFN_QFN:QFN-48-1EP_7x7mm_P0.5mm_EP5.15x5.15mm", "PMIC", 35, 65, w=3, h=3)
place_ic("U7", "Package_TO_SOT_SMD:SOT-223-3_TabPin2", "3.3V LDO", 50, 65)
place_ic("U8", "Package_TO_SOT_SMD:SOT-223-3_TabPin2", "1.8V LDO", 60, 65)

# COMMS & SENSORS (70 to 110)
out.append('  (gr_rect (start 70 50) (end 110 85) (layer "F.SilkS") (stroke (width 0.1) (type dash)) (fill none))')
out.append('  (gr_text "COMMS / SENSORS" (at 90 55) (layer "F.SilkS") (effects (font (size 1.5 1.5) (thickness 0.2))))')
place_ic("U11", "Package_SO:SOIC-8_3.9x4.9mm_P1.27mm", "RS485", 82, 65)
place_ic("U12", "Package_SO:SOIC-8_3.9x4.9mm_P1.27mm", "CAN FD", 98, 65)
place_ic("U15", "Package_LGA:LGA-14_2.5x3mm_P0.5mm", "IMU", 82, 77)
place_ic("U16", "Package_LGA:LGA-10_2x2mm_P0.5mm", "Barometer", 98, 77)

def add_track_segment(x1, y1, x2, y2, layer="F.Cu", width=0.25):
    out.append(f'  (segment (start {x1:.3f} {y1:.3f}) (end {x2:.3f} {y2:.3f}) (width {width}) (layer "{layer}") (net 0))')

def route_bus(pts, num_tracks=4, spacing=0.6, layer="F.Cu", width=0.25):
    for i in range(num_tracks):
        offset = (i - (num_tracks - 1) / 2.0) * spacing
        for j in range(len(pts)-1):
            x1, y1 = pts[j]
            x2, y2 = pts[j+1]
            dx, dy = x2 - x1, y2 - y1
            
            # Normal vector logic
            if abs(dx) > 0.1 and abs(dy) < 0.1: # Horizontal line
                oy = offset; ox = 0
            elif abs(dy) > 0.1 and abs(dx) < 0.1: # Vertical line
                ox = offset; oy = 0
            else: # Diagonal line (45 deg assumed)
                # sign_x and sign_y
                sx = 1 if dx > 0 else -1
                sy = 1 if dy > 0 else -1
                ox = -sy * offset * 0.7071
                oy = sx * offset * 0.7071
            
            add_track_segment(x1+ox, y1+oy, x2+ox, y2+oy, layer, width)

# ----- ROUTING BUSES -----
# Mic to Preamp (Analog)
route_bus([(22, 25), (28, 25), (32, 29)], num_tracks=2, layer="F.Cu", width=0.2)
route_bus([(22, 38), (28, 38), (32, 34)], num_tracks=2, layer="F.Cu", width=0.2)

# Preamp -> Filter -> ADC (Analog)
route_bus([(35, 31.5), (39, 31.5)], num_tracks=2, layer="F.Cu", width=0.2)
route_bus([(42, 34), (42, 40)], num_tracks=2, layer="F.Cu", width=0.2)

# ADC -> MCU (Digital Audio I2S)
route_bus([(46, 43), (67, 43), (76, 34)], num_tracks=6, layer="F.Cu", width=0.2, spacing=0.5)

# MCU -> AI NPU (High speed parallel/SPI)
route_bus([(84, 30), (126, 30)], num_tracks=16, layer="F.Cu", width=0.15, spacing=0.3)

# AI NPU -> SDRAM (Memory Bus)
route_bus([(130, 29), (130, 39)], num_tracks=16, layer="B.Cu", width=0.15, spacing=0.3)

# AI NPU -> Flash (SPI)
route_bus([(134, 25), (140, 25), (140, 39)], num_tracks=4, layer="F.Cu", width=0.2, spacing=0.4)

# MCU -> DACs (I2S Audio Out)
route_bus([(84, 32), (105, 32), (115, 42), (115, 76), (117, 76)], num_tracks=8, layer="B.Cu", width=0.2, spacing=0.4)
route_bus([(115, 65), (117, 65)], num_tracks=4, layer="B.Cu", width=0.2, spacing=0.4)

# DAC -> Amp (Analog Out)
route_bus([(123, 76), (136.5, 76), (136.5, 73)], num_tracks=2, layer="F.Cu", width=0.3)

# PMIC Power Distribution
route_bus([(38, 65), (47, 65)], num_tracks=3, layer="In1.Cu", width=0.6, spacing=0.8) # PMIC to LDOs
route_bus([(35, 62), (35, 52), (52, 35), (76, 35)], num_tracks=2, layer="In1.Cu", width=0.6, spacing=1.2) # To MCU

# Comms
route_bus([(80, 34), (80, 62)], num_tracks=4, layer="B.Cu", width=0.2, spacing=0.4) # MCU to UART/CAN

out.append('  (gr_text "DEFENCE AI-ANC SYSTEM v1.0" (at 80 92) (layer "F.SilkS") (effects (font (size 2.5 2.5) (thickness 0.5) (bold yes))))')
out.append('  (gr_text "MIL-STD-810H | IP67 | -40C to +85C | ITAR CONTROLLED" (at 80 95) (layer "F.SilkS") (effects (font (size 1.2 1.2) (thickness 0.2))))')

out.append(')')

with open('/Users/arpankailashgupta/Desktop/kicad/defence_anc.kicad_pcb', 'w') as f:
    f.write("\n".join(out))
