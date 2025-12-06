# Batch Executor Tool - Quick Reference

## 🚀 Quick Start

### 1. Simple Batch (3 steps)

```python
# Step 1: Add tasks
{
  "tool_name": "batch_executor",
  "action": "add_batch",
  "tasks": [
    {"name": "Task 1", "function": "simulate", "params": {"duration": 1.0}},
    {"name": "Task 2", "function": "simulate", "params": {"duration": 1.0}},
    {"name": "Task 3", "function": "simulate", "params": {"duration": 1.0}}
  ]
}

# Step 2: Start execution
{
  "tool_name": "batch_executor",
  "action": "start",
  "max_concurrent": 5
}

# Step 3: Get results
{
  "tool_name": "batch_executor",
  "action": "results"
}
```

## 📚 Documentation

| Document | Description | Size |
|----------|-------------|------|
| **BATCH_EXECUTOR_GUIDE.md** | Complete user guide with examples | 678 lines |
| **BATCH_EXECUTOR_ARCHITECTURE.md** | System architecture & design | 562 lines |
| **BATCH_EXECUTOR_SUMMARY.md** | Implementation summary | 397 lines |
| **agent.system.tool.batch_executor.md** | Agent integration prompt | 161 lines |

## 🔧 Implementation

| File | Description | Size |
|------|-------------|------|
| **python/tools/batch_executor_tool.py** | Core tool implementation | 944 lines |
| **test_batch_executor.py** | Test suite & demo | 540 lines |

**Total**: 3,282 lines of code and documentation

## 🎯 Core Features

### ✅ Implemented
- [x] Queue Management (priority-based)
- [x] Parallel Execution (asyncio)
- [x] Progress Tracking (real-time)
- [x] Result Aggregation
- [x] Export (JSON/CSV)
- [x] Error Handling (retry logic)
- [x] Resource Limiting
- [x] Task Cancellation
- [x] Comprehensive Testing

### 📊 Performance
- **I/O-bound**: Up to 20x faster (20 concurrent)
- **CPU-bound**: Up to 8x faster (8 concurrent)
- **Memory**: Efficient (asyncio-based)

## 🏃 Run Tests

```bash
# Full test suite
cd /data/data/com.termux/files/home/AI-EcoSystem/agent-zero
python test_batch_executor.py

# Interactive demo
python test_batch_executor.py demo
```

## 📋 Actions Reference

| Action | Purpose | Key Parameters |
|--------|---------|----------------|
| `add` | Add single task | name, function, params, priority |
| `add_batch` | Add multiple tasks | tasks (list) |
| `start` | Start execution | max_concurrent, timeout |
| `stop` | Stop execution | graceful |
| `status` | Get status | detailed |
| `results` | Get results | format, filter_status |
| `export` | Export results | format (json/csv), output_file |
| `clear` | Clear completed | - |
| `cancel` | Cancel task | task_id |

## 🎨 Priority Levels

```
CRITICAL → Urgent, execute first
HIGH     → Important, high priority
MEDIUM   → Default priority
LOW      → Background tasks
```

## 📈 Use Cases

### File Processing
```python
# Process 100 files in parallel
tasks = [
  {
    "name": f"Process file_{i}.csv",
    "function": "code_execution",
    "params": {"runtime": "python", "code": f"..."},
    "priority": "high"
  }
  for i in range(100)
]
```

### API Calls
```python
# Fetch from 50 endpoints
tasks = [
  {
    "name": f"Fetch user {id}",
    "function": "code_execution",
    "params": {"runtime": "python", "code": f"requests.get(...)"},
    "max_retries": 3
  }
  for id in range(50)
]
```

### Testing
```python
# Run test suites in parallel
tasks = [
  {"name": "Unit Tests", "function": "code_execution",
   "params": {"runtime": "terminal", "code": "pytest tests/unit/"}},
  {"name": "Integration Tests", "function": "code_execution",
   "params": {"runtime": "terminal", "code": "pytest tests/integration/"}}
]
```

## ⚡ Best Practices

### 1. Set Correct Concurrency
```python
# I/O-bound (files, network)
max_concurrent = 15-20

# CPU-bound (computation)
max_concurrent = 4-8

# Mixed
max_concurrent = 5-10
```

### 2. Use Priorities
```python
# Critical first
priority = "critical"  # User-facing, urgent

# Then important
priority = "high"      # Important features

# Then normal
priority = "medium"    # Regular tasks

# Finally background
priority = "low"       # Nice-to-have
```

### 3. Handle Errors
```python
# Network calls: more retries
max_retries = 5

# Expensive operations: fewer retries
max_retries = 1
```

### 4. Monitor Progress
```python
# Check status regularly
{"action": "status", "detailed": true}

# Filter results
{"action": "results", "filter_status": "failed"}
```

### 5. Export Results
```python
# JSON for structured data
{"action": "export", "format": "json"}

# CSV for spreadsheets
{"action": "export", "format": "csv"}
```

## 🔍 Troubleshooting

| Problem | Solution |
|---------|----------|
| Tasks not executing | Run `{"action": "start"}` |
| High failure rate | Increase `max_retries`, reduce `max_concurrent` |
| Out of memory | Reduce `max_concurrent`, clear completed tasks |
| Slow execution | Increase `max_concurrent` for I/O tasks |
| Tasks stuck | Stop and restart with timeout |

## 📊 Status Monitoring

```python
# Get overview
{
  "action": "status"
}

# Get detailed status
{
  "action": "status",
  "detailed": true
}

# Get specific results
{
  "action": "results",
  "filter_status": "completed"  # or "failed", "running"
}
```

## 💾 Export Options

### JSON Export
```python
{
  "action": "export",
  "format": "json",
  "output_file": "results.json"
}
```

### CSV Export
```python
{
  "action": "export",
  "format": "csv",
  "output_file": "results.csv"
}
```

## 🔄 Complete Workflow

```python
# 1. Add tasks (batch)
{
  "action": "add_batch",
  "tasks": [...]
}

# 2. Start processing
{
  "action": "start",
  "max_concurrent": 10
}

# 3. Monitor (optional)
{
  "action": "status",
  "detailed": true
}

# 4. Get results
{
  "action": "results"
}

# 5. Export
{
  "action": "export",
  "format": "json"
}

# 6. Clean up
{
  "action": "clear"
}
```

## 🎓 Examples

### Example 1: Data Analysis
```python
# Analyze 50 CSV files
{"action": "add_batch", "tasks": [
  {
    "name": f"Analyze sales_{i}.csv",
    "function": "code_execution",
    "params": {
      "runtime": "python",
      "code": """
import pandas as pd
df = pd.read_csv('sales_${i}.csv')
print(df.describe().to_json())
"""
    }
  } for i in range(50)
]}

{"action": "start", "max_concurrent": 10}
{"action": "status"}
{"action": "export", "format": "csv"}
```

### Example 2: Web Scraping
```python
# Scrape 100 URLs
urls = ["https://example.com/page1", ...]

{"action": "add_batch", "tasks": [
  {
    "name": f"Scrape {url}",
    "function": "code_execution",
    "params": {
      "runtime": "python",
      "code": f"""
import requests
from bs4 import BeautifulSoup
r = requests.get('{url}')
soup = BeautifulSoup(r.content, 'html.parser')
print(soup.find('title').text)
"""
    },
    "max_retries": 2
  } for url in urls
]}

{"action": "start", "max_concurrent": 20}
```

### Example 3: Image Processing
```python
# Process 200 images
{"action": "add_batch", "tasks": [
  {
    "name": f"Process image_{i}.jpg",
    "function": "code_execution",
    "params": {
      "runtime": "python",
      "code": f"""
from PIL import Image
img = Image.open('images/image_{i}.jpg')
img = img.resize((800, 600))
img.save('processed/image_{i}.jpg')
print('Processed image_{i}.jpg')
"""
    },
    "priority": "medium"
  } for i in range(200)
]}

{"action": "start", "max_concurrent": 8}  # CPU-bound
```

## 📈 Performance Tips

### Optimize Concurrency
```python
# Test different values
for max_concurrent in [5, 10, 15, 20]:
    # Measure throughput
    # Find optimal value
```

### Batch Size
```python
# Process in chunks
for batch in chunks(all_tasks, 100):
    add_batch(batch)
    start()
    export()
    clear()
```

### Memory Management
```python
# Clear regularly
{"action": "clear"}  # After each batch

# Export to free memory
{"action": "export", "format": "csv"}
```

## 🔐 Safety Features

- ✅ Thread-safe queue operations
- ✅ Automatic retry on failures
- ✅ Graceful shutdown
- ✅ Error isolation (one failure doesn't affect others)
- ✅ Resource limiting (prevent overload)

## 📞 Support

- **Documentation**: See BATCH_EXECUTOR_GUIDE.md
- **Architecture**: See BATCH_EXECUTOR_ARCHITECTURE.md
- **Tests**: Run `python test_batch_executor.py`
- **Demo**: Run `python test_batch_executor.py demo`

## 🎯 Key Metrics

| Metric | Value |
|--------|-------|
| Code Lines | 944 |
| Test Lines | 540 |
| Doc Lines | 1,798 |
| Total Lines | 3,282 |
| Test Coverage | 7 scenarios |
| Test Status | ✅ ALL PASSING |

## ✅ Status

**Version**: 1.0.0
**Status**: PRODUCTION READY ✅
**Date**: November 29, 2025
**Tests**: ALL PASSING ✅

---

**Get Started**: Run `python test_batch_executor.py demo`
