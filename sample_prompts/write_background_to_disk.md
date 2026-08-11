# Write the background to disk

For any project where you keep retyping history at the start of a session. Everything you have explained twice is a
durable fact: give it a file once, and every later prompt shrinks to a pointer. Fill in the bracketed parts before
sending.

```
GOAL: Stop re-explaining project history every session.

THIS TURN: Write two files. No other changes.

1. .status/decisions.md - record these decisions, one dated entry each, with
   consequences:

   - [decision one, stated as a flat fact]
   - [decision two]
   - Consequence: [what stops being maintained, or what becomes the single
     source of truth]
   - Long-term goal: [the durable objective, one sentence]

2. AGENTS.md - add a short "Repository map" section naming each location this
   project depends on and what it owns, one line each - by name, never by
   absolute path.

CONSTRAINTS: Facts and consequences only - no plans, no recommendations. Do
not touch anything under .status/ except creating decisions.md.
```
