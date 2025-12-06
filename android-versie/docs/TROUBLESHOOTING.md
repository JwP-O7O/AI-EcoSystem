# 🔧 Troubleshooting Guide - Agent Zero Android

Veelvoorkomende problemen en oplossingen voor Agent Zero op Android/Termux.

---

## 📱 Installatie Problemen

### Probleem: "pkg: command not found"

**Oorzaak:** Je bent niet in Termux

**Oplossing:**
1. Open de Termux app
2. Run commando's daar, niet in andere terminals

---

### Probleem: "Permission denied" bij setup.sh

**Oorzaak:** Script is niet executable

**Oplossing:**
```bash
chmod +x android-versie/scripts/setup.sh
bash android-versie/scripts/setup.sh
```

---

### Probleem: Package installatie faalt met "ERROR: Failed building wheel"

**Oorzaak:** Package heeft C dependencies die moeilijk te compileren zijn op ARM

**Oplossing A - Skip het package:**
```bash
# Installeer rest zonder problematic package
pip install -r android-versie/requirements-android.txt --no-deps
pip install anthropic openai langchain-anthropic langchain-openai flask beautifulsoup4
```

**Oplossing B - Install build tools:**
```bash
pkg install clang rust binutils
pip install -r android-versie/requirements-android.txt
```

**Oplossing C - Gebruik alternatieven:**
```python
# In initialize_android.py:
# Skip faiss-cpu, gebruik in-memory alleen
# Skip unstructured, doe geen PDF parsing
```

---

## 🔑 API Key Problemen

### Probleem: "No API key found" of "Invalid API key"

**Diagnose:**
```bash
# Check of .env bestaat
ls -la android-versie/config/.env

# Check inhoud
cat android-versie/config/.env
```

**Oplossing:**

**Stap 1 - Maak .env als die niet bestaat:**
```bash
cp android-versie/config/.env.example android-versie/config/.env
```

**Stap 2 - Edit en voeg key toe:**
```bash
nano android-versie/config/.env
```

**Stap 3 - Verifieer format:**
```env
# Correct:
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxx

# Fout (geen spaties, geen quotes):
OPENAI_API_KEY = "sk-proj-xxxxxxxxxxxx"  # FOUT!
```

**Stap 4 - Test:**
```python
python -c "import os; from dotenv import load_dotenv; load_dotenv('android-versie/config/.env'); print(os.getenv('OPENAI_API_KEY'))"
```

---

### Probleem: "Rate limit exceeded"

**Oorzaak:** Te veel requests naar API

**Oplossing A - Vertraag requests:**
```python
# In initialize_android.py:
rate_limit_requests=5,  # Verlaag van 15 naar 5
rate_limit_seconds=120,  # Verhoog van 60 naar 120
```

**Oplossing B - Check je quota:**
- OpenAI: https://platform.openai.com/usage
- Anthropic: https://console.anthropic.com/settings/usage
- Groq: https://console.groq.com/settings/limits

**Oplossing C - Wacht en retry:**
```bash
# Wacht 1 minuut en probeer opnieuw
```

---

## 💾 Memory & Performance Problemen

### Probleem: "MemoryError" of app crash

**Oorzaak:** Android heeft beperkt geheugen

**Oplossing 1 - Verlaag message history:**
```python
# In initialize_android.py:
msgs_keep_max=10,  # Verlaag van 20 naar 10
msgs_keep_start=3,
msgs_keep_end=5,
```

**Oplossing 2 - Verkort tool responses:**
```python
max_tool_response_length=1000,  # Verlaag van 2000 naar 1000
```

**Oplossing 3 - Gebruik kleiner model:**
```python
# Van:
chat_llm = models.get_openai_chat(model_name="gpt-4o", temperature=0)

# Naar:
chat_llm = models.get_openai_chat(model_name="gpt-4o-mini", temperature=0)
```

**Oplossing 4 - Close andere apps:**
- Sluit browser
- Sluit andere grote apps
- Herstart Termux

---

### Probleem: Agent is erg traag

**Diagnose:**
- Check internet speed
- Check CPU usage
- Check welk model je gebruikt

**Oplossing 1 - Sneller model:**
```python
# Groq is supersnel (gratis):
chat_llm = models.get_groq_chat(model_name="llama-3.2-90b-text-preview", temperature=0)
```

**Oplossing 2 - Lokaal klein model:**
```bash
# Install Ollama eerst
pkg install ollama

# Start Ollama
ollama serve &

# Pull klein model
ollama pull llama3.2:1b

# In initialize_android.py:
chat_llm = models.get_ollama_chat(model_name="llama3.2:1b", temperature=0)
```

---

## 🐍 Python Problemen

### Probleem: "ModuleNotFoundError: No module named 'anthropic'"

**Oplossing:**
```bash
pip install anthropic
# Of
pip install -r android-versie/requirements-android.txt
```

---

### Probleem: "ImportError: cannot import name 'AgentContext'"

**Oorzaak:** Agent Zero core files niet toegankelijk

**Oplossing:**
```bash
# Check of je in juiste directory bent
pwd
# Moet zijn: /data/data/com.termux/files/home/AI-EcoSystem

# Check of agent.py bestaat
ls agent.py

# Als niet, clone repo opnieuw of check paths
```

---

### Probleem: "SyntaxError" of "IndentationError"

**Oorzaak:** Python versie of file corrupt

**Diagnose:**
```bash
python --version  # Moet 3.11+ zijn
```

**Oplossing:**
```bash
# Update Python
pkg upgrade python

# Check file niet corrupt is
python -m py_compile android-versie/run_android_cli.py
```

---

## 🔧 Code Execution Problemen

### Probleem: "Permission denied" bij code execution

**Oplossing:**
```bash
# Geef permissies aan work directory
chmod -R 755 work_dir/

# Of maak opnieuw aan
rm -rf work_dir
mkdir work_dir
```

---

### Probleem: Code wordt niet uitgevoerd

**Diagnose:**
```python
# Test Python execution
python -c "print('Hello from Termux')"
```

**Oplossing:**
```python
# In initialize_android.py, check:
code_exec_docker_enabled=False,  # Moet False zijn!
code_exec_ssh_enabled=False,     # Moet False zijn!
```

---

### Probleem: "Docker daemon not running"

**Oorzaak:** Docker is enabled maar werkt niet goed in Termux

**Oplossing:**
```python
# In initialize_android.py:
code_exec_docker_enabled=False,
code_exec_ssh_enabled=False,
```

Docker in Termux is niet nodig en vaak instabiel. We gebruiken direct execution.

---

## 🌐 Network Problemen

### Probleem: "Connection timeout" of "Network error"

**Diagnose:**
```bash
# Test internet
ping -c 3 google.com

# Test API endpoint
curl https://api.openai.com/v1/models -H "Authorization: Bearer YOUR_KEY"
```

**Oplossing:**
- Check WiFi/mobile data
- Check VPN niet blokkeert API
- Check firewall settings
- Probeer ander netwerk

---

### Probleem: "SSL Certificate error"

**Oplossing:**
```bash
# Update certificates
pkg install ca-certificates

# Update OpenSSL
pkg install openssl

# Reinstall Python requests
pip install --upgrade requests certifi
```

---

## 📝 Logging & Debugging

### Debug Mode Aanzetten

**Edit initialize_android.py en voeg toe:**
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

**Of set environment variable:**
```bash
export LOG_LEVEL=DEBUG
python android-versie/run_android_cli.py
```

---

### Check Logs

```bash
# Lijst logs
ls -lh logs/

# Bekijk laatste log
cat logs/$(ls -t logs/ | head -1)

# Monitor live
tail -f logs/$(ls -t logs/ | head -1)
```

---

## 🔄 Reset & Clean Install

### Soft Reset (behoud .env)

```bash
# Reinstall packages
pip install -r android-versie/requirements-android.txt --force-reinstall --no-cache

# Clear work directory
rm -rf work_dir/*

# Clear logs
rm -rf logs/*

# Restart
bash android-versie/scripts/start.sh
```

---

### Hard Reset (clean slate)

```bash
cd /data/data/com.termux/files/home

# Backup .env
cp AI-EcoSystem/android-versie/config/.env ~/backup.env

# Remove and re-clone
rm -rf AI-EcoSystem
git clone [repo-url] AI-EcoSystem
cd AI-EcoSystem

# Restore .env
cp ~/backup.env android-versie/config/.env

# Run setup
bash android-versie/scripts/setup.sh
```

---

## 🆘 Nog Steeds Problemen?

### Collect Debug Info

```bash
# System info
uname -a
python --version
pip --version

# Package versions
pip list | grep -E "(anthropic|openai|langchain)"

# Check files
ls -la android-versie/
ls -la android-versie/config/

# Check permissions
ls -la work_dir/
```

---

### Report Issue

Als je een bug vindt, maak een issue met:
1. Error message (volledig)
2. System info (hierboven)
3. Stappen om te reproduceren
4. Config (zonder API keys!)

---

## 💡 Preventieve Tips

1. **Keep packages updated:**
   ```bash
   pkg upgrade
   pip install -r android-versie/requirements-android.txt --upgrade
   ```

2. **Monitor geheugen:**
   ```bash
   free -h
   ```

3. **Backup regelmatig:**
   ```bash
   cp android-versie/config/.env ~/backup_env_$(date +%Y%m%d)
   ```

4. **Test na changes:**
   ```bash
   python -c "from android_versie.config.initialize_android import initialize; initialize()"
   ```

5. **Read logs:**
   Altijd check logs/ na errors

---

## 📚 Meer Resources

- **Quick Start:** `android-versie/docs/QUICK_START.md`
- **Examples:** `android-versie/docs/EXAMPLES.md`
- **Main README:** `android-versie/README.md`
- **Agent Zero Docs:** `agent-zero/docs/`

---

**Nog vragen? Check de community:**
- Discord: https://discord.gg/B8KZKNsPpj
- GitHub Issues: https://github.com/frdel/agent-zero/issues

---

*Happy troubleshooting! 🔧*
