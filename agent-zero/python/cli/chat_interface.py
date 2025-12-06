"""
Agent Zero Interactive Chat Interface
Enhanced chat UI with rich formatting
"""

import asyncio
import sys
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.live import Live
from rich.text import Text

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agent import AgentContext
from initialize import initialize
from python.helpers.print_style import PrintStyle

console = Console()


async def start_chat(agent: Optional[str] = None, model: Optional[str] = None, debug: bool = False):
    """Start interactive chat session"""

    # Initialize agent
    console.print("[dim]Initializing Agent Zero...[/dim]")
    config = initialize()

    # Override model if specified
    if model:
        # TODO: Implement model override
        pass

    context = AgentContext(config)

    # Welcome message
    welcome_text = """
# Welcome to Agent Zero CLI 2.0

I'm Agent Zero, your advanced AI assistant. I can help you with:

- Code analysis and development
- Research and information gathering
- Task automation
- Data processing
- And much more!

**Commands:**
- Type your message to chat
- `exit` or `quit` to leave
- `clear` to clear screen
- `help` for more commands

Let's get started! What can I help you with today?
"""

    console.print(Panel(
        Markdown(welcome_text),
        title="[bold cyan]Agent Zero[/bold cyan]",
        border_style="cyan"
    ))

    # Main chat loop
    while True:
        try:
            # Get user input
            user_input = console.input("\n[bold cyan]You:[/bold cyan] ").strip()

            if not user_input:
                continue

            # Handle commands
            if user_input.lower() in ['exit', 'quit', 'e']:
                console.print("[yellow]Goodbye![/yellow]")
                break

            if user_input.lower() == 'clear':
                console.clear()
                continue

            if user_input.lower() == 'help':
                show_help()
                continue

            # Process message
            console.print()
            with Live(console=console) as live:
                live.update(Text("Agent Zero is thinking...", style="dim italic"))

                try:
                    result = await context.communicate(user_input).result()

                    # Display response
                    live.update(Panel(
                        Markdown(result),
                        title="[bold green]Agent Zero[/bold green]",
                        border_style="green"
                    ))

                except Exception as e:
                    live.update(Panel(
                        f"[red]Error: {str(e)}[/red]",
                        title="[bold red]Error[/bold red]",
                        border_style="red"
                    ))

        except KeyboardInterrupt:
            console.print("\n[yellow]Use 'exit' to quit[/yellow]")
            continue
        except EOFError:
            break


def show_help():
    """Show help information"""
    help_text = """
# Agent Zero Chat Commands

**Basic Commands:**
- `exit`, `quit` - Exit the chat
- `clear` - Clear the screen
- `help` - Show this help message

**Chat Tips:**
- Be specific about what you want
- You can ask follow-up questions
- Agent Zero has memory of the conversation

**Examples:**
- "Analyze the code in main.py"
- "Search for information about Python asyncio"
- "Create a REST API with FastAPI"
"""

    console.print(Panel(
        Markdown(help_text),
        title="Help",
        border_style="blue"
    ))
