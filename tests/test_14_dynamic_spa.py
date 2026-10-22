"""Task 16 - dynamic content. The element does not exist until the app finishes loading.
Waiting for the loader to disappear and the result to appear is reliable because it ends the moment the app is
ready (fast on a fast day, patient on a slow one); a fixed sleep is either too short (flaky) or too long (slow)."""
import pytest
from playwright.sync_api import expect

DYNAMIC_URL = "https://the-internet.herokuapp.com/dynamic_loading/2"


@pytest.mark.regression
def test_dynamic_loading_wait_for_condition(page):
    page.goto(DYNAMIC_URL)
    expect(page.locator("#finish")).to_have_count(0)      # initial state: nothing rendered
    page.get_by_role("button", name="Start").click()
    page.locator("#loading").wait_for(state="visible")
    page.locator("#loading").wait_for(state="hidden")       # loading indicator disappears
    expect(page.locator("#finish h4")).to_have_text("Hello World!")


@pytest.mark.regression
def test_dynamic_state_change_in_app(inventory_page):
    expect(inventory_page.cart_badge).to_have_count(0)
    inventory_page.add_to_cart(0)
    expect(inventory_page.cart_badge).to_have_text("1")   # badge appears after the click
