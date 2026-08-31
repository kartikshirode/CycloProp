# CycloProp handoff

Updated 2 September 2026. Stage 1 is due **27 September 2026** and we submit on 26 September.
This file is where a fresh session starts.

NEXT-WEEK: 2

**That marker still says 2 on purpose.** Week 2 ran and produced everything it was asked for,
then reported BLOCKED on the thrust to weight call. That call is now made and recorded as D30,
so week 2 reruns to freeze the geometry and finish. The marker moves when it does. Full account
in [stage-1/progress/week-2.md](stage-1/progress/week-2.md).

## Read these first, in order

1. **[context.md](context.md)** is the authority on what the competition requires. Built from
   the official problem statement PDF, and it outranks everything else here including this file
2. **[stage-1/progress/week-2.md](stage-1/progress/week-2.md)** is the current state and the
   blocked report
3. **[stage-1/audit/week-2.md](stage-1/audit/week-2.md)** is the 18 findings the week 2 audit
   returned and what was done about each
4. **[stage-1/plan.md](stage-1/plan.md)** is the week by week execution plan
5. **[stage-1/design/evidence-ledger.md](stage-1/design/evidence-ledger.md)** is what every
   number rests on and how strong it is
6. **[stage-1/decisions.md](stage-1/decisions.md)** is what has been frozen and why. 27 entries

`brief.md`, `_shared-timeline.md` and `_plan-review-round1.md` are earlier work kept as history.
They were written from page summaries and contradict `context.md` in several places. When they
disagree, context.md wins. `stage-1/literature.md` is week 1's technical input and is superseded
in two places by week 2; both are marked in the file. See D26.

## To start a week

Prompts are in [_run-prompts.md](_run-prompts.md), one per tick, each for a fresh session. Run
the pre-flight block at the top first. The loop halts after every week. The week 2 prompt gets
reused, because week 2 has to run again once a person has made the call below.

## Where we are

Week 1 is done. Week 2 has run once and is blocked.

Everything week 2 was asked to produce exists: the evidence ledger, three design documents, the
full numbers block, the candidate comparison, the coupled radius sweep, the mass envelope, the
frozen thrust sensitivity table, and four new gates the audit asked for. What does not exist is
a frozen geometry, because the conservative case came out at a thrust to weight of **2.252**
against a hard limit of 2.5 and an internal target of 2.75.

That is a miss of 69 g of module mass against the hard limit, on a 692 g conservative estimate.

## The decision has been made, see D30

Week 2 halted correctly and the call it stopped for is recorded as D30 in
[stage-1/decisions.md](stage-1/decisions.md). Read that entry before touching anything.

The short version. Four thrust to weight cases exist, not one. The design point is 3.1633.
The mass downside alone gives 2.6499 and the coefficient downside alone gives 2.6889, so each
clears the limit on its own. Only stacking both misses, at 2.2525. Nine of the thirteen
envelope lines are assumed sections carrying a blanket 20 or 25 percent growth rate, so the
stacked figure tests those rates as much as the design.

Geometry therefore freezes at 18 N and 110 mm, with 120 mm carried as insurance. The stacked
test moves to week 4, where `week4: conservative T/W clears 2.5` already applies the same
limit to a budget built from real sections and catalogue parts. Week 2 gains three new hard
gates in its place, one per single case, and a miss on the stacked case now has to hand week 4
a mass target of 623.9 g that the gate recomputes.

Every fallback was rechecked by hand before deciding and none of them closes. 20 N fails on
power at 110 mm and on an empty belt window at 120 mm. The 100 mm row has an empty belt window
too, for any pulley pair rather than only the half integer ones week 2 tried. No shortlist
drive reaches 503 W under 78 g. A uniform 10 percent growth rate still leaves 2.44.

## Still worth a human doing, in this order

**1. Pull Kellen 2019.** No longer a blocker, still the cheapest win available. It moves the
stacked case to 2.5173 on its own, and it settles D25, because Kellen measured across a
Reynolds band of 100,000 to 300,000 and this design sits at 134,074, inside it.

Handle 1969.1/184958, item `a4c62d38-3778-44f4-b398-cdcba283fa06` on the Texas A&M repository.
The item page, the bitstream and the handle URL all return 403 to a script, because it is a
Cloudflare JavaScript challenge rather than a permissions gate. A real browser passes it in
about two seconds. Open the item page, click Download, drop the PDF in `reference/`.

**2. Week H.** All five markers pending. It hard blocks week 5 and nothing else. Eligibility
first, because the clause disqualifies a whole team at any stage.

**3. The drive, at week 4.** Pack voltage sits outside the module boundary, so cell count
costs the module nothing. Motor torque ceiling goes as current over KV and speed ceiling as
KV times voltage, so their product is power and has no KV in it. Week 2 fixed KV450 on 6S and
then searched only the belt ratio, which imposed a constraint the motor's power rating does
not. A lower KV variant on more cells would reopen the 100 mm row. It needs a datasheet.

## What week 2 established that does not depend on the freeze

- **The single rotor beats a redesigned cluster.** 2.252 against 1.659 for two rotors and 1.323
  for three, on one common model with every contested assumption set in the cluster's favour.
  D2 was provisional since week 1 and is now settled. See D18
- **The 0.607 coefficient reproduces.** Recomputing it from Benedict's quad rotor figures gives
  0.6055, so the number the repo has carried since week 1 is right to a quarter of a percent
- **The Reynolds transfer is an extrapolation and cannot be made otherwise.** The conservative
  thrust gate forces design thrust above 11.76 N, which puts chord Reynolds above 108,000, above
  the 100,000 top of the range the transfer has published support over. See D25
- **Almost nothing in this module is fixed mass.** Sorted honestly, one 8 g controller board.
  D11 and D13 rest the feasibility case on fixed hardware amortising, and there is very little
  to amortise
- **Design thrust is a real lever with a top.** Between 13 N and 18 N the mass ceiling grows 203
  g while the drive grows about 30 g. At 20 N nothing in the shortlist fits. Four rows frozen at
  13, 16, 18 and 20 N. See D21
- **Both allocation questions are closed.** ESCs are module hardware, mounting counts in full,
  both against us and both fixed before scoring. See D19

## Week 3, when it starts

Configuration, sizing, thrust and power are all in place, so week 3 has what it needs on
geometry as long as somebody accepts a candidate radius. Linkage topology and loop closure, the
solved pitch schedule, the vectoring actuator and force-vector map, packaging, and the item 7
structure.

Two things week 3 inherits:

- The azimuthal load model uses a prescribed sinusoid with no phase offset, so side force is zero
  by construction. Week 3 reruns it against the schedule the solved linkage actually produces,
  and side force is where the real risk is. Benedict measured a resultant 30 degrees off
  vertical, Adams 15 to 35 degrees depending on amplitude and rpm
- The candidate radius is 110 mm with 120 mm carried as insurance. Switching after week 3 costs
  a week 3 rerun, because link lengths, offset geometry, the pitch schedule and gearing all move
  with radius

## The human gate

All five markers in [stage-1/human-gate.md](stage-1/human-gate.md) are still pending. They were
advisory before week 2 and the engineering did not depend on them, so week 2 ran. They are a
hard block on week 5, which cannot write a real capability section or stage a submission without
them.

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
exactly one gate failing and it is the thrust to weight decision line. `tools/check.py` was
changed this week, only to add four gates and never to loosen one, with 12 self-tests added
alongside them. The suite is 89 checks now.

## Open items

- **Two files claim to be the loop execution contract.** `stage-1/plan.md` names
  `.codex/weekly-loop.md`; this tick ran against `.claude/weekly-loop.md` because the launching
  human said so, and it is the newer file. The plan was deliberately not edited. Somebody has to
  say which wins. See D24
- **Working solo**, confirmed 27 August. Weekly hours still unstated, which matters more now
  than it did, because there is nobody to absorb a slipped week and week 2 has to run twice
- **The 0.80 continuous derate has no source.** T-Motor publishes a 180 second maximum and the
  problem statement states no endurance requirement, so the derate is a judgement. A stated
  hover duration would turn it into a calculation
- **Four of the five motor rows came from supplier listings**, not datasheet PDFs. Only the
  MN5006 was read off the manufacturer's sheet. Week 4 confirms the rest
- **Ramsey 2022 and Heimerl** are still unpulled. Ramsey would give a second structural mass
  anchor; there is currently one, Runco, four orders of magnitude smaller. Heimerl would replace
  the stated 28 degree stall cap and the peak to mean blade load with measured figures
- [stage-1/organiser-email.md](stage-1/organiser-email.md) is mostly answered by the problem
  statement now and should be cut down or dropped

## Standing risk

Week 3 collides with the UAV-X comms layer, the highest-risk piece across both projects. If
something has to slip, slip this one. Week 5 is 4 days and carries the deadline, so weeks 2 to 4
do not get to overrun into it. Week 2 has now used one of its slots and produced a decision
rather than a design, which eats calendar. The cheapest recovery is option 1 above.
