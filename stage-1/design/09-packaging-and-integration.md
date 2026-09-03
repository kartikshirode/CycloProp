# Packaging and integration

The integration half of the 5 percent packaging criterion. No CAD at Stage 1, so this is
dimensioned layout and interface definition, built on the swept envelope the week 3 linkage
solution actually produces rather than on the bare rotor circle.

## Package envelope

Start with what the blades sweep, because that is bigger than the rotor. The blade pitches plus
or minus 40 degrees about an axis at 30 percent chord, so 70 percent of a 72.6 mm chord swings
outboard of the pitch axis. Sampling the NACA 0020 outline at every rotor position gives an
outer swept radius of 148.25 mm and an inner one of 86.92 mm, so the swept annulus is 61.33 mm
thick and the swept diameter is 296.5 mm against a rotor diameter of 220.

That is worth flagging against week 2. The packaging rule in `01-configuration.md` compares
layouts on rotor count times 2R plus 20 mm of clearance plus 40 mm of frame, which put the
single rotor at 290 mm and made the span the largest dimension. On the swept diameter the same
rule gives 356 mm for one rotor, 511 for two and 625 for three, so the single rotor still wins
on size and it wins by more. Each rotor keeps its own 20 mm of clearance, which is how week 2
wrote the rule, so the cluster figures are not three swept diameters plus a single 60. The
comparison table stands because it is one rule applied to all three, and what changes is the
absolute figure rather than the ordering.

The module envelope is a sum of named parts, not an estimate:

| Direction | Build-up | Total |
| --- | --- | --- |
| Along the rotor axis | 290.4 mm span, two 8 mm side plates, two 12 mm bearing blocks, 16 mm phasing carrier at the non-drive end, 18 mm pulley and belt at the drive end | 364.4 mm |
| Across the rotor, in plane | 296.5 mm swept diameter plus 10 mm of frame tube each side | 316.5 mm |
| Across the rotor, vertical | the same 316.5 mm plus a 46 mm motor stack under the rotor | 362.5 mm |

Largest dimension is 364.4 mm, along the rotor axis, and the span is what drives it.

Inside that, the moving envelope has three parts an integrator has to keep clear. The blade
sweep is the 86.92 to 148.25 mm annulus over the full 360 degrees. The pitch link sweep is a
disc of 148 mm radius in one plane at the non-drive end, and that plane has to be empty on the
axis: the links pass within 0.019 mm of the rotor centreline, so nothing coaxial can sit in it.
The phasing carrier sweeps a 40 mm ring in the plane immediately outboard of that, and it moves
only on command, over 120 degrees.

That axis keep-out is the reason the drivetrain is single ended. The rotor shaft runs the span
and stops inboard of the pitch plane. The offset pivot is fed by a post from the phasing
carrier, which sits outboard of everything that rotates with the rotor and is supported from the
frame.

### Layout along the rotor axis

Dimensions in mm. The rotor axis runs left to right and the shaft stops before the pitch plane,
which is what makes the drive single ended.

```
      drive end                                                     non-drive end
  |<-18->|<--12-->|<-8->|<--------- 290.4 span --------->|<-8->|<--12-->|<--16-->|
  +------+--------+-----+--------------------------------+-----+--------+--------+
  | belt | bearing| side|                                | side| bearing| phasing|
  |  and | block  |plate|          blades and hubs       |plate| block  | carrier|
  |pulley|        |     |                                |     |        |  + 2   |
  +------+--------+-----+--------------------------------+-----+--------+ servos +
  |======= rotor shaft, 14 mm dia, stops here ==========================|        |
                                                              pitch     |  post  |
                                                              plane --->|<-------|
  |<------------------------------ 364.4 overall ----------------------------->|
```

The pitch plane sits between the non-drive bearing block and the phasing carrier. Nothing
coaxial may occupy it, because the pitch links pass within 0.019 mm of the centreline.

### Layout in the rotor plane

Looking along the rotor axis from the non-drive end. The rotor turns counter-clockwise and the
offset link points at 90 degrees of azimuth.

```
                        frame tube
                    +-------------------+
                    |   . - - - - - .   |   <-- outer swept radius 148.25
                    | .   blade 1     . |
                    |.   /             .|
        mount lug -->|  /   inner swept  |<-- mount lug
                    |. /    radius       |
                    | /     86.92       .|
                    |/    O <-- rotor axis, and 15.4 to the offset pivot E
                    |\   / \             |
                    | \ /   \           .|
        mount lug -->|  X  E  \ pitch   |<-- mount lug
                    |. / \    \  links  .|
                    | blade 2  blade 3  |
                    |   . - - - - - .   |
                    +-------------------+
                    |<-- 316.5 across -->|
                              |
                        46 motor stack
                              |
                    +-------------------+
                    |  motor and mount  |
                    +-------------------+
```

The three pitch links converge on E. The link belonging to the blade furthest from E is the one
that crosses the axis at O, and the swept annulus between 86.92 and 148.25 mm is what the frame
tubes have to stay outside.


## Mounting

Four mount points, on lugs at the corners of the frame, in the plane that contains the rotor
axis. Four rather than three because the module has to react a steady torque as well as a
steerable thrust, and a three point mount puts that torque into a triangle whose worst leg
carries most of it.

The reaction torque path runs: blade, spider arm, hub, through shaft, main bearing, bearing
block, frame tube, mount lug. Motor torque is 0.3902 Nm at the motor shaft and the belt
multiplies it by 4.25 into the rotor, so the frame sees that product as a steady moment about the
rotor axis whenever the module is producing thrust. Both bearing blocks take it, which is why
they sit on the frame tubes and not on the side plates.

Thrust reacts separately and it does not stay put. The resultant can be commanded anywhere
across 120 degrees, so the mount lugs see 17.0 N swinging through that arc rather than a fixed
vertical load, and the worst case for any one lug is not the vertical command. Week 4 sizes them
on the swung case.

Service access, in the order a person would need it. The phasing carrier and both servos come
off the non-drive end without disturbing the rotor. The belt is reachable at the drive end with
the motor in place. Blades come out individually once the pitch link is unpinned at the horn, so
a damaged blade does not mean stripping the mechanism. The ESC and the offset controller board
mount on the outside of the frame on the motor side, where they are in the rotor's own downwash.
The controller is a Matek Systems F411-WSE class board, 28 by 28 by 14 mm and 8.5 g, feeding
both servos off its own selectable 5 or 6 V rail at 3.5 A. It used to take the pack directly.
Its input range is 6 to 30 V and the declared pack is 8S, which reaches 33.6 V charged, so the
module needs a step-down ahead of the board or a controller rated past 34 V. That part is not
drawn and the 8.0 g line does not carry it. See D67 and `03-pitch-and-vectoring.md`.

## Drivetrain

One T-Motor Antigravity MN5006 KV450 on a single stage HTD-3M toothed belt at 4.25 to 1, 68
teeth against 16, turning at 9932 rpm to give the rotor 2337. Motor input is 483.2 W at 19.29 A
on an 8S pack, and the module draws 516.6 W once the actuator and controller allowances are
added. The pack moved from 6S to 8S in D67, because a 6S MN5006 caps at 392 W of mechanical
output against the 406 W the corrected rotor asks, and no belt ratio moves that cap.

The belt sits at the drive end outboard of the bearing block, on the opposite end of the module
from the pitch mechanism. That separation is deliberate and it falls out of the axis keep-out:
the two things that need the rotor axis, the drive pulley and the offset post, cannot share a
plane, so they take an end each.

Transmission efficiency is carried at 0.93, motor at 0.84 and ESC at 0.95. All three are assumed
rather than measured and the evidence ledger says so.

## Interfaces

Mechanical, to the airframe:

| Item | Definition |
| --- | --- |
| Mount pattern | 4 lugs, in the plane containing the rotor axis, taking thrust and reaction torque |
| Envelope reserved | 364.4 by 316.5 by 362.5 mm, with the swept annulus kept clear |
| Thrust vector | 17.0 N, steerable over 120 degrees in the plane normal to the rotor axis |
| Reaction torque | steady, about the rotor axis, motor torque times the belt ratio |
| Service faces | non-drive end for the pitch mechanism, drive end for the belt |

Electrical, to the vehicle:

| Item | Definition |
| --- | --- |
| Power in | 8S pack, 516.6 W at the module boundary including actuators and controller |
| Motor phases | three, motor to ESC, inside the module |
| ESC signal | one channel, throttle, sets rotor speed and therefore thrust magnitude |
| Actuator signal | one channel, phase command, driving both servos in parallel |
| Actuator power | 6.0 W allowance on the controller board's own 6 V servo rail |
| Sensing | none at Stage 1. The phase bias is a bench calibration, not a closed loop |

Two things an integrator should read twice. Thrust magnitude and thrust direction are separate
commands on separate channels, and they are not independent in effect: the side force tilt moves
with rpm, so a magnitude change needs a phase correction to hold the same direction. And the
120 degree vector range is the mechanism's authority before the side force trim is taken out of
it. `03-pitch-and-vectoring.md` has what that costs.

## Numbers used

- packaging.envelope_length_mm = 364.4
- packaging.envelope_width_mm = 316.5
- packaging.envelope_height_mm = 362.5
- packaging.mount_points = 4
- packaging.swept_diameter_mm = 296.5
- pitch.swept_outer_radius_mm = 148.25
- pitch.swept_inner_radius_mm = 86.92
- pitch.axis_keepout_mm = 0.019
- pitch.vector_range_deg = 120.0
- geometry.span_m = 0.2904
- geometry.chord_m = 0.0726
- performance.thrust_N = 17.0
- performance.motor_rpm = 9932.4
- performance.motor_torque_Nm = 0.3902
- performance.motor_input_W = 483.158
- performance.motor_input_current_A = 19.2876
- performance.belt_ratio = 4.25
- performance.module_electrical_power_W = 516.588
- performance.actuator_power_W = 6.0
- efficiency.transmission = 0.93
- efficiency.motor = 0.84
- efficiency.esc = 0.95