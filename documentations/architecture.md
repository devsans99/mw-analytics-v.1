# Architecture

## Layout

```text
app/
  __init__.py      create_app(): extensions, blueprints, ProxyFix, error handlers
  config.py        environment-based Config
  extensions.py    db, migrate, csrf, limiter, login_manager
  theme.py         palette tokens, font presets, template context
  utils.py         image upload (Pillow), slugs, safe redirects
  cli.py           flask create-admin | set-admin-password | seed
  models/          one module per table group
  site/            public blueprint (routes.py)
  cms/             admin blueprint (routes.py, forms.py), mounted at /<ADMIN_URL_PREFIX>
  templates/       base.html, partials/, site/, cms/, errors/
  static/          css/ js/ vendor/ uploads/
scripts/           path generators + copy_vendor.mjs
migrations/        Alembic (Flask-Migrate)
tests/             pytest smoke tests
```

## Public URLs

`/`, `/portfolio`, `/services`, `/services/<slug>`, `/projects`, `/projects/<slug>`, `/publications`, `/books`, `/media-coverage`, `/contact`.

Only Services and Projects have detail pages. Publications, Books and Media Coverage are cards linking to `external_url`.

## Data model

- `ContentMixin` (shared by `Service`, `Project`, `Publication`, `Book`, `MediaCoverage`): `title`, `slug`, `summary`, `body` (rich text HTML), `image`, `date`, `external_url`, `is_published`, timestamps.
- Single-row tables: `Hero` (home hero), `Portfolio` (principal's profile).
- `Setting` (key/value): contact info and active fonts.
- `Palette`: `name`, `is_active`, `light` and `dark` JSON token maps.
- `User`: the single administrator.

## Request flow

1. A public route loads published rows and renders a template extending `base.html`.
2. A context processor (`theme.register_theme`) injects the active palette, fonts, contact info, `site_name`, `current_year` and `upload_url()` into every template.
3. `base.html` renders palette tokens as CSS variables; Tailwind utilities read those variables, so no rebuild is needed when the theme changes.

## Production topology

Browser → Cloudflare (proxied) → Caddy container (HTTPS) → gunicorn container (Flask) → PostgreSQL container. See [deployment.md](deployment.md).

## Known limits (intentional for the skeleton)

- Flask-Limiter uses in-memory storage; with several gunicorn workers limits are per worker. Set `RATELIMIT_STORAGE_URI` to Redis later if stricter limits are needed.
- Rich text and hero URLs are authored by the trusted admin and are rendered as-is.
