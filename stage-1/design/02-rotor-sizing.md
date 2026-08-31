# Rotor sizing

Required Stage 1 item 2. Geometry, the radius trade, the blade section, and the coarse mass
envelope that decides whether any of it closes.

Read the last section first if you only have a minute. The sizing works, the geometry is
frozen, and the stacked conservative case clears thrust to weight 2.5 at 2.5457 on the week 4
refined budget. It clears by 12.5 g of conservative mass, which is thin but no longer a knife
edge. The internal 2.75 target from D17 is still unmet and the gap is 50.9 g. See D30, D35 and
D47, which is where the conservative column stopped being the week 2 estimate.

## Shape family

The family is Kellen's UAV-scale optimum: 3 blades, chord at 0.66 of the radius, blade aspect
ratio 4 so the span is 2.64 radii, NACA 0020, pitching plus or minus 40 degrees. Solving that
family for a given thrust pins the Reynolds number regardless of radius, because chord and span
both scale with radius and the size cancels out of the product of tip speed and chord.

At 18 N of design thrust the family gives a chord Reynolds number of 134,000.

**That number was a problem and this is where the correction goes.** The published support for
carrying a thrust coefficient across a change of Reynolds number was Shrestha and Benedict, who
show non-dimensional thrust holding while torque and power fall, over 10,000 to 100,000.
134,000 sits above that, and D25 recorded the design point as an extrapolation on those grounds.

Kellen 2019 is in hand now and it changes what that sentence can claim. Kellen measured this
exact shape family across a chord Reynolds range of 100,000 to 300,000, and his 3-bladed
optimum sits at 186,000 on a 5.5 in chord at 20 m/s. The design point is inside that range, so
the geometry and the coefficient it carries are bracketed by a measurement on their own shape
instead of sitting past the end of an invariance claim made about something else. D37 narrows
D25 to the part that survives.

What survives is worth naming. The nominal coefficient still comes from a Benedict rotor at a
chord Reynolds of 31,600, and Shrestha is still the only support for carrying a value across
that gap. Kellen bounds the shape family and the low case, and he is not the provenance of the
nominal. Raising thrust is no longer the trap it was either: with the haircut at 5 percent
rather than 15, design thrust can fall to 10.53 N before the conservative case fails, and
Reynolds there is 102,500, still inside Kellen's band.

Solidity comes out at 0.3151 on the definition the gate uses, blades times chord over the
circumference. Kellen's measured optimum band is 0.30 to 0.40, read off the thesis rather than
a summary of it, so the coefficient is used inside the solidity range it was measured for,
which is what D12 requires. The rotor the
coefficient came from has a solidity of 0.276 and is outside that band itself, so the transfer
runs into the band from outside on this axis too.

**The coefficient, and where it actually came from.** The repository built 0.6055 from 1.98 N
per rotor at 2000 rpm on Benedict's quad-cyclocopter, 4 blades of 33.0 mm chord and 158.8 mm
span at 76.2 mm radius. Reading the dissertation shows that pair is not in it. 1.98 N is the
809 gram all-up vehicle weight of Table 5.1 divided by four, and 2000 rpm belongs to the twin
rotor. The quad's measured hover point is 1.91 N at 1800 rpm on printed p.236, repeated as 195
grams at 1800 rpm on p.225, and in this project's blade-area convention that is 0.7211.

0.6055 is kept anyway. It is deliberate margin now rather than a transferred estimate: the
corrected quad point is 0.7211, Kellen's measurement on this shape family is 0.6648, and the
twin is 0.8114, so every measured or corrected value available sits above the number the design
is built on. Raising it would raise thrust everywhere and spend a margin nothing needs spent.
D36 records the call and the correction together.

The same recompute on Benedict's twin rotor, which has 3 blades like ours at the same radius
and the same 2000 rpm on a 25.4 mm chord and a 152.4 mm span, gives 0.8114. That is 34 percent
higher than the quad. It supports Benedict's own finding that at fixed solidity fewer blades
give more thrust, and it is not adopted, because the twin sits at a solidity of 0.159 and that
is a long way outside the band. It is in `numbers.json` as an upside scenario and nothing rests
on it.

**The low coefficient is built, not published.** Two allowances, added rather than compounded
because adding is the harsher of the two:

- 5 percent for blade flexibility
- 10 percent for configuration transfer, since blade count, airfoil and chord ratio all moved at
  once with nothing measured to de-risk it

The second one is retired. D23 set the test: a measured coefficient for this shape family, in
this Reynolds band, at or above the transferred value. Kellen 2019 gives 0.6648 on a rotor
whose solidity and chord-to-radius sit within 1.1 percent of ours, which passes it. So the low
coefficient is 0.5752, the nominal less blade flexibility alone.

It is still an engineering downside scenario and not a published lower bound. What changed is
that the half of the haircut covering an unmeasured configuration change now has a measurement
under it. See D35.

## Blade section and stiffness

The blade is a closed cell: PMI foam core at 52 kg/m3 filling 88 percent of the NACA 0020
section, two plies of 60 gsm carbon twill as skin at 0.22 kg/m2 over a perimeter of 2.05
chords, and a CFRP spar tube of 0.12 chord diameter with a 0.5 mm wall. Bond line and two root
fittings close it out.

At the design chord of 72.6 mm and span of 290.4 mm that is 9.60 g of foam, 9.51 g of skin,
5.81 g of spar and 4.53 g of bond and fittings, so 29.4 g per blade and 88.3 g for the set.
Those are the week 2 figures and week 4 moved two of them. Integrating the section rather
than assuming a perimeter takes the skin to 9.69 g, and drawing the root close-out as two
fittings and a bond line takes 4.53 g to 6.65 g, so the blade is 31.75 g and the set is
95.24 g. `05-mass-and-tw.md` carries both columns.

The stiffness check **bounds the flexibility allowance from above, and does not derive it.**
That distinction matters and the first draft of this document got it wrong. Week 4 rebuilt the
section with named material allowables in `tools/structure.py`, and the figures below are that
rebuild rather than the week 2 estimate it replaced. Bending stiffness works out at 51.1 Nm2,
dominated by the skin rather than the spar because the skin sits at the section extremes. Under
a peak blade load of 15.01 N spread over the span, simply supported at both spiders, tip
deflection is 0.0936 mm, which is 0.13 percent of chord. Torsional stiffness from the closed
cell is 7.81 Nm2 and the twist under the aerodynamic pitching moment about a 30 percent axis is
0.0145 degrees, against a pitch amplitude of 40 degrees.

Bending and aerodynamic torsion are both negligible, then. Blade torsion under the centrifugal
pitching moment is not, and week 4 is where that showed up: the blade is driven in pitch from
one end, so 2.2058 Nm winds it up by 2.35 degrees at the far end and about 1.6 degrees on span
average, which is 4 percent of the pitch amplitude. That is most of the 5 percent the low
coefficient carries, and it turns the allowance from a floor into something with a calculation
under it. The rest still covers build tolerance, bond line variation and unsteady effects a
static beam model does not see. Benedict's finding is that bending and torsional flexibility
both hurt, and the wind up is the torsional half of it. See `08-structure-and-loads.md`.

## Radius

Radius is not a free trade of rpm against envelope. Inside a fixed shape family at fixed
thrust, aerodynamic power falls roughly as 1 over radius while rotor torque rises with it, and
every geometry-scaled mass line grows as the square or the cube. So a bigger rotor is a
lower-power rotor with heavier blades and a heavier shaft, and power alone cannot choose it.

| Radius | rpm | Ideal power | Aero power | Rotor torque | Motor input | Belt | Module mass | Conservative T/W |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 100 mm | 2645 | 212.3 W | 353.9 W | 1.291 Nm | 503.3 W | none fits | 550 g | 2.655 |
| 110 mm | 2405 | 193.0 W | 321.7 W | 1.419 Nm | 457.6 W | 3.5 to 1 | 580 g | 2.517 |
| 120 mm | 2021 | 176.9 W | 294.9 W | 1.548 Nm | 419.4 W | 4.0 to 1 | 612 g | 2.384 |
| 130 mm | 1722 | 163.3 W | 272.1 W | 1.677 Nm | 387.2 W | 4.5 to 1 | 646 g | 2.257 |
| 140 mm | 1565 | 151.6 W | 252.7 W | 1.806 Nm | 359.5 W | 4.5 to 1 | 683 g | 2.134 |

Power times radius is constant across the sweep, which is the 1 over R behaviour the family
predicts, and Reynolds is 134,000 on every row because it depends on thrust and not on size.

**The binding constraint is the drive, and it is worth being exact about where.** Conservative
thrust to weight rises all the way down the radius range, because the geometry-scaled mass
falls faster than the drive mass rises. The 100 mm row would give 2.376, which is better than
anything the design can actually reach. No shortlist motor holds it: the torque wants a belt
ratio the KV450 cannot spin to on a 6S pack, and the KV700 that has the speed does not have the
torque. The power-route agreement, which the first draft blamed, is nowhere near binding: it
crosses 35 percent at about 82 mm and again at about 170 mm, and every row above is inside 10
percent.

So the radius is chosen at 110 mm because that is the smallest radius a named drive can hold
continuously, not because it is where the physics wants to be. That is a real finding and it
points at the cheapest fix available.

**Second candidate: 120 mm.** It costs 0.12 of conservative thrust to weight and buys 38 W less
motor input, 384 rpm less rotor speed, and a drive at 81 percent of its continuous power
instead of 88. It is the row to pick if week 3 finds the linkage cannot be packaged at 110 mm,
and it is not free, because link lengths, offset geometry and gearing all move with radius and
switching after week 3 still costs a week 3 rerun.

## Mass envelope

Coarse, component level, and every line is a build-up rather than a percentage. Each carries
its scaling class, which is D15: the drive is not a fixed mass. Conservative rates go by what a
line is made of, so catalogue parts take 15 percent, anything computed from an assumed section
takes 20 percent, and the module frame takes 25 percent because it is the least developed part
of the design.

This is the week 2 estimate and it is left as it was written. Week 4 replaced it line by
line with real sections and catalogue parts, and the budget that came out is in
`05-mass-and-tw.md`: 608.0 g nominal and 684.7 g conservative. The comparison below is kept
because every later table in this document is built on it.

| Line | Class | Nominal | Conservative | Rate |
| --- | --- | --- | --- | --- |
| blades | geometry | 88.3 g | 106.0 g | 20 |
| rotor frame and hubs | geometry | 49.5 g | 59.4 g | 20 |
| pitch mechanism | geometry | 42.7 g | 51.2 g | 20 |
| rotor shaft | power | 59.7 g | 71.7 g | 20 |
| main bearings | power | 14.0 g | 16.1 g | 15 |
| frame and mounting hardware | geometry | 78.2 g | 97.7 g | 25 |
| motor | power | 106.0 g | 121.9 g | 15 |
| transmission | power | 50.2 g | 60.3 g | 20 |
| esc | power | 20.0 g | 23.0 g | 15 |
| vectoring actuator | power | 25.0 g | 28.8 g | 15 |
| pitch offset controller | fixed | 8.0 g | 9.2 g | 15 |
| module wiring harness | geometry | 16.4 g | 19.7 g | 20 |
| fasteners and bonded joints | geometry | 22.0 g | 27.5 g | 25 |
| **total** | | **580.1 g** | **692.4 g** | 19.4 |

Geometry-scaled lines come to 297 g, power or torque-scaled to 275 g, and genuinely fixed to
**8 g**.

That last number is the one to sit with. D11 and D13 argue that the thrust to weight case
rests on fixed hardware amortising over five times the thrust. Sorted honestly, this module has
one fixed line in it, an 8 g controller board. Wiring follows the envelope. Fasteners follow
the frame. Servo torque follows the pitch link load, which follows thrust. Bearings and the
shaft follow rotor torque. The amortisation argument is therefore much weaker than D11 and D13
assume, and the week 2 answer reflects that: almost nothing in this module is free when the
rotor grows.

D11 also set a threshold, that non-blade hardware has to come in under roughly 40 percent of
the mass ceiling. Non-blade power-scaled and fixed hardware is 283 g against a nominal ceiling
of 733 g at 18 N, so 39 percent. Just inside, and the sweep says the same thing from the other
direction.

## The verdict, and the freeze

There are four thrust to weight cases here, not one, and reporting a single number hid that for
most of week 2.

| Case | Thrust | Mass | T/W | Against 2.5 |
| --- | --- | --- | --- | --- |
| design point | 18.00 N | 580.1 g | 3.163 | clears by 27 percent |
| mass downside alone | 18.00 N | 684.7 g | 2.680 | clears by 7 percent |
| coefficient downside alone | 17.10 N | 580.1 g | 3.005 | clears by 20 percent |
| both stacked | 17.10 N | 684.7 g | 2.5457 | clears by 12.5 g |

The nominal mass in rows 1 and 3 is still the week 2 envelope, because those two rows are what
geometry froze on. The conservative mass in rows 2 and 4 is the week 4 refined budget, which is
where `results.mass_g_conservative` now comes from. Week 4's own nominal is 608.0 g, so the
design case on the refined budget is 3.018 rather than 3.163.

All four clear 2.5, and geometry freezes on the first three regardless, which is D30. The
stacked case moved twice. First the coefficient: the low value is 0.5752 rather than 0.5147
since D35 retired the configuration-transfer allowance, so conservative thrust is 17.10 N
rather than 15.30 N. Then the mass, once week 4 refined it.

Read the fourth row carefully. It clears by 12.5 g of conservative mass, meaning the column
could reach 697.2 g before the stacked case fell under 2.5, and it sits at 684.7 g. That is a
real pass and still a thin one. The hard stacked test lives in week 4 under D30, on a budget
where eight of these thirteen lines stopped carrying a blanket 20 or 25 percent growth rate on
an assumed section, and `week4: conservative T/W clears 2.5` applies the same limit to what
came out. Week 4 rebuilt the conservative column line by line under D33.

D30 counts those lines as nine. Eight is what `mass_envelope_g` gives, and the 86.4 g of growth
allowance quoted everywhere else comes from the correct eight.

Nominal thrust to weight is 3.163 on the envelope and 3.018 on the refined budget, either way
well above the best published module on the same boundary. The internal 2.75 target from D17 is
still not met on the stacked case and is still not claimed. What it needs is 50.9 g: the
conservative column would have to reach 633.8 g against the 684.7 g it holds. Week 4 took 7.7 g
off it and stopped, because every remaining line is a drawn section or a catalogue part and
trimming one to reach a number is what D33 exists to prevent. It is a target rather than the
hard limit, which the stacked case clears.

## Numbers used

- geometry.radius_m = 0.110
- geometry.chord_m = 0.0726
- geometry.span_m = 0.2904
- performance.blade_area_coeff = 0.6055
- performance.blade_area_coeff_low = 0.5752
- performance.blade_deflection_thrust_loss = 0.05
- performance.solidity = 0.3151
- performance.blade_tip_deflection_mm = 0.0936
- performance.blade_twist_deg = 0.0145
- performance.thrust_N_conservative = 17.0992
- performance.motor_input_W = 457.573
- results.mass_envelope_g = 580.05
- results.mass_g_conservative = 684.7
- results.thrust_to_weight_conservative = 2.5457
