### web_search tool:
- Search the web for information using multiple search engines
- **Purpose**: Find current information, documentation, tutorials, code examples
- **Parameters**:
  - query (required): Search query string
  - engine (optional): Search engine - "duckduckgo" (default), "google", or "bing"
  - max_results (optional): Maximum results to return (default: 5)
- **Example usage**:
```json
{
  "thoughts": [
    "I need to find the latest Python documentation for asyncio",
    "I will search the web for this information"
  ],
  "tool_name": "web_search",
  "tool_args": {
    "query": "Python asyncio documentation latest",
    "engine": "duckduckgo",
    "max_results": 5
  }
}
```
- Use this tool whenever you need current information from the internet
- Combine with webpage_content_tool to get full content from search results
