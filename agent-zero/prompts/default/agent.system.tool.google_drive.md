# Google Drive Tool

Integrate with Google Drive for file storage, backup, and synchronization via rclone.

**Requirements:** rclone must be configured with a 'gdrive' remote.

## Usage

```json
{
    "tool_name": "google_drive",
    "tool_args": {
        "operation": "list|upload|download|sync|delete|mkdir|info|search",
        ...operation-specific args
    }
}
```

## Operations

### list
List files and directories in Google Drive.

**Arguments:**
- `path` (optional): Path in Google Drive to list (default: root)

**Example:**
```json
{
    "tool_name": "google_drive",
    "tool_args": {
        "operation": "list",
        "path": "backups"
    }
}
```

**Returns:** List of files with sizes and modification times

---

### upload
Upload a local file to Google Drive.

**Arguments:**
- `local_path` (required): Path to local file
- `gdrive_path` (optional): Destination path in Google Drive (default: root)

**Example - Upload to root:**
```json
{
    "tool_name": "google_drive",
    "tool_args": {
        "operation": "upload",
        "local_path": "/sdcard/report.pdf"
    }
}
```

**Example - Upload to specific folder:**
```json
{
    "tool_name": "google_drive",
    "tool_args": {
        "operation": "upload",
        "local_path": "/sdcard/data.csv",
        "gdrive_path": "backups/data"
    }
}
```

**Features:**
- Shows upload progress
- Sends Android notification on start/completion
- Displays file size after upload

---

### download
Download a file from Google Drive to local storage.

**Arguments:**
- `gdrive_path` (required): Path to file in Google Drive
- `local_path` (optional): Local destination directory (default: /sdcard/Download/)

**Example:**
```json
{
    "tool_name": "google_drive",
    "tool_args": {
        "operation": "download",
        "gdrive_path": "reports/summary.pdf",
        "local_path": "/sdcard/Documents/"
    }
}
```

**Features:**
- Progress indicator
- Android notifications
- Automatic destination creation

---

### sync
Synchronize a directory with Google Drive.

**Arguments:**
- `local_dir` (required): Local directory path
- `gdrive_dir` (required): Google Drive directory path
- `direction` (optional): "upload" or "download" (default: "upload")

**Example - Sync local to Drive:**
```json
{
    "tool_name": "google_drive",
    "tool_args": {
        "operation": "sync",
        "local_dir": "/sdcard/Documents/Projects",
        "gdrive_dir": "Projects-Backup",
        "direction": "upload"
    }
}
```

**Example - Sync Drive to local:**
```json
{
    "tool_name": "google_drive",
    "tool_args": {
        "operation": "sync",
        "local_dir": "/sdcard/Documents/Shared",
        "gdrive_dir": "Team-Docs",
        "direction": "download"
    }
}
```

**Warning:** Sync deletes files in destination that don't exist in source. Use with caution!

---

### delete
Delete a file or directory from Google Drive.

**Arguments:**
- `gdrive_path` (required): Path to delete

**Example:**
```json
{
    "tool_name": "google_drive",
    "tool_args": {
        "operation": "delete",
        "gdrive_path": "old-backups/obsolete.txt"
    }
}
```

**Warning:** Deletion is permanent!

---

### mkdir
Create a new directory in Google Drive.

**Arguments:**
- `gdrive_path` (required): Path of directory to create

**Example:**
```json
{
    "tool_name": "google_drive",
    "tool_args": {
        "operation": "mkdir",
        "gdrive_path": "backups/2025"
    }
}
```

---

### info
Get information about Google Drive storage (used space, quota, etc.).

**Arguments:** None

**Example:**
```json
{
    "tool_name": "google_drive",
    "tool_args": {
        "operation": "info"
    }
}
```

**Returns:** Storage statistics (total, used, free space)

---

### search
Search for files by name in Google Drive.

**Arguments:**
- `query` (required): Search term (case-insensitive)

**Example:**
```json
{
    "tool_name": "google_drive",
    "tool_args": {
        "operation": "search",
        "query": "report"
    }
}
```

**Returns:** Up to 20 matching files

---

## Common Use Cases

### Backup Important Files
```json
// Create backup directory
{
    "tool_name": "google_drive",
    "tool_args": {
        "operation": "mkdir",
        "gdrive_path": "Agent-Zero-Backups"
    }
}

// Upload backup
{
    "tool_name": "google_drive",
    "tool_args": {
        "operation": "upload",
        "local_path": "/data/data/com.termux/files/home/AI-EcoSystem/memory.db",
        "gdrive_path": "Agent-Zero-Backups"
    }
}
```

### Download Data for Processing
```json
// Download from Drive
{
    "tool_name": "google_drive",
    "tool_args": {
        "operation": "download",
        "gdrive_path": "datasets/sales_data.csv",
        "local_path": "/sdcard/work/"
    }
}

// Process with code_execution
{
    "tool_name": "code_execution",
    "tool_args": {
        "language": "python",
        "code": "import pandas as pd; df = pd.read_csv('/sdcard/work/sales_data.csv'); print(df.describe())"
    }
}
```

### Share Analysis Results
```json
// Save analysis results
{
    "tool_name": "code_execution",
    "tool_args": {
        "language": "python",
        "code": "# analysis code that saves to /sdcard/analysis_report.pdf"
    }
}

// Upload to Drive
{
    "tool_name": "google_drive",
    "tool_args": {
        "operation": "upload",
        "local_path": "/sdcard/analysis_report.pdf",
        "gdrive_path": "Reports/Analysis"
    }
}
```

### Automated Backups
```json
// Sync entire directory
{
    "tool_name": "google_drive",
    "tool_args": {
        "operation": "sync",
        "local_dir": "/data/data/com.termux/files/home/AI-EcoSystem/work_dir",
        "gdrive_dir": "Agent-Zero-Work",
        "direction": "upload"
    }
}
```

---

## Setup Instructions

If Google Drive is not configured yet:

1. **Install rclone** (already installed on your system)

2. **Configure Google Drive remote:**
   ```bash
   rclone config
   ```

3. **Follow prompts:**
   - n) New remote
   - name> gdrive
   - Storage> drive (select Google Drive)
   - Use defaults for most options
   - For "Use auto config?" choose **n** (on Termux)
   - Open the provided URL in browser
   - Login and authorize
   - Copy verification code back to Termux

4. **Test configuration:**
   ```bash
   rclone ls gdrive:
   ```

5. **Tool is now ready!**

---

## Error Messages

**"rclone is not installed"**
- Run: `pkg install rclone`

**"Google Drive not configured"**
- Run: `rclone config` and add 'gdrive' remote

**"Operation timed out"**
- File might be too large
- Internet connection slow
- Try smaller files first

**"File not found"**
- Check local_path is correct
- Use absolute paths (/sdcard/..., not ~/...)

---

## Android Integration

This tool automatically:
- ✅ Sends notifications on upload/download start
- ✅ Sends notifications on completion
- ✅ Shows progress during transfer
- ✅ Uses /sdcard/ paths for easy mobile access

---

## Best Practices

1. **Use descriptive paths:**
   - Good: `gdrive_path: "backups/agent-zero/2025-11-29"`
   - Bad: `gdrive_path: "stuff"`

2. **Check before sync:**
   - Always use `list` first to see what will be affected
   - Sync can delete files!

3. **Regular backups:**
   - Upload important data regularly
   - Use dated folders for organization

4. **Check storage:**
   - Use `info` operation to monitor quota
   - Google Drive free: 15GB limit

5. **Error handling:**
   - Always check operation results
   - Have fallbacks for network issues

---

## Path Examples

**Android paths:**
- `/sdcard/Download/` - Downloads folder
- `/sdcard/Documents/` - Documents
- `/sdcard/DCIM/` - Photos
- `/data/data/com.termux/files/home/` - Termux home

**Google Drive paths:**
- `""` or `"/"` - Root
- `"backups"` - Folder in root
- `"backups/2025/january"` - Nested folders
- `"reports/summary.pdf"` - Specific file

---

## Security Notes

- Credentials are stored securely by rclone in `~/.config/rclone/rclone.conf`
- Never share this file
- Keep permissions: `chmod 600 ~/.config/rclone/rclone.conf`
- You can revoke access in Google account settings anytime

---

## Performance Tips

**For large files:**
- Upload/download may take time
- Operations have 5-10 minute timeouts
- Consider splitting very large files

**For many files:**
- Use sync instead of individual uploads
- Batch operations when possible

**Network:**
- Works best on WiFi
- Mobile data may be slow/expensive
- Uploads pause if connection drops (resumable)
