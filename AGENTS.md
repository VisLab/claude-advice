# claude-advice

Purpose: the cross-repo conventions for AI-assisted work - documentation about configuration. This file is the instruction set for every assistant working in this folder: `CLAUDE.md` imports it, and `.github/copilot-instructions.md` points at it.

Not in scope: per-repo reviews and working plans about specific repositories. The advice stands alone; a reference set may be read while writing, but the committed text never names it.

## Commands

Test framework: none - documentation repository, no test suite.

Markdown formatting is `mdformat`, with the settings in `.mdformat.toml` (`wrap = "no"` - paragraphs are single lines, the convention across the HED repositories). It is installed in the system Python - no venv, and always `python -m mdformat`, since the bare `mdformat` command is not on PATH. Check before finishing (drop `--check` to fix):

```bash
# bash - the shell expands the globs
python -m mdformat --check *.md sample_prompts/*.md .github/*.md .github/instructions/*.md .claude/rules/*.md templates/README.md
```

```powershell
# PowerShell - globs must be expanded by Get-ChildItem, not the command line
python -m mdformat --check (Get-ChildItem *.md, sample_prompts\*.md, .github\*.md, .github\instructions\*.md, .claude\rules\*.md).FullName templates\README.md
```

Do not pass anything under `templates/` to it except `templates/README.md`: the JSON templates are not markdown, and the markdown templates carry frontmatter and placeholders that mdformat would mangle.

ASCII check, run over the tracked files before finishing (must print `0 non-ASCII chars` and exit 0):

```bash
git ls-files -z | python -c "import pathlib,sys; files=sys.stdin.buffer.read().decode().split('\0'); bad=[(f,c) for f in files if f and pathlib.Path(f).is_file() for c in pathlib.Path(f).read_text(encoding='utf-8',errors='replace') if ord(c)>127]; print(len(bad),'non-ASCII chars'); sys.exit(1 if bad else 0)"
```

## Layout

- `01`-`06` numbered documents: the advice, read in order. `README.md` indexes them.
- `sample_prompts/` - paste-ready prompts, one per file: illustrative and general, tracked as content.
- `templates/` - copy-paste starting points, indexed in `templates/README.md`. Named `NAME.template.EXT` - `template` before the final extension - so viewers render them as their real type while a session started here does not mistake them for live config.
- `.status/` - working notes. Gitignored; local to each machine.

## Rules for editing anything in this folder

- **ASCII only, no exceptions.** `-` not em or en dashes, `->` not arrows, `...` not an ellipsis character, straight quotes, and `|--` / `` `-- `` for tree diagrams rather than box-drawing characters. There is no data in this folder, so unlike a repo there is no genuine-data exception.
- **No absolute path or drive letter in any committed file.** This repository is public and is subject to the same rule it imposes on other repos.
- **No personal repository names in the advice or templates.**
- **Markdown filenames use `_` as the separator, never `-`** (`01_repo_standards.md`, not `01-repo-standards.md`). Fixed external names are the exception: `.github/copilot-instructions.md` is GitHub's filename and keeps its hyphens.
- Markdown headers in sentence case: capitalize the first word, proper nouns, and acronyms only.
- **Both Windows and Linux are first-class.** The advice serves machines of both kinds. Write user-level paths as `~/.claude/...` and give the Windows form (`%USERPROFILE%\.claude\...`) where it matters; when a command differs between PowerShell and bash, show both; a command identical in both shells gets one unlabeled block. Scope genuinely platform-specific facts explicitly ("on Windows, ...").
- **Every factual claim about Claude Code carries its source.** These documents cite `code.claude.com/docs` and state the date the claim was checked. If you cannot verify a claim, flag it in place rather than smoothing it over.
- **Numbers come from measuring, not estimating.** Any count quoted in an advice file must trace to a real measurement; re-run the measurement rather than adjusting a number by hand. The measured survey itself lives with the working notes, not in a committed file.
- When a later document overturns an earlier one, add a short block quote at the top of the superseded section pointing forward. Do not silently rewrite the old document - the reasoning is worth keeping even when the conclusion changed.

## Where the thinking lives

`.status/` is gitignored, so it exists only on this machine and never in a fresh clone or worktree. Read `.status/README.md` first; it is the index and lists what is active.

- `.status/decisions.md` - **the authority: if an advice file contradicts it, the file is wrong.** Read before proposing structural changes. Append entries; never rewrite one.
- `.status/plans/*.md` - active plans. Check the `Status:` header and the `[ ]` / `[x]` markers before starting work.
- IMPORTANT: do not read `.status/archive/` unless a file is named for you. Nothing new is created at the `.status/` root.

## Working agreements

- IMPORTANT: every file written to `.status/` opens with a `For humans:` summary - three or four sentences at the very top: what the file is and what a person needs to take from it. The same applies to a long answer in a session: lead with the conclusion.
- IMPORTANT: temporary scripts, experiments, and one-off test files go in `.status/scratch/` - never the repository root. Anything in `scratch/` may be deleted unread.
- IMPORTANT: never delete, move, or rewrite a file under `.status/` without asking first. Appending is fine.
- For a change spanning more than three files, write a plan to `.status/plans/` and stop for review before editing.
- When you are guessing about an external API or data format, say so explicitly.
- Show evidence, not assertions: the command you ran and its actual output.
- Do not commit, push, or create branches unless asked.
