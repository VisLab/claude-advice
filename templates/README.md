# Templates

Copy-paste starting points, one per target file. The naming pattern is `NAME.template.EXT` - `template` sits before the
final extension so viewers render the file as its real type, while the marker still keeps a session run in this folder
from mistaking it for live config. To use one: copy it to the target path below, drop `.template` from the name, and
fill in the placeholders.

**No absolute path, drive letter, or personal repository name belongs in any template marked "Yes"** - they are
committed into public repositories, and this repository holds itself to the same rule.

| Template                                  | Copy to                                                      | Committed?                    | Explained in             |
| ----------------------------------------- | ------------------------------------------------------------ | ----------------------------- | ------------------------ |
| `AGENTS.template.md`                      | `<repo>/AGENTS.md`                                           | Yes                           | `01_repo_standards.md`   |
| `CLAUDE.template.md`                      | `<repo>/CLAUDE.md`                                           | Yes                           | `01_repo_standards.md`   |
| `copilot-instructions.template.md`        | `<repo>/.github/copilot-instructions.md`                     | Yes                           | `01_repo_standards.md`   |
| `settings.template.json`                  | `<repo>/.claude/settings.json`                               | Yes                           | `01_repo_standards.md`   |
| `vscode-settings.template.json`           | `<repo>/.vscode/settings.json`                               | Yes                           | `01_repo_standards.md`   |
| `gitignore-snippet.txt`                   | append to `<repo>/.gitignore`                                | Yes                           | `01_repo_standards.md`   |
| `status_conduct.rules.template.md`        | `<repo>/.claude/rules/status_conduct.md`                     | Yes                           | `05_status_directory.md` |
| `status_conduct.instructions.template.md` | `<repo>/.github/instructions/status_conduct.instructions.md` | Yes                           | `05_status_directory.md` |
| `skill_example_SKILL.template.md`         | `<repo>/.claude/skills/<name>/SKILL.md`                      | Yes                           | `04_file_conventions.md` |
| `hub_REPOS.template.md`                   | `<hub-repo>/REPOS.md`                                        | Yes                           | its own header comment   |
| `CLAUDE.local.template.md`                | `<repo>/CLAUDE.local.md`                                     | **No** - gitignored           | `04_file_conventions.md` |
| `settings.local.template.json`            | `<repo>/.claude/settings.local.json`                         | **No** - gitignored           | `04_file_conventions.md` |
| `plan_doc.template.md`                    | `<repo>/.status/plans/<slug>.md`                             | No - `.status/` is gitignored | `05_status_directory.md` |
| `status_README.template.md`               | `<repo>/.status/README.md`                                   | No - same reason              | `05_status_directory.md` |
| `status_config.template.md`               | `<repo>/.status/config.md` (optional)                        | No - same reason              | `05_status_directory.md` |
| `status-triage.py`                        | run in place; not copied into repos                          | n/a                           | `06_status_migration.md` |

Two files here are not templates: `status-triage.py` is the migration script `06_status_migration.md` drives, and this
README is the index.
