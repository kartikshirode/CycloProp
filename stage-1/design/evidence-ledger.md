# Evidence ledger and selection rules

Built first, before any sizing, so no number in week 2 gets its authority from the document
that quotes it. Written 2 September 2026, revised the same day after the week 2 audit.

Every value that carries a design decision is below with its class. The classes are the ones
`numbers.json` enforces on the coefficient rows, extended here to cover sources as well as
scenarios.

| Class | What it means |
| --- | --- |
| measured | somebody measured this quantity, on this configuration, and I read the figure |
| derived | computed by me from figures somebody measured on a different configuration |
| transferred | a derived value carried across a change of geometry, blade count or Reynolds number |
| summary | the source exists but I have only read a summary of it |
| downside | an engineering scenario I built. Not a published bound |
| catalogue | a supplier datasheet figure |
| assumed | no source. A number I chose, with the reasoning stated and the sensitivity given |

Nothing in this project is class measured. Not one row. That is worth saying plainly, because
a reader skimming for a thrust coefficient finds 0.6055 sitting in `numbers.json` and could
easily assume somebody put this rotor on a load cell. Nobody did. The closest thing to a
measurement here is a figure measured on a different rotor and carried across.

## Evidence ledger

| # | Value | Class | Source and exact basis | Area convention | Source geometry | Source Re | How it is used |
| --- | --- | --- | --- | --- | --- | --- | --- |
| E1 | blade-area thrust coefficient 0.6055 | transferred | Benedict 2010 (S2), quad-cyclocopter rotor at hover: 1.98 N per rotor at 2000 rpm. Recomputed here, not quoted | blade area, blades times chord times span | 4 blades, NACA 0010, c/R 0.433, R 76.2 mm, chord 33.0 mm, span 158.8 mm | 35,100 | sets rpm at the design thrust, and through that everything else |
| E2 | blade-area thrust coefficient 0.8114 | derived | Benedict 2010 (S2), twin-cyclocopter rotor: 1.47 N per rotor at the same 76.2 mm radius and the same 2000 rpm, recomputed the same way | same | 3 blades, chord 25.4 mm, span 152.4 mm, c/R 0.333, solidity 0.159 | 27,000 | upside indication only. Solidity is far outside the measured band, so it is not adopted |
| E3 | low coefficient 0.5147 | downside | E1 less 5 percent for blade flexibility and 10 percent for configuration transfer, added rather than compounded | same | not applicable | not applicable | the conservative thrust the decision gate is judged on |
| E4 | figure of merit 0.6 | summary | Kellen 2019 (S5), reported in the abstract and the companion Forum papers. The thesis body is unread | projected, 2R times span | 3 blades, NACA 0020, c/R 0.66, blade AR 4 | 200,000 | turns the momentum floor into a working aerodynamic power. Load bearing, and summary class |
| E5 | solidity band 0.30 to 0.40 | summary | Kellen 2019, reported optimum range. Same unread thesis | not applicable | as E4 | 200,000 | the gate on whether E1 may be transferred at all. See D12 |
| E6 | power loading 0.062 N/W | derived | Benedict 2010 (S2), twin rotor at its operating point | blade aerodynamic power | 3 blades, c/R 0.333 | 27,000 | the independent second power route |
| E7 | rotor tare 10 percent of shaft power | transferred | Benedict 2010 (S2), measured on his flight-weight rotor. The heavy bench rig burned about 75 percent, same quantity and a different build quality | not applicable | 4 blades at 76.2 mm radius | 35,100 | the tare term between aerodynamic and shaft power. Measured, but not on this rotor, so transferred |
| E8 | peak to mean blade load 3 to 4 | summary | Alsabri et al., Aerospace 13(9):765, 2025, 2D URANS. Not read here | not applicable | 2 and 3 bladed rotors | not stated | week 4 uses 4.0, per D16 |
| E9 | module thrust to weight 2.13 | derived | Runco and Benedict 2023, Table 3 re-cut onto the competition module boundary: 8.2 g per rotor carrying a flight-demonstrated 17.5 gf | not applicable | 4 blades, flat plate, R 33 mm | 18,600 | the benchmark the mass case is argued against |
| E10 | blade mass per newton is scale invariant | summary | Shrestha and Benedict, JAHS 67(4) 2022. Simulated and validated, not a transcribed measurement | not applicable | geometric similarity | 10,000 to 100,000 | forbids the claim that growing the rotor shrinks blade mass. See D11 |
| E11 | Reynolds invariance of non-dimensional thrust holds from 10,000 to 100,000 | summary | Shrestha and Benedict, JAHS 67(4) 2022, same source as E10 | not applicable | geometric similarity | the range itself | this is the support under the Reynolds half of the E1 transfer, and the design point sits above it. See D25 |
| E12 | MN5006 KV450: 650 W and 26 A maximum for 180 s, 106 g with cable, 60 mOhm, 0.9 A idle at 22 V, 4-6S | catalogue | Supplier datasheet PDF, read directly, 2 September 2026 | not applicable | not applicable | not applicable | the selected drive and its mass line, after the 0.80 derate in E15 |
| E13 | MN3510 KV700 555 W / 25 A / 118 g; MN4006 KV380 380 W / 17.5 A / 57 g; MN3110 KV470 330 W / 15 A / 98 g; MN2806 KV650 187 W / 12.3 A / 46 g, all at 180 s | catalogue | Supplier listings, 2 September 2026. Not read off datasheet PDFs like E12 | not applicable | not applicable | not applicable | the rest of the drive shortlist and the sensitivity rows |
| E14 | densities: PMI foam 52, CFRP 1550, aluminium 2700 kg/m3, skin 0.22 kg/m2 | catalogue | Rohacell 51 IG class, cured carbon epoxy, 6061, two plies of 60 gsm twill at 45 percent resin | not applicable | not applicable | not applicable | every geometry-scaled mass line |
| E15 | continuous duty is 0.80 of the 180 s rating | assumed | No source. T-Motor publishes a three minute maximum and the problem statement states no endurance requirement, so there is nothing to size a derate against | not applicable | not applicable | not applicable | turns every catalogue rating into the continuous figure the drive is selected on |
| E16 | efficiencies: belt 0.93, motor 0.84, ESC 0.95 | assumed | No source. Belt drive is published at 0.95 to 0.98 at these speeds so 0.93 is pessimistic; the motor figure is the sensitive one and at 0.78 the motor input rises from 458 W to 493 W | not applicable | not applicable | not applicable | the whole electrical power chain and the drive selection |

Six rows deserve sentences rather than cells.

**E1 is the highest risk value in the project and it is now an extrapolation in two
directions at once.** Our family gives a solidity of 0.3151, inside Kellen's measured 0.30 to
0.40, which is what D12 asks. The rotor the coefficient came from has a solidity of 0.276, so
the transfer runs into the measured band from outside it. And the design point sits at a chord
Reynolds number of 134,000, above the 100,000 top of E11, the range over which non-dimensional
thrust is published as Reynolds invariant. That second problem is not avoidable inside this
shape family: the requirement that the conservative thrust clear 10 N forces design thrust
above 11.76 N, and Reynolds goes with the square root of thrust, so the lowest compliant point
already sits at 108,000. D25 carries it.

**E3 is a scenario I built, not a bound anybody published.** The repository has carried 0.516
as a low value since the external research round and it was always flagged as a caution rather
than a limit. It still is. Kellen 2019 holds the measured coefficient for this exact shape
family in roughly our Reynolds band, behind a Cloudflare browser challenge that needs a person
with a browser. Until somebody opens it, the low column is an engineering downside and the
submission says that in those words.

**E4 and E5 are summary class doing load-bearing work.** The figure of merit is what turns
the momentum floor into the 321.7 W the whole power chain and the drive selection rest on, and
it comes from an abstract. Anywhere this document or the design documents use it, they say
reported rather than measured. The three shape numbers quoted from the same summary do check
out against each other, which is decent evidence the summary read them correctly, and it is
still not the same as opening the thesis.

**E7 is a measurement, on somebody else's rotor.** Benedict measured tare on his flight-weight
build. Carrying that 10 percent onto a rotor of a different size and a different bearing count
is a transfer, so it is labelled one, even though the underlying number was measured.

**E12 was read off the datasheet PDF and E13 was not.** The MN5006 figures come from the
manufacturer's own specification sheet, which is why the selected drive is the one with the
best evidence behind it. The other four came from supplier listings and week 4 confirms them.

**E15 and E16 have no source at all and they matter.** The datasheet says "Max. Power (180s)"
and "Peak Current (180s)", which is a three minute maximum, not an indefinite hover rating.
Running a module continuously at that figure is not supported by anything, so week 2 takes 80
percent of it. Nothing justifies 80 rather than 70 or 90 except ordinary practice, and the
problem statement gives no endurance requirement to size it against. The efficiency chain is
in the same position. Both are marked assumed rather than dressed up.

## Selection rules

Fixed before any candidate was scored, which is the only thing that makes them worth having.

**The boundary.** The competition's own words: rotor blades, frame, pitch mechanism, motor,
actuator and associated mounting hardware. No battery, no avionics, no airframe. Applied
identically to every candidate, published or ours.

**The two disputed allocations, decided here rather than later.** ESCs count as module
hardware, because the motor does not turn without one and the problem statement lists the
motor. Mounting counts in full, so every fastener, insert, standoff, lug and bonded joint that
holds the module together or attaches it to a vehicle. Both choices push our own number down.
On Runco's re-cut they move the benchmark from 2.13 to roughly 1.78, and the comparison in this
week's documents quotes 2.13 anyway, which is the harder comparison to win.

**Decision metrics, in order.** Conservative thrust to weight first. Then whether a named
drive holds the design point on its derated continuous rating, in power, in torque and in the
speed the pack can actually turn it at. Then the largest dimension of the module. Then part
count. Power is reported and does not rank, since no criterion scores it, but a candidate no
shortlist drive can hold is rejected on the drive metric.

**The packaging assumption, stated because the brief gives no maximum rotor size.** Rotors sit
side by side in one plane. Each gets a 20 mm clearance allowance across its diameter and the
set carries 40 mm of frame overhang, so the module width is n times (2R plus 20 mm) plus 40 mm.
The largest dimension is that width or the blade span, whichever is greater. Every candidate
row and every sweep row is computed from that one rule.

**The radius rule.** A larger radius lowers aerodynamic power and lowers rpm, and it raises
rotor torque along with every geometry-scaled mass line. Power alone does not choose it. The
candidate table carries rpm, Reynolds, ideal power, aerodynamic power, rotor torque, electrical
power, largest dimension and both mass columns on every row.

**Mass classification.** Every line is geometry-scaled, power or torque-scaled, or fixed, and
a line is only fixed when nothing in its own basis moves with radius, thrust or torque. The
motor, the transmission, the ESC, the rotor shaft, the bearings and the vectoring actuator are
all power or torque-scaled. That is D15.

**Conservative column rates, applied by what a line is made of and not by where it sits.**
Catalogue parts whose mass is published take 15 percent. Anything computed from an assumed
section takes 20 percent. The module frame, which is the least developed part of the design,
takes 25 percent.

**The cluster comparison runs in the cluster's favour.** Non-overlapping wakes, no interaction
penalty, one shared motor sized on total power, one shared controller, and the same thrust
coefficient for all three even though splitting the thrust drops per-rotor Reynolds. If the
single rotor still wins on those terms, it wins.

**What freezes geometry.** The conservative case, meaning the low coefficient and the high
mass column together, clearing thrust to weight 2.5 with its inputs carrying evidence. The
internal target is 2.75. Between the two is compliant and red and needs a person to decide.
Below 2.5, nothing freezes.

## Disclosed gaps

- Kellen 2019, Heimerl et al. at the VFS 77th Forum, and Ramsey 2022 are all unread, all
  behind the same JavaScript challenge. Kellen stopped being supporting evidence this week and
  became load bearing, for the reason in `stage-1/progress/week-2.md`
- No published cyclorotor states a thrust to weight target and reports whether it met it.
  Searched in week 1, not found
- No openly tabulated spread of blade-area thrust coefficients exists. The values sit inside
  primary figures
- E13's four catalogue rows need a datasheet check before the submission quotes them. E12 has
  already had one
- E15 and E16 are assumptions with no source. The endurance requirement that would let the
  derate be calculated rather than chosen does not exist in the problem statement
