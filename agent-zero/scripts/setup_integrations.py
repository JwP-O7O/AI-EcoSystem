#!/usr/bin/env python3
"""
Integration Framework Setup Script

Interactive setup for Agent Zero integrations.
"""

import os
import sys
import json

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from python.helpers.integration_framework import IntegrationFramework


def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(text)
    print("=" * 60 + "\n")


def print_section(text):
    """Print a formatted section header"""
    print(f"\n--- {text} ---\n")


def get_input(prompt, default=None):
    """Get user input with optional default"""
    if default:
        prompt = f"{prompt} [{default}]: "
    else:
        prompt = f"{prompt}: "

    value = input(prompt).strip()
    return value if value else default


def yes_no(prompt, default=False):
    """Get yes/no input"""
    default_str = "Y/n" if default else "y/N"
    response = input(f"{prompt} [{default_str}]: ").strip().lower()

    if not response:
        return default

    return response in ['y', 'yes', 'true', '1']


def setup_gmail(framework):
    """Setup Gmail integration"""
    print_section("Gmail Integration Setup")

    print("Gmail requires OAuth 2.0 credentials from Google Cloud Console.")
    print("Visit: https://console.cloud.google.com/")
    print()

    if not yes_no("Do you want to configure Gmail?", default=False):
        return

    config = {
        "enabled": True,
        "client_id": get_input("Client ID"),
        "client_secret": get_input("Client Secret"),
        "redirect_uri": get_input("Redirect URI", "http://localhost:8080/oauth2callback"),
        "access_token": None,
        "refresh_token": None,
        "scopes": [
            "https://www.googleapis.com/auth/gmail.send",
            "https://www.googleapis.com/auth/gmail.readonly",
            "https://www.googleapis.com/auth/gmail.modify"
        ]
    }

    framework.configure("gmail", config, save=True)
    print("\nGmail configured successfully!")
    print("Note: You'll need to complete the OAuth flow to get tokens.")


def setup_slack(framework):
    """Setup Slack integration"""
    print_section("Slack Integration Setup")

    print("Slack requires a Bot User OAuth Token.")
    print("Create app at: https://api.slack.com/apps")
    print()

    if not yes_no("Do you want to configure Slack?", default=False):
        return

    config = {
        "enabled": True,
        "bot_token": get_input("Bot User OAuth Token")
    }

    framework.configure("slack", config, save=True)
    print("\nSlack configured successfully!")

    # Test connection
    if yes_no("Test connection now?", default=True):
        result = framework.test("slack")
        if result["status"] == "success":
            print(f"✓ Connection successful! Connected as: {result['user']} in {result['team']}")
        else:
            print(f"✗ Connection failed: {result.get('error', 'Unknown error')}")


def setup_github(framework):
    """Setup GitHub integration"""
    print_section("GitHub Integration Setup")

    print("GitHub requires a Personal Access Token.")
    print("Create token at: https://github.com/settings/tokens")
    print("Required scopes: repo, user, admin:org")
    print()

    if not yes_no("Do you want to configure GitHub?", default=False):
        return

    config = {
        "enabled": True,
        "token": get_input("Personal Access Token")
    }

    framework.configure("github", config, save=True)
    print("\nGitHub configured successfully!")

    # Test connection
    if yes_no("Test connection now?", default=True):
        result = framework.test("github")
        if result["status"] == "success":
            print(f"✓ Connection successful! Connected as: {result['login']}")
        else:
            print(f"✗ Connection failed: {result.get('error', 'Unknown error')}")


def setup_notion(framework):
    """Setup Notion integration"""
    print_section("Notion Integration Setup")

    print("Notion requires an Internal Integration Token.")
    print("Create integration at: https://www.notion.so/my-integrations")
    print("Don't forget to share pages/databases with the integration!")
    print()

    if not yes_no("Do you want to configure Notion?", default=False):
        return

    config = {
        "enabled": True,
        "api_key": get_input("Internal Integration Token")
    }

    framework.configure("notion", config, save=True)
    print("\nNotion configured successfully!")

    # Test connection
    if yes_no("Test connection now?", default=True):
        result = framework.test("notion")
        if result["status"] == "success":
            print(f"✓ Connection successful! Accessible pages: {result.get('accessible_pages', 0)}")
        else:
            print(f"✗ Connection failed: {result.get('error', 'Unknown error')}")


def setup_trello(framework):
    """Setup Trello integration"""
    print_section("Trello Integration Setup")

    print("Trello requires an API Key and Token.")
    print("Get API Key at: https://trello.com/app-key")
    print("Generate token by clicking the Token link on that page")
    print()

    if not yes_no("Do you want to configure Trello?", default=False):
        return

    config = {
        "enabled": True,
        "api_key": get_input("API Key"),
        "token": get_input("Token")
    }

    framework.configure("trello", config, save=True)
    print("\nTrello configured successfully!")

    # Test connection
    if yes_no("Test connection now?", default=True):
        result = framework.test("trello")
        if result["status"] == "success":
            print(f"✓ Connection successful! Connected as: {result['username']}")
        else:
            print(f"✗ Connection failed: {result.get('error', 'Unknown error')}")


def show_status(framework):
    """Show status of all integrations"""
    print_section("Integration Status")

    integrations = framework.list_all_with_status()

    for integration in integrations:
        status_symbol = {
            "enabled": "✓",
            "disabled": "○",
            "not_configured": "✗"
        }.get(integration['status'], "?")

        auth_status = "authenticated" if integration['authenticated'] else "not authenticated"

        print(f"{status_symbol} {integration['display_name']}: {integration['status']} ({auth_status})")
        print(f"  {integration['description']}")


def manage_integrations(framework):
    """Interactive integration management"""
    print_section("Manage Integrations")

    integrations = framework.list_all_with_status()

    print("Available integrations:")
    for i, integration in enumerate(integrations, 1):
        status = integration['status']
        print(f"{i}. {integration['display_name']} [{status}]")

    print(f"{len(integrations) + 1}. Back to main menu")

    choice = get_input("\nSelect integration to manage (number)")

    try:
        choice_num = int(choice)
        if 1 <= choice_num <= len(integrations):
            selected = integrations[choice_num - 1]
            manage_single_integration(framework, selected['name'])
        elif choice_num == len(integrations) + 1:
            return
    except (ValueError, TypeError):
        print("Invalid choice")


def manage_single_integration(framework, integration_name):
    """Manage a single integration"""
    print_section(f"Managing {integration_name}")

    integration = framework.get(integration_name)

    print("1. Enable")
    print("2. Disable")
    print("3. Test connection")
    print("4. View statistics")
    print("5. Reconfigure")
    print("6. Back")

    choice = get_input("\nSelect action")

    if choice == "1":
        framework.enable(integration_name)
        print(f"✓ {integration_name} enabled")
    elif choice == "2":
        framework.disable(integration_name)
        print(f"✓ {integration_name} disabled")
    elif choice == "3":
        result = framework.test(integration_name)
        print(f"\nStatus: {result['status']}")
        for key, value in result.items():
            if key != 'status':
                print(f"  {key}: {value}")
    elif choice == "4":
        if integration:
            stats = integration.get_stats()
            print("\nStatistics:")
            for key, value in stats.items():
                print(f"  {key}: {value}")
        else:
            print("Integration not initialized")
    elif choice == "5":
        # Call appropriate setup function
        setup_functions = {
            "gmail": setup_gmail,
            "slack": setup_slack,
            "github": setup_github,
            "notion": setup_notion,
            "trello": setup_trello
        }
        if integration_name in setup_functions:
            setup_functions[integration_name](framework)
        else:
            print("Reconfiguration not available for this integration")


def main_menu(framework):
    """Main menu"""
    while True:
        print_header("Integration Framework Setup")

        print("1. Setup new integration")
        print("2. Manage integrations")
        print("3. View status")
        print("4. Test all integrations")
        print("5. Create example configs")
        print("6. Exit")

        choice = get_input("\nSelect option")

        if choice == "1":
            print("\nSelect integration to setup:")
            print("1. Gmail")
            print("2. Slack")
            print("3. GitHub")
            print("4. Notion")
            print("5. Trello")

            sub_choice = get_input("\nSelect")

            setup_functions = {
                "1": setup_gmail,
                "2": setup_slack,
                "3": setup_github,
                "4": setup_notion,
                "5": setup_trello
            }

            if sub_choice in setup_functions:
                setup_functions[sub_choice](framework)

        elif choice == "2":
            manage_integrations(framework)

        elif choice == "3":
            show_status(framework)

        elif choice == "4":
            print_section("Testing Integrations")
            results = framework.test_all()
            for name, result in results.items():
                status_symbol = "✓" if result['status'] == 'success' else "✗"
                print(f"{status_symbol} {name}: {result['status']}")
                if result['status'] == 'error':
                    print(f"  Error: {result.get('error', 'Unknown')}")

        elif choice == "5":
            framework.create_default_configs()
            print("\n✓ Example config files created in:")
            print(f"  {framework.config_dir}")

        elif choice == "6":
            print("\nGoodbye!")
            break

        else:
            print("\nInvalid choice. Please try again.")


def main():
    """Main entry point"""
    print_header("Agent Zero - Integration Framework Setup")

    print("This script will help you configure integrations for Agent Zero.")
    print(f"\nConfigurations will be saved to:")
    print(f"  {os.path.expanduser('~/.agent-zero/integrations/')}")
    print()

    # Initialize framework
    framework = IntegrationFramework()
    framework.setup()

    # Run main menu
    main_menu(framework)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup cancelled.")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)
