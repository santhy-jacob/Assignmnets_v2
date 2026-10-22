"""Shared fixtures. Browser choice comes from pytest-playwright (--browser / --headed);
environment comes from --env or TEST_ENV; everything else from config/settings.py."""
import pytest
from playwright.sync_api import expect

from config.settings import MissingCredentialsError, get_credentials, load_settings
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from utils.soft_assert import SoftAssert


def pytest_addoption(parser):
    parser.addoption("--env", action="store", default=None, help="Environment: dev | qa | staging")


def pytest_report_header(config):
    s = load_settings(config.getoption("--env"))
    return f"test environment: {s.env} | base url: {s.base_url}"  # never print secrets


@pytest.fixture(scope="session")
def settings(pytestconfig):
    return load_settings(pytestconfig.getoption("--env"))


@pytest.fixture(scope="session", autouse=True)
def _expect_timeout(settings):
    expect.set_options(timeout=settings.expect_timeout_ms)


@pytest.fixture(scope="session")
def base_url(settings):
    return settings.base_url


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args, settings, pytestconfig):
    args = dict(browser_type_launch_args)
    if not pytestconfig.getoption("--headed"):
        args["headless"] = settings.headless
    if settings.slow_mo_ms and not args.get("slow_mo"):
        args["slow_mo"] = settings.slow_mo_ms
    return args


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, settings):
    return {
        **browser_context_args,
        "viewport": {"width": settings.viewport_width, "height": settings.viewport_height},
    }


@pytest.fixture
def context(context, settings):
    """Extends the plugin's context fixture with timeouts from configuration."""
    context.set_default_timeout(settings.default_timeout_ms)
    context.set_default_navigation_timeout(settings.navigation_timeout_ms)
    return context


# --- Custom context/page fixtures --------------------------------------------------------
# Function scope: a fresh BrowserContext per test = isolated cookies/storage and cheap to
# create. The expensive Browser is shared (session scope, provided by pytest-playwright).
@pytest.fixture
def isolated_context(browser, browser_context_args, settings):
    ctx = browser.new_context(**browser_context_args)
    ctx.set_default_timeout(settings.default_timeout_ms)
    ctx.set_default_navigation_timeout(settings.navigation_timeout_ms)
    yield ctx
    ctx.close()


@pytest.fixture
def isolated_page(isolated_context):
    return isolated_context.new_page()


# --- Credentials & helpers ---------------------------------------------------------------
@pytest.fixture(scope="session")
def credentials(settings):
    try:
        return get_credentials()
    except MissingCredentialsError as exc:
        pytest.skip(str(exc))


@pytest.fixture
def inventory_page(page, base_url, credentials):
    LoginPage(page, base_url).open().login(*credentials)
    expect(page).to_have_url(__import__("re").compile(r".*/inventory\.html"))
    return InventoryPage(page)


@pytest.fixture
def soft():
    return SoftAssert()
