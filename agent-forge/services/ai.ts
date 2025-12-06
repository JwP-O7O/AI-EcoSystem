import { GoogleGenAI } from "@google/genai";

if (!import.meta.env.VITE_API_KEY) {
    // This check is a safeguard. The environment should have the API key.
    console.error("API_KEY environment variable not set.");
    throw new Error("API_KEY environment variable not set. Please configure your API key.");
}

export const ai = new GoogleGenAI({ apiKey: import.meta.env.VITE_API_KEY });