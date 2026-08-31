# Week 3: pitch, thrust vectoring, packaging

31 August 2026. Covers required item 3, the thrust vectoring requirement at 15 percent, and the
integration half of the 5 percent packaging criterion.

STATUS: WEEK-COMPLETE

Geometry stayed frozen and no mass line moved. What week 3 added is a solved mechanism, the
pitch schedule it actually produces, a rerun of the week 2 load model against that schedule, the
vectoring sizing, the packaged envelope and a real draft PDF.

## What the week was meant to produce

The plan lists eight tasks. All eight ran.

1. Confirm the architecture week 2 screened in, and check the actuator and linkage mass against
   the week 2 envelope
2. Solve a real linkage, with topology, pivots, link lengths, loop closure, assembly mode,
   transmission angle, joint travel, clearance and singularity
3. Produce the pitch schedule from that solution and feed it back into week 2's azimuthal load
   model
4. Size the vectoring input: travel, stop range, holding torque, slew time, electrical draw, on
   a named actuator
5. Map command to force at three or more phase commands
6. Handle the side force against the measured literature range
7. Package the moving mechanism, with the swept envelope, interfaces and the reaction torque
   path
8. Start final assembly: seven submission headings and one real pandoc and xelatex build

## What it produced

**A solved four-bar, one per blade, sharing a common offset pivot.** Kellen's topology, scaled
where the sweep supported scaling and re-chosen where it did not. L1 110.0 mm, L2 15.40 mm, L3
105.0 mm, L4 24.4 mm. Only L2 was solved, by bisection on peak to peak pitch travel. Grashof
double crank with the ground as the shortest link, so the rotor arm turns fully and so does the
pitch link about the offset pivot. Transmission angle 58.58 to 143.23 degrees, worst sine 0.599,
nearest approach to a dead centre 36.8 degrees. See D38.

**A 37 row pitch schedule that closes.** Amplitude 39.998 degrees on a 0.25 degree grid, peak at
101.0, phase delay 11.00 degrees, rms residual against the harmonic 1.1951 degrees over the 36
distinct azimuths. The revolution closes at -8.0504 at both ends. Every row comes from the loop
closure, and `tools/test_gates.py` now proves it independently of the solver: one degree of hand
editing on one row shows as 0.38 mm of loop residual against 6.8e-8 mm for the published table.

**The week 2 load model, rerun rather than replaced.** `tools/linkage.py` reconstructs it from
the description in `04-thrust-and-power.md` and reproduces the published week 2 table to 5.2e-5
N on every one of its 36 rows before it changes anything. Then the schedule becomes the solved
one and the uniform inflow points opposite the resultant instead of at module vertical. Peak
blade load 14.24 to 15.01 N, peak to mean 2.374 to 2.501, and the two halves of the revolution
stop mirroring each other. Cycle mean vertical force is unchanged at 6.0000 N per blade, so the
week 2 gate that the loads average to the design thrust still passes on the new table. See D41.

**Side force stopped being zero.** The lateral column now carries real numbers, its cycle mean
is trimmed out by pointing the offset 11.978 degrees off vertical, and the instantaneous lateral
force reaches 10.10 N per blade inside the cycle.

**Vectoring sized on hardware rather than on angles.** 120 degrees of phase authority, from 80
degrees of published servo travel through a 1.5 step up set by a 60 mm sector gear on a 40 mm
carrier ring. Carrier torque peaks at 0.1371 Nm, the two servos hold 0.0457 Nm each through the
gearing, and the margin on half stall is 2.36. Slew 0.147 s end to end, draw 2.88 W against the
6.0 W week 2 carried. See D42.

**A packaged envelope built from the swept volume.** Swept outer radius 148.03 mm and inner
86.54 mm, so a 296.1 mm swept diameter against a 220 mm rotor. Module envelope 364.4 by 316.1 by
362.1 mm as a sum of named parts. Four mount points, reaction torque path and both interface
tables in `09-packaging-and-integration.md`.

**Two documents and a draft submission.** `03-pitch-and-vectoring.md` at 3147 words and
`09-packaging-and-integration.md` at 1291. `stage-1/submission/cycloprop-stage1.md` carries all
seven required headings with items 1 to 4 filled from frozen work and items 5 to 7 marked for
the weeks that own them.

## The PDF build, since the plan asks for the command and the readback

```
pandoc stage-1/submission/cycloprop-stage1.md --from=markdown --pdf-engine=xelatex \
  --toc --number-sections -o stage-1/submission/cycloprop-stage1.pdf
```

pandoc 3.9 with MiKTeX-XeTeX 4.18, exit 0, 45,054 bytes, 6.9 seconds. Read back with pypdf
6.10.0: 5 pages, 9,806 characters of extractable text. All seven required item headings are
present in the extracted text, and spot probes for 0.6055, 2.5173, 11.98, 58.58, 364.4 and the
phrase "120 degrees of phase authority" all resolve. This is the 15 September smoke build,
delivered early.

## What changed outside week 3's own files

- `stage-1/design/04-thrust-and-power.md`, azimuthal load section rewritten against the solved
  schedule, with the full revolution tabulated because the halves no longer mirror.
  `performance.blade_load_peak_to_mean` moved from 2.374 to 2.501 in `numbers.json` and in the
  document's Numbers used block
- `tools/check.py` gained five checks and one helper. Nothing was loosened. See D42
- `tools/test_gates.py` gained five attack cases, a lateral column and a wider force map in the
  fixture, and a read-only `linkage_selftests` pass over the stored four-bar. 104 self-tests to
  115
- `tools/linkage.py` is new. It is the solver, and it writes `numbers.json` under `--write` so
  the schedule is reproducible instead of asserted

## Gate state at the end of the week

| Command | Result |
| --- | --- |
| `python tools/check.py --week 3` | exit 0, cumulative over weeks 1 to 3 |
| `python tools/check.py --global` | exit 0 |
| `python tools/test_gates.py` | exit 0, 115 self-tests |

## Decisions

D38 to D44. Linkage geometry frozen, the azimuth convention, the single ended drive, the load
model rerun, the vectoring claim and its gate, the unbalanced blade, and the packaging rule
correction.

## Debts carried forward

1. **The blade is not chordwise balanced.** Centre of mass at 39.92 percent chord against a 30
   percent pitch axis. That doubles the peak blade pitching moment to 2.1201 Nm and takes the
   pitch link to 101.82 N. Week 4 decides whether to spend mass on balancing it. The stored
   numbers are the unbalanced ones. See D43
2. **The three per revolution carrier ripple is not bounded.** 0.1371 Nm at 120 Hz is above any
   servo's control bandwidth, so it is reacted through the gear train and the reflected motor
   inertia rather than by the holding torque. The static margin is 2.36 and covers it. The phase
   jitter it produces needs a real servo gearbox ratio and rotor inertia, which week 4 has to
   supply or the number stays open
3. **The offset strut is unsized.** It takes 47.48 N of peak radial pull from the three pitch
   links and it is structure. Week 4
4. **The gear pair is not in the week 2 envelope's stated basis.** The pitch mechanism line
   itemises pitch bearings, links, rod ends, the offset ring, its two support bearings and three
   pivots. It does not name the sector gear and ring gear that couple the servos to the carrier.
   The line total did not move this week because nothing was added to it, and that is the point:
   a part exists in the design that its own basis does not list. Week 4 either finds it inside
   the line or grows the line
5. **The aerodynamic side force is under-predicted and the design knows it.** The model gives
   0.98 degrees of aerodynamic tilt on top of the mechanism's 11.00. Measurement gives 10 to 45
   for the whole tilt. The design carries an indexed mechanical bias plus bench trim, and the
   uncertainty costs up to 35 degrees of the 120 degree authority. Heimerl would replace the
   estimate with a measurement and is still unpulled
6. **Transmission angle reaches 143.23 degrees**, which is 3.23 degrees outside the conventional
   40 to 140 band on the obtuse side. Reported as a worst sine of 0.599 rather than hidden. Not
   a singularity risk and not worth a geometry change on its own
7. **The servo is a supplier listing.** Corona DS-929MG class: 12.5 g, 0.216 Nm stall, 80 degrees
   travel, 0.11 s per 60 degrees, 0.24 A. This joins the existing debt on four of the five week 2
   motor rows. Week 4 confirms against manufacturer sheets
8. **`largest_dimension_mm` in the week 2 tables is 290 mm and the packaged module is 364.4 mm.**
   The comparison the week 2 table made is unaffected and the ordering is unchanged. See D44
9. **The submission draft is a skeleton.** Items 5 and 6 name what week 4 fills, item 7 names
   week 5 and week H. Its numeric coverage has not been run against the week 5 gate

Week 2's debts are unchanged except where D41 and D44 touch them. The 58.6 g margin gap to the
internal 2.75 target is still week 4's.

## Week H gap

All five markers in `stage-1/human-gate.md` are still pending, so `07-team-and-execution.md` was
not drafted. The plan moves it from week 5 to "week 3 onward, as soon as week H has returned",
and week H has not returned. No real names, institutions or capabilities were written anywhere,
and the submission draft says the section is deliberately empty rather than filling it with
placeholders that read like names.

This is now the item with the longest lead time in the project. It hard blocks week 5.

## What week 4 needs to know

- Geometry, the mechanism and the load model are all frozen. Week 4 inherits a pitch link load
  of 101.82 N, a blade pitching moment of 2.1201 Nm, a carrier torque of 0.1371 Nm and a 47.48 N
  radial pull into the offset strut, all at the design point and all on the unbalanced blade
- The blade balance decision is week 4's and it moves mass. So does the gear pair in debt 4.
  Both eat into a conservative column that clears 2.5 by 4.8 g
- The shaft stops inboard of the pitch plane and the drive is single ended. That is D40 and it
  constrains any shaft stiffness answer
- Peak to mean is 2.501 from the model and week 4 still sizes on 4.0 under D16. Nothing about
  this week changes that
- `pitch.blade_pitch_inertia_kgm2` is 1.1176e-05 on a uniform density section scaled to the week
  2 blade mass. A real section will move it, and both the inertial and the centrifugal pitching
  moments scale with it
