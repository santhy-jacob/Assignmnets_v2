# Playwright Python – Pytest Framework (Assignment 2)

Sync-API Playwright + pytest framework targeting <https://www.saucedemo.com/> (plus the-internet.herokuapp.com for one dynamic-wait test).

## Setup
```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
playwright install                 # chromium, firefox, webkit
cp .env.example .env               # then fill in SAUCE_USERNAME / SAUCE_PASSWORD (never commit .env)
```
SauceDemo's login page lists its public demo usernames and the shared password.

## Project structure
| Path | Purpose |
|---|---|
| `tests/` | test cases, one module per assignment task |
| `pages/` | Page Objects (`LoginPage`, `InventoryPage`) |
| `utils/` | `waits.py` (custom wait), `soft_assert.py`, `data_loader.py`, `run_matrix.py` |
| `config/` | `settings.py` + `environments/{dev,qa,staging}.env` (non-secret) |
| `test_data/` | non-sensitive data |
| `conftest.py` | fixtures: settings, timeouts, custom context/page, credentials, soft assert |
| `pytest.ini` | pytest configuration |

## Running
```bash
pytest                                   # default: chromium, dev, headless
pytest -m smoke                          # smoke only
pytest -m regression
pytest tests/test_07_locators.py         # one file
pytest tests/test_07_locators.py::test_get_by_role   # one test
pytest --headed --slowmo 300             # watch it run
pytest --browser firefox                 # one browser
pytest --browser chromium --browser firefox   # several browsers, one execution
pytest --env qa                          # environment (or TEST_ENV=qa pytest)
DEFAULT_TIMEOUT_MS=2000 pytest           # override any config value from the shell
pytest --html=reports/report.html --self-contained-html
python utils/run_matrix.py               # chromium+firefox+webkit, writes reports/browser_matrix.md
```

### pytest.ini options
| Option | Why |
|---|---|
| `testpaths = tests` | only collect from `tests/` |
| `pythonpath = .` | lets tests import `config`, `pages`, `utils` |
| `--strict-markers` | typos in markers fail instead of silently passing |
| `-ra` | summary of all non-passing tests |
| `--tracing=retain-on-failure` | keeps a Playwright trace (`playwright show-trace`) only for failures |
| `--screenshot=only-on-failure` | screenshot on failure |
| `--output=test-results` | where traces/screenshots go (git-ignored) |
| markers `smoke`, `regression` | select with `-m` |

`--browser`, `--headed`, `--slowmo` come from pytest-playwright; `--env` is defined in `conftest.py`.

## Configuration
Non-secret values live in `config/environments/<env>.env` (BASE_URL, timeouts, headless, viewport). Precedence: real environment variable > env file > default. Default timeout (5 s) and navigation timeout (15 s) are applied to each context in `conftest.py`; `expect()` timeout is set once per session. QA/STAGING currently differ from DEV by a `?env=` query string so all three work against the demo site – replace with your trainer's real URLs.

## Secrets
Credentials are read only from environment variables (loaded from the git-ignored `.env`). `.env.example` has placeholders. `tests/test_05_secrets.py` scans source and reports for the password value. **In CI/CD**, store secrets in the platform's secret store (GitHub Actions *Secrets*, GitLab masked variables, Azure Key Vault/Jenkins Credentials), inject them as environment variables at runtime, never echo them, and rotate them.

## Concepts (short answers)
- **Browser / Context / Page:** a browser is the running engine process; a context is an isolated profile (cookies, storage, cache); a page is one tab in a context.
- **Fixture scope:** `browser` is session-scoped (launching is slow); contexts/pages are function-scoped so each test gets clean state and tests cannot affect each other.
- **Most maintainable locators:** `get_by_role`, `get_by_label`, `get_by_placeholder`, `data-test` attributes. XPath/CSS-class selectors break when the DOM changes.
- **`expect()` vs `assert`:** `expect()` auto-retries until the page reaches the state (use for anything in the browser); `assert` checks a Python value immediately (use for extracted/calculated data).
- **Hard vs soft assertions:** hard stops at the first failure; soft (`utils/soft_assert.py`) records and continues, then `assert_all()` reports everything. Use soft only for independent UI checks.
- **Why condition waits beat sleeps:** they finish the moment the app is ready, so they are neither flaky (too short) nor slow (too long). Timeouts are kept modest; the fix for a failing wait is the right condition, not a huge timeout.

## Browser matrix (fill from `python utils/run_matrix.py`)
| Test | Chromium | Firefox | WebKit |
|---|---|---|---|
| Login (`test_login_valid_user`) | | | |
| Search/Sort (`test_sort_products_by_price`) | | | |
| Navigation (`test_navigation_back_forward_reload`) | | | |
| Form Validation (`test_form_validation_messages`) | | | |

## Notes
Tests that need credentials are skipped (not failed) if `.env` is missing. `test_14_dynamic_spa.py::test_dynamic_loading_wait_for_condition` needs internet access to the-internet.herokuapp.com.
