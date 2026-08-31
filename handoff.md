# CycloProp handoff

Updated 31 August 2026. Stage 1 is due **27 September 2026** and we submit on 26 September.
This file is where a fresh session starts.

NEXT-WEEK: 3

Weeks 1 and 2 are done. Geometry is frozen at 18 N of design thrust and a 110 mm radius, with
120 mm carried as insurance. Week 3 is next and it has everything it needs.

## Read these first, in order

1. **[context.md](context.md)** is the authority on what the competition requires. Built from
   the official problem statement PDF, and it outranks everything else here including this file
2. **[stage-1/plan.md](stage-1/plan.md)** is the week by week execution plan
3. **[stage-1/progress/week-2.md](stage-1/progress/week-2.md)** is where the design stands and
   what week 3 inherits
4. **[stage-1/decisions.md](stage-1/decisions.md)** is what has been frozen and why. 34 entries,
   and D30 is the one that unblocked week 2
5. **[stage-1/design/evidence-ledger.md](stage-1/design/evidence-ledger.md)** is what every
   number rests on and how strong it is
6. **[stage-1/audit/week-2.md](stage-1/audit/week-2.md)** is the two fresh-context audit
   passes over week 2, verbatim, and what was done about each finding

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

Four thrust to weight cases, and all four are reported everywhere because reporting one of them
is how week 2 confused itself for a fortnight:

| Case | Thrust | Mass | T/W |
| --- | --- | --- | --- |
| design point | 18.00 N | 580.1 g | 3.163 |
| mass downside alone | 18.00 N | 692.4 g | 2.650 |
| coefficient downside alone | 15.30 N | 580.1 g | 2.689 |
| both stacked | 15.30 N | 692.4 g | 2.252 |

The first three clear the hard limit of 2.5 and the geometry froze on them. The stacked case
misses by 68.5 g and that shortfall is now a number week 4 owns: `results.mass_target_week4_g`
is 623.9 g, the conservative mass that would put the stacked case exactly on 2.5. The gate
recomputes it. See D30 for the call and D31 for the target.

The internal 2.75 margin target from D17 is not met on the stacked case and nobody is claiming
it is.

## What week 3 does, and the two things it inherits

Linkage topology and loop closure, the solved pitch schedule, the vectoring actuator and the
force-vector map, packaging, and the item 7 structure. Configuration, sizing, thrust and power
are all frozen underneath it.

**1. The azimuthal load model has zero side force by construction.** It uses a prescribed
sinusoid with no phase offset, so the lateral components cancel exactly over the cycle. That is
the input, not a result. Week 3 reruns the model against the schedule the solved linkage
actually produces, and side force is where the real risk sits. Benedict measured a resultant 30
degrees off vertical and Adams 15 to 35 degrees depending on amplitude and rpm.

**2. The radius is 110 mm and it is frozen.** 120 mm is carried as insurance against a week 2
mistake, not as a free option. Switching after week 3 costs a week 3 rerun, because link
lengths, offset geometry, the pitch schedule and gearing all move with radius.

## Still worth a human doing, in this order

**1. Week H.** All five markers pending. It hard blocks week 5 and nothing else. Eligibility
first, because the clause disqualifies a whole team at any stage, including after results are
announced.

**2. Pull Kellen 2019.** Not a blocker any more, still the cheapest win on the list. A measured
coefficient at or above 0.6055 retires the configuration-transfer allowance, which takes
conservative thrust to 17.1 N and makes the mass that clears 2.5 into 697.2 g. The module
already weighs 692.4 g conservative, so week 4's mass target would disappear rather than
shrink. `check.py` is ready for it: a coefficient scenario classed measured, on this design's
own solidity and chord to radius, drops the haircut floor from 10 percent to 5. It would also
settle D25, because Kellen's test range is reported as 100,000 to 300,000 and this design sits
at 134,074, inside it.

Handle 1969.1/184958, item `a4c62d38-3778-44f4-b398-cdcba283fa06` on the Texas A&M repository.
The item page, the bitstream and the handle URL all return 403 to a script, because it is a
Cloudflare JavaScript challenge rather than a permissions gate. core.ac.uk and oatd.org were
tried on 31 August and neither has it. A real browser passes in about two seconds. Open the
item page, click Download, drop the PDF in `reference/`.

**3. The drive, at week 4.** Pack voltage sits outside the module boundary, so cell count costs
the module nothing. Motor torque ceiling goes as current over KV and speed ceiling as KV times
voltage, so their product is power and has no KV in it. Week 2 fixed KV450 on 6S and then
searched only the belt ratio, which imposed a constraint the motor's power rating does not. A
lower KV variant on more cells would reopen the 100 mm row, which is the best point on the
sweep at 2.376. It needs a datasheet.

## What week 2 established, beyond the freeze

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
all three green. `tools/check.py` was changed through week 2 and never loosened: four gates
after the first audit, the single stacked thrust to weight gate replaced by six, a narrow
measured-family exception on the coefficient floor, three document gates for D32 and four for
the week 4 conservative column. 104 self-tests.

## Open items

- **Week 4 owns a 68.5 g mass target.** If the refined budget cannot reach 623.9 g on the
  stacked case, that is a blocked trigger and a human decision, not a trimmed allowance. Week 4
  also builds its conservative column line by line under D33, and restates the stacked figure in
  the three week 2 design documents when the mass moves, under D34
- **`.claude/weekly-loop.md` describes the week 2 thrust to weight gate in its pre-D30 form**,
  at the paragraph about what the arithmetic gate checks. Its blocked triggers are current and
  correct. The config belongs to a person, so week 2 reported this rather than editing it
- **Working solo**, confirmed 27 August. Weekly hours still unstated, which matters because
  there is nobody to absorb a slipped week and week 2 already used two of its slots
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
something has to slip, slip this one. Week 5 is 4 days and carries the deadline, so weeks 3 and
4 do not get to overrun into it. Week 2 has already spent two ticks on one week, so the
calendar has no slack left in it.
