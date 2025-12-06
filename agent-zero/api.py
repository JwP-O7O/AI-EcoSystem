import sys
import os
import asyncio
import json
import uuid
from typing import Dict, Optional, List
from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Add current directory to sys.path to allow imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from initialize import initialize
from agent import AgentContext
from python.helpers import log

# --- DATA MODELS ---
class ChatRequest(BaseModel):
    message: str
    agent_role: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    agent_name: str

class SystemStatus(BaseModel):
    status: str
    active_agents: int
    version: str = "2.0.0"

# --- SESSION MANAGER ---
class SessionManager:
    def __init__(self):
        self.active_contexts: Dict[str, AgentContext] = {}
        self.config = None

    def load_config(self):
        print("⚙️ Loading Agent Zero Configuration...")
        self.config = initialize()
        print("✅ Configuration Loaded.")

    def get_or_create_context(self, session_id: str) -> AgentContext:
        if session_id not in self.active_contexts:
            print(f"✨ Creating new context for session: {session_id}")
            self.active_contexts[session_id] = AgentContext(self.config, id=session_id)
        return self.active_contexts[session_id]

    def remove_context(self, session_id: str):
        if session_id in self.active_contexts:
            AgentContext.remove(session_id)
            del self.active_contexts[session_id]

session_manager = SessionManager()

# --- LIFECYCLE ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    session_manager.load_config()
    yield
    # Shutdown
    print("🛑 Shutting down Synapse API...")

# --- APP SETUP ---
app = FastAPI(
    title="Synapse OS API",
    description="Backend API for Agent Zero AI EcoSystem",
    version="2.0.0",
    lifespan=lifespan
)

# CORS - Allow Frontend (localhost:3001)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001", "http://127.0.0.1:3001", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- WEBSOCKET MANAGER ---
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

ws_manager = ConnectionManager()

# --- ENDPOINTS ---

@app.get("/")
async def root():
    return {"message": "Synapse OS v2.0 Online", "docs": "/docs"}

@app.get("/health", response_model=SystemStatus)
async def health_check():
    return SystemStatus(
        status="operational", 
        active_agents=len(session_manager.active_contexts)
    )

@app.post("/chat/{session_id}", response_model=ChatResponse)
async def chat_endpoint(session_id: str, request: ChatRequest):
    """
    Send a message to the agent and wait for the full response (Synchronous Mode).
    For streaming, use WebSocket.
    """
    context = session_manager.get_or_create_context(session_id)
    agent = context.agent0

    # Handle role switching (optional)
    if request.agent_role:
        # Logic to switch role would go here (requires restart of context usually)
        pass

    print(f"📩 Message from {session_id}: {request.message}")
    
    try:
        # Execute the agent
        # We use the result() method from our patched defer.py which is thread-safe
        response_task = context.communicate(request.message)
        
        # Await the result
        # Note: context.communicate returns a DeferredTask. 
        # We need to await its result() method which returns the actual string.
        response_text = await response_task.result()
        
        return ChatResponse(
            response=str(response_text),
            agent_name=agent.agent_name
        )
    except Exception as e:
        print(f"❌ Error in chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await ws_manager.connect(websocket)
    try:
        await websocket.send_text(f"Connected to Synapse OS as {client_id}")
        context = session_manager.get_or_create_context(client_id)
        
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Processing: {data}")
            
            # Future: Hook into agent stream and send chunks
            # For now, simple echo or blocking call
            try:
                response_task = context.communicate(data)
                result = await response_task.result()
                await websocket.send_text(json.dumps({
                    "type": "response",
                    "content": str(result)
                }))
            except Exception as e:
                await websocket.send_text(f"Error: {str(e)}")

    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
        # Optional: Clean up context
        # session_manager.remove_context(client_id)
