import React, { useState } from 'react';
import { 
  HeartPulse, 
  IndianRupee, 
  ShieldCheck, 
  AlertTriangle, 
  TrendingUp, 
  Package, 
  Sliders, 
  Info
} from 'lucide-react';
import { sound } from '../utils/soundEffects';

interface ImpactSectionProps {
  isSlideMode?: boolean;
}

export const ImpactSection: React.FC<ImpactSectionProps> = ({ isSlideMode = false }) => {
  // Scenario Simulator Inputs
  const [payloadValue, setPayloadValue] = useState<number>(150000); // INR 1.5 Lakhs
  const [tripsPerYear, setTripsPerYear] = useState<number>(24); // 24 rural missions/year
  const [excursionRisk, setExcursionRisk] = useState<number>(15); // 15% risk in remote transit
  const [spoilageAvoided, setSpoilageAvoided] = useState<number>(75); // 75% hypothetical avoidance

  // Illustrative Value Protected Calculation
  const totalExposureINR = tripsPerYear * payloadValue;
  const potentialSpoiledINR = totalExposureINR * (excursionRisk / 100);
  const illustrativeProtectedINR = potentialSpoiledINR * (spoilageAvoided / 100);

  return (
    <div className={`w-full bg-white rounded-2xl border border-slate-200 shadow-xl ${
      isSlideMode ? 'p-4 md:p-6' : 'p-6 md:p-10'
    }`}>
      
      {/* Chapter Tag & Headline */}
      <div className="max-w-3xl">
        <div className="flex items-center gap-2">
          <span className="px-2.5 py-0.5 rounded text-[11px] font-mono uppercase bg-emerald-50 text-emerald-800 border border-emerald-200 font-bold">
            Chapter 08 • Techno-Economic & Healthcare Value
          </span>
          <span className="text-xs font-mono text-slate-500">
            STEM for Atmanirbhar Bharat
          </span>
        </div>
        <h2 className={`font-serif-display font-bold text-[#0B2545] mt-1.5 leading-tight ${
          isSlideMode ? 'text-2xl sm:text-3xl' : 'text-3xl sm:text-4xl md:text-5xl'
        }`}>
          The value of keeping medical supplies usable.
        </h2>
        <p className="text-slate-600 text-xs sm:text-sm mt-1.5 leading-relaxed">
          In rural primary health centres (PHCs) and off-grid disaster corridors, cold-chain failure is not merely a financial loss—it directly risks patient outcomes and compromises immunization coverage.
        </p>
      </div>

      {/* The Cascading Clinical Wastage Journey */}
      <div className={`rounded-xl bg-slate-50 border border-slate-200 ${
        isSlideMode ? 'mt-4 p-4' : 'mt-6 p-5 sm:p-6'
      }`}>
        <span className="text-xs font-mono text-slate-500 uppercase tracking-widest block mb-3 font-semibold">
          The Vulnerability Cascade: From Thermal Fluctuation to Health Consequences
        </span>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
          
          <div className="p-3.5 rounded-xl bg-white border border-slate-200 shadow-sm">
            <span className="text-[10px] font-mono text-slate-500 uppercase font-bold block">STEP 01</span>
            <h5 className="font-bold text-[#0B2545] text-sm mt-0.5">Temperature Instability</h5>
            <p className="text-[11px] text-slate-600 mt-1 leading-snug">
              Transit delays or extreme ambient heat cause chamber temperature to breach +8.0°C.
            </p>
          </div>

          <div className="p-3.5 rounded-xl bg-amber-50/60 border border-amber-200 shadow-sm">
            <span className="text-[10px] font-mono text-amber-800 uppercase font-bold block">STEP 02</span>
            <h5 className="font-bold text-amber-900 text-sm mt-0.5">Product Quality Risk</h5>
            <p className="text-[11px] text-slate-600 mt-1 leading-snug">
              Heat disrupts protein structure in hepatitis B, rabies, and mRNA vaccines, reducing efficacy.
            </p>
          </div>

          <div className="p-3.5 rounded-xl bg-rose-50/60 border border-rose-200 shadow-sm">
            <span className="text-[10px] font-mono text-rose-800 uppercase font-bold block">STEP 03</span>
            <h5 className="font-bold text-rose-900 text-sm mt-0.5">Potential Spoilage</h5>
            <p className="text-[11px] text-slate-600 mt-1 leading-snug">
              Vials must be discarded or, if administered without cold-chain integrity, fail to confer immunity.
            </p>
          </div>

          <div className="p-3.5 rounded-xl bg-teal-50/60 border border-teal-200 shadow-sm">
            <span className="text-[10px] font-mono text-[#0F766E] uppercase font-bold block">SANJIVANI IMPACT</span>
            <h5 className="font-bold text-[#0B2545] text-sm mt-0.5">Extended Margin</h5>
            <p className="text-[11px] text-slate-600 mt-1 leading-snug">
              Adds +38 hours of contingency hold, giving field health workers critical buffer during crises.
            </p>
          </div>

        </div>

        <div className="mt-3 pt-2 border-t border-slate-200 text-[11px] text-slate-500 text-center italic">
          *SANJIVANI is engineered as an attempt to reduce the risk of medical spoilage, not as a certified or proven waste-elimination guarantee.
        </div>
      </div>

      {/* Bill of Materials & Cost Architecture */}
      <div className={isSlideMode ? 'mt-4' : 'mt-6'}>
        <h3 className="font-serif-display text-lg sm:text-xl font-bold text-[#0B2545] mb-3">
          Audited Prototype Cost Framework (Indian Procurement in INR)
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          
          {/* MVP Tier Card */}
          <div className="p-4 rounded-xl bg-white border border-slate-200 shadow-sm">
            <div className="flex items-center justify-between">
              <span className="text-[10px] font-mono text-slate-600 uppercase tracking-wider font-bold">
                TIER 1 • MINIMUM VIABLE PROTOTYPE
              </span>
              <span className="text-xs font-mono text-slate-500 font-semibold">Benchtop Validated</span>
            </div>
            <div className="mt-1.5 flex items-baseline gap-1.5">
              <span className="text-2xl sm:text-3xl font-mono font-bold text-[#0B2545]">₹ 6,480</span>
              <span className="text-xs font-mono text-slate-500">Total CapEx</span>
            </div>
            <p className="text-xs text-slate-600 mt-1.5 leading-snug">
              Air-cooled architecture with external 12V DC auxiliary vehicle / solar plug-in input, 4.8 kg bio-PCM, and basic MOSFET switching.
            </p>
            <div className="mt-2.5 pt-2 border-t border-slate-100 text-[11px] font-mono text-slate-600 space-y-1">
              <div className="flex justify-between"><span>Bio-PCM & Insulated Shell:</span><span className="font-bold text-slate-800">₹ 3,450</span></div>
              <div className="flex justify-between"><span>Dual TEC + Fin Sink + Fans:</span><span className="font-bold text-slate-800">₹ 1,780</span></div>
              <div className="flex justify-between"><span>ESP32 & Sensors:</span><span className="font-bold text-slate-800">₹ 1,250</span></div>
            </div>
          </div>

          {/* Autonomous Field Unit Tier Card */}
          <div className="p-4 rounded-xl bg-teal-50/50 border border-teal-300 shadow-md">
            <div className="flex items-center justify-between">
              <span className="text-[10px] font-mono text-[#0F766E] uppercase tracking-wider font-bold">
                TIER 2 • FULLY AUTONOMOUS FIELD UNIT
              </span>
              <span className="text-xs font-mono text-[#0F766E] font-bold">Field Ready Target</span>
            </div>
            <div className="mt-1.5 flex items-baseline gap-1.5">
              <span className="text-2xl sm:text-3xl font-mono font-bold text-[#0B2545]">₹ 11,850</span>
              <span className="text-xs font-mono text-slate-500">Total CapEx</span>
            </div>
            <p className="text-xs text-slate-700 mt-1.5 leading-snug">
              Complete standalone logistics unit equipped with integrated 12.8V 30Ah LiFePO4 battery pack, smart BMS, micro-pump loop, and OLED telemetry.
            </p>
            <div className="mt-2.5 pt-2 border-t border-teal-200/60 text-[11px] font-mono text-slate-700 space-y-1">
              <div className="flex justify-between"><span>12.8V 30Ah LiFePO4 Battery & BMS:</span><span className="text-[#0B2545] font-bold">₹ 3,450 (29.1%)</span></div>
              <div className="flex justify-between"><span>Medical VIP + PUF Composite Shell:</span><span className="text-[#0B2545] font-bold">₹ 2,850 (24.1%)</span></div>
              <div className="flex justify-between"><span>Dual TEC, Heatsink & Fans:</span><span className="text-[#0B2545] font-bold">₹ 1,780 (15.0%)</span></div>
            </div>
          </div>

        </div>

        {/* Operating Cost Highlight */}
        <div className="mt-3 p-3.5 rounded-xl bg-emerald-50 border border-emerald-200 flex flex-col sm:flex-row items-center justify-between gap-2.5 text-xs font-mono text-emerald-950">
          <div className="flex items-center gap-2">
            <IndianRupee className="w-4 h-4 text-[#0F766E]" />
            <span>OPERATING COST: <strong className="text-[#0F766E] font-bold">₹ 0.24 / operating hour</strong></span>
          </div>
          <div className="text-slate-600">
            Complete 110-hour mission grid electrical recharge: <strong className="text-[#0B2545]">₹ 8.80 (at ₹8.00 / kWh)</strong>
          </div>
        </div>
      </div>

      {/* Interactive Illustrative Healthcare Value Protection Simulator */}
      <div className={`rounded-xl bg-slate-50 border border-slate-200 ${
        isSlideMode ? 'mt-4 p-4' : 'mt-6 p-5 sm:p-6'
      }`}>
        <div className="flex flex-col md:flex-row md:items-center justify-between pb-3 border-b border-slate-200 gap-1.5">
          <div className="flex items-center gap-2">
            <Sliders className="w-4 h-4 text-[#0F766E]" />
            <h4 className="font-serif-display text-base sm:text-lg font-bold text-[#0B2545]">
              Hypothetical Healthcare Value Protection Simulator
            </h4>
          </div>
          <span className="text-xs font-mono text-slate-500">
            Scenario exploration for rural healthcare logistics
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mt-4">
          
          {/* Slider 1: Payload Value */}
          <div>
            <div className="flex justify-between text-xs font-mono mb-1">
              <span className="text-slate-600">Payload Value / Trip:</span>
              <span className="font-bold text-[#0F766E]">₹ {(payloadValue / 1000).toFixed(0)}k</span>
            </div>
            <input
              type="range"
              min="25000"
              max="500000"
              step="5000"
              value={payloadValue}
              onChange={e => { setPayloadValue(parseInt(e.target.value)); sound.click(); }}
              className="w-full h-1.5 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-[#0F766E]"
            />
            <span className="text-[10px] text-slate-500 block mt-1">
              e.g. 24 vials rabies / antivenom
            </span>
          </div>

          {/* Slider 2: Trips Per Year */}
          <div>
            <div className="flex justify-between text-xs font-mono mb-1">
              <span className="text-slate-600">Trips / Year:</span>
              <span className="font-bold text-sky-700">{tripsPerYear} missions</span>
            </div>
            <input
              type="range"
              min="6"
              max="60"
              step="2"
              value={tripsPerYear}
              onChange={e => { setTripsPerYear(parseInt(e.target.value)); sound.click(); }}
              className="w-full h-1.5 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-sky-600"
            />
            <span className="text-[10px] text-slate-500 block mt-1">
              District outreach frequency
            </span>
          </div>

          {/* Slider 3: Excursion Risk */}
          <div>
            <div className="flex justify-between text-xs font-mono mb-1">
              <span className="text-slate-600">Remote Excursion Risk:</span>
              <span className="font-bold text-amber-700">{excursionRisk}%</span>
            </div>
            <input
              type="range"
              min="5"
              max="35"
              step="1"
              value={excursionRisk}
              onChange={e => { setExcursionRisk(parseInt(e.target.value)); sound.click(); }}
              className="w-full h-1.5 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-amber-600"
            />
            <span className="text-[10px] text-slate-500 block mt-1">
              Logistical transit delay risk
            </span>
          </div>

          {/* Slider 4: Spoilage Avoided */}
          <div>
            <div className="flex justify-between text-xs font-mono mb-1">
              <span className="text-slate-600">Spoilage Avoided (%):</span>
              <span className="font-bold text-indigo-700">{spoilageAvoided}%</span>
            </div>
            <input
              type="range"
              min="20"
              max="90"
              step="5"
              value={spoilageAvoided}
              onChange={e => { setSpoilageAvoided(parseInt(e.target.value)); sound.click(); }}
              className="w-full h-1.5 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-indigo-600"
            />
            <span className="text-[10px] text-slate-500 block mt-1">
              Hypothetical buffer contingency
            </span>
          </div>

        </div>

        {/* Output Banner */}
        <div className="mt-4 p-3.5 rounded-xl bg-[#0B2545] text-white flex flex-col sm:flex-row items-center justify-between gap-3 shadow-md">
          <div>
            <span className="text-[10px] font-mono text-teal-200 uppercase tracking-wider block">
              ILLUSTRATIVE POTENTIAL BIOLOGIC VALUE PROTECTED:
            </span>
            <div className="text-2xl sm:text-3xl font-mono font-bold text-teal-300 mt-0.5">
              ₹ {illustrativeProtectedINR.toLocaleString('en-IN', { maximumFractionDigits: 0 })} / year
            </div>
          </div>

          <div className="text-right text-xs font-mono text-slate-300 max-w-xs">
            Annual CapEx Amortization vs Protected Value: <strong className="text-teal-300">Strong Societal ROI</strong>
          </div>
        </div>

        <div className="mt-2 text-[10px] text-slate-500 italic">
          <strong>Disclosure:</strong> Output reflects a hypothetical mathematical scenario model. It does not constitute a certified economic guarantee or validated commercial return.
        </div>

      </div>

    </div>
  );
};
