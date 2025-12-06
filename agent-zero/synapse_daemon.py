import time
import os
import sys
import asyncio
import threading
from datetime import datetime

# Ensure we can import from current directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    import schedule
except ImportError:
    print("Installing required package: schedule")
    os.system("pip install schedule")
    import schedule

# Agent Zero Imports
from initialize import initialize
from agent import AgentContext

# Initialize Configuration
print("⚙️ Initializing Agent Zero Core...")
config = initialize()
print("✅ Core Config Loaded")

def run_agent_task(task_prompt):
    """Runs an agent task in a separate event loop to avoid blocking the scheduler"""
    print(f"🤖 [AGENT] Starting Task: {task_prompt}")
    
    async def _execute():
        # Create a new context for this execution
        context = AgentContext(config)
        agent = context.agent0
        
        # Execute the task (monologue)
        # Note: monologue is an infinite loop by default until a tool breaks it
        # We rely on the agent deciding to finish or us setting a timeout mechanism in future
        try:
            await agent.monologue(task_prompt)
        except Exception as e:
            print(f"❌ [AGENT] Error: {e}")
        finally:
            print(f"✅ [AGENT] Task Finished")

    # Run in new event loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(_execute())
    loop.close()

def pulse_check():
    """Basic heartbeat function"""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 💓 Synapse Pulse: System Active")

def morning_routine():
    """Trigger the morning briefing task"""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 🌅 Triggering Morning Routine...")
    task = "Geef me een korte, krachtige briefing over de crypto markten (BTC, SOL) en mijn open taken. Spreek het resultaat hardop uit."
    
    # Start agent in separate thread so daemon doesn't freeze
    thread = threading.Thread(target=run_agent_task, args=(task,))
    thread.start()

def evening_routine():
    """Trigger evening summary"""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 🌙 Triggering Evening Summary...")
    task = "Vat de dag samen en check of er nog urgente zaken zijn. Spreek het resultaat hardop uit."
    thread = threading.Thread(target=run_agent_task, args=(task,))
    thread.start()

# --- SCHEDULER CONFIG ---
print("🚀 Synapse Daemon v1.1 (Integrated) Initialized")
print("📅 Loading Schedule...")

# 1. Heartbeat every hour
schedule.every(1).hours.do(pulse_check)

# 2. Daily Routines
schedule.every().day.at("08:00").do(morning_routine)
schedule.every().day.at("20:00").do(evening_routine)

# 3. Debug Trigger (Optional: Uncomment for instant test)
# run_agent_task("Zeg hallo en bevestig dat je systemen online zijn.")

print("✅ Daemon Running. Press Ctrl+C to stop.")
pulse_check() # Initial check

while True:
    try:
        schedule.run_pending()
        time.sleep(10) # Sleep to save battery
    except KeyboardInterrupt:
        print("\n🛑 Daemon Stopping...")
        break
    except Exception as e:
        print(f"⚠️ Error in daemon loop: {e}")
        time.sleep(60) # Wait before retrying
