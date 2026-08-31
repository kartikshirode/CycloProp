# Week 4: structure, mass, thrust to weight, materials, manufacturing

31 August 2026. Covers required items 5 and 6 and the 15 percent structural criterion, which had
no section in the repository before this week.

STATUS: WEEK-COMPLETE

**This week was interrupted by an API failure and recovered.** The session running it stopped
partway through on a network error, having written `tools/structure.py`, the refined
`numbers.json`, `05-mass-and-tw.md`, `08-structure-and-loads.md` and the week 4 gate changes,
and having committed none of it. A second session read all 786 lines of that uncommitted work,
verified every number reproduced from the scripts, corrected four things in it, finished the
week and committed it. The week was not restarted and nothing already correct was rewritten.
What the recovery changed is listed under "What the recovery corrected" below.

## What the week was meant to produce

The plan lists 7 tasks. All 7 ran.

1. Close the blade stiffness assumption against final material allowables, and check that the
   result supports the blade flexibility loss the low thrust coefficient carries
2. Load cases and strength at an operating and a declared overspeed condition, closed form, with
   assumptions shown
3. Margins against the right allowables, and an honest list of the analyses not done
4. Refine the component mass budget line by line, each line pointing at the week 2 envelope line
   it refines, with a visible reserve
5. Compute nominal and conservative thrust to weight and reconcile every line that moved more
   than 25 percent
6. Tie material and process to the load, with an assembly order and the measurements that decide
   whether a built rotor is safe to spin
7. A costed BOM with quantity, source, price date, unit cost, lead time and Indian sourcing

## What it produced

**A structural calculation that reruns.** `tools/structure.py` integrates the NACA 0020 section
numerically, builds the blade from its materials, sizes the shaft, the pitch load path and the
attachment, computes all 8 margins and writes the mass budget, the BOM and the results block
into `numbers.json`. It reads geometry, speed and thrust back out of `numbers.json`, so it
cannot drift away from the frozen design, and it never reads its own output back in. Running
`tools/linkage.py --write` then `tools/structure.py --write` on a clean copy reproduces the
committed `numbers.json` byte for byte.

**The blade is a centrifugal part, and the gate could not see that until this week.** Each blade
pulls 221.464 N radially against a peak aerodynamic 24.00 N, a ratio of 9.2 where Runco measured
4.4 on a much smaller rotor. The gated `blade_margin` compares the section against aerodynamic
bending alone and reads 28.99. Combined with centrifugal bending it is 2.8341, and at the
declared 1.20 overspeed it is 1.9681. The attachment is 2.4383 and 1.6933. All four are gated at
1.5 now and the two overspeed cases are the tightest numbers in the design. See D49.

**The mass budget closed on the first pass, with no fallback used.** 33 lines, 607.97 g nominal
and 684.70 g conservative. The growth rate is a property of the line and not of the module:
catalogue 8 percent, machined 12, calculated 15, allowance 25, classified before the total was
looked at, which is what D33 requires. Weighted that is 12.6 percent against the 19.4 week 2
carried. There is a visible 15.00 g reserve on the frame and mounting group.

**All four thrust to weight cases clear 2.5.**

| Case | Thrust | Mass | T/W |
| --- | --- | --- | --- |
| design point | 18.00 N | 607.97 g | 3.018 |
| mass downside alone | 18.00 N | 684.70 g | 2.680 |
| coefficient downside alone | 17.10 N | 607.97 g | 2.867 |
| both stacked | 17.10 N | 684.70 g | 2.5457 |

The stacked case is the hard gate D30 moved into week 4 and it is applied to this budget rather
than to the week 2 estimate. It clears by 12.5 g where week 2 cleared by 4.8. The decision gate's
three fallbacks, another sensitivity row, a trimmed line, a reopened radius, were all available
and none was used. The radius fallback had a day 2 deadline and it passed unused.

**The blade flexibility allowance has a calculation under it now.** Week 2 could bound it from
above and no more: 0.0936 mm of tip deflection and 0.0145 degrees of aerodynamic twist are
nothing against a 40 degree amplitude. The term week 2 was missing is blade torsional wind up
under the centrifugal pitching moment, since the blade is driven in pitch from one end. 2.2058
Nm over the span at 7.81 Nm2 gives 2.35 degrees at the far end and about 1.6 on span average,
which is 4 percent of the amplitude. The 5 percent does not move, per D36 and D50.

**The balance trade closed against the blade.** 35.47 g of nose ballast takes the stacked case
to 2.406, under the limit, and buys a pitch link margin of 4.69 in place of 3.30. Declined. See
D46 and D53.

**Materials, processes and a costed BOM.** `06-materials-and-manufacturing.md` ties each of the
6 load carrying materials to the margin it decides, gives every part its stock form, process,
key tolerance and joining method, sets the assembly order and lists the 6 measurements that
decide whether the rotor is safe to spin. The BOM is 20 bought lines and 5 made ones, 36970 INR
of parts and material, 28800 of tooling and job work, 65770 total, longest lead 4 weeks on a
foam import with no Indian stockist. Prices are indicative and not quotations, which is D52 and
the first debt below.

## What changed outside week 4's own files

- `stage-1/design/02-rotor-sizing.md`: the blade section and stiffness section rebuilt against
  the drawn blade, the mass envelope marked as the week 2 estimate the budget replaced, the four
  case table's conservative column moved to the refined budget, and the D17 gap restated at 50.9
  g. The week 2 blade build-up paragraph keeps its own figures and now says what week 4 made of
  them
- `stage-1/design/01-configuration.md` and `04-thrust-and-power.md`: the stacked conservative
  figure moved from 2.517 to 2.5457, which is week 2 debt 12 discharged. 04 also explains why the
  radius sweep column still reads 2.517, because that sweep is built on the week 2 envelope
- `stage-1/design/03-pitch-and-vectoring.md`: the mechanism loads moved about 1 percent when the
  blade stopped being an estimate. Carrier torque 0.1371 to 0.1389 Nm, servo margin 2.363 to
  2.332, link force 101.82 to 105.93 N, offset post pull 47.48 to 53.22 N. Three of its open
  items are now answered rather than handed forward. See D48
- `tools/linkage.py`: `BLADE_PARTS_G` deleted. The blade build-up is imported from
  `tools/structure.py`, which retires week 3 debt 11. This creates a run order, linkage first,
  then structure, and it is documented at the top of both files
- `tools/check.py`: 4 new gates, 6 new required structural fields, the conservative mass source
  switched from the envelope to the budget when a budget exists, and the `dim_of_key` qualifier
  fix. Nothing was loosened. See D51
- `tools/test_gates.py`: the fixture's structure block carries the 6 new fields, `_rescale_mass`
  moves the budget's conservative column with the envelope's, and 6 attack cases went in. 117
  self-tests to 124

## Gate state at the end of the week

| Command | Result |
| --- | --- |
| `python tools/check.py --week 4` | exit 0, cumulative over weeks 1 to 4 |
| `python tools/check.py --global` | exit 0 |
| `python tools/test_gates.py` | exit 0, 124 self-tests |

## What the recovery corrected

Four things in the inherited work, none of them a rewrite.

1. **Three test fixtures were stale against a gate the same session added.** `honest_numbers()`
   had no `structure` overspeed or combined margin fields, so `blade centrifugal bending follows
   from the centrifugal load and the same lever` reported "computed 8.421, stated None" and 4
   cases broke. Fixed by teaching the fixture what a week 4 structure block contains, with the
   allowable derived from the combined overspeed case, not by deleting the gate. A fourth case
   broke because `_rescale_mass` moved the envelope and left the refined budget behind, which
   under D47 is not a heavier design but two mass lists disagreeing
2. **`02-rotor-sizing.md` still said 29.4 g per blade** three paragraphs above a section
   explaining that week 4 had rebuilt the blade to 31.75 g. Both figures are stated now, with
   which is which
3. **`03-pitch-and-vectoring.md` declared the old servo torque**, 0.0457 Nm against a stored
   0.0463. That is 1.3 percent, inside the gate's 2 percent display tolerance, so no gate would
   ever have caught it
4. **The BOM's date field was called `quote_date`.** Nothing was quoted. Renamed to
   `priced_date`, and the document says so above the table. D52

The self-test count also had a hand kept constant that had drifted one behind what the run
actually prints. It is counted at the point every line is printed now, which took two goes;
the audit caught the first attempt renaming the constant rather than removing it.

## The audit

One fresh-context read-only pass, run after the eleven week 4 commits landed. 13 findings,
reproduced verbatim in `stage-1/audit/week-4.md` with what was done about each. Twelve were
fixed and one is a declared deviation.

The two worth naming here. The balance trade was priced by multiplying the pitch link load by
0.655, which is week 3's balanced over unbalanced ratio taken on the week 2 blade, hardcoded,
and it survived the blade changing underneath it in the same week. The solver gives 74.62 N and
a margin of 4.69, not 69.4 N and 5.04, and the wrong pair had reached five documents including
D46. The decision does not move: 2.4061 is under 2.5 either way, and the trade is worse than D46
described rather than better. And `tools/structure.py` wrote `numbers.json` with the platform
newline, putting CRLF back into a file `tools/linkage.py` had just written as LF, which git
normalises on the way in, so the working tree file was 1520 bytes larger than the blob and
nothing showed in `git status`. `tools/linkage.py` carries a three line comment about that exact
trap, written in week 3.

The rest: two claims that overreached, one margin in an eight row table that no gate was
reading, an arithmetic slip in the mass decomposition that did not sum to its own stated net, a
week 4 figure sitting in a week 2 comparison row, a superseded 47.48 N hardcoded into a shipped
basis string, a material row crediting the adhesive with a margin nothing computes, and a
self-test count that was renamed rather than computed. The gate gained a floor on
`shaft_combined_margin` and one attack case, 123 self-tests to 124. D53 carries the corrections
that land inside frozen entries.

## Debts carried forward

1. **The BOM is priced and not quoted.** No supplier was contacted and no listing was fetched.
   The 5 lines above 4500 INR are 52 percent of the total and they are what Stage 2 has to
   replace with written quotes. Gear cutting is the one most likely to move. See D52
2. **Material allowables are published typical values for the material class**, not certificates
   for a batch, and no coupon has been tested. For the two aluminium alloys that is a small risk.
   For the foam, the cured laminate and the paste adhesive it is real, because a 15 percent
   shortfall on skin modulus moves the blade allowable by about as much
3. **The blade attachment at overspeed is 1.6933 and it is the lowest margin in the module.**
   Worse than the number is the duty: the pitch bearings swing 80 degrees under a steady 110 N
   each, which is fretting, and a static rating describes none of it. It needs a supplier
   oscillating derate or a bench test
4. **Ramsey 2022 and Heimerl are still unpulled.** Ramsey would give a second structural mass
   anchor and there is still only one, Runco, four orders of magnitude smaller than this rotor.
   Heimerl would replace the peak to mean load estimate and the side force angle with
   measurements. Both are supporting evidence and neither blocked the week, but the structural
   mass case rests on one analogue
5. **The two scripts have a hand resolved run order.** `tools/linkage.py` imports the blade from
   `tools/structure.py` and `tools/structure.py` reads the pitch link load back out of
   `numbers.json`. That is a cycle broken by running them in order, and no gate enforces the
   order. It is still better than the hand copied constant it replaced
6. **A balance tolerance is not set.** The jig is in the BOM and blades get matched inside 0.5 g,
   which is about 3.5 N of once per revolution bearing force at 110 mm. The residual unbalance
   limit that ought to back that up is a Stage 2 calculation
7. **The 2.75 internal target from D17 is unmet, by 50.9 g.** Refinement paid back 7.7 g of the
   58.6 g week 2 left, because the growth allowance fell 35.65 g and real parts added 27.92
   back. No
   further pass over the budget closes it: every remaining line is a drawn section or a catalogue
   part. The two routes that would are a lower KV motor on more cells, reopening the 100 mm row
   at 2.655, and a measured blade area coefficient. Both are outside week 4
8. **The submission draft is stale against `numbers.json`.** It declares
   `results.mass_g_conservative = 692.43` and `results.thrust_to_weight_conservative = 2.5173`,
   and its four case table and item 5 narrative carry the week 2 figures. Week 5 owns the
   submission and rewrites items 5 and 6 anyway, so this was left rather than half updated with
   no PDF rebuild behind it. The exact stale lines are 51, 53, 55, 110, 115, 126, 189, 194 and
   195
9. **Four of the five week 2 motor rows and the servo are still supplier listings.** Week 4 did
   not open a manufacturer sheet for any of them. It did grow the controller line to the 8.5 g
   board rather than looking for a lighter one, which retires week 3 debt 10
10. **The 0.80 continuous derate still has no source**, unchanged from week 2. A stated hover
    duration would turn it into a calculation

Unchanged from week 3 and not touched this week: the transmission angle at 143.23 degrees, the
side force under-prediction, `largest_dimension_mm` at 290 mm against a 364.4 mm module, and
`check.py` demanding the current week's audit while `.claude/weekly-loop.md` says the current
week is exempt.

## Week 3 debts this week retired

- **Debt 1, the blade balance decision.** Closed against balancing. D46
- **Debt 2, the carrier ripple.** Bounded by gear backlash rather than by the servo loop, at
  0.1432 degrees of carrier on 0.05 mm of backlash across the 40 mm gear, which is inside the 25
  degrees of authority the side force uncertainty already reserves
- **Debt 3, the offset strut.** Sized. 53.22 N of radial pull as a 2.13 Nm cantilever moment
  against 20.1 Nm of capacity in an 8 mm 7075-T6 post
- **Debt 4, the gear pair missing from the pitch mechanism basis.** The line grew to hold them.
  12.40 g between the sector gear and the carrier ring, which is most of the group's 17.0 percent
  drift
- **Debt 10, the controller 0.5 g over its line.** The line grew to 8.5 g
- **Debt 11, `BLADE_PARTS_G` duplicating the blade build-up.** Deleted. D48
- **Week 2 debt 12, the three design documents restating the stacked figure.** Done, at 2.5457

## Week H gap

All 5 markers in `stage-1/human-gate.md` are still pending, so `07-team-and-execution.md` was not
drafted for the second week running. No real names, institutions or capabilities were written
anywhere. This now hard blocks week 5 and it is the item with the longest lead time in the
project.

## What week 5 needs to know

- Items 5 and 6 are done and the numbers for them are frozen in `numbers.json`. The submission
  draft's item 5 and item 6 sections are the week 2 figures and have to be rewritten from
  `05-mass-and-tw.md`, `06-materials-and-manufacturing.md` and `08-structure-and-loads.md`
- The numeric coverage gate on the submission draft now reports 2 untraced numbers:
  `margin=25mm` in the pandoc front matter, which is the gate reading YAML as narrative, and
  125.4 mm at line 66. The week 3 gate on the week 3 numbers reported 7, and week 3's own debt
  of 10 was a manual tally counting exempt-region numbers the gate does not. The `dim_of_key`
  qualifier fix accounts for 3 of the 5 that went and the week 4 budget for the other 2
- The PDF has to be rebuilt after any submission edit. The committed one is the week 3 draft
- Nothing in week 5 should need to run either script. If it does, the order is
  `tools/linkage.py --write` then `tools/structure.py --write`
- Week H blocks the week. Report BLOCKED if the markers are still missing
