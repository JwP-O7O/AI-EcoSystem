# Agent Zero Integrations

This directory contains all 3rd party service integrations for Agent Zero.

## Available Integrations

### Core Integrations

1. **base.py** - Base integration class with OAuth, rate limiting, and retry logic
2. **gmail.py** - Gmail email operations
3. **slack.py** - Slack team messaging
4. **github.py** - GitHub repository management
5. **notion.py** - Notion knowledge management
6. **trello.py** - Trello project boards

## Quick Start

```python
from python.helpers.integration_framework import get_integration

# Get an integration
github = get_integration("github")

# Use it
issue = github.create_issue(
    repo="owner/repo",
    title="Bug found",
    body="Description..."
)
```

## Creating a New Integration

### 1. Create Integration File

Create `python/integrations/myservice.py`:

```python
from typing import Dict, Any
from .base import BaseIntegration, RateLimitConfig

class MyServiceIntegration(BaseIntegration):
    """MyService integration"""

    def __init__(self, name: str, config: Dict[str, Any]):
        rate_limit = RateLimitConfig(
            max_requests=100,
            window_seconds=60
        )
        super().__init__(name, config, rate_limit=rate_limit)

    def get_base_url(self) -> str:
        return "https://api.myservice.com/v1"

    def test_connection(self) -> Dict[str, Any]:
        try:
            result = self.some_test_method()
            return {"status": "success"}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def some_operation(self, param: str) -> Dict[str, Any]:
        """Perform some operation"""
        return self._make_request("GET", "/endpoint", params={"q": param})
```

### 2. Register Integration

```python
from python.helpers.integration_framework import get_framework
from python.integrations.myservice import MyServiceIntegration

framework = get_framework()
framework.registry.register("myservice", MyServiceIntegration)
```

### 3. Configure

```python
framework.configure("myservice", {
    "enabled": True,
    "api_key": "your-api-key"
})
```

### 4. Use It

```python
myservice = framework.get("myservice")
result = myservice.some_operation("test")
```

## Integration Features

All integrations inherit these features from `BaseIntegration`:

### Authentication
- OAuth 2.0 with automatic token refresh
- API key support
- Custom authentication headers

### Rate Limiting
- Token bucket algorithm
- Configurable limits per integration
- Automatic waiting when rate limited

### Retry Logic
- Exponential backoff
- Configurable retry attempts
- Automatic retry on specific HTTP status codes

### Webhook Support
- Register event handlers
- Signature verification
- Multiple handlers per event

### Error Handling
- Automatic retry on transient errors
- Detailed error messages
- Request/response logging

### Statistics
- Track request counts
- Success/failure rates
- Rate limit events
- Retry counts

## Base Integration API

### Methods You Must Override

```python
def get_base_url(self) -> str:
    """Return the base URL for API requests"""
    pass

def test_connection(self) -> Dict[str, Any]:
    """Test the connection and return status"""
    pass
```

### Methods You Can Use

```python
# Make HTTP requests
self._make_request(
    method="GET",
    url="/endpoint",
    params={"key": "value"},
    json_data={"key": "value"},
    headers={"Custom-Header": "value"}
)

# Check authentication
self.is_authenticated()

# OAuth flow
url = self.get_oauth_authorize_url()
token = self.exchange_code_for_token(code)
token = self.refresh_access_token()

# Statistics
stats = self.get_stats()
self.reset_stats()
```

## Configuration Files

Configurations are stored in `~/.agent-zero/integrations/`:

```
~/.agent-zero/integrations/
├── gmail.json
├── slack.json
├── github.json
├── notion.json
└── trello.json
```

Example config structure:

```json
{
  "enabled": true,
  "api_key": "your-api-key",
  "custom_setting": "value"
}
```

## Rate Limit Configuration

Customize rate limits per integration:

```python
from python.integrations.base import RateLimitConfig

rate_limit = RateLimitConfig(
    max_requests=1000,     # Max requests
    window_seconds=3600,   # Time window (1 hour)
    burst_size=50          # Burst allowance
)

integration = MyIntegration(
    name="myservice",
    config=config,
    rate_limit=rate_limit
)
```

## Retry Configuration

Customize retry behavior:

```python
from python.integrations.base import RetryConfig

retry_config = RetryConfig(
    max_retries=5,
    initial_delay=2.0,
    max_delay=120.0,
    backoff_factor=3.0,
    retry_on_status=[429, 500, 502, 503, 504]
)

integration = MyIntegration(
    name="myservice",
    config=config,
    retry_config=retry_config
)
```

## Best Practices

1. **Always implement test_connection()** - Used to verify configuration
2. **Use descriptive method names** - Make API operations clear
3. **Document parameters** - Use docstrings with examples
4. **Handle errors gracefully** - Provide useful error messages
5. **Respect rate limits** - Configure appropriate limits
6. **Add type hints** - Help users understand parameters
7. **Write examples** - Show how to use each method
8. **Test thoroughly** - Test with real API endpoints
9. **Keep secrets safe** - Never log tokens or API keys
10. **Version compatibility** - Document required API versions

## Testing

Test your integration:

```python
# Test connection
result = integration.test_connection()
assert result["status"] == "success"

# Check authentication
assert integration.is_authenticated()

# Verify statistics
stats = integration.get_stats()
print(f"Success rate: {stats['success_rate']}")
```

## Documentation

See main documentation: `INTEGRATION_FRAMEWORK.md`

## Examples

See usage examples: `examples/integration_examples.py`

## Setup Script

Interactive setup: `scripts/setup_integrations.py`

```bash
python scripts/setup_integrations.py
```

## Support

For issues or questions:
1. Check integration-specific documentation
2. Review service provider's API docs
3. Check error messages and logs
4. Review example usage in `examples/`
