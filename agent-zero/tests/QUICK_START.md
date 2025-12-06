# Agent Zero Testing - Quick Start Guide

Get up and running with Agent Zero tests in 5 minutes.

## ⚡ 1-Minute Setup

```bash
# Navigate to project root
cd /data/data/com.termux/files/home/AI-EcoSystem/agent-zero

# Install test dependencies
pip install -r tests/requirements.txt

# Run all tests
pytest

# Done! ✅
```

## 🎯 Common Commands

```bash
# Run all tests with coverage
pytest --cov=python --cov=agent --cov-report=html

# Run only unit tests (fast)
pytest -m unit

# Run specific test file
pytest tests/unit/test_task_planner.py

# Run tests in parallel (4x faster)
pytest -n auto

# Watch mode (auto-rerun on file changes)
pytest-watch
```

## 📊 Check Coverage

```bash
# Generate HTML coverage report
pytest --cov=python --cov=agent --cov-report=html

# View in browser (Termux)
termux-open htmlcov/index.html
```

## 🔍 Test Specific Features

```bash
# Test task planner
pytest tests/unit/test_task_planner.py -v

# Test code analyzer
pytest tests/unit/test_code_analyzer.py -v

# Test memory system
pytest tests/unit/test_memory.py -v

# Test all tools
pytest -m tools -v

# Test memory operations
pytest -m memory -v
```

## 🐛 Debug Failed Tests

```bash
# Show full output
pytest -vv -s

# Stop at first failure
pytest -x

# Drop into debugger on failure
pytest --pdb

# Show locals in traceback
pytest -l
```

## ✍️ Write Your First Test

Create `tests/unit/test_my_feature.py`:

```python
import pytest
from python.helpers.tool import Response

class TestMyFeature:
    """Test my new feature."""

    @pytest.mark.asyncio
    async def test_basic_functionality(self, mock_agent):
        """Test basic functionality."""
        # Your test code here
        assert True

    def test_edge_case(self, mock_agent):
        """Test edge case."""
        # Your test code here
        assert True
```

Run it:
```bash
pytest tests/unit/test_my_feature.py -v
```

## 📈 Quick Reference

### Test Markers

```bash
pytest -m unit          # Unit tests only
pytest -m integration   # Integration tests
pytest -m e2e          # End-to-end tests
pytest -m "not slow"   # Skip slow tests
```

### Common Fixtures

```python
# Available in all tests (via conftest.py)
mock_agent              # Mock agent instance
mock_llm_json_response  # Mock LLM JSON response
temp_memory_dir         # Temporary memory directory
sample_python_code      # Sample Python code
sample_javascript_code  # Sample JavaScript code
```

### Async Tests

```python
@pytest.mark.asyncio
async def test_async_function(mock_agent):
    result = await some_async_function()
    assert result is not None
```

### Parametrized Tests

```python
@pytest.mark.parametrize("input,expected", [
    ("a", "A"),
    ("b", "B"),
])
def test_multiple_cases(input, expected):
    assert input.upper() == expected
```

## 🎓 Next Steps

1. **Read full documentation**: `tests/README.md`
2. **Explore existing tests**: `tests/unit/`, `tests/integration/`
3. **Check coverage**: `pytest --cov`
4. **Write new tests**: Follow existing patterns
5. **Run CI locally**: `pytest --cov --cov-fail-under=80`

## 💡 Pro Tips

1. **Run tests before committing**: `pytest -n auto`
2. **Keep tests fast**: Mock external dependencies
3. **Test edge cases**: Empty inputs, invalid data, errors
4. **Use descriptive names**: `test_feature_scenario_expected()`
5. **One assertion per test**: Keep tests focused
6. **Check coverage**: `pytest --cov`

## 🆘 Troubleshooting

**Tests fail with import errors:**
```bash
# Install dependencies
pip install -r requirements.txt -r tests/requirements.txt
```

**Async warnings:**
```python
# Add decorator to async tests
@pytest.mark.asyncio
async def test_function():
    pass
```

**Fixture not found:**
- Check `conftest.py` for fixture definition
- Ensure fixture name is spelled correctly

**Coverage too low:**
```bash
# See which lines aren't covered
pytest --cov=python --cov=agent --cov-report=term-missing
```

## 📞 Need Help?

- Check `tests/README.md` for detailed documentation
- Review `conftest.py` for available fixtures
- Look at existing tests for examples
- See pytest docs: https://docs.pytest.org/

---

**Happy Testing! 🚀**
