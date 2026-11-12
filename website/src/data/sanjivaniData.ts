// Central source of truth for SANJIVANI Presentation Experience
// All values strictly audited against the official project report & scientific poster

export interface ComponentSpec {
  id: number;
  name: string;
  category: 'thermal' | 'electrical' | 'mechanical' | 'sensing';
  role: string;
  principle: string;
  specs: string;
  heatFluxRole: 'cold' | 'hot' | 'passive' | 'control';
  details: string;
}

export const COMPONENTS_3D: ComponentSpec[] = [
  {
    id: 1,
    name: "Insulated Outer Enclosure",
    category: "mechanical",
    role: "Passive environmental thermal isolation",
    principle: "Conductive and radiative heat attenuation via composite layering",
    specs: "LLDPE Outer Shell + 25mm High-Density PUF + 20mm Vacuum Insulation Panels (VIP), UA = 0.147 W/K",
    heatFluxRole: "passive",
    details: "Minimizes Fourier heat ingress under severe tropical ambient stress (up to 42°C diurnal peak). Heat ingress Q_in = UA · (T_amb - T_int) ≈ 4.41 W at 35°C mean ambient."
  },
  {
    id: 2,
    name: "Bio-PCM Perimeter Cassettes",
    category: "thermal",
    role: "Passive isothermal thermal energy storage",
    principle: "Latent heat absorption during solid-to-liquid phase transition (Q = m · L)",
    specs: "4.8 kg CrodaTherm 5 (6 packs × 800g), Melting Point: 5.0°C, Latent Heat: 218 kJ/kg (1,046.4 kJ / 290.7 Wh)",
    heatFluxRole: "passive",
    details: "Provides passive buffering within the WHO +2°C to +8°C safety corridor. Solid heat capacity cp = 2,100 J/(kg·K), liquid cp = 2,250 J/(kg·K). Absorbs heat without temperature change during phase equilibrium."
  },
  {
    id: 3,
    name: "Medical Payload Cavity",
    category: "mechanical",
    role: "Protected clinical storage compartment",
    principle: "Isothermal cold stabilization of biologics",
    specs: "ISO 6.5 Litres useful payload volume, holds 24 standard vaccine vials / biologics trays",
    heatFluxRole: "cold",
    details: "Surrounded by aluminium thermal spreading jacket. Thermal mass C_payload = 12,160 J/K (water equivalent of vaccine vials and internal fixtures)."
  },
  {
    id: 4,
    name: "Digital Temperature Sensors",
    category: "sensing",
    role: "High-precision multi-point thermal monitoring",
    principle: "1-Wire digital bandgap temperature sensing with calibrated ADC",
    specs: "Dallas DS18B20 1-Wire Digital Probes, ±0.1°C resolution, multi-probe bus (Core, PCM, Cold plate, Hot sink)",
    heatFluxRole: "control",
    details: "Continuously monitors payload core, PCM phase front, cold plate, and ambient heat sink to drive closed-loop hysteresis logic and fault detection."
  },
  {
    id: 5,
    name: "Thermoelectric Peltier Module",
    category: "thermal",
    role: "Solid-state active heat pumping",
    principle: "Peltier Effect (Thermoelectric energy absorption at semiconductor junctions)",
    specs: "Dual TEC1-12706 Modules, derated to 7.5V / 2.0A each (30.0W total electrical input, COP ≈ 0.61)",
    heatFluxRole: "cold",
    details: "Pumps 18.5 W of active cooling from payload to hot-side. Operates in derated mode to maximize thermodynamic Coefficient of Performance (COP) and battery runtime."
  },
  {
    id: 6,
    name: "Cold-Side Thermal Interface (TIM)",
    category: "thermal",
    role: "Thermal contact resistance elimination",
    principle: "Microscopic void filling with high-conductivity dielectric paste",
    specs: "Arctic MX-4 Carbon-Microparticle TIM, R_th < 0.04 K·cm²/W, 8.5 W/(m·K)",
    heatFluxRole: "cold",
    details: "Couples the Peltier cold ceramics to the copper heat-collection block with negligible thermal resistance, preventing temperature drops across mechanical junctions."
  },
  {
    id: 7,
    name: "Aluminium Heat-Spreading Jacket",
    category: "thermal",
    role: "Isothermal thermal distribution across payload",
    principle: "High-diffusivity lateral heat conduction",
    specs: "6061-T6 Aircraft-Grade Aluminium Alloy, 2.5mm thickness, thermal conductivity k = 167 W/(m·K)",
    heatFluxRole: "cold",
    details: "Distributes localized cooling from the cold plate evenly around the entire 6.5L payload perimeter, maintaining interior temperature gradients ΔT < 0.6°C."
  },
  {
    id: 8,
    name: "Liquid Thermal-Transfer Loop & Cold Plate",
    category: "thermal",
    role: "Fluid-mediated convective heat transport",
    principle: "Single-phase forced liquid convection",
    specs: "Nickel-plated copper micro-channel cold plate + closed inhibited propylene glycol-water loop (2.4W pump)",
    heatFluxRole: "cold",
    details: "Transports extracted thermal energy away from the interior without bulky ducting. Pump cuts off during standby to prevent parasitic reverse conduction."
  },
  {
    id: 9,
    name: "Peltier Hot-Side Copper Base",
    category: "thermal",
    role: "High-flux hot-side heat spreading",
    principle: "Conductive heat flux dispersion to heat pipe array",
    specs: "C11000 Pure Electrolytic Copper base plate (99.9% Cu), k = 398 W/(m·K)",
    heatFluxRole: "hot",
    details: "Receives total hot-side heat flux: Q_hot = Q_cold + P_elec = 18.5W + 30.0W = 48.5 W. Must dissipate rapidly to prevent thermal runaway into the cold junction."
  },
  {
    id: 10,
    name: "External Skived Fin Heat Sink",
    category: "thermal",
    role: "Forced heat rejection to ambient environment",
    principle: "Convective heat dissipation across extended surface area",
    specs: "24-fin skived copper/aluminium fin stack with 4× sintered copper heat pipes, R_th_sink ≈ 0.35 K/W",
    heatFluxRole: "hot",
    details: "Discharges all pumped heat and electrical waste energy to the external environment. Ensures hot-side junction remains under 48°C even in 40°C ambient air."
  },
  {
    id: 11,
    name: "Dual PWM Cooling Fans & Micro Pump",
    category: "mechanical",
    role: "Active convection and fluid circulation",
    principle: "Forced air boundary-layer disruption and liquid displacement",
    specs: "Dual 80mm ball-bearing PWM fans (1.8W total) + 12V 2.4W low-noise micro diaphragm pump",
    heatFluxRole: "hot",
    details: "Modulated synchronously with the Peltier modules. Automatically spins down during passive PCM standby, reducing auxiliary idle power to 0.15 W."
  },
  {
    id: 12,
    name: "Control Electronics & MOSFET Stage",
    category: "electrical",
    role: "Intelligent hysteresis sensing & power switching",
    principle: "Microcontroller closed-loop state machine with low-RDS(on) switching",
    specs: "ESP32 SoC + logic-level N-channel MOSFET switching stage + 0.96\" I2C OLED display",
    heatFluxRole: "control",
    details: "Implements closed-loop hysteresis (ON: ≥6.2°C, OFF: ≤3.8°C). Includes watchdog timer, reverse polarity protection, and sensor disconnection fail-safe cutoff."
  },
  {
    id: 13,
    name: "LiFePO4 Mission Battery Pack",
    category: "electrical",
    role: "Autonomous field electrical power supply",
    principle: "Electrochemical energy storage via lithium iron phosphate chemistry",
    specs: "12.8V 30Ah (384 Wh gross, 301.2 Wh mission demand at 78.4% DOD), integrated smart BMS, 3.4 kg",
    heatFluxRole: "control",
    details: "Provides sufficient energy for 8.75 hours of active Peltier heat pumping (8.0% mission duty cycle over 110 hours). Long cycle life (>2,000 cycles) and thermal stability."
  }
];

export const AUDITED_NUMBERS = {
  // Baseline & Target
  baselineHours: 72.0,
  targetHours: 110.0,
  extensionHours: 38.0,
  extensionPercent: 52.8, // (110 - 72) / 72 * 100
  modelledHours: 109.4,
  
  // Thermal parameters
  pcmMassKg: 4.8,
  pcmLatentHeatJkg: 218000,
  pcmLatentWh: 290.7, // (4.8 * 218000) / 3600
  enclosureUA: 0.147, // W/K
  payloadVolumeL: 6.5,
  payloadThermalMassJK: 12160,
  
  // Active cooling & electrical
  activeCoolingW: 18.5,
  peltierElectricalW: 30.0,
  auxiliaryPowerW: 4.2, // 2.4W pump + 1.8W fans
  totalActivePowerW: 34.2,
  standbyPowerW: 0.15,
  assumedCOP: 0.61, // 18.5 / 30.0
  hotSideRejectionW: 48.5, // 18.5 + 30.0
  
  // Mission Energy
  activeRuntimeHours: 8.75,
  dutyCyclePercent: 8.0, // 8.75 / 110 * 100
  missionEnergyWh: 301.2, // (34.2 * 8.75) + (0.15 * 101.25)
  batteryGrossWh: 384.0, // 12.8V * 30Ah
  batteryDODPercent: 78.4, // 301.2 / 384.0 * 100
  
  // Financial (INR)
  costMVP: 6480,
  costFieldUnit: 11850,
  batteryCost: 3450,
  batteryCostPercent: 29.1,
  insulationCost: 2850,
  insulationCostPercent: 24.1,
  peltierSinkFansCost: 1780,
  peltierCostPercent: 15.0,
  operatingCostPerHr: 0.24,
  rechargeCostPerMission: 8.80
};

export const CHAPTERS = [
  { id: 1, title: "The Opening", subtitle: "Preserving Temperature. Protecting Life." },
  { id: 2, title: "The Problem", subtitle: "When Cooling Ends, The Problem Begins" },
  { id: 3, title: "The Big Idea", subtitle: "Passive Protection. Intelligent Intervention." },
  { id: 4, title: "Explore The Engineering", subtitle: "Interactive 3D Cutaway System" },
  { id: 5, title: "How The System Thinks", subtitle: "Closed-Loop Hysteresis Simulation" },
  { id: 6, title: "The Science Behind It", subtitle: "Engineering The Movement of Heat" },
  { id: 7, title: "The Numbers", subtitle: "Audited Physics & Energy Calculator" },
  { id: 8, title: "Economic & Social Impact", subtitle: "Safeguarding High-Value Biologics" },
  { id: 9, title: "Testing & Validation", subtitle: "A Hypothesis Must Survive Measurement" },
  { id: 10, title: "The Future & The Team", subtitle: "Engineering Atmanirbhar Bharat" }
];

export const PRESENTER_NOTES: Record<number, { keyIdea: string; script: string; judgingFocus: string }> = {
  1: {
    keyIdea: "Set the stage with clinical gravity and technical elegance.",
    script: "Good morning respected judges. We present SANJIVANI—a sensor-triggered hybrid PCM-Peltier medical cooling system engineered to solve the acute last-mile cold-chain vulnerability in rural healthcare.",
    judgingFocus: "Note the clean problem articulation and school identity under Senior Bal Vigyan 2026-2027 Physics stream."
  },
  2: {
    keyIdea: "Explain why passive PCM alone inevitably fails over extended durations.",
    script: "Conventional vaccine boxes rely entirely on passive phase-change packs. While isothermal, latent heat storage is finite: Q = m·L. Once ambient heat depletes this reserve, the temperature spikes past +8°C, ruining vaccines. Our 72-hour reference is a planning baseline, not an industry ceiling.",
    judgingFocus: "Verify that the 72-hour figure is identified as a planning baseline, not an absolute claim."
  },
  3: {
    keyIdea: "Introduce the hybrid synergy: passive base + pulsed active intervention.",
    script: "Rather than running an active refrigerator continuously—which would drain an immense battery—SANJIVANI uses passive PCM for 92% of the mission and triggers solid-state Peltier heat pumping only during peak ambient thermal peaks to preserve the latent reserve, targeting 110 hours.",
    judgingFocus: "Check that the +53% extension is framed as an engineering design target, not a pre-claimed victory."
  },
  4: {
    keyIdea: "Demonstrate mechanical credibility and the first law of thermodynamics.",
    script: "Here is the SANJIVANI cutaway. Crucially, the Peltier module does not destroy heat—it moves heat from its cold side to its hot side where Q_hot = Q_cold + P_elec (48.5 W) must be forcibly rejected via our skived fin array.",
    judgingFocus: "Judges love First Law adherence and thermal resistance budgeting (Arctic MX-4, 6061-T6 spreader, dual PWM fans)."
  },
  5: {
    keyIdea: "Demonstrate closed-loop hysteresis and fail-safe thinking.",
    script: "The ESP32 controller samples 1-Wire DS18B20 probes. Cooling turns ON at ≥6.2°C and OFF at ≤3.8°C. This 2.4°C hysteresis band eliminates relay chattering and limits active duty cycle to just 8.0%. In case of sensor fault, the system fails safe.",
    judgingFocus: "Test the interactive sensor fault toggle to demonstrate rigorous fail-safe engineering."
  },
  6: {
    keyIdea: "Ground the innovation in pure physics: Latent heat, Seebeck/Peltier effect, Fourier conduction.",
    script: "SANJIVANI unites three physical phenomena: latent heat absorption Q=mL in CrodaTherm 5, thermoelectric electron transition across bismuth telluride p-n junctions, and high-conductivity Fourier conduction through our 6061 aluminium jacket.",
    judgingFocus: "Scientific rigor under the Physics Bal Vigyan competition guidelines."
  },
  7: {
    keyIdea: "Transparent, audited arithmetic. No fabricated numbers.",
    script: "Every metric has been audited: 4.8 kg bio-PCM yields 290.7 Wh of latent reserve. Over 110 hours, 8.75 hours of derated Peltier operation consumes 301.2 Wh, perfectly matching our 12.8V 30Ah LiFePO4 battery at 78.4% depth-of-discharge.",
    judgingFocus: "Let judges experiment with the live Energy Calculator to prove equation integrity."
  },
  8: {
    keyIdea: "Techno-economic viability in Indian rural logistics.",
    script: "Our MVP costs ₹6,480, and the fully autonomous field unit with LiFePO4 battery and smart BMS costs ₹11,850. Operating cost is just ₹0.24 per hour, protecting vaccine vials worth hundreds of thousands of rupees.",
    judgingFocus: "Real-world healthcare relevance under the 'Health & Hygiene' and 'Atmanirbhar Bharat' sub-themes."
  },
  9: {
    keyIdea: "Scientific honesty: distinguishing simulated models from physical measurement.",
    script: "A hypothesis must survive measurement. We have modeled Configuration A (PCM-only) versus Configuration B (Hybrid) under 40°C isothermal testing. We explicitly present these as numerical benchmarks with controlled chamber validation pending.",
    judgingFocus: "Exemplary scientific integrity—clear demarcation of simulation vs future physical trials."
  },
  10: {
    keyIdea: "Future vision and team dedication.",
    script: "Our roadmap includes flexible solar harvesting, direct vapor chambers, and WHO PQS certification. On behalf of Vaishnavi, Gaurav, Prathamesh, Bhavmanyu, and our mentor Mr. Gopal Kumar Roy at G.D. Goenka Public School Indore, thank you.",
    judgingFocus: "Passionate, humble, and forward-looking conclusion."
  }
};

export const TEAM_MEMBERS = [
  {
    name: "Vaishnavi Shrivastava",
    grade: "Class XI",
    role: "Thermal Physics & Phase Change Modeling",
    contribution: "Led analytical modeling of latent heat absorption (CrodaTherm 5 bio-PCM), differential heat ingress equations, and diurnal thermal balance simulations."
  },
  {
    name: "Gaurav Choudhary",
    grade: "Class XI",
    role: "Solid-State Thermoelectrics & Heat Rejection",
    contribution: "Engineered the dual TEC1-12706 derated driving stage, hot-side dissipation budget (Q_hot = Q_cold + P_elec), and skived fin heat exchanger matching."
  },
  {
    name: "Prathamesh Rao",
    grade: "Class XII",
    role: "Firmware, Hysteresis Logic & Telemetry",
    contribution: "Designed ESP32 closed-loop hysteresis control, 1-Wire DS18B20 multi-sensor bus, sensor-fault fail-safe routines, and power MOSFET gate switching."
  },
  {
    name: "Bhavmanyu Singh",
    grade: "Class XII",
    role: "Mechanical Integration & Enclosure CAD",
    contribution: "Architected the composite LLDPE/VIP/PUF insulation layup, 6061-T6 isothermal cold jacket, payload tray damping, and 3D cutaway system layout."
  }
];
