import React, { useState, useRef, useEffect } from 'react';
import { Send, Mic, Paperclip } from 'lucide-react';

interface InputAreaProps {
  onSendMessage: (content: string) => void;
  isLoading: boolean;
}

export const InputArea: React.FC<InputAreaProps> = ({ onSendMessage, isLoading }) => {
  const [input, setInput] = useState('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleSubmit = (e?: React.FormEvent) => {
    e?.preventDefault();
    if (!input.trim() || isLoading) return;
    
    onSendMessage(input);
    setInput('');
    
    // Reset height
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const handleInput = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInput(e.target.value);
    // Auto-resize
    e.target.style.height = 'auto';
    e.target.style.height = `${e.target.scrollHeight}px`;
  };

  return (
    <div className="p-6 bg-slate-900/80 backdrop-blur-md border-t border-slate-700/50">
      <div className="max-w-4xl mx-auto relative">
        <form onSubmit={handleSubmit} className="relative flex items-end gap-2 bg-slate-800/50 rounded-2xl border border-slate-700/50 p-2 focus-within:ring-2 focus-within:ring-blue-500/50 focus-within:border-blue-500/50 transition-all duration-300">
          <button
            type="button"
            className="p-3 text-slate-400 hover:text-blue-400 hover:bg-slate-700/50 rounded-xl transition-colors"
            title="Attach file"
          >
            <Paperclip size={20} />
          </button>
          
          <textarea
            ref={textareaRef}
            value={input}
            onChange={handleInput}
            onKeyDown={handleKeyDown}
            placeholder="Instruct the swarm..."
            rows={1}
            className="flex-1 bg-transparent border-none focus:ring-0 text-slate-200 placeholder-slate-500 py-3 max-h-48 resize-none scrollbar-hide"
            disabled={isLoading}
          />
          
          <div className="flex items-center gap-1">
            <button
              type="button"
              className="p-3 text-slate-400 hover:text-blue-400 hover:bg-slate-700/50 rounded-xl transition-colors"
              title="Voice input"
            >
              <Mic size={20} />
            </button>
            <button
              type="submit"
              disabled={!input.trim() || isLoading}
              className="p-3 bg-blue-600 hover:bg-blue-500 text-white rounded-xl disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-lg shadow-blue-600/20"
            >
              <Send size={20} />
            </button>
          </div>
        </form>
        <div className="text-center mt-3 text-xs text-slate-500">
          Agent Zero v2.5 • Quantum Context System Active • Secure Connection
        </div>
      </div>
    </div>
  );
};
