from python.helpers.tool import Tool, Response
import asyncio
import json
from typing import Dict, List
from datetime import datetime

class TaskManager(Tool):
    async def execute(self, **kwargs):
        """
        Multi-tasking and task management tool for parallel execution
        """
        operation = kwargs.get("operation", "")
        task_name = kwargs.get("task_name", "")
        task_description = kwargs.get("task_description", "")
        priority = kwargs.get("priority", "medium")

        self.log.log(type="info", heading=f"Task Manager: {operation}")

        # Initialize task list in agent data if not exists
        if "tasks" not in self.agent.data:
            self.agent.data["tasks"] = {}

        tasks = self.agent.data["tasks"]

        try:
            if operation == "create":
                return await self._create_task(tasks, task_name, task_description, priority)
            elif operation == "list":
                return await self._list_tasks(tasks)
            elif operation == "complete":
                return await self._complete_task(tasks, task_name)
            elif operation == "delete":
                return await self._delete_task(tasks, task_name)
            elif operation == "update":
                return await self._update_task(tasks, task_name, kwargs)
            elif operation == "prioritize":
                return await self._prioritize_tasks(tasks)
            else:
                return Response(
                    message=f"Unknown task operation: {operation}\n"
                    f"Available: create, list, complete, delete, update, prioritize",
                    break_loop=False
                )

        except Exception as e:
            return Response(message=f"Task manager error: {str(e)}", break_loop=False)

    async def _create_task(self, tasks, name, description, priority):
        """Create a new task"""
        if not name:
            return Response(message="Task name is required", break_loop=False)

        task_id = f"task_{len(tasks) + 1}"
        tasks[task_id] = {
            "name": name,
            "description": description,
            "priority": priority,
            "status": "pending",
            "created_at": datetime.now().isoformat(),
            "completed_at": None
        }

        return Response(
            message=f"Task created: {task_id}\n"
                    f"Name: {name}\n"
                    f"Priority: {priority}\n"
                    f"Status: pending",
            break_loop=False
        )

    async def _list_tasks(self, tasks):
        """List all tasks"""
        if not tasks:
            return Response(message="No tasks found", break_loop=False)

        task_list = []
        for task_id, task in tasks.items():
            status_symbol = "✓" if task["status"] == "completed" else "○"
            priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(
                task["priority"], "⚪"
            )

            task_list.append(
                f"{status_symbol} {priority_emoji} {task_id}: {task['name']}\n"
                f"   Status: {task['status']} | Priority: {task['priority']}\n"
                f"   {task['description']}"
            )

        return Response(
            message=f"Active Tasks ({len(tasks)}):\n\n" + "\n\n".join(task_list),
            break_loop=False
        )

    async def _complete_task(self, tasks, name):
        """Mark task as completed"""
        task_id = self._find_task_by_name(tasks, name)

        if not task_id:
            return Response(message=f"Task not found: {name}", break_loop=False)

        tasks[task_id]["status"] = "completed"
        tasks[task_id]["completed_at"] = datetime.now().isoformat()

        return Response(
            message=f"Task completed: {task_id} - {tasks[task_id]['name']}",
            break_loop=False
        )

    async def _delete_task(self, tasks, name):
        """Delete a task"""
        task_id = self._find_task_by_name(tasks, name)

        if not task_id:
            return Response(message=f"Task not found: {name}", break_loop=False)

        task_name = tasks[task_id]["name"]
        del tasks[task_id]

        return Response(message=f"Task deleted: {task_id} - {task_name}", break_loop=False)

    async def _update_task(self, tasks, name, updates):
        """Update task properties"""
        task_id = self._find_task_by_name(tasks, name)

        if not task_id:
            return Response(message=f"Task not found: {name}", break_loop=False)

        # Update allowed fields
        allowed_fields = ["description", "priority", "status"]
        updated_fields = []

        for field in allowed_fields:
            if field in updates:
                tasks[task_id][field] = updates[field]
                updated_fields.append(field)

        return Response(
            message=f"Task updated: {task_id}\n"
                    f"Updated fields: {', '.join(updated_fields)}",
            break_loop=False
        )

    async def _prioritize_tasks(self, tasks):
        """Show tasks sorted by priority"""
        if not tasks:
            return Response(message="No tasks to prioritize", break_loop=False)

        priority_order = {"high": 0, "medium": 1, "low": 2}
        sorted_tasks = sorted(
            tasks.items(),
            key=lambda x: (
                priority_order.get(x[1]["priority"], 3),
                x[1]["created_at"]
            )
        )

        task_list = []
        for task_id, task in sorted_tasks:
            if task["status"] != "completed":
                status_symbol = "○"
                priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(
                    task["priority"], "⚪"
                )

                task_list.append(
                    f"{status_symbol} {priority_emoji} {task['name']}\n"
                    f"   {task['description']}"
                )

        if not task_list:
            return Response(message="All tasks completed!", break_loop=False)

        return Response(
            message=f"Prioritized Task List:\n\n" + "\n\n".join(task_list),
            break_loop=False
        )

    def _find_task_by_name(self, tasks, name):
        """Find task ID by name"""
        for task_id, task in tasks.items():
            if task["name"].lower() == name.lower() or task_id == name:
                return task_id
        return None
