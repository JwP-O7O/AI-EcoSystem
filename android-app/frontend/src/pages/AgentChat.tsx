import { useState, useEffect, useRef } from 'react';
import { Send, Bot, User, Loader2, AlertCircle } from 'lucide-react';
import { sendAgentMessage, AgentResponse } from '../services/gatewayApi';

interface Message {
  id: number;
  role: 'user' | 'assistant';
  text: string;
  timestamp: number;
}

export default function AgentChat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || loading) return;

    const userMessage: Message = {
      id: Date.now(),
      role: 'user',
      text: input,
      timestamp: Date.now(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setLoading(true);
    setError(null);

    try {
      const response: AgentResponse = await sendAgentMessage({
        text: input,
        context: 'default',
        broadcast: 1,
      });

      const assistantMessage: Message = {
        id: Date.now() + 1,
        role: 'assistant',
        text: response.text || 'No response',
        timestamp: Date.now(),
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to send message');
      console.error('Agent error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="flex flex-col h-full bg-slate-950">
      {/* Header */}
      <div className="h-14 bg-slate-900 border-b border-slate-800 flex items-center px-4 shadow-lg">
        <Bot className="text-primary-500 mr-3" size={24} />
        <div>
          <h1 className="text-lg font-semibold">Agent Zero</h1>
          <p className="text-xs text-slate-400">AI Assistant</p>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 && (
          <div className="flex flex-col items-center justify-center h-full text-slate-500">
            <Bot size={64} className="mb-4 opacity-50" />
            <p className="text-center">Start een gesprek met Agent Zero</p>
            <p className="text-sm text-slate-600 mt-2">Stel een vraag of geef een opdracht</p>
          </div>
        )}

        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex gap-3 animate-slide-up ${
              message.role === 'user' ? 'flex-row-reverse' : 'flex-row'
            }`}
          >
            <div
              className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
                message.role === 'user'
                  ? 'bg-primary-600'
                  : 'bg-slate-700'
              }`}
            >
              {message.role === 'user' ? (
                <User size={18} />
              ) : (
                <Bot size={18} />
              )}
            </div>

            <div
              className={`flex-1 max-w-[80%] rounded-2xl px-4 py-2 ${
                message.role === 'user'
                  ? 'bg-primary-600 text-white'
                  : 'bg-slate-800 text-slate-100'
              }`}
            >
              <p className="whitespace-pre-wrap break-words">{message.text}</p>
            </div>
          </div>
        ))}

        {loading && (
          <div className="flex gap-3 animate-fade-in">
            <div className="flex-shrink-0 w-8 h-8 rounded-full bg-slate-700 flex items-center justify-center">
              <Bot size={18} />
            </div>
            <div className="flex items-center gap-2 bg-slate-800 rounded-2xl px-4 py-3">
              <Loader2 className="animate-spin" size={16} />
              <span className="text-sm text-slate-400">Denken...</span>
            </div>
          </div>
        )}

        {error && (
          <div className="flex gap-3 animate-slide-up">
            <AlertCircle className="text-red-500 flex-shrink-0" size={20} />
            <div className="bg-red-900/30 border border-red-800 rounded-lg px-4 py-2 text-red-200 text-sm">
              {error}
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="border-t border-slate-800 p-4 bg-slate-900">
        <div className="flex gap-2">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type een bericht..."
            className="flex-1 bg-slate-800 text-white rounded-xl px-4 py-3 resize-none focus:outline-none focus:ring-2 focus:ring-primary-500 placeholder-slate-500"
            rows={1}
            disabled={loading}
          />
          <button
            onClick={handleSend}
            disabled={!input.trim() || loading}
            className="bg-primary-600 hover:bg-primary-700 disabled:bg-slate-700 disabled:text-slate-500 text-white rounded-xl px-4 py-3 transition-colors duration-200 flex items-center justify-center"
          >
            {loading ? (
              <Loader2 className="animate-spin" size={20} />
            ) : (
              <Send size={20} />
            )}
          </button>
        </div>
      </div>
    </div>
  );
}
