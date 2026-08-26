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

**The table that used to sit here was wrong and has been deleted.** It came from search summaries rather than papers. The 700 rpm and 24 rpm figures had no source, the c/R values were scrambled between two different studies, and "1.3 in radius" was actually a 1.3 inch chord. Do not go looking for it in the git history and reuse it.

Rebuilt from the source PDFs in [literature.md](literature.md), which carries the geometry table, a status column saying which rows were actually read, the published mass breakdowns, and the findings that survived checking. Work from that file.

One thing worth repeating here because it shapes the whole sizing week. Blades see a curvilinear flowfield, so chordwise velocity varies along the blade and each point of the chord sits at its own angle of attack. That is why simple blade element estimates need caveating, and why the published analytical tools over-predict thrust away from their design point.

## Physics for the thrust and power estimate

- Thrust scales with the square of rotational speed. Power scales with the cube. Both measured, not assumed.
- Power loading runs about 12 kgf/HP at low thrust and settles near 5 kgf/HP at high thrust. Those two numbers come from Kim et al. 2003 at a Reynolds number near 260,000, so they are a scale extrapolation for us, not a match.

Anchor for the power budget:

```
10 N = 1.02 kgf
At the 5 kgf/HP asymptote  ->  0.204 HP  ->  152 W aerodynamic
Cross-check, Benedict's twin rotor at its operating point, 0.062 N/W  ->  161 W
At 65% chain efficiency  ->  roughly 230 to 250 W electrical
```

An earlier version of this plan said 95 W, taken from 8 kgf/HP in the middle of that range. That was too low by about 60%. 10 N is a high-thrust point, so read the asymptote rather than the middle. Working the other way, higher Reynolds number at our size should recover some of it, which is the one defensible reason to expect better than the measured MAV figures. Full derivation in [literature.md](literature.md).

Treat it as a sanity check on motor and battery selection, not a result. The real number falls out of the sizing once blade count, c/R and rpm are fixed.

Scaling arguments to use in the document:

- CFD shows non-dimensional thrust holding roughly constant as Reynolds number rises, while non-dimensional torque and power fall. Cyclorotors scale up well aerodynamically.
- Blade weight per unit thrust stays constant with size, but blade stress climbs monotonically if geometry stays similar. That is the structural counterweight to the aerodynamic argument, and holding both at once is the design case worth making.

## Blade pitch mechanism

The concept is a required section and it is where designs differentiate. Two families:

- **Active**, servo-driven per blade. More control authority, more mass, more parts inside a 408 g budget.
- **Passive, four-bar.** Every flying cyclocopter in the papers read so far uses this, none use per-blade servos.
- **Passive, cam-based.** Adams et al. drive the pitch off centrifugal force instead of a linkage, on a 535 g vehicle. Fewer parts again, and the paper is still paywalled.

The four-bar version is worth understanding before choosing, because it does more than the word "passive" suggests. The blade pitches about a fixed axis, driven by a pitch link attached aft of that axis, whose far end rides on a disk offset from the shaft centre. The size of that offset sets the pitching amplitude. Rotating the direction of the offset shifts the phase, which vectors the thrust, and that is the same adjustment used to cancel the 30 deg side-force tilt. So one passive linkage gives amplitude and direction control with no per-blade actuator, which is a strong answer to the mass constraint.

Given that, the passive route deserves the first look. Say why you chose whichever you chose. An unjustified choice reads worse than a conservative one.

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

## Papers

Pulled and read on 26 August, all recorded in [literature.md](literature.md):

- Sirohi, Parsons and Chopra, hover performance of a cycloidal rotor for a micro air vehicle. This is University of Maryland work from 2007, not UT Austin. Sirohi moved there later and his UT page hosts the PDF
- Benedict's 2010 UMD dissertation. The fullest parametric study at our kind of scale and the source of both the mass breakdowns and the side-force finding
- Xisto et al., parametric analysis of a large-scale cycloidal rotor, for the scaling argument
- Shrestha, Yeo, Benedict and Chopra, meso-scale cycloidal-rotor aircraft for MAV application

Still outstanding:

- The Texas A&M thesis on UAV-scale cyclorotor hover performance. It is the only study in our Reynolds band and the repository blocks direct requests, so it needs a library proxy or the faculty supervisor
- Cam-based passive blade pitching for a small-scale cyclogyro, Adams et al. Paywalled, and blade pitch is a required section
- Runco and Benedict, 70 gram micro quad-cyclocopter. Paywalled

## Judging, and what it implies

Nine weighted criteria across thrust feasibility, thrust-to-weight ratio, kinematic design, aerodynamic analysis, structural design, manufacturability, CAD quality and presentation.

Manufacturability and CAD quality being scored explicitly matters even at Stage 1, where no CAD is required. It tells you the evaluators care about buildability over novelty. A conservative design with a credible manufacturing route beats an exotic one with hand-waved fabrication.

## Open item to resolve early

The live FAQ answers a question about "two objectives" by stating only one is given, then leaves an editorial note about confirming with the team before the FAQ goes out. That note is still on the site. Email and ask what the second objective was meant to be before you fix your scope, because it could change the sizing target.

## Eligibility check

The entry list names academic institutions, faculty-led student teams, startups, MSMEs and consortia. A student team is eligible but faculty backing helps here, both for framing and for Stage 2 tool access. Worth lining up a supervisor in week 1 rather than in October.

Mentors are Prof. Arnab Maity and Dr. Dhwanil Shukla, Aerospace Engineering, IIT Bombay.

Full rules in `../_shared-timeline.md`, competition detail in `../brief.md`.
