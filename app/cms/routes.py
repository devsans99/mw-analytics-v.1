"""CMS routes. Every route requires login except cms.login (see before_request)."""
from flask import abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user

from ..extensions import db, limiter, login_manager
from ..models import (
    Book,
    Hero,
    MediaCoverage,
    Palette,
    Portfolio,
    Project,
    Publication,
    Service,
    Setting,
    User,
)
from ..theme import (
    DEFAULT_BODY_FONT,
    DEFAULT_DARK,
    DEFAULT_HEADING_FONT,
    DEFAULT_LIGHT,
    HEX_RE,
    PALETTE_TOKENS,
)
from ..utils import delete_image, is_safe_next, save_image, unique_slug
from . import bp
from .forms import ContactForm, ContentForm, FontForm, HeroForm, LoginForm, PaletteForm, PortfolioForm

# URL section -> model. `detail` marks sections that have a public detail page (rich text body).
SECTIONS = {
    "services": {"label": "Services", "model": Service, "detail": True},
    "projects": {"label": "Projects", "model": Project, "detail": True},
    "publications": {"label": "Publications", "model": Publication, "detail": False},
    "books": {"label": "Books", "model": Book, "detail": False},
    "media-coverage": {"label": "Media Coverage", "model": MediaCoverage, "detail": False},
}


def get_section(section: str) -> dict:
    cfg = SECTIONS.get(section)
    if cfg is None:
        abort(404)
    return cfg


def apply_upload(form, obj, attr: str = "image") -> bool:
    """Handle the image/remove_image fields of a form. Returns False (and flashes) on error."""
    try:
        if form.image.data:
            new_name = save_image(form.image.data)
            delete_image(getattr(obj, attr))
            setattr(obj, attr, new_name)
        elif form.remove_image.data:
            delete_image(getattr(obj, attr))
            setattr(obj, attr, None)
    except ValueError as exc:
        flash(str(exc), "error")
        return False
    return True


# --------------------------------------------------------------------------- guards
@bp.before_request
def require_login():
    if request.endpoint == "cms.login":
        return None
    if not current_user.is_authenticated:
        return login_manager.unauthorized()
    return None


@bp.after_request
def no_index(response):
    response.headers["X-Robots-Tag"] = "noindex, nofollow"
    return response


# --------------------------------------------------------------------------- auth
@bp.route("/login", methods=["GET", "POST"])
@limiter.limit("5 per minute", methods=["POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("cms.dashboard"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data.strip()).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            target = request.args.get("next")
            return redirect(target if is_safe_next(target) else url_for("cms.dashboard"))
        flash("Invalid username or password.", "error")
    return render_template("cms/login.html", form=form)


@bp.post("/logout")
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("cms.login"))


# --------------------------------------------------------------------------- dashboard
@bp.get("/")
def dashboard():
    counts = {key: cfg["model"].query.count() for key, cfg in SECTIONS.items()}
    return render_template("cms/dashboard.html", sections=SECTIONS, counts=counts)


# --------------------------------------------------------------------------- single-row pages
@bp.route("/hero", methods=["GET", "POST"])
def hero():
    item = Hero.query.first() or Hero()
    form = HeroForm(obj=item)
    if form.validate_on_submit() and apply_upload(form, item):
        item.title = form.title.data.strip()
        item.subtitle = form.subtitle.data or ""
        item.button_text = form.button_text.data or None
        item.button_url = form.button_url.data or None
        db.session.add(item)
        db.session.commit()
        flash("Home hero saved.", "success")
        return redirect(url_for("cms.hero"))
    return render_template(
        "cms/single_form.html", title="Home Hero", form=form, current_image=item.image
    )


@bp.route("/portfolio", methods=["GET", "POST"])
def portfolio():
    item = Portfolio.query.first() or Portfolio()
    form = PortfolioForm(obj=item)
    if form.validate_on_submit() and apply_upload(form, item, attr="photo"):
        item.name = form.name.data.strip()
        item.position = form.position.data or ""
        item.bio = form.bio.data or ""
        item.expertise = form.expertise.data or ""
        item.linkedin_url = form.linkedin_url.data or None
        db.session.add(item)
        db.session.commit()
        flash("Portfolio saved.", "success")
        return redirect(url_for("cms.portfolio"))
    return render_template(
        "cms/single_form.html", title="Portfolio", form=form, current_image=item.photo
    )


@bp.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm(
        data={
            "phone": Setting.get("contact_phone"),
            "address": Setting.get("contact_address"),
            "email": Setting.get("contact_email"),
        }
    )
    if form.validate_on_submit():
        Setting.set("contact_phone", form.phone.data or "")
        Setting.set("contact_address", form.address.data or "")
        Setting.set("contact_email", form.email.data or "")
        db.session.commit()
        flash("Contact info saved.", "success")
        return redirect(url_for("cms.contact"))
    return render_template("cms/single_form.html", title="Contact Info", form=form, current_image=None)


# --------------------------------------------------------------------------- content sections
@bp.get("/content/<section>/")
def content_list(section):
    cfg = get_section(section)
    model = cfg["model"]
    items = model.query.order_by(model.date.desc().nulls_last(), model.created_at.desc()).all()
    return render_template("cms/content_list.html", section=section, cfg=cfg, items=items)


def save_content(form, item, cfg) -> bool:
    if not apply_upload(form, item):
        return False
    item.title = form.title.data.strip()
    item.slug = unique_slug(cfg["model"], form.slug.data or item.title, item.id)
    item.summary = form.summary.data or ""
    item.body = (form.body.data or "") if cfg["detail"] else ""
    item.date = form.date.data
    item.external_url = form.external_url.data or None
    item.is_published = form.is_published.data
    db.session.add(item)
    db.session.commit()
    return True


@bp.route("/content/<section>/new", methods=["GET", "POST"])
def content_new(section):
    cfg = get_section(section)
    form = ContentForm()
    if form.validate_on_submit() and save_content(form, cfg["model"](), cfg):
        flash("Created.", "success")
        return redirect(url_for("cms.content_list", section=section))
    return render_template("cms/content_form.html", section=section, cfg=cfg, form=form, item=None)


@bp.route("/content/<section>/<int:item_id>/edit", methods=["GET", "POST"])
def content_edit(section, item_id):
    cfg = get_section(section)
    item = db.get_or_404(cfg["model"], item_id)
    form = ContentForm(obj=item)
    if form.validate_on_submit() and save_content(form, item, cfg):
        flash("Saved.", "success")
        return redirect(url_for("cms.content_list", section=section))
    return render_template("cms/content_form.html", section=section, cfg=cfg, form=form, item=item)


@bp.post("/content/<section>/<int:item_id>/delete")
def content_delete(section, item_id):
    cfg = get_section(section)
    item = db.get_or_404(cfg["model"], item_id)
    delete_image(item.image)
    db.session.delete(item)
    db.session.commit()
    flash("Deleted.", "info")
    return redirect(url_for("cms.content_list", section=section))


# --------------------------------------------------------------------------- theme
@bp.route("/theme", methods=["GET", "POST"])
def theme_settings():
    form = FontForm(
        data={
            "font_heading": Setting.get("font_heading", DEFAULT_HEADING_FONT),
            "font_body": Setting.get("font_body", DEFAULT_BODY_FONT),
        }
    )
    if form.validate_on_submit():
        Setting.set("font_heading", form.font_heading.data)
        Setting.set("font_body", form.font_body.data)
        db.session.commit()
        flash("Fonts saved.", "success")
        return redirect(url_for("cms.theme_settings"))
    palettes = Palette.query.order_by(Palette.name).all()
    return render_template("cms/theme.html", form=form, palettes=palettes)


def _edit_palette(palette: Palette | None):
    is_new = palette is None
    if is_new:
        palette = Palette(name="", light=dict(DEFAULT_LIGHT), dark=dict(DEFAULT_DARK))
    form = PaletteForm(obj=palette)
    values = {"light": dict(palette.light), "dark": dict(palette.dark)}

    if request.method == "POST":
        values = {
            mode: {t: request.form.get(f"{mode}_{t}", "") for t in PALETTE_TOKENS}
            for mode in ("light", "dark")
        }
        if form.validate_on_submit():
            all_valid = all(HEX_RE.match(v) for mode in values.values() for v in mode.values())
            if all_valid:
                palette.name = form.name.data.strip()
                palette.light, palette.dark = values["light"], values["dark"]
                db.session.add(palette)
                db.session.commit()
                flash("Palette saved.", "success")
                return redirect(url_for("cms.theme_settings"))
            flash("Every colour must be a valid hex value like #1a2b3c.", "error")

    return render_template(
        "cms/palette_form.html", form=form, values=values, tokens=PALETTE_TOKENS, is_new=is_new
    )


@bp.route("/theme/palettes/new", methods=["GET", "POST"])
def palette_new():
    return _edit_palette(None)


@bp.route("/theme/palettes/<int:palette_id>/edit", methods=["GET", "POST"])
def palette_edit(palette_id):
    return _edit_palette(db.get_or_404(Palette, palette_id))


@bp.post("/theme/palettes/<int:palette_id>/activate")
def palette_activate(palette_id):
    palette = db.get_or_404(Palette, palette_id)
    Palette.query.update({Palette.is_active: False})
    palette.is_active = True
    db.session.commit()
    flash(f"'{palette.name}' is now the active palette.", "success")
    return redirect(url_for("cms.theme_settings"))


@bp.post("/theme/palettes/<int:palette_id>/delete")
def palette_delete(palette_id):
    palette = db.get_or_404(Palette, palette_id)
    if palette.is_active:
        flash("The active palette cannot be deleted. Activate another one first.", "error")
    else:
        db.session.delete(palette)
        db.session.commit()
        flash("Palette deleted.", "info")
    return redirect(url_for("cms.theme_settings"))
