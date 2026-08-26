# Cyclorotor literature, checked against sources

Built 26 August 2026, day 1 of week 1. This replaces the parameter table that was in [plan.md](plan.md), which came out of search-result summaries and was wrong in several places. Nothing downstream should cite that table again.

Four sources were opened and read as full text. Two more are recorded from summaries only and marked as such, because the handoff was right that a clean-looking table hides how little of it was actually checked.

## Status column

- **read** means I pulled the PDF and read the relevant sections
- **publisher** means the publisher's own full-text page, not a search snippet
- **secondhand** means one paper reporting another paper's numbers
- **summary** means a search summary and nothing better yet

## Sources

| # | Source | Status |
| --- | --- | --- |
| S1 | Sirohi, J., Parsons, E., Chopra, I. "Hover Performance of a Cycloidal Rotor for a Micro Air Vehicle", Journal of the American Helicopter Society, July 2007 | read |
| S2 | Benedict, M. "Fundamental Understanding of the Cycloidal-Rotor Concept for Micro Air Vehicle Applications", PhD dissertation, University of Maryland, 2010 | read |
| S3 | Xisto, C., Leger, J., Pascoa, J. et al. "Parametric Analysis of a Large-Scale Cycloidal Rotor in Hovering Conditions", Journal of Aerospace Engineering, 2016 | read |
| S4 | Shrestha, E., Yeo, D., Benedict, M., Chopra, I. "Development of a meso-scale cycloidal-rotor aircraft for micro air vehicle application", International Journal of Micro Air Vehicles 9(3), 2017, 218-231 | publisher |
| S5 | "Performance Measurements on a UAV-Scale Cycloidal Rotor in Hover", thesis, Texas A&M University | summary |
| S6 | Adams, Z., Benedict, M., Hrishikeshavan, V., Chopra, I. "Design, Development, and Flight Test of a Small-Scale Cyclogyro UAV Utilizing a Novel Cam-Based Passive Blade Pitching Mechanism", International Journal of Micro Air Vehicles 5(2), 2013, 145 | summary |

One correction to the handoff. The Sirohi paper is University of Maryland work, not UT Austin. Sirohi moved to UT Austin afterwards and his UT page hosts the PDF, which is probably where the confusion started. Chopra is the common thread through S1, S2, S4 and S6.

## Geometry and measured performance

| Source | Config | Blades | Radius | Chord | c/R | Span | Blade AR | Airfoil | Pitch amp | Speed | Thrust | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S1 | UMD test rig | 3 and 6 | 76.2 mm | 25.4 mm | 0.333 | 152.4 mm | 6.0 | NACA 0010 | 0 to 40 deg | 0 to 1200 rpm | roughly 50 to 60 gf max | read |
| S2 | blade set 1 | 2, 3, 4, 5 | 76.2 mm | 25.4 mm | 0.333 | 152.4 mm | 6.0 | 0006 / 0010 / 0015, flat plates, reverse 0010 | 25 to 45 deg | 400 to 2000 rpm | to about 1.5 N | read |
| S2 | blade set 2, the optimum | 4 | 76.2 mm | 33.0 mm | 0.433 | 158.8 mm | 4.8 | NACA 0015 | 45 top, 25 bottom, axis at 25% c | 2000 rpm | about 2 N | read |
| S2 | twin-cyclocopter rotor | 3 | 76.2 mm | 25.4 mm | 0.333 | 152.4 mm | 6.0 | not stated | 40 deg | 2000 rpm | 1.47 N per rotor | read |
| S2 | quad-cyclocopter rotor | 4 | 76.2 mm | 33.0 mm | 0.433 | 158.8 mm | 4.8 | NACA 0010 | 40 deg symmetric | 2000 rpm | 1.98 N per rotor at hover | read |
| S4 | meso cyclocopter | 4 | 38 mm | 22 mm | 0.57 | 43 mm | 1.95 | NACA 0015 | 45 deg | 3000 rpm | 0.23 N per rotor | publisher |
| S5 | UAV-scale optimum, Re 200,000 | 3 | not given | not given | 0.66 | not given | 4.0 | NACA 0020 | 40 deg | not given | not given | summary |
| S3 | IAT21 L3 large rotor | 6 | 500 mm | 250 mm | 0.5 | 1000 mm | 4.0 | NACA 0016, axis at 35% c | 40 deg | 200 to 1200 rpm | order 400 to 1500 N | read |
| S1 | Gibbens full-scale rig | 6 | 610 mm | 305 mm | 0.5 | 1220 mm | 4.0 | NACA 0012 | not given | not given | power loading 10.88 lb/HP at Re 730,000 | secondhand |
| S1 | Kim et al. 2003 | not given | not given | 150 mm | not given | 800 mm | not given | NACA 0012 | not given | to 600 rpm | power loading 12 to 5 kgf/HP at Re 260,000 | secondhand |
| S1 | Wheatley 1930s NACA | 4 | 1220 mm | 95 mm | 0.078 | 2440 mm | 25.7 | NACA 0012 | not given | not given | not given | secondhand |

S5 could not be downloaded. The TAMU repository refused the request from here and the item page timed out. Its three quoted shape numbers do check out against each other though: c/R of 0.66 with a blade aspect ratio of 4 gives a span of 2.64 R, so the rotor aspect ratio comes to 1.32 against the 1.33 quoted. Three numbers agreeing by construction is decent evidence the summary read them correctly. It still is not the same as opening the thesis.

## What the old table got wrong

The 700 rpm entry has no source I can find. Every measured rig at this scale sits somewhere else. S1 was mechanically limited to 1200 rpm, S2 swept 400 to 2000, S4 runs at 3000. Nothing lands at 700.

The 24 rpm entry is junk, as the handoff guessed. No 150 mm radius, 80 mm chord, 200 mm span 4-blade config appears in anything I read.

"6 blades, c/R 0.67, NACA 0015, 45 deg" is two real results welded together. S2's optimum is 4 blades and NACA 0015, but at c/R 0.433 with asymmetric 45/25 pitching. The 0.66 c/R belongs to S5, which uses 3 blades and NACA 0020.

"1.3 in radius, c/R 0.8" is a units slip. 1.3 inches is the **chord** of S2's optimised blade, on a rotor of 3 inch radius, so c/R is 0.433 and not 0.8.

The blade aspect ratios of 1.181, 1.618 and 2.196 quoted in the plan are not in any source I opened. Don't cite them until someone finds where they came from.

## Findings that survive checking

From S2, the fullest parametric study at our kind of scale:

- Thrust keeps rising to a pitch amplitude of 45 deg with no sign of blade stall, and higher amplitude also improves power loading
- On power loading, NACA 0015 beat NACA 0010, which beat NACA 0006. All the NACA sections beat flat plates on thrust
- Adding blades at constant chord raises solidity and improves power loading, across a wide range of pitch amplitudes
- Hold solidity constant instead and the picture flips. Fewer blades give more thrust, and the 2-blade rotor had the best power loading of the set
- Best pitching axis sits at 25 to 35% of chord
- Bending and torsional flexibility both hurt, so the blades want to be stiff
- The overall optimum was 4 blades, 1.3 inch chord, NACA 0015, asymmetric pitching of 45 deg at the top of the trajectory and 25 deg at the bottom, axis at 25% chord

Two findings from S2 that nobody would guess from an abstract, and that matter for us:

**The side force is not small.** Measured lateral force was comparable in magnitude to the vertical force. On the twin-cyclocopter at its operating speed the resultant thrust sat 30 deg off vertical, and they fixed it by rotating the pitch mechanism offset by 30 deg. PIV showed a badly skewed wake, which is the same story told from the flow side. Any claim we make about "10 N of thrust" has to say which direction it points.

**Tare power depends on how well the rotor is built.** The heavy UMD bench rig burned about 75% of total power on structure. The flight-weight rotor built for S2 got that down to 10%. Same concept, same scale, and a 7.5x difference in parasitic loss out of mechanical design alone.

From S1:

- Thrust goes with the square of rotational speed, power with the cube. Measured, not assumed
- Going from 3 blades to 6 gave only 30% more thrust at the same speed and collective, because the downstream blades fly in the upstream blades' downwash
- Power loading levelled off near 25 g/W, but that counts blade aerodynamic power only, on a rig whose real losses were mostly friction

From S3, at roughly 10x our linear scale:

- c/R near 0.5 gives the best efficiency
- Adding blades can reduce efficiency, which is the opposite sign to S2's constant-chord result and worth being careful about
- Airfoil thickness matters at large scale in a way it does not at micro scale
- Moving the pitching axis aft of the leading edge helps, up to 35% of chord
- Simple analytical tools over-predicted thrust and under-predicted power away from the design point

## Published mass breakdowns

This is the part that bears on the 408 g question.

Quad-cyclocopter from S2, 809 g all up, four 6 inch rotors:

| Component | Weight (g) | % |
| --- | --- | --- |
| Rotors, all four | 385 | 47.6 |
| Structure | 225 | 27.8 |
| Motor and controller | 95 | 11.7 |
| Li-Po battery | 75 | 9.3 |
| Electronics | 29 | 3.6 |

Conceptual cyclo-MAV from S1, 248.9 g:

| Component | Weight (g) | % |
| --- | --- | --- |
| Rotor system | 91.3 | 37.0 |
| Li-Po, 700 mAh | 53.3 | 21.4 |
| Motors | 47.8 | 19.3 |
| Electronics and servos | 38.0 | 15.3 |
| Structure | 18.5 | 7.4 |

Both put the rotor between 37 and 48% of all-up weight. That framing is useful for intuition and **wrong for our budget**, because the denominator is all-up aircraft mass including battery, avionics and airframe, none of which the competition's module boundary contains. Re-cut onto the boundary the problem statement actually defines, the picture is harder.

### The published state of the art, on our boundary

The module is blades, frame, pitch mechanism, motor, actuator and mounting hardware. No battery, no avionics, no airframe. Taking each published design and keeping only what falls inside that line:

| Design | Rotor | Motor share | Module per rotor | Thrust per rotor | Module T/W |
| --- | --- | --- | --- | --- | --- |
| S2 quad-cyclocopter | 96.2 g | 23.8 g | 120.0 g | 1.98 N | **1.69** |
| S1 conceptual cyclo-MAV | 45.6 g | 23.9 g | 69.5 g | 1.23 N | **1.80** |

Mounting hardware is not broken out in either paper, so both numbers are optimistic.

**We need 2.5.** That is a 39 to 48 percent improvement in thrust per unit module mass over the closest published work, and it is the single hardest number in this project. Nothing else in the brief is as far from the state of the art.

The case that it is reachable, which week 2 has to make quantitatively rather than assert:

- **Scale.** Both designs are 3 to 6 inch research rotors at Reynolds numbers of 17,000 to 35,000. Ours lands near 100,000, where the published CFD says non-dimensional thrust holds while torque and power fall
- **Fixed masses amortise.** Bearings, fasteners, ESC and linkage hardware do not shrink with the rotor. On a 120 g module they dominate; on a 400 g module carrying five times the thrust they do not
- **These were demonstrators, not mass-optimised modules.** S2's own text says the earlier rig weighed 450 g and burned 75 percent of its power on structure, and that the flight-weight redesign cut tare to 10 percent. The same attention applied to mass, with CFRP instead of research-shop parts, is where the margin has to come from
- **Neither design was trying to hit a T/W target.** They were built to fly and to measure, and their mass budgets show it

The counterweight is the one the brief already names: blade weight per unit thrust stays constant under geometric similarity, and blade stress climbs. If blade mass per newton really is scale-invariant, scale alone does not close the gap and the answer has to come from materials and from the non-blade fraction. Week 2 has to establish which of those it is leaning on.

Drive details worth keeping. S2's twin used two 75 W outrunners geared 5:1 through bevel gears so the motors could sit at 10,000 rpm near peak efficiency while the rotors turned at 2,000. The quad drove all four rotors off a single 250 W outrunner through a two-stage transmission. S4 used 3 g AP-03 4000KV motors on a 7:1 single stage.

## What this does to the Stage 1 numbers

All three of these are provisional. None should be locked until the organisers answer whether T/W of 2.5 is measured on the module or on the aircraft.

**Power. The plan's 95 W is too low, probably by about 60%.** That figure came from picking 8 kgf/HP out of the middle of a 12-to-5 range. Two independent measured routes disagree with it. S2's twin rotor at its actual operating point gives 0.062 N/W, which is 4.71 kgf/HP. Kim's high-thrust asymptote in S1 is 5 kgf/HP. Both land at 152 to 161 W of aerodynamic power for 10 N, and 10 N is a high-thrust point, so the asymptote is the right end of that curve to read. Call it 230 to 250 W electrical at a 65% chain efficiency. Higher Reynolds number at our size should claw some of that back, which is the one honest reason to expect better than the measured MAV figures.

**Mass. A scaled-out MAV rotor cannot make the budget.** S2's flight-weight 6 inch rotor masses 96 g and carries 1.98 N at hover. Getting to 10 N by repeating that rotor takes 5.04 of them, so 485 g of rotor and nothing else, against a whole-module budget of 408 g. The module therefore has to be one larger rotor rather than a cluster of small ones, and the case for that is aerodynamic as well as structural, since non-dimensional thrust holds while torque and power fall as Reynolds number rises.

**Geometry. Similarity at fixed thrust pins the Reynolds number.** Take S5's shape family, meaning chord at 0.66 R and span at 2.64 R with 3 blades, and solve for 10 N using an effective blade-area thrust coefficient of 0.607 derived from S2's quad rotor at its hover point. Reynolds number comes out near 100,000 whatever radius you pick, because scaling chord and span with R while holding thrust fixed cancels size out of Re. Radius then buys nothing except a trade of speed against envelope:

| Radius | Chord | Span | Diameter | Speed | Tip speed |
| --- | --- | --- | --- | --- | --- |
| 80 mm | 52.8 mm | 211 mm | 160 mm | 3386 rpm | 28.4 m/s |
| 100 mm | 66.0 mm | 264 mm | 200 mm | 2167 rpm | 22.7 m/s |
| 120 mm | 79.2 mm | 317 mm | 240 mm | 1505 rpm | 18.9 m/s |
| 140 mm | 92.4 mm | 370 mm | 280 mm | 1106 rpm | 16.2 m/s |
| 160 mm | 105.6 mm | 422 mm | 320 mm | 846 rpm | 14.2 m/s |

That 100,000 sits at the bottom edge of the 100,000 to 300,000 band S5 studied, so its optimum applies to us directly instead of being an extrapolation off the end of somebody's data. Of everything this week turned up, that is the most useful.

The 0.607 coefficient is mine, derived for scaling, not a published quantity. It is thrust over tip dynamic pressure times total blade area, taken from S2's quad rotor at 2000 rpm carrying 809 g across four rotors. Treat it as a working anchor and re-derive it if S5 ever opens.

## Still to pull

- S5, the TAMU thesis. It is the only study in our Reynolds band and the repository blocks direct requests. Worth a library proxy, or ask the faculty supervisor once one is lined up
- S6, the cam-based passive pitching paper. Blade pitch is a required Stage 1 section and this is the closest published passive mechanism, on a 535 g vehicle
- Runco, C. and Benedict, M. "Design, development, and flight testing of a 70-gram micro quad-cyclocopter", 2023. Paywalled
