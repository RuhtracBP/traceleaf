# Keep Markdown portable and metadata durable

Traceleaf uses a monorepo with a shared Python core. Managed Markdown files will be canonical content; PostgreSQL will own identities, revisions, approvals, jobs and audit records. Search indexes are rebuildable projections. Filesystem storage keeps notes portable and compatible with Obsidian, but PostgreSQL and the filesystem cannot share an atomic transaction: M3 must implement the planned journal and reconciliation protocol.

External folders remain read-only in v1. Importing a copy creates a managed workspace, not two-way synchronization. Multiple hosts writing separate local disks are unsupported; horizontal scaling of writers requires a different storage adapter and coordination. No vault is mounted by M0.

`apps/api` owns HTTP contracts and `packages/core` owns shared configuration/persistence. AI, workers and MCP packages are added when their milestones introduce real behavior, not as empty runnable services. This preserves the planned boundaries without presenting stubs as implemented capabilities.
