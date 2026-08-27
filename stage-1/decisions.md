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
