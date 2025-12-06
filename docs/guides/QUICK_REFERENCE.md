# 🚀 Agent Zero - Quick Reference

**Android/Termux Edition**

---

## ⚡ Snelle Commando's

### Start Agent Zero:
```bash
python android-versie/run_android_cli.py
```

### Exit Agent Zero:
Type `e` in de chat

---

## 📝 Configuratie Files

| File | Doel |
|------|------|
| `android-versie/config/initialize_android.py` | Model configuratie |
| `android-versie/config/.env` | API keys |
| `android-versie/run_android_cli.py` | Main launcher |

---

## 🔧 Snelle Fixes

### Reinstall packages:
```bash
pip install -r android-versie/requirements-android.txt
```

### Check API key:
```bash
cat android-versie/config/.env | grep GOOGLE_API_KEY
```

### Test configuration:
```bash
python -c "from android_versie.config.initialize_android import initialize; initialize()"
```

---

## 🎯 Quick Tests

### Test 1: Basic
```
> Hello! Write a Python script that prints "Hello Android!"
```

### Test 2: Files
```
> Create a file notes.txt with "My first note"
```

### Test 3: Code
```
> Write a Python script that fetches data from https://api.github.com/users/frdel
```

---

## 🔑 API Keys

### Google (Active):
```bash
# In android-versie/config/.env:
GOOGLE_API_KEY=your-key-here
```

Get key: https://makersuite.google.com/app/apikey

### OpenAI (Optional):
```bash
OPENAI_API_KEY=your-key-here
```

Get key: https://platform.openai.com/api-keys

### Anthropic (Optional):
```bash
ANTHROPIC_API_KEY=your-key-here
```

Get key: https://console.anthropic.com/

---

## 📚 Documentatie

| Document | Command |
|----------|---------|
| Setup compleet | `cat AGENT_ZERO_ANDROID_SETUP_COMPLEET.md` |
| Examples | `cat android-versie/docs/EXAMPLES.md` |
| Troubleshooting | `cat android-versie/docs/TROUBLESHOOTING.md` |

---

## 💡 Model Wisselen

### In `initialize_android.py`:

**Google (current):**
```python
chat_llm = models.get_google_chat(model_name="gemini-1.5-flash", temperature=0)
```

**OpenAI:**
```python
chat_llm = models.get_openai_chat(model_name="gpt-4o-mini", temperature=0)
```

**Anthropic:**
```python
chat_llm = models.get_anthropic_chat(model_name="claude-3-5-sonnet-20240620", temperature=0)
```

---

## 🆘 Help

### Memory issues:
Verlaag `msgs_keep_max` en `max_tool_response_length` in config

### Rate limit:
Verlaag `rate_limit_requests` in config

### Import errors:
```bash
pip install --upgrade langchain langchain-google-genai
```

---

## 📊 Status Check

```bash
# Check Python
python --version

# Check packages
pip list | grep langchain

# Check Agent Zero files
ls -la android-versie/

# Check config
cat android-versie/config/.env
```

---

**Quick Start:**
```bash
python android-versie/run_android_cli.py
```

**Exit:** Type `e`

**Help:** Check `AGENT_ZERO_ANDROID_SETUP_COMPLEET.md`

---

*26 November 2025*
