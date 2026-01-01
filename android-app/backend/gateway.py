#!/usr/bin/env python3
"""
AI EcoSystem - Unified API Gateway
Orchestrates Agent Zero, Solana Bot, and Marketplace services
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_socketio import SocketIO, emit, join_room
import socketio as sio_client
import requests
import subprocess
import os
import sys
import time
import json
from threading import Thread, Lock
from pathlib import Path

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Solana Bot Socket.IO Client
solana_client = sio_client.Client()
solana_connect_lock = Lock()

@solana_client.event
def connect():
    print("✅ Connected to Solana Bot Socket.IO")

@solana_client.event
def disconnect():
    print("❌ Disconnected from Solana Bot Socket.IO")

@solana_client.on('dashboardUpdate')
def on_dashboard_update(data):
    """Forward dashboard updates to gateway clients"""
    # Broadcast to all clients in the subscription room
    socketio.emit('solana_update', data, room='solana_subscribers')

def ensure_solana_connection():
    """Ensure we are connected to Solana Bot"""
    with solana_connect_lock:
        if not solana_client.connected:
            try:
                url = SERVICES['solana_bot']['url']
                # Only attempt connection if service is likely running
                if check_service_health('solana_bot'):
                    print(f"Connecting to Solana Bot at {url}...")
                    solana_client.connect(url, wait_timeout=5)
                else:
                    print("⚠️ Solana Bot not healthy, skipping connection")
            except Exception as e:
                print(f"❌ Failed to connect to Solana Bot: {e}")

# Base paths
BASE_DIR = Path(__file__).parent.parent.parent
AGENT_ZERO_DIR = BASE_DIR / "agent-zero"
SOLANA_BOT_DIR = BASE_DIR / "solana-bot"
MARKETPLACE_DIR = BASE_DIR / "marketplace"

# Service configurations
SERVICES = {
    'agent_zero': {
        'url': 'http://localhost:5050',
        'start_cmd': None,  # Managed separately
        'process': None,
        'status': 'stopped'
    },
    'solana_bot': {
        'url': 'http://localhost:3000',
        'start_cmd': ['node', str(SOLANA_BOT_DIR / 'scalpingbot.js')],
        'process': None,
        'status': 'stopped'
    }
}

def check_service_health(service_name):
    """Check if a service is responding"""
    try:
        service = SERVICES.get(service_name)
        if not service:
            return False

        response = requests.get(
            f"{service['url']}/health" if service_name == 'agent_zero' else f"{service['url']}/api/status",
            timeout=2
        )
        return response.status_code == 200
    except:
        return False

def start_service(service_name):
    """Start a backend service"""
    service = SERVICES.get(service_name)
    if not service or not service['start_cmd']:
        return False

    try:
        if service['process'] is None or service['process'].poll() is not None:
            cwd = SOLANA_BOT_DIR if service_name == 'solana_bot' else None
            service['process'] = subprocess.Popen(
                service['start_cmd'],
                cwd=cwd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            service['status'] = 'starting'
            print(f"✅ Started {service_name}")
            return True
    except Exception as e:
        print(f"❌ Failed to start {service_name}: {e}")
        service['status'] = 'failed'
        return False

@app.route('/health', methods=['GET'])
def health_check():
    """System health check endpoint"""
    health = {
        'gateway': 'healthy',
        'timestamp': time.time(),
        'services': {}
    }

    for name, service in SERVICES.items():
        is_healthy = check_service_health(name)
        health['services'][name] = {
            'status': 'healthy' if is_healthy else 'unhealthy',
            'url': service['url']
        }

    # Marketplace (static)
    health['services']['marketplace'] = {
        'status': 'healthy' if MARKETPLACE_DIR.exists() else 'unavailable',
        'path': str(MARKETPLACE_DIR)
    }

    return jsonify(health), 200

# ==================== AGENT ZERO PROXY ====================

@app.route('/api/agent/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy_agent(path):
    """Proxy requests to Agent Zero backend"""
    try:
        url = f"{SERVICES['agent_zero']['url']}/{path}"

        # Prepare request data
        kwargs = {
            'method': request.method,
            'url': url,
            'headers': {k: v for k, v in request.headers if k.lower() != 'host'},
            'timeout': 30
        }

        if request.method in ['POST', 'PUT']:
            if request.is_json:
                kwargs['json'] = request.get_json()
            else:
                kwargs['data'] = request.get_data()

        # Forward request
        resp = requests.request(**kwargs)

        # Return response
        return (resp.content, resp.status_code, resp.headers.items())

    except requests.exceptions.ConnectionError:
        return jsonify({
            'error': 'Agent Zero backend not available',
            'message': 'Make sure Agent Zero is running on port 5050'
        }), 503
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== SOLANA BOT PROXY ====================

@app.route('/api/solana/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy_solana(path):
    """Proxy requests to Solana Bot"""
    try:
        url = f"{SERVICES['solana_bot']['url']}/api/{path}"

        kwargs = {
            'method': request.method,
            'url': url,
            'headers': {k: v for k, v in request.headers if k.lower() != 'host'},
            'timeout': 10
        }

        if request.method in ['POST', 'PUT']:
            if request.is_json:
                kwargs['json'] = request.get_json()
            else:
                kwargs['data'] = request.get_data()

        resp = requests.request(**kwargs)
        return (resp.content, resp.status_code, resp.headers.items())

    except requests.exceptions.ConnectionError:
        return jsonify({
            'error': 'Solana Bot not available',
            'message': 'Make sure Solana Bot is running on port 3000'
        }), 503
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== MARKETPLACE API ====================

@app.route('/api/marketplace/registry', methods=['GET'])
def get_marketplace_registry():
    """Get marketplace registry data"""
    try:
        registry_file = MARKETPLACE_DIR / 'registry.json'
        if not registry_file.exists():
            return jsonify({
                'version': '1.0.0',
                'agents': [],
                'tools': [],
                'message': 'Registry not found'
            }), 404

        with open(registry_file, 'r') as f:
            data = json.load(f)

        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/marketplace/agents', methods=['GET'])
def get_marketplace_agents():
    """Get available agents from marketplace"""
    try:
        agents_dir = MARKETPLACE_DIR / 'agents'
        if not agents_dir.exists():
            return jsonify([]), 200

        agents = []
        for agent_dir in agents_dir.iterdir():
            if agent_dir.is_dir():
                manifest_file = agent_dir / 'manifest.yml'
                if manifest_file.exists():
                    agents.append({
                        'id': agent_dir.name,
                        'path': str(agent_dir),
                        'manifest': str(manifest_file)
                    })

        return jsonify(agents), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== SERVICE MANAGEMENT ====================

@app.route('/api/services/start/<service_name>', methods=['POST'])
def start_service_endpoint(service_name):
    """Start a specific service"""
    if service_name not in SERVICES:
        return jsonify({'error': f'Unknown service: {service_name}'}), 404

    success = start_service(service_name)
    if success:
        return jsonify({
            'message': f'{service_name} started',
            'status': SERVICES[service_name]['status']
        }), 200
    else:
        return jsonify({'error': f'Failed to start {service_name}'}), 500

@app.route('/api/services/status', methods=['GET'])
def services_status():
    """Get status of all services"""
    status = {}
    for name, service in SERVICES.items():
        status[name] = {
            'url': service['url'],
            'status': service['status'],
            'healthy': check_service_health(name),
            'process_alive': service['process'] and service['process'].poll() is None if service['process'] else False
        }
    return jsonify(status), 200

# ==================== WEBSOCKET SUPPORT ====================

@socketio.on('connect')
def handle_connect():
    """Handle WebSocket connection"""
    print(f'Client connected: {request.sid}')
    emit('connected', {'message': 'Connected to AI EcoSystem Gateway'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle WebSocket disconnection"""
    print(f'Client disconnected: {request.sid}')

@socketio.on('subscribe_solana')
def handle_subscribe_solana():
    """Subscribe to Solana Bot updates"""
    # Add client to the subscription room
    join_room('solana_subscribers')

    # Ensure we are connected to the source
    Thread(target=ensure_solana_connection).start()

    emit('solana_subscribed', {'message': 'Subscribed to Solana Bot updates'})

# ==================== FRONTEND SERVING ====================

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    """Serve PWA frontend (in production)"""
    frontend_dir = Path(__file__).parent.parent / 'frontend' / 'dist'

    if frontend_dir.exists():
        if path and (frontend_dir / path).exists():
            return send_from_directory(frontend_dir, path)
        else:
            return send_from_directory(frontend_dir, 'index.html')
    else:
        return jsonify({
            'message': 'AI EcoSystem Gateway',
            'status': 'Frontend not built yet',
            'hint': 'Run: cd frontend && npm run build'
        }), 200

# ==================== STARTUP ====================

def initialize_services():
    """Initialize and start services on gateway startup"""
    print("\n🚀 AI EcoSystem Gateway Starting...")
    print("=" * 50)

    # Auto-start Solana Bot if available
    if SOLANA_BOT_DIR.exists():
        print("📊 Starting Solana Bot...")
        start_service('solana_bot')
        time.sleep(2)

    # Check Agent Zero (assuming it's started separately)
    if check_service_health('agent_zero'):
        print("✅ Agent Zero detected (already running)")
        SERVICES['agent_zero']['status'] = 'healthy'
    else:
        print("⚠️  Agent Zero not detected (start manually if needed)")

    print("=" * 50)
    print("✅ Gateway ready on http://localhost:8080")
    print("📱 API Endpoints:")
    print("   - /health")
    print("   - /api/agent/*")
    print("   - /api/solana/*")
    print("   - /api/marketplace/*")
    print("=" * 50)

if __name__ == '__main__':
    PORT = int(os.environ.get('GATEWAY_PORT', 8080))

    # Initialize services in background
    Thread(target=initialize_services, daemon=True).start()

    # Start Flask + SocketIO server
    socketio.run(
        app,
        host='0.0.0.0',
        port=PORT,
        debug=False,
        allow_unsafe_werkzeug=True
    )
