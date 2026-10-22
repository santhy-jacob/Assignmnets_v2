"""Configuration layer: non-secret settings from config/environments/<env>.env,
secrets from environment variables / .env. Real env vars always win."""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import dotenv_values, load_dotenv

ROOT = Path(__file__).resolve().parent.parent
ENV_DIR = Path(__file__).resolve().parent / "environments"
VALID_ENVS = ("dev", "qa", "staging")


class MissingCredentialsError(RuntimeError):
    pass


@dataclass(frozen=True)
class Settings:
    env: str
    base_url: str
    default_timeout_ms: int
    navigation_timeout_ms: int
    expect_timeout_ms: int
    headless: bool
    slow_mo_ms: int
    viewport_width: int
    viewport_height: int


def _as_bool(value: str) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "on"}


def load_settings(env: str | None = None) -> Settings:
    load_dotenv(ROOT / ".env")  # puts local secrets into os.environ (never overrides real env vars)
    env = (env or os.getenv("TEST_ENV") or "dev").lower()
    if env not in VALID_ENVS:
        raise ValueError(f"Unknown environment '{env}'. Choose one of {VALID_ENVS}")
    file_values = dotenv_values(ENV_DIR / f"{env}.env")

    def get(key: str, default: str = "") -> str:
        return os.getenv(key) or file_values.get(key) or default

    return Settings(
        env=env,
        base_url=get("BASE_URL").rstrip("/") if "?" not in get("BASE_URL") else get("BASE_URL"),
        default_timeout_ms=int(get("DEFAULT_TIMEOUT_MS", "5000")),
        navigation_timeout_ms=int(get("NAVIGATION_TIMEOUT_MS", "15000")),
        expect_timeout_ms=int(get("EXPECT_TIMEOUT_MS", "5000")),
        headless=_as_bool(get("HEADLESS", "true")),
        slow_mo_ms=int(get("SLOW_MO_MS", "0")),
        viewport_width=int(get("VIEWPORT_WIDTH", "1280")),
        viewport_height=int(get("VIEWPORT_HEIGHT", "720")),
    )


def get_credentials() -> tuple[str, str]:
    load_dotenv(ROOT / ".env")
    user, pwd = os.getenv("SAUCE_USERNAME"), os.getenv("SAUCE_PASSWORD")
    if not user or not pwd:
        raise MissingCredentialsError(
            "SAUCE_USERNAME / SAUCE_PASSWORD not set. Copy .env.example to .env and fill them in."
        )
    return user, pwd
