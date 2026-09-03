# Structure and loads

This covers the 15 percent structural criterion, which had no section before week 4. Every
demand here is calculated in `tools/structure.py` from the frozen geometry, the frozen speed and
the section drawing, and the gate recomputes five of them. Nothing is asserted next to a
picture.

The headline is that this rotor is a centrifugal machine before it is an aerodynamic one. Each
blade pulls 209.16 N radially at the design point against a peak aerodynamic load of 22.67 N per
blade. Runco measured that ratio at 4.4 on a much smaller rotor; here it is 9.2, because
centrifugal load grows with radius and speed while blade lift does not grow with either in the
same way. So the blade attachment, the blade bending case and the declared overspeed decide the
structure, and the aerodynamic case decides almost nothing.

## Load cases

Two cases, both at sea level and both steady. No gust case, because the problem statement sets
no flight envelope for the module.

**Operating.** 2337.04 rpm, 17.0 N of thrust, 5.67 N of mean vertical force per blade. Peak
blade aerodynamic load is that mean times 4.0, which is the peak to mean factor D16 fixes at the
top of the published 3 to 4 range rather than the bottom, because the range is simulated. The
rerun week 3 model gives 2.546 and is deliberately not used for sizing.

**Overspeed.** 1.20 times design rotor speed, so 2804.4 rpm. Centrifugal load goes as the square
of speed, so this is 301.19 N per blade rather than 209.16, and it is 44 percent worse rather
than 20. The factor covers ESC control overshoot and a transient on a rotor whose speed loop has
no published bandwidth. It is a declared case and not a derived one, and the gate requires it to
be at least 1.10 so a token overspeed cannot satisfy the rule.

Assumptions, stated once. The blade is a uniform beam held at both spiders, so a distributed
load gives a mid span moment of load times span over 8, a lever of 36.30 mm. Air loads are
quasi steady. Bond lines are treated as continuous. Fatigue, flutter and modal response are all
out of scope at Stage 1 and are named at the end.

## Blade

The section is the week 2 build rebuilt with named allowables: Rohacell 51 IG class PMI foam at
52 kg/m3 filling 88 percent of the NACA 0020, two plies of 60 gsm carbon twill at 0.22 kg/m2
cured, a CFRP spar tube of 8.71 mm outer diameter and 0.5 mm wall on the pitch axis, and two
7075-T6 root fittings bonded over the spar. The ordinates are integrated numerically rather than
taken from a shape factor, which is where the week 2 estimate lost 2 percent: the real perimeter
is 2.090 chords, not the 2.05 that was assumed, so the skin is 9.69 g rather than 9.51.

Blade mass is 31.75 g, and 95.24 g for the set.

Bending stiffness about the chord line is 51.12 Nm2, three quarters of it in the skin because
the skin sits at the section extremes and the spar sits near the middle. Torsional stiffness
from the closed cell is 7.81 Nm2. The section's allowable bending moment is 25.25 Nm and it is
set by skin wrinkling over the foam at 215.3 MPa, not by the 400 MPa laminate allowable and not
by the spar, which would take 63.19 Nm on its own.

Three demands sit against that 25.25 Nm.

| Demand | Operating | Overspeed |
| --- | --- | --- |
| aerodynamic bending, 22.67 N over the span | 0.8228 Nm | 1.1848 Nm |
| centrifugal bending, 209.16 N over the span | 7.5925 Nm | 10.9333 Nm |
| both together | 8.4153 Nm | 12.1181 Nm |

The gated `blade_margin` is 30.69 because it compares the section against aerodynamic bending
alone, and that is the small load. The number that matters is the combined one, 3.00 at the
design point and 2.08 at overspeed, and both are gated now.

**Blade torsion is the interesting result.** The blade is driven in pitch from one end, through
a single horn, so the centrifugal pitching moment on an unbalanced blade has to be carried
through the blade's own torsional stiffness. 2.0967 Nm distributed over 290.4 mm of span at
7.81 Nm2 winds the far end up by 2.23 degrees, about 1.5 degrees averaged along the span. That
is under 4 percent of the 40 degree pitch amplitude, and it is most of the 5 percent blade flexibility
loss the low thrust coefficient has been carrying since week 2 as a floor. Week 2 could only
bound that allowance from above. It now has a calculation under it, and driving the blade from
both ends would roughly quarter it, which is a Stage 2 option and not a Stage 1 change.

Deflection under the week 3 peak blade load of 14.43 N is 0.09 mm, 0.12 percent of chord.
Twist under the aerodynamic pitching moment about the 30 percent axis is 0.014 degrees. Neither
is a design driver.

**The attachment used to be the tightest joint in the module and D67 changed that twice over.**
Each blade's 209.16 N goes into the pitch bearings that carry it on the spider arms. Week 4 used
two 693ZZ bearings at a supplier listing of 270 N each, giving 540 N. Neither half of that
survived. The rating is now the ISO 76 basic static figure computed from the bearing's own ball
complement, `12.3 * 7 * 1.5875^2`, which is **216.985 N** and not 270. On that rating one bearing
at each of the blade's two root stations gives a margin of 1.36 at overspeed, under the 1.5
floor, so there are two at each station now. Four bearings at 90 percent sharing, because two
bearings on one pin do not split a radial load perfectly, give 781.15 N. The margin is 3.73 at
the design point and 2.59 at overspeed.

That cost 7.8 g and no redraw, because two 4 mm bearings fit inside the 10 mm root fitting that
was already there. It also moves the tightest margin in the module off this joint and onto the
blade in combined bending at overspeed, at 2.08. The bearings still oscillate through 80 degrees
rather than rotating, which is a fretting duty a static rating does not describe, and that is
worked out below.

## Shaft

A roll wrapped CFRP tube, 16 mm outer diameter and 1.5 mm wall, 340 mm long, with 7075-T6 plugs
bonded into both ends and turned to 15 mm bearing journals. D40 stops it inboard of the pitch
plane, because the pitch links sweep through the rotor axis, so it cannot be run out to an
outboard bearing on the mechanism side. The belt pulley has the other end to itself.

Rotor shaft torque is 1.54226 Nm, which is aerodynamic power plus tare divided by rotor angular
speed. Motor shaft torque is 0.3902 Nm, the same power through the 4.25 to 1 belt and its 0.93
efficiency. Those are different shafts and the document says which is which, because torque
upstream and downstream of a reduction is the number a reviewer checks first.

Torsional allowable is 24.96 Nm at 55 MPa of shear, so the torsional margin is 16.18. That is a
large number and it is honest: the shaft diameter is set by the bearing bore, the pulley
interface and lateral stiffness on a single ended drive, not by torque. The case that gets
closer is bending. The 68 tooth rotor pulley at 64.9 mm pitch diameter takes 47.53 N of
effective belt tension, 66.54 N of shaft side load at an HTD load factor of 1.4, and 30 mm of
overhang from the drive bearing, giving 1.9951 Nm of bending. Combining that with torsion by
maximum shear gives 5.56 MPa against 55, a margin of 9.90. The bigger pulley raised the torque
and lowered the side load at the same time, because the tension is the torque over a longer
radius, so the combined case improved while the torsional one got tighter.

Main bearings are 61802, 15 by 24 by 5 mm, static rating 2320 N each. They carry the rotor
weight, the belt side load and the instantaneous lateral blade force, none of which approaches
that. They are chosen for bore and width rather than for load.

## Pitch load path

Peak pitch link force is 144.19 N, from the four-bar solved against the week 4 blade. The
blade is not chordwise balanced, so this is the unbalanced figure per D43. It rose from 105.93 N
when D67 corrected the linkage, because a shorter horn turns the same blade moment into a bigger
link force.

Three elements are in that path and the weakest one sets the allowable.

| Element | Capacity as an axial link load | Margin |
| --- | --- | --- |
| pitch horn, 7075-T6, 8 by 4 mm at an 18.0 mm radius | 474.1 N | 3.29 |
| M3 aluminium bodied rod end, static | 600 N | 4.16 |
| CFRP link tube, 4 mm by 0.5 mm wall, Euler at 108 mm | 944.9 N | 6.55 |

The horn governs at 474.1 N and the margin is 3.29. The shorter horn raised the link load and
raised the horn's own capacity by more, because capacity goes as one over the radius while the
load goes up with it, so the margin barely moved from the 3.30 week 4 reported.

That margin is the number behind the decision not to balance the blade, and the reason it gives
has changed. A chordwise balance would take the link to 76.52 N and the margin to 6.20, and it
costs 35.5 g across three blades. Week 4 declined it because that mass took the stacked case
under 2.5. The stacked case is under 2.5 anyway since D67, and the 35.5 g leaves it at 2.0610,
still over the declared floor. What declines it now is that 3.29 is already more than twice the
1.5 floor, so the mass buys nothing the design needs. See D46, D53 and D67.

The offset post takes 80.36 N of radial pull from the three links converging on it. As an 8 mm
7075-T6 cantilever reaching 40 mm from the phasing carrier that is 3.21 Nm of bending against
20.1 Nm of capacity, a margin of 6.25. Carrier torque peaks at 0.1287 Nm at three per
revolution, 117 Hz, which is above any servo's control loop. The servos hold it statically on a
margin of 1.98, and the phase jitter it produces is bounded by gear backlash rather than by the servo:
0.05 mm of backlash across the 40 mm carrier gear is 0.143 degrees of carrier, inside the 25
degrees of authority the side force uncertainty already reserves.

## Pitch bearing oscillating duty

The tightest margin in the module is a bearing static rating, and a static rating is the wrong
yardstick for a bearing that never turns. Each blade hangs on two 693ZZ bearings that swing
through 80 degrees once a revolution while the centrifugal pull holds its direction in the
spider arm. There are four per blade since D67, two at each root station. Fixed load, oscillating rings, small amplitude. That is the arrangement false
brinelling is named after, so the duty is worked out here rather than left to the catalogue.

Two numbers decide whether the balls ever roll onto fresh raceway. With the outer ring held
still the cage turns at half of one minus the ball diameter over the pitch diameter, which for
7 balls of 1.5875 mm on a 5.5 mm pitch circle is a little over a third. Eighty degrees of blade
pitch therefore moves the ball set by 28.45 degrees. The balls sit 51.43 degrees apart. The
ratio is 0.5533, and anything under 1.0 means every ball spends the life of the machine inside
its own arc, grease stops being dragged back into the contact, and the bearing wears where it
sits instead of failing in fatigue.

Full recirculation would need 144.6 degrees of pitch travel. No cyclorotor schedule asks for
that and ours gives 80, so the regime is not something a pitch amplitude change can escape. It
has to be carried.

What carries it is load. At 2337.04 rpm each bearing takes 52.29 N, a quarter of the 209.161 N
centrifugal pull, and each is rated at 216.985 N on ISO 76, so the static safety factor at the
operating point is 4.15 against a declared floor of 2.0. It was 2.44 on two bearings at a
supplier listing, and both halves of that moved in D67. The floor is the same class of judgement as the
overspeed factor: a stated rule rather than a measurement, applied because a contact that never
moves has no second chance at a soft spot. It is gated, and the gate also refuses a floor that
a later week lowers.

Worth being plain about which of the two cases is actually binding. At the frozen 1.20
overspeed the 1.5 strength floor already asks more of the rating than the 2.0 wear floor does,
so the strength case still governs today and blade attachment at 2.59 is what sizes the joint,
even though it is no longer the tightest margin in the module. The wear floor starts to bite only if a later week drops the overspeed, which is exactly
the trade it exists to catch.

Friction settles the alternative. Twelve deep groove bearings at a swing rate set by 38.95 Hz
give back 0.154 W, under a tenth of a percent of rotor shaft power, which is why it is not a
line in the power budget. A PTFE fabric lined plain bearing is immune to the wear mode above and
is what an oscillating aerospace joint uses, and the same joints would cost 8.19 W instead. That
is better than fifty times the friction, and the sliding distance at 38.95 Hz is what turns it
around: a plain bearing that would be untroubled at ten swings a minute is running 162 mm of
liner past the shaft every second here.

So the ball bearing stays, on a static safety factor of 4.15 and an anti fretting grease behind
the shields. The answer to the old margin of 2.44 was to duplex the bearing rather than to find
a bigger one the project has no data for, which is the same fix in a cheaper form: two 4 mm
bearings fit inside the root fitting that was already drawn. If a Stage 2 bench run shows
fretting anyway, a larger bearing is still the next move.

## Frame and mount load path

Blade, spider arm, hub boss, shaft, main bearing, bearing block, frame tube, mount lug. The
reaction torque of 1.54226 Nm about the rotor axis reaches the airframe through both bearing
blocks and the four frame tubes, which is why the blocks sit on the tubes rather than on side
plates.

The lug pattern is 320 mm along the rotor axis by 240 mm across it, inside the 364.4 by 316.5 mm
packaged envelope. Thrust is 17.0 N and it swings across 120 degrees, so the worst single lug
sees roughly half the thrust rather than a quarter. Add its share of the 6.6503 N module weight
and the torque couple across the 240 mm transverse spacing, and the worst lug carries about 13.4
N. A 7075-T6 lug of 8 by 3 mm section with an M3 hole has 5.8 kN of net section capacity, so the
mount is not strength driven either. What it is driven by is the stiffness of an airframe
interface nobody has specified, and that stays open.

## Margins

All at a floor of 1.5. Seven of the eight are recomputed by the gate from the
allowable and the demand stored beside them. The eighth, the shaft's combined case, is
computed in `tools/structure.py` and floored by the gate but not recomputed by it, because it
needs the shaft section properties and those live in the script rather than in
`numbers.json`.

| Case | Demand | Allowable | Margin |
| --- | --- | --- | --- |
| blade bending, aerodynamic only | 0.8228 Nm | 25.25 Nm | 30.69 |
| blade bending, aerodynamic and centrifugal | 8.4153 Nm | 25.25 Nm | 3.00 |
| blade bending at 1.20 overspeed | 12.1181 Nm | 25.25 Nm | 2.08 |
| rotor shaft torsion | 1.54226 Nm | 24.96 Nm | 16.18 |
| rotor shaft, bending and torsion combined | 5.56 MPa | 55 MPa | 9.90 |
| pitch link path, horn governs | 144.19 N | 474.1 N | 3.29 |
| blade attachment, centrifugal | 209.16 N | 781.1 N | 3.73 |
| blade attachment at 1.20 overspeed | 301.19 N | 781.1 N | 2.59 |

The spread is the point, and it reads differently since D67. Two margins sit under 3 and both of
them are the overspeed cases, which says the declared 1.20 overspeed is what sizes this module
rather than any operating load. Everything at the design point is over 3. The blade in combined
bending at overspeed is the tightest at 2.08, and it took that place from the blade attachment,
which was 1.69 on a supplier listing and is 2.59 on a computed rating with twice the bearings.
So the effort in Stage 2 goes to the blade section first and the attachment second, and the
shaft and the frame are not close.

## What the blade allowable actually turns on

Two of the eight margins sit under 2 and both of them are the blade, so it is worth knowing
which material property they rest on. The answer is not the one this project assumed for four
weeks.

Skin wrinkling over the foam sets the section, at 0.5 times the cube root of the skin modulus,
the foam modulus and the foam shear modulus. That comes out at 215.2638 MPa, well under the 400
MPa the laminate itself would take, and the allowable moment is that stress times EI over the
skin modulus and the distance to the extreme fibre. Skin governs at 25.2528 Nm against 63.1857
Nm for the spar, so the spar is not close.

Now drop the skin modulus. The wrinkling stress falls as its cube root. EI over the skin modulus
rises, because the spar term and the foam term stay exactly where they are and only their share
of the total grows. The two nearly cancel. Swept from 0.5 of the published class value to all of
it, the worst overspeed margin found anywhere in the band is 2.0739, against 2.0839 at the
published value. Under 1 percent across a 2 to 1 range, and the worst point sits in the middle of
the band rather than at the bottom of it.

The foam is the sensitive input, because both of its moduli sit inside the same cube root. Knock
them down together and the allowable moves as the two thirds power. The overspeed margin reaches
1.5 at 0.6144 of the published foam properties, so nearly 40 percent off the delivered foam is
what it takes.

The realistic version of that is a grade substitution rather than a shortfall, and it is gentler
than the sweep suggests. On Rohacell 31 IG instead of 51 IG the blade weighs 28.057 g rather than
31.75, so the centrifugal demand falls along with the allowable and the overspeed margin lands at
1.6351. A shop that cannot get the specified grade can build the blade out of the lighter one and
stay above the floor. That is worth knowing before somebody has to decide it on a Friday.

So the blade is foam limited. Stage 2's first coupon is a sandwich wrinkling test on the
delivered foam, not the laminate panel that looked like the obvious answer, and the laminate
panel still earns its place for areal mass and for the deflection and wind up numbers, which do
move with the skin modulus.

## What Stage 2 has to do

A static beam check is not a structural qualification and this document does not pretend
otherwise.

- **Fatigue.** The blade sees a fully reversed bending cycle at 39 Hz and the pitch link a
  reversed axial cycle at the same rate. At 2337 rpm a 3 minute run is 7,000 cycles and an hour
  is 140,000. Nothing here has been checked against an S-N curve
- **Oscillating bearing life.** The regime is now computed rather than flagged, and the pitch
  bearings sit at 0.5533 of full recirculation on a static safety factor of 4.15. What is still
  missing is the only thing that settles it, which is a run to failure at speed under the real
  load, with the grease that will be in the flight bearing
- **Modal response.** Blade first bending and first torsion, shaft whirl and frame modes have
  not been calculated. The 3 per revolution excitation at 117 Hz is the forcing to check against
- **Balance sensitivity.** A rotor with 31.75 g blades at 110 mm needs a stated balance
  tolerance. The assembly jig in the BOM is where that gets measured, and the tolerance itself
  is not set
- **FEA.** The root fitting, the bracket and the bearing block are all three dimensional parts
  checked here with beam formulae

## Numbers used

- structure.blade_mass_kg = 0.031747
- structure.centrifugal_load_N = 209.161
- structure.centrifugal_load_overspeed_N = 301.192
- structure.overspeed_factor = 1.2
- structure.blade_root_bending_Nm = 0.8228
- structure.blade_centrifugal_bending_Nm = 7.59254
- structure.blade_allowable_Nm = 25.2528
- structure.blade_ei_Nm2 = 51.115
- structure.blade_gj_Nm2 = 7.8058
- structure.blade_windup_deg = 2.2346
- structure.blade_margin = 30.6913
- structure.blade_combined_margin = 3.0008
- structure.blade_combined_margin_overspeed = 2.0839
- structure.blade_attachment_allowable_N = 781.148
- structure.blade_attachment_margin = 3.7347
- structure.blade_attachment_margin_overspeed = 2.5935
- structure.shaft_torque_Nm = 1.54226
- structure.shaft_allowable_Nm = 24.9563
- structure.shaft_margin = 16.1817
- structure.shaft_bending_Nm = 1.99506
- structure.shaft_combined_margin = 9.8968
- structure.motor_shaft_torque_Nm = 0.3902
- structure.transmission_ratio = 4.25
- structure.blade_load_lever_m = 0.0363
- structure.blade_load_factor = 4.0
- structure.pitch_link_load_N = 144.19
- structure.pitch_link_allowable_N = 474.074
- structure.pitch_link_margin = 3.3015
- structure.carrier_phase_jitter_deg = 0.1432
- structure.pitch_bearing_balls = 7
- structure.pitch_bearing_ball_mm = 1.5875
- structure.pitch_bearing_pitch_diameter_mm = 5.5
- structure.pitch_bearing_cage_swing_deg = 28.4545
- structure.pitch_bearing_ball_spacing_deg = 51.4286
- structure.pitch_bearing_recirculation_ratio = 0.5533
- structure.pitch_bearing_recirculation_travel_deg = 144.592
- structure.pitch_bearing_load_N = 52.2902
- structure.pitch_bearing_static_safety = 4.1496
- structure.pitch_bearing_static_safety_floor = 2.0
- structure.pitch_bearing_oscillation_hz = 38.9507
- structure.pitch_bearing_friction_W = 0.1536
- structure.pitch_bearing_plain_alternative_W = 8.1902
- structure.blade_wrinkle_stress_MPa = 215.2638
- structure.blade_allow_skin_Nm = 25.2528
- structure.blade_allow_spar_Nm = 63.1857
- structure.blade_skin_modulus_GPa = 60.0
- structure.blade_foam_modulus_MPa = 70.0
- structure.blade_foam_shear_MPa = 19.0
- structure.blade_skin_band_low = 0.5
- structure.blade_skin_band_worst_margin = 2.0739
- structure.blade_foam_knockdown_at_floor = 0.6144
- structure.blade_foam_downgrade_margin = 1.6351
- structure.blade_foam_downgrade_blade_g = 28.057
- pitch.pitch_bearing_travel_deg = 80.0
- pitch.carrier_radial_force_N = 80.36
- pitch.carrier_torque_Nm = 0.1287
- pitch.peak_blade_moment_Nm = 2.0967
- performance.blade_tip_deflection_mm = 0.09
- performance.blade_twist_deg = 0.014
- results.weight_N = 6.6503