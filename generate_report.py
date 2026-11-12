"""
SANJIVANI — Senior Bal Vigyan 2026-2027 Project Report Generator
Generates a complete 25-page A4 PDF using ReportLab 5.x
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm, cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether, ListFlowable, ListItem,
    Flowable
)
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing, Rect, Line, String, Circle, Polygon, Ellipse
from reportlab.graphics import renderPDF
import math

def _poly(canvas_obj, pts, fill=1, stroke=0):
    """Draw a polygon from a flat list [x0,y0,x1,y1,...] using canvas paths."""
    p = canvas_obj.beginPath()
    p.moveTo(pts[0], pts[1])
    for i in range(2, len(pts), 2):
        p.lineTo(pts[i], pts[i+1])
    p.close()
    canvas_obj.drawPath(p, fill=fill, stroke=stroke)

# ─────────────────────────── COLOUR PALETTE ───────────────────────────
NAVY        = colors.HexColor("#0D1B2A")   # Deep navy headings
TEAL        = colors.HexColor("#1A7A8A")   # Muted teal accent
TEAL_LIGHT  = colors.HexColor("#E8F4F6")   # Light teal bg
GOLD        = colors.HexColor("#B8902A")   # Restrained gold
GOLD_LIGHT  = colors.HexColor("#FDF6E3")   # Light gold bg
SLATE       = colors.HexColor("#4A5568")   # Slate grey body
TABLE_BG    = colors.HexColor("#EEF2F7")   # Light blue-grey table
WHITE       = colors.white
BLACK       = colors.HexColor("#1A1A1A")
AMBER_PH    = colors.HexColor("#FFF3CD")   # Placeholder amber
AMBER_BD    = colors.HexColor("#D4A017")   # Placeholder border
RULE_COLOR  = colors.HexColor("#CBD5E0")
TEAL_DARK   = colors.HexColor("#0E5A67")

PAGE_W, PAGE_H = A4
L_MARGIN = 20*mm
R_MARGIN = 20*mm
T_MARGIN = 18*mm
B_MARGIN = 18*mm

# ─────────────────────────── STYLE REGISTRY ───────────────────────────
def build_styles():
    base = getSampleStyleSheet()

    styles = {}

    styles['cover_title'] = ParagraphStyle(
        'cover_title', fontName='Helvetica-Bold', fontSize=52,
        textColor=WHITE, alignment=TA_CENTER, leading=58, spaceAfter=4)

    styles['cover_sanskrit'] = ParagraphStyle(
        'cover_sanskrit', fontName='Helvetica', fontSize=22,
        textColor=colors.HexColor("#B8D4E0"), alignment=TA_CENTER,
        leading=28, spaceAfter=4)

    styles['cover_subtitle'] = ParagraphStyle(
        'cover_subtitle', fontName='Helvetica-Bold', fontSize=15,
        textColor=colors.HexColor("#7EC8D8"), alignment=TA_CENTER,
        leading=20, spaceAfter=6)

    styles['cover_formal'] = ParagraphStyle(
        'cover_formal', fontName='Helvetica', fontSize=10,
        textColor=colors.HexColor("#D0E8F0"), alignment=TA_CENTER,
        leading=15, spaceAfter=4)

    styles['cover_tagline'] = ParagraphStyle(
        'cover_tagline', fontName='Helvetica-BoldOblique', fontSize=12,
        textColor=GOLD, alignment=TA_CENTER, leading=16, spaceAfter=8)

    styles['cover_label'] = ParagraphStyle(
        'cover_label', fontName='Helvetica-Bold', fontSize=9,
        textColor=colors.HexColor("#7EC8D8"), alignment=TA_CENTER,
        leading=12, spaceAfter=2, spaceBefore=2)

    styles['cover_value'] = ParagraphStyle(
        'cover_value', fontName='Helvetica', fontSize=9,
        textColor=WHITE, alignment=TA_CENTER, leading=13, spaceAfter=2)

    styles['cert_title'] = ParagraphStyle(
        'cert_title', fontName='Helvetica-Bold', fontSize=18,
        textColor=NAVY, alignment=TA_CENTER, leading=24, spaceAfter=10)

    styles['cert_body'] = ParagraphStyle(
        'cert_body', fontName='Helvetica', fontSize=11,
        textColor=BLACK, alignment=TA_JUSTIFY, leading=18,
        spaceAfter=6, spaceBefore=6)

    styles['cert_name'] = ParagraphStyle(
        'cert_name', fontName='Helvetica-Bold', fontSize=11,
        textColor=NAVY, alignment=TA_CENTER, leading=14)

    styles['page_title'] = ParagraphStyle(
        'page_title', fontName='Helvetica-Bold', fontSize=15,
        textColor=WHITE, alignment=TA_LEFT, leading=20,
        spaceAfter=0, leftIndent=4)

    styles['section_heading'] = ParagraphStyle(
        'section_heading', fontName='Helvetica-Bold', fontSize=12,
        textColor=NAVY, alignment=TA_LEFT, leading=16,
        spaceAfter=4, spaceBefore=10,
        borderPad=2)

    styles['subsection_heading'] = ParagraphStyle(
        'subsection_heading', fontName='Helvetica-Bold', fontSize=10.5,
        textColor=TEAL_DARK, alignment=TA_LEFT, leading=14,
        spaceAfter=3, spaceBefore=7)

    styles['body'] = ParagraphStyle(
        'body', fontName='Helvetica', fontSize=9.5,
        textColor=BLACK, alignment=TA_JUSTIFY, leading=15,
        spaceAfter=5, spaceBefore=2)

    styles['body_sm'] = ParagraphStyle(
        'body_sm', fontName='Helvetica', fontSize=8.5,
        textColor=BLACK, alignment=TA_JUSTIFY, leading=13,
        spaceAfter=3)

    styles['caption'] = ParagraphStyle(
        'caption', fontName='Helvetica-Oblique', fontSize=8,
        textColor=SLATE, alignment=TA_CENTER, leading=11, spaceAfter=4)

    styles['equation'] = ParagraphStyle(
        'equation', fontName='Helvetica-Bold', fontSize=11,
        textColor=TEAL_DARK, alignment=TA_CENTER, leading=18,
        spaceAfter=4, spaceBefore=4)

    styles['eq_note'] = ParagraphStyle(
        'eq_note', fontName='Helvetica', fontSize=8.5,
        textColor=SLATE, alignment=TA_LEFT, leading=12,
        spaceAfter=2, leftIndent=12)

    styles['placeholder'] = ParagraphStyle(
        'placeholder', fontName='Helvetica-BoldOblique', fontSize=9,
        textColor=colors.HexColor("#7A5C00"), alignment=TA_CENTER,
        leading=13, spaceAfter=2)

    styles['keyword'] = ParagraphStyle(
        'keyword', fontName='Helvetica-Bold', fontSize=9,
        textColor=TEAL_DARK, alignment=TA_LEFT, leading=14, spaceAfter=2)

    styles['toc_entry'] = ParagraphStyle(
        'toc_entry', fontName='Helvetica', fontSize=9.5,
        textColor=BLACK, alignment=TA_LEFT, leading=15, spaceAfter=2)

    styles['toc_entry_bold'] = ParagraphStyle(
        'toc_entry_bold', fontName='Helvetica-Bold', fontSize=10,
        textColor=NAVY, alignment=TA_LEFT, leading=16, spaceAfter=2)

    styles['bullet'] = ParagraphStyle(
        'bullet', fontName='Helvetica', fontSize=9.5,
        textColor=BLACK, alignment=TA_LEFT, leading=14,
        spaceAfter=2, leftIndent=14, firstLineIndent=-8)

    styles['numbered'] = ParagraphStyle(
        'numbered', fontName='Helvetica', fontSize=9.5,
        textColor=BLACK, alignment=TA_LEFT, leading=14,
        spaceAfter=2, leftIndent=16)

    styles['footer_text'] = ParagraphStyle(
        'footer_text', fontName='Helvetica', fontSize=7.5,
        textColor=SLATE, alignment=TA_CENTER, leading=10)

    styles['ack_body'] = ParagraphStyle(
        'ack_body', fontName='Helvetica', fontSize=10,
        textColor=BLACK, alignment=TA_JUSTIFY, leading=16,
        spaceAfter=5, spaceBefore=3)

    styles['table_header'] = ParagraphStyle(
        'table_header', fontName='Helvetica-Bold', fontSize=8.5,
        textColor=WHITE, alignment=TA_CENTER, leading=12)

    styles['table_cell'] = ParagraphStyle(
        'table_cell', fontName='Helvetica', fontSize=8.5,
        textColor=BLACK, alignment=TA_LEFT, leading=12)

    styles['table_cell_c'] = ParagraphStyle(
        'table_cell_c', fontName='Helvetica', fontSize=8.5,
        textColor=BLACK, alignment=TA_CENTER, leading=12)

    styles['ref_entry'] = ParagraphStyle(
        'ref_entry', fontName='Helvetica', fontSize=8.5,
        textColor=BLACK, alignment=TA_LEFT, leading=14,
        spaceAfter=4, leftIndent=20, firstLineIndent=-20)

    return styles

S = build_styles()

# ─────────────────────────── HELPER FLOWABLES ─────────────────────────

def ph(text, width=None):
    """Placeholder block"""
    content = f"[ {text} ]"
    p = Paragraph(content, S['placeholder'])
    if width:
        return Table([[p]], colWidths=[width],
                     style=TableStyle([
                         ('BACKGROUND', (0,0), (-1,-1), AMBER_PH),
                         ('BOX', (0,0), (-1,-1), 0.5, AMBER_BD),
                         ('TOPPADDING', (0,0), (-1,-1), 4),
                         ('BOTTOMPADDING', (0,0), (-1,-1), 4),
                         ('LEFTPADDING', (0,0), (-1,-1), 6),
                         ('RIGHTPADDING', (0,0), (-1,-1), 6),
                     ]))
    return Table([[p]],
                 style=TableStyle([
                     ('BACKGROUND', (0,0), (-1,-1), AMBER_PH),
                     ('BOX', (0,0), (-1,-1), 0.5, AMBER_BD),
                     ('TOPPADDING', (0,0), (-1,-1), 4),
                     ('BOTTOMPADDING', (0,0), (-1,-1), 4),
                     ('LEFTPADDING', (0,0), (-1,-1), 6),
                     ('RIGHTPADDING', (0,0), (-1,-1), 6),
                 ]))

def sig_block(name, title, extra=""):
    """Signature block"""
    rows = [
        [Paragraph("_" * 28, S['body']), Paragraph("", S['body'])],
        [Paragraph(f"<b>{name}</b>", S['cert_body']), Paragraph("", S['body'])],
        [Paragraph(title, S['body_sm']), Paragraph("", S['body'])],
    ]
    if extra:
        rows.append([Paragraph(extra, S['body_sm']), Paragraph("", S['body'])])
    return Table(rows, colWidths=[80*mm, 10*mm])

def hr(color=RULE_COLOR, thickness=0.5):
    return HRFlowable(width="100%", thickness=thickness, color=color,
                      spaceAfter=4, spaceBefore=4)

def section_banner(text, pg_num=None):
    """Navy banner with page-section title"""
    label = text if pg_num is None else text
    p = Paragraph(label, S['page_title'])
    t = Table([[p]], colWidths=[PAGE_W - L_MARGIN - R_MARGIN],
              style=TableStyle([
                  ('BACKGROUND', (0,0), (-1,-1), NAVY),
                  ('TOPPADDING', (0,0), (-1,-1), 7),
                  ('BOTTOMPADDING', (0,0), (-1,-1), 7),
                  ('LEFTPADDING', (0,0), (-1,-1), 10),
                  ('RIGHTPADDING', (0,0), (-1,-1), 10),
              ]))
    return t

def teal_banner(text):
    p = Paragraph(text, ParagraphStyle('tb', fontName='Helvetica-Bold',
        fontSize=10, textColor=WHITE, alignment=TA_LEFT, leading=14))
    t = Table([[p]], colWidths=[PAGE_W - L_MARGIN - R_MARGIN],
              style=TableStyle([
                  ('BACKGROUND', (0,0), (-1,-1), TEAL),
                  ('TOPPADDING', (0,0), (-1,-1), 5),
                  ('BOTTOMPADDING', (0,0), (-1,-1), 5),
                  ('LEFTPADDING', (0,0), (-1,-1), 10),
                  ('RIGHTPADDING', (0,0), (-1,-1), 10),
              ]))
    return t

def info_table(rows_data, col_widths=None, header=False):
    """Standard info table"""
    cw = col_widths or [60*mm, 110*mm]
    ts = TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), TABLE_BG),
        ('ROWBACKGROUNDS', (0,0), (-1,-1), [TABLE_BG, WHITE]),
        ('BOX', (0,0), (-1,-1), 0.5, RULE_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.3, RULE_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ])
    if header:
        ts.add('BACKGROUND', (0,0), (-1,0), NAVY)
        ts.add('TEXTCOLOR', (0,0), (-1,0), WHITE)
        ts.add('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold')
    table_rows = []
    for r in rows_data:
        table_rows.append([Paragraph(str(c), S['table_cell']) for c in r])
    return Table(table_rows, colWidths=cw, style=ts)

def bullet(text):
    return Paragraph(f"&#x2022; &nbsp; {text}", S['bullet'])

def numbered_item(n, text):
    return Paragraph(f"<b>{n}.</b> &nbsp; {text}", S['numbered'])

# ─────────────────────────── DIAGRAMS ─────────────────────────────────

class PCMDiagram(Flowable):
    """PCM phase-change illustration"""
    def __init__(self, width=160*mm, height=55*mm):
        Flowable.__init__(self)
        self.width = width
        self.height = height

    def draw(self):
        c = self.canv
        w, h = self.width, self.height
        # Background
        c.setFillColor(colors.HexColor("#F7FBFC"))
        c.roundRect(0, 0, w, h, 6, fill=1, stroke=0)
        c.setStrokeColor(RULE_COLOR)
        c.setLineWidth(0.5)
        c.roundRect(0, 0, w, h, 6, fill=0, stroke=1)

        # Three phases
        col_w = w / 3
        phases = [
            ("SOLID PCM", colors.HexColor("#BFDBFE"), "Absorbing sensible heat\nT < T_melt"),
            ("MELTING (Phase Change)", colors.HexColor("#A7F3D0"), "Absorbing latent heat\nT ≈ T_melt (Isothermal)"),
            ("LIQUID PCM", colors.HexColor("#FDE68A"), "Absorbing sensible heat\nT > T_melt"),
        ]
        for i, (label, col, desc) in enumerate(phases):
            x = i * col_w + 2
            c.setFillColor(col)
            c.roundRect(x, h*0.3, col_w-4, h*0.5, 4, fill=1, stroke=0)
            c.setFillColor(BLACK)
            c.setFont("Helvetica-Bold", 7.5)
            c.drawCentredString(x + (col_w-4)/2, h*0.72, label)
            c.setFont("Helvetica", 6.5)
            for j, line in enumerate(desc.split('\n')):
                c.drawCentredString(x + (col_w-4)/2, h*0.6 - j*9, line)

        # Arrow
        c.setStrokeColor(TEAL_DARK)
        c.setLineWidth(1.5)
        c.line(10, h*0.15, w-10, h*0.15)
        # arrowhead
        c.setFillColor(TEAL_DARK)
        _poly(c, [w-10, h*0.15, w-16, h*0.18, w-16, h*0.12], fill=1, stroke=0)
        c.setFillColor(SLATE)
        c.setFont("Helvetica-Bold", 7)
        c.drawCentredString(w/2, h*0.07, "Heat input increasing  →  Temperature rising")

        # Title
        c.setFillColor(NAVY)
        c.setFont("Helvetica-Bold", 8)
        c.drawString(5, h - 12, "Figure 1 — PCM Phase-Change Thermal Storage Principle")

class PeltierDiagram(Flowable):
    """Peltier module schematic"""
    def __init__(self, width=160*mm, height=70*mm):
        Flowable.__init__(self)
        self.width = width
        self.height = height

    def draw(self):
        c = self.canv
        w, h = self.width, self.height

        c.setFillColor(colors.HexColor("#F7FBFC"))
        c.roundRect(0, 0, w, h, 6, fill=1, stroke=0)
        c.setStrokeColor(RULE_COLOR)
        c.setLineWidth(0.5)
        c.roundRect(0, 0, w, h, 6, fill=0, stroke=1)

        # Hot side (top)
        c.setFillColor(colors.HexColor("#FEE2E2"))
        c.roundRect(w*0.15, h*0.72, w*0.7, h*0.2, 3, fill=1, stroke=0)
        c.setFillColor(colors.HexColor("#DC2626"))
        c.setFont("Helvetica-Bold", 8)
        c.drawCentredString(w/2, h*0.80, "HOT SIDE — Heat Rejection  (Q_hot)")

        # Cold side (bottom)
        c.setFillColor(colors.HexColor("#DBEAFE"))
        c.roundRect(w*0.15, h*0.08, w*0.7, h*0.2, 3, fill=1, stroke=0)
        c.setFillColor(colors.HexColor("#1D4ED8"))
        c.setFont("Helvetica-Bold", 8)
        c.drawCentredString(w/2, h*0.17, "COLD SIDE — Cooling Interface  (Q_cold)")

        # Module body (semiconductors)
        c.setFillColor(colors.HexColor("#E5E7EB"))
        c.roundRect(w*0.25, h*0.30, w*0.5, h*0.40, 3, fill=1, stroke=0)
        c.setStrokeColor(SLATE)
        c.setLineWidth(0.4)
        c.roundRect(w*0.25, h*0.30, w*0.5, h*0.40, 3, fill=0, stroke=1)

        # N and P elements inside module
        for i in range(5):
            x = w*0.28 + i * (w*0.5-8*mm)/4.5
            c.setFillColor(colors.HexColor("#374151"))
            c.rect(x, h*0.35, 5*mm, h*0.15, fill=1, stroke=0)
            c.setFillColor(colors.HexColor("#9CA3AF"))
            c.rect(x, h*0.52, 5*mm, h*0.15, fill=1, stroke=0)
            c.setFillColor(WHITE)
            c.setFont("Helvetica-Bold", 6)
            c.drawCentredString(x+2.5*mm, h*0.42, "N")
            c.drawCentredString(x+2.5*mm, h*0.59, "P")

        c.setFillColor(SLATE)
        c.setFont("Helvetica", 7)
        c.drawCentredString(w/2, h*0.46, "Semiconductor Junctions (N-type & P-type)")

        # DC power arrow
        c.setStrokeColor(colors.HexColor("#7C3AED"))
        c.setLineWidth(1.5)
        c.line(w*0.08, h*0.42, w*0.22, h*0.42)
        c.setFillColor(colors.HexColor("#7C3AED"))
        _poly(c, [w*0.22, h*0.42, w*0.19, h*0.44, w*0.19, h*0.40], fill=1, stroke=0)
        c.setFont("Helvetica-Bold", 7)
        c.drawCentredString(w*0.08, h*0.47, "DC")
        c.drawCentredString(w*0.08, h*0.40, "Power")
        c.drawCentredString(w*0.08, h*0.33, "(P_elec)")

        # Heat arrows
        c.setStrokeColor(colors.HexColor("#DC2626"))
        c.setLineWidth(1.5)
        c.line(w/2, h*0.70, w/2, h*0.95)
        _poly(c, [w/2, h*0.95, w/2-3*mm, h*0.90, w/2+3*mm, h*0.90], fill=1, stroke=0)

        c.setStrokeColor(colors.HexColor("#1D4ED8"))
        c.line(w/2, h*0.08, w/2, h*0.30)
        c.setFillColor(colors.HexColor("#1D4ED8"))
        _poly(c, [w/2, h*0.30, w/2-3*mm, h*0.25, w/2+3*mm, h*0.25], fill=1, stroke=0)

        # Equation
        c.setFillColor(TEAL_DARK)
        c.setFont("Helvetica-Bold", 8.5)
        c.drawCentredString(w*0.80, h*0.50, "Q_hot = Q_cold + P_elec")

        # Title
        c.setFillColor(NAVY)
        c.setFont("Helvetica-Bold", 8)
        c.drawString(5, h - 12, "Figure 2 — Peltier Module: Heat Pumping Principle")

class SystemBlockDiagram(Flowable):
    """Full system block diagram"""
    def __init__(self, width=168*mm, height=120*mm):
        Flowable.__init__(self)
        self.width = width
        self.height = height

    def _box(self, c, x, y, bw, bh, label, fill_color, font_size=7, text_color=WHITE):
        c.setFillColor(fill_color)
        c.roundRect(x, y, bw, bh, 3, fill=1, stroke=0)
        c.setStrokeColor(colors.HexColor("#94A3B8"))
        c.setLineWidth(0.5)
        c.roundRect(x, y, bw, bh, 3, fill=0, stroke=1)
        c.setFillColor(text_color)
        c.setFont("Helvetica-Bold", font_size)
        lines = label.split('\n')
        for i, line in enumerate(lines):
            c.drawCentredString(x + bw/2,
                y + bh/2 - (len(lines)-1)*4 + i*8 - 3,
                line)

    def _arrow(self, c, x1, y1, x2, y2, color=SLATE, label=""):
        c.setStrokeColor(color)
        c.setLineWidth(1)
        c.line(x1, y1, x2, y2)
        # arrowhead
        angle = math.atan2(y2-y1, x2-x1)
        al = 4*mm
        c.setFillColor(color)
        ax = x2 - al*math.cos(angle)
        ay = y2 - al*math.sin(angle)
        _poly(c, [x2, y2,
                   ax + al*0.4*math.sin(angle), ay - al*0.4*math.cos(angle),
                   ax - al*0.4*math.sin(angle), ay + al*0.4*math.cos(angle)],
                  fill=1, stroke=0)
        if label:
            mx, my = (x1+x2)/2, (y1+y2)/2
            c.setFillColor(SLATE)
            c.setFont("Helvetica-Oblique", 5.5)
            c.drawCentredString(mx, my+2, label)

    def draw(self):
        c = self.canv
        w, h = self.width, self.height

        c.setFillColor(colors.HexColor("#F0F7F9"))
        c.roundRect(0, 0, w, h, 6, fill=1, stroke=0)
        c.setStrokeColor(RULE_COLOR)
        c.setLineWidth(0.5)
        c.roundRect(0, 0, w, h, 6, fill=0, stroke=1)

        bw = 28*mm; bh = 11*mm
        # Row layout
        # Top row: Power Supply -> Controller -> Peltier
        # Middle: Insulated Enclosure (large), Sensor feeds Controller
        # Bottom: PCM Chamber, Al Spreader, Liquid Chamber, Hot Side Sink

        ps_x, ps_y = 2*mm, h-18*mm
        self._box(c, ps_x, ps_y, bw, bh, "POWER SUPPLY\n(Battery/DC)", colors.HexColor("#374151"), 6.5)

        ctrl_x, ctrl_y = 38*mm, h-18*mm
        self._box(c, ctrl_x, ctrl_y, bw, bh, "CONTROLLER\n(Microcontroller)", colors.HexColor("#1E3A5F"), 6.5)

        pelt_x, pelt_y = 74*mm, h-18*mm
        self._box(c, pelt_x, pelt_y, bw, bh, "PELTIER MODULE\n(TEC)", colors.HexColor("#0E5A67"), 6.5)

        sensor_x, sensor_y = 110*mm, h-18*mm
        self._box(c, sensor_x, sensor_y, bw-5*mm, bh, "TEMP SENSORS\n(x2 or more)", colors.HexColor("#5B21B6"), 6.5)

        # Insulated enclosure (large box)
        enc_x, enc_y = 2*mm, h*0.08
        enc_w = 100*mm; enc_h = h*0.60
        c.setFillColor(colors.HexColor("#E8F4F6"))
        c.roundRect(enc_x, enc_y, enc_w, enc_h, 5, fill=1, stroke=0)
        c.setStrokeColor(TEAL)
        c.setLineWidth(1.5)
        c.roundRect(enc_x, enc_y, enc_w, enc_h, 5, fill=0, stroke=1)
        c.setFillColor(TEAL_DARK)
        c.setFont("Helvetica-Bold", 7)
        c.drawCentredString(enc_x + enc_w/2, enc_y + enc_h - 8, "INSULATED ENCLOSURE")

        # PCM inside enclosure
        pcm_x = enc_x + 5*mm; pcm_y = enc_y + enc_h*0.45
        self._box(c, pcm_x, pcm_y, 42*mm, 10*mm, "PCM CHAMBER\n(Passive Cooling Reserve)", colors.HexColor("#0369A1"), 6.5)

        # Payload inside enclosure
        pay_x = enc_x + 5*mm; pay_y = enc_y + enc_h*0.65
        self._box(c, pay_x, pay_y, 42*mm, 10*mm, "MEDICAL PAYLOAD\n(Temperature-Sensitive)", colors.HexColor("#15803D"), 6.5)

        # Al spreader inside enclosure
        al_x = enc_x + 52*mm; al_y = enc_y + enc_h*0.45
        self._box(c, al_x, al_y, 42*mm, 10*mm, "ALUMINIUM\nHEAT SPREADER", colors.HexColor("#B45309"), 6.5)

        # Liquid chamber inside enclosure
        lq_x = enc_x + 52*mm; lq_y = enc_y + enc_h*0.65
        self._box(c, lq_x, lq_y, 42*mm, 10*mm, "LIQUID THERMAL\nTRANSFER CHAMBER", colors.HexColor("#4338CA"), 6.5)

        # Cold side label
        c.setFillColor(colors.HexColor("#BFDBFE"))
        c.roundRect(enc_x + 5*mm, enc_y + enc_h*0.22, 90*mm, 8*mm, 2, fill=1, stroke=0)
        c.setFillColor(colors.HexColor("#1D4ED8"))
        c.setFont("Helvetica-Bold", 7)
        c.drawCentredString(enc_x + 50*mm, enc_y + enc_h*0.26, "COLD SIDE INTERFACE (Peltier → Al Spreader)")

        # Hot side heat sink (outside enclosure)
        hs_x = 110*mm; hs_y = enc_y + enc_h*0.3
        self._box(c, hs_x, hs_y, 50*mm, 11*mm, "HOT-SIDE HEAT SINK\n/ HEAT EXCHANGER", colors.HexColor("#9F1239"), 6.5)

        self._box(c, 110*mm, enc_y + enc_h*0.55, 50*mm, 11*mm, "AIRFLOW / THERMAL\nREJECTION MEDIUM", colors.HexColor("#6B7280"), 6.5)

        # Arrows
        # PS -> Controller
        self._arrow(c, ps_x+bw, ps_y+bh/2, ctrl_x, ctrl_y+bh/2, colors.HexColor("#374151"), "Power")
        # Controller -> Peltier
        self._arrow(c, ctrl_x+bw, ctrl_y+bh/2, pelt_x, pelt_y+bh/2, colors.HexColor("#7C3AED"), "Control signal")
        # Sensor -> Controller
        self._arrow(c, sensor_x, sensor_y+bh/2, ctrl_x+bw, ctrl_y+bh/2, colors.HexColor("#5B21B6"), "Temp data")
        # Peltier cold -> Al spreader
        self._arrow(c, pelt_x+bw/2, pelt_y, al_x+21*mm, enc_y+enc_h*0.52, colors.HexColor("#1D4ED8"), "Cold")
        # Peltier hot -> Heat sink
        self._arrow(c, pelt_x+bw, pelt_y+bh/2, hs_x, hs_y+bh/2, colors.HexColor("#DC2626"), "Heat (Q_hot)")
        # Sensor line into enclosure
        self._arrow(c, sensor_x+10*mm, sensor_y, sensor_x+10*mm, enc_y+enc_h, colors.HexColor("#5B21B6"), "Monitor")
        # Al spreader <-> Liquid chamber
        self._arrow(c, al_x+21*mm, al_y, al_x+21*mm, lq_y+10*mm, TEAL, "Heat flow")
        # PCM <-> Al spreader
        self._arrow(c, pcm_x+42*mm, pcm_y+5*mm, al_x, al_y+5*mm, TEAL, "Interface")

        # Legend
        legend_y = 2*mm
        c.setFont("Helvetica-Bold", 6)
        c.setFillColor(NAVY)
        c.drawString(2*mm, legend_y+2, "LEGEND:")
        items = [
            (colors.HexColor("#1D4ED8"), "Cold-side heat flow"),
            (colors.HexColor("#DC2626"), "Hot-side heat flow"),
            (colors.HexColor("#7C3AED"), "Electrical / control signal"),
            (TEAL, "Thermal interface"),
        ]
        for i, (col, lbl) in enumerate(items):
            x = 22*mm + i*38*mm
            c.setFillColor(col)
            c.rect(x, legend_y+1, 8*mm, 4, fill=1, stroke=0)
            c.setFillColor(BLACK)
            c.setFont("Helvetica", 5.5)
            c.drawString(x+9*mm, legend_y+1, lbl)

        c.setFillColor(NAVY)
        c.setFont("Helvetica-Bold", 7.5)
        c.drawCentredString(w/2, h-6, "Figure 3 — SANJIVANI System Architecture Block Diagram")

class FlowchartDiagram(Flowable):
    """Operational control flowchart"""
    def __init__(self, width=168*mm, height=130*mm):
        Flowable.__init__(self)
        self.width = width
        self.height = height

    def _rounded_box(self, c, x, y, bw, bh, text, fill_color, text_color=WHITE, font_size=7):
        c.setFillColor(fill_color)
        c.roundRect(x, y, bw, bh, 4, fill=1, stroke=0)
        c.setStrokeColor(colors.HexColor("#94A3B8"))
        c.setLineWidth(0.4)
        c.roundRect(x, y, bw, bh, 4, fill=0, stroke=1)
        c.setFillColor(text_color)
        c.setFont("Helvetica-Bold", font_size)
        lines = text.split('\n')
        for i, line in enumerate(lines):
            c.drawCentredString(x+bw/2,
                y + bh/2 + (len(lines)-1)*4 - i*8 - 2, line)

    def _diamond(self, c, cx, cy, hw, hh, text, fill_color=colors.HexColor("#FEF9C3")):
        pts = [cx, cy+hh, cx+hw, cy, cx, cy-hh, cx-hw, cy]
        c.setFillColor(fill_color)
        _poly(c, pts, fill=1, stroke=0)
        c.setStrokeColor(AMBER_BD)
        c.setLineWidth(0.5)
        _poly(c, pts, fill=0, stroke=1)
        c.setFillColor(colors.HexColor("#7A5C00"))
        c.setFont("Helvetica-Bold", 6.5)
        lines = text.split('\n')
        for i, line in enumerate(lines):
            c.drawCentredString(cx, cy+(len(lines)-1)*4-i*8-2, line)

    def _arr(self, c, x1, y1, x2, y2, label=""):
        c.setStrokeColor(SLATE)
        c.setLineWidth(0.8)
        c.line(x1, y1, x2, y2)
        angle = math.atan2(y2-y1, x2-x1)
        al = 3*mm
        c.setFillColor(SLATE)
        ax = x2 - al*math.cos(angle)
        ay = y2 - al*math.sin(angle)
        _poly(c, [x2, y2,
                   ax+al*0.4*math.sin(angle), ay-al*0.4*math.cos(angle),
                   ax-al*0.4*math.sin(angle), ay+al*0.4*math.cos(angle)],
                  fill=1, stroke=0)
        if label:
            c.setFillColor(TEAL_DARK)
            c.setFont("Helvetica-Bold", 6)
            c.drawString((x1+x2)/2+2, (y1+y2)/2+2, label)

    def draw(self):
        c = self.canv
        w, h = self.width, self.height

        c.setFillColor(colors.HexColor("#F9FAFB"))
        c.roundRect(0, 0, w, h, 5, fill=1, stroke=0)
        c.setStrokeColor(RULE_COLOR)
        c.setLineWidth(0.5)
        c.roundRect(0, 0, w, h, 5, fill=0, stroke=1)

        cx = w/2; bw = 60*mm; bh = 9*mm; gap = 6*mm

        # START
        y = h - 14*mm
        self._rounded_box(c, cx-bw/2, y, bw, bh, "START — System Powered On", colors.HexColor("#1E3A5F"), font_size=7)
        self._arr(c, cx, y, cx, y-gap)

        # PCM initial
        y -= gap + bh
        self._rounded_box(c, cx-bw/2, y, bw, bh, "PCM Provides Passive Cooling", colors.HexColor("#0369A1"), font_size=7)
        self._arr(c, cx, y, cx, y-gap)

        # Sensor read
        y -= gap + bh
        self._rounded_box(c, cx-bw/2, y, bw, bh, "Sensors Sample Internal Temperature", colors.HexColor("#374151"), font_size=7)
        self._arr(c, cx, y, cx, y-gap)

        # Decision: T > T_upper?
        y -= gap + 10*mm
        self._diamond(c, cx, y, bw/2, 7*mm, "T_internal ≥ T_upper\nThreshold?")
        # NO -> loop back
        no_y = y
        self._arr(c, cx-bw/2, no_y, cx-bw/2-15*mm, no_y, "NO")
        c.setStrokeColor(SLATE); c.setLineWidth(0.8)
        c.line(cx-bw/2-15*mm, no_y, cx-bw/2-15*mm, no_y+gap+bh+gap+bh+gap+10*mm+gap+bh+gap)
        self._arr(c, cx-bw/2-15*mm, no_y+gap+bh+gap+bh+gap+10*mm+gap+bh+gap,
                  cx-bw/2, no_y+gap+bh+gap+bh+gap+10*mm+gap+bh+gap)
        # YES -> down
        self._arr(c, cx, y-7*mm, cx, y-7*mm-gap, "YES")

        # Activate Peltier
        y2 = y - 7*mm - gap - bh
        self._rounded_box(c, cx-bw/2, y2, bw, bh, "Activate Peltier Modules", colors.HexColor("#9F1239"), font_size=7)
        self._arr(c, cx, y2, cx, y2-gap)

        # Al spreader / liquid distribute
        y2 -= gap + bh
        self._rounded_box(c, cx-bw/2, y2, bw, bh, "Al Spreader + Liquid Chamber\nDistribute Cold-Side Cooling", colors.HexColor("#4338CA"), font_size=7)
        self._arr(c, cx, y2, cx, y2-gap)

        # T < T_lower?
        y2 -= gap + 10*mm
        self._diamond(c, cx, y2, bw/2, 7*mm, "T_internal ≤ T_lower\nThreshold?")
        # NO -> wait and check again
        self._arr(c, cx+bw/2, y2, cx+bw/2+15*mm, y2, "NO")
        c.line(cx+bw/2+15*mm, y2, cx+bw/2+15*mm, y2+gap+bh+gap)
        self._arr(c, cx+bw/2+15*mm, y2+gap+bh+gap, cx+bw/2, y2+gap+bh+gap)

        # YES -> deactivate
        self._arr(c, cx, y2-7*mm, cx, y2-7*mm-gap, "YES")

        y3 = y2 - 7*mm - gap - bh
        self._rounded_box(c, cx-bw/2, y3, bw, bh, "Deactivate Peltier Modules", colors.HexColor("#374151"), font_size=7)
        self._arr(c, cx, y3, cx, y3-gap)

        # Return to PCM passive
        y3 -= gap + bh
        self._rounded_box(c, cx-bw/2, y3, bw, bh, "Resume PCM Passive Cooling", colors.HexColor("#0369A1"), font_size=7)

        # Arrow back up (right side)
        c.setStrokeColor(SLATE); c.setLineWidth(0.8)
        c.line(cx+bw/2, y3+bh/2, cx+bw/2+30*mm, y3+bh/2)
        c.line(cx+bw/2+30*mm, y3+bh/2, cx+bw/2+30*mm, h-14*mm+bh/2)
        self._arr(c, cx+bw/2+30*mm, h-14*mm+bh/2, cx+bw/2, h-14*mm+bh/2)

        # Title
        c.setFillColor(NAVY)
        c.setFont("Helvetica-Bold", 7.5)
        c.drawCentredString(w/2, h-5, "Figure 4 — SANJIVANI Operational Control Flowchart (Sensor-Triggered Hysteresis Cycle)")

class ThermalFlowDiagram(Flowable):
    """Thermal pathway diagram"""
    def __init__(self, width=168*mm, height=65*mm):
        Flowable.__init__(self)
        self.width = width
        self.height = height

    def draw(self):
        c = self.canv
        w, h = self.width, self.height

        c.setFillColor(colors.HexColor("#F0F7F9"))
        c.roundRect(0, 0, w, h, 5, fill=1, stroke=0)
        c.setStrokeColor(RULE_COLOR)
        c.setLineWidth(0.5)
        c.roundRect(0, 0, w, h, 5, fill=0, stroke=1)

        nodes = [
            ("Ambient\nEnvironment", colors.HexColor("#9F1239"), 5*mm),
            ("Insulation\nLayer", colors.HexColor("#B45309"), 32*mm),
            ("PCM\nChamber", colors.HexColor("#0369A1"), 59*mm),
            ("Al Heat\nSpreader", colors.HexColor("#0E5A67"), 86*mm),
            ("Peltier\nModule", colors.HexColor("#1E3A5F"), 113*mm),
            ("Hot-Side\nHeat Sink", colors.HexColor("#7C2D12"), 140*mm),
        ]

        bw = 24*mm; bh = 20*mm; ny = h/2-bh/2

        for label, col, x in nodes:
            c.setFillColor(col)
            c.roundRect(x, ny, bw, bh, 3, fill=1, stroke=0)
            c.setFillColor(WHITE)
            c.setFont("Helvetica-Bold", 6.5)
            lines = label.split('\n')
            for i, ln in enumerate(lines):
                c.drawCentredString(x+bw/2, ny+bh/2+(len(lines)-1)*4-i*8-2, ln)

        # Arrows between nodes + labels
        arrow_data = [
            (5*mm+bw, "Heat ingress\n(Q_in)", "red"),
            (32*mm+bw, "Thermal\nleakage", "orange"),
            (59*mm+bw, "PCM absorbs\nheat (passive)", "blue"),
            (86*mm+bw, "Cold-side\ninterface", "teal"),
            (113*mm+bw, "Q_hot rejected\nto environment", "red"),
        ]
        for x1, label, cname in arrow_data:
            col = {"red": colors.HexColor("#DC2626"),
                   "orange": colors.HexColor("#D97706"),
                   "blue": colors.HexColor("#1D4ED8"),
                   "teal": TEAL_DARK}[cname]
            c.setStrokeColor(col); c.setLineWidth(1.2)
            c.line(x1+1, h/2, x1+bw-5*mm, h/2)
            ax = x1+bw-5*mm; ay = h/2
            c.setFillColor(col)
            _poly(c, [ax+3*mm, ay, ax, ay+2*mm, ax, ay-2*mm], fill=1, stroke=0)
            c.setFont("Helvetica", 5.5)
            c.setFillColor(SLATE)
            for j, ln in enumerate(label.split('\n')):
                c.drawCentredString(x1+bw/2+1*mm, ny-9+j*7, ln)

        # Peltier power input
        pelt_x = 113*mm + bw/2
        c.setStrokeColor(colors.HexColor("#7C3AED")); c.setLineWidth(1)
        c.line(pelt_x, ny+bh+1*mm, pelt_x, ny+bh+8*mm)
        c.setFillColor(colors.HexColor("#7C3AED"))
        _poly(c, [pelt_x, ny+bh, pelt_x-2*mm, ny+bh+5*mm, pelt_x+2*mm, ny+bh+5*mm], fill=1, stroke=0)
        c.setFont("Helvetica-Bold", 6)
        c.drawCentredString(pelt_x, ny+bh+11*mm, "P_elec (DC input)")

        c.setFillColor(NAVY)
        c.setFont("Helvetica-Bold", 7.5)
        c.drawCentredString(w/2, h-5, "Figure 5 — SANJIVANI Thermal Pathway: Heat Flow from Environment to Rejection")

class ExperimentalSetupDiagram(Flowable):
    """Experimental setup schematic"""
    def __init__(self, width=168*mm, height=55*mm):
        Flowable.__init__(self)
        self.width = width
        self.height = height

    def draw(self):
        c = self.canv
        w, h = self.width, self.height

        c.setFillColor(colors.HexColor("#F9FAFB"))
        c.roundRect(0, 0, w, h, 5, fill=1, stroke=0)
        c.setStrokeColor(RULE_COLOR); c.setLineWidth(0.5)
        c.roundRect(0, 0, w, h, 5, fill=0, stroke=1)

        # Config A
        c.setFillColor(colors.HexColor("#DBEAFE"))
        c.roundRect(5*mm, h*0.15, 70*mm, h*0.65, 4, fill=1, stroke=0)
        c.setFillColor(colors.HexColor("#1D4ED8"))
        c.setFont("Helvetica-Bold", 7.5)
        c.drawCentredString(40*mm, h*0.75, "CONFIGURATION A")
        c.setFont("Helvetica", 7)
        c.setFillColor(SLATE)
        c.drawCentredString(40*mm, h*0.65, "PCM-Only (Conventional)")
        for i, item in enumerate(["Insulated enclosure", "PCM chamber", "Temp sensors (logging)", "No active cooling"]):
            c.drawCentredString(40*mm, h*0.52 - i*9, f"• {item}")

        # Config B
        c.setFillColor(colors.HexColor("#D1FAE5"))
        c.roundRect(93*mm, h*0.15, 70*mm, h*0.65, 4, fill=1, stroke=0)
        c.setFillColor(colors.HexColor("#065F46"))
        c.setFont("Helvetica-Bold", 7.5)
        c.drawCentredString(128*mm, h*0.75, "CONFIGURATION B")
        c.setFont("Helvetica", 7)
        c.setFillColor(SLATE)
        c.drawCentredString(128*mm, h*0.65, "SANJIVANI Hybrid (PCM + Peltier)")
        for i, item in enumerate(["Insulated enclosure", "PCM + Al spreader", "Peltier + liquid chamber", "Sensor-triggered control"]):
            c.drawCentredString(128*mm, h*0.52 - i*9, f"• {item}")

        # VS
        c.setFillColor(GOLD)
        c.circle(84*mm, h/2, 7*mm, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 9)
        c.drawCentredString(84*mm, h/2-3, "VS")

        c.setFillColor(NAVY)
        c.setFont("Helvetica-Bold", 7.5)
        c.drawCentredString(w/2, h-5, "Figure 6 — Comparative Experimental Setup: Configuration A vs Configuration B")

# ─────────────────────────── PAGE BUILDERS ────────────────────────────

def build_cover(c, doc):
    """Draw the cover page entirely on canvas"""
    cw, ch = A4

    # Background gradient effect (layered rectangles)
    c.setFillColor(NAVY)
    c.rect(0, 0, cw, ch, fill=1, stroke=0)

    # Decorative side bar
    c.setFillColor(TEAL)
    c.rect(0, 0, 8*mm, ch, fill=1, stroke=0)
    c.setFillColor(TEAL_DARK)
    c.rect(cw-8*mm, 0, 8*mm, ch, fill=1, stroke=0)

    # Top accent band
    c.setFillColor(TEAL)
    c.rect(0, ch-30*mm, cw, 30*mm, fill=1, stroke=0)

    # Bottom accent band
    c.setFillColor(colors.HexColor("#0A1520"))
    c.rect(0, 0, cw, 50*mm, fill=1, stroke=0)

    # Geometric decorative circles (subtle)
    c.setStrokeColor(colors.HexColor("#1A4A5A"))
    c.setLineWidth(0.5)
    for r in [30, 50, 70, 90]:
        c.circle(cw-15*mm, ch-15*mm, r*mm, fill=0, stroke=1)

    # School name in top band
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(cw/2, ch-13*mm,
        "Participating Institution (School UID: SBVPH-05)")
    c.setFont("Helvetica", 9)
    c.setFillColor(colors.HexColor("#B8D4E0"))
    c.drawCentredString(cw/2, ch-21*mm,
        "Dr. B. K. Passi Memorial Senior Bal Vigyan 2026–2027")

    # Cold-chain icon (simplified vector — insulated box)
    icon_x, icon_y = cw/2 - 25*mm, ch - 110*mm
    icon_w, icon_h = 50*mm, 35*mm
    # Outer box
    c.setFillColor(colors.HexColor("#1A4A5A"))
    c.roundRect(icon_x, icon_y, icon_w, icon_h, 5, fill=1, stroke=0)
    c.setStrokeColor(TEAL)
    c.setLineWidth(1)
    c.roundRect(icon_x, icon_y, icon_w, icon_h, 5, fill=0, stroke=1)
    # Inner box (payload)
    c.setFillColor(colors.HexColor("#0D3040"))
    c.roundRect(icon_x+5*mm, icon_y+5*mm, icon_w-10*mm, icon_h-14*mm, 3, fill=1, stroke=0)
    # Temperature symbol
    c.setFillColor(TEAL)
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(icon_x+icon_w/2, icon_y+12*mm, "❄")
    # Sensor line
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.7)
    c.line(icon_x+icon_w/2, icon_y+icon_h, icon_x+icon_w/2, icon_y+icon_h+8*mm)
    c.setFillColor(GOLD)
    c.circle(icon_x+icon_w/2, icon_y+icon_h+9*mm, 1.5*mm, fill=1, stroke=0)

    # SANJIVANI main title
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 54)
    c.drawCentredString(cw/2, ch - 148*mm, "SANJIVANI")

    # Sanskrit
    c.setFillColor(colors.HexColor("#B8D4E0"))
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(cw/2, ch - 160*mm, "\u0938\u0902\u091c\u0940\u0935\u0928\u0940")

    # Tagline
    c.setFillColor(GOLD)
    c.setFont("Helvetica-BoldOblique", 11)
    c.drawCentredString(cw/2, ch - 171*mm, "Preserving Temperature.  Protecting Life.")

    # Subtitle
    c.setFillColor(TEAL)
    c.rect(10*mm, ch-182*mm, cw-20*mm, 0.5, fill=1, stroke=0)
    c.setFillColor(colors.HexColor("#7EC8D8"))
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(cw/2, ch-191*mm, "Hybrid PCM–Peltier Medical Cold-Chain System")
    c.setFillColor(TEAL)
    c.rect(10*mm, ch-195*mm, cw-20*mm, 0.5, fill=1, stroke=0)

    # Formal title
    c.setFillColor(colors.HexColor("#D0E8F0"))
    c.setFont("Helvetica", 8.5)
    title_lines = [
        "Design and Development of a Sensor-Triggered Hybrid PCM–Thermoelectric",
        "Cooling System for Extended Medical Cold-Chain Storage"
    ]
    for i, line in enumerate(title_lines):
        c.drawCentredString(cw/2, ch - 204*mm - i*11, line)

    # Info box at bottom
    c.setFillColor(colors.HexColor("#0A1520"))
    c.roundRect(10*mm, 8*mm, cw-20*mm, 42*mm, 5, fill=1, stroke=0)
    c.setStrokeColor(TEAL)
    c.setLineWidth(0.7)
    c.roundRect(10*mm, 8*mm, cw-20*mm, 42*mm, 5, fill=0, stroke=1)

    # Participant names
    c.setFillColor(TEAL)
    c.setFont("Helvetica-Bold", 7)
    c.drawString(14*mm, 44*mm, "PROJECT PARTICIPANTS:")
    participants = [
        "Vaishnavi Shrivastava — Class XI",
        "Gaurav Choudhary — Class XI",
        "Prathamesh Rao — Class XII",
        "Bhavmanyu Singh — Class XII",
    ]
    c.setFillColor(WHITE)
    c.setFont("Helvetica", 8)
    for i, p in enumerate(participants):
        col = 14*mm if i < 2 else 110*mm
        row = 38*mm - (i % 2)*8*mm
        c.drawString(col, row, f"• {p}")

    # Mentor / Subject / Theme
    c.setFillColor(colors.HexColor("#7EC8D8"))
    c.setFont("Helvetica-Bold", 7)
    c.drawString(14*mm, 27*mm, "MENTOR TEACHER:")
    c.setFillColor(WHITE)
    c.setFont("Helvetica", 8)
    c.drawString(55*mm, 27*mm, "Mr. Gopal Kumar Roy")

    c.setFillColor(colors.HexColor("#7EC8D8"))
    c.setFont("Helvetica-Bold", 7)
    c.drawString(14*mm, 20*mm, "SUBJECT: Physics  |  THEME: STEM for Viksit and Atmanirbhar Bharat  |  SUB-THEME: Health and Hygiene")

    # Registration code
    c.setFillColor(AMBER_BD)
    c.roundRect(14*mm, 11*mm, 100*mm, 7*mm, 2, fill=1, stroke=0)
    c.setFillColor(colors.HexColor("#7A5C00"))
    c.setFont("Helvetica-Bold", 7)
    c.drawString(16*mm, 13.5*mm, "UNIQUE REGISTRATION CODE: [ TO BE FILLED BY TEACHER / ORGANISER ]")

    c.setFillColor(WHITE)
    c.setFont("Helvetica", 7)
    c.drawString(118*mm, 13.5*mm, "PRINCIPAL: Dr. Ashish Arora")


def on_later_pages(canvas_obj, doc):
    """Header/footer for pages 2+"""
    canvas_obj.saveState()
    pw, ph = A4
    page_num = doc.page

    # Header bar
    canvas_obj.setFillColor(NAVY)
    canvas_obj.rect(L_MARGIN, ph - T_MARGIN - 7*mm, pw - L_MARGIN - R_MARGIN, 7*mm, fill=1, stroke=0)
    canvas_obj.setFillColor(WHITE)
    canvas_obj.setFont("Helvetica-Bold", 7)
    canvas_obj.drawString(L_MARGIN + 3*mm, ph - T_MARGIN - 4.5*mm, "SANJIVANI — Hybrid PCM–Peltier Medical Cold-Chain System")
    canvas_obj.setFont("Helvetica", 7)
    canvas_obj.drawRightString(pw - R_MARGIN - 3*mm, ph - T_MARGIN - 4.5*mm,
        "Dr. B. K. Passi Memorial Senior Bal Vigyan 2026–2027")

    # Footer
    canvas_obj.setFillColor(RULE_COLOR)
    canvas_obj.rect(L_MARGIN, B_MARGIN, pw - L_MARGIN - R_MARGIN, 0.3*mm, fill=1, stroke=0)
    canvas_obj.setFillColor(SLATE)
    canvas_obj.setFont("Helvetica", 7)
    canvas_obj.drawString(L_MARGIN, B_MARGIN - 4*mm,
        "School UID: SBVPH-05  |  Mentor: Mr. Gopal Kumar Roy")
    canvas_obj.drawRightString(pw - R_MARGIN, B_MARGIN - 4*mm,
        f"Page {page_num}")

    # Teal side accent
    canvas_obj.setFillColor(TEAL)
    canvas_obj.rect(0, 0, 3*mm, ph, fill=1, stroke=0)

    canvas_obj.restoreState()


# ─────────────────────────── CONTENT BUILDERS ─────────────────────────

def page2_certificate(S):
    story = []
    story.append(Spacer(1, 8*mm))
    story.append(section_banner("CERTIFICATE OF ORIGINAL PROJECT WORK"))
    story.append(Spacer(1, 6*mm))

    # Decorative border note
    story.append(Paragraph(
        "This is to certify that the following students of <b>School UID: SBVPH-05, "
        "Madhya Pradesh</b> have independently undertaken and completed the project entitled:",
        S['cert_body']))
    story.append(Spacer(1, 4*mm))

    # Project title box
    t = Table([[Paragraph(
        "<b>SANJIVANI: Design and Development of a Sensor-Triggered Hybrid PCM–Thermoelectric "
        "Cooling System for Extended Medical Cold-Chain Storage</b>",
        ParagraphStyle('ptitle', fontName='Helvetica-BoldOblique', fontSize=11,
                       textColor=TEAL_DARK, alignment=TA_CENTER, leading=16))]],
        style=TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), TEAL_LIGHT),
            ('BOX', (0,0), (-1,-1), 1, TEAL),
            ('TOPPADDING', (0,0), (-1,-1), 8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('LEFTPADDING', (0,0), (-1,-1), 10),
            ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ]))
    story.append(t)
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph(
        "under the guidance of <b>Mr. Gopal Kumar Roy</b>, Mentor Teacher, as a submission for the "
        "<b>Dr. B. K. Passi Memorial Senior Bal Vigyan 2026–2027</b>. "
        "The work presented is genuine, original and has been carried out by the students named below "
        "to the best of our knowledge. All sources of information have been duly acknowledged within the report.",
        S['cert_body']))
    story.append(Spacer(1, 4*mm))

    # Participants table
    ptable = Table([
        [Paragraph("<b>Participant Name</b>", S['table_header']),
         Paragraph("<b>Class</b>", S['table_header']),
         Paragraph("<b>Role</b>", S['table_header'])],
        [Paragraph("Vaishnavi Shrivastava", S['table_cell']),
         Paragraph("XI", S['table_cell_c']),
         Paragraph("Project Participant", S['table_cell'])],
        [Paragraph("Gaurav Choudhary", S['table_cell']),
         Paragraph("XI", S['table_cell_c']),
         Paragraph("Project Participant", S['table_cell'])],
        [Paragraph("Prathamesh Rao", S['table_cell']),
         Paragraph("XII", S['table_cell_c']),
         Paragraph("Project Participant", S['table_cell'])],
        [Paragraph("Bhavmanyu Singh", S['table_cell']),
         Paragraph("XII", S['table_cell_c']),
         Paragraph("Project Participant", S['table_cell'])],
    ], colWidths=[90*mm, 25*mm, 55*mm],
    style=TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('BACKGROUND', (0,1), (-1,1), TABLE_BG),
        ('BACKGROUND', (0,2), (-1,2), WHITE),
        ('BACKGROUND', (0,3), (-1,3), TABLE_BG),
        ('BACKGROUND', (0,4), (-1,4), WHITE),
        ('BOX', (0,0), (-1,-1), 0.5, RULE_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.3, RULE_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
        ('RIGHTPADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(ptable)
    story.append(Spacer(1, 6*mm))

    story.append(Paragraph(
        "The report is submitted in fulfilment of the requirements of the competition and represents "
        "the students' own engineering investigation and analysis. This project has not been submitted "
        "to any other competition or institution.",
        S['cert_body']))
    story.append(Spacer(1, 8*mm))

    # Signature row
    sig_data = [
        [Paragraph("____________________________", S['cert_body']),
         Paragraph("____________________________", S['cert_body']),
         Paragraph("____________________________", S['cert_body'])],
        [Paragraph("<b>Mr. Gopal Kumar Roy</b>", S['cert_name']),
         Paragraph("<b>Dr. Ashish Arora</b>", S['cert_name']),
         Paragraph("<b>School Seal</b>", S['cert_name'])],
        [Paragraph("Mentor Teacher", S['body_sm']),
         Paragraph("Principal", S['body_sm']),
         Paragraph("", S['body_sm'])],
        [Paragraph("Date: ___________", S['body_sm']),
         Paragraph("Date: ___________", S['body_sm']),
         ph("OFFICIAL SCHOOL SEAL")],
    ]
    sig_t = Table(sig_data, colWidths=[56*mm, 56*mm, 56*mm],
                  style=TableStyle([
                      ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                      ('VALIGN', (0,0), (-1,-1), 'TOP'),
                      ('TOPPADDING', (0,0), (-1,-1), 4),
                      ('BOTTOMPADDING', (0,0), (-1,-1), 4),
                  ]))
    story.append(sig_t)
    story.append(Spacer(1, 4*mm))

    reg_row = [ph("Competition Registration Number: ____________________   |   "
                  "Project Code: ____________   |   School Code: ____________")]
    story.append(Table([reg_row], style=TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), AMBER_PH),
        ('BOX', (0,0), (-1,-1), 0.5, AMBER_BD),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
    ])))
    return story


def page3_declaration(S):
    story = []
    story.append(Spacer(1, 8*mm))
    story.append(section_banner("DECLARATION OF ORIGINALITY"))
    story.append(Spacer(1, 6*mm))
    story.append(Paragraph(
        "We, the undersigned students of <b>School UID: SBVPH-05</b>, hereby declare that:",
        S['cert_body']))
    story.append(Spacer(1, 4*mm))

    declarations = [
        ("1.", "The project report titled <b>SANJIVANI: Design and Development of a Sensor-Triggered "
               "Hybrid PCM–Thermoelectric Cooling System for Extended Medical Cold-Chain Storage</b> "
               "represents our own original work carried out for the Dr. B. K. Passi Memorial Senior "
               "Bal Vigyan 2026–2027."),
        ("2.", "The engineering principles, system design, prototype development process and experimental "
               "methodology described in this report have been developed by us under the guidance of "
               "our mentor, <b>Mr. Gopal Kumar Roy</b>."),
        ("3.", "All external sources of information — including textbooks, technical datasheets, research "
               "articles, official guidelines and online references — have been appropriately acknowledged "
               "in the References section of this report."),
        ("4.", "Wherever component specifications, experimental measurements or design parameters are "
               "yet to be confirmed or recorded, they have been clearly marked as placeholders. "
               "No experimental results have been fabricated or invented."),
        ("5.", "The report clearly and consistently distinguishes between (a) the proposed design concept, "
               "(b) assembled prototype components, (c) measured experimental data and (d) future "
               "engineering possibilities."),
        ("6.", "This report has not been submitted in its present form to any other competition, "
               "institution or publication."),
        ("7.", "We understand that any misrepresentation of experimental data or deliberate plagiarism "
               "constitutes academic misconduct and accept full responsibility for the content of this report."),
    ]

    for num, text in declarations:
        d_row = [[Paragraph(f"<b>{num}</b>", S['body']),
                  Paragraph(text, S['body'])]]
        d_t = Table(d_row, colWidths=[8*mm, 158*mm],
                    style=TableStyle([
                        ('VALIGN', (0,0), (-1,-1), 'TOP'),
                        ('TOPPADDING', (0,0), (-1,-1), 2),
                        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
                    ]))
        story.append(d_t)

    story.append(Spacer(1, 8*mm))
    story.append(Paragraph("Signatures of Project Participants:", S['subsection_heading']))
    story.append(Spacer(1, 4*mm))

    sig_data = [
        [Paragraph("________________________", S['body']),
         Paragraph("________________________", S['body']),
         Paragraph("________________________", S['body']),
         Paragraph("________________________", S['body'])],
        [Paragraph("Vaishnavi Shrivastava", S['cert_name']),
         Paragraph("Gaurav Choudhary", S['cert_name']),
         Paragraph("Prathamesh Rao", S['cert_name']),
         Paragraph("Bhavmanyu Singh", S['cert_name'])],
        [Paragraph("Class XI", S['body_sm']),
         Paragraph("Class XI", S['body_sm']),
         Paragraph("Class XII", S['body_sm']),
         Paragraph("Class XII", S['body_sm'])],
        [Paragraph("Date: __________", S['body_sm']),
         Paragraph("Date: __________", S['body_sm']),
         Paragraph("Date: __________", S['body_sm']),
         Paragraph("Date: __________", S['body_sm'])],
    ]
    sig_t = Table(sig_data, colWidths=[42*mm, 42*mm, 42*mm, 42*mm],
                  style=TableStyle([
                      ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                      ('VALIGN', (0,0), (-1,-1), 'TOP'),
                      ('TOPPADDING', (0,0), (-1,-1), 3),
                      ('BOTTOMPADDING', (0,0), (-1,-1), 3),
                  ]))
    story.append(sig_t)
    story.append(Spacer(1, 6*mm))
    story.append(Paragraph(
        "<i>Place: Indore, Madhya Pradesh</i>",
        ParagraphStyle('italic_sm', fontName='Helvetica-Oblique', fontSize=9, textColor=SLATE,
                       alignment=TA_LEFT)))
    return story


def page4_acknowledgement(S):
    story = []
    story.append(Spacer(1, 8*mm))
    story.append(section_banner("ACKNOWLEDGEMENT"))
    story.append(Spacer(1, 6*mm))

    story.append(Paragraph(
        "We consider it our foremost privilege to express our sincere gratitude to all those whose "
        "guidance, encouragement and support have made this project possible.",
        S['ack_body']))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(
        "We place on record our deepest respect and appreciation for <b>Dr. Ashish Arora, Principal, "
        "School UID: SBVPH-05</b>, whose visionary academic leadership continually "
        "encourages students to pursue innovation in science and engineering. His consistent support "
        "for science activities at the school has inspired this project.",
        S['ack_body']))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(
        "We owe our deepest gratitude to our Mentor Teacher, <b>Mr. Gopal Kumar Roy</b>, without whose "
        "unwavering guidance, technical clarity and patient mentorship this project would not have taken "
        "shape. Mr. Roy's ability to translate complex engineering ideas into understandable concepts "
        "has shaped the scientific foundation of SANJIVANI. He generously offered his time, expertise "
        "and constructive criticism at every stage of this investigation.",
        S['ack_body']))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(
        "We wish to express our heartfelt thanks to the management and faculty of <b>G. D. Goenka Public "
        "School, Indore</b>, for providing access to the school laboratory, necessary materials and an "
        "environment that nurtures scientific enquiry. We are especially grateful to our Science Department "
        "colleagues whose discussions enriched our understanding of thermal physics.",
        S['ack_body']))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(
        "We acknowledge our student observers, <b>Konav Singh (Class XI)</b> and "
        "<b>Animesh Mishra</b>, for their participation in observational sessions and their "
        "thoughtful feedback during the project development phase.",
        S['ack_body']))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(
        "Our heartfelt thanks go to our parents and families, whose moral support, understanding and "
        "encouragement sustained us throughout the demanding process of research, design and documentation. "
        "Their belief in our work has been our greatest motivation.",
        S['ack_body']))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(
        "We also acknowledge the organisers of the <b>Dr. B. K. Passi Memorial Senior Bal Vigyan "
        "2026–2027</b> competition for providing a platform that encourages young students to engage "
        "seriously with science and engineering challenges relevant to society.",
        S['ack_body']))
    story.append(Spacer(1, 6*mm))
    story.append(hr())
    story.append(Spacer(1, 4*mm))
    story.append(Paragraph(
        "<i>Vaishnavi Shrivastava &nbsp;·&nbsp; Gaurav Choudhary &nbsp;·&nbsp; "
        "Prathamesh Rao &nbsp;·&nbsp; Bhavmanyu Singh</i>",
        ParagraphStyle('ack_names', fontName='Helvetica-BoldOblique', fontSize=10,
                       textColor=TEAL_DARK, alignment=TA_CENTER, leading=14)))
    story.append(Paragraph(
        "School UID: SBVPH-05",
        ParagraphStyle('ack_school', fontName='Helvetica', fontSize=9,
                       textColor=SLATE, alignment=TA_CENTER, leading=12)))
    return story


def page5_particulars(S):
    story = []
    story.append(Spacer(1, 8*mm))
    story.append(section_banner("PROJECT AND TEAM PARTICULARS"))
    story.append(Spacer(1, 5*mm))

    story.append(teal_banner("A. Project Details"))
    story.append(Spacer(1, 2*mm))
    proj_info = [
        ["Project Name:", "SANJIVANI (संजीवनी)"],
        ["Full Title:", "Design and Development of a Sensor-Triggered Hybrid PCM–Thermoelectric Cooling System for Extended Medical Cold-Chain Storage"],
        ["Tagline:", "Preserving Temperature. Protecting Life."],
        ["Competition:", "Dr. B. K. Passi Memorial Senior Bal Vigyan 2026–2027"],
        ["Subject / Category:", "Physics / Thermal Engineering / Healthcare Technology"],
        ["Theme:", "STEM for Viksit and Atmanirbhar Bharat"],
        ["Sub-Theme:", "Health and Hygiene"],
        ["School:", "Participating Institution (School UID: SBVPH-05)"],
        ["Principal:", "Dr. Ashish Arora"],
        ["Mentor Teacher:", "Mr. Gopal Kumar Roy"],
        ["Unique Registration Code:", "[ TO BE FILLED BY TEACHER / ORGANISER ]"],
        ["School Code:", "[ TO BE FILLED IF REQUIRED ]"],
        ["Project Code:", "[ TO BE FILLED IF REQUIRED ]"],
        ["Date of Submission:", "[ TO BE FILLED ]"],
    ]
    rows = []
    for label, value in proj_info:
        is_ph = "TO BE FILLED" in value or "[ " in value
        v_style = S['placeholder'] if is_ph else S['table_cell']
        rows.append([
            Paragraph(f"<b>{label}</b>", S['table_cell']),
            Paragraph(value, v_style)
        ])
    story.append(Table(rows, colWidths=[55*mm, 115*mm],
                       style=TableStyle([
                           ('ROWBACKGROUNDS', (0,0), (-1,-1), [TABLE_BG, WHITE]),
                           ('BOX', (0,0), (-1,-1), 0.5, RULE_COLOR),
                           ('INNERGRID', (0,0), (-1,-1), 0.3, RULE_COLOR),
                           ('TOPPADDING', (0,0), (-1,-1), 4),
                           ('BOTTOMPADDING', (0,0), (-1,-1), 4),
                           ('LEFTPADDING', (0,0), (-1,-1), 6),
                           ('RIGHTPADDING', (0,0), (-1,-1), 6),
                           ('VALIGN', (0,0), (-1,-1), 'TOP'),
                       ])))
    story.append(Spacer(1, 5*mm))

    story.append(teal_banner("B. Project Participants"))
    story.append(Spacer(1, 2*mm))
    p_rows = [
        [Paragraph("<b>No.</b>", S['table_header']),
         Paragraph("<b>Name</b>", S['table_header']),
         Paragraph("<b>Class</b>", S['table_header']),
         Paragraph("<b>Role</b>", S['table_header'])],
        [Paragraph("1", S['table_cell_c']), Paragraph("Vaishnavi Shrivastava", S['table_cell']),
         Paragraph("XI", S['table_cell_c']), Paragraph("Project Participant", S['table_cell'])],
        [Paragraph("2", S['table_cell_c']), Paragraph("Gaurav Choudhary", S['table_cell']),
         Paragraph("XI", S['table_cell_c']), Paragraph("Project Participant", S['table_cell'])],
        [Paragraph("3", S['table_cell_c']), Paragraph("Prathamesh Rao", S['table_cell']),
         Paragraph("XII", S['table_cell_c']), Paragraph("Project Participant", S['table_cell'])],
        [Paragraph("4", S['table_cell_c']), Paragraph("Bhavmanyu Singh", S['table_cell']),
         Paragraph("XII", S['table_cell_c']), Paragraph("Project Participant", S['table_cell'])],
    ]
    story.append(Table(p_rows, colWidths=[12*mm, 70*mm, 20*mm, 68*mm],
                       style=TableStyle([
                           ('BACKGROUND', (0,0), (-1,0), NAVY),
                           ('ROWBACKGROUNDS', (0,1), (-1,-1), [TABLE_BG, WHITE]),
                           ('BOX', (0,0), (-1,-1), 0.5, RULE_COLOR),
                           ('INNERGRID', (0,0), (-1,-1), 0.3, RULE_COLOR),
                           ('TOPPADDING', (0,0), (-1,-1), 4),
                           ('BOTTOMPADDING', (0,0), (-1,-1), 4),
                           ('LEFTPADDING', (0,0), (-1,-1), 6),
                           ('RIGHTPADDING', (0,0), (-1,-1), 6),
                       ])))
    story.append(Spacer(1, 5*mm))

    story.append(teal_banner("C. Student Observers (Non-Participant)"))
    story.append(Spacer(1, 2*mm))
    obs_rows = [
        [Paragraph("<b>No.</b>", S['table_header']),
         Paragraph("<b>Name</b>", S['table_header']),
         Paragraph("<b>Class</b>", S['table_header']),
         Paragraph("<b>Role</b>", S['table_header'])],
        [Paragraph("1", S['table_cell_c']), Paragraph("Konav Singh", S['table_cell']),
         Paragraph("XI", S['table_cell_c']), Paragraph("Student Observer", S['table_cell'])],
        [Paragraph("2", S['table_cell_c']), Paragraph("Animesh Mishra", S['table_cell']),
         Paragraph("[ Class to be confirmed ]", S['placeholder']), Paragraph("Student Observer", S['table_cell'])],
    ]
    story.append(Table(obs_rows, colWidths=[12*mm, 70*mm, 50*mm, 38*mm],
                       style=TableStyle([
                           ('BACKGROUND', (0,0), (-1,0), TEAL),
                           ('ROWBACKGROUNDS', (0,1), (-1,-1), [TABLE_BG, WHITE]),
                           ('BOX', (0,0), (-1,-1), 0.5, RULE_COLOR),
                           ('INNERGRID', (0,0), (-1,-1), 0.3, RULE_COLOR),
                           ('TOPPADDING', (0,0), (-1,-1), 4),
                           ('BOTTOMPADDING', (0,0), (-1,-1), 4),
                           ('LEFTPADDING', (0,0), (-1,-1), 6),
                           ('RIGHTPADDING', (0,0), (-1,-1), 6),
                       ])))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(
        "<i>Note: Student observers attended project sessions and contributed to observational discussions "
        "but are not project authors. The four named participants above are solely responsible for the "
        "engineering investigation reported herein.</i>",
        ParagraphStyle('note', fontName='Helvetica-Oblique', fontSize=8, textColor=SLATE,
                       alignment=TA_LEFT, leading=12)))
    return story


def page6_abstract(S):
    story = []
    story.append(Spacer(1, 8*mm))
    story.append(section_banner("ABSTRACT"))
    story.append(Spacer(1, 5*mm))

    story.append(Paragraph(
        "Maintaining an unbroken medical cold chain is critical for preserving the efficacy of vaccines, "
        "insulin, blood products and other temperature-sensitive biological materials. Conventional "
        "Phase Change Material (PCM)-based portable coolers offer a passive, energy-independent thermal "
        "buffer that can maintain a defined temperature range for a limited duration — typically around "
        "72 hours under assumed standard conditions. However, extended transportation routes, delayed "
        "last-mile delivery and adverse ambient temperatures frequently exceed this passive capacity, "
        "creating temperature excursions that may compromise medical product quality.",
        S['body']))
    story.append(Spacer(1, 2*mm))
    story.append(Paragraph(
        "<b>SANJIVANI</b> proposes a hybrid thermal management architecture that integrates "
        "sensor-triggered Peltier thermoelectric cooling with an existing PCM-based insulated enclosure. "
        "The system design comprises six principal components operating in an intelligent control cycle: "
        "(i) a PCM chamber that provides the primary passive thermal reserve; "
        "(ii) digital temperature sensors that continuously monitor the internal thermal condition; "
        "(iii) a microcontroller that implements a threshold-based hysteresis control strategy; "
        "(iv) Peltier thermoelectric modules that deliver supplementary active cooling when the internal "
        "temperature approaches a predefined upper threshold; "
        "(v) an aluminium heat-spreading structure that distributes cold-side cooling across the thermal "
        "interface; and "
        "(vi) a liquid-based thermal transfer arrangement combined with a hot-side heat-rejection pathway "
        "that removes excess heat from the thermoelectric assembly.",
        S['body']))
    story.append(Spacer(1, 2*mm))
    story.append(Paragraph(
        "The proposed operating logic follows a duty-cycled pattern: Peltier cooling is activated only when "
        "required and deactivated once the lower temperature threshold is re-established, thereby reducing "
        "unnecessary electrical energy consumption and partially restoring the PCM's latent heat reserve. "
        "The design target is to extend the useful temperature-holding duration from an assumed baseline "
        "of approximately 72 hours towards approximately 110 hours. These figures represent preliminary "
        "engineering assumptions and experimental targets; they are not independently verified results.",
        S['body']))
    story.append(Spacer(1, 2*mm))
    story.append(Paragraph(
        "A comparative experimental protocol is proposed, contrasting Configuration A "
        "(PCM-only passive cooling) against Configuration B (the SANJIVANI hybrid system) under identical "
        "initial conditions and ambient environments. Temperature profiles, electrical energy consumption "
        "and duty-cycle data will be recorded to evaluate the system's thermal and electrical performance. "
        "Safety considerations, engineering limitations and future optimisation directions are discussed.",
        S['body']))
    story.append(Spacer(1, 2*mm))
    story.append(Paragraph(
        "<i>This report clearly distinguishes between the proposed design, the assembled prototype, "
        "planned experimental measurements and future engineering possibilities. No experimental results "
        "are presented as confirmed outcomes at the time of submission.</i>",
        ParagraphStyle('note_i', fontName='Helvetica-Oblique', fontSize=9, textColor=SLATE,
                       alignment=TA_JUSTIFY, leading=13)))
    story.append(Spacer(1, 5*mm))

    # Keywords
    kw_box = Table([[Paragraph(
        "<b>Keywords:</b> Phase Change Material (PCM) · Peltier thermoelectric cooling · "
        "Medical cold chain · Thermal management · Sensor-triggered control · "
        "Latent heat storage · Hybrid cooling system",
        S['keyword'])]], style=TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), TEAL_LIGHT),
            ('BOX', (0,0), (-1,-1), 0.8, TEAL),
            ('TOPPADDING', (0,0), (-1,-1), 7),
            ('BOTTOMPADDING', (0,0), (-1,-1), 7),
            ('LEFTPADDING', (0,0), (-1,-1), 10),
            ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ]))
    story.append(kw_box)
    return story


def page7_toc(S):
    story = []
    story.append(Spacer(1, 8*mm))
    story.append(section_banner("TABLE OF CONTENTS"))
    story.append(Spacer(1, 5*mm))

    toc_entries = [
        ("PAGE 1", "Cover Page", "1"),
        ("PAGE 2", "Certificate of Original Project Work", "2"),
        ("PAGE 3", "Declaration of Originality", "3"),
        ("PAGE 4", "Acknowledgement", "4"),
        ("PAGE 5", "Project and Team Particulars", "5"),
        ("PAGE 6", "Abstract and Keywords", "6"),
        ("PAGE 7", "Table of Contents", "7"),
        ("PAGE 8", "Introduction", "8"),
        ("PAGE 9", "Problem Statement and Need", "9"),
        ("PAGE 10", "Aim, Objectives and Hypothesis", "10"),
        ("PAGE 11", "Scientific Principle: Phase-Change Materials (PCM)", "11"),
        ("PAGE 12", "Scientific Principle: Peltier Thermoelectric Effect", "12"),
        ("PAGE 13", "Complete System Architecture", "13"),
        ("PAGE 14", "Components and Material Selection", "14"),
        ("PAGE 15", "Thermal Management and Heat Transfer", "15"),
        ("PAGE 16", "Sensors, Controller and Operational Logic", "16"),
        ("PAGE 17", "Engineering Calculations", "17"),
        ("PAGE 18", "Prototype Development", "18"),
        ("PAGE 19", "Experimental Methodology", "19"),
        ("PAGE 20", "Observations and Data Collection", "20"),
        ("PAGE 21", "Results, Graphs and Analysis", "21"),
        ("PAGE 22", "Energy, Cost and Economic Feasibility", "22"),
        ("PAGE 23", "Safety, Limitations and Reliability", "23"),
        ("PAGE 24", "Conclusion and Future Scope", "24"),
        ("PAGE 25", "References and Annexures", "25"),
    ]

    rows = []
    for pg, section, num in toc_entries:
        is_sci = any(x in section for x in ["Scientific", "Complete", "Thermal", "Sensors",
                                             "Engineering", "Prototype", "Experimental",
                                             "Observations", "Results", "Energy", "Safety",
                                             "Conclusion", "References"])
        rows.append([
            Paragraph(f"<b>{pg}</b>", S['table_cell_c']),
            Paragraph(section, S['toc_entry_bold'] if not is_sci else S['toc_entry']),
            Paragraph(f"<b>{num}</b>", S['table_cell_c']),
        ])

    story.append(Table(rows, colWidths=[22*mm, 140*mm, 10*mm],
                       style=TableStyle([
                           ('ROWBACKGROUNDS', (0,0), (-1,-1), [TABLE_BG, WHITE]),
                           ('BOX', (0,0), (-1,-1), 0.5, RULE_COLOR),
                           ('LINEBELOW', (0,0), (-1,-1), 0.3, RULE_COLOR),
                           ('TOPPADDING', (0,0), (-1,-1), 5),
                           ('BOTTOMPADDING', (0,0), (-1,-1), 5),
                           ('LEFTPADDING', (0,0), (-1,-1), 7),
                           ('RIGHTPADDING', (0,0), (-1,-1), 7),
                           ('ALIGN', (0,0), (0,-1), 'CENTER'),
                           ('ALIGN', (2,0), (2,-1), 'CENTER'),
                       ])))
    story.append(Spacer(1, 5*mm))
    story.append(Paragraph(
        "<i>List of Figures:</i> Fig. 1 — PCM Phase-Change Principle &nbsp;|&nbsp; "
        "Fig. 2 — Peltier Module Schematic &nbsp;|&nbsp; Fig. 3 — System Architecture Block Diagram &nbsp;|&nbsp; "
        "Fig. 4 — Operational Control Flowchart &nbsp;|&nbsp; Fig. 5 — Thermal Pathway Diagram &nbsp;|&nbsp; "
        "Fig. 6 — Comparative Experimental Setup",
        ParagraphStyle('toc_fig', fontName='Helvetica-Oblique', fontSize=8,
                       textColor=SLATE, leading=13)))
    return story


def page8_introduction(S):
    story = []
    story.append(Spacer(1, 8*mm))
    story.append(section_banner("1. INTRODUCTION"))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("1.1 The Medical Cold Chain", S['section_heading']))
    story.append(Paragraph(
        "A medical cold chain is the continuous, temperature-controlled logistics system that ensures "
        "temperature-sensitive pharmaceutical and biological products remain within their prescribed "
        "storage conditions from point of manufacture to point of use. Products such as vaccines, "
        "insulins, monoclonal antibodies, blood derivatives, diagnostic reagents and certain oral "
        "medications must be maintained within specific temperature bands — commonly 2 °C to 8 °C "
        "for refrigerated products — throughout transportation and storage [1, 2].",
        S['body']))
    story.append(Paragraph(
        "Cold chain failure is a leading cause of avoidable loss of medical product potency. The World "
        "Health Organisation estimates that temperature excursions account for a significant proportion "
        "of vaccine wastage globally, disproportionately affecting low- and middle-income countries "
        "where electrical infrastructure may be unreliable and last-mile distribution routes can be "
        "long and demanding [2]. In the Indian context, achieving Viksit Bharat and healthcare equity "
        "for rural and remote populations requires dependable cold-chain solutions that do not depend "
        "exclusively on mains electricity [3].",
        S['body']))

    story.append(Paragraph("1.2 Portable Cold-Chain Solutions", S['section_heading']))
    story.append(Paragraph(
        "Portable vaccine carriers and medical refrigeration boxes for field use are typically designed "
        "around Phase Change Materials (PCMs) or ice packs. The PCM stores thermal energy in a latent "
        "form during its phase transition; on deployment, the melting of the PCM absorbs ambient heat "
        "and maintains the internal temperature. This approach is passive, requires no electrical power "
        "during operation, and is therefore well suited to environments where reliable electricity is "
        "unavailable [4, 5].",
        S['body']))
    story.append(Paragraph(
        "However, the duration for which a PCM-based box can maintain its target temperature range is "
        "finite. It is determined by the quantity and thermal properties of the PCM, the quality of "
        "thermal insulation, the ambient temperature conditions, the frequency of opening and the "
        "thermal load of the payload. Once the PCM has fully transitioned and its latent heat reserve "
        "is exhausted, the internal temperature begins to rise.",
        S['body']))

    story.append(Paragraph("1.3 Motivation for SANJIVANI", S['section_heading']))
    story.append(Paragraph(
        "SANJIVANI — named after the legendary life-restoring herb of Sanskrit tradition — is designed "
        "to address the duration limitation of passive PCM systems. The core idea is to supplement the "
        "PCM's passive thermal storage with a selectively activated thermoelectric cooling subsystem. "
        "By introducing Peltier modules that are triggered only when the internal temperature approaches "
        "an upper threshold, the system seeks to slow the depletion of the PCM's cooling capacity, "
        "partially restore it during active cooling cycles, and thereby extend the total time for which "
        "the enclosure remains within the required temperature range.",
        S['body']))
    story.append(Paragraph(
        "This project is relevant to the national theme of STEM for Viksit and Atmanirbhar Bharat: it "
        "demonstrates that locally developed, low-cost engineering solutions can address real healthcare "
        "infrastructure challenges. The project is an educational engineering investigation rather than "
        "a certified or commercially available medical device.",
        S['body']))
    return story


def page9_problem(S):
    story = []
    story.append(Spacer(1, 8*mm))
    story.append(section_banner("2. PROBLEM STATEMENT AND NEED"))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("2.1 Limitations of Passive PCM Cooling", S['section_heading']))
    story.append(Paragraph(
        "A Phase Change Material cooler stores thermal energy as latent heat. For a given enclosure and "
        "set of conditions, the total latent heat reserve (Q = mL) is fixed. Heat continuously enters "
        "the enclosure from the warmer ambient environment through the insulation walls — a process "
        "governed by the insulation's thermal resistance and the prevailing temperature gradient. "
        "As each joule of heat ingress is absorbed by the PCM, the remaining reserve is progressively "
        "depleted. When the PCM has completely melted, no further latent heat absorption occurs and the "
        "internal temperature begins to rise towards ambient. At this point, the medical payload is at "
        "risk of a temperature excursion.",
        S['body']))

    story.append(Paragraph("2.2 Practical Challenges", S['section_heading']))
    challenges = [
        ("Extended routes:", "Rural health missions, border outposts and disaster-relief deployments "
         "frequently require storage durations that exceed the capacity of a single PCM charge."),
        ("Adverse ambient conditions:", "High ambient temperatures — common in Indian summers — "
         "increase heat ingress and reduce the passive holding duration below designed values."),
        ("Re-conditioning constraints:", "Returning a PCM box to a refrigeration facility for "
         "re-conditioning may not be feasible during extended field operations."),
        ("Electrical limitations:", "Conventional active refrigerators require continuous mains "
         "power, which is not always available in remote locations."),
        ("Temperature monitoring gaps:", "Without continuous temperature monitoring, a cold-chain "
         "breach may go undetected until the payload is examined."),
    ]
    for title, text in challenges:
        story.append(bullet(f"<b>{title}</b> {text}"))

    story.append(Spacer(1, 4*mm))
    story.append(Paragraph("2.3 Formal Problem Statement", S['section_heading']))

    prob_box = Table([[Paragraph(
        "Conventional PCM-based portable medical coolers have a fixed thermal reserve and a finite "
        "temperature-holding duration. Under adverse ambient conditions or for extended deployment "
        "scenarios, their passive cooling capacity may be insufficient to maintain temperature "
        "stability for the required period, thereby creating the risk of cold-chain failure and "
        "medical product compromise. A supplementary, energy-efficient and intelligently controlled "
        "active cooling mechanism is required to extend the useful holding duration without "
        "introducing a continuous or prohibitive electrical energy demand.",
        ParagraphStyle('prob_st', fontName='Helvetica', fontSize=10, textColor=NAVY,
                       alignment=TA_JUSTIFY, leading=16))]], style=TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), TEAL_LIGHT),
            ('BOX', (0,0), (-1,-1), 1.5, TEAL_DARK),
            ('LEFTPADDING', (0,0), (-1,-1), 12),
            ('RIGHTPADDING', (0,0), (-1,-1), 12),
            ('TOPPADDING', (0,0), (-1,-1), 10),
            ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ]))
    story.append(prob_box)
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("2.4 Why Thermoelectric Supplementation?", S['section_heading']))
    story.append(Paragraph(
        "Peltier thermoelectric modules offer a solid-state, mechanically simple cooling mechanism with "
        "no moving parts, no refrigerant and compact dimensions. When operated under intelligent "
        "threshold-based control rather than continuously, their electrical energy consumption can be "
        "limited to periods when supplementary cooling is genuinely required. This approach makes them "
        "potentially compatible with battery power for field deployment. Furthermore, by coupling the "
        "cold side of the Peltier module to the PCM arrangement, the thermoelectric cooling may partially "
        "compensate for heat ingress and slow or temporarily reverse the depletion of the PCM's latent "
        "heat reserve — a feature that is not achievable with passive PCM alone.",
        S['body']))
    return story


def page10_aim(S):
    story = []
    story.append(Spacer(1, 8*mm))
    story.append(section_banner("3. AIM, OBJECTIVES AND HYPOTHESIS"))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("3.1 Main Aim", S['section_heading']))
    aim_box = Table([[Paragraph(
        "To design, develop and experimentally evaluate a sensor-triggered hybrid PCM–Peltier thermal "
        "management system (SANJIVANI) capable of extending the temperature-holding duration of a "
        "portable insulated medical cooler while maintaining thermal stability within a defined "
        "range and controlling electrical energy consumption.",
        ParagraphStyle('aim_st', fontName='Helvetica-Bold', fontSize=10.5, textColor=NAVY,
                       alignment=TA_JUSTIFY, leading=16))]],
        style=TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), GOLD_LIGHT),
            ('BOX', (0,0), (-1,-1), 1.2, GOLD),
            ('LEFTPADDING', (0,0), (-1,-1), 10),
            ('RIGHTPADDING', (0,0), (-1,-1), 10),
            ('TOPPADDING', (0,0), (-1,-1), 8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ]))
    story.append(aim_box)
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("3.2 Specific Objectives", S['section_heading']))
    objectives = [
        "To study and explain the thermodynamic principles governing PCM latent heat storage, "
        "thermoelectric heat pumping and thermal insulation in portable cold-chain systems.",
        "To design a system architecture that integrates PCM passive cooling with sensor-triggered "
        "Peltier active cooling, aluminium heat spreading and liquid-assisted heat transport.",
        "To specify and select appropriate components — including PCM, Peltier modules, aluminium "
        "plates, temperature sensors, microcontroller and power supply — based on engineering criteria.",
        "To assemble a functional prototype of the SANJIVANI system and document the development process.",
        "To design and implement an operational control algorithm using threshold-based hysteresis "
        "to activate and deactivate Peltier cooling in response to temperature sensor data.",
        "To conduct a controlled comparative experiment between PCM-only cooling (Configuration A) "
        "and the SANJIVANI hybrid system (Configuration B) under equivalent conditions.",
        "To measure, record and analyse temperature profiles, electrical energy consumption and "
        "Peltier duty cycle data for both configurations.",
        "To evaluate the engineering feasibility, cost implications and future potential of the "
        "SANJIVANI system for portable medical cold-chain applications.",
    ]
    for i, obj in enumerate(objectives, 1):
        story.append(numbered_item(i, obj))

    story.append(Spacer(1, 4*mm))
    story.append(Paragraph("3.3 Main Research Question", S['section_heading']))
    story.append(Paragraph(
        "<i>Can an intelligently controlled thermoelectric cooling subsystem, integrated with a "
        "PCM-based medical cooling enclosure, extend its useful temperature-holding duration while "
        "maintaining acceptable temperature stability and controlling electrical energy consumption?</i>",
        ParagraphStyle('rq', fontName='Helvetica-BoldOblique', fontSize=10, textColor=TEAL_DARK,
                       alignment=TA_JUSTIFY, leading=15)))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("3.4 Hypothesis", S['section_heading']))
    story.append(Paragraph(
        "A sensor-triggered Peltier cooling arrangement, integrated with appropriate heat-spreading "
        "and heat-rejection components, may slow the loss of useful PCM cooling capacity and extend "
        "the time for which the enclosure remains within its defined temperature range compared with "
        "PCM-only passive cooling operating under identical conditions. The hypothesis will be tested "
        "through controlled experimentation; it is not presented as an established conclusion.",
        S['body']))

    story.append(Spacer(1, 3*mm))
    story.append(Paragraph("3.5 Design Targets and Their Basis", S['section_heading']))
    target_rows = [
        [Paragraph("<b>Parameter</b>", S['table_header']),
         Paragraph("<b>Value / Target</b>", S['table_header']),
         Paragraph("<b>Basis and Status</b>", S['table_header'])],
        [Paragraph("Baseline PCM-only duration", S['table_cell']),
         Paragraph("~72 hours", S['table_cell']),
         Paragraph("Preliminary engineering assumption; to be verified experimentally", S['table_cell'])],
        [Paragraph("Target hybrid duration", S['table_cell']),
         Paragraph("~110 hours", S['table_cell']),
         Paragraph("Engineering design target; not an achieved or guaranteed result", S['table_cell'])],
        [Paragraph("Temperature range", S['table_cell']),
         ph("2 °C – 8 °C  [ to be confirmed ]"),
         Paragraph("Typical WHO vaccine cold-chain requirement; actual range subject to PCM selection", S['table_cell'])],
        [Paragraph("Peltier activation threshold (T_upper)", S['table_cell']),
         ph("[ to be set after prototype testing ]"),
         Paragraph("Determined experimentally during control system commissioning", S['table_cell'])],
        [Paragraph("Peltier deactivation threshold (T_lower)", S['table_cell']),
         ph("[ to be set after prototype testing ]"),
         Paragraph("Determined experimentally during control system commissioning", S['table_cell'])],
    ]
    story.append(Table(target_rows, colWidths=[48*mm, 42*mm, 80*mm],
                       style=TableStyle([
                           ('BACKGROUND', (0,0), (-1,0), NAVY),
                           ('ROWBACKGROUNDS', (0,1), (-1,-1), [TABLE_BG, WHITE]),
                           ('BOX', (0,0), (-1,-1), 0.5, RULE_COLOR),
                           ('INNERGRID', (0,0), (-1,-1), 0.3, RULE_COLOR),
                           ('TOPPADDING', (0,0), (-1,-1), 4),
                           ('BOTTOMPADDING', (0,0), (-1,-1), 4),
                           ('LEFTPADDING', (0,0), (-1,-1), 6),
                           ('RIGHTPADDING', (0,0), (-1,-1), 6),
                           ('VALIGN', (0,0), (-1,-1), 'TOP'),
                       ])))
    return story


def page11_pcm(S):
    story = []
    story.append(Spacer(1, 8*mm))
    story.append(section_banner("4. SCIENTIFIC PRINCIPLE: PHASE-CHANGE MATERIALS"))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("4.1 Thermal Energy Storage: Sensible vs Latent Heat", S['section_heading']))
    story.append(Paragraph(
        "When heat is added to a material, two distinct types of thermal energy storage may occur:",
        S['body']))
    story.append(bullet("<b>Sensible heat storage</b> occurs when the temperature of the material changes "
                        "as it absorbs thermal energy. The amount of heat stored is given by:"))
    story.append(Spacer(1, 2*mm))
    story.append(Paragraph("Q = m c ΔT", S['equation']))
    eq_rows = [
        ["Q", "Thermal energy stored (J)"],
        ["m", "Mass of the material (kg)"],
        ["c", "Specific heat capacity of the material (J kg⁻¹ K⁻¹)"],
        ["ΔT", "Change in temperature (K or °C)"],
    ]
    story.append(Table([[Paragraph(r, S['eq_note']) for r in row] for row in eq_rows],
                       colWidths=[12*mm, 155*mm]))
    story.append(Spacer(1, 2*mm))
    story.append(bullet("<b>Latent heat storage</b> occurs during a phase transition — typically solid "
                        "to liquid or vice versa — where the material absorbs or releases a large "
                        "quantity of thermal energy without any change in temperature. This isothermal "
                        "absorption is the fundamental principle behind PCM cooling."))
    story.append(Spacer(1, 2*mm))
    story.append(Paragraph("Q = m L", S['equation']))
    eq_rows2 = [
        ["Q", "Latent heat energy stored or released (J)"],
        ["m", "Mass of the PCM (kg)"],
        ["L", "Specific latent heat of fusion of the PCM (J kg⁻¹)"],
    ]
    story.append(Table([[Paragraph(r, S['eq_note']) for r in row] for row in eq_rows2],
                       colWidths=[12*mm, 155*mm]))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(
        "The latent heat of fusion (L) is typically one to two orders of magnitude larger than the "
        "sensible heat capacity change over a comparable temperature range, making PCMs highly "
        "effective thermal buffers for temperature-critical applications.",
        S['body']))

    story.append(Paragraph("4.2 PCM Operation in a Cooling Context", S['section_heading']))
    story.append(Paragraph(
        "In a medical cooling application, the PCM is pre-conditioned (frozen / solidified) before "
        "deployment. As the ambient environment transfers heat into the insulated enclosure, the PCM "
        "absorbs this heat and undergoes the solid-to-liquid phase transition. During this transition, "
        "the PCM temperature remains essentially constant at its phase-change temperature, providing "
        "a stable thermal buffer for the medical payload. This continues until the entire PCM mass has "
        "melted, at which point sensible heating of the liquid PCM begins and the internal temperature "
        "rises more rapidly.",
        S['body']))

    story.append(Spacer(1, 2*mm))
    story.append(PCMDiagram(width=PAGE_W - L_MARGIN - R_MARGIN, height=55*mm))
    story.append(Spacer(1, 2*mm))

    story.append(Paragraph("4.3 PCM Selection Criteria", S['section_heading']))
    pcm_crit = [
        ("Phase-change temperature:", "Must fall within or at the boundary of the target storage range."),
        ("High latent heat of fusion:", "Maximises the energy stored per unit mass, extending duration."),
        ("Low supercooling tendency:", "The PCM should solidify reliably near its published melt temperature."),
        ("Thermal stability:", "Properties should not degrade significantly over repeated thermal cycles."),
        ("Low toxicity and chemical stability:", "Important for safe handling in a school laboratory setting."),
        ("Commercial availability:", "PCM should be obtainable in appropriate quantities with known specifications."),
    ]
    for title, text in pcm_crit:
        story.append(bullet(f"<b>{title}</b> {text}"))

    story.append(Spacer(1, 3*mm))
    story.append(Paragraph("PCM Specification (To Be Confirmed by Team):", S['subsection_heading']))
    pcm_spec_rows = [
        [Paragraph("<b>Parameter</b>", S['table_header']), Paragraph("<b>Value</b>", S['table_header'])],
        [Paragraph("PCM type / chemistry", S['table_cell']), ph("[ To be specified — e.g. water ice, paraffin, salt hydrate ]")],
        [Paragraph("Phase-change temperature", S['table_cell']), ph("[ T_melt = __ °C ]")],
        [Paragraph("Specific latent heat of fusion (L)", S['table_cell']), ph("[ L = __ J kg⁻¹ ]")],
        [Paragraph("Specific heat capacity (solid)", S['table_cell']), ph("[ c_s = __ J kg⁻¹ K⁻¹ ]")],
        [Paragraph("Specific heat capacity (liquid)", S['table_cell']), ph("[ c_l = __ J kg⁻¹ K⁻¹ ]")],
        [Paragraph("Mass used in prototype", S['table_cell']), ph("[ m_PCM = __ kg ]")],
        [Paragraph("Pre-conditioning temperature", S['table_cell']), ph("[ T_cond = __ °C ]")],
    ]
    story.append(Table(pcm_spec_rows, colWidths=[72*mm, 98*mm],
                       style=TableStyle([
                           ('BACKGROUND', (0,0), (-1,0), NAVY),
                           ('ROWBACKGROUNDS', (0,1), (-1,-1), [TABLE_BG, WHITE]),
                           ('BOX', (0,0), (-1,-1), 0.5, RULE_COLOR),
                           ('INNERGRID', (0,0), (-1,-1), 0.3, RULE_COLOR),
                           ('TOPPADDING', (0,0), (-1,-1), 4),
                           ('BOTTOMPADDING', (0,0), (-1,-1), 4),
                           ('LEFTPADDING', (0,0), (-1,-1), 6),
                           ('RIGHTPADDING', (0,0), (-1,-1), 6),
                           ('VALIGN', (0,0), (-1,-1), 'TOP'),
                       ])))
    return story


def page12_peltier(S):
    story = []
    story.append(Spacer(1, 8*mm))
    story.append(section_banner("5. SCIENTIFIC PRINCIPLE: PELTIER THERMOELECTRIC EFFECT"))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("5.1 The Peltier Effect", S['section_heading']))
    story.append(Paragraph(
        "In 1834, French physicist Jean Charles Athanase Peltier discovered that when a direct electric "
        "current flows through a junction of two dissimilar conducting materials, heat is either absorbed "
        "or released at that junction — depending on the direction of current flow [6]. This is the Peltier "
        "effect, which underlies all thermoelectric cooling devices.",
        S['body']))

    story.append(Paragraph("5.2 Thermoelectric Module Construction", S['section_heading']))
    story.append(Paragraph(
        "A practical Peltier module (Thermoelectric Cooler, TEC) consists of an array of N-type and "
        "P-type semiconductor elements (typically bismuth telluride, Bi₂Te₃) sandwiched between two "
        "ceramic plates. When DC current is applied, the charge carriers in the semiconductors transport "
        "thermal energy from one ceramic plate (the cold face) to the other (the hot face). "
        "Heat is therefore pumped from the cold side to the hot side against the temperature gradient — "
        "a thermodynamically driven process that requires electrical work input [6, 7].",
        S['body']))

    story.append(Spacer(1, 2*mm))
    story.append(PeltierDiagram(width=PAGE_W - L_MARGIN - R_MARGIN, height=68*mm))
    story.append(Spacer(1, 2*mm))

    story.append(Paragraph("5.3 Heat Balance", S['section_heading']))
    story.append(Paragraph(
        "The fundamental heat balance of a Peltier module is:", S['body']))
    story.append(Paragraph("Q̇_hot = Q̇_cold + P_elec", S['equation']))
    eq_rows = [
        ["Q̇_hot", "Rate of heat rejection from the hot side (W)"],
        ["Q̇_cold", "Rate of heat absorbed at the cold side = useful cooling power (W)"],
        ["P_elec", "Electrical power consumed by the module (W) = V × I"],
    ]
    story.append(Table([[Paragraph(r, S['eq_note']) for r in row] for row in eq_rows],
                       colWidths=[18*mm, 149*mm]))
    story.append(Paragraph(
        "<b>Critical implication:</b> The hot side must reject MORE heat than the cold side absorbs, "
        "because it must also dissipate the electrical energy converted to heat within the semiconductor "
        "junctions. If the hot side is not effectively cooled, its temperature rises, reducing the "
        "temperature differential across the module and severely limiting cooling performance. "
        "Hot-side thermal management is therefore as important as cold-side coupling.",
        S['body']))

    story.append(Paragraph("5.4 Coefficient of Performance", S['section_heading']))
    story.append(Paragraph("COP = Q̇_cold / P_elec", S['equation']))
    story.append(Paragraph(
        "The Coefficient of Performance (COP) expresses the ratio of useful cooling delivered to "
        "electrical power consumed. The COP of a Peltier module is typically less than 1 at practical "
        "temperature differentials — considerably lower than a vapour-compression refrigerator. "
        "This is a known limitation of thermoelectric systems. However, their solid-state construction, "
        "small size, low maintenance and suitability for duty-cycled operation make them appropriate "
        "for a supplementary, selectively activated cooling role rather than continuous primary cooling.",
        S['body']))

    story.append(Paragraph("5.5 Module Specification (To Be Confirmed)", S['subsection_heading']))
    tec_rows = [
        [Paragraph("<b>Parameter</b>", S['table_header']), Paragraph("<b>Specification</b>", S['table_header'])],
        [Paragraph("Module model number", S['table_cell']), ph("[ e.g. TEC1-12706, or as procured ]")],
        [Paragraph("Maximum voltage (V_max)", S['table_cell']), ph("[ __ V DC ]")],
        [Paragraph("Maximum current (I_max)", S['table_cell']), ph("[ __ A ]")],
        [Paragraph("Maximum cooling capacity (Q_max)", S['table_cell']), ph("[ __ W ]")],
        [Paragraph("Maximum temperature differential (ΔT_max)", S['table_cell']), ph("[ __ °C ]")],
        [Paragraph("Operating voltage (design point)", S['table_cell']), ph("[ __ V ]")],
        [Paragraph("Operating current (design point)", S['table_cell']), ph("[ __ A ]")],
        [Paragraph("Number of modules in prototype", S['table_cell']), ph("[ __ ]")],
    ]
    story.append(Table(tec_rows, colWidths=[80*mm, 90*mm],
                       style=TableStyle([
                           ('BACKGROUND', (0,0), (-1,0), NAVY),
                           ('ROWBACKGROUNDS', (0,1), (-1,-1), [TABLE_BG, WHITE]),
                           ('BOX', (0,0), (-1,-1), 0.5, RULE_COLOR),
                           ('INNERGRID', (0,0), (-1,-1), 0.3, RULE_COLOR),
                           ('TOPPADDING', (0,0), (-1,-1), 4),
                           ('BOTTOMPADDING', (0,0), (-1,-1), 4),
                           ('LEFTPADDING', (0,0), (-1,-1), 6),
                           ('RIGHTPADDING', (0,0), (-1,-1), 6),
                           ('VALIGN', (0,0), (-1,-1), 'TOP'),
                       ])))
    return story


def page13_architecture(S):
    story = []
    story.append(Spacer(1, 8*mm))
    story.append(section_banner("6. COMPLETE SYSTEM ARCHITECTURE"))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph(
        "The SANJIVANI system integrates passive and active thermal management into a single controlled "
        "architecture. The block diagram below presents the principal components and the interactions "
        "between them. Heat flow, electrical supply and control signal pathways are distinguished.",
        S['body']))
    story.append(Spacer(1, 3*mm))
    story.append(SystemBlockDiagram(width=PAGE_W - L_MARGIN - R_MARGIN, height=118*mm))
    story.append(Spacer(1, 3*mm))

    story.append(Paragraph("6.1 Principal Subsystems", S['section_heading']))
    subsystems = [
        ("Insulated Enclosure:", "Provides thermal isolation for the payload and PCM. Minimises "
         "heat ingress from the ambient environment. Material, thickness and insulation type to be specified."),
        ("PCM Chamber:", "Contains the phase-change material that provides primary passive cooling. "
         "The PCM is pre-conditioned before deployment and absorbs incoming heat during its phase transition."),
        ("Temperature Sensors:", "Continuously monitor the payload-zone and PCM temperatures. "
         "Sensor outputs are read by the microcontroller at regular intervals."),
        ("Microcontroller (Controller):", "Implements the threshold-based hysteresis algorithm. "
         "Activates the Peltier system when T ≥ T_upper and deactivates it when T ≤ T_lower. "
         "Optionally logs temperature and operating state data."),
        ("Peltier Module(s) [TEC]:", "Thermoelectric heat pumps that transfer heat from their cold "
         "face (thermally coupled to the aluminium spreader) to their hot face when powered."),
        ("Aluminium Heat Spreader:", "Distributes cold-side cooling uniformly across the thermal "
         "interface region, reducing localised hotspots and improving PCM–TEC thermal coupling."),
        ("Liquid Thermal Transfer Chamber:", "Provides a heat-transport pathway between the Peltier "
         "assembly and the heat rejection zone. Exact configuration (passive chamber, gravity-driven "
         "circulation, etc.) to be confirmed by the team."),
        ("Hot-Side Heat Rejection System:", "Receives the heat pumped by the Peltier module "
         "plus the electrical power dissipated within it, and rejects this heat to the external "
         "environment via a heat sink, airflow or liquid-coupled heat exchanger."),
        ("Power Supply:", "Provides DC electrical power to the Peltier module(s) and microcontroller. "
         "May be a battery bank, solar-charged battery or regulated DC supply. Specification to be confirmed."),
    ]
    for title, text in subsystems:
        story.append(bullet(f"<b>{title}</b> {text}"))
    return story


def page14_components(S):
    story = []
    story.append(Spacer(1, 8*mm))
    story.append(section_banner("7. COMPONENTS AND MATERIAL SELECTION"))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(
        "The table below provides a framework bill of materials. For each component, the engineering "
        "function, selection criteria and required specification are listed. Actual models and quantities "
        "are to be confirmed and inserted by the team during prototype development.",
        S['body']))
    story.append(Spacer(1, 3*mm))

    comp_rows = [
        [Paragraph("<b>#</b>", S['table_header']),
         Paragraph("<b>Component</b>", S['table_header']),
         Paragraph("<b>Function</b>", S['table_header']),
         Paragraph("<b>Key Selection Criteria</b>", S['table_header']),
         Paragraph("<b>Quantity / Model</b>", S['table_header'])],
        [Paragraph("1", S['table_cell_c']),
         Paragraph("Phase Change Material (PCM)", S['table_cell']),
         Paragraph("Primary passive thermal reserve", S['table_cell']),
         Paragraph("Phase-change temp in target range; high L; non-toxic; stable over cycles", S['table_cell']),
         ph("__ kg; model: __ ")],
        [Paragraph("2", S['table_cell_c']),
         Paragraph("Insulated Enclosure", S['table_cell']),
         Paragraph("Thermal isolation of payload + PCM", S['table_cell']),
         Paragraph("Low thermal conductivity; adequate volume; sealed construction", S['table_cell']),
         ph("1; size: __ L")],
        [Paragraph("3", S['table_cell_c']),
         Paragraph("Peltier TEC Module(s)", S['table_cell']),
         Paragraph("Active cold-side cooling when triggered", S['table_cell']),
         Paragraph("Adequate Q_cold at design ΔT; operating voltage compatible with supply", S['table_cell']),
         ph("__ units; model: __")],
        [Paragraph("4", S['table_cell_c']),
         Paragraph("Aluminium Plate / Sheet", S['table_cell']),
         Paragraph("Cold-side heat spreading and thermal interface", S['table_cell']),
         Paragraph("High thermal conductivity; flat surface; appropriate area and thickness", S['table_cell']),
         ph("__ pcs; size: __ mm")],
        [Paragraph("5", S['table_cell_c']),
         Paragraph("Liquid Thermal Transfer Chamber", S['table_cell']),
         Paragraph("Transport heat from Peltier assembly to heat rejection zone", S['table_cell']),
         Paragraph("Adequate thermal capacity; leak-proof; compatible liquid (water or other)", S['table_cell']),
         ph("Design TBC")],
        [Paragraph("6", S['table_cell_c']),
         Paragraph("Hot-Side Heat Sink / Exchanger", S['table_cell']),
         Paragraph("Reject hot-side heat to environment", S['table_cell']),
         Paragraph("Sufficient thermal resistance to environment; size compatible with enclosure", S['table_cell']),
         ph("__ units; model: __")],
        [Paragraph("7", S['table_cell_c']),
         Paragraph("Cooling Fan (if applicable)", S['table_cell']),
         Paragraph("Forced convection over hot-side heat sink", S['table_cell']),
         Paragraph("Appropriate airflow (CFM); low noise; DC voltage compatible with supply", S['table_cell']),
         ph("TBC")],
        [Paragraph("8", S['table_cell_c']),
         Paragraph("Temperature Sensors (×2+)", S['table_cell']),
         Paragraph("Monitor internal and PCM temperatures", S['table_cell']),
         Paragraph("Range −10 to +50 °C; resolution ≤0.1 °C; reliable at low temperatures", S['table_cell']),
         ph("__ pcs; model: __")],
        [Paragraph("9", S['table_cell_c']),
         Paragraph("Microcontroller", S['table_cell']),
         Paragraph("Read sensors; implement control logic; drive switching", S['table_cell']),
         Paragraph("Digital I/O; ADC or digital sensor interface; programmable; low power", S['table_cell']),
         ph("1; e.g. Arduino or similar")],
        [Paragraph("10", S['table_cell_c']),
         Paragraph("MOSFET / Relay Switching Module", S['table_cell']),
         Paragraph("Switch Peltier power on/off under microcontroller command", S['table_cell']),
         Paragraph("Rated for Peltier current; low switching loss; heat dissipation considered", S['table_cell']),
         ph("1; model: __")],
        [Paragraph("11", S['table_cell_c']),
         Paragraph("Power Supply / Battery", S['table_cell']),
         Paragraph("Provide regulated DC to Peltier and controller", S['table_cell']),
         Paragraph("Adequate capacity (Ah) for target operating duration; voltage regulated", S['table_cell']),
         ph("Spec TBC")],
        [Paragraph("12", S['table_cell_c']),
         Paragraph("Thermal Interface Material (TIM)", S['table_cell']),
         Paragraph("Minimise contact resistance at TEC–Al and Al–PCM interfaces", S['table_cell']),
         Paragraph("High thermal conductivity; conformable; compatible with operating temperature", S['table_cell']),
         ph("TBC")],
        [Paragraph("13", S['table_cell_c']),
         Paragraph("Wiring, Connectors and Insulation", S['table_cell']),
         Paragraph("Electrical interconnection; safety insulation", S['table_cell']),
         Paragraph("Appropriate wire gauge for current; moisture-resistant insulation", S['table_cell']),
         ph("As required")],
    ]

    story.append(Table(comp_rows, colWidths=[8*mm, 35*mm, 40*mm, 55*mm, 32*mm],
                       style=TableStyle([
                           ('BACKGROUND', (0,0), (-1,0), NAVY),
                           ('ROWBACKGROUNDS', (0,1), (-1,-1), [TABLE_BG, WHITE]),
                           ('BOX', (0,0), (-1,-1), 0.5, RULE_COLOR),
                           ('INNERGRID', (0,0), (-1,-1), 0.3, RULE_COLOR),
                           ('TOPPADDING', (0,0), (-1,-1), 4),
                           ('BOTTOMPADDING', (0,0), (-1,-1), 4),
                           ('LEFTPADDING', (0,0), (-1,-1), 5),
                           ('RIGHTPADDING', (0,0), (-1,-1), 5),
                           ('VALIGN', (0,0), (-1,-1), 'TOP'),
                           ('FONTSIZE', (0,0), (-1,-1), 7.5),
                       ])))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(
        "<i>Note: All highlighted cells are placeholders to be completed by the team. "
        "Actual specifications should be derived from component datasheets and experimental measurements.</i>",
        ParagraphStyle('note_it', fontName='Helvetica-Oblique', fontSize=8,
                       textColor=SLATE, alignment=TA_LEFT, leading=12)))
    return story


def page15_thermal(S):
    story = []
    story.append(Spacer(1, 8*mm))
    story.append(section_banner("8. THERMAL MANAGEMENT AND HEAT TRANSFER"))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("8.1 Complete Thermal Pathway", S['section_heading']))
    story.append(ThermalFlowDiagram(width=PAGE_W - L_MARGIN - R_MARGIN, height=63*mm))
    story.append(Spacer(1, 2*mm))
    story.append(Paragraph(
        "Heat continuously flows from the warmer ambient environment into the cooler insulated "
        "enclosure. This heat is first impeded by the insulation layer, then absorbed by the PCM, "
        "and when the Peltier system is active, partially countered by the cold-side cooling action. "
        "The heat pumped to the Peltier hot side plus the electrical power input must be effectively "
        "rejected to the external environment.",
        S['body']))

    story.append(Paragraph("8.2 Heat Ingress Through Insulation", S['section_heading']))
    story.append(Paragraph(
        "The rate of heat flowing into the enclosure through its insulating walls is governed by:", S['body']))
    story.append(Paragraph("Q̇_in = ΔT / R_thermal = (T_ambient − T_internal) / R_total", S['equation']))
    story.append(Paragraph(
        "where R_total (K W⁻¹) is the total thermal resistance of the enclosure walls. "
        "Better insulation = higher R_total = lower heat ingress for a given temperature difference. "
        "The insulation must minimise heat ingress while accommodating the Peltier assembly.", S['body']))

    story.append(Paragraph("8.3 PCM Thermal Buffering", S['section_heading']))
    story.append(Paragraph(
        "While the PCM is undergoing its phase transition, it absorbs heat at its latent heat capacity "
        "(Q = mL). During this period, the internal temperature remains approximately constant. "
        "The PCM's total thermal reserve determines the maximum time it can buffer heat ingress without "
        "a temperature rise. The SANJIVANI system aims to slow the consumption of this reserve by "
        "partially compensating for heat ingress with Peltier cooling.", S['body']))

    story.append(Paragraph("8.4 Aluminium Heat Spreading", S['section_heading']))
    story.append(Paragraph(
        "Aluminium has an exceptionally high thermal conductivity (approximately 205 W m⁻¹ K⁻¹). "
        "An aluminium plate or sheet placed between the Peltier cold face and the PCM/payload region "
        "distributes the localised cold-side cooling over a larger contact area, improving thermal "
        "coupling and reducing temperature non-uniformity. The effectiveness of heat spreading depends "
        "on the plate thickness, area, surface contact quality and the use of thermal interface material "
        "at all contact surfaces.", S['body']))

    story.append(Paragraph("8.5 Liquid Thermal Transfer — Important Distinctions", S['section_heading']))
    story.append(Paragraph(
        "A liquid-based thermal transfer element in this system serves to transport heat — not to "
        "destroy it. The following distinctions are critical:", S['body']))
    distinctions = [
        ("<b>Heat transport:</b> The liquid can carry thermal energy from the Peltier hot-side "
         "interface to the heat rejection zone, using its heat capacity (Q = mc_liquid × ΔT)."),
        ("<b>Temporary heat storage:</b> A finite volume of liquid can absorb a quantity of heat as "
         "its temperature rises. This is a temporary buffer, not a permanent solution."),
        ("<b>Heat rejection:</b> To continuously remove heat from the system, the liquid must "
         "eventually transfer that heat to the external environment via a heat exchanger or heat sink. "
         "Without an external heat rejection pathway, a sealed liquid volume will eventually saturate."),
    ]
    for d in distinctions:
        story.append(bullet(d))

    story.append(Paragraph(
        "The exact configuration of the liquid thermal transfer element (sealed chamber, "
        "gravity-driven loop, pumped circuit, etc.) is a design detail to be confirmed by the team "
        "based on prototype testing. The team must ensure an adequate hot-side heat rejection "
        "pathway is provided.", S['body']))

    story.append(Paragraph("8.6 Hot-Side Heat Rejection", S['section_heading']))
    story.append(Paragraph(
        "The Peltier hot side rejects Q̇_hot = Q̇_cold + P_elec. This heat must leave the system "
        "completely. Approaches include passive heat sinks (finned aluminium), forced convection (fan), "
        "liquid-coupled heat exchangers or combinations. If the hot side is inadequately cooled, "
        "the module's temperature differential is reduced, its cold-side cooling performance degrades "
        "and the system may eventually enter thermal runaway. For this reason, hot-side thermal "
        "management is of equal or greater importance than cold-side coupling.", S['body']))

    story.append(Paragraph("8.7 Condensation and Thermal Non-Uniformity", S['section_heading']))
    story.append(Paragraph(
        "Operating surfaces below the dew point of ambient air will attract condensation, which can "
        "affect electrical components, insulation integrity and PCM containment. The design must ensure "
        "that cold surfaces are either sealed from ambient humid air or are configured to manage "
        "condensation safely. Temperature non-uniformity within the payload zone should also be "
        "characterised during testing.", S['body']))
    return story


def page16_control(S):
    story = []
    story.append(Spacer(1, 8*mm))
    story.append(section_banner("9. SENSORS, CONTROLLER AND OPERATIONAL LOGIC"))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("9.1 Temperature Sensing", S['section_heading']))
    story.append(Paragraph(
        "Temperature sensors are deployed at multiple locations within the enclosure: in the payload "
        "zone, at the PCM interface and optionally at the Peltier cold face and hot face. "
        "Common choices for this application include digital sensors with resolution of 0.0625 °C "
        "(e.g. DS18B20 1-Wire) or precision analogue sensors (e.g. LM35). "
        "Sensor placement is critical: the controlling sensor must reflect the payload temperature "
        "accurately without being unduly influenced by local PCM or Peltier surface temperatures.",
        S['body']))

    story.append(Paragraph("9.2 Threshold-Based Hysteresis Control", S['section_heading']))
    story.append(Paragraph(
        "The proposed control strategy employs hysteresis to prevent rapid switching (cycling) of "
        "the Peltier modules. Two temperature thresholds are defined:", S['body']))
    thresh_rows = [
        [Paragraph("<b>Threshold</b>", S['table_header']),
         Paragraph("<b>Symbol</b>", S['table_header']),
         Paragraph("<b>Action</b>", S['table_header']),
         Paragraph("<b>Value (to be set)</b>", S['table_header'])],
        [Paragraph("Upper activation threshold", S['table_cell']),
         Paragraph("T_upper", S['table_cell_c']),
         Paragraph("Peltier ON when T_internal ≥ T_upper", S['table_cell']),
         ph("[ __ °C ]")],
        [Paragraph("Lower deactivation threshold", S['table_cell']),
         Paragraph("T_lower", S['table_cell_c']),
         Paragraph("Peltier OFF when T_internal ≤ T_lower", S['table_cell']),
         ph("[ __ °C ]")],
        [Paragraph("Hysteresis band", S['table_cell']),
         Paragraph("ΔT_hys", S['table_cell_c']),
         Paragraph("T_upper − T_lower (prevents rapid cycling)", S['table_cell']),
         ph("[ __ °C ]")],
    ]
    story.append(Table(thresh_rows, colWidths=[52*mm, 20*mm, 72*mm, 26*mm],
                       style=TableStyle([
                           ('BACKGROUND', (0,0), (-1,0), NAVY),
                           ('ROWBACKGROUNDS', (0,1), (-1,-1), [TABLE_BG, WHITE]),
                           ('BOX', (0,0), (-1,-1), 0.5, RULE_COLOR),
                           ('INNERGRID', (0,0), (-1,-1), 0.3, RULE_COLOR),
                           ('TOPPADDING', (0,0), (-1,-1), 4),
                           ('BOTTOMPADDING', (0,0), (-1,-1), 4),
                           ('LEFTPADDING', (0,0), (-1,-1), 6),
                           ('RIGHTPADDING', (0,0), (-1,-1), 6),
                           ('VALIGN', (0,0), (-1,-1), 'TOP'),
                       ])))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(
        "The thresholds will be selected after prototype commissioning based on the actual PCM "
        "transition temperature, the target storage range and the system's thermal response time.",
        S['body']))

    story.append(Paragraph("9.3 Operational Flowchart", S['section_heading']))
    story.append(FlowchartDiagram(width=PAGE_W - L_MARGIN - R_MARGIN, height=128*mm))
    story.append(Spacer(1, 2*mm))

    story.append(Paragraph("9.4 Data Logging and Fault Conditions", S['section_heading']))
    story.append(Paragraph(
        "The microcontroller may optionally log temperature readings, timestamps and Peltier operating "
        "states to an SD card or serial interface. Fault conditions to be handled include sensor "
        "disconnection, out-of-range sensor readings (indicating sensor failure), and Peltier "
        "overtemperature conditions detected by monitoring the hot-side temperature sensor.",
        S['body']))
    return story


def page17_calcs(S):
    story = []
    story.append(Spacer(1, 8*mm))
    story.append(section_banner("10. ENGINEERING CALCULATIONS"))
    story.append(Spacer(1, 4*mm))
    story.append(Paragraph(
        "The following calculation framework uses the governing thermal engineering equations. "
        "Where actual measurements or specifications are not yet available, clearly marked "
        "placeholders are provided. All quantities use SI units unless otherwise noted.",
        S['body']))

    story.append(Paragraph("10.1 PCM Latent Heat Thermal Reserve", S['section_heading']))
    story.append(Paragraph("Q_latent = m_PCM × L", S['equation']))
    story.append(Paragraph(
        "where m_PCM is the mass of PCM (kg) and L is the specific latent heat of fusion (J kg⁻¹).", S['eq_note']))
    calc_rows1 = [
        [Paragraph("<b>Parameter</b>", S['table_header']),
         Paragraph("<b>Symbol</b>", S['table_header']),
         Paragraph("<b>Unit</b>", S['table_header']),
         Paragraph("<b>Value</b>", S['table_header'])],
        [Paragraph("Mass of PCM", S['table_cell']), Paragraph("m_PCM", S['table_cell_c']),
         Paragraph("kg", S['table_cell_c']), ph("[ __ ]")],
        [Paragraph("Specific latent heat", S['table_cell']), Paragraph("L", S['table_cell_c']),
         Paragraph("J kg⁻¹", S['table_cell_c']), ph("[ __ ]")],
        [Paragraph("Total latent heat reserve", S['table_cell']), Paragraph("Q_latent", S['table_cell_c']),
         Paragraph("J", S['table_cell_c']), ph("[ Q = m × L ]")],
        [Paragraph("Q_latent in Wh (÷3600)", S['table_cell']), Paragraph("Q_latent", S['table_cell_c']),
         Paragraph("Wh", S['table_cell_c']), ph("[ __ Wh ]")],
    ]
    story.append(Table(calc_rows1, colWidths=[65*mm, 25*mm, 25*mm, 55*mm],
                       style=TableStyle([
                           ('BACKGROUND', (0,0), (-1,0), TEAL),
                           ('ROWBACKGROUNDS', (0,1), (-1,-1), [TABLE_BG, WHITE]),
                           ('BOX', (0,0), (-1,-1), 0.5, RULE_COLOR),
                           ('INNERGRID', (0,0), (-1,-1), 0.3, RULE_COLOR),
                           ('TOPPADDING', (0,0), (-1,-1), 4), ('BOTTOMPADDING', (0,0), (-1,-1), 4),
                           ('LEFTPADDING', (0,0), (-1,-1), 6), ('RIGHTPADDING', (0,0), (-1,-1), 6),
                           ('VALIGN', (0,0), (-1,-1), 'TOP'),
                       ])))

    story.append(Paragraph("10.2 Approximate Heat Ingress Rate", S['section_heading']))
    story.append(Paragraph("Q̇_in = (T_ambient − T_internal) / R_total", S['equation']))
    calc_rows2 = [
        [Paragraph("<b>Parameter</b>", S['table_header']),
         Paragraph("<b>Symbol</b>", S['table_header']),
         Paragraph("<b>Unit</b>", S['table_header']),
         Paragraph("<b>Value</b>", S['table_header'])],
        [Paragraph("Ambient temperature", S['table_cell']), Paragraph("T_ambient", S['table_cell_c']),
         Paragraph("°C", S['table_cell_c']), ph("[ __ ]")],
        [Paragraph("Target internal temperature", S['table_cell']), Paragraph("T_internal", S['table_cell_c']),
         Paragraph("°C", S['table_cell_c']), ph("[ __ ]")],
        [Paragraph("Total thermal resistance of enclosure", S['table_cell']), Paragraph("R_total", S['table_cell_c']),
         Paragraph("K W⁻¹", S['table_cell_c']), ph("[ measured / calculated ]")],
        [Paragraph("Approximate heat ingress rate", S['table_cell']), Paragraph("Q̇_in", S['table_cell_c']),
         Paragraph("W", S['table_cell_c']), ph("[ __ W ]")],
        [Paragraph("Estimated PCM-only duration at this rate", S['table_cell']), Paragraph("t_PCM", S['table_cell_c']),
         Paragraph("h", S['table_cell_c']), ph("[ Q_latent / (Q̇_in × 3600) ]")],
    ]
    story.append(Table(calc_rows2, colWidths=[65*mm, 25*mm, 25*mm, 55*mm],
                       style=TableStyle([
                           ('BACKGROUND', (0,0), (-1,0), TEAL),
                           ('ROWBACKGROUNDS', (0,1), (-1,-1), [TABLE_BG, WHITE]),
                           ('BOX', (0,0), (-1,-1), 0.5, RULE_COLOR),
                           ('INNERGRID', (0,0), (-1,-1), 0.3, RULE_COLOR),
                           ('TOPPADDING', (0,0), (-1,-1), 4), ('BOTTOMPADDING', (0,0), (-1,-1), 4),
                           ('LEFTPADDING', (0,0), (-1,-1), 6), ('RIGHTPADDING', (0,0), (-1,-1), 6),
                           ('VALIGN', (0,0), (-1,-1), 'TOP'),
                       ])))

    story.append(Paragraph("10.3 Peltier Electrical Power and Energy", S['section_heading']))
    story.append(Paragraph("P_elec = V_op × I_op", S['equation']))
    story.append(Paragraph("E_elec = P_elec × t_active  [expressed in Wh = J ÷ 3600]", S['equation']))
    calc_rows3 = [
        [Paragraph("<b>Parameter</b>", S['table_header']),
         Paragraph("<b>Symbol</b>", S['table_header']),
         Paragraph("<b>Unit</b>", S['table_header']),
         Paragraph("<b>Value</b>", S['table_header'])],
        [Paragraph("Operating voltage", S['table_cell']), Paragraph("V_op", S['table_cell_c']),
         Paragraph("V", S['table_cell_c']), ph("[ __ ]")],
        [Paragraph("Operating current", S['table_cell']), Paragraph("I_op", S['table_cell_c']),
         Paragraph("A", S['table_cell_c']), ph("[ __ ]")],
        [Paragraph("Peltier electrical power", S['table_cell']), Paragraph("P_elec", S['table_cell_c']),
         Paragraph("W", S['table_cell_c']), ph("[ V × I ]")],
        [Paragraph("Estimated Peltier active duration", S['table_cell']), Paragraph("t_active", S['table_cell_c']),
         Paragraph("h", S['table_cell_c']), ph("[ from experiment ]")],
        [Paragraph("Total electrical energy consumed", S['table_cell']), Paragraph("E_total", S['table_cell_c']),
         Paragraph("Wh", S['table_cell_c']), ph("[ P × t ]")],
        [Paragraph("Required battery capacity", S['table_cell']), Paragraph("C_bat", S['table_cell_c']),
         Paragraph("Ah", S['table_cell_c']), ph("[ E_total / V_bat ]")],
    ]
    story.append(Table(calc_rows3, colWidths=[65*mm, 25*mm, 25*mm, 55*mm],
                       style=TableStyle([
                           ('BACKGROUND', (0,0), (-1,0), TEAL),
                           ('ROWBACKGROUNDS', (0,1), (-1,-1), [TABLE_BG, WHITE]),
                           ('BOX', (0,0), (-1,-1), 0.5, RULE_COLOR),
                           ('INNERGRID', (0,0), (-1,-1), 0.3, RULE_COLOR),
                           ('TOPPADDING', (0,0), (-1,-1), 4), ('BOTTOMPADDING', (0,0), (-1,-1), 4),
                           ('LEFTPADDING', (0,0), (-1,-1), 6), ('RIGHTPADDING', (0,0), (-1,-1), 6),
                           ('VALIGN', (0,0), (-1,-1), 'TOP'),
                       ])))

    story.append(Paragraph("10.4 Coefficient of Performance", S['section_heading']))
    story.append(Paragraph("COP = Q̇_cold / P_elec", S['equation']))
    story.append(Paragraph(
        "where Q̇_cold is the actual cold-side cooling power (W) measured during testing. "
        "COP values for Peltier TECs typically range from 0.3 to 0.8 at practical temperature "
        "differentials. COP will be calculated from experimental measurements.",
        S['body']))
    story.append(Spacer(1, 2*mm))
    story.append(Paragraph(
        "<i>Calculation Worksheet Status: All fields above are to be populated with measured "
        "values following prototype testing. No values have been assumed or invented.</i>",
        ParagraphStyle('ws_note', fontName='Helvetica-Oblique', fontSize=8.5,
                       textColor=colors.HexColor("#7A5C00"), alignment=TA_LEFT, leading=12)))
    return story


def page18_prototype(S):
    story = []
    story.append(Spacer(1, 8*mm))
    story.append(section_banner("11. PROTOTYPE DEVELOPMENT"))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph(
        "The SANJIVANI prototype was developed in a phased assembly sequence. Each stage was "
        "documented and inspected before proceeding to the next. The following describes the "
        "development process and provides placeholders for prototype photographs.",
        S['body']))

    steps = [
        ("Stage 1: Insulated Chamber Preparation",
         "The insulated enclosure was selected or fabricated to provide adequate internal volume "
         "for the PCM and payload, with effective thermal insulation on all faces. "
         "Penetrations for the Peltier assembly and sensor wiring were carefully sealed to maintain insulation integrity."),
        ("Stage 2: PCM Arrangement",
         "The selected Phase Change Material was placed in a sealed container within the enclosure. "
         "The PCM container was designed to allow good thermal contact with the aluminium spreader "
         "while preventing leakage into the payload zone."),
        ("Stage 3: Aluminium Plate Preparation",
         "Aluminium plates were cut and finished to the required dimensions. Contact surfaces were "
         "cleaned and smoothed. Thermal interface material was applied to all mating surfaces "
         "to minimise contact resistance."),
        ("Stage 4: Peltier Module Assembly",
         "Peltier module(s) were mounted with cold faces in contact with the aluminium spreader "
         "(via thermal interface material) and hot faces interfacing with the liquid thermal transfer "
         "chamber or heat sink assembly. Uniform clamping force was applied to ensure good contact."),
        ("Stage 5: Liquid Thermal Transfer Arrangement",
         "The liquid chamber or circulation element was assembled and leak-tested. The liquid medium "
         "was filled to the appropriate level. All connections were sealed and inspected."),
        ("Stage 6: Hot-Side Heat Rejection",
         "The hot-side heat sink and/or heat exchanger was mounted and thermally coupled to the "
         "Peltier hot face. Airflow arrangements (fan, natural convection) were configured."),
        ("Stage 7: Sensor Integration",
         "Temperature sensors were positioned in the payload zone, at the PCM interface and at the "
         "Peltier surfaces as required. Sensor leads were routed to the microcontroller."),
        ("Stage 8: Controller and Electronics Integration",
         "The microcontroller was programmed with the hysteresis control algorithm. The switching "
         "module (MOSFET / relay) was wired to control Peltier power. The control software was "
         "bench-tested before full assembly."),
        ("Stage 9: Wiring and Safety Checks",
         "All electrical connections were inspected. Wire gauges were verified for the rated current. "
         "Polarity of Peltier connections was confirmed. The power supply was tested before connection."),
        ("Stage 10: Final Assembly and Inspection",
         "The complete system was assembled and visually inspected. A preliminary functional test "
         "was conducted to confirm that sensors respond, the controller operates correctly and "
         "the Peltier module activates and deactivates as intended."),
    ]

    for title, text in steps:
        story.append(Paragraph(title, S['subsection_heading']))
        story.append(Paragraph(text, S['body']))

    # Photograph placeholders
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph("Prototype Photographs (to be inserted by team):", S['section_heading']))
    photo_rows = [
        [ph("Figure P1 — Assembled SANJIVANI Prototype (External View)"),
         ph("Figure P2 — Internal Assembly: PCM + Al Spreader + Peltier")],
        [ph("Figure P3 — Controller and Sensor Wiring Detail"),
         ph("Figure P4 — Hot-Side Heat Rejection Assembly")],
    ]
    story.append(Table(photo_rows, colWidths=[84*mm, 86*mm],
                       style=TableStyle([
                           ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                           ('TOPPADDING', (0,0), (-1,-1), 6),
                           ('BOTTOMPADDING', (0,0), (-1,-1), 6),
                           ('LEFTPADDING', (0,0), (-1,-1), 4),
                           ('RIGHTPADDING', (0,0), (-1,-1), 4),
                       ])))
    return story


def page19_methodology(S):
    story = []
    story.append(Spacer(1, 8*mm))
    story.append(section_banner("12. EXPERIMENTAL METHODOLOGY"))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("12.1 Experimental Design Overview", S['section_heading']))
    story.append(Paragraph(
        "A controlled comparative experiment is designed to evaluate the performance of the SANJIVANI "
        "hybrid system relative to conventional PCM-only cooling. Two configurations are tested under "
        "identical conditions and their temperature profiles and energy consumption are compared.",
        S['body']))
    story.append(Spacer(1, 3*mm))
    story.append(ExperimentalSetupDiagram(width=PAGE_W - L_MARGIN - R_MARGIN, height=55*mm))
    story.append(Spacer(1, 3*mm))

    story.append(Paragraph("12.2 Variables", S['section_heading']))
    var_rows = [
        [Paragraph("<b>Variable Type</b>", S['table_header']),
         Paragraph("<b>Variable</b>", S['table_header']),
         Paragraph("<b>Description</b>", S['table_header'])],
        [Paragraph("Independent Variable", S['table_cell']),
         Paragraph("Cooling configuration", S['table_cell']),
         Paragraph("Config A: PCM only;  Config B: PCM + Peltier (SANJIVANI)", S['table_cell'])],
        [Paragraph("Dependent Variables", S['table_cell']),
         Paragraph("Internal temperature, T(t)", S['table_cell']),
         Paragraph("Payload-zone temperature recorded vs. time", S['table_cell'])],
        [Paragraph("", S['table_cell']),
         Paragraph("Duration within target range", S['table_cell']),
         Paragraph("Time (hours) for which T remains below the upper limit", S['table_cell'])],
        [Paragraph("", S['table_cell']),
         Paragraph("Electrical energy consumed, E_elec", S['table_cell']),
         Paragraph("Total Wh consumed by Peltier system (Config B only)", S['table_cell'])],
        [Paragraph("", S['table_cell']),
         Paragraph("Peltier duty cycle", S['table_cell']),
         Paragraph("Fraction of test time Peltier is active (Config B)", S['table_cell'])],
        [Paragraph("Controlled Variables", S['table_cell']),
         Paragraph("PCM type, quantity and pre-conditioning", S['table_cell']),
         Paragraph("Identical for both configurations", S['table_cell'])],
        [Paragraph("", S['table_cell']),
         Paragraph("Insulated enclosure", S['table_cell']),
         Paragraph("Same enclosure used for both tests", S['table_cell'])],
        [Paragraph("", S['table_cell']),
         Paragraph("Ambient temperature", S['table_cell']),
         Paragraph("Monitored and recorded throughout; tests conducted in same environment", S['table_cell'])],
        [Paragraph("", S['table_cell']),
         Paragraph("Initial PCM temperature", S['table_cell']),
         Paragraph("PCM fully pre-conditioned to same temperature before each trial", S['table_cell'])],
        [Paragraph("", S['table_cell']),
         Paragraph("Payload thermal mass", S['table_cell']),
         Paragraph("Equivalent thermal dummy payload used in both configurations", S['table_cell'])],
    ]
    story.append(Table(var_rows, colWidths=[40*mm, 52*mm, 78*mm],
                       style=TableStyle([
                           ('BACKGROUND', (0,0), (-1,0), NAVY),
                           ('ROWBACKGROUNDS', (0,1), (-1,-1), [TABLE_BG, WHITE]),
                           ('BOX', (0,0), (-1,-1), 0.5, RULE_COLOR),
                           ('INNERGRID', (0,0), (-1,-1), 0.3, RULE_COLOR),
                           ('TOPPADDING', (0,0), (-1,-1), 4), ('BOTTOMPADDING', (0,0), (-1,-1), 4),
                           ('LEFTPADDING', (0,0), (-1,-1), 6), ('RIGHTPADDING', (0,0), (-1,-1), 6),
                           ('VALIGN', (0,0), (-1,-1), 'TOP'),
                       ])))

    story.append(Paragraph("12.3 Procedure", S['section_heading']))
    proc_steps = [
        "Pre-condition the PCM fully (freeze / solidify) to the designated temperature in a refrigerator.",
        "Allow ambient temperature to stabilise and record T_ambient at the start of the trial.",
        "Assemble the enclosure with PCM and place the thermal dummy payload inside.",
        "Start the data logger and begin recording all sensor channels at the defined sampling interval.",
        "For Configuration A: allow passive PCM cooling only. Record until internal temperature exceeds the upper limit.",
        "For Configuration B: start the SANJIVANI control system. The microcontroller manages Peltier activation. "
        "Record all channels (temperature, Peltier state, electrical measurements) continuously.",
        "Record the total time for which internal temperature remains within the defined target range.",
        "Record total electrical energy consumed (Wh) for Configuration B.",
        "Repeat each configuration for a minimum of three trials to assess repeatability, "
        "subject to available resources and time constraints.",
        "Process data: plot temperature vs. time for all trials, calculate mean values and compare configurations.",
    ]
    for i, step in enumerate(proc_steps, 1):
        story.append(numbered_item(i, step))

    story.append(Spacer(1, 3*mm))
    story.append(Paragraph("12.4 Measurement Instruments and Logging", S['section_heading']))
    story.append(Paragraph(
        "Temperature sensors shall be calibrated against a reference thermometer before testing. "
        "Electrical measurements (voltage and current) shall be recorded using a multimeter or data "
        "logger with appropriate accuracy. All raw data shall be preserved in the annexure.", S['body']))
    return story


def page20_observations(S):
    story = []
    story.append(Spacer(1, 8*mm))
    story.append(section_banner("13. OBSERVATIONS AND DATA COLLECTION"))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph(
        "The following observation tables are designed for recording experimental data during testing. "
        "All highlighted cells are to be completed by the team during and after experiments. "
        "Multiple copies of these tables should be maintained for each trial.",
        S['body']))

    story.append(Paragraph("Table 1 — Configuration A: PCM-Only Cooling (Trial 1 / 2 / 3)", S['subsection_heading']))
    story.append(Paragraph(
        "Pre-condition temperature: ____ °C  |  Ambient temp (start): ____ °C  |  Trial no.: ____",
        S['body_sm']))

    obs_header = [
        Paragraph("<b>Time\n(h:mm)</b>", S['table_header']),
        Paragraph("<b>T_ambient\n(°C)</b>", S['table_header']),
        Paragraph("<b>T_payload\n(°C)</b>", S['table_header']),
        Paragraph("<b>T_PCM\n(°C)</b>", S['table_header']),
        Paragraph("<b>Remarks</b>", S['table_header']),
    ]
    obs_rows_a = [obs_header]
    for _ in range(14):
        obs_rows_a.append([ph("") , ph(""), ph(""), ph(""), ph("")])
    story.append(Table(obs_rows_a, colWidths=[22*mm, 25*mm, 25*mm, 25*mm, 73*mm],
                       style=TableStyle([
                           ('BACKGROUND', (0,0), (-1,0), NAVY),
                           ('ROWBACKGROUNDS', (0,1), (-1,-1), [AMBER_PH, colors.HexColor("#FFFEF0")]),
                           ('BOX', (0,0), (-1,-1), 0.5, RULE_COLOR),
                           ('INNERGRID', (0,0), (-1,-1), 0.3, RULE_COLOR),
                           ('TOPPADDING', (0,0), (-1,-1), 5), ('BOTTOMPADDING', (0,0), (-1,-1), 5),
                           ('LEFTPADDING', (0,0), (-1,-1), 4), ('RIGHTPADDING', (0,0), (-1,-1), 4),
                           ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                       ])))

    story.append(Spacer(1, 4*mm))
    story.append(Paragraph("Table 2 — Configuration B: SANJIVANI Hybrid System (Trial 1 / 2 / 3)", S['subsection_heading']))
    story.append(Paragraph(
        "Pre-condition temperature: ____ °C  |  Ambient temp (start): ____ °C  |  Trial no.: ____",
        S['body_sm']))

    obs_header_b = [
        Paragraph("<b>Time\n(h:mm)</b>", S['table_header']),
        Paragraph("<b>T_ambient\n(°C)</b>", S['table_header']),
        Paragraph("<b>T_payload\n(°C)</b>", S['table_header']),
        Paragraph("<b>T_PCM\n(°C)</b>", S['table_header']),
        Paragraph("<b>T_cold\n(°C)</b>", S['table_header']),
        Paragraph("<b>T_hot\n(°C)</b>", S['table_header']),
        Paragraph("<b>V (V)</b>", S['table_header']),
        Paragraph("<b>I (A)</b>", S['table_header']),
        Paragraph("<b>Peltier\nON/OFF</b>", S['table_header']),
    ]
    obs_rows_b = [obs_header_b]
    for _ in range(14):
        obs_rows_b.append([ph("") for _ in range(9)])
    story.append(Table(obs_rows_b, colWidths=[17*mm, 18*mm, 18*mm, 18*mm, 17*mm, 17*mm, 14*mm, 14*mm, 17*mm],
                       style=TableStyle([
                           ('BACKGROUND', (0,0), (-1,0), TEAL_DARK),
                           ('ROWBACKGROUNDS', (0,1), (-1,-1), [AMBER_PH, colors.HexColor("#FFFEF0")]),
                           ('BOX', (0,0), (-1,-1), 0.5, RULE_COLOR),
                           ('INNERGRID', (0,0), (-1,-1), 0.3, RULE_COLOR),
                           ('TOPPADDING', (0,0), (-1,-1), 5), ('BOTTOMPADDING', (0,0), (-1,-1), 5),
                           ('LEFTPADDING', (0,0), (-1,-1), 3), ('RIGHTPADDING', (0,0), (-1,-1), 3),
                           ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                           ('FONTSIZE', (0,0), (-1,-1), 7),
                       ])))
    story.append(Spacer(1, 2*mm))
    story.append(Paragraph(
        "<i>Note: Sampling interval to be defined (e.g. every 15 or 30 minutes). "
        "Additional rows can be added. Duplicate this table for each trial.</i>",
        ParagraphStyle('obs_note', fontName='Helvetica-Oblique', fontSize=7.5,
                       textColor=SLATE, alignment=TA_LEFT, leading=11)))
    return story


def page21_results(S):
    story = []
    story.append(Spacer(1, 8*mm))
    story.append(section_banner("14. RESULTS, GRAPHS AND ANALYSIS"))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph(
        "The following section provides the structure for recording, presenting and interpreting "
        "experimental results. All graph spaces and result fields are placeholders to be completed "
        "by the team after testing. No results have been fabricated or assumed.",
        S['body']))

    story.append(Paragraph("14.1 Temperature vs. Time Graph", S['section_heading']))
    story.append(ph("GRAPH 1 — Temperature (°C) vs. Time (hours): Config A vs Config B\n"
                    "Plot T_payload for both configurations on the same axes. Mark the upper "
                    "and lower thresholds. Indicate Peltier ON/OFF periods."))
    story.append(Spacer(1, 3*mm))

    story.append(Paragraph("14.2 Summary Results Table", S['section_heading']))
    res_rows = [
        [Paragraph("<b>Metric</b>", S['table_header']),
         Paragraph("<b>Config A: PCM Only</b>", S['table_header']),
         Paragraph("<b>Config B: SANJIVANI</b>", S['table_header']),
         Paragraph("<b>Difference</b>", S['table_header'])],
        [Paragraph("Duration within target range (Trial 1)", S['table_cell']),
         ph("__ h"), ph("__ h"), ph("__ h")],
        [Paragraph("Duration within target range (Trial 2)", S['table_cell']),
         ph("__ h"), ph("__ h"), ph("__ h")],
        [Paragraph("Duration within target range (Trial 3)", S['table_cell']),
         ph("__ h"), ph("__ h"), ph("__ h")],
        [Paragraph("Mean duration within target range", S['table_cell']),
         ph("__ h"), ph("__ h"), ph("__ %")],
        [Paragraph("Mean rate of temperature rise (°C h⁻¹)", S['table_cell']),
         ph("__"), ph("__"), ph("__")],
        [Paragraph("Peltier duty cycle (%)", S['table_cell']),
         Paragraph("N/A — no Peltier", S['table_cell']), ph("__ %"),
         Paragraph("N/A", S['table_cell'])],
        [Paragraph("Total electrical energy consumed (Wh)", S['table_cell']),
         Paragraph("0 (passive only)", S['table_cell']), ph("__ Wh"),
         Paragraph("N/A", S['table_cell'])],
    ]
    story.append(Table(res_rows, colWidths=[62*mm, 36*mm, 36*mm, 36*mm],
                       style=TableStyle([
                           ('BACKGROUND', (0,0), (-1,0), NAVY),
                           ('ROWBACKGROUNDS', (0,1), (-1,-1), [TABLE_BG, WHITE]),
                           ('BOX', (0,0), (-1,-1), 0.5, RULE_COLOR),
                           ('INNERGRID', (0,0), (-1,-1), 0.3, RULE_COLOR),
                           ('TOPPADDING', (0,0), (-1,-1), 4), ('BOTTOMPADDING', (0,0), (-1,-1), 4),
                           ('LEFTPADDING', (0,0), (-1,-1), 6), ('RIGHTPADDING', (0,0), (-1,-1), 6),
                           ('VALIGN', (0,0), (-1,-1), 'TOP'),
                       ])))

    story.append(Spacer(1, 3*mm))
    story.append(Paragraph("14.3 Additional Graphs (Placeholders)", S['section_heading']))
    graph_phs = [
        "GRAPH 2 — Peltier ON/OFF State vs. Time (Config B): Step chart showing duty cycle pattern",
        "GRAPH 3 — PCM Temperature vs. Time: Compare rate of PCM warming across both configurations",
        "GRAPH 4 — Trial Repeatability: Overlay three trials of each configuration for consistency check",
        "GRAPH 5 — Electrical Energy Accumulation vs. Time (Config B): Cumulative Wh consumed",
    ]
    for g in graph_phs:
        story.append(ph(g))
        story.append(Spacer(1, 2*mm))

    story.append(Paragraph("14.4 Results Interpretation Framework", S['section_heading']))
    story.append(Paragraph(
        "Following completion of experiments, the team should address the following analytical questions:",
        S['body']))
    questions = [
        "Does the SANJIVANI hybrid system extend the duration within the target temperature range compared to Config A? By how much, and is the difference statistically consistent across three trials?",
        "What is the Peltier duty cycle? Does the system cycle frequently or infrequently — and what does this indicate about the balance between heat ingress and Peltier cooling power?",
        "Is the electrical energy consumption practical for a battery-powered deployment of the stated duration?",
        "Are there periods of temperature instability or significant temperature gradients within the payload zone?",
        "Does the hot-side temperature remain within safe bounds throughout the test, confirming adequate heat rejection?",
        "How do the results compare with the engineering design targets stated in Section 3.5?",
    ]
    for i, q in enumerate(questions, 1):
        story.append(numbered_item(i, q))
    return story


def page22_economic(S):
    story = []
    story.append(Spacer(1, 8*mm))
    story.append(section_banner("15. ENERGY, COST AND ECONOMIC FEASIBILITY"))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("15.1 Prototype Component Cost Framework", S['section_heading']))
    story.append(Paragraph(
        "The table below provides a framework for recording actual component costs. "
        "Prices are to be inserted by the team based on actual procurement. "
        "No prices have been assumed or invented.",
        S['body']))

    cost_rows = [
        [Paragraph("<b>#</b>", S['table_header']),
         Paragraph("<b>Component</b>", S['table_header']),
         Paragraph("<b>Qty</b>", S['table_header']),
         Paragraph("<b>Unit Cost (₹)</b>", S['table_header']),
         Paragraph("<b>Total Cost (₹)</b>", S['table_header'])],
        [Paragraph("1", S['table_cell_c']), Paragraph("Phase Change Material", S['table_cell']),
         ph("__"), ph("__"), ph("__")],
        [Paragraph("2", S['table_cell_c']), Paragraph("Insulated Enclosure", S['table_cell']),
         ph("1"), ph("__"), ph("__")],
        [Paragraph("3", S['table_cell_c']), Paragraph("Peltier TEC Module(s)", S['table_cell']),
         ph("__"), ph("__"), ph("__")],
        [Paragraph("4", S['table_cell_c']), Paragraph("Aluminium Plate / Sheet", S['table_cell']),
         ph("__"), ph("__"), ph("__")],
        [Paragraph("5", S['table_cell_c']), Paragraph("Liquid Chamber / Fittings", S['table_cell']),
         ph("1"), ph("__"), ph("__")],
        [Paragraph("6", S['table_cell_c']), Paragraph("Heat Sink and Fan", S['table_cell']),
         ph("__"), ph("__"), ph("__")],
        [Paragraph("7", S['table_cell_c']), Paragraph("Temperature Sensors", S['table_cell']),
         ph("__"), ph("__"), ph("__")],
        [Paragraph("8", S['table_cell_c']), Paragraph("Microcontroller", S['table_cell']),
         ph("1"), ph("__"), ph("__")],
        [Paragraph("9", S['table_cell_c']), Paragraph("Switching Module (MOSFET/Relay)", S['table_cell']),
         ph("1"), ph("__"), ph("__")],
        [Paragraph("10", S['table_cell_c']), Paragraph("Power Supply / Battery", S['table_cell']),
         ph("1"), ph("__"), ph("__")],
        [Paragraph("11", S['table_cell_c']), Paragraph("Thermal Interface Material", S['table_cell']),
         ph("__"), ph("__"), ph("__")],
        [Paragraph("12", S['table_cell_c']), Paragraph("Miscellaneous (wire, connectors, hardware)", S['table_cell']),
         Paragraph("—", S['table_cell_c']), ph("__"), ph("__")],
        [Paragraph("", S['table_cell']),
         Paragraph("<b>TOTAL PROTOTYPE COST</b>", S['table_cell']),
         Paragraph("", S['table_cell']), Paragraph("", S['table_cell']),
         ph("₹ __ ")],
    ]
    story.append(Table(cost_rows, colWidths=[9*mm, 72*mm, 15*mm, 28*mm, 46*mm],
                       style=TableStyle([
                           ('BACKGROUND', (0,0), (-1,0), NAVY),
                           ('ROWBACKGROUNDS', (0,1), (-1,-2), [TABLE_BG, WHITE]),
                           ('BACKGROUND', (0,-1), (-1,-1), GOLD_LIGHT),
                           ('BOX', (0,0), (-1,-1), 0.5, RULE_COLOR),
                           ('INNERGRID', (0,0), (-1,-1), 0.3, RULE_COLOR),
                           ('TOPPADDING', (0,0), (-1,-1), 4), ('BOTTOMPADDING', (0,0), (-1,-1), 4),
                           ('LEFTPADDING', (0,0), (-1,-1), 5), ('RIGHTPADDING', (0,0), (-1,-1), 5),
                           ('VALIGN', (0,0), (-1,-1), 'TOP'),
                       ])))

    story.append(Spacer(1, 4*mm))
    story.append(Paragraph("15.2 Operating Energy and Cost Estimate", S['section_heading']))
    op_rows = [
        [Paragraph("<b>Parameter</b>", S['table_header']),
         Paragraph("<b>Value</b>", S['table_header']),
         Paragraph("<b>Notes</b>", S['table_header'])],
        [Paragraph("Peltier operating power", S['table_cell']), ph("__ W"),
         Paragraph("From measurements: V × I", S['table_cell'])],
        [Paragraph("Estimated Peltier active duration (per deployment)", S['table_cell']), ph("__ h"),
         Paragraph("From duty cycle experiment", S['table_cell'])],
        [Paragraph("Total electrical energy per deployment", S['table_cell']), ph("__ Wh"),
         Paragraph("P_elec × t_active", S['table_cell'])],
        [Paragraph("Battery capacity required", S['table_cell']), ph("__ Ah at __ V"),
         Paragraph("E_total / V_battery", S['table_cell'])],
        [Paragraph("Estimated battery cost", S['table_cell']), ph("₹ __"),
         Paragraph("From procurement", S['table_cell'])],
        [Paragraph("Approximate grid energy cost (if applicable)", S['table_cell']), ph("₹ __"),
         Paragraph("E_total (kWh) × tariff rate", S['table_cell'])],
    ]
    story.append(Table(op_rows, colWidths=[72*mm, 30*mm, 68*mm],
                       style=TableStyle([
                           ('BACKGROUND', (0,0), (-1,0), TEAL),
                           ('ROWBACKGROUNDS', (0,1), (-1,-1), [TABLE_BG, WHITE]),
                           ('BOX', (0,0), (-1,-1), 0.5, RULE_COLOR),
                           ('INNERGRID', (0,0), (-1,-1), 0.3, RULE_COLOR),
                           ('TOPPADDING', (0,0), (-1,-1), 4), ('BOTTOMPADDING', (0,0), (-1,-1), 4),
                           ('LEFTPADDING', (0,0), (-1,-1), 6), ('RIGHTPADDING', (0,0), (-1,-1), 6),
                           ('VALIGN', (0,0), (-1,-1), 'TOP'),
                       ])))

    story.append(Spacer(1, 4*mm))
    story.append(Paragraph("15.3 Feasibility Discussion", S['section_heading']))
    story.append(Paragraph(
        "The economic feasibility of SANJIVANI will be evaluated after actual costs and energy "
        "measurements are available. Relevant considerations include: "
        "(a) the incremental cost of the thermoelectric assembly relative to the value of the medical "
        "products being protected; "
        "(b) the battery cost and capacity required to support the design operating duration; "
        "(c) the potential benefit of extending cold-chain duration, expressed in terms of reduced "
        "product wastage or reduced frequency of re-conditioning logistics; and "
        "(d) the suitability of the system for scaling to larger volumes or multi-unit deployment. "
        "No superiority claim is made without supporting calculated data.",
        S['body']))
    return story


def page23_safety(S):
    story = []
    story.append(Spacer(1, 8*mm))
    story.append(section_banner("16. SAFETY, LIMITATIONS AND RELIABILITY"))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("16.1 Prototype Safety Considerations", S['section_heading']))
    safety_items = [
        ("Electrical safety:", "All wiring must be appropriately rated for the operating current. "
         "Connections must be properly insulated. The power supply must include overload and short-circuit protection. "
         "Components should be handled only when the system is powered off."),
        ("Liquid leakage:", "The liquid thermal transfer chamber must be constructed from compatible "
         "materials and leak-tested before integration. A leak near electrical components "
         "creates a serious hazard."),
        ("Condensation:", "Surfaces operating below ambient dew point will attract condensation. "
         "Electrical components in the vicinity of cold surfaces must be protected from moisture. "
         "Condensate management must be considered in the final design."),
        ("Peltier hot-side overheating:", "If hot-side heat rejection is inadequate, the Peltier "
         "module temperature can rise to damaging levels. Hot-side temperature should be monitored "
         "and an over-temperature software interlock implemented."),
        ("Sensor failure:", "A disconnected or malfunctioning temperature sensor may cause "
         "erroneous control decisions. The control software should validate sensor readings before "
         "acting on them and alert the user to suspect readings."),
        ("PCM handling:", "The selected PCM should be non-toxic and non-flammable. The PCM "
         "container must remain sealed to prevent spills. Users should wear gloves when handling cold PCM."),
        ("Battery safety:", "Lithium-based batteries must not be overcharged, over-discharged or "
         "short-circuited. Use of a battery management module (BMS) is recommended."),
    ]
    for title, text in safety_items:
        story.append(bullet(f"<b>{title}</b> {text}"))

    story.append(Spacer(1, 4*mm))
    story.append(Paragraph("16.2 Engineering Limitations", S['section_heading']))
    limitations = [
        ("Finite electrical energy:", "The Peltier system requires electrical power. When battery capacity "
         "is exhausted, the system reverts to PCM-only passive cooling. The system does not operate "
         "indefinitely without a power source."),
        ("Peltier efficiency:", "Peltier TECs have a COP typically below 1 at practical temperature "
         "differentials. The hot side rejects more heat than the cold side absorbs. If hot-side "
         "rejection is inadequate, net performance may be negative."),
        ("PCM recovery:", "While Peltier cooling may slow heat ingress into the PCM, it cannot "
         "fully re-solidify a significantly melted PCM during a typical duty cycle without substantially "
         "increasing electrical energy input. Partial latent heat recovery is feasible; "
         "complete re-solidification in situ requires more investigation."),
        ("Temperature non-uniformity:", "The PCM and payload temperature may not be uniform throughout "
         "the enclosure. Single-point sensor readings may not represent the entire internal condition."),
        ("Prototype vs commercial device:", "SANJIVANI is a student engineering prototype developed "
         "in a school laboratory. It has not undergone regulatory validation, vibration testing, "
         "long-term reliability assessment or independent laboratory verification."),
        ("Medical use disclaimer:", "This prototype must NOT be used for actual clinical storage "
         "of vaccines, blood products, insulin or any medical product intended for patient use "
         "until it has been appropriately validated, tested and approved by relevant regulatory authorities."),
    ]
    for title, text in limitations:
        story.append(bullet(f"<b>{title}</b> {text}"))

    story.append(Spacer(1, 4*mm))
    story.append(Paragraph("16.3 Maintenance and Reliability", S['section_heading']))
    story.append(Paragraph(
        "The SANJIVANI prototype requires the following maintenance actions before each deployment: "
        "(a) PCM re-conditioning (re-freezing) in a refrigerator; "
        "(b) battery charging to full capacity; "
        "(c) sensor calibration check; "
        "(d) visual inspection of all electrical connections, liquid chamber integrity and "
        "aluminium contact surfaces; "
        "(e) functional test of the control system to confirm correct threshold-based switching. "
        "Long-term reliability will depend on the durability of the Peltier module under repeated "
        "thermal cycling, the integrity of the liquid chamber seals and the stability of sensor calibration.",
        S['body']))
    return story


def page24_conclusion(S):
    story = []
    story.append(Spacer(1, 8*mm))
    story.append(section_banner("17. CONCLUSION AND FUTURE SCOPE"))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("17.1 Conclusions from This Investigation", S['section_heading']))
    story.append(Paragraph(
        "SANJIVANI proposes a hybrid PCM–Peltier thermal management architecture that integrates "
        "passive latent heat storage with intelligently triggered thermoelectric cooling to address "
        "the duration limitation of conventional portable medical coolers. The engineering principles "
        "underlying the system — PCM latent heat storage, Peltier thermoelectric heat pumping, "
        "aluminium thermal spreading and liquid-assisted heat transport — are scientifically sound "
        "and have been explained in this report.",
        S['body']))
    story.append(Paragraph(
        "The proposed sensor-triggered hysteresis control strategy offers a principled approach to "
        "minimising unnecessary electrical energy consumption while providing supplementary cooling "
        "when genuinely needed. The design correctly accounts for the thermodynamic requirement that "
        "the Peltier hot side must reject heat to the external environment and that the system "
        "requires a continuous electrical energy source while active.",
        S['body']))
    story.append(Paragraph(
        "The design targets — extending temperature-holding duration from approximately 72 hours "
        "towards approximately 110 hours — represent engineering aspirations derived from preliminary "
        "analysis. These targets have NOT been experimentally verified at the time of this submission. "
        "Verification requires the completion of controlled comparative experiments as described in "
        "Section 12 of this report.",
        S['body']))

    story.append(Paragraph("17.2 Anticipated Engineering Challenges", S['section_heading']))
    challenges = [
        "Achieving effective thermal contact between the Peltier cold face, aluminium spreader and PCM.",
        "Ensuring adequate hot-side heat rejection without excessive energy penalty from fans or pumps.",
        "Selecting PCM with appropriate phase-change temperature for the target storage range.",
        "Calibrating and validating the control algorithm's threshold values.",
        "Managing condensation on cold external surfaces without compromising insulation.",
        "Demonstrating adequate battery capacity for the full target operating duration.",
    ]
    for c in challenges:
        story.append(bullet(c))

    story.append(Paragraph("17.3 Future Scope", S['section_heading']))
    future = [
        ("Improved PCM selection:", "Evaluate salt hydrates or bio-based PCMs with optimised "
         "phase-change temperatures and higher latent heat for the specific medical product range."),
        ("Advanced temperature control:", "Implement PID or predictive control strategies "
         "to improve temperature stability and reduce Peltier cycling."),
        ("Optimised thermal coupling:", "Investigate advanced thermal interface materials, "
         "vapour chambers or heat pipes for improved cold-side coupling."),
        ("Liquid heat-transfer optimisation:", "Design and test a gravity-driven or pumped "
         "liquid circulation loop for more effective hot-side heat rejection."),
        ("Extended validation testing:", "Conduct multi-day trials under varying ambient "
         "conditions and thermal loads to validate performance across realistic scenarios."),
        ("Energy system integration:", "Integrate a solar charging panel to maintain battery "
         "charge during field deployment for extended off-grid operation."),
        ("Miniaturisation and packaging:", "Develop a compact, rugged housing suitable for "
         "field deployment, with sealed, waterproof connectors and tamper-evident closure."),
        ("Expert evaluation:", "Engage with cold-chain logistics and medical technology "
         "experts to evaluate the system's potential applicability and obtain independent feedback."),
        ("Regulatory pathway awareness:", "Research the regulatory requirements (e.g. WHO PQS, "
         "BIS standards) that would apply to a device of this type if developed for actual medical use."),
    ]
    for title, text in future:
        story.append(bullet(f"<b>{title}</b> {text}"))

    story.append(Spacer(1, 4*mm))
    story.append(hr())
    story.append(Spacer(1, 2*mm))
    story.append(Paragraph(
        "<i>SANJIVANI is a student engineering innovation — a serious attempt to address a real healthcare "
        "infrastructure challenge through the application of thermal engineering principles. The work "
        "presented here reflects the team's honest inquiry, transparent acknowledgement of limitations "
        "and commitment to scientific integrity.</i>",
        ParagraphStyle('closing', fontName='Helvetica-BoldOblique', fontSize=10, textColor=TEAL_DARK,
                       alignment=TA_CENTER, leading=15)))
    return story


def page25_references(S):
    story = []
    story.append(Spacer(1, 8*mm))
    story.append(section_banner("18. REFERENCES AND ANNEXURES"))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("18.1 References", S['section_heading']))
    story.append(Paragraph(
        "All references listed below are real, verifiable sources. Full retrieval information is provided. "
        "In-text citations use square bracket numbering consistent with the body of the report.",
        S['body_sm']))
    story.append(Spacer(1, 2*mm))

    refs = [
        ("[1]", "World Health Organisation (WHO). <i>Temperature-sensitive Healthcare Products: "
         "Maintaining the Cold Chain.</i> Geneva: WHO Press. Available at: "
         "https://www.who.int/teams/health-product-and-policy-standards/standards-and-specifications/"
         "vaccine-quality/cold-chain"),
        ("[2]", "World Health Organisation (WHO). <i>WHO Technical Report Series No. 961: "
         "Annex 9 — Model guidance for the storage and transport of time- and temperature-sensitive "
         "pharmaceutical products.</i> Geneva: WHO, 2011."),
        ("[3]", "Ministry of Health and Family Welfare, Government of India. "
         "<i>Universal Immunisation Programme (UIP) Cold Chain Handbook.</i> "
         "New Delhi: MoHFW. Available at: https://main.mohfw.gov.in/"),
        ("[4]", "Farid, M. M., Khudhair, A. M., Razack, S. A. K., & Al-Hallaj, S. (2004). "
         "A review on phase change energy storage: materials and applications. "
         "<i>Energy Conversion and Management</i>, 45(9–10), 1597–1615. "
         "https://doi.org/10.1016/j.enconman.2003.09.015"),
        ("[5]", "Oró, E., de Gracia, A., Castell, A., Farid, M. M., & Cabeza, L. F. (2012). "
         "Review on phase change materials (PCMs) for cold thermal energy storage applications. "
         "<i>Applied Energy</i>, 99, 513–533. "
         "https://doi.org/10.1016/j.apenergy.2012.03.058"),
        ("[6]", "Rowe, D. M. (Ed.). (2006). <i>Thermoelectrics Handbook: Macro to Nano.</i> "
         "Boca Raton: CRC Press / Taylor & Francis."),
        ("[7]", "Incropera, F. P., DeWitt, D. P., Bergman, T. L., & Lavine, A. S. (2011). "
         "<i>Fundamentals of Heat and Mass Transfer</i> (7th ed.). Hoboken, NJ: John Wiley & Sons."),
        ("[8]", "Huang, M.-J., Eames, P. C., & Norton, B. (2004). Thermal regulation of building-integrated "
         "photovoltaics using phase change materials. <i>International Journal of Heat and Mass Transfer</i>, "
         "47(12–13), 2715–2733. https://doi.org/10.1016/j.ijheatmasstransfer.2003.11.011"),
        ("[9]", "Zhao, D., & Tan, G. (2014). A review of thermoelectric cooling: Materials, modeling "
         "and applications. <i>Applied Thermal Engineering</i>, 66(1–2), 15–24. "
         "https://doi.org/10.1016/j.applthermaleng.2014.01.074"),
        ("[10]", "Maxim Integrated / Analog Devices. <i>DS18B20 Programmable Resolution "
         "1-Wire Digital Thermometer — Datasheet.</i> Available at: "
         "https://www.analog.com/media/en/technical-documentation/data-sheets/DS18B20.pdf"),
        ("[11]", "Bureau of Indian Standards (BIS). IS 1660:2019 — "
         "<i>Cold Chain Equipment — Walk-in Cold Rooms and Walk-in Freezers — Specification.</i> "
         "New Delhi: BIS. (For reference — relevant standard for cold-chain equipment context.)"),
    ]

    for num, text in refs:
        story.append(Table([[Paragraph(f"<b>{num}</b>", S['table_cell']),
                             Paragraph(text, S['ref_entry'])]],
                           colWidths=[12*mm, 158*mm],
                           style=TableStyle([
                               ('VALIGN', (0,0), (-1,-1), 'TOP'),
                               ('TOPPADDING', (0,0), (-1,-1), 2),
                               ('BOTTOMPADDING', (0,0), (-1,-1), 3),
                               ('LEFTPADDING', (0,0), (-1,-1), 0),
                               ('RIGHTPADDING', (0,0), (-1,-1), 0),
                           ])))

    story.append(Spacer(1, 5*mm))
    story.append(Paragraph("18.2 Annexures Checklist", S['section_heading']))
    story.append(Paragraph(
        "The following supporting documents should be attached to the submitted report as annexures.", S['body']))
    story.append(Spacer(1, 2*mm))

    ann_rows = [
        [Paragraph("<b>Annexure</b>", S['table_header']),
         Paragraph("<b>Contents</b>", S['table_header']),
         Paragraph("<b>Status</b>", S['table_header'])],
        [Paragraph("A", S['table_cell_c']),
         Paragraph("Detailed electrical circuit diagram of the SANJIVANI control system", S['table_cell']),
         ph("[ To be attached ]")],
        [Paragraph("B", S['table_cell_c']),
         Paragraph("Full system schematic (assembly drawing with component positions)", S['table_cell']),
         ph("[ To be attached ]")],
        [Paragraph("C", S['table_cell_c']),
         Paragraph("Peltier module datasheet (manufacturer's specification)", S['table_cell']),
         ph("[ To be attached ]")],
        [Paragraph("D", S['table_cell_c']),
         Paragraph("PCM datasheet (manufacturer's or supplier's specification)", S['table_cell']),
         ph("[ To be attached ]")],
        [Paragraph("E", S['table_cell_c']),
         Paragraph("Temperature sensor datasheet", S['table_cell']),
         ph("[ To be attached ]")],
        [Paragraph("F", S['table_cell_c']),
         Paragraph("Prototype photographs (minimum four, as identified in Section 11)", S['table_cell']),
         ph("[ To be attached ]")],
        [Paragraph("G", S['table_cell_c']),
         Paragraph("Raw experimental observation sheets (all trials, both configurations)", S['table_cell']),
         ph("[ To be attached after testing ]")],
        [Paragraph("H", S['table_cell_c']),
         Paragraph("Completed engineering calculation sheets", S['table_cell']),
         ph("[ To be attached after measurements ]")],
        [Paragraph("I", S['table_cell_c']),
         Paragraph("Cost evidence (purchase receipts or quotations for components)", S['table_cell']),
         ph("[ To be attached ]")],
        [Paragraph("J", S['table_cell_c']),
         Paragraph("Microcontroller source code (control algorithm)", S['table_cell']),
         ph("[ To be attached ]")],
        [Paragraph("K", S['table_cell_c']),
         Paragraph("Any additional supporting documents or expert communications", S['table_cell']),
         ph("[ If applicable ]")],
    ]
    story.append(Table(ann_rows, colWidths=[15*mm, 110*mm, 45*mm],
                       style=TableStyle([
                           ('BACKGROUND', (0,0), (-1,0), NAVY),
                           ('ROWBACKGROUNDS', (0,1), (-1,-1), [TABLE_BG, WHITE]),
                           ('BOX', (0,0), (-1,-1), 0.5, RULE_COLOR),
                           ('INNERGRID', (0,0), (-1,-1), 0.3, RULE_COLOR),
                           ('TOPPADDING', (0,0), (-1,-1), 4), ('BOTTOMPADDING', (0,0), (-1,-1), 4),
                           ('LEFTPADDING', (0,0), (-1,-1), 5), ('RIGHTPADDING', (0,0), (-1,-1), 5),
                           ('VALIGN', (0,0), (-1,-1), 'TOP'),
                       ])))
    story.append(Spacer(1, 5*mm))
    story.append(hr(GOLD, 1.0))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(
        "SANJIVANI — संजीवनी  |  Preserving Temperature. Protecting Life.",
        ParagraphStyle('end_tag', fontName='Helvetica-BoldOblique', fontSize=11,
                       textColor=TEAL_DARK, alignment=TA_CENTER, leading=14)))
    story.append(Paragraph(
        "School UID: SBVPH-05  |  Dr. B. K. Passi Memorial Senior Bal Vigyan 2026–2027",
        ParagraphStyle('end_sch', fontName='Helvetica', fontSize=8.5,
                       textColor=SLATE, alignment=TA_CENTER, leading=12)))
    return story


# ─────────────────────────── MAIN DOCUMENT BUILDER ────────────────────

def build_document():
    from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, NextPageTemplate
    output_path = r"c:\Users\PC5\Downloads\Sanjivani\SANJIVANI_Senior_Bal_Vigyan_2026-27.pdf"

    def cover_page_template(canvas_obj, doc_obj):
        canvas_obj.saveState()
        build_cover(canvas_obj, doc_obj)
        canvas_obj.restoreState()

    def later_page_template(canvas_obj, doc_obj):
        on_later_pages(canvas_obj, doc_obj)

    cover_frame = Frame(0, 0, PAGE_W, PAGE_H, leftPadding=0, rightPadding=0,
                        topPadding=0, bottomPadding=0, id='cover_frame')
    content_frame = Frame(L_MARGIN, B_MARGIN + 8*mm,
                          PAGE_W - L_MARGIN - R_MARGIN,
                          PAGE_H - T_MARGIN - B_MARGIN - 18*mm - 8*mm,
                          id='content_frame')

    cover_tmpl = PageTemplate(id='Cover', frames=[cover_frame],
                               onPage=cover_page_template)
    content_tmpl = PageTemplate(id='Content', frames=[content_frame],
                                 onPage=later_page_template)

    doc = BaseDocTemplate(
        output_path,
        pagesize=A4,
    )
    doc.addPageTemplates([cover_tmpl, content_tmpl])

    story = []

    # Page 1: blank flowable on cover template, then switch
    story.append(Spacer(PAGE_W, PAGE_H - 1))  # fill cover page
    story.append(NextPageTemplate('Content'))
    story.append(PageBreak())

    # Pages 2-25
    page_builders = [
        page2_certificate,
        page3_declaration,
        page4_acknowledgement,
        page5_particulars,
        page6_abstract,
        page7_toc,
        page8_introduction,
        page9_problem,
        page10_aim,
        page11_pcm,
        page12_peltier,
        page13_architecture,
        page14_components,
        page15_thermal,
        page16_control,
        page17_calcs,
        page18_prototype,
        page19_methodology,
        page20_observations,
        page21_results,
        page22_economic,
        page23_safety,
        page24_conclusion,
        page25_references,
    ]

    for i, builder in enumerate(page_builders):
        content = builder(S)
        story.extend(content)
        if i < len(page_builders) - 1:
            story.append(PageBreak())

    doc.build(story)
    return output_path


if __name__ == "__main__":
    print("Building SANJIVANI report...")
    path = build_document()
    print(f"PDF generated: {path}")
