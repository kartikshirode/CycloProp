# Structure and loads

This covers the 15 percent structural criterion, which had no section before week 4. Every
demand here is calculated in `tools/structure.py` from the frozen geometry, the frozen speed and
the section drawing, and the gate recomputes five of them. Nothing is asserted next to a
picture.

The headline is that this rotor is a centrifugal machine before it is an aerodynamic one. Each
blade pulls 221.46 N radially at the design point against a peak aerodynamic load of 24.00 N per
blade. Runco measured that ratio at 4.4 on a much smaller rotor; here it is 9.2, because
centrifugal load grows with radius and speed while blade lift does not grow with either in the
same way. So the blade attachment, the blade bending case and the declared overspeed decide the
structure, and the aerodynamic case decides almost nothing.

## Load cases

Two cases, both at sea level and both steady. No gust case, because the problem statement sets
no flight envelope for the module.

**Operating.** 2404.79 rpm, 18.0 N of thrust, 6.00 N of mean vertical force per blade. Peak
blade aerodynamic load is that mean times 4.0, which is the peak to mean factor D16 fixes at the
top of the published 3 to 4 range rather than the bottom, because the range is simulated. The
rerun week 3 model gives 2.501 and is deliberately not used for sizing.

**Overspeed.** 1.20 times design rotor speed, so 2885.7 rpm. Centrifugal load goes as the square
of speed, so this is 318.91 N per blade rather than 221.46, and it is 44 percent worse rather
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
| aerodynamic bending, 24.00 N over the span | 0.8712 Nm | 1.2545 Nm |
| centrifugal bending, 221.46 N over the span | 8.0391 Nm | 11.5763 Nm |
| both together | 8.9103 Nm | 12.8308 Nm |

The gated `blade_margin` is 28.99 because it compares the section against aerodynamic bending
alone, and that is the small load. The number that matters is the combined one, 2.83 at the
design point and 1.97 at overspeed, and both are gated now.

**Blade torsion is the interesting result.** The blade is driven in pitch from one end, through
a single horn, so the centrifugal pitching moment on an unbalanced blade has to be carried
through the blade's own torsional stiffness. 2.2058 Nm distributed over 290.4 mm of span at
7.81 Nm2 winds the far end up by 2.35 degrees, about 1.6 degrees averaged along the span. That
is 4 percent of the 40 degree pitch amplitude, and it is most of the 5 percent blade flexibility
loss the low thrust coefficient has been carrying since week 2 as a floor. Week 2 could only
bound that allowance from above. It now has a calculation under it, and driving the blade from
both ends would roughly quarter it, which is a Stage 2 option and not a Stage 1 change.

Deflection under the week 3 peak blade load of 15.01 N is 0.0936 mm, 0.13 percent of chord.
Twist under the aerodynamic pitching moment about the 30 percent axis is 0.0145 degrees. Neither
is a design driver.

**The attachment is the tightest joint in the module.** Each blade's 221.46 N goes into the two
pitch bearings that carry it on the spider arms. Two 693ZZ bearings at a 270 N static rating
give 540 N, so the margin is 2.44 at the design point and 1.69 at overspeed. That is the lowest
margin anywhere in the design and it is the one to watch, because the bearings oscillate through
80 degrees rather than rotating, which is a fretting duty a static rating does not describe.

## Shaft

A roll wrapped CFRP tube, 16 mm outer diameter and 1.5 mm wall, 340 mm long, with 7075-T6 plugs
bonded into both ends and turned to 15 mm bearing journals. D40 stops it inboard of the pitch
plane, because the pitch links sweep through the rotor axis, so it cannot be run out to an
outboard bearing on the mechanism side. The belt pulley has the other end to itself.

Rotor shaft torque is 1.41944 Nm, which is aerodynamic power plus tare divided by rotor angular
speed. Motor shaft torque is 0.43608 Nm, the same power through the 3.5 to 1 belt and its 0.93
efficiency. Those are different shafts and the document says which is which, because torque
upstream and downstream of a reduction is the number a reviewer checks first.

Torsional allowable is 24.96 Nm at 55 MPa of shear, so the torsional margin is 17.58. That is a
large number and it is honest: the shaft diameter is set by the bearing bore, the pulley
interface and lateral stiffness on a single ended drive, not by torque. The case that gets
closer is bending. The 56 tooth rotor pulley at 53.48 mm pitch diameter takes 53.09 N of
effective belt tension, 74.32 N of shaft side load at an HTD load factor of 1.4, and 30 mm of
overhang from the drive bearing, giving 2.2296 Nm of bending. Combining that with torsion by
maximum shear gives 5.83 MPa against 55, a margin of 9.44.

Main bearings are 61802, 15 by 24 by 5 mm, static rating 2320 N each. They carry the rotor
weight, the belt side load and the instantaneous lateral blade force, none of which approaches
that. They are chosen for bore and width rather than for load.

## Pitch load path

Peak pitch link force is 105.93 N, from the week 3 four-bar solved against the week 4 blade. The
blade is not chordwise balanced, so this is the unbalanced figure per D43.

Three elements are in that path and the weakest one sets the allowable.

| Element | Capacity as an axial link load | Margin |
| --- | --- | --- |
| pitch horn, 7075-T6, 8 by 4 mm at a 24.4 mm radius | 349.7 N | 3.30 |
| M3 aluminium bodied rod end, static | 600 N | 5.66 |
| CFRP link tube, 4 mm by 0.5 mm wall, Euler at 105 mm | 999.7 N | 9.44 |

The horn governs at 349.7 N and the margin is 3.30. That is the number behind the decision not
to balance the blade: a chordwise balance would take the link to 74.62 N and the margin to
4.69, and it costs 35.5 g across three blades, which is more than the thrust to weight case
can pay. See D46 and D53.

The offset post takes 53.22 N of radial pull from the three links converging on it. As an 8 mm
7075-T6 cantilever reaching 40 mm from the phasing carrier that is 2.13 Nm of bending against
20.1 Nm of capacity, a margin of 9.4. Carrier torque peaks at 0.1389 Nm at three per revolution,
120 Hz, which is above any servo's control loop. The servos hold it statically on a margin of
2.33, and the phase jitter it produces is bounded by gear backlash rather than by the servo:
0.05 mm of backlash across the 40 mm carrier gear is 0.143 degrees of carrier, inside the 25
degrees of authority the side force uncertainty already reserves.

## Pitch bearing oscillating duty

The tightest margin in the module is a bearing static rating, and a static rating is the wrong
yardstick for a bearing that never turns. Each blade hangs on two 693ZZ bearings that swing
through 80 degrees once a revolution while the centrifugal pull holds its direction in the
spider arm. Fixed load, oscillating rings, small amplitude. That is the arrangement false
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

What carries it is load. At 2404.79 rpm each bearing takes 110.73 N, half the 221.464 N
centrifugal pull, and the pair is rated at 540 N, so the static safety factor at the operating
point is 2.44 against a declared floor of 2.0. The floor is the same class of judgement as the
overspeed factor: a stated rule rather than a measurement, applied because a contact that never
moves has no second chance at a soft spot. It is gated, and the gate also refuses a floor that
a later week lowers.

Worth being plain about which of the two cases is actually binding. At the frozen 1.20
overspeed the 1.5 strength floor already asks more of the rating than the 2.0 wear floor does,
so the strength case governs today and blade attachment at 1.69 stays the number that sizes the
joint. The wear floor starts to bite only if a later week drops the overspeed, which is exactly
the trade it exists to catch.

Friction settles the alternative. Six deep groove bearings at a swing rate set by 40.08 Hz give
back 0.167 W, under a tenth of a percent of rotor shaft power, which is why it is not a line in
the power budget. A PTFE fabric lined plain bearing is immune to the wear mode above and is what
an oscillating aerospace joint uses, and the same six joints would cost 8.92 W instead. That is
better than fifty times the friction, and the sliding distance at 40.08 Hz is what turns it
around: a plain bearing that would be untroubled at ten swings a minute is running 167 mm of
liner past the shaft every second here.

So the ball bearing stays, on a static safety factor of 2.44 and an anti fretting grease behind
the shields. If a Stage 2 bench run shows fretting anyway, the fix is a larger bearing before it
is a different bearing type, and the conservative mass column has room for one.

## Frame and mount load path

Blade, spider arm, hub boss, shaft, main bearing, bearing block, frame tube, mount lug. The
reaction torque of 1.41944 Nm about the rotor axis reaches the airframe through both bearing
blocks and the four frame tubes, which is why the blocks sit on the tubes rather than on side
plates.

The lug pattern is 320 mm along the rotor axis by 240 mm across it, inside the 364.4 by 316.1 mm
packaged envelope. Thrust is 18.0 N and it swings across 120 degrees, so the worst single lug
sees roughly half the thrust rather than a quarter. Add its share of the 5.9642 N module weight
and the torque couple across the 240 mm transverse spacing, and the worst lug carries about 13.5
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
| blade bending, aerodynamic only | 0.8712 Nm | 25.25 Nm | 28.99 |
| blade bending, aerodynamic and centrifugal | 8.9103 Nm | 25.25 Nm | 2.83 |
| blade bending at 1.20 overspeed | 12.8308 Nm | 25.25 Nm | 1.97 |
| rotor shaft torsion | 1.41944 Nm | 24.96 Nm | 17.58 |
| rotor shaft, bending and torsion combined | 5.83 MPa | 55 MPa | 9.44 |
| pitch link path, horn governs | 105.93 N | 349.7 N | 3.30 |
| blade attachment, centrifugal | 221.46 N | 540 N | 2.44 |
| blade attachment at 1.20 overspeed | 318.91 N | 540 N | 1.69 |

The spread is the point. Two margins sit under 2 and everything else is over 3, which says the
module is sized by the blade attachment and by the blade in combined bending, and that the
places to spend effort in Stage 2 are those two joints rather than the shaft or the frame.

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
it, the worst overspeed margin found anywhere in the band is 1.9587, against 1.9681 at the
published value. Under 3 percent across a 2 to 1 range, and the worst point sits in the middle of
the band rather than at the bottom of it.

The foam is the sensitive input, because both of its moduli sit inside the same cube root. Knock
them down together and the allowable moves as the two thirds power. The overspeed margin reaches
1.5 at 0.6689 of the published foam properties, so a third off the delivered foam is what it
takes.

The realistic version of that is a grade substitution rather than a shortfall, and it is gentler
than the sweep suggests. On Rohacell 31 IG instead of 51 IG the blade weighs 28.057 g rather than
31.75, so the centrifugal demand falls along with the allowable and the overspeed margin lands at
1.5443. A shop that cannot get the specified grade can build the blade out of the lighter one and
stay above the floor. That is worth knowing before somebody has to decide it on a Friday.

So the blade is foam limited. Stage 2's first coupon is a sandwich wrinkling test on the
delivered foam, not the laminate panel that looked like the obvious answer, and the laminate
panel still earns its place for areal mass and for the deflection and wind up numbers, which do
move with the skin modulus.

## What Stage 2 has to do

A static beam check is not a structural qualification and this document does not pretend
otherwise.

- **Fatigue.** The blade sees a fully reversed bending cycle at 40 Hz and the pitch link a
  reversed axial cycle at the same rate. At 2405 rpm a 3 minute run is 7,200 cycles and an hour
  is 144,000. Nothing here has been checked against an S-N curve
- **Oscillating bearing life.** The regime is now computed rather than flagged, and the pitch
  bearings sit at 0.5533 of full recirculation on a static safety factor of 2.44. What is still
  missing is the only thing that settles it, which is a run to failure at speed under the real
  load, with the grease that will be in the flight bearing
- **Modal response.** Blade first bending and first torsion, shaft whirl and frame modes have
  not been calculated. The 3 per revolution excitation at 120 Hz is the forcing to check against
- **Balance sensitivity.** A rotor with 31.75 g blades at 110 mm needs a stated balance
  tolerance. The assembly jig in the BOM is where that gets measured, and the tolerance itself
  is not set
- **FEA.** The root fitting, the bracket and the bearing block are all three dimensional parts
  checked here with beam formulae

## Numbers used

- structure.blade_mass_kg = 0.031747
- structure.centrifugal_load_N = 221.464
- structure.centrifugal_load_overspeed_N = 318.908
- structure.overspeed_factor = 1.2
- structure.blade_root_bending_Nm = 0.8712
- structure.blade_centrifugal_bending_Nm = 8.03913
- structure.blade_allowable_Nm = 25.2528
- structure.blade_ei_Nm2 = 51.115
- structure.blade_gj_Nm2 = 7.8058
- structure.blade_windup_deg = 2.3509
- structure.blade_margin = 28.9863
- structure.blade_combined_margin = 2.8341
- structure.blade_combined_margin_overspeed = 1.9681
- structure.blade_attachment_allowable_N = 540.0
- structure.blade_attachment_margin = 2.4383
- structure.blade_attachment_margin_overspeed = 1.6933
- structure.shaft_torque_Nm = 1.41944
- structure.shaft_allowable_Nm = 24.9563
- structure.shaft_margin = 17.5818
- structure.shaft_bending_Nm = 2.22965
- structure.shaft_combined_margin = 9.442
- structure.motor_shaft_torque_Nm = 0.43608
- structure.transmission_ratio = 3.5
- structure.blade_load_lever_m = 0.0363
- structure.blade_load_factor = 4.0
- structure.pitch_link_load_N = 105.93
- structure.pitch_link_allowable_N = 349.727
- structure.pitch_link_margin = 3.3015
- structure.carrier_phase_jitter_deg = 0.1432
- structure.pitch_bearing_balls = 7
- structure.pitch_bearing_ball_mm = 1.5875
- structure.pitch_bearing_pitch_diameter_mm = 5.5
- structure.pitch_bearing_cage_swing_deg = 28.4545
- structure.pitch_bearing_ball_spacing_deg = 51.4286
- structure.pitch_bearing_recirculation_ratio = 0.5533
- structure.pitch_bearing_recirculation_travel_deg = 144.592
- structure.pitch_bearing_load_N = 110.7318
- structure.pitch_bearing_static_safety = 2.4383
- structure.pitch_bearing_static_safety_floor = 2.0
- structure.pitch_bearing_oscillation_hz = 40.0798
- structure.pitch_bearing_friction_W = 0.1673
- structure.pitch_bearing_plain_alternative_W = 8.9234
- structure.blade_wrinkle_stress_MPa = 215.2638
- structure.blade_allow_skin_Nm = 25.2528
- structure.blade_allow_spar_Nm = 63.1857
- structure.blade_skin_modulus_GPa = 60.0
- structure.blade_foam_modulus_MPa = 70.0
- structure.blade_foam_shear_MPa = 19.0
- structure.blade_skin_band_low = 0.5
- structure.blade_skin_band_worst_margin = 1.9587
- structure.blade_foam_knockdown_at_floor = 0.6689
- structure.blade_foam_downgrade_margin = 1.5443
- structure.blade_foam_downgrade_blade_g = 28.057
- pitch.pitch_bearing_travel_deg = 80.0
- pitch.carrier_radial_force_N = 53.22
- pitch.carrier_torque_Nm = 0.1389
- pitch.peak_blade_moment_Nm = 2.2058
- performance.blade_tip_deflection_mm = 0.0936
- performance.blade_twist_deg = 0.0145
- results.weight_N = 5.9642
