# 🤖 Gemini API Configuratie

Deze Agent Zero installatie is nu geconfigureerd om **altijd Google Gemini** te gebruiken.

## ✅ Huidige Configuratie

```bash
LLM_PROVIDER=google
GOOGLE_API_KEY=AIzaSyBQXtSC3mopsBJJgvRQI81hQRy877eklGo
```

### Model Details:
- **Chat Model**: `gemini-2.5-flash`
- **Embedding Model**: `models/embedding-001`
- **Provider**: Google Generative AI

---

## 🔧 Hoe het werkt

De configuratie in `config/initialize_android.py` controleert:

1. **Eerst**: `LLM_PROVIDER` environment variabele (nu: `google`)
2. **Dan**: Aanwezigheid van API keys als LLM_PROVIDER niet is ingesteld

Omdat `LLM_PROVIDER=google` expliciet is ingesteld in `.env`, wordt **altijd Gemini gebruikt**, zelfs als er andere API keys aanwezig zijn.

---

## 🎯 Voordelen van Gemini

- ✅ **Gratis tier** - Genereus gratis gebruik
- ✅ **Snel** - gemini-2.5-flash is geoptimaliseerd voor snelheid
- ✅ **Betrouwbaar** - Stabiele Google infrastructuur
- ✅ **Goed voor mobiel** - Lage latency, efficient

---

## 🔄 Als je een andere provider wilt gebruiken

Edit `android-versie/config/.env`:

```bash
# Voor OpenAI:
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...

# Voor Anthropic Claude:
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-...

# Voor Groq:
LLM_PROVIDER=groq
GROQ_API_KEY=gsk-...

# Voor lokale Ollama:
LLM_PROVIDER=ollama
```

---

## ✅ Verificatie

Test de configuratie:

```bash
cd /data/data/com.termux/files/home/AI-EcoSystem/android-versie
python3 -c "
import sys; sys.path.insert(0, 'config'); sys.path.insert(0, '..')
from initialize_android import get_chat_model
chat = get_chat_model()
print('Model:', type(chat).__name__)
"
```

Expected output: `📱 Provider: Google Gemini (Flash)`

---

## 📝 Startup Output

Wanneer je Agent Zero start, zie je:

```
═══════════════════════════════════════════════════════════
🚀 Agent Zero Starting...
═══════════════════════════════════════════════════════════

🔧 Initializing Android Configuration...
📱 Provider: Google Gemini (Flash)
✓ Ready
```

De "📱 Provider: Google Gemini (Flash)" regel bevestigt dat Gemini wordt gebruikt.

---

## 🆘 Troubleshooting

### Model niet gevonden?
```bash
# Check je .env file:
cat android-versie/config/.env | grep LLM_PROVIDER
cat android-versie/config/.env | grep GOOGLE_API_KEY
```

### API errors?
- Controleer of je API key geldig is: https://makersuite.google.com/app/apikey
- Check quota/limiet in Google AI Studio
- Verify internet connectie

---

**Laatste update**: November 29, 2025
