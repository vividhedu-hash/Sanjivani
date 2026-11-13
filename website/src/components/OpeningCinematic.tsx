import React, { useEffect, useRef, useState } from 'react';
import { 
  ArrowRight, 
  Volume2, 
  VolumeX, 
  Play, 
  ShieldCheck, 
  Thermometer, 
  Award,
  Sparkles
} from 'lucide-react';
import { sound } from '../utils/soundEffects';

interface OpeningCinematicProps {
  onExplore: () => void;
  onEnterPresentation: () => void;
  isSlideMode?: boolean;
}

export const OpeningCinematic: React.FC<OpeningCinematicProps> = ({ 
  onExplore, 
  onEnterPresentation,
  isSlideMode = false
}) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [isAudioActive, setIsAudioActive] = useState<boolean>(false);
  const [stage, setStage] = useState<number>(0);

  useEffect(() => {
    const t1 = setTimeout(() => setStage(1), 300);
    const t2 = setTimeout(() => setStage(2), 800);
    const t3 = setTimeout(() => setStage(3), 1400);

    return () => {
      clearTimeout(t1);
      clearTimeout(t2);
      clearTimeout(t3);
    };
  }, []);

  // Temperature Waveform Canvas Animation for Dark Mode
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let animId: number;
    let offset = 0;

    const render = () => {
      animId = requestAnimationFrame(render);
      const w = canvas.width = canvas.parentElement?.clientWidth || 800;
      const h = canvas.height = isSlideMode ? 100 : 130;

      ctx.clearRect(0, 0, w, h);

      // Safe Corridor Background Band (+2°C to +8°C equivalent)
      const topSafe = h * 0.22;
      const bottomSafe = h * 0.78;
      ctx.fillStyle = 'rgba(20, 184, 166, 0.08)';
      ctx.fillRect(0, topSafe, w, bottomSafe - topSafe);

      // Guidelines
      ctx.strokeStyle = 'rgba(20, 184, 166, 0.35)';
      ctx.lineWidth = 1;
      ctx.setLineDash([4, 4]);
      ctx.beginPath();
      ctx.moveTo(0, topSafe);
      ctx.lineTo(w, topSafe);
      ctx.moveTo(0, bottomSafe);
      ctx.lineTo(w, bottomSafe);
      ctx.stroke();
      ctx.setLineDash([]);

      // Dynamic Temperature Waveform
      offset += 0.025;
      ctx.beginPath();
      ctx.strokeStyle = '#2DD4BF'; // Vivid Medical Teal Glow
      ctx.lineWidth = 2.4;
      ctx.shadowColor = '#2DD4BF';
      ctx.shadowBlur = 10;

      for (let x = 0; x < w; x++) {
        const y = (topSafe + bottomSafe) / 2 + Math.sin(x * 0.015 + offset) * 16 + Math.cos(x * 0.035 - offset * 0.7) * 7;
        if (x === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      }
      ctx.stroke();
      ctx.shadowBlur = 0; // reset

      // Pulsing Telemetry Blip
      const blipX = (w * 0.65 + offset * 45) % w;
      const blipY = (topSafe + bottomSafe) / 2 + Math.sin(blipX * 0.015 + offset) * 16 + Math.cos(blipX * 0.035 - offset * 0.7) * 7;
      
      ctx.fillStyle = '#2DD4BF';
      ctx.beginPath();
      ctx.arc(blipX, blipY, 4, 0, Math.PI * 2);
      ctx.fill();

      // Blip pulse ring
      ctx.strokeStyle = 'rgba(45, 212, 191, 0.6)';
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      ctx.arc(blipX, blipY, 8 + Math.sin(offset * 5) * 3, 0, Math.PI * 2);
      ctx.stroke();
    };

    render();
    return () => cancelAnimationFrame(animId);
  }, [isSlideMode]);

  const toggleSound = () => {
    const nextState = !isAudioActive;
    setIsAudioActive(nextState);
    sound.setMuted(!nextState);
    if (nextState) {
      sound.startAmbientHum();
      sound.chime();
    }
  };

  return (
    <section className={`relative w-full flex flex-col items-center justify-center overflow-hidden px-4 bg-radial-glow ${
      isSlideMode ? 'py-4 min-h-[460px]' : 'py-12 min-h-[85vh]'
    }`}>
      
      {/* Sci-Fi Tech Grid */}
      <div className="absolute inset-0 bg-tech-grid-dark pointer-events-none" />

      {/* Competition & School Accreditation Badge */}
      <div className={`transition-all duration-700 transform ${
        stage >= 1 ? 'opacity-100 translate-y-0' : 'opacity-0 -translate-y-4'
      } z-10 flex flex-wrap items-center justify-center gap-2 mb-4`}>
        <div className="flex items-center gap-2 bg-slate-900/90 border border-slate-800 px-3.5 py-1.5 rounded-full shadow-lg text-xs font-mono text-slate-300">
          <Award className="w-3.5 h-3.5 text-amber-400" />
          <span className="font-bold text-white">Dr. B. K. Passi Memorial Senior Balvigyan 2026–2027</span>
          <span className="text-slate-600">•</span>
          <span className="text-teal-400 font-bold">Physics</span>
        </div>
        <div className="hidden sm:flex items-center gap-1.5 bg-teal-950/80 border border-teal-500/30 px-3 py-1.5 rounded-full text-[11px] font-mono text-teal-300 font-semibold shadow-lg">
          <ShieldCheck className="w-3 h-3 text-teal-400" />
          <span>STEM for Viksit and Atmanirbhar Bharat</span>
        </div>
      </div>

      {/* Laser Waveform Line Transition */}
      <div className={`w-full max-w-4xl h-[1.5px] bg-gradient-to-r from-transparent via-[#2DD4BF] to-transparent transition-all duration-700 ${
        stage >= 1 ? 'opacity-90 scale-x-100' : 'opacity-0 scale-x-0'
      }`} />

      {/* Temperature Waveform Display */}
      <div className={`w-full max-w-4xl my-2 transition-all duration-700 ${
        stage >= 1 ? 'opacity-100' : 'opacity-0'
      }`}>
        <canvas ref={canvasRef} className={`w-full block ${isSlideMode ? 'h-[75px]' : 'h-[95px]'}`} />
        <div className="flex justify-between text-[11px] font-mono text-slate-400 px-2 -mt-3">
          <span className="flex items-center gap-1 text-teal-400 font-bold">
            <Thermometer className="w-3 h-3" /> Core: +4.6°C Stable
          </span>
          <span>WHO PQS Safe Corridor (+2.0°C to +8.0°C)</span>
          <span className="text-cyan-400 font-semibold">Isothermal Latent Hold</span>
        </div>
      </div>

      {/* Title & Brand Messaging */}
      <div className={`text-center max-w-4xl z-10 transition-all duration-700 transform ${
        stage >= 3 ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'
      }`}>
        
        {/* Brand Name */}
        <div className="flex flex-col sm:flex-row items-center justify-center gap-3 sm:gap-5 my-1">
          <h1 className="font-serif-display text-5xl sm:text-7xl lg:text-8xl font-black tracking-tight text-white drop-shadow-2xl">
            SANJIVANI
          </h1>
          <span className="font-devanagari text-3xl sm:text-5xl text-[#2DD4BF] font-bold tracking-wide">
            संजीवनी
          </span>
        </div>

        {/* Tagline */}
        <p className="font-serif-display italic text-xl sm:text-2xl text-slate-300 mt-1 tracking-wide font-normal">
          “Preserving Temperature. Protecting Life.”
        </p>

        {/* Subtitle */}
        <div className="mt-3 max-w-2xl mx-auto space-y-1.5">
          <p className="text-xs sm:text-sm font-sans-tech font-bold text-teal-400 uppercase tracking-widest">
            Hybrid PCM–Peltier Medical Cold-Chain System
          </p>
          <p className="text-xs sm:text-sm text-slate-400 font-sans-tech leading-relaxed">
            Design and Development of a Sensor-Triggered Hybrid PCM–Peltier Cooling System for Extended Medical Cold-Chain Storage. An exploration of intelligent thermal management for resilient off-grid vaccine logistics.
          </p>
        </div>

        {/* Institution Attribution Strip */}
        <div className="mt-5 flex flex-wrap items-center justify-center gap-x-4 gap-y-1 text-xs font-mono text-slate-400 border-t border-b border-slate-800 py-2.5 max-w-xl mx-auto bg-slate-900/60 rounded-xl">
          <span className="font-semibold text-slate-200">G. D. Goenka Public School, Indore</span>
          <span>•</span>
          <span>Mentor: Mr. Gopal Kumar Roy</span>
          <span>•</span>
          <span className="text-teal-400 font-bold">UID: SBVPH-05</span>
        </div>

        {/* CTA Controls */}
        {!isSlideMode && (
          <div className="mt-7 flex flex-wrap items-center justify-center gap-3">
            <button
              onClick={() => { sound.click(); onExplore(); }}
              className="group px-7 py-3 rounded-xl font-mono text-xs uppercase tracking-wider font-bold bg-teal-600 hover:bg-teal-500 text-white shadow-xl shadow-teal-900/50 transition-all flex items-center gap-2.5 cursor-pointer"
            >
              <span>EXPLORE KEYNOTE & SYSTEM</span>
              <ArrowRight className="w-4 h-4 group-hover:translate-x-1.5 transition-transform" />
            </button>

            <button
              onClick={() => { sound.click(); onEnterPresentation(); }}
              className="px-6 py-3 rounded-xl font-mono text-xs uppercase tracking-wider font-bold bg-slate-900/90 hover:bg-slate-800 text-teal-300 border border-teal-500/40 shadow-lg transition-all flex items-center gap-2 cursor-pointer"
            >
              <Play className="w-3.5 h-3.5 fill-teal-400 text-teal-400" />
              <span>Fullscreen Deck</span>
            </button>

            <button
              onClick={toggleSound}
              className={`p-3 rounded-xl border transition-all cursor-pointer ${
                isAudioActive 
                  ? 'bg-teal-950/80 border-teal-500/40 text-teal-300 shadow-md' 
                  : 'bg-slate-900/80 border-slate-800 text-slate-400 hover:text-white'
              }`}
              title={isAudioActive ? 'Sound FX Active (Click to mute)' : 'Enable Sound FX & Ambience'}
            >
              {isAudioActive ? <Volume2 className="w-4 h-4" /> : <VolumeX className="w-4 h-4" />}
            </button>
          </div>
        )}

      </div>

    </section>
  );
};
