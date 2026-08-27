# CycloProp: research brief for an external agent

Written 27 August 2026. Self-contained on purpose, so you do not need the repository to
work from it. Everything below has been checked against primary sources unless it says
otherwise.

## What I need from you

Three problems, in priority order. Problem 1 decides whether the project is feasible at
all. Problem 2 feeds directly into it. Problem 3 is access to papers I cannot reach, and
those papers are the evidence for the first two.

I do not need a summary of what a cyclorotor is, and I do not need the design done for me.
I need evidence, numbers with sources, and where the published record contradicts what I
have assumed.

## The competition, in short

PUSHPAK Grand Challenge 2026, run by IIT Bombay under a MeitY-funded programme. The
CycloProp track asks for a **cycloidal rotor propulsion module**, designed on paper at
Stage 1 and built later.

Hard targets:

| Parameter | Requirement |
| --- | --- |
| Thrust | At least 10 N |
| Thrust to weight | Strictly greater than 2.5 |
| Rotor type | Cycloidal, with blade pitch variation |
| Thrust vectoring | Demonstrated by kinematic and performance analysis |

The critical definition, quoted from the official problem statement: the thrust to weight
ratio is measured on **"the complete cyclorotor module, including rotor blades, frame,
pitch mechanism, motor, actuator, and associated mounting hardware"**.

That boundary is the whole difficulty. No battery, no avionics, no airframe are counted,
so nothing can be pushed onto a vehicle to make the ratio work, and nothing published
measures a module on exactly that line.

Stage 1 is scored out of 100 across 8 criteria. The two that this brief is about carry 15
percent each: feasibility of 10 N thrust, and feasibility of T/W above 2.5. Stage 1 is
analysis, not hardware. Deadline is 27 September 2026.

Because the requirement is thrust **at or above** 10 N, design thrust is a free variable
and the mass ceiling moves with it:

| Design thrust | Mass ceiling for T/W > 2.5 |
| --- | --- |
| 10 N | 407 g |
| 12 N | 489 g |
| 13 N | 530 g |
| 15 N | 611 g |

Ceilings are floors rounded down, because the inequality is strict. Raising thrust is not
free: within a fixed shape family at fixed radius, going from 10 N to 13 N buys 30 percent
more mass ceiling and costs 14 percent more rpm, 30 percent more centrifugal load and 48
percent more ideal power.

## Where the project stands

Week 1 of 5 is done: requirements captured from the official PDF, and the literature table
rebuilt from primary sources. Weeks 2 to 5 cover sizing and thrust and power, then pitch
and vectoring, then structure and mass, then assembly. Nothing is sized yet. Week 2 starts
2 September and is the week that either closes the feasibility case or reports that it
cannot.

One person is doing this.

---

## Problem 1: the module thrust to weight gap

**This is the one that can sink the project.**

Taking the two closest published designs and re-cutting their mass breakdowns onto the
competition's module boundary:

| Design | Rotor | Motor share | Module per rotor | Thrust per rotor | Module T/W |
| --- | --- | --- | --- | --- | --- |
| Benedict 2010 quad-cyclocopter | 96.2 g | 23.8 g | 120.0 g | 1.98 N | **1.69** |
| Sirohi 2007 conceptual cyclo-MAV | 45.6 g | 23.9 g | 69.5 g | 1.23 N | **1.80** |

We need 2.5. That is 39 to 48 percent beyond the closest published work.

**Both figures are optimistic upper bounds, not measurements.** Neither paper reports a
module on this boundary, so I assembled them from line items, and several allocations are
unknown:

- Mounting hardware is excluded from both, because neither paper breaks it out
- Sirohi's whole 38 g "electronics and servos" line is excluded, and it contains the
  vectoring servos that the module boundary explicitly requires
- How much of Benedict's 225 g vehicle structure is module frame is unallocated, as is how
  much of Sirohi's 18.5 g structure line
- Benedict's 1.98 N is the vehicle weight share per rotor, not a plotted measurement. The
  thesis plots about 1.91 N at the operating point
- Sirohi's design was never built, so 1.23 N is a predicted requirement

Correcting any of those pushes the published ratio **down**, which widens the gap.

### The case that the gap is closable, which is exactly what I need checked

Four arguments, none of them yet supported by numbers:

1. **Scale.** Both published designs are 3 to 6 inch rotors at Reynolds numbers of 17,000
   to 35,000. Our design lands near 100,000. Published CFD suggests non-dimensional thrust
   holds while torque and power fall.
2. **Fixed masses amortise.** Bearings, fasteners, ESC and linkage hardware do not shrink
   with the rotor. On a 120 g module they dominate. On a 400 g module carrying five times
   the thrust they should not.
3. **Neither design was mass-optimised.** Benedict's earlier rig weighed 450 g and burned
   75 percent of its power on structure; the flight-weight redesign cut tare to 10 percent.
   Same concept, same scale, 7.5x difference out of mechanical design alone.
4. **Neither was chasing a T/W target.** They were built to fly and to measure.

**The counterargument I cannot dismiss:** under geometric similarity, blade mass per unit
thrust is scale invariant and blade stress climbs with size. If that holds, scale alone
does not close the gap, and the answer has to come from materials and from the non-blade
fraction instead.

### Questions

1. Is there any published cyclorotor, at any scale, whose mass breakdown can be re-cut
   onto this module boundary and gives better than 1.80? Large-scale work counts. So does
   anything from Seoul National University, IAT21, or the Chinese and Korean groups.
2. **Runco and Benedict, "Design, development, and flight testing of a 70-gram micro
   quad-cyclocopter", 2023.** At 70 g all-up this is the most mass-optimised cyclocopter
   published. What is its module-level mass breakdown and thrust per rotor? It is paywalled
   and I have not read it. It may be the single most useful data point for this problem.
3. Does anyone publish a **cyclorotor mass scaling law**, mass per newton against rotor
   size or Reynolds number? Even three or four points across scales would let me test
   argument 1 quantitatively instead of asserting it.
4. What is realistically achievable for **blade mass per unit span** in CFRP skin over foam
   core at 100 to 400 mm span, and how does that compare to what the published research
   rotors actually used? Most of them used balsa, depron or 3D printed parts.
5. Has anyone published a cyclorotor design that **states a thrust to weight target and
   reports whether it met it**? I have found none, which is itself worth confirming.
6. Is the 2.5 target in line with what conventional propellers achieve at this scale, and
   is there any public commentary on where the PUSHPAK organisers got that number?

---

## Problem 2: the thrust coefficient transfer

**This is the highest-risk assumption in the project and everything downstream scales off
it.**

All my sizing uses a blade-area thrust coefficient of **0.607**, meaning thrust equals
0.607 times 0.5 times air density times tip speed squared times total blade planform area.

That number is a single point derived from Benedict's 2010 quad-cyclocopter at its hover
point:

| | Source of 0.607 | Where I apply it |
| --- | --- | --- |
| Blades | 4 | 3 |
| Airfoil | NACA 0010 | NACA 0020 |
| Chord to radius | 0.433 | 0.66 |
| Reynolds | about 35,000 | about 100,000 |

Blade count, solidity, airfoil thickness and Reynolds number all move at once, and the
transfer is unvalidated.

The shape family I am moving to (3 blades, c/R 0.66, blade aspect ratio 4, NACA 0020, plus
or minus 40 degrees) comes from a Texas A&M thesis I have only seen in summary. Solving
that family for 10 N pins Reynolds near 100,000 regardless of the radius chosen, because
scaling chord and span with radius cancels size out of the Reynolds number. Convenient, and
it puts us at the bottom edge of the band that thesis studied.

### What I already know about the direction of each effect

From Benedict's own parametric results:

- Thrust rises to 45 degrees of pitch amplitude with no sign of stall
- NACA 0015 beats 0010 beats 0006 on power loading, and all NACA sections beat flat plates
- At **constant chord**, more blades raises solidity and improves power loading
- At **constant solidity** the picture flips: fewer blades give more thrust, and the 2-blade
  rotor had the best power loading
- Best pitching axis is 25 to 35 percent of chord

Xisto 2016, at roughly 10x our linear scale, contradicts some of this: c/R near 0.5 is
best, adding blades can reduce efficiency, and airfoil thickness matters at large scale in
a way it does not at micro scale.

### Questions

1. Is a **blade-area thrust coefficient** even the right non-dimensionalisation for a
   cyclorotor, or does the published field prefer something else? If the standard is a
   different reference area or a rotor-solidity form, tell me and give the conversion.
2. What is the **published spread** of this coefficient across blade count, airfoil,
   solidity and Reynolds number? I need a defensible lower bound, not a guessed percentage
   haircut. My current placeholder is 0.516, which is 85 percent of nominal and chosen with
   no better justification than caution.
3. How does cyclorotor thrust coefficient actually behave **between Re 35,000 and 100,000**?
   This is the specific question the Texas A&M thesis should answer and I cannot open it.
4. Going from **NACA 0010 to NACA 0020** at these Reynolds numbers, what happens to lift
   curve slope and stall margin under the continuously varying angle of attack a cyclorotor
   blade sees? Thicker sections usually help at low Reynolds. I want that confirmed or
   contradicted for this application.
5. Is there a **validated analytical or semi-empirical model** for cyclorotor hover thrust,
   double-multiple-streamtube or otherwise, with published validation against measurement?
   Xisto reports that simple analytical tools over-predict thrust and under-predict power
   away from the design point, which is the wrong direction for me.
6. Cyclorotor **side force is not small.** Benedict measured lateral force comparable to
   vertical force, with the twin-cyclocopter's resultant sitting 30 degrees off vertical at
   its operating point, corrected by rotating the pitch mechanism offset by 30 degrees. Is
   there published data on how that off-axis angle varies with pitch amplitude, phase and
   Reynolds number? Any claim of "10 N of thrust" has to say which way it points, and the
   competition also wants vectoring demonstrated.

---

## Problem 3: papers I cannot get

These are not optional reading. Two of the three are the primary evidence for problems 1
and 2. To be direct about why they are unread: it is access, not choice.

| Paper | Why it matters | Status |
| --- | --- | --- |
| **"Performance Measurements on a UAV-Scale Cycloidal Rotor in Hover"**, thesis, Texas A&M | The **only study in our Reynolds band**. Its shape optimum is my entire baseline geometry and I have it from a search summary only | The TAMU repository refused the request and the item page timed out |
| **Runco, C. and Benedict, M., "Design, development, and flight testing of a 70-gram micro quad-cyclocopter", 2023** | Most mass-optimised cyclocopter published. Directly addresses problem 1 | Paywalled |
| **Adams, Z., Benedict, M., Hrishikeshavan, V., Chopra, I., "Design, Development, and Flight Test of a Small-Scale Cyclogyro UAV Utilizing a Novel Cam-Based Passive Blade Pitching Mechanism", IJMAV 5(2), 2013, 145** | Closest published **passive pitching mechanism**, on a 535 g vehicle. Blade pitch is a required Stage 1 section | Summary only |

One consistency check that partly validates the Texas A&M summary: its three quoted shape
numbers agree by construction. A c/R of 0.66 with blade aspect ratio 4 gives a span of 2.64
R, so rotor aspect ratio comes to 1.32 against the 1.33 quoted. Three numbers agreeing that
way is decent evidence the summary read them correctly. It is not the same as opening the
thesis.

### Questions

1. Can you obtain any of these? Author copies on personal or lab pages, ResearchGate,
   institutional mirrors, conference preprints of the same work, or a later paper by the
   same authors that reproduces the key figures.
2. For the Texas A&M thesis specifically: the shape optimum, the thrust coefficient
   behaviour with Reynolds number, and the measured power loading.
3. For Runco 2023: the module-level mass breakdown and thrust per rotor.
4. For Adams 2013: the cam geometry, the achieved pitch schedule, and the mechanism mass.

---

## Sources I have already read in full, so do not re-derive these

- Sirohi, Parsons, Chopra, "Hover Performance of a Cycloidal Rotor for a Micro Air
  Vehicle", JAHS, July 2007. Note this is University of Maryland work; Sirohi moved to UT
  Austin afterwards and his UT page hosts the PDF, which is where the common misattribution
  comes from
- Benedict, M., "Fundamental Understanding of the Cycloidal-Rotor Concept for Micro Air
  Vehicle Applications", PhD dissertation, University of Maryland, 2010
- Xisto, Leger, Pascoa et al., "Parametric Analysis of a Large-Scale Cycloidal Rotor in
  Hovering Conditions", Journal of Aerospace Engineering, 2016
- Shrestha, Yeo, Benedict, Chopra, "Development of a meso-scale cycloidal-rotor aircraft
  for micro air vehicle application", IJMAV 9(3), 2017, 218-231

## What is already settled, so please do not spend time on it

- The requirements. They come from the official problem statement PDF and are transcribed
- Reynolds invariance under geometric similarity at fixed thrust. Derived and checked
- Aerodynamic power for 10 N is 152 to 161 W at the blade, from two independent measured
  routes that agree. An earlier 95 W figure was too low by about 60 percent
- Power goes roughly as 1/R within a fixed shape family at fixed thrust
- Copying one published MAV rotor five times to reach 10 N needs 485 g of rotor alone and
  does not close. A redesigned 2 or 3 rotor cluster is a different question and is still
  open
- No CAD at Stage 1. It is not asked for and carries 5 percent scored on the Stage 2 package

## How to hand results back

Findings with sources, please. For anything numeric I need the source, the configuration it
was measured on, and whether it was measured, simulated or predicted, because a design
number that turns out to be somebody's conceptual estimate has caused trouble here already.

Where you find the published record contradicts something in this brief, say so directly.
That is more useful to me than confirmation.
