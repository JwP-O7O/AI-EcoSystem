"""
Integration Framework for Agent Zero
Auto-discovery and management of 3rd party service integrations
"""

import os
import importlib
import inspect
import logging
from typing import Dict, Type, Optional, Any, List
from pathlib import Path

from .base import BaseIntegration

logger = logging.getLogger(__name__)


class IntegrationRegistry:
    """
    Registry for managing integrations

    Features:
    - Auto-discovery of integration classes
    - Enable/disable integrations
    - Configuration management
    - Lifecycle management
    """

    def __init__(self, config_dir: Optional[str] = None):
        self.integrations: Dict[str, BaseIntegration] = {}
        self.integration_classes: Dict[str, Type[BaseIntegration]] = {}
        self.config_dir = config_dir or os.path.expanduser("~/.agent-zero/integrations")
        self.configs: Dict[str, Dict[str, Any]] = {}

        # Ensure config directory exists
        os.makedirs(self.config_dir, exist_ok=True)

        logger.info(f"Integration registry initialized (config: {self.config_dir})")

    def discover_integrations(self):
        """
        Auto-discover integration classes in the integrations directory
        """
        # Get the directory containing integration modules
        integrations_dir = Path(__file__).parent

        # Scan for Python files
        for file_path in integrations_dir.glob("*.py"):
            if file_path.name.startswith("_") or file_path.name == "base.py":
                continue

            module_name = file_path.stem

            try:
                # Import the module
                module = importlib.import_module(f"python.integrations.{module_name}")

                # Find integration classes
                for name, obj in inspect.getmembers(module, inspect.isclass):
                    if (issubclass(obj, BaseIntegration) and
                        obj is not BaseIntegration and
                        not name.startswith("_")):

                        integration_name = module_name
                        self.integration_classes[integration_name] = obj
                        logger.info(f"Discovered integration: {integration_name} ({obj.__name__})")

            except Exception as e:
                logger.error(f"Failed to load integration module {module_name}: {e}")

    def load_config(self, integration_name: str) -> Dict[str, Any]:
        """Load configuration for an integration"""
        config_file = os.path.join(self.config_dir, f"{integration_name}.json")

        if os.path.exists(config_file):
            try:
                import json
                with open(config_file, "r") as f:
                    config = json.load(f)
                logger.info(f"Loaded config for {integration_name}")
                return config
            except Exception as e:
                logger.error(f"Failed to load config for {integration_name}: {e}")

        return {"enabled": False}

    def save_config(self, integration_name: str, config: Dict[str, Any]):
        """Save configuration for an integration"""
        config_file = os.path.join(self.config_dir, f"{integration_name}.json")

        try:
            import json
            with open(config_file, "w") as f:
                json.dump(config, indent=2, fp=f)
            logger.info(f"Saved config for {integration_name}")
        except Exception as e:
            logger.error(f"Failed to save config for {integration_name}: {e}")
            raise

    def register(self, integration_name: str, integration_class: Type[BaseIntegration]):
        """Manually register an integration class"""
        self.integration_classes[integration_name] = integration_class
        logger.info(f"Registered integration: {integration_name}")

    def initialize(self, integration_name: str, config: Optional[Dict[str, Any]] = None) -> BaseIntegration:
        """
        Initialize an integration

        Args:
            integration_name: Name of the integration
            config: Configuration dict (or load from file)

        Returns:
            Initialized integration instance
        """
        if integration_name not in self.integration_classes:
            raise ValueError(f"Unknown integration: {integration_name}")

        # Load config if not provided
        if config is None:
            config = self.load_config(integration_name)

        # Store config
        self.configs[integration_name] = config

        # Create instance
        integration_class = self.integration_classes[integration_name]
        integration = integration_class(name=integration_name, config=config)

        # Store instance
        self.integrations[integration_name] = integration

        logger.info(f"Initialized integration: {integration_name}")
        return integration

    def get(self, integration_name: str) -> Optional[BaseIntegration]:
        """Get an integration instance"""
        if integration_name not in self.integrations:
            # Try to initialize it
            if integration_name in self.integration_classes:
                try:
                    return self.initialize(integration_name)
                except Exception as e:
                    logger.error(f"Failed to initialize {integration_name}: {e}")
                    return None

        return self.integrations.get(integration_name)

    def enable(self, integration_name: str):
        """Enable an integration"""
        integration = self.get(integration_name)
        if integration:
            integration.enabled = True
            config = self.configs.get(integration_name, {})
            config["enabled"] = True
            self.save_config(integration_name, config)
            logger.info(f"Enabled integration: {integration_name}")

    def disable(self, integration_name: str):
        """Disable an integration"""
        integration = self.get(integration_name)
        if integration:
            integration.enabled = False
            config = self.configs.get(integration_name, {})
            config["enabled"] = False
            self.save_config(integration_name, config)
            logger.info(f"Disabled integration: {integration_name}")

    def list_available(self) -> List[str]:
        """List all available integrations"""
        return list(self.integration_classes.keys())

    def list_enabled(self) -> List[str]:
        """List all enabled integrations"""
        return [
            name for name, integration in self.integrations.items()
            if integration.enabled
        ]

    def get_all_stats(self) -> Dict[str, Dict[str, Any]]:
        """Get statistics for all integrations"""
        return {
            name: integration.get_stats()
            for name, integration in self.integrations.items()
        }

    def test_all(self) -> Dict[str, Dict[str, Any]]:
        """Test all enabled integrations"""
        results = {}
        for name, integration in self.integrations.items():
            if integration.enabled:
                try:
                    results[name] = integration.test_connection()
                except Exception as e:
                    results[name] = {"status": "error", "error": str(e)}
        return results


# Global registry instance
registry = IntegrationRegistry()


def get_integration(name: str) -> Optional[BaseIntegration]:
    """Get an integration by name"""
    return registry.get(name)


def list_integrations() -> List[str]:
    """List all available integrations"""
    return registry.list_available()


__all__ = [
    "BaseIntegration",
    "IntegrationRegistry",
    "registry",
    "get_integration",
    "list_integrations"
]
