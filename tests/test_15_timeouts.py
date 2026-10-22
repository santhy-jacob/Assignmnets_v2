"""Task 17 - timeouts and custom wait conditions."""
import pytest
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import expect

from utils.waits import ConditionTimeoutError, wait_until


def test_missing_element_times_out(page, base_url):
    page.goto(base_url)
    with pytest.raises(PlaywrightTimeoutError) as exc:
        page.locator("#does-not-exist").wait_for(state="visible", timeout=1500)
    assert "does-not-exist" in str(exc.value)


def test_expect_on_missing_element_fails_fast(page, base_url):
    page.goto(base_url)
    with pytest.raises(AssertionError):
        expect(page.locator("#does-not-exist")).to_be_visible(timeout=1000)


def test_custom_wait_succeeds_when_condition_met(inventory_page):
    inventory_page.add_to_cart(0)
    wait_until(
        lambda: inventory_page.cart_badge.count() == 1 and inventory_page.cart_badge.text_content() == "1",
        message="cart badge to show 1",
        page=inventory_page.page,
    )


def test_custom_wait_reports_useful_error(page, base_url):
    page.goto(base_url)
    with pytest.raises(ConditionTimeoutError, match="cart badge to show 99"):
        wait_until(lambda: page.locator(".shopping_cart_badge").count() == 1,
                   timeout_ms=800, message="cart badge to show 99", page=page)
