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

Until 31 August 2026 nothing here was class measured. Two rows are now, and the distinction
they rest on has to be stated precisely, because it is easy to overclaim.

Nobody has put this rotor on a load cell. E18 and E19 are Kellen's measurements on Kellen's
rotor, and that rotor is this design's shape family rather than this design: 3 blades, NACA
0020, chord-to-radius 0.6667 against our 0.66, solidity 0.3183 against our 0.3151, blade aspect
ratio 4.0 in both, pitching plus or minus 40 degrees in both. Solidity and chord-to-radius agree
to 1.1 percent, which is the test `tools/check.py` applies before it will treat a measurement as
covering this family. Chord Reynolds on his rotor is 186,000 and ours is 134,074, both inside
the 100,000 to 300,000 band he measured across.

So "measured" here means measured on this geometry at this scale by somebody else, not measured
on our hardware. E1, the coefficient the design is actually built on, is still not measured and
is still labelled for what it is.

## Evidence ledger

| # | Value | Class | Source and exact basis | Area convention | Source geometry | Source Re | How it is used |
| --- | --- | --- | --- | --- | --- | --- | --- |
| E1 | blade-area thrust coefficient 0.6055 | transferred | Held value, and its stated basis was wrong. It was built from 1.98 N per rotor at 2000 rpm, a pair Benedict never states: 1.98 N is the 809 g all-up weight of Table 5.1 over four and 2000 rpm is the twin's speed. The real quad point is E19. 0.6055 is kept as deliberate margin under D36, below all three measured or corrected values | blade area, blades times chord times span | 4 blades, NACA 0010, c/R 0.433, R 76.2 mm, chord 33.0 mm, span 158.8 mm | 31,600, not the 35,100 this row used to carry | sets rpm at the design thrust, and through that everything else |
| E2 | blade-area thrust coefficient 0.8114 | derived | Benedict 2010, twin-cyclocopter rotor at the same 76.2 mm radius and the same 2000 rpm, recomputed the same way. Verified against the source: printed p.229 gives 300 grams total for two rotors, so 1.47 N per rotor, and p.232 rounds the same point to 1.5 N | same | 3 blades, chord 25.4 mm, span 152.4 mm, c/R 0.333, solidity 0.159 | 27,000 | upside indication only. Solidity is far outside the measured band, so it is not adopted |
| E3 | low coefficient 0.5752 | downside | E1 less 5 percent for blade flexibility, and nothing else. The 10 percent configuration-transfer allowance retired against E18, which is the test D23 set. The retired 0.5147 stays in `numbers.json` as the record of what it used to be | same | not applicable | not applicable | the conservative thrust the decision gate is judged on |
| E4 | figure of merit 0.6 | measured | Kellen 2019 section 3.3, read off the thesis: the peak figure of merit was found to be 0.6, on the 3-bladed rotor with a 5.5in chord, 22in. span and 8.25 in radius. Reading CT/sigma off Fig 3.25 and CP/sigma off Fig 3.26 and closing FM = CT^1.5/(sqrt(2)*CP) gives 0.595, so the stated figure reproduces to 0.8 percent | projected, 2R times span | 3 blades, NACA 0020, c/R 0.6667, blade AR 4 | 186,000 | turns the momentum floor into a working aerodynamic power. Load bearing, and no longer summary class |
| E5 | solidity band 0.30 to 0.40 | measured | Kellen 2019 section 3.2.7, read off the thesis: the optimal rotor solidity was found to fall between 0.30 and 0.40, with power loading in Fig 3.30 roughly flat to a solidity of about 0.35 and falling after it | not applicable | as E4 | 186,000 | the gate on whether E1 may be transferred at all. See D12 |
| E6 | power loading 0.062 N/W | derived | Benedict 2010 printed p.232, verified: at the operating thrust of 1.5 N (per rotor), the power loading of the rotor was 0.062 N/W. The quad reaches 0.076 N/W on p.236, so this is the lower of the two and it is the one used | blade aerodynamic power | 3 blades, c/R 0.333 | 27,000 | the independent second power route |
| E7 | rotor tare 10 percent of shaft power | transferred | Benedict 2010, measured on his flight-weight rotor and verified at printed p.232 and p.236, where the structure power is 10 percent of the total on both vehicles. The heavy bench rig burned about 75 percent, same quantity and a different build quality | not applicable | 4 blades at 76.2 mm radius | 31,600 | the tare term between aerodynamic and shaft power. Measured, but not on this rotor, so transferred |
| E8 | peak to mean blade load 3 to 4 | summary | Alsabri et al., Aerospace 13(9):765, 2025, 2D URANS. Not read here | not applicable | 2 and 3 bladed rotors | not stated | week 4 uses 4.0, per D16 |
| E9 | module thrust to weight 2.13 | derived | Runco and Benedict 2023, Table 3 re-cut onto the competition module boundary: 8.2 g per rotor carrying a flight-demonstrated 17.5 gf | not applicable | 4 blades, flat plate, R 33 mm | 18,600 | the benchmark the mass case is argued against |
| E10 | blade mass per newton is scale invariant | summary | Shrestha and Benedict, JAHS 67(4) 2022. Simulated and validated, not a transcribed measurement | not applicable | geometric similarity | 10,000 to 100,000 | forbids the claim that growing the rotor shrinks blade mass. See D11 |
| E11 | Reynolds invariance of non-dimensional thrust holds from 10,000 to 100,000 | summary | Shrestha and Benedict, JAHS 67(4) 2022, same source as E10 | not applicable | geometric similarity | the range itself | still the only support under the Reynolds half of the E1 transfer, and the design point still sits above it. What changed is that the shape family now has its own measurement bracketing the design point, E17 and E18, so this row no longer carries the question alone. See D25 as narrowed by D37 |
| E12 | MN5006 KV450: 650 W and 26 A maximum for 180 s, 106 g with cable, 60 mOhm, 0.9 A idle at 22 V, 4-6S | catalogue | Supplier datasheet PDF, read directly, 2 September 2026 | not applicable | not applicable | not applicable | the selected drive and its mass line, after the 0.80 derate in E15 |
| E13 | MN3510 KV700 555 W / 25 A / 118 g; MN4006 KV380 380 W / 17.5 A / 57 g; MN3110 KV470 330 W / 15 A / 98 g; MN2806 KV650 187 W / 12.3 A / 46 g, all at 180 s | catalogue | Supplier listings, 2 September 2026. Not read off datasheet PDFs like E12 | not applicable | not applicable | not applicable | the rest of the drive shortlist and the sensitivity rows |
| E14 | densities: PMI foam 52, CFRP 1550, aluminium 2700 kg/m3, skin 0.22 kg/m2 | catalogue | Rohacell 51 IG class, cured carbon epoxy, 6061, two plies of 60 gsm twill at 45 percent resin | not applicable | not applicable | not applicable | every geometry-scaled mass line |
| E15 | continuous duty is 0.80 of the 180 s rating | assumed | No source. T-Motor publishes a three minute maximum and the problem statement states no endurance requirement, so there is nothing to size a derate against | not applicable | not applicable | not applicable | turns every catalogue rating into the continuous figure the drive is selected on |
| E17 | Kellen's test range, chord Reynolds 100,000 to 300,000 | measured | Kellen 2019 abstract, read off the thesis: the effect of pitch kinematics and rotor geometry on the performance of a cyclorotor operating at Reynolds numbers between 100,000 and 300,000. Table 2.1 lists all 37 configurations tested inside it | not applicable | as E4 | the range itself | the design point at 134,074 sits inside the band this shape family was measured across, which is what narrows D25. See D37 |
| E18 | blade-area thrust coefficient 0.6648, measured on this shape family | measured | Kellen 2019, Table 2.1 configuration 8. CT/sigma read off the vector paths of Fig 3.25 (1.04424) and Fig 3.28 (1.04428), agreeing to 0.003 percent, converted by coeff = (2/pi)(CT/sigma) out of Kellen's A = span times 2R convention. Cross-checked twice: FM closes at 0.595 against his stated 0.6, and power loading at his stated 60 N/m2 disk loading closes at 0.1202 against Fig 3.27's 0.1201 | blade area, converted from Kellen's projected area | 3 blades, NACA 0020, 5.5 in chord, 8.25 in radius, 22 in span, c/R 0.6667, solidity 0.3183, pitch plus or minus 40 degrees | 186,000 | retires the configuration-transfer half of the haircut, which is D23's test and D35's answer. Not adopted as the nominal, per D36 |
| E19 | blade-area thrust coefficient 0.7211 | derived | Benedict 2010 printed p.236, at the operating RPM of 1800, each rotor produced around 1.91 N of thrust, repeated as 195 grams at 1800 rpm on p.225. Geometry from p.220 and p.233. This is what E1 should have been | same as E1 | as E1 | 31,600 | the corrected quad point. Held in reserve rather than adopted, per D36 |
| E16 | efficiencies: belt 0.93, motor 0.84, ESC 0.95 | assumed | No source. Belt drive is published at 0.95 to 0.98 at these speeds so 0.93 is pessimistic; the motor figure is the sensitive one and at 0.78 the motor input rises from 458 W to 493 W | not applicable | not applicable | not applicable | the whole electrical power chain and the drive selection |

Seven rows deserve sentences rather than cells.

**E1 had the wrong basis written under it for the whole of weeks 1 and 2.** The row said 1.98 N
per rotor at 2000 rpm on Benedict's quad. Reading the dissertation, that pair is not in it.
1.98 N is the 809 gram all-up vehicle weight of Table 5.1 divided by four, and 2000 rpm is the
twin rotor's speed. The quad's actual hover point is 1.91 N at 1800 rpm, printed p.236, and
that recomputes to 0.7211. Two errors that happened to run in opposite directions, and the net
was a value 16 percent below the truth, which is the safe direction. The stored 0.6055 is not
changed, because raising a nominal coefficient raises thrust everywhere it is used and spends
margin the design does not need. It is now held on purpose rather than by accident. See D36.

**E1 is still the highest risk value in the project, and it is now an extrapolation on one axis
rather than two.** Our family gives a solidity of 0.3151, inside Kellen's 0.30 to 0.40, which
is what D12 asks. The rotor the coefficient came from sits at a solidity of 0.276, so the
transfer still runs into the band from outside it. The Reynolds axis is the one that moved. The
design point at 134,000 is still above the 100,000 top of E11, but E17 and E18 put a measurement
of this exact shape family across 100,000 to 300,000, with the measured rotor itself at 186,000.
The design point is inside a measured band now, even if the provenance of the nominal is not.
D37 narrows D25 to that.

**E3 is a scenario I built, not a bound anybody published, and half of it retired.** The
configuration-transfer allowance covered a change of blade count, airfoil and chord ratio that
nothing measured. E18 measures it: 0.6648 on a rotor within 1.1 percent of ours on both solidity
and chord-to-radius, above the nominal. That is exactly the test D23 set, so the allowance is
gone and the low coefficient is 0.5752. The blade-flexibility half stays, and the row stays
class downside, because a haircut I chose is not a published lower bound whatever evidence sits
next to it.

**E4 and E5 were summary class doing load-bearing work and are not any more.** The figure of
merit turns the momentum floor into the 321.7 W the whole power chain and the drive selection
rest on, and until now it came from an abstract. Section 3.3 of the thesis states it directly
for the 3-bladed rotor with a 5.5in chord, 22in span and 8.25 in radius. It also survives an
independent closure: taking CT/sigma from Fig 3.25 and CP/sigma from Fig 3.26 for that rotor and
computing FM = CT^1.5/(sqrt(2)*CP) gives 0.595. The three shape numbers quoted from the old
summary all check out against Table 2.1.

**E18 is read off a plot, and that is worth being exact about.** Kellen tabulates none of this;
CT/sigma exists only inside figures. The value came from the PDF's vector path data rather than
from pixels or from eye, so the axis calibration is the tick geometry itself and the data points
are the polyline vertices matplotlib wrote. Two separately drawn figures give 1.04424 and
1.04428. Two independent closures then tie the reading to quantitative claims in the surrounding
text: the figure of merit lands within 0.8 percent of Kellen's stated 0.6, and the power loading
at the 60 N/m2 disk loading his own text names lands within 0.15 percent of Fig 3.27. It is a
measurement, and it is a measurement transcribed from a picture, so the ledger says so.

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

**What freezes geometry.** Written before scoring as the stacked conservative case, meaning the
low coefficient and the high mass column together, clearing thrust to weight 2.5 with its
inputs carrying evidence. D30 changed that rule after the numbers came in and the change is
recorded rather than quietly applied. Geometry now freezes on three hard cases: the design
point, the mass downside alone and the coefficient downside alone, each above 2.5. The stacked
case has to be stated and reproduce, and a miss would have handed week 4 a computed mass target.
That branch is now unused: since D35 the stacked case is 2.517 and clears the limit, so the
target is gone from `numbers.json` rather than sitting there stale. The hard stacked test still
moved to week 4, where the mass lines are real sections and catalogue parts instead of eight
lines carrying a blanket 20 or 25 percent growth rate, six of them on an assumed section. Week 4
also has to build its conservative column line by line rather than state a total, which is D33.
The 2.75 internal target from D17 stands as a target and is still not met on the stacked case:
it wants the conservative column at 633.8 g against the 692.4 g it holds, a gap of 58.6 g.

## Disclosed gaps

- Kellen 2019 and Benedict 2010 are read. Both were retrieved from the Wayback Machine on 31
  August 2026 after the live OAKTrust and DRUM routes failed, and `reference/README.md` carries
  the URLs that worked. Heimerl et al. at the VFS 77th Forum and Ramsey 2022 are still unread.
  Heimerl would replace the assumed peak-to-mean blade load in E8, and Ramsey would give a
  second structural mass anchor against the single one E9 provides
- No published cyclorotor states a thrust to weight target and reports whether it met it.
  Searched in week 1, not found
- No openly tabulated spread of blade-area thrust coefficients exists, which is why E18 had to
  be read off a plot. The values sit inside primary figures and Kellen tabulates none of them
- E13's four catalogue rows need a datasheet check before the submission quotes them. E12 has
  already had one
- E15 and E16 are assumptions with no source. The endurance requirement that would let the
  derate be calculated rather than chosen does not exist in the problem statement
