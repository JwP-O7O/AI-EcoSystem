# Agent Zero Test Suite

Comprehensive testing framework for Agent Zero AI assistant with 80%+ code coverage.

## 📋 Overview

This test suite provides complete coverage of Agent Zero functionality:

- **Unit Tests**: Test individual components in isolation
- **Integration Tests**: Test component interactions
- **End-to-End Tests**: Test complete workflows
- **Mocked LLMs**: No real API calls during testing

## 🚀 Quick Start

### Installation

```bash
# Install test dependencies
pip install -r tests/requirements.txt

# Or install all dependencies including main requirements
pip install -r requirements.txt -r tests/requirements.txt
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=python --cov=agent --cov-report=html

# Run specific test category
pytest -m unit          # Unit tests only
pytest -m integration   # Integration tests only
pytest -m e2e          # End-to-end tests only

# Run specific test file
pytest tests/unit/test_task_planner.py

# Run specific test
pytest tests/unit/test_task_planner.py::TestTaskPlannerCreation::test_create_plan_success

# Run tests in parallel (faster)
pytest -n auto

# Run with verbose output
pytest -v

# Run and watch for changes
pytest-watch
```

## 📁 Test Structure

```
tests/
├── __init__.py                  # Test package initialization
├── conftest.py                  # Shared fixtures and mocks
├── requirements.txt             # Test dependencies
├── README.md                    # This file
│
├── unit/                        # Unit tests (fast, isolated)
│   ├── __init__.py
│   ├── test_task_planner.py    # Task planner tool tests (15+ tests)
│   ├── test_code_analyzer.py   # Code analyzer tool tests (30+ tests)
│   ├── test_memory.py           # Memory system tests (25+ tests)
│   └── ...
│
├── integration/                 # Integration tests (component interaction)
│   ├── __init__.py
│   ├── test_memory_system.py   # Memory integration tests
│   ├── test_tool_execution.py  # Tool execution pipeline tests
│   └── ...
│
├── e2e/                        # End-to-end tests (complete workflows)
│   ├── __init__.py
│   ├── test_full_workflow.py   # Complete workflow tests
│   └── ...
│
├── mocks/                      # Mock data and responses
│   └── ...
│
└── fixtures/                   # Test fixtures and data
    └── ...
```

## 🧪 Test Categories

### Unit Tests (`-m unit`)

Test individual components in complete isolation:

- **Task Planner**: Creation, updates, status, completion, replanning
- **Code Analyzer**: Python/JS analysis, security scanning, complexity metrics
- **Memory System**: Insert, search, delete, persistence
- **Tools**: All tool implementations
- **Helpers**: Utility functions and helper modules

**Example:**
```bash
pytest tests/unit/test_task_planner.py -v
```

### Integration Tests (`-m integration`)

Test component interactions:

- Agent-Memory integration
- Tool execution pipeline
- Knowledge base loading
- Multi-tool coordination
- Error handling across components

**Example:**
```bash
pytest tests/integration/ -v
```

### End-to-End Tests (`-m e2e`)

Test complete workflows from start to finish:

- Multi-step task workflows
- Multi-tool coordination
- Memory persistence across operations
- Real-world scenarios
- Error recovery workflows

**Example:**
```bash
pytest tests/e2e/ -v
```

## 🎯 Key Features

### Mock LLM Responses

All tests use mocked LLM responses - **no real API calls**:

```python
from conftest import MockChatModel, MockEmbeddings

# Mock chat model with predefined responses
mock_model = MockChatModel(responses=["Response 1", "Response 2"])

# Mock embeddings
mock_embeddings = MockEmbeddings(dimension=384)
```

### Shared Fixtures

Common test fixtures available in all tests:

```python
def test_example(mock_agent, mock_llm_json_response, temp_memory_dir):
    # mock_agent: Pre-configured mock agent
    # mock_llm_json_response: Mock JSON response
    # temp_memory_dir: Temporary directory for memory storage
    pass
```

### Parametrized Tests

Test multiple scenarios efficiently:

```python
@pytest.mark.parametrize("complexity", ["low", "medium", "high"])
async def test_all_complexity_levels(mock_agent, complexity):
    # Test runs 3 times with different complexity values
    pass
```

### Async Support

Full async/await support:

```python
@pytest.mark.asyncio
async def test_async_operation(mock_agent):
    result = await mock_agent.call_utility_llm("test")
    assert result is not None
```

## 📊 Coverage

Target coverage: **80%+**

Generate coverage report:

```bash
# HTML report (opens in browser)
pytest --cov=python --cov=agent --cov-report=html
open htmlcov/index.html

# Terminal report
pytest --cov=python --cov=agent --cov-report=term-missing

# Coverage with minimum threshold
pytest --cov=python --cov=agent --cov-fail-under=80
```

## 🏷️ Test Markers

Organize and filter tests with markers:

```bash
# Run only tool tests
pytest -m tools

# Run only memory tests
pytest -m memory

# Run only async tests
pytest -m async

# Run everything except slow tests
pytest -m "not slow"

# Combine markers
pytest -m "unit and tools"
```

Available markers:
- `unit`: Unit tests
- `integration`: Integration tests
- `e2e`: End-to-end tests
- `slow`: Slow tests
- `memory`: Memory/database tests
- `tools`: Tool functionality tests
- `helpers`: Helper module tests
- `async`: Async operation tests
- `mock`: Tests with mocked dependencies
- `real`: Tests with real dependencies

## 🔧 Configuration

### pytest.ini

Main pytest configuration file:

```ini
[pytest]
testpaths = tests
python_files = test_*.py
addopts = -v --strict-markers --asyncio-mode=auto
markers =
    unit: Unit tests
    integration: Integration tests
    e2e: End-to-end tests
```

### conftest.py

Shared fixtures and configuration:

- Mock LLM models
- Mock embeddings
- Agent fixtures
- Memory fixtures
- Tool fixtures
- Utility functions

## 📝 Writing Tests

### Basic Test Template

```python
import pytest
from python.tools.example_tool import ExampleTool

class TestExampleTool:
    """Test ExampleTool functionality."""

    @pytest.mark.asyncio
    async def test_basic_operation(self, mock_agent):
        """Test basic tool operation."""
        tool = ExampleTool(agent=mock_agent, name="example", args={}, message="")
        response = await tool.execute(action="test")

        assert response is not None
        assert "expected content" in response.message

    @pytest.mark.parametrize("input_value,expected", [
        ("input1", "output1"),
        ("input2", "output2"),
    ])
    async def test_multiple_inputs(self, mock_agent, input_value, expected):
        """Test with multiple input values."""
        tool = ExampleTool(agent=mock_agent, name="example", args={}, message="")
        response = await tool.execute(action="test", value=input_value)

        assert expected in response.message
```

### Testing Async Functions

```python
@pytest.mark.asyncio
async def test_async_function(mock_agent):
    """Test async function."""
    result = await some_async_function(mock_agent)
    assert result is not None
```

### Using Fixtures

```python
def test_with_fixtures(mock_agent, temp_memory_dir, sample_python_code):
    """Test using multiple fixtures."""
    # mock_agent is automatically provided
    # temp_memory_dir is a temporary directory
    # sample_python_code is sample Python code
    pass
```

### Mocking External Calls

```python
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_with_mock(mock_agent):
    """Test with mocked external call."""
    mock_agent.call_utility_llm = AsyncMock(return_value='{"result": "success"}')

    tool = SomeTool(agent=mock_agent, name="test", args={}, message="")
    response = await tool.execute(action="test")

    # Verify mock was called
    mock_agent.call_utility_llm.assert_called_once()
```

## 🐛 Debugging Tests

### Run with Extra Verbosity

```bash
pytest -vv
```

### Show Print Statements

```bash
pytest -s
```

### Run Single Test

```bash
pytest tests/unit/test_task_planner.py::TestTaskPlannerCreation::test_create_plan_success -v
```

### Drop into Debugger on Failure

```bash
pytest --pdb
```

### Show Locals in Traceback

```bash
pytest -l
```

## ⚡ Performance

### Run Tests in Parallel

```bash
# Auto-detect CPU cores
pytest -n auto

# Specific number of workers
pytest -n 4
```

### Skip Slow Tests

```bash
pytest -m "not slow"
```

### Benchmark Tests

```bash
pytest --benchmark-only
```

## 📈 Continuous Integration

Example GitHub Actions workflow:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r tests/requirements.txt
      - name: Run tests
        run: pytest --cov=python --cov=agent --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

## 🔍 Test Best Practices

1. **Isolation**: Each test should be independent
2. **Fast**: Unit tests should run quickly (< 1s each)
3. **Clear Names**: Use descriptive test names
4. **Arrange-Act-Assert**: Follow AAA pattern
5. **Mock External**: Mock all external dependencies
6. **Single Responsibility**: Test one thing per test
7. **Parametrize**: Use parametrize for similar tests
8. **Async Properly**: Mark async tests with `@pytest.mark.asyncio`

## 🆘 Common Issues

### Import Errors

```bash
# Make sure you're in the project root
cd /path/to/agent-zero

# Install in development mode
pip install -e .
```

### Async Test Warnings

```python
# Use this decorator for async tests
@pytest.mark.asyncio
async def test_async():
    pass
```

### Fixture Not Found

Check that fixture is defined in `conftest.py` or imported properly.

### Mock Not Working

```python
# Use AsyncMock for async functions
from unittest.mock import AsyncMock

mock_func = AsyncMock(return_value="value")
```

## 📚 Additional Resources

- [pytest documentation](https://docs.pytest.org/)
- [pytest-asyncio](https://pytest-asyncio.readthedocs.io/)
- [pytest-cov](https://pytest-cov.readthedocs.io/)
- [unittest.mock](https://docs.python.org/3/library/unittest.mock.html)

## 📞 Support

For issues or questions:
1. Check test output carefully
2. Review conftest.py for available fixtures
3. Examine existing tests for examples
4. Check pytest documentation

## 🎓 Test Statistics

Current test coverage:

- **Unit Tests**: 70+ tests across all components
- **Integration Tests**: 30+ tests for component interaction
- **E2E Tests**: 20+ tests for complete workflows
- **Total**: 120+ comprehensive tests
- **Coverage Target**: 80%+

---

**Happy Testing! 🚀**
