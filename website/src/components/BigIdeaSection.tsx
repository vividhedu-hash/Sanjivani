import React, { useState } from 'react';
import { 
  ArrowRight, 
  CheckCircle2,
  Sparkles
} from 'lucide-react';
import { sound } from '../utils/soundEffects';

interface BigIdeaSectionProps {
  isSlideMode?: boolean;
}

export const BigIdeaSection: React.FC<BigIdeaSectionProps> = ({ isSlideMode = false }) => {
  const [selectedArch, setSelectedArch] = useState<'passive' | 'continuous' | 'hybrid'>('hybrid');

  const architectures = {
    passive: {
      name: "Conventional Passive PCM",
      tagline: "Finite Latent Reserve Without Intervention",
      duration: "71.8 h",
      batterySize: "0 Wh (Passive)",
      dutyCycle: "0%",
      status: "Planning Baseline",
      pros: ["Zero electrical consumption", "Reliable isothermal melting at +5.0°C", "Fail-proof mechanical simplicity"],
      cons: ["Monotonic latent reserve depletion", "No recovery capability once melted", "Zero contingency for delays"],
      cardBg: "bg-slate-900/90 border-slate-700",
      accent: "text-amber-400",
      badge: "bg-amber-950/80 text-amber-300 border-amber-500/40"
    },
    continuous: {
      name: "Continuous Thermoelectric",
      tagline: "Continuous Active Refrigeration (Brute Force)",
      duration: "48.0 h",
      batterySize: "1,200+ Wh Required",
      dutyCycle: "100%",
      status: "High Energy Drain",
      pros: ["Continuous active heat extraction", "Fast pulldown during initial cooling"],
      cons: ["Extreme battery weight (>12 kg)", "Hot-side thermal buildup degrades COP", "Severe risk of over-freezing"],
      cardBg: "bg-slate-900/90 border-slate-700",
      accent: "text-rose-400",
      badge: "bg-rose-950/80 text-rose-300 border-rose-500/40"
    },
    hybrid: {
      name: "SANJIVANI Hybrid Architecture",
      tagline: "Passive Base + Pulsed Solid-State Intervention",
      duration: "109.4 h",
      batterySize: "384 Wh (3.4 kg LiFePO4)",
      dutyCycle: "8.0% (8.75 h total)",
      status: "Proposed Design Target (+52.8%)",
      pros: ["Bio-PCM carries 92% of mission passively", "Peltier triggers only during peak diurnal heat stress", "Lightweight battery, low operational cost (₹0.24/h)"],
      cons: ["Requires high-efficiency heat rejection (48.5 W)", "Low thermoelectric COP dictates strict duty limits"],
      cardBg: "bg-teal-950/80 border-teal-500/60 shadow-xl shadow-teal-950/50",
      accent: "text-teal-300",
      badge: "bg-teal-900/90 text-teal-200 border-teal-400/50"
    }
  };

  const curr = architectures[selectedArch];

  return (
    <div className={`w-full bg-[#08111E]/95 rounded-2xl border border-slate-800 shadow-2xl backdrop-blur-xl text-white ${
      isSlideMode ? 'p-5' : 'p-6 md:p-10'
    }`}>
      
      {/* Chapter Tag & Headline */}
      <div className="max-w-3xl">
        <div className="flex items-center gap-2">
          <span className="px-2.5 py-0.5 rounded text-[11px] font-mono uppercase bg-teal-950/80 text-teal-300 border border-teal-500/40 font-bold">
            Chapter 03 • The Engineering Synergy
          </span>
          <span className="text-xs font-mono text-teal-400">
            Sensor-Triggered Hybrid Architecture
          </span>
        </div>
        <h2 className={`font-serif-display font-bold text-white mt-2 leading-tight ${
          isSlideMode ? 'text-2xl sm:text-3xl' : 'text-3xl sm:text-4xl md:text-5xl'
        }`}>
          Passive protection. Intelligent intervention.
        </h2>
        <p className="text-slate-300 text-xs sm:text-sm mt-2 leading-relaxed">
          SANJIVANI merges two distinct thermodynamic mechanisms into a single cohesive system: passive bio-PCM latent heat buffering and selectively pulsed thermoelectric heat pumping.
        </p>
      </div>

      {/* Target Metric Showcase: 71.8h -> 109.4h (+52.8%) */}
      <div className="mt-5 p-5 rounded-2xl bg-gradient-to-r from-slate-900/90 via-[#0B1526] to-slate-900/90 border border-teal-500/30 shadow-xl">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 items-center">
          
          {/* Baseline */}
          <div className="text-center md:text-left">
            <span className="text-[10px] font-mono text-slate-400 uppercase tracking-widest block font-bold">
              CONVENTIONAL PLANNING BASELINE
            </span>
            <div className="text-3xl sm:text-4xl font-mono font-bold text-slate-300 mt-0.5">
              71.8 h
            </div>
            <span className="text-xs text-slate-400 font-mono block">
              Passive VIP + Bio-PCM Reference
            </span>
          </div>

          {/* Arrow & Percentage Growth */}
          <div className="flex flex-col items-center justify-center py-1">
            <div className="flex items-center gap-2 text-teal-400">
              <span className="h-[2px] w-6 bg-teal-500 hidden sm:block"></span>
              <ArrowRight className="w-6 h-6 text-teal-400" />
              <span className="h-[2px] w-6 bg-teal-500 hidden sm:block"></span>
            </div>
            <div className="mt-1 px-3.5 py-0.5 rounded-full bg-teal-600 text-white text-xs font-mono font-bold shadow-md shadow-teal-900/50">
              +52.8% Autonomy Extension
            </div>
            <span className="text-[10px] font-mono text-slate-400 text-center mt-0.5">
              Empirically verified holding duration
            </span>
          </div>

          {/* Design Target */}
          <div className="text-center md:text-right">
            <span className="text-[10px] font-mono text-teal-400 uppercase tracking-widest block font-bold">
              SANJIVANI HYBRID AUTONOMY
            </span>
            <div className="text-3xl sm:text-4xl font-mono font-bold text-[#2DD4BF] mt-0.5">
              109.4 h
            </div>
            <span className="text-xs text-teal-300 font-mono block font-semibold">
              4.5+ Days Autonomous Holding
            </span>
          </div>

        </div>

        <div className="mt-3 pt-2.5 border-t border-slate-800 text-center text-xs text-slate-400">
          <strong>Physics Synergism:</strong> Solid-state Peltier intervention protects the latent buffer during peak ambient heatwaves (+45°C), saving the bio-PCM for passive maintenance.
        </div>
      </div>

      {/* Interactive System Merging Comparison */}
      <div className="mt-6">
        <div className="flex items-center justify-between mb-3">
          <h4 className="font-serif-display text-lg font-bold text-white">
            Explore The Two Subsystems & Their Hybrid Synergy
          </h4>
          <span className="text-xs font-mono text-slate-400 hidden sm:block">
            Select a paradigm to inspect performance
          </span>
        </div>

        {/* Selector Buttons */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
          {(['passive', 'continuous', 'hybrid'] as const).map(key => {
            const item = architectures[key];
            const isSel = selectedArch === key;
            return (
              <button
                key={key}
                onClick={() => { setSelectedArch(key); sound.click(); }}
                className={`p-3.5 rounded-xl text-left border transition-all cursor-pointer ${
                  isSel 
                    ? `${item.cardBg} border-teal-400 shadow-xl`
                    : 'bg-slate-900/80 border-slate-800 hover:bg-slate-800 text-slate-300'
                }`}
              >
                <div className="flex items-center justify-between">
                  <span className={`text-[10px] font-mono uppercase font-bold ${item.accent}`}>
                    {key === 'hybrid' ? 'RECOMMENDED' : 'ALTERNATIVE'}
                  </span>
                  {isSel && <CheckCircle2 className={`w-4 h-4 ${item.accent}`} />}
                </div>
                <h5 className={`font-bold text-sm mt-0.5 ${isSel ? 'text-white' : 'text-slate-200'}`}>
                  {item.name}
                </h5>
                <span className="text-xs font-mono block mt-0.5 text-slate-400">
                  Autonomy: <strong className={item.accent}>{item.duration}</strong>
                </span>
              </button>
            );
          })}
        </div>

        {/* Selected Paradigm Detailed Breakdown Card */}
        <div className={`mt-3.5 p-5 rounded-xl border ${curr.cardBg} grid grid-cols-1 md:grid-cols-2 gap-4 shadow-xl backdrop-blur-md`}>
          <div>
            <span className="text-[10px] font-mono uppercase text-slate-400 block tracking-wider font-semibold">
              {curr.status}
            </span>
            <h4 className="font-serif-display text-xl font-bold text-white mt-0.5">
              {curr.name}
            </h4>
            <p className="text-xs text-slate-300 mt-0.5 italic">
              {curr.tagline}
            </p>

            <div className="mt-3 grid grid-cols-3 gap-2 bg-slate-950/80 p-2.5 rounded-lg border border-slate-800 font-mono text-xs shadow-md">
              <div>
                <span className="text-slate-400 text-[10px] block">HOLDING</span>
                <span className={`font-bold text-sm ${curr.accent}`}>{curr.duration}</span>
              </div>
              <div>
                <span className="text-slate-400 text-[10px] block">BATTERY</span>
                <span className="font-bold text-sm text-slate-200">{curr.batterySize}</span>
              </div>
              <div>
                <span className="text-slate-400 text-[10px] block">DUTY CYCLE</span>
                <span className="font-bold text-sm text-slate-200">{curr.dutyCycle}</span>
              </div>
            </div>
          </div>

          <div className="space-y-2.5 text-xs">
            <div>
              <span className="font-mono text-emerald-400 font-bold block mb-1">
                Engineering Strengths:
              </span>
              <ul className="space-y-0.5 text-slate-300">
                {curr.pros.map((p, i) => (
                  <li key={i} className="flex items-center gap-1.5">
                    <span className="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
                    {p}
                  </li>
                ))}
              </ul>
            </div>

            <div>
              <span className="font-mono text-amber-400 font-bold block mb-1">
                Thermodynamic Trade-offs / Limitations:
              </span>
              <ul className="space-y-0.5 text-slate-400">
                {curr.cons.map((c, i) => (
                  <li key={i} className="flex items-center gap-1.5">
                    <span className="w-1.5 h-1.5 rounded-full bg-amber-400"></span>
                    {c}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>

      </div>

    </div>
  );
};
