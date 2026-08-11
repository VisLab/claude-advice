# Claude Code advice for a multi-repo research workflow

Cross-repo conventions for working with AI coding assistants: what each repository commits, how instructions are wired
so several assistants read one source (`AGENTS.md`), and how working notes stay out of public history (`.status/`,
gitignored). Every factual claim about Claude Code cites `code.claude.com/docs`; each document carries the date its
claims were checked.

## Read in this order

| File                     | What it answers                                                                                                                                            |
| ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `01_repo_standards.md`   | Using Claude Code across repos: the central ideas, what every repository commits, and the `AGENTS.md` / `CLAUDE.md` wiring - with a checklist. Start here. |
| `02_prompt_patterns.md`  | How to frame prompts. The paste-ready examples live in `sample_prompts/`                                                                                   |
| `03_vscode.md`           | The VS Code extension: setup, what it is better at, and what belongs where                                                                                 |
| `04_file_conventions.md` | File naming, `.claude/`, committed versus gitignored, and the cross-tool `AGENTS.md` landscape                                                             |
| `05_status_directory.md` | How `.status/` is organized: the eight-entry layout, naming, and the exit rule for every location                                                          |
| `06_status_migration.md` | How to get an existing `.status/` there - one pass per repo, driven by `templates/status-triage.py`                                                        |
| `CLAUDE.md`              | House style for this folder. Loads automatically in any session started here                                                                               |
| `sample_prompts/`        | Paste-ready prompts, one per file, general enough to adapt anywhere                                                                                        |
| `templates/`             | Copy-paste starting points                                                                                                                                 |

## Templates

`templates/README.md` is the index: one row per template - what it is, where the copy goes, whether the copy is
committed, and which document explains it. Templates are named `NAME.template.EXT` - `template` before the final
extension - so viewers render them as their real type while a session run in this folder does not pick them up as live
config.

## Formatting this repo

```
python -m mdformat --check (Get-ChildItem *.md, sample_prompts\*.md).FullName templates\README.md
```

## Sources

All from the official documentation. First checked 2026-08-03; the memory, setup, and Copilot custom-instructions pages
were re-verified 2026-08-09 and 2026-08-10:

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
- [AGENTS.md](https://agents.md/) and
  [GitHub Copilot repository custom instructions](https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions)
