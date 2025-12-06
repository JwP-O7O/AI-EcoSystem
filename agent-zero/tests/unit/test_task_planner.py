"""
Unit tests for Task Planner Tool

Tests cover:
- Task plan creation
- Plan updates
- Status queries
- Task completion
- Adaptive replanning
- Error handling
"""

import pytest
import json
from unittest.mock import AsyncMock, Mock, patch
from python.tools.task_planner_tool import TaskPlanner
from python.helpers.tool import Response


class TestTaskPlannerCreation:
    """Test task plan creation functionality."""

    @pytest.mark.asyncio
    async def test_create_plan_success(self, mock_agent, mock_llm_json_response):
        """Test successful task plan creation."""
        mock_agent.call_utility_llm = AsyncMock(return_value=mock_llm_json_response)

        tool = TaskPlanner(agent=mock_agent, name="task_planner", args={}, message="")
        response = await tool.execute(action="create", task="Build a web app", context="Python Flask")

        assert isinstance(response, Response)
        assert not response.break_loop
        assert "Task Plan" in response.message
        assert "Build a web app" in response.message or "Test task" in response.message
        mock_agent.call_utility_llm.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_plan_with_empty_task(self, mock_agent):
        """Test plan creation with empty task."""
        mock_agent.call_utility_llm = AsyncMock(return_value='{"task": "", "complexity": "low"}')

        tool = TaskPlanner(agent=mock_agent, name="task_planner", args={}, message="")
        response = await tool.execute(action="create", task="", context="")

        assert isinstance(response, Response)

    @pytest.mark.asyncio
    async def test_create_plan_saves_to_agent_data(self, mock_agent, mock_llm_json_response):
        """Test that created plan is saved to agent data."""
        mock_agent.call_utility_llm = AsyncMock(return_value=mock_llm_json_response)

        tool = TaskPlanner(agent=mock_agent, name="task_planner", args={}, message="")
        await tool.execute(action="create", task="Test task", context="")

        # Verify plan was saved
        assert "task_plans" in mock_agent.data
        plans = mock_agent.data["task_plans"]
        assert len(plans) > 0

    @pytest.mark.asyncio
    async def test_create_plan_invalid_json(self, mock_agent):
        """Test plan creation with invalid JSON response."""
        mock_agent.call_utility_llm = AsyncMock(return_value="Not valid JSON at all")

        tool = TaskPlanner(agent=mock_agent, name="task_planner", args={}, message="")
        response = await tool.execute(action="create", task="Test task", context="")

        assert "Failed to create task plan" in response.message

    @pytest.mark.asyncio
    async def test_create_plan_with_context(self, mock_agent, mock_llm_json_response):
        """Test plan creation with additional context."""
        mock_agent.call_utility_llm = AsyncMock(return_value=mock_llm_json_response)

        tool = TaskPlanner(agent=mock_agent, name="task_planner", args={}, message="")
        response = await tool.execute(
            action="create",
            task="Deploy application",
            context="AWS cloud, Docker containers"
        )

        # Verify context was passed to LLM
        call_args = mock_agent.call_utility_llm.call_args
        assert "AWS cloud" in call_args[1]["msg"] or "Context" in call_args[1]["msg"]


class TestTaskPlannerUpdate:
    """Test task plan update functionality."""

    @pytest.mark.asyncio
    async def test_update_plan_success(self, mock_agent):
        """Test successful plan update."""
        # Setup existing plan
        mock_agent.data["task_plans"] = {
            "task_123": {
                "id": "task_123",
                "task": "Original task",
                "status": "active",
                "progress": 0
            }
        }

        tool = TaskPlanner(agent=mock_agent, name="task_planner", args={}, message="")
        response = await tool.execute(
            action="update",
            task_id="task_123",
            updates={"progress": 50, "status": "in_progress"}
        )

        assert "updated successfully" in response.message
        assert mock_agent.data["task_plans"]["task_123"]["progress"] == 50
        assert mock_agent.data["task_plans"]["task_123"]["status"] == "in_progress"

    @pytest.mark.asyncio
    async def test_update_nonexistent_plan(self, mock_agent):
        """Test updating a non-existent plan."""
        mock_agent.data["task_plans"] = {}

        tool = TaskPlanner(agent=mock_agent, name="task_planner", args={}, message="")
        response = await tool.execute(
            action="update",
            task_id="nonexistent",
            updates={"progress": 50}
        )

        assert "not found" in response.message

    @pytest.mark.asyncio
    async def test_update_plan_adds_timestamp(self, mock_agent):
        """Test that update adds timestamp."""
        mock_agent.data["task_plans"] = {
            "task_123": {"id": "task_123", "task": "Test"}
        }

        tool = TaskPlanner(agent=mock_agent, name="task_planner", args={}, message="")
        await tool.execute(action="update", task_id="task_123", updates={"progress": 25})

        assert "updated" in mock_agent.data["task_plans"]["task_123"]


class TestTaskPlannerStatus:
    """Test task status query functionality."""

    @pytest.mark.asyncio
    async def test_get_status_success(self, mock_agent, generate_mock_task_plan):
        """Test getting status of existing plan."""
        plan = generate_mock_task_plan()
        mock_agent.data["task_plans"] = {"task_123": plan}

        tool = TaskPlanner(agent=mock_agent, name="task_planner", args={}, message="")
        response = await tool.execute(action="status", task_id="task_123")

        assert "Task Plan" in response.message
        assert "task_123" in response.message

    @pytest.mark.asyncio
    async def test_get_status_nonexistent(self, mock_agent):
        """Test getting status of non-existent plan."""
        mock_agent.data["task_plans"] = {}

        tool = TaskPlanner(agent=mock_agent, name="task_planner", args={}, message="")
        response = await tool.execute(action="status", task_id="nonexistent")

        assert "not found" in response.message


class TestTaskPlannerCompletion:
    """Test task completion functionality."""

    @pytest.mark.asyncio
    async def test_complete_task_success(self, mock_agent):
        """Test marking task as completed."""
        mock_agent.data["task_plans"] = {
            "task_123": {
                "id": "task_123",
                "task": "Test task",
                "status": "in_progress",
                "progress": 80
            }
        }

        tool = TaskPlanner(agent=mock_agent, name="task_planner", args={}, message="")
        response = await tool.execute(action="complete", task_id="task_123")

        assert "completed" in response.message
        plan = mock_agent.data["task_plans"]["task_123"]
        assert plan["status"] == "completed"
        assert plan["progress"] == 100
        assert "completed" in plan

    @pytest.mark.asyncio
    async def test_complete_nonexistent_task(self, mock_agent):
        """Test completing non-existent task."""
        mock_agent.data["task_plans"] = {}

        tool = TaskPlanner(agent=mock_agent, name="task_planner", args={}, message="")
        response = await tool.execute(action="complete", task_id="nonexistent")

        assert "not found" in response.message


class TestTaskPlannerReplanning:
    """Test adaptive replanning functionality."""

    @pytest.mark.asyncio
    async def test_replan_success(self, mock_agent, mock_llm_json_response):
        """Test successful replanning."""
        mock_agent.data["task_plans"] = {
            "task_123": {
                "id": "task_123",
                "task": "Original task",
                "status": "active"
            }
        }
        mock_agent.call_utility_llm = AsyncMock(return_value=mock_llm_json_response)

        tool = TaskPlanner(agent=mock_agent, name="task_planner", args={}, message="")
        response = await tool.execute(
            action="replan",
            task_id="task_123",
            reason="Encountered blocker: API deprecated"
        )

        assert "adapted" in response.message.lower()
        plan = mock_agent.data["task_plans"]["task_123"]
        assert "replan_history" in plan
        assert len(plan["replan_history"]) == 1

    @pytest.mark.asyncio
    async def test_replan_preserves_history(self, mock_agent, mock_llm_json_response):
        """Test that replanning preserves history."""
        mock_agent.data["task_plans"] = {
            "task_123": {
                "id": "task_123",
                "task": "Test",
                "replan_history": [{"reason": "First replan"}]
            }
        }
        mock_agent.call_utility_llm = AsyncMock(return_value=mock_llm_json_response)

        tool = TaskPlanner(agent=mock_agent, name="task_planner", args={}, message="")
        await tool.execute(
            action="replan",
            task_id="task_123",
            reason="Second replan"
        )

        plan = mock_agent.data["task_plans"]["task_123"]
        assert len(plan["replan_history"]) == 2


class TestTaskPlannerEdgeCases:
    """Test edge cases and error handling."""

    @pytest.mark.asyncio
    async def test_unknown_action(self, mock_agent):
        """Test handling of unknown action."""
        tool = TaskPlanner(agent=mock_agent, name="task_planner", args={}, message="")
        response = await tool.execute(action="invalid_action")

        assert "Unknown action" in response.message

    @pytest.mark.asyncio
    async def test_create_plan_llm_timeout(self, mock_agent):
        """Test handling of LLM timeout."""
        mock_agent.call_utility_llm = AsyncMock(side_effect=TimeoutError("LLM timeout"))

        tool = TaskPlanner(agent=mock_agent, name="task_planner", args={}, message="")

        with pytest.raises(TimeoutError):
            await tool.execute(action="create", task="Test task")

    @pytest.mark.asyncio
    async def test_task_id_generation_unique(self, mock_agent, mock_llm_json_response):
        """Test that generated task IDs are unique."""
        mock_agent.call_utility_llm = AsyncMock(return_value=mock_llm_json_response)

        tool = TaskPlanner(agent=mock_agent, name="task_planner", args={}, message="")

        # Create multiple plans
        await tool.execute(action="create", task="Task 1")
        await tool.execute(action="create", task="Task 2")

        plans = mock_agent.data["task_plans"]
        task_ids = list(plans.keys())
        assert len(task_ids) == 2
        assert task_ids[0] != task_ids[1]


class TestTaskPlannerPrompts:
    """Test prompt generation."""

    def test_planning_prompt_format(self, mock_agent):
        """Test that planning prompt has required format."""
        tool = TaskPlanner(agent=mock_agent, name="task_planner", args={}, message="")
        prompt = tool._get_planning_prompt()

        assert "JSON" in prompt
        assert "subtasks" in prompt
        assert "complexity" in prompt

    def test_replanning_prompt_format(self, mock_agent):
        """Test that replanning prompt has required format."""
        tool = TaskPlanner(agent=mock_agent, name="task_planner", args={}, message="")
        prompt = tool._get_replanning_prompt()

        assert "plan" in prompt.lower()
        assert "JSON" in prompt


class TestTaskPlannerFormatting:
    """Test response formatting."""

    def test_format_plan_response(self, mock_agent, generate_mock_task_plan):
        """Test plan formatting."""
        tool = TaskPlanner(agent=mock_agent, name="task_planner", args={}, message="")
        plan = generate_mock_task_plan()
        formatted = tool._format_plan_response(plan)

        assert "Task Plan" in formatted
        assert "task_123" in formatted
        assert "Subtasks" in formatted
        assert "Success Criteria" in formatted

    def test_format_plan_minimal(self, mock_agent):
        """Test formatting of minimal plan."""
        tool = TaskPlanner(agent=mock_agent, name="task_planner", args={}, message="")
        minimal_plan = {"id": "test_id", "task": "Test"}
        formatted = tool._format_plan_response(minimal_plan)

        assert "test_id" in formatted
        assert "Test" in formatted


# ============================================================================
# PARAMETRIZED TESTS
# ============================================================================

@pytest.mark.parametrize("complexity", ["low", "medium", "high", "very-high"])
@pytest.mark.asyncio
async def test_create_plan_all_complexity_levels(mock_agent, complexity):
    """Test plan creation with different complexity levels."""
    response_json = f'{{"task": "Test", "complexity": "{complexity}", "subtasks": [], "success_criteria": [], "risks": [], "estimated_total_steps": 5}}'
    mock_agent.call_utility_llm = AsyncMock(return_value=response_json)

    tool = TaskPlanner(agent=mock_agent, name="task_planner", args={}, message="")
    response = await tool.execute(action="create", task="Test task")

    assert isinstance(response, Response)
    plan_id = list(mock_agent.data["task_plans"].keys())[0]
    assert mock_agent.data["task_plans"][plan_id]["complexity"] == complexity


@pytest.mark.parametrize("progress", [0, 25, 50, 75, 100])
@pytest.mark.asyncio
async def test_update_plan_various_progress(mock_agent, progress):
    """Test updating plan with various progress values."""
    mock_agent.data["task_plans"] = {
        "task_123": {"id": "task_123", "task": "Test", "progress": 0}
    }

    tool = TaskPlanner(agent=mock_agent, name="task_planner", args={}, message="")
    await tool.execute(action="update", task_id="task_123", updates={"progress": progress})

    assert mock_agent.data["task_plans"]["task_123"]["progress"] == progress
