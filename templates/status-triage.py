#!/usr/bin/env python3
"""status-triage.py - propose a .status/ reorganization without performing it.

Companion to 06_status_migration.md. Classifies every file in a repo's .status/
directory by rule and writes a reviewable plan. It NEVER deletes anything, and
it does nothing at all unless you pass --apply.

Usage:
    python status-triage.py <repo-root>                  # dry run, writes a plan
    python status-triage.py <repo-root> --plan out.tsv   # plan somewhere specific
    python status-triage.py <repo-root> --apply          # execute a plan you read

Why "never delete": .status/ is gitignored in every one of these repos, so a
wrong move has no `git checkout` to undo it. Noise and non-markdown go to
scratch/ instead, flattened, where the developer has them cleaned out
after living without them for a week. archive/<year>/ is flat and markdown only.

Stdlib only, ASCII only, works on Windows and POSIX.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import re
import shutil
import sys
from pathlib import Path

# --------------------------------------------------------------------------
# Classification rules. Order matters: first match wins.
# --------------------------------------------------------------------------

# Retention defaults. A repo overrides them with `key: days` lines in
# .status/config.md (see 05_status_directory.md); only stale_days is used here.
RETENTION_DEFAULTS = {"plan_days": 60, "stale_days": 90}

# Files that are noise no matter what they contain.
JUNK_SUFFIXES = {".log", ".bak", ".backup", ".tmp", ".orig", ".swp", ".pyc"}
JUNK_NAME_BITS = (" copy", ".md copy", "~")

# Root filenames that are part of the target layout and stay put.
KEEP_AT_ROOT = {"README.md", "decisions.md", "development_history.md", "local-environment.md", "config.md"}

# Markdown whose name advertises that the work is over.
DONE_NAME_RE = re.compile(
    r"(complete|completion|final|summary|report|progress|assessment|_old|deprecated)",
    re.IGNORECASE,
)

# Directory names that are junk drawers by another name. Matched case-insensitively
# against the first path component under .status/.
VAGUE_DIR_RE = re.compile(
    r"^(temp|tmp|.*temp|working.*|original.*|old.*|leftovers|unused|removed|"
    r"review_for_deletion|merged|unmerged|backup|chat.*|test_.*|"
    r".*_test|scripts|config|data|instructions|fixes|issues|prs|features|"
    r"migration|release_notes|schemas.*|search|helpers|documentation)$",
    re.IGNORECASE,
)

# A date anywhere in the filename, in any of the forms actually in use.
DATE_RE = re.compile(r"(20\d{2})[-_]?(\d{2})[-_]?(\d{2})")

# Names that declare what kind of document this is. Checked before the date rule.
PLAN_NAME_RE = re.compile(r"(^plan[_-]+|[_-]+plan$|^design[_-]+|[_-]+roadmap$)", re.IGNORECASE)
DECISION_NAME_RE = re.compile(r"(^decisions?[_-]+|[_-]+decisions?$)", re.IGNORECASE)

MARKDOWN = {".md", ".markdown"}


def load_retention(status: Path) -> dict:
    """Per-repo retention from .status/config.md; defaults for anything unset."""
    cfg = dict(RETENTION_DEFAULTS)
    config = status / "config.md"
    if config.is_file():
        for m in re.finditer(r"^(plan_days|stale_days)\s*[:=]\s*(\d+)\s*$",
                             config.read_text(encoding="utf-8"), re.MULTILINE):
            cfg[m.group(1)] = int(m.group(2))
    return cfg


def flat(parts: tuple[str, ...]) -> str:
    """One filename from a path: old directories become a prefix, not a folder.

    archive/<year>/ and scratch/ are flat - copying a junk drawer's folders
    into them is how one repo ended up with 52 subdirectories in its archive.
    """
    return "_".join(parts)


def plan_name(stem: str, full: Path, folder: str = "plans") -> str:
    """<folder>/YYYY-MM-DD_<slug>.md: the date in the old name, else the file's mtime."""
    m = DATE_RE.search(full.name)
    if m:
        date = f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
    else:
        date = dt.date.fromtimestamp(full.stat().st_mtime).isoformat()
    return f"{folder}/{date}_{stem}.md"


LEADING_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}_")


def classify(rel: Path, full: Path, today: dt.date, stale_days: int) -> tuple[str, str, str]:
    """Return (action, destination_relative_to_status, reason).

    action is one of: keep, rename, plan, note, archive, quarantine, review
    """
    year = str(today.year)
    name = rel.name
    parts = rel.parts
    is_md = full.suffix.lower() in MARKDOWN

    # 1. Anything inside a subdirectory that is already a junk drawer: do not
    #    look inside. Markdown is archived and non-markdown goes to scratch/,
    #    both flattened - the old folder names become a filename prefix.
    if len(parts) > 1 and VAGUE_DIR_RE.match(parts[0]):
        dest = f"archive/{year}/{flat(parts)}" if is_md else f"scratch/{flat(parts)}"
        return ("archive" if is_md else "quarantine", dest,
                f"inside junk-drawer directory '{parts[0]}/'")

    # 2. Obvious noise -> scratch/, except what is already under scratch/.
    if parts[0] != "scratch" and (
            full.suffix.lower() in JUNK_SUFFIXES or any(b in name for b in JUNK_NAME_BITS)):
        return ("quarantine", f"scratch/{flat(parts)}",
                f"noise ({full.suffix or 'name pattern'})")

    # 3. The fixed root files that belong to the target layout.
    if len(parts) == 1 and name in KEEP_AT_ROOT:
        return ("keep", str(rel).replace("\\", "/"), "part of the target layout")

    # 4. Already-correct locations are left alone - except a plan, prompt, or
    #    note directly in its folder without a leading date, which is renamed
    #    in place. The archive keeps its names, including old archived_ ones.
    if (len(parts) == 2 and parts[0] in ("plans", "prompts", "notes") and is_md
            and not LEADING_DATE_RE.match(name)):
        stem = DATE_RE.sub("", full.stem)
        stem = re.sub(r"[^A-Za-z0-9]+", "_", stem).strip("_").lower() or parts[0].rstrip("s")
        return ("rename", plan_name(stem, full, parts[0]),
                f"in {parts[0]}/ without a leading date - CONFIRM the date "
                f"(the day it was opened, or the day a note records)")
    if len(parts) > 1 and parts[0] in ("archive", "scratch", "plans", "prompts", "notes"):
        return ("keep", str(rel).replace("\\", "/"), "already in the target layout")

    # 5. Non-markdown needs a human: it either has a real home in the repo or it
    #    is throwaway. The script will not guess between src/, scripts/, and
    #    tests/. It never goes to archive/, which is markdown only.
    if not is_md:
        return ("review", f"scratch/{flat(parts)}",
                f"non-markdown ({full.suffix or 'no suffix'}): move to a real home "
                f"in the repo, or accept scratch/")

    age = (today - dt.date.fromtimestamp(full.stat().st_mtime)).days

    # 6. A name that says "decision" is checked FIRST, ahead of staleness: a
    #    five-month-old decision record is precisely what you want harvested into
    #    decisions.md, and archiving it unread is how the rationale gets lost.
    if DECISION_NAME_RE.search(full.stem):
        m = DATE_RE.search(name)
        date = f"{m.group(1)}-{m.group(2)}-{m.group(3)}" if m else "undated"
        stem = re.sub(r"[^A-Za-z0-9]+", "_",
                      DECISION_NAME_RE.sub("", DATE_RE.sub("", full.stem))
                      ).strip("_").lower() or "decision"
        return ("harvest", f"notes/{date}_{stem}.md",
                f"decision record ({age}d): copy its substance into decisions.md, "
                f"then file it")

    # 7. Markdown named after its own completion state.
    if DONE_NAME_RE.search(name):
        return ("archive", f"archive/{year}/{flat(parts)}",
                "filename advertises the work is finished")

    # 8. Stale markdown. A plan that has not been touched in this long is not
    #    active work, whatever it is called, so this precedes the plan rule.
    if age > stale_days:
        return ("archive", f"archive/{year}/{flat(parts)}", f"untouched for {age} days")

    # 9. A name that says "plan" is a plan even when it carries a date. This has
    #    to come before the date rule, or every plan_<date>_<slug>.md lands in
    #    notes/ - which is exactly what the first version of this script did.
    if PLAN_NAME_RE.search(full.stem):
        stem = PLAN_NAME_RE.sub("", full.stem)
        stem = DATE_RE.sub("", stem)
        stem = re.sub(r"[^A-Za-z0-9]+", "_", stem).strip("_").lower() or "plan"
        return ("plan", plan_name(stem, full),
                f"recent ({age}d) and named as a plan - CONFIRM it is still active")

    # 10. Recent markdown carrying a date is a dated record -> notes/, date first.
    m = DATE_RE.search(name)
    if m:
        stem = DATE_RE.sub("", full.stem).strip("_-. ")
        stem = re.sub(r"^(session|note|log|analysis|report)[_-]+", "", stem, flags=re.I)
        stem = re.sub(r"[^A-Za-z0-9]+", "_", stem).strip("_").lower() or "note"
        return ("note", f"notes/{m.group(1)}-{m.group(2)}-{m.group(3)}_{stem}.md",
                f"recent ({age}d) and dated: a record of a day")

    # 11. What is left is recent, undated, and unlabelled: candidate active work.
    stem = re.sub(r"[^A-Za-z0-9]+", "_", full.stem).strip("_").lower()
    return ("plan", plan_name(stem, full),
            f"recent ({age}d), undated: candidate active plan - CONFIRM by reading "
            f"and correct the date to the day it was opened")


def build_plan(status: Path, today: dt.date) -> list[dict]:
    stale_days = load_retention(status)["stale_days"]
    rows = []
    for full in sorted(status.rglob("*")):
        if not full.is_file():
            continue
        rel = full.relative_to(status)
        action, dest, reason = classify(rel, full, today, stale_days)
        rows.append({
            "action": action,
            "source": str(rel).replace("\\", "/"),
            "destination": dest,
            "kb": f"{full.stat().st_size / 1024:.0f}",
            "modified": dt.date.fromtimestamp(full.stat().st_mtime).isoformat(),
            "reason": reason,
        })
    return rows


def apply_plan(status: Path, rows: list[dict]) -> tuple[int, int]:
    moved = skipped = 0
    for r in rows:
        if r["action"] == "keep":
            skipped += 1
            continue
        src = status / r["source"]
        dst = status / r["destination"]
        if not src.exists():
            print(f"  MISSING, skipped: {r['source']}")
            skipped += 1
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        final = dst
        n = 2
        while final.exists():                      # never overwrite
            final = dst.with_name(f"{dst.stem}_{n}{dst.suffix}")
            n += 1
        shutil.move(str(src), str(final))
        moved += 1
    # remove directories left empty by the moves
    for d in sorted((p for p in status.rglob("*") if p.is_dir()),
                    key=lambda p: -len(p.parts)):
        try:
            next(d.iterdir())
        except StopIteration:
            d.rmdir()
    return moved, skipped


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("repo", type=Path, help="repository root (the dir containing .status)")
    ap.add_argument("--plan", type=Path, default=None,
                    help="where to write the plan (default: <repo>/../status-plan-<repo>.tsv)")
    ap.add_argument("--apply", action="store_true",
                    help="execute the plan. Read it first. Snapshot .status/ first.")
    ap.add_argument("--today", default=None, help="override today's date (YYYY-MM-DD)")
    args = ap.parse_args()

    status = args.repo / ".status"
    if not status.is_dir():
        print(f"No .status/ directory in {args.repo}")
        return 1

    today = dt.date.fromisoformat(args.today) if args.today else dt.date.today()
    rows = build_plan(status, today)
    if not rows:
        print(".status/ is empty. Nothing to do.")
        return 0

    plan_path = args.plan or args.repo.parent / f"status-plan-{args.repo.name}.tsv"
    with open(plan_path, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]), delimiter="\t",
                           lineterminator="\n")
        w.writeheader()
        w.writerows(rows)

    counts: dict[str, int] = {}
    for r in rows:
        counts[r["action"]] = counts.get(r["action"], 0) + 1
    order = ["keep", "rename", "plan", "harvest", "note", "archive", "review", "quarantine"]
    blurb = {
        "keep": "already correct, untouched",
        "rename": "in plans/, prompts/, or notes/ without a leading date - CONFIRM the date",
        "plan": "candidate ACTIVE work - read these, they are the whole point",
        "harvest": "decision records - copy their substance into decisions.md",
        "note": "dated record -> notes/, renamed date-first",
        "archive": "finished or stale -> archive/<year>/ (flat)",
        "review": "non-markdown - YOUR CALL: a real home in the repo, or scratch/",
        "quarantine": "noise and junk-drawer non-markdown -> scratch/",
    }
    print(f"\n{len(rows)} files under {status}\n")
    for a in order:
        if a in counts:
            print(f"  {counts[a]:5d}  {a:<11} {blurb[a]}")
    print(f"\nPlan written to: {plan_path}")

    if not args.apply:
        print("\nDry run. Nothing was moved. Next:")
        print("  1. Open the plan and fix the 'destination' column where it is wrong.")
        print("  2. Snapshot .status/ to a zip OUTSIDE the repo - it is not in git.")
        print("  3. Re-run with --apply.")
        return 0

    print("\n--apply given. Moving files (nothing is deleted)...")
    moved, skipped = apply_plan(status, rows)
    print(f"\nMoved {moved}, left in place {skipped}.")
    print("Now do the parts no script can: harvest decisions.md, write README.md")
    print("with its Next list, and confirm each file in plans/.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
