AUDIT-COMPLETE

# Round 10 verification

Audit date: 23 September 2026. Supersedes the verdict in `codex-final.md` for the files changed after commit `59ad408`; that round 9 audit remains the record of the original findings.

| Round 9 finding | Status | Proof |
| --- | --- | --- |
| F2, staged email | Partly fixed | `stage-1/submission/email-draft.md:35-45` now agrees with the report, and `stage-1/organiser-email.md:14-39` asks the format question early. `[SENDER NAME]` remains at email lines 27 and 50 and organiser email line 36. |
| F3, criteria map | Fixed | `stage-1/submission/cycloprop-stage1.md:735-738` says 34 lines, one nominal pass and three downside misses, and points structure at its own section. |
| F4, stale results | Partly fixed | The angle, side-force split, power, peak load, pitch-link margin and fixed-mass text now match `numbers.json` at report lines 233-236, 277-279, 354-363, 415, 855-861, 993 and 1056. The vector caption at line 296 still misattributes the tilt. |
| F5, internal T/W contract | Fixed as disclosure | Report lines 497-515 say the old downside rule was broken and give the closing mass. The engineering shortfall itself remains. The 2.0 at line 586 is a bearing safety floor, not a T/W floor. |
| F6, thin nominal pass | Fixed as framing | Report lines 34-40 and 497-509 call the 0.8 percent pass preliminary and say the mass estimate cannot support that accuracy. |
| F7, references | Partly fixed | Report lines 777-826 add a reference list and numerical locators, but reference 8 at lines 800-801 has the wrong year. |
| F8, audit context | Fixed | `_codex-context.md:48-64` carries the D70 mass, power and T/W values and describes the pending human work. |

## Findings, highest first

### 1. Medium: reference 8 has a false publication year

`stage-1/submission/cycloprop-stage1.md:800-801` prints *Aerospace* 13(9), article 765 as 2025. The [publisher's article page](https://www.mdpi.com/2226-4310/13/9/765) gives 2026 and DOI 10.3390/aerospace13090765. The same wrong year is at `stage-1/design/evidence-ledger.md:46` and `stage-1/literature.md:232`. Reproduce by opening the publisher page beside those lines. This costs credibility precisely where F7 was meant to make the borrowed load factor traceable. Replace report lines 800-801 with:

> 8. Alsabri, A. A. M. et al. *Independent Effects of Blade Number and Solidity on Cyclorotor Hover Performance: A Parametric CFD Study for Design Optimization.* *Aerospace* 13(9), article 765, 2026. https://doi.org/10.3390/aerospace13090765. Summary class, not read here.

Replace `Aerospace 13(9):765, 2025` with `Aerospace 13(9):765, 2026` in the ledger and literature record. Rebuild the PDF.

### 2. Medium: the vector-map caption contradicts the corrected split

`stage-1/submission/cycloprop-stage1.md:296` calls all 9.078 degrees a lag in the aerodynamics. Lines 277-279 and `stage-1/design/numbers.json` give 7.75 degrees from the linkage and about 1.33 from aerodynamics. Reproduce by reading the caption beside that paragraph in the source or the built PDF. A reviewer checking the figure against the mechanism text gets two explanations for one result. Replace the last sentence of the caption with:

> At zero command the resultant sits 9.078 degrees off the offset direction: 7.75 degrees from linkage phase delay and about 1.33 degrees from the aerodynamic model, not a commanded tilt.

Rebuild the PDF after the caption edit.

## Checks and score

The rounded configuration ratios at report lines 72-78 match `numbers.json:191-266`; the four T/W cases at lines 490-495, the 117.26 g gap, the 518.0 W power total, and the email's 0.8 percent statement also match. Appendix B's 2.5458 and 3.2878 declarations match their stored keys. The PDF is 32 pages and the current result strings appear in its extracted text. The format query at `stage-1/organiser-email.md:19-39` is clear and matches that page count, but it is not safe to send with `[SENDER NAME]` still present. Item 7 still has `[P-1]` to `[P-9]` in `stage-1/design/07-team-and-execution.md:46-128` and report line 725; a person owns those facts.

`python -B tools/check.py --all` passed. `python -B tools/check.py --week 5` failed only on `TECHNICAL-READ-COMPLETE`, as expected. `python -B tools/test_gates.py` ended with `All 223 gate self-tests behaved as expected.`

| Criterion | Round 10 | Basis |
| --- | --- | --- |
| Thrust feasibility | 11/15 | Carried from round 9. |
| T/W feasibility | 7/15 | Framing half improved by one point; the underlying three downside misses remain. |
| Kinematics | 13/15 | Current values now agree, with the caption attribution still wrong. |
| Aerodynamics | 7/15 | Carried from round 9. |
| Structure | 9/15 | Carried from round 9. |
| Manufacturability | 7/10 | Carried from round 9. |
| CAD and integration | 4/5 | Power and fixed-mass interface text now agrees; no Stage 1 CAD is claimed. |
| Presentation | 7/10 | Criteria map and most references repaired; one citation and one caption remain wrong, and item 7 is still open. |
| **Total** | **65/100** | Four untouched criteria carried; four touched criteria rescored. |

**Verdict: do not send yet.** Correct the citation and caption, rebuild the PDF, and have a person fill the sender and item 7 from real team facts. The format question should go from the registered address once its sender is filled. The human technical read remains the final gate.
