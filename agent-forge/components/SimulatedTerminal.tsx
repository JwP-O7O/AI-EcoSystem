import React, { useState, useRef, useEffect } from 'react';
import { GeneratedFile, TerminalLine } from '../types';

interface SimulatedTerminalProps {
    files: GeneratedFile[];
    agentName: string;
}

const SimulatedTerminal: React.FC<SimulatedTerminalProps> = ({ files, agentName }) => {
    const [lines, setLines] = useState<TerminalLine[]>([
        { type: 'output', content: `Welkom bij de gesimuleerde testomgeving. Typ 'help' voor een lijst met commando's.` }
    ]);
    const [input, setInput] = useState('');
    const endOfLinesRef = useRef<null | HTMLDivElement>(null);
    
    const agentPersonality = files.find(f => f.filename === 'agent.py')?.content.includes('Vriendelijk') ? 'vriendelijke' : 'professionele';

    useEffect(() => {
        endOfLinesRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [lines]);

    const handleCommand = (command: string) => {
        const [cmd, ...args] = command.trim().split(' ');
        const newLines: TerminalLine[] = [...lines, { type: 'input', content: command }];

        switch (cmd.toLowerCase()) {
            case 'help':
                newLines.push({ type: 'output', content: `Beschikbare commando's:\n  help    - Toon dit helpbericht\n  ls      - Toon bestanden in de directory\n  cat [bestand] - Toon de inhoud van een bestand\n  run     - Simuleer de uitvoering van de agent\n  clear   - Maak de terminal leeg` });
                break;
            case 'ls':
                const fileList = files.map(f => f.filename).join('   ');
                newLines.push({ type: 'output', content: fileList });
                break;
            case 'cat':
                const filename = args[0];
                const file = files.find(f => f.filename === filename);
                if (file) {
                    newLines.push({ type: 'output', content: `--- Inhoud van ${filename} ---\n${file.content}` });
                } else {
                    newLines.push({ type: 'output', content: `Fout: bestand '${filename}' niet gevonden.` });
                }
                break;
            case 'run':
                newLines.push({ type: 'output', content: `[SIMULATIE] Agent '${agentName}' wordt uitgevoerd met een ${agentPersonality} persoonlijkheid...` });
                newLines.push({ type: 'output', content: `Hallo! Ik ben uw nieuwe ${agentName}. Hoe kan ik u vandaag van dienst zijn?` });
                if(files.some(f => f.content.includes("analyze_data"))) {
                     newLines.push({ type: 'output', content: `[TOOL] Data-analyse tool is beschikbaar. Probeer 'run analyze_data'.` });
                }
                if(files.some(f => f.content.includes("create_content"))) {
                     newLines.push({ type: 'output', content: `[TOOL] Content creatie tool is beschikbaar. Probeer 'run create_content --topic "AI"'.` });
                }
                break;
             case 'clear':
                setLines([]);
                return;
            default:
                if (command.startsWith('run analyze_data')) {
                     newLines.push({ type: 'output', content: `[SIMULATIE] Voer data-analyse uit...` });
                     newLines.push({ type: 'output', content: `Analyse van 'sample_data.csv' voltooid. De gemiddelde omzet is 15000.` });
                } else if(command.startsWith('run create_content')) {
                     const topic = args.find(a => a.startsWith('--topic'))?.split('=')[1] || '"onbekend onderwerp"';
                     newLines.push({ type: 'output', content: `[SIMULATIE] Genereer content over ${topic}...` });
                     newLines.push({ type: 'output', content: `Hier is een korte paragraaf over ${topic.replace(/"/g, '')}: Kunstmatige intelligentie is een fascinerend veld dat...` });
                }
                else {
                    newLines.push({ type: 'output', content: `Fout: commando '${cmd}' niet herkend. Typ 'help' voor hulp.` });
                }
                break;
        }
        setLines(newLines);
    };

    const handleInputSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (input.trim()) {
            handleCommand(input);
            setInput('');
        }
    };

    return (
        <div className="bg-brand-primary border border-slate-700 rounded-lg mt-4 w-full h-96 flex flex-col font-mono text-sm">
            <div className="bg-slate-800 p-2 rounded-t-lg text-white font-semibold">
                Gesimuleerde Terminal
            </div>
            <div className="flex-grow p-4 overflow-y-auto">
                {lines.map((line, index) => (
                    <div key={index} className="whitespace-pre-wrap">
                        {line.type === 'input' && <span className="text-green-400 mr-2">$</span>}
                        <span className={line.type === 'input' ? 'text-white' : 'text-slate-300'}>
                            {line.content}
                        </span>
                    </div>
                ))}
                <div ref={endOfLinesRef} />
            </div>
            <form onSubmit={handleInputSubmit} className="flex border-t border-slate-700">
                <span className="p-2 text-green-400">$</span>
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    className="w-full bg-transparent text-white focus:outline-none p-2"
                    placeholder="Typ hier uw commando..."
                    autoFocus
                />
            </form>
        </div>
    );
};

export default SimulatedTerminal;