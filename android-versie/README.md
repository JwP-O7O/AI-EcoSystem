# 🤖 Agent Zero - Android/Termux Edition

**Agent Zero volledig geoptimaliseerd voor Android via Termux**

Deze directory bevat alles wat je nodig hebt om Agent Zero te draaien op je Android telefoon of tablet via Termux.

---

## 📦 Wat zit erin?

```
android-versie/
├── config/
│   ├── initialize_android.py    # Termux-optimized configuratie
│   ├── .env.example             # API keys template
│   └── .env                     # Je API keys (maak dit aan)
├── scripts/
│   ├── setup.sh                 # Installatie script
│   └── start.sh                 # Quick launcher
├── docs/
│   ├── QUICK_START.md           # 10-minuten start guide
│   ├── TROUBLESHOOTING.md       # Problemen oplossen
│   └── EXAMPLES.md              # Praktische voorbeelden
├── run_android_cli.py           # Main launcher
└── requirements-android.txt     # Lightweight dependencies
```

---

## 🚀 Quick Start

**3 commando's om te starten:**

```bash
# 1. Run setup (5 minuten)
bash android-versie/scripts/setup.sh

# 2. Configureer API key
nano android-versie/config/.env

# 3. Start Agent Zero
bash android-versie/scripts/start.sh
```

**Voor gedetailleerde instructies:** `cat android-versie/docs/QUICK_START.md`

---

## ✨ Wat is geoptimaliseerd voor Android?

### 🎯 Lightweight Dependencies
- Geen Docker (direct execution in Termux)
- Geen zware packages (faiss-cpu, unstructured)
- Optionele packages alleen waar nodig
- ARM-compatible alternatieven

### ⚡ Performance Optimized
- Verlaagde memory limiet (20 messages max)
- Kortere tool responses (2000 chars)
- Lagere rate limits (15 req/min)
- Efficiëntere context management

### 🔧 Termux-Specific
- Direct code execution (geen containers)
- Termux-compatible paths
- Android-friendly timeouts
- Mobile-optimized error handling

### 🧠 Model Configuratie
- **Standaard**: Google Gemini (gemini-2.5-flash) ✨
- Alternatief: OpenAI, Anthropic, Groq, Ollama
- Gratis tier: Gemini, Groq
- Lokale optie: Ollama

---

## 📋 Requirements

### Hardware:
- Android 7.0+ (aanbevolen: 10+)
- Minimaal 2GB RAM (aanbevolen: 4GB+)
- 2GB vrije opslag
- Internet verbinding

### Software:
- Termux (F-Droid of GitHub release)
- Python 3.11+ (auto-install via setup)
- API key (OpenAI, Anthropic, Groq, of Ollama lokaal)

---

## 🎯 Use Cases

### Perfect voor:
✅ Mobiele AI assistentie
✅ On-the-go development
✅ Learning & experimentation
✅ Quick prototyping
✅ Remote work scenarios
✅ Offline coding (met Ollama)

### Minder geschikt voor:
❌ Heavy compute tasks
❌ Large file processing
❌ High-concurrent operations
❌ Production deployments

---

## 🔌 Ondersteunde Providers

### Cloud (API key vereist):
- **OpenAI** - gpt-4o-mini, gpt-4o (aanbevolen)
- **Anthropic** - Claude 3.5 Sonnet, Haiku
- **Google** - Gemini 1.5 Flash, Pro
- **Groq** - Llama 3.2, Mixtral (snelste gratis optie)
- **Mistral** - Mistral Small, Large

### Lokaal (gratis, maar vereist Ollama):
- **Ollama** - Llama 3.2, Phi-3, Gemma 2
- Geen API key nodig
- Privacy friendly
- Internet alleen voor downloads

---

## 📖 Documentatie

### Start hier:
1. **QUICK_START.md** - 10-minuten setup guide
2. **TROUBLESHOOTING.md** - Problemen oplossen
3. **EXAMPLES.md** - Praktische voorbeelden

### Dieper duiken:
- `../TERMUX_SETUP_PLAN.md` - Complete setup guide
- `../GEBRUIKSAANWIJZING.md` - Slash commands gebruiken
- `../README.md` - Originele Agent Zero docs

---

## 🎮 Specialized Agents

Deze Android versie werkt perfect met de specialized agents!

**In Claude Code:**
```
/master    - Volledige workflow coördinatie
/code      - Python/JavaScript development
/research  - Online informatie zoeken
/scrape    - Web data extractie
/architect - Systeem ontwerp
/orchestrate - Multi-agent workflows
```

**In Agent Zero CLI:**
Prompt de agent met een rol:
```
> You are a Code Execution Specialist. Write Python code to...
```

---

## ⚙️ Configuratie

### Model Configuratie

**✨ Standaard: Google Gemini**

Deze installatie is geconfigureerd om **altijd Google Gemini** te gebruiken:

```bash
# In android-versie/config/.env:
LLM_PROVIDER=google
GOOGLE_API_KEY=AIzaSyBQXtSC3mopsBJJgvRQI81hQRy877eklGo
```

**Model details:**
- Chat: `gemini-2.5-flash` (snel, gratis tier)
- Embeddings: `models/embedding-001`

**Andere provider kiezen?** Edit `android-versie/config/.env`:
```env
# Voor OpenAI:
LLM_PROVIDER=openai

# Voor Anthropic Claude:
LLM_PROVIDER=anthropic

# Voor Groq:
LLM_PROVIDER=groq

# Voor lokale Ollama:
LLM_PROVIDER=ollama
```

📖 **Meer info**: Zie `android-versie/GEMINI_CONFIG.md`

### API Keys
Maak een kopie van het voorbeeld:
```bash
cp android-versie/config/.env.example android-versie/config/.env
nano android-versie/config/.env
```

---

## 🐛 Troubleshooting

### Snelle fixes:

**Module not found:**
```bash
pip install -r android-versie/requirements-android.txt
```

**Memory errors:**
```python
# In initialize_android.py:
msgs_keep_max=15,
max_tool_response_length=1500,
```

**API errors:**
```bash
# Check .env file
cat android-versie/config/.env
```

**Voor meer:** `cat docs/TROUBLESHOOTING.md`

---

## 🔄 Updates

### Python packages updaten:
```bash
pip install -r android-versie/requirements-android.txt --upgrade
```

### Git pull (als je git gebruikt):
```bash
cd /data/data/com.termux/files/home/AI-EcoSystem
git pull
```

---

## 💡 Best Practices

1. **Start klein** - Gebruik gpt-4o-mini voor testing
2. **Monitor usage** - Check je API dashboard regelmatig
3. **Save logs** - Check `logs/` voor debugging
4. **Backup .env** - Bewaar je API keys veilig
5. **Test lokaal** - Probeer Ollama voor experimenten

---

## 🤝 Contributing

Verbeteringen? Fork en submit een PR!

Interessante use cases? Deel ze in de docs/EXAMPLES.md!

---

## 📜 License

Volgt de Agent Zero licentie - zie hoofdproject README.

---

## 🆘 Support

**Documentatie:**
- Quick Start: `docs/QUICK_START.md`
- Troubleshooting: `docs/TROUBLESHOOTING.md`
- Examples: `docs/EXAMPLES.md`

**Agent Zero Community:**
- Discord: https://discord.gg/B8KZKNsPpj
- GitHub: https://github.com/frdel/agent-zero

---

## 🎉 Klaar om te starten?

```bash
bash android-versie/scripts/setup.sh
```

**Happy coding on Android! 🚀📱**

---

*Versie: 1.0*
*Android/Termux Optimized Edition*
*November 26, 2025*
