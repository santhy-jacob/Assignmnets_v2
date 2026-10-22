"""Task 6 - environment selection: pytest --env dev|qa|staging (or TEST_ENV=qa)."""
import pytest
from playwright.sync_api import expect

from config.settings import VALID_ENVS, load_settings


def test_each_environment_has_its_own_base_url():
    urls = {env: load_settings(env).base_url for env in VALID_ENVS}
    assert len(set(urls.values())) == len(VALID_ENVS), urls


@pytest.mark.smoke
def test_browser_uses_selected_environment_url(page, settings):
    print(f"[env] running against '{settings.env}': {settings.base_url}")  # URL is not a secret
    page.goto(settings.base_url)
    expect(page).to_have_url(settings.base_url + "/" if "?" not in settings.base_url else settings.base_url)
    if settings.env != "dev":
        assert f"env={settings.env}" in page.url
