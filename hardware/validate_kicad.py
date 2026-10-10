import sys
import os

def check_parens(filepath):
    if not os.path.exists(filepath):
        print(f"MISSING: {filepath}")
        return False
        
    text = open(filepath, 'r').read()
    
    # 1. Check paren balance
    opens = text.count('(')
    closes = text.count(')')
    if opens != closes:
        print(f"ERROR: {os.path.basename(filepath)} has unbalanced parens! Opens: {opens}, Closes: {closes}")
        return False
        
    # 2. Check for empty strings in places that might break
    if '""' in text:
        pass # Empty strings can be valid in some places like net_name
        
    # 3. Check for specific KiCad structure requirements
    if filepath.endswith('.kicad_sch'):
        if not text.strip().startswith('(kicad_sch'):
            print(f"ERROR: {os.path.basename(filepath)} does not start with (kicad_sch")
            return False
        if '(sheet_instances' not in text:
            print(f"ERROR: {os.path.basename(filepath)} missing sheet_instances")
            return False
            
    if filepath.endswith('.kicad_pcb'):
        if not text.strip().startswith('(kicad_pcb'):
            print(f"ERROR: {os.path.basename(filepath)} does not start with (kicad_pcb")
            return False
        if '(layers' not in text:
            print(f"ERROR: {os.path.basename(filepath)} missing layers definition")
            return False
            
    # 4. Check for known syntax errors previously encountered
    if '(fill (type none))' in text and filepath.endswith('.kicad_pcb'):
        # Wait, gr_rect uses (fill none) in our pcb generator now.
        pass
        
    if '(justify center)' in text:
        print(f"ERROR: {os.path.basename(filepath)} contains invalid (justify center)")
        return False
        
    print(f"OK: {os.path.basename(filepath)} looks structurally sound.")
    return True

all_ok = True
files = [
    '/Users/arpankailashgupta/Desktop/kicad/defence_anc.kicad_sch',
    '/Users/arpankailashgupta/Desktop/kicad/defence_anc.kicad_pcb',
    '/Users/arpankailashgupta/Desktop/kicad/defence_anc.kicad_pro'
]
for f in files:
    if not check_parens(f):
        all_ok = False
        
sys.exit(0 if all_ok else 1)
