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

## D18: the single rotor beats a redesigned cluster, so D2 stops being provisional

2 September 2026, week 2.

D2 said the module is one larger rotor and admitted it had only proved that copying
Benedict's 96 g rotor five times does not close. That was never the same claim. Week 2 ran
the comparison D2 asked for: one thrust model, one power model, one mass build-up, one module
boundary, each layout swept over radius, best conservative thrust to weight kept.

Every contested assumption was set in the cluster's favour. Non-overlapping wakes, no
interaction penalty, one shared motor sized on total power, one shared controller, and the
same thrust coefficient for all three even though splitting the thrust drops per-rotor
Reynolds below the band that coefficient was measured in.

Conservative thrust to weight came out at 2.389 for the single rotor, 1.795 for two rotors and
1.434 for three. The single rotor is also the smallest, has the fewest parts, and is the only
one whose Reynolds number stays inside Kellen's band. Splitting the thrust duplicates the
spider, hub, pitch mechanism, shaft, bearings and belt stage while raising total blade area,
because smaller rotors run slower for the same per-rotor thrust and need more area to make it
up.

D2 is confirmed on its own terms and the provisional label comes off.

## D19: ESCs and mounting hardware sit inside the module boundary

2 September 2026, week 2.

Two allocations have been open since the Runco re-cut and both move the benchmark. They are
settled here, before any candidate was scored, and both are settled against us.

ESCs count as module hardware. The motor does not turn without one and the problem statement
lists the motor. Mounting counts in full, so every fastener, insert, standoff, lug and bonded
joint that holds the module together or attaches it to a vehicle.

On Runco's numbers that moves the published benchmark from 2.13 down to roughly 1.78. The week
2 documents still argue against 2.13, which is the harder comparison, so the choice costs us
on our own side of the ledger and gains us nothing on theirs.

## D20: the low coefficient is two named allowances, one sized against a real section

2 September 2026, week 2.

The repository has carried 0.516 as a low thrust coefficient since the external research
round, always flagged as a caution rather than a published bound. Week 2 gives it a
construction instead of a provenance.

Nominal is 0.6055, recomputed from Benedict's quad rotor in this project's own blade-area
convention rather than quoted. The low value takes two allowances off it, added rather than
compounded because adding is harsher: 5 percent for blade flexibility and 10 percent for
configuration transfer. That gives 0.5147, or 85 percent of nominal.

The 5 percent is sized against the computed blade section. Bending stiffness is 66.8 Nm2 and
the tip deflects 0.086 mm under peak load; torsional stiffness is 9.6 Nm2 and the blade twists
0.054 degrees. Both are small, and Benedict found that bending and torsional flexibility both
hurt, so the allowance is not zero. It is generous against a section this stiff and it stays
generous until week 4 sizes the blade against centrifugal load.

The 10 percent carries the part nothing de-risks. Blade count, airfoil and chord ratio all
change at once in the transfer, and only the Reynolds half of it has published support.

This is still an engineering downside scenario. Not a published lower bound, and the
submission says so in those words.

## D21: the thrust sensitivity table is frozen, choosing a row is not a geometry freeze

2 September 2026, week 2.

D10 requires week 2 to freeze what raising thrust costs so week 4 cannot treat thrust as a
free knob under deadline. Four rows are frozen at 13, 16, 20 and 24 N, each carrying its mass
ceiling, ideal power, rpm, rotor torque and drive consequence.

20 N is the candidate row. Between 13 N and 20 N the mass ceiling grows 285 g while the drive
grows about 75 g, so raising thrust pays. Above 20 N it stops: the drive shortlist runs out at
555 W continuous and the next motor class costs more than the extra ceiling returns.

Freezing the table is not freezing the geometry. Week 4 may select from these four rows. It
may not invent a fifth.

## D22: week 2 reports BLOCKED and geometry does not freeze

2 September 2026, week 2.

The conservative case, meaning the low coefficient and the high mass column together, gives a
thrust to weight of 2.389 at the best point found. The hard limit is above 2.5 and D17 sets an
internal target of 2.75. Both are missed.

The plan's fallbacks were worked in the written order and none closed it. Higher thrust rows
peak at 20 N. The radius sweep peaks at 115 mm. There is no duplicated hardware to reject,
because the single rotor branch already won on its own. Revisiting the shape family reaches
2.481 at a blade aspect ratio of 6, and that number is not bankable, since leaving the family
the coefficient was measured in makes the transfer worse while chasing the target.

The shortfall is 32 g of conservative mass to reach 2.5, and 95 g to reach 2.75. Nominal
thrust to weight is 3.318, already 56 percent above the best published module on the same
boundary. Reaching 2.75 conservative needs a nominal of 3.82, which is 79 percent above the
published record, and nothing available supports it.

So this is a design finding rather than a failed week. Trimming the conservative mass
allowances to 10 percent across the board would give 2.564 and would clear the hard limit, and
doing that to make a number appear is the exact failure mode the blocked trigger exists to
prevent. That choice belongs to a person.

## D23: Kellen 2019 is a hard dependency now, not supporting evidence

2 September 2026, week 2.

The loop config classes the three unread papers as supporting evidence, which is why week 2
ran without them. Right at the start of the week, wrong by the end of it.

The whole gap between 2.389 and the hard limit sits inside the coefficient haircut. If
Kellen's measured blade-area coefficient for this shape family in this Reynolds band lands at
or above the transferred value, the 10 percent configuration-transfer allowance retires, the
haircut drops from 15 percent to 5, and conservative thrust to weight moves to roughly 2.68.
That clears 2.5 with margin while still sitting under the 2.75 internal target, so it would
turn a blocked week into a red one needing a margin decision rather than a design change.

No other single input available moves the answer that far. Kellen stops being a nice to have
and becomes the thing that decides whether this design closes. It is behind a Cloudflare
JavaScript challenge and needs a person with a browser, roughly two minutes of work. Unblock
steps are in `stage-1/progress/week-2.md`.

## D24: this tick ran against the .claude config while the plan still points at .codex

2 September 2026, week 2. Recorded as a deviation, not as a resolution.

`stage-1/plan.md` says the Codex config at `.codex/weekly-loop.md` is the execution contract
and that `.claude/weekly-loop.md` is history. The human who launched this tick designated
`.claude/weekly-loop.md` as the config and it is the newer of the two files, so week 2 ran
against it. Two differences mattered: the humanizer skill gets invoked before prose is written
to a file, and the git-commits skill owns the commit procedure.

The plan is not edited here. Two files each claiming to be the execution contract is a real
problem for a repeatable loop, and it needs a person to say which one wins rather than an
agent quietly picking. Carried as a debt.

## D25: no compliant point in this shape family sits inside the Reynolds band the coefficient is supported over

2 September 2026, week 2, after the audit. This does not supersede D12, it adds the axis D12
did not cover.

D12 gates the transferred coefficient on solidity, because solidity is the piece of the
configuration change that has a measured optimum attached to it. It also records the reason
the Reynolds half of the transfer was called safe: Shrestha and Benedict give non-dimensional
thrust as roughly invariant from 10,000 to 100,000.

The week 2 design point sits at a chord Reynolds number of 134,000. That is above the range,
so the Reynolds half of the transfer is an extrapolation and not an interpolation, and three
week 2 documents claimed the opposite before the audit caught it. The claim came from
substituting Kellen's study band of 100,000 to 300,000, which is where the figure of merit and
the solidity optimum live, for the band Benedict's coefficient was actually measured in.

Worse, it is not avoidable inside this family. The conservative thrust has to clear 10 N on its
own and the coefficient haircut is 15 percent, so design thrust cannot sit below 11.76 N.
Reynolds goes with the square root of thrust in this family, so the lowest compliant point is
already at 108,000. Every design that satisfies the gates is outside the documented band.

Two things stop this being fatal on its own. The direction is the benign one, since Shrestha's
result is that thrust holds while power falls, so pushing Reynolds up should not cost thrust.
And Kellen studied this exact shape family from 100,000 to 300,000 and reported it as the
optimum there, so the geometry is at home even if the coefficient is not.

Neither is evidence. It is one more reason geometry does not freeze this week, and one more
thing Kellen's measured coefficient would settle, since Kellen measured in the band the design
actually sits in.

## D26: literature.md is superseded on two points and is not rewritten

2 September 2026, week 2, after the audit.

`stage-1/literature.md` is week 1's deliverable and D1's convention is to leave superseded
documents standing rather than edit every one and risk leaving one stale. Week 2 overtook it in
two places and both are now marked in the file itself:

- The first-cut sizing table applies the shape family at Reynolds near 100,000, which was right
  for a 10 N design point and is not right for the 18 N one week 2 carries. See D25
- It says week 2 will bound the coefficient "with a low value derived from the spread in S2's
  own parametric results". Week 2 did not do that. No usable spread exists in the open
  literature, so the low value is two named allowances instead. See D20

The 0.607 against 0.6055 drift is a rounding difference and is not worth a note. The method and
the Reynolds statements are, so those two carry a dated pointer to this week's documents.

## D27: the audit moved the week 2 numbers, and these are the ones that stand

2 September 2026, week 2. Supersedes the figures in D18, D20, D21 and D22, and nothing else in
them.

Those four entries were written and committed before the week's own audit ran. The audit found
eighteen items, and fixing them moved the design point. The reasoning in all four entries
stands. The numbers do not, and rather than editing four entries in place, the corrected set
lives here.

**What moved and why.**

The conservative mass column now follows the rule the documents state for it. Blades and the
rotor shaft were taking the 15 percent catalogue rate while being built entirely from assumed
sections; they take 20 percent now. That alone cost 0.025 of conservative thrust to weight.

The mass envelope was resorted after the audit found three lines called fixed that scale. The
wiring harness follows the module envelope, the fasteners follow the frame, and the vectoring
servos are sized by a pitch link load that follows thrust. Sorted honestly, exactly one line in
this module is genuinely fixed: an 8 g controller board. That is a real finding in itself,
because D11 and D13 rest the thrust to weight case on fixed hardware amortising over more
thrust, and there is almost no fixed hardware to amortise.

The drive shortlist was wrong in two directions. It was missing two lighter and stronger real
motors, and it treated the datasheet figure as a continuous rating when T-Motor publishes it as
a maximum for 180 seconds. Week 2 now derates by 0.80 for continuous duty and checks power,
torque and attainable speed together rather than power alone. The selected motor changed to the
MN5006 KV450, which is lighter than the previous choice and carries more.

**The figures that stand.**

| | Value |
| --- | --- |
| design thrust | 18.0 N, with the table frozen at 13, 16, 18 and 20 N |
| radius | 110 mm, second candidate 120 mm |
| conservative thrust to weight | 2.252 |
| nominal thrust to weight | 3.163 |
| shortfall to the 2.5 hard limit | 69 g of conservative module mass, 9.9 percent |
| shortfall to the 2.75 internal target | 125 g, 18.1 percent |
| single against two and three rotors | 2.252, 1.659, 1.323 |
| selected drive | MN5006 KV450 at 3.5 to 1, 88 percent of derated continuous power |

D20's construction of the low coefficient also needs one correction. It said the 5 percent
flexibility allowance was sized against the computed blade section. It was not, and no
arithmetic connects a 0.078 mm tip deflection to a 5 percent thrust loss. The section bounds
the allowance from above and says it should be well under 1 percent. The 5 percent is a floor
covering build tolerance, bond line variation and unsteady effects the section does not model,
and it is kept because the section is preliminary.

D22's conclusion is unchanged and is now further from closing than it was. The week reports
BLOCKED.

**One thing the audit made better rather than worse.** The design is drive limited, not
aerodynamics limited and not structure limited. Conservative thrust to weight keeps rising as
the radius falls, and the 100 mm row would give 2.376, but no motor in the shortlist can hold
it: the torque wants a belt ratio the KV450 cannot spin to on a 6S pack, and the motor that has
the speed does not have the torque. So the radius is 110 mm because that is the smallest a
named drive can hold, not because it is where the design wants to be. That points at a cheap
unblock nobody had identified before the audit, and it is in the progress file.

## D28: one execution contract, and it is the Claude config

2 September 2026, after the week 2 checkpoint. Resolves D24.

Week 2 ran with the plan naming `.codex/weekly-loop.md` as the contract and the human naming
`.claude/weekly-loop.md`. The week-agent recorded the conflict and refused to resolve it
itself, which was the right call. Resolving it now.

`.claude/weekly-loop.md` is the contract for every runner. It is the newer file, it is the
stricter one, and it carries two rules the Codex copy had dropped: invoke the `humanizer`
skill before writing prose, and invoke `git-commits` for the commit procedure. Both are
binding from the global rules regardless of which runner executes a tick, so a config that
omits them is wrong rather than merely different.

`.codex/weekly-loop.md` is reduced to a pointer plus its own sentinel path. A runner needs a
separate sentinel so a tick that dies under one runner is not read as partial work by the
other. Everything else is inherited, so the two cannot drift again.

The plan said the opposite and is corrected.

## D29: gate output must not describe a failure that did not happen

2 September 2026, after the week 2 checkpoint.

The supervisor found `PASS  week2: the design thrust is one of the prequalified rows  18.0 N
not among [13.0, 16.0, 18.0, 20.0]`. The predicate was right and 18.0 is in the list. The
detail string was shared across both branches of `report()`, so a passing check printed the
wording written for its failure.

Cosmetic in the sense that nothing was mis-gated, and not cosmetic in the sense that this is
the one artifact a human reads to decide whether a week is sound. `report()` now takes an
optional `fail_detail` shown only when the check fails, and the two sites that were failure
worded use it.

## D30: geometry freezes on the design case, and the stacked downside becomes a week 4 gate

31 August 2026, after week 2 reported BLOCKED. Supersedes the freeze rule in D17 and answers
the decision D22 stopped for.

Week 2 came back at a stacked conservative thrust to weight of 2.2525 and halted, which is
what the loop config told it to do. The call it was waiting for is made here.

**What the four cases say.** The design point is 18 N on a 580.05 g module, giving 3.1633.
The mass downside on its own, meaning the 692.43 g conservative column at full thrust, gives
2.6499. The coefficient downside on its own, meaning 15.3007 N on the nominal mass, gives
2.6889. Only stacking both misses, at 2.2525. All four reproduce from the geometry.

So the design clears the competition limit by 27 percent and each downside alone clears it by
about 6. The miss appears when two independent allowances multiply.

**Why the stacked case is the wrong thing to freeze on in week 2.** Nine of the thirteen
envelope lines say "assumed" in their basis and carry a blanket 20 or 25 percent growth rate.
The stacked number tests those growth rates as much as it tests the design. Week 4 replaces
the assumed sections with real ones, catalogue parts and a BOM, and
`week4: conservative T/W clears 2.5` already applies the same limit to that refined budget.
The hard test exists. It sits one week later, where the mass is real.

**What was rechecked before deciding**, by hand rather than read back from the week 2 report:

- Higher thrust. 20 N wants 535.92 W at 110 mm against 520 W continuous, so it fails on power
  before anything else. At 120 mm the power fits at roughly 491 W, but the belt ratio has to
  clear 4.191 for torque and stay under 3.986 for speed, so the window is empty
- Smaller radius. The 100 mm row gives 2.3759 and is the best point on the sweep. Its window
  is empty too: torque wants a ratio above 3.143 and the speed rule caps it at 2.918. That
  holds for any pulley pair, not only the half integer ones week 2 searched, so the row is
  properly closed and not closed by rounding
- A lighter drive. Nothing in the shortlist reaches 503 W under 78 g. Best power density on
  the table is the MN4006 at 6.7 W per gram, which at 78 g would give 416 W continuous
- Trimming the growth rates. A uniform 10 percent gives 2.44 and still misses, and trimming
  an allowance until the number appears is the failure mode the blocked trigger exists for

None of it closes. The gap sits inside the coefficient haircut, where D23 put it.

**Kellen stays unobtained and the decision no longer waits for it.** The OAKTrust item, its
bitstream and the handle URL all return 403 behind a Cloudflare JavaScript challenge. A real
browser passes it in seconds, so it stays a human task, and it is still the cheapest thing
available, because it moves the stacked case to 2.5173 on its own. Nothing here depends on it.

**What changes.** Geometry freezes at 18 N and 110 mm, 120 mm carried as insurance. Week 2's
copy of the stacked gate is replaced by four: the design case, the mass downside alone and the
coefficient downside alone each have to clear 2.5, and the stacked figure has to be stated and
reproduce. A stacked miss now hands week 4 a computed mass target that the gate recomputes,
rather than a paragraph. That target is 623.9 g, which is 68.5 g below the conservative column
and 9.9 percent of it.

**The direction of this change, stated plainly.** It unblocks a week that was blocked, and
that is worth saying rather than burying. What makes it a restructure and not a trim is the
ledger. Week 2 goes from one thrust to weight gate to four plus a conditional target gate,
week 4 keeps the hard stacked test on refined mass, and no assumption moved. The coefficient
haircut, the 0.80 derate, the 90 percent speed rule, the growth rates and the 2.5 limit all
stand exactly where week 2 left them.

**One lead nobody has priced.** Pack voltage sits outside the module boundary, so cell count
is free on module mass. Motor torque ceiling goes as current over KV and speed ceiling as KV
times voltage, so their product is electrical power and carries no KV term at all. Fixing
KV450 on 6S and then searching only the belt ratio imposed a constraint the motor's power
rating does not impose. A lower KV variant on a higher cell count would reopen the 100 mm row.
Week 4 confirms the drive anyway and should price this properly. It is not used here because
overvolting a 6S rated motor needs a datasheet nobody has opened.

## D31: the stacked shortfall is a 623.9 g mass target, and it can retire from either side

31 August 2026, week 2 second run. Implements the target D30 asked for.

D30 moved the hard stacked test to week 4 and said a week 2 miss has to hand week 4 an
arithmetic target rather than a paragraph. This is that target and the reasoning behind the
number.

**The value.** 623.8818 g, stored as `results.mass_target_week4_g`. It is the conservative mass
that puts the stacked case exactly on 2.5 at the conservative thrust of 15.3007 N, so it is
15.3007 over 2.5 times 9.81, in grams. The gate recomputes it from the stored thrust and
rejects a stated value that misses by more than half a percent, which is why nothing here is a
round number chosen for comfort. Against the 692.43 g conservative column that is 68.5 g, or
9.9 percent.

**Where the 68.5 g is expected to come from.** Eight envelope lines carry a 20 or 25 percent
growth rate on an assumed basis: blades, rotor frame and hubs, pitch mechanism, rotor shaft,
frame and mounting hardware, transmission, wiring harness, fasteners and bonded joints. Between
them they hold 86.4 g of the 112.4 g total allowance. Week 4 draws real sections and quotes
catalogue parts, so those rates fall to what a weighed estimate deserves rather than what an
assumed one does. Retiring those eight to a uniform 10 percent gives back 45.7 g on its own,
which is two thirds of the gap and not all of it. The rest has to come out of the nominal
lines, and the softest of those are already named in the week 2 progress file: the shaft torque
allowance at 18 g per Nm, the fastener and bonded joint line at 22 g, and the 16 g harness.

**Trimming a growth rate to make the number appear is not a retirement path.** The rate falls
because a line stopped being assumed, or it does not fall. That distinction is the whole reason
the blocked trigger exists and D30 left it standing.

**The target can also retire from the thrust side, and that is worth knowing before week 4
spends effort on mass.** The 15 percent coefficient haircut is 10 points of configuration
transfer plus 5 of blade deflection. If Kellen's measured coefficient comes in at or above
0.6055 for this shape family, the transfer allowance retires, conservative thrust goes to 17.1
N, and the mass that clears 2.5 becomes 697.2 g. That is above the 692.43 g the module already
weighs in the conservative column, so the target disappears entirely and week 4 inherits no
shortfall. One browser session decides which of the two problems week 4 is actually solving.

## D32: every document that quotes the design case also carries the stacked one

31 August 2026, week 2 second run.

Week 2 spent most of its length reporting one conservative thrust to weight and D30 showed
there were four cases in the data the whole time. The design case at 3.163 is the honest
headline and 2.252 is the honest caveat, and a document that carries the first without the
second is selling the reader a number.

So the rule for weeks 3 to 5: any document stating the design thrust to weight also states the
stacked conservative figure, what it misses by, and where the test now lives. That is four
cases in the design documents and in the submission, not one. The evidence ledger says the same
thing about the freeze rule it originally published, because that rule changed after the
numbers arrived and a ledger that quietly shows the new rule is worse than useless.

The week 2 half of this is mechanical rather than a promise. Each of the three week 2 design
documents has to quote a number within half a percent of the recomputed stacked figure, at any
rounding, and a document that drops it fails the week. Weeks 3 to 5 are on the audit, because a
gate cannot tell which numeric token in a document is meant to be a thrust to weight.

The cost of this is a paragraph per document and some repetition across five of them. The
alternative is a Stage 2 team reading 3.163, building to it, and finding out from a scale.

## D33: week 4 builds its conservative column line by line, it does not state a total

31 August 2026, week 2 second run, after the audit.

D30 moved the hard stacked thrust to weight test into week 4 and called that a restructure
rather than a trim, on the grounds that the test still exists and only the mass under it gets
better. The audit went and read the week 4 gate. The test reads `results.mass_g_conservative`,
which was a single stored scalar with nothing behind it: `check_budget_continuity` groups the
refined budget against the nominal column only, and the sole constraint on the conservative
number was that it not be lighter than the nominal budget total.

So week 4 could have cleared the gate by picking a growth rate that lands the total under 623.9
g. That is the move the blocked trigger forbids, and it was reachable through the gate D30 named
as its mitigation. The mitigation was thinner than four documents said it was.

**What changes.** Every `mass_budget_g` line carries a `conservative_g` alongside its `mass_g`.
No line is allowed to be lighter in the conservative column. `results.mass_g_conservative` has
to equal the sum of those lines to half a percent, and the sum has to be at least 105 percent of
the nominal budget, which is the rule week 2 already applies to its envelope. Three self-tests:
a conservative total the lines do not give, a line that shrinks under growth while its neighbour
pays for it, and the honest budget that has to keep passing.

The growth rate can still be argued line by line, and it should be. What it cannot be any more
is one number chosen after seeing the target.

## D34: the week 2 documents follow the number, not the other way round

31 August 2026, week 2 second run, after the audit.

D32 put the stacked figure into all three week 2 design documents and a gate makes sure it stays
there. The gate compares against the recomputed stacked thrust to weight, and week 2's gates run
again on every later week, so the moment week 4 refines the conservative mass the recomputed
figure moves and the three frozen documents fail on the old one.

That reads like a trap and it is the right behavior. Those three documents are Stage 1 items 1,
2 and 4, and week 5 builds the submission out of them. A document that still says 2.252 while
the refined budget says 2.55 is wrong, and finding out at week 4 is much cheaper than finding
out from a reader.

So: geometry is frozen, the documents are not. Week 4 restates the stacked figure in
`01-configuration.md`, `02-rotor-sizing.md` and `04-thrust-and-power.md` when the mass moves,
and the gate's failure message says so. Frozen means the design stops moving, not that the prose
stops tracking it.


## D35: Kellen's measurement retires the configuration-transfer allowance

31 August 2026, after both primary sources were retrieved and read.

D23 set the test in one sentence: if Kellen's measured blade-area coefficient for this shape
family in this Reynolds band lands at or above the transferred value, the 10 percent
configuration-transfer allowance retires. The thesis is in hand and it passes the test.

**What was measured.** Kellen's Table 2.1 configuration 8 is a 3-bladed rotor, 5.5 in chord,
8.25 in radius, 22 in span, NACA 0020, run at pitch amplitudes up to plus or minus 40 degrees.
That is this design's shape family: chord-to-radius 0.6667 against our 0.66, solidity 0.3183
against our 0.3151, blade aspect ratio 4.0 in both, three blades and the same airfoil and the
same pitch amplitude. Solidity and chord-to-radius agree to 1.1 percent.

**How the number was got.** Kellen tabulates no coefficients. CT/sigma lives inside figures, so
it was read out of the PDF's vector path data rather than off pixels: the axis calibration is
the tick geometry, and the data points are the polyline vertices. Fig 3.25 gives 1.04424 at
three blades and Fig 3.28, drawn separately against solidity, gives 1.04428. They agree to 0.003
percent.

His conventions are on p.vii: A is the projected area, span times 2R; CT is TRes over rho A
(Omega R) squared; sigma is Nb c over 2 pi R. This project divides thrust by 0.5 rho (Omega R)
squared times blade area. Substituting one into the other, the rho, the areas and the speeds all
cancel and what is left is a constant:

    coeff = (2/pi) x (CT/sigma)

So 1.0443 becomes 0.6648.

**Why it is believable.** Two closures, both independent of the reading and both tied to
quantitative claims in Kellen's own text. Taking CP/sigma off Fig 3.26 for the same rotor and
computing FM = CT^1.5 / (sqrt(2) x CP) gives 0.595, against the 0.6 section 3.3 states for
exactly this configuration. And computing power loading at the 60 N/m2 fixed disk loading the
text names for Fig 3.27 gives 0.1202 N/W against the 0.1201 that figure plots. Neither closure
depends on the span, so neither can be rescued by a lucky guess about the rotor.

**What changes.** The low coefficient becomes 0.5752, the nominal less blade flexibility alone.
Conservative thrust becomes 17.0992 N. The stacked conservative thrust to weight becomes 2.5173,
which clears the hard limit of 2.5, so `results.mass_target_week4_g` describes a shortfall that
no longer exists and is deleted along with its source entry. The gate stops asking for that field
once the stacked case clears, so leaving it would have parked an unchecked number in the schema.

**What does not change.** The blade-flexibility allowance stays at 5 percent. Nominal thrust,
geometry, rpm, the power chain, the drive and the mass envelope are all untouched. The low
coefficient is still an engineering downside scenario rather than a published lower bound, and
the evidence ledger still says so.

**What it clears by, stated because it is thin.** 2.5173 against 2.5 is 4.8 g of conservative
mass. The column could reach 697.2 g before the stacked case fell under the limit and it sits at
692.4 g. The hard stacked test in week 4 under D30 is still the one that matters, and D33 still
governs how that column gets built.

## D36: the nominal coefficient stays at 0.6055, and the record of where it came from is corrected

31 August 2026, same reading session as D35.

Benedict 2010 was pulled to check the basis under `performance.blade_area_coeff`. The basis was
wrong.

**What the repository carried.** 1.98 N per rotor at 2000 rpm on the quad-cyclocopter, four
NACA 0010 blades of 33.0 mm chord and 158.8 mm span at 76.2 mm radius. That arithmetic does give
0.6055, so it reproduced every time anybody checked it, which is why it survived a week 1 pull
and two week 2 audits.

**What the dissertation says.** The pair does not appear in it. 1.98 N is the 809 gram all-up
vehicle weight of Table 5.1 divided by four, and the quad never hovered untethered at its own
weight. 2000 rpm belongs to the twin rotor. The quad's measured hover point is on printed p.236:
at the operating RPM of 1800, each rotor produced around 1.91 N of thrust. Printed p.225 gives
the same point as 195 grams at 1800 rpm and 40 degrees pitching amplitude. In this project's
convention that is 0.7211. The chord Reynolds of that rotor is 31,600, not the 35,100 the ledger
carried, because that too was computed at 2000 rpm.

Two mistakes that pulled in opposite directions. The thrust was too high by 3.7 percent and the
speed was too high by 11 percent, and since thrust goes as the square of speed the net was a
coefficient 16 percent below the truth.

**The decision: 0.6055 stands.** Every measured or corrected value now available sits above it.
Kellen measures 0.6648 on this shape family, the corrected quad point is 0.7211, and Benedict's
twin is 0.8114. Raising the nominal would raise design thrust everywhere it is used, move rpm,
power, torque, the drive selection and every mass line that scales with them, and it would spend
a margin nothing in the design is asking for. An error that ran in the safe direction is not a
reason to go back and remove the safety.

So the number is unchanged and its status is not. It was a transferred estimate that happened to
be low. It is now a deliberate floor, held below three separate measurements, and both
`numbers.json` and the evidence ledger say that in those words. The correction is recorded here
rather than applied, because a value that quietly stops matching its own stated basis is worse
than one that never matched it.

**What this does not license.** Nobody may quote 0.7211 or 0.6648 as the design coefficient in a
later week and recompute thrust upward from it. Those two are reserve. If a later week wants the
margin, that is a decision entry, not an edit.

## D37: D25 narrows to the provenance of the nominal, and no longer to the design point

31 August 2026. Narrows D25. Does not supersede D12, and does not touch the solidity axis.

D25 said no compliant point in this shape family sits inside the Reynolds band the coefficient is
supported over. The support it meant was Shrestha and Benedict, non-dimensional thrust holding
from 10,000 to 100,000, and the design point at 134,000 sits above it. That was correct on the
evidence available and it is why three week 2 documents had to be corrected after the first
audit.

Kellen changes what the sentence covers. The thesis abstract states the study range as chord
Reynolds 100,000 to 300,000, Table 2.1 lists all 37 configurations tested inside it, and the
3-bladed optimum sits at 186,000 on a 5.5 in chord at 20 m/s. The design point at 134,074 is
inside that band, on this design's own shape family, with a measured blade-area coefficient
attached to it.

**What survives, stated narrowly.** The nominal coefficient still comes from a Benedict rotor at
a chord Reynolds of 31,600, and Shrestha is still the only published support for carrying a
value across that gap. That specific transfer is still an extrapolation and E11 still carries it.

**What does not survive.** The claim that no compliant design in this family can sit inside a
measured band. It can, and this one does. D25 also argued the point was unavoidable because the
15 percent haircut forced design thrust above 11.76 N and put the floor at 108,000. The haircut
is 5 percent since D35, so the floor is 10.53 N and Reynolds there is 102,500, which is inside
Kellen's band as well. Every compliant point in this family now sits inside a band this shape was
measured across.

**Why this is a narrowing and not a reversal.** D25's underlying complaint was that a number was
being carried further than its evidence reached. That is still true of the nominal. What is no
longer true is that the geometry and the design point are out on their own, because the shape
family has its own measurement bracketing them. The risk moved from the design point to the
provenance, and the provenance is what D36 answers by holding the value low.

D25 is not edited. This entry is where the qualification lives.

## D38: the pitch link is 105 mm, picked by sweep, and only the horn is scaled from Kellen

31 August 2026, week 3. Freezes the linkage geometry.

The topology comes from Kellen, who names four fixed lengths and built the thing twice. L1 is the
rotor radius, L2 the offset link, L3 the pitch link, L4 the horn. On his cyclocopter those are 9
in, variable, 9.133 in and 2 in, printed pages 55 and 56.

Scaling both ratios to this radius gives a 24.4 mm horn and a 111.6 mm pitch link, and that
combination works. It is not the one to build. Running `tools/linkage.py --sweep` over horn
lengths of 18 to 36 mm and pitch links of 100 to 118 mm shows 111.6 mm sitting at 0.297 Nm of
carrier torque, a transmission angle floor of 40.97 degrees and a harmonic residual of 2.67
degrees, against 0.137 Nm, 58.58 degrees and 1.195 degrees at 105 mm with the same horn.

Four times the torque on the part a 12.5 g servo has to hold is the number that decided it. At
111.6 mm the two servos together cannot hold the carrier on half of their stall torque. At 105 mm
the margin is 2.36.

**What is frozen.** L1 110.0 mm from week 2, L2 15.40 mm, L3 105.0 mm, L4 24.4 mm, open assembly
mode, construction angle -110.524 degrees. L2 is the only one solved rather than chosen:
bisecting on peak to peak pitch travel is what puts it at 15.40 mm for plus or minus 40 degrees.

**Why the horn ratio survived and the link ratio did not.** The sweep is flat in horn length over
20 to 26 mm and steep in link length. Kellen's rotor is twice this radius and runs a different
offset regime, so there was never a reason to expect both ratios to carry across, and only one
did.

## D39: azimuth is measured from the offset link, not from module vertical

31 August 2026, week 3. Sets the convention every week 3 table is written in.

Two conventions were available and they put different numbers in `pitch.phase_delay_deg`.
Referencing azimuth to module vertical makes the stored delay minus the aerodynamic tilt, which
is a restatement of the side force number under a name that says pitch mechanism. Referencing it
to the offset link makes the stored delay the lag between the command and the pitch peak, which
is a property of the four-bar and of nothing else.

**The convention: 90 degrees of azimuth is the direction the offset link points.** The mechanism
then lags its own command by 11.00 degrees, and module vertical sits 11.978 degrees further round
because the aerodynamics adds its own tilt on top. Both numbers are stored, separately, and
neither is derivable from the other.

This is worth writing down because it is not the obvious choice and a later reader will want to
know why the pitch peak is at 101 degrees rather than at 90. `aero_azimuthal_loads` uses the same
azimuth column, with its two force components resolved in module axes, so the load table and the
schedule table can be read side by side.

## D40: the drive is single ended, because the pitch link sweeps through the rotor axis

31 August 2026, week 3. Constrains packaging and hands week 4 a shaft that stops short.

With all three pitch links converging on one offset pivot, the link belonging to the blade
furthest from the offset passes within 0.004 mm of the rotor centreline. That is a crossing, not
a near miss, and it is structural rather than unlucky: it happens whenever L3 minus L2 falls
inside the band L1 minus L4 to L1 plus L4, which for this link set is 89.6 mm to 134.4 mm against
an actual 89.6 mm.

**So the plane the pitch links sweep cannot contain the rotor shaft.** The shaft runs the span,
carries both main bearings and stops inboard of that plane. The rotor is driven from the other
end, where the belt pulley has the axis to itself. The offset pivot is fed by a post reaching in
from a phasing carrier that turns about the axis outboard of everything rotating with the rotor.

Kellen hit the same constraint and solved it differently, by shaping L3 to bend around the
central hardware. A cranked link carries bending as well as tension and it is a harder part to
make, so the end split is the better trade here.

**What this costs.** Nothing coaxial may sit in the pitch plane, and week 4 cannot answer a shaft
stiffness problem by running the shaft through to an outboard bearing on that side.

## D41: the azimuthal load model is rerun on the solved schedule, and week 2's table is replaced

31 August 2026, week 3. Supersedes the `aero_azimuthal_loads` table frozen in week 2 and the peak
to mean figure that came out of it.

Week 2's model prescribed a sinusoid with no phase offset. Its lateral components cancelled
exactly over the cycle, so the model reported zero side force as an input rather than as a
result, and week 2 said so at the time.

The model itself is kept and only its input changed. `tools/linkage.py` reconstructs it from
`04-thrust-and-power.md` and reproduces the published week 2 table to 5.2e-5 N on every one of
its 36 rows, which is what makes this a rerun rather than a new model. Two things then change.
The schedule is the one the four-bar produces. And the uniform inflow now points opposite the
resultant it helped produce, instead of being pinned to module vertical.

**What moved.** Peak blade load goes from 14.24 N to 15.01 N and peak to mean from 2.374 to
2.501. The upper and lower halves of the revolution stop mirroring each other, because that
mirroring was a property of the prescribed sinusoid. The lateral column is no longer zero: its
cycle mean is trimmed out by pointing the offset 11.978 degrees off vertical, and the
instantaneous lateral force still reaches 10.10 N per blade inside the cycle.

**What did not move.** The cycle mean vertical force is still 6.0000 N per blade and still
reproduces the 18.0 N design thrust across three blades, which is the week 2 gate. Nothing in the
mass envelope moved. Week 4 still sizes structure on the 4.0 peak to mean of D16 rather than on
2.501, because a quasi-steady model with uniform inflow under-predicts the peak.

`04-thrust-and-power.md` carries one load model and not two.

## D42: phase authority is 120 degrees, and the gate now tests the force map rather than two scalars

31 August 2026, week 3. Freezes the vectoring claim and changes `tools/check.py`.

The authority is a gear ratio and two published numbers, not a property of angles. The servo's
operating travel is 80 degrees, 40 per side. The phasing carrier is a ring around the rotor axis
and its gear cannot be much under 40 mm because it has to clear the offset post at 15.4 mm
radius. Putting a 60 mm sector gear on the servo makes that a 1.5 step up, so 80 degrees of servo
becomes 120 degrees of carrier. A larger step up needs a sector gear the module cannot carry.

**`pitch.vector_range_deg` is set equal to that**, because the model's map does support one to
one direction control. Five commands across the range turn the resultant by exactly the command
and hold its magnitude at 18.000 N. Be honest about why that is so clean: the rotor is
axisymmetric, the blades are evenly spaced and the inflow settles onto whichever direction the
resultant points, so rotating the command rotates the entire solution. It is a statement about
the model's symmetry and about the mechanism's reach, and not a measurement of force at any
command.

**The gate changed with it.** `check.py` compared `vector_range_deg` with `phase_authority_deg`
and nothing else, which only checks that the same number was written twice. Three new checks now
read the force table: every mapped command has to sit inside the authority, the commands have to
span at least half the claimed range, and the direction the forces imply has to turn with the
command to within 15 degrees. Two more read the load table: the cycle mean lateral force has to
be trimmed to within 5 percent of the mean vertical, and `pitch.peak_lateral_force_N` has to
reproduce from the rows.

Five attack cases went into `tools/test_gates.py` alongside them, one per new check, and each was
confirmed to fail on the gate it targets rather than incidentally. `linkage_selftests` was added
in the same file and it is the one part of that suite that reads the real repository: it
recomputes the four-bar loop closure on every published pitch row, and confirms that one degree
of hand editing and a target cosine both break it. The suite went from 104 self-tests to 115.

Nothing was loosened. `snum` was added because `num` rejects zero and negative values, which
would have silently dropped every phase command at or below zero out of the new checks.

## D43: the blade is not chordwise balanced, and the stored pitch loads are the unbalanced ones

31 August 2026, week 3. Hands week 4 a trade rather than making it.

The pitch axis is frozen at 30 percent chord. Building the blade the way `02-rotor-sizing.md`
describes puts its centre of mass at 39.92 percent, because the foam sits at the section centroid
and the skin sits further aft still, and only the spar and the root fittings sit on the axis.

On a cyclorotor the rotation axis runs parallel to the blade span, so centrifugal force acts in
the section plane and an unbalanced blade gets a steady moment trying to swing its chord radially
outward. That moment scales with the offset. At 9.92 percent of chord it doubles the peak blade
pitching moment, from 1.0139 Nm balanced to 2.1201 Nm as built, and takes the peak pitch link
force from 69.38 N to 101.82 N.

**The stored numbers are the unbalanced ones.** They describe the blade that exists on paper
today. `tools/linkage.py --balanced` prints the other case and refuses to write it, because a
target is not a design.

**What week 4 decides.** A nose balance mass on the pitch axis side would take the link load back
down and cost module mass, against a conservative column that clears 2.5 by 4.8 g. Moving the
spar forward or biasing the skin lay-up would do some of it for free. Neither is a week 3 call,
and both need the real section week 4 builds.

The actuator is not the reason to care. Even unbalanced the carrier torque is 0.1371 Nm and the
servo margin is 2.36. This is a pitch link strength case.

## D44: the week 2 packaging rule understates the module, and the comparison it made still stands

31 August 2026, week 3. Corrects a week 2 figure without reopening the week 2 conclusion.

`01-configuration.md` compares layouts on rotor count times 2R, plus 20 mm of clearance and 40 mm
of frame. For the single rotor that is 280 mm against a 290.4 mm span, so the span won and 290 mm
went into the table as the largest dimension.

2R is the wrong circle. The blade pitches plus or minus 40 degrees about an axis at 30 percent
chord, so 70 percent of a 72.6 mm chord swings outboard and the swept diameter is 296.1 mm rather
than 220. Sampling the section outline at every rotor position is what gives that.

**The ordering does not move.** Applying the swept diameter to the same rule gives 356 mm for one
rotor, 491 for two and 585 for three, so the single rotor still wins on size and wins by more
than the old figures said. The week 2 table is left as it is, because it is one rule applied to
all three layouts and correcting only the winning row would be worse than leaving it alone.

`09-packaging-and-integration.md` carries the real envelope, 364.4 by 316.1 by 362.1 mm, built as
a sum of named parts. The largest dimension is along the rotor axis and the span still drives it.

## D45: the week 3 audit corrects four figures inside D38, D40, D42 and D44

31 August 2026, week 3, after the audit. Corrects D38, D40, D42 and D44 without reopening any of
the decisions they carry. The log is append only, so the corrections live here.

The audit is in `stage-1/audit/week-3.md`, verbatim, with 16 findings and what was done about
each. Five of them landed on numbers already written into a frozen entry.

**D38's sweep figures were stale.** It quotes 0.297 Nm of carrier torque for the 111.6 mm pitch
link and says that is four times the 105 mm figure. Both come from a sweep run before the
resultant magnitude normalisation was corrected, and the delivered sweep gives **0.3240 Nm**
against 0.1371 Nm, a ratio of **2.36** rather than four. D38 also says the two servos "cannot
hold the carrier on half of their stall torque" at 111.6 mm. They can, on a margin of exactly
**1.000**, which is not a margin but is not a failure either.

The decision stands. 105 mm still wins on carrier torque, on transmission angle by 18 degrees and
on harmonic residual by half, and 2.36 times is still the number that decided it.

**D40's band arithmetic was wrong.** It says the reachable band is 89.6 to 134.4 mm. L1 minus L4
is 110.0 minus 24.4, which is **85.6** mm, so the band is 85.6 to 134.4 and the actual 89.6 mm
sits 4 mm inside it rather than exactly on its edge. The symbolic version in
`03-pitch-and-vectoring.md` was already right. The conclusion is unchanged and is now less of a
knife edge than D40 made it look.

**D42 overstates what the new gate can catch, and undercounts it.** `check_vector_map` emits four
reports, not three, so week 3 added six checks rather than five. More importantly: against this
solver the direction tracking check cannot fail. The model is rotationally equivariant, so
rotating the command rotates the whole solution and the map is an exact rotation by construction.
What the check actually catches is a hand-written or flat force table, which is what the old two
scalar comparison let through, and that is the claim to make for it. One of the five attack cases,
the command outside the authority, trips two gates rather than one.

**D44's cluster figures used a different rule from the one it cites.** Week 2 gives each rotor its
own 20 mm of clearance, so on the swept diameter the cluster figures are **510.6 mm** for two
rotors and **624.8 mm** for three, not 491 and 585. The single rotor figure of 356 mm is right.
The ordering conclusion was never in doubt under either arithmetic.

**And one thing the audit found that no decision had covered.** `tools/linkage.py` checked its
reconstruction of the week 2 load model against the live `aero_azimuthal_loads`, which `--write`
had already replaced with the week 3 table. The script therefore ran once and then refused to run
at all, which defeats the reason for having it. The week 2 published table is now a constant in
the script, `WEEK2_PUBLISHED_LOADS`, tagged with the commit it came from. That was the worst
finding in the set and it was invisible from inside the session, because the script was only ever
run before `--write` or in the same breath as it.

**What went into the gates as a result.** `lateral_force_N` is now a required field on
`aero_azimuthal_loads` and `pitch.peak_lateral_force_N` joined week 3's positive list, because
deleting the column and its stated peak left every gate green while removing the load week 4
inherits. Two attack cases went in with them. 115 self-tests to 117.
## D46: the blade stays unbalanced, because balancing it costs the thrust to weight case

31 August 2026, week 4. Closes the trade D43 handed over. D43 is not superseded and the stored
pitch loads are still the unbalanced ones.

The blade centre of mass sits at 39.31 percent of chord against a pitch axis at 30, so 6.759 mm
of chordwise offset. Centrifugal force on that offset is a steady pitching moment on every
blade, and it is most of the 2.2058 Nm peak and most of the 105.93 N in the pitch link.

Moving the centre onto the axis means lead at the nose. A slug at 5 percent chord needs 11.82 g
per blade and 35.47 g for the set. That takes the module from 607.97 to 643.44 g nominal and
from 684.70 to 724.42 g conservative, and the stacked conservative case falls from 2.5457 to
2.4061, under the hard limit of 2.5. Buying it would break the requirement the whole week exists
to test.

**What the mass would have bought is a margin that is already adequate.** The pitch link path is
governed by the horn at 349.727 N, so the unbalanced 105.93 N sits on a margin of 3.30 against a
floor of 1.5. Balancing takes the link to about 69.4 N and the margin to 5.04. Paying 35.47 g to
move a margin from 3.30 to 5.04 is not a trade this module can make.

Three things ride on this and they are named so a Stage 2 reader can find them. The pitch
bearings carry a steady 110 N each while swinging through 80 degrees, which is an oscillating
fretting duty a static rating does not describe. The blade winds up 2.35 degrees in torsion
under the same moment. And the link load is fully reversed at 40 Hz. If any of the three fails
its Stage 2 check, balancing is the first move, and by then the mass may have somewhere to come
from.

## D47: the conservative module mass is the refined budget's own column

31 August 2026, week 4. Extends D33 and answers what D31 expected. Supersedes nothing.

`results.mass_g_conservative` was the sum of the week 2 envelope's conservative lines, 692.43 g.
It is now the sum of the refined budget's conservative lines, 684.70 g, and `check.py` reads the
budget whenever a budget of 8 or more complete lines exists, the envelope only while it does
not.

Binding the scalar to the envelope for ever would have pinned the refined column to the estimate
it exists to replace, to half a percent. D31 expected the assumed growth rates to retire against
real sections, and D34 warned the week 2 documents that the stacked figure would move under them
when they did. This is that move, and it is the only week where it can happen without breaking
an earlier gate.

Nothing is unbound by it. Whichever column is live, the stated scalar has to equal a sum of per
line figures, no line may shrink under growth, and the total must clear 105 percent of its own
nominal. The refined column carries a further rule the envelope never had: it has to stay within
25 percent of the week 2 conservative envelope, so a week 4 budget cannot describe a module its
own estimate never described. 684.70 against 692.43 is 1.1 percent.

The four case table in `02-rotor-sizing.md` now mixes columns and says so. Rows 1 and 3 keep the
week 2 nominal envelope, because those are the rows geometry froze on. Rows 2 and 4 carry the
refined conservative mass. The stacked case moved from 2.5173 to 2.5457 and the clearance from
4.8 g to 12.5 g.

## D48: the pitch loads follow the drawn blade, so week 3's mechanism numbers move about 1 percent

31 August 2026, week 4. Retires debt 11 of week 3. D38 and D42 stand: the geometry did not move
and neither did the claim.

`tools/linkage.py` carried `BLADE_PARTS_G` as a hand copy of the week 2 blade build-up, and week
3 recorded that nothing would make it follow a change to the blade. Week 4 changed the blade.
The constant is gone and the build-up now comes from `tools/structure.py`, the same integration
that writes the blade budget lines, so the pitch loads and the mass budget cannot disagree about
what a blade weighs.

Two things moved inside the blade. Integrating the NACA 0020 perimeter gives 2.090 chords rather
than the assumed 2.05, so the skin is 9.69 g instead of 9.51. Drawing the root close-out as two
7075-T6 fittings over the spar plus a bond line gives 6.65 g instead of a lumped 4.53 g
allowance. Per blade the mass is 31.75 g instead of 29.4 g.

Everything downstream moved with it, by about 1 percent in each case except the last:

| Quantity | Week 3 | Week 4 |
| --- | --- | --- |
| blade centre of mass | 39.92 pct chord | 39.31 pct chord |
| peak blade pitching moment | 2.1201 Nm | 2.2058 Nm |
| peak pitch link force | 101.82 N | 105.93 N |
| carrier torque | 0.1371 Nm | 0.1389 Nm |
| servo holding torque, each | 0.0457 Nm | 0.0463 Nm |
| servo margin on half stall | 2.363 | 2.332 |
| offset post radial pull | 47.48 N | 53.22 N |

The offset post moved 12 percent, not 1, because the radial pull is a vector sum over three
links whose phasing shifts with the heavier blade. It is still a long way inside the post's 20.1
Nm of bending capacity, at 2.13 Nm.

Run order matters now and it is written at the top of both scripts. `tools/linkage.py --write`
first when the blade section moves, then `tools/structure.py --write`, which reads the pitch
link load back out.

## D49: the structure is signed off at a declared 1.20 overspeed, on combined bending

31 August 2026, week 4.

Centrifugal load goes as the square of rotor speed, so a structure signed off at exactly the
design rpm has no answer for control overshoot. The declared case is 1.20 times design speed,
2885.7 rpm, which makes centrifugal load 44 percent worse instead of 20. It covers ESC control
overshoot and a gust transient on a rotor whose speed loop has no published bandwidth. The
problem statement sets no flight envelope for the module, so this is a declared case and not a
derived one.

`check.py` requires the declared factor to be at least 1.10, because 1.001 satisfies an
inequality and covers nothing.

**The gated blade margin was measuring the wrong load.** `blade_margin` compares the section
against aerodynamic bending alone, and on a cyclorotor that is the smaller of the two spanwise
loads by a factor of 9.2. It reads 28.99 and it always would have. The margins that decide the
blade are the combined ones, 2.83 at the design point and 1.97 at overspeed, and the attachment
margins, 2.44 and 1.69. All four are gated at 1.5 and the two overspeed cases have the least in
hand.

`blade_margin` stays in the schema. Removing it would hide which half of the load the section
carries easily, and the spread between 28.99 and 1.97 is the clearest statement in the document
that this rotor is a centrifugal machine first.

## D50: the 5 percent blade flexibility allowance stays at 5 percent, and now has a calculation under it

31 August 2026, week 4. Answers the closure task week 2 left open. It does not reopen D35 or D36.

Week 2 could only bound the allowance from above. Bending deflection is 0.0936 mm at the peak
blade load and aerodynamic twist is 0.0145 degrees, both negligible against a 40 degree
amplitude, so the document said plainly that the section did not support 5 percent and kept the
number because the section was preliminary.

Week 4 found the term week 2 was missing. The blade is driven in pitch from one end through a
single horn, so the centrifugal pitching moment has to travel through the blade's own torsional
stiffness. 2.2058 Nm over 290.4 mm of span at 7.81 Nm2 winds the far end up by 2.35 degrees and
about 1.6 degrees averaged along the span, which is 4 percent of the pitch amplitude. That is
most of the 5 percent. The rest still covers build tolerance, bond line variation and unsteady
effects a static beam model does not see.

**The number does not move.** D36 says the coefficient reserve is deliberate and stays unspent,
and finding a mechanism that justifies an allowance is not a reason to spend it. What changed is
that the allowance is defensible in a viva now, instead of being a floor with an apology
attached.

Driving the blade from both ends would roughly quarter the wind up. That is a Stage 2 option and
it costs a second horn, a second link and a second offset path per blade, which the mass budget
has no room for.

## D51: four gates and one reader fix went into check.py this week

31 August 2026, week 4. Records a gate change, the way D42 did for week 3. Nothing was loosened.

The week 4 gate was checking that a blade survives aerodynamic bending, which it does by a
factor of 29, and it had nothing to say about the load that actually sizes the blade. Four gates
went in:

- `blade_combined_margin` and `blade_combined_margin_overspeed`, allowable over aerodynamic plus
  centrifugal bending, both floored at 1.5
- `blade_attachment_margin_overspeed`, with the overspeed centrifugal load recomputed from the
  declared factor squared
- `blade_centrifugal_bending_Nm` recomputed from the centrifugal load and the same lever the
  aerodynamic case uses, so it cannot be written down
- the conservative budget held within 25 percent of the week 2 conservative envelope, which is
  the band the nominal columns already carried per component and in total

Plus one reader fix. `dim_of_key` matched a unit only at the very end of a key, so
`thrust_N_conservative` was not a force and `mass_g_conservative` was not a mass, and the
submission's own conservative thrust of 17.10 N could not trace to the number that produced it.
Week 3 found that on the draft and recorded it as a gate defect. Qualifiers are peeled off
before matching now, from a closed list, which is narrower than widening the match: widening it
would let `power_loading_ref_N_per_W` read as two dimensions at once.

Five attack cases went in with them, one per gate plus a coverage probe for the qualifier fix.
Each of the four structural cases stores a self-consistent structure block, so every one of them
would have passed every margin gate that existed before this week. 117 self-tests to 123, and
the closing count is computed now, because the constant it replaced had drifted one behind what
the run actually prints.

## D52: the BOM is priced, and priced is not quoted

31 August 2026, week 4.

Every unit cost in the BOM is an indicative distributor list level price. No supplier was
contacted, no listing was fetched during the week, and the source column names the distributor a
part would be bought from and not one that has quoted for it. The field is `priced_date` in
`numbers.json` for that reason, and `06-materials-and-manufacturing.md` says it in bold above
the table.

The alternative was leaving the BOM out until real quotes exist, and that loses more than it
saves. Cost realism carries 10 percent with manufacturability, and the make against buy split
and the lead times are the parts a reviewer actually uses. Both are sound whether the rupee
figures move 20 percent or not. The critical path is a 4 week foam import with no Indian
stockist, and that finding does not depend on the price at all.

Five lines above 4500 INR carry 52 percent of the 65770 INR total, and those are the ones Stage
2 has to replace with written quotes. Gear cutting is the one most likely to move, because a
quantity of one is priced by setup.
## D53: the week 4 audit corrects the balance figures in D46 and one claim in D51

31 August 2026, week 4, after the audit. Corrects D46 and D51 without reopening either decision.
The log is append only, so the corrections live here.

The audit is in `stage-1/audit/week-4.md`, verbatim, with 13 findings and what was done about
each. Two of them landed on numbers or claims already written into a frozen entry.

**D46's balanced pitch link figures were computed from a stale ratio.** `balance_report` in
`tools/structure.py` priced the balanced link load by multiplying the unbalanced one by 0.655,
which is week 3's balanced over unbalanced ratio, 69.38 over 101.82, taken on the week 2 blade.
It was hardcoded and it survived the blade changing underneath it in the same week. The solver
gives **74.62 N** and a margin of **4.69**, not 69.4 N and 5.04, and the balanced blade pitching
moment is **1.0904 Nm** rather than about 1.06. `--balance` calls `linkage.solve` for that number
now instead of scaling.

The decision stands and it is not close. Balancing still costs 35.47 g, still takes the stacked
conservative case to 2.4061 and still puts it under the hard limit of 2.5. What changed is that
the margin the mass would have bought is 4.69 rather than 5.04, so the trade is 35.47 g to move a
pitch link margin from 3.30 to 4.69. That is a worse trade than D46 described, not a better one.

The wrong pair had reached `03-pitch-and-vectoring.md`, `05-mass-and-tw.md`,
`08-structure-and-loads.md`, the progress file and the journal. All five carry the solver's
figures now.

**D51's "Nothing was loosened" overreaches, and the sentence is withdrawn.** Three of the four
week 4 gates are new checks on things nothing checked before, and the `dim_of_key` fix only ever
widens what can trace. The fourth is different. Week 2 used to test
`results.mass_g_conservative` against the sum of the week 2 conservative envelope lines, exactly.
Since D47 it tests it against the refined budget's own lines instead, and the week 2 envelope is
held only by the new 25 percent band in `check_conservative_budget` and by the 105 percent floor
it always had. An exact sum rule became a band.

That is what D47 argues for and it is deliberate, because binding the refined column to the
estimate it replaces defeats the refinement. Calling it "nothing was loosened" was the error. The
accurate sentence is that one exact rule was replaced by a wider one on purpose, and three new
rules went in beside it.

**And one thing the audit found that no decision had covered.** `tools/structure.py` wrote
`numbers.json` with the platform newline, so it put CRLF back into a file `tools/linkage.py` had
just written as LF, against a repository that declares eol=lf. Git normalises on the way in, so
`git status` stayed clean and the working tree file was 1520 bytes larger than the committed
blob. The claim that the file reproduces byte for byte was true only after git had touched it.
`tools/linkage.py` carries a three line comment about that exact trap, written in week 3, and the
sibling script was written without it. Both scripts now write with `newline="\n"` and the same
`ensure_ascii`, and the file reproduces byte for byte with no normalisation in between.

**What went into the gates as a result.** `structure.shaft_combined_margin` was stated in an
eight row margin table that claimed every row was gated, and `check.py` had nothing to say about
it at all. It is floored at 1.5 now. It is still not recomputed, because it needs shaft section
properties that live in the solver rather than in `numbers.json`, and both the handoff and
`08-structure-and-loads.md` say so instead of claiming otherwise. One attack case went in with
it. The self test total is counted at the point every line is printed now, rather than kept as a
constant beside the loops, which is what D51 claimed and had not actually done. 123 self-tests to
124.

## D54: the coverage gate skips the pandoc front matter

31 August 2026, week 5 preparation. Records a gate change, the way D42 and D51 did for weeks 3
and 4. This one is a defect fix rather than a new check.

`check_numeric_coverage` read every line of the submission, including the YAML header pandoc
uses to set the page margin, the font size and the title. So `geometry: margin=25mm` was
reported as a 25 mm length the design had not justified from `numbers.json`, and it sat in the
gate output as one of two untraced numbers for the whole of week 4.

Front matter is build configuration and not a claim about the rotor, so `front_matter_lines`
finds the block and the coverage loop skips it. Two properties matter more than the fix.

**The skip is positional.** It applies to a delimited block at the top of the file and to
nothing else, so `margin=25mm` written into the body is still a claim and still fails. Fixing
this by exempting the string, or by deleting the margin setting, or by hanging an allow comment
on it would each have solved the symptom and left the gate lying about a different file later.

**An unterminated opening delimiter counts as no front matter.** Otherwise a stray horizontal
rule on line 1 hides an entire document from the audit, which is a worse failure than the one
being fixed.

Four self-tests went in: three coverage probes covering the three cases above, and one whole
week 5 case that puts a real header on the fixture submission. 124 self-tests to 128.

## D55: item 7 is structure plus tagged placeholders, and the tags are P-1 to P-9

31 August 2026, week 5 preparation.

`07-team-and-execution.md` did not exist for three weeks because week H is outstanding and D5
forbids an agent naming a person, an institution, a qualification or a tool licence. Waiting
also meant the one deliverable that needs nothing from `numbers.json` was sitting in the four
day week that carries the deadline, which the plan itself calls the worst place for it.

So the file is written as everything that does not need a human, with nine numbered gaps that
do. The execution plan across all 11 Stage 2 items, the capability gap analysis against the
problem statement's seven preference areas, the Stage 2 gates and the route through the missing
capability are all real content. The roster, the institution, the prior work behind each
preference area, the tool licences, the weekly hours, the sender, the registration reference,
the eligibility check and the facilities are `[P-1]` to `[P-9]`.

The tags are the decision. They appear in the design document, in the submission's identity
table and in the email draft, so one list drives all three and a person filling them in cannot
miss one by reading only the report. Four of the nine are also week H markers and the file says
which.

Claims that are already in the file are claims about the Stage 1 work rather than about people:
what was solved, what was calculated, what somebody else measured and we read. Those need no
human input because the files are the evidence.

## D56: the submission states the 33 budget lines, not group totals

31 August 2026, week 5 preparation. An assembly rule, recorded because it changed what the
submission contains rather than what it claims.

The first rebuild carried the mass budget as 13 group totals, which reads better and cannot be
traced: a group total is a sum computed for `05-mass-and-tw.md` and it exists in no file, so
five of them failed the coverage audit and the rest passed by accidentally landing within 2
percent of an unrelated stored mass. Passing by coincidence is worse than failing. The
submission carries all 33 stored lines instead, each of which is a value in `numbers.json`.

Two numbers came out of the narrative for the same reason. The Grashof sum of 125.4 mm is
arithmetic on two link lengths and is stated as the comparison it actually is, which keeps the
claim and loses the untraceable number. The balanced pitch link load is a solver output under
`--balanced` that is deliberately not stored, so the balance trade is stated by its margins and
its effect on the stacked case instead.

One allow comment is used in the whole document, on the published side force angles from three
studies. That is what the escape exists for, the reason is stated, and it hides 3 of the 4
numbers the ceiling permits.

## D57: the report is 21 pages and the page limit question goes with the submission

31 August 2026, week 5 preparation.

No organiser limit was ever supplied. The question was drafted for early September and never
sent, so the working assumption stands: 15 pages of main body plus cited appendices, which is
what the handoff told week 5 to use.

The built report is 21 pages. One page of title and contents, 15 pages of body through the
sources section, and the rest is appendix A, the examiner questions, and appendix B, the numbers
block. That meets the assumption on the reading that a page target applies to the report body,
and it does not meet it on the reading that it applies to the file.

Nothing was cut to reach a number. Two rounds of trimming took out repetition and loose wording,
and what is left is the seven required items, the criteria map, the claims table and the
provenance section. Cutting further means dropping the mass budget or the claims table, and both
are answering a weighted criterion directly.

The question is asked once, at the end of the staged email, framed so it needs no reply. That is
the last cheap chance to get the format right and it costs nothing if the answer never comes.

## D58: this pass prepares week 5 and does not run it

31 August 2026. Recorded so a later session cannot read five closed gates as a finished week.

Week 5 is hard blocked by week H and all four blocking markers are still pending. That block is
mechanical, it is in the loop config, and D5 puts the same rule under it. So this pass closed
every week 5 gate that does not need a person and stopped at the one that does.

What that means in practice: `python tools/check.py --week 5` fails on the human gate alone.
There is no `stage-1/progress/week-5.md`, nothing carries `STATUS: WEEK-COMPLETE` for week 5,
and `NEXT-WEEK:` in the handoff still reads 5. Week 5 runs when a person has added the markers
and the real team facts, and what is left of it then is short.

The alternative was to leave the submission stale until the markers arrive. That loses the four
days the deadline does not have, and it leaves the one gate defect in `check.py` sitting under
week 5 while it is being run.

## D59: human gate markers are read from the status block, not from the whole file

1 September 2026, found while listing what is left of week 5.

`check_human_gate` tested `marker not in text` across the entire file. The instructions in
`stage-1/human-gate.md` explain how to confirm the last item: replace `TECHNICAL-READ-PENDING`
with `TECHNICAL-READ-COMPLETE` after opening the built PDF and reading it end to end. That
sentence contains the literal marker, so the substring search found it and the gate reported
that marker satisfied.

The one that gates final staging, the human read of the attachment, was passing because the
file explained how to write it later.

The other four survived only by accident of wording. Their prose spells the PENDING form, so
nothing matched. Any edit that mentioned `ROSTER-CONFIRMED` while explaining the process would
have silently confirmed the roster.

**What changes.** The gate splits the file at the `## Status` heading and reads only what
follows, and a marker has to be the whole line after stripping. A file with no status block
fails rather than falling back to the whole text, so the failure mode is a refusal rather than
a pass. Three self-tests: a marker named only in the instructions, a missing status block, and
a marker buried inside a sentence within the block.

Nothing about the project's state changed. Four markers were outstanding before this and five
are outstanding now, which is the honest count and always was.

## D60: the pitch bearing carries an oscillating duty rule, and the ball bearing stays

1 September 2026, after week 4.

Week 4 left an open item saying the pitch bearings swing 80 degrees under a steady 110 N, that
this is a fretting duty, and that a static rating says nothing about it. It was carried as a
Stage 2 problem. It was carried wrongly, because the tightest margin in the whole module,
blade attachment at 1.69 under overspeed, is exactly that static rating. Leaving the duty
unquantified meant the number sizing the module rested on a criterion nobody had checked
applied.

**What the calculation says.** With the outer ring stationary the cage turns at `(1 - d/Dm)/2`
of the inner ring angle. For the 693ZZ that is 7 balls of 1.5875 mm on a 5.5 mm pitch circle,
so 80 degrees of pitch travel moves the ball set 28.45 degrees against a ball spacing of 51.43.
The ratio is 0.5533. Under 1.0 every ball stays inside its own arc for the life of the machine,
which is the false brinelling regime, and full recirculation would need 144.6 degrees of
travel. No cyclorotor pitch schedule asks for that, so the regime cannot be tuned out.

The ball count is the soft input and the conclusion survives it. At 6 balls the ratio is 0.474
and at 8 it is 0.632, both well under 1.0, and a complement large enough to reach 1.0 would need
20.6 mm of ball around a 17.3 mm pitch circle. `check.py` now gates that fit, so the cheap way
to claim recirculation is closed.

**What the rule is.** A bearing that never recirculates carries a static safety factor floor of
2.0 at the OPERATING load, not the declared overspeed. Wear accumulates at the speed the machine
runs at; overspeed is a strength case and it already has its own floor of 1.5. The design sits at
2.44, so it clears. The 2.0 is a declared rule in the same class as `overspeed_factor`, stated
rather than derived, and the gate refuses a floor a later week lowers.

Being honest about which case binds: at the frozen 1.20 overspeed the 1.5 strength floor asks
more of the rating than the 2.0 wear floor does, so today the strength case governs and the wear
floor is not the active constraint. That is not a reason to leave it out. It is the constraint
that catches a future week trading overspeed down and taking the wear case with it, which is
precisely the trade nobody would notice.

**Why the ball bearing stays.** The alternative that is immune to the wear mode is a PTFE fabric
lined plain bearing, which is what an oscillating aerospace joint uses. Six of them cost 8.92 W
of friction against 0.167 W for the ball bearings, better than fifty times, and at 40.08 Hz the
liner is running 167 mm past the shaft every second. The sliding rate is what kills it here, not
the load. So the ball bearing stays, on the 2.44 safety factor plus an anti fretting grease, and
if a Stage 2 bench run frets anyway the fix is a larger bearing before it is a different type.

**What this does not close.** A computed regime is not a tested one. Stage 2 still owes a run to
failure at speed under the real load with the flight grease, and this entry moves the item from
"unquantified" to "quantified and still untested" rather than closing it.

Ten new gates and six new self-tests, 138 to 144. Nothing was loosened.

## D61: the derate keeps its 0.80 and gets a bound on what it costs

1 September 2026, after week 4.

The 0.80 continuous derate has been the weakest number in the drive selection since week 2 and
it was carried as "assumed, no source" in E15. It cannot be given a source from inside the
project. T-Motor publishes a 180 second maximum, the problem statement asks for no endurance,
and there is no duty to size a derate against. So the choice was to keep arguing about it or to
bound the consequence. This entry bounds it.

**The break even.** The design draws 0.7927 of the published 180 second current and 0.704 of the
published 180 second power. Current is tighter, and 0.7927 turns out to be two numbers at once:
it is the fraction drawn and it is the derate at which the MN5006 stops covering the design
point. The declared 0.80 clears it by less than a point.

**Neither exit is open.** Lowering the design point does not work, because the stacked thrust to
weight case needs 17.6768 N and no row of the sensitivity table below 18 N reaches it. The 16 N
row has drive room to spare and still misses on the stacked case. A larger motor does not work
either, because motor mass is a power class item and the conservative column has 12.5 g in hand
against a next size up that costs several times that. Both of those are now gated, so neither can
be taken quietly.

**Why it is still tolerable.** 0.7927 is a fraction of a three minute rating, so any
demonstration inside three minutes runs against the datasheet figure with a fifth of it spare.
The 0.80 continuous rule is a conservatism we imposed for indefinite running that nothing asks
for. It stays, because a module that holds thrust for three minutes is a thin answer to a hover
requirement, but it is not what decides whether the module works. What settles it is a
dynamometer run at the working current, early enough in Stage 2 that a drive change is still
affordable, and that is now the first drive gate in the plan.

**One older rule moved out of prose.** Belt ratios were screened in week 2 on motor speed staying
under 90 percent of what the pack turns the motor at after the resistive drop. That rule is what
emptied the 100 mm radius row and it was enforced nowhere. The pack voltage, the loaded voltage,
the ceiling, the rule and the fraction are stored and recomputed now, and the gate refuses both a
rule looser than 0.9 and a ceiling KV and the pack do not give.

**One date corrected.** E12 and E13 dated a datasheet read to 2 September 2026, which had not
happened yet. That is week 2's systematic two day drift, recorded as debt 14 and deliberately
left across a dozen files. These two cells are the exception because they date a source read
rather than a piece of writing, and they now say what the commits say.

Thirteen new gates and five new self-tests, 144 to 149. The submission and its PDF are rebuilt,
still 21 pages, and the xelatex log has no overfull lines.
