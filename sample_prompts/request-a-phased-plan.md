# Request a phased plan

The six-slot template from `02-prompt-patterns.md`, applied to asking for a plan document: one deliverable at a known path, phases inside it, and one verification per phase so "done" is checkable rather than felt.

```
GOAL: [the durable objective, one sentence].

THIS TURN: One plan document. No code, no file changes outside .status/.

WHERE:
  @.status/decisions.md
  [@ any other file the plan must respect]
  [a directory to survey - "survey it and tell me what is there before
  relying on it"]

GIVEN: [decisions already made, as flat facts. No narrative.]

DELIVERABLE: .status/plans/[slug].md with exactly [N] phases:
  Phase 1 - [outcome]
  Phase 2 - [outcome - e.g. "list every file and call site that would need
            to change; do not change them"]
  Phase 3 - [outcome]

For each phase: concrete steps, files touched, open questions, and one
verification I can run to confirm the phase is done. Mark every step
[ ] TODO.

CONSTRAINTS: [what this plan must not design or touch]. Where you are
guessing about an external API or data shape, say so explicitly rather than
assuming.
```
