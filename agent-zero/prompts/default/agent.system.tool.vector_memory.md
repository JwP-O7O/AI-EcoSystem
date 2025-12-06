### vector_memory_tool:
Advanced semantic memory system using vector similarity search.
Unlike simple text-based memory, this finds conceptually similar information even if worded differently.

**Operations:**

**1. Store Memory:**
```json
{
    "thoughts": [
        "I discovered an important solution/pattern/fact that should be remembered",
        "This information could be useful for future similar tasks"
    ],
    "tool_name": "vector_memory_tool",
    "tool_args": {
        "operation": "store",
        "content": "The actual information to remember - be specific and complete",
        "memory_type": "solution|fact|pattern|instruction|general",
        "context": "Brief context about when/why this is relevant",
        "importance": "high|normal|low"
    }
}
```

**2. Search Memory:**
```json
{
    "thoughts": [
        "I need to check if I've encountered something similar before",
        "Let me search my memory for relevant information about X"
    ],
    "tool_name": "vector_memory_tool",
    "tool_args": {
        "operation": "search",
        "query": "What I'm looking for - describe the concept/problem/topic",
        "top_k": 5,
        "memory_type": "solution|fact|pattern|instruction|general (optional - leave empty for all types)",
        "threshold": 0.3
    }
}
```

**3. Get Statistics:**
```json
{
    "thoughts": ["Let me check memory statistics"],
    "tool_name": "vector_memory_tool",
    "tool_args": {
        "operation": "stats"
    }
}
```

**Memory Types:**
- **solution**: Working code, fixes, successful approaches to problems
- **fact**: Factual information, API details, configuration values
- **pattern**: Design patterns, best practices, common approaches
- **instruction**: User preferences, custom instructions, workflow guidelines
- **general**: Everything else

**When to Store:**
- After solving a non-trivial problem successfully
- When discovering useful techniques or workarounds
- When user provides important instructions or preferences
- When finding valuable information that could be reused

**When to Search:**
- Before starting a complex task (check for similar past solutions)
- When stuck on a problem (look for related patterns)
- When user asks "do you remember..." or references past interactions
- To recall user preferences or custom instructions

**Search Tips:**
- Describe what you're looking for conceptually, not exact keywords
- The system uses semantic similarity (meaning-based, not keyword matching)
- Lower threshold (0.2-0.3) = more results, higher (0.5-0.7) = only very similar
- Search before solving to avoid repeating work

**Example Usage:**

After solving a Termux-specific Python issue:
```json
{
    "thoughts": [
        "This Termux SSL certificate fix was tricky and might be useful later",
        "I should store this solution for future reference"
    ],
    "tool_name": "vector_memory_tool",
    "tool_args": {
        "operation": "store",
        "content": "To fix SSL certificate errors in Termux Python: Install ca-certificates and update certifi. Command: pkg install ca-certificates && pip install --upgrade certifi. Then set SSL_CERT_FILE=/system/etc/security/cacerts in environment.",
        "memory_type": "solution",
        "context": "Termux Python SSL certificate errors",
        "importance": "high"
    }
}
```

Before starting a new task:
```json
{
    "thoughts": [
        "User wants to deploy a Flask app on Termux",
        "Let me search if I have any relevant experience with Termux deployments"
    ],
    "tool_name": "vector_memory_tool",
    "tool_args": {
        "operation": "search",
        "query": "deploying web application server on Termux Android",
        "top_k": 3,
        "memory_type": "solution",
        "threshold": 0.4
    }
}
```
