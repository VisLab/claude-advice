# The VS Code extension

## VS Code extension versus the CLI

The extension and the CLI **share your configuration and your history**:

- `~/.claude/settings.json` (i.e. `%USERPROFILE%\.claude\settings.json`) - same file
- CLAUDE.md files, `.claude/rules/`, `.claude/skills/`, hooks - same files
- Conversation history - same sessions. Start in the panel, continue with `claude --resume` in the terminal, and vice
  versa.
- Plugins and marketplaces - configure in either, available in both

So the setup work in `01_repo_standards.md` - the `AGENTS.md` wiring, settings, directory access - is not CLI-specific.
Set the CLI up properly and the extension inherits all of it. That's also the catch: if your CLAUDE.md is bloated, the
extension is bloated too.

______________________________________________________________________

## Install

Requires **VS Code 1.94.0 or later** (Help -> About) and a paid Claude subscription or Console account - no API key
needed.

`Ctrl+Shift+X` -> search "Claude Code" -> Install. Then reload the window (Command Palette -> "Developer: Reload
Window") if nothing appears.

Four ways to open it, and knowing more than one saves frustration:

| Where                                           | Note                                                        |
| ----------------------------------------------- | ----------------------------------------------------------- |
| Spark icon in the editor toolbar, top-right     | **Only appears when a file is open** - this trips people up |
| Spark icon in the Activity Bar (left)           | Always visible; opens the sessions list                     |
| `* Claude Code` in the Status Bar, bottom-right | Works with no file open                                     |
| Command Palette -> "Claude Code"                | "Open in New Tab", etc.                                     |

Sign in when prompted. If you have `ANTHROPIC_API_KEY` set in your shell and get stuck on the sign-in screen, VS Code
didn't inherit your environment - launch it from a terminal with `code .`, or just sign in with your Claude account.

______________________________________________________________________

## Configure it once

VS Code Settings (`Ctrl+,`) -> Extensions -> Claude Code. The three that matter:

| Setting                            | Set to        | Why                                                                                                                                        |
| ---------------------------------- | ------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| `claudeCode.initialPermissionMode` | `plan`        | New conversations start in plan mode. Given your work, this is the right default - you get a reviewable plan before anything touches disk. |
| `claudeCode.preferredLocation`     | `sidebar`     | Keeps Claude visible beside your code. You can also just drag the panel wherever you like.                                                 |
| `claudeCode.useTerminal`           | leave `false` | The graphical panel is the point. Flip it to `true` only if you want CLI-in-a-tab.                                                         |

Others worth knowing: `autosave` (default true - saves files before Claude reads or writes them), `respectGitIgnore`
(default true), `usePythonEnvironment` (default true - activates the workspace's Python env, needs the Python
extension).

Those are your VS Code User settings. The *workspace* file each repo commits - `.vscode/settings.json`, portable
settings only - starts from `templates/vscode-settings.template.json`; see `01_repo_standards.md`.

______________________________________________________________________

## What the extension gives you that the terminal doesn't

**Plan review as a real document.** In plan mode, VS Code opens the plan as a full Markdown document where you can add
**inline comments** to give feedback before Claude begins. For a plan spanning three repos and twelve steps, this is
much better than reading it scroll past in a terminal.

**Side-by-side diffs with permission prompts.** Every proposed edit shows as a diff you accept, reject, or redirect. If
you edit the proposed content directly in the diff before accepting, Claude is told you modified it, so it doesn't
assume the file matches its proposal.

**Selection awareness.** Highlight lines and Claude sees them automatically. The prompt box footer shows how many lines
are selected; click the indicator to toggle visibility (eye-slash = hidden from Claude). `Alt+K` inserts an explicit
`@file.py#5-10` reference.

**`@terminal:name`** pulls a terminal's output into your prompt - no copy-pasting stack traces.

**Rewind/checkpoints via hover.** Hover any message -> rewind: fork the conversation, rewind the code, or both. Note:
checkpoints only track changes made through Claude's file-editing tools. Changes made via Bash commands or external
processes are **not** captured. Not a substitute for git commits.

**Session history with search.** Button at the top of the panel; search by keyword or browse by day. Sessions get
AI-generated titles; you can rename them.

**Multiple conversations.** "Open in New Tab" / "Open in New Window" from the Command Palette. Each has its own context.
A colored dot on the spark icon: blue = permission request pending, orange = Claude finished while the tab was hidden.

**`/plugins` and `/mcp` as dialogs** instead of CLI flags.

**`/usage`** opens an Account & usage dialog showing your plan limits, plus attribution for which skills, subagents,
plugins, and MCP servers consumed usage. Useful if you're near a cap. Figures are approximate and computed from local
sessions on that machine only.

______________________________________________________________________

## What the extension does *not* have

| Feature             | CLI | Extension                                                      |
| ------------------- | --- | -------------------------------------------------------------- |
| Commands and skills | All | **Subset** - type `/` to see what's available                  |
| MCP server config   | Yes | Partial - add servers via CLI, manage with `/mcp` in the panel |
| `!` bash shortcut   | Yes | No                                                             |
| Tab completion      | Yes | No                                                             |
| Checkpoints         | Yes | Yes                                                            |

Also: **installing the extension does not put `claude` on your PATH.** The extension bundles a private copy of the CLI
for its own panel. If you want to type `claude` in the integrated terminal, you need the standalone install too:
`irm https://claude.ai/install.ps1 | iex` in PowerShell on Windows, `curl -fsSL https://claude.ai/install.sh | bash` on
Linux and macOS. Having both is normal and recommended.

Background process visibility is weaker than the CLI. For a long-running job, have Claude print the command and run it
yourself in the integrated terminal.

______________________________________________________________________

## Sources of failure for extension

In rough order of likelihood:

1. **You tried it before setting up Claude for the repo.** With no CLAUDE.md, no repo map, and no directory access
   configured, the extension is just a chat box that can see one folder. All the leverage is in the configuration, and
   it's shared with the CLI - so it wasn't really an extension problem.

2. **The workspace folder wasn't the repo root.** The extension works against the folder you have open. If you opened a
   parent folder holding several repos you got a Claude that sees all of them and loads no project CLAUDE.md; if you
   opened one repo you get the right one. **Open one repository per VS Code window.** Your repos are on two different
   drives, so a multi-root workspace is a configuration I'd test deliberately rather than assume works cleanly - start
   with one repo per window and use `/add-dir` when you need a sibling.

3. **Spark icon nowhere to be found.** It only appears in the editor toolbar when a file is open. Use the Status Bar
   entry instead.

4. **Another AI extension was interfering.** Copilot, Cline, and Continue can conflict. Disable Copilot in workspaces
   where you're using Claude and see if things settle.

5. **You were reaching for a CLI-only feature** (a slash command not in the subset, `!` bash, tab completion) and
   concluded the extension was broken.

6. **Restricted Mode.** The extension doesn't work in VS Code's Restricted Mode. Check workspace trust if it seems
   inert.

If it still misbehaves: Command Palette -> "Claude Code: Show Logs", and `claude doctor` from a terminal.

______________________________________________________________________

## Which tool for which job

| Task                                                                      | Use                                                  |
| ------------------------------------------------------------------------- | ---------------------------------------------------- |
| Reviewing a multi-step plan before it runs                                | **Extension** - inline comments on the plan document |
| Reviewing proposed edits to code you know well                            | **Extension** - side-by-side diffs                   |
| Iterating on a Python module with the editor right there                  | **Extension**                                        |
| Anything Jupyter - the extension can execute cells in the active notebook | **Extension**                                        |
| Long unattended runs, batch work over many files                          | **CLI** - `claude -p`, loops, `--allowedTools`       |
| Multi-repo sessions with several `--add-dir` targets                      | **CLI** - flags are simpler than workspace juggling  |
| Anything scripted or scheduled                                            | **CLI**                                              |
| Parallel isolated work                                                    | **CLI** - `claude --worktree <name>`                 |
| A slash command missing from the panel                                    | **CLI** in the integrated terminal (`` Ctrl+` ``)    |

You don't have to choose. Same settings, same CLAUDE.md, same sessions - switch mid-task with `claude --resume` in the
integrated terminal.

______________________________________________________________________

## About the Copilot situation

Since that's what prompted this: the extension covers ordinary inline-assistance work fine, but it's a different shape
of tool - it's agentic (reads files, runs commands, makes multi-file changes) rather than a completions engine. If what
you miss most is as-you-type ghost-text completion, that specific thing isn't what this extension does. For "write this
function", "fix this test", "refactor this module", it's likely to be more capable than Copilot.
