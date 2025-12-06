export interface Message {
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: string;
}

export interface SystemStatus {
  cpu: number;
  memory: number;
  active_agents: number;
  uptime: number;
}
