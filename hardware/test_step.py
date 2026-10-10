import cadquery as cq

try:
    pcb = cq.importers.importStep("/Users/arpankailashgupta/Desktop/kicad/defence_anc_3D.step")
    bb = pcb.val().BoundingBox()
    print(f"PCB Bounding Box: X({bb.xmin:.1f} to {bb.xmax:.1f}), Y({bb.ymin:.1f} to {bb.ymax:.1f}), Z({bb.zmin:.1f} to {bb.zmax:.1f})")
except Exception as e:
    print("Error:", e)
