# Quick Start - Specialized Agents

## 🚀 Direct aan de slag in 3 stappen

### Stap 1: Test de configuratie

```bash
cd /data/data/com.termux/files/home/AI-EcoSystem/prompts/specialized-agents
python agent_config.py
```

### Stap 2: Gebruik een specialist in Agent Zero

Start je Agent Zero (CLI of UI) en gebruik dit voorbeeld:

**Voorbeeld 1: Code schrijven**
```
User: I need to write Python code to read a CSV file and show the first 10 rows

Agent 0: [calls subordinate]
{
    "thoughts": [
        "This task requires code execution expertise",
        "I will delegate to a Code Execution Specialist"
    ],
    "tool_name": "call_subordinate",
    "tool_args": {
        "message": "You are a Code Execution Specialist. Write Python code that:\n1. Reads 'data.csv' file\n2. Prints the first 10 rows\n3. Uses pandas library\n4. Includes error handling for file not found\n\nExecute the code and show output.",
        "reset": "true"
    }
}
```

**Voorbeeld 2: Research**
```
User: Find the best Python library for making HTTP requests with retry logic

Agent 0: [calls subordinate]
{
    "thoughts": [
        "This is a research task",
        "Knowledge Research Specialist is most suitable"
    ],
    "tool_name": "call_subordinate",
    "tool_args": {
        "message": "You are a Knowledge Research Specialist. Research:\n\nFind the best Python library for:\n- Making HTTP requests\n- Built-in retry logic\n- Timeout handling\n- Good documentation\n- Widely used\n\nProvide: library name, why it's good, installation command, and basic usage example.",
        "reset": "true"
    }
}
```

### Stap 3: Combineer specialists (Advanced)

Voor complexe taken, gebruik meerdere specialists:

```
User: Build a web scraper that saves data to database

Agent 0: [delegeert aan Solution Architect]
→ Solution Architect: [ontwerpt architectuur]
  → delegeert aan Task Orchestrator
    → Task Orchestrator:
       - delegeert web scraping → Web Scraper Specialist
       - delegeert database code → Code Execution Specialist
       - delegeert solution opslaan → Memory Manager
    → consolideert resultaten
→ rapporteert aan gebruiker
```

## 📋 Cheat Sheet - Welke Specialist voor welke Taak?

| Taak Type | Gebruik Deze Specialist | Voorbeeld |
|-----------|-------------------------|-----------|
| Code schrijven/uitvoeren | Code Execution Specialist | "Write Python script to..." |
| Online zoeken | Knowledge Research Specialist | "Find best library for..." |
| Data opslaan/ophalen | Memory Manager | "Save this solution..." |
| Website scrapen | Web Scraper Specialist | "Extract data from URL..." |
| Taak opsplitsen | Task Orchestrator | "Coordinate building..." |
| Architectuur ontwerpen | Solution Architect | "Design system for..." |
| Alles coördineren | Master Orchestrator | "Plan and execute..." |

## 🎯 Best Practice Pattern

```json
{
    "thoughts": [
        "Task analysis: [wat moet er gebeuren]",
        "Best specialist: [welke rol past]",
        "Delegation strategy: [hoe ga ik het aanpakken]"
    ],
    "tool_name": "call_subordinate",
    "tool_args": {
        "message": "You are a [ROL NAAM]. [Context over higher goal]. Your specific task: [gedetailleerde instructies]. Expected output: [wat je terug wilt].",
        "reset": "true"
    }
}
```

## ✅ Checklist voor Succesvolle Delegatie

- [ ] Rol expliciet genoemd in message ("You are a...")
- [ ] Higher-level context gegeven (waarom is dit nodig?)
- [ ] Specifieke taak beschrijving (wat precies doen?)
- [ ] Expected output format (wat verwacht je terug?)
- [ ] Success criteria (wanneer is het goed?)
- [ ] Tools vermeld indien relevant (welke tools gebruiken?)
- [ ] Reset parameter correct ("true" voor nieuwe taak)

## 🔥 Top 5 Use Cases

### 1. **Data Processing Pipeline**
```
Architect ontwerpt → Orchestrator coördineert → Code Specialist implementeert → Memory Manager slaat op
```

### 2. **Research + Implementation**
```
Researcher zoekt beste aanpak → Code Specialist implementeert → Memory Manager documenteert
```

### 3. **Web Data Collection**
```
Web Scraper extraheert → Code Specialist verwerkt → Memory Manager archiveert
```

### 4. **Complex Problem Solving**
```
Solution Architect analyseert → Task Orchestrator splitst op → Specialists voeren uit → Orchestrator consolideert
```

### 5. **Learning from Solutions**
```
[Any Specialist] lost probleem op → Memory Manager slaat solution op → Future tasks: snel ophalen
```

## 🐛 Veelvoorkomende Fouten & Fixes

### Fout: Agent doet niets
**Fix**: Controleer of message begint met "You are a [ROLE]"

### Fout: Oneindige loops
**Fix**: Gebruik Architect voor planning, dan directe execution (niet opnieuw delegeren)

### Fout: Verkeerde specialist keuze
**Fix**: Gebruik auto-detection in agent_config.py

### Fout: Agent vergeet context
**Fix**: Gebruik reset: false voor follow-up, reset: true voor nieuwe taak

## 📚 Meer Leren?

Bekijk de volledige guide:
```bash
cat /data/data/com.termux/files/home/AI-EcoSystem/docs/SPECIALIZED_AGENTS_GUIDE.md
```

Of test de configuratie:
```bash
python agent_config.py
```

---

**Happy delegating! 🎉**
