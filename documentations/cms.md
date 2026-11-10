# CMS

## Access

- URL: `/<ADMIN_URL_PREFIX>/login`. The prefix comes from `.env` and is deliberately not guessable. Use a long random value per deployment.
- One administrator only, created from the command line: `flask create-admin`. There is no registration page.
- Change the password: `flask set-admin-password`.
- Login is rate limited (5 attempts per minute per IP). All CMS routes require login by default (`before_request` in `app/cms/routes.py`) and send `X-Robots-Tag: noindex`.

## Menu

| Menu | Route name | Notes |
|---|---|---|
| Dashboard | `cms.dashboard` | counts per section |
| Home Hero | `cms.hero` | title, subtitle, image, button text and URL |
| Portfolio | `cms.portfolio` | single profile: name, position, photo, bio, expertise, LinkedIn |
| Services, Projects | `cms.content_*` | list/new/edit/delete, rich text body (detail pages) |
| Publications, Books, Media Coverage | `cms.content_*` | cards with external link, no rich text |
| Contact Info | `cms.contact` | phone, address, email (the public button is `mailto:`) |
| Theme | `cms.theme_settings` | fonts, palettes (create, edit, activate, delete) |

## Content sections

`SECTIONS` in `app/cms/routes.py` maps a URL segment to a model and says whether it has a detail page. One set of views (`content_list`, `content_new`, `content_edit`, `content_delete`) serves all sections, so adding a section means: new model + migration, entry in `SECTIONS`, public route and template, sidebar link.

## Images

Uploads are validated with Pillow, downscaled to 1920 px, renamed to a random name and stored in `app/static/uploads` (Docker volume `uploads` in production). Allowed: jpg, png, webp, max 8 MB per request.

## Rich text

Quill (local copy in `static/vendor/quill`) via the Alpine component `richEditor` in `static/js/cms.js`. HTML is stored in `body` and rendered with `|safe` because only the trusted admin writes it.
