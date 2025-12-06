"""
Agent Zero Configuration CLI
Manage Agent Zero configuration settings
"""

import json
import os
from pathlib import Path
from typing import Optional, Any

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.syntax import Syntax

config_app = typer.Typer(help="Configuration management")
console = Console()

# Configuration paths
CONFIG_DIR = Path.home() / ".agent-zero"
CONFIG_FILE = CONFIG_DIR / "config.json"
ENV_FILE = Path.cwd() / ".env"


class ConfigManager:
    """Manage Agent Zero configuration"""

    def __init__(self, config_path: Path = CONFIG_FILE):
        self.config_path = config_path
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        self._config = self._load()

    def _load(self) -> dict:
        """Load configuration from file"""
        if self.config_path.exists():
            try:
                return json.loads(self.config_path.read_text())
            except json.JSONDecodeError:
                console.print(f"[yellow]Warning: Invalid config file, using defaults[/yellow]")
                return self._default_config()
        return self._default_config()

    def _default_config(self) -> dict:
        """Get default configuration"""
        return {
            "model": {
                "chat": "gemini-2.5-flash",
                "utility": "gemini-2.5-flash",
                "embedding": "models/embedding-001",
                "provider": "google"
            },
            "agent": {
                "max_iterations": 10,
                "timeout": 300,
                "rate_limit": 30,
                "auto_memory": False
            },
            "cli": {
                "theme": "dark",
                "verbose": False,
                "color": True
            },
            "marketplace": {
                "api_url": "https://api.agent-zero.io",
                "auto_update": False
            },
            "deployment": {
                "default_target": "local"
            },
            "api_keys": {
                "google": os.getenv("GOOGLE_API_KEY", ""),
                "openai": os.getenv("OPENAI_API_KEY", ""),
                "anthropic": os.getenv("ANTHROPIC_API_KEY", "")
            }
        }

    def _save(self):
        """Save configuration to file"""
        self.config_path.write_text(json.dumps(self._config, indent=2))

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        keys = key.split(".")
        value = self._config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
            if value is None:
                return default
        return value

    def set(self, key: str, value: Any):
        """Set configuration value"""
        keys = key.split(".")
        config = self._config

        # Navigate to the nested dictionary
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]

        # Set the value
        config[keys[-1]] = value
        self._save()

    def delete(self, key: str) -> bool:
        """Delete configuration key"""
        keys = key.split(".")
        config = self._config

        # Navigate to the parent dictionary
        for k in keys[:-1]:
            if k not in config:
                return False
            config = config[k]

        # Delete the key
        if keys[-1] in config:
            del config[keys[-1]]
            self._save()
            return True
        return False

    def list_all(self) -> dict:
        """Get all configuration"""
        return self._config

    def reset(self):
        """Reset to default configuration"""
        self._config = self._default_config()
        self._save()


@config_app.command("get")
def get_config(
    key: str = typer.Argument(..., help="Configuration key (use dot notation, e.g., model.chat)"),
):
    """Get a configuration value"""
    manager = ConfigManager()
    value = manager.get(key)

    if value is None:
        console.print(f"[yellow]Key '{key}' not found[/yellow]")
        raise typer.Exit(1)

    console.print(Panel(
        f"[cyan]{key}[/cyan] = [green]{value}[/green]",
        title="Configuration Value",
        border_style="blue"
    ))


@config_app.command("set")
def set_config(
    key: str = typer.Argument(..., help="Configuration key"),
    value: str = typer.Argument(..., help="Configuration value"),
    value_type: str = typer.Option("auto", "--type", "-t", help="Value type (auto/string/int/float/bool/json)"),
):
    """Set a configuration value"""
    manager = ConfigManager()

    # Convert value to appropriate type
    if value_type == "auto":
        # Auto-detect type
        if value.lower() in ("true", "false"):
            converted_value = value.lower() == "true"
        elif value.isdigit():
            converted_value = int(value)
        elif value.replace(".", "", 1).isdigit():
            converted_value = float(value)
        elif value.startswith("{") or value.startswith("["):
            try:
                converted_value = json.loads(value)
            except json.JSONDecodeError:
                converted_value = value
        else:
            converted_value = value
    elif value_type == "string":
        converted_value = value
    elif value_type == "int":
        converted_value = int(value)
    elif value_type == "float":
        converted_value = float(value)
    elif value_type == "bool":
        converted_value = value.lower() in ("true", "1", "yes")
    elif value_type == "json":
        converted_value = json.loads(value)
    else:
        converted_value = value

    manager.set(key, converted_value)

    console.print(f"[green]Set {key} = {converted_value}[/green]")


@config_app.command("list")
def list_config(
    section: Optional[str] = typer.Argument(None, help="Configuration section to list"),
    format: str = typer.Option("table", "--format", "-f", help="Output format (table/json/yaml)"),
):
    """List configuration values"""
    manager = ConfigManager()

    if section:
        config = manager.get(section, {})
        title = f"Configuration: {section}"
    else:
        config = manager.list_all()
        title = "Configuration"

    if format == "json":
        console.print(Syntax(json.dumps(config, indent=2), "json", theme="monokai"))
    elif format == "yaml":
        # Simple YAML output
        yaml_str = json.dumps(config, indent=2).replace("{", "").replace("}", "").replace('"', '').replace(",", "")
        console.print(Syntax(yaml_str, "yaml", theme="monokai"))
    else:  # table
        table = Table(title=title, show_header=True)
        table.add_column("Key", style="cyan", no_wrap=True)
        table.add_column("Value", style="green")
        table.add_column("Type", style="yellow")

        def add_rows(d: dict, prefix: str = ""):
            for k, v in d.items():
                full_key = f"{prefix}.{k}" if prefix else k
                if isinstance(v, dict):
                    add_rows(v, full_key)
                else:
                    table.add_row(full_key, str(v), type(v).__name__)

        add_rows(config)
        console.print(table)


@config_app.command("delete")
def delete_config(
    key: str = typer.Argument(..., help="Configuration key to delete"),
    force: bool = typer.Option(False, "--force", "-f", help="Skip confirmation"),
):
    """Delete a configuration key"""
    manager = ConfigManager()

    if not force:
        if not Confirm.ask(f"Delete configuration key '{key}'?"):
            console.print("[yellow]Cancelled[/yellow]")
            return

    if manager.delete(key):
        console.print(f"[green]Deleted {key}[/green]")
    else:
        console.print(f"[yellow]Key '{key}' not found[/yellow]")


@config_app.command("reset")
def reset_config(
    force: bool = typer.Option(False, "--force", "-f", help="Skip confirmation"),
):
    """Reset configuration to defaults"""
    if not force:
        if not Confirm.ask("Reset all configuration to defaults?"):
            console.print("[yellow]Cancelled[/yellow]")
            return

    manager = ConfigManager()
    manager.reset()

    console.print("[green]Configuration reset to defaults[/green]")


@config_app.command("edit")
def edit_config():
    """Edit configuration in default editor"""
    import subprocess

    manager = ConfigManager()
    editor = os.getenv("EDITOR", "nano")

    try:
        subprocess.run([editor, str(manager.config_path)])
        console.print("[green]Configuration updated[/green]")
    except Exception as e:
        console.print(f"[red]Failed to open editor: {e}[/red]")
        raise typer.Exit(1)


@config_app.command("validate")
def validate_config():
    """Validate configuration"""
    manager = ConfigManager()
    config = manager.list_all()

    errors = []
    warnings = []

    # Validate model configuration
    if not config.get("model", {}).get("chat"):
        errors.append("model.chat is required")

    # Validate API keys
    api_keys = config.get("api_keys", {})
    provider = config.get("model", {}).get("provider", "")

    if provider == "google" and not api_keys.get("google"):
        warnings.append("Google API key not set")
    elif provider == "openai" and not api_keys.get("openai"):
        warnings.append("OpenAI API key not set")

    # Display results
    if errors:
        console.print("\n[bold red]Errors:[/bold red]")
        for error in errors:
            console.print(f"  [red]✗[/red] {error}")

    if warnings:
        console.print("\n[bold yellow]Warnings:[/bold yellow]")
        for warning in warnings:
            console.print(f"  [yellow]⚠[/yellow] {warning}")

    if not errors and not warnings:
        console.print("[green]✓ Configuration is valid[/green]")
    elif errors:
        raise typer.Exit(1)


@config_app.command("export")
def export_config(
    output: str = typer.Argument("config.json", help="Output file path"),
    format: str = typer.Option("json", "--format", "-f", help="Export format (json/env)"),
):
    """Export configuration to file"""
    manager = ConfigManager()
    config = manager.list_all()

    output_path = Path(output)

    if format == "json":
        output_path.write_text(json.dumps(config, indent=2))
        console.print(f"[green]Configuration exported to {output}[/green]")
    elif format == "env":
        # Convert to .env format
        env_lines = []

        def flatten(d: dict, prefix: str = ""):
            for k, v in d.items():
                key = f"{prefix}_{k}".upper() if prefix else k.upper()
                if isinstance(v, dict):
                    flatten(v, key)
                else:
                    env_lines.append(f"{key}={v}")

        flatten(config)
        output_path.write_text("\n".join(env_lines))
        console.print(f"[green]Configuration exported to {output} (env format)[/green]")
    else:
        console.print(f"[red]Unknown format: {format}[/red]")
        raise typer.Exit(1)


@config_app.command("import")
def import_config(
    input: str = typer.Argument(..., help="Input file path"),
    merge: bool = typer.Option(False, "--merge", "-m", help="Merge with existing config"),
):
    """Import configuration from file"""
    input_path = Path(input)

    if not input_path.exists():
        console.print(f"[red]File not found: {input}[/red]")
        raise typer.Exit(1)

    manager = ConfigManager()

    try:
        new_config = json.loads(input_path.read_text())

        if merge:
            # Merge with existing config
            def deep_merge(base: dict, update: dict):
                for key, value in update.items():
                    if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                        deep_merge(base[key], value)
                    else:
                        base[key] = value

            current_config = manager.list_all()
            deep_merge(current_config, new_config)
            manager._config = current_config
        else:
            manager._config = new_config

        manager._save()
        console.print(f"[green]Configuration imported from {input}[/green]")

    except json.JSONDecodeError as e:
        console.print(f"[red]Invalid JSON file: {e}[/red]")
        raise typer.Exit(1)


@config_app.command("init")
def init_config(
    interactive: bool = typer.Option(True, "--interactive/--no-interactive", help="Interactive setup"),
):
    """Initialize Agent Zero configuration"""
    manager = ConfigManager()

    if manager.config_path.exists():
        if not Confirm.ask("Configuration already exists. Overwrite?"):
            console.print("[yellow]Cancelled[/yellow]")
            return

    if interactive:
        console.print(Panel(
            "[bold cyan]Agent Zero Configuration Setup[/bold cyan]\n\n"
            "Let's configure your Agent Zero installation.",
            border_style="cyan"
        ))

        # Model provider
        provider = Prompt.ask(
            "AI Provider",
            choices=["google", "openai", "anthropic", "ollama"],
            default="google"
        )

        # API key
        if provider in ("google", "openai", "anthropic"):
            api_key = Prompt.ask(f"{provider.title()} API Key", password=True)
            manager.set(f"api_keys.{provider}", api_key)

        manager.set("model.provider", provider)

        # Model selection
        default_models = {
            "google": "gemini-2.5-flash",
            "openai": "gpt-4o-mini",
            "anthropic": "claude-3-5-sonnet",
            "ollama": "llama3.2:3b-instruct-fp16"
        }

        chat_model = Prompt.ask("Chat Model", default=default_models.get(provider, ""))
        manager.set("model.chat", chat_model)

        console.print("\n[green]✓ Configuration initialized successfully[/green]")
        console.print(f"[dim]Config saved to: {manager.config_path}[/dim]")

    else:
        # Non-interactive: use defaults
        manager.reset()
        console.print("[green]Configuration initialized with defaults[/green]")


if __name__ == "__main__":
    config_app()
