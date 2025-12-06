#!/usr/bin/env python3
"""
Agent Zero CLI 2.0 Setup
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text() if readme_file.exists() else ""

setup(
    name="agent-zero-cli",
    version="2.0.0",
    description="Advanced CLI for Agent Zero AI Agent Framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Agent Zero Team",
    author_email="team@agent-zero.io",
    url="https://github.com/frdel/agent-zero",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.10",
    install_requires=[
        "typer[all]>=0.12.0",
        "rich>=13.7.0",
        "python-dotenv>=1.0.0",
        "requests>=2.31.0",
        "psutil>=5.9.0",
        "watchdog>=4.0.0",
        "pydantic>=2.5.0",
        "pyyaml>=6.0.1",
    ],
    entry_points={
        "console_scripts": [
            "agent-zero=cli:cli_main",
            "az=cli:cli_main",  # Short alias
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    keywords="ai agent cli framework automation",
    project_urls={
        "Bug Reports": "https://github.com/frdel/agent-zero/issues",
        "Source": "https://github.com/frdel/agent-zero",
        "Documentation": "https://agent-zero.io/docs",
    },
)
