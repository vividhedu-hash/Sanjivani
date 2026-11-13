import React from 'react';
import { X } from 'lucide-react';
import { KeynotePresentationDeck } from './KeynotePresentationDeck';
import { sound } from '../utils/soundEffects';

interface PresentationModalProps {
  isOpen: boolean;
  onClose: () => void;
  initialChapter?: number;
  renderChapterContent?: (chapterId: number) => React.ReactNode;
}

export const PresentationModal: React.FC<PresentationModalProps> = ({
  isOpen,
  onClose
}) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 bg-[#040810] flex flex-col overflow-hidden select-none">
      {/* Top Floating Exit Ribbon */}
      <div className="absolute top-3 right-4 z-50 flex items-center gap-2">
        <button
          onClick={() => {
            sound.click();
            onClose();
          }}
          className="px-3 py-1.5 rounded-xl bg-slate-900/90 hover:bg-rose-950/90 text-rose-300 border border-slate-700 hover:border-rose-500 font-mono text-xs font-bold transition-all shadow-xl backdrop-blur-md flex items-center gap-1.5 cursor-pointer"
          title="Exit Presentation [ESC]"
        >
          <X className="w-4 h-4" />
          <span>EXIT [ESC]</span>
        </button>
      </div>

      {/* Main Full-Screen Keynote Deck */}
      <div className="w-full h-full">
        <KeynotePresentationDeck />
      </div>
    </div>
  );
};
