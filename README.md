# Traceleaf

Evidence-backed maintenance for Markdown knowledge bases. The planned workflow turns an incoming source into document-specific update proposals, with references, a diff, human approval and revision history. Compatible with an Obsidian workflow; external folders will be read-only in v1.

**Current stage: M0 foundation.** The web app displays the actual API, PostgreSQL schema/pgvector and Redis status. Markdown editing, RAG, agents and proposals are planned; they are not available yet. No personal folder is connected and no model calls are made, even if credentials are configured.

[Guia em português](docs/getting-started.pt-BR.md) · [Implementation status](docs/implementation-status.md) · [Product validation](docs/product-validation.md) · [Planning](docs/planning/ai-engineer/projeto-base-conhecimento-ia/00-leia-primeiro.md)

## Start locally

Requirements: Git, Python 3 (only for generating local configuration) and a running Docker engine with Compose v2.20+ (`docker compose`). The first build needs network access to download pinned images and dependencies. Run commands from the repository root.

```sh
git clone https://github.com/RuhtracBP/traceleaf.git
cd traceleaf
python3 scripts/setup_env.py
docker compose up --build --wait
```

Open **http://localhost:8080**. API documentation is at http://localhost:8000/docs. Ports bind to loopback; PostgreSQL and Redis have no published ports in the default setup. Change `TRACELEAF_WEB_PORT` / `TRACELEAF_API_PORT` in `.env` if needed.

The setup script creates `.env` with a random database password and does not overwrite an existing file. Do not commit it. Keep the generated alphanumeric password, or URL-encode any special characters if editing the database URL manually. Changing the password in `.env` does not change an already initialized PostgreSQL role.

Compose waits for PostgreSQL/Redis, runs Alembic migrations, then starts the API and web app. Health endpoints:

- `/api/v1/health/live`: process responds, independent of dependencies.
- `/api/v1/health/ready`: checks PostgreSQL, the expected migration, pgvector and Redis; returns 503 when unavailable.
- `/api/v1/capabilities`: honest feature availability, without exposing credentials.

```sh
docker compose ps
docker compose logs --tail=80 api migrate web
docker compose down
```

`down` preserves named database/Redis volumes. Do not use `down --volumes` unless intentionally discarding this installation's data. This is a local development foundation, not a public hosting configuration: authentication and workspace authorization arrive in M1 before document endpoints.

## Develop and verify

Install the versions in `.python-version` / `.node-version`, **uv 0.13.8** and **pnpm 12.18.0**, then:

```sh
make setup
make check
make integration
make up
pnpm exec playwright install chromium
make e2e
```

`make check` runs Ruff, Python types, API unit tests, frontend formatting/types/tests and the web build. `make integration` builds a separate `traceleaf-test` Compose project and checks real migrations, a vector query and service readiness. It removes only that test project's containers and volumes afterward. Do not run two integration sessions concurrently. `make e2e` needs the running main Compose stack; it exercises desktop/mobile Chromium and a failed-request/retry path. Override `TRACELEAF_E2E_URL` if the web port changes.

To run the API and web with hot reload instead of their containers:

```sh
docker compose stop api web
docker compose -f compose.yaml -f infra/compose/dev.yaml up -d --wait postgres redis
uv run --locked alembic upgrade head
uv run --locked uvicorn traceleaf_api.main:create_app --factory --reload --host 127.0.0.1 --port 8000
# In a second terminal:
pnpm dev
```

Vite proxies `/api` to localhost:8000. The optional development overlay publishes PostgreSQL/Redis on loopback ports 55432/56379, matching the generated `.env`. No CORS wildcard is needed. For API migrations in Docker, use `docker compose run --rm migrate`.

## Repository

```text
apps/api/        FastAPI routes and typed HTTP responses
apps/web/        React / TypeScript / Vite, pt-BR interface
packages/core/   Shared settings, SQLAlchemy connection and Alembic migrations
tests/          API, real-service integration and Playwright tests
evals/fixtures/  Synthetic UC01 corpus and future evaluation reference
infra/compose/  Pinned Docker builds and isolated development/test configurations
docs/           Original specification, ADRs and evidence of implementation
```

AI, workers, editor, evaluation, telemetry, AWS/Terraform and MCP are introduced in later milestones. See [the required stack and evidence](docs/skills-evidence.md). Technical tests do not establish product demand or hiring outcomes.
