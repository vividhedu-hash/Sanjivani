import React from 'react';
import { 
  TEAM_MEMBERS 
} from '../data/sanjivaniData';
import { 
  Sparkles, 
  ArrowUp, 
  Play, 
  Compass, 
  GraduationCap
} from 'lucide-react';
import { sound } from '../utils/soundEffects';

interface FutureTeamSectionProps {
  onRestartPresentation: () => void;
  onScrollToTop: () => void;
  onInspect3D: () => void;
  isSlideMode?: boolean;
}

export const FutureTeamSection: React.FC<FutureTeamSectionProps> = ({
  onRestartPresentation,
  onScrollToTop,
  onInspect3D,
  isSlideMode = false
}) => {
  const roadmapPhases = [
    {
      phase: "Phase 2",
      title: "Direct-Contact Vapor Chambers",
      timeline: "Q2 2027",
      desc: "Replace standard copper spreading blocks with sintered two-phase microchannel vapor chambers to reduce cold-side thermal resistance to R_th < 0.08 K/W."
    },
    {
      phase: "Phase 3",
      title: "Solar PV Energy Harvesting",
      timeline: "Q4 2027",
      desc: "Integrate 40W flexible monocrystalline solar PV cells into the exterior lid with maximum power point tracking (MPPT) for multi-week off-grid autonomy."
    },
    {
      phase: "Phase 4",
      title: "WHO PQS Formal Certification",
      timeline: "2028",
      desc: "Subject prototype to ISO 17025 accredited laboratory testing under WHO/PQS/E004/CB01.3 thermal cold box standards."
    },
    {
      phase: "Phase 5",
      title: "Cellular IoT & GPS Telemetry",
      timeline: "2028",
      desc: "Deploy NB-IoT / LTE-M modules with GPS geofencing and cloud MQTT logging to alert district immunization officers in real time."
    }
  ];

  return (
    <div className={`w-full bg-white rounded-2xl border border-slate-200 shadow-xl ${
      isSlideMode ? 'p-4 md:p-6' : 'p-6 md:p-10'
    }`}>
      
      {/* Chapter Tag & Headline */}
      <div className="max-w-3xl">
        <div className="flex items-center gap-2">
          <span className="px-2.5 py-0.5 rounded text-[11px] font-mono uppercase bg-teal-50 text-[#0F766E] border border-teal-200 font-bold">
            Chapter 10 • Future Roadmap & Team
          </span>
          <span className="text-xs font-mono text-slate-500">
            STEM for Viksit Bharat
          </span>
        </div>
        <h2 className={`font-serif-display font-bold text-[#0B2545] mt-1.5 leading-tight ${
          isSlideMode ? 'text-2xl sm:text-3xl' : 'text-3xl sm:text-4xl md:text-5xl'
        }`}>
          A better cold chain begins with better engineering.
        </h2>
        <p className="text-slate-600 text-xs sm:text-sm mt-1.5 leading-relaxed">
          SANJIVANI is envisioned not as an isolated classroom project, but as an ongoing student research initiative aimed at developing frugal, deployable medical hardware for the last mile of Indian healthcare.
        </p>
      </div>

      {/* Engineering Roadmap Timeline */}
      <div className={isSlideMode ? 'mt-4' : 'mt-8'}>
        <h3 className="font-serif-display text-lg sm:text-xl font-bold text-[#0B2545] mb-3">
          Future Development Roadmap
        </h3>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
          {roadmapPhases.map((r, i) => (
            <div key={i} className="p-3.5 rounded-xl bg-slate-50 border border-slate-200 flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between text-xs font-mono">
                  <span className="text-[#0F766E] font-bold">{r.phase}</span>
                  <span className="text-slate-500">{r.timeline}</span>
                </div>
                <h4 className="font-bold text-[#0B2545] text-sm mt-1.5">
                  {r.title}
                </h4>
                <p className="text-xs text-slate-600 mt-1 leading-relaxed">
                  {r.desc}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Research Team Profiles */}
      <div className={`pt-6 border-t border-slate-200 ${isSlideMode ? 'mt-6' : 'mt-10'}`}>
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-4">
          <div>
            <h3 className="font-serif-display text-lg sm:text-xl font-bold text-[#0B2545]">
              Student Investigators & Mentorship
            </h3>
            <span className="text-xs font-mono text-slate-500">
              G. D. Goenka Public School, Indore (M.P.), India
            </span>
          </div>

          <div className="flex items-center gap-1.5 text-xs font-mono text-[#0F766E] bg-teal-50 px-3 py-1 rounded-lg border border-teal-200 font-bold">
            <GraduationCap className="w-4 h-4 text-[#0F766E]" />
            <span>Senior Bal Vigyan 2026–2027</span>
          </div>
        </div>

        {/* 4 Students Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
          {TEAM_MEMBERS.map((m, i) => (
            <div key={i} className="p-4 rounded-xl bg-white border border-slate-200 hover:border-teal-400 transition-all shadow-sm flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between">
                  <span className="text-[10px] font-mono text-[#0F766E] uppercase font-bold">
                    {m.grade}
                  </span>
                  <span className="w-2 h-2 rounded-full bg-[#0F766E]"></span>
                </div>
                <h4 className="font-bold text-[#0B2545] text-sm sm:text-base mt-1.5">
                  {m.name}
                </h4>
                <span className="text-xs font-mono text-slate-500 block mt-0.5">
                  {m.role}
                </span>
                <p className="text-xs text-slate-600 mt-2 leading-relaxed">
                  {m.contribution}
                </p>
              </div>
            </div>
          ))}
        </div>

        {/* Mentor Card */}
        <div className="mt-4 p-4 rounded-xl bg-slate-50 border border-slate-200 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
          <div className="flex items-center gap-3">
            <div className="w-11 h-11 rounded-xl bg-gradient-to-br from-[#0B2545] to-[#0F766E] flex items-center justify-center text-white font-bold text-base font-mono shadow-sm">
              GK
            </div>
            <div>
              <span className="text-[10px] font-mono uppercase text-slate-500 tracking-wider font-semibold">
                PROJECT MENTOR & RESEARCH GUIDE
              </span>
              <h4 className="font-bold text-[#0B2545] text-base mt-0.5">
                Mr. Gopal Kumar Roy
              </h4>
              <p className="text-xs text-slate-600">
                PGT Physics • Department of Science, G. D. Goenka Public School, Indore
              </p>
            </div>
          </div>

          <div className="text-left sm:text-right font-mono text-xs text-slate-600">
            <div>Competition Code: <strong className="text-[#0F766E]">SBVPH-05</strong></div>
            <div>Category: <strong className="text-[#0B2545]">Physics / Thermal Engineering</strong></div>
          </div>
        </div>
      </div>

      {/* Final Memorable Climax & Replay CTAs */}
      <div className={`rounded-2xl bg-gradient-to-b from-[#0B2545] via-[#101C2C] to-[#0B2545] text-white text-center shadow-xl ${
        isSlideMode ? 'mt-6 p-6' : 'mt-10 p-8 sm:p-12'
      }`}>
        <div className="flex justify-center mb-2.5">
          <span className="px-3 py-0.5 rounded-full text-xs font-mono uppercase bg-teal-950 text-teal-300 border border-teal-700/60 flex items-center gap-1.5 font-bold">
            <Sparkles className="w-3.5 h-3.5" />
            Closing Affirmation
          </span>
        </div>

        <h2 className="font-serif-display text-3xl sm:text-5xl font-bold text-white tracking-tight">
          SANJIVANI
        </h2>
        <span className="font-devanagari text-2xl sm:text-3xl text-teal-300 font-bold block mt-1">
          संजीवनी
        </span>

        <p className="font-serif-display italic text-base sm:text-xl text-slate-200 mt-2 font-normal">
          “Preserving Temperature. Protecting Life.”
        </p>

        {/* Final Statement */}
        <p className="mt-3 max-w-2xl mx-auto font-serif-display text-sm sm:text-base text-teal-100/90 italic leading-relaxed">
          “Our goal is not simply to make a box colder. It is to engineer a more resilient way of protecting temperature-sensitive medical supplies.”
        </p>

        {/* Final Navigation Controls */}
        <div className="mt-6 flex flex-wrap items-center justify-center gap-3">
          <button
            onClick={() => { sound.click(); onRestartPresentation(); }}
            className="px-5 py-2.5 rounded-xl font-mono text-xs uppercase tracking-wider font-bold bg-[#0F766E] hover:bg-[#0D655E] text-white shadow-lg shadow-[#0F766E]/40 transition-all flex items-center gap-2 cursor-pointer"
          >
            <Play className="w-4 h-4 fill-white" />
            <span>Replay Presentation Mode</span>
          </button>

          <button
            onClick={() => { sound.click(); onInspect3D(); }}
            className="px-5 py-2.5 rounded-xl font-mono text-xs uppercase tracking-wider font-semibold bg-white/10 hover:bg-white/20 text-white border border-white/20 transition-all flex items-center gap-2 cursor-pointer"
          >
            <Compass className="w-4 h-4 text-teal-300" />
            <span>Inspect 3D Enclosure</span>
          </button>

          {!isSlideMode && (
            <button
              onClick={() => { sound.click(); onScrollToTop(); }}
              className="p-2.5 rounded-xl bg-white/10 hover:bg-white/20 text-white border border-white/20 transition-all cursor-pointer"
              title="Return to top"
            >
              <ArrowUp className="w-4 h-4" />
            </button>
          )}
        </div>

      </div>

    </div>
  );
};
