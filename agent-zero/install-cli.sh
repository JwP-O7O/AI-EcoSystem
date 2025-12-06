#!/bin/bash
# Agent Zero CLI 2.0 Installation Script

set -e

echo "=================================="
echo "Agent Zero CLI 2.0 Installation"
echo "=================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo -e "${YELLOW}Step 1: Installing Python requirements...${NC}"
pip install -r "$SCRIPT_DIR/requirements-cli.txt" || {
    echo -e "${RED}Failed to install requirements${NC}"
    exit 1
}
echo -e "${GREEN}✓ Requirements installed${NC}"
echo ""

echo -e "${YELLOW}Step 2: Making CLI executable...${NC}"
chmod +x "$SCRIPT_DIR/cli.py"
echo -e "${GREEN}✓ CLI is now executable${NC}"
echo ""

echo -e "${YELLOW}Step 3: Setting up shell integration...${NC}"

# Detect shell
if [ -n "$BASH_VERSION" ]; then
    SHELL_RC="$HOME/.bashrc"
    COMPLETION_FILE="$SCRIPT_DIR/completions/agent-zero-completion.bash"
elif [ -n "$ZSH_VERSION" ]; then
    SHELL_RC="$HOME/.zshrc"
    COMPLETION_FILE="$SCRIPT_DIR/completions/agent-zero-completion.zsh"
else
    SHELL_RC="$HOME/.bashrc"
    COMPLETION_FILE="$SCRIPT_DIR/completions/agent-zero-completion.bash"
fi

# Add alias
if ! grep -q "alias az=" "$SHELL_RC" 2>/dev/null; then
    echo "" >> "$SHELL_RC"
    echo "# Agent Zero CLI alias" >> "$SHELL_RC"
    echo "alias az='python $SCRIPT_DIR/cli.py'" >> "$SHELL_RC"
    echo "alias agent-zero='python $SCRIPT_DIR/cli.py'" >> "$SHELL_RC"
    echo -e "${GREEN}✓ Added alias to $SHELL_RC${NC}"
else
    echo -e "${YELLOW}⚠ Alias already exists in $SHELL_RC${NC}"
fi

# Add completion
if ! grep -q "agent-zero-completion" "$SHELL_RC" 2>/dev/null; then
    echo "source $COMPLETION_FILE" >> "$SHELL_RC"
    echo -e "${GREEN}✓ Added shell completion to $SHELL_RC${NC}"
else
    echo -e "${YELLOW}⚠ Shell completion already configured${NC}"
fi

echo ""
echo -e "${YELLOW}Step 4: Creating symlink (optional)...${NC}"

# Try to create symlink in ~/.local/bin
LOCAL_BIN="$HOME/.local/bin"
if [ -d "$LOCAL_BIN" ]; then
    ln -sf "$SCRIPT_DIR/cli.py" "$LOCAL_BIN/agent-zero" 2>/dev/null && {
        echo -e "${GREEN}✓ Created symlink in $LOCAL_BIN${NC}"
    } || {
        echo -e "${YELLOW}⚠ Could not create symlink (may need permissions)${NC}"
    }
else
    echo -e "${YELLOW}⚠ $LOCAL_BIN does not exist, skipping symlink${NC}"
fi

echo ""
echo "=================================="
echo -e "${GREEN}Installation Complete!${NC}"
echo "=================================="
echo ""
echo "Next steps:"
echo "  1. Reload your shell:"
echo "     ${YELLOW}source $SHELL_RC${NC}"
echo ""
echo "  2. Initialize configuration:"
echo "     ${YELLOW}agent-zero config init${NC}"
echo "     or: ${YELLOW}az config init${NC}"
echo ""
echo "  3. Start using Agent Zero:"
echo "     ${YELLOW}agent-zero chat${NC}"
echo "     ${YELLOW}agent-zero run \"your task\"${NC}"
echo "     ${YELLOW}agent-zero --help${NC}"
echo ""
echo "For the complete guide, see:"
echo "  ${YELLOW}$SCRIPT_DIR/CLI_GUIDE.md${NC}"
echo ""
