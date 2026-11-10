"""Configuration, read from environment variables (see .env.example)."""
import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


def _flag(name: str, default: bool = False) -> bool:
    raw = os.environ.get(name, "1" if default else "0")
    return raw.strip().lower() in {"1", "true", "yes", "on"}


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only-change-me")
    SITE_NAME = os.environ.get("SITE_NAME", "MWA")
    ADMIN_URL_PREFIX = os.environ.get("ADMIN_URL_PREFIX", "cms-change-me")

    # PostgreSQL via DATABASE_URL (Docker). SQLite is only a local fallback.
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or (
        f"sqlite:///{BASE_DIR / 'instance' / 'mwa.db'}"
    )

    UPLOAD_FOLDER = BASE_DIR / "app" / "static" / "uploads"
    MAX_CONTENT_LENGTH = 8 * 1024 * 1024  # 8 MB per request

    TRUST_PROXY = _flag("TRUST_PROXY")
    SESSION_COOKIE_SECURE = _flag("SESSION_COOKIE_SECURE")
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

    RATELIMIT_STORAGE_URI = os.environ.get("RATELIMIT_STORAGE_URI", "memory://")
