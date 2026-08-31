# Thrust and power

Required Stage 1 item 4. Thrust from the coefficient route, power closed three ways, the
azimuthal load distribution, the named drive on its continuous rating, and what changing the
design thrust costs.

## Thrust

Design thrust is 18.0 N. The requirement is at or above 10 N, and D6 made design thrust a free
variable above that because the two targets together set a mass ceiling that moves with thrust.
Choosing 18 N is not ambition, it is arithmetic in two steps.

First, a floor. The conservative case has to clear 10 N on its own, and the conservative case
uses a coefficient 15 percent below nominal, so the nominal point cannot sit below 11.8 N.
Second, a trade. The geometry-scaled mass lines do not care what thrust the rotor is turning
for, so extra thrust buys mass ceiling while only the drive grows. That trade runs out at 18 N
here, not because of the physics but because of the drive, and the sensitivity table below
shows exactly where.

Thrust comes from the blade-area coefficient route:

    T = Ct x 0.5 x rho x u^2 x N x c x s

At 2405 rpm and 110 mm radius the tip speed is 27.70 m/s, blade area is 0.0632 m2, and a
coefficient of 0.6055 gives 18.0 N. Chord Reynolds is 134,000.

The conservative case uses 0.5752, the same geometry at 95 percent of the coefficient, giving
17.10 N. Both clear the 10 N requirement on their own.

Where the coefficient comes from, why the low value is a scenario rather than a bound, and what
the two primary sources actually say is in `evidence-ledger.md` and `02-rotor-sizing.md`. The
short version has changed twice over. The nominal is transferred from a 4-blade NACA 0010 rotor
at a chord Reynolds of 31,600, not the 35,000 this document used to quote, and the correct
reading of that rotor gives 0.7211 rather than the 0.6055 stored here. 0.6055 stands as
deliberate margin under D36. The configuration half of the transfer is no longer undefended
either: Kellen measured this shape family at 0.6648, which is what took the haircut from 15
percent to 5 and is recorded as D35.

### Azimuthal load distribution

A cycle-averaged coefficient hides what the blade actually sees. The model uses 36 azimuths, a
uniform induced inflow from momentum theory, and the pitch schedule the week 3 linkage solves.
It used a prescribed sinusoid until week 3 replaced it, and the two are not the same shape.
Induced velocity is 10.72 m/s against a tip speed of 27.70, so the inflow ratio is 0.387. That
is large, and it is the single biggest reason a simple model should not be trusted for
magnitude here.

Angle of attack at each azimuth is the geometric pitch less the inflow angle, capped at 28
degrees to stand in for dynamic stall delay. Lift uses a thin-airfoil slope. The distribution
is then scaled so its cycle mean equals the thrust per blade from the coefficient route, which
is the point of it: a load distribution and a sanity check, not an independent thrust estimate.
`tools/linkage.py` is what evaluates it, and running that script with no arguments reproduces
the week 2 sinusoid table to 5.2e-5 N on every row before it moves on to the solved schedule.

Azimuth is measured from the offset link, so 90 degrees is where the pitch mechanism is
commanded to point. Module vertical sits 11.98 degrees past that, and the two force columns are
resolved in module axes.

| Azimuth | Vertical force per blade | Lateral force per blade |
| --- | --- | --- |
| 0 deg | 1.08 N | 5.08 N |
| 30 deg | 1.91 N | -5.86 N |
| 60 deg | 11.18 N | -10.06 N |
| 90 deg | 14.73 N | -3.13 N |
| 120 deg | 7.45 N | 2.42 N |
| 150 deg | 1.23 N | 1.37 N |
| 180 deg | 0.02 N | 0.12 N |
| 210 deg | 0.06 N | -0.19 N |
| 240 deg | 2.19 N | -1.97 N |
| 270 deg | 9.50 N | -2.02 N |
| 300 deg | 13.92 N | 4.53 N |
| 330 deg | 8.73 N | 9.71 N |

The lower half no longer mirrors the upper one. That mirroring was a property of the prescribed
sinusoid, not of the rotor, and the solved schedule has enough harmonic content to break it.
Peak vertical force is 15.01 N at 80 degrees against a cycle mean of 6.00 N, so peak to mean is
2.50.

That is still below the published 3 to 4 range, and the honest reading is that the model
under-predicts the peak rather than that this design is gentler than the literature. A
quasi-steady model with uniform inflow has no wake return, no shed vorticity and no dynamic
stall overshoot, and all three sharpen the peak. Week 4 uses 4.0 regardless, which is D16.

What sets what, since the plan asks: vertical force is set by pitch amplitude and inflow ratio
together. Side force is set by the phase between the pitch schedule and the azimuth, and it was
zero by construction while the schedule was a phase-free sinusoid. It is not zero now. The
cycle mean lateral force is trimmed to zero by pointing the offset 11.98 degrees off the module
vertical, and the instantaneous lateral force still reaches 10.10 N per blade inside the cycle,
which is a bearing and frame load rather than a thrust loss. Peak blade load is set by the
stall cap more than by anything else, which is exactly why the number is soft.
`03-pitch-and-vectoring.md` carries the schedule, the trim and what the measured literature
says about both.

## Power

Three levels, in the order the plan gives them.

**Level 1, the momentum floor.** Over the projected frontal area of 2R times span, which is
0.0639 m2 and is the cap the gate applies, ideal induced power for 18 N is 193.0 W. No rotor
beats this. It is a bound, not an estimate, because it is the same equation the induced velocity
came from.

**Level 2, figure of merit.** Kellen reports 0.6 at UAV scale for this shape family, so 193.0
over 0.6 gives 321.7 W of blade aerodynamic power. That is the working number, and it is worth
being clear that it is doing a lot of work on the strength of an abstract. The thesis body is
unread, so the figure of merit is summary class in the evidence ledger, and every number
downstream of it inherits that.

**Level 3, the independent cross-check.** Benedict's twin rotor at its operating point gives
0.062 N per watt of blade aerodynamic power, putting 18 N at 290.3 W. The two routes are 9.8
percent apart, inside the 35 percent the gate allows, and the figure of merit route is the more
pessimistic of the two. This is the only genuinely independent closure in the chain, since the
momentum floor and the figure of merit are the same equation twice.

The full module power chain:

| Term | Value | Where it comes from |
| --- | --- | --- |
| blade aerodynamic power | 321.7 W | ideal power over a figure of merit of 0.6 |
| rotor tare | 35.7 W | 10 percent of shaft power, Benedict's flight-weight rotor |
| rotor shaft power | 357.5 W | the two above |
| rotor torque | 1.419 Nm | shaft power over rotor speed |
| motor input power | 457.6 W | shaft power over 0.93 belt and 0.84 motor |
| electrical power at the ESC input | 481.7 W | motor input over 0.95 |
| actuator draw | 6.0 W | two servos holding against residual link load |
| controller draw | 2.0 W | offset controller board |
| module electrical power | 489.7 W | the last three above |

Tare sits at the rotor shaft, before the transmission, which is why it is added to aerodynamic
power and not to electrical power. Actuator and controller draw sit outside the drive chain
entirely and are added last. The three efficiencies are assumed, not measured, and they are the
only unevidenced links in the chain. The motor figure is the sensitive one: at 0.78 instead of
0.84 the motor input rises to 493 W and eats most of the drive margin below.

### The drive, on a derated continuous rating

T-Motor publishes "Max. Power (180s)" and "Peak Current (180s)". That is a three minute
maximum, not an indefinite hover rating, and a hovering module runs longer than three minutes.
Week 2 therefore derates both by 0.80 for continuous duty. Nothing justifies 0.80 rather than
0.70 or 0.90 except ordinary practice, and the problem statement states no endurance
requirement to size it against. The derate is an assumption and it is marked as one.

Continuous torque follows from 9.5493 over KV at the derated current.

| Motor | Mass | 180 s max | Continuous after derate | Continuous torque | Verdict |
| --- | --- | --- | --- | --- | --- |
| MN2806 KV650 | 46 g | 187 W | 149.6 W | 0.145 Nm | far short of 457.6 W |
| MN4006 KV380 | 57 g | 380 W | 304.0 W | 0.352 Nm | short, and the lightest thing that holds the 13 N row |
| MN3110 KV470 | 98 g | 330 W | 264.0 W | 0.244 Nm | dominated by the MN4006, which is lighter and stronger |
| MN5006 KV450 | 106 g | 650 W | 520.0 W | 0.441 Nm | **selected** |
| MN3510 KV700 | 118 g | 555 W | 444.0 W | 0.273 Nm | short of 457.6 W and 12 g heavier than the one that is not |

A drive is only accepted if three things hold at once, not one. Power: the motor input of 457.6
W is 88 percent of the MN5006's 520 W continuous. Torque: at 3.5 to 1 through a 93 percent belt
the motor sees 0.436 Nm, which is 99 percent of its 0.441 Nm continuous, and that is the tight
one. Speed: the rotor turns 2405 rpm so the motor turns 8417, and a 6S pack driving a KV450
against 60 mOhm at the working current can reach 9435, so the motor sits at 89 percent of
available with throttle headroom left. Input current is 20.6 A of the 20.8 A the derate allows.

3.5 to 1 is the only ratio that works at this radius. A lower ratio puts the motor over its
continuous torque and a higher one puts it past the speed a 6S pack can reach. That narrowness
is the reason the radius is where it is.

Two caveats. The MN5006 figures were read off the manufacturer's datasheet PDF; the other four
came from supplier listings and week 4 confirms them. And a 3.5 to 1 belt means a rotor pulley
of roughly 50 mm pitch diameter, which packages easily inside a 220 mm rotor.

## Sensitivity

Frozen here so week 4 can pick a row and cannot invent an operating point under deadline. That
is D10. Ideal power on every row is computed over the same projected area, so the table answers
"at this radius, what does changing thrust cost".

| Design thrust | Mass ceiling at T/W 2.5 | Ideal power | rpm | Rotor torque | Drive consequence |
| --- | --- | --- | --- | --- | --- |
| 13 N | 530 g | 118.5 W | 2044 | 1.024 Nm | MN5006 at 2.5 to 1, 12.65 A of 20.8 A, the roomiest row |
| 16 N | 652 g | 161.8 W | 2267 | 1.261 Nm | MN5006 at 3.5 to 1, 17.27 A of 20.8 A |
| 18 N | 733 g | 193.0 W | 2405 | 1.419 Nm | MN5006 at 3.5 to 1, 20.61 A of 20.8 A. The design point |
| 20 N | 815 g | 226.1 W | 2535 | 1.577 Nm | nothing in the shortlist fits |

Ceilings are floors rounded down, because the inequality is strict.

The shape of that table is the whole argument for 18 N, and for stopping there. Between 13 N
and 18 N the ceiling grows 203 g while the drive grows about 30 g, so raising thrust pays and
pays well. At 20 N it stops, and the reason is worth being precise about: the motor input of
512.6 W is still inside the 520 W continuous rating, so it is not a power limit. It is torque
and speed together. The rotor wants 1.577 Nm, which needs a ratio above 4, and a KV450 on 6S
cannot spin to the motor speed that ratio implies. No other shortlist motor covers it either,
because the ones with the speed do not have the torque.

Stacked conservative thrust to weight rises all the way down the radius range and peaks at 100
mm, at 2.655, where no belt ratio fits. The best row a drive actually covers is 18 N at 110 mm,
and that is the row the design freezes on per D30. The sweep column for it reads 2.517 because
the sweep is built on the week 2 envelope, the one estimate applied to all five radii. On the
week 4 refined budget the same row is 2.5457. All four cases clear 2.5: 3.163 at the design
point, 2.680 and 3.005 on each downside alone, 2.5457 stacked. The stacked row clears by 12.5 g
of conservative mass, so it is a pass without much in hand, and the hard version of that test
ran in week 4 against a budget built from drawn sections and catalogue parts.
`stage-1/progress/week-2.md` carries the fallbacks that were worked before the freeze, and
`05-mass-and-tw.md` carries the refined budget.

## Numbers used

- performance.thrust_N = 18.0
- performance.thrust_N_conservative = 17.0992
- performance.aero_power_W = 321.71
- performance.ideal_power_W = 193.026
- performance.figure_of_merit = 0.6
- performance.aero_power_W_published = 290.323
- performance.power_spread = 0.0976
- performance.tare_power_W = 35.746
- performance.electrical_power_W = 481.655
- performance.module_electrical_power_W = 489.655
- performance.momentum_area_m2 = 0.063888
- performance.induced_velocity_ms = 10.7237
- performance.inflow_ratio = 0.3871
- performance.blade_load_peak_to_mean = 2.501
- pitch.side_force_tilt_deg = 11.978
- pitch.peak_lateral_force_N = 10.0987
- performance.motor_input_W = 457.573
- performance.motor_rpm = 8417.0
- performance.motor_torque_Nm = 0.4361
- performance.motor_input_current_A = 20.611
- operating.tip_speed_ms = 27.7012
- efficiency.motor = 0.84
