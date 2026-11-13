import React, { useState, useEffect } from 'react';
import { 
  Zap, 
  ShieldCheck, 
  Cpu, 
  BatteryCharging, 
  RotateCw, 
  Radio, 
  CheckCircle2, 
  ChevronRight,
  Sparkles
} from 'lucide-react';
import { sound } from '../utils/soundEffects';

export interface SubsystemPoint {
  id: number;
  label: string;
  shortName: string;
  angle: number; // in degrees for circular placement
  role: string;
  specs: string;
  metric: string;
  metricLabel: string;
  equation: string;
  description: string;
  color: string;
  borderColor: string;
  glowColor: string;
}

export const SUBSYSTEM_POINTS: SubsystemPoint[] = [
  {
    id: 1,
    label: "POINT 1",
    shortName: "Thermoelectric Heat Pump",
    angle: 45,
    role: "Active Thermodynamic Heat Pumping",
    specs: "Dual TEC1-12706 Modules derated to 7.5V / 2.0A (30.0W Electrical Input)",
    metric: "COP = 0.61",
    metricLabel: "Thermodynamic Efficiency",
    equation: "COP = Q_c / W_elec = 18.5 W / 30.0 W",
    description: "Solid-state Peltier semiconductors pump active heat out of the vaccine cavity into the skived heat sink with zero moving refrigerants, eliminating compressor weight and toxic chemicals.",
    color: "#0284C7",
    borderColor: "#38BDF8",
    glowColor: "rgba(56, 189, 248, 0.4)"
  },
  {
    id: 2,
    label: "POINT 2",
    shortName: "Bio-PCM Isothermal Cassettes",
    angle: 135,
    role: "Passive Latent Heat Energy Storage",
    specs: "4.8 kg CrodaTherm 5 (6 packs × 800g), Melting Point: 5.0°C",
    metric: "1,046.4 kJ",
    metricLabel: "Latent Storage (290.7 Wh)",
    equation: "Q_latent = m · L = 4.8 kg × 218 kJ/kg",
    description: "During power cutoff or transit rest, the plant-based bio-PCM absorbs Fourier heat ingress through isothermal phase change without rising above +5°C, ensuring continuous WHO compliance.",
    color: "#0F766E",
    borderColor: "#2DD4BF",
    glowColor: "rgba(45, 212, 191, 0.4)"
  },
  {
    id: 3,
    label: "POINT 3",
    shortName: "Closed-Loop Hysteresis Sensing",
    angle: 225,
    role: "Algorithmic Thermal Duty-Cycle Control",
    specs: "Quad Dallas DS18B20 Digital Probes (Payload, PCM, Cold-plate, Hot-sink)",
    metric: "±0.1°C",
    metricLabel: "Digital Resolution",
    equation: "Duty = t_on / (t_on + t_off) ≈ 28.5%",
    description: "Microcontroller polls 1-Wire temperature sensors every 500ms, triggering Peltier cooling at +5.5°C and turning off at +2.8°C to prevent vaccine freezing and conserve 71.5% battery power.",
    color: "#D97706",
    borderColor: "#FBBF24",
    glowColor: "rgba(251, 191, 36, 0.4)"
  },
  {
    id: 4,
    label: "POINT 4",
    shortName: "LiFePO4 Power & Hybrid Solar",
    angle: 315,
    role: "Autonomous Energy System",
    specs: "12.8V 100Ah LiFePO4 Chemistry + Optional 60W Foldable Monocrystalline PV",
    metric: "42.8 Hours",
    metricLabel: "Holding Time Autonomy",
    equation: "E_batt = 12.8V × 100Ah = 1,280 Wh",
    description: "Lightweight, thermally stable lithium iron phosphate chemistry provides 2,500+ charge cycles and 42.8 hours of autonomous mission holding time under harsh tropical ambient temperatures.",
    color: "#10B981",
    borderColor: "#34D399",
    glowColor: "rgba(52, 211, 153, 0.4)"
  }
];

interface OrbitalRadarHUDProps {
  isSlideMode?: boolean;
}

export const OrbitalRadarHUD: React.FC<OrbitalRadarHUDProps> = ({ isSlideMode = false }) => {
  const [selectedPointId, setSelectedPointId] = useState<number>(1);
  const [rotationAngle, setRotationAngle] = useState<number>(0);
  const [autoRotate, setAutoRotate] = useState<boolean>(true);

  // Smooth continuous radar rotation
  useEffect(() => {
    let animId: number;
    let lastTime = performance.now();

    const animate = (time: number) => {
      const delta = (time - lastTime) / 1000;
      lastTime = time;
      if (autoRotate) {
        setRotationAngle(prev => (prev + delta * 24) % 360);
      }
      animId = requestAnimationFrame(animate);
    };

    animId = requestAnimationFrame(animate);
    return () => cancelAnimationFrame(animId);
  }, [autoRotate]);

  const activePoint = SUBSYSTEM_POINTS.find(p => p.id === selectedPointId) || SUBSYSTEM_POINTS[0];

  return (
    <div 
      className={`relative w-full flex flex-col lg:flex-row items-center justify-between gap-8 p-4 sm:p-8 rounded-3xl bg-gradient-to-br from-[#0B1523] via-[#08111D] to-[#040910] border border-slate-800 shadow-2xl text-white overflow-hidden select-none ${
        isSlideMode ? 'min-h-[380px]' : 'min-h-[520px]'
      }`}
      onMouseEnter={() => setAutoRotate(false)}
      onMouseLeave={() => setAutoRotate(true)}
    >
      {/* Background Cyber Grid & Vignette */}
      <div className="absolute inset-0 bg-[linear-gradient(to_right,#0f766e10_1px,transparent_1px),linear-gradient(to_bottom,#0f766e10_1px,transparent_1px)] bg-[size:32px_32px] pointer-events-none" />
      <div className="absolute -top-32 -left-32 w-80 h-80 rounded-full bg-[#0F766E]/15 blur-3xl pointer-events-none" />
      <div className="absolute -bottom-32 -right-32 w-80 h-80 rounded-full bg-[#0284C7]/15 blur-3xl pointer-events-none" />

      {/* LEFT: Interactive Holographic Radar Dial */}
      <div className="relative flex items-center justify-center w-[300px] sm:w-[380px] lg:w-[420px] h-[300px] sm:h-[380px] lg:h-[420px] shrink-0">
        
        {/* Outermost Segmented Dial Ring */}
        <div 
          className="absolute inset-4 rounded-full border border-dashed border-teal-500/25 transition-transform duration-300"
          style={{ transform: `rotate(${rotationAngle * 0.5}deg)` }}
        />
        
        {/* Concentric Telemetry Circles */}
        <div className="absolute inset-10 rounded-full border border-teal-500/30" />
        <div className="absolute inset-20 rounded-full border border-sky-500/25 border-dashed" />
        <div className="absolute inset-28 rounded-full border border-teal-500/20" />
        <div className="absolute inset-36 rounded-full border border-amber-500/30" />

        {/* 360-Degree Radial Rotating Radar Sweep Beam */}
        <div 
          className="absolute inset-8 rounded-full pointer-events-none transition-transform"
          style={{ 
            transform: `rotate(${rotationAngle}deg)`,
            background: 'conic-gradient(from 0deg at 50% 50%, rgba(45, 212, 191, 0.35) 0deg, rgba(45, 212, 191, 0.08) 45deg, transparent 90deg)'
          }}
        />

        {/* Crosshair Axes */}
        <div className="absolute inset-x-8 top-1/2 -translate-y-1/2 h-[1px] bg-teal-500/20 pointer-events-none" />
        <div className="absolute inset-y-8 left-1/2 -translate-x-1/2 w-[1px] bg-teal-500/20 pointer-events-none" />

        {/* Radar Center Hub: Sanjivani Core */}
        <div className="relative z-10 w-20 h-20 rounded-full bg-[#08111D] border-2 border-[#0F766E] shadow-lg shadow-teal-500/30 flex flex-col items-center justify-center p-1 text-center">
          <div className="w-2.5 h-2.5 rounded-full bg-teal-400 animate-ping mb-1" />
          <span className="font-mono text-[9px] font-bold text-teal-300 tracking-tighter">SANJIVANI</span>
          <span className="font-mono text-[8px] text-slate-400">CORE HUD</span>
        </div>

        {/* 4 Interactive Subsystem Nodes on Circular Orbit */}
        {SUBSYSTEM_POINTS.map((pt) => {
          const isSelected = pt.id === selectedPointId;
          const rad = (pt.angle * Math.PI) / 180;
          const orbitRadius = 135; // Distance from center
          const x = Math.cos(rad) * orbitRadius;
          const y = Math.sin(rad) * orbitRadius;

          return (
            <div
              key={pt.id}
              onClick={() => {
                sound.click();
                setSelectedPointId(pt.id);
              }}
              style={{
                transform: `translate(${x}px, ${y}px)`
              }}
              className={`absolute z-20 flex flex-col items-center justify-center cursor-pointer transition-all duration-300 group`}
            >
              {/* Node Circular Trigger */}
              <div 
                className={`w-12 h-12 rounded-2xl flex items-center justify-center font-mono font-bold text-xs transition-all duration-300 shadow-xl ${
                  isSelected 
                    ? 'scale-115 ring-4 ring-white/30 text-white' 
                    : 'scale-100 opacity-80 hover:opacity-100 hover:scale-105 text-slate-300 bg-[#0B1523]/90'
                }`}
                style={{
                  backgroundColor: isSelected ? pt.color : '#0B1523',
                  borderColor: pt.borderColor,
                  borderWidth: '2px',
                  boxShadow: isSelected ? `0 0 25px ${pt.glowColor}` : 'none'
                }}
              >
                {pt.id === 1 && <Zap className="w-5 h-5" />}
                {pt.id === 2 && <ShieldCheck className="w-5 h-5" />}
                {pt.id === 3 && <Cpu className="w-5 h-5" />}
                {pt.id === 4 && <BatteryCharging className="w-5 h-5" />}
              </div>

              {/* Point Indicator Pill */}
              <span 
                className={`mt-1 font-mono text-[10px] font-bold px-2 py-0.5 rounded-full backdrop-blur-md transition-all duration-300 ${
                  isSelected 
                    ? 'bg-white text-slate-900 shadow-md scale-105' 
                    : 'bg-black/60 text-slate-300 border border-slate-700'
                }`}
              >
                {pt.label}
              </span>
            </div>
          );
        })}
      </div>

      {/* RIGHT: Detailed Subsystem Engineering Dossier Card */}
      <div className="relative z-10 flex-1 max-w-xl w-full flex flex-col justify-between p-6 sm:p-8 rounded-2xl bg-[#0C1827]/85 border border-slate-700/80 backdrop-blur-xl shadow-2xl">
        
        {/* Top Header Row with Active Badge */}
        <div className="flex items-center justify-between pb-4 border-b border-slate-800">
          <div className="flex items-center gap-2">
            <span 
              className="w-3 h-3 rounded-full animate-pulse"
              style={{ backgroundColor: activePoint.borderColor }}
            />
            <span className="font-mono text-xs font-bold uppercase tracking-wider text-teal-400">
              {activePoint.label} ARCHITECTURE TELEMETRY
            </span>
          </div>

          <div className="flex items-center gap-1 font-mono text-[11px] text-slate-400 bg-slate-900 px-2.5 py-1 rounded-lg border border-slate-800">
            <Radio className="w-3 h-3 text-teal-400 animate-pulse" />
            <span>ORBIT 360° ACTIVE</span>
          </div>
        </div>

        {/* Title & Core Subsystem Role */}
        <div className="py-4 space-y-1">
          <h3 className="font-serif-display text-2xl sm:text-3xl font-bold text-white tracking-wide">
            {activePoint.shortName}
          </h3>
          <p className="text-sm font-sans-tech text-teal-300 font-medium">
            {activePoint.role}
          </p>
        </div>

        {/* Metric Highlight Box & Governing Equation */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 my-2">
          
          {/* Performance Metric Pill */}
          <div className="p-4 rounded-xl bg-black/40 border border-slate-700/80 flex flex-col justify-center">
            <span className="text-[10px] font-mono text-slate-400 uppercase tracking-wider">
              {activePoint.metricLabel}
            </span>
            <span className="font-mono text-2xl font-bold text-white mt-0.5">
              {activePoint.metric}
            </span>
          </div>

          {/* Governing Physics Equation */}
          <div className="p-4 rounded-xl bg-teal-950/30 border border-teal-500/30 flex flex-col justify-center">
            <span className="text-[10px] font-mono text-teal-400 uppercase tracking-wider">
              GOVERNING EQUATION
            </span>
            <span className="font-mono text-xs font-bold text-teal-200 mt-1 truncate">
              {activePoint.equation}
            </span>
          </div>
        </div>

        {/* Detailed Description */}
        <p className="text-xs sm:text-sm text-slate-300 leading-relaxed py-2">
          {activePoint.description}
        </p>

        {/* Hardware Specifications Bar */}
        <div className="mt-4 pt-3 border-t border-slate-800 flex items-start gap-2.5">
          <CheckCircle2 className="w-4 h-4 text-teal-400 shrink-0 mt-0.5" />
          <span className="font-mono text-xs text-slate-400">
            <strong className="text-slate-200">Hardware Spec:</strong> {activePoint.specs}
          </span>
        </div>

        {/* Subsystem Switcher Tabs */}
        <div className="mt-6 flex flex-wrap gap-2 pt-2">
          {SUBSYSTEM_POINTS.map(p => (
            <button
              key={p.id}
              onClick={() => {
                sound.click();
                setSelectedPointId(p.id);
              }}
              className={`px-3 py-1.5 rounded-lg text-xs font-mono font-semibold transition-all cursor-pointer flex items-center gap-1.5 ${
                p.id === selectedPointId 
                  ? 'bg-teal-600 text-white shadow-lg shadow-teal-700/40' 
                  : 'bg-slate-800 text-slate-400 hover:bg-slate-700 hover:text-white'
              }`}
            >
              <span>{p.label}</span>
              <ChevronRight className="w-3 h-3" />
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};
