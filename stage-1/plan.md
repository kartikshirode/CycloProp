# CycloProp Stage 1 plan

**Deadline:** 27 September 2026, by email to pushpak_gc2026@aero.iitb.ac.in

## What Stage 1 actually wants

A preliminary cyclorotor design covering:

1. Configuration
2. Rotor sizing
3. Blade-pitch concept
4. Estimated thrust and weight
5. Manufacturing approach

That is the whole Stage 1 deliverable. **No CAD model, no CFD, no prototype.** The full CAE package with CAD, kinematic and aerodynamic analysis, structural assessment, material selection and a build-and-test plan is Stage 2, and only if you clear this gate.

This is why running CycloProp alongside UAV-X is workable. This one is reading, arithmetic and writing. UAV-X is coding and debugging. Different modes, so switching between them when one stalls is realistic in a way that two coding projects would not be.

## The number that constrains everything

Target is at least 10 N thrust with a thrust-to-weight ratio above 2.5.

Work the constraint backwards:

```
T / W > 2.5
W = m x g
10 N > 2.5 x m x 9.81
m < 10 / 24.525
m < 0.408 kg
```

So the entire rotor module, blades, spars, hub, pitch mechanism, motor and structure, has to come in **under roughly 408 g** while producing 10 N.

Every decision in the document traces back to that. State it on page 1, because it shows the evaluators you understood the brief as a coupled problem rather than two separate targets.

## Starting geometry from the literature

Published cyclorotor configurations worth building a comparison table from:

| Source configuration | Blades | Radius | Chord | Span | Pitch | Speed |
| --- | --- | --- | --- | --- | --- | --- |
| Optimised MAV cyclorotor | 6 | c/R = 0.67 | NACA 0015 symmetric | | 45 deg amplitude | 700 RPM |
| Aerodynamic study config | 4 | 150 mm | 80 mm | 200 mm | 45 deg | low speed |
| Small scale config | | 1.3 in | c/R = 0.8 | AR 1.62 elliptical | | 4000 RPM |

Useful findings to cite:

- Chord-to-radius around 0.5 gives higher efficiency, though 0.67 and 0.8 both appear in working designs
- Solidity depends on blade count and c/R, and as with conventional rotors there is an optimum solidity at each thrust level
- Blade aspect ratios of 1.181, 1.618 and 2.196 were tested; medium and high aspect ratio blades produced nearly identical thrust, so aspect ratio is not where your gains are
- Blades see a curvilinear flowfield, so chordwise velocity varies along the blade. Worth acknowledging, because it is why simple blade element estimates need caveating

## Physics for the thrust and power estimate

- Thrust scales with the square of rotational speed. Power scales with the cube.
- Measured power loading runs about 12 kgf/HP at low thrust and settles near 5 kgf/HP at high thrust.

Order of magnitude anchor for the power budget:

```
10 N = 1.02 kgf
At roughly 8 kgf/HP  ->  about 0.13 HP  ->  about 95 W
```

Treat that as a sanity check on motor and battery selection, not a result. The real number comes out of your sizing once blade count, c/R and RPM are fixed.

Scaling arguments to use in the document:

- CFD shows non-dimensional thrust holding roughly constant as Reynolds number rises, while non-dimensional torque and power fall. Cyclorotors scale up well aerodynamically.
- Blade weight per unit thrust stays constant with size, but blade stress climbs monotonically if geometry stays similar. That is the structural counterweight to the aerodynamic argument, and holding both at once is the design case worth making.

## Blade pitch mechanism

The concept is a required section and it is where designs differentiate. Two families:

- **Active**, servo-driven per blade. More control authority, more mass, more parts inside a 408 g budget.
- **Passive, cam-based.** There is published work on cam-based passive blade pitching for small-scale cyclogyros. Fewer parts, lighter, less authority.

Given the mass constraint, the passive route deserves the first look. Say why you chose whichever you chose. An unjustified choice reads worse than a conservative one.

## Schedule, 32 days

Dates assume a start of 26 August 2026. This runs in parallel with UAV-X, which is why the daily load here is deliberately light.

| Days | Dates | Goal | Done when |
| --- | --- | --- | --- |
| 1 to 7 | 26 Aug to 1 Sep | Literature | Parameter table built from every published cyclorotor you can find, with geometry against measured thrust |
| 8 to 14 | 2 to 8 Sep | Sizing | Blade count, c/R, aspect ratio and RPM fixed, thrust backed out and iterated to 10 N under 408 g |
| 15 to 20 | 9 to 14 Sep | Pitch mechanism | Active or passive chosen and justified, kinematics sketched |
| 21 to 26 | 15 to 20 Sep | Weight and manufacturing | Component-level mass budget summing under 408 g, plus how each part gets made |
| 27 to 31 | 21 to 25 Sep | Write | Document complete against all 5 required sections |
| 32 | 26 Sep | Submit | Emailed alongside UAV-X |

## Papers to pull first

- Jayant Sirohi, UT Austin, hover performance of a cycloidal rotor for a micro air vehicle. Closest to your scale.
- Moble Benedict and Inderjit Chopra, meso-scale cycloidal-rotor aircraft for MAV application.
- Carl Runco and Moble Benedict, 70 gram micro quad-cyclocopter, design, development and flight testing.
- Cam-based passive blade pitching for a small-scale cyclogyro.
- Chalmers parametric analysis of a large-scale cycloidal rotor, for the scaling argument.
- Quad cycloidal-rotor UAV development, for configuration context.

## Judging, and what it implies

Nine weighted criteria across thrust feasibility, thrust-to-weight ratio, kinematic design, aerodynamic analysis, structural design, manufacturability, CAD quality and presentation.

Manufacturability and CAD quality being scored explicitly matters even at Stage 1, where no CAD is required. It tells you the evaluators care about buildability over novelty. A conservative design with a credible manufacturing route beats an exotic one with hand-waved fabrication.

## Open item to resolve early

The live FAQ answers a question about "two objectives" by stating only one is given, then leaves an editorial note about confirming with the team before the FAQ goes out. That note is still on the site. Email and ask what the second objective was meant to be before you fix your scope, because it could change the sizing target.

## Eligibility check

The entry list names academic institutions, faculty-led student teams, startups, MSMEs and consortia. A student team is eligible but faculty backing helps here, both for framing and for Stage 2 tool access. Worth lining up a supervisor in week 1 rather than in October.

Mentors are Prof. Arnab Maity and Dr. Dhwanil Shukla, Aerospace Engineering, IIT Bombay.

Full rules in `../_shared-timeline.md`, competition detail in `../brief.md`.
