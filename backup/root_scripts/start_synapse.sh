#!/bin/bash

# PROJECT SYNAPSE LAUNCHER
# Version: 1.0.0
# Identity: Prime Orchestrator

RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "╔══════════════════════════════════════════════════════════╗"
echo "║             PROJECT SYNAPSE: AWAKENING                   ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# 1. System Check
echo -e "${BLUE}[*] System Verification...${NC}"
if ! pkg list-installed | grep -q termux-api; then
    echo -e "${RED}[!] Termux API missing. Installing...${NC}"
    pkg install termux-api -y
else
    echo -e "${GREEN}[✓] Termux API detected.${NC}"
fi

# 2. Environment Setup
export AGENT_ZERO_HOME=$(pwd)/agent-zero
export AGENT_FORGE_HOME=$(pwd)/agent-forge

# 3. Menu
echo ""
echo "Select Neural Pathway:"
echo "1) 🧠 Start Agent Zero (The Brain - CLI)"
echo "2) 🖼️  Start Agent Forge (The Face - WebUI)"
echo "3) 🗣️  Test Voice Module (The Senses)"
echo "4) 🚀 Launch ALL Systems (Split Screen recommended)"
echo "5) 💓 Start Synapse Daemon (The Pulse)"
echo "q) Quit"
echo ""
read -p "Choice: " choice

case $choice in
    1)
        echo -e "${GREEN}Initializing Neural Core...${NC}"
        cd $AGENT_ZERO_HOME
        ./run-termux.sh
        ;;
    2)
        echo -e "${GREEN}Booting Visual Cortex...${NC}"
        cd $AGENT_FORGE_HOME
        npm run dev
        ;;
    3)
        echo -e "${GREEN}Testing Audio Output...${NC}"
        termux-tts-speak "Project Synapse Systems Online. Voice Module Active."
        echo "Did you hear that? (Make sure volume is up)"
        ;;
    4)
        echo -e "${GREEN}Full System Awakening (Synapse OS v2.0)...${NC}"
        
        # Start Backend API
        echo "Starting API Core (Port 8000)..."
        ./agent-zero/run_api.sh > api_service.log 2>&1 &
        API_PID=$!
        echo "API PID: $API_PID"
        
        # Start Frontend
        echo "Starting Visual Cortex (Port 3001)..."
        cd $AGENT_FORGE_HOME
        # Wait a bit for API to warm up
        sleep 3
        npm run dev > ../frontend.log 2>&1 &
        FRONTEND_PID=$!
        echo "Frontend PID: $FRONTEND_PID"
        
        echo -e "${GREEN}Systems Online.${NC}"
        echo "API Logs: tail -f api_service.log"
        echo "Frontend: http://localhost:3001"
        echo "Press Any Key to Shutdown..."
        read -n 1
        
        # Cleanup on exit
        kill $FRONTEND_PID
        kill $API_PID
        ;;
    5)
        echo -e "${GREEN}Igniting Synapse Pulse...${NC}"
        cd $AGENT_ZERO_HOME
        python synapse_daemon.py
        ;;
    q)
        echo "Hibernating..."
        exit 0
        ;;
    *)
        echo "Invalid input."
        ;;
esac
