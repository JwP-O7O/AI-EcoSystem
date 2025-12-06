import sys
import os
import asyncio
import time

# Add current directory to path
sys.path.append(os.getcwd())

from python.helpers.defer import DeferredTask

async def test_task(name, duration):
    print(f"Task {name} started")
    await asyncio.sleep(duration)
    print(f"Task {name} finished")
    return f"Result from {name}"

def main():
    print("Testing DeferredTask fix...")
    
    # Create a task
    task = DeferredTask(test_task, "A", 2)
    
    print("Task created, waiting for is_alive...")
    time.sleep(0.5)
    
    if task.is_alive():
        print("✅ Task is running correctly (is_alive=True)")
    else:
        print("❌ Task failed to start")
        return

    print("Waiting for result...")
    try:
        result = task.result_sync(timeout=5)
        print(f"✅ Task result: {result}")
    except Exception as e:
        print(f"❌ Error retrieving result: {e}")

if __name__ == "__main__":
    main()
