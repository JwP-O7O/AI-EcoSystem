import React, { useState, useEffect } from 'react';
import { useLocation, Link, useNavigate } from 'react-router-dom';
import Icon from '../components/Icon';
import { ICONS } from '../constants';
import { generateProject } from '../services/genesisForgeAgent';
import { GeneratedFile, PricingTier, CustomBuild, BuildLogLine } from '../types';
import { useAuth } from '../hooks/useAuth';

const ConfirmationPage = () => {
    const location = useLocation();
    const navigate = useNavigate();
    const { addAgent, user } = useAuth();
    const { order } = location.state as { email: string; order: PricingTier | (CustomBuild & { name: string }) } || {};

    const [buildLogs, setBuildLogs] = useState<BuildLogLine[]>([]);
    const [buildError, setBuildError] = useState<string | null>(null);
    const [isComplete, setIsComplete] = useState(false);

    useEffect(() => {
        if (!user) {
            navigate('/login', { state: { from: location } });
            return;
        }

        if (order) {
            const processBuild = async () => {
                try {
                    const generatedFiles = await generateProject(order, (log) => {
                        setBuildLogs(prev => [...prev, log]);
                    });
                    
                    await new Promise(res => setTimeout(res, 750));
                    setBuildLogs(prev => [...prev, { level: 'DEPLOY', message: "Registering agent to your account..." }]);
                    addAgent(order, generatedFiles);
                    
                    await new Promise(res => setTimeout(res, 750));
                    setBuildLogs(prev => [...prev, { level: 'SUCCESS', message: `Agent "${order.name}" successfully forged and deployed!` }]);
                    
                    setIsComplete(true);

                } catch (error) {
                    const errorMessage = error instanceof Error ? error.message : "An unknown error occurred.";
                    setBuildLogs(prev => [...prev, { level: 'ERROR', message: `Forge failed: ${errorMessage}` }]);
                    setBuildError(`The AI Forge encountered an error. ${errorMessage}`);
                }
            };
            processBuild();
        } else {
             const errorMsg = "Order details not found. Cannot activate forge.";
             setBuildLogs([{ level: 'ERROR', message: errorMsg }]);
             setBuildError(errorMsg);
        }
    // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [order, addAgent, navigate, user, location]);

    const getIconForLevel = (level: BuildLogLine['level']) => {
        switch (level) {
            case 'INFO': return <span className="text-blue-400">i</span>;
            case 'GEN': return <span className="text-purple-400">~</span>;
            case 'VALIDATE': return <span className="text-yellow-400">?</span>;
            case 'DEPLOY': return <span className="text-cyan-400">🚀</span>;
            case 'SUCCESS': return <span className="text-brand-green">✓</span>;
            case 'ERROR': return <span className="text-red-500">!</span>;
            default: return '';
        }
    };

    const renderStatus = () => {
        if (isComplete) {
            return (
                 <>
                    <div className="w-20 h-20 mx-auto bg-green-500/20 flex items-center justify-center rounded-full border-2 border-brand-green mb-6">
                        <Icon icon={ICONS.CHECK} className="w-10 h-10 text-brand-green" />
                    </div>
                    <h1 className="text-3xl font-bold text-white mb-4">Forge Complete!</h1>
                    <p className="text-lg text-slate-300 mb-8">
                        Your agent <strong className="text-white">{order.name}</strong> is now active in your Command Center.
                    </p>
                    <Link to="/dashboard/agents" className="bg-gradient-to-r from-brand-accent-start to-brand-accent-end text-black font-bold px-6 py-3 rounded-lg hover:opacity-90 transition-opacity flex items-center space-x-2 mx-auto max-w-xs justify-center">
                        <span>Go to My Agents</span>
                        <Icon icon={ICONS.CHEVRON_RIGHT} className="w-5 h-5" />
                    </Link>
                </>
            );
        }
        if (buildError) {
             return (
                 <>
                    <div className="w-20 h-20 mx-auto bg-red-500/20 flex items-center justify-center rounded-full border-2 border-red-500 mb-6">
                        <span className="text-4xl text-red-400">!</span>
                    </div>
                    <h1 className="text-3xl font-bold text-white mb-4">Build Failed</h1>
                    <p className="text-lg text-red-400 mb-8">{buildError}</p>
                    <Link to="/builder" className="bg-slate-600 hover:bg-slate-500 text-white font-semibold px-6 py-3 rounded-lg transition-colors">
                        Return to Builder
                    </Link>
                </>
            );
        }

        return (
            <>
                <div className="w-20 h-20 mx-auto bg-brand-secondary flex items-center justify-center rounded-full border-2 border-brand-accent-start mb-6">
                    <Icon icon={ICONS.GEAR} className="w-10 h-10 text-brand-accent-start animate-spin" />
                </div>
                <h1 className="text-3xl font-bold text-white mb-4">The Forge is Active</h1>
                <p className="text-lg text-slate-300 mb-8">
                    Your agent is being forged from raw code...
                </p>
            </>
        );
    };

    return (
        <div className="container mx-auto px-6 py-20">
            <div className="max-w-3xl mx-auto bg-brand-secondary border border-slate-700 rounded-xl p-8 md:p-12 text-center">
                {renderStatus()}
            </div>
            <div className="max-w-3xl mx-auto bg-black/50 border border-slate-700 rounded-xl p-4 mt-8 font-mono text-sm text-left">
                <div className="overflow-y-auto h-64">
                    {buildLogs.map((log, index) => (
                        <div key={index} className="flex items-start">
                            <span className="w-20 text-slate-500">[{log.level}]</span>
                            <span className="flex-1 text-slate-300 whitespace-pre-wrap">{log.message}</span>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default ConfirmationPage;