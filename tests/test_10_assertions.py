"""Task 12 - expect() (web-first, auto-retrying) vs plain pytest assert (instant check on Python values).
Prefer expect() for anything on the page: it re-checks until the condition holds or times out, so it
absorbs rendering/network delays. Use assert for values you already extracted/calculated in Python."""
import re

from playwright.sync_api import expect


def test_expect_and_assert(page, base_url):
    page.goto(base_url)
    expect(page).to_have_title("Swag Labs")
    expect(page).to_have_url(re.compile(r"saucedemo\.com"))
    expect(page.locator(".login_logo")).to_be_visible()
    expect(page.locator(".login_logo")).to_have_text("Swag Labs")
    user = page.get_by_placeholder("Username")
    user.fill("abc")
    expect(user).to_have_value("abc")
    expect(page.get_by_role("button", name="Login")).to_be_enabled()

    # pytest assert on an extracted/calculated value
    names = page.locator("[data-test='login-credentials'] , .login_credentials").first.inner_text().splitlines()
    assert len(names) >= 2


def test_disabled_state(page):
    page.set_content("<button id='b' disabled>Go</button><input id='i' value='x'>")
    expect(page.locator("#b")).to_be_disabled()
    expect(page.locator("#i")).to_be_enabled()
