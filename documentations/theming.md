# Theming

## Dark / light mode (visitors)

- Dark mode is the `.dark` class on `<html>`.
- `static/js/theme-init.js` runs before first paint: it uses the saved choice (`localStorage["theme"]`) or, if none, the system preference.
- The toggle button (`partials/_theme_toggle.html`) uses the Alpine component `themeToggle` in `static/js/app.js`.
- Visitors can only toggle dark/light. The colour palette is chosen in the CMS.

## Palettes (CMS only)

Each palette stores two token maps, `light` and `dark`:

`primary`, `primary-contrast`, `accent`, `background`, `surface`, `text`, `muted`, `border`

- Exactly one palette is active (CMS → Theme → Activate).
- `partials/_theme_style.html` writes the active palette as CSS variables (`--c-<token>`) on `:root` and `.dark`.
- `static/css/input.css` maps them into Tailwind v4 with `@theme inline` (`bg-primary`, `text-muted`, `border-border`, ...). Changing a palette needs no CSS rebuild.
- Use only token classes (`bg-background`, `text-text`, `bg-primary text-primary-contrast`, ...) so every page follows the palette. Avoid hard-coded colours such as `bg-blue-500`.
- Rich text (`.prose-theme`) is wired to the same tokens.

## Fonts (CMS only)

- CMS → Theme lets the admin pick a heading font and a body font from presets (`FONTS` in `app/theme.py`).
- Fonts load from Google Fonts. The URL is built from the two selected presets.
- Utilities: `font-heading`, `font-body`. `h1`–`h4` use the heading font by default.
- To add a font, add an entry to `FONTS` (label, CSS family, Google spec).

## Adding a token

1. Add the name to `PALETTE_TOKENS` and the defaults in `app/theme.py`.
2. Add `--color-<token>: var(--c-<token>);` to `@theme inline` in `input.css`.
3. Existing palettes fall back to the default value until edited.
