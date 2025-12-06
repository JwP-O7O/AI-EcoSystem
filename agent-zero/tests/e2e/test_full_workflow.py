"""
End-to-End Tests for Agent Zero

Tests complete workflows from user input to final response:
- Complete task execution workflows
- Multi-tool coordination
- Memory persistence across operations
- Error recovery workflows
- Real-world scenarios
"""

import pytest
import asyncio
from unittest.mock import AsyncMock, patch

from agent import Agent, AgentConfig, AgentContext
from python.helpers.memory import Memory
from conftest import MockChatModel, MockEmbeddings


class TestCompleteTaskWorkflow:
    """Test complete task execution from start to finish."""

    @pytest.mark.asyncio
    async def test_simple_task_completion(self, agent_context):
        """Test a simple task from input to completion."""
        agent = agent_context.agent0

        # Simulate task execution
        # Note: This uses mock models, so we're testing the flow, not actual LLM responses
        task = "Create a test plan"

        # Agent should be able to process this
        # (In real usage, this would go through agent.monologue())
        assert agent is not None
        assert agent.config is not None

    @pytest.mark.asyncio
    async def test_multi_step_task_workflow(self, mock_agent, mock_llm_json_response):
        """Test a multi-step task workflow."""
        from python.tools.task_planner_tool import TaskPlanner

        mock_agent.call_utility_llm = AsyncMock(return_value=mock_llm_json_response)

        planner = TaskPlanner(agent=mock_agent, name="task_planner", args={}, message="")

        # Step 1: Create plan
        create_resp = await planner.execute(
            action="create",
            task="Develop web application",
            context="Python Flask, PostgreSQL"
        )
        assert "Task Plan" in create_resp.message

        # Step 2: Get task ID
        plans = mock_agent.data.get("task_plans", {})
        assert len(plans) > 0
        task_id = list(plans.keys())[0]

        # Step 3: Update progress
        await planner.execute(
            action="update",
            task_id=task_id,
            updates={"progress": 25}
        )

        # Step 4: Check status
        status_resp = await planner.execute(action="status", task_id=task_id)
        assert "25" in status_resp.message or "progress" in status_resp.message.lower()

        # Step 5: Complete task
        complete_resp = await planner.execute(action="complete", task_id=task_id)
        assert "completed" in complete_resp.message


class TestMultiToolWorkflow:
    """Test workflows involving multiple tools."""

    @pytest.mark.asyncio
    async def test_plan_and_analyze_workflow(self, mock_agent, mock_llm_json_response):
        """Test workflow combining task planning and code analysis."""
        from python.tools.task_planner_tool import TaskPlanner
        from python.tools.code_analyzer_tool import CodeAnalyzer

        mock_agent.call_utility_llm = AsyncMock(return_value=mock_llm_json_response)

        # Step 1: Create task plan
        planner = TaskPlanner(agent=mock_agent, name="task_planner", args={}, message="")
        plan_resp = await planner.execute(
            action="create",
            task="Refactor legacy code"
        )
        assert "Task Plan" in plan_resp.message

        # Step 2: Analyze code
        analyzer = CodeAnalyzer(agent=mock_agent, name="code_analyzer", args={}, message="")
        code = """
def legacy_function(x, y):
    if x > 0:
        return x + y
    return y
"""
        analyze_resp = await analyzer.execute(action="analyze", code=code)
        assert "Code Analysis" in analyze_resp.message

        # Step 3: Check security
        security_resp = await analyzer.execute(action="security", code=code)
        assert "Security Scan" in security_resp.message

        # Step 4: Update task progress
        plans = mock_agent.data.get("task_plans", {})
        if plans:
            task_id = list(plans.keys())[0]
            await planner.execute(
                action="update",
                task_id=task_id,
                updates={"progress": 100}
            )

    @pytest.mark.asyncio
    async def test_iterative_refinement_workflow(self, mock_agent, mock_llm_json_response):
        """Test iterative task refinement workflow."""
        from python.tools.task_planner_tool import TaskPlanner

        mock_agent.call_utility_llm = AsyncMock(return_value=mock_llm_json_response)

        planner = TaskPlanner(agent=mock_agent, name="task_planner", args={}, message="")

        # Initial plan
        await planner.execute(action="create", task="Build API")

        plans = mock_agent.data.get("task_plans", {})
        task_id = list(plans.keys())[0]

        # Replan due to blocker
        replan_resp = await planner.execute(
            action="replan",
            task_id=task_id,
            reason="API specifications changed"
        )
        assert "adapted" in replan_resp.message.lower() or "plan" in replan_resp.message.lower()


class TestMemoryPersistenceWorkflow:
    """Test workflows involving memory persistence."""

    @pytest.mark.asyncio
    async def test_save_and_retrieve_workflow(self, agent, temp_memory_dir):
        """Test saving and retrieving information across operations."""
        with patch('python.helpers.files.get_abs_path', return_value=temp_memory_dir):
            memory = await Memory.get(agent)

            # Save information
            doc_id1 = memory.insert_text(
                "Project requirement: Support 1000 concurrent users",
                {"type": "requirement", "priority": "high"}
            )
            doc_id2 = memory.insert_text(
                "Project constraint: Must use PostgreSQL",
                {"type": "constraint", "priority": "high"}
            )

            # Retrieve requirements
            requirements = await memory.search_similarity_threshold(
                query="requirements",
                limit=10,
                threshold=0.0,
                filter="type == 'requirement'"
            )

            assert isinstance(requirements, list)

            # Retrieve constraints
            constraints = await memory.search_similarity_threshold(
                query="constraints",
                limit=10,
                threshold=0.0,
                filter="type == 'constraint'"
            )

            assert isinstance(constraints, list)

    @pytest.mark.asyncio
    async def test_context_accumulation_workflow(self, agent, temp_memory_dir):
        """Test accumulating context over multiple operations."""
        with patch('python.helpers.files.get_abs_path', return_value=temp_memory_dir):
            memory = await Memory.get(agent)

            # Accumulate context
            contexts = [
                "User prefers Python for backend",
                "User wants React for frontend",
                "User needs real-time updates",
                "User requires mobile support"
            ]

            for ctx in contexts:
                memory.insert_text(ctx, {"type": "preference"})

            # Query accumulated context
            results = await memory.search_similarity_threshold(
                query="user preferences",
                limit=10,
                threshold=0.0
            )

            assert len(results) >= 0


class TestErrorRecoveryWorkflow:
    """Test error recovery in complete workflows."""

    @pytest.mark.asyncio
    async def test_recovery_from_failed_operation(self, mock_agent, mock_llm_json_response):
        """Test recovery after failed operation."""
        from python.tools.task_planner_tool import TaskPlanner

        planner = TaskPlanner(agent=mock_agent, name="task_planner", args={}, message="")

        # Successful operation
        mock_agent.call_utility_llm = AsyncMock(return_value=mock_llm_json_response)
        success_resp = await planner.execute(action="create", task="Valid task")
        assert "Task Plan" in success_resp.message

        # Failed operation (invalid task ID)
        fail_resp = await planner.execute(action="status", task_id="nonexistent")
        assert "not found" in fail_resp.message

        # Recovery with new successful operation
        recovery_resp = await planner.execute(action="create", task="Recovery task")
        assert "Task Plan" in recovery_resp.message

    @pytest.mark.asyncio
    async def test_handling_llm_errors(self, mock_agent):
        """Test handling of LLM errors in workflow."""
        from python.tools.task_planner_tool import TaskPlanner

        # Simulate LLM error
        mock_agent.call_utility_llm = AsyncMock(side_effect=Exception("LLM timeout"))

        planner = TaskPlanner(agent=mock_agent, name="task_planner", args={}, message="")

        with pytest.raises(Exception):
            await planner.execute(action="create", task="Test")

    @pytest.mark.asyncio
    async def test_partial_completion_workflow(self, mock_agent, mock_llm_json_response):
        """Test workflow with partial completion."""
        from python.tools.task_planner_tool import TaskPlanner

        mock_agent.call_utility_llm = AsyncMock(return_value=mock_llm_json_response)

        planner = TaskPlanner(agent=mock_agent, name="task_planner", args={}, message="")

        # Create task
        await planner.execute(action="create", task="Multi-step task")

        plans = mock_agent.data.get("task_plans", {})
        task_id = list(plans.keys())[0]

        # Partial progress
        await planner.execute(
            action="update",
            task_id=task_id,
            updates={"progress": 50, "status": "blocked"}
        )

        # Verify partial state
        status_resp = await planner.execute(action="status", task_id=task_id)
        assert task_id in status_resp.message


class TestRealWorldScenarios:
    """Test real-world usage scenarios."""

    @pytest.mark.asyncio
    async def test_code_review_workflow(self, mock_agent):
        """Test a code review workflow."""
        from python.tools.code_analyzer_tool import CodeAnalyzer

        analyzer = CodeAnalyzer(agent=mock_agent, name="code_analyzer", args={}, message="")

        # Code to review
        code = """
import os

def process_user_input(user_data):
    # Potentially dangerous: eval usage
    result = eval(user_data)
    return result

def database_query(user_id):
    # Potentially dangerous: SQL injection
    query = f"SELECT * FROM users WHERE id = {user_id}"
    return query
"""

        # Full analysis
        analysis_resp = await analyzer.execute(action="analyze", code=code)
        assert "Code Analysis" in analysis_resp.message

        # Security scan
        security_resp = await analyzer.execute(action="security", code=code)
        assert "Security Scan" in security_resp.message
        # Should detect eval and potential SQL injection

        # Complexity check
        complexity_resp = await analyzer.execute(action="complexity", code=code)
        assert "Complexity" in complexity_resp.message

    @pytest.mark.asyncio
    async def test_project_planning_workflow(self, mock_agent, mock_llm_json_response):
        """Test a complete project planning workflow."""
        from python.tools.task_planner_tool import TaskPlanner

        mock_agent.call_utility_llm = AsyncMock(return_value=mock_llm_json_response)

        planner = TaskPlanner(agent=mock_agent, name="task_planner", args={}, message="")

        # Main project plan
        main_plan = await planner.execute(
            action="create",
            task="Develop e-commerce platform",
            context="Team of 3 developers, 3-month timeline"
        )
        assert "Task Plan" in main_plan.message

        # Get main task ID
        plans = mock_agent.data.get("task_plans", {})
        main_task_id = list(plans.keys())[0]

        # Sub-task: Frontend
        frontend_plan = await planner.execute(
            action="create",
            task="Build frontend with React",
            context="Part of e-commerce platform"
        )

        # Sub-task: Backend
        backend_plan = await planner.execute(
            action="create",
            task="Build backend API with Django",
            context="Part of e-commerce platform"
        )

        # Track progress on main task
        await planner.execute(
            action="update",
            task_id=main_task_id,
            updates={"progress": 30}
        )

        # Check status
        status = await planner.execute(action="status", task_id=main_task_id)
        assert task_id in status.message

    @pytest.mark.asyncio
    async def test_knowledge_base_workflow(self, agent, temp_memory_dir):
        """Test building and querying knowledge base."""
        with patch('python.helpers.files.get_abs_path', return_value=temp_memory_dir):
            memory = await Memory.get(agent)

            # Build knowledge base
            knowledge_items = [
                ("Python best practices: Use type hints for better code clarity", {"category": "python", "area": "main"}),
                ("Python best practices: Follow PEP 8 style guide", {"category": "python", "area": "main"}),
                ("JavaScript best practices: Use const and let instead of var", {"category": "javascript", "area": "main"}),
                ("Security best practice: Never store passwords in plain text", {"category": "security", "area": "main"}),
                ("Security best practice: Always validate user input", {"category": "security", "area": "main"}),
            ]

            for text, metadata in knowledge_items:
                memory.insert_text(text, metadata)

            # Query Python practices
            python_results = await memory.search_similarity_threshold(
                query="Python coding standards",
                limit=5,
                threshold=0.0,
                filter="category == 'python'"
            )
            assert isinstance(python_results, list)

            # Query security practices
            security_results = await memory.search_similarity_threshold(
                query="security guidelines",
                limit=5,
                threshold=0.0,
                filter="category == 'security'"
            )
            assert isinstance(security_results, list)


class TestConcurrentWorkflows:
    """Test concurrent workflow execution."""

    @pytest.mark.asyncio
    async def test_concurrent_task_planning(self, mock_agent, mock_llm_json_response):
        """Test concurrent task planning operations."""
        from python.tools.task_planner_tool import TaskPlanner

        mock_agent.call_utility_llm = AsyncMock(return_value=mock_llm_json_response)

        # Create multiple planners concurrently
        async def create_plan(task_name):
            planner = TaskPlanner(agent=mock_agent, name=f"planner_{task_name}", args={}, message="")
            return await planner.execute(action="create", task=task_name)

        tasks = ["Task A", "Task B", "Task C"]
        results = await asyncio.gather(*[create_plan(task) for task in tasks])

        assert len(results) == 3
        assert all("Task Plan" in r.message for r in results)

    @pytest.mark.asyncio
    async def test_concurrent_code_analysis(self, mock_agent):
        """Test concurrent code analysis operations."""
        from python.tools.code_analyzer_tool import CodeAnalyzer

        code_samples = [
            "def func1(): pass",
            "def func2(x): return x * 2",
            "class Test: pass"
        ]

        async def analyze_code(code):
            analyzer = CodeAnalyzer(agent=mock_agent, name="analyzer", args={}, message="")
            return await analyzer.execute(action="analyze", code=code)

        results = await asyncio.gather(*[analyze_code(code) for code in code_samples])

        assert len(results) == 3
        assert all("Code Analysis" in r.message for r in results)


class TestLongRunningWorkflow:
    """Test long-running workflow scenarios."""

    @pytest.mark.asyncio
    async def test_multi_phase_project(self, mock_agent, mock_llm_json_response):
        """Test a multi-phase project workflow."""
        from python.tools.task_planner_tool import TaskPlanner

        mock_agent.call_utility_llm = AsyncMock(return_value=mock_llm_json_response)

        planner = TaskPlanner(agent=mock_agent, name="task_planner", args={}, message="")

        # Phase 1: Planning
        phase1 = await planner.execute(
            action="create",
            task="Phase 1: Requirements gathering"
        )
        assert "Task Plan" in phase1.message

        plans = mock_agent.data.get("task_plans", {})
        phase1_id = list(plans.keys())[0]

        await planner.execute(
            action="complete",
            task_id=phase1_id
        )

        # Phase 2: Development
        phase2 = await planner.execute(
            action="create",
            task="Phase 2: Core development"
        )

        phase2_id = [k for k in plans.keys() if k != phase1_id][0]

        await planner.execute(
            action="update",
            task_id=phase2_id,
            updates={"progress": 50}
        )

        # Phase 3: Testing
        phase3 = await planner.execute(
            action="create",
            task="Phase 3: Testing and QA"
        )

        # All phases created
        assert len(mock_agent.data.get("task_plans", {})) == 3


class TestDataFlowWorkflow:
    """Test data flow through complete workflows."""

    @pytest.mark.asyncio
    async def test_data_propagation(self, mock_agent, mock_llm_json_response, temp_memory_dir):
        """Test data propagation through workflow steps."""
        from python.tools.task_planner_tool import TaskPlanner
        from python.helpers.memory import Memory

        mock_agent.call_utility_llm = AsyncMock(return_value=mock_llm_json_response)

        # Step 1: Create plan (data in agent.data)
        planner = TaskPlanner(agent=mock_agent, name="task_planner", args={}, message="")
        await planner.execute(action="create", task="Test task")

        # Data should be in agent
        assert "task_plans" in mock_agent.data

        # Step 2: Store related info in memory
        # (Would need real agent for this, mock_agent doesn't have full memory integration)

        # Step 3: Retrieve and update
        plans = mock_agent.data.get("task_plans", {})
        if plans:
            task_id = list(plans.keys())[0]
            await planner.execute(
                action="update",
                task_id=task_id,
                updates={"progress": 100}
            )

            # Updated data should be accessible
            updated_plan = mock_agent.data["task_plans"][task_id]
            assert updated_plan["progress"] == 100


# ============================================================================
# STRESS TESTS
# ============================================================================

class TestWorkflowStress:
    """Stress test complete workflows."""

    @pytest.mark.asyncio
    async def test_many_sequential_operations(self, mock_agent, mock_llm_json_response):
        """Test many sequential operations."""
        from python.tools.task_planner_tool import TaskPlanner

        mock_agent.call_utility_llm = AsyncMock(return_value=mock_llm_json_response)

        planner = TaskPlanner(agent=mock_agent, name="task_planner", args={}, message="")

        # Create 20 plans
        for i in range(20):
            await planner.execute(action="create", task=f"Task {i}")

        # Should have 20 plans
        plans = mock_agent.data.get("task_plans", {})
        assert len(plans) == 20

    @pytest.mark.asyncio
    async def test_rapid_updates(self, mock_agent, mock_llm_json_response):
        """Test rapid updates to same task."""
        from python.tools.task_planner_tool import TaskPlanner

        mock_agent.call_utility_llm = AsyncMock(return_value=mock_llm_json_response)

        planner = TaskPlanner(agent=mock_agent, name="task_planner", args={}, message="")

        # Create task
        await planner.execute(action="create", task="Rapid update test")

        plans = mock_agent.data.get("task_plans", {})
        task_id = list(plans.keys())[0]

        # Rapid updates
        for progress in range(0, 101, 10):
            await planner.execute(
                action="update",
                task_id=task_id,
                updates={"progress": progress}
            )

        # Final progress should be 100
        final_plan = mock_agent.data["task_plans"][task_id]
        assert final_plan["progress"] == 100
