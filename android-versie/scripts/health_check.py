#!/usr/bin/env python3
"""
Agent Zero Android - Health Check & Diagnostics Tool
Versie: 1.0 - November 29, 2025

Dit script checkt of alle componenten correct zijn geïnstalleerd en geconfigureerd.
"""

import sys
import os
import subprocess

# Colors for terminal output
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(text):
    print(f"\n{Colors.BLUE}{Colors.BOLD}{'='*60}{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}{text:^60}{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}{'='*60}{Colors.END}\n")

def print_check(name, status, detail=""):
    symbol = f"{Colors.GREEN}✓{Colors.END}" if status else f"{Colors.RED}✗{Colors.END}"
    print(f"{symbol} {name:40} ", end="")
    if detail:
        print(f"{Colors.YELLOW}{detail}{Colors.END}")
    else:
        print()

def check_python():
    """Check Python version"""
    version = sys.version_info
    required = (3, 11)
    status = version >= required
    detail = f"v{version.major}.{version.minor}.{version.micro}"
    if not status:
        detail += f" (need ≥{required[0]}.{required[1]})"
    return status, detail

def check_package(package_name):
    """Check if Python package is installed"""
    try:
        __import__(package_name.replace('-', '_'))
        return True, "installed"
    except ImportError:
        return False, "missing"

def check_file(filepath):
    """Check if file exists"""
    exists = os.path.exists(filepath)
    return exists, "found" if exists else "missing"

def check_env_var(var_name):
    """Check if environment variable is set"""
    value = os.getenv(var_name)
    if value:
        # Mask API keys
        if len(value) > 8:
            masked = value[:4] + "..." + value[-4:]
        else:
            masked = "***"
        return True, masked
    return False, "not set"

def run_health_check():
    """Run complete health check"""

    print_header("🏥 Agent Zero Android - Health Check")

    # === System Check ===
    print(f"\n{Colors.BOLD}📱 System:{Colors.END}")

    status, detail = check_python()
    print_check("Python Version", status, detail)

    # Check platform
    import platform
    is_termux = "TERMUX_VERSION" in os.environ or "com.termux" in os.getcwd()
    print_check("Termux Environment", is_termux,
                "detected" if is_termux else "not detected")

    # === Core Packages ===
    print(f"\n{Colors.BOLD}📦 Core Packages:{Colors.END}")

    core_packages = [
        "langchain",
        "langchain_core",
        "langchain_anthropic",
        "langchain_openai",
        "langchain_google_genai",
        "anthropic",
        "openai",
        "google.generativeai",
    ]

    all_core_ok = True
    for pkg in core_packages:
        status, detail = check_package(pkg)
        print_check(pkg, status, detail)
        if not status:
            all_core_ok = False

    # === Utility Packages ===
    print(f"\n{Colors.BOLD}🛠️  Utility Packages:{Colors.END}")

    util_packages = [
        "dotenv",
        "flask",
        "beautifulsoup4",
        "paramiko",
        "ansio",
    ]

    all_util_ok = True
    for pkg in util_packages:
        status, detail = check_package(pkg)
        print_check(pkg, status, detail)
        if not status:
            all_util_ok = False

    # === Files Check ===
    print(f"\n{Colors.BOLD}📁 Configuration Files:{Colors.END}")

    base_dir = os.path.join(os.path.dirname(__file__), '../..')

    files_to_check = [
        ('android-versie/config/initialize_android.py', 'Config'),
        ('android-versie/config/.env', 'Environment'),
        ('android-versie/run_android_cli.py', 'CLI Launcher'),
        ('agent.py', 'Agent Core'),
        ('models.py', 'Models'),
    ]

    all_files_ok = True
    for filepath, name in files_to_check:
        full_path = os.path.join(base_dir, filepath)
        status, detail = check_file(full_path)
        print_check(name, status, detail)
        if not status:
            all_files_ok = False

    # === API Keys Check ===
    print(f"\n{Colors.BOLD}🔑 API Keys:{Colors.END}")

    # Load .env file
    env_path = os.path.join(base_dir, 'android-versie/config/.env')
    if os.path.exists(env_path):
        from dotenv import load_dotenv
        load_dotenv(env_path)

    api_keys = [
        'GOOGLE_API_KEY',
        'OPENAI_API_KEY',
        'ANTHROPIC_API_KEY',
        'GROQ_API_KEY',
    ]

    keys_found = 0
    for key in api_keys:
        status, detail = check_env_var(key)
        print_check(key, status, detail)
        if status:
            keys_found += 1

    # === Agent Zero Test ===
    print(f"\n{Colors.BOLD}🤖 Agent Zero Components:{Colors.END}")

    # Test imports
    try:
        sys.path.insert(0, os.path.join(base_dir, 'android-versie/config'))
        from initialize_android import initialize
        print_check("Initialize Module", True, "loadable")

        try:
            config = initialize()
            print_check("Configuration Load", True, "success")
        except Exception as e:
            print_check("Configuration Load", False, str(e)[:40])

    except Exception as e:
        print_check("Initialize Module", False, str(e)[:40])

    try:
        sys.path.insert(0, base_dir)
        from agent import AgentContext
        print_check("Agent Module", True, "loadable")
    except Exception as e:
        print_check("Agent Module", False, str(e)[:40])

    # === Summary ===
    print(f"\n{Colors.BOLD}📊 Summary:{Colors.END}\n")

    issues = []

    if not all_core_ok:
        issues.append("Missing core packages")
    if not all_util_ok:
        issues.append("Missing utility packages")
    if not all_files_ok:
        issues.append("Missing configuration files")
    if keys_found == 0:
        issues.append("No API keys configured")

    if not issues:
        print(f"{Colors.GREEN}{Colors.BOLD}✅ All checks passed! Agent Zero is ready to use.{Colors.END}\n")
        print(f"Start with: {Colors.BLUE}bash android-versie/agent0_wrapper.sh{Colors.END}\n")
        return 0
    else:
        print(f"{Colors.YELLOW}{Colors.BOLD}⚠️  Issues found:{Colors.END}\n")
        for issue in issues:
            print(f"  • {issue}")
        print()

        # Provide fixes
        print(f"{Colors.BOLD}🔧 Quick Fixes:{Colors.END}\n")

        if not all_core_ok or not all_util_ok:
            print(f"  Install missing packages:")
            print(f"  {Colors.BLUE}pip install -r android-versie/requirements-android.txt{Colors.END}\n")

        if keys_found == 0:
            print(f"  Configure API keys:")
            print(f"  {Colors.BLUE}nano android-versie/config/.env{Colors.END}")
            print(f"  Add at least one: GOOGLE_API_KEY, OPENAI_API_KEY, or ANTHROPIC_API_KEY\n")

        return 1

if __name__ == "__main__":
    try:
        exit_code = run_health_check()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Interrupted by user.{Colors.END}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.RED}Error: {e}{Colors.END}")
        sys.exit(1)
