# AI-EcoSystem Agent Architectuur

## 1. Overzicht
Dit document beschrijft de structuur, rollen en interactieprotocollen van de gespecialiseerde agents binnen het AI-EcoSystem. Het systeem is ontworpen om autonoom taken uit te voeren door gebruik te maken van domein-experts onder leiding van een centrale orchestrator.

## 2. Agent Registry
De agents worden technisch gedefinieerd in `prompts/specialized-agents/` (Markdown) en geregistreerd in `prompts/specialized-agents/agent_config.py` (Python Dictionary).

| Agent Naam | Bestandsnaam | Rol |
|------------|--------------|-----|
| **Prime Orchestrator** | `role.prime_orchestrator.md` | Projectleider & Strategie |
| **Nexus Architect** | `role.nexus_architect.md` | Lead Developer (Cloud/API/Full-stack) |
| **System Core** | `role.system_core.md` | DevOps (Termux/Android Focus) |
| **Quantum Trader** | `role.quantum_trader.md` | Crypto/Solana Specialist |
| **Content Synapse** | `role.content_synapse.md` | Content Creator & Researcher |

## 3. Orkestratie & Communicatie
Het systeem hanteert een **Hiërarchisch Model**:

1.  **User** geeft een opdracht aan de **Prime Orchestrator**.
2.  **Prime Orchestrator** analyseert de taak en bepaalt de benodigde expertise.
3.  **Prime Orchestrator** instrueert de gebruiker (of het systeem via CLI-hooks) om de specialist te activeren.
4.  **Specialist (Sub-agent)** voert de taak uit binnen zijn domein.
5.  **Specialist** rapporteert terug (via bestanden of logs).
6.  **Prime Orchestrator** verifieert en koppelt terug aan de gebruiker.

### Communicatie Protocol
Agents communiceren primair via:
- **Gedeelde Bestanden:** `write_todos` (Taaklijst), bestanden in `work_dir/`.
- **Context:** Het geheugen van de sessie (indien doorgegeven).
- **Instructies:** Expliciete taakomschrijvingen in natuurlijke taal.

## 4. Test Scenario's

### Scenario A: Nieuwe Feature Implementatie
1.  **Start:** User vraagt "Voeg een login pagina toe aan de dashboard".
2.  **Flow:**
    - Prime: Analyseert verzoek -> Maakt Todo -> Delegeert aan Nexus.
    - Nexus: Ontwerpt API -> Schrijft React component -> Update docs.
    - System: (Optioneel) Herstart server.
3.  **Success:** Login pagina is bereikbaar en functioneel.

### Scenario B: Trading Bot Update
1.  **Start:** User vraagt "Verhoog risk tolerance voor Solana bot".
2.  **Flow:**
    - Prime: Delegeert aan Quantum.
    - Quantum: Leest config -> Past JSON aan -> Start dry-run.
3.  **Success:** Bot draait met nieuwe parameters zonder errors.

## 5. Onderhoud
Om een nieuwe agent toe te voegen:
1.  Maak `role.nieuwe_agent.md` in `prompts/specialized-agents/`.
2.  Voeg entry toe aan `AGENT_ROLES` in `agent_config.py`.
3.  Voeg beschrijving toe aan `ROLE_DESCRIPTIONS` in `agent_config.py`.

## 6. Succes Metrieken
- **Autonomous Resolution:** % taken opgelost zonder gebruikersinterventie.
- **System Stability:** Uptime van de Termux omgeving.
- **User Satisfaction:** Kwaliteit van de output (code/content/trade).
