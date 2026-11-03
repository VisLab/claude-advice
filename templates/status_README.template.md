<!--
  Copy to .status/README.md  (see 05_status_directory.md)

  This is the index. It exists so a session can orient from ONE read instead of
  globbing a directory. About a hundred lines at most. Keep the sections in this
  order; `## Next` is the LAST section and is an ordered list of concrete
  actions. No record of shipped work here: that goes in development_history.md.

  Not committed, because .status/ is gitignored. If you later decide to commit
  the durable parts, this file and decisions.md are the two to start with.
-->

# Status directory - <repo-name>

**For humans:** <what is happening in this repo right now, and what comes next. Two or three sentences. Rewrite it when the answer changes; delete it never.>

## What is where

Working notes for this repo. Gitignored: local to this machine, not on GitHub, and absent from fresh clones and `claude --worktree` worktrees.

- `decisions.md` - why things are the way they are. Append; never rewrite an entry.
- `development_history.md` - what has shipped, newest first. Append at the top.
- `plans/` - unfinished plans, one file each, `[ ]`/`[x]` markers.
- `prompts/` - working prompts for starting or restarting the work in `plans/`. Disposable.
- `notes/` - dated records, always `YYYY-MM-DD_slug.md`. Write-once.
- `archive/` - finished work, in four places: `completed_plans/`, `completed_prompts/`, `completed_notes/`, `other/<year>/`. **Do not read unless asked for a named file.**
- `scratch/` - the workbench: temporary scripts and experiments, any file type. **Throwaway files go here, never the repository root.** May be deleted unread.
- `local-environment.md` - this machine's paths, interpreter, and quirks.
- `config.md` - this repo's retention settings (optional; defaults apply).

The root holds only the files listed above. New material goes in `plans/`, `prompts/`, `notes/`, or `scratch/`.

## Current state (YYYY-MM-DD)

- <what works, what is released, which branch is live - facts a session needs before touching anything>

## Unfinished work

<!-- Grouped by what each item waits on. Delete a group that is empty. -->

### Waiting on a ruling

- `plans/<slug>.md` - <the question that needs an answer>

### Waiting on another repository

- `plans/<slug>.md` - <which repository, and what it must do first>

### Waiting on a release

- <item> - <which release>

### Not scheduled

- <item>

## Machine quirks

<!-- Optional. Only what bites a session on this machine; the full record is local-environment.md. -->

- <quirk>

## Next

1. <the next concrete action>
2. <the one after>
