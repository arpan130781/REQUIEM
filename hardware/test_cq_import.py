import cadquery as cq

try:
    print("Exporting pro-routed PCB to STEP using KiCad CLI...")
    import subprocess
    subprocess.run([
        "/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli",
        "pcb", "export", "step", "--force", "--subst-models",
        "-o", "/Users/arpankailashgupta/Desktop/kicad/defence_anc_pro_routed.step",
        "/Users/arpankailashgupta/Desktop/kicad/defence_anc_pro_routed.kicad_pcb"
    ], check=True)
    
    print("Importing STEP to CadQuery...")
    pcb = cq.importers.importStep("/Users/arpankailashgupta/Desktop/kicad/defence_anc_pro_routed.step")
    
    # Get bounding box to center it automatically
    bb = pcb.val().BoundingBox()
    cx = (bb.xmin + bb.xmax) / 2
    cy = (bb.ymin + bb.ymax) / 2
    cz = (bb.zmin + bb.zmax) / 2
    print(f"PCB Bounding Box: X({bb.xmin:.1f} to {bb.xmax:.1f}), Y({bb.ymin:.1f} to {bb.ymax:.1f}), Z({bb.zmin:.1f} to {bb.zmax:.1f})")
    print(f"Center: {cx:.1f}, {cy:.1f}, {cz:.1f}")
except Exception as e:
    print("Error:", e)
