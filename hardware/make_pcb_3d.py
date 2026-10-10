#!/usr/bin/env python3
"""
Generate a KiCad PCB with proper footprints that include pad definitions
and 3D model references so that kicad-cli can export a rich STEP file
importable into Autodesk Fusion 360.
"""
import uuid, textwrap

def uid(): return str(uuid.uuid4())

# 3D model path prefix (KiCad env variable)
M3D = "${KICAD8_3DMODEL_DIR}"

# ────────────────────────────────────────────────────
# Footprint generators — each returns a complete
# (footprint ...) s-expression string WITH real pads
# and a (model ...) reference.
# ────────────────────────────────────────────────────

def _fp_header(lib, ref, val, x, y, rot=0):
    return textwrap.dedent(f"""\
  (footprint "{lib}" (layer "F.Cu") (at {x} {y} {rot}) (attr smd)
    (fp_text reference "{ref}" (at 0 -3) (layer "F.SilkS") (effects (font (size 1 1) (thickness 0.15))))
    (fp_text value "{val}" (at 0 3) (layer "F.SilkS") (effects (font (size 0.8 0.8) (thickness 0.12))))""")

def _model(shape_dir, filename, sx=1, sy=1, sz=1):
    return f'    (model "{M3D}/{shape_dir}/{filename}" (offset (xyz 0 0 0)) (scale (xyz {sx} {sy} {sz})) (rotate (xyz 0 0 0)))'

def _smd_pad(num, x, y, w, h):
    return f'    (pad "{num}" smd rect (at {x} {y}) (size {w} {h}) (layers "F.Cu" "F.Paste" "F.Mask"))'

def _th_pad(num, x, y, size, drill):
    return f'    (pad "{num}" thru_hole circle (at {x} {y}) (size {size} {size}) (drill {drill}) (layers "*.Cu" "*.Mask"))'

def _np_pad(x, y, size, drill):
    return f'    (pad "" np_thru_hole circle (at {x} {y}) (size {size} {size}) (drill {drill}) (layers "*.Cu" "*.Mask"))'

# ── LQFP-144 (STM32) ──
def fp_lqfp144(ref, val, x, y):
    lines = [_fp_header("Package_QFP:LQFP-144_20x20mm_P0.5mm", ref, val, x, y)]
    # Generate 144 pads around 4 sides
    for i in range(36):
        px = -8.75 + i * 0.5
        lines.append(_smd_pad(i+1, px, 10.8, 0.3, 1.5))
    for i in range(36):
        py = 8.75 - i * 0.5
        lines.append(_smd_pad(37+i, 10.8, py, 1.5, 0.3))
    for i in range(36):
        px = 8.75 - i * 0.5
        lines.append(_smd_pad(73+i, px, -10.8, 0.3, 1.5))
    for i in range(36):
        py = -8.75 + i * 0.5
        lines.append(_smd_pad(109+i, -10.8, py, 1.5, 0.3))
    lines.append(_model("Package_QFP.3dshapes", "LQFP-144_20x20mm_P0.5mm.step"))
    lines.append("  )")
    return "\n".join(lines)

# ── BGA-144 (K210) ──
def fp_bga144(ref, val, x, y):
    lines = [_fp_header("Package_BGA:LFBGA-144_10x10mm_Layout12x12_P0.8mm", ref, val, x, y)]
    letters = "ABCDEFGHJKLM"
    for row in range(12):
        for col in range(12):
            px = -4.4 + col * 0.8
            py = -4.4 + row * 0.8
            pname = f"{letters[row]}{col+1}"
            lines.append(f'    (pad "{pname}" smd circle (at {px:.1f} {py:.1f}) (size 0.45 0.45) (layers "F.Cu" "F.Paste" "F.Mask"))')
    lines.append(_model("Package_BGA.3dshapes", "LFBGA-144_10x10mm_Layout12x12_P0.8mm.step"))
    lines.append("  )")
    return "\n".join(lines)

# ── TQFP-64 (ADC) ──
def fp_tqfp64(ref, val, x, y):
    lines = [_fp_header("Package_QFP:TQFP-64_10x10mm_P0.5mm", ref, val, x, y)]
    for i in range(16):
        px = -3.75 + i * 0.5
        lines.append(_smd_pad(i+1, px, 5.8, 0.25, 1.2))
    for i in range(16):
        py = 3.75 - i * 0.5
        lines.append(_smd_pad(17+i, 5.8, py, 1.2, 0.25))
    for i in range(16):
        px = 3.75 - i * 0.5
        lines.append(_smd_pad(33+i, px, -5.8, 0.25, 1.2))
    for i in range(16):
        py = -3.75 + i * 0.5
        lines.append(_smd_pad(49+i, -5.8, py, 1.2, 0.25))
    lines.append(_model("Package_QFP.3dshapes", "TQFP-64_10x10mm_P0.5mm.step"))
    lines.append("  )")
    return "\n".join(lines)

# ── SOIC-8 (generic) ──
def fp_soic8(ref, val, x, y):
    lines = [_fp_header("Package_SO:SOIC-8_3.9x4.9mm_P1.27mm", ref, val, x, y)]
    for i in range(4):
        py = -1.905 + i * 1.27
        lines.append(_smd_pad(i+1, -2.7, py, 1.5, 0.6))
        lines.append(_smd_pad(8-i, 2.7, py, 1.5, 0.6))
    lines.append(_model("Package_SO.3dshapes", "SOIC-8_3.9x4.9mm_P1.27mm.step"))
    lines.append("  )")
    return "\n".join(lines)

# ── SSOP-28 (Codec / DAC) ──
def fp_ssop28(ref, val, x, y):
    lines = [_fp_header("Package_SO:SSOP-28_5.3x10.2mm_P0.65mm", ref, val, x, y)]
    for i in range(14):
        py = -4.225 + i * 0.65
        lines.append(_smd_pad(i+1, -3.5, py, 1.5, 0.4))
        lines.append(_smd_pad(28-i, 3.5, py, 1.5, 0.4))
    lines.append(_model("Package_SO.3dshapes", "SSOP-28_5.3x10.2mm_P0.65mm.step"))
    lines.append("  )")
    return "\n".join(lines)

# ── QFN-48 (PMIC) ──
def fp_qfn48(ref, val, x, y):
    lines = [_fp_header("Package_DFN_QFN:QFN-48-1EP_7x7mm_P0.5mm_EP5.15x5.15mm", ref, val, x, y)]
    for i in range(12):
        px = -2.75 + i * 0.5
        lines.append(_smd_pad(i+1, px, 3.85, 0.25, 0.85))
    for i in range(12):
        py = 2.75 - i * 0.5
        lines.append(_smd_pad(13+i, 3.85, py, 0.85, 0.25))
    for i in range(12):
        px = 2.75 - i * 0.5
        lines.append(_smd_pad(25+i, px, -3.85, 0.25, 0.85))
    for i in range(12):
        py = -2.75 + i * 0.5
        lines.append(_smd_pad(37+i, -3.85, py, 0.85, 0.25))
    lines.append(_model("Package_DFN_QFN.3dshapes", "QFN-48-1EP_7x7mm_P0.5mm_EP5.15x5.15mm.step"))
    lines.append("  )")
    return "\n".join(lines)

# ── QFN-56 (TPA3255 Amp) ──
def fp_qfn56(ref, val, x, y):
    lines = [_fp_header("Package_DFN_QFN:QFN-56-1EP_8x8mm_P0.5mm_EP6.1x6.1mm", ref, val, x, y)]
    for i in range(14):
        px = -3.25 + i * 0.5
        lines.append(_smd_pad(i+1, px, 4.35, 0.25, 0.85))
    for i in range(14):
        py = 3.25 - i * 0.5
        lines.append(_smd_pad(15+i, 4.35, py, 0.85, 0.25))
    for i in range(14):
        px = 3.25 - i * 0.5
        lines.append(_smd_pad(29+i, px, -4.35, 0.25, 0.85))
    for i in range(14):
        py = -3.25 + i * 0.5
        lines.append(_smd_pad(43+i, -4.35, py, 0.85, 0.25))
    lines.append(_model("Package_DFN_QFN.3dshapes", "QFN-56-1EP_7x7mm_P0.4mm_EP3.2x3.2mm.step"))
    lines.append("  )")
    return "\n".join(lines)

# ── SOT-223 (LDO) ──
def fp_sot223(ref, val, x, y):
    lines = [_fp_header("Package_TO_SOT_SMD:SOT-223-3_TabPin2", ref, val, x, y)]
    lines.append(_smd_pad(1, -2.3, 3.15, 1.0, 0.7))
    lines.append(_smd_pad(2, 0, 3.15, 1.0, 0.7))
    lines.append(_smd_pad(3, 2.3, 3.15, 1.0, 0.7))
    lines.append(_smd_pad(4, 0, -3.15, 3.8, 1.6))
    lines.append(_model("Package_TO_SOT_SMD.3dshapes", "SOT-223.step"))
    lines.append("  )")
    return "\n".join(lines)

# ── TSOP-II-54 (SDRAM) ──
def fp_tsop54(ref, val, x, y):
    lines = [_fp_header("Package_SO:TSOP-II-54_22.2x10.16mm_P0.8mm", ref, val, x, y)]
    for i in range(27):
        px = -10.4 + i * 0.8
        lines.append(_smd_pad(i+1, px, 5.7, 0.4, 1.0))
        lines.append(_smd_pad(54-i, px, -5.7, 0.4, 1.0))
    lines.append(_model("Package_SO.3dshapes", "TSOP-II-54_22.2x10.16mm_P0.8mm.step"))
    lines.append("  )")
    return "\n".join(lines)

# ── LGA-14 (IMU) ──
def fp_lga14(ref, val, x, y):
    lines = [_fp_header("Package_LGA:LGA-14_3x2.5mm_P0.5mm_LayoutBorder3x4y", ref, val, x, y)]
    for i in range(7):
        py = -1.5 + i * 0.5
        lines.append(_smd_pad(i+1, -1.45, py, 0.6, 0.3))
        lines.append(_smd_pad(14-i, 1.45, py, 0.6, 0.3))
    lines.append(_model("Package_LGA.3dshapes", "LGA-14_3x2.5mm_P0.5mm_LayoutBorder3x4y.step"))
    lines.append("  )")
    return "\n".join(lines)

# ── LGA-10 / Bosch (Barometer) ──
def fp_lga10(ref, val, x, y):
    lines = [_fp_header("Package_LGA:LGA-12_2x2mm_P0.5mm", ref, val, x, y)]
    for i in range(5):
        py = -1.0 + i * 0.5
        lines.append(_smd_pad(i+1, -0.95, py, 0.5, 0.25))
        lines.append(_smd_pad(10-i, 0.95, py, 0.5, 0.25))
    lines.append(_model("Package_LGA.3dshapes", "LGA-12_2x2mm_P0.5mm.step"))
    lines.append("  )")
    return "\n".join(lines)

# ── MEMS Microphone ──
def fp_mic(ref, val, x, y):
    lines = [_fp_header("Sensor_Audio:Knowles_LGA-5_3.5x2.65mm", ref, val, x, y)]
    lines.append(_smd_pad(1, -1.1, -0.65, 0.7, 0.5))
    lines.append(_smd_pad(2, 1.1, -0.65, 0.7, 0.5))
    lines.append(_smd_pad(3, 1.1, 0.65, 0.7, 0.5))
    lines.append(_smd_pad(4, -1.1, 0.65, 0.7, 0.5))
    lines.append(_smd_pad(5, 0, 0.65, 0.7, 0.5))
    lines.append("  )")
    return "\n".join(lines)

# ── Pin Header 1x02 ──
def fp_pinheader(ref, val, x, y):
    lines = [_fp_header("Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical", ref, val, x, y).replace("(attr smd)", "")]
    lines.append(_th_pad(1, 0, 0, 1.7, 1.0))
    lines.append(_th_pad(2, 0, 2.54, 1.7, 1.0))
    lines.append(_model("Connector_PinHeader_2.54mm.3dshapes", "PinHeader_1x02_P2.54mm_Vertical.step"))
    lines.append("  )")
    return "\n".join(lines)

# ── Mounting hole ──
def fp_mounting(x, y):
    return f'  (footprint "MountingHole:MountingHole_3.2mm_M3" (layer "F.Cu") (at {x} {y}) (pad "" np_thru_hole circle (at 0 0) (size 3.2 3.2) (drill 3.2) (layers "*.Cu" "*.Mask")))'


# ════════════════════════════════════════════════════
# Assemble the full PCB
# ════════════════════════════════════════════════════
pcb = []
pcb.append('(kicad_pcb (version 20230121) (generator pcbnew)')
pcb.append('  (general (thickness 1.6))')
pcb.append('  (paper "A4")')
pcb.append('  (title_block (title "Defence AI-ANC System PCB") (rev "v1.0") (company "Defence AI Systems"))')

pcb.append('''
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

# Board outline
pcb.append('  (gr_rect (start 0 0) (end 160 100) (layer "Edge.Cuts") (stroke (width 0.1) (type solid)) (fill none))')

# Mounting holes
for mx, my in [(4,4),(156,4),(4,96),(156,96)]:
    pcb.append(fp_mounting(mx, my))

# Zone labels (silkscreen)
zones_silk = [
    ('  (gr_rect (start 50 10) (end 110 50) (layer "F.SilkS") (stroke (width 0.1) (type dash)) (fill none))', "MCU CORE", 80, 14),
    ('  (gr_rect (start 110 10) (end 150 50) (layer "F.SilkS") (stroke (width 0.1) (type dash)) (fill none))', "AI NPU", 130, 14),
    ('  (gr_rect (start 10 10) (end 50 50) (layer "F.SilkS") (stroke (width 0.1) (type dash)) (fill none))', "AUDIO INPUT", 30, 14),
    ('  (gr_rect (start 110 50) (end 150 85) (layer "F.SilkS") (stroke (width 0.1) (type dash)) (fill none))', "AUDIO OUT", 130, 55),
    ('  (gr_rect (start 10 50) (end 70 85) (layer "F.SilkS") (stroke (width 0.1) (type dash)) (fill none))', "POWER", 40, 55),
    ('  (gr_rect (start 70 50) (end 110 85) (layer "F.SilkS") (stroke (width 0.1) (type dash)) (fill none))', "COMMS / SENSORS", 90, 55),
]
for rect, label, lx, ly in zones_silk:
    pcb.append(rect)
    pcb.append(f'  (gr_text "{label}" (at {lx} {ly}) (layer "F.SilkS") (effects (font (size 2 2) (thickness 0.3))))')

# ── Place components ──
pcb.append(fp_lqfp144("U1", "STM32H755", 80, 30))
pcb.append(fp_bga144("U2", "K210 NPU", 130, 28))
pcb.append(fp_tsop54("U14", "SDRAM", 125, 42))
pcb.append(fp_soic8("U13", "Flash", 140, 42))
pcb.append(fp_mic("MK1", "Mic1", 20, 25))
pcb.append(fp_mic("MK2", "Mic2", 20, 38))
pcb.append(fp_soic8("U4", "PreAmp", 32, 31.5))
pcb.append(fp_soic8("U18", "Filter", 42, 31.5))
pcb.append(fp_tqfp64("U5", "ADC", 42, 43))
pcb.append(fp_ssop28("U3", "Codec", 120, 65))
pcb.append(fp_ssop28("U10", "DAC", 120, 76))
pcb.append(fp_qfn56("U9", "Amplifier", 140, 70))
pcb.append(fp_pinheader("J4", "PWR_IN", 20, 65))
pcb.append(fp_qfn48("U6", "PMIC", 35, 68))
pcb.append(fp_sot223("U7", "3.3V LDO", 52, 68))
pcb.append(fp_sot223("U8", "1.8V LDO", 62, 68))
pcb.append(fp_soic8("U11", "RS485", 82, 65))
pcb.append(fp_soic8("U12", "CAN FD", 98, 65))
pcb.append(fp_lga14("U15", "IMU", 82, 77))
pcb.append(fp_lga10("U16", "Baro", 98, 77))

# Title silkscreen
pcb.append('  (gr_text "DEFENCE AI-ANC SYSTEM v1.0" (at 80 92) (layer "F.SilkS") (effects (font (size 2.5 2.5) (thickness 0.5) (bold yes))))')
pcb.append('  (gr_text "MIL-STD-810H | IP67 | -40C to +85C | ITAR CONTROLLED" (at 80 95) (layer "F.SilkS") (effects (font (size 1.2 1.2) (thickness 0.2))))')

pcb.append(')')

with open('/Users/arpankailashgupta/Desktop/kicad/defence_anc.kicad_pcb', 'w') as f:
    f.write("\n".join(pcb))

print("PCB with full 3D model references written successfully.")
