# Rotor sizing

Required Stage 1 item 2. Geometry, the radius trade, the blade section, and the coarse mass
envelope that decides whether any of it closes.

Read the last section first if you only have a minute. The sizing works and the geometry is
frozen. The stacked conservative case is still 68.5 g short of thrust to weight 2.5, and that
shortfall now travels to week 4 as a mass target instead of holding the freeze. See D30.

## Shape family

The family is Kellen's UAV-scale optimum: 3 blades, chord at 0.66 of the radius, blade aspect
ratio 4 so the span is 2.64 radii, NACA 0020, pitching plus or minus 40 degrees. Solving that
family for a given thrust pins the Reynolds number regardless of radius, because chord and span
both scale with radius and the size cancels out of the product of tip speed and chord.

At 18 N of design thrust the family gives a chord Reynolds number of 134,000.

**That number is a problem and this document is the place to say so.** The published support
for carrying a thrust coefficient across a change of Reynolds number is Shrestha and Benedict,
who show non-dimensional thrust holding while torque and power fall, over 10,000 to 100,000.
134,000 is above that. Kellen studied 100,000 to 300,000 and reports this shape family as the
optimum there, which is why the family was chosen, but Kellen is not the source of the
coefficient. So the transfer is an extrapolation upward, out of the range that supports it and
into a range that has been studied for the shape but not for this quantity.

It is also not avoidable inside this family. The conservative thrust has to clear 10 N on its
own, the coefficient haircut is 15 percent, so design thrust cannot go below 11.76 N, and
Reynolds goes with the square root of thrust. The lowest compliant point in this family already
sits at 108,000. There is no design here that stays inside the documented band. Recorded as
D25, and it is the largest piece of unretired risk the freeze carries.

The direction of the extrapolation is at least the benign one. Shrestha's result is that
non-dimensional thrust barely moves while power falls, so pushing Reynolds up should not cost
thrust and should help power. That is an argument, not evidence.

Solidity comes out at 0.3151 on the definition the gate uses, blades times chord over the
circumference. Kellen's reported optimum band is 0.30 to 0.40, so the coefficient is being used
inside the solidity range it was reported for, which is what D12 requires. The rotor the
coefficient came from has a solidity of 0.276 and is outside that band itself, so the transfer
runs into the band from outside on this axis too.

**The coefficient, recomputed rather than quoted.** Benedict's quad-cyclocopter rotor makes
1.98 N per rotor at 2000 rpm on 4 blades of 33.0 mm chord and 158.8 mm span at 76.2 mm radius.
Tip speed is 15.96 m/s, blade area is 0.02096 m2, and dividing gives 0.6055 in this project's
own blade-area convention. The repository has been carrying 0.607, so the recompute agrees to
0.25 percent and the small difference is now the stored value.

The same recompute on Benedict's twin rotor, which has 3 blades like ours at the same radius
and the same 2000 rpm on a 25.4 mm chord and a 152.4 mm span, gives 0.8114. That is 34 percent
higher than the quad. It supports Benedict's own finding that at fixed solidity fewer blades
give more thrust, and it is not adopted, because the twin sits at a solidity of 0.159 and that
is a long way outside the band. It is in `numbers.json` as an upside scenario and nothing rests
on it.

**The low coefficient is built, not published.** Two allowances, added rather than compounded
because adding is the harsher of the two:

- 5 percent for blade flexibility
- 10 percent for configuration transfer, since blade count, airfoil and chord ratio all move at
  once and only the Reynolds half of the transfer has any published support at all

That gives 0.5147, or 85 percent of nominal. It is an engineering downside scenario. Kellen
2019 holds the measured coefficient for this exact family and it is not in hand, so nothing
here is a published lower bound and the submission has to say so.

## Blade section and stiffness

The blade is a closed cell: PMI foam core at 52 kg/m3 filling 88 percent of the NACA 0020
section, two plies of 60 gsm carbon twill as skin at 0.22 kg/m2 over a perimeter of 2.05
chords, and a CFRP spar tube of 0.12 chord diameter with a 0.5 mm wall. Bond line and two root
fittings close it out.

At the design chord of 72.6 mm and span of 290.4 mm that is 9.60 g of foam, 9.51 g of skin,
5.81 g of spar and 4.53 g of bond and fittings, so 29.4 g per blade and 88.3 g for the set.

The stiffness check **bounds the flexibility allowance from above, and does not derive it.**
That distinction matters and the first draft of this document got it wrong. Bending stiffness
works out at 58.4 Nm2, dominated by the skin rather than the spar because the skin sits at the
section extremes. Under a peak blade load of 14.2 N spread over the span, simply supported at
both spiders, tip deflection is 0.078 mm, which is 0.11 percent of chord. Torsional stiffness
from the closed cell is 8.4 Nm2 and the twist under the aerodynamic pitching moment about a 30
percent axis is 0.051 degrees, against a pitch amplitude of 40 degrees.

So the geometric pitch error the section actually allows is under a fifth of a percent, and a
thrust loss proportional to it would be far below 1 percent. The 5 percent in the low
coefficient is therefore a floor rather than a calculation: it covers build tolerance, bond
line variation, a spar that week 4 has not yet sized against centrifugal load, and unsteady
effects a static beam model does not see. Benedict's finding is that bending and torsional
flexibility both hurt, so the allowance is not zero, and the section says it should not be 5
percent either. It is kept at 5 because the section is preliminary.

## Radius

Radius is not a free trade of rpm against envelope. Inside a fixed shape family at fixed
thrust, aerodynamic power falls roughly as 1 over radius while rotor torque rises with it, and
every geometry-scaled mass line grows as the square or the cube. So a bigger rotor is a
lower-power rotor with heavier blades and a heavier shaft, and power alone cannot choose it.

| Radius | rpm | Ideal power | Aero power | Rotor torque | Motor input | Belt | Module mass | Conservative T/W |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 100 mm | 2645 | 212.3 W | 353.9 W | 1.291 Nm | 503.3 W | none fits | 550 g | 2.376 |
| 110 mm | 2405 | 193.0 W | 321.7 W | 1.419 Nm | 457.6 W | 3.5 to 1 | 580 g | 2.252 |
| 120 mm | 2021 | 176.9 W | 294.9 W | 1.548 Nm | 419.4 W | 4.0 to 1 | 612 g | 2.134 |
| 130 mm | 1722 | 163.3 W | 272.1 W | 1.677 Nm | 387.2 W | 4.5 to 1 | 646 g | 2.019 |
| 140 mm | 1565 | 151.6 W | 252.7 W | 1.806 Nm | 359.5 W | 4.5 to 1 | 683 g | 1.909 |

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
| mass downside alone | 18.00 N | 692.4 g | 2.650 | clears by 6 percent |
| coefficient downside alone | 15.30 N | 580.1 g | 2.689 | clears by 8 percent |
| both stacked | 15.30 N | 692.4 g | 2.252 | misses by 68.5 g |

Geometry freezes on the first three. 18 N, 110 mm, with 120 mm carried as insurance. The
stacked case is the one that misses and it is stated rather than buried: to reach 2.5 the
conservative column has to come down to 623.9 g, which is 68.5 g or 9.9 percent.

That target is now week 4's, and D30 gives the reasoning in full. The short version is what the
conservative column is made of. Nine of these thirteen lines say assumed in their basis and
carry a blanket 20 or 25 percent growth rate, so the stacked number tests those rates about as
hard as it tests the rotor. Week 4 replaces them with real sections, catalogue parts and a BOM,
and `week4: conservative T/W clears 2.5` applies the same limit to that budget. The hard test
did not go away. It moved to the week where the mass is real.

Nominal thrust to weight is 3.163, already 49 percent above the best published module on the
same boundary. Reaching 2.75 on the stacked case would need a nominal of 3.86, which is 81
percent above the published record, and nothing available supports that. So the internal 2.75
target from D17 is not met on the stacked case and is not claimed.

## Numbers used

- geometry.radius_m = 0.110
- geometry.chord_m = 0.0726
- geometry.span_m = 0.2904
- performance.blade_area_coeff = 0.6055
- performance.blade_area_coeff_low = 0.5147
- performance.blade_deflection_thrust_loss = 0.05
- performance.solidity = 0.3151
- performance.blade_tip_deflection_mm = 0.0778
- performance.blade_twist_deg = 0.0512
- performance.thrust_N_conservative = 15.3007
- performance.motor_input_W = 457.573
- results.mass_envelope_g = 580.05
- results.mass_g_conservative = 692.43
- results.thrust_to_weight_conservative = 2.2525
- results.mass_target_week4_g = 623.8818
