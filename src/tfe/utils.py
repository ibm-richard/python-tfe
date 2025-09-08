from __future__ import annotations
import time


def poll_until(fn, *, interval_s: float = 5.0, timeout_s: int | None = 600):
    start = time.time()
    while True:
        value = fn()
        if value:
            return value
        if timeout_s is not None and (time.time() - start) > timeout_s:
            raise TimeoutError("Timed out")
        time.sleep(interval_s)
