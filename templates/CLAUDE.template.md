<!--
  CLAUDE.md template. Copy to <repo-root>/CLAUDE.md.

  COMMITTED, and deliberately almost empty: AGENTS.md is the single source of
  instructions for every assistant and is imported below. Anything true of
  the repo goes in AGENTS.md, not here - a rule stated in two files is a rule
  that will disagree with itself. The second import is the machine-facts
  file, gitignored; Claude Code skips a missing import silently, so a clone
  without it loads cleanly.
-->

@AGENTS.md

@.status/local-environment.md

# Claude Code

`AGENTS.md`, imported above, is the whole instruction set. `.status/local-environment.md`, also imported, holds this machine's paths and quirks for every tool. Path-scoped rules in `.claude/rules/` load when a session touches files matching their `paths:` globs - for example, `status_conduct.md` applies under `.status/`. After changing an import, run `/context` and confirm the file appears under **Memory files**.
