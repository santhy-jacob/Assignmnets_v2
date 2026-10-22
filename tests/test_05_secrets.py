"""Task 7 - secrets: read from env vars, never hardcode, never leak into files/reports."""
from playwright.sync_api import expect

from config.settings import ROOT
from pages.login_page import LoginPage

SKIP_DIRS = {".venv", "venv", ".git", "__pycache__", ".pytest_cache", "node_modules"}
TEXT_SUFFIXES = {".py", ".md", ".ini", ".txt", ".json", ".html", ".xml", ".env", ".example", ".yml", ".yaml"}


def test_login_with_env_credentials(page, base_url, credentials):
    user, _ = credentials
    LoginPage(page, base_url).open().login(*credentials)
    print(f"Logged in as: {user}")  # username only - never the password
    expect(page).to_have_url(__import__("re").compile(r".*/inventory\.html"))


def test_password_not_present_in_source_or_reports(credentials):
    _, password = credentials
    leaks = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.name == ".env" or SKIP_DIRS & set(path.parts):
            continue
        if path.suffix not in TEXT_SUFFIXES and path.name != ".env.example":
            continue
        if password in path.read_text(encoding="utf-8", errors="ignore"):
            leaks.append(str(path.relative_to(ROOT)))
    assert leaks == [], f"Secret found in: {leaks}"


def test_env_file_is_gitignored_and_example_has_placeholders_only():
    assert ".env" in (ROOT / ".gitignore").read_text().splitlines()
    for line in (ROOT / ".env.example").read_text().splitlines():
        if line.strip() and not line.startswith("#"):
            key, _, value = line.partition("=")
            assert key == "TEST_ENV" or value.startswith("<"), f"{key} must be a placeholder"
