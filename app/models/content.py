"""Content models. Placeholder fields only; extend per model later."""
from ..extensions import db
from .base import ContentMixin


class Service(ContentMixin, db.Model):
    __tablename__ = "services"


class Project(ContentMixin, db.Model):
    __tablename__ = "projects"


class Publication(ContentMixin, db.Model):
    __tablename__ = "publications"


class Book(ContentMixin, db.Model):
    __tablename__ = "books"


class MediaCoverage(ContentMixin, db.Model):
    __tablename__ = "media_coverage"
