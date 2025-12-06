# ⚡ WORKFLOW QUICK REFERENCE

**1-pagina cheatsheet voor AI-EcoSystem workflows**

---

## 🎯 WELKE WORKFLOW GEBRUIK IK?

| Je Vraag | Gebruik | Time | Agents |
|----------|---------|------|--------|
| "Schrijf code voor X" | Pattern 1 | 30-60s | Master → Code |
| "Zoek library voor Y en gebruik het" | Pattern 2 | 90-180s | Master → Research → Code |
| "Scrape website Z" | Pattern 3 | 2-4min | Master → Scraper → Code |
| "Bouw complete X systeem" | Pattern 4 | 5-15min | Master → Architect → Orchestrator → Specialists |
| "Multi-day project" | Pattern 5 | Multiple | All + Memory + Scheduler |
| "Check battery/GPS/etc" | Pattern 6 | 15-30s | Master → Android Tools |

---

## 📋 PATTERN TEMPLATES

### Pattern 1: Simple Code
```
Master → Code Specialist
Tools: code_execution_tool, file_operations_tool
```

### Pattern 2: Research + Code
```
Master → Knowledge Researcher → Code Specialist
Tools: knowledge_tool, web_search_tool, code_execution_tool
```

### Pattern 3: Web Scraping
```
Master → Web Scraper → Code Specialist → Storage
Tools: webpage_content_tool, code_execution_tool, file_operations_tool
```

### Pattern 4: Architecture
```
Master → Solution Architect → Task Orchestrator → Multiple Specialists
Tools: All tools, task_manager_tool, persistent_memory_tool
```

### Pattern 5: Multi-Session
```
Session 1: Architect → Plan → Execute Phase 1 → Save to Memory
Session 2+: Load Memory → Continue → Update Memory
Tools: persistent_memory_tool (critical!), task_scheduler_tool
```

### Pattern 6: Android
```
Master → Android Tools (direct or via Code Specialist)
Tools: android_features_tool, voice_interface_tool
```

---

## 🔧 CRITICAL TOOLS PER PATTERN

### All Patterns
- `call_subordinate` - Delegatie naar specialists
- `response` - Final answer naar user
- `persistent_memory_tool` - Save solutions (altijd!)

### Code Patterns (1, 2, 3)
- `code_execution_tool` - Python/NodeJS/Terminal
- `file_operations_tool` - File read/write
- `git_operations_tool` - Version control (optional)

### Research Pattern (2)
- `knowledge_tool` - Online search + memory
- `web_search_tool` - Multi-engine search
- `webpage_content_tool` - Extract URL content

### Scraping Pattern (3)
- `webpage_content_tool` - Extract webpage
- `code_execution_tool` - BeautifulSoup parsing
- `file_operations_tool` OR SQLite - Store data

### Architecture Pattern (4)
- `task_manager_tool` - Track subtasks
- `call_subordinate` - Multiple delegations
- `persistent_memory_tool` - Save architecture

### Multi-Session Pattern (5)
- `persistent_memory_tool` - CRITICAL for state
- `task_scheduler_tool` - Schedule future work
- `task_manager_tool` - Track progress

### Android Pattern (6)
- `android_features_tool` - 13 Android features
- `voice_interface_tool` - TTS/STT
- `code_execution_tool` - Process results

---

## ✅ CHECKLIST: BEFORE YOU START

**Voor elk type taak**:

1. ☐ Is dit al eerder gedaan? → Check `persistent_memory_tool("search")`
2. ☐ Is het complex? → Start met Solution Architect
3. ☐ Meerdere stappen? → Use Task Orchestrator
4. ☐ Waardevol voor later? → Save met `persistent_memory_tool("store")`

**Voor code taken**:

5. ☐ Dependencies nodig? → `code_execution_tool("terminal", "pip install X")`
6. ☐ Output zichtbaar? → ALTIJD `print()` gebruiken!
7. ☐ Errors? → `knowledge_tool("How to fix [error]")`

**Voor research taken**:

8. ☐ Specifieke vraag? → "What is best X for Y with Z constraints?"
9. ☐ Documentation URL known? → Use `webpage_content_tool`
10. ☐ General search? → Use `knowledge_tool`

**Voor multi-day projecten**:

11. ☐ Architecture designed? → Solution Architect eerst
12. ☐ Tasks tracked? → `task_manager_tool`
13. ☐ Future work scheduled? → `task_scheduler_tool`
14. ☐ State saved? → `persistent_memory_tool` after each session

---

## 🎭 AGENT SELECTION GUIDE

**Vraag jezelf**:

| Vraag | Agent | Command |
|-------|-------|---------|
| Moet er code geschreven worden? | Code Specialist | `/code` |
| Moet er onderzoek gedaan worden? | Knowledge Researcher | `/research` |
| Moet er van een website data gehaald worden? | Web Scraper | `/scrape` |
| Moet er een systeem ontworpen worden? | Solution Architect | `/architect` |
| Moeten er taken verdeeld worden? | Task Orchestrator | `/orchestrate` |
| Is het een complete workflow A-Z? | Master Orchestrator | `/master` |

**Start altijd met Master Orchestrator tenzij je exact weet welke specialist je nodig hebt.**

---

## 🚫 COMMON MISTAKES

| Mistake | Problem | Solution |
|---------|---------|----------|
| No `print()` in code | Geen output zichtbaar | ALTIJD print gebruiken |
| Delegate entire task | Infinite loop | Behoud oversight, delegate subtasks |
| No memory save | Solutions lost | Save valuable work! |
| Vague instructions | Poor results | Wees specifiek met requirements |
| Wrong agent for task | Inefficient | Use decision guide above |
| Forget `reset=true` | Agent confusion | New task → reset=true |

---

## 💡 PRO TIPS

### Memory Usage
```json
// Always save solutions
{
  "tool_name": "persistent_memory_tool",
  "tool_args": {
    "operation": "store",
    "content": "# Title\n[Solution]",
    "importance": 8,
    "tags": ["category"],
    "context": "Use when..."
  }
}

// Load at start
{
  "tool_name": "persistent_memory_tool",
  "tool_args": {
    "operation": "search",
    "query": "[problem]"
  }
}
```

### Delegation
```json
// New task
{
  "tool_name": "call_subordinate",
  "tool_args": {
    "message": "You are a Code Specialist. Task: [specific]",
    "reset": "true"
  }
}

// Follow-up
{
  "tool_name": "call_subordinate",
  "tool_args": {
    "message": "Good! Now adjust: [changes]",
    "reset": "false"
  }
}
```

### Code Execution
```json
// Always install dependencies first
{
  "tool_name": "code_execution_tool",
  "tool_args": {
    "runtime": "terminal",
    "code": "pip install requests beautifulsoup4"
  }
}

// Then execute with prints
{
  "tool_name": "code_execution_tool",
  "tool_args": {
    "runtime": "python",
    "code": "import requests\nresult = requests.get('...')\nprint(result.status_code)\nprint(result.text[:100])"
  }
}
```

---

## 📊 WORKFLOW DECISION FLOWCHART

```
Start
  ↓
Single simple task?
  ├─ YES → Pattern 1 (Simple Code)
  └─ NO ↓
        Research needed?
          ├─ YES → Pattern 2 (Research + Code)
          └─ NO ↓
                Web scraping?
                  ├─ YES → Pattern 3 (Scraping)
                  └─ NO ↓
                        Large project?
                          ├─ YES → Pattern 4 (Architecture)
                          └─ NO ↓
                                Multiple sessions?
                                  ├─ YES → Pattern 5 (Multi-Session)
                                  └─ NO ↓
                                        Android feature?
                                          ├─ YES → Pattern 6 (Android)
                                          └─ NO → Pattern 1 (default)
```

---

## 🎯 EXAMPLE REQUESTS

### Pattern 1
- "Schrijf Python code om CSV te lezen"
- "Maak een script dat files kopieert"
- "Debug deze code: [code]"

### Pattern 2
- "Zoek beste async library en maak voorbeeld"
- "Find documentation voor X en implementeer Y"
- "Research best practice en pas toe"

### Pattern 3
- "Scrape producten van example.com"
- "Extract API endpoints van docs"
- "Haal data van website en sla op"

### Pattern 4
- "Bouw REST API met database en auth"
- "Maak complete web scraper met dashboard"
- "Ontwikkel monitoring systeem"

### Pattern 5
- "Multi-day project: build X over 3 sessions"
- "Large application development"
- "Iterative feature additions"

### Pattern 6
- "Check battery en notificeer als < 20%"
- "Get GPS location en toon op kaart"
- "Lees deze tekst voor via TTS"

---

## ⚡ QUICK COMMANDS

```bash
# Start agent selector
cd /data/data/com.termux/files/home/AI-EcoSystem/agent-zero
./select-agent.sh

# Or direct
export AGENT_ZERO_ROLE="master_orchestrator"
python run_cli.py

# In Claude Code
/master      # Master Orchestrator
/code        # Code Specialist
/research    # Knowledge Researcher
/scrape      # Web Scraper
/architect   # Solution Architect
/orchestrate # Task Orchestrator
/agents      # Show all agents info
```

---

## 📚 MORE INFO

- **Full Workflows**: `.claude/OPTIMAL_WORKFLOWS.md`
- **Complete Analysis**: Ask for Task agent output
- **Agent Details**: `/agents` command
- **Tool Reference**: `ANDROID_TOOLS_QUICK_REF.md`

---

**Print this page for quick reference!**

Generated: 2025-11-29
Version: 1.0
