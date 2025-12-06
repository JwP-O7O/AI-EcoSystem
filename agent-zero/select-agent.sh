#!/data/data/com.termux/files/usr/bin/bash
#
# Agent Zero - Specialized Agent Selector
# Interactief menu om een gespecialiseerde agent te kiezen
#

clear
echo "╔══════════════════════════════════════════════════════════╗"
echo "║          🤖 Agent Zero - Agent Selector 🤖              ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
echo "Kies je gespecialiseerde agent:"
echo ""
echo "  1) 🎭 Master Orchestrator (Default - Hoofdcoördinator)"
echo "  2) 💻 Code Specialist (Python/NodeJS/Terminal expert)"
echo "  3) 🔍 Research Specialist (Online research expert)"
echo "  4) 💾 Memory Manager (Geheugen beheerder)"
echo "  5) 🌐 Web Scraper (Web content extractie)"
echo "  6) 🎯 Task Orchestrator (Delegatie coördinator)"
echo "  7) 🏗️  Solution Architect (Strategische planner)"
echo ""
echo "  8) ⚡ Default Agent (Geen specialisatie)"
echo ""
echo "  0) ❌ Annuleren"
echo ""
read -p "Maak je keuze (0-8): " choice

case $choice in
    1)
        AGENT_ROLE="master_orchestrator"
        AGENT_NAME="Master Orchestrator"
        ;;
    2)
        AGENT_ROLE="code_specialist"
        AGENT_NAME="Code Specialist"
        ;;
    3)
        AGENT_ROLE="knowledge_researcher"
        AGENT_NAME="Research Specialist"
        ;;
    4)
        AGENT_ROLE="memory_manager"
        AGENT_NAME="Memory Manager"
        ;;
    5)
        AGENT_ROLE="web_scraper"
        AGENT_NAME="Web Scraper"
        ;;
    6)
        AGENT_ROLE="task_orchestrator"
        AGENT_NAME="Task Orchestrator"
        ;;
    7)
        AGENT_ROLE="solution_architect"
        AGENT_NAME="Solution Architect"
        ;;
    8)
        AGENT_ROLE="default"
        AGENT_NAME="Default Agent"
        ;;
    0)
        echo "❌ Geannuleerd."
        exit 0
        ;;
    *)
        echo "❌ Ongeldige keuze!"
        exit 1
        ;;
esac

echo ""
echo "✅ Agent geselecteerd: $AGENT_NAME"
echo ""
echo "Wil je starten in:"
echo "  1) Native Termux (Snelst)"
echo "  2) Ubuntu Container (Volledig Linux)"
echo ""
read -p "Keuze (1-2): " runtime

echo ""
echo "🚀 Starting $AGENT_NAME..."
echo ""

# Export agent role for use in Agent Zero
export AGENT_ZERO_ROLE="$AGENT_ROLE"

if [ "$runtime" = "2" ]; then
    # Ubuntu container
    proot-distro login ubuntu -- bash -c "
    export AGENT_ZERO_ROLE='$AGENT_ROLE'
    cd /root/agent-zero-link || cd /data/data/com.termux/files/home/AI-EcoSystem/agent-zero
    if [ -d 'venv' ]; then
        echo '✓ Activating virtual environment...'
        source venv/bin/activate
    fi
    python3 run_cli.py
    "
else
    # Native Termux
    cd /data/data/com.termux/files/home/AI-EcoSystem/agent-zero
    python run_cli.py
fi
