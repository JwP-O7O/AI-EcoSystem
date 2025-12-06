import { ai } from './ai';
import { PricingTier, CustomBuild, GeneratedFile } from '../types';

interface BuildSelections {
    botType: string;
    features: string[];
    tradingTactic?: string;
}

export async function getAdvice(selections: BuildSelections): Promise<string> {
    const prompt = `
        You are an Expert Solutions Architect at AgentForge. A user is building a custom AI agent.
        Based on their current selections, provide a brief, insightful, and encouraging recommendation for a complementary feature or a potential use case.
        Do not be pushy or upsell. Be a helpful expert. Keep your response to 2-3 concise sentences.

        User's Selections:
        - Bot Type: ${selections.botType}
        ${selections.tradingTactic ? `- Trading Tactic: ${selections.tradingTactic}` : ''}
        - Features: ${selections.features.join(', ') || 'None'}

        Your Expert Advice:
    `;

    try {
        const response = await ai.models.generateContent({
            model: 'gemini-2.5-flash',
            contents: prompt,
            config: {
                temperature: 0.7,
            }
        });
        
        return response.text.trim();

    } catch (error) {
        console.error("Gemini API call for advice failed:", error);
        throw new Error("Could not get advice from the AI consultant.");
    }
}

export async function getAgentResponse(
    order: PricingTier | (CustomBuild & { name: string }),
    files: GeneratedFile[],
    conversationHistory: string[],
    command: string
): Promise<string> {
    const agentName = order.name;
    const agentPersonality = 'personality' in order ? order.personality : "Professioneel";
    const mainAgentFile = files.find(f => f.filename === 'agent.py')?.content || '';
    const agentFeatures = 'features' in order ? order.features : [];

    const prompt = `
        You are an AI agent responding to a user within a simulated terminal.
        Your persona and capabilities are defined by the following context.
        Generate a concise, in-character response to the user's command, considering the conversation history.

        CONTEXT:
        - Agent Name: ${agentName}
        - Agent Personality: ${agentPersonality}
        - Agent Features: ${agentFeatures.join(', ')}
        - Core Logic (agent.py excerpt): """${mainAgentFile.substring(0, 1000)}..."""
        - Conversation History (last few lines): 
          ${conversationHistory.slice(-4).join('\n')}

        USER'S COMMAND: "${command}"

        YOUR RESPONSE (as stdout):
    `;

    try {
        const response = await ai.models.generateContent({
            model: 'gemini-2.5-flash',
            contents: prompt,
            config: {
                temperature: 0.6,
            }
        });
        
        return response.text.trim();

    } catch (error) {
        console.error("Gemini API call for agent response failed:", error);
        throw new Error("Could not get a response from the agent.");
    }
}