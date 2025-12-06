from python.helpers.tool import Tool, Response
import subprocess
import os
import json

class GoogleDrive(Tool):
    """
    Google Drive integration via rclone

    Requires rclone to be configured with a 'gdrive' remote.
    Setup: rclone config
    """

    async def execute(self, operation="list", **kwargs):
        """
        Execute Google Drive operations

        Args:
            operation: One of: list, upload, download, sync, delete, mkdir, info
            **kwargs: Operation-specific arguments
        """

        # Check if rclone is installed
        if not self._check_rclone():
            return Response(
                message="❌ rclone is not installed. Run: pkg install rclone",
                break_loop=False
            )

        # Check if gdrive remote is configured
        if not self._check_gdrive_config():
            return Response(
                message="❌ Google Drive not configured. Run: rclone config\n" +
                        "Then add a remote named 'gdrive' for Google Drive.",
                break_loop=False
            )

        # Execute operation
        if operation == "list":
            return await self._list(**kwargs)
        elif operation == "upload":
            return await self._upload(**kwargs)
        elif operation == "download":
            return await self._download(**kwargs)
        elif operation == "sync":
            return await self._sync(**kwargs)
        elif operation == "delete":
            return await self._delete(**kwargs)
        elif operation == "mkdir":
            return await self._mkdir(**kwargs)
        elif operation == "info":
            return await self._info(**kwargs)
        elif operation == "search":
            return await self._search(**kwargs)
        else:
            return Response(
                message=f"❌ Unknown operation: {operation}\n" +
                        "Available: list, upload, download, sync, delete, mkdir, info, search",
                break_loop=False
            )

    def _check_rclone(self):
        """Check if rclone is installed"""
        try:
            result = subprocess.run(["which", "rclone"], capture_output=True)
            return result.returncode == 0
        except:
            return False

    def _check_gdrive_config(self):
        """Check if gdrive remote is configured"""
        try:
            result = subprocess.run(
                ["rclone", "listremotes"],
                capture_output=True,
                text=True
            )
            return "gdrive:" in result.stdout
        except:
            return False

    async def _list(self, path="", **kwargs):
        """List files in Google Drive"""
        try:
            # Use lsf for file listing (one per line)
            result = subprocess.run(
                ["rclone", "lsf", f"gdrive:{path}", "--format", "pst"],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                files = result.stdout.strip().split('\n') if result.stdout.strip() else []

                if not files or files == ['']:
                    return Response(
                        message=f"📁 No files found in gdrive:{path}",
                        break_loop=False
                    )

                # Format output
                output = f"📁 Files in gdrive:{path}\n\n"
                for i, file in enumerate(files[:50], 1):  # Limit to 50
                    parts = file.split(';')
                    if len(parts) >= 3:
                        size = parts[0]
                        mtime = parts[1]
                        name = parts[2]
                        output += f"{i:3}. {name:40} ({size} bytes)\n"
                    else:
                        output += f"{i:3}. {file}\n"

                if len(files) > 50:
                    output += f"\n... and {len(files) - 50} more files"

                return Response(message=output, break_loop=False)
            else:
                return Response(
                    message=f"❌ Error listing files: {result.stderr}",
                    break_loop=False
                )
        except subprocess.TimeoutExpired:
            return Response(
                message="❌ Operation timed out. Google Drive might be slow or remote not configured.",
                break_loop=False
            )
        except Exception as e:
            return Response(
                message=f"❌ Error: {str(e)}",
                break_loop=False
            )

    async def _upload(self, local_path="", gdrive_path="", **kwargs):
        """Upload file to Google Drive"""
        if not local_path:
            return Response(
                message="❌ Missing required argument: local_path",
                break_loop=False
            )

        # Expand paths
        local_path = os.path.expanduser(local_path)

        # Check if file exists
        if not os.path.exists(local_path):
            return Response(
                message=f"❌ File not found: {local_path}",
                break_loop=False
            )

        try:
            # Send notification (if on Android)
            try:
                subprocess.run([
                    "termux-notification",
                    "--title", "Google Drive Upload",
                    "--content", f"Uploading {os.path.basename(local_path)}...",
                ], timeout=2)
            except:
                pass

            # Upload
            result = subprocess.run(
                ["rclone", "copy", local_path, f"gdrive:{gdrive_path}", "-P"],
                capture_output=True,
                text=True,
                timeout=300  # 5 min timeout
            )

            if result.returncode == 0:
                filename = os.path.basename(local_path)
                file_size = os.path.getsize(local_path)

                # Success notification
                try:
                    subprocess.run([
                        "termux-notification",
                        "--title", "Upload Complete",
                        "--content", f"{filename} uploaded to Google Drive"
                    ], timeout=2)
                except:
                    pass

                return Response(
                    message=f"✅ Uploaded: {filename}\n" +
                            f"   From: {local_path}\n" +
                            f"   To: gdrive:{gdrive_path}\n" +
                            f"   Size: {file_size:,} bytes",
                    break_loop=False
                )
            else:
                return Response(
                    message=f"❌ Upload failed: {result.stderr}",
                    break_loop=False
                )
        except subprocess.TimeoutExpired:
            return Response(
                message="❌ Upload timed out. File might be too large or connection slow.",
                break_loop=False
            )
        except Exception as e:
            return Response(
                message=f"❌ Error: {str(e)}",
                break_loop=False
            )

    async def _download(self, gdrive_path="", local_path="/sdcard/Download/", **kwargs):
        """Download file from Google Drive"""
        if not gdrive_path:
            return Response(
                message="❌ Missing required argument: gdrive_path",
                break_loop=False
            )

        try:
            # Notification
            try:
                subprocess.run([
                    "termux-notification",
                    "--title", "Google Drive Download",
                    "--content", f"Downloading {gdrive_path}..."
                ], timeout=2)
            except:
                pass

            # Download
            result = subprocess.run(
                ["rclone", "copy", f"gdrive:{gdrive_path}", local_path, "-P"],
                capture_output=True,
                text=True,
                timeout=300
            )

            if result.returncode == 0:
                filename = os.path.basename(gdrive_path)

                # Success notification
                try:
                    subprocess.run([
                        "termux-notification",
                        "--title", "Download Complete",
                        "--content", f"{filename} downloaded"
                    ], timeout=2)
                except:
                    pass

                return Response(
                    message=f"✅ Downloaded: {filename}\n" +
                            f"   From: gdrive:{gdrive_path}\n" +
                            f"   To: {local_path}",
                    break_loop=False
                )
            else:
                return Response(
                    message=f"❌ Download failed: {result.stderr}",
                    break_loop=False
                )
        except subprocess.TimeoutExpired:
            return Response(
                message="❌ Download timed out.",
                break_loop=False
            )
        except Exception as e:
            return Response(
                message=f"❌ Error: {str(e)}",
                break_loop=False
            )

    async def _sync(self, local_dir="", gdrive_dir="", direction="upload", **kwargs):
        """Sync directory with Google Drive"""
        if not local_dir or not gdrive_dir:
            return Response(
                message="❌ Missing required arguments: local_dir and gdrive_dir",
                break_loop=False
            )

        try:
            if direction == "upload":
                source = local_dir
                dest = f"gdrive:{gdrive_dir}"
            else:
                source = f"gdrive:{gdrive_dir}"
                dest = local_dir

            result = subprocess.run(
                ["rclone", "sync", source, dest, "-P"],
                capture_output=True,
                text=True,
                timeout=600  # 10 min
            )

            if result.returncode == 0:
                return Response(
                    message=f"✅ Synced: {source} → {dest}",
                    break_loop=False
                )
            else:
                return Response(
                    message=f"❌ Sync failed: {result.stderr}",
                    break_loop=False
                )
        except subprocess.TimeoutExpired:
            return Response(
                message="❌ Sync timed out.",
                break_loop=False
            )
        except Exception as e:
            return Response(
                message=f"❌ Error: {str(e)}",
                break_loop=False
            )

    async def _delete(self, gdrive_path="", **kwargs):
        """Delete file from Google Drive"""
        if not gdrive_path:
            return Response(
                message="❌ Missing required argument: gdrive_path",
                break_loop=False
            )

        try:
            result = subprocess.run(
                ["rclone", "delete", f"gdrive:{gdrive_path}"],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                return Response(
                    message=f"✅ Deleted: gdrive:{gdrive_path}",
                    break_loop=False
                )
            else:
                return Response(
                    message=f"❌ Delete failed: {result.stderr}",
                    break_loop=False
                )
        except Exception as e:
            return Response(
                message=f"❌ Error: {str(e)}",
                break_loop=False
            )

    async def _mkdir(self, gdrive_path="", **kwargs):
        """Create directory in Google Drive"""
        if not gdrive_path:
            return Response(
                message="❌ Missing required argument: gdrive_path",
                break_loop=False
            )

        try:
            result = subprocess.run(
                ["rclone", "mkdir", f"gdrive:{gdrive_path}"],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                return Response(
                    message=f"✅ Created directory: gdrive:{gdrive_path}",
                    break_loop=False
                )
            else:
                return Response(
                    message=f"❌ Failed to create directory: {result.stderr}",
                    break_loop=False
                )
        except Exception as e:
            return Response(
                message=f"❌ Error: {str(e)}",
                break_loop=False
            )

    async def _info(self, **kwargs):
        """Get Google Drive info"""
        try:
            # Get about info
            result = subprocess.run(
                ["rclone", "about", "gdrive:"],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                return Response(
                    message=f"📊 Google Drive Info:\n\n{result.stdout}",
                    break_loop=False
                )
            else:
                return Response(
                    message=f"❌ Failed to get info: {result.stderr}",
                    break_loop=False
                )
        except Exception as e:
            return Response(
                message=f"❌ Error: {str(e)}",
                break_loop=False
            )

    async def _search(self, query="", **kwargs):
        """Search for files in Google Drive"""
        if not query:
            return Response(
                message="❌ Missing required argument: query",
                break_loop=False
            )

        try:
            # Use rclone lsf with grep
            result = subprocess.run(
                f"rclone lsf gdrive: -R | grep -i '{query}'",
                capture_output=True,
                text=True,
                shell=True,
                timeout=60
            )

            if result.returncode == 0 and result.stdout.strip():
                files = result.stdout.strip().split('\n')
                output = f"🔍 Search results for '{query}':\n\n"
                for i, file in enumerate(files[:20], 1):
                    output += f"{i:3}. {file}\n"

                if len(files) > 20:
                    output += f"\n... and {len(files) - 20} more results"

                return Response(message=output, break_loop=False)
            else:
                return Response(
                    message=f"🔍 No files found matching '{query}'",
                    break_loop=False
                )
        except Exception as e:
            return Response(
                message=f"❌ Search error: {str(e)}",
                break_loop=False
            )
