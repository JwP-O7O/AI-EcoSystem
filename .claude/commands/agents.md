# 🤖 AI-EcoSystem Specialized Agents & Tools Reference

Complete overzicht van alle beschikbare agents, tools en capabilities in je AI-EcoSystem.

---

## 🎭 BESCHIKBARE SPECIALIZED AGENTS (7 TOTAAL)

### 1. Master Orchestrator Agent
**Shortcut**: `/master`
**Rol**: Hoofdcoördinator en primaire interface

**Expertise**:
- Task analysis en decomposition
- Multi-agent coördinatie
- Quality assurance
- User communication
- Strategische planning

**Gebruik wanneer**:
- Complex multi-step taken
- Complete workflows van start tot finish
- Coördinatie van meerdere sub-agents nodig is
- High-level planning vereist is

**Voorbeeld taak**: "Plan en implementeer een complete web scraper met data opslag en error handling"

**Locatie**: `prompts/specialized-agents/role.master_orchestrator.md`

---

### 2. Code Execution Specialist
**Shortcut**: `/code`
**Rol**: Python/NodeJS/Terminal expert

**Expertise**:
- Python scripting en library usage
- NodeJS/JavaScript development
- Linux/Unix terminal commando's
- Package management (pip, npm, apt-get)
- Error debugging en troubleshooting
- File operations en data processing

**Gebruik wanneer**:
- Code schrijven en uitvoeren
- Scripts ontwikkelen
- Packages installeren
- File operaties uitvoeren
- Errors debuggen

**Voorbeeld taak**: "Schrijf Python code om JSON data te parsen en op te slaan in SQLite database"

**Locatie**: `prompts/specialized-agents/role.code_specialist.md`

---

### 3. Knowledge Research Specialist
**Shortcut**: `/research`
**Rol**: Online research en information retrieval expert

**Expertise**:
- Online search en information extraction
- Memory database queries
- Fact verification en cross-referencing
- Documentation research
- Solution pattern identification
- Up-to-date information gathering

**Gebruik wanneer**:
- Research naar libraries en tools
- Documentatie zoeken
- Best practices vinden
- Error solutions opzoeken
- Fact checking

**Voorbeeld taak**: "Zoek de beste Python library voor PDF parsing met OCR support"

**Locatie**: `prompts/specialized-agents/role.knowledge_researcher.md`

---

### 4. Memory Management Specialist
**Shortcut**: Gebruik via `/master` of `/orchestrate`
**Rol**: Knowledge keeper en long-term memory beheerder

**Expertise**:
- Store valuable solutions en code snippets
- Efficient memory database searches
- Maintain en cleanup oude memories
- Metadata filtering en relevancy scoring
- Memory organization en categorization

**Gebruik wanneer**:
- Solutions opslaan voor hergebruik
- Memories zoeken en filteren
- Knowledge base onderhoud
- Oude memories opschonen

**Voorbeeld taak**: "Sla deze database query pattern op voor later gebruik"

**Locatie**: `prompts/specialized-agents/role.memory_manager.md`

---

### 5. Web Content Extraction Specialist
**Shortcut**: `/scrape`
**Rol**: Web scraping en data extractie expert

**Expertise**:
- Webpage content extraction
- HTML parsing en analysis
- Data filtering en structuring
- API endpoint discovery
- Documentation scraping
- Real-time web data collection

**Gebruik wanneer**:
- Webpage content scrapen
- API documentation extractie
- HTML parsing
- Data verzameling van websites

**Voorbeeld taak**: "Extraheer alle productprijzen van deze e-commerce website"

**Locatie**: `prompts/specialized-agents/role.web_scraper.md`

---

### 6. Task Delegation Orchestrator
**Shortcut**: `/orchestrate`
**Rol**: Coordination expert en subtask delegator

**Expertise**:
- Task decomposition en analysis
- Role-based delegation
- Instruction formulation
- Progress tracking
- Result consolidation
- Context management

**Gebruik wanneer**:
- Complex multi-agent workflows
- Task decomposition nodig is
- Subordinate management
- Result consolidatie

**Voorbeeld taak**: "Coördineer de development van een REST API met database, tests en documentatie"

**Locatie**: `prompts/specialized-agents/role.task_orchestrator.md`

---

### 7. Solution Architecture Specialist
**Shortcut**: `/architect`
**Rol**: Strategische planner en problem solver

**Expertise**:
- Problem decomposition en analysis
- Solution pattern recognition
- Architecture design
- Dependency mapping
- Risk assessment
- Performance optimization strategies
- Best practices application

**Gebruik wanneer**:
- Complexe architectuur design
- Solution planning
- Dependency mapping
- Risk assessment
- Performance optimization

**Voorbeeld taak**: "Ontwerp de architectuur voor een real-time data processing pipeline"

**Locatie**: `prompts/specialized-agents/role.solution_architect.md`

---

## 🛠️ BESCHIKBARE TOOLS (21 TOTAAL)

### Core Agent Zero Tools

**1. call_subordinate**
- Delegeer taken naar sub-agents met specifieke rollen
- Gebruik `reset: true` voor nieuwe taken
- Gebruik `reset: false` voor follow-up

**2. code_execution_tool**
- Voer Python/NodeJS/Terminal code uit
- Runtimes: python, nodejs, terminal, output, reset
- ALTIJD gebruik print() voor output!

**3. knowledge_tool**
- Combinatie van online search + memory queries
- Vraag specifieke vragen, geen algemene guidance
- Prioriteert opensource tools

**4. webpage_content_tool**
- Extraheer content van webpages
- Specificeer URL en doel
- Filtert relevante informatie

**5. memory_save**
- Sla valuable solutions op
- Automatische metadata
- Voor hergebruik later

**6. memory_load**
- Zoek in memory database
- Threshold 0.6 (0=alles, 1=exact)
- Gebruik filters voor specifieke queries

**7. memory_delete**
- Verwijder memories by ID
- Gebruik UUID's
- Verify met load query

**8. memory_forget**
- Verwijder memories by query
- Threshold 0.75 default
- Gebruik voor cleanup

**9. response**
- Stuur antwoord naar user
- Final step in workflow
- Bevat complete resultaat

**10. task_done**
- Markeer taak als compleet
- Signaleert einde van agent werk

---

### Android-Specific Tools (11 extra)

**11. android_features_tool**
Capabilities:
- Battery status & optimization
- Network info & management
- Storage management
- Process management
- Termux:API integration
- GPS en sensor data
- Notifications

**12. file_operations_tool**
Capabilities:
- Find files by pattern
- Batch file operations
- Permission management
- Symlink operations
- Advanced search

**13. git_operations_tool**
Capabilities:
- Repository management
- Commit operations
- Branch management
- Remote operations (push/pull)
- Status en diff

**14. search_grep_tool**
Capabilities:
- Content search in files
- Pattern matching (regex)
- Multi-file search
- Context lines

**15. task_manager_tool**
Capabilities:
- Create/update/delete tasks
- Priority management
- Status tracking
- Task lists en filtering

**16. task_scheduler_tool**
Capabilities:
- Cron-like scheduling
- Recurring tasks
- Task automation
- Delayed execution

**17. web_search_tool**
Capabilities:
- DuckDuckGo integration
- Perplexity search
- Multiple search engines
- Enhanced results

**18. persistent_memory_tool**
Capabilities:
- Long-term storage
- Cross-session persistence
- Advanced queries
- Metadata support

**19. voice_interface_tool**
Capabilities:
- Text-to-speech
- Voice commands
- Audio processing
- Termux:API integration

**20. vector_memory_tool**
Capabilities:
- Semantic similarity search
- Embeddings storage
- Advanced retrieval
- Vector-based matching

**21. unknown**
- Fallback voor onbekende tools
- Error handling

**Tool Locaties**:
- Implementations: `python/tools/`
- Prompts: `prompts/default/agent.system.tool.*.md`

---

## 🎯 QUICK DECISION GUIDE

**Wat wil je doen?** → **Gebruik deze agent/command**

| Taak | Agent | Command |
|------|-------|---------|
| Code schrijven | Code Specialist | `/code` |
| Online research | Research Specialist | `/research` |
| Website scrapen | Web Scraper | `/scrape` |
| Architectuur ontwerpen | Solution Architect | `/architect` |
| Taken coördineren | Task Orchestrator | `/orchestrate` |
| Complete workflow | Master Orchestrator | `/master` |
| Memories beheren | Memory Manager | Via `/master` |

---

## 💡 WORKFLOW PATTERNS

### Pattern 1: Simple Code Task
```
1. /code
2. Geef specifieke instructies
3. Agent schrijft en test code
4. Resultaat
```

### Pattern 2: Research + Implementation
```
1. /research - Find best approach/library
2. /code - Implement solution
3. Test en verify
4. Save to memory (optional)
```

### Pattern 3: Complex Web Scraping
```
1. /scrape - Extract webpage content
2. /code - Process en clean data
3. /code - Save to database
4. Resultaat
```

### Pattern 4: Full Architecture Project
```
1. /architect - Design system architecture
2. /orchestrate - Break down into tasks
3. Multiple /code calls - Implement components
4. Test en integrate
5. Save solution
```

### Pattern 5: Master Orchestration
```
1. /master - Analyze complete task
2. Master delegates to:
   - /research voor info
   - /code voor implementation
   - /scrape voor data
   - Memory voor opslag
3. Consolidate results
4. Complete response
```

---

## 🚀 HOE TE STARTEN

### Methode 1: Agent Selector (Aanbevolen)
```bash
cd /data/data/com.termux/files/home/AI-EcoSystem/agent-zero
./select-agent.sh
```
Interactief menu met alle 7 agents.

### Methode 2: Direct Start
```bash
# In Termux
cd /data/data/com.termux/files/home/AI-EcoSystem/agent-zero
python run_cli.py

# In Ubuntu container
proot-distro login ubuntu -- bash -c "
cd /root/agent-zero-link
python run_cli.py
"
```

### Methode 3: Met Specifieke Role
```bash
# Set environment variable
export AGENT_ZERO_ROLE="code_specialist"

# Then start
python run_cli.py
```

**Agent Role Names**:
- `master_orchestrator` (default)
- `code_specialist`
- `knowledge_researcher`
- `memory_manager`
- `web_scraper`
- `task_orchestrator`
- `solution_architect`

---

## 📁 DIRECTORY STRUCTURE

### Prompts
```
prompts/
├── default/              # Core Agent Zero prompts (45+ files)
├── specialized-agents/   # Custom specialized roles (7 agents)
├── dianoia-small/        # Lightweight model prompts
└── dianoia-xl/           # Extended model prompts
```

### Python Code
```
python/
├── tools/                # 21 tool implementations
├── helpers/              # Utility functions
└── extensions/           # Custom extensions
    ├── message_loop_prompts/
    └── monologue_end/
```

### Documentation
```
/data/data/com.termux/files/home/AI-EcoSystem/
├── README.md
├── QUICK_REFERENCE.md
├── AGENT_ZERO_ANDROID_SETUP_COMPLEET.md
├── ANDROID_TOOLS_QUICK_REF.md
├── COMPLETE_GEBRUIKERSHANDLEIDING.md
└── docs/
    └── SPECIALIZED_AGENTS_GUIDE.md
```

### Data Directories
```
├── memory/          # Vector database storage
├── knowledge/       # Knowledge base files
├── work_dir/        # Agent workspace
├── logs/            # Agent execution logs
└── instruments/     # Custom instruments
```

---

## 🔧 SYSTEM CAPABILITIES

### Ondersteunde Runtimes
- Python 3.x (primary)
- NodeJS/JavaScript
- Bash/Terminal commands
- Ubuntu container (proot-distro)

### Pre-installed Packages (Termux)
**Python**:
- pandas, numpy, scipy
- requests, beautifulsoup4, lxml
- flask, fastapi
- sqlite3, psycopg2
- opencv-python, pillow
- anthropic, openai

**System**:
- git, curl, wget
- jq, fzf, ripgrep
- nodejs, npm
- termux-api (Android integration)

### Android Integration (via Termux:API)
- Battery monitoring
- Network status
- GPS location
- Notifications
- Voice/TTS
- Camera access
- Sensors
- Clipboard
- Storage management

---

## 📝 BEST PRACTICES

### ✅ DO's

**1. Wees Specifiek**
```
✅ "Schrijf Python code om CSV te lezen met pandas, filter rows waar age > 18, save als filtered.csv"
❌ "Verwerk deze data"
```

**2. Kies Juiste Agent**
- Code? → Code Specialist
- Research? → Research Specialist
- Complex? → Architect eerst, dan Orchestrator

**3. Geef Context**
```
✅ "Voor een web scraper project: extract product data van URL X met BeautifulSoup"
❌ "Haal data van een site"
```

**4. Gebruik Memory**
- Save waardevolle solutions
- Query memories voor hergebruik
- Keep knowledge organized

**5. Itereer Bij Errors**
- Analyseer error met knowledge_tool
- Fix code met code_execution_tool
- Test opnieuw

### ❌ DON'Ts

**1. Vermijd Vage Instructies**
```
❌ "Maak iets voor data"
✅ "Parse JSON file, extract user records, save to SQLite with schema: id, name, email"
```

**2. Geen Complete Task Delegatie**
```
❌ "Los alles op" (infinite loop!)
✅ "Step 1: Research best library" → dan volgende stappen
```

**3. Mix Geen Rollen**
```
❌ "Research AND code AND test AND document" in 1 call
✅ Separate calls voor research, code, test
```

**4. Vergeet Print Statements Niet**
```python
# ❌ BAD - geen output
result = calculate()

# ✅ GOOD - wel output
result = calculate()
print(f"Result: {result}")
```

---

## 🔍 TROUBLESHOOTING

### Probleem: Agent begrijpt rol niet

**Oplossing**: Wees explicieter
```json
{
    "message": "IMPORTANT: You are a Code Execution Specialist. Your ONLY job is to write and execute code.\n\nTask: [details]"
}
```

### Probleem: Infinite delegation loops

**Oorzaak**: Agent delegeert complete taak
**Oplossing**:
- Gebruik Architect voor planning
- Dan directe execution met tools
- Check hierarchical level (agent number)

### Probleem: Code heeft geen output

**Oorzaak**: Vergeten print() statements
**Oplossing**: ALTIJD print/console.log gebruiken
```python
# Add prints everywhere
print("Starting...")
result = process_data()
print(f"Result: {result}")
```

### Probleem: Tool niet gevonden

**Check**:
1. Tool bestaat in `python/tools/`?
2. Tool prompt in `prompts/default/`?
3. Correct gespeld in tool_name?

**Logs**: Check `logs/agent-*.log` voor details

### Probleem: Memory queries vinden niks

**Oplossing**:
- Verlaag threshold (0.5 i.p.v. 0.6)
- Gebruik bredere query terms
- Check of memories bestaan: `memory_load` zonder query

---

## 📊 ADVANCED FEATURES

### Custom Agents Maken

**Stap 1**: Creëer prompt file
```bash
nano prompts/specialized-agents/role.my_specialist.md
```

**Stap 2**: Voeg toe aan agent_config.py
```python
AGENT_ROLES = {
    "my_specialist": "role.my_specialist.md",
}
```

**Stap 3**: Start met role
```bash
export AGENT_ZERO_ROLE="my_specialist"
python run_cli.py
```

### Vector Memory Features

**Semantic Search**:
```json
{
    "tool_name": "vector_memory_tool",
    "tool_args": {
        "query": "database connection patterns",
        "limit": 5
    }
}
```

**Save with Embeddings**:
```json
{
    "tool_name": "vector_memory_tool",
    "tool_args": {
        "action": "save",
        "content": "Solution for async database pooling..."
    }
}
```

### Task Scheduling

**Schedule Recurring Task**:
```json
{
    "tool_name": "task_scheduler_tool",
    "tool_args": {
        "action": "schedule",
        "task": "backup_data",
        "cron": "0 2 * * *",
        "command": "python backup.py"
    }
}
```

---

## 🎓 EXAMPLE TASKS

### 1. Web Scraping to Database
```
1. /scrape
   "Extract product data from https://example.com/products"

2. /code
   "Process scraped data, clean it, save to SQLite with schema:
    products(id, name, price, url, scraped_at)"

3. /master
   "Verify database has data, count rows, show sample"
```

### 2. API Development
```
1. /architect
   "Design REST API with endpoints: /users, /posts, /comments
    Using Flask, SQLite, JWT auth"

2. /orchestrate
   "Implement the architecture:
    - Database models
    - API routes
    - Auth middleware
    - Error handling"

3. /code (multiple calls)
   "Implement each component"

4. Test en verify
```

### 3. Data Analysis Pipeline
```
1. /research
   "Find best Python libraries for:
    - CSV processing (large files)
    - Statistical analysis
    - Visualization"

2. /code
   "Implement pipeline:
    - Read CSV with chunking
    - Calculate statistics
    - Generate plots
    - Save report"
```

### 4. Automated Monitoring System
```
1. /architect
   "Design system that:
    - Monitors website uptime (every 5 min)
    - Logs to database
    - Sends alerts on downtime
    - Web dashboard"

2. /code
   "Implement monitoring script"

3. /schedule
   "Setup cron job for continuous monitoring"

4. /code
   "Create simple Flask dashboard"
```

---

## 📚 COMPLETE FILE REFERENCE

### Core Files
```
/data/data/com.termux/files/home/AI-EcoSystem/
├── agent.py              # Main agent class
├── initialize.py         # System initialization
├── models.py             # LLM model configs
├── run_cli.py            # CLI interface
├── run_ui.py             # Web UI interface
└── .env                  # Environment variables
```

### Agent Prompts (Specialized)
```
prompts/specialized-agents/
├── role.master_orchestrator.md
├── role.code_specialist.md
├── role.knowledge_researcher.md
├── role.memory_manager.md
├── role.web_scraper.md
├── role.task_orchestrator.md
├── role.solution_architect.md
├── agent_config.py
├── communication.md
├── README.md
└── QUICK_START.md
```

### Tool Files (21 tools)
```
python/tools/
├── call_subordinate.py
├── code_execution_tool.py
├── knowledge_tool.py
├── webpage_content_tool.py
├── memory_save.py
├── memory_load.py
├── memory_delete.py
├── memory_forget.py
├── response.py
├── task_done.py
├── android_features_tool.py
├── file_operations_tool.py
├── git_operations_tool.py
├── search_grep_tool.py
├── task_manager_tool.py
├── task_scheduler_tool.py
├── web_search_tool.py
├── persistent_memory_tool.py
├── voice_interface_tool.py
├── vector_memory_tool.py
└── unknown.py
```

---

## 🌟 QUICK COMMANDS REFERENCE

### Start Agents
```bash
# Interactive menu
./agent-zero/select-agent.sh

# Direct CLI
cd agent-zero && python run_cli.py

# With specific role
export AGENT_ZERO_ROLE="code_specialist" && python run_cli.py

# Web UI
python run_ui.py  # Then open browser to http://localhost:50002
```

### Check System
```bash
# List all agents
ls prompts/specialized-agents/role.*.md

# List all tools
ls python/tools/*.py

# Test agent config
cd prompts/specialized-agents && python agent_config.py

# View logs
tail -f logs/agent-*.log

# Check memory database
ls -lh memory/
```

### Documentation
```bash
# Full guide
cat docs/SPECIALIZED_AGENTS_GUIDE.md

# Quick reference
cat QUICK_REFERENCE.md

# Tool reference
cat ANDROID_TOOLS_QUICK_REF.md

# This file
cat .claude/commands/agents.md
```

---

**System Info**:
- **Platform**: Termux (Android) + Ubuntu Container
- **Agent Zero Version**: v0.6+
- **Specialized Agents**: v1.0
- **Total Agents**: 7
- **Total Tools**: 21
- **Python**: 3.11+
- **Node**: 18+

**Last Updated**: 2025-11-29

Voor meer details, zie de volledige documentatie in `docs/SPECIALIZED_AGENTS_GUIDE.md`
