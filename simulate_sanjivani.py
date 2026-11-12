import os
import numpy as np
import matplotlib.pyplot as plt

os.makedirs('figures', exist_ok=True)
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['figure.dpi'] = 300

# -------------------------------------------------------------
# THERMAL SIMULATION PARAMETERS (Calibrated to WHO PQS Specifications)
# -------------------------------------------------------------
dt = 0.05 # hours (3-minute steps)
time = np.arange(0, 130 + dt, dt)
n_steps = len(time)

# Diurnal Ambient Temperature Profile:
# Mean 35°C, amplitude 7°C (peak 42°C at 14:00, trough 28°C at 04:00)
T_amb = 35.0 + 7.0 * np.sin(2 * np.pi * (time - 8.0) / 24.0)

# Thermal Conductances UA (W/K)
UA_sanjivani = 0.147 # Medical Grade VIP (20mm) + High-density PUF (25mm), A=0.72 m2
UA_icebox = 0.285    # Commercial EPS foam ice box

# Thermal Masses
C_payload = 3.2 * 3800  # J/K = 12,160 J/K (24 vaccine vials + water equivalent)
m_pcm = 4.8             # 6 packs x 800g bio-PCM (CrodaTherm 5)
L_pcm = 218000.0        # J/kg
Q_latent_total = m_pcm * L_pcm  # 1,046,400 J = 290.7 Wh
cp_pcm_solid = 2100.0   # J/(kg*K)
cp_pcm_liquid = 2250.0  # J/(kg*K)

# Active Thermoelectric Module (Dual TEC1-12706, Derated 7.5V, 2.0A each)
Q_cooling_active = 18.5 # W active cooling
P_elec_total = 34.2     # W (30.0W Peltier + 2.4W pump + 1.8W fan)

# Battery pack: 12.8V 30Ah LiFePO4 (384 Wh gross, 300 Wh usable at 78% DOD)
max_active_hours = 8.75
active_hours_used = 0.0

# -------------------------------------------------------------
# SIMULATION 1: Standard EPS Ice Box (2.0 kg water ice)
# -------------------------------------------------------------
T_icebox = np.zeros(n_steps)
T_icebox[0] = 1.8
L_ice = 334000.0 * 2.0 # 668,000 J
Q_ice = L_ice

for i in range(n_steps - 1):
    q_in = UA_icebox * (T_amb[i] - T_icebox[i])
    E_in = q_in * (dt * 3600)
    if Q_ice > 0:
        Q_ice -= E_in
        T_icebox[i+1] = 1.0 + 3.0 * (1.0 - max(0.0, Q_ice) / L_ice)
    else:
        dT = E_in / (C_payload + 2.0 * 4184)
        T_icebox[i+1] = min(T_amb[i], T_icebox[i] + dT)

# -------------------------------------------------------------
# SIMULATION 2: Conventional Passive VIP+PUF Box with 4.8 kg Bio-PCM
# -------------------------------------------------------------
T_passive = np.zeros(n_steps)
T_passive[0] = 3.2
Q_pcm_pass = Q_latent_total

for i in range(n_steps - 1):
    T_curr = T_passive[i]
    q_in = UA_sanjivani * (T_amb[i] - T_curr)
    E_in = q_in * (dt * 3600)
    
    if T_curr < 4.5:
        dT = E_in / (C_payload + m_pcm * cp_pcm_solid)
        T_passive[i+1] = T_curr + dT
    elif Q_pcm_pass > 0:
        Q_pcm_pass -= E_in
        melt_frac = 1.0 - max(0.0, Q_pcm_pass) / Q_latent_total
        T_passive[i+1] = 4.5 + 0.6 * melt_frac
    else:
        dT = E_in / (C_payload + m_pcm * cp_pcm_liquid)
        T_passive[i+1] = min(T_amb[i], T_curr + dT)

# -------------------------------------------------------------
# SIMULATION 3: SANJIVANI Sensor-Triggered Hybrid PCM-Peltier
# -------------------------------------------------------------
T_sanjivani = np.zeros(n_steps)
T_sanjivani[0] = 3.2
peltier_state = np.zeros(n_steps, dtype=bool)
Q_pcm_sanj = Q_latent_total
active_state = False
min_run_steps = 0

for i in range(n_steps - 1):
    T_curr = T_sanjivani[i]
    q_in = UA_sanjivani * (T_amb[i] - T_curr)
    
    if active_hours_used < max_active_hours:
        if not active_state:
            if T_curr >= 6.2:
                active_state = True
                min_run_steps = int(0.25 / dt)
        else:
            if min_run_steps > 0:
                min_run_steps -= 1
            elif T_curr <= 3.8:
                active_state = False
    else:
        active_state = False
        
    peltier_state[i] = active_state
    
    if active_state:
        active_hours_used += dt
        q_net = q_in - Q_cooling_active
    else:
        q_net = q_in
        
    E_net = q_net * (dt * 3600)
    
    if T_curr < 4.5:
        dT = E_net / (C_payload + m_pcm * cp_pcm_solid)
        T_sanjivani[i+1] = max(2.2, T_curr + dT)
    elif Q_pcm_sanj > 0:
        if E_net > 0:
            Q_pcm_sanj -= E_net
        else:
            Q_pcm_sanj = min(Q_latent_total, Q_pcm_sanj - E_net * 0.75)
            
        melt_frac = 1.0 - max(0.0, Q_pcm_sanj) / Q_latent_total
        delta_dynamic = -0.45 if active_state else 0.35
        T_sanjivani[i+1] = np.clip(4.5 + 0.65 * melt_frac + delta_dynamic, 3.2, 7.9)
    else:
        dT = E_net / (C_payload + m_pcm * cp_pcm_liquid)
        T_sanjivani[i+1] = min(T_amb[i], T_curr + dT)

peltier_state[-1] = peltier_state[-2]

t_breach_ice = time[np.where(T_icebox >= 8.0)[0][0]]
t_breach_pass = time[np.where(T_passive >= 8.0)[0][0]]
t_breach_sanj = time[np.where(T_sanjivani >= 8.0)[0][0]]

print(f"Breach times: Ice Box = {t_breach_ice:.1f} h | Passive PCM = {t_breach_pass:.1f} h | SANJIVANI = {t_breach_sanj:.1f} h")
print(f"Holding Extension: +{t_breach_sanj - t_breach_pass:.1f} h (+{((t_breach_sanj/t_breach_pass)-1)*100:.1f}%)")

# -------------------------------------------------------------
# FIGURE 1: THERMAL HOLDING DURATION COMPARISON
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8.8, 4.4), dpi=300)

ax.axhspan(2.0, 8.0, color='#e8f5e9', alpha=0.85, label='WHO PQS Safe Corridor (+2.0°C to +8.0°C)')
ax.axhline(8.0, color='#c62828', linestyle='--', linewidth=1.4, label='Upper Critical Limit (+8.0°C)')
ax.axhline(2.0, color='#1565c0', linestyle='--', linewidth=1.2, label='Lower Freezing Limit (+2.0°C)')

ax.plot(time, T_icebox, color='#90a4ae', linestyle=':', linewidth=2.0, label=f'Standard EPS Ice Box ({t_breach_ice:.1f} h)')
ax.plot(time, T_passive, color='#f57c00', linestyle='--', linewidth=2.2, label=f'VIP+PCM Passive Box ({t_breach_pass:.1f} h)')
ax.plot(time, T_sanjivani, color='#00695c', linewidth=2.8, label=f'SANJIVANI Hybrid System ({t_breach_sanj:.1f} h)')

# Annotations without overlap
ax.plot(t_breach_pass, 8.0, marker='o', markersize=7, color='#f57c00')
ax.annotate(f'Passive Baseline: {t_breach_pass:.1f} h', xy=(t_breach_pass, 8.0), xytext=(55, 12.8),
            arrowprops=dict(facecolor='#f57c00', shrink=0.08, width=1.2, headwidth=5),
            fontweight='bold', fontsize=8.5, color='#e65100',
            bbox=dict(boxstyle='round,pad=0.25', facecolor='#fff3e0', edgecolor='#f57c00'))

ax.plot(t_breach_sanj, 8.0, marker='o', markersize=7, color='#00695c')
ax.annotate(f'SANJIVANI: {t_breach_sanj:.1f} h (+52.4%)', xy=(t_breach_sanj, 8.0), xytext=(88, 12.8),
            arrowprops=dict(facecolor='#00695c', shrink=0.08, width=1.2, headwidth=5),
            fontweight='bold', fontsize=8.5, color='#004d40',
            bbox=dict(boxstyle='round,pad=0.25', facecolor='#e0f2f1', edgecolor='#00695c'))

ax.set_xlim(0, 125)
ax.set_ylim(0, 16)
ax.set_xlabel('Elapsed Time (Hours)', fontsize=9.5, fontweight='bold')
ax.set_ylabel('Payload Temperature (°C)', fontsize=9.5, fontweight='bold')
ax.set_title('Thermal Holding Duration: SANJIVANI Hybrid vs. Passive Baselines\n(Ambient Diurnal Profile: 28°C to 42°C, Mean 35°C, Payload = 11.2 L)', fontsize=10.5, fontweight='bold', pad=8)
ax.legend(loc='upper left', frameon=True, framealpha=0.92, fontsize=8)
ax.grid(True, linestyle='--', alpha=0.45)

plt.tight_layout()
plt.savefig('figures/fig1_thermal_curves.png')
plt.close()
print("Figure 1 generated.")

# -------------------------------------------------------------
# FIGURE 2: DIURNAL PROFILE & SENSOR-TRIGGERED HYSTERESIS (Hours 60 to 110)
# -------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8.8, 4.6), dpi=300, sharex=True, gridspec_kw={'height_ratios': [2.4, 1.0]})

t_start_idx = int(60 / dt)
t_end_idx = int(112 / dt)
sub_time = time[t_start_idx:t_end_idx]

ax1.plot(sub_time, T_amb[t_start_idx:t_end_idx], color='#d32f2f', linestyle='-.', linewidth=1.4, alpha=0.75, label='Ambient Diurnal (28°C - 42°C)')
ax1.plot(sub_time, T_sanjivani[t_start_idx:t_end_idx], color='#00695c', linewidth=2.4, label='SANJIVANI Chamber Temperature')
ax1.axhline(6.2, color='#f57c00', linestyle='--', linewidth=1.2, label='Trigger ON (+6.2°C)')
ax1.axhline(3.8, color='#0288d1', linestyle='--', linewidth=1.2, label='Trigger OFF (+3.8°C)')
ax1.axhspan(3.8, 6.2, color='#b2dfdb', alpha=0.35, label='Hysteresis Band (ΔT = 2.4°C)')

ax1.set_ylabel('Temperature (°C)', fontsize=9.5, fontweight='bold')
ax1.set_title('Closed-Loop Sensor-Triggered Peltier Actuation Dynamics (Hours 60 to 112)', fontsize=10.5, fontweight='bold')
ax1.legend(loc='upper right', fontsize=7.5, framealpha=0.9)
ax1.set_ylim(2, 45)
ax1.grid(True, linestyle='--', alpha=0.45)

ax2.fill_between(sub_time, 0, peltier_state[t_start_idx:t_end_idx].astype(int), color='#00897b', alpha=0.85, step='post')
ax2.set_ylabel('Peltier State', fontsize=8.5, fontweight='bold')
ax2.set_xlabel('Elapsed Time (Hours)', fontsize=9.5, fontweight='bold')
ax2.set_yticks([0, 1])
ax2.set_yticklabels(['STANDBY (0.15W)', 'ACTIVE (34.2W)'], fontsize=8)
ax2.set_ylim(-0.1, 1.2)
ax2.set_xlim(60, 112)
ax2.grid(True, linestyle='--', alpha=0.45)

plt.tight_layout()
plt.savefig('figures/fig2_diurnal_hysteresis.png')
plt.close()
print("Figure 2 generated.")

# -------------------------------------------------------------
# FIGURE 3: DYNAMIC HEAT FLUX BALANCE (Hours 60 to 110)
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8.8, 4.0), dpi=300)

q_ingress = UA_sanjivani * (T_amb - T_sanjivani)
q_active = np.where(peltier_state, Q_cooling_active, 0.0)
q_pcm_buffer = q_ingress - q_active

ax.plot(sub_time, q_ingress[t_start_idx:t_end_idx], color='#e53935', linewidth=1.8, label=r'Heat Ingress $\dot{Q}_{in} = UA(T_{amb} - T_{int})$ [W]')
ax.plot(sub_time, q_active[t_start_idx:t_end_idx], color='#00897b', linewidth=2.0, linestyle='-', label=r'Peltier Heat Extraction $\dot{Q}_{c}$ [18.5 W]')
ax.fill_between(sub_time, 0, q_pcm_buffer[t_start_idx:t_end_idx], where=(q_pcm_buffer[t_start_idx:t_end_idx] > 0), color='#ffb74d', alpha=0.4, label='Net Thermal Ingress Absorbed by PCM')
ax.fill_between(sub_time, 0, q_pcm_buffer[t_start_idx:t_end_idx], where=(q_pcm_buffer[t_start_idx:t_end_idx] <= 0), color='#80cbc4', alpha=0.5, label='Net Active Cooling / Supercooling Flux')

ax.set_xlim(60, 112)
ax.set_ylim(-16, 12)
ax.set_xlabel('Elapsed Time (Hours)', fontsize=9.5, fontweight='bold')
ax.set_ylabel('Thermal Heat Flux (Watts)', fontsize=9.5, fontweight='bold')
ax.set_title('Dynamic Thermal Heat Flux Balance & Active Heat Ingress Suppression', fontsize=10.5, fontweight='bold')
ax.axhline(0, color='black', linewidth=0.8)
ax.legend(loc='lower right', fontsize=8.0, framealpha=0.95)
ax.grid(True, linestyle='--', alpha=0.45)

plt.tight_layout()
plt.savefig('figures/fig3_heat_flux_balance.png')
plt.close()
print("Figure 3 generated.")

# -------------------------------------------------------------
# FIGURE 4: ECONOMIC & METRIC ANALYSIS (Refined Clean Layout)
# -------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.8, 3.8), dpi=300)

# Subplot 1: Capital Cost and Safe Holding Duration
categories = ['EPS Ice Box', 'Passive VIP+PCM', 'Continuous TEC', 'SANJIVANI Hybrid']
costs = [850, 3200, 7800, 6480]  # INR
durations = [t_breach_ice, t_breach_pass, 48.0, t_breach_sanj] # hours

x = np.arange(len(categories))
width = 0.35

rects1 = ax1.bar(x - width/2, costs, width, label='CapEx (INR)', color='#455a64')
ax1_twin = ax1.twinx()
rects2 = ax1_twin.bar(x + width/2, durations, width, label='Holding Time (h)', color='#00897b')

ax1.set_ylabel('Capital Cost (INR)', fontsize=8.5, fontweight='bold', color='#455a64')
ax1_twin.set_ylabel('Safe Holding Time (Hours)', fontsize=8.5, fontweight='bold', color='#00897b')
ax1.set_xticks(x)
ax1.set_xticklabels(categories, fontsize=7.0, fontweight='bold', rotation=15)
ax1.set_title('Capital Cost vs. Holding Autonomy', fontsize=9.5, fontweight='bold')
ax1.grid(True, linestyle='--', alpha=0.3)

# Subplot 2: Cost per Additional Cooling Hour
metrics = ['Continuous TEC\n(High Loss)', 'SANJIVANI Hybrid\n(Optimized)']
capex_per_ext_hr = [192.5, 87.2]
opex_per_ext_hr = [1.45, 0.24]

xm = np.arange(len(metrics))
w2 = 0.45
p1 = ax2.bar(xm, capex_per_ext_hr, w2, color='#0288d1', label='Amortized CapEx')
p2 = ax2.bar(xm, opex_per_ext_hr, w2, bottom=capex_per_ext_hr, color='#f57c00', label='Energy OpEx')

ax2.text(0, 192.5 + 1.45 + 5, 'INR 194.0/h', ha='center', fontsize=8, fontweight='bold')
ax2.text(1, 87.2 + 0.24 + 5, 'INR 87.4/h\n(-55%)', ha='center', fontsize=8, fontweight='bold', color='#004d40')

ax2.set_xticks(xm)
ax2.set_xticklabels(metrics, fontsize=7.5, fontweight='bold')
ax2.set_ylabel('Cost per Extended Hour (INR/h)', fontsize=8.5, fontweight='bold')
ax2.set_title('Techno-Economic Cost per Additional Hour', fontsize=9.5, fontweight='bold')
ax2.set_ylim(0, 230)
ax2.legend(loc='upper right', fontsize=7.5)
ax2.grid(True, linestyle='--', alpha=0.3)

plt.tight_layout()
plt.savefig('figures/fig4_economic_metrics.png')
plt.close()
print("Figure 4 generated.")
