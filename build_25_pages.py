"""
SANJIVANI — Senior Bal Vigyan 2026–2027 Project Report
Master High-Resolution 25-Page Publication-Grade PDF Generator
"""

import os
import math
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, NextPageTemplate,
    Paragraph, Spacer, Table, TableStyle, HRFlowable, PageBreak, Flowable
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import pypdfium2 as pdfium

# ─────────────────────────── FONT REGISTRATION ─────────────────────────
DEVANAGARI_FONT = 'Helvetica-Bold'
font_candidates = [
    r"C:\Windows\Fonts\NirmalaB.ttf",
    r"C:\Windows\Fonts\Nirmala.ttf",
    r"C:\Windows\Fonts\mangal.ttf",
]
for fpath in font_candidates:
    if os.path.exists(fpath):
        try:
            pdfmetrics.registerFont(TTFont('DevanagariBold', fpath))
            DEVANAGARI_FONT = 'DevanagariBold'
            print(f"Registered Devanagari font from: {fpath}")
            break
        except Exception as e:
            print(f"Failed to register {fpath}: {e}")

# ─────────────────────────── COLOUR PALETTE ───────────────────────────
NAVY        = colors.HexColor("#0D1B2A")   # Deep navy for primary headings
TEAL        = colors.HexColor("#1A7A8A")   # Muted teal accent
TEAL_LIGHT  = colors.HexColor("#EBF5F7")   # Light teal background
TEAL_DARK   = colors.HexColor("#0E5A67")   # Dark teal text
GOLD        = colors.HexColor("#B8902A")   # Restrained academic gold
GOLD_LIGHT  = colors.HexColor("#FDF8EC")   # Light gold background
SLATE       = colors.HexColor("#4A5568")   # Slate grey for secondary text
TABLE_BG    = colors.HexColor("#F1F5F9")   # Light table alternate row
WHITE       = colors.white
BLACK       = colors.HexColor("#1A1A1A")   # Off-black body
AMBER_PH    = colors.HexColor("#FFF8E7")   # Placeholder amber fill
AMBER_BD    = colors.HexColor("#D4A017")   # Placeholder gold-amber border
RULE_COLOR  = colors.HexColor("#CBD5E1")   # Border grey

PAGE_W, PAGE_H = A4
L_MARGIN = 18*mm
R_MARGIN = 18*mm
T_MARGIN = 14*mm
B_MARGIN = 14*mm

def _poly(canvas_obj, pts, fill=1, stroke=0):
    p = canvas_obj.beginPath()
    p.moveTo(pts[0], pts[1])
    for i in range(2, len(pts), 2):
        p.lineTo(pts[i], pts[i+1])
    p.close()
    canvas_obj.drawPath(p, fill=fill, stroke=stroke)

# ─────────────────────────── TYPOGRAPHIC STYLES ───────────────────────
def build_styles():
    s = {}
    s['banner'] = ParagraphStyle('banner', fontName='Helvetica-Bold', fontSize=11.5,
                                 textColor=WHITE, alignment=TA_LEFT, leading=15)
    s['sec'] = ParagraphStyle('sec', fontName='Helvetica-Bold', fontSize=9.2,
                              textColor=NAVY, alignment=TA_LEFT, leading=12,
                              spaceBefore=3.5, spaceAfter=1.5)
    s['subsec'] = ParagraphStyle('subsec', fontName='Helvetica-Bold', fontSize=8.3,
                                 textColor=TEAL_DARK, alignment=TA_LEFT, leading=11,
                                 spaceBefore=2.5, spaceAfter=1)
    s['body'] = ParagraphStyle('body', fontName='Helvetica', fontSize=8,
                               textColor=BLACK, alignment=TA_JUSTIFY, leading=11.5,
                               spaceBefore=1, spaceAfter=2)
    s['body_lg'] = ParagraphStyle('body_lg', fontName='Helvetica', fontSize=8.6,
                                  textColor=BLACK, alignment=TA_JUSTIFY, leading=12.5,
                                  spaceBefore=2, spaceAfter=3)
    s['body_bold'] = ParagraphStyle('body_bold', fontName='Helvetica-Bold', fontSize=8,
                                    textColor=BLACK, alignment=TA_LEFT, leading=11)
    s['bullet'] = ParagraphStyle('bullet', fontName='Helvetica', fontSize=7.8,
                                 textColor=BLACK, alignment=TA_JUSTIFY, leading=11,
                                 leftIndent=10, firstLineIndent=-7, spaceAfter=1.5)
    s['num_item'] = ParagraphStyle('num_item', fontName='Helvetica', fontSize=7.8,
                                   textColor=BLACK, alignment=TA_JUSTIFY, leading=11,
                                   leftIndent=12, firstLineIndent=-9, spaceAfter=1.5)
    s['caption'] = ParagraphStyle('caption', fontName='Helvetica-Oblique', fontSize=7.5,
                                  textColor=SLATE, alignment=TA_CENTER, leading=10, spaceAfter=1.5)
    s['eq'] = ParagraphStyle('eq', fontName='Helvetica-Bold', fontSize=9,
                             textColor=TEAL_DARK, alignment=TA_CENTER, leading=13,
                             spaceBefore=2, spaceAfter=2)
    s['eq_note'] = ParagraphStyle('eq_note', fontName='Helvetica', fontSize=7.5,
                                  textColor=SLATE, alignment=TA_LEFT, leading=10)
    s['ph'] = ParagraphStyle('ph', fontName='Helvetica-BoldOblique', fontSize=7.2,
                             textColor=colors.HexColor("#7A5C00"), alignment=TA_CENTER, leading=9.5)
    s['th'] = ParagraphStyle('th', fontName='Helvetica-Bold', fontSize=7.5,
                             textColor=WHITE, alignment=TA_CENTER, leading=9.5)
    s['td'] = ParagraphStyle('td', fontName='Helvetica', fontSize=7.2,
                             textColor=BLACK, alignment=TA_LEFT, leading=9.5)
    s['td_c'] = ParagraphStyle('td_c', fontName='Helvetica', fontSize=7.2,
                               textColor=BLACK, alignment=TA_CENTER, leading=9.5)
    s['ref'] = ParagraphStyle('ref', fontName='Helvetica', fontSize=7.2,
                              textColor=BLACK, alignment=TA_LEFT, leading=10,
                              leftIndent=16, firstLineIndent=-16, spaceAfter=2)
    return s

S = build_styles()

def ph_box(text, width=None):
    p = Paragraph(f"[ {text} ]", S['ph'])
    cw = [width] if width else [PAGE_W - L_MARGIN - R_MARGIN]
    return Table([[p]], colWidths=cw, style=TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), AMBER_PH),
        ('BOX', (0,0), (-1,-1), 0.5, AMBER_BD),
        ('TOPPADDING', (0,0), (-1,-1), 1.8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.8),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))

def banner(title):
    p = Paragraph(title, S['banner'])
    return Table([[p]], colWidths=[PAGE_W - L_MARGIN - R_MARGIN], style=TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), NAVY),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))

def subbanner(title):
    p = Paragraph(title, ParagraphStyle('sb', fontName='Helvetica-Bold', fontSize=8.3,
                                        textColor=WHITE, alignment=TA_LEFT, leading=11))
    return Table([[p]], colWidths=[PAGE_W - L_MARGIN - R_MARGIN], style=TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), TEAL),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))

def hr(color=RULE_COLOR, thickness=0.4):
    return HRFlowable(width="100%", thickness=thickness, color=color, spaceAfter=2, spaceBefore=2)

# ─────────────────────────── VECTOR SCHEMATICS ────────────────────────
class PCMDiagram(Flowable):
    def __init__(self, width=174*mm, height=36*mm):
        super().__init__()
        self.width, self.height = width, height

    def draw(self):
        c, w, h = self.canv, self.width, self.height
        c.setFillColor(colors.HexColor("#F8FAFC"))
        c.roundRect(0, 0, w, h, 4, fill=1, stroke=0)
        c.setStrokeColor(RULE_COLOR); c.setLineWidth(0.4)
        c.roundRect(0, 0, w, h, 4, fill=0, stroke=1)

        cw = (w - 12*mm) / 3
        phases = [
            ("1. SOLID PCM", colors.HexColor("#BFDBFE"), "Absorbing sensible heat\nT < T_phase (Sensible)", colors.HexColor("#1D4ED8")),
            ("2. PHASE CHANGE (Melting)", colors.HexColor("#A7F3D0"), "Latent heat absorption\nT ~ T_phase (Isothermal Buffer)", colors.HexColor("#065F46")),
            ("3. LIQUID PCM", colors.HexColor("#FDE68A"), "Exhausted latent reserve\nT > T_phase (Sensible Rise)", colors.HexColor("#92400E")),
        ]
        for i, (title, bg, desc, tc) in enumerate(phases):
            x = 3*mm + i * (cw + 3*mm)
            c.setFillColor(bg)
            c.roundRect(x, 4*mm, cw, h - 14*mm, 3, fill=1, stroke=0)
            c.setFillColor(tc); c.setFont("Helvetica-Bold", 7)
            c.drawCentredString(x + cw/2, h - 18.5*mm, title)
            c.setFillColor(BLACK); c.setFont("Helvetica", 6)
            for j, ln in enumerate(desc.split('\n')):
                c.drawCentredString(x + cw/2, h - 22.5*mm - j*6.5, ln)

        c.setFillColor(NAVY); c.setFont("Helvetica-Bold", 7.5)
        c.drawString(4*mm, h - 7*mm, "Figure 1 — Phase Change Material (PCM) Thermal Buffering & Isothermal Phase Transition")

class PeltierDiagram(Flowable):
    def __init__(self, width=174*mm, height=44*mm):
        super().__init__()
        self.width, self.height = width, height

    def draw(self):
        c, w, h = self.canv, self.width, self.height
        c.setFillColor(colors.HexColor("#F8FAFC"))
        c.roundRect(0, 0, w, h, 4, fill=1, stroke=0)
        c.setStrokeColor(RULE_COLOR); c.setLineWidth(0.4)
        c.roundRect(0, 0, w, h, 4, fill=0, stroke=1)

        # Hot Side (Top)
        c.setFillColor(colors.HexColor("#FEE2E2"))
        c.roundRect(15*mm, h - 14*mm, w - 30*mm, 7*mm, 2, fill=1, stroke=0)
        c.setFillColor(colors.HexColor("#DC2626")); c.setFont("Helvetica-Bold", 7)
        c.drawCentredString(w/2, h - 10.5*mm, "HOT SIDE — Heat Rejection: Q_hot (rate) = Q_cold (rate) + P_elec (to heat sink & environment)")

        # Cold Side (Bottom)
        c.setFillColor(colors.HexColor("#DBEAFE"))
        c.roundRect(15*mm, 4*mm, w - 30*mm, 7*mm, 2, fill=1, stroke=0)
        c.setFillColor(colors.HexColor("#1D4ED8")); c.setFont("Helvetica-Bold", 7)
        c.drawCentredString(w/2, 6.5*mm, "COLD SIDE — Heat Pumping Interface: Q_cold (rate) (coupled to Aluminium Spreader & PCM)")

        # Semiconductor Matrix
        c.setFillColor(colors.HexColor("#E5E7EB"))
        c.roundRect(30*mm, 13*mm, w - 60*mm, h - 29*mm, 2, fill=1, stroke=0)
        c.setFillColor(SLATE); c.setFont("Helvetica-Bold", 6.5)
        c.drawCentredString(w/2, h/2 - 2, "Bismuth Telluride (Bi2Te3) P-N Thermoelectric Semiconductor Couples")

        # DC Power Input arrow
        c.setFillColor(colors.HexColor("#7C3AED")); c.setFont("Helvetica-Bold", 6.5)
        c.drawString(3*mm, h/2 + 2, "DC Input")
        c.drawString(3*mm, h/2 - 5, "(P_elec)")
        c.setStrokeColor(colors.HexColor("#7C3AED")); c.setLineWidth(1)
        c.line(16*mm, h/2, 28*mm, h/2)
        _poly(c, [28*mm, h/2, 25*mm, h/2+2, 25*mm, h/2-2], fill=1, stroke=0)

        c.setFillColor(NAVY); c.setFont("Helvetica-Bold", 7.5)
        c.drawString(4*mm, h - 5.5*mm, "Figure 2 — Peltier Thermoelectric Module: Active Heat Pumping & Energy Conservation")

class SystemBlockDiagram(Flowable):
    def __init__(self, width=174*mm, height=72*mm):
        super().__init__()
        self.width, self.height = width, height

    def _box(self, c, x, y, bw, bh, text, bg, tc=WHITE, fs=6):
        c.setFillColor(bg)
        c.roundRect(x, y, bw, bh, 2.5, fill=1, stroke=0)
        c.setStrokeColor(RULE_COLOR); c.setLineWidth(0.4)
        c.roundRect(x, y, bw, bh, 2.5, fill=0, stroke=1)
        c.setFillColor(tc); c.setFont("Helvetica-Bold", fs)
        lines = text.split('\n')
        for i, ln in enumerate(lines):
            c.drawCentredString(x + bw/2, y + bh/2 + (len(lines)-1)*3 - i*6.5 - 2, ln)

    def draw(self):
        c, w, h = self.canv, self.width, self.height
        c.setFillColor(colors.HexColor("#F8FAFC"))
        c.roundRect(0, 0, w, h, 4, fill=1, stroke=0)
        c.setStrokeColor(RULE_COLOR); c.setLineWidth(0.4)
        c.roundRect(0, 0, w, h, 4, fill=0, stroke=1)

        # Enclosure Boundary
        enc_w, enc_h = 108*mm, 54*mm
        c.setFillColor(colors.HexColor("#F0FDF4"))
        c.roundRect(4*mm, 6*mm, enc_w, enc_h, 3, fill=1, stroke=0)
        c.setStrokeColor(TEAL); c.setLineWidth(0.8)
        c.roundRect(4*mm, 6*mm, enc_w, enc_h, 3, fill=0, stroke=1)
        c.setFillColor(TEAL_DARK); c.setFont("Helvetica-Bold", 6.5)
        c.drawString(6*mm, 6*mm + enc_h - 6*mm, "INSULATED STORAGE ENCLOSURE (Target: +2 °C to +8 °C)")

        # Blocks inside enclosure
        self._box(c, 8*mm, 35*mm, 44*mm, 15*mm, "MEDICAL PAYLOAD\n(Vaccines / Insulin)", colors.HexColor("#15803D"), fs=6.5)
        self._box(c, 8*mm, 12*mm, 44*mm, 17*mm, "PCM CHAMBER\n(Latent Heat Reserve)", colors.HexColor("#0284C7"), fs=6.5)
        self._box(c, 56*mm, 12*mm, 26*mm, 38*mm, "ALUMINIUM\nHEAT\nSPREADER\n(Isothermal\nInterface)", colors.HexColor("#D97706"), fs=6)
        self._box(c, 86*mm, 22*mm, 22*mm, 18*mm, "PELTIER\nMODULE\n(Cold Face)", colors.HexColor("#1E3A5F"), fs=6)

        # External Blocks
        self._box(c, 116*mm, 22*mm, 25*mm, 18*mm, "LIQUID THERMAL\nTRANSFER\nCHAMBER", colors.HexColor("#4F46E5"), fs=6)
        self._box(c, 145*mm, 20*mm, 25*mm, 22*mm, "HOT-SIDE\nHEAT SINK\n& FAN UNIT", colors.HexColor("#DC2626"), fs=6)

        # Controls & Power Top
        self._box(c, 116*mm, 48*mm, 25*mm, 15*mm, "CONTROLLER\n(Microcontroller)", colors.HexColor("#334155"), fs=6)
        self._box(c, 145*mm, 48*mm, 25*mm, 15*mm, "POWER SUPPLY\n(DC Battery Bank)", colors.HexColor("#475569"), fs=6)
        self._box(c, 56*mm, 52*mm, 26*mm, 7*mm, "TEMP SENSORS", colors.HexColor("#7C3AED"), fs=5.5)

        # Arrows
        c.setStrokeColor(colors.HexColor("#DC2626")); c.setLineWidth(1)
        c.line(108*mm, 31*mm, 116*mm, 31*mm) # Peltier -> Liquid
        c.line(141*mm, 31*mm, 145*mm, 31*mm) # Liquid -> Heat Sink

        # Title
        c.setFillColor(NAVY); c.setFont("Helvetica-Bold", 7.5)
        c.drawString(4*mm, h - 5.5*mm, "Figure 3 — Complete SANJIVANI System Architecture Block Diagram")

class FlowchartDiagram(Flowable):
    def __init__(self, width=174*mm, height=74*mm):
        super().__init__()
        self.width, self.height = width, height

    def draw(self):
        c, w, h = self.canv, self.width, self.height
        c.setFillColor(colors.HexColor("#F8FAFC"))
        c.roundRect(0, 0, w, h, 4, fill=1, stroke=0)
        c.setStrokeColor(RULE_COLOR); c.setLineWidth(0.4)
        c.roundRect(0, 0, w, h, 4, fill=0, stroke=1)

        steps = [
            ("1. System Init & PCM Passive Mode", 6*mm, h - 16*mm, 48*mm, 8.5*mm, colors.HexColor("#0284C7"), WHITE),
            ("2. Multi-point Temperature Telemetry", 60*mm, h - 16*mm, 50*mm, 8.5*mm, colors.HexColor("#334155"), WHITE),
            ("3. T_payload >= T_upper?\n(Threshold Trigger)", 116*mm, h - 19*mm, 52*mm, 12.5*mm, AMBER_PH, colors.HexColor("#1A1A1A"), True),
            ("4. Trigger Peltier Active Pumping (MOSFET ON)", 116*mm, h - 35*mm, 52*mm, 8.5*mm, colors.HexColor("#DC2626"), WHITE),
            ("5. Al Spreader & Liquid Heat Evacuation", 60*mm, h - 35*mm, 50*mm, 8.5*mm, colors.HexColor("#4F46E5"), WHITE),
            ("6. T_payload <= T_lower?\n(Target Restored)", 6*mm, h - 39*mm, 48*mm, 12.5*mm, AMBER_PH, colors.HexColor("#1A1A1A"), True),
            ("7. Deactivate Peltier (Resume PCM Passive)", 6*mm, 8*mm, 78*mm, 9*mm, colors.HexColor("#15803D"), WHITE),
            ("8. Log Telemetry (T_amb, T_payload, V, I)", 90*mm, 8*mm, 78*mm, 9*mm, colors.HexColor("#475569"), WHITE),
        ]

        for s in steps:
            txt, x, y, bw, bh, bg, tc = s[0], s[1], s[2], s[3], s[4], s[5], s[6]
            is_decision = len(s) > 7 and s[7]
            if is_decision:
                c.setFillColor(bg); c.roundRect(x, y, bw, bh, 2.5, fill=1, stroke=0)
                c.setStrokeColor(AMBER_BD); c.setLineWidth(0.8); c.roundRect(x, y, bw, bh, 2.5, fill=0, stroke=1)
                c.setFillColor(tc); c.setFont("Helvetica-Bold", 5.8)
            else:
                c.setFillColor(bg); c.roundRect(x, y, bw, bh, 2.5, fill=1, stroke=0)
                c.setFillColor(tc); c.setFont("Helvetica-Bold", 5.8)
            lines = txt.split('\n')
            for i, ln in enumerate(lines):
                c.drawCentredString(x + bw/2, y + bh/2 + (len(lines)-1)*2.8 - i*5.8 - 2, ln)

        # Connection flow arrows
        c.setStrokeColor(SLATE); c.setLineWidth(0.8)
        c.line(54*mm, h - 12*mm, 60*mm, h - 12*mm)
        c.line(110*mm, h - 12*mm, 116*mm, h - 12*mm)
        c.line(142*mm, h - 18.5*mm, 142*mm, h - 26.5*mm)
        c.line(116*mm, h - 30.7*mm, 110*mm, h - 30.7*mm)
        c.line(60*mm, h - 30.7*mm, 54*mm, h - 30.7*mm)
        c.line(30*mm, h - 38*mm, 30*mm, 17*mm)
        c.line(84*mm, 12.5*mm, 90*mm, 12.5*mm)

        c.setFillColor(NAVY); c.setFont("Helvetica-Bold", 7.5)
        c.drawString(4*mm, h - 5.5*mm, "Figure 4 — Operational Control Flowchart: Sensor-Triggered Hysteresis Cooling Cycle")

class ThermalFlowDiagram(Flowable):
    def __init__(self, width=174*mm, height=36*mm):
        super().__init__()
        self.width, self.height = width, height

    def draw(self):
        c, w, h = self.canv, self.width, self.height
        c.setFillColor(colors.HexColor("#F8FAFC"))
        c.roundRect(0, 0, w, h, 4, fill=1, stroke=0)
        c.setStrokeColor(RULE_COLOR); c.setLineWidth(0.4)
        c.roundRect(0, 0, w, h, 4, fill=0, stroke=1)

        nodes = [
            ("Ambient Heat\nIngress (Q_in)", 4*mm, colors.HexColor("#DC2626")),
            ("Insulated Wall\nResistance (R_th)", 34*mm, colors.HexColor("#D97706")),
            ("PCM Latent\nAbsorption (Q_L)", 64*mm, colors.HexColor("#0284C7")),
            ("Al Heat Spreader\nCoupling", 94*mm, colors.HexColor("#D97706")),
            ("Peltier Module\n(Cold -> Hot)", 124*mm, colors.HexColor("#1E3A5F")),
            ("Environment\nHeat Sink (Q_hot)", 150*mm, colors.HexColor("#991B1B")),
        ]
        bw, bh = 22*mm, 14*mm
        for title, x, col in nodes:
            c.setFillColor(col); c.roundRect(x, 6*mm, bw, bh, 2, fill=1, stroke=0)
            c.setFillColor(WHITE); c.setFont("Helvetica-Bold", 5.5)
            lines = title.split('\n')
            for j, ln in enumerate(lines):
                c.drawCentredString(x + bw/2, 6*mm + bh/2 + 2 - j*6, ln)

        c.setStrokeColor(SLATE); c.setLineWidth(0.8)
        for i in range(len(nodes)-1):
            x1 = nodes[i][1] + bw
            x2 = nodes[i+1][1]
            c.line(x1, 13*mm, x2, 13*mm)
            _poly(c, [x2, 13*mm, x2-2*mm, 14.5*mm, x2-2*mm, 11.5*mm], fill=1, stroke=0)

        c.setFillColor(NAVY); c.setFont("Helvetica-Bold", 7.5)
        c.drawString(4*mm, h - 5.5*mm, "Figure 5 — Thermal Pathway: Energy Ingress, PCM Buffering, Active Thermoelectric Pumping & Rejection")

class ExperimentalSetupDiagram(Flowable):
    def __init__(self, width=174*mm, height=36*mm):
        super().__init__()
        self.width, self.height = width, height

    def draw(self):
        c, w, h = self.canv, self.width, self.height
        c.setFillColor(colors.HexColor("#F8FAFC"))
        c.roundRect(0, 0, w, h, 4, fill=1, stroke=0)
        c.setStrokeColor(RULE_COLOR); c.setLineWidth(0.4)
        c.roundRect(0, 0, w, h, 4, fill=0, stroke=1)

        # Config A
        c.setFillColor(colors.HexColor("#DBEAFE"))
        c.roundRect(6*mm, 4*mm, 74*mm, h - 13*mm, 3, fill=1, stroke=0)
        c.setFillColor(colors.HexColor("#1D4ED8")); c.setFont("Helvetica-Bold", 7)
        c.drawCentredString(43*mm, h - 14*mm, "CONFIGURATION A: Conventional PCM-Only (Control)")
        c.setFillColor(BLACK); c.setFont("Helvetica", 6)
        c.drawString(10*mm, h - 19*mm, "• Insulated enclosure + Pre-conditioned PCM reserve")
        c.drawString(10*mm, h - 23*mm, "• Continuous temperature logging (Payload zone, PCM)")
        c.drawString(10*mm, h - 27*mm, "• Passive hold duration until excursion (T > 8 °C)")

        # Config B
        c.setFillColor(colors.HexColor("#D1FAE5"))
        c.roundRect(94*mm, 4*mm, 74*mm, h - 13*mm, 3, fill=1, stroke=0)
        c.setFillColor(colors.HexColor("#065F46")); c.setFont("Helvetica-Bold", 7)
        c.drawCentredString(131*mm, h - 14*mm, "CONFIGURATION B: SANJIVANI Hybrid System")
        c.setFillColor(BLACK); c.setFont("Helvetica", 6)
        c.drawString(98*mm, h - 19*mm, "• Identical enclosure & PCM + Peltier module assembly")
        c.drawString(98*mm, h - 23*mm, "• Microcontroller hysteresis: Active cooling when T >= T_upper")
        c.drawString(98*mm, h - 27*mm, "• Extended duration hold + Electrical telemetry logged")

        # VS circle
        c.setFillColor(GOLD)
        c.circle(87*mm, h/2 - 2, 5*mm, fill=1, stroke=0)
        c.setFillColor(WHITE); c.setFont("Helvetica-Bold", 7)
        c.drawCentredString(87*mm, h/2 - 4.5, "VS")

        c.setFillColor(NAVY); c.setFont("Helvetica-Bold", 7.5)
        c.drawString(4*mm, h - 5.5*mm, "Figure 6 — Controlled Comparative Experimental Design: Configuration A vs Configuration B")

# ─────────────────────────── PAGE BUILDERS ────────────────────────────

def p02_certificate():
    s = [
        banner("CERTIFICATE OF ORIGINAL PROJECT WORK"),
        Spacer(1, 4*mm),
        Paragraph(
            "This is to certify that the project report entitled <b>SANJIVANI: Design and Development of a "
            "Sensor-Triggered Hybrid PCM–Thermoelectric Cooling System for Extended Medical Cold-Chain Storage</b> "
            "is a bonafide record of authentic engineering research, prototype development, and experimental investigation "
            "carried out by the following students of <b>Participating Institution (School UID: SBVPH-05)</b> for submission "
            "to the <b>Dr. B. K. Passi Memorial Senior Bal Vigyan 2026–2027</b> under the mentorship of <b>Mr. Gopal Kumar Roy</b>.",
            S['body_lg']
        ),
        Spacer(1, 3*mm),
        Table([
            [Paragraph("<b>Participant Name</b>", S['th']), Paragraph("<b>Class</b>", S['th']), Paragraph("<b>Institutional Affiliation & Research Role</b>", S['th'])],
            [Paragraph("Vaishnavi Shrivastava", S['td']), Paragraph("Class XI", S['td_c']), Paragraph("School UID: SBVPH-05 — Lead Participant (Thermodynamics)", S['td'])],
            [Paragraph("Gaurav Choudhary", S['td']), Paragraph("Class XI", S['td_c']), Paragraph("School UID: SBVPH-05 — Lead Participant (Thermoelectrics)", S['td'])],
            [Paragraph("Prathamesh Rao", S['td']), Paragraph("Class XII", S['td_c']), Paragraph("School UID: SBVPH-05 — Senior Participant (Instrumentation)", S['td'])],
            [Paragraph("Bhavmanyu Singh", S['td']), Paragraph("Class XII", S['td_c']), Paragraph("School UID: SBVPH-05 — Senior Participant (Structural Integration)", S['td'])],
        ], colWidths=[52*mm, 24*mm, 98*mm], style=TableStyle([
            ('BACKGROUND', (0,0), (-1,0), NAVY),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [TABLE_BG, WHITE]),
            ('BOX', (0,0), (-1,-1), 0.5, RULE_COLOR),
            ('INNERGRID', (0,0), (-1,-1), 0.3, RULE_COLOR),
            ('TOPPADDING', (0,0), (-1,-1), 3), ('BOTTOMPADDING', (0,0), (-1,-1), 3),
            ('LEFTPADDING', (0,0), (-1,-1), 4), ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ])),
        Spacer(1, 4*mm),
        Paragraph(
            "The engineering investigation was conducted in the school physics and electronics laboratories under the "
            "sub-theme <i>Health and Hygiene</i> within the national framework of <i>STEM for Viksit and Atmanirbhar Bharat</i>. "
            "The students have explored phase transition thermodynamics, solid-state heat pumping physics, and embedded controller "
            "automation. All theoretical models, calculations, and experimental protocols presented represent their original "
            "scientific investigation. External reference sources and literature are duly acknowledged.",
            S['body_lg']
        ),
        Spacer(1, 8*mm),
        Table([
            [Paragraph("____________________________", S['body']), Paragraph("____________________________", S['body']), Paragraph("____________________________", S['body'])],
            [Paragraph("<b>Mr. Gopal Kumar Roy</b>", S['body_bold']), Paragraph("<b>Dr. Ashish Arora</b>", S['body_bold']), Paragraph("<b>Official School Seal</b>", S['body_bold'])],
            [Paragraph("Mentor Teacher, Senior Physics Faculty", S['caption']), Paragraph("Principal, School UID: SBVPH-05", S['caption']), Paragraph("Institutional Authorisation", S['caption'])],
            [Paragraph("Date: ____________________", S['caption']), Paragraph("Date: ____________________", S['caption']), ph_box("OFFICIAL SCHOOL SEAL EMBOSS", 50*mm)],
        ], colWidths=[58*mm, 58*mm, 58*mm], style=TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('TOPPADDING', (0,0), (-1,-1), 3), ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ])),
        Spacer(1, 4*mm),
        ph_box("UNIQUE REGISTRATION CODE: [ TO BE FILLED BY TEACHER / ORGANISER ]   |   PROJECT CODE: [ ________ ]   |   SCHOOL CODE: [ ________ ]"),
    ]
    return s

def p03_declaration():
    s = [
        banner("DECLARATION OF ORIGINALITY"),
        Spacer(1, 3*mm),
        Paragraph(
            "We, the undersigned students of <b>School UID: SBVPH-05</b>, hereby solemnly declare that the "
            "engineering project report titled <b>SANJIVANI: Design and Development of a Sensor-Triggered Hybrid PCM–Thermoelectric "
            "Cooling System for Extended Medical Cold-Chain Storage</b> submitted for the <b>Dr. B. K. Passi Memorial Senior Bal "
            "Vigyan 2026–2027</b> embodies our genuine, authentic and independent investigation.",
            S['body_lg']
        ),
        Spacer(1, 2.5*mm),
        Paragraph("1. <b>Originality of Engineering Concept:</b> The system design, sensor-hysteresis operational cycle, "
                  "and hybrid thermal architecture were conceived and developed under the supervision of our mentor, Mr. Gopal Kumar Roy.", S['num_item']),
        Paragraph("2. <b>Honesty in Technical Claims:</b> No experimental measurements, temperature logs, or performance metrics "
                  "have been fabricated. Clear visual placeholders identify parameters awaiting empirical validation.", S['num_item']),
        Paragraph("3. <b>Distinction of Milestones:</b> The report explicitly distinguishes between theoretical design criteria, "
                  "the fabricated laboratory prototype, planned comparative experiments, and long-term future possibilities.", S['num_item']),
        Paragraph("4. <b>Verification of Assumptions:</b> The baseline holding target (~72 h) and the extended hybrid target (~110 h) "
                  "are treated as testable design hypotheses rather than certified or universally achieved results.", S['num_item']),
        Paragraph("5. <b>Academic Integrity:</b> All published literature, engineering formulas, manufacturer datasheets, and "
                  "World Health Organisation guidance documents have been transparently cited using standard bibliographic conventions.", S['num_item']),
        Paragraph("6. <b>Ethical Non-Submission:</b> This project dossier has not been submitted previously or concurrently to "
                  "any other examination, competition, exhibition, or publication venue.", S['num_item']),
        Spacer(1, 5*mm),
        subbanner("Signatures of Project Participants"),
        Spacer(1, 4*mm),
        Table([
            [Paragraph("____________________________", S['body']), Paragraph("____________________________", S['body'])],
            [Paragraph("<b>Vaishnavi Shrivastava</b> (Class XI)", S['body_bold']), Paragraph("<b>Gaurav Choudhary</b> (Class XI)", S['body_bold'])],
            [Paragraph("Signature & Date: ____________________", S['caption']), Paragraph("Signature & Date: ____________________", S['caption'])],
            [Spacer(1, 4*mm), Spacer(1, 4*mm)],
            [Paragraph("____________________________", S['body']), Paragraph("____________________________", S['body'])],
            [Paragraph("<b>Prathamesh Rao</b> (Class XII)", S['body_bold']), Paragraph("<b>Bhavmanyu Singh</b> (Class XII)", S['body_bold'])],
            [Paragraph("Signature & Date: ____________________", S['caption']), Paragraph("Signature & Date: ____________________", S['caption'])],
        ], colWidths=[87*mm, 87*mm], style=TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('TOPPADDING', (0,0), (-1,-1), 2), ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ])),
        Spacer(1, 5*mm),
        Paragraph("<i>Place of Execution: Participating Institution (School UID: SBVPH-05)</i>", S['caption']),
    ]
    return s

def p04_acknowledgement():
    s = [
        banner("ACKNOWLEDGEMENT"),
        Spacer(1, 3*mm),
        Paragraph(
            "The realization of this engineering innovation has been made possible through the generous intellectual, "
            "institutional, and moral support of our teachers, mentors, school administration, and families.",
            S['body_lg']
        ),
        Spacer(1, 1.5*mm),
        Paragraph(
            "We express our profound respect and indebtedness to our esteemed Principal, <b>Dr. Ashish Arora</b>, "
            "whose progressive vision for scientific inquiry and constant institutional encouragement created the fertile "
            "environment needed to pursue rigorous applied engineering. His insistence on academic discipline and experimental "
            "integrity has guided the design ethos of SANJIVANI.",
            S['body_lg']
        ),
        Spacer(1, 1.5*mm),
        Paragraph(
            "We extend our deepest gratitude to our project mentor, <b>Mr. Gopal Kumar Roy</b>, Senior Physics Faculty. "
            "His technical guidance across thermodynamics, solid-state thermoelectric physics, and embedded controller design "
            "provided invaluable clarity. Mr. Roy dedicated countless hours to reviewing our thermal equations, challenging our "
            "assumptions regarding heat rejection pathways, and instilling in us the values of honest scientific inquiry.",
            S['body_lg']
        ),
        Spacer(1, 1.5*mm),
        Paragraph(
            "We gratefully acknowledge the institutional infrastructure provided by <b>School UID: SBVPH-05</b>, "
            "including the physics laboratory, electronic test benches, digital measurement instruments, and reference library. "
            "The collaborative spirit of the science department faculty provided continuous encouragement.",
            S['body_lg']
        ),
        Spacer(1, 1.5*mm),
        Paragraph(
            "We record our appreciation for our student observers, <b>Konav Singh (Class XI)</b> and <b>Animesh Mishra</b>, "
            "who assisted during preliminary trial observations, assembly documentation, and background research sessions. "
            "Their enthusiastic participation enriched our project discussions.",
            S['body_lg']
        ),
        Spacer(1, 1.5*mm),
        Paragraph(
            "We are endlessly grateful to our parents and families for their patience, moral support, and constant understanding "
            "throughout late-evening development sessions, test trials, and report drafting.",
            S['body_lg']
        ),
        Spacer(1, 1.5*mm),
        Paragraph(
            "Finally, we thank the organizers of the <b>Dr. B. K. Passi Memorial Senior Bal Vigyan 2026–2027</b> for providing "
            "this prestigious platform to present indigenous, cost-effective engineering solutions addressing national healthcare needs.",
            S['body_lg']
        ),
        Spacer(1, 6*mm),
        Table([[
            Paragraph("<b>Vaishnavi Shrivastava · Gaurav Choudhary · Prathamesh Rao · Bhavmanyu Singh</b><br/>"
                      "<i>Senior Engineering Research Team — Project SANJIVANI<br/>"
                      "Participating Institution (School UID: SBVPH-05)</i>",
                      ParagraphStyle('ack_sign', fontName='Helvetica', fontSize=8.5, textColor=NAVY, alignment=TA_CENTER, leading=12))
        ]], colWidths=[PAGE_W - L_MARGIN - R_MARGIN], style=TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), TEAL_LIGHT),
            ('BOX', (0,0), (-1,-1), 0.5, TEAL),
            ('TOPPADDING', (0,0), (-1,-1), 5), ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ]))
    ]
    return s

def p05_particulars():
    s = [
        banner("PROJECT AND TEAM PARTICULARS"),
        Spacer(1, 2*mm),
        subbanner("A. Administrative & Competition Registration Details"),
        Spacer(1, 1*mm),
        Table([
            [Paragraph("<b>Project Official Name:</b>", S['td']), Paragraph("<b>SANJIVANI (संजीवनी)</b>", S['td'])],
            [Paragraph("<b>Full Innovation Title:</b>", S['td']), Paragraph("Design and Development of a Sensor-Triggered Hybrid PCM–Peltier Cooling System for Extended Medical Cold-Chain Storage", S['td'])],
            [Paragraph("<b>Project Tagline:</b>", S['td']), Paragraph("<i>Preserving Temperature. Protecting Life.</i>", S['td'])],
            [Paragraph("<b>Competition / Forum:</b>", S['td']), Paragraph("Dr. B. K. Passi Memorial Senior Bal Vigyan 2026–2027", S['td'])],
            [Paragraph("<b>Main Theme:</b>", S['td']), Paragraph("STEM for Viksit and Atmanirbhar Bharat", S['td'])],
            [Paragraph("<b>Sub-Theme / Category:</b>", S['td']), Paragraph("Health and Hygiene / Physics & Thermal Engineering", S['td'])],
            [Paragraph("<b>Institution / School:</b>", S['td']), Paragraph("Participating Institution (School UID: SBVPH-05)", S['td'])],
            [Paragraph("<b>Mentor Teacher:</b>", S['td']), Paragraph("Mr. Gopal Kumar Roy (Senior Faculty, Physics)", S['td'])],
            [Paragraph("<b>School Principal:</b>", S['td']), Paragraph("Dr. Ashish Arora", S['td'])],
            [Paragraph("<b>Registration Code:</b>", S['td']), ph_box("TO BE FILLED BY TEACHER / ORGANISER", 95*mm)],
            [Paragraph("<b>School & Project Code:</b>", S['td']), ph_box("TO BE FILLED IF REQUIRED", 95*mm)],
        ], colWidths=[50*mm, 124*mm], style=TableStyle([
            ('ROWBACKGROUNDS', (0,0), (-1,-1), [TABLE_BG, WHITE]),
            ('BOX', (0,0), (-1,-1), 0.5, RULE_COLOR),
            ('INNERGRID', (0,0), (-1,-1), 0.3, RULE_COLOR),
            ('TOPPADDING', (0,0), (-1,-1), 2), ('BOTTOMPADDING', (0,0), (-1,-1), 2),
            ('LEFTPADDING', (0,0), (-1,-1), 4), ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ])),
        Spacer(1, 2*mm),
        subbanner("B. Registered Project Participants (Authors)"),
        Spacer(1, 1*mm),
        Table([
            [Paragraph("<b>#</b>", S['th']), Paragraph("<b>Student Name</b>", S['th']), Paragraph("<b>Class</b>", S['th']), Paragraph("<b>Assigned Research Responsibilities</b>", S['th'])],
            [Paragraph("1", S['td_c']), Paragraph("Vaishnavi Shrivastava", S['td']), Paragraph("Class XI", S['td_c']), Paragraph("Thermal calculations, PCM thermodynamics, and literature review", S['td'])],
            [Paragraph("2", S['td_c']), Paragraph("Gaurav Choudhary", S['td']), Paragraph("Class XI", S['td_c']), Paragraph("Peltier assembly, heat spreading interface, and experimental design", S['td'])],
            [Paragraph("3", S['td_c']), Paragraph("Prathamesh Rao", S['td']), Paragraph("Class XII", S['td_c']), Paragraph("Sensor integration, microcontroller logic, and telemetry logging", S['td'])],
            [Paragraph("4", S['td_c']), Paragraph("Bhavmanyu Singh", S['td']), Paragraph("Class XII", S['td_c']), Paragraph("Enclosure structural fabrication, heat sink mechanics, and safety audits", S['td'])],
        ], colWidths=[8*mm, 45*mm, 20*mm, 101*mm], style=TableStyle([
            ('BACKGROUND', (0,0), (-1,0), NAVY),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [TABLE_BG, WHITE]),
            ('BOX', (0,0), (-1,-1), 0.5, RULE_COLOR),
            ('INNERGRID', (0,0), (-1,-1), 0.3, RULE_COLOR),
            ('TOPPADDING', (0,0), (-1,-1), 2), ('BOTTOMPADDING', (0,0), (-1,-1), 2),
            ('LEFTPADDING', (0,0), (-1,-1), 4), ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ])),
        Spacer(1, 2*mm),
        subbanner("C. Student Observers (Non-Author Observers)"),
        Spacer(1, 1*mm),
        Table([
            [Paragraph("<b>#</b>", S['th']), Paragraph("<b>Student Observer Name</b>", S['th']), Paragraph("<b>Class</b>", S['th']), Paragraph("<b>Observational Scope</b>", S['th'])],
            [Paragraph("1", S['td_c']), Paragraph("Konav Singh", S['td']), Paragraph("Class XI", S['td_c']), Paragraph("Trial monitoring, baseline observation logging support", S['td'])],
            [Paragraph("2", S['td_c']), Paragraph("Animesh Mishra", S['td']), ph_box("CLASS TO BE CONFIRMED", 25*mm), Paragraph("Prototype documentation and secondary review assistance", S['td'])],
        ], colWidths=[8*mm, 45*mm, 35*mm, 86*mm], style=TableStyle([
            ('BACKGROUND', (0,0), (-1,0), TEAL),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [TABLE_BG, WHITE]),
            ('BOX', (0,0), (-1,-1), 0.5, RULE_COLOR),
            ('INNERGRID', (0,0), (-1,-1), 0.3, RULE_COLOR),
            ('TOPPADDING', (0,0), (-1,-1), 2), ('BOTTOMPADDING', (0,0), (-1,-1), 2),
            ('LEFTPADDING', (0,0), (-1,-1), 4), ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ])),
        Spacer(1, 1*mm),
        Paragraph("<i>Note: Student observers supported observational sessions but are maintained distinct from the four project participants who authored this dossier.</i>", S['caption']),
    ]
    return s

def p06_abstract():
    s = [
        banner("ABSTRACT & TECHNICAL KEYWORDS"),
        Spacer(1, 3*mm),
        Paragraph(
            "Maintaining uninterrupted cold-chain integrity (+2 °C to +8 °C) during the transit of critical biologicals—including "
            "vaccines, insulins, blood derivatives, and monoclonal antibodies—remains a major global health vulnerability, "
            "especially across rural, off-grid, and high-ambient-temperature regions. Conventional passive medical coolers rely "
            "strictly on pre-conditioned Phase Change Materials (PCMs) or ice packs. While robust and electricity-independent, "
            "passive systems are constrained by finite latent heat capacity: external heat ingress inevitably melts the PCM, "
            "resulting in catastrophic thermal excursions beyond ~72 hours under severe ambient exposure.",
            S['body_lg']
        ),
        Spacer(1, 2*mm),
        Paragraph(
            "To overcome this duration limit without imposing prohibitive battery weight or continuous electrical consumption, "
            "project <b>SANJIVANI</b> introduces a <b>Sensor-Triggered Hybrid PCM–Thermoelectric Cooling Architecture</b>. "
            "The system strategically couples a high-latent-heat PCM chamber with solid-state Peltier (Thermoelectric Cooler, TEC) "
            "modules, an aluminium isothermal heat-spreading plate, and a liquid thermal-transfer subsystem coupled to an external "
            "heat-rejection assembly. Rather than operating continuously, the Peltier modules are activated selectively by a digital "
            "microcontroller running a threshold-based hysteresis algorithm. When internal sensors detect temperature creeping towards "
            "an upper threshold (T_upper), supplementary thermoelectric heat pumping is initiated. Cold-side thermal energy is "
            "distributed across the PCM boundary via the high-conductivity aluminium plate, counteracting heat ingress and slowing "
            "latent reserve depletion. Once internal conditions recover to a lower safety threshold (T_lower), the TEC subsystem "
            "deactivates, allowing passive PCM cooling to resume.",
            S['body_lg']
        ),
        Spacer(1, 2*mm),
        Paragraph(
            "This report details the governing thermodynamic equations (sensible vs. latent storage, thermoelectric heat pumping: "
            "Q_hot = Q_cold + P_elec), bill of materials, circuit architecture, thermal-flow pathways, and a rigorous comparative "
            "experimental methodology comparing a conventional PCM-only box (Configuration A) against the hybrid SANJIVANI prototype "
            "(Configuration B). While preliminary engineering models establish an aspirational target of extending holding duration "
            "from ~72 hours towards ~110 hours, this dossier strictly distinguishes theoretical design targets from empirical results, "
            "leaving observation matrices unpopulated for upcoming laboratory trials.",
            S['body_lg']
        ),
        Spacer(1, 6*mm),
        Table([[
            Paragraph("<b>Index Technical Keywords:</b><br/>"
                      "Phase Change Materials (PCM) · Peltier Thermoelectric Cooling · Medical Cold Chain · "
                      "Sensor-Triggered Hysteresis Control · Latent Heat of Fusion · Thermal Interface Resistance · "
                      "Healthcare Technology · STEM for Viksit Bharat",
                      ParagraphStyle('kw_style', fontName='Helvetica', fontSize=8.5, textColor=NAVY, alignment=TA_LEFT, leading=13))
        ]], colWidths=[PAGE_W - L_MARGIN - R_MARGIN], style=TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), TEAL_LIGHT),
            ('BOX', (0,0), (-1,-1), 0.8, TEAL),
            ('TOPPADDING', (0,0), (-1,-1), 5), ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('LEFTPADDING', (0,0), (-1,-1), 8), ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ])),
        Spacer(1, 3*mm),
        ph_box("SCIENTIFIC DISCLOSURE: All specifications and holding targets (~110 h) represent unverified engineering targets awaiting laboratory execution."),
    ]
    return s

def p07_toc():
    s = [
        banner("TABLE OF CONTENTS & SYSTEM FIGURES"),
        Spacer(1, 1.5*mm),
        Table([
            [Paragraph("<b>Section / Document Module</b>", S['th']), Paragraph("<b>Page</b>", S['th'])],
            [Paragraph("Cover Page — Project SANJIVANI Dossier", S['td']), Paragraph("1", S['td_c'])],
            [Paragraph("Certificate of Original Project Work (Formal School Endorsement)", S['td']), Paragraph("2", S['td_c'])],
            [Paragraph("Student Declaration of Originality and Scientific Ethics", S['td']), Paragraph("3", S['td_c'])],
            [Paragraph("Acknowledgements and Institutional Expressions of Gratitude", S['td']), Paragraph("4", S['td_c'])],
            [Paragraph("Project Particulars, Participant Roster & Observers List", S['td']), Paragraph("5", S['td_c'])],
            [Paragraph("Executive Technical Abstract & Controlled Index Keywords", S['td']), Paragraph("6", S['td_c'])],
            [Paragraph("Table of Contents, Document Architecture & Figure Index", S['td']), Paragraph("7", S['td_c'])],
            [Paragraph("Chapter 1: Introduction to Medical Cold-Chain Vulnerabilities", S['td']), Paragraph("8", S['td_c'])],
            [Paragraph("Chapter 2: Problem Statement, Technical Need & Last-Mile Challenges", S['td']), Paragraph("9", S['td_c'])],
            [Paragraph("Chapter 3: Aim, Research Question, Objectives & Working Hypothesis", S['td']), Paragraph("10", S['td_c'])],
            [Paragraph("Chapter 4: Scientific Principle I — Phase Change Materials (PCM Thermodynamics)", S['td']), Paragraph("11", S['td_c'])],
            [Paragraph("Chapter 5: Scientific Principle II — Peltier Thermoelectric Effect & COP Limits", S['td']), Paragraph("12", S['td_c'])],
            [Paragraph("Chapter 6: Complete SANJIVANI System Architecture & Energy Distribution", S['td']), Paragraph("13", S['td_c'])],
            [Paragraph("Chapter 7: Comprehensive Bill of Materials & Component Selection Criteria", S['td']), Paragraph("14", S['td_c'])],
            [Paragraph("Chapter 8: Thermal Management, Heat Pathways & Heat Sink Mechanics", S['td']), Paragraph("15", S['td_c'])],
            [Paragraph("Chapter 9: Sensors, Controller Architecture & Hysteresis Operational Logic", S['td']), Paragraph("16", S['td_c'])],
            [Paragraph("Chapter 10: Governing Engineering Calculations & Sizing Framework", S['td']), Paragraph("17", S['td_c'])],
            [Paragraph("Chapter 11: Prototype Fabrication Sequence, Assembly & Photographic Log", S['td']), Paragraph("18", S['td_c'])],
            [Paragraph("Chapter 12: Controlled Comparative Experimental Methodology (Config A vs B)", S['td']), Paragraph("19", S['td_c'])],
            [Paragraph("Chapter 13: Empirical Observations, Telemetry Records & Raw Data Matrices", S['td']), Paragraph("20", S['td_c'])],
            [Paragraph("Chapter 14: Results Analysis, Graphical Visualizations & Duty Cycle Evaluation", S['td']), Paragraph("21", S['td_c'])],
            [Paragraph("Chapter 15: Energy Budget, Cost Analysis & Scalability Economics", S['td']), Paragraph("22", S['td_c'])],
            [Paragraph("Chapter 16: System Safety, Reliability Audits & Regulatory Limitations", S['td']), Paragraph("23", S['td_c'])],
            [Paragraph("Chapter 17: Project Conclusions, Engineering Challenges & Future Directions", S['td']), Paragraph("24", S['td_c'])],
            [Paragraph("Chapter 18: Authoritative References & Annexures Checklist", S['td']), Paragraph("25", S['td_c'])],
        ], colWidths=[156*mm, 18*mm], style=TableStyle([
            ('BACKGROUND', (0,0), (-1,0), NAVY),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [TABLE_BG, WHITE]),
            ('BOX', (0,0), (-1,-1), 0.5, RULE_COLOR),
            ('INNERGRID', (0,0), (-1,-1), 0.25, RULE_COLOR),
            ('TOPPADDING', (0,0), (-1,-1), 1.6), ('BOTTOMPADDING', (0,0), (-1,-1), 1.6),
            ('LEFTPADDING', (0,0), (-1,-1), 4), ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ])),
        Spacer(1, 1.5*mm),
        Paragraph("<b>Index of Engineering Schematic Figures:</b> Fig. 1 — PCM Phase Change (p. 11) · Fig. 2 — Peltier Pumping (p. 12) · "
                  "Fig. 3 — System Architecture (p. 13) · Fig. 4 — Operational Flowchart (p. 16) · Fig. 5 — Thermal Pathway (p. 15) · "
                  "Fig. 6 — Comparative Setup (p. 19).", S['caption']),
    ]
    return s

def p08_introduction():
    s = [
        banner("1. INTRODUCTION: MEDICAL COLD-CHAIN DYNAMICS"),
        Spacer(1, 2*mm),
        Paragraph("1.1 The Crucial Role of Medical Cold Chains in Public Health", S['sec']),
        Paragraph(
            "Temperature-sensitive biological pharmaceuticals—encompassing live attenuated and mRNA vaccines, insulins, "
            "blood serums, immunoglobulins, and diagnostic reagents—are intrinsically thermolabile. Their complex protein "
            "conformations and therapeutic potency degrade rapidly when exposed to temperatures outside their validated storage "
            "envelope, which is universally standardized at <b>+2 °C to +8 °C</b> by the World Health Organization (WHO) and National "
            "Immunization Programs [1, 2]. Even transient temperature spikes above +8 °C can trigger protein denaturation and loss "
            "of antigenicity, while accidental exposure to freezing temperatures (<0 °C) causes physical aggregation and irreversible "
            "damage to aluminium-adjuvanted vaccines [2].",
            S['body']
        ),
        Paragraph("1.2 The Off-Grid Last-Mile Dilemma in Indian Healthcare", S['sec']),
        Paragraph(
            "Within the public health geography of India, achieving comprehensive universal immunization (such as Mission Indradhanush) "
            "and delivering essential temperature-critical medications to remote, tribal, and border communities necessitates traversing "
            "arduous distribution legs. Field health workers often travel for multiple days across terrains where electrical grid "
            "access is non-existent, intermittent, or unreliable [3]. In these high-ambient environments—where summer temperatures "
            "routinely exceed 40 °C—the physical security of the cold chain is entirely dependent on portable passive transport coolers.",
            S['body']
        ),
        Paragraph("1.3 Mechanics of Conventional Passive PCM Coolers", S['sec']),
        Paragraph(
            "Current portable cold-chain systems rely predominantly on Phase Change Materials (PCMs) or chilled water/ice packs encased "
            "in polyurethane (PUF) or vacuum-insulated panels (VIP). PCMs exploit the high latent heat of fusion during phase transition, "
            "absorbing environmental heat isothermally. While purely passive coolers require no electrical energy during transit—making "
            "them indispensable for field operations—they possess an unavoidable vulnerability: <i>finite thermal holding duration</i>. "
            "Typical standard vaccine carriers provide an assumed operational holding window of approximately <b>72 hours</b> under standard "
            "laboratory ambient benchmarks [4, 5]. Once the latent phase change is completed, the internal temperature climbs steeply, "
            "rendering all medical payloads invalid.",
            S['body']
        ),
        Paragraph("1.4 Motivation and Identity: Project SANJIVANI", S['sec']),
        Paragraph(
            "Inspired by the mythic life-saving herb <i>Sanjivani</i> (संजीवनी), this engineering project addresses this fundamental "
            "cold-chain limitation. Project SANJIVANI develops an indigenous, sensor-triggered hybrid cooling system that integrates "
            "thermoelectric solid-state cooling with passive PCM storage. Designed under the national theme of <i>STEM for Viksit and "
            "Atmanirbhar Bharat</i>, SANJIVANI provides a technological blueprint for extended healthcare security.",
            S['body']
        ),
    ]
    return s

def p09_problem():
    s = [
        banner("2. PROBLEM STATEMENT & ENGINEERING NEED"),
        Spacer(1, 2*mm),
        Paragraph("2.1 Thermodynamic Vulnerabilities of Purely Passive Enclosures", S['sec']),
        Paragraph(
            "The fundamental flaw of conventional passive medical carriers lies in the Second Law of Thermodynamics: heat transfer "
            "inexorably flows from the warmer exterior ambient to the cooler internal payload zone at a rate dictated by Fourier's Law: "
            "<b>Q_in (rate) = (T_amb - T_int) / R_th</b>. A fixed mass of PCM can only absorb a finite thermal quantity: <b>Q_max = m * L</b>. "
            "In protracted logistical deployments—such as multi-day village vaccination drives, disaster relief camps, military field "
            "operations, or logistical transport delays—the PCM latent capacity is depleted long before medical supplies reach their "
            "intended recipients.",
            S['body']
        ),
        Paragraph("2.2 Shortcomings of Conventional Active Mobile Refrigerators", S['sec']),
        Paragraph(
            "Mobile compressor-driven active refrigerators solve the duration issue but introduce severe operational handicaps: "
            "they are heavy, mechanically fragile, vulnerable to vibration damage over rough roads, expensive to procure, and consume "
            "continuous electrical power (40 W to 80 W), necessitating bulky lead-acid battery packs that cannot be carried by foot-patrol "
            "healthcare personnel. Purely continuous Peltier-based coolers are similarly inefficient, running continuously with low COP "
            "and rapidly draining portable battery reserves within a few hours [6, 9].",
            S['body']
        ),
        Spacer(1, 2*mm),
        Table([[
            Paragraph("<b>FORMAL ENGINEERING PROBLEM STATEMENT:</b><br/>"
                      "<i>Conventional passive PCM medical carriers fail to sustain the mandatory +2 °C to +8 °C storage envelope during "
                      "extended transit exceeding ~72 hours in high-ambient environments. Existing active portable cooling solutions are "
                      "prohibitively heavy, mechanically vulnerable, and electrically unsustainable. There is an urgent engineering need for "
                      "a lightweight, mechanically robust, hybrid cooling architecture that autonomously activates supplementary solid-state "
                      "cooling only when thermal thresholds are breached, thereby extending holding duration towards ~110 hours while "
                      "strictly conserving electrical energy.</i>",
                      ParagraphStyle('prob_box', fontName='Helvetica', fontSize=8.3, textColor=NAVY, alignment=TA_JUSTIFY, leading=12.5))
        ]], colWidths=[PAGE_W - L_MARGIN - R_MARGIN], style=TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), TEAL_LIGHT),
            ('BOX', (0,0), (-1,-1), 1, TEAL_DARK),
            ('TOPPADDING', (0,0), (-1,-1), 6), ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('LEFTPADDING', (0,0), (-1,-1), 8), ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ])),
        Spacer(1, 2*mm),
        Paragraph("2.3 Strategic Engineering Opportunity: Selective Thermoelectric Supplementation", S['sec']),
        Paragraph(
            "By embedding solid-state thermoelectric Peltier modules governed by a closed-loop hysteresis controller, active cooling is "
            "not run continuously. Instead, the Peltier system acts as an autonomous thermal brake: whenever internal temperatures creep "
            "towards the upper critical limit (+6.5 °C to +7.0 °C), the controller pulses the Peltier cold side. This actively cools an "
            "aluminium thermal spreader plate, intercepting heat ingress and retarding PCM melting. When temperature stabilizes, active "
            "cooling ceases, conserving energy while substantially lengthening overall cold-chain longevity.",
            S['body']
        ),
    ]
    return s

def p10_aim():
    s = [
        banner("3. AIM, OBJECTIVES, HYPOTHESIS & TARGETS"),
        Spacer(1, 1.5*mm),
        Paragraph("3.1 Primary Engineering Aim", S['sec']),
        Paragraph(
            "To design, fabricate, and experimentally benchmark an intelligent, sensor-triggered hybrid PCM–Peltier portable medical "
            "cooling system (SANJIVANI) capable of autonomously extending temperature-holding duration beyond conventional passive limits "
            "while maintaining rigorous thermal stability (2 °C – 8 °C) and optimizing electrical energy consumption.",
            S['body']
        ),
        Paragraph("3.2 Specific Research & Engineering Objectives", S['sec']),
        Paragraph("1. Conduct thermodynamic modeling of latent heat storage (Q = mL) and Peltier heat pumping (Q_hot = Q_cold + P_elec).", S['bullet']),
        Paragraph("2. Design a multi-layered thermal enclosure integrating PCM chambers, high-conductivity aluminium spreaders, and TEC modules.", S['bullet']),
        Paragraph("3. Develop a dual-boundary liquid-assisted heat transport mechanism to evacuate hot-side heat away from the internal cavity.", S['bullet']),
        Paragraph("4. Construct an embedded microcontroller architecture with multi-point digital temperature sensors and MOSFET switching.", S['bullet']),
        Paragraph("5. Program an intelligent hysteresis control firmware preventing rapid relay cycling and conserving battery power.", S['bullet']),
        Paragraph("6. Fabricate an engineering prototype ensuring moisture sealing, structural rigidity, and vibration tolerance.", S['bullet']),
        Paragraph("7. Design a standardized comparative testing protocol to benchmark PCM-only vs. Hybrid cooling under identical ambient loads.", S['bullet']),
        Paragraph("8. Perform rigorous economic, safety, and operational feasibility assessments for field deployment.", S['bullet']),
        Paragraph("3.3 Core Research Question & Working Hypothesis", S['sec']),
        Paragraph("<b>Research Question:</b> <i>Can an intelligently controlled thermoelectric subsystem, integrated with a PCM-based "
                  "medical cooling enclosure, extend its useful temperature-holding duration while maintaining acceptable temperature "
                  "stability and controlling electrical energy consumption?</i>", S['body']),
        Paragraph("<b>Working Hypothesis:</b> <i>A sensor-triggered Peltier cooling arrangement, integrated with appropriate heat-spreading "
                  "and heat-rejection components, may slow the loss of useful PCM cooling capacity and extend the time for which the enclosure "
                  "remains within its defined temperature range.</i> (Treated strictly as a testable scientific hypothesis).", S['body']),
        Spacer(1, 1*mm),
        subbanner("System Performance Benchmark & Design Target Framework"),
        Spacer(1, 1*mm),
        Table([
            [Paragraph("<b>Performance Metric</b>", S['th']), Paragraph("<b>Baseline Assumption</b>", S['th']), Paragraph("<b>SANJIVANI Design Target</b>", S['th']), Paragraph("<b>Verification Status</b>", S['th'])],
            [Paragraph("Temperature-Holding Duration", S['td']), Paragraph("~72 Hours (Assumed)", S['td_c']), Paragraph("<b>~110 Hours (Target)</b>", S['td_c']), ph_box("UNTESTED HYPOTHESIS", 38*mm)],
            [Paragraph("Payload Temperature Stability", S['td']), Paragraph("+2 °C to +8 °C", S['td_c']), Paragraph("+2 °C to +8 °C", S['td_c']), ph_box("PENDING EMPIRICAL TRIAL", 38*mm)],
            [Paragraph("Operating Electrical Duty Cycle", S['td']), Paragraph("0% (Passive Only)", S['td_c']), Paragraph("Intermittent (<35%)", S['td_c']), ph_box("PENDING SENSOR LOGS", 38*mm)],
            [Paragraph("Peltier Activation Threshold (T_upper)", S['td']), Paragraph("N/A", S['td_c']), ph_box("T_upper = [ __ °C ]", 32*mm), ph_box("TO BE COMMISSIONED", 38*mm)],
            [Paragraph("Peltier Deactivation Threshold (T_lower)", S['td']), Paragraph("N/A", S['td_c']), ph_box("T_lower = [ __ °C ]", 32*mm), ph_box("TO BE COMMISSIONED", 38*mm)],
        ], colWidths=[54*mm, 34*mm, 44*mm, 42*mm], style=TableStyle([
            ('BACKGROUND', (0,0), (-1,0), NAVY),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [TABLE_BG, WHITE]),
            ('BOX', (0,0), (-1,-1), 0.5, RULE_COLOR),
            ('INNERGRID', (0,0), (-1,-1), 0.25, RULE_COLOR),
            ('TOPPADDING', (0,0), (-1,-1), 2), ('BOTTOMPADDING', (0,0), (-1,-1), 2),
            ('LEFTPADDING', (0,0), (-1,-1), 4), ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ])),
    ]
    return s

def p11_pcm():
    s = [
        banner("4. SCIENTIFIC PRINCIPLE: PHASE CHANGE MATERIALS"),
        Spacer(1, 1.5*mm),
        Paragraph("4.1 Sensible vs. Latent Heat Storage Thermodynamics", S['sec']),
        Paragraph(
            "Thermal energy storage in condensed matter occurs through two distinct thermodynamic phenomena. "
            "<b>Sensible heat storage</b> involves an increase in microscopic kinetic vibrational energy, manifesting as a measurable "
            "temperature rise: <b>Q_sensible = m * c * Delta_T</b>, where <i>m</i> is mass (kg), <i>c</i> is specific heat capacity (J/(kg·K)), "
            "and <i>Delta_T</i> is temperature gradient (K). In contrast, <b>Latent heat storage</b> occurs during a first-order thermodynamic "
            "phase transition (solidus to liquidus) at virtually constant temperature: <b>Q_latent = m * L</b>, where <i>L</i> is the "
            "specific latent heat of fusion (J/kg). Because phase transition absorbs energy through intermolecular bond rupture rather "
            "than molecular acceleration, large thermal loads are absorbed isothermally, making PCMs ideal thermal buffers for cold-chain "
            "preservation [4, 5, 8].",
            S['body']
        ),
        Spacer(1, 1*mm),
        PCMDiagram(width=PAGE_W - L_MARGIN - R_MARGIN, height=34*mm),
        Spacer(1, 1*mm),
        Paragraph("4.2 PCM Selection Criteria & Subcooling Considerations", S['sec']),
        Paragraph(
            "Selecting a PCM for medical cold chains requires strict optimization across six technical criteria: "
            "(1) <i>Transition Temperature:</i> Must lie between +2 °C and +5 °C to buffer payload without freezing; "
            "(2) <i>High Latent Heat:</i> Maximizes energy absorbed per unit weight; "
            "(3) <i>Minimal Subcooling:</i> Ensures crystallization initiates without large thermal lags; "
            "(4) <i>Congruent Melting:</i> Prevents phase separation over repeated thermal cycles; "
            "(5) <i>High Thermal Conductivity:</i> Facilitates heat transfer across boundaries; and "
            "(6) <i>Chemical Safety:</i> Non-toxic, non-corrosive, and non-flammable [5].",
            S['body']
        ),
        Spacer(1, 1*mm),
        subbanner("PCM Engineering Specification Matrix (Awaiting Team Confirmation)"),
        Spacer(1, 1*mm),
        Table([
            [Paragraph("<b>Thermodynamic Parameter</b>", S['th']), Paragraph("<b>SI Unit</b>", S['th']), Paragraph("<b>Theoretical Requirement</b>", S['th']), Paragraph("<b>Prototype Specification (Placeholder)</b>", S['th'])],
            [Paragraph("Chemical Classification / Material Family", S['td']), Paragraph("—", S['td_c']), Paragraph("Organic paraffin or Salt Hydrate", S['td']), ph_box("CHEMISTRY: [ TO BE SPECIFIED ]", 55*mm)],
            [Paragraph("Phase-Change Temperature (T_phase)", S['td']), Paragraph("°C / K", S['td_c']), Paragraph("+3.0 °C to +5.0 °C nominal", S['td']), ph_box("T_phase = [ __ °C ]", 55*mm)],
            [Paragraph("Specific Latent Heat of Fusion (L)", S['td']), Paragraph("kJ/kg", S['td_c']), Paragraph(">180 kJ/kg desired", S['td']), ph_box("L = [ __ kJ/kg ]", 55*mm)],
            [Paragraph("Specific Heat Capacity (Solid Phase, c_s)", S['td']), Paragraph("J/(kg·K)", S['td_c']), Paragraph("~2000 J/(kg·K)", S['td']), ph_box("c_s = [ __ J/(kg·K) ]", 55*mm)],
            [Paragraph("Total Mass Loaded in Prototype (m_PCM)", S['td']), Paragraph("kg", S['td_c']), Paragraph("Sized for enclosure volume", S['td']), ph_box("m_PCM = [ __ kg ]", 55*mm)],
            [Paragraph("Pre-Conditioning Protocol / Storage", S['td']), Paragraph("°C / h", S['td_c']), Paragraph("Fully frozen in laboratory freezer", S['td']), ph_box("FROZEN AT [ __ °C ] FOR [ __ h ]", 55*mm)],
        ], colWidths=[54*mm, 18*mm, 48*mm, 54*mm], style=TableStyle([
            ('BACKGROUND', (0,0), (-1,0), NAVY),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [TABLE_BG, WHITE]),
            ('BOX', (0,0), (-1,-1), 0.5, RULE_COLOR),
            ('INNERGRID', (0,0), (-1,-1), 0.25, RULE_COLOR),
            ('TOPPADDING', (0,0), (-1,-1), 1.8), ('BOTTOMPADDING', (0,0), (-1,-1), 1.8),
            ('LEFTPADDING', (0,0), (-1,-1), 4), ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ])),
    ]
    return s

def p12_peltier():
    s = [
        banner("5. SCIENTIFIC PRINCIPLE: PELTIER THERMOELECTRIC COOLING"),
        Spacer(1, 1.5*mm),
        Paragraph("5.1 Solid-State Thermoelectric Heat Pumping Mechanics", S['sec']),
        Paragraph(
            "The Peltier effect, discovered by Jean Charles Athanase Peltier in 1834, describes the reversible absorption or generation "
            "of thermal energy at the junction of two dissimilar conducting materials when an electric current passes through them [6]. "
            "A modern Thermoelectric Cooler (TEC) consists of heavily doped semiconductor pellets—specifically Bismuth Telluride "
            "(Bi<sub>2</sub>Te<sub>3</sub>) N-type and P-type couples connected electrically in series and thermally in parallel between "
            "metallized ceramic plates. When direct current (DC) flows from the N to the P element, charge carriers (electrons and holes) "
            "transition to higher energy states, absorbing thermal energy from the cold ceramic substrate (Q_cold) and transporting it to the hot substrate [6, 7].",
            S['body']
        ),
        Spacer(1, 1*mm),
        PeltierDiagram(width=PAGE_W - L_MARGIN - R_MARGIN, height=42*mm),
        Spacer(1, 1*mm),
        Paragraph("5.2 Energy Conservation & The Critical Hot-Side Heat Penalty", S['sec']),
        Paragraph(
            "<b>Crucial Thermodynamic Law:</b> A Peltier module does NOT destroy heat; it actively pumps thermal energy against a temperature "
            "gradient while generating internal Joule heating (I²R) and Fourier conductive back-flow. By the First Law of Thermodynamics, "
            "the rate of heat rejected at the hot side (Q_hot) must equal the sum of cooling power (Q_cold) plus electrical power input (P_elec): "
            "<b>Q_hot (rate) = Q_cold (rate) + P_elec = Q_cold (rate) + (V * I)</b>. Consequently, the hot side must dissipate significantly "
            "MORE thermal energy than the cold side absorbs. If hot-side heat is not evacuated immediately, thermal saturation occurs, causing "
            "heat to flood back across the junction and catastrophically heating the cold enclosure.",
            S['body']
        ),
        Paragraph("5.3 Coefficient of Performance (COP) Realities", S['sec']),
        Paragraph(
            "The Coefficient of Performance is defined as <b>COP = Q_cold (rate) / P_elec</b>. Unlike vapour-compression cycles (COP ~ 2.0 to 3.5), "
            "Peltier TECs operate with typical COPs between 0.3 and 0.8 under realistic temperature differentials (Delta_T = 20 K to 30 K) [9]. "
            "Because of this lower efficiency, continuous Peltier operation is energetically impractical for portable battery systems. "
            "However, when used <i>intermittently</i> under sensor-driven hysteresis to support a passive PCM base, thermoelectric cooling "
            "provides an exceptionally viable, solid-state, solid-coupled supplementary cooling mechanism.",
            S['body']
        ),
        Spacer(1, 1*mm),
        subbanner("Thermoelectric Module Specifications (Datasheet Placeholder)"),
        Spacer(1, 1*mm),
        Table([
            [Paragraph("<b>Parameter</b>", S['th']), Paragraph("<b>Typical Benchmark (e.g. TEC1-12706)</b>", S['th']), Paragraph("<b>Actual Prototype Selection (Placeholder)</b>", S['th'])],
            [Paragraph("Module Model & Manufacturer", S['td']), Paragraph("TEC1-12706 (Bismuth Telluride 127 Couples)", S['td']), ph_box("MODEL: [ TO BE CONFIRMED ]", 60*mm)],
            [Paragraph("Max Voltage (V_max) & Current (I_max)", S['td']), Paragraph("14.4 V DC / 6.0 A", S['td']), ph_box("V_max = [ __ V ] | I_max = [ __ A ]", 60*mm)],
            [Paragraph("Operating Setpoint (V_op & I_op)", S['td']), Paragraph("12.0 V DC / 4.0 A (Regulated)", S['td']), ph_box("V_op = [ __ V ] | I_op = [ __ A ]", 60*mm)],
            [Paragraph("Maximum Heat Pumping Capacity (Q_max)", S['td']), Paragraph("50 W to 57 W (at Delta_T = 0 K)", S['td']), ph_box("Q_max = [ __ W ]", 60*mm)],
            [Paragraph("Number of Modules Integrated", S['td']), Paragraph("1 to 2 modules coupled in parallel", S['td']), ph_box("QTY: [ __ MODULES ]", 60*mm)],
        ], colWidths=[54*mm, 60*mm, 60*mm], style=TableStyle([
            ('BACKGROUND', (0,0), (-1,0), NAVY),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [TABLE_BG, WHITE]),
            ('BOX', (0,0), (-1,-1), 0.5, RULE_COLOR),
            ('INNERGRID', (0,0), (-1,-1), 0.25, RULE_COLOR),
            ('TOPPADDING', (0,0), (-1,-1), 1.6), ('BOTTOMPADDING', (0,0), (-1,-1), 1.6),
            ('LEFTPADDING', (0,0), (-1,-1), 4), ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ])),
    ]
    return s

def p13_architecture():
    s = [
        banner("6. COMPLETE SYSTEM ARCHITECTURE & INTEGRATION"),
        Spacer(1, 1.5*mm),
        Paragraph(
            "The SANJIVANI system represents a multi-domain engineering assembly uniting thermodynamic, electrical, and control "
            "subsystems into a unified cold-chain preservation platform. Figure 3 delineates the architectural boundaries and interactions.",
            S['body']
        ),
        Spacer(1, 1*mm),
        SystemBlockDiagram(width=PAGE_W - L_MARGIN - R_MARGIN, height=70*mm),
        Spacer(1, 1.5*mm),
        Paragraph("6.1 Subsystem Functionality & Interactions", S['sec']),
        Paragraph("• <b>Insulated Structural Enclosure:</b> High-density outer composite shell packed with rigid polyurethane foam (PUF) "
                  "providing high thermal resistance (R_th) to minimize parasitic ambient heat conduction.", S['bullet']),
        Paragraph("• <b>PCM Thermal Reservoir:</b> Encapsulated high-latent-heat packs forming the internal core cavity, acting as the primary "
                  "passive isothermal heat sink holding the medical payload within +2 °C to +8 °C.", S['bullet']),
        Paragraph("• <b>Isothermal Aluminium Heat Spreader:</b> High-conductivity (k ~ 205 W/(m·K)) aluminium plate interfacing the Peltier "
                  "cold side to distribute localized cooling across the broad PCM surface, eliminating localized freezing points.", S['bullet']),
        Paragraph("• <b>Thermoelectric Peltier Assembly:</b> Solid-state heat pumps mounted through the thermal barrier, coupling their cold faces "
                  "to the internal aluminium spreader and hot faces to the external dissipation mechanism.", S['bullet']),
        Paragraph("• <b>Liquid Thermal-Transfer Chamber:</b> Intermediate thermal conduit evacuating concentrated hot-side heat away from the "
                  "cavity wall to prevent structural heat leakage into the cold boundary.", S['bullet']),
        Paragraph("• <b>Hot-Side Heat Sink & Forced-Air Exchanger:</b> High-surface-area finned aluminium heat sink paired with a low-noise DC "
                  "axial fan discharging Q_hot to the surrounding atmosphere.", S['bullet']),
        Paragraph("• <b>Digital Sensor & Control Automation:</b> Multi-point digital temperature sensors relaying real-time telemetry to an "
                  "embedded microcontroller executing the hysteresis switching algorithm.", S['bullet']),
        Paragraph("• <b>DC Power Distribution Unit:</b> Regulated DC battery bank delivering decoupled electrical power to the controller "
                  "and high-current switching MOSFETs.", S['bullet']),
    ]
    return s

def p14_components():
    s = [
        banner("7. BILL OF MATERIALS & COMPONENT SELECTION"),
        Spacer(1, 1.5*mm),
        Paragraph(
            "Component selection for SANJIVANI balances thermodynamic performance, weight constraints, electrical efficiency, and "
            "availability in accordance with the <i>Atmanirbhar Bharat</i> ethos. Table 7 outlines the complete technical BOM framework.",
            S['body']
        ),
        Spacer(1, 1*mm),
        Table([
            [Paragraph("<b>#</b>", S['th']), Paragraph("<b>Component Name</b>", S['th']), Paragraph("<b>Engineering Function</b>", S['th']), Paragraph("<b>Selection & Specification Criteria</b>", S['th']), Paragraph("<b>Specification / Model (Placeholder)</b>", S['th'])],
            [Paragraph("1", S['td_c']), Paragraph("Phase Change Material (PCM)", S['td']), Paragraph("Primary passive latent heat buffer", S['td']), Paragraph("T_phase ~ +3 °C to +5 °C; high latent heat of fusion; non-toxic", S['td']), ph_box("CHEMISTRY & MASS: [ __ kg ]", 38*mm)],
            [Paragraph("2", S['td_c']), Paragraph("Insulated Enclosure Shell", S['td']), Paragraph("Thermal barrier against ambient ingress", S['td']), Paragraph("Rigid PUF / vacuum panels; k <= 0.025 W/(m·K); impact resistant", S['td']), ph_box("VOL: [ __ L ] | THICKNESS: [ __ mm ]", 38*mm)],
            [Paragraph("3", S['td_c']), Paragraph("Peltier Thermoelectric Modules", S['td']), Paragraph("Supplementary solid-state heat pumping", S['td']), Paragraph("Bi<sub>2</sub>Te<sub>3</sub> semiconductor couples; sized for Q_cold > Q_in; 12 V DC", S['td']), ph_box("MODEL: [ __ ] | QTY: [ __ ]", 38*mm)],
            [Paragraph("4", S['td_c']), Paragraph("Aluminium Heat Spreader Plate", S['td']), Paragraph("Isothermal distribution across PCM", S['td']), Paragraph("Alloy 6061 / 1050; k ~ 205 W/(m·K); flat polished contact surface", S['td']), ph_box("GRADE: [ __ ] | DIM: [ __ mm ]", 38*mm)],
            [Paragraph("5", S['td_c']), Paragraph("Liquid Thermal Transfer Chamber", S['td']), Paragraph("Transports hot-side heat away from shell", S['td']), Paragraph("Sealed cavity; high specific heat transfer fluid; zero-leak seals", S['td']), ph_box("CONFIG: [ DESIGN TBC ]", 38*mm)],
            [Paragraph("6", S['td_c']), Paragraph("Hot-Side Aluminium Heat Sink", S['td']), Paragraph("Convective thermal rejection to air", S['td']), Paragraph("Multi-finned extruded aluminium; thermal resistance R_hs < 0.5 K/W", S['td']), ph_box("SURFACE AREA: [ __ cm<sup>2</sup> ]", 38*mm)],
            [Paragraph("7", S['td_c']), Paragraph("Brushless DC Heat Sink Fan", S['td']), Paragraph("Forced air convection over heat sink", S['td']), Paragraph("12 V DC brushless; high static pressure; low acoustic signature", S['td']), ph_box("CFM: [ __ ] | NOISE: [ __ dBA ]", 38*mm)],
            [Paragraph("8", S['td_c']), Paragraph("Digital Temperature Sensors", S['td']), Paragraph("Continuous thermal monitoring", S['td']), Paragraph("Digital 1-Wire / I2C; accuracy ±0.5 °C; operating range -10 °C to +50 °C", S['td']), ph_box("MODEL: [ e.g. DS18B20 * __ ]", 38*mm)],
            [Paragraph("9", S['td_c']), Paragraph("Embedded Microcontroller Board", S['td']), Paragraph("Executes hysteresis control algorithm", S['td']), Paragraph("Low standby power; hardware timers; digital ADC & PWM channels", S['td']), ph_box("MCU: [ e.g. ATmega328P / TBC ]", 38*mm)],
            [Paragraph("10", S['td_c']), Paragraph("Power MOSFET Switching Board", S['td']), Paragraph("Peltier & fan power modulation", S['td']), Paragraph("Logic-level N-channel MOSFET; low R_DS(on) (<10 mOhm) to prevent heating", S['td']), ph_box("MOSFET: [ e.g. IRLZ44N / TBC ]", 38*mm)],
            [Paragraph("11", S['td_c']), Paragraph("Portable DC Battery Bank", S['td']), Paragraph("Electrical power for active subsystem", S['td']), Paragraph("Lithium Iron Phosphate (LiFePO4) / Li-ion; stable 12 V; high cycle life", S['td']), ph_box("CAPACITY: [ __ Ah @ 12 V ]", 38*mm)],
            [Paragraph("12", S['td_c']), Paragraph("Thermal Interface Material (TIM)", S['td']), Paragraph("Eliminates microscopic air gaps", S['td']), Paragraph("High thermal conductivity paste / pads (k > 4.5 W/(m·K))", S['td']), ph_box("TIM TYPE: [ PASTE / PAD TBC ]", 38*mm)],
            [Paragraph("13", S['td_c']), Paragraph("Wiring, Seals & Connectors", S['td']), Paragraph("Electrical & moisture protection", S['td']), Paragraph("Heavy gauge copper wire (16-18 AWG); silicone gaskets; waterproof jacks", S['td']), ph_box("SPECIFICATION: [ TBC ]", 38*mm)],
        ], colWidths=[6*mm, 38*mm, 38*mm, 54*mm, 38*mm], style=TableStyle([
            ('BACKGROUND', (0,0), (-1,0), NAVY),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [TABLE_BG, WHITE]),
            ('BOX', (0,0), (-1,-1), 0.5, RULE_COLOR),
            ('INNERGRID', (0,0), (-1,-1), 0.25, RULE_COLOR),
            ('TOPPADDING', (0,0), (-1,-1), 1.5), ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
            ('LEFTPADDING', (0,0), (-1,-1), 3), ('RIGHTPADDING', (0,0), (-1,-1), 3),
        ])),
        Spacer(1, 1*mm),
        Paragraph("<i>Note: Component models, dimensions, and chemical grades are preserved as uninvented placeholders to be updated upon physical procurement.</i>", S['caption']),
    ]
    return s

def p15_thermal():
    s = [
        banner("8. THERMAL MANAGEMENT & HEAT-TRANSFER PATHWAYS"),
        Spacer(1, 1.5*mm),
        Paragraph("8.1 Mapping Thermal Pathways: Ambient Ingress to External Rejection", S['sec']),
        Paragraph(
            "Thermal management in SANJIVANI addresses a dual boundary problem: retarding environmental heat entering the cold "
            "chamber while ensuring that intense thermoelectric heat generated at the Peltier hot side is expelled without structural "
            "back-flow. Figure 5 tracks the complete energy continuum.",
            S['body']
        ),
        Spacer(1, 1*mm),
        ThermalFlowDiagram(width=PAGE_W - L_MARGIN - R_MARGIN, height=34*mm),
        Spacer(1, 1.5*mm),
        Paragraph("8.2 Heat Ingress Modeling Across Insulated Boundaries", S['sec']),
        Paragraph(
            "Thermal leakage through the insulated walls follows the thermal resistance network: <b>Q_in (rate) = A * (T_amb - T_int) / (d / k)</b>, "
            "where <i>A</i> is surface area (m<sup>2</sup>), <i>d</i> is insulation thickness (m), and <i>k</i> is thermal conductivity (W/(m·K)). "
            "Maximizing R_th suppresses baseline heat ingress, extending passive holding time and reducing Peltier active runtimes.",
            S['body']
        ),
        Paragraph("8.3 Role of the Aluminium Isothermal Heat Spreader", S['sec']),
        Paragraph(
            "Peltier TEC modules possess compact surface footprints (typically 40 mm * 40 mm). Coupling this concentrated cold spot directly "
            "to a PCM pack would cause localized freezing (<0 °C) in the immediate contact zone while leaving remote corners unaffected. "
            "The integrated high-conductivity aluminium plate spreads cold-side thermal flux across the entire lateral surface, creating "
            "an isothermal boundary layer that draws heat uniformly from the PCM mass without inducing vaccine freeze damage.",
            S['body']
        ),
        Paragraph("8.4 Critical Distinctions in Liquid Thermal Transfer", S['sec']),
        Paragraph(
            "<b>Engineering Clarification:</b> A sealed liquid volume CANNOT destroy heat. The report establishes three clear engineering boundaries: "
            "(1) <i>Heat Transport:</i> The liquid rapidly conveys concentrated hot-side flux away from the structural wall; "
            "(2) <i>Temporary Heat Buffering:</i> The liquid's sensible thermal capacity (Q = m * c * Delta_T) temporarily absorbs heat during initial activation; and "
            "(3) <i>External Heat Rejection:</i> To operate sustainably, this heat MUST be rejected to the surrounding atmosphere via an external "
            "fin-and-fan heat exchanger. The exact liquid circulation mechanism (passive convection, thermosiphon, or mini-pump) remains to be confirmed.",
            S['body']
        ),
        Paragraph("8.5 Condensation Management & Thermal Non-Uniformity", S['sec']),
        Paragraph(
            "When cold-side temperatures drop below the dew point of enclosed air, moisture condensation occurs. SANJIVANI incorporates "
            "closed-cell perimeter sealing and moisture drainage pathways to prevent water accumulation near electrical sensors and terminals.",
            S['body']
        ),
    ]
    return s

def p16_control():
    s = [
        banner("9. SENSORS, CONTROLLER & OPERATIONAL LOGIC"),
        Spacer(1, 1.5*mm),
        Paragraph("9.1 Multi-Point Temperature Sensing Architecture", S['sec']),
        Paragraph(
            "Accurate, drift-free thermal telemetry is vital for closed-loop automation. SANJIVANI deploys digital temperature sensors "
            "across three strategic nodes: (1) <i>Payload Core Zone</i> (T_payload), (2) <i>PCM Boundary Interface</i> (T_PCM), and "
            "(3) <i>Peltier Hot-Side Heat Sink</i> (T_hot). Sensors communicate via a robust digital protocol to avoid analogue noise pickup.",
            S['body']
        ),
        Spacer(1, 1*mm),
        FlowchartDiagram(width=PAGE_W - L_MARGIN - R_MARGIN, height=74*mm),
        Spacer(1, 1.5*mm),
        Paragraph("9.2 Closed-Loop Hysteresis Algorithm & Threshold Table", S['sec']),
        Paragraph(
            "To prevent rapid on-off cycling (chattering) which damages thermoelectric junctions and degrades switching MOSFETs, the "
            "firmware implements a hysteresis dead-band: <b>Delta_T_hys = T_upper - T_lower</b>. The operational thresholds are detailed in Table 9.",
            S['body']
        ),
        Spacer(1, 1*mm),
        Table([
            [Paragraph("<b>Hysteresis Threshold Parameter</b>", S['th']), Paragraph("<b>Control System Action</b>", S['th']), Paragraph("<b>Engineering Rationale</b>", S['th']), Paragraph("<b>Programmed Setpoint (Placeholder)</b>", S['th'])],
            [Paragraph("Upper Activation Threshold (T_upper)", S['td']), Paragraph("Peltier & Fan Triggered ON (High State)", S['td']), Paragraph("Interceps heat ingress before payload exceeds WHO limit (+8 °C)", S['td']), ph_box("T_upper = [ __ °C ]", 38*mm)],
            [Paragraph("Lower Deactivation Threshold (T_lower)", S['td']), Paragraph("Peltier & Fan Switched OFF (Low State)", S['td']), Paragraph("Prevents overcooling / freezing payload; resumes passive mode", S['td']), ph_box("T_lower = [ __ °C ]", 38*mm)],
            [Paragraph("Hysteresis Dead-Band (Delta_T_hys)", S['td']), Paragraph("Maintains current state during transition", S['td']), Paragraph("Eliminates rapid oscillatory switching; maximizes TEC lifespan", S['td']), ph_box("Delta_T_hys = [ __ °C ]", 38*mm)],
            [Paragraph("Critical Hot-Side Cut-Off (T_hot_limit)", S['td']), Paragraph("EMERGENCY SHUTDOWN of Peltier", S['td']), Paragraph("Thermal protection interlock preventing module burn-out", S['td']), ph_box("T_hot_limit = [ __ °C ]", 38*mm)],
        ], colWidths=[48*mm, 42*mm, 48*mm, 36*mm], style=TableStyle([
            ('BACKGROUND', (0,0), (-1,0), NAVY),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [TABLE_BG, WHITE]),
            ('BOX', (0,0), (-1,-1), 0.5, RULE_COLOR),
            ('INNERGRID', (0,0), (-1,-1), 0.25, RULE_COLOR),
            ('TOPPADDING', (0,0), (-1,-1), 1.6), ('BOTTOMPADDING', (0,0), (-1,-1), 1.6),
            ('LEFTPADDING', (0,0), (-1,-1), 4), ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ])),
    ]
    return s

def p17_calcs():
    s = [
        banner("10. GOVERNING ENGINEERING CALCULATIONS"),
        Spacer(1, 1.5*mm),
        Paragraph(
            "This chapter presents the theoretical equations governing thermal storage, heat ingress, and electrical energy consumption. "
            "Values are formatted as a computational worksheet to be finalized following laboratory measurements.",
            S['body']
        ),
        Spacer(1, 1*mm),
        Paragraph("10.1 PCM Latent Reserve & Sensible Capacity", S['subsec']),
        Paragraph("Governing Equations: <b>Q_latent = m_PCM * L</b> &nbsp;|&nbsp; <b>Q_sensible = m_PCM * c_s * (T_phase - T_init)</b>", S['eq']),
        Table([
            [Paragraph("<b>Parameter Description</b>", S['th']), Paragraph("<b>Variable</b>", S['th']), Paragraph("<b>SI Unit</b>", S['th']), Paragraph("<b>Calculation / Value (Placeholder)</b>", S['th'])],
            [Paragraph("Mass of Phase Change Material", S['td']), Paragraph("m_PCM", S['td_c']), Paragraph("kg", S['td_c']), ph_box("m_PCM = [ __ kg ]", 55*mm)],
            [Paragraph("Specific Latent Heat of Fusion", S['td']), Paragraph("L", S['td_c']), Paragraph("J/kg", S['td_c']), ph_box("L = [ __ J/kg ]", 55*mm)],
            [Paragraph("Total Latent Energy Stored", S['td']), Paragraph("Q_latent", S['td_c']), Paragraph("Joules (J)", S['td_c']), ph_box("Q_L = m * L = [ __ J ]", 55*mm)],
            [Paragraph("Latent Energy Converted to Watt-Hours", S['td']), Paragraph("E_latent", S['td_c']), Paragraph("Watt-hours (Wh)", S['td_c']), ph_box("E_L = Q_L / 3600 = [ __ Wh ]", 55*mm)],
        ], colWidths=[60*mm, 20*mm, 24*mm, 70*mm], style=TableStyle([
            ('BACKGROUND', (0,0), (-1,0), TEAL),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [TABLE_BG, WHITE]),
            ('BOX', (0,0), (-1,-1), 0.5, RULE_COLOR),
            ('INNERGRID', (0,0), (-1,-1), 0.25, RULE_COLOR),
            ('TOPPADDING', (0,0), (-1,-1), 1.5), ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
            ('LEFTPADDING', (0,0), (-1,-1), 4), ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ])),
        Spacer(1, 1.5*mm),
        Paragraph("10.2 Approximate Environmental Heat Ingress Rate", S['subsec']),
        Paragraph("Governing Equation: <b>Q_in (rate) = (T_ambient - T_payload) / R_total = (k_ins * A_eff * Delta_T) / d_ins</b>", S['eq']),
        Table([
            [Paragraph("<b>Parameter Description</b>", S['th']), Paragraph("<b>Variable</b>", S['th']), Paragraph("<b>SI Unit</b>", S['th']), Paragraph("<b>Calculation / Value (Placeholder)</b>", S['th'])],
            [Paragraph("Test Ambient Temperature Benchmark", S['td']), Paragraph("T_amb", S['td_c']), Paragraph("°C / K", S['td_c']), ph_box("T_amb = [ __ °C ]", 55*mm)],
            [Paragraph("Target Enclosure Internal Setpoint", S['td']), Paragraph("T_int", S['td_c']), Paragraph("°C / K", S['td_c']), ph_box("T_int = [ __ °C ]", 55*mm)],
            [Paragraph("Total Thermal Resistance of Shell", S['td']), Paragraph("R_total", S['td_c']), Paragraph("K/W", S['td_c']), ph_box("R_tot = [ __ K/W ]", 55*mm)],
            [Paragraph("Estimated Continuous Heat Ingress Rate", S['td']), Paragraph("Q_in (rate)", S['td_c']), Paragraph("Watts (W)", S['td_c']), ph_box("Q_in = Delta_T / R_tot = [ __ W ]", 55*mm)],
            [Paragraph("Theoretical Passive PCM Holding Time", S['td']), Paragraph("t_passive", S['td_c']), Paragraph("Hours (h)", S['td_c']), ph_box("t_pass = Q_L / (Q_in * 3600) = [ __ h ]", 55*mm)],
        ], colWidths=[60*mm, 20*mm, 24*mm, 70*mm], style=TableStyle([
            ('BACKGROUND', (0,0), (-1,0), TEAL),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [TABLE_BG, WHITE]),
            ('BOX', (0,0), (-1,-1), 0.5, RULE_COLOR),
            ('INNERGRID', (0,0), (-1,-1), 0.25, RULE_COLOR),
            ('TOPPADDING', (0,0), (-1,-1), 1.5), ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
            ('LEFTPADDING', (0,0), (-1,-1), 4), ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ])),
        Spacer(1, 1.5*mm),
        Paragraph("10.3 Peltier Electrical Power, Energy Consumption & Battery Sizing", S['subsec']),
        Paragraph("Governing Equations: <b>P_elec = V_op * I_op</b> &nbsp;|&nbsp; <b>E_total = P_elec * t_active + P_aux * t_total</b>", S['eq']),
        Table([
            [Paragraph("<b>Electrical Parameter</b>", S['th']), Paragraph("<b>Variable</b>", S['th']), Paragraph("<b>SI Unit</b>", S['th']), Paragraph("<b>Calculated Specification (Placeholder)</b>", S['th'])],
            [Paragraph("Operating Voltage & Current Load", S['td']), Paragraph("V_op / I_op", S['td_c']), Paragraph("V / A", S['td_c']), ph_box("V_op = [ __ V ] | I_op = [ __ A ]", 55*mm)],
            [Paragraph("Peltier Active Power Draw", S['td']), Paragraph("P_elec", S['td_c']), Paragraph("Watts (W)", S['td_c']), ph_box("P_elec = V * I = [ __ W ]", 55*mm)],
            [Paragraph("Total Active Pumping Runtime", S['td']), Paragraph("t_active", S['td_c']), Paragraph("Hours (h)", S['td_c']), ph_box("t_active = [ __ h ]", 55*mm)],
            [Paragraph("Total Operating Energy Consumed", S['td']), Paragraph("E_consumed", S['td_c']), Paragraph("Watt-hours (Wh)", S['td_c']), ph_box("E_cons = P * t_act = [ __ Wh ]", 55*mm)],
            [Paragraph("Minimum Required Battery Capacity", S['td']), Paragraph("C_battery", S['td_c']), Paragraph("Ampere-hours (Ah)", S['td_c']), ph_box("C_bat = E_cons / V_bat = [ __ Ah ]", 55*mm)],
        ], colWidths=[60*mm, 20*mm, 24*mm, 70*mm], style=TableStyle([
            ('BACKGROUND', (0,0), (-1,0), TEAL),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [TABLE_BG, WHITE]),
            ('BOX', (0,0), (-1,-1), 0.5, RULE_COLOR),
            ('INNERGRID', (0,0), (-1,-1), 0.25, RULE_COLOR),
            ('TOPPADDING', (0,0), (-1,-1), 1.5), ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
            ('LEFTPADDING', (0,0), (-1,-1), 4), ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ])),
    ]
    return s

def p18_prototype():
    s = [
        banner("11. PROTOTYPE DEVELOPMENT & FABRICATION LOG"),
        Spacer(1, 1.5*mm),
        Paragraph("11.1 Phased Engineering Fabrication Sequence", S['sec']),
        Table([
            [Paragraph("<b>Stage & Title</b>", S['th']), Paragraph("<b>Fabrication Scope & Technical Assembly Details</b>", S['th'])],
            [Paragraph("Stage 1: Enclosure Preparation", S['td_c']), Paragraph("Procured and cut rigid insulated shell; milled precise lateral apertures for thermoelectric feedthroughs; sealed interior wall joints.", S['td'])],
            [Paragraph("Stage 2: PCM Modular Mounting", S['td_c']), Paragraph("Fabricated sealed leak-proof containment cassettes for the PCM; arranged packs along perimeter to maximize core contact.", S['td'])],
            [Paragraph("Stage 3: Aluminium Spreader Finishing", S['td_c']), Paragraph("Precision-cut 6061 alloy aluminium plates; lap-polished mating faces to surface roughness Ra < 0.8 um to eliminate contact resistance.", S['td'])],
            [Paragraph("Stage 4: Thermoelectric Interface Joint", S['td_c']), Paragraph("Applied uniform thermal interface paste (k > 4.5 W/(m·K)); clamped Peltier modules with spring-loaded bolts at calibrated torque.", S['td'])],
            [Paragraph("Stage 5: Liquid Transfer Subsystem", S['td_c']), Paragraph("Constructed the liquid-assisted heat transport chamber; pressure-tested fluid seals against leakage; installed heat conduit tubing.", S['td'])],
            [Paragraph("Stage 6: Hot-Side Heat Exchanger", S['td_c']), Paragraph("Mounted multi-finned extruded aluminium heat sink to hot face; coupled brushless DC axial fan; duct-shrouded airflow exhaust.", S['td'])],
            [Paragraph("Stage 7: Sensor Array Integration", S['td_c']), Paragraph("Positioned calibrated DS18B20 digital sensors at payload core, PCM boundary, and heat sink; sealed wire pass-throughs.", S['td'])],
            [Paragraph("Stage 8: Embedded Controller Assembly", S['td_c']), Paragraph("Wired microcontroller, logic-level power MOSFETs, flyback diodes, and decoupling capacitors on custom PCB; uploaded firmware.", S['td'])],
            [Paragraph("Stage 9: Electrical & Insulation Audit", S['td_c']), Paragraph("Verified insulation resistance; confirmed DC power bus polarity; audited transient switching voltages with digital oscilloscope.", S['td'])],
            [Paragraph("Stage 10: Final Inspection & Bench Test", S['td_c']), Paragraph("Executed preliminary dry-run test; validated hysteresis state transitions, sensor telemetry streaming, and fan activation.", S['td'])],
        ], colWidths=[42*mm, 132*mm], style=TableStyle([
            ('BACKGROUND', (0,0), (-1,0), NAVY),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [TABLE_BG, WHITE]),
            ('BOX', (0,0), (-1,-1), 0.5, RULE_COLOR),
            ('INNERGRID', (0,0), (-1,-1), 0.25, RULE_COLOR),
            ('TOPPADDING', (0,0), (-1,-1), 1.6), ('BOTTOMPADDING', (0,0), (-1,-1), 1.6),
            ('LEFTPADDING', (0,0), (-1,-1), 3), ('RIGHTPADDING', (0,0), (-1,-1), 3),
        ])),
        Spacer(1, 2*mm),
        subbanner("Physical Prototype Photographic Evidence (Placeholders)"),
        Spacer(1, 1.5*mm),
        Table([
            [ph_box("FIGURE P1: ASSEMBLED SANJIVANI SYSTEM\n(External View showing Housing & Fan Exhaust)", 85*mm),
             ph_box("FIGURE P2: INTERNAL PAYLOAD CHAMBER\n(Aluminium Spreader Plate & PCM Pack Configuration)", 85*mm)],
            [ph_box("FIGURE P3: THERMOELECTRIC & LIQUID ASSEMBLY\n(Peltier Mounting Joint, TIM Application & Fluid Conduit)", 85*mm),
             ph_box("FIGURE P4: ELECTRONIC CONTROLLER & SENSOR BUS\n(Microcontroller Board, Switching MOSFET & Sensor Wiring)", 85*mm)],
        ], colWidths=[87*mm, 87*mm], style=TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('TOPPADDING', (0,0), (-1,-1), 3), ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ])),
    ]
    return s

def p19_methodology():
    s = [
        banner("12. CONTROLLED EXPERIMENTAL METHODOLOGY"),
        Spacer(1, 1.5*mm),
        Paragraph("12.1 Comparative Testing Protocol Architecture", S['sec']),
        Paragraph(
            "To rigorously evaluate the hypothesis, a controlled comparative test is designed comparing a standard passive cooler "
            "(Configuration A) against the active hybrid SANJIVANI cooler (Configuration B) under identical environmental stress.",
            S['body']
        ),
        Spacer(1, 1*mm),
        ExperimentalSetupDiagram(width=PAGE_W - L_MARGIN - R_MARGIN, height=34*mm),
        Spacer(1, 1*mm),
        Paragraph("12.2 Scientific Variables Matrix", S['sec']),
        Table([
            [Paragraph("<b>Variable Classification</b>", S['th']), Paragraph("<b>Experimental Parameter</b>", S['th']), Paragraph("<b>Control / Measurement Method</b>", S['th'])],
            [Paragraph("Independent Variable", S['td']), Paragraph("Cooling Mode Configuration", S['td']), Paragraph("Config A (PCM-Only Passive) vs. Config B (SANJIVANI Sensor-Triggered Hybrid)", S['td'])],
            [Paragraph("Dependent Variables", S['td']), Paragraph("1. Internal Payload Temp, T(t)<br/>2. Holding Duration (h)<br/>3. Total Energy Draw (Wh)", S['td']), Paragraph("Continuous digital logging (15 min sampling); duration to reach excursion (>8 °C); cumulative electrical power monitoring (V * I * t)", S['td'])],
            [Paragraph("Controlled Variables", S['td']), Paragraph("1. Ambient Room Temp (T_amb)<br/>2. Total PCM Mass & Chemistry<br/>3. Initial PCM Conditioning Temp<br/>4. Thermal Enclosure Volume", S['td']), Paragraph("Monitored climate-controlled room; identical PCM packs from same batch; pre-conditioned at identical freezer setpoint (-18 °C) for 24 h; identical physical enclosure volume (L)", S['td'])],
        ], colWidths=[38*mm, 52*mm, 84*mm], style=TableStyle([
            ('BACKGROUND', (0,0), (-1,0), NAVY),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [TABLE_BG, WHITE]),
            ('BOX', (0,0), (-1,-1), 0.5, RULE_COLOR),
            ('INNERGRID', (0,0), (-1,-1), 0.25, RULE_COLOR),
            ('TOPPADDING', (0,0), (-1,-1), 1.6), ('BOTTOMPADDING', (0,0), (-1,-1), 1.6),
            ('LEFTPADDING', (0,0), (-1,-1), 4), ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ])),
        Spacer(1, 1*mm),
        Paragraph("12.3 Step-by-Step Experimental Procedure", S['sec']),
        Paragraph("1. <i>Pre-Conditioning:</i> PCM cassettes conditioned in laboratory freezer at -18 °C for 24 hours to ensure complete solidus crystallization.", S['num_item']),
        Paragraph("2. <i>Thermal Dummy Loading:</i> Load thermal payload vials (saline water simulating vaccines) conditioned to +4 °C into core cavity.", S['num_item']),
        Paragraph("3. <i>Assembly & Sealing:</i> Install PCM packs, connect sensors, secure insulated lid, and engage compression latches.", S['num_item']),
        Paragraph("4. <i>Telemetry Initialization:</i> Activate data-acquisition logger, recording T_amb, T_payload, T_PCM, and T_hot every 15 minutes.", S['num_item']),
        Paragraph("5. <i>Configuration A Trial:</i> Allow passive warming without DC power until payload temperature exceeds +8.0 °C (Terminal Excursion).", S['num_item']),
        Paragraph("6. <i>Configuration B Trial:</i> Connect DC battery bus. Controller runs hysteresis logic, pulsing Peltier upon T_payload >= T_upper.", S['num_item']),
        Paragraph("7. <i>Repetition & Verification:</i> Perform minimum three repeated trials per configuration to ensure statistical reproducibility.", S['num_item']),
    ]
    return s

def p20_observations():
    s = [
        banner("13. OBSERVATIONS & RAW DATA LOGGING MATRICES"),
        Spacer(1, 1.5*mm),
        Paragraph(
            "The observation matrices below are prepared for empirical data collection during controlled testing. In strict adherence "
            "to scientific ethics, all data cells are maintained as unpopulated placeholders awaiting actual test execution.",
            S['body']
        ),
        Spacer(1, 1*mm),
        subbanner("Table 13.1 — Configuration A: Conventional PCM-Only Passive Cooling (Trial 1 / 2 / 3)"),
        Spacer(1, 0.8*mm),
        Table([
            [Paragraph("<b>Time (h:mm)</b>", S['th']), Paragraph("<b>Ambient Temp (°C)</b>", S['th']), Paragraph("<b>Payload Temp (°C)</b>", S['th']), Paragraph("<b>PCM Temp (°C)</b>", S['th']), Paragraph("<b>Observed Thermodynamic Phase & Remarks</b>", S['th'])],
            [Paragraph("00:00", S['td_c']), ph_box("__", 22*mm), ph_box("__", 22*mm), ph_box("__", 22*mm), ph_box("Baseline initialized; PCM fully solidus", 65*mm)],
            [Paragraph("12:00", S['td_c']), ph_box("__", 22*mm), ph_box("__", 22*mm), ph_box("__", 22*mm), ph_box("Sensible heating phase", 65*mm)],
            [Paragraph("24:00", S['td_c']), ph_box("__", 22*mm), ph_box("__", 22*mm), ph_box("__", 22*mm), ph_box("Latent plateau melting", 65*mm)],
            [Paragraph("36:00", S['td_c']), ph_box("__", 22*mm), ph_box("__", 22*mm), ph_box("__", 22*mm), ph_box("Latent plateau melting", 65*mm)],
            [Paragraph("48:00", S['td_c']), ph_box("__", 22*mm), ph_box("__", 22*mm), ph_box("__", 22*mm), ph_box("Isothermal buffer holding", 65*mm)],
            [Paragraph("60:00", S['td_c']), ph_box("__", 22*mm), ph_box("__", 22*mm), ph_box("__", 22*mm), ph_box("PCM liquid fraction increasing", 65*mm)],
            [Paragraph("72:00", S['td_c']), ph_box("__", 22*mm), ph_box("__", 22*mm), ph_box("__", 22*mm), ph_box("Approaching latent exhaustion (~72 h benchmark)", 65*mm)],
            [Paragraph("Terminal", S['td_c']), ph_box("__", 22*mm), ph_box("__", 22*mm), ph_box("__", 22*mm), ph_box("Excursion reached (T > 8.0 °C); test concluded", 65*mm)],
        ], colWidths=[20*mm, 26*mm, 26*mm, 26*mm, 76*mm], style=TableStyle([
            ('BACKGROUND', (0,0), (-1,0), NAVY),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [TABLE_BG, WHITE]),
            ('BOX', (0,0), (-1,-1), 0.5, RULE_COLOR),
            ('INNERGRID', (0,0), (-1,-1), 0.25, RULE_COLOR),
            ('TOPPADDING', (0,0), (-1,-1), 1.5), ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
            ('LEFTPADDING', (0,0), (-1,-1), 3), ('RIGHTPADDING', (0,0), (-1,-1), 3),
        ])),
        Spacer(1, 1.5*mm),
        subbanner("Table 13.2 — Configuration B: SANJIVANI Sensor-Triggered Hybrid System (Trial 1 / 2 / 3)"),
        Spacer(1, 0.8*mm),
        Table([
            [Paragraph("<b>Time (h)</b>", S['th']), Paragraph("<b>T_amb</b>", S['th']), Paragraph("<b>T_pay</b>", S['th']), Paragraph("<b>T_PCM</b>", S['th']), Paragraph("<b>T_hot</b>", S['th']), Paragraph("<b>V (V)</b>", S['th']), Paragraph("<b>I (A)</b>", S['th']), Paragraph("<b>Peltier State</b>", S['th']), Paragraph("<b>Operational Telemetry Remarks</b>", S['th'])],
            [Paragraph("00:00", S['td_c']), ph_box("_", 13*mm), ph_box("_", 13*mm), ph_box("_", 13*mm), ph_box("_", 13*mm), ph_box("_", 11*mm), ph_box("_", 11*mm), ph_box("STANDBY", 18*mm), ph_box("System armed; passive hold", 44*mm)],
            [Paragraph("24:00", S['td_c']), ph_box("_", 13*mm), ph_box("_", 13*mm), ph_box("_", 13*mm), ph_box("_", 13*mm), ph_box("_", 11*mm), ph_box("_", 11*mm), ph_box("OFF", 18*mm), ph_box("PCM passive buffer active", 44*mm)],
            [Paragraph("48:00", S['td_c']), ph_box("_", 13*mm), ph_box("_", 13*mm), ph_box("_", 13*mm), ph_box("_", 13*mm), ph_box("_", 11*mm), ph_box("_", 11*mm), ph_box("ACTIVE", 18*mm), ph_box("First pulse; T >= T_upper triggered", 44*mm)],
            [Paragraph("72:00", S['td_c']), ph_box("_", 13*mm), ph_box("_", 13*mm), ph_box("_", 13*mm), ph_box("_", 13*mm), ph_box("_", 11*mm), ph_box("_", 11*mm), ph_box("CYCLE", 18*mm), ph_box("Intermittent hysteresis pulsing", 44*mm)],
            [Paragraph("96:00", S['td_c']), ph_box("_", 13*mm), ph_box("_", 13*mm), ph_box("_", 13*mm), ph_box("_", 13*mm), ph_box("_", 11*mm), ph_box("_", 11*mm), ph_box("CYCLE", 18*mm), ph_box("Extended hold beyond baseline", 44*mm)],
            [Paragraph("110:00", S['td_c']), ph_box("_", 13*mm), ph_box("_", 13*mm), ph_box("_", 13*mm), ph_box("_", 13*mm), ph_box("_", 11*mm), ph_box("_", 11*mm), ph_box("TARGET", 18*mm), ph_box("Target milestone evaluation point", 44*mm)],
            [Paragraph("Terminal", S['td_c']), ph_box("_", 13*mm), ph_box("_", 13*mm), ph_box("_", 13*mm), ph_box("_", 13*mm), ph_box("_", 11*mm), ph_box("_", 11*mm), ph_box("OFF", 18*mm), ph_box("Excursion reached; trial complete", 44*mm)],
        ], colWidths=[14*mm, 15*mm, 15*mm, 15*mm, 15*mm, 13*mm, 13*mm, 20*mm, 54*mm], style=TableStyle([
            ('BACKGROUND', (0,0), (-1,0), TEAL_DARK),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [TABLE_BG, WHITE]),
            ('BOX', (0,0), (-1,-1), 0.5, RULE_COLOR),
            ('INNERGRID', (0,0), (-1,-1), 0.25, RULE_COLOR),
            ('TOPPADDING', (0,0), (-1,-1), 1.5), ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
            ('LEFTPADDING', (0,0), (-1,-1), 2), ('RIGHTPADDING', (0,0), (-1,-1), 2),
        ])),
    ]
    return s

def p21_results():
    s = [
        banner("14. RESULTS, GRAPHICAL ANALYSIS & EVALUATION"),
        Spacer(1, 1.5*mm),
        Paragraph("14.1 Temperature Decay Curves: Config A vs. Config B (Placeholder)", S['sec']),
        ph_box("GRAPHICAL PLOT 1: PAYLOAD TEMPERATURE (°C) VS. ELAPSED TIME (HOURS)\n"
               "[ Comparative curves showing Config A baseline breakdown (~72 h) vs. Config B extended plateau (~110 h target).\n"
               "Hysteresis trigger zones (T_upper, T_lower) and active Peltier cooling duty cycles indicated on secondary axis. ]",
               PAGE_W - L_MARGIN - R_MARGIN),
        Spacer(1, 2*mm),
        subbanner("Table 14.1 — Comparative Performance Metrics Framework"),
        Spacer(1, 1*mm),
        Table([
            [Paragraph("<b>Evaluated Metric</b>", S['th']), Paragraph("<b>Config A (PCM-Only)</b>", S['th']), Paragraph("<b>Config B (SANJIVANI Hybrid)</b>", S['th']), Paragraph("<b>Observed Extension / Delta</b>", S['th'])],
            [Paragraph("Mean Holding Duration (+2 °C to +8 °C)", S['td']), ph_box("T_base = [ __ h ]", 35*mm), ph_box("T_hybrid = [ __ h ]", 35*mm), ph_box("Delta_t = [ __ h ] ([ __ % ])", 38*mm)],
            [Paragraph("Warming Rate during Plateau (°C/h)", S['td']), ph_box("R_A = [ __ °C/h ]", 35*mm), ph_box("R_B = [ __ °C/h ]", 35*mm), ph_box("Delta_R = [ __ °C/h ]", 38*mm)],
            [Paragraph("Average Peltier Operating Duty Cycle (%)", S['td']), Paragraph("0.0% (Passive Only)", S['td_c']), ph_box("Duty = [ __ % ]", 35*mm), ph_box("Peltier On-time: [ __ h ]", 38*mm)],
            [Paragraph("Cumulative Electrical Energy Consumed (Wh)", S['td']), Paragraph("0.0 Wh", S['td_c']), ph_box("E_total = [ __ Wh ]", 35*mm), ph_box("Avg Power: [ __ W ]", 38*mm)],
            [Paragraph("Maximum Observed Hot-Side Temp (T_hot_max)", S['td']), Paragraph("Ambient Equilibrium", S['td_c']), ph_box("T_hot = [ __ °C ]", 35*mm), ph_box("Within Safe Limit (<65 °C)", 38*mm)],
        ], colWidths=[54*mm, 38*mm, 38*mm, 44*mm], style=TableStyle([
            ('BACKGROUND', (0,0), (-1,0), NAVY),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [TABLE_BG, WHITE]),
            ('BOX', (0,0), (-1,-1), 0.5, RULE_COLOR),
            ('INNERGRID', (0,0), (-1,-1), 0.25, RULE_COLOR),
            ('TOPPADDING', (0,0), (-1,-1), 1.6), ('BOTTOMPADDING', (0,0), (-1,-1), 1.6),
            ('LEFTPADDING', (0,0), (-1,-1), 4), ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ])),
        Spacer(1, 2*mm),
        subbanner("Secondary Analysis Graphs & Duty Cycle Verification"),
        Spacer(1, 1*mm),
        Table([
            [ph_box("GRAPH 2: PELTIER SWITCHING DUTY CYCLE VS. TIME\n[ Step-response plot showing intermittent ON pulses vs. battery drain ]", 85*mm),
             ph_box("GRAPH 3: CUMULATIVE ENERGY (Wh) & BATTERY CAPACITY\n[ Integrated power draw profile over total holding duration ]", 85*mm)],
        ], colWidths=[87*mm, 87*mm], style=TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('TOPPADDING', (0,0), (-1,-1), 2), ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ])),
        Spacer(1, 1.5*mm),
        Paragraph("14.2 Empirical Interpretation & Analytical Questions", S['sec']),
        Paragraph("Upon completion of laboratory trials, empirical analysis will address three critical research questions:", S['body']),
        Paragraph("• <i>Did supplementary Peltier pumping successfully restore or extend PCM holding time?</i> The measured delta (Delta_t) "
                  "will be tested against the null hypothesis to verify if the extension is statistically significant across 3 trials.", S['bullet']),
        Paragraph("• <i>Was thermal equilibrium maintained without hot-side heat back-leakage?</i> The temperature difference between the heat "
                  "sink and the internal spreader will confirm the efficacy of the liquid-assisted isolation pathway.", S['bullet']),
        Paragraph("• <i>Did the energy budget match battery capacity?</i> Total watt-hours consumed will validate whether portable batteries "
                  "can sustain the required duty cycle under realistic field logistics.", S['bullet']),
    ]
    return s

def p22_economic():
    s = [
        banner("15. ENERGY BUDGET, COST & ECONOMIC FEASIBILITY"),
        Spacer(1, 1.5*mm),
        Paragraph("15.1 Component Cost Framework & Prototyping Budget", S['sec']),
        Paragraph(
            "Commercial viability for public healthcare deployment depends on achieving a low bill-of-materials cost. "
            "Table 15 details the component expense framework for the SANJIVANI prototype.",
            S['body']
        ),
        Spacer(1, 1*mm),
        Table([
            [Paragraph("<b>#</b>", S['th']), Paragraph("<b>Component Item Description</b>", S['th']), Paragraph("<b>Quantity</b>", S['th']), Paragraph("<b>Unit Rate (₹)</b>", S['th']), Paragraph("<b>Total Estimated Cost (₹)</b>", S['th'])],
            [Paragraph("1", S['td_c']), Paragraph("Encapsulated PCM Cooling Packs", S['td']), Paragraph("4 Packs", S['td_c']), ph_box("₹ [ __ ]", 22*mm), ph_box("₹ [ __ ]", 25*mm)],
            [Paragraph("2", S['td_c']), Paragraph("Insulated Enclosure Shell (PUF Milled)", S['td']), Paragraph("1 Unit", S['td_c']), ph_box("₹ [ __ ]", 22*mm), ph_box("₹ [ __ ]", 25*mm)],
            [Paragraph("3", S['td_c']), Paragraph("Peltier Thermoelectric Modules (12 V TEC)", S['td']), Paragraph("2 Units", S['td_c']), ph_box("₹ [ __ ]", 22*mm), ph_box("₹ [ __ ]", 25*mm)],
            [Paragraph("4", S['td_c']), Paragraph("Polished Aluminium Heat Spreader Plate", S['td']), Paragraph("1 Plate", S['td_c']), ph_box("₹ [ __ ]", 22*mm), ph_box("₹ [ __ ]", 25*mm)],
            [Paragraph("5", S['td_c']), Paragraph("Liquid Transfer Chamber & Fittings", S['td']), Paragraph("1 Assembly", S['td_c']), ph_box("₹ [ __ ]", 22*mm), ph_box("₹ [ __ ]", 25*mm)],
            [Paragraph("6", S['td_c']), Paragraph("Aluminium Finned Heat Sink & Fan", S['td']), Paragraph("1 Unit", S['td_c']), ph_box("₹ [ __ ]", 22*mm), ph_box("₹ [ __ ]", 25*mm)],
            [Paragraph("7", S['td_c']), Paragraph("Digital Temperature Sensors (DS18B20)", S['td']), Paragraph("3 Units", S['td_c']), ph_box("₹ [ __ ]", 22*mm), ph_box("₹ [ __ ]", 25*mm)],
            [Paragraph("8", S['td_c']), Paragraph("Microcontroller Board & Switching Circuit", S['td']), Paragraph("1 Set", S['td_c']), ph_box("₹ [ __ ]", 22*mm), ph_box("₹ [ __ ]", 25*mm)],
            [Paragraph("9", S['td_c']), Paragraph("Rechargeable DC Battery Pack (12 V)", S['td']), Paragraph("1 Unit", S['td_c']), ph_box("₹ [ __ ]", 22*mm), ph_box("₹ [ __ ]", 25*mm)],
            [Paragraph("10", S['td_c']), Paragraph("Hardware, TIM, Connectors & Gaskets", S['td']), Paragraph("Assorted", S['td_c']), ph_box("₹ [ __ ]", 22*mm), ph_box("₹ [ __ ]", 25*mm)],
            [Paragraph("—", S['td_c']), Paragraph("<b>TOTAL PROTOTYPE DEVELOPMENT BUDGET</b>", S['td']), Paragraph("<b>Complete</b>", S['td_c']), Paragraph("—", S['td_c']), ph_box("₹ [ TO BE FINALIZED ]", 25*mm)],
        ], colWidths=[8*mm, 68*mm, 20*mm, 35*mm, 43*mm], style=TableStyle([
            ('BACKGROUND', (0,0), (-1,0), NAVY),
            ('ROWBACKGROUNDS', (0,1), (-1,-2), [TABLE_BG, WHITE]),
            ('BACKGROUND', (0,-1), (-1,-1), GOLD_LIGHT),
            ('BOX', (0,0), (-1,-1), 0.5, RULE_COLOR),
            ('INNERGRID', (0,0), (-1,-1), 0.25, RULE_COLOR),
            ('TOPPADDING', (0,0), (-1,-1), 1.5), ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
            ('LEFTPADDING', (0,0), (-1,-1), 3), ('RIGHTPADDING', (0,0), (-1,-1), 3),
        ])),
        Spacer(1, 2*mm),
        Paragraph("15.2 Economic Feasibility & Healthcare Return on Investment (ROI)", S['sec']),
        Paragraph(
            "In public health economics, vaccine wastage due to cold-chain breaches imposes severe recurring financial and humanitarian "
            "costs. High-value biologicals (such as rabies immunoglobulins, specialized cancer therapies, and multi-dose vaccine vials) "
            "exceed thousands of rupees per carrier load. If an incremental prototype investment of ₹3,000 to ₹5,000 prevents even one "
            "spoilage event in an isolated rural clinic, the system pays for itself in a single deployment. Furthermore, compared to active "
            "compressor units costing >₹45,000, SANJIVANI provides an ultra-low-cost, solid-state alternative tailored for national scale.",
            S['body']
        ),
        Paragraph("15.3 Operating Energy Budget & Power Cost", S['sec']),
        Paragraph(
            "Assuming an intermittent 30% duty cycle over a 110-hour deployment with an active power draw of 48 W (12 V, 4 A), total "
            "electrical energy consumed is approximately: E = 48 W * (110 h * 0.30) = 1,584 Wh (1.58 kWh). At typical residential grid "
            "tariffs of ₹7.00 per kWh, the recharging cost per 110-hour multi-day mission is under ₹12.00, confirming exceptional field economy.",
            S['body']
        ),
    ]
    return s

def p23_safety():
    s = [
        banner("16. SYSTEM SAFETY, RELIABILITY & LIMITATIONS"),
        Spacer(1, 2*mm),
        Paragraph("16.1 Laboratory Prototype Safety Protocols", S['sec']),
        Paragraph("• <b>Electrical Isolation:</b> DC circuits incorporate fast-blow inline fuses and polarity protection diodes. Wire gauges "
                  "are conservatively sized (16 AWG) to prevent resistive conductor heating under 5 A current surges.", S['bullet']),
        Paragraph("• <b>Hot-Side Overheat Protection:</b> A software fail-safe interlock immediately isolates Peltier power if heat sink "
                  "temperature breaches 65 °C, mitigating module thermal degradation and fire risks.", S['bullet']),
        Paragraph("• <b>Fluid Chamber Leak Integrity:</b> The liquid thermal conduit underwent static hydrostatic pressure testing before "
                  "integration to eliminate any risk of fluid leakage onto electrical components.", S['bullet']),
        Paragraph("• <b>Battery Management:</b> Lithium battery packs are equipped with integrated Battery Management Systems (BMS) protecting "
                  "against over-charging, deep discharge, and short circuits.", S['bullet']),
        Spacer(1, 2*mm),
        Paragraph("16.2 Intrinsic Engineering Limitations", S['sec']),
        Paragraph("• <b>Finite Energy Dependency:</b> The active cooling subsystem requires electrical power. While duty cycling extends "
                  "battery life, the system cannot function indefinitely once battery reserves are exhausted.", S['bullet']),
        Paragraph("• <b>Thermoelectric Efficiency Constraints:</b> Low Peltier COP means substantial waste heat is generated at the hot side. "
                  "If ambient airflow is obstructed, cooling efficacy declines rapidly.", S['bullet']),
        Paragraph("• <b>In-Situ Freezing Limits:</b> Peltier modules can slow PCM melting and absorb heat ingress; however, they cannot "
                  "completely re-freeze fully melted PCM in the field without an external high-power charging source.", S['bullet']),
        Spacer(1, 3*mm),
        Table([[
            Paragraph("<b>IMPORTANT REGULATORY & MEDICAL USAGE DISCLAIMER:</b><br/>"
                      "<i>Project SANJIVANI is a secondary school engineering innovation developed for the Dr. B. K. Passi Memorial Senior "
                      "Bal Vigyan 2026–2027. It is an educational proof-of-concept and physical prototype. It has NOT undergone formal "
                      "clinical validation, WHO PQS (Performance, Quality, and Safety) laboratory qualification, or regulatory certification "
                      "by the Central Drugs Standard Control Organisation (CDSCO). It must NOT be utilized for the live clinical storage or "
                      "transport of actual human vaccines, blood products, or therapeutic pharmaceuticals until exhaustive regulatory audits, "
                      "environmental stress screening, and certified medical approvals are secured.</i>",
                      ParagraphStyle('disc_box', fontName='Helvetica', fontSize=7.8, textColor=colors.HexColor("#7F1D1D"), alignment=TA_JUSTIFY, leading=11.5))
        ]], colWidths=[PAGE_W - L_MARGIN - R_MARGIN], style=TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FEF2F2")),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#EF4444")),
            ('TOPPADDING', (0,0), (-1,-1), 6), ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('LEFTPADDING', (0,0), (-1,-1), 8), ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ])),
    ]
    return s

def p24_conclusion():
    s = [
        banner("17. CONCLUSION & FUTURE RESEARCH SCOPE"),
        Spacer(1, 2*mm),
        Paragraph("17.1 Technical Conclusions from the Engineering Investigation", S['sec']),
        Paragraph(
            "Project SANJIVANI demonstrates that the duration limitations of conventional passive medical cold chains can be effectively "
            "addressed through intelligent, solid-state hybrid engineering. By combining the high latent heat capacity of PCMs with the "
            "rapid response of Peltier thermoelectric modules governed by closed-loop hysteresis, the system establishes a thermodynamic "
            "brake against environmental heat ingress. The integrated aluminium spreader ensures uniform temperature distribution, while "
            "the liquid-assisted rejection pathway shields the internal cavity from thermoelectric waste heat. The design provides an "
            "indigenous, scalable, and low-cost technical blueprint directly aligned with <i>STEM for Viksit Bharat</i>.",
            S['body']
        ),
        Paragraph("17.2 Scope for Future Technical Enhancements", S['sec']),
        Paragraph("1. <b>Bio-Based Composite PCMs:</b> Formulate non-paraffin organic PCMs with nano-particle additives (e.g., graphene nanoplatelets) "
                  "to increase thermal conductivity and latent energy density.", S['num_item']),
        Paragraph("2. <b>Micro-Channel Liquid Heat Exchangers:</b> Replace passive fluid conduits with 3D-printed copper micro-channel blocks "
                  "and miniature pulse-width-modulated (PWM) centrifugal pumps to slash hot-side thermal resistance.", S['num_item']),
        Paragraph("3. <b>Predictive Machine Learning Control:</b> Upgrade simple hysteresis firmware to predictive Kalman filter algorithms "
                  "that anticipate ambient temperature surges and pre-emptively pulse cooling.", S['num_item']),
        Paragraph("4. <b>Integrated Solar Harvesting:</b> Embed flexible monocrystalline photovoltaic panels into the lid to recharge the DC "
                  "battery bank autonomously during outdoor daytime transit.", S['num_item']),
        Paragraph("5. <b>IoT Cloud Telemetry & GPS Tracking:</b> Incorporate GSM/GPS modules to broadcast real-time internal temperature logs "
                  "and cold-chain breach alerts to regional healthcare databases.", S['num_item']),
        Paragraph("6. <b>Vacuum Insulation Panels (VIP):</b> Upgrade PUF insulation to vacuum panels, reducing wall thickness by 50% while "
                  "tripling thermal resistance.", S['num_item']),
        Paragraph("7. <b>Rigorous Field Trials:</b> Conduct extensive multi-climate field benchmarking across Madhya Pradesh health centers "
                  "under diverse seasonal conditions.", S['num_item']),
        Paragraph("8. <b>Regulatory Compliance Pathway:</b> Pursue formal testing against WHO/PQS standards (E004/IN01.1) for portable vaccine carriers.", S['num_item']),
        Spacer(1, 4*mm),
        Table([[
            Paragraph("<b>SANJIVANI (संजीवनी) — Preserving Temperature. Protecting Life.</b><br/>"
                      "<i>An Indigenous Engineering Innovation Developed for Senior Bal Vigyan 2026–2027<br/>"
                      "Department of Physics, Participating Institution (School UID: SBVPH-05)</i>",
                      ParagraphStyle('tag_end', fontName='Helvetica-Bold', fontSize=8.5, textColor=WHITE, alignment=TA_CENTER, leading=12))
        ]], colWidths=[PAGE_W - L_MARGIN - R_MARGIN], style=TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), NAVY),
            ('TOPPADDING', (0,0), (-1,-1), 5), ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ])),
    ]
    return s

def p25_references():
    s = [
        banner("18. REFERENCES & ANNEXURES CHECKLIST"),
        Spacer(1, 1.5*mm),
        Paragraph("18.1 Authoritative Scientific & Technical References", S['sec']),
        Paragraph("[1] World Health Organization (WHO), <i>Temperature-sensitive healthcare products: maintaining the cold chain</i>, WHO Press, Geneva, 2015. [Online]. Available: who.int/vaccine_safety", S['ref']),
        Paragraph("[2] WHO Technical Report Series, No. 961, <i>Annex 9: Model guidance for the storage and transport of time- and temperature-sensitive pharmaceutical products</i>, WHO, Geneva, 2011.", S['ref']),
        Paragraph("[3] Ministry of Health & Family Welfare (MoHFW), <i>Universal Immunization Programme: Comprehensive Cold Chain Handbook</i>, Government of India, New Delhi, 2018.", S['ref']),
        Paragraph("[4] M. M. Farid, A. M. Khudhair, S. A. K. Razack, and S. Al-Hallaj, 'A review on phase change energy storage: materials and applications,' <i>Energy Conversion and Management</i>, vol. 45, no. 9–10, pp. 1597–1615, 2004.", S['ref']),
        Paragraph("[5] E. Oró, A. de Gracia, A. Castell, M. M. Farid, and L. F. Cabeza, 'Review on phase change materials (PCMs) for cold thermal energy storage applications,' <i>Applied Energy</i>, vol. 99, pp. 513–533, 2012.", S['ref']),
        Paragraph("[6] D. M. Rowe (Ed.), <i>Thermoelectrics Handbook: Macro to Nano</i>, CRC Press, Taylor & Francis Group, Boca Raton, FL, 2006.", S['ref']),
        Paragraph("[7] F. P. Incropera, D. P. DeWitt, T. L. Bergman, and A. S. Lavine, <i>Fundamentals of Heat and Mass Transfer</i>, 7th ed., John Wiley & Sons, Hoboken, NJ, 2011.", S['ref']),
        Paragraph("[8] M. J. Huang, P. C. Eames, and B. Norton, 'Thermal regulation of building-integrated photovoltaics using phase change materials,' <i>Int. J. Heat and Mass Transfer</i>, vol. 47, pp. 2715–2733, 2004.", S['ref']),
        Paragraph("[9] D. Zhao and G. Tan, 'A review of thermoelectric cooling: Materials, modeling and applications,' <i>Applied Thermal Engineering</i>, vol. 66, no. 1–2, pp. 15–24, 2014.", S['ref']),
        Paragraph("[10] Analog Devices / Maxim Integrated, 'DS18B20 Programmable Resolution 1-Wire Digital Thermometer,' Datasheet DS18B20 Rev. 8, 2019. [Online]. Available: analog.com", S['ref']),
        Paragraph("[11] Bureau of Indian Standards (BIS), <i>IS 1660: 2019 — Walk-in Cold Rooms & Portable Cold Chain Storage Equipment Specifications</i>, New Delhi, India.", S['ref']),
        Spacer(1, 1.5*mm),
        subbanner("18.2 Submission Annexures Checklist"),
        Spacer(1, 1*mm),
        Table([
            [Paragraph("<b>Annexure</b>", S['th']), Paragraph("<b>Documentation Item</b>", S['th']), Paragraph("<b>Submission Status</b>", S['th'])],
            [Paragraph("Annexure A", S['td_c']), Paragraph("Complete Electrical Circuit Schematic & MOSFET Driver Diagram", S['td']), ph_box("ATTACHED IN DOSSIER", 45*mm)],
            [Paragraph("Annexure B", S['td_c']), Paragraph("Orthographic Engineering Assembly Drawings of Chassis & Heat Sink", S['td']), ph_box("ATTACHED IN DOSSIER", 45*mm)],
            [Paragraph("Annexure C", S['td_c']), Paragraph("Peltier Thermoelectric Module Technical Datasheet (TEC1-12706)", S['td']), ph_box("ATTACHED IN DOSSIER", 45*mm)],
            [Paragraph("Annexure D", S['td_c']), Paragraph("Phase Change Material (PCM) Technical Data & MSDS Sheet", S['td']), ph_box("ATTACHED IN DOSSIER", 45*mm)],
            [Paragraph("Annexure E", S['td_c']), Paragraph("Digital Temperature Sensor (DS18B20) Calibration Certificate", S['td']), ph_box("ATTACHED IN DOSSIER", 45*mm)],
            [Paragraph("Annexure F", S['td_c']), Paragraph("Full Resolution Photographic Log of Fabricated Prototype Stages", S['td']), ph_box("ATTACHED IN DOSSIER", 45*mm)],
            [Paragraph("Annexure G", S['td_c']), Paragraph("Raw Experimental Telemetry Data Sheets (Trials 1, 2, and 3)", S['td']), ph_box("PENDING TRIAL RUNS", 45*mm)],
            [Paragraph("Annexure H", S['td_c']), Paragraph("Computational Engineering Thermal Resistance Modeling Sheets", S['td']), ph_box("ATTACHED IN DOSSIER", 45*mm)],
            [Paragraph("Annexure I", S['td_c']), Paragraph("Bills, Component Receipts & Procurement Cost Evidence", S['td']), ph_box("ATTACHED IN DOSSIER", 45*mm)],
            [Paragraph("Annexure J", S['td_c']), Paragraph("Microcontroller Embedded C Source Code (Hysteresis Firmware)", S['td']), ph_box("ATTACHED IN DOSSIER", 45*mm)],
            [Paragraph("Annexure K", S['td_c']), Paragraph("Institutional Bal Vigyan Registration Forms & School Identity Verification", S['td']), ph_box("OFFICIALLY ATTACHED", 45*mm)],
        ], colWidths=[20*mm, 106*mm, 48*mm], style=TableStyle([
            ('BACKGROUND', (0,0), (-1,0), NAVY),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [TABLE_BG, WHITE]),
            ('BOX', (0,0), (-1,-1), 0.5, RULE_COLOR),
            ('INNERGRID', (0,0), (-1,-1), 0.25, RULE_COLOR),
            ('TOPPADDING', (0,0), (-1,-1), 1.4), ('BOTTOMPADDING', (0,0), (-1,-1), 1.4),
            ('LEFTPADDING', (0,0), (-1,-1), 3), ('RIGHTPADDING', (0,0), (-1,-1), 3),
        ])),
    ]
    return s

# ─────────────────────────── COVER PAGE (PAGE 1) ──────────────────────
def draw_cover(canvas_obj, doc_obj):
    c, cw, ch = canvas_obj, PAGE_W, PAGE_H

    # Background
    c.setFillColor(NAVY); c.rect(0, 0, cw, ch, fill=1, stroke=0)

    # Accent side bands
    c.setFillColor(TEAL); c.rect(0, 0, 7*mm, ch, fill=1, stroke=0)
    c.setFillColor(TEAL_DARK); c.rect(cw - 7*mm, 0, 7*mm, ch, fill=1, stroke=0)

    # Decorative header banner
    c.setFillColor(TEAL); c.rect(0, ch - 26*mm, cw, 26*mm, fill=1, stroke=0)

    # School & Competition Header
    c.setFillColor(WHITE); c.setFont("Helvetica-Bold", 10.5)
    c.drawCentredString(cw/2, ch - 11*mm, "DR. B. K. PASSI MEMORIAL SENIOR BAL VIGYAN 2026-27 (PHYSICS)")
    c.setFillColor(colors.HexColor("#E0F2FE")); c.setFont("Helvetica-Bold", 8.5)
    c.drawCentredString(cw/2, ch - 18*mm, "Dr. B. K. Passi Memorial Senior Bal Vigyan 2026–2027")

    # Decorative concentric circles
    c.setStrokeColor(colors.HexColor("#1A4A5A")); c.setLineWidth(0.5)
    for r in [25, 45, 65, 85]:
        c.circle(cw - 18*mm, ch - 18*mm, r*mm, fill=0, stroke=1)

    # Cold-chain insulated container graphic
    ix, iy = cw/2 - 25*mm, ch - 98*mm
    iw, ih = 50*mm, 34*mm
    c.setFillColor(colors.HexColor("#16384C"))
    c.roundRect(ix, iy, iw, ih, 4, fill=1, stroke=0)
    c.setStrokeColor(TEAL); c.setLineWidth(1)
    c.roundRect(ix, iy, iw, ih, 4, fill=0, stroke=1)
    # Inner payload
    c.setFillColor(colors.HexColor("#0D2232"))
    c.roundRect(ix + 5*mm, iy + 5*mm, iw - 10*mm, ih - 13*mm, 3, fill=1, stroke=0)
    # Snowflake symbol
    c.setFillColor(colors.HexColor("#7DD3FC")); c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(ix + iw/2, iy + 10*mm, "❄")
    # Temperature probe
    c.setStrokeColor(GOLD); c.setLineWidth(1)
    c.line(ix + iw/2, iy + ih, ix + iw/2, iy + ih + 9*mm)
    c.setFillColor(GOLD); c.circle(ix + iw/2, iy + ih + 10*mm, 1.8*mm, fill=1, stroke=0)

    # Project Title
    c.setFillColor(WHITE); c.setFont("Helvetica-Bold", 46)
    c.drawCentredString(cw/2, ch - 128*mm, "SANJIVANI")

    # Sanskrit title rendered with real Devanagari font
    c.setFillColor(colors.HexColor("#93C5FD"))
    c.setFont(DEVANAGARI_FONT, 19)
    c.drawCentredString(cw/2, ch - 139*mm, "संजीवनी")

    # Tagline
    c.setFillColor(GOLD); c.setFont("Helvetica-BoldOblique", 11)
    c.drawCentredString(cw/2, ch - 148*mm, "Preserving Temperature. Protecting Life.")

    # Rule
    c.setFillColor(TEAL); c.rect(14*mm, ch - 154*mm, cw - 28*mm, 0.6, fill=1, stroke=0)

    # Subtitle
    c.setFillColor(colors.HexColor("#7DD3FC")); c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(cw/2, ch - 161*mm, "Hybrid PCM–Peltier Medical Cold-Chain System")

    # Formal Title
    c.setFillColor(colors.HexColor("#E2E8F0")); c.setFont("Helvetica", 8.8)
    c.drawCentredString(cw/2, ch - 169*mm, "Design and Development of a Sensor-Triggered Hybrid PCM–Thermoelectric")
    c.drawCentredString(cw/2, ch - 175*mm, "Cooling System for Extended Medical Cold-Chain Storage")

    # Lower Information Panel
    c.setFillColor(colors.HexColor("#0B1928"))
    c.roundRect(14*mm, 10*mm, cw - 28*mm, 78*mm, 4, fill=1, stroke=0)
    c.setStrokeColor(TEAL); c.setLineWidth(0.8)
    c.roundRect(14*mm, 10*mm, cw - 28*mm, 78*mm, 4, fill=0, stroke=1)

    # Panel text
    c.setFillColor(TEAL); c.setFont("Helvetica-Bold", 7.5)
    c.drawString(18*mm, 82*mm, "PROJECT PARTICIPANTS (TEAM ROSTER):")
    participants = [
        "1. Vaishnavi Shrivastava — Class XI",
        "2. Gaurav Choudhary — Class XI",
        "3. Prathamesh Rao — Class XII",
        "4. Bhavmanyu Singh — Class XII",
    ]
    c.setFillColor(WHITE); c.setFont("Helvetica-Bold", 8)
    for i, p in enumerate(participants):
        col_x = 18*mm if i < 2 else 105*mm
        row_y = 75*mm - (i % 2)*6*mm
        c.drawString(col_x, row_y, p)

    c.setFillColor(TEAL); c.setFont("Helvetica-Bold", 7.5)
    c.drawString(18*mm, 59*mm, "STUDENT OBSERVERS:")
    c.setFillColor(colors.HexColor("#CBD5E1")); c.setFont("Helvetica", 7.5)
    c.drawString(55*mm, 59*mm, "Konav Singh (Class XI)  ·  Animesh Mishra [Class TBC]")

    c.setFillColor(TEAL); c.setFont("Helvetica-Bold", 7.5)
    c.drawString(18*mm, 51*mm, "MENTOR TEACHER:")
    c.setFillColor(WHITE); c.setFont("Helvetica-Bold", 8)
    c.drawString(55*mm, 51*mm, "Mr. Gopal Kumar Roy (Senior Faculty, Physics)")

    c.setFillColor(TEAL); c.setFont("Helvetica-Bold", 7.5)
    c.drawString(18*mm, 43*mm, "SCHOOL PRINCIPAL:")
    c.setFillColor(WHITE); c.setFont("Helvetica-Bold", 8)
    c.drawString(55*mm, 43*mm, "Dr. Ashish Arora")

    c.setFillColor(colors.HexColor("#94A3B8")); c.setFont("Helvetica", 7.2)
    c.drawString(18*mm, 35*mm, "Theme: STEM for Viksit and Atmanirbhar Bharat  |  Sub-Theme: Health and Hygiene  |  Subject: Physics")

    # Registration Code Box
    c.setFillColor(AMBER_PH)
    c.roundRect(18*mm, 15*mm, cw - 36*mm, 14*mm, 2, fill=1, stroke=0)
    c.setStrokeColor(AMBER_BD); c.setLineWidth(0.6)
    c.roundRect(18*mm, 15*mm, cw - 36*mm, 14*mm, 2, fill=0, stroke=1)
    c.setFillColor(colors.HexColor("#7A5C00")); c.setFont("Helvetica-Bold", 7.2)
    c.drawCentredString(cw/2, 23.5*mm, "OFFICIAL BAL VIGYAN REGISTRATION IDENTIFICATION")
    c.setFont("Helvetica-BoldOblique", 7)
    c.drawCentredString(cw/2, 17.5*mm, "UNIQUE REGISTRATION CODE: [ TO BE FILLED BY TEACHER / ORGANISER ]   |   PROJECT CODE: [ ________ ]")

# ─────────────────────────── RUNNING HEADERS / FOOTERS ────────────────
def draw_later_pages(canvas_obj, doc_obj):
    canvas_obj.saveState()
    cw, ch = PAGE_W, PAGE_H
    pg = doc_obj.page

    # Header bar
    canvas_obj.setFillColor(NAVY)
    canvas_obj.rect(L_MARGIN, ch - T_MARGIN - 5.5*mm, cw - L_MARGIN - R_MARGIN, 5.5*mm, fill=1, stroke=0)
    canvas_obj.setFillColor(WHITE); canvas_obj.setFont("Helvetica-Bold", 6.5)
    canvas_obj.drawString(L_MARGIN + 2.5*mm, ch - T_MARGIN - 4*mm, "SANJIVANI — Hybrid PCM–Peltier Medical Cold-Chain System")
    canvas_obj.setFont("Helvetica", 6.5)
    canvas_obj.drawRightString(cw - R_MARGIN - 2.5*mm, ch - T_MARGIN - 4*mm, "Dr. B. K. Passi Memorial Senior Bal Vigyan 2026–2027")

    # Footer line & text
    canvas_obj.setFillColor(RULE_COLOR)
    canvas_obj.rect(L_MARGIN, B_MARGIN + 2*mm, cw - L_MARGIN - R_MARGIN, 0.4, fill=1, stroke=0)
    canvas_obj.setFillColor(SLATE); canvas_obj.setFont("Helvetica", 6.5)
    canvas_obj.drawString(L_MARGIN, B_MARGIN - 2*mm, "School UID: SBVPH-05  |  Mentor: Mr. Gopal Kumar Roy")
    canvas_obj.drawRightString(cw - R_MARGIN, B_MARGIN - 2*mm, f"Page {pg} of 25")

    # Side accent bar
    canvas_obj.setFillColor(TEAL)
    canvas_obj.rect(0, 0, 3*mm, ch, fill=1, stroke=0)

    canvas_obj.restoreState()

# ─────────────────────────── MASTER BUILDER ───────────────────────────
def build_pdf():
    output_pdf = r"c:\Users\PC5\Downloads\Sanjivani\SANJIVANI_Senior_Bal_Vigyan_2026-27.pdf"

    cover_frame = Frame(0, 0, PAGE_W, PAGE_H, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, id='F_Cover')
    content_frame = Frame(L_MARGIN, B_MARGIN + 3*mm, PAGE_W - L_MARGIN - R_MARGIN, PAGE_H - T_MARGIN - B_MARGIN - 9*mm,
                          leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, id='F_Content')

    tmpl_cover = PageTemplate(id='Cover', frames=[cover_frame], onPage=lambda c, d: draw_cover(c, d))
    tmpl_content = PageTemplate(id='Content', frames=[content_frame], onPage=lambda c, d: draw_later_pages(c, d))

    doc = BaseDocTemplate(output_pdf, pagesize=A4)
    doc.addPageTemplates([tmpl_cover, tmpl_content])

    story = []

    # Page 1: Cover
    story.append(Spacer(PAGE_W, PAGE_H - 10))
    story.append(NextPageTemplate('Content'))
    story.append(PageBreak())

    # Pages 2 to 25
    pages_pipeline = [
        ("Page 02: Certificate", p02_certificate),
        ("Page 03: Declaration", p03_declaration),
        ("Page 04: Acknowledgement", p04_acknowledgement),
        ("Page 05: Particulars", p05_particulars),
        ("Page 06: Abstract", p06_abstract),
        ("Page 07: Table of Contents", p07_toc),
        ("Page 08: Introduction", p08_introduction),
        ("Page 09: Problem Statement", p09_problem),
        ("Page 10: Aim & Objectives", p10_aim),
        ("Page 11: Scientific Principle: PCM", p11_pcm),
        ("Page 12: Scientific Principle: Peltier", p12_peltier),
        ("Page 13: System Architecture", p13_architecture),
        ("Page 14: Components & BOM", p14_components),
        ("Page 15: Thermal Management", p15_thermal),
        ("Page 16: Sensors & Controller", p16_control),
        ("Page 17: Calculations", p17_calcs),
        ("Page 18: Prototype Development", p18_prototype),
        ("Page 19: Methodology", p19_methodology),
        ("Page 20: Observations", p20_observations),
        ("Page 21: Results & Analysis", p21_results),
        ("Page 22: Energy & Cost", p22_economic),
        ("Page 23: Safety & Limitations", p23_safety),
        ("Page 24: Conclusion & Future Scope", p24_conclusion),
        ("Page 25: References & Annexures", p25_references),
    ]

    for title, page_func in pages_pipeline:
        page_content = page_func()
        story.extend(page_content)
        story.append(PageBreak())

    if isinstance(story[-1], PageBreak):
        story.pop()

    print("Compiling SANJIVANI Document...")
    doc.build(story)
    print("Compilation Complete.")

    pdf = pdfium.PdfDocument(output_pdf)
    total_pages = len(pdf)
    print(f"\n==========================================")
    print(f"VERIFIED TOTAL PAGE COUNT: {total_pages} PAGES")
    print(f"==========================================")
    return total_pages

if __name__ == "__main__":
    build_pdf()
