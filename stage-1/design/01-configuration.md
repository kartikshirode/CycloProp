# Configuration

Required Stage 1 item 1. This is the candidate configuration carried out of week 2. It is
not frozen: the conservative case does not clear thrust to weight 2.5, so the decision gate
in `stage-1/plan.md` holds the freeze. What follows is the layout the comparison chose and
the reasoning behind it, both of which stand whatever a person decides about the margin.

The module is one cyclorotor. Three blades, NACA 0020, chord at 0.66 of the radius, blade
aspect ratio 4, pitching plus or minus 40 degrees about an axis at 30 percent of chord. The
rotor turns on a through shaft carried in two bearing blocks, driven by one outrunner
through a single stage toothed belt. Blade pitch comes from a four-bar arrangement hung off
an offset ring, and thrust vectoring comes from rotating the direction of that offset, which
is week 3's problem.

At the design point the rotor is 230 mm across and 304 mm along the span, so the largest
dimension of the module is the span. That matters more than it sounds: a cyclorotor is a
rectangle, and the thing an integrator has to package is the span, not the diameter.

## Why this configuration

D2 said the module should be one larger rotor rather than a cluster, and it said so on thin
grounds. All it really established was that copying Benedict's 96 g six inch rotor five
times gives 485 g of rotor and nothing else. That rules out copying. It never ruled out a
cluster designed properly, and the decision has been carrying a "provisional" label since
week 1 waiting for this comparison.

So the comparison got run on one common model. Same thrust coefficient, same figure of
merit, same efficiency chain, same mass build-up, same module boundary. Each layout was
then swept over radius and the best conservative thrust to weight kept. Every assumption
that could go either way was set in the cluster's favour: wakes that never overlap, no
interaction penalty, one shared motor sized on total power, one shared controller, and the
same coefficient for all three even though splitting the thrust drops per-rotor Reynolds.

| Layout | Per rotor radius | Per rotor thrust | rpm | Reynolds | Blade area | Largest dimension | Module mass | Nominal T/W | Conservative T/W |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| single, 3 blades | 115 mm | 20.0 N | 2319 | 141,000 | 0.0691 m2 | 304 mm | 614 g | 3.318 | 2.389 |
| two rotors | 85 mm | 10.0 N | 2998 | 99,800 | 0.0755 m2 | 420 mm | 815 g | 2.501 | 1.795 |
| three rotors | 70 mm | 6.67 N | 3610 | 81,500 | 0.0768 m2 | 520 mm | 1019 g | 2.002 | 1.434 |

The single rotor wins on the first metric by a wide margin and on every other metric too. It
is smallest, it has the fewest parts, and it is the only one of the three whose per-rotor
Reynolds number stays inside the band the thrust coefficient was measured in. Two rotors
drop to 99,800 and three to 81,500, and D12 says a coefficient carried outside its measured
band has to be re-derived rather than carried across, so the cluster rows are flattered even
by their own numbers.

The reason is not subtle once the mass lines are sorted. Splitting the thrust does not split
the hardware. Each rotor still needs its own spider arms, hub bosses, pitch mechanism, offset
ring, through shaft, pair of main bearings, belt stage and pitch offset actuator, and the
frame has to grow sideways to hold them all. Total blade area actually rises when the thrust
is split, because smaller rotors run at lower tip speed for the same per-rotor thrust and
need more area to make it up. So the cluster pays twice, once in duplicated hardware and once
in blade area, and gets nothing back except a shorter span.

D2 is therefore confirmed, and this time on a like-for-like comparison rather than on a
rejected copy. Recorded as D18.

Three more configuration choices, each of which could reasonably have gone the other way.

**Three blades rather than four or six.** Benedict found that adding blades at constant chord
raises solidity and improves power loading, and that holding solidity fixed instead flips the
result so fewer blades give more thrust. Solidity is the quantity D12 gates, so it is the one
held fixed here, and that argues for fewer blades. Kellen's measured optimum for this
Reynolds band is 3 blades. Both point the same way.

**NACA 0020 rather than something thinner.** Kellen at UAV scale and Xisto at large scale
both support thick sections, and Kellen reports thickness up to 25 percent of chord staying
efficient while widening the usable pitch range. A thick section is also what makes the blade
buildable as a closed foam and skin cell with a real spar inside it, which is where the
bending and torsional stiffness comes from. Ramsey chose NACA 0015 at 25 kg, so the record
does not show thicker winning everywhere, and D14 already warns against claiming it does.

**One motor with a belt reduction rather than a direct drive or per-blade actuation.** Rotor
torque at the design point is 1.65 Nm at 2319 rpm. No outrunner in the mass class this module
can afford makes that torque directly, so the choice is between a reduction and a much
heavier motor. A single belt stage at 6 to 1 puts the motor at about 13,900 rpm and 21.7 A,
inside the 25 A continuous rating of the selected part. Per-blade servo pitching would remove
the linkage and add three actuators, which is the wrong trade on a module whose fixed hardware
is already 42 percent of its ceiling.

## What this configuration does not settle

The linkage geometry, the pitch schedule the four-bar actually produces, and the phase
authority available for vectoring are all week 3. The azimuthal load model in
`04-thrust-and-power.md` uses a prescribed sinusoidal pitch, and week 3 reruns it against the
solved schedule. Side force is the open question there. Benedict measured a resultant sitting
30 degrees off vertical on his twin, and Adams measured 15 to 35 degrees depending on
amplitude and rpm, so a claim about thrust magnitude that says nothing about direction is not
a finished claim.

## Numbers used

- geometry.radius_m = 0.115
- geometry.chord_m = 0.0759
- geometry.span_m = 0.3036
- geometry.blades = 3
- geometry.pitch_amplitude_deg = 40.0
- geometry.pitch_axis_pct_chord = 30.0
- operating.rpm = 2319.26
- operating.reynolds = 141327
- performance.thrust_N = 20.0
- performance.solidity = 0.3151
- performance.blade_area_m2 = 0.06913
- results.mass_envelope_g = 614.4
- results.thrust_to_weight_conservative = 2.3889
