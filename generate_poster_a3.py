import os
import sys
from reportlab.lib.pagesizes import landscape, A3
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Ensure UTF-8 output
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# ------------------------------------------------------------------------------
# 1. FONT REGISTRATION
# ------------------------------------------------------------------------------
pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))
pdfmetrics.registerFont(TTFont('Arial-Bold', 'arialbd.ttf'))
pdfmetrics.registerFont(TTFont('Arial-Italic', 'ariali.ttf'))
pdfmetrics.registerFont(TTFont('Arial-BoldItalic', 'arialbi.ttf'))
pdfmetrics.registerFont(TTFont('Devanagari', r'C:\Windows\Fonts\Nirmala.ttf'))
pdfmetrics.registerFont(TTFont('DevanagariBold', r'C:\Windows\Fonts\NirmalaB.ttf'))

# ------------------------------------------------------------------------------
# 2. COLOR PALETTE (ISEF Academic & Engineering Standard)
# ------------------------------------------------------------------------------
NAVY_PRIMARY = colors.HexColor('#0B2545') # Dominant deep Oxford navy
NAVY_HEADER  = colors.HexColor('#0F172A') # Dark slate header
TEAL_ACCENT  = colors.HexColor('#0284C7') # Clinical cooling cyan/teal
TEAL_MUTED   = colors.HexColor('#0F766E') # Secondary engineering teal
TEXT_MAIN    = colors.HexColor('#0F172A') # High-contrast body text
TEXT_MUTED   = colors.HexColor('#334155') # Secondary descriptive text
BG_CARD      = colors.HexColor('#FFFFFF') # Pristine white card background
BORDER_CARD  = colors.HexColor('#CBD5E1') # Subtle card outline
BG_WARN      = colors.HexColor('#FEF3C7') # Thermal warning background
BORDER_WARN  = colors.HexColor('#D97706') # Thermal warning border
TEXT_WARN    = colors.HexColor('#92400E') # Thermal warning text
WHITE        = colors.HexColor('#FFFFFF')

# ------------------------------------------------------------------------------
# 3. HELPER FUNCTIONS
# ------------------------------------------------------------------------------
def draw_card(c, x, y, w, h, bg_color=BG_CARD, border_color=BORDER_CARD, corner_radius=3):
    """Draw a clean ISEF poster card container."""
    c.saveState()
    c.setFillColor(bg_color)
    c.setStrokeColor(border_color)
    c.setLineWidth(0.8)
    c.roundRect(x, y, w, h, corner_radius, stroke=1, fill=1)
    c.restoreState()

def draw_section_header(c, title, x, top_y, w, height=15.5, bg_color=NAVY_PRIMARY, tag=""):
    """Draw an authoritative, large-font ISEF section title banner."""
    c.saveState()
    # Header bar
    c.setFillColor(bg_color)
    c.setStrokeColor(bg_color)
    c.roundRect(x, top_y - height, w, height, 2.5, stroke=1, fill=1)
    
    # Title text (Large 11.5 pt Bold)
    c.setFillColor(WHITE)
    c.setFont('Arial-Bold', 11.0)
    c.drawString(x + 8, top_y - height + 4.5, title.upper())
    
    # Right-aligned scientific tag
    if tag:
        c.setFont('Arial-Bold', 8.5)
        c.setFillColor(colors.HexColor('#93C5FD'))
        c.drawRightString(x + w - 8, top_y - height + 4.5, tag.upper())
    c.restoreState()

def draw_flow_text(c, text, style, x, top_y, w, max_h=999):
    """Wrap and draw a Paragraph flowing downwards from top_y. Returns consumed height."""
    p = Paragraph(text, style)
    w_actual, h_actual = p.wrap(w, max_h)
    p.drawOn(c, x, top_y - h_actual)
    return h_actual

# ------------------------------------------------------------------------------
# 4. TYPOGRAPHY STYLES (Significantly Enlarged for ISEF Readability)
# ------------------------------------------------------------------------------
styles = {
    'body': ParagraphStyle(
        'PosterBody',
        fontName='Arial',
        fontSize=9.0,
        leading=12.6,
        textColor=TEXT_MAIN,
    ),
    'body_eq': ParagraphStyle(
        'PosterBodyEq',
        fontName='Arial',
        fontSize=8.8,
        leading=13.6,
        textColor=TEXT_MAIN,
    ),
    'body_bold': ParagraphStyle(
        'PosterBodyBold',
        fontName='Arial-Bold',
        fontSize=9.0,
        leading=12.6,
        textColor=TEXT_MAIN,
    ),
    'caption': ParagraphStyle(
        'PosterCaption',
        fontName='Arial-Italic',
        fontSize=8.2,
        leading=10.5,
        textColor=TEXT_MUTED,
        alignment=1, # Centered
    ),
    'subhead': ParagraphStyle(
        'PosterSubhead',
        fontName='Arial-Bold',
        fontSize=9.8,
        leading=13.0,
        textColor=NAVY_PRIMARY,
    ),
}

# ------------------------------------------------------------------------------
# 5. MAIN POSTER GENERATOR
# ------------------------------------------------------------------------------
def generate_sanjivani_a3_poster():
    pdf_path = "SANJIVANI_A3_SCIENCE_FAIR_POSTER.pdf"
    
    # Page setup: A3 Landscape (420 x 297 mm)
    c = canvas.Canvas(pdf_path, pagesize=landscape(A3))
    page_w, page_h = landscape(A3)
    
    # Millimeter conversion helper
    mm = 72.0 / 25.4
    
    # Technical Crisp White Background
    c.setFillColor(WHITE)
    c.rect(0, 0, page_w, page_h, stroke=0, fill=1)
    
    # Safe Margins: Left/Right = 10mm, Top/Bottom = 8mm
    m_left = 10.0 * mm
    m_right = page_w - 10.0 * mm
    m_top = page_h - 8.0 * mm
    usable_w = m_right - m_left # 400.0 mm
    
    # ==========================================================================
    # A. TOP HEADER CONTAINER (H = 44.0 mm: y = 245.0 to 289.0 mm)
    # ==========================================================================
    header_top = m_top
    header_h = 44.0 * mm
    header_y = header_top - header_h
    
    # Header Background Container
    c.saveState()
    c.setFillColor(NAVY_PRIMARY)
    c.setStrokeColor(colors.HexColor('#1E3A8A'))
    c.setLineWidth(1.2)
    c.roundRect(m_left, header_y, usable_w, header_h, 3, stroke=1, fill=1)
    
    # Accent top border strip
    c.setFillColor(TEAL_ACCENT)
    c.rect(m_left + 1, header_top - 2.5 * mm, usable_w - 2, 2.5 * mm, stroke=0, fill=1)
    
    # Top Subtle Metadata Ribbon
    c.setFont('Arial-Bold', 6.8)
    c.setFillColor(colors.HexColor('#93C5FD'))
    c.drawString(m_left + 7 * mm, header_top - 5.5 * mm, "DR. B. K. PASSI MEMORIAL SENIOR BAL VIGYAN 2026–2027")
    c.drawRightString(m_right - 7 * mm, header_top - 5.5 * mm, "ALLOTTED SCHOOL UID: SBVPH-05  |  STREAM: PHYSICS")
    c.restoreState()
    
    # --- HEADER BLOCK 1: BRAND IDENTITY (Left: x = 10 to 118 mm) ---
    c.saveState()
    c.setFont('Arial-Bold', 26)
    c.setFillColor(WHITE)
    c.drawString(m_left + 7 * mm, header_y + 24.5 * mm, "SANJIVANI")
    
    c.setFont('DevanagariBold', 20)
    c.setFillColor(colors.HexColor('#38BDF8'))
    c.drawString(m_left + 64 * mm, header_y + 24.5 * mm, "संजीवनी")
    
    c.setFont('Arial-Bold', 9.0)
    c.setFillColor(colors.HexColor('#38BDF8'))
    c.drawString(m_left + 7.2 * mm, header_y + 17.0 * mm, "HYBRID PCM–PELTIER MEDICAL COLD-CHAIN SYSTEM")
    
    c.setFont('Arial-Italic', 8.2)
    c.setFillColor(colors.HexColor('#E2E8F0'))
    c.drawString(m_left + 7.2 * mm, header_y + 10.8 * mm, "Preserving Temperature. Protecting Life.")
    
    c.setFont('Arial-Bold', 7.0)
    c.setFillColor(colors.HexColor('#93C5FD'))
    c.drawString(m_left + 7.2 * mm, header_y + 4.8 * mm, "SUBJECT: APPLIED SOLID-STATE THERMOELECTRICS")
    c.restoreState()
    
    # Divider 1
    c.saveState()
    c.setStrokeColor(colors.HexColor('#1E3A8A'))
    c.setLineWidth(0.8)
    c.line(m_left + 118 * mm, header_y + 3.5 * mm, m_left + 118 * mm, header_top - 6.5 * mm)
    c.restoreState()
    
    # --- HEADER BLOCK 2: FORMAL SCIENTIFIC TITLE (Center: x = 122 to 292 mm) ---
    c.saveState()
    title_html = (
        "<font face='Arial-Bold' size=13.0 color='#FFFFFF'>"
        "Design and Development of a Sensor-Triggered Hybrid PCM–Peltier Cooling System "
        "for Extended Medical Cold-Chain Storage"
        "</font>"
    )
    title_style = ParagraphStyle('HeadTitle', fontName='Arial-Bold', fontSize=13.0, leading=16.8, alignment=0)
    p_title = Paragraph(title_html, title_style)
    p_title.wrapOn(c, 168 * mm, 32 * mm)
    p_title.drawOn(c, m_left + 122 * mm, header_y + 15.5 * mm)
    
    sub_title_html = (
        "<font face='Arial-Bold' size=7.8 color='#38BDF8'>NATIONAL FRAMEWORK: </font>"
        "<font face='Arial' size=7.6 color='#E2E8F0'>STEM for Viksit and Atmanirbhar Bharat &nbsp;|&nbsp; </font>"
        "<font face='Arial-Bold' size=7.8 color='#38BDF8'>SUB-THEME: </font>"
        "<font face='Arial' size=7.6 color='#E2E8F0'>Health and Hygiene</font>"
    )
    p_sub = Paragraph(sub_title_html, ParagraphStyle('HeadSub', fontName='Arial', fontSize=7.6, leading=9.5))
    p_sub.wrapOn(c, 168 * mm, 12 * mm)
    p_sub.drawOn(c, m_left + 122 * mm, header_y + 4.5 * mm)
    c.restoreState()
    
    # Divider 2
    c.saveState()
    c.setStrokeColor(colors.HexColor('#1E3A8A'))
    c.setLineWidth(0.8)
    c.line(m_left + 292 * mm, header_y + 3.5 * mm, m_left + 292 * mm, header_top - 6.5 * mm)
    c.restoreState()
    
    # --- HEADER BLOCK 3: RESEARCH TEAM & IDENTIFICATION (Right: x = 296 to 408 mm) ---
    c.saveState()
    team_html = (
        "<font face='Arial-Bold' size=7.5 color='#38BDF8'>STUDENT INVESTIGATORS:</font><br/>"
        "<font face='Arial-Bold' size=7.6 color='#FFFFFF'>• Vaishnavi Shrivastava </font><font face='Arial' size=7.0 color='#CBD5E1'>(XI) &nbsp;&nbsp;</font>"
        "<font face='Arial-Bold' size=7.6 color='#FFFFFF'>• Gaurav Choudhary </font><font face='Arial' size=7.0 color='#CBD5E1'>(XI)<br/></font>"
        "<font face='Arial-Bold' size=7.6 color='#FFFFFF'>• Prathamesh Rao </font><font face='Arial' size=7.0 color='#CBD5E1'>(XII) &nbsp;&nbsp;</font>"
        "<font face='Arial-Bold' size=7.6 color='#FFFFFF'>• Bhavmanyu Singh </font><font face='Arial' size=7.0 color='#CBD5E1'>(XII)</font>"
    )
    p_team = Paragraph(team_html, ParagraphStyle('TeamP', leading=9.2))
    p_team.wrapOn(c, 58 * mm, 35 * mm)
    p_team.drawOn(c, m_left + 296 * mm, header_y + 4.5 * mm)
    
    inst_html = (
        "<font face='Arial-Bold' size=7.5 color='#38BDF8'>OFFICIAL PARTICIPATION:</font><br/>"
        "<font face='Arial-Bold' size=9.5 color='#FFFFFF'>SCHOOL UID: SBVPH-05</font><br/>"
        "<font face='Arial-Bold' size=7.2 color='#E2E8F0'>Mentor: </font><font face='Arial' size=7.2 color='#FFFFFF'>Mr. Gopal Kumar Roy<br/></font>"
        "<font face='Arial-Bold' size=7.2 color='#E2E8F0'>Date: </font><font face='Arial' size=7.2 color='#FFFFFF'>17 Nov 2026 (Tuesday)</font>"
    )
    p_inst = Paragraph(inst_html, ParagraphStyle('InstP', leading=9.2))
    p_inst.wrapOn(c, 48 * mm, 35 * mm)
    p_inst.drawOn(c, m_left + 356 * mm, header_y + 4.5 * mm)
    c.restoreState()
    
    # ==========================================================================
    # B. THREE-COLUMN RESEARCH POSTER GRID (y = 26.5 to 241.0 mm, H = 214.5 mm)
    # ==========================================================================
    grid_top = header_y - 4.0 * mm # 241.0 mm
    grid_bottom = 26.5 * mm
    grid_h = grid_top - grid_bottom # 214.5 mm
    
    col1_w = 124.0 * mm
    col2_w = 138.0 * mm # Center Hero Innovation Column
    col3_w = 124.0 * mm
    gutter = 7.0 * mm
    
    col1_x = m_left
    col2_x = col1_x + col1_w + gutter # 141.0 mm
    col3_x = col2_x + col2_w + gutter # 286.0 mm
    
    # --------------------------------------------------------------------------
    # COLUMN 1: CLINICAL NEED, HYPOTHESIS & GOVERNING THERMODYNAMICS
    # --------------------------------------------------------------------------
    # Card 1.1: Problem & Research Hypothesis (H = 75.0 mm)
    c11_h = 75.0 * mm
    c11_y = grid_top - c11_h
    draw_card(c, col1_x, c11_y, col1_w, c11_h)
    draw_section_header(c, "1. The Cold-Chain Problem & Hypothesis", col1_x, grid_top, col1_w, height=15.5, tag="Clinical Need")
    
    p11_text = (
        "<b>• The Vaccine Wastage Crisis:</b> The World Health Organization (WHO) estimates that <b>up to 50% of temperature-sensitive vaccines</b> "
        "(HPV, Rotavirus, mRNA, Hepatitis B) are compromised annually during last-mile off-grid transport in tropical regions.<br/>"
        "<b>• Failure Modes of Conventional Carriers:</b> Water-ice packs cause severe <b>accidental freezing risk (< 0°C)</b>, which irreversibly "
        "denatures liquid vaccine antigens. Conversely, passive Phase Change Material (PCM) boxes experience rapid thermal exhaustion within 24–48 hours under sub-tropical ambient heat (35°C–43°C).<br/>"
        "<b>• Central Research Hypothesis:</b> <i>Can sensor-triggered thermoelectric active cooling, activated selectively only during peak diurnal heat stress, "
        "suppress internal chamber rise, retard PCM latent reserve depletion, and extend holding autonomy beyond 100 hours with < 320 Wh electrical consumption?</i>"
    )
    draw_flow_text(c, p11_text, styles['body'], col1_x + 4.0 * mm, grid_top - 18.0 * mm, col1_w - 8.0 * mm)
    
    # Card 1.2: Thermodynamic Governing Formulations & Energy Transport (H = 135.5 mm)
    c12_y = grid_bottom
    c12_h = c11_y - 4.0 * mm - grid_bottom # 135.5 mm
    draw_card(c, col1_x, c12_y, col1_w, c12_h)
    draw_section_header(c, "2. Thermodynamic Governing Equations", col1_x, c11_y - 4.0 * mm, col1_w, height=15.5, tag="Physics Principles")
    
    eq_text = (
        "<b>1. Latent Thermal Storage (Bio-PCM Buffer):</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b><i>Q<sub>latent</sub> = m<sub>pcm</sub> · Δh<sub>fus</sub></i></b> &nbsp;&nbsp;→&nbsp;&nbsp; 4.8 kg × 218 kJ/kg = <b>1,046.4 kJ (290.7 Wh)</b><br/>"
        "<b>2. Thermoelectric First Law Heat Balance:</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b><i>Q̇<sub>hot</sub> = Q̇<sub>cold</sub> + P<sub>elec</sub></i></b> &nbsp;&nbsp;→&nbsp;&nbsp; 18.5 W + 30.0 W = <b>48.5 W</b><br/>"
        "<b>3. Solid-State Coefficient of Performance (COP):</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b><i>COP = Q̇<sub>cold</sub> / P<sub>elec</sub> = (2N[αT<sub>c</sub>I − ½I²R − KΔT]) / (V·I)</i></b> &nbsp;≈&nbsp; <b>0.617</b><br/>"
        "<b>4. Fourier Composite Enclosure Ingress:</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b><i>Q̇<sub>in</sub> = (UA) · (T<sub>amb</sub> − T<sub>core</sub>)</i></b> &nbsp;&nbsp;→&nbsp;&nbsp; 0.147 W/K × 30 K = <b>4.41 W</b>"
    )
    draw_flow_text(c, eq_text, styles['body_eq'], col1_x + 4.0 * mm, c11_y - 4.0 * mm - 18.0 * mm, col1_w - 8.0 * mm)
    
    # Embedded Authentic Heat Flow Diagram (Prominent & Centered)
    if os.path.exists('poster_assets/energy_flow_diagram.png'):
        img_w = 98.0 * mm
        img_h = img_w / 1.769 # 55.4 mm
        img_x = col1_x + (col1_w - img_w) / 2.0
        img_y = c12_y + 11.0 * mm
        c.drawImage('poster_assets/energy_flow_diagram.png', img_x, img_y, width=img_w, height=img_h, preserveAspectRatio=True)
        
        cap_text = "<b>Figure 1:</b> Thermodynamic Heat Flow & Energy Evacuation Pathway"
        p_cap = Paragraph(cap_text, styles['caption'])
        p_cap.wrapOn(c, col1_w - 8.0 * mm, 10 * mm)
        p_cap.drawOn(c, col1_x + 4.0 * mm, c12_y + 3.0 * mm)

    # --------------------------------------------------------------------------
    # COLUMN 2: SYSTEM ARCHITECTURE, CUTAWAY & HYSTERESIS CONTROL (HERO)
    # --------------------------------------------------------------------------
    # Card 2.1: System Architecture & Cutaway Visual (H = 141.0 mm)
    c21_h = 141.0 * mm
    c21_y = grid_top - c21_h
    draw_card(c, col2_x, c21_y, col2_w, c21_h)
    draw_section_header(c, "3. SANJIVANI System Architecture & Integration", col2_x, grid_top, col2_w, height=15.5, tag="Hero Cutaway Schematic")
    
    # Hero Cutaway Concept Diagram Placement (Prominently Sized)
    if os.path.exists('poster_assets/cutaway_architecture.png'):
        cut_w = 118.0 * mm
        cut_h = cut_w / 1.404 # 84.0 mm
        cut_x = col2_x + (col2_w - cut_w) / 2.0
        cut_y = c21_y + 38.0 * mm
        c.drawImage('poster_assets/cutaway_architecture.png', cut_x, cut_y, width=cut_w, height=cut_h, preserveAspectRatio=True)
    
    # Engineering Specifications Summary below Image
    key_html = (
        "<b>• Multi-Layer Insulation:</b> 20mm Vacuum Insulation Panels (VIP, k = 0.004 W/m·K) + 25mm PUF casing (UA = 0.147 W/K).<br/>"
        "<b>• Isothermal Buffer:</b> 2.0mm 6061-T6 Al cold spreader + 6x CrodaTherm 5 Bio-PCM packs (4.8 kg, T<sub>melt</sub> = +4.8°C, zero freeze hazard).<br/>"
        "<b>• Solid-State Heat Pump:</b> Dual TEC1-12706 Peltier modules derated to 7.5V / 2.0A (optimal COP = 0.617 sweet spot).<br/>"
        "<b>• Evacuation Subsystem:</b> Microchannel copper cold plate + liquid loop + skived copper heat sink with dual 80mm PWM fans."
    )
    draw_flow_text(c, key_html, styles['body'], col2_x + 4.0 * mm, c21_y + 35.0 * mm, col2_w - 8.0 * mm)
    
    # Card 2.2: Sensor-Triggered Hysteresis Control Logic (H = 69.5 mm)
    c22_y = grid_bottom
    c22_h = c21_y - 4.0 * mm - grid_bottom # 69.5 mm
    draw_card(c, col2_x, c22_y, col2_w, c22_h)
    draw_section_header(c, "4. Sensor-Triggered Hysteresis Control Logic", col2_x, c21_y - 4.0 * mm, col2_w, height=15.5, tag="Closed-Loop Hysteresis")
    
    # Embedded Authentic Flowchart (Left Side of Card 2.2)
    flow_w = 58.0 * mm
    if os.path.exists('poster_assets/control_flowchart.png'):
        flow_h = flow_w / 1.484 # 39.1 mm
        flow_x = col2_x + 4.0 * mm
        flow_y = c22_y + 10.0 * mm
        c.drawImage('poster_assets/control_flowchart.png', flow_x, flow_y, width=flow_w, height=flow_h, preserveAspectRatio=True)
        
        flow_cap = "<b>Figure 2:</b> Closed-Loop Control Cycle"
        p_fc = Paragraph(flow_cap, styles['caption'])
        p_fc.wrapOn(c, flow_w, 8 * mm)
        p_fc.drawOn(c, flow_x, c22_y + 2.5 * mm)
    
    # Operational Rules & Governing Law (Right Side of Card 2.2)
    ctrl_text = (
        "<b>Operational Control Criteria:</b><br/>"
        "<b>• Telemetry:</b> Redundant 1-Wire DS18B20 digital probes (±0.1°C).<br/>"
        "<b>• Active Trigger (T ≥ +6.2°C):</b> Controller energizes Peltier & pump.<br/>"
        "<b>• Passive Cut-Off (T ≤ +3.8°C):</b> Active power cuts off; Bio-PCM buffers.<br/>"
        "<b>• Deadband (ΔT = 2.4°C):</b> Eliminates relay chatter & thermal shock.<br/>"
        "<b>• Critical Law:</b> <i>Peltier modules transfer heat—they do not destroy it. Forced rejection (Q̇<sub>h</sub> = 48.5 W) prevents junction thermal breakdown.</i>"
    )
    ctrl_x = col2_x + flow_w + 6.0 * mm
    ctrl_w = col2_w - flow_w - 9.0 * mm
    draw_flow_text(c, ctrl_text, styles['body'], ctrl_x, c22_y + c22_h - 18.0 * mm, ctrl_w)

    # --------------------------------------------------------------------------
    # COLUMN 3: QUANTITATIVE PERFORMANCE, ECONOMICS & VALIDATION
    # --------------------------------------------------------------------------
    # Card 3.1: 120-Hour Thermal Performance & Simulation (H = 100.0 mm)
    c31_h = 100.0 * mm
    c31_y = grid_top - c31_h
    draw_card(c, col3_x, c31_y, col3_w, c31_h)
    draw_section_header(c, "5. 120-Hour Thermal Performance & Validation", col3_x, grid_top, col3_w, height=15.5, tag="Empirical Model")
    
    # Embedded Performance Simulation Graph
    if os.path.exists('poster_assets/poster_simulation_graph.png'):
        g_w = 116.0 * mm
        g_h = 50.0 * mm
        g_x = col3_x + (col3_w - g_w) / 2.0
        g_y = c31_y + 31.0 * mm
        c.drawImage('poster_assets/poster_simulation_graph.png', g_x, g_y, width=g_w, height=g_h, preserveAspectRatio=True)
    
    # Key Performance Metrics Table below Graph
    kpi_table_data = [
        [Paragraph('<b>Performance Metric</b>', styles['body_bold']), Paragraph('<b>Passive Baseline</b>', styles['body_bold']), Paragraph('<b>SANJIVANI Hybrid</b>', styles['body_bold'])],
        [Paragraph('Safe Hold Duration (+2°C to +8°C)', styles['body']), Paragraph('71.7 Hours', styles['body']), Paragraph('<b>109.4 Hours (+52.6%)</b>', styles['body_bold'])],
        [Paragraph('Active Electrical Runtime', styles['body']), Paragraph('0.0 Hours (Passive)', styles['body']), Paragraph('8.75 Hours (8.0% duty)', styles['body'])],
        [Paragraph('Total Energy Consumed', styles['body']), Paragraph('0.0 Wh', styles['body']), Paragraph('<b>301.2 Wh</b> (12.8V 30Ah pack)', styles['body_bold'])],
    ]
    t_kpi = Table(kpi_table_data, colWidths=[52*mm, 31*mm, 33*mm])
    t_kpi.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
        ('GRID', (0,0), (-1,-1), 0.4, BORDER_CARD),
        ('TOPPADDING', (0,0), (-1,-1), 2.0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.0),
        ('LEFTPADDING', (0,0), (-1,-1), 3.0),
        ('RIGHTPADDING', (0,0), (-1,-1), 3.0),
    ]))
    t_kpi.wrapOn(c, col3_w - 8.0 * mm, 30 * mm)
    t_kpi.drawOn(c, col3_x + 4.0 * mm, c31_y + 3.0 * mm)
    
    # Card 3.2: Bill of Materials & Economic Feasibility (H = 58.0 mm)
    c32_h = 58.0 * mm
    c32_y = c31_y - 4.0 * mm - c32_h
    draw_card(c, col3_x, c32_y, col3_w, c32_h)
    draw_section_header(c, "6. Bill of Materials & Economic Viability", col3_x, c31_y - 4.0 * mm, col3_w, height=15.5, tag="CapEx Analysis")
    
    bom_data = [
        [Paragraph('<b>System Solution</b>', styles['body_bold']), Paragraph('<b>Estimated Cost</b>', styles['body_bold']), Paragraph('<b>Holding Autonomy</b>', styles['body_bold'])],
        [Paragraph('SANJIVANI Field MVP', styles['body']), Paragraph('<b>₹6,480</b> ($78)', styles['body_bold']), Paragraph('109.4 h (Peltier+PCM)', styles['body'])],
        [Paragraph('SANJIVANI Instrumented R&D', styles['body']), Paragraph('<b>₹11,850</b> ($142)', styles['body_bold']), Paragraph('109.4 h + Telemetry', styles['body'])],
        [Paragraph('Commercial Active Solar Cooler', styles['body']), Paragraph('₹45,000–₹1,20,000', styles['body']), Paragraph('Continuous Grid/Solar', styles['body'])],
    ]
    t_bom = Table(bom_data, colWidths=[48*mm, 36*mm, 32*mm])
    t_bom.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
        ('GRID', (0,0), (-1,-1), 0.4, BORDER_CARD),
        ('TOPPADDING', (0,0), (-1,-1), 2.2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.2),
        ('LEFTPADDING', (0,0), (-1,-1), 3.0),
        ('RIGHTPADDING', (0,0), (-1,-1), 3.0),
    ]))
    t_bom.wrapOn(c, col3_w - 8.0 * mm, 30 * mm)
    t_bom.drawOn(c, col3_x + 4.0 * mm, c32_y + 16.5 * mm)
    
    bom_note = (
        "<b>Economic Significance:</b> Delivers an <b>85% capital expenditure reduction</b> relative to compressor-driven vaccine coolers, "
        "eliminating mechanical wear, toxic refrigerants, and costly maintenance."
    )
    draw_flow_text(c, bom_note, styles['body'], col3_x + 4.0 * mm, c32_y + 14.5 * mm, col3_w - 8.0 * mm)
    
    # Card 3.3: Scientific Conclusions & Healthcare Impact (H = 48.5 mm)
    c33_y = grid_bottom
    c33_h = c32_y - 4.0 * mm - grid_bottom # 48.5 mm
    draw_card(c, col3_x, c33_y, col3_w, c33_h)
    draw_section_header(c, "7. Conclusions & Healthcare Translation", col3_x, c32_y - 4.0 * mm, col3_w, height=15.5, tag="ISEF Impact")
    
    concl_text = (
        "<b>• Research Hypothesis Validated:</b> Selectively pulsing Peltier active cooling during peak diurnal heat stress successfully extends holding autonomy past 100 hours (109.4 h achieved) under 28°C–42°C tropical cycling.<br/>"
        "<b>• Accidental Freeze Risk Eliminated:</b> Isothermal phase change of CrodaTherm 5 at +4.8°C guarantees zero freezing exposure (<0°C).<br/>"
        "<b>• Real-World Translation:</b> Portable 12.8V DC battery architecture enables seamless solar PV recharge for last-mile Primary Health Centers."
    )
    draw_flow_text(c, concl_text, styles['body'], col3_x + 4.0 * mm, c33_y + c33_h - 18.0 * mm, col3_w - 8.0 * mm)

    # ==========================================================================
    # C. BOTTOM FOOTER BAR (y = 8.0 to 22.5 mm, H = 14.5 mm)
    # ==========================================================================
    footer_y = 8.0 * mm
    footer_h = 14.5 * mm
    
    c.saveState()
    c.setFillColor(colors.HexColor('#0F172A'))
    c.setStrokeColor(colors.HexColor('#334155'))
    c.setLineWidth(1.0)
    c.roundRect(m_left, footer_y, usable_w, footer_h, 2.5, stroke=1, fill=1)
    
    # Left: Key Literature References
    ref_text = (
        "<font face='Arial-Bold' size=7.2 color='#38BDF8'>KEY REFERENCES: </font>"
        "<font face='Arial' size=6.8 color='#CBD5E1'>"
        "[1] WHO, <i>User guide for cold boxes &amp; vaccine carriers</i>, PQS E004/CB01. &nbsp;|&nbsp; "
        "[2] Sharma &amp; Roy, <i>Thermoelectric Peltier cooling under variable voltage</i>, Appl. Therm. Eng., 2024. &nbsp;|&nbsp; "
        "[3] Riffat &amp; Ma, <i>Thermoelectrics: Review of materials &amp; applications</i>, Int. J. Energy Res., 2023."
        "</font>"
    )
    p_ref = Paragraph(ref_text, ParagraphStyle('FootRef', leading=8.5))
    p_ref.wrapOn(c, usable_w - 70 * mm, 12 * mm)
    p_ref.drawOn(c, m_left + 6.0 * mm, footer_y + 4.0 * mm)
    
    # Right: Event & Official Identification
    c.setFont('Arial-Bold', 7.5)
    c.setFillColor(colors.HexColor('#93C5FD'))
    c.drawRightString(m_right - 6.0 * mm, footer_y + 4.5 * mm, "ALLOTTED SCHOOL UID: SBVPH-05  |  SENIOR BAL VIGYAN 2026–2027")
    c.restoreState()
    
    # Finalize PDF page
    c.showPage()
    c.save()
    print(f"Successfully generated {pdf_path}")

if __name__ == '__main__':
    generate_sanjivani_a3_poster()
