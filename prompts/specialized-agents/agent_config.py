"""
Specialized Agents Configuration
=================================

Dit script helpt bij het laden van de juiste rol-prompts voor specialized agents.
"""

import os
from pathlib import Path

# Beschikbare agent rollen
AGENT_ROLES = {
    "master": "role.master_orchestrator.md",
    "coder": "role.code_specialist.md",
    "researcher": "role.knowledge_researcher.md",
    "memory": "role.memory_manager.md",
    "scraper": "role.web_scraper.md",
    "orchestrator": "role.task_orchestrator.md",
    "architect": "role.solution_architect.md",
    "prime": "role.prime_orchestrator.md",
    "nexus": "role.nexus_architect.md",
    "quantum": "role.quantum_trader.md",
    "core": "role.system_core.md",
    "synapse": "role.content_synapse.md",
    "innovator": "role.innovation_agent.md",
    "synergy": "role.synergy_agent.md",
    "optimizer": "role.optimization_agent.md",
}

# Rol beschrijvingen voor selectie
ROLE_DESCRIPTIONS = {
    "master": "Master Orchestrator - Hoofdcoördinator voor task analysis en delegatie",
    "coder": "Code Specialist - Python/NodeJS/Terminal execution expert",
    "researcher": "Knowledge Researcher - Online search en information retrieval",
    "memory": "Memory Manager - Long-term geheugen beheer specialist",
    "scraper": "Web Scraper - Webpage content extraction expert",
    "orchestrator": "Task Orchestrator - Subtask delegatie coördinator",
    "architect": "Solution Architect - Complexe probleem-oplossing strategist",
    "prime": "Prime Orchestrator - Centrale projectleider en strategist",
    "nexus": "Nexus Architect - Full-stack & Cloud API specialist",
    "quantum": "Quantum Trader - Solana & DeFi trading specialist",
    "core": "System Core - Android Termux DevOps engineer",
    "synapse": "Content Synapse - Web content & Creative researcher",
    "innovator": "Innovator - Visionair voor nieuwe ideeën",
    "synergy": "Synergy Agent - Cross-project code hergebruik specialist",
    "optimizer": "Optimizer - Performance & Efficiency engineer",
}

def get_role_prompt_path(role_key: str) -> Path:
    """
    Geeft het pad naar het role prompt bestand.

    Args:
        role_key: Een van de keys in AGENT_ROLES

    Returns:
        Path object naar het prompt bestand

    Raises:
        ValueError: Als role_key niet bestaat
    """
    if role_key not in AGENT_ROLES:
        raise ValueError(
            f"Onbekende rol '{role_key}'. "
            f"Beschikbare rollen: {', '.join(AGENT_ROLES.keys())}"
        )

    prompts_dir = Path(__file__).parent
    return prompts_dir / AGENT_ROLES[role_key]

def load_role_prompt(role_key: str) -> str:
    """
    Laadt de role prompt content.

    Args:
        role_key: Een van de keys in AGENT_ROLES

    Returns:
        String met de prompt content
    """
    prompt_path = get_role_prompt_path(role_key)

    if not prompt_path.exists():
        raise FileNotFoundError(f"Prompt bestand niet gevonden: {prompt_path}")

    with open(prompt_path, 'r', encoding='utf-8') as f:
        return f.read()

def get_role_for_task(task_description: str) -> str:
    """
    Suggereert een rol op basis van de task beschrijving.

    Args:
        task_description: Beschrijving van de taak

    Returns:
        Rol key die het beste past
    """
    task_lower = task_description.lower()

    # Keyword mapping naar rollen
    keywords = {
        "coder": ["code", "python", "script", "nodejs", "terminal", "execute", "run", "implement"],
        "researcher": ["search", "find", "research", "documentation", "how to", "what is", "explain"],
        "memory": ["remember", "save", "recall", "memory", "store", "retrieve", "forget"],
        "scraper": ["scrape", "webpage", "website", "extract", "url", "html", "web content"],
        "orchestrator": ["delegate", "coordinate", "subtask", "split", "organize", "manage tasks"],
        "architect": ["design", "architecture", "strategy", "plan", "complex", "solution", "approach"],
        "prime": ["manage", "lead", "project", "strategy", "oversee", "prime", "boss"],
        "nexus": ["api", "backend", "frontend", "dashboard", "docker", "cloud", "server"],
        "quantum": ["trade", "crypto", "solana", "blockchain", "token", "bot", "financial"],
        "core": ["android", "termux", "os", "system", "devops", "shell", "bash"],
        "synapse": ["content", "blog", "write", "creative", "seo", "article"],
        "innovator": ["idea", "innovate", "new feature", "dream", "vision", "future"],
        "synergy": ["reuse", "shared", "dependency", "cross-project", "duplicate", "common"],
        "optimizer": ["optimize", "fast", "speed", "efficient", "performance", "cost", "token"],
    }

    # Score elke rol
    scores = {role: 0 for role in keywords.keys()}
    for role, words in keywords.items():
        for word in words:
            if word in task_lower:
                scores[role] += 1

    # Vind de hoogste score
    best_role = max(scores.items(), key=lambda x: x[1])

    # Als geen keywords gevonden, gebruik master
    if best_role[1] == 0:
        return "master"

    return best_role[0]

def list_available_roles():
    """Print alle beschikbare rollen met beschrijvingen."""
    print("Beschikbare Specialized Agent Rollen:")
    print("=" * 70)
    for key, description in ROLE_DESCRIPTIONS.items():
        print(f"  {key:15} - {description}")
    print("=" * 70)

# Voorbeeld gebruik
if __name__ == "__main__":
    print("Specialized Agents Configuration\n")

    # Toon alle beschikbare rollen
    list_available_roles()

    # Voorbeeld: laad een specifieke rol
    print("\nVoorbeeld: Laden van Code Specialist rol")
    print("-" * 70)
    try:
        code_prompt = load_role_prompt("coder")
        print(f"Prompt geladen: {len(code_prompt)} karakters")
        print(f"\nEerste 200 karakters:")
        print(code_prompt[:200] + "...")
    except Exception as e:
        print(f"Error: {e}")

    # Voorbeeld: auto-detectie van rol
    print("\n\nVoorbeeld: Auto-detectie van rol op basis van taak")
    print("-" * 70)
    test_tasks = [
        "Write Python code to read a CSV file",
        "Search for the best web scraping library",
        "Remember this solution for later",
        "Extract data from this website",
    ]

    for task in test_tasks:
        suggested_role = get_role_for_task(task)
        print(f"Task: {task}")
        print(f"  → Suggested role: {suggested_role} ({ROLE_DESCRIPTIONS[suggested_role]})")
        print()
