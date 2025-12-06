### task_manager tool:
- Manage multiple tasks and priorities
- **Purpose**: Create, track, and organize tasks for complex multi-step problems
- **Operations**:
  - **create**: Create a new task
    - task_name (required): Task name/identifier
    - task_description (required): Detailed description
    - priority (optional): "high", "medium", or "low" (default: "medium")
  - **list**: List all tasks
  - **complete**: Mark task as completed
    - task_name (required): Task name or ID
  - **delete**: Delete a task
    - task_name (required): Task name or ID
  - **update**: Update task properties
    - task_name (required): Task name or ID
    - description (optional): New description
    - priority (optional): New priority
    - status (optional): New status
  - **prioritize**: Show tasks sorted by priority
- **Example usage**:
```json
{
  "thoughts": [
    "This is a complex problem, I should break it into manageable tasks"
  ],
  "tool_name": "task_manager",
  "tool_args": {
    "operation": "create",
    "task_name": "Setup database",
    "task_description": "Initialize PostgreSQL database with required schemas",
    "priority": "high"
  }
}
```
```json
{
  "thoughts": [
    "Let me see all pending tasks to plan my next steps"
  ],
  "tool_name": "task_manager",
  "tool_args": {
    "operation": "prioritize"
  }
}
```
- Use this to organize complex multi-step solutions
- Helps maintain context across long conversations
- Essential for project management and planning
