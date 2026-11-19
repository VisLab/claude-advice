# Triage Copilot review comments on a PR

For the recurring chore after opening a pull request that Copilot (or any bot reviewer) has commented on. The point of the framing: bot comments are suggestions to evaluate, not orders to apply - they pattern-match and are sometimes confidently wrong, so every factual claim gets verified against the actual code or data before it is accepted. Run it from the repository the PR belongs to, on the PR branch.

```
Copilot left review comments on PR <number> of <owner>/<repo>. Evaluate each
one and if you agree fix it; if not, say why. Specifically:

1. Fetch the full comment bodies from the GitHub REST API:
   /repos/<owner>/<repo>/pulls/<number>/comments for the line comments and
   /repos/<owner>/<repo>/pulls/<number>/reviews for the overview. A public
   repository needs no authentication. Do not read the PR's github.com page:
   it renders only where the comments are, and the bodies load by script.
2. Judge each comment on its merits. Verify every factual claim against the
   actual code, data, or format it makes a claim about before agreeing.
3. If you agree, fix it in the local working tree of the PR branch. Do not
   commit or push - I do that.
4. If you disagree, leave the text alone.

End with a brief summary, a line or two per comment: agree or disagree, and
why. No code blocks, no reproduction transcripts, no test output.
```

Use whichever HTTP client works on the machine. Where curl is denied in the assistant's settings, or gh is not authenticated, PowerShell's `Invoke-RestMethod` reaches the API directly; a tool's own web fetcher may fail on `api.github.com`.

If this chore recurs on every PR, stop pasting it: the procedure is true of every project, so it belongs in `~/.claude/CLAUDE.md` - the decision table in section 6 of `04_file_conventions.md` covers where such a rule goes.
