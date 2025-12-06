import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate, Link } from 'react-router-dom';
import { PRICING_TIERS } from '../constants';
import { PricingTier, CustomBuild } from '../types';

const CheckoutPage = () => {
    const location = useLocation();
    const navigate = useNavigate();
    const [plan, setPlan] = useState<PricingTier | null>(null);
    const [customBuild, setCustomBuild] = useState<CustomBuild | null>(null);
    const [email, setEmail] = useState('');
    const [isProcessing, setIsProcessing] = useState(false);

    useEffect(() => {
        if(location.state?.customBuild) {
            setCustomBuild(location.state.customBuild);
        } else {
            const queryParams = new URLSearchParams(location.search);
            const planId = queryParams.get('plan');
            const foundPlan = PRICING_TIERS.find(p => p.id === planId);
            if (foundPlan) {
                setPlan(foundPlan);
            }
        }
    }, [location]);

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if(!email) {
            alert("Please enter your email address.");
            return;
        }
        setIsProcessing(true);
        // Simulate payment processing
        setTimeout(() => {
            const orderDetails = customBuild ? { ...customBuild, id: `custom_${Date.now()}` } : plan;
            navigate('/confirmation', { state: { email, order: orderDetails } });
        }, 2000);
    };
    
    const item = customBuild ? { name: customBuild.name, price: customBuild.totalPrice } : plan;

    if (!item) {
        return (
            <div className="text-center py-20">
                <h2 className="text-2xl text-white">No plan selected.</h2>
                <Link to="/" className="text-brand-accent-start hover:text-brand-accent-end mt-4 inline-block">Return to plans</Link>
            </div>
        );
    }
    
    return (
        <div className="container mx-auto px-6 py-16">
            <div className="max-w-2xl mx-auto">
                <h1 className="text-4xl font-extrabold text-center text-white mb-12">Finalize Your Order</h1>
                <div className="bg-brand-secondary border border-slate-700 rounded-xl p-8 shadow-2xl shadow-brand-accent-end/10">
                    <div className="flex justify-between items-center mb-6 pb-6 border-b border-slate-700">
                        <h2 className="text-xl font-semibold text-white">{item.name}</h2>
                        <span className="text-2xl font-bold text-white">€{item.price}</span>
                    </div>
                    
                    <form onSubmit={handleSubmit}>
                        <div className="space-y-6">
                            <div>
                                <label htmlFor="email" className="block text-sm font-medium text-slate-300 mb-2">Email Address</label>
                                <input type="email" id="email" value={email} onChange={(e) => setEmail(e.target.value)} className="w-full bg-slate-800 border border-slate-600 rounded-lg p-3 text-white focus:ring-brand-accent-start focus:border-brand-accent-start" placeholder="you@example.com" required />
                                <p className="text-xs text-slate-500 mt-2">Your agent's code and documentation will be sent here.</p>
                            </div>
                            
                            <div>
                                <label className="block text-sm font-medium text-slate-300 mb-2">Payment Details</label>
                                <div className="bg-slate-800 border border-slate-600 rounded-lg p-3 text-slate-400">
                                    Simulated Credit Card Input
                                </div>
                            </div>
                        </div>

                        <div className="mt-8">
                            <button type="submit" disabled={isProcessing} className="w-full bg-gradient-to-r from-brand-accent-start to-brand-accent-end text-black font-bold py-3 rounded-lg hover:opacity-90 transition-opacity disabled:opacity-50 disabled:cursor-not-allowed">
                                {isProcessing ? 'Processing...' : `Pay €${item.price} and Forge Agent`}
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    );
};

export default CheckoutPage;