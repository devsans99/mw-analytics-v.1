# Deployment (Docker)

Everything runs in Docker: development on macOS, production on Ubuntu. Only Docker is needed on the host.

## A. macOS (development)

1. Install Docker Desktop (or OrbStack / Colima).
2. `cp .env.example .env` and edit `SECRET_KEY`, `ADMIN_URL_PREFIX`, `POSTGRES_PASSWORD`.
3. Start: `docker compose -f compose.dev.yaml up --build`
4. First run only:
   ```bash
   docker compose -f compose.dev.yaml exec web flask seed
   docker compose -f compose.dev.yaml exec web flask create-admin
   ```
5. Open http://localhost:5000 (CMS at `/<ADMIN_URL_PREFIX>/login`).
6. Stop: `docker compose -f compose.dev.yaml down` (add `-v` to also delete the dev database).

Code is bind-mounted; Flask reloads on save and the `tailwind` service rebuilds CSS. After changing Python dependencies run `docker compose -f compose.dev.yaml exec web uv sync` or rebuild with `--build`.

## B. Ubuntu server (production)

### 1. Prepare the server

```bash
# Docker Engine + Compose plugin: follow https://docs.docker.com/engine/install/ubuntu/
sudo usermod -aG docker $USER      # log out and in again
sudo ufw allow OpenSSH && sudo ufw allow 80,443/tcp && sudo ufw allow 443/udp && sudo ufw enable
```

### 2. Cloudflare

1. DNS: `A` record for your domain → server IP, **Proxied** (orange cloud).
2. SSL/TLS → Overview → mode **Full (strict)**.
3. If Caddy cannot obtain its certificate while proxied, either temporarily switch the record to DNS-only for the first issuance, or create a Cloudflare Origin Certificate and mount it in Caddy (`tls cert.pem key.pem`).

### 3. Deploy

```bash
git clone <your-repo-url> mwa && cd mwa
cp .env.example .env
nano .env        # set SECRET_KEY, ADMIN_URL_PREFIX, POSTGRES_PASSWORD, DOMAIN
docker compose up -d --build
docker compose exec web flask seed
docker compose exec web flask create-admin
```

Open `https://<DOMAIN>/<ADMIN_URL_PREFIX>/login`.

The `web` container runs `flask db upgrade` on every start, so migrations are applied automatically.

### 4. Update

```bash
git pull
docker compose up -d --build
```

### 5. Backup and restore

```bash
# database
docker compose exec -T db sh -c 'pg_dump -U "$POSTGRES_USER" "$POSTGRES_DB"' > backup.sql
# uploads
docker run --rm -v mwa_uploads:/data -v "$PWD":/backup alpine tar czf /backup/uploads.tgz -C /data .
# restore database
docker compose exec -T db sh -c 'psql -U "$POSTGRES_USER" "$POSTGRES_DB"' < backup.sql
```

(The volume name is prefixed with the project folder name; check with `docker volume ls`.)

### 6. Useful commands

```bash
docker compose ps
docker compose logs -f web
docker compose logs -f proxy
docker compose restart web
```

## How the real visitor IP is kept

Cloudflare sends `CF-Connecting-IP`. The `Caddyfile` trusts Cloudflare's IP ranges and reads that header; Caddy forwards the result as `X-Forwarded-For`; Flask's `ProxyFix` (enabled by `TRUST_PROXY=1`) uses it. This keeps the login rate limit per visitor instead of per Cloudflare node. Cloudflare's ranges change rarely: check https://www.cloudflare.com/ips/ from time to time and update `Caddyfile`.

## Checklist before going live

- [ ] Strong random `SECRET_KEY`, `POSTGRES_PASSWORD` and `ADMIN_URL_PREFIX`
- [ ] Cloudflare SSL mode is Full (strict)
- [ ] Admin created, seed data reviewed in the CMS
- [ ] Backup job (cron) for database and uploads
