"""
Agent Zero Interactive Chat Interface
Enhanced chat UI with rich formatting
"""

import asyncio
import sys
from pathlib import Path
from typing import Optional
import os

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
import models

console = Console()


def get_llm_from_string(model_spec: str):
    """
    Parses a model specification string and returns the corresponding LangChain LLM object.

    Format: "provider/model_name"
    Example: "openai/gpt-4o", "anthropic/claude-3-5-sonnet"

    If no provider is specified (no '/'), defaults to OpenRouter.
    """
    if "/" in model_spec:
        provider, model_name = model_spec.split("/", 1)
    else:
        # Default to OpenRouter if no provider specified
        provider = "openrouter"
        model_name = model_spec

    provider = provider.lower()

    # Map providers to models.py functions
    if provider == "openai":
        return models.get_openai_chat(model_name=model_name, temperature=0)
    elif provider == "anthropic":
        return models.get_anthropic_chat(model_name=model_name, temperature=0)
    elif provider == "google" or provider == "gemini":
        return models.get_google_chat(model_name=model_name, temperature=0)
    elif provider == "ollama":
        return models.get_ollama_chat(model_name=model_name, temperature=0)
    elif provider == "azure":
        return models.get_azure_openai_chat(deployment_name=model_name, temperature=0)
    elif provider == "mistral":
        return models.get_mistral_chat(model_name=model_name, temperature=0)
    elif provider == "groq":
        return models.get_groq_chat(model_name=model_name, temperature=0)
    elif provider == "openrouter":
        return models.get_openrouter_chat(model_name=model_name)
    elif provider == "sambanova":
        return models.get_sambanova_chat(model_name=model_name, temperature=0)
    elif provider == "lmstudio":
        return models.get_lmstudio_chat(model_name=model_name, temperature=0)
    else:
        # Fallback to OpenRouter for unknown providers, or handle as error.
        # Following agent_runner behavior: default to OpenRouter
        # But here we identified provider from split, so if it's unknown, maybe we should warn?
        # The prompt says: "defaulting to OpenRouter if the provider is unknown."
        console.print(f"[yellow]Warning: Unknown provider '{provider}', defaulting to OpenRouter.[/yellow]")
        return models.get_openrouter_chat(model_name=f"{provider}/{model_name}")


async def start_chat(agent: Optional[str] = None, model: Optional[str] = None, debug: bool = False):
    """Start interactive chat session"""

    # Initialize agent
    console.print("[dim]Initializing Agent Zero...[/dim]")
    config = initialize()

    # Override model if specified
    if model:
        try:
            console.print(f"[dim]Overriding model with: {model}[/dim]")
            new_llm = get_llm_from_string(model)
            config.chat_model = new_llm
            config.utility_model = new_llm
        except Exception as e:
            console.print(f"[bold red]Error initializing model override: {e}[/bold red]")
            console.print("[yellow]Falling back to default model.[/yellow]")

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
