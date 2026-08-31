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
