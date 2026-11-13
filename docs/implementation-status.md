# Implementation status

Updated 2026-11-13. Source of acceptance criteria: [implementation plan](planning/ai-engineer/projeto-base-conhecimento-ia/09-plano-de-implementacao.md).

| Milestone | Status | Evidence / remaining work |
|---|---|---|
| M0 foundation | Implemented; validated locally | Monorepo, lockfiles, API/web, Compose, migration, CI configuration and ADRs; execution results below |
| M1 Markdown product | Pending | Identity/auth, workspaces, import, CodeMirror, history/export and integrity tests |
| M2 grounded retrieval | Pending | Full-text/vector/hybrid search, embeddings, official provider SDK, Celery/outbox and real-model evaluation |
| M3 proposals/review | Pending | Persistent LangGraph, proposals, review and safe apply/reconciliation |
| M4 operations | Pending | OpenTelemetry/Langfuse, budgets, cancellation, recovery and operational evidence |
| M5 measured quality/scale | Pending | Dataset, Ragas, model comparison, load and real product validation |
| M6 distribution/cloud | Pending | Release, backup/restore and AWS/Terraform; no cloud provisioned |
| M7 open source/portfolio | Pending | MCP, licensing, contributor/security guides, case study and video |

## M0 implementation

- Typed health/capability endpoints in `apps/api/src/traceleaf_api/main.py`. Liveness is independent of infrastructure. Readiness checks database connection, migration revision, pgvector and Redis. Errors do not return credentials.
- React pt-BR status screen in `apps/web`, with loading/failure/retry states and explicit future milestones. No fake documents, retrieval or chat.
- `uv` workspace and `pnpm` workspace with exact direct versions and lockfiles. Database image includes pgvector; first Alembic revision enables it.
- Compose starts services in dependency order and binds published ports to loopback. `.env` is generated with a random password; no personal folders or model credentials are mounted.
- `Makefile` and GitHub Actions run quality checks, isolated real-service tests and browser tests. A configured workflow is not evidence of a completed remote CI run.
- [UC01 fixture](../evals/fixtures/uc01/README.md), [product validation](product-validation.md), [storage](adr/0001-storage-and-boundaries.md), [stack/versions](adr/0002-stack-and-version-policy.md) and [model/budgets](adr/0003-model-provider-and-execution-budget.md).

## Verification record

Local host: macOS ARM64; Docker Engine 29.8.2 / Compose 5.5.0. Python 3.12.16, Node 26.13.1, uv 0.13.8, pnpm 12.18.0.

| Check | Observed result |
|---|---|
| API unit tests | 9 passed; dependency failure paths use test doubles |
| Python types | Passed for 9 source files |
| Frontend unit tests | 3 passed; mocked HTTP responses |
| TypeScript + Vite production build | Passed locally |
| Full consolidated `make check` | Passed: Ruff lint/format, mypy, pytest, Prettier, TypeScript, Vitest and Vite build |
| Docker installation / real services | Linux ARM64 images built with locked dependencies; web/API/PostgreSQL/Redis healthy; HTTP readiness returned 200 |
| Fresh-volume startup | Passed in an isolated Compose project: automatic migration and readiness through the web proxy; disposable test volumes removed afterward |
| Migrations / vector integration | 1 real-service test passed: upgrade twice, downgrade, upgrade, vector distance query, and 503/200 readiness transitions |
| Browser desktop/mobile | 6 Playwright tests passed: actual ready stack, simulated dependency failure and failed-request/retry; screenshots also inspected |
| GitHub Actions | Workflow written; remote run not observed |

No model, embedding, agent, cloud, performance or product-utility validation has run. M0 may establish infrastructure readiness only. See [acceptance matrix](acceptance-matrix.md) and [skills evidence](skills-evidence.md) before claiming a broader capability.

The first cold startup exposed a readiness race: `pg_isready` without a host accepted PostgreSQL's temporary initialization server over a Unix socket before TCP connections were possible. Compose now probes `127.0.0.1` and allows a startup period. The isolated fresh-volume startup above verified the correction. Integration tests remain separate from the installation's persistent data.

The tests currently emit upstream deprecation notices for the Starlette/httpx test client and Alembic's legacy path separator default; they do not affect the observed results. Remote GitHub Actions, Linux AMD64 and other browsers have not been observed in this session. Product validation and the final provider/model choice remain explicitly pending as described in the ADRs.
