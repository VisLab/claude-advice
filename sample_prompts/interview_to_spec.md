# Interview to a spec

For when the goal is still fuzzy - the tell is your own prompt trailing off or admitting the problem is complicated.
Invert the questioning: have the assistant interview you, then write the answers down as a spec. Run it in plan mode;
when the spec exists, /clear and execute against it in a fresh session.

```
I want to build [one-sentence statement of the durable goal].

Read .status/decisions.md and [the directory or file holding the existing
work] first.

Then interview me in detail using the AskUserQuestion tool. Ask about the
data model, what the core terms have to mean formally, how the pieces bind
together, edge cases, and the tradeoffs I have not considered. Don't ask
obvious questions - dig into the hard parts.

Keep interviewing until we've covered everything, then write a complete spec
to .status/plans/[slug]-spec.md.
```
