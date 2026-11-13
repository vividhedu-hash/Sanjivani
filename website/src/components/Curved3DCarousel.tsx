import React, { useState, useEffect, useRef } from 'react';
import { ChevronLeft, ChevronRight, Compass, ShieldAlert, Thermometer, Wind, Activity } from 'lucide-react';
import { sound } from '../utils/soundEffects';

export interface DeploymentScenario {
  id: string;
  title: string;
  category: string;
  location: string;
  ambientTemp: string;
  coreTemp: string;
  stressFactor: string;
  holdingPerformance: string;
  image: string;
  description: string;
  badge: string;
}

export const DEPLOYMENT_SCENARIOS: DeploymentScenario[] = [
  {
    id: 'thar-desert',
    title: 'Thar Desert Extreme Heatwave',
    category: 'Thermal Stress Test',
    location: 'Jaisalmer / Pokhran Hinterlands, Rajasthan',
    ambientTemp: '+45.2°C Peak',
    coreTemp: '+4.1°C Safe',
    stressFactor: 'High Solar Irradiance (1,050 W/m²)',
    holdingPerformance: '42.8 Hours Validated Holdover',
    image: '/assets/photos/desert_heat.jpg',
    description: 'Under severe tropical summer ambient temperatures exceeding 45°C, Fourier heat ingress is throttled by 20mm Vacuum Insulation Panels (UA = 0.147 W/K) while the derated Peltier engine continuously rejects heat through high-density skived fins.',
    badge: '45°C PEAK HEATWAVE'
  },
  {
    id: 'himalayan-transit',
    title: 'High-Altitude Himalayan Transit',
    category: 'Sub-Zero Freeze Prevention',
    location: 'Khardung La / Changthang Plateau, Ladakh',
    ambientTemp: '-14.0°C Freeze Zone',
    coreTemp: '+3.8°C Safe',
    stressFactor: 'Cold Abuse & Hypothermic Denaturation',
    holdingPerformance: 'Zero Freeze-Damage Events',
    image: '/assets/photos/himalayan_transit.jpg',
    description: 'Conventional ice-packs freeze vaccines solid below 0°C, destroying liquid adjuvant emulsions. SANJIVANI detects temperatures dropping below +2.0°C and reverses Peltier polarity to provide precision solid-state warming.',
    badge: 'SUB-ZERO ARCTIC MISSION'
  },
  {
    id: 'monsoon-ghats',
    title: 'Western Ghats Monsoon Deluge',
    category: 'Humidity & Remote Grid Cutoff',
    location: 'Agumbe / Wayanad Rain-Belt',
    ambientTemp: '+32.0°C / 98% RH',
    coreTemp: '+4.3°C Constant',
    stressFactor: 'Flash Flooding & 72-Hour Grid Failure',
    holdingPerformance: 'IP67 Ingress Protection',
    image: '/assets/photos/monsoon_rain.jpg',
    description: 'Hermetically sealed O-ring gasket barrier and conformal coated electronics ensure complete operation during tropical monsoon downpours where bridge washouts isolate villages from regional depots.',
    badge: '98% RH RAIN CORRIDOR'
  },
  {
    id: 'rural-asha',
    title: 'Last-Mile ASHA Outreach',
    category: 'Ergonomic Field Transport',
    location: 'Tribal Hamlets, Mandla & Dindori, M.P.',
    ambientTemp: '+38.5°C Ambient',
    coreTemp: '+4.0°C Stable',
    stressFactor: '6-Hour On-Foot Walking Route',
    holdingPerformance: '5.2 kg Lightweight Payload Ergonomics',
    image: '/assets/photos/rural_clinic.jpg',
    description: 'Carried comfortably by female community health workers across unpaved footpaths. Eliminates the backbreaking 12 kg burden of melting wet-ice boxes while delivering 24 life-saving vaccine vials at peak potency.',
    badge: 'COMMUNITY LOGISTICS'
  },
  {
    id: 'solid-state-lab',
    title: 'Physics Laboratory Benchmarking',
    category: 'Scientific Empirical Testing',
    location: 'Applied Thermodynamics & Electronics Lab',
    ambientTemp: 'Controlled Chamber (+15°C to +45°C)',
    coreTemp: '±0.15°C Regulation',
    stressFactor: 'Continuous 4-Wire Digital Telemetry',
    holdingPerformance: 'COP = 0.61 Validated at 7.5V',
    image: '/assets/photos/solid_state_lab.jpg',
    description: 'Rigorous empirical verification using 4-point Dallas DS18B20 digital temperature sensors calibrated against NPL-traceable reference thermometers to validate latent PCM phase equilibrium and Seebeck heat pumping.',
    badge: 'NPL TRACEABLE RIGOR'
  },
  {
    id: 'clinical-immunization',
    title: 'Primary Health Center Immunization',
    category: 'WHO PQS E004 Safety Standard',
    location: 'Model Rural PHC Vaccination Suite',
    ambientTemp: '+34.0°C Room Ambient',
    coreTemp: '+4.2°C Golden Mean',
    stressFactor: 'Repeated Lid Openings (25 Vials Distributed)',
    holdingPerformance: '99.8% Potency Preservation',
    image: '/assets/photos/vaccine_vials.jpg',
    description: 'Preserves delicate tertiary and quaternary protein structures of measles, BCG, polio, and hepatitis B vaccines without risk of accidental freezing or thermal degradation.',
    badge: 'CLINICAL GRADE SAFETY'
  }
];

interface Curved3DCarouselProps {
  isSlideMode?: boolean;
}

export const Curved3DCarousel: React.FC<Curved3DCarouselProps> = ({ isSlideMode = false }) => {
  const [activeIndex, setActiveIndex] = useState<number>(0);
  const [isAutoPlaying, setIsAutoPlaying] = useState<boolean>(true);
  const total = DEPLOYMENT_SCENARIOS.length;
  const anglePerItem = 360 / total;
  const containerRef = useRef<HTMLDivElement>(null);

  // Auto-play interval
  useEffect(() => {
    if (!isAutoPlaying) return;
    const interval = setInterval(() => {
      setActiveIndex(prev => (prev + 1) % total);
    }, 4500);
    return () => clearInterval(interval);
  }, [isAutoPlaying, total]);

  const handlePrev = () => {
    sound.click();
    setActiveIndex(prev => (prev - 1 + total) % total);
  };

  const handleNext = () => {
    sound.click();
    setActiveIndex(prev => (prev + 1) % total);
  };

  const activeScenario = DEPLOYMENT_SCENARIOS[activeIndex];

  // Cylinder radius for 3D perspective
  const radius = isSlideMode ? 420 : 560;

  return (
    <div 
      className="relative w-full flex flex-col items-center justify-center overflow-hidden py-4 select-none"
      onMouseEnter={() => setIsAutoPlaying(false)}
      onMouseLeave={() => setIsAutoPlaying(true)}
    >
      {/* Horizon Curvature Stage */}
      <div 
        ref={containerRef}
        className={`w-full relative flex items-center justify-center ${
          isSlideMode ? 'h-[360px]' : 'h-[460px] sm:h-[500px]'
        }`}
        style={{ perspective: '1400px' }}
      >
        {/* Rotating Cylinder Hub */}
        <div 
          className="relative w-full h-full flex items-center justify-center transition-transform duration-700 ease-out"
          style={{
            transformStyle: 'preserve-3d',
            transform: `translateZ(-${radius}px) rotateY(${-activeIndex * anglePerItem}deg)`
          }}
        >
          {DEPLOYMENT_SCENARIOS.map((scenario, index) => {
            const itemAngle = index * anglePerItem;
            const isCurrent = index === activeIndex;

            return (
              <div
                key={scenario.id}
                onClick={() => {
                  sound.click();
                  setActiveIndex(index);
                }}
                className={`absolute rounded-2xl cursor-pointer overflow-hidden border transition-all duration-700 ${
                  isSlideMode 
                    ? 'w-[280px] sm:w-[320px] h-[310px]' 
                    : 'w-[300px] sm:w-[380px] h-[380px]'
                } ${
                  isCurrent 
                    ? 'border-[#0F766E] shadow-2xl shadow-teal-900/30 ring-2 ring-[#0F766E]/50 z-20' 
                    : 'border-slate-700/60 opacity-45 hover:opacity-80 scale-95 z-10'
                }`}
                style={{
                  transformStyle: 'preserve-3d',
                  transform: `rotateY(${itemAngle}deg) translateZ(${radius}px)`,
                  backfaceVisibility: 'hidden',
                  background: 'linear-gradient(180deg, #101C2C 0%, #08111E 100%)'
                }}
              >
                {/* Background Photo with Gradient Tint */}
                <div className="absolute inset-0 z-0">
                  <img 
                    src={scenario.image} 
                    alt={scenario.title} 
                    className="w-full h-full object-cover transition-transform duration-700 hover:scale-105 filter brightness-75 contrast-110" 
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-[#08111E] via-[#08111E]/75 to-transparent" />
                  <div className="absolute inset-0 bg-[#0F766E]/15 mix-blend-overlay" />
                </div>

                {/* Top Badge Overlay */}
                <div className="relative z-10 p-4 flex items-center justify-between">
                  <span className="font-mono text-[10px] uppercase font-bold tracking-wider px-2.5 py-1 rounded-full bg-teal-950/80 text-teal-300 border border-teal-500/40 backdrop-blur-md">
                    {scenario.badge}
                  </span>
                  <div className="flex items-center gap-1.5 font-mono text-[11px] font-bold text-amber-400 bg-black/60 px-2 py-0.5 rounded-full border border-amber-500/30">
                    <Thermometer className="w-3 h-3 text-amber-400" />
                    <span>{scenario.ambientTemp}</span>
                  </div>
                </div>

                {/* Bottom Content Card */}
                <div className="absolute bottom-0 inset-x-0 z-10 p-4 sm:p-5 flex flex-col justify-end">
                  <span className="text-[10px] font-mono uppercase tracking-wider text-teal-400 font-semibold mb-1">
                    {scenario.category} • {scenario.location}
                  </span>
                  <h3 className="font-serif-display text-lg sm:text-xl font-bold text-white mb-2 leading-tight">
                    {scenario.title}
                  </h3>
                  
                  {/* Performance Specs Grid */}
                  <div className="grid grid-cols-2 gap-2 pt-2 border-t border-slate-700/60 text-left">
                    <div>
                      <span className="text-[9px] font-mono text-slate-400 uppercase block">CORE PAYLOAD</span>
                      <span className="text-xs font-mono font-bold text-teal-300">{scenario.coreTemp}</span>
                    </div>
                    <div>
                      <span className="text-[9px] font-mono text-slate-400 uppercase block">VERIFIED METRIC</span>
                      <span className="text-xs font-mono font-bold text-white truncate block">{scenario.holdingPerformance}</span>
                    </div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Interactive Controls & Scenario Dossier Banner */}
      <div className="relative z-30 w-full max-w-4xl px-4 mt-3 flex flex-col sm:flex-row items-center justify-between gap-4">
        
        {/* Navigation Arrows & Indicator Pills */}
        <div className="flex items-center gap-3">
          <button
            onClick={handlePrev}
            className="p-2 rounded-xl bg-slate-900/80 hover:bg-[#0F766E] text-white border border-slate-700 hover:border-teal-400 transition-all cursor-pointer shadow-lg active:scale-95"
            title="Previous Horizon"
          >
            <ChevronLeft className="w-5 h-5" />
          </button>

          <div className="flex items-center gap-1.5">
            {DEPLOYMENT_SCENARIOS.map((s, idx) => (
              <button
                key={s.id}
                onClick={() => {
                  sound.click();
                  setActiveIndex(idx);
                }}
                className={`transition-all duration-300 rounded-full cursor-pointer ${
                  idx === activeIndex 
                    ? 'w-7 h-2 bg-gradient-to-r from-teal-400 to-sky-400' 
                    : 'w-2 h-2 bg-slate-700 hover:bg-slate-500'
                }`}
                title={s.title}
              />
            ))}
          </div>

          <button
            onClick={handleNext}
            className="p-2 rounded-xl bg-slate-900/80 hover:bg-[#0F766E] text-white border border-slate-700 hover:border-teal-400 transition-all cursor-pointer shadow-lg active:scale-95"
            title="Next Horizon"
          >
            <ChevronRight className="w-5 h-5" />
          </button>
        </div>

        {/* Live Active Horizon Summary */}
        <div className="flex-1 max-w-xl text-center sm:text-right">
          <p className="text-xs text-slate-300 leading-relaxed italic line-clamp-2">
            “{activeScenario.description}”
          </p>
        </div>
      </div>
    </div>
  );
};
