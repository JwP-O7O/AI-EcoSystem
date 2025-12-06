from python.helpers.tool import Tool, Response
import os
import shutil
import glob
from pathlib import Path

class FileOperations(Tool):
    async def execute(self, **kwargs):
        """
        Advanced file operations tool for reading, writing, searching, and managing files
        """
        operation = kwargs.get("operation", "")
        path = kwargs.get("path", "")
        content = kwargs.get("content", "")
        pattern = kwargs.get("pattern", "")
        destination = kwargs.get("destination", "")

        self.log.log(type="info", heading=f"File Operation: {operation}")

        try:
            if operation == "read":
                return await self._read_file(path)
            elif operation == "write":
                return await self._write_file(path, content)
            elif operation == "append":
                return await self._append_file(path, content)
            elif operation == "delete":
                return await self._delete_file(path)
            elif operation == "copy":
                return await self._copy_file(path, destination)
            elif operation == "move":
                return await self._move_file(path, destination)
            elif operation == "list":
                return await self._list_directory(path, pattern)
            elif operation == "create_dir":
                return await self._create_directory(path)
            elif operation == "search":
                return await self._search_files(path, pattern)
            elif operation == "info":
                return await self._file_info(path)
            else:
                return Response(
                    message=f"Unknown operation: {operation}\n"
                    f"Available: read, write, append, delete, copy, move, list, create_dir, search, info",
                    break_loop=False
                )

        except Exception as e:
            return Response(message=f"File operation error: {str(e)}", break_loop=False)

    async def _read_file(self, path):
        """Read file contents"""
        if not os.path.exists(path):
            return Response(message=f"File not found: {path}", break_loop=False)

        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # Truncate if too long
        max_length = self.agent.config.max_tool_response_length
        if len(content) > max_length:
            content = content[:max_length] + f"\n\n[... truncated {len(content) - max_length} characters]"

        return Response(
            message=f"File: {path}\n\n```\n{content}\n```",
            break_loop=False
        )

    async def _write_file(self, path, content):
        """Write content to file"""
        os.makedirs(os.path.dirname(path) or '.', exist_ok=True)

        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)

        return Response(message=f"Successfully wrote to: {path}", break_loop=False)

    async def _append_file(self, path, content):
        """Append content to file"""
        with open(path, 'a', encoding='utf-8') as f:
            f.write(content)

        return Response(message=f"Successfully appended to: {path}", break_loop=False)

    async def _delete_file(self, path):
        """Delete file or directory"""
        if os.path.isdir(path):
            shutil.rmtree(path)
            return Response(message=f"Successfully deleted directory: {path}", break_loop=False)
        else:
            os.remove(path)
            return Response(message=f"Successfully deleted file: {path}", break_loop=False)

    async def _copy_file(self, path, destination):
        """Copy file or directory"""
        if os.path.isdir(path):
            shutil.copytree(path, destination)
        else:
            shutil.copy2(path, destination)

        return Response(
            message=f"Successfully copied {path} to {destination}",
            break_loop=False
        )

    async def _move_file(self, path, destination):
        """Move file or directory"""
        shutil.move(path, destination)
        return Response(
            message=f"Successfully moved {path} to {destination}",
            break_loop=False
        )

    async def _list_directory(self, path, pattern="*"):
        """List directory contents"""
        if not os.path.exists(path):
            return Response(message=f"Directory not found: {path}", break_loop=False)

        search_path = os.path.join(path, pattern)
        items = glob.glob(search_path)

        # Get details
        result_lines = []
        for item in sorted(items):
            size = os.path.getsize(item) if os.path.isfile(item) else 0
            item_type = "DIR" if os.path.isdir(item) else "FILE"
            result_lines.append(f"{item_type:4} {size:>10} {item}")

        result = "\n".join(result_lines) if result_lines else "No items found"

        return Response(
            message=f"Directory listing for: {path}\n\n{result}",
            break_loop=False
        )

    async def _create_directory(self, path):
        """Create directory"""
        os.makedirs(path, exist_ok=True)
        return Response(message=f"Successfully created directory: {path}", break_loop=False)

    async def _search_files(self, path, pattern):
        """Search for files matching pattern"""
        search_path = os.path.join(path, "**", pattern)
        matches = glob.glob(search_path, recursive=True)

        result = "\n".join(matches[:100]) if matches else "No matches found"
        if len(matches) > 100:
            result += f"\n\n[... {len(matches) - 100} more matches]"

        return Response(
            message=f"Search results for '{pattern}' in {path}:\n\n{result}",
            break_loop=False
        )

    async def _file_info(self, path):
        """Get file/directory information"""
        if not os.path.exists(path):
            return Response(message=f"Path not found: {path}", break_loop=False)

        stat = os.stat(path)
        info = [
            f"Path: {path}",
            f"Type: {'Directory' if os.path.isdir(path) else 'File'}",
            f"Size: {stat.st_size} bytes",
            f"Modified: {stat.st_mtime}",
            f"Permissions: {oct(stat.st_mode)}"
        ]

        return Response(message="\n".join(info), break_loop=False)
