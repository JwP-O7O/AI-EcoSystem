import React from 'react';
import { useAuth } from '../../hooks/useAuth';
import AgentCard from '../../components/AgentCard';
import { Link } from 'react-router-dom';
import Icon from '../../components/Icon';
import { ICONS } from '../../constants';

const AgentsPage = () => {
    const { agents } = useAuth();

    return (
        <div>
            <h1 className="text-3xl font-bold text-white mb-6">My Agents</h1>
            {agents.length > 0 ? (
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    {agents.map(agent => (
                        <AgentCard key={agent.id} agent={agent} />
                    ))}
                </div>
            ) : (
                <div className="text-center py-16 px-8 bg-brand-secondary border-2 border-dashed border-slate-700 rounded-xl">
                    <h2 className="text-xl font-semibold text-white">Your Agent Roster is Empty</h2>
                    <p className="text-slate-400 mt-2 mb-6">You have not yet forged any AI agents. It's time to build your first one!</p>
                    <Link
                        to="/builder"
                        className="bg-gradient-to-r from-brand-accent-start to-brand-accent-end text-black font-bold px-6 py-3 rounded-lg hover:opacity-90 transition-opacity inline-flex items-center space-x-2"
                    >
                        <Icon icon={ICONS.CUBE} />
                        <span>Forge Your First Agent</span>
                    </Link>
                </div>
            )}
        </div>
    );
};

export default AgentsPage;