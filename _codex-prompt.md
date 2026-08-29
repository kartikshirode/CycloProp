# Codex review prompt: can this plan actually be executed

Paste everything below the line into a **fresh Codex session** with the repository available.
Replaces the earlier prompt, which was aimed at finding holes in the gates. That job is done.

---

You are reviewing an execution plan for a national engineering design competition. The
deadline is 27 September 2026 and today is 29 August, so there are 28 days and no slack.

**Start with `_codex-context.md`.** It is self-contained and holds the competition
requirements, the project state, the central engineering problem and the fourteen frozen
decisions. Everything the official website would tell you is already in the repository under
`reference/`. Do not spend time fetching anything.

Then read, in this order:

1. `stage-1/plan.md`, the plan under review
2. `tools/check.py`, the mechanical gates that decide whether a week passed
3. `stage-1/literature.md`, the technical evidence the plan rests on
4. `stage-1/decisions.md`, the fourteen decisions

## The question this round has to answer

Previous rounds asked whether the gates could be fooled. They were mined hard across four
rounds and every finding is closed, so **do not spend this round hunting gate holes.** If you
find one, report it, but it is not the job.

The question now is different and has never been reviewed:

> **Can an agent execute this plan and produce a Stage 1 submission an IIT Bombay evaluator
> would believe?**

Concretely, judge these:

**1. Executability.** Take week 2, the heaviest week, and walk it as if you were the agent
doing it. Does the plan tell you enough to actually produce the numbers? Where would you be
guessing? Where would you stop and ask a human? The plan breaks each week into subsessions;
say whether that decomposition is right and whether the dependencies between them are stated
correctly.

**2. Sufficiency against the rubric.** Five criteria carry 15 percent each. For each of the
eight, is what the plan produces enough to score well, or merely enough to pass a gate? Name
the criteria where the plan is thin. Aerodynamic analysis quality at 15 percent is worth
particular attention: the plan does no CFD and no wind tunnel, and has to be credible anyway.

**3. Engineering credibility.** The central claim is that a module can reach thrust to weight
above 2.5 when the best published comparable is 2.13. Is the argument the plan intends to
make defensible in a viva? What would a hostile examiner who knows this literature ask that
the plan has no answer for?

**4. The schedule against one person.** 28 days, one person, four serial weeks, another
project running alongside. Is the calendar realistic? If it is not, say which week to cut and
what to cut from it, rather than saying it is tight.

**5. Anything that will fail late.** Things that look fine now and bite on 26 September.

## You may change the plan

You have permission to edit `stage-1/plan.md` directly rather than only reporting on it. If
you do:

- Keep the format. Each week has scope files, tasks, subsessions, a "Done when" tied to gate
  behaviour, and a fallback
- Anything you change in the plan that the gates enforce has to stay consistent with
  `tools/check.py`, or say explicitly that the gate needs to change too
- Do not weaken a gate to make a week easier to pass. If a gate is wrong, say why
- Run `python tools/check.py --all` and `python tools/test_gates.py` after any edit and
  report the result
- No em dashes or en dashes anywhere in file prose, plain ASCII only. A gate enforces this

## Constraints that are not yours to relax

- The submission email is never sent by an agent, and the team is never registered by one
- Real names, institutions and claimed capability are written by a human, never invented
- No CAD at Stage 1
- If a conservative case cannot clear both targets, that is a finding to report, not an
  assumption to trim

## How to report

Findings ranked by severity, each with: where it is, what is wrong, why it matters for the
submission rather than for tidiness, and a concrete fix. Separate the ones that block week 2
from the ones that can wait.

State plainly at the end whether you would run this plan as written. If you would not, say
what has to change first.

Be skeptical of the decisions file. It is settled ground, but settled by us, and D2 is
explicitly marked provisional and unretested.
