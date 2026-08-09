# Claude Code advice for a multi-repo research workflow

Written 2026-08-03 for Kay. Every factual claim was checked against `code.claude.com/docs` on that date; anything I couldn't verify is flagged in place rather than smoothed over.

## Read in this order

| File                     | What it answers                                                                                                                                                                                         |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `00-roadmap.md`          | The phased plan: what to do first, second, third. Start here.                                                                                                                                           |
| `01-repo-standards.md`   | "What should be in each repository?" - with a checklist                                                                                                                                                 |
| `02-prompt-patterns.md`  | "How should I frame my prompts?" - includes a rewrite of the prompt you sent me                                                                                                                         |
| `03-vscode.md`           | Extension setup, what it's better at, and why last time probably failed                                                                                                                                 |
| `04-file-conventions.md` | `CLAUDE.md` vs `Claude.md`, what's in `.claude/`, committed vs gitignored, and whether `.rules` / `.context` / `AGENTS.md` are real conventions                                                         |
| `05-status-directory.md` | **How `.status/` should be organized** - the target. Written 2026-08-04 from a survey of all 25 of your actual `.status/` directories (2,229 files, 185 MB): layout, naming scheme, and retention rules |
| `06-status-migration.md` | **How to get an existing `.status/` there** - the procedure, one pass per repo, driven by `templates/status-triage.py`                                                                                  |
| `CLAUDE.md`              | House style for this folder. Loads automatically in any session started here                                                                                                                            |
| `repos/`                 | Per-repo reviews and the applied reference set for `hed-metadata-toolkit`                                                                                                                               |
| `templates/`             | Copy-paste starting points                                                                                                                                                                              |

## Templates

| File                           | Copy to                                        | Commit?                                                  |
| ------------------------------ | ---------------------------------------------- | -------------------------------------------------------- |
| `CLAUDE.md.template`           | `<repo>/CLAUDE.md`                             | Yes                                                      |
| `CLAUDE.local.md.template`     | `<repo>/CLAUDE.local.md`                       | **No**                                                   |
| `settings.json.template`       | `<repo>/.claude/settings.json`                 | Yes                                                      |
| `settings.local.json.template` | `<repo>/.claude/settings.local.json`           | **No**                                                   |
| `hub-REPOS.md.template`        | `<hub-repo>/REPOS.md`                          | Yes                                                      |
| `plan-doc.template.md`         | `<repo>/.status/plans/<slug>.md`               | No - `.status/` is gitignored in every one of your repos |
| `status-README.md.template`    | `<repo>/.status/README.md`                     | No - same reason                                         |
| `status-triage.py`             | run in place; not copied into repos            | n/a                                                      |
| `skill-example-SKILL.md`       | `<repo>/.claude/skills/status-update/SKILL.md` | Yes                                                      |
| `gitignore-snippet.txt`        | append to `<repo>/.gitignore`                  | Yes                                                      |

**No absolute path or drive letter belongs in any file marked "Yes".** That was a real bug in the first version of these templates; `04-file-conventions.md` section 2 explains the split and `gitignore-snippet.txt` includes a grep to catch leaks.

Templates are named `.template` deliberately so that if you ever run Claude in this folder, they aren't picked up as live config.

## The 90-second version

1. **Context is the scarce resource.** Every recommendation follows from that.
2. **Durable facts go in files, not prompts.** A `CLAUDE.md` per repo, plus `.status/decisions.md` for the "why". You are currently retyping several paragraphs of project history every session; write it down once.
3. **Directory access is configuration, not a request.** "Add to your trusted folders" in a prompt does nothing. Use `--add-dir`, `/add-dir`, or `permissions.additionalDirectories` in `.claude/settings.local.json`.
4. **Committed files must be portable.** `CLAUDE.md` and `.claude/settings.json` are shared; drive letters and checkout paths go in `CLAUDE.local.md` and `.claude/settings.local.json`, both gitignored.
5. **Where you launch `claude` decides what loads.** Launch from the narrowest directory containing the work.
6. **One deliverable per prompt.** Three plans is three prompts.
7. **Plan mode -> plan on disk -> `/clear` -> execute -> verify.** The `/clear` is the step everyone skips and the one that most improves results.
8. **When the goal is fuzzy, have Claude interview you** and write a `SPEC.md`. Given where your task-modeling work is, this is the highest-value single thing in this folder.
9. **Give Claude something that returns pass/fail.** Without a check, you are the verification loop.

## Two things to double-check in your own setup

- You wrote both `I:\Repos\hed-task` and `H:\Repos\hed-task` in the same prompt. A wrong drive letter fails silently and looks like Claude ignoring you.
- Confirm which of your five locations are real git repos versus plain working folders. It changes what worktrees, checkpoints, and per-repo memory can do.

## If you want this tailored

I wrote these as templates with your paths as examples, because the repos themselves weren't reachable from this session. If you connect `H:\Research\task-research`, `H:\Repos\hed-task`, `H:\Repos\hed-metadata-toolkit`, and `I:\RepositoryMetadata\nemar-metadata` via **Add folder** in the desktop app, I can read them and write real drafts of each `CLAUDE.md`, `REPOS.md`, and the first plan document instead of skeletons.

## Sources

All from the official documentation, fetched 2026-08-03:

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
- [AGENTS.md](https://agents.md/) (for the cross-tool comparison in `04-file-conventions.md`)
