<!--
  AGENTS.md template. Copy to <repo-root>/AGENTS.md and fill in.

  COMMITTED AND PUBLIC, and the single source of instructions for every AI
  assistant working in the repo. Claude Code reads it through the @AGENTS.md
  import in CLAUDE.md (see CLAUDE.template.md); Copilot reads it directly.

  Write only what a reader needs going forward:
  - No project history: no dates, no "this was changed", no phase, session, or
    PR labels. Rationale about how the repo got here goes in
    .status/decisions.md, which is gitignored and is the place for that.
  - No ephemeral facts: no test counts, no version pins, no dataset counts.
    Point at the file that owns the fact.
  - Nothing machine-specific: no absolute paths, no drive letters, no secrets.
    Machine facts go in .status/local-environment.md.
  - No references to .status/ outside the "Where the thinking lives" section,
    whose job is to orient a tool.

  Delete every section you don't have a real answer for - an empty heading
  teaches nothing. Target: under 200 lines.
-->

# <repo-name>

Purpose: <what this repo produces or owns>.
Not in scope: <the thing people assume is here but is not>.

## Commands

Test framework: <unittest | pytest>. Never convert the suite from one style to
the other as a side effect of other work.

<!-- Only commands an assistant cannot guess. Verify each one actually works.
     Keep them repo-relative so they run anywhere. -->

- Install dev env: `<command>`
- Run tests: `<command>`
- Single test: `<command>`
- Lint / typecheck: `<command>`
- Validate data: `<command>`

## Layout

<!-- Two to six lines. Where things live, RELATIVE to the repo root. -->

- `<dir>/` - <what it owns>
- `<dir>/` - <what it owns>
- `.status/` - working notes. Gitignored; local to each machine.

## Conventions that differ from defaults

<!-- Only things that would surprise a competent stranger. A style rule true
     of EVERY project belongs in your user-level configuration; repeat it here
     only because the repo is public, so a collaborator still sees it. -->

- **ASCII only** in prose, code, comments, and filenames: `-` not em or en
  dashes, `->` not arrows, `...` not an ellipsis character, straight quotes.
  Exception: genuine data (author names, dataset titles, recorded API
  responses) keeps whatever characters it actually contains.
- <e.g. "Sidecar JSON is written with 2-space indent and sorted keys.">
- <e.g. "Column order in events.tsv is significant - never reorder.">

## Rules that are easy to get wrong

<!-- Non-obvious behaviour that has cost a session before. -->

- <e.g. "The citation cache is keyed by DOI, not dataset ID. Two datasets can
  share a citation.">

## Related repositories

<!-- Refer to sibling repos BY NAME, never by path. The path is
     machine-specific and lives in .status/local-environment.md. -->

- `<other-repo-name>` - <what it provides to this repo>. Not vendored here; a
  session that needs it must be granted access to that checkout.

## Where the thinking lives

`.status/` is gitignored, so it exists only on the machine that wrote it and
never in a fresh clone or worktree.

- `.status/README.md` - the index. Read this first; it lists what is active.
- `.status/decisions.md` - why things are the way they are. Read before
  proposing structural changes. Append entries; never rewrite one.
- `.status/plans/*.md` - active plans. Check the `Status:` header and the
  `[ ]` / `[x]` markers before starting work.
- `.status/local-environment.md` - this machine's paths, interpreter, and
  quirks. Tool-agnostic. Never copy its contents into a committed file.
- IMPORTANT: do not read `.status/archive/` unless a file is named for you.
  Nothing new is created at the `.status/` root.

## Working agreements

- IMPORTANT: every file written to `.status/` opens with a `For humans:`
  summary - three or four sentences, at the very top: what the file is and
  what a person needs to take from it. The same applies to a long answer in a
  session: lead with the conclusion.
- IMPORTANT: temporary scripts, experiments, and one-off test files go in
  `.status/scratch/` - **never the repository root**. Delete them when the
  experiment ends; anything in `scratch/` may be deleted unread.
- IMPORTANT: never delete or rewrite a file under `.status/` without asking
  first. Appending is fine.
- For a change spanning more than three files, write a plan to
  `.status/plans/` and stop for review before editing.
- When you are guessing about an external API or data format, say so
  explicitly rather than assuming.
- Show evidence, not assertions: the command you ran and its actual output.
- Do not commit, push, or create branches unless asked.
