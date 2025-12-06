"""
Task Planner Tool - Advanced task decomposition and planning
"""

import json
from python.helpers.tool import Tool, Response
from python.helpers import files
from python.helpers.print_style import PrintStyle


class TaskPlanner(Tool):
    """
    Intelligent task planning and decomposition tool

    Capabilities:
    - Analyze task complexity
    - Decompose large tasks into subtasks
    - Create dependency graphs
    - Estimate resources and time
    - Track progress
    - Adaptive replanning
    """

    async def execute(self, action: str = "create", **kwargs):
        """
        Execute task planning operations

        Args:
            action: Operation to perform
                - "create": Create a new task plan
                - "update": Update existing plan
                - "status": Get plan status
                - "complete": Mark task as complete
                - "replan": Adapt plan based on progress

        Actions:
            create: task, context
            update: task_id, updates
            status: task_id
            complete: task_id
            replan: task_id, reason
        """

        if action == "create":
            return await self._create_plan(
                task=kwargs.get("task", ""),
                context=kwargs.get("context", "")
            )
        elif action == "update":
            return await self._update_plan(
                task_id=kwargs.get("task_id", ""),
                updates=kwargs.get("updates", {})
            )
        elif action == "status":
            return await self._get_status(
                task_id=kwargs.get("task_id", "")
            )
        elif action == "complete":
            return await self._complete_task(
                task_id=kwargs.get("task_id", "")
            )
        elif action == "replan":
            return await self._replan(
                task_id=kwargs.get("task_id", ""),
                reason=kwargs.get("reason", "")
            )
        else:
            return Response(
                message=f"Unknown action: {action}",
                break_loop=False
            )

    async def _create_plan(self, task: str, context: str = "") -> Response:
        """
        Create a comprehensive task plan with decomposition
        """

        PrintStyle(font_color="cyan").print(f"Creating task plan for: {task}")

        # Use agent's utility LLM to analyze and decompose task
        system = self._get_planning_prompt()
        user_msg = f"Task: {task}\n\nContext: {context}"

        plan_json = await self.agent.call_utility_llm(
            system=system,
            msg=user_msg
        )

        # Parse the plan
        try:
            plan = json.loads(plan_json)
        except json.JSONDecodeError:
            # Try to extract JSON from response
            import re
            json_match = re.search(r'\{.*\}', plan_json, re.DOTALL)
            if json_match:
                plan = json.loads(json_match.group())
            else:
                return Response(
                    message="Failed to create task plan. Could not parse response.",
                    break_loop=False
                )

        # Save plan to agent data
        task_id = self._generate_task_id()
        plan["id"] = task_id
        plan["status"] = "active"
        plan["progress"] = 0
        plan["created"] = self._get_timestamp()

        self._save_plan(task_id, plan)

        # Format response
        response = self._format_plan_response(plan)

        PrintStyle(font_color="green").print("✅ Task plan created")

        return Response(
            message=response,
            break_loop=False
        )

    async def _update_plan(self, task_id: str, updates: dict) -> Response:
        """Update an existing task plan"""

        plan = self._load_plan(task_id)
        if not plan:
            return Response(
                message=f"Task plan '{task_id}' not found",
                break_loop=False
            )

        # Apply updates
        plan.update(updates)
        plan["updated"] = self._get_timestamp()

        self._save_plan(task_id, plan)

        return Response(
            message=f"Task plan '{task_id}' updated successfully",
            break_loop=False
        )

    async def _get_status(self, task_id: str) -> Response:
        """Get current status of a task plan"""

        plan = self._load_plan(task_id)
        if not plan:
            return Response(
                message=f"Task plan '{task_id}' not found",
                break_loop=False
            )

        response = self._format_plan_response(plan)

        return Response(
            message=response,
            break_loop=False
        )

    async def _complete_task(self, task_id: str) -> Response:
        """Mark a task as completed"""

        plan = self._load_plan(task_id)
        if not plan:
            return Response(
                message=f"Task plan '{task_id}' not found",
                break_loop=False
            )

        plan["status"] = "completed"
        plan["progress"] = 100
        plan["completed"] = self._get_timestamp()

        self._save_plan(task_id, plan)

        return Response(
            message=f"✅ Task '{plan.get('task', task_id)}' marked as completed!",
            break_loop=False
        )

    async def _replan(self, task_id: str, reason: str) -> Response:
        """Adapt plan based on new information or blockers"""

        plan = self._load_plan(task_id)
        if not plan:
            return Response(
                message=f"Task plan '{task_id}' not found",
                break_loop=False
            )

        PrintStyle(font_color="yellow").print(f"Replanning task: {reason}")

        # Use utility LLM to adapt plan
        system = self._get_replanning_prompt()
        user_msg = f"Current Plan:\n{json.dumps(plan, indent=2)}\n\nReason for replanning: {reason}"

        new_plan_json = await self.agent.call_utility_llm(
            system=system,
            msg=user_msg
        )

        try:
            new_plan = json.loads(new_plan_json)
            new_plan["id"] = task_id
            new_plan["status"] = "active"
            new_plan["updated"] = self._get_timestamp()
            new_plan["replan_history"] = plan.get("replan_history", []) + [
                {"reason": reason, "timestamp": self._get_timestamp()}
            ]

            self._save_plan(task_id, new_plan)

            response = f"🔄 Plan adapted successfully\n\n{self._format_plan_response(new_plan)}"

            return Response(message=response, break_loop=False)

        except json.JSONDecodeError:
            return Response(
                message="Failed to replan. Could not parse new plan.",
                break_loop=False
            )

    def _get_planning_prompt(self) -> str:
        """System prompt for task planning"""
        return """You are an expert task planner. Given a task, create a comprehensive plan with:

1. Task analysis (complexity, requirements, constraints)
2. Subtask decomposition (break into manageable steps)
3. Dependencies (which tasks depend on others)
4. Resource estimates (tools needed, time estimates)
5. Success criteria (how to know when done)
6. Risk assessment (potential blockers)

Output as JSON:
{
    "task": "original task description",
    "complexity": "low|medium|high|very-high",
    "subtasks": [
        {
            "id": "subtask_1",
            "description": "...",
            "dependencies": [],
            "tools_needed": ["tool1", "tool2"],
            "estimated_steps": 3,
            "priority": "high|medium|low",
            "status": "pending"
        }
    ],
    "success_criteria": ["criterion 1", "criterion 2"],
    "risks": [
        {"risk": "description", "mitigation": "how to handle"}
    ],
    "estimated_total_steps": 10
}

Be specific and actionable. Focus on creating clear, executable subtasks."""

    def _get_replanning_prompt(self) -> str:
        """System prompt for adaptive replanning"""
        return """You are adapting a task plan based on new information or blockers.

Given the current plan and the reason for replanning, create an updated plan that:
1. Addresses the blocker or new information
2. Adjusts dependencies if needed
3. Adds or removes subtasks as appropriate
4. Updates estimates and priorities
5. Maintains completed progress

Output the complete updated plan in the same JSON format as the original.
Be pragmatic and focus on getting the task done despite the challenges."""

    def _format_plan_response(self, plan: dict) -> str:
        """Format plan as readable text"""

        output = f"📋 **Task Plan: {plan.get('task', 'Untitled')}**\n\n"
        output += f"ID: {plan.get('id', 'unknown')}\n"
        output += f"Status: {plan.get('status', 'unknown')}\n"
        output += f"Complexity: {plan.get('complexity', 'unknown')}\n"
        output += f"Progress: {plan.get('progress', 0)}%\n\n"

        if plan.get('subtasks'):
            output += "**Subtasks:**\n"
            for i, subtask in enumerate(plan['subtasks'], 1):
                status_icon = "✅" if subtask.get('status') == 'completed' else "⏳" if subtask.get('status') == 'in_progress' else "⬜"
                output += f"{i}. {status_icon} {subtask.get('description', 'No description')}\n"
                if subtask.get('dependencies'):
                    output += f"   Dependencies: {', '.join(subtask['dependencies'])}\n"
                if subtask.get('tools_needed'):
                    output += f"   Tools: {', '.join(subtask['tools_needed'])}\n"
                output += "\n"

        if plan.get('success_criteria'):
            output += "**Success Criteria:**\n"
            for criterion in plan['success_criteria']:
                output += f"- {criterion}\n"
            output += "\n"

        if plan.get('risks'):
            output += "**Risks & Mitigation:**\n"
            for risk in plan['risks']:
                output += f"- Risk: {risk.get('risk', 'Unknown')}\n"
                output += f"  Mitigation: {risk.get('mitigation', 'None')}\n"
            output += "\n"

        output += f"Estimated total steps: {plan.get('estimated_total_steps', 'unknown')}\n"

        return output

    def _generate_task_id(self) -> str:
        """Generate unique task ID"""
        import time
        return f"task_{int(time.time())}"

    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.utcnow().isoformat()

    def _save_plan(self, task_id: str, plan: dict):
        """Save plan to agent data"""
        plans = self.agent.get_data("task_plans") or {}
        plans[task_id] = plan
        self.agent.set_data("task_plans", plans)

    def _load_plan(self, task_id: str) -> dict:
        """Load plan from agent data"""
        plans = self.agent.get_data("task_plans") or {}
        return plans.get(task_id)
