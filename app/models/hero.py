from ..extensions import db
from .base import TimestampMixin


class Hero(TimestampMixin, db.Model):
    """Home page hero section (single row)."""

    __tablename__ = "hero"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, default="")
    subtitle = db.Column(db.Text, nullable=False, default="")
    image = db.Column(db.String(255))
    button_text = db.Column(db.String(80))
    button_url = db.Column(db.String(500))
