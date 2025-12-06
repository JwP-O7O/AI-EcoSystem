### file_operations tool:
- Advanced file and directory operations
- **Purpose**: Read, write, search, copy, move, and manage files and directories
- **Operations**:
  - **read**: Read file contents
    - path (required): File path to read
  - **write**: Write content to file (creates directories if needed)
    - path (required): File path to write
    - content (required): Content to write
  - **append**: Append content to existing file
    - path (required): File path
    - content (required): Content to append
  - **delete**: Delete file or directory
    - path (required): Path to delete
  - **copy**: Copy file or directory
    - path (required): Source path
    - destination (required): Destination path
  - **move**: Move/rename file or directory
    - path (required): Source path
    - destination (required): Destination path
  - **list**: List directory contents
    - path (required): Directory path
    - pattern (optional): Glob pattern (default: "*")
  - **create_dir**: Create directory
    - path (required): Directory path to create
  - **search**: Search for files matching pattern
    - path (required): Starting directory
    - pattern (required): File name pattern (e.g., "*.py")
  - **info**: Get file/directory information
    - path (required): Path to inspect
- **Example usage**:
```json
{
  "thoughts": [
    "I need to read the configuration file to understand the settings"
  ],
  "tool_name": "file_operations",
  "tool_args": {
    "operation": "read",
    "path": "/path/to/config.json"
  }
}
```
```json
{
  "thoughts": [
    "I'll create a new Python script with the requested functionality"
  ],
  "tool_name": "file_operations",
  "tool_args": {
    "operation": "write",
    "path": "/path/to/new_script.py",
    "content": "#!/usr/bin/env python3\n\ndef main():\n    print('Hello World')\n\nif __name__ == '__main__':\n    main()"
  }
}
```
- Use this for all file operations instead of code execution when possible
- More efficient than using bash commands for file operations
