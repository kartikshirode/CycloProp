# Week 2: configuration, sizing, thrust, power, feasibility

**STATUS: WEEK-COMPLETE.** Geometry is frozen at 18 N of design thrust and a 110 mm radius,
with 120 mm carried as insurance. All three gate commands exit 0.

Week 2 ran twice. The first run, 2 September 2026, produced everything the plan asked for and
then reported BLOCKED, because the stacked conservative case came in at a thrust to weight of
2.252 against a hard limit of 2.5. A person made the call and recorded it as D30. The second
run, 31 August 2026, froze the geometry, wrote the mass target that D30 asked for, and closed
the week. Both runs used the config at `.claude/weekly-loop.md`, which D28 settled as the only
execution contract.

## What the week was meant to produce

Required Stage 1 items 1, 2 and 4, plus the feasibility envelope that decides whether the
design closes at all. Seven work packages: evidence ledger and selection rules, common
candidates, the thrust and power model with coefficient scenarios, the drive and blade section,
the coupled comparison, a frozen design point, and the audit.

## What it produced

- `stage-1/design/evidence-ledger.md`, 16 numbered evidence rows with class, source, exact
  basis, area convention, source geometry, source Reynolds number and use, plus the selection
  rules written before any candidate was scored
- `stage-1/design/01-configuration.md`, the single rotor against redesigned 2 and 3 rotor
  clusters on one common model, with the packaging rule stated and the cluster mass build-up
  written out
- `stage-1/design/02-rotor-sizing.md`, shape family, coefficient recompute, blade section and
  stiffness closure, the radius sweep, the mass envelope and the four case verdict
- `stage-1/design/04-thrust-and-power.md`, thrust, the 36 point azimuthal load distribution,
  power closed three ways, the named drive on a derated continuous rating, and the sensitivity
  table
- `stage-1/design/numbers.json`, the full week 2 block: 24 performance scalars, 7 geometry, 3
  operating, 3 efficiency, plus `power_by_radius` at 5 radii, 3 configuration candidates, 4
  coefficient scenarios, 36 azimuthal load rows, 5 drive candidates, 13 mass envelope lines, 4
  sensitivity rows and the week 4 mass target
- Four new gates in `tools/check.py` from the audit, the one stacked thrust to weight gate
  replaced by six, and three document gates for D32, with 22 self-tests behind them
- D18 to D27 in `stage-1/decisions.md` from the first run, D31 and D32 from the second
- `stage-1/audit/week-2.md`, two independent passes, the first 18 findings and the second on
  the freeze

## The result

Four thrust to weight cases, which is the thing the first run got wrong by reporting one.

| Case | Thrust | Mass | T/W | Verdict |
| --- | --- | --- | --- | --- |
| design point | 18.00 N | 580.1 g | 3.163 | clears 2.5 by 27 percent |
| mass downside alone | 18.00 N | 692.4 g | 2.650 | clears by 6 percent |
| coefficient downside alone | 15.30 N | 580.1 g | 2.689 | clears by 8 percent |
| both stacked | 15.30 N | 692.4 g | 2.252 | misses by 68.5 g, goes to week 4 |

The other headline numbers, none of which moved this run:

| | Value | Target | Verdict |
| --- | --- | --- | --- |
| nominal thrust | 18.0 N | at or above 10 N | clears |
| conservative thrust | 15.30 N | at or above 10 N | clears |
| figure of merit | 0.60 | 0.20 to 0.75 | clears, and matches what Kellen reports |
| two power routes | 9.8 percent apart | within 35 percent | clears |
| solidity | 0.3151 | 0.30 to 0.40 | clears |
| chord Reynolds | 134,000 | inside 10,000 to 100,000 for the transfer | **fails, and cannot pass. See D25** |

Frozen geometry: 110 mm radius, 72.6 mm chord, 290.4 mm span, 3 blades, NACA 0020, plus or
minus 40 degrees, 2405 rpm, one MN5006 KV450 on a 3.5 to 1 belt. The insurance radius is 120
mm, which costs 0.12 of stacked conservative thrust to weight and buys 38 W and 384 rpm.

## Why the stacked case does not close, in one paragraph

It multiplies two independent penalties. Thrust drops to 85 percent because the coefficient is
transferred across a change of blade count, airfoil and chord ratio at once, and now across a
Reynolds extrapolation as well. Mass rises to 119 percent because the structural lines come
from assumed sections rather than weighed parts. 0.85 over 1.19 is 0.71, so a nominal thrust to
weight of 3.51 is needed to put the stacked case on 2.5 and 3.86 to put it on 2.75. The best
published module on the same boundary is Runco at 2.13. This design reaches 3.163 nominal,
already 49 percent above the record.

What the second run changed is not that number. It is what the number is allowed to decide.
Nine of the thirteen envelope lines say assumed in their basis and carry a blanket 20 or 25
percent growth rate, so the stacked figure tests those rates about as hard as it tests the
rotor. Week 4 replaces them with real sections and catalogue parts and gets tested against the
same limit. Full reasoning in D30, target in D31.

## The fallbacks, worked in the plan's order

**1. Higher precomputed thrust row.** Swept 13 to 24 N. Stacked conservative thrust to weight
rises with thrust because the geometry-scaled mass lines do not move, then turns over when the
drive runs out.

| Design thrust | Best radius | Stacked T/W |
| --- | --- | --- |
| 13 N | 80 mm | 1.949 |
| 14 N | 80 mm | 2.088 |
| 16 N | 100 mm | 2.134 |
| 18 N | 110 mm | **2.252** |
| 20 N | 135 mm | 2.157 |
| 22 N | 155 mm | 2.094 |
| 24 N | 175 mm | 2.012 |

**2. Along the coupled radius table.** Swept 75 to 200 mm at each thrust. At 18 N:

| Radius | Motor input | Drive fits | Stacked T/W |
| --- | --- | --- | --- |
| 100 mm | 503 W | no | 2.376 |
| 110 mm | 458 W | yes, 3.5 to 1 | **2.252** |
| 120 mm | 419 W | yes, 4.0 to 1 | 2.134 |
| 130 mm | 387 W | yes, 4.5 to 1 | 2.019 |
| 140 mm | 360 W | yes, 4.5 to 1 | 1.909 |

**3. Reject duplicated hardware, return to the single rotor branch.** Already there. The cluster
comparison went the other way: 1.659 for two rotors and 1.323 for three, on assumptions set in
the cluster's favour throughout. Nothing to recover.

**4. Revisit the shape family.** Swept chord ratio 0.63 to 0.836 and blade aspect ratio 3 to 6,
holding solidity inside the reported band. The best was about 4 percent better than the
baseline family, at a blade aspect ratio of 6, and it is not bankable because it leaves the
family the coefficient was measured in. Buying a number by weakening the evidence behind it is
not a fallback.

D30 rechecked all four by hand before deciding, and added the two the first run had not priced
properly: 20 N fails on power at 110 mm and on an empty belt window at 120 mm, and the 100 mm
row's belt window is empty for any pulley pair rather than only the half integer ones week 2
tried. None closed the stacked case.

## How the stacked shortfall retires

Ranked by leverage. The full argument is D31; this is the short form.

**1. Kellen's measured thrust coefficient, and it retires the target completely.** If it lands
at or above 0.6055 for this shape family, the 10 point configuration-transfer allowance goes,
the haircut drops from 15 percent to 5, conservative thrust becomes 17.1 N and the mass that
clears 2.5 becomes 697.2 g. The module already weighs 692.4 g in the conservative column, so
there would be no shortfall left for week 4 to find. It also settles D25, because Kellen
measured across 100,000 to 300,000 and this design sits at 134,074, inside that band. Two
minutes in a browser.

**2. Real sections in the week 4 budget.** The eight assumed lines carry 86.4 g of the 112.4 g
total growth allowance. Retiring them to a uniform 10 percent gives back 45.7 g of the 68.5 g
needed, so most of the gap sits there. The rest has to come from the nominal lines.

**3. A lighter drive.** The design is **drive limited**, not aerodynamics limited and not
structure limited. Stacked conservative thrust to weight keeps rising as the radius falls and
the 100 mm row gives 2.376, but no shortlist motor holds it: rotor torque wants a belt ratio
the KV450 cannot spin to on a 6S pack. Working backwards, the drive would have to deliver 503 W
continuously at 78 g or less, which is 6.5 W per gram. The best part in the shortlist is the
MN4006 at 6.7 W per gram of rated power but only 5.3 continuous, and the selected MN5006 is at
4.9. D30 also points out that pack voltage sits outside the module boundary, so a lower KV part
on more cells reopens the 100 mm row without costing module mass. That needs a datasheet.

**4. Weighed hardware on the softest lines.** The rotor shaft's torque allowance at 18 g per Nm,
the fastener and bonded joint line at 22 g, and the wiring harness at 16 g. Together about 98 g
of the 692 g conservative total.

**5. Ramsey 2022.** A 25 kg subsystem mass table would give a second real anchor for the
structural lines. There is currently one, Runco, four orders of magnitude smaller.

## What changed

- **Geometry is frozen**, on the design case and the two single downsides, per D30. Week 3 has
  a real operating point to solve the linkage against
- **D2 is no longer provisional.** The cluster comparison it asked for has been run on a common
  boundary and the single rotor wins by 36 percent on stacked conservative thrust to weight
- **The 0.607 coefficient is now 0.6055 and recomputed rather than quoted.** Same number to a
  quarter of a percent, now reproducible from Benedict's published figures in one line
- **The two open allocations are closed.** ESCs are module hardware and mounting counts in full,
  both settled against us and both settled before scoring
- **The design is drive limited.** Radius is set by the smallest rotor a named motor can hold
  continuously, not by where the aerodynamics or the structure want to be
- **Almost nothing in this module is fixed mass.** Sorted honestly, one 8 g controller board.
  D11 and D13 rest the feasibility case on fixed hardware amortising over more thrust, and
  there is very little of it to amortise
- **The Reynolds transfer is an extrapolation and cannot be made otherwise** inside this shape
  family, because the conservative thrust gate forces design thrust above 11.76 N. See D25
- **Kellen went from supporting evidence to hard dependency and back.** D23 made it load
  bearing when the freeze depended on it. D30 put it back, because the freeze no longer does.
  It is still the cheapest item on the list

## Debts carried forward

| # | Debt | Owner |
| --- | --- | --- |
| 1 | The stacked conservative case is 68.5 g short of T/W 2.5, carried as `results.mass_target_week4_g` = 623.9 g. Week 4 closes it against a refined budget or reports BLOCKED. See D30 and D31 | week 4 |
| 2 | Four of the five motor rows and the ESC came from supplier listings rather than datasheet PDFs. Only the MN5006 was read off the manufacturer's sheet. Week 4 confirms the rest, and prices the lower KV on more cells idea D30 raised | week 4 |
| 3 | The 0.80 continuous derate on a 180 s rating has no source, because the problem statement states no endurance requirement to size it against. A stated hover duration would turn a judgement into a calculation | human |
| 4 | The three efficiencies, 0.93 belt, 0.84 motor, 0.95 ESC, are assumed. The motor figure is the sensitive one: at 0.78 the motor input rises to 493 W and eats most of the drive margin | week 4 |
| 5 | The cluster mass build-up is written out in prose in `01-configuration.md` but only its totals are in `numbers.json`, so a reader can follow it and a gate cannot check it | week 4 |
| 6 | The azimuthal model gives a peak to mean blade load of 2.37 against a published 3 to 4. The model has no wake return, no shed vorticity and no dynamic stall overshoot, so it under-predicts the peak. Week 4 uses 4.0 regardless, per D16 | week 3 and 4 |
| 7 | The 28 degree stall cap in the azimuthal model is stated, not measured. Heimerl would replace it | blocked on a paper |
| 8 | Side force is zero in the azimuthal model by construction, because the prescribed schedule has no phase offset. Week 3 reruns it against the solved linkage | week 3 |
| 9 | The blade spar is sized geometrically at 0.12 chord diameter with a 0.5 mm wall. Week 4 sizes it against centrifugal load, which at 2405 rpm is the load that governs | week 4 |
| 10 | The 2.75 internal margin target from D17 is not met on the stacked case and the freeze went ahead anyway. That is a deliberate call, not an oversight, and D30 carries the reasoning | closed by D30 |
| 11 | `stage-1/organiser-email.md` is still mostly answered by the problem statement and should be cut down or dropped | human |

Debt 1 from the first run, two files claiming to be the execution contract, was closed by D28.

## Week H gap

All five markers in `stage-1/human-gate.md` are still pending: `REGISTRATION-PENDING`,
`ELIGIBILITY-PENDING`, `ROSTER-PENDING`, `SENDER-PENDING`, `TECHNICAL-READ-PENDING`. Week H is
advisory before week 2 and the engineering genuinely did not depend on the roster, so week 2
ran and this records the gap. It becomes a hard block on week 5. The eligibility check is still
the one worth doing first, because the clause disqualifies a whole team at any stage including
after results.

## Evidence gap: three unread papers

All three sit behind the same Cloudflare JavaScript challenge on the Texas A&M repository. A
user agent string does not pass it; a real browser passes it in about two seconds. Rechecked on
31 August against the item page, the bitstream and the handle URL, and core.ac.uk and oatd.org
as well. All 403.

- **Kellen 2019**, handle 1969.1/184958, item `a4c62d38-3778-44f4-b398-cdcba283fa06`. Wanted:
  the measured blade-area thrust coefficient, power loading in N/W, per-rotor thrust and rpm at
  the optimum. Highest leverage item on the list. See D23, D25 and D30
- **Heimerl, Halder, Benedict et al.**, VFS 77th Forum, cyclorotor in forward flight. Wanted:
  the measured blade peak to mean load factor and the side force angle against pitch offset.
  Answers debts 6 and 7 and feeds week 3's vectoring section
- **Ramsey 2022**, handle 1969.1/198531, item `692efcdd-c56a-4c7a-b507-f3e673986b51`. Wanted:
  the 25 kg subsystem mass table and any blade mass or deflection figures

Week 2 ran without all three and disclosed it, which is what the config asks for supporting
evidence.

## Gate state at the end of the week

```
python tools/check.py --week 2   pass
python tools/check.py --global   pass
python tools/test_gates.py       98 of 98 self-tests behaved as expected
```

**`tools/check.py` was changed twice and never loosened.** The first run added four gates after
the audit found that three of the lists week 2 fills carried numbers nothing read: a 36 row
table of arbitrary positive values satisfied the azimuthal check identically to a calibrated
one, and nothing asked whether the named drive could hold the design point. The D30 restructure
then took the one stacked T/W gate out and put six in: three cases each hard against 2.5, one
requiring the stacked figure to be stated and reproduce, one recomputing the week 4 mass target
and one on how it retires. The second run added three more, one per week 2 document, which are
D32 made mechanical. Twenty two self-tests came with the three rounds, roughly one per attack,
and the suite went from 77 to 98. No tolerance, bound or
limit moved in either direction.

The mass target gate is the one worth describing, because it is the only gate in the file whose
requirement depends on a result. When the stacked case clears 2.5 it reports and asks for
nothing. When it misses, `results.mass_target_week4_g` has to be present and reproduce from the
conservative thrust to half a percent, and `sources.results.mass_target_week4_g` has to say in
at least 40 characters how the shortfall retires. A stated target 15 percent above the computed one
fails, so does one 15 percent below it, and so does a target with the word "week 4" as its
whole explanation. Five self-tests cover those cases.

The three document gates are simpler. Each of the week 2 design documents has to quote a number
within half a percent of the recomputed stacked figure somewhere in its text, at any rounding,
so 2.25 and 2.2525 both count. Stripping the number out of one document while leaving every
stored value untouched is a self-test of its own, because nothing else in the file would notice.

## What week 3 needs to know

Geometry is frozen, so week 3 starts on a real operating point: 110 mm radius, 72.6 mm chord,
290.4 mm span, 3 blades, NACA 0020, plus or minus 40 degrees, 2405 rpm.

Two things it inherits, and both are real work rather than notes:

1. **The azimuthal load model has zero side force by construction.** The prescribed sinusoid
   carries no phase offset, so the lateral components cancel exactly over the cycle. That is an
   artifact of the input, not a result. Week 3 reruns the model against the schedule the solved
   linkage actually produces, and side force is where the real risk sits. Benedict measured a
   resultant 30 degrees off vertical and Adams 15 to 35 degrees depending on amplitude and rpm
2. **The radius is 110 mm and it is frozen.** 120 mm is carried as insurance against a week 2
   mistake, not as a free option. Switching after week 3 costs a week 3 rerun, because link
   lengths, offset geometry, the pitch schedule and gearing all move with radius

Week 3's own scope is unchanged: linkage topology and loop closure, the solved pitch schedule,
the vectoring actuator and the force-vector map, packaging, and the item 7 structure.
