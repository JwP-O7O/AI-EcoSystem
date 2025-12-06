# 🤖 AI-EcoSystem - Termux Setup Plan

**Datum:** November 26, 2025
**Platform:** Android via Termux
**Doel:** Agent Zero Framework volledig werkend krijgen op Android

---

## 📋 Huidige Status

### ✅ Al Geïnstalleerd
- Python 3.12.12
- Docker (`/data/data/com.termux/files/usr/bin/docker`)
- Veel Python packages (anthropic, aiohttp, etc.)
- Claude Code met slash commands in `.claude/commands/`

### 📁 Project Structuur
```
AI-EcoSystem/
├── .claude/
│   └── commands/           # ✅ Slash commands (master, code, research, etc.)
├── agent-zero/            # Agent Zero framework
├── prompts/
│   └── specialized-agents/ # Agent prompts voor Agent Zero
├── requirements.txt       # Dependencies
├── initialize.py          # Configuratie
├── run_cli.py            # Terminal interface
├── run_ui.py             # Web UI
└── agent.py              # Core agent logic
```

---

## 🎯 Implementatie Plan voor Termux

### Phase 1: Dependencies Installeren ⚙️

**Stap 1.1 - Check en installeer system dependencies**
```bash
# Update Termux packages
pkg update && pkg upgrade -y

# Install essentiële build tools
pkg install -y \
  python \
  python-pip \
  git \
  openssh \
  openssl \
  libffi \
  rust \
  binutils \
  clang

# Install Docker dependencies (als Docker nog niet werkt)
pkg install -y docker
```

**Stap 1.2 - Installeer Python dependencies**

Sommige packages kunnen problemen geven op ARM. Strategie:
```bash
cd /data/data/com.termux/files/home/AI-EcoSystem

# Probeer eerst requirements.txt
pip install -r requirements.txt

# Als specifieke packages falen, installeer één voor één:
# Prioriteit packages:
pip install anthropic
pip install openai
pip install langchain-anthropic
pip install langchain-openai
pip install python-dotenv
pip install beautifulsoup4
pip install flask

# Problematische packages voor ARM:
# - faiss-cpu (grote compile, mogelijk skip)
# - docker (check of Termux versie werkt)
# - unstructured (heavy dependencies)
```

**Stap 1.3 - Alternatieve packages voor ARM**
```bash
# Als faiss-cpu faalt (vector search voor memory):
# Optie 1: Skip (memory werkt beperkt)
# Optie 2: Gebruik lightweight alternatieven

# Als docker package faalt:
# Gebruik Termux's docker binary direct
```

---

### Phase 2: Agent Zero Configuratie 🔧

**Stap 2.1 - Configureer initialize.py**

Edit `/data/data/com.termux/files/home/AI-EcoSystem/initialize.py`:

```python
# Voor Termux: Disable Docker, use local execution
config = AgentConfig(
    chat_model = chat_llm,
    utility_model = utility_llm,
    embeddings_model = embedding_llm,
    knowledge_subdirs = ["default","custom"],
    auto_memory_count = 0,
    rate_limit_requests = 30,
    max_tool_response_length = 3000,

    # DISABLE Docker voor Termux (kan instabiel zijn)
    code_exec_docker_enabled = False,

    # DISABLE SSH (niet nodig zonder Docker)
    code_exec_ssh_enabled = False,

    # Code execution zal direct in Termux omgeving draaien
)
```

**Stap 2.2 - API Keys configureren**

Maak `.env` bestand:
```bash
cd /data/data/com.termux/files/home/AI-EcoSystem
nano .env
```

Voeg toe:
```env
# Voor OpenAI (gpt-4o-mini)
OPENAI_API_KEY=your-key-here

# OF voor Anthropic (Claude)
ANTHROPIC_API_KEY=your-key-here

# OF voor Ollama (local, gratis)
# OLLAMA_API_BASE=http://localhost:11434

# OF andere providers...
```

**Stap 2.3 - Kies je LLM provider**

Edit `initialize.py` regel 8 om je gekozen model te activeren:

**Optie A - OpenAI (aanbevolen voor start):**
```python
chat_llm = models.get_openai_chat(model_name="gpt-4o-mini", temperature=0)
```

**Optie B - Anthropic Claude:**
```python
chat_llm = models.get_anthropic_chat(model_name="claude-3-5-sonnet-20240620", temperature=0)
```

**Optie C - Ollama (gratis, local):**
```python
chat_llm = models.get_ollama_chat(model_name="llama3.2:3b-instruct-fp16", temperature=0)
```
*Note: Voor Ollama moet je eerst Ollama installeren in Termux*

---

### Phase 3: Docker Setup (Optioneel) 🐳

**Alleen als je Docker execution wilt:**

**Stap 3.1 - Start Docker daemon**
```bash
# Check of Docker daemon draait
docker ps

# Als het niet werkt, probeer:
dockerd &

# Of gebruik proot-distro voor container:
pkg install proot-distro
proot-distro install alpine
```

**Stap 3.2 - Configureer Docker in Agent Zero**

Als Docker werkt, behoud in `initialize.py`:
```python
code_exec_docker_enabled = True,
code_exec_ssh_enabled = True,
```

**WAARSCHUWING**: Docker in Termux kan instabiel zijn. Aanbeveling: Gebruik local execution (Docker disabled).

---

### Phase 4: Testen 🧪

**Stap 4.1 - Test CLI**
```bash
cd /data/data/com.termux/files/home/AI-EcoSystem
python run_cli.py
```

**Verwachte output:**
```
Initializing framework...
User message ('e' to leave):
>
```

**Stap 4.2 - Test basis commando**
```
> Hello, can you help me?
```

**Stap 4.3 - Test code execution**
```
> Write a simple Python script that prints "Hello from Agent Zero"
```

**Stap 4.4 - Test met specialized agent prompt**
```
> You are a Code Execution Specialist. Write Python code to list all files in current directory
```

---

### Phase 5: Claude Code Slash Commands Gebruiken 🎮

**Je slash commands zijn al geïnstalleerd!**

In je huidige Claude Code sessie kun je nu gebruiken:

**1. Overzicht van agents:**
```
/agents
```

**2. Master Orchestrator (coördineert alles):**
```
/master

Bouw een Python script dat een CSV file analyseert
```

**3. Code Specialist:**
```
/code

Schrijf een Python script dat de Fibonacci reeks berekent
```

**4. Research Specialist:**
```
/research

Wat is de beste Python library voor async HTTP requests?
```

**5. Web Scraper:**
```
/scrape

URL: https://example.com
Doel: Extraheer alle links
```

**6. Architect (voor complexe ontwerpen):**
```
/architect

Ontwerp een scalable API voor user authentication
```

**7. Orchestrator (voor multi-step workflows):**
```
/orchestrate

Complete workflow:
1. Research beste library
2. Ontwerp architectuur
3. Implementeer code
4. Test alles
```

---

## 🚨 Potentiële Problemen & Oplossingen

### Probleem 1: Package compilatie faalt
**Symptoom:** `error: failed building wheel for faiss-cpu`

**Oplossing:**
```bash
# Skip heavy packages
pip install -r requirements.txt --no-deps
# Installeer alleen essentiële packages handmatig
```

### Probleem 2: Docker werkt niet
**Symptom:** `Cannot connect to Docker daemon`

**Oplossing:**
```python
# In initialize.py:
code_exec_docker_enabled = False,
code_exec_ssh_enabled = False,
```
Code execution zal dan direct in Termux draaien.

### Probleem 3: Memory overflow
**Symptoom:** `MemoryError` of proces crash

**Oplossing:**
```bash
# Gebruik kleinere models
# In initialize.py:
chat_llm = models.get_openai_chat(model_name="gpt-4o-mini", temperature=0)
# OF lokaal klein model:
chat_llm = models.get_ollama_chat(model_name="llama3.2:1b", temperature=0)
```

### Probleem 4: API rate limits
**Symptoom:** `Rate limit exceeded`

**Oplossing:**
```python
# In initialize.py:
rate_limit_requests = 10,  # Verlaag van 30 naar 10
```

---

## 📝 Quick Start Checklist

Volg deze stappen in volgorde:

- [ ] 1. Installeer system dependencies (`pkg install python python-pip git openssh`)
- [ ] 2. Installeer Python packages (`pip install -r requirements.txt`)
- [ ] 3. Maak `.env` bestand met API keys
- [ ] 4. Edit `initialize.py` - disable Docker, kies LLM provider
- [ ] 5. Test run: `python run_cli.py`
- [ ] 6. Test basis interactie in Agent Zero CLI
- [ ] 7. Test code execution in Agent Zero
- [ ] 8. Test Claude Code slash commands (`/agents`, `/code`, etc.)
- [ ] 9. Bouw je eerste agent workflow!

---

## 🎯 Aanbevolen Setup voor Termux

**Minimale Setup (best voor beginnen):**
```python
# initialize.py configuration:
chat_llm = models.get_openai_chat(model_name="gpt-4o-mini", temperature=0)
code_exec_docker_enabled = False
code_exec_ssh_enabled = False
```

**Waarom:**
- `gpt-4o-mini` is snel, goedkoop, en capabel
- Geen Docker = minder complexity, stabieler
- Code draait direct in Termux = sneller

**Advanced Setup (als je wilt experimenteren):**
```python
chat_llm = models.get_ollama_chat(model_name="llama3.2:3b-instruct-fp16", temperature=0)
```
Volledig lokaal, geen API keys nodig, maar vereist Ollama installatie.

---

## 🔗 Nuttige Resources

**Agent Zero Documentatie:**
- README: `/data/data/com.termux/files/home/AI-EcoSystem/README.md`
- Installation docs: `agent-zero/docs/installation/README.md`

**Specialized Agents Docs:**
- Usage guide: `GEBRUIKSAANWIJZING.md`
- Quick start: `prompts/specialized-agents/QUICK_START.md`

**Claude Code Commands:**
- Lijst: `ls .claude/commands/`
- Usage: Type `/agents` in Claude Code

---

## 🚀 Next Steps

1. **Volg de Quick Start Checklist** hierboven
2. **Test eerst Agent Zero CLI** - zorg dat het werkt
3. **Test Claude Code slash commands** - gebruik de specialized agents
4. **Experimenteer** met verschillende workflows

---

## 💡 Pro Tips

1. **Start simpel**: Gebruik OpenAI gpt-4o-mini eerst, experimenteer later
2. **Disable Docker**: Minder hoofdpijn op Termux
3. **Gebruik slash commands**: `/master` is je beste vriend voor complete workflows
4. **Combineer**: Agent Zero CLI + Claude Code = krachtige combo
5. **Itereer**: Build stap voor stap, test veel

---

**Veel succes! 🎉**

Vragen? Check de documentatie of experimenteer - je hebt nu alle tools!
