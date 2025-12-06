import asyncio
import threading
from concurrent.futures import Future
from typing import Any, Callable, Optional, Coroutine

# Global event loop for background tasks
_loop_thread = None
_loop = None
_lock = threading.Lock()

def _start_background_loop():
    global _loop
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        _loop = loop
        loop.run_forever()
    except Exception as e:
        print(f"Background loop error: {e}")

def get_background_loop():
    global _loop_thread, _loop
    with _lock:
        if _loop_thread is None:
            _loop_thread = threading.Thread(target=_start_background_loop, daemon=True)
            _loop_thread.start()
            # Wait for loop to be initialized
            import time
            start = time.time()
            while _loop is None:
                if time.time() - start > 5:
                    raise RuntimeError("Failed to start background loop")
                time.sleep(0.01)
    return _loop

class DeferredTask:
    def __init__(self, func: Callable[..., Coroutine[Any, Any, Any]], *args: Any, **kwargs: Any):
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.loop = get_background_loop()
        self._future: Optional[Future] = None
        self._start_task()

    def _start_task(self):
        # Schedule the coroutine in the background loop
        # This returns a concurrent.futures.Future which is thread-safe
        self._future = asyncio.run_coroutine_threadsafe(self._run(), self.loop)

    async def _run(self):
        try:
            return await self.func(*self.args, **self.kwargs)
        except asyncio.CancelledError:
            pass
        except Exception as e:
            print(f"Task execution error: {e}")
            raise e

    def is_ready(self) -> bool:
        return self._future.done() if self._future else False

    def result_sync(self, timeout: Optional[float] = None) -> Any:
        if not self._future:
            raise RuntimeError("Task hasn't been started")
        try:
            return self._future.result(timeout)
        except TimeoutError:
            raise TimeoutError("The task did not complete within the specified timeout.")

    async def result(self, timeout: Optional[float] = None) -> Any:
        """
        Await the result in the current asyncio loop (e.g. main loop),
        bridging from the background thread's future.
        """
        if not self._future:
            raise RuntimeError("Task hasn't been started")
            
        # Wrap the concurrent.futures.Future in an asyncio.Future for the current loop
        loop = asyncio.get_running_loop()
        return await asyncio.wrap_future(self._future, loop=loop)

    def kill(self) -> None:
        if self._future:
            self._future.cancel()

    def is_alive(self) -> bool:
        return self._future is not None and not self._future.done()

    def restart(self) -> None:
        self.kill()
        self._start_task()

# Simple alias for compatibility
Process = DeferredTask