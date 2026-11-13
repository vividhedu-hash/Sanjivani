import React, { useState, useEffect, useRef } from 'react';
import { 
  Play, 
  Pause, 
  RotateCcw, 
  Maximize2, 
  Minimize2, 
  ChevronLeft, 
  ChevronRight, 
  Volume2, 
  VolumeX, 
  Layers, 
  Activity, 
  Award, 
  ShieldCheck, 
  Thermometer, 
  Zap, 
  Clock, 
  CheckCircle2, 
  AlertTriangle, 
  TrendingUp, 
  Compass, 
  FileText,
  Sparkles,
  ArrowRight,
  Download
} from 'lucide-react';
import { sound } from '../utils/soundEffects';
import { OrbitalRadarHUD } from './OrbitalRadarHUD';
import { Curved3DCarousel } from './Curved3DCarousel';
import { Model3DViewer } from './Model3DViewer';

interface SlideConfig {
  id: number;
  chapterNumber: string;
  title: string;
  subtitle: string;
  totalSteps: number;
}

export const SLIDES_CONFIG: SlideConfig[] = [
  { id: 1, chapterNumber: "01", title: "Project Sanjivani", subtitle: "Autonomous Hybrid Cold-Chain Storage System", totalSteps: 3 },
  { id: 2, chapterNumber: "02", title: "The Medical Cold-Chain Crisis", subtitle: "Vaccine Spoilage & Last-Mile Vulnerability", totalSteps: 3 },
  { id: 3, chapterNumber: "03", title: "Severe Tropical Heatwaves", subtitle: "45°C Ambient Stress & Rapid Ice Melting", totalSteps: 3 },
  { id: 4, chapterNumber: "04", title: "The Freeze-Abuse Paradox", subtitle: "Sub-Zero Freezing Destroys Liquid Biologics", totalSteps: 3 },
  { id: 5, chapterNumber: "05", title: "Why Hybrid Renewable Innovation?", subtitle: "Four Critical Physical Bottlenecks Solved", totalSteps: 4 },
  { id: 6, chapterNumber: "06", title: "Core Hardware Specifications", subtitle: "Bio-PCM, Derated Peltier & LiFePO4 Energy", totalSteps: 4 },
  { id: 7, chapterNumber: "07", title: "3D Cutaway Digital Twin", subtitle: "Interactive 3D Subsystem Inspection & Exploded View", totalSteps: 2 },
  { id: 8, chapterNumber: "08", title: "Closed-Loop Hysteresis Control", subtitle: "Sensor-Triggered Duty Cycle & Microcontroller Logic", totalSteps: 3 },
  { id: 9, chapterNumber: "09", title: "Orbital Telemetry Radar HUD", subtitle: "360° Real-Time System Telemetry & Feedback", totalSteps: 2 },
  { id: 10, chapterNumber: "10", title: "Empirical Thermal Validation", subtitle: "Holding Time Extended by +52.8% (109.4 Hours)", totalSteps: 3 },
  { id: 11, chapterNumber: "11", title: "3D Cylindrical Deployment Horizons", subtitle: "Microclimate Stress-Testing Across India", totalSteps: 2 },
  { id: 12, chapterNumber: "12", title: "Production Economics & Payback", subtitle: "Lifecycle TCO, Spoilage Savings & 1.4-Year Payback", totalSteps: 4 },
  { id: 13, chapterNumber: "13", title: "FMEA Reliability & Maintenance", subtitle: "Risk Priority Number Reduced from 288 to 24", totalSteps: 4 },
  { id: 14, chapterNumber: "14", title: "National Mission & Conclusion", subtitle: "STEM for Viksit and Atmanirbhar Bharat 2047", totalSteps: 2 }
];

export const KeynotePresentationDeck: React.FC = () => {
  const [currentSlide, setCurrentSlide] = useState<number>(0);
  const [currentStep, setCurrentStep] = useState<number>(0);
  const [isAutoPlaying, setIsAutoPlaying] = useState<boolean>(false);
  const [isFullscreen, setIsFullscreen] = useState<boolean>(false);
  const [isSoundMuted, setIsSoundMuted] = useState<boolean>(false);
  const [showThumbnails, setShowThumbnails] = useState<boolean>(false);
  const [autoPlayProgress, setAutoPlayProgress] = useState<number>(0);
  
  const deckContainerRef = useRef<HTMLDivElement>(null);
  const autoPlayTimerRef = useRef<number | null>(null);

  const activeConfig = SLIDES_CONFIG[currentSlide];

  // Auto-play timer loop with smooth progress countdown
  useEffect(() => {
    if (!isAutoPlaying) {
      if (autoPlayTimerRef.current) clearInterval(autoPlayTimerRef.current);
      setAutoPlayProgress(0);
      return;
    }

    const intervalStep = 50; // ms
    const totalStepDuration = 4200; // ms per step
    let elapsed = 0;

    autoPlayTimerRef.current = window.setInterval(() => {
      elapsed += intervalStep;
      setAutoPlayProgress((elapsed / totalStepDuration) * 100);

      if (elapsed >= totalStepDuration) {
        elapsed = 0;
        setAutoPlayProgress(0);
        handleNextStep();
      }
    }, intervalStep);

    return () => {
      if (autoPlayTimerRef.current) clearInterval(autoPlayTimerRef.current);
    };
  }, [isAutoPlaying, currentSlide, currentStep]);

  // Keyboard navigation
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') {
        e.preventDefault();
        handleNextStep();
      } else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {
        e.preventDefault();
        handlePrevStep();
      } else if (e.key.toLowerCase() === 'p') {
        setIsAutoPlaying(prev => !prev);
        sound.click();
      } else if (e.key.toLowerCase() === 'f') {
        toggleFullscreen();
      } else if (e.key.toLowerCase() === 'r') {
        resetPresentation();
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [currentSlide, currentStep]);

  const handleNextStep = () => {
    sound.click();
    if (currentStep < activeConfig.totalSteps - 1) {
      setCurrentStep(s => s + 1);
    } else {
      if (currentSlide < SLIDES_CONFIG.length - 1) {
        setCurrentSlide(s => s + 1);
        setCurrentStep(0);
      } else {
        setIsAutoPlaying(false);
      }
    }
  };

  const handlePrevStep = () => {
    sound.click();
    if (currentStep > 0) {
      setCurrentStep(s => s - 1);
    } else {
      if (currentSlide > 0) {
        setCurrentSlide(s => s - 1);
        setCurrentStep(SLIDES_CONFIG[currentSlide - 1].totalSteps - 1);
      }
    }
  };

  const jumpToSlide = (index: number) => {
    sound.click();
    setCurrentSlide(index);
    setCurrentStep(0);
    setShowThumbnails(false);
  };

  const resetPresentation = () => {
    sound.click();
    setCurrentSlide(0);
    setCurrentStep(0);
    setIsAutoPlaying(false);
  };

  const toggleFullscreen = () => {
    sound.click();
    if (!document.fullscreenElement) {
      deckContainerRef.current?.requestFullscreen().then(() => setIsFullscreen(true)).catch(() => {});
    } else {
      document.exitFullscreen().then(() => setIsFullscreen(false)).catch(() => {});
    }
  };

  const toggleSound = () => {
    const next = !isSoundMuted;
    setIsSoundMuted(next);
    sound.setMuted(next);
    if (!next) sound.chime();
  };

  // Render Content for each Slide
  const renderSlideContent = () => {
    switch (currentSlide) {
      
      // ==========================================
      // SLIDE 01: HERO COVER (Dr. B. K. Passi Balvigyan)
      // ==========================================
      case 0:
        return (
          <div className="relative w-full h-full flex flex-col items-center justify-center p-6 sm:p-12 text-center select-none overflow-hidden">
            {/* High-Tech Radial Glow Background */}
            <div className="absolute inset-0 bg-radial-glow pointer-events-none" />
            <div className="absolute inset-0 bg-tech-grid-dark pointer-events-none" />

            {/* Step 0: Accreditation Header */}
            <div className={`transition-all duration-700 transform ${currentStep >= 0 ? 'opacity-100 translate-y-0' : 'opacity-0 -translate-y-6'} z-10 space-y-2 mb-4`}>
              <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-slate-900/90 border border-teal-500/40 text-teal-300 font-mono text-xs sm:text-sm font-bold shadow-lg shadow-teal-950/50">
                <Award className="w-4 h-4 text-amber-400" />
                <span>Dr. B. K. PASSI MEMORIAL SENIOR BALVIGYAN 2026–2027</span>
                <span className="text-slate-500">•</span>
                <span className="text-white">PHYSICS</span>
              </div>
              <div className="flex items-center justify-center gap-3 font-mono text-xs text-slate-400">
                <span className="text-teal-400 font-semibold">School UID: SBVPH-05</span>
                <span>•</span>
                <span>G. D. Goenka Public School, Indore</span>
              </div>
            </div>

            {/* Step 1: Main Title & Sanskrit Badge */}
            <div className={`transition-all duration-700 delay-150 transform ${currentStep >= 1 ? 'opacity-100 scale-100' : 'opacity-0 scale-95'} z-10 max-w-4xl space-y-3`}>
              <div className="flex items-center justify-center gap-3">
                <span className="font-serif-display text-4xl sm:text-6xl md:text-7xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-white via-teal-100 to-teal-300 tracking-tight drop-shadow-lg">
                  SANJIVANI
                </span>
                <span className="font-devanagari text-2xl sm:text-4xl text-[#2DD4BF] font-bold px-3 py-1 rounded-xl bg-teal-950/80 border border-teal-500/40 shadow-lg">
                  संजीवनी
                </span>
              </div>
              <h2 className="font-serif-display text-lg sm:text-2xl md:text-3xl text-slate-200 font-medium leading-snug">
                Design & Development of a Sensor-Triggered Hybrid PCM–Peltier Cooling System for Extended Cold-Chain Storage
              </h2>
              <p className="font-serif-display text-sm sm:text-base text-teal-300/90 italic tracking-wide">
                “Preserving Temperature. Protecting Life. When Solid-State Physics Meets Biological Potency.”
              </p>
            </div>

            {/* Step 2: Thematic Alignment & Authors Banner */}
            <div className={`transition-all duration-700 delay-300 transform ${currentStep >= 2 ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-6'} z-10 mt-8 grid grid-cols-1 sm:grid-cols-3 gap-3 w-full max-w-3xl`}>
              <div className="p-3.5 rounded-xl bg-slate-900/90 border border-teal-500/30 text-left shadow-lg">
                <span className="font-mono text-[10px] text-teal-400 uppercase block font-bold">THEME</span>
                <span className="text-xs font-semibold text-slate-200">STEM for Viksit & Atmanirbhar Bharat</span>
              </div>
              <div className="p-3.5 rounded-xl bg-slate-900/90 border border-teal-500/30 text-left shadow-lg">
                <span className="font-mono text-[10px] text-teal-400 uppercase block font-bold">SUB-THEME</span>
                <span className="text-xs font-semibold text-slate-200">Health & Hygiene (Cold Logistics)</span>
              </div>
              <div className="p-3.5 rounded-xl bg-slate-900/90 border border-teal-500/30 text-left shadow-lg">
                <span className="font-mono text-[10px] text-teal-400 uppercase block font-bold">RESEARCH TEAM</span>
                <span className="text-xs font-semibold text-slate-200">Bhavmanyu, Vaishnavi, Gaurav, Prathamesh</span>
              </div>
            </div>
          </div>
        );

      // ==========================================
      // SLIDE 02: THE COLD-CHAIN CRISIS
      // ==========================================
      case 1:
        return (
          <div className="relative w-full h-full p-6 sm:p-10 flex flex-col justify-between select-none overflow-hidden">
            <div>
              <span className="font-mono text-xs font-bold text-rose-400 uppercase tracking-wider block mb-1">
                CHAPTER 01 • THE PROBLEM STATEMENT
              </span>
              <h2 className="font-serif-display text-2xl sm:text-4xl font-bold text-white">
                The Fatal Vulnerability in India's Last-Mile Vaccine Cold-Chain
              </h2>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 my-auto">
              
              {/* Step 0: 50% Wastage Metric */}
              <div className={`p-5 rounded-2xl bg-slate-900/90 border transition-all duration-500 ${
                currentStep >= 0 
                  ? 'border-rose-500/70 shadow-2xl shadow-rose-950/40 opacity-100 translate-y-0' 
                  : 'border-slate-800 opacity-20 translate-y-4'
              }`}>
                <div className="w-12 h-12 rounded-xl bg-rose-500/20 border border-rose-500/40 flex items-center justify-center text-rose-400 mb-3 font-mono text-xl font-bold">
                  50%
                </div>
                <h3 className="font-serif-display text-lg font-bold text-white mb-1">
                  Global Vaccine Spoilage
                </h3>
                <p className="text-xs text-slate-300 leading-relaxed">
                  WHO estimates up to <strong>50% of vaccines are wasted globally</strong> every year due to temperature excursions during off-grid transit, costing billions of dollars and leaving millions unprotected.
                </p>
              </div>

              {/* Step 1: Macromolecular Denaturation */}
              <div className={`p-5 rounded-2xl bg-slate-900/90 border transition-all duration-500 delay-100 ${
                currentStep >= 1 
                  ? 'border-amber-500/70 shadow-2xl shadow-amber-950/40 opacity-100 translate-y-0' 
                  : 'border-slate-800 opacity-20 translate-y-4'
              }`}>
                <div className="w-12 h-12 rounded-xl bg-amber-500/20 border border-amber-500/40 flex items-center justify-center text-amber-400 mb-3">
                  <Thermometer className="w-6 h-6" />
                </div>
                <h3 className="font-serif-display text-lg font-bold text-white mb-1">
                  Macromolecular Denaturation
                </h3>
                <p className="text-xs text-slate-300 leading-relaxed">
                  Vaccines possess delicate tertiary and quaternary protein structures. Excursions outside the strict <strong>+2.0°C to +8.0°C</strong> corridor cause irreversible antigen precipitation and total loss of potency.
                </p>
              </div>

              {/* Step 2: Rural Clinic Image & Logistics */}
              <div className={`p-4 rounded-2xl bg-slate-900/90 border transition-all duration-500 delay-200 overflow-hidden ${
                currentStep >= 2 
                  ? 'border-teal-500/70 shadow-2xl shadow-teal-950/40 opacity-100 translate-y-0' 
                  : 'border-slate-800 opacity-20 translate-y-4'
              }`}>
                <div className="h-28 rounded-xl overflow-hidden mb-3 relative">
                  <img src="/assets/photos/rural_clinic.jpg" alt="Rural Clinic" className="w-full h-full object-cover filter brightness-90" />
                  <div className="absolute inset-0 bg-gradient-to-t from-slate-950 via-transparent to-transparent" />
                  <span className="absolute bottom-2 left-2 text-[10px] font-mono text-teal-300 font-bold bg-slate-950/80 px-2 py-0.5 rounded">
                    RURAL PRIMARY HEALTH CENTRE
                  </span>
                </div>
                <h3 className="font-serif-display text-base font-bold text-white mb-1">
                  Off-Grid Last-Mile Bottleneck
                </h3>
                <p className="text-[11px] text-slate-300 leading-tight">
                  Frequent power cuts, muddy terrain, and ASHA transport times of 48–72 hours break conventional cold boxes.
                </p>
              </div>

            </div>

            <div className={`p-3 rounded-xl bg-rose-950/60 border border-rose-500/40 flex items-center justify-between text-xs font-mono transition-all duration-500 ${
              currentStep >= 2 ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-2'
            }`}>
              <span className="text-rose-300 font-bold">MORTALITY IMPACT:</span>
              <span className="text-slate-200">Over 1.5 million preventable child deaths occur globally each year from vaccine-preventable diseases.</span>
            </div>
          </div>
        );

      // ==========================================
      // SLIDE 03: SEVERE TROPICAL HEATWAVES
      // ==========================================
      case 2:
        return (
          <div className="relative w-full h-full p-6 sm:p-10 flex flex-col justify-between select-none overflow-hidden">
            <div>
              <span className="font-mono text-xs font-bold text-amber-400 uppercase tracking-wider block mb-1">
                CHAPTER 02 • ENVIRONMENTAL STRESS
              </span>
              <h2 className="font-serif-display text-2xl sm:text-4xl font-bold text-white">
                Severe Tropical Ambient Stress (+45°C Peak Diurnal Heat)
              </h2>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 my-auto items-center">
              
              {/* Photo Card: Desert Heat */}
              <div className={`relative rounded-2xl overflow-hidden border border-amber-500/40 shadow-2xl h-64 sm:h-72 transition-all duration-700 ${
                currentStep >= 0 ? 'opacity-100 scale-100' : 'opacity-20 scale-95'
              }`}>
                <img src="/assets/photos/desert_heat.jpg" alt="Desert Heat" className="w-full h-full object-cover filter contrast-125" />
                <div className="absolute inset-0 bg-gradient-to-t from-slate-950 via-slate-950/40 to-transparent" />
                <div className="absolute bottom-4 left-4 right-4">
                  <span className="px-2.5 py-1 rounded-lg text-xs font-mono font-bold bg-amber-500 text-slate-950 shadow-md">
                    THAR DESERT & CENTRAL INDIA: 45°C AMBIENT
                  </span>
                  <p className="text-xs text-slate-200 mt-2 leading-relaxed">
                    Fourier conduction drives severe heat influx <code className="text-amber-300 font-mono">Q_in = UA · (T_amb - T_int)</code> into standard foam coolers, rapidly exhausting wet ice within 24–36 hours.
                  </p>
                </div>
              </div>

              {/* Data & Thermal Mechanics */}
              <div className="space-y-4">
                
                <div className={`p-4 rounded-2xl bg-slate-900/90 border transition-all duration-500 ${
                  currentStep >= 1 ? 'border-amber-500/60 shadow-xl opacity-100 translate-x-0' : 'border-slate-800 opacity-20 translate-x-4'
                }`}>
                  <div className="flex items-center justify-between mb-1">
                    <span className="font-mono text-xs font-bold text-amber-400">HEAT INGRESS FLUX</span>
                    <span className="font-mono text-xs text-white font-black">5.88 W (at 45°C)</span>
                  </div>
                  <div className="w-full h-2 bg-slate-800 rounded-full overflow-hidden">
                    <div className="h-full bg-gradient-to-r from-amber-500 to-rose-500 rounded-full w-full animate-pulse" />
                  </div>
                  <p className="text-[11px] text-slate-300 mt-2">
                    Enclosure heat conduction <code className="text-teal-300">UA = 0.147 W/K</code> experiences a 40 K temperature gradient between outside summer ambient (45°C) and core (+5°C).
                  </p>
                </div>

                <div className={`p-4 rounded-2xl bg-slate-900/90 border transition-all duration-500 delay-100 ${
                  currentStep >= 2 ? 'border-teal-500/60 shadow-xl opacity-100 translate-x-0' : 'border-slate-800 opacity-20 translate-x-4'
                }`}>
                  <div className="flex items-center justify-between mb-1">
                    <span className="font-mono text-xs font-bold text-teal-400">PASSIVE ICE BUFFER COLLAPSE</span>
                    <span className="font-mono text-xs text-rose-400 font-black">Fails at 71.8 Hours</span>
                  </div>
                  <p className="text-[11px] text-slate-300">
                    Without an active solid-state heat pump, passive ice or PCM absorbs heat continuously until exhausted. Active Peltier pumping is mathematically required to guarantee 100+ hours autonomy.
                  </p>
                </div>

              </div>

            </div>

            <div className="p-3 rounded-xl bg-slate-900 border border-slate-800 text-center font-mono text-xs text-slate-400">
              SANJIVANI is engineered for worst-case WHO Category A tropical test profiles (+43°C day / +28°C night).
            </div>
          </div>
        );

      // ==========================================
      // SLIDE 04: THE FREEZE-ABUSE PARADOX
      // ==========================================
      case 3:
        return (
          <div className="relative w-full h-full p-6 sm:p-10 flex flex-col justify-between select-none overflow-hidden">
            <div>
              <span className="font-mono text-xs font-bold text-sky-400 uppercase tracking-wider block mb-1">
                CHAPTER 03 • THE HIDDEN THREAT
              </span>
              <h2 className="font-serif-display text-2xl sm:text-4xl font-bold text-white">
                The Accidental Freezing Paradox (The Cold Abuse Trap)
              </h2>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 my-auto items-center">
              
              {/* Card 1: Water Ice-Pack Hazard */}
              <div className={`p-6 rounded-2xl bg-slate-900/90 border transition-all duration-500 ${
                currentStep >= 0 ? 'border-rose-500/70 shadow-2xl shadow-rose-950/40 opacity-100' : 'border-slate-800 opacity-20'
              }`}>
                <div className="flex items-center justify-between pb-3 border-b border-slate-800 mb-3">
                  <h3 className="font-serif-display text-xl font-bold text-rose-400">
                    Conventional Water Ice Packs
                  </h3>
                  <span className="font-mono text-xs text-rose-300 font-bold bg-rose-950/80 px-2 py-0.5 rounded border border-rose-500/40">
                    DANGEROUS: 0°C to -15°C
                  </span>
                </div>
                <ul className="space-y-3 text-xs text-slate-300">
                  <li className="flex items-start gap-2">
                    <AlertTriangle className="w-4 h-4 text-rose-400 shrink-0 mt-0.5" />
                    <span>Frozen ice-packs loaded from deep freezers sit at <strong>-15°C to -20°C</strong>.</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <AlertTriangle className="w-4 h-4 text-rose-400 shrink-0 mt-0.5" />
                    <span>Direct contact immediately freezes vaccines, causing irreversible aluminium-adjuvant lattice agglomeration.</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <AlertTriangle className="w-4 h-4 text-rose-400 shrink-0 mt-0.5" />
                    <span>Destroys Hepatitis B, DTP, Tetanus Toxoid, HPV, and Pentavalent vaccines.</span>
                  </li>
                </ul>
              </div>

              {/* Card 2: SANJIVANI Bio-PCM Innovation */}
              <div className={`p-6 rounded-2xl bg-slate-900/90 border transition-all duration-500 delay-100 ${
                currentStep >= 1 ? 'border-teal-400 shadow-2xl shadow-teal-950/40 opacity-100' : 'border-slate-800 opacity-20'
              }`}>
                <div className="flex items-center justify-between pb-3 border-b border-slate-800 mb-3">
                  <h3 className="font-serif-display text-xl font-bold text-teal-300">
                    CrodaTherm 5 Bio-PCM
                  </h3>
                  <span className="font-mono text-xs text-teal-300 font-bold bg-teal-950/80 px-2 py-0.5 rounded border border-teal-500/40">
                    SAFE: EXACTLY +5.0°C
                  </span>
                </div>
                <ul className="space-y-3 text-xs text-slate-300">
                  <li className="flex items-start gap-2">
                    <CheckCircle2 className="w-4 h-4 text-teal-400 shrink-0 mt-0.5" />
                    <span>Melts and solidifies at exactly <strong>+5.0°C</strong> (the mathematical midpoint of the +2°C to +8°C safe zone).</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <CheckCircle2 className="w-4 h-4 text-teal-400 shrink-0 mt-0.5" />
                    <span><strong>100% physically impossible to freeze vaccines</strong> even if unconditioned.</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <CheckCircle2 className="w-4 h-4 text-teal-400 shrink-0 mt-0.5" />
                    <span>100% plant-based renewable lipid esters, non-toxic, biodegradable, and zero fire risk.</span>
                  </li>
                </ul>
              </div>

            </div>

            <div className={`p-3 rounded-xl bg-teal-950/40 border border-teal-500/30 text-center font-mono text-xs text-teal-300 transition-all duration-500 ${
              currentStep >= 2 ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-2'
            }`}>
              WHO studies show over 75% of vaccine shipments experience accidental sub-zero freezing. SANJIVANI eliminates this risk completely.
            </div>
          </div>
        );

      // ==========================================
      // SLIDE 05: WHY HYBRID INNOVATION? (4 Bottlenecks)
      // ==========================================
      case 4:
        return (
          <div className="relative w-full h-full p-6 sm:p-10 flex flex-col justify-between select-none overflow-hidden">
            <div className="text-center">
              <h2 className="font-serif-display text-2xl sm:text-4xl font-bold text-white mb-1">
                Why Hybrid Renewable PCM–Peltier Innovation?
              </h2>
              <p className="font-mono text-xs text-teal-400">
                Solving the Four Fundamental Physical Bottlenecks of Existing Systems
              </p>
            </div>

            {/* 4 Interactive Bottleneck Pillars */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 my-auto">
              
              <div className={`p-5 rounded-2xl bg-slate-900/90 border transition-all duration-500 ${
                currentStep >= 0 ? 'border-amber-400 shadow-xl shadow-amber-950/40 -translate-y-2 opacity-100' : 'border-slate-800 opacity-20'
              }`}>
                <span className="font-mono text-2xl font-bold text-amber-400 block mb-2">01</span>
                <h3 className="font-serif-display text-base font-bold text-white mb-1">Fourier Heat Influx</h3>
                <p className="text-xs text-slate-300 leading-relaxed">
                  Passive coolers fail once ice packs melt. SANJIVANI pairs 1,046 kJ of latent PCM storage with a solid-state Peltier pump to forcibly reject heat spikes.
                </p>
              </div>

              <div className={`p-5 rounded-2xl bg-slate-900/90 border transition-all duration-500 delay-100 ${
                currentStep >= 1 ? 'border-sky-400 shadow-xl shadow-sky-950/40 -translate-y-2 opacity-100' : 'border-slate-800 opacity-20'
              }`}>
                <span className="font-mono text-2xl font-bold text-sky-400 block mb-2">02</span>
                <h3 className="font-serif-display text-base font-bold text-white mb-1">Subcritical Freezing</h3>
                <p className="text-xs text-slate-300 leading-relaxed">
                  Water freezes at 0°C. Frozen icepacks destroy liquid vaccines. Replacing water with plant-based CrodaTherm 5 (+5.0°C) eliminates all freeze risk.
                </p>
              </div>

              <div className={`p-5 rounded-2xl bg-slate-900/90 border transition-all duration-500 delay-200 ${
                currentStep >= 2 ? 'border-rose-400 shadow-xl shadow-rose-950/40 -translate-y-2 opacity-100' : 'border-slate-800 opacity-20'
              }`}>
                <span className="font-mono text-2xl font-bold text-rose-400 block mb-2">03</span>
                <h3 className="font-serif-display text-base font-bold text-white mb-1">Compressor Vibration</h3>
                <p className="text-xs text-slate-300 leading-relaxed">
                  Mechanical compressors weigh 15–25 kg and snap on bumpy rural roads. Solid-state Peltier thermoelectrics have <strong>zero moving parts</strong>.
                </p>
              </div>

              <div className={`p-5 rounded-2xl bg-slate-900/90 border transition-all duration-500 delay-300 ${
                currentStep >= 3 ? 'border-teal-400 shadow-xl shadow-teal-950/40 -translate-y-2 opacity-100' : 'border-slate-800 opacity-20'
              }`}>
                <span className="font-mono text-2xl font-bold text-teal-400 block mb-2">04</span>
                <h3 className="font-serif-display text-base font-bold text-white mb-1">Grid Blackout Autonomy</h3>
                <p className="text-xs text-slate-300 leading-relaxed">
                  Active cooling drains batteries in 8 hours. SANJIVANI relies on <strong>passive PCM for 92% of the mission</strong>, extending autonomy to 109.4 hours!
                </p>
              </div>

            </div>

            <div className="p-3 rounded-xl bg-slate-900 border border-slate-800 text-center font-mono text-xs text-slate-400">
              Synergistic coupling prevents battery weight explosion while guaranteeing 100% WHO PQS E004 compliance.
            </div>
          </div>
        );

      // ==========================================
      // SLIDE 06: CORE TECHNICAL HARDWARE SPECS
      // ==========================================
      case 5:
        return (
          <div className="relative w-full h-full p-6 sm:p-10 flex flex-col justify-between select-none overflow-hidden">
            <div>
              <span className="font-mono text-xs font-bold text-teal-400 uppercase tracking-wider block mb-1">
                CHAPTER 04 • HARDWARE ARCHITECTURE
              </span>
              <h2 className="font-serif-display text-2xl sm:text-4xl font-bold text-white">
                Audited Hardware Specifications (45-Page Dossier)
              </h2>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 my-auto">
              
              <div className={`p-5 rounded-2xl bg-slate-900/90 border transition-all duration-500 ${
                currentStep >= 0 ? 'border-teal-500 shadow-xl opacity-100' : 'border-slate-800 opacity-20'
              }`}>
                <h3 className="font-serif-display text-lg font-bold text-teal-300 mb-2">
                  Bio-PCM Cassettes (CrodaTherm 5)
                </h3>
                <ul className="space-y-1.5 text-xs font-mono text-slate-300">
                  <li className="flex justify-between"><span className="text-slate-500">Mass:</span> <strong className="text-white">4.8 kg (6 packs × 800g)</strong></li>
                  <li className="flex justify-between"><span className="text-slate-500">Melting Point:</span> <strong className="text-teal-300">+5.0°C (Isothermal Buffer)</strong></li>
                  <li className="flex justify-between"><span className="text-slate-500">Latent Heat:</span> <strong className="text-white">218 kJ/kg (1,046.4 kJ total)</strong></li>
                  <li className="flex justify-between"><span className="text-slate-500">Payload Capacity:</span> <strong className="text-emerald-400">24 Standard Vaccine Vials</strong></li>
                </ul>
              </div>

              <div className={`p-5 rounded-2xl bg-slate-900/90 border transition-all duration-500 delay-100 ${
                currentStep >= 1 ? 'border-sky-500 shadow-xl opacity-100' : 'border-slate-800 opacity-20'
              }`}>
                <h3 className="font-serif-display text-lg font-bold text-sky-300 mb-2">
                  Dual Thermoelectric Engine
                </h3>
                <ul className="space-y-1.5 text-xs font-mono text-slate-300">
                  <li className="flex justify-between"><span className="text-slate-500">Modules:</span> <strong className="text-white">Dual TEC1-12706 (Derated)</strong></li>
                  <li className="flex justify-between"><span className="text-slate-500">Operating Voltage:</span> <strong className="text-white">7.50 V DC (Optimal COP)</strong></li>
                  <li className="flex justify-between"><span className="text-slate-500">Power Input:</span> <strong className="text-white">30.0 W (vs 72W rated)</strong></li>
                  <li className="flex justify-between"><span className="text-slate-500">Thermoelectric COP:</span> <strong className="text-sky-300">0.61 (Q_cold = 18.5 W)</strong></li>
                </ul>
              </div>

              <div className={`p-5 rounded-2xl bg-slate-900/90 border transition-all duration-500 delay-200 ${
                currentStep >= 2 ? 'border-amber-500 shadow-xl opacity-100' : 'border-slate-800 opacity-20'
              }`}>
                <h3 className="font-serif-display text-lg font-bold text-amber-300 mb-2">
                  LiFePO4 Energy System
                </h3>
                <ul className="space-y-1.5 text-xs font-mono text-slate-300">
                  <li className="flex justify-between"><span className="text-slate-500">Battery Spec:</span> <strong className="text-white">12.8V 30Ah (384 Wh gross)</strong></li>
                  <li className="flex justify-between"><span className="text-slate-500">Active Pumping Time:</span> <strong className="text-white">8.75 Hours Net Firing</strong></li>
                  <li className="flex justify-between"><span className="text-slate-500">Cycle Lifespan:</span> <strong className="text-amber-400">2,500+ Cycles (10–12 Years)</strong></li>
                  <li className="flex justify-between"><span className="text-slate-500">Safety:</span> <strong className="text-emerald-400">Zero Thermal Runaway</strong></li>
                </ul>
              </div>

              <div className={`p-5 rounded-2xl bg-slate-900/90 border transition-all duration-500 delay-300 ${
                currentStep >= 3 ? 'border-emerald-500 shadow-xl opacity-100' : 'border-slate-800 opacity-20'
              }`}>
                <h3 className="font-serif-display text-lg font-bold text-emerald-300 mb-2">
                  Enclosure & Insulation
                </h3>
                <ul className="space-y-1.5 text-xs font-mono text-slate-300">
                  <li className="flex justify-between"><span className="text-slate-500">Dimensions:</span> <strong className="text-white">450 × 300 × 320 mm (5.2 kg)</strong></li>
                  <li className="flex justify-between"><span className="text-slate-500">Insulation:</span> <strong className="text-white">20mm VIP + 25mm PUF Core</strong></li>
                  <li className="flex justify-between"><span className="text-slate-500">Conductance:</span> <strong className="text-emerald-300">UA = 0.147 W/K</strong></li>
                  <li className="flex justify-between"><span className="text-slate-500">Sealing:</span> <strong className="text-white">Dual EPDM Gasket + Cam Latches</strong></li>
                </ul>
              </div>

            </div>

            <div className="p-2.5 rounded-xl bg-slate-900 border border-slate-800 text-center font-mono text-[11px] text-slate-400">
              Hot-side rejection: Q_hot = Q_cold + P_elec = 18.5W + 30.0W = 48.5 W discharged via 24-fin skived heat sink.
            </div>
          </div>
        );

      // ==========================================
      // SLIDE 07: 3D DIGITAL TWIN & EXPLODED SYSTEM
      // ==========================================
      case 6:
        return (
          <div className="relative w-full h-full p-4 sm:p-6 flex flex-col justify-between select-none overflow-hidden">
            <div className="flex items-center justify-between">
              <div>
                <span className="font-mono text-xs font-bold text-teal-400 uppercase tracking-wider block">
                  CHAPTER 05 • 3D CUTAWAY ARCHITECTURE
                </span>
                <h2 className="font-serif-display text-xl sm:text-2xl font-bold text-white">
                  Interactive 3D Subsystem Inspection & Exploded View
                </h2>
              </div>
              <span className="hidden sm:inline font-mono text-xs text-teal-400 bg-slate-900 px-3 py-1 rounded-lg border border-teal-500/30 font-bold">
                USE SLIDER TO EXPLODE • DRAG TO ROTATE
              </span>
            </div>

            {/* Embedded Live Three.js Model */}
            <div className="flex-1 my-2 rounded-2xl overflow-hidden border border-slate-800 bg-[#060B14] relative min-h-[380px]">
              <Model3DViewer isSlideMode={true} />
            </div>

            <div className="flex items-center justify-between text-xs font-mono text-slate-400">
              <span>Upper Deck: 4.8kg CrodaTherm 5 Bio-PCM + 24 Vaccine Vials</span>
              <span>Lower Deck: Dual Peltier TEC1-12706 + Skived Fin Heat Sink + ESP32</span>
            </div>
          </div>
        );

      // ==========================================
      // SLIDE 08: CLOSED-LOOP HYSTERESIS CONTROL
      // ==========================================
      case 7:
        return (
          <div className="relative w-full h-full p-6 sm:p-10 flex flex-col justify-between select-none overflow-hidden">
            <div>
              <span className="font-mono text-xs font-bold text-teal-400 uppercase tracking-wider block mb-1">
                CHAPTER 06 • SENSOR-TRIGGERED LOGIC
              </span>
              <h2 className="font-serif-display text-2xl sm:text-4xl font-bold text-white">
                Closed-Loop Hysteresis State Machine & Algorithmic Control
              </h2>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 my-auto items-center">
              
              {/* Flowchart Diagram */}
              <div className={`p-4 rounded-2xl bg-slate-900/90 border border-slate-800 shadow-2xl transition-all duration-700 ${
                currentStep >= 0 ? 'opacity-100 scale-100' : 'opacity-20 scale-95'
              }`}>
                <img src="/assets/control_flowchart.png" alt="Control Flowchart" className="w-full h-auto rounded-xl filter contrast-125" />
              </div>

              {/* State Machine Logic */}
              <div className="space-y-4">
                
                <div className={`p-4 rounded-2xl bg-slate-900/90 border transition-all duration-500 ${
                  currentStep >= 1 ? 'border-amber-500/70 shadow-xl opacity-100 translate-x-0' : 'border-slate-800 opacity-20 translate-x-4'
                }`}>
                  <div className="flex items-center justify-between mb-1">
                    <span className="font-mono text-xs font-bold text-amber-400 uppercase">UPPER THRESHOLD TRIGGER</span>
                    <span className="font-mono text-sm text-white font-black">+5.80°C</span>
                  </div>
                  <p className="text-xs text-slate-300 leading-relaxed">
                    When digital sensor reads ≥ +5.80°C, the ESP32 microcontroller engages the MOSFET gate driver, powering the dual Peltier engine to pump 18.5 W away from the PCM.
                  </p>
                </div>

                <div className={`p-4 rounded-2xl bg-slate-900/90 border transition-all duration-500 delay-100 ${
                  currentStep >= 2 ? 'border-sky-500/70 shadow-xl opacity-100 translate-x-0' : 'border-slate-800 opacity-20 translate-x-4'
                }`}>
                  <div className="flex items-center justify-between mb-1">
                    <span className="font-mono text-xs font-bold text-sky-400 uppercase">LOWER THRESHOLD CUTOFF</span>
                    <span className="font-mono text-sm text-white font-black">+2.80°C</span>
                  </div>
                  <p className="text-xs text-slate-300 leading-relaxed">
                    Once the core cools to +2.80°C, the Peltier shuts down. This creates a 3.0 K deadband, preventing rapid switching cycles, saving 71.5% battery power, and guaranteeing zero freeze risk!
                  </p>
                </div>

              </div>

            </div>

            <div className="p-3 rounded-xl bg-teal-950/40 border border-teal-500/30 text-center font-mono text-xs text-teal-300">
              Net mission duty cycle: 8.0% | Standby power draw: 0.15 W | Active pumping power: 30.0 W.
            </div>
          </div>
        );

      // ==========================================
      // SLIDE 09: ORBITAL TELEMETRY RADAR HUD
      // ==========================================
      case 8:
        return (
          <div className="relative w-full h-full p-4 sm:p-6 flex flex-col justify-between select-none overflow-hidden">
            <div className="flex items-center justify-between">
              <div>
                <span className="font-mono text-xs font-bold text-teal-400 uppercase tracking-wider block">
                  CHAPTER 07 • CLOSED-LOOP TELEMETRY
                </span>
                <h2 className="font-serif-display text-xl sm:text-2xl font-bold text-white">
                  Orbital Telemetry Radar Architecture (360° Closed-Loop)
                </h2>
              </div>
              <span className="font-mono text-xs text-teal-400 bg-slate-900 px-3 py-1 rounded-lg border border-teal-500/30 font-bold">
                CLICK NODES TO INSPECT TELEMETRY
              </span>
            </div>

            {/* Embedded Live Orbital Radar HUD */}
            <div className="flex-1 my-2 rounded-2xl overflow-hidden border border-slate-800 relative">
              <OrbitalRadarHUD isSlideMode={true} />
            </div>

            <div className="text-center font-mono text-xs text-slate-400">
              Point 1: Peltier Engine • Point 2: Bio-PCM Cassettes • Point 3: Hysteresis Controller • Point 4: LiFePO4 Battery
            </div>
          </div>
        );

      // ==========================================
      // SLIDE 10: EMPIRICAL THERMAL VALIDATION
      // ==========================================
      case 9:
        return (
          <div className="relative w-full h-full p-6 sm:p-10 flex flex-col justify-between select-none overflow-hidden">
            <div>
              <span className="font-mono text-xs font-bold text-teal-400 uppercase tracking-wider block mb-1">
                CHAPTER 08 • EXPERIMENTAL RESULTS
              </span>
              <h2 className="font-serif-display text-2xl sm:text-4xl font-bold text-white">
                Empirical Holding Time Validation: +52.8% Autonomy Extension
              </h2>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 my-auto items-center">
              
              {/* Thermal Curve Graph */}
              <div className={`p-4 rounded-2xl bg-slate-900/90 border border-slate-800 shadow-2xl transition-all duration-700 ${
                currentStep >= 0 ? 'opacity-100 scale-100' : 'opacity-20 scale-95'
              }`}>
                <img src="/assets/fig1_thermal_curves.png" alt="Thermal Curves" className="w-full h-auto rounded-xl filter contrast-125" />
              </div>

              {/* Verified Metrics */}
              <div className="space-y-4">
                
                <div className={`p-5 rounded-2xl bg-slate-900/90 border transition-all duration-500 ${
                  currentStep >= 1 ? 'border-teal-400 shadow-xl opacity-100 translate-x-0' : 'border-slate-800 opacity-20 translate-x-4'
                }`}>
                  <span className="font-mono text-4xl sm:text-5xl font-black text-[#2DD4BF] block mb-1">
                    109.4 Hours
                  </span>
                  <span className="font-mono text-xs text-teal-300 uppercase font-bold block">
                    Validated Hybrid Holding Autonomy
                  </span>
                  <p className="text-xs text-slate-300 mt-2 leading-relaxed">
                    Extended from 71.8 hours (passive-only baseline) to 109.4 hours in continuous +35°C mean tropical ambient, achieving <strong>+52.8% extension</strong> without adding ice.
                  </p>
                </div>

                <div className={`p-5 rounded-2xl bg-slate-900/90 border transition-all duration-500 delay-100 ${
                  currentStep >= 2 ? 'border-sky-400 shadow-xl opacity-100 translate-x-0' : 'border-slate-800 opacity-20 translate-x-4'
                }`}>
                  <span className="font-mono text-4xl sm:text-5xl font-black text-sky-400 block mb-1">
                    0.0%
                  </span>
                  <span className="font-mono text-xs text-sky-300 uppercase font-bold block">
                    Zero Freeze Events & Zero High Spikes
                  </span>
                  <p className="text-xs text-slate-300 mt-2 leading-relaxed">
                    Core temperature never fell below +2.8°C and never breached +6.4°C across all 109 hours of empirical logging, ensuring 100% WHO PQS compliance.
                  </p>
                </div>

              </div>

            </div>

            <div className="p-3 rounded-xl bg-slate-900 border border-slate-800 text-center font-mono text-xs text-slate-400">
              Audited in calibrated physics environmental testing chamber with 4-point Dallas DS18B20 digital probes.
            </div>
          </div>
        );

      // ==========================================
      // SLIDE 11: 3D CYLINDRICAL DEPLOYMENT HORIZONS
      // ==========================================
      case 10:
        return (
          <div className="relative w-full h-full p-4 sm:p-6 flex flex-col justify-between select-none overflow-hidden">
            <div className="flex items-center justify-between">
              <div>
                <span className="font-mono text-xs font-bold text-teal-400 uppercase tracking-wider block">
                  CHAPTER 09 • MICROCLIMATE STRESS-TESTING
                </span>
                <h2 className="font-serif-display text-xl sm:text-2xl font-bold text-white">
                  3D Cylindrical Horizon: Multi-Terrain Microclimate Validation
                </h2>
              </div>
              <span className="font-mono text-xs text-teal-400 bg-slate-900 px-3 py-1 rounded-lg border border-teal-500/30 font-bold">
                DRAG OR USE ARROWS TO ROTATE
              </span>
            </div>

            {/* Embedded Live 3D Curved Carousel */}
            <div className="flex-1 my-2 rounded-2xl overflow-hidden border border-slate-800 bg-[#050C16] relative flex items-center justify-center">
              <Curved3DCarousel isSlideMode={true} />
            </div>

            <div className="text-center font-mono text-xs text-slate-400">
              Validated in Thar Desert (+45°C), Ladakh (-14°C), Western Ghats Monsoon (98% RH), and Rural Tribal Hamlets.
            </div>
          </div>
        );

      // ==========================================
      // SLIDE 12: ECONOMIC ANALYSIS & PRODUCTION ECONOMICS
      // ==========================================
      case 11:
        return (
          <div className="relative w-full h-full p-6 sm:p-10 flex flex-col justify-between select-none overflow-hidden">
            <div>
              <span className="font-mono text-xs font-bold text-teal-400 uppercase tracking-wider block mb-1">
                CHAPTER 10 • PRODUCTION & HEALTHCARE ECONOMICS
              </span>
              <h2 className="font-serif-display text-2xl sm:text-4xl font-bold text-white">
                Economic Viability, Lifecycle TCO & Payback Analysis
              </h2>
            </div>

            <div className="my-auto max-w-4xl mx-auto w-full space-y-5">
              
              <div className={`space-y-1 transition-all duration-500 ${currentStep >= 0 ? 'opacity-100' : 'opacity-20'}`}>
                <div className="flex justify-between font-mono text-xs">
                  <span className="text-slate-300 font-bold">SANJIVANI Unit Capital Cost (Prototype BOM):</span>
                  <span className="text-[#2DD4BF] font-black text-sm">₹12,450 (Target Mass-Production: ₹8,900)</span>
                </div>
                <div className="w-full h-3 bg-slate-800 rounded-full overflow-hidden">
                  <div className="h-full bg-gradient-to-r from-teal-500 to-[#2DD4BF] rounded-full transition-all duration-1000" style={{ width: currentStep >= 0 ? '38%' : '0%' }} />
                </div>
                <span className="text-[10px] text-slate-400 font-mono block">63% lower cost than commercial active compressor portable coolers (₹35,000+).</span>
              </div>

              <div className={`space-y-1 transition-all duration-500 delay-100 ${currentStep >= 1 ? 'opacity-100' : 'opacity-20'}`}>
                <div className="flex justify-between font-mono text-xs">
                  <span className="text-slate-300 font-bold">10-Year Total Cost of Ownership (TCO):</span>
                  <span className="text-sky-300 font-black text-sm">₹28,400</span>
                </div>
                <div className="w-full h-3 bg-slate-800 rounded-full overflow-hidden">
                  <div className="h-full bg-gradient-to-r from-sky-500 to-teal-400 rounded-full transition-all duration-1000" style={{ width: currentStep >= 1 ? '45%' : '0%' }} />
                </div>
                <span className="text-[10px] text-slate-400 font-mono block">Includes replacement PCM refills, battery servicing, and maintenance.</span>
              </div>

              <div className={`space-y-1 transition-all duration-500 delay-200 ${currentStep >= 2 ? 'opacity-100' : 'opacity-20'}`}>
                <div className="flex justify-between font-mono text-xs">
                  <span className="text-slate-300 font-bold">Cumulative Vaccine Spoilage Losses Prevented:</span>
                  <span className="text-emerald-300 font-black text-sm">₹1,85,000 / PHC</span>
                </div>
                <div className="w-full h-3 bg-slate-800 rounded-full overflow-hidden">
                  <div className="h-full bg-gradient-to-r from-emerald-500 to-teal-300 rounded-full transition-all duration-1000" style={{ width: currentStep >= 2 ? '88%' : '0%' }} />
                </div>
                <span className="text-[10px] text-slate-400 font-mono block">Assumes 24 vials per trip × 50 trips/year × ₹150 average dose replacement cost.</span>
              </div>

              <div className={`space-y-1 transition-all duration-500 delay-300 ${currentStep >= 3 ? 'opacity-100' : 'opacity-20'}`}>
                <div className="flex justify-between font-mono text-xs">
                  <span className="text-slate-300 font-bold">Economic Payback Period:</span>
                  <span className="text-amber-300 font-black text-sm">1.4 Years</span>
                </div>
                <div className="w-full h-3 bg-slate-800 rounded-full overflow-hidden">
                  <div className="h-full bg-gradient-to-r from-amber-500 to-emerald-400 rounded-full transition-all duration-1000" style={{ width: currentStep >= 3 ? '22%' : '0%' }} />
                </div>
                <span className="text-[10px] text-slate-400 font-mono block">Rapid ROI achieved via zero vaccine waste and minimal operating power.</span>
              </div>

            </div>

            <div className="p-3 rounded-xl bg-teal-950/40 border border-teal-500/30 text-xs font-mono text-teal-200 text-center">
              Operating cost: ₹10.24 per operating hour | 2,500 units deployed across MP saves ₹4.62 Crores annually in wasted biologics.
            </div>
          </div>
        );

      // ==========================================
      // SLIDE 13: FMEA RELIABILITY & MAINTENANCE
      // ==========================================
      case 12:
        return (
          <div className="relative w-full h-full p-6 sm:p-10 flex flex-col justify-between select-none overflow-hidden">
            <div>
              <span className="font-mono text-xs font-bold text-teal-400 uppercase tracking-wider block mb-1">
                CHAPTER 11 • RELIABILITY ASSURANCE
              </span>
              <h2 className="font-serif-display text-2xl sm:text-4xl font-bold text-white">
                Scheduled Maintenance Protocol & FMEA Reliability Assurance
              </h2>
            </div>

            <div className="my-auto max-w-4xl mx-auto w-full grid grid-cols-1 sm:grid-cols-2 gap-4">
              
              <div className={`p-5 rounded-2xl bg-slate-900/90 border transition-all duration-500 ${
                currentStep >= 0 ? 'border-teal-500 shadow-lg opacity-100' : 'border-slate-800 opacity-20'
              }`}>
                <div className="flex items-center gap-2 mb-2">
                  <span className="w-2.5 h-2.5 rounded-full bg-teal-400" />
                  <span className="font-mono text-xs font-bold text-teal-300 uppercase">Quarterly Check (3 Months)</span>
                </div>
                <p className="text-xs text-slate-300 leading-relaxed">
                  Visual inspection of EPDM lid gasket seal integrity, check for dust fouling on heat sink fin stack, clean dual 80mm blower impellers, and verify battery state-of-health.
                </p>
              </div>

              <div className={`p-5 rounded-2xl bg-slate-900/90 border transition-all duration-500 delay-100 ${
                currentStep >= 1 ? 'border-sky-500 shadow-lg opacity-100' : 'border-slate-800 opacity-20'
              }`}>
                <div className="flex items-center gap-2 mb-2">
                  <span className="w-2.5 h-2.5 rounded-full bg-sky-400" />
                  <span className="font-mono text-xs font-bold text-sky-300 uppercase">Bi-Annual Service (6 Months)</span>
                </div>
                <p className="text-xs text-slate-300 leading-relaxed">
                  Re-calibrate 4-point Dallas DS18B20 digital temperature sensors against ice-point standard (0.0°C), verify thermal interface paste (TIM) conductance, inspect bio-PCM pouches.
                </p>
              </div>

              <div className={`p-5 rounded-2xl bg-slate-900/90 border transition-all duration-500 delay-200 ${
                currentStep >= 2 ? 'border-amber-500 shadow-lg opacity-100' : 'border-slate-800 opacity-20'
              }`}>
                <div className="flex items-center gap-2 mb-2">
                  <span className="w-2.5 h-2.5 rounded-full bg-amber-400" />
                  <span className="font-mono text-xs font-bold text-amber-300 uppercase">Annual Comprehensive Audit</span>
                </div>
                <p className="text-xs text-slate-300 leading-relaxed">
                  Full electrical stress test of MOSFET power switches, measure internal resistance of LiFePO4 battery pack, re-apply Arctic MX-4 thermal paste on Peltier ceramics.
                </p>
              </div>

              <div className={`p-5 rounded-2xl bg-slate-900/90 border transition-all duration-500 delay-300 ${
                currentStep >= 3 ? 'border-emerald-500 shadow-lg opacity-100' : 'border-slate-800 opacity-20'
              }`}>
                <div className="flex items-center gap-2 mb-2">
                  <span className="w-2.5 h-2.5 rounded-full bg-emerald-400" />
                  <span className="font-mono text-xs font-bold text-emerald-300 uppercase">10–12 Year Life Cycle Overhaul</span>
                </div>
                <p className="text-xs text-slate-300 leading-relaxed">
                  Replace LiFePO4 cells at 2,500 cycle mark; replace blower fans; vacuum insulation panels and structural LLDPE shell remain active for 20+ years.
                </p>
              </div>

            </div>

            <div className="p-3 rounded-xl bg-slate-900 border border-slate-800 text-center font-mono text-xs text-slate-400">
              FMEA RPN (Risk Priority Number) reduced from 288 (unmitigated thermal failure) down to 24 with fault-tolerant hysteresis.
            </div>
          </div>
        );

      // ==========================================
      // SLIDE 14: GRAND FINALE / CONCLUSION
      // ==========================================
      case 13:
        return (
          <div className="relative w-full h-full flex flex-col items-center justify-center p-6 sm:p-12 text-center select-none overflow-hidden bg-black">
            {/* Background Himalayan Transit Photo */}
            <div className="absolute inset-0 opacity-40">
              <img 
                src="/assets/photos/himalayan_transit.jpg" 
                alt="Transit" 
                className="w-full h-full object-cover filter brightness-50 contrast-125"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-black via-black/60 to-black/80" />
            </div>

            <div className="relative z-10 space-y-4 max-w-4xl">
              <span className="font-mono text-xs uppercase tracking-widest text-teal-400 font-bold block">
                SENIOR BALVIGYAN 2026–2027 • CONCLUSION & VISION
              </span>

              <h1 className="font-serif-display text-5xl sm:text-7xl md:text-8xl font-black text-white tracking-tight drop-shadow-2xl">
                SANJIVANI
              </h1>

              <div className="p-4 rounded-2xl bg-black/70 border border-slate-700/80 backdrop-blur-xl max-w-2xl mx-auto space-y-2">
                <p className="font-serif-display text-lg sm:text-xl text-teal-200 font-medium">
                  “Preserving Temperature. Protecting Life.”
                </p>
                <p className="text-xs sm:text-sm text-slate-300 leading-relaxed">
                  By synergizing solid-state thermoelectric physics with plant-based latent energy storage, SANJIVANI demonstrates that Indian school innovators can solve critical national logistics challenges and empower Viksit Bharat 2047.
                </p>
              </div>

              <div className="pt-4 flex items-center justify-center gap-3">
                <button
                  onClick={resetPresentation}
                  className="px-6 py-2.5 rounded-xl bg-teal-600 hover:bg-teal-500 text-white font-mono text-xs font-bold transition-all shadow-lg shadow-teal-700/50 flex items-center gap-2 cursor-pointer"
                >
                  <RotateCcw className="w-4 h-4" />
                  <span>REPLAY PRESENTATION</span>
                </button>
              </div>
            </div>
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <div 
      ref={deckContainerRef}
      className={`relative w-full bg-[#060B14] text-white overflow-hidden flex flex-col select-none ${
        isFullscreen ? 'fixed inset-0 z-50 h-screen' : 'rounded-3xl border border-slate-800 shadow-2xl h-[670px] sm:h-[740px]'
      }`}
    >
      {/* Top Deck Control Header Bar */}
      <header className="h-14 px-4 sm:px-6 bg-[#08111E]/95 border-b border-slate-800/90 flex items-center justify-between z-30 shrink-0 backdrop-blur-md">
        
        {/* Left: Branding & Slide Counter */}
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2">
            <span className="font-serif-display font-extrabold text-white text-base tracking-wide">
              SANJIVANI
            </span>
            <span className="font-devanagari text-teal-400 font-bold text-xs">संजीवनी</span>
          </div>

          <div className="hidden sm:flex items-center gap-1.5 font-mono text-xs font-bold text-teal-300 bg-teal-950/80 border border-teal-500/30 px-3 py-1 rounded-full">
            <span>SLIDE {activeConfig.chapterNumber}</span>
            <span className="text-slate-600">/</span>
            <span>{SLIDES_CONFIG.length.toString().padStart(2, '0')}</span>
          </div>

          <div className="hidden md:flex items-center gap-1 font-mono text-[11px] text-slate-400 bg-slate-900 px-2.5 py-0.5 rounded-md border border-slate-800">
            <span>STEP {currentStep + 1} OF {activeConfig.totalSteps}</span>
          </div>
        </div>

        {/* Center: Slide Title */}
        <div className="hidden lg:flex items-center gap-2 max-w-md truncate">
          <span className="font-serif-display text-sm font-bold text-slate-200 truncate">
            {activeConfig.title}
          </span>
          <span className="text-slate-600">•</span>
          <span className="text-xs font-sans-tech text-teal-400 truncate">
            {activeConfig.subtitle}
          </span>
        </div>

        {/* Right Action Toolbar */}
        <div className="flex items-center gap-2">
          
          {/* Download Official PPTX Deck */}
          <a
            href="/assets/SANJIVANI_Balvigyan_Keynote_Presentation.pptx"
            download="SANJIVANI_Balvigyan_Keynote_Presentation.pptx"
            onClick={() => sound.chime()}
            className="hidden sm:inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-gradient-to-r from-amber-500/20 to-teal-500/20 hover:from-amber-500/30 hover:to-teal-500/30 text-amber-300 border border-amber-500/40 text-xs font-mono font-bold transition-all shadow-md cursor-pointer"
            title="Download Official 16:9 Widescreen PowerPoint Presentation Deck"
          >
            <Download className="w-3.5 h-3.5 text-amber-400" />
            <span>PPTX DECK</span>
          </a>

          {/* Auto-Play Toggle with Countdown Ring */}
          <button
            onClick={() => {
              sound.click();
              setIsAutoPlaying(!isAutoPlaying);
            }}
            className={`relative px-3.5 py-1.5 rounded-xl font-mono text-xs font-bold transition-all flex items-center gap-2 cursor-pointer overflow-hidden ${
              isAutoPlaying 
                ? 'bg-amber-500 text-slate-950 shadow-lg shadow-amber-500/40 ring-2 ring-amber-400/50' 
                : 'bg-teal-600 hover:bg-teal-500 text-white shadow-md shadow-teal-900/40'
            }`}
            title="Auto-Play Presentation [P]"
          >
            {isAutoPlaying && (
              <div 
                className="absolute inset-0 bg-white/30 transition-all duration-75 pointer-events-none"
                style={{ width: `${autoPlayProgress}%` }}
              />
            )}
            <span className="relative z-10 flex items-center gap-1.5">
              {isAutoPlaying ? <Pause className="w-3.5 h-3.5 fill-current" /> : <Play className="w-3.5 h-3.5 fill-current" />}
              <span>{isAutoPlaying ? 'PAUSE' : 'AUTO-PLAY'}</span>
            </span>
          </button>

          {/* Slide Thumbnails Drawer */}
          <button
            onClick={() => {
              sound.click();
              setShowThumbnails(!showThumbnails);
            }}
            className={`p-2 rounded-xl border transition-colors cursor-pointer ${
              showThumbnails 
                ? 'bg-slate-800 text-teal-400 border-teal-500' 
                : 'bg-slate-900/80 text-slate-400 hover:text-white border-slate-800'
            }`}
            title="Slide Index"
          >
            <Layers className="w-4 h-4" />
          </button>

          {/* Sound Toggle */}
          <button
            onClick={toggleSound}
            className="p-2 rounded-xl bg-slate-900/80 text-slate-400 hover:text-white border border-slate-800 transition-colors cursor-pointer"
            title="Toggle Audio"
          >
            {isSoundMuted ? <VolumeX className="w-4 h-4" /> : <Volume2 className="w-4 h-4" />}
          </button>

          {/* Fullscreen Toggle */}
          <button
            onClick={toggleFullscreen}
            className="p-2 rounded-xl bg-slate-900/80 text-slate-400 hover:text-white border border-slate-800 transition-colors cursor-pointer"
            title="Toggle Fullscreen [F]"
          >
            {isFullscreen ? <Minimize2 className="w-4 h-4" /> : <Maximize2 className="w-4 h-4" />}
          </button>

        </div>

      </header>

      {/* Progress Strip */}
      <div className="w-full h-1 bg-slate-900 relative z-20">
        <div 
          className="h-full bg-gradient-to-r from-teal-500 via-[#2DD4BF] to-sky-400 transition-all duration-300"
          style={{ width: `${((currentSlide + (currentStep + 1) / activeConfig.totalSteps) / SLIDES_CONFIG.length) * 100}%` }}
        />
      </div>

      {/* Main Interactive Slide Stage (Click anywhere advances step!) */}
      <main 
        onClick={handleNextStep}
        className="flex-1 relative overflow-hidden cursor-pointer"
      >
        {renderSlideContent()}

        {/* Click Cue Overlay Helper in Bottom Center */}
        <div className="absolute bottom-3 left-1/2 -translate-x-1/2 z-20 px-3 py-1 rounded-full bg-black/60 border border-slate-800 text-[10px] font-mono text-slate-400 pointer-events-none backdrop-blur-md">
          CLICK ANYWHERE OR PRESS SPACE TO ADVANCE STEP
        </div>
      </main>

      {/* Slide Thumbnails Drawer Modal */}
      {showThumbnails && (
        <div className="absolute inset-x-0 bottom-14 z-40 bg-[#08111E]/95 border-t border-slate-800 p-4 max-h-72 overflow-y-auto backdrop-blur-xl animate-ppt-slide">
          <div className="flex items-center justify-between pb-2 mb-3 border-b border-slate-800">
            <span className="font-mono text-xs font-bold text-teal-400 uppercase tracking-wider">
              KEYNOTE SLIDE NAVIGATION (14 CHAPTERS)
            </span>
            <button 
              onClick={() => setShowThumbnails(false)} 
              className="font-mono text-xs text-slate-400 hover:text-white"
            >
              CLOSE [×]
            </button>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-4 md:grid-cols-6 lg:grid-cols-7 gap-2">
            {SLIDES_CONFIG.map((s, idx) => (
              <button
                key={s.id}
                onClick={(e) => {
                  e.stopPropagation();
                  jumpToSlide(idx);
                }}
                className={`p-2.5 rounded-xl border text-left transition-all cursor-pointer ${
                  currentSlide === idx 
                    ? 'bg-teal-950 border-teal-400 text-white shadow-lg shadow-teal-900/50' 
                    : 'bg-slate-900/80 border-slate-800 text-slate-400 hover:bg-slate-800 hover:text-slate-200'
                }`}
              >
                <span className="font-mono text-[10px] font-bold text-teal-400 block mb-0.5">
                  SLIDE {s.chapterNumber}
                </span>
                <span className="text-xs font-serif-display font-bold truncate block">
                  {s.title}
                </span>
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Bottom Keynote Navigation Bar */}
      <footer className="h-12 px-4 sm:px-6 bg-[#08111E] border-t border-slate-800/90 flex items-center justify-between shrink-0 z-30">
        
        {/* Previous Button */}
        <button
          onClick={(e) => {
            e.stopPropagation();
            handlePrevStep();
          }}
          disabled={currentSlide === 0 && currentStep === 0}
          className={`px-3 py-1.5 rounded-xl text-xs font-mono font-semibold flex items-center gap-1.5 border transition-all cursor-pointer ${
            currentSlide === 0 && currentStep === 0 
              ? 'opacity-25 border-transparent text-slate-600 cursor-not-allowed' 
              : 'bg-slate-900 hover:bg-slate-800 text-slate-200 border-slate-700'
          }`}
        >
          <ChevronLeft className="w-4 h-4" />
          <span>PREVIOUS</span>
        </button>

        {/* Step Indicator Bullets */}
        <div className="flex items-center gap-1.5">
          {Array.from({ length: activeConfig.totalSteps }).map((_, stepIdx) => (
            <button
              key={stepIdx}
              onClick={(e) => {
                e.stopPropagation();
                sound.click();
                setCurrentStep(stepIdx);
              }}
              className={`h-2 rounded-full transition-all duration-300 cursor-pointer ${
                stepIdx === currentStep 
                  ? 'w-6 bg-[#2DD4BF]' 
                  : stepIdx < currentStep 
                  ? 'w-2 bg-teal-700' 
                  : 'w-2 bg-slate-800 hover:bg-slate-700'
              }`}
              title={`Step ${stepIdx + 1}`}
            />
          ))}
        </div>

        {/* Next Button */}
        <button
          onClick={(e) => {
            e.stopPropagation();
            handleNextStep();
          }}
          className="px-4 py-1.5 rounded-xl text-xs font-mono font-bold bg-[#0F766E] hover:bg-teal-500 text-white transition-all shadow-md shadow-teal-950/50 flex items-center gap-1.5 cursor-pointer"
        >
          <span>{currentSlide === SLIDES_CONFIG.length - 1 && currentStep === activeConfig.totalSteps - 1 ? 'FINISH' : 'NEXT STEP'}</span>
          <ChevronRight className="w-4 h-4" />
        </button>

      </footer>

    </div>
  );
};
