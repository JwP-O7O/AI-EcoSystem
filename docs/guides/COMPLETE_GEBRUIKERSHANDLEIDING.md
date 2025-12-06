# 🤖 Agent Zero Android - Complete Gebruikershandleiding

**Versie:** 2.0
**Datum:** 29 November 2025
**Platform:** Android/Termux

---

## 📋 Inhoudsopgave

1. [Quick Start (5 minuten)](#quick-start)
2. [Alle Beschikbare Tools](#alle-tools)
3. [Specialized Agents Gebruiken](#specialized-agents)
4. [Praktische Voorbeelden](#voorbeelden)
5. [Troubleshooting](#troubleshooting)
6. [Best Practices](#best-practices)
7. [Advanced Tips](#advanced-tips)

---

## 🚀 Quick Start {#quick-start}

### Methode 1: Interactive Menu (Aanbevolen)

```bash
bash android-versie/scripts/quick_start.sh
```

Dit opent een interactief menu met alle opties:
- 🚀 Start Agent Zero
- 🎯 Specialized Agent Selector
- 🏥 Health Check
- ⚙️  Configuration Info
- 📚 Documentation

### Methode 2: Direct Starten

```bash
bash android-versie/agent0_wrapper.sh
```

### Methode 3: Python Direct

```bash
python android-versie/run_android_cli.py
```

---

## 🛠️ Alle Beschikbare Tools {#alle-tools}

### 1. **Quick Start Menu** ⭐ NIEUW!

**Commando:**
```bash
bash android-versie/scripts/quick_start.sh
```

**Wat doet het:**
- Centraal menu voor alle Agent Zero functies
- Eenvoudige navigatie
- Toegang tot alle tools en documentatie

**Gebruik:**
Ideaal als je niet zeker weet wat je wilt doen. Het menu begeleidt je.

---

### 2. **Agent Selector** ⭐ NIEUW!

**Commando:**
```bash
python android-versie/scripts/agent_selector.py
```

**Wat doet het:**
- Interactieve selectie van specialized agents
- Genereert correcte prompts automatisch
- Kopieert prompt naar clipboard (Termux)
- Kan direct Agent Zero starten

**Gebruik:**
Perfect wanneer je een specifieke taak hebt maar niet zeker weet welke agent te gebruiken.

**Voorbeeld Flow:**
1. Run het script
2. Kies agent (bijv. "2" voor Code Specialist)
3. Beschrijf je taak: "Write a CSV parser"
4. Krijg complete prompt
5. Start Agent Zero direct of kopieer prompt

---

### 3. **Health Check** ⭐ NIEUW!

**Commando:**
```bash
python android-versie/scripts/health_check.py
```

**Wat doet het:**
- Checkt alle dependencies
- Verifieert configuratie
- Test API keys
- Controleert Agent Zero componenten
- Geeft concrete fix suggesties

**Output:**
```
✓ Python Version         v3.12.12
✓ Termux Environment     detected
✓ langchain              installed
✓ GOOGLE_API_KEY         AIza...klGo
✓ Configuration Load     success

✅ All checks passed!
```

**Gebruik:**
- Na installatie om te verifiëren
- Bij problemen om diagnose te krijgen
- Voor updates checken

---

### 4. **Agent Zero CLI**

**Commando:**
```bash
bash android-versie/agent0_wrapper.sh
```

**Wat doet het:**
- Start Agent Zero in je huidige directory
- Behoudt working directory
- Optimized voor Android/Termux

**Chat Commando's:**
- `e` - Exit Agent Zero
- Regular text - Stuur bericht naar agent
- Bij timeout: `w` - Wacht langer

**Voorbeeld Sessie:**
```
You:
→ Write a Python script to list all .py files

Agent0: response:
I'll write a Python script to list all Python files...

[Code execution happens...]

Done! Found 47 .py files.
```

---

## 🎯 Specialized Agents Gebruiken {#specialized-agents}

### Beschikbare Agents

| Agent | Icon | Gebruik Voor |
|-------|------|--------------|
| **Master Orchestrator** | 🎯 | Complexe multi-step workflows |
| **Code Specialist** | 💻 | Python/JS code, scripting |
| **Research Specialist** | 🔍 | Online research, informatie zoeken |
| **Web Scraper** | 🌐 | Website scraping, data extractie |
| **Solution Architect** | 🏗️ | Systeem ontwerp, architectuur |
| **Memory Manager** | 🧠 | Knowledge opslaan/ophalen |
| **Task Orchestrator** | 📋 | Workflow coördinatie |

### Methode 1: Via Agent Selector (Makkelijkst)

```bash
python android-versie/scripts/agent_selector.py
```

1. Selecteer agent nummer
2. Beschrijf taak
3. Krijg prompt
4. Start Agent Zero

### Methode 2: Handmatige Prompt

Start Agent Zero en type:

```
You are a [ROL NAAM]. [TAAK BESCHRIJVING]
```

**Voorbeelden:**

**Code Specialist:**
```
You are a Code Execution Specialist. Write a Python script
that reads data.csv, filters rows where amount > 100,
and saves to filtered.csv
```

**Research Specialist:**
```
You are a Knowledge Research Specialist. Find the latest
best practices for Python async programming in 2025
```

**Master Orchestrator:**
```
You are a Master Orchestrator. I need to build a web scraper
that extracts product data from e-commerce sites, stores it
in a database, and generates weekly reports. Coordinate all
necessary specialists to complete this project.
```

---

## 💡 Praktische Voorbeelden {#voorbeelden}

### Voorbeeld 1: Data Processing Pipeline

**Doel:** CSV file inlezen, filteren, en visualiseren

**Agent:** Code Specialist

**Prompt:**
```
You are a Code Execution Specialist. I have sales_data.csv
with columns: date, product, amount, region.

Please:
1. Read the CSV
2. Filter sales > $1000
3. Group by region
4. Create a summary
5. Save to summary.csv
```

**Verwachte Output:**
Agent schrijft en voert Python code uit, toont resultaten.

---

### Voorbeeld 2: Research + Implementation

**Doel:** Best practice vinden en implementeren

**Agent:** Master Orchestrator

**Prompt:**
```
You are a Master Orchestrator. I need to implement
rate limiting for an API. First research best practices,
then design a solution, and finally implement it in Python.
```

**Agent Flow:**
1. Delegeert naar Research Specialist → zoekt info
2. Delegeert naar Architect → ontwerpt solution
3. Delegeert naar Code Specialist → implementeert
4. Presenteert resultaat

---

### Voorbeeld 3: Web Scraping Project

**Agent:** Web Scraper

**Prompt:**
```
You are a Web Content Extraction Specialist. Extract all
article titles and URLs from https://news.ycombinator.com
and save them to a JSON file.
```

---

### Voorbeeld 4: Knowledge Management

**Agent:** Memory Manager

**First, save knowledge:**
```
You are a Memory Manager. Please save this important information:
- Project uses Python 3.12
- Main database: PostgreSQL 15
- API framework: FastAPI
- Deployment: Docker on AWS
Tag this as "project-setup"
```

**Later, retrieve:**
```
You are a Memory Manager. What do you remember about our project setup?
```

---

## 🔧 Troubleshooting {#troubleshooting}

### Probleem 1: "ModuleNotFoundError"

**Symptoom:**
```
ModuleNotFoundError: No module named 'langchain'
```

**Oplossing:**
```bash
# Run health check voor diagnose
python android-versie/scripts/health_check.py

# Installeer ontbrekende packages
pip install -r android-versie/requirements-android.txt
```

---

### Probleem 2: "API Key Error"

**Symptoom:**
```
Error: No API key found
```

**Oplossing:**
```bash
# Check .env file
cat android-versie/config/.env

# Edit en voeg key toe
nano android-versie/config/.env

# Voeg toe:
GOOGLE_API_KEY=your_key_here
# OF
OPENAI_API_KEY=sk-...
# OF
ANTHROPIC_API_KEY=sk-ant-...
```

---

### Probleem 3: Agent Start Niet

**Oplossing:**
```bash
# 1. Run health check
python android-versie/scripts/health_check.py

# 2. Check Python versie (moet ≥3.11 zijn)
python --version

# 3. Test configuratie
python -c "import sys; sys.path.insert(0, 'android-versie/config'); from initialize_android import initialize; initialize()"

# 4. Check logs
cat logs/agent.log  # Als beschikbaar
```

---

### Probleem 4: Memory Errors

**Symptoom:**
```
MemoryError
```

**Oplossing:**

Edit `android-versie/config/initialize_android.py`:

```python
# Verlaag memory gebruik
msgs_keep_max=10,           # Was: 20
max_tool_response_length=1000,  # Was: 2000
```

---

### Probleem 5: "Timeout" Errors

**Symptoom:**
Agent reageert niet of timeout

**Oplossing:**

Edit `initialize_android.py`:

```python
response_timeout_seconds=120,  # Was: 60
```

Of gebruik sneller model:
```python
# In .env:
LLM_PROVIDER=groq  # Snelste optie
```

---

## 🎯 Best Practices {#best-practices}

### 1. **Kies de Juiste Agent**

| Taak Type | Agent |
|-----------|-------|
| Code schrijven | Code Specialist |
| Info zoeken | Research Specialist |
| Complex project | Master Orchestrator |
| Web data | Web Scraper |
| Ontwerp | Solution Architect |

**Tip:** Gebruik Agent Selector als je twijfelt!

### 2. **Schrijf Duidelijke Prompts**

❌ **Slecht:**
```
make me a thing
```

✅ **Goed:**
```
You are a Code Execution Specialist. Write a Python function
that takes a list of numbers and returns the median. Include
error handling for empty lists.
```

**Principes:**
- Start met rol ("You are a...")
- Wees specifiek over input/output
- Vermeld edge cases
- Geef context waar nodig

### 3. **Gebruik Working Directory**

Agent Zero werkt in je huidige directory:

```bash
# Navigate to project
cd ~/my-project

# Start agent (het onthoud ~/my-project als working dir)
bash ~/AI-EcoSystem/android-versie/agent0_wrapper.sh

# Agent kan nu files in ~/my-project lezen/schrijven
```

### 4. **Itereer Stapsgewijs**

Voor complexe taken:

```
Step 1: Research best approach
Step 2: Design architecture
Step 3: Implement core functionality
Step 4: Add error handling
Step 5: Test thoroughly
```

### 5. **Monitor API Usage**

```bash
# Check je API dashboard regelmatig
# Google AI Studio: https://aistudio.google.com/
# OpenAI: https://platform.openai.com/usage
```

### 6. **Save Belangrijke Output**

```
You are a Code Execution Specialist. [taak]
Please save the final code to solution.py
```

---

## 🚀 Advanced Tips {#advanced-tips}

### Tip 1: Model Switching

**Quick Switch via .env:**

```bash
# Edit .env
nano android-versie/config/.env

# Change provider
LLM_PROVIDER=groq  # Snelst, gratis
# LLM_PROVIDER=google  # Goed, gratis tier
# LLM_PROVIDER=openai  # Best quality
# LLM_PROVIDER=anthropic  # Claude
```

**No restart needed** - Agent leest .env bij elke start.

---

### Tip 2: Multi-Agent Workflows

**Master Orchestrator coordinating:**

```
You are a Master Orchestrator. Build a blog platform:

1. Research Specialist: Find best Python web frameworks
2. Solution Architect: Design the architecture
3. Code Specialist: Implement backend API
4. Code Specialist: Implement frontend
5. Memory Manager: Document the architecture
```

Agent delegeert automatisch!

---

### Tip 3: Custom Agent Roles

Maak je eigen agent:

```
You are a [CUSTOM ROLE]. You specialize in [EXPERTISE].

Your task: [SPECIFIC TASK]

Rules:
- [RULE 1]
- [RULE 2]
```

**Voorbeeld - Data Analyst Agent:**
```
You are a Data Analysis Specialist. You excel at statistical
analysis, data visualization, and insight generation using Python
(pandas, matplotlib, seaborn).

Task: Analyze sales_data.csv and identify trends

Rules:
- Always visualize findings
- Provide statistical significance
- Suggest actionable insights
```

---

### Tip 4: Conversation Context

Agent onthoudt conversatie binnen sessie:

```
You:
→ Create a list of 10 random numbers and save to numbers.txt

Agent: [Creates file]

You:
→ Now calculate the average of those numbers

Agent: [Reads numbers.txt, calculates]  # Remembers context!
```

---

### Tip 5: Batch Operations

```
You are a Code Execution Specialist. Process all .csv files
in the data/ directory:
1. Read each file
2. Remove duplicates
3. Save to cleaned/ directory with same name
```

Agent loopt door alle files!

---

### Tip 6: Use Health Check Regularly

```bash
# Weekly check
python android-versie/scripts/health_check.py

# After updates
pip install --upgrade -r android-versie/requirements-android.txt
python android-versie/scripts/health_check.py
```

---

## 📞 Support & Resources

### Documentation

- **Deze Guide:** `COMPLETE_GEBRUIKERSHANDLEIDING.md`
- **Quick Ref:** `QUICK_REFERENCE.md`
- **Specialized Agents:** `docs/SPECIALIZED_AGENTS_GUIDE.md`
- **Setup:** `TERMUX_SETUP_PLAN.md`
- **Changes:** `WIJZIGINGEN_OVERZICHT.md`

### Tools

```bash
# Interactive menu
bash android-versie/scripts/quick_start.sh

# Agent selector
python android-versie/scripts/agent_selector.py

# Health check
python android-versie/scripts/health_check.py
```

### Community

- **Agent Zero Discord:** https://discord.gg/B8KZKNsPpj
- **GitHub:** https://github.com/frdel/agent-zero

---

## 🎉 Quick Command Reference

```bash
# === Starting ===
bash android-versie/scripts/quick_start.sh          # Interactive menu
bash android-versie/agent0_wrapper.sh               # Direct start
python android-versie/run_android_cli.py            # Python direct

# === Tools ===
python android-versie/scripts/agent_selector.py     # Choose agent
python android-versie/scripts/health_check.py       # Diagnostics

# === Maintenance ===
pip install -r android-versie/requirements-android.txt   # Update deps
nano android-versie/config/.env                          # Edit config

# === Info ===
cat android-versie/README.md                        # Overview
cat COMPLETE_GEBRUIKERSHANDLEIDING.md              # This guide
```

---

## ✅ Checklist voor Eerste Gebruik

- [ ] Run health check: `python android-versie/scripts/health_check.py`
- [ ] Check .env heeft minimaal 1 API key
- [ ] Test start: `bash android-versie/agent0_wrapper.sh`
- [ ] Probeer eenvoudige prompt: "Write hello world in Python"
- [ ] Test specialized agent via selector
- [ ] Bookmark dit document!

---

**🎊 Je bent nu klaar om Agent Zero op Android te gebruiken!**

**Veel plezier met je AI Assistant! 🤖📱**

---

*Versie 2.0 - November 29, 2025*
*Voor Agent Zero Android/Termux Edition*
