# MWA — Consulting Website

Flask + Alpine.js + Tailwind CSS v4, with a custom CMS. All page names and URLs are in English.

## Stack

| Layer | Choice |
|---|---|
| Backend | Python 3.13, Flask (app factory + blueprints), uv |
| Database | PostgreSQL (Docker). SQLite is only a fallback when `DATABASE_URL` is unset |
| Frontend | Tailwind CSS v4 (CLI), Alpine.js 3, Font Awesome Free, Quill (CMS editor) |
| Runtime | Docker Compose; Caddy (HTTPS) behind Cloudflare in production |

Front-end libraries are installed with npm and copied to `app/static/vendor` (served locally, no CDN except Google Fonts).

## Quick start (development, macOS, full Docker)

```bash
cp .env.example .env            # then edit SECRET_KEY, ADMIN_URL_PREFIX, passwords
docker compose -f compose.dev.yaml up --build
```

In a second terminal (first run only):

```bash
docker compose -f compose.dev.yaml exec web flask seed
docker compose -f compose.dev.yaml exec web flask create-admin
```

- Site: http://localhost:5000
- CMS: http://localhost:5000/`<ADMIN_URL_PREFIX>`/login
- The `tailwind` service installs npm packages, copies vendor libraries and rebuilds CSS on every change. The first start has unstyled pages until it finishes.

## Common commands

| Task | Command (prefix with `docker compose -f compose.dev.yaml exec web`) |
|---|---|
| Run tests | `pytest` |
| Create a migration | `flask db migrate -m "message"` then `flask db upgrade` |
| Change admin password | `flask set-admin-password` |
| Regenerate path docs | `python scripts/generate_paths.py && python scripts/generate_paths_def.py && python scripts/generate_paths_func.py` |

## Documentation index

- [architecture.md](architecture.md) — structure, request flow, data model
- [theming.md](theming.md) — dark/light mode, palettes, fonts
- [cms.md](cms.md) — admin area, sections, security
- [conventions.md](conventions.md) — coding conventions
- [deployment.md](deployment.md) — Docker deployment on Ubuntu and macOS, Cloudflare + Caddy
- Generated: [paths.md](paths.md), [paths_def.md](paths_def.md), [paths_func.md](paths_func.md)
