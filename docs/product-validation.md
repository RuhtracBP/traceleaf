# Product validation

Initial scenario: **UC01 — a technical decision affects several documents**.

The intended user is a solo developer maintaining project documentation in Markdown. Today they use an editor or Obsidian, text search, Git and possibly an AI assistant to locate affected instructions, compare sources, edit and check the result.

The hypothesis is that Traceleaf can reduce the total time spent locating and updating affected documentation while preserving evidence and human control. Installation, ingestion, waiting, review and corrections must count toward that time. This is a hypothesis, not a demonstrated saving or evidence of demand.

## Available examples

`evals/fixtures/uc01/` contains original synthetic Markdown: three affected documents, one similar but unaffected document, and an incoming decision. `expected.json` records the human-authored reference and an intentional information gap. It supports future technical tests; it is not a real customer dataset or a completed RAG evaluation. Nothing in this fixture executes a deployment.

No personal vault is connected. No real participants, consenting examples or measured product results are available yet.

## Comparison protocol — pending

1. Collect up to ten authorized real changes and the documents that should change. Record frequency and provenance; redact private material before publication.
2. Prepare snapshots and a human reference, including irrelevant documents and no-change cases.
3. Measure the existing workflow, including any AI assistance already used: search, comparison, editing, verification and corrections.
4. Measure equivalent tasks with Traceleaf after M3. Alternate order or use comparable tasks to reduce learning effects.
5. Compare total time, missed documents, false positives, incorrect edits and accept/edit/reject decisions with reasons. Review accepted output against the reference.
6. Separate author observations, external feedback and synthetic benchmarks. Report failures and whether installation/review costs outweighed benefits.

| Evidence | Status |
|---|---|
| Synthetic UC01 fixture | Available; not automatically imported |
| Ten real changes | Pending |
| Existing-workflow baseline | Pending |
| Prototype comparison | Pending M3 and authorized examples |
| External feedback | Pending |
| Benefit or demand proven | No |
