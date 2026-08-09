# Claude Code advice for a multi-repo research workflow

Cross-repo conventions for working with AI coding assistants: what each repository commits, how instructions are wired so several assistants read one source (`AGENTS.md`), and how working notes stay out of public history (`.status/`, gitignored). Every factual claim about Claude Code cites `code.claude.com/docs`; each document carries the date its claims were checked.

## Read in this order

| File                     | What it answers                                                                                     |
| ------------------------ | --------------------------------------------------------------------------------------------------- |
| `00-roadmap.md`          | The phased plan: what to do first, second, third. Start here.                                       |
| `01-repo-standards.md`   | What every repository commits, and the `AGENTS.md` / `CLAUDE.md` wiring - with a checklist          |
| `02-prompt-patterns.md`  | How to frame prompts. The paste-ready examples live in `sample_prompts/`                            |
| `03-vscode.md`           | The VS Code extension: setup, what it is better at, and what belongs where                          |
| `04-file-conventions.md` | File naming, `.claude/`, committed versus gitignored, and the cross-tool `AGENTS.md` landscape      |
| `05-status-directory.md` | How `.status/` is organized: the eight-entry layout, naming, and the exit rule for every location   |
| `06-status-migration.md` | How to get an existing `.status/` there - one pass per repo, driven by `templates/status-triage.py` |
| `CLAUDE.md`              | House style for this folder. Loads automatically in any session started here                        |
| `sample_prompts/`        | Paste-ready prompts, one per file, general enough to adapt anywhere                                 |
| `templates/`             | Copy-paste starting points                                                                          |

## Templates

| File                               | Copy to                                        | Commit?                       |
| ---------------------------------- | ---------------------------------------------- | ----------------------------- |
| `AGENTS.md.template`               | `<repo>/AGENTS.md`                             | Yes                           |
| `CLAUDE.md.template`               | `<repo>/CLAUDE.md`                             | Yes                           |
| `copilot-instructions.md.template` | `<repo>/.github/copilot-instructions.md`       | Yes                           |
| `settings.json.template`           | `<repo>/.claude/settings.json`                 | Yes                           |
| `vscode-settings.json.template`    | `<repo>/.vscode/settings.json`                 | Yes                           |
| `gitignore-snippet.txt`            | append to `<repo>/.gitignore`                  | Yes                           |
| `hub-REPOS.md.template`            | `<hub-repo>/REPOS.md`                          | Yes                           |
| `skill-example-SKILL.md`           | `<repo>/.claude/skills/status-update/SKILL.md` | Yes                           |
| `CLAUDE.local.md.template`         | `<repo>/CLAUDE.local.md`                       | **No** - gitignored           |
| `settings.local.json.template`     | `<repo>/.claude/settings.local.json`           | **No** - gitignored           |
| `plan-doc.template.md`             | `<repo>/.status/plans/<slug>.md`               | No - `.status/` is gitignored |
| `status-README.md.template`        | `<repo>/.status/README.md`                     | No - same reason              |
| `status-triage.py`                 | run in place; not copied into repos            | n/a                           |

**No absolute path, drive letter, or personal repository name belongs in any file marked "Yes"** - and this repository holds itself to the same rule. Templates are named `*.template` deliberately, so a session run in this folder does not pick them up as live config.

## Sources

All from the official documentation:

- [Memory and project instructions](https://code.claude.com/docs/en/memory)
- [Best practices](https://code.claude.com/docs/en/best-practices)
- [Monorepos and large repos](https://code.claude.com/docs/en/large-codebases)
- [Common workflows](https://code.claude.com/docs/en/common-workflows)
- [Extend Claude Code](https://code.claude.com/docs/en/features-overview)
- [Skills](https://code.claude.com/docs/en/skills)
- [Settings](https://code.claude.com/docs/en/settings)
- [VS Code extension](https://code.claude.com/docs/en/vs-code)
- [Advanced setup](https://code.claude.com/docs/en/setup)
- [Explore the .claude directory](https://code.claude.com/docs/en/claude-directory)
- [Debug your configuration](https://code.claude.com/docs/en/debug-your-config)
- [AGENTS.md](https://agents.md/) and [GitHub Copilot repository custom instructions](https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions)
