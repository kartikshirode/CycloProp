# CycloProp context: everything the submission has to satisfy

Built 26 August 2026 from the official problem statement PDF, which was found on the Techfest competition API after the website itself turned out to be a JavaScript app that serves no readable content to a fetcher.

**This file outranks every other document in the repo.** Where [brief.md](brief.md), [handoff.md](handoff.md), [_shared-timeline.md](_shared-timeline.md) or [stage-1/plan.md](stage-1/plan.md) disagree with it, this file wins, because those were written from the rendered page summary and this one is from the source PDF.

## Authority order

1. [reference/cycloprop-problem-statement.pdf](reference/cycloprop-problem-statement.pdf), the official problem statement. Plain text alongside it at [reference/cycloprop-problem-statement.txt](reference/cycloprop-problem-statement.txt)
2. [reference/techfest-api-cycloprop.json](reference/techfest-api-cycloprop.json), the raw competition record from `https://techfest.org/api/compis/`, which carries the site's about, structure, timeline, rules and FAQ fields
3. This file
4. Everything else

A note for whoever refreshes this later. The page at techfest.org/competitions/cycloprop renders client side and returns nothing useful to curl or WebFetch. The data lives at `https://techfest.org/api/compis/`, a plain JSON list of 15 competitions. Filter on `compi_id == "cycloprop"`. The `probStatement` field holds the PDF URL.

## The ask, in one paragraph

Design an indigenous cycloidal rotor module for drone use, producing at least 10 N of thrust at a thrust-to-weight ratio above 2.5, supported by CAD and CAE. The end goal is not a prototype. It is a build-ready design. Stage 1 is a preliminary design on paper, due 27 September 2026 by email.

## Stage 1: the seven required items

Quoted from the problem statement. Our earlier documents listed five of these. Items 4, 5 and 7 were wrong or missing.

> The preliminary design submission should include:
>
> 1. Cyclorotor concept and configuration.
> 2. Preliminary rotor sizing.
> 3. Blade arrangement and pitch-control concept.
> 4. Estimated thrust and power requirement.
> 5. Estimated module weight and thrust-to-weight ratio.
> 6. Initial material and manufacturing approach.
> 7. Team capability and execution plan.

Three things to notice.

Item 4 asks for **power**, not just thrust. The old plan treated power as an optional sanity check. It is a named deliverable.

Item 5 splits weight from the ratio, so both the component mass budget and the computed T/W have to appear as results, not as one number.

Item 7 is a **team capability and execution plan**, which nothing in the repo had until now. It is not a technical section. Given that the stated purpose of Stage 1 is "to identify technically promising teams for detailed design support", this section is doing real work in the shortlisting, and 15 slots against a national call is not generous.

## Evaluation criteria

Eight criteria, not the nine the FAQ claims. These sum to exactly 100, so the PDF table is right and the FAQ is stale.

| Criterion | Weight |
| --- | --- |
| Feasibility of achieving 10 N thrust | 15% |
| Feasibility of achieving thrust-to-weight ratio greater than 2.5 | 15% |
| Kinematic design of blade-pitch and thrust-vectoring mechanism | 15% |
| Aerodynamic analysis or simulation quality | 15% |
| Structural design and strength assessment | 15% |
| Manufacturability, material selection, and cost realism | 10% |
| CAD quality, integration readiness, and packaging | 5% |
| Presentation, viva, and technical clarity | 10% |

The PDF attaches these to the final evaluation: "The final score will be based on the detailed design report, CAE-supported evidence, final presentation, and viva during the Techfest evaluation." No separate Stage 1 rubric is published. Treat this as the best available signal of what the evaluators care about and write Stage 1 so it maps onto these headings, because a Stage 1 document that already speaks in the evaluators' categories is easier to score well.

Reading the weights: five criteria carry 15% each and four of those five are engineering analysis. Manufacturability at 10% outweighs CAD quality at 5%. Presentation and viva at 10% is not decoration.

## Hard design targets

Quoted from the problem statement table.

| Parameter | Target requirement |
| --- | --- |
| Thrust capacity | At least 10 N |
| Thrust-to-weight ratio | Greater than 2.5 |
| Rotor type | Cycloidal rotor with blade-pitch variation |
| Thrust vectoring | Demonstrated through kinematic and performance analysis |
| Design support | CAD and CAE-supported design |
| Analysis requirement | Kinematic, aerodynamic, and structural simulations |
| Final outcome | Build-ready cyclorotor design suitable for future prototype development |

## The thrust-to-weight basis, settled

This was the blocking question in the repo, and the problem statement answers it outright:

> The thrust-to-weight ratio shall be estimated based on the complete cyclorotor module, including rotor blades, frame, pitch mechanism, motor, actuator, and associated mounting hardware.

Module level, not aircraft level. So the arithmetic that was sitting on an assumption is now sitting on a quoted requirement:

```
T / W > 2.5,  T = 10 N
W < 10 / 2.5 = 4 N
m < 4 / 9.81 = 0.408 kg
```

**The whole module comes in under 408 g**, and the PDF enumerates what "whole module" includes: blades, frame, pitch mechanism, motor, actuator, mounting hardware. Nothing on that list can be pushed onto an imaginary airframe to make the number work. Sizing is unblocked and can start immediately.

## Thrust vectoring is a requirement, not a bonus

The design targets table demands thrust vectoring "demonstrated through kinematic and performance analysis", and criterion 3 names it explicitly at 15%. No document in this repo mentioned it before today.

This lands well against what the literature already gave us. In a four-bar passive pitch mechanism the offset size sets the pitching amplitude and the offset direction sets the phase, and phase is exactly what steers the thrust vector. So one passive linkage answers the mass constraint and the vectoring requirement together. It also handles the measured side force, since rotating the offset is how Benedict pulled a resultant that sat 30 degrees off vertical back onto the vertical. Details in [stage-1/literature.md](stage-1/literature.md).

Note the wording: at Stage 1 vectoring has to be *demonstrated through analysis*, so a kinematic argument and a performance number, not hardware.

## Dates

| Milestone | Date |
| --- | --- |
| Announcement and registration open | 22 August 2026 |
| Stage 1 work period | 22 August to 27 September 2026 |
| Stage 1 submission deadline | on or before 27 September 2026 |
| Stage 1 results | 2 October 2026 |
| Stage 2 work period | 3 October to 2 December 2026 |
| Stage 2 submission deadline | on or before 2 December 2026 |
| Stage 2 results | 6 December 2026 |
| Finale at Techfest | 16 to 18 December 2026 |

Plan to send on 26 September, a day early.

## Submission mechanics

Register first on techfest.org, under Competitions then PUSHPAK Grand Challenge. Everything after that is email to **pushpak_gc2026@aero.iitb.ac.in**. No portal, no form, no upload link, at any stage.

Team size is up to 5.

## Eligibility, and the clause that can end a run

> Project staff, research staff, consultants, interns, and other personnel directly engaged with the PUSHPAK Project, and Drone Centre, or the organizing/host institutions in connection with the Grand Challenge are NOT eligible to participate.

It applies to individuals and to teams, and a team carrying one such person "may be disqualified at any stage of the Grand Challenge, including after selection or announcement of results". Check every member before the team is fixed.

The PDF also lists where preference may be given: rotor design and unsteady aerodynamics, CAD and mechanical design, kinematic analysis of mechanisms, CFD and FEA and multibody dynamics, lightweight structures and material selection, motor and actuator and control selection, UAV subsystem integration and testing. That list is effectively a spec for item 7, so write the capability section against it.

## What Stage 2 will demand

Worth knowing now so Stage 1 does not commit to something that collapses in October. Eleven items:

1. CAD model of the complete cyclorotor module
2. Kinematic model of the blade-pitch mechanism
3. Aerodynamic analysis or simulation for thrust prediction
4. Structural analysis of blades, supports, frame, shaft, and critical linkages
5. Motor, actuator, bearing, and controller selection
6. Material selection and mass estimate
7. Thrust-to-weight ratio estimate
8. Manufacturability and assembly plan
9. Bill of materials and cost estimate
10. Risk assessment and mitigation plan
11. Build and test plan for the next phase

Stage 3 is a presentation and technical viva at Techfest, with a feedback window beforehand where the committee "may provide brief feedback" and teams are encouraged to improve the design before the final round.

## Money

No funding during Stage 1. The INR 1 lakh goes to each of the up-to-15 qualifying teams after Stage 1 results, to pay for Stage 2 work. That resolves the contradiction flagged in [_shared-timeline.md](_shared-timeline.md), which came from reading one sentence as two claims.

Stage 2 brings domestic travel and accommodation support per IIT Bombay norms. Stage 3 prizes are named: Zenith INR 3 lakh, Horizon INR 2.5 lakh, Vector INR 2 lakh, and two Ascent awards of INR 1.5 lakh. That totals 10.5 lakh, which with 15 lakh of Stage 1 grants gives the 25.5 lakh headline.

## Corrections to what the repo used to say

| Was | Actually |
| --- | --- |
| No detailed problem statement exists | It exists. It is a 200 kB PDF linked from the API record, and it is far more specific than the page |
| Stage 1 wants 5 items | It wants 7. Power, T/W as a stated result, and a team capability section were missing |
| Nine weighted criteria | Eight, and they sum to 100. The FAQ saying nine is stale |
| T/W basis unknown, size against both readings | Module level, quoted. 408 g confirmed |
| Thrust vectoring not mentioned | Required, and carries 15% |
| Stage 1 funding contradiction | No contradiction. No money during Stage 1, 1 lakh after results |
| Prize ceiling is a vague 25.5 lakh | Broken out by named award |

## Still open

The FAQ's "two objectives" answer still carries its editorial note about confirming internally, and it is still live on the site. The problem statement settles the substance though: the structure field says "Teams work on a single objective" and the PDF states one objective. Treat it as one objective and stop worrying about it.

That leaves nothing blocking. [stage-1/organiser-email.md](stage-1/organiser-email.md) is now mostly answered by the PDF and should be cut down or dropped.

## Where the technical inputs live

[stage-1/literature.md](stage-1/literature.md) carries the verified parameter table, the published mass breakdowns, the power-loading numbers and the first-cut sizing. It was built the same day and is the input to rotor sizing.
