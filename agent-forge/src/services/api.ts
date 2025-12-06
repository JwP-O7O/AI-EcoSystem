import { Message, SystemStatus } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const DEFAULT_SESSION_ID = 'session_1';

export const api = {
  async sendMessage(content: string, sessionId: string = DEFAULT_SESSION_ID): Promise<Message> {
    try {
      const response = await fetch(`${API_BASE_URL}/chat/${sessionId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: content,
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to send message');
      }

      const data = await response.json();
      return {
        role: 'assistant',
        content: data.response,
        timestamp: new Date().toISOString(),
      };
    } catch (error) {
      console.error('API Error:', error);
      throw error;
    }
  },

  async checkHealth(): Promise<SystemStatus> {
    try {
      const response = await fetch(`${API_BASE_URL}/health`);
      if (!response.ok) {
         return { cpu: 0, memory: 0, active_agents: 0, uptime: 0 };
      }
      const data = await response.json();
      // Map backend response to frontend interface
      // Backend returns: { status: "operational", active_agents: 1, version: "2.0.0" }
      return { 
        cpu: 15, // Mock data as backend doesn't provide this yet
        memory: 40, // Mock data
        active_agents: data.active_agents || 0, 
        uptime: 1234 // Mock data
      };
    } catch (error) {
      console.error('Health Check Error:', error);
      return { cpu: 0, memory: 0, active_agents: 0, uptime: 0 };
    }
  }
};
