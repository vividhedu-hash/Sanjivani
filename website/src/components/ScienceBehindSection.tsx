import React, { useState } from 'react';
import { 
  Atom, 
  Flame, 
  Snowflake, 
  Zap, 
  ArrowRight
} from 'lucide-react';
import { sound } from '../utils/soundEffects';

interface ScienceBehindSectionProps {
  isSlideMode?: boolean;
}

export const ScienceBehindSection: React.FC<ScienceBehindSectionProps> = ({ isSlideMode = false }) => {
  const [activeTab, setActiveTab] = useState<'pcm' | 'peltier' | 'conduction'>('pcm');

  return (
    <div className={`w-full bg-white rounded-2xl border border-slate-200 shadow-xl ${
      isSlideMode ? 'p-4 md:p-6' : 'p-6 md:p-10'
    }`}>
      
      {/* Chapter Tag & Headline */}
      <div className="max-w-3xl">
        <div className="flex items-center gap-2">
          <span className="px-2.5 py-0.5 rounded text-[11px] font-mono uppercase bg-indigo-50 text-indigo-800 border border-indigo-200 font-bold">
            Chapter 06 • Pure Physics Principles
          </span>
          <span className="text-xs font-mono text-slate-500">
            Thermodynamic Governing Laws
          </span>
        </div>
        <h2 className={`font-serif-display font-bold text-[#0B2545] mt-1.5 leading-tight ${
          isSlideMode ? 'text-2xl sm:text-3xl' : 'text-3xl sm:text-4xl md:text-5xl'
        }`}>
          Engineering the movement of heat.
        </h2>
        <p className="text-slate-600 text-xs sm:text-sm mt-1.5 leading-relaxed">
          SANJIVANI is grounded in three classical physical phenomena: isothermal latent heat storage, solid-state thermoelectric electron energy transport, and high-conductivity Fourier conduction.
        </p>
      </div>

      {/* Interactive Physics Selector Tabs */}
      <div className={`grid grid-cols-1 sm:grid-cols-3 gap-2.5 ${isSlideMode ? 'mt-4' : 'mt-6'}`}>
        
        {/* Tab 1: PCM */}
        <button
          onClick={() => { setActiveTab('pcm'); sound.click(); }}
          className={`p-3 sm:p-4 rounded-xl text-left border transition-all cursor-pointer ${
            activeTab === 'pcm'
              ? 'bg-teal-50/80 border-[#0F766E] shadow-md text-[#0B2545]'
              : 'bg-slate-50 border-slate-200 hover:bg-slate-100 text-slate-600'
          }`}
        >
          <div className="flex items-center justify-between">
            <span className="text-[10px] font-mono text-[#0F766E] uppercase font-bold">PRINCIPLE 01</span>
            <Atom className="w-4 h-4 text-[#0F766E]" />
          </div>
          <h4 className="font-bold text-sm sm:text-base mt-1 text-[#0B2545]">Latent Heat Storage (PCM)</h4>
          <span className="text-xs font-mono text-[#0F766E] block mt-0.5 font-semibold">Q = m · L</span>
        </button>

        {/* Tab 2: Peltier */}
        <button
          onClick={() => { setActiveTab('peltier'); sound.click(); }}
          className={`p-3 sm:p-4 rounded-xl text-left border transition-all cursor-pointer ${
            activeTab === 'peltier'
              ? 'bg-indigo-50/80 border-indigo-600 shadow-md text-[#0B2545]'
              : 'bg-slate-50 border-slate-200 hover:bg-slate-100 text-slate-600'
          }`}
        >
          <div className="flex items-center justify-between">
            <span className="text-[10px] font-mono text-indigo-700 uppercase font-bold">PRINCIPLE 02</span>
            <Zap className="w-4 h-4 text-indigo-600" />
          </div>
          <h4 className="font-bold text-sm sm:text-base mt-1 text-[#0B2545]">Thermoelectric Pumping</h4>
          <span className="text-xs font-mono text-indigo-700 block mt-0.5 font-semibold">Q̇_hot = Q̇_cold + P_elec</span>
        </button>

        {/* Tab 3: Conduction */}
        <button
          onClick={() => { setActiveTab('conduction'); sound.click(); }}
          className={`p-3 sm:p-4 rounded-xl text-left border transition-all cursor-pointer ${
            activeTab === 'conduction'
              ? 'bg-sky-50/80 border-sky-600 shadow-md text-[#0B2545]'
              : 'bg-slate-50 border-slate-200 hover:bg-slate-100 text-slate-600'
          }`}
        >
          <div className="flex items-center justify-between">
            <span className="text-[10px] font-mono text-sky-700 uppercase font-bold">PRINCIPLE 03</span>
            <Snowflake className="w-4 h-4 text-sky-600" />
          </div>
          <h4 className="font-bold text-sm sm:text-base mt-1 text-[#0B2545]">Conduction & Fluid Loop</h4>
          <span className="text-xs font-mono text-sky-700 block mt-0.5 font-semibold">q = -k A (dT/dx)</span>
        </button>

      </div>

      {/* Main Physics Interactive Showcase Box */}
      <div className={`rounded-xl bg-slate-50 border border-slate-200 ${
        isSlideMode ? 'mt-4 p-4 md:p-5' : 'mt-6 p-6 md:p-8'
      }`}>
        
        {/* MODULE 1: LATENT HEAT OF FUSION */}
        {activeTab === 'pcm' && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 items-center">
            <div>
              <div className="flex items-center gap-2">
                <span className="px-2 py-0.5 rounded text-[10px] font-mono uppercase bg-teal-100 text-teal-800 border border-teal-200 font-bold">
                  Phase Change Material Physics
                </span>
                <span className="text-xs font-mono text-slate-500">CrodaTherm 5 Bio-PCM</span>
              </div>
              <h3 className="font-serif-display text-xl sm:text-2xl font-bold text-[#0B2545] mt-1.5">
                Isothermal Energy Absorption: Q = m · L
              </h3>
              <p className="text-slate-600 text-xs sm:text-sm mt-2 leading-relaxed">
                When a substance changes phase from solid to liquid, it absorbs a massive amount of thermal energy without increasing its sensible temperature. As long as solid and liquid phases coexist in equilibrium, the core remains pinned near <strong>+5.0°C</strong>.
              </p>

              <div className="mt-3.5 space-y-2 font-mono text-xs">
                <div className="bg-white p-2.5 rounded-lg border border-slate-200 flex justify-between">
                  <span className="text-slate-600">Bio-PCM Mass (m):</span>
                  <span className="text-[#0B2545] font-bold">4.8 kg (6 cassettes × 800g)</span>
                </div>
                <div className="bg-white p-2.5 rounded-lg border border-slate-200 flex justify-between">
                  <span className="text-slate-600">Specific Latent Heat (L):</span>
                  <span className="text-[#0F766E] font-bold">218 kJ/kg (CrodaTherm 5)</span>
                </div>
                <div className="bg-white p-2.5 rounded-lg border border-slate-200 flex justify-between">
                  <span className="text-slate-600">Total Latent Thermal Reserve:</span>
                  <span className="text-sky-700 font-bold">1,046.4 kJ = 290.7 Wh</span>
                </div>
              </div>
            </div>

            {/* Visual Physics Diagram: Lattice Dissolution */}
            <div className="bg-white p-5 rounded-xl border border-slate-200 flex flex-col items-center shadow-sm">
              <span className="text-xs font-mono text-slate-500 uppercase tracking-wider mb-3 font-semibold">
                Solid-to-Liquid Molecular Latent Absorption
              </span>
              
              <div className="w-full flex items-center justify-between gap-3">
                {/* Solid Crystal Lattice */}
                <div className="flex-1 bg-slate-50 p-3.5 rounded-xl border border-teal-200 text-center">
                  <span className="text-[11px] font-mono text-[#0F766E] font-bold block mb-2">SOLID (Ordered)</span>
                  <div className="grid grid-cols-4 gap-1.5 justify-items-center py-1.5">
                    {Array.from({ length: 16 }).map((_, i) => (
                      <span key={i} className="w-2.5 h-2.5 rounded-full bg-[#0F766E] shadow-sm animate-pulse" />
                    ))}
                  </div>
                  <span className="text-[10px] font-mono text-slate-500 mt-1.5 block">Bond Energy Intact</span>
                </div>

                <div className="flex flex-col items-center">
                  <span className="text-amber-700 font-mono text-xs font-bold">+ 218 kJ/kg</span>
                  <ArrowRight className="w-5 h-5 text-[#0F766E] my-1" />
                  <span className="text-[#0F766E] font-mono text-[10px] font-semibold">ΔT = 0.0°C</span>
                </div>

                {/* Liquid Fluid State */}
                <div className="flex-1 bg-slate-50 p-3.5 rounded-xl border border-sky-200 text-center">
                  <span className="text-[11px] font-mono text-sky-700 font-bold block mb-2">LIQUID (Absorbed)</span>
                  <div className="relative h-16 overflow-hidden py-1.5">
                    {Array.from({ length: 16 }).map((_, i) => (
                      <span 
                        key={i} 
                        className="w-2.5 h-2.5 rounded-full bg-sky-600 absolute"
                        style={{
                          left: `${(i % 4) * 26 + (Math.sin(i) * 12 + 6)}%`,
                          top: `${Math.floor(i / 4) * 20 + (Math.cos(i) * 6 + 4)}%`
                        }}
                      />
                    ))}
                  </div>
                  <span className="text-[10px] font-mono text-slate-500 mt-1.5 block">Latent Energy Trapped</span>
                </div>
              </div>

              <span className="text-[11px] text-slate-500 text-center mt-3 italic">
                *Internal temperature stays pinned within +2°C to +8°C until the entire 1,046.4 kJ reserve melts.
              </span>
            </div>
          </div>
        )}

        {/* MODULE 2: PELTIER EFFECT & FIRST LAW */}
        {activeTab === 'peltier' && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 items-center">
            <div>
              <div className="flex items-center gap-2">
                <span className="px-2 py-0.5 rounded text-[10px] font-mono uppercase bg-indigo-100 text-indigo-800 border border-indigo-200 font-bold">
                  Thermoelectric Energy Balance
                </span>
                <span className="text-xs font-mono text-slate-500">Dual TEC1-12706 Derated</span>
              </div>
              <h3 className="font-serif-display text-xl sm:text-2xl font-bold text-[#0B2545] mt-1.5">
                Peltier Effect & The First Law of Thermodynamics
              </h3>
              <p className="text-slate-600 text-xs sm:text-sm mt-2 leading-relaxed">
                When direct current passes through bismuth telluride (Bi₂Te₃) semiconductor pairs, electrons absorb energy transitioning from low to high potential states, chilling the cold ceramic junction and transferring heat to the opposite side.
              </p>

              {/* Crucial Equation Box */}
              <div className="mt-3.5 p-3.5 rounded-xl bg-amber-50 border border-amber-300 text-amber-900">
                <span className="text-[10px] font-mono font-bold uppercase text-amber-800 block tracking-wider">
                  MANDATORY FIRST LAW ENERGY BALANCE
                </span>
                <div className="text-lg font-mono font-bold text-[#0B2545] mt-0.5">
                  Q̇_hot = Q̇_cold + P_elec
                </div>
                <div className="text-xs font-mono text-amber-800 mt-0.5 font-bold">
                  48.5 W = 18.5 W (Cooling) + 30.0 W (Electrical Input)
                </div>
                <p className="text-[11px] text-slate-700 mt-1 leading-snug">
                  The hot side must forcibly reject both the heat pumped from the payload AND the electrical energy driving the module. Without forced dissipation, heat back-conducts, destroying the net cooling effect.
                </p>
              </div>
            </div>

            {/* Visual Semiconductor Junction Diagram */}
            <div className="bg-white p-5 rounded-xl border border-slate-200 flex flex-col items-center shadow-sm">
              <span className="text-xs font-mono text-slate-500 uppercase tracking-wider mb-2.5 font-semibold">
                Bismuth Telluride (Bi₂Te₃) p-n Semiconductor Couple
              </span>

              <div className="w-full bg-slate-50 p-3.5 rounded-xl border border-slate-200 relative text-center">
                {/* Cold Ceramic Plate Top */}
                <div className="w-full bg-cyan-700 py-1.5 rounded text-white text-xs font-mono font-bold flex items-center justify-center gap-1.5">
                  <Snowflake className="w-3.5 h-3.5 text-cyan-200" />
                  COLD JUNCTION: Q̇_cold = 18.5 W (Heat Ingress Extracted)
                </div>

                {/* Semiconductor Pellets */}
                <div className="flex justify-around my-3 px-4">
                  <div className="w-16 h-14 bg-sky-100 border border-sky-400 rounded flex flex-col items-center justify-center text-xs font-mono font-bold text-sky-900">
                    <span>N-TYPE</span>
                    <span className="text-[9px] text-sky-700">Electrons e⁻</span>
                  </div>
                  <div className="flex items-center text-slate-600 font-mono text-xs font-bold">
                    DC 7.5V • 4.0A
                  </div>
                  <div className="w-16 h-14 bg-purple-100 border border-purple-400 rounded flex flex-col items-center justify-center text-xs font-mono font-bold text-purple-900">
                    <span>P-TYPE</span>
                    <span className="text-[9px] text-purple-700">Holes h⁺</span>
                  </div>
                </div>

                {/* Hot Ceramic Plate Bottom */}
                <div className="w-full bg-amber-600 py-1.5 rounded text-white text-xs font-mono font-bold flex items-center justify-center gap-1.5">
                  <Flame className="w-3.5 h-3.5 text-amber-200" />
                  HOT JUNCTION: Q̇_hot = 48.5 W (Forced Dissipation to Air)
                </div>
              </div>

              <div className="mt-2.5 flex items-center justify-between w-full text-[10px] font-mono text-slate-500 px-1">
                <span>Derated Voltage: 7.5V</span>
                <span className="text-indigo-700 font-bold">COP ≈ 0.61 (Thermodynamic Peak)</span>
                <span>Current: 2.0A / Module</span>
              </div>
            </div>
          </div>
        )}

        {/* MODULE 3: CONDUCTION & FLUID LOOP */}
        {activeTab === 'conduction' && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 items-center">
            <div>
              <div className="flex items-center gap-2">
                <span className="px-2 py-0.5 rounded text-[10px] font-mono uppercase bg-sky-100 text-sky-800 border border-sky-200 font-bold">
                  Heat Transfer Mechanics
                </span>
                <span className="text-xs font-mono text-slate-500">6061-T6 Al & Glycol Loop</span>
              </div>
              <h3 className="font-serif-display text-xl sm:text-2xl font-bold text-[#0B2545] mt-1.5">
                Fourier Conduction & Fluid-Mediated Heat Transport
              </h3>
              <p className="text-slate-600 text-xs sm:text-sm mt-2 leading-relaxed">
                To prevent hotspots, SANJIVANI utilizes a high-diffusivity 6061-T6 aluminium spreading jacket (<span className="text-sky-700 font-mono font-bold">k = 167 W/m·K</span>) coupled to a micro-channel cold plate and closed liquid glycol loop.
              </p>

              <div className="mt-3.5 space-y-2 font-mono text-xs">
                <div className="bg-white p-2.5 rounded-lg border border-slate-200">
                  <span className="text-sky-800 font-bold block mb-0.5">1. Fourier Conduction Law:</span>
                  <span className="text-slate-600 text-[11px]">
                    q = -k · A · (dT/dx) — Distributes localized Peltier cold evenly across the entire 6.5L payload volume (internal gradient ΔT &lt; 0.6°C).
                  </span>
                </div>
                <div className="bg-white p-2.5 rounded-lg border border-slate-200">
                  <span className="text-[#0F766E] font-bold block mb-0.5">2. Closed-Circuit Glycol Convection:</span>
                  <span className="text-slate-600 text-[11px]">
                    q̇ = ṁ · c_p · ΔT — Transports heat efficiently through silicone tubing. Micro-pump cuts off during standby to decouple parasitic reverse heat conduction.
                  </span>
                </div>
              </div>
            </div>

            {/* Visual Conduction Schematic */}
            <div className="bg-white p-5 rounded-xl border border-slate-200 flex flex-col items-center shadow-sm">
              <span className="text-xs font-mono text-slate-500 uppercase tracking-wider mb-3 font-semibold">
                Thermal Spreading & Forced Heat Dissipation Flow
              </span>

              <div className="w-full space-y-2 font-mono text-xs">
                <div className="flex items-center justify-between p-2.5 rounded-lg bg-sky-50 border border-sky-200">
                  <span className="text-sky-900 font-bold">1. Payload Cavity</span>
                  <span className="text-slate-600 text-[11px]">6061-T6 Al Spreader (k = 167 W/m·K)</span>
                  <span className="text-sky-700 font-bold">+4.5°C</span>
                </div>

                <div className="flex justify-center text-slate-400 font-mono text-[10px]">↓ Fourier Conduction & Arctic MX-4 TIM</div>

                <div className="flex items-center justify-between p-2.5 rounded-lg bg-indigo-50 border border-indigo-200">
                  <span className="text-indigo-900 font-bold">2. Dual TEC1-12706</span>
                  <span className="text-slate-600 text-[11px]">Solid-State Heat Pump (30W Input)</span>
                  <span className="text-indigo-700 font-bold">Pumps 18.5W</span>
                </div>

                <div className="flex justify-center text-slate-400 font-mono text-[10px]">↓ Sintered Copper Heat Pipes (k ≈ 398 W/m·K)</div>

                <div className="flex items-center justify-between p-2.5 rounded-lg bg-amber-50 border border-amber-200">
                  <span className="text-amber-900 font-bold">3. Skived Fin Sink + Dual Fans</span>
                  <span className="text-slate-600 text-[11px]">Forced Air Convection (48.5W Total)</span>
                  <span className="text-amber-700 font-bold">Discharges to Air</span>
                </div>
              </div>

              <span className="text-[10px] font-mono text-slate-500 mt-3 text-center">
                Total System Thermal Resistance Budget: R_th_system &lt; 0.42 K/W
              </span>
            </div>
          </div>
        )}

      </div>

    </div>
  );
};
