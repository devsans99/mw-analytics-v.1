"""Flask CLI commands: create-admin, set-admin-password, seed."""
import click

from .extensions import db
from .models import Hero, Palette, Portfolio, Setting, User
from .theme import DEFAULT_BODY_FONT, DEFAULT_HEADING_FONT, SEED_PALETTES

DEFAULT_SETTINGS = {
    "font_heading": DEFAULT_HEADING_FONT,
    "font_body": DEFAULT_BODY_FONT,
    "contact_phone": "+62 000 0000 0000",
    "contact_address": "Your street address, City, Country",
    "contact_email": "hello@example.com",
}


def seed_database() -> None:
    """Idempotent: only fills in what is missing."""
    if Palette.query.count() == 0:
        for index, data in enumerate(SEED_PALETTES):
            db.session.add(
                Palette(name=data["name"], light=data["light"], dark=data["dark"], is_active=index == 0)
            )
    if Hero.query.first() is None:
        db.session.add(
            Hero(
                title="Strategic consulting that moves your organization forward",
                subtitle="Placeholder text. Edit this hero section from the CMS.",
                button_text="Get in touch",
                button_url="/contact",
            )
        )
    if Portfolio.query.first() is None:
        db.session.add(
            Portfolio(
                name="Your Name",
                position="Founder & Principal Consultant",
                bio="<p>Placeholder biography. Edit it from the CMS.</p>",
                expertise="Strategy, Policy, Research",
            )
        )
    for key, value in DEFAULT_SETTINGS.items():
        if db.session.get(Setting, key) is None:
            db.session.add(Setting(key=key, value=value))
    db.session.commit()


def register_cli(app) -> None:
    def admin_url() -> str:
        return f"/{app.config['ADMIN_URL_PREFIX'].strip('/')}/login"

    @app.cli.command("create-admin")
    @click.option("--username", prompt=True)
    @click.password_option()
    def create_admin(username, password):
        """Create the single CMS administrator."""
        if User.query.first():
            raise click.ClickException("An admin already exists. Use 'flask set-admin-password'.")
        user = User(username=username.strip())
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        click.echo(f"Admin '{user.username}' created. Login at: {admin_url()}")

    @app.cli.command("set-admin-password")
    @click.password_option()
    def set_admin_password(password):
        """Change the administrator password."""
        user = User.query.first()
        if user is None:
            raise click.ClickException("No admin yet. Run 'flask create-admin' first.")
        user.set_password(password)
        db.session.commit()
        click.echo("Password updated.")

    @app.cli.command("seed")
    def seed():
        """Insert starter data (palettes, hero, profile, contact info)."""
        seed_database()
        click.echo("Seed data ready.")
