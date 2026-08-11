<!--
  CLAUDE.md template. Copy to <repo-root>/CLAUDE.md.

  COMMITTED, and deliberately almost empty: AGENTS.md is the single source of
  instructions for every assistant, and Claude Code does not read AGENTS.md,
  so it is imported below. Anything true of the repo goes in AGENTS.md, not
  here - a rule stated in two files is a rule that will disagree with itself.
  Only Claude-Code-specific behaviour belongs under the heading.
-->

@AGENTS.md

# Claude Code

- Path-scoped rules live in `.claude/rules/` and load automatically when a
  session touches files matching their `paths:` globs - for example,
  `status_conduct.md` applies under `.status/`. Nothing needs to reference
  them; this note exists so a reader knows they are there.
- `CLAUDE.local.md` (gitignored) holds notes about this machine's Claude Code
  setup and imports `.status/local-environment.md`, which is where machine
  facts live for every tool, not just this one.
- After changing either import, run `/context` and confirm the file appears
  under **Memory files**.
