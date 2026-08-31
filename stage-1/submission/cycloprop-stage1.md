---
title: "CycloProp: a cyclorotor propulsion module"
subtitle: "PUSHPAK Grand Challenge, Stage 1 preliminary design report"
date: "Prepared 31 August 2026, for submission on 26 September 2026"
geometry: margin=25mm
fontsize: 11pt
toc: true
---

# Submission identity

Three lines a person completes before this report is sent. They are blank because no agent
working on this repository may write them.

| Field | Value |
| --- | --- |
| Team name and members | `[P-1]` to be completed |
| Institution | `[P-2]` to be completed |
| Registration reference | `[P-7]` to be completed |

Fill the three fields, rebuild the PDF, then send it.

- Attachment name: `cycloprop-stage1.pdf`
- Address: pushpak_gc2026@aero.iitb.ac.in

# Summary

One cycloidal rotor. 3 blades on a 110.0 mm radius, NACA 0020, pitching plus or minus 40
degrees about an axis at 30 percent chord, turning at 2405 rpm, driven by a single outrunner
through a toothed belt at 3.5 to 1. Design thrust is 18.0 N against a requirement of at least
10 N.

The module weighs 607.97 g at the nominal budget and 684.70 g in the conservative column, so
thrust to weight is 3.018 at the design point. Four cases are reported rather than one, because
reporting a single case is how this design misread itself for a fortnight early on, and the
worst of the four stacks a low thrust coefficient on the conservative mass and still gives
2.5457.

Blade pitch is passive. One four-bar per blade, all three sharing a single offset pivot 15.4 mm
from the rotor axis, and thrust vectoring is the direction of that offset rather than a separate
mechanism. Two 12.5 g servos turn a phasing carrier through a 1.5 step up and reach 120 degrees
of vector authority.

What this report is not: it is not a measurement, and it is not CAE. No CFD has been run, no
finite element model exists, nothing has been built and no coupon has been tested. Every load is
closed form, every allowable is a published class value and the thrust coefficient is
transferred from somebody else's rotor. Stage 1 asks for a preliminary design and this is one.
The sections that would be weak if it claimed more are marked, and the claims table near the end
carries every headline number with its confidence and its failure mode.

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
| single, 3 blades | 18.0 N | 2405 rpm | 290.4 mm | 580.05 g | 2.517 |
| two rotors | 9.0 N | 3215 rpm | 400.0 mm | 786.12 g | 1.855 |
| three rotors | 6.0 N | 3976 rpm | 490.0 mm | 984.94 g | 1.479 |

The single rotor wins the decision metric by 36 percent and it wins every other column too. The
reason is not subtle once the mass lines are sorted: splitting the thrust splits the aerodynamics
and does not split the hardware, since seven of the thirteen envelope lines multiply by the rotor
count while only three are shared. Total blade area also rises, because smaller rotors run at
lower tip speed for the same per rotor thrust. Chord Reynolds falls with the split too, from
134,074 on the single rotor to 94,805 and 77,408, which takes both cluster rows below the
measured band and the single rotor stays inside it.

Those three rows are built on the week 2 mass envelope, applied identically to all three layouts.
The refined budget later in this report moves the winning row from 2.517 to 2.5457 and leaves the
other two where they are.

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
rotor torque at the design point is 1.41944 Nm at 2405 rpm and no outrunner in this mass class
makes that directly.

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
| Rotor speed | 2405 rpm |
| Tip speed | 27.70 m/s |
| Chord Reynolds | 134,074 |
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
smaller rotor wants a belt ratio the selected motor cannot spin to on a 6S pack, and the motor
that has the speed does not have the torque. So the radius is the smallest one a named drive
holds continuously, which is a real finding and points at the cheapest available improvement.

# Blade arrangement and pitch-control concept

Three blades at 120 degree spacing, each on its own passive four-bar, all three sharing one
offset pivot. No blade carries an actuator. The offset link's length sets the pitch amplitude and
its direction sets the phase, so one linkage answers the pitching requirement and the vectoring
requirement together.

| Link | Length | What it is |
| --- | --- | --- |
| L1 rotor arm | 110.0 mm | input crank, frozen by the radius |
| L2 offset link | 15.4 mm | ground link, solved for the pitch amplitude |
| L3 pitch link | 105.0 mm | output crank |
| L4 pitch horn | 24.4 mm | coupler |

Only L2 was solved. Bisecting on peak to peak pitch travel gives 15.4 mm for plus or minus 40
degrees. L1 is the radius, and L3 and L4 come off a vehicle Kellen built, with L3 rescaled by a
sweep rather than by his ratio: his length scaled to this radius costs more than twice the
carrier torque and leaves the two servos holding on exactly half their stall figure, which is not
a margin.

**Grashof and the assembly mode.** Sorted, the links are 15.4 mm, 24.4 mm, 105.0 mm and 110.0 mm.
The shortest plus the longest is less than the other two added together, and the shortest link is
the ground, so this is a double crank: the rotor arm turns fully, which it has to, and the pitch
link turns fully about the offset pivot once per rotor revolution.

**Transmission angle runs 58.58 to 143.23 degrees.** The conventional band is 40 to 140 and the
obtuse end sits outside it, so the cost is stated rather than the band quoted: the worst sine
over the revolution is 0.599, meaning the mechanism's poorest moment arm is 60 percent of its
best. The nearest approach to a dead centre is 36.8 degrees away, so nothing is near a
singularity.

The solved schedule is 37 rows at 10 degree spacing. It reaches 40 degrees both ways, closes
exactly on itself over the revolution, and lags the offset direction by 11.00 degrees. Fitting a
cosine to it leaves an rms residual of 1.1951 degrees, which is 3 percent of amplitude. That
residual is not noise. It is where the side force comes from, and a prescribed sinusoid does not
have it.

**One geometric result set the whole drivetrain layout.** The pitch link passes within 0.004 mm
of the rotor axis, which is a crossing rather than a near miss, and it follows from the link set
rather than from bad luck. So the plane the pitch links sweep cannot contain the rotor shaft. The
shaft stops inboard of that plane, the rotor is driven from one end only, and the offset pivot is
fed by a post from a phasing carrier sitting outboard of everything that rotates with the rotor.
Clearance to the next blade is not close at 94.6 mm.

**Thrust vectoring.** The command is the direction of the offset link, and rotating it rotates the
whole pitch schedule rigidly. Two servos of the 12.5 g class drive a phasing carrier through
sector gears set 180 degrees apart, which doubles the holding torque and preloads the mesh so
backlash does not appear as thrust direction error. The servo gear is 60 mm and the carrier ring
gear is 40 mm, a 1.5 step up, so 80 degrees of servo travel becomes 120 degrees of carrier.

| Phase command | Vertical | Lateral | Resultant | Direction |
| --- | --- | --- | --- | --- |
| -60 degrees | 9.0 N | -15.5885 N | 18.0 N | -60 degrees |
| -30 degrees | 15.5885 N | -9.0 N | 18.0 N | -30 degrees |
| 0 degrees | 18.0 N | 0 N | 18.0 N | 0 degrees |
| 30 degrees | 15.5885 N | 9.0 N | 18.0 N | 30 degrees |
| 60 degrees | 9.0 N | 15.5885 N | 18.0 N | 60 degrees |

Direction follows command one to one and the magnitude holds across the range. Be clear about
why that comes out so clean: the rotor is axisymmetric, the blades are evenly spaced and the
inflow in this model is a uniform vector, so rotating the command rotates the entire solution
exactly. **That table is a statement about the model's symmetry and about what the mechanism can
reach. It is not a measurement of force at any of those commands.** What breaks it in hardware is
everything the model leaves out, and none of it is symmetric.

Holding torque peaks at 0.1389 Nm at three per revolution, 120 Hz, which is above any servo's
control bandwidth. Through the step up and across two servos that is 0.0463 Nm each against half
of a 0.216 Nm stall figure, a margin of 2.33, and the phase jitter is bounded by gear backlash at
0.1432 degrees of carrier rather than by the servo loop.

**Side force is the open risk in this section and it is stated as one.** The model puts the
resultant 11.978 degrees round from the offset direction, of which 11.00 comes from the linkage
phase delay and only 0.978 from the aerodynamics. Measurement says the aerodynamic part is much
larger. Sirohi measured about 10 degrees, Adams 15 to 35 depending on amplitude and rotor speed,
and Benedict's twin sat at 30 at its operating point. <!-- allow: published side force angles from three cyclorotor studies, and the trim residual worked in 03-pitch-and-vectoring.md; none of them is a value this design computes -->
A quasi steady model with uniform inflow has no wake return, no shed vorticity and no dynamic
stall hysteresis, and all three feed the lateral component, so under-prediction is the expected
failure and not a surprise.

The tilt is a bias rather than a loss, and the mechanism absorbs a known bias for free by
indexing the carrier zero at assembly. What the uncertainty costs is vectoring authority: indexed
at the centre of the measured band, the worst case residual comes out of the 120 degrees and
leaves the module with roughly four fifths of it. That is still a usable vectoring range and it
is the single largest consumer of authority in the design.

# Estimated thrust and power requirement

Design thrust is 18.0 N and the conservative case is 17.0992 N. Both clear the 10 N requirement
on their own. Thrust comes from the blade area coefficient route, `T = Ct x 0.5 x rho x u^2 x N x
c x s`, at a tip speed of 27.70 m/s over a blade area of 0.06325 square metres.

Choosing 18.0 N is arithmetic rather than ambition. The conservative case has to clear 10 N by
itself, which puts a floor under the nominal. Above that, the geometry scaled mass lines do not
care what thrust the rotor is turning for, so extra thrust buys mass ceiling while only the drive
grows. The trade runs out at 18.0 N, and it runs out because of the drive rather than the
physics.

| Design thrust | Mass ceiling at T/W 2.5 | Ideal power | Rotor speed | Rotor torque | Drive consequence |
| --- | --- | --- | --- | --- | --- |
| 13.0 N | 530 g | 118.474 W | 2044 rpm | 1.0251 Nm | the roomiest row, 12.65 A of 20.8 A |
| 16.0 N | 652 g | 161.766 W | 2267 rpm | 1.2617 Nm | 17.27 A of 20.8 A |
| 18.0 N | 733 g | 193.026 W | 2405 rpm | 1.4194 Nm | the design point, 20.61 A of 20.8 A |
| 20.0 N | 815 g | 226.075 W | 2535 rpm | 1.5772 Nm | nothing in the shortlist fits |

At 20.0 N the motor input is still inside the continuous power rating, so it is not a power
limit. It is torque and speed together: the rotor wants a ratio above 4 and a KV450 on 6S cannot
spin to the motor speed that implies.

**Power is closed three ways rather than asserted once.**

Momentum theory over the projected frontal area, 2R times span, gives an ideal induced power of
193.026 W for 18.0 N. No rotor beats that. At Kellen's measured figure of merit of 0.6 the blade
aerodynamic power is 321.71 W. An independent route through Benedict's measured power loading
puts the same thrust at 290.323 W, so two routes that share no equation agree to 9.8 percent.
Induced velocity is 10.7237 m/s against a tip speed of 27.70, an inflow ratio of 0.3871, and that
is high enough to be the main reason a simple model should not be trusted for magnitude.

| Term | Value | Where it comes from |
| --- | --- | --- |
| blade aerodynamic power | 321.71 W | ideal power over a figure of merit of 0.6 |
| rotor tare | 35.746 W | 10 percent of shaft power, measured on a flight weight rotor |
| motor input power | 457.573 W | shaft power through a 0.93 belt and a 0.84 motor |
| electrical power at the ESC input | 481.655 W | motor input over 0.95 |
| actuator draw | 6.0 W | two servos holding against residual link load |
| controller draw | 2.0 W | offset controller board |
| module electrical power | 489.655 W | the three above |

The three efficiencies are assumed rather than measured and they are the only unevidenced links
in the chain. The motor figure is the sensitive one.

**The drive, on a derated continuous rating.** The selected motor is a T-Motor Antigravity MN5006
KV450 at 106 g. Its published figures are a maximum power and a peak current over 180 seconds,
which is a three minute maximum and not a hover rating, so every rating in the shortlist is
derated by 0.80 before anything is selected against it. Nothing justifies 0.80 rather than 0.70
or 0.90 except ordinary practice, and the problem statement states no endurance requirement to
size it against. It is an assumption and it is marked as one.

A drive is accepted only if three things hold at once. Power: 457.573 W of a derated 520.0 W
continuous. Torque: 0.4361 Nm against 0.4414 Nm continuous at 3.5 to 1 through a 0.93 belt, which
is the tight one at 99 percent. Speed: the motor turns 8417 rpm and a 6S pack can reach 9435
against its internal resistance at the working current. Four other motors were screened and each
one fails at least one of the three.

**Azimuthal load distribution.** A cycle averaged coefficient hides what a blade actually sees, so
the load model runs 36 azimuths with a uniform induced inflow and the solved pitch schedule
rather than a prescribed sinusoid. Peak vertical force per blade is 15.0061 N against a cycle mean
of 6.0 N, so peak to mean is 2.501. That sits below the published 3 to 4 range, and the honest
reading is that the model under-predicts the peak rather than that this rotor is gentler than the
literature. Structure is sized on 4.0 regardless.

The cycle mean lateral force is trimmed to zero by pointing the offset off module vertical. The
instantaneous lateral force still reaches 10.0987 N per blade inside the revolution, which is a
bearing and frame load rather than a thrust loss.

# Estimated module weight and thrust-to-weight ratio

The module is 33 budget lines, every one a drawn section, a catalogue part or a stated allowance,
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
| rotor hub bosses, 2 off | 14.41 g | 16.14 g | machined |
| root attachment brackets, 6 off | 18.0 g | 20.16 g | machined |
| pitch bearings, 6 off | 7.8 g | 8.42 g | catalogue |
| pitch links with rod ends, 3 off | 12.28 g | 13.27 g | catalogue |
| pitch horns, 3 off | 6.58 g | 7.37 g | machined |
| offset pivot post and pin | 6.5 g | 7.28 g | machined |
| phasing carrier ring, 40 mm gear | 7.9 g | 8.85 g | machined |
| servo sector gear, 60 mm | 4.5 g | 5.04 g | machined |
| carrier support bearings, 2 off | 4.4 g | 4.75 g | catalogue |
| rotor shaft tube | 36.01 g | 41.41 g | calculated |
| shaft end plugs, 2 off | 17.24 g | 19.31 g | machined |
| main bearings, 2 off | 16.0 g | 17.28 g | catalogue |
| bearing blocks, 2 off | 16.0 g | 17.92 g | machined |
| frame tubes, 4 off | 46.36 g | 53.31 g | calculated |
| motor mount plate | 8.0 g | 8.96 g | machined |
| airframe mount lugs, 4 off | 7.2 g | 8.06 g | machined |
| frame and mount design reserve | 15.0 g | 18.75 g | allowance |
| motor, MN5006 KV450 | 106.0 g | 114.48 g | catalogue |
| rotor belt pulley, 56 tooth | 28.15 g | 31.53 g | machined |
| motor belt pulley, 16 tooth | 6.62 g | 7.41 g | machined |
| drive belt | 10.2 g | 11.02 g | catalogue |
| belt tensioner and bracket | 6.0 g | 6.72 g | machined |
| esc, 40 A 6S class | 19.5 g | 21.06 g | catalogue |
| vectoring actuator servos, 2 off | 25.0 g | 27.0 g | catalogue |
| pitch offset controller | 8.5 g | 9.18 g | catalogue |
| module wiring harness | 15.6 g | 19.5 g | allowance |
| fasteners and threaded inserts | 14.0 g | 17.5 g | allowance |
| structural adhesive at module joints | 7.5 g | 9.38 g | allowance |
| **module total** | **607.97 g** | **684.7 g** | |

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

**What is genuinely fixed in this module is one 8.0 g controller board.** That is worth saying
plainly, because the usual thrust to weight argument for a bigger rotor is that fixed hardware
amortises over more thrust. Sorted honestly, the wiring follows the envelope, the fasteners follow
the frame, the servo torque follows the pitch link load which follows thrust, and the bearings,
shaft and transmission follow rotor torque. Almost nothing here is free when the rotor grows.

| Case | Thrust | Mass | Weight | T/W |
| --- | --- | --- | --- | --- |
| design point | 18.0 N | 607.97 g | 5.9642 N | 3.018 |
| mass downside alone | 18.0 N | 684.7 g | | 2.680 |
| coefficient downside alone | 17.0992 N | 607.97 g | | 2.867 |
| both stacked | 17.0992 N | 684.7 g | | 2.5457 |

All four clear the requirement. The stacked row is the one that matters, since it applies the low
coefficient and the conservative mass at the same time, and it clears by 12.5 g of mass. That is
a real pass and a thin one, and it is described as thin rather than rounded up.

An internal target of 2.75 on the stacked case was set early as a margin goal. It is not met, it
is not claimed anywhere, and no further pass over the budget closes it: every remaining line is a
drawn section or a catalogue part, and trimming one to reach a number is exactly the move the
budget rules exist to stop. The two routes that would close it are a lower KV motor on more cells
and a measured thrust coefficient, and both are Stage 2 work.

One trade was priced and declined. Balancing the blade chordwise would lift the pitch link
margin from 3.30 to 4.69, and the nose ballast that needs across three blades takes the stacked
case to 2.406, under the hard limit. Spending a requirement
to improve a margin that already passes twice over is the wrong trade, so the blade stays
unbalanced and the load path carries it.

# Initial material and manufacturing approach

Six materials carry load and each one was chosen because a structural calculation needed an
allowable. They are defined once, in the solver, and both the structures work and this section
cite that definition rather than restating it.

| Material | Where | The margin it decides |
| --- | --- | --- |
| Rohacell 51 IG class PMI foam, 88 percent fill | blade core | blade bending, through skin wrinkling |
| 60 gsm carbon twill, 2 plies | blade skin | blade bending, 2.83 and 1.97 |
| roll wrapped CFRP tube | spar, pitch links, rotor shaft, frame tubes | shaft torsion 17.58, combined 9.44 |
| 7075-T6 aluminium | horns, root fittings, brackets, blocks, lugs | pitch link path, 3.30 |
| 6061-T6 aluminium | pulleys, carrier ring gear, sector gear | none, these are stiffness parts |
| Araldite 2011 class epoxy paste | shaft plugs, root fittings, block bonds | none yet, and that is stated |

**The foam is structural here and not a filler.** Skin wrinkling over a soft core is what limits
the blade, and the wrinkling stress depends on the skin modulus and both core moduli, two of the
three belonging to the foam. Drop to a lighter grade and the wrinkling stress falls by roughly a
quarter, which takes the blade's combined margin at overspeed under its floor. The grade is part
of the structure and a substitution means a recalculation.

## Structural design and margins

This is the 15 percent structural criterion and it belongs with the material choice, because each
allowable is what makes a margin real.

**The headline is that this rotor is a centrifugal machine before it is an aerodynamic one.** Each
blade pulls 221.464 N radially at the design point, and at a declared 1.20 overspeed that becomes
318.908 N, because centrifugal load goes as the square of speed. Mean aerodynamic force per blade
is 6.0 N and structure is sized on 4.0 times that. The ratio between the two loads is 9.2 here,
where Runco measured 4.4 on a much smaller rotor.

| Case | Demand | Allowable | Margin |
| --- | --- | --- | --- |
| blade bending, aerodynamic only | 0.8712 Nm | 25.2528 Nm | 28.99 |
| blade bending, aerodynamic and centrifugal | | 25.2528 Nm | 2.83 |
| blade bending at 1.20 overspeed | | 25.2528 Nm | 1.97 |
| rotor shaft torsion | 1.41944 Nm | 24.9563 Nm | 17.58 |
| rotor shaft, bending and torsion combined | 2.22965 Nm of bending | | 9.44 |
| pitch link path, the horn governs | 105.93 N | 349.727 N | 3.30 |
| blade attachment, centrifugal | 221.464 N | 540.0 N | 2.44 |
| blade attachment at 1.20 overspeed | 318.908 N | 540.0 N | 1.69 |

The spread is the point. Two margins sit under 2 and everything else is over 3, so the module is
sized by the blade in combined bending and by the blade attachment, and Stage 2 effort belongs at
those two joints rather than at the shaft or the frame. The blade's own section allowable is set
by skin wrinkling over the foam and not by the laminate, and the spar would take more than twice
the section's rating on its own.

**The attachment is the tightest joint and the number is not the worst part of it.** The two pitch
bearings that carry each blade give 540.0 N together and see 318.908 N at overspeed. They
oscillate through 80 degrees under a steady load rather than rotating, which is a fretting duty
that a static rating describes not at all. It needs a supplier's oscillating derate or a bench
test, and it has neither.

**Blade stiffness came out fine in bending and interesting in torsion.** Tip deflection under the
peak blade load is 0.0936 mm and twist under the aerodynamic pitching moment is 0.0145 degrees,
so neither is a design driver. The blade is driven in pitch from one end though, so the
centrifugal pitching moment on an unbalanced blade has to go through the blade's own torsional
stiffness, and 2.2058 Nm winds the far end up by 2.3509 degrees. That is 4 percent of the pitch
amplitude, and it is most of the 5 percent blade flexibility allowance the conservative
coefficient carries. The allowance had a bound over it before and has a calculation under it now.

The reaction torque path is blade, spider arm, hub, through shaft, main bearing, bearing block,
frame tube, mount lug. The rotor shaft carries 1.41944 Nm and the motor shaft 0.43608 Nm, and the
airframe sees the rotor figure as a steady moment about the rotor axis whenever the module makes
thrust. Both bearing blocks take it, which is why they sit on the frame tubes rather than on side
plates, and there are 4 mount points rather than 3 because a three point mount puts that torque
into a triangle whose worst leg carries most of it.

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

**What gets measured before it spins**, because a rotor at 2405 rpm with 221.464 N pulling on
every blade is not a thing to power up hopefully. Blade masses matched across the set, shaft
journal run out on the jig, and pitch angle checked against the solved schedule at 12 azimuths by
hand, where peak to peak travel is what matters because the rod ends can correct it. Then the
rotor turned by hand through two revolutions at both ends of servo travel, watching for a link
going over centre, since the worst transmission angle is 143.23 degrees and it wants feeling
rather than assuming. Then a static pull on one attachment above the overspeed load of 318.908 N,
and a first spin staged in four steps with current logged against prediction.

Bought parts and material come to 36970 INR, tooling and fabrication to 28800, and the module
totals 65770 INR at a longest single lead of 4 weeks. **These are indicative prices at
distributor list level and they are not obtained quotations.** No supplier was contacted, and the
source column of the full bill of materials names the distributor a part would be bought from
rather than one that has quoted for it. Five lines above 4500 INR carry 52 percent of the total
and those are what Stage 2 has to replace with written quotes.

The schedule driver is a 4 week foam import with no Indian source. Everything on a 3 week lead
sits inside that window, so ordering the foam first is the whole mitigation. If it slips, a
lighter core is not a drop in substitute, because the wrinkling calculation depends on the core
moduli, and the fallback is a thicker skin and a rerun.

# Team capability and execution plan

**This section is deliberately incomplete and the reason is worth stating.** The people, the
institution, the prior projects and the tool licences behind this entry are facts about a team,
and no part of the automated work that produced this report may write them. The structure below
is real, the gap analysis is real, and the fields marked `[P-n]` are for a person.

Roster: `[P-1]` `[P-2]`. One person as of 27 August 2026. Team size is capped at 5 and nothing in
Stage 1 needed more than one, though the two solver workstreams in Stage 2 are where a second
person would first pay for themselves.

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
on 1 December. All 11 Stage 2 items are scheduled, with the tool category each one needs, what it
waits on and the gate that closes it.

| Weeks | Stage 2 items | Closed when |
| --- | --- | --- |
| 1 to 2 | CAD model of the module, and supplier quotations started | every budget line exists as a solid and the model's mass properties reproduce the budget |
| 2 to 3 | kinematic model, then motor, actuator, bearing and controller selection | the multibody schedule matches the closed form one and reproduces the pitch link load |
| 4 to 5 | aerodynamic analysis for thrust prediction | a converged run at the design point with mesh and timestep independence shown |
| 6 | structural analysis of blades, supports, frame, shaft and linkages | the 8 margins reproduce or move, with every difference explained |
| 7 | material selection, mass estimate and thrust to weight | cured laminate modulus measured on a panel built the way the blade is built |
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
| Feasibility of achieving 10 N thrust | 15% | Item 4, thrust from geometry and a coefficient measured on this shape family |
| Feasibility of thrust-to-weight above 2.5 | 15% | Item 5, a 33 line budget and four cases, all clearing the limit |
| Kinematic design of blade-pitch and thrust-vectoring mechanism | 15% | Item 3, loop closure, solved schedule, Grashof and the force vector map |
| Aerodynamic analysis or simulation quality | 15% | Item 4, momentum floor, figure of merit, a second power route and an azimuthal model |
| Structural design and strength assessment | 15% | Item 6, two load cases, 8 margins and the analyses not done |
| Manufacturability, material selection and cost realism | 10% | Item 6, per part process and tolerance, assembly order and a costed bill of materials |
| CAD quality, integration readiness and packaging | 5% | Item 1 and item 6, swept envelope, interfaces and mounts, without CAD at this stage |
| Presentation, viva and technical clarity | 10% | This report, the claims table below and the examiner questions in appendix A |

# Claims, evidence and risk

Every headline claim, what produced it, how much weight it carries, what would break it and what
Stage 2 does about that.

| Claim | Where it comes from | Confidence | Main failure mode | Stage 2 validation |
| --- | --- | --- | --- | --- |
| Blade area coefficient 0.6055 gives 18.0 N | transferred from a recomputed hover point, bracketed above by 0.6648 measured on this shape family | medium | the transfer is wrong in the unsafe direction, or the model overstates thrust at an inflow ratio of 0.3871 | transient CFD, then a load cell run |
| Module mass 607.97 g nominal, 684.7 g conservative | 33 drawn or catalogue lines, growth by line class | medium to high | a wet layup blade comes out heavy, or undrawn frame parts eat the 15.0 g reserve | CAD mass properties, a mould trial, weighed parts |
| Blade deflection 0.0936 mm, wind up 2.3509 degrees | closed form beam and torsion on the integrated section | medium | cured laminate modulus below the published class value | coupon panel, then FEA |
| Direction follows the vector command one to one at 18.0 N | model symmetry, not measurement | low on magnitude | wake skew, the frame in the flow, the blade meeting its own wake | two axis load cell across the range |
| Stacked conservative thrust to weight 2.5457 | recomputed from geometry and the mass lines | medium | either input moving, since it clears by 12.5 g | items 3, 6 and 7 together |
| Blade attachment margin 1.6933 at overspeed | static rating over recomputed centrifugal load | low | an oscillating fretting duty that a static rating does not describe | oscillating derate or a bench test |
| Peak to mean blade load 4.0 | published simulated range, top of it taken | low to medium | the true peak is higher under dynamic stall | measured blade forces, or CFD |
| Module electrical power 489.655 W | momentum floor, figure of merit, efficiency chain | medium | all three efficiencies are assumed and the motor one is sensitive | bench measurement on the built module |
| The drive holds the design point continuously | derated ratings against power, torque and speed | medium | the 0.80 derate has no source and torque sits at 99 percent | datasheets, then a thermal run |
| Side force tilt 11.978 degrees | quasi steady model with uniform inflow | low | measurement puts it far higher and it moves with rotor speed | load cell calibration across the speed range |
| Module cost 65770 INR, longest lead 4 weeks | distributor list prices, nothing quoted | low on price | gear cutting is priced by setup at a quantity of one | written quotations |
| Material allowables | published typical values per class | medium | no certificate, no coupon, and the skin modulus is what the blade turns on | coupon panel and a bond shear coupon |

# Sources and how they were read

Five evidence classes are used: measured, somebody measured this quantity on this configuration
and the figure was read off the source; derived, computed here from figures measured on a
different configuration; transferred, a derived value carried across a change of geometry or
Reynolds number; summary, only a summary of the source has been read; assumed, no source at all.

**Nobody has put this rotor on a load cell.** Where this report says measured, it means measured
by somebody else on a rotor of this shape family, and the distinction is kept everywhere it
matters.

- **Kellen 2019**, MS thesis, Texas A&M. Read as a machine text extract of the full PDF, which is
  held in the repository along with the hash and a working re-fetch URL. Source of the figure of
  merit, the solidity band, the Reynolds range and the 0.6648 coefficient measured on this shape
  family
- **Benedict 2010**, PhD dissertation, University of Maryland. Read the same way. Source of the
  nominal coefficient's provenance, the corrected quad hover point, the power loading cross check
  and the rotor tare fraction
- **Sirohi, Parsons and Chopra 2007**, read. **Xisto et al. 2016**, read. Both support the
  configuration choices rather than any stored number
- **Shrestha and Benedict**, JAHS 2022, summary class. It carries the Reynolds invariance claim
  and the blade mass scaling argument, and it is cited as a summary
- **Adams et al. 2013** and **Alsabri et al. 2025**, summary class. The side force band and the
  peak to mean load range come from them and are labelled
- **Runco and Benedict 2023**, open access, re-cut onto this competition's module boundary to give
  the benchmark this design is argued against
- **Ramsey 2022** and **Heimerl et al.** are **not read**. Neither is cited as evidence anywhere in
  this report. Ramsey would give a second structural mass anchor, and Heimerl measured
  instantaneous blade forces across a Reynolds band that brackets this design, which would replace
  both the peak to mean estimate and the side force angle with measurements

No figure or table has been reproduced from any source. Every published number used here was
recomputed into this project's own conventions from figures printed in the source, and the
conversion is recorded in the evidence ledger alongside the printed page it came from.

# Appendix A: examiner questions

Twelve questions this design should expect, answered short. Where an answer exposed a gap, the
report was changed rather than the answer smoothed.

**1. Your whole design hangs off a thrust coefficient measured on a different rotor. Why should
anyone believe 18.0 N?** They should believe the conservative case first. The nominal 0.6055 is
transferred, and its original provenance was wrong, so it was recomputed from the printed pages
and the corrected value is 0.7211, higher than what is used. Kellen then measured 0.6648 on a
rotor whose solidity and chord to radius are within 1.1 percent of this one. Three independent
values sit above the number the design is built on. That is the argument, and it does not make
18.0 N a measurement. The claim is that the design closes on a coefficient deliberately below the
evidence, and the requirement is 10 N.

**2. The published benchmark for a module like this is between 1.78 and 2.13 depending on
allocation. You claim 2.5457. Why is that credible?** Because the benchmark is a 70 gram
micro-scale vehicle re-cut onto this boundary, and blade mass per newton is roughly scale
invariant while the drive and structure are not. This module makes 18.0 N from one motor, one
belt, one shaft and one pitch mechanism, where the benchmark makes a fraction of that per rotor
from four sets of hardware. The gap is not a claim to have beaten anybody at the same scale. It
is amortisation, and the report is careful about how little of it is real: the genuinely fixed
mass in this module is one 8.0 g board.

**3. What in the module is actually fixed as the rotor grows?** Almost nothing. The 8.0 g
controller. Wiring follows the envelope, fasteners follow the frame, servo torque follows the
pitch link load which follows thrust, and the shaft, bearings and transmission follow rotor
torque. This is stated in item 5 because it is the weakest part of the usual argument for a large
single rotor and hiding it would be worse than losing the point.

**4. Why 110.0 mm and not the radius your own sweep prefers?** The sweep prefers smaller. A
smaller rotor is lighter on every geometry scaled line and conservative thrust to weight rises
all the way down. What stops it is the drive: below this radius the rotor torque wants a belt
ratio the KV450 cannot spin to on 6S, and the motor with the speed lacks the torque. So 110.0 mm
is the smallest radius a named drive holds continuously. If a lower KV motor on more cells were
available, that is where the design would go next.

**5. Your motor sits at 99 percent of its continuous torque and the derate has no source. Is that
a design or a hope?** It is a judgement, stated as one. T-Motor publishes a maximum over 180
seconds, which is not a hover rating, so every shortlist figure is cut to 0.80 before selection.
Nothing supports 0.80 over 0.70 or 0.90 except practice, and the problem statement gives no
endurance requirement to size it against. At the derated figure the design point takes 457.573 W
of 520.0 W and 0.4361 Nm of 0.4414 Nm, so power has room and torque does not. A thermal run on
the bench is what settles it, and it is in the Stage 2 plan.

**6. Where does the reaction torque go?** Blade, spider arm, hub, through shaft, main bearing,
bearing block, frame tube, mount lug. The rotor shaft carries 1.41944 Nm and the motor shaft
0.43608 Nm upstream of the belt, and the report says which is which because that is the first
thing a reviewer checks. The airframe sees the rotor figure as a steady moment whenever the
module makes thrust, both bearing blocks react it, and the mount has 4 points rather than 3 for
exactly that reason.

**7. Your transmission angle reaches 143.23 degrees, outside the conventional band. How close is
this mechanism to a singularity?** Not close. The conventional band is 40 to 140 and the obtuse
end sits just outside it, which costs moment arm rather than control: the worst sine over the
revolution is 0.599, so the poorest moment arm is 60 percent of the best. The nearest approach to
a dead centre is 36.8 degrees. The linkage is a double crank by the Grashof test, both cranks
turn fully, and the assembly is checked by hand through two revolutions at both ends of servo
travel before first spin.

**8. Your vector map shows constant 18.0 N at every command. Real rotors do not do that. Is the
table a measurement?** No, and the report says so in bold in item 3. The rotor is axisymmetric,
the blades are evenly spaced and the inflow in this model is uniform, so rotating the command
rotates the whole solution exactly. The table is a statement about model symmetry and about the
commands the mechanism can reach, nothing more. Wake skew, the frame and shaft supports sitting
in the flow on one side, and the blade passing through its own returning wake all break that
symmetry and none of them is symmetric. A two axis load cell across the command range is the
measurement that replaces it.

**9. Is the blade stiff enough, and how do you know without FEA?** In bending, comfortably, and
the numbers are small enough that FEA would not change the answer: 0.0936 mm of tip deflection
under peak blade load and 0.0145 degrees of aerodynamic twist against a 40 degree amplitude. The
one that matters is torsion. The blade is pitched from one end, so the centrifugal pitching
moment of 2.2058 Nm on an unbalanced blade winds the far end up by 2.3509 degrees, about 4
percent of amplitude. That is most of the 5 percent flexibility allowance the conservative
coefficient carries, so the allowance now has a calculation under it instead of being a chosen
floor. Driving the blade from both ends would roughly quarter it and costs hardware the mass
budget has no room for.

**10. Your side force model gives about 1 degree of aerodynamic tilt and the literature measures
tens of degrees. Why publish it?** Because it is the honest output of a quasi steady model with
uniform inflow, and because the difference is explainable rather than mysterious: that model has
no wake return, no shed vorticity and no dynamic stall hysteresis, and all three drive the
lateral component. The stored figure is carried as a lower bound and labelled one. The design
handles the tilt as a bias rather than a loss, since indexing the phasing carrier zero at
assembly costs no actuator range, and the uncertainty in the bias is what costs range. It is the
largest single consumer of vectoring authority in the design.

**11. What is the tightest thing in the module?** The blade attachment at overspeed, at 1.6933,
and the duty is worse than the number. Two pitch bearings per blade give 540.0 N against 318.908
N, but they swing through 80 degrees under a steady load rather than rotating, and a static
rating says nothing about fretting. That is why the overspeed case is declared at all: at the
design point the same joint reads 2.44 and looks comfortable.

**12. What is the first test you run in Stage 2?** A coupon panel, laid up the way the blade is
laid up, for cured laminate modulus and areal mass. It is cheap, it is fast, and the blade
allowable turns on the skin modulus more than on anything else, so a 15 percent shortfall there
moves the margin that sizes the module. Second is a static pull on one blade attachment above the
overspeed load of 318.908 N. The rotor does not spin until both have passed.

# Appendix B: numbers and provenance

Every number in this report is defined once, in `stage-1/design/numbers.json`, and the prose
cites it rather than restating it. A gate script recomputes the physics from the stored geometry
and the mass lines, applies the competition limits to what it recomputed rather than to any
stored headline, and fails on disagreement. It also audits this document: every number in the
narrative carrying a physical unit has to match a computed value in the same dimension.

## Numbers used

- performance.thrust_N = 18.0
- geometry.radius_m = 0.11
- results.thrust_to_weight_conservative = 2.5457
- geometry.chord_m = 0.0726
- geometry.span_m = 0.2904
- geometry.blades = 3
- geometry.pitch_amplitude_deg = 40.0
- geometry.pitch_axis_pct_chord = 30.0
- operating.rpm = 2404.79
- operating.tip_speed_ms = 27.7012
- operating.reynolds = 134074.0
- performance.thrust_N_conservative = 17.0992
- performance.blade_area_coeff = 0.6055
- performance.blade_area_coeff_low = 0.5752
- performance.blade_deflection_thrust_loss = 0.05
- performance.solidity = 0.3151
- performance.blade_area_m2 = 0.06325
- performance.aero_power_W = 321.71
- performance.ideal_power_W = 193.026
- performance.figure_of_merit = 0.6
- performance.aero_power_W_published = 290.323
- performance.power_spread = 0.0976
- performance.tare_power_W = 35.746
- performance.electrical_power_W = 481.655
- performance.module_electrical_power_W = 489.655
- performance.actuator_power_W = 6.0
- performance.controller_power_W = 2.0
- performance.induced_velocity_ms = 10.7237
- performance.inflow_ratio = 0.3871
- performance.blade_load_peak_to_mean = 2.501
- performance.motor_input_W = 457.573
- performance.motor_rpm = 8416.8
- performance.motor_torque_Nm = 0.4361
- performance.motor_input_current_A = 20.611
- performance.belt_ratio = 3.5
- performance.blade_tip_deflection_mm = 0.0936
- performance.blade_twist_deg = 0.0145
- efficiency.transmission = 0.93
- efficiency.motor = 0.84
- efficiency.esc = 0.95
- pitch.offset_m = 0.0154
- pitch.pitch_link_m = 0.105
- pitch.horn_m = 0.0244
- pitch.phase_delay_deg = 11.0
- pitch.schedule_rms_residual_deg = 1.1951
- pitch.transmission_angle_min_deg = 58.58
- pitch.transmission_angle_max_deg = 143.23
- pitch.axis_keepout_mm = 0.004
- pitch.neighbour_clearance_mm = 94.6
- pitch.pitch_bearing_travel_deg = 80.0
- pitch.vector_range_deg = 120.0
- pitch.phase_authority_deg = 120.0
- pitch.servo_travel_deg = 80.0
- pitch.gear_step_up = 1.5
- pitch.carrier_gear_mm = 40.0
- pitch.servo_gear_mm = 60.0
- pitch.servo_mass_g = 12.5
- pitch.actuator_count = 2
- pitch.carrier_torque_Nm = 0.1389
- pitch.servo_torque_Nm = 0.0463
- pitch.servo_stall_torque_Nm = 0.216
- pitch.servo_torque_margin = 2.332
- structure.carrier_phase_jitter_deg = 0.1432
- pitch.side_force_tilt_deg = 11.978
- pitch.peak_lateral_force_N = 10.0987
- pitch.peak_blade_moment_Nm = 2.2058
- pitch.peak_link_force_N = 105.93
- packaging.mount_points = 4
- structure.centrifugal_load_N = 221.464
- structure.centrifugal_load_overspeed_N = 318.908
- structure.overspeed_factor = 1.2
- structure.blade_load_factor = 4.0
- structure.blade_root_bending_Nm = 0.8712
- structure.blade_allowable_Nm = 25.2528
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
- structure.pitch_link_load_N = 105.93
- structure.pitch_link_allowable_N = 349.727
- structure.pitch_link_margin = 3.3015
- structure.blade_windup_deg = 2.3509
- results.total_mass_g = 607.97
- results.mass_envelope_g = 580.05
- results.mass_g_conservative = 684.7
- results.weight_N = 5.9642
- results.thrust_to_weight = 3.018
- results.bom_bought_inr = 36970
- results.bom_tooling_inr = 28800
- results.bom_total_inr = 65770
- results.bom_longest_lead_weeks = 4
