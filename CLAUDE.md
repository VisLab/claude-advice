# ClaudeAdvice - house style

This folder holds the cross-repo Claude Code conventions. It is documentation
about configuration, not a repo, and this file exists so the rules below apply
automatically to any session started here.

## What this folder is

- `00`-`06` numbered documents: the advice, read in order. `README.md` indexes them.
- `templates/`: copy-paste starting points. Named `*.template` on purpose so a
  session started here does not mistake them for live config.
- `repos/`: per-repo reviews plus the applied reference set for
  `hed-metadata-toolkit`, which is the worked example the other repos copy.

## Rules for editing anything in this folder

- **ASCII only, no exceptions.** `-` not em or en dashes, `->` not arrows, `...`
  not an ellipsis character, straight quotes, and `|--` / `` `-- `` for tree
  diagrams rather than box-drawing characters. There is no data in this folder,
  so unlike a repo there is no genuine-data exception. Check before finishing:

  ```bash
  python -c "import pathlib,sys; bad=[(p,c) for p in pathlib.Path('.').rglob('*') if p.is_file() for c in p.read_text(encoding='utf-8',errors='replace') if ord(c)>127]; print(len(bad),'non-ASCII chars'); sys.exit(1 if bad else 0)"
  ```

- **No absolute path or drive letter in anything under `templates/`.** Templates
  are copied into repos and committed; a `H:\` in one of them is the exact bug
  that `04-file-conventions.md` section 2 was written about. Drive letters are
  fine in the numbered documents and in `repos/`, which describe this machine and
  are never committed anywhere.
- **Every factual claim about Claude Code carries its source.** These documents
  are dated and cite `code.claude.com/docs`. If you cannot verify a claim, flag it
  in place rather than smoothing it over.
- **Numbers about Kay's repos come from measuring, not estimating.** The survey
  table in `05-status-directory.md` is real counts; keep it that way, and re-run
  the measurement rather than adjusting a number by hand.
- When a later document overturns an earlier one, add a short block quote at the
  top of the superseded section pointing forward. Do not silently rewrite the old
  document - the reasoning is worth keeping even when the conclusion changed.
- Markdown headers in sentence case.
