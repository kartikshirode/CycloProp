AUDIT-COMPLETE

# Final Stage 1 audit

Audit date: 23 September 2026

This supersedes the audit dated 4 September 2026 that previously occupied this file. The response
to that older audit remains at `stage-1/audit/codex-final-response.md`, but it is not the current
verdict.

## Verdict

I would not send the package as it stands, and I would not expect this version to land in the top
15. The engineering package is much better than the usual paper concept. The four-bar closes, the
power chain has more than one route, the structure has real load paths and the risks are stated.
The problem is the last mile. A required team section is still a form, the staged email contains
old results and a placeholder, and the attachment contradicts its own current data in several
places that sit directly under the high-weight criteria.

My score on the published final-evaluation weights is 60 out of 100. That is not a score for the
underlying effort. It is the score I think an evaluator can defend from the PDF in front of them.

The current read-only checks give this result:

```
python -B tools/check.py --all      -> exit 0
python -B tools/check.py --week 5   -> exit 1, TECHNICAL-READ-COMPLETE only
```

I did not run `tools/test_gates.py`. It creates throwaway trees, and this audit was required not to
run commands that write. The existing 212-test result is recorded in `_codex-context.md:98-100`.

## Findings to fix before 26 September

### F1. Blocker: required item 7 is still a template, despite the roster marker saying confirmed

Where: `stage-1/submission/cycloprop-stage1.md:674-721`,
`stage-1/design/07-team-and-execution.md:18-34`, `:42-50`, `:68-76`, `:92-109`, `:116-128`,
`stage-1/human-gate.md:62-66`.

The PDF says the section is deliberately incomplete. It has no member names, roles, programmes,
prior work, tool access, facility access or real Stage 2 owners. Every owner in the detailed plan
is `[P-1]`, and the submission still contains `[P-9]`. At the same time,
`stage-1/human-gate.md:64` says `ROSTER-CONFIRMED`. Those two states do not agree.

This matters because team capability and execution is one of the seven required Stage 1 items,
not an appendix. The competition says Stage 1 identifies teams for detailed design support. A
good technical report with no evidence that the named team can execute it gives an evaluator a
simple reason to rank another team ahead.

Reproduce: run `rg -n '\[P-[0-9]\]|still needs|unstated|Owner' stage-1/design/07-team-and-execution.md stage-1/submission/cycloprop-stage1.md`, then compare the hits with
`stage-1/human-gate.md:62-66`.

Fix: a person supplies the real facts. Put each member's role and programme in the report, attach
prior work only where it is true, name tool and test access, and replace each Stage 2 owner token
with a real owner. If capability is missing, say who will obtain it and by when. Do not mark this
done by deleting the tags.

### F2. Blocker: the staged email is not the email for the current attachment

Where: `stage-1/submission/email-draft.md:8-9`, `:27`, `:35-40`, `:49`, `:59-60`.

The email still contains `[SENDER NAME]`. It also quotes thrust-to-weight as 2.5563 nominal and
2.1569 stacked. The current attachment and data say 2.5191 and 2.1221 at
`stage-1/submission/cycloprop-stage1.md:34-39` and
`stage-1/design/numbers.json:1304-1309`. The regulator added under D70 caused that change.

This is a late-send failure, not a cosmetic mismatch. It puts different headline results in the
message and its attachment. The page-limit question is also being asked in the submission email
on 26 September, one day before the deadline. If the answer requires a new format, there is almost
no recovery time.

Reproduce: compare `email-draft.md:27-40` with `numbers.json:1304-1309`. Search the submission
folder with `rg -n 'SENDER NAME|2\.5563|2\.1569' stage-1/submission`.

Fix: ask the format question now. Then a person fills the sender name and checks the registered
address. Replace both T/W values from the current source, rebuild the PDF if any report text
changes and read the email beside the final attachment before sending.

### F3. High: the criteria map makes a false compliance claim

Where: `stage-1/submission/cycloprop-stage1.md:489-503`, `:517`, `:723-736`, `:743-756`.

The T/W results table says one case clears 2.5 and three do not. The criteria map says a 33-line
budget has four cases, all clearing the limit. Both parts are wrong. The current budget has 34
lines and the stacked case is 2.1221. The claims table repeats 33 lines. The structural criterion
also points the evaluator to the materials section even though the report has a separate
`# Structural design and margins` section at line 519.

This is the most damaging prose error in the PDF. It is placed in the evaluator's map and directly
contradicts the main result. It can look like the downside table was disclosed while the scorecard
was written to claim a pass anyway.

Reproduce: read `cycloprop-stage1.md:489-503`, then `:727-735`. Count the component rows at
`:431-466`, or read the gate output that reports 34 mass lines.

Fix: say "34-line budget; the nominal case clears and all three downside cases miss." Point the
structural row at `Structural design and margins`. Check every criteria-map sentence against the
section it names.

### F4. High: the attachment still contains pre-correction kinematic, aerodynamic and power values

Where: `stage-1/submission/cycloprop-stage1.md:232-236`, `:278-280`, `:292-296`, `:362`,
`:414-422`, `:586`, `:819-821`, `:951-956`, `:1019`; current values at
`stage-1/design/numbers.json:27`, `:35`, `:581`, `:591-592`, `:869` and
`stage-1/design/03-pitch-and-vectoring.md:163-170`, `:245-269`.

The live contradictions are:

- Transmission angle is written as 58.58 to 135.68 degrees, while the figure caption and data say
  53.88 to 135.68. The same paragraph says 135.68 is outside a 40 to 140 band. It is inside.
- Side-force decomposition says 11.00 degrees from the linkage and 0.978 from aerodynamics, even
  though the current design says 7.75 and 1.33. The old pair does not sum to the stated 9.078.
- Module power is 516.6 W in two paragraphs and 518.0 W in the power table, claims table and data.
- Appendix B declares `performance.blade_load_peak_to_mean = 2.501`; the current value is 2.5458.
- Appendix B declares `structure.pitch_link_margin = 3.3015`; the current value is 3.2878.
- Appendix A calls one 8.5 g board the only fixed mass, after the report correctly added the fixed
  10.0 g regulator at line 482.

These are not rounding differences. They cross the kinematics, aerodynamic, structural,
integration and presentation criteria. A reviewer who checks one caption against the paragraph
will stop trusting the rest of the number trail.

Reproduce: compare the cited source lines with the cited JSON keys. A direct key-by-key read of
Appendix B finds the two declaration mismatches at lines 956 and 1019. Search the source with
`rg -n '516\.6|58\.58|11\.00|0\.978|2\.501|3\.3015|only fixed' stage-1/submission/cycloprop-stage1.md`.

Fix: regenerate these sentences from the current design records or correct them in one controlled
pass. Then compare every Appendix B declaration with its exact JSON key, rebuild the PDF and read
the kinematics, power, mass, structure and viva sections side by side. The green gate does not
catch this set, so the readback matters.

### F5. High: the project did not meet its own thrust-to-weight margin contract

Where: `stage-1/plan.md:288-319`, `:437-451`, `stage-1/decisions.md:1825-1843`,
`stage-1/design/05-mass-and-tw.md:130-160`.

The week 2 plan first required the conservative case to clear 2.5. D30 moved the stacked test to
week 4 and still required the design point and each downside alone to clear 2.5. The final design
does not meet that rule: 2.5191 nominal, 2.3931 coefficient downside, 2.2339 mass downside and
2.1221 stacked. D67 changed the downside gate to 2.0 after the corrected design failed the earlier
contract.

The decision log discloses the change, so this is not hidden. It is still a delivery miss against
the plan. Calling weeks 2 and 4 complete now means complete under a weaker post-review rule, not
under the margin rule the plan used to freeze geometry.

Reproduce: compare the rule at `plan.md:314-319` with the current four-case table at
`05-mass-and-tw.md:135-152`. The two individual downside cases and the stacked case are all below
2.5.

Fix: do not claim the original margin plan was delivered. In the submission, frame the result as
a preliminary nominal pass with an open compliance risk. Actual closure needs a lower verified
mass, a measured thrust result or a new design point. Moving the reporting floor again is not a
fix.

### F6. High, disclosed risk: the nominal T/W pass is too thin for the evidence behind its mass

Where: `stage-1/design/05-mass-and-tw.md:6-10`, `:15-55`, `:135-152`,
`stage-1/audit/phase-6-reaudit.md:67-101`.

Nominal compliance is 2.5191, only 0.8 percent above the requirement. The mass downside alone is
2.2339. The earlier independent audit found 29 non-blade lines governed mainly by basis text,
growth rules and agreement with another list. D70 then added the regulator as a 34th line, also an
allowance rather than CAD mass or a weighed part.

The arithmetic is consistent. The issue is whether the first estimate is accurate inside 0.8
percent. Nothing in the repository supports that level of mass accuracy. Publishing the 117.26 g
stacked gap is the right call because hiding it would be worse. The invented 2.0 downside floor is
not useful to an evaluator and should not be used as reassurance.

Reproduce: `17 / (0.68791 * 9.81) = 2.5191`. Replace nominal mass with 0.77574 kg and nominal
thrust with 16.1493 N to reproduce 2.1221. Read the mass-evidence attack at
`phase-6-reaudit.md:73-101`.

Fix before send: change the framing, not the numbers. Keep the detailed budget and the gap. Say
that compliance is unverified until CAD mass properties, selected hardware and measured thrust
replace the estimates.

Suggested replacement paragraph:

> At the current design point the module estimate is 687.91 g and thrust to weight is 2.5191,
> which is a preliminary pass with 0.8 percent margin. Applying either the 5 percent coefficient
> downside or the conservative mass budget drops the result below 2.5. With both applied it is
> 2.1221, and the conservative mass would need to fall by 117.26 g to recover the requirement at
> the low thrust case. Stage 2 therefore treats 658.48 g as a gate, then replaces the estimate
> with CAD mass properties, weighed parts and a thrust test.

### F7. Medium: the evaluator cannot reconstruct the literature trail from the attachment

Where: `stage-1/submission/cycloprop-stage1.md:758-795`.

The source section mostly gives author surnames and years. Several entries have no paper title,
journal, volume, pages, DOI or stable URL. The exact page and figure references live in the
internal evidence ledger, not in the submitted report. Claims such as the 0.6648 coefficient, the
0.6 figure of merit, the 3 to 4 peak-load range and the 10 to 35 degree side-force range cannot be
checked from the attachment alone.

This matters most for aerodynamics, already the weakest 15 percent criterion. It also weakens the
originality and third-party evidence trail required by `context.md:150-158`.

Reproduce: inspect the eight bullets at `cycloprop-stage1.md:772-790`; try to identify each work
without opening the repository's evidence ledger.

Fix: add a normal reference list with author, full title, venue or institution, year and DOI or
stable URL. Put page or figure locators beside each borrowed numerical claim. This can be compact.

### F8. Low, internal: the audit context is stale after D70

Where: `_codex-context.md:103-106`, `:125-136`, `:233-239`.

The file calls 677.91 g, 763.24 g, 2.5563, 2.1569 and 104.76 g current. It also says the controller
regulator is still an open engineering hole. D70 added the regulator and moved all five numbers.
The submission is newer than the context that tells a fresh reviewer what the submission contains.

Reproduce: compare those lines with `stage-1/decisions.md:1994-2012` and
`numbers.json:1304-1315`.

Fix later: update the context after the submission fixes. This does not affect the evaluator, but
it already caused the old and current design states to be mixed in review.

## The seven required Stage 1 items

| Item | What is in the attachment | Judgment |
| --- | --- | --- |
| 1. Concept and configuration | Single rotor choice, cluster comparison, boundary and envelope | Delivered. The comparison is clear enough for Stage 1. |
| 2. Preliminary rotor sizing | Radius, chord, span, Reynolds, solidity, coefficient cases and drive-limited radius | Delivered. Coefficient evidence remains preliminary. |
| 3. Blade arrangement and pitch control | Four-bar closure, pitch schedule, actuator sizing and vector map | Delivered strongly, but the live prose has stale kinematic values. |
| 4. Estimated thrust and power | 17 N estimate, momentum floor, figure-of-merit route, second power route and drive chain | Delivered. It is analytical, not a simulation or test. |
| 5. Module weight and T/W | 34-line budget and four cases | Delivered as an estimate. Only the nominal case complies. |
| 6. Material and manufacturing approach | Materials, processes, tolerances, assembly, inspection and cost | Delivered. Prices are not quotes and several critical parts lack supplier qualification. |
| 7. Team capability and execution plan | Schedule skeleton, dependencies and gates | Not delivered as real team content. Owners, roles, tools and facilities are placeholders. |

## Delivery against the plan

| Plan block | What landed | What did not |
| --- | --- | --- |
| Week 1 | Official requirements, literature record and source recovery | No material gap for Stage 1. |
| Week H | Registration and eligibility are marked; roster and sender markers were later changed to confirmed | Team facts are absent from the report and the technical read is pending. The marker and deliverable disagree. |
| Week 2 | Configuration screen, sizing, thrust, power, evidence ledger and sensitivity work | The final post-D67 design no longer meets the downside T/W freeze rule the week originally used. |
| Week 3 | Solved linkage, schedule, vector map, packaging and draft PDF | Item 7 remained a skeleton. Current submission prose carries old week 3 values. |
| Week 4 | Structure, mass budget, materials, manufacturing and BOM | The original stacked 2.5 gate was replaced with 2.0. Mass is not closed from CAD or weighing. |
| Week 5 | Submission, criteria map, claims table, viva appendix, seven figures, PDF and email draft | No `stage-1/progress/week-5.md`, item 7 is incomplete, the email is stale and the technical read is pending. Week 5 is not complete. |

The project also produced work the plan did not ask for at this depth: seven data-linked figures,
a six-phase review, 212 gate self-tests, an explicit controller regulator interface, bearing
oscillation analysis and a large hostile-viva appendix. Those are useful. They do not replace the
missing team facts or the failed internal T/W margin.

## Engineering assumptions the gates cannot settle

| Assumption | Viva position | What would make it defensible |
| --- | --- | --- |
| Blade-area coefficient 0.6055 | Reasonable as a preliminary lower design value because Kellen measured 0.6648 on a close shape family. It is still not a measurement at this operating point, inflow or build. | Readable source plots tied to the exact operating point, transient CFD and a load-cell run. |
| Figure of merit 0.5215 | Self-consistent bookkeeping from Kellen's 0.6 and the reduced coefficient. It assumes the power coefficient transfers. | A sensitivity band on power coefficient, then measured thrust and shaft power. |
| Momentum area 2R times span | Defensible as an ideal lower bound only. It is not proof of the real streamtube area or rotor power. | Validated flow modelling or wake measurements. |
| Peak-to-mean load factor 4.0 | A conservative screen from the top of a summary-only 3 to 4 range. Fine for paper sizing, weak as source evidence. | Read Heimerl, run unsteady CFD or measure blade loads. |
| Foam and skin allowables | Useful class-value screen with a good sensitivity study. Hand layup, batch properties, defects and bonds are not represented. | Wrinkling, laminate and bond coupons made with the planned process. |
| Pitch bearings | ISO 76 gives a static screen. The report correctly identifies false brinelling, but has no oscillating-life basis. | Manufacturer oscillating guidance or a duty test with the selected grease. |
| Belt and pulleys | Ratio and shaft side load are calculated. Tooth capacity, wrap, pretension, temperature and life are not. | Select a belt by a manufacturer's power or tooth-load chart, then run it at load. |

## The mass case

Publishing the 117.26 g stacked gap is the right decision. It will cost points in both thrust and
T/W, but hiding it would turn a weak estimate into a credibility problem. I would remove the
language about clearing a self-declared floor of 2.0. That floor is not in the competition brief
and looks like the target moved after the design failed. Use the replacement paragraph under F6.

## What can fail on 26 September

- The email contains a sender placeholder and old results.
- The PDF still says member roles and programmes need confirmation while the gate says the roster
  is confirmed.
- The criteria map says all four T/W cases pass. Three fail.
- The PDF is 30 pages. No published limit exists, but asking in the submission email leaves one
  day to react.
- Figures are numbered 1 through 7 in the built PDF. Tables are not numbered. This is a minor
  navigation issue, not a blocker.
- The built PDF matches the current Markdown source, including the current mistakes. Rebuilding
  without fixing the source will not help.
- The source list is not complete enough for an evaluator to follow the main aerodynamic claims.

## The hostile viva question

> At chord-to-radius 0.66 and an inflow ratio of 0.387, what measured or unsteady result shows
> that this rotor will still achieve a blade-area coefficient of 0.6055 after wake return, dynamic
> stall hysteresis and the built blade's flexibility are included?

The repository has no direct answer. It has a good argument from Kellen's close shape family and
a deliberately lower coefficient, but it has no matched unsteady analysis and no test. The silence
is serious because thrust, drive power and the 0.8 percent nominal T/W pass all depend on that
coefficient. For Stage 1, the honest answer is that it is the first aerodynamic gate in Stage 2.

## Criterion score

| Criterion | Score | Reason |
| --- | ---: | --- |
| Feasibility of 10 N thrust | 11 / 15 | Both coefficient cases clear 10 N by a wide amount, with a useful shape-family measurement. No matched CFD or test. |
| Feasibility of T/W above 2.5 | 6 / 15 | Nominal clears by 0.8 percent. All three downside cases miss, and most mass lines lack CAD or weighed closure. |
| Kinematics and thrust vectoring | 12 / 15 | Strong closed-form mechanism, schedule, actuator sizing and command map. The attachment has stale values and no friction or multibody result. |
| Aerodynamic analysis quality | 7 / 15 | Momentum, figure of merit, a second power route and an azimuthal model are useful. The model is calibrated to the coefficient and misses key unsteady physics. |
| Structural assessment | 9 / 15 | Good centrifugal, shaft, blade and linkage screens. Bond, fatigue, modes, belt life and local stress remain open. |
| Manufacturability, materials and cost | 7 / 10 | Strong process detail and BOM. Prices are indicative, the regulator is an allowance and critical supplier data is missing. |
| CAD, integration and packaging | 3 / 5 | Good envelope, interface and mounting work for Stage 1. No CAD, and the interface prose has a stale power value. |
| Presentation, viva and clarity | 5 / 10 | Good figures and candid risk writing. False criteria-map text, placeholders, stale numbers and incomplete references cut this sharply. |
| **Total** | **60 / 100** | **Technically serious, not top-15 ready in its current submitted form.** |

## Send decision

No, not as it stands.

The shortest route to yes is:

1. A person completes item 7 and the sender fields with real names, roles, programmes, capability,
   tool access, facilities and owners.
2. Correct the false criteria-map row and every stale value listed in F4. Check Appendix B key by
   key against `numbers.json`.
3. Update the email from the final report and resolve the page-limit question before send day.
4. Add a usable reference list and keep the mass paragraph honest about the nominal-only pass.
5. Rebuild the PDF. A person reads the PDF and email end to end, then and only then writes
   `TECHNICAL-READ-COMPLETE`.
6. Run the three existing verification commands after those edits. The expected week 5 human-gate
   failure should be gone, and no other failure should replace it.
