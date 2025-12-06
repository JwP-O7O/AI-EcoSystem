#!/usr/bin/env python3
"""
Google Drive Helper Script
Quick CLI voor Google Drive operaties via rclone
"""

import subprocess
import sys
import os
from pathlib import Path

def check_rclone():
    """Check if rclone is installed and configured"""
    try:
        result = subprocess.run(["which", "rclone"], capture_output=True)
        if result.returncode != 0:
            print("❌ rclone is not installed")
            print("   Install: pkg install rclone")
            return False

        result = subprocess.run(["rclone", "listremotes"], capture_output=True, text=True)
        if "gdrive:" not in result.stdout:
            print("❌ Google Drive not configured")
            print("   Setup: rclone config")
            print("   Add a remote named 'gdrive'")
            return False

        return True
    except Exception as e:
        print(f"❌ Error checking rclone: {e}")
        return False

def list_files(path=""):
    """List files in Google Drive"""
    print(f"📁 Listing gdrive:{path}\n")
    result = subprocess.run(
        ["rclone", "lsf", f"gdrive:{path}", "--format", "pst"],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        files = result.stdout.strip().split('\n') if result.stdout.strip() else []
        if not files or files == ['']:
            print("   (empty)")
        else:
            for i, file in enumerate(files, 1):
                parts = file.split(';')
                if len(parts) >= 3:
                    try:
                        size = int(parts[0])
                    except ValueError:
                        size = 0 # Directory or invalid size
                    
                    name = parts[2]
                    if size > 0:
                        size_mb = size / (1024 * 1024)
                        print(f"{i:3}. {name:50} {size_mb:10.2f} MB")
                    else:
                        print(f"{i:3}. {name:50}   [DIR]")
                else:
                    print(f"{i:3}. {file}")
    else:
        print(f"❌ Error: {result.stderr}")

def upload(local_path, gdrive_path=""):
    """Upload file to Google Drive"""
    if not os.path.exists(local_path):
        print(f"❌ File not found: {local_path}")
        return

    filename = os.path.basename(local_path)
    file_size = os.path.getsize(local_path)
    size_mb = file_size / (1024 * 1024)

    print(f"⬆️  Uploading: {filename} ({size_mb:.2f} MB)")
    print(f"   From: {local_path}")
    print(f"   To: gdrive:{gdrive_path}")
    print()

    # Send notification
    try:
        subprocess.run([
            "termux-notification",
            "--title", "Google Drive Upload",
            "--content", f"Uploading {filename}..."
        ], timeout=2)
    except:
        pass

    result = subprocess.run(
        ["rclone", "copy", local_path, f"gdrive:{gdrive_path}", "-P"],
        timeout=600
    )

    if result.returncode == 0:
        print(f"\n✅ Upload complete!")

        # Success notification
        try:
            subprocess.run([
                "termux-notification",
                "--title", "Upload Complete",
                "--content", f"{filename} uploaded to Google Drive"
            ], timeout=2)
        except:
            pass
    else:
        print(f"\n❌ Upload failed")

def download(gdrive_path, local_path="/sdcard/Download/"):
    """Download from Google Drive"""
    filename = os.path.basename(gdrive_path)

    print(f"⬇️  Downloading: {filename}")
    print(f"   From: gdrive:{gdrive_path}")
    print(f"   To: {local_path}")
    print()

    # Notification
    try:
        subprocess.run([
            "termux-notification",
            "--title", "Google Drive Download",
            "--content", f"Downloading {filename}..."
        ], timeout=2)
    except:
        pass

    result = subprocess.run(
        ["rclone", "copy", f"gdrive:{gdrive_path}", local_path, "-P"],
        timeout=600
    )

    if result.returncode == 0:
        print(f"\n✅ Download complete!")
        print(f"   Saved to: {local_path}{filename}")

        # Success notification
        try:
            subprocess.run([
                "termux-notification",
                "--title", "Download Complete",
                "--content", f"{filename} downloaded"
            ], timeout=2)
        except:
            pass
    else:
        print(f"\n❌ Download failed")

def sync(local_dir, gdrive_dir, direction="upload"):
    """Sync directory"""
    if direction == "upload":
        print(f"🔄 Syncing {local_dir} → gdrive:{gdrive_dir}")
        source = local_dir
        dest = f"gdrive:{gdrive_dir}"
    else:
        print(f"🔄 Syncing gdrive:{gdrive_dir} → {local_dir}")
        source = f"gdrive:{gdrive_dir}"
        dest = local_dir

    print("\n⚠️  WARNING: Sync will delete files in destination that don't exist in source!")
    print("   Press Ctrl+C to cancel, or Enter to continue...")
    try:
        input()
    except KeyboardInterrupt:
        print("\n❌ Cancelled")
        return

    result = subprocess.run(
        ["rclone", "sync", source, dest, "-P"],
        timeout=1200
    )

    if result.returncode == 0:
        print(f"\n✅ Sync complete!")
    else:
        print(f"\n❌ Sync failed")

def info():
    """Show Google Drive info"""
    print("📊 Google Drive Storage Info:\n")
    result = subprocess.run(
        ["rclone", "about", "gdrive:"],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        print(result.stdout)
    else:
        print(f"❌ Error: {result.stderr}")

def search(query):
    """Search for files"""
    print(f"🔍 Searching for: {query}\n")
    result = subprocess.run(
        f"rclone lsf gdrive: -R | grep -i '{query}'",
        capture_output=True,
        text=True,
        shell=True,
        timeout=60
    )

    if result.returncode == 0 and result.stdout.strip():
        files = result.stdout.strip().split('\n')
        print(f"Found {len(files)} matches:\n")
        for i, file in enumerate(files[:30], 1):
            print(f"{i:3}. {file}")

        if len(files) > 30:
            print(f"\n... and {len(files) - 30} more")
    else:
        print("   No matches found")

def print_usage():
    """Print usage instructions"""
    print("""
Google Drive Helper - Quick CLI for rclone

Usage:
  python gdrive.py list [path]              List files
  python gdrive.py upload <file> [path]     Upload file
  python gdrive.py download <file> [dest]   Download file
  python gdrive.py sync <local> <remote>    Sync directory (upload)
  python gdrive.py syncdown <remote> <local> Sync directory (download)
  python gdrive.py info                     Show storage info
  python gdrive.py search <query>           Search files

Examples:
  python gdrive.py list
  python gdrive.py list backups
  python gdrive.py upload /sdcard/data.csv backups
  python gdrive.py download reports/summary.pdf /sdcard/Download/
  python gdrive.py sync /sdcard/Documents my-docs
  python gdrive.py info
  python gdrive.py search report

Setup:
  If not configured yet, run: rclone config
  Then add a remote named 'gdrive' for Google Drive
""")

def main():
    if not check_rclone():
        sys.exit(1)

    if len(sys.argv) < 2:
        print_usage()
        sys.exit(0)

    command = sys.argv[1].lower()

    try:
        if command == "list" or command == "ls":
            path = sys.argv[2] if len(sys.argv) > 2 else ""
            list_files(path)

        elif command == "upload" or command == "up":
            if len(sys.argv) < 3:
                print("❌ Usage: gdrive.py upload <local_file> [gdrive_path]")
                sys.exit(1)
            local_path = sys.argv[2]
            gdrive_path = sys.argv[3] if len(sys.argv) > 3 else ""
            upload(local_path, gdrive_path)

        elif command == "download" or command == "dl":
            if len(sys.argv) < 3:
                print("❌ Usage: gdrive.py download <gdrive_file> [local_path]")
                sys.exit(1)
            gdrive_path = sys.argv[2]
            local_path = sys.argv[3] if len(sys.argv) > 3 else "/sdcard/Download/"
            download(gdrive_path, local_path)

        elif command == "sync":
            if len(sys.argv) < 4:
                print("❌ Usage: gdrive.py sync <local_dir> <gdrive_dir>")
                sys.exit(1)
            local_dir = sys.argv[2]
            gdrive_dir = sys.argv[3]
            sync(local_dir, gdrive_dir, "upload")

        elif command == "syncdown":
            if len(sys.argv) < 4:
                print("❌ Usage: gdrive.py syncdown <gdrive_dir> <local_dir>")
                sys.exit(1)
            gdrive_dir = sys.argv[2]
            local_dir = sys.argv[3]
            sync(local_dir, gdrive_dir, "download")

        elif command == "info":
            info()

        elif command == "search":
            if len(sys.argv) < 3:
                print("❌ Usage: gdrive.py search <query>")
                sys.exit(1)
            query = sys.argv[2]
            search(query)

        elif command == "help" or command == "-h" or command == "--help":
            print_usage()

        else:
            print(f"❌ Unknown command: {command}")
            print_usage()
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n\n❌ Interrupted by user")
        sys.exit(1)
    except subprocess.TimeoutExpired:
        print("\n❌ Operation timed out")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
