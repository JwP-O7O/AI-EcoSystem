# AI EcoSystem - Native Android App

Complete unified Android app integrating Agent Zero, Solana Trading Bot, and Marketplace.

## 📱 Architecture

**Type:** Progressive Web App (PWA) + Trusted Web Activity (TWA)

```
📱 Android APK (TWA Package)
    ↓
🌐 PWA Frontend (React + TypeScript)
    ↓ HTTP/WebSocket
🔧 Backend Gateway (Python Flask - Port 8080)
    ↓ Reverse Proxy
├─ 🤖 Agent Zero (Flask - Port 5050)
├─ 💰 Solana Bot (Node.js - Port 3000)
└─ 📦 Marketplace (Static JSON)
```

## ✨ Features

- **Agent Zero Chat**: AI assistant interface with real-time streaming
- **Solana Trading Bot**: Live dashboard with P&L tracking, trade history
- **Marketplace**: Browse and install agents and tools
- **Settings**: System health monitoring and configuration
- **Native Navigation**: Bottom tab bar (mobile-optimized)
- **PWA**: Installable, offline-capable, app-like experience

## 🚀 Quick Start

### 1. Start the Application

From the AI-EcoSystem root directory:

```bash
./start-app.sh
```

This will:
- Start the Backend Gateway (port 8080)
- Auto-start Solana Bot (if available)
- Proxy all services through unified API

### 2. Access the App

**Development (with hot reload):**
```bash
cd android-app/frontend
npm install    # First time only
npm run dev
```
Open: http://localhost:3001

**Production (from gateway):**
```bash
cd android-app/frontend
npm install    # First time only
npm run build
```
Open: http://localhost:8080

### 3. Install Dependencies

**Backend:**
```bash
cd android-app/backend
pip install -r requirements.txt
```

**Frontend:**
```bash
cd android-app/frontend
npm install
```

## 📁 Project Structure

```
android-app/
├── backend/
│   ├── gateway.py              # Main API Gateway
│   ├── requirements.txt        # Python dependencies
│   └── start-backend.sh        # Backend launcher
├── frontend/
│   ├── src/
│   │   ├── App.tsx             # Router + TabBar
│   │   ├── pages/              # 4 main pages
│   │   │   ├── AgentChat.tsx
│   │   │   ├── SolanaBot.tsx
│   │   │   ├── Marketplace.tsx
│   │   │   └── Settings.tsx
│   │   ├── components/
│   │   │   └── TabBar.tsx      # Bottom navigation
│   │   └── services/
│   │       └── gatewayApi.ts   # API client
│   ├── public/
│   │   ├── icons/              # App icons (192x192, 512x512)
│   │   └── manifest.json       # PWA manifest (auto-generated)
│   ├── package.json
│   ├── vite.config.ts          # Vite + PWA config
│   └── tsconfig.json
├── .env                        # Configuration
└── README.md                   # This file
```

## 🔧 Configuration

Edit `android-app/.env`:

```bash
# Gateway port
GATEWAY_PORT=8080

# Backend service URLs
AGENT_ZERO_URL=http://localhost:5050
SOLANA_BOT_URL=http://localhost:3000

# Frontend API URL
VITE_API_URL=http://localhost:8080
```

## 📡 API Endpoints

### Gateway (Port 8080)

- `GET /health` - System health check
- `POST /api/agent/*` - Agent Zero proxy
- `POST /api/solana/*` - Solana Bot proxy
- `GET /api/marketplace/*` - Marketplace data
- `GET /api/services/status` - Services status

### Usage Example

```javascript
// Send message to Agent Zero
fetch('http://localhost:8080/api/agent/msg', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    text: 'Hello Agent!',
    context: 'default',
    broadcast: 1
  })
});

// Get Solana Bot status
fetch('http://localhost:8080/api/solana/status')
  .then(r => r.json())
  .then(data => console.log(data));
```

## 🏗️ Development

### Run Development Server

```bash
cd android-app/frontend
npm run dev
```

- Hot reload enabled
- Runs on http://localhost:3001
- Proxies API calls to gateway (8080)

### Build for Production

```bash
cd android-app/frontend
npm run build
```

Output: `frontend/dist/`

### Test Backend Gateway

```bash
cd android-app/backend
python gateway.py
```

Test endpoints:
```bash
curl http://localhost:8080/health
curl http://localhost:8080/api/services/status
```

## 📱 Building Android APK (Optional)

### Using Trusted Web Activity (TWA)

1. **Install Bubblewrap:**
```bash
npm install -g @bubblewrap/cli
```

2. **Create TWA Manifest:**
```json
{
  "packageId": "com.aiecosystem.app",
  "host": "localhost:8080",
  "name": "AI EcoSystem",
  "launcherName": "AI-Eco",
  "display": "standalone",
  "themeColor": "#3b82f6",
  "startUrl": "/",
  "iconUrl": "/icons/icon-512.png"
}
```

3. **Build APK:**
```bash
cd android-app
bubblewrap init --manifest=./twa-manifest.json
bubblewrap build
```

Output: `app-release-signed.apk`

### Install APK

```bash
# Via ADB
adb install app-release-signed.apk

# Or copy to device
cp app-release-signed.apk ~/storage/downloads/
# Install via Android file manager
```

## 🧪 Testing

### Backend Health Check

```bash
curl http://localhost:8080/health | jq
```

Expected output:
```json
{
  "gateway": "healthy",
  "timestamp": 1234567890,
  "services": {
    "agent_zero": { "status": "healthy", "url": "http://localhost:5050" },
    "solana_bot": { "status": "healthy", "url": "http://localhost:3000" },
    "marketplace": { "status": "healthy" }
  }
}
```

### Frontend Testing

1. Open http://localhost:3001 (dev) or http://localhost:8080 (prod)
2. Navigate between tabs: Agent, Trading, Market, Settings
3. Test Agent Chat: Send a message
4. Test Solana Bot: View dashboard, start/stop trading
5. Test Marketplace: Browse agents
6. Test Settings: Check service status

### PWA Testing

1. Open in Chrome/Edge
2. DevTools → Application → Manifest
3. Verify PWA installability
4. Run Lighthouse audit (aim for >90 PWA score)

## 🛠️ Troubleshooting

### Port Already in Use

```bash
# Find process using port 8080
lsof -i :8080

# Kill process
kill -9 <PID>
```

### Frontend Build Fails

```bash
cd android-app/frontend
rm -rf node_modules package-lock.json
npm install
npm run build
```

### Backend Gateway Won't Start

```bash
# Check Python dependencies
cd android-app/backend
pip install -r requirements.txt

# Check ports
netstat -tulpn | grep :8080
netstat -tulpn | grep :5050
netstat -tulpn | grep :3000
```

### Services Not Responding

1. Check service status:
```bash
curl http://localhost:8080/api/services/status
```

2. Start services manually:
```bash
# Agent Zero
cd agent-zero
python run_ui.py

# Solana Bot
cd solana-bot
node scalpingbot.js
```

### APK Won't Install

- Enable "Install from Unknown Sources" in Android settings
- Check APK signing (TWA requires valid signature)
- Verify manifest.json has correct package ID

## 📊 Performance Tips

### Backend

- Use gunicorn for production:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8080 gateway:app
```

### Frontend

- Enable gzip compression
- Lazy load routes (code splitting)
- Cache API responses (service worker)
- Optimize images (< 100KB per icon)

## 🔐 Security

### Development

- CORS enabled for localhost
- No authentication required
- HTTP (not HTTPS)

### Production

**Recommended for deployment:**

1. Enable HTTPS (Cloudflare Tunnel / Nginx reverse proxy)
2. Add authentication (JWT / OAuth)
3. Rate limiting (Flask-Limiter)
4. Input validation
5. Disable CORS wildcard

## 🚢 Deployment

### Local (Termux/Android)

1. Start gateway: `./start-app.sh`
2. Keep Termux running in background
3. Open APK or browser to localhost:8080

### LAN Access

1. Bind gateway to 0.0.0.0:
```python
socketio.run(app, host='0.0.0.0', port=8080)
```

2. Update TWA manifest with LAN IP:
```json
{
  "host": "192.168.1.100:8080"
}
```

3. Rebuild APK

### Cloud (Optional)

Use Cloudflare Tunnel for public access:

```bash
pkg install cloudflared
cloudflared tunnel --url http://localhost:8080
```

Update TWA manifest with public URL.

## 📚 Tech Stack

**Frontend:**
- React 18 + TypeScript
- Vite (build tool)
- TailwindCSS (styling)
- React Router (navigation)
- Socket.IO Client (WebSocket)
- Lucide React (icons)
- Vite PWA Plugin

**Backend:**
- Python 3.11+
- Flask 3.0 (web server)
- Flask-CORS (CORS support)
- Flask-SocketIO (WebSocket)
- Requests (HTTP proxy)

**Integration:**
- Agent Zero (AI assistant)
- Solana Trading Bot (Node.js)
- Marketplace (static JSON)

## 🎯 Next Steps

### Phase 1: MVP (Current)
- ✅ Backend Gateway
- ✅ PWA Frontend
- ✅ 4 Pages (Agent, Solana, Marketplace, Settings)
- ✅ API Integration
- ⏳ TWA APK Build

### Phase 2: Enhancements
- [ ] Real-time WebSocket integration
- [ ] Notifications (trading alerts)
- [ ] Offline mode (IndexedDB cache)
- [ ] Dark/Light theme toggle
- [ ] Voice input (speech-to-text)

### Phase 3: Advanced
- [ ] Multi-agent support
- [ ] Biometric authentication
- [ ] Home screen widgets
- [ ] Backup/sync (cloud)
- [ ] Analytics dashboard

## 🤝 Contributing

This is a personal/internal project. For issues or improvements, see the main AI-EcoSystem repository.

## 📄 License

Same as parent project (AI-EcoSystem).

## 📞 Support

- Agent Zero: https://github.com/frdel/agent-zero
- Discord: https://discord.gg/B8KZKNsPpj
- Issues: Check PROJECT_HISTORY_AND_STATUS.md

---

**Built with ❤️ for Agent Zero Community**
