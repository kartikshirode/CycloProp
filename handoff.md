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
4. **[stage-1/decisions.md](stage-1/decisions.md)** is what has been frozen and why. 37 entries.
   D30 unblocked week 2 and D35 is the one that closed the stacked case
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
| coefficient downside alone | 17.10 N | 580.1 g | 3.005 |
| both stacked | 17.10 N | 692.4 g | 2.517 |

All four now clear the hard limit of 2.5. Geometry froze on the first three under D30, and the
stacked case joined them on 31 August when Kellen 2019 arrived: a measured coefficient of 0.6648
for this shape family retired the configuration-transfer allowance, so the low coefficient went
from 0.5147 to 0.5752 and conservative thrust from 15.30 N to 17.10 N. That is D35.

Read the stacked row as a thin pass rather than a comfortable one. It clears by 4.8 g: the
conservative column would have to stay under 697.2 g and it sits at 692.4 g. The hard version of
that test still runs in week 4 against a refined budget, under D30 and D33.

`results.mass_target_week4_g` is gone. It described a shortfall that no longer exists, and the
gate stops checking that field once the stacked case clears, so leaving it would have parked an
unchecked number in the schema.

What week 4 inherits instead is the internal 2.75 target from D17, which is still not met and
still not claimed. Reaching it wants the conservative column at 633.8 g against the 692.4 g it
holds now, so the gap is 58.6 g. That is a target and not a limit.

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

**2. Done. Kellen 2019 and Benedict 2010 are both read**, retrieved from the Wayback Machine on
31 August after the live OAKTrust route stayed behind its Cloudflare challenge and DRUM served a
maintenance page. `reference/README.md` has the two URLs that worked and a curl line for each.
The PDFs are 52 MB together so they are not committed; the text extracts and the sha256 of each
PDF are.

What came out of them: D35 retired the configuration-transfer allowance and closed the stacked
case, D36 corrected the provenance of the nominal coefficient and held it at 0.6055 anyway, and
D37 narrowed D25 on the Reynolds axis. E4, E5 and E17 in the evidence ledger moved from summary
to measured, and E18 and E19 are new.

**3. The drive, at week 4.** Pack voltage sits outside the module boundary, so cell count costs
the module nothing. Motor torque ceiling goes as current over KV and speed ceiling as KV times
voltage, so their product is power and has no KV in it. Week 2 fixed KV450 on 6S and then
searched only the belt ratio, which imposed a constraint the motor's power rating does not. A
lower KV variant on more cells would reopen the 100 mm row, which is the best point on the
sweep at 2.376. It needs a datasheet.

## What week 2 established, beyond the freeze

- **The single rotor beats a redesigned cluster.** 2.517 against 1.855 for two rotors and 1.479
  for three, on one common model with every contested assumption set in the cluster's favour.
  D2 was provisional since week 1 and is now settled. See D18
- **The 0.6055 coefficient reproduced, and its basis did not.** The arithmetic behind it checks
  out every time. The inputs it used are not in Benedict: 1.98 N is a vehicle weight over four
  and 2000 rpm belongs to the twin. The real quad point gives 0.7211. 0.6055 is held anyway as
  deliberate reserve. See D36
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

- **Week 4 owns a 58.6 g margin gap, not a compliance gap.** The stacked case clears 2.5 at
  2.517 and clears it by 4.8 g, so the hard limit is met and the internal 2.75 target from D17
  is not. Closing that wants the conservative column at 633.8 g. Failing to close it is a margin
  decision rather than a blocked trigger; falling under 2.5 on the refined budget is still the
  blocked trigger. Week 4 also builds its conservative column line by line under D33, and
  restates the stacked figure in the three week 2 design documents when the mass moves, under
  D34
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
- **The coefficient reserve is deliberate and must stay unspent.** 0.6055 sits below all three
  measured or corrected values available: Kellen at 0.6648, the corrected Benedict quad at
  0.7211, the twin at 0.8114. No later week may recompute thrust upward off those without a new
  decision entry. See D36
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
