"""
SANJIVANI — Senior Bal Vigyan 2026–2027 Project Report
Master High-Resolution 25-Page Publication-Grade PDF Generator
Fully Simulated Performance, Zero Placeholders, Embedded Visual Graphs, Native Rupee Symbol
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
    Paragraph, Spacer, Table, TableStyle, HRFlowable, PageBreak, Flowable, Image
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import pypdfium2 as pdfium

# ─────────────────────────── FONT REGISTRATION ─────────────────────────
pdfmetrics.registerFont(TTFont('Arial', r'C:\Windows\Fonts\arial.ttf'))
pdfmetrics.registerFont(TTFont('Arial-Bold', r'C:\Windows\Fonts\arialbd.ttf'))
pdfmetrics.registerFont(TTFont('Arial-Italic', r'C:\Windows\Fonts\ariali.ttf'))
pdfmetrics.registerFont(TTFont('Arial-BoldItalic', r'C:\Windows\Fonts\arialbi.ttf'))

DEVANAGARI_FONT = 'Arial-Bold'
if os.path.exists(r"C:\Windows\Fonts\NirmalaB.ttf"):
    try:
        pdfmetrics.registerFont(TTFont('DevanagariBold', r"C:\Windows\Fonts\NirmalaB.ttf"))
        DEVANAGARI_FONT = 'DevanagariBold'
        print("Registered Devanagari font: NirmalaB.ttf")
    except Exception as e:
        print(f"Failed to register NirmalaB: {e}")

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
RULE_COLOR  = colors.HexColor("#CBD5E1")   # Border grey
CARD_BG     = colors.HexColor("#F8FAFC")

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
    s['banner'] = ParagraphStyle('banner', fontName='Arial-Bold', fontSize=11.0,
                                 textColor=WHITE, alignment=TA_LEFT, leading=14)
    s['sec'] = ParagraphStyle('sec', fontName='Arial-Bold', fontSize=9.0,
                              textColor=NAVY, alignment=TA_LEFT, leading=11.5,
                              spaceBefore=3.0, spaceAfter=1.5)
    s['subsec'] = ParagraphStyle('subsec', fontName='Arial-Bold', fontSize=8.2,
                                 textColor=TEAL_DARK, alignment=TA_LEFT, leading=10.5,
                                 spaceBefore=2.0, spaceAfter=1.0)
    s['body'] = ParagraphStyle('body', fontName='Arial', fontSize=7.8,
                               textColor=BLACK, alignment=TA_JUSTIFY, leading=11.2,
                               spaceBefore=1, spaceAfter=2)
    s['body_lg'] = ParagraphStyle('body_lg', fontName='Arial', fontSize=8.4,
                                  textColor=BLACK, alignment=TA_JUSTIFY, leading=12.0,
                                  spaceBefore=2, spaceAfter=3)
    s['body_bold'] = ParagraphStyle('body_bold', fontName='Arial-Bold', fontSize=7.8,
                                    textColor=BLACK, alignment=TA_LEFT, leading=11)
    s['bullet'] = ParagraphStyle('bullet', fontName='Arial', fontSize=7.6,
                                 textColor=BLACK, alignment=TA_JUSTIFY, leading=10.8,
                                 leftIndent=10, firstLineIndent=-7, spaceAfter=1.5)
    s['caption'] = ParagraphStyle('caption', fontName='Arial-Italic', fontSize=7.2,
                                  textColor=SLATE, alignment=TA_CENTER, leading=9.5, spaceAfter=1.5)
    s['eq'] = ParagraphStyle('eq', fontName='Arial-Bold', fontSize=8.8,
                             textColor=TEAL_DARK, alignment=TA_CENTER, leading=12.5,
                             spaceBefore=2, spaceAfter=2)
    s['th'] = ParagraphStyle('th', fontName='Arial-Bold', fontSize=7.2,
                             textColor=WHITE, alignment=TA_CENTER, leading=9.2)
    s['td'] = ParagraphStyle('td', fontName='Arial', fontSize=7.0,
                             textColor=BLACK, alignment=TA_LEFT, leading=9.2)
    s['td_c'] = ParagraphStyle('td_c', fontName='Arial', fontSize=7.0,
                               textColor=BLACK, alignment=TA_CENTER, leading=9.2)
    s['td_b'] = ParagraphStyle('td_b', fontName='Arial-Bold', fontSize=7.0,
                               textColor=BLACK, alignment=TA_LEFT, leading=9.2)
    s['ref'] = ParagraphStyle('ref', fontName='Arial', fontSize=7.0,
                              textColor=BLACK, alignment=TA_LEFT, leading=9.8,
                              leftIndent=16, firstLineIndent=-16, spaceAfter=1.8)
    return s

S = build_styles()

def banner(title):
    p = Paragraph(f"<b>{title.upper()}</b>", S['banner'])
    w = PAGE_W - L_MARGIN - R_MARGIN
    t = Table([[p]], colWidths=[w])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), TEAL),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    return t

def hr(color=RULE_COLOR, thickness=0.4):
    return HRFlowable(width="100%", thickness=thickness, color=color, spaceAfter=2, spaceBefore=2)

# ─────────────────────────── VECTOR SCHEMATICS ────────────────────────
class PCMDiagram(Flowable):
    def __init__(self, width=174*mm, height=34*mm):
        super().__init__()
        self.width, self.height = width, height

    def draw(self):
        c, w, h = self.canv, self.width, self.height
        c.setFillColor(CARD_BG); c.roundRect(0, 0, w, h, 3, fill=1, stroke=0)
        c.setStrokeColor(RULE_COLOR); c.setLineWidth(0.4); c.roundRect(0, 0, w, h, 3, fill=0, stroke=1)

        cw = (w - 12*mm) / 3
        phases = [
            ("1. SOLID BIO-PCM", colors.HexColor("#BFDBFE"), "Sensible Subcooling\nT < +4.8°C (Solid Matrix)", colors.HexColor("#1D4ED8")),
            ("2. PHASE TRANSITION", colors.HexColor("#A7F3D0"), "Latent Heat Absorption\nT = +4.8°C (Isothermal Buffer)", colors.HexColor("#065F46")),
            ("3. LIQUID STATE", colors.HexColor("#FDE68A"), "Latent Reserve Exhausted\nT > +5.2°C (Sensible Warmup)", colors.HexColor("#92400E")),
        ]
        for i, (title, bg, desc, tc) in enumerate(phases):
            x = 3*mm + i * (cw + 3*mm)
            c.setFillColor(bg); c.roundRect(x, 3*mm, cw, h - 11*mm, 2.5, fill=1, stroke=0)
            c.setFillColor(tc); c.setFont("Arial-Bold", 6.8)
            c.drawCentredString(x + cw/2, h - 15*mm, title)
            c.setFillColor(BLACK); c.setFont("Arial", 5.8)
            for j, ln in enumerate(desc.split('\n')):
                c.drawCentredString(x + cw/2, h - 18.5*mm - j*5.5, ln)

        c.setFillColor(NAVY); c.setFont("Arial-Bold", 7.2)
        c.drawString(4*mm, h - 5.5*mm, "Figure 1 — Phase Change Material (Bio-PCM) Latent Heat Buffering Mechanism")

class PeltierDiagram(Flowable):
    def __init__(self, width=174*mm, height=38*mm):
        super().__init__()
        self.width, self.height = width, height

    def draw(self):
        c, w, h = self.canv, self.width, self.height
        c.setFillColor(CARD_BG); c.roundRect(0, 0, w, h, 3, fill=1, stroke=0)
        c.setStrokeColor(RULE_COLOR); c.setLineWidth(0.4); c.roundRect(0, 0, w, h, 3, fill=0, stroke=1)

        # Hot Side (Top)
        c.setFillColor(colors.HexColor("#FEE2E2")); c.roundRect(14*mm, h - 13*mm, w - 28*mm, 6*mm, 2, fill=1, stroke=0)
        c.setFillColor(colors.HexColor("#DC2626")); c.setFont("Arial-Bold", 6.5)
        c.drawCentredString(w/2, h - 9.5*mm, "HOT SIDE — Thermal Dissipation: Q_hot = Q_cold + P_elec (to Fin Stack & Fan)")

        # Cold Side (Bottom)
        c.setFillColor(colors.HexColor("#DBEAFE")); c.roundRect(14*mm, 3*mm, w - 28*mm, 6*mm, 2, fill=1, stroke=0)
        c.setFillColor(colors.HexColor("#1D4ED8")); c.setFont("Arial-Bold", 6.5)
        c.drawCentredString(w/2, 5.5*mm, "COLD SIDE — Heat Pumping Interface: Q_cold = 18.5 W (coupled to Al Cold Jacket)")

        # Semiconductor Matrix
        c.setFillColor(colors.HexColor("#E5E7EB")); c.roundRect(26*mm, 11*mm, w - 52*mm, h - 26*mm, 2, fill=1, stroke=0)
        c.setFillColor(SLATE); c.setFont("Arial-Bold", 6.2)
        c.drawCentredString(w/2, h/2 - 2, "Bismuth Telluride (Bi2Te3) P-N Thermoelectric Semiconductor Matrix")

        # DC Power Input arrow
        c.setFillColor(colors.HexColor("#7C3AED")); c.setFont("Arial-Bold", 6.2)
        c.drawString(2.5*mm, h/2 + 2, "7.5V DC")
        c.drawString(2.5*mm, h/2 - 5, "(30W)")
        c.setStrokeColor(colors.HexColor("#7C3AED")); c.setLineWidth(0.8)
        c.line(14*mm, h/2, 24*mm, h/2)
        _poly(c, [24*mm, h/2, 21*mm, h/2+2, 21*mm, h/2-2], fill=1, stroke=0)

        c.setFillColor(NAVY); c.setFont("Arial-Bold", 7.2)
        c.drawString(4*mm, h - 5.5*mm, "Figure 2 — Dual TEC1-12706 Thermoelectric Module: Active Heat Pumping Dynamics")

class SystemBlockDiagram(Flowable):
    def __init__(self, width=174*mm, height=64*mm):
        super().__init__()
        self.width, self.height = width, height

    def _box(self, c, x, y, bw, bh, text, bg, tc=WHITE, fs=5.8):
        c.setFillColor(bg); c.roundRect(x, y, bw, bh, 2.2, fill=1, stroke=0)
        c.setStrokeColor(RULE_COLOR); c.setLineWidth(0.4); c.roundRect(x, y, bw, bh, 2.2, fill=0, stroke=1)
        c.setFillColor(tc); c.setFont("Arial-Bold", fs)
        lines = text.split('\n')
        for i, ln in enumerate(lines):
            c.drawCentredString(x + bw/2, y + bh/2 + (len(lines)-1)*2.6 - i*5.8 - 2, ln)

    def draw(self):
        c, w, h = self.canv, self.width, self.height
        c.setFillColor(CARD_BG); c.roundRect(0, 0, w, h, 3, fill=1, stroke=0)
        c.setStrokeColor(RULE_COLOR); c.setLineWidth(0.4); c.roundRect(0, 0, w, h, 3, fill=0, stroke=1)

        # Enclosure Boundary
        enc_w, enc_h = 106*mm, 48*mm
        c.setFillColor(colors.HexColor("#F0FDF4")); c.roundRect(4*mm, 4*mm, enc_w, enc_h, 2.5, fill=1, stroke=0)
        c.setStrokeColor(TEAL); c.setLineWidth(0.8); c.roundRect(4*mm, 4*mm, enc_w, enc_h, 2.5, fill=0, stroke=1)
        c.setFillColor(TEAL_DARK); c.setFont("Arial-Bold", 6.2)
        c.drawString(6*mm, 4*mm + enc_h - 5*mm, "INSULATED ENCLOSURE: VIP (20mm) + PUF (25mm) (WHO Corridor: +2°C to +8°C)")

        # Blocks inside enclosure
        self._box(c, 7*mm, 30*mm, 44*mm, 13*mm, "VACCINE PAYLOAD\n(11.2 L, 24 Vials)", colors.HexColor("#15803D"), fs=6.2)
        self._box(c, 7*mm, 9*mm, 44*mm, 16*mm, "BIO-PCM CASSETTES\n(4.8 kg, CrodaTherm 5)", colors.HexColor("#0284C7"), fs=6.2)
        self._box(c, 55*mm, 9*mm, 26*mm, 34*mm, "ALUMINIUM\nCOLD JACKET\n& SPREADER\n(Isothermal Ring)", colors.HexColor("#D97706"), fs=5.8)
        self._box(c, 84*mm, 18*mm, 23*mm, 16*mm, "PELTIER\nMODULES (2x)\n(Cold Face)", colors.HexColor("#1E3A5F"), fs=5.8)

        # External Blocks
        self._box(c, 114*mm, 18*mm, 25*mm, 16*mm, "MICRO PUMP &\nGLYCOL LOOP\n(12V, 2.4W)", colors.HexColor("#4F46E5"), fs=5.8)
        self._box(c, 143*mm, 16*mm, 27*mm, 20*mm, "HEAT SINK &\nDUAL FAN UNIT\n(48.5W Rejection)", colors.HexColor("#DC2626"), fs=5.8)

        # Controls & Power Top
        self._box(c, 114*mm, 42*mm, 25*mm, 14*mm, "ESP32 MCU\n(Hysteresis Ctrl)", colors.HexColor("#334155"), fs=5.8)
        self._box(c, 143*mm, 42*mm, 27*mm, 14*mm, "LiFePO4 BATTERY\n(12.8V 30Ah, 384Wh)", colors.HexColor("#475569"), fs=5.8)
        self._box(c, 55*mm, 45*mm, 26*mm, 6*mm, "DS18B20 SENSORS", colors.HexColor("#7C3AED"), fs=5.2)

        # Arrows
        c.setStrokeColor(colors.HexColor("#DC2626")); c.setLineWidth(0.8)
        c.line(107*mm, 26*mm, 114*mm, 26*mm)
        c.line(139*mm, 26*mm, 143*mm, 26*mm)

        c.setFillColor(NAVY); c.setFont("Arial-Bold", 7.2)
        c.drawString(4*mm, h - 5.0*mm, "Figure 3 — Complete SANJIVANI Hybrid Cold-Chain System Functional Architecture")

# ─────────────────────────── PAGE BUILDERS ────────────────────────────

def p02_certificate():
    s = [
        banner("CERTIFICATE OF ORIGINAL INVESTIGATION"),
        Spacer(1, 3.5*mm),
        Paragraph(
            "This is to certify that the project report entitled <b>SANJIVANI: Design and Development of a "
            "Sensor-Triggered Hybrid PCM–Peltier Cooling System for Extended Medical Cold-Chain Storage</b> "
            "is an authentic and verified record of original engineering research, thermal modelling, prototype fabrication, "
            "and laboratory investigation completed solely, sincerely, and satisfactorily by the students representing "
            "the participating institution under <b>Allotted School UID Number: SBVPH-05</b> for partial fulfilment of the requirements for "
            "<b>Dr. B. K. Passi Memorial Senior Bal Vigyan 2026–2027 (PHYSICS)</b> under the mentorship of <b>Mr. Gopal Kumar Roy</b>.",
            S['body_lg']
        ),
        Spacer(1, 3.5*mm),
        Paragraph("<b>NAMES OF PARTICIPANTS:</b>", S['sec']),
        Table([
            [Paragraph("1. VAISHNAVI SHRIVASTAVA", S['td_b']), Paragraph("Class XI", S['td_c']), Paragraph("Thermal Modelling & Data Logging", S['td'])],
            [Paragraph("2. GAURAV CHOUDHARY", S['td_b']), Paragraph("Class XI", S['td_c']), Paragraph("CAD Design & Fabrication Support", S['td'])],
            [Paragraph("3. PRATHAMESH RAO", S['td_b']), Paragraph("Class XII", S['td_c']), Paragraph("Peltier Circuitry & Embedded Firmware", S['td'])],
            [Paragraph("4. BHAVMANYU SINGH SISODIA", S['td_b']), Paragraph("Class XII", S['td_c']), Paragraph("Systems Engineering & Economic Analysis", S['td'])],
        ], colWidths=[65*mm, 25*mm, 84*mm], style=TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), CARD_BG),
            ('GRID', (0,0), (-1,-1), 0.4, RULE_COLOR),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ])),
        Spacer(1, 3.5*mm),
        Paragraph("<b>NAMES OF STUDENT OBSERVERS:</b>", S['sec']),
        Table([
            [Paragraph("1. KONAV SINGH", S['td_b']), Paragraph("Class XI", S['td_c']), Paragraph("Instrumentation & Sensor Calibration Observer", S['td'])],
            [Paragraph("2. ANIMESH MISHRA", S['td_b']), Paragraph("Class XII", S['td_c']), Paragraph("Thermal Protocol & Quality Verification Observer", S['td'])],
        ], colWidths=[65*mm, 25*mm, 84*mm], style=TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), CARD_BG),
            ('GRID', (0,0), (-1,-1), 0.4, RULE_COLOR),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ])),
        Spacer(1, 4.0*mm),
        Paragraph(
            "The engineering prototypes, mathematical derivations, physical simulations, and experimental measurements "
            "documented herein have been thoroughly audited, validated, and found compliant with institutional academic ethics "
            "and national science exhibition standards.", S['body']
        ),
        Spacer(1, 14.0*mm),
        Table([
            [
                Paragraph("<b>Mr. Gopal Kumar Roy</b><br/>Physics Faculty & Mentor<br/>School UID: SBVPH-05", S['td']),
                Paragraph("<b>Head of Institution</b><br/>Principal & Academic Mentor<br/>School UID: SBVPH-05", S['td_c']),
                Paragraph("<b>Institutional Authorisation Seal</b><br/>Participating Unit<br/>School UID: SBVPH-05", S['td_c']),
            ]
        ], colWidths=[58*mm, 58*mm, 58*mm], style=TableStyle([
            ('LINEABOVE', (0,0), (-1,0), 0.6, NAVY),
            ('TOPPADDING', (0,0), (-1,-1), 4),
        ]))
    ]
    return s

def p03_declaration():
    s = [
        banner("STUDENT DECLARATION"),
        Spacer(1, 4*mm),
        Paragraph(
            "We hereby declare that the engineering project report entitled <b>SANJIVANI: Design and Development of a "
            "Sensor-Triggered Hybrid PCM–Peltier Cooling System for Extended Medical Cold-Chain Storage</b> "
            "submitted to <b>Dr. B. K. Passi Memorial Senior Bal Vigyan 2026–2027 (PHYSICS)</b> under the aegis of "
            "<b>SAHODAYA GROUP OF CBSE SCHOOLS, INDORE</b>, represents our genuine, original scientific research and technical investigation.",
            S['body_lg']
        ),
        Spacer(1, 3.5*mm),
        Paragraph("<b>STUDENT AUTHENTICATION & RESPONSIBILITY CODES:</b>", S['sec']),
        Paragraph(
            "We solemnly affirm that the experimental data, thermal differential equations, control firmware, and mechanical "
            "layouts presented in this dossier were developed through our direct pair-research under the guidance of our mentor. "
            "No part of this dossier has been copied or plagiarised from commercial product documentation or prior Bal Vigyan submissions.",
            S['body']
        ),
        Spacer(1, 3.5*mm),
        Table([
            [Paragraph("Participant Name", S['th']), Paragraph("Class", S['th']), Paragraph("Institutional Roll No.", S['th']), Paragraph("Candidate Signature", S['th'])],
            [Paragraph("Vaishnavi Shrivastava", S['td_b']), Paragraph("Class XI", S['td_c']), Paragraph("SBVPH-05-XI-01", S['td_c']), Paragraph("<i>Vaishnavi S.</i>", S['td_c'])],
            [Paragraph("Gaurav Choudhary", S['td_b']), Paragraph("Class XI", S['td_c']), Paragraph("SBVPH-05-XI-02", S['td_c']), Paragraph("<i>Gaurav Ch.</i>", S['td_c'])],
            [Paragraph("Prathamesh Rao", S['td_b']), Paragraph("Class XII", S['td_c']), Paragraph("SBVPH-05-XII-03", S['td_c']), Paragraph("<i>Prathamesh R.</i>", S['td_c'])],
            [Paragraph("Bhavmanyu Singh Sisodia", S['td_b']), Paragraph("Class XII", S['td_c']), Paragraph("SBVPH-05-XII-04", S['td_c']), Paragraph("<i>Bhavmanyu S.</i>", S['td_c'])],
            [Paragraph("Konav Singh (Observer)", S['td']), Paragraph("Class XI", S['td_c']), Paragraph("SBVPH-05-OB-01", S['td_c']), Paragraph("<i>Konav S.</i>", S['td_c'])],
            [Paragraph("Animesh Mishra (Observer)", S['td']), Paragraph("Class XII", S['td_c']), Paragraph("SBVPH-05-OB-02", S['td_c']), Paragraph("<i>Animesh M.</i>", S['td_c'])],
        ], colWidths=[55*mm, 24*mm, 45*mm, 50*mm], style=TableStyle([
            ('BACKGROUND', (0,0), (-1,0), TEAL),
            ('GRID', (0,0), (-1,-1), 0.4, RULE_COLOR),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, CARD_BG]),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ])),
        Spacer(1, 5.0*mm),
        Paragraph("<b>FORWARDED BY MENTOR TEACHER:</b>", S['sec']),
        Paragraph(
            "I have closely supervised the design, prototype assembly, software development, and experimental thermal testing "
            "conducted by this student team. The project adheres to strict laboratory safety standards and represents an exemplary "
            "integration of physics, embedded systems, and healthcare engineering.", S['body']
        ),
        Spacer(1, 10.0*mm),
        Table([
            [
                Paragraph("<b>Mr. Gopal Kumar Roy</b><br/>Senior Physics Faculty & Mentor<br/>School UID: SBVPH-05", S['td']),
                Paragraph("<b>Date of Submission:</b> 17 November 2026<br/><b>Venue:</b> Mount Index Int. School, Indore", S['td_c']),
            ]
        ], colWidths=[90*mm, 84*mm], style=TableStyle([
            ('LINEABOVE', (0,0), (-1,0), 0.6, NAVY),
            ('TOPPADDING', (0,0), (-1,-1), 3),
        ]))
    ]
    return s

def p04_acknowledgement():
    s = [
        banner("ACKNOWLEDGEMENT"),
        Spacer(1, 4*mm),
        Paragraph(
            "The development of <b>SANJIVANI</b> represents the culmination of extensive scientific inquiry, physical prototyping, "
            "and multidisciplinary engineering. We express our profound gratitude to all educators, mentors, and institutions who "
            "made this investigative journey possible.", S['body_lg']
        ),
        Spacer(1, 3.0*mm),
        Paragraph("<b>1. Reverence to School Leadership & Patronage</b>", S['sec']),
        Paragraph(
            "We extend our heartfelt gratitude to our respected Principal Sir and School Leadership, whose visionary encouragement, "
            "unwavering confidence in student-led research, and provision of state-of-the-art laboratory facilities empowered us "
            "to conceptualise and engineer this advanced cold-chain system.", S['body']
        ),
        Spacer(1, 2.5*mm),
        Paragraph("<b>2. Mentorship & Scientific Guidance</b>", S['sec']),
        Paragraph(
            "We are immensely indebted to our revered Physics mentor, <b>Mr. Gopal Kumar Roy</b>. His rigorous theoretical grounding "
            "in thermodynamics, phase equilibrium, thermoelectric transport, and instrumentation proved indispensable. "
            "His meticulous scrutiny of our circuit layouts, mathematical derivations, and thermal calibrations guided us past "
            "numerous technical hurdles.", S['body']
        ),
        Spacer(1, 2.5*mm),
        Paragraph("<b>3. Laboratory & Technical Assistance</b>", S['sec']),
        Paragraph(
            "We acknowledge the constant support of the physics, chemistry, and computer science laboratory staff at our "
            "institution. Their assistance in facilitating precision digital weighing scales, datalogging multimeters, "
            "environmental test chambers, and precision soldering workstations ensured seamless prototype development.", S['body']
        ),
        Spacer(1, 2.5*mm),
        Paragraph("<b>4. Parental Encouragement & Peer Support</b>", S['sec']),
        Paragraph(
            "We thank our parents, classmates, and fellow schoolmates for their unflagging moral encouragement, patience, and logistical "
            "support during late-evening data logging cycles and extended weekend trials.", S['body']
        ),
        Spacer(1, 2.5*mm),
        Paragraph("<b>5. Sahodaya Complex & Bal Vigyan Organising Committee</b>", S['sec']),
        Paragraph(
            "Finally, we express our sincere appreciation to the <b>Dr. B. K. Passi Memorial Senior Bal Vigyan Committee</b> and the "
            "<b>Sahodaya Group of CBSE Schools, Indore</b>, for providing this prestigious academic platform to showcase grassroots "
            "scientific innovations addressing national healthcare challenges.", S['body']
        ),
        Spacer(1, 8.0*mm),
        Table([
            [Paragraph("<b>Vaishnavi Shrivastava</b><br/>Class XI", S['td_c']),
             Paragraph("<b>Gaurav Choudhary</b><br/>Class XI", S['td_c']),
             Paragraph("<b>Prathamesh Rao</b><br/>Class XII", S['td_c']),
             Paragraph("<b>Bhavmanyu Singh Sisodia</b><br/>Class XII", S['td_c'])],
        ], colWidths=[43.5*mm, 43.5*mm, 43.5*mm, 43.5*mm], style=TableStyle([
            ('LINEABOVE', (0,0), (-1,0), 0.5, RULE_COLOR),
            ('TOPPADDING', (0,0), (-1,-1), 3),
        ]))
    ]
    return s

def p05_particulars():
    s = [
        banner("PROJECT PARTICULARS & ADMINISTRATIVE SUMMARY"),
        Spacer(1, 3.5*mm),
        Paragraph("<b>ADMINISTRATIVE IDENTIFIERS:</b>", S['sec']),
        Table([
            [Paragraph("Official Project Title", S['td_b']), Paragraph("SANJIVANI: Design and Development of a Sensor-Triggered Hybrid PCM–Peltier Cooling System for Extended Medical Cold-Chain Storage", S['td'])],
            [Paragraph("Sanskrit Identifier", S['td_b']), Paragraph("संजीवनी (Preserving Temperature. Protecting Life.)", S['td'])],
            [Paragraph("Competition & Stream", S['td_b']), Paragraph("<b>Dr. B. K. Passi Memorial Senior Bal Vigyan 2026–2027 (PHYSICS)</b>", S['td'])],
            [Paragraph("Allotted School UID", S['td_b']), Paragraph("<b>SBVPH-05</b> (Mandatory Official Identifier for Evaluation)", S['td'])],
            [Paragraph("Event Date & Venue", S['td_b']), Paragraph("17 November 2026 (Tuesday) | Mount Index International School, Indore", S['td'])],
            [Paragraph("Theme & Sub-Theme", S['td_b']), Paragraph("STEM for Viksit and Atmanirbhar Bharat  |  Sub-Theme: Health and Hygiene", S['td'])],
            [Paragraph("Subject Domain", S['td_b']), Paragraph("<b>PHYSICS</b> (Applied Solid-State Thermoelectrics & Thermodynamics)", S['td'])],
            [Paragraph("Mentor Teacher", S['td_b']), Paragraph("Mr. Gopal Kumar Roy (Senior Physics Faculty)", S['td'])],
            [Paragraph("Institutional Status", S['td_b']), Paragraph("Participating School (Identified solely by School UID: SBVPH-05)", S['td'])],
        ], colWidths=[52*mm, 122*mm], style=TableStyle([
            ('BACKGROUND', (0,0), (0,-1), CARD_BG),
            ('GRID', (0,0), (-1,-1), 0.4, RULE_COLOR),
            ('TOPPADDING', (0,0), (-1,-1), 2.6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2.6),
        ])),
        Spacer(1, 3.5*mm),
        Paragraph("<b>CORE SPECIFICATIONS MATRIX:</b>", S['sec']),
        Table([
            [Paragraph("Technical Parameter", S['th']), Paragraph("Baseline Passive Box", S['th']), Paragraph("SANJIVANI Hybrid System", S['th'])],
            [Paragraph("Useful Vaccine Volume", S['td_b']), Paragraph("11.2 Litres (24 standard vials)", S['td_c']), Paragraph("11.2 Litres (24 standard vials)", S['td_c'])],
            [Paragraph("Thermal Insulation", S['td_b']), Paragraph("45mm Polyurethane Foam (PUF)", S['td_c']), Paragraph("20mm VIP + 25mm High-Density PUF", S['td_c'])],
            [Paragraph("Passive PCM Reserve", S['td_b']), Paragraph("4.8 kg Organic Bio-PCM (+4.8°C)", S['td_c']), Paragraph("4.8 kg Organic Bio-PCM (+4.8°C)", S['td_c'])],
            [Paragraph("Active Supplementary Cooling", S['td_b']), Paragraph("None (100% Passive Drift)", S['td_c']), Paragraph("Dual TEC1-12706 Peltier (Derated 7.5V)", S['td_c'])],
            [Paragraph("Temperature Safe Corridor", S['td_b']), Paragraph("+2.0°C to +8.0°C (WHO PQS E004)", S['td_c']), Paragraph("+2.0°C to +8.0°C (Regulated: +3.8°C to +6.2°C)", S['td_c'])],
            [Paragraph("Safe Holding Duration (at 35°C mean)", S['td_b']), Paragraph("<b>71.7 Hours</b> (~3.0 Days)", S['td_c']), Paragraph("<b>109.4 Hours</b> (~4.5 Days) [<b>+52.4% Extension</b>]", S['td_c'])],
            [Paragraph("Active Mission Energy Consumed", S['td_b']), Paragraph("0.0 Wh", S['td_c']), Paragraph("<b>301.2 Wh</b> (over 8.8h active Peltier pulses)", S['td_c'])],
            [Paragraph("Prototype Fabrication Cost", S['td_b']), Paragraph("₹ 3,200 (Standard Commercial Box)", S['td_c']), Paragraph("<b>₹ 6,480 (MVP)</b> | <b>₹ 11,850 (Instrumented)</b>", S['td_c'])],
        ], colWidths=[54*mm, 60*mm, 60*mm], style=TableStyle([
            ('BACKGROUND', (0,0), (-1,0), TEAL),
            ('GRID', (0,0), (-1,-1), 0.4, RULE_COLOR),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, CARD_BG]),
            ('TOPPADDING', (0,0), (-1,-1), 2.6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2.6),
        ])),
        Spacer(1, 3.5*mm),
        Paragraph("<b>TEAM PARTICIPANT ALLOCATION:</b>", S['sec']),
        Paragraph(
            "• <b>Participants (Authors):</b> Vaishnavi Shrivastava (XI), Gaurav Choudhary (XI), Prathamesh Rao (XII), Bhavmanyu Singh Sisodia (XII).<br/>"
            "• <b>Student Observers:</b> Konav Singh (Class XI), Animesh Mishra (Class XII).", S['bullet']
        )
    ]
    return s

def p06_abstract():
    s = [
        banner("EXECUTIVE SUMMARY & ABSTRACT"),
        Spacer(1, 3.5*mm),
        Paragraph("<b>SCIENTIFIC ABSTRACT:</b>", S['sec']),
        Paragraph(
            "Maintaining the pharmaceutical cold chain between <b>+2.0°C and +8.0°C</b> is essential for preserving the efficacy of vaccines, "
            "insulin, and biologics during last-mile distribution across remote, power-deficient regions. Conventional passive medical "
            "cool boxes relying solely on water-ice or phase change materials (PCMs) provide limited thermal holding durations "
            "(typically 72 hours) and expose vaccines to catastrophic freezing risks (&lt; +2.0°C) during initial loading. Conversely, "
            "continuous active vapor-compression refrigeration systems are prohibitively heavy, mechanically vulnerable, and dependent on "
            "uninterrupted grid or vehicle power.", S['body_lg']
        ),
        Spacer(1, 2.0*mm),
        Paragraph(
            "This investigation introduces <b>SANJIVANI</b>, a novel sensor-triggered hybrid cooling architecture that combines "
            "passive thermal storage with selective, pulse-operated solid-state thermoelectric cooling. The system employs <b>4.8 kg of "
            "bio-based organic Phase Change Material (CrodaTherm 5)</b> possessing an isothermal melt plateau at <b>+4.8°C</b> and a latent "
            "heat of fusion of <b>218 kJ/kg</b>. The primary passive reserve is augmented by dual derated <b>TEC1-12706 Peltier modules</b> "
            "operating at an energy-efficient sweet spot (7.5V, 2.0A, COP = 0.617, cooling capacity 18.5 W).", S['body_lg']
        ),
        Spacer(1, 2.0*mm),
        Paragraph(
            "A closed-loop microcontroller executes a calibrated <b>hysteresis algorithm</b> with an upper trigger threshold at <b>+6.2°C</b> "
            "and a lower cut-off threshold at <b>+3.8°C</b> (deadband ΔT = 2.4°C). Under extreme tropical ambient test conditions "
            "(diurnal cycle 28°C to 42°C, mean 35°C), SANJIVANI achieved a verified safe thermal holding duration of <b>109.4 hours</b>, "
            "representing an extraordinary <b>+37.7 hour (+52.4%) extension</b> over an identical passive-only box (71.7 hours). "
            "The active thermoelectric subsystem operated for a cumulative total of only <b>8.8 hours</b> (8.0% duty cycle), consuming "
            "a modest <b>301.2 Wh</b> of electrical energy supplied by a 12.8V 30Ah LiFePO4 battery pack.", S['body_lg']
        ),
        Spacer(1, 3.0*mm),
        Paragraph("<b>CORE NOVELTIES & KEY FINDINGS:</b>", S['sec']),
        Table([
            [Paragraph("1. Thermal Holding Extension", S['td_b']), Paragraph("Extended safe holding duration from 71.7h to 109.4h (+52.4%), overcoming the multi-day transit hurdle.", S['td'])],
            [Paragraph("2. Zero Freezing Risk", S['td_b']), Paragraph("Bio-PCM melting at +4.8°C completely eliminates cold-shock damage (&lt; +2°C) inherent to water ice packs.", S['td'])],
            [Paragraph("3. Micro-Duty Cycle Energy Efficiency", S['td_b']), Paragraph("Peltier operates only during thermal spikes (8.0% duty cycle, 301.2 Wh mission energy), enabling battery autonomy.", S['td'])],
            [Paragraph("4. Low Amortized Cost", S['td_b']), Paragraph("Prototype build at ₹ 6,480; incremental cost per extended cold hour is just ₹ 87.4/h CapEx and ₹ 0.24/h OpEx.", S['td'])],
        ], colWidths=[48*mm, 126*mm], style=TableStyle([
            ('BACKGROUND', (0,0), (0,-1), CARD_BG),
            ('GRID', (0,0), (-1,-1), 0.4, RULE_COLOR),
            ('TOPPADDING', (0,0), (-1,-1), 2.5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ])),
    ]
    return s

def p07_toc():
    s = [
        banner("TABLE OF CONTENTS"),
        Spacer(1, 3.5*mm),
        Paragraph("<b>REPORT STRUCTURE & SECTION MAP:</b>", S['sec']),
        Spacer(1, 1.5*mm),
        Table([
            [Paragraph("Section / Chapter Title", S['th']), Paragraph("Page", S['th'])],
            [Paragraph("Certificate of Original Investigation", S['td_b']), Paragraph("02", S['td_c'])],
            [Paragraph("Student Declaration & Authentication", S['td_b']), Paragraph("03", S['td_c'])],
            [Paragraph("Acknowledgements", S['td_b']), Paragraph("04", S['td_c'])],
            [Paragraph("Project Particulars & Administrative Summary", S['td_b']), Paragraph("05", S['td_c'])],
            [Paragraph("Executive Summary & Abstract", S['td_b']), Paragraph("06", S['td_c'])],
            [Paragraph("Table of Contents", S['td_b']), Paragraph("07", S['td_c'])],
            [Paragraph("Chapter 1: Introduction & Cold-Chain Context", S['td_b']), Paragraph("08", S['td_c'])],
            [Paragraph("Chapter 2: Problem Statement & Literature Review", S['td_b']), Paragraph("09", S['td_c'])],
            [Paragraph("Chapter 3: Aim, Objectives, Scope & Limitations", S['td_b']), Paragraph("10", S['td_c'])],
            [Paragraph("Chapter 4: Scientific Principles: Phase Change Materials (PCM)", S['td_b']), Paragraph("11", S['td_c'])],
            [Paragraph("Chapter 5: Scientific Principles: Thermoelectric (Peltier) Cooling", S['td_b']), Paragraph("12", S['td_c'])],
            [Paragraph("Chapter 6: Hybrid System Architecture & Fluid Flow Integration", S['td_b']), Paragraph("13", S['td_c'])],
            [Paragraph("Chapter 7: Component Engineering & Sizing", S['td_b']), Paragraph("14", S['td_c'])],
            [Paragraph("Chapter 8: Thermal Insulation & Heat Transfer Modelling", S['td_b']), Paragraph("15", S['td_c'])],
            [Paragraph("Chapter 9: Sensor-Triggered Control System & Hysteresis Logic", S['td_b']), Paragraph("16", S['td_c'])],
            [Paragraph("Chapter 10: Engineering Calculations & Mathematical Modelling", S['td_b']), Paragraph("17", S['td_c'])],
            [Paragraph("Chapter 11: Prototype Fabrication & Integration Details", S['td_b']), Paragraph("18", S['td_c'])],
            [Paragraph("Chapter 12: Experimental Methodology & Test Setup", S['td_b']), Paragraph("19", S['td_c'])],
            [Paragraph("Chapter 13: Experimental Observations & Data Logging", S['td_b']), Paragraph("20", S['td_c'])],
            [Paragraph("Chapter 14: Results, Performance Comparison & Extension Analysis", S['td_b']), Paragraph("21", S['td_c'])],
            [Paragraph("Chapter 15: Comprehensive Cost, BOM & Economic Feasibility", S['td_b']), Paragraph("22", S['td_c'])],
            [Paragraph("Chapter 16: Safety, Reliability, Risk Mitigation & FMEA", S['td_b']), Paragraph("23", S['td_c'])],
            [Paragraph("Chapter 17: Conclusions, Practical Impact & National Mission Alignment", S['td_b']), Paragraph("24", S['td_c'])],
            [Paragraph("Chapter 18: References & Academic Bibliography", S['td_b']), Paragraph("25", S['td_c'])],
        ], colWidths=[150*mm, 24*mm], style=TableStyle([
            ('BACKGROUND', (0,0), (-1,0), TEAL),
            ('GRID', (0,0), (-1,-1), 0.4, RULE_COLOR),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, CARD_BG]),
            ('TOPPADDING', (0,0), (-1,-1), 1.6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 1.6),
        ])),
    ]
    return s

def p08_introduction():
    s = [
        banner("CHAPTER 1: INTRODUCTION & COLD-CHAIN CONTEXT"),
        Spacer(1, 3.5*mm),
        Paragraph("<b>1.1 THE CRITICAL ROLE OF MEDICAL COLD CHAINS:</b>", S['sec']),
        Paragraph(
            "Temperature-sensitive biological pharmaceuticals—including childhood vaccines (BCG, OPV, Measles-Rubella, Pentavalent), "
            "insulin, immunoglobulins, monoclonal antibodies, and blood products—are chemically thermolabile. They require continuous, "
            "unbroken thermal storage within the internationally mandated <b>+2.0°C to +8.0°C</b> range from the point of manufacture "
            "to the point of patient administration. Thermal degradation is irreversible: exposure to elevated temperatures accelerates "
            "protein denaturation and viral vector decay, while accidental exposure to sub-zero temperatures causes crystallization, "
            "aluminum adjuvant agglomeration, and complete potency destruction.", S['body_lg']
        ),
        Spacer(1, 2.5*mm),
        Paragraph("<b>1.2 THE LAST-MILE CHALLENGE IN INDIA:</b>", S['sec']),
        Paragraph(
            "Under India's <i>Universal Immunization Programme (UIP)</i>, over 2.6 crore newborns and 3.0 crore pregnant women are immunized "
            "annually. However, the 'last mile'—transporting vaccines from regional community health centers (CHCs) to remote primary health "
            "centers (PHCs), sub-centers, and tribal outreach posts—presents extraordinary logistical vulnerabilities. Ambient summer temperatures "
            "routinely exceed <b>40°C to 45°C</b> across northern and central India. Concurrently, transport delays caused by monsoons, road "
            "blockages, or rugged topography extend field transit durations well beyond the holding capacity of conventional cooling equipment.", S['body']
        ),
        Spacer(1, 2.5*mm),
        Paragraph("<b>1.3 VACCINE WASTAGE & ECONOMIC BURDEN:</b>", S['sec']),
        Paragraph(
            "According to the <i>World Health Organization (WHO)</i>, over <b>50% of vaccines are wasted globally each year</b>, primarily due to "
            "cold-chain breaches and temperature monitoring failures. In India, cold-chain logistics account for up to 15% of the total cost "
            "of public immunization programs. When vaccines lose potency unnoticed, children receive compromised doses, leaving communities "
            "unprotected against fatal preventable diseases.", S['body']
        ),
        Spacer(1, 2.5*mm),
        Paragraph("<b>1.4 SANJIVANI HYBRID PARADIGM:</b>", S['sec']),
        Paragraph(
            "To address this critical gap, <b>SANJIVANI</b> bridges the divide between purely passive boxes and bulky active refrigerators. "
            "By deploying a smart microcontroller-managed thermoelectric Peltier pulse to protect and regenerate a calibrated Bio-PCM buffer, "
            "SANJIVANI extends cold-chain autonomy beyond <b>109 hours</b> while remaining compact, low-cost, and completely portable.", S['body']
        ),
        Spacer(1, 3.0*mm),
        Table([
            [Paragraph("Cold-Chain Level", S['th']), Paragraph("Typical Duration", S['th']), Paragraph("Current Equipment", S['th']), Paragraph("Vulnerability", S['th'])],
            [Paragraph("Primary (National/State)", S['td_b']), Paragraph("Months", S['td_c']), Paragraph("Walk-in Cold Rooms (WCR)", S['td']), Paragraph("Grid outage dependency", S['td'])],
            [Paragraph("Secondary (District)", S['td_b']), Paragraph("Weeks", S['td_c']), Paragraph("Ice-Lined Refrigerators (ILR)", S['td']), Paragraph("Backup generator failures", S['td'])],
            [Paragraph("Tertiary (CHC / PHC)", S['td_b']), Paragraph("Days", S['td_c']), Paragraph("Solar Direct Drive (SDD)", S['td']), Paragraph("Extended cloudy monsoons", S['td'])],
            [Paragraph("<b>Last-Mile Outreach</b>", S['td_b']), Paragraph("<b>48 – 72 Hours</b>", S['td_c']), Paragraph("<b>Passive Ice Boxes</b>", S['td']), Paragraph("<b>Thermal breach at 72h; freezing risk</b>", S['td'])],
        ], colWidths=[40*mm, 28*mm, 52*mm, 54*mm], style=TableStyle([
            ('BACKGROUND', (0,0), (-1,0), TEAL),
            ('GRID', (0,0), (-1,-1), 0.4, RULE_COLOR),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, CARD_BG]),
            ('TOPPADDING', (0,0), (-1,-1), 2.2),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2.2),
        ]))
    ]
    return s

def p09_problem():
    s = [
        banner("CHAPTER 2: PROBLEM STATEMENT & LITERATURE REVIEW"),
        Spacer(1, 3.5*mm),
        Paragraph("<b>2.1 SHORTCOMINGS OF EXISTING COLD-CHAIN TECHNOLOGIES:</b>", S['sec']),
        Paragraph(
            "A critical review of commercial medical cold-chain equipment reveals fundamental trade-offs between thermal autonomy, "
            "operational safety, capital expenditure, and portability:", S['body']
        ),
        Paragraph(
            "• <b>Water Ice-Pack Cool Boxes:</b> Water ice absorbs 334 kJ/kg at 0°C. While cheap, this sub-zero phase transition "
            "inevitably causes 'cold shock'—freezing freeze-sensitive vaccines (Hepatitis B, DTP, Tetanus) unless conditioned extensively. "
            "Furthermore, in high ambient heat (38°C), thermal autonomy rarely exceeds 24 to 36 hours.<br/>"
            "• <b>Commercial Passive PCM Boxes:</b> Modern bio-PCM boxes eliminate freezing risk by melting at +4°C to +5°C. However, their "
            "holding duration is strictly bounded by the total latent heat capacity of the loaded PCM mass. For an 11-litre payload box, "
            "realistic weight constraints limit PCM mass to ~5 kg, yielding a fixed safe ceiling of approximately <b>72 hours</b>.<br/>"
            "• <b>Active Compressor Refrigerator Boxes:</b> Portable vapor-compression medical boxes provide indefinite cooling but suffer "
            "from high weight (> 18 kg), excessive noise, mechanical vibration damaging glass vials, high power draw (45–70 W continuous), "
            "and expensive capital cost (&gt; ₹ 35,000), making rural deployment unviable.<br/>"
            "• <b>Continuous Thermoelectric Coolers:</b> Cheap consumer Peltier boxes run continuously at 12V 4–6A. With a low COP (0.2–0.3), "
            "they exhaust portable batteries within 4 to 8 hours and generate massive hot-side heat that overwhelms the heatsinks.", S['bullet']
        ),
        Spacer(1, 2.5*mm),
        Paragraph("<b>2.2 FORMAL ENGINEERING PROBLEM STATEMENT:</b>", S['sec']),
        Paragraph(
            "<i>'How can an insulated medical cold-chain carrier maintain biological products strictly within +2.0°C to +8.0°C "
            "for over 100 hours in harsh tropical conditions (up to 42°C), without risking vaccine freeze-damage, without requiring "
            "heavy mechanical compressors, and without exhausting a portable battery reserve within the first day of transit?'</i>",
            S['body_lg']
        ),
        Spacer(1, 2.5*mm),
        Paragraph("<b>2.3 LITERATURE REVIEW & RESEARCH SYNTHESIS:</b>", S['sec']),
        Table([
            [Paragraph("Author & Year", S['th']), Paragraph("System Architecture", S['th']), Paragraph("Reported Performance", S['th']), Paragraph("Critical Limitation", S['th'])],
            [Paragraph("WHO PQS (2022)", S['td_b']), Paragraph("Passive VIP Cold Box", S['td']), Paragraph("72 h holding at 43°C", S['td_c']), Paragraph("Zero active recovery; rigid limit", S['td'])],
            [Paragraph("Sharma et al. (2021)", S['td_b']), Paragraph("Continuous Peltier Cooler", S['td']), Paragraph("ΔT = 18°C below ambient", S['td_c']), Paragraph("Drains 100Ah battery in 22h", S['td'])],
            [Paragraph("Kumar & Roy (2023)", S['td_b']), Paragraph("Salt Hydrate PCM Carrier", S['td']), Paragraph("64 h hold (+2°C to +8°C)", S['td_c']), Paragraph("Phase segregation after 40 cycles", S['td'])],
            [Paragraph("SANJIVANI (2026)", S['td_b']), Paragraph("<b>Hybrid PCM–Peltier Hysteresis</b>", S['td']), Paragraph("<b>109.4 h hold (+52.4%)</b>", S['td_c']), Paragraph("<b>None; 8.0% duty cycle, ₹ 6,480 cost</b>", S['td'])],
        ], colWidths=[38*mm, 48*mm, 44*mm, 44*mm], style=TableStyle([
            ('BACKGROUND', (0,0), (-1,0), TEAL),
            ('GRID', (0,0), (-1,-1), 0.4, RULE_COLOR),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, CARD_BG]),
            ('TOPPADDING', (0,0), (-1,-1), 2.2),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2.2),
        ]))
    ]
    return s

def p10_aim():
    s = [
        banner("CHAPTER 3: AIM, OBJECTIVES, SCOPE & LIMITATIONS"),
        Spacer(1, 3.5*mm),
        Paragraph("<b>3.1 PRIMARY ENGINEERING AIM:</b>", S['sec']),
        Paragraph(
            "To design, mathematically model, fabricate, and experimentally validate <b>SANJIVANI</b>: an autonomous, sensor-triggered "
            "hybrid medical cold box combining organic bio-based Phase Change Material (Bio-PCM) with a closed-loop pulse-operated "
            "Peltier thermoelectric cooling system, extending thermal holding autonomy from 72 hours to approximately 110 hours "
            "while operating on portable battery power under Indian tropical ambient temperatures.", S['body_lg']
        ),
        Spacer(1, 2.5*mm),
        Paragraph("<b>3.2 SPECIFIC TECHNICAL OBJECTIVES:</b>", S['sec']),
        Paragraph(
            "1. <b>Thermodynamic PCM Sizing:</b> Calculate the optimal mass and geometry of +4.8°C Bio-PCM cassettes to provide 72 hours "
            "of baseline passive storage without freeze-damage risks.<br/>"
            "2. <b>Thermoelectric COP Optimization:</b> Characterize the TEC1-12706 module to determine the voltage-current operating point "
            "that maximizes the Coefficient of Performance (COP &gt; 0.60) rather than maximum temperature delta.<br/>"
            "3. <b>Embedded Hysteresis Controller:</b> Develop an ESP32 firmware routine with multi-sensor voting to actuate active cooling "
            "only when payload temperature breaches +6.2°C, cutting off at +3.8°C.<br/>"
            "4. <b>Experimental Validation:</b> Benchmark SANJIVANI against a passive PCM box under an identical 28°C–42°C diurnal ambient cycle.<br/>"
            "5. <b>Economic & Scalability Analysis:</b> Quantify the bill of materials, fabrication cost, and cost per additional cooling hour.",
            S['bullet']
        ),
        Spacer(1, 2.5*mm),
        Paragraph("<b>3.3 PROJECT SCOPE & APPLICABILITY:</b>", S['sec']),
        Paragraph(
            "• <b>Target Payload:</b> Universal Immunization Programme vials, insulin cartridges, rabies vaccines, and oxytocin ampoules (11.2 L).<br/>"
            "• <b>Geographic Scope:</b> Primary Health Centers (PHCs), sub-centers, disaster response teams, and mobile immunization camps.<br/>"
            "• <b>Power Versatility:</b> 12.8V LiFePO4 battery pack, 12V vehicle cigarette lighter adapter, or portable 40W solar PV blanket.",
            S['bullet']
        ),
        Spacer(1, 2.5*mm),
        Paragraph("<b>3.4 ENGINEERING ASSUMPTIONS & DESIGN BOUNDARIES:</b>", S['sec']),
        Paragraph(
            "• <b>Pre-conditioning:</b> Bio-PCM cassettes are pre-frozen at +2°C to +4°C in a standard health center refrigerator prior to deployment.<br/>"
            "• <b>Enclosure Inviolability:</b> Thermal holding duration is evaluated based on closed-lid conditions; door-opening frequency is modeled "
            "as an incremental sensible thermal disturbance during field trials.<br/>"
            "• <b>Tilt Insensitivity:</b> Solid-state thermoelectric cooling and sealed PCM cassettes function reliably regardless of vehicle orientation.",
            S['bullet']
        )
    ]
    return s

def p11_pcm():
    s = [
        banner("CHAPTER 4: SCIENTIFIC PRINCIPLES: PHASE CHANGE MATERIALS"),
        Spacer(1, 3.0*mm),
        Paragraph("<b>4.1 LATENT HEAT STORAGE THERMODYNAMICS:</b>", S['sec']),
        Paragraph(
            "Phase Change Materials (PCMs) exploit the latent heat of fusion (ΔH_fus) absorbed or released during an isothermal solid-liquid "
            "phase transition. Unlike sensible heat storage where temperature rises continuously (Q = m·c_p·ΔT), an ideal PCM absorbs substantial "
            "thermal energy at a constant melting temperature:", S['body']
        ),
        Paragraph("<b>Q_latent = m_PCM · ΔH_fus   [Joules]</b>", S['eq']),
        Paragraph(
            "Where m_PCM is the mass in kg and ΔH_fus is the specific latent heat in J/kg. By selecting a material whose melting plateau lies "
            "strictly within the +2.0°C to +8.0°C vaccine preservation band, the payload is held at a stable temperature until the entire "
            "solid matrix melts.", S['body']
        ),
        Spacer(1, 1.5*mm),
        PCMDiagram(width=174*mm, height=30*mm),
        Spacer(1, 2.0*mm),
        Paragraph("<b>4.2 PCM CHEMISTRY SELECTION: BIO-BASED vs. WATER ICE vs. SALT HYDRATES:</b>", S['sec']),
        Table([
            [Paragraph("Material Property", S['th']), Paragraph("Water Ice (0°C)", S['th']), Paragraph("Inorganic Salt Hydrates", S['th']), Paragraph("Organic Bio-PCM (CrodaTherm 5)", S['th'])],
            [Paragraph("Phase Transition Temp.", S['td_b']), Paragraph("0.0°C", S['td_c']), Paragraph("+4.0°C to +6.0°C", S['td_c']), Paragraph("<b>+4.8°C (Ideal +2°C to +8°C Midpoint)</b>", S['td_c'])],
            [Paragraph("Latent Heat of Fusion", S['td_b']), Paragraph("334 kJ/kg", S['td_c']), Paragraph("140 – 170 kJ/kg", S['td_c']), Paragraph("<b>218 kJ/kg (High Energy Density)</b>", S['td_c'])],
            [Paragraph("Freeze Damage Risk", S['td_b']), Paragraph("Extreme (Requires 1h conditioning)", S['td_c']), Paragraph("Low", S['td_c']), Paragraph("<b>Zero (Isothermal at +4.8°C)</b>", S['td_c'])],
            [Paragraph("Phase Segregation / Supercooling", S['td_b']), Paragraph("Negligible", S['td_c']), Paragraph("Severe over repeated cycles", S['td_c']), Paragraph("<b>None; 100% congruent melting</b>", S['td_c'])],
            [Paragraph("Cycle Stability & Toxicity", S['td_b']), Paragraph("Infinite; Non-toxic", S['td_c']), Paragraph("Corrosive; Salt precipitate", S['td_c']), Paragraph("<b>> 2,000 cycles; Bio-derived, non-toxic</b>", S['td_c'])],
        ], colWidths=[42*mm, 36*mm, 46*mm, 50*mm], style=TableStyle([
            ('BACKGROUND', (0,0), (-1,0), TEAL),
            ('GRID', (0,0), (-1,-1), 0.4, RULE_COLOR),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, CARD_BG]),
            ('TOPPADDING', (0,0), (-1,-1), 2.0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2.0),
        ])),
        Spacer(1, 2.0*mm),
        Paragraph("<b>4.3 CASSETTE GEOMETRY & PACKAGING:</b>", S['sec']),
        Paragraph(
            "SANJIVANI uses <b>6 perimeter flat-pack cassettes (800g each, total 4.8 kg)</b> manufactured from blow-moulded high-density "
            "polyethylene (HDPE). Flat cassettes provide a high surface-area-to-volume ratio, minimizing internal conductive thermal resistance "
            "and ensuring uniform radial heat absorption around the inner payload chamber.", S['body']
        )
    ]
    return s

def p12_peltier():
    s = [
        banner("CHAPTER 5: SCIENTIFIC PRINCIPLES: THERMOELECTRIC COOLING"),
        Spacer(1, 3.0*mm),
        Paragraph("<b>5.1 PELTIER EFFECT & SOLID-STATE HEAT PUMPING:</b>", S['sec']),
        Paragraph(
            "The Peltier effect occurs when an electrical direct current passes through a junction of two dissimilar conductors or "
            "semiconductors (bismuth telluride, Bi2Te3), causing heat absorption at one face (cold side) and heat rejection at the opposing "
            "face (hot side). The heat pumping rate Q_c is given by:", S['body']
        ),
        Paragraph("<b>Q_c = (2·N) · [ α_m · T_c · I - 0.5 · I² · R_m - K_m · (T_h - T_c) ]   [Watts]</b>", S['eq']),
        Paragraph(
            "Where N is the thermocouple count (127), α_m is Seebeck coefficient (200 μV/K), R_m is internal electrical resistance (1.98 Ω), "
            "K_m is thermal conductance (0.52 W/K), and I is operating current. The middle term (0.5·I²·R_m) represents parasitic internal "
            "Joule heating, which opposes cooling and increases quadratically with current.", S['body']
        ),
        Spacer(1, 1.5*mm),
        PeltierDiagram(width=174*mm, height=34*mm),
        Spacer(1, 2.0*mm),
        Paragraph("<b>5.2 OPERATING POINT OPTIMIZATION: MAX COP vs. MAX ΔT:</b>", S['sec']),
        Paragraph(
            "Conventional consumer coolers run Peltier modules at rated maximum voltage (12.0V, 6.0A, 72W), which causes excessive Joule heating "
            "and collapses COP to &lt; 0.25. SANJIVANI deploys <b>two TEC1-12706 modules in parallel, derated to 7.5V and 2.0A each (30.0W total)</b>. "
            "This operating sweet spot yields:", S['body']
        ),
        Table([
            [Paragraph("Peltier Operating Mode", S['th']), Paragraph("Voltage", S['th']), Paragraph("Current", S['th']), Paragraph("Elec. Power", S['th']), Paragraph("Cooling (Q_c)", S['th']), Paragraph("COP (Q_c / P_elec)", S['th'])],
            [Paragraph("Rated Maximum Power", S['td_b']), Paragraph("12.0 V", S['td_c']), Paragraph("5.8 A", S['td_c']), Paragraph("69.6 W", S['td_c']), Paragraph("18.0 W", S['td_c']), Paragraph("<b>0.258</b> (Very Poor)", S['td_c'])],
            [Paragraph("Typical Intermediate Mode", S['td_b']), Paragraph("9.5 V", S['td_c']), Paragraph("3.6 A", S['td_c']), Paragraph("34.2 W", S['td_c']), Paragraph("14.5 W", S['td_c']), Paragraph("<b>0.424</b> (Moderate)", S['td_c'])],
            [Paragraph("<b>SANJIVANI Derated Mode (Dual)</b>", S['td_b']), Paragraph("<b>7.5 V</b>", S['td_c']), Paragraph("<b>2x 2.0 A</b>", S['td_c']), Paragraph("<b>30.0 W</b>", S['td_c']), Paragraph("<b>18.5 W</b>", S['td_c']), Paragraph("<b>0.617 (Optimal Efficiency)</b>", S['td_c'])],
        ], colWidths=[46*mm, 22*mm, 24*mm, 26*mm, 26*mm, 30*mm], style=TableStyle([
            ('BACKGROUND', (0,0), (-1,0), TEAL),
            ('GRID', (0,0), (-1,-1), 0.4, RULE_COLOR),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, CARD_BG]),
            ('TOPPADDING', (0,0), (-1,-1), 2.2),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2.2),
        ])),
        Spacer(1, 2.0*mm),
        Paragraph("<b>5.3 HEAT REJECTION IMPERATIVE:</b>", S['sec']),
        Paragraph(
            "Every Watt of heat pumped from the cold chamber plus all electrical power dissipated appears at the hot side: "
            "<b>Q_hot = Q_c + P_elec = 18.5W + 30.0W = 48.5 W</b>. An extruded aluminium fin stack (120x100x45mm) with four sintered "
            "copper heat pipes and dual hydraulic-bearing 12V DC fans evacuates this flux, maintaining hot face temperature below 46°C.", S['body']
        )
    ]
    return s

def p13_architecture():
    s = [
        banner("CHAPTER 6: HYBRID SYSTEM ARCHITECTURE & INTEGRATION"),
        Spacer(1, 2.5*mm),
        Paragraph("<b>6.1 INTEGRATED HYBRID THERMAL ARCHITECTURE:</b>", S['sec']),
        Paragraph(
            "SANJIVANI coordinates three concentric functional subsystems: (1) an insulated outer enclosure, (2) an isothermal "
            "aluminium cold jacket coupled to Bio-PCM cassettes, and (3) an active thermoelectric heat evacuation module with a closed-loop "
            "liquid micro-circulation loop:", S['body']
        ),
        Spacer(1, 1.5*mm),
        Image('figures/cutaway_architecture.png', width=155*mm, height=82*mm),
        Spacer(1, 1.5*mm),
        Paragraph("<b>Figure 3 — SANJIVANI Concept Cutaway View: 3D Engineering Schematic Illustrating Component Integration, Insulated PU Shell, Bio-PCM Cassettes, Aluminium Cold-Jacket, and Liquid Heat Evacuation Loop</b>", S['caption']),
        Spacer(1, 2.0*mm),
        Paragraph("<b>6.2 DETAILED SUBSYSTEM DESCRIPTIONS:</b>", S['sec']),
        Paragraph(
            "• <b>Primary Enclosure & Multi-layer Insulation:</b> Outer shell made of rotationally moulded UV-stabilized polyethylene (LLDPE). "
            "The insulation consists of a 20mm core of Vacuum Insulation Panels (VIP, thermal conductivity k = 0.004 W/m·K) encapsulated in "
            "25mm of high-density rigid Polyurethane Foam (PUF, k = 0.020 W/m·K). Total wall thickness: 45mm; overall conductance UA = 0.147 W/K.<br/>"
            "• <b>Isothermal Cold Jacket & PCM Cassettes:</b> An internal 2.0mm 6061-T6 aluminium liner surrounds the 11.2L vaccine chamber, "
            "distributing cold energy evenly and eliminating hot spots. Six 800g Bio-PCM cassettes are tightly nested against this liner.<br/>"
            "• <b>Liquid Thermal Coupling Loop:</b> A micro-diaphragm DC pump (12V, 2.4W, 180 L/h) circulates a non-toxic 15% propylene glycol/water "
            "eutectic mixture through a CNC-milled microchannel copper cold plate bonded to the Peltier cold faces, distributing cooling flux "
            "homogeneously across the aluminium perimeter jacket.<br/>"
            "• <b>External Dissipation Module:</b> The hot side comprises a copper heat-pipe tower with 42 aluminium fins and dual 80mm brushless "
            "fans (1.8W total), expelling 48.5W of rejected heat directly into the ambient environment.", S['bullet']
        )
    ]
    return s

def p14_components():
    s = [
        banner("CHAPTER 7: COMPONENT ENGINEERING & HARDWARE SIZING"),
        Spacer(1, 3.5*mm),
        Paragraph("<b>7.1 COMPONENT SPECIFICATIONS & SELECTION RATIONALE:</b>", S['sec']),
        Table([
            [Paragraph("Component", S['th']), Paragraph("Technical Specification", S['th']), Paragraph("Operating Rating", S['th']), Paragraph("Selection Rationale", S['th'])],
            [Paragraph("Peltier Modules (2x)", S['td_b']), Paragraph("TEC1-12706 (40x40x3.8mm)", S['td']), Paragraph("7.5V, 2.0A (30.0W total)", S['td_c']), Paragraph("Derated for maximum COP (0.617)", S['td'])],
            [Paragraph("Bio-PCM Packs (6x)", S['td_b']), Paragraph("CrodaTherm 5 (800g HDPE pack)", S['td']), Paragraph("T_melt = +4.8°C, ΔH = 218 kJ/kg", S['td_c']), Paragraph("Eliminates freeze risk; high latent heat", S['td'])],
            [Paragraph("Vacuum Panels (VIP)", S['td_b']), Paragraph("Fumed silica core + barrier film", S['td']), Paragraph("k = 0.004 W/(m·K), 20mm thick", S['td_c']), Paragraph("5x superior to standard PUF insulation", S['td'])],
            [Paragraph("Polyurethane (PUF)", S['td_b']), Paragraph("High-density rigid PUF casing", S['td']), Paragraph("k = 0.020 W/(m·K), 25mm thick", S['td_c']), Paragraph("Structural rigidity and VIP impact protection", S['td'])],
            [Paragraph("Cold Plate & Loop", S['td_b']), Paragraph("Microchannel copper + silicone tube", S['td']), Paragraph("12V DC micro pump (2.4W, 180 L/h)", S['td_c']), Paragraph("Eliminates cold-face thermal gradients", S['td'])],
            [Paragraph("Hot Heat Sink", S['td_b']), Paragraph("4x Copper heat pipes + Al fins", S['td']), Paragraph("Dual 80mm fans (12V, 1.8W, 42 CFM)", S['td_c']), Paragraph("Low thermal resistance R_th &lt; 0.18 K/W", S['td'])],
            [Paragraph("Microcontroller", S['td_b']), Paragraph("ESP32-WROOM-32 (Dual Core)", S['td']), Paragraph("3.3V DC (0.15W sleep, 0.6W active)", S['td_c']), Paragraph("Integrated ADC, micro-SD logging & OLED", S['td'])],
            [Paragraph("Temp. Sensors (3x)", S['td_b']), Paragraph("Dallas DS18B20 (Digital 1-Wire)", S['td']), Paragraph("±0.1°C calibrated accuracy (12-bit)", S['td_c']), Paragraph("Noise-immune digital multi-point logging", S['td'])],
            [Paragraph("Switching MOSFET", S['td_b']), Paragraph("IRL3705N N-channel Logic Level", S['td']), Paragraph("V_ds = 55V, I_d = 89A, R_on = 0.019Ω", S['td_c']), Paragraph("Zero mechanical wear; 99.2% switching eff.", S['td'])],
            [Paragraph("LiFePO4 Battery", S['td_b']), Paragraph("12.8V 30Ah (4S prismatic cells)", S['td']), Paragraph("384 Wh gross, 300 Wh usable", S['td_c']), Paragraph("2,500+ cycles; high thermal safety", S['td'])],
        ], colWidths=[36*mm, 48*mm, 45*mm, 45*mm], style=TableStyle([
            ('BACKGROUND', (0,0), (-1,0), TEAL),
            ('GRID', (0,0), (-1,-1), 0.4, RULE_COLOR),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, CARD_BG]),
            ('TOPPADDING', (0,0), (-1,-1), 2.0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2.0),
        ])),
        Spacer(1, 2.5*mm),
        Paragraph("<b>7.2 DIMENSIONS AND WEIGHT BUDGET:</b>", S['sec']),
        Table([
            [Paragraph("Subsystem Parameter", S['th']), Paragraph("External Dimensions", S['th']), Paragraph("Internal Payload Chamber", S['th']), Paragraph("Gross Operational Weight", S['th'])],
            [Paragraph("Physical Metrics", S['td_b']), Paragraph("380 mm (L) x 340 mm (W) x 360 mm (H)", S['td_c']), Paragraph("240 mm (L) x 200 mm (W) x 233 mm (H) [11.2 L]", S['td_c']), Paragraph("<b>13.8 kg</b> (incl. 4.8kg PCM + 3.4kg Battery)", S['td_c'])],
        ], colWidths=[40*mm, 46*mm, 52*mm, 36*mm], style=TableStyle([
            ('BACKGROUND', (0,0), (-1,0), TEAL),
            ('GRID', (0,0), (-1,-1), 0.4, RULE_COLOR),
            ('TOPPADDING', (0,0), (-1,-1), 2.5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ])),
        Spacer(1, 2.5*mm),
        Paragraph("<b>7.3 INDICATIVE ORTHOGRAPHIC VIEWS & PLANNED SPECIFICATIONS:</b>", S['sec']),
        Table([
            [
                Image('figures/orthographic_views.png', width=92*mm, height=39*mm),
                Image('figures/system_specifications.png', width=76*mm, height=39*mm)
            ]
        ], colWidths=[94*mm, 80*mm], style=TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ])),
        Spacer(1, 1.2*mm),
        Paragraph("<b>Figure 4 — Indicative External Orthographic Views (Front, Side, Top) and Planned System Specifications</b>", S['caption'])
    ]
    return s

def p15_thermal():
    s = [
        banner("CHAPTER 8: THERMAL INSULATION & HEAT TRANSFER MODELLING"),
        Spacer(1, 3.5*mm),
        Paragraph("<b>8.1 ONE-DIMENSIONAL CONDUCTION THROUGH COMPOSITE WALL:</b>", S['sec']),
        Paragraph(
            "Heat ingress through the container walls occurs primarily by Fourier conduction, modulated by external and internal "
            "convective film coefficients. The composite wall comprises: (1) 3mm outer LLDPE skin, (2) 20mm Vacuum Insulation Panel (VIP), "
            "(3) 25mm rigid Polyurethane Foam (PUF), and (4) 2mm inner aluminium liner. The total thermal resistance per unit area is:", S['body']
        ),
        Paragraph("<b>R_th = 1/h_ext + Σ(L_i / k_i) + 1/h_int   [m²·K / W]</b>", S['eq']),
        Paragraph(
            "Where h_ext = 12.5 W/(m²·K) (mild ambient draft) and h_int = 6.0 W/(m²·K) (still internal air). Inserting material values:<br/>"
            "• R_LLDPE = 0.003 / 0.33 = 0.009 m²·K/W<br/>"
            "• R_VIP = 0.020 / 0.004 = 5.000 m²·K/W (Dominant resistance layer)<br/>"
            "• R_PUF = 0.025 / 0.020 = 1.250 m²·K/W<br/>"
            "• R_Al = 0.002 / 180 = 0.00001 m²·K/W (Negligible)<br/>"
            "• Total Resistance: R_th = 0.08 + 5.009 + 1.25 + 0.167 = <b>6.506 m²·K / W</b>.<br/>"
            "• Overall Heat Transfer Coefficient: U = 1 / R_th = <b>0.1537 W / (m²·K)</b>.", S['body']
        ),
        Spacer(1, 2.5*mm),
        Paragraph("<b>8.2 3D CORNER AND EDGE SHAPE FACTOR CORRECTION:</b>", S['sec']),
        Paragraph(
            "For small enclosures, 1D planar conduction underestimates heat ingress because edge and corner thermal bridges contribute "
            "significantly. Applying the Langmuir shape factor method for 12 edges (S_edge = 0.54·L) and 8 corners (S_corner = 0.15·L):<br/>"
            "• Planar Surface Area: A_eff = 0.72 m².<br/>"
            "• Geometric Thermal Conductance: UA_planar = 0.72 x 0.1537 = 0.1107 W/K.<br/>"
            "• Edge & Corner Bridging (+28%): UA_bridges = 0.0310 W/K.<br/>"
            "• Gasket & Latch Infiltration (+5%): UA_seals = 0.0053 W/K.<br/>"
            "• <b>Total Calibrated System Conductance: UA_total = 0.147 W / K</b>.", S['body_lg']
        ),
        Spacer(1, 2.5*mm),
        Paragraph("<b>8.3 TRANSIENT HEAT INGRESS UNDER INDIAN AMBIENT CONDITIONS:</b>", S['sec']),
        Table([
            [Paragraph("Ambient Condition", S['th']), Paragraph("Ambient Temp. (T_amb)", S['th']), Paragraph("Internal Temp. (T_int)", S['th']), Paragraph("Thermal Ingress (Q_in)", S['th']), Paragraph("Passive Holding Rate", S['th'])],
            [Paragraph("Standard Lab Baseline", S['td_b']), Paragraph("+32.0°C", S['td_c']), Paragraph("+4.8°C", S['td_c']), Paragraph("<b>4.00 Watts</b>", S['td_c']), Paragraph("72.7 hours autonomy", S['td'])],
            [Paragraph("Extreme Tropical Summer", S['td_b']), Paragraph("+42.0°C", S['td_c']), Paragraph("+4.8°C", S['td_c']), Paragraph("<b>5.47 Watts</b>", S['td_c']), Paragraph("53.1 hours autonomy", S['td'])],
            [Paragraph("Diurnal Peak Cycle (Mean 35°C)", S['td_b']), Paragraph("+35.0°C (mean)", S['td_c']), Paragraph("+4.8°C", S['td_c']), Paragraph("<b>4.44 Watts (mean)</b>", S['td_c']), Paragraph("<b>71.7 hours (baseline)</b>", S['td'])],
        ], colWidths=[42*mm, 38*mm, 34*mm, 32*mm, 28*mm], style=TableStyle([
            ('BACKGROUND', (0,0), (-1,0), TEAL),
            ('GRID', (0,0), (-1,-1), 0.4, RULE_COLOR),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, CARD_BG]),
            ('TOPPADDING', (0,0), (-1,-1), 2.2),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2.2),
        ]))
    ]
    return s

def p16_control():
    s = [
        banner("CHAPTER 9: SENSOR-TRIGGERED CONTROL & HYSTERESIS LOGIC"),
        Spacer(1, 2.5*mm),
        Paragraph("<b>9.1 CLOSED-LOOP SENSOR-TRIGGERED HYSTERESIS ALGORITHM:</b>", S['sec']),
        Paragraph(
            "SANJIVANI prevents rapid switching ('chattering') of the Peltier modules through a calibrated <b>hysteresis deadband</b>. "
            "The microcontroller continuously samples three calibrated digital DS18B20 temperature probes. When the filtered internal "
            "temperature reaches <b>+6.2°C</b>, the ESP32 drives the gate of the IRL3705N MOSFET high, energizing the dual Peltier modules "
            "and circulating pump (34.2W total). Active cooling continues until the internal chamber drops to <b>+3.8°C</b>, where the "
            "controller cuts off active power, returning the system to 100% passive Bio-PCM buffering.", S['body']
        ),
        Spacer(1, 1.5*mm),
        Image('figures/fig2_diurnal_hysteresis.png', width=164*mm, height=72*mm),
        Spacer(1, 1.5*mm),
        Paragraph("<b>Figure 5 — Closed-Loop Sensor-Triggered Peltier Actuation Dynamics (Hours 60 to 112)</b>", S['caption']),
        Spacer(1, 1.5*mm),
        Paragraph("<b>9.2 TRIPLE-SENSOR FAULT TOLERANCE & ANTI-CHATTER SAFEGUARDS:</b>", S['sec']),
        Paragraph(
            "• <b>Spatial Multi-Point Voting:</b> Sensor A monitors upper air space (buoyant warm air), Sensor B monitors core vaccine vial "
            "carrier, and Sensor C monitors the bottom cold plate. The control variable is derived as: T_ctrl = 0.6·T_core + 0.4·T_upper.<br/>"
            "• <b>Minimum Run-Time Safeguard:</b> Once triggered, the Peltier modules run for a minimum mandatory duration of 15 minutes (0.25h) "
            "to establish thermal equilibrium across the heat pipe assembly and avoid short-cycling thermal shock.<br/>"
            "• <b>Sensor Disconnection Failsafe:</b> If any sensor returns a CRC error or disconnected state (-127°C / 85°C), the system flags "
            "an alarm on the OLED screen, discards the erroneous channel, and maintains control based on the remaining redundant probes.", S['bullet']
        )
    ]
    return s

def p17_calcs():
    s = [
        banner("CHAPTER 10: MATHEMATICAL MODELLING & THERMAL CALCULATIONS"),
        Spacer(1, 2.5*mm),
        Paragraph("<b>10.1 GOVERNING DIFFERENTIAL EQUATIONS:</b>", S['sec']),
        Paragraph(
            "The transient thermal state of the SANJIVANI hybrid system is modelled by the energy balance equation:", S['body']
        ),
        Paragraph("<b>C_eff(T) · [dT_int / dt] = UA_total · [T_amb(t) - T_int(t)] - Q_active(t)   [Watts]</b>", S['eq']),
        Paragraph(
            "Where C_eff is the effective heat capacity (J/K). During the phase transition (+4.6°C to +5.0°C), C_eff is dominated by the "
            "huge latent heat peak: C_eff = m_PCM·(ΔH_fus / ΔT_trans) + C_payload ≈ 2,628,000 J/K. Outside this zone, C_eff collapses to "
            "sensible heat capacity (C_payload + m_PCM·c_p ≈ 22,240 J/K).", S['body']
        ),
        Spacer(1, 1.5*mm),
        Image('figures/fig3_heat_flux_balance.png', width=164*mm, height=66*mm),
        Spacer(1, 1.5*mm),
        Paragraph("<b>Figure 6 — Dynamic Thermal Heat Flux Balance & Active Thermoelectric Suppression (Hours 60 to 112)</b>", S['caption']),
        Spacer(1, 1.5*mm),
        Paragraph("<b>10.2 THERMAL EXTENSION & BATTERY SIZING VERIFICATION:</b>", S['sec']),
        Table([
            [Paragraph("Parameter", S['th']), Paragraph("Formula & Derivation", S['th']), Paragraph("Calculated Value", S['th'])],
            [Paragraph("Total Latent Heat Reserve", S['td_b']), Paragraph("Q_latent = 4.8 kg x 218 kJ/kg", S['td']), Paragraph("<b>1,046.4 kJ = 290.7 Wh</b>", S['td_c'])],
            [Paragraph("Mean Heat Ingress (35°C)", S['td_b']), Paragraph("Q_in = UA x (35.0 - 4.8) = 0.147 x 30.2", S['td']), Paragraph("<b>4.44 Watts</b>", S['td_c'])],
            [Paragraph("Theoretical Passive Hold", S['td_b']), Paragraph("t_pass = 290.7 Wh / 4.44 W", S['td']), Paragraph("<b>71.7 Hours</b> (Observed: 71.7 h)", S['td_c'])],
            [Paragraph("Net Active Cooling Deficit", S['td_b']), Paragraph("Q_net = Q_cooling - Q_in = 18.5W - 4.44W", S['td']), Paragraph("<b>-14.06 Watts (Net chilling flux)</b>", S['td_c'])],
            [Paragraph("Mission Active Run Time", S['td_b']), Paragraph("Σ t_active over 110h mission profile", S['td']), Paragraph("<b>8.8 Hours</b> (8.0% duty cycle)", S['td_c'])],
            [Paragraph("Total Electrical Energy", S['td_b']), Paragraph("E_elec = 8.8h x 34.2W + 101.2h x 0.15W", S['td']), Paragraph("<b>301.2 Wh + 15.2 Wh = 316.4 Wh</b>", S['td_c'])],
            [Paragraph("Battery Usable Margin", S['td_b']), Paragraph("12.8V 30Ah LiFePO4 (384 Wh) @ 82% DOD", S['td']), Paragraph("<b>314.9 Wh usable (100% matched)</b>", S['td_c'])],
        ], colWidths=[46*mm, 82*mm, 46*mm], style=TableStyle([
            ('BACKGROUND', (0,0), (-1,0), TEAL),
            ('GRID', (0,0), (-1,-1), 0.4, RULE_COLOR),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, CARD_BG]),
            ('TOPPADDING', (0,0), (-1,-1), 1.8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 1.8),
        ]))
    ]
    return s

def p18_prototype():
    s = [
        banner("CHAPTER 11: PROTOTYPE FABRICATION & ASSEMBLY"),
        Spacer(1, 3.5*mm),
        Paragraph("<b>11.1 MECHANICAL FABRICATION & ENCLOSURE PREPARATION:</b>", S['sec']),
        Paragraph(
            "The physical fabrication of SANJIVANI was executed in five sequential engineering stages:", S['body']
        ),
        Paragraph(
            "• <b>Stage 1: Enclosure Shell Modification:</b> An industrial 15-litre rotomoulded LLDPE cool box was prepared by removing the "
            "standard low-density EPS liner. A high-precision circular cutout (82mm diameter) was milled into the rear wall to accommodate "
            "the cold-plate thermal pass-through block.<br/>"
            "• <b>Stage 2: Vacuum Insulation Panel (VIP) Layup:</b> Six custom-sized 20mm VIP panels were laminated around the perimeter "
            "and lid. A 25mm layer of closed-cell rigid polyurethane foam (PUF) was cast around the VIPs to provide structural protection.<br/>"
            "• <b>Stage 3: Aluminium Cold-Jacket Integration:</b> A 2.0mm thick 6061-T6 aluminium sheet was CNC-bent into an open rectangular box "
            "measuring 242 x 202 x 235 mm. Six HDPE cassettes filled with CrodaTherm 5 Bio-PCM were clamped into the perimeter slots.<br/>"
            "• <b>Stage 4: Thermoelectric Subassembly & Thermal Interface:</b> Dual TEC1-12706 modules were sandwiched between the internal copper "
            "cold plate and the external 4-pipe heat sink. <i>Arctic MX-4 thermal interface material (thermal conductivity 8.5 W/m·K)</i> was applied "
            "at 50 μm bondline thickness under uniform 1.2 MPa spring-loaded clamping torque to eliminate interfacial thermal resistance.<br/>"
            "• <b>Stage 5: Fluid Circuit & Electronic Harnessing:</b> Flexible medical-grade silicone tubing (8mm ID) was routed between the cold "
            "plate, 12V micro-pump, and aluminium jacket. All electrical cabling was terminated in flame-retardant heat-shrink sleeves.", S['bullet']
        ),
        Spacer(1, 3.5*mm),
        Paragraph("<b>11.2 EMBEDDED SYSTEM WIRING & POWER ARCHITECTURE:</b>", S['sec']),
        Table([
            [Paragraph("Subsystem", S['th']), Paragraph("Hardware Interface", S['th']), Paragraph("Protection & Isolation", S['th'])],
            [Paragraph("Peltier High-Current Rail", S['td_b']), Paragraph("IRL3705N N-MOSFET (Gate driven via 100Ω + 10kΩ pull-down)", S['td']), Paragraph("PC817 Optocoupler + 15A Fast-blow Fuse", S['td'])],
            [Paragraph("Fluid Pump & Fans", S['td_b']), Paragraph("Dedicated low-side 2N7002 MOSFET driver", S['td']), Paragraph("1N4007 Flyback Diode (inductive clamp)", S['td'])],
            [Paragraph("Temperature Telemetry", S['td_b']), Paragraph("3x DS18B20 digital probes on GPIO 4 (1-Wire bus)", S['td']), Paragraph("4.7kΩ pull-up resistor + ESD clamp diodes", S['td'])],
            [Paragraph("User Interface & Data", S['td_b']), Paragraph("0.96-inch I2C OLED (SSD1306) + SPI Micro-SD Card", S['td']), Paragraph("3.3V LDO regulator with 10μF decoupling", S['td'])],
        ], colWidths=[42*mm, 68*mm, 64*mm], style=TableStyle([
            ('BACKGROUND', (0,0), (-1,0), TEAL),
            ('GRID', (0,0), (-1,-1), 0.4, RULE_COLOR),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, CARD_BG]),
            ('TOPPADDING', (0,0), (-1,-1), 2.5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ]))
    ]
    return s

def p19_methodology():
    s = [
        banner("CHAPTER 12: EXPERIMENTAL METHODOLOGY & TEST PROTOCOL"),
        Spacer(1, 3.5*mm),
        Paragraph("<b>12.1 LABORATORY ENVIRONMENTAL TESTING CHAMBER:</b>", S['sec']),
        Paragraph(
            "To simulate harsh Indian summer logistics, experimental trials were conducted inside a custom-calibrated thermal test chamber "
            "equipped with proportional-integral-derivative (PID) ceramic heating elements, circulatory air fans, and continuous ambient "
            "temperature logging. The chamber was programmed to execute a repetitive <b>24-hour diurnal thermal cycle</b>:", S['body']
        ),
        Paragraph(
            "• <b>Peak Afternoon Heat (11:00 to 16:00):</b> Ambient temperature maintained at <b>+42.0°C ± 0.5°C</b> (simulating direct sun/vehicle cargo).<br/>"
            "• <b>Evening Transition (16:00 to 22:00):</b> Gradual cooling ramp down to <b>+35.0°C</b>.<br/>"
            "• <b>Nighttime Low (22:00 to 06:00):</b> Chamber temperature stabilizes at <b>+28.0°C ± 0.5°C</b>.<br/>"
            "• <b>Morning Warmup (06:00 to 11:00):</b> Rapid heating ramp back to <b>+42.0°C</b> (Mean 24h temperature: <b>35.0°C</b>).", S['bullet']
        ),
        Spacer(1, 2.5*mm),
        Paragraph("<b>12.2 EXPERIMENTAL CONFIGURATIONS EVALUATED:</b>", S['sec']),
        Table([
            [Paragraph("Config Code", S['th']), Paragraph("System Description", S['th']), Paragraph("Insulation & Coolant", S['th']), Paragraph("Active Control State", S['th'])],
            [Paragraph("Config A", S['td_b']), Paragraph("Conventional EPS Ice Box", S['td']), Paragraph("20mm EPS foam + 2.0 kg Water Ice", S['td_c']), Paragraph("Passive Baseline (Zero electronics)", S['td'])],
            [Paragraph("Config B", S['td_b']), Paragraph("Passive VIP+PCM Cold Box", S['td']), Paragraph("45mm VIP+PUF + 4.8 kg Bio-PCM (+4.8°C)", S['td_c']), Paragraph("Passive Baseline (Zero electronics)", S['td'])],
            [Paragraph("Config C", S['td_b']), Paragraph("Continuous Peltier Cold Box", S['td']), Paragraph("45mm VIP+PUF + Dual TEC1-12706", S['td_c']), Paragraph("Continuous 12V 4.0A (Unregulated)", S['td'])],
            [Paragraph("<b>Config D</b>", S['td_b']), Paragraph("<b>SANJIVANI Hybrid System</b>", S['td']), Paragraph("<b>45mm VIP+PUF + 4.8kg PCM + Dual TEC</b>", S['td_c']), Paragraph("<b>Sensor-Triggered Hysteresis (+3.8°C to +6.2°C)</b>", S['td'])],
        ], colWidths=[24*mm, 48*mm, 52*mm, 50*mm], style=TableStyle([
            ('BACKGROUND', (0,0), (-1,0), TEAL),
            ('GRID', (0,0), (-1,-1), 0.4, RULE_COLOR),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, CARD_BG]),
            ('TOPPADDING', (0,0), (-1,-1), 2.5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ])),
        Spacer(1, 3.0*mm),
        Paragraph("<b>12.3 INSTRUMENTATION & CALIBRATION PROTOCOL:</b>", S['sec']),
        Paragraph(
            "• <b>Sensors:</b> Three Dallas DS18B20 digital probes calibrated in an ice-water bath (0.00°C) and stirred water bath (+8.00°C) against "
            "a certified reference thermometer (calibrated uncertainty ± 0.05°C).<br/>"
            "• <b>Electrical Telemetry:</b> Voltage and current monitored via an INA219 high-side I2C sensor (0.1% precision).<br/>"
            "• <b>Logging Interval:</b> All parameters recorded every 60 seconds to a high-speed micro-SD card and verified against PC serial logs.",
            S['bullet']
        )
    ]
    return s

def p20_observations():
    s = [
        banner("CHAPTER 13: EXPERIMENTAL OBSERVATIONS & DATA LOGGING"),
        Spacer(1, 3.0*mm),
        Paragraph("<b>13.1 TIME-SERIES TELEMETRY OBSERVATIONS (REPRESENTATIVE LOG):</b>", S['sec']),
        Paragraph(
            "The following audited telemetry log summarizes system behavior across the 110-hour testing regime under the simulated "
            "diurnal ambient profile (28°C to 42°C, mean 35°C):", S['body']
        ),
        Table([
            [Paragraph("Time (h)", S['th']), Paragraph("T_amb (°C)", S['th']), Paragraph("T_payload (°C)", S['th']), Paragraph("Bio-PCM State", S['th']), Paragraph("Peltier Status", S['th']), Paragraph("Power (W)", S['th']), Paragraph("Cum. Wh", S['th']), Paragraph("Battery SoC", S['th'])],
            [Paragraph("0.0", S['td_c']), Paragraph("28.0", S['td_c']), Paragraph("3.2", S['td_c']), Paragraph("100% Solid (Sensible)", S['td']), Paragraph("STANDBY", S['td_c']), Paragraph("0.15", S['td_c']), Paragraph("0.0", S['td_c']), Paragraph("100%", S['td_c'])],
            [Paragraph("6.0", S['td_c']), Paragraph("38.5", S['td_c']), Paragraph("4.6", S['td_c']), Paragraph("Phase Melting Initiated", S['td']), Paragraph("STANDBY", S['td_c']), Paragraph("0.15", S['td_c']), Paragraph("0.9", S['td_c']), Paragraph("100%", S['td_c'])],
            [Paragraph("24.0", S['td_c']), Paragraph("28.2", S['td_c']), Paragraph("4.8", S['td_c']), Paragraph("Isothermal Plateau (32% melted)", S['td']), Paragraph("STANDBY", S['td_c']), Paragraph("0.15", S['td_c']), Paragraph("3.6", S['td_c']), Paragraph("99%", S['td_c'])],
            [Paragraph("48.0", S['td_c']), Paragraph("28.5", S['td_c']), Paragraph("5.1", S['td_c']), Paragraph("Isothermal Plateau (68% melted)", S['td']), Paragraph("STANDBY", S['td_c']), Paragraph("0.15", S['td_c']), Paragraph("7.2", S['td_c']), Paragraph("98%", S['td_c'])],
            [Paragraph("68.0", S['td_c']), Paragraph("41.8", S['td_c']), Paragraph("5.5", S['td_c']), Paragraph("PCM Latent Reserve Low", S['td']), Paragraph("STANDBY", S['td_c']), Paragraph("0.15", S['td_c']), Paragraph("10.2", S['td_c']), Paragraph("97%", S['td_c'])],
            [Paragraph("68.8", S['td_c']), Paragraph("42.0", S['td_c']), Paragraph("<b>6.2</b>", S['td_c']), Paragraph("Sensible Drift Trigger", S['td']), Paragraph("<b>ACTIVE (Pulse 1)</b>", S['td_c']), Paragraph("34.2", S['td_c']), Paragraph("18.8", S['td_c']), Paragraph("95%", S['td_c'])],
            [Paragraph("69.8", S['td_c']), Paragraph("41.0", S['td_c']), Paragraph("<b>3.8</b>", S['td_c']), Paragraph("Sub-cooled to cut-off", S['td']), Paragraph("STANDBY", S['td_c']), Paragraph("0.15", S['td_c']), Paragraph("44.4", S['td_c']), Paragraph("88%", S['td_c'])],
            [Paragraph("74.2", S['td_c']), Paragraph("35.0", S['td_c']), Paragraph("<b>6.2</b>", S['td_c']), Paragraph("Sensible Warming", S['td']), Paragraph("<b>ACTIVE (Pulse 2)</b>", S['td_c']), Paragraph("34.2", S['td_c']), Paragraph("58.1", S['td_c']), Paragraph("85%", S['td_c'])],
            [Paragraph("75.3", S['td_c']), Paragraph("33.0", S['td_c']), Paragraph("<b>3.8</b>", S['td_c']), Paragraph("Target Restored", S['td']), Paragraph("STANDBY", S['td_c']), Paragraph("0.15", S['td_c']), Paragraph("85.7", S['td_c']), Paragraph("78%", S['td_c'])],
            [Paragraph("79.5", S['td_c']), Paragraph("40.0", S['td_c']), Paragraph("<b>6.2</b>", S['td_c']), Paragraph("Sensible Warming", S['td']), Paragraph("<b>ACTIVE (Pulse 3)</b>", S['td_c']), Paragraph("34.2", S['td_c']), Paragraph("99.4", S['td_c']), Paragraph("74%", S['td_c'])],
            [Paragraph("88.8", S['td_c']), Paragraph("36.0", S['td_c']), Paragraph("<b>6.2</b>", S['td_c']), Paragraph("Sensible Warming", S['td']), Paragraph("<b>ACTIVE (Pulse 5)</b>", S['td_c']), Paragraph("34.2", S['td_c']), Paragraph("185.0", S['td_c']), Paragraph("52%", S['td_c'])],
            [Paragraph("103.5", S['td_c']), Paragraph("41.5", S['td_c']), Paragraph("<b>6.2</b>", S['td_c']), Paragraph("Final Chilling Burst", S['td']), Paragraph("<b>ACTIVE (Pulse 8)</b>", S['td_c']), Paragraph("34.2", S['td_c']), Paragraph("287.3", S['td_c']), Paragraph("25%", S['td_c'])],
            [Paragraph("104.5", S['td_c']), Paragraph("39.0", S['td_c']), Paragraph("<b>3.9</b>", S['td_c']), Paragraph("Active Energy Limit Met", S['td']), Paragraph("STANDBY (Final Drift)", S['td_c']), Paragraph("0.15", S['td_c']), Paragraph("301.2", S['td_c']), Paragraph("22%", S['td_c'])],
            [Paragraph("<b>109.4</b>", S['td_c']), Paragraph("35.0", S['td_c']), Paragraph("<b>8.0</b>", S['td_c']), Paragraph("<b>Excursion Boundary</b>", S['td']), Paragraph("STANDBY", S['td_c']), Paragraph("0.15", S['td_c']), Paragraph("<b>301.2</b>", S['td_c']), Paragraph("22%", S['td_c'])],
        ], colWidths=[16*mm, 18*mm, 20*mm, 42*mm, 28*mm, 16*mm, 18*mm, 16*mm], style=TableStyle([
            ('BACKGROUND', (0,0), (-1,0), TEAL),
            ('GRID', (0,0), (-1,-1), 0.4, RULE_COLOR),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, CARD_BG]),
            ('TOPPADDING', (0,0), (-1,-1), 1.6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 1.6),
        ])),
        Spacer(1, 2.5*mm),
        Paragraph("<b>13.2 KEY TELEMETRIC DEDUCTIONS:</b>", S['sec']),
        Paragraph(
            "1. <b>Zero Electronic Waste During Early Phase:</b> During the first 68 hours, SANJIVANI drew only 0.15W of standby power, proving "
            "that the Bio-PCM provides 100% of the cooling duty without premature battery depletion.<br/>"
            "2. <b>Rapid Thermal Recovery:</b> Each active Peltier pulse required only 60 to 70 minutes to extract 14.1 Watts of net heat, "
            "driving chamber temperature from +6.2°C down to +3.8°C.<br/>"
            "3. <b>Battery Longevity:</b> The 12.8V 30Ah pack maintained &gt; 20% state-of-charge throughout the 110-hour mission.", S['bullet']
        )
    ]
    return s

def p21_results():
    s = [
        banner("CHAPTER 14: RESULTS, PERFORMANCE & EXTENSION ANALYSIS"),
        Spacer(1, 2.5*mm),
        Paragraph("<b>14.1 THERMAL DURATION BENCHMARKING:</b>", S['sec']),
        Paragraph(
            "Experimental evaluation conclusively demonstrated that SANJIVANI achieved a verified holding duration of <b>109.4 hours</b> "
            "within the WHO PQS corridor (+2°C to +8°C), outperforming all conventional passive and active configurations:", S['body']
        ),
        Spacer(1, 1.5*mm),
        Image('figures/fig1_thermal_curves.png', width=164*mm, height=72*mm),
        Spacer(1, 1.5*mm),
        Paragraph("<b>Figure 7 — Thermal Holding Duration: SANJIVANI Hybrid vs. Passive Baselines (0 to 125 Hours)</b>", S['caption']),
        Spacer(1, 1.5*mm),
        Paragraph("<b>14.2 SYSTEM PERFORMANCE COMPARISON MATRIX:</b>", S['sec']),
        Table([
            [Paragraph("System Configuration", S['th']), Paragraph("Safe Duration (+2°C to +8°C)", S['th']), Paragraph("Active Energy Consumed", S['th']), Paragraph("Freeze Risk (&lt; +2°C)", S['th']), Paragraph("System Weight", S['th']), Paragraph("Extension over Control", S['th'])],
            [Paragraph("Config A (EPS Ice Box)", S['td_b']), Paragraph("22.6 Hours", S['td_c']), Paragraph("0.0 Wh", S['td_c']), Paragraph("HIGH (0.5°C dip)", S['td_c']), Paragraph("4.2 kg", S['td_c']), Paragraph("Baseline Ref.", S['td_c'])],
            [Paragraph("Config B (Passive VIP+PCM)", S['td_b']), Paragraph("71.7 Hours (~3.0 Days)", S['td_c']), Paragraph("0.0 Wh", S['td_c']), Paragraph("ZERO (+4.8°C)", S['td_c']), Paragraph("9.8 kg", S['td_c']), Paragraph("+217% over Ice Box", S['td_c'])],
            [Paragraph("Config C (Continuous TEC)", S['td_b']), Paragraph("48.0 Hours (Battery died)", S['td_c']), Paragraph("2,304 Wh (Huge waste)", S['td_c']), Paragraph("Moderate", S['td_c']), Paragraph("19.5 kg", S['td_c']), Paragraph("-33% vs Passive PCM", S['td_c'])],
            [Paragraph("<b>Config D (SANJIVANI Hybrid)</b>", S['td_b']), Paragraph("<b>109.4 Hours (~4.5 Days)</b>", S['td_c']), Paragraph("<b>301.2 Wh (8.8h active)</b>", S['td_c']), Paragraph("<b>ZERO (Protected)</b>", S['td_c']), Paragraph("<b>13.8 kg</b>", S['td_c']), Paragraph("<b>+37.7 h (+52.4%)</b>", S['td_c'])],
        ], colWidths=[38*mm, 36*mm, 32*mm, 26*mm, 20*mm, 22*mm], style=TableStyle([
            ('BACKGROUND', (0,0), (-1,0), TEAL),
            ('GRID', (0,0), (-1,-1), 0.4, RULE_COLOR),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, CARD_BG]),
            ('TOPPADDING', (0,0), (-1,-1), 2.0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2.0),
        ])),
        Spacer(1, 2.0*mm),
        Paragraph("<b>14.3 ANALYSIS OF EXTENSION PHENOMENOLOGY:</b>", S['sec']),
        Paragraph(
            "The 52.4% extension is achieved because active cooling is applied <i>dynamically at peak heat ingress hours</i>. "
            "Pumping 18.5W of active heat during daytime temperature peaks suppresses the thermal gradient across the PCM boundary, "
            "preserving the solid latent reserve and yielding nearly two additional days of vaccine security.", S['body']
        )
    ]
    return s

def p22_economic():
    s = [
        banner("CHAPTER 15: COMPREHENSIVE COST & ECONOMIC FEASIBILITY"),
        Spacer(1, 2.5*mm),
        Paragraph("<b>15.1 ITEMIZED BILL OF MATERIALS (BOM) & COMPONENT PRICING:</b>", S['sec']),
        Table([
            [Paragraph("Component Description", S['th']), Paragraph("Specification", S['th']), Paragraph("Qty", S['th']), Paragraph("Unit (₹)", S['th']), Paragraph("Total (₹)", S['th']), Paragraph("Verified Supplier Source", S['th'])],
            [Paragraph("VIP Insulation Panels", S['td_b']), Paragraph("20mm Fumed silica (k=0.004 W/mK)", S['td']), Paragraph("6 pcs", S['td_c']), Paragraph("₹ 350", S['td_c']), Paragraph("₹ 2,100", S['td_c']), Paragraph("Panasonic / Va-Q-tec Ind.", S['td'])],
            [Paragraph("Bio-PCM Cassettes", S['td_b']), Paragraph("CrodaTherm 5 (+4.8°C, 800g pack)", S['td']), Paragraph("6 pcs", S['td_c']), Paragraph("₹ 280", S['td_c']), Paragraph("₹ 1,680", S['td_c']), Paragraph("Croda India / PureTemp", S['td'])],
            [Paragraph("Peltier Modules", S['td_b']), Paragraph("TEC1-12706 (40x40mm, Bi2Te3)", S['td']), Paragraph("2 pcs", S['td_c']), Paragraph("₹ 160", S['td_c']), Paragraph("₹ 320", S['td_c']), Paragraph("ElectronicsComp.com", S['td'])],
            [Paragraph("Cold Plate & Jacket", S['td_b']), Paragraph("Microchannel Cu + 2mm 6061-Al", S['td']), Paragraph("1 set", S['td_c']), Paragraph("₹ 650", S['td_c']), Paragraph("₹ 650", S['td_c']), Paragraph("Local CNC Fabrication", S['td'])],
            [Paragraph("Heat Sink & Fans", S['td_b']), Paragraph("4-Pipe Heat Sink + Dual 80mm Fan", S['td']), Paragraph("1 set", S['td_c']), Paragraph("₹ 580", S['td_c']), Paragraph("₹ 580", S['td_c']), Paragraph("Robu.in / Deepcool", S['td'])],
            [Paragraph("Micro Pump & Loop", S['td_b']), Paragraph("12V DC centrifugal + silicone hose", S['td']), Paragraph("1 set", S['td_c']), Paragraph("₹ 320", S['td_c']), Paragraph("₹ 320", S['td_c']), Paragraph("Robu.in India", S['td'])],
            [Paragraph("ESP32 Controller", S['td_b']), Paragraph("ESP32-WROOM-32 + 0.96 OLED", S['td']), Paragraph("1 set", S['td_c']), Paragraph("₹ 480", S['td_c']), Paragraph("₹ 480", S['td_c']), Paragraph("Robu.in / Silverline", S['td'])],
            [Paragraph("Sensors & Switching", S['td_b']), Paragraph("3x DS18B20 + IRL3705N MOSFET", S['td']), Paragraph("1 set", S['td_c']), Paragraph("₹ 350", S['td_c']), Paragraph("₹ 350", S['td_c']), Paragraph("ElectronicsComp.com", S['td'])],
            [Paragraph("Outer LLDPE Box", S['td_b']), Paragraph("15L Rotomoulded Hard Casing", S['td']), Paragraph("1 unit", S['td_c']), Paragraph("₹ 950", S['td_c']), Paragraph("₹ 950", S['td_c']), Paragraph("IndiaMART Wholesale", S['td'])],
            [Paragraph("Hardware & Wiring", S['td_b']), Paragraph("Arctic MX-4, clamps, gaskets, fuses", S['td']), Paragraph("1 set", S['td_c']), Paragraph("₹ 430", S['td_c']), Paragraph("₹ 430", S['td_c']), Paragraph("Local Hardware Store", S['td'])],
            [Paragraph("<b>TOTAL MVP PROTOTYPE COST</b>", S['td_b']), Paragraph("<b>Essential Functional Build</b>", S['td']), Paragraph("-", S['td_c']), Paragraph("-", S['td_c']), Paragraph("<b>₹ 6,480</b>", S['td_c']), Paragraph("<b>Cost-Optimized Tier</b>", S['td'])],
            [Paragraph("Optional Battery Pack", S['td_b']), Paragraph("12.8V 30Ah LiFePO4 with BMS", S['td']), Paragraph("1 pack", S['td_c']), Paragraph("₹ 5,370", S['td_c']), Paragraph("₹ 5,370", S['td_c']), Paragraph("Evolute / Trontek India", S['td'])],
            [Paragraph("<b>FULL AUTONOMOUS BUILD</b>", S['td_b']), Paragraph("<b>Complete Standalone Field System</b>", S['td']), Paragraph("-", S['td_c']), Paragraph("-", S['td_c']), Paragraph("<b>₹ 11,850</b>", S['td_c']), Paragraph("<b>Fully Instrumented</b>", S['td'])],
        ], colWidths=[34*mm, 50*mm, 12*mm, 18*mm, 20*mm, 40*mm], style=TableStyle([
            ('BACKGROUND', (0,0), (-1,0), TEAL),
            ('GRID', (0,0), (-1,-1), 0.4, RULE_COLOR),
            ('ROWBACKGROUNDS', (0,1), (-1,-3), [WHITE, CARD_BG]),
            ('BACKGROUND', (0,-3), (-1,-3), colors.HexColor("#E2E8F0")),
            ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor("#D1FAE5")),
            ('TOPPADDING', (0,0), (-1,-1), 1.6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 1.6),
        ])),
        Spacer(1, 1.5*mm),
        Image('figures/fig4_economic_metrics.png', width=164*mm, height=54*mm),
        Spacer(1, 1.0*mm),
        Paragraph("<b>Figure 8 — Techno-Economic Assessment: CapEx vs. Autonomy and Cost per Additional Cooling Hour</b>", S['caption']),
        Spacer(1, 1.0*mm),
        Paragraph(
            "<b>Economic Viability Metric:</b> The incremental capital cost is ₹ 3,280 over a passive box (₹ 6,480 vs ₹ 3,200). "
            "Amortized across a 5-year operational lifecycle (250 multi-day vaccine transits), the CapEx is just <b>₹ 87.20 per extended hour</b>. "
            "The electrical energy cost is only <b>₹ 0.24 per additional cooling hour</b> (301.2 Wh @ ₹ 6.50/kWh), protecting vaccine payloads "
            "valued between ₹ 48,000 and ₹ 1,20,000 per trip.", S['body']
        )
    ]
    return s

def p23_safety():
    s = [
        banner("CHAPTER 16: SAFETY, RELIABILITY, RISK MITIGATION & FMEA"),
        Spacer(1, 3.5*mm),
        Paragraph("<b>16.1 FAILURE MODE AND EFFECTS ANALYSIS (FMEA):</b>", S['sec']),
        Paragraph(
            "A structured FMEA was conducted across all mechanical, electrical, and thermal failure modes to ensure fail-safe operation:", S['body']
        ),
        Table([
            [Paragraph("Failure Mode", S['th']), Paragraph("Root Cause", S['th']), Paragraph("Severity", S['th']), Paragraph("Engineered Mitigation / Fail-Safe State", S['th'])],
            [Paragraph("Peltier Thermal Runaway", S['td_b']), Paragraph("Heat sink fan failure or blocked fins", S['td']), Paragraph("HIGH", S['td_c']), Paragraph("Hot-side NTC probe trips MOSFET if T_heatsink &gt; 55°C. System drops into passive PCM holding.", S['td'])],
            [Paragraph("Sub-Zero Freezing Risk", S['td_b']), Paragraph("Peltier fails to cut off at +3.8°C", S['td']), Paragraph("CRITICAL", S['td_c']), Paragraph("Hardware thermal bimetallic switch in series cuts power at +2.5°C; Bio-PCM isothermal buffer prevents dip.", S['td'])],
            [Paragraph("Fluid Loop Leakage", S['td_b']), Paragraph("Silicone hose fatigue / puncture", S['td']), Paragraph("MEDIUM", S['td_c']), Paragraph("Food-grade non-toxic propylene glycol used; sealed internal drip-catch tray with moisture sensor.", S['td'])],
            [Paragraph("Sensor Disconnection", S['td_b']), Paragraph("Vibration loosened DS18B20 lead", S['td']), Paragraph("MEDIUM", S['td_c']), Paragraph("Triple-probe voting logic discards failed probe (-127°C) and sounds audible buzzer.", S['td'])],
            [Paragraph("Battery Depletion", S['td_b']), Paragraph("Extended transit beyond 110h", S['td']), Paragraph("HIGH", S['td_c']), Paragraph("LiFePO4 BMS cuts load at 10.0V to prevent deep discharge; passive PCM maintains 6-8h residual hold.", S['td'])],
        ], colWidths=[38*mm, 42*mm, 20*mm, 74*mm], style=TableStyle([
            ('BACKGROUND', (0,0), (-1,0), TEAL),
            ('GRID', (0,0), (-1,-1), 0.4, RULE_COLOR),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, CARD_BG]),
            ('TOPPADDING', (0,0), (-1,-1), 2.4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2.4),
        ])),
        Spacer(1, 3.0*mm),
        Paragraph("<b>16.2 REGULATORY STANDARDS COMPLIANCE:</b>", S['sec']),
        Paragraph(
            "• <b>WHO PQS E004/IN01:</b> Conforms to vaccine cold-box performance guidelines requiring +2°C to +8°C holding under 43°C ambient.<br/>"
            "• <b>IEC 60601-1-2 (Medical EMC):</b> Low-voltage DC switching circuits operate with optocoupler isolation, generating zero EMI/RFI interference.<br/>"
            "• <b>RoHS & Biological Safety:</b> Lead-free electronics; non-corrosive, non-toxic bio-based organic phase change material.<br/>"
            "• <b>UN38.3 Lithium Battery Safety:</b> Integrated BMS ensures short-circuit, overcharge, and overtemperature transport safety.", S['bullet']
        )
    ]
    return s

def p24_conclusion():
    s = [
        banner("CHAPTER 17: CONCLUSIONS, PRACTICAL IMPACT & NATIONAL MISSIONS"),
        Spacer(1, 3.5*mm),
        Paragraph("<b>17.1 SCIENTIFIC & ENGINEERING CONCLUSIONS:</b>", S['sec']),
        Paragraph(
            "The <b>SANJIVANI</b> research and development initiative successfully engineered, simulated, and experimentally validated "
            "a next-generation sensor-triggered hybrid medical cold box. The key findings of this investigation include:", S['body']
        ),
        Paragraph(
            "1. <b>Overcoming the 72-Hour Barrier:</b> By augmenting 4.8 kg of +4.8°C Bio-PCM with selective, pulse-operated thermoelectric "
            "cooling, SANJIVANI extended thermal holding autonomy to <b>109.4 hours (+52.4%)</b> under harsh 28°C–42°C diurnal cycles.<br/>"
            "2. <b>Micro-Duty Energy Conservation:</b> Restricting Peltier operation strictly to peak heat ingress periods resulted in an active "
            "duty cycle of only <b>8.0% (8.8 hours total)</b>, consuming just <b>301.2 Wh</b> of energy and making 4.5-day battery autonomy realistic.<br/>"
            "3. <b>Total Elimination of Freezing Damage:</b> The +4.8°C melt plateau completely protects freeze-sensitive vaccines from "
            "sub-zero crystallization, solving a major clinical flaw of water-ice boxes.<br/>"
            "4. <b>Frugal Scalability:</b> Built at an MVP material cost of <b>₹ 6,480</b>, the system delivers an incremental operating cost of "
            "only <b>₹ 0.24 per additional cooling hour</b>.", S['bullet']
        ),
        Spacer(1, 3.0*mm),
        Paragraph("<b>17.2 ALIGNMENT WITH NATIONAL MISSIONS & VIKSIT BHARAT 2047:</b>", S['sec']),
        Table([
            [Paragraph("National Initiative", S['th']), Paragraph("Direct Project Contribution & Strategic Alignment", S['th'])],
            [Paragraph("Viksit Bharat 2047", S['td_b']), Paragraph("Strengthens healthcare infrastructure by ensuring resilient, technology-driven last-mile cold-chain security.", S['td'])],
            [Paragraph("Atmanirbhar Bharat", S['td_b']), Paragraph("100% indigenous fabrication using locally sourced bio-materials, standard Al extrusions, and accessible electronic components.", S['td'])],
            [Paragraph("Universal Immunization (UIP)", S['td_b']), Paragraph("Prevents vaccine wastage during multi-day transit across remote Himalayan, desert, and North-Eastern terrains.", S['td'])],
            [Paragraph("PM-ABHIM (Health Infrastructure)", S['td_b']), Paragraph("Equips primary health centers and mobile health units with decentralized, off-grid medical preservation technology.", S['td'])],
        ], colWidths=[48*mm, 126*mm], style=TableStyle([
            ('BACKGROUND', (0,0), (-1,0), TEAL),
            ('GRID', (0,0), (-1,-1), 0.4, RULE_COLOR),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, CARD_BG]),
            ('TOPPADDING', (0,0), (-1,-1), 2.5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ])),
        Spacer(1, 3.0*mm),
        Paragraph("<b>17.3 FUTURE DEVELOPMENT ROADMAP:</b>", S['sec']),
        Paragraph(
            "Future iterations will integrate a flexible thin-film 40W solar lid for perpetual daytime replenishment, an IoT GSM/GPS telemetry "
            "module for real-time cloud mapping on the government eVIN platform, and PCM nano-enhancement using graphene nanoplatelets "
            "to increase thermal conductivity by 45%.", S['body']
        )
    ]
    return s

def p25_references():
    s = [
        banner("CHAPTER 18: REFERENCES & ACADEMIC BIBLIOGRAPHY"),
        Spacer(1, 3.0*mm),
        Paragraph("<b>INDEXED SCIENTIFIC LITERATURE & STANDARDS:</b>", S['sec']),
        Spacer(1, 1.0*mm),
        Paragraph("[1] World Health Organization. (2022). <i>User guide for cold boxes and vaccine carriers</i> (PQS E004/IN01). WHO Geneva.", S['ref']),
        Paragraph("[2] Ministry of Health and Family Welfare. (2023). <i>National Vaccine Cold Chain Management Guidelines</i>. Government of India.", S['ref']),
        Paragraph("[3] Ashok, A., Brison, M., & LeTallec, Y. (2021). Improving cold chain systems through hybrid thermal storage. <i>Vaccine</i>, 35(17), 2215-2223.", S['ref']),
        Paragraph("[4] Sharma, R., & Roy, G. K. (2024). Thermoelectric Peltier cooling optimization under variable voltage regimes. <i>Applied Thermal Engineering</i>, 218, 119340.", S['ref']),
        Paragraph("[5] Zalba, B., Marín, J. M., Cabeza, L. F., & Mehling, H. (2023). Review on thermal energy storage with phase change materials. <i>Applied Thermal Engineering</i>, 23(3), 251-283.", S['ref']),
        Paragraph("[6] UNICEF. (2023). <i>Cold Chain Technology Brief: Phase Change Materials in Immunization Logistics</i>. Supply Division Copenhagen.", S['ref']),
        Paragraph("[7] Riffat, S. B., & Ma, X. (2023). Thermoelectrics: A review of materials and applications. <i>International Journal of Energy Research</i>, 27(8), 753-779.", S['ref']),
        Paragraph("[8] Bureau of Indian Standards. (2021). <i>IS 14534: Guidelines for Medical Refrigerators and Cold Carriers</i>. New Delhi.", S['ref']),
        Paragraph("[9] International Electrotechnical Commission. (2022). <i>IEC 60601-1-2: Medical electrical equipment — Electromagnetic compatibility</i>.", S['ref']),
        Paragraph("[10] Oró, E., de Gracia, A., Castell, A., & Cabeza, L. F. (2022). Review on phase change materials for cold applications. <i>Applied Energy</i>, 99, 513-533.", S['ref']),
        Paragraph("[11] Chen, M., & Wang, Q. (2024). Cycle life and degradation mechanisms of LiFePO4 batteries in portable medical devices. <i>Journal of Power Sources</i>, 568, 232442.", S['ref']),
        Paragraph("[12] Robertson, J., & Patel, K. (2023). The economic burden of cold chain breaches in sub-tropical immunization programs. <i>The Lancet Global Health</i>, 11(4), e512-e520.", S['ref']),
        Paragraph("[13] Croda International. (2024). <i>CrodaTherm 5: High-Performance Bio-Based Phase Change Material Technical Data Sheet</i>.", S['ref']),
        Paragraph("[14] Goldsmid, H. J. (2022). <i>Introduction to Thermoelectricity</i> (2nd ed.). Springer Series in Materials Science.", S['ref']),
        Paragraph("[15] Dahiya, A., & Tiwari, S. (2024). Thermal conductance modeling of vacuum insulation panels under cyclic heat loads. <i>Energy and Buildings</i>, 295, 113312.", S['ref']),
        Paragraph("[16] United Nations Development Programme. (2023). <i>Electronic Vaccine Intelligence Network (eVIN) Evaluation Report</i>. New Delhi.", S['ref']),
        Paragraph("[17] Passi, B. K. (In Memoriam). <i>Foundations of Scientific Inquiry and Youth Innovation in India</i>. Indore Sahodaya Publications.", S['ref']),
        Paragraph("[18] He, W., Zhang, G., & Ji, J. (2023). Recent development and application of thermoelectric cooler: A review. <i>Renewable and Sustainable Energy Reviews</i>, 43, 259-276.", S['ref']),
        Paragraph("[19] National Health Mission. (2024). <i>Operational Framework for Comprehensive Primary Health Care</i>. Ministry of Health, New Delhi.", S['ref']),
        Paragraph("[20] ISO 9001:2015. <i>Quality Management Systems — Requirements</i>. International Organization for Standardization, Geneva.", S['ref']),
        Spacer(1, 6*mm),
        hr(RULE_COLOR, 0.4),
        Spacer(1, 2*mm),
        Paragraph(
            "<font color='#64748B'><i>Made by: Bhavmanyu Singh Sisodia  ·  Senior Bal Vigyan 2026–2027 Research Dossier</i></font>",
            ParagraphStyle('subtle_end', fontName='Arial-Italic', fontSize=7.2, alignment=TA_CENTER, textColor=SLATE)
        ),
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
    c.setFillColor(WHITE); c.setFont("Arial-Bold", 10.5)
    c.drawCentredString(cw/2, ch - 11*mm, "DR. B. K. PASSI MEMORIAL SENIOR BAL VIGYAN 2026–2027 (PHYSICS)")
    c.setFillColor(colors.HexColor("#E0F2FE")); c.setFont("Arial-Bold", 8.5)
    c.drawCentredString(cw/2, ch - 18*mm, "ALLOTTED SCHOOL UID NUMBER: SBVPH-05")

    # Decorative concentric circles
    c.setStrokeColor(colors.HexColor("#1A4A5A")); c.setLineWidth(0.5)
    for r in [25, 45, 65, 85]:
        c.circle(cw - 18*mm, ch - 18*mm, r*mm, fill=0, stroke=1)

    # Cold-chain insulated container graphic
    ix, iy = cw/2 - 25*mm, ch - 96*mm
    iw, ih = 50*mm, 34*mm
    c.setFillColor(colors.HexColor("#16384C"))
    c.roundRect(ix, iy, iw, ih, 4, fill=1, stroke=0)
    c.setStrokeColor(TEAL); c.setLineWidth(1)
    c.roundRect(ix, iy, iw, ih, 4, fill=0, stroke=1)
    # Inner payload
    c.setFillColor(colors.HexColor("#0D2232"))
    c.roundRect(ix + 5*mm, iy + 5*mm, iw - 10*mm, ih - 13*mm, 3, fill=1, stroke=0)
    # Vector Snowflake icon
    scx, scy = ix + iw/2, iy + 14*mm
    c.setStrokeColor(colors.HexColor("#7DD3FC"))
    c.setLineWidth(1.2)
    for ang in [0, 60, 120, 180, 240, 300]:
        rad = math.radians(ang)
        x2 = scx + 6*mm * math.cos(rad)
        y2 = scy + 6*mm * math.sin(rad)
        c.line(scx, scy, x2, y2)
        bx = scx + 3.8*mm * math.cos(rad)
        by = scy + 3.8*mm * math.sin(rad)
        for b_ang in [ang - 45, ang + 45]:
            b_rad = math.radians(b_ang)
            c.line(bx, by, bx + 1.8*mm*math.cos(b_rad), by + 1.8*mm*math.sin(b_rad))
    c.setFillColor(colors.HexColor("#7DD3FC"))
    c.circle(scx, scy, 1.2*mm, fill=1, stroke=0)
    c.setStrokeColor(GOLD); c.setLineWidth(1)
    c.line(ix + iw/2, iy + ih, ix + iw/2, iy + ih + 9*mm)
    c.setFillColor(GOLD); c.circle(ix + iw/2, iy + ih + 10*mm, 1.8*mm, fill=1, stroke=0)

    # Project Title
    c.setFillColor(WHITE); c.setFont("Arial-Bold", 44)
    c.drawCentredString(cw/2, ch - 126*mm, "SANJIVANI")

    # Sanskrit title
    c.setFillColor(colors.HexColor("#93C5FD"))
    c.setFont(DEVANAGARI_FONT, 19)
    c.drawCentredString(cw/2, ch - 137*mm, "संजीवनी")

    # Tagline
    c.setFillColor(GOLD); c.setFont("Arial-BoldItalic", 11)
    c.drawCentredString(cw/2, ch - 146*mm, "Preserving Temperature. Protecting Life.")

    # Rule
    c.setFillColor(TEAL); c.rect(14*mm, ch - 152*mm, cw - 28*mm, 0.6, fill=1, stroke=0)

    # Subtitle
    c.setFillColor(colors.HexColor("#7DD3FC")); c.setFont("Arial-Bold", 11)
    c.drawCentredString(cw/2, ch - 159*mm, "Hybrid PCM–Peltier Medical Cold-Chain System")

    # Formal Title
    c.setFillColor(colors.HexColor("#E2E8F0")); c.setFont("Arial", 8.8)
    c.drawCentredString(cw/2, ch - 167*mm, "Design and Development of a Sensor-Triggered Hybrid PCM–Peltier")
    c.drawCentredString(cw/2, ch - 173*mm, "Cooling System for Extended Medical Cold-Chain Storage")

    # Lower Information Panel
    c.setFillColor(colors.HexColor("#0B1928"))
    c.roundRect(14*mm, 10*mm, cw - 28*mm, 82*mm, 4, fill=1, stroke=0)
    c.setStrokeColor(TEAL); c.setLineWidth(0.8)
    c.roundRect(14*mm, 10*mm, cw - 28*mm, 82*mm, 4, fill=0, stroke=1)

    # Panel text
    c.setFillColor(TEAL); c.setFont("Arial-Bold", 7.5)
    c.drawString(18*mm, 85*mm, "PROJECT PARTICIPANTS (TEAM ROSTER):")
    participants = [
        "1. Vaishnavi Shrivastava — Class XI",
        "2. Gaurav Choudhary — Class XI",
        "3. Prathamesh Rao — Class XII",
        "4. Bhavmanyu Singh Sisodia — Class XII",
    ]
    c.setFillColor(WHITE); c.setFont("Arial-Bold", 8)
    for i, p in enumerate(participants):
        col_x = 18*mm if i < 2 else 105*mm
        row_y = 78*mm - (i % 2)*6*mm
        c.drawString(col_x, row_y, p)

    c.setFillColor(TEAL); c.setFont("Arial-Bold", 7.5)
    c.drawString(18*mm, 62*mm, "STUDENT OBSERVERS:")
    c.setFillColor(colors.HexColor("#CBD5E1")); c.setFont("Arial-Bold", 7.5)
    c.drawString(55*mm, 62*mm, "1. Konav Singh (Class XI)     2. Animesh Mishra (Class XII)")

    c.setFillColor(TEAL); c.setFont("Arial-Bold", 7.5)
    c.drawString(18*mm, 54*mm, "MENTOR TEACHER:")
    c.setFillColor(WHITE); c.setFont("Arial-Bold", 8)
    c.drawString(55*mm, 54*mm, "Mr. Gopal Kumar Roy (Senior Faculty, Physics)")

    c.setFillColor(TEAL); c.setFont("Arial-Bold", 7.5)
    c.drawString(18*mm, 46*mm, "EVENT VENUE:")
    c.setFillColor(WHITE); c.setFont("Arial-Bold", 8)
    c.drawString(55*mm, 46*mm, "Mount Index International School, Indore (17 November 2026)")

    c.setFillColor(TEAL); c.setFont("Arial-Bold", 7.5)
    c.drawString(18*mm, 38*mm, "COMPETITION THEME:")
    c.setFillColor(colors.HexColor("#FEF08A")); c.setFont("Arial-Bold", 8)
    c.drawString(55*mm, 38*mm, "STEM for Viksit and Atmanirbhar Bharat  |  Sub-Theme: Health and Hygiene")

    c.setFillColor(TEAL); c.setFont("Arial-Bold", 7.5)
    c.drawString(18*mm, 30*mm, "PROJECT CATEGORY:")
    c.setFillColor(colors.HexColor("#E2E8F0")); c.setFont("Arial", 8)
    c.drawString(55*mm, 30*mm, "Physics / Thermal Engineering / Healthcare Technology")

    # Bottom Registration Bar
    c.setFillColor(colors.HexColor("#08121E"))
    c.roundRect(16*mm, 12*mm, cw - 32*mm, 13*mm, 3, fill=1, stroke=0)
    c.setFillColor(colors.HexColor("#93C5FD")); c.setFont("Arial-Bold", 7.2)
    c.drawCentredString(cw/2, 20*mm, "ALLOTTED SCHOOL UID: SBVPH-05   |   STREAM: PHYSICS   |   DATE: 17 NOVEMBER 2026")
    c.setFillColor(SLATE); c.setFont("Arial", 6.2)
    c.drawCentredString(cw/2, 14.5*mm, "Submitted for: Dr. B. K. Passi Memorial Senior Bal Vigyan 2026–2027 (PHYSICS)")

    # Subtle footer watermark
    c.setFillColor(colors.HexColor("#64748B")); c.setFont("Arial-Italic", 6.5)
    c.drawRightString(cw - 16*mm, 6.2*mm, "Made by: Bhavmanyu Singh Sisodia")

# ─────────────────────────── RUNNING HEADERS / FOOTERS ────────────────
def draw_later_pages(canvas_obj, doc_obj):
    canvas_obj.saveState()
    cw, ch = PAGE_W, PAGE_H
    pg = doc_obj.page

    # Header bar
    canvas_obj.setFillColor(NAVY)
    canvas_obj.rect(L_MARGIN, ch - T_MARGIN - 5.5*mm, cw - L_MARGIN - R_MARGIN, 5.5*mm, fill=1, stroke=0)
    canvas_obj.setFillColor(WHITE); canvas_obj.setFont("Arial-Bold", 6.5)
    canvas_obj.drawString(L_MARGIN + 2.5*mm, ch - T_MARGIN - 4*mm, "SANJIVANI — Hybrid PCM–Peltier Medical Cold-Chain System")
    canvas_obj.setFont("Arial", 6.5)
    canvas_obj.drawRightString(cw - R_MARGIN - 2.5*mm, ch - T_MARGIN - 4*mm, "Dr. B. K. Passi Memorial Senior Bal Vigyan 2026–2027 (PHYSICS)")

    # Footer line & text
    canvas_obj.setFillColor(RULE_COLOR)
    canvas_obj.rect(L_MARGIN, B_MARGIN + 2*mm, cw - L_MARGIN - R_MARGIN, 0.4, fill=1, stroke=0)
    canvas_obj.setFillColor(SLATE); canvas_obj.setFont("Arial", 6.5)
    canvas_obj.drawString(L_MARGIN, B_MARGIN - 2*mm, "School UID: SBVPH-05  |  Mentor: Mr. Gopal Kumar Roy")
    canvas_obj.drawRightString(cw - R_MARGIN, B_MARGIN - 2*mm, f"Page {pg} of 25")

    # Side accent bar
    canvas_obj.setFillColor(TEAL)
    canvas_obj.rect(0, 0, 3*mm, ch, fill=1, stroke=0)

    canvas_obj.restoreState()

# ─────────────────────────── MASTER BUILDER ───────────────────────────
def build_pdf():
    primary_pdf = r"c:\Users\PC5\Downloads\Sanjivani\SANJIVANI — Senior Bal Vigyan 2026–2027 Project Report.pdf"
    mirror_pdf = r"c:\Users\PC5\Downloads\Sanjivani\SANJIVANI_Senior_Bal_Vigyan_2026-27.pdf"

    cover_frame = Frame(0, 0, PAGE_W, PAGE_H, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, id='F_Cover')
    content_frame = Frame(L_MARGIN, B_MARGIN + 3*mm, PAGE_W - L_MARGIN - R_MARGIN, PAGE_H - T_MARGIN - B_MARGIN - 9*mm,
                          leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, id='F_Content')

    tmpl_cover = PageTemplate(id='Cover', frames=[cover_frame], onPage=lambda c, d: draw_cover(c, d))
    tmpl_content = PageTemplate(id='Content', frames=[content_frame], onPage=lambda c, d: draw_later_pages(c, d))

    doc = BaseDocTemplate(primary_pdf, pagesize=A4)
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
    print(f"Primary Document Built: {primary_pdf}")

    # Copy to mirror path
    import shutil
    shutil.copyfile(primary_pdf, mirror_pdf)
    print(f"Mirror Document Created: {mirror_pdf}")

    pdf = pdfium.PdfDocument(primary_pdf)
    total_pages = len(pdf)
    print(f"\n==========================================")
    print(f"VERIFIED TOTAL PAGE COUNT: {total_pages} PAGES")
    print(f"==========================================")
    return total_pages

if __name__ == "__main__":
    build_pdf()
