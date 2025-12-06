# Batch Executor Tool - Complete Guide

Een geavanceerd parallel processing systeem voor Agent Zero dat het mogelijk maakt om meerdere taken efficiënt en parallel uit te voeren.

## 📋 Inhoudsopgave

1. [Overzicht](#overzicht)
2. [Features](#features)
3. [Installatie](#installatie)
4. [Quick Start](#quick-start)
5. [Gebruik](#gebruik)
6. [Voorbeelden](#voorbeelden)
7. [Best Practices](#best-practices)
8. [Troubleshooting](#troubleshooting)

## 🎯 Overzicht

De Batch Executor Tool maakt het mogelijk om:
- Meerdere taken parallel uit te voeren
- Taken te prioriteren en plannen
- Voortgang real-time te monitoren
- Resultaten te aggregeren en exporteren
- Resources efficiënt te beheren

### Wanneer Gebruiken?

- **File Processing**: 100+ bestanden analyseren
- **Data Transformatie**: Meerdere datasets verwerken
- **API Calls**: Parallel data ophalen
- **Web Scraping**: Meerdere URLs scrapen
- **Testing**: Batch tests uitvoeren

## ✨ Features

### 1. Queue Management
- ✅ Priority-based scheduling (LOW, MEDIUM, HIGH, CRITICAL)
- ✅ FIFO binnen dezelfde priority
- ✅ Task status tracking
- ✅ Queue inspection en management

### 2. Parallel Execution
- ✅ Asyncio-based parallelism
- ✅ Configureerbare max concurrent tasks
- ✅ Resource limiting
- ✅ Automatic retry op failures

### 3. Progress Tracking
- ✅ Real-time status updates
- ✅ Percentage completion
- ✅ Estimated time remaining
- ✅ Task execution times
- ✅ Success/failure counts

### 4. Result Aggregation
- ✅ Collect all results
- ✅ Filter by status
- ✅ Generate summaries
- ✅ Export to JSON/CSV

### 5. Error Handling
- ✅ Automatic retry logic
- ✅ Configurable max retries
- ✅ Detailed error tracking
- ✅ Graceful degradation

## 🚀 Installatie

De tool is al geïnstalleerd in je Agent Zero systeem:

```
/data/data/com.termux/files/home/AI-EcoSystem/agent-zero/
├── python/tools/batch_executor_tool.py
├── prompts/default/agent.system.tool.batch_executor.md
└── test_batch_executor.py
```

### Verificatie

Test de installatie:

```bash
cd /data/data/com.termux/files/home/AI-EcoSystem/agent-zero
python test_batch_executor.py
```

Voor een interactieve demo:

```bash
python test_batch_executor.py demo
```

## 🏃 Quick Start

### Voorbeeld 1: Eenvoudige Batch

```python
# 1. Voeg taken toe
{
  "tool_name": "batch_executor",
  "action": "add_batch",
  "tasks": [
    {
      "name": "Task 1",
      "function": "simulate",
      "params": {"duration": 1.0}
    },
    {
      "name": "Task 2",
      "function": "simulate",
      "params": {"duration": 1.5}
    }
  ]
}

# 2. Start uitvoering
{
  "tool_name": "batch_executor",
  "action": "start",
  "max_concurrent": 5
}

# 3. Check status
{
  "tool_name": "batch_executor",
  "action": "status"
}

# 4. Bekijk resultaten
{
  "tool_name": "batch_executor",
  "action": "results"
}
```

### Voorbeeld 2: File Processing

```python
# Verwerk meerdere CSV files
{
  "tool_name": "batch_executor",
  "action": "add_batch",
  "tasks": [
    {
      "name": "Analyze sales_2023.csv",
      "function": "code_execution",
      "params": {
        "runtime": "python",
        "code": "import pandas as pd\ndf = pd.read_csv('sales_2023.csv')\nprint(df.describe())"
      },
      "priority": "high"
    },
    {
      "name": "Analyze sales_2024.csv",
      "function": "code_execution",
      "params": {
        "runtime": "python",
        "code": "import pandas as pd\ndf = pd.read_csv('sales_2024.csv')\nprint(df.describe())"
      },
      "priority": "high"
    }
  ]
}
```

## 📖 Gebruik

### Actions Overzicht

| Action | Beschrijving | Parameters |
|--------|--------------|------------|
| `add` | Voeg 1 taak toe | name, function, params, priority, max_retries |
| `add_batch` | Voeg meerdere taken toe | tasks (list) |
| `start` | Start uitvoering | max_concurrent, timeout |
| `stop` | Stop uitvoering | graceful |
| `status` | Bekijk status | detailed |
| `results` | Bekijk resultaten | format, filter_status |
| `export` | Exporteer resultaten | format, output_file |
| `clear` | Verwijder voltooide taken | - |
| `cancel` | Annuleer specifieke taak | task_id |

### Priority Levels

```python
"priority": "critical"  # Hoogste prioriteit
"priority": "high"      # Hoge prioriteit
"priority": "medium"    # Default prioriteit
"priority": "low"       # Laagste prioriteit
```

### Task Status

- `QUEUED`: Wacht op uitvoering
- `RUNNING`: Wordt uitgevoerd
- `COMPLETED`: Succesvol afgerond
- `FAILED`: Gefaald (na retries)
- `CANCELLED`: Geannuleerd

## 💡 Voorbeelden

### Voorbeeld 1: Multiple File Analysis

```python
# Stap 1: Voeg batch toe
{
  "tool_name": "batch_executor",
  "action": "add_batch",
  "tasks": [
    {
      "name": f"Analyze file_{i}.csv",
      "function": "code_execution",
      "params": {
        "runtime": "python",
        "code": f"""
import pandas as pd
import json

df = pd.read_csv('data/file_{i}.csv')
stats = {{
    'rows': len(df),
    'columns': len(df.columns),
    'missing': df.isnull().sum().to_dict(),
    'summary': df.describe().to_dict()
}}
print(json.dumps(stats))
"""
      },
      "priority": "high" if i < 5 else "medium"
    }
    for i in range(1, 101)  # 100 files
  ]
}

# Stap 2: Start met 10 parallel workers
{
  "tool_name": "batch_executor",
  "action": "start",
  "max_concurrent": 10
}

# Stap 3: Monitor progress
{
  "tool_name": "batch_executor",
  "action": "status",
  "detailed": true
}

# Stap 4: Export naar CSV
{
  "tool_name": "batch_executor",
  "action": "export",
  "format": "csv",
  "output_file": "analysis_results.csv"
}
```

### Voorbeeld 2: Parallel API Calls

```python
# Fetch data van 50 users
{
  "tool_name": "batch_executor",
  "action": "add_batch",
  "tasks": [
    {
      "name": f"Fetch user {user_id}",
      "function": "code_execution",
      "params": {
        "runtime": "python",
        "code": f"""
import requests
import json

response = requests.get('https://api.example.com/users/{user_id}')
data = response.json()
print(json.dumps(data))
"""
      },
      "priority": "high",
      "max_retries": 3
    }
    for user_id in range(1, 51)
  ]
}

# Start met 20 concurrent requests
{
  "tool_name": "batch_executor",
  "action": "start",
  "max_concurrent": 20
}
```

### Voorbeeld 3: Web Scraping

```python
urls = [
    "https://example.com/page1",
    "https://example.com/page2",
    # ... meer URLs
]

{
  "tool_name": "batch_executor",
  "action": "add_batch",
  "tasks": [
    {
      "name": f"Scrape {url}",
      "function": "code_execution",
      "params": {
        "runtime": "python",
        "code": f"""
import requests
from bs4 import BeautifulSoup

response = requests.get('{url}')
soup = BeautifulSoup(response.content, 'html.parser')
title = soup.find('title').text
print(f'Title: {{title}}')
"""
      },
      "priority": "medium",
      "max_retries": 2
    }
    for url in urls
  ]
}
```

### Voorbeeld 4: Data Transformatie

```python
# Transform multiple datasets
{
  "tool_name": "batch_executor",
  "action": "add_batch",
  "tasks": [
    {
      "name": f"Transform dataset_{i}",
      "function": "code_execution",
      "params": {
        "runtime": "python",
        "code": f"""
import pandas as pd
import numpy as np

# Load data
df = pd.read_csv('raw_data/dataset_{i}.csv')

# Transform
df['normalized'] = (df['value'] - df['value'].mean()) / df['value'].std()
df['log_value'] = np.log1p(df['value'])
df['category'] = pd.cut(df['value'], bins=5, labels=['A','B','C','D','E'])

# Save
df.to_csv('processed_data/dataset_{i}.csv', index=False)
print(f'Processed {{len(df)}} rows')
"""
      },
      "priority": "medium"
    }
    for i in range(1, 51)
  ]
}
```

### Voorbeeld 5: Testing Suite

```python
# Run multiple test suites in parallel
{
  "tool_name": "batch_executor",
  "action": "add_batch",
  "tasks": [
    {
      "name": "Unit Tests",
      "function": "code_execution",
      "params": {
        "runtime": "terminal",
        "code": "pytest tests/unit/"
      },
      "priority": "critical"
    },
    {
      "name": "Integration Tests",
      "function": "code_execution",
      "params": {
        "runtime": "terminal",
        "code": "pytest tests/integration/"
      },
      "priority": "high"
    },
    {
      "name": "E2E Tests",
      "function": "code_execution",
      "params": {
        "runtime": "terminal",
        "code": "pytest tests/e2e/"
      },
      "priority": "medium"
    }
  ]
}
```

## 🎯 Best Practices

### 1. Resource Management

```python
# Voor I/O-bound taken (API calls, file ops): Hoge concurrency
{
  "action": "start",
  "max_concurrent": 20  # I/O operations
}

# Voor CPU-bound taken (data processing): Lage concurrency
{
  "action": "start",
  "max_concurrent": 4  # CPU operations
}
```

### 2. Error Handling

```python
# Stel max_retries in op basis van reliability
{
  "name": "Critical API Call",
  "function": "code_execution",
  "params": {...},
  "max_retries": 5  # Belangrijke operatie
}

{
  "name": "Optional Task",
  "function": "code_execution",
  "params": {...},
  "max_retries": 1  # Minder belangrijk
}
```

### 3. Priority Gebruik

```python
# Gebruik priorities voor belangrijke taken
{
  "tasks": [
    # Kritieke data eerst
    {"name": "Customer Data", "priority": "critical", ...},
    {"name": "Sales Data", "priority": "high", ...},

    # Normale processing
    {"name": "Analytics", "priority": "medium", ...},

    # Nice-to-have
    {"name": "Generate Report", "priority": "low", ...}
  ]
}
```

### 4. Monitoring

```python
# Monitor progress regelmatig
import asyncio

async def monitor_batch():
    while True:
        status = await executor.execute(action="status")
        print(status.message)

        # Check if done
        if "Progress: 100.0%" in status.message:
            break

        await asyncio.sleep(5)  # Check elke 5 seconden
```

### 5. Result Export

```python
# Exporteer altijd grote batches
{
  "action": "export",
  "format": "json",
  "output_file": "results_YYYYMMDD_HHMMSS.json"
}

# Of CSV voor spreadsheet analysis
{
  "action": "export",
  "format": "csv",
  "output_file": "results.csv"
}
```

## 🔧 Troubleshooting

### Probleem: Tasks worden niet uitgevoerd

**Oplossing:**
```python
# 1. Check of batch is gestart
{"action": "status"}

# 2. Start de batch
{"action": "start", "max_concurrent": 5}

# 3. Check voor errors
{"action": "results", "filter_status": "failed"}
```

### Probleem: Hoge failure rate

**Oplossing:**
```python
# 1. Verhoog max_retries
{
  "tasks": [
    {"max_retries": 5, ...}
  ]
}

# 2. Verlaag concurrency (minder resource contention)
{"action": "start", "max_concurrent": 2}

# 3. Check error messages
{"action": "results", "filter_status": "failed"}
```

### Probleem: Out of memory

**Oplossing:**
```python
# 1. Verlaag max_concurrent
{"action": "start", "max_concurrent": 3}

# 2. Process in kleinere batches
# Run 50 tasks, export, clear, repeat

# 3. Clear completed tasks regelmatig
{"action": "clear"}
```

### Probleem: Slow execution

**Oplossing:**
```python
# 1. Verhoog concurrency (voor I/O tasks)
{"action": "start", "max_concurrent": 20}

# 2. Check task execution times
{"action": "status", "detailed": true}

# 3. Optimize task code
# - Reduce unnecessary operations
# - Use efficient algorithms
# - Cache results where possible
```

### Probleem: Tasks stuck in RUNNING

**Oplossing:**
```python
# 1. Stop gracefully
{"action": "stop", "graceful": true}

# 2. Check for infinite loops in task code
{"action": "results", "filter_status": "running"}

# 3. Restart met timeout
{"action": "start", "max_concurrent": 5, "timeout": 300}
```

## 📊 Performance Tips

### Optimal Concurrency

```python
# I/O-bound (network, file ops)
max_concurrent = 10-20

# CPU-bound (computations)
max_concurrent = CPU_cores (meestal 2-8)

# Mixed workload
max_concurrent = 5-10
```

### Memory Optimization

```python
# 1. Process in batches
for batch_num in range(10):
    # Add 100 tasks
    # Execute
    # Export results
    # Clear

# 2. Stream large results
{"action": "export", "format": "csv"}  # CSV uses less memory

# 3. Filter results
{"action": "results", "filter_status": "completed"}
```

### Network Optimization

```python
# Use connection pooling in tasks
"""
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

session = requests.Session()
retry = Retry(total=3, backoff_factor=0.3)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

response = session.get(url)
"""
```

## 📚 Geavanceerde Gebruik

### Custom Functions

```python
{
  "name": "Custom Processing",
  "function": "custom_function",
  "params": {
    "code": """
def process(input_data):
    # Your custom logic here
    result = input_data * 2
    return result
""",
    "args": {"input_data": 42}
  }
}
```

### Integration met andere Tools

```python
# Gebruik batch executor met andere Agent Zero tools
{
  "tasks": [
    {
      "name": "Search Knowledge",
      "function": "knowledge_search",
      "params": {"query": "topic 1"}
    },
    {
      "name": "Save Memory",
      "function": "memory_operation",
      "params": {"action": "save", "data": {...}}
    }
  ]
}
```

## 🎓 Conclusie

De Batch Executor Tool is een krachtig systeem voor:
- ✅ Parallel processing van multiple taken
- ✅ Efficiënt resource gebruik
- ✅ Real-time monitoring
- ✅ Robuuste error handling
- ✅ Flexibele result export

Voor vragen of problemen, raadpleeg:
- Tool source: `python/tools/batch_executor_tool.py`
- Tests: `test_batch_executor.py`
- Prompt: `prompts/default/agent.system.tool.batch_executor.md`
