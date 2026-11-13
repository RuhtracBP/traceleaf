# Lock an executable foundation, introduce AI dependencies with behavior

M0 uses Python 3.12.16, uv 0.13.8, Node 26.13.1 and pnpm 12.18.0. Python 3.12 leaves room for the planned evaluation and AI ecosystem; Node matches the verified local runtime and Vite requirements. Runtime identifiers live in `.python-version`, `.node-version`, package metadata, CI and Dockerfiles. Direct dependencies are exact versions; `uv.lock` and `pnpm-lock.yaml` fix the resolved dependency graphs.

FastAPI/Pydantic provide typed HTTP contracts; SQLAlchemy/psycopg and Alembic establish database access and migrations; React/TypeScript/Vite provide the web application. PostgreSQL 17 with pgvector 0.8.7 and Redis 8.8.4 run in Compose. Docker base images and GitHub Actions are pinned by digest/SHA. The initial migration enables vector support without prematurely inventing M1 domain tables. Rolling back the application revision intentionally retains the extension to avoid deleting shared database infrastructure.

Later required technologies remain in [skills-evidence.md](../skills-evidence.md). In particular, installing pgvector does not implement RAG, and connecting Redis does not implement durable jobs. Add LangGraph, Celery, CodeMirror, Ragas, OpenTelemetry/Langfuse, provider SDK and MCP with their corresponding behavior, lockfiles and tests. Review compatibility at that point.

Updates must change manifest/lockfiles and any relevant runtime/image pins together, then pass checks, real-service integration, image builds and browser tests. An exact version is reproducible, not permanently secure; dependencies need continued review.

Implementation references: [uv in Docker](https://docs.astral.sh/uv/guides/integration/docker/), [Vite runtime requirements](https://vite.dev/guide/), [FastAPI lifespan](https://fastapi.tiangolo.com/advanced/events/), [pgvector](https://github.com/pgvector/pgvector). Package versions were checked against PyPI/npm and image identifiers against their registries on 2026-11-13.
