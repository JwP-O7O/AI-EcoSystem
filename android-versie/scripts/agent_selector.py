#!/usr/bin/env python3
"""
Agent Zero - Specialized Agent Selector
Versie: 1.0 - November 29, 2025

Interactieve tool om de juiste specialized agent te selecteren voor je taak.
"""

import sys
import os

# Colors
class C:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    BOLD = '\033[1m'
    END = '\033[0m'

# Agent definitions met details
AGENTS = {
    '1': {
        'name': 'Master Orchestrator',
        'icon': '🎯',
        'color': C.MAGENTA,
        'role': 'Master Orchestrator',
        'description': 'Coördineert complexe multi-step workflows, delegeert naar andere agents',
        'use_cases': [
            'Complexe projecten met meerdere stappen',
            'Wanneer je niet zeker weet welke agent te gebruiken',
            'End-to-end project uitvoering',
            'Research + Design + Implementation workflows'
        ],
        'prompt_prefix': 'You are a Master Orchestrator. Your role is to coordinate complex tasks by delegating to specialized agents.'
    },
    '2': {
        'name': 'Code Specialist',
        'icon': '💻',
        'color': C.GREEN,
        'role': 'Code Execution Specialist',
        'description': 'Expert in Python, JavaScript, Bash scripting en code execution',
        'use_cases': [
            'Python/JavaScript code schrijven',
            'Scripts uitvoeren en debuggen',
            'File operations en data processing',
            'Terminal commando\'s uitvoeren'
        ],
        'prompt_prefix': 'You are a Code Execution Specialist. You excel at writing and executing code in Python, JavaScript, and Bash.'
    },
    '3': {
        'name': 'Research Specialist',
        'icon': '🔍',
        'color': C.CYAN,
        'role': 'Knowledge Research Specialist',
        'description': 'Online research, informatie verzamelen, DuckDuckGo searches',
        'use_cases': [
            'Online research doen',
            'Actuele informatie opzoeken',
            'Documentatie vinden',
            'Best practices onderzoeken'
        ],
        'prompt_prefix': 'You are a Knowledge Research Specialist. You excel at finding and synthesizing information from online sources.'
    },
    '4': {
        'name': 'Web Scraper',
        'icon': '🌐',
        'color': C.YELLOW,
        'role': 'Web Content Extraction Specialist',
        'description': 'Web scraping, HTML parsing, data extractie van websites',
        'use_cases': [
            'Data extractie van websites',
            'Web scraping opdrachten',
            'HTML/CSS parsing',
            'Content aggregatie'
        ],
        'prompt_prefix': 'You are a Web Content Extraction Specialist. You excel at extracting and processing data from websites.'
    },
    '5': {
        'name': 'Solution Architect',
        'icon': '🏗️',
        'color': C.BLUE,
        'role': 'Solution Architecture Specialist',
        'description': 'Systeemontwerp, architectuur, technische planning',
        'use_cases': [
            'Architectuur ontwerpen',
            'Technische beslissingen',
            'System design',
            'Long-term planning'
        ],
        'prompt_prefix': 'You are a Solution Architecture Specialist. You excel at designing robust, scalable system architectures.'
    },
    '6': {
        'name': 'Memory Manager',
        'icon': '🧠',
        'color': C.MAGENTA,
        'role': 'Memory Manager',
        'description': 'Kennisbeheer, memories opslaan en ophalen',
        'use_cases': [
            'Informatie opslaan voor later',
            'Knowledge base beheren',
            'Context bewaren tussen sessies',
            'Belangrijke insights onthouden'
        ],
        'prompt_prefix': 'You are a Memory Manager. You excel at organizing and retrieving knowledge from long-term storage.'
    },
    '7': {
        'name': 'Task Orchestrator',
        'icon': '📋',
        'color': C.CYAN,
        'role': 'Task Delegation Orchestrator',
        'description': 'Taken verdelen over meerdere agents, workflow management',
        'use_cases': [
            'Parallelle taken uitvoeren',
            'Workflow coördinatie',
            'Team van agents aansturen',
            'Complexe delegatie'
        ],
        'prompt_prefix': 'You are a Task Delegation Orchestrator. You excel at breaking down complex tasks and delegating them efficiently.'
    }
}

def print_header():
    print(f"\n{C.BOLD}{C.BLUE}{'='*70}{C.END}")
    print(f"{C.BOLD}{C.BLUE}{'🤖 Agent Zero - Specialized Agent Selector':^70}{C.END}")
    print(f"{C.BOLD}{C.BLUE}{'='*70}{C.END}\n")

def print_agent_list():
    print(f"{C.BOLD}Beschikbare Agents:{C.END}\n")

    for key, agent in AGENTS.items():
        color = agent['color']
        icon = agent['icon']
        name = agent['name']
        desc = agent['description']

        print(f"  {color}{C.BOLD}[{key}]{C.END} {icon} {C.BOLD}{name}{C.END}")
        print(f"      {desc}\n")

    print(f"  {C.YELLOW}{C.BOLD}[0]{C.END} ❌ {C.BOLD}Exit{C.END}\n")

def print_agent_details(agent):
    color = agent['color']
    icon = agent['icon']

    print(f"\n{color}{C.BOLD}{'─'*70}{C.END}")
    print(f"{color}{C.BOLD}{icon} {agent['name']}{C.END}")
    print(f"{color}{C.BOLD}{'─'*70}{C.END}\n")

    print(f"{C.BOLD}Beschrijving:{C.END}")
    print(f"  {agent['description']}\n")

    print(f"{C.BOLD}Gebruik voor:{C.END}")
    for use_case in agent['use_cases']:
        print(f"  • {use_case}")
    print()

    print(f"{C.BOLD}Agent Prompt Prefix:{C.END}")
    print(f"{C.CYAN}  {agent['prompt_prefix']}{C.END}\n")

def get_task_description():
    print(f"{C.BOLD}Beschrijf je taak:{C.END}")
    print(f"{C.YELLOW}(Typ je opdracht, of druk Enter voor algemene instructies){C.END}\n")

    task = input(f"{C.BOLD}→{C.END} ").strip()
    return task

def generate_full_prompt(agent, task):
    """Generate complete prompt for Agent Zero"""
    prompt = f"{agent['prompt_prefix']}\n\n"

    if task:
        prompt += f"Task: {task}"
    else:
        prompt += "Awaiting your instructions."

    return prompt

def copy_to_clipboard(text):
    """Try to copy text to clipboard (Termux-specific)"""
    try:
        import subprocess
        # Termux heeft termux-clipboard-set
        subprocess.run(['termux-clipboard-set'], input=text.encode(), check=True)
        return True
    except:
        return False

def main():
    print_header()

    while True:
        print_agent_list()

        choice = input(f"{C.BOLD}Selecteer een agent [0-7]:{C.END} ").strip()

        if choice == '0':
            print(f"\n{C.YELLOW}👋 Goodbye!{C.END}\n")
            break

        if choice not in AGENTS:
            print(f"\n{C.RED}❌ Ongeldige keuze. Probeer opnieuw.{C.END}\n")
            continue

        agent = AGENTS[choice]

        # Show agent details
        print_agent_details(agent)

        # Get task description
        task = get_task_description()

        # Generate full prompt
        full_prompt = generate_full_prompt(agent, task)

        # Display result
        print(f"\n{C.GREEN}{C.BOLD}{'─'*70}{C.END}")
        print(f"{C.GREEN}{C.BOLD}✓ Prompt gegenereerd!{C.END}")
        print(f"{C.GREEN}{C.BOLD}{'─'*70}{C.END}\n")

        print(f"{C.BOLD}Kopieer en plak dit in Agent Zero:{C.END}\n")
        print(f"{C.CYAN}{full_prompt}{C.END}\n")

        # Try to copy to clipboard
        if copy_to_clipboard(full_prompt):
            print(f"{C.GREEN}📋 Prompt gekopieerd naar clipboard!{C.END}\n")

        print(f"{C.BOLD}Opties:{C.END}")
        print(f"  {C.YELLOW}[n]{C.END} Nieuwe agent selecteren")
        print(f"  {C.YELLOW}[a]{C.END} Start Agent Zero nu")
        print(f"  {C.YELLOW}[q]{C.END} Quit\n")

        action = input(f"{C.BOLD}→{C.END} ").strip().lower()

        if action == 'q':
            print(f"\n{C.YELLOW}👋 Goodbye!{C.END}\n")
            break
        elif action == 'a':
            print(f"\n{C.GREEN}🚀 Starting Agent Zero...{C.END}\n")
            print(f"{C.YELLOW}TIP: Plak de prompt in het chat venster!{C.END}\n")

            # Start Agent Zero
            base_dir = os.path.join(os.path.dirname(__file__), '../..')
            launcher = os.path.join(base_dir, 'android-versie/agent0_wrapper.sh')

            os.system(f'bash {launcher}')
            break
        else:
            # Continue loop for new selection
            print()
            continue

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{C.YELLOW}Interrupted by user.{C.END}\n")
        sys.exit(0)
