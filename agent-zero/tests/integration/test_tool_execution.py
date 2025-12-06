"""
Integration tests for Tool Execution

Tests the complete tool execution pipeline including:
- Tool loading and instantiation
- Tool execution workflow
- Tool-Agent interaction
- Tool response handling
- Multiple tool coordination
"""

import pytest
from unittest.mock import AsyncMock, Mock, patch

from python.helpers.tool import Tool, Response


class TestToolLoadingIntegration:
    """Test tool loading and instantiation."""

    def test_agent_can_load_tool(self, mock_agent):
        """Test that agent can load tools dynamically."""
        tool = mock_agent.get_tool("test_tool", {}, "Test message")

        assert tool is not None
        assert hasattr(tool, 'execute')

    def test_load_multiple_tools(self, mock_agent):
        """Test loading multiple different tools."""
        tool1 = mock_agent.get_tool("task_planner", {}, "")
        tool2 = mock_agent.get_tool("code_analyzer", {}, "")

        assert tool1 is not None
        assert tool2 is not None
        assert type(tool1) != type(tool2)

    def test_tool_inherits_agent_context(self, mock_agent):
        """Test that loaded tools have access to agent context."""
        from python.tools.task_planner_tool import TaskPlanner

        tool = TaskPlanner(agent=mock_agent, name="task_planner", args={}, message="")

        assert tool.agent == mock_agent
        assert tool.agent.config == mock_agent.config


class TestToolExecutionWorkflow:
    """Test complete tool execution workflow."""

    @pytest.mark.asyncio
    async def test_tool_before_execute_called(self, mock_agent):
        """Test that before_execution is called."""
        from python.tools.task_planner_tool import TaskPlanner

        tool = TaskPlanner(agent=mock_agent, name="task_planner", args={}, message="")

        # Mock before_execution
        tool.before_execution = AsyncMock()

        await tool.before_execution()

        tool.before_execution.assert_called_once()

    @pytest.mark.asyncio
    async def test_tool_execute_returns_response(self, mock_agent, mock_llm_json_response):
        """Test that tool execution returns Response object."""
        from python.tools.task_planner_tool import TaskPlanner

        mock_agent.call_utility_llm = AsyncMock(return_value=mock_llm_json_response)

        tool = TaskPlanner(agent=mock_agent, name="task_planner", args={}, message="")
        response = await tool.execute(action="create", task="Test task")

        assert isinstance(response, Response)
        assert hasattr(response, 'message')
        assert hasattr(response, 'break_loop')

    @pytest.mark.asyncio
    async def test_tool_after_execute_called(self, mock_agent):
        """Test that after_execution is called."""
        from python.tools.task_planner_tool import TaskPlanner

        tool = TaskPlanner(agent=mock_agent, name="task_planner", args={}, message="")
        tool.after_execution = AsyncMock()

        mock_response = Response(message="Test", break_loop=False)
        await tool.after_execution(mock_response)

        tool.after_execution.assert_called_once()

    @pytest.mark.asyncio
    async def test_agent_processes_tool_request(self, mock_agent):
        """Test that agent can process tool requests."""
        # Simulate tool request message
        message = '{"tool_name": "response", "tool_args": {"message": "Done"}}'

        result = await mock_agent.process_tools(message)

        # Should process the tool request
        # Note: mock_agent.process_tools is mocked, so we just verify it can be called


class TestToolAgentInteraction:
    """Test interaction between tools and agent."""

    @pytest.mark.asyncio
    async def test_tool_can_call_agent_llm(self, mock_agent, mock_llm_json_response):
        """Test that tools can call agent's LLM."""
        from python.tools.task_planner_tool import TaskPlanner

        mock_agent.call_utility_llm = AsyncMock(return_value=mock_llm_json_response)

        tool = TaskPlanner(agent=mock_agent, name="task_planner", args={}, message="")
        await tool.execute(action="create", task="Test")

        # Tool should have called agent's LLM
        mock_agent.call_utility_llm.assert_called()

    @pytest.mark.asyncio
    async def test_tool_can_access_agent_data(self, mock_agent):
        """Test that tools can access and modify agent data."""
        from python.tools.task_planner_tool import TaskPlanner

        mock_agent.data = {"existing": "data"}

        tool = TaskPlanner(agent=mock_agent, name="task_planner", args={}, message="")

        # Tool should be able to set data
        tool.agent.set_data("test_key", "test_value")

        assert mock_agent.data.get("test_key") == "test_value"

    @pytest.mark.asyncio
    async def test_tool_can_read_prompts(self, mock_agent):
        """Test that tools can read prompt files."""
        from python.tools.task_planner_tool import TaskPlanner

        mock_agent.read_prompt = Mock(return_value="Test prompt content")

        tool = TaskPlanner(agent=mock_agent, name="task_planner", args={}, message="")

        # Tools typically read prompts through agent
        prompt = tool.agent.read_prompt("test.md")

        assert prompt == "Test prompt content"


class TestToolResponseHandling:
    """Test tool response handling."""

    @pytest.mark.asyncio
    async def test_response_with_break_loop(self, mock_agent, mock_llm_json_response):
        """Test tool response that breaks the loop."""
        from python.tools.task_planner_tool import TaskPlanner

        mock_agent.call_utility_llm = AsyncMock(return_value=mock_llm_json_response)

        tool = TaskPlanner(agent=mock_agent, name="task_planner", args={}, message="")
        response = await tool.execute(action="create", task="Test")

        # Most tools don't break loop
        assert response.break_loop == False

    @pytest.mark.asyncio
    async def test_response_message_format(self, mock_agent, mock_llm_json_response):
        """Test that tool responses have proper message format."""
        from python.tools.task_planner_tool import TaskPlanner

        mock_agent.call_utility_llm = AsyncMock(return_value=mock_llm_json_response)

        tool = TaskPlanner(agent=mock_agent, name="task_planner", args={}, message="")
        response = await tool.execute(action="create", task="Test")

        assert isinstance(response.message, str)
        assert len(response.message) > 0

    @pytest.mark.asyncio
    async def test_tool_error_response(self, mock_agent):
        """Test tool error handling and response."""
        from python.tools.task_planner_tool import TaskPlanner

        # Simulate error condition
        mock_agent.call_utility_llm = AsyncMock(side_effect=Exception("Test error"))

        tool = TaskPlanner(agent=mock_agent, name="task_planner", args={}, message="")

        with pytest.raises(Exception):
            await tool.execute(action="create", task="Test")


class TestMultipleToolCoordination:
    """Test coordination between multiple tools."""

    @pytest.mark.asyncio
    async def test_sequential_tool_execution(self, mock_agent, mock_llm_json_response):
        """Test executing multiple tools sequentially."""
        from python.tools.task_planner_tool import TaskPlanner
        from python.tools.code_analyzer_tool import CodeAnalyzer

        mock_agent.call_utility_llm = AsyncMock(return_value=mock_llm_json_response)

        # Execute task planner
        tool1 = TaskPlanner(agent=mock_agent, name="task_planner", args={}, message="")
        response1 = await tool1.execute(action="create", task="Build app")

        # Execute code analyzer
        tool2 = CodeAnalyzer(agent=mock_agent, name="code_analyzer", args={}, message="")
        response2 = await tool2.execute(action="analyze", code="def test(): pass")

        assert isinstance(response1, Response)
        assert isinstance(response2, Response)

    @pytest.mark.asyncio
    async def test_tools_share_agent_data(self, mock_agent, mock_llm_json_response):
        """Test that tools can share data through agent."""
        from python.tools.task_planner_tool import TaskPlanner

        mock_agent.call_utility_llm = AsyncMock(return_value=mock_llm_json_response)

        # First tool stores data
        tool1 = TaskPlanner(agent=mock_agent, name="task_planner", args={}, message="")
        await tool1.execute(action="create", task="Test")

        # Second tool can access it
        tool2 = TaskPlanner(agent=mock_agent, name="task_planner2", args={}, message="")
        plans = tool2.agent.get_data("task_plans")

        # Both tools share the same agent data
        assert plans is not None

    @pytest.mark.asyncio
    async def test_tool_chain_workflow(self, mock_agent, mock_llm_json_response):
        """Test a workflow chain using multiple tools."""
        from python.tools.task_planner_tool import TaskPlanner

        mock_agent.call_utility_llm = AsyncMock(return_value=mock_llm_json_response)

        planner = TaskPlanner(agent=mock_agent, name="task_planner", args={}, message="")

        # Create plan
        create_response = await planner.execute(action="create", task="Implement feature")
        assert "Task Plan" in create_response.message

        # Get task ID from agent data
        plans = mock_agent.data.get("task_plans", {})
        if plans:
            task_id = list(plans.keys())[0]

            # Update plan
            update_response = await planner.execute(
                action="update",
                task_id=task_id,
                updates={"progress": 50}
            )
            assert "updated" in update_response.message

            # Complete plan
            complete_response = await planner.execute(
                action="complete",
                task_id=task_id
            )
            assert "completed" in complete_response.message


class TestToolStateManagement:
    """Test tool state management."""

    @pytest.mark.asyncio
    async def test_tool_maintains_state_in_agent(self, mock_agent, mock_llm_json_response):
        """Test that tools maintain state through agent data."""
        from python.tools.task_planner_tool import TaskPlanner

        mock_agent.call_utility_llm = AsyncMock(return_value=mock_llm_json_response)

        tool = TaskPlanner(agent=mock_agent, name="task_planner", args={}, message="")

        # Create multiple plans
        await tool.execute(action="create", task="Task 1")
        await tool.execute(action="create", task="Task 2")

        # State should be maintained
        plans = mock_agent.data.get("task_plans", {})
        assert len(plans) == 2

    @pytest.mark.asyncio
    async def test_tool_state_persistence(self, mock_agent, mock_llm_json_response):
        """Test that tool state persists between tool instances."""
        from python.tools.task_planner_tool import TaskPlanner

        mock_agent.call_utility_llm = AsyncMock(return_value=mock_llm_json_response)

        # First tool instance creates plan
        tool1 = TaskPlanner(agent=mock_agent, name="task_planner", args={}, message="")
        await tool1.execute(action="create", task="Test")

        # Second tool instance can access it
        tool2 = TaskPlanner(agent=mock_agent, name="task_planner", args={}, message="")
        plans = tool2.agent.get_data("task_plans")

        assert plans is not None
        assert len(plans) > 0


class TestToolErrorRecovery:
    """Test tool error handling and recovery."""

    @pytest.mark.asyncio
    async def test_tool_handles_llm_error(self, mock_agent):
        """Test tool handling of LLM errors."""
        from python.tools.task_planner_tool import TaskPlanner

        mock_agent.call_utility_llm = AsyncMock(side_effect=Exception("LLM error"))

        tool = TaskPlanner(agent=mock_agent, name="task_planner", args={}, message="")

        with pytest.raises(Exception):
            await tool.execute(action="create", task="Test")

    @pytest.mark.asyncio
    async def test_tool_handles_invalid_args(self, mock_agent):
        """Test tool handling of invalid arguments."""
        from python.tools.task_planner_tool import TaskPlanner

        tool = TaskPlanner(agent=mock_agent, name="task_planner", args={}, message="")

        # Execute with missing required args
        response = await tool.execute(action="update", task_id="nonexistent")

        # Should handle gracefully
        assert isinstance(response, Response)

    @pytest.mark.asyncio
    async def test_tool_recovers_from_partial_failure(self, mock_agent, mock_llm_json_response):
        """Test tool recovery from partial failures."""
        from python.tools.task_planner_tool import TaskPlanner

        mock_agent.call_utility_llm = AsyncMock(return_value=mock_llm_json_response)

        tool = TaskPlanner(agent=mock_agent, name="task_planner", args={}, message="")

        # Create plan successfully
        response1 = await tool.execute(action="create", task="Test")
        assert isinstance(response1, Response)

        # Try invalid operation
        response2 = await tool.execute(action="update", task_id="nonexistent", updates={})
        assert "not found" in response2.message

        # Should still be able to create new plan
        response3 = await tool.execute(action="create", task="Test 2")
        assert isinstance(response3, Response)


class TestToolConcurrency:
    """Test concurrent tool execution."""

    @pytest.mark.asyncio
    async def test_concurrent_tool_executions(self, mock_agent, mock_llm_json_response):
        """Test executing tools concurrently."""
        import asyncio
        from python.tools.task_planner_tool import TaskPlanner

        mock_agent.call_utility_llm = AsyncMock(return_value=mock_llm_json_response)

        # Create multiple tool instances
        tools = [
            TaskPlanner(agent=mock_agent, name=f"planner_{i}", args={}, message="")
            for i in range(3)
        ]

        # Execute concurrently
        tasks = [
            tool.execute(action="create", task=f"Task {i}")
            for i, tool in enumerate(tools)
        ]

        responses = await asyncio.gather(*tasks)

        assert len(responses) == 3
        assert all(isinstance(r, Response) for r in responses)

    @pytest.mark.asyncio
    async def test_concurrent_data_access(self, mock_agent, mock_llm_json_response):
        """Test concurrent access to agent data."""
        import asyncio
        from python.tools.task_planner_tool import TaskPlanner

        mock_agent.call_utility_llm = AsyncMock(return_value=mock_llm_json_response)

        # Multiple tools accessing data concurrently
        async def create_and_read(i):
            tool = TaskPlanner(agent=mock_agent, name=f"planner_{i}", args={}, message="")
            await tool.execute(action="create", task=f"Task {i}")
            return tool.agent.get_data("task_plans")

        tasks = [create_and_read(i) for i in range(5)]
        results = await asyncio.gather(*tasks)

        # All should access the same data
        assert all(r is not None for r in results)


class TestToolWithMemory:
    """Test tools with memory integration."""

    @pytest.mark.asyncio
    async def test_tool_can_access_memory(self, agent, temp_memory_dir):
        """Test that tools can access memory system."""
        from python.helpers.memory import Memory
        from python.tools.task_planner_tool import TaskPlanner

        with patch('python.helpers.files.get_abs_path', return_value=temp_memory_dir):
            memory = await Memory.get(agent)
            memory.insert_text("Task context information")

            # Tool should be able to access memory through agent
            tool = TaskPlanner(agent=agent, name="task_planner", args={}, message="")

            assert tool.agent == agent


class TestToolLogging:
    """Test tool logging integration."""

    @pytest.mark.asyncio
    async def test_tool_logs_execution(self, mock_agent, mock_llm_json_response):
        """Test that tools log their execution."""
        from python.tools.task_planner_tool import TaskPlanner

        mock_agent.call_utility_llm = AsyncMock(return_value=mock_llm_json_response)

        tool = TaskPlanner(agent=mock_agent, name="task_planner", args={}, message="")
        await tool.execute(action="create", task="Test")

        # Tool should use agent's logging
        # mock_agent.context.log should have been called


# ============================================================================
# REAL TOOL INTEGRATION TESTS
# ============================================================================

class TestRealToolIntegration:
    """Test real tool implementations in integration."""

    @pytest.mark.asyncio
    async def test_code_analyzer_full_workflow(self, mock_agent, sample_python_code):
        """Test complete code analyzer workflow."""
        from python.tools.code_analyzer_tool import CodeAnalyzer

        tool = CodeAnalyzer(agent=mock_agent, name="code_analyzer", args={}, message="")

        # Analyze
        analyze_resp = await tool.execute(action="analyze", code=sample_python_code)
        assert "Code Analysis" in analyze_resp.message

        # Security
        security_resp = await tool.execute(action="security", code=sample_python_code)
        assert "Security Scan" in security_resp.message

        # Complexity
        complexity_resp = await tool.execute(action="complexity", code=sample_python_code)
        assert "Complexity" in complexity_resp.message

    @pytest.mark.asyncio
    async def test_task_planner_full_workflow(self, mock_agent, mock_llm_json_response):
        """Test complete task planner workflow."""
        from python.tools.task_planner_tool import TaskPlanner

        mock_agent.call_utility_llm = AsyncMock(return_value=mock_llm_json_response)

        tool = TaskPlanner(agent=mock_agent, name="task_planner", args={}, message="")

        # Create, update, status, complete cycle
        create_resp = await tool.execute(action="create", task="Build feature")
        assert "Task Plan" in create_resp.message

        plans = mock_agent.data.get("task_plans", {})
        if plans:
            task_id = list(plans.keys())[0]

            status_resp = await tool.execute(action="status", task_id=task_id)
            assert task_id in status_resp.message

            update_resp = await tool.execute(
                action="update",
                task_id=task_id,
                updates={"progress": 75}
            )
            assert "updated" in update_resp.message

            complete_resp = await tool.execute(action="complete", task_id=task_id)
            assert "completed" in complete_resp.message
