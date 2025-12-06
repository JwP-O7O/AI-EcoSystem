#!/usr/bin/env python3
"""
Test script for Batch Executor Tool

This script demonstrates all features of the batch processing system:
- Adding single and multiple tasks
- Priority-based scheduling
- Parallel execution
- Progress tracking
- Result aggregation
- Export functionality
"""

import asyncio
import sys
import time
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from python.tools.batch_executor_tool import (
    BatchExecutor, BatchQueue, BatchTask, Priority, TaskStatus
)


class MockAgent:
    """Mock agent for testing"""
    def __init__(self):
        self.agent_name = "TestAgent"
        self.data = {}

    def get_data(self, key):
        return self.data.get(key)

    def set_data(self, key, value):
        self.data[key] = value

    async def call_utility_llm(self, system, msg):
        # Mock LLM response
        return '{"status": "mock_response"}'


async def test_basic_operations():
    """Test basic add, start, status operations"""
    print("\n" + "="*60)
    print("TEST 1: Basic Operations")
    print("="*60)

    agent = MockAgent()
    executor = BatchExecutor(
        agent=agent,
        name="batch_executor",
        args={},
        message=""
    )

    # Test 1: Add single task
    print("\n1. Adding single task...")
    response = await executor.execute(
        action="add",
        name="Test Task 1",
        function="simulate",
        params={"duration": 1.0},
        priority="high"
    )
    print(response.message)

    # Test 2: Add batch of tasks
    print("\n2. Adding batch of tasks...")
    response = await executor.execute(
        action="add_batch",
        tasks=[
            {
                "name": "Task 2",
                "function": "simulate",
                "params": {"duration": 0.5},
                "priority": "medium"
            },
            {
                "name": "Task 3",
                "function": "simulate",
                "params": {"duration": 0.8},
                "priority": "low"
            },
            {
                "name": "Task 4",
                "function": "simulate",
                "params": {"duration": 0.3},
                "priority": "critical"
            }
        ]
    )
    print(response.message)

    # Test 3: Check status
    print("\n3. Checking status...")
    response = await executor.execute(action="status", detailed=True)
    print(response.message)

    print("\n✅ Basic operations test completed")


async def test_parallel_execution():
    """Test parallel task execution"""
    print("\n" + "="*60)
    print("TEST 2: Parallel Execution")
    print("="*60)

    agent = MockAgent()
    executor = BatchExecutor(
        agent=agent,
        name="batch_executor",
        args={},
        message=""
    )

    # Add multiple tasks with different durations
    print("\n1. Adding 10 tasks with varying durations...")
    tasks = [
        {
            "name": f"Task {i+1}",
            "function": "simulate",
            "params": {"duration": (i % 3) * 0.5 + 0.5},
            "priority": ["low", "medium", "high"][i % 3]
        }
        for i in range(10)
    ]

    await executor.execute(action="add_batch", tasks=tasks)

    # Start execution
    print("\n2. Starting parallel execution (max 3 concurrent)...")
    start_time = time.time()

    await executor.execute(action="start", max_concurrent=3)

    # Wait for completion
    print("\n3. Waiting for tasks to complete...")
    await asyncio.sleep(2)  # Give workers time to start

    # Monitor progress
    for i in range(10):
        response = await executor.execute(action="status", detailed=False)
        print(f"\nProgress check {i+1}:")
        print(response.message)

        # Check if done
        if "Running" in response.message and "🟢" not in response.message:
            break

        await asyncio.sleep(1)

    # Wait a bit more for stragglers
    await asyncio.sleep(3)

    # Final status
    print("\n4. Final status:")
    response = await executor.execute(action="status", detailed=True)
    print(response.message)

    elapsed = time.time() - start_time
    print(f"\nTotal time: {elapsed:.2f}s")
    print("(Should be less than sum of all task durations due to parallelism)")

    print("\n✅ Parallel execution test completed")


async def test_priority_scheduling():
    """Test priority-based task scheduling"""
    print("\n" + "="*60)
    print("TEST 3: Priority Scheduling")
    print("="*60)

    agent = MockAgent()
    executor = BatchExecutor(
        agent=agent,
        name="batch_executor",
        args={},
        message=""
    )

    # Add tasks with different priorities
    print("\n1. Adding tasks with mixed priorities...")
    tasks = [
        {"name": "Low Priority 1", "function": "simulate", "params": {"duration": 0.2}, "priority": "low"},
        {"name": "Critical Task", "function": "simulate", "params": {"duration": 0.2}, "priority": "critical"},
        {"name": "Medium Priority", "function": "simulate", "params": {"duration": 0.2}, "priority": "medium"},
        {"name": "Low Priority 2", "function": "simulate", "params": {"duration": 0.2}, "priority": "low"},
        {"name": "High Priority", "function": "simulate", "params": {"duration": 0.2}, "priority": "high"},
    ]

    await executor.execute(action="add_batch", tasks=tasks)

    # Check queue order
    print("\n2. Queue order (should be: Critical -> High -> Medium -> Low -> Low):")
    queue = executor.queue
    all_tasks = await queue.get_all_tasks()
    for i, task in enumerate(all_tasks, 1):
        print(f"{i}. {task.name} - Priority: {task.priority.name}")

    # Execute with single worker to see order
    print("\n3. Executing with 1 worker to observe order...")
    await executor.execute(action="start", max_concurrent=1)

    # Wait for completion
    await asyncio.sleep(3)

    # Show results in execution order
    print("\n4. Results (execution order):")
    response = await executor.execute(action="results", format="text")
    print(response.message)

    print("\n✅ Priority scheduling test completed")


async def test_error_handling():
    """Test error handling and retry logic"""
    print("\n" + "="*60)
    print("TEST 4: Error Handling & Retry")
    print("="*60)

    agent = MockAgent()
    executor = BatchExecutor(
        agent=agent,
        name="batch_executor",
        args={},
        message=""
    )

    # Add tasks that will fail
    print("\n1. Adding tasks (some will fail)...")
    tasks = [
        {
            "name": "Success Task",
            "function": "simulate",
            "params": {"duration": 0.1},
            "max_retries": 2
        },
        {
            "name": "Failing Task",
            "function": "non_existent_function",
            "params": {},
            "max_retries": 2
        },
        {
            "name": "Another Success",
            "function": "simulate",
            "params": {"duration": 0.1},
            "max_retries": 2
        }
    ]

    await executor.execute(action="add_batch", tasks=tasks)

    # Execute
    print("\n2. Starting execution...")
    await executor.execute(action="start", max_concurrent=2)

    # Wait for completion
    await asyncio.sleep(3)

    # Check results
    print("\n3. Results (showing successes and failures):")
    response = await executor.execute(action="results", format="text")
    print(response.message)

    # Show only failed tasks
    print("\n4. Failed tasks only:")
    response = await executor.execute(action="results", filter_status="failed")
    print(response.message)

    print("\n✅ Error handling test completed")


async def test_export_functionality():
    """Test result export to JSON and CSV"""
    print("\n" + "="*60)
    print("TEST 5: Export Functionality")
    print("="*60)

    agent = MockAgent()
    executor = BatchExecutor(
        agent=agent,
        name="batch_executor",
        args={},
        message=""
    )

    # Add and execute some tasks
    print("\n1. Adding and executing tasks...")
    tasks = [
        {"name": f"Export Test {i}", "function": "simulate", "params": {"duration": 0.1}}
        for i in range(5)
    ]

    await executor.execute(action="add_batch", tasks=tasks)
    await executor.execute(action="start", max_concurrent=3)
    await asyncio.sleep(2)

    # Export to JSON
    print("\n2. Exporting to JSON...")
    response = await executor.execute(
        action="export",
        format="json",
        output_file="test_batch_results.json"
    )
    print(response.message)

    # Export to CSV
    print("\n3. Exporting to CSV...")
    response = await executor.execute(
        action="export",
        format="csv",
        output_file="test_batch_results.csv"
    )
    print(response.message)

    print("\n✅ Export functionality test completed")


async def test_queue_management():
    """Test queue management operations"""
    print("\n" + "="*60)
    print("TEST 6: Queue Management")
    print("="*60)

    agent = MockAgent()
    executor = BatchExecutor(
        agent=agent,
        name="batch_executor",
        args={},
        message=""
    )

    # Add tasks
    print("\n1. Adding 5 tasks...")
    tasks = [
        {"name": f"Task {i}", "function": "simulate", "params": {"duration": 0.5}}
        for i in range(5)
    ]
    await executor.execute(action="add_batch", tasks=tasks)

    # Get initial status
    response = await executor.execute(action="status")
    print("\nInitial status:")
    print(response.message)

    # Cancel a task
    print("\n2. Cancelling task_2...")
    # Get task IDs
    all_tasks = await executor.queue.get_all_tasks()
    if len(all_tasks) >= 2:
        task_id = all_tasks[1].task_id
        response = await executor.execute(action="cancel", task_id=task_id)
        print(response.message)

    # Execute remaining
    print("\n3. Executing remaining tasks...")
    await executor.execute(action="start", max_concurrent=2)
    await asyncio.sleep(3)

    # Check status
    response = await executor.execute(action="status", detailed=True)
    print("\nStatus after execution:")
    print(response.message)

    # Clear completed
    print("\n4. Clearing completed tasks...")
    response = await executor.execute(action="clear")
    print(response.message)

    # Final status
    response = await executor.execute(action="status")
    print("\nFinal status:")
    print(response.message)

    print("\n✅ Queue management test completed")


async def test_stop_execution():
    """Test stopping execution"""
    print("\n" + "="*60)
    print("TEST 7: Stop Execution")
    print("="*60)

    agent = MockAgent()
    executor = BatchExecutor(
        agent=agent,
        name="batch_executor",
        args={},
        message=""
    )

    # Add long-running tasks
    print("\n1. Adding 10 long-running tasks...")
    tasks = [
        {"name": f"Long Task {i}", "function": "simulate", "params": {"duration": 2.0}}
        for i in range(10)
    ]
    await executor.execute(action="add_batch", tasks=tasks)

    # Start execution
    print("\n2. Starting execution...")
    await executor.execute(action="start", max_concurrent=3)
    await asyncio.sleep(1)  # Let some tasks start

    # Check status
    response = await executor.execute(action="status")
    print("\nStatus during execution:")
    print(response.message)

    # Stop execution
    print("\n3. Stopping execution (graceful)...")
    response = await executor.execute(action="stop", graceful=True)
    print(response.message)

    # Wait a bit
    await asyncio.sleep(2)

    # Final status
    response = await executor.execute(action="status", detailed=True)
    print("\nFinal status:")
    print(response.message)

    print("\n✅ Stop execution test completed")


async def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("BATCH EXECUTOR TOOL - COMPREHENSIVE TEST SUITE")
    print("="*60)

    try:
        await test_basic_operations()
        await test_parallel_execution()
        await test_priority_scheduling()
        await test_error_handling()
        await test_export_functionality()
        await test_queue_management()
        await test_stop_execution()

        print("\n" + "="*60)
        print("ALL TESTS COMPLETED SUCCESSFULLY!")
        print("="*60)

    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()


async def interactive_demo():
    """Interactive demonstration"""
    print("\n" + "="*60)
    print("INTERACTIVE BATCH EXECUTOR DEMO")
    print("="*60)

    agent = MockAgent()
    executor = BatchExecutor(
        agent=agent,
        name="batch_executor",
        args={},
        message=""
    )

    # Scenario: Processing multiple data files
    print("\nScenario: Processing 20 data files in parallel")
    print("-" * 60)

    # Add batch of file processing tasks
    print("\n1. Adding 20 file processing tasks...")
    tasks = []
    for i in range(1, 21):
        tasks.append({
            "name": f"Process data_file_{i:02d}.csv",
            "function": "simulate",
            "params": {"duration": 0.2 + (i % 5) * 0.1},
            "priority": "high" if i <= 5 else "medium"
        })

    await executor.execute(action="add_batch", tasks=tasks)
    print(f"✅ Added {len(tasks)} tasks to queue")

    # Show initial status
    print("\n2. Initial queue status:")
    response = await executor.execute(action="status")
    print(response.message)

    # Start execution
    print("\n3. Starting parallel execution (5 workers)...")
    await executor.execute(action="start", max_concurrent=5)

    # Monitor progress
    print("\n4. Monitoring progress...")
    for i in range(10):
        await asyncio.sleep(0.5)
        response = await executor.execute(action="status")
        # Extract just the progress line
        lines = response.message.split('\n')
        for line in lines:
            if 'Progress' in line or 'Completed' in line or 'Running' in line:
                print(f"  {line}")

        # Check if done
        if "Running" in response.message and "🟢" not in response.message:
            break

    # Wait for completion
    await asyncio.sleep(2)

    # Final results
    print("\n5. Final results:")
    response = await executor.execute(action="status", detailed=False)
    print(response.message)

    # Export results
    print("\n6. Exporting results...")
    response = await executor.execute(
        action="export",
        format="json",
        output_file="demo_batch_results.json"
    )
    print(response.message)

    print("\n" + "="*60)
    print("DEMO COMPLETED!")
    print("="*60)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        # Run interactive demo
        asyncio.run(interactive_demo())
    else:
        # Run all tests
        asyncio.run(run_all_tests())
