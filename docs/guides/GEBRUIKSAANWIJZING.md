# 🤖 Specialized Agents - Gebruiksaanwijzing

**Welkom!** Je hebt nu toegang tot 6 gespecialiseerde AI agents in Claude Code.

Deze agents zijn geconverteerd van het Agent Zero framework en werken via **slash commands**.

---

## 🚀 Quick Start (3 minuten)

### Stap 1: Verifieer Installatie

De agents zijn geïnstalleerd in:
```bash
/data/data/com.termux/files/home/AI-EcoSystem/.claude/commands/
```

Controleer:
```bash
ls /data/data/com.termux/files/home/AI-EcoSystem/.claude/commands/
```

Je zou moeten zien:
- `agents.md` - Helper overzicht
- `architect.md` - Solution Architect
- `code.md` - Code Specialist
- `master.md` - Master Orchestrator
- `orchestrate.md` - Task Orchestrator
- `research.md` - Research Specialist
- `scrape.md` - Web Scraper

---

### Stap 2: Configureer Claude Code

Claude Code moet weten waar je slash commands staan:

**Optie A: Automatisch** (als je in de AI-EcoSystem directory bent):
```bash
cd /data/data/com.termux/files/home/AI-EcoSystem
# Claude Code detecteert automatisch .claude/commands/
```

**Optie B: Handmatig** (als commands niet werken):
Zorg dat je `claude` command draait vanuit de AI-EcoSystem directory.

---

### Stap 3: Test Een Agent

Probeer dit in Claude Code:

```bash
/agents
```

Dit toont je een overzicht van alle beschikbare agents.

Probeer nu een specialist:

```bash
/code

Schrijf een simpel Python script dat "Hello, World!" print
```

**Werkt het?** ✅ Je bent klaar!
**Werkt het niet?** ⚠️ Zie de Troubleshooting sectie hieronder.

---

## 📚 Beschikbare Agents

### 1. 🎯 `/master` - Master Orchestrator
**Wanneer gebruiken**: Voor complete workflows van A tot Z

**Wat doet het**:
- Analyseert je taak volledig
- Plant de aanpak
- Delegeert aan de juiste specialists
- Consolideert resultaten
- Rapporteert compleet

**Voorbeeld**:
```
/master

Bouw een web scraper die product prijzen vergelijkt van 3 websites,
opslaat in database, en een dagelijks rapport genereert
```

---

### 2. 💻 `/code` - Code Execution Specialist
**Wanneer gebruiken**: Als je code moet schrijven of uitvoeren

**Wat doet het**:
- Schrijft Python/JavaScript code
- Voert code uit en test
- Installeert packages (pip, npm)
- Debug errors
- File operations

**Voorbeeld**:
```
/code

Schrijf een Python script dat:
1. CSV file inleest
2. Top 10 rijen met hoogste waarde in kolom 'sales' vindt
3. Resultaat print
```

---

### 3. 🔍 `/research` - Knowledge Research Specialist
**Wanneer gebruiken**: Als je online informatie moet zoeken

**Wat doet het**:
- Zoekt online naar informatie
- Vindt beste libraries/tools
- Zoekt documentatie
- Fact-checking
- Best practices

**Voorbeeld**:
```
/research

Wat is de beste Python library voor async HTTP requests
met retry logic en rate limiting?
```

---

### 4. 🌐 `/scrape` - Web Scraper Specialist
**Wanneer gebruiken**: Als je data van websites moet halen

**Wat doet het**:
- Scrapet webpagina's
- Extraheert specifieke data
- Parseert HTML
- Structureert data
- Filtert relevante content

**Voorbeeld**:
```
/scrape

URL: https://example.com/products
Doel: Extraheer alle product namen en prijzen
```

---

### 5. 🏗️ `/architect` - Solution Architect
**Wanneer gebruiken**: Voor complexe systeem ontwerp en planning

**Wat doet het**:
- Analyseert complexe problemen
- Ontwerpt system architectuur
- Plant implementatie stappen
- Identificeert risico's
- Adviseert best practices

**Voorbeeld**:
```
/architect

Ontwerp een scalable notification systeem dat:
- 10,000+ users ondersteunt
- Real-time push notifications
- Email backup
- User preferences
- PostgreSQL database
```

---

### 6. 🎭 `/orchestrate` - Task Orchestrator
**Wanneer gebruiken**: Voor multi-step workflows met verschillende specialists

**Wat doet het**:
- Splitst grote taken op
- Delegeert aan juiste specialists
- Coördineert workflow
- Consolideert resultaten
- Verifieert alles werkt samen

**Voorbeeld**:
```
/orchestrate

Complete pipeline:
1. Scrape data van 3 websites
2. Clean en validate data
3. Analyse en compare
4. Save naar database
5. Genereer rapport
```

---

### 7. ℹ️ `/agents` - Helper
**Wanneer gebruiken**: Als je niet zeker weet welke agent te gebruiken

**Wat doet het**:
- Toont alle agents
- Geeft voorbeelden
- Quick decision guide

---

## 🎯 Welke Agent Gebruiken? (Decision Tree)

```
Wil je...

├─ Code schrijven/uitvoeren?
│  └─> /code
│
├─ Iets opzoeken online?
│  └─> /research
│
├─ Data van website halen?
│  └─> /scrape
│
├─ Complex systeem ontwerpen?
│  └─> /architect
│
├─ Grote taak opdelen en coördineren?
│  └─> /orchestrate
│
└─ Complete workflow van A tot Z?
   └─> /master
```

---

## 💡 Best Practices

### 1. Wees Specifiek

❌ **Slecht**:
```
/code
Maak een API
```

✅ **Goed**:
```
/code

Maak een REST API met Flask:
- Endpoint: GET /users (lijst van users)
- Endpoint: POST /users (create user)
- SQLite database
- Input validatie
- Error handling
```

---

### 2. Geef Context

Vertel altijd:
- **Wat** wil je bereiken?
- **Waarom** is dit nodig? (higher-level doel)
- **Welke** constraints zijn er? (tech stack, budget, etc.)
- **Hoe** ziet succes eruit? (success criteria)

**Voorbeeld**:
```
/architect

CONTEXT: Ik bouw een e-commerce platform

PROBLEEM: Real-time inventory updates tussen warehouse en webshop

CONSTRAINTS:
- Python backend
- PostgreSQL database
- Must handle 1000+ products
- Budget: opensource only

DOEL: Ontwerp systeem voor real-time sync
```

---

### 3. Combineer Agents

Voor complexe projecten, gebruik meerdere agents:

**Workflow Voorbeeld**:
```bash
# Stap 1: Research
/research
Beste Python library voor PDF generatie met charts?

# Stap 2: Design
/architect
Ontwerp een rapport systeem met de gekozen library

# Stap 3: Implement
/code
Implementeer het ontworpen rapport systeem

# Stap 4: Test
/code
Test het systeem met sample data
```

**Of gebruik Master voor auto-coördinatie**:
```bash
/master

Complete project: PDF rapport generator
Research → Design → Implement → Test
```

---

### 4. Iteratief Werken

Je kunt stap voor stap bouwen:

```bash
# Iteratie 1: Basic
/code
Maak basic Flask API met 1 endpoint

# Iteratie 2: Auth
/code
Voeg JWT authentication toe aan de API

# Iteratie 3: Database
/code
Voeg SQLite database toe

# Iteratie 4: Validation
/code
Voeg input validatie toe
```

---

## 📖 Praktische Voorbeelden

### Voorbeeld 1: Data Processing

**Scenario**: CSV data analyseren en visualiseren

```bash
/master

Taak: Analyseer sales data

Ik heb een CSV file 'sales_2024.csv' met kolommen:
- date, product, quantity, price, region

Ik wil:
1. Data inlezen en cleanen
2. Bereken totale sales per product
3. Bereken totale sales per region
4. Maak bar charts
5. Genereer HTML rapport

Lever werkend script met output.
```

---

### Voorbeeld 2: Web Scraping

**Scenario**: Product prijzen vergelijken

```bash
/orchestrate

Taak: Price comparison scraper

Scrape product prijzen van:
- example-shop-1.com/laptops
- example-shop-2.com/laptops
- example-shop-3.com/laptops

Voor elk product extract:
- Naam
- Prijs
- Specs (als beschikbaar)

Vergelijk prijzen en vind beste deal.
Sla resultaat op in SQLite database.
Genereer comparison tabel.
```

---

### Voorbeeld 3: API Development

**Scenario**: REST API bouwen

```bash
/master

Bouw een complete REST API voor todo app:

Requirements:
- CRUD endpoints voor todos
- User authentication (JWT)
- SQLite database met SQLAlchemy
- Input validatie
- Error handling
- Tests

Tech stack:
- Flask
- SQLAlchemy
- PyJWT
- Pytest voor tests

Lever production-ready API met documentatie.
```

---

### Voorbeeld 4: Research & Implementation

**Scenario**: Nieuwe functionaliteit toevoegen

```bash
# Stap 1: Research
/research

Ik moet rate limiting toevoegen aan mijn Flask API.
Wat is de beste aanpak?

Zoek naar:
- Best practices
- Libraries (Flask extensions)
- Implementatie voorbeelden
- Configuratie opties (requests per minute, etc.)

# Stap 2: Implement (na research results)
/code

Implementeer rate limiting met [chosen library]:
- 100 requests per minute per IP
- Custom error message bij limit
- Whitelist voor localhost
- Test met script
```

---

## 🐛 Troubleshooting

### Probleem: Slash command niet herkend

**Symptoom**: `/code` doet niets of error

**Oplossing**:
1. Controleer of je in de juiste directory bent:
   ```bash
   pwd
   # Moet zijn: .../AI-EcoSystem of subdirectory
   ```

2. Verifieer .claude/commands bestaat:
   ```bash
   ls /data/data/com.termux/files/home/AI-EcoSystem/.claude/commands/
   ```

3. Herstart Claude Code in de AI-EcoSystem directory

---

### Probleem: Agent doet niet wat ik verwacht

**Symptoom**: Output is niet relevant

**Oplossing**:
1. Wees specifieker in je instructies
2. Geef meer context
3. Gebruik een andere specialist (misschien verkeerde keuze)
4. Probeer `/agents` voor guidance

---

### Probleem: Agent zegt dat tools niet beschikbaar zijn

**Symptoom**: "I don't have access to that tool"

**Oplossing**:
Dit is normaal - slash commands zijn prompts, geen echte tools.
De agent zal wel zijn best doen met beschikbare Claude Code tools.

---

## 📁 Bestandsstructuur

Na installatie heb je:

```
AI-EcoSystem/
├── .claude/
│   ├── commands/           # Slash commands (agents)
│   │   ├── agents.md
│   │   ├── architect.md
│   │   ├── code.md
│   │   ├── master.md
│   │   ├── orchestrate.md
│   │   ├── research.md
│   │   └── scrape.md
│   └── agents/            # Documentatie
│       ├── README.md
│       └── EXAMPLES.md
├── prompts/
│   └── specialized-agents/  # Originele Agent Zero prompts
│       ├── role.*.md
│       ├── README.md
│       └── QUICK_START.md
└── GEBRUIKSAANWIJZING.md   # Dit bestand
```

---

## 🎓 Leerpad

### Week 1: Basics
- Gebruik `/agents` om overzicht te krijgen
- Probeer `/code` voor simpele scripts
- Probeer `/research` voor info zoeken
- Experimenteer met verschillende taken

### Week 2: Intermediate
- Probeer `/architect` voor planning
- Gebruik `/orchestrate` voor multi-step taken
- Combineer specialists (research → code)
- Build complete mini-projecten

### Week 3: Advanced
- Gebruik `/master` voor complete workflows
- Bouw complexe multi-component systemen
- Optimaliseer je prompts voor betere results
- Maak eigen workflows

---

## 🔗 Meer Resources

### Documentatie
```bash
# Algemene info
cat /data/data/com.termux/files/home/AI-EcoSystem/.claude/agents/README.md

# Voorbeelden
cat /data/data/com.termux/files/home/AI-EcoSystem/.claude/agents/EXAMPLES.md

# Originele Agent Zero docs
cat /data/data/com.termux/files/home/AI-EcoSystem/prompts/specialized-agents/QUICK_START.md
```

### In Claude Code
```bash
# Overzicht van agents
/agents

# Specifieke agent gebruiken
/code
/research
/scrape
/architect
/orchestrate
/master
```

---

## ❓ Veelgestelde Vragen

**Q: Kan ik eigen agents toevoegen?**
A: Ja! Maak een nieuwe .md file in `.claude/commands/` met je custom prompt.

**Q: Werken deze agents zoals Agent Zero?**
A: Niet precies. Het zijn conceptuele conversies. Agent Zero heeft features zoals persistent memory die Claude Code niet heeft.

**Q: Welke agent is het beste?**
A: Hangt af van je taak. Gebruik `/agents` voor decision guide.

**Q: Kan ik meerdere agents tegelijk gebruiken?**
A: Nee, slash commands werken sequentieel. Gebruik `/master` of `/orchestrate` voor automatische multi-agent workflows.

**Q: Hoe kan ik een agent stoppen?**
A: Agents zijn prompts, geen processen. Ze stoppen automatisch na hun taak.

---

## 🤝 Hulp Nodig?

1. **Eerst proberen**: `/agents` voor quick reference
2. **Documentatie**: Lees EXAMPLES.md voor praktische voorbeelden
3. **Experimenteer**: Probeer verschillende agents met kleine taken

---

## 🎉 Success Tips

1. **Start klein**: Begin met simpele taken
2. **Wees specifiek**: Hoe duidelijker je vraag, hoe beter het resultaat
3. **Geef context**: Vertel waarom en wat je wilt bereiken
4. **Itereer**: Bouw stap voor stap op
5. **Combineer**: Gebruik meerdere specialists voor complexe taken
6. **Leer**: Elke interactie maakt je beter in het gebruiken van agents

---

**Veel succes met je Specialized Agents! 🚀**

Vragen? Probeer `/agents` of lees de documentatie in `.claude/agents/`
