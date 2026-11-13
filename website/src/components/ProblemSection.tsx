import React, { useState } from 'react';
import { 
  AlertTriangle, 
  Sliders, 
  ThermometerSnowflake,
  TrendingUp,
  ShieldAlert
} from 'lucide-react';
import { sound } from '../utils/soundEffects';

interface ProblemSectionProps {
  isSlideMode?: boolean;
}

export const ProblemSection: React.FC<ProblemSectionProps> = ({ isSlideMode = false }) => {
  const [scrubHour, setScrubHour] = useState<number>(45);

  const totalReserveKJ = 1046.4;
  const ingressRateW = 4.41;
  const energyConsumedKJ = scrubHour * ingressRateW * 3.6;
  const remainingReservePercent = Math.max(0, Math.min(100, 100 - (energyConsumedKJ / totalReserveKJ) * 100));

  let simulatedTemp = 3.2;
  if (scrubHour <= 10) {
    simulatedTemp = 3.2 + (scrubHour / 10) * 1.3;
  } else if (scrubHour <= 68) {
    simulatedTemp = 4.5 + ((scrubHour - 10) / 58) * 1.2;
  } else if (scrubHour <= 72) {
    simulatedTemp = 5.7 + ((scrubHour - 68) / 4) * 2.3;
  } else {
    simulatedTemp = 8.0 + ((scrubHour - 72) / 12) * 8.5;
  }

  const isBreached = simulatedTemp > 8.0;

  return (
    <div className={`w-full bg-[#08111E]/95 rounded-2xl border border-slate-800 shadow-2xl backdrop-blur-xl text-white ${
      isSlideMode ? 'p-5' : 'p-6 md:p-10'
    }`}>
      
      {/* Chapter Tag & Main Headline */}
      <div className="max-w-3xl">
        <div className="flex items-center gap-2">
          <span className="px-2.5 py-0.5 rounded text-[11px] font-mono uppercase bg-amber-950/80 text-amber-300 border border-amber-500/40 font-bold">
            Chapter 02 • The Cold-Chain Challenge
          </span>
          <span className="text-xs font-mono text-slate-400">
            WHO Last-Mile Logistical Crisis
          </span>
        </div>
        <h2 className={`font-serif-display font-bold text-white mt-2 leading-tight ${
          isSlideMode ? 'text-2xl sm:text-3xl' : 'text-3xl sm:text-4xl md:text-5xl'
        }`}>
          When cooling ends, the problem begins.
        </h2>
        <p className="text-slate-300 text-xs sm:text-sm mt-2 leading-relaxed">
          Maintaining vaccines strictly between <strong>+2.0°C and +8.0°C</strong> is essential for potency. The World Health Organization (WHO) estimates that up to <strong>50% of vaccines are compromised globally</strong> during off-grid transit in developing regions.
        </p>
      </div>

      {/* The 72-Hour Planning Baseline Box */}
      <div className="mt-5 p-4 rounded-xl bg-slate-900/90 border border-slate-800 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <span className="text-xs font-mono text-teal-400 font-bold uppercase tracking-wider block">
            CONVENTIONAL PASSIVE PLANNING BASELINE
          </span>
          <div className="flex items-baseline gap-2 mt-0.5">
            <span className="text-3xl sm:text-4xl font-mono font-bold text-white">72 Hours</span>
            <span className="text-xs font-mono text-slate-400">(≈ 3 Days Under Tropical Stress)</span>
          </div>
          <p className="text-xs text-slate-300 mt-1 max-w-xl">
            <strong className="text-teal-300">Methodological Clarification:</strong> This 72-hour figure is the conventional passive PCM planning reference, not a universal industry ceiling. It provides zero contingency margin during logistical delays or extreme heat pulses.
          </p>
        </div>

        <div className="bg-amber-950/60 border border-amber-500/40 p-3.5 rounded-xl text-xs text-amber-200 max-w-xs shadow-lg">
          <div className="font-bold flex items-center gap-1.5 text-amber-400 font-mono">
            <AlertTriangle className="w-4 h-4 text-amber-400" />
            THE PASSIVE THERMAL TRAP
          </div>
          <p className="mt-1 text-[11px] leading-relaxed text-slate-300">
            Latent heat storage is finite (Q = mL). As ambient heat enters, the phase-change reserve depletes monotonically (Q_latent → 0), culminating in rapid thermal runaway.
          </p>
        </div>
      </div>

      {/* Interactive Conventional PCM Depletion Simulator */}
      <div className="mt-5 bg-slate-900/80 rounded-xl p-4 sm:p-5 border border-slate-800">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-3 border-b border-slate-800 gap-2">
          <div>
            <h4 className="font-mono text-xs font-bold uppercase text-white flex items-center gap-2">
              <Sliders className="w-4 h-4 text-teal-400" />
              Time Scrubber: Conventional Passive PCM Exhaustion
            </h4>
            <span className="text-[11px] text-slate-400">
              Drag timeline to observe latent reserve depletion and temperature breach
            </span>
          </div>

          <div className="flex items-center gap-2 font-mono text-xs">
            <span className="text-slate-400">Elapsed:</span>
            <span className="text-xl font-bold text-teal-300">{scrubHour} h</span>
          </div>
        </div>

        {/* Timeline Scrubber */}
        <div className="mt-4">
          <input
            type="range"
            min="0"
            max="85"
            step="1"
            value={scrubHour}
            onChange={e => { setScrubHour(parseInt(e.target.value)); sound.click(); }}
            className="w-full h-2 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-teal-400"
          />
          <div className="flex justify-between text-[11px] font-mono text-slate-400 mt-1">
            <span>0 h (Deploy)</span>
            <span>24 h (Day 1)</span>
            <span>48 h (Day 2)</span>
            <span className="text-amber-400 font-bold">72 h (Baseline Limit)</span>
            <span className="text-rose-400 font-bold">85 h (Breach)</span>
          </div>
        </div>

        {/* Live Gauges Row */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3.5 mt-4">
          
          {/* Latent Reserve Gauge */}
          <div className="p-3.5 rounded-xl bg-slate-950/80 border border-slate-800 shadow-md">
            <div className="flex items-center justify-between text-xs font-mono text-slate-400">
              <span>PCM LATENT RESERVE</span>
              <ThermometerSnowflake className="w-4 h-4 text-teal-400" />
            </div>
            <div className="mt-1 flex items-baseline gap-2">
              <span className={`text-2xl sm:text-3xl font-mono font-bold ${
                remainingReservePercent > 25 ? 'text-teal-300' : 'text-amber-400 animate-pulse'
              }`}>
                {remainingReservePercent.toFixed(0)}%
              </span>
              <span className="text-xs font-mono text-slate-400">
                ({(1046.4 * (remainingReservePercent / 100)).toFixed(0)} kJ left)
              </span>
            </div>
            <div className="w-full h-2 bg-slate-800 rounded-full mt-2.5 overflow-hidden">
              <div 
                className={`h-full transition-all duration-200 ${
                  remainingReservePercent > 30 ? 'bg-teal-500' : remainingReservePercent > 10 ? 'bg-amber-500' : 'bg-rose-500'
                }`}
                style={{ width: `${remainingReservePercent}%` }}
              />
            </div>
            <span className="text-[10px] font-mono text-slate-400 block mt-1.5">
              {remainingReservePercent > 0 ? 'Absorbing latent heat at ~4.4 W' : 'Fully melted: 0 kJ latent buffering left'}
            </span>
          </div>

          {/* Chamber Temperature Gauge */}
          <div className={`p-3.5 rounded-xl border transition-all ${
            isBreached ? 'bg-rose-950/80 border-rose-500/60 shadow-lg' : 'bg-slate-950/80 border-slate-800 shadow-md'
          }`}>
            <div className="flex items-center justify-between text-xs font-mono text-slate-400">
              <span>INTERNAL TEMPERATURE</span>
              <TrendingUp className={`w-4 h-4 ${isBreached ? 'text-rose-400' : 'text-teal-400'}`} />
            </div>
            <div className="mt-1 flex items-baseline gap-2">
              <span className={`text-2xl sm:text-3xl font-mono font-bold ${
                isBreached ? 'text-rose-400' : 'text-emerald-400'
              }`}>
                +{simulatedTemp.toFixed(1)}°C
              </span>
              <span className="text-xs font-mono text-slate-400">
                {isBreached ? '(CRITICAL EXCURSION)' : '(Safe Zone)'}
              </span>
            </div>
            <div className="w-full h-2 bg-slate-800 rounded-full mt-2.5 overflow-hidden">
              <div 
                className={`h-full transition-all duration-200 ${
                  isBreached ? 'bg-rose-500' : 'bg-emerald-500'
                }`}
                style={{ width: `${Math.min(100, (simulatedTemp / 16.0) * 100)}%` }}
              />
            </div>
            <span className="text-[10px] font-mono text-slate-400 block mt-1.5">
              Critical Upper Threshold: +8.0°C (WHO Standard)
            </span>
          </div>

          {/* Clinical Risk Summary */}
          <div className="p-3.5 rounded-xl bg-slate-950/80 border border-slate-800 shadow-md flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between text-xs font-mono text-slate-400">
                <span>CLINICAL STATUS</span>
                <ShieldAlert className={`w-4 h-4 ${isBreached ? 'text-rose-400' : 'text-emerald-400'}`} />
              </div>
              <div className="mt-1">
                {isBreached ? (
                  <span className="px-2 py-0.5 rounded text-xs font-mono font-bold bg-rose-600 text-white animate-pulse inline-block shadow-md">
                    VACCINES COMPROMISED
                  </span>
                ) : (
                  <span className="px-2 py-0.5 rounded text-xs font-mono font-bold bg-emerald-950 text-emerald-300 border border-emerald-500/40 inline-block">
                    POTENCY PRESERVED
                  </span>
                )}
              </div>
              <p className="text-[11px] text-slate-300 mt-1.5 leading-tight">
                {isBreached 
                  ? 'Excursion past +8.0°C risks protein denaturation in hepatitis B and mRNA biologics, rendering doses unusable.'
                  : 'Bio-PCM maintains temperature stability within safe +2.0°C to +8.0°C boundaries.'}
              </p>
            </div>
            <span className="text-[10px] font-mono text-slate-500 mt-1">
              *Fourier heat ingress simulation
            </span>
          </div>

        </div>
      </div>

      {/* The Central Question Leading into SANJIVANI */}
      <div className="mt-6 p-5 rounded-xl bg-teal-950/60 border border-teal-500/40 text-center shadow-lg">
        <span className="text-xs font-mono text-teal-400 uppercase tracking-widest block font-bold">
          THE FUNDAMENTAL RESEARCH QUESTION
        </span>
        <h3 className="font-serif-display text-xl sm:text-2xl text-white font-bold mt-1 max-w-3xl mx-auto leading-snug">
          “Can we intelligently extend the useful thermal reserve instead of relying on passive cooling alone?”
        </h3>
        <p className="text-xs text-slate-300 mt-1 max-w-2xl mx-auto">
          Instead of making the box heavier with more PCM or draining huge batteries with continuous refrigeration, SANJIVANI engineers sensor-triggered thermoelectric intervention.
        </p>
      </div>

    </div>
  );
};
