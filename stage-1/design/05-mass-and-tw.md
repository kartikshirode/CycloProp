# Mass and thrust to weight

Required Stage 1 item 5. This is the refined component mass budget and the thrust to weight it
gives, replacing the coarse envelope week 2 used to decide whether the design closed at all.

Short version. The module weighs 677.91 g nominal and 763.24 g in the conservative column. At
17.0 N that is a thrust to weight of 2.5563, which clears the 2.5 requirement. Stacking the low
thrust coefficient on the conservative mass gives 2.1569, which does not, and closing that
would take 104.76 g out of the conservative column. The internal 2.75 target from D17 is not
met either and its gap is 164.6 g. D67 is where the design point and six envelope lines moved;
this document is the budget after that.

## Mass budget

33 lines, every one of them a drawn section, a catalogue part or a stated allowance, and every
one pointing at the week 2 envelope line it refines. `tools/structure.py` builds it and writes
it, so the arithmetic is rerunnable rather than typed.

| Line | Nominal | Conservative | Class | Refines |
| --- | --- | --- | --- | --- |
| blade foam cores, 3 off | 28.79 g | 33.11 g | calculated | blades |
| blade skins, 3 off | 29.08 g | 33.44 g | calculated | blades |
| blade spar tubes, 3 off | 17.42 g | 20.03 g | calculated | blades |
| blade root close-outs, 3 blades | 19.95 g | 22.35 g | machined | blades |
| rotor spider arms, 6 off | 21.48 g | 24.71 g | calculated | rotor frame and hubs |
| rotor hub bosses, 2 off | 23.97 g | 26.85 g | machined | rotor frame and hubs |
| root attachment brackets, 6 off | 17.20 g | 19.26 g | machined | rotor frame and hubs |
| pitch bearings, 12 off | 15.60 g | 16.85 g | catalogue | pitch mechanism |
| pitch links with rod ends, 3 off | 12.36 g | 13.35 g | catalogue | pitch mechanism |
| pitch horns, 3 off | 4.86 g | 5.44 g | machined | pitch mechanism |
| offset pivot post and pin | 6.50 g | 7.28 g | machined | pitch mechanism |
| phasing carrier ring, 40 mm gear | 7.90 g | 8.85 g | machined | pitch mechanism |
| servo sector gear, 60 mm | 4.50 g | 5.04 g | machined | pitch mechanism |
| carrier support bearings, 2 off | 4.40 g | 4.75 g | catalogue | pitch mechanism |
| rotor shaft tube | 36.01 g | 41.41 g | calculated | rotor shaft |
| shaft end plugs, 2 off | 23.20 g | 25.98 g | machined | rotor shaft |
| main bearings, 2 off | 16.00 g | 17.28 g | catalogue | main bearings |
| bearing blocks, 2 off | 25.27 g | 28.30 g | machined | frame and mounting hardware |
| frame tubes, 4 off | 46.36 g | 53.31 g | calculated | frame and mounting hardware |
| motor mount plate | 13.95 g | 15.62 g | machined | frame and mounting hardware |
| airframe mount lugs, 4 off | 7.20 g | 8.06 g | machined | frame and mounting hardware |
| frame and mount design reserve | 15.00 g | 18.75 g | allowance | frame and mounting hardware |
| motor, MN5006 KV450 | 106.00 g | 114.48 g | catalogue | motor |
| rotor belt pulley, 68 tooth | 34.84 g | 39.02 g | machined | transmission |
| motor belt pulley, 16 tooth | 6.62 g | 7.41 g | machined | transmission |
| drive belt | 12.75 g | 13.77 g | catalogue | transmission |
| belt tensioner and bracket | 6.00 g | 6.72 g | machined | transmission |
| esc, 40 A 8S class | 19.50 g | 21.06 g | catalogue | esc |
| vectoring actuator servos, 2 off | 40.00 g | 43.20 g | catalogue | vectoring actuator |
| pitch offset controller | 8.50 g | 9.18 g | catalogue | pitch offset controller |
| module wiring harness | 25.20 g | 31.50 g | allowance | module wiring harness |
| fasteners and threaded inserts | 14.00 g | 17.50 g | allowance | fasteners and bonded joints |
| structural adhesive at module joints | 7.50 g | 9.38 g | allowance | fasteners and bonded joints |
| **total** | **677.91 g** | **763.24 g** | | |

**The growth rate is a property of the line, not of the module.** Week 2 gave nine of thirteen
lines a blanket 20 or 25 percent because their sections were assumed. Week 4 sorts every line
into one of four classes and each class carries a rate, decided before the total was looked at,
which is the rule D33 wrote after an audit found the old test could be passed by choosing a
number.

| Class | Rate | What it covers |
| --- | --- | --- |
| catalogue | 8 percent | a published part mass, plus leads, screws and heatshrink the listing omits |
| machined | 12 percent | a drawn part, plus machining allowance and a fillet the drawing has not got yet |
| calculated | 15 percent | a section computed from stock, plus resin uptake and bond fillets |
| allowance | 25 percent | not drawn at all: the harness, fasteners, adhesive and the reserve |

Weighted across the module that is 12.6 percent, against the 19.4 percent the envelope
carries.

**The visible reserve is 15.00 g**, on the frame and mount group because that is the least
developed part of the module and week 2 said so first. It covers gussets, cable clamps, the
servo bracket and the ESC tray, none of which is drawn. It is not spread across rounded lines
and it is not hidden in a growth rate. Separately, the 85.33 g between the nominal and
conservative columns is the module's uncertainty allowance and it is itemised line by line.

## Continuity with the week 2 envelope

Each group has to land within 25 percent of the envelope line it refines, and no envelope line
may end up with nothing refining it. Comparing totals alone would let the whole budget move into
the blades while everything else collapsed.

| Group | Envelope | Budget | Drift | Conservative |
| --- | --- | --- | --- | --- |
| blades | 88.33 g | 95.24 g | +7.8 percent | 108.93 g |
| rotor frame and hubs | 59.04 g | 62.65 g | +6.1 percent | 70.82 g |
| pitch mechanism | 50.49 g | 56.12 g | +11.2 percent | 61.56 g |
| rotor shaft | 59.73 g | 59.21 g | -0.9 percent | 67.39 g |
| main bearings | 14.00 g | 16.00 g | +14.3 percent | 17.28 g |
| frame and mounting hardware | 93.40 g | 107.78 g | +15.4 percent | 124.04 g |
| motor | 106.00 g | 106.00 g | 0 | 114.48 g |
| transmission | 50.23 g | 60.21 g | +19.9 percent | 66.92 g |
| esc | 20.00 g | 19.50 g | -2.5 percent | 21.06 g |
| vectoring actuator | 40.00 g | 40.00 g | 0 | 43.20 g |
| pitch offset controller | 8.00 g | 8.50 g | +6.2 percent | 9.18 g |
| module wiring harness | 26.01 g | 25.20 g | -3.1 percent | 31.50 g |
| fasteners and bonded joints | 22.00 g | 21.50 g | -2.3 percent | 26.88 g |

Four groups moved more than 10 percent and each has a reason.

**Transmission, up 19.9 percent, and this one is new.** The envelope line was sized for a 3.5 to
1 belt. D67 moved the ratio to 4.25 to hold the corrected motor torque, which takes the rotor
pulley from 56 teeth to 68 and the belt from 300 mm to 375. The pulley alone is 34.84 g against
28.15. Nothing was redrawn; the ratio changed and the parts followed it.

**Frame and mounting hardware, up 15.4 percent.** The 15.00 g reserve sits here. Without it the
group is 92.78 g against an envelope of 93.40, so the drawn part of the group lands almost
exactly on the line it refines.

**Main bearings, up 14.3 percent.** Two 61802 bearings at 8.0 g rather than the 7.0 g the
envelope assumed, which is what a 15 mm bore costs on this shaft.

**Pitch mechanism, up 11.2 percent.** Week 3 left the sector gear and the carrier ring gear out
of the envelope line's stated basis; they are 12.40 g between them. The envelope line has since
grown to 50.49 g to hold the second pitch bearing at each root station, so the residual drift is
the gear pair and little else.

The rotor shaft group used to sit 10.8 percent under its line and now sits 0.9 percent under it.
Nothing about the shaft changed. D67 corrected the end plugs, which had no allowance for the
15 mm journal their own basis describes, and that closed most of the gap.

**The blade grew 7.8 percent, and it grew for two reasons worth naming.** The section perimeter
integrates to 2.090 chords rather than the assumed 2.05, so the skin is 0.18 g per blade
heavier. And the root close-out was a single 4.53 g allowance; drawn as two 7075-T6 fittings
over the spar plus a bond line it is 6.65 g. Neither is a mistake in week 2, both are what
happens when an allowance becomes a part.

## Thrust-to-weight

Weight is 6.6503 N at the nominal budget. Four cases, and all four are reported, because
reporting one of them is how week 2 confused itself for a fortnight. D32 makes that a rule.

| Case | Thrust | Mass | T/W | Against 2.5 |
| --- | --- | --- | --- | --- |
| design point | 17.00 N | 677.91 g | 2.5563 | clears by 2 percent |
| coefficient downside alone | 16.15 N | 677.91 g | 2.4284 | misses by 3 percent |
| mass downside alone | 17.00 N | 763.24 g | 2.2705 | misses by 9 percent |
| both stacked | 16.15 N | 763.24 g | 2.1569 | misses by 14 percent |

**The design case clears the requirement and the three downside cases do not.** Before D67 all
four cleared. What moved was the figure of merit, which took the design point from 18 N to 17,
and six envelope lines that were wrong for reasons of their own. The requirement is stated on
the module and the module meets it on the design estimate. Holding the downside cases to 2.5 as
well was this project's own discipline rather than the competition's, and that is the part the
corrections spent.

What the downsides are held to now is a declared floor of 2.0, which the stacked case clears at
2.1569, and the gate requires the closing mass to be computed and published rather than argued
away. **It is 104.76 g.** The conservative column would have to reach 658.48 g and it holds
763.24. That is a mass reduction programme, and Stage 2 item 6 is where it belongs.

The fallback list is worth reading against that. The decision gate offered three moves in order:
take another row of the frozen thrust sensitivity table, trim a budget line with genuine slack,
or reopen radius. The first is closed, because no row below 17 N comes near the 19.7045 N the
stacked case would need. The second is closed by D33, because every remaining line is a drawn
section or a catalogue part. The third is closed because the regenerated radius sweep still puts
110 mm at the top of what a drive covers. So no line was trimmed to reach a number and radius
was not reopened, and the gap is published instead.

## Margin against the 2.75 target

D17 wants the conservative column at 2.75, which needs 598.62 g. It holds 763.24, so the gap is
164.62 g. On the envelope the same gap is 162.43 g, so refinement did not pay it back at all.
It cost 2.19 g.

That is worth setting out, because refinement pushed in both directions at once and the two
nearly cancel. The growth allowance fell from 123.82 g to 85.33 g, which is 19.4 percent of the
nominal column down to 12.6, and it is worth 38.49 g. Against that, the nominal column rose
40.68 g: the 68 tooth pulley and the longer belt, the 20 g class servos, the gear pair, the
corrected hub bosses and shaft plugs and bearing blocks and motor plate. 38.49 less 40.68 leaves
the conservative column 2.19 g heavier than the envelope it refines.

**Neither target is met and neither is claimed.** 2.75 is a judgment target from D17 and 2.5 on
the downside cases was this project's own rule, and this document does not treat a 2.1569 as if
it were either. What would close them is not another pass over the budget, because every
remaining line is a drawn section or a catalogue part and trimming one to land a number is
exactly the move D33 exists to stop. The routes that would actually close them are a lighter
drive than the MN5006 at this power, which nothing in the shortlist offers, or a measured blade
area coefficient that retires the last 5 percent of the haircut and takes the conservative
thrust back to 17.0 N. The second alone moves the stacked case to 2.2705, still short.

One thing week 4 could have spent and did not. Balancing the blade chordwise would take the
pitch link from 144.19 N to 76.52 N, and it costs 35.47 g of nose ballast across three blades.
That drops the stacked case from 2.1569 to 2.0610, which still clears the declared floor, so the
mass argument that used to decline it no longer decides. What decides it is the load path: the
pitch link carries the unbalanced blade on a margin of 3.29 against a balanced 6.20, and 3.29 is
already more than twice the 1.5 floor, so the mass buys nothing the design needs. Both link
loads come from the solver under `--balanced`. See D46, D53 and D67.

## Numbers used

- results.total_mass_g = 677.91
- results.weight_N = 6.6503
- results.thrust_to_weight = 2.5563
- results.mass_g_conservative = 763.24
- results.thrust_to_weight_conservative = 2.1569
- results.mass_envelope_g = 637.23
- performance.thrust_N = 17.0
- performance.thrust_N_conservative = 16.1493
- structure.pitch_link_load_N = 144.19
- structure.pitch_link_margin = 3.2878
- structure.blade_mass_kg = 0.031747