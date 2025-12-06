"""
Agent Zero CLI 2.0
Advanced Command Line Interface for Agent Zero
"""

__version__ = "2.0.0"
__author__ = "Agent Zero Team"

from .marketplace import marketplace_app
from .config import config_app, ConfigManager
from .project import project_app
from .agent_runner import agent_app
from .logs import logs_app

__all__ = [
    "marketplace_app",
    "config_app",
    "ConfigManager",
    "project_app",
    "agent_app",
    "logs_app",
]
