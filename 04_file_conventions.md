# File naming and placement

## 1. CLAUDE.md or Claude.md?

**`CLAUDE.md` - all caps.** Every mention in the official documentation uses that exact spelling, and it's the only form you should write.

The lowercase variant is a trap on Windows specifically. NTFS is case-insensitive, so `Claude.md` may well work on your machine and give you no reason to suspect a problem. It then fails silently the moment the repo touches a case-sensitive filesystem - Linux CI, a cloud session, a collaborator on Linux. Nothing errors; the instructions just quietly stop loading.

Treat the all-caps form as the only safe answer and don't test the boundary. If you ever suspect a naming problem, `/context` is the check: if the file doesn't appear under **Memory files**, Claude cannot see it.

The same convention applies to the companions:

| Correct                                      | Not                                   |
| -------------------------------------------- | ------------------------------------- |
| `CLAUDE.md`                                  | `Claude.md`, `claude.md`, `CLAUDE.MD` |
| `CLAUDE.local.md`                            | `CLAUDE.LOCAL.md`, `Claude.local.md`  |
| `SKILL.md` (inside `.claude/skills/<name>/`) | `skill.md`, `Skill.md`                |
| `.claude/settings.json`                      | `.claude/Settings.json`               |

Two related naming facts worth knowing:

- A skill must be `<name>/SKILL.md` in its own folder. A bare `.claude/skills/name.md` does not register - it's a documented cause of "my skill doesn't appear in `/skills`". `templates/skill_example_SKILL.template.md` is a worked example.
- Project MCP config is `.mcp.json` at the **repo root**, not inside `.claude/`. Putting it under `.claude/` is another documented silent failure.

______________________________________________________________________

## 2. Committed versus local

Every configuration file is either **portable** (true on any machine, for any collaborator, on Linux CI) or **machine-specific**, and mixing the two is the highest-damage mistake available: an absolute path in a committed file works fine for you and quietly breaks for everyone and everywhere else. One test, from `01_repo_standards.md`, decides every line:

> **Would this line still be true on a colleague's laptop, or in a cloud session on Linux?** If no, it belongs in a `.local` file.

The split, using the official committed/gitignored designations:

| File                                             | Status          | What goes in it                                                                                                                            |
| ------------------------------------------------ | --------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| `AGENTS.md`                                      | committed       | The single instruction source: commands, layout, conventions, gotchas, agreements. Relative paths only. Sibling repos named, never pathed. |
| `CLAUDE.md`                                      | committed       | The `@AGENTS.md` import plus Claude-Code-specific notes, nothing else                                                                      |
| `.github/copilot-instructions.md`                | committed       | A pointer to `AGENTS.md`, duplicating nothing                                                                                              |
| `CLAUDE.local.md`                                | **gitignored**  | This machine's Claude Code notes; machine facts themselves go in `.status/local-environment.md`, which every tool can read                 |
| `.claude/settings.json`                          | committed       | Deny rules with relative paths, hooks calling repo-relative scripts, `worktree.sparsePaths`                                                |
| `.claude/settings.local.json`                    | **gitignored**  | `additionalDirectories`, `claudeMdExcludes`, personal permissions, anything absolute                                                       |
| `.claude/rules/*.md`                             | committed       | Path-scoped project conventions                                                                                                            |
| `.claude/skills/*/SKILL.md`                      | committed       | Shared procedures                                                                                                                          |
| `.claude/agents/*.md`                            | committed       | Custom subagents                                                                                                                           |
| `.mcp.json`                                      | committed       | Project MCP servers. **No secrets** - per-server `env` for those, and keep tokens out of the repo.                                         |
| `.worktreeinclude`                               | committed       | Lists gitignored files to copy into new worktrees                                                                                          |
| `.vscode/settings.json`                          | committed       | Portable editor settings only; the testing keys must match the repo's declared test framework                                              |
| `.env.example`                                   | committed       | Documents every variable `.env` needs                                                                                                      |
| `.env`                                           | **gitignored**  | Real tokens and machine values                                                                                                             |
| `.gitattributes`                                 | committed       | Line-ending normalization (`* text=auto eol=lf`)                                                                                           |
| `.status/`                                       | **gitignored**  | Plans, notes, decisions, working prompts - layout in `05_status_directory.md`                                                              |
| `~/.claude/CLAUDE.md`, `~/.claude/settings.json` | never in a repo | Your preferences across all projects                                                                                                       |

Three gotchas that make this easy to get wrong:

1. **`.claude/settings.local.json` is auto-gitignored only when Claude Code saves a setting to it.** Hand-create it and you must gitignore it yourself.
2. **`CLAUDE.local.md` is missing inside new git worktrees**, because it's gitignored and worktrees are fresh checkouts. Two fixes: list it in `.worktreeinclude` at the repo root, or keep the content in a home-directory file and import it with `@~/.claude/<repo>-local.md`. (A project-level import resolving outside the working directory prompts for approval once.)
3. **`~/.claude.json` is not `~/.claude/settings.json`.** The first is app state and UI preferences; `permissions`, `hooks`, and `env` set there are ignored. Two different files, one letter apart.

`templates/gitignore-snippet.txt` has the lines to add plus a one-line grep that catches any drive letter that sneaks into a committed file.

### Two more rules for anything committed

The portability test covers where a line is *true*; these cover what a committed file may *say*. Both follow from the same reader - a stranger on GitHub:

- **No project history.** No dates, no "this was changed", no "previously", no phase, session, or PR labels. A committed file states what is true now; how it got that way goes in `.status/decisions.md`.
- **No references to `.status/`.** It is gitignored, so the pointer is a dead link for every reader but its author - except in the handful of files whose job is to orient a tool. `01_repo_standards.md` states both rules with the full exception list.

______________________________________________________________________

## 3. The `.claude/` directory: what lives where

`.claude/` is Claude Code's configuration directory - the tool-specific folder, exactly analogous to `.vscode/` or `.github/`. This section is the reference inventory: every file Claude Code reads, at the two levels that layer together, plus the commands that show what actually loaded. Use it to answer "where does this setting/instruction/skill live?"

- **`<repo>/.claude/`** - configuration for this project, mostly committed
- **`~/.claude/`** (on Windows, `%USERPROFILE%\.claude\`) - your configuration for every project, never committed. Per-machine: each machine you work from has its own.

The official inventory, project level:

```
your-repo/
|-- AGENTS.md                     committed   the shared instructions, imported by CLAUDE.md
|-- CLAUDE.md                     committed   the @AGENTS.md import, read every session
|-- .mcp.json                     committed   project-scoped MCP servers
|-- .worktreeinclude              committed   gitignored files to copy into worktrees
`-- .claude/
    |-- settings.json             committed   permissions, hooks, config
    |-- settings.local.json       gitignored  your overrides for this project
    |-- CLAUDE.md                 committed   alternative home for the above
    |-- rules/                    committed   topic instructions, optionally path-gated
    |   |-- testing.md
    |   `-- api-design.md
    |-- skills/                   committed   named procedures, invoked as /name
    |   `-- security-review/
    |       |-- SKILL.md                      entrypoint
    |       `-- checklist.md                  supporting file
    |-- agents/                   committed   custom subagents: each .md defines a named
    |   `-- code-reviewer.md                  helper that works in its own context window
    |-- workflows/                committed   scripts that orchestrate many subagents
    |                                         deterministically; advanced, rarely needed
    `-- agent-memory/                         notes subagents write for themselves,
                                              machine-local, written by Claude not you
```

And the user level:

```
~/                                (on Windows: %USERPROFILE%\)
|-- .claude.json                  app state and UI preferences (NOT settings)
`-- .claude/
    |-- CLAUDE.md                 your preferences across every project
    |-- settings.json             your defaults across every project
    |-- keybindings.json          custom keyboard shortcuts
    |-- rules/                    user-level rules, apply everywhere
    |-- skills/                   personal skills, available everywhere
    |-- agents/                   personal subagents
    |-- workflows/                personal workflows
    |-- output-styles/            system-prompt sections that adjust how Claude works
    |-- themes/                   custom color themes
    `-- projects/                 auto memory Claude writes and maintains itself
```

Most repos need only a fraction of this: `AGENTS.md`, `CLAUDE.md`, and `.claude/settings.json` cover everyday work. Add the rest when a concrete need appears - a rule that only matters for certain files goes in `.claude/rules/`, a procedure you keep retyping becomes a skill, a check that must always run becomes a hook. Section 6 is the decision table.

Diagnostics, since knowing these makes the whole directory less mysterious:

| Command              | Shows                                                                                    |
| -------------------- | ---------------------------------------------------------------------------------------- |
| `/context`           | Everything occupying the context window, including which memory files loaded             |
| `/memory`            | Memory file locations across scopes, opens them in your editor                           |
| `/skills`            | Available skills and their source                                                        |
| `/permissions`       | Resolved allow and deny rules actually in effect                                         |
| `/hooks`             | Registered hooks by event                                                                |
| `/status`            | Which settings sources are active                                                        |
| `/doctor`            | Setup checkup: invalid settings, duplicate installs, CLAUDE.md content it can trim       |
| `claude --safe-mode` | A session with all customization disabled - the fastest way to prove config is the cause |

______________________________________________________________________

## 4. `.rules` and `.context` - are those standard?

**Not as top-level files, no.** Neither `.rules` nor `.context` is a broadly adopted convention. What usually gets mistaken for one is a *rules subdirectory inside a tool's own folder* - a real and common pattern, but tool-scoped rather than universal. The actual landscape, as of August 2026:

### The one genuine cross-tool standard: AGENTS.md

`AGENTS.md` at the repo root is the closest thing to a real convention. It's an open format - "a README for agents" - now stewarded by the Agentic AI Foundation under the Linux Foundation, used by 60,000+ open-source projects, and read by OpenAI Codex, Google Jules, Cursor, Aider, GitHub Copilot, VS Code, Devin, JetBrains Junie, Factory, Warp, and Zed. Placement rules mirror CLAUDE.md's: root file, nested files in subpackages, closest one to the edited file wins.

**Claude Code reads `CLAUDE.md`, not `AGENTS.md`.** The documented way to support both without duplicating content is to import one from the other:

```markdown
<!-- CLAUDE.md -->
@AGENTS.md

## Claude Code

Use plan mode for changes under `src/citations/`.
```

A symlink works too, but on Windows creating one needs Administrator or Developer Mode, so use the `@AGENTS.md` import.

### Tool-specific files you'll encounter

| Tool           | File(s)                                             |
| -------------- | --------------------------------------------------- |
| Claude Code    | `CLAUDE.md`, `.claude/rules/`                       |
| Cursor         | `.cursor/rules/` (current), `.cursorrules` (legacy) |
| GitHub Copilot | `.github/copilot-instructions.md`                   |
| Windsurf       | `.windsurf/rules/` or `.windsurfrules`              |
| Cline          | `.clinerules`                                       |
| Devin          | `.devin/rules/`                                     |
| Cross-tool     | `AGENTS.md`                                         |

Note the pattern: `.cursor/rules/`, `.windsurf/rules/`, `.devin/rules/`, `.claude/rules/`. **A `rules/` directory inside a dotted tool folder is the convention; a bare top-level `.rules` is not.** A literal `.rules` or `.context` in someone's repo is either one of the above with the parent folder collapsed in a listing, or a project-local invention - worth opening to see, not worth copying as a standard.

### Useful consequence: `/init` reads the competition

When you run `/init`, Claude Code reads Cursor rules (`.cursor/rules/` or `.cursorrules`) and Copilot rules (`.github/copilot-instructions.md`) and folds the relevant parts into the `CLAUDE.md` it generates. With `CLAUDE_CODE_NEW_INIT=1` set it also reads `AGENTS.md`, `.devin/rules/`, `.windsurf/rules/` or `.windsurfrules`, and `.clinerules`.

So a repo that already carries Copilot instructions gets them picked up rather than retyped - worth checking for a `.github/copilot-instructions.md` before running `/init`.

### What to do with all this

`AGENTS.md` is the single instruction source in every repo, with `CLAUDE.md` reduced to the `@AGENTS.md` import and `.github/copilot-instructions.md` a pointer - `01_repo_standards.md` has the wiring and the sources. Don't invent a `.context` or `.rules` folder: `.claude/rules/` already does that job for Claude Code, and `.status/` already does the job of holding project reasoning.

______________________________________________________________________

## 5. Making the committed half work on both Windows and Linux

"No drive letters" is the obvious rule and it is not sufficient. A committed `AGENTS.md` or `.claude/settings.json` gets read on a Windows box, on a colleague's Mac, and on Ubuntu in CI, and there are six other ways for it to be quietly Windows-only. All of them are real:

| Trap                                     | Why it breaks                                                                          | What to commit instead                                                                                                                                                                                            |
| ---------------------------------------- | -------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Bash(source .venv/Scripts/activate)`    | `Scripts/` is the Windows venv layout; POSIX is `bin/`                                 | Both forms. And know that **each Bash tool call is a fresh shell**, so activation never carries to the next call anyway - the real fix is to say "invoke the interpreter directly" in `AGENTS.md`                 |
| `python` in a documented command         | On many Linux and macOS setups only `python3` exists                                   | Name `python` in `AGENTS.md` but say "an interpreter with the package installed"; the exact interpreter goes in `.status/local-environment.md`. Allow both `Bash(python --version)` and `Bash(python3 --version)` |
| A hook that runs `bash scripts/check.sh` | On native Windows the Bash tool needs Git Bash, and a hook is not guaranteed to get it | Write hooks as `python scripts/check.py`. Python is the one interpreter every contributor to a Python repo already has                                                                                            |
| `Read(.\\vendor\\**)` with backslashes   | Permission patterns are globs; `\` is an escape character, not a separator             | Forward slashes always - `Read(./vendor/**)`. They work on Windows too                                                                                                                                            |
| `Claude.md`, `claude.md`                 | NTFS is case-insensitive so it works for you and silently stops loading on Linux       | `CLAUDE.md`, and never two files differing only in case anywhere in the repo                                                                                                                                      |
| CRLF in a committed file                 | A Windows editor writes CRLF; Linux tools and diffs then see the whole file as changed | `.gitattributes` with `* text=auto eol=lf` in every repo, plus `newline=""` on every text-mode write in Python. The `.gitattributes` is the backstop, not the fix                                                 |
| Expecting the sandbox to enforce a rule  | Claude Code's OS-level sandbox is **not supported on native Windows** - WSL 2 only     | On Windows, enforcement means a `PreToolUse` hook. Treat the `deny` list as stated intent, not a wall                                                                                                             |

The test to apply to every line of a committed config file is still the one from section 2 - *would this be true on a colleague's laptop, or on Linux CI?* - but run it against **shell layout, interpreter names, path separators, filename case, and line endings**, not just against drive letters.

The full split - which files carry the portable half and which carry the machine half - is specified in `01_repo_standards.md`: `AGENTS.md`, `.claude/settings.json`, and `.vscode/settings.json` carry the portable half; `.status/local-environment.md` and `.claude/settings.local.json` carry the interpreter path, checkout locations, cache root, and that machine's quirks.

______________________________________________________________________

## 6. Where does a new rule go?

The question that comes up every time you notice Claude doing something you did not want. Two axes decide it: **how many projects does this apply to**, and **does it need to hold every time or just usually**.

| The rule is...                                                               | Put it in                                                  | Loads                                  |
| ---------------------------------------------------------------------------- | ---------------------------------------------------------- | -------------------------------------- |
| True of every project you work on ("ASCII only", "never touch `.status/`")   | `~/.claude/CLAUDE.md`, on every machine                    | every session, every project           |
| True of one repo, and a collaborator or CI needs it too                      | that repo's `AGENTS.md`, committed                         | every session in that repo             |
| True of one repo, only on this machine (paths, interpreter, "the slow disk") | that repo's `CLAUDE.local.md`, gitignored                  | every session in that repo, yours only |
| Only relevant when touching certain files (event files, sidecar JSON)        | `.claude/rules/<topic>.md` with a `paths:` glob, committed | only when Claude opens a matching file |
| A multi-step procedure you keep retyping                                     | `.claude/skills/<name>/SKILL.md`, committed                | only when invoked                      |
| Something that must hold every time, no exceptions                           | a hook in `.claude/settings.json`                          | enforced, not requested                |
| A convention about how these advice documents themselves are written         | this folder's `CLAUDE.md`                                  | any session started in this folder     |

Three practical notes:

- **Prefer the narrowest scope that covers the rule.** A user-level `CLAUDE.md` is paid for in context on every request in every project, so it earns its place only if it is genuinely universal. Fifteen lines is a good target; if it grows past thirty, something in it belongs in a repo instead.
- **Duplicate deliberately, once.** A universal style rule already in your user-level file is worth repeating in a *public* repo's committed `AGENTS.md`, because a collaborator does not have your user-level file. That is the only good reason to state the same rule twice.
- **`AGENTS.md` is context, not enforcement.** Claude reads it and tries to comply; there is no guarantee. If a rule matters enough that a violation is a real problem, write the check as a hook or as a test - the ASCII rule, for instance, is one `python -c` away from being a CI check rather than a request.

### The ASCII rule, as a worked example

A universal style rule - "ASCII only in prose, code, comments, and filenames" - belongs in three places, and the reasoning for each is the general case:

1. `~/.claude/CLAUDE.md` on each machine - it applies to every project, so this is its real home.
2. `templates/AGENTS.template.md` - so every repo set up from the template inherits it, and public repos state it for collaborators who do not have your user-level file.
3. The instruction file of any folder where drift is likely - a folder with no instruction file at all is precisely where violations accumulate uncaught.

And any blanket character rule needs **an exception clause**: a citation library legitimately contains accented surnames and non-Latin titles as test fixtures, because folding them is what the code under test does. A rule with no data exception would have someone "fix" the fixtures and break the tests. Write the carve-out into the rule rather than leaving it to judgment.
