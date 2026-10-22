"""Task 13 - soft assertions (utils/soft_assert.py).
Hard assertion: stops the test at the first failure. Soft: records the failure, continues, reports all at the end.
Use soft only when later checks give useful diagnostics independent of earlier ones (e.g. many UI properties)."""
from playwright.sync_api import expect


def test_soft_validation_of_login_page(page, base_url, soft):
    page.goto(base_url)
    with soft.check("title"):
        expect(page).to_have_title("Swag Labs")
    with soft.check("logo text"):
        expect(page.locator(".login_logo")).to_have_text("Swag Labs")
    with soft.check("username placeholder"):
        expect(page.get_by_placeholder("Username")).to_be_visible()
    with soft.check("login button enabled"):
        expect(page.get_by_role("button", name="Login")).to_be_enabled()
    soft.assert_all()


def test_soft_assert_collects_failures_and_continues(page, base_url, soft):
    page.goto(base_url)
    with soft.check("wrong title (expected to fail)"):
        expect(page).to_have_title("Not the title", timeout=500)
    with soft.check("logo text (should still run)"):
        expect(page.locator(".login_logo")).to_have_text("Swag Labs")
    with soft.check("wrong placeholder (expected to fail)"):
        expect(page.get_by_placeholder("Username")).to_have_attribute("placeholder", "Nope", timeout=500)
    with soft.check("button visible (should still run)"):
        expect(page.get_by_role("button", name="Login")).to_be_visible()

    assert soft.checks_run == 4          # execution did not stop at the first failure
    assert len(soft.failures) == 2       # both failures were collected
