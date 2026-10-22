"""Custom wait condition: poll a callable until it is truthy, then stop immediately."""
from __future__ import annotations

import time
from typing import Callable


class ConditionTimeoutError(TimeoutError):
    pass


def wait_until(
    condition: Callable[[], bool],
    *,
    timeout_ms: int = 5000,
    poll_ms: int = 100,
    message: str = "condition to become true",
    page=None,
) -> None:
    """Return as soon as `condition()` is truthy; raise a descriptive error after timeout_ms."""
    deadline = time.monotonic() + timeout_ms / 1000
    last_error: Exception | None = None
    while True:
        try:
            if condition():
                return
            last_error = None
        except Exception as exc:  # condition may raise while the UI is still settling
            last_error = exc
        if time.monotonic() >= deadline:
            detail = f" (last error: {last_error!r})" if last_error else ""
            raise ConditionTimeoutError(f"Timed out after {timeout_ms} ms waiting for: {message}{detail}")
        page.wait_for_timeout(poll_ms) if page else time.sleep(poll_ms / 1000)
