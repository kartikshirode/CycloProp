# Team capability and execution plan

Required Stage 1 item 7. The execution plan, the capability structure and the gap analysis are
written from the work the repository already contains. The member details come from the team,
supplied on 23 September 2026, and nothing about a person goes in here that the team didn't
supply. That rule is a blocked trigger in the loop config under D5 and it still holds.

Where the team gave no fact, this file says the fact isn't claimed rather than guessing one. The
team handed two calls to the plan, the tool choice and the Stage 2 owners, so both are made here
on cost and fit and marked as the plan's choice.

The claims about the Stage 1 work itself are checkable against the files: what was solved, what
was calculated, what was read off somebody else's measurement and what was neither.

## What the team supplied, and what is still open

Nine fields were tracked for the human handoff. Their state on 23 September:

| Tag | Field | State |
| --- | --- | --- |
| P-1 | Roster and each member's role | Supplied. Three members, roster below |
| P-2 | Institution and programme | Supplied. VPKBIET, B.Tech third year for all three. Branch not stated |
| P-3 | Prior work behind each preference area | None claimed. The team supplied roles and no prior projects, so none is listed |
| P-4 | CAD, CFD, FEA and multibody tools | Left to the plan. Chosen below, all on free licences. OpenFOAM already runs and the rest are planned installs |
| P-5 | Weekly hours from 3 October | 5 to 7 hours per week per member |
| P-6 | Sender | Kartik Shirode, from the registered address. SENDER-CONFIRMED |
| P-7 | Competition ID and Team ID | Supplied. REGISTRATION-CONFIRMED |
| P-8 | Eligibility against the disqualification clause | Checked by the team. ELIGIBILITY-CHECKED |
| P-9 | Workshop, lab and test access | A workshop and a 3D printer. No composites layup setup and no test rig |

P-8 went first because it's the one that can end the run after results are announced. The clause
is in `../../context.md`.

## Team capability

### Roster

Kalash, 3 members, VPKBIET.

| Member | Role on the team | Programme |
| --- | --- | --- |
| Kartik Shirode | Core programmer, and the sender | B.Tech, third year |
| Mandar Wagh | Programmer | B.Tech, third year |
| Aditya Shilalkar | Full stack programmer | B.Tech, third year |

Competition ID: `CP-439436FADAD2`
Team ID: `TM-5A7C41AF909`

All three are programmers. That's the team's real strength and it's also the plain answer to
what's missing: nobody on the roster claims mechanical, aerospace or fabrication experience. The
problem statement caps a team at 5, so two places are open. The plan is to fill them with
mechanical or aerospace students before the Stage 2 build weeks, and to ask a faculty member in
mechanical engineering to mentor the build. Neither has happened yet and nothing here names
either person.

### Capability against the preference list

The problem statement names seven areas where preference may be given. That list is close to a
specification for this section, so it's answered area by area, including the areas that aren't
covered.

No member claims prior project work in any of the seven, so the table carries only what the
Stage 1 files show and what's missing. The middle column is checkable against the repository.

| Preference area | What the Stage 1 work shows | The gap, and the Stage 2 route |
| --- | --- | --- |
| Rotor design and unsteady aerodynamics | A blade area coefficient traced back to two primary sources and recomputed from the printed pages, three coefficient scenarios with an evidence class each, a momentum floor, a figure of merit closure, an independent power route and a 36 point azimuthal load model rerun against the solved pitch schedule | No unsteady solver has been run and no rotor has been tested. Stage 2 item 3 |
| CAD and mechanical design | Dimensioned layout, a swept envelope from the linkage solution rather than the rotor circle, an interface table and a mount pattern, all without CAD because Stage 1 does not ask for it | No solid model exists. Stage 2 item 1 |
| Kinematic analysis of mechanisms | A four-bar closed per blade, the offset length solved by bisection for the frozen amplitude, a 37 row schedule that closes on itself, a Grashof classification, the transmission angle range, an interference result that decided the drivetrain layout, and a force vector map | The kinematics are closed form and planar. No multibody model, no joint friction, no compliance. Stage 2 item 2 |
| CFD, FEA and multibody dynamics | None of the three. The aerodynamics are analytical, the structure is closed form beam work and the mechanism is a loop closure | This is the largest single gap in the project. All three are Stage 2 items 2, 3 and 4 |
| Lightweight structures and material selection | Six load carrying materials each tied to the margin it decides, a blade section integrated from its own ordinates, eight margins against a 1.5 floor, a declared overspeed case and a named list of the analyses not done | Published class allowables, no coupon test, no certificate. Stage 2 item 6 and the coupon plan below |
| Motor, actuator and control selection | A five row drive shortlist screened on power, torque and the speed the pack can turn the motor at, all on a derated continuous rating rather than a 180 second maximum, plus servo torque and slew from the carrier load | Four of the five motor rows and the servo are supplier listings and not datasheets. No control loop is designed. Stage 2 item 5 |
| UAV subsystem integration and testing | An electrical and mechanical interface definition, a service access order, an assembly order and six pre-spin measurements written down | Nothing has been built and nothing has been tested. Stage 2 item 11 |

What the team does bring is software, and the Stage 1 work is built the way programmers build
things. Every number in the report is recomputed from stored geometry by Python solvers and a
gate script with 223 self-tests, and a stale or contradicted number fails a check before it
reaches the attachment. Stage 2 inherits that method. The tool choices below lean on it.

### Capability gaps, stated rather than covered

Four of them.

**No CFD, FEA or multibody model exists.** Everything in this submission is analytical or
closed form. That is defensible at Stage 1, which asks for a preliminary design, and it isn't
defensible at Stage 2, which names all three. It is the first thing the Stage 2 plan spends
time on.

**Nothing has been built or measured.** No coupon, no blade, no rotor, no load cell run. Every
material allowable is a published class value and the thrust coefficient comes off somebody
else's rotor.

**Nobody on the roster is a mechanical or aerospace student.** The analysis can be carried by
programmers who read the sources carefully, and Stage 1 shows that. Laying up a blade, machining
a root fitting and spinning a rotor safely are different skills, and the two open places on the
team are how the plan closes this.

**The facilities stop short of the build.** The team has a workshop and a 3D printer. The printer
covers fit check parts, linkage mock ups and layup jigs. A mould, a vacuum bag setup, a
balancing jig and somewhere safe to spin a rotor at 2337 rpm with 209.161 N pulling on each blade
aren't confirmed. Some of that is in the bill of materials as tooling. The room it happens in
isn't.

### Tools, chosen on cost and fit

The team left the tool choice to the plan. Everything below is on a free licence, so nothing
depends on a seat that may not exist, and the CAD and multibody tools are scripted in Python so
they read the same `numbers.json` the Stage 1 solvers write.

| Job | Tool | Licence | State on 23 September |
| --- | --- | --- | --- |
| Solid model and mass properties, items 1 and 6 | CadQuery, solids generated from `numbers.json` | Apache 2.0 | planned install |
| Drawings and assembly check, item 8 | FreeCAD with the TechDraw workbench | LGPL | planned install |
| Multibody, item 2 | Project Chrono through PyChrono | BSD 3-clause | planned install |
| CFD, item 3 | OpenFOAM v2412, meshes from gmsh, ParaView for post processing | GPL, ParaView BSD | OpenFOAM runs on the team's Slurm cluster account at Baramati, checked on a converged case. gmsh and ParaView planned |
| FEA, item 4 | CalculiX through the FreeCAD FEM workbench | GPL | planned install |

A scripted CAD model is the choice a programming team gets the most out of. A changed dimension
regenerates the solid, and its mass properties go into the gate the same way the solver outputs
do, which is how item 1's closing test gets checked without anyone reading a mass off a screen.
A student licence for a commercial modeller can be added later if the team gets one. The plan
doesn't need it.

## Execution plan

Stage 2 runs 3 October to 2 December 2026 and the report is due on or before 2 December. The
plan below submits on 1 December, a day early, the same margin Stage 1 uses. Stage 1 results
land on 2 October and the grant that pays for Stage 2 work arrives after them, which is why
quotations and coupon material sit in the first week rather than the third.

Each member commits 5 to 7 hours per week from 3 October, so 15 to 21 team hours a week against
11 deliverables in 9 weeks with two solver workstreams in it. That's tight. The owner column
below spreads the load three, three and four items, and item 11 needs all three.

### Stage 2 deliverables and the weeks they land in

All 11 required items, with what each one needs, what it waits on, the tool, an owner and the
gate that closes it. The team left the owners to the plan, so they're assigned here by role and
the team confirms them before 3 October.

| # | Stage 2 item | Week | Depends on | Tool | Owner | Closed when |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | CAD model of the complete module | 1 to 2 | Stage 1 geometry, frozen | CadQuery | Aditya Shilalkar | Every part in the 34 line budget exists as a solid, and the model's mass properties reproduce the budget within 5 percent |
| 2 | Kinematic model of the pitch mechanism | 2 to 3 | Item 1 | PyChrono | Mandar Wagh | The multibody schedule matches the closed form 37 row schedule, and joint reactions reproduce the pitch link load |
| 3 | Aerodynamic analysis for thrust prediction | 4 to 5 | Item 1 for the blade profile | OpenFOAM, 2D transient first then 3D | Kartik Shirode | A converged run at the design point, mesh and timestep independence shown, and the blade area coefficient either confirmed or replaced |
| 4 | Structural analysis of blades, supports, frame, shaft and linkages | 6 | Items 1 and 3 for the load case | CalculiX | Mandar Wagh | The eight Stage 1 margins reproduce or move, with every difference explained, plus the three dimensional parts beam theory could not reach |
| 5 | Motor, actuator, bearing and controller selection | 3 | Item 2 for the actuator load | Datasheets and supplier data | Mandar Wagh | Manufacturer datasheets for all five drive rows and the servo, and an oscillating rating or a bench test for the pitch bearings |
| 6 | Material selection and mass estimate | 7 | Items 1 and 4 | Coupon test and the CAD mass properties | Aditya Shilalkar | Cured laminate modulus and areal mass measured on a panel built the way the blade is built |
| 7 | Thrust-to-weight ratio estimate | 7 | Items 3 and 6 | The existing gate script | Kartik Shirode | All four cases recomputed on measured inputs, and the stacked case still above 2.5 |
| 8 | Manufacturability and assembly plan | 8 | Items 1 and 6 | FreeCAD drawings | Aditya Shilalkar | Every part has a drawing, a tolerance and a process, and the assembly order survives a dry run |
| 9 | Bill of materials and cost estimate | 1 and 8 | Item 6 for material quantities | Supplier quotations | Aditya Shilalkar | Written quotes for the five lines above 4500 INR, which are 49.8 percent of the total |
| 10 | Risk assessment and mitigation | 8 | Everything above | Risk register | Kartik Shirode | Every open item in the Stage 1 claims table has an owner, a trigger and a mitigation |
| 11 | Build and test plan | 8 to 9 | Items 8 and 10 | Test plan, the workshop and a test facility | All three | A staged spin plan, an instrumented thrust measurement and a named place to run it |

Two things about that table are worth reading twice.

Item 9 appears in week 1 and again in week 8. The 4 week foam import is the critical path on the
whole build and it has no Indian stockist, so the quote and the order go early or the build
plan is fiction. Everything else on a 3 week lead sits inside that window.

Item 3 is scheduled for two weeks and it is the one most likely to overrun. The design's own
inflow ratio is 0.3871, which is high, and that is exactly the regime where a simple model
stops being trustworthy and a CFD case stops converging quickly. If it slips, the fallback is
2D transient at the design azimuth set rather than a full 3D run, reported as what it is.

### Stage 2 gates

Stage 1 ran on a gate script that recomputes the physics from stored geometry and fails on
disagreement, and 223 self-tests behind it. That machinery carries straight into Stage 2 and it
is cheaper to extend than to rebuild.

- Every number in the Stage 2 report keeps tracing to `numbers.json`, and CFD and FEA outputs
  become new blocks in it rather than figures pasted into prose
- A solver result may not silently replace an analytical one. When CFD gives a different
  coefficient, the change is a numbered decision entry and the old value stays in the file as
  the record of what it was
- The four thrust to weight cases stay four. Reporting one of them is how week 2 of Stage 1
  confused itself for a fortnight
- Each week still ends with a progress file, a fresh context audit, a handoff and a decision
  entry, which is the protocol that caught the errors listed in the Stage 1 audits

Only item 3 needs shared hardware. The cluster has no walltime cap and a 2D transient case is
small next to it, so CFD runs overnight while the other items run on laptops.

### The route through the missing capability

Three of the four gaps have a route that needs no new person.

**CFD.** OpenFOAM already runs, so the cost is the rotating mesh and the validation rather than
the install. The validation case is Kellen's measured rotor, because the shape family is already
matched to within 1.1 percent on solidity and chord to radius, so there is a published number to
land on.

**FEA.** The parts that need it are the root fitting, the root bracket and the bearing block.
All three are small, all three are already sized by beam formulae, and the FEA job is to find
where the beam idealisation was wrong rather than to discover the design.

**Multibody.** The kinematics are already solved in closed form and the schedule is stored, so
the multibody model has a published answer to reproduce on day one. That makes it the cheapest
of the three to close and it is the one to do first.

**Testing.** This is the gap with no software route. The workshop and the 3D printer cover jigs,
fixtures and fit checks. A coupon panel and a lap shear coupon also need a layup bench and a test
frame, and a thrust measurement needs a load cell, a mount and a place where a rotor can be spun
to 2337 rpm behind something solid. None of those is confirmed. If they stay unavailable, Stage 2
says so and the report carries analysis where it wanted measurement, which is worse and is still
better than claiming a test nobody ran.

### What stops this plan

- **The roster.** Three programmers and no mechanical member yet. The two open places are the fix
- **Hours.** 5 to 7 per member per week against 11 deliverables in 9 weeks
- **Installs.** Four of the five tools are planned installs, and a failed one costs a week
- **The foam lead time.** 4 weeks, no Indian source, and it gates the build plan rather than the report
- **Test access.** Nothing in the plan can measure anything without it

## Numbers used

- operating.rpm = 2337.04
- structure.centrifugal_load_N = 209.161
- performance.inflow_ratio = 0.3871
- results.bom_longest_lead_weeks = 4
