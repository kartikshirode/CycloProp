# CycloProp Stage 1 plan

Execution plan, one week per loop tick. Requirements live in [../context.md](../context.md) and technical inputs in [literature.md](literature.md). This file only says what gets done when, and how a machine decides whether it happened.

**Deadline 27 September 2026, submitting 26 September.** Email to pushpak_gc2026@aero.iitb.ac.in.

Revised 29 August after the execution review. The week 2 order now follows the actual
dependencies, the mass case separates fixed hardware from power-scaled hardware, and each
high-score claim has an evidence route. PDF assembly and the hostile viva check also start
before the final four days.

## How this plan is executed

Driven by the `weekly-loop` skill under `/loop`. One tick runs one week through a fresh
week-agent, then the supervisor runs the gates in its own shell. **The execution contract is
[../.claude/weekly-loop.md](../.claude/weekly-loop.md), whichever runner executes the tick.**
[../.codex/weekly-loop.md](../.codex/weekly-loop.md) defers to it and carries only its own
sentinel path. It needs one human confirmation before the first tick.

This file said the opposite until week 2 ran into it. See D24 and D28.

Rules that make the weeks machine-checkable:

- Every number the submission states lives in `stage-1/design/numbers.json` and nowhere else. Prose cites it through a `## Numbers used` block. The gate recomputes the arithmetic and fails on disagreement
- **Hard limits are applied to recomputed values, never stored ones.** Thrust comes from the geometry, weight from the mass lines, T/W from both. Writing a flattering headline number does nothing
- Weeks are cumulative. `--week 4` reruns weeks 1 to 3, so week 4 cannot pass by breaking week 2
- A week is done when `python tools/check.py --week N` exits 0
- The gates have their own test suite at `tools/test_gates.py`, which builds throwaway trees and checks that an honest design passes and eleven specific attacks fail. Run it if you change `check.py`

## How each week is broken into work packages

One tick is one week. The packages below are checkpoints inside the week-agent's turn, not
extra loop ticks and not a promise of seven fresh contexts. Read-only source extraction and
independent calculations may be delegated. Repo writes stay sequential unless isolated in
git worktrees. One subagent slot stays free for the mandatory audit at the end.

The "fills" column is the count of sub-parameters in `numbers.json` that week is
responsible for. Every one of them is gated.

| Week | Fills | Work packages | Of those, parallel |
| --- | --- | --- | --- |
| 2 | 38 scalars plus 3 tables, roughly 80 cells | 7 | 2 |
| 3 | 13 scalars | 6 | 2 |
| 4 | 23 scalars plus the mass budget, roughly 55 cells | 6 | 1 |
| 5 | 0, it assembles | 5 | 0 |

**Week 2**, the heaviest week and the one that decides feasibility.

1. Evidence ledger, module boundary and selection rules
2. Common shape families and single, 2 rotor and 3 rotor candidates. Needs 1
3. Thrust, azimuthal load and power model, with coefficient scenarios. Needs 2
4. Drive shortlist and preliminary blade and frame section. Both need 3 and can run in
   parallel as read-only calculations
5. Coupled configuration, radius, thrust and mass comparison. Needs both parts of 4
6. Freeze one design point, fill `numbers.json` and write the three design documents
7. Audit, including a hostile-examiner read

**Week 3.** Packaging and item 7 can move while the force map is being checked.

1. Linkage topology, loop closure and the solved pitch schedule
2. Vectoring actuator and force-vector map. Needs 1
3. Moving envelope, packaging and interfaces. Needs the linkage geometry from 1
4. Item 7 structure and the draft PDF build. **Parallel**, no force-map dependency
5. Write and reconcile the documents. Needs 1 to 4
6. Audit

**Week 4.**

1. Final material allowables and blade stiffness closure
2. Structural loads and the full load path. Needs 1
3. Mass budget, BOM and manufacturing route. Starts after 1 and can overlap the load work
4. Thrust-to-weight and margin reconciliation. Needs 2 and 3
5. Write the three design documents. Needs 4
6. Audit

**Week 5**, strictly sequential because each step consumes the last.

1. Finish item 7 specifics from week H
2. Assemble the submission with its criteria, claims and risk tables
3. Run the hostile-viva, citation and human technical-read passes
4. Build and inspect the final PDF
5. Audit, then draft and stage the email. **Never send**

Totals: 24 work packages across 4 ticks, plus the 4 supervisor runs that gate them.

## What every week ends with, without exception

The scope files listed under each week are the deliverables. These four are the protocol,
they are the same every week, and three of them are supervisor gates that fail the tick if
they are missing. A week that produces perfect design documents and skips these has not
finished.

1. **`stage-1/progress/week-{N}.md`** containing the literal line `STATUS: WEEK-COMPLETE`.
   What the week was meant to produce, what it actually produced, what changed, and what is
   carried forward as a debt
2. **`stage-1/audit/week-{N}.md`** containing the literal line `AUDIT-COMPLETE`. Written by
   the audit subagent, checking plan against delivered and documents against the actual
   diff. This is where the things the gates deliberately cannot check get caught: whether
   the prose says anything, whether a mass basis is real, whether a source carries the
   weight put on it
3. **`handoff.md`** with its `NEXT-WEEK:` line bumped to the next week number. Exactly one
   such line in the file. The supervisor greps for it and does not read around it
4. **`stage-1/decisions.md`** gets a numbered entry for anything frozen, and
   `stage-1/journal.md` a short note. Reopening an earlier decision is a new entry saying
   which one it supersedes, never an edit in place

Commit at the end of the week, split by concern, on the branch that is already checked out.

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

## The one deliverable that can move between weeks

Weeks 2 to 4 are strictly serial. Week 3 needs frozen geometry, week 4 needs the pitch
mechanism mass, and the gates are cumulative, so none of that can be reordered.

**Required item 7, team capability and execution plan, is the exception.** It needs nothing
from `numbers.json`, and the week 5 gate asks only for its three headings. Its only
dependency is week H returning the roster. It currently sits in week 5, which is the 4 day
week that carries the deadline, and that is the worst place for the one deliverable that
does not have to be there.

So: **`07-team-and-execution.md` gets its structure and its Stage 2 argument drafted from
week 3 onward**, as soon as week H returns. Week 5 then fills specifics and assembles,
rather than writing an entire required item in a week that also builds the PDF. The
specifics still come from a human. Inventing a team is a blocked trigger, and that does not
change by moving the file earlier.

Everything else that is genuinely parallel is human work: week H itself, and pulling the
three papers.

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

This plan needs about 84 focused hours after week 1: 26 in week 2, 18 in week 3, 24 in week
4 and 16 in week 5. Week H has to replace that estimate with real availability. If fewer
than 84 hours exist, run the reduced scope from the start: keep the 2 and 3 rotor branches
to a first-pass rejection table, carry one blade construction after the screen, carry one
drive after the shortlist, and compress the packaging narrative. Do not cut coefficient
sensitivity, linkage closure, the force-vector map, the mass evidence or the structural
load path. Those are the claims an evaluator will attack first.

Internal dates stop a quiet overrun:

| Date | Must be true |
| --- | --- |
| 4 Sep | Evidence ledger and coefficient scenarios fixed |
| 6 Sep | Coupled candidate comparison complete |
| 8 Sep | Week 2 decision and audit complete |
| 12 Sep | Linkage closes without singularity or interference |
| 15 Sep | Vector map, packaging sketch and first PDF smoke build complete |
| 18 Sep | Blade stiffness and refined mass budget agree with week 2 |
| 22 Sep | Week 4 decision and audit complete |
| 24 Sep | Full PDF and claims audit complete |
| 25 Sep | Human technical read complete |
| 26 Sep | Named human sends and keeps proof of sending |

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
7. **Pull the three priority papers in a browser** if access works. Save the PDFs under
   `reference/` and record the exact pages or figures used. Kellen is first because its
   measured coefficient could replace the weakest transfer in week 2. Missing papers stay
   a disclosed evidence gap, not a licence to invent their figures
8. **Ask the two submission questions by 2 September.** Page limit and file naming, then the
   registration reference format. If no answer arrives by 8 September, use a 15 page main
   body plus cited appendices and a plain registration reference in the email draft

**One policy, stated once so the config and the handoff can match it.** Items 1, 2, 3 and 5 are a **hard block on week 5**, which cannot write a real capability section or stage a submission without them. They are **advisory before week 2**, because the engineering genuinely does not depend on the roster.

So: if week H is not done by 1 September, week 2 runs anyway and the loop records the gap. If it is not done by 23 September, week 5 stops and reports BLOCKED. Item 2, eligibility, is the one worth doing first regardless, because an ineligible roster makes every other week wasted effort.

---

## Week 2: configuration, sizing, thrust, power, feasibility

Covers required items 1, 2 and 4, and settles whether the design closes at all.

**Scope files:** `stage-1/design/01-configuration.md`, `02-rotor-sizing.md`,
`04-thrust-and-power.md`, `stage-1/design/evidence-ledger.md`, `numbers.json`,
`stage-1/decisions.md`

### Tasks

1. **Build the evidence ledger before sizing.** For every value that carries a design
   decision, record the source, source status, exact page or figure when available, area
   convention, source geometry, Reynolds number and how the value is used. A summary-only
   result stays labelled summary. If Kellen is still unavailable, the low coefficient is
   an engineering downside scenario, not a published lower bound. The submission has to
   say that plainly.
2. **Fix the comparison rules before seeing a winner.** Use the official module boundary.
   Count the ESC, vectoring actuator, its controller and a full mounting allocation in the
   conservative column. Set a stated selection rule and packaging assumption because the
   brief gives no maximum rotor size. Use conservative T/W, continuous drive rating,
   largest dimension and part count as decision metrics. A larger radius lowers power but
   also lowers rpm and raises rotor torque, so power alone cannot pick it.
3. **Define common candidates.** Compare a single rotor with redesigned 2 and 3 rotor
   layouts. Give every row its rotor count, per-rotor radius and span, blade count, solidity,
   total blade area, projected area, rpm and hardware count. Add an interaction penalty for
   clustered rotors or state that the comparison assumes non-overlapping wakes. Include
   reaction torque and mounting complexity in the decision. D2 only ruled out copying five
   old rotors.
4. **Choose and bound the blade family.** The default is Kellen's 3 blade, c/R 0.66,
   aspect-ratio 4, NACA 0020 family at plus or minus 40 degrees. Recompute the 0.607 anchor
   in the same area convention. Split the low case into configuration-transfer uncertainty
   and blade-flexibility loss. Use values extracted from source figures when available. If
   they are not available, run named downside scenarios and do not call the range measured.
   Solidity stays inside 0.30 to 0.40 unless a new coefficient is derived.
5. **Add a preliminary azimuthal load model.** Use at least 24 azimuths with a prescribed
   pitch schedule, induced-flow assumption and the stated peak-to-mean load factor. Calibrate
   its cycle mean to the coefficient route. It is a load distribution and a sanity check,
   not CFD and not an independent thrust measurement. Week 3 reruns it with the solved
   linkage schedule. Show which assumptions set vertical force, side force and peak blade
   load.
6. **Sweep the coupled design, not radius alone.** For at least three radii and three thrust
   rows, carry rpm, Reynolds number, ideal and actual aerodynamic power, rotor torque,
   electrical power, largest dimension and mass. Power should fall roughly as 1/R inside a
   fixed family, while torque and structural mass may move the other way.
7. **Close power with three levels.** Coefficient scaling predicts thrust. Momentum theory
   is only a power floor over an area no larger than 2R times span. Figure of merit turns
   that floor into a working power estimate, and published power loading is the independent
   cross-check. Add rotor tare, transmission loss, actuator draw and controller draw. Name
   a motor, ESC and transmission shortlist with continuous power, speed, torque and mass
   evidence, not only assumed efficiencies.
8. **Build a coarse but physical mass envelope.** Blade mass comes from preliminary skin,
   core, spar, adhesive and end hardware geometry. Run a first beam stiffness and deflection
   check so the flexibility loss in task 4 has a real section behind it. Frame and mounting
   come from dimensions and density. Motor, transmission, bearings, ESC, actuator,
   controller, wiring and fasteners come from named hardware or a measured analogue.
   Classify each line as blade or geometry-scaled, power or torque-scaled, or fixed and
   duplicated. Do not call the motor fixed mass.
9. **Freeze the design thrust and configuration together.** Store the configuration,
   coefficient, azimuthal load, drive, radius and thrust tables in `numbers.json`. The
   `thrust_sensitivity` table has at least three rows, each with its mass ceiling, ideal
   power, rpm, torque and drive consequence. Week 4 may select a prequalified row, not
   invent a new operating point.

### Done when

`python tools/check.py --week 2` exits 0. Beyond the file and heading checks it recomputes tip speed, Reynolds, thrust and conservative thrust from geometry, requires the conservative coefficient to actually be lower than the nominal one, requires **both** the nominal and the conservative recomputed thrust to clear 10 N, requires the conservative mass at conservative thrust to still clear T/W 2.5, and requires the power sweep to cover at least three radii. The sweep also has to pass through the design point: the row at the chosen radius must carry the same aerodynamic power the rest of the week uses, or the curve is a different curve that happens to have the right shape.

Four more, all added after the gates were shown to certify an impossible design:

- **The momentum floor.** Aerodynamic power must sit at or above the ideal induced power over a declared area no larger than the projected 2R times span, and the resulting figure of merit must land between 0.20 and 0.75. Kellen measured 0.6 at UAV scale, so that is the number to design toward. This is the only gate in the whole plan that asks whether the design could exist rather than whether it agrees with itself
- **A second power route.** The published power loading gives an independent closure, and the two estimates have to agree within 35 percent
- **The thrust sensitivity table**, at least 3 rows, each reproducing its own mass ceiling and ideal power, with the chosen design thrust among them
- **Solidity inside 0.30 to 0.40**, and a low thrust coefficient that answers a stated blade deflection loss with its stiffness case cited

The audit adds the credibility checks that are not mechanical: the evidence ledger has no
summary result presented as measured, the coefficient scenarios are reproducible, the
candidate comparison follows the rule fixed in task 2, the named drive works continuously
at the design point, and every mass line has a usable scaling basis. The conservative T/W
target is 2.75, giving 10 percent paper margin over the hard limit. A value from 2.5 to 2.75
is compliant but stays red and needs a human decision before geometry freezes. This is a
judgment gate and does not weaken or change `tools/check.py`.

### Decision gate

**Geometry freezes only if the conservative case closes and its inputs have evidence.** If
the low coefficient and high mass miss either hard target, geometry does not freeze. If the
case clears 2.5 but misses the 2.75 internal target, stop for a human margin decision rather
than describing the result as safe.

**Fallback, in order:** pick a higher precomputed thrust row; move along the coupled radius
table; reject duplicated hardware and return to the single-rotor branch; revisit the shape
family. If none closes, stop and report. A result that reaches 2.51 by paper rounding is not
a design margin.

**Carry two candidate radii forward** rather than one. Be honest about what that buys: it saves week 2's exploration if the first choice fails, but it does not save week 3, because link lengths, offset geometry, the pitch schedule and gearing all move with radius. Switching radius after week 3 still costs a week 3 rerun. The second candidate is insurance against a week 2 mistake, not a free option in week 4.

---

## Week 3: pitch, thrust vectoring, packaging

Covers required item 3, the thrust-vectoring requirement at 15%, and the integration half of the 5% packaging criterion.

**Scope files:** `stage-1/design/03-pitch-and-vectoring.md`,
`09-packaging-and-integration.md`, `numbers.json`, `stage-1/decisions.md`,
`07-team-and-execution.md` if week H has returned, and a submission skeleton plus draft
PDF under `stage-1/submission/`

### Tasks

1. **Confirm the architecture screened in week 2.** Passive cyclic pitch remains the
   default because it avoids per-blade actuators. The vectoring actuator, controller and
   linkage mass must still match the week 2 envelope. If the actual mechanism needs another
   actuator or a heavier part, update the envelope before doing the rest of the week.
2. **Solve a real linkage.** State the topology, fixed pivots, moving pivots, link lengths,
   blade pitch axis and eccentric offset. Write the loop-closure equation or keep the small
   calculation script used to solve it. Evaluate every rotor position. Report assembly
   mode, transmission angle, joint travel, minimum clearance and any singularity. A target
   cosine is not a linkage solution.
3. **Produce the pitch schedule from that solution.** Use at least 24 distinct azimuths,
   close the revolution and compare the solved schedule with the intended harmonic. Record
   the residual, extrema and phase delay. Feed this schedule back into week 2's azimuthal
   load model instead of leaving the preliminary prescribed schedule in place. Store every
   schedule row in `numbers.json` as well as the readable design table.
4. **Size the vectoring input.** Show how the eccentric direction changes, the mechanical
   stop range, actuator travel, holding torque, slew time and electrical draw. Tie those to
   a named actuator and controller. This is a slow vector command, separate from the
   once-per-revolution blade motion.
5. **Map command to force.** Evaluate at least three phase commands. For each, give vertical
   force, lateral force, resultant magnitude and resultant direction from the updated load
   model, with the table stored in `numbers.json`. Mechanical phase authority sets the
   possible command span, but it is not evidence of force magnitude by itself. Keep
   `pitch.vector_range_deg` equal to phase authority only when the axisymmetric model
   supports one-to-one direction control. If the model does not, change that gate and its
   tests before making the claim.
6. **Handle the side force.** Compare the predicted nominal tilt with the measured 10 to 35
   degree literature range, explain the phase correction and show what happens at the ends
   of the operating range. State the uncertainty instead of using one measured angle as a
   universal correction.
7. **Package the moving mechanism.** Draw the swept linkage envelope, blade clearance,
   shaft supports, bearings, motor and transmission, actuator, ESC, controller, wiring and
   mounting points. Include the reaction-torque path, service access and the mechanical and
   electrical interface table. Dimensioned sketches are enough. No CAD.
8. **Start final assembly early.** Create the seven top-level submission headings, put the
   finished week 2 and 3 material under them and run one real pandoc and xelatex build. Read
   the draft PDF back. This smoke build is due 15 September, not during the final four days.
   Draft item 7's structure when week H has returned.

### Done when

`python tools/check.py --week 3` exits 0, cumulatively with weeks 1 and 2. Checks both files, requires the pitch schedule to have 24 or more **distinct** azimuths spanning at least 300 degrees, and requires whole numbers of actuators and mount points rather than merely positive ones.

The schedule also has to show a mechanism working. It must reach the stated amplitude in both directions, travel peak to peak by roughly twice the amplitude, close on itself over a revolution, and peak where the stated phase delay says it should, within 10 degrees. It has to track the harmonic model it claims to follow to a stated residual. And the vectoring range has to equal the mechanism's phase authority, so a claimed 360 degrees on a linkage that can drive 90 fails instead of passing as an assertion. A 37 row table spanning the full revolution with zero pitch at every azimuth used to pass all of this.

The audit checks what `check.py` cannot: every schedule row comes from the stated loop
closure, the linkage avoids singularity and interference, the named actuator meets travel
and holding torque, and the force-vector table follows from the load model at three or more
commands. It also records the successful draft PDF command and readback. If force direction
does not follow phase one to one, update `tools/check.py`, its fixtures and the plan together.

### Decision gate

Active or passive freezes here, and actuator count and mass go to week 4.

**Fallback:** cut prose around packaging and carry one actuator rather than several supplier
options. Keep the dimensioned layout and interface table. Do not defer linkage closure, the
phase delay or the force-vector map. Those are the defensible core of the 15 percent
kinematics and vectoring criterion.

---

## Week 4: structure, mass, thrust-to-weight, materials, manufacturing

Covers required items 5 and 6, plus the 15% structural criterion that had no section before.

**Scope files:** `stage-1/design/05-mass-and-tw.md`, `06-materials-and-manufacturing.md`, `08-structure-and-loads.md`, `numbers.json`, `stage-1/decisions.md`

This is the second heavy week. Geometry and the mechanism are frozen, but the blade section
and drive still have to survive the loads. Material allowables and structural calculations
run first, then the refined mass and T/W close together.

### Tasks

1. **Close the blade stiffness assumption first.** Rebuild the week 2 skin, core, spar,
   adhesive and root section with the final material allowables. Calculate bending
   deflection and torsional twist at peak aerodynamic load and operating centrifugal load.
   The result has to support the blade-flexibility loss used for the low thrust coefficient.
   If it does not, week 2 reopens on 18 September rather than failing on the last day.
2. **Load cases and strength.** Use operating and a declared overspeed condition. Calculate
   blade centrifugal load, peak aerodynamic root bending, blade-root and attachment demand,
   rotor shaft torque, shaft and bearing reactions, pitch-link and pin load, and the frame
   and mount load path. Use closed-form calculations with assumptions shown. No FEA is
   claimed at Stage 1.

   **Centrifugal is the larger term, not a secondary one.** Runco measured 71 gf of centrifugal force against 16 gf of aerodynamic loading on the same blade, a factor of 4.4. The blade attachment therefore carries its own margin against the recomputed centrifugal load, and the aerodynamic peak-to-mean factor is gated at 4.0 rather than 3.0, since the 3-to-4 range it comes from is simulated and 3.0 is the bottom of it.

   Every one of these is derived from the design, not asserted beside it, and the gate recomputes three of them. Per-blade mass is the blade mass budget divided by the blade count, so a 1 g blade cannot sit next to a 108 g blade budget. Rotor shaft torque is shaft power over rotor angular speed, which is the first thing a reviewer recomputes and takes about ten seconds. Blade root bending is thrust per blade times a declared lever arm times a declared peak-to-mean load factor. State which shaft each torque refers to and give the transmission ratio, because torque upstream and downstream of a reduction are different numbers.
3. **Margins and missing analyses.** Compare each demand with the right allowable and a
   safety factor. Margins below 1.5 fail. Name the work left for Stage 2, including fatigue,
   modal response, balance sensitivity and FEA. Do not imply that a static beam check covers
   it.
4. **Refine the component mass budget.** Cover blades, frame, pitch mechanism, motor,
   vectoring actuator, mounting, bearings, shaft, hub, transmission, ESC, controller,
   wiring, adhesive and fasteners. Each line carries a material calculation, measured
   analogue or named supplier figure and points to the week 2 line it refines. Add a visible
   design-maturity reserve rather than hiding it across rounded lines.
5. **Compute nominal and conservative T/W.** State compliance against 2.5, margin against
   the 2.75 internal target and the contribution of every mass category from D15. Reconcile
   any line that moved more than 25 percent from week 2 before accepting the total.
6. **Tie material and process to the load.** Give each part its material, stock form,
   process, key tolerance, joining method, balance or inspection step and make-or-buy
   choice. Include an assembly order and the measurements that decide whether a built rotor
   is safe to spin.
7. **Build a costed BOM.** Record quantity, supplier or calculation basis, quote date, unit
   cost, lead time and Indian source where one exists. Separate bought parts from tooling
   and fabricated parts. Cost realism is 10 percent with manufacturing, so a total without
   traceable rows is not enough.

### Done when

`python tools/check.py --week 4` exits 0, cumulatively. It sums the mass lines and rejects any that vanish or carry a thin basis, recomputes weight and both T/W values, requires the conservative mass not to be lighter than the budget, recomputes the centrifugal load from blade mass, speed and radius, recomputes per-blade mass, shaft torque and blade root bending from the design, and requires all four structural margins, blade, shaft, pitch link and blade attachment, to be at least 1.5.

Two of those come from reading the published loads properly. The blade attachment carries its own margin against the recomputed centrifugal force, because Runco measured centrifugal beating aerodynamic load by 4.4 times on the same blade, and the aerodynamic peak to mean factor must be at least 4.0.

Continuity with week 2 is checked per component, not just on the total. Each envelope line has to stay within 25 percent of what the budget lines refining it add up to, and no envelope line may end up with nothing refining it. Comparing totals alone let the whole budget move into the blades while every other component shrank to the smallest legal line, because the sum came out the same.

The audit also requires the calculated blade deflection to support week 2's thrust-loss
case, a visible shaft and frame load path, a mass reserve, supplier or calculation evidence
for every expensive line and a BOM with lead times. These are judgment checks. The existing
week 4 gate remains unchanged.

### Decision gate

If the refined budget breaks T/W, the second radius from week 2 is available, but taking it **invalidates weeks 3 and 4** because link lengths, offset geometry, pitch schedule, gearing and centrifugal load all move with radius. With four days left after week 4 that is not recoverable, so treat it as a last resort and trigger it on day 2 of the week or not at all. That is exactly why the feasibility envelope moved into week 2.

The cheaper fallbacks, in order, are to **move to another row of week 2's frozen thrust sensitivity table**, then to trim the mass budget where a line has slack, then to reopen radius. Raising thrust to a point week 2 never studied is not a cheap fallback and the gate rejects it: a thrust outside the table fails, because the row carries the rpm, the ideal power and the structural loading that come with it. An unstudied increase is a rerun of week 2, not a week 4 edit.

---

## Week 5: team, execution plan, assembly, staging

Covers required item 7, then packages for a human to send.

**Scope files:** `stage-1/design/07-team-and-execution.md`, `stage-1/submission/`, `stage-1/decisions.md`

### Tasks

1. **Finish the team capability section** from the week 3 draft. Map real capability and
   real gaps against the preference list. **Names, institutions, claimed capability and
   tool access come from the human.** The agent does not infer them.
2. **Finish the Stage 2 execution plan.** Map it onto all 11 required items, with tool
   access, owners, dependencies, build and test gates and the missing capability route. A
   list of 11 headings without dates or ownership is not a plan.
3. **Assemble, do not rewrite.** Put all 7 required items in the official order and add the
   8-row criteria map. Pull from the reviewed design files so week 5 does not introduce a
   fresh set of technical claims.
4. **Add a claims, evidence and risk table.** Every headline claim names its calculation or
   source, confidence, main failure mode and Stage 2 validation. Put the transferred thrust
   coefficient, module mass, blade deflection and vector map first.
5. **Run the hostile viva pass.** Write and answer at least 10 short questions. Cover the
   coefficient transfer, why 2.5 is believable from a 2.13 benchmark, what mass is truly
   fixed, why the radius was chosen, motor continuous rating, reaction torque, linkage
   singularity, vector direction, blade stiffness and the first Stage 2 test. Fix the report
   when an answer exposes a gap.
6. **Build and inspect the PDF.** Run the known week 3 toolchain, read the attachment back,
   inspect page breaks, figure labels, citations, units and the 15 page target when no
   organiser limit was supplied. The attachment is what gets evaluated.
7. **Run final consistency and provenance checks.** Every design number traces to
   `numbers.json`. Every borrowed figure or table has permission or is redrawn from cited
   data. No summary-only source is presented as a read paper. The title, team details,
   registration reference and file name are checked by the human on 25 September.
8. **Draft the email** with the final attachment name and stage it. **Do not send.** The
   named human sends it on 26 September and keeps the sent-message record.

### Done when

`python tools/check.py --week 5` exits 0, cumulatively. Requires all 7 items as real top-level headings, a criteria map that is an actual table with all 8 criteria in its rows, a submission of substance rather than an outline, and a staged email draft naming the attachment, the organiser address and a subject line.

The PDF condition is no longer a byte count. The gate reads the attachment back with pypdf and requires it to carry this submission's seven section names and its declared values, because a file size cannot tell the difference between the right report and an unrelated one. The old wording asked for 50 kB and the earlier gate only asked for four readable pages, which between them accepted the competition's own problem statement as our submission.

Week 5 also blocks on the four markers in [human-gate.md](human-gate.md). It cannot write a real capability section or stage a submission without them.

The audit must also find the claims table, the hostile-viva notes, complete citations and
`TECHNICAL-READ-COMPLETE` in the human gate. The final audit owns these checks. `check.py`
still owns document identity and number consistency.

### Decision gate

**The roster is one person and that is what the section says.** A solo entry with a credible plan and honest scope reads better in a viva than five names nobody can stand behind. Name the capability gaps and say how Stage 2 fills them, because the problem statement's preference list is a spec for this section and pretending to cover all of it is the failure mode.

---

## What counts as enough against the evaluation criteria

The published weights belong to the final evaluation, not a separate Stage 1 rubric. They
are still the best signal available. Passing `check.py` is the floor. The table below is the
standard for a Stage 1 report an evaluator could believe.

| Criterion | Stage 1 evidence this plan must produce | Honest ceiling |
| --- | --- | --- |
| 10 N thrust, 15% | Recomputed coefficient model, source ledger, area conversion, three coefficient scenarios, coupled sensitivity and a load distribution | Good preliminary case, not proof without test or CFD |
| T/W above 2.5, 15% | Physical blade estimate, named drive and actuator, complete boundary, component scaling classes, mass reserve and conservative T/W target of 2.75 | Strong only if the named hardware and section close |
| Kinematics and vectoring, 15% | Solved loop closure, linkage dimensions, singularity and clearance check, actuator sizing and a force-vector map | Can be strong at Stage 1 |
| Aerodynamic analysis, 15% | Dimensionless match, momentum floor, measured power route, azimuthal analytical model and uncertainty table | Credible preliminary analysis, not a top CFD or wind-tunnel score |
| Structural design, 15% | Centrifugal, peak aerodynamic, shaft, bearing, linkage and mount load paths, blade deflection and stated missing analyses | Good preliminary strength case, with FEA left to Stage 2 |
| Manufacturing and cost, 10% | Material and process per part, tolerances, inspection, assembly order, supplier-backed BOM and lead times | Can be strong if rows are traceable |
| CAD, integration and packaging, 5% | Dimensioned moving-envelope sketches, drivetrain layout, mounts and interface table | Intentionally medium because Stage 1 has no CAD |
| Presentation and clarity, 10% | Criteria map, claims and risk table, clean figures, traced numbers and hostile-viva answers | Can be strong |

The aerodynamic criterion stays the thinnest even after these changes. The report should
say why full CFD is scheduled for Stage 2 and avoid phrases such as "validated model" for a
coefficient transfer. Transparency helps more here than another decimal place.

---

## Standing risks

**The highest-risk assumption is the thrust coefficient transfer.** The 0.607 anchor is a single measured point on a rotor with a different blade count, airfoil, solidity and Reynolds number. Everything downstream scales off it. Week 2 bounds it rather than adopting it, and the conservative case has to close on its own, which is the only real defence available without a wind tunnel.

**The published benchmark is tight and does not prove this design.** Re-cut onto the module
boundary, Runco gives 2.13 on the optimistic allocation and 1.53 on the harsh allocation.
The target is 2.5. Blade mass per newton is scale invariant, and the motor and transmission
cannot be treated as fixed either. Only genuinely fixed and duplicated hardware amortises.
Week 2 has to close the gap component by component with named hardware, blade construction
and a full mounting allocation. Full working in [literature.md](literature.md) and decisions
D8, D11, D13 and D15.

**Three papers are still unread**, one of them the only study in our Reynolds band. Kellen's
measured coefficient is the highest-value pull for week 2. If it stays unavailable, the
submission carries a labelled downside scenario and does not describe it as a published
bound. Heimerl improves week 3 and 4 loads. Ramsey improves the blade mass and stiffness
basis.

**One person is doing this.** Confirmed 27 August. The full plan needs about 84 focused hours
after week 1 and another project collides with week 3. Until real hours are written down,
the calendar is an assumption. Use the reduced scope in the calendar when the hours do not
exist. Never repay a schedule slip from the final four days.

**Late integration can still kill an otherwise sound report.** The draft PDF is built on 15
September, source status is carried in the evidence ledger, and the human reads the final
attachment on 25 September. Team markers, registration reference, file name and the actual
sent email remain human responsibilities.

**No CAD is required at Stage 1** and none should be built. CAD quality is scored at Stage 2 and 3.
