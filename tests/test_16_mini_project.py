"""Task 18 - integrated end-to-end scenario using page objects, 6 locator strategies,
expect + assert, first/last/nth, dynamic waits, a custom wait, and timeout handling."""
import re

import pytest
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import expect

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from utils.waits import wait_until


@pytest.mark.regression
def test_end_to_end_add_to_cart_flow(page, base_url, credentials, settings):
    print(f"[env={settings.env}] {base_url}")

    # Login: placeholder + role locators (inside LoginPage)
    LoginPage(page, base_url).open().login(*credentials)
    expect(page).to_have_url(re.compile(r".*/inventory\.html"))
    inv = InventoryPage(page)

    # CSS (data-test) and visible text strategies
    expect(page.locator("[data-test='title']")).to_have_text("Products")
    expect(page.get_by_text("Sauce Labs Backpack")).to_be_visible()

    # Collection handling: first / last / nth
    expect(inv.items).to_have_count(6)
    first_name = inv.names.first.inner_text()
    last_name = inv.names.last.inner_text()
    inv.add_to_cart(0)
    inv.add_to_cart(5)

    # Custom wait condition for a dynamic state
    wait_until(
        lambda: inv.cart_badge.count() == 1 and inv.cart_badge.text_content() == "2",
        message="cart badge to show 2 items", page=page,
    )

    # XPath strategy to open the cart
    page.locator("//a[@data-test='shopping-cart-link']").click()
    expect(page).to_have_url(re.compile(r".*/cart\.html"))

    # Timeout handling with a clear failure message
    try:
        expect(inv.names).to_have_count(2)
    except AssertionError as exc:
        pytest.fail(f"Cart did not show 2 items in time: {exc}")

    names = inv.names.all_inner_texts()
    assert names == [first_name, last_name]
    try:
        page.get_by_role("button", name="Checkout").wait_for(state="visible", timeout=3000)
    except PlaywrightTimeoutError:
        pytest.fail("Checkout button never became visible on the cart page")
