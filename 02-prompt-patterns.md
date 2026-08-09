# How to frame prompts

You sent me a real prompt to look at. Let's use it, because what's wrong with it is instructive and fixable, and most of it isn't your fault - it's what happens when the only place to put context is the chat box.

______________________________________________________________________

## What your prompt was actually doing

Your prompt contained six different things at once:

| #   | What it was                                                                          | Where it belongs                                                                                                |
| --- | ------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------- |
| 1   | `add to your trusted folders h:\..., i:\..., ...`                                    | A launch flag or settings file - **not a prompt**                                                               |
| 2   | `Read the .status/TaskResearchStructure.md and the stuff in i:\NemarCitationWorking` | Fine in a prompt, but `i:\NemarCitationWorking` is unscoped - "the stuff in" a folder could be 3 files or 3,000 |
| 3   | The nemar-vs-openneuro history and rationale                                         | `.status/decisions.md`, written once                                                                            |
| 4   | Facts about what hed-task contains and its limitations                               | `hed-task/CLAUDE.md`, written once                                                                              |
| 5   | "My ultimate goal is to create models of tasks that can be applied to real data"     | A `SPEC.md`, arrived at through an interview                                                                    |
| 6   | Three sequenced plans: download nemar repos -> remove openneuro -> merge citations   | The actual ask - but it's three asks                                                                            |

Plus it ends mid-word: `"I don't know how to assig..."`. That's the tell. You were still thinking while typing, which is fine - but the model receives a half-formed thought as if it were a specification.

**The core problem: 80% of that prompt was durable background that you will retype next session, and next session, and next session.** Everything in rows 3 and 4 is a fact about your project that never changes. Write it to a file once and it loads automatically forever.

______________________________________________________________________

## The template

Six slots. Not every prompt needs all six - but for anything non-trivial, if a slot is empty, ask yourself whether you actually know the answer.

```
GOAL       One sentence. The durable objective, not today's step.
THIS TURN  What I want out of *this* message specifically.
WHERE      Exact paths. Use @ to pull a file in directly.
GIVEN      Decisions already made, as flat facts. No narrative.
CONSTRAINTS  Non-goals. What not to touch. What's out of scope.
DELIVERABLE  Exact output path and format. Plus: how we'll know it's right.
```

Two rules that do most of the work:

1. **One deliverable per prompt.** Three plans is three prompts, or one plan with three phases - decide which and say so.
2. **If you're explaining history, stop and write a file instead.** Then the prompt becomes `see .status/decisions.md` and you never type it again.

______________________________________________________________________

## Your prompt, rewritten

### Step 0 - outside the prompt, once

```powershell
cd H:\Research\task-research
claude --add-dir H:\Repos\hed-task --add-dir H:\Repos\hed-metadata-toolkit --add-dir I:\RepositoryMetadata\nemar-metadata --add-dir I:\NemarCitationWorking
```

Or put those four paths in `.claude/settings.json` under `permissions.additionalDirectories` once and just type `claude`. Either way, directory access is now settled and never appears in a prompt again.

*(Note: you wrote both `I:\Repos\hed-task` and `H:\Repos\hed-task` in the same prompt. Worth confirming which is real - a wrong drive letter is a silent failure that looks like Claude ignoring you.)*

### Step 1 - write the background to disk (one prompt, once)

```
GOAL: Stop re-explaining project history every session.

THIS TURN: Write two files. No other changes.

1. H:\Research\task-research\.status\decisions.md - record these decisions
   with dates and consequences:

   - All OpenNeuro datasets have been exported to nemar.org. Nemar has richer
     metadata and already gathers citations per dataset, each tied to an actual
     open dataset. Nemar does not produce PDFs.
   - Consequence: OpenNeuro integration is being retired, not maintained.
   - hed-task defines a curated set of "tasks" and "processes". The list is
     incomplete and is not currently linked to any data.
   - Long-term goal: models of tasks that apply to real data and integrate with
     events, so comparisons can be made across datasets.

2. H:\Research\task-research\CLAUDE.md - add a short "Repository map" section
   naming each of the five locations and what it owns, in one line each.

CONSTRAINTS: Facts and consequences only, no plans, no recommendations. Do not
touch anything under .status/ other than creating decisions.md.
```

That is a 30-second prompt whose value compounds across every future session.

### Step 2 - interview, don't specify (because the goal is still fuzzy)

Your prompt admitted *"I realize this is a complicated problem"* and trailed off at *"I don't know how to assig..."*. That's exactly the signal to invert the direction of questioning:

```
I want to build models of experimental tasks that can be applied to real
datasets and integrate with event files, so that task-level comparisons can be
made across datasets.

Read .status/decisions.md and H:\Repos\hed-task first.

Then interview me in detail using the AskUserQuestion tool. Ask about the data
model, what "task" and "process" have to mean formally, how a task model binds
to an events.tsv, edge cases, and the tradeoffs I haven't considered. Don't ask
obvious questions - dig into the hard parts.

Keep interviewing until we've covered everything, then write a complete spec to
.status/task-model-SPEC.md.
```

Run this in **plan mode** (`Shift+Tab`). Then `/clear` and start a fresh session against the spec.

### Step 3 - the plan you actually asked for

Now, with background on disk and the goal sharper, the plan request gets short:

```
GOAL: Retire the OpenNeuro path and re-found the pipeline on nemar.

THIS TURN: One plan document. No code, no file changes outside .status/.

WHERE:
  @.status/decisions.md
  @.status/TaskResearchStructure.md
  I:\NemarCitationWorking  (survey it - tell me what's there before relying on it)

GIVEN: Nemar is now the single source for datasets and citations. hed-task's
curated task/process list is the seed vocabulary, incomplete and unlinked to data.

DELIVERABLE: .status/nemar-migration-plan.md with exactly three phases:
  Phase 1 - mirror individual nemar dataset repositories locally
  Phase 2 - remove the OpenNeuro integration (list every file and call site
            that would need to change; do not change them)
  Phase 3 - merge nemar citations into the existing task-research citation store

For each phase: concrete steps, files touched, open questions, and one
verification I can run to confirm the phase is done. Mark every step
`[ ] TODO`.

CONSTRAINTS: Don't design the task model here - that's task-model-SPEC.md.
Where you're guessing about nemar's API or metadata shape, say so explicitly
rather than assuming.
```

Length: about the same as your original. Difference: every line is either an instruction or a pointer, none of it is narrative you'll retype, and there's one named deliverable at a known path.

______________________________________________________________________

## Six habits worth more than any template

**1. Point at sources instead of describing them.**

| Instead of                                   | Write                                                                                                                  |
| -------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| "why does the citation loader behave oddly?" | "look through the git history of `citations/loader.py` and summarize how its API came to be"                           |
| "the metadata is inconsistent"               | "compare the `task` field across the first 20 dataset JSONs in nemar-metadata and report the distinct shapes you find" |
| "the stuff in I:\\NemarCitationWorking"      | "list `I:\NemarCitationWorking`, then read only the files that define the citation record format"                      |

**2. `@` pulls a file in immediately.** `@.status/decisions.md` inlines the content rather than hoping Claude decides to read it. Type `@` for a path picker. A bonus: an `@` file reference also brings in the CLAUDE.md files from that file's directory and its parents.

**3. Reference an existing pattern.** Your strongest lever in a codebase you partly wrote: *"`hed_metadata_toolkit/validators/sidecar.py` is the pattern I like. Follow it for the nemar dataset validator."* Vastly better than describing the pattern in words.

**4. Say what "done" looks like, in the same prompt.** From the docs:

> *"write a validateEmail function. example test cases: user@example.com is true, invalid is false, user@.com is false. run the tests after implementing"*

For your work that's usually a count or a schema check: *"after downloading, report how many dataset repos you got, how many failed and why, and confirm each has a dataset_description.json."*

**5. Vague prompts are a legitimate tool - just know when you're using one.** *"what would you improve about how task-research is organized?"* is a good prompt. It's exploration. What goes wrong is mixing exploration and specification in one message and expecting a specified result.

**6. Prompts for unattended runs need to be self-contained.** If you ever set up a scheduled task, it can't ask you anything. Be explicit about what success is and what to do with the results.

______________________________________________________________________

## The rhythm of a session

```
1. Land in the right directory. Check /context if unsure what loaded.
2. Shift+Tab -> plan mode.
3. Explore:  "read X and Y and tell me how Z works" - no edits happen.
4. Plan:     "write a plan to .status/foo-plan.md" - review it, Ctrl+G to edit.
5. /clear.
6. Execute:  "implement phase 1 of @.status/foo-plan.md. run <check> when done."
7. Verify:   "use a subagent to review the diff against the plan. Report gaps
             that affect correctness, not style."
8. Commit:   "commit with a descriptive message."
```

Step 5 is the one people skip. The plan is on disk; the exploration that produced it is dead weight. Clearing before execution gives the implementation a full context window.

Step 7 matters more than it looks: a reviewer in a fresh subagent context sees only the diff and your criteria, not the reasoning that produced the change, so it evaluates the result on its own terms. Tell it to flag correctness gaps only - a reviewer asked to find problems will always find some, and chasing all of them leads to over-engineering.

______________________________________________________________________

## Things that don't work the way you might expect

- **"Add to your trusted folders"** - not a prompt-level action. `--add-dir`, `/add-dir`, or `permissions.additionalDirectories`.
- **"Remember this for next time"** - Claude does keep auto-memory notes per repository (`/memory` to browse them), but for anything you rely on, write it to CLAUDE.md or `.status/` yourself. Auto-memory is machine-local and Claude decides what's worth saving.
- **CLAUDE.md is not enforcement.** It's context delivered as a message. If a rule must hold every time, use a hook.
- **Instructions given only in conversation don't survive `/compact`.** The project-root CLAUDE.md is re-read from disk after compaction; a rule you typed in chat is not. Another argument for files over chat.
- **Nested CLAUDE.md files** in subdirectories load on demand when Claude reads a file there, and are *not* re-injected after `/compact`.
