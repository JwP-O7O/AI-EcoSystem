# 📱 Android Tools - Quick Reference

**Versie 3.0** | **Voor Agent Zero Android**

---

## 🚀 Quick Start

```bash
# Test if tools are loaded
python android-versie/config/android_tools_config.py

# Start Agent Zero with Android tools
bash android-versie/agent0_wrapper.sh
```

---

## 🔔 Android Features Tool

### Notification
```json
{"tool_name": "android_features", "tool_args": {"feature": "notification", "title": "Title", "content": "Message"}}
```

### Text-to-Speech
```json
{"tool_name": "android_features", "tool_args": {"feature": "tts", "text": "Hello world"}}
```

### Clipboard (Set)
```json
{"tool_name": "android_features", "tool_args": {"feature": "clipboard", "action": "set", "text": "Copy this"}}
```

### Clipboard (Get)
```json
{"tool_name": "android_features", "tool_args": {"feature": "clipboard", "action": "get"}}
```

### Battery
```json
{"tool_name": "android_features", "tool_args": {"feature": "battery"}}
```

### Location
```json
{"tool_name": "android_features", "tool_args": {"feature": "location", "provider": "gps"}}
```

### Camera
```json
{"tool_name": "android_features", "tool_args": {"feature": "camera", "camera_id": 0, "filepath": "/sdcard/photo.jpg"}}
```

### Sensors (List)
```json
{"tool_name": "android_features", "tool_args": {"feature": "sensors"}}
```

### Sensors (Read)
```json
{"tool_name": "android_features", "tool_args": {"feature": "sensors", "sensor": "accelerometer", "limit": 5}}
```

### Vibrate
```json
{"tool_name": "android_features", "tool_args": {"feature": "vibrate", "duration": 500}}
```

### Toast
```json
{"tool_name": "android_features", "tool_args": {"feature": "toast", "text": "Message", "position": "bottom"}}
```

---

## 🧠 Persistent Memory Tool

### Store Memory
```json
{
    "tool_name": "persistent_memory",
    "tool_args": {
        "operation": "store",
        "content": "Important information here",
        "summary": "Brief summary",
        "importance": 8,
        "tags": ["tag1", "tag2"],
        "context": "project-name"
    }
}
```

### Recall Memories
```json
{
    "tool_name": "persistent_memory",
    "tool_args": {
        "operation": "recall",
        "tags": ["tag1"],
        "limit": 5,
        "min_importance": 6
    }
}
```

### Search Memories
```json
{
    "tool_name": "persistent_memory",
    "tool_args": {
        "operation": "search",
        "query": "search terms",
        "limit": 10
    }
}
```

### List Memories
```json
{
    "tool_name": "persistent_memory",
    "tool_args": {
        "operation": "list",
        "limit": 20,
        "tag": "specific-tag"
    }
}
```

### Memory Stats
```json
{"tool_name": "persistent_memory", "tool_args": {"operation": "stats"}}
```

### Update Memory
```json
{
    "tool_name": "persistent_memory",
    "tool_args": {
        "operation": "update",
        "memory_id": 123,
        "importance": 9
    }
}
```

### Delete Memory
```json
{"tool_name": "persistent_memory", "tool_args": {"operation": "delete", "memory_id": 123}}
```

---

## 🎤 Voice Interface Tool

### Speak (TTS)
```json
{
    "tool_name": "voice_interface",
    "tool_args": {
        "mode": "speak",
        "text": "Text to speak",
        "language": "en-US",
        "rate": "1.0"
    }
}
```

### Listen (STT)
```json
{
    "tool_name": "voice_interface",
    "tool_args": {
        "mode": "listen",
        "language": "en-US",
        "duration": 10
    }
}
```

### Conversation Mode
```json
{
    "tool_name": "voice_interface",
    "tool_args": {
        "mode": "conversation",
        "greeting": "Hello! How can I help?",
        "language": "en-US",
        "duration": 30
    }
}
```

---

## 📅 Task Scheduler Tool

### Schedule One-Time Task
```json
{
    "tool_name": "task_scheduler",
    "tool_args": {
        "operation": "schedule",
        "name": "Task Name",
        "command": "python script.py",
        "schedule_type": "once",
        "schedule_data": {"delay_seconds": 3600}
    }
}
```

### Schedule Recurring Task
```json
{
    "tool_name": "task_scheduler",
    "tool_args": {
        "operation": "schedule",
        "name": "Daily Task",
        "command": "python daily.py",
        "schedule_type": "recurring",
        "schedule_data": {"time": "2025-01-01T09:00:00"}
    }
}
```

### Schedule Interval Task
```json
{
    "tool_name": "task_scheduler",
    "tool_args": {
        "operation": "schedule",
        "name": "Periodic Check",
        "command": "python check.py",
        "schedule_type": "interval",
        "schedule_data": {"interval_seconds": 1800}
    }
}
```

### List Tasks
```json
{
    "tool_name": "task_scheduler",
    "tool_args": {
        "operation": "list",
        "status": "pending",
        "limit": 20
    }
}
```

### Get Task Status
```json
{"tool_name": "task_scheduler", "tool_args": {"operation": "status", "task_id": 1}}
```

### Cancel Task
```json
{"tool_name": "task_scheduler", "tool_args": {"operation": "cancel", "task_id": 1}}
```

### Run Pending Tasks
```json
{"tool_name": "task_scheduler", "tool_args": {"operation": "run_pending"}}
```

### Clear Completed
```json
{"tool_name": "task_scheduler", "tool_args": {"operation": "clear", "keep_days": 7}}
```

---

## 🔌 Plugin System

### Create Plugin Directory
```bash
mkdir -p plugins
```

### Create New Plugin
```python
# plugins/my_tool.py

PLUGIN_METADATA = {
    "name": "my_tool",
    "version": "1.0.0",
    "author": "Your Name",
    "description": "My custom tool",
    "dependencies": [],
    "enabled": True,
    "tool_class": "MyTool"
}

from python.helpers.tool import Tool, Response

class MyTool(Tool):
    async def execute(self, **kwargs):
        action = self.args.get("action", "")
        return Response(message=f"Executed: {action}", break_loop=False)
```

### Load Plugins
```python
from python.helpers.plugin_manager import get_plugin_manager

pm = get_plugin_manager()
pm.load_all_plugins()  # Auto-loads from plugins/
```

### Use Custom Plugin
```json
{"tool_name": "my_tool", "tool_args": {"action": "test"}}
```

---

## 💡 Common Patterns

### Pattern 1: Notify & Speak
```
1. Complete task
2. Send notification
3. Speak result via TTS
```

### Pattern 2: Remember & Recall
```
1. Learn something important
2. Store in persistent_memory with tags
3. Later: Recall by tag or search
```

### Pattern 3: Scheduled Automation
```
1. Create scheduled task
2. Task runs automatically
3. Results trigger notification
```

### Pattern 4: Voice Control
```
1. Listen for voice command
2. Execute action
3. Speak confirmation
4. Store in memory
```

---

## 📊 Tool Comparison

| Feature | android_features | persistent_memory | voice_interface | task_scheduler |
|---------|-----------------|-------------------|-----------------|----------------|
| **Purpose** | Android API access | Long-term storage | Voice I/O | Background tasks |
| **Persistence** | No | Yes (SQLite) | No | Yes (SQLite) |
| **Real-time** | Yes | No | Yes | Scheduled |
| **User Interaction** | Yes (notifications) | No | Yes (voice) | No |
| **Requires Termux API** | Yes | No | Yes | No |

---

## 🎯 Tool Selection Guide

**Need to...**
- **Alert user** → android_features (notification)
- **Remember something** → persistent_memory
- **Talk to user** → voice_interface
- **Automate task** → task_scheduler
- **Custom functionality** → Create plugin

**Want to combine:**
- **Voice + Memory** → Voice-controlled knowledge base
- **Tasks + Notifications** → Automated alerts
- **Memory + Search** → Searchable knowledge
- **Android + Tasks** → Location-based automation

---

## 🔧 Configuration

### Enable/Disable Tools

Edit `android-versie/config/android_tools_config.py`:

```python
ANDROID_TOOLS = {
    "android_features": {"enabled": True},
    "persistent_memory": {"enabled": True},
    "voice_interface": {"enabled": True},
    "task_scheduler": {"enabled": True}
}
```

### Database Locations

- Memory: `memory_db/agent_memory.db`
- Tasks: `scheduler_db/tasks.db`
- Plugins: `plugins/`

---

## 📚 More Documentation

- **Full Guide:** `ANDROID_FEATURES_UPGRADE.md`
- **Complete Manual:** `COMPLETE_GEBRUIKERSHANDLEIDING.md`
- **Setup Guide:** `ANDROID_PROJECT_UPGRADE_COMPLEET.md`

---

**Quick Help:**
```bash
# Test tools
python android-versie/config/android_tools_config.py

# Start agent
bash android-versie/agent0_wrapper.sh

# Health check
python android-versie/scripts/health_check.py
```

---

*Agent Zero Android v3.0 - Quick Reference*
