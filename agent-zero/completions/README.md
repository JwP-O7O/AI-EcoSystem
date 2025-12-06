# Agent Zero CLI Shell Completions

Auto-completion scripts for Bash and Zsh shells.

## Installation

### Bash

Add to your `~/.bashrc`:

```bash
source /path/to/agent-zero/completions/agent-zero-completion.bash
```

Or for Termux:

```bash
source $HOME/AI-EcoSystem/agent-zero/completions/agent-zero-completion.bash
```

Then reload:

```bash
source ~/.bashrc
```

### Zsh

Add to your `~/.zshrc`:

```zsh
source /path/to/agent-zero/completions/agent-zero-completion.zsh
```

Or for Termux:

```zsh
source $HOME/AI-EcoSystem/agent-zero/completions/agent-zero-completion.zsh
```

Then reload:

```zsh
source ~/.zshrc
```

## Usage

After installation, you can use Tab to auto-complete:

```bash
agent-zero <TAB>              # Shows all main commands
agent-zero marketplace <TAB>  # Shows marketplace subcommands
agent-zero config <TAB>       # Shows config subcommands
agent-zero --template <TAB>   # Shows template options
```

## Alias

Both completion scripts support the `az` alias as a shortcut:

```bash
az <TAB>  # Same as agent-zero <TAB>
```

To enable the alias, add to your shell config:

```bash
alias az='agent-zero'
```
