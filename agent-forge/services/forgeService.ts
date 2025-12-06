import { GoogleGenAI, Type } from "@google/genai";
import { PricingTier, CustomBuild, GeneratedFile } from '../types';

const ai = new GoogleGenAI({ apiKey: import.meta.env.VITE_API_KEY });

function getOrderDetails(order: PricingTier | CustomBuild): { name: string, features: string[], personality?: string, botType?: string, tradingTactic?: string } {
    if ('botType' in order) { // CustomBuild
        return {
            name: `Aangepaste ${order.botType}`,
            botType: order.botType,
            features: order.features,
            personality: order.personality,
            tradingTactic: order.tradingTactic,
        };
    } else { // PricingTier
        return {
            name: order.name,
            features: order.features,
            botType: "Gespreks-AI" // Standaard voor kant-en-klare pakketten
        };
    }
}

export async function buildAgent(order: PricingTier | CustomBuild): Promise<GeneratedFile[]> {
    if (!import.meta.env.VITE_API_KEY) {
        throw new Error("API Key niet geconfigureerd. Neem contact op met support.");
    }

    const details = getOrderDetails(order);

    const prompt = `
        U bent de "AI Forge", een meesterlijke code-generatie agent. Uw taak is om een compleet, uitvoerbaar Python-project voor een klant te genereren op basis van hun bestelling.
        De output MOET een JSON-array van objecten zijn, waarbij elk object een "filename" en een "content" sleutel heeft.
        Het project moet goed gestructureerd, gedocumenteerd en klaar zijn om te draaien na het installeren van de afhankelijkheden uit een 'requirements.txt' bestand.

        Bestelling van de klant:
        - Naam: ${details.name}
        - Type Bot: ${details.botType}
        ${details.tradingTactic ? `- Handelsstrategie: ${details.tradingTactic}` : ''}
        - Extra Functies: ${details.features.join(', ') || 'Geen'}
        ${details.personality ? `- Persoonlijkheid: ${details.personality}` : ''}

        Instructies:
        1.  **requirements.txt**: Creëer dit bestand. Het MOET de basisbibliotheken bevatten.
            - Als het een 'Trading Bot' of 'Scalping Bot' is, voeg 'ccxt', 'pandas' en 'pandas-ta' toe.
            - Als het een 'Auto-Clicker Bot' is, voeg 'pynput' toe.
            - Als het een 'Web Scraper Bot' is, of als "Web Search" is geselecteerd, voeg 'requests' en 'beautifulsoup4' toe.
        2.  **config.ini**: Maak een configuratiebestand voor instellingen. Gebruik placeholders zoals UW_API_SLEUTEL_HIER. Voor trading bots, voeg exchange en symbol parameters toe.
        3.  **agent.py**: De kernlogica.
            - **Voor Trading/Scalping Bot**: Maak een class-based agent die 'ccxt' gebruikt om verbinding te maken. Implementeer de gekozen strategie (${details.tradingTactic || 'geen'}) met 'pandas-ta' voor indicatorberekeningen. De 'run' methode moet een loop bevatten die marktdata ophaalt, analyseert en gesimuleerde koop/verkoop signalen print.
            - **Voor Auto-Clicker Bot**: Maak een agent die 'pynput' gebruikt. Het moet een 'start_clicking(interval, duration)' methode hebben die op een ingesteld interval klikt voor een bepaalde duur.
            - **Voor Web Scraper Bot**: Maak een agent met een 'scrape_website(url)' methode die 'requests' en 'BeautifulSoup' gebruikt om alle links van een pagina te extraheren en te printen.
            - **Voor Gespreks-AI**: Maak een standaard chatbot-klasse die een 'respond(message)' methode heeft.
        4.  **main.py**: Een eenvoudig script om de agent te instantiëren en een van zijn kernfuncties aan te roepen.
        5.  **README.md**: Genereer een duidelijke README met projecttitel, beschrijving en setup/gebruiksinstructies.
        6.  **Persoonlijkheid**: De gekozen persoonlijkheid moet terugkomen in codecommentaar en alle gebruikersgerichte print-statements.
        7.  **Extra Functies**: Implementeer de extra functies als aparte methodes ('tools') in de agent-klasse, indien van toepassing op het bottype.
    `;
    
    const responseSchema = {
        type: Type.ARRAY,
        items: {
          type: Type.OBJECT,
          properties: {
            filename: {
              type: Type.STRING,
            },
            content: {
              type: Type.STRING,
            },
          },
          required: ["filename", "content"]
        },
    };

    try {
        const response = await ai.models.generateContent({
            model: 'gemini-2.5-flash',
            contents: prompt,
            config: {
                temperature: 0.5,
                responseMimeType: "application/json",
                responseSchema,
            }
        });

        const jsonResponse = JSON.parse(response.text);
        return jsonResponse as GeneratedFile[];

    } catch (error) {
        console.error("Gemini API-aanroep mislukt voor forgeService:", error);
        throw new Error("De AI Forge is er niet in geslaagd de code van de agent te genereren. De respons van het model was mogelijk onjuist geformatteerd.");
    }
}