# Decisions

Numbered, append only. Reopening an earlier decision means a new entry that says which one it supersedes and why, never an edit in place.

## D1: context.md outranks the earlier documents

26 August 2026, week 1.

`brief.md`, `handoff.md` and `_shared-timeline.md` were written from summaries of a page that serves no content to a fetcher. The problem statement PDF contradicts them in several places. Rather than edit every file and risk leaving one stale, `context.md` is the single authority on requirements and the others are left as history.

## D2: the module is one larger rotor, not a cluster of small ones

26 August 2026, week 1. **Provisional and weaker than it looked.** Superseded in part by D8.

Benedict's flight-weight 6 inch rotor masses 96 g and carries 1.98 N. Reaching 10 N by repeating it takes 5.04 rotors, which is 485 g of rotor alone against a 408 g budget for the entire module. What that actually proves is that copying one published rotor five times does not close. It does not rule out a redesigned two or three rotor cluster, which is a different claim and was never tested. Week 2 must compare single against clustered on the same component boundary, the same coefficient assumptions and the same power model before this freezes.

## D3: numbers live in one file

26 August 2026, week 1.

Every quantity the submission states is defined in `stage-1/design/numbers.json` and cited from prose through a `## Numbers used` block. The gate recomputes the arithmetic and fails on disagreement. Chosen because the failure mode on a design document written across five weeks is a number that drifts between sections, and that is exactly what a viva finds.

## D4: no CAD at Stage 1

26 August 2026, week 1.

The problem statement does not ask for it and CAD quality carries 5 percent, scored on the Stage 2 and 3 package. Five criteria at 15 percent each are analysis. Modelling time now is taken from those.

## D5: the submission email is never sent by an agent

26 August 2026, week 1.

Outward facing, irreversible, and it represents a team to a national programme. The loop drafts and stages it. A human sends it. Recorded as a blocked trigger in the loop config.

## D6: design thrust is a free variable above 10 N

26 August 2026, after the round 2 review.

The requirement is thrust at or above 10 N with T/W above 2.5. Those two together set the mass ceiling, and the ceiling moves with thrust: 407 g at 10 N, 489 g at 12 N, 530 g at 13 N, floors rounded down because the inequality is strict. Treating 408 g as fixed, which every earlier document here did, pinned the design to the most constrained corner of the feasible region for no reason the problem statement gives.

Design thrust therefore becomes a week 2 decision rather than an assumption. It buys mass ceiling at the cost of power, and power is not a scored criterion. It is not free, because the margin a paper design carries eats into the gain, but it is a real lever.

## D7: hard limits apply to recomputed values, never stored ones

26 August 2026, after the round 2 review.

The first version of the gate script compared stored headline numbers against the limits while only checking consistency to 2 percent. A 1.9 percent overstatement of thrust and a 1.9 percent understatement of mass both passed, and compounded into a design with an actual thrust of 9.82 N and an actual T/W of 2.41 that satisfied every gate. Verified, not hypothesised.

Limits now test what the geometry and the mass lines give. Internal arithmetic must reproduce to 0.5 percent, with a looser 2 percent allowance only for numbers rounded for prose. A conservative case using a lower coefficient and a higher mass must clear both targets independently.

## D8: the module thrust-to-weight gap is the project's main risk

26 August 2026, after the round 2 review.

Re-cutting the published designs onto the competition's module boundary, meaning blades, frame, pitch mechanism, motor, actuator and mounting but no battery or avionics, gives a module T/W of 1.69 for Benedict's quad rotor and 1.80 for Sirohi's conceptual design. Both exclude mounting hardware, which neither paper breaks out, so both are optimistic.

The requirement is 2.5. That is a 39 to 48 percent improvement over the closest published work, and it is further from the state of the art than anything else in the brief.

The earlier 37 to 48 percent rotor-fraction benchmark in the literature file was measured against all-up aircraft mass including battery, avionics and airframe. It is not comparable and should not be used for budgeting.

This does not stop the project. It does mean the argument for clearing 2.5 has to be made explicitly in week 2, resting on scale, on fixed masses amortising over more thrust, and on the fact that the published designs were flying demonstrators rather than mass-optimised modules. If week 2's conservative case cannot close, that is a reportable finding and not something to trim assumptions around.

## D9: a paper design has to clear a physical bound, not only its own arithmetic

27 August 2026, after the goal-based review.

Every gate up to this point checked that stored numbers agreed with each other. None asked
whether the design could exist. A review demonstrated the consequence: a module claiming
13.5 N of thrust from 1 W of aerodynamic power passed week 2 completely, because the power
chain, the radius sweep and the thrust recompute were all internally consistent with it.

Aerodynamic power is now bounded below by momentum theory, computed over a declared
effective area that may not exceed the projected frontal area of 2R times span, and the
figure of merit that falls out has to land between 0.20 and 0.75. The momentum route is a
bound rather than a second opinion, since it is the same equation rearranged, so the
independent cross-check is the published power loading route and the two have to agree
within 35 percent.

The same principle applies to structure in week 4. Per-blade mass comes from the blade mass
budget divided by the blade count, rotor shaft torque from shaft power over angular speed,
and blade root bending from thrust per blade with a declared lever arm and load factor. A
reviewer recomputes shaft torque from power and speed in about ten seconds, and a
structural model disconnected from the design costs more than the 15 percent it is scored
on, because it makes everything else look unchecked too.

## D10: design thrust is frozen as a table in week 2, not reopened in week 4

27 August 2026, after the goal-based review.

D6 made design thrust a free variable above 10 N, which was right. The plan then listed
raising thrust as the cheapest week 4 fallback, which was wrong. Within the fixed shape
family, going from 10 N to 13 N buys 30 percent more mass ceiling and spends 14 percent
more rpm, 30 percent more centrifugal load and 48 percent more ideal power. That can move
the motor, the transmission, the thermal case and the structure at once, in a week with
four days left after it.

Week 2 therefore freezes a thrust sensitivity table with at least three candidates, each
carrying its mass ceiling, ideal power and rpm. Week 4 may only select a row from it. A
design thrust outside the table fails the gate, because an unstudied increase is a rerun of
week 2 wearing the costume of a small edit.

## D11: the thrust-to-weight case rests on fixed masses, not on blade scaling

29 August 2026, after the external research round.

D8 left the case for clearing 2.5 resting on four arguments, one of which was scale, and
flagged a counterargument it could not dismiss: that blade mass per newton is scale
invariant under geometric similarity, so growing the rotor buys nothing on blade mass.

Shrestha and Benedict, JAHS 2022, settle it, and they settle it against us on that point.
Their validated model gives both halves at once. Non-dimensional thrust holds as Reynolds
rises while torque and power fall, so efficiency does improve with scale. But blade weight
per unit thrust stays constant and blade stress rises monotonically, independent of how the
blade is designed.

So the argument narrows. Scale buys aerodynamic efficiency and nothing on blade mass. The
gap has to be closed by the non-blade fixed masses, meaning bearings, fasteners, ESC,
linkage and motor, amortising over roughly five times the thrust, plus materials and stress
management on the blades themselves. Week 2 makes that case in those terms and drops the
claim that scale shrinks blade mass fraction, which the published record contradicts.

The practical threshold, worth testing early in week 2: if the non-blade fixed masses
cannot come in under roughly 40 percent of the mass ceiling at the chosen thrust, the
target is not reachable at that radius and the answer is a larger radius, a higher design
thrust, or fewer fixed parts, meaning one motor per module and passive pitching rather than
per-blade servos.

## D12: the borrowed coefficient is only valid inside the solidity band it was measured in

29 August 2026, after the external research round.

Kellen 2019 is the source of the shape family this project defaults to, and its measured
optimum sits at a solidity of 0.30 to 0.40. Our family gives 0.315, which is inside it.

The 0.607 coefficient is transferred into that family across a change in blade count,
airfoil and chord ratio all at once. The published record says the Reynolds part of that
transfer is safe, since non-dimensional thrust is roughly Reynolds invariant from 35,000 to
100,000, and that the configuration part is not de-risked by anything. Solidity is the one
piece of the configuration change that has a measured optimum attached to it, so it is
gated: outside 0.30 to 0.40 the coefficient has to be re-derived rather than carried
across.

Two other consequences of the same round. Peak blade thrust runs 3 to 4 times the cycle
mean on 2 and 3 bladed rotors, which a cycle-averaged coefficient hides, so the blade load
factor is gated at 3.0 or above. And the figure of merit to design against is about 0.6,
which is what Kellen measured, comfortably inside the 0.20 to 0.75 band the gate allows.

## D13: the feasibility case starts from 2.1, not from 1.69

29 August 2026, after the Runco figure was settled.

D8 set the benchmark at 1.69 and 1.80 and called the gap 39 to 48 percent. D11 then removed
the blade-mass half of the argument for closing it. Both stand on their own terms, and
together they read worse than the record actually supports.

Runco 2023, read properly, gives a module thrust to weight of **2.13** on the same
optimistic boundary that produced 1.69 and 1.80, and 1.53 on the harshest allocation. It is
the best published point available and it is better than either of the two this project has
been budgeting against. Its 8.2 g already carries the servo that the module boundary
requires and that Sirohi's number excludes, so it is the least optimistic of the three, not
the most.

The case therefore reads: a mass-optimised micro module at Reynolds 18,600, built from flat
plate blades with no thrust to weight target in mind, already reaches about 2.1 on our
boundary. Scaling that to 10 N is neutral on blade mass per newton, favourable on fixed
mass amortisation, and favourable on power, since power falls with Reynolds. The
expectation is therefore **above** 2.1, not below.

That is a materially different argument from the one D8 and D11 leave standing. The gap to
2.5 is roughly 17 percent from the best comparable point, not 39 to 48 percent from the
second and third best. Week 2 argues from 2.13 and states the allocation choices, ESCs and
mounting share, that move it.

Neither D8 nor D11 is withdrawn. D8's benchmarks are still correct for the designs they
describe, and D11's finding that scale buys nothing on blade mass still holds and still
constrains where the remaining margin comes from.

## D14: the three-point mass series bounds the argument, it does not fit a law

29 August 2026.

Runco at 70 g, Kellen at roughly 17 lb and Ramsey at 25 kg span four orders of magnitude
from one lab, and the temptation is to fit mass per newton against scale and call it the
scaling law this project could not find. That would be wrong, and week 2 must not do it.

The three designs are not geometrically similar:

| | Runco 70 g | Kellen UAV | Ramsey 25 kg |
| --- | --- | --- | --- |
| Blades | 4 | 3 | 6 |
| Chord to radius | 0.8 | 0.66 | 0.64 |
| Airfoil | flat plate | NACA 0020 | NACA 0015 |
| Pitch amplitude | 45 deg | 40 deg | 45 deg |

Blade count and airfoil do not move monotonically with scale, so any exponent fitted to
these three points conflates scale with design choice, and at three points the two cannot
be separated. Shrestha's blade-mass invariance, which D11 rests on, is derived **under
geometric similarity**, and these designs are not that.

So the series is used to **bound** the fixed-mass amortisation argument and to show the
direction of travel. It is not used to fit an exponent, and any figure taken from it is
quoted with the scatter and with the fact that three different rotors are being compared.

Two smaller readings from the same table. Chord to radius converges on roughly 0.65 above
micro scale, which supports the 0.66 baseline independently of Kellen. And the same lab
chose NACA 0015 at 25 kg, so the record does not show 0020 winning at every scale. Our
Reynolds number sits beside Kellen's rather than Ramsey's, so 0020 still holds, but the
submission should not claim thicker is universally better.

## D15: the fixed-mass case excludes the power-scaled drive

29 August 2026, after the execution review. This narrows one phrase in D11.

D11 is right that blade mass per unit thrust does not improve through geometric scaling.
It then groups the motor with fixed masses. That part is not safe. Motor mass follows
continuous power, speed and thermal duty. Transmission, shaft and bearing mass also follow
torque and speed. A larger radius lowers aerodynamic power inside the chosen family, but it
raises rotor torque, so the drive cannot be treated as a constant allowance.

Week 2 now sorts every mass line into three groups: blade or geometry-scaled, power or
torque-scaled, and fixed or duplicated. The last group includes items such as controller
electronics, fasteners and linkage pivots only when the basis supports it. The 2.13 Runco
benchmark remains a starting point, not a scaling law. The design closes only through the
component-level mass envelope and named drive hardware.

## D16: use the top of the published peak-load range

29 August 2026, after the execution review. This supersedes the 3.0 minimum stated in the
second consequence under D12.

The cited simulated range for peak blade thrust is 3 to 4 times the cycle mean. The source
has not yet been replaced by measured Heimerl data, so taking the bottom of the range is not
conservative. The minimum blade load factor stays 4.0, matching `tools/check.py` and the
current plan.

## D17: geometry needs paper margin, not bare compliance

29 August 2026, after the execution review.

The competition limit remains strictly above 2.5 and `tools/check.py` still enforces that
limit. A paper estimate built on a transferred thrust coefficient should not freeze at
2.51 and be presented as safe. Week 2 therefore targets a conservative T/W of 2.75, which
is 10 percent above the hard limit. A result between 2.5 and 2.75 is compliant but remains
red and needs a human decision before geometry freezes. This is a judgment gate, not a
replacement for the competition rule.
