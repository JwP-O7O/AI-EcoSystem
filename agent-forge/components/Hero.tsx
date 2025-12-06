import React from 'react';
import { Link } from 'react-router-dom';
import Icon from './Icon';
import { ICONS } from '../constants';

const Hero = () => {
    return (
        <div className="py-24 md:py-32 text-center relative overflow-hidden">
             <div className="absolute inset-0 bg-grid-pattern opacity-10"></div>
             <div className="absolute inset-0 bg-gradient-to-b from-brand-dark via-brand-dark to-transparent"></div>
            <div className="container mx-auto px-6 relative">
                <h1 className="text-4xl md:text-6xl font-extrabold text-white leading-tight mb-4 animate-fade-in-up">
                    Forge, Deploy & Command<br />Your Autonomous AI Workforce
                </h1>
                <p className="text-lg md:text-xl text-slate-300 max-w-3xl mx-auto mb-8 animate-fade-in-up" style={{ animationDelay: '200ms' }}>
                   From concept to code to command. Design your perfect agent, and our Forge builds and deploys it into a live environment, ready for your instructions.
                </p>
                <div className="flex justify-center space-x-4 animate-fade-in-up" style={{ animationDelay: '400ms' }}>
                    <Link to="/builder" className="bg-gradient-to-r from-brand-accent-start to-brand-accent-end text-black font-bold px-8 py-4 rounded-lg hover:opacity-90 transition-transform hover:scale-105 text-lg flex items-center space-x-2">
                        <span>Start Forging</span>
                        <Icon icon={ICONS.CHEVRON_RIGHT} className="w-5 h-5" />
                    </Link>
                </div>
            </div>
             <style>{`
                @keyframes fade-in-up {
                    from { opacity: 0; transform: translateY(20px); }
                    to { opacity: 1; transform: translateY(0); }
                }
                .animate-fade-in-up {
                    animation: fade-in-up 0.6s ease-out forwards;
                }
                .bg-grid-pattern {
                    background-image: linear-gradient(to right, #10142A 1px, transparent 1px), linear-gradient(to bottom, #10142A 1px, transparent 1px);
                    background-size: 40px 40px;
                }
            `}</style>
        </div>
    );
};

export default Hero;