import os
import sys
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Color Palette Definitions
    DARK_BG = RGBColor(6, 11, 20)        # #060B14
    DARK_CARD = RGBColor(11, 21, 40)     # #0B1528
    CARD_BORDER = RGBColor(30, 41, 59)   # #1E293B
    TEAL_ACCENT = RGBColor(20, 184, 166) # #14B8A6
    CYAN_ACCENT = RGBColor(56, 189, 248) # #38BDF8
    AMBER_ACCENT = RGBColor(245, 158, 11)# #F59E0B
    ROSE_ACCENT = RGBColor(244, 63, 94)  # #F43F5E
    GREEN_ACCENT = RGBColor(16, 185, 129)# #10B981
    WHITE = RGBColor(255, 255, 255)
    SLATE_LIGHT = RGBColor(203, 213, 225) # #CBD5E1
    SLATE_MUTED = RGBColor(148, 163, 184) # #94A3B8
    SLATE_DARK = RGBColor(71, 85, 105)   # #475569

    def add_base_slide(tag, title, subtitle, slide_idx, total_slides=25):
        slide = prs.slides.add_slide(blank_layout)
        
        # Slide Background
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = DARK_BG
        bg.line.fill.background()

        # Top Accent Glow Line
        top_glow = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.4), Inches(11.733), Inches(0.04))
        top_glow.fill.solid()
        top_glow.fill.fore_color.rgb = TEAL_ACCENT
        top_glow.line.fill.background()

        # Header Text Box
        header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.733), Inches(1.1))
        tf = header_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        # Tag
        p_tag = tf.paragraphs[0]
        p_tag.text = f"[ {tag.upper()} ]"
        p_tag.font.size = Pt(10)
        p_tag.font.bold = True
        p_tag.font.name = "Segoe UI"
        p_tag.font.color.rgb = TEAL_ACCENT

        # Title
        p_title = tf.add_paragraph()
        p_title.text = title
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.name = "Segoe UI"
        p_title.font.color.rgb = WHITE
        p_title.space_before = Pt(2)

        # Subtitle
        if subtitle:
            p_sub = tf.add_paragraph()
            p_sub.text = subtitle
            p_sub.font.size = Pt(11)
            p_sub.font.name = "Segoe UI"
            p_sub.font.color.rgb = SLATE_MUTED
            p_sub.space_before = Pt(2)

        # Bottom Footer
        footer_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.05), Inches(11.733), Inches(0.35))
        ftf = footer_box.text_frame
        ftf.word_wrap = True
        ftf.margin_left = ftf.margin_top = ftf.margin_right = ftf.margin_bottom = 0
        fp = ftf.paragraphs[0]
        fp.text = f"SANJIVANI (संजीवनी) | Dr. B. K. Passi Balvigyan 2026–27 | Physics (SBVPH-05) | G. D. Goenka Public School, Indore | Slide {slide_idx:02d} of {total_slides:02d}"
        fp.font.size = Pt(9)
        fp.font.name = "Segoe UI"
        fp.font.color.rgb = SLATE_DARK

        return slide

    def add_card(slide, left, top, width, height, border_color=CARD_BORDER, bg_color=DARK_CARD):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1)
        return card

    # =========================================================================
    # SLIDE 01: HERO COVER
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = DARK_BG
    bg1.line.fill.background()

    # Top Tag
    tb1_tag = s1.shapes.add_textbox(Inches(1.0), Inches(0.8), Inches(11.333), Inches(0.4))
    tf1_tag = tb1_tag.text_frame
    p = tf1_tag.paragraphs[0]
    p.text = "DR. B. K. PASSI MEMORIAL SENIOR BALVIGYAN 2026–2027  •  SUBJECT: PHYSICS  •  CODE: SBVPH-05"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = TEAL_ACCENT

    # Main Title Box
    tb1_title = s1.shapes.add_textbox(Inches(1.0), Inches(1.2), Inches(11.333), Inches(2.2))
    tf1_title = tb1_title.text_frame
    tf1_title.word_wrap = True
    p_main = tf1_title.paragraphs[0]
    p_main.text = "SANJIVANI (संजीवनी)"
    p_main.font.size = Pt(46)
    p_main.font.bold = True
    p_main.font.color.rgb = WHITE

    p_sub1 = tf1_title.add_paragraph()
    p_sub1.text = "A Hybrid Thermoelectric–Biochemical Active/Passive Cold-Chain Carrier for Vulnerable Last-Mile Vaccine Distribution"
    p_sub1.font.size = Pt(18)
    p_sub1.font.bold = True
    p_sub1.font.color.rgb = CYAN_ACCENT
    p_sub1.space_before = Pt(8)

    p_sub2 = tf1_title.add_paragraph()
    p_sub2.text = "Solving the tropical cold-chain failure paradox through derated Peltier heat pumping, high-latent bio-PCM buffers, and vacuum insulation."
    p_sub2.font.size = Pt(13)
    p_sub2.font.color.rgb = SLATE_MUTED
    p_sub2.space_before = Pt(6)

    # 4 Key Stat Cards
    metrics = [
        ("109.4 HOURS", "+52.8% Autonomy", "Holding time at 38°C ambient vs 71.8h baseline", TEAL_ACCENT),
        ("ZERO FREEZE", "0.0% Cold Shock", "Strict isothermal buffer at +5.0°C; 0 freeze events", GREEN_ACCENT),
        ("₹12,450 BOM", "Target ₹8,900 Scale", "Ultra-frugal bill of materials (vs ₹65,000 active fridges)", AMBER_ACCENT),
        ("6.5 LITRES", "24 Standard 10R Vials", "Optimized payload envelope for primary immunization", CYAN_ACCENT)
    ]
    card_w = Inches(2.7)
    gap = Inches(0.24)
    start_x = Inches(1.0)
    for i, (m_val, m_sub, m_desc, col) in enumerate(metrics):
        cx = start_x + i * (card_w + gap)
        add_card(s1, cx, Inches(3.7), card_w, Inches(1.9), border_color=col)
        tb_card = s1.shapes.add_textbox(cx + Inches(0.15), Inches(3.8), card_w - Inches(0.3), Inches(1.7))
        tfc = tb_card.text_frame
        tfc.word_wrap = True
        
        p0 = tfc.paragraphs[0]
        p0.text = m_val
        p0.font.size = Pt(20)
        p0.font.bold = True
        p0.font.color.rgb = col
        
        p1 = tfc.add_paragraph()
        p1.text = m_sub
        p1.font.size = Pt(11)
        p1.font.bold = True
        p1.font.color.rgb = WHITE
        p1.space_before = Pt(4)

        p2 = tfc.add_paragraph()
        p2.text = m_desc
        p2.font.size = Pt(9)
        p2.font.color.rgb = SLATE_MUTED
        p2.space_before = Pt(4)

    # Footer Info Bar
    tb1_foot = s1.shapes.add_textbox(Inches(1.0), Inches(5.9), Inches(11.333), Inches(1.0))
    tf1_foot = tb1_foot.text_frame
    tf1_foot.word_wrap = True
    pf1 = tf1_foot.paragraphs[0]
    pf1.text = "Student Investigators: Daksh Sharma & Yashveer Solanki  |  Faculty Mentor: Dr. Ankit Soni"
    pf1.font.size = Pt(13)
    pf1.font.bold = True
    pf1.font.color.rgb = WHITE

    pf2 = tf1_foot.add_paragraph()
    pf2.text = "Institution: G. D. Goenka Public School, Indore  |  Affiliation: CBSE Affiliation No. 1030588  |  Academic Year: 2026–2027"
    pf2.font.size = Pt(10)
    pf2.font.color.rgb = SLATE_MUTED
    pf2.space_before = Pt(3)

    # =========================================================================
    # SLIDE 02: RESEARCH TEAM & INSTITUTIONAL ACCREDITATION
    # =========================================================================
    s2 = add_base_slide("Academic Accreditation", "Research Team & Institutional Credentials", "Dr. B. K. Passi Memorial Senior Balvigyan 2026–2027 | Subject: Physics", 2)
    
    # Left Card: Student Investigators
    add_card(s2, Inches(0.8), Inches(1.8), Inches(5.7), Inches(4.9), TEAL_ACCENT)
    tb = s2.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(5.1), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = "STUDENT INVESTIGATORS"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = TEAL_ACCENT

    p = tf.add_paragraph()
    p.text = "Daksh Sharma"
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.space_before = Pt(6)

    p = tf.add_paragraph()
    p.text = "Lead Physics Modeling & Thermodynamic Systems Architecture\n• Formulated Fourier multi-layer conduction models & VIP thermal resistance\n• Derived derated Peltier COP balance & CrodaTherm 5 phase-change enthalpy\n• Designed closed-loop hysteresis control parameters & empirical holding tests"
    p.font.size = Pt(10)
    p.font.color.rgb = SLATE_LIGHT
    p.space_before = Pt(3)

    p = tf.add_paragraph()
    p.text = "Yashveer Solanki"
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.space_before = Pt(14)

    p = tf.add_paragraph()
    p.text = "Hardware Integration & Embedded Electronics Architecture\n• Programmed 10 Hz 1-Wire DS18B20 multi-point sensor acquisition & fail-safes\n• Designed MOSFET PWM switching stages, LiFePO4 BMS, and buck converters\n• Built 3D CAD parametric enclosures and heat sink vapor-chamber thermal paths"
    p.font.size = Pt(10)
    p.font.color.rgb = SLATE_LIGHT
    p.space_before = Pt(3)

    # Right Card: Institutional Mentor & Lab
    add_card(s2, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.9), CYAN_ACCENT)
    tb = s2.shapes.add_textbox(Inches(7.1), Inches(2.0), Inches(5.1), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "FACULTY MENTOR & INSTITUTION"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT

    p = tf.add_paragraph()
    p.text = "Dr. Ankit Soni"
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.space_before = Pt(6)

    p = tf.add_paragraph()
    p.text = "Postgraduate Teacher in Physics, Department of Science\nG. D. Goenka Public School, Indore\n• Guided First Law energy balance and thermal circuit network formulation\n• Supervised rigorous empirical calibration against calibrated laboratory probes\n• Mentored technical documentation, FMEA analysis, and Balvigyan defense"
    p.font.size = Pt(10)
    p.font.color.rgb = SLATE_LIGHT
    p.space_before = Pt(3)

    p = tf.add_paragraph()
    p.text = "Institutional Laboratory Validation"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.space_before = Pt(16)

    p = tf.add_paragraph()
    p.text = "• Advanced Physics Lab & Mechatronics Workshop, GDGPS Indore\n• Data Logging: Keysight 34972A multi-channel DAQ + Fluke 52-II Thermometer\n• Climate Chamber: Thermal simulation bench (+28°C to +45°C cyclic control)\n• Ethical Compliance: Non-clinical simulation using inert saline vaccine vials"
    p.font.size = Pt(10)
    p.font.color.rgb = SLATE_LIGHT
    p.space_before = Pt(4)

    # =========================================================================
    # SLIDE 03: EXECUTIVE SUMMARY & BREAKTHROUGH VALUE
    # =========================================================================
    s3 = add_base_slide("Executive Summary", "The SANJIVANI Paradigm: Frugal Physics for Global Health", "How a dual active/passive architecture outlasts conventional ice-boxes by 52.8% at a fraction of the cost", 3)
    
    # 3 Column Cards
    col_w = Inches(3.7)
    gap = Inches(0.3)
    
    # Col 1: The Dilemma
    add_card(s3, Inches(0.8), Inches(1.8), col_w, Inches(4.9), ROSE_ACCENT)
    tb = s3.shapes.add_textbox(Inches(1.0), Inches(2.0), col_w - Inches(0.4), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "1. THE COLD-CHAIN DILEMMA"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ROSE_ACCENT
    p = tf.add_paragraph()
    p.text = "Fragile Ice & Heavy Fridges"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.space_before = Pt(4)
    p = tf.add_paragraph()
    p.text = "• 25–50% of vaccines spoil globally due to broken cold chains in remote regions.\n\n• Ice packs freeze vaccines at 0°C (13.5% damage rate) or melt prematurely in 45°C summer heat.\n\n• Compressor-based fridges weigh >18 kg, cost ₹65,000+, and fail on unpaved motorcycle tracks."
    p.font.size = Pt(10)
    p.font.color.rgb = SLATE_LIGHT
    p.space_before = Pt(8)

    # Col 2: The Solution
    add_card(s3, Inches(0.8) + col_w + gap, Inches(1.8), col_w, Inches(4.9), TEAL_ACCENT)
    tb = s3.shapes.add_textbox(Inches(1.0) + col_w + gap, Inches(2.0), col_w - Inches(0.4), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "2. SANJIVANI BREAKTHROUGH"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = TEAL_ACCENT
    p = tf.add_paragraph()
    p.text = "Hybrid Synergistic Engine"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.space_before = Pt(4)
    p = tf.add_paragraph()
    p.text = "• Passive Baseline: 4.8 kg CrodaTherm 5 Bio-PCM holds chamber locked at +5.0°C with ZERO electrical drain.\n\n• Active Pulse: Derated Peltier heat pump runs on 8.0% duty cycle only when ambient heat spikes.\n\n• Super Insulation: 20mm VIP + 25mm PUF yields ultra-low conductance (UA = 0.147 W/K)."
    p.font.size = Pt(10)
    p.font.color.rgb = SLATE_LIGHT
    p.space_before = Pt(8)

    # Col 3: The Impact
    add_card(s3, Inches(0.8) + (col_w + gap) * 2, Inches(1.8), col_w, Inches(4.9), GREEN_ACCENT)
    tb = s3.shapes.add_textbox(Inches(1.0) + (col_w + gap) * 2, Inches(2.0), col_w - Inches(0.4), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "3. MEASURED IMPACT"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = GREEN_ACCENT
    p = tf.add_paragraph()
    p.text = "109.4h at ₹12,450 BOM"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.space_before = Pt(4)
    p = tf.add_paragraph()
    p.text = "• +52.8% Autonomy Boost: 109.4 hours holding time under relentless 38°C heat.\n\n• Zero Freezing: Absolute elimination of sub-zero ice-pack freeze shock.\n\n• Economic Payback: Recoups capital cost in 1.4 years via prevented vaccine waste at a primary health centre.\n\n• Scalable: ₹8,900 target production BOM."
    p.font.size = Pt(10)
    p.font.color.rgb = SLATE_LIGHT
    p.space_before = Pt(8)

    # =========================================================================
    # SLIDE 04: THE COLD-CHAIN CRISIS
    # =========================================================================
    s4 = add_base_slide("Global & National Context", "The Last-Mile Cold-Chain Crisis: Where Vaccines Perish", "Why 25% to 50% of life-saving immunizations are destroyed before reaching the child", 4)
    
    # Left Side: Statistics & Narrative
    add_card(s4, Inches(0.8), Inches(1.8), Inches(6.8), Inches(4.9))
    tb = s4.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(6.4), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = "THE SCALE OF THE DISASTER"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ROSE_ACCENT

    p = tf.add_paragraph()
    p.text = "Over 50% Vaccine Spoilage in Tropical Last Miles"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.space_before = Pt(4)

    p = tf.add_paragraph()
    p.text = "• WHO & UNICEF Telemetry: Between 25% and 50% of all vaccines distributed globally degrade or lose potency during transit before injection.\n\n• Financial Burden: Over $50 Million to $300 Million lost annually in India alone from spoiled biopharmaceuticals.\n\n• The Last-Mile Bottleneck: In India's Universal Immunization Programme (UIP), 26,000 cold-chain points serve 392,000 sub-centres. The final 5 to 50 kilometres require foot, bicycle, or motorcycle transport in +42°C to +47°C heat.\n\n• Power Blackouts: Rural sub-centres suffer frequent 8 to 14 hour electrical blackouts, disabling standard compressor coolers."
    p.font.size = Pt(10.5)
    p.font.color.rgb = SLATE_LIGHT
    p.space_before = Pt(8)

    # Right Side: Real photo + Callout
    if os.path.exists('website/public/assets/photos/rural_clinic.jpg'):
        s4.shapes.add_picture('website/public/assets/photos/rural_clinic.jpg', Inches(7.9), Inches(1.8), Inches(4.6), Inches(2.6))
    
    add_card(s4, Inches(7.9), Inches(4.6), Inches(4.6), Inches(2.1), border_color=AMBER_ACCENT)
    tb = s4.shapes.add_textbox(Inches(8.1), Inches(4.7), Inches(4.2), Inches(1.9))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "CRITICAL COLD-CHAIN STATS"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = AMBER_ACCENT
    p = tf.add_paragraph()
    p.text = "2.8 Million Children Unprotected"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.space_before = Pt(2)
    p = tf.add_paragraph()
    p.text = "Each year, millions of infants receive thermally degraded, ineffective vaccines because temperature breaches leave no visual trace in liquid vials."
    p.font.size = Pt(9.5)
    p.font.color.rgb = SLATE_MUTED
    p.space_before = Pt(4)

    # =========================================================================
    # SLIDE 05: THE BIOLOGICAL STAKES: PROTEIN DENATURATION
    # =========================================================================
    s5 = add_base_slide("Biomedical Imperative", "The Biological Stakes: Protein Denaturation vs Adjuvant Agglutination", "Vaccines exist on a razor's edge: destruction occurs both above +8.0°C and below +2.0°C", 5)

    # Left: Upper Breach (>8°C)
    add_card(s5, Inches(0.8), Inches(1.8), Inches(5.7), Inches(4.9), border_color=ROSE_ACCENT)
    tb = s5.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.3), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "UPPER THERMAL BREACH (> +8.0°C)"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ROSE_ACCENT
    p = tf.add_paragraph()
    p.text = "Irreversible Protein Denaturation"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.space_before = Pt(4)
    p = tf.add_paragraph()
    p.text = "• Structural Unfolding: Temperatures above +8.0°C disrupt hydrogen bonds, hydrophobic interactions, and tertiary/quaternary polypeptide folding.\n\n• Viral Envelope Inactivation: Live-attenuated vaccines (Measles, Rubella, Polio, Rotavirus) lose membrane integrity; antigenic epitopes lose receptor binding affinity.\n\n• Cumulative Degradation: Thermal exposure is irreversible. A vial exposed to 25°C for 4 hours loses up to 60% of its protective titre permanently."
    p.font.size = Pt(10)
    p.font.color.rgb = SLATE_LIGHT
    p.space_before = Pt(8)

    # Right: Lower Breach (<2°C)
    add_card(s5, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.9), border_color=CYAN_ACCENT)
    tb = s5.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "LOWER THERMAL BREACH (< +2.0°C)"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT
    p = tf.add_paragraph()
    p.text = "Adjuvant Agglutination & Freezing Shock"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.space_before = Pt(4)
    p = tf.add_paragraph()
    p.text = "• The Aluminium Adjuvant Hazard: Freeze-sensitive vaccines (Hepatitis B, DTP, Tetanus Toxoid, HPV, Pentavalent) rely on aluminium hydroxide or phosphate adjuvants.\n\n• Microscopic Crystal Growth: Freezing causes ice lattice formation that forces adjuvant colloids to irreversibly coagulate and aggregate into heavy sediment.\n\n• Antigen Detachment: Bound proteins dissociate from adjuvants; immune response drops to zero, and large precipitates cause sterile abscesses at injection sites."
    p.font.size = Pt(10)
    p.font.color.rgb = SLATE_LIGHT
    p.space_before = Pt(8)

    # =========================================================================
    # SLIDE 06: THE FREEZE-ABUSE PARADOX
    # =========================================================================
    s6 = add_base_slide("Root Cause Analysis", "The Freeze-Abuse Paradox: Conventional Ice Packs Destroy Vaccines", "Field surveys reveal that improperly conditioned water ice packs cause more damage than heatwaves", 6)

    # 2 Column layout
    add_card(s6, Inches(0.8), Inches(1.8), Inches(6.0), Inches(4.9))
    tb = s6.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.6), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "THE 0°C WATER ICE PROBLEM"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = AMBER_ACCENT
    p = tf.add_paragraph()
    p.text = "Why Frozen Water is the Worst Choice"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.space_before = Pt(4)
    p = tf.add_paragraph()
    p.text = "1. Thermodynamic Mismatch: Water freezes and melts at 0.0°C. But vaccines MUST stay between +2.0°C and +8.0°C. There is zero safety margin.\n\n2. The Conditioning Trap: Health workers are instructed to 'condition' ice packs by leaving them at room temp until sloshing occurs. In practice, rush or lack of time leads to unconditioned packs placed directly adjacent to glass vials.\n\n3. Rapid Flash Freezing: Direct contact with 0°C to -10°C ice packs cools 2-3 mL glass vials to sub-zero within 35 minutes, destroying adjuvant binding.\n\n4. WHO Field Data: Up to 21.9% of vaccine vials in developing nations show signs of accidental freeze damage upon arrival."
    p.font.size = Pt(10)
    p.font.color.rgb = SLATE_LIGHT
    p.space_before = Pt(8)

    # Right side: Visual comparison card
    add_card(s6, Inches(7.1), Inches(1.8), Inches(5.4), Inches(4.9), border_color=TEAL_ACCENT)
    tb = s6.shapes.add_textbox(Inches(7.3), Inches(2.0), Inches(5.0), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "THE SANJIVANI CONTRAST"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = TEAL_ACCENT
    p = tf.add_paragraph()
    p.text = "Bio-PCM +5.0°C Isothermal Buffer"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.space_before = Pt(4)
    p = tf.add_paragraph()
    p.text = "• Isothermal Phase Transition at +5.0°C: CrodaTherm 5 transitions exactly at +5.0°C — the exact mathematical center of the +2°C to +8°C safety window.\n\n• Physical Impossibility of Freezing: Even if placed in direct physical contact with vials, the PCM CANNOT cool below +5.0°C during passive discharge.\n\n• 0% Freeze Failure Rate: Completely eliminates the need for field conditioning, eliminating human error from the last mile."
    p.font.size = Pt(10)
    p.font.color.rgb = SLATE_LIGHT
    p.space_before = Pt(8)

    # =========================================================================
    # SLIDE 07: BOTTLENECKS OF EXISTING TECHNOLOGIES
    # =========================================================================
    s7 = add_base_slide("State-of-the-Art Analysis", "The 4 Fatal Bottlenecks of Existing Cold-Chain Technologies", "Why current commercial systems fail the demanding requirements of rural Indian transit", 7)
    
    bottlenecks = [
        ("BOTTLENECK 01", "Passive Ice Boxes", "High Freeze Risk & Rapid Decay", "Water ice packs melt in <24h in 40°C heat; zero active intervention when ice melts; high risk of flash-freezing vaccines when fresh out of the freezer.", ROSE_ACCENT),
        ("BOTTLENECK 02", "Compressor Refrigerators", "Extreme Mass & Fragility", "Compressor systems weigh >18–25 kg, cost ₹65,000–₹1,50,000, contain delicate capillary tubing, and cannot survive bumpy motorcycle or foot trails.", AMBER_ACCENT),
        ("BOTTLENECK 03", "Continuous Active Coolers", "Severe Battery Depletion", "Running a thermoelectric chip continuously at 12V 5A consumes 60W, exhausting a heavy 150Wh battery in less than 2.5 hours.", CYAN_ACCENT),
        ("BOTTLENECK 04", "Passive-Only PCM Boxes", "Thermal Drift & Depletion", "Once a passive PCM pack melts, it cannot regenerate in the field. When ambient temperatures exceed 42°C, heat ingress overwhelms passive walls.", WHITE)
    ]
    b_w = Inches(5.6)
    b_h = Inches(2.25)
    coords = [(Inches(0.8), Inches(1.8)), (Inches(6.8), Inches(1.8)), (Inches(0.8), Inches(4.45)), (Inches(6.8), Inches(4.45))]
    
    for (tag, title, sub, desc, col), (x, y) in zip(bottlenecks, coords):
        add_card(s7, x, y, b_w, b_h, border_color=col)
        tb = s7.shapes.add_textbox(x + Inches(0.2), y + Inches(0.15), b_w - Inches(0.4), b_h - Inches(0.3))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = tag
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = col
        
        p = tf.add_paragraph()
        p.text = title + " — " + sub
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = WHITE
        p.space_before = Pt(2)

        p = tf.add_paragraph()
        p.text = desc
        p.font.size = Pt(9.5)
        p.font.color.rgb = SLATE_LIGHT
        p.space_before = Pt(4)

    # =========================================================================
    # SLIDE 08: THE CORE BREAKTHROUGH: HYBRID SYNERGY
    # =========================================================================
    s8 = add_base_slide("Architectural Breakthrough", "The SANJIVANI Synergistic Engine: Passive Buffer + Active Pulse", "How biochemical latent heat fusion and derated solid-state heat pumping work as one", 8)

    # Left: Explanation
    add_card(s8, Inches(0.8), Inches(1.8), Inches(6.5), Inches(4.9), border_color=TEAL_ACCENT)
    tb = s8.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(6.1), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "THE SYNERGISTIC PRINCIPLE"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = TEAL_ACCENT
    p = tf.add_paragraph()
    p.text = "Never Waste Power When Physics Works for Free"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.space_before = Pt(4)
    p = tf.add_paragraph()
    p.text = "1. Passive Thermal Baseline:\nUnder normal transit, the 4.8 kg CrodaTherm 5 Bio-PCM absorbs heat ingress at 0W power consumption, holding chamber temperature rock-steady at +5.0°C.\n\n2. Intermittent Active Peltier Pulse:\nOnly when ambient temperatures spike to 40°C–45°C and chamber temperature creeps toward +5.8°C does the microcontroller energize the dual TEC1-12706 Peltier modules.\n\n3. Sub-Zero Cooling Without Freezing Risk:\nThe Peltier cold face extracts heat directly into the PCM thermal reservoir, actively re-solidifying melted PCM without subjecting vaccine vials to local freeze points.\n\n4. 8.0% Duty Cycle Advantage:\nActive cooling is active only 8% of the mission duration (5 minutes per hour), multiplying battery autonomy from 6 hours to over 96 hours!"
    p.font.size = Pt(10)
    p.font.color.rgb = SLATE_LIGHT
    p.space_before = Pt(6)

    # Right: Diagram / Energy Flow
    if os.path.exists('website/public/assets/energy_flow_diagram.png'):
        s8.shapes.add_picture('website/public/assets/energy_flow_diagram.png', Inches(7.6), Inches(1.8), Inches(4.9), Inches(4.9))
    else:
        add_card(s8, Inches(7.6), Inches(1.8), Inches(4.9), Inches(4.9), border_color=CYAN_ACCENT)
        tb = s8.shapes.add_textbox(Inches(7.8), Inches(2.0), Inches(4.5), Inches(4.5))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = "ENERGY DYNAMICS"
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = CYAN_ACCENT

    # =========================================================================
    # SLIDE 09: THERMODYNAMIC PRINCIPLES & GOVERNING EQUATIONS
    # =========================================================================
    s9 = add_base_slide("Mathematical Modeling", "Thermodynamic Principles & Governing Physical Equations", "Rigorous first-principles thermal circuit derivation and energy conservation balance", 9)

    eq_cards = [
        ("EQUATION 01: LATENT HEAT FUSION", "Bio-PCM Phase Absorption", "Q_PCM = m · L_f = 4.8 kg × 218 kJ/kg = 1,046.4 kJ (290.7 Wh)", "The latent heat of fusion provides a massive isothermal thermal capacity, absorbing heat during solid-to-liquid transition at +5.0°C without increasing temperature.", TEAL_ACCENT),
        ("EQUATION 02: THERMOELECTRIC ENERGY BALANCE", "Peltier First Law Balance", "Q_hot = Q_cold + P_elec = 18.5 W + 30.0 W = 48.5 W", "By conservation of energy, the heat rejected through the exterior heat sink equals the heat pumped from the cold chamber plus electrical power consumed by the semiconductor junctions.", CYAN_ACCENT),
        ("EQUATION 03: FOURIER MULTI-LAYER CONDUCTION", "Composite Wall Heat Flux", "q = -k A (dT/dx)   -->   UA = 0.147 W/K", "Fourier's law across the serial composite (LLDPE + 25mm PUF + 20mm VIP) yields an overall thermal conductance of 0.147 W/K, limiting heat ingress at 40°C ambient to just 5.15 W.", AMBER_ACCENT)
    ]

    for i, (tag, title, formula, desc, col) in enumerate(eq_cards):
        y = Inches(1.8) + i * Inches(1.65)
        add_card(s9, Inches(0.8), y, Inches(11.733), Inches(1.45), border_color=col)
        tb = s9.shapes.add_textbox(Inches(1.1), y + Inches(0.12), Inches(11.2), Inches(1.2))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = tag + "  •  " + title
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = col

        p = tf.add_paragraph()
        p.text = formula
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.name = "Consolas"
        p.font.color.rgb = WHITE
        p.space_before = Pt(3)

        p = tf.add_paragraph()
        p.text = desc
        p.font.size = Pt(9.5)
        p.font.color.rgb = SLATE_LIGHT
        p.space_before = Pt(3)

    # =========================================================================
    # SLIDE 10: PHASE CHANGE MATERIAL CHEMISTRY
    # =========================================================================
    s10 = add_base_slide("Biochemical Engineering", "Bio-Based Phase Change Material: CrodaTherm 5 Organic Ester", "Why 100% plant-based organic esters supersede traditional paraffin and salt hydrates", 10)

    # Left: Properties
    add_card(s10, Inches(0.8), Inches(1.8), Inches(6.0), Inches(4.9), border_color=TEAL_ACCENT)
    tb = s10.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.6), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "CHEMICAL & THERMAL SPECIFICATIONS"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = TEAL_ACCENT
    p = tf.add_paragraph()
    p.text = "CrodaTherm 5 Bio-Organic Ester"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.space_before = Pt(4)
    p = tf.add_paragraph()
    p.text = "• Melting Peak Temperature: +5.0°C (Exact WHO target midpoint)\n• Latent Heat of Fusion: 218 kJ/kg (Highest organic latent capacity)\n• Total Mass in Jacket: 4.8 kg across perimeter pouches\n• Total Latent Energy: 1,046.4 kJ (290.7 Watt-hours)\n• Specific Heat (Liquid): 2.15 kJ/kg·K  |  Solid: 1.85 kJ/kg·K\n• Density: 875 kg/m³ (Liquid)  |  920 kg/m³ (Solid)\n• Volume Expansion on Phase Change: < 5% (zero burst pressure)"
    p.font.size = Pt(10.5)
    p.font.color.rgb = SLATE_LIGHT
    p.space_before = Pt(8)

    # Right: Advantages Over Paraffin & Hydrates
    add_card(s10, Inches(7.1), Inches(1.8), Inches(5.4), Inches(4.9), border_color=GREEN_ACCENT)
    tb = s10.shapes.add_textbox(Inches(7.3), Inches(2.0), Inches(5.0), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "SUPERIORITY OVER ALTERNATIVES"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = GREEN_ACCENT
    p = tf.add_paragraph()
    p.text = "Why CrodaTherm 5 Wins"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.space_before = Pt(4)
    p = tf.add_paragraph()
    p.text = "1. Zero Supercooling:\nUnlike inorganic salt hydrates that require cooling to -5°C before freezing initiates, CrodaTherm 5 crystallizes crisply at +4.8°C with zero supercooling additives.\n\n2. 10,000+ Cycle Stability:\nOrganic fatty acid esters maintain identical DSC melting peaks over 10,000 cycles with zero phase separation or thermal degradation.\n\n3. Non-Toxic & Biodegradable:\n100% renewable bio-based feedstock derived from plant oils. FDA/EU compliant for incidental contact, non-corrosive to aluminium."
    p.font.size = Pt(10)
    p.font.color.rgb = SLATE_LIGHT
    p.space_before = Pt(8)

    # =========================================================================
    # SLIDE 11: DERATED THERMOELECTRIC ENGINE ARCHITECTURE
    # =========================================================================
    s11 = add_base_slide("Solid-State Physics", "Derated Solid-State Thermoelectric Engine Architecture", "Operating dual TEC1-12706 Peltier modules at optimal electrical efficiency points", 11)

    # Left: Physics of Derating
    add_card(s11, Inches(0.8), Inches(1.8), Inches(6.8), Inches(4.9), border_color=CYAN_ACCENT)
    tb = s11.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(6.4), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "THE DERATING BREAKTHROUGH"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT
    p = tf.add_paragraph()
    p.text = "Maximizing COP: 7.5V / 2.0A Operation"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.space_before = Pt(4)
    p = tf.add_paragraph()
    p.text = "• The Joule Heating Dilemma ($I^2 R$):\nPeltier modules exhibit internal resistance (~1.8 Ω). At max 12V 6A, internal Joule heating consumes 64.8W, dropping COP to an abysmal ~0.22.\n\n• Derated Sweet Spot:\nBy derating each module to 7.50 V and 2.0 A (15.0 W per chip), internal Joule heating drops by 89%, pushing the Coefficient of Performance to peak at COP = 0.617.\n\n• Thermal Parallel / Electrical Series:\nDual chips are wired in electrical series (15V rail or 7.5V PWM) while their cold faces are thermally coupled in parallel across the aluminium spreader plate.\n\n• Cooling Capacity:\nDelivers 18.5 W of net cold heat extraction at ΔT = 25°C, perfectly countering midday thermal influx."
    p.font.size = Pt(10)
    p.font.color.rgb = SLATE_LIGHT
    p.space_before = Pt(8)

    # Right: Photo & Stats
    if os.path.exists('website/public/assets/photos/thermoelectric_chip.jpg'):
        s11.shapes.add_picture('website/public/assets/photos/thermoelectric_chip.jpg', Inches(7.9), Inches(1.8), Inches(4.6), Inches(2.6))
    
    add_card(s11, Inches(7.9), Inches(4.6), Inches(4.6), Inches(2.1), border_color=TEAL_ACCENT)
    tb = s11.shapes.add_textbox(Inches(8.1), Inches(4.7), Inches(4.2), Inches(1.9))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "SOLID-STATE ADVANTAGES"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = TEAL_ACCENT
    p = tf.add_paragraph()
    p.text = "Zero Moving Parts, Zero Gas"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.space_before = Pt(2)
    p = tf.add_paragraph()
    p.text = "No compressors, no flammable HFC refrigerants, zero vibration. Completely immune to shock, inversion, and rough terrain drops."
    p.font.size = Pt(9.5)
    p.font.color.rgb = SLATE_MUTED
    p.space_before = Pt(4)

    # =========================================================================
    # SLIDE 12: MULTI-LAYER THERMAL ENVELOPE
    # =========================================================================
    s12 = add_base_slide("Thermal Insulation", "Advanced Multi-Layer Thermal Envelope: VIP + PUF + LLDPE", "Engineering a composite barrier with an ultra-low conductance of UA = 0.147 W/K", 12)

    layers = [
        ("LAYER 1: OUTER SHELL", "4mm Roto-Molded LLDPE", "k = 0.33 W/m·K", "High-density linear low-density polyethylene provides structural armor against 1.5-meter drop impacts, IP65 water seal, and UV solar reflection pigments.", WHITE),
        ("LAYER 2: STRUCTURAL FOAM", "25mm High-Density PUF Core", "k = 0.022 W/m·K", "Closed-cell polyurethane foam injected at 42 kg/m³ provides mechanical rigidity, thermal bridging elimination, and secondary insulative dampening.", AMBER_ACCENT),
        ("LAYER 3: NANO-POROUS BARRIER", "20mm Vacuum Insulation Panels (VIP)", "k = 0.004 W/m·K", "Fumed silica core evacuated to < 1 mbar in a multi-layer metallized barrier envelope. Provides 5x to 8x higher thermal resistance than conventional foam.", CYAN_ACCENT),
        ("TOTAL COMPOSITE PERFORMANCE", "Thermal Conductance: UA = 0.147 W/K", "Heat Influx @ 40°C: 5.15 W", "The combined wall achieves an equivalent R-value exceeding R-38 (m²·K/W = 6.8), restricting total heat ingress under extreme heat to just 5.15 Watts.", GREEN_ACCENT)
    ]

    for i, (l_tag, l_title, l_k, l_desc, col) in enumerate(layers):
        y = Inches(1.8) + i * Inches(1.25)
        add_card(s12, Inches(0.8), y, Inches(11.733), Inches(1.1), border_color=col)
        tb = s12.shapes.add_textbox(Inches(1.1), y + Inches(0.1), Inches(11.2), Inches(0.9))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = l_tag + "  |  " + l_k
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = col

        p = tf.add_paragraph()
        p.text = l_title + "  —  " + l_desc
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = WHITE
        p.space_before = Pt(2)

    # =========================================================================
    # SLIDE 13: 3D SYSTEM ARCHITECTURE & 13 SUBSYSTEMS
    # =========================================================================
    s13 = add_base_slide("Mechanical Architecture", "3D System Cutaway: 13 Precision-Engineered Subsystems", "Physical breakdown of the complete active/passive carrier assembly", 13)

    if os.path.exists('website/public/assets/cutaway_architecture_clean.png'):
        s13.shapes.add_picture('website/public/assets/cutaway_architecture_clean.png', Inches(0.8), Inches(1.8), Inches(7.2), Inches(4.9))
    
    # Right Side: 13 Subsystems Legend Card
    add_card(s13, Inches(8.3), Inches(1.8), Inches(4.2), Inches(4.9), border_color=TEAL_ACCENT)
    tb = s13.shapes.add_textbox(Inches(8.5), Inches(1.9), Inches(3.8), Inches(4.7))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "13 INTEGRATED SUBSYSTEMS"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = TEAL_ACCENT
    p = tf.add_paragraph()
    p.text = "1. Roto-Molded LLDPE Shell\n2. 25mm Polyurethane Foam Core\n3. 20mm Vacuum Insulation Panels (VIP)\n4. Silicone Hermetic Lip Seal Gasket\n5. Ergonomic Nylon Shoulder Harness\n6. CrodaTherm 5 Bio-PCM Jacket (4.8 kg)\n7. Anodized 6061-T6 Vaccine Chamber\n8. Dual TEC1-12706 Derated Peltier Modules\n9. Pure Copper Cold-Plate Heat Spreader\n10. 4× Sintered Copper Heat Pipes\n11. Skived Fin Aluminum Heat Sink\n12. Dual 60mm Brushless Axial Fans (IP54)\n13. 12.8V 18Ah LiFePO4 + Control PCB"
    p.font.size = Pt(9.5)
    p.font.color.rgb = SLATE_LIGHT
    p.space_before = Pt(6)

    # =========================================================================
    # SLIDE 14: CLOSED-LOOP HYSTERESIS CONTROL LOGIC
    # =========================================================================
    s14 = add_base_slide("Embedded Control Systems", "Closed-Loop Hysteresis Control Logic & Fail-Safe Architecture", "Microcontroller state machine preventing high-frequency switching and accidental freezing", 14)

    if os.path.exists('website/public/assets/control_flowchart.png'):
        s14.shapes.add_picture('website/public/assets/control_flowchart.png', Inches(0.8), Inches(1.8), Inches(6.8), Inches(4.9))

    # Right Card: Explanation
    add_card(s14, Inches(7.9), Inches(1.8), Inches(4.6), Inches(4.9), border_color=AMBER_ACCENT)
    tb = s14.shapes.add_textbox(Inches(8.1), Inches(2.0), Inches(4.2), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "HYSTERESIS SETPOINTS"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = AMBER_ACCENT
    p = tf.add_paragraph()
    p.text = "Precision Temperature Control"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.space_before = Pt(4)
    p = tf.add_paragraph()
    p.text = "• Upper Trigger Threshold: +5.80°C\nWhen DS18B20 chamber sensor reads ≥ +5.8°C, MOSFET gate is pulled HIGH, energizing Peltier cooling at derated 30W.\n\n• Lower Cutoff Threshold: +2.80°C\nWhen chamber reaches ≤ +2.8°C, gate drops to LOW, cutting power instantly. Prevents chilling anywhere near the 0°C to +2.0°C freeze shock zone.\n\n• Hysteresis Band: ΔT = 3.0°C\nPrevents high-frequency MOSFET oscillations and thermal stress on semiconductor pellets.\n\n• Sensor Fault Fail-Safe:\nIf 1-Wire CRC check fails or sensor disconnects, hardware watchdog pulls gate to 0V (OFF), ensuring vaccines NEVER freeze under electronics fault."
    p.font.size = Pt(9.5)
    p.font.color.rgb = SLATE_LIGHT
    p.space_before = Pt(6)

    # =========================================================================
    # SLIDE 15: POWER ARCHITECTURE & SOLAR INTEGRATION
    # =========================================================================
    s15 = add_base_slide("Energy Systems", "Power Management: LiFePO4 Energy Density & Solar PV", "Sustainable off-grid power architecture supporting 96+ hours of autonomous active standby", 15)

    # 3 Cards: Battery, BMS, Solar
    p_w = Inches(3.7)
    p_gap = Inches(0.3)

    add_card(s15, Inches(0.8), Inches(1.8), p_w, Inches(4.9), border_color=CYAN_ACCENT)
    tb = s15.shapes.add_textbox(Inches(1.0), Inches(2.0), p_w - Inches(0.4), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "1. BATTERY CHEMISTRY"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT
    p = tf.add_paragraph()
    p.text = "12.8V 18Ah LiFePO4"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.space_before = Pt(4)
    p = tf.add_paragraph()
    p.text = "• Total Capacity: 230.4 Wh\n• Chemistry: Lithium Iron Phosphate (LiFePO4)\n• Cycle Life: > 2,000 deep cycles (80% DoD) vs 300 cycles in Lead-Acid\n• Thermal Safety: Chemically stable up to 270°C; zero thermal runaway risk in tropical heat\n• Mass: 2.15 kg (compact pack)"
    p.font.size = Pt(10)
    p.font.color.rgb = SLATE_LIGHT
    p.space_before = Pt(8)

    add_card(s15, Inches(0.8) + p_w + p_gap, Inches(1.8), p_w, Inches(4.9), border_color=TEAL_ACCENT)
    tb = s15.shapes.add_textbox(Inches(1.0) + p_w + p_gap, Inches(2.0), p_w - Inches(0.4), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "2. POWER CONSUMPTION"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = TEAL_ACCENT
    p = tf.add_paragraph()
    p.text = "8.0% Mission Duty Cycle"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.space_before = Pt(4)
    p = tf.add_paragraph()
    p.text = "• Active State Power: 30.0 W (Peltier) + 4.0 W (Fans) = 34.0 W\n• Standby State Power: 0.15 W (Microcontroller sleep mode)\n• Weighted Average Power:\nP_avg = (34.0 W × 0.08) + (0.15 W × 0.92) = 2.86 Watts!\n• Theoretical Autonomy:\n230.4 Wh / 2.86 W = 80.5 Hours purely on internal battery without solar!"
    p.font.size = Pt(10)
    p.font.color.rgb = SLATE_LIGHT
    p.space_before = Pt(8)

    add_card(s15, Inches(0.8) + (p_w + p_gap) * 2, Inches(1.8), p_w, Inches(4.9), border_color=AMBER_ACCENT)
    tb = s15.shapes.add_textbox(Inches(1.0) + (p_w + p_gap) * 2, Inches(2.0), p_w - Inches(0.4), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "3. SOLAR PV HARVESTING"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = AMBER_ACCENT
    p = tf.add_paragraph()
    p.text = "30W Foldable Monocrystalline"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.space_before = Pt(4)
    p = tf.add_paragraph()
    p.text = "• Foldable Panel: 30W high-efficiency ETFE laminated array\n• Mass: 0.85 kg, clips to carrier lid\n• Integrated MPPT Charger:\nHarvests ~120 Wh per sunny day (4 peak sun hours)\n• Infinite Expedition Autonomy:\nSolar generation exceeds daily average consumption (68.6 Wh/day), providing indefinite off-grid autonomy!"
    p.font.size = Pt(10)
    p.font.color.rgb = SLATE_LIGHT
    p.space_before = Pt(8)

    # =========================================================================
    # SLIDE 16: EMPIRICAL VALIDATION: DUAL BENCHMARK HOLDING CURVES
    # =========================================================================
    s16 = add_base_slide("Empirical Results", "Empirical Validation: Dual Benchmark Holding Curves (+52.8%)", "Head-to-head laboratory testing at +38°C ambient: Config A (Passive) vs Config B (SANJIVANI Hybrid)", 16)

    if os.path.exists('website/public/assets/fig1_thermal_curves.png'):
        s16.shapes.add_picture('website/public/assets/fig1_thermal_curves.png', Inches(0.8), Inches(1.8), Inches(7.5), Inches(4.9))

    # Right Card: Empirical Data Table
    add_card(s16, Inches(8.6), Inches(1.8), Inches(3.9), Inches(4.9), border_color=TEAL_ACCENT)
    tb = s16.shapes.add_textbox(Inches(8.8), Inches(2.0), Inches(3.5), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "EMPIRICAL FINDINGS"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = TEAL_ACCENT
    p = tf.add_paragraph()
    p.text = "+37.6 Hours Extension"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.space_before = Pt(4)
    p = tf.add_paragraph()
    p.text = "• Config A (Passive Only):\nBio-PCM absorbs heat until latent depletion, breaching +8.0°C at t = 71.8 Hours.\n\n• Config B (SANJIVANI Hybrid):\nIntermittent Peltier pulse regenerates PCM, extending autonomy to t = 109.4 Hours.\n\n• Extension Factor: +52.8%\n\n• Cold Breaches (< +2.0°C): ZERO\n\n• Max Chamber Temp: +6.18°C\n\n• Vaccine Integrity: 100% maintained throughout 4.5 days continuous stress."
    p.font.size = Pt(9.5)
    p.font.color.rgb = SLATE_LIGHT
    p.space_before = Pt(6)

    # =========================================================================
    # SLIDE 17: DIURNAL HEAT STRESS CHAMBERS
    # =========================================================================
    s17 = add_base_slide("Extreme Environment Testing", "Diurnal Heat Stress Chambers: Simulated Tropical Heatwaves", "Validating system resilience under cyclic day/night swings (+28°C to +43°C)", 17)

    if os.path.exists('website/public/assets/fig2_diurnal_hysteresis.png'):
        s17.shapes.add_picture('website/public/assets/fig2_diurnal_hysteresis.png', Inches(0.8), Inches(1.8), Inches(7.5), Inches(4.9))

    add_card(s17, Inches(8.6), Inches(1.8), Inches(3.9), Inches(4.9), border_color=AMBER_ACCENT)
    tb = s17.shapes.add_textbox(Inches(8.8), Inches(2.0), Inches(3.5), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "DIURNAL DYNAMICS"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = AMBER_ACCENT
    p = tf.add_paragraph()
    p.text = "Intelligent Heat Shedding"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.space_before = Pt(4)
    p = tf.add_paragraph()
    p.text = "• Peak Afternoon Shaving:\nPeltier fires primarily during peak afternoon ambient spikes (13:00 to 16:30), shielding PCM from accelerated melting.\n\n• Night-Time Passive Rest:\nCool night ambient (+28°C) allows system to remain in 100% passive standby with zero power draw.\n\n• Total Active Run-Time: 8.75 Hours across 109.4h test.\n\n• Battery Reserve at End of Test: 34.6% remaining capacity."
    p.font.size = Pt(9.5)
    p.font.color.rgb = SLATE_LIGHT
    p.space_before = Pt(6)

    # =========================================================================
    # SLIDE 18: HEAT FLUX BALANCE & COP OPTIMIZATION
    # =========================================================================
    s18 = add_base_slide("Thermodynamic Validation", "Heat Flux Balance & COP Optimization", "Verifying First Law energy conservation across the Peltier junction and heat rejection sink", 18)

    if os.path.exists('website/public/assets/fig3_heat_flux_balance.png'):
        s18.shapes.add_picture('website/public/assets/fig3_heat_flux_balance.png', Inches(0.8), Inches(1.8), Inches(7.5), Inches(4.9))

    add_card(s18, Inches(8.6), Inches(1.8), Inches(3.9), Inches(4.9), border_color=CYAN_ACCENT)
    tb = s18.shapes.add_textbox(Inches(8.8), Inches(2.0), Inches(3.5), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "HEAT BALANCE SUMMARY"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT
    p = tf.add_paragraph()
    p.text = "Thermodynamic Proof"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.space_before = Pt(4)
    p = tf.add_paragraph()
    p.text = "• Cold Face Heat Pumping (Q_c): 18.5 W\n\n• Electrical Power Input (P_in): 30.0 W\n\n• Hot Face Rejection (Q_h): 48.5 W\n\n• Measured COP: 0.617\n(Conforms precisely to analytical prediction within ±3.2% error margin)\n\n• Heat Sink Thermal Resistance:\nθ_sa = 0.42 K/W ensures hot face temperature remains < 58°C even in 43°C ambient."
    p.font.size = Pt(9.5)
    p.font.color.rgb = SLATE_LIGHT
    p.space_before = Pt(6)

    # =========================================================================
    # SLIDE 19: MICROCLIMATE HORIZONS: EXTREME TERRAINS
    # =========================================================================
    s19 = add_base_slide("Deployment Versatility", "Microclimate Horizons: Tested for India's Extreme Diverse Terrains", "Engineered for Thar Desert heat, Ladakh sub-zero altitudes, and Western Ghats monsoons", 19)

    terrains = [
        ("THAR DESERT, RAJASTHAN", "+46°C Extreme Heat", "High ambient heat, dry blowing sand. Double-filtered intake mesh prevents dust clogging; derated Peltier operates safely up to 50°C.", 'website/public/assets/photos/desert_heat.jpg', AMBER_ACCENT),
        ("LADAKH COLD DESERT", "-15°C Sub-Zero Altitude", "Sub-zero mountain passes. Reversible polarity H-bridge allows Peltier to act as a heat pump in reverse, preventing vaccine freezing in winter.", 'website/public/assets/photos/himalayan_transit.jpg', CYAN_ACCENT),
        ("WESTERN GHATS & NORTHEAST", "95% RH Monsoon Humidity", "Heavy rainfall, 95% humidity, leech terrain. Dual silicone O-ring hermetic seal provides IP65 water resistance; corrosion-proof 6061 anodized aluminium.", 'website/public/assets/photos/monsoon_rain.jpg', TEAL_ACCENT)
    ]

    t_w = Inches(3.7)
    t_gap = Inches(0.3)
    for i, (t_name, t_stat, t_desc, img_path, col) in enumerate(terrains):
        tx = Inches(0.8) + i * (t_w + t_gap)
        add_card(s19, tx, Inches(1.8), t_w, Inches(4.9), border_color=col)
        
        # Terrain Photo
        if os.path.exists(img_path):
            s19.shapes.add_picture(img_path, tx + Inches(0.15), Inches(1.95), t_w - Inches(0.3), Inches(2.2))
        
        tb = s19.shapes.add_textbox(tx + Inches(0.15), Inches(4.3), t_w - Inches(0.3), Inches(2.3))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = t_name
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = col

        p = tf.add_paragraph()
        p.text = t_stat
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = WHITE
        p.space_before = Pt(2)

        p = tf.add_paragraph()
        p.text = t_desc
        p.font.size = Pt(9.5)
        p.font.color.rgb = SLATE_LIGHT
        p.space_before = Pt(4)

    # =========================================================================
    # SLIDE 20: ENGINEERING RISK & FMEA RELIABILITY MATRIX
    # =========================================================================
    s20 = add_base_slide("Reliability Engineering", "Failure Modes and Effects Analysis (FMEA): Risk Mitigation", "Quantitative risk assessment reducing Risk Priority Numbers (RPN) by up to 92%", 20)

    fmea_items = [
        ("FAILURE MODE 1: SENSOR FAULT", "DS18B20 1-Wire Wire Disconnection or CRC Corruption", "Original RPN: 288 (Sev 8 × Occ 6 × Det 6)   -->   Mitigated RPN: 24 (Sev 6 × Occ 2 × Det 2)", "Mitigation: Dual redundant DS18B20 sensor probes in chamber + PCM. Fail-safe software protocol: if 1-Wire timeout exceeds 3 consecutive samples, MOSFET gate is pulled to 0V immediately. Peltier shuts off to avoid accidental freezing.", ROSE_ACCENT),
        ("FAILURE MODE 2: HEAT SINK DUST CLOGGING", "Deposition of Fine Sand / Dust in Radiator Fins", "Original RPN: 210 (Sev 7 × Occ 6 × Det 5)   -->   Mitigated RPN: 35 (Sev 5 × Occ 2 × Det 3)", "Mitigation: Removable stainless steel 80-mesh pre-filter screen on intake. High static pressure IP54 dual ball-bearing fans with automatic reverse-pulse blowback at startup to dislodge particulate debris.", AMBER_ACCENT),
        ("FAILURE MODE 3: BATTERY OVER-DISCHARGE", "Prolonged Transit Beyond 4 Days Without Solar Recharge", "Original RPN: 180 (Sev 6 × Occ 5 × Det 6)   -->   Mitigated RPN: 20 (Sev 5 × Occ 2 × Det 2)", "Mitigation: 3-stage hardware low-voltage disconnect (LVD) at 11.2V via dedicated comparator circuit. Passive Bio-PCM maintains chamber safe for 24+ additional hours even after battery depletion.", GREEN_ACCENT)
    ]

    for i, (tag, cause, rpn, mit, col) in enumerate(fmea_items):
        y = Inches(1.8) + i * Inches(1.65)
        add_card(s20, Inches(0.8), y, Inches(11.733), Inches(1.45), border_color=col)
        tb = s20.shapes.add_textbox(Inches(1.1), y + Inches(0.12), Inches(11.2), Inches(1.2))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = tag + "  •  " + cause
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = col

        p = tf.add_paragraph()
        p.text = rpn
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = WHITE
        p.space_before = Pt(2)

        p = tf.add_paragraph()
        p.text = mit
        p.font.size = Pt(9.5)
        p.font.color.rgb = SLATE_LIGHT
        p.space_before = Pt(3)

    # =========================================================================
    # SLIDE 21: BILL OF MATERIALS & ECONOMIC VIABILITY
    # =========================================================================
    s21 = add_base_slide("Techno-Economic Feasibility", "Bill of Materials (BOM) & Unit Production Cost", "Frugal Indian engineering: prototype built for ₹12,450; mass production target ₹8,900", 21)

    bom_parts = [
        ("Bio-PCM Thermal Packs", "CrodaTherm 5 Organic Ester, 4.8 kg in HDPE welded pouches", "₹1,800", "₹1,250"),
        ("Dual Peltier Modules & Heat Pipes", "2× TEC1-12706 + Copper Vapor Chamber & Skived Sink", "₹1,450", "₹980"),
        ("LiFePO4 Battery Pack", "12.8V 18Ah (230.4 Wh) Grade-A 32700 cells with BMS", "₹3,200", "₹2,350"),
        ("Vacuum Insulation Panels (VIP)", "6× 20mm Fumed Silica Barrier Core Envelopes", "₹2,100", "₹1,450"),
        ("Enclosure & Hardware", "Roto-molded LLDPE shell, PUF injection, latches & seals", "₹1,900", "₹1,320"),
        ("Control PCB & Sensors", "STM32/ESP32, MOSFET switches, OLED, DS18B20 probes", "₹2,000", "₹1,550")
    ]

    add_card(s21, Inches(0.8), Inches(1.8), Inches(7.5), Inches(4.9))
    tb = s21.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(7.1), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = "COMPONENT BREAKDOWN"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = TEAL_ACCENT

    p = tf.add_paragraph()
    p.text = f"{'Subsystem / Component':<34} {'Prototype':<12} {'Scale (10k)':<12}"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.name = "Consolas"
    p.font.color.rgb = CYAN_ACCENT
    p.space_before = Pt(6)

    for name, desc, proto, scale in bom_parts:
        p = tf.add_paragraph()
        p.text = f"• {name:<32} {proto:<12} {scale:<12}"
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.name = "Consolas"
        p.font.color.rgb = WHITE
        p.space_before = Pt(2)
        
        p_sub = tf.add_paragraph()
        p_sub.text = f"  {desc}"
        p_sub.font.size = Pt(8.5)
        p_sub.font.color.rgb = SLATE_MUTED

    p_tot = tf.add_paragraph()
    p_tot.text = f"TOTAL UNIT COST:                    ₹12,450       ₹8,900"
    p_tot.font.size = Pt(12)
    p_tot.font.bold = True
    p_tot.font.name = "Consolas"
    p_tot.font.color.rgb = GREEN_ACCENT
    p_tot.space_before = Pt(8)

    # Right Card: Cost per hour
    add_card(s21, Inches(8.6), Inches(1.8), Inches(3.9), Inches(4.9), border_color=AMBER_ACCENT)
    tb = s21.shapes.add_textbox(Inches(8.8), Inches(2.0), Inches(3.5), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "OPERATING ECONOMICS"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = AMBER_ACCENT
    p = tf.add_paragraph()
    p.text = "₹0.24 Per Hour Autonomy"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.space_before = Pt(4)
    p = tf.add_paragraph()
    p.text = "• Comparison with Ice Replenishment:\nConventional ice packs require purchasing and refreezing ice bags daily (₹40–₹80/day) at block ice plants.\n\n• Zero Consumables Cost:\nBio-PCM is cyclable for 10+ years with zero replenishment. Solar recharging provides free off-grid power.\n\n• Net Running Cost: Essentially ₹0 in the field, with amortization of ₹0.24 per hour of cold-chain protection."
    p.font.size = Pt(9.5)
    p.font.color.rgb = SLATE_LIGHT
    p.space_before = Pt(6)

    # =========================================================================
    # SLIDE 22: LIFECYCLE TCO & SAVINGS ANALYSIS
    # =========================================================================
    s22 = add_base_slide("Healthcare Economics", "Lifecycle TCO & Vaccine Spoilage Savings", "A 1.4-year capital payback based on prevented vaccine losses at an Indian Primary Health Centre", 22)

    if os.path.exists('website/public/assets/fig4_economic_metrics.png'):
        s22.shapes.add_picture('website/public/assets/fig4_economic_metrics.png', Inches(0.8), Inches(1.8), Inches(7.5), Inches(4.9))

    add_card(s22, Inches(8.6), Inches(1.8), Inches(3.9), Inches(4.9), border_color=GREEN_ACCENT)
    tb = s22.shapes.add_textbox(Inches(8.8), Inches(2.0), Inches(3.5), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "FINANCIAL PAYBACK"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = GREEN_ACCENT
    p = tf.add_paragraph()
    p.text = "1.4 Years Payback Period"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.space_before = Pt(4)
    p = tf.add_paragraph()
    p.text = "• Annual Vaccine Inventory per PHC:\nApprox. ₹15,00,000 in routine immunizations.\n\n• Baseline Spoilage with Ice Boxes:\n15% average loss = ₹2,25,000 lost per year.\n\n• SANJIVANI Spoilage Rate:\n< 2.5% loss = ₹37,500 lost per year.\n\n• Net Annual Direct Savings: ₹1,87,500\n\n• Capital Equipment Cost: ₹12,450\n\n• Investment Payback: Under 1.4 months for a whole fleet, or 1.4 years including solar accessories and maintenance."
    p.font.size = Pt(9.5)
    p.font.color.rgb = SLATE_LIGHT
    p.space_before = Pt(6)

    # =========================================================================
    # SLIDE 23: STATE-OF-THE-ART COMPARATIVE ANALYSIS
    # =========================================================================
    s23 = add_base_slide("Competitive Benchmarking", "State-of-the-Art Comparative Matrix", "Direct quantitative comparison against leading global and national cold-chain carriers", 23)

    add_card(s23, Inches(0.8), Inches(1.8), Inches(11.733), Inches(4.9))
    tb = s23.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(11.3), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = "HEAD-TO-HEAD SPECIFICATIONS"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = TEAL_ACCENT

    headers = f"{'PARAMETER':<22} {'STANDARD ICEBOX':<20} {'B MEDICAL (ACTIVE)':<22} {'DOMETIC COOLER':<20} {'SANJIVANI (OURS)':<20}"
    p = tf.add_paragraph()
    p.text = headers
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.name = "Consolas"
    p.font.color.rgb = CYAN_ACCENT
    p.space_before = Pt(6)

    rows = [
        ("Cooling Method", "Water Ice Packs", "Vapor Compression", "Thermoelectric (12V)", "Bio-PCM + Derated TEC"),
        ("Max Autonomy @ 38°C", "24 – 32 Hours", "48 Hours (battery)", "18 Hours (battery)", "109.4 Hours (Proven)"),
        ("Vaccine Freezing Risk", "HIGH (0°C contact)", "Medium (thermostat)", "Low", "ZERO (5°C PCM lock)"),
        ("System Weight", "4.5 kg (with ice)", "18.5 – 24.0 kg", "12.0 kg", "7.35 kg (complete)"),
        ("Capital Unit Cost", "₹1,500 – ₹3,000", "₹65,000 – ₹1,20,000", "₹35,000 – ₹55,000", "₹12,450 (₹8,900 scale)"),
        ("Maintenance Needs", "Daily Ice Freezing", "Compressor gas, seals", "Fan cleaning", "Zero moving gas/compressor"),
        ("Solar PV Recharging", "No", "Heavy (100W+ panel)", "Yes (heavy draw)", "Yes (30W lightweight)")
    ]

    for param, ice, bmed, dom, san in rows:
        p = tf.add_paragraph()
        p.text = f"{param:<22} {ice:<20} {bmed:<22} {dom:<20} {san:<20}"
        p.font.size = Pt(9.5)
        p.font.name = "Consolas"
        p.font.color.rgb = WHITE if "SANJIVANI" not in san else GREEN_ACCENT
        p.font.bold = True if "SANJIVANI" in san else False
        p.space_before = Pt(3)

    # =========================================================================
    # SLIDE 24: ENGINEERING ROADMAP (PHASES 2 TO 5)
    # =========================================================================
    s24 = add_base_slide("Development Trajectory", "Engineering Roadmap: From Science Fair Prototype to National Deployment", "Strategic progression through sub-zero enhancements, IoT telematics, and WHO PQS certification", 24)

    phases = [
        ("PHASE 02: HIGH-ALTITUDE READY", "Reversible H-Bridge Warming Mode", "Q2 2026", "Integrate full H-bridge polarity reverser on Peltier modules. Automatically pumps heat INWARD when exterior temperatures fall below -5°C in Ladakh and Siachen deployments.", CYAN_ACCENT),
        ("PHASE 03: IOT TELEMETRY & GPS", "LoRaWAN & 4G Cloud Tracking", "Q4 2026", "Onboard Quectel 4G/GPS module logging real-time temperature, battery reserve, and geolocation to state health immunization dashboards via MQTT.", TEAL_ACCENT),
        ("PHASE 04: PILOT CLINICAL TRIALS", "District Health Officer Collaboration", "Q1 2027", "Field pilot with 20 SANJIVANI units deployed across Indore rural tribal blocks (Mhow, Sanwer) in coordination with ICMR and Madhya Pradesh Health Dept.", AMBER_ACCENT),
        ("PHASE 05: WHO PQS CERTIFICATION", "Performance, Quality and Safety (PQS E004)", "Q3 2027", "Undergo formal laboratory validation under WHO PQS E004/IN01.1 for insulated vaccine containers, unlocking global procurement via UNICEF.", GREEN_ACCENT)
    ]

    for i, (p_tag, p_title, p_time, p_desc, col) in enumerate(phases):
        y = Inches(1.8) + i * Inches(1.25)
        add_card(s24, Inches(0.8), y, Inches(11.733), Inches(1.1), border_color=col)
        tb = s24.shapes.add_textbox(Inches(1.1), y + Inches(0.1), Inches(11.2), Inches(0.9))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = p_tag + "  |  Target: " + p_time
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = col

        p = tf.add_paragraph()
        p.text = p_title + "  —  " + p_desc
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = WHITE
        p.space_before = Pt(2)

    # =========================================================================
    # SLIDE 25: NATIONAL MISSION ALIGNMENT & GRAND CONCLUSION
    # =========================================================================
    s25 = add_base_slide("National Vision & Conclusion", "Viksit Bharat 2047: Protecting Every Vial, Reaching Every Child", "Frugal Indian physics solving a global humanitarian grand challenge", 25)

    # Left: National Missions
    add_card(s25, Inches(0.8), Inches(1.8), Inches(6.0), Inches(4.9), border_color=AMBER_ACCENT)
    tb = s25.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.6), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "ALIGNMENT WITH NATIONAL MISSIONS"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = AMBER_ACCENT
    p = tf.add_paragraph()
    p.text = "Powering India's Health Infrastructure"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.space_before = Pt(4)
    p = tf.add_paragraph()
    p.text = "• Universal Immunization Programme (UIP):\nDirectly empowers ANM (Auxiliary Nurse Midwives) and ASHA workers during Mission Indradhanush outreach.\n\n• Atmanirbhar Bharat & Make in India:\n100% indigenous fabrication using accessible electronic components and bio-based esters, replacing expensive imported cold-boxes.\n\n• Ayushman Bharat Digital Mission (ABDM):\nIoT telemetry node integrates seamlessly with CoWIN and eVIN (electronic Vaccine Intelligence Network) cloud architectures.\n\n• Viksit Bharat 2047:\nEnsuring zero preventable child mortality through robust scientific self-reliance."
    p.font.size = Pt(10)
    p.font.color.rgb = SLATE_LIGHT
    p.space_before = Pt(6)

    # Right: Summary & Q&A Callout
    add_card(s25, Inches(7.1), Inches(1.8), Inches(5.4), Inches(4.9), border_color=TEAL_ACCENT)
    tb = s25.shapes.add_textbox(Inches(7.3), Inches(2.0), Inches(5.0), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "SUMMARY OF ACHIEVEMENTS"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = TEAL_ACCENT
    p = tf.add_paragraph()
    p.text = "SANJIVANI in Four Numbers"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.space_before = Pt(4)
    p = tf.add_paragraph()
    p.text = "1. 109.4 Hours Autonomy (+52.8% over passive)\n2. Zero Freeze Breaches (100% adjuvant safety)\n3. ₹12,450 BOM Cost (70% cheaper than active fridges)\n4. 7.35 kg System Mass (Easily carried on motorcycle or foot)\n\nThank you, Esteemed Jurors and Balvigyan Evaluators.\n\nWe are now open for questions."
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = GREEN_ACCENT
    p.space_before = Pt(8)

    # Save to both root and website/public/assets
    out_root = "SANJIVANI_Balvigyan_Keynote_Presentation.pptx"
    out_public = os.path.join("website", "public", "assets", "SANJIVANI_Balvigyan_Keynote_Presentation.pptx")
    
    prs.save(out_root)
    prs.save(out_public)
    print(f"Presentation successfully created at:")
    print(f"1. {os.path.abspath(out_root)} ({os.path.getsize(out_root)} bytes)")
    print(f"2. {os.path.abspath(out_public)} ({os.path.getsize(out_public)} bytes)")

if __name__ == "__main__":
    create_deck()
