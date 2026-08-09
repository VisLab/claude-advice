# How to organize `.status/`

Written 2026-08-04, after surveying every `.status/` directory reachable on this
machine. Unlike the other files in this folder, this one is not general advice -
it is a diagnosis of your 25 actual directories and a scheme sized to fix them.

---

## What the survey found

25 repositories under `H:\Repos`, `H:\Research`, and `I:\RepositoryMetadata`
have a `.status/` directory. Together they hold **2,229 files, about 185 MB**.

| Measure | Count | What it means |
| --- | --- | --- |
| Total files | 2,229 | |
| Markdown files | 664 | the only thing `.status/` is *for* |
| **Non-markdown files** | **1,565** | code, logs, XML, TSV, CSS, `.yaml`, PDFs, `.backup` |
| Markdown untouched in 90+ days | **552 of 664 (83%)** | the directory is mostly archive, but nothing says so |
| Filenames containing `complete` / `final` / `summary` / `report` / `progress` | 85 | files named after their own state |
| Filenames carrying a date | 154 of 664 (23%) | and only 5 put the date first, so sorting does nothing |
| `.backup` / `.bak` / `.tmp` / `.log` / `copy` files | 48 | pure noise |
| ALL_CAPS filenames | 35 | a third naming convention, alongside `snake_case` and `kebab-case` |
| Directories with a `README.md` index | **3 of 25** | nothing tells you where to start |
| Directories with `local-environment.md` | 12 of 25 | your one convention that actually propagated |
| `.status/` **not** gitignored | 2 (`hed-ontology`, `H:\Research\OpenAlex`) | their files sit in `git status` as `??` forever |

The worst four: `hed-resources` (457 files, 31 MB), `hed-python` (396, 28 MB),
`hed-server` (177), `table-remodeler` (170). `task-research` has 170 files but
156 are markdown - it is large but it is the *right kind* of large.

### The four failure modes, with your own examples

1. **`.status/` became a junk drawer.** 1,565 of 2,229 files are not notes.
   `HED8.5.0.xml`, `sphinx_build3.log`, `pyproject.toml`, `custom.css`,
   `layout.html`, `downloaded_paper.pdf`, `requirements.txt`, `black.yaml`,
   `osa-chat-widget.js`, `test_pandas3_deep_dive.py`, `create_ontology.py`.
   Every one of these has a real home elsewhere in its repo.

2. **Filenames encode completion state, so you cannot tell what is current.**
   `table-remodeler` alone has `documentation_integration_plan.md`,
   `documentation_integration_status.md`,
   `documentation_integration_complete.md`, and
   `documentation_integration_completion.md` - four files for one initiative,
   and the newest is not obviously the truth. Also `FINAL_STATUS.md` next to
   `FINAL_STATUS_REPORT.md`; `ENHANCEMENT_PROGRESS_REPORT.md` next to
   `COMPLETE_ENHANCEMENT_REPORT.md` next to `ENHANCEMENT_SUMMARY.md`.

3. **Nothing ever leaves.** The escape hatch you reached for was a subdirectory
   with a vague name, and there are now dozens: `temp`, `temp_files`,
   `temp_tsv_test`, `mainTemp`, `working`, `working_original`,
   `working_second_draft`, `original`, `original_2`, `original_3`, `oldStuff`,
   `old_docs`, `leftovers`, `unused`, `removed`, `review_for_deletion`,
   `merged`, `unmerged`, `backup`, `chat1`, `chat2`. None of these has a rule
   for when it gets emptied, so none ever does.

4. **Four naming schemes coexist.** In `hed-schemas`: `HedSchemas.md`,
   `action_versions.md`, `2026-02-05_removed-build-scripts.md`,
   `SETUP_COMPLETE.md`. Sorting is meaningless, and you cannot guess a filename,
   so you `ls` and read.

### Why this matters more for Claude than for you

You can skim a 457-file listing and ignore it. Claude cannot. Point it at
`.status/` and it globs, reads, and burns the context window on
`sphinx_build2.log` before it reaches the plan you wanted. A `.status/` that is
83% stale actively degrades every session that touches it - the directory that
was supposed to *save* context starts costing it.

That is the whole argument for the scheme below: **`.status/` must be small
enough and predictable enough that Claude can orient from it in one read.**

---

## The governing idea

The mess is not a naming problem. It is that **one directory is doing four jobs
with four different lifetimes**, and they are all mixed together at the top
level:

| Job | Lifetime | Read when? |
| --- | --- | --- |
| Why this repo is the way it is | permanent | before proposing structural change |
| What we are doing right now | weeks | at the start of the work |
| What happened on a given day | write-once, then cold | only when explicitly hunting history |
| Throwaway | days | never |

Give each job its own place and the directory stops growing without bound,
because each place has its own exit rule.

---

## The layout

```
.status/
  README.md               <- the index. The ONE file worth reading to orient.
  decisions.md            <- append-only log of WHY. Permanent.
  local-environment.md    <- machine specifics. Keep; 12 repos already have it.
  plans/                  <- active initiatives. One file each. THE ONLY HOT DIR.
    recursive-repo-metadata.md
    nemar-reorientation.md
  notes/                  <- dated write-once records. Never edited after the day.
    2026-06-15_recursive_repo_metadata.md
    2026-07-23_crlf_lineending_fix.md
  archive/                <- finished. Never read unless explicitly asked.
    2026/
  scratch/                <- throwaway. Deletable without reading. No exceptions.
```

Seven entries at the top level, forever. `ls .status/` stays useful no matter
how much history accumulates, because history lives in `archive/`, and
`archive/` is something Claude is told not to read.

**Rules that make it work, in order of how much they matter:**

1. **`.status/` holds markdown only.** No `.py`, `.log`, `.xml`, `.tsv`, `.json`,
   `.css`, `.yaml`, `.pdf`, `.backup`. This single rule removes 1,565 of your
   2,229 files. Everything non-markdown has a real home: live code -> `scripts/`
   or `src/`, test data -> `tests/data/`, CI config -> `.github/workflows/`, logs
   and backups -> delete. The only exception is a small fixture a note is
   meaningless without, and it goes in `notes/` beside the note.

2. **The filename never encodes status.** Not `_complete`, not `_final`, not
   `_status`, not `_progress`, not `FINAL_v2`. Status is expressed by **which
   directory the file is in** and by a `Status:` line in its header. When a plan
   finishes it *moves* to `archive/2026/`; it is not renamed.

3. **One initiative, one plan file, edited in place.** If you want the history
   of how the plan changed, that is what the session notes in `notes/` are for.
   Four files named after one initiative is the disease, not the record.

4. **Only `plans/` is ever edited.** `notes/` is write-once: a note records what
   happened on a day and is never revised, which is exactly why it can be
   trusted later. `decisions.md` is append-only.

5. **Nothing new is ever created at the `.status/` root.** New file -> `plans/`,
   `notes/`, or `scratch/`. If you cannot tell which, it is `scratch/`.

6. **Every file opens with a `For humans:` summary.** Three or four sentences at
   the very top, before any other heading: what the file is, and the one or two
   things you need to take away from it. Everything below may be written for an
   assistant to consume; that block is not.

   This rule exists because of who writes these files. An assistant asked for a
   status note produces something thorough, structured, and long - optimised for
   being complete rather than for being read. Six months later you open it and
   have to reconstruct the point from four screens of prose. Requiring the
   summary forces the point to exist somewhere, in one place, in your language.
   It is also the cheapest quality check available: if the assistant cannot state
   the takeaway in three sentences, the document does not have one yet.

   No throat-clearing, no restating the title, no listing what the document will
   cover. Extend the same rule to answers in a session: lead with the conclusion.

---

## Naming

One scheme, no exceptions:

| Directory | Pattern | Example |
| --- | --- | --- |
| `plans/` | `<slug>.md` - no date, no status | `recursive-repo-metadata.md` |
| `notes/` | `YYYY-MM-DD_<slug>.md` - **date first** | `2026-07-23_crlf_lineending_fix.md` |
| `archive/YYYY/` | keeps whatever name it arrived with | |
| root | fixed set of four filenames only | |

A plan gets no date because it is a living document and its creation date stops
being interesting on day two. A note gets a date *first* because that is the only
position where sorting by name equals sorting by time. You currently have 149
files with the date in the middle or at the end and 5 with it in front - flipping
that is most of what makes a large `notes/` directory navigable.

Character rules, which matter because these repos also get touched from Linux:

- lowercase only, ASCII only, `-` or `_` as separators, never a space.
  `HedMatlabTools.md copy.backup` fails all three.
- Never let two files differ only in case. Windows lets you think
  `README.md` and `readme.md` are two files; Linux agrees, and then one of them
  vanishes on the next checkout on Windows.
- Pick `-` or `_` per repo and stay consistent. I would use `_` since your
  existing dated notes already do.

---

## How files leave

This is the part that was missing, and it is the whole difference between a
notes directory and a landfill. Each location gets one exit rule:

| Location | Exit rule |
| --- | --- |
| `scratch/` | **Anything older than 30 days is deleted without being read.** That is the deal that makes `scratch/` safe to use freely. |
| `plans/` | A plan is *active* or it is gone. When it completes, or when it has had no activity for 60 days, it moves to `archive/YYYY/` - with a one-line outcome added to `decisions.md` if it decided anything. |
| `notes/` | Stays until the year turns, then the whole year moves to `archive/YYYY/`. |
| `decisions.md` | Never. It is the point. |
| `local-environment.md` | Never; it is edited in place. |
| `archive/` | Never read unless you name a file explicitly. Never pruned either - it is cheap, it is markdown, and it is the only history you have. |

Two consequences worth stating plainly:

**`.status/` is gitignored in every one of your repos** (I verified: zero tracked
`.status` files across all 40 repos on this machine). So **`git` will not save you
from a bad prune** - there is no `git checkout` to undo it, and no copy on GitHub.
Before any cleanup, snapshot the directory (see the migration section). This is
also the strongest argument for `archive/` over deletion: moving is reversible,
deleting is not.

**Being gitignored means `.status/` is absent from fresh clones and from
`claude --worktree` worktrees.** If you start using worktrees, either list
`.status/**` in a `.worktreeinclude` at the repo root, or accept that worktree
sessions start with no project memory.

---

## `README.md` - the file that makes the rest work

Three of your 25 directories have one. It should be in all of them, it should be
under 30 lines, and it is the only `.status/` file `CLAUDE.md` needs to point at
by name. It exists so that a session can orient in a single read instead of a
glob.

```markdown
# Status directory - <repo-name>

**For humans:** <what is going on in this repo right now, in two or three
sentences, and where to look first.>

Working notes for this repo. Gitignored: local to this machine, not on GitHub.

- `decisions.md` - why things are the way they are. Append; never rewrite.
- `plans/` - active initiatives, one file each, `[ ]`/`[x]` markers. Start here.
- `notes/` - dated records of what happened. Write-once. Reference only.
- `archive/` - finished work. **Do not read unless asked for a specific file.**
- `scratch/` - throwaway; anything here may be deleted without warning.
- `local-environment.md` - this machine's paths, interpreter, quirks.

## Active right now

- `plans/recursive-repo-metadata.md` - in progress, step 4 of 7.
- `plans/nemar-reorientation.md` - blocked on the nemar export finishing.

Last tidied: 2026-08-04.
```

The "Active right now" section is three lines you update when work changes state,
and it is worth more than the other 400 files combined.

---

## Plan and note headers

Every plan file starts with the same four lines, so status is readable without
parsing prose:

```markdown
# Plan: recursive-tree-based repo metadata

**For humans:** <what this plan achieves, what state it is in, and what the next
action is - three sentences, before the header block.>

Status: active | blocked | done
Opened: 2026-06-15
Last touched: 2026-08-04
Supersedes: notes/2026-06-01_flat_entries_schema.md
```

Then goal, decisions, and steps with `[ ]` / `[x]`. Your existing
`plan_2026-06-15_recursive_repo_metadata.md` in `hed-metadata-toolkit` is already
close to this - it has Goal, Decisions, Schema, and Scope sections and reads well.
It just needs the status header and a home in `plans/`.

Notes need only a title and a date, because a note is a fact about a day:

```markdown
# 2026-07-23 - CRLF line-ending fix

**For humans:** <what happened that day and what it means for you now - two or
three sentences.>

## Problem / What was done / Left for next session
```

Your `session_2026-07-23_crlf-lineending-fix.md` is a genuinely good example of
this form. Keep writing them exactly that way.

---

## What `CLAUDE.md` should say

Five lines, no more. Point at the index and the two files with authority; say
explicitly what *not* to read, because that is the instruction that saves context:

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

And back the important half of that with a rule rather than a request. In the
**committed** `.claude/settings.json` - the pattern is repo-relative, so it is
portable, and it is inert for a collaborator who has no `.status/`:

```json
{
  "permissions": {
    "deny": [
      "Read(.status/archive/**)",
      "Read(.status/scratch/**)"
    ]
  }
}
```

That is a real wall for Claude's file tools and for the Bash file commands it
recognizes, and it means an archive can grow to 10,000 files without ever costing
you a token. If you want the same for `notes/`, add it - but notes are often what
you actually want found, so I would leave that one readable.

---

## Migrating an existing directory

**The procedure is `06-status-migration.md`,** with the classification rules
encoded in `templates/status-triage.py` so you review a proposed plan instead of
hand-sorting 457 files. This document describes the target; that one gets you
there.

The short version: snapshot the directory to a zip (it is not in git), run the
triage script in dry-run mode, read and correct the plan it writes, re-run with
`--apply`, then do the two things no script can - harvest `decisions.md` and write
`README.md` with the "Active right now" list.

---

## Keeping it from happening again

Three things, in descending order of effect:

1. **The `.status/` root is closed.** Four filenames, and new material goes in a
   subdirectory. This is one line in `CLAUDE.md` and one habit.
2. **`scratch/` with a real 30-day delete rule.** The junk-drawer subdirectories
   exist because there was no sanctioned place for junk. Give junk a place with
   an expiry and it stops colonizing everything else.
3. **A tidy pass when a plan closes, not on a schedule.** Plan completes ->
   move it to `archive/`, add its decision to `decisions.md`, update the "Active
   right now" list. Three minutes, at the one moment you have the context to do
   it correctly. Calendar-based cleanups do not happen; you have 25 directories
   proving it.

If you want it enforced rather than intended, a `PreToolUse` hook on `Write` can
reject any path matching `^\.status/[^/]+\.md$` that is not one of the four
allowed root filenames. Worth it only if you find yourself drifting back; the
rule is cheap to follow by hand.

Two loose ends from the survey while you are in there:

- `hed-ontology` and `H:\Research\OpenAlex` do not gitignore `.status/`, so those
  files show as untracked in every `git status`. Add the line.
- `hed-typescript` has an empty `.status/`. Delete it or leave it; it costs
  nothing either way.

---

## Should `.status/` be committed?

`01-repo-standards.md` says commit it. You have gitignored it in all 25 repos.
**Your call is the defensible one and I would not change it**, for two reasons I
did not have when I wrote that file: these repos are public, and `.status/` holds
half-formed thinking that becomes part of the permanent public record the moment
it is pushed.

The cost is real and worth naming: no backup, no visibility to collaborators, and
nothing in worktrees. If you ever want the middle path, the split is clean under
this layout - commit `README.md`, `decisions.md`, and `plans/`; gitignore
`notes/`, `archive/`, `scratch/`, and `local-environment.md`:

```gitignore
.status/*
!.status/README.md
!.status/decisions.md
!.status/plans/
.status/local-environment.md
```

The decisions and the active plans are the two things whose loss would actually
hurt, and they are also the two things that are safe to publish. But an
`archive/` you back up by hand once a quarter gets you most of the same
protection without publishing anything, and that is probably where I would leave
it.

---

## One-page checklist

- [ ] Snapshot `.status/` to a zip outside the repo - it is not in git
- [ ] Skeleton: `README.md`, `decisions.md`, `plans/`, `notes/`, `archive/YYYY/`, `scratch/`
- [ ] `.status/` holds markdown only; everything else moved to a real home or deleted
- [ ] No filename contains `complete`, `final`, `status`, `progress`, or `summary`
- [ ] Every note is `YYYY-MM-DD_slug.md`, date first; every plan is `<slug>.md`, no date
- [ ] Every plan has a `Status:` header line
- [ ] Every file opens with a `For humans:` summary, three or four sentences
- [ ] Nothing older than 90 days sits outside `archive/`
- [ ] `README.md` exists and lists what is active
- [ ] `decisions.md` has at least one real entry harvested from the old files
- [ ] `Read(.status/archive/**)` and `Read(.status/scratch/**)` denied in `.claude/settings.json`
- [ ] `CLAUDE.md` points at `README.md`, `decisions.md`, `plans/` - and says what not to read
- [ ] `.status/` is gitignored (check `hed-ontology` and `OpenAlex`)
- [ ] Lowercase, ASCII, no spaces, no case-only differences anywhere
