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

**The 408 g budget is confirmed.** The PDF says the ratio is measured on "the complete cyclorotor module, including rotor blades, frame, pitch mechanism, motor, actuator, and associated mounting hardware". That was the one question holding up sizing and it is answered. 10 N at T/W above 2.5 puts the whole module under 408 g, and nothing on that list can be pushed onto an airframe to make the number work.

**Stage 1 wants 7 items, not 5.** Every document here said five. The three that were wrong or missing: power as a named deliverable, thrust-to-weight as a stated result separate from the mass budget, and a team capability and execution plan.

**Thrust vectoring is required and carries 15%.** It had never been mentioned in this repo. At Stage 1 it has to be demonstrated through kinematic and performance analysis, so an argument and a number, not hardware.

**Eight evaluation criteria, not nine**, summing to 100. Five of them carry 15% each and four of those five are engineering analysis.

## How this gets executed

Under `/loop` with the `weekly-loop` skill, one tick per plan week, config at [.claude/weekly-loop.md](.claude/weekly-loop.md). Gates are mechanical and run by the supervisor, not self-reported: `python tools/check.py --week N`.

The gates are not decorative. Every number in the submission is defined once in `stage-1/design/numbers.json`, prose cites it through a `## Numbers used` block, and the gate recomputes thrust from the geometry, weight from the mass lines and T/W from both. Writing a flattering number into prose fails the week.

Human checkpoint every 2 weeks. **The submission email is never sent by an agent**, nor is the team registered or real names written into the capability section. Those are blocked triggers in the config.

Never run a loop longer than 7 to 8 hours. Past that the increment per cycle collapses.

## Week 2, next up

Configuration, rotor sizing, thrust and power. The plan has the task list. The shape of the answer is already visible from week 1:

- One larger rotor, not a cluster. Repeating a published MAV rotor to reach 10 N needs 485 g of rotor against a 408 g whole-module budget
- Default to the Texas A&M UAV-scale optimum, meaning 3 blades at c/R 0.66, blade aspect ratio 4, NACA 0020, plus or minus 40 degrees, because solving that shape family for 10 N pins Reynolds near 100,000 and that sits inside the band they studied
- Radius is then a free trade of rpm against envelope and structural mass. The table in literature.md runs 80 to 160 mm
- Power is 152 to 161 W aerodynamic and 230 to 250 W electrical, not the 95 W this file used to carry

Geometry freezes at the end of week 2. Week 3 needs it fixed.

## Open items

- **Weekly hours and team size are still unknown.** This is the input most likely to invalidate the schedule and the cheapest one to fix
- **Three papers unread.** The Texas A&M thesis is the only study in our own Reynolds band and the repository refuses direct requests. Week 2 leans on a summary of it whose internal consistency checks out but which has not been opened. A library proxy or the faculty supervisor would close it
- **Registration, team confirmation and the eligibility check** are human tasks and none are done. The eligibility clause disqualifies a whole team at any stage, including after results, so check every member before the team is fixed
- **A faculty supervisor** is still needed, both for the Stage 2 CAE tool access and because the problem statement's preference list reads like a spec for the team capability section
- [stage-1/organiser-email.md](stage-1/organiser-email.md) is mostly answered by the problem statement now and should be cut down or dropped
- Round 2 of the plan cross-check, by Codex, has not run

## Standing risk

Week 3 collides with the UAV-X comms layer, which is the highest-risk piece across both projects. If something has to slip, slip this one. Week 5 is only 4 days and carries the deadline, so weeks 2 to 4 do not get to overrun into it. Each has a written fallback in the plan.
