import React, { useState, useEffect } from 'react';
import { Agent } from '../types';
import Icon from './Icon';
import { ICONS } from '../constants';
import LiveTerminal from './LiveTerminal';
import { useAuth } from '../hooks/useAuth';

interface AgentCardProps {
    agent: Agent;
}

const AgentCard: React.FC<AgentCardProps> = ({ agent }) => {
    const [showTerminal, setShowTerminal] = useState(false);
    const { removeAgent } = useAuth();
    
    const botType = 'botType' in agent.order ? agent.order.botType : "Standaard";
    
    // Effect to prevent body scroll when modal is open
    useEffect(() => {
        const originalStyle = window.getComputedStyle(document.body).overflow;
        if (showTerminal) {
            document.body.style.overflow = 'hidden';
        } else {
            document.body.style.overflow = originalStyle;
        }
        return () => {
            document.body.style.overflow = originalStyle;
        };
    }, [showTerminal]);
    
    const handleRemove = (e: React.MouseEvent) => {
        e.stopPropagation();
        if (window.confirm(`Are you sure you want to delete agent "${agent.name}"? This action cannot be undone.`)) {
            removeAgent(agent.id);
        }
    }

    return (
        <>
            <div className="bg-brand-secondary border border-slate-700 rounded-xl p-6 flex flex-col h-full transition-all duration-300 hover:border-brand-accent-start/50 hover:shadow-xl hover:shadow-brand-accent-start/10">
                <div className="flex justify-between items-start">
                    <div>
                        <h3 className="text-xl font-bold text-white">{agent.name}</h3>
                        <p className="text-sm text-brand-accent-start font-semibold">{botType}</p>
                    </div>
                    <div className={`flex items-center space-x-2 text-xs font-bold px-3 py-1 rounded-full ${agent.status === 'Actief' ? 'bg-green-500/20 text-brand-green' : 'bg-slate-600 text-slate-300'}`}>
                        <div className={`w-2 h-2 rounded-full ${agent.status === 'Actief' ? 'bg-brand-green' : 'bg-slate-400'}`}></div>
                        <span>{agent.status}</span>
                    </div>
                </div>
                
                <div className="border-t border-slate-700 my-4"></div>
                
                <div className="text-sm text-slate-400 space-y-2 flex-grow font-mono">
                    <div className="flex justify-between">
                        <span>Created:</span>
                        <span className="text-slate-300">{new Date(agent.createdAt).toLocaleDateString('nl-NL')}</span>
                    </div>
                    <div className="flex justify-between">
                        <span>Agent ID:</span>
                        <span className="text-slate-300">{agent.id}</span>
                    </div>
                </div>

                <div className="border-t border-slate-700 my-4"></div>

                <div className="flex space-x-2 mt-auto">
                    <button
                        onClick={() => setShowTerminal(true)}
                        className="flex-1 bg-gradient-to-r from-brand-accent-start to-brand-accent-end text-black font-bold py-2 px-4 rounded-lg hover:opacity-90 transition-opacity flex items-center justify-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
                        disabled={!agent.generatedFiles || agent.generatedFiles.length === 0}
                    >
                        <Icon icon={ICONS.TERMINAL} className="w-5 h-5"/>
                        <span>Command Center</span>
                    </button>
                    <button 
                        onClick={handleRemove}
                        className="bg-red-900/50 hover:bg-red-900 text-white font-semibold py-2 px-3 rounded-lg transition-colors"
                        title="Delete Agent"
                    >
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
                    </button>
                </div>
            </div>

            {showTerminal && (
                 <LiveTerminal 
                    files={agent.generatedFiles}
                    order={agent.order}
                    onClose={() => setShowTerminal(false)}
                    agentName={agent.name}
                 />
            )}
        </>
    );
};

export default AgentCard;