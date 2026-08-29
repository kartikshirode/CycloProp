# Run prompts

One prompt per tick, each pasted into a **fresh session** in this repository. The loop is set
to `checkpoint_every: 1`, so every run does one week and halts for you to read it.

## Before the first run

Run this and read the output. Everything should say YES.

```
git status --porcelain                       # empty
ls .claude/weekly-loop-sentinel.json         # should not exist
grep '^NEXT-WEEK:' handoff.md                # exactly one line
python tools/check.py --week 1               # exits 0
python tools/test_gates.py                   # 77 pass
```

A sentinel file present means a previous tick died part way. Do not start the week fresh in
that case; the supervisor will spawn a recovery agent, which is correct. If you committed
anything by hand during a halt, **delete the sentinel first**, or your commits get treated as
a dead agent's partial work.

Week H is still outstanding, all five markers pending. It does not block weeks 2 to 4. It
hard-blocks week 5, and eligibility is worth doing before any of this.

---

## Week 2, the feasibility week

Starts 2 September. 26 hours of work, 22 gates currently failing, roughly 80 numbers to fill.
This is the week that decides whether the project closes.

```
/loop

Run week 2 of stage-1/plan.md under the weekly-loop skill, config at
.claude/weekly-loop.md. One tick only, then halt at the checkpoint.

Read _codex-context.md first for the competition requirements and the state of
the argument. stage-1/decisions.md is settled ground: D2 is the exception and is
explicitly provisional, so the single versus cluster comparison is genuinely open.

Three things decide whether this week is worth anything:

- Every value that carries a design decision goes in the evidence ledger with its
  class. A transferred coefficient is never labelled measured. The 0.516 low value
  is an engineering downside scenario, not a published bound, unless the Kellen
  figures arrive.
- The conservative case has to clear the targets on its own. Geometry freezes only
  then. If it clears 2.5 but misses the 2.75 internal target that is compliant and
  still red, so stop and report rather than freezing.
- Sort every mass line into geometry-scaled, power or torque-scaled, or genuinely
  fixed. The drive is not a fixed mass. Larger radius lowers power but raises
  torque, so it does not come free.

If the conservative case cannot close after the written fallbacks, report BLOCKED.
That is a finding, not a failure, and it is more useful than a number that appears
after an assumption gets trimmed.
```

**At the halt, read:** `stage-1/progress/week-2.md`, `stage-1/audit/week-2.md`, and the
conservative T/W in `stage-1/design/numbers.json`. The audit's hostile-examiner section is
the part worth your attention. Then check the evidence ledger for anything called measured
that was transferred.

---

## Week 3, pitch and vectoring

Starts 9 September. 18 hours. Two 15 percent criteria live here.

```
/loop

Run week 3 of stage-1/plan.md under the weekly-loop skill, config at
.claude/weekly-loop.md. One tick only, then halt.

The pitch schedule has to come out of a solved linkage, not a harmonic table that
looks right. Loop closure, link dimensions, clearance and singularity checks, and
an actuator sized for the load.

Thrust vectoring is demonstrated by force results at three or more phase commands,
each giving vertical and lateral force. Mechanical phase authority on its own is
not evidence of vectoring.

Item 7, team capability, has no engineering dependency and gets drafted here if
week H has returned the roster. Structure and argument only. Real names,
institutions and capability claims come from a human and are never invented.
```

**At the halt, read:** the linkage closure and the force-vector map. Ask whether the map
would survive someone asking why the vector points where it does.

---

## Week 4, mass, structure and the number

Starts 16 September. 24 hours. This is where T/W becomes a stated result.

```
/loop

Run week 4 of stage-1/plan.md under the weekly-loop skill, config at
.claude/weekly-loop.md. One tick only, then halt.

Every budget line names the envelope line it refines and stays within 25 percent
of it. Structural demands are derived from the design, never asserted beside it:
per-blade mass from the blade budget and blade count, rotor shaft torque from
shaft power and speed, blade root bending from thrust per blade with the lever arm
and load factor. Centrifugal load is the larger term and the attachment carries
its own margin against it.

Design thrust may only move to a row already in the week 2 sensitivity table. An
unstudied increase is a rerun of week 2, not a week 4 edit.

If the budget still misses after the prequalified fallbacks, report BLOCKED.
```

**At the halt, read:** the recomputed nominal and conservative T/W, and whether the mass
categories still agree with the scaling classes set in week 2.

---

## Week 5, assembly and staging

Starts 23 September, 4 days, carries the deadline. Blocked on week H.

```
/loop

Run week 5 of stage-1/plan.md under the weekly-loop skill, config at
.claude/weekly-loop.md. One tick only, then halt.

All seven required items as top-level sections in the problem statement's order,
with the criteria map as a real table covering all eight criteria. Build the PDF
and confirm it reads back as this submission rather than some other document.

Draft the email, name the attachment and the organiser address, and stage
everything. Do not send. A person sends on 26 September.

If any human gate marker is outstanding, report BLOCKED rather than inventing the
team capability section.
```

**At the halt:** open the built PDF and read it end to end. Only then replace
`TECHNICAL-READ-PENDING` with `TECHNICAL-READ-COMPLETE` in `stage-1/human-gate.md`. The gate
will not let the submission stage without it, which is the point.

---

## What each halt state means

| Report | What it means | What you do |
| --- | --- | --- |
| CHECKPOINT | Week done, all gates green | Read the progress and audit files, then run the next prompt |
| BLOCKED | A design finding or a human task | Read the unblock steps. This is the loop working, not failing |
| GATE-FAIL | A fix agent already tried and gates still fail | Read the gate output. Something is genuinely wrong |
| DIRTY-TREE | Uncommitted work was present | Commit or stash it, then rerun |
| PLAN-DONE | No week left | Week 5 finished |

Never run a loop longer than 7 to 8 hours. Past that the increment per cycle collapses, and
none of these weeks needs that long in one sitting.
