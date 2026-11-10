"""Small helpers: uploads, slugs, safe redirects."""
from pathlib import Path
from urllib.parse import urlparse
from uuid import uuid4

from flask import current_app
from slugify import slugify


def is_safe_next(target: str | None) -> bool:
    """Allow only local, absolute-path redirects."""
    if not target or not target.startswith("/") or target.startswith("//") or "\\" in target:
        return False
    parts = urlparse(target)
    return not parts.scheme and not parts.netloc


def unique_slug(model, text: str, exclude_id: int | None = None) -> str:
    base = slugify(text)[:200] or "item"
    slug, n = base, 2
    while True:
        query = model.query.filter_by(slug=slug)
        if exclude_id:
            query = query.filter(model.id != exclude_id)
        if query.first() is None:
            return slug
        slug = f"{base}-{n}"
        n += 1


def save_image(file_storage) -> str:
    """Validate with Pillow, downscale, store under UPLOAD_FOLDER, return the filename."""
    from PIL import Image, UnidentifiedImageError

    try:
        image = Image.open(file_storage.stream)
        image.load()
    except (UnidentifiedImageError, OSError) as exc:
        raise ValueError("Not a valid image file.") from exc

    fmt = image.format if image.format in {"JPEG", "PNG", "WEBP"} else "PNG"
    if fmt == "JPEG" and image.mode != "RGB":
        image = image.convert("RGB")
    image.thumbnail((1920, 1920))

    ext = "jpg" if fmt == "JPEG" else fmt.lower()
    filename = f"{uuid4().hex}.{ext}"
    folder = Path(current_app.config["UPLOAD_FOLDER"])
    folder.mkdir(parents=True, exist_ok=True)
    image.save(folder / filename, fmt, optimize=True)
    return filename


def delete_image(filename: str | None) -> None:
    if not filename:
        return
    path = Path(current_app.config["UPLOAD_FOLDER"]) / Path(filename).name
    path.unlink(missing_ok=True)
