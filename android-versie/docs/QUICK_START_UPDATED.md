# 🚀 Agent Zero - Quick Start (Updated 28 Nov 2025)

## Snelle Start

```bash
# Ga naar jouw project directory
cd ~/mijn-project

# Start Agent Zero
agent0
```

Dat is alles! Agent Zero werkt nu in `~/mijn-project` 🎉

---

## ✨ Wat is Er Nieuw? (28 Nov 2025)

### 1. ✅ Working Directory Support
Agent Zero werkt nu in de directory waar je hem start!

**Voor:**
```bash
agent0  # Werkt altijd in ~/AI-EcoSystem
```

**Nu:**
```bash
cd ~/any/directory
agent0  # Werkt in ~/any/directory!
```

### 2. ✅ Paramiko Fix
Code execution werkt nu volledig:
- Terminal commands
- Python scripts
- File operations

**Oplossing:**
```bash
pkg install libsodium -y
SODIUM_INSTALL=system pip install pynacl --no-binary :all:
pip install paramiko
```

---

## 📂 Basis Gebruik

### Start Agent Zero

```bash
cd ~/jouw-project
agent0
```

Je ziet:
```
============================================
🚀 Starting Agent Zero - Android/Termux Edition...
============================================
📂 Working Directory: /data/data/com.termux/files/home/jouw-project
============================================

🤖 Agent Zero - Android/Termux Edition
📱 Running in Termux optimized mode
📂 Working in: /data/data/com.termux/files/home/jouw-project
Type 'e' to exit, or start chatting!
```

### Chat Met Agent Zero

```
> Wat staat er in deze directory?
> Lees README.md
> Run python script.py
> Maak een nieuwe file met...
```

### Stop Agent Zero

```
> e
```

Of: `Ctrl+C`

---

## 💡 Handige Commando's

### Analyseer Project
```
> Analyseer deze directory en vertel me wat dit project doet
> Zoek alle Python files en maak een overzicht
> Zijn er TODO's in de code?
```

### Files Lezen
```
> Lees config.json
> Wat staat er in requirements.txt?
> Toon me de eerste 20 regels van app.py
```

### Code Uitvoeren
```
> Run python test.py
> Voer ls -la uit
> Test of script.sh werkt
```

### Files Wijzigen
```
> Voeg een nieuwe functie toe aan utils.py
> Fix de bug op regel 42 in main.py
> Maak een nieuwe file helpers.py met...
```

---

## ⚙️ Configuratie

### API Keys

Edit `.env` file:
```bash
nano ~/AI-EcoSystem/android-versie/config/.env
```

Voeg toe:
```bash
GOOGLE_API_KEY=your-key-here
```

Get key: https://makersuite.google.com/app/apikey

### Model Wijzigen

Edit config:
```bash
nano ~/AI-EcoSystem/android-versie/config/initialize_android.py
```

Kies je model (regel 57):
```python
# Google Gemini (huidige)
chat_llm = models.get_google_chat(model_name="gemini-2.5-flash", temperature=0)

# Of OpenAI:
# chat_llm = models.get_openai_chat(model_name="gpt-4o-mini", temperature=0)

# Of Anthropic:
# chat_llm = models.get_anthropic_chat(model_name="claude-3-5-sonnet-20240620", temperature=0)
```

---

## 🔧 Troubleshooting

### "ModuleNotFoundError: No module named 'paramiko'"

Opgelost met:
```bash
pkg install libsodium -y
SODIUM_INSTALL=system pip install pynacl --no-binary :all:
pip install paramiko
```

Zie: `android-versie/docs/PARAMIKO_FIX.md`

### "Agent Zero werkt niet in mijn directory"

Check:
1. Herlaad aliases: `source ~/.bashrc`
2. Verify wrapper: `ls -la ~/AI-EcoSystem/android-versie/agent0_wrapper.sh`
3. Check permissions: `chmod +x ~/AI-EcoSystem/android-versie/agent0_wrapper.sh`

### "API key error"

Check `.env`:
```bash
cat ~/AI-EcoSystem/android-versie/config/.env
```

Moet bevatten:
```
GOOGLE_API_KEY=your-actual-key-here
```

---

## 📚 Meer Documentatie

- **Paramiko Fix:** `android-versie/docs/PARAMIKO_FIX.md`
- **Working Directory:** `android-versie/docs/WORKING_DIRECTORY.md`
- **Volledige Setup:** `AGENT_ZERO_ANDROID_SETUP_COMPLEET.md`
- **Wijzigingen:** `WIJZIGINGEN_OVERZICHT.md`
- **Quick Reference:** `QUICK_REFERENCE.md`

---

## ✅ Status Check

Alles werkt? Check:

```bash
# 1. Paramiko installed?
python -c "import paramiko; print('✅ Paramiko OK')"

# 2. Agent Zero files?
ls -la ~/AI-EcoSystem/android-versie/

# 3. Wrapper executable?
ls -la ~/AI-EcoSystem/android-versie/agent0_wrapper.sh

# 4. Aliases loaded?
alias | grep agent0
```

Als alle checks ✅ zijn → Agent Zero is klaar! 🎉

---

## 🎯 Voorbeelden

### Voorbeeld 1: Python Project

```bash
cd ~/python-project
agent0
```

```
> Analyseer de code structure
> Run alle tests
> Zoek naar bugs
> Documenteer de functies
```

### Voorbeeld 2: Website

```bash
cd ~/website
agent0
```

```
> Maak een nieuwe pagina about.html
> Fix CSS issues in style.css
> Test of JavaScript werkt
> Optimize images
```

### Voorbeeld 3: Scripts

```bash
cd ~/scripts
agent0
```

```
> Run backup.sh en vertel me wat het doet
> Maak een nieuwe script voor...
> Debug waarom script faalt
```

---

## 🔒 Veiligheid

⚠️ **Belangrijk:**

- Agent Zero heeft **volledige toegang** tot working directory
- Start ALLEEN in directories waar je dit wilt
- NOOIT in system directories (`/`, `/system`, `/etc`)
- Maak altijd backups van belangrijke files

✅ **Veilig:**
```bash
cd ~/mijn-project
agent0
```

🚫 **NIET veilig:**
```bash
cd /
agent0  # NOOIT DOEN!
```

---

## 🆘 Hulp Nodig?

1. **Check documentatie:** `ls ~/AI-EcoSystem/android-versie/docs/`
2. **Restart terminal:** Sluit en heropen Termux
3. **Reload bashrc:** `source ~/.bashrc`
4. **Check logs:** Agent Zero toont errors in terminal

---

## 🎊 Klaar!

Agent Zero is volledig operationeel!

```bash
cd ~/jouw-project
agent0
```

**Veel plezier! 🚀**

*Laatste update: 28 November 2025*
