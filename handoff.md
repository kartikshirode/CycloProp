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

## The decision waiting for you

**1. Pull Kellen 2019.** Two minutes in a browser and the single highest-leverage thing
available. If the measured blade-area thrust coefficient for this shape family lands at or above
0.6055, the configuration-transfer allowance retires, the coefficient haircut drops from 15
percent to 5, and the conservative case moves to **2.518** with nothing else changing. That
clears the hard limit while still sitting under 2.75, so it turns a blocked week into a red one
needing a margin call. It also settles D25, because Kellen measured in the Reynolds band this
design actually sits in and the current transfer does not.

Handle 1969.1/184958, item `a4c62d38-3778-44f4-b398-cdcba283fa06` on the Texas A&M repository.
Open the item page, click Download, drop the PDF in `reference/`. The 403 is a Cloudflare
JavaScript challenge, not a permissions gate, and a real browser passes it in about two seconds.

**2. Search the motor catalogue properly.** Week 2's audit turned up that this design is **drive
limited**. Conservative thrust to weight keeps improving as the rotor gets smaller, and the 100
mm row would give 2.376, but nothing in the shortlist can hold it: the rotor torque wants a belt
ratio the selected KV450 cannot spin to on 6S, and the motor that has the speed does not have
the torque. A drive delivering about 503 W continuously at 78 g or less clears 2.5 at 100 mm on
its own. With Kellen in hand the same row tolerates 86 g and clears **2.75**. That pair is the
only route to the internal target this week found.

**3. Rule on the conservative mass allowance.** Week 2 uses 15 percent growth on catalogue parts,
20 on anything computed from an assumed section and 25 on the module frame, averaging 19.4. At a
uniform 10 percent the case reaches 2.44, still short. It is a smaller lever than it looks.

**4. Accept the finding.** Nominal thrust to weight is 3.163, already 49 percent above the best
published module on the same boundary. Reaching 2.75 conservative needs 3.86, which is 81
percent above the record. If none of the above moves, the honest position is that this design
does not close with 10 percent paper margin, and Stage 2 gets told so.

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
