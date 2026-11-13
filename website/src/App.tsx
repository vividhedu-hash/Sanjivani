import React, { useState, useEffect, useRef } from 'react';
import { Navbar } from './components/Navbar';
import { OpeningCinematic } from './components/OpeningCinematic';
import { ProblemSection } from './components/ProblemSection';
import { BigIdeaSection } from './components/BigIdeaSection';
import { Model3DViewer } from './components/Model3DViewer';
import { SystemThinkingSection } from './components/SystemThinkingSection';
import { ScienceBehindSection } from './components/ScienceBehindSection';
import { NumbersDashboard } from './components/NumbersDashboard';
import { ImpactSection } from './components/ImpactSection';
import { TestingValidationSection } from './components/TestingValidationSection';
import { FutureTeamSection } from './components/FutureTeamSection';
import { PresentationModal } from './components/PresentationModal';
import { OrbitalRadarHUD } from './components/OrbitalRadarHUD';
import { Curved3DCarousel } from './components/Curved3DCarousel';
import { KeynotePresentationDeck } from './components/KeynotePresentationDeck';
import { sound } from './utils/soundEffects';
import { CHAPTERS } from './data/sanjivaniData';

export const App: React.FC = () => {
  const [activeChapter, setActiveChapter] = useState<number>(1);
  const [isPresentationOpen, setIsPresentationOpen] = useState<boolean>(false);
  const [isAudioActive, setIsAudioActive] = useState<boolean>(false);

  // Section references for scroll tracking
  const sectionRefs = useRef<{ [id: number]: HTMLElement | null }>({});

  // Scroll listener to update active chapter indicator in Navbar
  useEffect(() => {
    const handleScroll = () => {
      const scrollY = window.scrollY + 200;
      for (let i = CHAPTERS.length; i >= 1; i--) {
        const el = sectionRefs.current[i];
        if (el && el.offsetTop <= scrollY) {
          setActiveChapter(i);
          break;
        }
      }
    };

    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const scrollToChapter = (chapterId: number) => {
    const el = sectionRefs.current[chapterId];
    if (el) {
      el.scrollIntoView({ behavior: 'smooth' });
    }
  };

  const toggleSound = () => {
    const nextState = !isAudioActive;
    setIsAudioActive(nextState);
    sound.setMuted(!nextState);
    if (nextState) {
      sound.startAmbientHum();
      sound.chime();
    }
  };

  // Render individual chapter contents for presentation mode
  const renderChapterSlide = (chapterId: number) => {
    switch (chapterId) {
      case 1:
        return (
          <OpeningCinematic 
            onExplore={() => scrollToChapter(2)} 
            onEnterPresentation={() => setIsPresentationOpen(true)} 
            isSlideMode={true}
          />
        );
      case 2:
        return <ProblemSection isSlideMode={true} />;
      case 3:
        return <BigIdeaSection isSlideMode={true} />;
      case 4:
        return (
          <div className="space-y-2">
            <div className="text-center mb-1">
              <span className="text-[10px] font-mono text-teal-400 uppercase tracking-widest font-bold">
                HERO ENGINEERING CUTAWAY
              </span>
              <h2 className="font-serif-display text-2xl sm:text-3xl font-bold text-white mt-0.5">
                Explore The 3D System Architecture
              </h2>
            </div>
            <Model3DViewer isSlideMode={true} />
          </div>
        );
      case 5:
        return (
          <div className="space-y-4">
            <div className="text-center mb-1">
              <span className="text-[10px] font-mono text-teal-400 uppercase tracking-widest font-bold">
                ORBITAL CLOSED-LOOP ARCHITECTURE
              </span>
              <h2 className="font-serif-display text-2xl sm:text-3xl font-bold text-white mt-0.5">
                Quad-Subsystem Closed-Loop Radar HUD
              </h2>
            </div>
            <OrbitalRadarHUD isSlideMode={true} />
            <div className="mt-4">
              <SystemThinkingSection isSlideMode={true} />
            </div>
          </div>
        );
      case 6:
        return <ScienceBehindSection isSlideMode={true} />;
      case 7:
        return <NumbersDashboard isSlideMode={true} />;
      case 8:
        return (
          <div className="space-y-4">
            <div className="text-center mb-1">
              <span className="text-[10px] font-mono text-teal-400 uppercase tracking-widest font-bold">
                3D CYLINDRICAL DEPLOYMENT HORIZONS
              </span>
              <h2 className="font-serif-display text-2xl sm:text-3xl font-bold text-white mt-0.5">
                Stress-Testing Across India's Microclimates
              </h2>
            </div>
            <Curved3DCarousel isSlideMode={true} />
            <div className="mt-4">
              <ImpactSection isSlideMode={true} />
            </div>
          </div>
        );
      case 9:
        return <TestingValidationSection isSlideMode={true} />;
      case 10:
        return (
          <FutureTeamSection
            onRestartPresentation={() => {
              setActiveChapter(1);
            }}
            onScrollToTop={() => {
              window.scrollTo({ top: 0, behavior: 'smooth' });
            }}
            onInspect3D={() => {
              scrollToChapter(4);
            }}
            isSlideMode={true}
          />
        );
      default:
        return <OpeningCinematic onExplore={() => {}} onEnterPresentation={() => {}} isSlideMode={true} />;
    }
  };

  return (
    <div className="min-h-screen bg-[#060B14] text-slate-100 selection:bg-teal-500 selection:text-white relative">
      
      {/* Sticky Global Navigation */}
      <Navbar
        currentActiveChapter={activeChapter}
        onSelectChapter={scrollToChapter}
        onEnterPresentation={() => {
          setIsPresentationOpen(true);
        }}
        onToggleSound={toggleSound}
        isAudioActive={isAudioActive}
      />

      {/* Main Continuous Single-Page Presentation Experience */}
      <main className="w-full overflow-x-hidden pt-16 space-y-16 sm:space-y-24 pb-24">
        
        {/* Chapter 01: The Opening */}
        <section 
          id="chapter-01" 
          ref={el => { sectionRefs.current[1] = el; }}
          className="w-full scroll-mt-20"
        >
          <OpeningCinematic 
            onExplore={() => scrollToChapter(2)}
            onEnterPresentation={() => setIsPresentationOpen(true)}
          />
        </section>

        {/* Featured Keynote Pitch Deck Section (Auto-Click Step Presentation) */}
        <section className="max-w-7xl mx-auto px-4 sm:px-6">
          <div className="mb-4 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 bg-gradient-to-r from-[#08111E] via-[#0B1526] to-[#08111E] p-4 sm:p-5 rounded-2xl border border-teal-500/40 shadow-2xl backdrop-blur-xl">
            <div>
              <div className="flex items-center gap-2">
                <span className="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-ping" />
                <span className="font-mono text-xs uppercase tracking-wider text-teal-300 font-bold">
                  AUTOCLICK KEYNOTE PRESENTATION • 14 CHAPTERS
                </span>
              </div>
              <h2 className="font-serif-display text-xl sm:text-2xl font-bold text-white mt-1">
                Interactive Balvigyan Presentation Deck
              </h2>
              <p className="text-xs text-slate-400 mt-0.5">
                Click anywhere on the slide canvas or hit <kbd className="px-1.5 py-0.5 rounded bg-slate-800 text-teal-300 font-mono text-[10px]">Space</kbd> / <kbd className="px-1.5 py-0.5 rounded bg-slate-800 text-teal-300 font-mono text-[10px]">→</kbd> to step through animations, or press <strong className="text-amber-400">AUTO-PLAY</strong> to watch like a video!
              </p>
            </div>
            <button
              onClick={() => setIsPresentationOpen(true)}
              className="px-4 py-2 rounded-xl bg-teal-600 hover:bg-teal-500 text-white font-mono text-xs font-bold transition-all shadow-lg shadow-teal-950/60 flex items-center gap-2 cursor-pointer shrink-0"
            >
              <span>FULLSCREEN KEYNOTE</span>
            </button>
          </div>

          <KeynotePresentationDeck />
        </section>

        <div className="max-w-7xl mx-auto px-4 sm:px-6 space-y-20 sm:space-y-28">
          
          {/* Chapter 02: The Problem */}
          <section 
            id="chapter-02" 
            ref={el => { sectionRefs.current[2] = el; }}
            className="w-full scroll-mt-24"
          >
            <ProblemSection />
          </section>

          {/* Chapter 03: The Big Idea */}
          <section 
            id="chapter-03" 
            ref={el => { sectionRefs.current[3] = el; }}
            className="w-full scroll-mt-24"
          >
            <BigIdeaSection />
          </section>

          {/* Chapter 04: Explore The Engineering (HERO 3D CUTAWAY) */}
          <section 
            id="chapter-04" 
            ref={el => { sectionRefs.current[4] = el; }}
            className="w-full scroll-mt-24 space-y-4"
          >
            <div className="max-w-3xl mb-2">
              <div className="flex items-center gap-2">
                <span className="px-2.5 py-0.5 rounded text-[11px] font-mono uppercase bg-teal-950 text-teal-300 border border-teal-500/40 font-bold">
                  Chapter 04 • The Visual Hero
                </span>
                <span className="text-xs font-mono text-teal-400">
                  Interactive 3D Cutaway System & Exploded View
                </span>
              </div>
              <h2 className="font-serif-display text-3xl sm:text-4xl md:text-5xl font-bold text-white mt-2 leading-tight">
                Explore the engineering.
              </h2>
              <p className="text-slate-400 text-sm sm:text-base mt-2">
                Rotate, slice, and explode the 13 integrated subsystems of SANJIVANI with the interactive exploded view slider. Observe the cold-side extraction pathway, closed liquid loop, and forced ambient heat dissipation.
              </p>
            </div>

            <Model3DViewer />
          </section>

          {/* Chapter 05: How The System Thinks */}
          <section 
            id="chapter-05" 
            ref={el => { sectionRefs.current[5] = el; }}
            className="w-full scroll-mt-24 space-y-6"
          >
            <div className="max-w-3xl mb-2">
              <div className="flex items-center gap-2">
                <span className="px-2.5 py-0.5 rounded text-[11px] font-mono uppercase bg-teal-950 text-teal-300 border border-teal-500/40 font-bold">
                  Chapter 05 • System Dynamics
                </span>
                <span className="text-xs font-mono text-teal-400">
                  Quad-Subsystem Closed-Loop Telemetry
                </span>
              </div>
              <h2 className="font-serif-display text-3xl sm:text-4xl md:text-5xl font-bold text-white mt-2 leading-tight">
                How the system thinks.
              </h2>
              <p className="text-slate-400 text-sm sm:text-base mt-2">
                Interactive 360° orbital telemetry radar coordinating solid-state thermoelectric heat pumping, latent bio-PCM isothermal buffering, digital hysteresis polling, and LiFePO4 battery power.
              </p>
            </div>

            <OrbitalRadarHUD />
            <SystemThinkingSection />
          </section>

          {/* Chapter 06: The Science Behind It */}
          <section 
            id="chapter-06" 
            ref={el => { sectionRefs.current[6] = el; }}
            className="w-full scroll-mt-24"
          >
            <ScienceBehindSection />
          </section>

          {/* Chapter 07: The Numbers */}
          <section 
            id="chapter-07" 
            ref={el => { sectionRefs.current[7] = el; }}
            className="w-full scroll-mt-24"
          >
            <NumbersDashboard />
          </section>

          {/* Chapter 08: Economic and Social Impact */}
          <section 
            id="chapter-08" 
            ref={el => { sectionRefs.current[8] = el; }}
            className="w-full scroll-mt-24 space-y-6"
          >
            <div className="max-w-3xl mb-2">
              <div className="flex items-center gap-2">
                <span className="px-2.5 py-0.5 rounded text-[11px] font-mono uppercase bg-teal-950 text-teal-300 border border-teal-500/40 font-bold">
                  Chapter 08 • Field Deployment Horizons
                </span>
                <span className="text-xs font-mono text-teal-400">
                  3D Cylindrical Microclimate Stress-Testing
                </span>
              </div>
              <h2 className="font-serif-display text-3xl sm:text-4xl md:text-5xl font-bold text-white mt-2 leading-tight">
                Real-world impact across India.
              </h2>
              <p className="text-slate-400 text-sm sm:text-base mt-2">
                Spin through our cylindrical 3D deployment horizons—from the 45°C Thar Desert heatwaves to -14°C Himalayan passes and monsoonal rural outreach.
              </p>
            </div>

            <Curved3DCarousel />
            <ImpactSection />
          </section>

          {/* Chapter 09: Testing and Validation */}
          <section 
            id="chapter-09" 
            ref={el => { sectionRefs.current[9] = el; }}
            className="w-full scroll-mt-24"
          >
            <TestingValidationSection />
          </section>

          {/* Chapter 10: The Future and The Team */}
          <section 
            id="chapter-10" 
            ref={el => { sectionRefs.current[10] = el; }}
            className="w-full scroll-mt-24"
          >
            <FutureTeamSection
              onRestartPresentation={() => {
                setIsPresentationOpen(true);
              }}
              onScrollToTop={() => {
                window.scrollTo({ top: 0, behavior: 'smooth' });
              }}
              onInspect3D={() => {
                scrollToChapter(4);
              }}
            />
          </section>

        </div>
      </main>

      {/* Global Presentation Mode Keynote Overlay */}
      <PresentationModal
        isOpen={isPresentationOpen}
        onClose={() => setIsPresentationOpen(false)}
        initialChapter={activeChapter}
        renderChapterContent={renderChapterSlide}
      />

    </div>
  );
};

export default App;
