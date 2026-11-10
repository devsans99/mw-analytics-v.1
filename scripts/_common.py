"""Shared helpers for the path generators (standard library only)."""
from __future__ import annotations

import fnmatch
import os
from collections.abc import Iterator
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = ROOT / "documentations"

# Directory names skipped anywhere in the tree.
EXCLUDE_DIR_NAMES = {
    ".git",
    ".venv",
    "venv",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
    "instance",
    ".idea",
    ".vscode",
}
# Directories skipped by path relative to the project root.
EXCLUDE_DIR_PATHS = {
    "migrations/versions",
    "app/static/vendor",
    "app/static/uploads",
}
# File name patterns skipped anywhere.
EXCLUDE_FILE_PATTERNS = [
    "*.pyc",
    "*.min.js",
    "*.min.css",
    "*.db",
    "*.sqlite3",
    "output.css",
    "package-lock.json",
    "uv.lock",
    ".env",
    ".DS_Store",
]


def _dir_excluded(rel: Path) -> bool:
    return rel.name in EXCLUDE_DIR_NAMES or rel.as_posix() in EXCLUDE_DIR_PATHS


def _file_excluded(name: str) -> bool:
    return any(fnmatch.fnmatch(name, pattern) for pattern in EXCLUDE_FILE_PATTERNS)


def iter_files(*suffixes: str) -> Iterator[Path]:
    """Yield project files (relative to ROOT), sorted; optionally filtered by suffix."""
    for dirpath, dirnames, filenames in os.walk(ROOT):
        rel_dir = Path(dirpath).relative_to(ROOT)
        dirnames[:] = sorted(d for d in dirnames if not _dir_excluded(rel_dir / d))
        for name in sorted(filenames):
            if _file_excluded(name):
                continue
            if suffixes and Path(name).suffix not in suffixes:
                continue
            yield rel_dir / name


def write_doc(filename: str, text: str) -> Path:
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    target = DOCS_DIR / filename
    target.write_text(text, encoding="utf-8")
    print(f"Wrote {target.relative_to(ROOT)}")
    return target
