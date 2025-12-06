import React, { createContext, useContext, useState, useEffect } from 'react';
import { AuthContextType, Agent, PricingTier, CustomBuild, GeneratedFile } from '../types';

export const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<{ name: string } | null>(null);
  const [agents, setAgents] = useState<Agent[]>([]);

  // Load state from localStorage
  useEffect(() => {
    const storedUser = localStorage.getItem('agent_forge_user');
    const storedAgents = localStorage.getItem('agent_forge_agents');
    
    if (storedUser) setUser(JSON.parse(storedUser));
    if (storedAgents) setAgents(JSON.parse(storedAgents));
  }, []);

  const login = (username: string) => {
    const newUser = { name: username };
    setUser(newUser);
    localStorage.setItem('agent_forge_user', JSON.stringify(newUser));
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem('agent_forge_user');
  };

  const addAgent = (order: PricingTier | (CustomBuild & { name: string }), generatedFiles: GeneratedFile[]) => {
    const newAgent: Agent = {
      id: Date.now().toString(),
      name: order.name,
      status: 'Actief',
      order: order,
      createdAt: new Date().toISOString(),
      generatedFiles: generatedFiles
    };
    
    const updatedAgents = [...agents, newAgent];
    setAgents(updatedAgents);
    localStorage.setItem('agent_forge_agents', JSON.stringify(updatedAgents));
  };

  const removeAgent = (agentId: string) => {
    const updatedAgents = agents.filter(a => a.id !== agentId);
    setAgents(updatedAgents);
    localStorage.setItem('agent_forge_agents', JSON.stringify(updatedAgents));
  };

  return (
    <AuthContext.Provider value={{ user, agents, login, logout, addAgent, removeAgent }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
