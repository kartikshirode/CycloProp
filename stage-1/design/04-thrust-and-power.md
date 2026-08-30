# Thrust and power

Required Stage 1 item 4. Thrust from the coefficient route, power closed three ways, the
azimuthal load distribution, and what changing the design thrust costs.

## Thrust

Design thrust is 20.0 N. The requirement is at or above 10 N, and D6 made design thrust a
free variable above that limit because the two targets together set a mass ceiling that moves
with thrust. Choosing 20 N is not an ambition, it is arithmetic: the geometry-scaled mass
lines do not care what thrust the rotor is turning for, so every extra newton buys about 27 g
of ceiling and spends about 11 g of drive. The section on sensitivity below shows where that
trade stops paying, which is around 24 N.

Thrust comes from the blade-area coefficient route:

    T = Ct x 0.5 x rho x u^2 x N x c x s

At 2319 rpm and 115 mm radius the tip speed is 27.93 m/s, blade area is 0.0691 m2, and a
coefficient of 0.6055 gives 20.0 N. Chord Reynolds is 141,000.

The conservative case uses 0.5147, which is the same geometry at 85 percent of the
coefficient, and gives 17.00 N. Both numbers clear the 10 N requirement on their own, and
that is the constraint that pushed the design thrust up in the first place: a 15 percent
coefficient haircut means the nominal point has to sit above 11.8 N before the conservative
point clears 10 N at all.

Where the coefficient comes from, how it was recomputed, and why the low value is a scenario
rather than a bound is all in `evidence-ledger.md` and `02-rotor-sizing.md`. The short
version: it is transferred from a 4-blade NACA 0010 rotor at Reynolds 35,000 onto a 3-blade
NACA 0020 family at 141,000, and the Reynolds half of that transfer is defensible while the
configuration half is not de-risked by anything.

### Azimuthal load distribution

A cycle-averaged coefficient hides what the blade actually sees. The model here uses 36
azimuths, a prescribed sinusoidal pitch of plus or minus 40 degrees, and a uniform induced
inflow taken from momentum theory. Induced velocity is 10.81 m/s against a tip speed of
27.93, so the inflow ratio is 0.387, which is large and is the single biggest reason a
simple model should not be trusted for magnitude here.

Angle of attack at each azimuth is the geometric pitch less the inflow angle, capped at 28
degrees to stand in for dynamic stall delay. Lift uses a thin-airfoil slope. The resulting
distribution is then scaled so its cycle mean equals the thrust per blade from the
coefficient route, which is the point: this is a load distribution and a sanity check, not an
independent thrust measurement.

| Azimuth | Vertical force per blade |
| --- | --- |
| 0 deg | 0.00 N |
| 30 deg | 6.44 N |
| 60 deg | 15.18 N |
| 90 deg | 13.04 N |
| 120 deg | 4.80 N |
| 150 deg | 0.54 N |
| 180 deg | 0.00 N |

The lower half mirrors the upper half, which follows from a symmetric prescribed schedule and
a uniform inflow. Peak is 15.83 N against a cycle mean of 6.67 N, so peak to mean is 2.37.

That is below the published 3 to 4 range, and the honest reading is that the model
under-predicts the peak rather than that the design is gentler than the literature. A
prescribed sinusoid with uniform inflow has no wake return, no shed vorticity and no dynamic
stall overshoot, and all three sharpen the peak. Week 4 uses 4.0 regardless, which is D16, and
week 3 reruns this against the pitch schedule the solved linkage actually produces.

What sets what, since the plan asks: vertical force is set by the pitch amplitude and the
inflow ratio together. Side force is set by the phase between the pitch schedule and the
azimuth, which is zero in this model by construction and will not be zero in week 3. Peak
blade load is set by the stall cap more than by anything else, which is exactly why the number
is soft.

## Power

Three levels, in the order the plan gives them.

**Level 1, the momentum floor.** Over the projected frontal area of 2R times span, which is
0.0698 m2 and is the cap the gate applies, ideal induced power for 20 N is 216.2 W. No rotor
beats this. It is a bound and not an estimate, because it is the same equation the induced
velocity came from.

**Level 2, figure of merit.** Kellen measured 0.6 at UAV scale on this shape family, so
216.2 over 0.6 gives 360.4 W of blade aerodynamic power. That is the working number.

**Level 3, the independent cross-check.** Benedict's twin rotor at its operating point gives
0.062 N per watt of blade aerodynamic power, which puts 20 N at 322.6 W. The two routes are
10.5 percent apart, comfortably inside the 35 percent the gate allows, and the figure of merit
route is the more pessimistic of the two. This is the only genuinely independent closure in
the chain, since the momentum floor and the figure of merit are the same equation twice.

The full module power chain:

| Term | Value | Where it comes from |
| --- | --- | --- |
| blade aerodynamic power | 360.4 W | ideal power over a figure of merit of 0.6 |
| rotor tare | 40.0 W | 10 percent of shaft power, Benedict's flight-weight rotor |
| rotor shaft power | 400.4 W | the two above |
| rotor torque | 1.649 Nm | shaft power over rotor speed |
| electrical power at the ESC input | 539.6 W | shaft power over 0.93 belt, 0.84 motor, 0.95 ESC |
| actuator draw | 6.0 W | two servos holding against residual link load |
| controller draw | 2.0 W | offset controller board |
| module electrical power | 547.6 W | the three above |

Tare sits at the rotor shaft, before the transmission, which is why it is added to aerodynamic
power and not to electrical power. Actuator and controller draw sit outside the drive chain
entirely and are added last.

### The drive, on its continuous rating

| Motor | Continuous power | Continuous torque | Mass | Verdict |
| --- | --- | --- | --- | --- |
| MN2806 KV650 | 187 W | 0.181 Nm | 46 g | short of the 513 W the design point needs |
| MN3110 KV470 | 330 W | 0.299 Nm | 98 g | covers the 13 N row at 4 to 1, not the design point |
| MN3510 KV700 | 555 W | 0.341 Nm | 118 g | selected |

Continuous torque is derived from 9.5493 over KV at the datasheet continuous current, so 25 A
on a KV700 gives 0.341 Nm.

At the design point the motor sees 513 W at its terminals, which is 92 percent of its 555 W
continuous rating. Rotor torque of 1.649 Nm through a 6 to 1 belt at 93 percent gives 0.296 Nm
at the motor, so 21.7 A of the 25 A allowed, and 13,900 rpm. On 6S the back EMF at that current
leaves roughly 14,800 rpm available, so there is throttle margin. Every one of those is a
continuous figure and none is a peak or burst rating.

Two honest caveats. The catalogue figures came from supplier listings this week rather than
from the manufacturer's datasheet PDF, and week 4 has to confirm them. And a 6 to 1 single
stage means a rotor pulley of about 86 mm pitch diameter, which fits inside a 230 mm rotor but
is not a small part.

## Sensitivity

Frozen here so week 4 can pick a row and cannot invent an operating point under deadline.
That is D10. Ideal power on every row is computed over the same projected area, so the table
answers "at this radius, what does changing thrust cost".

| Design thrust | Mass ceiling at T/W 2.5 | Ideal power | rpm | Rotor torque | Drive consequence |
| --- | --- | --- | --- | --- | --- |
| 13 N | 530 g | 113.3 W | 1870 | 1.072 Nm | MN3110 KV470 covers it at 4 to 1 |
| 16 N | 652 g | 154.7 W | 2074 | 1.319 Nm | MN3510 at 5 to 1, 17 A of 25 A |
| 20 N | 815 g | 216.2 W | 2319 | 1.649 Nm | MN3510 at 6 to 1, 22 A of 25 A |
| 24 N | 978 g | 284.3 W | 2541 | 1.979 Nm | past the shortlist, a heavier motor class is needed |

Ceilings are floors rounded down, because the inequality is strict.

The shape of this table is the whole argument for a design thrust of 20 N. Between 13 N and 20
N the ceiling grows 285 g while the drive grows about 75 g, so the trade pays. Above 20 N it
stops: the shortlist runs out at 555 W continuous, the next motor class costs more mass than
the extra ceiling buys back, and rpm and centrifugal load keep climbing. Conservative thrust to
weight measured across the sweep peaks at 20 N and 115 mm, at 2.389.

Which is below 2.5, so nothing here freezes. `stage-1/progress/week-2.md` carries the fallbacks
that were worked and the report.

## Numbers used

- performance.thrust_N = 20.0
- performance.thrust_N_conservative = 17.0
- performance.aero_power_W = 360.409
- performance.ideal_power_W = 216.246
- performance.figure_of_merit = 0.6
- performance.aero_power_W_published = 322.581
- performance.power_spread = 0.105
- performance.tare_power_W = 40.045
- performance.electrical_power_W = 539.595
- performance.module_electrical_power_W = 547.595
- performance.momentum_area_m2 = 0.069828
- performance.induced_velocity_ms = 10.8123
- performance.inflow_ratio = 0.3871
- performance.blade_load_peak_to_mean = 2.374
- operating.tip_speed_ms = 27.9303
- efficiency.motor = 0.84
