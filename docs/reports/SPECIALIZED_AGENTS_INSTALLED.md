# Geïnstalleerde Specialized Agents

De volgende agents zijn succesvol aangemaakt en geconfigureerd in het systeem. Ze kunnen worden aangeroepen via de `Prime Orchestrator` of direct via hun rol-naam.

## 1. Core Project Agents

| Agent | Rol | Specialisme |
|-------|-----|-------------|
| **Prime Orchestrator** | `prime` | Projectleider, Strategie, Delegatie. |
| **Nexus Architect** | `nexus` | Backend, API's, Docker, Dashboard, Integratie. |
| **Quantum Trader** | `quantum` | Solana, DeFi, Trading Bot, Blockchain. |
| **System Core** | `core` | Android, Termux, OS Management, DevOps. |
| **Content Synapse** | `synapse` | Web Content, SEO, Research, Copywriting. |

## 2. Speciale AI-EcoSystem Agents

| Agent | Rol | Specialisme |
|-------|-----|-------------|
| **Innovator** | `innovator` | Genereren van revolutionaire ideeën & roadmaps. |
| **Synergy Agent** | `synergy` | Cross-project code hergebruik & dependency mapping. |
| **Optimizer** | `optimizer` | Code efficiency, prompt optimalisatie & kosten reductie. |

## Hoe te gebruiken?

### Optie 1: Via de Prime Orchestrator (Aanbevolen)
Geef een commando aan de hoofd-agent en hij zal automatisch de juiste specialist inschakelen.
*   *"Bedenk een plan om de trading bot sneller te maken."* -> Prime roept **Innovator** en **Quantum Trader**.
*   *"Check of we code van de bot kunnen gebruiken in het dashboard."* -> Prime roept **Synergy Agent**.

### Optie 2: Directe Selectie
Je kunt een sub-agent direct starten als je weet wat je nodig hebt:
*   *"Start een sessie als Nexus Architect en fix de API gateway."*

## Configuratie
De configuratie bevindt zich in: `prompts/specialized-agents/agent_config.py`.
De prompts staan in: `prompts/specialized-agents/*.md`.