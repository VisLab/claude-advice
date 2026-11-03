# Using Claude Code across repos

## Central ideas

### Each agent accesses many repos

The recurring problems, each with its fix:

- **A kitchen sink session** - one task, then something unrelated, then back. The risk is highest when the repos are conceptually linked.

  **Fix:** `/clear` between unrelated tasks - one task per session. After two failed corrections on the same task, `/clear` and restart with a better prompt; a clean session outperforms a long one with accumulated corrections.

- **Over-specified AGENTS.md** - if Claude ignores half of it, it's too long.

  **Fix:** cut every line whose removal would not cause a mistake, and keep the file under 200 lines. Move rules that only matter for certain files into `.claude/rules/` with a `paths:` glob, so they load only when those files are touched.

- **A trust-then-verify gap** - plausible-looking output that doesn't hold up.

  **Fix:** require the evidence with the claim: the command that was run and its actual output - for metadata work, counts and a sample of records. Better, give the session something that returns pass/fail (a test, a schema check, a validator); without one, "looks done" is the only signal and you are the verification loop.

- **Infinite exploration** - "investigate the datasets" without scope will read hundreds of files.

  **Fix:** scope the ask ("read X and Y, then answer") or hand it to a subagent - it reads in its own context window and returns only the findings.

- **Stale data pollution** - Claude verifies a claim against cached or remembered data instead of measuring.

  **Fix:** make "verify" mean re-running the measurement in this session: ask for the command and today's output, and reject any number that arrives without them. Keep ephemeral counts out of committed files (a stale count reads as a target), and treat cached artifacts - old command output, dated cache buckets, numbers quoted from memory - as claims to re-check, never as verification.

- **Overly complex responses** - verbose, over-structured replies that are hard to wade through.

  **Fix:** demand the conclusion first with a length cap: "three or four sentences of takeaway, then the detail". This is the `For humans:` rule applied to answers. Put the instruction in `AGENTS.md` once ("lead with the conclusion") so it holds in every session instead of being re-asked.

### Context is the scarce resource

**Context is the scarce resource, not tokens or time.** Claude Code starts each session with an empty context window and fills it with: your CLAUDE.md files, skill descriptions, every file it reads, and every command output. Performance degrades as it fills - Claude starts "forgetting" earlier instructions.

That single constraint explains almost every recommendation below:

| Symptom                                                   | Cause                                                     | Fix                                                                   |
| --------------------------------------------------------- | --------------------------------------------------------- | --------------------------------------------------------------------- |
| Claude re-derives your project background every session   | The background only exists in your head and in past chats | Put durable facts in `AGENTS.md`, decisions in `.status/decisions.md` |
| Long prompts that explain history, then ask for something | You're paying context for narrative                       | Split: facts -> files, ask -> prompt                                  |
| Claude ignores an instruction you definitely gave         | AGENTS.md too long, rule buried                           | Keep AGENTS.md under 200 lines                                        |
| Session gets worse the longer it runs                     | Accumulated failed approaches                             | `/clear` between unrelated tasks                                      |
| "Investigate X" fills the window with file reads          | Unscoped exploration in the main context                  | "use a subagent to investigate X"                                     |

Docs: [best-practices](https://code.claude.com/docs/en/best-practices), [context-window](https://code.claude.com/docs/en/context-window)

______________________________________________________________________

Target state:

- **Each repo is self-contained.** `AGENTS.md` holds the instructions (`CLAUDE.md` imports it), `.claude/settings.json` holds the permissions, and `.status/` holds the working notes.
- **One repo is the hub.** It carries the map of the repositories and the cross-repo plans.
- **The working habit:** plan mode first; the plan is written to disk; a fresh session executes it; the result is verified against a check.

More than one assistant works in these repos, so the shared rules live in `AGENTS.md`, a file no single vendor owns. `CLAUDE.md` imports it and the machine-facts file, and `.github/copilot-instructions.md` is a pointer: every tool gets the same instructions without duplicating them. Machine facts go in `.status/local-environment.md`, which any tool can read. The wiring and the sources are detailed in the rest of this document.

## The shape

The standard shape for a repository. Verified against `code.claude.com/docs` and the GitHub Copilot documentation; the sources, and the date they were checked, are at the bottom.

```
your-repo/
|-- AGENTS.md                    # committed - THE instruction file, under 200 lines
|-- CLAUDE.md                    # committed - imports AGENTS.md and .status/local-environment.md
|-- README.md                    # committed - for humans browsing GitHub
|-- .github/
|   `-- copilot-instructions.md  # committed - a pointer to AGENTS.md, duplicating nothing
|-- .claude/
|   |-- settings.json            # committed - portable permission rules only
|   `-- settings.local.json      # gitignored - personal grants, absolute paths
|-- .vscode/
|   `-- settings.json            # committed - portable editor settings only
|-- .status/                     # gitignored - plans, notes, decisions, working prompts
|-- .env.example                 # committed - documents every variable .env needs
|-- .env                         # gitignored - real tokens and machine values
|-- .editorconfig                # committed - LF and whitespace defaults for every editor
`-- .gitattributes               # committed - line-ending normalization
```

## One instruction file: AGENTS.md

A repo's instructions live in one committed file, `AGENTS.md`. Three facts, checked against the vendors' documentation rather than assumed, settle the wiring:

- **Claude Code reads `AGENTS.md` natively (2.1.277 and later), but only when no `CLAUDE.md` or `CLAUDE.local.md` exists** in the working directory or above. A repo that has a `CLAUDE.md` for any other reason must import `AGENTS.md` from it, which its docs also prescribe: "create a `CLAUDE.md` that imports it so both tools read the same instructions without duplicating them."
- **`CLAUDE.md` is kept for one job: imports.** `@path` imports are a `CLAUDE.md` feature; they are not documented for a natively read `AGENTS.md`. The machine-facts file, `.status/local-environment.md`, has to reach every session, so `CLAUDE.md` imports it alongside `AGENTS.md`. A missing import is skipped silently (measured: a `CLAUDE.md` importing an absent file loaded its other import and started with no warning), so the committed file is safe in a clone that has no `.status/`.
- **GitHub Copilot reads `AGENTS.md` natively** - in VS Code and in the coding agent - while still supporting `.github/copilot-instructions.md`.

`CLAUDE.md` cannot be the shared instruction file: more than one assistant works in these repos, and the other tools do not read a file named for one vendor. The same reasoning puts machine facts in `.status/local-environment.md`, which every tool can read, rather than in a Claude-only file. `CLAUDE.local.md` is therefore not part of the standard: it stays in `.gitignore` so that a personal file, if someone wants one, never ships, but no repo needs one.

One source, several pointers - a rule stated in two files is a rule that will disagree with itself:

- **`CLAUDE.md`** is the two imports plus a one-paragraph orientation, and nothing else. Keep a blank line between the imports: mdformat joins adjacent lines into one paragraph, and whether Claude Code reads two `@` imports from one line is undocumented.

  ```markdown
  @AGENTS.md

  @.status/local-environment.md

  # Claude Code

  `AGENTS.md`, imported above, is the whole instruction set.
  `.status/local-environment.md`, also imported, holds this machine's paths
  and quirks for every tool. Path-scoped rules in `.claude/rules/` load when
  a session touches matching files. After changing an import, run `/context`
  and confirm the file appears under **Memory files**.
  ```

- **`.github/copilot-instructions.md`** says "read `AGENTS.md` and follow it" and duplicates nothing.

Templates for all three: `templates/AGENTS.template.md`, `templates/CLAUDE.template.md`, and `templates/copilot-instructions.template.md` (`templates/README.md` indexes the full set).

## What goes in AGENTS.md

Under 200 lines - past that, instructions stop being read, by people and by assistants alike; a whole repo's rules fit in fewer. The sections that earn their place: commands (the exact test, lint, and format invocations, and what CI runs), layout (one line per top-level thing), conventions that differ from defaults, rules that are easy to get wrong, and working agreements.

One line is mandatory:

```
Test framework: unittest | pytest
```

The framework is whichever one the repo's suite was written in, declared once so it is an explicit choice rather than something the repo drifts into. `python -m pytest` runs a unittest suite unchanged, so the runner can be uniform across repos either way - but never convert a suite from one style to the other as a side effect of other work.

## Four rules for every committed file

The reader is a stranger on GitHub; all four follow from that.

1. **No project history.** No dates, no "this was changed", no "previously", no phase, session, or PR labels. A committed file says what is true now and the rule a reader must follow; how it got that way goes in `.status/decisions.md`.
2. **No references to `.status/`.** It is gitignored, so the pointer is a dead link for everyone but its author. Exception: the files whose job is to orient a tool - `AGENTS.md`, `CLAUDE.md`, `.github/copilot-instructions.md`, `.gitignore`, `.claude/settings.json` - may name `.status/README.md`, `.status/decisions.md`, `.status/plans/`, and `.status/local-environment.md` as places to look.
3. **No local path or drive letter.** Machine facts go in `.status/local-environment.md`; examples use placeholders (`REPO_NAME`, not a real dataset ID). Grep committed files for drive letters before pushing.
4. **No ephemeral facts.** Test counts, dependency pins, and dataset counts change on their own, and a stale count reads as a target; point at the file that owns the fact instead of restating it.

## `.status/` is gitignored

These repos are public and `.status/` holds half-formed thinking, so it stays out of git everywhere. Take the consequence seriously: **there is no safety net.** Nothing under `.status/` is versioned or backed up, nothing appears in a fresh clone or a `claude --worktree` worktree, and a deleted file is simply gone. So finished work moves to `.status/archive/` rather than being deleted, and nothing under `.status/` is rewritten without its owner's say-so.

Layout, naming, and retention rules: `05_status_directory.md`.

## Committed or gitignored

| Committed                                                   | Gitignored                        |
| ----------------------------------------------------------- | --------------------------------- |
| `AGENTS.md`, `CLAUDE.md`, `.github/copilot-instructions.md` | `CLAUDE.local.md` (optional)      |
| `.claude/settings.json`                                     | `.claude/settings.local.json`     |
| `.vscode/settings.json` (portable settings only)            | `.status/`                        |
| `.env.example`                                              | `.env`                            |
| `.gitattributes`, `.editorconfig`, `README.md`              | `.venv/` and everything generated |

The test for the left column: would this line be true on a colleague's laptop and on Linux CI? If not, it goes on the right, or into `.status/local-environment.md`.

Two gotchas:

- Put `.claude/settings.local.json` in `.gitignore` up front, when the repo is set up - `templates/gitignore-snippet.txt` is the block to paste. Claude Code adds the entry itself only when it creates the file (saving a permission you approved); a file you create by hand gets no such protection, and it is exactly the file that collects absolute paths.
- Everything in the right column is absent from clones and worktrees. That is the point, but it means a second machine starts with none of it.

## `.claude/settings.json`

Committed, so relative paths only. The shape that works: allow the repo's own test, lint, and format commands; ask before `git add`, `git commit`, and content-destroying restores; deny `Read(.env)`, `git push`, package installs, and network fetchers. `templates/settings.template.json` is the copy-paste starting point.

Three facts about rules that are easy to get wrong:

- **A deny is a wall, not a prompt.** Deny rules are evaluated before ask and allow, and nothing can approve one at prompt time, so a deny must never cover something `AGENTS.md` permits on request. The archive guard ("do not read `.status/archive/` unless a file is named for you") is an instruction in `AGENTS.md` and the conduct rule, not a deny: the hazard is context flooding, not secrets, and a deny would also block the named-file exception. `.status/scratch/` stays readable too - it is the agents' workbench for throwaway scripts; see `05_status_directory.md`.
- **A rule without `*` matches one exact command.** `Bash(npm test)` does not match `npm test -- --watch`; write `Bash(npm test *)`. A trailing ` *` also matches the bare command, so `Bash(git log *)` covers `git log`.
- **Rules are per shell tool.** A `Bash(...)` rule does not govern Claude Code's PowerShell tool, which has its own `PowerShell(...)` rules, and on Windows with Git Bash installed Claude Code offers both tools and treats PowerShell as primary. Rather than keep two copies of every list, a Windows machine with Git Bash turns the PowerShell tool off: `CLAUDE_CODE_USE_POWERSHELL_TOOL=0` as a user environment variable (verified: the session's shell tools go from "Bash, PowerShell" to "Bash"). That affects only Claude's tool set, not the person's own terminal. The committed rules are then Bash rules only.

Read-only shell commands (`cat`, `head`, `tail`, `grep`, `find`, `wc`, read-only `git`) need no allow rule: Claude Code runs its built-in read-only set without a prompt in every mode. Explicit `ask` rules prompt in every mode, including auto mode, so the ask list is exactly the set of things that should always stop for a human.

Do not set `permissions.blockReadsOutsideWorkingDirectories`. While it is on, any Bash command the shell parser cannot trace prompts even in auto mode, whether or not it names an outside path, and a running session keeps the block until restarted. Sessions that need a sibling checkout add it with `--add-dir`.

Gotcha: project settings load only from the directory Claude Code is started in - they are not inherited from parent directories the way `CLAUDE.md` files are.

## `.vscode/settings.json`

Committed, portable settings only - workspace settings override user settings, so a machine-specific value here is imposed on everyone. Interpreter paths go in your VS Code user settings; environment values go in `.env`.

The testing keys must match the repo's declared framework: `python.testing.pytestEnabled` true and `python.testing.unittestEnabled` false in a pytest repo, the reverse in a unittest repo. The wrong pair makes test discovery silently show nothing.

Also set `files.eol` to `"\n"`, `files.trimTrailingWhitespace`, and `files.insertFinalNewline` - the VS Code layer of the line-ending defence described next. `templates/vscode-settings.template.json` is the starting point.

## Line endings: .editorconfig and the CRLF check

Every repository is LF only, on every OS, and four layers keep it that way:

- **`.editorconfig`** (`end_of_line = lf`) - every editor that reads EditorConfig, for every file, including gitignored working files.
- **`.vscode/settings.json`** (`files.eol`) - VS Code, for new files in that workspace.
- **`.gitattributes`** (`* text=auto eol=lf`) - what git stores, at commit time.
- **A CI check** that fails when `git ls-files --eol` reports a tracked text file as CRLF or mixed - anything that reached a commit by another route.

`.gitattributes` and the CI check never see gitignored files; only the editor layers reach them. A file committed before `.gitattributes` existed keeps its CRLF until renormalized, so in a repo with committed CRLF run `git add --renormalize .` as a commit of its own before adding the check.

`templates/editorconfig.template` is the floor, not the ceiling: a repo may add sections (indent rules per file type, for example) but does not override the `[*]` keys. It trims trailing whitespace in Markdown too, so write a hard line break as a trailing backslash rather than two spaces - which is what mdformat produces anyway. `templates/ci-crlf-check.template.yml` is the CI step.

## The ruff lint block

One rule set for every repo that lints, so ruff behaves identically in every session and every repo: select E, W, F, I, N, B, C4, UP; ignore E501, N802, N803, N806. `templates/ruff-lint-snippet.toml` is the paste-in block; it also sets `[tool.ruff.format] line-ending = "lf"`, because the default, `auto`, keeps whatever ending a file already has. The families beyond the flake8 baseline earn their place: I makes import order deterministic and is fully auto-fixable, which removes a whole class of diff noise in repos that several assistants write in; UP keeps syntax at the repo's declared Python floor and is nearly all auto-fixable; N catches naming errors in public APIs, with the three ignores covering legacy camelCase test methods and scientific naming (`df`-style locals and arguments).

Two rules that come from how these configs actually drift:

- A committed doc never restates the rule list - it points at `pyproject.toml`. A restated list and the config it restates will disagree eventually, and the doc is the one that will be wrong.
- Delete dead config on sight: an ignore for a family that is not selected, or a mccabe setting without C90 selected, does nothing but mislead the next reader into thinking it is policy.

`__init__.py` files are exempt from both F401 (unused imports are re-exports) and I001 (their import order is often curated by hand to dodge circular imports - an auto-sort can turn a working package into an ImportError at import time). Never let a lint autofix reorder an `__init__.py`; if one is reordered and imports break, restore the original order rather than restructuring the package.

A repo whose only Python is a single utility script gets no ruff config; the overhead is not worth it for one file.

## Per-repo checklist

- [ ] `AGENTS.md` under 200 lines, with the `Test framework:` line
- [ ] `CLAUDE.md` is `@AGENTS.md` and `@.status/local-environment.md` plus the orientation paragraph; `/context` shows it under **Memory files**; no `CLAUDE.local.md` is needed
- [ ] `.github/copilot-instructions.md` points at `AGENTS.md`, duplicates nothing
- [ ] `.claude/settings.json` committed; `Read(.env)` denied; no `Read(.status/archive/**)` deny; no allow rules for read-only shell commands; every allow rule for a command that takes arguments ends in ` *`; Bash rules only; no `blockReadsOutsideWorkingDirectories`; relative paths only
- [ ] `.vscode/settings.json` committed; testing keys match the declared framework
- [ ] `.gitignore` covers `.status/`, `.env`, `CLAUDE.local.md`, `.claude/settings.local.json`
- [ ] `.env.example` documents every variable `.env` needs
- [ ] `.gitattributes` normalizes line endings, and no tracked text file is CRLF (`git ls-files --eol | grep -E '^i/(crlf|mixed)' | grep -v attr/-text` prints nothing)
- [ ] `.editorconfig` committed (LF, final newline, trailing whitespace trimmed, UTF-8); extra sections allowed, `[*]` keys not overridden
- [ ] Where the repo has CI, the main workflow runs the CRLF check from `templates/ci-crlf-check.template.yml`
- [ ] Repos with a ruff config: lint block matches `templates/ruff-lint-snippet.toml`, no dead config; single-utility-script repos have no ruff config
- [ ] No drive letter, no project history, no `.status/` pointer in any committed file
- [ ] Every command in `AGENTS.md` verified to actually run

## Sources

Checked 2026-08-09:

- [Memory - AGENTS.md and imports](https://code.claude.com/docs/en/memory) - the `@AGENTS.md` recommendation quoted above, and the Windows symlink caveat
- [Settings](https://code.claude.com/docs/en/settings) - settings files, precedence, and the load-from-starting-directory behaviour
- [GitHub Copilot - repository custom instructions](https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions) - native `AGENTS.md` support alongside `copilot-instructions.md`

Checked 2026-11-03:

- [Permissions](https://code.claude.com/docs/en/permissions) - the built-in read-only command set, and that `Read` deny rules do not cover commands that read files without naming them
