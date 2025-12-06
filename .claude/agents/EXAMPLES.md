# Specialized Agents - Gebruiksvoorbeelden

Dit document bevat praktische voorbeelden van hoe je de specialized agents gebruikt.

## 📋 Inhoudsopgave

1. [Code Execution Specialist](#code-execution-specialist)
2. [Knowledge Research Specialist](#knowledge-research-specialist)
3. [Web Scraper Specialist](#web-scraper-specialist)
4. [Solution Architect](#solution-architect)
5. [Task Orchestrator](#task-orchestrator)
6. [Master Orchestrator](#master-orchestrator)
7. [Complexe Workflows](#complexe-workflows)

---

## Code Execution Specialist

### Voorbeeld 1: Python Script Schrijven

**Commando**:
```bash
/code
```

**Taak**:
```
Schrijf een Python script dat:
1. Een CSV file 'sales.csv' inleest
2. De top 10 producten met hoogste verkoop berekent
3. Een bar chart maakt met matplotlib
4. De chart opslaat als 'top_products.png'

Requirements:
- Gebruik pandas voor data processing
- Error handling voor file not found
- Print summary statistics
```

**Verwacht Gedrag**:
- Installeert pandas en matplotlib indien nodig
- Schrijft het script
- Voert het uit en test
- Rapporteert resultaat met output

---

### Voorbeeld 2: Debugging Bestaande Code

**Commando**:
```bash
/code
```

**Taak**:
```
Fix de error in /path/to/script.py:

Error: TypeError: unsupported operand type(s) for +: 'int' and 'str'

Analyseer het probleem, fix it, en test dat het werkt.
```

---

## Knowledge Research Specialist

### Voorbeeld 1: Library Research

**Commando**:
```bash
/research
```

**Vraag**:
```
Wat is de beste Python library voor:
- Asynchrone HTTP requests
- Built-in retry logic met exponential backoff
- Rate limiting support
- Goed gedocumenteerd
- Actief onderhouden

Geef voor de top 3 opties:
- Library naam
- Voor/nadelen
- Code voorbeeld van basic gebruik
- Installatie commando
```

---

### Voorbeeld 2: Error Message Oplossen

**Commando**:
```bash
/research
```

**Vraag**:
```
Ik krijg deze error in Python:

"SSL: CERTIFICATE_VERIFY_FAILED"

Wat zijn de oorzaken en hoe fix ik dit?
Geef meerdere oplossingen (development vs production safe).
```

---

### Voorbeeld 3: Best Practices

**Commando**:
```bash
/research
```

**Vraag**:
```
Wat zijn de best practices voor:
- API rate limiting in Python
- Inclusief retry logic
- Error handling
- Logging

Geef concrete code voorbeelden en library aanbevelingen.
```

---

## Web Scraper Specialist

### Voorbeeld 1: API Documentation Scrapen

**Commando**:
```bash
/scrape
```

**Taak**:
```
URL: https://docs.python-requests.org/en/latest/

Doel:
Extraheer alle API methods van de requests library met:
- Method naam
- Parameters
- Return type
- Korte beschrijving

Presenteer als gestructureerde lijst of JSON.
```

---

### Voorbeeld 2: Pricing Information

**Commando**:
```bash
/scrape
```

**Taak**:
```
URL: https://example.com/pricing

Extraheer:
- Alle pricing tiers (namen)
- Prijs per tier
- Features per tier
- Beperkingen (limits)

Maak een comparison tabel.
```

---

## Solution Architect

### Voorbeeld 1: Systeem Ontwerp

**Commando**:
```bash
/architect
```

**Probleem**:
```
Ontwerp een scalable real-time notification systeem voor een web app:

Requirements:
- 10,000+ concurrent users
- Push notifications naar browser
- Email notifications als backup
- Persistence van notificaties
- User preferences (welke notificaties ontvangen)

Constraints:
- Python backend (Flask/Django)
- PostgreSQL database
- Budget-vriendelijk (opensource preferred)

Lever:
1. High-level architectuur diagram (text-based)
2. Component beschrijvingen
3. Data flow
4. Technology stack recommendations
5. Implementatie plan (stappen)
6. Potentiële challenges en oplossingen
```

---

### Voorbeeld 2: Performance Optimalisatie Strategie

**Commando**:
```bash
/architect
```

**Probleem**:
```
Ons Python API is traag:
- Database queries duren >2 seconden
- API response time >5 seconden
- 100 requests/min current load
- Target: <500ms response time

Analyseer mogelijke bottlenecks en ontwerp optimalisatie strategie:
1. Database optimalisaties
2. Caching strategie
3. Code optimalisaties
4. Infrastructure changes

Prioriteer op impact vs effort.
```

---

## Task Orchestrator

### Voorbeeld 1: Multi-Step Workflow

**Commando**:
```bash
/orchestrate
```

**Taak**:
```
Bouw een automated data pipeline:

Stappen:
1. Scrape product data van 3 e-commerce websites
2. Clean en normalize de data
3. Vergelijk prijzen en features
4. Sla resultaten op in SQLite database
5. Genereer HTML rapport met charts
6. Email het rapport (save to file for now)

Coördineer alle stappen en zorg dat ze correct integreren.
```

**Verwacht Gedrag**:
Orchestrator zal:
1. `/scrape` gebruiken voor web scraping
2. `/code` voor data cleaning
3. `/code` voor database operaties
4. `/code` voor rapport generatie
5. Consolideren en verifiëren

---

### Voorbeeld 2: Research + Implementation

**Commando**:
```bash
/orchestrate
```

**Taak**:
```
Complete workflow:

1. Research beste library voor PDF generatie in Python
2. Ontwerp een template systeem voor rapportages
3. Implementeer PDF generator met:
   - Company logo
   - Tables met data
   - Charts (matplotlib)
   - Page numbers
4. Test met sample data
5. Documenteer gebruik

Coördineer het hele proces van research tot working implementation.
```

---

## Master Orchestrator

### Voorbeeld 1: Complete Feature Development

**Commando**:
```bash
/master
```

**Taak**:
```
Ik wil een user authentication systeem toevoegen aan mijn Flask app:

Requirements:
- User registration met email verificatie
- Login/logout
- Password reset functionaliteit
- JWT tokens voor API auth
- SQLAlchemy models
- Route protection decorators

Start vanaf research, ontwerp de architectuur, implementeer, en test.
Geef me een volledig werkend systeem.
```

**Verwacht Gedrag**:
Master zal:
1. Analyseren van requirements
2. `/research` - Beste libraries vinden (Flask-Login, PyJWT, etc.)
3. `/architect` - Systeem ontwerp maken
4. `/code` - Implementatie van alle componenten
5. `/code` - Tests schrijven en uitvoeren
6. Consolideren en rapporteren

---

### Voorbeeld 2: Problem Solving

**Commando**:
```bash
/master
```

**Probleem**:
```
Mijn Docker container voor Python app start niet:

Error:
"ModuleNotFoundError: No module named 'flask'"

Maar flask staat wel in requirements.txt

Debug en fix dit probleem. Verifieer dat het werkt.
```

**Verwacht Gedrag**:
1. Analyse van het probleem
2. Check Dockerfile en requirements.txt
3. Identificeer root cause
4. Fix (waarschijnlijk pip install timing issue)
5. Test de oplossing
6. Rapporteer met uitleg

---

## Complexe Workflows

### Workflow 1: API Development (Complete)

```bash
/master

Bouw een complete REST API voor een todo app:

Features:
- CRUD operaties voor todos
- User authentication (JWT)
- SQLite database
- Input validatie
- Error handling
- API documentatie (OpenAPI/Swagger)
- Unit tests
- Docker container

Lever een production-ready API met:
- Clean code structure
- Documentatie
- Tests
- Deployment instructies
```

---

### Workflow 2: Data Analysis Pipeline

**Stap 1 - Research**:
```bash
/research

Beste Python libraries voor:
- CSV/Excel processing (grote files, >1GB)
- Data cleaning en validation
- Statistical analysis
- Visualization (interactive charts)
```

**Stap 2 - Architect**:
```bash
/architect

Op basis van de research results, ontwerp een data pipeline voor:

Input: Multiple CSV files met sales data
Process:
- Data cleaning (duplicates, missing values)
- Aggregation (per product, per region, per month)
- Statistical analysis (trends, outliers)
- Visualization (interactive dashboard)
Output: HTML dashboard + PDF rapport

Ontwerp de architectuur en flow.
```

**Stap 3 - Implement**:
```bash
/orchestrate

Implementeer de ontworpen data pipeline:

1. CSV readers en validators
2. Data cleaning functions
3. Analysis modules
4. Visualization generators
5. Dashboard builder
6. PDF export

Coördineer alle componenten en zorg voor integratie.
```

**Stap 4 - Test & Verify**:
```bash
/code

Test de complete pipeline met sample data:
- Create test CSV files
- Run pipeline
- Verify outputs
- Check for errors
- Generate final report
```

---

### Workflow 3: Web Scraping Project

```bash
/master

Complete web scraping project:

Target: Scrape job postings van meerdere job boards

Requirements:
1. Scrape 3 verschillende job sites
2. Extract: job title, company, location, salary, description
3. Handle pagination (max 100 posts per site)
4. Store in SQLite database
5. Deduplicate jobs (same title + company)
6. Export to CSV
7. Generate statistics rapport (top companies, avg salary, etc.)
8. Schedule to run daily (cron job)

Lever compleet werkend systeem met documentatie.
```

**Master zal gebruiken**:
- `/research` - Scraping libraries en best practices
- `/architect` - Database schema en scraper architectuur
- `/scrape` - Voor elke website een scraper
- `/code` - Database operations, deduplication logic
- `/orchestrate` - Coördinatie van alle scrapers
- `/code` - Scheduling en automation

---

## 💡 Tips voor Effectief Gebruik

### 1. Start met de Juiste Specialist

- **Klein & Specifiek** → Directe specialist (`/code`, `/research`, `/scrape`)
- **Groot & Complex** → Orchestrator (`/orchestrate`, `/master`)
- **Strategisch** → Architect (`/architect`)

### 2. Geef Volledige Context

Inclusief:
- Wat wil je bereiken? (doel)
- Wat zijn je constraints? (tech stack, budget, tijd)
- Wat is succes? (success criteria)
- Wat heb je al? (bestaande code/data)

### 3. Iteratief Werken

Je kunt altijd verder bouwen:

```bash
# Eerste iteratie
/code
Maak basic API met Flask

# Tweede iteratie
/code
Voeg JWT authentication toe aan bestaande API

# Derde iteratie
/code
Voeg rate limiting toe
```

### 4. Combineer Strategisch

```
Research → Architect → Implement → Test
   ↓          ↓           ↓          ↓
/research  /architect   /code     /code
```

---

## 🎓 Leer van Voorbeelden

De beste manier om te leren:

1. **Start simpel**: Begin met `/code` of `/research`
2. **Gradueel complexer**: Probeer `/orchestrate`
3. **Full workflows**: Gebruik `/master` voor complete projecten
4. **Experimenteer**: Probeer verschillende combinaties

---

Meer vragen? Gebruik `/agents` voor een quick reference!
