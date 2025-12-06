# 🚀 Agent Zero - Android/Termux Quick Start

**Welkom bij de Android/Termux versie van Agent Zero!**

Deze guide brengt je van installatie naar je eerste AI agent in minder dan 10 minuten.

---

## 📋 Wat je nodig hebt

- ✅ Android telefoon/tablet
- ✅ Termux app geïnstalleerd ([F-Droid](https://f-droid.org/packages/com.termux/) of [GitHub](https://github.com/termux/termux-app/releases))
- ✅ Minimaal 2GB vrije ruimte
- ✅ Internet connectie
- ✅ Een API key (OpenAI, Anthropic, of Groq aanbevolen)

---

## ⚡ Snelle Installatie (5 minuten)

### Stap 1: Run Setup Script

```bash
cd /data/data/com.termux/files/home/AI-EcoSystem
bash android-versie/scripts/setup.sh
```

Dit script installeert:
- System dependencies (Python, git, etc.)
- Python packages (AI libraries, web framework, etc.)
- Directory structuur
- Configuration templates

**Dit duurt 3-5 minuten. Pak een kopje koffie! ☕**

---

### Stap 2: Configureer API Key

```bash
# Kopieer example naar .env
cp android-versie/config/.env.example android-versie/config/.env

# Edit met nano
nano android-versie/config/.env
```

**Minimaal vereist - kies één:**

**Optie A - OpenAI (aanbevolen):**
```env
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx
```
[Get key hier](https://platform.openai.com/api-keys)

**Optie B - Anthropic Claude:**
```env
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxx
```
[Get key hier](https://console.anthropic.com/)

**Optie C - Groq (gratis tier):**
```env
GROQ_API_KEY=gsk_xxxxxxxxxxxxx
```
[Get key hier](https://console.groq.com/keys)

**Save met:** `Ctrl+X`, dan `Y`, dan `Enter`

---

### Stap 3: Start Agent Zero! 🎉

```bash
# Optie A - Direct
python android-versie/run_android_cli.py

# Optie B - Via launcher
bash android-versie/scripts/start.sh
```

**Je zou dit moeten zien:**
```
============================================================
🤖 Agent Zero - Android/Termux Edition
============================================================
📱 Running in Termux optimized mode
Type 'e' to exit, or start chatting!

User message ('e' to leave):
>
```

---

## 🎮 Eerste Stappen

### Test 1: Basis Conversatie
```
> Hello! Who are you?
```

### Test 2: Code Execution
```
> Write a Python script that prints "Hello from Agent Zero on Android!"
```

### Test 3: Web Search
```
> What's the weather like today? (search online)
```

### Test 4: File Operations
```
> Create a file called test.txt with the content "Agent Zero works!"
```

---

## 🎯 Specialized Agents Gebruiken

Deze Android versie werkt naadloos met de slash commands!

### In Agent Zero CLI:

**Prompt de agent met een rol:**
```
> You are a Code Execution Specialist. Write Python code to list all files in the current directory.
```

### In Claude Code:

**Gebruik slash commands:**
```
/master

Analyseer mijn Android project en geef suggesties voor verbetering
```

```
/code

Schrijf een Python script dat mijn Termux environment info print
```

```
/research

Wat zijn de beste Python libraries voor mobiele development?
```

---

## 🔧 Configuratie Aanpassen

### Model Wisselen

Edit `android-versie/config/initialize_android.py`:

```python
# Van OpenAI naar Claude:
# chat_llm = models.get_openai_chat(model_name="gpt-4o-mini", temperature=0)
chat_llm = models.get_anthropic_chat(model_name="claude-3-5-sonnet-20240620", temperature=0)
```

### Geheugen Limiet Verlagen

Als je memory errors krijgt:

```python
# In initialize_android.py:
msgs_keep_max=15,  # Verlaag van 20 naar 15
max_tool_response_length=1500,  # Verlaag van 2000 naar 1500
```

### Rate Limits Aanpassen

```python
# In initialize_android.py:
rate_limit_requests=10,  # Verlaag van 15 naar 10
rate_limit_seconds=120,  # Verhoog van 60 naar 120
```

---

## 🐛 Problemen Oplossen

### Probleem: "Module not found"

**Oplossing:**
```bash
pip install -r android-versie/requirements-android.txt
```

### Probleem: "API key not found"

**Oplossing:**
1. Check of `.env` bestaat: `ls android-versie/config/.env`
2. Check of API key correct is: `cat android-versie/config/.env`
3. Herstart Agent Zero

### Probleem: "Memory Error"

**Oplossing:**
- Verlaag `msgs_keep_max` in `initialize_android.py`
- Close andere apps op je telefoon
- Gebruik een kleiner model (gpt-4o-mini)

### Probleem: "Rate limit exceeded"

**Oplossing:**
- Verlaag `rate_limit_requests` in `initialize_android.py`
- Wacht even en probeer opnieuw
- Check je API plan/quota

---

## 📚 Meer Leren

### Documentatie:
```bash
# Troubleshooting guide
cat android-versie/docs/TROUBLESHOOTING.md

# Voorbeelden
cat android-versie/docs/EXAMPLES.md

# Volledige setup guide
cat TERMUX_SETUP_PLAN.md
```

### Claude Code Slash Commands:
```bash
# Overzicht van alle agents
cat .claude/commands/agents.md

# Gebruiksaanwijzing
cat GEBRUIKSAANWIJZING.md
```

---

## 💡 Pro Tips

1. **Start simpel** - Test eerst met basis conversaties
2. **Gebruik kleinere models** - `gpt-4o-mini` is snel en goedkoop
3. **Monitor je usage** - Check je API usage in je provider dashboard
4. **Save je werk** - Agent Zero slaat logs op in `logs/`
5. **Experiment** - Probeer verschillende prompts en rollen

---

## 🎯 Handige Commands

```bash
# Start Agent Zero
bash android-versie/scripts/start.sh

# Check logs
ls -lh logs/

# Edit configuratie
nano android-versie/config/initialize_android.py

# Edit API keys
nano android-versie/config/.env

# Update packages
pip install -r android-versie/requirements-android.txt --upgrade

# Check Python packages
pip list | grep -E "(anthropic|openai|langchain)"
```

---

## 🆘 Hulp Nodig?

1. **Troubleshooting Guide:** `android-versie/docs/TROUBLESHOOTING.md`
2. **Examples:** `android-versie/docs/EXAMPLES.md`
3. **Main README:** `README.md`
4. **Agent Zero Docs:** `agent-zero/docs/`

---

## 🎉 Je bent klaar!

Agent Zero draait nu op je Android toestel via Termux!

**Next steps:**
- Experimenteer met verschillende taken
- Probeer de specialized agents (slash commands)
- Bouw je eigen workflows
- Deel je ervaring!

**Happy building! 🚀**

---

*Versie: 1.0 - November 26, 2025*
*Android/Termux Optimized Edition*
