import { io, Socket } from 'socket.io-client';

// API Base URL
const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8080';

// WebSocket instance
let socket: Socket | null = null;

// ==================== GATEWAY HEALTH ====================

export interface HealthStatus {
  gateway: string;
  timestamp: number;
  services: {
    [key: string]: {
      status: string;
      url?: string;
      path?: string;
    };
  };
}

export const getHealth = async (): Promise<HealthStatus> => {
  const response = await fetch(`${API_BASE}/health`);
  if (!response.ok) throw new Error('Health check failed');
  return response.json();
};

// ==================== AGENT ZERO API ====================

export interface AgentMessage {
  text: string;
  context?: string;
  broadcast?: number;
}

export interface AgentResponse {
  no: number;
  role: string;
  text: string;
  kvargs?: Record<string, any>;
}

export const sendAgentMessage = async (message: AgentMessage): Promise<AgentResponse> => {
  const response = await fetch(`${API_BASE}/api/agent/msg`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(message),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ error: 'Unknown error' }));
    throw new Error(error.error || 'Agent request failed');
  }

  return response.json();
};

export const pollAgentLogs = async (context: string, logFrom: number = 0) => {
  const response = await fetch(`${API_BASE}/api/agent/poll`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ context, log_from: logFrom }),
  });

  if (!response.ok) throw new Error('Poll failed');
  return response.json();
};

export const pauseAgent = async (context: string, paused: boolean) => {
  const response = await fetch(`${API_BASE}/api/agent/pause`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ context, paused }),
  });

  if (!response.ok) throw new Error('Pause request failed');
  return response.json();
};

// ==================== SOLANA BOT API ====================

export interface SolanaStatus {
  wallet?: {
    solBalance: number;
    tokenBalances: Record<string, number>;
  };
  activeTrades?: any[];
  tradeHistory?: any[];
  dailyPnL?: number;
  totalPnL?: number;
  isTrading?: boolean;
  systemStatus?: string;
  stats?: {
    winRate: number;
    avgReturn: number;
    maxDrawdown: number;
  };
  config?: {
    backtestMode: boolean;
    maxPositionSize: number;
    takeProfitTarget: number;
  };
}

export const getSolanaStatus = async (): Promise<SolanaStatus> => {
  const response = await fetch(`${API_BASE}/api/solana/status`);
  if (!response.ok) {
    const error = await response.json().catch(() => ({ error: 'Solana Bot unavailable' }));
    throw new Error(error.error || 'Failed to fetch Solana status');
  }
  return response.json();
};

export const startSolanaTrading = async (): Promise<{ message: string }> => {
  const response = await fetch(`${API_BASE}/api/solana/start-trading`, {
    method: 'POST',
  });

  if (!response.ok) throw new Error('Failed to start trading');
  return response.json();
};

export const stopSolanaTrading = async (): Promise<{ message: string }> => {
  const response = await fetch(`${API_BASE}/api/solana/stop-trading`, {
    method: 'POST',
  });

  if (!response.ok) throw new Error('Failed to stop trading');
  return response.json();
};

// ==================== MARKETPLACE API ====================

export interface MarketplaceRegistry {
  version: string;
  updated?: string;
  total_items?: number;
  agents: MarketplaceAgent[];
  tools?: any[];
  prompts?: any[];
  message?: string;
}

export interface MarketplaceAgent {
  id: string;
  name: string;
  version?: string;
  author?: string;
  description: string;
  category?: string;
  tags?: string[];
  downloads?: number;
  rating?: number;
  verified?: boolean;
  manifest_url?: string;
  path?: string;
  manifest?: string;
}

export const getMarketplaceRegistry = async (): Promise<MarketplaceRegistry> => {
  const response = await fetch(`${API_BASE}/api/marketplace/registry`);
  if (!response.ok) {
    // Return empty registry if not found
    return {
      version: '1.0.0',
      agents: [],
      message: 'Marketplace not available'
    };
  }
  return response.json();
};

export const getMarketplaceAgents = async (): Promise<MarketplaceAgent[]> => {
  const response = await fetch(`${API_BASE}/api/marketplace/agents`);
  if (!response.ok) return [];
  return response.json();
};

// ==================== SERVICE MANAGEMENT ====================

export const startService = async (serviceName: string) => {
  const response = await fetch(`${API_BASE}/api/services/start/${serviceName}`, {
    method: 'POST',
  });

  if (!response.ok) throw new Error(`Failed to start ${serviceName}`);
  return response.json();
};

export const getServicesStatus = async () => {
  const response = await fetch(`${API_BASE}/api/services/status`);
  if (!response.ok) throw new Error('Failed to fetch services status');
  return response.json();
};

// ==================== WEBSOCKET SUPPORT ====================

export const connectWebSocket = (): Socket => {
  if (socket && socket.connected) {
    return socket;
  }

  socket = io(API_BASE, {
    transports: ['websocket', 'polling'],
    reconnection: true,
    reconnectionDelay: 1000,
    reconnectionAttempts: 5,
  });

  socket.on('connect', () => {
    console.log('✅ WebSocket connected');
  });

  socket.on('disconnect', (reason) => {
    console.log('❌ WebSocket disconnected:', reason);
  });

  socket.on('connect_error', (error) => {
    console.error('WebSocket connection error:', error);
  });

  return socket;
};

export const disconnectWebSocket = () => {
  if (socket) {
    socket.disconnect();
    socket = null;
  }
};

export const getSocket = (): Socket | null => socket;

// ==================== UTILITY FUNCTIONS ====================

export const isServiceAvailable = async (serviceName: 'agent' | 'solana' | 'marketplace'): Promise<boolean> => {
  try {
    const health = await getHealth();
    const service = health.services[serviceName === 'agent' ? 'agent_zero' : serviceName === 'solana' ? 'solana_bot' : 'marketplace'];
    return service && service.status === 'healthy';
  } catch {
    return false;
  }
};

export default {
  getHealth,
  sendAgentMessage,
  pollAgentLogs,
  pauseAgent,
  getSolanaStatus,
  startSolanaTrading,
  stopSolanaTrading,
  getMarketplaceRegistry,
  getMarketplaceAgents,
  startService,
  getServicesStatus,
  connectWebSocket,
  disconnectWebSocket,
  getSocket,
  isServiceAvailable,
};
