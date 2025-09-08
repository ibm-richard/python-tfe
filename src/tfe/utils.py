from __future__ import annotations

import time
from typing import Callable


def poll_until(
    fn: Callable[[], bool],
    *,
    interval_s: float = 5.0,
    timeout_s: float | None = 600,
) -> bool:
    start = time.time()
    while True:
        value = fn()
        if value:
            return True
        if timeout_s is not None and (time.time() - start) > timeout_s:
            raise TimeoutError("Timed out")
        time.sleep(interval_s)
