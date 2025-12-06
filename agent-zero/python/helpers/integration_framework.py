"""
Integration Framework Helper for Agent Zero

Main interface for managing and using 3rd party service integrations.
Provides unified access to Gmail, Slack, GitHub, Notion, Trello, and custom integrations.

Usage:
    >>> from python.helpers.integration_framework import IntegrationFramework
    >>> framework = IntegrationFramework()
    >>> framework.setup()
    >>>
    >>> # Use an integration
    >>> gmail = framework.get("gmail")
    >>> gmail.send_email(to="user@example.com", subject="Hello", body="Test")
    >>>
    >>> # List all integrations
    >>> framework.list_all()
"""

import os
import json
import logging
from typing import Dict, Any, Optional, List

from python.integrations import IntegrationRegistry, BaseIntegration
from python.integrations.gmail import GmailIntegration
from python.integrations.slack import SlackIntegration
from python.integrations.github import GitHubIntegration
from python.integrations.notion import NotionIntegration
from python.integrations.trello import TrelloIntegration

logger = logging.getLogger(__name__)


class IntegrationFramework:
    """
    Unified Integration Framework for Agent Zero

    Manages all 3rd party service integrations with:
    - Auto-discovery of available integrations
    - Configuration management
    - Easy enable/disable
    - Connection testing
    - Statistics and monitoring
    """

    def __init__(self, config_dir: Optional[str] = None):
        """
        Initialize the integration framework

        Args:
            config_dir: Directory for integration configs (default: ~/.agent-zero/integrations)
        """
        self.config_dir = config_dir or os.path.expanduser("~/.agent-zero/integrations")
        self.registry = IntegrationRegistry(config_dir=self.config_dir)

        logger.info(f"Integration framework initialized (config: {self.config_dir})")

    def setup(self):
        """
        Setup the integration framework

        Registers all built-in integrations and discovers any custom ones.
        """
        # Register built-in integrations
        self.registry.register("gmail", GmailIntegration)
        self.registry.register("slack", SlackIntegration)
        self.registry.register("github", GitHubIntegration)
        self.registry.register("notion", NotionIntegration)
        self.registry.register("trello", TrelloIntegration)

        # Discover custom integrations
        self.registry.discover_integrations()

        logger.info(f"Framework setup complete. Available integrations: {self.list_available()}")

    def get(self, integration_name: str) -> Optional[BaseIntegration]:
        """
        Get an integration instance

        Args:
            integration_name: Name of the integration (gmail, slack, github, etc.)

        Returns:
            Integration instance or None if not found/configured

        Example:
            >>> gmail = framework.get("gmail")
            >>> if gmail and gmail.is_authenticated():
            ...     gmail.send_email(...)
        """
        return self.registry.get(integration_name)

    def configure(
        self,
        integration_name: str,
        config: Dict[str, Any],
        save: bool = True
    ) -> BaseIntegration:
        """
        Configure an integration

        Args:
            integration_name: Name of the integration
            config: Configuration dict
            save: Save configuration to file

        Returns:
            Configured integration instance

        Example:
            >>> framework.configure("github", {
            ...     "enabled": True,
            ...     "token": "ghp_xxxxxxxxxxxx"
            ... })
        """
        if save:
            self.registry.save_config(integration_name, config)

        return self.registry.initialize(integration_name, config)

    def enable(self, integration_name: str):
        """
        Enable an integration

        Args:
            integration_name: Name of the integration

        Example:
            >>> framework.enable("slack")
        """
        self.registry.enable(integration_name)

    def disable(self, integration_name: str):
        """
        Disable an integration

        Args:
            integration_name: Name of the integration

        Example:
            >>> framework.disable("slack")
        """
        self.registry.disable(integration_name)

    def list_available(self) -> List[str]:
        """
        List all available integrations

        Returns:
            List of integration names

        Example:
            >>> integrations = framework.list_available()
            >>> print(integrations)
            ['gmail', 'slack', 'github', 'notion', 'trello']
        """
        return self.registry.list_available()

    def list_enabled(self) -> List[str]:
        """
        List enabled integrations

        Returns:
            List of enabled integration names

        Example:
            >>> enabled = framework.list_enabled()
        """
        return self.registry.list_enabled()

    def test_all(self) -> Dict[str, Dict[str, Any]]:
        """
        Test all enabled integrations

        Returns:
            Dict mapping integration names to test results

        Example:
            >>> results = framework.test_all()
            >>> for name, result in results.items():
            ...     print(f"{name}: {result['status']}")
        """
        return self.registry.test_all()

    def test(self, integration_name: str) -> Dict[str, Any]:
        """
        Test a specific integration

        Args:
            integration_name: Name of the integration

        Returns:
            Test result dict

        Example:
            >>> result = framework.test("gmail")
            >>> if result["status"] == "success":
            ...     print("Gmail is configured correctly!")
        """
        integration = self.get(integration_name)
        if not integration:
            return {"status": "error", "error": "Integration not found or not configured"}

        try:
            return integration.test_connection()
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def get_stats(self) -> Dict[str, Dict[str, Any]]:
        """
        Get statistics for all integrations

        Returns:
            Dict mapping integration names to their stats

        Example:
            >>> stats = framework.get_stats()
            >>> for name, stat in stats.items():
            ...     print(f"{name}: {stat['success_rate']}")
        """
        return self.registry.get_all_stats()

    def reset_stats(self, integration_name: Optional[str] = None):
        """
        Reset statistics

        Args:
            integration_name: Reset specific integration, or all if None

        Example:
            >>> framework.reset_stats("gmail")  # Reset Gmail stats
            >>> framework.reset_stats()  # Reset all stats
        """
        if integration_name:
            integration = self.get(integration_name)
            if integration:
                integration.reset_stats()
        else:
            for integration in self.registry.integrations.values():
                integration.reset_stats()

    def create_default_configs(self):
        """
        Create default configuration templates for all integrations

        This creates example config files that users can fill in with their credentials.
        """
        configs = {
            "gmail": {
                "enabled": False,
                "client_id": "YOUR_CLIENT_ID.apps.googleusercontent.com",
                "client_secret": "YOUR_CLIENT_SECRET",
                "redirect_uri": "http://localhost:8080/oauth2callback",
                "access_token": None,
                "refresh_token": None,
                "scopes": [
                    "https://www.googleapis.com/auth/gmail.send",
                    "https://www.googleapis.com/auth/gmail.readonly",
                    "https://www.googleapis.com/auth/gmail.modify"
                ]
            },
            "slack": {
                "enabled": False,
                "bot_token": "xoxb-YOUR-BOT-TOKEN",
                "webhook_secret": "YOUR_WEBHOOK_SECRET"
            },
            "github": {
                "enabled": False,
                "token": "ghp_YOUR_PERSONAL_ACCESS_TOKEN"
            },
            "notion": {
                "enabled": False,
                "api_key": "secret_YOUR_INTERNAL_INTEGRATION_TOKEN"
            },
            "trello": {
                "enabled": False,
                "api_key": "YOUR_API_KEY",
                "token": "YOUR_TOKEN"
            }
        }

        for name, config in configs.items():
            config_file = os.path.join(self.config_dir, f"{name}.json.example")
            try:
                with open(config_file, "w") as f:
                    json.dump(config, f, indent=2)
                logger.info(f"Created example config: {config_file}")
            except Exception as e:
                logger.error(f"Failed to create example config for {name}: {e}")

    def get_integration_info(self, integration_name: str) -> Dict[str, Any]:
        """
        Get detailed information about an integration

        Args:
            integration_name: Name of the integration

        Returns:
            Dict with integration information

        Example:
            >>> info = framework.get_integration_info("gmail")
            >>> print(info["description"])
            >>> print(info["setup_instructions"])
        """
        info_map = {
            "gmail": {
                "name": "Gmail",
                "description": "Send and manage emails through Gmail API",
                "setup_instructions": [
                    "1. Enable Gmail API in Google Cloud Console",
                    "2. Create OAuth 2.0 credentials",
                    "3. Add authorized redirect URI",
                    "4. Configure client_id and client_secret",
                    "5. Complete OAuth flow to get tokens"
                ],
                "required_config": ["client_id", "client_secret", "redirect_uri"],
                "capabilities": [
                    "Send emails with attachments",
                    "Read email messages",
                    "Search emails",
                    "Mark as read/unread",
                    "Archive and delete",
                    "Create drafts",
                    "Manage labels"
                ]
            },
            "slack": {
                "name": "Slack",
                "description": "Send messages and interact with Slack workspace",
                "setup_instructions": [
                    "1. Create Slack App at api.slack.com/apps",
                    "2. Add Bot Token Scopes",
                    "3. Install app to workspace",
                    "4. Copy Bot User OAuth Token",
                    "5. Configure bot_token in config"
                ],
                "required_config": ["bot_token"],
                "capabilities": [
                    "Send messages to channels/users",
                    "Read channel history",
                    "Search messages",
                    "Upload files",
                    "Manage channels",
                    "React to messages",
                    "Get user info"
                ]
            },
            "github": {
                "name": "GitHub",
                "description": "Manage repositories, issues, and pull requests",
                "setup_instructions": [
                    "1. Go to github.com/settings/tokens",
                    "2. Create Personal Access Token",
                    "3. Select scopes: repo, user, admin:org",
                    "4. Copy token",
                    "5. Configure token in config"
                ],
                "required_config": ["token"],
                "capabilities": [
                    "Create/manage repositories",
                    "Create/update issues",
                    "Create/merge pull requests",
                    "Manage branches",
                    "Search code/repos",
                    "Create releases",
                    "Get file content"
                ]
            },
            "notion": {
                "name": "Notion",
                "description": "Create and manage Notion pages and databases",
                "setup_instructions": [
                    "1. Go to notion.so/my-integrations",
                    "2. Create new integration",
                    "3. Copy Internal Integration Token",
                    "4. Share pages/databases with integration",
                    "5. Configure api_key in config"
                ],
                "required_config": ["api_key"],
                "capabilities": [
                    "Create/update pages",
                    "Query databases",
                    "Create database entries",
                    "Search content",
                    "Add blocks to pages",
                    "Create comments",
                    "Manage page hierarchy"
                ]
            },
            "trello": {
                "name": "Trello",
                "description": "Manage Trello boards, lists, and cards",
                "setup_instructions": [
                    "1. Go to trello.com/app-key",
                    "2. Copy API Key",
                    "3. Click Token link to generate token",
                    "4. Copy token",
                    "5. Configure api_key and token in config"
                ],
                "required_config": ["api_key", "token"],
                "capabilities": [
                    "Create/manage boards",
                    "Create/update cards",
                    "Manage lists",
                    "Add comments",
                    "Assign members",
                    "Add labels and checklists",
                    "Search cards"
                ]
            }
        }

        return info_map.get(integration_name, {
            "name": integration_name,
            "description": "Custom integration",
            "setup_instructions": [],
            "required_config": [],
            "capabilities": []
        })

    def list_all_with_status(self) -> List[Dict[str, Any]]:
        """
        List all integrations with their status

        Returns:
            List of dicts with integration info and status

        Example:
            >>> integrations = framework.list_all_with_status()
            >>> for integration in integrations:
            ...     print(f"{integration['name']}: {integration['status']}")
        """
        result = []

        for name in self.list_available():
            integration = self.get(name)
            info = self.get_integration_info(name)

            status = "not_configured"
            if integration:
                if integration.enabled:
                    status = "enabled"
                else:
                    status = "disabled"

            result.append({
                "name": name,
                "display_name": info.get("name", name),
                "status": status,
                "authenticated": integration.is_authenticated() if integration else False,
                "description": info.get("description", "")
            })

        return result


# Global framework instance
_framework = None


def get_framework() -> IntegrationFramework:
    """Get the global integration framework instance"""
    global _framework
    if _framework is None:
        _framework = IntegrationFramework()
        _framework.setup()
    return _framework


def get_integration(name: str) -> Optional[BaseIntegration]:
    """Get an integration by name (convenience function)"""
    return get_framework().get(name)
