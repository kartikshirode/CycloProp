# CycloProp handoff

Written 26 August 2026. Stage 1 is due **27 September 2026**, so there are 32 days. This file is where a fresh session starts; everything else links from here.

## What this is

PUSHPAK Grand Challenge 2026, Grand Challenge on advanced UAV propulsion. Design an indigenous cycloidal rotor module for drones, targeting at least 10 N thrust with a thrust-to-weight ratio above 2.5. The brief is explicit that the goal is **not fabrication**. It is identifying strong, build-ready designs.

Funded by MeitY under the national drone mission, hosted by IIT Bombay. Mentored by Prof. Arnab Maity and Dr. Dhwanil Shukla, Aerospace Engineering, IIT Bombay. Prize ceiling is INR 25,50,000 across the whole staged programme.

Read [brief.md](brief.md) for the full competition rules, then [stage-1/plan.md](stage-1/plan.md) for the work plan. Shared track rules are in [_shared-timeline.md](_shared-timeline.md), compute notes in [_compute.md](_compute.md), and the first plan review in [_plan-review-round1.md](_plan-review-round1.md).

Repo: github.com/kartikshirode/CycloProp. This project is its own repository and does not share a session with UAV-X.

## Where we are

Week 1 of 5, literature. Day 1 done on 26 August.

Four sources are read and the parameter table is rebuilt from the PDFs in [stage-1/literature.md](stage-1/literature.md). The bad table is gone from the plan. Three papers are still outstanding, all of them behind paywalls or a repository that refuses requests from here, and one of those is the only study in our own Reynolds band.

The organiser email is drafted at [stage-1/organiser-email.md](stage-1/organiser-email.md) and needs a registered team and a signature block before it can go.

Nothing is sized yet. No sizing should start until question 1 in that email is answered, or until week 2 begins and we proceed on a stated assumption.

Round 1 of the plan cross-check is done and found 8 issues, two of which land on this project. Both of those are now closed. Round 2 by Codex has not happened yet.

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

### 2. The literature table, closed on 26 August

The old table came from search summaries and was wrong. It is deleted, and the replacement is [stage-1/literature.md](stage-1/literature.md), built from the source PDFs with a status column saying which rows were actually read.

For the record, since the suspicions in this file turned out to be right and it is worth knowing how they were wrong: 700 rpm had no source at all, 24 rpm was junk as guessed, the c/R figures were two different studies welded together, and "1.3 in radius" was a 1.3 inch chord. Don't dig the old version out of git history and reuse it.

Three papers are still outstanding and one of them matters. The Texas A&M thesis on UAV-scale cyclorotor hover performance is the only published work in the Reynolds band our own sizing lands in, and the repository refuses direct requests. It needs a library proxy or the faculty supervisor.

## Papers

Read: Sirohi, Parsons and Chopra 2007 (University of Maryland, not UT Austin, the handoff had that wrong); Benedict's 2010 UMD dissertation; Xisto et al. 2016 on the large-scale rotor; Shrestha et al. 2017 on the meso-scale cyclocopter.

Outstanding: the Texas A&M UAV-scale thesis, Adams et al. on cam-based passive pitching, Runco and Benedict on the 70 gram quad-cyclocopter.

## Physics that should shape the argument

- Thrust scales with the square of rotational speed, power with the cube. Buying thrust through RPM gets expensive fast.
- Power loading runs about 12 kgf/HP at low thrust, settling near 5 kgf/HP at high thrust. 10 N is a high-thrust point, so read the asymptote and not the middle: 152 W aerodynamic, cross-checked at 161 W against Benedict's twin rotor at its operating point, so 230 to 250 W electrical. The 95 W figure this file used to carry was about 60% low.
- CFD shows non-dimensional thrust roughly constant as Reynolds number rises while torque and power fall, so cyclorotors scale up well aerodynamically. The counterweight is structural: blade weight per unit thrust stays constant with size, but blade stress climbs monotonically at similar geometry. Holding both of those at once is the design case worth making.
- **The side force is comparable to the vertical force.** Benedict measured a resultant sitting 30 deg off vertical at the twin-cyclocopter's operating point, and PIV showed a badly skewed wake. He corrected it by rotating the pitch mechanism offset by 30 deg. Whatever "10 N of thrust" ends up meaning, the submission has to say which way it points.
- Repeating a published MAV rotor five times to reach 10 N gives 485 g of rotor against a 408 g whole-module budget. So the module is one larger rotor, not a cluster, and the aerodynamic scaling argument above is what justifies it.
- Holding a fixed shape family and solving for 10 N pins the Reynolds number near 100,000 regardless of radius, because scaling chord and span with radius cancels size out of Re. Radius then only trades rpm against envelope. That number lands at the bottom of the band the Texas A&M study covers, which is why that thesis is worth chasing.

## Blade pitch mechanism

A required section and where designs differentiate. Active servo-driven per blade gives control authority at the cost of mass and part count inside a 408 g budget.

Reading the papers moved this on. Every flying cyclocopter in the sources read so far uses a passive four-bar linkage and none use per-blade servos, and that linkage is less limited than the word "passive" suggests. Amplitude comes from the size of a disk offset, phase comes from rotating the direction of that offset, and phase is what vectors the thrust. One passive mechanism, both controls, no actuator on any blade. Adams et al. take a different passive route on a 535 g vehicle, driving the pitch off centrifugal force through a cam, and that paper is still paywalled.

Given the mass constraint the passive route deserves the first look. Whichever is chosen, justify it, because an unjustified choice reads worse than a conservative one.

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
- Send the organiser email. It is drafted at [stage-1/organiser-email.md](stage-1/organiser-email.md), covering the thrust-to-weight basis, the missing second objective and whether a fuller problem statement exists. It needs a registered team and a signature block, nothing else

## Honest gaps

- The 32-day schedule assumes a daily worker and does not know real weekly hours or team size. Less fatal here than for UAV-X, since writing compresses and debugging does not, but it still needs a real number.
- Week 3 collides with the UAV-X comms layer, which is the highest-risk piece across both projects. If something has to slip, slip this one.
- Round 2 of the plan cross-check, by Codex, has not run.

## Execution notes

Runs under `/loop` in its own session, separate from UAV-X. **Never run a loop longer than 7 to 8 hours**; past that the increment per cycle collapses and it just spins.
