#!/usr/bin/env python3
import cadquery as cq
from generate_full_3d import make_pcb_assembly, make_enclosure, make_headset, make_jetson, make_ref_mic, make_cable

# Rebuild assembly
final = cq.Assembly()
encl = make_enclosure()
pcb = make_pcb_assembly()
headset = make_headset()
jetson = make_jetson()
ref_mic = make_ref_mic()

final.add(encl, name="wearable_enclosure", loc=cq.Location((0, 0, 0)))
final.add(pcb, name="custom_pcb", loc=cq.Location((0, 0, -2)))
final.add(headset, name="military_headset", loc=cq.Location((0, 0, 120)))
final.add(jetson, name="jetson_base_station", loc=cq.Location((250, 0, 36)))
final.add(ref_mic, name="reference_microphone", loc=cq.Location((-250, 0, 0)))

c1 = cq.Workplane("XY").cylinder(100, 2.5)
final.add(c1, name="cable_headset", loc=cq.Location((0, 50, 60)), color=cq.Color(0.1, 0.1, 0.1, 1))
c2 = cq.Workplane("XY").cylinder(200, 3)
final.add(c2, name="cable_jetson", loc=cq.Location((125, 0, 12.5), (0, 90, 0)), color=cq.Color(0.1, 0.1, 0.1, 1))
c3 = cq.Workplane("XY").cylinder(200, 2)
final.add(c3, name="cable_ref_mic", loc=cq.Location((-125, 0, 12.5), (0, 90, 0)), color=cq.Color(0.5, 0.5, 0.5, 1))

# Export to SVG for the presentation
final.save("/Users/arpankailashgupta/Desktop/kicad/Defence_ANC_System_Render.svg")
print("Saved SVG render")
