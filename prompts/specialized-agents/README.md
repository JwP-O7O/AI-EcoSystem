# Specialized Agents - AI-EcoSystem

Dit is een set van gespecialiseerde agent prompts voor het Agent Zero framework.

## Beschikbare Agent Rollen

### 1. Master Orchestrator Agent
**File**: `role.master_orchestrator.md`
**Doel**: Hoofdcoördinator die taken analyseert, plant en distribueert
**Gebruik**: Als primaire agent (Agent 0) voor gebruikersinteractie

### 2. Code Execution Specialist
**File**: `role.code_specialist.md`
**Doel**: Expert in Python, NodeJS en Terminal commando's
**Gebruik**: Voor alle code-gerelateerde taken

### 3. Knowledge Research Specialist
**File**: `role.knowledge_researcher.md`
**Doel**: Expert in online research en information retrieval
**Gebruik**: Voor research, fact-checking, documentatie zoeken

### 4. Memory Management Specialist
**File**: `role.memory_manager.md`
**Doel**: Expert in long-term geheugen beheer
**Gebruik**: Voor opslaan, zoeken en beheren van memories

### 5. Web Content Extraction Specialist
**File**: `role.web_scraper.md`
**Doel**: Expert in web scraping en content extractie
**Gebruik**: Voor het extraheren van data van webpagina's

### 6. Task Delegation Orchestrator
**File**: `role.task_orchestrator.md`
**Doel**: Expert in subtask delegatie en coördinatie
**Gebruik**: Voor complexe multi-agent workflows

### 7. Solution Architecture Specialist
**File**: `role.solution_architect.md`
**Doel**: Expert in complexe probleem-analyse en strategieën
**Gebruik**: Voor architectuurontwerp en strategische planning

## Hoe Te Gebruiken

### Optie 1: Via call_subordinate met rol instructie

In je hoofdagent, gebruik:

```json
{
    "thoughts": ["I need code execution expertise..."],
    "tool_name": "call_subordinate",
    "tool_args": {
        "message": "You are a Code Execution Specialist. Your task is to write Python code that reads a CSV file and outputs the first 10 rows...",
        "reset": "true"
    }
}
```

### Optie 2: Via Configuratie (zie agent_config.py)

Configureer welke rol-prompt geladen moet worden op basis van de agent context.

## Prompt Structuur

Elke rol-prompt bevat:
- **Role definitie**: Wie ben je en wat is je expertise
- **Core skills/responsibilities**: Wat kun je doen
- **Rules**: Operationele regels en best practices
- **Patterns/Examples**: Concrete voorbeelden van tool usage
- **Mission**: Je primaire doel

## Integratie met Agent Zero

Deze prompts zijn compatibel met het standaard Agent Zero framework en kunnen:
- Gebruikt worden in combinatie met alle standaard tools
- Dynamisch geladen worden per agent instantie
- Gecombineerd worden met de default prompts
- Aangepast worden naar specifieke use cases

## Customization

Je kunt deze prompts aanpassen door:
1. De rol definitie te wijzigen
2. Regels toe te voegen of aan te passen
3. Voorbeelden aan te passen aan je use case
4. Extra tools of constraints toe te voegen

## License

Deze prompts zijn onderdeel van het AI-EcoSystem project en volgen dezelfde licentie als Agent Zero.
