#!/usr/bin/env bash
# Agent Zero CLI Bash Completion Script
# Install: source this file or add to ~/.bashrc

_agent_zero_completion() {
    local cur prev opts base
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"

    # Main commands
    commands="marketplace config project agent logs chat init run dev deploy status version --help --version"

    # Marketplace subcommands
    marketplace_cmds="search list install publish info update"

    # Config subcommands
    config_cmds="get set list delete reset edit validate export import init"

    # Project subcommands
    project_cmds="init templates info validate clean"

    # Agent subcommands
    agent_cmds="run list info create test"

    # Logs subcommands
    logs_cmds="list show clear"

    case "${COMP_CWORD}" in
        1)
            COMPREPLY=( $(compgen -W "${commands}" -- ${cur}) )
            return 0
            ;;
        2)
            case "${prev}" in
                marketplace)
                    COMPREPLY=( $(compgen -W "${marketplace_cmds}" -- ${cur}) )
                    return 0
                    ;;
                config)
                    COMPREPLY=( $(compgen -W "${config_cmds}" -- ${cur}) )
                    return 0
                    ;;
                project)
                    COMPREPLY=( $(compgen -W "${project_cmds}" -- ${cur}) )
                    return 0
                    ;;
                agent)
                    COMPREPLY=( $(compgen -W "${agent_cmds}" -- ${cur}) )
                    return 0
                    ;;
                logs)
                    COMPREPLY=( $(compgen -W "${logs_cmds}" -- ${cur}) )
                    return 0
                    ;;
            esac
            ;;
        *)
            # Option completions
            case "${prev}" in
                --template|-t)
                    COMPREPLY=( $(compgen -W "default minimal research code" -- ${cur}) )
                    return 0
                    ;;
                --category|-c)
                    COMPREPLY=( $(compgen -W "agent tool prompt" -- ${cur}) )
                    return 0
                    ;;
                --format|-f)
                    COMPREPLY=( $(compgen -W "table json yaml" -- ${cur}) )
                    return 0
                    ;;
                --target)
                    COMPREPLY=( $(compgen -W "local cloud mobile docker" -- ${cur}) )
                    return 0
                    ;;
            esac
            ;;
    esac

    # Default to file completion
    COMPREPLY=( $(compgen -f -- ${cur}) )
    return 0
}

complete -F _agent_zero_completion agent-zero
complete -F _agent_zero_completion az  # Shortcut alias
