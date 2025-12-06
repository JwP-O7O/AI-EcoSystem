#!/data/data/com.termux/files/usr/bin/bash
#
# Agent Zero Android - Quick Start Menu
# Versie: 1.0 - November 29, 2025
#

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
ANDROID_DIR="$(dirname "$SCRIPT_DIR")"
BASE_DIR="$(dirname "$ANDROID_DIR")"

# Functions
print_header() {
    echo ""
    echo -e "${BLUE}${BOLD}╔════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}${BOLD}║${NC}     ${CYAN}${BOLD}🤖 Agent Zero Android - Quick Start Menu${NC}${BLUE}${BOLD}           ║${NC}"
    echo -e "${BLUE}${BOLD}╚════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

print_menu() {
    echo -e "${BOLD}Wat wil je doen?${NC}"
    echo ""
    echo -e "  ${GREEN}${BOLD}[1]${NC} 🚀 Start Agent Zero"
    echo -e "  ${CYAN}${BOLD}[2]${NC} 🎯 Specialized Agent Selector"
    echo -e "  ${YELLOW}${BOLD}[3]${NC} 🏥 Health Check (Diagnostics)"
    echo -e "  ${MAGENTA}${BOLD}[4]${NC} ⚙️  Configuration Info"
    echo -e "  ${BLUE}${BOLD}[5]${NC} 📚 Documentation"
    echo ""
    echo -e "  ${RED}${BOLD}[0]${NC} ❌ Exit"
    echo ""
}

start_agent_zero() {
    echo ""
    echo -e "${GREEN}${BOLD}🚀 Starting Agent Zero...${NC}"
    echo ""
    bash "$ANDROID_DIR/agent0_wrapper.sh"
}

start_agent_selector() {
    echo ""
    echo -e "${CYAN}${BOLD}🎯 Opening Agent Selector...${NC}"
    echo ""
    python "$SCRIPT_DIR/agent_selector.py"
}

run_health_check() {
    echo ""
    echo -e "${YELLOW}${BOLD}🏥 Running Health Check...${NC}"
    echo ""
    python "$SCRIPT_DIR/health_check.py"
    echo ""
    read -p "Press Enter to continue..."
}

show_config_info() {
    echo ""
    echo -e "${MAGENTA}${BOLD}╔════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${MAGENTA}${BOLD}║${NC}                  ${BOLD}⚙️  Configuration Info${NC}${MAGENTA}${BOLD}                    ║${NC}"
    echo -e "${MAGENTA}${BOLD}╚════════════════════════════════════════════════════════════════╝${NC}"
    echo ""

    # Load .env and show provider
    if [ -f "$ANDROID_DIR/config/.env" ]; then
        echo -e "${BOLD}📍 Config File:${NC} $ANDROID_DIR/config/.env"
        echo ""

        # Check which provider is configured
        source "$ANDROID_DIR/config/.env" 2>/dev/null

        echo -e "${BOLD}🔑 API Keys Status:${NC}"
        [ ! -z "$GOOGLE_API_KEY" ] && echo -e "  ${GREEN}✓${NC} Google API Key" || echo -e "  ${RED}✗${NC} Google API Key"
        [ ! -z "$OPENAI_API_KEY" ] && echo -e "  ${GREEN}✓${NC} OpenAI API Key" || echo -e "  ${RED}✗${NC} OpenAI API Key"
        [ ! -z "$ANTHROPIC_API_KEY" ] && echo -e "  ${GREEN}✓${NC} Anthropic API Key" || echo -e "  ${RED}✗${NC} Anthropic API Key"
        [ ! -z "$GROQ_API_KEY" ] && echo -e "  ${GREEN}✓${NC} Groq API Key" || echo -e "  ${RED}✗${NC} Groq API Key"
        echo ""

        if [ ! -z "$LLM_PROVIDER" ]; then
            echo -e "${BOLD}📱 Active Provider:${NC} $LLM_PROVIDER"
        else
            echo -e "${BOLD}📱 Active Provider:${NC} Auto-detect (based on available keys)"
        fi
        echo ""

    else
        echo -e "${RED}❌ .env file not found!${NC}"
        echo ""
        echo "Create it with:"
        echo -e "${CYAN}  cp $ANDROID_DIR/config/.env.example $ANDROID_DIR/config/.env${NC}"
        echo -e "${CYAN}  nano $ANDROID_DIR/config/.env${NC}"
        echo ""
    fi

    echo -e "${BOLD}📂 Directories:${NC}"
    echo "  Base: $BASE_DIR"
    echo "  Android: $ANDROID_DIR"
    echo "  Scripts: $SCRIPT_DIR"
    echo ""

    read -p "Press Enter to continue..."
}

show_documentation() {
    echo ""
    echo -e "${BLUE}${BOLD}╔════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}${BOLD}║${NC}                    ${BOLD}📚 Documentation${NC}${BLUE}${BOLD}                        ║${NC}"
    echo -e "${BLUE}${BOLD}╚════════════════════════════════════════════════════════════════╝${NC}"
    echo ""

    echo -e "${BOLD}Available Documentation:${NC}"
    echo ""
    echo -e "  ${GREEN}[1]${NC} README - Overview"
    echo -e "  ${GREEN}[2]${NC} QUICK_START - 10-min setup"
    echo -e "  ${GREEN}[3]${NC} TROUBLESHOOTING - Problem solving"
    echo -e "  ${GREEN}[4]${NC} EXAMPLES - Use cases"
    echo -e "  ${GREEN}[5]${NC} SPECIALIZED_AGENTS_GUIDE - Agent usage"
    echo ""
    echo -e "  ${RED}[0]${NC} Back to main menu"
    echo ""

    read -p "Select document [0-5]: " doc_choice

    case $doc_choice in
        1)
            cat "$ANDROID_DIR/README.md" | less
            ;;
        2)
            if [ -f "$ANDROID_DIR/docs/QUICK_START.md" ]; then
                cat "$ANDROID_DIR/docs/QUICK_START.md" | less
            else
                echo -e "${YELLOW}Document not found${NC}"
            fi
            ;;
        3)
            if [ -f "$ANDROID_DIR/docs/TROUBLESHOOTING.md" ]; then
                cat "$ANDROID_DIR/docs/TROUBLESHOOTING.md" | less
            else
                echo -e "${YELLOW}Document not found${NC}"
            fi
            ;;
        4)
            if [ -f "$ANDROID_DIR/docs/EXAMPLES.md" ]; then
                cat "$ANDROID_DIR/docs/EXAMPLES.md" | less
            else
                echo -e "${YELLOW}Document not found${NC}"
            fi
            ;;
        5)
            if [ -f "$BASE_DIR/docs/SPECIALIZED_AGENTS_GUIDE.md" ]; then
                cat "$BASE_DIR/docs/SPECIALIZED_AGENTS_GUIDE.md" | less
            else
                echo -e "${YELLOW}Document not found${NC}"
            fi
            ;;
        0)
            ;;
        *)
            echo -e "${RED}Invalid choice${NC}"
            ;;
    esac
}

# Main loop
while true; do
    clear
    print_header
    print_menu

    read -p "Select option [0-5]: " choice

    case $choice in
        1)
            start_agent_zero
            ;;
        2)
            start_agent_selector
            ;;
        3)
            run_health_check
            ;;
        4)
            show_config_info
            ;;
        5)
            show_documentation
            ;;
        0)
            echo ""
            echo -e "${YELLOW}👋 Goodbye!${NC}"
            echo ""
            exit 0
            ;;
        *)
            echo ""
            echo -e "${RED}❌ Invalid choice. Try again.${NC}"
            echo ""
            sleep 2
            ;;
    esac
done
