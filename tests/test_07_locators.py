"""Task 9 - five locator strategies; each performs an action and asserts.
Most maintainable: get_by_role / get_by_label / get_by_placeholder / data-test attributes - they
mirror what users (and assistive tech) see, and survive CSS-class or DOM-structure refactors.
XPath is the most brittle (tied to DOM structure); CSS depends on class names unless it targets data-* attrs."""
import pytest
from playwright.sync_api import expect


@pytest.fixture
def login_page(page, base_url):
    page.goto(base_url)
    return page


def test_css_selector(login_page):
    field = login_page.locator("input[data-test='username']")
    field.fill("css_user")
    expect(field).to_have_value("css_user")


def test_xpath_selector(login_page):
    field = login_page.locator("//input[@id='password']")
    field.fill("xpath_pass")
    expect(field).to_have_value("xpath_pass")


def test_visible_text(login_page):
    hint = login_page.get_by_text("Accepted usernames are:")
    expect(hint).to_be_visible()
    hint.click()  # clicking plain text is harmless; proves it is actionable


def test_get_by_role(login_page):
    login_page.get_by_role("button", name="Login").click()
    expect(login_page.locator("[data-test='error']")).to_contain_text("Username is required")


def test_get_by_placeholder(login_page):
    field = login_page.get_by_placeholder("Username")
    field.fill("placeholder_user")
    expect(field).to_have_value("placeholder_user")
