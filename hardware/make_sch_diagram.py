import uuid

out = []
out.append('(kicad_sch (version 20230121) (generator eeschema)')
out.append('  (uuid "a1b2c3d4-e5f6-7890-abcd-ef1234567890")')
out.append('  (paper "A3")')
out.append('  (title_block (title "Defence AI-ANC System - Block Diagram") (date "2026-09-25") (rev "v1.0") (company "Defence AI Systems"))')

def make_uuid():
    return str(uuid.uuid4())

def draw_box(x, y, w, h, title, subtitle):
    # Box
    out.append(f'  (rectangle (start {x} {y}) (end {x+w} {y+h}) (stroke (width 0.5) (type solid)) (fill (type background)))')
    # Title bar
    out.append(f'  (rectangle (start {x} {y}) (end {x+w} {y+6}) (stroke (width 0.5) (type solid)) (fill (type background)))')
    # Text
    out.append(f'  (text "{title}" (at {x+w/2} {y+3} 0) (effects (font (size 2 2) (thickness 0.3) (bold yes))))')
    if subtitle:
        out.append(f'  (text "{subtitle}" (at {x+w/2} {y+h/2+2} 0) (effects (font (size 1.5 1.5))))')

def draw_wire(x1, y1, x2, y2, label=""):
    uid = make_uuid()
    out.append(f'  (wire (pts (xy {x1} {y1}) (xy {x2} {y2})) (stroke (width 0) (type solid)) (uuid "{uid}"))')
    if label:
        lx = (x1+x2)/2
        ly = (y1+y2)/2 - 1.5
        out.append(f'  (global_label "{label}" (shape input) (at {lx} {ly} 0) (fields_autoplaced) (effects (font (size 1.5 1.5)) (justify left)))')

# --- Layout ---
# Input chain
draw_box(20, 50, 40, 20, "ICS-40300 x2", "Primary & Ref Mics")
draw_wire(60, 60, 80, 60, "Analog")
draw_box(80, 50, 40, 20, "INA217", "Low-Noise Pre-Amp")
draw_wire(120, 60, 140, 60, "Gain")
draw_box(140, 50, 40, 20, "MAX7401", "8th-Order Filter")
draw_wire(180, 60, 200, 60, "Filtered")
draw_box(200, 50, 40, 20, "ADS1274", "24-bit 4-ch ADC")
draw_wire(240, 60, 270, 60, "I2S / SAI")

# Core MCU
draw_box(270, 40, 50, 80, "STM32H755", "Dual-Core ARM Cortex\\nDSP / DMA Controller\\nAudio Router")

# NPU Coprocessor
draw_wire(320, 60, 360, 60, "SPI (50 MHz)")
draw_box(360, 40, 50, 80, "Kendryte K210", "RISC-V AI NPU\\nConv-TasNet Model\\n12ms Inference")

# Memory (attached to NPU)
draw_wire(385, 120, 385, 140, "SPI Bus")
draw_box(360, 140, 50, 20, "W25Q128 Flash", "AI Model Storage")

draw_wire(385, 40, 385, 20, "RAM Bus")
draw_box(360, 0, 50, 20, "IS42S32200L", "64Mb SDRAM")

# Output chain
draw_wire(295, 120, 295, 150, "I2S Out")
draw_box(270, 150, 50, 20, "CS4270 / PCM1794A", "24-bit DAC")
draw_wire(295, 170, 295, 190, "Analog L/R")
draw_box(270, 190, 50, 20, "TPA3255", "315W Class-D Amp")
draw_wire(295, 210, 295, 230, "Speaker Out")
draw_box(270, 230, 50, 20, "Anti-Noise Headset", "Output")

# Power Management (bottom left)
draw_box(20, 180, 50, 30, "TPS65217 PMIC", "Power Management\\n7-36V Input")
draw_wire(70, 195, 100, 195, "5V, 3.3V, 1.8V")
draw_box(100, 185, 40, 20, "TLV1117 x2", "LDO Regulators")

# Sensors
draw_box(20, 100, 40, 20, "ICM-42688-P", "6-Axis IMU")
draw_wire(60, 110, 270, 110, "I2C")
draw_box(80, 130, 40, 20, "BMP388", "Barometer")
draw_wire(100, 130, 100, 110)

# Comms
draw_wire(320, 90, 360, 170, "UART") # Just a line to the right
draw_box(360, 170, 50, 20, "SP3485", "RS-485 Transceiver")
draw_wire(320, 100, 360, 210, "CAN")
draw_box(360, 200, 50, 20, "TCAN1044", "CAN FD Transceiver")

out.append('  (sheet_instances (path "/" (page "1")))')
out.append(')')

with open('/Users/arpankailashgupta/Desktop/kicad/defence_anc.kicad_sch', 'w') as f:
    f.write("\n".join(out))

print("Block diagram schematic generated.")
