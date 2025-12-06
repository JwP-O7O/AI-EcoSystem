#!/usr/bin/env python3
"""
Agent Zero - Android/Termux CLI Launcher
Versie: 1.0 - November 26, 2025

Dit script start Agent Zero in CLI mode, geoptimaliseerd voor Android/Termux.
"""

import asyncio
import sys
import os
import threading
import time

# Add parent directory and config directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'config'))

from agent import AgentContext
from python.helpers.print_style import PrintStyle
from python.helpers.files import read_file
from python.helpers import files
import python.helpers.timed_input as timed_input

# Import Android-specific configuration
from initialize_android import initialize

context: AgentContext = None  # type: ignore
input_lock = threading.Lock()


# Main conversation loop
async def chat(context: AgentContext):
    """Main chat loop for Agent Zero"""

    # Get working directory from agent data
    work_dir = context.agent0.get_data("work_dir") or os.getcwd()

    # Welcome message - meer compact en overzichtelijk
    print("\n" + "─" * 60)
    PrintStyle(font_color="green", bold=True).print("🤖 Agent Zero Ready")
    print("─" * 60)
    PrintStyle(font_color="cyan").print(f"📂 {work_dir}")
    PrintStyle(font_color="yellow").print("💡 Type 'e' to exit")
    print("─" * 60 + "\n")

    # Start the conversation loop
    while True:
        # Ask user for message
        with input_lock:
            timeout = context.agent0.get_data("timeout")

            if not timeout:
                # Compacte user prompt
                PrintStyle(font_color="blue", bold=True).print("You:")

                if sys.platform != "win32":
                    import readline  # Arrow keys fix

                user_input = input("→ ")
                PrintStyle(font_color="white", padding=False, log_only=True).print(f"→ {user_input}")

            else:
                PrintStyle(
                    background_color="#6C3483",
                    font_color="white",
                    bold=True,
                    padding=True
                ).print(f"User message ({timeout}s timeout, 'w' to wait, 'e' to leave):")

                if sys.platform != "win32":
                    import readline

                user_input = timeout_input("> ", timeout=timeout)

                if not user_input:
                    user_input = context.agent0.read_prompt("fw.msg_timeout.md")
                    PrintStyle(font_color="white", padding=False).stream(f"{user_input}")
                else:
                    user_input = user_input.strip()
                    if user_input.lower() == "w":
                        user_input = input("> ").strip()
                    PrintStyle(font_color="white", padding=False, log_only=True).print(f"> {user_input}")

        # Exit check
        if user_input.lower() == 'e':
            print("\n" + "─" * 60)
            PrintStyle(font_color="yellow", bold=True).print("👋 Goodbye!")
            print("─" * 60 + "\n")
            break

        # Visual separator before agent response
        print()  # Extra line for clarity

        # Send message to agent
        try:
            assistant_response = await context.communicate(user_input).result()

            # Print response
            PrintStyle(
                font_color="white",
                background_color="#1D8348",
                bold=True,
                padding=True
            ).print(f"{context.agent0.agent_name}: response:")
            PrintStyle(font_color="white").print(f"{assistant_response}")

        except Exception as e:
            PrintStyle(font_color="red", bold=True).print(f"\n❌ Error: {str(e)}")
            PrintStyle(font_color="yellow").print("Continuing... (type 'e' to exit)")


def intervention():
    """User intervention during agent streaming"""
    if context.streaming_agent and not context.paused:
        context.paused = True
        PrintStyle(
            background_color="#6C3483",
            font_color="white",
            bold=True,
            padding=True
        ).print("User intervention ('e' to leave, empty to continue):")

        if sys.platform != "win32":
            import readline

        user_input = input("> ").strip()
        PrintStyle(font_color="white", padding=False, log_only=True).print(f"> {user_input}")

        if user_input.lower() == 'e':
            os._exit(0)
        if user_input:
            context.streaming_agent.intervention_message = user_input

        context.paused = False


def timeout_input(prompt, timeout=10):
    """User input with timeout"""
    return timed_input.timeout_input(prompt=prompt, timeout=timeout)


def check_environment():
    """Check if environment is properly configured"""
    errors = []

    # Check .env file
    env_path = os.path.join(
        os.path.dirname(__file__),
        'config',
        '.env'
    )
    if not os.path.exists(env_path):
        errors.append("⚠️  .env file not found in android-versie/config/")
        errors.append("   Run: cp android-versie/config/.env.example android-versie/config/.env")
        errors.append("   Then add your API keys")

    if errors:
        PrintStyle(font_color="red", bold=True).print("\n❌ Configuration Errors:\n")
        for error in errors:
            PrintStyle(font_color="yellow").print(error)
        PrintStyle(font_color="cyan").print("\nSee: android-versie/docs/QUICK_START.md for help\n")
        return False

    return True


if __name__ == "__main__":
    # Get and store the working directory
    work_dir = os.environ.get('AGENT_WORK_DIR', os.getcwd())

    # Compacte startup
    print("\n" + "═" * 60)
    print("🚀 Agent Zero Starting...")
    print("═" * 60)

    # Check environment
    if not check_environment():
        sys.exit(1)

    try:
        # Initialize with Android config (stil)
        config = initialize()

        # Create context (stil)
        context = AgentContext(config)

        # Set working directory in agent's data
        context.agent0.set_data("work_dir", work_dir)

        # Klaar bericht
        PrintStyle(font_color="green").print("✓ Ready")

        # Start chat
        asyncio.run(chat(context))

    except KeyboardInterrupt:
        PrintStyle(font_color="yellow").print("\n\n👋 Interrupted by user. Goodbye!")
        sys.exit(0)
    except Exception as e:
        PrintStyle(font_color="red", bold=True).print(f"\n❌ Fatal error: {str(e)}")
        PrintStyle(font_color="yellow").print("\nFor help, see: android-versie/docs/TROUBLESHOOTING.md")
        sys.exit(1)
