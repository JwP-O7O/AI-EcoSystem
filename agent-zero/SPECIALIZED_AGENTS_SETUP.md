# 🎭 Specialized Agents - Complete Setup

## 🎯 OVERZICHT

Agent Zero heeft nu **7 gespecialiseerde agent rollen** die je kunt kiezen bij het starten!

Elke agent heeft unieke expertise en is geoptimaliseerd voor specifieke taken.

---

## 🚀 HOE TE STARTEN

### Optie 1: Interactive Selector (AANBEVOLEN) ⭐
```bash
cd /data/data/com.termux/files/home/AI-EcoSystem/agent-zero
./select-agent.sh
```

**Je krijgt een menu:**
```
╔══════════════════════════════════════════════════════════╗
║          🤖 Agent Zero - Agent Selector 🤖              ║
╚══════════════════════════════════════════════════════════╝

Kies je gespecialiseerde agent:

  1) 🎭 Master Orchestrator (Hoofdcoördinator)
  2) 💻 Code Specialist (Python/NodeJS/Terminal)
  3) 🔍 Research Specialist (Online research)
  4) 💾 Memory Manager (Geheugen beheer)
  5) 🌐 Web Scraper (Web extractie)
  6) 🎯 Task Orchestrator (Delegatie)
  7) 🏗️  Solution Architect (Strategisch)
  8) ⚡ Default Agent (Geen specialisatie)

Maak je keuze (1-8):
```

### Optie 2: Direct Met Environment Variable
```bash
# Start specifieke agent
export AGENT_ZERO_ROLE=code_specialist
./run-termux.sh

# Of in Ubuntu
export AGENT_ZERO_ROLE=research_specialist
./run-ubuntu.sh
```

### Optie 3: Default Agent (Zoals Altijd)
```bash
./run-termux.sh  # Of ./run-ubuntu.sh
```

---

## 🎭 BESCHIKBARE AGENTS

### 1. Master Orchestrator 🎭
**Rol:** Hoofdcoördinator
**Expertise:** Taakanalyse, planning, distributie
**Gebruik voor:** Complexe multi-step projecten, team coördinatie

**Specialiteiten:**
- Analyseert complexe taken
- Maakt uitvoeringsplannen
- Delegeert naar juiste specialisten
- Coördineert meerdere agents

---

### 2. Code Specialist 💻
**Rol:** Code Expert
**Expertise:** Python, NodeJS, Terminal commands
**Gebruik voor:** Programmeren, scripting, code debugging

**Specialiteiten:**
- Python development
- NodeJS/JavaScript
- Terminal automation
- Code optimization
- Debugging

---

### 3. Research Specialist 🔍
**Rol:** Knowledge Expert
**Expertise:** Online research, fact-checking
**Gebruik voor:** Information retrieval, documentatie, research

**Specialiteiten:**
- Web search expertise
- Fact verification
- Documentation lookup
- Comparative analysis
- Source evaluation

---

### 4. Memory Manager 💾
**Rol:** Memory Expert
**Expertise:** Long-term geheugen beheer
**Gebruik voor:** Opslaan, zoeken en beheren van memories

**Specialiteiten:**
- Memory storage optimization
- Semantic search
- Memory organization
- Context recall
- Knowledge base management

---

### 5. Web Scraper 🌐
**Rol:** Web Content Expert
**Expertise:** Web scraping, data extractie
**Gebruik voor:** Website data extraction, content parsing

**Specialiteiten:**
- HTML parsing
- CSS selector expertise
- JavaScript rendering
- Data structuring
- Rate limiting compliance

---

### 6. Task Orchestrator 🎯
**Rol:** Delegation Expert
**Expertise:** Subtask management, coordination
**Gebruik voor:** Multi-agent workflows, complex task breakdown

**Specialiteiten:**
- Task decomposition
- Dependency management
- Agent coordination
- Workflow optimization
- Progress tracking

---

### 7. Solution Architect 🏗️
**Rol:** Architecture Expert
**Expertise:** Strategic planning, design patterns
**Gebruik voor:** System design, architecture planning

**Specialiteiten:**
- Problem analysis
- Architecture design
- Strategy formulation
- Best practices
- Long-term planning

---

## 🔧 TECHNISCHE DETAILS

### Hoe Het Werkt

1. **Environment Variable:** Stel `AGENT_ZERO_ROLE` in
2. **Extension Loader:** `_02_load_specialized_role.py` laadt de rol
3. **Prompt Injection:** Role prompt wordt toegevoegd aan system messages
4. **Specialization:** Agent gedraagt zich volgens de rol

### File Structuur
```
agent-zero/
├── select-agent.sh                              # Interactive selector
├── python/extensions/message_loop_prompts/
│   └── _02_load_specialized_role.py            # Role loader extension
└── prompts/specialized-agents/
    ├── role.master_orchestrator.md             # Roles
    ├── role.code_specialist.md
    ├── role.knowledge_researcher.md
    ├── role.memory_manager.md
    ├── role.web_scraper.md
    ├── role.task_orchestrator.md
    ├── role.solution_architect.md
    ├── communication.md                        # Communication guidelines
    ├── README.md                               # Overview
    └── QUICK_START.md                          # Quick reference
```

---

## 💡 USE CASES & VOORBEELDEN

### Use Case 1: Software Development
```bash
# Start als Code Specialist
export AGENT_ZERO_ROLE=code_specialist
./run-termux.sh

# Vraag:
"Create a Python script to analyze CSV files and generate charts"
```

### Use Case 2: Research Project
```bash
# Start als Research Specialist
export AGENT_ZERO_ROLE=knowledge_researcher
./run-termux.sh

# Vraag:
"Research the latest developments in AI agents and summarize key findings"
```

### Use Case 3: Web Data Collection
```bash
# Start als Web Scraper
export AGENT_ZERO_ROLE=web_scraper
./run-termux.sh

# Vraag:
"Extract product information from this e-commerce site"
```

### Use Case 4: Complex Project
```bash
# Start als Master Orchestrator
export AGENT_ZERO_ROLE=master_orchestrator
./run-termux.sh

# Vraag:
"Design and implement a complete REST API with database and documentation"
```

---

## 🎯 WANNEER WELKE AGENT GEBRUIKEN?

| Taak Type | Beste Agent | Waarom |
|-----------|-------------|--------|
| **Code schrijven** | Code Specialist | Geoptimaliseerd voor development |
| **Online research** | Research Specialist | Expert in information retrieval |
| **Data scraping** | Web Scraper | Gespecialiseerd in extractie |
| **Geheugen beheer** | Memory Manager | Memory operations expert |
| **Complexe projecten** | Master Orchestrator | Coördinatie capabilities |
| **Multi-step workflows** | Task Orchestrator | Delegatie expertise |
| **Architecture design** | Solution Architect | Strategic thinking |
| **General purpose** | Default Agent | All-round capabilities |

---

## 🔄 SWITCHEN TUSSEN AGENTS

### Tijdens Runtime
Je kunt **niet** switchen tijdens een sessie. Stop de agent en start opnieuw met een andere rol.

### Meerdere Sessies
Je kunt meerdere terminal sessions hebben met verschillende agents:

**Terminal 1:**
```bash
export AGENT_ZERO_ROLE=code_specialist
./run-termux.sh
```

**Terminal 2:**
```bash
export AGENT_ZERO_ROLE=research_specialist
./run-termux.sh
```

---

## 🎨 CUSTOMIZATION

### Maak Je Eigen Specialized Agent

1. **Maak rol prompt:**
```bash
nano prompts/specialized-agents/role.my_specialist.md
```

2. **Definieer de rol:**
```markdown
# My Custom Specialist

You are a specialist in [YOUR DOMAIN].

## Core Responsibilities
- [Responsibility 1]
- [Responsibility 2]

## Expertise
- [Skill 1]
- [Skill 2]

## Approach
[How you work]
```

3. **Update selector:**
```bash
nano select-agent.sh
# Add new option to menu
```

4. **Update extension:**
```bash
nano python/extensions/message_loop_prompts/_02_load_specialized_role.py
# Add to role_files dictionary
```

---

## 📊 FEATURE COMPARISON

| Feature | Default | Specialized |
|---------|---------|-------------|
| **General Tasks** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Expert Tasks** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Context Focus** | Broad | Narrow & Deep |
| **Tool Usage** | All tools | Role-specific focus |
| **Efficiency** | Good | Excellent (in domain) |

---

## 🆘 TROUBLESHOOTING

### Agent Rol Laadt Niet
```bash
# Check of rol file bestaat:
ls -la prompts/specialized-agents/role.*.md

# Check environment variable:
echo $AGENT_ZERO_ROLE

# Check extension:
ls -la python/extensions/message_loop_prompts/_02_load_specialized_role.py
```

### Selector Script Werkt Niet
```bash
# Maak executable:
chmod +x select-agent.sh

# Test direct:
./select-agent.sh
```

### Welke Rol Is Actief?
Bij start zie je:
```
🎭 Loaded Specialized Role: Code Specialist
```

---

## 📚 EXTRA DOCUMENTATIE

- **Volledige Guide:** `prompts/specialized-agents/README.md`
- **Quick Start:** `prompts/specialized-agents/QUICK_START.md`
- **Communication:** `prompts/specialized-agents/communication.md`

---

## ✅ QUICK REFERENCE

```bash
# Interactive selector
./select-agent.sh

# Direct start met rol
export AGENT_ZERO_ROLE=code_specialist && ./run-termux.sh

# Beschikbare rollen
master_orchestrator
code_specialist
knowledge_researcher
memory_manager
web_scraper
task_orchestrator
solution_architect
```

---

## 🎉 CONCLUSIE

Je hebt nu **8 verschillende manieren** om Agent Zero te starten:

1. **7 Specialized Agents** - Voor specifieke expertise
2. **1 Default Agent** - Voor algemeen gebruik

**Plus 2 runtime omgevingen:**
- Native Termux (snelst)
- Ubuntu Container (volledig)

**= 16 verschillende configuraties!** 🚀

---

*Specialized Agents v1.0*
*Compatible met Agent Zero v2.0*
*Werkt in Termux & Ubuntu*
