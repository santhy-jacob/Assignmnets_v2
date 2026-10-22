"""Task 3/4 - pytest configuration & settings layer.
Try: pytest -m smoke | pytest tests/test_03_pytest_config.py | pytest tests/test_03_pytest_config.py::test_timeout_override_from_env"""
import time

import pytest
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from config.settings import load_settings


@pytest.mark.smoke
def test_settings_loaded(settings):
    assert settings.base_url.startswith("https://")
    assert settings.navigation_timeout_ms >= settings.default_timeout_ms > 0


def test_timeout_override_from_env(monkeypatch):
    """Changing configuration changes behaviour without touching test logic."""
    monkeypatch.setenv("DEFAULT_TIMEOUT_MS", "1234")
    assert load_settings("dev").default_timeout_ms == 1234


@pytest.mark.regression
def test_configured_default_timeout_is_applied(page, base_url, settings):
    page.goto(base_url)
    start = time.monotonic()
    with pytest.raises(PlaywrightTimeoutError):
        page.locator("#element-that-does-not-exist").click()
    elapsed_ms = (time.monotonic() - start) * 1000
    assert settings.default_timeout_ms * 0.8 <= elapsed_ms <= settings.default_timeout_ms + 3000
