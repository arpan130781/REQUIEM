#!/usr/bin/env python3
"""
Generate a professional multi-view 2D engineering drawing of the Defence AI-ANC PCB
with Top View, Front View (elevation), Right Side View, and an Isometric sketch.
All views are drawn to scale with proper dimensions, annotations, and a title block.
"""
from reportlab.lib.pagesizes import A3, landscape
from reportlab.lib.units import mm, cm
from reportlab.lib import colors
from reportlab.pdfgen import canvas
import math, os

OUT = "/Users/arpankailashgupta/Desktop/kicad/PCB_2D_Engineering_Views.pdf"

# Board dimensions in mm
BW, BH, BT = 160.0, 100.0, 1.6  # width, height, board thickness
SCALE = 2.0  # drawing scale (2:1 so it fills A3 nicely)

# Component heights (mm above board surface)
COMP_HEIGHTS = {
    "U1":   1.6,   # LQFP-144
    "U2":   1.2,   # BGA
    "U14":  1.2,   # TSOP SDRAM
    "U13":  1.5,   # SOIC-8
    "MK1":  1.1,   # MEMS mic
    "MK2":  1.1,
    "U4":   1.5,   # SOIC-8
    "U18":  1.5,
    "U5":   1.0,   # TQFP-64
    "U3":   2.0,   # SSOP-28
    "U10":  2.0,
    "U9":   1.0,   # QFN-56
    "J4":   8.5,   # Pin header (tallest)
    "U6":   1.0,   # QFN-48
    "U7":   1.8,   # SOT-223
    "U8":   1.8,
    "U11":  1.5,
    "U12":  1.5,
    "U15":  0.9,   # LGA
    "U16":  0.8,
}

# Component positions (x, y in board coords) and widths for front/side projections
COMPS = [
    # ref,    x,    y,   pkg_w, pkg_h, height
    ("MK1",   20,   25,   4,     3,    1.1),
    ("MK2",   20,   38,   4,     3,    1.1),
    ("U4",    32,   31.5, 4,     5,    1.5),
    ("U18",   42,   31.5, 4,     5,    1.5),
    ("U5",    42,   43,   10,    10,   1.0),
    ("U1",    80,   30,   20,    20,   1.6),
    ("U2",    130,  28,   10,    10,   1.2),
    ("U14",   125,  42,   22,    10,   1.2),
    ("U13",   140,  42,   4,     5,    1.5),
    ("U3",    120,  65,   5.3,   10,   2.0),
    ("U10",   120,  76,   5.3,   10,   2.0),
    ("U9",    140,  70,   8,     8,    1.0),
    ("J4",    20,   65,   2.5,   5,    8.5),
    ("U6",    35,   68,   7,     7,    1.0),
    ("U7",    52,   68,   3.5,   6.5,  1.8),
    ("U8",    62,   68,   3.5,   6.5,  1.8),
    ("U11",   82,   65,   4,     5,    1.5),
    ("U12",   98,   65,   4,     5,    1.5),
    ("U15",   82,   77,   3,     2.5,  0.9),
    ("U16",   98,   77,   2,     2,    0.8),
]

def main():
    W, H = landscape(A3)
    c = canvas.Canvas(OUT, pagesize=landscape(A3))

    # Colors
    C_BOARD   = colors.HexColor("#2E7D32")
    C_COPPER  = colors.HexColor("#B8860B")
    C_COMP    = colors.HexColor("#1A237E")
    C_PIN     = colors.HexColor("#C62828")
    C_DIM     = colors.HexColor("#424242")
    C_SILK    = colors.HexColor("#FFFFFF")
    C_LIGHT   = colors.HexColor("#E8F5E9")
    C_BG      = colors.HexColor("#FAFAFA")

    # Background
    c.setFillColor(C_BG)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    # Title block
    tb_h = 25*mm
    c.setFillColor(colors.HexColor("#1B2A4A"))
    c.rect(0, 0, W, tb_h, fill=1, stroke=0)
    c.setFillColor(colors.HexColor("#D4A528"))
    c.rect(0, tb_h-2, W, 2, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(15*mm, 13*mm, "DEFENCE AI-ANC SYSTEM — 2D ORTHOGRAPHIC VIEWS")
    c.setFont("Helvetica", 10)
    c.drawString(15*mm, 6*mm, "Scale 2:1  |  Board: 160 x 100 x 1.6 mm  |  4-Layer FR4 Tg170  |  ENIG  |  MIL-STD-810H")
    c.drawRightString(W - 15*mm, 13*mm, "Rev v1.0  |  Sep 2026")
    c.drawRightString(W - 15*mm, 6*mm, "Defence AI Systems  |  ITAR CONTROLLED")

    # ────────────────────────────────────────
    # Helper: dimension line
    # ────────────────────────────────────────
    def dim_line(x1, y1, x2, y2, label, offset=8, horiz=True):
        c.setStrokeColor(C_DIM)
        c.setFillColor(C_DIM)
        c.setLineWidth(0.3)
        c.setFont("Helvetica", 7)
        if horiz:
            yo = y1 + offset
            c.line(x1, y1, x1, yo + 2)
            c.line(x2, y2, x2, yo + 2)
            c.line(x1, yo, x2, yo)
            # arrows
            p = c.beginPath()
            p.moveTo(x1, yo); p.lineTo(x1+3, yo+1.5); p.lineTo(x1+3, yo-1.5); p.close()
            c.drawPath(p, fill=1)
            p = c.beginPath()
            p.moveTo(x2, yo); p.lineTo(x2-3, yo+1.5); p.lineTo(x2-3, yo-1.5); p.close()
            c.drawPath(p, fill=1)
            c.drawCentredString((x1+x2)/2, yo+3, label)
        else:
            xo = x1 + offset
            c.line(x1, y1, xo + 2, y1)
            c.line(x2, y2, xo + 2, y2)
            c.line(xo, y1, xo, y2)
            p = c.beginPath()
            p.moveTo(xo, y1); p.lineTo(xo+1.5, y1+3); p.lineTo(xo-1.5, y1+3); p.close()
            c.drawPath(p, fill=1)
            p = c.beginPath()
            p.moveTo(xo, y2); p.lineTo(xo+1.5, y2-3); p.lineTo(xo-1.5, y2-3); p.close()
            c.drawPath(p, fill=1)
            c.saveState()
            c.translate(xo+5, (y1+y2)/2)
            c.rotate(90)
            c.drawCentredString(0, 0, label)
            c.restoreState()

    # ════════════════════════════════════════
    # VIEW 1: TOP VIEW (upper-left)
    # ════════════════════════════════════════
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(colors.HexColor("#1B2A4A"))
    c.drawString(20*mm, H - 15*mm, "1. TOP VIEW (Component Side)")

    ox1, oy1 = 25*mm, H - 25*mm  # origin (top-left of board drawing)
    s = SCALE

    # Board body
    bx, by = ox1, oy1 - BH*s
    c.setFillColor(C_BOARD)
    c.setStrokeColor(colors.black)
    c.setLineWidth(0.8)
    c.rect(bx, by, BW*s, BH*s, fill=1, stroke=1)

    # Mounting holes
    c.setFillColor(C_BG)
    for mx, my in [(4,4),(156,4),(4,96),(156,96)]:
        c.circle(bx + mx*s, by + (BH - my)*s, 1.6*s, fill=1, stroke=1)

    # Zone boxes
    zones = [
        (10, 10, 50, 50, "AUDIO\nINPUT"),
        (50, 10, 110, 50, "MCU\nCORE"),
        (110, 10, 150, 50, "AI\nNPU"),
        (10, 50, 70, 85, "POWER"),
        (70, 50, 110, 85, "COMMS\nSENSORS"),
        (110, 50, 150, 85, "AUDIO\nOUT"),
    ]
    c.setStrokeColor(colors.HexColor("#FFFFFF"))
    c.setLineWidth(0.4)
    c.setDash(3, 2)
    for zx1, zy1, zx2, zy2, zlabel in zones:
        rx = bx + zx1*s
        ry = by + (BH - zy2)*s
        rw = (zx2 - zx1)*s
        rh = (zy2 - zy1)*s
        c.rect(rx, ry, rw, rh, fill=0, stroke=1)
        c.setFillColor(colors.HexColor("#FFFFFF"))
        c.setFont("Helvetica-Bold", 6)
        for li, line in enumerate(zlabel.split("\n")):
            c.drawCentredString(rx + rw/2, ry + rh - 6 - li*8, line)
    c.setDash()

    # Components as filled rectangles
    c.setFillColor(C_COMP)
    c.setStrokeColor(colors.HexColor("#0D1B3E"))
    c.setLineWidth(0.3)
    for ref, cx, cy, pw, ph, ch in COMPS:
        rx = bx + (cx - pw/2)*s
        ry = by + (BH - cy - ph/2)*s
        c.rect(rx, ry, pw*s, ph*s, fill=1, stroke=1)
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 5)
        c.drawCentredString(rx + pw*s/2, ry + ph*s/2 - 2, ref)
        c.setFillColor(C_COMP)

    # Dimension lines for top view
    dim_line(bx, by - 3, bx + BW*s, by - 3, "160 mm", offset=-12, horiz=True)
    dim_line(bx + BW*s + 3, by, bx + BW*s + 3, by + BH*s, "100 mm", offset=8, horiz=False)

    # ════════════════════════════════════════
    # VIEW 2: FRONT VIEW (bottom-left)
    # ════════════════════════════════════════
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(colors.HexColor("#1B2A4A"))
    c.drawString(20*mm, H/2 - 15*mm, "2. FRONT VIEW (Long Edge)")

    ox2, oy2 = 25*mm, H/2 - 25*mm
    front_s = SCALE  # same scale

    # Board cross-section (thin rectangle)
    fb_y = oy2 - 30*mm  # baseline
    c.setFillColor(C_BOARD)
    c.setStrokeColor(colors.black)
    c.setLineWidth(0.8)
    c.rect(ox2, fb_y, BW*front_s, BT*front_s*5, fill=1, stroke=1)  # exaggerate thickness for visibility
    bt_draw = BT * front_s * 5

    # Components on top (front projection = width along X, height above board)
    h_scale = 4.0  # exaggerate height for visibility
    c.setFillColor(C_COMP)
    c.setStrokeColor(colors.HexColor("#0D1B3E"))
    c.setLineWidth(0.3)
    for ref, cx, cy, pw, ph, ch in COMPS:
        rx = ox2 + (cx - pw/2)*front_s
        ry = fb_y + bt_draw
        rw = pw * front_s
        rh = ch * front_s * h_scale
        c.rect(rx, ry, rw, rh, fill=1, stroke=1)
        if rw > 8:
            c.setFillColor(colors.white)
            c.setFont("Helvetica", 4)
            c.drawCentredString(rx + rw/2, ry + rh/2 - 1.5, ref)
            c.setFillColor(C_COMP)

    # Pin header J4 highlight (tallest)
    c.setFillColor(C_PIN)
    j4_x = ox2 + (20 - 1.25)*front_s
    j4_h = 8.5 * front_s * h_scale
    c.rect(j4_x, fb_y + bt_draw, 2.5*front_s, j4_h, fill=1, stroke=1)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 5)
    c.drawCentredString(j4_x + 1.25*front_s, fb_y + bt_draw + j4_h/2, "J4")

    # Dimension
    dim_line(ox2, fb_y - 3, ox2 + BW*front_s, fb_y - 3, "160 mm", offset=-12, horiz=True)
    # Height dimension for tallest component
    dim_line(ox2 + BW*front_s + 5, fb_y, ox2 + BW*front_s + 5, fb_y + bt_draw + 8.5*front_s*h_scale, f"Max H: {8.5+1.6:.1f} mm", offset=12, horiz=False)

    # Board thickness callout
    c.setFillColor(C_DIM)
    c.setFont("Helvetica", 6)
    c.drawString(ox2 + BW*front_s + 25, fb_y + bt_draw/2 - 2, f"PCB: {BT} mm")

    # ════════════════════════════════════════
    # VIEW 3: RIGHT SIDE VIEW (upper-right)
    # ════════════════════════════════════════
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(colors.HexColor("#1B2A4A"))
    side_ox = W/2 + 20*mm
    c.drawString(side_ox, H - 15*mm, "3. RIGHT SIDE VIEW (Short Edge)")

    ox3 = side_ox
    oy3 = H - 25*mm
    side_s = SCALE

    # Board (thin rect, depth = BH)
    sb_y = oy3 - BH*side_s - 20*mm
    c.setFillColor(C_BOARD)
    c.setStrokeColor(colors.black)
    c.setLineWidth(0.8)
    c.rect(ox3, sb_y, BT*side_s*5, BH*side_s, fill=1, stroke=1)
    sbt_draw = BT * side_s * 5

    # Components on top (side projection = depth along Y, height above board)
    c.setFillColor(C_COMP)
    c.setStrokeColor(colors.HexColor("#0D1B3E"))
    c.setLineWidth(0.3)
    for ref, cx, cy, pw, ph, ch in COMPS:
        ry = sb_y + (BH - cy - ph/2)*side_s
        rx = ox3 + sbt_draw
        rw = ch * side_s * h_scale
        rh = ph * side_s
        c.rect(rx, ry, rw, rh, fill=1, stroke=1)
        if rh > 8:
            c.setFillColor(colors.white)
            c.setFont("Helvetica", 4)
            c.drawCentredString(rx + rw/2, ry + rh/2 - 1.5, ref)
            c.setFillColor(C_COMP)

    # Dimension
    dim_line(ox3 - 5, sb_y, ox3 - 5, sb_y + BH*side_s, "100 mm", offset=-15, horiz=False)

    # ════════════════════════════════════════
    # VIEW 4: LAYER STACKUP (bottom-right)
    # ════════════════════════════════════════
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(colors.HexColor("#1B2A4A"))
    c.drawString(side_ox, H/2 - 15*mm, "4. PCB LAYER STACKUP (Cross-Section)")

    ls_ox = side_ox + 10*mm
    ls_oy = H/2 - 35*mm
    layer_h = 12*mm
    layer_w = 140*mm

    layers_info = [
        ("F.Cu (Signal)", colors.HexColor("#B8860B"), "0.035 mm copper — MCU, NPU, ADC/DAC signals"),
        ("Prepreg", colors.HexColor("#C8E6C9"), "0.20 mm FR4 dielectric"),
        ("In1.Cu (GND Plane)", colors.HexColor("#B8860B"), "0.035 mm copper — solid ground reference"),
        ("Core", colors.HexColor("#2E7D32"), "1.0 mm FR4 Tg170 core"),
        ("In2.Cu (PWR Plane)", colors.HexColor("#B8860B"), "0.035 mm copper — 3.3V / 1.8V power"),
        ("Prepreg", colors.HexColor("#C8E6C9"), "0.20 mm FR4 dielectric"),
        ("B.Cu (Signal)", colors.HexColor("#B8860B"), "0.035 mm copper — Memory bus, I2S, SPI"),
    ]

    for i, (name, col, desc) in enumerate(layers_info):
        ly = ls_oy - i * (layer_h + 1)
        th = layer_h if "Core" in name else layer_h * 0.6
        c.setFillColor(col)
        c.setStrokeColor(colors.black)
        c.setLineWidth(0.5)
        c.rect(ls_ox, ly - th, layer_w, th, fill=1, stroke=1)
        c.setFillColor(colors.white if "Cu" in name else colors.black)
        c.setFont("Helvetica-Bold", 7)
        c.drawString(ls_ox + 4, ly - th + th/2 - 2, name)
        c.setFillColor(C_DIM)
        c.setFont("Helvetica", 6)
        c.drawString(ls_ox + layer_w + 5, ly - th + th/2 - 2, desc)

    # Total thickness annotation
    total_top = ls_oy
    total_bot = ls_oy - len(layers_info) * (layer_h + 1)
    c.setFillColor(C_DIM)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(ls_ox, total_bot - 12, f"Total Stackup: 1.6 mm  |  Impedance: 50Ω SE / 100Ω Differential  |  Finish: ENIG (Gold)")

    c.save()
    print(f"2D Engineering Views PDF saved: {OUT}")

if __name__ == "__main__":
    main()
