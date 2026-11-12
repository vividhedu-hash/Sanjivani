import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Set figure size and DPI for high-resolution A3 print
fig, ax = plt.subplots(figsize=(11.0, 6.2), dpi=300)
ax.set_xlim(-1.2, 19.5)
ax.set_ylim(-0.8, 11.2)
ax.axis('off')

# Clean white background
fig.patch.set_facecolor('#FFFFFF')
ax.set_facecolor('#FFFFFF')

# -----------------------------------------------------------
# 0. TITLE & ENGINEERING HEADER
# -----------------------------------------------------------
ax.text(0.2, 10.7, "SECTION A-A: HYBRID THERMAL ARCHITECTURE & COMPONENT INTEGRATION", 
        fontsize=8.5, fontweight='bold', color='#0F172A', family='Arial')
ax.text(0.2, 10.35, "Cross-sectional engineering schematic of SANJIVANI enclosure, solid-state pumping and dissipation loop", 
        fontsize=6.5, color='#475569', family='Arial', style='italic')

# -----------------------------------------------------------
# 1. MAIN ENCLOSURE CUTAWAY (Cross-Section View)
# -----------------------------------------------------------
# Outer Shell (LLDPE Casing) - Deep Slate
outer_box = patches.FancyBboxPatch((0.5, 1.2), 9.0, 8.4, boxstyle="round,pad=0.2,rounding_size=0.35",
                                  facecolor='#1E293B', edgecolor='#0F172A', linewidth=1.8)
ax.add_patch(outer_box)

# PUF Shell Layer (Polyurethane Foam - Warm Cream)
puf_box = patches.Rectangle((0.8, 1.5), 8.4, 7.8, facecolor='#FEF3C7', edgecolor='#F59E0B', linewidth=1.0, linestyle='--')
ax.add_patch(puf_box)

# VIP Core Layer (Vacuum Insulation Panel - Silver-Grey)
vip_box = patches.Rectangle((1.3, 2.0), 7.4, 6.8, facecolor='#E2E8F0', edgecolor='#94A3B8', linewidth=1.0)
ax.add_patch(vip_box)

# Aluminium Isothermal Cold Jacket (6061-T6 Plate - Cool Steel)
al_jacket = patches.Rectangle((1.7, 2.4), 6.6, 6.0, facecolor='#CBD5E1', edgecolor='#0284C7', linewidth=1.5)
ax.add_patch(al_jacket)

# Bio-PCM Perimeter Cassettes (Ice Blue with crosshatch)
# Left PCM Cassette
pcm_left = patches.Rectangle((1.9, 2.6), 1.0, 5.6, facecolor='#BAE6FD', edgecolor='#0284C7', linewidth=1.0, hatch='//', alpha=0.9)
ax.add_patch(pcm_left)
# Right PCM Cassette
pcm_right = patches.Rectangle((7.1, 2.6), 1.0, 5.6, facecolor='#BAE6FD', edgecolor='#0284C7', linewidth=1.0, hatch='//', alpha=0.9)
ax.add_patch(pcm_right)
# Bottom PCM Cassette
pcm_bottom = patches.Rectangle((2.9, 2.6), 4.2, 0.8, facecolor='#BAE6FD', edgecolor='#0284C7', linewidth=1.0, hatch='//', alpha=0.9)
ax.add_patch(pcm_bottom)

# Medical Payload Chamber (ISO 6.5L, Clean Clinical Green)
payload_box = patches.Rectangle((3.0, 3.5), 4.0, 4.6, facecolor='#F0FDF4', edgecolor='#16A34A', linewidth=1.4)
ax.add_patch(payload_box)
ax.text(5.0, 7.8, "PAYLOAD CAVITY (ISO 6.5 L)", ha='center', va='center', fontsize=6.8, fontweight='bold', color='#166534')

# Vaccine Vials inside Payload (Draw 7 vials on tray)
vial_positions = [(3.4, 3.8), (4.2, 3.8), (5.0, 3.8), (5.8, 3.8),
                  (3.8, 5.5), (4.6, 5.5), (5.4, 5.5)]
for vx, vy in vial_positions:
    # Glass Vial Body
    v_body = patches.Rectangle((vx, vy), 0.6, 1.2, facecolor='#E0F2FE', edgecolor='#0284C7', linewidth=0.8)
    ax.add_patch(v_body)
    # Liquid vaccine inside
    v_liq = patches.Rectangle((vx+0.05, vy+0.05), 0.5, 0.75, facecolor='#0284C7', alpha=0.5)
    ax.add_patch(v_liq)
    # Stopper / Cap
    v_cap = patches.Rectangle((vx+0.1, vy+1.2), 0.4, 0.22, facecolor='#DC2626', edgecolor='#991B1B', linewidth=0.6)
    ax.add_patch(v_cap)

# Temperature Probes (DS18B20 1-Wire Digital Probes)
# Sensor 1: Core Payload
ax.plot([4.9, 4.9], [7.7, 4.9], color='#7C3AED', linewidth=1.8, linestyle='-')
ax.plot(4.9, 4.9, marker='s', markersize=6, color='#7C3AED', markeredgecolor='#4C1D95')
# Sensor 2: PCM Interface
ax.plot([7.6, 7.6], [7.7, 5.4], color='#7C3AED', linewidth=1.8, linestyle='-')
ax.plot(7.6, 5.4, marker='s', markersize=6, color='#7C3AED', markeredgecolor='#4C1D95')
# Sensor 3: Cold Plate Interface
ax.plot([10.4, 10.4], [7.7, 5.8], color='#7C3AED', linewidth=1.8, linestyle='-')
ax.plot(10.4, 5.8, marker='s', markersize=6, color='#7C3AED', markeredgecolor='#4C1D95')

# -----------------------------------------------------------
# 2. THERMOELECTRIC HEAT PUMP & DISSIPATION UNIT
# -----------------------------------------------------------
# Thermal Pass-Through Port (High Density PUF plug)
pass_port = patches.Rectangle((9.5, 4.2), 0.8, 2.8, facecolor='#94A3B8', edgecolor='#475569', linewidth=1.0)
ax.add_patch(pass_port)

# 8. Liquid Cold Plate / Chamber (Copper-Nickel Plated)
cu_cold = patches.Rectangle((10.3, 4.3), 0.5, 2.6, facecolor='#0EA5E9', edgecolor='#0369A1', linewidth=1.2)
ax.add_patch(cu_cold)

# 6. Cold-Side Thermal Interface Material (Arctic MX-4 TIM Layer)
tim_cold = patches.Rectangle((10.8, 4.4), 0.08, 2.4, facecolor='#64748B', edgecolor='#334155', linewidth=0.5)
ax.add_patch(tim_cold)

# 5. Dual Thermoelectric Peltier Modules (TEC1-12706)
tec1 = patches.Rectangle((10.9, 5.7), 0.35, 1.0, facecolor='#0D9488', edgecolor='#042F2E', linewidth=1.2)
ax.add_patch(tec1)
ax.text(11.07, 6.2, "TEC 1", ha='center', va='center', color='#FFFFFF', fontsize=5.5, fontweight='bold', rotation=-90)

tec2 = patches.Rectangle((10.9, 4.5), 0.35, 1.0, facecolor='#0D9488', edgecolor='#042F2E', linewidth=1.2)
ax.add_patch(tec2)
ax.text(11.07, 5.0, "TEC 2", ha='center', va='center', color='#FFFFFF', fontsize=5.5, fontweight='bold', rotation=-90)

# 9. Peltier Hot Side Copper Thermal Base
hot_base = patches.Rectangle((11.27, 4.2), 0.45, 2.8, facecolor='#B45309', edgecolor='#78350F', linewidth=1.2)
ax.add_patch(hot_base)

# Sintered Copper Heat Pipes (4x Heat Pipes)
ax.plot([11.72, 12.3, 12.7], [6.3, 6.7, 6.7], color='#D97706', linewidth=3.5)
ax.plot([11.72, 12.3, 12.7], [4.9, 4.5, 4.5], color='#D97706', linewidth=3.5)

# 10. Skived Extruded Aluminium Fin Stack
for fy in np.arange(3.4, 7.8, 0.20):
    fin = patches.Rectangle((12.7, fy), 2.2, 0.10, facecolor='#64748B', edgecolor='#334155', linewidth=0.5)
    ax.add_patch(fin)

# 11. Dual 80mm Forced Convection Cooling Fans
fan1 = patches.Rectangle((15.0, 5.7), 0.8, 1.9, facecolor='#1E293B', edgecolor='#0F172A', linewidth=1.2)
ax.add_patch(fan1)
fan2 = patches.Rectangle((15.0, 3.6), 0.8, 1.9, facecolor='#1E293B', edgecolor='#0F172A', linewidth=1.2)
ax.add_patch(fan2)
ax.text(15.4, 6.65, 'FAN 1 (PWM)', ha='center', va='center', color='#FFFFFF', fontsize=5.5, fontweight='bold', rotation=-90)
ax.text(15.4, 4.55, 'FAN 2 (PWM)', ha='center', va='center', color='#FFFFFF', fontsize=5.5, fontweight='bold', rotation=-90)

# -----------------------------------------------------------
# 3. PUMP REPOSITIONED (NO OVERLAP WITH LEGEND)
# -----------------------------------------------------------
# Micro DC Diaphragm Pump positioned cleanly at x = 5.2 to 7.0
pump_box = patches.FancyBboxPatch((5.4, 0.2), 1.8, 0.8, boxstyle="round,pad=0.1,rounding_size=0.15",
                                facecolor='#4338CA', edgecolor='#312E81', linewidth=1.1)
ax.add_patch(pump_box)
ax.text(6.3, 0.6, 'MICRO PUMP\n(12V, 2.4W)', ha='center', va='center', color='#FFFFFF', fontsize=5.8, fontweight='bold')

# Silicone Tubing Routing (Teal Liquid Transport Loop)
ax.plot([7.2, 10.5, 10.5], [0.6, 0.6, 4.3], color='#06B6D4', linewidth=2.2, linestyle='-')
ax.plot([10.5, 10.5, 8.3, 8.3], [6.9, 8.7, 8.7, 8.2], color='#06B6D4', linewidth=2.2, linestyle='-')
ax.plot([1.7, 1.7, 5.4], [4.5, 0.6, 0.6], color='#06B6D4', linewidth=2.2, linestyle='-')

# -----------------------------------------------------------
# 4. CONTROL ELECTRONICS & POWER SOURCE
# -----------------------------------------------------------
# 12. ESP32 Controller Module & Power MOSFETs
ctrl_box = patches.FancyBboxPatch((11.0, 8.3), 3.4, 1.8, boxstyle="round,pad=0.12,rounding_size=0.2",
                                facecolor='#0F172A', edgecolor='#38BDF8', linewidth=1.4)
ax.add_patch(ctrl_box)
ax.text(12.7, 9.4, 'ESP32 CONTROLLER &\nMOSFET SWITCHING', ha='center', va='center', color='#38BDF8', fontsize=6.8, fontweight='bold')
# OLED Display Screen
oled = patches.Rectangle((11.4, 8.5), 1.2, 0.55, facecolor='#000000', edgecolor='#22C55E', linewidth=0.8)
ax.add_patch(oled)
ax.text(12.0, 8.78, '4.8°C | 12.8V', ha='center', va='center', color='#22C55E', fontsize=5.2, fontfamily='monospace')

# 13. 12.8V 30Ah LiFePO4 Battery Pack
bat_box = patches.FancyBboxPatch((11.0, 0.2), 4.8, 2.4, boxstyle="round,pad=0.15,rounding_size=0.25",
                               facecolor='#334155', edgecolor='#64748B', linewidth=1.4)
ax.add_patch(bat_box)
ax.text(13.4, 1.6, '12.8V 30Ah LiFePO4 BATTERY PACK\n(384 Wh Gross Storage · 3.4 kg)', 
        ha='center', va='center', color='#FFFFFF', fontsize=7.0, fontweight='bold')
ax.text(13.4, 0.7, 'Integrated BMS · Over-discharge, Thermal & Short-Circuit Cutoff', 
        ha='center', va='center', color='#CBD5E1', fontsize=5.5, style='italic')

# -----------------------------------------------------------
# 5. HEAT FLOW FLUX & ELECTRICAL WIRING ARROWS
# -----------------------------------------------------------
# Ambient Heat Ingress (Red Arrows through Outer Wall)
for wy in [3.2, 5.2, 7.2]:
    ax.annotate('', xy=(0.8, wy), xytext=(-0.5, wy),
                arrowprops=dict(facecolor='#DC2626', edgecolor='#991B1B', width=2.2, headwidth=6, headlength=6))
ax.text(-0.6, 5.2, 'Ambient Heat Ingress\nQ̇_in = 4.4 W (at 35°C)', ha='right', va='center', color='#DC2626', fontsize=6.5, fontweight='bold')

# Cold Heat Extraction Arrow (Blue Arrow into Cold Plate)
ax.annotate('', xy=(10.3, 5.6), xytext=(8.8, 5.6),
            arrowprops=dict(facecolor='#0284C7', edgecolor='#0369A1', width=3.0, headwidth=8, headlength=8))
ax.text(9.5, 6.1, 'Cold Extraction\nQ̇_c = 18.5 W', ha='center', va='bottom', color='#0284C7', fontsize=6.8, fontweight='bold')

# Hot Heat Rejection Arrows (Orange Arrows leaving Fin Stack)
for ay in [4.3, 5.6, 6.9]:
    ax.annotate('', xy=(17.4, ay), xytext=(15.9, ay),
                arrowprops=dict(facecolor='#EA580C', edgecolor='#C2410C', width=3.2, headwidth=8, headlength=8))
ax.text(17.6, 5.6, 'Forced Heat Rejection\nQ̇_h = Q̇_c + P_elec = 48.5 W\nto Ambient Air', 
        ha='left', va='center', color='#EA580C', fontsize=7.0, fontweight='bold')

# Electrical lines (Grey dashed lines from Controller to TEC and Fans)
ax.plot([12.7, 11.2, 11.2], [8.3, 7.4, 6.7], color='#94A3B8', linewidth=1.5, linestyle=':')
ax.plot([12.7, 15.4], [8.3, 7.6], color='#94A3B8', linewidth=1.5, linestyle=':')
ax.plot([13.4, 13.4], [2.6, 8.3], color='#64748B', linewidth=1.5, linestyle='--') # Battery to Controller

# -----------------------------------------------------------
# 6. EXACT 13 NUMBERED CALLOUT BADGES (Matching User Master Prompt)
# -----------------------------------------------------------
callouts = [
    (1, (0.5, 9.0), (-0.2, 9.8), "1. Insulated outer enclosure (LLDPE + VIP + PUF)"),
    (2, (2.2, 3.2), (0.8, 2.0), "2. PCM chamber (4.8 kg CrodaTherm 5 Cassettes)"),
    (3, (3.5, 5.5), (3.6, 9.6), "3. Medical payload compartment (ISO 6.5 L, 24 vials)"),
    (4, (4.9, 4.9), (4.9, 8.9), "4. Temperature sensors (DS18B20 1-Wire, ±0.1°C)"),
    (5, (10.9, 6.2), (10.2, 7.6), "5. Thermoelectric Peltier module (Dual TEC1-12706)"),
    (6, (10.85, 4.8), (9.8, 3.8), "6. Cold-side thermal interface (Arctic MX-4 TIM)"),
    (7, (6.8, 8.0), (6.8, 9.6), "7. Aluminium heat-spreading plates (6061-T6 Jacket)"),
    (8, (10.3, 6.5), (9.4, 8.4), "8. Liquid-based thermal-transfer loop & cold plate"),
    (9, (11.5, 4.4), (11.5, 3.5), "9. Peltier hot side (Copper heat-spreading base)"),
    (10, (13.5, 7.4), (13.5, 8.0), "10. External heat sink (Skived Cu/Al fin stack)"),
    (11, (15.2, 7.3), (16.2, 8.5), "11. Fans & pump (Dual 80mm fans & 12V pump)"),
    (12, (12.7, 9.2), (12.7, 10.3), "12. Control electronics (ESP32 & MOSFET driver)"),
    (13, (13.4, 2.0), (16.5, 2.0), "13. Power source (12.8V 30Ah LiFePO4 battery pack)")
]

for num, target, pos, text in callouts:
    ax.annotate(str(num), xy=target, xytext=pos,
                arrowprops=dict(arrowstyle="->", color='#0F172A', lw=1.1),
                bbox=dict(boxstyle="circle,pad=0.22", facecolor='#0284C7', edgecolor='#0369A1', lw=1.1),
                color='#FFFFFF', fontsize=7.2, fontweight='bold', ha='center', va='center', zorder=10)

# -----------------------------------------------------------
# 7. COLOR-CODED PATHWAYS LEGEND (Bottom Left: Compact x = 0.2 to 4.2)
# -----------------------------------------------------------
leg_box = patches.FancyBboxPatch((0.2, 0.1), 4.2, 1.4, boxstyle="round,pad=0.1,rounding_size=0.15",
                               facecolor='#F8FAFC', edgecolor='#CBD5E1', linewidth=1.0)
ax.add_patch(leg_box)
ax.text(0.35, 1.30, 'PATHWAYS LEGEND:', color='#0F172A', fontsize=6.2, fontweight='bold')

# Blue: Cold extraction
ax.plot([0.35, 0.80], [1.05, 1.05], color='#0284C7', linewidth=3.0)
ax.text(0.95, 1.05, 'Blue: Cold-side extraction', va='center', color='#334155', fontsize=5.8)

# Orange: Hot rejection
ax.plot([0.35, 0.80], [0.75, 0.75], color='#EA580C', linewidth=3.0)
ax.text(0.95, 0.75, 'Orange: Hot-side rejection', va='center', color='#334155', fontsize=5.8)

# Teal: Liquid heat transport
ax.plot([0.35, 0.80], [0.45, 0.45], color='#06B6D4', linewidth=2.5)
ax.text(0.95, 0.45, 'Teal: Glycol liquid loop', va='center', color='#334155', fontsize=5.8)

# Grey: Electrical & control
ax.plot([0.35, 0.80], [0.18, 0.18], color='#64748B', linewidth=2.0, linestyle='--')
ax.text(0.95, 0.18, 'Grey: Sensor & power lines', va='center', color='#334155', fontsize=5.8)

plt.tight_layout()
plt.savefig('poster_assets/cutaway_architecture.png', bbox_inches='tight', pad_inches=0.06)
plt.close()
print("Cutaway Architecture Diagram successfully updated at poster_assets/cutaway_architecture.png")
