"""Task 10 - fill, press, clear/replace, keyboard shortcut."""
from playwright.sync_api import expect


def test_typing_and_keyboard_actions(page, base_url):
    page.goto(base_url)
    user = page.get_by_placeholder("Username")
    pwd = page.get_by_placeholder("Password")

    user.fill("first_value")
    expect(user).to_have_value("first_value")

    user.clear()
    user.fill("replaced_value")
    expect(user).to_have_value("replaced_value")

    user.press("Tab")  # keyboard navigation moves focus
    expect(pwd).to_be_focused()

    user.focus()
    page.keyboard.press("ControlOrMeta+A")  # shortcut: select all
    page.keyboard.press("Backspace")
    expect(user).to_have_value("")

    user.press("Enter")  # submits the form
    expect(page.locator("[data-test='error']")).to_contain_text("Username is required")
