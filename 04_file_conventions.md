# File naming, the .claude directory, and what other tools use

Four questions answered, in order.

______________________________________________________________________

## 1. CLAUDE.md or Claude.md?

**`CLAUDE.md` - all caps.** Every mention in the official documentation uses that exact spelling, and it's the only form you should write.

The lowercase variant is a trap on Windows specifically. NTFS is case-insensitive, so `Claude.md` may well work on your machine and give you no reason to suspect a problem. It then fails silently the moment the repo touches a case-sensitive filesystem - Linux CI, a cloud session, a collaborator on Linux. Nothing errors; the instructions just quietly stop loading.

I could not find an explicit statement in the docs about whether the lookup itself is case-sensitive, so treat the all-caps form as the only safe answer and don't test the boundary. If you ever suspect a naming problem, `/context` is the check: if the file doesn't appear under **Memory files**, Claude cannot see it.

The same convention applies to the companions:

| Correct                                      | Not                                   |
| -------------------------------------------- | ------------------------------------- |
| `CLAUDE.md`                                  | `Claude.md`, `claude.md`, `CLAUDE.MD` |
| `CLAUDE.local.md`                            | `CLAUDE.LOCAL.md`, `Claude.local.md`  |
| `SKILL.md` (inside `.claude/skills/<name>/`) | `skill.md`, `Skill.md`                |
| `.claude/settings.json`                      | `.claude/Settings.json`               |

Two related naming facts worth knowing:

- A skill must be `<name>/SKILL.md` in its own folder. A bare `.claude/skills/name.md` does not register - it's a documented cause of "my skill doesn't appear in `/skills`".
- Project MCP config is `.mcp.json` at the **repo root**, not inside `.claude/`. Putting it under `.claude/` is another documented silent failure.

______________________________________________________________________

## 2. You're right about the committed/local leak

You caught a real error in the first version of my templates. `CLAUDE.md.template` had a "Related repositories" section with an absolute checkout path in it, and `settings.json.template` had `additionalDirectories` full of drive-letter paths - both in files marked COMMIT. That's wrong, and it's wrong in the way that does the most damage: it works fine for you and quietly breaks for everyone and everywhere else.

The templates are fixed. The rule now stated in `01_repo_standards.md`:

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

### A dissenting note on `.status/`

> **Settled in `05_status_directory.md`:** you gitignore `.status/` in all 25 repos that have one, these repos are public, and that combination makes your choice the right one. Read `.status/` as **gitignored** everywhere in this folder. The paragraph below is kept for the reasoning, not the conclusion.

I have `.status/` as committed, and I'd defend that - decisions and plans are project history, and the whole point of writing them down is that they outlive your session and your machine. But it's a judgment call. If a plan document is really a personal scratchpad, either keep it in `CLAUDE.local.md` or split `.status/` into a committed part and a gitignored `.status/local/`.

______________________________________________________________________

## 3. What is `.claude/` for?

It's Claude Code's configuration directory - the tool-specific folder, exactly analogous to `.vscode/` or `.github/`. There are two of them and they layer:

- **`<repo>/.claude/`** - configuration for this project, mostly committed
- **`~/.claude/`** (on Windows, `%USERPROFILE%\.claude\`) - your configuration for every project, never committed. Per-machine: each machine you work from has its own.

The official inventory, project level:

```
your-repo/
|-- CLAUDE.md                     committed   instructions read every session
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
    |-- agents/                   committed   subagents with their own context window
    |   `-- code-reviewer.md
    |-- commands/                 committed   legacy single-file commands (use skills/)
    |-- workflows/                committed   scripts orchestrating many subagents
    `-- agent-memory/                         subagent memory, written by Claude
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
    |-- commands/                 personal single-file commands
    |-- agents/                   personal subagents
    |-- workflows/                personal workflows
    |-- output-styles/            system-prompt sections that adjust how Claude works
    |-- themes/                   custom color themes
    `-- projects/                 auto memory Claude writes and maintains itself
```

You need almost none of this. `CLAUDE.md` plus `.claude/settings.json` covers the first month. The rest exists for when a specific trigger appears - see the trigger table at the end of `01_repo_standards.md`.

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

Short answer: **not as top-level files, no.** I could not find either `.rules` or `.context` as a broadly adopted convention. What you're almost certainly seeing is a *rules subdirectory inside a tool's own folder*, which is a real and common pattern - just tool-scoped rather than universal.

Here's the actual landscape as of August 2026.

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

If your repos are private and only you and Claude ever read them, you don't need `AGENTS.md` at all - `CLAUDE.md` alone is simpler. Adopt it when a repo goes public, or when a collaborator uses a different tool.

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

Note the pattern: `.cursor/rules/`, `.windsurf/rules/`, `.devin/rules/`, `.claude/rules/`. **A `rules/` directory inside a dotted tool folder is the convention; a bare top-level `.rules` is not.** If you saw a literal `.rules` or `.context` in someone's repo, my read is that it's either one of the above with the parent folder collapsed in whatever listing you were looking at, or a project-local invention. Worth opening it to see - but I wouldn't copy it as a standard, because I can't verify it is one.

### Useful consequence: `/init` reads the competition

When you run `/init`, Claude Code reads Cursor rules (`.cursor/rules/` or `.cursorrules`) and Copilot rules (`.github/copilot-instructions.md`) and folds the relevant parts into the `CLAUDE.md` it generates. With `CLAUDE_CODE_NEW_INIT=1` set it also reads `AGENTS.md`, `.devin/rules/`, `.windsurf/rules/` or `.windsurfrules`, and `.clinerules`.

So if any of your repos already carry Copilot instructions - plausible, given you've been using Copilot - `/init` will pick them up rather than making you retype them. Worth checking for a `.github/copilot-instructions.md` before you start Phase 1.

### What I'd actually do

> **Superseded: `AGENTS.md` is now the single instruction source in every repo**, with `CLAUDE.md` reduced to the `@AGENTS.md` import - see `01_repo_standards.md`. The conclusion below changed when Copilot's native `AGENTS.md` support was verified and more than one assistant began working in these repos; the paragraph is kept for the reasoning.

For your five repositories: `CLAUDE.md` only. Skip `AGENTS.md` until a repo goes public or a collaborator shows up with a different tool, at which point the one-line `@AGENTS.md` import handles it. Don't invent a `.context` or `.rules` folder - `.claude/rules/` already does that job, and `.status/` already does the job of holding project reasoning.

______________________________________________________________________

## 5. Making the committed half work on both Windows and Linux

"No drive letters" is the obvious rule and it is not sufficient. A committed `CLAUDE.md` or `.claude/settings.json` gets read on your Windows box, on a colleague's Mac, and on Ubuntu in CI, and there are six other ways for it to be quietly Windows-only. All of these are real, and most of them were in the first draft of these templates.

| Trap                                     | Why it breaks                                                                          | What to commit instead                                                                                                                                                                              |
| ---------------------------------------- | -------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Bash(source .venv/Scripts/activate)`    | `Scripts/` is the Windows venv layout; POSIX is `bin/`                                 | Both forms. And know that **each Bash tool call is a fresh shell**, so activation never carries to the next call anyway - the real fix is to say "invoke the interpreter directly" in `CLAUDE.md`   |
| `python` in a documented command         | On many Linux and macOS setups only `python3` exists                                   | Name `python` in `CLAUDE.md` but say "an interpreter with the package installed"; put the exact interpreter in `CLAUDE.local.md`. Allow both `Bash(python --version)` and `Bash(python3 --version)` |
| A hook that runs `bash scripts/check.sh` | On native Windows the Bash tool needs Git Bash, and a hook is not guaranteed to get it | Write hooks as `python scripts/check.py`. Python is the one interpreter every contributor to a Python repo already has                                                                              |
| `Read(.\\vendor\\**)` with backslashes   | Permission patterns are globs; `\` is an escape character, not a separator             | Forward slashes always - `Read(./vendor/**)`. They work on Windows too                                                                                                                              |
| `Claude.md`, `claude.md`                 | NTFS is case-insensitive so it works for you and silently stops loading on Linux       | `CLAUDE.md`, and never two files differing only in case anywhere in the repo                                                                                                                        |
| CRLF in a committed file                 | A Windows editor writes CRLF; Linux tools and diffs then see the whole file as changed | `.gitattributes` with `* text=auto eol=lf` in every repo, plus `newline=""` on every text-mode write in Python. The `.gitattributes` is the backstop, not the fix                                   |
| Expecting the sandbox to enforce a rule  | Claude Code's OS-level sandbox is **not supported on native Windows** - WSL 2 only     | On Windows, enforcement means a `PreToolUse` hook. Treat the `deny` list as stated intent, not a wall                                                                                               |

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

The trigger was real: this folder was clean until a session added 91 non-ASCII characters to it (80 em dashes, 8 arrows, 2 en dashes, one ellipsis) across four files. It went in three places, and the reasoning for each is the general case:

1. `~/.claude/CLAUDE.md` on each machine - it applies to every project, so this is its real home.
2. `templates/AGENTS.md.template` - so every repo set up from the template inherits it, and public repos state it for collaborators.
3. This folder's `CLAUDE.md` (new) - this folder had no `CLAUDE.md`, which is precisely why the drift happened here and was not caught.

Note what the rule needed once it met a real codebase: **an exception clause.** `hed-metadata-toolkit` legitimately contains an accented surname and a CJK title as test fixtures, because folding them is what the code under test does. A style rule with no data exception would have had someone "fix" the fixtures and break the tests. Expect any blanket character rule to need that carve-out, and write it into the rule rather than leaving it to judgment.
