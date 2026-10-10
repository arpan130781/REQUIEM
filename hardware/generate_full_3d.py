#!/usr/bin/env python3
"""
Generate a complete 3D CAD model of the Defence AI-ANC System.
Imports the ACTUAL KiCad PCB 3D model and places it inside the enclosure.
"""
import cadquery as cq
import os

OUT = "/Users/arpankailashgupta/Desktop/kicad/Defence_ANC_Full_System.step"
KICAD_PCB_STEP = "/Users/arpankailashgupta/Desktop/kicad/defence_anc_3D.step"

# ════════════════════════════════════════════════════
# 1. ACTUAL KICAD PCB
# ════════════════════════════════════════════════════
def make_pcb_assembly():
    # Import the beautiful 3D STEP file generated directly by KiCad!
    print("Loading KiCad PCB STEP file (14MB)... this might take a moment.")
    pcb = cq.importers.importStep(KICAD_PCB_STEP)
    assy = cq.Assembly()
    # The KiCad STEP has origin at top-left. Translate to center it.
    assy.add(pcb, name="real_kicad_pcb", loc=cq.Location((-80, 50, 0)))
    return assy

# ════════════════════════════════════════════════════
# 2. SEALED MILITARY ENCLOSURE (Hammond-style)
# ════════════════════════════════════════════════════
def make_enclosure():
    ow, od, oh = 180, 120, 25
    wall = 3
    outer = cq.Workplane("XY").box(ow, od, oh)
    inner = cq.Workplane("XY").box(ow - 2*wall, od - 2*wall, oh - wall).translate((0, 0, wall/2))
    shell = outer.cut(inner)
    shell = shell.faces("<Y").workplane().pushPoints([(-40, 0), (40, 0)]).hole(12)
    lid = cq.Workplane("XY").box(ow, od, 3).translate((0, 0, oh/2 + 1.5))
    assy = cq.Assembly()
    assy.add(shell, name="enclosure_base", color=cq.Color(0.45, 0.48, 0.50, 1))
    assy.add(lid, name="enclosure_lid", color=cq.Color(0.50, 0.53, 0.55, 1))
    return assy, ow, od, oh

# ════════════════════════════════════════════════════
# 3. MILITARY HEADSET
# ════════════════════════════════════════════════════
def make_headset():
    assy = cq.Assembly()
    headband = (cq.Workplane("XZ")
        .moveTo(-80, 0).threePointArc((0, 50), (80, 0))
        .lineTo(80, -5).threePointArc((0, 45), (-80, -5))
        .close().extrude(15).translate((0, -7.5, 0)))
    assy.add(headband, name="headband", color=cq.Color(0.15, 0.15, 0.15, 1))
    
    left_cup = cq.Workplane("YZ").circle(40).extrude(25).translate((-80, 0, 0))
    left_pad = cq.Workplane("YZ").circle(42).circle(30).extrude(8).translate((-105, 0, 0))
    assy.add(left_cup, name="left_earcup", color=cq.Color(0.25, 0.30, 0.20, 1))
    assy.add(left_pad, name="left_pad", color=cq.Color(0.1, 0.1, 0.1, 1))
    
    right_cup = cq.Workplane("YZ").circle(40).extrude(25).translate((55, 0, 0))
    right_pad = cq.Workplane("YZ").circle(42).circle(30).extrude(8).translate((80, 0, 0))
    assy.add(right_cup, name="right_earcup", color=cq.Color(0.25, 0.30, 0.20, 1))
    assy.add(right_pad, name="right_pad", color=cq.Color(0.1, 0.1, 0.1, 1))
    
    boom = cq.Workplane("XY").circle(3).extrude(80).translate((-100, -25, 0))
    assy.add(boom, name="boom_arm", color=cq.Color(0.15, 0.15, 0.15, 1))
    mic_head = cq.Workplane("XY").circle(6).extrude(15).translate((-100, -25, 80))
    assy.add(mic_head, name="boom_mic", color=cq.Color(0.3, 0.3, 0.3, 1))
    return assy

# ════════════════════════════════════════════════════
# 4. NVIDIA JETSON AGX ORIN
# ════════════════════════════════════════════════════
def make_jetson():
    assy = cq.Assembly()
    body = cq.Workplane("XY").box(110, 110, 72)
    assy.add(body, name="jetson_body", color=cq.Color(0.15, 0.18, 0.15, 1))
    for i in range(10):
        fin = cq.Workplane("XY").box(100, 2, 15).translate((0, -45 + i*10, 72/2 + 7.5))
        assy.add(fin, name=f"fin_{i}", color=cq.Color(0.25, 0.25, 0.25, 1))
    led = cq.Workplane("XY").cylinder(2, 2).translate((-50, 0, 0))
    assy.add(led, name="jetson_led", color=cq.Color(0.0, 0.8, 0.0, 1))
    for i in range(3):
        port = cq.Workplane("XY").box(9, 5, 3.5).translate((-50 + 20*i, -55, -20))
        assy.add(port, name=f"usb_port_{i}", color=cq.Color(0.6, 0.6, 0.6, 1))
    return assy

# ════════════════════════════════════════════════════
# 5. REFERENCE MIC
# ════════════════════════════════════════════════════
def make_ref_mic_stand():
    assy = cq.Assembly()
    base = cq.Workplane("XY").cylinder(5, 50)
    assy.add(base, name="mic_base", color=cq.Color(0.2, 0.2, 0.2, 1))
    pole = cq.Workplane("XY").cylinder(200, 5).translate((0, 0, 105))
    assy.add(pole, name="mic_pole", color=cq.Color(0.3, 0.3, 0.3, 1))
    clip = cq.Workplane("XY").box(20, 20, 15).translate((0, 0, 210))
    assy.add(clip, name="mic_clip", color=cq.Color(0.15, 0.15, 0.15, 1))
    mic = cq.Workplane("XY").cylinder(40, 10).translate((0, 0, 240))
    assy.add(mic, name="ref_mic", color=cq.Color(0.4, 0.4, 0.4, 1))
    windscreen = cq.Workplane("XY").sphere(18).translate((0, 0, 265))
    assy.add(windscreen, name="windscreen", color=cq.Color(0.2, 0.2, 0.2, 1))
    return assy

# ════════════════════════════════════════════════════
# FINAL ASSEMBLY
# ════════════════════════════════════════════════════
def main():
    print("Building PCB assembly...")
    pcb_assy = make_pcb_assembly()
    
    print("Building enclosure...")
    encl_assy, ew, ed, eh = make_enclosure()
    
    print("Building headset...")
    headset_assy = make_headset()
    
    print("Building Jetson AGX Orin...")
    jetson_assy = make_jetson()
    
    print("Building reference mic stand...")
    mic_stand_assy = make_ref_mic_stand()
    
    print("Creating final assembly...")
    final = cq.Assembly()
    
    final.add(encl_assy, name="wearable_enclosure", loc=cq.Location((0, 0, 0)))
    final.add(pcb_assy, name="actual_kicad_pcb", loc=cq.Location((0, 0, 1)))  # slightly raised
    
    final.add(headset_assy, name="military_headset", loc=cq.Location((0, 0, 120)))
    final.add(jetson_assy, name="jetson_base_station", loc=cq.Location((250, 0, 36)))
    final.add(mic_stand_assy, name="reference_microphone", loc=cq.Location((-250, 0, 0)))
    
    c1 = cq.Workplane("XY").cylinder(100, 2.5)
    final.add(c1, name="cable_headset", loc=cq.Location((0, 50, 60)), color=cq.Color(0.1, 0.1, 0.1, 1))
    c2 = cq.Workplane("XY").cylinder(200, 3)
    final.add(c2, name="cable_jetson", loc=cq.Location((125, 0, 12.5), (0, 90, 0)), color=cq.Color(0.1, 0.1, 0.1, 1))
    c3 = cq.Workplane("XY").cylinder(200, 2)
    final.add(c3, name="cable_ref_mic", loc=cq.Location((-125, 0, 12.5), (0, 90, 0)), color=cq.Color(0.5, 0.5, 0.5, 1))
    
    print("Exporting massive STEP file...")
    final.save(OUT)
    
    fsize = os.path.getsize(OUT) / (1024*1024)
    print(f"\nDone! Full system 3D model updated: {OUT}")
    print(f"File size: {fsize:.1f} MB")

if __name__ == "__main__":
    main()
