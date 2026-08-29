# Weekly loop config: CycloProp Stage 1

Status: draft for one-time human confirmation before the first `/loop` run.

This file is the Codex weekly-loop config for one Stage 1 plan week per tick. The loop
supervisor runs the gates in its own shell and stops for a human read after every week.

## Paths

```text
repo_path:      C:/Users/Kartik/Documents/Kartik/EDU/Local/Projects/Techfest/PUSHPAK-Grand-Challenge/CycloProp
plan_file:      stage-1/plan.md
handoff_file:   handoff.md
context_file:   context.md
progress_dir:   stage-1/progress
progress_file:  stage-1/progress/week-{N}.md
audit_dir:      stage-1/audit
audit_file:     stage-1/audit/week-{N}.md
decisions_file: stage-1/decisions.md
journal_file:   stage-1/journal.md
numbers_file:   stage-1/design/numbers.json
sentinel_path:  .codex/weekly-loop-sentinel.json
```

The sentinel is ignored by git. If it exists, the next tick uses recovery mode instead of
starting the week again.

## Gate commands

```text
python tools/check.py --week {N}
python tools/check.py --global
```

Run both commands after the week-agent finishes, even when the first one fails. The
supervisor also checks for a clean tree, commits since the tick start, scope overlap and
the progress, audit and handoff markers.

## Markers

```text
done_marker:      STATUS: WEEK-COMPLETE
audit_marker:     AUDIT-COMPLETE
next_week_marker: NEXT-WEEK: {N_plus_1}
```

## Checkpoints

```text
checkpoint_every: 1
human_gate_advisory_before_week: 2
human_gate_required_before_week: 5
```

Week H stays advisory before week 2 and is a hard block before week 5. A person, never an
agent, adds the four confirmed markers in `stage-1/human-gate.md`.

## Work and audit rules

- Execute one plan week only. Treat the plan's work packages as checkpoints inside that
  week, not as extra loop ticks
- Read `handoff.md`, the current plan week, the current codemap entries, the last progress
  file and recent decisions before editing
- Parallel read-only work is allowed. Parallel repo writes need separate git worktrees.
  Prefer sequential writes when the isolation cost is larger than the saved time
- Run the independent read-only audit required by the weekly-loop skill. Write its return
  verbatim to the week's audit file, then fix the findings or record them as debt
- `stage-1/design/numbers.json` is the only definition point for submission numbers. Prose
  declares the dotted keys it uses in a `## Numbers used` section
- Hard limits use recomputed thrust, mass and T/W. A stored headline cannot override them
- Week 2 geometry freezes only when the conservative thrust and mass case clears both hard
  targets. A legal but low-margin result remains a review finding
- Week 4 derives blade mass, shaft torque, blade root bending and centrifugal load from the
  design. Every refined mass line points to its week 2 envelope line
- No CAD at Stage 1. Use dimensioned sketches and interface tables for integration work
- Follow the repository `AGENTS.md` instructions for prose, commits and attribution. Do not
  depend on a separate humanizer or git-commit skill
- Commit small logical changes. Never push, amend, force, branch, tag or open a PR

## Blocked triggers

Stop and return exact unblock steps when any of these occurs:

- Sending mail to the organisers, registering a team or entering personal details
- Inventing real names, institutions, capability claims or tool access
- The conservative week 2 case still misses a hard target after the written fallbacks
- The week 4 mass budget still misses after the prequalified fallbacks
- A source or resource marked as a hard dependency is unavailable
- Human gate markers are missing when week 5 starts
- `TECHNICAL-READ-COMPLETE` is missing before final email staging

The three unread papers are supporting evidence unless the plan explicitly promotes one to
a hard dependency. Missing support must be disclosed in the design notes and handoff.

## Week-specific checks to remember

Week 2 includes the momentum floor, a published power-loading route, three or more thrust
sensitivity rows, the solidity band and a stiffness-linked low thrust coefficient. Week 3
must derive the pitch schedule from a real linkage solution and quantify vectoring. Week 4
must close the structural load path and mass budget. Week 5 builds and reads back the actual
submission PDF, then stages an email draft for a person to send.
