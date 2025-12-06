import React from 'react';
import Hero from '../components/Hero';
import PricingCard from '../components/PricingCard';
import FeatureCard from '../components/FeatureCard';
import { PRICING_TIERS, ICONS } from '../constants';

const HomePage = () => {
    return (
        <div>
            <Hero />

            <div className="py-20 bg-brand-dark">
                <div className="container mx-auto px-6">
                    <div className="text-center mb-16">
                        <h2 className="text-3xl md:text-4xl font-bold text-white">From Concept to Command in Minutes</h2>
                        <p className="text-lg text-slate-400 max-w-3xl mx-auto mt-4">A seamless three-step process to design, build, and take control of your custom AI agent.</p>
                    </div>
                    <div className="grid md:grid-cols-3 gap-8">
                        <FeatureCard 
                            step={1}
                            icon={ICONS.CUBE}
                            title="Design Your Agent"
                            description="Use our intuitive builder to select your agent's type, skills, and personality, or choose a pre-configured model."
                        />
                        <FeatureCard
                            step={2}
                            icon={ICONS.CODE}
                            title="Forge & Deploy"
                            description="Our AI Forge writes, validates, and deploys the code for your agent into a secure, live environment in real-time."
                        />
                        <FeatureCard
                            step={3}
                            icon={ICONS.COMMAND}
                            title="Take Command"
                            description="Your agent appears instantly in your Command Center, ready to be controlled and tasked via the live terminal."
                        />
                    </div>
                </div>
            </div>

            <div className="py-20">
                <div className="container mx-auto px-6">
                    <div className="text-center mb-16">
                        <h2 className="text-3xl md:text-4xl font-bold text-white">Flexible Plans for Any Mission</h2>
                        <p className="text-lg text-slate-400 max-w-2xl mx-auto mt-4">Whether you need a single-task bot or a full suite of autonomous agents, we have a plan that fits your objective.</p>
                    </div>
                    <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-6xl mx-auto">
                        {PRICING_TIERS.map(tier => (
                            <PricingCard key={tier.id} tier={tier} />
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default HomePage;