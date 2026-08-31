# Week 4 audit

One fresh-context read-only pass, run after the eleven week 4 commits landed, on the diff from
`8bcfd69` to HEAD. The findings are reproduced verbatim below and what was done about each
follows them. 13 findings: 12 fixed, 1 accepted as a declared deviation.

## The audit, verbatim

I have verified every claim against the diff, the files, and by running the read-only tooling. Findings below, most severe first.

**1. The week 4 audit file was never written, so `python tools/check.py --week 4` exits 1 - and three documents say otherwise.**
`stage-1/audit/` contains only `week-1.md`, `week-2.md`, `week-3.md`. `stage-1/progress/week-4.md:6` carries `STATUS: WEEK-COMPLETE`, so `done_set()` includes 4 and `check_audits_exist` (tools/check.py:1774) demands `stage-1/audit/week-4.md` for `--week 4`. Measured at HEAD:

```
FAIL  every completed week carries a finished audit  week 4 has no audit file
FAILED: 1 gate(s)      # week4 exit=1 ; global exit=0
```

Against this, `stage-1/progress/week-4.md:117` states `python tools/check.py --week 4 | exit 0, cumulative`; `handoff.md:146` states "Week 4 leaves all three green"; `handoff.md:25` lists `stage-1/audit/week-4.md` as a file to read first, "verbatim, and what was done about each finding". The plan's non-negotiable protocol (stage-1/plan.md:96) requires that file with `AUDIT-COMPLETE`. Week 3 shipped its audit in commit `8bcfd69` before `bed70f2` closed the week; week 4 closed in `606ac73` without one. Note `handoff.md:177-179` admits the gate fails until the audit exists, contradicting line 146 in the same file.

**2. The blade-balance trade is priced off a hardcoded stale ratio, and the document names a command that disagrees with it.**
`tools/structure.py:605-606` computes the balanced pitch-link load as `b['link_load_N'] * 0.655` - 0.655 is the week 3 balanced/unbalanced ratio (69.38/101.82) on the *old* blade, not a rerun. `03-pitch-and-vectoring.md:280` says "Running `--balanced` shows a chordwise balance would take those to about 1.06 Nm and 69.4 N." Running it:

```
$ python tools/linkage.py --balanced
  peak blade pitching moment 1.0904 Nm, peak pitch link force 74.62 N
$ python tools/structure.py --balance
  pitch link would fall to about 69.4 N, margin 5.04 against the 3.30 it already has
```

True balanced margin is 349.727/74.62 = **4.69**, not 5.04. The wrong pair (69.4 N, 5.04) is repeated in D46 ("takes the link to about 69.4 N and the margin to 5.04"), `05-mass-and-tw.md:165`, `08-structure-and-loads.md:122`, `stage-1/progress/week-4.md:78` and the journal. The decline decision itself survives (2.406 < 2.5 either way), but the numbers backing it do not.

**3. `01-configuration.md:42` puts a week 4 mass-basis number into a week 2 comparison row that explicitly claims one common model.**
The single-rotor row now reads `... | 580 g | 3.163 | 2.5457 |` while rows 2 and 3 keep week 2 basis. Line 28 of the same file states "the comparison got run on one common model. Same thrust coefficient, same figure of merit, same efficiency chain, **same mass build-up**". 2.5457 requires 684.70 g, not the 580 g in the row's own mass column (17.0992/(0.58005 x 9.81) = 3.005). It also contradicts the JSON the table renders: `configuration_candidates[0].module_tw_conservative = 2.5173`, `module_mass_conservative_g = 692.43`. `02-rotor-sizing.md` handled the same mixing honestly ("The nominal mass in rows 1 and 3 is still the week 2 envelope..."); `01` and `04-thrust-and-power.md:190-196` ("3.163 at the design point, 2.680 and 3.005 on each downside alone, 2.5457 stacked") do not.

**4. "Eight margins, all recomputed from the design, all floored at 1.5" is false for one of the eight.**
`handoff.md:74` and `08-structure-and-loads.md:150` both make this claim over an 8-row table that includes "rotor shaft, bending and torsion combined | 5.83 MPa | 55 MPa | 9.44". `structure.shaft_combined_margin` appears nowhere in `tools/check.py`: not in `recompute()`, not in the `MIN_MARGIN` loop at check.py:1649-1651, not in the `require_positive` schema list at check.py:1599-1612. `grep -n "shaft_combined_margin" tools/check.py` returns nothing. Seven margins are gated; the eighth is a stored number nothing checks.

**5. The numeric-coverage improvement is attributed to the wrong cause and the baseline is overstated.**
`handoff.md:107-110` and `stage-1/progress/week-4.md:218-220`: "It failed on 10 numbers when week 3 ran it on the draft. It now fails on 2 ... The `dim_of_key` qualifier fix in D51 took out the other 8." Measured (submission source unchanged since `8bcfd69`):

| check.py | numbers.json | untraced |
| --- | --- | --- |
| week 3 (`8bcfd69`) | week 3 | **7** |
| HEAD minus the qualifier fix | week 3 | 7 |
| HEAD | week 3 | 4 |
| HEAD minus the qualifier fix | HEAD | 5 |
| HEAD | HEAD | 2 |

The qualifier fix accounts for 3 numbers (the `17.10 N` / `17.1 N` occurrences), not 8; the rest moved because `numbers.json` changed. The gate's own week 3 count was 7, not 10 (the week-3 audit's 10 was a manual tally that included exempt-region numbers).

**6. The mass-refinement decomposition does not add up to its own stated net, in three files.**
`05-mass-and-tw.md:150-154`: "Growth rates fell from 19.4 percent to 12.6, worth 40.7 g. Against that ... the nominal column rose 27.9 g. The net is 7.7 g." 40.7 minus 27.9 = 12.8, not 7.7. The consistent figure is 35.6 g: conservative moved 692.43 to 684.70 (minus 7.73) while nominal moved 580.05 to 607.97 (plus 27.92), so the rate saving is 27.92 + 7.73 = 35.65 g. Repeated verbatim in `stage-1/progress/week-4.md:170-173` and in the week 4 journal entry.

**7. `tools/structure.py` writes `numbers.json` with the platform newline, undoing the fix `tools/linkage.py` carries a comment about, and falsifying "byte for byte".**
`tools/linkage.py:766-770` writes with `newline="\n"` and an explicit comment: ".gitattributes declares eol=lf, and the default here is the platform newline, which puts CRLF into a file every sibling document writes as LF. Git normalises it on the way in, so the damage does not show up in git status." `tools/structure.py:766` is `NUMBERS.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")` - no `newline`, no `ensure_ascii=False`. Since the documented run order is linkage first then structure, structure's CRLF always wins. Working tree: 1520 CRLF, 60101 bytes. `HEAD` blob: 0 CRLF, 58581 bytes. So `stage-1/progress/week-4.md:40` and `handoff.md:113` ("reproduces the committed `numbers.json` byte for byte") are wrong by 1520 bytes; the files agree only after git's `text=auto eol=lf` normalisation.

**8. A superseded week 3 number is hardcoded into a shipped mass-budget basis string.**
`tools/structure.py:317` writes the carrier-bearing basis as "carrying the **47.48 N** radial pull the three pitch links put into the offset post", landing verbatim at `stage-1/design/numbers.json:1016`. D48's own table records that figure moving 47.48 to 53.22 N this week, `pitch.carrier_radial_force_N = 53.22`, and `08-structure-and-loads.md:125` uses 53.22 N. `check.py` only measures basis length (`MIN_BASIS_CHARS`), never content, so nothing catches it.

**9. "The closing count is computed now" is not true - it is still a hand-kept constant.**
D51, `stage-1/progress/week-4.md:141-142` and the journal all say the self-test count was made computed after the old constant "had drifted one behind". `tools/test_gates.py:460-463` replaces the literal `22` with `PROBE_CHECKS = 24`, a module-level literal with a comment enumerating "13 coverage probes, 6 unit awareness probes and 5 --all probes", and line 1866 prints `len(CASES) + PROBE_CHECKS + len(extra)`. It was renamed and documented, not computed; it will drift again the same way. (The 123 total itself checks out: 93 cases + 24 + 6 linkage self-tests.)

**10. `.claude/codemap.md` carries a full entry for a file that does not exist.**
Lines 290-297 add `### stage-1/audit/week-4.md` with Holds/Used by/Gotcha text ("must contain the literal line AUDIT-COMPLETE and end with the 'Findings: N' line"). No such file is in the tree or the diff. Every other source file in the diff does have an accurate entry - I spot-checked the `tools/structure.py` Gotcha word against code and it holds: `margins()` returns exactly 8, the budget is 33 rows and the BOM 25, `build()` reads only geometry/operating/performance/efficiency/pitch and no week 4 key, and the "blade" naming constraint matches `check.py:411-414` exactly.

**11. D51's "Nothing was loosened" is only partly true.**
`tools/check.py:1013-1022` changes week 2 from "conservative mass matches the conservative envelope lines" (exact equality to `mass_envelope_g`'s conservative sum) to "matches the refined budget lines" whenever `budget_conservative_total` returns a value. The replacement tie to the envelope is the new plus or minus 25% band in `check_conservative_budget` (check.py:1478-1491). So an exact sum rule over the week 2 conservative column was replaced with a 25%-wide band; the envelope's conservative column is now only held by `CONSERVATIVE_MASS_MIN_RATIO`. Confirmed live: `PASS week2: conservative mass matches the refined budget lines  lines give 684.7 g, stated 684.7 g`. The change is deliberate and argued in D47; the "nothing was loosened" sentence is what overreaches.

**12. `06-materials-and-manufacturing.md:25` credits the epoxy paste with a margin nothing computes.**
The material table's "The margin it sets" column reads "bond lines, sized on area" for Araldite 2011. `MATERIALS["epoxy_paste"]` (`tools/structure.py:71-74`) is referenced only once in the file, inside the basis string for the "structural adhesive at module joints" mass line; no bond-line demand, allowable or margin exists in `structure.py`, `check.py` or `08-structure-and-loads.md`, whose assumptions instead say "Bond lines are treated as continuous". The line above the table ("Every material here was chosen because a structural calculation ... needed an allowable") does not hold for this row.

**13. Plan deviation, declared: the BOM has no quote date.**
`stage-1/plan.md:436-439` asks for "quantity, supplier or calculation basis, **quote date**, unit cost, lead time and Indian source". The delivered field is `priced_date` and no supplier was contacted. This is argued in D52, flagged in bold in `06-materials-and-manufacturing.md:120-124`, and carried as debt 1. Recording it as a deviation from what the week section asked for, not as concealment.

Everything else in the week section reconciles: all 7 tasks have artefacts in the diff; the four gate-checked structural derivations, both centrifugal cases, all four T/W cases, the 33 budget lines, the 13 group-continuity rows, the BOM totals (36970 / 28800 / 65770), the 15.00 g visible reserve, the 50.87 g D17 gap and the 12.5 g stacked clearance all reproduce from `numbers.json` and the scripts. The four new attack cases are real tests, not mirrors: `token_overspeed` and `aero_only_blade` each store a fully self-consistent structure block and fail only on the new rule, and `asserted_centrifugal_bending` isolates the derivation check without tripping the margin floor.

Cannot certify: approach correctness, statistical validity of results, anything requiring the blocked or external resources.
Findings: 13

## What was done about each

**1. The missing audit file.** This one is the audit auditing its own absence, and the loop's own
order produces it: the audit runs after the week's commits, so at the moment it ran, the file it
was about to become did not exist. This file is that file, and `--week 4` exits 0 with it in
place. The handoff's two statements are both true in the order things actually happen and the
open item at the bottom of the handoff already says so. Week 3 recorded the same thing as its
debt 12: `check.py` demands the current week's audit while `.claude/weekly-loop.md` says the
current week is exempt. It stays a reported mismatch, because the config belongs to a person.

**2. The stale balance ratio.** Fixed, and it is the worst finding in the set. `balance_report`
called `linkage.solve(data, balanced=True)` now instead of multiplying by 0.655, and the numbers
that reach prose are 74.62 N and a margin of 4.69, with the balanced pitching moment at 1.0904
Nm. Corrected in `03-pitch-and-vectoring.md`, `05-mass-and-tw.md`, `08-structure-and-loads.md`,
the progress file and the journal, and carried into the frozen log by D53 rather than by editing
D46. The decision does not move: balancing still costs 35.47 g and still puts the stacked case at
2.4061, under the limit.

**3. A week 4 figure in a week 2 comparison row.** Fixed. The single rotor row is back to 2.517,
which is the number its own 580 g mass column gives and the number `configuration_candidates`
stores, and a note under the table says the whole comparison is on the week 2 envelope and that
the winning row is 2.5457 on the refined budget. D32's requirement is still met, because the
document states 2.5457 in its opening paragraph. `04-thrust-and-power.md` now names which two of
its four cases are on which basis.

**4. The margin table's eighth row.** Fixed both ways. `check.py` floors
`structure.shaft_combined_margin` at 1.5 now, with an attack case behind it, and both
`08-structure-and-loads.md` and the handoff say plainly that seven of the eight are recomputed by
the gate and that this one is floored but not recomputed, because it needs shaft section
properties that live in the solver.

**5. The coverage numbers.** Fixed. Both the handoff and the progress file now carry the
measured figures: the gate reported 7 on week 3's numbers, reports 2 now, the qualifier fix
accounts for 3 of the 5 and the week 4 budget for the other 2, and week 3's debt of 10 was a
manual tally that counted exempt-region numbers.

**6. The decomposition arithmetic.** Fixed in all three files. The growth allowance fell from
112.38 g to 76.73 g, which is 35.65 g, the nominal column rose 27.92 g, and 35.65 less 27.92 is
the 7.73 g the conservative column moved.

**7. The newline.** Fixed. `tools/structure.py` writes with `newline="\n"` and
`ensure_ascii=False`, matching `tools/linkage.py`, with a comment saying why. The working tree
file is 58581 bytes with no CRLF in it and reproduces byte for byte from the two scripts with no
git normalisation in between, so the claim in the progress file and the handoff is now true as
written. D53 carries it.

**8. The hardcoded 47.48 N in a basis string.** Fixed. The carrier bearing line reads
`data['pitch']['carrier_radial_force_N']` and the stored basis says 53.22 N. Nothing gates basis
content and that stays true: the gate measures length only, and this was caught by reading.

**9. The self-test count.** Fixed properly this time. Every self-test line in `test_gates.py`
goes out through one print prefix, so the counter appends there and the closing total is
`len(ANNOUNCED)`. It is counted at the point of printing rather than derived beside the loops,
and the per-block constant is gone. 124 checks, printed and reported.

**10. The codemap entry for a file that did not exist.** Resolved by this file existing. The
entry describes it accurately.

**11. "Nothing was loosened".** Accepted and withdrawn in D53. One exact rule, the week 2
conservative mass matching the envelope's own lines, was replaced by a 25 percent band on purpose
under D47, and three new rules went in beside it. The claim as written was wrong.

**12. The epoxy row.** Fixed. The material table says "none yet" for that row and the paragraph
above it says plainly that five of the six materials have a computed margin and the adhesive does
not, that no bond line demand or allowable is computed anywhere in week 4, and why the allowable
is on the record anyway.

**13. The BOM's quote date.** Accepted as a declared deviation. The plan asks for a quote date
and no quote exists, so inventing one would be the worse answer. D52 argues it, the document
flags it in bold, and it is debt 1 in the progress file.

AUDIT-COMPLETE
