# Pitch and thrust vectoring

Required Stage 1 item 3, and the whole of the 15 percent kinematics and vectoring criterion.
Geometry is frozen from week 2 and nothing here moves it: 110 mm radius, 72.6 mm chord, 290.4
mm span, 3 blades, NACA 0020, plus or minus 40 degrees about a 30 percent chord axis at 2405
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
already sits 4.8 g under the ceiling, and there is nothing to take them out of.

The topology is Kellen's, taken off a vehicle he built rather than invented here. His printed
pages 13 and 55 name four fixed lengths. L1 is the rotor radius. L2 is an offset link from the
rotor axis to the offset pivot, and it is the control link: its length sets the pitch amplitude
and its direction sets the phase. L3 is the pitch link. L4 is the horn from the blade pitch
axis to the pitch link pin.

Physically the three pitch links stack on one pin at the offset pivot, 15.4 mm off the rotor
axis. That pin is carried on a short post reaching in from a phasing carrier, which turns about
the rotor axis on its own bearings outboard of the non-drive end plate. Two digital metal gear
servos of the 12.5 g class drive the carrier through sector gears set 180 degrees apart, which
doubles the holding torque and preloads the mesh so backlash does not show up as thrust
direction error. That is the week 2 envelope line for the vectoring actuator, spelled the same
way, at the same 25 g. No line in the mass envelope moved this week.

The offset link length is a shimmed dimension set at build, not an actuator. It sees a 47.5 N
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
reversed. Blade pitch is alpha minus psi minus a construction angle of -110.52 degrees, which
is the fixed angle between the horn and the chord and is chosen so the cycle mean pitch is zero.

| Link | Length | What it is |
| --- | --- | --- |
| L1 rotor arm | 110.0 mm | input crank, frozen by the week 2 radius |
| L2 offset link | 15.4 mm | ground link, solved for the pitch amplitude |
| L3 pitch link | 105.0 mm | output crank |
| L4 pitch horn | 24.4 mm | coupler |

The horn is Kellen's 2 in on a 9 in radius, scaled. The pitch link is not. His 9.133 in scales
to 111.6 mm here, and the sweep under `--sweep` puts that at 0.3240 Nm of carrier torque against
0.1371 Nm at 105 mm, with a transmission angle 18 degrees tighter and a harmonic residual more
than twice as large. At 111.6 mm the two servos hold the carrier on exactly half their stall
torque, a margin of 1.000, which is not a margin. His rotor ran a different offset regime on a
radius twice this one, so the ratio does not carry across and the sweep is what picked 105 mm.

Only L2 was solved. Bisecting on the peak to peak pitch travel gives 15.40 mm for plus or minus
40 degrees, and the bracket is not arbitrary either: the horn tip circle has to meet the pitch
link circle at every rotor position, which needs `R + e - a <= l <= R - e + a`, so e cannot
exceed 24.4 mm on this link set.

**Grashof.** Sorted, the links are 15.4, 24.4, 105.0 and 110.0 mm. Shortest plus longest is
125.4 mm against 129.4 for the other two, so the criterion holds, and the shortest link is the
ground. That makes it a double crank. The rotor arm turns fully, which it has to, and so does
the pitch link about the offset pivot, one full revolution per rotor revolution.

**Transmission angle**, taken at the horn tip between the horn and the pitch link, because its
sine is the moment arm the pitch link force turns the blade on. It runs 58.58 to 143.23 degrees.
The conventional band is 40 to 140 and the obtuse end sits 3.23 degrees outside it, so say what
that costs instead of quoting the band: the worst sine over the revolution is 0.599, meaning the
mechanism's poorest moment arm is 60 percent of its best. Nothing approaches a singularity. The
nearest approach to a dead centre is 36.8 degrees away.

**Joint travel.** The blade pitch bearing sweeps 80.00 degrees. The pitch link bearing at the
offset pin turns a full revolution each rotor revolution, so it is a continuously rotating joint
and not an oscillating one, which is a different bearing selection and a different life
calculation for week 4.

**Interference, and the one result that set the architecture.** The pitch link passes within
0.004 mm of the rotor axis. That is not a near miss, it is a crossing: at the azimuth where the
horn tip, the rotor axis and the offset pivot line up, the straight line between the two pins
runs through the middle of the rotor. It follows from `l - e` sitting inside the reachable band
`R - a` to `R + a`, so it is a property of this link set and not bad luck. The consequence is
that the plane the pitch links sweep cannot contain the rotor shaft. The shaft therefore stops
inboard of that plane, the rotor is driven from one end, and the offset pivot is fed by a post
from a carrier sitting outboard where nothing rotates with the rotor. Kellen hit the same thing
and solved it by bending L3 around the central hardware.

Clearance to the next blade is not close: the nearest a pitch link comes to a neighbouring pitch
axis is 94.6 mm.

## Pitch schedule

37 rows at 10 degree spacing, closing the revolution. Every one comes from the loop closure
above at the design command, evaluated on a 0.25 degree grid and sampled here.

Azimuth is measured from the offset link, so 90 degrees is the direction the mechanism is
commanded to point. That choice matters for reading the table: it makes the phase delay below a
property of the linkage rather than of the aerodynamics, and it puts module vertical 11.98
degrees further round.

| Azimuth (deg) | Pitch (deg) |
| --- | --- |
| 0 | -8.0504 |
| 10 | -1.9611 |
| 20 | 4.3127 |
| 30 | 10.6654 |
| 40 | 16.9520 |
| 50 | 22.9781 |
| 60 | 28.4987 |
| 70 | 33.2313 |
| 80 | 36.8871 |
| 90 | 39.2288 |
| 100 | 40.1175 |
| 110 | 39.5420 |
| 120 | 37.6076 |
| 130 | 34.4899 |
| 140 | 30.3949 |
| 150 | 25.5209 |
| 160 | 20.0470 |
| 170 | 14.1250 |
| 180 | 7.8888 |
| 190 | 1.4547 |
| 200 | -5.0629 |
| 210 | -11.5502 |
| 220 | -17.8716 |
| 230 | -23.8636 |
| 240 | -29.3066 |
| 250 | -33.9222 |
| 260 | -37.3826 |
| 270 | -39.3987 |
| 280 | -39.8312 |
| 290 | -38.7680 |
| 300 | -36.4514 |
| 310 | -33.1568 |
| 320 | -29.1112 |
| 330 | -24.4797 |
| 340 | -19.3753 |
| 350 | -13.8773 |
| 360 | -8.0504 |

Extrema are 40.12 degrees at 100 and -39.83 at 280, so peak to peak is 79.95 against the 80 the
design asks for. On the finer grid the solved amplitude is 39.998 degrees and the peak sits at
101.0. The revolution closes exactly, -8.0504 at both ends, which it has to for a mechanism and
would not for a fitted curve.

**Phase delay 11.00 degrees.** The pitch peak lags the offset direction by that much. It is not
a free parameter and it is not the aerodynamic tilt further down; it falls out of the four-bar,
because the offset pivot direction and the horn angle each contribute a term and the two are 90
degrees apart in phase.

**Residual against the harmonic it approximates.** Fitting `40*cos(psi - 90 - 11.00)` leaves an
rms of 1.1951 degrees over the 36 distinct azimuths, which is 3.0 percent of amplitude. That is
the number that says a real four-bar is not a cosine. Week 2's load model assumed it was, and
the difference between the two is where the side force comes from.

## Thrust vectoring

The command is the direction of the offset link, and rotating it rotates the pitch schedule
rigidly. Nothing else in the rotor is asymmetric, so the load distribution and the resultant
rotate with it.

**Phase authority is 120 degrees, and it comes from two pitch diameters.** The servo's published
operating travel is 80 degrees, 40 per side. The carrier ring gear is 40 mm and cannot be much
smaller, because it is a ring around the rotor axis that has to clear the offset post at 15.4 mm
radius. The servo sector gear is 60 mm. That is a 1.5 step up, so 80 degrees of servo becomes
120 degrees of carrier, and a bigger step up would need a sector gear bigger than the module can
sensibly carry. This is the whole claim. There is no arrangement of these parts that reaches 360
degrees, and quoting 360 because the offset direction is an angle would be an assertion about a
circle rather than about hardware.

**Holding torque.** The three pitch links load the offset pin, and their moment about the rotor
axis is what the carrier holds. It peaks at 0.1389 Nm and its cycle mean is under 0.001 Nm,
because the once per revolution content cancels across three blades at 120 degree spacing and
what survives is a three per revolution ripple at 120 Hz. Through the 1.5 step up and across two
servos that is 0.0463 Nm each, against half of a 0.216 Nm stall figure, so the margin is 2.33.
Those figures moved by about 1 percent in week 4, when the blade the loads are taken on stopped
being the week 2 estimate and became the drawn section. See D48.

**Travel, slew and draw.** Mechanical stops sit at the ends of the 120 degree carrier range.
End to end takes 0.147 s at the published 0.11 s per 60 degrees, which is a vector command and
not a control loop, so that is fast enough by a wide margin. Two servos at 0.24 A on 6 V draw
2.88 W, inside the 6.0 W week 2 carried for them.

**The controller.** A Matek Systems F411-WSE class board, 8.5 g in a 28 by 28 by 14 mm case,
with four servo outputs and a servo rail selectable to 5 or 6 V at 3.5 A continuous. It takes
the 6S pack directly on a 6 to 30 V input, so the module needs no separate regulator, and 3.5 A
covers two servos drawing 0.24 A each with room over. It is 0.5 g above the 8.0 g week 2
nominal for the pitch offset controller and inside that line's 9.2 g conservative figure, which
is a week 4 line to close rather than a week 3 mass change.

**Command to force.** Five commands across the authority, with vertical and lateral resolved in
module axes and vertical taken along the design resultant.

| Phase command (deg) | Servo angle (deg) | Vertical (N) | Lateral (N) | Resultant (N) | Direction (deg) |
| --- | --- | --- | --- | --- | --- |
| -60 | -40 | 9.000 | -15.588 | 18.000 | -60.0 |
| -30 | -20 | 15.588 | -9.000 | 18.000 | -30.0 |
| +0 | +0 | 18.000 | 0.000 | 18.000 | +0.0 |
| +30 | +20 | 15.588 | 9.000 | 18.000 | +30.0 |
| +60 | +40 | 9.000 | 15.588 | 18.000 | +60.0 |

Direction follows command one to one and magnitude holds at 18.000 N across the range, so
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

The model puts the resultant 11.98 degrees round from the offset direction, in the direction of
rotation. Of that, the pitch peak accounts for 11.00 and the aerodynamics for the remaining
0.98, which is the honest split and the second number is small.

The measured range is not small. Sirohi measured about 10 degrees, Adams 15 to 35 depending on
amplitude and rpm, and Benedict's twin sat at 30 at its operating point, so the band the design
works to is 10 to 35 degrees. Benedict's figure 2.33 is the reason to expect this design high in
that band rather than low. It sweeps 2, 3, 4 and 5 bladed rotors at 35 and 40 degrees of
pitching amplitude from 400 to 2000 rpm, and his text states both trends in words: the tilt
rises with rotational speed, and it rises with blade count. No number is taken off that figure,
because the text extract we hold carries its axis and not its plotted values. This design runs 3
blades at 40 degrees and 2405 rpm, past the top of that speed sweep, on both trends.

So the model under-predicts, and it should. A quasi-steady blade element model with uniform
inflow has no wake return, no shed vorticity and no dynamic stall hysteresis. All three feed the
lateral component, which is why measurement gives 10 to 35 and arithmetic gives 0.98.

**How the design handles it.** The tilt is a bias, not a loss. Benedict measured his by rotating
the whole rotor assembly by the phase angle until the resultant lay on the vertical axis, and
the mechanism here does the same thing by construction: the phasing carrier's zero is indexed at
assembly, so a known bias costs no actuator range at all. The stored 11.98 degrees is what the
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
instantaneous lateral force at up to 10.10 N per blade inside the revolution. It cancels over
the cycle and it does not cancel in the bearings, the offset post or the frame. Week 4 carries
it.

## Open items this hands on

- The blade centre of mass sits at 39.31 percent chord on the week 4 drawn section, aft of the
  30 percent pitch axis. That unbalance roughly doubles the peak blade pitching moment, to
  2.2058 Nm, and puts 105.93 N in the pitch link. Running `--balanced` shows a chordwise balance
  would take those to 1.0904 Nm and 74.62 N. The stored numbers are the unbalanced ones.
  Week 4 priced the balance at 35.5 g across three blades and declined it, because that mass
  takes the stacked conservative case to 2.406 and under the limit, while the pitch link path
  carries the unbalanced load on a margin of 3.30. See D46
- The three per revolution carrier ripple at 120 Hz is above any servo's control bandwidth. The
  torque margin covers it statically. Week 4 bounded the phase jitter it produces by gear
  backlash instead of by the servo, at 0.14 degrees of carrier on 0.05 mm of backlash across the
  40 mm carrier gear, which is inside the 25 degrees of authority the side force uncertainty
  already reserves
- The servo and controller figures are supplier listings rather than manufacturer datasheets,
  the same evidence class as four of the five week 2 drive rows, and they carry the same debt.
  Week 4 grew the controller line to the 8.5 g board rather than looking for a lighter one

## Numbers used

- pitch.offset_m = 0.0154
- pitch.horn_m = 0.0244
- pitch.pitch_link_m = 0.105
- pitch.construction_angle_deg = -110.524
- pitch.phase_delay_deg = 11.0
- pitch.schedule_rms_residual_deg = 1.1951
- pitch.transmission_angle_min_deg = 58.58
- pitch.transmission_angle_max_deg = 143.23
- pitch.axis_keepout_mm = 0.004
- pitch.neighbour_clearance_mm = 94.6
- pitch.pitch_bearing_travel_deg = 80.0
- pitch.phase_authority_deg = 120.0
- pitch.vector_range_deg = 120.0
- pitch.actuator_count = 2
- pitch.actuator_mass_g = 25.0
- pitch.servo_travel_deg = 80.0
- pitch.gear_step_up = 1.5
- pitch.carrier_gear_mm = 40.0
- pitch.servo_gear_mm = 60.0
- pitch.servo_mass_g = 12.5
- pitch.carrier_torque_Nm = 0.1389
- pitch.servo_torque_Nm = 0.0463
- pitch.servo_stall_torque_Nm = 0.216
- pitch.servo_torque_margin = 2.332
- pitch.slew_time_s = 0.1467
- pitch.actuator_draw_W = 2.88
- pitch.carrier_radial_force_N = 53.22
- pitch.side_force_tilt_deg = 11.978
- pitch.peak_lateral_force_N = 10.0987
- pitch.peak_blade_moment_Nm = 2.2058
- pitch.peak_link_force_N = 105.93
- pitch.blade_cg_pct_chord = 39.31
- geometry.pitch_amplitude_deg = 40.0
- geometry.radius_m = 0.11
- performance.thrust_N = 18.0
- performance.actuator_power_W = 6.0
