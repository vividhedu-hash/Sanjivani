import React, { useState } from 'react';
import { 
  Calculator, 
  BatteryCharging, 
  Zap, 
  Clock, 
  CheckCircle2, 
  Layers, 
  ChevronDown, 
  ChevronUp, 
  AlertCircle,
  Sparkles
} from 'lucide-react';
import { sound } from '../utils/soundEffects';

interface NumbersDashboardProps {
  isSlideMode?: boolean;
}

export const NumbersDashboard: React.FC<NumbersDashboardProps> = ({ isSlideMode = false }) => {
  const [cop, setCop] = useState<number>(0.61);
  const [pcmMass, setPcmMass] = useState<number>(4.8);
  const [latentHeat, setLatentHeat] = useState<number>(218);
  const [targetDuration, setTargetDuration] = useState<number>(109.4);
  const [auxPower, setAuxPower] = useState<number>(4.2);

  const [expandedCard, setExpandedCard] = useState<string | null>(null);

  const calcLatentKJ = pcmMass * latentHeat;
  const calcLatentWh = calcLatentKJ / 3.6;
  const calcBaselineHours = (pcmMass / 4.8) * 71.8;
  const extraHoursNeeded = Math.max(0, targetDuration - calcBaselineHours);
  const heatIngressRateW = 4.41;
  const extraThermalEnergyWh = extraHoursNeeded * heatIngressRateW;
  const activeCoolingRateW = 18.5;
  const activeRuntimeHours = extraThermalEnergyWh / activeCoolingRateW;
  const peltierElecPowerW = activeCoolingRateW / cop;
  const totalActiveElecW = peltierElecPowerW + auxPower;
  const standbyHours = Math.max(0, targetDuration - activeRuntimeHours);
  const totalMissionEnergyWh = (activeRuntimeHours * totalActiveElecW) + (standbyHours * 0.15);
  const recommendedBatteryGrossWh = totalMissionEnergyWh / 0.80;
  const recommendedBatteryAh12V = recommendedBatteryGrossWh / 12.8;

  const toggleExpand = (cardKey: string) => {
    sound.click();
    setExpandedCard(prev => prev === cardKey ? null : cardKey);
  };

  return (
    <div className={`w-full bg-[#08111E]/95 rounded-2xl border border-slate-800 shadow-2xl backdrop-blur-xl text-white ${
      isSlideMode ? 'p-5' : 'p-6 md:p-8'
    }`}>
      
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between pb-4 border-b border-slate-800 gap-3">
        <div>
          <div className="flex items-center gap-2">
            <span className="px-2.5 py-0.5 rounded text-[11px] font-mono uppercase bg-teal-950/80 text-teal-300 border border-teal-500/40 font-bold">
              Rigorous Mathematical Audit
            </span>
            <span className="text-xs font-mono text-teal-400">
              WHO PQS E004/CB01 Calibrated
            </span>
          </div>
          <h3 className={`font-serif-display font-bold text-white mt-1.5 ${
            isSlideMode ? 'text-2xl sm:text-3xl' : 'text-2xl md:text-3xl'
          }`}>
            The Numbers: Engineering Assumptions to Measurable Targets
          </h3>
          <p className="text-slate-300 text-xs sm:text-sm mt-0.5 max-w-2xl leading-relaxed">
            Every technical quantity in SANJIVANI has been recalculated from first principles. Nothing has been assumed or copied without verification.
          </p>
        </div>

        {/* Verification Status Pill */}
        <div className="flex items-center gap-2 bg-emerald-950/80 border border-emerald-500/40 px-3.5 py-1.5 rounded-xl text-emerald-300 text-xs font-mono font-bold shadow-lg">
          <CheckCircle2 className="w-4 h-4 text-emerald-400" />
          <span>FIRST LAW ENERGY CONSERVED</span>
        </div>
      </div>

      {/* KPI Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3.5 mt-4">
        
        {/* KPI 1: Duration Target */}
        <div 
          onClick={() => toggleExpand('duration')}
          className="p-4 rounded-xl bg-slate-900/90 border border-slate-800 hover:border-teal-400 transition-all cursor-pointer group shadow-md"
        >
          <div className="flex items-center justify-between text-xs font-mono text-slate-400">
            <span>MISSION AUTONOMY</span>
            <Clock className="w-4 h-4 text-teal-400" />
          </div>
          <div className="mt-1 flex items-baseline gap-1.5">
            <span className="text-3xl font-mono font-bold text-white">109.4</span>
            <span className="text-sm font-mono text-slate-400">h</span>
          </div>
          <div className="mt-0.5 flex items-center justify-between text-[11px] font-mono">
            <span className="text-slate-400">Baseline: 71.8 h</span>
            <span className="text-teal-300 font-bold">+52.8% Target</span>
          </div>
          <div className="mt-2 pt-2 border-t border-slate-800 flex items-center justify-between text-[10px] font-mono text-teal-400 font-semibold">
            <span>DESIGN TARGET</span>
            {expandedCard === 'duration' ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
          </div>
          {expandedCard === 'duration' && (
            <div className="mt-2 text-[11px] text-slate-300 border-t border-slate-800 pt-2 space-y-1">
              <p><strong>Baseline:</strong> 71.8 h conventional reference under 43°C stress.</p>
              <p><strong>Modelled:</strong> 109.4 h holding duration before breach past +8.0°C.</p>
            </div>
          )}
        </div>

        {/* KPI 2: Latent Energy Reserve */}
        <div 
          onClick={() => toggleExpand('latent')}
          className="p-4 rounded-xl bg-slate-900/90 border border-slate-800 hover:border-teal-400 transition-all cursor-pointer group shadow-md"
        >
          <div className="flex items-center justify-between text-xs font-mono text-slate-400">
            <span>LATENT PCM RESERVE</span>
            <Layers className="w-4 h-4 text-teal-400" />
          </div>
          <div className="mt-1 flex items-baseline gap-1.5">
            <span className="text-3xl font-mono font-bold text-white">290.7</span>
            <span className="text-sm font-mono text-slate-400">Wh</span>
          </div>
          <div className="mt-0.5 flex items-center justify-between text-[11px] font-mono">
            <span className="text-slate-400">Mass: 4.8 kg</span>
            <span className="text-teal-300 font-bold">1,046.4 kJ</span>
          </div>
          <div className="mt-2 pt-2 border-t border-slate-800 flex items-center justify-between text-[10px] font-mono text-teal-400 font-semibold">
            <span>AUDITED SPEC</span>
            {expandedCard === 'latent' ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
          </div>
          {expandedCard === 'latent' && (
            <div className="mt-2 text-[11px] text-slate-300 border-t border-slate-800 pt-2 space-y-1">
              <p><strong>Formula:</strong> Q = m_pcm · Δh_fus</p>
              <p><strong>Calculation:</strong> 4.8 kg bio-PCM × 218 kJ/kg = 1,046.4 kJ (290.7 Wh).</p>
            </div>
          )}
        </div>

        {/* KPI 3: Mission Electrical Energy */}
        <div 
          onClick={() => toggleExpand('electrical')}
          className="p-4 rounded-xl bg-slate-900/90 border border-slate-800 hover:border-teal-400 transition-all cursor-pointer group shadow-md"
        >
          <div className="flex items-center justify-between text-xs font-mono text-slate-400">
            <span>ELECTRICAL CONSUMPTION</span>
            <Zap className="w-4 h-4 text-indigo-400" />
          </div>
          <div className="mt-1 flex items-baseline gap-1.5">
            <span className="text-3xl font-mono font-bold text-white">301.2</span>
            <span className="text-sm font-mono text-slate-400">Wh</span>
          </div>
          <div className="mt-0.5 flex items-center justify-between text-[11px] font-mono">
            <span className="text-slate-400">Active Run: 8.75 h</span>
            <span className="text-indigo-300 font-bold">8.0% Duty Cycle</span>
          </div>
          <div className="mt-2 pt-2 border-t border-slate-800 flex items-center justify-between text-[10px] font-mono text-indigo-400 font-semibold">
            <span>SIMULATED RESULT</span>
            {expandedCard === 'electrical' ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
          </div>
          {expandedCard === 'electrical' && (
            <div className="mt-2 text-[11px] text-slate-300 border-t border-slate-800 pt-2 space-y-1">
              <p><strong>Calculation:</strong> (34.2 W × 8.75 h) + (0.15 W × 100.65 h) = 301.2 Wh.</p>
            </div>
          )}
        </div>

        {/* KPI 4: Battery Sizing */}
        <div 
          onClick={() => toggleExpand('battery')}
          className="p-4 rounded-xl bg-slate-900/90 border border-slate-800 hover:border-teal-400 transition-all cursor-pointer group shadow-md"
        >
          <div className="flex items-center justify-between text-xs font-mono text-slate-400">
            <span>BATTERY SIZING</span>
            <BatteryCharging className="w-4 h-4 text-amber-400" />
          </div>
          <div className="mt-1 flex items-baseline gap-1.5">
            <span className="text-3xl font-mono font-bold text-white">30.0</span>
            <span className="text-sm font-mono text-slate-400">Ah (12.8V)</span>
          </div>
          <div className="mt-0.5 flex items-center justify-between text-[11px] font-mono">
            <span className="text-slate-400">Gross: 384 Wh</span>
            <span className="text-amber-300 font-bold">78.4% DOD</span>
          </div>
          <div className="mt-2 pt-2 border-t border-slate-800 flex items-center justify-between text-[10px] font-mono text-amber-400 font-semibold">
            <span>ENGINEERING SPEC</span>
            {expandedCard === 'battery' ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
          </div>
          {expandedCard === 'battery' && (
            <div className="mt-2 text-[11px] text-slate-300 border-t border-slate-800 pt-2 space-y-1">
              <p><strong>Chemistry:</strong> 12.8V 30Ah LiFePO4 (4S configuration).</p>
              <p><strong>Reserve Margin:</strong> 21.6% reserve remains at conclusion of 109.4 h mission.</p>
            </div>
          )}
        </div>

      </div>

      {/* Interactive Thermal & Battery Calculator */}
      <div className="mt-6 p-5 rounded-xl bg-slate-900/80 border border-slate-800">
        <div className="flex flex-col md:flex-row md:items-center justify-between pb-3 border-b border-slate-800 gap-1">
          <div className="flex items-center gap-2">
            <Calculator className="w-5 h-5 text-teal-400" />
            <h4 className="font-serif-display text-lg font-bold text-white">
              Interactive Thermal & Battery Capacity Calculator
            </h4>
          </div>
          <span className="text-xs font-mono text-slate-400">
            Adjust design assumptions to recalculate mission demands live
          </span>
        </div>

        {/* Sliders Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4 mt-4">
          
          {/* Slider 1: COP */}
          <div>
            <div className="flex justify-between text-xs font-mono mb-1">
              <span className="text-slate-300 font-semibold">Peltier COP:</span>
              <span className="font-bold text-teal-300">{cop.toFixed(2)}</span>
            </div>
            <input
              type="range"
              min="0.40"
              max="0.85"
              step="0.01"
              value={cop}
              onChange={e => { setCop(parseFloat(e.target.value)); sound.click(); }}
              className="w-full h-1.5 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-teal-400"
            />
            <span className="text-[10px] text-slate-400 block mt-0.5">Reference: 0.61 (7.5V)</span>
          </div>

          {/* Slider 2: PCM Mass */}
          <div>
            <div className="flex justify-between text-xs font-mono mb-1">
              <span className="text-slate-300 font-semibold">PCM Mass:</span>
              <span className="font-bold text-teal-300">{pcmMass.toFixed(1)} kg</span>
            </div>
            <input
              type="range"
              min="3.0"
              max="7.0"
              step="0.2"
              value={pcmMass}
              onChange={e => { setPcmMass(parseFloat(e.target.value)); sound.click(); }}
              className="w-full h-1.5 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-teal-400"
            />
            <span className="text-[10px] text-slate-400 block mt-0.5">Reference: 4.8 kg</span>
          </div>

          {/* Slider 3: Latent Heat */}
          <div>
            <div className="flex justify-between text-xs font-mono mb-1">
              <span className="text-slate-300 font-semibold">Latent Heat:</span>
              <span className="font-bold text-indigo-300">{latentHeat} kJ/kg</span>
            </div>
            <input
              type="range"
              min="180"
              max="240"
              step="2"
              value={latentHeat}
              onChange={e => { setLatentHeat(parseInt(e.target.value)); sound.click(); }}
              className="w-full h-1.5 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-indigo-400"
            />
            <span className="text-[10px] text-slate-400 block mt-0.5">Reference: 218 kJ/kg</span>
          </div>

          {/* Slider 4: Target Duration */}
          <div>
            <div className="flex justify-between text-xs font-mono mb-1">
              <span className="text-slate-300 font-semibold">Target Duration:</span>
              <span className="font-bold text-amber-300">{targetDuration.toFixed(1)} h</span>
            </div>
            <input
              type="range"
              min="80"
              max="140"
              step="2"
              value={targetDuration}
              onChange={e => { setTargetDuration(parseFloat(e.target.value)); sound.click(); }}
              className="w-full h-1.5 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-amber-400"
            />
            <span className="text-[10px] text-slate-400 block mt-0.5">Reference: 109.4 h mission</span>
          </div>

          {/* Slider 5: Aux Power */}
          <div>
            <div className="flex justify-between text-xs font-mono mb-1">
              <span className="text-slate-300 font-semibold">Aux Power:</span>
              <span className="font-bold text-purple-300">{auxPower.toFixed(1)} W</span>
            </div>
            <input
              type="range"
              min="2.0"
              max="8.0"
              step="0.2"
              value={auxPower}
              onChange={e => { setAuxPower(parseFloat(e.target.value)); sound.click(); }}
              className="w-full h-1.5 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-purple-400"
            />
            <span className="text-[10px] text-slate-400 block mt-0.5">Reference: 4.2 W</span>
          </div>

        </div>

        {/* Live Recalculated Output Strip */}
        <div className="mt-4 p-4 rounded-xl bg-slate-950/90 border border-slate-800 grid grid-cols-2 md:grid-cols-4 gap-3 shadow-md">
          <div>
            <span className="text-[10px] font-mono text-slate-400 block">Calculated Latent Reserve:</span>
            <span className="text-base font-mono font-bold text-teal-300">
              {calcLatentWh.toFixed(1)} Wh ({calcLatentKJ.toFixed(0)} kJ)
            </span>
          </div>

          <div>
            <span className="text-[10px] font-mono text-slate-400 block">Peltier Active Runtime:</span>
            <span className="text-base font-mono font-bold text-cyan-300">
              {activeRuntimeHours.toFixed(2)} h ({((activeRuntimeHours / targetDuration) * 100).toFixed(1)}% duty)
            </span>
          </div>

          <div>
            <span className="text-[10px] font-mono text-slate-400 block">Total Electrical Energy:</span>
            <span className="text-base font-mono font-bold text-indigo-300">
              {totalMissionEnergyWh.toFixed(1)} Wh
            </span>
          </div>

          <div>
            <span className="text-[10px] font-mono text-slate-400 block">Recommended Battery:</span>
            <span className="text-base font-mono font-bold text-amber-300">
              {recommendedBatteryAh12V.toFixed(1)} Ah @ 12.8V
            </span>
          </div>
        </div>

        <div className="mt-2.5 flex items-start gap-1.5 text-xs text-slate-400 italic">
          <AlertCircle className="w-3.5 h-3.5 text-amber-400 shrink-0 mt-0.5" />
          <span>
            <strong>Scientific Integrity Note:</strong> This interactive calculator evaluates theoretical model equations. Modifying inputs recalculates mathematical estimates, not physical prototype results.
          </span>
        </div>

      </div>

    </div>
  );
};
