# ClaudeAdvice - house style

This repository holds the cross-repo conventions for AI-assisted work. It is documentation about configuration, and this file exists so the rules below apply automatically to any session started here.

## What this repository is

- `01`-`06` numbered documents: the advice, read in order. `README.md` indexes them. (There is no `00`: the personal adoption roadmap moved to the toolkit repo's `.status/plans/`, because working plans about specific repos do not belong in shared advice.)
- `sample_prompts/`: paste-ready prompts, one per file - illustrative and general, tracked as content.
- `templates/`: copy-paste starting points, indexed in `templates/README.md`. Named `NAME.template.EXT` - `template` before the final extension - so viewers render them as their real type while a session started here does not mistake them for live config.
- `.status/` (gitignored): working state. Read `.status/README.md` first. **`.status/decisions.md` is the authority: if an advice file contradicts it, the file is wrong.**

## Rules for editing anything in this folder

- **ASCII only, no exceptions.** `-` not em or en dashes, `->` not arrows, `...` not an ellipsis character, straight quotes, and `|--` / `` `-- `` for tree diagrams rather than box-drawing characters. There is no data in this folder, so unlike a repo there is no genuine-data exception. Check before finishing:

  ```bash
  python -c "import pathlib,sys; bad=[(p,c) for p in pathlib.Path('.').rglob('*') if p.is_file() for c in p.read_text(encoding='utf-8',errors='replace') if ord(c)>127]; print(len(bad),'non-ASCII chars'); sys.exit(1 if bad else 0)"
  ```

- **No absolute path or drive letter in any committed file.** This repository is public and is subject to the same rule it imposes on other repos. Machine paths still present in the numbered documents are a known cleanup tracked in `.status/plans/`; do not add new ones.

- **No personal repository names in the advice or templates.** The advice stands alone; a reference set may be read while writing, but the committed text never names it.

- **Markdown filenames use `_` as the separator, never `-`** (`01_repo_standards.md`, not `01-repo-standards.md`). Fixed external names are the exception: `.github/copilot-instructions.md` is GitHub's filename and keeps its hyphens.

- **Both Windows and Linux are first-class.** The advice serves machines of both kinds. Write user-level paths as `~/.claude/...` and give the Windows form (`%USERPROFILE%\.claude\...`) where it matters; when a command differs between PowerShell and bash, show both; a command identical in both shells gets one unlabeled block. Scope genuinely platform-specific facts explicitly ("on Windows, ...").

- **Every factual claim about Claude Code carries its source.** These documents cite `code.claude.com/docs` and state the date the claim was checked. If you cannot verify a claim, flag it in place rather than smoothing it over.

- **Numbers come from measuring, not estimating.** Any count quoted in an advice file (like the `.status/` survey figures in `05_status_directory.md`) must trace to a real measurement; re-run the measurement rather than adjusting a number by hand. The measured survey itself lives with the working notes, not in a committed file.

- When a later document overturns an earlier one, add a short block quote at the top of the superseded section pointing forward. Do not silently rewrite the old document - the reasoning is worth keeping even when the conclusion changed.

- Markdown formatting is `mdformat`, with the settings in `.mdformat.toml`. Run `python -m mdformat --check *.md sample_prompts/*.md` before finishing. Do not pass anything under `templates/` to it except `templates/README.md`: the JSON templates are not markdown, and the markdown templates carry frontmatter and placeholders that mdformat would mangle. Markdown headers in sentence case.
