# Specialized Agents - Gebruikershandleiding

## 📚 Inhoudsopgave

1. [Introductie](#introductie)
2. [Beschikbare Agent Rollen](#beschikbare-agent-rollen)
3. [Installatie & Setup](#installatie--setup)
4. [Gebruik](#gebruik)
5. [Voorbeelden](#voorbeelden)
6. [Best Practices](#best-practices)
7. [Troubleshooting](#troubleshooting)

---

## Introductie

De **Specialized Agents** zijn een set van rol-gebaseerde system prompts voor het Agent Zero framework. Elke agent heeft een specifieke expertise en is geoptimaliseerd voor bepaalde taken.

### Waarom Specialized Agents?

- **🎯 Gerichtere responses**: Agents met specifieke rollen geven betere, meer gerichte antwoorden
- **⚡ Efficiënter**: Minder context switching en duidelijkere tool usage
- **🔧 Modulair**: Combineer agents voor complexe workflows
- **📈 Schaalbaarheid**: Breid eenvoudig uit met nieuwe rollen

---

## Beschikbare Agent Rollen

### 1. 🎭 Master Orchestrator Agent
**Expertise**: Hoofdcoördinatie en task management

**Gebruik voor**:
- Complex multi-step taken
- High-level planning en strategie
- Coördinatie van meerdere sub-agents
- Gebruikersinteractie

**Voorbeeld taak**: "Plan en implementeer een complete web scraper met data opslag en error handling"

---

### 2. 💻 Code Execution Specialist
**Expertise**: Python, NodeJS, Terminal commando's

**Gebruik voor**:
- Code schrijven en uitvoeren
- Package installatie
- File operations
- Script development
- Error debugging

**Voorbeeld taak**: "Schrijf Python code om JSON data te parsen en op te slaan in SQLite database"

---

### 3. 🔍 Knowledge Research Specialist
**Expertise**: Online search en information retrieval

**Gebruik voor**:
- Research naar libraries en tools
- Documentatie zoeken
- Best practices vinden
- Error solutions opzoeken
- Fact checking

**Voorbeeld taak**: "Zoek de beste Python library voor PDF parsing met OCR support"

---

### 4. 🧠 Memory Management Specialist
**Expertise**: Long-term geheugen beheer

**Gebruik voor**:
- Solutions opslaan voor hergebruik
- Memories zoeken en filteren
- Knowledge base onderhoud
- Oude memories opschonen

**Voorbeeld taak**: "Sla deze database query pattern op voor later gebruik"

---

### 5. 🌐 Web Content Extraction Specialist
**Expertise**: Web scraping en data extractie

**Gebruik voor**:
- Webpage content scrapen
- API documentation extractie
- HTML parsing
- Data verzameling van websites

**Voorbeeld taak**: "Extraheer alle productprijzen van deze e-commerce website"

---

### 6. 🎯 Task Delegation Orchestrator
**Expertise**: Subtask delegatie en coördinatie

**Gebruik voor**:
- Complex multi-agent workflows
- Task decomposition
- Subordinate management
- Result consolidatie

**Voorbeeld taak**: "Coördineer de development van een REST API met database, tests en documentatie"

---

### 7. 🏗️ Solution Architecture Specialist
**Expertise**: Strategische probleem-oplossing

**Gebruik voor**:
- Complexe architectuur design
- Solution planning
- Dependency mapping
- Risk assessment
- Performance optimization

**Voorbeeld taak**: "Ontwerp de architectuur voor een real-time data processing pipeline"

---

## Installatie & Setup

### Stap 1: Verifieer Installatie

De specialized agents zijn al geïnstalleerd in:
```
prompts/specialized-agents/
```

Verifieer met:
```bash
ls -la prompts/specialized-agents/
```

Je zou moeten zien:
- `role.master_orchestrator.md`
- `role.code_specialist.md`
- `role.knowledge_researcher.md`
- `role.memory_manager.md`
- `role.web_scraper.md`
- `role.task_orchestrator.md`
- `role.solution_architect.md`
- `agent_config.py`
- `communication.md`
- `README.md`

### Stap 2: Test Configuratie

Run het configuratie script:
```bash
cd prompts/specialized-agents
python agent_config.py
```

Dit toont alle beschikbare rollen en test de laad-functionaliteit.

---

## Gebruik

### Methode 1: Via call_subordinate Tool (Aanbevolen)

Gebruik de `call_subordinate` tool met een duidelijke rol-instructie:

```json
{
    "thoughts": [
        "Deze taak vereist code expertise...",
        "Ik delegeer naar een Code Execution Specialist..."
    ],
    "tool_name": "call_subordinate",
    "tool_args": {
        "message": "You are a Code Execution Specialist. Your task is to write Python code that:\n1. Reads data.csv\n2. Filters rows where value > 100\n3. Outputs results to filtered.csv\n\nUse pandas library and include error handling.",
        "reset": "true"
    }
}
```

**Key points**:
- Begin message met: "You are a [ROL]..."
- Geef specifieke, gedetailleerde instructies
- Vermeld expected output format
- Gebruik `"reset": "true"` voor nieuwe taken

### Methode 2: Via Auto-detectie

Gebruik het `agent_config.py` script om automatisch de beste rol te kiezen:

```python
from prompts.specialized_agents.agent_config import get_role_for_task, ROLE_DESCRIPTIONS

task = "Write Python code to scrape a website"
role = get_role_for_task(task)
print(f"Suggested role: {role} - {ROLE_DESCRIPTIONS[role]}")
```

### Methode 3: Direct Prompt Laden (Advanced)

Voor directe integratie in je Agent Zero setup:

```python
from prompts.specialized_agents.agent_config import load_role_prompt

# Laad specifieke rol prompt
code_specialist_prompt = load_role_prompt("coder")

# Gebruik in je agent configuratie
agent.system_prompt = code_specialist_prompt + shared_tools_prompt
```

---

## Voorbeelden

### Voorbeeld 1: Code Development Workflow

**Scenario**: Je wilt een Python script ontwikkelen

```json
{
    "thoughts": ["I need to delegate to Code Execution Specialist..."],
    "tool_name": "call_subordinate",
    "tool_args": {
        "message": "You are a Code Execution Specialist. Write Python code that:\n1. Connects to a PostgreSQL database\n2. Executes SELECT query to get all users\n3. Exports results to JSON file\n4. Includes proper error handling\n\nUse psycopg2 library. Show all output with print statements.",
        "reset": "true"
    }
}
```

### Voorbeeld 2: Research Task

**Scenario**: Je zoekt de beste tool voor een taak

```json
{
    "thoughts": ["I need research expertise..."],
    "tool_name": "call_subordinate",
    "tool_args": {
        "message": "You are a Knowledge Research Specialist. Research:\n\nFind the best open-source Python library for:\n- Real-time video processing\n- Face detection\n- Compatible with OpenCV\n- Good documentation\n- Active maintenance\n\nProvide: library name, key features, installation command, and basic usage example.",
        "reset": "true"
    }
}
```

### Voorbeeld 3: Web Scraping Project

**Scenario**: Data extractie van een website

```json
{
    "thoughts": ["I need web scraping expertise..."],
    "tool_name": "call_subordinate",
    "tool_args": {
        "message": "You are a Web Content Extraction Specialist. Extract from https://example.com/products:\n\n1. All product names\n2. Prices\n3. Availability status\n4. Product URLs\n\nReturn structured data (JSON format). Handle pagination if present.",
        "reset": "true"
    }
}
```

### Voorbeeld 4: Multi-Agent Complex Workflow

**Scenario**: Complete solution met meerdere agents

**Step 1**: Architect designs de oplossing
```json
{
    "thoughts": ["Complex task, need architecture design..."],
    "tool_name": "call_subordinate",
    "tool_args": {
        "message": "You are a Solution Architecture Specialist. Design architecture for:\n\nTask: Build a web scraper that:\n- Scrapes data every hour\n- Stores in database\n- Sends email alerts on errors\n- Has a simple web dashboard\n\nProvide: component breakdown, tech stack suggestions, execution steps.",
        "reset": "true"
    }
}
```

**Step 2**: Task Orchestrator coördineert de implementatie
```json
{
    "thoughts": ["Architecture ready, now coordinate implementation..."],
    "tool_name": "call_subordinate",
    "tool_args": {
        "message": "You are a Task Delegation Orchestrator. Implement the architecture:\n\n[paste architecture from step 1]\n\nBreak down into subtasks and delegate to appropriate specialists:\n- Code Specialist for scraper code\n- Code Specialist for database setup\n- Web Scraper for testing extraction\n- Memory Manager to save the solution\n\nCoordinate and consolidate results.",
        "reset": "true"
    }
}
```

---

## Best Practices

### ✅ DO's

1. **Wees specifiek in rol-toewijzing**
   ```
   ✅ "You are a Code Execution Specialist..."
   ❌ "You are a helpful assistant..."
   ```

2. **Geef gedetailleerde context**
   - Vermeldt higher-level doel
   - Specifieke subtask beschrijving
   - Expected output format
   - Success criteria

3. **Gebruik de juiste rol voor de taak**
   - Code schrijven? → Code Specialist
   - Research? → Knowledge Researcher
   - Complexe planning? → Solution Architect

4. **Combineer agents strategisch**
   - Start met Architect voor design
   - Gebruik Orchestrator voor coördinatie
   - Delegeer specifieke taken aan specialists

5. **Save waardevolle solutions**
   - Gebruik Memory Manager om solutions op te slaan
   - Faciliteer hergebruik en leren

### ❌ DON'Ts

1. **Vermijd vage instructies**
   ```
   ❌ "Do something with this data"
   ✅ "Parse this JSON, extract 'users' array, filter active users, output to CSV"
   ```

2. **Delegeer niet je hele taak**
   ```
   ❌ "Solve everything"
   ✅ "Handle step 2: database connection" (als onderdeel van groter plan)
   ```

3. **Mix geen rollen in één instructie**
   ```
   ❌ "Research AND implement AND test..."
   ✅ Aparte delegaties voor research, implementation, testing
   ```

4. **Negeer geen errors**
   - Analyseer errors met Knowledge Researcher
   - Fix met Code Specialist
   - Iterate tot succes

---

## Troubleshooting

### Probleem: Agent begrijpt zijn rol niet

**Oplossing**: Maak rol explicieter in je message:
```json
{
    "message": "IMPORTANT: You are a Code Execution Specialist. Your ONLY job is to write and execute code. Do not research, do not delegate. Focus on coding.\n\nYour task: [...]"
}
```

### Probleem: Infinite delegation loops

**Oplossing**:
- Check hierarchical level (agent_name bevat nummer)
- Gebruik Solution Architect voor planning, dan directe execution
- Vermijd "solve this completely" statements

### Probleem: Agent gebruikt verkeerde tools

**Oplossing**:
- Specificeer welke tools de agent moet gebruiken
- Geef voorbeelden van correct tool usage
- Verwijs naar de rol-prompt voorbeelden

### Probleem: Inconsistente resultaten

**Oplossing**:
- Gebruik `reset: true` voor nieuwe taken
- Gebruik `reset: false` alleen voor iteratie op dezelfde taak
- Clear context tussen verschillende taken

---

## Advanced: Custom Rollen Maken

Je kan eenvoudig nieuwe rollen toevoegen:

### Stap 1: Creëer Role Prompt File

Maak `prompts/specialized-agents/role.your_role.md`:

```markdown
## Your role: Your Custom Specialist

- Your name is {{agent_name}}, current time is {{date_time}}
- You are a [Your Role], specialized in [expertise]
- [Role description]

## Core Skills
- [Skill 1]
- [Skill 2]

## Rules
1. [Rule 1]
2. [Rule 2]

## Example Pattern
```json
{
    "thoughts": ["..."],
    "tool_name": "...",
    "tool_args": { }
}
```

## Your Mission
[Primary goal]
```

### Stap 2: Voeg toe aan agent_config.py

```python
AGENT_ROLES = {
    # ... existing roles ...
    "your_role": "role.your_role.md",
}

ROLE_DESCRIPTIONS = {
    # ... existing descriptions ...
    "your_role": "Your Custom Specialist - [description]",
}
```

---

## Support & Feedback

Voor vragen, bugs of suggesties:
- Check de Agent Zero documentation
- Bekijk voorbeelden in `prompts/specialized-agents/README.md`
- Test met `agent_config.py`

---

**Versie**: 1.0
**Laatste update**: {{ date_time }}
**Compatibel met**: Agent Zero v0.6+
