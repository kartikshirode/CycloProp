# CycloProp handoff

Updated 31 August 2026. Stage 1 is due **27 September 2026** and we submit on 26 September.
This file is where a fresh session starts.

NEXT-WEEK: 5

Weeks 1 to 4 are done. Geometry froze in week 2, the mechanism in week 3, and week 4 closed the
structure, the refined mass budget and the materials and manufacturing case.

**Week 5 has not run and this file does not say it has.** It is hard blocked by week H, and a
preparation pass on 31 August closed every week 5 gate that does not need a person: item 7 is
written, the submission is rebuilt and its PDF is built and inspected, the coverage gate defect
is fixed, and the email is drafted and staged. `python tools/check.py --week 5` now fails on the
human gate alone. See D58, and "What is left of week 5" below.

## Read these first, in order

1. **[context.md](context.md)** is the authority on what the competition requires. Built from
   the official problem statement PDF, and it outranks everything else here including this file
2. **[stage-1/plan.md](stage-1/plan.md)** is the week by week execution plan
3. **[stage-1/progress/week-4.md](stage-1/progress/week-4.md)** is where the design stands and
   what week 5 inherits. [week-3.md](stage-1/progress/week-3.md) is the mechanism record and
   [week-2.md](stage-1/progress/week-2.md) the feasibility one
4. **[stage-1/decisions.md](stage-1/decisions.md)** is what has been frozen and why. 58 entries.
   D30 unblocked week 2, D35 closed the stacked case, D38 to D45 are week 3, and D46 to D53 are
   week 4, with D53 the audit response. D54 to D58 are the week 5 preparation pass. D47 is the
   one to read before touching any mass number, and D58 before assuming week 5 ran
5. **[stage-1/design/evidence-ledger.md](stage-1/design/evidence-ledger.md)** is what every
   number rests on and how strong it is
6. **[stage-1/audit/week-4.md](stage-1/audit/week-4.md)** is the week 4 fresh-context audit,
   verbatim, and what was done about each finding.
   [week-5.md](stage-1/audit/week-5.md) audits the preparation pass the same way
7. **[stage-1/submission/cycloprop-stage1.md](stage-1/submission/cycloprop-stage1.md)** is the
   assembled report and [email-draft.md](stage-1/submission/email-draft.md) is the staged mail.
   Both carry `[P-n]` placeholders and neither is finished until a person fills them

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

## What is left of week 5

Required item 7, the submission, the PDF and the staged email are done. What is left is the
human gate, the real team facts, and one short run to fold them in.

**1. Week H still blocks it.** Four markers in [stage-1/human-gate.md](stage-1/human-gate.md) are
pending and `check.py` fails week 5 until a person adds all four. An agent never writes one. The
fifth, `TECHNICAL-READ-COMPLETE`, already appears in that file's prose, so the gate does not see
it as outstanding; it is still a real task and it blocks final staging rather than the start.

**2. The nine placeholders.** `[P-1]` to `[P-9]`, listed in one table at the top of
[07-team-and-execution.md](stage-1/design/07-team-and-execution.md) and referenced from the
submission's identity table and the email draft. Four are also week H markers. Filling them is
the substance of what is left, per D55.

**3. Then one short run.** Fold the team facts into item 7 and the submission's identity table,
rebuild the PDF, add the markers, read the PDF end to end, and write the week 5 progress file
and audit. Nothing in it needs either solver. If one is ever needed, the order is
`tools/linkage.py --write` then `tools/structure.py --write`, and `numbers.json` reproduces byte
for byte from that pair.

## What the preparation pass changed

- **`stage-1/design/07-team-and-execution.md` exists.** The execution plan across all 11 Stage 2
  items with the gate that closes each one, the capability gap analysis against the problem
  statement's seven preference areas, the Stage 2 gates and the route through the missing
  capability. No name, institution, qualification or tool licence is written anywhere in it
- **The submission is rebuilt from the reviewed design documents**, assembled rather than
  rewritten. All 7 required items in the official order, the 8 row criteria map, a claims and
  risk table, a provenance section naming which sources were read and which were not, and an
  appendix of 12 examiner questions. The stale week 2 mass figures are gone
- **The PDF is built, read back and inspected.** 21 pages, 1 of title and contents, 15 of body,
  the rest appendix. The xelatex log is clean of overfull lines after two were fixed
- **The coverage gate defect is fixed.** `margin=25mm` in the pandoc header is build
  configuration, not a design claim, and the skip is positional so the same text in the body
  still fails. 124 self-tests to 128. See D54
- **The email is drafted and staged.** Nothing was sent. The registration reference is a marked
  placeholder and the draft lists the six things a person does before pressing send

## Still worth a human doing, in this order

**1. Eligibility, first.** The clause disqualifies a whole team at any stage, including after
results are announced, so an ineligible roster turns every other week into wasted effort. Then
add `ELIGIBILITY-CHECKED`.

**2. Register** on techfest.org and keep the reference. Then add `REGISTRATION-CONFIRMED`, and
put the reference into `[P-7]`, which is the placeholder in the email subject and body.

**3. Confirm the roster and the sender**, then add `ROSTER-CONFIRMED` and `SENDER-CONFIRMED`.
That is the four markers and it unblocks week 5.

**4. Fill `[P-1]` to `[P-9]`** in `07-team-and-execution.md`, and the three identity fields at
the top of the submission.

**5. Rebuild the PDF.** The command is in `.claude/codemap.md`. A stale PDF passes the page
count and fails the string check.

**6. Read the built PDF end to end**, then add `TECHNICAL-READ-COMPLETE`. Title, the three
identity fields, section order, the summary numbers and the claims table.

**7. Send on 26 September**, from the registered address, and keep the sent copy. That is D5 and
it does not move.

**Ramsey 2022 and Heimerl** are still unpulled and still worth an hour if one exists. Ramsey
would give a second structural mass anchor and Heimerl would replace the peak to mean load
factor and the side force angle with measurements. Neither is cited as read anywhere.

## The human gate

Four of the five markers in [stage-1/human-gate.md](stage-1/human-gate.md) are outstanding and
they are the only thing failing `--week 5`. They were advisory before week 2 and the engineering
did not depend on them, so weeks 2, 3 and 4 ran. Week 5 cannot finish without them, because a
capability section with invented names and a submission staged against no registration reference
would both be fabrication rather than work.

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
conservative budget. The week 5 preparation pass fixed one reader defect and loosened nothing:
the coverage audit no longer reads the pandoc front matter as a design claim, and the skip is
positional so the same text in the body still fails. 128 self-tests.

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
- **The page limit and the file naming convention were never answered.** The questions were
  drafted for early September and never sent. The working assumption is 15 pages of body plus
  cited appendices, the built report is 21 pages on that reading, and the question now rides at
  the end of the staged submission email. See D57
- **The submission carries `[P-1]`, `[P-2]` and `[P-7]` in its identity table** and will print
  "to be completed" in the attachment until a person fills them and rebuilds the PDF
- [stage-1/organiser-email.md](stage-1/organiser-email.md) is mostly answered by the problem
  statement now and its two live questions have moved into the submission email draft

## Standing risk

Week 4 was interrupted by an API failure partway through and recovered from an uncommitted
working tree in a second session. Nothing was lost, and the lesson is in the loop's favour: the
week's own scripts regenerate `numbers.json` byte for byte, so the state that mattered was
reproducible rather than remembered.

Week H is still the one dependency an agent cannot clear, and it now has the longest lead time in
the project by a distance. Everything else that could be done ahead of it has been done. What is
left of week 5 is short, and it stays blocked until four markers and nine facts arrive from a
person.

One trap found while reading the built PDF back, worth knowing before the last rebuild. pypdf
returns a single ff ligature character wherever the text says "off", and the contents page
returns "T eam capability" with a space in it from kerning while the same heading in the body
extracts cleanly. The identity gate passes on the body copy. A gate string carrying a double f
would not.
