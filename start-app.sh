#!/bin/bash
# AI EcoSystem - Master Startup Script

set -e

echo "=========================================="
echo "🚀 AI EcoSystem Starting..."
echo "=========================================="
echo ""

# Change to script directory
cd "$(dirname "$0")"

# Load environment variables
if [ -f android-app/.env ]; then
    export $(cat android-app/.env | grep -v '^#' | xargs)
fi

# Set defaults
export GATEWAY_PORT=${GATEWAY_PORT:-8080}
export NODE_ENV=${NODE_ENV:-production}

# Function to check if port is in use
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
        echo "⚠️  Port $1 is already in use"
        return 1
    fi
    return 0
}

# Function to wait for service
wait_for_service() {
    local url=$1
    local name=$2
    local max_attempts=10
    local attempt=0

    echo "⏳ Waiting for $name..."
    while [ $attempt -lt $max_attempts ]; do
        if curl -s "$url" >/dev/null 2>&1; then
            echo "✅ $name is ready"
            return 0
        fi
        attempt=$((attempt + 1))
        sleep 1
    done

    echo "⚠️  $name did not start in time"
    return 1
}

# Trap cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping services..."
    if [ ! -z "$GATEWAY_PID" ]; then
        kill $GATEWAY_PID 2>/dev/null || true
    fi
    echo "👋 Goodbye!"
    exit 0
}

trap cleanup INT TERM

# Check ports
echo "🔍 Checking ports..."
check_port 8080 || { echo "Please stop the service using port 8080 first"; exit 1; }

# Install backend dependencies if needed
if [ ! -d "android-app/backend/venv" ]; then
    echo "📦 Installing backend dependencies..."
    cd android-app/backend
    python -m pip install -q -r requirements.txt
    cd ../..
fi

# Start Backend Gateway
echo ""
echo "🌐 Starting Backend Gateway (port $GATEWAY_PORT)..."
cd android-app/backend
python gateway.py &
GATEWAY_PID=$!
cd ../..

# Wait for gateway to be ready
wait_for_service "http://localhost:$GATEWAY_PORT/health" "Gateway"

echo ""
echo "=========================================="
echo "✅ AI EcoSystem is running!"
echo "=========================================="
echo ""
echo "📱 Access the app:"
echo "   - Gateway API: http://localhost:$GATEWAY_PORT"
echo "   - Health Check: http://localhost:$GATEWAY_PORT/health"
echo ""
echo "🔧 Services:"
echo "   - Agent Zero: Configure and start separately"
echo "   - Solana Bot: Auto-started by gateway"
echo "   - Marketplace: Static files"
echo ""
echo "💡 Frontend Development:"
echo "   cd android-app/frontend"
echo "   npm install"
echo "   npm run dev"
echo ""
echo "📱 Production:"
echo "   - Build: cd android-app/frontend && npm run build"
echo "   - Frontend served from: http://localhost:$GATEWAY_PORT"
echo ""
echo "Press Ctrl+C to stop all services"
echo "=========================================="
echo ""

# Keep script running
wait $GATEWAY_PID
