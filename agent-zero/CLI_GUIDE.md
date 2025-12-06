# Agent Zero CLI 2.0 - Complete Guide

## Overzicht

Agent Zero CLI 2.0 is een geavanceerde command-line interface voor het Agent Zero framework met moderne features zoals marketplace integratie, project management, en een enhanced user experience.

## Installatie

### Stap 1: Installeer Requirements

```bash
cd /data/data/com.termux/files/home/AI-EcoSystem/agent-zero
pip install -r requirements-cli.txt
```

### Stap 2: Installeer CLI

```bash
# Optie 1: Setup installatie
python setup.py install

# Optie 2: Development mode
python setup.py develop

# Optie 3: Direct gebruik (zonder installatie)
chmod +x cli.py
```

### Stap 3: Shell Completion (Optioneel)

Voor Bash:
```bash
echo "source $HOME/AI-EcoSystem/agent-zero/completions/agent-zero-completion.bash" >> ~/.bashrc
source ~/.bashrc
```

Voor Zsh:
```bash
echo "source $HOME/AI-EcoSystem/agent-zero/completions/agent-zero-completion.zsh" >> ~/.zshrc
source ~/.zshrc
```

### Stap 4: Alias Setup (Optioneel)

```bash
echo "alias az='agent-zero'" >> ~/.bashrc
source ~/.bashrc
```

## Configuratie

### Eerste Setup

```bash
agent-zero config init
```

Dit start een interactieve setup wizard voor:
- AI Provider selectie (Google, OpenAI, Anthropic, Ollama)
- API keys
- Model configuratie
- Agent instellingen

### Handmatige Configuratie

```bash
# Bekijk huidige configuratie
agent-zero config list

# Zet individuele waarden
agent-zero config set model.chat "gemini-2.5-flash"
agent-zero config set api_keys.google "your-api-key"

# Exporteer configuratie
agent-zero config export my-config.json

# Importeer configuratie
agent-zero config import my-config.json --merge
```

## Marketplace

### Zoeken naar Items

```bash
# Zoek in marketplace
agent-zero marketplace search "code"

# Filter op categorie
agent-zero marketplace search "analysis" --category tool

# Lijst alle items
agent-zero marketplace list
```

### Installeren

```bash
# Installeer een agent/tool/prompt
agent-zero marketplace install code-expert

# Bekijk info eerst
agent-zero marketplace info code-expert

# Force reinstall
agent-zero marketplace install code-expert --force
```

### Publiceren

```bash
# Publiceer je eigen item
agent-zero marketplace publish ./my-agent --category agent --name "My Agent"
```

### Updates

```bash
# Update alles
agent-zero marketplace update

# Update specifiek item
agent-zero marketplace update code-expert

# Check alleen voor updates
agent-zero marketplace update --check
```

## Project Management

### Nieuw Project

```bash
# Initialiseer standaard project
agent-zero init my-project

# Gebruik een template
agent-zero init my-research-project --template research

# Custom locatie
agent-zero init my-project --path /custom/path
```

### Beschikbare Templates

```bash
# Toon alle templates
agent-zero project templates
```

Templates:
- **default**: Standaard Agent Zero project
- **minimal**: Minimale setup
- **research**: Research-georiënteerd met web search
- **code**: Code development focus

### Project Info

```bash
# Bekijk project informatie
agent-zero project info

# Valideer project structuur
agent-zero project validate

# Clean artifacts
agent-zero project clean
agent-zero project clean --deep
```

## Agent Management

### Agents Uitvoeren

```bash
# Voer een enkele taak uit
agent-zero run "Analyze the code in main.py"

# Gebruik specifieke agent
agent-zero run "Research Python asyncio" --agent research

# Met output naar bestand
agent-zero run "Generate report" --output report.txt

# Met timeout
agent-zero run "Long task" --timeout 300
```

### Interactive Chat

```bash
# Start chat sessie
agent-zero chat

# Met specifieke agent
agent-zero chat --agent code

# Met debug mode
agent-zero chat --debug
```

### Agent Beheer

```bash
# List beschikbare agents
agent-zero agent list

# Bekijk agent info
agent-zero agent info code-expert

# Creëer nieuwe custom agent
agent-zero agent create my-agent

# Test een agent
agent-zero agent test my-agent --task "test task"
```

## Development Mode

```bash
# Start dev server met hot reload
agent-zero dev

# Custom port
agent-zero dev --port 8080

# Zonder reload
agent-zero dev --no-reload
```

## Deployment

```bash
# Deploy lokaal
agent-zero deploy local

# Deploy naar cloud
agent-zero deploy cloud

# Deploy naar mobile/Termux
agent-zero deploy mobile

# Docker deployment
agent-zero deploy docker

# Dry run (test zonder deployment)
agent-zero deploy cloud --dry-run
```

## Logs

```bash
# Bekijk recente logs
agent-zero logs list

# Toon log details
agent-zero logs show <log-id>

# Follow logs real-time
agent-zero logs show <log-id> --follow

# Clear oude logs
agent-zero logs clear --days 7
agent-zero logs clear --all
```

## Status

```bash
# Bekijk systeem status
agent-zero status
```

Toont:
- Systeem informatie (CPU, Memory, Disk)
- Agent Zero status
- Actieve processen
- Configuratie locatie

## Quick Commands

```bash
# Versie info
agent-zero version

# Help
agent-zero --help
agent-zero marketplace --help
agent-zero config --help
```

## Voorbeelden

### Voorbeeld 1: Snel Project Setup

```bash
# 1. Initialiseer config
agent-zero config init

# 2. Creëer project
agent-zero init my-ai-project --template research

# 3. Ga naar project
cd my-ai-project

# 4. Start chat
agent-zero chat
```

### Voorbeeld 2: Marketplace Workflow

```bash
# Zoek naar code tools
agent-zero marketplace search code --category tool

# Bekijk details
agent-zero marketplace info code-analyzer

# Installeer
agent-zero marketplace install code-analyzer

# Gebruik
agent-zero run "Analyze my codebase" --agent code-analyzer
```

### Voorbeeld 3: Custom Agent Development

```bash
# Creëer project
agent-zero init dev-project --template code

# Creëer custom agent
cd dev-project
agent-zero agent create data-processor

# Edit agent (gebruik je favoriete editor)
nano agents/data_processor.py

# Test
agent-zero agent test data-processor --task "process test data"

# Deploy
agent-zero deploy local
```

### Voorbeeld 4: Configuration Management

```bash
# Exporteer huidige config
agent-zero config export backup-config.json

# Wijzig settings
agent-zero config set model.chat "gpt-4"
agent-zero config set agent.rate_limit 50

# Valideer
agent-zero config validate

# Reset indien nodig
agent-zero config reset
agent-zero config import backup-config.json
```

## Keyboard Shortcuts (in Chat Mode)

- `Ctrl+C`: Interrupt huidige operatie
- `Ctrl+D`: Exit chat
- Type `exit` of `quit`: Stop chat sessie
- Type `clear`: Clear screen
- Type `help`: Toon help

## Environment Variables

```bash
# Verbose output
export AGENT_ZERO_VERBOSE=1

# Quiet mode
export AGENT_ZERO_QUIET=1

# Custom config locatie
export AGENT_ZERO_CONFIG=/path/to/config.json
```

## Troubleshooting

### CLI niet gevonden na installatie

```bash
# Zorg dat Python bin directory in PATH staat
export PATH="$HOME/.local/bin:$PATH"

# Of gebruik direct
python cli.py --help
```

### Import errors

```bash
# Installeer alle requirements
pip install -r requirements-cli.txt

# Of installeer handmatig
pip install typer rich python-dotenv requests psutil
```

### Permission errors

```bash
# Maak cli.py executable
chmod +x cli.py

# Of run met python
python cli.py
```

## Advanced Features

### Custom Templates

Creëer je eigen project templates door een template directory toe te voegen aan `python/cli/project.py`.

### Custom Marketplace

Wijzig de `MARKETPLACE_API` in `python/cli/marketplace.py` om je eigen marketplace te gebruiken.

### Plugin System

Extend de CLI door nieuwe typer apps toe te voegen aan `cli.py`.

## Best Practices

1. **Gebruik Config Init**: Start altijd met `agent-zero config init`
2. **Template Gebruik**: Gebruik de juiste template voor je project type
3. **Marketplace**: Check marketplace items voor herbruikbare componenten
4. **Version Control**: Voeg `.env` toe aan `.gitignore`
5. **Regular Updates**: Run `agent-zero marketplace update` regelmatig
6. **Logs Cleanup**: Clean oude logs met `agent-zero logs clear`
7. **Validation**: Valideer project en config regelmatig

## Shortcuts & Aliases

```bash
# Alias setup
alias az='agent-zero'
alias azr='agent-zero run'
alias azc='agent-zero chat'
alias azi='agent-zero init'
alias azm='agent-zero marketplace'

# Nu kun je gebruiken:
az chat
azr "my task"
azm search tools
```

## Integration met Bestaande Agent Zero

Deze CLI 2.0 is volledig compatible met bestaande Agent Zero installaties. Je kunt het gebruiken naast de oude `run_cli.py`:

```bash
# Oude manier
python run_cli.py

# Nieuwe manier
agent-zero chat

# Beide werken!
```

## Updates & Feedback

- Report bugs: GitHub Issues
- Feature requests: GitHub Discussions
- Contribute: Pull Requests welkom!

---

**Veel succes met Agent Zero CLI 2.0!**
