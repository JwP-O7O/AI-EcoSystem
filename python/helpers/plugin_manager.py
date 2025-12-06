"""
Plugin Manager - Extensible Plugin System for Agent Zero
Allows dynamic loading of custom tools and capabilities

Features:
- Hot-reload plugins without restart
- Plugin discovery
- Dependency management
- Plugin configuration
- Error isolation
"""

import os
import sys
import importlib
import importlib.util
import json
from typing import Dict, List, Optional, Any
from pathlib import Path
import traceback


class PluginMetadata:
    """Plugin metadata and configuration"""

    def __init__(self, config: Dict[str, Any]):
        self.name = config.get("name", "unknown")
        self.version = config.get("version", "0.0.0")
        self.author = config.get("author", "unknown")
        self.description = config.get("description", "")
        self.dependencies = config.get("dependencies", [])
        self.enabled = config.get("enabled", True)
        self.tool_class = config.get("tool_class")
        self.config = config.get("config", {})


class Plugin:
    """Wrapper for loaded plugin"""

    def __init__(self, metadata: PluginMetadata, module, tool_class):
        self.metadata = metadata
        self.module = module
        self.tool_class = tool_class
        self.instance = None

    def instantiate(self, agent, *args, **kwargs):
        """Create instance of plugin tool"""
        if self.tool_class:
            self.instance = self.tool_class(agent, *args, **kwargs)
            return self.instance
        return None


class PluginManager:
    """Manages plugins for Agent Zero"""

    def __init__(self, plugin_dir: Optional[str] = None):
        self.plugins: Dict[str, Plugin] = {}
        self.plugin_dir = plugin_dir or self._get_default_plugin_dir()
        self._ensure_plugin_dir()

    def _get_default_plugin_dir(self) -> str:
        """Get default plugin directory"""
        base_dir = Path(__file__).parent.parent.parent
        return str(base_dir / "plugins")

    def _ensure_plugin_dir(self):
        """Create plugin directory if it doesn't exist"""
        os.makedirs(self.plugin_dir, exist_ok=True)

        # Create example plugin if directory is empty
        example_file = Path(self.plugin_dir) / "example_plugin.py.template"
        if not example_file.exists():
            self._create_example_plugin(example_file)

    def _create_example_plugin(self, filepath: Path):
        """Create example plugin template"""
        example_code = '''"""
Example Plugin for Agent Zero
Copy this file and modify to create your own plugin
"""

from python.helpers.tool import Tool, Response


# Plugin metadata (required)
PLUGIN_METADATA = {
    "name": "example_tool",
    "version": "1.0.0",
    "author": "Your Name",
    "description": "Example plugin demonstrating custom tools",
    "dependencies": [],  # List of required Python packages
    "enabled": True,
    "tool_class": "ExampleTool",  # Name of the tool class
    "config": {
        # Custom configuration for this plugin
        "example_setting": "value"
    }
}


class ExampleTool(Tool):
    """Example custom tool"""

    async def execute(self, **kwargs):
        """
        Execute the tool

        Args from self.args:
            action: What action to perform
            message: Message to process
        """
        action = self.args.get("action", "hello")
        message = self.args.get("message", "")

        if action == "hello":
            return Response(
                message=f"Hello! You said: {message}",
                break_loop=False
            )
        elif action == "info":
            return Response(
                message=f"Example Tool v{PLUGIN_METADATA['version']}\\n"
                       f"{PLUGIN_METADATA['description']}",
                break_loop=False
            )
        else:
            return Response(
                message=f"Unknown action: {action}",
                break_loop=False
            )


# To use this plugin:
# 1. Copy this file to a new .py file in the plugins/ directory
# 2. Modify PLUGIN_METADATA and ExampleTool class
# 3. Reload plugins in Agent Zero
# 4. Use in prompts with tool_name matching metadata "name"
'''
        filepath.write_text(example_code)

    def discover_plugins(self) -> List[str]:
        """Discover all available plugins in plugin directory"""
        discovered = []

        for item in Path(self.plugin_dir).iterdir():
            if item.is_file() and item.suffix == '.py' and not item.name.startswith('_'):
                if not item.name.endswith('.template'):
                    discovered.append(item.stem)

        return discovered

    def load_plugin(self, plugin_name: str) -> Optional[Plugin]:
        """Load a specific plugin"""
        try:
            # Construct plugin file path
            plugin_file = Path(self.plugin_dir) / f"{plugin_name}.py"

            if not plugin_file.exists():
                print(f"Plugin file not found: {plugin_file}")
                return None

            # Load module
            spec = importlib.util.spec_from_file_location(plugin_name, plugin_file)
            if not spec or not spec.loader:
                print(f"Could not load plugin spec: {plugin_name}")
                return None

            module = importlib.util.module_from_spec(spec)
            sys.modules[plugin_name] = module
            spec.loader.exec_module(module)

            # Get metadata
            if not hasattr(module, 'PLUGIN_METADATA'):
                print(f"Plugin {plugin_name} missing PLUGIN_METADATA")
                return None

            metadata = PluginMetadata(module.PLUGIN_METADATA)

            # Check if enabled
            if not metadata.enabled:
                print(f"Plugin {plugin_name} is disabled")
                return None

            # Check dependencies
            missing_deps = self._check_dependencies(metadata.dependencies)
            if missing_deps:
                print(f"Plugin {plugin_name} missing dependencies: {missing_deps}")
                return None

            # Get tool class
            tool_class_name = metadata.tool_class
            if not tool_class_name or not hasattr(module, tool_class_name):
                print(f"Plugin {plugin_name} missing tool class: {tool_class_name}")
                return None

            tool_class = getattr(module, tool_class_name)

            # Create plugin wrapper
            plugin = Plugin(metadata, module, tool_class)

            # Register plugin
            self.plugins[metadata.name] = plugin

            print(f"✓ Loaded plugin: {metadata.name} v{metadata.version}")
            return plugin

        except Exception as e:
            print(f"Error loading plugin {plugin_name}: {e}")
            traceback.print_exc()
            return None

    def load_all_plugins(self) -> int:
        """Load all discovered plugins"""
        discovered = self.discover_plugins()
        loaded = 0

        for plugin_name in discovered:
            if self.load_plugin(plugin_name):
                loaded += 1

        return loaded

    def reload_plugin(self, plugin_name: str) -> bool:
        """Reload a plugin (hot-reload)"""
        # Unload first
        if plugin_name in self.plugins:
            self.unload_plugin(plugin_name)

        # Load again
        plugin = self.load_plugin(plugin_name)
        return plugin is not None

    def unload_plugin(self, plugin_name: str):
        """Unload a plugin"""
        if plugin_name in self.plugins:
            # Remove from sys.modules if present
            if plugin_name in sys.modules:
                del sys.modules[plugin_name]

            del self.plugins[plugin_name]
            print(f"✓ Unloaded plugin: {plugin_name}")

    def get_plugin(self, name: str) -> Optional[Plugin]:
        """Get loaded plugin by name"""
        return self.plugins.get(name)

    def list_plugins(self) -> List[Dict[str, Any]]:
        """List all loaded plugins"""
        return [
            {
                "name": p.metadata.name,
                "version": p.metadata.version,
                "author": p.metadata.author,
                "description": p.metadata.description,
                "enabled": p.metadata.enabled
            }
            for p in self.plugins.values()
        ]

    def get_tool_class(self, tool_name: str):
        """Get tool class for a given tool name"""
        plugin = self.get_plugin(tool_name)
        if plugin:
            return plugin.tool_class
        return None

    def _check_dependencies(self, dependencies: List[str]) -> List[str]:
        """Check if plugin dependencies are satisfied"""
        missing = []

        for dep in dependencies:
            try:
                __import__(dep)
            except ImportError:
                missing.append(dep)

        return missing

    def create_plugin_template(self, plugin_name: str, description: str = "") -> str:
        """Create a new plugin from template"""
        plugin_file = Path(self.plugin_dir) / f"{plugin_name}.py"

        if plugin_file.exists():
            return f"Plugin {plugin_name} already exists"

        # Read template
        template_file = Path(self.plugin_dir) / "example_plugin.py.template"
        if template_file.exists():
            template = template_file.read_text()

            # Customize template
            template = template.replace("example_tool", plugin_name)
            template = template.replace("Example Tool", plugin_name.replace('_', ' ').title())
            template = template.replace("ExampleTool", ''.join(word.capitalize() for word in plugin_name.split('_')))

            if description:
                template = template.replace(
                    "Example plugin demonstrating custom tools",
                    description
                )

            # Write new plugin file
            plugin_file.write_text(template)

            return f"✓ Created plugin: {plugin_file}"

        return "Template not found"


# Global plugin manager instance
_plugin_manager = None


def get_plugin_manager(plugin_dir: Optional[str] = None) -> PluginManager:
    """Get global plugin manager instance"""
    global _plugin_manager
    if _plugin_manager is None:
        _plugin_manager = PluginManager(plugin_dir)
    return _plugin_manager
