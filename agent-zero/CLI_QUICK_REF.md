# Agent Zero CLI 2.0 - Quick Reference

## Installation

```bash
cd /data/data/com.termux/files/home/AI-EcoSystem/agent-zero
./install-cli.sh
source ~/.bashrc
```

## Essential Commands

### Setup & Configuration

```bash
agent-zero config init                    # Interactive setup
agent-zero config set <key> <value>       # Set config value
agent-zero config list                    # Show all config
agent-zero version                        # Show version
agent-zero status                         # System status
```

### Chat & Execution

```bash
agent-zero chat                           # Interactive chat
agent-zero run "task description"         # Run single task
az chat                                   # Short alias
az run "analyze code"                     # Short alias
```

### Project Management

```bash
agent-zero init myproject                 # New project
agent-zero init myproject --template research
agent-zero project templates              # List templates
agent-zero project info                   # Project info
agent-zero project validate               # Validate project
```

### Marketplace

```bash
agent-zero marketplace search "query"     # Search items
agent-zero marketplace install <item>     # Install item
agent-zero marketplace list               # List all items
agent-zero marketplace info <item>        # Item details
agent-zero marketplace update             # Update all
```

### Agent Management

```bash
agent-zero agent list                     # List agents
agent-zero agent create myagent           # Create agent
agent-zero agent info <name>              # Agent info
agent-zero agent test <name>              # Test agent
```

### Development

```bash
agent-zero dev                            # Dev server
agent-zero deploy local                   # Deploy locally
agent-zero deploy cloud                   # Deploy to cloud
agent-zero logs list                      # View logs
agent-zero logs show <id> --follow        # Follow logs
```

## Common Workflows

### Quick Start

```bash
az config init          # Setup
az chat                 # Start chatting
```

### New Project

```bash
az init myproject --template code
cd myproject
az chat
```

### Install & Use Marketplace Item

```bash
az marketplace search code
az marketplace install code-expert
az run "analyze my code" --agent code-expert
```

### Custom Agent Development

```bash
az agent create myagent
# Edit agents/myagent.py
az agent test myagent
```

## Options & Flags

### Global Options

```bash
--help, -h              # Show help
--version               # Show version
--verbose, -v           # Verbose output
--quiet, -q             # Quiet mode
```

### Common Flags

```bash
--agent, -a <name>      # Use specific agent
--model, -m <model>     # Override model
--output, -o <file>     # Output to file
--timeout, -t <sec>     # Set timeout
--template, -t <name>   # Project template
--category, -c <cat>    # Item category
--force, -f             # Force operation
```

## Configuration Keys

```bash
model.chat              # Chat model name
model.provider          # AI provider
api_keys.google         # Google API key
api_keys.openai         # OpenAI API key
agent.rate_limit        # Rate limit
agent.max_iterations    # Max iterations
cli.theme               # CLI theme
cli.verbose             # Verbose mode
```

## Templates

- `default` - Standard project
- `minimal` - Minimal setup
- `research` - Research-oriented
- `code` - Code development

## Marketplace Categories

- `agent` - Complete agents
- `tool` - Individual tools
- `prompt` - Prompt templates

## Environment Variables

```bash
AGENT_ZERO_VERBOSE=1    # Enable verbose
AGENT_ZERO_QUIET=1      # Enable quiet
GOOGLE_API_KEY=xxx      # Google API key
OPENAI_API_KEY=xxx      # OpenAI API key
```

## File Locations

```bash
~/.agent-zero/config.json           # Config file
~/.agent-zero/marketplace/          # Marketplace cache
./project.json                      # Project config
./.env                              # Environment vars
./agents/                           # Custom agents
./tools/                            # Custom tools
./prompts/                          # Custom prompts
```

## Aliases

```bash
alias az='agent-zero'
alias azr='agent-zero run'
alias azc='agent-zero chat'
alias azi='agent-zero init'
alias azm='agent-zero marketplace'
```

Add to `~/.bashrc` or `~/.zshrc`

## Tab Completion

Auto-complete commands with Tab key:

```bash
agent-zero <TAB>              # Main commands
agent-zero marketplace <TAB>  # Subcommands
agent-zero --template <TAB>   # Options
```

## Help Commands

```bash
agent-zero --help                     # Main help
agent-zero marketplace --help         # Marketplace help
agent-zero config --help              # Config help
agent-zero <command> --help           # Command help
```

## Troubleshooting

```bash
# If CLI not found
export PATH="$HOME/.local/bin:$PATH"

# Or use directly
python cli.py --help

# Reinstall requirements
pip install -r requirements-cli.txt

# Check status
agent-zero status
```

## Quick Examples

```bash
# Setup and start
az config init && az chat

# Create project and start
az init myproject && cd myproject && az chat

# Search, install, use
az marketplace search tools
az marketplace install web-scraper
az run "scrape website" --agent web-scraper

# Config management
az config set model.chat gpt-4
az config validate
az config export backup.json

# Deploy workflow
az init production --template minimal
cd production
az deploy local
```

---

**Full Guide**: See `CLI_GUIDE.md`

**Support**: GitHub Issues
