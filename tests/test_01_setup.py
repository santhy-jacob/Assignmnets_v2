"""Task 1 - installation check: launch a browser, open a site, validate the title."""
import pytest
from playwright.sync_api import expect


@pytest.mark.smoke
def test_homepage_title(page, base_url):
    page.goto(base_url)
    expect(page).to_have_title("Swag Labs")


def test_launch_browser_manually(playwright, browser_name, base_url):
    """Same check without the page fixture, to show what the plugin does for you."""
    browser = getattr(playwright, browser_name).launch()
    try:
        page = browser.new_page()
        page.goto(base_url)
        assert page.title() == "Swag Labs"
    finally:
        browser.close()
