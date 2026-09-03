# Rotor sizing

Required Stage 1 item 2. Geometry, the radius trade, the blade section, and the coarse mass
envelope that decides whether any of it closes.

Read the last section first if you only have a minute. The sizing works and the geometry is
frozen, and the design case clears thrust to weight 2.5 at 2.5563 on the week 4 refined budget.
The stacked conservative case does not. It sits at 2.1569, and closing it would take 104.76 g
out of a 763.2 g conservative column. D67 is where that changed: a corrected figure of merit
moved the design point from 18 N to 17 N and six mass lines went up. The downside cases are
held to a declared floor of 2.0 now and the gap is published rather than trimmed away. See D30,
D35, D47 and D67.

## Shape family

The family is Kellen's UAV-scale optimum: 3 blades, chord at 0.66 of the radius, blade aspect
ratio 4 so the span is 2.64 radii, NACA 0020, pitching plus or minus 40 degrees. Solving that
family for a given thrust pins the Reynolds number regardless of radius, because chord and span
both scale with radius and the size cancels out of the product of tip speed and chord.

At 17 N of design thrust the family gives a chord Reynolds number of 130,300.

**That number was a problem and this is where the correction goes.** The published support for
carrying a thrust coefficient across a change of Reynolds number was Shrestha and Benedict, who
show non-dimensional thrust holding while torque and power fall, over 10,000 to 100,000.
130,300 sits above that, and D25 recorded the design point as an extrapolation on those grounds.

Kellen 2019 is in hand now and it changes what that sentence can claim. Kellen measured this
exact shape family across a chord Reynolds range of 100,000 to 300,000, and his 3-bladed
optimum sits at 186,000 on a 5.5 in chord at 20 m/s. The design point is inside that range, so
the geometry and the coefficient it carries are bracketed by a measurement on their own shape
instead of sitting past the end of an invariance claim made about something else. D37 narrows
D25 to the part that survives.

What survives is worth naming. The nominal coefficient still comes from a Benedict rotor at a
chord Reynolds of 31,600, and Shrestha is still the only support for carrying a value across
that gap. Kellen bounds the shape family and the low case, and he is not the provenance of the
nominal. Reynolds also has room underneath it: design thrust can fall to 15.76 N before the stacked
case reaches its declared floor of 2.0, and Reynolds there is 125,500, still well inside <!-- allow: 125,500 is the chord Reynolds at 15.76 N, not at the design point. It sits near the design figure because the two thrusts are close, and it is a different operating point rather than a stale copy -->
Kellen's band.

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
a peak blade load of 14.43 N spread over the span, simply supported at both spiders, tip
deflection is 0.09 mm, which is 0.12 percent of chord. Torsional stiffness from the closed
cell is 7.81 Nm2 and the twist under the aerodynamic pitching moment about a 30 percent axis is
0.014 degrees, against a pitch amplitude of 40 degrees.

Bending and aerodynamic torsion are both negligible, then. Blade torsion under the centrifugal
pitching moment is not, and week 4 is where that showed up: the blade is driven in pitch from
one end, so 2.0967 Nm winds it up by 2.23 degrees at the far end and about 1.5 degrees on span
average, which is just under 4 percent of the pitch amplitude. That is most of the 5 percent the low
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
| 100 mm | 2828 | 194.9 W | 373.7 W | 1.402 Nm | 531.5 W | none fits | 662 g | 2.211 |
| 110 mm | 2337 | 177.2 W | 339.7 W | 1.542 Nm | 483.2 W | 4.25 to 1 | 678 g | 2.157 |
| 120 mm | 1964 | 162.4 W | 311.4 W | 1.683 Nm | 442.9 W | 4.625 to 1 | 696 g | 2.099 |
| 130 mm | 1673 | 149.9 W | 287.5 W | 1.823 Nm | 408.9 W | 5.0 to 1 | 717 g | 2.038 |
| 140 mm | 1443 | 139.2 W | 266.9 W | 1.963 Nm | 379.6 W | 5.375 to 1 | 739 g | 1.974 |

Power times radius is constant across the sweep, which is the 1 over R behaviour the family
predicts, and Reynolds is 130,300 on every row because it depends on thrust and not on size.
The module mass column is the week 4 refined budget rebuilt at each radius, not the week 2
envelope the earlier version of this table used.

**The binding constraint is the drive, and it is worth being exact about where.** Conservative
thrust to weight rises all the way down the radius range, because the geometry-scaled mass
falls faster than the drive mass rises. The 100 mm row would give 2.211, which is better than
anything the design can actually reach. No shortlist motor holds it, and since D67 the reason
is power rather than speed: 100 mm asks 531.5 W at the motor terminals against the 520 W the
MN5006 carries continuously, and nothing lighter in the shortlist carries more. The
power-route agreement, which the first draft blamed, is nowhere near binding. The published
route is set by thrust alone while the aerodynamic route falls as 1 over radius, so the two
cross exactly at 136.3 mm and the spread widens either side of that: 35 percent at about 88.6
mm and again at about 184 mm. The 110 mm design point sits at 19.3 percent, and 100 mm at 26.6
percent, both inside the 35 percent limit.

So the radius is chosen at 110 mm because that is the smallest radius a named drive can hold
continuously, not because it is where the physics wants to be. That is a real finding and it
points at the cheapest fix available.

**Second candidate: 120 mm.** It costs 0.058 of conservative thrust to weight and buys 40 W
less motor input, 373 rpm less rotor speed, and a drive at 85 percent of its continuous power
instead of 93. It is the row to pick if week 3 finds the linkage cannot be packaged at 110 mm,
and it is not free, because link lengths, offset geometry and gearing all move with radius and
switching after week 3 still costs a week 3 rerun.

## Mass envelope

Coarse, component level, and every line is a build-up rather than a percentage. Each carries
its scaling class, which is D15: the drive is not a fixed mass. Conservative rates go by what a
line is made of, so catalogue parts take 15 percent, anything computed from an assumed section
takes 20 percent, and the module frame takes 25 percent because it is the least developed part
of the design.

This started as the week 2 estimate. D67 corrected six of its thirteen lines, because they
were wrong for reasons that had nothing to do with the refinement week 4 did separately: a hub
boss drawn with a 14 mm bore on a 16 mm shaft, bearing blocks carried at 16 g against 25.3 g
for the housing their own description gives, a motor plate at 8 g against 14 g, root brackets
hard coded at 3.00 g, shaft plugs with no allowance for the journal they sit on, and a harness
priced as one conductor when current goes out and comes back. Week 4 separately replaced the
whole thing line by line with real sections and catalogue parts, and that budget is in
`05-mass-and-tw.md`: 677.9 g nominal and 763.2 g conservative.

| Line | Class | Nominal | Conservative | Rate |
| --- | --- | --- | --- | --- |
| blades | geometry | 88.3 g | 106.0 g | 20 |
| rotor frame and hubs | geometry | 59.0 g | 70.9 g | 20 |
| pitch mechanism | geometry | 50.5 g | 60.6 g | 20 |
| rotor shaft | power | 59.7 g | 71.7 g | 20 |
| main bearings | power | 14.0 g | 16.1 g | 15 |
| frame and mounting hardware | geometry | 93.4 g | 116.7 g | 25 |
| motor | power | 106.0 g | 121.9 g | 15 |
| transmission | power | 50.2 g | 60.3 g | 20 |
| esc | power | 20.0 g | 23.0 g | 15 |
| vectoring actuator | power | 40.0 g | 46.0 g | 15 |
| pitch offset controller | fixed | 8.0 g | 9.2 g | 15 |
| module wiring harness | geometry | 26.0 g | 31.2 g | 20 |
| fasteners and bonded joints | geometry | 22.0 g | 27.5 g | 25 |
| **total** | | **637.2 g** | **761.1 g** | 19.4 |

Geometry-scaled lines come to 339 g, power or torque-scaled to 290 g, and genuinely fixed to
**8 g**.

That last number is the one to sit with. D11 and D13 argue that the thrust to weight case
rests on fixed hardware amortising over five times the thrust. Sorted honestly, this module has
one fixed line in it, an 8 g controller board. Wiring follows the envelope. Fasteners follow
the frame. Servo torque follows the pitch link load, which follows thrust. Bearings and the
shaft follow rotor torque. The amortisation argument is therefore much weaker than D11 and D13
assume, and the week 2 answer reflects that: almost nothing in this module is free when the
rotor grows.

D11 also set a threshold, that non-blade hardware has to come in under roughly 40 percent of
the mass ceiling. **That threshold is missed now.** Non-blade power-scaled and fixed hardware
is 298 g against a nominal ceiling of 693 g at 17 N, so 43 percent. It moved for two reasons
at once: the corrected vectoring actuator and the corrected drive lines put 15 g on the
numerator, and the design point falling from 18 N to 17 N took 40 g off the ceiling. D11 set
the figure as a rough screen rather than a limit, and nothing in the design gates on it, but
it was inside before D67 and it is outside now and this document is not going to bury that.

## The verdict, and the freeze

There are four thrust to weight cases here, not one, and reporting a single number hid that for
most of week 2.

| Case | Thrust | Mass | T/W | Against 2.5 |
| --- | --- | --- | --- | --- |
| design point | 17.00 N | 677.9 g | 2.5563 | clears by 2 percent |
| coefficient downside alone | 16.15 N | 677.9 g | 2.4284 | misses by 3 percent |
| mass downside alone | 17.00 N | 763.2 g | 2.2705 | misses by 9 percent |
| both stacked | 16.15 N | 763.2 g | 2.1569 | misses by 14 percent |

Every row is on the week 4 refined budget now, nominal and conservative both. The earlier
version of this table mixed the week 2 envelope into rows 1 and 3 and the refined column into
rows 2 and 4, which made the four rows harder to read against each other than they needed to
be.

**One of the four clears 2.5 and three do not.** That is the change D67 made and it is the
most important sentence in this document. Before it, all four cleared. The design point moved
from 18 N to 17 N because the figure of merit was being read inconsistently with the thrust
coefficient, and six mass lines went up for reasons unrelated to that. Geometry still freezes,
because D30 froze it on the design case and the design case still clears, but the margin
around it is thinner than week 2 reported and the downside cases are now below the requirement
rather than above it.

What the downside cases are held to instead is a declared floor of 2.0, and the stacked case
sits at 2.1569 against it. The gate also requires the closing mass be computed and published:
104.76 g out of the 763.2 g conservative column, or a target of 658.5 g. That is a mass
reduction programme for Stage 2 and not an arithmetic change available now, and D67 says so in
those words rather than moving a threshold quietly.

The stacked case moved twice before this. First the coefficient: the low value is 0.5752
rather than 0.5147 since D35 retired the configuration-transfer allowance, so conservative
thrust is 16.15 N rather than 14.45 N at the current design point. Then the mass, once week 4
refined it, and again once D67 corrected it.

D30 counts as nine the lines that stopped carrying a blanket 20 or 25 percent growth rate on
an assumed section. Eight is what `mass_envelope_g` gives, and the 95.6 g of growth allowance
those eight carry is the correct figure.

The internal 2.75 target from D17 is further away than it was and is still not claimed. It
needs the conservative column at 598.6 g against the 763.2 g it holds, so 164.6 g. Week 4 took
7.7 g off and stopped, because every remaining line is a drawn section or a catalogue part and
trimming one to reach a number is what D33 exists to prevent. Nothing here has been trimmed to
reach a number since.

## Numbers used

- geometry.radius_m = 0.110
- geometry.chord_m = 0.0726
- geometry.span_m = 0.2904
- performance.blade_area_coeff = 0.6055
- performance.blade_area_coeff_low = 0.5752
- performance.blade_deflection_thrust_loss = 0.05
- performance.solidity = 0.3151
- performance.blade_tip_deflection_mm = 0.09
- performance.blade_twist_deg = 0.014
- performance.thrust_N_conservative = 16.1493
- performance.motor_input_W = 483.158
- results.mass_envelope_g = 637.23
- results.mass_g_conservative = 763.24
- results.thrust_to_weight_conservative = 2.1569