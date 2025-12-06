# Integration Framework Documentation

Complete guide for the Agent Zero Integration Framework - easily add and use 3rd party services.

## Table of Contents

1. [Overview](#overview)
2. [Quick Start](#quick-start)
3. [Available Integrations](#available-integrations)
4. [Configuration](#configuration)
5. [Usage Examples](#usage-examples)
6. [Creating Custom Integrations](#creating-custom-integrations)
7. [API Reference](#api-reference)
8. [Troubleshooting](#troubleshooting)

---

## Overview

The Integration Framework provides a unified way to integrate 3rd party services into Agent Zero. It handles:

- **OAuth 2.0 Authentication** - Secure token management and automatic refresh
- **API Key Management** - Safe storage and usage of credentials
- **Rate Limiting** - Per-service rate limiting with token bucket algorithm
- **Retry Logic** - Exponential backoff for failed requests
- **Webhook Support** - Handle incoming events from services
- **Auto-Discovery** - Automatically find and register integrations
- **Configuration Management** - Easy enable/disable and configuration storage

### Built-in Integrations

1. **Gmail** - Email operations
2. **Slack** - Team messaging
3. **GitHub** - Repository management
4. **Notion** - Knowledge management
5. **Trello** - Project boards

---

## Quick Start

### 1. Initialize the Framework

```python
from python.helpers.integration_framework import IntegrationFramework

# Create framework instance
framework = IntegrationFramework()
framework.setup()

# List available integrations
print(framework.list_available())
# Output: ['gmail', 'slack', 'github', 'notion', 'trello']
```

### 2. Configure an Integration

```python
# Configure GitHub
framework.configure("github", {
    "enabled": True,
    "token": "ghp_your_personal_access_token_here"
})

# Test the connection
result = framework.test("github")
print(result)
# Output: {'status': 'success', 'login': 'yourusername', 'name': 'Your Name'}
```

### 3. Use the Integration

```python
# Get the integration
github = framework.get("github")

# Create an issue
issue = github.create_issue(
    repo="owner/repo",
    title="Bug: Login fails",
    body="Steps to reproduce...",
    labels=["bug", "priority-high"]
)

print(f"Created issue: {issue['html_url']}")
```

---

## Available Integrations

### Gmail Integration

**Capabilities:**
- Send emails with attachments
- Read and search emails
- Mark as read/unread
- Archive and delete messages
- Create drafts
- Manage labels and threads

**Setup:**
1. Enable Gmail API in [Google Cloud Console](https://console.cloud.google.com)
2. Create OAuth 2.0 credentials
3. Add authorized redirect URI: `http://localhost:8080/oauth2callback`
4. Download credentials and configure

**Configuration:**
```json
{
  "enabled": true,
  "client_id": "YOUR_CLIENT_ID.apps.googleusercontent.com",
  "client_secret": "YOUR_CLIENT_SECRET",
  "redirect_uri": "http://localhost:8080/oauth2callback",
  "access_token": null,
  "refresh_token": null
}
```

**Usage Example:**
```python
gmail = framework.get("gmail")

# Send email
gmail.send_email(
    to="user@example.com",
    subject="Hello from Agent Zero",
    body="<h1>Hello!</h1>",
    html=True
)

# Search unread emails
messages = gmail.search_messages("is:unread", max_results=10)
for msg in messages:
    print(f"From: {msg['snippet']}")
```

---

### Slack Integration

**Capabilities:**
- Send messages to channels/users
- Read channel history
- Search messages
- Upload files
- Create/join/leave channels
- React to messages
- Get user information

**Setup:**
1. Create Slack App at [api.slack.com/apps](https://api.slack.com/apps)
2. Add Bot Token Scopes:
   - `chat:write`
   - `channels:read`
   - `channels:history`
   - `files:write`
   - `users:read`
3. Install app to workspace
4. Copy Bot User OAuth Token

**Configuration:**
```json
{
  "enabled": true,
  "bot_token": "xoxb-YOUR-BOT-TOKEN-HERE"
}
```

**Usage Example:**
```python
slack = framework.get("slack")

# Send message
slack.send_message(
    channel="#general",
    text="Hello from Agent Zero!"
)

# Send rich message with blocks
slack.send_message(
    channel="#general",
    text="Notification",
    blocks=[
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*Important Update*\nTask completed successfully!"
            }
        }
    ]
)

# Upload file
slack.upload_file(
    channels="C1234567890",
    content="Log data here...",
    filename="app.log",
    title="Application Logs"
)
```

---

### GitHub Integration

**Capabilities:**
- Create/manage repositories
- Create/update/close issues
- Create/merge pull requests
- Manage branches
- Search code/repos/issues
- Create releases
- Get file content

**Setup:**
1. Go to [github.com/settings/tokens](https://github.com/settings/tokens)
2. Click "Generate new token (classic)"
3. Select scopes: `repo`, `user`, `admin:org`
4. Generate and copy token

**Configuration:**
```json
{
  "enabled": true,
  "token": "ghp_YOUR_PERSONAL_ACCESS_TOKEN"
}
```

**Usage Example:**
```python
github = framework.get("github")

# Create repository
repo = github.create_repository(
    name="my-awesome-project",
    description="An awesome project",
    private=False,
    auto_init=True
)

# Create issue
issue = github.create_issue(
    repo="owner/repo",
    title="Feature: Add dark mode",
    body="We need dark mode support...",
    labels=["enhancement", "ui"]
)

# Create pull request
pr = github.create_pull_request(
    repo="owner/repo",
    title="Add authentication",
    head="feature-auth",
    base="main",
    body="This PR adds user authentication..."
)

# Search repositories
results = github.search_repositories(
    query="agent framework language:python",
    sort="stars"
)
for repo in results["items"][:5]:
    print(f"{repo['full_name']}: {repo['stargazers_count']} stars")
```

---

### Notion Integration

**Capabilities:**
- Create/update pages
- Query databases
- Create database entries
- Search content
- Add blocks to pages
- Create comments
- Manage page hierarchy

**Setup:**
1. Go to [notion.so/my-integrations](https://www.notion.so/my-integrations)
2. Click "New integration"
3. Configure integration name and workspace
4. Copy Internal Integration Token
5. Share pages/databases with the integration

**Configuration:**
```json
{
  "enabled": true,
  "api_key": "secret_YOUR_INTERNAL_INTEGRATION_TOKEN"
}
```

**Usage Example:**
```python
notion = framework.get("notion")

# Search for a database
results = notion.search(query="Tasks", filter_type="database")
database_id = results["results"][0]["id"]

# Create a page in database
page = notion.create_page(
    parent_id=database_id,
    title="New Task",
    properties={
        "Status": {"select": {"name": "In Progress"}},
        "Priority": {"select": {"name": "High"}}
    }
)

# Add content to page
notion.append_blocks(
    block_id=page["id"],
    children=[
        notion.create_heading_block("Task Details", level=1),
        notion.create_paragraph_block("This task involves..."),
        notion.create_todo_block("Step 1: Research", checked=True),
        notion.create_todo_block("Step 2: Implementation", checked=False)
    ]
)

# Query database
results = notion.query_database(
    database_id=database_id,
    filter_conditions={
        "property": "Status",
        "select": {"equals": "In Progress"}
    },
    sorts=[{"property": "Priority", "direction": "descending"}]
)
```

---

### Trello Integration

**Capabilities:**
- Create/manage boards
- Create/update/move cards
- Manage lists
- Add comments and attachments
- Assign members
- Add labels and checklists
- Search cards

**Setup:**
1. Go to [trello.com/app-key](https://trello.com/app-key)
2. Copy your API Key
3. Click "Token" link to generate a token
4. Authorize and copy token

**Configuration:**
```json
{
  "enabled": true,
  "api_key": "YOUR_API_KEY",
  "token": "YOUR_TOKEN"
}
```

**Usage Example:**
```python
trello = framework.get("trello")

# Create board
board = trello.create_board(
    name="Project X",
    desc="Project management board"
)

# Get lists
lists = trello.list_lists(board["id"])
todo_list = [l for l in lists if l["name"] == "To Do"][0]

# Create card
card = trello.create_card(
    list_id=todo_list["id"],
    name="Implement feature X",
    desc="Detailed description...",
    due="2024-12-31"
)

# Add checklist
trello.add_checklist(
    card_id=card["id"],
    name="Tasks",
    items=[
        "Design architecture",
        "Write code",
        "Write tests",
        "Documentation"
    ]
)

# Search cards
results = trello.search("urgent bug")
for card in results.get("cards", []):
    print(f"{card['name']} on {card['board']['name']}")
```

---

## Configuration

### Configuration Files

Configurations are stored in `~/.agent-zero/integrations/` as JSON files:

```
~/.agent-zero/integrations/
├── gmail.json
├── slack.json
├── github.json
├── notion.json
└── trello.json
```

### Generate Example Configs

```python
framework = IntegrationFramework()
framework.create_default_configs()
# Creates .json.example files with templates
```

### Programmatic Configuration

```python
# Configure and save
framework.configure("slack", {
    "enabled": True,
    "bot_token": "xoxb-..."
}, save=True)

# Configure without saving
slack_config = {
    "enabled": True,
    "bot_token": os.getenv("SLACK_BOT_TOKEN")
}
framework.configure("slack", slack_config, save=False)
```

### Enable/Disable Integrations

```python
# Enable
framework.enable("gmail")

# Disable
framework.disable("gmail")

# Check status
integrations = framework.list_all_with_status()
for integration in integrations:
    print(f"{integration['name']}: {integration['status']}")
```

---

## Creating Custom Integrations

### Step 1: Create Integration Class

Create a new file in `python/integrations/`:

```python
# python/integrations/custom.py
from typing import Dict, Any
from .base import BaseIntegration, RateLimitConfig

class CustomIntegration(BaseIntegration):
    """Custom service integration"""

    def __init__(self, name: str, config: Dict[str, Any]):
        # Define rate limits
        rate_limit = RateLimitConfig(
            max_requests=100,
            window_seconds=60
        )

        super().__init__(name, config, rate_limit=rate_limit)

    def get_base_url(self) -> str:
        return "https://api.custom-service.com/v1"

    def test_connection(self) -> Dict[str, Any]:
        """Test API connection"""
        try:
            result = self.get_status()
            return {"status": "success", "data": result}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def get_status(self) -> Dict[str, Any]:
        """Get API status"""
        return self._make_request("GET", "/status")

    def custom_operation(self, param: str) -> Dict[str, Any]:
        """Custom operation"""
        return self._make_request(
            "POST",
            "/operation",
            json_data={"param": param}
        )
```

### Step 2: Register Integration

```python
from python.integrations.custom import CustomIntegration

framework.registry.register("custom", CustomIntegration)
```

### Step 3: Configure and Use

```python
framework.configure("custom", {
    "enabled": True,
    "api_key": "your-api-key"
})

custom = framework.get("custom")
result = custom.custom_operation("test")
```

---

## API Reference

### IntegrationFramework

Main interface for managing integrations.

#### Methods

**`setup()`**
- Setup framework and discover integrations

**`get(integration_name: str) -> Optional[BaseIntegration]`**
- Get integration instance

**`configure(integration_name: str, config: Dict, save: bool = True) -> BaseIntegration`**
- Configure an integration

**`enable(integration_name: str)`**
- Enable an integration

**`disable(integration_name: str)`**
- Disable an integration

**`list_available() -> List[str]`**
- List all available integrations

**`list_enabled() -> List[str]`**
- List enabled integrations

**`test(integration_name: str) -> Dict`**
- Test specific integration

**`test_all() -> Dict[str, Dict]`**
- Test all enabled integrations

**`get_stats() -> Dict[str, Dict]`**
- Get statistics for all integrations

### BaseIntegration

Base class for all integrations.

#### Methods

**`_make_request(method, url, params, data, json_data, headers) -> Any`**
- Make HTTP request with rate limiting and retries

**`is_authenticated() -> bool`**
- Check authentication status

**`get_oauth_authorize_url(state) -> str`**
- Get OAuth authorization URL

**`exchange_code_for_token(code) -> Dict`**
- Exchange OAuth code for token

**`refresh_access_token() -> Dict`**
- Refresh OAuth access token

**`test_connection() -> Dict`**
- Test API connection (override in subclass)

**`get_stats() -> Dict`**
- Get integration statistics

**`reset_stats()`**
- Reset statistics

---

## Troubleshooting

### Authentication Issues

**Problem:** `401 Unauthorized` errors

**Solutions:**
1. Check if credentials are correctly configured
2. Verify OAuth tokens haven't expired
3. Test connection: `framework.test("integration_name")`
4. Check if API key/token has required permissions

### Rate Limiting

**Problem:** `429 Too Many Requests` errors

**Solutions:**
1. Rate limiting is automatic, but check stats: `framework.get_stats()`
2. Adjust rate limits in integration constructor
3. Spread requests over time

### OAuth Token Refresh

**Problem:** Tokens expire and need refresh

**Solution:**
- Token refresh is automatic for OAuth integrations
- Ensure `refresh_token` is saved in config
- If refresh fails, re-authenticate

### Connection Timeouts

**Problem:** Requests timeout

**Solutions:**
1. Check internet connectivity
2. Verify service API is accessible
3. Timeout is set to 30 seconds by default
4. Retries happen automatically (3 times by default)

### Configuration Not Saving

**Problem:** Config changes don't persist

**Solutions:**
1. Ensure config directory exists and is writable
2. Use `save=True` when calling `configure()`
3. Check file permissions on `~/.agent-zero/integrations/`

### Integration Not Found

**Problem:** `get()` returns None

**Solutions:**
1. Ensure framework is setup: `framework.setup()`
2. Check integration is registered: `framework.list_available()`
3. Verify configuration exists
4. Try re-initializing: `framework.configure(...)`

---

## Advanced Usage

### Webhook Handling

```python
integration = framework.get("slack")

# Register webhook handler
def handle_message(payload):
    print(f"Received: {payload}")
    return {"status": "ok"}

integration.webhook.register("message", handle_message)

# Verify webhook signature
is_valid = integration.webhook.verify_signature(
    payload=request_body,
    signature=request_headers["X-Slack-Signature"],
    algorithm="sha256"
)
```

### Custom Rate Limits

```python
from python.integrations.base import RateLimitConfig

custom_rate_limit = RateLimitConfig(
    max_requests=1000,  # 1000 requests
    window_seconds=3600,  # per hour
    burst_size=50  # allow bursts of 50
)

# Use when creating integration
integration = CustomIntegration(
    name="custom",
    config=config,
    rate_limit=custom_rate_limit
)
```

### Custom Retry Logic

```python
from python.integrations.base import RetryConfig

custom_retry = RetryConfig(
    max_retries=5,
    initial_delay=2.0,
    max_delay=120.0,
    backoff_factor=3.0,
    retry_on_status=[429, 500, 502, 503, 504]
)

# Use when creating integration
integration = CustomIntegration(
    name="custom",
    config=config,
    retry_config=custom_retry
)
```

### Monitoring and Stats

```python
# Get stats for all integrations
all_stats = framework.get_stats()
for name, stats in all_stats.items():
    print(f"{name}:")
    print(f"  Total requests: {stats['total_requests']}")
    print(f"  Success rate: {stats['success_rate']}")
    print(f"  Rate limited: {stats['rate_limited']}")
    print(f"  Retries: {stats['retries']}")

# Reset stats
framework.reset_stats("github")  # Reset specific
framework.reset_stats()  # Reset all
```

---

## Best Practices

1. **Always test connections** after configuration
2. **Use environment variables** for sensitive credentials
3. **Enable only needed integrations** for better performance
4. **Monitor statistics** to identify issues
5. **Handle errors gracefully** in your code
6. **Respect rate limits** - they're there for a reason
7. **Keep tokens secure** - never commit them to version control
8. **Use webhooks** for real-time updates when possible
9. **Test in development** before using in production
10. **Keep integrations updated** with latest API versions

---

## Support

For issues, questions, or contributions:

1. Check this documentation
2. Review integration-specific API docs
3. Check service provider's API documentation
4. Review error messages and logs
5. Test with minimal examples

Happy integrating!
