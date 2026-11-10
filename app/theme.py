"""Theme support: colour tokens, font presets and template context."""
import re
from datetime import datetime

from flask import url_for
from sqlalchemy.exc import SQLAlchemyError

from .extensions import db
from .models import Palette, Setting

HEX_RE = re.compile(r"^#[0-9a-fA-F]{6}$")

PALETTE_TOKENS = [
    "primary",
    "primary-contrast",
    "accent",
    "background",
    "surface",
    "text",
    "muted",
    "border",
]

DEFAULT_LIGHT = {
    "primary": "#1d4ed8",
    "primary-contrast": "#ffffff",
    "accent": "#f59e0b",
    "background": "#ffffff",
    "surface": "#f3f4f6",
    "text": "#111827",
    "muted": "#6b7280",
    "border": "#e5e7eb",
}
DEFAULT_DARK = {
    "primary": "#60a5fa",
    "primary-contrast": "#0b1220",
    "accent": "#fbbf24",
    "background": "#0b1220",
    "surface": "#131c2e",
    "text": "#e5e7eb",
    "muted": "#9ca3af",
    "border": "#243049",
}

SEED_PALETTES = [
    {"name": "Corporate Blue", "light": DEFAULT_LIGHT, "dark": DEFAULT_DARK},
    {
        "name": "Emerald",
        "light": {
            "primary": "#047857", "primary-contrast": "#ffffff", "accent": "#d97706",
            "background": "#ffffff", "surface": "#f0fdf4", "text": "#052e16",
            "muted": "#4b5563", "border": "#d1fae5",
        },
        "dark": {
            "primary": "#34d399", "primary-contrast": "#04130d", "accent": "#fbbf24",
            "background": "#07130e", "surface": "#0d1f17", "text": "#ecfdf5",
            "muted": "#9ca3af", "border": "#1b3a2c",
        },
    },
    {
        "name": "Slate & Amber",
        "light": {
            "primary": "#334155", "primary-contrast": "#ffffff", "accent": "#d97706",
            "background": "#fafaf9", "surface": "#f5f5f4", "text": "#1c1917",
            "muted": "#78716c", "border": "#e7e5e4",
        },
        "dark": {
            "primary": "#cbd5e1", "primary-contrast": "#0f172a", "accent": "#fbbf24",
            "background": "#0c0a09", "surface": "#1c1917", "text": "#fafaf9",
            "muted": "#a8a29e", "border": "#292524",
        },
    },
]

# key -> label, CSS font-family value, Google Fonts "family" spec
FONTS = {
    "inter": {"label": "Inter", "css": "'Inter', sans-serif", "google": "Inter:wght@400;500;600;700"},
    "poppins": {"label": "Poppins", "css": "'Poppins', sans-serif", "google": "Poppins:wght@400;500;600;700"},
    "dm-sans": {"label": "DM Sans", "css": "'DM Sans', sans-serif", "google": "DM+Sans:wght@400;500;700"},
    "montserrat": {"label": "Montserrat", "css": "'Montserrat', sans-serif", "google": "Montserrat:wght@400;500;600;700"},
    "playfair-display": {"label": "Playfair Display", "css": "'Playfair Display', serif", "google": "Playfair+Display:wght@500;600;700"},
    "merriweather": {"label": "Merriweather", "css": "'Merriweather', serif", "google": "Merriweather:wght@400;700"},
    "lora": {"label": "Lora", "css": "'Lora', serif", "google": "Lora:wght@400;500;600;700"},
    "source-serif": {"label": "Source Serif 4", "css": "'Source Serif 4', serif", "google": "Source+Serif+4:wght@400;600;700"},
}
FONT_CHOICES = [(key, meta["label"]) for key, meta in FONTS.items()]
DEFAULT_HEADING_FONT = "playfair-display"
DEFAULT_BODY_FONT = "inter"


def google_fonts_url(*keys: str) -> str:
    families = dict.fromkeys(FONTS[key]["google"] for key in keys)
    query = "&".join(f"family={spec}" for spec in families)
    return f"https://fonts.googleapis.com/css2?{query}&display=swap"


def upload_url(filename: str | None) -> str:
    return url_for("static", filename=f"uploads/{filename}") if filename else ""


def load_theme() -> dict:
    """Read palette, fonts and contact info; falls back to defaults if the DB is not ready."""
    settings: dict[str, str] = {}
    palette = None
    try:
        settings = {row.key: row.value for row in Setting.query.all()}
        palette = Palette.query.filter_by(is_active=True).first()
    except SQLAlchemyError:
        db.session.rollback()

    heading_key = settings.get("font_heading", DEFAULT_HEADING_FONT)
    body_key = settings.get("font_body", DEFAULT_BODY_FONT)
    if heading_key not in FONTS:
        heading_key = DEFAULT_HEADING_FONT
    if body_key not in FONTS:
        body_key = DEFAULT_BODY_FONT

    return {
        "theme": {
            "light": {**DEFAULT_LIGHT, **(palette.light if palette else {})},
            "dark": {**DEFAULT_DARK, **(palette.dark if palette else {})},
            "heading_css": FONTS[heading_key]["css"],
            "body_css": FONTS[body_key]["css"],
            "fonts_url": google_fonts_url(heading_key, body_key),
        },
        "contact": {
            "phone": settings.get("contact_phone", ""),
            "address": settings.get("contact_address", ""),
            "email": settings.get("contact_email", ""),
        },
    }


def register_theme(app) -> None:
    @app.context_processor
    def inject_theme():
        return {
            **load_theme(),
            "site_name": app.config["SITE_NAME"],
            "current_year": datetime.now().year,
            "upload_url": upload_url,
        }
