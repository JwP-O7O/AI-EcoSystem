# Agent Zero Marketplace

> Community-driven registry for Agent Zero agents, tools, prompts, and integrations

## Overview

The Agent Zero Marketplace is a decentralized registry where developers can publish and discover:
- **Agents**: Pre-configured specialized agents
- **Tools**: Custom tools and integrations
- **Prompts**: Optimized prompt templates
- **Integrations**: Third-party service connectors

## Structure

```
marketplace/
├── agents/           # Agent configurations
├── tools/            # Custom tools
├── prompts/          # Prompt templates
├── integrations/     # Third-party integrations
├── registry.json     # Master registry (auto-generated)
└── schemas/          # JSON schemas for validation
```

## Publishing to the Marketplace

### 1. Create Your Item

#### Publishing an Agent
```yaml
# agents/my-agent/manifest.yml
name: data-analyst-agent
version: 1.0.0
author: username
description: Specialized agent for data analysis tasks
category: data-science
tags: [data, analytics, pandas, visualization]
license: MIT

agent:
  role: data_analyst
  tools:
    - code_execution
    - web_search
    - file_operations
  config:
    auto_memory_count: 5
    rate_limit_requests: 30
```

#### Publishing a Tool
```yaml
# tools/my-tool/manifest.yml
name: notion-tool
version: 1.0.0
author: username
description: Integration with Notion API
category: productivity
tags: [notion, productivity, documentation]
license: MIT
dependencies:
  - notion-client==2.0.0

tool:
  class_name: NotionTool
  file: notion_tool.py
  config_required:
    - NOTION_API_KEY
```

#### Publishing a Prompt
```yaml
# prompts/my-prompt/manifest.yml
name: technical-writer
version: 1.0.0
author: username
description: Prompt for technical documentation writing
category: writing
tags: [documentation, technical-writing, markdown]
license: MIT

prompt:
  file: technical_writer.md
  variables:
    - topic
    - audience
    - format
```

### 2. Test Locally

```bash
# Install from local marketplace
agent-zero marketplace install ./marketplace/agents/my-agent

# Test the agent
agent-zero run --agent my-agent "Analyze this dataset"
```

### 3. Submit Pull Request

1. Fork the marketplace repository
2. Add your item to the appropriate directory
3. Run validation: `agent-zero marketplace validate`
4. Submit PR with description

### 4. Automated Checks

All submissions go through:
- ✅ Schema validation
- ✅ Security scanning
- ✅ License verification
- ✅ Code quality checks
- ✅ Automated testing

## Installing from Marketplace

### CLI Installation

```bash
# Install an agent
agent-zero marketplace install agent/data-analyst-agent

# Install a tool
agent-zero marketplace install tool/notion-tool

# Install a prompt
agent-zero marketplace install prompt/technical-writer

# Search marketplace
agent-zero marketplace search "data analysis"

# List installed items
agent-zero marketplace list

# Update all installed items
agent-zero marketplace update
```

### Programmatic Installation

```python
from agent_zero.marketplace import MarketplaceClient

client = MarketplaceClient()

# Install agent
client.install("agent/data-analyst-agent", version="1.0.0")

# Search
results = client.search("productivity", category="tools")

# List all
items = client.list_all(category="agents")
```

## Categories

### Agents
- `general` - General purpose agents
- `code` - Software development
- `data-science` - Data analysis and ML
- `content` - Content creation
- `research` - Research and analysis
- `automation` - Task automation
- `enterprise` - Business applications

### Tools
- `productivity` - Productivity tools
- `development` - Developer tools
- `data` - Data sources and databases
- `communication` - Messaging and notifications
- `ai-ml` - AI/ML services
- `cloud` - Cloud platforms
- `automation` - Automation services

### Prompts
- `system` - System prompts
- `specialized` - Domain-specific prompts
- `techniques` - Prompting techniques
- `languages` - Multi-language prompts

## Quality Guidelines

### Agent Guidelines
- Must include clear description
- Should have example usage
- Must specify required tools
- Should include cost estimates
- Must have testing coverage

### Tool Guidelines
- Must follow Tool base class
- Should include error handling
- Must have clear documentation
- Should include rate limiting
- Must handle API key security

### Prompt Guidelines
- Must be well-tested
- Should include examples
- Must document variables
- Should specify target LLM
- Must follow ethical guidelines

## Security

### Automated Security Checks
- Dependency vulnerability scanning
- Code security analysis
- Secrets detection
- License compatibility

### Reporting Security Issues
Report security vulnerabilities to: security@agentzero.dev

## Registry Schema

The `registry.json` is auto-generated from manifests:

```json
{
  "version": "1.0.0",
  "updated": "2025-11-29T12:00:00Z",
  "agents": [
    {
      "id": "data-analyst-agent",
      "name": "Data Analyst Agent",
      "version": "1.0.0",
      "author": "username",
      "description": "...",
      "category": "data-science",
      "downloads": 1234,
      "rating": 4.8,
      "verified": true
    }
  ],
  "tools": [...],
  "prompts": [...]
}
```

## Verified Publishers

Publishers with verified badge have:
- ✅ Identity verification
- ✅ Code review approval
- ✅ Security audit passed
- ✅ Community trust score > 4.5

## Monetization (Future)

Coming soon:
- Premium listings ($19-99/month)
- Paid integrations (revenue share)
- Sponsorship opportunities
- Enterprise support packages

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

The marketplace registry is licensed under MIT.
Individual items have their own licenses (specified in manifests).

## Support

- Discord: [discord.gg/agent-zero](https://discord.gg/agent-zero)
- Discussions: [GitHub Discussions](https://github.com/agent-zero-framework/marketplace/discussions)
- Email: marketplace@agentzero.dev

---

**Total Items**: 0 agents, 0 tools, 0 prompts
**Last Updated**: 2025-11-29
