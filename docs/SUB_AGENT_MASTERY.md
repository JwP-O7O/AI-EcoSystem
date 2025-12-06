# Mastering Sub-Agents in Agent Zero v3.0

**Een complete gids voor het effectief gebruiken van gespecialiseerde agents**

---

## 📚 Inhoudsopgave

1. [De Sub-Agent Filosofie](#de-sub-agent-filosofie)
2. [Wanneer Sub-Agents Gebruiken](#wanneer-sub-agents-gebruiken)
3. [Effectieve Delegatie Patronen](#effectieve-delegatie-patronen)
4. [Beschikbare Agent Rollen](#beschikbare-agent-rollen)
5. [Sub-Agent Orchestratie Patronen](#sub-agent-orchestratie-patronen)
6. [Veelgemaakte Fouten & Oplossingen](#veelgemaakte-fouten--oplossingen)
7. [Geavanceerde Technieken](#geavanceerde-technieken)
8. [Android-Specifieke Delegatie](#android-specifieke-delegatie)
9. [Praktische Oefeningen](#praktische-oefeningen)

---

## De Sub-Agent Filosofie

Sub-agents zijn **NIET** alleen task delegators - ze zijn **gespecialiseerde experts met gefocuste context**.

### Kernprincipes

1. **Specialisatie**: Elke agent heeft een specifieke expertise
2. **Context Isolatie**: Sub-agents hebben schone, gefocuste context (geen "ruis")
3. **Autonomie**: Agents werken onafhankelijk en rapporteren resultaten
4. **Hiërarchie**: Agents kunnen sub-agents aanroepen (Agent 0 → Agent 1 → Agent 2)

### Hoe Het Werkt

```
User Input
    ↓
Agent 0 (Jij praat hiermee)
    ↓ [call_subordinate]
Agent 1 (Gespecialiseerde expert)
    ↓ [call_subordinate indien nodig]
Agent 2 (Sub-task specialist)
    ↓
Resultaten stromen terug omhoog
```

**Belangrijk**: Sub-agents zien hun "superior" (bovenliggende agent) als de gebruiker. Berichten stromen natuurlijk door de hiërarchie.

---

## Wanneer Sub-Agents Gebruiken

### ✅ GEBRUIK sub-agents wanneer:

- **Taak vereist gespecialiseerde expertise** (coding, research, scraping)
- **Je wilt geïsoleerde context** (voorkom vervuiling van main agent context)
- **Taak complex genoeg is** om dedicated focus te rechtvaardigen
- **Je parallelle uitvoering nodig hebt** (meerdere agents tegelijk)

### ❌ GEBRUIK GEEN sub-agents wanneer:

- **Simpele tool call voldoende is** (bijv. alleen een bestand lezen)
- **Taak de volledige context van main agent nodig heeft**
- **Overhead van delegatie groter is dan de taak zelf**

### Voorbeelden

**GOED - Gebruik Sub-Agent:**
```
User: "Zoek uit wat de beste Python PDF library is voor Termux, en implementeer het dan"

Agent 0 denkt:
1. Research vereist → Knowledge Researcher
2. Implementatie vereist → Code Specialist
```

**SLECHT - Gebruik Directe Tool:**
```
User: "Lees het bestand data.txt"

Agent 0 denkt:
1. Dit is een simpele tool call → gebruik code_execution direct
```

---

## Effectieve Delegatie Patronen

### ❌ SLECHTE Delegatie: Vaag en Zonder Context

```json
{
    "tool_name": "call_subordinate",
    "tool_args": {
        "message": "Write some code for data processing"
    }
}
```

**Problemen:**
- Geen specifieke rol
- Geen context
- Geen duidelijke taak
- Geen verwachtingen

### ✅ GOEDE Delegatie: Precies en Compleet

```json
{
    "tool_name": "call_subordinate",
    "tool_args": {
        "message": "You are a Code Execution Specialist expert in Python data processing.

CONTEXT: User has a CSV file at /sdcard/Download/sales_data.csv with columns: date, product, quantity, price.

TASK: Write Python code to:
1. Load the CSV using pandas
2. Calculate total revenue per product (quantity × price)
3. Find top 5 products by revenue
4. Save results to /sdcard/Download/top_products.csv

CONSTRAINTS:
- Use pandas (already installed)
- Include error handling for missing file
- Print progress messages
- Test with sample data first

EXPECTED OUTPUT:
- Code implementation
- Execution results
- Summary of top 5 products

Execute the code and report results.",
        "reset": "true"
    }
}
```

**Waarom dit goed is:**
- ✅ Duidelijke rol (Code Execution Specialist)
- ✅ Volledige context (bestand locatie, structuur)
- ✅ Specifieke stappen (4 duidelijke taken)
- ✅ Constraints (requirements & beperkingen)
- ✅ Verwachte output (wat terug rapporteren)
- ✅ `reset: "true"` (schone context)

---

## Beschikbare Agent Rollen

### 1. Master Orchestrator
**Prompt File:** `prompts/specialized-agents/role.master_orchestrator.md`

**Expertise:**
- Taak analyse en decompositie
- Multi-agent coördinatie
- Strategische planning
- Resource allocatie

**Wanneer gebruiken:**
- Complexe projecten met meerdere fasen
- Coördinatie van verschillende specialisten nodig
- High-level strategisch denken vereist

**Voorbeeld:**
```json
{
    "tool_name": "call_subordinate",
    "tool_args": {
        "message": "You are a Master Orchestrator.

TASK: Build a price comparison system that scrapes 3 e-commerce websites, analyzes prices, and sends daily reports.

Break this into subtasks and coordinate specialists to complete the project.",
        "reset": "true"
    }
}
```

### 2. Code Execution Specialist
**Prompt File:** `prompts/specialized-agents/role.code_specialist.md`

**Expertise:**
- Python scripting
- Bash/shell commands
- Node.js execution
- File operations
- Code debugging

**Wanneer gebruiken:**
- Code moet worden geschreven en uitgevoerd
- Scripts voor automatisering
- Data processing taken
- File manipulatie

**Voorbeeld:**
```json
{
    "tool_name": "call_subordinate",
    "tool_args": {
        "message": "You are a Code Execution Specialist.

TASK: Create a Python script that monitors /sdcard/Download/ for new PDF files, extracts text using PyPDF2, and saves to .txt files.

REQUIREMENTS:
- Use watchdog library for monitoring
- Handle errors gracefully
- Log all operations
- Test with sample PDF",
        "reset": "true"
    }
}
```

### 3. Knowledge Research Specialist
**Prompt File:** `prompts/specialized-agents/role.knowledge_researcher.md`

**Expertise:**
- Online search (DuckDuckGo)
- Information synthesis
- Documentation lookup
- Fact verification

**Wanneer gebruiken:**
- Informatie opzoeken
- Best practices research
- Library/package vergelijking
- Troubleshooting errors

**Voorbeeld:**
```json
{
    "tool_name": "call_subordinate",
    "tool_args": {
        "message": "You are a Knowledge Research Specialist.

RESEARCH TASK: Find the best Python library for image processing on ARM/Termux Android devices.

CRITERIA:
- ARM compatibility (crucial!)
- Active maintenance
- Good documentation
- Lightweight (mobile device)

DELIVERABLE: Top 3 options with pros/cons and installation commands for Termux.",
        "reset": "true"
    }
}
```

### 4. Memory Manager
**Prompt File:** `prompts/specialized-agents/role.memory_manager.md`

**Expertise:**
- Long-term memory storage
- Information retrieval
- Knowledge organization
- Context management

**Wanneer gebruiken:**
- Belangrijke informatie opslaan
- Oplossingen voor later hergebruiken
- Project context bijhouden
- Knowledge base opbouwen

**Voorbeeld:**
```json
{
    "tool_name": "call_subordinate",
    "tool_args": {
        "message": "You are a Memory Manager Specialist.

TASK: Store the successful solution for installing TensorFlow Lite on Termux.

CONTEXT: After 3 failed attempts, we found that 'pkg install python-tensorflow' works, while pip install fails due to ARM compilation issues.

Store this as high-importance memory with tags: termux, tensorflow, installation, arm",
        "reset": "true"
    }
}
```

### 5. Web Scraper Specialist
**Prompt File:** `prompts/specialized-agents/role.web_scraper.md`

**Expertise:**
- Webpage content extraction
- HTML parsing
- Data extraction patterns
- API interaction

**Wanneer gebruiken:**
- Webpagina's scrapen
- Content extraction
- Web data verzamelen
- HTML parsing

**Voorbeeld:**
```json
{
    "tool_name": "call_subordinate",
    "tool_args": {
        "message": "You are a Web Scraper Specialist.

TASK: Extract product information from https://example.com/products

EXTRACT:
- Product name
- Price
- Availability status
- Rating

OUTPUT FORMAT: JSON array with all products",
        "reset": "true"
    }
}
```

### 6. Task Orchestrator
**Prompt File:** `prompts/specialized-agents/role.task_orchestrator.md`

**Expertise:**
- Multi-agent delegation
- Task breakdown
- Parallel execution
- Results consolidation

**Wanneer gebruiken:**
- Complexe workflows met meerdere stappen
- Parallelle taken coördineren
- Meerdere specialisten nodig

**Voorbeeld:**
```json
{
    "tool_name": "call_subordinate",
    "tool_args": {
        "message": "You are a Task Orchestrator.

PROJECT: Build automated news aggregator

DELEGATE TO SPECIALISTS:
1. Web Scraper → Extract articles from 5 news sites
2. Code Specialist → Process and filter articles
3. Memory Manager → Store important articles
4. Task Scheduler → Set up daily automation

Coordinate their work and deliver final system.",
        "reset": "true"
    }
}
```

### 7. Solution Architect
**Prompt File:** `prompts/specialized-agents/role.solution_architect.md`

**Expertise:**
- System design
- Architecture planning
- Technology selection
- Best practices

**Wanneer gebruiken:**
- Nieuw systeem ontwerpen
- Architectuur beslissingen
- Technology stack kiezen
- Complex probleem oplossen

**Voorbeeld:**
```json
{
    "tool_name": "call_subordinate",
    "tool_args": {
        "message": "You are a Solution Architect.

CHALLENGE: Design a mobile-first AI assistant system on Android/Termux with offline capabilities.

REQUIREMENTS:
- Works offline (local LLM)
- Voice interface
- Persistent memory
- Low battery consumption
- < 500MB RAM usage

DELIVERABLE: Architecture proposal with component design and technology recommendations.",
        "reset": "true"
    }
}
```

---

## Sub-Agent Orchestratie Patronen

### Patroon 1: Sequentiële Delegatie
**Research → Implementatie → Validatie**

```json
// Stap 1: Research
{
    "thoughts": ["Need to research best approach first"],
    "tool_name": "call_subordinate",
    "tool_args": {
        "message": "You are a Knowledge Research Specialist.

Research: Best Python libraries for PDF text extraction on Android/Termux.
Focus on ARM compatibility.
Report top 3 options with pros/cons.",
        "reset": "true"
    }
}

// Wacht op resultaat...

// Stap 2: Implementatie (na research resultaten)
{
    "thoughts": ["Research shows PyPDF2 is best, now implement"],
    "tool_name": "call_subordinate",
    "tool_args": {
        "message": "You are a Code Execution Specialist.

Based on research showing PyPDF2 is best for Termux:
1. Install PyPDF2
2. Write code to extract text from /sdcard/document.pdf
3. Save to /sdcard/extracted_text.txt
4. Test and report results",
        "reset": "true"
    }
}

// Stap 3: Opslaan in Memory
{
    "thoughts": ["Solution works, save for future use"],
    "tool_name": "call_subordinate",
    "tool_args": {
        "message": "You are a Memory Manager.

Store this successful solution:
- PyPDF2 works on Termux
- Installation: pip install PyPDF2
- Code pattern: [include code]

Tags: termux, pdf, pypi, solution
Importance: 9",
        "reset": "true"
    }
}
```

### Patroon 2: Parallelle Delegatie
**Meerdere onafhankelijke sub-agents tegelijk**

**Belangrijk:** Je kunt GEEN parallelle call_subordinate doen in één message. Agent Zero werkt sequentieel. Voor echte parallelisatie moet je Master Orchestrator gebruiken die intern meerdere agents aanroept.

**Alternatief - Snelle Sequentiële Uitvoering:**
```json
// Agent 1: Data verzamelen
{
    "tool_name": "call_subordinate",
    "tool_args": {
        "message": "Web Scraper: Extract product prices from example.com/products. Be quick!",
        "reset": "true"
    }
}

// Meteen daarna Agent 2: Lokale data verwerken
{
    "tool_name": "call_subordinate",
    "tool_args": {
        "message": "Code Specialist: Process local inventory CSV at /sdcard/inventory.csv. Be quick!",
        "reset": "true"
    }
}

// Main agent consolideert beide resultaten
```

### Patroon 3: Hiërarchische Delegatie
**Master → Task Orchestrator → Specialisten**

```json
{
    "tool_name": "call_subordinate",
    "tool_args": {
        "message": "You are a Task Orchestrator.

CONTEXT: User wants to build a price comparison system for 3 websites.

YOUR MISSION:
Break this into subtasks and delegate to specialists:
1. Delegate web scraping to Web Scraper (for each site)
2. Delegate data processing to Code Specialist
3. Delegate result storage to Memory Manager

YOU coordinate their work using call_subordinate tool.
YOU consolidate results.
YOU report final comparison to me.",
        "reset": "true"
    }
}
```

---

## Veelgemaakte Fouten & Oplossingen

### Fout 1: Oneindige Delegatie Loop

**SLECHT:**
```json
{
    "message": "Complete the user's request: [hele user message kopiëren]"
}
```

**Probleem:** Sub-agent delegeert weer terug → infinite loop

**OPLOSSING:**
```json
{
    "message": "You are Code Specialist.

SPECIFIC SUBTASK: Write Python code to calculate average from [1,2,3,4,5].
DO NOT delegate further, just execute."
}
```

### Fout 2: Verkeerde Agent voor Taak

**SLECHT:**
```json
{
    "message": "Code Specialist: Search Google for Python tutorials"
}
```

**Probleem:** Code Specialist heeft geen web search focus

**OPLOSSING:**
```json
{
    "message": "Knowledge Research Specialist: Search for best Python tutorials for beginners"
}
```

### Fout 3: Geen Context Doorgeven

**SLECHT:**
```json
{
    "message": "Process that file we discussed earlier"
}
```

**Probleem:** Sub-agent heeft GEEN eerdere context (tenzij reset=false)

**OPLOSSING:**
```json
{
    "message": "Code Specialist:

CONTEXT: User has file /sdcard/data.csv with sales data (columns: date, product, price, quantity)

TASK: Calculate total revenue per product and save to /sdcard/revenue.csv"
}
```

### Fout 4: reset Niet Gebruiken

**Zonder reset:**
```json
{
    "tool_args": {
        "message": "Do something"
        // reset niet gespecificeerd
    }
}
```

**Probleem:** Sub-agent erft ALLE conversatie geschiedenis (kan ENORM zijn!)

**OPLOSSING:**
```json
{
    "tool_args": {
        "message": "Do something specific",
        "reset": "true"  // Schone, gefocuste context
    }
}
```

---

## Geavanceerde Technieken

### Techniek 1: Context Injectie

Geef sub-agent belangrijke bevindingen mee:

```json
{
    "message": "You are Code Specialist.

PREVIOUS FINDINGS:
- User prefers pandas over csv module (stated in earlier message)
- Data has missing values in 'price' column (discovered during exploration)
- User wants results in /sdcard/results/ directory (requirement)
- Battery is at 35% (be efficient)

NEW TASK: Process the sales data with these preferences in mind.
1. Use pandas (not csv)
2. Handle missing prices (skip or set to 0)
3. Save to /sdcard/results/
4. Keep code efficient (battery consideration)"
}
```

### Techniek 2: Android-Aware Delegatie

Maak gebruik van Android features in delegatie:

```json
{
    "message": "Code Specialist for Android/Termux:

ANDROID CONTEXT:
- Running on mobile device, battery at 45%
- Storage: use /sdcard/ for all outputs
- Send notification when task completes

TASK: Process large dataset /sdcard/bigdata.csv

REQUIREMENTS:
1. Check battery level first (android_features tool)
2. Process data efficiently
3. Send notification on completion using android_features tool:
   {\"tool_name\": \"android_features\", \"tool_args\": {\"feature\": \"notification\", \"title\": \"Processing Complete\", \"content\": \"Dataset processed successfully\"}}
4. Include vibration on completion

DELIVER: Processing results + confirmation of notification sent"
}
```

### Techniek 3: Error Recovery Delegatie

Sub-agent specifiek voor error recovery:

```json
{
    "message": "Code Specialist - ERROR RECOVERY MODE:

PREVIOUS ATTEMPT FAILED WITH ERROR:
Error: ModuleNotFoundError: No module named 'pandas'

CONTEXT:
- Running on Termux Android
- pip install might have failed
- Package might be available via pkg manager

YOUR ERROR RECOVERY TASK:
1. Check if pandas is truly missing (try importing)
2. If missing, try: pkg install python-numpy python-pandas
3. If pkg fails, try: pip install pandas
4. If all fails, use stdlib csv module instead
5. Report which approach worked

REQUIREMENT: Make it work using ANY available method. Be creative!"
}
```

### Techniek 4: Iterative Refinement

Gebruik sub-agent meerdere keren met feedback:

```json
// Ronde 1: Eerste poging
{
    "tool_name": "call_subordinate",
    "tool_args": {
        "message": "Code Specialist: Write regex to extract email addresses from text",
        "reset": "true"
    }
}

// Resultaat: Basis regex die alleen simple emails vindt

// Ronde 2: Verfijning met feedback
{
    "tool_name": "call_subordinate",
    "tool_args": {
        "message": "Code Specialist:

PREVIOUS VERSION: Basic regex that missed edge cases

REFINEMENT NEEDED:
- Handle emails with + symbol (user+tag@domain.com)
- Handle subdomains (user@mail.company.com)
- Handle new TLDs (.dev, .app, etc)

TASK: Improve the regex to handle these cases.
Test with these examples:
- user+tag@example.com
- admin@mail.company.org
- dev@startup.app",
        "reset": "true"
    }
}
```

---

## Android-Specifieke Delegatie

### Voorbeeld 1: Voice-Enabled Task

```json
{
    "tool_name": "call_subordinate",
    "tool_args": {
        "message": "Code Specialist with Voice Interface:

MOBILE TASK: Create a voice-controlled timer

IMPLEMENTATION:
1. Use voice_interface tool to listen for duration (\"set timer for 5 minutes\")
2. Parse the duration from speech
3. Use task_scheduler to schedule notification
4. Confirm with TTS: \"Timer set for X minutes\"

ANDROID TOOLS AVAILABLE:
- voice_interface (listen mode)
- task_scheduler (schedule notification)
- android_features (TTS confirmation)

DELIVER: Working voice timer with confirmation",
        "reset": "true"
    }
}
```

### Voorbeeld 2: Location-Aware Processing

```json
{
    "tool_name": "call_subordinate",
    "tool_args": {
        "message": "Code Specialist - Location-Aware:

TASK: Find nearby restaurants from local database based on current GPS location

STEPS:
1. Get GPS location using android_features tool
2. Load restaurant database from /sdcard/restaurants.json
3. Calculate distances (haversine formula)
4. Find 5 nearest restaurants
5. Send notification with results
6. Use TTS to announce top 3

ANDROID INTEGRATION:
- android_features for GPS
- android_features for notification
- voice_interface for TTS announcement",
        "reset": "true"
    }
}
```

### Voorbeeld 3: Battery-Aware Processing

```json
{
    "tool_name": "call_subordinate",
    "tool_args": {
        "message": "Code Specialist - Battery Optimization:

TASK: Process large image dataset

BATTERY-AWARE REQUIREMENTS:
1. Check battery level first (android_features)
2. If battery < 20% and not charging:
   - Send warning notification
   - Process only 10 images
   - Suggest user to charge device
3. If battery > 20% or charging:
   - Process all images
   - Send progress notifications every 25%
4. Vibrate when complete

ADAPTIVE BEHAVIOR based on battery!",
        "reset": "true"
    }
}
```

---

## Praktische Oefeningen

### Oefening 1: Simpele Delegatie
**Taak:** Vraag Code Specialist om een bestand te maken met top 10 prime numbers.

**Jouw Opdracht:** Schrijf de perfecte call_subordinate JSON.

<details>
<summary>Oplossing</summary>

```json
{
    "thoughts": ["Need code specialist to generate prime numbers"],
    "tool_name": "call_subordinate",
    "tool_args": {
        "message": "You are a Code Execution Specialist.

TASK: Create a Python script that generates the first 10 prime numbers and saves them to /sdcard/primes.txt

REQUIREMENTS:
- Use efficient prime checking algorithm
- One prime per line in output file
- Print confirmation when done
- Test the script

EXPECTED OUTPUT:
- File created at /sdcard/primes.txt
- Confirmation message
- List of the 10 primes",
        "reset": "true"
    }
}
```
</details>

### Oefening 2: Research + Implementatie
**Taak:** Zoek beste JSON parsing library voor Python, en maak dan een voorbeeld script.

**Jouw Opdracht:** Plan de sequentiële delegatie (2 stappen).

<details>
<summary>Oplossing</summary>

```json
// Stap 1: Research
{
    "thoughts": ["First research best JSON library"],
    "tool_name": "call_subordinate",
    "tool_args": {
        "message": "You are a Knowledge Research Specialist.

RESEARCH: Best Python libraries for JSON parsing and manipulation.

CRITERIA:
- Built-in vs third-party
- Performance
- Ease of use
- Special features (pretty print, schema validation, etc)

DELIVERABLE: Top 3 options with recommendation for general use case",
        "reset": "true"
    }
}

// Stap 2: Implementatie (na research)
{
    "thoughts": ["Research recommends stdlib json, now implement example"],
    "tool_name": "call_subordinate",
    "tool_args": {
        "message": "You are a Code Execution Specialist.

CONTEXT: Research shows stdlib 'json' module is best for general use.

TASK: Create example script demonstrating JSON operations:
1. Create a dict with person data (name, age, hobbies list)
2. Save to /sdcard/person.json (pretty printed)
3. Read it back
4. Modify age +1
5. Save again
6. Print final JSON

DELIVER: Working script with output",
        "reset": "true"
    }
}
```
</details>

### Oefening 3: Multi-Agent Workflow
**Taak:** Scrape product prices van website, verwerk data, en sla op in memory.

**Jouw Opdracht:** Ontwerp 3-staps workflow met juiste specialisten.

<details>
<summary>Oplossing</summary>

```json
// Stap 1: Web Scraping
{
    "thoughts": ["Web Scraper to extract prices"],
    "tool_name": "call_subordinate",
    "tool_args": {
        "message": "You are a Web Scraper Specialist.

TASK: Extract product information from https://example.com/products

EXTRACT FOR EACH PRODUCT:
- Product name
- Current price
- Original price (if on sale)
- Stock status

OUTPUT FORMAT: Return as JSON array for next agent to process",
        "reset": "true"
    }
}

// Stap 2: Data Processing
{
    "thoughts": ["Code Specialist to analyze pricing"],
    "tool_name": "call_subordinate",
    "tool_args": {
        "message": "You are a Code Execution Specialist.

INPUT DATA: [JSON array from web scraper]

TASK: Analyze pricing data:
1. Calculate average price
2. Find products on sale (discount > 20%)
3. Find out-of-stock items
4. Create summary report

OUTPUT: Formatted analysis report + JSON data for memory storage",
        "reset": "true"
    }
}

// Stap 3: Memory Storage
{
    "thoughts": ["Memory Manager to store findings"],
    "tool_name": "call_subordinate",
    "tool_args": {
        "message": "You are a Memory Manager Specialist.

TASK: Store pricing analysis for future reference

DATA TO STORE:
- Analysis report: [insert report]
- Key findings: average price, best deals, stock issues
- Timestamp: current date/time

MEMORY PARAMETERS:
- Context: price_monitoring
- Tags: ecommerce, pricing, analysis
- Importance: 7
- Summary: Daily price analysis for example.com products

Use persistent_memory tool to store",
        "reset": "true"
    }
}
```
</details>

### Oefening 4: Android Integration
**Taak:** Maak een systeem dat elke dag om 9:00 het weer opzoekt en een notificatie stuurt.

**Jouw Opdracht:** Design de delegatie met Android features.

<details>
<summary>Oplossing</summary>

```json
{
    "thoughts": ["Task Orchestrator to set up daily weather notification system"],
    "tool_name": "call_subordinate",
    "tool_args": {
        "message": "You are a Task Orchestrator.

PROJECT: Daily Weather Notification System

REQUIREMENTS:
- Check weather every day at 09:00
- Send Android notification with weather info
- Use TTS to announce weather

YOUR COORDINATION TASK:

1. DELEGATE TO Code Specialist:
   Create Python script that:
   - Gets current location (android_features GPS)
   - Fetches weather from API (use knowledge tool to find free weather API)
   - Formats weather message
   - Sends notification (android_features)
   - Uses TTS to speak weather (voice_interface)

2. DELEGATE TO Task Scheduler Setup:
   Schedule the weather script to run daily at 09:00
   - Use task_scheduler tool
   - Set as recurring task
   - Action: execute the Python weather script

3. TEST:
   Run the weather script manually once to verify it works

DELIVERABLE:
- Working weather script
- Scheduled task confirmed
- Test results

Use call_subordinate to delegate these tasks to appropriate specialists.",
        "reset": "true"
    }
}
```
</details>

---

## Quick Reference Card

### Delegatie Template

```json
{
    "thoughts": ["I need [EXPERTISE] for [SUBTASK]"],
    "tool_name": "call_subordinate",
    "tool_args": {
        "message": "You are a [ROLE].

CONTEXT:
[Relevante achtergrond informatie]

TASK:
[Specifieke, uitvoerbare instructies met nummering]

CONSTRAINTS:
[Beperkingen, requirements, te vermijden dingen]

EXPECTED OUTPUT:
[Wat je terug wilt hebben]

[Extra instructies indien nodig]",
        "reset": "true"
    }
}
```

### Agent Selectie Cheat Sheet

| Taak Type | Beste Agent | Reden |
|-----------|-------------|-------|
| Python/Bash uitvoeren | Code Execution Specialist | Direct tool access, execution focus |
| Web search, docs opzoeken | Knowledge Research Specialist | Search tools, synthesis skills |
| Website scrapen | Web Scraper | Webpage tool, extraction focus |
| Info opslaan/ophalen | Memory Manager | Memory tools, organization |
| Multi-step complex | Task Orchestrator | Delegation skills, coördinatie |
| Systeem ontwerpen | Solution Architect | High-level denken, planning |
| Algemene coördinatie | Master Orchestrator | Balanced, all-tool access |

---

## Belangrijkste Lessen

1. **Wees Specifiek**: Geef volledige context en duidelijke instructies
2. **Kies Juiste Agent**: Match expertise met taak requirements
3. **Gebruik reset: "true"**: Schone context = betere resultaten
4. **Geef Context**: Sub-agent heeft GEEN eerdere conversatie geschiedenis
5. **Definieer Output**: Zeg wat je terug verwacht
6. **Android Features**: Gebruik notifications, TTS, GPS waar relevant
7. **Error Handling**: Instrueer sub-agent hoe met fouten om te gaan

---

## Volgende Stappen

1. **Experimenteer**: Probeer de oefeningen hierboven
2. **Start Klein**: Begin met simpele delegatie, bouw op naar complex
3. **Gebruik Template**: Copy/paste de delegatie template en vul in
4. **Leer van Fouten**: Als delegatie faalt, analyseer waarom
5. **Bouw Library**: Sla succesvolle delegatie patterns op in memory

**Sub-agents zijn krachtig wanneer gebruikt met precisie en doel!**

---

*Laatst bijgewerkt: 2025-11-29*
*Agent Zero v3.0 on Android/Termux*
