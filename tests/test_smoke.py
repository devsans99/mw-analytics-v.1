import pytest

from app.extensions import db
from app.models import Service, User

PUBLIC_PAGES = [
    "/",
    "/portfolio",
    "/services",
    "/projects",
    "/publications",
    "/books",
    "/media-coverage",
    "/contact",
]


@pytest.mark.parametrize("path", PUBLIC_PAGES)
def test_public_pages_render(client, path):
    assert client.get(path).status_code == 200


def test_listing_titles_come_from_child_templates(client):
    assert b"Media Coverage" in client.get("/media-coverage").data


def test_service_detail_and_404(client):
    db.session.add(Service(title="Advisory", slug="advisory", body="<p>Hello</p>"))
    db.session.commit()
    assert client.get("/services/advisory").status_code == 200
    assert client.get("/services/missing").status_code == 404


def test_theme_variables_rendered(client):
    html = client.get("/").data.decode()
    assert "--c-primary" in html and ".dark" in html


def test_cms_requires_login(client):
    response = client.get("/cms-test/")
    assert response.status_code == 302
    assert "/cms-test/login" in response.headers["Location"]


def test_cms_login_and_pages(client):
    user = User(username="boss")
    user.set_password("secret-pass")
    db.session.add(user)
    db.session.commit()

    assert client.get("/cms-test/login").status_code == 200
    response = client.post("/cms-test/login", data={"username": "boss", "password": "secret-pass"})
    assert response.status_code == 302

    for path in [
        "/cms-test/",
        "/cms-test/hero",
        "/cms-test/portfolio",
        "/cms-test/contact",
        "/cms-test/theme",
        "/cms-test/theme/palettes/new",
        "/cms-test/content/services/",
        "/cms-test/content/services/new",
        "/cms-test/content/books/new",
    ]:
        assert client.get(path).status_code == 200, path


def test_cms_create_service_and_theme_change(client):
    user = User(username="boss")
    user.set_password("secret-pass")
    db.session.add(user)
    db.session.commit()
    client.post("/cms-test/login", data={"username": "boss", "password": "secret-pass"})

    response = client.post(
        "/cms-test/content/services/new",
        data={"title": "Strategy", "summary": "S", "body": "<p>x</p>", "is_published": "y"},
    )
    assert response.status_code == 302
    assert client.get("/services/strategy").status_code == 200

    response = client.post("/cms-test/theme", data={"font_heading": "lora", "font_body": "inter"})
    assert response.status_code == 302
    assert b"Lora" in client.get("/").data
