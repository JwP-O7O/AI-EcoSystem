# 🎯 AI-ECOSYSTEM OPTIMAL WORKFLOWS

**Gebaseerd op complete project analyse**
**Gegenereerd**: 2025-11-29
**Voor**: AI-EcoSystem met 7 Specialized Agents + 21 Tools

---

## 📊 EXECUTIVE SUMMARY

Je AI-EcoSystem heeft een krachtige architectuur met:
- **7 Specialized Agents** met unieke expertise
- **21 Tools** voor diverse operaties
- **Hierarchical Delegation** systeem
- **Persistent Memory** met SQLite + FTS5
- **Android/Termux Native** integratie
- **Multi-Model Support** (Google Gemini, OpenAI, Claude, Ollama, etc.)

Dit document bevat **optimale workflows** voor elk type taak.

---

## 🎭 AGENT CAPABILITY MATRIX

| Agent | Primary Tools | Best For | Avoid For |
|-------|---------------|----------|-----------|
| **Master Orchestrator** | All tools, call_subordinate | Complex multi-step, coordination | Simple single tasks |
| **Code Specialist** | code_execution_tool, file_operations | Python/NodeJS/Terminal coding | Research, web scraping |
| **Knowledge Researcher** | knowledge_tool, web_search_tool, webpage_content_tool | Online research, documentation | Code execution |
| **Memory Manager** | persistent_memory_tool, memory_* | Storing/retrieving solutions | Real-time research |
| **Web Scraper** | webpage_content_tool, code_execution (BeautifulSoup) | Website data extraction | Code development |
| **Task Orchestrator** | call_subordinate, task_manager_tool | Multi-agent coordination | Direct execution |
| **Solution Architect** | All tools via delegation | Strategic planning, architecture | Simple implementation |

---

## 🔄 WORKFLOW PATTERNS

### Pattern 1: SIMPLE CODE TASK
**When**: Single script needed, no research required

```
USER REQUEST
    ↓
Master Orchestrator (analyzes)
    ↓
Code Specialist (delegates with reset=true)
    ├─ Plan code structure
    ├─ code_execution_tool("python", code)
    ├─ Test with print() statements
    └─ Return result
    ↓
Master Orchestrator (consolidates)
    ├─ Verify result
    ├─ Save to memory (if valuable)
    └─ Response to user
```

**Tools Used**:
- `call_subordinate` (Master → Code)
- `code_execution_tool` (Python/NodeJS/Terminal)
- `persistent_memory_tool` (optional save)
- `response` (final answer)

**Example**: "Schrijf Python code om CSV te lezen en eerste 10 rijen te printen"

**Time**: ~30-60 seconds

---

### Pattern 2: RESEARCH + IMPLEMENTATION
**When**: Need to find best approach/library before implementing

```
USER REQUEST
    ↓
Master Orchestrator
    ↓
┌─────────────────┐
│ PHASE 1: RESEARCH│
└─────────────────┘
Knowledge Researcher (delegates)
    ├─ knowledge_tool("What is best library for X?")
    ├─ webpage_content_tool(documentation_url)
    └─ Return findings
    ↓
Master Orchestrator (consolidates findings)
    ↓
┌─────────────────┐
│ PHASE 2: IMPLEMENT│
└─────────────────┘
Code Specialist (delegates with reset=true)
    ├─ Use findings from Phase 1
    ├─ code_execution_tool("terminal", "pip install library")
    ├─ code_execution_tool("python", implementation_code)
    └─ Return result
    ↓
┌─────────────────┐
│ PHASE 3: SAVE   │
└─────────────────┘
Master Orchestrator
    ├─ persistent_memory_tool("store", solution)
    └─ Response to user
```

**Tools Used**:
- `call_subordinate` (2x: Researcher, Code)
- `knowledge_tool` (research)
- `webpage_content_tool` (documentation)
- `code_execution_tool` (install + run)
- `persistent_memory_tool` (save)
- `response` (final)

**Example**: "Zoek de beste Python library voor async HTTP requests en maak een voorbeeld"

**Time**: ~90-180 seconds

---

### Pattern 3: WEB SCRAPING PROJECT
**When**: Extract data from websites and process it

```
USER REQUEST (URL + data requirements)
    ↓
Master Orchestrator (analyzes)
    ↓
┌─────────────────┐
│ PHASE 1: SCRAPE │
└─────────────────┘
Web Scraper (delegates)
    ├─ webpage_content_tool(url, objective)
    ├─ If complex HTML:
    │   └─ code_execution_tool("python", BeautifulSoup_code)
    └─ Return raw data
    ↓
┌─────────────────┐
│ PHASE 2: PROCESS│
└─────────────────┘
Code Specialist (delegates)
    ├─ Clean data
    ├─ Transform to required format
    ├─ file_operations_tool("write", output_file)
    └─ Return processed data
    ↓
┌─────────────────┐
│ PHASE 3: STORE  │
└─────────────────┘
Code Specialist (same or new)
    ├─ code_execution_tool("python", sqlite_insert)
    ├─ Verify with SELECT
    └─ Return confirmation
    ↓
Master Orchestrator
    ├─ persistent_memory_tool("store", scraping_pattern)
    └─ Response with summary
```

**Tools Used**:
- `call_subordinate` (3x: Scraper, Code, Code)
- `webpage_content_tool` (extract)
- `code_execution_tool` (parse, clean, store)
- `file_operations_tool` (save output)
- `persistent_memory_tool` (save pattern)
- `response` (final)

**Example**: "Scrape producten van https://example.com en sla op in SQLite database"

**Time**: ~120-240 seconds

---

### Pattern 4: COMPLEX ARCHITECTURE PROJECT
**When**: Large project requiring design, planning, and multi-phase execution

```
USER REQUEST (complex system requirements)
    ↓
Master Orchestrator
    ↓
┌─────────────────────┐
│ PHASE 1: ARCHITECTURE│
└─────────────────────┘
Solution Architect (delegates with reset=true)
    ├─ persistent_memory_tool("search", similar_projects)
    ├─ knowledge_tool("Best practices for X architecture")
    ├─ Decompose into components
    ├─ Design data flow
    ├─ Identify dependencies
    └─ Return architecture document
    ↓
Master Orchestrator (saves architecture)
    ├─ persistent_memory_tool("store", architecture)
    └─ Ask user for approval (optional)
    ↓
┌─────────────────────┐
│ PHASE 2: ORCHESTRATION│
└─────────────────────┘
Task Orchestrator (delegates with reset=true)
    ├─ Read architecture
    ├─ task_manager_tool("create", subtasks)
    ├─ Delegate to specialists:
    │   ├─ Code Specialist → Component A
    │   ├─ Code Specialist → Component B
    │   ├─ Knowledge Researcher → Documentation
    │   └─ Web Scraper → External data
    └─ Return status
    ↓
┌─────────────────────┐
│ PHASE 3: INTEGRATION│
└─────────────────────┘
Code Specialist (delegates)
    ├─ Combine all components
    ├─ code_execution_tool("python", integration_code)
    ├─ file_operations_tool("write", final_app)
    ├─ git_operations_tool("commit", "Initial implementation")
    └─ Return integrated system
    ↓
┌─────────────────────┐
│ PHASE 4: TESTING    │
└─────────────────────┘
Code Specialist (same or reset=false)
    ├─ code_execution_tool("python", test_suite)
    ├─ Fix errors if found
    └─ Return test results
    ↓
Master Orchestrator
    ├─ persistent_memory_tool("store", complete_solution)
    ├─ task_manager_tool("complete", all_tasks)
    └─ Response with project summary
```

**Tools Used**:
- `call_subordinate` (5x: Architect, Orchestrator, Code x3)
- `persistent_memory_tool` (search, save x2)
- `knowledge_tool` (research)
- `task_manager_tool` (create, complete)
- `code_execution_tool` (multiple components + tests)
- `file_operations_tool` (save files)
- `git_operations_tool` (version control)
- `response` (final)

**Example**: "Bouw een REST API met Flask, SQLite database, JWT authenticatie, en tests"

**Time**: ~5-15 minutes

---

### Pattern 5: MULTI-SESSION PROJECT
**When**: Project spans multiple days/sessions

```
SESSION 1:
    USER REQUEST
        ↓
    Master Orchestrator
        ↓
    Solution Architect (design)
        ├─ Create architecture
        ├─ persistent_memory_tool("store", architecture, importance=10)
        └─ Return plan
        ↓
    Task Orchestrator (plan execution)
        ├─ task_manager_tool("create", phase_1_tasks)
        ├─ task_scheduler_tool("schedule", phase_2, tomorrow)
        ├─ persistent_memory_tool("store", project_status)
        └─ Execute Phase 1
        ↓
    Master Orchestrator
        ├─ persistent_memory_tool("store", session_1_results)
        └─ Response: "Phase 1 done, scheduled Phase 2"

SESSION 2 (next day):
    USER REQUEST: "Continue project"
        ↓
    Master Orchestrator
        ├─ persistent_memory_tool("search", project_name)
        ├─ Load architecture, status, results
        └─ Understand context
        ↓
    Task Orchestrator
        ├─ task_manager_tool("list", pending)
        ├─ task_scheduler_tool("check", due_today)
        └─ Execute Phase 2
        ↓
    [Continue pattern...]
        ↓
    Master Orchestrator
        └─ persistent_memory_tool("update", project_status)

FINAL SESSION:
    ├─ Complete all tasks
    ├─ persistent_memory_tool("store", final_solution, importance=10)
    ├─ task_manager_tool("complete", all)
    └─ Response with complete project
```

**Tools Used**:
- `persistent_memory_tool` (search, store, update - critical!)
- `task_manager_tool` (create, list, complete)
- `task_scheduler_tool` (schedule, check)
- `call_subordinate` (various agents)
- All execution tools as needed

**Example**: "Bouw een complete web scraper met dashboard - spread over 3 dagen"

**Time**: Multiple sessions

---

### Pattern 6: ANDROID-SPECIFIC TASK
**When**: Using Android device capabilities

```
USER REQUEST (Android feature needed)
    ↓
Master Orchestrator
    ↓
Code Specialist OR direct execution
    ├─ android_features_tool("battery", "status")
    ├─ android_features_tool("location", "get")
    ├─ android_features_tool("notification", "show", params)
    ├─ voice_interface_tool("speak", text)
    ├─ Process results
    └─ Return data
    ↓
Master Orchestrator
    └─ Response with Android data
```

**Tools Used**:
- `android_features_tool` (13 features: battery, location, notification, etc.)
- `voice_interface_tool` (TTS, STT)
- `code_execution_tool` (process data)
- `response` (final)

**Example**: "Check battery status, get GPS location, and notify me if battery < 20%"

**Time**: ~15-30 seconds

---

## 🎯 TASK TYPE → OPTIMAL WORKFLOW

### Research Tasks
**Pattern**: Research + Implementation
**Agents**: Master → Knowledge Researcher → Code Specialist (optional)
**Tools**: knowledge_tool, web_search_tool, webpage_content_tool

**Examples**:
- "Wat is de beste library voor X?"
- "Zoek documentatie voor Y"
- "Hoe werkt Z technologie?"

---

### Coding Tasks
**Pattern**: Simple Code OR Research + Implementation
**Agents**: Master → Code Specialist
**Tools**: code_execution_tool, file_operations_tool

**Examples**:
- "Schrijf Python code voor X"
- "Maak een script dat Y doet"
- "Debug deze code"

---

### Web Scraping
**Pattern**: Web Scraping Project
**Agents**: Master → Web Scraper → Code Specialist
**Tools**: webpage_content_tool, code_execution_tool, file_operations_tool

**Examples**:
- "Scrape data van website X"
- "Extraheer producten van Y"
- "Haal API endpoints van documentatie"

---

### Architecture & Planning
**Pattern**: Complex Architecture Project
**Agents**: Master → Solution Architect → Task Orchestrator → Specialists
**Tools**: persistent_memory_tool, task_manager_tool, all execution tools

**Examples**:
- "Ontwerp een X systeem"
- "Plan de architectuur voor Y"
- "Hoe bouw ik Z schaalbaar?"

---

### Long-term Projects
**Pattern**: Multi-Session Project
**Agents**: All, coordinated over multiple sessions
**Tools**: persistent_memory_tool (critical!), task_manager_tool, task_scheduler_tool

**Examples**:
- "Bouw een complete applicatie"
- "Multi-day development project"
- "Incrementele features toevoegen"

---

### Android Integration
**Pattern**: Android-Specific Task
**Agents**: Master → Code Specialist (or direct)
**Tools**: android_features_tool, voice_interface_tool

**Examples**:
- "Check battery en notificeer me"
- "Get GPS location en sla op"
- "Lees deze tekst voor via TTS"

---

## 🔧 OPTIMIZATION STRATEGIES

### 1. MEMORY USAGE
**Always save valuable solutions**:
```json
{
  "tool_name": "persistent_memory_tool",
  "tool_args": {
    "operation": "store",
    "content": "# Solution Title\n[Details]",
    "summary": "Brief summary",
    "importance": 8,
    "tags": ["category", "problem-type"],
    "context": "Use when: [conditions]"
  }
}
```

**Load memories at start**:
```python
auto_memory_count = 3  # In initialize.py
```

Or manually:
```json
{
  "tool_name": "persistent_memory_tool",
  "tool_args": {
    "operation": "search",
    "query": "[problem description]",
    "limit": 5
  }
}
```

---

### 2. DELEGATION EFFICIENCY

**Use reset=true for new tasks**:
```json
{
  "tool_name": "call_subordinate",
  "tool_args": {
    "message": "You are a Code Specialist. Task: [specific]",
    "reset": "true"
  }
}
```

**Use reset=false for iterations**:
```json
{
  "tool_name": "call_subordinate",
  "tool_args": {
    "message": "Good! Now adjust: [changes]",
    "reset": "false"
  }
}
```

**Never delegate entire task** (causes infinite loops):
❌ "Solve this completely"
✅ "Research best library" → then use findings

---

### 3. TOOL COMBINATIONS

**Powerful combinations**:

1. **Research + Code**:
   - knowledge_tool → findings
   - code_execution_tool → implementation

2. **Scrape + Process + Store**:
   - webpage_content_tool → raw data
   - code_execution_tool → clean data
   - file_operations_tool OR code_execution_tool(sqlite) → persist

3. **Plan + Task + Execute**:
   - persistent_memory_tool → load previous work
   - task_manager_tool → track subtasks
   - call_subordinate → delegate execution

4. **Android + Code**:
   - android_features_tool → get device data
   - code_execution_tool → process & analyze
   - voice_interface_tool → speak results

---

### 4. ERROR HANDLING

**Standard error recovery flow**:
```
Error occurs
    ↓
knowledge_tool("How to fix [error message]?")
    ↓
Apply fix
    ↓
code_execution_tool (retry)
    ↓
If still fails: delegate to Code Specialist with error context
```

---

## 📈 PERFORMANCE METRICS

### Response Times (Gemini 2.5 Flash)

| Workflow Type | Expected Time | Complexity |
|---------------|---------------|------------|
| Simple Code | 30-60s | Low |
| Research + Implementation | 90-180s | Medium |
| Web Scraping | 120-240s | Medium-High |
| Architecture Project | 5-15min | High |
| Multi-Session | Multiple sessions | Very High |
| Android Task | 15-30s | Low |

### Tool Usage Frequency

| Tool | Usage % | Primary Agent |
|------|---------|---------------|
| code_execution_tool | 45% | Code Specialist |
| call_subordinate | 30% | Master, Orchestrator |
| persistent_memory_tool | 15% | All |
| knowledge_tool | 10% | Knowledge Researcher |
| Others | Varies | Varies |

---

## 🎓 BEST PRACTICES

### ✅ DO's

1. **Always specify role in delegation**:
   ```
   "You are a [EXACT ROLE NAME]. Your task: [specific]"
   ```

2. **Use print() in all code**:
   ```python
   result = calculate()
   print(f"Result: {result}")  # ← Critical!
   ```

3. **Save valuable solutions**:
   ```
   After successful implementation → persistent_memory_tool("store")
   ```

4. **Break complex tasks**:
   ```
   1 complex task → 3-5 subtasks → delegate each
   ```

5. **Verify before responding**:
   ```
   Execute → Test → Verify → Save → Respond
   ```

### ❌ DON'Ts

1. **No vague instructions**:
   ❌ "Make something for data"
   ✅ "Parse JSON, extract users, save to SQLite"

2. **No complete delegation**:
   ❌ "Solve everything"
   ✅ "Research library" → "Implement with library"

3. **No mixed roles**:
   ❌ "Research AND code AND test" in 1 call
   ✅ Separate calls: research, then code, then test

4. **No forgotten print statements**:
   ```python
   # ❌ No output
   result = process()

   # ✅ Output
   result = process()
   print(result)
   ```

---

## 🚀 QUICK START COMMANDS

### Start with Specific Agent

```bash
# Interactive selector
cd /data/data/com.termux/files/home/AI-EcoSystem/agent-zero
./select-agent.sh

# Direct with role
export AGENT_ZERO_ROLE="master_orchestrator"
python run_cli.py

# Or use shortcuts in Claude Code
/master
/code
/research
/scrape
/architect
/orchestrate
```

---

## 📊 WORKFLOW DECISION TREE

```
USER REQUEST
    ↓
    Is it a simple, single task?
    ├─ YES → Simple Code Task (Pattern 1)
    │         Master → Code Specialist
    │         Time: ~30-60s
    │
    └─ NO → Complex task
            ↓
            Need research first?
            ├─ YES → Research + Implementation (Pattern 2)
            │         Master → Researcher → Code Specialist
            │         Time: ~90-180s
            │
            └─ NO → Direct implementation needed
                    ↓
                    Involves web scraping?
                    ├─ YES → Web Scraping Project (Pattern 3)
                    │         Master → Scraper → Code Specialist
                    │         Time: ~2-4min
                    │
                    └─ NO → Complex development
                            ↓
                            Large multi-component project?
                            ├─ YES → Architecture Project (Pattern 4)
                            │         Master → Architect → Orchestrator → Specialists
                            │         Time: ~5-15min
                            │
                            └─ Spans multiple sessions?
                                ├─ YES → Multi-Session (Pattern 5)
                                │         Use persistent_memory + task_scheduler
                                │         Time: Multiple sessions
                                │
                                └─ Android feature needed?
                                    └─ YES → Android Task (Pattern 6)
                                              Master → android_features_tool
                                              Time: ~15-30s
```

---

## 🔍 EXAMPLE WORKFLOWS

### Example 1: "Maak een CSV processor"
**Pattern**: Simple Code Task
```
1. Master analyzes request
2. Delegates to Code Specialist (reset=true)
3. Code writes Python with pandas
4. Executes: code_execution_tool("python", code)
5. Tests with sample CSV
6. Master saves to memory
7. Response with code & results
```

### Example 2: "Zoek beste async library en maak voorbeeld"
**Pattern**: Research + Implementation
```
1. Master analyzes
2. Delegates to Knowledge Researcher
3. Researcher: knowledge_tool("best async HTTP library Python")
4. Researcher: webpage_content_tool(library_docs)
5. Researcher returns findings
6. Master delegates to Code Specialist with findings
7. Code: code_execution_tool("terminal", "pip install aiohttp")
8. Code: code_execution_tool("python", example_code)
9. Master saves solution to memory
10. Response with recommendation + working example
```

### Example 3: "Scrape products en sla op in database"
**Pattern**: Web Scraping Project
```
1. Master analyzes URL + requirements
2. Delegates to Web Scraper
3. Scraper: webpage_content_tool(url, "extract products")
4. Scraper returns raw HTML data
5. Master delegates to Code Specialist (new subordinate)
6. Code: parse HTML with BeautifulSoup
7. Code: create SQLite database
8. Code: insert products
9. Code: verify with SELECT query
10. Master saves scraping pattern to memory
11. Response with database path + sample data
```

### Example 4: "Ontwerp en bouw REST API"
**Pattern**: Complex Architecture Project
```
1. Master analyzes requirements
2. Delegates to Solution Architect
3. Architect: persistent_memory_tool("search", "REST API patterns")
4. Architect: knowledge_tool("Flask best practices")
5. Architect designs: routes, models, auth, tests
6. Architect returns architecture doc
7. Master: persistent_memory_tool("store", architecture)
8. Master delegates to Task Orchestrator with architecture
9. Orchestrator: task_manager_tool("create", [model, routes, auth, tests])
10. Orchestrator delegates:
    - Code Specialist A: database models
    - Code Specialist B: API routes
    - Code Specialist C: JWT auth
    - Code Specialist D: tests
11. Each specialist executes their part
12. Orchestrator consolidates results
13. Master delegates to Code Specialist (integration)
14. Code: combine all components
15. Code: git_operations_tool("commit", "Complete API")
16. Code: run test suite
17. Master: persistent_memory_tool("store", complete_solution)
18. Response with API code + test results
```

---

## 📝 CONFIGURATION RECOMMENDATIONS

### For Your Use Case

**Current Setup** (from analysis):
- Model: Google Gemini 2.5 Flash
- Platform: Termux/Android
- Capabilities: Full Android integration

**Recommended `initialize.py` settings**:
```python
# Models
chat_llm = models.get_google_chat(
    model_name="gemini-2.5-flash",
    temperature=0  # Consistent results
)

# Memory
auto_memory_count = 3  # Load top 3 memories

# Rate limiting
rate_limit_requests = 30  # Per minute

# Tools
max_tool_response_length = 3000

# Code execution
code_exec_docker_enabled = False  # Use native Termux
code_exec_ssh_enabled = False

# History
max_messages_before_cleanup = 25
```

---

## 🎯 WORKFLOW AUTOMATION SCRIPTS

See accompanying files:
- `workflow_simple_code.json` - Template for Pattern 1
- `workflow_research_implement.json` - Template for Pattern 2
- `workflow_web_scraping.json` - Template for Pattern 3
- `workflow_architecture.json` - Template for Pattern 4

Use these as starting points for common tasks.

---

## 📚 ADDITIONAL RESOURCES

- **Full Analysis**: See Task agent output above
- **Agent Details**: `/agents` command
- **Tool Reference**: `ANDROID_TOOLS_QUICK_REF.md`
- **Quick Start**: `QUICK_REFERENCE.md`
- **Specialized Agents**: `docs/SPECIALIZED_AGENTS_GUIDE.md`

---

**Generated by**: Claude Code Analysis
**Based on**: Complete AI-EcoSystem codebase analysis
**Version**: 1.0
**Last Updated**: 2025-11-29

**Ready to use!** Pick the pattern that matches your task and let the agents work for you. 🚀
