# Google Drive Verbinden met Termux

**Gids voor het koppelen van Google Drive aan je Agent Zero systeem**

---

## 🎯 Doel

Google Drive toegankelijk maken vanuit:
- Agent Zero scripts
- Python code
- Termux terminal
- File synchronisatie

---

## 📋 Methode Overzicht

| Methode | Gebruik | Moeilijkheid | Aanbevolen |
|---------|---------|--------------|------------|
| **1. rclone** | Volledige sync, mount als directory | Medium | ⭐⭐⭐⭐⭐ |
| **2. Google Drive API (Python)** | Programmatische toegang | Medium | ⭐⭐⭐⭐ |
| **3. gdown** | Simpel downloaden | Makkelijk | ⭐⭐⭐ |
| **4. Termux Storage** | Alleen Android local | Makkelijk | ⭐⭐ |

---

## 🌟 METHODE 1: rclone (AANBEVOLEN)

**Beste optie voor:** Volledige integratie, sync, mount als directory

### Installatie

```bash
# Installeer rclone
pkg install rclone

# Verificeer installatie
rclone version
```

### Configuratie

```bash
# Start rclone config
rclone config

# Volg deze stappen:
# n) New remote
# name> gdrive
# Storage> drive (kies nummer voor Google Drive)
# client_id> [ENTER voor default]
# client_secret> [ENTER voor default]
# scope> 1 (Full access)
# root_folder_id> [ENTER]
# service_account_file> [ENTER]
# Edit advanced config? n
# Use auto config? n (BELANGRIJK op Termux!)

# Je krijgt een URL te zien - open op je telefoon:
# 1. Open de URL in browser
# 2. Login met je Google account
# 3. Geef toegang
# 4. Kopieer de verificatie code
# 5. Plak in Termux

# Configure this as a team drive? n
# Yes this is OK? y
```

### Gebruik rclone

```bash
# List bestanden in Google Drive
rclone ls gdrive:

# List directories
rclone lsd gdrive:

# Copy bestand VAN Google Drive
rclone copy gdrive:mijnbestand.txt /sdcard/Download/

# Copy bestand NAAR Google Drive
rclone copy /sdcard/data.csv gdrive:/backups/

# Sync hele directory
rclone sync /sdcard/Documents gdrive:/Android-Backup

# Mount Google Drive als directory (advanced)
mkdir -p ~/gdrive
rclone mount gdrive: ~/gdrive &
# Nu toegankelijk via: ~/gdrive/

# Unmount
fusermount -u ~/gdrive
```

### rclone in Python Scripts

```python
import subprocess
import os

def gdrive_upload(local_file, gdrive_path):
    """Upload bestand naar Google Drive via rclone"""
    cmd = ["rclone", "copy", local_file, f"gdrive:{gdrive_path}"]
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        print(f"✅ Uploaded: {local_file} → gdrive:{gdrive_path}")
        return True
    else:
        print(f"❌ Error: {result.stderr}")
        return False

def gdrive_download(gdrive_path, local_dir):
    """Download van Google Drive"""
    cmd = ["rclone", "copy", f"gdrive:{gdrive_path}", local_dir]
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        print(f"✅ Downloaded: gdrive:{gdrive_path} → {local_dir}")
        return True
    else:
        print(f"❌ Error: {result.stderr}")
        return False

def gdrive_list(path=""):
    """List bestanden in Google Drive"""
    cmd = ["rclone", "lsf", f"gdrive:{path}"]
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        files = result.stdout.strip().split('\n')
        return files
    else:
        return []

# Gebruik
if __name__ == "__main__":
    # Upload
    gdrive_upload("/sdcard/data.csv", "/backups/")

    # Download
    gdrive_download("/reports/summary.pdf", "/sdcard/Download/")

    # List
    files = gdrive_list("/backups")
    print("Files in /backups:", files)
```

### Agent Zero Integratie

**Agent kan automatisch uploaden/downloaden:**

```
User: "Backup /sdcard/important.db to Google Drive"

Agent: [Gebruikt code_execution met rclone]

User: "Download latest report from Google Drive"

Agent: [Gebruikt rclone to download]

User: "List all files in my Google Drive backups folder"

Agent: [Gebruikt rclone ls]
```

---

## 🐍 METHODE 2: Google Drive API (Python)

**Beste voor:** Programmatische controle, metadata, sharing

### Installatie

```bash
# Installeer Google API libraries
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

### Google Cloud Setup

1. **Ga naar Google Cloud Console:**
   - https://console.cloud.google.com/

2. **Create Project:**
   - Click "Select Project" → "New Project"
   - Name: "Agent Zero Drive"
   - Click "Create"

3. **Enable Google Drive API:**
   - Search "Google Drive API"
   - Click "Enable"

4. **Create Credentials:**
   - Go to "Credentials"
   - Click "Create Credentials" → "OAuth client ID"
   - Application type: "Desktop app"
   - Name: "Agent Zero"
   - Click "Create"
   - Download JSON → save as `credentials.json`

5. **Transfer credentials.json naar Termux:**
   ```bash
   # Download credentials.json naar /sdcard/Download/
   # Dan:
   cp /sdcard/Download/credentials.json ~/AI-EcoSystem/
   ```

### Python Code

```python
# File: gdrive_api.py
import os
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import io

SCOPES = ['https://www.googleapis.com/auth/drive']

class GoogleDriveAPI:
    def __init__(self, credentials_file='credentials.json'):
        self.creds = None
        self.service = None
        self.credentials_file = credentials_file
        self.token_file = 'token.pickle'

        self.authenticate()

    def authenticate(self):
        """Authenticate met Google Drive"""
        # Check for existing token
        if os.path.exists(self.token_file):
            with open(self.token_file, 'rb') as token:
                self.creds = pickle.load(token)

        # If no valid credentials, login
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, SCOPES)
                # Use run_local_server with specific settings for Termux
                self.creds = flow.run_local_server(port=8080, open_browser=False)

                print("\n🔗 Open this URL in your browser to authenticate:")
                print(flow.authorization_url()[0])

            # Save credentials
            with open(self.token_file, 'wb') as token:
                pickle.dump(self.creds, token)

        self.service = build('drive', 'v3', credentials=self.creds)
        print("✅ Authenticated with Google Drive")

    def list_files(self, folder_id=None, query=None):
        """List files in Google Drive"""
        try:
            if query is None:
                query = "trashed=false"
                if folder_id:
                    query += f" and '{folder_id}' in parents"

            results = self.service.files().list(
                q=query,
                pageSize=100,
                fields="files(id, name, mimeType, size, modifiedTime)"
            ).execute()

            files = results.get('files', [])
            return files
        except Exception as e:
            print(f"❌ Error listing files: {e}")
            return []

    def upload_file(self, local_path, drive_folder_id=None, drive_name=None):
        """Upload bestand naar Google Drive"""
        try:
            if drive_name is None:
                drive_name = os.path.basename(local_path)

            file_metadata = {'name': drive_name}
            if drive_folder_id:
                file_metadata['parents'] = [drive_folder_id]

            media = MediaFileUpload(local_path, resumable=True)
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id, name, webViewLink'
            ).execute()

            print(f"✅ Uploaded: {drive_name}")
            print(f"   File ID: {file.get('id')}")
            print(f"   Link: {file.get('webViewLink')}")

            return file
        except Exception as e:
            print(f"❌ Error uploading: {e}")
            return None

    def download_file(self, file_id, local_path):
        """Download bestand van Google Drive"""
        try:
            request = self.service.files().get_media(fileId=file_id)

            with io.FileIO(local_path, 'wb') as fh:
                downloader = MediaIoBaseDownload(fh, request)
                done = False
                while not done:
                    status, done = downloader.next_chunk()
                    if status:
                        print(f"Download {int(status.progress() * 100)}%")

            print(f"✅ Downloaded to: {local_path}")
            return True
        except Exception as e:
            print(f"❌ Error downloading: {e}")
            return False

    def search_files(self, name):
        """Zoek bestanden op naam"""
        query = f"name contains '{name}' and trashed=false"
        return self.list_files(query=query)

    def create_folder(self, folder_name, parent_id=None):
        """Maak folder aan in Google Drive"""
        try:
            file_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            if parent_id:
                file_metadata['parents'] = [parent_id]

            folder = self.service.files().create(
                body=file_metadata,
                fields='id, name'
            ).execute()

            print(f"✅ Folder created: {folder_name} (ID: {folder.get('id')})")
            return folder
        except Exception as e:
            print(f"❌ Error creating folder: {e}")
            return None

# Voorbeeld gebruik
if __name__ == "__main__":
    # Initialize
    gdrive = GoogleDriveAPI()

    # List files
    print("\n📁 Files in Google Drive:")
    files = gdrive.list_files()
    for f in files[:10]:  # Show first 10
        print(f"  - {f['name']} ({f.get('size', 'N/A')} bytes)")

    # Upload
    print("\n⬆️  Uploading file...")
    gdrive.upload_file("/sdcard/test.txt")

    # Search
    print("\n🔍 Searching for 'report'...")
    results = gdrive.search_files("report")
    for f in results:
        print(f"  Found: {f['name']}")
```

### Eerste Keer Authenticatie

```bash
# Run het script
python gdrive_api.py

# Output:
# 🔗 Open this URL in your browser to authenticate:
# https://accounts.google.com/o/oauth2/auth?...

# 1. Kopieer de URL
# 2. Open in browser (op telefoon of PC)
# 3. Login & geef toegang
# 4. Wordt automatisch gered in token.pickle
```

---

## 📦 METHODE 3: gdown (Simpel Downloaden)

**Beste voor:** Snel downloaden van publieke bestanden

### Installatie

```bash
pip install gdown
```

### Gebruik

```bash
# Download publiek bestand
gdown https://drive.google.com/uc?id=FILE_ID

# Download naar specifieke locatie
gdown https://drive.google.com/uc?id=FILE_ID -O /sdcard/Download/myfile.pdf

# Download folder (publiek)
gdown --folder https://drive.google.com/drive/folders/FOLDER_ID
```

### Python

```python
import gdown

# Download bestand
url = "https://drive.google.com/uc?id=YOUR_FILE_ID"
output = "/sdcard/Download/file.pdf"
gdown.download(url, output, quiet=False)

# Download folder
folder_url = "https://drive.google.com/drive/folders/YOUR_FOLDER_ID"
gdown.download_folder(folder_url, quiet=False)
```

**Limitaties:** Alleen publieke bestanden of met share link

---

## 🔧 METHODE 4: Termux Storage + Google Drive App

**Simpel maar gelimiteerd**

```bash
# Geef Termux toegang tot storage
termux-setup-storage

# Nu kun je /sdcard/ gebruiken
# En handmatig via Google Drive app syncen
```

**Gebruik:**
1. Installeer Google Drive app op Android
2. Enable "Backup & Sync" in Drive app
3. Selecteer folders om te syncen
4. Bestanden in /sdcard/ zijn toegankelijk

**Nadeel:** Geen programmatische controle

---

## 🤖 Agent Zero Integratie

### Met rclone (Aanbevolen)

**Maak tool voor Agent Zero:**

```python
# File: python/tools/google_drive_tool.py
from python.helpers.tool import Tool, Response
import subprocess

class GoogleDrive(Tool):
    async def execute(self, operation="", **kwargs):
        """
        Google Drive operations via rclone

        Operations:
        - list: List files
        - upload: Upload file
        - download: Download file
        - sync: Sync directory
        """

        if operation == "list":
            path = kwargs.get("path", "")
            result = subprocess.run(
                ["rclone", "lsf", f"gdrive:{path}"],
                capture_output=True,
                text=True
            )
            files = result.stdout.strip().split('\n') if result.stdout else []
            return Response(message=f"Files in gdrive:{path}:\n" + "\n".join(files))

        elif operation == "upload":
            local_file = kwargs.get("local_file")
            gdrive_path = kwargs.get("gdrive_path", "")

            result = subprocess.run(
                ["rclone", "copy", local_file, f"gdrive:{gdrive_path}"],
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                return Response(message=f"✅ Uploaded {local_file} to gdrive:{gdrive_path}")
            else:
                return Response(message=f"❌ Error: {result.stderr}")

        elif operation == "download":
            gdrive_file = kwargs.get("gdrive_file")
            local_path = kwargs.get("local_path", "/sdcard/Download/")

            result = subprocess.run(
                ["rclone", "copy", f"gdrive:{gdrive_file}", local_path],
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                return Response(message=f"✅ Downloaded gdrive:{gdrive_file} to {local_path}")
            else:
                return Response(message=f"❌ Error: {result.stderr}")

        else:
            return Response(message="Unknown operation. Use: list, upload, download, sync")
```

**Gebruik in Agent Zero:**

```
User: "Upload /sdcard/data.csv to my Google Drive backups folder"

Agent: [Gebruikt google_drive tool]
{
    "tool_name": "google_drive",
    "tool_args": {
        "operation": "upload",
        "local_file": "/sdcard/data.csv",
        "gdrive_path": "/backups/"
    }
}

User: "List all files in my Google Drive"

Agent: [Gebruikt google_drive tool]
{
    "tool_name": "google_drive",
    "tool_args": {
        "operation": "list"
    }
}
```

---

## 💡 Praktische Use Cases

### 1. Automatische Backups

```python
# Backup script
import subprocess
from datetime import datetime

def backup_to_gdrive():
    """Backup belangrijke data naar Google Drive"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"backup_{timestamp}.tar.gz"

    # Create backup
    subprocess.run([
        "tar", "-czf", f"/sdcard/{backup_name}",
        "/data/data/com.termux/files/home/AI-EcoSystem/memory",
        "/data/data/com.termux/files/home/AI-EcoSystem/knowledge"
    ])

    # Upload to Google Drive
    subprocess.run([
        "rclone", "copy",
        f"/sdcard/{backup_name}",
        "gdrive:/Agent-Zero-Backups/"
    ])

    print(f"✅ Backup completed: {backup_name}")

# Schedule dagelijks met cron of task_scheduler
backup_to_gdrive()
```

### 2. Document Sync

```python
# Sync Agent Zero outputs naar Google Drive
import subprocess

def sync_outputs():
    """Sync work_dir naar Google Drive"""
    subprocess.run([
        "rclone", "sync",
        "/data/data/com.termux/files/home/AI-EcoSystem/work_dir",
        "gdrive:/Agent-Zero-Outputs/",
        "--exclude", "*.tmp",
        "--exclude", ".git/"
    ])
    print("✅ Synced work_dir to Google Drive")

sync_outputs()
```

### 3. Data Analysis Workflow

```
User: "Download sales_data.csv from Google Drive, analyze it, and upload the report back"

Agent:
1. [Downloads via rclone]
2. [Analyzes with Python/pandas]
3. [Creates report.pdf]
4. [Uploads report back to Google Drive]
5. [Sends Android notification when done]
```

---

## 🔒 Beveiliging

### Best Practices

1. **Credentials Veilig Houden:**
   ```bash
   chmod 600 ~/AI-EcoSystem/credentials.json
   chmod 600 ~/AI-EcoSystem/token.pickle
   chmod 600 ~/.config/rclone/rclone.conf
   ```

2. **Nooit Committen:**
   ```bash
   # Add to .gitignore
   echo "credentials.json" >> .gitignore
   echo "token.pickle" >> .gitignore
   echo "rclone.conf" >> .gitignore
   ```

3. **Gebruik Scoped Access:**
   - Alleen drive.file scope als je alleen eigen bestanden nodig hebt
   - Full drive access alleen als echt nodig

---

## 🚀 Quick Start Checklist

### Voor rclone (Aanbevolen):

- [ ] `pkg install rclone`
- [ ] `rclone config` en Google Drive toevoegen
- [ ] Test: `rclone ls gdrive:`
- [ ] Upload test: `rclone copy /sdcard/test.txt gdrive:/`
- [ ] Klaar! ✅

### Voor Python API:

- [ ] `pip install google-api-python-client google-auth`
- [ ] Maak Google Cloud project
- [ ] Enable Drive API
- [ ] Download credentials.json
- [ ] Run authentication script
- [ ] Test upload/download
- [ ] Klaar! ✅

---

## 📚 Verder Lezen

- rclone docs: https://rclone.org/drive/
- Google Drive API: https://developers.google.com/drive/api/v3/about-sdk
- Python quickstart: https://developers.google.com/drive/api/v3/quickstart/python

---

**Welke methode wil je gebruiken? ik help je met de setup! 🚀**
