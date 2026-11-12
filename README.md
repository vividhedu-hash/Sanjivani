# Sanjivani (संजीवनी)

> **Design and Development of a Sensor-Triggered Hybrid PCM–Peltier Cooling System for Extended Medical Cold-Chain Storage**  
> *Preserving Temperature. Protecting Life.*

**Competition:** Dr. B. K. Passi Memorial Senior Bal Vigyan 2026–2027  
**Category / Subject:** Physics (Thermal Engineering)  
**Theme:** STEM for Viksit and Atmanirbhar Bharat  
**Sub-Theme:** Health and Hygiene  
**Institution:** G. D. Goenka Public School, Indore (M.P.), India  
**Project Code:** SBVPH-05  

---

## 👥 Student Research Team & Mentorship
- **Vaishnavi Shrivastava** — Class XI (Co-Investigator • Thermal Physics & PCM Mechanics)
- **Gaurav Choudhary** — Class XI (Co-Investigator • CAD, Structural Enclosure & Heat Sink Mechanics)
- **Prathamesh Rao** — Class XII (Co-Investigator • Embedded Systems, Hysteresis Logic & Telemetry)
- **Bhavmanyu Singh** — Class XII (Lead Investigator • System Architecture & Thermodynamic Modeling)
- **Mr. Gopal Kumar Roy** — Project Mentor & Research Guide (PGT Physics, Department of Science)

---

## 🔬 System Overview
SANJIVANI is an intelligent hybrid medical cold-chain container engineered to maintain temperature-sensitive vaccines and biologics within the strict **+2.0°C to +8.0°C** WHO safety corridor for up to **110 hours** in extreme ambient conditions (mean 35.0°C diurnal cycling).

### Core Thermodynamic Architecture
1. **Passive Buffer (Primary):** 4.8 kg bio-based phase change material (CrodaTherm 5, $T_m = +5.0^\circ\text{C}$, $L_f = 218\text{ kJ/kg}$) providing 1,046.4 kJ of latent thermal storage.
2. **Active Intervention (Supplementary):** Sensor-triggered dual thermoelectric modules (TEC1-12706 derated at 7.5V / 4A, $\text{COP} \approx 0.61$) pumping $Q_{cold} = 18.5\text{ W}$ during thermal spikes.
3. **Heat Rejection:** Sintered copper heat pipes ($k \approx 398\text{ W/m}\cdot\text{K}$) and 24-fin skived copper stack with dual 80mm PWM fans forcibly exhausting $Q_{hot} = Q_{cold} + P_{elec} = 48.5\text{ W}$ to ambient air.
4. **Embedded Intelligence:** ESP32 microcontroller with DS18B20 1-Wire temperature sensing harness executing non-linear hysteresis switching ($T_{upper} \ge 6.2^\circ\text{C}$, $T_{lower} \le 3.8^\circ\text{C}$) to minimize battery consumption.
5. **Autonomy:** Integrated 12.8V 30Ah LiFePO4 battery pack delivering 384 Wh of autonomous energy at an operating cost of **₹0.24 / operating hour**.

---

## 💻 Interactive Presentation Website
The `/website` directory contains an award-winning scientific presentation web application built with:
- **React 19 & TypeScript**
- **Vite & Tailwind CSS v4**
- **Three.js** interactive 3D cutaway model with realistic 3D airflow streamlines, fluid circulation, and thermal flux vectors
- **Web Audio API** procedural sound synthesizer
- **Two Interaction Modes:** Full-screen Keynote / PowerPoint Presentation Mode and Free-form Engineering Explorer Mode

### Running the Website
```bash
cd website
npm install
npm run dev
```

Build for production:
```bash
cd website
npm run build
npm run preview
```
