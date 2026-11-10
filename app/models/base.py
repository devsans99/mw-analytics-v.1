"""Shared column mixins."""
from datetime import datetime, timezone

from ..extensions import db


def _now() -> datetime:
    return datetime.now(timezone.utc)


class TimestampMixin:
    created_at = db.Column(db.DateTime(timezone=True), default=_now, nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), default=_now, onupdate=_now, nullable=False)


class ContentMixin(TimestampMixin):
    """Common fields for Service, Project, Publication, Book and MediaCoverage."""

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(220), unique=True, nullable=False, index=True)
    summary = db.Column(db.Text, nullable=False, default="")
    body = db.Column(db.Text, nullable=False, default="")  # rich text (HTML)
    image = db.Column(db.String(255))
    date = db.Column(db.Date)
    external_url = db.Column(db.String(500))
    is_published = db.Column(db.Boolean, nullable=False, default=True)
