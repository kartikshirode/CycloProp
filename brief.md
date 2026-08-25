# CycloProp: Advanced UAV Propulsion Challenge

**Track:** PUSHPAK Grand Challenge 2026
**Prize pool:** Upto INR 25,50,000
**Page:** https://techfest.org/competitions/cycloprop
**Status:** open, Stage 1 closes 27 September 2026

Shared timeline, rules and funding ladder are in `../_shared-timeline.md`.

Design an indigenous cycloidal rotor module for drone applications, targeting at least 10 N thrust and a thrust-to-weight ratio above 2.5. The stated goal is not fabrication. It is identifying strong, build-ready cyclorotor designs backed by CAE.

## Eligibility and team

Academic institutions, faculty-led student teams, startups, MSMEs, and academia-startup-industry consortia with expertise in UAVs, rotorcraft, aerodynamics, robotics, controls or mechanical design.

Up to 5 members per team.

## Structure

### Stage 1, preliminary design submission

About a month to submit a preliminary cyclorotor design covering configuration, rotor sizing, blade-pitch concept, estimated thrust and weight, and a manufacturing approach. Up to 15 teams qualify at INR 1 lakh each.

### Stage 2, detailed design development

About two months to build a complete CAE-supported design package: CAD model, kinematic and aerodynamic analysis, structural assessment, material selection, and a build-and-test plan. Up to 10 teams advance with travel and accommodation support.

### Stage 3, grand challenge finale

Present and defend the detailed design before the evaluation committee at Techfest, with a technical viva. Up to 5 winning teams continue into the Prototype Development Support Programme.

## Judging

Nine weighted criteria covering thrust feasibility, thrust-to-weight ratio, kinematic design, aerodynamic analysis, structural design, manufacturability, CAD quality and presentation.

Manufacturability and CAD quality being scored explicitly matters. A clever concept with sloppy drawings loses to a conservative one with a clean package.

## Mentors

Prof. Arnab Maity, Aerospace Engineering, IIT Bombay. Expertise in autonomous flight systems, UAV and drone technologies, guidance and control.

Dr. Dhwanil Shukla, Aerospace Engineering, IIT Bombay. Research in rotorcraft design, low-speed aerodynamics, experimental flow diagnostics.

## Research notes

### What a cyclorotor is

A fluid propulsion device with a horizontal axis of rotation, perpendicular to the direction of fluid motion, whose blades are cyclically pitched twice per revolution. That lets it vector thrust in any direction normal to the axis, which is the appeal for VTOL: instant thrust vectoring without tilting the airframe.

### The physics you will be arguing with

- Thrust scales with the square of rotational speed. Power scales with the cube. Buying thrust through RPM gets expensive quickly.
- Measured power loading sits around 12 kgf/HP at low thrust and asymptotes near 5 kgf/HP at high thrust.
- CFD work shows non-dimensional thrust holding roughly constant as Reynolds number rises, while non-dimensional torque and power fall significantly. So cyclorotors scale up favourably on aerodynamics.
- The structural side does not scale as kindly. Blade weight per unit thrust stays constant with size, but blade stress increases monotonically if you keep the geometry similar. That tension is where your design argument lives.
- Open problems in the literature: structural design, system weight, control dynamics, power supply, applicable scales, blade type and flowfield behaviour.

### Literature that maps onto a 10 N target

At least 10 N thrust with T/W above 2.5 puts you at meso scale, which is exactly where the published work sits:

- Jayant Sirohi at UT Austin, hover performance of a cycloidal rotor for micro air vehicles
- Moble Benedict and Inderjit Chopra, meso-scale cycloidal-rotor aircraft for MAV application, and later the 70 gram micro quad-cyclocopter at Texas A&M
- Quad cycloidal-rotor UAV development work
- Cam-based passive blade pitching mechanisms for small-scale cyclogyros
- A NASA study on a stopped-rotor cyclocopter for Venus exploration, if you want the extreme case

### Loose end on the page

The FAQ answers a question about "two objectives" by saying only one objective is stated, then adds an editorial note about confirming with the team before the FAQ goes out. That note is still live on the site. Ask what the second objective was meant to be before you scope your Stage 1 submission.

### Verdict

A design and analysis competition, so the cost is CAE competence and time rather than a workshop. Realistically needs faculty backing, both for the eligibility framing and for access to the analysis tools.

## Contact

pushpak_gc2026@aero.iitb.ac.in
