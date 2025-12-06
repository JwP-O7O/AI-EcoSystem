import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import Icon from './Icon';
import { ICONS } from '../constants';
import { useAuth } from '../hooks/useAuth';

const Header = () => {
    const { user } = useAuth();
    const navigate = useNavigate();

    return (
        <header className="bg-brand-dark/80 backdrop-blur-sm sticky top-0 z-50 border-b border-brand-secondary">
            <div className="container mx-auto px-6 py-4 flex justify-between items-center">
                <Link to="/" className="flex items-center space-x-3">
                    <Icon icon={ICONS.CUBE} className="w-8 h-8 text-brand-accent-start" />
                    <span className="text-2xl font-bold text-white tracking-wider">AgentForge</span>
                </Link>
                <nav className="hidden md:flex items-center space-x-8">
                    <Link to="/" className="text-slate-300 hover:text-white transition-colors">Solutions</Link>
                    <Link to="/builder" className="text-slate-300 hover:text-white transition-colors">Builder</Link>
                </nav>
                {user ? (
                    <button onClick={() => navigate('/dashboard')} className="bg-gradient-to-r from-brand-accent-start to-brand-accent-end text-black font-bold px-4 py-2 rounded-lg hover:opacity-90 transition-opacity flex items-center space-x-2">
                        <span>Dashboard</span>
                        <Icon icon={ICONS.DASHBOARD} className="w-5 h-5" />
                    </button>
                ) : (
                    <button onClick={() => navigate('/login')} className="bg-slate-700 hover:bg-slate-600 text-white font-bold px-4 py-2 rounded-lg transition-colors flex items-center space-x-2">
                         <span>Login</span>
                    </button>
                )}
            </div>
        </header>
    );
};

export default Header;