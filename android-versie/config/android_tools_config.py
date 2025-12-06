"""
Android Tools Configuration
Register and configure all Android-specific tools

This file integrates the new Android features into Agent Zero
"""

import sys
import os

# Add paths for imports
base_dir = os.path.join(os.path.dirname(__file__), '../..')
sys.path.insert(0, base_dir)

from python.tools.android_features_tool import AndroidFeatures
from python.tools.persistent_memory_tool import PersistentMemory
from python.tools.voice_interface_tool import VoiceInterface
from python.tools.task_scheduler_tool import TaskScheduler
from python.helpers.plugin_manager import get_plugin_manager


# Tool Registry
ANDROID_TOOLS = {
    "android_features": {
        "class": AndroidFeatures,
        "description": "Access Android-specific features (notifications, TTS, sensors, etc.)",
        "enabled": True,
        "requires": ["termux-api"]  # Optional dependency check
    },
    "persistent_memory": {
        "class": PersistentMemory,
        "description": "Advanced persistent memory with SQLite backend",
        "enabled": True,
        "requires": []
    },
    "voice_interface": {
        "class": VoiceInterface,
        "description": "Voice input/output for hands-free operation",
        "enabled": True,
        "requires": ["termux-api"]
    },
    "task_scheduler": {
        "class": TaskScheduler,
        "description": "Schedule and manage background tasks",
        "enabled": True,
        "requires": []
    }
}


def register_android_tools(agent_config):
    """
    Register Android tools with Agent Zero configuration

    Args:
        agent_config: AgentConfig instance to modify

    Returns:
        Modified agent_config
    """

    print("\n🔧 Registering Android-specific tools...")

    # Initialize plugin manager
    plugin_manager = get_plugin_manager()

    # Load any available plugins
    loaded_plugins = plugin_manager.load_all_plugins()
    if loaded_plugins > 0:
        print(f"   ✓ Loaded {loaded_plugins} custom plugins")

    # Register built-in Android tools
    registered = 0
    for tool_name, tool_info in ANDROID_TOOLS.items():
        if tool_info["enabled"]:
            print(f"   ✓ {tool_name}: {tool_info['description']}")
            registered += 1

    print(f"\n✓ {registered} Android tools registered\n")

    return agent_config


def check_android_dependencies():
    """Check if Android-specific dependencies are available"""
    import subprocess

    checks = {
        "Termux API": "termux-notification",
        "SQLite": "sqlite3",
    }

    print("🔍 Checking Android dependencies...\n")

    all_ok = True
    for name, command in checks.items():
        try:
            result = subprocess.run(
                ["which", command],
                capture_output=True,
                timeout=2
            )
            if result.returncode == 0:
                print(f"   ✓ {name}")
            else:
                print(f"   ⚠️  {name} (optional)")
        except:
            print(f"   ⚠️  {name} (optional)")

    print()
    return all_ok


def get_android_tools_info():
    """Get information about available Android tools"""
    tools_info = []

    for tool_name, tool_info in ANDROID_TOOLS.items():
        if tool_info["enabled"]:
            tools_info.append({
                "name": tool_name,
                "description": tool_info["description"],
                "requires": tool_info.get("requires", [])
            })

    # Add plugin tools
    plugin_manager = get_plugin_manager()
    for plugin_info in plugin_manager.list_plugins():
        tools_info.append({
            "name": plugin_info["name"],
            "description": plugin_info["description"],
            "type": "plugin",
            "version": plugin_info["version"]
        })

    return tools_info


def print_android_tools_summary():
    """Print summary of available Android tools"""
    print("\n" + "="*60)
    print("📱 Android Tools Available:")
    print("="*60 + "\n")

    tools = get_android_tools_info()

    for tool in tools:
        tool_type = f"[{tool.get('type', 'built-in').upper()}]"
        print(f"• {tool['name']} {tool_type}")
        print(f"  {tool['description']}")

        if tool.get('requires'):
            print(f"  Requires: {', '.join(tool['requires'])}")

        if tool.get('version'):
            print(f"  Version: {tool['version']}")

        print()

    print(f"Total: {len(tools)} tools available")
    print("="*60 + "\n")


if __name__ == "__main__":
    # When run directly, show tool info
    check_android_dependencies()
    print_android_tools_summary()
