"""Task 15 - auto-waiting, locator.wait_for, load states, URL waits. No fixed sleeps."""
import re

from playwright.sync_api import expect

from pages.login_page import LoginPage


def test_builtin_waits(page, base_url, credentials):
    page.goto(base_url, wait_until="domcontentloaded")
    page.wait_for_load_state("load")
    button = page.get_by_role("button", name="Login")
    button.wait_for(state="visible")
    expect(button).to_be_enabled()  # ready before interacting

    login = LoginPage(page, base_url)
    login.username.fill(credentials[0])   # fill/click auto-wait for actionability
    login.password.fill(credentials[1])
    button.click()
    page.wait_for_url(re.compile(r".*/inventory\.html"))
    page.locator(".inventory_list").wait_for(state="visible")
    expect(page.locator(".inventory_item").first).to_be_visible()
