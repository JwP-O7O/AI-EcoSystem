#!/data/data/com.termux/files/usr/bin/bash
#
# Agent Zero Wrapper - Compact startup
#

# Bewaar de huidige directory
WORK_DIR="$(pwd)"

# Determine script location and project root
WRAPPER_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
AGENT_DIR="$(dirname "$WRAPPER_DIR")"

# Export work directory als environment variable
export AGENT_WORK_DIR="$WORK_DIR"

# Start Agent Zero vanuit zijn eigen directory (stil)
cd "$AGENT_DIR" 2>/dev/null
python android-versie/run_android_cli.py

# Ga terug naar work directory na exit
cd "$WORK_DIR" 2>/dev/null
