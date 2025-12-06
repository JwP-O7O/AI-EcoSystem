# Nieuwe Tool Prompt Templates

**Aangemaakt op:** 2025-11-29
**Locatie:** `/data/data/com.termux/files/home/AI-EcoSystem/agent-zero/prompts/default/`

## Overzicht

Er zijn **4 complete prompt templates** gecreëerd voor de nieuwe tools die recent zijn geïmplementeerd in Agent Zero. Elk template volgt de gestandaardiseerde structuur en bevat uitgebreide documentatie.

---

## 1. Task Planner Tool Template

**Bestand:** `agent.system.tool.task_planner.md`
**Grootte:** 5.8 KB (191 regels)

### Functionaliteit
Intelligente taakplanning en decompositie voor complexe taken. Analyseert complexiteit, breekt taken op in subtaken, maakt dependency graphs en tracked voortgang.

### Belangrijkste Features
- **5 Operaties:** create, update, status, complete, replan
- **Task Analysis:** Complexiteit (low/medium/high/very-high)
- **Subtask Decomposition:** Geordende lijst met dependencies
- **Resource Estimates:** Tools needed, geschatte stappen
- **Success Criteria:** Duidelijke doelen
- **Risk Assessment:** Potentiële blockers en mitigatie

### Use Cases
- Complexe multi-step taken (>5 stappen)
- Taken met dependencies
- Long-running projecten
- Onbekende domeinen
- Team coördinatie met subordinate agents

### Voorbeeld Workflow
```json
// 1. Create plan
{"action": "create", "task": "...", "context": "..."}

// 2. Update progress
{"action": "update", "task_id": "...", "updates": {...}}

// 3. Adapt when blocked
{"action": "replan", "task_id": "...", "reason": "..."}

// 4. Complete
{"action": "complete", "task_id": "..."}
```

---

## 2. Code Analyzer Tool Template

**Bestand:** `agent.system.tool.code_analyzer.md`
**Grootte:** 8.2 KB (302 regels)

### Functionaliteit
Geavanceerde statische code-analyse met security scanning, complexity metrics en quality assessment. Ondersteunt Python (AST-based) en JavaScript.

### Belangrijkste Features
- **5 Operaties:** analyze, security, complexity, dependencies, quality
- **AST Parsing:** Python en JavaScript (pattern-based)
- **Security Scan:** SQL injection, command injection, hardcoded secrets, eval usage
- **Complexity Analysis:** Cyclomatic complexity per functie
- **Quality Score:** 0-100 met gedetailleerde feedback

### Detecties
**Security Patterns:**
- SQL Injection risico's
- Command injection (os.system, subprocess)
- Hardcoded secrets (passwords, API keys)
- Dangerous eval/exec usage
- Unsafe pickle usage

**Code Issues:**
- Bare except clauses
- Lange functies (>50 regels)
- Teveel parameters (>5)
- Hoge complexity (>20)
- Code smells

### Complexity Ratings
- **Simple (1-5):** Easy to maintain
- **Moderate (6-10):** Manageable
- **Complex (11-20):** Consider refactoring
- **Very Complex (21+):** Refactor immediately

### Voorbeeld Workflow
```json
// 1. Full analysis
{"action": "analyze", "file_path": "/path/to/code.py"}

// 2. Security scan
{"action": "security", "file_path": "/path/to/api.py"}

// 3. Complexity check
{"action": "complexity", "file_path": "/path/to/module.py"}

// 4. Quality score
{"action": "quality", "file_path": "/path/to/code.py"}
```

---

## 3. Vision Tool Template

**Bestand:** `agent.system.tool.vision.md`
**Grootte:** 11 KB (411 regels)

### Functionaliteit
Image analysis en understanding via vision-enabled LLMs (GPT-4 Vision, Gemini Vision, Claude 3). Analyseert screenshots, diagrammen, charts, extraheert tekst via OCR.

### Belangrijkste Features
- **5 Operaties:** analyze, ocr, describe, compare, screenshot
- **Model Support:** GPT-4V, Gemini Vision, Claude 3
- **OCR Capabilities:** Text extractie met pytesseract fallback
- **Image Comparison:** Before/after analysis
- **Context-Aware:** Screenshot analysis met context

### Use Cases
**Debugging:**
- Error screenshots analyseren
- UI rendering issues
- Visual glitches
- Console output screenshots

**Documentation:**
- Architecture diagrammen begrijpen
- Flowcharts interpreteren
- API documentation images
- Code uit screenshots extraheren

**Data Analysis:**
- Charts en graphs lezen
- Data uit tabellen extraheren
- Infographics begrijpen

**Quality Assurance:**
- Visual regression testing
- Before/after vergelijkingen
- Pixel-perfect implementaties checken

### Model-Specific Features
- **GPT-4 Vision:** Excellent detailed analysis, code reading
- **Gemini Vision:** Fast processing, multilingual OCR
- **Claude 3:** Detailed descriptions, strong reasoning

### Voorbeeld Workflow
```json
// 1. Analyze error screenshot
{"action": "analyze", "image_path": "/error.png",
 "prompt": "What error is shown and what's the cause?"}

// 2. Extract text (OCR)
{"action": "ocr", "image_path": "/code_screenshot.png"}

// 3. Analyze UI
{"action": "screenshot", "image_path": "/ui.png",
 "context": "User reports button not visible"}

// 4. Compare versions
{"action": "compare",
 "image_path_1": "/before.png",
 "image_path_2": "/after.png"}
```

---

## 4. Batch Executor Tool Template

**Bestand:** `agent.system.tool.batch_executor.md`
**Grootte:** 4.0 KB (161 regels)

### Functionaliteit
Parallel task processing systeem voor efficiënte batch operaties. Queue management, priority scheduling, progress tracking en result aggregation.

### Belangrijkste Features
- **9 Operaties:** add, add_batch, start, stop, status, results, export, clear, cancel
- **Priority Levels:** CRITICAL, HIGH, MEDIUM, LOW
- **Task Status:** QUEUED, RUNNING, COMPLETED, FAILED, CANCELLED
- **Parallel Execution:** 5x+ snelheidswinst met concurrent processing
- **Progress Tracking:** Real-time status updates
- **Export Formats:** JSON, CSV

### Use Cases
**File Processing:**
- Analyze multiple code files
- Bulk image processing
- Security scan codebase
- Generate reports

**Data Operations:**
- Parallel API calls
- Database record processing
- Batch transformations
- Multiple validations

**Performance Benefit:**
```
Sequential:  10 tasks × 5 sec = 50 seconds
Parallel:    10 tasks ÷ 5 × 5 sec = 10 seconds (5x faster!)
```

### Best Practices
1. **Concurrency Settings:**
   - CPU-intensive: 4-8 concurrent
   - I/O-intensive: 10-20 concurrent
   - API calls: 5-10 concurrent

2. **Priority Usage:**
   - CRITICAL: Authentication/security
   - HIGH: Important features
   - MEDIUM: Normal tasks
   - LOW: Nice-to-have

3. **Error Handling:**
   - Set max_retries for flaky operations
   - Monitor failed tasks
   - Export results for analysis

### Voorbeeld Workflow
```json
// 1. Add batch tasks
{"action": "add_batch", "tasks": [...]}

// 2. Start processing
{"action": "start", "max_concurrent": 5, "timeout": 300}

// 3. Monitor progress
{"action": "status", "detailed": true}

// 4. Get results
{"action": "results", "format": "summary"}

// 5. Export
{"action": "export", "format": "json", "output_file": "/results.json"}

// 6. Clean up
{"action": "clear"}
```

---

## Template Structuur

Alle templates volgen dezelfde consistente structuur:

1. **Tool Beschrijving** (1-2 zinnen)
2. **Operaties/Actions** met JSON voorbeelden
3. **Input Parameters** met uitleg
4. **Output Format** beschrijving
5. **Use Cases** (3-5 praktische voorbeelden)
6. **Best Practices** sectie
7. **Complete Workflow Voorbeelden**
8. **Error Handling** guidance
9. **Tips & Limitations**
10. **Integration Examples** met andere tools

## Format Kenmerken

- **Markdown Format:** Duidelijk en actionable
- **JSON Examples:** Alle voorbeelden met "thoughts" field
- **Praktijkgericht:** Real-world use cases
- **Complete:** Van basics tot advanced gebruik
- **Consistent:** Zelfde structuur als bestaande templates

## Integratie met Agent Zero

Deze templates worden automatisch geladen door Agent Zero's prompt systeem en zijn beschikbaar voor de agent tijdens conversaties. De agent kan deze templates gebruiken om:

1. Correct tool gebruik te begrijpen
2. Juiste parameters te kiezen
3. Best practices te volgen
4. Complexe workflows te implementeren
5. Errors te voorkomen

## Verificatie

Alle templates zijn aangemaakt en geverifieerd:

```bash
ls -lh /data/data/com.termux/files/home/AI-EcoSystem/agent-zero/prompts/default/agent.system.tool.{task_planner,code_analyzer,vision,batch_executor}.md
```

Output:
```
-rw-------  4.0K  agent.system.tool.batch_executor.md
-rw-------  8.2K  agent.system.tool.code_analyzer.md
-rw-------  5.8K  agent.system.tool.task_planner.md
-rw------- 11.0K  agent.system.tool.vision.md
```

**Totaal:** ~29 KB aan uitgebreide tool documentatie (1065 regels)

## Volgende Stappen

1. **Testen:** Probeer elke tool uit met de voorbeelden in de templates
2. **Feedback:** Pas templates aan op basis van praktijkervaring
3. **Uitbreiden:** Voeg meer voorbeelden toe waar nodig
4. **Integreren:** Zorg dat tools correct geregistreerd zijn in Agent Zero

## Conclusie

Alle gevraagde prompt templates zijn succesvol aangemaakt met:
- Duidelijke beschrijvingen
- Uitgebreide voorbeelden
- Best practices
- Praktische use cases
- Error handling guidance
- Integratie met andere tools

De templates zijn production-ready en volgen de Agent Zero standaarden.
