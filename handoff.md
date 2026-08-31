# CycloProp handoff

Updated 31 August 2026. Stage 1 is due **27 September 2026** and we submit on 26 September.
This file is where a fresh session starts.

NEXT-WEEK: 5

Weeks 1 to 4 are done. Geometry froze in week 2, the mechanism in week 3, and week 4 closed the
structure, the refined mass budget and the materials and manufacturing case. Week 5 is 4 days,
it carries the deadline, and it is hard blocked by week H.

## Read these first, in order

1. **[context.md](context.md)** is the authority on what the competition requires. Built from
   the official problem statement PDF, and it outranks everything else here including this file
2. **[stage-1/plan.md](stage-1/plan.md)** is the week by week execution plan
3. **[stage-1/progress/week-4.md](stage-1/progress/week-4.md)** is where the design stands and
   what week 5 inherits. [week-3.md](stage-1/progress/week-3.md) is the mechanism record and
   [week-2.md](stage-1/progress/week-2.md) the feasibility one
4. **[stage-1/decisions.md](stage-1/decisions.md)** is what has been frozen and why. 53 entries.
   D30 unblocked week 2, D35 closed the stacked case, D38 to D45 are week 3, and D46 to D53 are
   week 4, with D53 the audit response. D47 is the one to read before touching any mass number
5. **[stage-1/design/evidence-ledger.md](stage-1/design/evidence-ledger.md)** is what every
   number rests on and how strong it is
6. **[stage-1/audit/week-4.md](stage-1/audit/week-4.md)** is the week 4 fresh-context audit,
   verbatim, and what was done about each finding

`brief.md`, `_shared-timeline.md` and `_plan-review-round1.md` are earlier work kept as history.
They were written from page summaries and contradict `context.md` in several places. When they
disagree, context.md wins. `stage-1/literature.md` is week 1's technical input and is superseded
in two places by week 2; both are marked in the file. See D26.

## To start a week

Prompts are in [_run-prompts.md](_run-prompts.md), one per tick, each for a fresh session. Run
the pre-flight block at the top first. The loop halts after every week. The execution contract
is `.claude/weekly-loop.md` and only that file, per D28.

## Where the design stands

One cyclorotor. 110 mm radius, 72.6 mm chord, 290.4 mm span, 3 blades, NACA 0020, pitching plus
or minus 40 degrees about the 30 percent chord axis, turning at 2405 rpm, driven by one T-Motor
MN5006 KV450 through a 3.5 to 1 toothed belt. 18 N of design thrust against a 10 N requirement.

The pitch mechanism is a passive four-bar per blade, all three sharing one offset pivot 15.4 mm
off the rotor axis. Link lengths 110.0, 15.40, 105.0 and 24.4 mm. Two 12.5 g servos turn a
phasing carrier through a 1.5 step up and give 120 degrees of phase authority. Packaged envelope
364.4 by 316.1 by 362.1 mm on four mount points.

The blade is a PMI foam core at 88 percent fill, two plies of 60 gsm carbon twill, a CFRP spar on
the pitch axis and two bonded 7075-T6 root fittings. 31.75 g a blade. The shaft is a 16 mm CFRP
tube with bonded end plugs, driven from one end only.

Four thrust to weight cases, and all four are reported everywhere because reporting one of them
is how week 2 confused itself for a fortnight:

| Case | Thrust | Mass | T/W |
| --- | --- | --- | --- |
| design point | 18.00 N | 607.97 g | 3.018 |
| mass downside alone | 18.00 N | 684.70 g | 2.680 |
| coefficient downside alone | 17.10 N | 607.97 g | 2.867 |
| both stacked | 17.10 N | 684.70 g | 2.5457 |

All four clear the hard limit of 2.5, and since week 4 the mass in that table is a 33 line budget
of drawn sections and catalogue parts rather than an estimate. The stacked row clears by 12.5 g,
where week 2 cleared by 4.8. That is the hard gate D30 moved into week 4 and it is passed.

The internal 2.75 target from D17 is still unmet and still not claimed. It wants the conservative
column at 633.8 g, so the gap is 50.9 g. That is a target and not a limit, and no further pass
over the budget closes it.

## Structural state

Eight margins, all floored at 1.5. Seven are recomputed by the gate from the allowable and the
demand beside them. The shaft's combined case is floored but not recomputed, because it needs
section properties that live in `tools/structure.py` and not in `numbers.json`.

| Case | Demand | Margin |
| --- | --- | --- |
| blade bending, aerodynamic only | 0.8712 Nm | 28.99 |
| blade bending, aerodynamic and centrifugal | 8.9103 Nm | 2.83 |
| blade bending at 1.20 overspeed | 12.8308 Nm | 1.97 |
| rotor shaft torsion | 1.41944 Nm | 17.58 |
| rotor shaft, bending and torsion combined | 5.83 MPa | 9.44 |
| pitch link path, the horn governs | 105.93 N | 3.30 |
| blade attachment, centrifugal | 221.464 N | 2.44 |
| blade attachment at 1.20 overspeed | 318.908 N | 1.69 |

The module is sized by the blade in combined bending and by the blade attachment, and everything
else is over 3. Each blade pulls 221.464 N against a peak aerodynamic 24.00 N, so this is a
centrifugal machine before it is an aerodynamic one. See D49.

## What week 5 does, and what it inherits

Required item 7, the execution plan, final assembly of the submission, the PDF build and staging
for a human to send. 4 days.

**1. Week H blocks it.** All 5 markers in [stage-1/human-gate.md](stage-1/human-gate.md) are
pending and `check.py` fails week 5 until a person adds all five. An agent never writes one.
Report BLOCKED if they are still missing when the tick starts. This is mechanical, not advisory.

**2. The submission draft is stale and week 5 owns it.** Items 5 and 6 are placeholders naming
week 4, and the draft's own numbers block declares `results.mass_g_conservative = 692.43` and
`results.thrust_to_weight_conservative = 2.5173`, both of which moved. Rewrite items 5 and 6 from
`05-mass-and-tw.md`, `06-materials-and-manufacturing.md` and `08-structure-and-loads.md`, fix the
four case table, then rebuild the PDF. A stale PDF passes the page count and fails the string
check.

**3. The numeric coverage gate is nearly clean already.** Run against the draft it now reports 2
untraced numbers: `margin=25mm` in the pandoc front matter, which is the gate reading YAML as
narrative, and 125.4 mm at line 66. The week 3 gate on the week 3 numbers reported 7, and week
3's own debt of 10 was a manual tally that counted exempt-region numbers the gate does not. Of
the 5 that went, the `dim_of_key` qualifier fix in D51 accounts for 3 and the rest traced once
`numbers.json` carried the week 4 budget. The front matter one is a gate defect and week 5 owns
the fix.

**4. Neither script should need running.** If one does, the order is `tools/linkage.py --write`
then `tools/structure.py --write`. `numbers.json` reproduces byte for byte from that pair.

## Still worth a human doing, in this order

**1. Week H.** All 5 markers pending, including `TECHNICAL-READ-COMPLETE`, which a person adds
only after opening the built PDF and reading it end to end. It hard blocks week 5 and it now has
the longest lead time in the project. Eligibility first, because the clause disqualifies a whole
team at any stage, including after results are announced.

**2. The two organiser questions**, page limit and registration reference format, were due by 2
September and are unsent. If no answer arrives by 8 September, use a 15 page main body plus cited
appendices.

**3. Ramsey 2022 and Heimerl.** Both are still unpulled. Ramsey would give a second structural
mass anchor and there is still only Runco, four orders of magnitude smaller than this rotor.
Heimerl measured instantaneous blade forces across Re 30,000 to 100,000 and would replace the
peak to mean estimate and the side force angle with measurements. Week 4 shipped without either
and said so.

## The human gate

All 5 markers in [stage-1/human-gate.md](stage-1/human-gate.md) are still pending. They were
advisory before week 2 and the engineering did not depend on them, so weeks 2, 3 and 4 ran. They
are a hard block on week 5, which cannot write a real capability section or stage a submission
without them. `07-team-and-execution.md` still does not exist for the same reason.

## Standing constraints

**The submission email is never sent by an agent.** Nor is the team registered, nor are real
names written into the capability section. Those are blocked triggers in the loop config and they
do not move.

Gates are run by the supervisor in its own shell and never taken from the week-agent's report:
`python tools/check.py --week N`, `--global`, and `python tools/test_gates.py`. Week 4 leaves all
three green. `tools/check.py` has never been loosened: week 2 added four gates after the first
audit, six thrust to weight gates, a measured-family exception and seven document gates; week 3
added four force map checks and two lateral load checks; week 4 added two combined blade margins,
an overspeed attachment margin, a recomputed centrifugal bending term and a band on the
conservative budget. 123 self-tests.

## Open items

- **The blade attachment at 1.20 overspeed is 1.69 and it is the tightest margin in the module.**
  The number is not the problem. The duty is: the pitch bearings swing 80 degrees under a steady
  110 N each, which is fretting, and a static rating says nothing about it. Stage 2 needs a
  supplier oscillating derate or a bench test
- **The BOM is priced and not quoted.** No supplier was contacted. The 5 lines above 4500 INR are
  52 percent of the 65770 INR total and they need written quotes at Stage 2. See D52
- **Material allowables are published typical values for the class**, not batch certificates, and
  no coupon has been tested. The cured laminate modulus is the one that matters, because the
  blade allowable turns on it
- **The two scripts have a hand resolved run order** and no gate enforces it. Better than the
  hand copied constant it replaced, and still a cycle
- **Working solo**, confirmed 27 August. Weekly hours still unstated, which matters because there
  is nobody to absorb a slipped week and week 2 already used two of its slots
- **The 0.80 continuous derate has no source.** T-Motor publishes a 180 second maximum and the
  problem statement states no endurance requirement, so the derate is a judgement
- **Four of the five motor rows and the servo are supplier listings**, not datasheet PDFs. Week 4
  did not open a manufacturer sheet for any of them
- **The coefficient reserve is deliberate and must stay unspent.** 0.6055 sits below all three
  measured or corrected values available. Week 4 found a calculation that supports the 5 percent
  blade flexibility allowance and deliberately did not spend it. See D36 and D50
- **`largest_dimension_mm` in the week 2 tables is 290 mm** and the packaged module is 364.4 mm.
  The week 2 comparison is unaffected because it applied one rule to all three layouts. See D44
- **`check.py` demands the current week's audit** while `.claude/weekly-loop.md` says the current
  week is exempt, so `--week N` fails until the audit file exists. Harmless in the order the loop
  actually runs. The config belongs to a person, so it is reported and not changed
- [stage-1/organiser-email.md](stage-1/organiser-email.md) is mostly answered by the problem
  statement now and should be cut down or dropped

## Standing risk

Week 4 was interrupted by an API failure partway through and recovered from an uncommitted
working tree in a second session. Nothing was lost, and the lesson is in the loop's favour: the
week's own scripts regenerate `numbers.json` byte for byte, so the state that mattered was
reproducible rather than remembered. Week 5 is 4 days and carries the deadline. There is no slack
left in the calendar, and week H is the one dependency an agent cannot clear.
