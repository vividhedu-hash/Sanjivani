import React, { useState, useEffect } from 'react';
import { 
  CHAPTERS, 
  PRESENTER_NOTES 
} from '../data/sanjivaniData';
import { 
  X, 
  ChevronLeft, 
  ChevronRight, 
  Maximize, 
  Minimize, 
  FileText, 
  List, 
  Keyboard,
  Sun,
  Moon,
  Sparkles
} from 'lucide-react';
import { sound } from '../utils/soundEffects';

interface PresentationModalProps {
  isOpen: boolean;
  onClose: () => void;
  initialChapter?: number;
  renderChapterContent: (chapterId: number) => React.ReactNode;
}

export const PresentationModal: React.FC<PresentationModalProps> = ({
  isOpen,
  onClose,
  initialChapter = 1,
  renderChapterContent
}) => {
  const [currentChapter, setCurrentChapter] = useState<number>(initialChapter);
  const [showNotes, setShowNotes] = useState<boolean>(false);
  const [showJumpMenu, setShowJumpMenu] = useState<boolean>(false);
  const [isFullscreen, setIsFullscreen] = useState<boolean>(false);
  const [showHelp, setShowHelp] = useState<boolean>(false);
  const [slideAnimationKey, setSlideAnimationKey] = useState<number>(0);

  useEffect(() => {
    setCurrentChapter(initialChapter);
    setSlideAnimationKey(prev => prev + 1);
  }, [initialChapter]);

  // Keyboard navigation listener
  useEffect(() => {
    if (!isOpen) return;

    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') {
        e.preventDefault();
        goToNext();
      } else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {
        e.preventDefault();
        goToPrev();
      } else if (e.key === 'Escape') {
        e.preventDefault();
        onClose();
      } else if (e.key.toLowerCase() === 'n') {
        setShowNotes(prev => !prev);
        sound.click();
      } else if (e.key.toLowerCase() === 'f') {
        toggleFullscreen();
      } else if (e.key.toLowerCase() === 'r') {
        setCurrentChapter(1);
        setSlideAnimationKey(prev => prev + 1);
        sound.click();
      } else if (e.key === '?') {
        setShowHelp(prev => !prev);
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, currentChapter]);

  const goToNext = () => {
    if (currentChapter < CHAPTERS.length) {
      setCurrentChapter(c => c + 1);
      setSlideAnimationKey(prev => prev + 1);
      sound.click();
    }
  };

  const goToPrev = () => {
    if (currentChapter > 1) {
      setCurrentChapter(c => c - 1);
      setSlideAnimationKey(prev => prev + 1);
      sound.click();
    }
  };

  const toggleFullscreen = () => {
    sound.click();
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen().then(() => setIsFullscreen(true)).catch(() => {});
    } else {
      document.exitFullscreen().then(() => setIsFullscreen(false)).catch(() => {});
    }
  };

  if (!isOpen) return null;

  const activeChap = CHAPTERS[currentChapter - 1];
  const activeNote = PRESENTER_NOTES[currentChapter];

  return (
    <div className="fixed inset-0 z-50 bg-[#F1F5F9] text-[#0F172A] flex flex-col overflow-hidden select-none">
      
      {/* Top Presentation Header Bar */}
      <header className="h-12 px-4 md:px-6 bg-white border-b border-slate-200 flex items-center justify-between z-30 shrink-0 shadow-sm">
        
        {/* Left: Branding & Slide Counter */}
        <div className="flex items-center gap-3">
          <span className="font-serif-display font-bold text-[#0B2545] text-lg tracking-wide">
            SANJIVANI
          </span>
          <span className="font-devanagari text-[#0F766E] font-bold text-sm">संजीवनी</span>
          <span className="text-slate-300">•</span>
          <div className="flex items-center gap-1.5 font-mono text-xs font-bold text-[#0F766E] bg-teal-50 border border-teal-200 px-2.5 py-0.5 rounded-full">
            <span>SLIDE {currentChapter.toString().padStart(2, '0')}</span>
            <span className="text-slate-400">/</span>
            <span>{CHAPTERS.length.toString().padStart(2, '0')}</span>
          </div>
        </div>

        {/* Center: Slide Chapter Title */}
        <div className="hidden md:flex items-center gap-2">
          <span className="font-serif-display text-sm font-bold text-[#0B2545]">
            {activeChap.title}:
          </span>
          <span className="text-xs font-sans-tech text-slate-600">
            {activeChap.subtitle}
          </span>
        </div>

        {/* Right: Keynote Controls */}
        <div className="flex items-center gap-2">
          
          {/* Index Jump Menu */}
          <button
            onClick={() => { setShowJumpMenu(!showJumpMenu); sound.click(); }}
            className={`px-2.5 py-1 rounded-lg text-xs font-mono font-semibold border transition-all flex items-center gap-1.5 cursor-pointer ${
              showJumpMenu ? 'bg-[#0F766E] text-white border-[#0F766E]' : 'bg-slate-100 text-slate-700 border-slate-200 hover:bg-slate-200'
            }`}
            title="Jump to Slide"
          >
            <List className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">Index</span>
          </button>

          {/* Floating Notes Toggle */}
          <button
            onClick={() => { setShowNotes(!showNotes); sound.click(); }}
            className={`px-2.5 py-1 rounded-lg text-xs font-mono font-semibold border transition-all flex items-center gap-1.5 cursor-pointer ${
              showNotes ? 'bg-amber-600 text-white border-amber-600' : 'bg-slate-100 text-slate-700 border-slate-200 hover:bg-slate-200'
            }`}
            title="Toggle Speaker Notes [N]"
          >
            <FileText className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">Notes</span>
          </button>

          {/* Keyboard Shortcuts Help */}
          <button
            onClick={() => { setShowHelp(!showHelp); sound.click(); }}
            className="p-1 rounded-lg bg-slate-100 text-slate-600 hover:text-slate-900 border border-slate-200 transition-colors cursor-pointer"
            title="Shortcuts [?]"
          >
            <Keyboard className="w-4 h-4" />
          </button>

          {/* Fullscreen */}
          <button
            onClick={toggleFullscreen}
            className="p-1 rounded-lg bg-slate-100 text-slate-600 hover:text-slate-900 border border-slate-200 transition-colors cursor-pointer"
            title="Fullscreen [F]"
          >
            {isFullscreen ? <Minimize className="w-4 h-4" /> : <Maximize className="w-4 h-4" />}
          </button>

          {/* Exit Button */}
          <button
            onClick={() => { sound.click(); onClose(); }}
            className="px-3 py-1 rounded-lg bg-rose-50 hover:bg-rose-100 text-rose-700 border border-rose-200 text-xs font-mono font-bold flex items-center gap-1.5 transition-colors cursor-pointer"
            title="Exit Presentation [ESC]"
          >
            <X className="w-4 h-4" />
            <span>Exit [ESC]</span>
          </button>
        </div>

      </header>

      {/* Slide Progress Indicator Bar */}
      <div className="w-full h-1 bg-slate-200 relative">
        <div 
          className="h-full bg-gradient-to-r from-[#0F766E] to-[#0284C7] transition-all duration-300"
          style={{ width: `${(currentChapter / CHAPTERS.length) * 100}%` }}
        />
      </div>

      {/* Main Slide Presentation Stage: Fits 100% of the screen */}
      <main className="flex-1 overflow-y-auto px-4 md:px-8 py-3 flex items-center justify-center relative bg-gradient-to-b from-[#F8FAFC] to-[#F1F5F9]">
        
        {/* Animated Slide Container with PowerPoint-Style Motion */}
        <div 
          key={slideAnimationKey} 
          className="w-full max-w-6xl mx-auto my-auto animate-ppt-slide"
        >
          {renderChapterContent(currentChapter)}
        </div>

        {/* Floating Draggable/Dockable Speaker Notes Modal */}
        {showNotes && activeNote && (
          <div className="absolute bottom-5 right-5 z-40 max-w-md w-full bg-white/95 border border-amber-400 rounded-2xl p-4 shadow-2xl backdrop-blur-xl animate-ppt-up">
            <div className="flex items-center justify-between pb-2 border-b border-amber-200">
              <div className="flex items-center gap-1.5 text-xs font-mono font-bold text-amber-800">
                <FileText className="w-3.5 h-3.5 text-amber-600" />
                <span>SPEAKER SCRIPT • CHAPTER {currentChapter}</span>
              </div>
              <button 
                onClick={() => setShowNotes(false)} 
                className="text-slate-400 hover:text-slate-700"
              >
                <X className="w-3.5 h-3.5" />
              </button>
            </div>

            <div className="mt-2 space-y-2 text-xs">
              <div>
                <span className="text-[10px] font-mono text-slate-500 uppercase font-semibold">Key Idea:</span>
                <p className="text-slate-800 font-medium">{activeNote.keyIdea}</p>
              </div>

              <div className="bg-amber-50/80 p-2.5 rounded-lg border border-amber-200">
                <span className="text-[10px] font-mono text-amber-800 uppercase font-bold block mb-0.5">
                  Suggested Oral Cue:
                </span>
                <p className="text-slate-800 italic leading-relaxed text-[11px]">
                  “{activeNote.script}”
                </p>
              </div>

              <div className="text-[10px] font-mono text-slate-500">
                Judging Focus: <span className="text-slate-700 font-semibold">{activeNote.judgingFocus}</span>
              </div>
            </div>
          </div>
        )}

        {/* Quick Slide Index Menu Overlay */}
        {showJumpMenu && (
          <div className="absolute top-4 right-4 z-40 w-80 bg-white border border-slate-200 rounded-2xl p-4 shadow-2xl backdrop-blur-xl animate-ppt-zoom">
            <div className="flex items-center justify-between pb-2 border-b border-slate-100">
              <span className="font-serif-display font-bold text-[#0B2545] text-sm">Slide Index</span>
              <button onClick={() => setShowJumpMenu(false)} className="text-slate-400 hover:text-slate-700">
                <X className="w-4 h-4" />
              </button>
            </div>
            <div className="mt-2 space-y-1 max-h-96 overflow-y-auto">
              {CHAPTERS.map(ch => (
                <button
                  key={ch.id}
                  onClick={() => {
                    setCurrentChapter(ch.id);
                    setSlideAnimationKey(prev => prev + 1);
                    setShowJumpMenu(false);
                    sound.click();
                  }}
                  className={`w-full text-left p-2 rounded-lg text-xs transition-colors flex items-center justify-between ${
                    currentChapter === ch.id 
                      ? 'bg-[#0F766E] text-white font-bold' 
                      : 'text-slate-700 hover:bg-slate-100'
                  }`}
                >
                  <span className="font-mono">{ch.id.toString().padStart(2, '0')}. {ch.title}</span>
                  <span className="text-[10px] text-slate-400">{ch.subtitle.slice(0, 16)}...</span>
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Keyboard Shortcuts Modal */}
        {showHelp && (
          <div className="absolute inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4">
            <div className="bg-white border border-slate-200 rounded-2xl p-6 max-w-md w-full shadow-2xl animate-ppt-zoom">
              <div className="flex items-center justify-between pb-3 border-b border-slate-200">
                <h4 className="font-mono text-sm font-bold text-[#0B2545] flex items-center gap-2">
                  <Keyboard className="w-4 h-4 text-[#0F766E]" />
                  Keynote Keyboard Shortcuts
                </h4>
                <button onClick={() => setShowHelp(false)} className="text-slate-400 hover:text-slate-700">
                  <X className="w-4 h-4" />
                </button>
              </div>

              <div className="mt-4 space-y-2 text-xs font-mono">
                <div className="flex justify-between p-2 bg-slate-50 rounded border border-slate-100">
                  <span className="text-slate-600">Next Slide</span>
                  <span className="text-[#0F766E] font-bold">Right Arrow / Spacebar</span>
                </div>
                <div className="flex justify-between p-2 bg-slate-50 rounded border border-slate-100">
                  <span className="text-slate-600">Previous Slide</span>
                  <span className="text-[#0F766E] font-bold">Left Arrow</span>
                </div>
                <div className="flex justify-between p-2 bg-slate-50 rounded border border-slate-100">
                  <span className="text-slate-600">Toggle Speaker Notes</span>
                  <span className="text-amber-600 font-bold">N</span>
                </div>
                <div className="flex justify-between p-2 bg-slate-50 rounded border border-slate-100">
                  <span className="text-slate-600">Toggle Fullscreen</span>
                  <span className="text-cyan-600 font-bold">F</span>
                </div>
                <div className="flex justify-between p-2 bg-slate-50 rounded border border-slate-100">
                  <span className="text-slate-600">Restart from Slide 1</span>
                  <span className="text-purple-600 font-bold">R</span>
                </div>
                <div className="flex justify-between p-2 bg-slate-50 rounded border border-slate-100">
                  <span className="text-slate-600">Exit Presentation</span>
                  <span className="text-rose-600 font-bold">ESC</span>
                </div>
              </div>

              <button
                onClick={() => setShowHelp(false)}
                className="w-full mt-4 py-2 rounded-lg bg-[#0F766E] text-white text-xs font-mono font-bold"
              >
                Got It
              </button>
            </div>
          </div>
        )}

      </main>

      {/* Bottom Floating Navigation Toolbar */}
      <footer className="h-12 px-6 bg-white border-t border-slate-200 flex items-center justify-between shrink-0 z-30 shadow-sm">
        
        {/* Previous Button */}
        <button
          onClick={goToPrev}
          disabled={currentChapter === 1}
          className={`px-3 py-1.5 rounded-lg text-xs font-mono font-semibold flex items-center gap-1.5 border transition-all cursor-pointer ${
            currentChapter === 1 
              ? 'opacity-30 border-transparent text-slate-400 cursor-not-allowed' 
              : 'bg-slate-100 hover:bg-slate-200 text-slate-800 border-slate-200'
          }`}
        >
          <ChevronLeft className="w-3.5 h-3.5" />
          <span>PREVIOUS</span>
        </button>

        {/* Chapter Pills */}
        <div className="hidden sm:flex items-center gap-1.5">
          {CHAPTERS.map(ch => (
            <button
              key={ch.id}
              onClick={() => { 
                setCurrentChapter(ch.id); 
                setSlideAnimationKey(prev => prev + 1);
                sound.click(); 
              }}
              className={`h-2 rounded-full transition-all cursor-pointer ${
                currentChapter === ch.id 
                  ? 'w-8 bg-[#0F766E]' 
                  : currentChapter > ch.id 
                  ? 'w-2 bg-teal-300' 
                  : 'w-2 bg-slate-200 hover:bg-slate-300'
              }`}
              title={`${ch.id}. ${ch.title}`}
            />
          ))}
        </div>

        {/* Next Button */}
        <button
          onClick={goToNext}
          disabled={currentChapter === CHAPTERS.length}
          className={`px-4 py-1.5 rounded-lg text-xs font-mono font-bold flex items-center gap-1.5 transition-all cursor-pointer ${
            currentChapter === CHAPTERS.length
              ? 'opacity-30 border-transparent text-slate-400 cursor-not-allowed'
              : 'bg-[#0F766E] hover:bg-[#0D9488] text-white shadow-md shadow-[#0F766E]/20'
          }`}
        >
          <span>{currentChapter === CHAPTERS.length ? 'FINISH' : 'NEXT SLIDE'}</span>
          <ChevronRight className="w-3.5 h-3.5" />
        </button>

      </footer>

    </div>
  );
};
