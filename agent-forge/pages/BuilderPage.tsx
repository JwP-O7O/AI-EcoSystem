import React, { useState, useMemo, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { BUILDER_OPTIONS, ICONS } from '../constants';
import { getAdvice } from '../services/geminiService';
import Icon from '../components/Icon';

const BuilderPage = () => {
    const [botType, setBotType] = useState<string>('');
    const [selectedFeatures, setSelectedFeatures] = useState<string[]>([]);
    const [personality, setPersonality] = useState<string>(BUILDER_OPTIONS.personalities[0]);
    const [tradingTactic, setTradingTactic] = useState<string>('');
    const [advice, setAdvice] = useState<string>('');
    const [isLoadingAdvice, setIsLoadingAdvice] = useState<boolean>(false);
    
    const navigate = useNavigate();

    const isTradingBot = useMemo(() => botType === 'Trading Bot', [botType]);

    useEffect(() => {
        if (!isTradingBot) {
            setTradingTactic('');
        }
    }, [isTradingBot]);

    const handleFeatureToggle = (featureName: string) => {
        setSelectedFeatures(prev =>
            prev.includes(featureName)
                ? prev.filter(f => f !== featureName)
                : [...prev, featureName]
        );
    };

    const totalPrice = useMemo(() => {
        const botPrice = BUILDER_OPTIONS.botTypes.find(m => m.name === botType)?.price || 0;
        const tacticPrice = BUILDER_OPTIONS.tradingTactics.find(t => t.name === tradingTactic)?.price || 0;
        const featuresPrice = selectedFeatures.reduce((acc, featureName) => {
            return acc + (BUILDER_OPTIONS.features.find(f => f.name === featureName)?.price || 0);
        }, 0);
        return botPrice + featuresPrice + tacticPrice;
    }, [botType, selectedFeatures, tradingTactic]);

    const handleGetAdvice = async () => {
        if (!botType) return;
        setIsLoadingAdvice(true);
        setAdvice('');
        try {
            const result = await getAdvice({ botType, features: selectedFeatures, tradingTactic });
            setAdvice(result);
        } catch (error) {
            console.error("Error fetching advice from Gemini:", error);
            setAdvice("Sorry, I was unable to get advice at this time. Please try again later.");
        } finally {
            setIsLoadingAdvice(false);
        }
    };
    
    const handleCheckout = () => {
        if (!botType) {
            alert("Please select a bot type to proceed.");
            return;
        }
        const build = {
            name: `Custom ${botType}`,
            botType,
            features: selectedFeatures,
            personality,
            tradingTactic: isTradingBot ? tradingTactic : undefined,
            totalPrice
        };
        navigate('/checkout', { state: { customBuild: build } });
    }

    const Section = ({ title, step, children }: { title: string, step: number, children: React.ReactNode }) => (
        <div className="bg-brand-secondary/50 border border-slate-700/50 rounded-lg p-6">
            <h2 className="text-2xl font-semibold text-white mb-5"><span className="text-brand-accent-start">{step}.</span> {title}</h2>
            {children}
        </div>
    );

    return (
        <div className="container mx-auto px-6 py-16">
            <h1 className="text-4xl font-extrabold text-center text-white mb-4">Agent Builder</h1>
            <p className="text-lg text-slate-400 text-center max-w-3xl mx-auto mb-12">Craft your perfect AI by selecting its core type, capabilities, and personality. Your agent's blueprint and cost will update in real-time.</p>
            
            <div className="grid lg:grid-cols-3 gap-8 items-start">
                <div className="lg:col-span-2 space-y-8">
                    <Section title="Choose a Core Bot Type" step={1}>
                        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
                            {BUILDER_OPTIONS.botTypes.map(model => (
                                <button key={model.name} onClick={() => setBotType(model.name)} className={`p-4 rounded-lg text-left transition-all border-2 h-full flex flex-col ${botType === model.name ? 'bg-brand-secondary border-brand-accent-start shadow-[0_0_10px_rgba(0,191,255,0.4)]' : 'bg-brand-secondary border-slate-700 hover:border-slate-500'}`}>
                                    <h3 className="font-bold text-white flex-grow">{model.name}</h3>
                                    <p className="text-sm text-slate-400 my-2">{model.description}</p>
                                    <span className="text-lg font-semibold text-white mt-auto">€{model.price}</span>
                                </button>
                            ))}
                        </div>
                    </Section>

                    {isTradingBot && (
                         <Section title="Select a Trading Tactic" step={2}>
                            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
                                {BUILDER_OPTIONS.tradingTactics.map(tactic => (
                                     <button key={tactic.name} onClick={() => setTradingTactic(tactic.name)} className={`p-4 rounded-lg text-left transition-all border-2 h-full flex flex-col ${tradingTactic === tactic.name ? 'bg-brand-secondary border-brand-accent-start shadow-[0_0_10px_rgba(0,191,255,0.4)]' : 'bg-brand-secondary border-slate-700 hover:border-slate-500'}`}>
                                        <h3 className="font-bold text-white flex-grow">{tactic.name}</h3>
                                        <p className="text-sm text-slate-400 my-2">{tactic.description}</p>
                                        <span className="text-lg font-semibold text-white">€{tactic.price}</span>
                                    </button>
                                ))}
                            </div>
                        </Section>
                    )}
                    
                    <Section title={`Add Capabilities`} step={isTradingBot ? 3 : 2}>
                        <div className="grid md:grid-cols-2 gap-4">
                            {BUILDER_OPTIONS.features.map(feature => (
                                <label key={feature.name} className={`p-4 rounded-lg flex items-center justify-between cursor-pointer transition-all border-2 ${selectedFeatures.includes(feature.name) ? 'bg-brand-secondary border-brand-accent-start shadow-[0_0_10px_rgba(0,191,255,0.4)]' : 'bg-brand-secondary border-slate-700 hover:border-slate-500'}`}>
                                    <div>
                                        <h3 className="font-bold text-white">{feature.name}</h3>
                                        <p className="text-sm text-slate-400">{feature.description}</p>
                                        <span className="font-semibold text-white">€{feature.price}</span>
                                    </div>
                                    <input type="checkbox" checked={selectedFeatures.includes(feature.name)} onChange={() => handleFeatureToggle(feature.name)} className="form-checkbox h-5 w-5 bg-slate-700 border-slate-500 text-brand-accent-start rounded focus:ring-brand-accent-start" />
                                </label>
                            ))}
                        </div>
                    </Section>

                    <Section title={`Define Personality`} step={isTradingBot ? 4 : 3}>
                        <select value={personality} onChange={(e) => setPersonality(e.target.value)} className="w-full bg-brand-secondary border-2 border-slate-700 rounded-lg p-3 text-white focus:ring-brand-accent-start focus:border-brand-accent-start">
                            {BUILDER_OPTIONS.personalities.map(p => <option key={p} value={p}>{p}</option>)}
                        </select>
                    </Section>
                </div>
                
                <div className="lg:col-span-1">
                    <div className="bg-brand-secondary border border-slate-700 rounded-xl p-6 sticky top-24">
                        <h2 className="text-2xl font-bold text-white mb-6 text-center">Agent Blueprint</h2>
                        
                        <div className="space-y-3 mb-6 font-mono text-sm">
                            <div className="flex justify-between items-center">
                                <span className="text-slate-400">Type:</span>
                                <span className="text-white font-semibold text-right">{botType || 'Not Selected'}</span>
                            </div>
                            {isTradingBot && (
                                <div className="flex justify-between items-center">
                                    <span className="text-slate-400">Tactic:</span>
                                    <span className="text-white font-semibold text-right">{tradingTactic || 'Not Selected'}</span>
                                </div>
                            )}
                            <div className="flex justify-between items-center">
                                <span className="text-slate-400">Personality:</span>
                                <span className="text-white font-semibold">{personality}</span>
                            </div>
                             <div className="flex justify-between items-start">
                                <span className="text-slate-400">Capabilities:</span>
                                <span className="text-white font-semibold text-right">{selectedFeatures.length > 0 ? selectedFeatures.join(', ') : 'None'}</span>
                            </div>
                        </div>

                        <div className="bg-brand-dark/50 p-4 rounded-lg mb-6">
                             <h3 className="text-lg font-semibold text-white mb-2 flex items-center space-x-2">
                                <Icon icon={ICONS.SPARKLES} className="text-brand-accent-end" />
                                <span>AI Architect</span>
                             </h3>
                             <p className="text-sm text-slate-400 mb-3">Get expert advice on your current configuration.</p>
                             <button onClick={handleGetAdvice} disabled={isLoadingAdvice || !botType} className="w-full bg-slate-600 hover:bg-slate-500 text-white font-semibold px-4 py-2 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed">
                                {isLoadingAdvice ? "Thinking..." : "Ask for Advice"}
                             </button>
                             {advice && (
                                <div className="mt-3 p-3 bg-brand-secondary/50 border border-brand-accent-end/30 rounded-lg text-slate-300 text-sm">
                                    <p className="whitespace-pre-wrap">{advice}</p>
                                </div>
                            )}
                        </div>

                        <div className="border-t border-slate-700 my-4"></div>
                        <div className="flex justify-between items-center mb-6">
                            <span className="text-xl text-slate-300">Total Cost:</span>
                            <span className="text-3xl font-extrabold text-white">€{totalPrice}</span>
                        </div>
                        <button onClick={handleCheckout} disabled={!botType || (isTradingBot && !tradingTactic)} className="w-full bg-gradient-to-r from-brand-accent-start to-brand-accent-end text-black font-bold py-3 rounded-lg hover:opacity-90 transition-opacity disabled:opacity-50 disabled:cursor-not-allowed">
                            Proceed to Checkout
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default BuilderPage;