# SESSION CHECKPOINT - AI-ECOSYSTEM
**Datum:** 5 December 2025
**Laatste Rol:** Prime Orchestrator

## 🛑 Huidige Status: PAUSED (Error Debugging)

### 1. Actieve Processen
*   **Solana Scalping Bot:**
    *   Status: ✅ Draait (Backtest Mode)
    *   Port: `3000`
    *   PID: (Check met `pgrep -f scalpingbot`)
    *   Log: `solana-bot/bot_output.log`
*   **Agent-Forge (Frontend):**
    *   Status: ❌ Crashed / Build Error
    *   Port: `3001` (Beoogd)
    *   Log: `agent-forge/agent_forge_output_v3.log`

### 2. Het Probleem (De "Cliffhanger")
We probeerden Agent-Forge te starten met Vite. De browser toonde een wit scherm of de build faalde met:
`Uncaught ReferenceError: process is not defined` of `API_KEY environment variable not set`.

**Oorzaak:** De code in `agent-forge/services/ai.ts` (waarschijnlijk) gebruikt `process.env.API_KEY`. Vite stelt `process` niet beschikbaar in de browser.
**Oplossing voor volgende keer:**
1.  Open `agent-forge/vite.config.ts` en voeg `define: { 'process.env': {} }` toe.
2.  OF wijzig de code naar `import.meta.env.VITE_API_KEY`.

### 3. Bestanden Locaties
*   **Frontend:** `/data/data/com.termux/files/home/AI-EcoSystem/agent-forge/`
*   **Backend:** `/data/data/com.termux/files/home/AI-EcoSystem/solana-bot/`
*   **Google Drive Tool:** `tools/gdrive.py`

### 4. Hoe te hervatten?
Start de volgende sessie met:
*"Ik ben terug. Lees SESSION_CHECKPOINT.md, neem de rol van Prime Orchestrator aan en fix de process.env error in Agent-Forge."*
