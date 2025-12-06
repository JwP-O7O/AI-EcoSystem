### task_planner_tool:
Intelligent task planning and decomposition system for complex tasks.
Analyzes task complexity, breaks down into subtasks, creates dependency graphs, and tracks progress.

**Operations:**

**1. Create Task Plan:**
```json
{
    "thoughts": [
        "This is a complex task that needs proper planning",
        "I should break it down into manageable subtasks with dependencies"
    ],
    "tool_name": "task_planner_tool",
    "tool_args": {
        "action": "create",
        "task": "Build a web scraper for product prices with database storage and scheduling",
        "context": "User needs to track prices daily from 3 e-commerce sites and get alerts on price drops"
    }
}
```

**2. Update Plan Progress:**
```json
{
    "thoughts": [
        "I've completed the database setup subtask",
        "Let me update the plan to reflect this progress"
    ],
    "tool_name": "task_planner_tool",
    "tool_args": {
        "action": "update",
        "task_id": "task_1732901234",
        "updates": {
            "subtasks": [
                {"id": "subtask_1", "status": "completed"},
                {"id": "subtask_2", "status": "in_progress"}
            ],
            "progress": 30
        }
    }
}
```

**3. Get Plan Status:**
```json
{
    "thoughts": [
        "Let me check the current status of the task plan",
        "I need to see what's completed and what's remaining"
    ],
    "tool_name": "task_planner_tool",
    "tool_args": {
        "action": "status",
        "task_id": "task_1732901234"
    }
}
```

**4. Complete Task:**
```json
{
    "thoughts": [
        "All subtasks are finished and tested",
        "The entire task is now complete"
    ],
    "tool_name": "task_planner_tool",
    "tool_args": {
        "action": "complete",
        "task_id": "task_1732901234"
    }
}
```

**5. Adaptive Replanning:**
```json
{
    "thoughts": [
        "I encountered a blocker - the API requires authentication",
        "This wasn't in the original plan, I need to adapt"
    ],
    "tool_name": "task_planner_tool",
    "tool_args": {
        "action": "replan",
        "task_id": "task_1732901234",
        "reason": "API requires OAuth2 authentication which wasn't anticipated. Need to add authentication setup subtasks."
    }
}
```

**Plan Output Structure:**
The tool creates comprehensive plans with:
- **Task Analysis**: Complexity level (low/medium/high/very-high)
- **Subtasks**: Ordered list with dependencies, tools needed, priority
- **Dependencies**: Which tasks must complete before others can start
- **Resource Estimates**: Tools needed, estimated steps per subtask
- **Success Criteria**: Clear goals to know when task is complete
- **Risk Assessment**: Potential blockers and mitigation strategies

**When to Use Task Planner:**
- **Complex multi-step tasks** (>5 steps or multiple tools)
- **Tasks with dependencies** (some steps depend on others)
- **Long-running projects** (need to track progress over time)
- **Unfamiliar domains** (planning helps identify knowledge gaps)
- **Team coordination** (when using subordinate agents)
- **Tasks prone to scope creep** (keeps focus on defined goals)

**When NOT to Use:**
- Simple single-step tasks
- Well-known repetitive tasks
- Quick information lookups
- Tasks you can complete in <3 steps

**Best Practices:**

1. **Create Plans Early**: Before starting complex tasks, create a plan first
2. **Be Specific**: Provide detailed task descriptions and context
3. **Update Progress**: Mark subtasks as completed to track progress
4. **Adapt When Needed**: Use replan when you hit unexpected blockers
5. **Check Dependencies**: Complete prerequisite subtasks before dependent ones
6. **Review Success Criteria**: Ensure all criteria are met before marking complete

**Example Workflow:**

```json
// Step 1: Create plan for complex task
{
    "tool_name": "task_planner_tool",
    "tool_args": {
        "action": "create",
        "task": "Set up automated testing pipeline for Python project",
        "context": "Project uses pytest, needs CI/CD with GitHub Actions, coverage reports"
    }
}

// Output shows plan with subtasks:
// 1. Install and configure pytest (priority: high)
// 2. Write unit tests for core modules (depends on 1)
// 3. Set up GitHub Actions workflow (priority: high)
// 4. Configure coverage reporting (depends on 1, 3)
// 5. Add status badges to README (depends on 3, 4)

// Step 2: Work through subtasks, updating as you go
{
    "tool_name": "task_planner_tool",
    "tool_args": {
        "action": "update",
        "task_id": "task_1732901234",
        "updates": {"subtasks": [{"id": "subtask_1", "status": "completed"}]}
    }
}

// Step 3: Hit a blocker? Replan!
{
    "tool_name": "task_planner_tool",
    "tool_args": {
        "action": "replan",
        "task_id": "task_1732901234",
        "reason": "GitHub Actions requires repository secrets for coverage upload"
    }
}

// Step 4: Complete when done
{
    "tool_name": "task_planner_tool",
    "tool_args": {
        "action": "complete",
        "task_id": "task_1732901234"
    }
}
```

**Complexity Levels:**
- **Low**: 1-3 straightforward steps, no dependencies
- **Medium**: 4-7 steps, some dependencies, known tools
- **High**: 8-15 steps, complex dependencies, may need new tools
- **Very High**: 15+ steps, intricate dependencies, multiple unknowns

**Success Indicators:**
- All subtasks marked as completed
- All success criteria met
- No blocking issues remaining
- Solution tested and validated

**Tips for Effective Planning:**
- Break tasks into 5-10 subtasks (not too granular, not too broad)
- Each subtask should be completable in one session
- Identify dependencies early to avoid blocking yourself
- Set realistic estimates - complex tasks take longer than expected
- Use risk assessment to prepare for common failure modes
- Store completed plans in vector memory for future reference
