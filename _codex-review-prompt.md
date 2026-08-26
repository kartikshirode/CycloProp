# Codex review prompt

Paste everything below the line into Codex, with the repo open. Round 2 of the plan cross-check. Round 1 was a self-review and is at `_plan-review-round1.md`; several of its findings are now closed and one of them (finding 7, "no problem statement document exists") turned out to be wrong.

---

You are reviewing an execution plan for a national engineering design competition. The submission is due 27 September 2026 and gets made once. Be adversarial. I want the plan's weak points found now, not in week 4.

## What this is

PUSHPAK Grand Challenge 2026, CycloProp track, run by IIT Bombay and funded by MeitY. The task is to design a cycloidal rotor module for drones producing at least 10 N of thrust at a thrust-to-weight ratio above 2.5, submitted as a preliminary design document. No CAD, no CFD, no prototype at this stage. Up to 15 teams qualify nationally.

The plan will be executed by an autonomous agent loop, one week per tick, with mechanical gates run by a supervisor between ticks. So the plan has to be executable by an agent that has only the repo and no memory of the conversation that produced it.

## Read in this order

1. `reference/cycloprop-problem-statement.txt`, the official problem statement, extracted from the PDF in the same folder. **This is ground truth.**
2. `context.md`, my transcription of what the competition requires
3. `stage-1/plan.md`, the plan under review
4. `tools/check.py`, the gate script the plan's done-when conditions depend on
5. `.claude/weekly-loop.md`, the loop config
6. `stage-1/literature.md`, the technical inputs the sizing rests on
7. `stage-1/decisions.md` and `stage-1/audit/week-1.md` for what is already frozen and what is already known to be weak

`brief.md`, `_shared-timeline.md` and `_plan-review-round1.md` are older files written before the problem statement was found. They contradict `context.md` in places. That is known and deliberate; do not report it unless you think the authority note is insufficient.

## Highest value checks, in order

**1. Is `context.md` a faithful reading of the problem statement?** Everything downstream depends on it. Diff it against `reference/cycloprop-problem-statement.txt` line by line. Specifically verify:

- the seven Stage 1 required items are complete and correctly worded
- the eight evaluation criteria and their weights, and that they sum to 100
- the thrust-to-weight basis quote, since the entire 408 g mass budget rests on it
- the target design requirements table
- anything in the problem statement that `context.md` omits entirely. Omissions matter more than errors here

**2. Are the gates gameable?** Read `tools/check.py` as an adversary. The design intent is that an agent cannot pass a week by writing a flattering number into prose, because the arithmetic has to reproduce from stored geometry. Try to find a way to satisfy every gate with a design that is wrong, incomplete or physically absurd. Run it: `python tools/check.py --all` should exit 0, `python tools/check.py --week 5` should exit 1. Check the tolerance (2 percent) is not hiding real error, and check that a week can not pass by deleting or emptying a file.

**3. Does the plan actually cover the requirements?** Build two coverage matrices and report any gap:

- each of the 7 Stage 1 required items against the week and file that produces it
- each of the 8 evaluation criteria against the section that answers it

**4. Is the schedule survivable?** Week 1 is done. Weeks 2 to 4 are seven days each, week 5 is four days and carries the deadline. Each week has a stated fallback. Ask whether the fallbacks actually protect the deadline or just move the failure, and whether the week 4 decision gate that can reopen week 2 geometry is recoverable in the time left.

**5. Is the engineering defensible?** You do not need to be a rotorcraft specialist. Check the reasoning chain rather than the domain:

- the mass argument that rules out a cluster of small rotors in favour of one larger one
- the claim that holding a fixed shape family at fixed thrust pins Reynolds number near 100,000 regardless of radius
- the blade-area thrust coefficient of 0.607, which is derived from a single measured data point and which all the week 2 sizing scales off
- the power estimate of 152 to 161 W aerodynamic and 230 to 250 W electrical, which replaced an earlier 95 W figure
- whether a 10 N single cyclorotor under 408 g is plausible at all, or whether the plan is walking toward a wall it should see now

## Known weak points, so you do not spend effort confirming them

These are already recorded. Tell me if they are worse than I think, otherwise skip them:

- The Texas A&M thesis that week 2's default blade shape family comes from was never opened, only summarised. Its three shape numbers are internally consistent, which is evidence and not verification
- Two more papers are paywalled, one of them the closest published passive pitch mechanism
- Real weekly hours and team size are unknown, so the schedule is unvalidated
- This runs in parallel with a second competition project whose week 3 collides with this one's

## Do not

- Do not edit any file. Report only
- Do not rewrite prose for style. The repo bans em dashes and en dashes on purpose; that is a house rule, not an error
- Do not relitigate the decisions in `stage-1/decisions.md` unless you have found an actual flaw in one
- Do not propose CAD, CFD or FEA work at Stage 1. The problem statement does not ask for it and it is scored at Stage 2
- Do not propose git operations. No pushing, branching or history rewriting

## Output format

Findings ordered by how much damage they do if left alone, not by which file they sit in.

For each:

```
### F<n>: <one line statement of the defect>
Severity: blocker | significant | minor
Location: <file>, <section or line>
What is wrong:
Why it matters:
Concrete fix:
```

"Blocker" means the plan fails or the submission loses marks if this ships unchanged. "Significant" means real cost. "Minor" means worth fixing cheaply.

Then close with:

- **Coverage matrices** from check 3, as tables, with any gap called out
- **Verdict**: is this plan good enough to execute as written, good enough with the listed fixes, or does it need restructuring
- **The single highest-risk assumption** in the whole plan, named in one sentence

If you find nothing at a given severity, say so explicitly rather than inventing something to fill the section.
