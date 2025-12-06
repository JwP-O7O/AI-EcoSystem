"""
Agent Zero Logs CLI
View and manage agent execution logs
"""

import json
from pathlib import Path
from typing import Optional
from datetime import datetime

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.syntax import Syntax

logs_app = typer.Typer(help="View agent logs and execution history")
console = Console()

LOGS_DIR = Path("logs")


@logs_app.command("list")
def list_logs(
    limit: int = typer.Option(10, "--limit", "-n", help="Number of logs to show"),
    agent: Optional[str] = typer.Option(None, "--agent", "-a", help="Filter by agent"),
):
    """List recent execution logs"""

    if not LOGS_DIR.exists():
        console.print("[yellow]No logs directory found[/yellow]")
        return

    log_files = sorted(LOGS_DIR.glob("*.log"), key=lambda x: x.stat().st_mtime, reverse=True)

    if not log_files:
        console.print("[yellow]No logs found[/yellow]")
        return

    table = Table(title="Recent Execution Logs", show_header=True)
    table.add_column("Date/Time", style="cyan")
    table.add_column("Agent", style="green")
    table.add_column("Status", style="yellow")
    table.add_column("Duration", style="blue")
    table.add_column("File", style="dim")

    for log_file in log_files[:limit]:
        # Parse log file
        try:
            # Simple parsing - in production, use structured logging
            stat = log_file.stat()
            mtime = datetime.fromtimestamp(stat.st_mtime)

            table.add_row(
                mtime.strftime("%Y-%m-%d %H:%M:%S"),
                "agent-0",  # Default agent
                "completed",
                "-",
                log_file.name
            )
        except Exception:
            continue

    console.print(table)


@logs_app.command("show")
def show_log(
    log_id: str = typer.Argument(..., help="Log ID or filename"),
    follow: bool = typer.Option(False, "--follow", "-f", help="Follow log updates"),
    tail: int = typer.Option(50, "--tail", "-n", help="Show last N lines"),
):
    """Show log contents"""

    log_file = LOGS_DIR / f"{log_id}.log" if not log_id.endswith('.log') else LOGS_DIR / log_id

    if not log_file.exists():
        console.print(f"[yellow]Log file not found: {log_id}[/yellow]")
        return

    if follow:
        console.print(f"[cyan]Following {log_file.name}...[/cyan]")
        console.print("[dim]Press Ctrl+C to stop[/dim]\n")

        # Simple tail -f implementation
        import time
        with open(log_file, 'r') as f:
            # Go to end
            f.seek(0, 2)
            while True:
                line = f.readline()
                if line:
                    console.print(line, end='')
                else:
                    time.sleep(0.1)
    else:
        content = log_file.read_text()
        lines = content.split('\n')

        if tail and len(lines) > tail:
            lines = lines[-tail:]
            console.print(f"[dim]Showing last {tail} lines[/dim]\n")

        console.print('\n'.join(lines))


@logs_app.command("clear")
def clear_logs(
    all: bool = typer.Option(False, "--all", help="Clear all logs"),
    days: Optional[int] = typer.Option(None, "--days", help="Clear logs older than N days"),
):
    """Clear execution logs"""

    if not LOGS_DIR.exists():
        console.print("[yellow]No logs directory found[/yellow]")
        return

    if all:
        if not typer.confirm("Clear all logs?"):
            console.print("[yellow]Cancelled[/yellow]")
            return

        count = 0
        for log_file in LOGS_DIR.glob("*.log"):
            log_file.unlink()
            count += 1

        console.print(f"[green]Cleared {count} log files[/green]")

    elif days:
        import time
        threshold = time.time() - (days * 24 * 60 * 60)
        count = 0

        for log_file in LOGS_DIR.glob("*.log"):
            if log_file.stat().st_mtime < threshold:
                log_file.unlink()
                count += 1

        console.print(f"[green]Cleared {count} log files older than {days} days[/green]")

    else:
        console.print("[yellow]Specify --all or --days[/yellow]")


if __name__ == "__main__":
    logs_app()
