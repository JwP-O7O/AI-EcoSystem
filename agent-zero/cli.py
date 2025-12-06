#!/usr/bin/env python3
"""
Agent Zero CLI 2.0 - Advanced Command Line Interface
Modern, user-friendly CLI with marketplace, project management, and enhanced UX
"""

import asyncio
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

import typer
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from typing import Optional

from python.cli.marketplace import marketplace_app
from python.cli.config import config_app
from python.cli.project import project_app
from python.cli.agent_runner import agent_app
from python.cli.logs import logs_app

# Initialize main app
app = typer.Typer(
    name="agent-zero",
    help="Agent Zero CLI 2.0 - Advanced AI Agent Framework",
    add_completion=True,
    rich_markup_mode="rich",
)

console = Console()

# Add sub-commands
app.add_typer(marketplace_app, name="marketplace", help="Marketplace for agents, tools, and prompts")
app.add_typer(config_app, name="config", help="Configuration management")
app.add_typer(project_app, name="project", help="Project management and scaffolding")
app.add_typer(agent_app, name="agent", help="Agent execution and management")
app.add_typer(logs_app, name="logs", help="View agent logs and execution history")


@app.command()
def version():
    """Display Agent Zero version information"""
    console.print(Panel.fit(
        "[bold cyan]Agent Zero CLI[/bold cyan]\n"
        "[yellow]Version:[/yellow] 2.0.0\n"
        "[yellow]Framework:[/yellow] Advanced AI Agent System\n"
        "[yellow]Platform:[/yellow] Universal (Termux/Desktop)",
        title="Version Info",
        border_style="cyan"
    ))


@app.command()
def chat(
    agent: Optional[str] = typer.Option(None, "--agent", "-a", help="Use specialized agent"),
    model: Optional[str] = typer.Option(None, "--model", "-m", help="Override default model"),
    debug: bool = typer.Option(False, "--debug", "-d", help="Enable debug mode"),
):
    """Start interactive chat session with Agent Zero"""
    from python.cli.chat_interface import start_chat

    console.print(Panel(
        "[bold green]Starting Agent Zero Chat Interface[/bold green]\n"
        f"Agent: [cyan]{agent or 'default'}[/cyan]\n"
        f"Model: [cyan]{model or 'default'}[/cyan]",
        border_style="green"
    ))

    asyncio.run(start_chat(agent=agent, model=model, debug=debug))


@app.command()
def init(
    name: str = typer.Argument(..., help="Project name"),
    template: str = typer.Option("default", "--template", "-t", help="Project template"),
    path: Optional[str] = typer.Option(None, "--path", "-p", help="Target directory"),
):
    """Initialize a new Agent Zero project"""
    from python.cli.project import init_project

    target_path = Path(path) if path else Path.cwd() / name

    console.print(Panel(
        f"[bold green]Initializing Project[/bold green]\n"
        f"Name: [cyan]{name}[/cyan]\n"
        f"Template: [cyan]{template}[/cyan]\n"
        f"Path: [cyan]{target_path}[/cyan]",
        border_style="green"
    ))

    init_project(name, template, target_path)


@app.command()
def run(
    task: str = typer.Argument(..., help="Task description for the agent"),
    agent: Optional[str] = typer.Option(None, "--agent", "-a", help="Specialized agent to use"),
    model: Optional[str] = typer.Option(None, "--model", "-m", help="Model to use"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output file for results"),
    timeout: Optional[int] = typer.Option(None, "--timeout", "-t", help="Timeout in seconds"),
):
    """Execute a single task with Agent Zero"""
    from python.cli.agent_runner import run_task

    console.print(Panel(
        f"[bold green]Executing Task[/bold green]\n"
        f"Task: [cyan]{task}[/cyan]\n"
        f"Agent: [cyan]{agent or 'default'}[/cyan]",
        border_style="green"
    ))

    asyncio.run(run_task(task, agent=agent, model=model, output=output, timeout=timeout))


@app.command()
def dev(
    port: int = typer.Option(8080, "--port", "-p", help="Development server port"),
    host: str = typer.Option("0.0.0.0", "--host", "-h", help="Host to bind to"),
    reload: bool = typer.Option(True, "--reload/--no-reload", help="Enable hot reload"),
):
    """Start development server with hot reload"""
    from python.cli.dev_server import start_dev_server

    console.print(Panel(
        f"[bold green]Starting Development Server[/bold green]\n"
        f"URL: [cyan]http://{host}:{port}[/cyan]\n"
        f"Hot Reload: [cyan]{'Enabled' if reload else 'Disabled'}[/cyan]",
        border_style="green"
    ))

    start_dev_server(host=host, port=port, reload=reload)


@app.command()
def deploy(
    target: str = typer.Argument(..., help="Deployment target (local/cloud/mobile)"),
    config_file: Optional[str] = typer.Option(None, "--config", "-c", help="Deployment config file"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Simulate deployment"),
):
    """Deploy Agent Zero to various platforms"""
    from python.cli.deployment import deploy_agent

    console.print(Panel(
        f"[bold green]Deploying Agent Zero[/bold green]\n"
        f"Target: [cyan]{target}[/cyan]\n"
        f"Dry Run: [cyan]{'Yes' if dry_run else 'No'}[/cyan]",
        border_style="green"
    ))

    deploy_agent(target, config_file=config_file, dry_run=dry_run)


@app.command()
def status():
    """Show system status and running agents"""
    from python.cli.status import show_status

    show_status()


@app.callback()
def main(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output"),
    quiet: bool = typer.Option(False, "--quiet", "-q", help="Suppress non-essential output"),
):
    """
    Agent Zero CLI 2.0 - Advanced AI Agent Framework

    A modern, powerful CLI for managing AI agents, projects, and deployments.
    """
    if verbose:
        os.environ['AGENT_ZERO_VERBOSE'] = '1'
    if quiet:
        os.environ['AGENT_ZERO_QUIET'] = '1'


def cli_main():
    """Entry point for CLI"""
    try:
        app()
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user[/yellow]")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[bold red]Error:[/bold red] {str(e)}")
        if os.environ.get('AGENT_ZERO_VERBOSE'):
            console.print_exception()
        sys.exit(1)


if __name__ == "__main__":
    cli_main()
