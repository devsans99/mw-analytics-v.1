from ..extensions import db


class Setting(db.Model):
    """Key/value site settings (contact info, active fonts, ...)."""

    __tablename__ = "settings"

    key = db.Column(db.String(80), primary_key=True)
    value = db.Column(db.Text, nullable=False, default="")

    @classmethod
    def get(cls, key: str, default: str = "") -> str:
        row = db.session.get(cls, key)
        return row.value if row else default

    @classmethod
    def set(cls, key: str, value: str) -> None:
        """Stage a value; the caller commits."""
        row = db.session.get(cls, key)
        if row is None:
            db.session.add(cls(key=key, value=value))
        else:
            row.value = value
