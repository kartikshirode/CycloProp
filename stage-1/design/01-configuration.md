# Configuration

Required Stage 1 item 1. This is the frozen configuration for Stage 1, frozen at 18 N of design
thrust and a 110 mm radius by D30, with 120 mm carried as the insurance radius. The design case
clears thrust to weight 2.5 at 3.163 and each downside taken on its own clears it too. Since
D35 the stacked downside clears it as well, and on the week 4 refined mass budget it stands at
2.5457. What follows is the layout the comparison chose and the reasoning behind it.

The module is one cyclorotor. Three blades, NACA 0020, chord at 0.66 of the radius, blade
aspect ratio 4, pitching plus or minus 40 degrees about an axis at 30 percent of chord. The
rotor turns on a through shaft carried in two bearing blocks, driven by one outrunner through
a single stage toothed belt at 3.5 to 1. Blade pitch comes from a four-bar arrangement hung
off an offset ring, and thrust vectoring comes from rotating the direction of that offset,
which is week 3's problem.

At the design point the rotor is 220 mm across and 290 mm along the span, so the largest
dimension of the module is the span. That matters more than it sounds: a cyclorotor is a
rectangle, and what an integrator has to package is the span, not the diameter.

## Why this configuration

D2 said the module should be one larger rotor rather than a cluster, and it said so on thin
grounds. All it really established was that copying Benedict's 96 g six inch rotor five times
gives 485 g of rotor and nothing else. That rules out copying. It never ruled out a cluster
designed properly, and the decision has carried a provisional label since week 1 waiting for
this comparison.

So the comparison got run on one common model. Same thrust coefficient, same figure of merit,
same efficiency chain, same mass build-up, same module boundary, same drive shortlist and the
same derate on its ratings. Each layout was swept over radius from 55 to 180 mm in 5 mm steps
and the best conservative thrust to weight kept. Every assumption that could go either way was
set in the cluster's favour: wakes that never overlap, no interaction penalty, one shared motor
sized on total power, one shared controller, and the same coefficient for all three even though
splitting the thrust drops per-rotor Reynolds.

Packaging follows one stated rule, because the brief gives no maximum rotor size. Rotors sit
side by side in a plane, each with a 20 mm clearance allowance across its diameter, and the set
carries 40 mm of frame overhang. Module width is the rotor count times 2R plus 20 mm, plus 40
mm. Largest dimension is that width or the span, whichever wins.

| Layout | Per rotor radius | Per rotor thrust | rpm | Reynolds | Blade area | Largest dimension | Module mass | Nominal T/W | Conservative T/W |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| single, 3 blades | 110 mm | 18.0 N | 2405 | 134,000 | 0.0632 m2 | 290 mm | 580 g | 3.163 | 2.5457 |
| two rotors | 80 mm | 9.0 N | 3141 | 94,800 | 0.0669 m2 | 400 mm | 786 g | 2.334 | 1.855 |
| three rotors | 65 mm | 6.0 N | 3891 | 77,400 | 0.0663 m2 | 490 mm | 985 g | 1.863 | 1.479 |

The single rotor wins the first metric by 36 percent and every other metric as well. It is
smallest, and it has a third of the rotor hardware.

How the cluster masses are built, since a number nobody can reproduce is not evidence. Seven
lines multiply by the rotor count because each rotor needs its own: blades, spider arms and
hubs, pitch mechanism, through shaft, main bearings, belt stage and pitch offset actuator.
Three lines are shared once across the module: the motor, sized on total power, the controller
and the offset controller board. The frame takes two bearing blocks per rotor plus four tubes
spanning the full packaged width, and the wiring harness follows that width. A cross shaft
allowance of 12 g per extra rotor lets the shared motor reach them all. Nothing else changes.

The reason the cluster loses is not subtle once the lines are sorted that way. Splitting the
thrust splits the aerodynamics and does not split the hardware. Total blade area also rises,
because smaller rotors run at lower tip speed for the same per-rotor thrust and need more area
to make it up. So the cluster pays twice and gets a shorter span back.

One thing points the other way and is worth stating, because the audit caught this document
claiming the opposite. Per-rotor Reynolds falls as the thrust is split: 134,000 single, 94,800
at two rotors, 77,400 at three. Read against Shrestha's invariance range, which stops at
100,000, the cluster rows sit closer to the support than the single rotor does. Read against
Kellen, who measured this shape family from 100,000 to 300,000, the single rotor is the one
inside and both cluster rows fall below. D37 says why the second reading governs now. On
either reading the point is small, it is included in the comparison anyway, and it does not
come close to covering a 36 percent gap in the decision metric.

D2 is therefore confirmed, this time on a like-for-like comparison rather than on a rejected
copy. Recorded as D18.

Three more configuration choices, each of which could reasonably have gone the other way.

**Three blades rather than four or six.** Benedict found that adding blades at constant chord
raises solidity and improves power loading, and that holding solidity fixed instead flips the
result so fewer blades give more thrust. Solidity is the quantity D12 gates, so it is the one
held fixed here, and that argues for fewer blades. Kellen's reported optimum for this Reynolds
band is 3 blades. Both point the same way.

**NACA 0020 rather than something thinner.** Kellen at UAV scale and Xisto at large scale both
support thick sections, and Kellen reports thickness up to 25 percent of chord staying
efficient while widening the usable pitch range. A thick section is also what makes the blade
buildable as a closed foam and skin cell with a real spar inside it. Ramsey chose NACA 0015 at
25 kg, so the record does not show thicker winning everywhere, and D14 already warns against
claiming it does.

**One motor with a belt reduction rather than a direct drive or per-blade actuation.** Rotor
torque at the design point is 1.42 Nm at 2405 rpm. No outrunner in the mass class this module
can afford makes that torque directly, so the choice is between a reduction and a much heavier
motor. Per-blade servo pitching would remove the linkage and add three actuators, which is the
wrong trade on a module whose non-blade hardware already carries most of the mass.

## What this configuration does not settle

The linkage geometry, the pitch schedule the four-bar actually produces, and the phase
authority available for vectoring are all week 3. The azimuthal load model in
`04-thrust-and-power.md` uses a prescribed sinusoidal pitch, and week 3 reruns it against the
solved schedule. Side force is the open question there. Benedict measured a resultant sitting
30 degrees off vertical on his twin, and Adams measured 15 to 35 degrees depending on amplitude
and rpm, so a claim about thrust magnitude that says nothing about direction is not a finished
claim.

## Numbers used

- geometry.radius_m = 0.110
- geometry.chord_m = 0.0726
- geometry.span_m = 0.2904
- geometry.blades = 3
- geometry.pitch_amplitude_deg = 40.0
- geometry.pitch_axis_pct_chord = 30.0
- operating.rpm = 2404.79
- operating.reynolds = 134074
- performance.thrust_N = 18.0
- performance.solidity = 0.3151
- performance.blade_area_m2 = 0.06325
- performance.belt_ratio = 3.5
- results.mass_envelope_g = 580.05
- results.thrust_to_weight_conservative = 2.5457
