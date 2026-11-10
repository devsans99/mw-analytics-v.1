"""Public pages. All URLs and page names are in English."""
from flask import render_template

from ..models import Book, Hero, MediaCoverage, Portfolio, Project, Publication, Service
from . import bp


def published(model):
    return (
        model.query.filter_by(is_published=True)
        .order_by(model.date.desc().nulls_last(), model.created_at.desc())
        .all()
    )


def published_or_404(model, slug: str):
    return model.query.filter_by(slug=slug, is_published=True).first_or_404()


@bp.get("/")
def home():
    return render_template("site/home.html", hero=Hero.query.first())


@bp.get("/portfolio")
def portfolio():
    return render_template("site/portfolio.html", profile=Portfolio.query.first())


@bp.get("/services")
def services():
    return render_template("site/services.html", items=published(Service))


@bp.get("/services/<slug>")
def service_detail(slug):
    return render_template("site/service_detail.html", item=published_or_404(Service, slug))


@bp.get("/projects")
def projects():
    return render_template("site/projects.html", items=published(Project))


@bp.get("/projects/<slug>")
def project_detail(slug):
    return render_template("site/project_detail.html", item=published_or_404(Project, slug))


@bp.get("/publications")
def publications():
    return render_template("site/publications.html", items=published(Publication))


@bp.get("/books")
def books():
    return render_template("site/books.html", items=published(Book))


@bp.get("/media-coverage")
def media_coverage():
    return render_template("site/media_coverage.html", items=published(MediaCoverage))


@bp.get("/contact")
def contact():
    return render_template("site/contact.html")
