"""
Agent Zero Status CLI
Show system status and running agents
"""

import os
import sys
import psutil
from pathlib import Path
from datetime import datetime

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.columns import Columns

console = Console()


def show_status():
    """Show system status and running agents"""

    # System info
    system_info = Panel(
        f"[bold]Platform:[/bold] {sys.platform}\n"
        f"[bold]Python:[/bold] {sys.version.split()[0]}\n"
        f"[bold]CPU:[/bold] {psutil.cpu_count()} cores ({psutil.cpu_percent()}% used)\n"
        f"[bold]Memory:[/bold] {psutil.virtual_memory().percent}% used\n"
        f"[bold]Disk:[/bold] {psutil.disk_usage('/').percent}% used",
        title="[cyan]System Information[/cyan]",
        border_style="cyan"
    )

    # Agent Zero info
    agent_info = Panel(
        f"[bold]Version:[/bold] 2.0.0\n"
        f"[bold]CLI Version:[/bold] 2.0.0\n"
        f"[bold]Status:[/bold] [green]Active[/green]\n"
        f"[bold]Uptime:[/bold] N/A\n"
        f"[bold]Active Agents:[/bold] 0",
        title="[green]Agent Zero Status[/green]",
        border_style="green"
    )

    console.print(Columns([system_info, agent_info]))

    # Running processes
    console.print("\n[bold cyan]Running Agent Processes:[/bold cyan]")

    table = Table(show_header=True)
    table.add_column("PID", style="cyan")
    table.add_column("Agent", style="green")
    table.add_column("Status", style="yellow")
    table.add_column("CPU%", style="blue")
    table.add_column("Memory", style="magenta")
    table.add_column("Started", style="dim")

    # Find Agent Zero processes
    found_processes = False
    for proc in psutil.process_iter(['pid', 'name', 'create_time', 'cpu_percent', 'memory_info']):
        try:
            if 'python' in proc.info['name'].lower():
                cmdline = ' '.join(proc.cmdline())
                if 'agent' in cmdline.lower() or 'cli.py' in cmdline:
                    found_processes = True
                    started = datetime.fromtimestamp(proc.info['create_time'])
                    mem_mb = proc.info['memory_info'].rss / 1024 / 1024

                    table.add_row(
                        str(proc.info['pid']),
                        "agent-zero",
                        "running",
                        f"{proc.info['cpu_percent']:.1f}",
                        f"{mem_mb:.1f} MB",
                        started.strftime("%H:%M:%S")
                    )
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    if found_processes:
        console.print(table)
    else:
        console.print("[dim]No active agent processes found[/dim]")

    # Configuration
    config_file = Path.home() / ".agent-zero" / "config.json"
    if config_file.exists():
        console.print(f"\n[bold cyan]Configuration:[/bold cyan]")
        console.print(f"[dim]Location: {config_file}[/dim]")
        console.print(f"[dim]Last modified: {datetime.fromtimestamp(config_file.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')}[/dim]")
    else:
        console.print(f"\n[yellow]No configuration file found[/yellow]")
        console.print(f"[dim]Run: agent-zero config init[/dim]")
