# Conventions

## Python

- App factory + blueprints. No code that needs the app at import time.
- Extensions live in `extensions.py`; models in `app/models/` (one file per concern, exported from `__init__.py`).
- Routes stay thin: query, render. Shared logic goes to `utils.py` or a service module.
- Schema changes always go through Flask-Migrate: `flask db migrate -m "..."` then `flask db upgrade`. Review the generated file before committing.
- Configuration only through environment variables (`config.py`, `.env.example`). Never commit `.env`.
- Type hints on new functions; docstring first line is picked up by `paths_def.md`.

## Templates

- Pages extend `base.html`; CMS pages extend `cms/base.html`.
- Listing pages extend `site/_list.html`, detail pages extend `site/_detail.html` (child templates set `page_title`, `detail_endpoint`, `back_endpoint`, ...).
- Partials start with an underscore (`_card.html`).
- All user-facing text is English.
- Styling: Tailwind utilities with palette tokens only (see [theming.md](theming.md)).

## JavaScript

- Alpine.js components are registered in `static/js/app.js` (public) and `static/js/cms.js` (CMS) with `Alpine.data(...)`; keep inline `x-data` small.
- No bundler. Libraries are copied from `node_modules` by `npm run vendor`.

## Naming

- URLs: lowercase English, hyphen separated (`/media-coverage`). Endpoint names: snake_case (`site.media_coverage`).
- Branches/commits: short imperative messages.

## Tests

`pytest` smoke tests in `tests/` use an in-memory SQLite database. Add a test for every new route.

## Generated docs

Run the three scripts in `scripts/` after structural changes and commit the updated `paths*.md`. They are meant to be uploaded to a Claude project as an up-to-date map of the code.
