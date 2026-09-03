# Team capability and execution plan

Required Stage 1 item 7. Two halves. The execution plan, the capability structure and the gap
analysis are written here from the work the repository already contains. The member-level
details, prior projects, tool licences and facility access are not complete, and no agent may
invent them: that is a blocked trigger in the loop config
under D5.

So read this as a form with the arithmetic already done. **Structure comes from the repository,
substance comes from a person.** Every place a person has to supply a fact is marked `[P-n]` and
all of them are listed in the next section. Nothing below claims a name, a qualification, a
degree, an employer, a tool licence or a piece of equipment.

The claims that are already here are claims about the Stage 1 work itself, which is checkable:
what was solved, what was calculated, what was measured by somebody else and read, and what was
neither. Those need no human input because the files are the evidence.

## What a person has to supply

Nine fields were tracked for the human handoff. The Competition ID and Team ID for P-7 are now
supplied, while the remaining member details still need filling. Four of the fields are also
week H items in `../human-gate.md`.

| Tag | What is missing | Where it goes | Also a week H item |
| --- | --- | --- | --- |
| P-1 | Roster: how many people, and each one's role on this module | Roster, and the submission's item 7 | yes, ROSTER-CONFIRMED |
| P-2 | Institution and programme for each member | Roster | institution supplied, programmes still needed |
| P-3 | Prior work behind each preference area claimed | Capability against the preference list | still needed |
| P-4 | Which CAD, CFD, FEA and multibody tools are actually available, and on what licence | Stage 2 gates, and the tool column | no |
| P-5 | Weekly hours each member can commit from 3 October | Execution plan | 5 hours per week |
| P-6 | Who sends the submission, from which address | Nowhere in this file. It is a week H marker | yes, SENDER-CONFIRMED |
| P-7 | The Competition ID and Team ID the submission has to quote | The email draft and the report identity table | yes, REGISTRATION-CONFIRMED |
| P-8 | Eligibility checked against the disqualification clause, for every member | Nowhere in this file. It is a week H marker | yes, ELIGIBILITY-CHECKED |
| P-9 | Workshop, lab and test access: what exists and what has to be hired or borrowed | The route through the missing capability | no |

P-8 goes first whatever the order of the rest. The clause in `../../context.md` disqualifies a
whole team at any stage, including after results are announced, so an unchecked roster puts
every hour of this at risk rather than just the section it sits in.

## Team capability

### Roster

Kalash, 3 members, VPKBIET.

`[P-1]` still needs each member's name and role. `[P-2]` still needs the programme for each
member.

The roster count and institution are now supplied. The capability section stays open until the
three member roles and programmes are written down.

Competition ID: `CP-439436FADAD2`
Team ID: `TM-5A7C41AF909`

Team size is capped at 5 by the problem statement. Nothing in Stage 1 needed more than one
person, and the Stage 2 item list below is where headcount starts to matter: CFD and FEA are
the two workstreams that can genuinely run in parallel with everything else.

### Capability against the preference list

The problem statement names seven areas where preference may be given. That list is close to a
specification for this section, so the honest thing is to answer it area by area and to say
which ones are not covered rather than to write around them.

The middle column is what the Stage 1 work shows and it is checkable against the files. The
third is where a person adds their own evidence. The fourth is what is genuinely missing.

| Preference area | What the Stage 1 work shows | Person supplies | The gap, and the Stage 2 route |
| --- | --- | --- | --- |
| Rotor design and unsteady aerodynamics | A blade area coefficient traced back to two primary sources and recomputed from the printed pages, three coefficient scenarios with an evidence class each, a momentum floor, a figure of merit closure, an independent power route and a 36 point azimuthal load model rerun against the solved pitch schedule | `[P-3]` | No unsteady solver has been run and no rotor has been tested. Stage 2 item 3 |
| CAD and mechanical design | Dimensioned layout, a swept envelope from the linkage solution rather than the rotor circle, an interface table and a mount pattern, all without CAD because Stage 1 does not ask for it | `[P-3]` | No solid model exists. Stage 2 item 1 |
| Kinematic analysis of mechanisms | A four-bar closed per blade, the offset length solved by bisection for the frozen amplitude, a 37 row schedule that closes on itself, a Grashof classification, the transmission angle range, an interference result that decided the drivetrain layout, and a force vector map | `[P-3]` | The kinematics are closed form and planar. No multibody model, no joint friction, no compliance. Stage 2 item 2 |
| CFD, FEA and multibody dynamics | None of the three. The aerodynamics are analytical, the structure is closed form beam work and the mechanism is a loop closure | `[P-3]` `[P-4]` | This is the largest single gap in the project. All three are Stage 2 items 2, 3 and 4 |
| Lightweight structures and material selection | Six load carrying materials each tied to the margin it decides, a blade section integrated from its own ordinates, eight margins against a 1.5 floor, a declared overspeed case and a named list of the analyses not done | `[P-3]` | Published class allowables, no coupon test, no certificate. Stage 2 item 6 and the coupon plan below |
| Motor, actuator and control selection | A five row drive shortlist screened on power, torque and the speed the pack can turn the motor at, all on a derated continuous rating rather than a 180 second maximum, plus servo torque and slew from the carrier load | `[P-3]` | Four of the five motor rows and the servo are supplier listings and not datasheets. No control loop is designed. Stage 2 item 5 |
| UAV subsystem integration and testing | An electrical and mechanical interface definition, a service access order, an assembly order and six pre-spin measurements written down | `[P-3]` `[P-9]` | Nothing has been built and nothing has been tested. Stage 2 item 11 |

### Capability gaps, stated rather than covered

Four, and pretending to cover the preference list is the failure mode this section is trying
to avoid.

**No CFD, FEA or multibody model exists.** Everything in this submission is analytical or
closed form. That is defensible at Stage 1, which asks for a preliminary design, and it is not
defensible at Stage 2, which names all three. It is the first thing the Stage 2 plan spends
time on.

**Nothing has been built or measured.** No coupon, no blade, no rotor, no load cell run. Every
material allowable is a published class value and the thrust coefficient comes off somebody
else's rotor.

**Tool access is unstated.** `[P-4]` The Stage 2 plan below names the category of tool each item
needs and deliberately does not name a product, because claiming a licence that may not exist
is the same class of error as claiming a person.

**Facilities are unstated.** `[P-9]` A mould, a vacuum bag setup, a CNC route, a balancing jig
and somewhere safe to spin a rotor at 2337 rpm with 209.161 N pulling on each blade. Some of
that is in the bill of materials as tooling. The room it happens in is not.

## Execution plan

Stage 2 runs 3 October to 2 December 2026 and the report is due on or before 2 December. The
plan below submits on 1 December, a day early, the same margin Stage 1 uses. Stage 1 results
land on 2 October and the grant that pays for Stage 2 work arrives after them, which is why
quotations and coupon material sit in the first week rather than the third.

`[P-5]` sets whether this calendar is real. The current commitment is 5 hours per week from
3 October. Stage 2 is a bigger package with two solver workstreams in it, so the calendar below
still needs the roster and role details before it becomes a schedule.

### Stage 2 deliverables and the weeks they land in

All 11 required items, with what each one needs, what it waits on, the tool category, an owner
and the gate that closes it.

| # | Stage 2 item | Week | Depends on | Tool category | Owner | Closed when |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | CAD model of the complete module | 1 to 2 | Stage 1 geometry, frozen | Parametric solid modeller | `[P-1]` | Every part in the 33 line budget exists as a solid, and the model's mass properties reproduce the budget within 5 percent |
| 2 | Kinematic model of the pitch mechanism | 2 to 3 | Item 1 | Multibody dynamics | `[P-1]` | The multibody schedule matches the closed form 37 row schedule, and joint reactions reproduce the pitch link load |
| 3 | Aerodynamic analysis for thrust prediction | 4 to 5 | Item 1 for the blade profile | Transient CFD, 2D first then 3D | `[P-1]` | A converged run at the design point, mesh and timestep independence shown, and the blade area coefficient either confirmed or replaced |
| 4 | Structural analysis of blades, supports, frame, shaft and linkages | 6 | Items 1 and 3 for the load case | FEA | `[P-1]` | The eight Stage 1 margins reproduce or move, with every difference explained, plus the three dimensional parts beam theory could not reach |
| 5 | Motor, actuator, bearing and controller selection | 3 | Item 2 for the actuator load | Datasheets and supplier data | `[P-1]` | Manufacturer datasheets for all five drive rows and the servo, and an oscillating rating or a bench test for the pitch bearings |
| 6 | Material selection and mass estimate | 7 | Items 1 and 4 | Coupon test and the CAD mass properties | `[P-1]` | Cured laminate modulus and areal mass measured on a panel built the way the blade is built |
| 7 | Thrust-to-weight ratio estimate | 7 | Items 3 and 6 | The existing gate script | `[P-1]` | All four cases recomputed on measured inputs, and the stacked case still above 2.5 |
| 8 | Manufacturability and assembly plan | 8 | Items 1 and 6 | Drawings | `[P-1]` | Every part has a drawing, a tolerance and a process, and the assembly order survives a dry run |
| 9 | Bill of materials and cost estimate | 1 and 8 | Item 6 for material quantities | Supplier quotations | `[P-1]` | Written quotes for the five lines above 4500 INR, which are 52 percent of the total |
| 10 | Risk assessment and mitigation | 8 | Everything above | Risk register | `[P-1]` | Every open item in the Stage 1 claims table has an owner, a trigger and a mitigation |
| 11 | Build and test plan | 8 to 9 | Items 8 and 10 | Test plan and a facility | `[P-1]` `[P-9]` | A staged spin plan, an instrumented thrust measurement and a named place to run it |

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
disagreement, and 204 self-tests behind it. That machinery carries straight into Stage 2 and it
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

`[P-4]` decides which of these can run unattended. A licensed solver on a single seat is a
scheduling constraint as much as a capability one.

### The route through the missing capability

Three of the four gaps have a route that does not need a new person.

**CFD.** Open source transient solvers exist and need no licence, at the cost of setup time and
a steeper validation burden. A licensed commercial solver is faster to get a first result out
of. Either way the deliverable is the same and the validation case is Kellen's measured rotor,
because the shape family is already matched to within 1.1 percent on solidity and chord to
radius, so there is a published number to land on.

**FEA.** The parts that need it are the root fitting, the root bracket and the bearing block.
All three are small, all three are already sized by beam formulae, and the FEA job is to find
where the beam idealisation was wrong rather than to discover the design.

**Multibody.** The kinematics are already solved in closed form and the schedule is stored, so
the multibody model has a published answer to reproduce on day one. That makes it the cheapest
of the three to close and it is the one to do first.

**Testing.** This is the gap with no software route. `[P-9]` A coupon panel and a lap shear
coupon need a layup bench and a test frame. A thrust measurement needs a load cell, a mount and
a place where a rotor can be spun to 2337 rpm behind something solid. If none of that is
available, Stage 2 says so and the report carries analysis where it wanted measurement, which
is worse and is still better than claiming a test nobody ran.

### What stops this plan

- **Eligibility.** `[P-8]` Unchecked, and it can end the run at any stage
- **Hours.** `[P-5]` Five hours per week against 11 deliverables in 9 weeks
- **Tool access.** `[P-4]` Three of the 11 items need a solver
- **The foam lead time.** 4 weeks, no Indian source, and it gates the build plan rather than the report
- **Test access.** `[P-9]` Nothing in the plan can measure anything without it

## Numbers used

- operating.rpm = 2337.04
- structure.centrifugal_load_N = 209.161
- performance.inflow_ratio = 0.3871
- results.bom_longest_lead_weeks = 4
