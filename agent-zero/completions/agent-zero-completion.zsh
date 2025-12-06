#!/usr/bin/env zsh
# Agent Zero CLI Zsh Completion Script
# Install: source this file or add to ~/.zshrc

#compdef agent-zero

_agent_zero() {
    local -a commands
    commands=(
        'marketplace:Marketplace for agents, tools, and prompts'
        'config:Configuration management'
        'project:Project management and scaffolding'
        'agent:Agent execution and management'
        'logs:View agent logs and execution history'
        'chat:Start interactive chat session'
        'init:Initialize a new Agent Zero project'
        'run:Execute a single task'
        'dev:Start development server'
        'deploy:Deploy Agent Zero to various platforms'
        'status:Show system status'
        'version:Display version information'
    )

    local -a marketplace_commands
    marketplace_commands=(
        'search:Search the marketplace'
        'list:List marketplace items'
        'install:Install an item'
        'publish:Publish an item'
        'info:Show item information'
        'update:Update installed items'
    )

    local -a config_commands
    config_commands=(
        'get:Get a configuration value'
        'set:Set a configuration value'
        'list:List configuration values'
        'delete:Delete a configuration key'
        'reset:Reset to defaults'
        'edit:Edit configuration'
        'validate:Validate configuration'
        'export:Export configuration'
        'import:Import configuration'
        'init:Initialize configuration'
    )

    local -a project_commands
    project_commands=(
        'init:Initialize a new project'
        'templates:List available templates'
        'info:Show project information'
        'validate:Validate project structure'
        'clean:Clean project artifacts'
    )

    local -a agent_commands
    agent_commands=(
        'run:Execute a task'
        'list:List available agents'
        'info:Show agent information'
        'create:Create a new agent'
        'test:Test an agent'
    )

    local -a logs_commands
    logs_commands=(
        'list:List recent logs'
        'show:Show log contents'
        'clear:Clear logs'
    )

    _arguments -C \
        '1: :->command' \
        '2: :->subcommand' \
        '*:: :->args' \
        && return 0

    case $state in
        command)
            _describe 'command' commands
            ;;
        subcommand)
            case $words[1] in
                marketplace)
                    _describe 'marketplace command' marketplace_commands
                    ;;
                config)
                    _describe 'config command' config_commands
                    ;;
                project)
                    _describe 'project command' project_commands
                    ;;
                agent)
                    _describe 'agent command' agent_commands
                    ;;
                logs)
                    _describe 'logs command' logs_commands
                    ;;
            esac
            ;;
        args)
            case $words[1] in
                marketplace|config|project|agent|logs)
                    _agent_zero_options
                    ;;
            esac
            ;;
    esac
}

_agent_zero_options() {
    _arguments \
        '--help[Show help message]' \
        '--version[Show version]' \
        '--verbose[Enable verbose output]' \
        '--quiet[Suppress non-essential output]' \
        '--template[Project template]:template:(default minimal research code)' \
        '--category[Item category]:category:(agent tool prompt)' \
        '--format[Output format]:format:(table json yaml)' \
        '--target[Deployment target]:target:(local cloud mobile docker)'
}

compdef _agent_zero agent-zero
compdef _agent_zero az  # Shortcut alias
