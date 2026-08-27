# CycloProp Stage 1 plan

Execution plan, one week per loop tick. Requirements live in [../context.md](../context.md) and technical inputs in [literature.md](literature.md). This file only says what gets done when, and how a machine decides whether it happened.

**Deadline 27 September 2026, submitting 26 September.** Email to pushpak_gc2026@aero.iitb.ac.in.

Revised 26 August after the round 2 review. What changed: mass and power feasibility moved into week 2 so geometry no longer freezes before anyone knows the module can close, two rubric criteria that had no home got sections, and the human steps that were sitting unscheduled at the end got a gate of their own before week 2 starts.

## How this plan is executed

Driven by the `weekly-loop` skill under `/loop`. One tick runs one week through a fresh agent, then the supervisor runs the gates in its own shell. Config at [../.claude/weekly-loop.md](../.claude/weekly-loop.md).

Rules that make the weeks machine-checkable:

- Every number the submission states lives in `stage-1/design/numbers.json` and nowhere else. Prose cites it through a `## Numbers used` block. The gate recomputes the arithmetic and fails on disagreement
- **Hard limits are applied to recomputed values, never stored ones.** Thrust comes from the geometry, weight from the mass lines, T/W from both. Writing a flattering headline number does nothing
- Weeks are cumulative. `--week 4` reruns weeks 1 to 3, so week 4 cannot pass by breaking week 2
- A week is done when `python tools/check.py --week N` exits 0
- The gates have their own test suite at `tools/test_gates.py`, which builds throwaway trees and checks that an honest design passes and eleven specific attacks fail. Run it if you change `check.py`

## The target is not exactly 10 N

The requirement is thrust **at or above** 10 N with T/W above 2.5. Those two together set the mass ceiling, and the ceiling moves with thrust:

The ratio has to be strictly greater than 2.5, so these are floors rounded down, not the rounded figures the repo used to quote. 408 g at 10 N actually fails, since the exact ceiling is 407.75 g.

| Design thrust | Safe mass ceiling for T/W > 2.5 |
| --- | --- |
| 10 N | 407 g |
| 11 N | 448 g |
| 12 N | 489 g |
| 13 N | 530 g |
| 15 N | 611 g |

The old plan treated 408 g as a fixed requirement, which pinned the design to the most constrained corner of the feasible region. It is not a requirement, and taken literally it is not even inside it.

Designing above 10 N is a real lever, though not a free one. Power rises, and the margin a paper design has to carry eats into what the extra thrust buys. Power has no separate weighted criterion, but it is a named Stage 1 deliverable and it feeds the motor, battery and thermal case, so it is not free either. Week 2 picks the design thrust deliberately and says why.

## Calendar

| Week | Dates | Days | Covers |
| --- | --- | --- | --- |
| 1 | 26 Aug to 1 Sep | 7 | Requirements and literature. Done |
| H | by 1 Sep | human | Registration, eligibility, roster, tool access |
| 2 | 2 to 8 Sep | 7 | Items 1, 2, 4. Configuration, sizing, thrust, power, feasibility envelope |
| 3 | 9 to 15 Sep | 7 | Item 3 plus thrust vectoring and packaging |
| 4 | 16 to 22 Sep | 7 | Items 5, 6 plus structural loads and strength |
| 5 | 23 to 26 Sep | 4 | Item 7, assembly, PDF, staged for a human to send |

Week 5 is the short one and it carries the deadline, so weeks 2 to 4 do not get to slip into it. Each has a fallback below that trades depth rather than pushing work forward.

Runs alongside UAV-X. Week 3 collides with the UAV-X comms layer. If one has to give, this one gives, because writing compresses under pressure and debugging does not.

---

## Week 1: requirements and literature

**Status: done, 26 August 2026.** Delivered [../context.md](../context.md) and [literature.md](literature.md), and recovered the official problem statement. Progress at `stage-1/progress/week-1.md`.

---

## Week H: the human gate, before week 2 starts

Not a loop tick. These are things an agent must not do and the plan previously left sitting in week 5 with four days to go.

1. **Register** the team on techfest.org under Competitions, then PUSHPAK Grand Challenge
2. **Check eligibility for every member.** Nobody attached to the PUSHPAK Project, the Drone Centre, or the organising and host institutions. This disqualifies an entire team at any stage, including after results are announced
3. **Fix the roster** and collect what each member actually brings, against the preference list in the problem statement. Week 5 writes the section around real names and real capability, and cannot invent either
4. **Line up the faculty supervisor**, and with them the Stage 2 CAE tool access
5. **Name who sends the submission** on 26 September, and confirm they will be reachable
6. **State real weekly hours available.** The schedule is unvalidated without this and it is the cheapest thing here to fix

**One policy, stated once so the config and the handoff can match it.** Items 1, 2, 3 and 5 are a **hard block on week 5**, which cannot write a real capability section or stage a submission without them. They are **advisory before week 2**, because the engineering genuinely does not depend on the roster.

So: if week H is not done by 1 September, week 2 runs anyway and the loop records the gap. If it is not done by 23 September, week 5 stops and reports BLOCKED. Item 2, eligibility, is the one worth doing first regardless, because an ineligible roster makes every other week wasted effort.

---

## Week 2: configuration, sizing, thrust, power, feasibility

Covers required items 1, 2 and 4, and settles whether the design closes at all.

**Scope files:** `stage-1/design/01-configuration.md`, `02-rotor-sizing.md`, `04-thrust-and-power.md`, `numbers.json`, `stage-1/decisions.md`

### Tasks

1. **Compare single against clustered properly**, under a heading called "Why this configuration" rather than one that presumes the answer. Decision D2 currently rests on the observation that copying one published rotor five times needs 485 g of rotor alone. That rules out copying, not every multi-rotor layout. Compare a single larger rotor against a redesigned two and three rotor cluster on the same component boundary, the same coefficient assumptions and the same power model, then freeze the configuration. Use the module boundary the problem statement defines, not published all-up aircraft mass, which includes battery and avionics we are not carrying.
2. **Choose the blade shape family.** Texas A&M UAV-scale optimum is 3 blades at c/R 0.66, blade aspect ratio 4, NACA 0020, plus or minus 40 degrees. Benedict's MAV optimum is 4 blades at c/R 0.433, NACA 0015, asymmetric 45 top and 25 bottom. Our Reynolds number lands in the Texas A&M band, so that is the default.
3. **Bound the thrust coefficient, do not just adopt it.** The 0.607 anchor comes from a 4-blade NACA 0010 rotor at c/R 0.433 and Re near 35,000. Moving it to 3 blades, NACA 0020, c/R 0.66 and Re near 100,000 changes blade count, solidity, airfoil and Reynolds number all at once. Derive a defensible low value from the spread in the published data and record both. Benedict's own results give the direction of several of these effects, so use them rather than guessing a percentage.
4. **Sweep radius against power, not just rpm.** Within a fixed shape family at fixed thrust, tip speed goes as 1/R, so aerodynamic power goes roughly as 1/R. Radius changes the motor, the thermal load and the mass, not only the envelope. Compute power for at least three candidate radii and record the sweep.
5. **Compute thrust two ways** and report the gap. Coefficient scaling, plus a momentum estimate with its closure assumption stated. A momentum calculation without an independent closure is a bound, not a second opinion, and should be labelled as one.

   The gate now treats it as exactly that. Aerodynamic power has to sit at or above the momentum bound computed over a declared `momentum_area_m2`, which may not exceed the projected frontal area of 2R times span, and the figure of merit that falls out has to land between 0.20 and 0.75. Nothing else in week 2 asks whether the thrust and power pair could exist: without this the gate certified 13.5 N produced by 1 W. The second opinion is the published power loading route, which is an independent closure rather than the same equation rearranged, and the two have to agree within 35 percent.
6. **Build the whole-module mass envelope now, at line-item level but coarse.** Blades, frame, pitch mechanism, motor, actuator, mounting. Week 4 refines it. Week 2 only has to answer whether it can close. Give each line a distinct name, because every week 4 budget line has to point back at one of them by name.
7. **Pick the design thrust** using the ceiling table above, and say why. Then freeze a `thrust_sensitivity` table of at least three candidates, each carrying its mass ceiling, its ideal power, its rpm and what it does to the motor and the structure. Raising thrust is not a free knob on the numerator of T/W: going from 10 N to 13 N buys 30 percent more mass ceiling and spends 14 percent more rpm, 30 percent more centrifugal load and 48 percent more ideal power, which can move the motor, the transmission, the thermal case and the structure together. Week 4 may only pick a row from this table, so the sensitivity has to be worked here, where there is time for it.
8. **Add rotor tare, transmission, actuator and controller draw** to module power. The published power loading figures are blade aerodynamic power on a rig whose structure power was a tenth of the total, so tare is not already included.

### Done when

`python tools/check.py --week 2` exits 0. Beyond the file and heading checks it recomputes tip speed, Reynolds, thrust and conservative thrust from geometry, requires the conservative coefficient to actually be lower than the nominal one, requires **both** the nominal and the conservative recomputed thrust to clear 10 N, requires the conservative mass at conservative thrust to still clear T/W 2.5, and requires the power sweep to cover at least three radii. The sweep also has to pass through the design point: the row at the chosen radius must carry the same aerodynamic power the rest of the week uses, or the curve is a different curve that happens to have the right shape.

### Decision gate

**Geometry freezes only if the conservative case closes.** If the conservative coefficient and the conservative mass together fail T/W 2.5, geometry does not freeze and the week has produced a finding rather than a design.

**Fallback, in order:** raise design thrust toward the ceiling table; move to a larger radius, which lowers power and rpm; revisit the shape family. If none of the three closes, stop and report. A Stage 1 submission that honestly reports the module is infeasible at this scale is worth more than one that reaches 2.51 by rounding, and the reviewers know the literature better than we do.

**Carry two candidate radii forward** rather than one. Be honest about what that buys: it saves week 2's exploration if the first choice fails, but it does not save week 3, because link lengths, offset geometry, the pitch schedule and gearing all move with radius. Switching radius after week 3 still costs a week 3 rerun. The second candidate is insurance against a week 2 mistake, not a free option in week 4.

---

## Week 3: pitch, thrust vectoring, packaging

Covers required item 3, the thrust-vectoring requirement at 15%, and the integration half of the 5% packaging criterion.

**Scope files:** `stage-1/design/03-pitch-and-vectoring.md`, `09-packaging-and-integration.md`, `numbers.json`, `stage-1/decisions.md`

### Tasks

1. **Choose active or passive and justify it.** Passive four-bar is the default on mass evidence, since every flying cyclocopter in the read literature uses one and none use per-blade servos.
2. **Work the four-bar kinematics.** Link lengths, pitching axis, and the offset that produces the chosen amplitude, for the frozen geometry.
3. **Produce the pitch schedule** as computed values across the revolution, not a sketch. It has to show motion: reach the stated amplitude in both directions, travel peak to peak by roughly twice the amplitude, and close on itself over a revolution. A table that spanned 360 degrees with zero pitch at every azimuth used to pass, and that is not evidence of a mechanism.
4. **Quantify the phase delay.** Peak pitch does not land exactly at 90 and 270 degrees, and that is where the side force comes from. The stated delay has to be the one the schedule shows, within 10 degrees of where the table actually peaks, and the schedule has to track the harmonic model it claims to follow to a stated RMS residual.
5. **Thrust vectoring, quantified.** Offset magnitude sets amplitude, offset direction sets phase, phase steers the vector. Give the achievable range in degrees and what actuates it, and state the mechanism's phase authority separately: the range is the authority, so a claimed 360 degrees of vectoring on a linkage that can only drive 90 degrees of phase now fails rather than passing as an assertion. This answers a 15% criterion, so it gets the most care in the week.
6. **Handle the side force.** Predict the resultant tilt, benchmark against the 30 degrees Benedict measured, and state the correction.
7. **Package envelope and interfaces.** Overall dimensions, mounting scheme and mount count, drivetrain arrangement from motor through transmission to shaft, and the electrical and mechanical interfaces the module presents to an airframe. Dimensioned sketches and a table, no CAD.

### Done when

`python tools/check.py --week 3` exits 0, cumulatively with weeks 1 and 2. Checks both files, requires the pitch schedule to have 24 or more **distinct** azimuths spanning at least 300 degrees, and requires a non-zero actuator count and a real package envelope.

### Decision gate

Active or passive freezes here, and actuator count and mass go to week 4.

**Fallback:** trim the depth of the packaging narrative and the interface table, which is where the least score sits. Do not defer the phase delay, which the gate requires as a number and which falls straight out of the four-bar analysis once the kinematics exist. Do not defer the vectoring section or the envelope either, since between them they carry 20% of the rubric.

---

## Week 4: structure, mass, thrust-to-weight, materials, manufacturing

Covers required items 5 and 6, plus the 15% structural criterion that had no section before.

**Scope files:** `stage-1/design/05-mass-and-tw.md`, `06-materials-and-manufacturing.md`, `08-structure-and-loads.md`, `numbers.json`, `stage-1/decisions.md`

This is the heaviest week, but the geometry and mechanism are frozen by now, so it is execution rather than exploration. The three files run in order, because loads size the structure, the structure sets the mass, and the mass decides T/W.

### Tasks

1. **Load cases and strength.** Centrifugal load on the blade at design speed, blade root bending from aerodynamic and inertial load, shaft torque from the power and speed already fixed, and the pitch link load. Analytical, closed form, with the assumptions written down. No FEA, and none is expected at Stage 1.

   Every one of these is derived from the design, not asserted beside it, and the gate recomputes three of them. Per-blade mass is the blade mass budget divided by the blade count, so a 1 g blade cannot sit next to a 108 g blade budget. Rotor shaft torque is shaft power over rotor angular speed, which is the first thing a reviewer recomputes and takes about ten seconds. Blade root bending is thrust per blade times a declared lever arm times a declared peak-to-mean load factor. State which shaft each torque refers to and give the transmission ratio, because torque upstream and downstream of a reduction are different numbers.
2. **Margins.** Each load case against an allowable for the chosen material, with a stated safety factor. Margins below 1.5 fail the gate. The pitch link gets a demand, an allowable and a margin like everything else.
3. **Component mass budget.** Every line the problem statement names, plus bearings, shaft, hub, ESC and fasteners. Each line carries a basis, meaning a measured analogue, a material calculation or a supplier figure. The gate rejects one-word bases. Each line also names the week 2 envelope line it refines, through a `refines` field holding that line's name. Several budget lines may refine one envelope line, which is the normal case: a coarse "motor and drive" turns into a motor, a hub, a shaft and bearings.
4. **Compute T/W nominal and conservative** and state the margin against 2.5.
5. **Material selection tied to the load cases**, not chosen first and justified after.
6. **Manufacturing route per part**, with Indian sourcing where it exists, since indigenous development is the point of the programme.
7. **Bill of materials with indicative costs.** Cost realism sits in the same criterion as manufacturability.

### Done when

`python tools/check.py --week 4` exits 0, cumulatively. It sums the mass lines and rejects any that vanish or carry a thin basis, recomputes weight and both T/W values, requires the conservative mass not to be lighter than the budget, recomputes the centrifugal load from blade mass, speed and radius, recomputes per-blade mass, shaft torque and blade root bending from the design, and requires all three structural margins to be at least 1.5.

Continuity with week 2 is checked per component, not just on the total. Each envelope line has to stay within 25 percent of what the budget lines refining it add up to, and no envelope line may end up with nothing refining it. Comparing totals alone let the whole budget move into the blades while every other component shrank to the smallest legal line, because the sum came out the same.

### Decision gate

If the refined budget breaks T/W, the second radius from week 2 is available, but taking it **invalidates weeks 3 and 4** because link lengths, offset geometry, pitch schedule, gearing and centrifugal load all move with radius. With four days left after week 4 that is not recoverable, so treat it as a last resort and trigger it on day 2 of the week or not at all. That is exactly why the feasibility envelope moved into week 2.

The cheaper fallbacks, in order, are to **move to another row of week 2's frozen thrust sensitivity table**, then to trim the mass budget where a line has slack, then to reopen radius. Raising thrust to a point week 2 never studied is not a cheap fallback and the gate rejects it: a thrust outside the table fails, because the row carries the rpm, the ideal power and the structural loading that come with it. An unstudied increase is a rerun of week 2, not a week 4 edit.

---

## Week 5: team, execution plan, assembly, staging

Covers required item 7, then packages for a human to send.

**Scope files:** `stage-1/design/07-team-and-execution.md`, `stage-1/submission/`, `stage-1/decisions.md`

### Tasks

1. **Team capability section** against the problem statement's preference list, using the roster and capability evidence from week H. The agent writes structure and argument. **Real names, institutions and claimed capability come from the human**, and the agent must not invent them.
2. **Execution plan for Stage 2**, mapped onto the 11 items Stage 2 demands, with the CAE tool access named.
3. **Assemble the submission** with all 7 required items as top-level sections in the problem statement's order, plus a map at the front showing which section answers each of the 8 criteria.
4. **Build the PDF.** `pandoc` and `xelatex` are both present on this machine. The attachment is what gets evaluated, not the markdown.
5. **Final consistency pass.** Every number traced to `numbers.json`.
6. **Draft the email**, naming the attachment, and stage everything. **Do not send.** A human sends it on 26 September.

### Done when

`python tools/check.py --week 5` exits 0, cumulatively. Requires all 7 items as real top-level headings, a criteria map that is an actual table with all 8 criteria in its rows, a submission of substance rather than an outline, and a staged email draft naming the attachment, the organiser address and a subject line.

The PDF condition is no longer a byte count. The gate reads the attachment back with pypdf and requires it to carry this submission's seven section names and its declared values, because a file size cannot tell the difference between the right report and an unrelated one. The old wording asked for 50 kB and the earlier gate only asked for four readable pages, which between them accepted the competition's own problem statement as our submission.

Week 5 also blocks on the four markers in [human-gate.md](human-gate.md). It cannot write a real capability section or stage a submission without them.

### Decision gate

**The roster is one person and that is what the section says.** A solo entry with a credible plan and honest scope reads better in a viva than five names nobody can stand behind. Name the capability gaps and say how Stage 2 fills them, because the problem statement's preference list is a spec for this section and pretending to cover all of it is the failure mode.

---

## Standing risks

**The highest-risk assumption is the thrust coefficient transfer.** The 0.607 anchor is a single measured point on a rotor with a different blade count, airfoil, solidity and Reynolds number. Everything downstream scales off it. Week 2 bounds it rather than adopting it, and the conservative case has to close on its own, which is the only real defence available without a wind tunnel.

**The published benchmark is worse than tight.** Re-cut onto the competition's module boundary, the closest published designs give a module thrust-to-weight of 1.69 and 1.80, and both exclude mounting hardware neither paper breaks out. We need 2.5, so the gap is 39 to 48 percent over the state of the art, and it is further from published work than anything else in the brief. The case for closing it rests on scale, on fixed masses amortising over more thrust, and on these being flying demonstrators rather than mass-optimised modules. Week 2 makes that case quantitatively or reports that it cannot. Full working in [literature.md](literature.md) and decision D8.

**Three papers are still unread**, one of them the only study in our Reynolds band. If a library proxy or the faculty supervisor opens it, re-derive the shape family and record a decision entry.

**One person is doing this.** Confirmed 27 August. More people can be brought in if the work needs them. Until then every week is serial, nothing runs in parallel, and a slipped week is a slipped project. Weekly hours are still unstated.

**No CAD is required at Stage 1** and none should be built. CAD quality is scored at Stage 2 and 3.
