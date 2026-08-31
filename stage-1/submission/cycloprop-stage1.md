---
title: "CycloProp: a cyclorotor propulsion module for Stage 1"
subtitle: "PUSHPAK Grand Challenge, Stage 1 design report"
date: "Draft, week 3"
geometry: margin=25mm
fontsize: 11pt
toc: true
---

# About this draft

This is the week 3 smoke build. Items 1 to 4 carry the frozen week 2 and week 3 work. Items 5
and 6 are filled in week 4 and item 7 in week 5, and each says so where the content will go.
The purpose of building it now is to find the assembly problems in week 3 rather than in the
last four days, so the numbers below are the ones in `stage-1/design/numbers.json` and the
prose is a condensation of the design documents rather than a rewrite of them.

# Cyclorotor concept and configuration

One cycloidal rotor, 3 blades on a 110 mm radius, driven by a single motor through a toothed
belt. The blades run parallel to the rotation axis and pitch cyclically about a spanwise axis
at 30 percent chord, so the whole rotor produces a resultant force that can be steered in the
plane normal to its axis without changing anything about the airframe.

The single rotor was chosen against redesigned two and three rotor clusters on one common
model, with every contested assumption set in the cluster's favour. It wins on conservative
thrust to weight by 36 percent and it wins on every other metric as well, because splitting the
thrust splits the aerodynamics without splitting the hardware. Full argument and the mass
build-up for all three layouts are in `01-configuration.md`.

Module boundary, taken from the problem statement rather than chosen: blades, frame, pitch
mechanism, motor, actuator and mounting hardware. ESCs and mounting count in full.

# Preliminary rotor sizing

Radius 110 mm, chord 72.6 mm, span 290.4 mm, 3 blades, NACA 0020, pitch amplitude 40 degrees,
2405 rpm. Tip speed 27.70 m/s and chord Reynolds 134,074.

Solidity is 0.3151, inside the 0.30 to 0.40 band Kellen measured this shape family across, and
the design point sits inside the 100,000 to 300,000 Reynolds range of that same study. The
blade area coefficient is held at 0.6055 as deliberate reserve: every measured or corrected
value now available sits above it, at 0.6648 for Kellen's optimum rotor of this shape family
and 0.7211 for the corrected Benedict quad point.

Four thrust to weight cases are reported rather than one, because reporting a single case is
how this design misread itself for a fortnight.

| Case | Thrust | Mass | T/W |
| --- | --- | --- | --- |
| Design point | 18.00 N | 580.1 g | 3.163 |
| Mass downside alone | 18.00 N | 692.4 g | 2.650 |
| Coefficient downside alone | 17.10 N | 580.1 g | 3.005 |
| Both stacked | 17.10 N | 692.4 g | 2.517 |

All four clear the 2.5 requirement. The stacked case clears it by 4.8 g of mass, which is a
thin pass and is described as one.

# Blade arrangement and pitch-control concept

Three blades at 120 degrees, each on its own passive four-bar, all three sharing one offset
pivot 15.4 mm from the rotor axis. The offset link's length sets the pitch amplitude and its
direction sets the phase, so one linkage answers the pitching requirement and the vectoring
requirement together and no blade carries an actuator of its own.

Link lengths are 110.0 mm rotor arm, 15.4 mm offset link, 105.0 mm pitch link and 24.4 mm pitch
horn. Sorted, the shortest plus the longest is 125.4 mm against 129.4 for the other two and the
shortest link is the ground, so the four-bar is a double crank: the rotor arm turns fully and so
does the pitch link about the offset pivot. Transmission angle stays between 58.58 and 143.23
degrees and never approaches a dead centre.

The solved schedule reaches 40 degrees in both directions, closes on itself over the revolution
and lags the offset direction by 11.00 degrees. It is not a cosine: fitting one leaves an rms
residual of 1.1951 degrees, and that residual is where the side force comes from.

Thrust vectoring: two 12.5 g servos turn a phasing carrier through a 60 mm sector gear onto a
40 mm ring, a 1.5 step up on 80 degrees of servo travel, which gives 120 degrees of phase
authority. Direction follows command one to one in the model and the resultant magnitude holds
at 18.0 N across the range.

The measured side force is the open risk and it is stated as one. The model puts the resultant
11.98 degrees off the commanded direction. Published measurements run 10 to 35 degrees and rise
with rpm and blade count, so the model under-predicts and the design carries an indexed
mechanical bias plus actuator trim, at a worst case cost of 25 degrees of the 120.

Detail in `03-pitch-and-vectoring.md`, including the loop closure, the 37 row schedule, the
force vector map and the interference result that put the drive on one end.

# Estimated thrust and power requirement

Design thrust 18.0 N against a 10 N requirement, and 17.1 N on the conservative coefficient.
Power is closed three ways rather than asserted once.

Momentum theory over the projected frontal area of 0.0639 m2 gives an ideal induced power of
193.0 W, which no rotor beats. At Kellen's measured figure of merit of 0.6 that is 321.7 W of
blade aerodynamic power. An independent route through Benedict's measured power loading of
0.062 N/W gives 290.3 W, so the two agree to 9.8 percent.

Through a 0.93 belt, a 0.84 motor and a 0.95 ESC the rotor draws 481.7 W electrical, and the
module draws 489.7 W once the actuators and controller are added. The drive is a T-Motor
Antigravity MN5006 KV450 on 6S through a 3.5 to 1 belt, wanting 457.6 W at the motor terminals
against a 520.0 W continuous rating after an 0.80 derate on the published 180 second figure.

The azimuthal load model, rerun in week 3 against the solved schedule, gives a peak blade load
2.50 times the cycle mean. That is below the published 3 to 4 range, so week 4 sizes structure
on 4.0 rather than on this.

# Estimated module weight and thrust-to-weight ratio

Week 4 fills this item. The week 2 mass envelope stands underneath it: 13 component lines
totalling 580.05 g nominal and 692.43 g conservative, each line carrying its own basis and its
own conservative figure. Week 4 refines every line against a real section and a real bill of
materials, and each refined line names the envelope line it came from.

The target week 4 works to is the internal 2.75 from D17, which needs the conservative column
at 633.8 g against the 692.4 g it holds now. That is a margin target and not a requirement. The
requirement is 2.5 and the refined stacked case has to clear it.

# Initial material and manufacturing approach

Week 4 fills this item. The blade section carried into it is a closed cell: PMI foam core at
52 kg/m3, two plies of 60 gsm carbon twill skin and a CFRP spar tube, giving 29.4 g per blade
and 88.3 g for the set.

Week 3 hands this item two requirements. The blade centre of mass sits at 39.92 percent chord
against a pitch axis at 30 percent, and that unbalance doubles the peak blade pitching moment,
so a chordwise balance is a real trade with a real mass cost. And the pitch link carries 101.82
N at peak on the unbalanced blade, which is a strength case rather than a stiffness case.

# Team capability and execution plan

Week 5 fills this item, and only after a person has fixed the roster. Naming people or
institutions before that is fabrication, so the section is deliberately empty here rather than
populated with placeholders that read like names.

# Criteria map

| Criterion | Weight | Where it is answered |
| --- | --- | --- |
| 10 N thrust demonstrated | 15% | Item 4, thrust from geometry and a measured-family coefficient |
| Thrust-to-weight above 2.5 | 20% | Item 5, four cases, all clearing the limit |
| Kinematic design and thrust vectoring | 15% | Item 3, loop closure, solved schedule and force vector map |
| Aerodynamic reasoning | 15% | Item 4, momentum bound, figure of merit and a second power route |
| Structural feasibility | 15% | Item 6, blade section, centrifugal and aerodynamic load paths |
| Manufacturability | 10% | Item 6, materials and build route |
| Packaging and integration | 5% | `09-packaging-and-integration.md`, swept envelope and interfaces |
| Presentation quality | 5% | This document |

# Numbers used

- geometry.radius_m = 0.11
- geometry.chord_m = 0.0726
- geometry.span_m = 0.2904
- geometry.blades = 3
- geometry.pitch_amplitude_deg = 40.0
- operating.rpm = 2404.79
- operating.tip_speed_ms = 27.7012
- operating.reynolds = 134074.0
- performance.thrust_N = 18.0
- performance.thrust_N_conservative = 17.0992
- performance.blade_area_coeff = 0.6055
- performance.solidity = 0.3151
- performance.aero_power_W = 321.71
- performance.ideal_power_W = 193.026
- performance.figure_of_merit = 0.6
- performance.aero_power_W_published = 290.323
- performance.power_spread = 0.0976
- performance.electrical_power_W = 481.655
- performance.module_electrical_power_W = 489.655
- performance.momentum_area_m2 = 0.063888
- performance.motor_input_W = 457.573
- performance.belt_ratio = 3.5
- performance.blade_load_peak_to_mean = 2.501
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
- pitch.vector_range_deg = 120.0
- pitch.carrier_gear_mm = 40.0
- pitch.servo_gear_mm = 60.0
- pitch.servo_mass_g = 12.5
- pitch.actuator_count = 2
- pitch.side_force_tilt_deg = 11.978
- pitch.peak_link_force_N = 101.82
- pitch.blade_cg_pct_chord = 39.92
- packaging.envelope_length_mm = 364.4
- packaging.swept_diameter_mm = 296.1
- results.mass_envelope_g = 580.05
- results.mass_g_conservative = 692.43
- results.thrust_to_weight_conservative = 2.5173
