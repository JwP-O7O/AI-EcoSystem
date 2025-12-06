import { GeneratedFile, PricingTier, CustomBuild } from '../types';
import { getAgentResponse } from './geminiService';

/**
 * Simuleert de backend-executieomgeving.
 * Ontvangt de code van de agent en een commando, en retourneert een realistische output.
 */
export async function executeCommand(
    command: string,
    files: GeneratedFile[],
    order: PricingTier | (CustomBuild & { name: string }),
    conversationHistory: string[]
): Promise<string> {
    const [cmd, ...args] = command.trim().toLowerCase().split(' ');

    // Prioritaire commando's die de terminal besturen
    switch (cmd) {
        case 'help':
            return `Beschikbare commando's:
  help      - Toon dit helpbericht
  ls        - Toon projectbestanden
  cat [bestand] - Toon de inhoud van een bestand
  run       - Activeer de agent en start een gesprek
  exit      - Verlaat de agent-modus
  clear     - Maak de terminal leeg`;
        
        case 'ls':
            return files.map(f => f.filename).join('   ');
            
        case 'cat':
            const filename = args[0];
            if (!filename) return "Fout: geef een bestandsnaam op. Gebruik: cat [bestandsnaam]";
            const file = files.find(f => f.filename.toLowerCase() === filename);
            if (file) {
                return `--- Inhoud van ${file.filename} ---\n${file.content}`;
            } else {
                return `Fout: bestand '${filename}' niet gevonden.`;
            }

        case 'clear':
            return 'CLEAR_TERMINAL'; // Speciaal signaal voor de terminal
    }

    // Als geen van bovenstaande, geef het door aan de agent
    // We gebruiken Gemini om de reactie van de agent te simuleren
    try {
        const response = await getAgentResponse(order, files, conversationHistory, command);
        return response;
    } catch (error) {
        console.error("Fout bij het simuleren van agent-respons:", error);
        return "Er is een fout opgetreden in de agent.";
    }
}