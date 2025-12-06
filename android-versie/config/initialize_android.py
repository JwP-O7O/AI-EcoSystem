"""
Android/Termux Optimized Configuration for Agent Zero
Versie: 1.1 - November 28, 2025

Deze configuratie is specifiek geoptimaliseerd voor:
- Android via Termux
- Geen Docker execution (direct local)
- Lightweight models
- Beperkt geheugen gebruik
- Dynamic Configuration via .env
"""

import sys
import os
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(env_path)

# Voeg parent directory toe aan path voor imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

import models
from agent import AgentConfig
from python.helpers import files

def get_chat_model():
    """
    Determine and return the chat model based on environment variables.
    Priority:
    1. LLM_PROVIDER in .env (openai, anthropic, google, groq, ollama)
    2. Presence of specific API keys
    """
    provider = os.getenv("LLM_PROVIDER", "").lower()

    # --- Google Gemini (Default/Recommended for Free Tier) ---
    if provider == "google" or (not provider and os.getenv("GOOGLE_API_KEY")):
        print("📱 Provider: Google Gemini (Flash)")
        return models.get_google_chat(model_name="gemini-2.5-flash", temperature=0)

    # --- OpenAI ---
    if provider == "openai" or (not provider and os.getenv("OPENAI_API_KEY")):
        print("📱 Provider: OpenAI (GPT-4o-mini)")
        return models.get_openai_chat(model_name="gpt-4o-mini", temperature=0)

    # --- Anthropic ---
    if provider == "anthropic" or (not provider and os.getenv("ANTHROPIC_API_KEY")):
        print("📱 Provider: Anthropic (Claude 3.5 Sonnet)")
        return models.get_anthropic_chat(model_name="claude-3-5-sonnet-20240620", temperature=0)

    # --- Groq ---
    if provider == "groq" or (not provider and os.getenv("GROQ_API_KEY")):
        print("📱 Provider: Groq (Llama 3.2)")
        return models.get_groq_chat(model_name="llama-3.2-90b-text-preview", temperature=0)

    # --- Ollama (Local) ---
    if provider == "ollama":
        print("📱 Provider: Ollama (Local)")
        return models.get_ollama_chat(model_name="llama3.2:3b-instruct-fp16", temperature=0)

    # --- Fallback ---
    print("⚠️ No specific provider found. Defaulting to Google Gemini configuration.")
    return models.get_google_chat(model_name="gemini-2.5-flash", temperature=0)

def get_embedding_model():
    """
    Determine and return the embedding model.
    Tries to match the chat provider to minimize API keys needed.
    """
    provider = os.getenv("LLM_PROVIDER", "").lower()

    if provider == "google" or os.getenv("GOOGLE_API_KEY"):
        return models.get_google_embedding(model_name="models/embedding-001")
    
    if provider == "openai" or os.getenv("OPENAI_API_KEY"):
        return models.get_openai_embedding(model_name="text-embedding-3-small")
        
    if provider == "ollama":
        return models.get_ollama_embedding(model_name="nomic-embed-text")

    # Fallback to Google if key exists, otherwise OpenAI (assumes user has one of them)
    if os.getenv("GOOGLE_API_KEY"):
        return models.get_google_embedding(model_name="models/embedding-001")
    
    if os.getenv("OPENAI_API_KEY"):
        return models.get_openai_embedding(model_name="text-embedding-3-small")

    print("⚠️  Warning: No API key found for embeddings (Google/OpenAI). Vector memory functionalities may fail.")
    return models.get_openai_embedding(model_name="text-embedding-3-small")

def initialize():
    """
    Initialiseer Agent Zero configuratie voor Android/Termux
    """
    print("\n🔧 Initializing Android Configuration...")

    # 1. Select Models
    chat_llm = get_chat_model()
    utility_llm = chat_llm  # Reuse for efficiency
    embedding_llm = get_embedding_model()

    # 2. Agent Configuration
    config = AgentConfig(
        # Models
        chat_model=chat_llm,
        utility_model=utility_llm,
        embeddings_model=embedding_llm,

        # Prompts & Knowledge
        prompts_subdir="default",
        knowledge_subdirs=["default", "custom"],

        # Memory Settings (Optimized for Mobile)
        auto_memory_count=0,  # Disabled for performance
        auto_memory_skip=2,

        # Rate Limiting (Conservative for Mobile/Free Tiers)
        rate_limit_seconds=60,
        rate_limit_requests=15,

        # Message Context Window
        msgs_keep_max=20,
        msgs_keep_start=5,
        msgs_keep_end=10,

        # Response Length
        max_tool_response_length=2000,
        response_timeout_seconds=60,

        # Code Execution - DIRECT TERMUX MODE
        code_exec_docker_enabled=False,
        code_exec_ssh_enabled=False,

        additional={
            "termux_mode": True,
            "android_optimized": True,
            "platform": "android-termux"
        },
    )

    # 3. Register Android-specific tools
    try:
        from android_tools_config import register_android_tools
        config = register_android_tools(config)
    except ImportError:
        print("⚠️  Android tools not loaded (android_tools_config not found)")

    return config