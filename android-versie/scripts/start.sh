#!/data/data/com.termux/files/usr/bin/bash

# ============================================================
# Agent Zero - Quick Start Launcher (Android/Termux)
# ============================================================

# Colors
GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m'

echo ""
echo -e "${CYAN}============================================================${NC}"
echo -e "${CYAN}🤖 Starting Agent Zero - Android Edition${NC}"
echo -e "${CYAN}============================================================${NC}"
echo ""

# Navigate to project root
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"
cd "$PROJECT_ROOT"

# Run Android CLI
python android-versie/run_android_cli.py
