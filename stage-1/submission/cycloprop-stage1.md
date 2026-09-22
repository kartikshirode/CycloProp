---
title: "CycloProp: a cyclorotor propulsion module"
subtitle: "PUSHPAK Grand Challenge, Stage 1 preliminary design report"
date: "Prepared 31 August 2026, for submission on 26 September 2026"
geometry: margin=25mm
fontsize: 11pt
toc: true
---

# Submission identity

The team has supplied the identity details below. The member-level capability fields remain open
until the roster and sender are confirmed.

| Field | Value |
| --- | --- |
| Team name and members | Kalash, 3 |
| Institution | VPKBIET |
| Competition ID | CP-439436FADAD2 |
| Team ID | TM-5A7C41AF909 |

Rebuild the PDF after any source edit, then send it only from the confirmed address.

- Attachment name: `cycloprop-stage1.pdf`
- Address: kartikshirode123@gmail.com

# Summary

One cycloidal rotor. 3 blades on a 110.0 mm radius, NACA 0020, pitching plus or minus 40
degrees about an axis at 30 percent chord, turning at 2337 rpm, driven by a single outrunner
through a toothed belt at 4.25 to 1. Design thrust is 17.0 N against a requirement of at least
10 N.

The module weighs 687.91 g at the nominal budget and 775.74 g in the conservative column, so
thrust to weight is 2.5191 at the design point, which is a preliminary pass on the 2.5
requirement by 0.8 percent and not a margin anybody should rely on. Four cases are
reported rather than one, because reporting a single case is how this design misread itself for
a fortnight early on. The worst of the four stacks a low thrust coefficient on the conservative
mass and gives 2.1221, under the requirement, and the 117.26 g that would close it is published
in the mass section rather than argued away.

Blade pitch is passive. One four-bar per blade, all three sharing a single offset pivot 11.53 mm
from the rotor axis, and thrust vectoring is the direction of that offset rather than a separate
mechanism. Two 20 g servos turn a phasing carrier through a 1.5 step up and reach 120 degrees
of vector authority.

What this report is not: it is not a measurement, and it is not CAE. No CFD has been run, no
finite element model exists, nothing has been built and no coupon has been tested. Every load is
closed form, every allowable is a published class value and the thrust coefficient is
transferred from somebody else's rotor. Stage 1 asks for a preliminary design and this is one.
The sections that would be weak if it claimed more are marked, and the claims table near the end
carries every headline number with its confidence and its failure mode.

This report is submitted commercial in confidence. The problem statement invites teams to say so
and this one does, which covers the design, the numbers behind it and the tooling described in
the manufacturing section.

# Cyclorotor concept and configuration

One rotor, not a cluster. The blades run parallel to the rotation axis and pitch cyclically, so
the rotor makes a resultant force that can be pointed anywhere in the plane normal to its axis
without moving anything on the airframe.

The single rotor was chosen against redesigned two and three rotor clusters on one common model.
Same thrust coefficient, same figure of merit, same efficiency chain, same mass build-up, same
module boundary, same drive shortlist. Each layout was swept over radius in
small steps and its best conservative thrust to weight kept, and every contested assumption was set in the
cluster's favour: wakes that never overlap, no interaction penalty, one shared motor sized on
total power, one shared controller, and the same coefficient for all three even though splitting
the thrust drops the per rotor Reynolds number.

| Layout | Per rotor thrust | Rotor speed | Largest dimension | Module mass | Stacked T/W |
| --- | --- | --- | --- | --- | --- |
| single, 3 blades | 17.0 N | 2337 rpm | 290.4 mm | 647.23 g | 2.1281 |
| two rotors | 8.5 N | 3124 rpm | 400.0 mm | 796.12 g | 1.7286 |
| three rotors | 5.6667 N | 3864 rpm | 490.0 mm | 994.94 g | 1.3823 |

The single rotor wins the decision metric by 23 percent and it wins every other column too. The
reason is not subtle once the mass lines are sorted: splitting the thrust splits the aerodynamics
and does not split the hardware, since seven of the thirteen envelope lines multiply by the rotor
count while only three are shared. Total blade area also rises, because smaller rotors run at
lower tip speed for the same per rotor thrust. Chord Reynolds falls with the split too, from
130,296 on the single rotor to 92,133 and 75,227, which takes both cluster rows below the
measured band and the single rotor stays inside it.

Those three rows are built on the week 2 mass envelope, applied identically to all three layouts.
The refined budget later in this report moves the winning row from 2.1281 to 2.1221 and leaves
the other two where they are. Only the single rotor row carries the six corrected mass lines, and
three of those are per rotor, so correcting the cluster rows widens the gap rather than closing
it.

![Module general arrangement. Rotor radius 110 mm, 3 blades of 72.6 mm chord and 290.4 mm span, swept diameter 296.5 mm, packaged envelope 364.4 by 316.5 by 362.5 mm on 4 mount points.](figures/fig-arrangement.pdf)

**On CAD, since the problem statement is explicit about it.** It says teams must support
their design through CAD models, kinematic analysis, aerodynamic calculations or simulations,
structural assessment, mass estimation, material selection, actuation strategy, and an
implementation plan. Eight things, and this report carries seven of them. The missing one is CAD,
and the reading taken here is that the sentence describes the programme rather than the Stage 1
paper, because the same document lists CAD models under Stage 2 and attaches the published
weights to the final evaluation. That reading may be wrong. What is offered against it is that
every dimension a CAD model would carry is in this report and in the file that generates it: the
swept envelope, the four-bar lengths, the section, the mount pattern and the axial stack are all
solved rather than sketched, and the figures here are rendered from that same file.

The module boundary is taken from the problem statement rather than chosen: blades, frame, pitch
mechanism, motor, actuator and mounting hardware. Two disputed allocations were settled before
anything was scored, and both push our own number down. ESCs count in full, because the motor
does not turn without one. Mounting counts in full, so every fastener, insert, lug and bonded
joint.

Three more configuration choices, each of which could have gone the other way. Three blades
rather than four or six, because solidity is the quantity held fixed and at fixed solidity fewer
blades give more thrust, which is Benedict's own finding and matches Kellen's reported optimum
for this Reynolds band. NACA 0020 rather than something thinner, because thick sections stay
efficient at this scale and a thick section is what makes the blade buildable as a closed cell
with a real spar inside it. One motor with a belt reduction rather than direct drive, because
rotor torque at the design point is 1.54226 Nm at 2337 rpm and no outrunner in this mass class
makes that directly.


## Packaging and the moving envelope

Start with what the blades sweep, because that is larger than the rotor. The blade pitches plus or
minus 40 degrees about an axis at 30
percent chord, so seventy percent of a 72.6 mm chord swings outboard of the
pitch axis. Sampling the section at every rotor position gives an outer swept radius of
148.25 mm and an inner one of 86.92 mm, so
the swept diameter is 296.5 mm against a rotor diameter of
220.

The envelope is a sum of named parts rather than an estimate.

| Direction | Build-up | Total |
| --- | --- | --- |
| Along the rotor axis | 290.4 mm span, two 8 mm side plates, two 12 mm bearing blocks, a 16 mm phasing carrier at the non-drive end, 18 mm of pulley and belt at the drive end | 364.4 mm |
| Across the rotor, in plane | 296.5 mm swept diameter plus 10 mm of frame tube each side | 316.5 mm |
| Across the rotor, vertical | the same 316.5 mm plus a 46 mm motor stack under the rotor | 362.5 mm |

Largest dimension is 364.4 mm along the rotor axis, and the span drives
it. Three moving parts have to be kept clear inside that. The blade sweep is the
86.92 to 148.25 mm annulus over the full
revolution. The pitch links sweep one plane at the non-drive end and they pass within
0.019 mm of the rotor centreline, so nothing coaxial may sit in that plane,
which is the reason the drivetrain is single ended. The phasing carrier sweeps a
40 mm ring in the plane immediately outboard, and only on command.

The module mounts on 4 lugs in the plane containing the rotor axis. Four
rather than three, because the airframe sees the rotor shaft torque as a steady moment whenever
the module makes thrust, and a three point mount puts that moment into a triangle whose worst leg
carries most of it. Reserved envelope for an integrator is 364.4 by
316.5 by 362.5 mm with the swept annulus kept
clear, power in is an 8S pack at
518.0 W at the module boundary, and control is two channels:
throttle for thrust magnitude and a phase command for its direction. There is no sensing at Stage
1, so the phase bias is a bench calibration rather than a loop.


# Preliminary rotor sizing

The shape family is Kellen's UAV scale optimum: 3 blades, chord at 0.66 of the radius, blade
aspect ratio 4, NACA 0020, pitching plus or minus 40 degrees. Solving that family for a given
thrust pins the Reynolds number whatever the radius, because chord and span both scale with
radius and the size cancels out of the product of tip speed and chord.

| Parameter | Value |
| --- | --- |
| Radius | 110.0 mm |
| Chord | 72.6 mm |
| Span | 290.4 mm |
| Blades | 3 |
| Airfoil | NACA 0020 |
| Pitch amplitude | 40 degrees about 30 percent chord |
| Rotor speed | 2337 rpm |
| Tip speed | 26.92 m/s |
| Chord Reynolds | 130,296 |
| Solidity | 0.3151 |

Solidity sits inside the 0.30 to 0.40 band Kellen measured this shape family across, and the
design point sits inside the 100,000 to 300,000 Reynolds range of the same study, with his own
optimum rotor at 186,000. That matters more than it sounds. The earlier support for carrying a
thrust coefficient across a Reynolds change was Shrestha and Benedict, whose invariance range
stops at 100,000, so the design point used to sit past the end of an argument made about
something else. It now sits inside a measured band on its own shape.

**The blade area coefficient is 0.6055 and it is held deliberately below every measured or
corrected value available.** Kellen's optimum rotor of this shape family gives 0.6648, measured.
Benedict's quad hover point, recomputed from the printed pages rather than from the pairing this
project used to carry, gives 0.7211. His twin gives 0.8114 at a solidity far outside the band, so
that one is an upside indication and nothing rests on it. Raising the nominal to any of the three
would raise thrust everywhere and spend margin the design does not need.

The conservative coefficient is 0.5752, the nominal less 5 percent for blade flexibility and
nothing else. It used to carry a further 10 percent for a configuration transfer that changed
blade count, airfoil and chord ratio at once with nothing measured behind it. Kellen's
measurement on this shape family retired that half. What is left is an engineering downside
scenario, not a published lower bound, and it is labelled that way in the evidence ledger.

**Radius.** Inside a fixed shape family at fixed thrust, aerodynamic power falls roughly as one
over radius while rotor torque rises with it, and every geometry scaled mass line grows as the
square or the cube. Conservative thrust to weight therefore rises all the way down the radius
range and the best row is not the one the design uses. What picks 110.0 mm is the drive. A
smaller rotor asks more motor input power than the selected motor carries continuously, 531.5 W
against 520.0 W at 100 mm, and nothing lighter in the shortlist carries more. So the radius is the smallest one a named drive
holds continuously, which is a real finding and points at the cheapest available improvement.

![Blade section. NACA 0020 at 72.6 mm chord on a 8.712 mm spar tube at 30 percent chord, which is also the pitch axis. EI 51.115 Nm2 and GJ 7.8058 Nm2 come from this section, and so does the 25.2528 Nm allowable that the 8.4153 Nm combined root moment is held against. Skin wrinkling governs at 215.2638 MPa.](figures/fig-blade-section.pdf)

# Blade arrangement and pitch-control concept

Three blades at 120 degree spacing, each on its own passive four-bar, all three sharing one
offset pivot. No blade carries an actuator. The offset link's length sets the pitch amplitude and
its direction sets the phase, so one linkage answers the pitching requirement and the vectoring
requirement together.

| Link | Length | What it is |
| --- | --- | --- |
| L1 rotor arm | 110.0 mm | input crank, frozen by the radius |
| L2 offset link | 11.53 mm | ground link, solved for the pitch amplitude |
| L3 pitch link | 108.0 mm | output crank |
| L4 pitch horn | 18.0 mm | coupler |

Only L2 was solved. Bisecting on peak to peak pitch travel gives 11.53 mm for plus or minus 40
degrees. L1 is the radius, and L3 and L4 come off a vehicle Kellen built, with L3 rescaled by a
sweep rather than by his ratio: his length scaled to this radius costs more than twice the
carrier torque and leaves the two servos holding on exactly half their stall figure, which is not
a margin.

**Grashof and the assembly mode.** Sorted, the links are 11.53 mm, 18.0 mm, 108.0 mm and 110.0 mm.
The shortest plus the longest is less than the other two added together, and the shortest link is
the ground, so this is a double crank: the rotor arm turns fully, which it has to, and the pitch
link turns fully about the offset pivot once per rotor revolution.

**Transmission angle runs 53.88 to 135.68 degrees.** Both ends sit inside the conventional band
of 40 to 140. The cost is stated anyway rather than the band quoted: the worst sine over the
revolution is 0.699, meaning the mechanism's poorest moment arm is 70 percent of its best. Read folded, which is the reading that matters because an angle and its supplement cost
the same moment arm, the worst is 44.32 degrees, so nothing is near a singularity.

The solved schedule is 37 rows at 10 degree spacing. It reaches 40 degrees both ways, closes
exactly on itself over the revolution, and lags the offset direction by 7.75 degrees. Fitting a
cosine to it leaves an rms residual of 1.1406 degrees, which is 3 percent of amplitude. That
residual is not noise. It is where the side force comes from, and a prescribed sinusoid does not
have it.

**One geometric result set the whole drivetrain layout.** The pitch link passes within 0.019 mm
of the rotor axis, which is a crossing rather than a near miss, and it follows from the link set
rather than from bad luck. So the plane the pitch links sweep cannot contain the rotor shaft. The
shaft stops inboard of that plane, the rotor is driven from one end only, and the offset pivot is
fed by a post from a phasing carrier sitting outboard of everything that rotates with the rotor.
Clearance to the next blade is not close at 98.47 mm.

**Thrust vectoring.** The command is the direction of the offset link, and rotating it rotates the
whole pitch schedule rigidly. Two servos of the 20 g class drive a phasing carrier through
sector gears set 180 degrees apart, which doubles the holding torque and preloads the mesh so
backlash does not appear as thrust direction error. The servo gear is 60 mm and the carrier ring
gear is 40 mm, a 1.5 step up, so 80 degrees of servo travel becomes 120 degrees of carrier.

| Phase command | Vertical | Lateral | Resultant | Direction |
| --- | --- | --- | --- | --- |
| -60 degrees | 8.5000 N | -14.7224 N | 17.0 N | -60 degrees |
| -30 degrees | 14.7224 N | -8.5000 N | 17.0 N | -30 degrees |
| +0 degrees | 17.0000 N | 0.0000 N | 17.0 N | +0 degrees |
| +30 degrees | 14.7224 N | 8.5000 N | 17.0 N | +30 degrees |
| +60 degrees | 8.5000 N | 14.7224 N | 17.0 N | +60 degrees |

Direction follows command one to one and the magnitude holds across the range. Be clear about
why that comes out so clean: the rotor is axisymmetric, the blades are evenly spaced and the
inflow in this model is a uniform vector, so rotating the command rotates the entire solution
exactly. **That table is a statement about the model's symmetry and about what the mechanism can
reach. It is not a measurement of force at any of those commands.** What breaks it in hardware is
everything the model leaves out, and none of it is symmetric.

Holding torque peaks at 0.1287 Nm at three per revolution, 120 Hz, which is above any servo's
control bandwidth. Through the step up and across two servos that is 0.0965 Nm each against half
of a 0.3825 Nm stall figure, a margin of 1.982, and the phase jitter is bounded by gear backlash at
0.1432 degrees of carrier rather than by the servo loop.

**Side force is the open risk in this section and it is stated as one.** The model puts the
resultant 9.078 degrees round from the offset direction, of which 7.75 comes from the linkage
phase delay and only 1.33 from the aerodynamics. Measurement says the aerodynamic part is much
larger. Sirohi measured about 10 degrees, Adams 15 to 35 depending on amplitude and rotor speed,
and Benedict's twin sat at 30 degrees at its operating point.
A quasi steady model with uniform inflow has no wake return, no shed vorticity and no dynamic
stall hysteresis, and all three feed the lateral component, so under-prediction is the expected
failure and not a surprise.

The tilt is a bias rather than a loss, and the mechanism absorbs a known bias for free by
indexing the carrier zero at assembly. What the uncertainty costs is vectoring authority: indexed
at the centre of the measured band, the worst case residual comes out of the 120 degrees and
leaves the module with roughly four fifths of it. That is still a usable vectoring range and it
is the single largest consumer of authority in the design.

![Four-bar pitch kinematics at four azimuths. L1 110.0 mm rotor arm, L2 11.53 mm offset, L3 108.0 mm pitch link, L4 18.0 mm horn. The dotted path is the horn tip locus. Transmission angle runs 53.88 to 135.68 degrees, worst 44.32 degrees read folded.](figures/fig-linkage.pdf)

![Blade pitch schedule from the solved four-bar, against the 40 degree sinusoid it is usually assumed to be. The mechanism is not sinusoidal and the residual is what the load model runs on, rms 1.1406 degrees, peak pitch delayed 7.75 degrees past the offset direction.](figures/fig-pitch-schedule.pdf)

![Thrust vector map. Left, the resultant at each phase command, spanning 120 degrees. Right, direction against command on a one to one line. The magnitude is flat at 17.0000 N across the sweep, and that is the load model being rotationally equivariant rather than a measured result: turning the schedule and the inflow together turns the whole solution and preserves its size. At zero command the resultant already sits 9.078 degrees off the offset direction, which is a lag in the aerodynamics and not a commanded tilt.](figures/fig-vector-map.pdf)

# Estimated thrust and power requirement

Design thrust is 17.0 N and the conservative case is 16.1493 N. Both clear the 10 N requirement
on their own. Thrust comes from the blade area coefficient route, `T = Ct x 0.5 x rho x u^2 x N x
c x s`, at a tip speed of 26.92 m/s over a blade area of 0.06325 square metres.

Choosing 17.0 N is arithmetic rather than ambition. The conservative case has to clear 10 N by
itself, which puts a floor under the nominal. Above that, the geometry scaled mass lines do not
care what thrust the rotor is turning for, so extra thrust buys mass ceiling while only the drive
grows. The trade runs out at 17.0 N, and it runs out because of the drive rather than the
physics.

| Design thrust | Mass ceiling at T/W 2.5 | Ideal power | Rotor speed | Rotor torque | Drive consequence |
| --- | --- | --- | --- | --- | --- |
| 13.0 N | 530 g | 118.474 W | 2044 rpm | 1.1795 Nm | MN5006 on a 67 tooth rotor pulley, 4.1875 to 1. 15.17 A of the 20.8 A continuous, 323 W of 520 W, 0.3029 Nm of 0.4414 Nm and 66% of the speed ceiling. The binding line is current at 73%, so the row has 27% in hand |
| 16.0 N | 652 g | 161.766 W | 2267 rpm | 1.4516 Nm | MN5006 on a 70 tooth rotor pulley, 4.375 to 1. 17.71 A of the 20.8 A continuous, 441 W of 520 W, 0.3568 Nm of 0.4414 Nm and 77% of the speed ceiling. The binding line is current at 85%, so the row has 15% in hand |
| 17.0 N | 693 g | 177.166 W | 2337 rpm | 1.5424 Nm | MN5006 on a 68 tooth rotor pulley, 4.25 to 1. 19.29 A of the 20.8 A continuous, 483 W of 520 W, 0.3902 Nm of 0.4414 Nm and 78% of the speed ceiling. The binding line is power at 93%, so the row has 7% in hand |
| 18.0 N | 733 g | 193.026 W | 2405 rpm | 1.6331 Nm | no shortlist drive covers it. On the best whole tooth ratio available, 4.125 to 1 on a 66 tooth rotor pulley, the binding line is power at 101% of the MN5006's continuous rating: 526 W of motor input against 520 W. Nothing lighter in the shortlist carries more, and no ratio moves a power limit |
| 20.0 N | 815 g | 226.075 W | 2535 rpm | 1.8146 Nm | no shortlist drive covers it. On the best whole tooth ratio available, 3.875 to 1 on a 62 tooth rotor pulley, the binding line is power at 119% of the MN5006's continuous rating: 617 W of motor input against 520 W. Nothing lighter in the shortlist carries more, and no ratio moves a power limit |

Read the last column rather than the first. Below the design point the drive is stopped by
current, at 73 percent for 13 N and 85 percent for 16 N. At the design point power takes over at
93 percent, and above it power is what fails: 101 percent at 18 N and 119 percent at 20 N. No
belt ratio moves a power limit, because gearing slides the operating point along the motor's
capacity line without moving the line, and nothing lighter in the shortlist carries more power.
That is why the trade stops at 17 N rather than at a number chosen for the mass ceiling it
buys.

**Virtual camber is the reason the transfer is defensible, and it is also the largest single
uncertainty in it.** A blade on a circular path meets a curved oncoming flow, so a symmetric
section behaves like a cambered one and the effective incidence varies along the chord. The
effect scales with chord over radius. This rotor runs 0.66, Benedict's runs 0.43, and he calls it
significant at his value. Two things follow, and they point in opposite directions. Against the
transfer: at 0.66 the departure from the geometric section is larger here than on the rotor the
coefficient came from, so a blade element calculation on the nominal section would be wrong by
more. In favour of it, which is the stronger point: Kellen measured his coefficient on this same
shape family at a comparable chord to radius, so the virtual camber his rotor carried is close to
the one ours carries, and it is already inside the number being transferred rather than left out
of it. That is the case for moving a measured coefficient across rather than deriving one, and it
is why the analytical route here is used to bound the answer instead of to produce it. The
conformal correction that makes a blade element model usable at this chord to radius is Stage 2
work and is listed as such.

**Power is closed three ways rather than asserted once.**

Momentum theory over the projected frontal area, 2R times span, gives an ideal induced power of
177.166 W for 17.0 N. No rotor beats that. Kellen measures a figure of merit of 0.6, and it sits
with the thrust coefficient he measured beside it. This design carries a lower thrust coefficient
as deliberate margin, and figure of merit goes as the thrust coefficient to the power of one and
a half, so carrying his 0.6 alongside a cut coefficient would spend the same conservatism twice.
The consistent value is 0.5215, and blade aerodynamic power is 339.699 W. An independent route
through Benedict's measured power loading puts the same thrust at 274.194 W, so two routes that
share no equation agree to 19.3 percent. Induced velocity is 10.4215 m/s against a tip speed of
26.92, an inflow ratio of 0.3871, and that is high enough to be the main reason a simple model
should not be trusted for magnitude.

| Term | Value | Where it comes from |
| --- | --- | --- |
| blade aerodynamic power | 339.699 W | ideal power over a figure of merit of 0.5215 |
| rotor tare | 37.744 W | 10 percent of shaft power, measured on a flight weight rotor |
| motor input power | 483.158 W | shaft power through a 0.93 belt and a 0.84 motor |
| electrical power at the ESC input | 508.588 W | motor input over 0.95 |
| actuator draw | 6.0 W | two servos holding against residual link load |
| controller draw | 2.0 W | offset controller board |
| regulator conversion loss | 1.4118 W | board and servo rail through a 0.85 step down |
| module electrical power | 518.0 W | the four above |

The three efficiencies are assumed rather than measured and they are the only unevidenced links
in the chain. The motor figure is the sensitive one.

**The drive, on a derated continuous rating.** The selected motor is a T-Motor Antigravity MN5006
KV450 at 106 g. Its published figures are a maximum power and a peak current over 180 seconds,
which is a three minute maximum and not a hover rating, so every rating in the shortlist is
derated by 0.80 before anything is selected against it. Nothing justifies 0.80 rather than 0.70
or 0.90 except ordinary practice, and the problem statement states no endurance requirement to
size it against. It is an assumption and it is marked as one.

The consequence is bounded even though the number is not sourced. The design draws 0.7433 of
the published 180 second power and 0.7418 of the current, and the larger of the two, the power
fraction, is the derate at which the selection breaks even. It used to be the current fraction
and D67 moved it, which is worth saying because a derate checked against the line that stopped
binding is a check that passes for the wrong reason. Neither exit is open below it: the stacked thrust to weight
case needs 20.0272 N so no lower sensitivity row helps, and motor mass is a power class item
on a conservative column that is already 117.26 g over the 2.5 ceiling. What makes it tolerable is the duty. 0.7433 is a
fraction of a three minute rating, so a demonstration inside three minutes runs with a quarter of
the datasheet figure spare. A dynamometer run is the first drive gate in Stage 2.

A drive is accepted only if four things hold at once. Power: 483.158 W of a derated 520.0 W
continuous, which is the tight one at 93 percent. Torque: 0.3902 Nm against 0.4414 Nm continuous
at 4.25 to 1 through a 0.93 belt, 88 percent. Current: 19.2876 A of 20.8 A, derived from the
torque rather than from input power over pack voltage. Speed: the motor turns 9932.4 rpm against
a ceiling of 12799.2 rpm the pack can reach at the working current, 78 percent. Four other motors
were screened and each one fails at least one of the four.

**The motor is catalogued 4 to 6S and the pack is 8S, and those two facts do not conflict.** An
ESC is a buck converter, so the windings never see the pack. What they see is the back EMF plus
the resistive drop, which at 9932.4 rpm on a KV of 450 and 19.2876 A through 60 mOhm is
23.2293 V against the 25.2 V six cells reach off the charger. The motor is inside its catalogue
window at the design point. The pack is 8S because a 6S pack sags under this current to less
than the windings ask for, not because anything wants 33.6 V across it. What does meet 33.6 V is
the ESC, rated for it, the harness, and the pitch offset controller, which is rated 6 to 30 V and
therefore sits behind a 10.0 g step down regulator rated 42 V in and putting out 12 V. Two things
this does not settle and neither is buried: the 650 W and 26 A ratings were published against a
6S test, so a written manufacturer confirmation at this duty is a Stage 2 gate, and ESC switching
losses rise with the higher rail beyond what the assumed 0.95 accounts for.

The pack interface is 8S and the module declares it, because the battery sits outside the module
boundary. It has to be declared: the mechanical output a motor can make is capped at the speed
rule times the loaded pack voltage times the continuous current, and KV cancels out of that
product exactly, so gearing slides the operating point along that line and cannot move the line.
At 8S the cap is 532.448 W against the 405.853 W of mechanical
output this rotor asks for. At 6S the same product falls below what the rotor asks, which is why
the interface moved.

**Azimuthal load distribution.** A cycle averaged coefficient hides what a blade actually sees, so
the load model runs 36 azimuths with a uniform induced inflow and the solved pitch schedule
rather than a prescribed sinusoid. Peak vertical force per blade is 14.4260 N against a cycle mean
of 5.6667 N, so peak to mean is 2.5458. That sits below the published 3 to 4 range, and the honest
reading is that the model under-predicts the peak rather than that this rotor is gentler than the
literature. Structure is sized on 4.0 regardless.

The cycle mean lateral force is trimmed to zero by pointing the offset off module vertical. The
instantaneous lateral force still reaches 9.8252 N per blade inside the revolution, which is a
bearing and frame load rather than a thrust loss.

![Blade force against azimuth on the solved pitch schedule. Peak vertical 14.4260 N against a cycle mean of 5.6667 N, a peak to mean of 2.5458, which is what the structure is sized on rather than the mean.](figures/fig-blade-load.pdf)

# Estimated module weight and thrust-to-weight ratio

The module is 34 budget lines, every one a drawn section, a catalogue part or a stated allowance,
and every one pointing at the coarse envelope line it refines. The budget is built by a script
from the section drawing and the material densities, so the arithmetic reruns rather than being
typed.

| Line | Nominal | Conservative | Class |
| --- | --- | --- | --- |
| blade foam cores, 3 off | 28.79 g | 33.11 g | calculated |
| blade skins, 3 off | 29.08 g | 33.44 g | calculated |
| blade spar tubes, 3 off | 17.42 g | 20.03 g | calculated |
| blade root close-outs, 3 blades | 19.95 g | 22.35 g | machined |
| rotor spider arms, 6 off | 21.48 g | 24.71 g | calculated |
| rotor hub bosses, 2 off | 23.97 g | 26.85 g | machined |
| root attachment brackets, 6 off | 17.20 g | 19.26 g | machined |
| pitch bearings, 12 off | 15.60 g | 16.85 g | catalogue |
| pitch links with rod ends, 3 off | 12.36 g | 13.35 g | catalogue |
| pitch horns, 3 off | 4.86 g | 5.44 g | machined |
| offset pivot post and pin | 6.50 g | 7.28 g | machined |
| phasing carrier ring, 40 mm gear | 7.90 g | 8.85 g | machined |
| servo sector gear, 60 mm | 4.50 g | 5.04 g | machined |
| carrier support bearings, 2 off | 4.40 g | 4.75 g | catalogue |
| rotor shaft tube | 36.01 g | 41.41 g | calculated |
| shaft end plugs, 2 off | 23.20 g | 25.98 g | machined |
| main bearings, 2 off | 16.00 g | 17.28 g | catalogue |
| bearing blocks, 2 off | 25.27 g | 28.30 g | machined |
| frame tubes, 4 off | 46.36 g | 53.31 g | calculated |
| motor mount plate | 13.95 g | 15.62 g | machined |
| airframe mount lugs, 4 off | 7.20 g | 8.06 g | machined |
| frame and mount design reserve | 15.00 g | 18.75 g | allowance |
| motor, MN5006 KV450 | 106.00 g | 114.48 g | catalogue |
| rotor belt pulley, 68 tooth | 34.84 g | 39.02 g | machined |
| motor belt pulley, 16 tooth | 6.62 g | 7.41 g | machined |
| drive belt | 12.75 g | 13.77 g | catalogue |
| belt tensioner and bracket | 6.00 g | 6.72 g | machined |
| esc, 40 A 8S class | 19.50 g | 21.06 g | catalogue |
| vectoring actuator servos, 2 off | 40.00 g | 43.20 g | catalogue |
| pitch offset controller | 8.50 g | 9.18 g | catalogue |
| controller step down regulator | 10.00 g | 12.50 g | allowance |
| module wiring harness | 25.20 g | 31.50 g | allowance |
| fasteners and threaded inserts | 14.00 g | 17.50 g | allowance |
| structural adhesive at module joints | 7.50 g | 9.38 g | allowance |
| **module total** | **687.91 g** | **775.74 g** | |

**The growth rate is a property of the line, not of the module.** Each line is sorted into one of
four classes and each class carries a rate, decided before the total was looked at: 8 percent for
a catalogue part, 12 for a drawn and machined one, 15 for a section computed from stock, 25 for
anything not drawn at all. Weighted across the module that is 12.6 percent. Every group also has
to land within 25 percent of the coarse envelope line it refines, so the budget cannot quietly
move mass from one part of the module into another, and the four groups that moved more than 10
percent each have a stated reason.

There is a visible 15.0 g reserve, and it sits on the frame and mount group because that is the
least developed part of the module. It covers gussets, cable clamps, the servo bracket and the
ESC tray, none of which is drawn. It is not spread across rounded lines and it is not buried
inside a growth rate.

**What is genuinely fixed in this module is an 8.5 g controller board and the 10.0 g regulator
behind it.** That is worth saying
plainly, because the usual thrust to weight argument for a bigger rotor is that fixed hardware
amortises over more thrust. Sorted honestly, the wiring follows the envelope, the fasteners follow
the frame, the servo torque follows the pitch link load which follows thrust, and the bearings,
shaft and transmission follow rotor torque. Almost nothing here is free when the rotor grows.

| Case | Thrust | Mass | Weight | T/W |
| --- | --- | --- | --- | --- |
| design point | 17.0 N | 687.91 g | 6.7484 N | 2.5191 |
| coefficient downside alone | 16.1493 N | 687.91 g | | 2.3931 |
| mass downside alone | 17.0 N | 775.74 g | | 2.2339 |
| both stacked | 16.1493 N | 775.74 g | | 2.1221 |

**This is a preliminary nominal pass with an open compliance risk, and it is reported as one.**
The requirement is a thrust to weight above 2.5 on the module. At the design point the estimate
is 687.91 g and 2.5191, a margin of 0.8 percent, and the mass estimate behind it is not accurate
to 0.8 percent: most of its lines rest on drawn sections and catalogue figures rather than CAD
mass properties or weighed parts. Either downside on its own takes the result under 2.5, and both
together give 2.1221.

This project set out to hold every downside case to 2.5 as well, which was its own rule rather
than the competition's, and a correction to the figure of merit and to six mass lines broke it.
That is written down rather than redefined. The conservative column would have to lose
**117.26 g** to carry the stacked case back over 2.5, so Stage 2 treats 658.48 g as a gate on
that column and replaces the estimate with CAD mass properties, weighed parts and a thrust test,
in that order. It is Stage 2 item 6.

An internal target of 2.75 on the stacked case was set early as a margin goal. It is not met, it
is not claimed anywhere, and no further pass over the budget closes it: every remaining line is a
drawn section or a catalogue part, and trimming one to reach a number is exactly the move the
budget rules exist to stop. The two routes that would close it are a lower KV motor on more cells
and a measured thrust coefficient, and both are Stage 2 work.

One trade was priced and declined. Balancing the blade chordwise would lift the pitch link
margin from 3.2878 to 6.20, and the nose ballast that needs across three blades takes the
stacked case from 2.1221 to 2.0292, which spends mass on a case that already misses. Spending mass to improve a margin that already passes twice over is the wrong trade, so the
blade stays unbalanced and the load path carries it.

![Module mass by group. 34 drawn lines totalling 687.91 g nominal and 775.74 g conservative, with the line count per group in brackets. Thrust to weight is 2.5191 at the design point and 2.1221 with the coefficient and mass downsides stacked.](figures/fig-mass.pdf)

# Structural design and margins

Every allowable below is recomputed from the section and the moduli rather than quoted, so a
margin here is a calculation and not an assertion. The material choices those allowables rest on
are in the next section.

**The headline is that this rotor is a centrifugal machine before it is an aerodynamic one.** Each
blade pulls 209.161 N radially at the design point, and at a declared 1.20 overspeed that becomes
301.192 N, because centrifugal load goes as the square of speed. Mean aerodynamic force per blade
is 5.6667 N and structure is sized on 4.0 times that. The ratio between the two loads is 9.2 here,
where Runco measured 4.4 on a much smaller rotor.

| Case | Demand | Allowable | Margin |
| --- | --- | --- | --- |
| blade bending, aerodynamic only | 0.8228 Nm | 25.2528 Nm | 30.6913 |
| blade bending, aerodynamic and centrifugal | 8.4153 Nm | 25.2528 Nm | 3.0008 |
| blade bending at 1.20 overspeed | 12.1181 Nm | 25.2528 Nm | 2.0839 |
| rotor shaft torsion | 1.54226 Nm | 24.9563 Nm | 16.1817 |
| rotor shaft, bending and torsion combined | 1.99506 Nm of bending | von Mises on the tube | 9.8968 |
| pitch link path, the horn governs | 144.19 N | 474.074 N | 3.2878 |
| blade root pitch bearings, centrifugal | 209.161 N | 781.148 N | 3.7347 |
| blade root pitch bearings at 1.20 overspeed | 301.192 N | 781.148 N | 2.5935 |

The spread is the point. Two margins sit under 3 and everything else is over 3, and both of the
two are overspeed cases, so what sizes this module is the declared 1.20 factor rather than any
load it sees in normal operation. The tightest is the blade in combined bending at
2.0839, and it took that place from the root bearings
during the correction described below. Stage 2 effort belongs at the blade root rather than at
the shaft or the frame.

Those last two rows are a bearing capacity check and not a qualification of the bonded root
fitting, and the difference matters enough to say rather than leave to the row label. The
bearings are the softest element in the path from blade to spider arm, softer than the bond or
the bracket bolts, which is an argument from stiffness rather than a calculation. No adhesive
shear area, peel stress, stress concentration or cyclic knockdown has been computed for the
fitting itself. It carries 209.161 N steady with a load cycling at three per revolution on top,
and until a coupon and a local model exist the honest statement is a screened bearing margin
over an unquantified joint. The belt tooth and pulley stand in the same place, screened on
geometry and a factor with no supplier tooth rating behind them. The blade's own section allowable is set by skin wrinkling over the foam
and not by the laminate, and the spar would take more than twice the section's rating on its own.

**The attachment was the tightest joint until its rating was checked properly, and the
correction went the unusual way.** The earlier number rested on a supplier listing of 270 N for
the 693ZZ with no catalogue page behind it. Computing the static rating from the bearing's own
ball complement through ISO 76, `C0 = f0 x Z x Dw^2 x cos a` with f0 at 12.3, gives
216.985 N, which is lower. Duplexing to
4 bearings per blade over
2 stations at 90 percent load
sharing then gives 781.148 N against
301.192 N at overspeed, so the margin went from 1.69 to
2.5935 and the joint stopped being the driver. That costs
12 bearings in the mass budget and it is
carried there.

**What a static rating does not describe is the duty.** The bearing oscillates through
80 degrees under a steady radial load at
38.9507 Hz rather than rotating, and the balls travel
144.592 degrees against a
51.4286 degree spacing, a recirculation ratio of
0.5533. Below 1.0 the balls never leave their own arc, so
the raceway wears where they sit and false brinelling is the failure mode rather than fatigue.
The static safety factor at the operating load is 4.1496 against
a declared floor of 2.0, which is comfortable, and it
is still the wrong kind of number for this duty. What it needs is a supplier oscillating derate
or a run to failure at speed on the flight grease, and it has neither. The bearing was chosen
over a plain bush on friction: 0.1536 W against
8.1902 W for the plain alternative, and at
518.0 W of module power the plain option is not free.

**Blade stiffness came out fine in bending and interesting in torsion.** Tip deflection under the
peak blade load is 0.09 mm and twist under the aerodynamic pitching moment is 0.014 degrees,
so neither is a design driver. The blade is driven in pitch from one end though, so the
centrifugal pitching moment on an unbalanced blade has to go through the blade's own torsional
stiffness, and 2.0967 Nm winds the far end up by 2.2346 degrees. That is 4 percent of the pitch
amplitude, and it is most of the 5 percent blade flexibility allowance the conservative
coefficient carries. The allowance had a bound over it before and has a calculation under it now.

The reaction torque path is blade, spider arm, hub, through shaft, main bearing, bearing block,
frame tube, mount lug. The rotor shaft carries 1.54226 Nm and the motor shaft 0.3902 Nm, and the
airframe sees the rotor figure as a steady moment about the rotor axis whenever the module makes
thrust. Both bearing blocks take it, which is why they sit on the frame tubes rather than on side
plates, and there are 4 mount points rather than 3 because a three point mount puts that torque
into a triangle whose worst leg carries most of it.

**Four analyses are missing and none of them is closed form.** There is no finite element model,
so the root fitting, the spider arm and the bearing block are sized on net section and not on the
stress concentration each one really carries. There is no fatigue case, because the blade sees a
fully reversed aerodynamic cycle at 3 per revolution on top of a steady
centrifugal load and a paper design has no S-N data for this laminate. There is no rotor dynamics
case, so the first bending mode of the shaft is unknown against a
2337 rpm running speed. And there is no bonded joint analysis beyond area
and a class shear allowable, which is the weakest single assumption in the blade, since the root
fitting carries 301.192 N through adhesive. All four are named
in the Stage 2 plan with a test or a model against them.


# Initial material and manufacturing approach

Six materials carry load and each one was chosen because a structural calculation needed an
allowable. They are defined once, in the solver, and both the structures work and this section
cite that definition rather than restating it.

| Material | Where | The margin it decides |
| --- | --- | --- |
| Rohacell 51 IG class PMI foam, 88 percent fill | blade core | blade bending, through skin wrinkling |
| 60 gsm carbon twill, 2 plies | blade skin | blade bending, 3.00 and 2.08 |
| roll wrapped CFRP tube | spar, pitch links, rotor shaft, frame tubes | shaft torsion 16.18, combined 9.90 |
| 7075-T6 aluminium | horns, root fittings, brackets, blocks, lugs | pitch link path, 3.29 |
| 6061-T6 aluminium | pulleys, carrier ring gear, sector gear | none, these are stiffness parts |
| Araldite 2011 class epoxy paste | shaft plugs, root fittings, block bonds | none yet, and that is stated |

**The foam is structural here and not a filler.** Skin wrinkling over a soft core is what limits
the blade, and the wrinkling stress depends on the skin modulus and both core moduli, two of the
three belonging to the foam. Drop to a lighter grade and the wrinkling stress falls by roughly a
quarter, which takes the blade's combined margin at overspeed from 2.08 to 1.6351. That still
clears the 1.5 floor, and the point is not that the substitution fails but that it moves the
number a whole margin's worth. The margin reaches the floor at 0.6144 of the published foam
properties, so the grade is part of the structure and a substitution means a recalculation.

## Manufacturing and cost

Every part has a stock form, a process, one tolerance that matters and a joining method. Nothing
needs a process a university lab or a job shop in an Indian metro cannot run, and the one part
with no Indian stockist is called out.

The blade is CNC profiled foam in two halves with the spar channel cut, two plies wet laid in a
machined two part mould and vacuum bagged, cured at room temperature, then two turned 7075-T6
root fittings bonded over the spar and pinned. The shaft plugs are bonded into the tube first and
both journals ground afterwards in one setup, because grinding after bonding is what makes them
concentric. Three CNC job lines cover six part families between them, so a shop quotes them as
batches. The gear pair is the only job needing a cutter nobody local keeps on a shelf.

**What gets measured before it spins**, because a rotor at 2337 rpm with 209.161 N pulling on
every blade is not a thing to power up hopefully. Blade masses matched across the set, shaft
journal run out on the jig, and pitch angle checked against the solved schedule at 12 azimuths by
hand, where peak to peak travel is what matters because the rod ends can correct it. Then the
rotor turned by hand through two revolutions at both ends of servo travel, watching for a link
going over centre, since the worst transmission angle is 135.68 degrees and it wants feeling
rather than assuming. Then a static pull on one attachment above the overspeed load of 301.192 N,
and a first spin staged in four steps with current logged against prediction.

Bought parts and material come to 40030 INR, tooling and fabrication to 28800, and the module
totals 68830 INR at a longest single lead of 4 weeks. **These are indicative prices at
distributor list level and they are not obtained quotations.** No supplier was contacted, and the
source column of the full bill of materials names the distributor a part would be bought from
rather than one that has quoted for it. Five lines above 4500 INR carry 49.8 percent of the total
and those are what Stage 2 has to replace with written quotes.

The schedule driver is a 4 week foam import with no Indian source. Everything on a 3 week lead
sits inside that window, so ordering the foam first is the whole mitigation. If it slips, a
lighter core is not a drop in substitute, because the wrinkling calculation depends on the core
moduli, and the fallback is a thicker skin and a rerun.

# Team capability and execution plan

**This section is deliberately incomplete and the reason is worth stating.** Member details, prior
projects and tool licences behind this entry are facts about a team, and no part of the automated
work that produced this report may invent them. The structure below is real, the gap analysis is
real, and the fields still marked `[P-n]` are for a person.

Roster: Kalash, three members at VPKBIET. Individual names, roles and programmes still need to be
confirmed before submission. Team size is capped at 5 and the two solver workstreams in Stage 2
are where the additional members first pay for themselves.

The problem statement names seven areas where preference may be given, which is close to a
specification for this section, so it is answered area by area including the areas that are not
covered.

| Preference area | What the Stage 1 work shows | The gap |
| --- | --- | --- |
| Rotor design and unsteady aerodynamics | a coefficient traced to primary sources and recomputed, three scenarios with an evidence class each, a momentum floor, two independent power routes and a 36 point azimuthal load model | no unsteady solver has been run |
| CAD and mechanical design | dimensioned layout, a swept envelope from the linkage solution, an interface table and a mount pattern | no solid model exists |
| Kinematic analysis of mechanisms | a four-bar closed per blade, an offset solved by bisection, a schedule that closes on itself, Grashof and transmission angle, and a force vector map | closed form and planar, no multibody model |
| CFD, FEA and multibody dynamics | none of the three | the largest single gap in the project |
| Lightweight structures and material selection | six materials each tied to the margin it decides, a section integrated from its own ordinates, 8 margins and a declared overspeed | published class allowables, no coupon test |
| Motor, actuator and control selection | a five row drive shortlist screened on power, torque and reachable speed, all on derated continuous ratings | four rows and the servo are supplier listings, and no control loop is designed |
| UAV subsystem integration and testing | interface definitions, an assembly order and six pre-spin measurements | nothing has been built or tested |

**Execution plan for Stage 2.** The window is 3 October to 2 December 2026 and this plan submits
on 1 December. All 11 Stage 2 items are scheduled below with the gate that closes each one, and
`07-team-and-execution.md` carries the same schedule with the tool category, the dependency and
the owner against every item.

| Weeks | Stage 2 items | Closed when |
| --- | --- | --- |
| 1 to 2 | CAD model of the module, and supplier quotations started | every budget line exists as a solid and the model's mass properties reproduce the budget |
| 2 to 3 | kinematic model, then motor, actuator, bearing and controller selection | the multibody schedule matches the closed form one and reproduces the pitch link load |
| 4 to 5 | aerodynamic analysis for thrust prediction | a converged run at the design point with mesh and timestep independence shown |
| 6 | structural analysis of blades, supports, frame, shaft and linkages | the 8 margins reproduce or move, with every difference explained |
| 7 | material selection, mass estimate and thrust to weight | a wrinkling coupon on the delivered foam, which is what the blade allowable turns on, then the laminate panel |
| 8 | manufacturability and assembly plan, bill of materials, risk assessment | written quotes for the five lines above 4500 INR, and every open risk owned |
| 8 to 9 | build and test plan, then the report | a staged spin plan, an instrumented thrust measurement and a place to run it |

Quotations sit in week 1 rather than week 8 because the 4 week foam lead gates the build plan.
The aerodynamic item is the one most likely to overrun, and its fallback is a 2D transient study
at the design azimuth set, reported as what it is rather than as a full solution.

Three of the four capability gaps have a route that needs no new person. CFD has an open source
option and a validation case in Kellen's measured rotor, whose shape family matches this design to
within 1.1 percent. FEA is wanted for three small parts already sized by beam formulae, so its job
is to find where the idealisation was wrong. Multibody has a published answer to reproduce on day
one, so it is cheapest and goes first. Testing is the gap with no software route: `[P-9]` a layup
bench, a test frame, a load cell and somewhere safe to spin a rotor.

# Evaluation criteria map

Where each published criterion is answered in this report.

| Criterion | Weight | Where it is answered |
| --- | --- | --- |
| Feasibility of achieving 10 N thrust | 15% | Estimated thrust and power requirement: thrust from geometry on a transferred coefficient held below a measurement of this shape family |
| Feasibility of thrust-to-weight above 2.5 | 15% | Estimated module weight and thrust-to-weight ratio: a 34 line budget and four cases. The design case clears 2.5 by 0.8 percent and all three downside cases miss, with the 117.26 g that would close the stacked case published |
| Kinematic design of blade-pitch and thrust-vectoring mechanism | 15% | Blade arrangement and pitch-control concept: loop closure, solved schedule, Grashof and the force vector map |
| Aerodynamic analysis or simulation quality | 15% | Estimated thrust and power requirement: momentum floor, figure of merit, a second power route and an azimuthal model |
| Structural design and strength assessment | 15% | Structural design and margins: two load cases, 8 margins, what the root bearing rows do and do not qualify, and the analyses not done |
| Manufacturability, material selection and cost realism | 10% | Initial material and manufacturing approach: per part process and tolerance, assembly order and a costed bill of materials |
| CAD quality, integration readiness and packaging | 5% | Cyclorotor concept and configuration, with the swept envelope, interfaces and mounts, and no CAD at this stage |
| Presentation, viva and technical clarity | 10% | This report, the claims table below and the examiner questions in appendix A |

# Claims, evidence and risk

Every headline claim, what produced it, how much weight it carries, what would break it and what
Stage 2 does about that.

| Claim | Where it comes from | Confidence | Main failure mode | Stage 2 validation |
| --- | --- | --- | --- | --- |
| Blade area coefficient 0.6055 gives 17.0 N | transferred from a recomputed hover point, bracketed above by 0.6648 measured on this shape family | medium | the transfer is wrong in the unsafe direction, or the model overstates thrust at an inflow ratio of 0.3871 | transient CFD, then a load cell run |
| Module mass 687.91 g nominal, 775.74 g conservative | 34 lines, each a drawn section, a catalogue part or a stated allowance, growth by line class | medium to high | a wet layup blade comes out heavy, or undrawn frame parts eat the 15.0 g reserve | CAD mass properties, a mould trial, weighed parts |
| Blade deflection 0.09 mm, wind up 2.2346 degrees | closed form beam and torsion on the integrated section | medium | cured laminate modulus under the class value, which moves these two even though it barely moves the strength margin | coupon panel, then FEA |
| Direction follows the vector command one to one at 17.0 N | model symmetry, not measurement | low on magnitude | wake skew, the frame in the flow, the blade meeting its own wake | two axis load cell across the range |
| Stacked conservative thrust to weight 2.1221 | recomputed from geometry and the mass lines | medium | it is under the 2.5 requirement, and 117.26 g is published as the mass that would close it | Stage 2 items 3, 6 and 7 together |
| Blade attachment margin 2.5935 at overspeed | ISO 76 static rating over recomputed centrifugal load, oscillating duty computed | medium | 0.5533 of full recirculation, so it wears where it sits and no catalogue figure covers that | run to failure at speed, on the flight grease |
| Structural blade load factor 4.0, against a solved peak to mean of 2.5458 | published simulated range, top of it taken, and the solved schedule sits under it | low to medium | the true peak is higher under dynamic stall | measured blade forces, or CFD |
| Module electrical power 518.0 W | momentum floor, figure of merit, efficiency chain | medium | all three efficiencies are assumed and the motor one is sensitive | bench measurement on the built module |
| The drive holds the design point continuously | derated ratings against power, torque, current and speed | medium | the 0.80 derate has no source and breaks even at 0.7433, with power the binding line at 93 percent | dynamometer run at the working current, early |
| Side force tilt 9.078 degrees | quasi steady model with uniform inflow | low | measurement puts it far higher and it moves with rotor speed | load cell calibration across the speed range |
| Module cost 68830 INR, longest lead 4 weeks | distributor list prices, nothing quoted | low on price | gear cutting is priced by setup at a quantity of one | written quotations |
| Material allowables | published typical values per class | medium | no certificate, no coupon, and the foam is the sensitive one rather than the laminate: the floor arrives at 0.6144 of the published foam properties | wrinkling coupon on the delivered foam, then a laminate panel and a bond shear coupon |

# Sources and how they were read

Seven evidence classes are used: measured, somebody measured this quantity on this configuration
and the figure was read off the source; derived, computed here from figures measured on a
different configuration; transferred, a derived value carried across a change of geometry or
Reynolds number; catalogue, a manufacturer or supplier figure for a part; summary, only a summary
of the source has been read; downside, a deliberately pessimistic value carried to bound a case;
assumed, no source at all. Four rows in the ledger are class measured and none of them was
measured on this hardware.

**Nobody has put this rotor on a load cell.** Where this report says measured, it means measured
by somebody else on a rotor of this shape family, and the distinction is kept everywhere it
matters.

## References

Each entry says how it was read. Where a volume, page range or DOI is missing, it is because this
project does not hold one it could check, and a guessed identifier would be worse than none.

1. Kellen, A. J. *Performance Measurements on a UAV-Scale Cycloidal Rotor in Hover.* MS thesis,
   Texas A&M University, 2019. Handle 1969.1/184958, https://hdl.handle.net/1969.1/184958. Read
   in full from a text extract of the PDF, held with its sha256
2. Benedict, M. *Fundamental Understanding of the Cycloidal-Rotor Concept for Micro Air Vehicle
   Applications.* PhD dissertation, University of Maryland, 2010. Handle 1903/11257,
   https://hdl.handle.net/1903/11257. Read in full the same way
3. Sirohi, J., Parsons, E. and Chopra, I. Hover performance of a cycloidal rotor for a micro air
   vehicle. *Journal of the American Helicopter Society*, July 2007. Read
4. Xisto, C., Leger, J., Pascoa, J. et al. Parametric analysis of a large-scale cycloidal rotor in
   hovering conditions. *Journal of Aerospace Engineering*, 2016. Read
5. Runco, C. and Benedict, M. Design, development, and flight testing of a 70-gram micro
   quad-cyclocopter. *International Journal of Micro Air Vehicles* 15, 2023. Open access, read
6. Shrestha, E., Benedict, M. et al. Understanding upward scalability of cycloidal rotors for
   large-scale UAS applications. *Journal of the American Helicopter Society* 67(4), October
   2022. Summary class
7. Adams, Z., Benedict, M., Hrishikeshavan, V. and Chopra, I. Design, development, and flight
   test of a small-scale cyclogyro UAV utilizing a novel cam-based passive blade pitching
   mechanism. *International Journal of Micro Air Vehicles* 5(2), 2013, p. 145. Summary class
8. Alsabri et al. *Aerospace* 13(9), article 765, 2025. Two dimensional URANS. Summary class,
   not read here

Not read and not cited as evidence anywhere in this report: Ramsey, R. A., *Development and
Flight Testing of a 25-Kilogram Quad-Cyclocopter*, MS thesis, Texas A&M University, 2022,
handle 1969.1/198531, which would give a second structural mass anchor; and Heimerl, Halder,
Benedict et al., *Experimental and Computational Investigation of a UAV-Scale Cycloidal Rotor in
Forward Flight*, VFS 77th Annual Forum, which measured instantaneous blade forces across a
Reynolds band that brackets this design and would replace both the peak to mean estimate and the
side force angle with measurements.

## Where each borrowed number comes from

| Number used here | Source and locator | Class |
| --- | --- | --- |
| blade area thrust coefficient 0.6648 | [1] Table 2.1 configuration 8, CT/sigma read off Figures 3.25 and 3.28 | measured |
| figure of merit 0.6 | [1] section 3.3, closed against Figures 3.25 and 3.26 to 0.595 | measured |
| solidity band 0.30 to 0.40 | [1] section 3.2.7 and Figure 3.30 | measured |
| chord Reynolds 100,000 to 300,000 | [1] abstract and Table 2.1 | measured |
| blade area thrust coefficient 0.7211 | [2] printed pp. 220, 225, 233 and 236, the quad hover point | derived |
| blade area thrust coefficient 0.8114 | [2] printed pp. 229 and 232, the twin rotor | derived |
| power loading 0.062 N/W | [2] printed p. 232 | derived |
| rotor tare 10 percent of shaft power | [2] printed pp. 232 and 236 | transferred |
| module thrust to weight benchmark 2.13 | [5] Table 3, re-cut onto this competition's module boundary | derived |
| side force tilt 10 to 35 degrees | [3], [7] and [2] | summary |
| peak to mean blade load 3 to 4 | [8] | summary |
| Reynolds invariance, blade mass scaling | [6] | summary |

No figure or table has been reproduced from any source. Every published number used here was
recomputed into this project's own conventions from figures printed in the source, and the
conversion is recorded in the evidence ledger alongside the printed page it came from.

# Appendix A: examiner questions

Twelve questions this design should expect, answered short. Where an answer exposed a gap, the
report was changed rather than the answer smoothed.

**1. Your whole design hangs off a thrust coefficient measured on a different rotor. Why should
anyone believe 17.0 N?** They should believe the conservative case first. The nominal 0.6055 is
transferred, and its original provenance was wrong, so it was recomputed from the printed pages
and the corrected value is 0.7211, higher than what is used. Kellen then measured 0.6648 on a
rotor whose solidity and chord to radius are within 1.1 percent of this one. Three values sit
above the number the design is built on, and they are three values from two studies rather than
three independent ones: 0.7211 and 0.8114 both come out of Benedict 2010, on his quad and his
twin. That is the argument, and it does not make
17.0 N a measurement. The claim is that the design closes on a coefficient deliberately below the
evidence, and the requirement is 10 N.

**2. The published benchmark for a module like this is between 1.78 and 2.13 depending on
allocation. You claim 2.5191 at the design point. Why is that credible?**
Because the benchmark is a 70 gram micro-scale vehicle re-cut onto this boundary, and blade mass
per newton is roughly scale invariant while the drive and structure are not. This module makes
17.0 N from one motor, one belt, one shaft and one pitch mechanism, where the
benchmark makes a fraction of that per rotor from four sets of hardware. The gap is not a claim
to have beaten anybody at the same scale. It is amortisation, and the report is careful about how
little of it is real: the genuinely fixed mass in this module is an 8.5 g board and the 10.0 g
regulator in front of it. The stacked
conservative case is 2.1221, which lands inside the
benchmark band rather than above it, and that is the number to argue with.

**3. What in the module is actually fixed as the rotor grows?** Almost nothing. The 8.5 g
controller and the 10.0 g regulator that feeds it. Wiring follows the envelope, fasteners follow the frame, servo torque follows the
pitch link load which follows thrust, and the shaft, bearings and transmission follow rotor
torque. This is stated in the module weight section because it is the weakest part of the usual argument
for a large single rotor, and hiding it would be worse than losing the point.

**4. Why 110.0 mm and not the radius your own sweep prefers?** The sweep prefers smaller. A
smaller rotor is lighter on every geometry scaled line and conservative thrust to weight rises
all the way down. What stops it is the drive, and it stops on power rather than on gearing. At
100 mm the rotor asks 531.51 W of motor input against
520.0 W
continuous, and no belt ratio moves a power limit because gearing slides the operating point
along the motor's capacity line without moving the line. Nothing lighter in the shortlist carries
more. So 110.0 mm is the smallest radius a named drive holds continuously, and a motor with more
continuous power in the same mass class is where the design would go next.

**5. Your motor sits at 93 percent of its continuous power and the derate has no source. Is that
a design or a hope?** It is a judgement, stated as one. T-Motor publishes a maximum over 180
seconds, which is not a hover rating, so every shortlist figure is cut to 0.80 before selection.
Nothing supports 0.80 over 0.70 or 0.90 except practice, and the problem statement gives no
endurance requirement to size it against. At the derated figure the design point takes 483.158 W
of 520.0 W and 0.3902 Nm of 0.4414 Nm, so power is the line that binds and torque has room. The
selection breaks even at a derate of 0.7433, so a true continuous derate of 0.75 still holds. A
thermal run on the bench is what settles it, and it is in the Stage 2 plan.

**6. Where does the reaction torque go?** Blade, spider arm, hub, through shaft, main bearing,
bearing block, frame tube, mount lug. The rotor shaft carries 1.54226 Nm and the motor shaft
0.3902 Nm upstream of the belt, and the report says which is which because that is the first
thing a reviewer checks. The airframe sees the rotor figure as a steady moment whenever the
module makes thrust, both bearing blocks react it, and the mount has 4 points rather than 3 for
exactly that reason.

**7. Your transmission angle reaches 135.68 degrees. How close is this mechanism to a
singularity?** Not close. The whole range, 53.88 to 135.68, sits inside the conventional band of
40 to 140, and reading it folded is what matters anyway, because an angle and its supplement
cost the same moment arm. Folded, the worst is 44.32 degrees, whose sine is
0.6987, so the poorest moment arm over the revolution is 70 percent of the
best. The linkage is a double crank by the Grashof test, both cranks
turn fully, and the assembly is checked by hand through two revolutions at both ends of servo
travel before first spin.

**8. Your vector map shows constant 17.0 N at every command. Real rotors do not do that. Is the
table a measurement?** No, and the report says so in bold in item 3. The rotor is axisymmetric,
the blades are evenly spaced and the inflow in this model is uniform, so rotating the command
rotates the whole solution exactly. The table is a statement about model symmetry and about the
commands the mechanism can reach, nothing more. Wake skew, the frame and shaft supports sitting
in the flow on one side, and the blade passing through its own returning wake all break that
symmetry and none of them is symmetric. A two axis load cell across the command range is the
measurement that replaces it.

**9. Is the blade stiff enough, and how do you know without FEA?** In bending, comfortably, and
the numbers are small enough that FEA would not change the answer: 0.09 mm of tip deflection
under peak blade load and 0.014 degrees of aerodynamic twist against a 40 degree amplitude. The
one that matters is torsion. The blade is pitched from one end, so the centrifugal pitching
moment of 2.0967 Nm on an unbalanced blade winds the far end up by 2.2346 degrees, about 4
percent of amplitude. That is most of the 5 percent flexibility allowance the conservative
coefficient carries, so the allowance now has a calculation under it instead of being a chosen
floor. Driving the blade from both ends would roughly quarter it and costs hardware the mass
budget has no room for.

**10. Your side force model gives about a degree of aerodynamic tilt and the literature measures
tens of degrees. Why publish it?** Because it is the honest output of a quasi steady model with
uniform inflow, and because the difference is explainable rather than mysterious: that model has
no wake return, no shed vorticity and no dynamic stall hysteresis, and all three drive the
lateral component. The stored figure is carried as a lower bound and labelled one. The design
handles the tilt as a bias rather than a loss, since indexing the phasing carrier zero at
assembly costs no actuator range, and the uncertainty in the bias is what costs range. It is the
largest single consumer of vectoring authority in the design.

**11. What is the tightest thing in the module?** The blade in combined bending at
1.20 overspeed, at 2.0839. It took
that place from the root pitch bearings, which were 1.69 on a supplier listing of 270 N per bearing
and reads 2.5935 once the rating is computed from the
bearing's own ball complement through ISO 76 and the joint is duplexed to
4 bearings per blade. Both of the two margins under 3 are
overspeed cases, so the declared 1.20 factor is what sizes this module
rather than any load it sees in normal operation. The attachment still has the worst duty even
with the better number: 4 bearings give
781.148 N against
301.192 N, but they swing through
80 degrees under a steady load rather than rotating, and a
static rating says nothing about fretting.

**12. What is the first test you run in Stage 2?** A sandwich wrinkling coupon on the delivered
foam. The obvious answer is a laminate panel, and we assumed it was the answer until the
sensitivity was actually run. Skin wrinkling over the foam sets the blade allowable, and dropping
the skin modulus lowers the wrinkling stress as its cube root while raising EI over the skin
modulus, so the two nearly cancel: over a 2 to 1 band on the skin the worst overspeed margin is
2.0739 against
2.0839 at the published value. The foam moduli sit in the
same cube root as a pair, so the allowable moves as their two thirds power and the margin reaches
its floor at 0.6144 of them. The blade is foam limited. Second is a static pull on one blade attachment above the
overspeed load of 301.192 N. The rotor does not spin until both have passed.

# Appendix B: numbers and provenance

Every number in this report is defined once, in `stage-1/design/numbers.json`, and the prose
cites it rather than restating it. A gate script recomputes the physics from the stored geometry
and the mass lines, applies the competition limits to what it recomputed rather than to any
stored headline, and fails on disagreement. It also audits this document: every number in the
narrative carrying a physical unit has to match a computed value in the same dimension.

## Numbers used

- performance.thrust_N = 17.0
- geometry.radius_m = 0.11
- results.thrust_to_weight_conservative = 2.1221
- geometry.chord_m = 0.0726
- geometry.span_m = 0.2904
- geometry.blades = 3
- geometry.pitch_amplitude_deg = 40.0
- geometry.pitch_axis_pct_chord = 30.0
- operating.rpm = 2337.04
- operating.tip_speed_ms = 26.9207
- operating.reynolds = 130296.0
- performance.thrust_N_conservative = 16.1493
- performance.blade_area_coeff = 0.6055
- performance.blade_area_coeff_low = 0.5752
- performance.blade_deflection_thrust_loss = 0.05
- performance.solidity = 0.3151
- performance.blade_area_m2 = 0.06325
- performance.aero_power_W = 339.699
- performance.ideal_power_W = 177.166
- performance.figure_of_merit = 0.5215
- performance.aero_power_W_published = 274.194
- performance.power_spread = 0.1928
- performance.tare_power_W = 37.744
- performance.electrical_power_W = 508.588
- performance.module_electrical_power_W = 518.0
- performance.actuator_power_W = 6.0
- performance.controller_power_W = 2.0
- performance.induced_velocity_ms = 10.4215
- performance.inflow_ratio = 0.3871
- performance.blade_load_peak_to_mean = 2.5458
- performance.motor_input_W = 483.158
- performance.motor_rpm = 9932.4
- performance.motor_torque_Nm = 0.3902
- performance.motor_input_current_A = 19.2876
- performance.pack_voltage_charged_V = 33.6
- performance.motor_terminal_voltage_V = 23.2293
- performance.motor_catalogue_ceiling_V = 25.2
- performance.regulator_loss_W = 1.4118
- performance.belt_ratio = 4.25
- performance.blade_tip_deflection_mm = 0.09
- performance.blade_twist_deg = 0.014
- efficiency.transmission = 0.93
- efficiency.motor = 0.84
- efficiency.esc = 0.95
- pitch.offset_m = 0.01153
- pitch.pitch_link_m = 0.108
- pitch.horn_m = 0.018
- pitch.phase_delay_deg = 7.75
- pitch.schedule_rms_residual_deg = 1.1406
- pitch.transmission_angle_min_deg = 53.88
- pitch.transmission_angle_max_deg = 135.68
- pitch.axis_keepout_mm = 0.019
- pitch.neighbour_clearance_mm = 98.47
- pitch.pitch_bearing_travel_deg = 80.0
- pitch.vector_range_deg = 120.0
- pitch.phase_authority_deg = 120.0
- pitch.servo_travel_deg = 80.0
- pitch.gear_step_up = 1.5
- pitch.carrier_gear_mm = 40.0
- pitch.servo_gear_mm = 60.0
- pitch.servo_mass_g = 20.0
- pitch.actuator_count = 2
- pitch.carrier_torque_Nm = 0.1287
- pitch.servo_torque_Nm = 0.0965
- pitch.servo_stall_torque_Nm = 0.3825
- pitch.servo_torque_margin = 1.982
- structure.carrier_phase_jitter_deg = 0.1432
- pitch.side_force_tilt_deg = 9.078
- pitch.peak_lateral_force_N = 9.8252
- pitch.peak_blade_moment_Nm = 2.0967
- pitch.peak_link_force_N = 144.19
- packaging.mount_points = 4
- structure.centrifugal_load_N = 209.161
- structure.centrifugal_load_overspeed_N = 301.192
- structure.overspeed_factor = 1.2
- structure.blade_load_factor = 4.0
- structure.blade_root_bending_Nm = 0.8228
- structure.blade_allowable_Nm = 25.2528
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
- structure.pitch_link_load_N = 144.19
- structure.pitch_link_allowable_N = 474.074
- structure.pitch_link_margin = 3.2878
- structure.blade_windup_deg = 2.2346
- results.total_mass_g = 687.91
- results.mass_envelope_g = 647.23
- results.mass_g_conservative = 775.74
- results.weight_N = 6.7484
- results.thrust_to_weight = 2.5191
- results.bom_bought_inr = 40030
- results.bom_tooling_inr = 28800
- results.bom_total_inr = 68830
- results.bom_longest_lead_weeks = 4
