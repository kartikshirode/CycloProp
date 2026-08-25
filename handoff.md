# CycloProp handoff

Written 26 August 2026. Stage 1 is due **27 September 2026**, so there are 32 days. This file is where a fresh session starts; everything else links from here.

## What this is

PUSHPAK Grand Challenge 2026, Grand Challenge on advanced UAV propulsion. Design an indigenous cycloidal rotor module for drones, targeting at least 10 N thrust with a thrust-to-weight ratio above 2.5. The brief is explicit that the goal is **not fabrication**. It is identifying strong, build-ready designs.

Funded by MeitY under the national drone mission, hosted by IIT Bombay. Mentored by Prof. Arnab Maity and Dr. Dhwanil Shukla, Aerospace Engineering, IIT Bombay. Prize ceiling is INR 25,50,000 across the whole staged programme.

Read [brief.md](brief.md) for the full competition rules, then [stage-1/plan.md](stage-1/plan.md) for the work plan. Shared track rules are in [_shared-timeline.md](_shared-timeline.md), compute notes in [_compute.md](_compute.md), and the first plan review in [_plan-review-round1.md](_plan-review-round1.md).

Repo: github.com/kartikshirode/CycloProp. This project is its own repository and does not share a session with UAV-X.

## Where we are

Planning only. Nothing researched, sized or written. Round 1 of the plan cross-check is done and found 8 issues, two of which land squarely on this project. Round 2 by Codex has not happened yet.

## Stage 1 deliverables

To `pushpak_gc2026@aero.iitb.ac.in`, same inbox as UAV-X, no portal.

A preliminary cyclorotor design covering:

1. Configuration
2. Rotor sizing
3. Blade-pitch concept
4. Estimated thrust and weight
5. Manufacturing approach

**No CAD model, no CFD, no prototype.** All of that is Stage 2, and only if this gate clears. That asymmetry is why running this alongside UAV-X is realistic: this one is reading, arithmetic and writing, while UAV-X is coding and debugging.

Plan sends on 26 September, a day early.

## Two things to settle before any sizing starts

### 1. The mass budget rests on an unverified reading

Working the target backwards:

```
T / W > 2.5,  T = 10 N
W < 10 / 2.5 = 4 N
m < 4 / 9.81 = 0.408 kg
```

So the whole module, blades, spars, hub, pitch mechanism, motor and structure, comes in under roughly **408 g**.

The arithmetic is right. The premise is not confirmed. The brief says "cycloidal rotor module for drone applications, targeting at least 10 N thrust and a thrust-to-weight ratio greater than 2.5", and that T/W could be module-level or aircraft-level. If it is aircraft-level, the module has to be far lighter, because it is also carrying airframe, battery, avionics and payload. This changes the design target enough that sizing should wait on an answer. Until then, size against both readings.

### 2. The literature table in the plan is not trustworthy yet

The starting geometry currently in [stage-1/plan.md](stage-1/plan.md) came from search-result summaries, not from the source PDFs. The 700 RPM figure looks low for that scale and the 24 RPM one is almost certainly a stripped or misread value, since a cyclorotor at 24 RPM produces essentially nothing.

**Treat nothing in that table as usable until it has been checked against a paper.** Week 1 is literature anyway, so rebuild it from the PDFs and let nothing downstream cite the current version.

## Papers to pull first

- Jayant Sirohi, UT Austin, hover performance of a cycloidal rotor for a micro air vehicle. Closest to our scale.
- Moble Benedict and Inderjit Chopra, meso-scale cycloidal-rotor aircraft for MAV application.
- Carl Runco and Moble Benedict, 70 gram micro quad-cyclocopter, design, development and flight testing.
- Cam-based passive blade pitching for a small-scale cyclogyro.
- Chalmers parametric analysis of a large-scale cycloidal rotor, for the scaling argument.

## Physics that should shape the argument

- Thrust scales with the square of rotational speed, power with the cube. Buying thrust through RPM gets expensive fast.
- Published power loading runs about 12 kgf/HP at low thrust, settling near 5 kgf/HP at high thrust. As an order-of-magnitude anchor only: 10 N is 1.02 kgf, so at roughly 8 kgf/HP that is about 0.13 HP, near 95 W. Sanity check for motor and battery selection, not a result.
- CFD shows non-dimensional thrust roughly constant as Reynolds number rises while torque and power fall, so cyclorotors scale up well aerodynamically. The counterweight is structural: blade weight per unit thrust stays constant with size, but blade stress climbs monotonically at similar geometry. Holding both of those at once is the design case worth making.

## Blade pitch mechanism

A required section and where designs differentiate. Active servo-driven per blade gives control authority at the cost of mass and part count inside a 408 g budget. Passive cam-based is lighter with fewer parts and less authority, and there is published work on it for small-scale cyclogyros. Given the mass constraint the passive route deserves the first look. Whichever is chosen, justify it, because an unjustified choice reads worse than a conservative one.

## Judging, and what it implies

Nine weighted criteria across thrust feasibility, thrust-to-weight, kinematic design, aerodynamic analysis, structural design, manufacturability, CAD quality and presentation.

Manufacturability and CAD quality being scored explicitly matters even at Stage 1, where no CAD is required. The evaluators care about buildability over novelty. A conservative design with a credible manufacturing route beats an exotic one with hand-waved fabrication.

## Compute

Baramati HPC is available in principle. Full notes in [_compute.md](_compute.md).

**Stage 1 needs no compute at all.** It is literature, arithmetic and writing.

Stage 2 is a different story and the cluster is a real asset there: the full CAE package wants CFD and FEA, and a 16-core, 96 GB, 12-hour Slurm job on the `gpu` partition covers it. Worth knowing now so Stage 2 is not a scramble, and worth checking whether MPI is configured and whether a CPU partition exists, since most CFD is CPU-MPI rather than GPU work.

The cluster is off-LAN and unreachable today, which does not matter for this project yet.

## Do these in week 1, before technical work

- Register on techfest.org under Competitions, then PUSHPAK Grand Challenge
- Confirm the team, up to 5 members
- **Check no team member is attached to the PUSHPAK project, the Drone Centre, or the organising or host institutions.** This disqualifies an entire team at any stage.
- **Line up a faculty supervisor.** The eligibility list names academic institutions, faculty-led student teams, startups, MSMEs and consortia, so faculty backing helps the framing, and Stage 2 needs CAE tool access that should not be arranged in October.
- Send the organiser email, one mail covering all three questions:
  1. Is the thrust-to-weight target of 2.5 on the rotor module alone or the complete aircraft?
  2. The FAQ references two objectives, then says only one is stated and leaves an internal note about confirming it. What is the second objective?
  3. Is there a detailed problem statement document beyond the competition page?

## Honest gaps

- The 32-day schedule assumes a daily worker and does not know real weekly hours or team size. Less fatal here than for UAV-X, since writing compresses and debugging does not, but it still needs a real number.
- Week 3 collides with the UAV-X comms layer, which is the highest-risk piece across both projects. If something has to slip, slip this one.
- Round 2 of the plan cross-check, by Codex, has not run.

## Execution notes

Runs under `/loop` in its own session, separate from UAV-X. **Never run a loop longer than 7 to 8 hours**; past that the increment per cycle collapses and it just spins.
