# Batch Executor - System Architecture

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        Agent Zero                                │
│                                                                   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    Batch Executor Tool                     │  │
│  │                                                             │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │  │
│  │  │   Actions    │  │    Queue     │  │   Executor   │    │  │
│  │  │              │  │              │  │              │    │  │
│  │  │ - add        │  │ - Priority   │  │ - Workers    │    │  │
│  │  │ - add_batch  │  │   sorting    │  │ - Parallel   │    │  │
│  │  │ - start      │  │ - Task mgmt  │  │   execution  │    │  │
│  │  │ - stop       │  │ - Status     │  │ - Retry      │    │  │
│  │  │ - status     │  │   tracking   │  │   logic      │    │  │
│  │  │ - results    │  │              │  │              │    │  │
│  │  │ - export     │  │              │  │              │    │  │
│  │  │ - clear      │  │              │  │              │    │  │
│  │  │ - cancel     │  │              │  │              │    │  │
│  │  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘    │  │
│  │         │                 │                 │             │  │
│  │         └─────────────────┴─────────────────┘             │  │
│  │                           │                                │  │
│  └───────────────────────────┼────────────────────────────────┘  │
│                              │                                   │
│  ┌───────────────────────────┼────────────────────────────────┐  │
│  │                    Task Execution Layer                    │  │
│  │                                                             │  │
│  │  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌─────────┐ │  │
│  │  │   Code    │  │ Knowledge │  │  Memory   │  │ Custom  │ │  │
│  │  │ Execution │  │   Search  │  │    Ops    │  │Function │ │  │
│  │  └───────────┘  └───────────┘  └───────────┘  └─────────┘ │  │
│  │                                                             │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                                                                   │
└───────────────────────────────────────────────────────────────────┘
```

## 🔄 Data Flow

```
User Request
     │
     ▼
┌─────────────────┐
│  add / add_batch│
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│     BatchQueue          │
│                         │
│  ┌─────────────────┐   │
│  │ Priority Sorting│   │
│  │                 │   │
│  │ CRITICAL  ████  │   │
│  │ HIGH      ███   │   │
│  │ MEDIUM    ██    │   │
│  │ LOW       █     │   │
│  └─────────────────┘   │
└──────────┬──────────────┘
           │
           ▼
┌───────────────────────────┐
│   start (trigger)         │
└───────────┬───────────────┘
            │
            ▼
┌────────────────────────────────────┐
│      Executor (Async Loop)         │
│                                    │
│  ┌────────────────────────────┐   │
│  │   Worker Pool (1-N)        │   │
│  │                            │   │
│  │  Worker 1  ─────> Task A   │   │
│  │  Worker 2  ─────> Task B   │   │
│  │  Worker 3  ─────> Task C   │   │
│  │     ...                    │   │
│  │  Worker N  ─────> Task N   │   │
│  │                            │   │
│  └────────┬───────────────────┘   │
│           │                       │
│           ▼                       │
│  ┌────────────────┐               │
│  │  Task Execute  │               │
│  │                │               │
│  │  Success?      │               │
│  │    Yes → Done  │               │
│  │    No → Retry  │               │
│  └────────┬───────┘               │
│           │                       │
└───────────┼───────────────────────┘
            │
            ▼
┌────────────────────────┐
│   Results Collection   │
│                        │
│  ┌──────────────────┐  │
│  │ Status: COMPLETE │  │
│  │ Status: FAILED   │  │
│  │ Errors tracking  │  │
│  │ Execution times  │  │
│  └──────────────────┘  │
└───────────┬────────────┘
            │
            ▼
┌────────────────────────┐
│   status / results     │
│   export (JSON/CSV)    │
└────────────────────────┘
            │
            ▼
         Output
```

## 📊 Class Hierarchy

```
BatchExecutor (Tool)
    │
    ├── execute(action, **kwargs) → Response
    │   │
    │   ├── _add_task()
    │   ├── _add_batch()
    │   ├── _start_execution()
    │   │   └── _run_executor()
    │   │       └── _worker(worker_id)
    │   │           └── _execute_task()
    │   │               ├── _execute_code_tool()
    │   │               ├── _execute_knowledge_tool()
    │   │               ├── _execute_memory_tool()
    │   │               ├── _execute_custom_function()
    │   │               └── _execute_agent_tool()
    │   │
    │   ├── _stop_execution()
    │   ├── _get_status()
    │   ├── _get_results()
    │   ├── _export_results()
    │   ├── _clear_completed()
    │   └── _cancel_task()
    │
    └── queue: BatchQueue
        │
        ├── tasks: List[BatchTask]
        │   │
        │   └── BatchTask
        │       ├── task_id
        │       ├── name
        │       ├── function
        │       ├── params
        │       ├── priority: Priority
        │       ├── status: TaskStatus
        │       ├── result
        │       ├── error
        │       └── execution_time
        │
        ├── add_task()
        ├── get_next_task()
        ├── update_task()
        ├── cancel_task()
        └── get_stats() → BatchStats
            │
            └── BatchStats
                ├── total_tasks
                ├── queued/running/completed/failed
                ├── progress_percentage
                ├── average_task_time
                └── estimated_time_remaining
```

## 🔀 State Machine

```
Task Lifecycle:

    ┌─────────┐
    │ Created │
    └────┬────┘
         │
         ▼
    ┌─────────┐
    │ QUEUED  │◄──────────┐
    └────┬────┘           │
         │                │
         │ get_next_task()│ retry
         │                │
         ▼                │
    ┌─────────┐           │
    │ RUNNING │           │
    └────┬────┘           │
         │                │
         ├─ Success ──────┼────────┐
         │                │        │
         └─ Failure ──────┘        │
            (retry_count < max)    │
                                   │
                                   ▼
                              ┌──────────┐
                              │COMPLETED │
                              └──────────┘

    Or:

    ┌─────────┐
    │ QUEUED  │
    └────┬────┘
         │
         │ user cancels
         │
         ▼
    ┌───────────┐
    │ CANCELLED │
    └───────────┘

    Or:

    ┌─────────┐
    │ RUNNING │
    └────┬────┘
         │
         │ max retries exceeded
         │
         ▼
    ┌─────────┐
    │ FAILED  │
    └─────────┘
```

## ⚙️ Execution Model

### Parallel Execution

```
Time →

Worker 1: [Task A ]     [Task D ]          [Task G]
Worker 2:   [Task B]         [Task E]     [Task H ]
Worker 3:    [Task C ]         [Task F] [Task I  ]

Legend:
[      ] = Task execution time
Workers run concurrently (asyncio)
Tasks pulled from priority queue
```

### Sequential vs Parallel

```
Sequential (1 worker):
Total Time = T1 + T2 + T3 + ... + Tn

[T1][T2][T3][T4][T5][T6][T7][T8][T9][T10]
|_______________________________________|
         Total: 10 × T_avg


Parallel (3 workers):
Total Time ≈ (T1 + T2 + ... + Tn) / num_workers

Worker 1: [T1][T4][T7][T10]
Worker 2: [T2][T5][T8]
Worker 3: [T3][T6][T9]
          |____________|
           Total: ~3.3 × T_avg

Speedup = 10 / 3.3 = ~3x faster
```

## 🧩 Component Interactions

```
┌────────────────────────────────────────────────────────┐
│                    User / Agent                         │
└───────────────┬────────────────────────────────────────┘
                │
                │ Tool Call (action + params)
                ▼
┌────────────────────────────────────────────────────────┐
│              BatchExecutor.execute()                    │
│                                                         │
│  Route action to handler:                              │
│  ┌────────────────────────────────────────────┐        │
│  │ if action == "add": _add_task()            │        │
│  │ if action == "start": _start_execution()   │        │
│  │ if action == "status": _get_status()       │        │
│  │ etc.                                       │        │
│  └────────────────────────────────────────────┘        │
└───────────────┬────────────────────────────────────────┘
                │
                ▼
┌────────────────────────────────────────────────────────┐
│                   BatchQueue                            │
│                                                         │
│  Manages task list with async locking:                 │
│  ┌────────────────────────────────────────────┐        │
│  │ async with self._lock:                     │        │
│  │     # Add/remove/update tasks              │        │
│  │     self.tasks.sort(by=priority, time)     │        │
│  └────────────────────────────────────────────┘        │
└───────────────┬────────────────────────────────────────┘
                │
                │ (on start)
                ▼
┌────────────────────────────────────────────────────────┐
│              _run_executor() (async)                    │
│                                                         │
│  Creates worker tasks:                                 │
│  ┌────────────────────────────────────────────┐        │
│  │ workers = [                                │        │
│  │     create_task(_worker(0)),               │        │
│  │     create_task(_worker(1)),               │        │
│  │     ...                                    │        │
│  │     create_task(_worker(N))                │        │
│  │ ]                                          │        │
│  │ await gather(*workers)                     │        │
│  └────────────────────────────────────────────┘        │
└───────────────┬────────────────────────────────────────┘
                │
                │ Each worker loops:
                ▼
┌────────────────────────────────────────────────────────┐
│              _worker(worker_id) (async)                 │
│                                                         │
│  Worker loop:                                          │
│  ┌────────────────────────────────────────────┐        │
│  │ while is_running:                          │        │
│  │     task = await queue.get_next_task()     │        │
│  │     if task is None: break                 │        │
│  │                                            │        │
│  │     try:                                   │        │
│  │         result = await _execute_task(task) │        │
│  │         update(COMPLETED, result)          │        │
│  │     except Exception as e:                 │        │
│  │         if retry_count < max_retries:      │        │
│  │             requeue(task)                  │        │
│  │         else:                              │        │
│  │             update(FAILED, error)          │        │
│  └────────────────────────────────────────────┘        │
└───────────────┬────────────────────────────────────────┘
                │
                ▼
┌────────────────────────────────────────────────────────┐
│           _execute_task(task) (async)                   │
│                                                         │
│  Dispatch based on function:                           │
│  ┌────────────────────────────────────────────┐        │
│  │ if function == "code_execution":           │        │
│  │     return await _execute_code_tool()      │        │
│  │ elif function == "simulate":               │        │
│  │     await sleep(duration)                  │        │
│  │ else:                                      │        │
│  │     return await _execute_agent_tool()     │        │
│  └────────────────────────────────────────────┘        │
└───────────────┬────────────────────────────────────────┘
                │
                │ Result
                ▼
┌────────────────────────────────────────────────────────┐
│           Queue.update_task()                           │
│                                                         │
│  Update task status and result:                       │
│  ┌────────────────────────────────────────────┐        │
│  │ task.status = COMPLETED                    │        │
│  │ task.result = result                       │        │
│  │ task.completed_at = time.time()            │        │
│  └────────────────────────────────────────────┘        │
└────────────────────────────────────────────────────────┘
```

## 📦 Data Structures

### BatchTask
```python
@dataclass
class BatchTask:
    task_id: str              # Unique identifier
    name: str                 # Human-readable name
    function: str             # Function to execute
    params: Dict[str, Any]    # Function parameters
    priority: Priority        # Execution priority
    status: TaskStatus        # Current status
    created_at: float         # Timestamp
    started_at: Optional[float]
    completed_at: Optional[float]
    result: Optional[Any]     # Execution result
    error: Optional[str]      # Error message (if failed)
    retry_count: int          # Current retry count
    max_retries: int          # Maximum retries allowed
```

### BatchStats
```python
@dataclass
class BatchStats:
    total_tasks: int
    queued: int
    running: int
    completed: int
    failed: int
    cancelled: int
    start_time: Optional[float]
    end_time: Optional[float]
    total_execution_time: float
    average_task_time: float

    @property
    def progress_percentage(self) -> float

    @property
    def estimated_time_remaining(self) -> Optional[float]
```

## 🔐 Thread Safety

### Async Locking Strategy
```python
class BatchQueue:
    def __init__(self):
        self._lock = asyncio.Lock()

    async def add_task(...):
        async with self._lock:
            # Thread-safe task addition
            self.tasks.append(task)
            self.tasks.sort(...)

    async def get_next_task(...):
        async with self._lock:
            # Thread-safe task retrieval
            for task in self.tasks:
                if task.status == QUEUED:
                    task.status = RUNNING
                    return task
```

## 🎯 Design Patterns

### 1. Strategy Pattern
- Different execution strategies for different function types
- `_execute_code_tool()`, `_execute_knowledge_tool()`, etc.

### 2. Producer-Consumer Pattern
- Queue produces tasks
- Workers consume tasks
- Asyncio-based coordination

### 3. Observer Pattern
- Real-time status updates
- Progress tracking
- Event notifications

### 4. Command Pattern
- Actions as commands (add, start, stop, etc.)
- Encapsulated operations

## 🚀 Performance Optimizations

### 1. Asyncio-based Parallelism
```python
# Non-blocking I/O
await asyncio.gather(*workers)

# Efficient task switching
await asyncio.sleep(0.1)
```

### 2. Priority Queue
```python
# O(n log n) sorting
self.tasks.sort(key=lambda t: (-t.priority.value, t.created_at))

# O(n) next task retrieval
for task in self.tasks:
    if task.status == QUEUED:
        return task
```

### 3. Lazy Evaluation
```python
# Only calculate stats when requested
@property
def progress_percentage(self):
    return (finished / total) * 100
```

### 4. Resource Limiting
```python
# Configurable max concurrent tasks
max_concurrent = 5  # Prevent resource exhaustion
```

## 📈 Scalability

### Horizontal Scaling
```
Current: Single agent, multiple workers
Future:  Multiple agents, distributed queue

Agent 1: Workers 1-5
Agent 2: Workers 6-10
Agent 3: Workers 11-15

Shared Queue (Redis/Database)
```

### Vertical Scaling
```
Increase workers within single agent:
- max_concurrent: 5 → 20 (for I/O-bound)
- max_concurrent: 2 → 8 (for CPU-bound)
```

## 🔍 Monitoring & Observability

### Metrics Collected
1. **Task Metrics**
   - Total tasks
   - Status breakdown
   - Success/failure rates

2. **Performance Metrics**
   - Average execution time
   - Wait time
   - Queue depth

3. **System Metrics**
   - Active workers
   - Resource usage
   - Throughput

### Real-time Monitoring
```python
# Status polling
{
  "action": "status",
  "detailed": true
}

# Results filtering
{
  "action": "results",
  "filter_status": "failed"
}
```

## 📝 Summary

The Batch Executor architecture provides:

✅ **Scalable**: Handle 1-1000+ tasks
✅ **Efficient**: Asyncio-based parallelism
✅ **Reliable**: Retry logic, error handling
✅ **Observable**: Real-time monitoring
✅ **Flexible**: Support multiple function types
✅ **Safe**: Thread-safe operations
✅ **Fast**: Optimized data structures

**Core Principle**: Simple, efficient, and reliable parallel task execution.
