export interface PricingTier {
  id: string;
  name: string;
  description: string;
  price: number;
  pricePeriod?: string;
  features: string[];
  isPopular?: boolean;
}

export interface CustomBuild {
  name: string;
  botType: string;
  features: string[];
  personality: string;
  tradingTactic?: string;
  totalPrice: number;
}

export interface GeneratedFile {
  filename: string;
  content: string;
}

export interface TerminalLine {
    type: 'input' | 'output' | 'system' | 'error';
    content: string;
}

export interface BuildLogLine {
    level: 'INFO' | 'GEN' | 'VALIDATE' | 'DEPLOY' | 'SUCCESS' | 'ERROR';
    message: string;
}

export interface Agent {
    id: string;
    name: string;
    status: 'Actief' | 'Inactief';
    order: PricingTier | (CustomBuild & { name: string });
    createdAt: string;
    generatedFiles: GeneratedFile[];
}

export interface AuthContextType {
    user: { name: string } | null;
    agents: Agent[];
    login: (username: string) => void;
    logout: () => void;
    addAgent: (order: PricingTier | (CustomBuild & { name: string }), generatedFiles: GeneratedFile[]) => void;
    removeAgent: (agentId: string) => void;
}