# Mass and thrust to weight

Required Stage 1 item 5. This is the refined component mass budget and the thrust to weight it
gives, replacing the coarse envelope week 2 used to decide whether the design closed at all.

Short version. The module weighs 607.97 g nominal and 684.70 g in the conservative column. At
18.0 N that is a thrust to weight of 3.018. Stacking the low thrust coefficient on the
conservative mass gives 2.5457, which clears the 2.5 requirement by 12.5 g of mass. The internal
2.75 target from D17 is not met and the gap is 50.9 g.

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
| rotor hub bosses, 2 off | 14.41 g | 16.14 g | machined | rotor frame and hubs |
| root attachment brackets, 6 off | 18.00 g | 20.16 g | machined | rotor frame and hubs |
| pitch bearings, 6 off | 7.80 g | 8.42 g | catalogue | pitch mechanism |
| pitch links with rod ends, 3 off | 12.28 g | 13.27 g | catalogue | pitch mechanism |
| pitch horns, 3 off | 6.58 g | 7.37 g | machined | pitch mechanism |
| offset pivot post and pin | 6.50 g | 7.28 g | machined | pitch mechanism |
| phasing carrier ring, 40 mm gear | 7.90 g | 8.85 g | machined | pitch mechanism |
| servo sector gear, 60 mm | 4.50 g | 5.04 g | machined | pitch mechanism |
| carrier support bearings, 2 off | 4.40 g | 4.75 g | catalogue | pitch mechanism |
| rotor shaft tube | 36.01 g | 41.41 g | calculated | rotor shaft |
| shaft end plugs, 2 off | 17.24 g | 19.31 g | machined | rotor shaft |
| main bearings, 2 off | 16.00 g | 17.28 g | catalogue | main bearings |
| bearing blocks, 2 off | 16.00 g | 17.92 g | machined | frame and mounting hardware |
| frame tubes, 4 off | 46.36 g | 53.31 g | calculated | frame and mounting hardware |
| motor mount plate | 8.00 g | 8.96 g | machined | frame and mounting hardware |
| airframe mount lugs, 4 off | 7.20 g | 8.06 g | machined | frame and mounting hardware |
| frame and mount design reserve | 15.00 g | 18.75 g | allowance | frame and mounting hardware |
| motor, MN5006 KV450 | 106.00 g | 114.48 g | catalogue | motor |
| rotor belt pulley, 56 tooth | 28.15 g | 31.53 g | machined | transmission |
| motor belt pulley, 16 tooth | 6.62 g | 7.41 g | machined | transmission |
| drive belt | 10.20 g | 11.02 g | catalogue | transmission |
| belt tensioner and bracket | 6.00 g | 6.72 g | machined | transmission |
| esc, 40 A 6S class | 19.50 g | 21.06 g | catalogue | esc |
| vectoring actuator servos, 2 off | 25.00 g | 27.00 g | catalogue | vectoring actuator |
| pitch offset controller | 8.50 g | 9.18 g | catalogue | pitch offset controller |
| module wiring harness | 15.60 g | 19.50 g | allowance | module wiring harness |
| fasteners and threaded inserts | 14.00 g | 17.50 g | allowance | fasteners and bonded joints |
| structural adhesive at module joints | 7.50 g | 9.38 g | allowance | fasteners and bonded joints |
| **total** | **607.97 g** | **684.70 g** | | |

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

Weighted across the module that is 12.6 percent, against the 19.4 percent week 2 carried.

**The visible reserve is 15.00 g**, on the frame and mount group because that is the least
developed part of the module and week 2 said so first. It covers gussets, cable clamps, the
servo bracket and the ESC tray, none of which is drawn. It is not spread across rounded lines
and it is not hidden in a growth rate. Separately, the 76.73 g between the nominal and
conservative columns is the module's uncertainty allowance and it is itemised line by line.

## Continuity with the week 2 envelope

Each group has to land within 25 percent of the envelope line it refines, and no envelope line
may end up with nothing refining it. Comparing totals alone would let the whole budget move into
the blades while everything else collapsed.

| Group | Envelope | Budget | Drift | Conservative |
| --- | --- | --- | --- | --- |
| blades | 88.33 g | 95.24 g | +7.8 percent | 108.93 g |
| rotor frame and hubs | 49.48 g | 53.89 g | +8.9 percent | 61.01 g |
| pitch mechanism | 42.69 g | 49.96 g | +17.0 percent | 54.98 g |
| rotor shaft | 59.73 g | 53.25 g | -10.8 percent | 60.72 g |
| main bearings | 14.00 g | 16.00 g | +14.3 percent | 17.28 g |
| frame and mounting hardware | 78.18 g | 92.56 g | +18.4 percent | 107.00 g |
| motor | 106.00 g | 106.00 g | 0 | 114.48 g |
| transmission | 50.23 g | 50.97 g | +1.5 percent | 56.68 g |
| esc | 20.00 g | 19.50 g | -2.5 percent | 21.06 g |
| vectoring actuator | 25.00 g | 25.00 g | 0 | 27.00 g |
| pitch offset controller | 8.00 g | 8.50 g | +6.2 percent | 9.18 g |
| module wiring harness | 16.41 g | 15.60 g | -4.9 percent | 19.50 g |
| fasteners and bonded joints | 22.00 g | 21.50 g | -2.3 percent | 26.88 g |

Four groups moved more than 10 percent and each has a reason.

**Pitch mechanism, up 17.0 percent.** Week 3 left this as an open debt: the sector gear and the
carrier ring gear that couple the servos to the phasing carrier were in the design but not in
the week 2 line's stated basis. They are 12.40 g between them. The line grows to hold them
rather than pretending they fit, which was the choice week 3 handed over.

**Frame and mounting hardware, up 18.4 percent.** The 15.00 g reserve sits here. Without it the
group is 77.56 g against an envelope of 78.18, so the drawn part of the group landed almost
exactly where week 2 put it.

**Rotor shaft, down 10.8 percent.** Week 2 carried a torque scaled drive end allowance of 18 g
per newton metre, which is 25.5 g of unspecified hardware. Drawing the actual tube and its two
bonded end plugs gives 53.25 g. The parts that allowance was standing in for have moved into the
transmission group, where the pulleys are.

**Main bearings, up 14.3 percent.** Two 61802 bearings at 8.0 g rather than the 7.0 g the
envelope assumed, which is what a 15 mm bore costs on this shaft.

**The blade grew 7.8 percent, and it grew for two reasons worth naming.** The section perimeter
integrates to 2.090 chords rather than the assumed 2.05, so the skin is 0.18 g per blade
heavier. And the root close-out was a single 4.53 g allowance; drawn as two 7075-T6 fittings
over the spar plus a bond line it is 6.65 g. Neither is a mistake in week 2, both are what
happens when an allowance becomes a part.

## Thrust-to-weight

Weight is 5.9642 N at the nominal budget. Four cases, and all four are reported, because
reporting one of them is how week 2 confused itself for a fortnight. D32 makes that a rule.

| Case | Thrust | Mass | T/W | Against 2.5 |
| --- | --- | --- | --- | --- |
| design point | 18.00 N | 607.97 g | 3.018 | clears by 21 percent |
| mass downside alone | 18.00 N | 684.70 g | 2.680 | clears by 7 percent |
| coefficient downside alone | 17.10 N | 607.97 g | 2.867 | clears by 15 percent |
| both stacked | 17.10 N | 684.70 g | 2.5457 | clears by 12.5 g |

The stacked row is the hard gate D30 moved into week 4, and it is applied to this budget rather
than to the week 2 estimate. It clears. The conservative column could reach 697.16 g before it
fell under 2.5, and it sits at 684.70 g.

Nothing in the fallback list was needed. The decision gate offered three moves in order: take
another row of the frozen thrust sensitivity table, trim a budget line with genuine slack, or
reopen radius. The refined budget cleared the limit on the first pass at 18.0 N, so the design
thrust stays where week 2 froze it, no line was trimmed to reach a number, and radius was never
opened. That last one had a deadline of day 2 of the week and it passed unused.

## Margin against the 2.75 target

D17 wants the conservative column at 2.75, which needs 633.83 g. It holds 684.70, so the gap is
50.87 g. Week 2 left the gap at 58.6 g against a 692.43 g estimate, so refinement paid back 7.7
g of it, or 13 percent.

That is a smaller return than D31 expected, and the reason is that refinement pushed in both
directions at once. Growth rates fell from 19.4 percent to 12.6, worth 40.7 g. Against that, the
gear pair arrived at 12.40 g, the controller at 0.50 g, the blade close-out at 6.36 g and the
bearings, brackets and reserve at most of the rest, so the nominal column rose 27.9 g. The net
is 7.7 g.

**The target is not met and it is not claimed.** It is a judgment target from D17, not the
competition limit, and this document does not treat a 2.5457 as if it were 2.75. What would
close it is not another pass over the budget: every remaining line is a drawn section or a
catalogue part, and trimming one to land a number is exactly the move D33 exists to stop. The
routes that would actually close it are a lower KV motor on more cells, which reopens the 100 mm
radius row at 2.655 and needs a datasheet nobody has opened, or a measured blade area
coefficient that retires the last 5 percent of the haircut. Both are outside week 4.

One thing week 4 could have spent and did not. Balancing the blade chordwise would have taken
the pitch link from 105.93 N to about 69 N, and it costs 35.47 g of nose ballast across three
blades. That drops the stacked case to 2.406, under the hard limit. The pitch load path carries
the unbalanced blade on a margin of 3.30, so the mass buys nothing that is needed. See D46.

## Numbers used

- results.total_mass_g = 607.97
- results.weight_N = 5.9642
- results.thrust_to_weight = 3.018
- results.mass_g_conservative = 684.7
- results.thrust_to_weight_conservative = 2.5457
- results.mass_envelope_g = 580.05
- performance.thrust_N = 18.0
- performance.thrust_N_conservative = 17.0992
- structure.pitch_link_load_N = 105.93
- structure.pitch_link_margin = 3.3015
- structure.blade_mass_kg = 0.031747
