# ⚡ Agent Zero Android - Snelstart Gids

**Voor wie?** Iedereen die snel wil beginnen met Agent Zero op Android
**Tijd nodig:** 2 minuten om te lezen, 30 seconden om te starten

---

## 🚀 Starten in 3 Stappen

### Stap 1: Open het Menu

```bash
bash android-versie/scripts/quick_start.sh
```

### Stap 2: Kies een Optie

Je ziet:
```
[1] 🚀 Start Agent Zero
[2] 🎯 Specialized Agent Selector
[3] 🏥 Health Check
[4] ⚙️  Configuration Info
[5] 📚 Documentation
```

### Stap 3: Start!

**Eerste keer?** → Kies `[3] Health Check` om te verifiëren
**Daarna?** → Kies `[1] Start Agent Zero` of `[2] Agent Selector`

---

## 💡 Of Direct Starten

```bash
# Simpelste manier
bash android-versie/agent0_wrapper.sh
```

Je ziet:
```
🤖 Agent Zero Ready
You:
→ [Type je vraag hier]
```

**Probeer bijvoorbeeld:**
```
→ Write a Python script that prints "Hello World"
```

**Of:**
```
→ You are a Code Execution Specialist. List all .py files in the current directory
```

---

## 🎯 Welke Agent Voor Welke Taak?

| Wil je... | Gebruik... | Prompt start |
|-----------|------------|--------------|
| Code schrijven | Code Specialist | `You are a Code Execution Specialist.` |
| Info zoeken | Research Specialist | `You are a Knowledge Research Specialist.` |
| Website scrapen | Web Scraper | `You are a Web Content Extraction Specialist.` |
| Complex project | Master Orchestrator | `You are a Master Orchestrator.` |
| Iets ontwerpen | Solution Architect | `You are a Solution Architecture Specialist.` |

**Niet zeker?**
```bash
python android-versie/scripts/agent_selector.py
```
→ Interactieve agent keuze!

---

## 🔧 Problemen?

### "Module not found"
```bash
pip install -r android-versie/requirements-android.txt
```

### "API key error"
```bash
nano android-versie/config/.env
# Voeg toe: GOOGLE_API_KEY=your_key
```

### Alles checken
```bash
python android-versie/scripts/health_check.py
```

---

## 📚 Meer Weten?

**Complete guide:** `cat COMPLETE_GEBRUIKERSHANDLEIDING.md`

**Alle commando's:** `cat ANDROID_PROJECT_UPGRADE_COMPLEET.md`

**Quick reference:** `cat QUICK_REFERENCE.md`

---

## ⚡ Top 5 Meest Gebruikte Commando's

```bash
# 1. Main menu (start hier!)
bash android-versie/scripts/quick_start.sh

# 2. Direct starten
bash android-versie/agent0_wrapper.sh

# 3. Agent kiezen
python android-versie/scripts/agent_selector.py

# 4. Check systeem
python android-versie/scripts/health_check.py

# 5. Config bekijken
cat android-versie/config/.env
```

---

## 🎯 Eerste Project Voorbeeld

```bash
# 1. Start Agent Zero
bash android-versie/agent0_wrapper.sh

# 2. Type in Agent Zero:
You are a Code Execution Specialist.

Create a Python script that:
1. Asks user for their name
2. Saves it to greeting.txt
3. Reads it back and prints a greeting

# 3. Agent schrijft en runt de code
# 4. Je hebt je eerste project! 🎉
```

---

## 💪 Pro Tips

1. **Gebruik het Quick Start Menu** - het maakt alles makkelijker
2. **Begin met Health Check** - weet zeker dat alles werkt
3. **Agent Selector helpt** - als je niet zeker bent welke agent
4. **Wees specifiek** - hoe duidelijker je prompt, hoe beter het resultaat
5. **Experimenteer!** - Agent Zero is veilig om mee te spelen

---

**Dat is alles! Je bent klaar om te beginnen! 🚀**

**Veel plezier met Agent Zero! 🤖📱**

---

*Voor meer details: zie COMPLETE_GEBRUIKERSHANDLEIDING.md*
