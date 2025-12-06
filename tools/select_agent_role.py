#!/usr/bin/env python3
"""
Interactive Sub-Agent Role Selector
Helpt gebruikers de juiste agent te kiezen voor hun taak
"""

import sys
import os
from pathlib import Path

# Inline definitions (agent_config.py might not be in Python path)
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

def get_role_for_task(task_description: str) -> str:
    """Suggereert een rol op basis van de task beschrijving."""
    task_lower = task_description.lower()

    keywords = {
        "coder": ["code", "python", "script", "nodejs", "terminal", "execute", "run", "implement", "schrijf"],
        "researcher": ["search", "find", "research", "documentation", "how to", "what is", "explain", "zoek"],
        "memory": ["remember", "save", "recall", "memory", "store", "retrieve", "forget", "onthoud"],
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

    scores = {role: 0 for role in keywords.keys()}
    for role, words in keywords.items():
        for word in words:
            if word in task_lower:
                scores[role] += 1

    best_role = max(scores.items(), key=lambda x: x[1])

    if best_role[1] == 0:
        return "master"

    return best_role[0]

def print_header():
    """Print fancy header"""
    print()
    print("=" * 70)
    print("🤖  SUB-AGENT ROLE SELECTOR")
    print("    Agent Zero v3.0 - Interactive Role Selection")
    print("=" * 70)
    print()

def get_task_input():
    """Get task description from user"""
    print("Beschrijf je taak (in het Nederlands of Engels):")
    print("Voorbeelden:")
    print("  - Write Python code to analyze CSV data")
    print("  - Zoek informatie over beste PDF libraries voor Termux")
    print("  - Scrape product prices from website")
    print()
    task = input("Taak: ").strip()

    if not task:
        print("\n❌ Geen taak opgegeven. Afsluiten.")
        sys.exit(1)

    return task

def display_suggestion(task, suggested_role):
    """Display AI suggestion"""
    print()
    print("─" * 70)
    print(f"💡 AANBEVELING (gebaseerd op AI-analyse)")
    print("─" * 70)
    print(f"   Rol: {suggested_role}")
    print(f"   └─ {ROLE_DESCRIPTIONS[suggested_role]}")
    print()

def display_all_roles(suggested_role):
    """Display all available roles"""
    print("📋 ALLE BESCHIKBARE ROLLEN:")
    print()

    roles_list = list(ROLE_DESCRIPTIONS.items())

    for i, (key, desc) in enumerate(roles_list, 1):
        marker = "→" if key == suggested_role else " "
        print(f"{marker} {i:2}. {key:15} - {desc}")

    print()

def get_role_choice(suggested_role, roles_list):
    """Get user's role selection"""
    print("Kies een rol:")
    print("  - Druk ENTER voor aanbevolen rol")
    print("  - Of typ nummer (1-{})".format(len(roles_list)))
    print()

    choice = input("Keuze: ").strip()

    if not choice:
        return suggested_role

    try:
        idx = int(choice) - 1
        if 0 <= idx < len(roles_list):
            return roles_list[idx][0]
        else:
            print(f"\n⚠️  Ongeldige keuze ({choice}). Gebruik aanbevolen rol.")
            return suggested_role
    except ValueError:
        print(f"\n⚠️  Ongeldige invoer. Gebruik aanbevolen rol.")
        return suggested_role

def generate_delegation_json(role, task):
    """Generate the call_subordinate JSON"""
    role_desc = ROLE_DESCRIPTIONS[role]

    json_template = f'''{{
    "thoughts": [
        "I need {role_desc} expertise for this task",
        "Delegating to specialized agent with focused context"
    ],
    "tool_name": "call_subordinate",
    "tool_args": {{
        "message": "You are a {role_desc}.

CONTEXT:
[Geef hier relevante achtergrond informatie]

TASK: {task}

REQUIREMENTS:
[Specificeer requirements, constraints, te vermijden dingen]

EXPECTED OUTPUT:
[Beschrijf wat je terug wilt hebben]

[Extra instructies indien nodig]",
        "reset": "true"
    }}
}}'''

    return json_template

def display_result(role, json_template):
    """Display final result"""
    print()
    print("=" * 70)
    print(f"🎯 GESELECTEERDE ROL: {role}")
    print("=" * 70)
    print(f"   {ROLE_DESCRIPTIONS[role]}")
    print()
    print("─" * 70)
    print("📋 COPY DEZE JSON VOOR call_subordinate:")
    print("─" * 70)
    print()
    print(json_template)
    print()

def copy_to_clipboard(text):
    """Try to copy to Android clipboard"""
    try:
        import subprocess
        result = subprocess.run(
            ["termux-clipboard-set"],
            input=text,
            text=True,
            capture_output=True,
            timeout=2
        )
        if result.returncode == 0:
            print("✅ Gekopieerd naar klembord!")
            return True
        else:
            return False
    except Exception:
        return False

def show_usage_tips(role):
    """Show tips for using this role"""
    print()
    print("─" * 70)
    print("💡 TIPS VOOR HET GEBRUIKEN VAN DEZE ROL:")
    print("─" * 70)

    tips = {
        "coder": [
            "• Geef specifieke requirements (taal, libraries, input/output)",
            "• Vermeld file paths expliciet (bijv. /sdcard/data.csv)",
            "• Vraag om error handling en testing",
            "• Op Android: vermeld Termux-compatibiliteit indien relevant"
        ],
        "researcher": [
            "• Wees specifiek over wat je wilt weten",
            "• Geef criteria voor resultaten (bijv. ARM-compatible, recent, etc.)",
            "• Vraag om vergelijking tussen opties",
            "• Specificeer output format (lijst, tabel, samenvatting)"
        ],
        "memory": [
            "• Gebruik duidelijke tags voor later terugvinden",
            "• Geef importance score (1-10)",
            "• Voeg context toe (project name, categorie)",
            "• Schrijf goede summaries voor quick scanning"
        ],
        "scraper": [
            "• Geef exacte URL",
            "• Specificeer welke data je wilt extracten",
            "• Vraag om output format (JSON, CSV, etc.)",
            "• Vermeld error handling voor unavailable pages"
        ],
        "orchestrator": [
            "• Beschrijf het grote plaatje / end goal",
            "• Laat de orchestrator subtaken identificeren",
            "• Geef constraints (tijd, resources, etc.)",
            "• Vraag om coördinatie van andere specialists"
        ],
        "architect": [
            "• Beschrijf probleem/challenge volledig",
            "• Geef requirements en constraints",
            "• Vraag om meerdere opties met trade-offs",
            "• Specificeer technologie preferences indien relevant"
        ],
        "master": [
            "• Geef complete project overview",
            "• Beschrijf alle requirements",
            "• Laat master de task breakdown maken",
            "• Vraag om delegatie strategie"
        ]
    }

    # Get tips for this role, fallback to general tips
    role_tips = tips.get(role, [
        "• Geef volledige context in CONTEXT sectie",
        "• Specificeer duidelijke stappen in TASK sectie",
        "• Voeg constraints toe (beperkingen, requirements)",
        "• Beschrijf verwachte output in EXPECTED OUTPUT sectie"
    ])

    for tip in role_tips:
        print(f"   {tip}")

    print()

def show_quick_reference():
    """Show quick reference for common patterns"""
    print("─" * 70)
    print("📖 QUICK REFERENCE - Veel gebruikte patronen:")
    print("─" * 70)
    print()
    print("1. SEQUENTIËLE DELEGATIE (Research → Code → Memory)")
    print("   • Eerst researcher voor info")
    print("   • Dan coder voor implementatie")
    print("   • Tot slot memory om op te slaan")
    print()
    print("2. ANDROID INTEGRATIE")
    print("   • Vermeld in TASK: 'Send notification on completion'")
    print("   • Gebruik android_features, voice_interface tools")
    print("   • Check battery level voor intensive operations")
    print()
    print("3. ERROR RECOVERY")
    print("   • Geef in CONTEXT aan wat eerder fout ging")
    print("   • Vraag om alternative approach")
    print("   • Specificeer fallback opties")
    print()
    print("Voor meer info: /data/data/com.termux/files/home/AI-EcoSystem/docs/SUB_AGENT_MASTERY.md")
    print()

def main():
    """Main function"""
    print_header()

    # Get task from user
    task = get_task_input()

    # Get AI suggestion
    suggested_role = get_role_for_task(task)

    # Display suggestion
    display_suggestion(task, suggested_role)

    # Display all roles
    roles_list = list(ROLE_DESCRIPTIONS.items())
    display_all_roles(suggested_role)

    # Get user choice
    final_role = get_role_choice(suggested_role, roles_list)

    # Generate JSON
    delegation_json = generate_delegation_json(final_role, task)

    # Display result
    display_result(final_role, delegation_json)

    # Try to copy to clipboard
    copied = copy_to_clipboard(delegation_json)
    if not copied:
        print("ℹ️  Kon niet kopiëren naar klembord (niet op Termux)")

    # Show usage tips
    show_usage_tips(final_role)

    # Show quick reference
    show_quick_reference()

    print("=" * 70)
    print("✨ Klaar! Gebruik de JSON hierboven in je Agent Zero conversatie")
    print("=" * 70)
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Afgebroken door gebruiker")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
