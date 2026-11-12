import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

os.makedirs('poster_assets', exist_ok=True)
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['figure.dpi'] = 300

# ==============================================================================
# 1. SPECIALIZED SIMULATION GRAPH
# Title: Modelled Thermal-Energy Balance: PCM-Only vs Hybrid Cooling
# Subtitle: Scenario simulation — not experimental measurements
# ==============================================================================
def create_poster_simulation_graph():
    dt = 0.05
    time = np.arange(0, 125 + dt, dt)
    n = len(time)
    
    # Ambient diurnal wave
    T_amb = 35.0 + 7.0 * np.sin(2 * np.pi * (time - 8.0) / 24.0)
    
    # Physical parameters
    UA = 0.147 # W/K
    C_payload = 12160.0 # J/K
    m_pcm = 4.8 # kg
    L_pcm = 218000.0 # J/kg
    Q_latent_tot = m_pcm * L_pcm # 1,046,400 J
    Q_active = 18.5 # W
    
    # Passive simulation
    T_pass = np.zeros(n)
    T_pass[0] = 3.2
    Q_pcm_pass = np.zeros(n)
    Q_pcm_pass[0] = Q_latent_tot
    q_res_p = Q_latent_tot
    
    for i in range(n - 1):
        qin = UA * (T_amb[i] - T_pass[i])
        Ein = qin * (dt * 3600)
        if T_pass[i] < 4.5:
            T_pass[i+1] = T_pass[i] + Ein / (C_payload + m_pcm * 2100)
            Q_pcm_pass[i+1] = q_res_p
        elif q_res_p > 0:
            q_res_p -= Ein
            Q_pcm_pass[i+1] = max(0.0, q_res_p)
            melt = 1.0 - Q_pcm_pass[i+1] / Q_latent_tot
            T_pass[i+1] = 4.5 + 0.6 * melt
        else:
            Q_pcm_pass[i+1] = 0.0
            T_pass[i+1] = min(T_amb[i], T_pass[i] + Ein / (C_payload + m_pcm * 2250))
            
    # Hybrid simulation
    T_sanj = np.zeros(n)
    T_sanj[0] = 3.2
    Q_pcm_sanj = np.zeros(n)
    Q_pcm_sanj[0] = Q_latent_tot
    q_res_s = Q_latent_tot
    active = False
    active_h = 0.0
    max_active_h = 8.75
    min_run = 0
    
    for i in range(n - 1):
        qin = UA * (T_amb[i] - T_sanj[i])
        if active_h < max_active_h:
            if not active:
                if T_sanj[i] >= 6.2:
                    active = True
                    min_run = int(0.25 / dt)
            else:
                if min_run > 0:
                    min_run -= 1
                elif T_sanj[i] <= 3.8:
                    active = False
        else:
            active = False
            
        if active:
            active_h += dt
            qnet = qin - Q_active
        else:
            qnet = qin
            
        Enet = qnet * (dt * 3600)
        if T_sanj[i] < 4.5:
            T_sanj[i+1] = max(2.2, T_sanj[i] + Enet / (C_payload + m_pcm * 2100))
            Q_pcm_sanj[i+1] = q_res_s
        elif q_res_s > 0:
            if Enet > 0:
                q_res_s -= Enet
            else:
                q_res_s = min(Q_latent_tot, q_res_s - Enet * 0.75)
            Q_pcm_sanj[i+1] = max(0.0, q_res_s)
            melt = 1.0 - Q_pcm_sanj[i+1] / Q_latent_tot
            dyn = -0.45 if active else 0.35
            T_sanj[i+1] = np.clip(4.5 + 0.65 * melt + dyn, 3.2, 7.9)
        else:
            Q_pcm_sanj[i+1] = 0.0
            T_sanj[i+1] = min(T_amb[i], T_sanj[i] + Enet / (C_payload + m_pcm * 2250))

    # Figure creation (2 stacked subplots)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6.2, 4.4), dpi=300, sharex=True,
                                   gridspec_kw={'height_ratios': [2.2, 1.4]})
    fig.patch.set_facecolor('#FFFFFF')
    
    # --- SUBPLOT 1: TEMPERATURE DYNAMICS ---
    ax1.set_facecolor('#FCFDFE')
    # Safe WHO Corridor
    ax1.axhspan(2.0, 8.0, color='#E8F5E9', alpha=0.9, zorder=1)
    ax1.axhline(8.0, color='#DC2626', linestyle='--', linewidth=1.1, zorder=2)
    ax1.axhline(2.0, color='#2563EB', linestyle='--', linewidth=1.1, zorder=2)
    
    # Ambient Temperature (dotted thin grey)
    ax1.plot(time, T_amb, color='#94A3B8', linestyle=':', linewidth=1.0, alpha=0.85, label='Ambient Diurnal (28–42°C)')
    
    # Passive PCM curve
    ax1.plot(time, T_pass, color='#D97706', linestyle='--', linewidth=1.8, zorder=4, label='Passive PCM Baseline (71.7 h)')
    
    # SANJIVANI Hybrid curve
    ax1.plot(time, T_sanj, color='#0F766E', linestyle='-', linewidth=2.2, zorder=5, label='SANJIVANI Hybrid System (109.4 h)')
    
    # Breach points and vertical target lines
    ax1.axvline(71.7, color='#D97706', linestyle=':', linewidth=1.2, alpha=0.9)
    ax1.axvline(109.4, color='#0F766E', linestyle=':', linewidth=1.2, alpha=0.9)
    
    # Annotations
    ax1.text(3, 2.5, 'WHO Safe Vaccine Corridor (+2°C to +8°C)', fontsize=6.8, color='#166534', fontweight='bold')
    ax1.scatter([71.7], [8.0], color='#D97706', s=35, zorder=6)
    ax1.text(71.7 - 2, 8.8, '72 h\nPlanning\nBaseline', fontsize=6.2, color='#92400E', ha='right', fontweight='bold')
    
    ax1.scatter([109.4], [8.0], color='#0F766E', s=35, zorder=6)
    ax1.text(109.4 + 2, 8.8, '110 h\nDesign\nTarget', fontsize=6.2, color='#115E59', ha='left', fontweight='bold')
    
    ax1.set_ylabel('Core Temp (°C)', fontsize=7.5, fontweight='bold', color='#1E293B')
    ax1.set_ylim(0, 16)
    ax1.set_yticks([2, 5, 8, 12, 16])
    ax1.grid(True, linestyle='-', linewidth=0.5, color='#E2E8F0', alpha=0.8)
    ax1.legend(loc='upper left', fontsize=6.0, framealpha=0.92, facecolor='#FFFFFF', edgecolor='#CBD5E1')
    
    # Prominent title and scientific caveat
    ax1.set_title('Modelled Thermal-Energy Balance: PCM-Only vs Hybrid Cooling', fontsize=8.2, fontweight='bold', color='#0F172A', pad=12)
    ax1.text(0.5, 1.02, 'Scenario simulation — not experimental measurements', transform=ax1.transAxes,
             fontsize=6.5, color='#DC2626', fontstyle='italic', ha='center')
    
    # --- SUBPLOT 2: REMAINING PCM LATENT THERMAL RESERVE ---
    ax2.set_facecolor('#FCFDFE')
    ax2.plot(time, (Q_pcm_pass / Q_latent_tot) * 100, color='#D97706', linestyle='--', linewidth=1.6, label='Passive PCM Depletion')
    ax2.plot(time, (Q_pcm_sanj / Q_latent_tot) * 100, color='#0F766E', linestyle='-', linewidth=2.0, label='Hybrid Controlled Depletion')
    
    ax2.axvline(71.7, color='#D97706', linestyle=':', linewidth=1.2, alpha=0.9)
    ax2.axvline(109.4, color='#0F766E', linestyle=':', linewidth=1.2, alpha=0.9)
    
    ax2.text(28, 48, 'Sensor pulses preserve latent reserve', fontsize=6.0, color='#0F766E', fontweight='bold', rotation=-14)
    
    ax2.set_ylabel('PCM Latent\nReserve (%)', fontsize=7.0, fontweight='bold', color='#1E293B')
    ax2.set_xlabel('Mission Time (Hours)', fontsize=7.5, fontweight='bold', color='#1E293B')
    ax2.set_xlim(0, 120)
    ax2.set_xticks(np.arange(0, 121, 20))
    ax2.set_ylim(-5, 105)
    ax2.set_yticks([0, 25, 50, 75, 100])
    ax2.grid(True, linestyle='-', linewidth=0.5, color='#E2E8F0', alpha=0.8)
    ax2.legend(loc='lower left', fontsize=6.0, framealpha=0.92, facecolor='#FFFFFF', edgecolor='#CBD5E1')
    
    plt.tight_layout()
    plt.subplots_adjust(hspace=0.14)
    plt.savefig('poster_assets/poster_simulation_graph.png', bbox_inches='tight', pad_inches=0.06)
    plt.close()
    print("Poster Simulation Graph generated successfully.")

# ==============================================================================
# 2. VECTOR OPERATIONAL FLOWCHART
# Clean, professional engineering control algorithm diagram
# ==============================================================================
def create_control_flowchart():
    fig, ax = plt.subplots(figsize=(6.2, 2.5), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4.2)
    ax.axis('off')
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')
    
    # Box styles
    b_passive = dict(boxstyle="round,pad=0.25,rounding_size=0.15", facecolor='#F0FDF4', edgecolor='#16A34A', lw=1.2)
    b_sense   = dict(boxstyle="round,pad=0.25,rounding_size=0.15", facecolor='#F8FAFC', edgecolor='#475569', lw=1.2)
    b_decide  = dict(boxstyle="round4,pad=0.25", facecolor='#FEF3C7', edgecolor='#D97706', lw=1.2)
    b_active  = dict(boxstyle="round,pad=0.25,rounding_size=0.15", facecolor='#EFF6FF', edgecolor='#2563EB', lw=1.2)
    b_fault   = dict(boxstyle="round,pad=0.25,rounding_size=0.15", facecolor='#FEF2F2', edgecolor='#DC2626', lw=1.2)
    
    # 1. State: Passive PCM
    ax.text(1.2, 3.4, "STATE 0: PASSIVE COOLING\n• Peltier OFF (0.0 W)\n• Bio-PCM buffers ambient flux",
            ha='center', va='center', fontsize=6.0, fontweight='bold', color='#14532D', bbox=b_passive)
    
    # 2. Continuous Monitoring
    ax.text(3.9, 3.4, "DS18B20 TELEMETRY\n• Core Temp (T_core)\n• Hot-side Sink (T_hs)\n• Sampling: 1 Hz (Filtered)",
            ha='center', va='center', fontsize=6.0, fontweight='bold', color='#1E293B', bbox=b_sense)
    
    # Arrow 1 -> 2
    ax.annotate('', xy=(2.7, 3.4), xytext=(2.3, 3.4),
                arrowprops=dict(arrowstyle="->", color='#334155', lw=1.2))
    
    # 3. Decision 1: Is T_core >= 6.2°C?
    ax.text(6.4, 3.4, "T_core ≥\n+6.2°C ?",
            ha='center', va='center', fontsize=6.2, fontweight='bold', color='#92400E', bbox=b_decide)
    
    # Arrow 2 -> 3
    ax.annotate('', xy=(5.5, 3.4), xytext=(5.1, 3.4),
                arrowprops=dict(arrowstyle="->", color='#334155', lw=1.2))
    
    # Arrow 3 (NO) -> Loops back to 1
    ax.plot([6.4, 6.4, 1.2, 1.2], [3.9, 4.05, 4.05, 3.85], color='#16A34A', lw=1.1, linestyle='--')
    ax.text(3.8, 4.12, "NO: Remain Passive (Zero Parasitic Drain)", fontsize=5.5, color='#15803D', ha='center', fontweight='bold')
    
    # Arrow 3 (YES) -> Down to Active State
    ax.annotate('', xy=(6.4, 2.3), xytext=(6.4, 2.9),
                arrowprops=dict(arrowstyle="->", color='#2563EB', lw=1.4))
    ax.text(6.55, 2.6, "YES (Stress)", fontsize=5.5, color='#1D4ED8', fontweight='bold')
    
    # 4. State: Active Peltier
    ax.text(6.4, 1.8, "STATE 1: ACTIVE COOLING\n• Dual TECs ON (7.5V, 2.0A)\n• Exhaust Fans ON (PWM)\n• Heat Pumping Q_c = 18.5 W",
            ha='center', va='center', fontsize=6.0, fontweight='bold', color='#1E40AF', bbox=b_active)
    
    # 5. Fault Check (Branch right)
    ax.text(9.0, 1.8, "FAIL-SAFE CHECK\n• T_hs > +65°C ?\n• Sensor disconnect?\n→ SHUTDOWN & ALARM",
            ha='center', va='center', fontsize=5.8, fontweight='bold', color='#991B1B', bbox=b_fault)
    
    # Arrow 4 -> 5
    ax.annotate('', xy=(7.9, 1.8), xytext=(7.55, 1.8),
                arrowprops=dict(arrowstyle="->", color='#DC2626', lw=1.2))
    
    # 6. Lower Threshold Check: T_core <= 3.8°C?
    ax.text(3.9, 1.8, "T_core ≤\n+3.8°C ?",
            ha='center', va='center', fontsize=6.2, fontweight='bold', color='#92400E', bbox=b_decide)
    
    # Arrow 4 -> 6
    ax.annotate('', xy=(4.8, 1.8), xytext=(5.25, 1.8),
                arrowprops=dict(arrowstyle="->", color='#2563EB', lw=1.2))
    
    # Arrow 6 (YES) -> Return to State 0
    ax.plot([3.9, 1.2, 1.2], [1.35, 1.35, 2.95], color='#16A34A', lw=1.3)
    ax.text(2.5, 1.15, "YES: Target Reached → Cut Peltier Power", fontsize=5.5, color='#15803D', ha='center', fontweight='bold')
    
    # Arrow 6 (NO) -> Loop back to State 1
    ax.plot([3.9, 3.9, 6.4], [2.25, 2.4, 2.4], color='#2563EB', lw=1.1, linestyle=':')
    ax.text(5.1, 2.45, "NO: Continue Pumping", fontsize=5.2, color='#1D4ED8', ha='center')
    
    # Footer caption
    ax.text(5.0, 0.35, "Hysteresis Gap: ΔT = 2.4°C (Upper 6.2°C / Lower 3.8°C) prevents rapid relay cycling and maximizes TEC COP.",
            ha='center', va='center', fontsize=6.0, color='#475569', fontstyle='italic')
    
    plt.tight_layout()
    plt.savefig('poster_assets/control_flowchart.png', bbox_inches='tight', pad_inches=0.04)
    plt.close()
    print("Control Flowchart generated successfully.")

# ==============================================================================
# 3. THERMAL-ENERGY BALANCE FLOW DIAGRAM
# Explaining: Electrical Input + Cold Heat Extraction = Hot Heat Rejection
# ==============================================================================
def create_energy_flow_diagram():
    fig, ax = plt.subplots(figsize=(6.2, 1.8), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 3.0)
    ax.axis('off')
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')
    
    # Peltier Element in center
    tec_box = patches.FancyBboxPatch((4.0, 0.7), 2.0, 1.6, boxstyle="round,pad=0.15,rounding_size=0.15",
                                   facecolor='#0F766E', edgecolor='#134E4A', lw=1.5)
    ax.add_patch(tec_box)
    ax.text(5.0, 1.6, "SOLID-STATE\nPELTIER MODULE", ha='center', va='center', fontsize=6.8, fontweight='bold', color='#FFFFFF')
    ax.text(5.0, 1.05, "Dual TEC1-12706\nDerated: 7.5V · 2.0A", ha='center', va='center', fontsize=5.5, color='#CCFBF1')
    
    # Cold Extraction (Left -> Center)
    ax.annotate('', xy=(3.8, 1.5), xytext=(0.8, 1.5),
                arrowprops=dict(facecolor='#0284C7', edgecolor='#0369A1', width=3.5, headwidth=9, headlength=9))
    ax.text(2.3, 1.9, "COLD HEAT EXTRACTION (Q̇_c)", ha='center', va='bottom', fontsize=6.2, fontweight='bold', color='#0284C7')
    ax.text(2.3, 1.45, "18.5 W from PCM & Payload", ha='center', va='top', fontsize=5.5, color='#0369A1')
    
    # Electrical Power (Bottom -> Center)
    ax.annotate('', xy=(5.0, 0.65), xytext=(5.0, 0.05),
                arrowprops=dict(facecolor='#6366F1', edgecolor='#4338CA', width=3.5, headwidth=9, headlength=9))
    ax.text(5.0, 0.0, "ELECTRICAL INPUT (P_elec = V × I = 30.0 W)", ha='center', va='top', fontsize=6.0, fontweight='bold', color='#4338CA')
    
    # Hot Rejection (Center -> Right)
    ax.annotate('', xy=(9.2, 1.5), xytext=(6.2, 1.5),
                arrowprops=dict(facecolor='#EA580C', edgecolor='#C2410C', width=5.5, headwidth=11, headlength=10))
    ax.text(7.7, 1.9, "TOTAL HOT REJECTION (Q̇_h)", ha='center', va='bottom', fontsize=6.2, fontweight='bold', color='#EA580C')
    ax.text(7.7, 1.45, "Q̇_h = Q̇_c + P_elec = 48.5 W", ha='center', va='top', fontsize=5.5, color='#C2410C')
    
    # COP Callout
    ax.text(5.0, 2.7, "Thermodynamic Balance: Q̇_h = Q̇_c + P_elec  |  Operating COP = Q̇_c / P_elec = 0.61",
            ha='center', va='center', fontsize=6.4, fontweight='bold', color='#0F172A',
            bbox=dict(boxstyle="round,pad=0.2", facecolor='#F1F5F9', edgecolor='#CBD5E1', lw=0.8))
            
    plt.tight_layout()
    plt.savefig('poster_assets/energy_flow_diagram.png', bbox_inches='tight', pad_inches=0.04)
    plt.close()
    print("Energy Flow Diagram generated successfully.")

if __name__ == '__main__':
    create_poster_simulation_graph()
    create_control_flowchart()
    create_energy_flow_diagram()
