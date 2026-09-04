# Pitch and thrust vectoring

Required Stage 1 item 3, and the whole of the 15 percent kinematics and vectoring criterion.
Geometry is frozen from week 2 and nothing here moves it: 110 mm radius, 72.6 mm chord, 290.4
mm span, 3 blades, NACA 0020, plus or minus 40 degrees about a 30 percent chord axis at 2337
rpm. What week 3 adds is a linkage that produces that pitch amplitude, the schedule it actually
produces rather than the one week 2 assumed, and what happens to the thrust vector when the
mechanism is commanded.

Everything below comes out of `tools/linkage.py`. Run it with no arguments for the report, with
`--sweep` for the table the link lengths were chosen off, and with `--balanced` for the one
sensitivity case that is not stored. It writes `numbers.json` under `--write`, so the schedule
is reproducible rather than asserted.

## Pitch mechanism

Passive cyclic pitch, one four-bar per blade, and all three sharing a common offset pivot. That
is the architecture week 2 screened in and this week confirms it. The reason is mass: per-blade
actuators would put three servos and three controllers inside a module whose conservative mass
already sits 104.8 g over the 2.5 ceiling since D67, and there is nothing to take them out of.

The topology is Kellen's, taken off a vehicle he built rather than invented here. His printed
pages 13 and 55 name four fixed lengths. L1 is the rotor radius. L2 is an offset link from the
rotor axis to the offset pivot, and it is the control link: its length sets the pitch amplitude
and its direction sets the phase. L3 is the pitch link. L4 is the horn from the blade pitch
axis to the pitch link pin.

Physically the three pitch links stack on one pin at the offset pivot, 11.53 mm off the rotor
axis. That pin is carried on a short post reaching in from a phasing carrier, which turns about
the rotor axis on its own bearings outboard of the non-drive end plate. Two digital metal gear
servos of the 20 g class drive the carrier through sector gears set 180 degrees apart, which
doubles the holding torque and preloads the mesh so backlash does not show up as thrust
direction error. The envelope line for the vectoring actuator is 40 g and it moved in D67: week
3 sized the servo against a holding torque with the gear ratio applied backwards, and the
corrected torque needs a bigger part.

The offset link length is a shimmed dimension set at build, not an actuator. It sees an 80.36 N
peak radial pull from the three pitch links and it is structure, so week 4 sizes it.

## Kinematics

One loop per blade, closing at the offset pivot:

    R*u(psi) + a*u(alpha) + l*u(gamma) = e*u(phi)

with `u(x)` the unit vector at angle x, psi the blade azimuth, alpha the horn direction in the
fixed frame and gamma the pitch link direction. Solving it is a circle intersection. The horn
tip sits at distance a from the pitch axis and at distance l from the offset pivot, so with
D = E - P, d the length of D and delta its direction,

    cos(alpha - delta) = (a^2 + d^2 - l^2) / (2*a*d)

Two roots, and the sign is the assembly mode. The open branch is held for the whole revolution
and the crossed one is its mirror image, which produces the same amplitude with the rotation
reversed. Blade pitch is alpha minus psi minus a construction angle of -102.50 degrees, which
is the fixed angle between the horn and the chord and is chosen so the cycle mean pitch is zero.

| Link | Length | What it is |
| --- | --- | --- |
| L1 rotor arm | 110.0 mm | input crank, frozen by the week 2 radius |
| L2 offset link | 11.53 mm | ground link, solved for the pitch amplitude |
| L3 pitch link | 108.0 mm | output crank |
| L4 pitch horn | 18.0 mm | coupler |

Neither the horn nor the pitch link is scaled from Kellen, and week 3 claimed the horn was.
His 2 in on a 9 in radius scales to 24.4 mm here and the sweep does not pick it. The reason
week 3 landed there is that its sweep printed the minimum transmission angle and ignored the
maximum, and 143.23 degrees is exactly as far from a right angle as 36.77 is. Reading the
angle folded, the sweep picks 18 mm on a 108 mm link, and that row is better on every column
it prints: worst folded angle 44.32 degrees against 36.77, carrier torque 0.1287 Nm against
0.1389, harmonic residual 1.1406 degrees against 1.1951. D67 records the correction.

Only L2 was solved. Bisecting on the peak to peak pitch travel gives 11.53 mm for plus or minus
40 degrees, and the bracket is not arbitrary either: the horn tip circle has to meet the pitch
link circle at every rotor position, which needs `R + e - a <= l <= R - e + a`, so e cannot
exceed 16.0 mm on this link set.

**Grashof.** Sorted, the links are 11.53, 18.0, 108.0 and 110.0 mm. Shortest plus longest is
121.5 mm against 126.0 for the other two, so the criterion holds, and the shortest link is the
ground. That makes it a double crank. The rotor arm turns fully, which it has to, and so does
the pitch link about the offset pivot, one full revolution per rotor revolution.

**Transmission angle**, taken at the horn tip between the horn and the pitch link, because its
sine is the moment arm the pitch link force turns the blade on. It runs 53.88 to 135.68 degrees
and the conventional band is 40 to 140, so both ends are inside it now. Read folded, which is
the reading that matters because an angle and its supplement cost the same moment arm, the
worst is 44.32 degrees. The worst sine over the revolution is 0.699, meaning the mechanism's
poorest moment arm is 70 percent of its best, and the nearest approach to a dead centre is
44.3 degrees away.

**Joint travel.** The blade pitch bearing sweeps 80.00 degrees. The pitch link bearing at the
offset pin turns a full revolution each rotor revolution, so it is a continuously rotating joint
and not an oscillating one, which is a different bearing selection and a different life
calculation for week 4.

**Interference, and the one result that set the architecture.** The pitch link passes within
0.019 mm of the rotor axis. That is not a near miss, it is a crossing: at the azimuth where the
horn tip, the rotor axis and the offset pivot line up, the straight line between the two pins
runs through the middle of the rotor. It follows from `l - e` sitting inside the reachable band
`R - a` to `R + a`, so it is a property of this link set and not bad luck. The consequence is
that the plane the pitch links sweep cannot contain the rotor shaft. The shaft therefore stops
inboard of that plane, the rotor is driven from one end, and the offset pivot is fed by a post
from a carrier sitting outboard where nothing rotates with the rotor. Kellen hit the same thing
and solved it by bending L3 around the central hardware.

Clearance to the next blade is not close: the nearest a pitch link comes to a neighbouring pitch
axis is 98.47 mm.

## Pitch schedule

37 rows at 10 degree spacing, closing the revolution. Every one comes from the loop closure
above at the design command, evaluated on a 0.25 degree grid and sampled here.

Azimuth is measured from the offset link, so 90 degrees is the direction the mechanism is
commanded to point. That choice matters for reading the table: it makes the phase delay below a
property of the linkage rather than of the aerodynamics, and it puts module vertical 9.08
degrees further round.

| Azimuth (deg) | Pitch (deg) |
| --- | --- |
| 0 | -6.4473 |
| 10 | -0.1523 |
| 20 | 6.2841 |
| 30 | 12.7386 |
| 40 | 19.0519 |
| 50 | 25.0196 |
| 60 | 30.3905 |
| 70 | 34.8788 |
| 80 | 38.1988 |
| 90 | 40.1199 |
| 100 | 40.5243 |
| 110 | 39.4333 |
| 120 | 36.9884 |
| 130 | 33.3994 |
| 140 | 28.8936 |
| 150 | 23.6826 |
| 160 | 17.9503 |
| 170 | 11.8517 |
| 180 | 5.5203 |
| 190 | -0.9242 |
| 200 | -7.3660 |
| 210 | -13.6834 |
| 220 | -19.7378 |
| 230 | -25.3623 |
| 240 | -30.3532 |
| 250 | -34.4704 |
| 260 | -37.4624 |
| 270 | -39.1213 |
| 280 | -39.3528 |
| 290 | -38.2089 |
| 300 | -35.8548 |
| 310 | -32.4999 |
| 320 | -28.3419 |
| 330 | -23.5430 |
| 340 | -18.2296 |
| 350 | -12.5020 |
| 360 | -6.4473 |

Extrema are 40.52 degrees at 100 and -39.35 at 280, so peak to peak is 79.88 against the 80 the
design asks for. The revolution closes exactly, -6.4473 at both ends, which it has to for a
mechanism and would not for a fitted curve.

**Phase delay 7.75 degrees.** The pitch peak lags the offset direction by that much. It is not
a free parameter and it is not the aerodynamic tilt further down; it falls out of the four-bar,
because the offset pivot direction and the horn angle each contribute a term and the two are 90
degrees apart in phase. It was 11.00 degrees on the link set week 3 picked, and the corrected
sweep in D67 brought it down.

**Residual against the harmonic it approximates.** Fitting `40*cos(psi - 90 - 7.75)` leaves an
rms of 1.1406 degrees over the 36 distinct azimuths, which is 2.9 percent of amplitude. That is
the number that says a real four-bar is not a cosine. Week 2's load model assumed it was, and
the difference between the two is where the side force comes from.

## Thrust vectoring

The command is the direction of the offset link, and rotating it rotates the pitch schedule
rigidly. Nothing else in the rotor is asymmetric, so the load distribution and the resultant
rotate with it.

**Phase authority is 120 degrees, and it comes from two pitch diameters.** The servo's published
operating travel is 80 degrees, 40 per side. The carrier ring gear is 40 mm and cannot be much
smaller, because it is a ring around the rotor axis that has to clear the offset post at 11.53 mm
radius. The servo sector gear is 60 mm. That is a 1.5 step up, so 80 degrees of servo becomes
120 degrees of carrier, and a bigger step up would need a sector gear bigger than the module can
sensibly carry. This is the whole claim. There is no arrangement of these parts that reaches 360
degrees, and quoting 360 because the offset direction is an angle would be an assertion about a
circle rather than about hardware.

**Holding torque.** The three pitch links load the offset pin, and their moment about the rotor
axis is what the carrier holds. It peaks at 0.1287 Nm and its cycle mean is under 0.001 Nm,
because the once per revolution content cancels across three blades at 120 degree spacing and
what survives is a three per revolution ripple at 117 Hz. The gear pair steps the carrier angle
**up** by 1.5, and angle amplification at the output is torque multiplication at the input, so
across two servos each one holds 0.0965 Nm. Week 3 divided by the ratio instead of multiplying
and got 0.0463 Nm, which is what let a 12.5 g servo look adequate. Against half of a 0.3825 Nm
stall figure, which is a 20 g class part at 3.9 kgf.cm, the margin is 1.98. D67 records the
correction and D48 the smaller week 4 move that preceded it.

**Travel, slew and draw.** Mechanical stops sit at the ends of the 120 degree carrier range.
End to end takes 0.173 s at the published 0.13 s per 60 degrees, which is a vector command and
not a control loop, so that is fast enough by a wide margin. Two servos at 0.35 A on 6 V draw
4.2 W, inside the 6.0 W week 2 carried for them.

**The controller, and the regulator D70 put in front of it.** A Matek Systems F411-WSE class
board, 8.5 g in a 28 by 28 by 14 mm case, with four servo outputs and a servo rail selectable to
5 or 6 V at 3.5 A continuous. 3.5 A covers two servos drawing 0.35 A each with room over.

Its input range is 6 to 30 V and that does not cover the pack. This document used to say the
board takes the pack directly and the module needs no separate regulator. On 6S that was true.
D67 moved the declared pack interface to 8S, which is 29.6 V nominal and **33.6 V on a full
charge**, so the board would sit 3.6 V over its rating at the top of every flight. That was
carried as an open item for three days with no part behind it, which is how the 4 September
audit found it.

What closes it is a switching regulator between the pack and the board, rated at least 42 V in
against the 33.6 V it will actually see, putting out 12 V at 1 A, which lands in the middle of
the board's window rather than at an edge of it. It costs 10.0 g nominal and 12.5 g
conservative, and it carries the servo rail behind the board as well, so its conversion loss of
1.4118 W is a module electrical draw rather than a rounding error. No supplier listing has been
read for a specific part, so the line is a requirement and a mass allowance and the growth class
says so. Stage 2 item 5 turns it into a part number.

**Command to force.** Five commands across the authority, with vertical and lateral resolved in
module axes and vertical taken along the design resultant.

| Phase command (deg) | Servo angle (deg) | Vertical (N) | Lateral (N) | Resultant (N) | Direction (deg) |
| --- | --- | --- | --- | --- | --- |
| -60 | -40 | 8.500 | -14.722 | 17.000 | -60.0 |
| -30 | -20 | 14.722 | -8.500 | 17.000 | -30.0 |
| +0 | +0 | 17.000 | 0.000 | 17.000 | +0.0 |
| +30 | +20 | 14.722 | 8.500 | 17.000 | +30.0 |
| +60 | +40 | 8.500 | 14.722 | 17.000 | +60.0 |

Direction follows command one to one and magnitude holds at 17.000 N across the range, so
`pitch.vector_range_deg` is set equal to the phase authority. Be clear about why that came out
so clean. The rotor is axisymmetric, the three blades are evenly spaced, and the inflow in this
model is a uniform vector that settles onto whatever direction the resultant points. Rotate the
command and the entire solution rotates with it, exactly. The table is therefore a statement
about the model's symmetry, and the mechanism's ability to reach those commands, and it is not a
measurement of force magnitude at any of them. What would break the one to one relation in
hardware is everything the model leaves out: wake skew, the frame and shaft supports sitting in
the flow on one side, and the blade passing through its own returning wake. Those also move the
magnitude, and none of them is symmetric.

## Side force

The model puts the resultant 9.08 degrees round from the offset direction, in the direction of
rotation. Of that, the pitch peak accounts for 7.75 and the aerodynamics for the remaining
1.33, which is the honest split and the second number is small.

The measured range is not small. Sirohi measured about 10 degrees, Adams 15 to 35 depending on
amplitude and rpm, and Benedict's twin sat at 30 at its operating point, so the band the design
works to is 10 to 35 degrees. Benedict's figure 2.33 is the reason to expect this design high in <!-- allow: 2.33 is a figure number in Benedict 2010, not the retired servo margin -->
that band rather than low. It sweeps 2, 3, 4 and 5 bladed rotors at 35 and 40 degrees of
pitching amplitude from 400 to 2000 rpm, and his text states both trends in words: the tilt
rises with rotational speed, and it rises with blade count. No number is taken off that figure,
because the text extract we hold carries its axis and not its plotted values. This design runs 3
blades at 40 degrees and 2337 rpm, past the top of that speed sweep, on both trends.

So the model under-predicts, and it should. A quasi-steady blade element model with uniform
inflow has no wake return, no shed vorticity and no dynamic stall hysteresis. All three feed the
lateral component, which is why measurement gives 10 to 35 and arithmetic gives 1.33.

**How the design handles it.** The tilt is a bias, not a loss. Benedict measured his by rotating
the whole rotor assembly by the phase angle until the resultant lay on the vertical axis, and
the mechanism here does the same thing by construction: the phasing carrier's zero is indexed at
assembly, so a known bias costs no actuator range at all. The stored 9.08 degrees is what the
model gives and it is the value the design carries into week 4, marked as a lower bound rather
than a prediction.

**What the uncertainty costs, which is the part worth arguing about.** Index the carrier at the
centre of the 10 to 35 band and the residual after trim is up to 12.5 degrees either way. The
actuator has to absorb that, and it comes straight off the symmetric vectoring range: 120
degrees of authority becomes 95 degrees usable, worst case, or plus and minus 47.5 about
vertical instead of plus and minus 60. That is still a usable vectoring module and it is the
single largest consumer of authority in the design. It also means the bench calibration is not
optional. One hover run with a two axis load cell fixes the bias to a degree or two and gives
the range straight back.

**At the ends of the operating range.** The tilt rises with rpm, so trimming at the design point
leaves a residual at any other speed. Benedict's figure spans roughly 20 degrees of phase across
its 400 to 2000 rpm sweep on a 3-bladed rotor, which is the same order as the 12.5 degrees the
band uncertainty already costs. Thrust magnitude on this module is set by rpm, so the two are
coupled and a vectoring command at reduced thrust needs a different trim. That is a calibration
schedule rather than a constant, and writing one measured angle into the design as a universal
correction would be wrong in both directions.

**And the cycle mean is not the whole load.** Trimming the mean lateral force to zero leaves the
instantaneous lateral force at up to 9.83 N per blade inside the revolution. It cancels over
the cycle and it does not cancel in the bearings, the offset post or the frame. Week 4 carries
it.

## Open items this hands on

- The blade centre of mass sits at 39.31 percent chord on the week 4 drawn section, aft of the
  30 percent pitch axis. That unbalance roughly doubles the peak blade pitching moment, to
  2.0967 Nm, and puts 144.19 N in the pitch link. Running `--balanced` shows a chordwise balance
  would take those to 1.0177 Nm and 76.52 N. The stored numbers are the unbalanced ones.
  Week 4 priced the balance at 35.5 g across three blades and declined it, and the reason it
  gave has weakened. That reason was that the mass took the stacked conservative case under
  2.5. The stacked case is under 2.5 anyway since D67, and 35.5 g takes it from 2.1221 to
  2.0292, which still clears the declared floor of 2.0. What still declines the balance is the
  structure: the pitch link path carries the unbalanced load on a margin of 3.29 against a 1.5
  floor, so the mass buys nothing the design needs. See D46 and D67
- The three per revolution carrier ripple at 117 Hz is above any servo's control bandwidth. The
  torque margin covers it statically. Week 4 bounded the phase jitter it produces by gear
  backlash instead of by the servo, at 0.14 degrees of carrier on 0.05 mm of backlash across the
  40 mm carrier gear, which is inside the 25 degrees of authority the side force uncertainty
  already reserves
- The servo and controller figures are supplier listings rather than manufacturer datasheets,
  the same evidence class as four of the five week 2 drive rows, and they carry the same debt.
  Week 4 grew the controller line to the 8.5 g board rather than looking for a lighter one

## Numbers used

- pitch.offset_m = 0.01153
- pitch.horn_m = 0.018
- pitch.pitch_link_m = 0.108
- pitch.construction_angle_deg = -102.496
- pitch.phase_delay_deg = 7.75
- pitch.schedule_rms_residual_deg = 1.1406
- pitch.transmission_angle_min_deg = 53.88
- pitch.transmission_angle_max_deg = 135.68
- pitch.axis_keepout_mm = 0.019
- pitch.neighbour_clearance_mm = 98.47
- pitch.pitch_bearing_travel_deg = 80.0
- pitch.phase_authority_deg = 120.0
- pitch.vector_range_deg = 120.0
- pitch.actuator_count = 2
- pitch.actuator_mass_g = 40.0
- pitch.servo_travel_deg = 80.0
- pitch.gear_step_up = 1.5
- pitch.carrier_gear_mm = 40.0
- pitch.servo_gear_mm = 60.0
- pitch.servo_mass_g = 20.0
- pitch.carrier_torque_Nm = 0.1287
- pitch.servo_torque_Nm = 0.0965
- pitch.servo_stall_torque_Nm = 0.3825
- pitch.servo_torque_margin = 1.982
- pitch.slew_time_s = 0.1733
- pitch.actuator_draw_W = 4.2
- pitch.carrier_radial_force_N = 80.36
- pitch.side_force_tilt_deg = 9.078
- pitch.peak_lateral_force_N = 9.8252
- pitch.peak_blade_moment_Nm = 2.0967
- pitch.peak_link_force_N = 144.19
- pitch.blade_cg_pct_chord = 39.31
- geometry.pitch_amplitude_deg = 40.0
- geometry.radius_m = 0.11
- performance.thrust_N = 17.0
- performance.actuator_power_W = 6.0