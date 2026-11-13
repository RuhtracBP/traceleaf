# Required stack and evidence

Status is about demonstrated behavior, not dependency counts. M0 implements a foundation; it is not yet an AI Engineer portfolio demonstration of RAG or agents.

| Required axis | Code / planned location | Verification | Current limitation / milestone |
|---|---|---|---|
| Python, FastAPI, Pydantic | `apps/api`, `packages/core` | API unit tests, mypy, real readiness endpoint | Foundation only; domain/auth in M1 |
| PostgreSQL, SQLAlchemy, Alembic | `packages/core/src/traceleaf_core/database.py`, `migrations/` | `make integration`: upgrade/repeat/downgrade/upgrade | No domain tables or transactions yet (M1) |
| pgvector + PostgreSQL full-text | pgvector enabled by migration | Integration executes a vector distance query | Extension only; retrieval/full-text pending M2 |
| Official model SDK + internal gateway | Planned `packages/ai` | Not run | Pending M2–M3; no provider selected or calls made |
| Configurable embeddings | Planned `packages/ai` | Not run | Pending M2; no index or configured dimensions |
| LangGraph | Planned `packages/ai` | Not run | Pending M3; no graph/checkpoints yet |
| Celery + Redis | Redis service and actual ping | Readiness + integration | Celery, outbox, durable jobs and idempotency pending M2–M4 |
| React, TypeScript, Vite, CodeMirror | `apps/web` | Typecheck, Vitest, Vite build, Playwright | Status UI only; CodeMirror/editor pending M1 |
| pytest + Ragas | `tests`; synthetic `evals/fixtures/uc01` | API unit/integration tests | No retrieval or Ragas evaluation yet (M2–M5) |
| OpenTelemetry + Langfuse | Planned in API/worker/model boundaries | Not run | Pending M4; transitive packages do not count as instrumentation |
| Ruff, types, Vitest, Playwright | `Makefile`, tests and browser config | `make check`, `make e2e` | M0 coverage only; file integrity/security scenarios pending |
| Docker, Compose, GitHub Actions | `infra/compose`, `compose.yaml`, `.github/workflows/ci.yml` | Build/start and checks defined in CI | See implementation status for actual local/remote execution evidence |
| AWS + Terraform | Planned `infra/terraform` | Not run | Pending M6; no infrastructure provisioned |
| Official MCP SDK | Planned `packages/mcp` | Not run | Pending M7; no MCP tools provided |

Version selection and update policy: [ADR 0002](adr/0002-stack-and-version-policy.md). Provider and budget decision: [ADR 0003](adr/0003-model-provider-and-execution-budget.md). Full acceptance tracking: [acceptance-matrix.md](acceptance-matrix.md).
