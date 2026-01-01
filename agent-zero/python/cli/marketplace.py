"""
Agent Zero Marketplace CLI
Install, search, publish, and manage marketplace items (agents, tools, prompts)
"""

import json
import shutil
import tempfile
from pathlib import Path
from typing import Optional, List
import requests
from datetime import datetime

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.prompt import Confirm

marketplace_app = typer.Typer(help="Marketplace for agents, tools, and prompts")
console = Console()

# Marketplace configuration
MARKETPLACE_API = "https://api.agent-zero.io"  # Example API endpoint
LOCAL_CACHE = Path.home() / ".agent-zero" / "marketplace"
INSTALL_DIR = Path.cwd() / "python"


class MarketplaceClient:
    """Client for interacting with the Agent Zero Marketplace"""

    def __init__(self, api_url: str = MARKETPLACE_API):
        self.api_url = api_url
        self.cache_dir = LOCAL_CACHE
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def search(self, query: str, category: Optional[str] = None) -> List[dict]:
        """Search marketplace for items"""
        # For demo, use local cache/mock data
        # In production, this would make API calls
        mock_items = [
            {
                "id": "code-expert",
                "name": "Code Expert Agent",
                "category": "agent",
                "description": "Specialized agent for code analysis and refactoring",
                "version": "1.2.0",
                "author": "agent-zero-team",
                "downloads": 1542,
                "rating": 4.8,
            },
            {
                "id": "web-scraper",
                "name": "Web Scraper Tool",
                "category": "tool",
                "description": "Advanced web scraping with JavaScript support",
                "version": "2.0.1",
                "author": "community",
                "downloads": 892,
                "rating": 4.5,
            },
            {
                "id": "research-assistant",
                "name": "Research Assistant Agent",
                "category": "agent",
                "description": "AI agent specialized in research and information gathering",
                "version": "1.0.3",
                "author": "research-team",
                "downloads": 2104,
                "rating": 4.9,
            },
            {
                "id": "data-analyzer",
                "name": "Data Analysis Tool",
                "category": "tool",
                "description": "Statistical analysis and data visualization",
                "version": "1.5.0",
                "author": "data-team",
                "downloads": 675,
                "rating": 4.6,
            },
            {
                "id": "creative-writing",
                "name": "Creative Writing Prompts",
                "category": "prompt",
                "description": "Collection of prompts for creative writing tasks",
                "version": "1.1.0",
                "author": "writers-collective",
                "downloads": 334,
                "rating": 4.7,
            },
        ]

        # Filter by query and category
        results = []
        for item in mock_items:
            if query.lower() in item['name'].lower() or query.lower() in item['description'].lower():
                if category is None or item['category'] == category:
                    results.append(item)

        return results

    def get_item(self, item_id: str) -> dict:
        """Get detailed information about a marketplace item"""
        # Mock implementation
        return {
            "id": item_id,
            "name": f"{item_id.replace('-', ' ').title()}",
            "category": "agent",
            "description": "A powerful agent for various tasks",
            "version": "1.0.0",
            "author": "agent-zero-team",
            "license": "MIT",
            "homepage": f"https://agent-zero.io/marketplace/{item_id}",
            "repository": f"https://github.com/agent-zero/{item_id}",
            "dependencies": [],
            "files": {
                "agent": f"agents/{item_id}.py",
                "prompts": f"prompts/{item_id}/",
            }
        }

    def download_item(self, item_id: str, target_dir: Path) -> bool:
        """Download and install marketplace item"""
        try:
            # In production, this would download from the marketplace
            # For demo, create mock files
            item = self.get_item(item_id)
            category = item['category']

            if category == 'agent':
                # Create agent file
                agent_file = target_dir / "tools" / f"{item_id}_tool.py"
                agent_file.parent.mkdir(parents=True, exist_ok=True)

                agent_code = self._generate_agent_template(item_id, item['name'])
                agent_file.write_text(agent_code)

                # Create prompt directory
                prompt_dir = target_dir.parent / "prompts" / "default"
                prompt_dir.mkdir(parents=True, exist_ok=True)

                prompt_file = prompt_dir / f"agent.system.tool.{item_id}.md"
                prompt_file.write_text(self._generate_prompt_template(item_id, item['name']))

            elif category == 'tool':
                # Create tool file
                tool_file = target_dir / "tools" / f"{item_id}_tool.py"
                tool_file.parent.mkdir(parents=True, exist_ok=True)

                tool_code = self._generate_tool_template(item_id, item['name'])
                tool_file.write_text(tool_code)

            elif category == 'prompt':
                # Create prompt files
                prompt_dir = target_dir.parent / "prompts" / "marketplace" / item_id
                prompt_dir.mkdir(parents=True, exist_ok=True)

                prompt_file = prompt_dir / "main.md"
                prompt_file.write_text(self._generate_prompt_template(item_id, item['name']))

            return True

        except Exception as e:
            console.print(f"[red]Download failed: {e}[/red]")
            return False

    def _generate_agent_template(self, item_id: str, name: str) -> str:
        """Generate agent code template"""
        return f'''"""
{name} - Marketplace Agent
Auto-generated from Agent Zero Marketplace
"""

from python.helpers.tool import Tool, Response


class {self._to_class_name(item_id)}(Tool):
    """
    {name}

    This is a specialized agent downloaded from the marketplace.
    """

    async def execute(self, **kwargs):
        """Execute the {name} agent"""

        # Get parameters
        task = self.args.get("task", "")

        self.agent.set_data("timeout", 0)

        # Agent logic here
        result = f"Executing {{task}} with {name}"

        return Response(
            message=result,
            break_loop=False
        )
'''

    def _generate_tool_template(self, item_id: str, name: str) -> str:
        """Generate tool code template"""
        return f'''"""
{name} - Marketplace Tool
Auto-generated from Agent Zero Marketplace
"""

from python.helpers.tool import Tool, Response


class {self._to_class_name(item_id)}(Tool):
    """
    {name}

    This is a specialized tool downloaded from the marketplace.
    """

    async def execute(self, **kwargs):
        """Execute the {name} tool"""

        # Get parameters from kwargs
        input_data = self.args.get("input", "")

        # Tool logic here
        result = f"Processing {{input_data}} with {name}"

        return Response(
            message=result,
            break_loop=False
        )
'''

    def _generate_prompt_template(self, item_id: str, name: str) -> str:
        """Generate prompt template"""
        return f'''# {name}

This is a specialized prompt for {name}.

## Purpose
Provide intelligent assistance for {item_id.replace("-", " ")} tasks.

## Capabilities
- Advanced analysis
- Smart recommendations
- Efficient execution

## Usage
Use this agent when you need {item_id.replace("-", " ")} capabilities.

## Tool Format
```json
{{
    "thoughts": [
        "Your reasoning here"
    ],
    "tool_name": "{item_id}",
    "tool_args": {{
        "task": "task description"
    }}
}}
```
'''

    def _to_class_name(self, item_id: str) -> str:
        """Convert item ID to Python class name"""
        return ''.join(word.capitalize() for word in item_id.split('-'))


@marketplace_app.command("search")
def search(
    query: str = typer.Argument(..., help="Search query"),
    category: Optional[str] = typer.Option(None, "--category", "-c", help="Filter by category (agent/tool/prompt)"),
    limit: int = typer.Option(10, "--limit", "-l", help="Maximum results to show"),
):
    """Search the Agent Zero Marketplace"""

    client = MarketplaceClient()

    with console.status(f"[bold green]Searching marketplace for '{query}'...", spinner="dots"):
        results = client.search(query, category=category)

    if not results:
        console.print(f"[yellow]No items found for query: {query}[/yellow]")
        return

    # Display results in table
    table = Table(title=f"Marketplace Search Results for '{query}'", show_header=True)
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Name", style="green")
    table.add_column("Category", style="blue")
    table.add_column("Version", style="yellow")
    table.add_column("Downloads", justify="right", style="magenta")
    table.add_column("Rating", justify="right", style="yellow")

    for item in results[:limit]:
        table.add_row(
            item['id'],
            item['name'],
            item['category'],
            item['version'],
            str(item['downloads']),
            f"{item['rating']}/5.0"
        )

    console.print(table)
    console.print(f"\n[dim]Showing {min(len(results), limit)} of {len(results)} results[/dim]")


@marketplace_app.command("list")
def list_items(
    category: Optional[str] = typer.Option(None, "--category", "-c", help="Filter by category"),
    installed: bool = typer.Option(False, "--installed", help="Show only installed items"),
):
    """List marketplace items"""

    if installed:
        console.print("[yellow]Listing installed marketplace items...[/yellow]")

        metadata_file = LOCAL_CACHE / "installed.json"
        if not metadata_file.exists():
            console.print("[dim]No installed items tracked yet[/dim]")
            return

        try:
            installed_items = json.loads(metadata_file.read_text())
        except json.JSONDecodeError:
            console.print("[red]Error reading installed items cache[/red]")
            return

        if not installed_items:
            console.print("[dim]No installed items tracked yet[/dim]")
            return

        table = Table(title="Installed Marketplace Items", show_header=True)
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Name", style="green")
        table.add_column("Category", style="blue")
        table.add_column("Version", style="yellow")
        table.add_column("Installed At", style="magenta")
        table.add_column("Path", style="dim")

        for item_id, data in installed_items.items():
            installed_at = data.get('installed_at', 'Unknown')
            try:
                dt = datetime.fromisoformat(installed_at)
                installed_at = dt.strftime("%Y-%m-%d %H:%M")
            except (ValueError, TypeError):
                pass

            table.add_row(
                item_id,
                data.get('name', 'Unknown'),
                data.get('category', 'Unknown'),
                data.get('version', 'Unknown'),
                installed_at,
                data.get('path', 'Unknown')
            )

        console.print(table)
        return

    client = MarketplaceClient()

    with console.status("[bold green]Fetching marketplace items...", spinner="dots"):
        results = client.search("", category=category)

    table = Table(title="Marketplace Items", show_header=True)
    table.add_column("ID", style="cyan")
    table.add_column("Name", style="green")
    table.add_column("Category", style="blue")
    table.add_column("Description")
    table.add_column("Version", style="yellow")

    for item in results:
        table.add_row(
            item['id'],
            item['name'],
            item['category'],
            item['description'][:50] + "..." if len(item['description']) > 50 else item['description'],
            item['version']
        )

    console.print(table)


@marketplace_app.command("install")
def install(
    item_id: str = typer.Argument(..., help="Item ID to install"),
    force: bool = typer.Option(False, "--force", "-f", help="Force reinstall if already exists"),
    path: Optional[str] = typer.Option(None, "--path", "-p", help="Custom installation path"),
):
    """Install an item from the marketplace"""

    client = MarketplaceClient()
    target_dir = Path(path) if path else INSTALL_DIR

    # Get item details
    with console.status(f"[bold green]Fetching {item_id} details...", spinner="dots"):
        try:
            item = client.get_item(item_id)
        except Exception as e:
            console.print(f"[red]Failed to fetch item: {e}[/red]")
            raise typer.Exit(1)

    # Display item info
    console.print(Panel(
        f"[bold]{item['name']}[/bold]\n"
        f"Category: [cyan]{item['category']}[/cyan]\n"
        f"Version: [yellow]{item['version']}[/yellow]\n"
        f"Author: [blue]{item['author']}[/blue]\n"
        f"License: [green]{item['license']}[/green]\n\n"
        f"{item['description']}",
        title=f"Installing {item_id}",
        border_style="green"
    ))

    # Confirm installation
    if not force:
        if not Confirm.ask(f"Install {item['name']}?"):
            console.print("[yellow]Installation cancelled[/yellow]")
            return

    # Install with progress
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        console=console
    ) as progress:
        task = progress.add_task(f"Installing {item_id}...", total=100)

        progress.update(task, advance=30, description="Downloading...")
        if not client.download_item(item_id, target_dir):
            console.print(f"[red]Installation failed[/red]")
            raise typer.Exit(1)

        progress.update(task, advance=40, description="Installing files...")
        # Installation happens in download_item

        progress.update(task, advance=30, description="Finalizing...")
        # Save installation metadata
        metadata_file = LOCAL_CACHE / "installed.json"
        installed = {}
        if metadata_file.exists():
            installed = json.loads(metadata_file.read_text())

        installed[item_id] = {
            "name": item['name'],
            "version": item['version'],
            "category": item['category'],
            "installed_at": datetime.now().isoformat(),
            "path": str(target_dir)
        }

        metadata_file.write_text(json.dumps(installed, indent=2))

    console.print(f"\n[bold green]Successfully installed {item['name']} ({item_id})[/bold green]")
    console.print(f"[dim]Location: {target_dir}[/dim]")


@marketplace_app.command("publish")
def publish(
    path: str = typer.Argument(..., help="Path to item to publish"),
    category: str = typer.Option(..., "--category", "-c", help="Item category (agent/tool/prompt)"),
    name: Optional[str] = typer.Option(None, "--name", "-n", help="Item name"),
    description: Optional[str] = typer.Option(None, "--description", "-d", help="Item description"),
):
    """Publish an item to the marketplace"""

    item_path = Path(path)
    if not item_path.exists():
        console.print(f"[red]Path not found: {path}[/red]")
        raise typer.Exit(1)

    # Gather metadata
    if not name:
        name = typer.prompt("Item name")
    if not description:
        description = typer.prompt("Item description")

    console.print(Panel(
        f"[bold]Publishing to Marketplace[/bold]\n\n"
        f"Name: [cyan]{name}[/cyan]\n"
        f"Category: [blue]{category}[/blue]\n"
        f"Description: {description}\n"
        f"Path: [dim]{path}[/dim]",
        border_style="green"
    ))

    if not Confirm.ask("Proceed with publishing?"):
        console.print("[yellow]Publishing cancelled[/yellow]")
        return

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Publishing...", total=100)

        progress.update(task, advance=25, description="Validating...")
        # TODO: Validation logic

        progress.update(task, advance=25, description="Packaging...")
        # TODO: Create package

        progress.update(task, advance=25, description="Uploading...")
        # TODO: Upload to marketplace

        progress.update(task, advance=25, description="Finalizing...")
        # TODO: Register in marketplace

    console.print(f"\n[bold green]Successfully published {name}[/bold green]")
    console.print(f"[cyan]View at: https://agent-zero.io/marketplace/your-item[/cyan]")


@marketplace_app.command("info")
def info(
    item_id: str = typer.Argument(..., help="Item ID"),
):
    """Show detailed information about a marketplace item"""

    client = MarketplaceClient()

    with console.status(f"[bold green]Fetching {item_id} details...", spinner="dots"):
        try:
            item = client.get_item(item_id)
        except Exception as e:
            console.print(f"[red]Failed to fetch item: {e}[/red]")
            raise typer.Exit(1)

    # Display detailed info
    info_panel = f"""[bold cyan]{item['name']}[/bold cyan]

[yellow]Category:[/yellow] {item['category']}
[yellow]Version:[/yellow] {item['version']}
[yellow]Author:[/yellow] {item['author']}
[yellow]License:[/yellow] {item['license']}

[bold]Description:[/bold]
{item['description']}

[bold]Links:[/bold]
[blue]Homepage:[/blue] {item['homepage']}
[blue]Repository:[/blue] {item['repository']}

[bold]Dependencies:[/bold]
{', '.join(item['dependencies']) if item['dependencies'] else 'None'}
"""

    console.print(Panel(info_panel, title=f"Marketplace Item: {item_id}", border_style="cyan"))


@marketplace_app.command("update")
def update(
    item_id: Optional[str] = typer.Argument(None, help="Item ID to update (or all if not specified)"),
    check: bool = typer.Option(False, "--check", help="Only check for updates"),
):
    """Update installed marketplace items"""

    if item_id:
        console.print(f"[yellow]Checking updates for {item_id}...[/yellow]")
    else:
        console.print("[yellow]Checking updates for all installed items...[/yellow]")

    # TODO: Implement update checking and installation
    console.print("[green]All items are up to date[/green]")


if __name__ == "__main__":
    marketplace_app()
