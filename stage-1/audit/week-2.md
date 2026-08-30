# Week 2 audit

Fresh-context read-only audit, 2 September 2026. Findings are reproduced below exactly as the
auditor returned them. What was done about each is recorded after the list, and in
`stage-1/progress/week-2.md`.

---

I have what I need. Running the three gates confirmed the reported state exactly: `--week 2` fails on one line (`week2: conservative mass and thrust still clear T/W 2.5  T/W 2.389 at 17.00 N and 725 g`), `--global` passes, `test_gates.py` reports 77/77. No uncommitted changes; the diff touches ten files and no file under `tools/`.

## Findings

**1. The design point sits outside the Reynolds window D12 says the coefficient transfer is safe over, and three documents claim the opposite.**
`stage-1/decisions.md:137` states the transfer's support: "non-dimensional thrust is roughly Reynolds invariant from 35,000 to 100,000". The week 2 design point is Re 141,327 (`numbers.json` `operating.reynolds`), 41 percent above that ceiling. `stage-1/design/04-thrust-and-power.md:31-32` nonetheless asserts "the Reynolds half of that transfer is defensible" with no new support, and `02-rotor-sizing.md:16-18` argues it "lands inside the band rather than extrapolating out of it" by substituting Kellen's *study* band (100,000-300,000, which is where E4's figure of merit and E5's solidity optimum live) for the band Benedict's coefficient was actually measured in (E1: "about 35,000"). Nothing in the diff notes that the move from 10 N to 20 N is what consumed the headroom: in this family Re scales as sqrt(T), so 10 N gives Re 99,933, exactly the "near 100,000" `stage-1/literature.md:162,174` was written against, and 20 N gives 141,327. The single highest-risk value in the project is extrapolated further than any week 2 document admits.

**2. The same false Reynolds claim is what confirms D2, and it points the wrong way.**
`stage-1/design/01-configuration.md:42-45` says the single rotor "is the only one of the three whose per-rotor Reynolds number stays inside the band the thrust coefficient was measured in. Two rotors drop to 99,800 and three to 81,500 ... so the cluster rows are flattered even by their own numbers", and `decisions.md:256-258` (D18) repeats it. Per E1 and D12 the coefficient's own band is 35,000 to 100,000: 99,809 and 81,494 are inside it and 141,327 is not. The cluster rows are the ones sitting where the coefficient has support. This inverts the "every assumption set in the cluster's favour" argument at the exact point it is used to retire D2's provisional label, and D18's third paragraph quietly says the correct thing ("inside Kellen's band") while its second paragraph says the wrong one.

**3. E7 is labelled `measured` in a ledger whose headline sentence says nothing is.**
`stage-1/design/evidence-ledger.md:19` states "Nothing in this project is class measured"; `:33` classes E7, rotor tare at 10 percent of shaft power, as `measured`. By the ledger's own definition at `:12` ("somebody measured this quantity, **on this configuration**") a figure taken off Benedict's 4-blade NACA 0010 rotor is transferred, not measured. This is not decorative: tare sets shaft power (400.454 W), which sets rotor torque (1.6488 Nm), which sets the belt ratio and the motor's percent-of-continuous claim. `.claude/codemap.md:56` repeats the false headline as the file's Gotcha.

**4. The figure of merit and the solidity band are summary class in the ledger and are presented as measured everywhere they are used.**
E4 (`evidence-ledger.md:30`) classes FM 0.6 as `summary`, "abstract and companion Forum papers", and `:58-60` admits "the thesis is unread". `04-thrust-and-power.md:82` states "Kellen measured 0.6 at UAV scale on this shape family" with no caveat, and `stage-1/progress/week-2.md:45` scores it in the results table as "clears, and matches what Kellen measured". Same for E5 at `02-rotor-sizing.md:21` ("Kellen's measured optimum band"). FM 0.6 is the single value that turns the momentum floor into the 360.4 W working power, and through it picks the drive, the belt ratio, the electrical power and the motor mass line. A summary-only result is doing measured-grade work in the prose a reader sees.

**5. The named drive runs at 92 percent of a 180-second rating, on an unsourced efficiency.**
`evidence-ledger.md:37` records the MN3510 as "555 W and 25 A **maximum continuous at 180 s**", yet `04-thrust-and-power.md:123` concludes "Every one of those is a continuous figure and none is a peak or burst rating" and `handoff.md` repeats "Not a peak figure". A 180 s manufacturer rating is not an indefinite hover rating, no required endurance is stated anywhere, and no thermal or duty argument is given. Worse, the 513 W figure depends entirely on `efficiency.motor = 0.84`, which appears in no ledger row and in no `sources` entry: at 0.78 the motor input is 552 W and the design point is at the limit. Plan task 7 asked for the shortlist "with continuous power, speed, torque and mass evidence, not only assumed efficiencies" - the three efficiencies (0.93 / 0.84 / 0.95) are the only unevidenced links in the chain.

**6. "21.7 A of the 25 A allowed" is the torque current, not the input current the rating limits.**
`04-thrust-and-power.md:120-122` derives 21.7 A from Kt = 9.5493/700 against shaft torque, then compares it to a datasheet *input* current limit. The document's own 555 W = 25 A at 6S nominal (22.2 V) is arithmetically exact, so 513 W at the terminals is 23.1 A, i.e. 92 percent of 25 A, not 87 percent. The two headline percentages in the same paragraph (92 percent of power, 87 percent of torque/current) cannot both be true with a 0.84 efficiency. The sensitivity table at `numbers.json:545` says "22 A of the 25 A allowed" for the same row, a third value.

**7. The conservative mass column does not follow the rule the document states for it, and the deviation flatters the result.**
`02-rotor-sizing.md:122-124` says the column is "15 percent on catalogue parts whose mass is known, 20 to 25 percent on structure computed from assumed sections". The actual per-line ratios are: blades 1.150, main shaft and bearings 1.150, rotor frame and hubs 1.200, pitch mechanism 1.200, frame and mounting 1.250. Blades (97 g, built entirely from an assumed foam/skin/spar geometry) and the main shaft (a CFRP tube of assumed section) both carry the catalogue rate. Applying the stated rule at 20 percent to those two lines adds 8.8 g and moves conservative T/W from 2.389 to 2.360, in a week whose entire finding is a 32 g miss.

**8. The cluster comparison's decisive numbers have no derivation and no stated packaging assumption.**
`01-configuration.md:36-38` and `numbers.json:135-172` carry module masses of 815.2 g and 1018.5 g and largest dimensions of 420 mm and 520 mm for the two- and three-rotor layouts. Nothing in the diff shows how any of the four is obtained: the mass envelope exists only for the single rotor, and no spacing, gap or arrangement rule reproduces 420 or 520 from the per-rotor span (224.4 mm, 184.8 mm) or diameter (170 mm, 140 mm). Plan task 2 explicitly required "a stated selection rule **and packaging assumption**"; the selection rules section (`evidence-ledger.md:67-106`) states the boundary, the metrics, the radius rule and the cluster's favourable assumptions, and states no packaging assumption. `01-configuration.md:30-33` also claims "Each layout was then swept over radius and the best conservative thrust to weight kept" - that sweep is recorded nowhere. D2's re-test is not reproducible by a reader.

**9. The radius sweep omits mass, which plan task 6 requires, so the second candidate cannot be checked and its one checkable number is wrong.**
Plan task 6: "carry rpm, Reynolds number, ideal and actual aerodynamic power, rotor torque, electrical power, largest dimension **and mass**". Neither `02-rotor-sizing.md:78-84` nor `numbers.json` `power_by_radius` carries a mass column (Reynolds is in the JSON and stated as constant in prose; mass is absent from both). The 125 mm second candidate's conservative T/W of 2.297 (`:93`) therefore rests on a mass nobody can see. Its stated drive loading is also wrong: `:96` says "a motor running at 89 percent of continuous instead of 92", but 496.43 W at the ESC input is 471.6 W at the motor terminals, which is 85.0 percent of 555 W.

**10. Two rows of the published radius sweep already exceed the selected motor's continuous rating, and the text places the bound elsewhere.**
`02-rotor-sizing.md:89-91` says "Below about 95 mm the aerodynamic power route and the published power loading route stop agreeing within 35 percent, and the electrical power walks past the top of the drive shortlist." Applying the document's own efficiency chain to its own sweep: the 105 mm row puts 561.4 W at the motor terminals and the 95 mm row 620.5 W, against a 555 W rating - the drive bound bites at about 106 mm, not 95 mm, and two of the five published rows are already past it with no note. The 35 percent power-spread bound crosses at about 83.5 mm (at 95 mm the spread is 26.1 percent), not 95 mm. Both stated bounds on the radius trade are misplaced.

**11. The 5 percent flexibility allowance is described as derived from the section and is not.**
`numbers.json:506` (`sources.performance.blade_deflection_thrust_loss`), D20 and `02-rotor-sizing.md:41` all say the 5 percent is "sized against the computed blade section ... rather than assumed". The section gives a tip deflection of 0.086 mm and 0.054 degrees of twist, and `:67-69` then concedes "5 percent is generous against a section this stiff, and it is kept because the section is preliminary". No arithmetic anywhere connects 0.086 mm to a 5 percent thrust loss. `check.py` requires the low coefficient to "cover the stated blade deflection loss" and requires that source string to exist, so this is precisely the claim the mechanical gate cannot reach and the plan's "Done when" bullet asks the audit to check.

**12. Three mass lines are classified `fixed` when their own basis says they scale.**
`numbers.json:485-497`: "actuator controller and wiring" is `fixed` while its basis reads "17 g of silicone power and signal wiring **routed over the module envelope**", an envelope that runs 250.8 to 356.4 mm across the sweep; "fasteners and bonded joints" is `fixed` while its basis is joints "at the frame, bearing and blade attachment" whose count and bond area follow the frame; "vectoring actuator" is `fixed` while its basis is servos sized "against the residual pitch link load", which moves with thrust across a sensitivity table that is frozen from 13 to 24 N. Separately, "main shaft and bearings" is a single line mixing a span-scaled CFRP tube with a torque-scaled drive-end allowance and is forced into one class. This matters because the 72 g "genuinely fixed" total at `02-rotor-sizing.md:121` and the radius-trade argument at `:91-92` both depend on which lines are held constant.

**13. The progress file overclaims what the week produced, on three counts.**
`stage-1/progress/week-2.md:13-15` lists seven work packages including "the audit"; `:19` then says "Everything except the freeze". `stage-1/audit/week-2.md` does not exist in the diff, and `stage-1/plan.md:93-97` names it as one of four artifacts every week ends with "without exception". `:30` claims "26 performance scalars"; `numbers.json` has 24. `:66-78` describes four fallback sweeps (12 to 26 N, 70 to 150 mm, chord ratio 0.63 to 0.836, aspect ratio 3 to 6) whose results (peak 2.389, 2.481 at AR 6) are the justification for reporting BLOCKED, and none of the four leaves any artifact: `numbers.json` carries five radii from 95 to 135 mm and four thrusts from 13 to 24 N, and nothing else.

**14. Week 2 added no tests, and the seven list artifacts it filled are gated only on shape.**
No file under `tools/` is in the diff, which the progress file states honestly at `:172`. The consequence is that every substantive new claim is prose only. `check.py` `ROW_SPECS` checks `drive_candidates` for two rows with four non-empty fields and never checks that the selected drive's continuous power covers the design point, that `continuous_torque_Nm` equals 9.5493/KV times the continuous current, or that exactly one row is selected. `configuration_candidates` never checks that the selected row's `module_mass_g` matches `results.mass_envelope_g`, or that it wins on the stated first metric. `aero_azimuthal_loads` checks 24 rows of two numbers and never checks the cycle mean equals thrust per blade, the peak-to-mean, symmetry or periodicity - a 36-row table of arbitrary positive numbers passes identically. The four gates the plan added at `:281-286` do bite, but nothing added this week would fail if the drive, the candidate ranking or the load distribution were subtly wrong.

**15. Codemap entries that do not match the files they describe.**
`.claude/codemap.md:56` gives the evidence ledger the Gotcha "nothing in this project is class measured", contradicted by E7 in that same file (finding 3). `:44-46` says week 2 "filled all of these" including `sources` and `results`, but `results.total_mass_g`, `results.weight_N`, `results.thrust_to_weight` and all three `sources.structure` fields are null. `:19` says "Progress, audit, decisions and journal are the four artifacts every week ends with", which drops `handoff.md` and merges decisions with journal; `stage-1/plan.md:90-102` lists progress, audit, handoff, and decisions-plus-journal. Every changed source file does have an entry, and the `tools/test_gates.py` "77 checks" figure matches the run.

**16. Two ledger cells and one journal claim are not reproducible from what is written.**
E1 reproduces cleanly (1.98 N over 0.5 rho 15.96^2 0.020962 = 0.6055) and E3 is 0.6055 x 0.85 = 0.5147, so the two values that matter are fine. E2 is not: `evidence-ledger.md:28` gives 3 blades, c/R 0.333, "same radius, same 2000 rpm" but omits the span, and the span is 152.4 mm rather than E1's 158.8 mm - using the row as written gives 0.78, not 0.8114 (only `numbers.json:184` carries the missing span). E2's source Reynolds is also given as "about 35,000"; at a 25.4 mm chord and 15.96 m/s it is about 27,000. And `stage-1/journal.md:43` argues the model is not being harsh on the strength of "Our rotor group is 24 percent heavier than Runco's scaled geometrically" - no scaling of Runco's 8.2 g at R 33 mm to R 115 mm reproduces that figure by any exponent, and under geometric similarity the comparison runs the other way.

**17. Cross-week: `literature.md` was left contradicting what week 2 delivered, with no superseding entry.**
`stage-1/literature.md:162,174,200,236` still carries 0.607 and 0.516 (now 0.6055 and 0.5147), still says the family is applied at "Re near 100,000" (now 141,327, finding 1), and still says "Week 2 bounds it with a low value **derived from the spread in S2's own parametric results**" - week 2 instead built 0.5147 from a 5 plus 10 percent haircut. Week 1 marked literature.md as the verified parameter table; `handoff.md` dropped the line that said so rather than reconciling it, and `decisions.md` records no entry superseding the literature statement. The 0.25 percent value drift is harmless; the method and Reynolds statements are not.

**18. Minor: `handoff.md` no longer tells a fresh session how to start a week.**
The diff removes the "To start the next week" section pointing at `_run-prompts.md` and the open item naming `_codex-prompt.md` as the active prompt, while `:3` still claims "This file is where a fresh session starts". Both referenced files still exist and are unreachable from the handoff. Nothing mechanical breaks (`check.py` only greps `NEXT-WEEK`, which is correctly a single line still reading 2, matching a progress file deliberately without `STATUS: WEEK-COMPLETE`).

Cannot certify: approach correctness, statistical validity of results, anything requiring the blocked or external resources.
Findings: 18

---

## What was done

Fifteen findings were fixed. Three are carried as debts. The fixes moved the headline number
**down**, not up: conservative thrust to weight went from 2.389 to **2.252**, and the shortfall
against the hard limit grew from 32 g to 69 g. The design point moved with them, from 20 N at
115 mm to 18 N at 110 mm, because finding 5 forced the drive ratings to be derated and findings
7 and 12 corrected the mass column.

One fix made the week more useful rather than less. Chasing finding 10, which said the stated
radius bounds were in the wrong place, showed that the bound is the drive and that conservative
thrust to weight keeps improving as the rotor shrinks. The design is drive limited. That was not
visible before the audit and it is now the cheapest route to closing.

| Finding | Action |
| --- | --- |
| 1 | Fixed. The Reynolds extrapolation is stated in the ledger, both design documents and the progress file, and recorded as D25. The conservative-thrust gate forces design thrust above 11.76 N, which forces Re above 108,000, so no compliant point in this family sits inside the documented band |
| 2 | Fixed. The inverted claim is gone from `01-configuration.md` and the corrected version is in D27. The cluster rows sit nearer the coefficient's own Reynolds band, which is now stated as a point in the cluster's favour |
| 3 | Fixed. E7 reclassed transferred. Ledger headline and codemap Gotcha corrected |
| 4 | Fixed. Every use of the figure of merit and the solidity band now says reported, and both are named as summary class doing load-bearing work |
| 5 | Fixed, and it cost more than anything else. The datasheet says "Max. Power (180s)", so week 2 now derates by 0.80 for continuous duty and checks power, torque and attainable motor speed together. The efficiency chain is in the ledger as E16 with its sensitivity. The missing endurance requirement is debt 3 |
| 6 | Fixed. Input current and torque current are separated, and the sensitivity table strings carry the input current at 6S |
| 7 | Fixed. The stated rule is applied: blades and the rotor shaft move to the 20 percent structural rate |
| 8 | Fixed. The packaging assumption is in the selection rules, the cluster mass build-up is written out line by line, and every candidate row's largest dimension reproduces from that one rule |
| 9 | Fixed. `power_by_radius` carries both mass columns, conservative T/W, motor input power, the belt ratio and whether a drive fits, on every row |
| 10 | Fixed, and it turned into the week's main new result. The drive is what bounds the radius, the power-route agreement is nowhere near binding, and rows past the rating are flagged rather than quietly included |
| 11 | Fixed. The stiffness check bounds the loss from above instead of deriving it, and the text says the section supports well under 1 percent while the 5 percent is kept as a floor |
| 12 | Fixed. The envelope is resorted into 13 lines. Wiring and fasteners are geometry, the actuator is power, and the shaft is split into an assumed-section tube and catalogue bearings. Genuinely fixed mass is now 8 g, which weakens the amortisation argument D11 and D13 rest on, and that is stated in three places |
| 13 | Fixed. Scalar count corrected to 24, the audit is no longer claimed before it existed, and all four fallback sweeps are written out as tables |
| 14 | Fixed. Four gates added to `check.py` with 12 matching self-tests: the azimuthal table has to average to the recomputed thrust, exactly one drive is selected and its continuous rating has to cover the recomputed motor input, continuous torque has to reproduce from KV and current, and exactly one configuration candidate is selected and has to be the one that wins on conservative thrust to weight. The suite went from 77 to 89 |
| 15 | Fixed. All three codemap errors corrected, plus entries added for the audit file and literature.md |
| 16 | Fixed. E2 carries its span and its own Reynolds number of 27,000, and the unreproducible journal claim is removed |
| 17 | Fixed. Dated supersession notes at the two places in `literature.md` that week 2 overtook, plus D26 |
| 18 | Fixed. The pointer to `_run-prompts.md` is back in the handoff |

Debts opened by this audit, carried in `stage-1/progress/week-2.md`: the 180 s rating against an
unstated endurance requirement, the three efficiencies which remain assumed, and the cluster
mass build-up which is written out in prose but stored in `numbers.json` only as totals.

AUDIT-COMPLETE
