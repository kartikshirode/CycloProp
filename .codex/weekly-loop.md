# Weekly loop config: Codex runner

**This file is not the execution contract.** [`.claude/weekly-loop.md`](../.claude/weekly-loop.md)
is, whichever runner executes the tick. Read that file for paths, gate commands, markers,
checkpoints, blocked triggers and the rules digest, and follow it exactly.

Two configs each claiming to be the contract is how a loop stops being repeatable. Week 2 hit
this: the plan pointed here, the human designated the other file, and the tick ran against
`.claude` while the plan said otherwise. Recorded as D24 and resolved in D28.

## The only thing that differs

```
sentinel_path:  .codex/weekly-loop-sentinel.json
```

A runner needs its own sentinel so a tick that dies under one runner is not mistaken for
partial work by the other. Everything else comes from the Claude config.

## Rules that apply here too, stated because they are easy to assume away

The rules digest in the Claude config is binding on a Codex week-agent as well. In particular
the two that week 2 found were missing from this file:

- **Invoke the `humanizer` skill before writing prose to any file.** It owns tone and the
  AI-detection patterns, and the `--global` gate enforces the punctuation part
- **Invoke the `git-commits` skill for the commit procedure.** Staging safety, splitting by
  concern, message style, and the hard bans on push, amend, branch, tag and history rewriting

If a rule in this file ever appears to contradict the Claude config, the Claude config wins
and this file is the thing to fix.
