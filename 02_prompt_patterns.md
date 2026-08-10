# How to frame prompts

The chat box is the worst place to keep context, and most bad prompts are good intentions crammed into it. This document gives the anatomy of an overloaded prompt, a template, the two homes for prompts, and the habits that matter more than either.

______________________________________________________________________

## The anatomy of an overloaded prompt

A typical kickoff prompt mixes six different things at once:

| #   | What it is                                        | Where it belongs                                                                 |
| --- | ------------------------------------------------- | -------------------------------------------------------------------------------- |
| 1   | An access request ("add these folders...")        | A launch flag or settings file - **not a prompt**                                |
| 2   | An unscoped read ("read the stuff in `<folder>`") | Fine in a prompt once scoped - "the stuff in" a folder could be 3 files or 3,000 |
| 3   | Project history and rationale                     | `.status/decisions.md`, written once                                             |
| 4   | Durable facts about a repository                  | That repo's `AGENTS.md`, written once                                            |
| 5   | The long-term goal, still fuzzy                   | A spec in `.status/plans/`, arrived at through an interview                      |
| 6   | Several sequenced asks                            | The actual ask - but it should be one deliverable per prompt                     |

**The core problem: most of such a prompt is durable background that gets retyped next session, and the next.** Rows 3 and 4 are facts that never change. Write them to a file once and they load automatically forever.

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

## Two kinds of prompt, two homes

- **`sample_prompts/` at the repo root, tracked**: illustrative, general, meant to be adapted - part of the repository's content. The paste-ready versions of the prompts this document discusses live there, one per file.
- **`.status/prompts/`, gitignored**: working prompts - the ones that hand a task to a fresh session, or restart one that has drifted. About one piece of work at one moment; local and disposable.

The test: **would someone else, in another repository, get value from this prompt?** If yes it is a sample. If it names your current task, it is a working prompt.

______________________________________________________________________

## From one overloaded prompt to three good ones

### Step 0 - settle access outside the prompt, once

```
# same in PowerShell and bash
cd <absolute path to the main repo>
claude --add-dir <absolute path to each sibling repo, repeated per repo>
```

Or put those paths in `.claude/settings.local.json` under `permissions.additionalDirectories` once and just type `claude`. Either way, directory access is settled and never appears in a prompt again. (Confirm the paths: a wrong drive letter fails silently and looks like Claude ignoring you.)

### Step 1 - write the background to disk (one prompt, once)

The prompt states each decision as a flat fact, sends the durable history to `.status/decisions.md`, and puts the repository map - locations by name, never by path - in `AGENTS.md`. The paste-ready version is `sample_prompts/write_background_to_disk.md`.

That is a 30-second prompt whose value compounds across every future session.

### Step 2 - interview, don't specify (because the goal is still fuzzy)

The tell is a prompt that admits "this is a complicated problem" or trails off mid-thought. That is exactly the signal to invert the direction of questioning: state the goal in one sentence, point at the existing work, and have the assistant interview you with the AskUserQuestion tool until a spec can be written to `.status/plans/`. The paste-ready version is `sample_prompts/interview_to_spec.md`.

Run it in **plan mode** (`Shift+Tab`). Then `/clear` and start a fresh session against the spec.

### Step 3 - the plan you actually wanted

Now, with background on disk and the goal sharper, the plan request gets short: all six slots filled, one named deliverable in `.status/plans/`, and one verification per phase so "done" is checkable. The paste-ready version is `sample_prompts/request_a_phased_plan.md`.

No longer than the overloaded original - but every line is either an instruction or a pointer, none of it is narrative you'll retype, and there is one named deliverable at a known path.

______________________________________________________________________

## Six habits worth more than any template

**1. Point at sources instead of describing them.**

| Instead of                                   | Write                                                                                                |
| -------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| "why does the citation loader behave oddly?" | "look through the git history of `citations/loader.py` and summarize how its API came to be"         |
| "the metadata is inconsistent"               | "compare the `task` field across the first 20 dataset JSONs and report the distinct shapes you find" |
| "the stuff in `<folder>`"                    | "list `<folder>`, then read only the files that define the record format"                            |

**2. `@` pulls a file in immediately.** `@.status/decisions.md` inlines the content rather than hoping Claude decides to read it. Type `@` for a path picker. A bonus: an `@` file reference also brings in the CLAUDE.md files from that file's directory and its parents.

**3. Reference an existing pattern.** Your strongest lever in a codebase you partly wrote: *"`src/<package>/validators/sidecar.py` is the pattern I like. Follow it for the new validator."* Vastly better than describing the pattern in words.

**4. Say what "done" looks like, in the same prompt.** From the docs:

> *"write a validateEmail function. example test cases: user@example.com is true, invalid is false, user@.com is false. run the tests after implementing"*

For metadata work that's usually a count or a schema check: *"after downloading, report how many dataset repos you got, how many failed and why, and confirm each has a dataset_description.json."*

**5. Vague prompts are a legitimate tool - just know when you're using one.** *"what would you improve about how this repo is organized?"* is a good prompt. It's exploration. What goes wrong is mixing exploration and specification in one message and expecting a specified result.

**6. Prompts for unattended runs need to be self-contained.** If you ever set up a scheduled task, it can't ask you anything. Be explicit about what success is and what to do with the results.

______________________________________________________________________

## The rhythm of a session

```
1. Land in the right directory. Check /context if unsure what loaded.
2. Shift+Tab -> plan mode.
3. Explore:  "read X and Y and tell me how Z works" - no edits happen.
4. Plan:     "write a plan to .status/plans/foo.md" - review it, Ctrl+G to edit.
5. /clear.
6. Execute:  "implement phase 1 of @.status/plans/foo.md. run <check> when done."
7. Verify:   "use a subagent to review the diff against the plan. Report gaps
             that affect correctness, not style."
8. Commit:   "commit with a descriptive message."
```

Step 5 is the one people skip. The plan is on disk; the exploration that produced it is dead weight. Clearing before execution gives the implementation a full context window.

Step 7 matters more than it looks: a reviewer in a fresh subagent context sees only the diff and your criteria, not the reasoning that produced the change, so it evaluates the result on its own terms. Tell it to flag correctness gaps only - a reviewer asked to find problems will always find some, and chasing all of them leads to over-engineering.

______________________________________________________________________

## Things that don't work the way you might expect

- **"Add to your trusted folders"** - not a prompt-level action. `--add-dir`, `/add-dir`, or `permissions.additionalDirectories`.
- **"Remember this for next time"** - Claude does keep auto-memory notes per repository (`/memory` to browse them), but for anything you rely on, write it to `AGENTS.md` or `.status/` yourself. Auto-memory is machine-local and Claude decides what's worth saving.
- **CLAUDE.md is not enforcement.** It's context delivered as a message. If a rule must hold every time, use a hook.
- **Instructions given only in conversation don't survive `/compact`.** The project-root CLAUDE.md is re-read from disk after compaction; a rule you typed in chat is not. Another argument for files over chat.
- **Nested CLAUDE.md files** in subdirectories load on demand when Claude reads a file there, and are *not* re-injected after `/compact`.
