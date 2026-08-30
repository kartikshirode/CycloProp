# Rotor sizing

Required Stage 1 item 2. Geometry, the radius trade, the blade section, and the coarse mass
envelope that decides whether any of it closes.

Read the last section before the middle ones if you only have a minute. The sizing works. The
mass does not close against the conservative case, and the gap is 32 g.

## Shape family

The family is Kellen's UAV-scale optimum: 3 blades, chord at 0.66 of the radius, blade aspect
ratio 4 so the span is 2.64 radii, NACA 0020, pitching plus or minus 40 degrees. Solving that
family for a given thrust pins the Reynolds number regardless of radius, because chord and
span both scale with radius and the size cancels out of the product of tip speed and chord.

At 20 N of design thrust the family gives a chord Reynolds number of 141,000. Kellen studied
100,000 to 300,000, so this lands inside the band rather than extrapolating out of it. That is
the whole reason the family was chosen.

Solidity comes out at 0.3151 on the definition the gate uses, blades times chord over the
circumference. Kellen's measured optimum band is 0.30 to 0.40, so the transferred coefficient
is being used inside the range it was measured in, which is what D12 requires. Worth noting
that the rotor the coefficient came from has a solidity of 0.276 and is outside that band
itself. The transfer runs into the band from outside it.

**The coefficient, recomputed rather than quoted.** Benedict's quad-cyclocopter rotor makes
1.98 N per rotor at 2000 rpm on 4 blades of 33.0 mm chord and 158.8 mm span at 76.2 mm radius.
Tip speed is 15.96 m/s, blade area is 0.02096 m2, and dividing gives 0.6055 in this project's
own blade-area convention. The repository has been carrying 0.607, so the recompute agrees to
0.25 percent and the small difference is now the stored value.

The same recompute on Benedict's twin rotor, which has 3 blades like ours at the same radius
and the same 2000 rpm, gives 0.8114. That is 34 percent higher than the quad. It supports
Benedict's own finding that at fixed solidity fewer blades give more thrust, and it is not
adopted, because the twin sits at a solidity of 0.159 and that is a long way outside the
measured band. It is in `numbers.json` as an upside scenario and nothing rests on it.

**The low coefficient is built, not published.** Two allowances, added rather than compounded
because adding is the harsher of the two:

- 5 percent for blade flexibility, sized against the section below rather than picked
- 10 percent for configuration transfer, since blade count, airfoil and chord ratio all move
  at once and nothing measured de-risks any of it

That gives 0.5147, or 85 percent of nominal. It is an engineering downside scenario. Kellen
2019 holds the measured coefficient for this exact family and it is not in hand, so nothing
here is a published lower bound and the submission has to say so.

## Blade section and stiffness

The blade is a closed cell: PMI foam core at 52 kg/m3 filling 88 percent of the NACA 0020
section, two plies of 60 gsm carbon twill as skin at 0.22 kg/m2 over a perimeter of 2.05
chords, and a CFRP spar tube of 0.12 chord diameter with a 0.5 mm wall. Bond line and two root
fittings close it out.

At the design chord of 75.9 mm and span of 303.6 mm that is 10.96 g of foam, 10.39 g of skin,
6.36 g of spar and 4.60 g of bond and fittings, so 32.3 g per blade and 97.0 g for the set.

The stiffness check is what makes the 5 percent flexibility allowance a number rather than a
guess. Bending stiffness works out at 66.8 Nm2, dominated by the skin rather than the spar
because the skin sits at the section extremes. Under a peak blade load of 15.8 N spread over
the span, simply supported at both spiders, tip deflection is 0.086 mm. Torsional stiffness
from the closed cell is 9.6 Nm2 and the twist under the aerodynamic pitching moment about a
30 percent axis is 0.054 degrees.

Both are small, and Benedict's finding is that bending and torsional flexibility both hurt, so
the allowance is not zero. 5 percent is generous against a section this stiff, and it is kept
because the section is preliminary and week 4 has to size it properly against centrifugal load,
which at this rotor speed is the load that actually matters.

## Radius

Radius is not a free trade of rpm against envelope. Inside a fixed shape family at fixed
thrust, aerodynamic power falls roughly as 1 over radius while rotor torque rises with it, and
every geometry-scaled mass line grows as the square or the cube. So a bigger rotor is a
lower-power rotor with heavier blades and a heavier shaft, and power alone cannot choose it.

| Radius | rpm | Tip speed | Ideal power | Aerodynamic power | Rotor torque | Electrical power | Largest dimension |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 95 mm | 3399 | 33.81 m/s | 261.8 W | 436.3 W | 1.362 Nm | 653.2 W | 251 mm |
| 105 mm | 2782 | 30.59 m/s | 236.8 W | 394.7 W | 1.506 Nm | 591.0 W | 277 mm |
| 115 mm | 2319 | 27.93 m/s | 216.2 W | 360.4 W | 1.649 Nm | 539.6 W | 304 mm |
| 125 mm | 1963 | 25.70 m/s | 198.9 W | 331.6 W | 1.792 Nm | 496.4 W | 330 mm |
| 135 mm | 1683 | 23.79 m/s | 184.2 W | 307.0 W | 1.936 Nm | 459.7 W | 356 mm |

Power times radius is constant across the sweep, which is the 1 over R behaviour the family
predicts, and Reynolds is 141,000 on every row because it depends on thrust and not on size.

Two things bound the radius from opposite sides. Below about 95 mm the aerodynamic power route
and the published power loading route stop agreeing within 35 percent, and the electrical power
walks past the top of the drive shortlist. Above about 125 mm the blade and frame mass growth
overtakes what the lower power saves on the motor. The best conservative thrust to weight lands
at 115 mm, with 125 mm second at 2.297 and worth carrying forward as insurance.

**Second candidate: 125 mm.** It costs 0.09 of conservative thrust to weight and buys 43 W less
electrical power, 356 rpm less speed, and a motor running at 89 percent of continuous instead
of 92. It is the row to pick if week 3 finds the linkage cannot be packaged at 115 mm, and it
is not free, because link lengths, offset geometry and gearing all move with radius and
switching after week 3 still costs a week 3 rerun.

## Mass envelope

Coarse, component level, and every line is a build-up rather than a percentage. Each carries
its scaling class, which is D15: the drive is not a fixed mass.

| Line | Class | Nominal | Conservative | Basis in one phrase |
| --- | --- | --- | --- | --- |
| blades | geometry | 97.0 g | 111.5 g | foam, skin, spar, bond, times 3 |
| rotor frame and hubs | geometry | 50.5 g | 60.6 g | six spider arms, two hub bosses, six brackets |
| pitch mechanism | geometry | 43.5 g | 52.2 g | pitch bearings, links, offset ring and pivots |
| main shaft and bearings | power | 78.7 g | 90.5 g | CFRP through shaft, stubs, two main bearings, torque allowance |
| frame and mounting hardware | geometry | 79.5 g | 99.4 g | two bearing blocks, four frame tubes, motor mount, four lugs |
| motor | power | 118.0 g | 135.7 g | MN3510 KV700, catalogue mass with leads |
| transmission | power | 55.3 g | 66.3 g | belt stage, pulleys following torque |
| esc | power | 20.0 g | 23.0 g | controller above 25 A continuous |
| vectoring actuator | fixed | 25.0 g | 28.8 g | two servos of the 12.5 g class |
| actuator controller and wiring | fixed | 25.0 g | 30.0 g | offset controller board and module wiring |
| fasteners and bonded joints | fixed | 22.0 g | 27.5 g | screws, inserts, standoffs, structural adhesive |
| **total** | | **614.4 g** | **725.4 g** | |

Geometry-scaled lines come to 270 g, power or torque-scaled to 272 g, and genuinely fixed to
72 g. The conservative column is 18.1 percent heavier than nominal, built line by line: 15
percent on catalogue parts whose mass is known, 20 to 25 percent on structure computed from
assumed sections.

D11 set a threshold worth testing early, that the non-blade hardware has to come in under
roughly 40 percent of the mass ceiling or the target is not reachable at that radius. Non-blade
power-scaled and fixed hardware is 344 g against a nominal ceiling of 815 g at 20 N, so 42
percent. Marginally over, and the sweep says the same thing from the other direction.

## The verdict, and it is not a freeze

Conservative thrust is 17.00 N and conservative mass is 725.4 g, giving a thrust to weight of
**2.389**. The hard limit is above 2.5 and the internal target from D17 is 2.75.

- to reach 2.5 the conservative column has to lose 32 g, which is 4.4 percent
- to reach 2.75 it has to lose 95 g, which is 13.1 percent

Nominal thrust to weight is 3.318, which is already 56 percent above the best published module
on the same boundary. Reaching 2.75 conservative needs a nominal of 3.82, and that is 79 percent
above the published record. Nothing available supports it.

So geometry does not freeze. The fallbacks and what happens next are in
`stage-1/progress/week-2.md`.

## Numbers used

- geometry.radius_m = 0.115
- geometry.chord_m = 0.0759
- geometry.span_m = 0.3036
- performance.blade_area_coeff = 0.6055
- performance.blade_area_coeff_low = 0.5147
- performance.blade_deflection_thrust_loss = 0.05
- performance.solidity = 0.3151
- performance.blade_tip_deflection_mm = 0.0863
- performance.blade_twist_deg = 0.0544
- performance.thrust_N_conservative = 17.0
- results.mass_envelope_g = 614.4
- results.mass_g_conservative = 725.42
- results.thrust_to_weight_conservative = 2.3889
