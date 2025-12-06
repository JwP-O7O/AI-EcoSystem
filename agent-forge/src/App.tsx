import React, { useState, useEffect, useRef } from 'react';
import { Sidebar } from './components/Sidebar';
import { ChatMessage } from './components/ChatMessage';
import { InputArea } from './components/InputArea';
import { api } from './services/api';
import { Message, SystemStatus } from './types';
import { Layers, Brain, Zap } from 'lucide-react';

function App() {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: 'system',
      content: 'System initialized. Agent Zero ready for commands.',
      timestamp: new Date().toISOString()
    }
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const [status, setStatus] = useState<SystemStatus>(
    {
      cpu: 12,
      memory: 34,
      active_agents: 1,
      uptime: 3600
    }
  );

  const chatEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    const interval = setInterval(async () => {
      const newStatus = await api.checkHealth();
      // Simple fallback if API returns 0s for demo purposes
      if (newStatus.cpu === 0 && newStatus.memory === 0) {
         return; 
      }
      setStatus(newStatus);
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSendMessage = async (content: string) => {
    const userMessage: Message = {
      role: 'user',
      content,
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const response = await api.sendMessage(content);
      setMessages(prev => [...prev, response]);
    } catch (error) {
      const errorMessage: Message = {
        role: 'system',
        content: 'Error: Failed to communicate with Agent Zero. Please check the backend connection.',
        timestamp: new Date().toISOString()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex h-screen bg-slate-950 text-slate-200 overflow-hidden font-sans selection:bg-blue-500/30">
      <Sidebar status={status} />

      <main className="flex-1 flex flex-col relative">
        {/* Background Effects */}
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-blue-900/20 via-slate-950 to-slate-950 pointer-events-none" />
        <div className="absolute inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-20 pointer-events-none" />

        {/* Header */}
        <header className="h-16 border-b border-slate-800/50 bg-slate-900/50 backdrop-blur-sm flex items-center justify-between px-6 z-10">
          <div className="flex items-center gap-4">
            <h2 className="font-semibold text-lg tracking-tight">Main Session</h2>
            <span className="px-2 py-0.5 rounded-full bg-blue-500/10 text-blue-400 text-xs border border-blue-500/20">
              Interactive
            </span>
          </div>
          <div className="flex items-center gap-4 text-sm text-slate-400">
             <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-slate-800/50 border border-slate-700/50">
               <Brain size={14} className="text-purple-400"/>
               <span>RAG: Active</span>
             </div>
             <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-slate-800/50 border border-slate-700/50">
               <Layers size={14} className="text-emerald-400"/>
               <span>Tools: 12</span>
             </div>
          </div>
        </header>

        {/* Chat Area */}
        <div className="flex-1 overflow-y-auto p-6 scrollbar-thin scrollbar-thumb-slate-700 scrollbar-track-transparent">
          <div className="max-w-4xl mx-auto space-y-6">
            {messages.map((msg, idx) => (
              <ChatMessage key={idx} message={msg} />
            ))}
            {isLoading && (
              <div className="flex w-full mb-6 justify-start">
                 <div className="bg-slate-800/90 border border-slate-700/50 rounded-2xl rounded-bl-none p-4 shadow-lg backdrop-blur-sm flex items-center gap-3">
                   <div className="w-8 h-8 rounded-full bg-indigo-500 flex items-center justify-center">
                     <Zap size={16} className="text-white animate-pulse"/>
                   </div>
                   <div className="flex gap-1">
                     <span className="w-2 h-2 rounded-full bg-indigo-400 animate-bounce" style={{ animationDelay: '0ms' }}/>
                     <span className="w-2 h-2 rounded-full bg-indigo-400 animate-bounce" style={{ animationDelay: '150ms' }}/>
                     <span className="w-2 h-2 rounded-full bg-indigo-400 animate-bounce" style={{ animationDelay: '300ms' }}/>
                   </div>
                 </div>
              </div>
            )}
            <div ref={chatEndRef} />
          </div>
        </div>

        <InputArea onSendMessage={handleSendMessage} isLoading={isLoading} />
      </main>
    </div>
  );
}

export default App;
