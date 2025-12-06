# Google Drive - Quick Start

**Klaar om te gebruiken! Google Drive is geïntegreerd met Agent Zero.**

---

## ⚡ Snelste Start (3 stappen)

### 1. Check of rclone geïnstalleerd is
```bash
rclone version
```
✅ Al geïnstalleerd op jouw systeem!

### 2. Configureer Google Drive (EENMALIG)
```bash
rclone config
```

**Volg deze stappen:**
```
n) New remote
name> gdrive
Storage> drive (kies het nummer voor Google Drive)
client_id> [druk ENTER]
client_secret> [druk ENTER]
scope> 1 (Full access)
root_folder_id> [druk ENTER]
service_account_file> [druk ENTER]
Edit advanced config? n
Use auto config? n  ← BELANGRIJK!

Je krijgt een URL te zien:
1. Kopieer de URL
2. Open in browser (op telefoon of PC)
3. Login met Google account
4. Geef toegang
5. Kopieer verificatie code
6. Plak terug in Termux
7. Druk ENTER

Configure as team drive? n
Yes this is OK? y
```

### 3. Test Het!
```bash
rclone ls gdrive:
```

Zie je je Google Drive bestanden? **KLAAR!** ✅

---

## 🚀 3 Manieren Om Te Gebruiken

### Methode 1: Via Agent Zero (Makkelijkst!)

**Gewoon vragen in natuurlijke taal:**

```
User: "List all files in my Google Drive"

User: "Upload /sdcard/data.csv to Google Drive backups folder"

User: "Download the latest report from Google Drive"

User: "Search for files containing 'invoice' in Google Drive"

User: "Check my Google Drive storage"
```

Agent Zero gebruikt automatisch de `google_drive` tool! 🎉

---

### Methode 2: Helper Script (Snel & Direct)

```bash
# List bestanden
python tools/gdrive.py list

# List specifieke folder
python tools/gdrive.py list backups

# Upload bestand
python tools/gdrive.py upload /sdcard/photo.jpg photos

# Download bestand
python tools/gdrive.py download reports/summary.pdf

# Search
python tools/gdrive.py search invoice

# Storage info
python tools/gdrive.py info

# Help
python tools/gdrive.py help
```

---

### Methode 3: Direct rclone (Voor Experts)

```bash
# List
rclone ls gdrive:

# Upload
rclone copy /sdcard/file.txt gdrive:/backups/

# Download
rclone copy gdrive:/file.txt /sdcard/Download/

# Sync (let op: verwijdert bestanden!)
rclone sync /sdcard/docs gdrive:/docs-backup
```

---

## 💡 Praktische Voorbeelden

### Backup Agent Zero Memory

**Via Agent Zero:**
```
"Backup my Agent Zero memory database to Google Drive"
```

**Via script:**
```bash
python tools/gdrive.py upload ~/AI-EcoSystem/memory.db backups/agent-zero
```

---

### Download Dataset voor Analyse

**Via Agent Zero:**
```
"Download sales_data.csv from my Google Drive and analyze it"
```

Agent doet:
1. Download van Google Drive
2. Analyseer met Python
3. Rapporteer resultaten

---

### Dagelijkse Backup Automatiseren

**Via Agent Zero:**
```
"Create a scheduled task to backup my work directory to Google Drive every day at 2 AM"
```

Agent gebruikt `task_scheduler` + `google_drive` tools!

---

### Upload met Notificatie

**Via script:**
```bash
python tools/gdrive.py upload /sdcard/report.pdf reports
```

Je krijgt automatisch Android notificaties:
- "Google Drive Upload - Uploading report.pdf..."
- "Upload Complete - report.pdf uploaded"

---

## 📱 Android Paths Cheat Sheet

```bash
/sdcard/Download/          # Downloads
/sdcard/Documents/         # Documenten
/sdcard/DCIM/              # Foto's
/sdcard/Music/             # Muziek
/data/data/com.termux/files/home/  # Termux home
```

---

## 🎯 Meest Gebruikte Commando's

### List & Browse
```bash
# Root level
python tools/gdrive.py list

# Specifieke folder
python tools/gdrive.py list backups
python tools/gdrive.py list photos/2024
```

### Upload
```bash
# Naar root
python tools/gdrive.py upload /sdcard/file.txt

# Naar specifieke folder
python tools/gdrive.py upload /sdcard/data.csv backups/data

# Foto
python tools/gdrive.py upload /sdcard/DCIM/photo.jpg photos/vacation
```

### Download
```bash
# Naar Downloads
python tools/gdrive.py download file.pdf

# Naar specifieke locatie
python tools/gdrive.py download reports/summary.pdf /sdcard/Documents/
```

### Search
```bash
# Zoek bestanden
python tools/gdrive.py search invoice
python tools/gdrive.py search "report 2024"
```

### Info
```bash
# Check storage
python tools/gdrive.py info
```

---

## 🤖 Agent Zero Voorbeelden

### Simpele Upload
```
User: "Upload /sdcard/data.csv to Google Drive"

Agent: {
    "tool_name": "google_drive",
    "tool_args": {
        "operation": "upload",
        "local_path": "/sdcard/data.csv"
    }
}
```

### Backup Workflow
```
User: "Create a backup of my important files to Google Drive"

Agent:
1. Creates backup folder
2. Uploads files
3. Sends notification
4. Reports summary
```

### Download & Process
```
User: "Download sales data from Google Drive and calculate total revenue"

Agent:
1. Downloads file
2. Processes with Python
3. Uploads result back
4. Sends summary
```

---

## ⚠️ Belangrijke Tips

### 1. Check Eerst, Sync Later
```bash
# EERST kijken wat er is
python tools/gdrive.py list backups

# DAN pas uploaden
python tools/gdrive.py upload /sdcard/file.txt backups
```

### 2. Sync is GEVAARLIJK!
Sync **VERWIJDERT** bestanden die niet in source staan!

**Veilig testen:**
```bash
# Dry-run (alleen kijken, niet doen)
rclone sync /sdcard/docs gdrive:/docs --dry-run
```

### 3. Grote Bestanden
- Uploads/downloads hebben 5-10 min timeout
- Voor >100MB: gebruik WiFi, niet mobiele data
- rclone hervat automatisch bij onderbreking

### 4. Quota Check
```bash
python tools/gdrive.py info
```

Google Drive gratis: **15GB** limiet

---

## 🔒 Beveiliging

### Credentials Beschermen
```bash
chmod 600 ~/.config/rclone/rclone.conf
```

### Toegang Intrekken
Als je later toegang wilt intrekken:
1. Ga naar https://myaccount.google.com/permissions
2. Zoek "rclone"
3. Klik "Remove Access"

---

## 🔧 Troubleshooting

### "Google Drive not configured"
```bash
rclone config
# Voeg 'gdrive' remote toe
```

### "Operation timed out"
- Check internet verbinding
- Probeer kleinere bestanden
- Gebruik WiFi

### "Permission denied"
- Check file paths (gebruik absolute paths)
- Verify rclone config: `rclone listremotes`

### Files not showing up
```bash
# Refresh cache
rclone ls gdrive: --max-age 0s
```

---

## 🎓 Verder Leren

### Volledige Gids
```bash
cat ~/AI-EcoSystem/docs/GOOGLE_DRIVE_SETUP.md
```

### rclone Documentatie
```bash
rclone help
man rclone
```

### Agent Zero Gebruik
Gewoon vragen:
- "How do I use Google Drive?"
- "Show me Google Drive examples"
- "What can I do with Google Drive tool?"

---

## ✅ Checklist - Ben Je Klaar?

- [ ] rclone geïnstalleerd (check: `rclone version`)
- [ ] Google Drive geconfigureerd (run: `rclone config`)
- [ ] Test gedaan (run: `rclone ls gdrive:`)
- [ ] Helper script werkt (run: `python tools/gdrive.py list`)
- [ ] Agent Zero kent de tool (vraag: "List Google Drive files")

**Alles checked? Je bent klaar! 🎉**

---

## 🚀 Nu Doen!

**Stap 1:** Configureer (als nog niet gedaan)
```bash
rclone config
```

**Stap 2:** Test
```bash
python tools/gdrive.py list
```

**Stap 3:** Start Agent Zero en vraag
```bash
cd agent-zero && python run_cli.py
```
```
"List my Google Drive files"
"Upload /sdcard/test.txt to Google Drive"
```

**DONE!** ✨

---

*Voor vragen: zie docs/GOOGLE_DRIVE_SETUP.md of vraag Agent Zero!*
