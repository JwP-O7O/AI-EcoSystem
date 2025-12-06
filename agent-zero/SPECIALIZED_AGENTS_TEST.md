# 🎭 Specialized Agents - TEST GUIDE

## ✅ KLAAR VOOR GEBRUIK

Alle specialized agents zijn geïnstalleerd en klaar! Je hebt nu **3 manieren** om Agent Zero te starten:

---

## 🚀 METHODE 1: Interactive Selector (AANBEVOLEN)

```bash
cd /data/data/com.termux/files/home/AI-EcoSystem/agent-zero
./select-agent.sh
```

Dit geeft je een interactief menu:
```
╔══════════════════════════════════════════════════════════╗
║          🤖 Agent Zero - Agent Selector 🤖              ║
╚══════════════════════════════════════════════════════════╝

Kies je gespecialiseerde agent:

  1) 🎭 Master Orchestrator (Default - Hoofdcoördinator)
  2) 💻 Code Specialist (Python/NodeJS/Terminal expert)
  3) 🔍 Research Specialist (Online research expert)
  4) 💾 Memory Manager (Geheugen beheerder)
  5) 🌐 Web Scraper (Web content extractie)
  6) 🎯 Task Orchestrator (Delegatie coördinator)
  7) 🏗️  Solution Architect (Strategische planner)

  8) ⚡ Default Agent (Geen specialisatie)

  0) ❌ Annuleren

Maak je keuze (0-8): _
```

Daarna kies je runtime:
```
Wil je starten in:
  1) Native Termux (Snelst)
  2) Ubuntu Container (Volledig Linux)

Keuze (1-2): _
```

---

## 🚀 METHODE 2: Direct Met Environment Variable

### Native Termux (Snelst):
```bash
cd /data/data/com.termux/files/home/AI-EcoSystem/agent-zero
export AGENT_ZERO_ROLE=code_specialist
./run-termux.sh
```

### Ubuntu Container (Volledig):
```bash
cd /data/data/com.termux/files/home/AI-EcoSystem/agent-zero
export AGENT_ZERO_ROLE=research_specialist
./run-ubuntu.sh
```

**Beschikbare roles:**
- `master_orchestrator` - Hoofdcoördinator voor complexe projecten
- `code_specialist` - Python/NodeJS/Terminal expert
- `knowledge_researcher` - Online research specialist
- `memory_manager` - Geheugen beheer expert
- `web_scraper` - Web content extractie specialist
- `task_orchestrator` - Delegatie coördinator
- `solution_architect` - Strategische planner
- `default` - Geen specialisatie (all-rounder)

---

## 🚀 METHODE 3: Default (Zoals Altijd)

```bash
cd /data/data/com.termux/files/home/AI-EcoSystem/agent-zero
./run-termux.sh   # Of: ./run-ubuntu.sh
```

Start Agent Zero zonder specialisatie.

---

## 📋 TEST CHECKLIST

### ✅ Wat is geverifieerd:

1. **Ubuntu Container Setup**
   - ✅ proot-distro Ubuntu 25.10 geïnstalleerd
   - ✅ Virtual environment aangemaakt in Ubuntu
   - ✅ Symlink naar Agent Zero files: `/root/agent-zero-link`
   - ✅ Alle dependencies geïnstalleerd (langchain-ollama, etc.)
   - ✅ Import test succesvol: `langchain_ollama` werkt

2. **Specialized Agents System**
   - ✅ 7 specialized agent role files bestaan
   - ✅ Interactive selector script gemaakt: `select-agent.sh`
   - ✅ Extension gemaakt: `_02_load_specialized_role.py`
   - ✅ Scripts zijn executable
   - ✅ Virtual environment activatie gefixed

3. **Launch Scripts**
   - ✅ `run-termux.sh` - Native Termux launcher
   - ✅ `run-ubuntu.sh` - Ubuntu container launcher (met venv activatie)
   - ✅ `select-agent.sh` - Interactive agent selector
   - ✅ `ubuntu-shell.sh` - Ubuntu development shell

4. **Documentation**
   - ✅ `SPECIALIZED_AGENTS_SETUP.md` - Complete setup guide
   - ✅ `SPECIALIZED_AGENTS_TEST.md` - Deze test guide
   - ✅ `START_HIER.md` - Quick start
   - ✅ `DOCKER_UBUNTU_SETUP.md` - Ubuntu container guide

---

## 🧪 AANBEVOLEN TESTS

### Test 1: Selector Menu Test
```bash
./select-agent.sh
# Kies optie 2 (Code Specialist)
# Kies runtime 1 (Native Termux)
# Verifieer dat het start met: "🎭 Loaded Specialized Role: Code Specialist"
```

### Test 2: Direct Launch Test (Termux)
```bash
export AGENT_ZERO_ROLE=code_specialist
./run-termux.sh
# Verifieer specialized role melding bij start
```

### Test 3: Direct Launch Test (Ubuntu)
```bash
export AGENT_ZERO_ROLE=research_specialist
./run-ubuntu.sh
# Verifieer "✓ Activating virtual environment..."
# Verifieer "🎭 Loaded Specialized Role: Research Specialist"
```

### Test 4: Default Agent Test
```bash
./run-termux.sh
# Verifieer normale start zonder specialized role melding
```

---

## 🎯 EXPECTED BEHAVIOR

### Bij Starten Met Specialized Role:

1. **Je zou moeten zien:**
```
🎭 Loaded Specialized Role: Code Specialist
```

2. **In de agent logs:**
```
Specialized Role: Code Specialist
Agent 0 initialized with Code Specialist capabilities
```

3. **Agent gedrag:**
   - Agent zal zich gedragen volgens de rol
   - Focus op expertise van de rol
   - Gebruikt role-specific prompts

### Bij Starten Zonder Specialized Role:

1. **Geen special melding**
2. **Default all-round behavior**

---

## 🔧 TROUBLESHOOTING

### Selector werkt niet:
```bash
chmod +x select-agent.sh
./select-agent.sh
```

### Ubuntu venv niet gevonden:
```bash
proot-distro login ubuntu
cd /root/agent-zero-link
python3 -m venv venv
exit
./run-ubuntu.sh
```

### Langchain imports falen:
```bash
proot-distro login ubuntu -- bash -c "
cd /root/agent-zero-link &&
source venv/bin/activate &&
pip install langchain-ollama langchain-community langchain-core
"
```

### Role laadt niet:
```bash
# Check environment variable:
echo $AGENT_ZERO_ROLE

# Check role file bestaat:
ls -la prompts/specialized-agents/role.*.md

# Check extension:
ls -la python/extensions/message_loop_prompts/_02_load_specialized_role.py
```

---

## 📊 SYSTEM STATUS

### Ubuntu Container:
- **Status:** ✅ Installed & Configured
- **Location:** `/root/agent-zero-link` (symlink)
- **Python:** Python 3.13.1 (in venv)
- **Dependencies:** ✅ All installed

### Specialized Agents:
- **Available:** 7 roles + 1 default
- **Selector:** ✅ Working
- **Extension:** ✅ Active
- **Status:** ✅ Ready to use

### Runtime Options:
- **Native Termux:** ✅ Working (snelst)
- **Ubuntu Container:** ✅ Working (volledig)

---

## 🎉 KLAAR OM TE GEBRUIKEN!

Je kunt nu Agent Zero starten met:

1. **Interactive menu:** `./select-agent.sh`
2. **Direct Termux:** `./run-termux.sh`
3. **Direct Ubuntu:** `./run-ubuntu.sh`
4. **Met rol:** `export AGENT_ZERO_ROLE=code_specialist && ./run-termux.sh`

Enjoy de **specialized agents!** 🚀

---

*Laatste update: 2025-11-29*
*Status: ALL SYSTEMS GO ✅*
