<!--
  Copy to .status/plans/<slug>.md   (see 05-status-directory.md)

  No date and no "-plan" suffix in the filename: it lives in plans/, so the kind
  is already known, and its creation date stops being interesting on day two.
  When it finishes, MOVE it to .status/archive/<year>/ - never rename it to
  <slug>_complete.md.

  Why a file and not chat: long sessions compact their context and lose detail.
  A file on disk survives compaction, /clear, and next week.
-->

# <Initiative name>

**For humans:** <what this achieves, what state it is in, and what happens next.
Three sentences, before the header block below. If you cannot write it, the plan
is not clear enough yet.>

- **Status**: DRAFT | ACTIVE | BLOCKED | DONE | SUPERSEDED
- **Created**: YYYY-MM-DD
- **Last reconciled with disk**: YYYY-MM-DD
- **Supersedes**: <path to older plan, or none>
- **Related decisions**: `.status/decisions.md` section <heading>

## Goal

One paragraph. What is true when this is finished that isn't true now.

## Non-goals

Explicit. This section prevents scope creep more effectively than anything else
in the document.

- <thing that is obviously adjacent but out of scope>
- <thing a previous plan covers instead>

## Open questions

Things that must be answered before or during the work. Mark them resolved
in place rather than deleting them - the resolution is the valuable part.

- [ ] <question> -> <resolution once known>

---

## Phase 1 - <name>

**Done when**: <observable condition - a count, a passing check, a file existing>
**Verify with**: `<exact command or check>`

- [ ] TODO <step>
      Files: `<path>`, `<path>`
      Notes: <anything Claude would otherwise guess wrong>
- [ ] TODO <step>

## Phase 2 - <name>

**Done when**: <...>
**Verify with**: `<...>`

- [ ] TODO <step>

## Phase 3 - <name>

**Done when**: <...>
**Verify with**: `<...>`

- [ ] TODO <step>

---

## Assumptions and risks

Where the plan is guessing. Be specific - this is the section that saves you
when a phase fails.

- ASSUMPTION: <e.g. nemar exposes a per-dataset citation endpoint>.
  If false: <what changes>.
- RISK: <e.g. mirroring every dataset repo exceeds available disk>.
  Mitigation: <...>.

## Log

Append as work happens. One line each; date them.

- YYYY-MM-DD - <what happened, what changed about the plan>
