# Conform a repository to the standard

For bringing any repository up to the shared configuration standard: the AGENTS.md wiring, the committed/local split, and the `.status/` layout. Run it from the repository being conformed, with the claude-advice checkout reachable. It audits first and changes nothing until the plan is approved.

```
Read, in <path to claude-advice>: 01_repo_standards.md (the per-repo checklist
at the end) and 05_status_directory.md (the one-page checklist at the end).

Audit this repository against both checklists. Produce a conformance table:
one row per checklist item - item, pass or fail, and the evidence (the command
you ran or the file you inspected). Measure; do not assume, and re-run any
measurement rather than quoting a cached or remembered result. Write this table to .status/notes/

Then write a plan to .status/plans/conform_repo.md containing only the failing
items, each with its concrete fix and one verification I can run, using
<path to claude-advice>/templates/ as the starting points. Open the plan with
a "For humans:" summary.

Do not change any other file until I have read the plan and said go.
```
