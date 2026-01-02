"""
Agent Zero Agent Runner CLI
Execute and manage agents
"""

import asyncio
import sys
from pathlib import Path
from typing import Optional
from datetime import datetime

import typer
from rich.console import Console
from rich.panel import Panel
from rich.live import Live
from rich.spinner import Spinner
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.text import Text

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import models
from agent import AgentContext
from initialize import initialize
from python.helpers.print_style import PrintStyle

agent_app = typer.Typer(help="Agent execution and management")
console = Console()


async def run_task(
    task: str,
    agent: Optional[str] = None,
    model: Optional[str] = None,
    output: Optional[str] = None,
    timeout: Optional[int] = None,
):
    """Run a single task with Agent Zero"""

    # Initialize agent
    console.print("[dim]Initializing agent...[/dim]")
    config = initialize()

    # Override model if specified
    if model:
        console.print(f"[dim]Overriding model with: {model}[/dim]")

        parts = model.split("/", 1)
        if len(parts) == 2:
            provider, model_name = parts
        else:
            provider = "auto"
            model_name = model

        # Normalize provider
        provider = provider.lower()

        if provider == "openai":
            config.chat_model = models.get_openai_chat(model_name=model_name, temperature=0)
        elif provider == "anthropic":
             config.chat_model = models.get_anthropic_chat(model_name=model_name, temperature=0)
        elif provider == "google":
             config.chat_model = models.get_google_chat(model_name=model_name, temperature=0)
        elif provider == "groq":
             config.chat_model = models.get_groq_chat(model_name=model_name, temperature=0)
        elif provider == "mistral":
             config.chat_model = models.get_mistral_chat(model_name=model_name, temperature=0)
        elif provider == "ollama":
             config.chat_model = models.get_ollama_chat(model_name=model_name, temperature=0)
        elif provider == "openrouter":
             config.chat_model = models.get_openrouter_chat(model_name=model_name, temperature=0)
        elif provider == "sambanova":
             config.chat_model = models.get_sambanova_chat(model_name=model_name, temperature=0)
        elif provider == "lmstudio":
             config.chat_model = models.get_lmstudio_chat(model_name=model_name, temperature=0)
        elif provider == "azure":
             config.chat_model = models.get_azure_openai_chat(deployment_name=model_name, temperature=0)
        elif provider == "auto":
            # Heuristics
            if model_name.startswith("gpt-") or model_name.startswith("o1-"):
                config.chat_model = models.get_openai_chat(model_name=model_name, temperature=0)
            elif model_name.startswith("claude-"):
                config.chat_model = models.get_anthropic_chat(model_name=model_name, temperature=0)
            elif model_name.startswith("gemini-"):
                config.chat_model = models.get_google_chat(model_name=model_name, temperature=0)
            elif model_name.startswith("llama"):
                # Ambiguous. Let's assume Ollama for local or Groq for speed?
                # Defaulting to Ollama seems safe for "llama"
                config.chat_model = models.get_ollama_chat(model_name=model_name, temperature=0)
            else:
                 console.print(f"[bold red]Error:[/bold red] Could not determine provider for model '{model}'. Please use format 'provider/model_name' (e.g. openai/gpt-4o).")
                 raise typer.Exit(1)
        else:
             console.print(f"[bold red]Error:[/bold red] Unknown provider '{provider}'. Supported providers: openai, anthropic, google, groq, mistral, ollama, openrouter, sambanova, lmstudio, azure.")
             raise typer.Exit(1)

        # Update utility model to match
        config.utility_model = config.chat_model

    context = AgentContext(config)

    # Set timeout if specified
    if timeout:
        context.agent0.set_data("timeout", timeout)

    # Execute task
    with Live(Spinner("dots", text=f"[cyan]Executing: {task}[/cyan]"), console=console):
        try:
            result = await context.communicate(task).result()

            # Output result
            console.print("\n")
            console.print(Panel(
                result,
                title="[bold green]Task Result[/bold green]",
                border_style="green"
            ))

            # Save to file if requested
            if output:
                output_path = Path(output)
                output_path.write_text(result)
                console.print(f"\n[dim]Result saved to: {output}[/dim]")

        except Exception as e:
            console.print(f"\n[bold red]Error:[/bold red] {str(e)}")
            raise typer.Exit(1)


@agent_app.command("run")
def run(
    task: str = typer.Argument(..., help="Task description"),
    agent: Optional[str] = typer.Option(None, "--agent", "-a", help="Specialized agent"),
    model: Optional[str] = typer.Option(None, "--model", "-m", help="Model to use"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output file"),
    timeout: Optional[int] = typer.Option(None, "--timeout", "-t", help="Timeout in seconds"),
):
    """Execute a single task"""
    asyncio.run(run_task(task, agent=agent, model=model, output=output, timeout=timeout))


@agent_app.command("list")
def list_agents():
    """List available agents"""

    # Scan for available agents
    agents_dir = Path("agents")
    custom_agents = []

    if agents_dir.exists():
        for agent_file in agents_dir.glob("*.py"):
            if agent_file.name != "__init__.py":
                custom_agents.append(agent_file.stem)

    # Built-in agents
    builtin_agents = [
        ("default", "General purpose AI agent"),
        ("code", "Code analysis and development"),
        ("research", "Research and information gathering"),
        ("data", "Data analysis and visualization"),
    ]

    console.print("\n[bold cyan]Built-in Agents:[/bold cyan]")
    for name, description in builtin_agents:
        console.print(f"  [green]{name:15}[/green] {description}")

    if custom_agents:
        console.print("\n[bold cyan]Custom Agents:[/bold cyan]")
        for name in custom_agents:
            console.print(f"  [green]{name}[/green]")

    console.print(f"\n[dim]Use: agent-zero agent run --agent <name> \"task\"[/dim]")


@agent_app.command("info")
def agent_info(
    name: str = typer.Argument(..., help="Agent name"),
):
    """Show agent information"""

    # Check if agent exists
    agent_file = Path("agents") / f"{name}.py"

    if not agent_file.exists():
        console.print(f"[yellow]Agent '{name}' not found[/yellow]")
        return

    # Read agent file
    content = agent_file.read_text()

    # Extract docstring
    import ast
    try:
        tree = ast.parse(content)
        docstring = ast.get_docstring(tree)
    except:
        docstring = "No description available"

    info_panel = f"""[bold cyan]{name}[/bold cyan]

[bold]Description:[/bold]
{docstring or 'No description available'}

[bold]Location:[/bold]
[dim]{agent_file.absolute()}[/dim]
"""

    console.print(Panel(info_panel, title="Agent Information", border_style="cyan"))


@agent_app.command("create")
def create_agent(
    name: str = typer.Argument(..., help="Agent name"),
    template: str = typer.Option("default", "--template", "-t", help="Agent template"),
):
    """Create a new custom agent"""

    agents_dir = Path("agents")
    agents_dir.mkdir(exist_ok=True)

    agent_file = agents_dir / f"{name}.py"

    if agent_file.exists():
        console.print(f"[yellow]Agent '{name}' already exists[/yellow]")
        if not typer.confirm("Overwrite?"):
            return

    # Generate agent code
    class_name = ''.join(word.capitalize() for word in name.split('_'))

    agent_code = f'''"""
{name} - Custom Agent
Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

from python.helpers.tool import Tool, Response


class {class_name}Agent(Tool):
    """
    {class_name} Agent

    A specialized agent for {name.replace('_', ' ')} tasks.

    Capabilities:
    - Task execution
    - Data processing
    - Result generation
    """

    async def execute(self, **kwargs):
        """
        Execute the {name} agent

        Args:
            task: Task description
            **kwargs: Additional parameters

        Returns:
            Response object with results
        """

        # Get parameters
        task = self.args.get("task", "")

        # Agent logic here
        self.agent.set_data("timeout", 0)

        # Example: Process the task
        result = f"Processing task with {class_name}Agent: {{task}}"

        # You can use other tools
        # await self.agent.call_tool("tool_name", {{"param": "value"}})

        # Return response
        return Response(
            message=result,
            break_loop=False  # Set to True to end the conversation
        )
'''

    agent_file.write_text(agent_code)

    console.print(f"[green]✓ Created agent: {name}[/green]")
    console.print(f"[dim]Location: {agent_file}[/dim]")
    console.print(f"\n[cyan]Next steps:[/cyan]")
    console.print(f"1. Edit {agent_file} to implement your agent logic")
    console.print(f"2. Test with: agent-zero agent run --agent {name} \"your task\"")


@agent_app.command("test")
def test_agent(
    name: str = typer.Argument(..., help="Agent name"),
    task: str = typer.Option("test task", "--task", "-t", help="Test task"),
):
    """Test an agent with a sample task"""

    console.print(f"[yellow]Testing agent '{name}' with task: {task}[/yellow]\n")

    # Run the agent
    asyncio.run(run_task(task, agent=name))


if __name__ == "__main__":
    agent_app()
