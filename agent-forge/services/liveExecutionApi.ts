import { ai } from './ai';
import { GeneratedFile, PricingTier, CustomBuild, TerminalLine } from '../types';

/**
 * Simulates an API call to a backend "Live Execution Environment".
 * This function interprets the context (generated code, command) and uses Gemini
 * to generate a realistic output of the "executed" command.
 */
export async function runInCloud(
    command: string,
    files: GeneratedFile[],
    order: PricingTier | (CustomBuild & { name: string }),
    conversationHistory: TerminalLine[]
): Promise<string> {
    // Simulate network latency for realism
    await new Promise(resolve => setTimeout(resolve, 400 + Math.random() * 400));

    const agentName = order.name;
    const agentPersonality = 'personality' in order ? order.personality : "Professioneel";
    const mainAgentFile = files.find(f => f.filename === 'agent.py')?.content || '';
    const mainPyFile = files.find(f => f.filename === 'main.py')?.content || '';
    const agentFeatures = 'features' in order ? order.features : [];

    const prompt = `
        You are the backend server for the "Live Execution Environment". You are receiving a command from a user via a web-terminal.
        Your task is to simulate what would happen if this command was executed in a shell where the user's generated Python agent is running.
        Generate ONLY the stdout of the command. Be concise and direct, as a real terminal would be.

        CONTEXT:
        - Agent Name: ${agentName}
        - Agent Personality: ${agentPersonality}
        - Agent Features: ${agentFeatures.join(', ')}
        - Core Logic (agent.py): """${mainAgentFile.substring(0, 1000)}..."""
        - Entrypoint (main.py): """${mainPyFile.substring(0, 600)}..."""
        - Conversation History (last 4 entries): 
          ${conversationHistory.slice(-4).map(l => `${l.type === 'input' ? 'User' : 'Agent'}: ${l.content}`).join('\n')}
        
        COMMAND TO EXECUTE: "${command}"

        INSTRUCTIONS:
        1.  Analyze the command and generate the most likely stdout.
        2.  If the command is a standard shell command:
            - "help": Show a list of useful commands (ls, cat, run, clear, exit).
            - "ls": List all generated filenames.
            - "cat [filename]": Display the content of that file or an error if it doesn't exist.
            - "clear": Return the special string 'CLEAR_TERMINAL'.
            - "exit": Give a polite sign-off message from the agent.
        3.  If the command is "run" or "run [args...]": Simulate the output of running the 'main.py' script. This usually involves the agent introducing itself and stating its purpose.
        4.  If the command is anything else: Treat it as a message to the already-running agent. Generate a plausible, in-character response based on the agent's personality, purpose (from its code), and the conversation history. The agent should try to use its implemented features if the command implies it (e.g., if asked 'what is the capital of France' and it has Web Search, it should provide the answer).
        5.  **Adhere strictly to the persona of a terminal output.** No extra conversation or explanation.

        STDOUT:
    `;

    try {
        const response = await ai.models.generateContent({
            model: 'gemini-2.5-flash',
            contents: prompt,
            config: {
                temperature: 0.3,
            }
        });
        let output = response.text.trim();
        
        // Handle special case for clear command
        if (command.trim().toLowerCase() === 'clear') {
            return 'CLEAR_TERMINAL';
        }
        
        return output;

    } catch (error) {
        console.error("Error simulating cloud execution:", error);
        return "System Error: Could not execute command in the simulated environment.";
    }
}