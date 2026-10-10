import os
import sys

content = open('/Users/arpankailashgupta/Desktop/kicad/generate_pdfs.py').read()
start_idx = content.find("def build_teammate():")

new_func = '''def build_teammate():
    path = os.path.join(OUT_DIR, "Teammate_Embedded_Summary.pdf")
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import Image, PageBreak
    
    W, H = A4
    doc = SimpleDocTemplate(path, pagesize=A4,
        leftMargin=2.0*cm, rightMargin=2.0*cm,
        topMargin=2.0*cm,  bottomMargin=2.0*cm,
        title="Embedded System Brief",
        author="Defence AI Systems")
    PW = W - 4.0*cm
    story = []

    def add_heading(text):
        story.append(sp(10))
        story.append(Paragraph(f"<b>{text}</b>", S("Heading2", fontSize=13, textColor=C_BLUE, spaceBefore=10, spaceAfter=6)))

    def add_text(text):
        story.append(Paragraph(text, S("Normal", fontSize=10, leading=15, textColor=C_DARK, spaceAfter=8)))

    # Title
    story.append(Paragraph("<b>DEFENCE AI-ANC SYSTEM</b>", S("Title", fontSize=22, textColor=C_NAVY, alignment=TA_CENTER)))
    story.append(Paragraph("Hardware & Embedded Systems Summary", S("Normal", fontSize=12, textColor=C_GRAY, alignment=TA_CENTER, spaceAfter=20)))
    story.append(hr(C_NAVY))
    story.append(sp(10))

    # 1. Overview
    add_heading("1. What Is This Project?")
    add_text("This project is a custom, military-grade circuit board with a built-in Artificial Intelligence chip. Its purpose is to perform <b>Active Noise Cancellation (ANC)</b> in real-time for soldiers and pilots in extreme environments.")
    add_text("Unlike standard noise-canceling headphones, this board uses a Deep Learning AI model specifically trained to erase loud, chaotic battlefield noises—such as <b>gunshots (165 dB), artillery blasts, and helicopter rotor wash</b>—so that voice communication remains crystal clear.")
    add_text("The entire process, from capturing the noise to outputting clean audio, happens in just <b>18 milliseconds</b>, so there is no noticeable delay.")

    # 2. How It Works
    add_heading("2. How It Works (The Signal Flow)")
    add_text("The system processes audio in a straight line from input to output:")
    steps = [
        "<b>1. Audio Input:</b> Two heavy-duty military microphones (capable of surviving 141 dB of sound) capture the voice and the background noise.",
        "<b>2. Pre-Amplifier:</b> An ultra-low-noise amplifier boosts the tiny microphone signals so they can be read accurately.",
        "<b>3. Digitization (ADC):</b> A 24-bit Analog-to-Digital Converter turns the audio into digital data that the computer chips can understand.",
        "<b>4. Central Processor (MCU):</b> An STM32 processor collects the data and instantly routes it to the AI chip.",
        "<b>5. AI Noise Removal (NPU):</b> The Kendryte K210 AI Chip runs our custom neural network. It isolates human speech and deletes the battlefield noise in just 12 milliseconds.",
        "<b>6. Audio Output (DAC & Amp):</b> The cleaned digital signal is converted back to analog audio, and a powerful 315W amplifier drives it into the user's headset."
    ]
    for step in steps:
        story.append(Paragraph(step, S("Normal", fontSize=10, leading=15, textColor=C_DARK, leftIndent=15, spaceAfter=6, bulletText="•")))

    story.append(PageBreak())

    # 3. Component Costs
    add_heading("3. Detailed Bill of Materials (BOM) & Costing")
    add_text("To build the first prototype, the total cost is approximately <b>$224.20 per unit</b>. When manufactured at scale (1,000+ units), the cost drops to about <b>$85.00 per unit</b>.")
    add_text("Below is the complete list of major active components used on the board, their exact part numbers, functions, and estimated prototype costs:")
    
    cost_data = [
        ["Ref", "Part Number", "Description", "Est. Cost"],
        ["PCB", "Custom 4-Layer", "FR4 Tg170, ENIG Finish (160x100mm)", "$45.00"],
        ["U1", "STM32H755ZIT6", "Dual-Core Central Microcontroller (MCU)", "$18.50"],
        ["U2", "Kendryte K210", "Artificial Intelligence Chip (NPU)", "$8.00"],
        ["U14", "IS42S32200L", "64Mb SDRAM (Memory for AI Models)", "$4.50"],
        ["U13", "W25Q128", "128Mb SPI Flash (Storage)", "$1.80"],
        ["MK1,2", "ICS-40300 (x2)", "Military MEMS Microphones (141dB SPL)", "$2.40"],
        ["U4", "INA217", "Low-Noise Microphone Pre-Amplifier", "$6.80"],
        ["U18", "MAX7401", "8th-Order Low-Pass Filter", "$4.10"],
        ["U5", "ADS1274", "24-bit 144kSPS Analog-to-Digital Converter", "$28.00"],
        ["U3", "CS4270", "Digital Audio Codec", "$8.50"],
        ["U10", "PCM1794A", "24-bit Digital-to-Analog Converter (DAC)", "$9.80"],
        ["U9", "TPA3255", "315W Class-D Audio Power Amplifier", "$12.50"],
        ["U6", "TPS65217", "Power Management IC (PMIC)", "$4.20"],
        ["U7, U8", "TLV1117 Series", "3.3V and 1.8V Linear Voltage Regulators", "$1.70"],
        ["U11", "SP3485", "RS-485 Communication Transceiver", "$2.50"],
        ["U12", "TCAN1044", "CAN FD Communication Transceiver", "$2.50"],
        ["U15", "ICM-42688", "6-Axis IMU (Vibration Tracking)", "$2.90"],
        ["U16", "BMP388", "Barometric Pressure Sensor (Wind Tracking)", "$2.20"],
        ["Misc", "Passives/Conn", "Resistors, Capacitors, Connectors", "$18.30"]
    ]
    
    t = Table(cost_data, colWidths=[1.8*cm, 3.5*cm, PW-7.3*cm, 2*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), C_NAVY),
        ("TEXTCOLOR", (0,0), (-1,0), C_WHITE),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("ALIGN", (3,0), (3,-1), "RIGHT"),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [C_WHITE, C_LIGHT]),
        ("GRID", (0,0), (-1,-1), 0.5, C_SILVER),
        ("PADDING", (0,0), (-1,-1), 5),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("FONTSIZE", (0,0), (-1,-1), 9),
    ]))
    story.append(sp(6))
    story.append(t)
    story.append(sp(15))

    # 4. Durability
    add_heading("4. Military Durability & Standards")
    add_text("Because this hardware is used in defense applications, it is built to survive extreme conditions:")
    
    mil = [
        "<b>MIL-STD-810H:</b> Rated to survive temperatures from -40°C to +85°C, as well as thermal shock, extreme humidity, and heavy vibration.",
        "<b>IP67 Waterproofing:</b> The entire circuit board is housed inside a sealed Hammond aluminium enclosure with waterproof military connectors.",
        "<b>Conformal Coating:</b> After the chips are soldered on, the board is sprayed with a special chemical layer (Humiseal 1A33) that prevents dust or condensation from causing electrical shorts.",
        "<b>ITAR Controlled:</b> The design contains restricted defense technology, so the board itself has 'ITAR CONTROLLED' printed on it in silkscreen."
    ]
    for item in mil:
        story.append(Paragraph(item, S("Normal", fontSize=10, leading=14, textColor=C_DARK, leftIndent=15, spaceAfter=6, bulletText="•")))

    doc.build(story)
    print(f"Teammate PDF saved: {path}")
    return path
'''

content = content[:start_idx] + new_func + content[content.find('if __name__ == "__main__":'):]

with open('/Users/arpankailashgupta/Desktop/kicad/generate_pdfs.py', 'w') as f:
    f.write(content)

print("generate_pdfs.py rewritten to remove image and add detailed BOM.")
