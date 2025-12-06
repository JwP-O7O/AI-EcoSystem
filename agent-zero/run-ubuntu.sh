#!/data/data/com.termux/files/usr/bin/bash
#
# Agent Zero - Ubuntu Container Launcher
# Draait Agent Zero binnen proot-distro Ubuntu omgeving
#

echo "🐧 Starting Agent Zero in Ubuntu container..."
echo ""

# Check of Ubuntu geïnstalleerd is
if [ ! -d "$PREFIX/var/lib/proot-distro/installed-rootfs/ubuntu" ]; then
    echo "❌ Ubuntu not installed!"
    echo "Run: proot-distro install ubuntu"
    exit 1
fi

# Launch Agent Zero in Ubuntu
proot-distro login ubuntu -- bash -c "
cd /root/agent-zero-link || cd /data/data/com.termux/files/home/AI-EcoSystem/agent-zero
if [ -d 'venv' ]; then
    echo '✓ Activating virtual environment...'
    source venv/bin/activate
else
    echo '⚠️  No virtual environment found, using system Python'
fi
python3 run_cli.py
"
