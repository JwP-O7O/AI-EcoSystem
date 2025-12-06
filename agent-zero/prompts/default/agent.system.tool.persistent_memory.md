# Persistent Memory Tool

Store and retrieve long-term memories across sessions using SQLite database with full-text search capabilities.

## Usage

```json
{
    "tool_name": "persistent_memory",
    "tool_args": {
        "operation": "store",
        "content": "Memory content to store",
        "summary": "Brief summary",
        "importance": 8,
        "tags": ["project", "solution"],
        "context": "project_name"
    }
}
```

## Operations

### store
Save new memory with metadata for future retrieval.

**Arguments:**
- `content` (required): The main content to remember
- `summary` (optional): Brief summary for quick scanning
- `importance` (1-10, default: 5): How important is this information
- `tags` (optional): List of tags for categorization
- `context` (optional): Context identifier (e.g., project name, task type)

**Example:**
```json
{
    "tool_name": "persistent_memory",
    "tool_args": {
        "operation": "store",
        "content": "Successfully implemented PDF text extraction using PyPDF2 library. Works well on ARM/Termux. Command: pip install PyPDF2",
        "summary": "PyPDF2 setup for Termux",
        "importance": 8,
        "tags": ["termux", "pdf", "setup"],
        "context": "pdf_processing"
    }
}
```

### recall
Retrieve memories by context, tags, or importance level.

**Arguments:**
- `context` (optional): Filter by context identifier
- `tags` (optional): Filter by tags (returns memories with ANY of these tags)
- `min_importance` (optional): Minimum importance level (1-10)
- `limit` (default: 10): Maximum number of memories to return

**Example:**
```json
{
    "tool_name": "persistent_memory",
    "tool_args": {
        "operation": "recall",
        "tags": ["termux", "setup"],
        "min_importance": 7,
        "limit": 5
    }
}
```

### search
Full-text search across all memory content using SQLite FTS5.

**Arguments:**
- `query` (required): Search query (supports boolean operators: AND, OR, NOT)
- `limit` (default: 10): Maximum results

**Example:**
```json
{
    "tool_name": "persistent_memory",
    "tool_args": {
        "operation": "search",
        "query": "PDF extraction ARM",
        "limit": 5
    }
}
```

### update
Modify existing memory by ID.

**Arguments:**
- `memory_id` (required): ID of memory to update
- `content`, `summary`, `importance`, `tags`, `context`: Fields to update

### delete
Remove specific memory by ID.

**Arguments:**
- `memory_id` (required): ID of memory to delete

### list
Show recent memories.

**Arguments:**
- `limit` (default: 20): Number of recent memories to show

### stats
Get database statistics (total memories, storage size, etc.).

**Arguments:** None

### summarize
Generate a summary of stored memories by context or tag.

**Arguments:**
- `context` (optional): Summarize memories in this context
- `tags` (optional): Summarize memories with these tags

## When to Use

Use persistent_memory for:
- **Solutions that work**: Store successful approaches, commands, configurations
- **Important discoveries**: Findings that save time in future tasks
- **Project context**: Remember project-specific details across sessions
- **Error solutions**: Remember how you fixed specific errors
- **Best practices**: Store patterns that work well

DO NOT use for:
- Temporary task data (use agent.data instead)
- Every single detail (be selective, store important things)
- Highly volatile information that changes frequently

## Best Practices

1. **Be selective**: Store only valuable, reusable information
2. **Use good tags**: Make memories easy to find later
3. **Set appropriate importance**: Use 8-10 for critical info, 5-7 for useful info, 1-4 for minor details
4. **Add context**: Group related memories by project/task
5. **Search before storing**: Avoid duplicates by searching first
6. **Update instead of creating new**: If memory exists, update it

## Example Workflow

```json
// 1. Search for existing solution
{
    "tool_name": "persistent_memory",
    "tool_args": {
        "operation": "search",
        "query": "termux numpy install"
    }
}

// 2. If not found, store new solution after solving
{
    "tool_name": "persistent_memory",
    "tool_args": {
        "operation": "store",
        "content": "Install numpy on Termux: pkg install python-numpy (ARM-optimized). Avoid pip install numpy as it may fail to compile.",
        "summary": "Termux numpy installation",
        "importance": 9,
        "tags": ["termux", "numpy", "installation"],
        "context": "termux_setup"
    }
}
```

## Storage Location

Memories are stored in SQLite database at: `{project_root}/memory_db/persistent_memory.db`

The database persists across agent restarts and can be backed up/restored.
