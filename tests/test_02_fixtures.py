"""Task 2 - Browser -> BrowserContext -> Page.

Browser  : one running browser process (expensive; shared per session).
Context  : an isolated "incognito-like" profile (own cookies/localStorage/cache); cheap, one per test.
Page     : one tab inside a context.
"""
import pytest
from urllib.parse import urlparse
from playwright.sync_api import expect


@pytest.mark.smoke
def test_page_fixture_navigates(page, base_url):
    page.goto(base_url)
    expect(page.get_by_role("button", name="Login")).to_be_visible()


def test_isolated_page_fixture(isolated_page, base_url):
    isolated_page.goto(base_url)
    expect(isolated_page).to_have_title("Swag Labs")


def test_state_written_in_first_test(isolated_page, base_url):
    isolated_page.goto(base_url)
    isolated_page.evaluate("localStorage.setItem('session', 'from-test-1')")
    assert isolated_page.evaluate("localStorage.getItem('session')") == "from-test-1"


def test_state_not_visible_in_second_test(isolated_page, base_url):
    isolated_page.goto(base_url)
    assert isolated_page.evaluate("localStorage.getItem('session')") is None  # new context = clean state


def test_two_contexts_in_one_test_are_isolated(browser, browser_context_args, base_url):
    origin = "{0.scheme}://{0.netloc}".format(urlparse(base_url))
    ctx_a, ctx_b = browser.new_context(**browser_context_args), browser.new_context(**browser_context_args)
    try:
        a, b = ctx_a.new_page(), ctx_b.new_page()
        a.goto(base_url)
        b.goto(base_url)
        ctx_a.add_cookies([{"name": "sid", "value": "A", "url": origin}])
        a.evaluate("localStorage.setItem('user', 'alice')")
        assert a.evaluate("localStorage.getItem('user')") == "alice"
        assert b.evaluate("localStorage.getItem('user')") is None
        assert [c for c in ctx_b.cookies() if c["name"] == "sid"] == []
    finally:
        ctx_a.close()
        ctx_b.close()
