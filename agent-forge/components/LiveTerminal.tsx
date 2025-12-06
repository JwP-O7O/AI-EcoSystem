import React, { useState, useRef, useEffect } from 'react';
import { GeneratedFile, TerminalLine, PricingTier, CustomBuild } from '../types';
import { runInCloud } from '../services/liveExecutionApi';

interface LiveTerminalProps {
    files: GeneratedFile[];
    order: PricingTier | (CustomBuild & { name: string });
    onClose: () => void;
    agentName: string;
}

const LiveTerminal: React.FC<LiveTerminalProps> = ({ files, order, onClose, agentName }) => {
    const [lines, setLines] = useState<TerminalLine[]>([
        { type: 'system', content: `Verbinding gemaakt met agent "${agentName}". Welkom bij het Command Center.` },
        { type: 'system', content: "Typ 'help' voor een lijst met commando's." }
    ]);
    const [input, setInput] = useState('');
    const [isExecuting, setIsExecuting] = useState(false);
    const [history, setHistory] = useState<string[]>([]);
    const [historyIndex, setHistoryIndex] = useState(-1);
    const [activeFile, setActiveFile] = useState<GeneratedFile | null>(null);
    
    const endOfLinesRef = useRef<null | HTMLDivElement>(null);
    const inputRef = useRef<null | HTMLInputElement>(null);

    useEffect(() => {
        // Automatically select agent.py on load if it exists
        const agentPy = files.find(f => f.filename === 'agent.py');
        if (agentPy) {
            setActiveFile(agentPy);
        } else if (files.length > 0) {
            setActiveFile(files[0]);
        }
    }, [files]);
    
    useEffect(() => {
        endOfLinesRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [lines]);
    
    useEffect(() => {
        inputRef.current?.focus();
    }, [isExecuting]);

    const handleCommand = async (command: string) => {
        if (command.trim() === '') return;
        
        setIsExecuting(true);
        const commandLines: TerminalLine[] = [{ type: 'input', content: command }];
        setLines(prev => [...prev, ...commandLines]);

        if (command.trim().toLowerCase() !== 'clear') {
             setHistory(prev => [command, ...prev].slice(0, 50)); // Keep last 50 commands
        }
        setHistoryIndex(-1);

        const fullConversationHistory = [...lines, ...commandLines];
        const output = await runInCloud(command, files, order, fullConversationHistory);

        if (output === 'CLEAR_TERMINAL') {
            setLines([]);
        } else {
            setLines(prev => [...prev, { type: 'output', content: output }]);
        }
        
        setIsExecuting(false);
    };

    const handleInputSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (input.trim() && !isExecuting) {
            handleCommand(input);
            setInput('');
        }
    };
    
    const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
        if (e.key === 'ArrowUp') {
            e.preventDefault();
            if (historyIndex < history.length - 1) {
                const newIndex = historyIndex + 1;
                setHistoryIndex(newIndex);
                setInput(history[newIndex]);
            }
        } else if (e.key === 'ArrowDown') {
            e.preventDefault();
            if (historyIndex > 0) {
                const newIndex = historyIndex - 1;
                setHistoryIndex(newIndex);
                setInput(history[newIndex]);
            } else {
                setHistoryIndex(-1);
                setInput('');
            }
        } else if (e.key === 'Tab') {
            e.preventDefault();
            // Basic autocomplete for filenames
            const filePrefix = input.split(' ').pop() || '';
            const matchingFile = files.find(f => f.filename.startsWith(filePrefix));
            if (matchingFile) {
                const commandParts = input.split(' ');
                commandParts[commandParts.length - 1] = matchingFile.filename;
                setInput(commandParts.join(' '));
            }
        }
    };

    const promptSymbol = '$';

    return (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-md z-50 flex items-center justify-center p-4 animate-fade-in">
            <div className="w-full h-full max-w-7xl max-h-[90vh] flex flex-col bg-brand-secondary rounded-lg border border-brand-accent-end/30 shadow-2xl shadow-brand-accent-end/20">
                <div className="flex justify-between items-center p-3 border-b border-brand-accent-end/30 flex-shrink-0">
                    <div className="flex items-center space-x-2">
                        <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
                        <h3 className="text-lg font-bold text-white">Command Center: {agentName}</h3>
                    </div>
                    <button onClick={onClose} className="text-slate-400 hover:text-white transition-colors text-3xl leading-none px-2">&times;</button>
                </div>
                <div className="flex-grow p-4 h-full flex gap-4 overflow-hidden">
                    {/* File Explorer */}
                    <div className="w-1/4 h-full bg-brand-dark/50 rounded-md p-2 flex-shrink-0 overflow-y-auto">
                        <h4 className="font-bold text-white p-2 mb-2 border-b border-slate-700">Project Files</h4>
                        <ul className="space-y-1">
                            {files.map(file => (
                                <li key={file.filename}>
                                    <button 
                                        onClick={() => setActiveFile(file)}
                                        className={`w-full text-left px-3 py-1.5 text-sm rounded transition-colors ${activeFile?.filename === file.filename ? 'bg-brand-accent-start/20 text-brand-accent-start font-semibold' : 'text-slate-300 hover:bg-slate-700/50'}`}
                                    >
                                        {file.filename}
                                    </button>
                                </li>
                            ))}
                        </ul>
                    </div>
                    {/* Code & Terminal Panes */}
                    <div className="w-3/4 h-full flex flex-col gap-4">
                        <div className="h-1/2 flex flex-col bg-brand-dark/50 rounded-md overflow-hidden">
                           <div className="bg-slate-800 p-2 rounded-t-md text-white font-semibold flex-shrink-0">
                                {activeFile?.filename || "Select a file"}
                           </div>
                           <pre className="text-sm overflow-auto p-4 h-full">
                                <code className="language-python text-slate-300 font-mono whitespace-pre-wrap">
                                    {activeFile?.content || "No file selected."}
                                </code>
                           </pre>
                        </div>
                        <div className="h-1/2 flex flex-col bg-black/50 rounded-md font-mono text-sm border border-slate-700">
                            <div className="bg-slate-800 p-2 rounded-t-md text-white font-semibold flex-shrink-0">
                                Live Terminal
                            </div>
                            <div className="flex-grow p-4 overflow-y-auto" onClick={() => inputRef.current?.focus()}>
                                {lines.map((line, index) => (
                                    <div key={index} className="whitespace-pre-wrap leading-relaxed">
                                        {line.type === 'input' && <span className="text-brand-green mr-2">{promptSymbol}</span>}
                                        <span className={
                                            line.type === 'input' ? 'text-white' : 
                                            line.type === 'system' ? 'text-slate-400' :
                                            line.type === 'error' ? 'text-red-400' : 
                                            'text-slate-300'}>
                                            {line.content}
                                        </span>
                                    </div>
                                ))}
                                {isExecuting && (
                                    <div className="flex items-center space-x-2 pt-1">
                                        <div className="w-2 h-2 bg-brand-green rounded-full animate-pulse"></div>
                                        <span className="text-slate-400">executing...</span>
                                    </div>
                                )}
                                <div ref={endOfLinesRef} />
                            </div>
                            <form onSubmit={handleInputSubmit} className="flex border-t border-slate-700">
                                <span className="p-2 text-brand-green">{promptSymbol}</span>
                                <input
                                    ref={inputRef}
                                    type="text"
                                    value={input}
                                    onChange={(e) => setInput(e.target.value)}
                                    onKeyDown={handleKeyDown}
                                    className="w-full bg-transparent text-white focus:outline-none p-2"
                                    placeholder={isExecuting ? 'Agent is busy...' : 'Type a command...'}
                                    disabled={isExecuting}
                                    autoFocus
                                />
                            </form>
                        </div>
                    </div>
                </div>
            </div>
             <style>{`
                @keyframes fadeIn {
                    from { opacity: 0; transform: scale(0.98); }
                    to { opacity: 1; transform: scale(1); }
                }
                .animate-fade-in { animation: fadeIn 0.2s ease-out forwards; }
            `}</style>
        </div>
    );
};

export default LiveTerminal;