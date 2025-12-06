import React from 'react';
import Icon from './Icon';

interface FeatureCardProps {
    icon: React.ReactNode;
    title: string;
    description: string;
    step: number;
}

const FeatureCard: React.FC<FeatureCardProps> = ({ icon, title, description, step }) => {
    return (
        <div className="bg-brand-secondary p-8 rounded-lg border border-slate-700/50 relative overflow-hidden transition-all duration-300 hover:border-slate-600/80 hover:shadow-2xl hover:shadow-brand-accent-end/10">
             <div className="absolute -top-2 -right-2 bg-brand-accent-end/10 text-brand-accent-end font-bold text-3xl w-16 h-16 flex items-center justify-center rounded-bl-full rounded-tr-lg opacity-50">
                {step}
            </div>
            <div className="mb-4 bg-slate-800/50 w-16 h-16 flex items-center justify-center rounded-lg">
                <Icon icon={icon} />
            </div>
            <h3 className="text-xl font-bold text-white mb-2">{title}</h3>
            <p className="text-slate-400 leading-relaxed">{description}</p>
        </div>
    );
};

export default FeatureCard;