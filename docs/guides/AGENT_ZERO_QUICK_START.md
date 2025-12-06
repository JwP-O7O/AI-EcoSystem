# Agent Zero v3.0 - Quick Start Gids

**Snelle start voor je Agent Zero installatie op Android/Termux**

---

## 🚀 Start Agent Zero

```bash
cd /data/data/com.termux/files/home/AI-EcoSystem/agent-zero
python run_cli.py
```

Of gebruik de root versie:
```bash
cd /data/data/com.termux/files/home/AI-EcoSystem
python agent.py
```

---

## 🤖 Sub-Agents Gebruiken

### Methode 1: Gewoon vragen (Aanbevolen!)

Gewoon in normale taal vragen. De AI roept automatisch de juiste sub-agent aan:

```
Jij: "Schrijf Python code om CSV data te analyseren"
→ Agent roept automatisch Code Specialist aan

Jij: "Zoek informatie over beste PDF libraries voor Termux"
→ Agent roept automatisch Knowledge Researcher aan

Jij: "Scrape product prices van example.com"
→ Agent roept automatisch Web Scraper aan
```

### Methode 2: Interactieve Selector Tool

```bash
python tools/select_agent_role.py
```

Dit geeft je:
- AI-aanbeveling voor beste agent
- Overzicht van alle agents
- Ready-to-use JSON voor call_subordinate
- Tips voor effectief gebruik

### Methode 3: Direct via JSON (Gevorderd)

Voor full control, gebruik `call_subordinate` direct:

```json
{
    "thoughts": ["Need Code Specialist for this task"],
    "tool_name": "call_subordinate",
    "tool_args": {
        "message": "You are a Code Execution Specialist.

CONTEXT: User has CSV file at /sdcard/data.csv

TASK: Read CSV, calculate averages, save to /sdcard/results.csv

REQUIREMENTS:
- Use pandas
- Handle missing values
- Include error handling

EXPECTED OUTPUT: Summary of results",
        "reset": "true"
    }
}
```

---

## 🛠️ Beschikbare Tools

### Android Features
```bash
# Notificatie sturen
android_features → feature: "notification"

# Text-to-speech
android_features → feature: "tts"

# GPS locatie
android_features → feature: "location"

# Battery status
android_features → feature: "battery"

# Foto maken
android_features → feature: "camera"
```

### Memory Management
```bash
# Opslaan
persistent_memory → operation: "store"

# Zoeken
persistent_memory → operation: "search"

# Ophalen
persistent_memory → operation: "recall"
```

### Voice Interface
```bash
# Spreken
voice_interface → mode: "speak"

# Luisteren
voice_interface → mode: "listen"
```

### Task Management
```bash
# Task maken
task_manager → operation: "create"

# Tasks tonen
task_manager → operation: "list"

# Task voltooien
task_manager → operation: "complete"
```

---

## 📱 Android Paths

```bash
# User files
/sdcard/

# Downloads
/sdcard/Download/

# Foto's
/sdcard/DCIM/

# Agent Zero home
/data/data/com.termux/files/home/AI-EcoSystem/
```

---

## 🎯 Agent Rollen Cheat Sheet

| Agent | Gebruik voor |
|-------|-------------|
| **coder** | Python/Bash code schrijven en uitvoeren |
| **researcher** | Online zoeken, info opzoeken |
| **memory** | Info opslaan/ophalen voor later |
| **scraper** | Websites scrapen |
| **orchestrator** | Multi-step taken coördineren |
| **architect** | Systeem design, strategie |
| **master** | Complex project coördinatie |

---

## 💡 Handige Commando's

### Agent Zero
```bash
# Start agent
python agent.py

# Check logs
tail -f logs/agent.log

# View memory
ls -la memory/

# View knowledge base
ls -la knowledge/
```

### Termux API (voor Android features)
```bash
# Check Termux API
pkg list-installed | grep termux-api

# Installeer indien nodig
pkg install termux-api

# Test notificatie
termux-notification --title "Test" --content "Het werkt!"

# Test TTS
termux-tts-speak "Hallo wereld"

# Check battery
termux-battery-status
```

---

## 📚 Documentatie

### Uitgebreide Gidsen
```bash
# Sub-agent mastery
cat docs/SUB_AGENT_MASTERY.md

# Complete gebruikershandleiding
cat COMPLETE_GEBRUIKERSHANDLEIDING.md

# Android setup
cat ANDROID_INSTALLATIE_COMPLEET.md

# Gemini configuratie
cat GEMINI_CONFIGURATIE_COMPLEET.md
```

### Tool Prompts
```bash
ls agent-zero/prompts/default/agent.system.tool.*.md
```

---

## 🔧 Troubleshooting

### Agent start niet
```bash
# Check Python
python --version

# Check dependencies
pip list | grep google-generativeai

# Check .env
cat android-versie/config/.env
```

### Termux API werkt niet
```bash
# Installeer Termux:API app (via F-Droid of Play Store)
# Dan:
pkg install termux-api
```

### Memory errors
```bash
# Check memory directory
ls -la memory/

# Create if missing
mkdir -p memory/main
```

### Docker errors
```bash
# Docker staat uit (correct voor Android!)
# Check initialize.py regel 59:
grep "code_exec_docker_enabled" agent-zero/initialize.py
# Moet zijn: False
```

---

## ⚡ Snelle Voorbeelden

### Voorbeeld 1: CSV Analyse
```
Vraag: "Read /sdcard/sales.csv, calculate total revenue, and save to /sdcard/summary.csv"

Agent doet automatisch:
1. Roept Code Specialist aan
2. Schrijft pandas code
3. Voert uit
4. Rapporteert resultaten
```

### Voorbeeld 2: Research + Implementeer
```
Vraag: "Find best JSON parser for Python and show me an example"

Agent doet:
1. Knowledge Researcher zoekt info
2. Code Specialist maakt voorbeeld
3. Rapporteert beiden
```

### Voorbeeld 3: Voice Timer
```
Vraag: "Create a voice-controlled 5-minute timer with notification"

Agent doet:
1. Gebruikt voice_interface om te luisteren
2. Gebruikt task_scheduler om timer te zetten
3. Stuurt notificatie na 5 minuten
```

---

## 🎓 Leer Meer

### Stap voor Stap
1. ✅ Start met simpele vragen
2. ✅ Probeer `python tools/select_agent_role.py`
3. ✅ Lees `docs/SUB_AGENT_MASTERY.md`
4. ✅ Experimenteer met JSON call_subordinate
5. ✅ Bouw complexere workflows

### Best Practices
- **Wees specifiek**: Geef duidelijke instructies
- **Gebruik reset: "true"**: Voor schone context
- **Android features**: Maak gebruik van notifications/TTS
- **Sla op in memory**: Belangrijke oplossingen bewaren
- **Test eerst**: Probeer klein, schaal op

---

## 🆘 Hulp Nodig?

```bash
# In Agent Zero chat:
"How do I use [tool name]?"
"Show me all available tools"
"What can you do?"

# Documentatie:
cat docs/SUB_AGENT_MASTERY.md
cat COMPLETE_GEBRUIKERSHANDLEIDING.md

# Tool selector:
python tools/select_agent_role.py
```

---

## ✨ Pro Tips

1. **Parallelle taken**: Vraag meerdere dingen tegelijk
   ```
   "Search for PDF libraries AND check my battery status"
   ```

2. **Android notificaties**: Vraag om notificatie bij completion
   ```
   "Process this data and send notification when done"
   ```

3. **Voice feedback**: Voor hands-free
   ```
   "Analyze data and speak the results"
   ```

4. **Memory voor later**: Sla successen op
   ```
   "Save this solution to memory for future use"
   ```

5. **Batch operaties**: Meerdere bestanden tegelijk
   ```
   "Process all CSV files in /sdcard/data/"
   ```

---

**Veel succes met Agent Zero v3.0! 🚀**

*Laatst bijgewerkt: 2025-11-29*
