"""
Agent Zero Development Server
Hot-reload development environment
"""

import subprocess
import sys
from pathlib import Path

from rich.console import Console
from rich.panel import Panel

console = Console()


def start_dev_server(host: str = "0.0.0.0", port: int = 8080, reload: bool = True):
    """Start development server with hot reload"""

    console.print(Panel(
        f"[bold green]Agent Zero Development Server[/bold green]\n\n"
        f"Server: http://{host}:{port}\n"
        f"Hot Reload: {'Enabled' if reload else 'Disabled'}\n\n"
        f"[dim]Press Ctrl+C to stop[/dim]",
        border_style="green"
    ))

    # For now, just run the regular CLI
    # In production, this would start a web server with hot reload
    try:
        if reload:
            console.print("\n[cyan]Watching for file changes...[/cyan]\n")

            # Simple file watcher (in production, use watchdog)
            import time
            from watchlib import watch

            # Run in watch mode
            console.print("[yellow]Development mode with hot reload not fully implemented[/yellow]")
            console.print("[dim]Running standard mode...[/dim]\n")

        # Run the CLI
        from run_cli import main
        main()

    except KeyboardInterrupt:
        console.print("\n[yellow]Development server stopped[/yellow]")
