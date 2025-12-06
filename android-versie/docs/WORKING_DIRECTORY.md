# Agent Zero - Working Directory Support

**Datum:** 28 November 2025
**Feature:** Agent Zero werkt in jouw huidige directory

---

## 🎯 Wat is Dit?

Agent Zero kan nu werken in **elke map** waar je hem start. Hij weet waar hij zich bevindt en kan alleen files in die map lezen en aanpassen.

---

## 📂 Hoe Werkt Het?

### Start Agent Zero

Simpel `agent0` typen in welke map dan ook:

```bash
cd ~/mijn-project
agent0
```

Agent Zero ziet dan:
```
============================================
🚀 Starting Agent Zero - Android/Termux Edition...
============================================
📂 Working Directory: /data/data/com.termux/files/home/mijn-project
============================================

🤖 Agent Zero - Android/Termux Edition
📱 Running in Termux optimized mode
📂 Working in: /data/data/com.termux/files/home/mijn-project
Type 'e' to exit, or start chatting!
```

### Wat Kan Agent Zero Doen?

In de working directory kan Agent Zero:

✅ **Files lezen**
```
> Lees README.md
> Wat staat er in config.json?
```

✅ **Code uitvoeren**
```
> Run python script.py
> Voer ls -la uit
```

✅ **Files aanpassen**
```
> Wijzig line 42 in app.py naar...
> Maak een nieuwe file test.txt met...
```

✅ **Projecten analyseren**
```
> Analyseer deze codebase
> Zoek alle TODO's in Python files
> Maak een overzicht van alle functies
```

---

## 🔧 Technische Details

### Hoe Wordt De Directory Doorgegeven?

1. **Wrapper script** (`agent0_wrapper.sh`):
   - Bewaard huidige directory met `pwd`
   - Export als `AGENT_WORK_DIR` environment variable
   - Start Agent Zero vanuit zijn eigen directory
   - Keert terug naar work directory na exit

2. **run_android_cli.py**:
   - Leest `AGENT_WORK_DIR` of gebruikt `os.getcwd()`
   - Slaat op in agent's data: `context.agent0.set_data("work_dir", work_dir)`
   - Toont working directory in welcome message

3. **code_execution_tool.py**:
   - Haalt work_dir op: `work_dir = self.agent.get_data("work_dir")`
   - Wijzigt CWD voor elke command: `os.chdir(work_dir)`
   - Alle terminal commands draaien in correct directory

### Code Changes

**File:** `android-versie/agent0_wrapper.sh` (NEW)
```bash
#!/data/data/com.termux/files/usr/bin/bash
WORK_DIR="$(pwd)"
export AGENT_WORK_DIR="$WORK_DIR"
cd "$HOME/AI-EcoSystem"
python android-versie/run_android_cli.py
cd "$WORK_DIR"
```

**File:** `android-versie/run_android_cli.py`
```python
# Line 179: Get working directory
work_dir = os.environ.get('AGENT_WORK_DIR', os.getcwd())

# Line 201: Store in agent data
context.agent0.set_data("work_dir", work_dir)

# Line 37: Show in chat welcome
work_dir = context.agent0.get_data("work_dir") or os.getcwd()
PrintStyle(font_color="green").print(f"📂 Working in: {work_dir}")
```

**File:** `python/tools/code_execution_tool.py`
```python
# Lines 27-31: Change to work directory
import os
work_dir = self.agent.get_data("work_dir")
if work_dir and os.path.exists(work_dir):
    os.chdir(work_dir)
```

---

## 🚀 Voorbeelden

### Voorbeeld 1: Project Analyseren

```bash
cd ~/mijn-python-project
agent0
```

```
> Analyseer deze directory en vertel me wat dit project doet
```

Agent Zero zal:
- `ls` uitvoeren in ~/mijn-python-project
- Python files lezen
- Project structuur analyseren
- Uitleg geven

### Voorbeeld 2: Code Wijzigen

```bash
cd ~/website
agent0
```

```
> Voeg een nieuwe functie toe aan index.html die een knop maakt
```

Agent Zero zal:
- index.html lezen in ~/website
- Code wijziging maken
- File opslaan in ~/website
- Wijziging verifiëren

### Voorbeeld 3: Scripts Uitvoeren

```bash
cd ~/scripts
agent0
```

```
> Run cleanup.sh en vertel me wat het doet
```

Agent Zero zal:
- chmod +x cleanup.sh (if needed)
- ./cleanup.sh uitvoeren vanuit ~/scripts
- Output tonen
- Uitleggen wat script deed

---

## ⚠️ Belangrijke Notities

### Veiligheid

🔒 Agent Zero heeft **volledige toegang** tot de working directory waar je hem start.

- ✅ **Gebruik in eigen projecten**
- ⚠️ **Wees voorzichtig in system directories**
- 🚫 **NOOIT in /** (root) starten
- 🚫 **NOOIT in system directories** zoals /system, /etc

### Best Practices

1. **Start altijd in project directory:**
   ```bash
   cd ~/mijn-project
   agent0
   ```

2. **Niet in parent directories:**
   ```bash
   # NIET dit:
   cd ~
   agent0  # Heeft toegang tot alles in home!

   # WEL dit:
   cd ~/specific-project
   agent0  # Alleen toegang tot specific-project
   ```

3. **Verify working directory:**
   Kijk altijd even of Agent Zero in de juiste map start (zie welcome message)

---

## 🔄 Oude vs Nieuwe Gedrag

### VOOR Deze Update

```bash
agent0
```
- Agent Zero werkt altijd in ~/AI-EcoSystem
- Kan alleen files daar lezen/wijzigen
- Moet absolute paths gebruiken voor andere directories

### NA Deze Update

```bash
cd /any/directory
agent0
```
- Agent Zero werkt in `/any/directory`
- Kan direct files in die directory lezen/wijzigen
- Relatieve paths werken correct

---

## 🆘 Troubleshooting

### "Agent Zero kan mijn file niet vinden"

**Check working directory:**
```
> Wat is mijn huidige directory?
> Run pwd
```

**Oplossing:**
- Exit Agent Zero (type `e`)
- `cd` naar correcte directory
- Start `agent0` opnieuw

### "Wijzigingen worden op verkeerde plek opgeslagen"

**Verify waar Agent Zero denkt dat hij is:**
Kijk naar de welcome message - daar staat de working directory.

**Oplossing:**
- Type `e` om te stoppen
- Verify met `pwd` dat je in de juiste directory bent
- Start `agent0` opnieuw

### "Permission denied bij code execution"

Agent Zero probeert iets te draaien waar hij geen toegang toe heeft.

**Check:**
```bash
ls -la  # Check file permissions
```

**Oplossing:**
```bash
chmod +x script.sh  # Maak executable
```

---

## 📝 Aliases

Na de update zijn er nieuwe aliases:

```bash
# Start Agent Zero in huidige directory (NIEUWE GEDRAG)
agent0

# Same, alternative naam
agent-zero

# Oude agent0-here is nu overbodig
# (agent0 doet nu automatisch hetzelfde)
```

---

## ✅ Checklist Voor Gebruik

Voordat je Agent Zero start:

- [ ] Ben ik in de juiste directory? (`pwd`)
- [ ] Is het veilig voor Agent Zero om hier te werken?
- [ ] Wil ik echt dat Agent Zero files hier kan wijzigen?
- [ ] Heb ik een backup? (altijd goed idee!)

Als alle antwoorden "ja" zijn → `agent0` 🚀

---

## 🎊 Conclusie

Agent Zero is nu een **context-aware** assistant die:

1. ✅ Weet waar hij zich bevindt
2. ✅ Werkt in jouw project directory
3. ✅ Kan direct files lezen en wijzigen
4. ✅ Terminal commands in correct directory uitvoert
5. ✅ Flexibel is - start hem waar je maar wilt!

**Start Agent Zero waar je hem nodig hebt!**

```bash
cd ~/jouw-project
agent0
```

*Laatste update: 28 November 2025*
