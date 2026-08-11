# How to organize `.status/`

How a `.status/` directory should be organized: the layout, the naming scheme, and an exit rule for every location. The
scheme was sized against a real survey of 25 grown `.status/` directories - 2,229 files, 185 MB, 70% of it not markdown
at all, 83% of the markdown untouched for 90+ days. The survey itself, with its per-repo counts, lives with the working
notes; what matters here is what it showed.

______________________________________________________________________

## The four failure modes of an unmanaged `.status/`

1. **It becomes a junk drawer.** In the survey, more than two thirds of all files were not notes: build logs, XML
   schemas, CSS, downloaded PDFs, stray test scripts. Every one of them has a real home elsewhere in its repo.

2. **Filenames encode completion state, so nothing says what is current.** One initiative accumulates `<name>_plan.md`,
   `<name>_status.md`, `<name>_complete.md`, and `<name>_completion.md` - and the newest is not obviously the truth.

3. **Nothing ever leaves.** The escape hatch is a subdirectory with a vague name - `temp`, `working`, `old_docs`,
   `leftovers`, `review_for_deletion`, `backup` - and none of them has a rule for when it gets emptied, so none ever
   does.

4. **Several naming schemes coexist.** `CamelCase.md` next to `snake_case.md` next to `2026-02-05_dated-kebab.md` next
   to `ALL_CAPS.md`. Sorting is meaningless, and you cannot guess a filename, so you `ls` and read.

### Why this matters more for Claude than for you

You can skim a several-hundred-file listing and ignore it. Claude cannot. Point it at `.status/` and it globs, reads,
and burns the context window on a stray build log before it reaches the plan you wanted. A `.status/` that is mostly
stale actively degrades every session that touches it - the directory that was supposed to *save* context starts costing
it.

That is the whole argument for the scheme below: **`.status/` must be small enough and predictable enough that Claude
can orient from it in one read.**

______________________________________________________________________

## The governing idea

The mess is not a naming problem. It is that **one directory is doing four jobs with four different lifetimes**, and
they are all mixed together at the top level:

| Job                            | Lifetime              | Read when?                           |
| ------------------------------ | --------------------- | ------------------------------------ |
| Why this repo is the way it is | permanent             | before proposing structural change   |
| What we are doing right now    | weeks                 | at the start of the work             |
| What happened on a given day   | write-once, then cold | only when explicitly hunting history |
| Throwaway                      | days                  | never                                |

Give each job its own place and the directory stops growing without bound, because each place has its own exit rule.

______________________________________________________________________

## The layout

```
.status/
  README.md               <- the index. The ONE file worth reading to orient.
  decisions.md            <- append-only log of WHY. Permanent.
  local-environment.md    <- machine specifics, tool-agnostic. Every tool reads it.
  config.md               <- this repo's retention settings. Optional; defaults apply.
  plans/                  <- active initiatives. One file each. THE ONLY HOT DIR.
    recursive_repo_metadata.md
    upstream_migration.md
  prompts/                <- working prompts: how to start or restart one piece of work.
    kick_off_repo_metadata.md
  notes/                  <- dated write-once records. Never edited after the day.
    2026-06-15_recursive_repo_metadata.md
    2026-07-23_crlf_lineending_fix.md
  archive/                <- finished. Never read unless explicitly asked.
    2026/
  scratch/                <- the workbench: any file type. Deleted unread after scratch_days.
```

Eight entries at the top level (nine with the optional `config.md`), forever. `ls .status/` stays useful no matter how
much history accumulates, because history lives in `archive/`, and `archive/` is something Claude is told not to read.

**Rules that make it work, in order of how much they matter:**

1. **`.status/` holds markdown only - except `scratch/`, which holds anything.** No `.py`, `.log`, `.xml`, `.tsv`,
   `.json`, `.css`, `.yaml`, `.pdf`, `.backup` anywhere else. In the survey this one rule accounted for 1,565 of the
   2,229 files. Everything non-markdown that is *kept* has a real home: live code -> `scripts/` or `src/`, test data ->
   `tests/data/`, CI config -> `.github/workflows/`. Everything non-markdown that is *throwaway* - the `test.py` an
   agent writes to try something, a downloaded sample, a one-off script - goes in `scratch/`, **never the repository
   root**, and expires unread after `scratch_days`. (One more exception: a small fixture a note is meaningless without
   goes in `notes/` beside the note.)

2. **The filename never encodes status.** Not `_complete`, not `_final`, not `_status`, not `_progress`, not `FINAL_v2`.
   Status is expressed by **which directory the file is in** and by a `Status:` line in its header. When a plan finishes
   it *moves* to `archive/2026/`; it is not renamed.

3. **One initiative, one plan file, edited in place.** If you want the history of how the plan changed, that is what the
   session notes in `notes/` are for. Four files named after one initiative is the disease, not the record.

4. **Only `plans/` and `prompts/` are ever edited.** `notes/` is write-once: a note records what happened on a day and
   is never revised, which is exactly why it can be trusted later. `decisions.md` is append-only.

5. **Nothing new is ever created at the `.status/` root.** New file -> `plans/`, `prompts/`, `notes/`, or `scratch/`. If
   you cannot tell which, it is `scratch/`.

6. **Every file opens with a `For humans:` summary.** Three or four sentences at the very top, before any other heading:
   what the file is, and the one or two things you need to take away from it. Everything below may be written for an
   assistant to consume; that block is not.

   This rule exists because of who writes these files. An assistant asked for a status note produces something thorough,
   structured, and long - optimised for being complete rather than for being read. Six months later you open it and have
   to reconstruct the point from four screens of prose. Requiring the summary forces the point to exist somewhere, in
   one place, in your language. It is also the cheapest quality check available: if the assistant cannot state the
   takeaway in three sentences, the document does not have one yet.

   No throat-clearing, no restating the title, no listing what the document will cover. Extend the same rule to answers
   in a session: lead with the conclusion.

7. **A plan is the work; a prompt is how to start it.** `plans/<slug>.md` holds the work itself - goal, decisions,
   steps. `prompts/<slug>.md` holds the words that hand that work to a fresh session, or restart one that has drifted;
   it is about one piece of work at one moment, and it is local and disposable. The test for where a prompt belongs:
   would someone else, in another repository, get value from it? If yes, it is illustrative and goes in the tracked
   `sample_prompts/` at the repo root, part of the repository's content; if it names your current task, it is a working
   prompt and goes in `.status/prompts/`.

______________________________________________________________________

## How an agent learns these rules

An agent never reads this document. A rule that matters to agent behaviour exists only if it is carried by one of four
channels - and a rule in none of them does not exist, however clearly it is stated here:

1. **`AGENTS.md`, loaded at the start of every session.** Its "Where the thinking lives" block and working agreements
   carry the few behavioural rules an agent actually needs: read `.status/README.md` first, `decisions.md` is
   append-only, do not read `archive/`, create nothing at the `.status/` root, temporary scripts and experiments go in
   `.status/scratch/` and never the repository root, open every `.status/` file with a `For humans:` summary, never
   delete or rewrite without asking. `templates/AGENTS.template.md` contains all of them.
2. **Path-scoped rules, loaded the moment the agent touches `.status/`.** `.claude/rules/status_conduct.md`, with
   `paths: [".status/**"]` in its frontmatter, re-injects the full conduct list exactly when it becomes relevant -
   including after `/compact` (Claude Code's context compression: when the window fills, the conversation is replaced by
   a summary, and instructions given mid-session survive only as what the summary kept). This is the channel for the
   detail that would bloat `AGENTS.md`. `templates/status_conduct.rules.template.md` is the copy-paste start;
   `templates/status_conduct.instructions.template.md` is the GitHub Copilot twin
   (`.github/instructions/status_conduct.instructions.md`, honored by the Copilot cloud agent and code review).
3. **`.status/README.md`, read on arrival.** Thirty lines is enough because it does not have to teach the scheme - it
   says what is where *in this repo*, what is active right now, and repeats the two or three prohibitions beside the
   directory they protect.
4. **`.claude/settings.json` deny rules and hooks, enforced regardless.** The `archive/` read-wall holds whether or not
   the agent read anything. (`scratch/` is deliberately *not* read-denied: it is the workbench, and an agent cannot
   iterate on a script it is forbidden to read back.)

Everything else in this document - the survey figures, the naming rationale, the exit times, the migration procedure -
is for the person setting the scheme up and tidying it, not for the agent. If an agent violates a rule that matters, the
fix is to add it to one of the four channels (or promote it from instruction to hook), not to write more prose here. And
bringing a repository up to this standard is a procedure, not a rule: `sample_prompts/conform_repo.md` runs the audit
against the checklists.

______________________________________________________________________

## Naming

One scheme, no exceptions:

| Directory       | Pattern                                 | Example                                                                   |
| --------------- | --------------------------------------- | ------------------------------------------------------------------------- |
| `plans/`        | `<slug>.md` - no date, no status        | `recursive_repo_metadata.md`                                              |
| `prompts/`      | `<slug>.md` - no date, no status        | `kick_off_repo_metadata.md`                                               |
| `notes/`        | `YYYY-MM-DD_<slug>.md` - **date first** | `2026-07-23_crlf_lineending_fix.md`                                       |
| `archive/YYYY/` | keeps whatever name it arrived with     |                                                                           |
| root            | fixed set of filenames only             | `README.md`, `decisions.md`, `local-environment.md`, optional `config.md` |

A plan gets no date because it is a living document and its creation date stops being interesting on day two. A note
gets a date *first* because that is the only position where sorting by name equals sorting by time. In the survey, 149
of 154 dated filenames had the date in the middle or at the end - flipping that is most of what makes a large `notes/`
directory navigable.

Character rules, which matter because these repos also get touched from Linux:

- lowercase only, ASCII only, `-` or `_` as separators, never a space. `HedMatlabTools.md copy.backup` fails all three.
- Never let two files differ only in case. Windows lets you think `README.md` and `readme.md` are two files; Linux
  agrees, and then one of them vanishes on the next checkout on Windows.
- Use `_` as the separator, never `-`. This is the decided convention across these repos - the dated notes already
  follow it, and the markdown filenames in `claude-advice` do too.

______________________________________________________________________

## How files leave

Each location gets one exit rule. The rules say *what* leaves; the day counts say *when*, and they are per-repo settings
with defaults - an actively developed library and a slow-moving dataset catalogue should not share a rhythm. A repo that
wants non-default counts declares them in `.status/config.md` (format below); everywhere else the defaults apply.

| Location               | Exit rule                                                                                                                                                                                                               |
| ---------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `scratch/`             | **Anything older than `scratch_days` (default 30) is deleted without being read.** That is the deal that makes `scratch/` safe to use freely.                                                                           |
| `plans/`               | A plan is *active* or it is gone. When it completes, or when it has had no activity for `plan_days` (default 60), it moves to `archive/YYYY/` - with a one-line outcome added to `decisions.md` if it decided anything. |
| `prompts/`             | Tied to one piece of work: when that work closes, delete the prompt, or move it to `archive/YYYY/` beside its plan if it captured anything worth keeping.                                                               |
| `notes/`               | Stays until the year turns, then the whole year moves to `archive/YYYY/`.                                                                                                                                               |
| `decisions.md`         | Never. It is the point.                                                                                                                                                                                                 |
| `local-environment.md` | Never; it is edited in place.                                                                                                                                                                                           |
| `config.md`            | Never; edited in place when the repo's rhythm changes.                                                                                                                                                                  |
| `archive/`             | Never read unless you name a file explicitly. Never pruned either - it is cheap, it is markdown, and it is the only history you have.                                                                                   |

Consequences:

**`.status/` is gitignored in every one of these repos** - verify in yours with `git ls-files .status`, which should
print nothing. So **`git` will not save you from a bad prune** - there is no `git checkout` to undo it, and no copy on
GitHub. Before any cleanup, snapshot the directory (see the migration section). This is also the strongest argument for
`archive/` over deletion: moving is reversible, deleting is not.

**Being gitignored means `.status/` is absent from fresh clones and from `claude --worktree` worktrees.** If you start
using worktrees, either list `.status/**` in a `.worktreeinclude` at the repo root, or accept that worktree sessions
start with no project memory.

### `config.md` - per-repo retention settings

Markdown, so the markdown-only rule holds; three `key: days` lines, so a script can parse it.
`templates/status_config.template.md` is the starting point:

```markdown
# Status configuration - <repo-name>

**For humans:** this repo's retention settings. Defaults apply to anything not
set here, and everywhere the file is absent.

scratch_days: 30
plan_days: 60
stale_days: 90
```

`stale_days` is what the triage script (`templates/status-triage.py`) uses to classify markdown as stale during a
migration; `scratch_days` and `plan_days` govern the manual tidy pass. Set them per repository: 30-day scratch fits an
active library, while a slow-moving archive of datasets might want 120 everywhere.

______________________________________________________________________

## `.status/README.md` orients agents to `.status`

Every repository should have a `.status/README` (ideally under 30 lines) that is the only `.status/` file `AGENTS.md`
needs to point at by name. It exists so that a session can orient in a single read instead of a glob. Start from
`templates/status_README.template.md`.

```markdown
# Status directory - <repo-name>

**For humans:** <what is going on in this repo right now, in two or three
sentences, and where to look first.>

Working notes for this repo. Gitignored: local to this machine, not on GitHub.

- `decisions.md` - why things are the way they are. Append; never rewrite.
- `plans/` - active initiatives, one file each, `[ ]`/`[x]` markers. Start here.
- `prompts/` - working prompts for starting or restarting the work in `plans/`. Disposable.
- `notes/` - dated records of what happened. Write-once. Reference only.
- `archive/` - finished work. **Do not read unless asked for a specific file.**
- `scratch/` - throwaway; anything here may be deleted without warning.
- `local-environment.md` - this machine's paths, interpreter, quirks.

## Active right now

- `plans/recursive_repo_metadata.md` - in progress, step 4 of 7.
- `plans/upstream_migration.md` - blocked on the upstream export finishing.

Last tidied: 2026-08-04.
```

The "Active right now" section is three lines you update when work changes state, and it is worth more than the rest of
the directory combined.

______________________________________________________________________

## Plan and note headers

Every plan file starts with the same four lines, so status is readable without parsing prose
(`templates/plan_doc.template.md` is the starting point). A plan file named `plans/recursive_repo_metadata.md` opens
like this:

```markdown
# Plan: recursive-tree-based repo metadata

**For humans:** <what this plan achieves, what state it is in, and what the next
action is - three sentences, before the header block.>

Status: active | blocked | done
Opened: 2026-06-15
Last touched: 2026-08-04
Supersedes: notes/2026-06-01_flat_entries_schema.md
```

Then goal, decisions, and steps with `[ ]` / `[x]`. A plan that already has Goal, Decisions, and Scope sections is close
\- usually all it needs is the status header and a home in `plans/`.

Notes need only a title and a date, because a note is a fact about a day. A note file named
`notes/2026-07-23_crlf_lineending_fix.md` - date first, so sorting by name sorts by time - looks like this inside:

```markdown
# 2026-07-23 - CRLF line-ending fix

**For humans:** <what happened that day and what it means for you now - two or three sentences.>

## Problem / What was done / Left for next session
```

A note in this form - title, date, three short sections - is the cheapest trustworthy record there is. Keep writing them
exactly that way.

______________________________________________________________________

## What `AGENTS.md` should say

Five lines, no more. Point at the index and the two files with authority; say explicitly what *not* to read, because
that is the instruction that saves context:

```markdown
## Where the thinking lives

`.status/` is gitignored - local to this machine, absent from clones and worktrees.

- `.status/README.md` - the index. Read this first; it lists what is active.
- `.status/decisions.md` - why things are the way they are. Read before proposing
  structural changes. Append entries; never rewrite one.
- `.status/plans/*.md` - active plans. Check the `Status:` header and the `[ ]`
  markers before starting work.
- IMPORTANT: do not read `.status/archive/` or `.status/notes/` unless I name a
  file. Do not delete or rewrite anything under `.status/` without asking.
```

And back the important half of that with a rule rather than a request. In the **committed** `.claude/settings.json` -
the pattern is repo-relative, so it is portable, and it is inert for a collaborator who has no `.status/`:

```json
{
  "permissions": {
    "deny": [
      "Read(.status/archive/**)"
    ]
  }
}
```

That is a real wall for Claude's file tools and for the Bash file commands it recognizes, and it means an archive can
grow to 10,000 files without ever costing you a token. If you want the same for `notes/`, add it - but notes are often
what you actually want found, so I would leave that one readable. Do **not** deny `scratch/`: it is the agents'
workbench, and an agent that cannot read a script back will not iterate on it there - it will fall back to leaving
`test.py` in the repository root.

______________________________________________________________________

## Migrating an existing directory

**The procedure is `06_status_migration.md`,** with the classification rules encoded in `templates/status-triage.py` so
you review a proposed plan instead of hand-sorting hundreds of files. This document describes the target; that one gets
you there.

The short version: snapshot the directory to a zip (it is not in git), run the triage script in dry-run mode, read and
correct the plan it writes, re-run with `--apply`, then do the two things no script can - harvest `decisions.md` and
write `README.md` with the "Active right now" list.

______________________________________________________________________

## Keeping it from happening again

Three things, in descending order of effect:

1. **The `.status/` root is closed.** A fixed set of filenames, and new material goes in a subdirectory. This is one
   line in `AGENTS.md` and one habit.
2. **`scratch/` with a real delete-unread rule.** The junk-drawer subdirectories exist because there was no sanctioned
   place for junk. Give junk a place with an expiry (`scratch_days`) and it stops colonizing everything else.
3. **A tidy pass when a plan closes, not on a schedule.** Plan completes -> move it to `archive/`, add its decision to
   `decisions.md`, update the "Active right now" list. Three minutes, at the one moment you have the context to do it
   correctly. Calendar-based cleanups do not happen; the survey's 25 directories prove it.

If you want it enforced rather than intended, a `PreToolUse` hook on `Write` can reject any path matching
`^\.status/[^/]+\.md$` that is not one of the allowed root filenames. Worth it only if you find yourself drifting back;
the rule is cheap to follow by hand.

______________________________________________________________________

## Should `.status/` be committed?

These repos gitignore it everywhere, and `01_repo_standards.md` says the same. **The call is the defensible one**, for
two reasons: the repos are public, and `.status/` holds half-formed thinking that becomes part of the permanent public
record the moment it is pushed.

The cost is real and worth naming: no backup, no visibility to collaborators, and nothing in worktrees. If you ever want
the middle path, the split is clean under this layout - commit `README.md`, `decisions.md`, and `plans/`; gitignore
`notes/`, `archive/`, `scratch/`, and `local-environment.md`:

```gitignore
.status/*
!.status/README.md
!.status/decisions.md
!.status/plans/
.status/local-environment.md
```

The decisions and the active plans are the two things whose loss would actually hurt, and they are also the two things
that are safe to publish. But an `archive/` you back up by hand once a quarter gets you most of the same protection
without publishing anything, and that is probably where I would leave it.

______________________________________________________________________

## One-page checklist

- [ ] Snapshot `.status/` to a zip outside the repo - it is not in git
- [ ] Skeleton: `README.md`, `decisions.md`, `plans/`, `prompts/`, `notes/`, `archive/YYYY/`, `scratch/` - plus
  `config.md` if this repo needs non-default retention
- [ ] `.status/` holds markdown only outside `scratch/`; everything else moved to a real home or deleted
- [ ] No filename contains `complete`, `final`, `status`, `progress`, or `summary`
- [ ] Every note is `YYYY-MM-DD_slug.md`, date first; every plan is `<slug>.md`, no date
- [ ] Every plan has a `Status:` header line
- [ ] Working prompts live in `.status/prompts/`; anything general enough for another repository is promoted to the
  tracked `sample_prompts/` at the repo root
- [ ] Every file opens with a `For humans:` summary, three or four sentences
- [ ] Nothing older than this repo's `stale_days` (default 90) sits outside `archive/`
- [ ] `README.md` exists and lists what is active
- [ ] `decisions.md` has at least one real entry harvested from the old files
- [ ] `Read(.status/archive/**)` denied in `.claude/settings.json`; `scratch/` left readable
- [ ] `AGENTS.md` says temporary scripts go in `.status/scratch/`, never the repository root
- [ ] `.claude/rules/status_conduct.md` present, with its `.github/instructions/` twin
- [ ] `AGENTS.md` points at `.status/README.md`, `.status/decisions.md`, `.status/plans/` - and says what not to read
- [ ] `.status/` is gitignored - `git ls-files .status` prints nothing
- [ ] Lowercase, ASCII, no spaces, no case-only differences anywhere
