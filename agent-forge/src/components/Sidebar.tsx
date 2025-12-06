import React from 'react';
import { Activity, Cpu, HardDrive, Network, Settings, Database, Code, Zap } from 'lucide-react';
import { SystemStatus } from '../types';

interface SidebarProps {
  status: SystemStatus;
}

export const Sidebar: React.FC<SidebarProps> = ({ status }) => {
  return (
    <div className="w-80 bg-slate-900/90 border-r border-slate-700/50 p-6 flex flex-col backdrop-blur-md">
      <div className="flex items-center gap-3 mb-10">
        <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center shadow-lg shadow-blue-500/20">
          <Zap className="text-white" size={24} />
        </div>
        <div>
          <h1 className="font-bold text-xl tracking-tight bg-gradient-to-r from-white to-slate-400 bg-clip-text text-transparent">
            Agent Forge
          </h1>
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
            <span className="text-xs text-emerald-500 font-medium tracking-wide">SYSTEM ONLINE</span>
          </div>
        </div>
      </div>

      <div className="space-y-8">
        <div className="space-y-4">
          <h2 className="text-xs font-bold text-slate-500 uppercase tracking-widest px-2">System Status</h2>
          
          <div className="bg-slate-800/50 rounded-xl p-4 border border-slate-700/50 space-y-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3 text-slate-300">
                <Cpu size={16} className="text-blue-400" />
                <span className="text-sm font-medium">CPU Load</span>
              </div>
              <span className="text-sm font-mono text-blue-400">{status.cpu}%</span>
            </div>
            <div className="w-full bg-slate-700/50 h-1.5 rounded-full overflow-hidden">
              <div 
                className="bg-blue-500 h-full rounded-full transition-all duration-500"
                style={{ width: `${status.cpu}%` }}
              />
            </div>

            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3 text-slate-300">
                <HardDrive size={16} className="text-purple-400" />
                <span className="text-sm font-medium">Memory</span>
              </div>
              <span className="text-sm font-mono text-purple-400">{status.memory}%</span>
            </div>
            <div className="w-full bg-slate-700/50 h-1.5 rounded-full overflow-hidden">
              <div 
                className="bg-purple-500 h-full rounded-full transition-all duration-500"
                style={{ width: `${status.memory}%` }}
              />
            </div>

            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3 text-slate-300">
                <Activity size={16} className="text-emerald-400" />
                <span className="text-sm font-medium">Active Agents</span>
              </div>
              <span className="text-sm font-mono text-emerald-400">{status.active_agents}</span>
            </div>
          </div>
        </div>

        <nav className="space-y-2">
          <h2 className="text-xs font-bold text-slate-500 uppercase tracking-widest px-2 mb-4">Modules</h2>
          
          {[
            { icon: Network, label: 'Agent Network', active: true },
            { icon: Database, label: 'Knowledge Base', active: false },
            { icon: Code, label: 'Tool Registry', active: false },
            { icon: Settings, label: 'Configuration', active: false },
          ].map((item, i) => (
            <button
              key={i}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-all duration-200 ${
                item.active 
                  ? 'bg-blue-500/10 text-blue-400 border border-blue-500/20' 
                  : 'text-slate-400 hover:bg-slate-800/50 hover:text-slate-200'
              }`}
            >
              <item.icon size={18} />
              {item.label}
            </button>
          ))}
        </nav>
      </div>
      
      <div className="mt-auto pt-6 border-t border-slate-800">
         <div className="text-xs text-slate-500 text-center">
            v2.5.0-alpha
         </div>
      </div>
    </div>
  );
};
