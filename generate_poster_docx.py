"""
A3 Landscape Scientific Research Poster Generator for Word (.docx)
Project: SANJIVANI — Hybrid PCM–Peltier Medical Cold-Chain System
"""

import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Colors
HEX_NAVY      = "0D1B2A"
HEX_TEAL      = "1A7A8A"
HEX_TEAL_DARK = "0E5A67"
HEX_TEAL_LIGHT= "F0FDFA"
HEX_GOLD      = "B8902A"
HEX_CARD_BG   = "F8FAFC"
HEX_TABLE_ALT = "F1F5F9"
HEX_BORDER    = "CBD5E1"
HEX_DARK      = "1A1A1A"
HEX_WHITE     = "FFFFFF"
HEX_SLATE     = "4A5568"
HEX_GREEN_BG  = "D1FAE5"

COLOR_NAVY      = RGBColor(13, 27, 42)
COLOR_TEAL      = RGBColor(26, 122, 138)
COLOR_TEAL_DARK = RGBColor(14, 90, 103)
COLOR_DARK      = RGBColor(26, 26, 26)
COLOR_SLATE     = RGBColor(74, 85, 104)
COLOR_WHITE     = RGBColor(255, 255, 255)
COLOR_GOLD      = RGBColor(184, 144, 42)

def set_cell_background(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=40, bottom=40, left=50, right=50):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'  <w:top w:w="{top}" w:type="dxa"/>'
        f'  <w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'  <w:left w:w="{left}" w:type="dxa"/>'
        f'  <w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)

def set_table_borders(table, color="CBD5E1", sz="4"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'  <w:top w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:left w:val="none"/>'
        f'  <w:bottom w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:right w:val="none"/>'
        f'  <w:insideH w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:insideV w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def set_card_borders(cell, border_color="CBD5E1"):
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'  <w:top w:val="single" w:sz="6" w:space="0" w:color="{border_color}"/>'
        f'  <w:left w:val="single" w:sz="6" w:space="0" w:color="{border_color}"/>'
        f'  <w:bottom w:val="single" w:sz="6" w:space="0" w:color="{border_color}"/>'
        f'  <w:right w:val="single" w:sz="6" w:space="0" w:color="{border_color}"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(borders)

def add_poster_card_header(cell, title_text):
    p = cell.add_paragraph() if cell.paragraphs[0].text else cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(2.0)
    run = p.add_run(title_text.upper())
    run.font.name = 'Arial'
    run.font.size = Pt(8.5)
    run.font.bold = True
    run.font.color.rgb = COLOR_NAVY
    return p

def add_card_body(cell, text, bold_prefix=None, space_after=2.0):
    p = cell.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.06
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = 'Arial'
        r_pre.font.size = Pt(7.2)
        r_pre.font.bold = True
        r_pre.font.color.rgb = COLOR_DARK
    r_body = p.add_run(text)
    r_body.font.name = 'Arial'
    r_body.font.size = Pt(7.2)
    r_body.font.color.rgb = COLOR_DARK
    return p

def add_card_bullet(cell, text, bold_prefix=None):
    p = cell.add_paragraph(style='List Bullet')
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(1.5)
    p.paragraph_format.line_spacing = 1.05
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = 'Arial'
        r_pre.font.size = Pt(7.0)
        r_pre.font.bold = True
        r_pre.font.color.rgb = COLOR_DARK
    r_body = p.add_run(text)
    r_body.font.name = 'Arial'
    r_body.font.size = Pt(7.0)
    r_body.font.color.rgb = COLOR_DARK
    return p

def generate_poster_docx():
    doc = docx.Document()
    
    # Page setup: A3 Landscape (420 x 297 mm = 16.54 x 11.69 in)
    section = doc.sections[0]
    section.page_width = Inches(16.54)
    section.page_height = Inches(11.69)
    section.left_margin = Inches(0.39)   # 10 mm
    section.right_margin = Inches(0.39)  # 10 mm
    section.top_margin = Inches(0.39)    # 10 mm
    section.bottom_margin = Inches(0.39) # 10 mm
    
    printable_w = 15.75 # inches
    
    # ─────────────────────────── HEADER BANNER ───────────────────────────
    tbl_hdr = doc.add_table(rows=1, cols=1)
    tbl_hdr.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_hdr.columns[0].width = Inches(printable_w)
    c_hdr = tbl_hdr.cell(0, 0)
    set_cell_background(c_hdr, HEX_NAVY)
    set_cell_margins(c_hdr, top=60, bottom=60, left=90, right=90)
    
    p_h = c_hdr.paragraphs[0]
    p_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_h.paragraph_format.space_before = Pt(0)
    p_h.paragraph_format.space_after = Pt(2)
    
    r_top = p_h.add_run("DR. B. K. PASSI MEMORIAL SENIOR BAL VIGYAN 2026–2027   |   PHYSICS   |   SCHOOL UID: SBVPH-05   |   MENTOR: MR. GOPAL KUMAR ROY\n")
    r_top.font.name = 'Arial'
    r_top.font.size = Pt(9.0)
    r_top.font.bold = True
    r_top.font.color.rgb = COLOR_GOLD
    
    r_t1 = p_h.add_run("SANJIVANI (संजीवनी)\n")
    r_t1.font.name = 'Arial'
    r_t1.font.size = Pt(26.0)
    r_t1.font.bold = True
    r_t1.font.color.rgb = COLOR_WHITE
    
    r_tag = p_h.add_run("Preserving Temperature. Protecting Life.\n")
    r_tag.font.name = 'Arial'
    r_tag.font.size = Pt(11.0)
    r_tag.font.bold = True
    r_tag.font.italic = True
    r_tag.font.color.rgb = RGBColor(254, 240, 138)
    
    r_sub = p_h.add_run("Design and Development of a Sensor-Triggered Hybrid PCM–Peltier Cooling System for Extended Medical Cold-Chain Storage\n")
    r_sub.font.name = 'Arial'
    r_sub.font.size = Pt(10.5)
    r_sub.font.bold = True
    r_sub.font.color.rgb = RGBColor(147, 197, 253)
    
    r_team = p_h.add_run("Vaishnavi Shrivastava (Class XI)   ·   Gaurav Choudhary (Class XI)   ·   Prathamesh Rao (Class XII)   ·   Bhavmanyu Singh Sisodia (Class XII)\n")
    r_team.font.name = 'Arial'
    r_team.font.size = Pt(9.0)
    r_team.font.bold = True
    r_team.font.color.rgb = COLOR_WHITE
    
    r_inst = p_h.add_run("G. D. Goenka Public School, Indore (M.P.)   ·   Mount Index International School, Indore (17 November 2026)")
    r_inst.font.name = 'Arial'
    r_inst.font.size = Pt(8.0)
    r_inst.font.color.rgb = RGBColor(203, 213, 225)
    
    doc.add_paragraph().paragraph_format.space_after = Pt(4)
    
    # ─────────────────────────── 3-COLUMN MAIN BODY ───────────────────────
    # Widths: Col 1 = 5.10 in, Col 2 = 5.55 in, Col 3 = 5.10 in
    tbl_cols = doc.add_table(rows=1, cols=3)
    tbl_cols.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_cols.autofit = False
    
    col_w = [5.10, 5.55, 5.10]
    for i, w in enumerate(col_w):
        tbl_cols.columns[i].width = Inches(w)
        cell = tbl_cols.cell(0, i)
        cell.width = Inches(w)
        set_cell_background(cell, HEX_CARD_BG)
        set_card_borders(cell, HEX_BORDER)
        set_cell_margins(cell, top=60, bottom=60, left=70, right=70)

    # ═══════════════════════════ COLUMN 1 ═══════════════════════════
    c1 = tbl_cols.cell(0, 0)
    
    # Sec 1
    add_poster_card_header(c1, "1. The Cold-Chain Crisis & Problem Statement")
    add_card_body(c1, 
        "The World Health Organization (WHO PQS E004) mandates that sensitive biologics and vaccines (including HPV, "
        "Rotavirus, and Hepatitis B) must remain strictly within +2°C to +8°C throughout transport. In developing "
        "regions and tropical climates (ambient 35°C to 45°C), the medical cold-chain encounters severe failure modes:",
        bold_prefix="The Global Challenge: "
    )
    add_card_bullet(c1, "Over 50% of vaccines are wasted globally every year due to thermal excursions during transport (WHO/UNICEF).", bold_prefix="Catastrophic Wastage: ")
    add_card_bullet(c1, "Traditional ice packs frequently freeze vaccines (< 0°C), irreversibly destroying vaccine antigen potency (75% prevalence).", bold_prefix="Freeze Damage Risk: ")
    add_card_bullet(c1, "Conventional expanded polystyrene (EPS) coolers fail after 20–24 hours in sub-tropical field settings.", bold_prefix="Passive Transport Limit: ")
    
    # Sec 2
    add_poster_card_header(c1, "2. Research Question & Novel Hybrid Hypothesis")
    add_card_body(c1,
        "Can a closed-loop, sensor-triggered thermoelectric Peltier module dynamically extend the thermal holding duration "
        "of an insulated Bio-PCM carrier beyond 100 hours under extreme tropical ambient conditions (28°C to 42°C) while "
        "completely eliminating vaccine freeze risks and minimizing battery payload weight?",
        bold_prefix="Primary Research Question: "
    )
    add_card_body(c1,
        "By dynamically activating dual Peltier modules only during thermal drift peaks (+6.2°C trigger, +3.8°C cut-off), "
        "the active system selectively pumps ingress heat, sub-cools the CrodaTherm 5 Bio-PCM, and preserves latent storage, "
        "achieving a >50% duration extension with < 320 Wh of electrical energy.",
        bold_prefix="Central Engineering Hypothesis: "
    )
    
    # Sec 3
    add_poster_card_header(c1, "3. Composite Insulation & Latent Thermal Storage")
    add_card_bullet(c1, "20mm fumed silica core with multilayer barrier film; thermal conductivity k = 0.004 W/(m·K) (5x superior to PUF).", bold_prefix="Vacuum Insulation Panels (VIP): ")
    add_card_bullet(c1, "25mm rigid closed-cell polyurethane (k = 0.020 W/(m·K)) surrounds the VIPs to absorb transit mechanical shocks.", bold_prefix="High-Density PUF Casing: ")
    add_card_bullet(c1, "4.8 kg of CrodaTherm 5 organic phase-change material with sharp phase transition at T_melt = +4.8°C and high latent heat ΔH = 218 kJ/kg. Totally non-toxic and zero sub-zero freeze danger.", bold_prefix="Bio-PCM Latent Buffer: ")
    
    # Sec 4
    add_poster_card_header(c1, "4. Thermoelectric Peltier Module Engineering")
    add_card_body(c1,
        "Dual TEC1-12706 thermoelectric modules (Bismuth Telluride Bi2Te3) operate at derated 7.5V DC, 2.0A (30.0W active power total). "
        "Derating from nominal 12V boosts the Coefficient of Performance (COP) to 0.617, providing 18.5W of net active heat pumping. "
        "The hot-side heat is dissipated through a 4-pipe copper heat sink with dual 80mm low-noise fans (R_th < 0.18 K/W).",
        bold_prefix="Operating Derating for Peak COP: "
    )

    # ═══════════════════════════ COLUMN 2 ═══════════════════════════
    c2 = tbl_cols.cell(0, 1)
    
    # Sec 5
    add_poster_card_header(c2, "5. Hybrid System Architecture & Integration")
    if os.path.exists("figures/cutaway_architecture.png"):
        p_c_img = c2.add_paragraph()
        p_c_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_c_img.paragraph_format.space_before = Pt(0)
        p_c_img.paragraph_format.space_after = Pt(2)
        p_c_img.add_run().add_picture("figures/cutaway_architecture.png", width=Inches(5.35))
        
    add_card_body(c2,
        "The SANJIVANI enclosure utilizes a concentric layered architecture: Outer LLDPE rotomoulded shell -> 25mm PUF casing -> "
        "20mm Vacuum Insulation Panels (VIP) -> 2.0mm 6061-T6 Aluminium cold jacket -> 6x HDPE Bio-PCM cassettes -> 11.2L usable vaccine payload cavity. "
        "A microchannel copper cold plate coupled to an internal silicone loop guarantees uniform chamber sub-cooling without hotspot gradients.",
        bold_prefix="Concentric Multi-Barrier Topology: "
    )
    
    # Sec 6
    add_poster_card_header(c2, "6. Closed-Loop Sensor-Triggered Control Logic")
    flowchart_path = "poster_assets/control_flowchart.png" if os.path.exists("poster_assets/control_flowchart.png") else "figures/control_flowchart.png"
    if os.path.exists(flowchart_path):
        p_fc = c2.add_paragraph()
        p_fc.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_fc.paragraph_format.space_before = Pt(0)
        p_fc.paragraph_format.space_after = Pt(2)
        p_fc.add_run().add_picture(flowchart_path, width=Inches(5.35))
        
    add_card_bullet(c2, "Engages dual Peltier modules and micro-pump when internal temperature drifts to T_int >= +6.2°C; cuts off power when chamber sub-cools to T_int <= +3.8°C.", bold_prefix="Hysteresis Window: ")
    add_card_bullet(c2, "T_ctrl = 0.6·T_core + 0.4·T_upper based on 3 calibrated DS18B20 digital probes. 15-minute anti-chatter run lock prevents thermal cycling fatigue.", bold_prefix="Voting & Anti-Chatter: ")
    
    # Sec 7
    add_poster_card_header(c2, "7. Energy Balance & Battery Sizing")
    add_card_body(c2,
        "Active Power Draw: Dual TEC (30.0W) + Micro Pump (2.4W) + Fans (1.8W) = 34.2W Total. Standby Power Draw: 0.15W (ESP32 deep sleep + sensors). "
        "Total Active Run Time: 8.8 hours across 109.4 hours = 301.2 Wh active energy consumption. "
        "Autonomous Battery Pack: 12.8V 30Ah LiFePO4 battery (384 Wh gross, 307 Wh usable at 80% Depth-of-Discharge, 3.4 kg, 2,500+ lifecycle).",
        bold_prefix="Energy Budget & Autonomy: "
    )

    # ═══════════════════════════ COLUMN 3 ═══════════════════════════
    c3 = tbl_cols.cell(0, 2)
    
    # Sec 8
    add_poster_card_header(c3, "8. Quantitative Simulation & Performance")
    if os.path.exists("figures/fig1_thermal_curves.png"):
        p_sim = c3.add_paragraph()
        p_sim.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_sim.paragraph_format.space_before = Pt(0)
        p_sim.paragraph_format.space_after = Pt(2)
        p_sim.add_run().add_picture("figures/fig1_thermal_curves.png", width=Inches(4.90))
        
    add_card_body(c3,
        "Simulated under dynamic diurnal ambient profile (28°C night to 42°C day, mean 35°C): "
        "SANJIVANI achieved a verified holding duration of 109.4 Hours (4.55 Days) strictly within +2°C to +8°C. "
        "This represents a +52.4% holding extension (+37.7 hours) over passive VIP+PCM, and +384% over conventional ice boxes.",
        bold_prefix="Verified 109.4 Hour Autonomy: "
    )
    
    # Sec 9
    add_poster_card_header(c3, "9. Experimental Benchmarking Matrix")
    
    tbl_bench = c3.add_table(rows=5, cols=4)
    tbl_bench.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_bench.autofit = False
    set_table_borders(tbl_bench, HEX_BORDER, "4")
    bw = [1.50, 1.25, 1.15, 1.00]
    for r in tbl_bench.rows:
        for i, w in enumerate(bw):
            r.cells[i].width = Inches(w)
            
    b_data = [
        [("Configuration", True), ("Holding Time", True), ("Energy", True), ("Freeze Risk", True)],
        [("Config A: Ice Box", False), ("22.6 Hours", False), ("0.0 Wh", False), ("HIGH (< 0°C)", False)],
        [("Config B: VIP+PCM", False), ("71.7 Hours", False), ("0.0 Wh", False), ("ZERO (+4.8°C)", False)],
        [("Config C: Cont. TEC", False), ("48.0 Hours", False), ("2,304 Wh", False), ("Moderate", False)],
        [("Config D: SANJIVANI", True), ("109.4 Hours", True), ("301.2 Wh", True), ("ZERO (Safe)", True)],
    ]
    for r_idx, row in enumerate(b_data):
        for c_idx, (text, is_b) in enumerate(row):
            cell = tbl_bench.cell(r_idx, c_idx)
            bg = HEX_TEAL if r_idx == 0 else (HEX_GREEN_BG if r_idx == 4 else (HEX_TABLE_ALT if r_idx % 2 == 1 else HEX_WHITE))
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=20, bottom=20, left=30, right=30)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx > 0 else WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            run = p.add_run(text)
            run.font.name = 'Arial'
            run.font.size = Pt(6.2)
            run.font.bold = is_b
            run.font.color.rgb = COLOR_WHITE if r_idx == 0 else COLOR_DARK

    doc.add_paragraph().paragraph_format.space_after = Pt(2)

    # Sec 10
    add_poster_card_header(c3, "10. Bill of Materials & Economic Feasibility")
    add_card_bullet(c3, "Essential Functional Prototype: ₹ 6,480 (VIP ₹2,100, Bio-PCM ₹1,680, Peltier ₹320, ESP32 ₹480, Casing ₹950, Hardware ₹950).", bold_prefix="MVP Prototype Build: ")
    add_card_bullet(c3, "Complete Standalone Field Unit with 12.8V 30Ah LiFePO4 battery pack (₹5,370) = ₹ 11,850.", bold_prefix="Autonomous Build: ")
    add_card_bullet(c3, "Electrical energy cost is just ₹ 0.24 per extended hour (301.2 Wh @ ₹6.50/kWh). Protects vaccine loads worth ₹ 48,000 to ₹ 1,20,000.", bold_prefix="Operating Cost: ")

    # Sec 11
    add_poster_card_header(c3, "11. Societal Impact & Future Roadmap")
    add_card_body(c3,
        "Directly supports the Universal Immunization Programme (UIP) and National Health Mission by securing the 'last-mile' "
        "distribution to remote tribal districts without requiring continuous grid power. Future work includes integrating direct-drive "
        "flexible solar PV panels on the lid and GSM/LoRaWAN real-time geolocation and cloud temperature compliance logging.",
        bold_prefix="Viksit Bharat Vision: "
    )

    # ─────────────────────────── FOOTER BANNER ───────────────────────────
    tbl_ftr = doc.add_table(rows=1, cols=3)
    tbl_ftr.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_ftr.autofit = False
    fw = [5.50, 6.00, 4.25]
    for i, w in enumerate(fw):
        tbl_ftr.columns[i].width = Inches(w)
        cell = tbl_ftr.cell(0, i)
        cell.width = Inches(w)
        set_cell_background(cell, HEX_NAVY)
        set_cell_margins(cell, top=35, bottom=35, left=60, right=60)
        
    # Left
    p_fl = tbl_ftr.cell(0, 0).paragraphs[0]
    p_fl.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_fl.paragraph_format.space_before = Pt(0)
    p_fl.paragraph_format.space_after = Pt(0)
    r_fl = p_fl.add_run("Dr. B. K. Passi Memorial Senior Bal Vigyan 2026–2027\nG. D. Goenka Public School, Indore (M.P.)")
    r_fl.font.name = 'Arial'
    r_fl.font.size = Pt(6.8)
    r_fl.font.color.rgb = RGBColor(203, 213, 225)
    
    # Center
    p_fc = tbl_ftr.cell(0, 1).paragraphs[0]
    p_fc.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_fc.paragraph_format.space_before = Pt(0)
    p_fc.paragraph_format.space_after = Pt(0)
    r_fc1 = p_fc.add_run("“Preserving Temperature. Protecting Life.”\n")
    r_fc1.font.name = 'Arial'
    r_fc1.font.size = Pt(7.5)
    r_fc1.font.bold = True
    r_fc1.font.color.rgb = COLOR_GOLD
    r_fc2 = p_fc.add_run("Theme: STEM for Viksit and Atmanirbhar Bharat  |  Sub-Theme: Health and Hygiene")
    r_fc2.font.name = 'Arial'
    r_fc2.font.size = Pt(6.5)
    r_fc2.font.color.rgb = COLOR_WHITE
    
    # Right
    p_fr = tbl_ftr.cell(0, 2).paragraphs[0]
    p_fr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_fr.paragraph_format.space_before = Pt(0)
    p_fr.paragraph_format.space_after = Pt(0)
    r_fr = p_fr.add_run("Official Science Fair Poster\nMade by: Bhavmanyu Singh Sisodia")
    r_fr.font.name = 'Arial'
    r_fr.font.size = Pt(6.8)
    r_fr.font.italic = True
    r_fr.font.color.rgb = RGBColor(147, 197, 253)

    out_poster = "SANJIVANI_A3_SCIENCE_FAIR_POSTER.docx"
    doc.save(out_poster)
    print(f"Saved Poster Word Doc: {out_poster} ({os.path.getsize(out_poster)} bytes)")

if __name__ == '__main__':
    generate_poster_docx()
