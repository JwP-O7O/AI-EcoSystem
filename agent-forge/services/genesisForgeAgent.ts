import { Type } from "@google/genai";
import { ai } from './ai';
import { PricingTier, CustomBuild, GeneratedFile, BuildLogLine } from '../types';

// Helper to get consistent details from any order type
function getOrderDetails(order: PricingTier | CustomBuild): { name: string, features: string[], personality?: string, botType?: string, tradingTactic?: string } {
    if ('botType' in order) { // CustomBuild
        return {
            name: order.name,
            botType: order.botType,
            features: order.features,
            personality: order.personality,
            tradingTactic: order.tradingTactic,
        };
    } else { // PricingTier
        const defaultPersonalities: { [key: string]: string } = {
            'scout_agent': 'Behulpzaam',
            'hunter_agent': 'Proactief',
            'apex_agent': 'Strategisch',
        };
        return {
            name: order.name,
            features: order.features,
            botType: "Gespreks-AI", // Default for pre-made tiers
            personality: defaultPersonalities[order.id] || 'Professioneel',
        };
    }
}

/**
 * The main function of the Genesis Forge Agent.
 * It orchestrates the entire process of building an agent, from planning to code generation.
 */
export async function generateProject(
    order: PricingTier | CustomBuild,
    onProgress: (log: BuildLogLine) => void
): Promise<GeneratedFile[]> {
    
    onProgress({ level: 'INFO', message: "Order received. Initializing Forge environment..." });
    await new Promise(res => setTimeout(res, 500));

    const details = getOrderDetails(order);

    onProgress({ level: 'INFO', message: `Analyzing blueprint for a ${details.botType}...` });
    await new Promise(res => setTimeout(res, 500));

    const prompt = `
        You are the "AgentForge," a master code-generation AI. Your task is to generate a complete, executable Python project for a client based on their order.
        The output MUST be a JSON array of objects, where each object has a "filename" and a "content" key.
        The project must be well-structured, documented, and ready to run after installing dependencies from a 'requirements.txt' file.

        Customer's Order:
        - Name: ${details.name}
        - Bot Type: ${details.botType}
        ${details.tradingTactic ? `- Trading Tactic: ${details.tradingTactic}` : ''}
        - Additional Features: ${details.features.join(', ') || 'None'}
        ${details.personality ? `- Personality: ${details.personality}` : ''}

        Generation Instructions:
        1.  **Project Structure**: Generate all of the following files: 'requirements.txt', 'config.ini', 'agent.py', 'main.py', and 'README.md'.
        2.  **requirements.txt**: ALWAYS include 'python-dotenv'.
            - If Bot Type is 'Trading Bot', add 'ccxt', 'pandas', 'pandas-ta'.
            - If Bot Type is 'Web Scraper Bot' OR feature 'Real-time Web Search' is included, add 'requests', 'beautifulsoup4'.
            - If Bot Type is 'Data Analyse Bot', add 'pandas', 'numpy', 'matplotlib'.
        3.  **config.ini**: Create a configuration file. For sensitive data like API keys, use placeholders (e.g., 'YOUR_API_KEY_HERE'). For a Trading Bot, include exchange details. For a Web Scraper, include a default URL.
        4.  **agent.py**: This is the core logic. Create a class-based agent.
            - The agent's personality ('${details.personality}') must be reflected in code comments and any user-facing print statements.
            - Implement the core logic based on the 'Bot Type'. This should be the main purpose of the agent.
            - Implement all 'Additional Features' as separate, well-documented methods within the agent class. For example, a 'search_web(query)' method or a 'calculate(expression)' method.
        5.  **main.py**: The entry point. It should load the config, instantiate the agent, and have a simple loop that takes user input and calls the agent's primary method. It should demonstrate how to use the agent.
        6.  **README.md**: Generate a clear README with the project title, a brief description, and instructions for setup (installing requirements, setting up config) and usage.
        7.  **Code Quality**: All Python code must be clean, follow PEP 8 standards, and include helpful comments.
    `;
    
    const responseSchema = {
        type: Type.ARRAY,
        items: {
          type: Type.OBJECT,
          properties: {
            filename: { type: Type.STRING },
            content: { type: Type.STRING },
          },
          required: ["filename", "content"]
        },
    };

    try {
        onProgress({ level: 'GEN', message: "Engaging model to generate project files..." });
        
        const response = await ai.models.generateContent({
            model: 'gemini-2.5-flash',
            contents: prompt,
            config: {
                temperature: 0.4,
                responseMimeType: "application/json",
                responseSchema,
            }
        });

        onProgress({ level: 'VALIDATE', message: "Parsing generated code..." });
        await new Promise(res => setTimeout(res, 500));
        
        const jsonText = response.text.trim();
        const generatedFiles = JSON.parse(jsonText) as GeneratedFile[];

        if (!Array.isArray(generatedFiles) || generatedFiles.length < 5) {
             throw new Error("The Forge returned an incomplete or invalid project structure.");
        }

        onProgress({ level: 'VALIDATE', message: "Validating critical files (main.py, agent.py)..." });
         await new Promise(res => setTimeout(res, 500));
        if (!generatedFiles.some(f => f.filename === 'main.py') || !generatedFiles.some(f => f.filename === 'agent.py')) {
            throw new Error("Validation failed: Critical files (main.py, agent.py) are missing.");
        }
        
        return generatedFiles;

    } catch (error) {
        console.error("Error during project generation:", error);
        let errorMessage = "The Forge failed to generate the agent's code.";
        if (error instanceof Error) {
            if (error.message.includes('rate limit') || error.message.includes('RESOURCE_EXHAUSTED')) {
                errorMessage = "The Forge is currently at maximum capacity. Please try again in a few moments.";
            } else if (error instanceof SyntaxError) {
                errorMessage = "The Forge returned invalid data. Could not parse the project files.";
            } else {
                errorMessage = error.message;
            }
        }
        throw new Error(errorMessage);
    }
}