import React, { useState } from 'react';
import { 
  ArrowRight, 
  CheckCircle2
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
      duration: "72.0 h",
      batterySize: "0 Wh (Passive)",
      dutyCycle: "0%",
      status: "Planning Baseline",
      pros: ["Zero electrical consumption", "Reliable isothermal melting at 5.0°C", "Fail-proof simplicity"],
      cons: ["Monotonic latent reserve depletion", "No recovery capability once melted", "Zero contingency for delays"],
      cardBg: "bg-white border-amber-300",
      accent: "text-amber-800",
      badge: "bg-amber-100 text-amber-900 border-amber-300"
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
      cardBg: "bg-white border-rose-300",
      accent: "text-rose-800",
      badge: "bg-rose-100 text-rose-900 border-rose-300"
    },
    hybrid: {
      name: "SANJIVANI Hybrid Architecture",
      tagline: "Passive Base + Pulsed Solid-State Intervention",
      duration: "110.0 h",
      batterySize: "384 Wh (3.4 kg LiFePO4)",
      dutyCycle: "8.0% (8.75 h total)",
      status: "Proposed Design Target (+52.8%)",
      pros: ["Bio-PCM carries 92% of mission passively", "Peltier triggers only during peak diurnal heat stress", "Lightweight battery, low operational cost (₹0.24/h)"],
      cons: ["Requires high-efficiency heat rejection (48.5 W)", "Low thermoelectric COP dictates strict duty limits"],
      cardBg: "bg-teal-50/80 border-teal-500",
      accent: "text-[#0F766E]",
      badge: "bg-teal-100 text-[#0F766E] border-teal-300"
    }
  };

  const curr = architectures[selectedArch];

  return (
    <div className={`w-full bg-white rounded-2xl border border-slate-200 shadow-xl ${
      isSlideMode ? 'p-5' : 'p-6 md:p-10'
    }`}>
      
      {/* Chapter Tag & Headline */}
      <div className="max-w-3xl">
        <div className="flex items-center gap-2">
          <span className="px-2.5 py-0.5 rounded text-[11px] font-mono uppercase bg-teal-50 text-[#0F766E] border border-teal-200 font-bold">
            Chapter 03 • The Engineering Synergy
          </span>
          <span className="text-xs font-mono text-slate-500">
            Sensor-Triggered Hybrid Architecture
          </span>
        </div>
        <h2 className={`font-serif-display font-bold text-[#0B2545] mt-1.5 leading-tight ${
          isSlideMode ? 'text-2xl sm:text-3xl' : 'text-3xl sm:text-4xl md:text-5xl'
        }`}>
          Passive protection. Intelligent intervention.
        </h2>
        <p className="text-slate-600 text-xs sm:text-sm mt-2 leading-relaxed">
          SANJIVANI merges two distinct thermodynamic mechanisms into a single cohesive system: passive bio-PCM latent heat buffering and selectively pulsed thermoelectric heat pumping.
        </p>
      </div>

      {/* Target Metric Showcase: 72h -> 110h (+52.8%) */}
      <div className="mt-5 p-5 rounded-2xl bg-gradient-to-r from-teal-50/60 via-slate-50 to-teal-50/60 border border-teal-200 shadow-sm">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 items-center">
          
          {/* Baseline */}
          <div className="text-center md:text-left">
            <span className="text-[10px] font-mono text-slate-500 uppercase tracking-widest block font-bold">
              CONVENTIONAL PLANNING BASELINE
            </span>
            <div className="text-3xl sm:text-4xl font-mono font-bold text-slate-700 mt-0.5">
              72 h
            </div>
            <span className="text-xs text-slate-500 font-mono block">
              Passive VIP + Bio-PCM Reference
            </span>
          </div>

          {/* Arrow & Percentage Growth */}
          <div className="flex flex-col items-center justify-center py-1">
            <div className="flex items-center gap-2 text-[#0F766E]">
              <span className="h-[2px] w-6 bg-[#0F766E] hidden sm:block"></span>
              <ArrowRight className="w-6 h-6 text-[#0F766E]" />
              <span className="h-[2px] w-6 bg-[#0F766E] hidden sm:block"></span>
            </div>
            <div className="mt-1 px-3.5 py-0.5 rounded-full bg-[#0F766E] text-white text-xs font-mono font-bold shadow-sm">
              +52.8% Target Extension
            </div>
            <span className="text-[10px] font-mono text-slate-500 text-center mt-0.5">
              Proposed relative to 72h baseline
            </span>
          </div>

          {/* Design Target */}
          <div className="text-center md:text-right">
            <span className="text-[10px] font-mono text-[#0F766E] uppercase tracking-widest block font-bold">
              SANJIVANI EXTENDED DESIGN TARGET
            </span>
            <div className="text-3xl sm:text-4xl font-mono font-bold text-[#0B2545] mt-0.5">
              110 h
            </div>
            <span className="text-xs text-[#0F766E] font-mono block font-semibold">
              4.5+ Days Autonomous Holding Target
            </span>
          </div>

        </div>

        <div className="mt-3 pt-2.5 border-t border-slate-200 text-center text-xs text-slate-500">
          <strong>Engineering Integrity Disclosure:</strong> The +52.8% extension (72 h → 110 h) represents the project's numerical design target under simulated diurnal thermal stress, not a certified or experimentally verified metric.
        </div>
      </div>

      {/* Interactive System Merging Comparison */}
      <div className="mt-6">
        <div className="flex items-center justify-between mb-3">
          <h4 className="font-serif-display text-lg font-bold text-[#0B2545]">
            Explore The Two Subsystems & Their Hybrid Synergy
          </h4>
          <span className="text-xs font-mono text-slate-500 hidden sm:block">
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
                    ? `${item.cardBg} shadow-md`
                    : 'bg-slate-50 border-slate-200 hover:bg-slate-100 text-slate-600'
                }`}
              >
                <div className="flex items-center justify-between">
                  <span className={`text-[10px] font-mono uppercase font-bold ${item.accent}`}>
                    {key === 'hybrid' ? 'RECOMMENDED' : 'ALTERNATIVE'}
                  </span>
                  {isSel && <CheckCircle2 className={`w-4 h-4 ${item.accent}`} />}
                </div>
                <h5 className={`font-bold text-sm mt-0.5 ${isSel ? 'text-[#0B2545]' : 'text-slate-800'}`}>
                  {item.name}
                </h5>
                <span className="text-xs font-mono block mt-0.5 text-slate-600">
                  Autonomy: <strong className={item.accent}>{item.duration}</strong>
                </span>
              </button>
            );
          })}
        </div>

        {/* Selected Paradigm Detailed Breakdown Card */}
        <div className={`mt-3.5 p-5 rounded-xl border ${curr.cardBg} grid grid-cols-1 md:grid-cols-2 gap-4 shadow-sm`}>
          <div>
            <span className="text-[10px] font-mono uppercase text-slate-500 block tracking-wider font-semibold">
              {curr.status}
            </span>
            <h4 className="font-serif-display text-xl font-bold text-[#0B2545] mt-0.5">
              {curr.name}
            </h4>
            <p className="text-xs text-slate-600 mt-0.5 italic">
              {curr.tagline}
            </p>

            <div className="mt-3 grid grid-cols-3 gap-2 bg-white p-2.5 rounded-lg border border-slate-200 font-mono text-xs shadow-xs">
              <div>
                <span className="text-slate-500 text-[10px] block">HOLDING</span>
                <span className={`font-bold text-sm ${curr.accent}`}>{curr.duration}</span>
              </div>
              <div>
                <span className="text-slate-500 text-[10px] block">BATTERY</span>
                <span className="font-bold text-sm text-slate-800">{curr.batterySize}</span>
              </div>
              <div>
                <span className="text-slate-500 text-[10px] block">DUTY CYCLE</span>
                <span className="font-bold text-sm text-slate-800">{curr.dutyCycle}</span>
              </div>
            </div>
          </div>

          <div className="space-y-2.5 text-xs">
            <div>
              <span className="font-mono text-emerald-700 font-bold block mb-1">
                Engineering Strengths:
              </span>
              <ul className="space-y-0.5 text-slate-700">
                {curr.pros.map((p, i) => (
                  <li key={i} className="flex items-center gap-1.5">
                    <span className="w-1.5 h-1.5 rounded-full bg-emerald-600"></span>
                    {p}
                  </li>
                ))}
              </ul>
            </div>

            <div>
              <span className="font-mono text-amber-800 font-bold block mb-1">
                Thermodynamic Trade-offs / Limitations:
              </span>
              <ul className="space-y-0.5 text-slate-600">
                {curr.cons.map((c, i) => (
                  <li key={i} className="flex items-center gap-1.5">
                    <span className="w-1.5 h-1.5 rounded-full bg-amber-500"></span>
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
