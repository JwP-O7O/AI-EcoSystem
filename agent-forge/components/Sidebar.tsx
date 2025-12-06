import React from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import Icon from './Icon';
import { ICONS } from '../constants';

const Sidebar = () => {
    const { logout, user } = useAuth();
    const navigate = useNavigate();

    const handleLogout = () => {
        logout();
        navigate('/');
    };
    
    const baseLinkClass = "flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors";
    const inactiveLinkClass = "text-slate-300 hover:bg-brand-secondary hover:text-white";
    const activeLinkClass = "bg-brand-secondary text-white font-semibold shadow-inner";

    return (
        <div className="bg-brand-secondary/50 border border-slate-700 rounded-xl p-4 sticky top-24">
            <div className="p-4 mb-4 border-b border-slate-700">
                <h2 className="text-lg font-bold text-white truncate">Welcome, {user?.name}</h2>
                <p className="text-sm text-slate-400">Command Center</p>
            </div>
            <nav className="space-y-2">
                 <NavLink 
                    to="/dashboard/agents" 
                    end
                    className={({ isActive }) => `${baseLinkClass} ${isActive ? activeLinkClass : inactiveLinkClass}`}
                >
                    <Icon icon={ICONS.AGENTS} className="w-6 h-6" />
                    <span>My Agents</span>
                </NavLink>
                 <NavLink 
                    to="/builder" 
                    className={`${baseLinkClass} text-slate-300 bg-gradient-to-r from-brand-accent-start/80 to-brand-accent-end/80 text-black font-bold hover:opacity-90 my-4 block`}
                >
                    <Icon icon={ICONS.CUBE} className="w-6 h-6" />
                    <span>Forge New Agent</span>
                </NavLink>
                <NavLink 
                    to="/dashboard/account" 
                    className={({ isActive }) => `${baseLinkClass} ${isActive ? activeLinkClass : inactiveLinkClass}`}
                >
                    <Icon icon={ICONS.GEAR} className="w-6 h-6" />
                    <span>Account</span>
                </NavLink>
                <button 
                    onClick={handleLogout} 
                    className={`${baseLinkClass} ${inactiveLinkClass} w-full`}
                >
                    <Icon icon={ICONS.LOGOUT} className="w-6 h-6" />
                    <span>Logout</span>
                </button>
            </nav>
        </div>
    );
};

export default Sidebar;