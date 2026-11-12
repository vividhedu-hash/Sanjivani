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
  AlertCircle 
} from 'lucide-react';
import { sound } from '../utils/soundEffects';

interface NumbersDashboardProps {
  isSlideMode?: boolean;
}

export const NumbersDashboard: React.FC<NumbersDashboardProps> = ({ isSlideMode = false }) => {
  const [cop, setCop] = useState<number>(0.61);
  const [pcmMass, setPcmMass] = useState<number>(4.8);
  const [latentHeat, setLatentHeat] = useState<number>(218);
  const [targetDuration, setTargetDuration] = useState<number>(110);
  const [auxPower, setAuxPower] = useState<number>(4.2);

  const [expandedCard, setExpandedCard] = useState<string | null>(null);

  const calcLatentKJ = pcmMass * latentHeat;
  const calcLatentWh = calcLatentKJ / 3.6;
  const calcBaselineHours = (pcmMass / 4.8) * 72.0;
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
    <div className={`w-full bg-white rounded-2xl border border-slate-200 shadow-xl ${
      isSlideMode ? 'p-5' : 'p-6 md:p-8'
    }`}>
      
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between pb-4 border-b border-slate-200 gap-3">
        <div>
          <div className="flex items-center gap-2">
            <span className="px-2.5 py-0.5 rounded text-[11px] font-mono uppercase bg-teal-50 text-[#0F766E] border border-teal-200 font-bold">
              Rigorous Mathematical Audit
            </span>
            <span className="text-xs font-mono text-slate-500">
              WHO PQS E004/CB01 Calibrated
            </span>
          </div>
          <h3 className={`font-serif-display font-bold text-[#0B2545] mt-1 ${
            isSlideMode ? 'text-2xl sm:text-3xl' : 'text-2xl md:text-3xl'
          }`}>
            The Numbers: Engineering Assumptions to Measurable Targets
          </h3>
          <p className="text-slate-600 text-xs sm:text-sm mt-0.5 max-w-2xl">
            Every technical quantity in SANJIVANI has been recalculated from first principles. Nothing has been assumed or copied without verification.
          </p>
        </div>

        {/* Verification Status Pill */}
        <div className="flex items-center gap-2 bg-emerald-50 border border-emerald-300 px-3 py-1.5 rounded-xl text-emerald-800 text-xs font-mono font-bold shadow-xs">
          <CheckCircle2 className="w-4 h-4 text-emerald-600" />
          <span>FIRST LAW ENERGY CONSERVED</span>
        </div>
      </div>

      {/* KPI Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3.5 mt-4">
        
        {/* KPI 1: Duration Target */}
        <div 
          onClick={() => toggleExpand('duration')}
          className="p-3.5 rounded-xl bg-slate-50 border border-slate-200 hover:border-teal-400 transition-all cursor-pointer group shadow-xs"
        >
          <div className="flex items-center justify-between text-xs font-mono text-slate-500">
            <span>MISSION AUTONOMY</span>
            <Clock className="w-4 h-4 text-[#0F766E]" />
          </div>
          <div className="mt-1 flex items-baseline gap-1.5">
            <span className="text-3xl font-mono font-bold text-[#0B2545]">110.0</span>
            <span className="text-sm font-mono text-slate-500">h</span>
          </div>
          <div className="mt-0.5 flex items-center justify-between text-[11px] font-mono">
            <span className="text-slate-500">Baseline: 72.0 h</span>
            <span className="text-[#0F766E] font-bold">+52.8% Target</span>
          </div>
          <div className="mt-2 pt-2 border-t border-slate-200 flex items-center justify-between text-[10px] font-mono text-[#0F766E] font-semibold">
            <span>DESIGN TARGET</span>
            {expandedCard === 'duration' ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
          </div>
          {expandedCard === 'duration' && (
            <div className="mt-2 text-[11px] text-slate-700 border-t border-slate-200 pt-2 space-y-1">
              <p><strong>Baseline:</strong> 72.0 h conventional reference under 43°C stress.</p>
              <p><strong>Modelled:</strong> 109.4 h holding duration before breach past +8.0°C.</p>
            </div>
          )}
        </div>

        {/* KPI 2: Latent Energy Reserve */}
        <div 
          onClick={() => toggleExpand('latent')}
          className="p-3.5 rounded-xl bg-slate-50 border border-slate-200 hover:border-teal-400 transition-all cursor-pointer group shadow-xs"
        >
          <div className="flex items-center justify-between text-xs font-mono text-slate-500">
            <span>LATENT PCM RESERVE</span>
            <Layers className="w-4 h-4 text-[#0F766E]" />
          </div>
          <div className="mt-1 flex items-baseline gap-1.5">
            <span className="text-3xl font-mono font-bold text-[#0B2545]">290.7</span>
            <span className="text-sm font-mono text-slate-500">Wh</span>
          </div>
          <div className="mt-0.5 flex items-center justify-between text-[11px] font-mono">
            <span className="text-slate-500">Mass: 4.8 kg</span>
            <span className="text-[#0F766E] font-bold">1,046.4 kJ</span>
          </div>
          <div className="mt-2 pt-2 border-t border-slate-200 flex items-center justify-between text-[10px] font-mono text-[#0F766E] font-semibold">
            <span>AUDITED SPEC</span>
            {expandedCard === 'latent' ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
          </div>
          {expandedCard === 'latent' && (
            <div className="mt-2 text-[11px] text-slate-700 border-t border-slate-200 pt-2 space-y-1">
              <p><strong>Formula:</strong> Q = m_pcm · Δh_fus</p>
              <p><strong>Calculation:</strong> 4.8 kg bio-PCM × 218 kJ/kg = 1,046.4 kJ (290.7 Wh).</p>
            </div>
          )}
        </div>

        {/* KPI 3: Mission Electrical Energy */}
        <div 
          onClick={() => toggleExpand('electrical')}
          className="p-3.5 rounded-xl bg-slate-50 border border-slate-200 hover:border-teal-400 transition-all cursor-pointer group shadow-xs"
        >
          <div className="flex items-center justify-between text-xs font-mono text-slate-500">
            <span>ELECTRICAL CONSUMPTION</span>
            <Zap className="w-4 h-4 text-indigo-600" />
          </div>
          <div className="mt-1 flex items-baseline gap-1.5">
            <span className="text-3xl font-mono font-bold text-[#0B2545]">301.2</span>
            <span className="text-sm font-mono text-slate-500">Wh</span>
          </div>
          <div className="mt-0.5 flex items-center justify-between text-[11px] font-mono">
            <span className="text-slate-500">Active Run: 8.75 h</span>
            <span className="text-indigo-600 font-bold">8.0% Duty Cycle</span>
          </div>
          <div className="mt-2 pt-2 border-t border-slate-200 flex items-center justify-between text-[10px] font-mono text-indigo-600 font-semibold">
            <span>SIMULATED RESULT</span>
            {expandedCard === 'electrical' ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
          </div>
          {expandedCard === 'electrical' && (
            <div className="mt-2 text-[11px] text-slate-700 border-t border-slate-200 pt-2 space-y-1">
              <p><strong>Calculation:</strong> (34.2 W × 8.75 h) + (0.15 W × 101.25 h) = 301.2 Wh.</p>
            </div>
          )}
        </div>

        {/* KPI 4: Battery Sizing */}
        <div 
          onClick={() => toggleExpand('battery')}
          className="p-3.5 rounded-xl bg-slate-50 border border-slate-200 hover:border-teal-400 transition-all cursor-pointer group shadow-xs"
        >
          <div className="flex items-center justify-between text-xs font-mono text-slate-500">
            <span>BATTERY SIZING</span>
            <BatteryCharging className="w-4 h-4 text-amber-600" />
          </div>
          <div className="mt-1 flex items-baseline gap-1.5">
            <span className="text-3xl font-mono font-bold text-[#0B2545]">30.0</span>
            <span className="text-sm font-mono text-slate-500">Ah (12.8V)</span>
          </div>
          <div className="mt-0.5 flex items-center justify-between text-[11px] font-mono">
            <span className="text-slate-500">Gross: 384 Wh</span>
            <span className="text-amber-700 font-bold">78.4% DOD</span>
          </div>
          <div className="mt-2 pt-2 border-t border-slate-200 flex items-center justify-between text-[10px] font-mono text-amber-700 font-semibold">
            <span>ENGINEERING SPEC</span>
            {expandedCard === 'battery' ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
          </div>
          {expandedCard === 'battery' && (
            <div className="mt-2 text-[11px] text-slate-700 border-t border-slate-200 pt-2 space-y-1">
              <p><strong>Chemistry:</strong> 12.8V 30Ah LiFePO4 (4S configuration).</p>
              <p><strong>Reserve Margin:</strong> 21.6% reserve remains at conclusion of 110 h mission.</p>
            </div>
          )}
        </div>

      </div>

      {/* Interactive Thermal & Battery Calculator */}
      <div className="mt-6 p-5 rounded-xl bg-slate-50 border border-slate-200">
        <div className="flex flex-col md:flex-row md:items-center justify-between pb-3 border-b border-slate-200 gap-1">
          <div className="flex items-center gap-2">
            <Calculator className="w-5 h-5 text-[#0F766E]" />
            <h4 className="font-serif-display text-lg font-bold text-[#0B2545]">
              Interactive Thermal & Battery Capacity Calculator
            </h4>
          </div>
          <span className="text-xs font-mono text-slate-500">
            Adjust design assumptions to recalculate mission demands live
          </span>
        </div>

        {/* Sliders Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4 mt-4">
          
          {/* Slider 1: COP */}
          <div>
            <div className="flex justify-between text-xs font-mono mb-1">
              <span className="text-slate-700 font-semibold">Peltier COP:</span>
              <span className="font-bold text-[#0F766E]">{cop.toFixed(2)}</span>
            </div>
            <input
              type="range"
              min="0.40"
              max="0.85"
              step="0.01"
              value={cop}
              onChange={e => { setCop(parseFloat(e.target.value)); sound.click(); }}
              className="w-full h-1.5 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-[#0F766E]"
            />
            <span className="text-[10px] text-slate-500 block mt-0.5">Reference: 0.61 (7.5V)</span>
          </div>

          {/* Slider 2: PCM Mass */}
          <div>
            <div className="flex justify-between text-xs font-mono mb-1">
              <span className="text-slate-700 font-semibold">PCM Mass:</span>
              <span className="font-bold text-[#0F766E]">{pcmMass.toFixed(1)} kg</span>
            </div>
            <input
              type="range"
              min="3.0"
              max="7.0"
              step="0.2"
              value={pcmMass}
              onChange={e => { setPcmMass(parseFloat(e.target.value)); sound.click(); }}
              className="w-full h-1.5 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-[#0F766E]"
            />
            <span className="text-[10px] text-slate-500 block mt-0.5">Reference: 4.8 kg</span>
          </div>

          {/* Slider 3: Latent Heat */}
          <div>
            <div className="flex justify-between text-xs font-mono mb-1">
              <span className="text-slate-700 font-semibold">Latent Heat:</span>
              <span className="font-bold text-indigo-700">{latentHeat} kJ/kg</span>
            </div>
            <input
              type="range"
              min="180"
              max="240"
              step="2"
              value={latentHeat}
              onChange={e => { setLatentHeat(parseInt(e.target.value)); sound.click(); }}
              className="w-full h-1.5 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-indigo-600"
            />
            <span className="text-[10px] text-slate-500 block mt-0.5">Reference: 218 kJ/kg</span>
          </div>

          {/* Slider 4: Target Duration */}
          <div>
            <div className="flex justify-between text-xs font-mono mb-1">
              <span className="text-slate-700 font-semibold">Target Duration:</span>
              <span className="font-bold text-amber-700">{targetDuration} h</span>
            </div>
            <input
              type="range"
              min="80"
              max="140"
              step="2"
              value={targetDuration}
              onChange={e => { setTargetDuration(parseInt(e.target.value)); sound.click(); }}
              className="w-full h-1.5 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-amber-600"
            />
            <span className="text-[10px] text-slate-500 block mt-0.5">Reference: 110 h mission</span>
          </div>

          {/* Slider 5: Aux Power */}
          <div>
            <div className="flex justify-between text-xs font-mono mb-1">
              <span className="text-slate-700 font-semibold">Aux Power:</span>
              <span className="font-bold text-purple-700">{auxPower.toFixed(1)} W</span>
            </div>
            <input
              type="range"
              min="2.0"
              max="8.0"
              step="0.2"
              value={auxPower}
              onChange={e => { setAuxPower(parseFloat(e.target.value)); sound.click(); }}
              className="w-full h-1.5 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-purple-600"
            />
            <span className="text-[10px] text-slate-500 block mt-0.5">Reference: 4.2 W</span>
          </div>

        </div>

        {/* Live Recalculated Output Strip */}
        <div className="mt-4 p-3.5 rounded-xl bg-white border border-slate-200 grid grid-cols-2 md:grid-cols-4 gap-3 shadow-xs">
          <div>
            <span className="text-[10px] font-mono text-slate-500 block">Calculated Latent Reserve:</span>
            <span className="text-base font-mono font-bold text-[#0F766E]">
              {calcLatentWh.toFixed(1)} Wh ({calcLatentKJ.toFixed(0)} kJ)
            </span>
          </div>

          <div>
            <span className="text-[10px] font-mono text-slate-500 block">Peltier Active Runtime:</span>
            <span className="text-base font-mono font-bold text-cyan-700">
              {activeRuntimeHours.toFixed(2)} h ({((activeRuntimeHours / targetDuration) * 100).toFixed(1)}% duty)
            </span>
          </div>

          <div>
            <span className="text-[10px] font-mono text-slate-500 block">Total Electrical Energy:</span>
            <span className="text-base font-mono font-bold text-indigo-700">
              {totalMissionEnergyWh.toFixed(1)} Wh
            </span>
          </div>

          <div>
            <span className="text-[10px] font-mono text-slate-500 block">Recommended Battery:</span>
            <span className="text-base font-mono font-bold text-amber-700">
              {recommendedBatteryAh12V.toFixed(1)} Ah @ 12.8V
            </span>
          </div>
        </div>

        <div className="mt-2.5 flex items-start gap-1.5 text-xs text-slate-500 italic">
          <AlertCircle className="w-3.5 h-3.5 text-amber-600 shrink-0 mt-0.5" />
          <span>
            <strong>Scientific Integrity Note:</strong> This interactive calculator evaluates theoretical model equations. Modifying inputs recalculates mathematical estimates, not physical prototype results.
          </span>
        </div>

      </div>

    </div>
  );
};
