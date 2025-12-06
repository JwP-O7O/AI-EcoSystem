const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

// Basic Auth credentials (default for Agent Zero)
const AUTH = {
    username: 'admin',
    password: 'admin' // Dit kan later via .env worden aangepast
};

const getHeaders = () => {
    const headers = new Headers();
    headers.set('Content-Type', 'application/json');
    headers.set('Authorization', 'Basic ' + btoa(AUTH.username + ":" + AUTH.password));
    return headers;
};

export interface AgentMessage {
    text: string;
    context?: string;
    broadcast?: number;
}

export interface AgentResponse {
    ok: boolean;
    message: string | any;
    [key: string]: any;
}

export const api = {
    /**
     * Send a message to Agent Zero (Async)
     */
    sendMessage: async (text: string, contextId: string = ''): Promise<AgentResponse> => {
        const response = await fetch(`${API_URL}/msg`, {
            method: 'POST',
            headers: getHeaders(),
            body: JSON.stringify({ text, context: contextId, broadcast: 1 })
        });
        return response.json();
    },

    /**
     * Send a message to Agent Zero (Sync - waits for reply)
     */
    sendMessageSync: async (text: string, contextId: string = ''): Promise<AgentResponse> => {
        const response = await fetch(`${API_URL}/msg_sync`, {
            method: 'POST',
            headers: getHeaders(),
            body: JSON.stringify({ text, context: contextId })
        });
        return response.json();
    },

    /**
     * Poll for logs/updates
     */
    poll: async (contextId: string = '', logFrom: number = 0): Promise<AgentResponse> => {
        const response = await fetch(`${API_URL}/poll`, {
            method: 'POST',
            headers: getHeaders(),
            body: JSON.stringify({ context: contextId, log_from: logFrom })
        });
        return response.json();
    },

    /**
     * Pause/Unpause Agent
     */
    setPaused: async (paused: boolean, contextId: string = ''): Promise<AgentResponse> => {
        const response = await fetch(`${API_URL}/pause`, {
            method: 'POST',
            headers: getHeaders(),
            body: JSON.stringify({ paused, context: contextId })
        });
        return response.json();
    },

    /**
     * Health Check
     */
    checkHealth: async (): Promise<boolean> => {
        try {
            const response = await fetch(`${API_URL}/ok`);
            return response.ok;
        } catch (e) {
            return false;
        }
    }
};
