# CycloProp handoff

Updated 31 August 2026. Stage 1 is due **27 September 2026** and we submit on 26 September.
This file is where a fresh session starts.

NEXT-WEEK: 4

Weeks 1, 2 and 3 are done. Geometry froze in week 2 and the mechanism froze in week 3. Week 4 is
structure, mass, materials and manufacturing, and it is the second heavy week.

## Read these first, in order

1. **[context.md](context.md)** is the authority on what the competition requires. Built from
   the official problem statement PDF, and it outranks everything else here including this file
2. **[stage-1/plan.md](stage-1/plan.md)** is the week by week execution plan
3. **[stage-1/progress/week-3.md](stage-1/progress/week-3.md)** is where the design stands and
   what week 4 inherits. [week-2.md](stage-1/progress/week-2.md) is still the mass and
   feasibility record
4. **[stage-1/decisions.md](stage-1/decisions.md)** is what has been frozen and why. 45 entries.
   D30 unblocked week 2, D35 closed the stacked case, D38 to D45 are week 3, and D45 is the
   audit response that corrects four figures inside D38, D40, D42 and D44
5. **[stage-1/design/evidence-ledger.md](stage-1/design/evidence-ledger.md)** is what every
   number rests on and how strong it is
6. **[stage-1/audit/week-3.md](stage-1/audit/week-3.md)** is the week 3 fresh-context audit,
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

Four thrust to weight cases, and all four are reported everywhere because reporting one of them
is how week 2 confused itself for a fortnight:

| Case | Thrust | Mass | T/W |
| --- | --- | --- | --- |
| design point | 18.00 N | 580.1 g | 3.163 |
| mass downside alone | 18.00 N | 692.4 g | 2.650 |
| coefficient downside alone | 17.10 N | 580.1 g | 3.005 |
| both stacked | 17.10 N | 692.4 g | 2.517 |

All four clear the hard limit of 2.5. Read the stacked row as a thin pass rather than a
comfortable one: it clears by 4.8 g, with the conservative column at 692.4 g against a 697.2 g
ceiling. The hard version of that test runs in week 4 against a refined budget, under D30 and
D33. Week 3 did not move a single mass line.

The internal 2.75 target from D17 is still unmet and still not claimed. It wants the
conservative column at 633.8 g, so the gap is 58.6 g. That is a target and not a limit.

## What week 4 does, and the four things it inherits

Final material allowables and blade stiffness, structural loads and the full load path, the mass
budget and BOM, and the thrust to weight reconciliation. Required items 5 and 6.

**1. Two mass decisions that both push the wrong way.** The blade centre of mass sits at 39.92
percent chord against a pitch axis at 30 percent. Unbalanced, the peak blade pitching moment is
2.1201 Nm and the pitch link takes 101.82 N; balanced, those fall to 1.0139 Nm and 69.38 N.
Balancing costs mass. Separately, the sector gear and ring gear that couple the servos to the
phasing carrier are not named in the week 2 pitch mechanism line's stated basis, so either they
fit inside that line or the line grows. Both land on a conservative column with 4.8 g of room.
See D43.

**2. The shaft stops short and the drive is single ended.** The pitch links sweep through the
rotor axis, so the plane they move in cannot contain the shaft. Belt on one end, phasing carrier
on the other. A shaft stiffness problem cannot be answered by running the shaft through to an
outboard bearing on the mechanism side. See D40.

**3. Structural loads that are already computed and are week 3's, not week 4's, to change.**
Pitch link 101.82 N, blade pitching moment 2.1201 Nm, carrier torque 0.1371 Nm, offset strut
47.48 N radial, instantaneous lateral blade force 10.10 N. Peak to mean from the rerun load
model is 2.501 and week 4 still sizes on 4.0 under D16.

**4. The drive rows.** Pack voltage sits outside the module boundary, so cell count costs the
module nothing. Motor torque goes as current over KV and speed as KV times voltage, so their
product is power and has no KV in it. Week 2 fixed KV450 on 6S and then searched only the belt
ratio, which imposed a constraint the motor's power rating does not. A lower KV variant on more
cells would reopen the 100 mm row, which is the best point on the sweep at 2.376. It needs a
datasheet, and so do four of the five motor rows and the servo.

## Still worth a human doing, in this order

**1. Week H.** All five markers pending. It hard blocks week 5 and nothing else, and it now has
the longest lead time of anything in the project. Eligibility first, because the clause
disqualifies a whole team at any stage, including after results are announced.

**2. The two organiser questions**, page limit and registration reference format, were due by 2
September and are unsent. If no answer arrives by 8 September, use a 15 page main body plus
cited appendices.

**3. Ramsey 2022 and Heimerl.** Ramsey would give a second structural mass anchor; there is
currently one, Runco, four orders of magnitude smaller. Heimerl measured instantaneous blade
forces across Re 30,000 to 100,000 and would replace two estimates with measurements: the peak to
mean blade load, and the side force angle against pitch offset. Both feed week 4 directly.

## What week 3 established

- **The mechanism is real and it is reproducible.** `tools/linkage.py` solves the four-bar,
  writes `numbers.json` under `--write`, and `tools/test_gates.py` recomputes the loop closure on
  every published pitch row. A hand-edited row or a target cosine both fail it
- **Kellen's link ratio does not carry across and his horn ratio does.** 105 mm rather than 111.6
  takes the carrier torque from 0.3240 Nm to 0.1371 Nm and opens the transmission angle by 18
  degrees. The sweep is in the script under `--sweep`. See D38
- **The week 2 load model was rerun, not replaced.** It reconstructs to 5.2e-5 N on all 36 of its
  published rows before the schedule changes, so the comparison is like for like. See D41
- **Side force is the open risk and it is stated as one.** The model gives 0.98 degrees of
  aerodynamic tilt; measurement gives 10 to 35 for the whole tilt and rising with rpm. The design
  carries an indexed bias plus bench trim, and the uncertainty costs up to 25 of the 120 degrees
  of authority
- **The vectoring gate now tests the force map.** Comparing `vector_range_deg` with
  `phase_authority_deg` only checked that the same number was written twice. Six new checks, two
  new required fields and seven new attack cases. See D42 and D45

## The human gate

All five markers in [stage-1/human-gate.md](stage-1/human-gate.md) are still pending. They were
advisory before week 2, the engineering did not depend on them, so weeks 2 and 3 ran. They are a
hard block on week 5, which cannot write a real capability section or stage a submission without
them. `07-team-and-execution.md` does not exist yet for the same reason.

Do the eligibility check first regardless. The clause disqualifies a whole team at any stage,
including after results are announced, so an ineligible roster makes every other week wasted
effort.

## Standing constraints

**The submission email is never sent by an agent.** Nor is the team registered, nor are real
names written into the capability section. Those are blocked triggers in the loop config and
they do not move.

Gates are run by the supervisor in its own shell and never taken from the week-agent's report:
`python tools/check.py --week N`, `--global`, and `python tools/test_gates.py`. Week 3 leaves all
three green. `tools/check.py` has never been loosened: week 2 added four gates after the first
audit, six thrust to weight gates, a measured-family exception on the coefficient floor and
seven document gates; week 3 added four force map checks and two lateral load checks, then two
more required fields after its audit. 117 self-tests.

## Open items

- **Week 4 owns a 58.6 g margin gap, not a compliance gap**, and now owns two candidate mass
  additions against it: the blade balance mass and the servo to carrier gear pair. The stacked
  case clears 2.5 at 2.517 by 4.8 g. Falling under 2.5 on the refined budget is a blocked
  trigger; missing the 2.75 target is a margin decision
- **The three per revolution carrier ripple is not bounded.** 0.1371 Nm at 120 Hz sits above any
  servo's control bandwidth. The static margin of 2.36 covers it, and the phase jitter needs a
  real servo gearbox ratio and rotor inertia
- **Working solo**, confirmed 27 August. Weekly hours still unstated, which matters because there
  is nobody to absorb a slipped week and week 2 already used two of its slots
- **The 0.80 continuous derate has no source.** T-Motor publishes a 180 second maximum and the
  problem statement states no endurance requirement, so the derate is a judgement. A stated hover
  duration would turn it into a calculation
- **Four of the five motor rows came from supplier listings**, not datasheet PDFs, and the servo
  is now a fifth. Only the MN5006 was read off a manufacturer's sheet
- **The coefficient reserve is deliberate and must stay unspent.** 0.6055 sits below all three
  measured or corrected values available: Kellen at 0.6648, the corrected Benedict quad at
  0.7211, the twin at 0.8114. No later week may recompute thrust upward off those without a new
  decision entry. See D36
- **`largest_dimension_mm` in the week 2 tables is 290 mm** and the packaged module is 364.4 mm.
  The week 2 comparison is unaffected because it applied one rule to all three layouts. See D44
- [stage-1/organiser-email.md](stage-1/organiser-email.md) is mostly answered by the problem
  statement now and should be cut down or dropped

## Standing risk

Week 3 collided with the UAV-X comms layer and came through. Week 5 is 4 days and carries the
deadline, so week 4 does not get to overrun into it. Week 2 already spent two ticks on one week,
so the calendar has no slack left in it. The draft PDF build is done and green, which takes one
known unknown out of the final four days.
