### search_grep tool:
- Search for patterns in files using advanced grep functionality
- **Purpose**: Find specific code, text patterns, or content across multiple files
- **Parameters**:
  - pattern (required): Search pattern (supports regex)
  - path (optional): Directory to search in (default: ".")
  - file_pattern (optional): File name pattern to search in (default: "*")
  - case_sensitive (optional): Case sensitive search (default: false)
  - whole_word (optional): Match whole words only (default: false)
  - context_lines (optional): Lines of context around matches (default: 2)
- **Example usage**:
```json
{
  "thoughts": [
    "I need to find where the 'calculate_total' function is defined",
    "I'll search for this pattern in Python files"
  ],
  "tool_name": "search_grep",
  "tool_args": {
    "pattern": "def calculate_total",
    "path": "./src",
    "file_pattern": "*.py",
    "context_lines": 3
  }
}
```
```json
{
  "thoughts": [
    "Looking for all TODO comments in the codebase"
  ],
  "tool_name": "search_grep",
  "tool_args": {
    "pattern": "TODO|FIXME|XXX",
    "path": ".",
    "case_sensitive": false,
    "context_lines": 1
  }
}
```
- Automatically uses ripgrep (rg) if available for faster searches
- Falls back to grep or Python search if needed
- Perfect for code exploration and debugging
