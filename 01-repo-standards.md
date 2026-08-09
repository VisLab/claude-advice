# What belongs in every repository

Your question was: *"I don't know what a basic set of things that should be in each repository."* Here it is.

______________________________________________________________________

## The minimum, in priority order

```
your-repo/
|-- CLAUDE.md                     # 1. REQUIRED. Committed. Under 200 lines.
|-- CLAUDE.local.md               # 2. GITIGNORED. Your machine's specifics.
|-- .claude/
|   |-- settings.json             # 3. Committed. Portable settings only.
|   |-- settings.local.json       # 4. GITIGNORED. Absolute paths live here.
|   |-- rules/                    # 5. Committed. Path-scoped instructions.
|   |   `-- data-files.md
|   |-- skills/                   # 6. Committed. Repeatable procedures.
|   |   `-- status-update/SKILL.md
|   `-- agents/                   #    Committed. Custom subagents (optional).
|-- .status/                      # 7. Committed. Your convention - keep it.
|   |-- decisions.md              #    why things are the way they are
|   `-- <initiative>-plan.md      #    one file per piece of work
|-- .mcp.json                     #    Committed, if this repo needs MCP servers
`-- README.md                     # for humans, not for Claude
```

Items 1, 3, and 7 pay off immediately. Item 2 exists the moment you have a machine-specific fact. The rest are for when a specific trigger appears (see the trigger table at the end).

______________________________________________________________________

## The rule that governs all of it: committed vs local

Every file above is either **portable** (true on any machine, for any collaborator, on Linux CI) or **machine-specific**. Never mix them in one file.

**The test:** *would this line still be true on a colleague's laptop, or in a cloud session on Linux?* If no, it belongs in a `.local` file.

| Portable - COMMIT                                                 | Machine-specific - GITIGNORE                                                                      |
| ----------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| `CLAUDE.md` - commands, layout, conventions, gotchas, agreements  | `CLAUDE.local.md` - your drive letters, sibling repo paths, scratch dirs                          |
| `.claude/settings.json` - deny rules with *relative* paths, hooks | `.claude/settings.local.json` - `additionalDirectories`, `claudeMdExcludes`, personal permissions |
| `.claude/rules/`, `.claude/skills/`, `.claude/agents/`            | `%USERPROFILE%\.claude\CLAUDE.md` - preferences across all projects                               |
| `.status/` - decisions and plans are project history              | `%USERPROFILE%\.claude\settings.json` - your global defaults                                      |
| `.mcp.json` - server definitions (no secrets)                     | `.worktreeinclude` is committed, but lists gitignored files to copy                               |

Concretely: **an absolute path with a drive letter must never appear in a committed file.** `H:\Repos\hed-task` is meaningless to anyone else and breaks the moment anything runs on Linux. Same for `I:\NemarCitationWorking`. Put those in `.claude/settings.local.json` and refer to the repo by *name* in `CLAUDE.md`.

Two gotchas:

- **`.claude/settings.local.json` is auto-gitignored only when Claude Code saves a setting to it.** If you create it by hand, add it to `.gitignore` yourself.
- **`CLAUDE.local.md` does not exist in new git worktrees**, because it's gitignored. If you use `claude --worktree`, put personal instructions in a home-directory file and import it instead: `@~/.claude/my-hedtask-instructions.md`. (Project-level imports that resolve outside the working directory trigger a one-time approval dialog; accept it once.)

See `templates/gitignore-snippet.txt` for the lines to add.

______________________________________________________________________

## 1. CLAUDE.md - the only mandatory file

Loaded in full at the start of every session, so every line costs context in every request. Location: `./CLAUDE.md` or `./.claude/CLAUDE.md` - both work, pick one and be consistent. Commit it.

**Generate the first draft with `/init`, then cut it down.** The docs are blunt about this: *"Bloated CLAUDE.md files cause Claude to ignore your actual instructions!"*

| Include                                            | Exclude                                            |
| -------------------------------------------------- | -------------------------------------------------- |
| Bash/PowerShell commands Claude can't guess        | Anything Claude can figure out by reading the code |
| Code style rules that differ from defaults         | Standard language conventions                      |
| Testing instructions and preferred test runner     | Detailed API docs (link instead)                   |
| Repo etiquette - branch naming, PR conventions     | Information that changes frequently                |
| Architectural decisions specific to this project   | Long explanations or tutorials                     |
| Environment quirks - required env vars, data paths | File-by-file descriptions of the codebase          |
| Non-obvious gotchas                                | "Write clean code"                                 |

For each line, ask: **would removing this cause Claude to make a mistake?** If no, delete it.

Two things worth knowing:

- Emphasis works. "IMPORTANT" and "YOU MUST" measurably improve adherence.
- Block-level HTML comments (`<!-- note to self -->`) are stripped before the content reaches Claude's context, so you can leave notes for yourself for free.

See `templates/CLAUDE.md.template`.

### If a rule has to hold every single time

CLAUDE.md is *context*, not enforcement. Claude reads it and tries to follow it; there's no guarantee. If something must always happen - never touch `.status/`, always run a validator after edits - write a **hook** instead. Hooks are shell commands fired at lifecycle events and are deterministic. A `PreToolUse` hook can block an action outright.

You can ask Claude to write hooks for you: *"write a hook that blocks writes to the .status folder"*.

______________________________________________________________________

## 2. `.claude/settings.json` - shared project settings

Two things worth setting in almost every repo:

```json
{
  "permissions": {
    "deny": [
      "Read(./**/dist/**)",
      "Read(./**/build/**)",
      "Read(./**/*.generated.*)"
    ]
  }
}
```

Content searches already respect `.gitignore`, so `node_modules/`, `dist/`, and friends stay out of results for free. Deny rules are for things that *are* checked in - vendored SDKs, committed generated files, and (relevant to you) large committed data or citation dumps you never want Claude reading in bulk.

Deny rules cover Claude's file tools and recognized Bash file commands (`cat`, `head`, `grep`, `find`) when a denied path is an argument. They do not filter denied paths out of a recursive search's output.

Note the paths are **relative** (`./**/dist/**`). That's what makes this file safe to commit.

The second thing you'll want - reading a sibling repo - is machine-specific, so it goes in `.claude/settings.local.json`, **not** here:

```json
{
  "permissions": {
    "additionalDirectories": ["I:\\RepositoryMetadata\\nemar-metadata"]
  }
}
```

That path is true only on your machine. Committing it would hand a collaborator a broken config and would fail outright in any Linux session. The committed `CLAUDE.md` can still *mention* that this repo depends on `nemar-metadata` by name - just never by path.

**Critical gotcha:** `.claude/settings.json` loads **only from the directory you start Claude in**. It is *not* inherited from parent directories the way CLAUDE.md files are. If you sometimes launch from the repo root and sometimes from a subdirectory, each starting point needs its own self-contained settings file.

### Which settings file to use

| File                                  | Scope                 | Commit?         |
| ------------------------------------- | --------------------- | --------------- |
| `%USERPROFILE%\.claude\settings.json` | You, all projects     | n/a             |
| `.claude/settings.json`               | Everyone in this repo | Yes             |
| `.claude/settings.local.json`         | You, this repo only   | No - gitignored |

Precedence, highest first: managed policy -> command-line args -> local -> project -> user. **Permission rules merge across scopes** rather than overriding, which is unlike most settings.

Add `"$schema": "https://json.schemastore.org/claude-code-settings.json"` as the first key to get autocomplete and validation while editing in VS Code.

______________________________________________________________________

## 3. `.claude/rules/` - when CLAUDE.md gets crowded

Markdown files in `.claude/rules/`, one topic per file, discovered recursively. Without frontmatter they load every session at the same priority as `.claude/CLAUDE.md`. **With** a `paths:` glob they load only when Claude touches matching files:

```markdown
---
paths:
  - "**/*.tsv"
  - "**/sourcedata/**"
---

# Working with BIDS event files

- Never edit `events.tsv` in place; write a sibling `.corrected.tsv` first.
- Column order matters to downstream tools - preserve it.
```

This is a good fit for your work: instructions about event files, sidecar JSON, or citation formats that only matter when Claude is actually in those files.

Personal rules go in `%USERPROFILE%\.claude\rules\` and apply to every project; they load *before* project rules, so project rules win.

______________________________________________________________________

## 4. `.claude/skills/` - procedures, not facts

The rule of thumb: **facts and "always do X" -> CLAUDE.md. Multi-step procedures and reference material -> skills.** Skill bodies load only when used.

```
.claude/skills/
  status-update/
    SKILL.md          # invoke as /status-update
```

Frontmatter fields you'll actually use:

| Field                            | Purpose                                                                                     |
| -------------------------------- | ------------------------------------------------------------------------------------------- |
| `name`                           | Display name. Defaults to the directory name.                                               |
| `description`                    | **How Claude decides whether to use it.** Lead with the trigger words.                      |
| `argument-hint`                  | Autocomplete hint, e.g. `[initiative-name]`                                                 |
| `disable-model-invocation: true` | Only *you* can invoke it. Zero context cost until used. Use for anything with side effects. |
| `allowed-tools`                  | Pre-approve tools for the turn that invokes the skill                                       |
| `paths`                          | Globs; auto-load only when working with matching files                                      |
| `context: fork`                  | Run the skill in an isolated subagent context                                               |

Arguments: `$ARGUMENTS` is everything you typed after the skill name; `$0`, `$1` are positional. If your skill body has no `$ARGUMENTS`, Claude Code appends `ARGUMENTS: <your input>` at the end so nothing is lost.

Skills in nested `.claude/skills/` directories below your starting point **don't load at startup** - they appear the first time Claude reads a file in that subdirectory. Skills at or above your starting directory load immediately.

See `templates/skill-example-SKILL.md`.

______________________________________________________________________

## 5. `.status/` - keep doing this

> **Superseded in two respects by `05-status-directory.md`, written after surveying your 25 real `.status/` directories.** (1) The layout below is too flat: a single directory with dated files at the top level is what grew to 457 files in `hed-resources`. Use the `plans/` / `notes/` / `archive/` / `scratch/` split instead. (2) The "committed" designation in the table above is wrong for your setup - you gitignore `.status/` in all 25 repos, and for public repos that is the right call. The rest of this section still holds.

You invented a good convention. Two refinements:

**`.status/decisions.md`** - an append-only log of *why*. This is where the paragraph you wrote in your prompt belongs, permanently, in about six lines:

```markdown
## 2026-08 - Nemar replaces OpenNeuro as the citation/dataset source

All OpenNeuro datasets have been exported to nemar.org. Nemar has better
metadata and already gathers citations per dataset, each tied to an actual
open dataset. It does not produce PDFs.

Consequence: the OpenNeuro integration is being removed, not maintained.
Superseded: `.status/openneuro-citation-plan.md` (kept for history, do not act on).
```

Write it once, and every future session reads it in seconds instead of you retyping it.

**`.status/<initiative>-plan.md`** - one file per initiative, with an explicit status marker per step. Then `/status-update` can reconcile it against disk. See `templates/plan-doc.template.md`.

Point CLAUDE.md at both:

```markdown
## Where the thinking lives
- `.status/decisions.md` - decisions and their rationale. Read this before
  proposing structural changes. Append, never rewrite.
- `.status/*-plan.md` - active plans. Check status markers before starting work.
```

______________________________________________________________________

## The hub repo gets two extras

Designate one repo (I'd suggest `H:\Research\task-research`) as the hub. It gets everything above plus:

- **`REPOS.md`** - the map of all your repositories, by name and role. Reference it from the hub's CLAUDE.md with `@REPOS.md` so it loads automatically, or leave it un-imported and let Claude read it on demand. Keep the drive letters out of it if you commit it; see the note in the template.
- **`.claude/settings.local.json` with `additionalDirectories`** listing the sibling repos by absolute path, so you don't retype `--add-dir` every launch. This one is gitignored precisely because those paths are yours alone.

______________________________________________________________________

## Per-repo checklist

Copy this into each repo's first session:

- [ ] `claude` launched from the repo root, `/init` run
- [ ] CLAUDE.md pruned to under 200 lines; every remaining line earns its place
- [ ] `/context` confirms CLAUDE.md appears under **Memory files**
- [ ] `.claude/settings.json` with `Read` deny rules, **relative paths only**
- [ ] `.claude/settings.local.json` and `CLAUDE.local.md` in `.gitignore`
- [ ] **No drive letter appears anywhere in a committed file** - grep for `H:\` and `I:\` before you commit
- [ ] `.status/decisions.md` exists and has at least one real entry
- [ ] Build/test/validate commands in CLAUDE.md and verified to actually work
- [ ] One thing Claude can run that returns pass/fail
- [ ] CLAUDE.md and `.claude/settings.json` committed

______________________________________________________________________

## When to add each extra thing

Don't build all of this up front. Wait for the trigger:

| Trigger                                                      | Add                                             |
| ------------------------------------------------------------ | ----------------------------------------------- |
| Claude gets a convention or command wrong twice              | A line in CLAUDE.md                             |
| CLAUDE.md is past 200 lines                                  | Move sections to `.claude/rules/` with `paths:` |
| You keep typing the same prompt to start a task              | A user-invocable skill                          |
| You paste the same multi-step procedure a third time         | A skill                                         |
| A side task floods your conversation with output             | Route it through a subagent                     |
| You want something to happen every time, no exceptions       | A hook                                          |
| A second repo needs the same setup                           | Package it as a plugin                          |
| Claude keeps reading files to find where a symbol is defined | A code-intelligence plugin for that language    |

For Python work, `/plugin install python-lsp@claude-plugins-official` (add the marketplace first with `/plugin marketplace add anthropics/claude-plugins-official` if it isn't found). It gives Claude go-to-definition and find-references instead of grepping, which cuts file reads substantially in a large codebase.
