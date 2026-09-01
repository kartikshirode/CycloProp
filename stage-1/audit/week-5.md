# Week 5 preparation audit

One fresh-context read-only pass, run after the seven preparation commits landed, on the diff
from `307e9b7` to `a907712`. This audits a preparation pass rather than a finished week: week 5
is still blocked on the human gate and no progress file exists, which the auditor picks up as
finding 3. The findings are reproduced verbatim below and what was done about each follows them.
17 findings: 13 fixed, 4 reported rather than changed.

## The audit, verbatim

Audit of the week 5 preparation pass (base `307e9b7`..`a907712`, working tree clean, no uncommitted changes).

Verified as accurate before listing defects: `check.py --week 5` exits 1 on the human gate alone as the handoff claims; 128 self-tests pass; the PDF is 21 pages with Appendix A starting on page 17 (so 1 + 15 + 5 as claimed) and its text matches the current source; 12 examiner questions cover all 10 topics the plan names; the criteria map is 8 rows summing to 100%; the claims table leads with coefficient, mass, deflection, vector map as the plan requires; the 33 budget lines sum to 607.97 g and 684.70 g exactly; the 52 percent BOM share, 37-row schedule, 36-point azimuthal model, 8 margins, 1.1 percent shape-family match and 12.5 g stacked clearance all reproduce from `numbers.json`; and no name, institution or tool licence appears in `07-team-and-execution.md`.

1. **The submission contradicts its own mass table on the controller, using a figure `numbers.json` records as superseded.** `stage-1/submission/cycloprop-stage1.md:357` ("What is genuinely fixed in this module is one 8.0 g controller board"), repeated at :631 and :633, against its own table row at :338 (`pitch offset controller | 8.5 g`). `numbers.json` `mass_budget_g` states the basis explicitly: "8.5 g against the 8.0 g week 2 carried, which is the debt week 3 left open", and `05-mass-and-tw.md:93` shows the same 8.00 to 8.50 refinement. The coverage gate cannot catch it because 8.0 g still traces to the retired `mass_envelope_g` line. The error is baked into the committed PDF (both strings extract from it).

2. **The human-gate check can never detect a missing `TECHNICAL-READ-COMPLETE`, which is the marker that gates final staging.** `tools/check.py:1839` uses `m not in text` over the whole file, and `stage-1/human-gate.md` contains the literal string in prose ("Replace `TECHNICAL-READ-PENDING` below with `TECHNICAL-READ-COMPLETE` only after..."). The gate output confirms it: only four markers are reported outstanding out of the five in `HUMAN_GATE_MARKERS`. The week fixed one reader defect in the same file (`front_matter_lines`) and left this one; the handoff discloses it ("the gate does not see it as outstanding") but nothing was done, so the last gate before the submission goes out is permanently green.

3. **Week 5 scope work was delivered while a blocked trigger the config says must not be worked around was active.** `.claude/weekly-loop.md:79` says "Stop the week and report BLOCKED, with unblock steps, on any of these. Do not work around them," and :86 lists the missing human gate markers; `stage-1/plan.md:213` says "if it is not done by 23 September, week 5 stops and reports BLOCKED" and :503 says week 5 "cannot write a real capability section or stage a submission without them". The diff delivers plan tasks 1 through 8 minus the human parts: item 7 written, submission assembled, PDF built, email drafted and staged. It is disclosed loudly (D58, sentinel note, handoff), and no progress file or `NEXT-WEEK` bump was written, but the delivered work is the blocked week's work.

4. **`01-configuration.md`'s cluster rpm column disagrees with `numbers.json` and with the submission built from it, and nothing records the correction.** `stage-1/design/01-configuration.md:44-45` gives 3141 and 3891 rpm; `numbers.json` `configuration_candidates` gives 3214.9 and 3976.3; `stage-1/submission/cycloprop-stage1.md:68-69` gives 3215 and 3976. The stored values are the physically correct ones (9.0 N on 0.033454 m2 of blade at coefficient 0.6055 fixes the tip speed, giving 3214.7 rpm at R = 0.08 m). Week 5 assembled the table from the design document, silently emitted different numbers, and left the design document wrong with no decision entry. `git log -S` shows both figures have been in place since week 2, so no gate has ever read that column.

5. **The coverage gate is blind to angles written as "degrees", so 30 numeric angle claims in the submission are unaudited while the report tells the evaluator otherwise.** `tools/check.py:502` matches `deg` only when not followed by a word character, and the submission uses "degrees" 30 times and "deg" zero times. Independently, `collect_dimensioned` loads 86 angle values including every multiple of 10 from 0 to 360 (from `pitch_schedule.azimuth_deg`), and `DISPLAY_TOL` is 0.02, so any round angle would trace by coincidence even if the pattern matched. `cycloprop-stage1.md:715` states "every number in the narrative carrying a physical unit has to match a computed value in the same dimension", and `.claude/weekly-loop.md:106` makes the same claim. This is the same "passing by coincidence" failure the journal correctly rejected for group mass totals.

6. **The submission's single allow comment exempts nothing, while three documents claim it hides three of the four permitted numbers.** `cycloprop-stage1.md:220` carries the comment, but the numbers it justifies ("Sirohi measured about 10 degrees, Adams 15 to 35") are on :219, and `allow_reason` is evaluated per line. Instrumenting `check_numeric_coverage` over the real file returns `unchecked = []`, i.e. zero exempted numbers. D56 ("it hides 3 of the 4 numbers the ceiling permits"), the same sentence in `.claude/codemap.md` under the submission entry, and the journal's "One allow comment survives" paragraph are all wrong about the count.

7. **D54 claims test coverage for a safety property that has no test, and the tests that exist would not catch an off-by-one.** D54 says "three coverage probes covering the three cases above" where the cases include "An unterminated opening delimiter counts as no front matter"; grepping `tools/test_gates.py` for `front_matter` returns only the three probes at :1833-1838 plus the week-5 case at :1592, and none of them feeds a document whose leading `---` is unterminated. Separately, all four new tests place a blank line between the closing delimiter and the first body line, so `front_matter_lines` returning `i + 1` would still pass every one of them.

8. **The submission's item 7 describes a table it does not contain.** `cycloprop-stage1.md:516` says "All 11 Stage 2 items are scheduled, with the tool category each one needs, what it waits on and the gate that closes it", and the table that follows at :519-529 has three columns (Weeks, Stage 2 items, Closed when) with no tool category and no dependency column. The design document `07-team-and-execution.md` does carry both plus an owner column, so the claim was carried across from a table that was cut.

9. **The criteria map calls the design's thrust coefficient measured when the report classes it derived everywhere else.** `cycloprop-stage1.md:546` answers the 15% thrust criterion with "thrust from geometry and a coefficient measured on this shape family"; the design runs on 0.6055, whose `sources` entry in `numbers.json` ends "Derived, never measured on this configuration", and the report's own Appendix at :592 and examiner answer 1 both say the nominal is transferred. The measured 0.6648 is Kellen's and is deliberately not used.

10. **The built PDF's section numbers do not match the "Item n" cross-references used throughout the report.** `--number-sections` (the command in `.claude/codemap.md`) numbers `Submission identity` as 1 and `Summary` as 2, so required item 5 prints as "7 Estimated module weight and thrust-to-weight ratio" (PDF page 8) and Appendix A as "13". The criteria map (:546-553), the claims table and examiner answer 3 all cite "Item 4", "Item 5", "Item 6", which an evaluator reading the attachment cannot resolve.

11. **D55 claims the placeholder scheme makes it impossible to miss a tag by reading only the report; five of the nine are absent from it.** `stage-1/decisions.md`, D55: "one list drives all three and a person filling them in cannot miss one by reading only the report". The submission contains only `[P-1]`, `[P-2]`, `[P-7]` and `[P-9]`; `[P-3]`, `[P-4]`, `[P-5]`, `[P-6]` and `[P-8]` appear nowhere in it.

12. **The one required item written this week is the only design document with no substance or number gate.** `tools/check.py:1736` calls `require_headings` on `07-team-and-execution.md` and nothing else, where every other design document gets `require_headings` plus `require_substance` and, where applicable, `check_declared_numbers` (:1230-1231, :1390-1392, :1431-1433, :1714-1715). The file ends with a `## Numbers used` block in the repo's standard verified format that no gate reads, and a three-heading stub would pass week 5. Its four declared values do reproduce from `numbers.json`, so this is an unenforced promise rather than a wrong number.

13. **The file the human is directed to never names the four strings they have to type.** `stage-1/human-gate.md` says "Add each marker below on its own line as it is confirmed" and then lists only `REGISTRATION-PENDING`, `ELIGIBILITY-PENDING`, `ROSTER-PENDING`, `SENDER-PENDING`, `TECHNICAL-READ-PENDING`, while `check.py:1805` requires `REGISTRATION-CONFIRMED`, `ELIGIBILITY-CHECKED`, `ROSTER-CONFIRMED`, `SENDER-CONFIRMED`. Everything left of week 5 depends on those four exact strings, the week 5 pass rewrote the handoff around them, and it did not touch the file that needs them.

14. **The handoff now states a weaker block than the config it is supposed to match.** New handoff text: "The fifth, `TECHNICAL-READ-COMPLETE` ... blocks final staging rather than the start"; `.claude/weekly-loop.md:86` lists that marker inside the blocked trigger "The human gate markers are missing when week 5 starts, including `TECHNICAL-READ-COMPLETE`". `human-gate.md` supports the handoff's reading, so the config and the gate file disagree and the handoff silently picked the permissive one, replacing the previous handoff's "All 5 markers ... hard blocks week 5".

15. **Two documents disagree on how many overfull lines the PDF build produced.** The handoff says "the log is clean of overfull lines after two were fixed" and `.claude/codemap.md` says "the two that were fixed"; `stage-1/journal.md` says "First one had five overfull lines". No xelatex log is committed, so neither count is checkable from the diff.

16. **The handoff points a reader at a file that does not exist at HEAD.** New handoff item 6 links `stage-1/audit/week-5.md` as something that "audits the preparation pass the same way"; `stage-1/audit/` contains only weeks 1 to 4. Expected if this audit's output lands there next, but the link is dangling in the committed state.

17. **A passing gate line prints a contradictory reason.** `tools/check.py:1759` passes `"no header separator row"` as the always-shown `detail` rather than as `fail_detail`, producing `PASS  week5: the criteria map is a real markdown table  no header separator row` in this week's gate output. `report()`'s own docstring at :123 says `fail_detail` exists precisely to stop that. Introduced in `52c3baa`, before this window, but week 5 is the first week whose routine output shows it.

Cannot certify: approach correctness, statistical validity of results, anything requiring the blocked or external resources.
Findings: 17

## What was done about each

**1. The 8.0 g controller.** Fixed. The refined budget line is 8.5 g and the 8.0 g figure is the
week 2 envelope it replaced, so the submission was contradicting its own table three lines above
the claim. All three occurrences now read 8.5 g and the PDF is rebuilt. The auditor is also right
about why no gate caught it: a retired envelope line is still a stored mass, so the value traced.

**2. `TECHNICAL-READ-COMPLETE` is undetectable.** Reported and deliberately not changed, and D59
carries the argument. The marker is unfindable because `human-gate.md` names it in prose while
explaining what to replace, and an agent may not touch that file at all. Making the check
line-based is the obvious fix and it is not an agent's call: it would make the fifth marker block
the start of week 5, where `human-gate.md` and the plan both say it blocks final staging instead.
Two documents disagree about when that marker bites and a person owns both. This is the same
treatment the repository already gives the audit-exemption conflict between `check.py` and the
loop config: report it, do not quietly pick a side.

**3. Scope work delivered under a live blocked trigger.** Accepted as a declared deviation. The
operator directed a preparation pass explicitly, and the block itself was never worked around: no
human gate marker was written, nothing was sent to anybody, no progress file exists, nothing says
`STATUS: WEEK-COMPLETE`, and `NEXT-WEEK:` still reads 5. What the pass did is the part of week 5
that needs no person, and D58 says so in as many words. The auditor is right that the distinction
lives in the documents rather than in the config, which still reads as stop and report.

**4. The cluster rpm column.** Fixed. `01-configuration.md` now reads 3215 and 3976, matching
`configuration_candidates` and the submission built from it. The auditor's arithmetic reproduces:
at 9.0 N per rotor on 0.033454 m2 of blade at 0.6055, tip speed fixes rpm at 3214.7 for an 80 mm
radius. Two figures had been wrong since week 2 in a table column no gate reads. D59 records it.

**5. Angles written as "degrees" were invisible.** Fixed, and it is the most useful finding in the
pass. `deg` sat before `degrees` in the alternation, so the regex took the short branch, failed
its own lookahead on the "r" and matched nothing at all. `degrees` and `degree` now come first and
both map to the angle dimension. Three probes went in: a wrong angle in words fails, a wrong
angle as an adjective fails, and the design's own pitch amplitude passes. Running the fixed gate
over the submission surfaced exactly one untraced number, "about 1 degree" in examiner answer 10,
which was a rounded restatement of a difference that is in no file and now reads "about a
degree". The auditor's second point stands and is recorded in D59: the angle dimension holds 86
stored values including every multiple of 10 from the pitch schedule, so a round angle can trace
by coincidence. That is a property of a value-based coverage audit and it is not fixed here.

**6. The allow comment that exempted nothing.** Fixed by deleting it. It sat one line below the
numbers it named and `allow_reason` is per line, so it was hiding nothing, and after the angle fix
both published angles trace on value anyway. The document now carries zero escapes. D56's "hides
3 of the 4" sentence, the same sentence in the codemap and the journal's paragraph are corrected
in D59 rather than edited in place.

**7. D54 claimed a test that did not exist.** Fixed. Two probes went in: an opening delimiter with
no closing one is not front matter, and a body line sitting directly under the closing delimiter
with no blank line between is still body. The second is the off-by-one the auditor named, and it
fails if `front_matter_lines` returns one line too many.

**8. Item 7's table description.** Fixed. The sentence now describes the three column table that
is actually there and points at `07-team-and-execution.md` for the version carrying the tool
category, the dependency and the owner.

**9. "Measured" in the criteria map.** Fixed. That row now reads "a transferred coefficient held
below a measurement of this shape family", which is what the rest of the report says and what the
evidence ledger classes it as.

**10. "Item n" cross references.** Fixed. The criteria map cites sections by name, the claims
table says "Stage 2 items 3, 6 and 7" where it meant the Stage 2 list, and examiner answer 3
points at the module weight section rather than at a number pandoc renumbers.

**11. D55's placeholder claim.** Corrected in D59. Four of the nine tags appear in the submission
and the other five are report-irrelevant, so the accurate statement is that the design document
holds the full list and the report carries the ones a reader of the report has to fill.

**12. Item 7 had no substance or number gate.** Fixed. Week 5 now runs `require_substance` and
`check_declared_numbers` over `07-team-and-execution.md` like every other design document, the
test fixture gained a declaration block, and two attack cases went in: three headings with nothing
under them is rejected, and a declared value that disagrees with `numbers.json` is rejected.

**13. `human-gate.md` never names the strings a person types.** Reported, not fixed, because that
file is untouchable for an agent under the loop config and D5. The handoff's ordered human list
names all five exact strings, `REGISTRATION-CONFIRMED`, `ELIGIBILITY-CHECKED`, `ROSTER-CONFIRMED`,
`SENDER-CONFIRMED` and `TECHNICAL-READ-COMPLETE`, beside the step that earns each one, so a person
working from the handoff has them. Editing the gate file itself is a person's job and it is now an
open item.

**14. The handoff stated a weaker block than the config.** Fixed. The handoff no longer picks the
permissive reading. It says the config lists all five markers in the blocked trigger, that
`human-gate.md` says the fifth blocks final staging rather than the start, that the two disagree,
and that the gate cannot currently see the fifth at all.

**15. Five overfull lines or two.** Fixed by making both precise. The first build produced five
overfull boxes: two real ones, 20.30 pt on the paragraph carrying the organiser address beside a
code span and 4.06 pt on a table header wider than its own column, and three at 0.12 pt inside a
table alignment, which is rounding. Fixing the two removed all five. The handoff and the codemap
say that now and the journal's count was right all along.

**16. The dangling audit link.** Resolved by this file existing.

**17. The separator detail on a passing line.** Fixed. It is a `fail_detail` now, so a passing
criteria table no longer prints "no header separator row" beside the word PASS.

AUDIT-COMPLETE
