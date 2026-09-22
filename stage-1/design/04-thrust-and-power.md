# Thrust and power

Required Stage 1 item 4. Thrust from the coefficient route, power closed three ways, the
azimuthal load distribution, the named drive on its continuous rating, and what changing the
design thrust costs.

## Thrust

Design thrust is 17.0 N. The requirement is at or above 10 N, and D6 made design thrust a free
variable above that because the two targets together set a mass ceiling that moves with thrust.
Choosing 17 N is not ambition, it is arithmetic in two steps.

First, a floor. The conservative case has to clear 10 N on its own, and since D35 it uses a
coefficient 5 percent below nominal, so the nominal point cannot sit below 10.53 N. Second, a
trade. The geometry-scaled mass lines do not care what thrust the rotor is turning for, so
extra thrust buys mass ceiling while only the drive grows. That trade runs out at 17 N here,
not because of the physics but because of the drive, and the sensitivity table below shows
exactly where. It used to run out at 18 N. D67 corrected the figure of merit, which raised the
power at every thrust, and 18 N now asks 526 W of motor input against the 520 W the selected
motor carries continuously.

Thrust comes from the blade-area coefficient route:

    T = Ct x 0.5 x rho x u^2 x N x c x s

At 2337 rpm and 110 mm radius the tip speed is 26.92 m/s, blade area is 0.0632 m2, and a
coefficient of 0.6055 gives 17.0 N. Chord Reynolds is 130,300.

The conservative case uses 0.5752, the same geometry at 95 percent of the coefficient, giving
16.15 N. Both clear the 10 N requirement on their own.

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
Induced velocity is 10.42 m/s against a tip speed of 26.92, so the inflow ratio is 0.387. That
is large, and it is the single biggest reason a simple model should not be trusted for
magnitude here.

Angle of attack at each azimuth is the geometric pitch less the inflow angle, capped at 28
degrees to stand in for dynamic stall delay. Lift uses a thin-airfoil slope. The distribution
is then scaled so its cycle mean equals the thrust per blade from the coefficient route, which
is the point of it: a load distribution and a sanity check, not an independent thrust estimate.
`tools/linkage.py` is what evaluates it, and running that script with no arguments reproduces
the week 2 sinusoid table to 5.2e-5 N on every row before it moves on to the solved schedule.

Azimuth is measured from the offset link, so 90 degrees is where the pitch mechanism is
commanded to point. Module vertical sits 9.08 degrees past that, and the two force columns are
resolved in module axes.

| Azimuth | Vertical force per blade | Lateral force per blade |
| --- | --- | --- |
| 0 deg | 0.64 N | 3.99 N |
| 30 deg | 2.50 N | -6.54 N |
| 60 deg | 11.51 N | -9.35 N |
| 90 deg | 13.73 N | -2.19 N |
| 120 deg | 6.25 N | 2.39 N |
| 150 deg | 0.83 N | 1.02 N |
| 180 deg | 0.00 N | -0.03 N |
| 210 deg | 0.12 N | -0.31 N |
| 240 deg | 2.40 N | -1.95 N |
| 270 deg | 9.27 N | -1.48 N |
| 300 deg | 13.08 N | 5.00 N |
| 330 deg | 7.68 N | 9.45 N |

The lower half no longer mirrors the upper one. That mirroring was a property of the prescribed
sinusoid, not of the rotor, and the solved schedule has enough harmonic content to break it.
Peak vertical force is 14.43 N at 80 degrees against a cycle mean of 5.67 N, so peak to mean is
2.55.

That is still below the published 3 to 4 range, and the honest reading is that the model
under-predicts the peak rather than that this design is gentler than the literature. A
quasi-steady model with uniform inflow has no wake return, no shed vorticity and no dynamic
stall overshoot, and all three sharpen the peak. Week 4 uses 4.0 regardless, which is D16.

What sets what, since the plan asks: vertical force is set by pitch amplitude and inflow ratio
together. Side force is set by the phase between the pitch schedule and the azimuth, and it was
zero by construction while the schedule was a phase-free sinusoid. It is not zero now. The
cycle mean lateral force is trimmed to zero by pointing the offset 9.08 degrees off the module
vertical, and the instantaneous lateral force still reaches 9.83 N per blade inside the cycle,
which is a bearing and frame load rather than a thrust loss. Peak blade load is set by the
stall cap more than by anything else, which is exactly why the number is soft.
`03-pitch-and-vectoring.md` carries the schedule, the trim and what the measured literature
says about both.

## Power

Three levels, in the order the plan gives them.

**Level 1, the momentum floor.** Over the projected frontal area of 2R times span, which is
0.0639 m2 and is the cap the gate applies, ideal induced power for 17 N is 177.2 W. No rotor
beats this. It is a bound, not an estimate, because it is the same equation the induced velocity
came from.

**Level 2, figure of merit, and this is where D67 found an error the design carried for weeks.**
Kellen reports 0.6 at UAV scale for this shape family. That 0.6 belongs with the thrust
coefficient he measured alongside it, 0.6648, and this design carries 0.6055 instead as
deliberate margin. Figure of merit is thrust coefficient to the power one and a half, over root
two times the power coefficient. So cutting the thrust coefficient while holding Kellen's power
coefficient is not conservative, it is inconsistent: it spends the same caution twice, once as
caution on thrust and once as optimism on power. On the consistent reading the figure of merit
scales by the coefficient ratio to the power of one and a half, 0.6 times 0.9108 to the 1.5,
which is **0.5215**. So 177.2 over 0.5215 gives 339.7 W of blade aerodynamic power, against the
321.7 W this document used to report at a higher thrust. The thesis body is still unread, so the
figure of merit is summary class in the evidence ledger and every number downstream inherits it.

**Level 3, the independent cross-check.** Benedict's twin rotor at its operating point gives
0.062 N per watt of blade aerodynamic power, putting 17 N at 274.2 W. The two routes are 19.3
percent apart, inside the 35 percent the gate allows, and the figure of merit route is the more
pessimistic of the two. The gap widened when the figure of merit was corrected, which is the
expected direction: the published route is set by thrust alone and does not know the design got
less efficient. This is the only genuinely independent closure in the chain, since the momentum
floor and the figure of merit are the same equation twice.

The full module power chain:

| Term | Value | Where it comes from |
| --- | --- | --- |
| blade aerodynamic power | 339.7 W | ideal power over a figure of merit of 0.5215 |
| rotor tare | 37.7 W | 10 percent of shaft power, Benedict's flight-weight rotor |
| rotor shaft power | 377.4 W | the two above |
| rotor torque | 1.542 Nm | shaft power over rotor speed |
| motor input power | 483.2 W | shaft power over 0.93 belt and 0.84 motor |
| electrical power at the ESC input | 508.6 W | motor input over 0.95 |
| actuator draw | 6.0 W | two servos holding against residual link load |
| controller draw | 2.0 W | offset controller board |
| regulator conversion loss | 1.4118 W | board and servo rail through a 0.85 step down |
| module electrical power | 518.0 W | the last four above |

Tare sits at the rotor shaft, before the transmission, which is why it is added to aerodynamic
power and not to electrical power. Actuator and controller draw sit outside the drive chain
entirely and are added last. The three efficiencies are assumed, not measured, and they are the
only unevidenced links in the chain. The motor figure is the sensitive one: at 0.78 instead of
0.84 the motor input rises to 520 W, which is exactly the continuous rating and leaves nothing.

### The drive, on a derated continuous rating

T-Motor publishes "Max. Power (180s)" and "Peak Current (180s)". That is a three minute
maximum, not an indefinite hover rating, and a hovering module runs longer than three minutes.
Week 2 therefore derates both by 0.80 for continuous duty. Nothing justifies 0.80 rather than
0.70 or 0.90 except ordinary practice, and the problem statement states no endurance
requirement to size it against. The derate is an assumption and it is marked as one.

Continuous torque follows from 9.5493 over KV at the derated current.

| Motor | Mass | 180 s max | Continuous after derate | Continuous torque | Verdict |
| --- | --- | --- | --- | --- | --- |
| MN2806 KV650 | 46 g | 187 W | 149.6 W | 0.145 Nm | far short of 483.2 W |
| MN4006 KV380 | 57 g | 380 W | 304.0 W | 0.352 Nm | short, and the lightest thing that holds the 13 N row |
| MN3110 KV470 | 98 g | 330 W | 264.0 W | 0.244 Nm | dominated by the MN4006, which is lighter and stronger |
| MN5006 KV450 | 106 g | 650 W | 520.0 W | 0.441 Nm | **selected** |
| MN3510 KV700 | 118 g | 555 W | 444.0 W | 0.273 Nm | short of 483.2 W and 12 g heavier than the one that is not |

A drive is only accepted if four things hold at once, not one. Power: the motor input of 483.2
W is 93 percent of the MN5006's 520 W continuous, and that is the tight one. Torque: at 4.25 to
1 through a 93 percent belt the motor sees 0.3902 Nm, which is 88 percent of its 0.4414 Nm
continuous. Current: 19.29 A of the 20.8 A the derate allows, so 93 percent, and it is derived
from the torque through Kt = 9.5493 over KV plus the 0.9 A idle draw. It used to be input power
over pack voltage, which is the draw of an ideal resistor and runs low by roughly the
efficiency. Speed: the rotor turns 2337 rpm so the motor turns 9932, and an 8S pack driving a
KV450 against 60 mOhm at the working current can reach 12799, so the motor sits at 78 percent
of available with throttle headroom left.

**The pack interface moved from 6S to 8S, and that is the change that made this close.** The
battery sits outside the module boundary, so pack voltage is an interface the module declares
rather than a part it carries. It has to be declared because of an identity worth stating
plainly: a motor held to a speed rule s and a continuous current Ic can deliver at most s times
the loaded pack voltage times Ic of mechanical output, and KV cancels out of that product
exactly, because 2 pi over 60 times 9.5493 is 1. Gearing slides the operating point along that
line and cannot move the line. At 6S the MN5006 caps at 392 W of mechanical output and the
corrected rotor asks 406 W, so no belt ratio and no KV was ever going to fix it. At 8S the cap
is 532 W. See D67.

**8S is a pack the ESC sees and the motor does not.** The datasheet lists the MN5006 as a 4 to
6S motor, so declaring an 8S pack over it reads like running a part out of range, and it reads
that way right up to the point where the terminal voltage is worked out instead of assumed. An
ESC is a buck converter. What the windings see is the back EMF plus the resistive drop, and at
9932 rpm on a KV of 450 with 19.29 A through 60 mOhm that is **23.2293 V**. Six cells off the
charger are 25.2 V, so at the design point the motor sits inside its own catalogue window and it
is the pack outside it, not the machine. The pack has to be 8S because of sag rather than
appetite: under this current a 6S pack holds less than the windings are asking for, and gearing
slides along the line without moving it. What actually meets 33.6 V is the ESC, the harness and
the pitch offset controller, each rated or regulated for it on its own terms.

Two things that does not settle, and both are written down rather than argued away. The 650 W
and 26 A ratings were published against a test the manufacturer ran on 6S, so a written
confirmation at this duty is a Stage 2 action rather than a closed one. And ESC switching
losses rise with the higher rail, which the 0.95 efficiency in the chain above does not
separately account for. See D70.

4.25 to 1 is the smallest whole tooth ratio that leaves 6 percent on every line at this radius,
which is what picked 68 teeth against the 16 tooth motor pulley.

Two caveats. The MN5006 figures were read off the manufacturer's datasheet PDF; the other four
came from supplier listings and week 4 confirms them. And a 4.25 to 1 belt means a rotor pulley
of 64.9 mm pitch diameter on HTD-3M, which packages easily inside a 220 mm rotor.

### What the derate is worth

The 0.80 is the softest number in this document. T-Motor publishes Max Power and Peak Current
for 180 seconds, week 2 multiplied both by 0.80 to get something continuous, and nothing
outside the project sets that factor. The problem statement asks for no endurance at all, so
there is no duty to size it against. It cannot be given a source from in here. What it can be
given is a bound on what it costs, and that bound is now computed and gated rather than argued.

Start with what the design actually draws. Motor input is 0.7433 of the published 180 second
power and 0.7418 of the published 180 second current. Power is the tighter of the two now, and
0.7433 is the more useful number than it first looks, because it is also the derate at which
the selection breaks even. Above it the MN5006 covers the design point and below it the motor
does not. The declared 0.80 sits over that line with 5.7 points to spare.

That margin was 0.7 points before D67 and it widened for a reason that has nothing to do with
the derate: the design point came down to 17 N. So a true continuous derate of 0.75 no longer
breaks the selection. 650 W times 0.75 is 487.5 W against the 483.2 W the design draws, and 26 A
times 0.75 is 19.5 A against 19.29 A. Both still hold, narrowly.

Below 0.7433 neither exit is open, and that has not changed. Backing the design point down a
row does not work: the stacked case needs 20.0272 N of design thrust to hold 2.5 and no row of
the sensitivity table comes near it from below. A larger motor does not work either, because
motor mass is a power class item and the conservative column is already 117.3 g over the 2.5
ceiling rather than under it.

That sounds worse than it is, and the reason is the duty. 0.7433 is the fraction of a 180
second rating, so for any demonstration that fits inside three minutes the datasheet figure is
the one that applies and there is a quarter of it spare. The 0.80 continuous rule is a
conservatism we imposed on ourselves for indefinite running that nothing asks for. It stays,
because a rotor module that can only hold thrust for three minutes is a poor answer to a hover
requirement, but it is not the case that decides whether the module works.

What closes it is measurement, and it is cheap: a dynamometer run on the actual motor at the
actual current, early enough in Stage 2 that a drive change is still affordable. That is the
first drive gate in the Stage 2 plan.

One older rule moved into the data at the same time. Belt ratios were screened in week 2 on
motor speed staying under 90 percent of what the pack can turn the motor at, allowing for the
resistive drop. It lived in prose. The pack sits at 29.6 V nominal and 28.4427 V loaded, the
ceiling is 12799.2 rpm, the design is at 0.776 of it, and the gate now refuses both a rule
looser than 0.9 and a ceiling that KV and the loaded voltage do not give.

Speed is no longer what empties the 100 mm radius row. On 8S there is speed to spare at every
radius in the sweep, and what stops 100 mm is power: 531.5 W of motor input against 520 W
continuous. The screening rule stays because it is still a real limit, and it stopped being the
binding one.

## Sensitivity

Frozen here so week 4 can pick a row and cannot invent an operating point under deadline. That
is D10. Ideal power on every row is computed over the same projected area, so the table answers
"at this radius, what does changing thrust cost".

| Design thrust | Mass ceiling at T/W 2.5 | Ideal power | rpm | Rotor torque | Drive consequence |
| --- | --- | --- | --- | --- | --- |
| 13 N | 530 g | 118.5 W | 2044 | 1.179 Nm | MN5006 at 4.188 to 1, 15.17 A of 20.8 A, worst line current at 73 percent. The roomiest row |
| 16 N | 652 g | 161.8 W | 2267 | 1.452 Nm | MN5006 at 4.375 to 1, 17.71 A of 20.8 A, worst line current at 85 percent |
| 17 N | 693 g | 177.2 W | 2337 | 1.542 Nm | MN5006 at 4.25 to 1, 19.29 A of 20.8 A, worst line power at 93 percent. The design point |
| 18 N | 733 g | 193.0 W | 2405 | 1.633 Nm | nothing fits. 526 W of motor input against 520 W continuous |
| 20 N | 815 g | 226.1 W | 2535 | 1.815 Nm | nothing fits. 617 W against 520 W |

Ceilings are floors rounded down, because the inequality is strict.

The shape of that table is the whole argument for 17 N, and for stopping there. Between 13 N
and 17 N the ceiling grows 163 g while the drive grows about 30 g, so raising thrust pays and
pays well. At 18 N it stops, and the reason is now simple where it used to be subtle: the motor
input of 526 W is past the 520 W continuous rating, so it is a power limit and nothing about
the ratio can move it. Before the figure of merit was corrected the 18 N row drew 512.6 W and
was limited by torque and speed together. It draws more now, and the limit it hits first is the
one no gearing can slide.

Stacked conservative thrust to weight rises all the way down the radius range and peaks at 100
mm, at 2.1745, where no drive fits. The best row a drive actually covers is 17 N at 110 mm, and
that is the row the design freezes on per D30. The sweep column for it reads **2.1221**, the
same figure the week 4 refined budget gives, because the sweep row at the frozen radius carries
that budget rather than an estimate of its own. Only one of the four cases clears 2.5: 2.5191
at the design point, against 2.3931 and 2.2339 on each downside alone and 2.1221 stacked. That
is the change D67 made and `05-mass-and-tw.md` sets it out row by row, along with the 117.26 g
that would carry the stacked case back over the requirement.
`stage-1/progress/week-2.md` carries the fallbacks that were worked before the freeze, and
`05-mass-and-tw.md` carries the refined budget.

## Numbers used

- performance.thrust_N = 17.0
- performance.thrust_N_conservative = 16.1493
- performance.aero_power_W = 339.699
- performance.ideal_power_W = 177.166
- performance.figure_of_merit = 0.5215
- performance.aero_power_W_published = 274.194
- performance.power_spread = 0.1928
- performance.tare_power_W = 37.744
- performance.electrical_power_W = 508.588
- performance.module_electrical_power_W = 518.0
- performance.momentum_area_m2 = 0.063888
- performance.induced_velocity_ms = 10.4215
- performance.inflow_ratio = 0.3871
- performance.blade_load_peak_to_mean = 2.5458
- pitch.side_force_tilt_deg = 9.078
- pitch.peak_lateral_force_N = 9.8252
- performance.motor_input_W = 483.158
- performance.motor_rpm = 9932.4
- performance.motor_torque_Nm = 0.3902
- performance.motor_input_current_A = 19.2876
- performance.motor_derate = 0.8
- performance.motor_current_frac_180s = 0.7418
- performance.motor_power_frac_180s = 0.7433
- performance.pack_voltage_nominal_V = 29.6
- performance.pack_voltage_charged_V = 33.6
- performance.motor_terminal_voltage_V = 23.2293
- performance.motor_catalogue_ceiling_V = 25.2
- performance.pack_voltage_loaded_V = 28.4427
- performance.motor_speed_ceiling_rpm = 12799.2
- performance.motor_speed_rule = 0.9
- performance.motor_rpm_frac_ceiling = 0.776
- performance.thrust_floor_stacked_N = 20.0272
- operating.tip_speed_ms = 26.9207
- efficiency.motor = 0.84