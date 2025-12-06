# Specialized Agents voor Claude Code

Deze directory bevat de **Claude Code adaptatie** van de Agent Zero specialized agents.

## 📖 Wat is Dit?

De originele specialized agents zijn gebouwd voor het **Agent Zero framework**, dat werkt met custom prompts en subordinate agents. Claude Code werkt anders - het heeft voorgedefinieerde agents via de Task tool.

Deze conversie brengt de **concepten** van specialized agents naar Claude Code via **slash commands**.

## 🔄 Conversie Strategie

### Agent Zero → Claude Code Mapping

| Agent Zero Concept | Claude Code Equivalent |
|-------------------|------------------------|
| `call_subordinate` | Slash commands (`/code`, `/research`, etc.) |
| `code_execution_tool` | `Bash` tool voor terminal/code executie |
| `knowledge_tool` | `WebSearch` + `WebFetch` tools |
| `memory_save/load` | File storage met `Write`/`Read` tools |
| `webpage_content_tool` | `WebFetch` tool |
| Custom role prompts | Slash command prompts |

### Tool Mapping Details

**Agent Zero** → **Claude Code**
- `runtime: "python"` → `Bash` met python command
- `runtime: "terminal"` → `Bash` tool
- `memory_save` → `Write` naar .memory/ directory
- `memory_load` → `Grep` in .memory/ directory
- `knowledge_tool` → `WebSearch` voor zoeken, `WebFetch` voor specifieke pagina's

## 📁 Beschikbare Slash Commands

Alle commands bevinden zich in `/.claude/commands/`:

### Core Specialists
- **`/code`** - Code Execution Specialist
  - Python, JavaScript, terminal commando's
  - Package management, debugging

- **`/research`** - Knowledge Research Specialist
  - Online research, documentatie zoeken
  - Best practices, library discovery

- **`/scrape`** - Web Content Extraction Specialist
  - Web scraping, HTML parsing
  - Data extractie en structurering

### Strategic Agents
- **`/architect`** - Solution Architecture Specialist
  - Complexe probleem analyse
  - Systeem ontwerp, strategische planning

- **`/orchestrate`** - Task Delegation Orchestrator
  - Task decompositie
  - Multi-agent workflow coördinatie

- **`/master`** - Master Orchestrator
  - Algemene coördinatie
  - Complete workflows van A tot Z

### Helper
- **`/agents`** - Overzicht van alle agents
  - Quick reference guide
  - Gebruik voorbeelden

## 🚀 Hoe Te Gebruiken

### Basis Gebruik

1. **Direct een specialist aanroepen**:
   ```
   /code

   Schrijf een Python script dat een CSV file inleest
   ```

2. **Master Orchestrator voor complexe taken**:
   ```
   /master

   Bouw een web scraper die data opslaat in een database
   ```

3. **Architect voor planning**:
   ```
   /architect

   Ontwerp een scalable notification systeem
   ```

### Gecombineerd Gebruik

Specialists kunnen elkaar aanvullen:

```bash
# Stap 1: Research
/research
Wat is de beste Python library voor async HTTP requests?

# Stap 2: Design
/architect
Ontwerp een systeem dat deze library gebruikt voor rate-limited API calls

# Stap 3: Implement
/code
Implementeer het ontworpen systeem
```

### Via Master Orchestrator

De Master Orchestrator kan automatisch de juiste specialists inzetten:

```bash
/master

Taak: Bouw een complete web scraping pipeline:
1. Scrape product data van e-commerce sites
2. Clean en valideer de data
3. Sla op in SQLite database
4. Genereer dagelijks rapport

De master zal automatisch:
- /research gebruiken voor beste scraping libraries
- /architect voor systeem ontwerp
- /code voor implementatie
- /orchestrate voor coördinatie
```

## 🎯 Best Practices

### 1. Kies de Juiste Specialist

| Wanneer | Gebruik |
|---------|---------|
| Code schrijven | `/code` |
| Info zoeken | `/research` |
| Website scrapen | `/scrape` |
| Systeem ontwerpen | `/architect` |
| Grote taak coördineren | `/orchestrate` |
| Complete workflow | `/master` |

### 2. Wees Specifiek

❌ **Slecht**: "Maak een API"
✅ **Goed**: "Maak een REST API met Flask die user data uit PostgreSQL haalt, met JWT auth"

### 3. Geef Context

Elke specialist werkt beter met context:
- Wat is het doel?
- Welke constraints zijn er?
- Wat is het verwachte resultaat?
- Zijn er specifieke requirements?

### 4. Combineer Waar Nuttig

Gebruik meerdere specialists voor complexe taken:
1. `/research` - Vind beste aanpak
2. `/architect` - Ontwerp de oplossing
3. `/code` - Implementeer
4. `/orchestrate` - Coördineer alles

## ⚠️ Belangrijke Verschillen met Agent Zero

### Wat NIET werkt zoals in Agent Zero:

1. **Geen Persistent Memory**
   - Agent Zero heeft `memory_save/load` met vector database
   - Claude Code: gebruik file storage of documentatie

2. **Geen Subordinate Agents met State**
   - Agent Zero: subordinates behouden context
   - Claude Code: elke slash command is een fresh start

3. **Geen Automatische Tool Selection**
   - Agent Zero: agents kiezen zelf tools
   - Claude Code: tools worden bewust gekozen in prompt

4. **Geen Hierarchical Numbering**
   - Agent Zero: Agent 0 → Agent 1 → Agent 2
   - Claude Code: flat structure met slash commands

### Wat WEL werkt:

✅ Gespecialiseerde expertise per domein
✅ Task decompositie en delegatie
✅ Code execution en testing
✅ Web research en scraping
✅ Solution architecture en planning

## 📚 Voorbeelden

Zie `EXAMPLES.md` voor gedetailleerde gebruiksvoorbeelden.

## 🔗 Originele Bronnen

De originele Agent Zero prompts staan in:
```
/data/data/com.termux/files/home/AI-EcoSystem/prompts/specialized-agents/
```

Documentatie:
- `README.md` - Algemene uitleg
- `QUICK_START.md` - Quick start guide
- `role.*.md` - Individuele role definities

## 🤝 Contributing

Wil je een specialist toevoegen of verbeteren?

1. Maak een nieuwe `.md` file in `/.claude/commands/`
2. Gebruik bestaande commands als template
3. Test grondig
4. Update deze README

## 📝 License

Volgt dezelfde licentie als het AI-EcoSystem project.
