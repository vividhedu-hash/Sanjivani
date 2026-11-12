import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

# Ensure UTF-8
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Colors
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

def set_cell_margins(cell, top=80, bottom=80, left=120, right=120):
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

def add_banner(doc, title_text):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    tbl.columns[0].width = Inches(6.85)
    cell = tbl.cell(0, 0)
    set_cell_background(cell, HEX_TEAL)
    set_cell_margins(cell, top=70, bottom=70, left=140, right=140)
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    run = p.add_run(title_text.upper())
    run.font.name = 'Arial'
    run.font.size = Pt(10.0)
    run.font.bold = True
    run.font.color.rgb = COLOR_WHITE
    doc.add_paragraph().paragraph_format.space_after = Pt(2)

def add_sec_head(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(1.5)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = 'Arial'
    run.font.size = Pt(8.6)
    run.font.bold = True
    run.font.color.rgb = COLOR_NAVY
    return p

def add_body(doc, text, bold_prefix=None, space_after=2.5):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.10
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = 'Arial'
        r_pre.font.size = Pt(7.8)
        r_pre.font.bold = True
        r_pre.font.color.rgb = COLOR_DARK
    r_body = p.add_run(text)
    r_body.font.name = 'Arial'
    r_body.font.size = Pt(7.8)
    r_body.font.color.rgb = COLOR_DARK
    return p

def add_bullet(doc, text, bold_prefix=None):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(1.8)
    p.paragraph_format.line_spacing = 1.08
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = 'Arial'
        r_pre.font.size = Pt(7.6)
        r_pre.font.bold = True
        r_pre.font.color.rgb = COLOR_DARK
    r_body = p.add_run(text)
    r_body.font.name = 'Arial'
    r_body.font.size = Pt(7.6)
    r_body.font.color.rgb = COLOR_DARK
    return p

def add_equation_box(doc, eq_text):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.columns[0].width = Inches(6.85)
    cell = tbl.cell(0, 0)
    set_cell_background(cell, HEX_CARD_BG)
    set_cell_margins(cell, top=50, bottom=50, left=100, right=100)
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    run = p.add_run(eq_text)
    run.font.name = 'Arial'
    run.font.size = Pt(8.2)
    run.font.bold = True
    run.font.color.rgb = COLOR_TEAL_DARK
    doc.add_paragraph().paragraph_format.space_after = Pt(1.5)

def build_docx_table(doc, headers, rows, col_widths=None, alt_bg=True):
    num_cols = len(headers)
    tbl = doc.add_table(rows=len(rows) + 1, cols=num_cols)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    set_table_borders(tbl, HEX_BORDER, "4")
    
    # Header Row
    hdr_cells = tbl.rows[0].cells
    for i, h in enumerate(headers):
        set_cell_background(hdr_cells[i], HEX_TEAL)
        set_cell_margins(hdr_cells[i], top=50, bottom=50, left=80, right=80)
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        run = p.add_run(h)
        run.font.name = 'Arial'
        run.font.size = Pt(7.0)
        run.font.bold = True
        run.font.color.rgb = COLOR_WHITE
        
    # Data Rows
    for r_idx, row in enumerate(rows):
        row_cells = tbl.rows[r_idx + 1].cells
        row_bg = HEX_TABLE_ALT if (alt_bg and r_idx % 2 == 1) else HEX_WHITE
        for c_idx, val in enumerate(row):
            set_cell_background(row_cells[c_idx], row_bg)
            set_cell_margins(row_cells[c_idx], top=40, bottom=40, left=80, right=80)
            p = row_cells[c_idx].paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.05
            
            is_bold = (c_idx == 0) or ("<b>" in str(val))
            text_clean = str(val).replace("<b>", "").replace("</b>", "").replace("<i>", "").replace("</i>", "")
            run = p.add_run(text_clean)
            run.font.name = 'Arial'
            run.font.size = Pt(6.8)
            run.font.bold = is_bold
            run.font.color.rgb = COLOR_DARK
            if c_idx > 0 and len(headers) > 2 and ("%" in text_clean or "Hours" in text_clean or "₹" in text_clean or "°C" in text_clean or "V" in text_clean or "A" in text_clean):
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            
    # Apply column widths
    if col_widths:
        for row in tbl.rows:
            for i, w in enumerate(col_widths):
                row.cells[i].width = Inches(w)
                
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    return tbl

def add_figure_image(doc, img_path, width_in, caption_text):
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(2)
        p_img.paragraph_format.space_after = Pt(2)
        p_img.add_run().add_picture(img_path, width=Inches(width_in))
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(0)
        p_cap.paragraph_format.space_after = Pt(2)
        run_cap = p_cap.add_run(caption_text)
        run_cap.font.name = 'Arial'
        run_cap.font.size = Pt(6.8)
        run_cap.font.italic = True
        run_cap.font.color.rgb = COLOR_SLATE

print("All base builder functions ready.")
