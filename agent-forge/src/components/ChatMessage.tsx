import React from 'react';
import { Message } from '../types';
import { Bot, User, Terminal } from 'lucide-react';
import { clsx } from 'clsx';

interface ChatMessageProps {
  message: Message;
}

export const ChatMessage: React.FC<ChatMessageProps> = ({ message }) => {
  const isUser = message.role === 'user';
  const isSystem = message.role === 'system';

  return (
    <div
      className={clsx(
        "flex w-full mb-6",
        isUser ? "justify-end" : "justify-start"
      )}
    >
      <div
        className={clsx(
          "flex max-w-[80%] rounded-2xl p-4 shadow-lg backdrop-blur-sm border",
          isUser 
            ? "bg-blue-600/90 border-blue-500/50 text-white rounded-br-none" 
            : isSystem
            ? "bg-slate-800/90 border-slate-700/50 text-slate-300 font-mono text-sm w-full"
            : "bg-slate-800/90 border-slate-700/50 text-slate-100 rounded-bl-none"
        )}
      >
        <div className="flex gap-4">
          <div className={clsx(
            "w-8 h-8 rounded-full flex items-center justify-center shrink-0",
            isUser ? "bg-blue-500" : isSystem ? "bg-slate-700" : "bg-indigo-500"
          )}>
            {isUser ? <User size={16} /> : isSystem ? <Terminal size={16} /> : <Bot size={16} />}
          </div>
          
          <div className="flex-1 overflow-hidden">
            <div className="text-xs opacity-50 mb-1 flex justify-between">
              <span className="font-bold uppercase tracking-wider">
                {message.role}
              </span>
              <span>{new Date(message.timestamp).toLocaleTimeString()}</span>
            </div>
            <div className="whitespace-pre-wrap leading-relaxed">
              {message.content}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
