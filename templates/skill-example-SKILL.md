<!--
  Copy to: <repo>/.claude/skills/status-update/SKILL.md
  Invoke with: /status-update            (or /status-update nemar-migration)

  The directory name becomes the command name. `disable-model-invocation: true`
  means only you can trigger it, and it costs ZERO context until you do.

  This is a real, useful example - not a placeholder. Adapt the paths.
-->
---
name: status-update
description: Reconcile a .status plan document against what is actually on disk and update its checkboxes. Use when asked to refresh, reconcile, or check the status of a plan.
argument-hint: "[plan-name]"
disable-model-invocation: true
allowed-tools: Read, Grep, Glob, Bash(git log *), Bash(git status)
---

# Reconcile a plan with reality

Target plan: `$ARGUMENTS`
If no argument was given, list the files in `.status/` and ask me which one.

## Steps

1. Read the plan document at `.status/$ARGUMENTS-plan.md` (try `.status/$ARGUMENTS.md`
   if that doesn't exist).

2. Also read `.status/decisions.md`. If any decision recorded there contradicts
   or supersedes part of this plan, **say so before doing anything else** and stop
   for my confirmation.

3. For each step marked `[ ] TODO`, determine from the filesystem and git history
   whether it is actually done. Evidence only - a file existing with the right
   shape, a passing check, a commit that touched the named files. Do not infer
   "done" from the step sounding plausible.

4. Run each phase's stated `Verify with` command. Report the actual output.

5. Update the plan in place:
   - `[ ] TODO` -> `[x] DONE <YYYY-MM-DD>` only where you have evidence
   - `[ ] TODO` -> `[~] PARTIAL - <what is missing>` where it is half done
   - Leave untouched anything you could not verify, and list those separately
   - Append one line to the `## Log` section describing this reconciliation

6. Report back in this shape:
   - Newly done: <list>
   - Partial: <list, with what's missing>
   - Could not verify: <list, with why>
   - Contradictions with decisions.md: <list, or none>
   - Suggested next step: <one thing>

## Rules

- IMPORTANT: Do not add, remove, or reorder plan steps. Only update status
  markers and append to the Log. Structural changes to the plan need my approval.
- Do not modify any file outside the plan document.
- If the plan's `Status:` header should change (e.g. all phases done -> `DONE`),
  propose it; don't apply it.

<!--
  Other skills worth writing for this work, same pattern:

  /plan-doc <name>
    Create a new .status plan from the house template with the standard sections,
    pre-filled with what you can infer from the repo. disable-model-invocation: true.

  /decide "<summary>"
    Append a dated entry to .status/decisions.md in the house format: decision,
    rationale, consequence, what it supersedes. Refuses to rewrite existing entries.

  /dataset-audit <path>
    Whatever your repeated "check this dataset's metadata against X" procedure is.
    Give it a `paths:` frontmatter field so it auto-suggests when Claude touches
    dataset files.
-->
