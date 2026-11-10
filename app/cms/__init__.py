"""CMS blueprint. Mounted at /<ADMIN_URL_PREFIX> (see app.create_app)."""
from flask import Blueprint

bp = Blueprint("cms", __name__)

from . import routes  # noqa: E402,F401
