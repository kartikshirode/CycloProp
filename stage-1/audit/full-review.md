# Full Stage 1 review, all four weeks, and the fix plan

Run 1 September 2026, after week 4 and the 1 September hardening pass. Five fresh-context
auditors read the repository cold, in parallel, with no knowledge of why anything was built the
way it was. Each was read only. Every finding below was reproduced by the supervisor against a
baseline of 208 gate passes and 162 self-tests at commit `d21c01a` before it was written down.

The five passes were: alignment against the official problem statement, delivery against
`stage-1/plan.md`, adversarial attack on `tools/check.py`, independent re-derivation of the
engineering, and cross-document consistency.

**Read this first.** The arithmetic in `numbers.json` is sound. Roughly sixty quantities were
re-derived from scratch by an auditor who wrote its own four-bar solver and its own section
integration, and essentially all of them reproduce to five or six figures. What the review found
is in the two layers wrapped around that arithmetic: a set of first-write physical assumptions
no gate can see, and a set of sentences a later week falsified without moving a number.

Three findings change the design. The rest change documents and gates.

## What did not survive the review

**The gates hold the numerator of thrust to weight and barely hold the denominator.** Thrust and
power are recomputed from geometry and refuse to be flattered; an auditor inflating the
coefficient 30 percent was caught by four independent gates at once. Mass is held by a
25 character basis string, a 25 percent self-consistency band between two lists the same author
writes, and a growth rule. Halving every mass line together passes every gate at a reported
thrust to weight of 6.881. The claim this project has repeated, that every published number is
recomputed from first principles, is true of thrust and power and is not true of mass.

**One auditor built a tree that passes `--all` and `--week 5` cleanly** while carrying no motor,
no shaft, no bearings and no transmission in the module, a 900 g selected motor in no mass line,
foam a thousand times softer than the blade allowable assumes, a blade under its own declared
floor, junk in the pitch schedule and the four-bar, five unwritten audits and a fabricated power
claim in the submission narrative. Reported thrust to weight: 4.959.

## Tier 1: the design may not close

These move numbers. Nothing downstream is worth correcting until they are settled.

### R1. Aerodynamic power spends the thrust conservatism a second time, as optimism

`numbers.json` `performance.aero_power_W`, `04-thrust-and-power.md:96-108`

The design takes the thrust coefficient 9 percent below Kellen's measured value and then
computes power as ideal over figure of merit at that reduced thrust, holding Kellen's figure of
merit at 0.6. Figure of merit is defined by the thrust and power coefficients together, so they
are not independent. Cutting one and holding the other cuts the power demand by 13 percent.

Recomputed at the design point, 2404.79 rpm and 27.7012 m/s over the declared 0.063888 m2:

```
design      C_T/sigma = 0.95120   C_P/sigma = 0.61371
Kellen      C_T/sigma = 1.04427   C_P/sigma = 0.70595   at FM 0.6
power on Kellen C_P at our operating point : 370.1 W
project aero_power_W                       : 321.71 W    15.0 percent low
implied FM holding 18 N against 370 W      : 0.5216
```

The project takes thrust from the case where this rotor underperforms Kellen and power from the
case where it matches Kellen. The favourable half of each.

Downstream, on the consistent reading:

| Quantity | As designed | Consistent | Continuous rating |
| --- | --- | --- | --- |
| motor shaft torque | 0.4361 Nm | 0.5017 Nm | 0.4414 Nm, 114 percent |
| motor input | 457.6 W | 526.4 W | 520 W, 101 percent |
| bus current | 20.61 A | 23.71 A | 20.8 A, 114 percent |

The selected drive does not cover the design point. And 0.52 is not an implausible figure of
merit: Benedict's two flight rotors delivered 0.318 and 0.431, and Kellen's 0.6 is the peak
across 37 configurations and every pitch amplitude, measured on a 139.7 mm chord at Reynolds
186,000 against this design's 72.6 mm and 134,074, and adopted here with no scale or Reynolds
knockdown.

### R2. Motor current is a power over voltage quotient, not a torque derivation

`numbers.json` `performance.motor_input_current_A`

Stored as 457.573 divided by 22.2. Current in a permanent magnet motor comes from torque. With
Kt = 9.5493/450 = 0.021221 Nm/A, the required 0.43608 Nm needs 20.551 A, and the 0.9 A idle
current that evidence row E12 records is dropped from the calculation. That gives 21.451 A
against the 20.8 A the derate allows, so 103 percent. Break even derate becomes 0.825 rather
than the stated 0.7927, and the gate written on 1 September passes only because the stored
current is low.

Unresolved without the manufacturer sheet: whether T-Motor's 26 A figure is a bus current or a
phase current. The two conventions differ by roughly the throttle fraction. Either way the
margin sits between 99 and 104 percent, which is no margin.

There is also no gate anywhere comparing motor shaft torque against the selected motor's
continuous torque, which `04-thrust-and-power.md:216` itself calls the tight one at 99 percent.

### R3. The servo gear ratio is applied backwards

`tools/linkage.py:534-535`

```python
step_up = SERVO_GEAR_MM / CARRIER_GEAR_MM      # 60/40 = 1.5
servo_torque = hold / step_up / SERVO_COUNT     # divides
```

Line 538 uses the same factor to multiply travel, `authority = 80 * 1.5 = 120`, so the carrier
turns 1.5 times the servo angle. Angle amplification at the output is torque multiplication at
the input. The servo has to supply 1.5 times the carrier torque and the code divides by it.

Correct: 0.1389 x 1.5 / 2 servos = 0.1042 Nm each against a usable 0.108 Nm.

**Margin 1.04, not 2.332.** Two 12.5 g servos holding 96 percent of half stall against a 120 Hz
reversing ripple. `08-structure-and-loads.md:130` rests on the wrong number and no gate touches
either figure.

### R4. The bearing static rating carries the tightest margin and has no named source

`tools/structure.py:91`, a supplier listing with no supplier named. ISO 76 for a single row
radial ball bearing gives C0 = 12.3 x 7 x 1.5875^2 = 217 N against the 270 N used, from the ball
complement this project already publishes. At 217 N the overspeed attachment margin falls to
1.361 and the oscillating static safety factor to 1.960, under the 2.0 floor D60 declared.

### R5. Roughly 20 to 32 g of mass lines do not reproduce from their stated geometry

Against a stacked case that clears by 12.5 g.

- Rotor hub bosses: 14 mm bore stated and modelled, on a 16 mm shaft. Physically impossible, a
  week 2 leftover. Plus 1.7 g at the same wall, plus 8.2 g for a real clamp boss
- Bearing blocks: 16.00 g for two, where the stated 34 x 28 x 9 mm 7075 housing with a 24 mm
  bore is 12.64 g each. Plus 9.3 g, with no cutout in the description
- Motor mount plate: 8.00 g against 17.39 g for the stated 55 x 45 x 2.5 mm plate
- Root attachment brackets: a hard coded 3.00 g whose basis claims it was "sized on the
  recomputed centrifugal pull at the declared overspeed". Nothing sizes it
- Shaft end plugs with no allowance for the 15 mm bearing journal the basis describes, plus 5.0 g
- Wiring at 15.60 g total where the stated gauge and length cover a single conductor

## Tier 2: wrong statements in documents that go out

Every one verified. None of them moves a stored number.

| # | Where | Says | Should say |
| --- | --- | --- | --- |
| R6 | `cycloprop-stage1.md:250`, `04:226` | at 20 N "the motor input is still inside the continuous rating, so it is not a power limit", quoting 512.6 W | The stored row is 535.92 W and I reproduced it. That is above 520 W, so it fails on power. D30 says so. 512.6 matches no computed value anywhere |
| R7 | `06:35` against `06:65` | a 32 kg/m3 foam grade takes the overspeed margin under the floor | Rohacell 31 IG is that grade and lands at 1.5443. It clears. The first paragraph drops the mass reduction. Also live in the submission twice |
| R8 | `02:125`, `02:129` | 100 mm at 2645 rpm, 140 mm at 1565 | 2909.8 and 1484.6. Inside the fixed family rpm goes as 1/R squared; these two rows were scaled as 1/R |
| R9 | `evidence-ledger.md:20,23` | "Two rows are now" measured; "E18 and E19 are Kellen's measurements" | Four rows are measured. E19 is a derived Benedict row on a different rotor. The intended pair is E17 and E18 |
| R10 | `literature.md:22,43,204` | S5 "could not be downloaded", the coefficient is "still not in hand" | Kellen was retrieved 31 August and four evidence rows are class measured off it |
| R11 | `02:136` | the 100 mm row would give 2.376 | 2.655. Pre-D35 figure, and at 2.376 the sentence it sits in stops being true |
| R12 | `04:105` | the figure of merit is summary class, the thesis body is unread | E4 is class measured, read off the thesis |
| R13 | `04:13` | the conservative case uses a coefficient 15 percent below nominal, so nominal cannot sit below 11.8 N | The haircut has been 5 percent since D35 and the floor is 10.53 N. D37 says so |
| R14 | `04:164`, `evidence-ledger.md:110` | the other four motor rows came from listings "and week 4 confirms them" | Week 4 opened no manufacturer sheet for any of them |
| R15 | `08:213`, `cycloprop-stage1.md:437` | "two margins sit under 2 and everything else is over 3" | Two of the other six sit between 2 and 3, and the sentence undercuts its own conclusion |
| R16 | `09:112`, `09:153` | airframe reaction torque is motor torque times the belt ratio, 1.526 Nm | 1.41944 Nm. The belt is 93 percent efficient and three other files say so. 7.5 percent high in the number an integrator designs a mount to |
| R17 | `09:59` | ASCII layout draws a 14 mm rotor shaft | 16 mm |
| R18 | `03:36`, `03:20` | 47.5 N offset post pull; conservative mass 4.8 g under the ceiling | 53.22 N since D48; 12.5 g since D47 |
| R19 | `05:54` | week 2 gave nine of thirteen lines a blanket rate | Eight. `02:228` is written specifically to correct this and `05` reproduces the error |
| R20 | `evidence-ledger.md:157,172,178` | 15/20/25 percent growth rates; stacked 2.5173; 692.4 g and 58.6 g | D33's four classes at 8/12/15/25; 2.5457; 684.70 g and 50.87 g |
| R21 | `cycloprop-stage1.md:586` | five evidence classes | Seven are defined and six are used. The conservative coefficient is class downside and has no home in the five |
| R22 | `numbers.json` basis strings | belt "6 to 1"; ESC "25 A continuous"; 0.78 motor gives "552 W"; EI 66.8 and GJ 9.6 with 0.086 mm and 0.054 deg | 3.5 to 1; 20.8 A; 493 W; 51.115, 7.8058, 0.0936 mm, 0.0145 deg. The gate reads numeric fields and never these strings |
| R23 | `cycloprop-stage1.md:67` | module largest dimension 290.4 mm | The swept circle alone is 296.1 mm and the module is 364.4 mm. Fixed in `01` on 1 September and missed here |
| R24 | `cycloprop-stage1.md:75` | falling per rotor Reynolds is another win for the single rotor | `01:75` flags that exact framing as one the audit already caught, and gives both readings. The report keeps only the favourable one |

## Tier 3: gates that certify what they do not check

| # | Gate | Hole |
| --- | --- | --- |
| R25 | `check_audits_exist`, `check.py:2152` | `AUDIT_MARKER not in text` over the whole file. `audit/week-4.md` quotes the marker twice in prose, so deleting the sign off leaves the gate passing. **Reproduced on a mirror of the live repo.** This is the D59 bug, unswept |
| R26 | `done_set` | Same defect for `STATUS: WEEK-COMPLETE`. Four progress files reading "write STATUS: WEEK-COMPLETE once it is finished" all count as done |
| R27 | `MODULE_COMPONENTS`, `check.py:110` | Substring search over concatenated item names. One line named "motor mount bracket and fasteners" satisfies both motor and mount, so a module with no motor, shaft, bearings or transmission passes the gate that exists to prevent exactly that |
| R28 | `check_blade_sensitivity` | Recomputes the wrinkling stress from three moduli and never uses it. `blade_allowable_Nm` is only compared against two other stored numbers. Foam a thousand times softer passes with a 2.0 overspeed margin |
| R29 | Unrecomputed allowables | `shaft_allowable_Nm`, `pitch_link_allowable_N`, `blade_attachment_allowable_N`, `blade_allow_spar_Nm`, both blade sweep results, `shaft_combined_margin` |
| R30 | `check_numeric_coverage` | Accepts a prose number within 2 percent of any stored number in the same dimension. Measured hit rate for a fabricated value: 57.8 percent for watts, 50.2 for degrees, 33.3 for grams. Five wrong numbers injected into the live submission all traced |
| R31 | Candidate comparison, `check.py:887` | `module_tw_conservative` is never recomputed from the row's own mass and thrust, and `module_tw` is checked by nothing. The worst of three configurations can be declared the winner |
| R32 | `drive_candidates.mass_g` | Required by the row shape and read nowhere. A 900 g motor can be selected and not carried |
| R33 | Chained tolerance in the structural chain | Four links compared at DISPLAY_TOL against the previous stored value. Four 1.95 percent shaves take a true 1.428 overspeed margin to a reported 1.505 |
| R34 | `states_value`, `check.py:294` | Accepts any numeric token within 0.5 percent. The stacked thrust to weight sentence is satisfied by an unrelated belt ratio of 2.606 |
| R35 | Two `report(True, ...)` branches at `check.py:1794` and `:1866` | Pass on both arms. D61 claims one of them is gated. It is a printed observation |
| R36 | Schema guards | Every key added by D53, D60, D61 and D63 can be deleted to make its gate vanish. Week 2 protects its block with `require_positive` and the later gates did not copy the pattern |
| R37 | `bom` | 25 rows, 9 fields, four derived totals, zero gates. `grep -ci bom tools/check.py` returns 0. Backs the 10 percent manufacturability and cost criterion |
| R38 | Ungated stored values | `servo_torque_margin`, both transmission angles, `axis_keepout_mm`, `pitch_schedule` and `linkage_dimensions` in `numbers.json`, `vector_map` force magnitudes, `swept_diameter_mm`, and 47 numeric leaves in total |
| R39 | `MIN_BASIS_CHARS` | A length test. Twenty six junk characters is a basis |
| R40 | Solidity gate, `check.py:1017` | Passes the failure wording as `detail`, so a passing run prints "so the transferred coefficient needs re-deriving". D29 exists to prevent this |
| R41 | `linkage_selftests` | Returns an empty list if any of five keys is absent, and three of the five are required by no gate. The four-bar closure check can be switched off and the suite still reports success |
| R42 | `pdf_selftests` double f probe | Passes with the ligature expansion deleted, because the PDF also contains un-ligatured occurrences. Its sibling probe holds, so the pair is sound, but this one passes for the wrong reason |

## Tier 4: content the submission does not carry

| # | What | Cost |
| --- | --- | --- |
| R43 | **Zero figures in 21 pages.** No rotor layout, no linkage sketch, no pitch schedule plot, no blade section, no assembly view. The four-bar is four numbers in a table | Touches criteria summing to 30 percent: kinematic design 15, CAD and packaging 5, presentation and clarity 10. The report claims a dimensioned layout it does not contain |
| R44 | `09-packaging-and-integration.md` reaches the submission nowhere. All four envelope numbers return zero hits | The 5 percent packaging criterion is answered by pointing at a section that has none of it |
| R45 | Virtual camber is never named. 52 mentions in the Benedict extract, 18 in Kellen, zero here | At c/R 0.66 the effect is larger than at Benedict's 0.43, where he calls it significant. It is also the strongest available defence of the coefficient transfer, since Kellen's shape family matches ours |
| R46 | The problem statement's only mandatory sentence about design content was never transcribed into `context.md`: "Teams must support their design through CAD models, kinematic analysis, aerodynamic calculations or simulations, structural assessment, mass estimation, material selection, actuation strategy, and an implementation plan" | Eight items named, seven delivered, and the missing one is CAD. The position that Stage 1 is not a CAD deliverable may hold, but it was reached without confronting the strongest sentence against it |
| R47 | Structural work, a 15 percent criterion, is nested under a heading titled material and manufacturing | The report's strongest technical content is the hardest to find |
| R48 | Effort against weight | Appendix A, serving a Stage 3 viva, is the largest section in the report. Thrust and power, sole home of two 15 percent criteria, is 10.2 percent of the words |
| R49 | Confidentiality is never asserted, though the problem statement invites it | One free line |
| R50 | Nothing re-checks the official channels between the 26 August requirements snapshot and the 26 September send | The problem statement reserves the right to change any stage and says changes come through official channels |

## Tier 5: records and steering files

| # | What |
| --- | --- |
| R51 | Four files say week 5 blocks on four markers. The code requires five. `plan.md:211,503`, `weekly-loop.md:71`, `human-gate.md:4,47` |
| R52 | `human-gate.md` tells a person to add each marker and then lists only the PENDING strings, never the four CONFIRMED ones they have to type |
| R53 | `audit/week-5.md:59` still reads "deliberately not changed" about the gate D59 then changed, in a paragraph that now names D59 and contradicts itself |
| R54 | Stale counts: `handoff.md:25` 63 decisions against 64; `codemap.md:155` D1 to D58; `codemap.md:56` 128 self-tests against 162; `plan.md:28` eleven attacks against 117 fixtures; `07-team-and-execution.md:140` 128 self-tests, inside a required Stage 1 item |
| R55 | `weekly-loop.md:75` "Nothing here has run a tick yet", after four weeks |
| R56 | `plan.md:550` "Three papers are still unread". Kellen was retrieved 31 August |
| R57 | The calendar in `plan.md:147-183` places weeks 2 to 4 between 2 and 22 September. They landed 30 and 31 August. Week 5 still reads as a sprint carrying the deadline and there are more than three weeks of slack |
| R58 | No journal entry for the 1 September hardening pass, D59 to D64, against the plan's own end of session rule |
| R59 | Week 2 debts 4, 5 and 7 carry owner "week 4" and appear in no later ledger. Debt 4, the three assumed efficiencies, sets motor input power and therefore the drive selection |
| R60 | Six debts recorded as open in the files a fresh session is told to read are closed, and one instruction inside frozen decision D30, to price the lower KV route, was reassigned to nobody |
| R61 | `organiser-email.md` and `handoff.md` say two questions ride with the submission. The email draft asks one. `human-gate.md` points the human at a file that says the questions are somewhere else |
| R62 | Week 2 delivered one shortlist where the plan asked for three. The ESC is a single mass line with no named part and the transmission was never shortlisted. No decision records the reduction |
| R63 | Week 1's gate is five heading strings and ignores its data argument, so "Done when `--week 1` exits 0" carries almost no weight |

## The plan

Six phases. The order is not negotiable in one place: gates come before the numbers they hold,
because a gate written after the fix is a gate nobody has seen fail.

### Phase 1: make the gates fail

Write the gates that expose Tier 1 and watch them reject the current repository. This is the
only phase that produces a red tree on purpose.

1. Recompute the blade allowable inside `check.py` from the section and the moduli rather than
   reading it, closing R28 and R29. The section integration has to move where the gate can reach
   it or the gate has to call the solver
2. Derive motor current from torque and the torque constant, and gate motor shaft torque against
   the selected motor's continuous torque. Closes R2's gate half and R32
3. Gate the servo margin, both transmission angles and the axis keepout. Closes part of R38
4. Gate figure of merit against the coefficient it was transferred with, so R1 cannot recur
5. Word boundary and distinct line rules on `MODULE_COMPONENTS`, plus a required drive line whose
   mass matches the selected candidate. Closes R27 and R32
6. Marker gates read a status block and match whole lines, everywhere, not only in the human
   gate. Sweep for the pattern. Closes R25 and R26
7. `require_positive` schema lists for every key added since D53. Closes R36
8. BOM row shape, line arithmetic and totals. Closes R37
9. Candidate thrust to weight recomputed from the row's own mass and thrust. Closes R31
10. Tighten the structural chain to `TOL` and stop comparing against shaved stored values.
    Closes R33
11. `states_value` requires the number to sit near words that name it. Closes R34
12. Narrow the coverage window, and extend the coverage audit to the nine design documents rather
    than the submission alone. Closes R30
13. Fix the two `report(True)` branches and the solidity `fail_detail`. Closes R35 and R40
14. `linkage_selftests` fails loudly instead of returning empty. Closes R41

Expect the tree to be red at the end of this phase. That is the point.

### Phase 2: settle Tier 1 and make the tree green again

15. **R1.** Adopt one self-consistent reading of thrust and power. Recommendation below
16. **R3.** Invert the servo torque calculation, then resize the actuator or the gear pair
17. **R2.** Recompute current from torque, add the idle current, restate the derate break even
18. **R4.** Name a catalogue page for the 693ZZ or adopt the ISO 76 rating and carry the
    consequences
19. **R5.** Redraw the six mass lines that do not reproduce, then rerun the thrust to weight cases
20. Regenerate `numbers.json` with `linkage.py --write` then `structure.py --write`, and record
    every number that moved

### Phase 3: correct the documents

21. R6 to R24, in one pass per document, then rebuild the submission and the PDF
22. R22 is inside `numbers.json` and needs the solver's source strings changed, not the file

### Phase 4: add what is missing

23. **R43, the figures.** `tools/figures.py` rendering from `numbers.json` so every figure is
    reproducible and gated the same way every number is. matplotlib 3.11.1 and numpy are
    installed and the data is already stored: 37 pitch schedule rows, 36 azimuthal load rows, the
    vector map, 33 budget lines, six linkage dimensions. Seven figures: module general
    arrangement, four-bar kinematic diagram, pitch schedule, azimuthal blade load, thrust vector
    map, blade section, mass breakdown
24. **R44.** Fold the packaging section into the submission, with the envelope numbers
25. **R45.** A virtual camber paragraph in item 4, used as the defence of the transfer rather than
    as a confession
26. **R46.** One sentence in the submission saying why the CAD clause is read as programme level
27. **R47.** Promote the structural work to a visible heading. R48, R49 as cheap wins

### Phase 5: records and steering

28. R51 to R63. Mechanical, and the marker count and the human gate wording matter most because
    the only person who can unblock this project reads that file

### Phase 6: re-audit

29. Rerun the five passes against the fixed tree. A fix nobody attacked is a fix nobody has
    tested

## What needs a person

**The Tier 1 reading, R1.** The recommendation is to adopt the consistent reading: state figure
of merit at 0.52, aerodynamic power at 370 W, and re-run the drive selection against it. It makes
the design look worse and it is what the evidence supports, which is how every correction in this
project has gone. The consequence is that the MN5006 no longer covers the design point, and motor
mass is a power class item with 12.5 g of headroom, so this can reach the radius freeze. The
alternative readings are defensible and all of them are worse arguments.

**The 26 A convention, R2.** Needs the manufacturer datasheet. Bus or phase changes the answer.

**The 693ZZ rating, R4.** Needs a named catalogue page, or the ISO number stands.

**The registration reference.** `CP-439436FADAD2` was supplied on 1 September. It matches neither
`id = 14` nor `compi_id = cycloprop` in the stored API payload, so it is probably a team
registration reference and `[P-7]` is probably where it goes. Probably is not good enough for a
string that goes in a submission subject line, and confirming registration is a fact only a person
holds, so it is recorded here and written nowhere else.
