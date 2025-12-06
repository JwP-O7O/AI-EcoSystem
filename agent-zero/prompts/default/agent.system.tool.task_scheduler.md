# Task Scheduler Tool

Schedule tasks for delayed or recurring execution with Android notification support.

## Usage

```json
{
    "tool_name": "task_scheduler",
    "tool_args": {
        "operation": "schedule",
        "task_name": "daily_backup",
        "schedule_type": "recurring",
        "interval": "daily",
        "action": "execute_code",
        "action_params": {
            "language": "python",
            "code": "import shutil; shutil.copy('/sdcard/data.db', '/sdcard/backups/data.db')"
        }
    }
}
```

## Operations

### schedule
Create a new scheduled task.

**Arguments:**
- `task_name` (required): Unique identifier for this task
- `schedule_type` (required): "once" or "recurring"
- `execute_at` (required for "once"): Timestamp "YYYY-MM-DD HH:MM:SS"
- `interval` (required for "recurring"): "hourly", "daily", "weekly", "monthly"
- `action` (required): "notification", "execute_code", "api_call", "call_tool"
- `action_params` (required): Parameters for the action (see below)

**Example - One-time reminder:**
```json
{
    "tool_name": "task_scheduler",
    "tool_args": {
        "operation": "schedule",
        "task_name": "meeting_reminder",
        "schedule_type": "once",
        "execute_at": "2025-11-29 14:30:00",
        "action": "notification",
        "action_params": {
            "title": "Meeting Reminder",
            "content": "Team standup in 10 minutes",
            "priority": "high"
        }
    }
}
```

**Example - Recurring backup:**
```json
{
    "tool_name": "task_scheduler",
    "tool_args": {
        "operation": "schedule",
        "task_name": "daily_backup",
        "schedule_type": "recurring",
        "interval": "daily",
        "action": "execute_code",
        "action_params": {
            "language": "bash",
            "code": "tar -czf /sdcard/backup_$(date +%Y%m%d).tar.gz /data/data/com.termux/files/home/AI-EcoSystem/work_dir"
        }
    }
}
```

**Example - API health check:**
```json
{
    "tool_name": "task_scheduler",
    "tool_args": {
        "operation": "schedule",
        "task_name": "api_health_check",
        "schedule_type": "recurring",
        "interval": "hourly",
        "action": "api_call",
        "action_params": {
            "url": "https://api.example.com/health",
            "method": "GET",
            "notify_on_failure": true
        }
    }
}
```

### list
Show all scheduled tasks.

**Arguments:**
- `status` (optional): Filter by status ("pending", "running", "completed", "failed")
- `schedule_type` (optional): Filter by type ("once", "recurring")

**Example:**
```json
{
    "tool_name": "task_scheduler",
    "tool_args": {
        "operation": "list",
        "status": "pending"
    }
}
```

### cancel
Cancel/delete a scheduled task.

**Arguments:**
- `task_name` (required): Name of task to cancel

**Example:**
```json
{
    "tool_name": "task_scheduler",
    "tool_args": {
        "operation": "cancel",
        "task_name": "daily_backup"
    }
}
```

### execute
Manually trigger a scheduled task immediately.

**Arguments:**
- `task_name` (required): Name of task to execute now

**Example:**
```json
{
    "tool_name": "task_scheduler",
    "tool_args": {
        "operation": "execute",
        "task_name": "daily_backup"
    }
}
```

### pause
Pause a recurring task without deleting it.

**Arguments:**
- `task_name` (required): Name of task to pause

### resume
Resume a paused task.

**Arguments:**
- `task_name` (required): Name of task to resume

## Action Types

### notification
Send Android notification via Termux:API.

**action_params:**
- `title`: Notification title
- `content`: Notification text
- `priority`: "default", "high", "low"

### execute_code
Run code (Python, Bash, Node.js).

**action_params:**
- `language`: "python", "bash", "nodejs"
- `code`: Code to execute
- `notify_on_completion`: Send notification when done (default: false)
- `notify_on_error`: Send notification on error (default: true)

### api_call
Make HTTP API request.

**action_params:**
- `url`: API endpoint
- `method`: "GET", "POST", "PUT", "DELETE"
- `headers`: Optional headers dict
- `body`: Optional request body
- `notify_on_failure`: Send notification if request fails (default: true)

### call_tool
Execute another Agent Zero tool.

**action_params:**
- `tool_name`: Name of tool to call
- `tool_args`: Arguments for the tool

**Example:**
```json
{
    "operation": "schedule",
    "task_name": "hourly_memory_cleanup",
    "schedule_type": "recurring",
    "interval": "hourly",
    "action": "call_tool",
    "action_params": {
        "tool_name": "persistent_memory",
        "tool_args": {
            "operation": "delete",
            "min_importance": 3,
            "older_than_days": 7
        }
    }
}
```

## Intervals for Recurring Tasks

- **hourly**: Every hour at :00
- **daily**: Every day at midnight (00:00)
- **weekly**: Every Monday at midnight
- **monthly**: First day of month at midnight

**Note:** For more specific timing (e.g., daily at 3pm), use cron-style scheduling or create multiple "once" tasks.

## When to Use

Use task_scheduler for:
- **Reminders**: Meeting notifications, deadline alerts
- **Automated backups**: Regular data backups
- **Monitoring**: Periodic health checks, API monitoring
- **Maintenance**: Cleanup tasks, data archiving
- **Recurring reports**: Daily summaries, weekly stats
- **Delayed actions**: Execute something after delay

DO NOT use for:
- Immediate tasks (use tools directly instead)
- Sub-second timing (scheduler has minute-level precision)
- Tasks requiring user interaction (notifications only)

## Best Practices

1. **Unique task names**: Use descriptive, unique identifiers
2. **Handle failures**: Set `notify_on_error: true` for critical tasks
3. **Clean up**: Cancel completed one-time tasks to avoid clutter
4. **Battery awareness**: Limit frequent recurring tasks on mobile
5. **Test first**: Manually execute before scheduling
6. **Monitor logs**: Check task execution history regularly

## Example Workflows

### Daily Report Generation
```json
{
    "tool_name": "task_scheduler",
    "tool_args": {
        "operation": "schedule",
        "task_name": "daily_report",
        "schedule_type": "recurring",
        "interval": "daily",
        "action": "execute_code",
        "action_params": {
            "language": "python",
            "code": "import pandas as pd; df = pd.read_csv('/sdcard/data.csv'); summary = df.describe(); print(summary)",
            "notify_on_completion": true
        }
    }
}
```

### Reminder with Follow-up
```json
// 1. Schedule initial reminder
{
    "operation": "schedule",
    "task_name": "review_reminder",
    "schedule_type": "once",
    "execute_at": "2025-11-30 09:00:00",
    "action": "notification",
    "action_params": {
        "title": "Code Review Due",
        "content": "Please review pull request #42"
    }
}

// 2. Schedule follow-up if not done
{
    "operation": "schedule",
    "task_name": "review_followup",
    "schedule_type": "once",
    "execute_at": "2025-11-30 17:00:00",
    "action": "notification",
    "action_params": {
        "title": "Reminder: Code Review",
        "content": "Still pending: pull request #42",
        "priority": "high"
    }
}
```

### API Monitoring with Alert
```json
{
    "tool_name": "task_scheduler",
    "tool_args": {
        "operation": "schedule",
        "task_name": "api_monitor",
        "schedule_type": "recurring",
        "interval": "hourly",
        "action": "api_call",
        "action_params": {
            "url": "https://api.example.com/status",
            "method": "GET",
            "notify_on_failure": true
        }
    }
}
```

## Storage & Persistence

Scheduled tasks are stored persistently and survive agent restarts. The scheduler runs as a background process when enabled.

## Android Integration

On Android/Termux, the scheduler can:
- Send notifications via Termux:API
- Vibrate device on task completion/failure
- Use TTS to announce task results
- Integrate with Android calendar/alarms (future enhancement)

## Limitations

- **Precision**: Minute-level accuracy (not suitable for sub-second timing)
- **Background execution**: Subject to Android battery optimization
- **Termux wake locks**: May need wake locks for reliable execution
- **No UI**: Cannot interact with UI, only notifications/code execution
