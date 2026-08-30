# Evidence ledger and selection rules

Built first, before any sizing, so no number in week 2 gets its authority from the document
that quotes it. Written 2 September 2026.

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

Nothing in this project is class measured. That is worth saying plainly, because a reader
skimming for a thrust coefficient finds 0.6055 sitting in `numbers.json` and could easily
assume somebody put a cyclorotor on a load cell to get it. Nobody did, at least not this one.

## Evidence ledger

| # | Value | Class | Source and exact basis | Area convention | Source geometry | Source Re | How it is used |
| --- | --- | --- | --- | --- | --- | --- | --- |
| E1 | blade-area thrust coefficient 0.6055 | transferred | Benedict 2010 (S2), quad-cyclocopter rotor at hover: 1.98 N per rotor at 2000 rpm. Recomputed here, not quoted | blade area, blades times chord times span | 4 blades, NACA 0010, c/R 0.433, R 76.2 mm, span 158.8 mm | about 35,000 | sets rpm at the design thrust, and through that everything else |
| E2 | blade-area thrust coefficient 0.8114 | derived | Benedict 2010 (S2), twin-cyclocopter rotor: 1.47 N per rotor, 3 blades, same radius, same 2000 rpm | same | 3 blades, c/R 0.333, solidity 0.159 | about 35,000 | upside indication only. Solidity is far outside the measured band so it is not adopted |
| E3 | low coefficient 0.5147 | downside | E1 less 5 percent for blade flexibility and 10 percent for configuration transfer, added rather than compounded | same | not applicable | not applicable | the conservative thrust the decision gate is judged on |
| E4 | figure of merit 0.6 | summary | Kellen 2019 (S5), abstract and companion Forum papers | projected, 2R times span | 3 blades, NACA 0020, c/R 0.66, blade AR 4 | about 200,000 | turns the momentum floor into a working aerodynamic power |
| E5 | solidity band 0.30 to 0.40 | summary | Kellen 2019, stated optimum range | not applicable | as E4 | about 200,000 | the gate on whether E1 may be transferred at all. See D12 |
| E6 | power loading 0.062 N/W | derived | Benedict 2010 (S2), twin rotor at its operating point | blade aerodynamic power | 3 blades, c/R 0.333 | about 35,000 | the independent second power route |
| E7 | rotor tare 10 percent of shaft power | measured | Benedict 2010 (S2), flight-weight rotor. The heavy bench rig burned about 75 percent, same quantity and a different build quality | not applicable | not applicable | not applicable | the tare term between aerodynamic and shaft power |
| E8 | peak to mean blade load 3 to 4 | summary | Alsabri et al., Aerospace 13(9):765, 2025, 2D URANS. Not read here | not applicable | 2 and 3 bladed rotors | not stated | week 4 uses 4.0, per D16 |
| E9 | module thrust to weight 2.13 | derived | Runco and Benedict 2023, Table 3 re-cut onto the competition module boundary: 8.2 g per rotor carrying a flight-demonstrated 17.5 gf | not applicable | 4 blades, flat plate, R 33 mm | 18,600 | the benchmark the mass case is argued against |
| E10 | blade mass per newton is scale invariant | summary | Shrestha and Benedict, JAHS 67(4) 2022. Simulated and validated, not a transcribed measurement | not applicable | geometric similarity | 10,000 to 100,000 | forbids the claim that growing the rotor shrinks blade mass. See D11 |
| E11 | MN3510 KV700: 555 W and 25 A maximum continuous at 180 s, 118 g with leads | catalogue | T-Motor supplier listing, retrieved 2 September 2026 | not applicable | not applicable | not applicable | the selected drive, and its mass line |
| E12 | MN3110 KV470: 330 W and 15 A maximum continuous at 180 s, 98 g with leads, 0.3 A idle, 135 mOhm | catalogue | same | not applicable | not applicable | not applicable | the 13 N sensitivity row |
| E13 | MN2806 KV650: 187 W and 12.3 A maximum continuous at 180 s, 46 g | catalogue | same | not applicable | not applicable | not applicable | shortlist floor, rejected on power |
| E14 | densities: PMI foam 52, CFRP 1550, aluminium 2700 kg/m3, skin 0.22 kg/m2 | catalogue | Rohacell 51 IG class, cured carbon epoxy, 6061, two plies of 60 gsm twill at 45 percent resin | not applicable | not applicable | not applicable | every geometry-scaled mass line |

Four rows deserve sentences rather than cells.

**E1 is the highest risk value in the project, and its source rotor sits outside the band its
destination sits inside.** Our family gives a solidity of 0.3151, comfortably within Kellen's
measured 0.30 to 0.40. The rotor the coefficient came from has a solidity of 0.276, which is
below it. So the transfer runs into the measured band from outside, across a change of blade
count, airfoil and chord ratio at once. D12 gates the destination. Nothing gates the origin,
and nothing can until Kellen's own figure is in hand.

**E3 is a scenario I built, not a bound anybody published.** The repository has carried 0.516
as a low value since the external research round, and that figure was always flagged as a
caution rather than a published limit. It still is. Kellen 2019 holds the measured
coefficient for this exact shape family in roughly our Reynolds band, behind a Cloudflare
browser challenge that needs a person with a browser. Until somebody opens it, the low column
is an engineering downside and the submission says that in those words.

**E4 and E5 are summary class and the thesis is unread.** Its three quoted shape numbers do
check out against each other, which is decent evidence the summary read them correctly.
Still not the same as opening the body.

**E11 to E13 are catalogue figures pulled from supplier listings this week.** Good enough to
size a mass line and to show the design point sits on a continuous rating. They are not a
bench test, and week 4 confirms each against the manufacturer's own datasheet before the
submission quotes it. Recorded as a debt.

## Selection rules

Fixed before any candidate was scored, which is the only thing that makes them worth having.

**The boundary.** The competition's own words: rotor blades, frame, pitch mechanism, motor,
actuator and associated mounting hardware. No battery, no avionics, no airframe. Applied
identically to every candidate, published or ours.

**The two disputed allocations, decided here rather than later.** ESCs count as module
hardware, because the motor does not turn without one. Mounting counts in full, so every
fastener, insert, lug and bonded joint that holds the module together or attaches it to a
vehicle sits inside the line. Both choices push our own number down. On Runco's re-cut they
move the benchmark from 2.13 to roughly 1.78, and the comparison in this week's documents
quotes 2.13 anyway, which is the harder comparison to win.

**Decision metrics, in order.** Conservative thrust to weight first. Then whether a named
drive covers the design point on its continuous rating. Then the largest dimension of the
module. Then part count. Power is reported and does not rank, since no criterion scores it,
but a candidate whose electrical power walks out of the drive shortlist gets rejected on the
drive metric instead.

**The radius rule.** A larger radius lowers aerodynamic power and lowers rpm, and it raises
rotor torque along with every geometry-scaled mass line. Power alone does not choose it. The
candidate table carries rpm, Reynolds, ideal power, aerodynamic power, rotor torque,
electrical power, largest dimension and mass on every row.

**Mass classification.** Every line is geometry-scaled, power or torque-scaled, or fixed. The
motor, the transmission, the ESC and the main shaft are power or torque-scaled and are never
called fixed. That is D15, and it is the difference between an argument that survives a viva
and one that does not.

**The cluster comparison runs in the cluster's favour.** Non-overlapping wakes, no interaction
penalty, one shared motor and one shared controller sized on total power, and the same thrust
coefficient even though splitting the thrust drops per-rotor Reynolds below the band that
coefficient was measured in. If the single rotor still wins on those terms, it wins.

**What freezes geometry.** The conservative case, meaning the low coefficient and the high
mass column together, clearing thrust to weight 2.5 with its inputs carrying evidence. The
internal target is 2.75. Between the two is compliant and red and needs a person to decide.
Below 2.5, nothing freezes.

## Disclosed gaps

- Kellen 2019, Heimerl et al. at the VFS 77th Forum, and Ramsey 2022 are all unread, all
  behind the same JavaScript challenge. Kellen stopped being supporting evidence this week
  and became the load-bearing one, for the reason set out in `stage-1/progress/week-2.md`
- No published cyclorotor states a thrust to weight target and reports whether it met it.
  Searched in week 1, not found
- No openly tabulated spread of blade-area thrust coefficients exists. The values sit inside
  primary figures
- Every catalogue figure in E11 to E14 needs a datasheet check before the submission quotes it
