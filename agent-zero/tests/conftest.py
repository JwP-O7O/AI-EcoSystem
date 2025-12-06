"""
Pytest configuration and shared fixtures for Agent Zero tests.

This module provides:
- Mock LLM responses (no real API calls)
- Agent instance fixtures
- Memory database fixtures
- Common test utilities
"""

import pytest
import asyncio
import os
import tempfile
import shutil
from unittest.mock import Mock, AsyncMock, MagicMock, patch
from typing import AsyncIterator, List
from pathlib import Path

# Add project root to path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from agent import Agent, AgentConfig, AgentContext
from python.helpers.memory import Memory
from python.helpers.tool import Tool, Response
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.embeddings import Embeddings


# ============================================================================
# PYTEST CONFIGURATION
# ============================================================================

@pytest.fixture(scope="session")
def event_loop():
    """Create an event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# ============================================================================
# MOCK LLM CLASSES
# ============================================================================

class MockChatModel:
    """Mock chat model that returns predefined responses without API calls."""

    def __init__(self, responses: List[str] = None):
        self.responses = responses or ["Mock response"]
        self.response_index = 0
        self.call_count = 0
        self.last_input = None

    async def astream(self, messages):
        """Async stream mock responses."""
        self.call_count += 1
        self.last_input = messages

        response = self.responses[self.response_index % len(self.responses)]
        self.response_index += 1

        # Stream character by character
        for char in response:
            yield char
            await asyncio.sleep(0.001)  # Simulate streaming delay

    def __call__(self, *args, **kwargs):
        """Sync call support."""
        return self.responses[0]


class MockEmbeddings(Embeddings):
    """Mock embeddings model that returns fake vectors."""

    def __init__(self, dimension: int = 384):
        self.dimension = dimension
        self.model = "mock-embeddings"

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Return fake embeddings for documents."""
        import numpy as np
        return [np.random.rand(self.dimension).tolist() for _ in texts]

    def embed_query(self, text: str) -> List[float]:
        """Return fake embedding for query."""
        import numpy as np
        return np.random.rand(self.dimension).tolist()

    async def aembed_documents(self, texts: List[str]) -> List[List[float]]:
        """Async version of embed_documents."""
        return self.embed_documents(texts)

    async def aembed_query(self, text: str) -> List[float]:
        """Async version of embed_query."""
        return self.embed_query(text)


# ============================================================================
# AGENT FIXTURES
# ============================================================================

@pytest.fixture
def mock_chat_model():
    """Fixture providing a mock chat model."""
    return MockChatModel(responses=[
        "I understand the task.",
        '{"tool_name": "response", "tool_args": {"message": "Task completed"}}',
        "Analysis complete."
    ])


@pytest.fixture
def mock_utility_model():
    """Fixture providing a mock utility model."""
    return MockChatModel(responses=[
        "Utility response",
        '{"result": "success"}',
        "Processing complete"
    ])


@pytest.fixture
def mock_embeddings():
    """Fixture providing mock embeddings."""
    return MockEmbeddings(dimension=384)


@pytest.fixture
def temp_memory_dir():
    """Fixture providing a temporary directory for memory storage."""
    temp_dir = tempfile.mkdtemp(prefix="agent_zero_test_")
    yield temp_dir
    # Cleanup
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)


@pytest.fixture
def agent_config(mock_chat_model, mock_utility_model, mock_embeddings, temp_memory_dir):
    """Fixture providing a test agent configuration."""
    config = AgentConfig(
        chat_model=mock_chat_model,
        utility_model=mock_utility_model,
        embeddings_model=mock_embeddings,
        prompts_subdir="default",
        memory_subdir="test",
        auto_memory_count=3,
        auto_memory_skip=2,
        rate_limit_seconds=60,
        rate_limit_requests=100,  # High limit for tests
        msgs_keep_max=25,
        msgs_keep_start=5,
        msgs_keep_end=10,
        response_timeout_seconds=30,
        max_tool_response_length=3000,
        code_exec_docker_enabled=False,  # Disable Docker in tests
        code_exec_ssh_enabled=False,  # Disable SSH in tests
    )

    # Override memory path for testing
    original_get_abs_path = None

    def mock_get_abs_path(*paths):
        """Mock file path resolution to use temp directory."""
        if "memory" in paths:
            return os.path.join(temp_memory_dir, *[p for p in paths if p != "memory"])
        # Use original implementation for other paths
        from python.helpers import files
        return files.get_abs_path(*paths)

    # Patch file paths
    with patch('python.helpers.files.get_abs_path', side_effect=mock_get_abs_path):
        yield config


@pytest.fixture
async def agent_context(agent_config):
    """Fixture providing a test agent context."""
    context = AgentContext(config=agent_config)
    yield context
    # Cleanup
    AgentContext.remove(context.id)


@pytest.fixture
async def agent(agent_context):
    """Fixture providing a test agent instance."""
    agent = agent_context.agent0
    yield agent


@pytest.fixture
def mock_agent():
    """Fixture providing a minimal mock agent for tool testing."""
    agent = Mock(spec=Agent)
    agent.config = Mock()
    agent.config.max_tool_response_length = 3000
    agent.context = Mock()
    agent.context.log = Mock()
    agent.context.log.log = Mock(return_value=Mock(stream=Mock(), update=Mock()))
    agent.data = {}
    agent.history = []

    # Mock async methods
    agent.call_utility_llm = AsyncMock(return_value='{"result": "success"}')
    agent.append_message = AsyncMock()
    agent.handle_intervention = AsyncMock()

    # Mock sync methods
    agent.get_data = Mock(side_effect=lambda key: agent.data.get(key))
    agent.set_data = Mock(side_effect=lambda key, value: agent.data.update({key: value}))
    agent.read_prompt = Mock(return_value="Test prompt")

    return agent


# ============================================================================
# MEMORY FIXTURES
# ============================================================================

@pytest.fixture
async def memory_db(agent, temp_memory_dir):
    """Fixture providing an in-memory test database."""
    # Create temporary memory instance
    with patch('python.helpers.files.get_abs_path') as mock_path:
        mock_path.return_value = temp_memory_dir
        memory = await Memory.get(agent)
        yield memory


@pytest.fixture
def mock_memory():
    """Fixture providing a mock memory object."""
    memory = Mock(spec=Memory)
    memory.search_similarity_threshold = AsyncMock(return_value=[])
    memory.insert_text = Mock(return_value="test-id-123")
    memory.insert_documents = Mock(return_value=["id1", "id2"])
    memory.delete_documents_by_ids = AsyncMock(return_value=[])
    memory.delete_documents_by_query = AsyncMock(return_value=[])
    return memory


# ============================================================================
# TOOL FIXTURES
# ============================================================================

@pytest.fixture
def mock_tool_response():
    """Fixture providing a mock tool response."""
    return Response(
        message="Tool executed successfully",
        break_loop=False
    )


@pytest.fixture
def mock_tool(mock_agent):
    """Fixture providing a mock tool instance."""
    tool = Mock(spec=Tool)
    tool.agent = mock_agent
    tool.name = "test_tool"
    tool.args = {}
    tool.message = "Test message"
    tool.execute = AsyncMock(return_value=Response(message="Success", break_loop=False))
    tool.before_execution = AsyncMock()
    tool.after_execution = AsyncMock()
    return tool


# ============================================================================
# LLM RESPONSE MOCKS
# ============================================================================

@pytest.fixture
def mock_llm_json_response():
    """Fixture providing a mock LLM response with JSON."""
    return '''
    {
        "task": "Test task",
        "complexity": "medium",
        "subtasks": [
            {
                "id": "subtask_1",
                "description": "First step",
                "dependencies": [],
                "tools_needed": ["tool1"],
                "estimated_steps": 2,
                "priority": "high",
                "status": "pending"
            }
        ],
        "success_criteria": ["Criterion 1"],
        "risks": [{"risk": "Test risk", "mitigation": "Test mitigation"}],
        "estimated_total_steps": 5
    }
    '''


@pytest.fixture
def mock_code_analysis_response():
    """Fixture providing a mock code analysis response."""
    return {
        "language": "python",
        "lines": 100,
        "functions": [
            {"name": "test_func", "line": 10, "args": 2, "decorators": 0, "is_async": False}
        ],
        "classes": [
            {"name": "TestClass", "line": 20, "methods": 3, "bases": 1}
        ],
        "imports": ["os", "sys", "json"],
        "complexity": 5,
        "issues": [],
        "metrics": {
            "total_functions": 1,
            "total_classes": 1,
            "total_imports": 3,
            "cyclomatic_complexity": 5,
            "avg_function_args": 2.0
        }
    }


# ============================================================================
# FILE FIXTURES
# ============================================================================

@pytest.fixture
def sample_python_code():
    """Fixture providing sample Python code for testing."""
    return '''
import os
import sys

def example_function(arg1, arg2):
    """Example function."""
    if arg1:
        return arg1 + arg2
    return arg2

class ExampleClass:
    """Example class."""

    def __init__(self):
        self.value = 0

    def method(self, x):
        return x * 2
'''


@pytest.fixture
def sample_javascript_code():
    """Fixture providing sample JavaScript code for testing."""
    return '''
function exampleFunction(arg1, arg2) {
    if (arg1) {
        return arg1 + arg2;
    }
    return arg2;
}

class ExampleClass {
    constructor() {
        this.value = 0;
    }

    method(x) {
        return x * 2;
    }
}
'''


@pytest.fixture
def temp_test_file(tmp_path, sample_python_code):
    """Fixture providing a temporary test file."""
    test_file = tmp_path / "test_code.py"
    test_file.write_text(sample_python_code)
    return str(test_file)


# ============================================================================
# UTILITY FIXTURES
# ============================================================================

@pytest.fixture
def capture_prints(monkeypatch):
    """Fixture to capture print statements during tests."""
    printed = []

    def mock_print(*args, **kwargs):
        printed.append(' '.join(str(arg) for arg in args))

    monkeypatch.setattr('builtins.print', mock_print)
    return printed


@pytest.fixture
def mock_datetime():
    """Fixture providing a mock datetime."""
    from datetime import datetime
    with patch('python.helpers.memory.datetime') as mock_dt:
        mock_dt.now.return_value = datetime(2024, 1, 1, 12, 0, 0)
        mock_dt.now().strftime.return_value = "2024-01-01 12:00:00"
        yield mock_dt


# ============================================================================
# PARAMETRIZE HELPERS
# ============================================================================

# Common test data for parametrized tests
TOOL_ACTIONS = ["create", "update", "delete", "status"]
COMPLEXITY_LEVELS = ["low", "medium", "high", "very-high"]
PROGRAMMING_LANGUAGES = ["python", "javascript", "typescript", "java"]


# ============================================================================
# ASSERTION HELPERS
# ============================================================================

def assert_response_valid(response: Response):
    """Assert that a tool response is valid."""
    assert isinstance(response, Response)
    assert isinstance(response.message, str)
    assert isinstance(response.break_loop, bool)
    assert len(response.message) > 0


def assert_tool_called_with(mock_tool, **expected_kwargs):
    """Assert that a tool was called with expected arguments."""
    mock_tool.execute.assert_called_once()
    actual_kwargs = mock_tool.execute.call_args[1]
    for key, expected_value in expected_kwargs.items():
        assert key in actual_kwargs
        assert actual_kwargs[key] == expected_value


async def assert_async_called(mock_async_func, times=1):
    """Assert that an async mock was called a specific number of times."""
    assert mock_async_func.call_count == times


# ============================================================================
# MOCK DATA GENERATORS
# ============================================================================

def generate_mock_documents(count: int = 5):
    """Generate mock document objects for testing."""
    from langchain_core.documents import Document
    return [
        Document(
            page_content=f"Document {i} content",
            metadata={
                "id": f"doc_{i}",
                "timestamp": "2024-01-01 12:00:00",
                "area": "main",
                "source": "test"
            }
        )
        for i in range(count)
    ]


def generate_mock_task_plan():
    """Generate a mock task plan for testing."""
    return {
        "id": "task_123",
        "task": "Test task",
        "complexity": "medium",
        "status": "active",
        "progress": 50,
        "created": "2024-01-01T12:00:00",
        "subtasks": [
            {
                "id": "subtask_1",
                "description": "First step",
                "dependencies": [],
                "tools_needed": ["tool1"],
                "estimated_steps": 2,
                "priority": "high",
                "status": "completed"
            },
            {
                "id": "subtask_2",
                "description": "Second step",
                "dependencies": ["subtask_1"],
                "tools_needed": ["tool2"],
                "estimated_steps": 3,
                "priority": "medium",
                "status": "in_progress"
            }
        ],
        "success_criteria": ["All subtasks completed", "Tests pass"],
        "risks": [
            {"risk": "API timeout", "mitigation": "Add retry logic"}
        ],
        "estimated_total_steps": 10
    }


# ============================================================================
# CLEANUP
# ============================================================================

@pytest.fixture(autouse=True)
def cleanup_agent_contexts():
    """Automatically cleanup agent contexts after each test."""
    yield
    # Clear all contexts
    AgentContext._contexts.clear()


@pytest.fixture(autouse=True)
def reset_memory_index():
    """Reset memory index between tests."""
    yield
    Memory.index.clear()
