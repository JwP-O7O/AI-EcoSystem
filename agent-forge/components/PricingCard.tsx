import React from 'react';
import { Link } from 'react-router-dom';
import { PricingTier } from '../types';
import Icon from './Icon';
import { ICONS } from '../constants';

interface PricingCardProps {
    tier: PricingTier;
}

const PricingCard: React.FC<PricingCardProps> = ({ tier }) => {
    const cardClasses = `
        bg-brand-secondary rounded-xl p-8 flex flex-col h-full transition-all duration-300 transform hover:-translate-y-2
        ${tier.isPopular ? 'border-2 border-brand-green shadow-[0_0_20px_rgba(0,255,127,0.3)]' : 'border border-slate-700 hover:border-slate-500'}
    `;

    return (
        <div className={cardClasses}>
            {tier.isPopular && (
                <div className="absolute top-0 -translate-y-1/2 left-1/2 -translate-x-1/2 bg-brand-green text-black text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">
                    Most Popular
                </div>
            )}
            <h3 className="text-2xl font-bold text-white mb-2">{tier.name}</h3>
            <p className="text-slate-400 mb-6 flex-grow">{tier.description}</p>
            
            <div className="mb-6">
                <span className="text-5xl font-extrabold text-white">€{tier.price}</span>
                <span className="text-slate-400"> {tier.pricePeriod || 'eenmalig'}</span>
            </div>
            
            <ul className="space-y-4 mb-8">
                {tier.features.map((feature, index) => (
                    <li key={index} className="flex items-start">
                        <Icon icon={ICONS.CHECK} className={`w-6 h-6 ${tier.isPopular ? 'text-brand-green' : 'text-brand-accent-start'} mr-3 mt-1 flex-shrink-0`} />
                        <span className="text-slate-300">{feature}</span>
                    </li>
                ))}
            </ul>
            
            <Link to={`/checkout?plan=${tier.id}`} className={`mt-auto w-full text-center font-bold py-3 rounded-lg transition-all ${tier.isPopular ? 'bg-brand-green text-black hover:opacity-90' : 'bg-gradient-to-r from-brand-accent-start to-brand-accent-end text-black opacity-80 hover:opacity-100'}`}>
                Get Started
            </Link>
        </div>
    );
};

export default PricingCard;