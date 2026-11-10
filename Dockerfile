# syntax=docker/dockerfile:1

# ---- Stage 1: build CSS and copy local front-end libraries ------------------
FROM node:lts-slim AS assets
WORKDIR /build
COPY package.json package-lock.json ./
RUN npm ci
COPY scripts/copy_vendor.mjs scripts/copy_vendor.mjs
COPY app app
RUN npm run vendor && npm run build

# ---- Stage 2: Python runtime -------------------------------------------------
FROM python:3.13-slim AS runtime
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    PATH="/opt/venv/bin:$PATH" \
    FLASK_APP=run.py

WORKDIR /srv/mwa
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY . .
COPY --from=assets /build/app/static/css/output.css app/static/css/output.css
COPY --from=assets /build/app/static/vendor app/static/vendor

RUN useradd --system --create-home app \
    && mkdir -p app/static/uploads instance \
    && chown -R app:app app/static/uploads instance
USER app

EXPOSE 8000
CMD ["sh", "-c", "flask db upgrade && exec gunicorn --bind 0.0.0.0:8000 --workers 2 --access-logfile - run:app"]
