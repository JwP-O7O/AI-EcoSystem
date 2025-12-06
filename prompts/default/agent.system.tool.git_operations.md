### git_operations tool:
- Complete Git version control operations
- **Purpose**: Manage Git repositories, commits, branches, and remote operations
- **Operations**:
  - **status**: Get repository status
    - path (optional): Repository path (default: ".")
  - **init**: Initialize new repository
    - path (optional): Repository path
  - **clone**: Clone repository
    - url (required): Repository URL
    - path (required): Destination path
  - **add**: Stage files for commit
    - path (optional): Repository path
    - files (optional): Files to add (default: ["."] for all)
  - **commit**: Commit staged changes
    - path (optional): Repository path
    - message (required): Commit message
  - **push**: Push to remote
    - path (optional): Repository path
    - remote (optional): Remote name (default: "origin")
    - branch (optional): Branch name
  - **pull**: Pull from remote
    - path (optional): Repository path
    - remote (optional): Remote name (default: "origin")
    - branch (optional): Branch name
  - **branch**: Create or list branches
    - path (optional): Repository path
    - branch (optional): Branch name to create
  - **checkout**: Checkout branch
    - path (optional): Repository path
    - branch (required): Branch name
  - **log**: Show commit history
    - path (optional): Repository path
    - limit (optional): Number of commits (default: 10)
  - **diff**: Show changes
    - path (optional): Repository path
  - **reset**: Reset changes
    - path (optional): Repository path
    - mode (optional): Reset mode - "soft", "mixed", "hard" (default: "soft")
  - **stash**: Stash changes
    - path (optional): Repository path
    - action (optional): "save", "pop", "list" (default: "save")
- **Example usage**:
```json
{
  "thoughts": [
    "I need to check the current status of the Git repository"
  ],
  "tool_name": "git_operations",
  "tool_args": {
    "operation": "status",
    "path": "."
  }
}
```
```json
{
  "thoughts": [
    "I'll commit these changes with a descriptive message"
  ],
  "tool_name": "git_operations",
  "tool_args": {
    "operation": "commit",
    "message": "Add new feature for user authentication"
  }
}
```
- Use this instead of code_execution for Git commands
- Provides better error handling and formatted output
