"""
Perfect Visual Replica Word (.docx) Dossier Generator for SANJIVANI
Matches the official 25-page PDF report with 100% pixel-perfect visual fidelity.
"""

import os
import sys
import re
from xml.etree import ElementTree as ET
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.section import WD_SECTION_START
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

import build_complete_dossier as bcd
from reportlab.platypus import Paragraph, Table, Spacer, Image, HRFlowable

# ─────────────────────────── COLOR PALETTE ───────────────────────────
HEX_NAVY      = "0D1B2A"
HEX_TEAL      = "1A7A8A"
HEX_TEAL_DARK = "0E5A67"
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

def set_cell_margins(cell, top=40, bottom=40, left=60, right=60):
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

def parse_html_to_runs(text):
    text = text.replace('&nbsp;', ' ')
    text = text.replace('<br/>', '\n').replace('<br>', '\n')
    xml_str = f'<root>{text}</root>'
    xml_str = re.sub(r'&(?!amp;|lt;|gt;|quot;|apos;|#\d+;)', '&amp;', xml_str)
    try:
        root = ET.fromstring(xml_str)
    except Exception:
        text_clean = re.sub(r'<[^>]+>', '', text)
        return [(text_clean, {})]
    
    runs = []
    def traverse(node, state):
        cur_state = dict(state)
        tag = node.tag.lower()
        if tag in ('b', 'strong'):
            cur_state['bold'] = True
        elif tag in ('i', 'em'):
            cur_state['italic'] = True
        elif tag in ('sup', 'super'):
            cur_state['superscript'] = True
        elif tag == 'sub':
            cur_state['subscript'] = True
        elif tag == 'font':
            if 'color' in node.attrib:
                c = node.attrib['color'].lstrip('#')
                if len(c) == 6:
                    cur_state['color'] = c
        
        if node.text:
            runs.append((node.text, dict(cur_state)))
        for child in node:
            traverse(child, dict(cur_state))
            if child.tail:
                runs.append((child.tail, dict(cur_state)))
                
    if root.text:
        runs.append((root.text, {}))
    for child in root:
        traverse(child, {})
        if child.tail:
            runs.append((child.tail, {}))
    return runs

def apply_runs_to_para(p, runs, default_size=Pt(7.6), default_color=COLOR_DARK, default_bold=False):
    for text_part, state in runs:
        text_part = text_part.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
        run = p.add_run(text_part)
        run.font.name = 'Arial'
        run.font.size = default_size
        run.font.bold = state.get('bold', default_bold)
        run.font.italic = state.get('italic', False)
        if state.get('superscript', False):
            run.font.superscript = True
        if state.get('subscript', False):
            run.font.subscript = True
        if 'color' in state:
            c = state['color']
            run.font.color.rgb = RGBColor(int(c[:2], 16), int(c[2:4], 16), int(c[4:6], 16))
        else:
            run.font.color.rgb = default_color

def add_banner(doc, title_text):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    tbl.columns[0].width = Inches(6.85)
    cell = tbl.cell(0, 0)
    set_cell_background(cell, HEX_TEAL)
    set_cell_margins(cell, top=45, bottom=45, left=80, right=80)
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    
    clean_title = re.sub(r'<[^>]+>', '', title_text).strip().upper()
    run = p.add_run(clean_title)
    run.font.name = 'Arial'
    run.font.size = Pt(9.2)
    run.font.bold = True
    run.font.color.rgb = COLOR_WHITE
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(0)
    p_sp.paragraph_format.space_after = Pt(1.5)

def add_sec_head(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(3.5)
    p.paragraph_format.space_after = Pt(1.5)
    p.paragraph_format.keep_with_next = True
    runs = parse_html_to_runs(text)
    apply_runs_to_para(p, runs, default_size=Pt(8.4), default_color=COLOR_NAVY, default_bold=True)
    return p

def add_equation_box(doc, text):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.columns[0].width = Inches(6.85)
    cell = tbl.cell(0, 0)
    set_cell_background(cell, HEX_CARD_BG)
    set_cell_margins(cell, top=40, bottom=40, left=80, right=80)
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    runs = parse_html_to_runs(text)
    apply_runs_to_para(p, runs, default_size=Pt(8.0), default_color=COLOR_TEAL_DARK, default_bold=True)
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(0)
    p_sp.paragraph_format.space_after = Pt(1.5)

def add_body_para(doc, text, style_name='body'):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(2.0)
    p.paragraph_format.line_spacing = 1.08
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    
    font_size = Pt(8.2) if style_name == 'body_lg' else Pt(7.6)
    runs = parse_html_to_runs(text)
    apply_runs_to_para(p, runs, default_size=font_size, default_color=COLOR_DARK)
    return p

def add_bullet_para(doc, text):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(1.6)
    p.paragraph_format.line_spacing = 1.06
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    runs = parse_html_to_runs(text)
    apply_runs_to_para(p, runs, default_size=Pt(7.4), default_color=COLOR_DARK)
    return p

def add_ref_para(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(1.6)
    p.paragraph_format.line_spacing = 1.05
    p.paragraph_format.left_indent = Inches(0.20)
    p.paragraph_format.first_line_indent = Inches(-0.20)
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    runs = parse_html_to_runs(text)
    apply_runs_to_para(p, runs, default_size=Pt(7.0), default_color=COLOR_DARK)
    return p

def add_caption_para(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(1.8)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    runs = parse_html_to_runs(text)
    apply_runs_to_para(p, runs, default_size=Pt(6.8), default_color=COLOR_SLATE)
    return p

def add_pcm_diagram(doc):
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(1.5)
    p_title.paragraph_format.space_after = Pt(1.0)
    r = p_title.add_run("Figure 1 — Phase Change Material (Bio-PCM) Latent Heat Buffering Mechanism")
    r.font.name = 'Arial'
    r.font.size = Pt(7.0)
    r.font.bold = True
    r.font.color.rgb = COLOR_NAVY
    
    tbl = doc.add_table(rows=1, cols=3)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    set_table_borders(tbl, HEX_BORDER, "4")
    col_w = 6.85 / 3.0
    
    phases = [
        ("1. SOLID BIO-PCM", "BFDBFE", "Sensible Subcooling\nT < +4.8°C (Solid Matrix)", RGBColor(29, 78, 216)),
        ("2. PHASE TRANSITION", "A7F3D0", "Latent Heat Absorption\nT = +4.8°C (Isothermal Buffer)", RGBColor(6, 95, 70)),
        ("3. LIQUID STATE", "FDE68A", "Latent Reserve Exhausted\nT > +5.2°C (Sensible Warmup)", RGBColor(146, 64, 14)),
    ]
    for i, (title, bg, desc, tc) in enumerate(phases):
        tbl.columns[i].width = Inches(col_w)
        cell = tbl.cell(0, i)
        set_cell_background(cell, bg)
        set_cell_margins(cell, top=35, bottom=35, left=50, right=50)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(1)
        r1 = p.add_run(f"<b>{title}</b>\n")
        r1.font.name = 'Arial'
        r1.font.size = Pt(6.8)
        r1.font.bold = True
        r1.font.color.rgb = tc
        
        r2 = p.add_run(desc)
        r2.font.name = 'Arial'
        r2.font.size = Pt(6.0)
        r2.font.color.rgb = COLOR_DARK
        
    doc.add_paragraph().paragraph_format.space_after = Pt(1.5)

def add_peltier_diagram(doc):
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(1.5)
    p_title.paragraph_format.space_after = Pt(1.0)
    r = p_title.add_run("Figure 2 — Dual TEC1-12706 Thermoelectric Module: Active Heat Pumping Dynamics")
    r.font.name = 'Arial'
    r.font.size = Pt(7.0)
    r.font.bold = True
    r.font.color.rgb = COLOR_NAVY
    
    tbl = doc.add_table(rows=3, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    set_table_borders(tbl, HEX_BORDER, "4")
    tbl.columns[0].width = Inches(6.85)
    
    layers = [
        ("HOT SIDE — Thermal Dissipation: Q_hot = Q_cold + P_elec (to Fin Stack & Fan)", "FEE2E2", RGBColor(220, 38, 38)),
        ("Semiconductor Matrix: Bismuth Telluride (Bi2Te3) P-N Thermoelectric Semiconductor Matrix (Powered at 7.5V DC, 30W)", "F1F5F9", COLOR_SLATE),
        ("COLD SIDE — Heat Pumping Interface: Q_cold = 18.5 W (coupled to Al Cold Jacket)", "DBEAFE", RGBColor(29, 78, 216)),
    ]
    for i, (text, bg, tc) in enumerate(layers):
        cell = tbl.cell(i, 0)
        set_cell_background(cell, bg)
        set_cell_margins(cell, top=30, bottom=30, left=60, right=60)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        run = p.add_run(text)
        run.font.name = 'Arial'
        run.font.size = Pt(6.5)
        run.font.bold = True
        run.font.color.rgb = tc
        
    doc.add_paragraph().paragraph_format.space_after = Pt(1.5)

def render_table_flowable(doc, table_obj):
    has_images = False
    for row in table_obj._cellvalues:
        for cell in row:
            if isinstance(cell, Image):
                has_images = True
                break
                
    if has_images:
        tbl = doc.add_table(rows=len(table_obj._cellvalues), cols=len(table_obj._cellvalues[0]))
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        tbl.autofit = False
        tot_w = sum(table_obj._colWidths)
        for r_idx, row in enumerate(table_obj._cellvalues):
            for c_idx, cell in enumerate(row):
                w_in = (table_obj._colWidths[c_idx] / tot_w) * 6.85
                tbl.cell(r_idx, c_idx).width = Inches(w_in)
                p = tbl.cell(r_idx, c_idx).paragraphs[0]
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p.paragraph_format.space_before = Pt(0)
                p.paragraph_format.space_after = Pt(0)
                if isinstance(cell, Image):
                    img_w_in = cell.drawWidth / 72.0
                    if img_w_in > w_in - 0.1:
                        img_w_in = w_in - 0.1
                    img_src = getattr(cell, 'filename', getattr(cell, '_filename', None))
                    p.add_run().add_picture(img_src, width=Inches(img_w_in))
        doc.add_paragraph().paragraph_format.space_after = Pt(1.5)
        return

    num_rows = len(table_obj._cellvalues)
    num_cols = len(table_obj._cellvalues[0])
    tbl = doc.add_table(rows=num_rows, cols=num_cols)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    set_table_borders(tbl, HEX_BORDER, "4")
    
    tot_w = sum(table_obj._colWidths) if table_obj._colWidths else (num_cols * 50)
    col_widths_in = [(w / tot_w) * 6.85 for w in table_obj._colWidths] if table_obj._colWidths else [6.85 / num_cols]*num_cols

    for r_idx, row in enumerate(table_obj._cellvalues):
        is_header = (r_idx == 0) and num_rows > 1
        is_highlight_green = False
        is_highlight_slate = False
        
        row_str = " ".join(str(c.text if isinstance(c, Paragraph) else c) for c in row)
        if "FULL AUTONOMOUS BUILD" in row_str:
            is_highlight_green = True
        elif "TOTAL MVP PROTOTYPE COST" in row_str:
            is_highlight_slate = True
            
        for c_idx, cell in enumerate(row):
            tbl_cell = tbl.cell(r_idx, c_idx)
            tbl_cell.width = Inches(col_widths_in[c_idx])
            
            if is_header:
                set_cell_background(tbl_cell, HEX_TEAL)
            elif is_highlight_green:
                set_cell_background(tbl_cell, HEX_GREEN_BG)
            elif is_highlight_slate:
                set_cell_background(tbl_cell, "E2E8F0")
            elif r_idx % 2 == 1:
                set_cell_background(tbl_cell, HEX_TABLE_ALT)
            else:
                set_cell_background(tbl_cell, HEX_WHITE)
                
            set_cell_margins(tbl_cell, top=25, bottom=25, left=45, right=45)
            p = tbl_cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.04
            
            cell_text = ""
            is_cell_center = False
            if isinstance(cell, Paragraph):
                cell_text = cell.text
                if cell.style.name in ('th', 'td_c'):
                    is_cell_center = True
            else:
                cell_text = str(cell)
                
            if is_header or is_cell_center:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                
            runs = parse_html_to_runs(cell_text)
            f_color = COLOR_WHITE if is_header else COLOR_DARK
            f_bold = is_header or (c_idx == 0 and num_rows > 2)
            apply_runs_to_para(p, runs, default_size=Pt(6.5), default_color=f_color, default_bold=f_bold)
            
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(0)
    p_sp.paragraph_format.space_after = Pt(1.5)

def build_perfect_replica():
    doc = docx.Document()
    
    # ═══════════════════════════ SECTION 1: COVER PAGE ═══════════════════════════
    sec1 = doc.sections[0]
    sec1.page_width = Inches(8.27)
    sec1.page_height = Inches(11.69)
    sec1.left_margin = Inches(0)
    sec1.right_margin = Inches(0)
    sec1.top_margin = Inches(0)
    sec1.bottom_margin = Inches(0)
    sec1.different_first_page_header_footer = True
    
    p_cover = doc.add_paragraph()
    p_cover.paragraph_format.space_before = Pt(0)
    p_cover.paragraph_format.space_after = Pt(0)
    p_cover.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    cover_img_path = "rendered_pages/page_01_updated.png" if os.path.exists("rendered_pages/page_01_updated.png") else "rendered_pages/page_01.png"
    p_cover.add_run().add_picture(cover_img_path, width=Inches(8.27), height=Inches(11.69))
    
    # ═══════════════════════════ SECTION 2: PAGES 2 TO 25 ═══════════════════════════
    sec2 = doc.add_section(WD_SECTION_START.NEW_PAGE)
    sec2.page_width = Inches(8.27)
    sec2.page_height = Inches(11.69)
    sec2.left_margin = Inches(0.71)   # 18mm
    sec2.right_margin = Inches(0.71)  # 18mm
    sec2.top_margin = Inches(0.55)    # 14mm
    sec2.bottom_margin = Inches(0.55) # 14mm
    sec2.header.is_linked_to_previous = False
    sec2.footer.is_linked_to_previous = False
    
    # ─────────────────────────── RUNNING HEADER BAR (SOLID NAVY) ───────────────────────────
    header = sec2.header
    p_hdr_clear = header.paragraphs[0]
    p_hdr_clear.text = ""
    
    tbl_hdr = header.add_table(rows=1, cols=2, width=Inches(6.85))
    tbl_hdr.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_hdr.autofit = False
    tbl_hdr.columns[0].width = Inches(4.50)
    tbl_hdr.columns[1].width = Inches(2.35)
    
    c_hl = tbl_hdr.cell(0, 0)
    c_hr = tbl_hdr.cell(0, 1)
    set_cell_background(c_hl, HEX_NAVY)
    set_cell_background(c_hr, HEX_NAVY)
    set_cell_margins(c_hl, top=30, bottom=30, left=60, right=40)
    set_cell_margins(c_hr, top=30, bottom=30, left=40, right=60)
    
    p_hl = c_hl.paragraphs[0]
    p_hl.paragraph_format.space_before = Pt(0)
    p_hl.paragraph_format.space_after = Pt(0)
    r_hl = p_hl.add_run("SANJIVANI — Hybrid PCM–Peltier Medical Cold-Chain System")
    r_hl.font.name = 'Arial'
    r_hl.font.size = Pt(6.5)
    r_hl.font.bold = True
    r_hl.font.color.rgb = COLOR_WHITE
    
    p_hr = c_hr.paragraphs[0]
    p_hr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_hr.paragraph_format.space_before = Pt(0)
    p_hr.paragraph_format.space_after = Pt(0)
    r_hr = p_hr.add_run("Dr. B. K. Passi Memorial Senior Bal Vigyan 2026–2027 (PHYSICS)")
    r_hr.font.name = 'Arial'
    r_hr.font.size = Pt(6.2)
    r_hr.font.color.rgb = RGBColor(224, 242, 254)
    
    # ─────────────────────────── RUNNING FOOTER BAR ───────────────────────────
    footer = sec2.footer
    p_ftr_clear = footer.paragraphs[0]
    p_ftr_clear.text = ""
    
    tbl_ftr = footer.add_table(rows=1, cols=2, width=Inches(6.85))
    tbl_ftr.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_ftr.autofit = False
    set_table_borders(tbl_ftr, HEX_BORDER, "4")
    tbl_ftr.columns[0].width = Inches(4.50)
    tbl_ftr.columns[1].width = Inches(2.35)
    
    c_fl = tbl_ftr.cell(0, 0)
    c_fr = tbl_ftr.cell(0, 1)
    set_cell_margins(c_fl, top=20, bottom=20, left=40, right=40)
    set_cell_margins(c_fr, top=20, bottom=20, left=40, right=40)
    
    p_fl = c_fl.paragraphs[0]
    p_fl.paragraph_format.space_before = Pt(0)
    p_fl.paragraph_format.space_after = Pt(0)
    r_fl = p_fl.add_run("School UID: SBVPH-05  |  Mentor: Mr. Gopal Kumar Roy")
    r_fl.font.name = 'Arial'
    r_fl.font.size = Pt(6.5)
    r_fl.font.color.rgb = COLOR_SLATE
    
    p_fr = c_fr.paragraphs[0]
    p_fr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_fr.paragraph_format.space_before = Pt(0)
    p_fr.paragraph_format.space_after = Pt(0)
    r_fr = p_fr.add_run("Made by: Bhavmanyu Singh Sisodia   |   Senior Bal Vigyan (Physics)")
    r_fr.font.name = 'Arial'
    r_fr.font.size = Pt(6.2)
    r_fr.font.italic = True
    r_fr.font.color.rgb = COLOR_SLATE
    
    # ─────────────────────────── BUILD PAGES 2 TO 25 ───────────────────────────
    page_funcs = [
        ('Page 02: Certificate', bcd.p02_certificate),
        ('Page 03: Declaration', bcd.p03_declaration),
        ('Page 04: Acknowledgement', bcd.p04_acknowledgement),
        ('Page 05: Particulars', bcd.p05_particulars),
        ('Page 06: Abstract', bcd.p06_abstract),
        ('Page 07: Table of Contents', bcd.p07_toc),
        ('Page 08: Introduction', bcd.p08_introduction),
        ('Page 09: Problem Statement', bcd.p09_problem),
        ('Page 10: Aim & Objectives', bcd.p10_aim),
        ('Page 11: Phase Change Material', bcd.p11_pcm),
        ('Page 12: Thermoelectric Cooling', bcd.p12_peltier),
        ('Page 13: System Architecture', bcd.p13_architecture),
        ('Page 14: Components & Circuitry', bcd.p14_components),
        ('Page 15: Mathematical Modelling', bcd.p15_thermal),
        ('Page 16: Control Logic & Firmware', bcd.p16_control),
        ('Page 17: Engineering Calculations', bcd.p17_calcs),
        ('Page 18: Prototype Fabrication', bcd.p18_prototype),
        ('Page 19: Testing Methodology', bcd.p19_methodology),
        ('Page 20: Experimental Observations', bcd.p20_observations),
        ('Page 21: Results & Analysis', bcd.p21_results),
        ('Page 22: Economic Feasibility', bcd.p22_economic),
        ('Page 23: Safety & Risk', bcd.p23_safety),
        ('Page 24: Conclusion & Scope', bcd.p24_conclusion),
        ('Page 25: References & Signatures', bcd.p25_references),
    ]
    
    for idx, (p_name, fn) in enumerate(page_funcs, start=2):
        print(f"Building {p_name}...")
        elements = fn()
        for el in elements:
            if isinstance(el, Table):
                if len(el._cellvalues) == 1 and len(el._cellvalues[0]) == 1:
                    first_val = el._cellvalues[0][0]
                    txt = first_val.text if isinstance(first_val, Paragraph) else str(first_val)
                    if any(k in txt.upper() for k in ['CHAPTER', 'CERTIFICATE', 'DECLARATION', 'ACKNOWLEDGEMENT', 'PARTICULARS', 'EXECUTIVE SUMMARY', 'TABLE OF CONTENTS']):
                        add_banner(doc, txt)
                        continue
                render_table_flowable(doc, el)
                
            elif isinstance(el, Paragraph):
                st_name = el.style.name
                if st_name in ('sec', 'subsec'):
                    add_sec_head(doc, el.text)
                elif st_name == 'eq':
                    add_equation_box(doc, el.text)
                elif st_name == 'caption':
                    add_caption_para(doc, el.text)
                elif st_name == 'bullet':
                    add_bullet_para(doc, el.text)
                elif st_name == 'ref':
                    add_ref_para(doc, el.text)
                elif st_name == 'subtle_end':
                    p_sub = doc.add_paragraph()
                    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    r_sub = p_sub.add_run("Made by: Bhavmanyu Singh Sisodia  ·  Senior Bal Vigyan 2026–2027 Research Dossier")
                    r_sub.font.name = 'Arial'
                    r_sub.font.size = Pt(7.2)
                    r_sub.font.italic = True
                    r_sub.font.color.rgb = COLOR_SLATE
                else:
                    add_body_para(doc, el.text, style_name=st_name)
                    
            elif isinstance(el, Image):
                p_img = doc.add_paragraph()
                p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p_img.paragraph_format.space_before = Pt(1.5)
                p_img.paragraph_format.space_after = Pt(1.5)
                w_in = min(6.85, el.drawWidth / 72.0)
                img_src = getattr(el, 'filename', getattr(el, '_filename', None))
                p_img.add_run().add_picture(img_src, width=Inches(w_in))
                
            elif isinstance(el, Spacer):
                pass
            elif isinstance(el, HRFlowable):
                pass
            elif type(el).__name__ == 'PCMDiagram':
                add_pcm_diagram(doc)
            elif type(el).__name__ == 'PeltierDiagram':
                add_peltier_diagram(doc)
            else:
                print(f"Unknown element type: {type(el).__name__}")
                
        if idx < 25:
            doc.add_page_break()

    out_path1 = "SANJIVANI — Senior Bal Vigyan 2026–2027 Project Report.docx"
    out_path2 = "SANJIVANI_Senior_Bal_Vigyan_2026-27_Report.docx"
    doc.save(out_path1)
    doc.save(out_path2)
    print(f"Saved: {out_path1} ({os.path.getsize(out_path1)} bytes)")
    print(f"Saved: {out_path2} ({os.path.getsize(out_path2)} bytes)")

if __name__ == '__main__':
    build_perfect_replica()
