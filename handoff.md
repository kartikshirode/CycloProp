# CycloProp handoff

Updated 2 September 2026. Stage 1 is due **27 September 2026** and we submit on 26 September.
This file is where a fresh session starts.

NEXT-WEEK: 2

**That marker still says 2 on purpose.** Week 2 ran, produced everything it was asked for, and
reported BLOCKED on the one thing that decides the project. Geometry did not freeze, so week 2
is not done and the marker does not move. Full account in
[stage-1/progress/week-2.md](stage-1/progress/week-2.md).

## Read these first, in order

1. **[context.md](context.md)** is the authority on what the competition requires. Built from
   the official problem statement PDF, and it outranks everything else here including this file
2. **[stage-1/progress/week-2.md](stage-1/progress/week-2.md)** is the current state and the
   blocked report
3. **[stage-1/plan.md](stage-1/plan.md)** is the week by week execution plan
4. **[stage-1/design/evidence-ledger.md](stage-1/design/evidence-ledger.md)** is what every
   number rests on and how strong it is
5. **[stage-1/decisions.md](stage-1/decisions.md)** is what has been frozen and why. 24 entries

`brief.md`, `_shared-timeline.md` and `_plan-review-round1.md` are earlier work kept as
history. They were written from page summaries and contradict `context.md` in several places.
When they disagree, context.md wins.

## Where we are

Week 1 is done. Week 2 has run once and is blocked.

Everything week 2 was asked to produce exists: the evidence ledger, three design documents,
the full numbers block, the candidate comparison, the coupled radius sweep, the mass envelope
and the frozen thrust sensitivity table. What does not exist is a frozen geometry, because the
conservative case came out at a thrust to weight of **2.389** against a hard limit of 2.5 and
an internal target of 2.75.

That is a miss of 32 g of module mass against the hard limit. It is close, and being close is
why the decision goes to a person rather than getting rounded.

## The decision waiting for you

Three ways forward. The first is cheap and the third is honest.

**1. Pull Kellen 2019.** Two minutes in a browser. If the measured blade-area thrust
coefficient for this shape family lands at or above 0.6055, the 10 percent
configuration-transfer allowance retires, the coefficient haircut drops from 15 percent to 5,
and the conservative case moves to roughly 2.68. That clears the hard limit while still
sitting under 2.75, so it turns a blocked week into a red one needing a margin call. This is
the highest-leverage thing available and it costs almost nothing. Details in D23.

Handle 1969.1/184958, item `a4c62d38-3778-44f4-b398-cdcba283fa06` on the Texas A&M repository.
Open the item page, click Download, drop the PDF in `reference/`. The 403 is a Cloudflare
JavaScript challenge, not a permissions gate, and a real browser passes it in about two
seconds.

**2. Rule on the conservative mass allowance.** Week 2 used 15 percent growth on catalogue
parts and 20 to 25 percent on structure computed from assumed sections, which averages 18
percent. At a uniform 10 percent the conservative case reaches 2.564 and clears the limit. The
agent did not make that change, because moving an allowance until the number appears is the
failure mode the blocked trigger exists to catch. It is a legitimate engineering judgement and
it is yours to make.

**3. Accept the finding.** Nominal thrust to weight is 3.318, already 56 percent above the best
published module on the same boundary. Reaching 2.75 conservative needs 3.82, which is 79
percent above the record. If neither 1 nor 2 moves, the honest position is that this design
does not close with 10 percent paper margin, and Stage 2 gets told so.

## What week 2 established that does not depend on the freeze

- **The single rotor beats a redesigned cluster.** 2.389 against 1.795 for two rotors and
  1.434 for three, on one common model with every contested assumption set in the cluster's
  favour. D2 was provisional since week 1 and is now settled. See D18
- **The 0.607 coefficient reproduces.** Recomputing it from Benedict's quad rotor figures gives
  0.6055, so the number the repo has carried since week 1 is right to a quarter of a percent
  and is now derivable in one line rather than quoted
- **Design thrust is a real lever and it has a top.** Between 13 N and 20 N the mass ceiling
  grows 285 g while the drive grows about 75 g. Above 20 N the drive shortlist runs out at 555
  W continuous and it stops paying. Four rows frozen at 13, 16, 20 and 24 N. See D21
- **The named drive works on its continuous rating.** MN3510 KV700 at 6 to 1 sits at 92 percent
  of continuous power and 87 percent of continuous torque. Not a peak figure
- **Both allocation questions are closed.** ESCs are module hardware, mounting counts in full,
  both against us and both fixed before scoring. See D19

## Week 3, when it starts

Configuration, sizing, thrust and power are all in place, so week 3 has what it needs on
geometry as long as somebody accepts a candidate radius. Linkage topology and loop closure, the
solved pitch schedule, the vectoring actuator and force-vector map, packaging, and the item 7
structure.

Two things week 3 inherits from week 2:

- The azimuthal load model uses a prescribed sinusoid with no phase offset, so side force is
  zero by construction. Week 3 reruns it against the schedule the solved linkage actually
  produces, and side force is where the real risk is. Benedict measured a resultant 30 degrees
  off vertical, Adams 15 to 35 degrees depending on amplitude and rpm
- The candidate radius is 115 mm with 125 mm carried as insurance. Switching after week 3 costs
  a week 3 rerun, because link lengths, offset geometry, the pitch schedule and gearing all
  move with radius

## The human gate

All five markers in [stage-1/human-gate.md](stage-1/human-gate.md) are still pending. They were
advisory before week 2 and the engineering did not depend on them, so week 2 ran. They are a
hard block on week 5, which cannot write a real capability section or stage a submission
without them.

Do the eligibility check first regardless. The clause disqualifies a whole team at any stage,
including after results are announced, so an ineligible roster makes every other week wasted
effort.

The two organiser questions, page limit and registration reference format, were due by 2
September and are unsent. If no answer arrives by 8 September, use a 15 page main body plus
cited appendices.

## Standing constraints

**The submission email is never sent by an agent.** Nor is the team registered, nor are real
names written into the capability section. Those are blocked triggers in the loop config and
they do not move.

Gates are run by the supervisor in its own shell and never taken from the week-agent's report:
`python tools/check.py --week N`, `--global`, and `python tools/test_gates.py`. Week 2 leaves
exactly one gate failing and it is the thrust to weight decision line. Nothing in
`tools/check.py` was modified.

## Open items

- **Two files claim to be the loop execution contract.** `stage-1/plan.md` names
  `.codex/weekly-loop.md`; this tick ran against `.claude/weekly-loop.md` because the launching
  human said so, and it is the newer file. The plan was deliberately not edited. Somebody has
  to say which wins. See D24
- **Working solo**, confirmed 27 August. Weekly hours still unstated, which matters more now
  than it did, because there is nobody to absorb a slipped week
- **Motor and ESC figures are supplier listings, not datasheet PDFs.** Week 4 confirms them
- **Ramsey 2022 and Heimerl** are still unpulled. Ramsey would give a second structural mass
  anchor; there is currently exactly one, Runco, four orders of magnitude smaller. Heimerl
  would replace the stated 28 degree stall cap and the peak to mean blade load with measured
  figures
- [stage-1/organiser-email.md](stage-1/organiser-email.md) is mostly answered by the problem
  statement now and should be cut down or dropped

## Standing risk

Week 3 collides with the UAV-X comms layer, the highest-risk piece across both projects. If
something has to slip, slip this one. Week 5 is 4 days and carries the deadline, so weeks 2 to
4 do not get to overrun into it. Week 2 has now used one of its slots and produced a decision
rather than a design, which eats calendar. The cheapest recovery is option 1 above.
