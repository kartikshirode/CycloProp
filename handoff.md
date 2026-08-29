# CycloProp handoff

Updated 26 August 2026. Stage 1 is due **27 September 2026** and we submit on 26 September. This file is where a fresh session starts.

NEXT-WEEK: 2

## Read these first, in order

1. **[context.md](context.md)** is the authority on what the competition requires. It was built from the official problem statement PDF and it outranks everything else in the repo, including this file
2. **[stage-1/plan.md](stage-1/plan.md)** is the week by week execution plan
3. **[stage-1/literature.md](stage-1/literature.md)** is the technical input: verified parameter table, published mass breakdowns, power loading, first-cut sizing
4. **[stage-1/decisions.md](stage-1/decisions.md)** is what has been frozen and why

`brief.md`, `_shared-timeline.md` and `_plan-review-round1.md` are earlier work kept as history. They were written from page summaries and contradict `context.md` in several places. When they disagree, context.md wins.

## Where we are

Week 1 of 5 is done. Week 2 is next and starts 2 September.

Week 1 delivered the requirements document and the literature rebuild. It also found the official problem statement, which nobody had located before, and that moved several things enough that the plan was restructured around it. Full account in [stage-1/progress/week-1.md](stage-1/progress/week-1.md).

Nothing is sized yet. Week 2 does that, and it is no longer blocked.

## What the problem statement settled

**The thrust-to-weight basis is settled.** The PDF says the ratio is measured on "the complete cyclorotor module, including rotor blades, frame, pitch mechanism, motor, actuator, and associated mounting hardware". That was the one question holding up sizing. Nothing on that list can be pushed onto an airframe to make the number work.

408 g follows from it, but only at exactly 10 N, and the requirement is at least 10 N. See the ceiling table below.

**Stage 1 wants 7 items, not 5.** Every document here said five. The three that were wrong or missing: power as a named deliverable, thrust-to-weight as a stated result separate from the mass budget, and a team capability and execution plan.

**Thrust vectoring is required and carries 15%.** It had never been mentioned in this repo. At Stage 1 it has to be demonstrated through kinematic and performance analysis, so an argument and a number, not hardware.

**Eight evaluation criteria, not nine**, summing to 100. Five of them carry 15% each and four of those five are engineering analysis.

## How this gets executed

Under `/loop` with the `weekly-loop` skill, one tick per plan week, config at [.claude/weekly-loop.md](.claude/weekly-loop.md). Gates are mechanical and run by the supervisor, not self-reported: `python tools/check.py --week N`.

The gates are not decorative. Every number in the submission is defined once in `stage-1/design/numbers.json`, prose cites it through a `## Numbers used` block, and the gate recomputes thrust from the geometry, weight from the mass lines and T/W from both. Writing a flattering number into prose fails the week.

They are also not sufficient on their own, which took a goal-based review to establish. Agreement between stored numbers is not feasibility: the gates once certified 13.5 N of thrust from 1 W of aerodynamic power, and a structural model with 1 g blades sitting beside a 108 g blade budget. Week 2 now has a momentum floor under its power estimate and week 4 derives its structural loads from the design. Decisions D9 and D10 carry the reasoning.

Human checkpoint every 2 weeks. **The submission email is never sent by an agent**, nor is the team registered or real names written into the capability section. Those are blocked triggers in the config.

Never run a loop longer than 7 to 8 hours. Past that the increment per cycle collapses.

## Before week 2: the human gate

Week H in the plan, with the task list and the status markers in [stage-1/human-gate.md](stage-1/human-gate.md). Not a loop tick.

Registration, the eligibility check, the roster and naming who sends are a **hard block on week 5**, which cannot write a real capability section or stage a submission without them. They are advisory before week 2, because the engineering does not depend on the roster. The faculty supervisor and the weekly-hours figure are wanted early but block nothing; they change what Stage 2 can promise and how much the schedule can be trusted.

Do the eligibility check first regardless. An ineligible roster makes every other week wasted effort, and the clause bites at any stage, including after results.

## Week 2, next up

Configuration, rotor sizing, thrust, power, and the feasibility envelope that decides whether this closes at all.

- **Design thrust is a choice, not 10 N by default.** The mass ceiling moves with thrust: 407 g at 10 N, 489 g at 12 N, 530 g at 13 N. Every earlier document here treated 408 g as fixed, which it is not, and 408 g fails the strict inequality anyway
- Default to the Texas A&M UAV-scale optimum, meaning 3 blades at c/R 0.66, blade aspect ratio 4, NACA 0020, plus or minus 40 degrees, because solving that shape family pins Reynolds near 100,000 and that sits inside the band they studied
- Radius trades rpm, envelope, structural mass **and power**. Within a fixed shape family at fixed thrust, aerodynamic power goes roughly as 1/R, so radius is not power-neutral
- Bound the 0.607 thrust coefficient rather than adopting it. It comes from a different blade count, airfoil, solidity and Reynolds number
- Single versus clustered has to be compared properly, on the module boundary. D2 only proved that copying one published rotor five times fails

**Geometry freezes only if the conservative case closes.** If a low coefficient and a high mass together miss T/W 2.5, that is a finding, not a reason to trim an assumption.

## The number that decides this project

Re-cut onto the competition's module boundary, the closest published designs give a module thrust-to-weight of **1.69 and 1.80**. We need 2.5, so the gap is 39 to 48 percent over the state of the art, and it is further from published work than anything else in the brief.

The earlier "rotor is 37 to 48 percent of all-up weight" benchmark measured against whole-aircraft mass including battery and avionics, which the module boundary excludes. It was not comparable and should not be used for budgeting.

This is survivable, but the argument is narrower than it was. External research settled the piece D8 could not: blade mass per newton is scale invariant and blade stress climbs, so **scale buys aerodynamic efficiency and nothing on blade mass**. What is left is the non-blade fixed masses, bearings and fasteners and ESC and linkage and motor, amortising over five times the thrust, plus materials. Week 2 makes that case in those terms and drops the scale-shrinks-blade-mass claim, which the record contradicts. Decisions D8 and D11 and [stage-1/literature.md](stage-1/literature.md) carry the working.

Early test worth running first in week 2: if the non-blade fixed masses cannot come in under roughly 40 percent of the mass ceiling at the chosen thrust, this does not close at that radius.

## Open items

- **Working solo.** Confirmed 27 August. More people are available if the work needs them, but the plan should assume one person until that changes. Weekly hours are still unstated, which now matters more than it did, because there is nobody to absorb a slipped week
- **Two papers to pull in a browser, and both are open access.** Scripted fetching fails on Cloudflare, so these need a human with a browser and about five minutes:
  - **Kellen 2019**, Texas A&M handle 1969.1/184958, the thesis behind our whole baseline geometry. Wanted from the body: the measured blade-area thrust coefficient, power loading in N/W, per-rotor thrust and the rpm at the optimum. **Getting the coefficient would retire most of the project's second-biggest risk**, since it is the same shape family in the same Reynolds band
  - **Runco and Benedict 2023**, IJMAV 15, DOI 10.1177/17568293231189999. Wanted: thrust per rotor, because the research return quotes 10 gf per rotor and 68 gf total on a 4 rotor vehicle, and those disagree. The module T/W re-cut is 1.22 on one reading and 2.07 on the other, which is the difference between the gap widening and nearly closing
- **Registration, team confirmation and the eligibility check** are human tasks and none are done. The eligibility clause disqualifies a whole team at any stage, including after results, so check every member before the team is fixed
- **A faculty supervisor** is still needed, both for the Stage 2 CAE tool access and because the problem statement's preference list reads like a spec for the team capability section
- [stage-1/organiser-email.md](stage-1/organiser-email.md) is mostly answered by the problem statement now and should be cut down or dropped
- Round 2 of the plan cross-check is done. 11 findings, 4 of them blockers, all addressed; the plan was restructured around them. Prompt kept at [_codex-review-prompt.md](_codex-review-prompt.md) if a round 3 is wanted

## Standing risk

Week 3 collides with the UAV-X comms layer, which is the highest-risk piece across both projects. If something has to slip, slip this one. Week 5 is only 4 days and carries the deadline, so weeks 2 to 4 do not get to overrun into it. Each has a written fallback in the plan.
