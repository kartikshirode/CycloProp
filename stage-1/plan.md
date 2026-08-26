# CycloProp Stage 1 plan

Execution plan, one week per loop tick. Requirements live in [../context.md](../context.md) and technical inputs in [literature.md](literature.md). This file only says what gets done when, and how a machine decides whether it happened.

**Deadline 27 September 2026, submitting 26 September.** Email to pushpak_gc2026@aero.iitb.ac.in.

## How this plan is executed

Driven by the `weekly-loop` skill under `/loop`. One tick runs one week through a fresh agent, then the supervisor runs the gates in its own shell. Config at [../.claude/weekly-loop.md](../.claude/weekly-loop.md).

Rules that make the weeks machine-checkable:

- Every number the submission states lives in `stage-1/design/numbers.json` and nowhere else. Prose cites it, never restates it from memory. The gate recomputes the arithmetic and fails on any disagreement
- Each week writes its own final prose into its own file under `stage-1/design/`. Week 5 stitches, it does not write from scratch
- A week is done when `python tools/check.py --week N` exits 0, not when the agent says so
- Every week ends with a go or no-go decision recorded in `stage-1/decisions.md`, with the fallback already written down before the week starts

## Calendar

| Week | Dates | Days | Covers required items |
| --- | --- | --- | --- |
| 1 | 26 Aug to 1 Sep | 7 | Requirements and literature. Done |
| 2 | 2 to 8 Sep | 7 | 1 configuration, 2 rotor sizing, 4 thrust and power |
| 3 | 9 to 15 Sep | 7 | 3 blade arrangement and pitch control, plus thrust vectoring |
| 4 | 16 to 22 Sep | 7 | 5 module weight and T/W, 6 material and manufacturing |
| 5 | 23 to 26 Sep | 4 | 7 team capability and execution plan, assembly, submit |

Week 5 is the short one and it carries the deadline, so weeks 2 to 4 do not get to slip into it. Each of those has a fallback below that trades depth for schedule rather than pushing work forward.

Runs alongside UAV-X. Week 3 collides with the UAV-X comms layer. If one has to give, this one gives, because writing compresses under pressure and debugging does not.

---

## Week 1: requirements and literature

**Status: done, 26 August 2026.**

Delivered [../context.md](../context.md) and [literature.md](literature.md). Recovered the official problem statement PDF, which nobody had found before, and it moved several things:

- Stage 1 wants 7 items, not 5. Power, T/W as a stated result, and a team capability section were all missing from the old plan
- Thrust vectoring is a requirement carrying 15%, and had never been mentioned in this repo
- The thrust-to-weight ratio is measured on the module, quoted in the PDF, so the 408 g budget is confirmed and sizing is unblocked
- Eight evaluation criteria, not nine, summing to 100

Progress at `stage-1/progress/week-1.md`.

---

## Week 2: configuration, rotor sizing, thrust and power

Covers required items 1, 2 and 4.

**Scope files:** `stage-1/design/01-configuration.md`, `stage-1/design/02-rotor-sizing.md`, `stage-1/design/04-thrust-and-power.md`, `stage-1/design/numbers.json`, `stage-1/decisions.md`

### Tasks

1. **Fix the configuration.** Single cyclorotor module, or several small ones. The literature already answers this: repeating a published MAV rotor to reach 10 N needs 485 g of rotor against a 408 g whole-module budget, so it has to be one larger rotor. Write the argument properly, with the aerodynamic half as well as the mass half, since non-dimensional thrust holds while torque and power fall as Reynolds number rises.
2. **Choose the blade shape family.** Two candidates, both from measured work. The Texas A&M UAV-scale optimum is 3 blades at c/R 0.66, blade aspect ratio 4, NACA 0020, plus or minus 40 degrees. Benedict's MAV optimum is 4 blades at c/R 0.433, NACA 0015, asymmetric 45 at top and 25 at bottom, axis at 25 percent chord. Our Reynolds number lands in the Texas A&M band, so that is the default and the burden of proof is on choosing otherwise.
3. **Pick the radius.** Solving the shape family for 10 N pins Reynolds near 100,000 whatever radius is chosen, so radius is a free trade of rpm against envelope and structural mass. Take the table in [literature.md](literature.md), add an estimated blade mass column, and choose. Larger radius means lower rpm and lower tip speed but more bending moment and more material.
4. **Compute thrust two ways.** Blade-area coefficient scaling off Benedict's measured quad rotor, and a streamtube momentum estimate. Report both and the gap between them. One method agreeing with itself is not a check.
5. **Compute power.** Aerodynamic power from measured power loading at the high-thrust end, then the electrical number through transmission, motor and ESC efficiencies, each stated separately with a source or a justified assumption.
6. **Write `numbers.json`.** Every fixed quantity, with units, and a `source` field on each saying whether it is measured, derived or assumed.

### Done when

`python tools/check.py --week 2` exits 0. That checks the three prose files exist with their required headings, `numbers.json` parses and carries every key in the week 2 schema, the thrust arithmetic reproduces from the stored geometry, the Reynolds number reproduces, and no prose file states a number that contradicts `numbers.json`.

### Decision gate

Radius, blade count, chord, span, airfoil, pitch amplitude and rpm are all frozen at the end of this week and recorded in `stage-1/decisions.md`. Later weeks may not quietly reopen them; changing one is a numbered decision entry with a reason.

**Fallback if the week overruns:** drop the second thrust method and ship the coefficient scaling alone, flagged in the text as single-method. Do not push the freeze into week 3, because week 3's kinematics need fixed geometry.

---

## Week 3: blade arrangement, pitch control, thrust vectoring

Covers required item 3, and the thrust-vectoring requirement that carries 15%.

**Scope files:** `stage-1/design/03-pitch-and-vectoring.md`, `stage-1/design/numbers.json`, `stage-1/decisions.md`

### Tasks

1. **Choose active or passive, and justify it.** Passive four-bar is the default on mass evidence, since every flying cyclocopter in the read literature uses one and none use per-blade servos. Say what the choice costs as well as what it buys.
2. **Work the four-bar kinematics.** Link lengths, pitching axis location, and the offset distance that produces the chosen amplitude. Produce blade pitch angle against azimuth as a table of computed values, not a sketch.
3. **Show the phase delay.** The mechanism does not put peak pitch exactly at 90 and 270 degrees. Quantify the delay for our geometry, because it is the origin of the side force and pretending it is not there would be caught in a viva.
4. **Thrust vectoring, quantified.** Offset magnitude sets amplitude, offset direction sets phase, and phase steers the vector. Give the achievable vector range in degrees and what actuates it. This is the section that answers criterion 3, so it gets the most care.
5. **Handle the side force.** Predict the resultant tilt for our geometry, benchmark it against the 30 degrees Benedict measured, and state the correction, which is rotating the mechanism offset by the same angle.
6. **Select the actuators** for amplitude and phase, with masses, and hand those masses to week 4.

### Done when

`python tools/check.py --week 3` exits 0. Checks the file exists with its required headings, the pitch schedule table has at least 24 azimuth rows, the actuator masses are present in `numbers.json`, and the stated vector range is a number rather than a claim.

### Decision gate

Active or passive is frozen here, and the actuator count and mass go into the mass budget. **Fallback if the week overruns:** ship the kinematics and the vectoring argument, defer the phase-delay quantification to a stated Stage 2 item. Do not defer the vectoring section itself, since it is 15 percent of the score.

---

## Week 4: mass budget, thrust-to-weight, materials, manufacturing

Covers required items 5 and 6.

**Scope files:** `stage-1/design/05-mass-and-tw.md`, `stage-1/design/06-materials-and-manufacturing.md`, `stage-1/design/numbers.json`, `stage-1/decisions.md`

### Tasks

1. **Component mass budget to 408 g.** Every line the problem statement names has to appear: blades, frame, pitch mechanism, motor, actuator, mounting hardware. Add bearings, shaft, hub, ESC and fasteners. Each line gets a basis, meaning a measured analogue, a material calculation or a supplier figure.
2. **Benchmark the split.** Published designs put the rotor at 37 to 48 percent of all-up weight. If our budget lands far outside that, either the budget is wrong or there is a reason worth stating.
3. **Compute T/W and state the margin.** The requirement is above 2.5. Landing at 2.51 is not a design, it is a rounding error, so carry visible margin and say how much.
4. **Material selection with reasons.** Carbon fibre for spars and skins, core choice for the blades, hub and endplate material, bearing selection. Each choice tied to a property that matters, since blade stiffness is one of the few things the literature shows hurting performance directly when it is missing.
5. **Manufacturing route per part.** How each piece actually gets made, with Indian sourcing where it exists, because indigenous development is the point of the programme and manufacturability carries 10 percent.
6. **Cost realism.** A preliminary bill of materials with indicative prices. Cost realism is named in the same criterion as manufacturability.

### Done when

`python tools/check.py --week 4` exits 0. Checks both files exist with required headings, every mass line in `numbers.json` has a non-empty basis field, the mass lines sum to the stated total, the total is under 408 g, and the T/W recomputed from thrust and total mass matches the stated value and exceeds 2.5.

### Decision gate

If the budget will not close under 408 g, that is a real finding and not a reason to fudge a line. **Fallback:** reopen radius from week 2 as a numbered decision, since a smaller rotor at higher rpm is lighter, and rerun weeks 2 and 4 numbers. Trigger this by day 4 of the week, not day 7.

---

## Week 5: team capability, execution plan, assembly, submit

Covers required item 7, then ships.

**Scope files:** `stage-1/design/07-team-and-execution.md`, `stage-1/submission/`, `stage-1/decisions.md`

### Tasks

1. **Team capability section**, written against the preference list the problem statement publishes: rotor design and unsteady aerodynamics, CAD and mechanical design, kinematic analysis, CFD and FEA and multibody dynamics, lightweight structures, motor and actuator selection, UAV subsystem integration. Claim only what is real and name who covers what.
2. **Execution plan for Stage 2**, mapped onto the 11 items Stage 2 will demand, with the CAE tool access named. This is where faculty backing shows up as an asset rather than a formality.
3. **Assemble the submission.** All 7 required items in the problem statement's own order, with a short map at the front showing which section answers which of the 8 evaluation criteria. Evaluators scoring against a rubric should not have to hunt.
4. **Final consistency pass.** Every number in the document traced to `numbers.json`.
5. **Send on 26 September**, a day early, and record what went where.

### Done when

`python tools/check.py --week 5` exits 0. Checks the submission document exists, contains all 7 required item headings, contains the criteria map, and that no number in it contradicts `numbers.json`.

### Decision gate

**Fallback if the team is not assembled by 23 September:** submit as a smaller team and say so plainly in item 7. An honest two-person team with a credible plan reads better than five names that cannot be stood behind in a viva.

---

## Standing risks

**The schedule assumes hours nobody has counted.** This is the input most likely to invalidate the rest, and it stays open until someone states real weekly availability. Writing compresses better than code, which is why this project rather than UAV-X absorbs a squeeze.

**Three papers are still unread**, one of them the only study in our own Reynolds band. Week 2 leans on a search summary of it. If a library proxy or the faculty supervisor opens it, re-derive the shape family and record a decision entry.

**No CAD is required at Stage 1** and none should be built. CAD quality is scored at Stage 2 and 3. Time spent modelling now is time not spent on the five 15-percent criteria.
