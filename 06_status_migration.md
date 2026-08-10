# Migrating an existing `.status/` directory

`05_status_directory.md` describes the target layout and why. This document is the procedure for getting a directory that already has hundreds of files in it to that layout, and it is deliberately separate because the two get read at different times: the target once, the procedure once per repo.

The classification rules live in `templates/status-triage.py`, which **proposes** a plan and changes nothing unless you pass `--apply`.

______________________________________________________________________

## Before you start: the one thing that makes this different

`.status/` is gitignored in every one of these repos. There is **no `git checkout`, no `git stash`, and nothing on GitHub.** A wrong `Move-Item` is a permanent loss of the only copy.

Everything below follows from that:

- The script **never deletes**. Noise goes to `archive/<year>/_quarantine/`, and you delete that one directory by hand after living without it for a week.
- The script **never overwrites**. A destination collision becomes `name_2.md`.
- You snapshot first. Not optional.

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
    121  archive     finished or stale -> archive/
      4  review      non-markdown - YOUR CALL
      1  quarantine  noise -> archive/<year>/_quarantine/
```

Read those numbers as the answer to "is this worth doing": that repo goes from a 170-file listing to **7 plans and 29 notes in view**. The most extreme directory tested went from 457 files to 2 in view.

### Step 2 - read the plan and correct it

The plan is a TSV with `action`, `source`, `destination`, `kb`, `modified`, `reason`. Open it in Excel or VS Code. The columns you care about:

- **`action = review`** - the script refuses to guess where non-markdown belongs. These are yours to route. For each: does anything still run or import it? Then `scripts/` or `src/` or `tests/data/`, and commit it. Otherwise accept the `archive/` destination it proposed. A code-heavy directory can have dozens of these; that is where most of the correction time goes.
- **`action = plan`** - candidate *active* work, and the script says CONFIRM for a reason. It only knows the file is recent and named like a plan. Read each one. Half will turn out to be finished; change their destination to `archive/<year>/`.
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
# expect: archive, notes, plans, prompts, README.md, decisions.md, local-environment.md, scratch
```

### Step 4 - harvest the decisions (the part that matters)

This is the only step a script cannot do, and it is the step that makes the whole exercise worth the afternoon. Read the files marked `harvest`, plus the plans that survived step 2, and pull each real decision into `decisions.md` as four lines:

```markdown
## 2026-04-28 - Stable cache keys for lookups, not date-bucketed

Date-bucketed keys meant a re-run on a new day re-fetched everything and the
"immutable cache" guarantee did nothing for lookups.

Consequence: lookup caches key on the identifier alone. Response caches stay
date-bucketed.
Superseded: notes/2026-04-28_stable_cache_for_lookups.md (kept; do not act on it).
```

Date, what was decided, why, what it supersedes. Every `harvest` row is a paragraph that currently exists only in a file you will never open again - and it is exactly the background that otherwise gets re-typed into prompts.

### Step 5 - write the index and wire it up

1. `.status/README.md` from `templates/status-README.md.template`, including the "Active right now" list. Three lines, and it is worth more than everything you just archived.
2. Add the deny rules to the repo's **committed** `.claude/settings.json` - the patterns are repo-relative, so they are portable and inert for anyone without a `.status/`:
   ```json
   "deny": ["Read(.status/archive/**)", "Read(.status/scratch/**)"]
   ```
3. Add the "Where the thinking lives" block to `AGENTS.md` (see `05_status_directory.md`).
4. If `.status/` is not gitignored in this repo, add it - `git ls-files .status` should print nothing.

### Step 6 - a week later

Delete `archive/<year>/_quarantine/`. If you have not missed it in a week, it was noise, which is what the classification said.

______________________________________________________________________

## The classification rules, in order

First match wins. This is the whole of the script's judgment, stated so you can argue with it rather than reverse-engineer it.

| #   | Test                                                                                                                               | Action                                                   |
| --- | ---------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------- |
| 1   | inside a junk-drawer directory (`temp`, `working*`, `original*`, `old*`, `leftovers`, `unused`, `removed`, `merged`, `chat*`, ...) | whole tree -> `archive/<year>/`, unopened                |
| 2   | `.log` `.bak` `.backup` `.tmp` `.orig` `.swp` `.pyc`, or `" copy"` in the name                                                     | -> `archive/<year>/_quarantine/`                         |
| 3   | root `README.md`, `decisions.md`, `local-environment.md`                                                                           | keep                                                     |
| 4   | already under `plans/`, `prompts/`, `notes/`, `archive/`, `scratch/`                                                               | keep                                                     |
| 5   | not markdown                                                                                                                       | **review** - human routes it                             |
| 6   | name says "decision"                                                                                                               | **harvest** - checked before staleness, on purpose       |
| 7   | name contains `complete`/`final`/`summary`/`report`/`progress`/`assessment`/`deprecated`                                           | -> `archive/`                                            |
| 8   | markdown untouched for more than 90 days                                                                                           | -> `archive/`                                            |
| 9   | name says "plan"/"design"/"roadmap"                                                                                                | -> `plans/<slug>.md`, date stripped                      |
| 10  | name carries a date                                                                                                                | -> `notes/YYYY-MM-DD_<slug>.md`, date moved to the front |
| 11  | anything left (recent, undated, unlabelled)                                                                                        | -> `plans/<slug>.md`, flagged CONFIRM                    |

Two of those orderings were bugs hit while testing on real directories, and they are worth knowing because they are the same mistake in two places:

- **Rule 9 must precede rule 10.** Otherwise `plan_<date>_<slug>.md` matches "has a date" and lands in `notes/` as a session record. The first version did exactly that to one repo's only real plan.
- **Rule 6 must precede rule 8.** Otherwise a five-month-old `decision_<date>_*.md` is archived unread as "stale", and the rationale it holds - the whole reason you write decision records - is lost. Fixing the order took one directory from 1 harvest to 8.

Adjust `STALE_DAYS`, `VAGUE_DIR_RE`, and `DONE_NAME_RE` at the top of the script if your repos disagree. `VAGUE_DIR_RE` is deliberately aggressive - it treats `scripts`, `config`, `data`, and `documentation` as junk drawers when they appear *inside* `.status/`, because there that is what they usually are.

______________________________________________________________________

## Doing it with Claude instead

The script exists so this does not need a conversation, but the judgment steps (2 and 4) are a reasonable thing to hand over. A prompt that works:

```
Read 06_status_migration.md in <path to claude-advice>.

Run the triage script on this repo in dry-run mode. Then, for every row with
action=review or action=plan, read the file and tell me the correct destination
in a table: source, proposed, your recommendation, one-line justification.

Do not move anything. Do not read anything with action=archive.
```

Then, after applying:

```
Read the files under .status/notes/ that came from action=harvest rows and draft
decisions.md entries for them: date, what was decided, why, what it supersedes.
Four lines each, append-only order, oldest first. Show me the draft; do not write
the file yet.
```

The "do not read anything with action=archive" line matters - without it the context window goes to stray build logs.

______________________________________________________________________

## Checklist per repo

- [ ] Snapshot `.status/` to a zip or tarball outside the repo
- [ ] Dry run; read the summary and sanity-check the counts
- [ ] Correct every `review` row and confirm every `plan` row
- [ ] `--apply`; verify the top level has exactly the eight expected entries
- [ ] Harvest the `harvest` rows and the surviving plans into `decisions.md`
- [ ] Write `README.md` with the "Active right now" list
- [ ] Add the two `Read(.status/...)` deny rules to `.claude/settings.json`
- [ ] Add the "Where the thinking lives" block to `AGENTS.md`
- [ ] Confirm `.status/` is gitignored
- [ ] A week later: delete `archive/<year>/_quarantine/`
