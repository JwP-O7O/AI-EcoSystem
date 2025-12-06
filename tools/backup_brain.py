import os
import subprocess
import datetime
import sys
import shutil

# --- CONFIGURATIE ---
BACKUP_DIRS = [
    "knowledge",
    "agent-zero/knowledge",
    "agent-zero/work_dir",
    "agent-zero/logs",
    "memory" # Toch meenemen voor als het later gevuld wordt
]

# Google Drive map via rclone config (gdrive:)
RCLONE_REMOTE = "gdrive:AI-EcoSystem-Backups"

# Temp dir voor het maken van de zip
TEMP_DIR = os.path.expanduser("~/.gemini/tmp")
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def log(msg):
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {msg}")

def check_rclone():
    """Check of rclone werkt en geconfigureerd is"""
    try:
        subprocess.run(["rclone", "version"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        log("❌ FOUT: rclone is niet geïnstalleerd! Run 'pkg install rclone'.")
        sys.exit(1)

    # Check remotes
    result = subprocess.run(["rclone", "listremotes"], capture_output=True, text=True)
    if "gdrive:" not in result.stdout:
        log("⚠️  LET OP: 'gdrive:' remote niet gevonden.")
        log("   Controleer 'rclone listremotes'. Als je remote anders heet, pas dit script aan.")
        # We proberen het toch, misschien heet hij anders, maar we waarschuwen wel.

def create_backup():
    """Maakt een tar.gz van de belangrijke mappen"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_name = f"brain_backup_{timestamp}.tar.gz"
    archive_path = os.path.join(TEMP_DIR, archive_name)

    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)

    log(f"📦 Start backup naar: {archive_name}")
    
    # Bestanden verzamelen
    # We gebruiken tar direct omdat dat makkelijker is met paden en symlinks
    
    # Construct tar command
    # tar -czf /path/to/archive.tar.gz -C /project/root dir1 dir2 ...
    
    dirs_to_backup = []
    for d in BACKUP_DIRS:
        full_path = os.path.join(PROJECT_ROOT, d)
        if os.path.exists(full_path):
            dirs_to_backup.append(d) # Relatief pad toevoegen
        else:
            log(f"   Skipping {d} (bestaat niet)")

    if not dirs_to_backup:
        log("❌ Geen mappen gevonden om te back-uppen!")
        return None

    cmd = ["tar", "-czf", archive_path, "-C", PROJECT_ROOT] + dirs_to_backup
    
    try:
        subprocess.run(cmd, check=True)
        size_mb = os.path.getsize(archive_path) / (1024 * 1024)
        log(f"✅ Archief gemaakt ({size_mb:.2f} MB)")
        return archive_path
    except subprocess.CalledProcessError as e:
        log(f"❌ Fout bij maken archief: {e}")
        return None

def upload_to_drive(local_path):
    """Upload het archief naar Google Drive via rclone"""
    filename = os.path.basename(local_path)
    target = f"{RCLONE_REMOTE}/{filename}"
    
    log(f"☁️  Uploaden naar {target}...")
    
    try:
        # Gebruik rclone copy
        subprocess.run(["rclone", "copy", local_path, RCLONE_REMOTE], check=True)
        log("✅ Upload geslaagd!")
        return True
    except subprocess.CalledProcessError as e:
        log(f"❌ Upload mislukt: {e}")
        return False

def cleanup(local_path):
    """Verwijder lokaal bestand"""
    try:
        os.remove(local_path)
        log("🧹 Lokaal bestand opgeruimd.")
    except OSError as e:
        log(f"⚠️ Kon lokaal bestand niet verwijderen: {e}")

def main():
    print("--- 🧠 AI Brain Backup Tool ---")
    check_rclone()
    
    archive = create_backup()
    if archive:
        success = upload_to_drive(archive)
        if success:
            cleanup(archive)
            print(f"\n🎉 Backup compleet! Je 'brein' staat veilig op Google Drive.")
        else:
            print(f"\n⚠️ Backup lokaal bewaard op: {archive}")

if __name__ == "__main__":
    main()
