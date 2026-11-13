# Acceptance tracking

The original specification remains authoritative. A working health dashboard does not satisfy the document/RAG requirements below.

| Requirement | Status | Planned evidence | Milestone |
|---|---|---|---|
| RF01 workspaces | Pending | Workspace switching and authorization integration tests | M1 |
| RF02 import | Pending | Import, duplicates, invalid files and progress tests | M1 |
| RF03 library | Pending | Tree/filter/browser tests | M1 |
| RF04 Markdown reader/editor | Pending | Safe preview, frontmatter and revision preconditions | M1 |
| RF05 create/move/archive | Pending | Collision, affected links and restore tests | M1 |
| RF06 hybrid search | Pending | Text/vector/hybrid baselines | M2 |
| RF07 grounded answers | Pending | Snapshot citations and insufficient evidence | M2 |
| RF08 source ingestion | Pending | Immutable source provenance | M3 |
| RF09 structured proposals | Pending | Create/update/no-change evaluation | M3 |
| RF10 review | Pending | Diff/edit/reject/approve e2e | M3 |
| RF11 approved/current apply | Pending | Approval hash, version and concurrency tests | M3 |
| RF12 history/restore | Pending | New revision, preserved audit trail | M1/M3 |
| RF13 execution status | Pending | Progress/errors/cost/cancel tests | M3/M4 |
| RF14 export | Pending | Portable Markdown and proposal exports | M1/M3 |
| RF15 provider configuration | Pending | Consent/exclusions/capability tests | M2 |
| RF16 pt-BR interface | Partial | M0 status screen is pt-BR; domain flows pending | M0–M3 |

All mandatory technologies are tracked individually in [skills-evidence.md](skills-evidence.md).

| Critical integrity scenario | Status | Milestone |
|---|---|---|
| Edited proposal invalidates approval | Pending | M3 |
| Changed note causes conflict, no overwrite | Pending | M1/M3 |
| Concurrent/repeated apply has one logical effect | Pending | M3 |
| Crash after file replacement reconciles metadata | Pending | M3/M4 |
| Crash before write leaves original intact | Pending | M3/M4 |
| Traversal and escaping symlink refused | Pending | M1 |
| Workspace isolation across jobs/citations/cache | Pending | M1–M4 |
| Prompt injection cannot expand permissions | Pending | M3 |
| Invented target/citation blocks proposal | Pending | M3 |
| Restore checks current revision and preserves history | Pending | M1/M3 |

| Evaluation / operational artifact | Status | Milestone |
|---|---|---|
| Reproducible 120-case dataset, dev/test split and baselines | Only synthetic UC01 seed exists; no scores claimed | M2/M5 |
| Ragas and human audit | Pending | M5 |
| Real provider comparison and dated cost table | Pending | M2/M5 |
| Load/capacity measurements | Pending | M5 |
| Trace and failure/recovery report | Pending | M4 |
| Backup/restore runbook and tested recovery | Pending | M6 |
| AWS/Terraform validation and authorized deployment | Pending | M6 |
| Utility comparison with existing workflow | [Protocol ready; results pending](product-validation.md) | M3/M5 |
| Public case study, demo/video, license and contribution/security guides | Pending | M7 |
