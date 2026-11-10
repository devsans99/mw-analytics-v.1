"""Application factory."""
from pathlib import Path

from flask import Flask, render_template
from werkzeug.middleware.proxy_fix import ProxyFix

from .config import Config
from .extensions import csrf, db, limiter, login_manager, migrate


def create_app(config_class: type = Config) -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)

    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    Path(app.config["UPLOAD_FOLDER"]).mkdir(parents=True, exist_ok=True)

    if app.config["TRUST_PROXY"]:
        # Behind Cloudflare + Caddy: trust one proxy hop for client IP / scheme / host.
        app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)

    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    limiter.init_app(app)
    login_manager.init_app(app)

    from . import models  # noqa: F401  (registers models for migrations)
    from .cli import register_cli
    from .cms import bp as cms_bp
    from .site import bp as site_bp
    from .theme import register_theme

    prefix = app.config["ADMIN_URL_PREFIX"].strip("/")
    app.register_blueprint(site_bp)
    app.register_blueprint(cms_bp, url_prefix=f"/{prefix}")
    register_theme(app)
    register_cli(app)

    @app.errorhandler(404)
    def not_found(_error):
        return render_template("errors/404.html"), 404

    return app
