import React, { useState, useEffect } from 'react';
import { 
  Play, 
  Volume2, 
  VolumeX, 
  Maximize, 
  Minimize, 
  List,
  Sparkles,
  Download
} from 'lucide-react';
import { sound } from '../utils/soundEffects';
import { CHAPTERS } from '../data/sanjivaniData';

interface NavbarProps {
  currentActiveChapter: number;
  onSelectChapter: (chapterId: number) => void;
  onEnterPresentation: () => void;
  onToggleSound: () => void;
  isAudioActive: boolean;
}

export const Navbar: React.FC<NavbarProps> = ({
  currentActiveChapter,
  onSelectChapter,
  onEnterPresentation,
  onToggleSound,
  isAudioActive
}) => {
  const [isScrolled, setIsScrolled] = useState<boolean>(false);
  const [showNavMenu, setShowNavMenu] = useState<boolean>(false);
  const [isFullscreen, setIsFullscreen] = useState<boolean>(false);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 30);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const toggleFullscreen = () => {
    sound.click();
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen().then(() => setIsFullscreen(true)).catch(() => {});
    } else {
      document.exitFullscreen().then(() => setIsFullscreen(false)).catch(() => {});
    }
  };

  return (
    <header className={`fixed top-0 left-0 right-0 z-40 transition-all duration-300 ${
      isScrolled 
        ? 'bg-[#060B14]/95 backdrop-blur-md border-b border-slate-800 shadow-xl py-2.5' 
        : 'bg-[#060B14]/80 backdrop-blur-sm py-3.5 border-b border-slate-800/60'
    }`}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 flex items-center justify-between">
        
        {/* Left: Brand Identity */}
        <div 
          onClick={() => onSelectChapter(1)}
          className="flex items-center gap-3 cursor-pointer group"
        >
          <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-teal-500 to-sky-500 p-[1.5px] shadow-lg group-hover:scale-105 transition-transform">
            <div className="w-full h-full bg-[#060B14] rounded-[10px] flex items-center justify-center font-serif-display font-bold text-teal-300 text-base">
              S
            </div>
          </div>

          <div>
            <div className="flex items-center gap-1.5">
              <span className="font-serif-display font-bold text-white text-lg tracking-wide group-hover:text-teal-300 transition-colors">
                SANJIVANI
              </span>
              <span className="font-devanagari text-[#2DD4BF] font-bold text-sm">
                संजीवनी
              </span>
            </div>
            <span className="text-[10px] font-mono text-slate-400 block -mt-0.5">
              Hybrid Cold-Chain System • Balvigyan 2026–27
            </span>
          </div>
        </div>

        {/* Center: Chapter Quick Selector Pills (Hidden on Mobile) */}
        <nav className="hidden lg:flex items-center gap-1 bg-slate-900/90 p-1 rounded-full border border-slate-800 backdrop-blur-md">
          {CHAPTERS.map(ch => {
            const isActive = currentActiveChapter === ch.id;
            return (
              <button
                key={ch.id}
                onClick={() => { onSelectChapter(ch.id); sound.click(); }}
                className={`px-3 py-1 rounded-full text-xs font-mono transition-all cursor-pointer ${
                  isActive 
                    ? 'bg-teal-600 text-white font-bold shadow-md shadow-teal-900/50' 
                    : 'text-slate-400 hover:text-white hover:bg-slate-800'
                }`}
                title={ch.title}
              >
                {ch.id.toString().padStart(2, '0')}
              </button>
            );
          })}
        </nav>

        {/* Right: Actions & Mode Controls */}
        <div className="flex items-center gap-2">
          
          {/* Chapter Drawer Toggle on Small Screens */}
          <div className="relative lg:hidden">
            <button
              onClick={() => { setShowNavMenu(!showNavMenu); sound.click(); }}
              className="p-2 rounded-xl bg-slate-900 border border-slate-800 text-slate-300 hover:text-white"
            >
              <List className="w-4 h-4" />
            </button>

            {showNavMenu && (
              <div className="absolute right-0 top-12 w-64 bg-[#08111E] border border-slate-800 rounded-2xl p-3 shadow-2xl z-50">
                <span className="text-[10px] font-mono text-teal-400 uppercase tracking-wider block px-2 pb-1 border-b border-slate-800 font-bold">
                  Chapters
                </span>
                <div className="mt-1 space-y-0.5">
                  {CHAPTERS.map(ch => (
                    <button
                      key={ch.id}
                      onClick={() => {
                        onSelectChapter(ch.id);
                        setShowNavMenu(false);
                        sound.click();
                      }}
                      className={`w-full text-left p-2 rounded-lg text-xs font-mono transition-colors ${
                        currentActiveChapter === ch.id ? 'bg-teal-950 text-teal-300 font-bold border border-teal-500/40' : 'text-slate-300 hover:bg-slate-800'
                      }`}
                    >
                      {ch.id}. {ch.title}
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Sound FX Toggle */}
          <button
            onClick={onToggleSound}
            className={`p-2 rounded-xl border transition-all cursor-pointer ${
              isAudioActive 
                ? 'bg-teal-950/80 border-teal-500/40 text-teal-300 shadow-md' 
                : 'bg-slate-900/80 border-slate-800 text-slate-400 hover:text-white'
            }`}
            title={isAudioActive ? 'Mute Procedural Audio' : 'Enable Procedural Sound FX'}
          >
            {isAudioActive ? <Volume2 className="w-4 h-4" /> : <VolumeX className="w-4 h-4" />}
          </button>

          {/* Fullscreen Toggle */}
          <button
            onClick={toggleFullscreen}
            className="p-2 rounded-xl bg-slate-900/80 border border-slate-800 text-slate-400 hover:text-white transition-all cursor-pointer hidden sm:block"
            title="Toggle Browser Fullscreen"
          >
            {isFullscreen ? <Minimize className="w-4 h-4" /> : <Maximize className="w-4 h-4" />}
          </button>

          {/* Download Official PPTX Deck */}
          <a
            href="/assets/SANJIVANI_Balvigyan_Keynote_Presentation.pptx"
            download="SANJIVANI_Balvigyan_Keynote_Presentation.pptx"
            onClick={() => sound.chime()}
            className="hidden md:inline-flex items-center gap-1.5 px-3 py-2 rounded-xl font-mono text-xs font-bold uppercase tracking-wider bg-slate-900/90 hover:bg-slate-800 text-amber-300 border border-amber-500/40 shadow-md transition-all cursor-pointer"
            title="Download Official 16:9 Widescreen PowerPoint Presentation (.pptx)"
          >
            <Download className="w-3.5 h-3.5 text-amber-400" />
            <span>PPTX</span>
          </a>

          {/* Presentation Mode CTA Button */}
          <button
            onClick={() => { sound.click(); onEnterPresentation(); }}
            className="group px-4 py-2 rounded-xl font-mono text-xs font-bold uppercase tracking-wider bg-gradient-to-r from-teal-600 to-sky-600 hover:from-teal-500 hover:to-sky-500 text-white shadow-lg shadow-teal-950/50 transition-all flex items-center gap-2 cursor-pointer"
          >
            <Play className="w-3.5 h-3.5 fill-white text-white group-hover:scale-110 transition-transform" />
            <span className="hidden sm:inline">Present Deck</span>
            <span className="sm:hidden">Deck</span>
          </button>

        </div>

      </div>
    </header>
  );
};
