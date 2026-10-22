"""Soft assertions: record failures, keep going, report everything at the end."""
from contextlib import contextmanager


class SoftAssert:
    def __init__(self):
        self.failures: list[str] = []
        self.checks_run = 0

    @contextmanager
    def check(self, label: str):
        self.checks_run += 1
        try:
            yield
        except AssertionError as exc:
            self.failures.append(f"{label}: {str(exc).strip().splitlines()[0] if str(exc).strip() else 'failed'}")

    def assert_all(self):
        if self.failures:
            raise AssertionError(
                f"{len(self.failures)} of {self.checks_run} soft check(s) failed:\n- " + "\n- ".join(self.failures)
            )
