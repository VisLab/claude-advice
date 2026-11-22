# Migrating an existing `.status/` directory

`05_status_directory.md` describes the target layout and why. This document is the procedure for getting a directory that already has hundreds of files in it to that layout, and it is deliberately separate because the two get read at different times: the target once, the procedure once per repo.

The classification rules live in `templates/status-triage.py`, which **proposes** a plan and changes nothing unless you pass `--apply`.

______________________________________________________________________

## Before you start

`.status/` is gitignored in every one of these repos. There is **no `git checkout`, no `git stash`, and nothing on GitHub.** A wrong `Move-Item` is a permanent loss of the only copy.

Everything below follows from that:

- The script **never deletes**. Noise and non-markdown go to `scratch/`, flattened, and are deleted only when the developer asks - after living without them for a week.
- The script **never overwrites**. A destination collision becomes `name_2.md`.
- Your snapshot first. Not optional.

```powershell
# From the repo root. Adjust the name.
Compress-Archive -Path .status\* -DestinationPath ..\status-backup-<repo-name>-<date>.zip
```

```bash
# POSIX equivalent
tar czf ../status-backup-$(basename "$PWD")-$(date +%F).tgz .status
```

______________________________________________________________________

## Which repo first

Do the small ones first. Not for safety - for calibration. You want to find out whether you actually like the scheme on a 5-file directory, not discover it on the one with 457. A sensible order: a tiny repo that is already otherwise in shape (it becomes the reference example), then one whose files are mostly well-named dated notes (tests the `notes/` renaming without much judgment), then the hub with real active plans (tests the plan/harvest distinction), then everything else, and the near-pure-archive giants last - boring by the time you get there, which is the goal.

______________________________________________________________________

## The procedure

### Step 1 - dry run

```
# same in PowerShell and bash
python <path to claude-advice>/templates/status-triage.py <path to the repo>
```

It walks `.status/`, classifies every file, writes a tab-separated plan next to the repo, and prints a summary. Nothing is moved. Real output from one of the directories the script was tested on:

```
### <repo> - 170 files
      7  plan        candidate ACTIVE work - read these, they are the whole point
      8  harvest     decision records - copy their substance into decisions.md
     29  note        dated record -> notes/, renamed date-first
    121  archive     finished or stale -> archive/<year>/ (flat)
      4  review      non-markdown - YOUR CALL
      1  quarantine  noise and junk-drawer non-markdown -> scratch/
```

Read those numbers as the answer to "is this worth doing": that repo goes from a 170-file listing to **7 plans and 29 notes in view**. The most extreme directory tested went from 457 files to 2 in view.

### Step 2 - read the plan and correct it

The plan is a TSV with `action`, `source`, `destination`, `kb`, `modified`, `reason`. Open it in Excel or VS Code. The columns you care about:

- **`action = review`** - the script refuses to guess where non-markdown belongs. These are yours to route. For each: does anything still run or import it? Then `scripts/` or `src/` or `tests/data/`, and commit it. Otherwise accept the `scratch/` destination it proposed - non-markdown never goes to `archive/`. A code-heavy directory can have dozens of these; that is where most of the correction time goes.
- **`action = plan`** - candidate *active* work, and the script says CONFIRM for a reason. It only knows the file is recent and named like a plan. Read each one. Half will turn out to be finished; change their destination to `archive/completed_plans/`, name unchanged. Check the date the script put in front of each name: it is the date in the old name, else the last-modified time; correct it to the day the plan was opened.
- **`action = harvest`** - decision records. Leave the destination alone; the work is step 4.
- **Everything else** - `archive`, `note`, `quarantine`, `keep` - is rule-driven and rarely needs a correction.

Editing the `destination` cell is how you override. The script honors whatever the column says, so an edited plan is the source of truth on apply. Anything you delete the row for is simply left where it is.

### Step 3 - apply

```
# same in PowerShell and bash
python <path to claude-advice>/templates/status-triage.py <path to the repo> --apply
```

It creates directories as needed, moves each file, refuses to overwrite, and removes directories the moves left empty. It re-derives the plan by default; pass `--plan <path>` to apply the exact file you edited.

Verify:

```
# `ls` works in PowerShell and bash alike
ls .status
# expect: archive, notes, plans, prompts, README.md, decisions.md, development_history.md, local-environment.md, scratch
```

### Step 4 - keep only the decisions that still govern (agent work; you skim)

The `harvest` rows are old files whose names say "decision". Most of them no longer matter: a decision that no longer governs how the code or data is handled *today* is history, and history goes to `archive/` unread. The reorganization itself is housekeeping and gets no `decisions.md` entry at all - `decisions.md` records rulings, not tidying.

The one thing worth extracting is the ruling a future session would otherwise re-litigate, and extracting it is agent work, not yours:

```
Read the files under .status/notes/ that came from action=harvest rows, plus
the plans that survived step 2. For each, answer one question: does this still
govern how the code or data is handled today? If no, propose moving it to
archive/. If yes, draft a decisions.md entry - date, what was decided, why,
what it supersedes - four lines, like:

  ## 2026-04-28 - Stable cache keys for lookups, not date-bucketed

  Date-bucketed keys meant a re-run on a new day re-fetched everything and the
  "immutable cache" guarantee did nothing for lookups.

  Consequence: lookup caches key on the identifier alone. Response caches stay
  date-bucketed.
  Superseded: notes/2026-04-28_stable_cache_for_lookups.md (kept; do not act on it).

Show me the drafts and the archive list. Do not write any file.
```

Your part is skimming the drafts and saying which go in - minutes, not an afternoon. Expect most candidates to be archived.

### Step 5 - write the index and wire it up

1. `.status/README.md` from `templates/status_README.template.md`, ending with its ordered `Next` list - worth more than everything you just archived - and `.status/development_history.md` from `templates/status_development_history.template.md`.
2. Make sure the repo's **committed** `.claude/settings.json` has no `Read(.status/archive/**)` deny; an older setup may carry one, and it blocks the named-file exception (see `05_status_directory.md`).
3. Add the "Where the thinking lives" block to `AGENTS.md` (see `05_status_directory.md`).
4. If `.status/` is not gitignored in this repo, add it - `git ls-files .status` should print nothing.

### Step 6 - when ready to cleanup

When the developer asks - after living without it for a week - the agent lists the files that will be deleted: the noise and non-markdown the migration moved into `scratch/`, each with its path, size, and why it is junk. It asks whether it is okay to delete them, and once the developer says yes, it deletes exactly those files itself. Obvious junk only.

______________________________________________________________________

## Bringing an already-migrated repo to the current layout

A repo migrated to an earlier version of the layout may have `archive/<year>/` folders with subdirectories, an `archive/other/<year>/`, undated plans and prompts, and its shipped-work record in `README.md`. Bringing it to the current layout is a one-session procedure. Show the owner an old -> new table before each batch of moves, and move nothing until it is approved.

1. Snapshot `.status/` first, as above.
2. Read `.status/README.md`, the `Status:` line of every plan, `git status`, and `git log -5`. Verify every "done" claim against the code or the merged PR before moving anything.
3. Write `.status/development_history.md` from the template: move the README's shipped-work sections into it verbatim, newest first, and add an entry for anything merged since.
4. Date every plan and prompt in `plans/` and `prompts/` that lacks a leading `YYYY-MM-DD_`: the day it was opened, from its `Opened:` line, else its last-modified time in the oldest snapshot of the directory, else its current last-modified time. Rename before any bulk edit (a line-ending conversion, for example), which would move that time. Then move finished plans to `archive/completed_plans/` and finished prompts to `archive/completed_prompts/`, names unchanged. Split a plan's still-open boxes into a new plan first, and add a `development_history.md` entry for each.
5. Already-archived plans and prompts (`archive/<year>/plans/`, `archive/<year>/prompts/`, or undated files in `archive/completed_plans/` and `archive/completed_prompts/`): date them the same way and move them to `completed_plans/` or `completed_prompts/`. Files already named `archived_YYYY-MM-DD_<name>` keep that name.
6. Notes: rename any note in `notes/` or in an archived year without a leading `YYYY-MM-DD_` (the date it records, from its title or first heading, else as in step 4). Notes from past years move to `archive/completed_notes/`, names otherwise unchanged.
7. Everything else in `archive/<year>/` or `archive/other/<year>/` ends up in `archive/<year>/`, flat: a file in a subdirectory takes the subdirectory path as a filename prefix (`archive/2026/documentation/cli_update.md` -> `archive/2026/documentation_cli_update.md`). Non-markdown goes to `scratch/`, flattened the same way, never to the archive. Remove the emptied subdirectories and `archive/other/`.
8. Rewrite `.status/README.md` in the template's shape, `## Next` last.
9. Bring all three rule carriers to the template wording: the "Where the thinking lives" block in `AGENTS.md`, `.claude/rules/status_conduct.md`, and `.github/instructions/status_conduct.instructions.md`.

______________________________________________________________________

## The classification rules, in order

First match wins. This is the whole of the script's judgment, stated so you can argue with it rather than reverse-engineer it.

| #   | Test                                                                                                                               | Action                                                                                              |
| --- | ---------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| 1   | inside a junk-drawer directory (`temp`, `working*`, `original*`, `old*`, `leftovers`, `unused`, `removed`, `merged`, `chat*`, ...) | markdown -> `archive/<year>/`, non-markdown -> `scratch/`; flattened, unopened                      |
| 2   | `.log` `.bak` `.backup` `.tmp` `.orig` `.swp` `.pyc`, or `" copy"` in the name - except under `scratch/`                           | -> `scratch/`, flattened                                                                            |
| 3   | root `README.md`, `decisions.md`, `development_history.md`, `local-environment.md`, `config.md`                                    | keep                                                                                                |
| 4   | already under `plans/`, `prompts/`, `notes/`, `archive/`, `scratch/`                                                               | keep - except an undated file directly in `plans/`, `prompts/`, or `notes/`: **rename**, date first |
| 5   | not markdown                                                                                                                       | **review** - human routes it; default `scratch/`                                                    |
| 6   | name says "decision"                                                                                                               | **harvest** - checked before staleness, on purpose                                                  |
| 7   | name contains `complete`/`final`/`summary`/`report`/`progress`/`assessment`/`deprecated`                                           | -> `archive/<year>/`, flattened                                                                     |
| 8   | markdown untouched longer than `stale_days` (default 90, set in `.status/config.md`)                                               | -> `archive/<year>/`, flattened                                                                     |
| 9   | name says "plan"/"design"/"roadmap"                                                                                                | -> `plans/YYYY-MM-DD_<slug>.md`, date moved to the front (else mtime)                               |
| 10  | name carries a date                                                                                                                | -> `notes/YYYY-MM-DD_<slug>.md`, date moved to the front                                            |
| 11  | anything left (recent, undated, unlabelled)                                                                                        | -> `plans/YYYY-MM-DD_<slug>.md` (mtime), flagged CONFIRM                                            |

Two of those orderings were bugs hit while testing on real directories, and they are worth knowing because they are the same mistake in two places:

- **Rule 9 must precede rule 10.** Otherwise `plan_<date>_<slug>.md` matches "has a date" and lands in `notes/` as a session record. The first version did exactly that to one repo's only real plan.
- **Rule 6 must precede rule 8.** Otherwise a five-month-old `decision_<date>_*.md` is archived unread as "stale", and the rationale it holds - the whole reason you write decision records - is lost. Fixing the order took one directory from 1 harvest to 8.

The day threshold comes from the repo's `.status/config.md` (`stale_days`, default 90 - see `05_status_directory.md`). Adjust `VAGUE_DIR_RE` and `DONE_NAME_RE` at the top of the script if your repos disagree. `VAGUE_DIR_RE` is deliberately aggressive - it treats `scripts`, `config`, `data`, and `documentation` as junk drawers when they appear *inside* `.status/`, because there that is what they usually are.

______________________________________________________________________

## Doing it with Claude instead

The script exists so this does not need a conversation, but the judgment reads in step 2 are also a reasonable thing to hand over (step 4's prompt is already in step 4). A prompt that works:

```
Read 06_status_migration.md in <path to claude-advice>.

Run the triage script on this repo in dry-run mode. Then, for every row with
action=review or action=plan, read the file and tell me the correct destination
in a table: source, proposed, your recommendation, one-line justification.

Do not move anything. Do not read anything with action=archive.
```

The "do not read anything with action=archive" line matters - without it the context window goes to stray build logs.

______________________________________________________________________

## Checklist per repo

- [ ] Snapshot `.status/` to a zip or tarball outside the repo
- [ ] Dry run; read the summary and sanity-check the counts
- [ ] Correct every `review` row and confirm every `plan` row
- [ ] `--apply`; verify the top level has exactly the nine expected entries (ten with the optional `config.md`)
- [ ] Have the agent draft `decisions.md` entries for what still governs; skim, accept, archive the rest
- [ ] Write `README.md` with its `Next` list, and `development_history.md`
- [ ] No `Read(.status/archive/**)` deny in `.claude/settings.json`; recursive `rm` is `ask`, not `deny`
- [ ] Add the "Where the thinking lives" block to `AGENTS.md`
- [ ] Confirm `.status/` is gitignored
- [ ] A week later, when the developer asks: the agent lists the junk the migration put in `scratch/`, asks whether it is okay to delete it, and deletes it on a yes
