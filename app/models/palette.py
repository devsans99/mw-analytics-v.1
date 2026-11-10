from ..extensions import db
from .base import TimestampMixin


class Palette(TimestampMixin, db.Model):
    """A colour theme. `light` and `dark` map token name -> hex colour."""

    __tablename__ = "palettes"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    is_active = db.Column(db.Boolean, nullable=False, default=False)
    light = db.Column(db.JSON, nullable=False)
    dark = db.Column(db.JSON, nullable=False)
