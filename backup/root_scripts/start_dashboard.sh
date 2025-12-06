#!/bin/bash

# Kleuren voor output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Starting AI Ecosystem Unified Dashboard...${NC}"

# 1. Configureer React Environment
echo -e "${BLUE}⚙️  Configuring Frontend...${NC}"
echo "VITE_API_URL=http://localhost:5000" > agent-forge/.env

# 2. Start Agent Zero Backend
echo -e "${BLUE}🧠 Starting Agent Zero Brain (Backend)...${NC}"
cd agent-zero
# Start backend in background, log naar file
python run_ui.py > ../backend.log 2>&1 &
BACKEND_PID=$!
cd ..

echo -e "${GREEN}✅ Backend started (PID: $BACKEND_PID)${NC}"
echo "   Logs: tail -f backend.log"

# 3. Wacht op Backend
echo -e "${BLUE}⏳ Waiting for Brain to wake up...${NC}"
max_retries=30
count=0
while ! curl -s http://localhost:5000/ok > /dev/null; do
    sleep 1
    count=$((count+1))
    if [ $count -ge $max_retries ]; then
        echo -e "${RED}❌ Backend failed to start! Check backend.log${NC}"
        kill $BACKEND_PID
        exit 1
    fi
    echo -n "."
done
echo -e "\n${GREEN}✅ Brain is ACTIVE!${NC}"

# 4. Start React Frontend
echo -e "${BLUE}🎨 Starting Dashboard (Frontend)...${NC}"
cd agent-forge
npm run dev -- --host &
FRONTEND_PID=$!
cd ..

# Cleanup functie
cleanup() {
    echo -e "\n${RED}🛑 Shutting down...${NC}"
    kill $BACKEND_PID
    kill $FRONTEND_PID
    exit 0
}

# Trap CTRL+C
trap cleanup SIGINT

echo -e "\n${GREEN}✨ SYSTEM OPERATIONAL! ✨${NC}"
echo -e "📱 Dashboard URL:  http://localhost:3001"
echo -e "🔌 API Endpoint:   http://localhost:5000"
echo -e "📝 Press CTRL+C to stop everything.\n"

# Keep script running to maintain processes
wait
