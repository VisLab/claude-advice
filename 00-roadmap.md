# Roadmap: getting good at Claude Code across many repos

Written for Kay, August 2026. Every factual claim here was checked against `code.claude.com/docs` on 2026-08-03; links are at the bottom of each section.

______________________________________________________________________

## The one idea everything else follows from

**Context is the scarce resource, not tokens or time.** Claude Code starts each session with an empty context window and fills it with: your CLAUDE.md files, skill descriptions, every file it reads, and every command output. Performance degrades as it fills - Claude starts "forgetting" earlier instructions.

That single constraint explains almost every recommendation below:

| Symptom you've probably hit                               | Cause                                                     | Fix                                                                   |
| --------------------------------------------------------- | --------------------------------------------------------- | --------------------------------------------------------------------- |
| Claude re-derives your project background every session   | The background only exists in your head and in past chats | Put durable facts in `AGENTS.md`, decisions in `.status/decisions.md` |
| Long prompts that explain history, then ask for something | You're paying context for narrative                       | Split: facts -> files, ask -> prompt                                  |
| Claude ignores an instruction you definitely gave         | AGENTS.md too long, rule buried                           | Keep AGENTS.md under 200 lines                                        |
| Session gets worse the longer it runs                     | Accumulated failed approaches                             | `/clear` between unrelated tasks                                      |
| "Investigate X" fills the window with file reads          | Unscoped exploration in the main context                  | "use a subagent to investigate X"                                     |

Docs: [best-practices](https://code.claude.com/docs/en/best-practices), [context-window](https://code.claude.com/docs/en/context-window)

______________________________________________________________________

## Where you are and where this is going

Your current setup, as far as I can tell from your prompt:

- Work spans at least 5 locations on 2 drives: `task-research`, `hed-task`, `hed-metadata-toolkit`, `nemar-metadata`, and a citation staging folder. The paths belong in `.status/local-environment.md`, not here.
- You already have a `.status/` convention (`.status/TaskResearchStructure.md`) - this is genuinely good practice and the docs independently recommend it ("ask Claude to write the plan to a markdown file in the repository ... the saved plan survives where conversation history may not")
- You're asking Claude to "add to your trusted folders" inside a prompt. That isn't how directory access works - see Phase 2. This is probably the single biggest mechanical thing to fix.
- Each session starts by re-explaining the nemar/openneuro history. That history is a *decision record* and belongs in a file.

Target state:

```
Each repo:  self-contained. AGENTS.md (CLAUDE.md imports it) + .claude/settings.json + .status/
One repo:   the "hub" - holds the map of repos and cross-repo plans
Your habit: plan mode -> plan doc on disk -> fresh session to execute -> verify
```

More than one assistant works in these repos, so the shared rules live in `AGENTS.md`, a file no single vendor owns. `CLAUDE.md` is the `@AGENTS.md` import plus Claude-Code-specific notes, and `.github/copilot-instructions.md` is a pointer: Claude Code does not read `AGENTS.md` and Copilot does, so this wiring gives every tool the same instructions without duplicating them. Machine facts go in `.status/local-environment.md`, which any tool can read - `CLAUDE.local.md` is loaded only by Claude Code, so it holds nothing another assistant would need. The wiring and the sources are in `01-repo-standards.md`.

______________________________________________________________________

## Phase 0 - Half an hour, once

1. Confirm the install is healthy - same commands in PowerShell and bash:

   ```
   claude --version
   claude doctor
   ```

   `claude doctor` prints install health, settings-file validation errors, and warnings with suggested fixes, without starting a session.

2. **Windows only: install [Git for Windows](https://git-scm.com/downloads/win)** if you haven't. On native Windows, Claude Code uses Git Bash for its Bash tool; if Git Bash is absent it falls back to the PowerShell tool. If it can't find Git Bash, point it there in your user settings (`%USERPROFILE%\.claude\settings.json`):

   ```json
   { "env": { "CLAUDE_CODE_GIT_BASH_PATH": "<absolute path to Git's bin\\bash.exe>" } }
   ```

   Linux and macOS need no equivalent step - the Bash tool uses the system shell.

3. Write a short user-level `CLAUDE.md` at `~/.claude/CLAUDE.md` (on Windows, `%USERPROFILE%\.claude\CLAUDE.md`). This loads in *every* session, every project - but it is per-machine, so put a copy on each machine you work from. Keep it to genuine personal preferences - 10-20 lines. Example:

   ```markdown
   - I am a researcher, not a software engineer by trade. Explain the "why" of
     structural suggestions briefly; don't just do them silently.
   - Prefer Python. Use pathlib, not os.path. Type-hint public functions.
   - When a task spans more than ~3 files, write a plan to `.status/` first and
     let me read it before editing.
   - Never delete or rewrite files under `.status/` without asking.
   - Windows paths: drive letters are case-insensitive but be consistent -
     always uppercase.
   ```

4. Learn these five keystrokes and nothing else for now:

   | Key         | Does                                                      |
   | ----------- | --------------------------------------------------------- |
   | `Shift+Tab` | Cycle permission mode: default -> acceptEdits -> **plan** |
   | `Esc`       | Stop Claude mid-action, context preserved, redirect       |
   | `Esc Esc`   | Rewind menu - restore conversation and/or code state      |
   | `/clear`    | Wipe context. Use between unrelated tasks.                |
   | `/context`  | Show what actually loaded, including which memory files   |

   `/context` is the debugging tool. If a CLAUDE.md isn't listed under **Memory files**, Claude cannot see it.

Docs: [setup](https://code.claude.com/docs/en/setup), [memory](https://code.claude.com/docs/en/memory)

______________________________________________________________________

## Phase 1 - One pass per repository (~20 min each)

Do this in each of your five locations. Details and templates in `01-repo-standards.md`.

1. `cd` into the repo, run `claude`, then `/init`. It analyzes the codebase and writes a starting `CLAUDE.md` with build commands, test instructions, and conventions it discovers. If a CLAUDE.md already exists, `/init` proposes improvements instead of overwriting.
2. **Then prune it.** `/init` output is a first draft and is usually too long. For every line ask the docs' question: *"would removing this cause Claude to make mistakes?"* If not, cut it. Target under 200 lines.
3. Move the pruned content into `AGENTS.md`, shrink `CLAUDE.md` to the `@AGENTS.md` import plus any Claude-Code-specific notes, and add the `.github/copilot-instructions.md` pointer. `01-repo-standards.md` has the wiring and the reasons.
4. Add `.claude/settings.json` with read-deny rules for generated/vendored content and (where needed) sibling-repo access.
5. Add `.status/` with `decisions.md` if you don't have one. This is where the nemar-vs-openneuro reasoning goes.
6. Commit the shared set: `AGENTS.md`, `CLAUDE.md`, `.github/copilot-instructions.md`, `.claude/settings.json`. `CLAUDE.local.md` and `.claude/settings.local.json` are personal and gitignored, and `.status/` is gitignored too.

Order I'd suggest, easiest-to-hardest so you build the habit on a small repo first: `hed-metadata-toolkit` -> `hed-task` -> `nemar-metadata` -> `task-research`.

______________________________________________________________________

## Phase 2 - Make the multi-repo problem go away

This is the part your current prompt is fighting. Three mechanisms, and they are **not** interchangeable:

| How you add a directory                                              | Claude can read/edit it | Loads its CLAUDE.md + rules  | Loads its skills |
| -------------------------------------------------------------------- | ----------------------- | ---------------------------- | ---------------- |
| `permissions.additionalDirectories` in `.claude/settings.local.json` | Yes                     | **Never**                    | **Never**        |
| `--add-dir` flag at launch, or `/add-dir` mid-session                | Yes                     | Only with an env var (below) | Yes              |

To also load memory files from an added directory:

```powershell
# PowerShell
$env:CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD = 1
claude --add-dir <absolute path to nemar-metadata>
```

```bash
# bash (Linux/macOS)
CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1 claude --add-dir <absolute path to nemar-metadata>
```

(The env var has no effect on directories listed in `additionalDirectories`.)

**Three things to internalize:**

1. **"Add to your trusted folders" in a prompt does nothing.** Directory access is a launch flag, a slash command, or a settings file. Not a request.
2. **Where you launch `claude` decides almost everything** - which files are reachable without a grant, which CLAUDE.md files load, and which `.claude/settings.json` applies. Project settings load *only* from the starting directory; they are **not** inherited from parent directories the way CLAUDE.md files are.
3. **Ancestor CLAUDE.md discovery walks up the directory tree** from your working directory. Your repos are on two different drives, so there is no common ancestor - a shared parent CLAUDE.md is not available to you. Use explicit `--add-dir`, or `@` imports with absolute paths (imports accept both relative and absolute paths, max 4 hops deep). Verify with `/context` that the import actually resolved; cross-drive absolute imports are something I'd test rather than assume.

### Pick a hub

Designate **`task-research` as the hub**. It already has `.status/` and it's where your cross-cutting thinking lives. In it:

- `REPOS.md` - the map: every repo, its one-line purpose, what it owns, what it depends on. Template provided.
- `.status/` - cross-repo plans, one file per initiative, plus `decisions.md`.
- `.claude/skills/` - the workflows you'll otherwise retype.

Then launch from the hub with the sibling repos added:

```
# same in PowerShell and bash
cd <absolute path to task-research>
claude --add-dir <absolute path to hed-task> --add-dir <absolute path to nemar-metadata>
```

Or, so you don't retype it, put the durable set in the hub's `.claude/settings.local.json` - the **gitignored** settings file, because these paths are true only on your machine and must never be committed:

```json
{
  "permissions": {
    "additionalDirectories": [
      "<absolute path to hed-task>",
      "<absolute path to hed-metadata-toolkit>",
      "<absolute path to nemar-metadata>",
      "<absolute path to the citation staging folder>"
    ]
  }
}
```

Remember: this grants *file access only*, no CLAUDE.md, no skills. That's often what you want - you get to read the other repos without paying context for four more instruction files.

Add `.claude/settings.local.json` to `.gitignore` yourself. It is auto-gitignored only when Claude Code writes a setting to it, not when you create it by hand. See `templates/gitignore-snippet.txt` and `04-file-conventions.md` for the full committed-vs-local split.

**When to use one session vs. several:** if a change touches several repos together (updating a shared schema and every consumer), do it in one session - the docs are explicit that handing over the whole change keeps the decisions consistent instead of re-deriving them per repo. If the tasks are independent, use separate sessions; a fresh context is better than a shared one.

Docs: [large-codebases](https://code.claude.com/docs/en/large-codebases)

______________________________________________________________________

## Phase 3 - Stop retyping (skills)

The trigger is mechanical: **the third time you paste the same multi-step procedure into chat, it becomes a skill.**

A skill is a directory with a `SKILL.md`:

```
.claude/skills/plan-doc/SKILL.md   ->  invoke with /plan-doc
```

Its body loads only when used, so long reference material costs almost nothing until you need it. (Custom commands have been merged into skills - `.claude/commands/deploy.md` and `.claude/skills/deploy/SKILL.md` both create `/deploy`. Skills are the current form.)

Three skills I'd write first for your work, based on your prompt:

| Skill            | Why                                                                                                                                                      |
| ---------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `/plan-doc`      | You asked Claude to "provide another plan in task-research.status". Encode the format once: filename convention, required sections, where it links from. |
| `/status-update` | Reconcile a `.status/` plan against what's actually on disk and mark steps done. You will want this constantly.                                          |
| `/dataset-audit` | Whatever your repeated "check this dataset's metadata against X" procedure is.                                                                           |

Set `disable-model-invocation: true` on skills with side effects, so only you trigger them and they cost zero context until invoked.

Docs: [skills](https://code.claude.com/docs/en/skills), [features-overview](https://code.claude.com/docs/en/features-overview)

______________________________________________________________________

## Phase 4 - VS Code

Do this *after* Phases 0-2. The extension shares `~/.claude/settings.json`, CLAUDE.md, and your conversation history with the CLI, so a good CLI setup carries over for free - and a bad one carries over too. See `03-vscode.md`.

______________________________________________________________________

## Phase 5 - The working habits that matter most

In rough order of payoff:

1. **Plan mode for anything you can't describe in one sentence.** `Shift+Tab` to plan mode; Claude reads and proposes but writes nothing until you approve. Press `Ctrl+G` to open the plan in your editor and edit it directly. Skip plan mode for typos and one-liners - it's overhead there.

2. **Plans go on disk, then start a fresh session to execute.** Long sessions compact their context; a file doesn't. This is the single practice most suited to how you work.

3. **Let Claude interview you when the goal is still fuzzy.** This is the right move for your task-modeling problem specifically. The docs' prompt:

   ```
   I want to build [brief description]. Interview me in detail using the
   AskUserQuestion tool.

   Ask about technical implementation, UI/UX, edge cases, concerns, and
   tradeoffs. Don't ask obvious questions, dig into the hard parts I might
   not have considered.

   Keep interviewing until we've covered everything, then write a complete
   spec to SPEC.md.
   ```

   Then `/clear` and execute against `SPEC.md` in a clean session.

4. **Delegate reading to subagents.** "use a subagent to investigate how the nemar metadata represents task labels" - it reads in its own context window and returns only findings.

5. **Give Claude something that returns pass/fail.** A test, a script that validates output against a fixture, a schema check. Without a check, "looks done" is the only signal and *you* are the verification loop. With one, Claude iterates until it passes.

6. **`/clear` after two failed corrections.** From the docs: "A clean session with a better prompt almost always outperforms a long session with accumulated corrections."

7. **`/usage`** to see what's actually consuming your plan - it flags behaviors accounting for 10%+ of recent usage and attributes usage per skill, subagent, plugin, and MCP server.

______________________________________________________________________

## Failure patterns to watch for in your own work

Straight from the docs, annotated for your situation:

- **The kitchen sink session** - one task, then something unrelated, then back. You are at high risk of this because your repos are conceptually linked. Fix: `/clear`.
- **The over-specified AGENTS.md** - if Claude ignores half of it, it's too long.
- **The trust-then-verify gap** - plausible-looking output that doesn't hold up. For metadata/citation work specifically: always have Claude show you counts, a sample of records, and the command it ran.
- **The infinite exploration** - "investigate the nemar datasets" without scope will read hundreds of files. Scope it or subagent it.

______________________________________________________________________

## Reading order for the rest of this folder

1. `01-repo-standards.md` - what goes in every repo, with a checklist
2. `02-prompt-patterns.md` - including a rewrite of your actual prompt
3. `03-vscode.md` - extension setup and what belongs where
4. `templates/` - copy-paste starting points
