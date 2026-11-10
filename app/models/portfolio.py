from ..extensions import db
from .base import TimestampMixin


class Portfolio(TimestampMixin, db.Model):
    """Profile of the principal consultant (single row)."""

    __tablename__ = "portfolio"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, default="")
    position = db.Column(db.String(150), nullable=False, default="")
    photo = db.Column(db.String(255))
    bio = db.Column(db.Text, nullable=False, default="")
    expertise = db.Column(db.Text, nullable=False, default="")  # comma separated
    linkedin_url = db.Column(db.String(500))
