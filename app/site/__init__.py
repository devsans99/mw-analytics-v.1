"""Public website blueprint."""
from flask import Blueprint

bp = Blueprint("site", __name__)

from . import routes  # noqa: E402,F401
