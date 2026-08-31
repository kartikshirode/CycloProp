# Week 3 audit

One fresh-context read-only pass over week 3, run after the seven week 3 commits landed and
before the audit file existed. Reproduced verbatim below, then what was done about each finding.

The auditor read the plan's week 3 section, the diff from the tick start at `1e1e15f` to HEAD,
the new and changed tests and every document week 3 touched. It ran the gates itself and
replayed `tools/linkage.py` against the pre-week-3 `numbers.json`, which is how finding 1 was
caught.

---

## The audit, verbatim

I audited week 3 without editing anything. I read the plan's week 3 section, the full diff from `1e1e15f` to HEAD (working tree is clean, no uncommitted changes), ran the gates and the self-tests, replayed `tools/linkage.py` against the pre-week-3 `numbers.json`, and checked every claim in the progress file, journal, decisions, handoff and submission against what the diff actually contains.

## Findings

**1. `tools/linkage.py` cannot be run against the committed repo, so nothing week 3 produced can be regenerated or verified from the tool that produced it.** `write_numbers` (tools/linkage.py:726) overwrites `aero_azimuthal_loads` with the week 3 solved table, while `main` (tools/linkage.py:743-747) first calls `check_week2_model`, which rebuilds week 2's *prescribed sinusoid* forces and compares them against that same key, then `raise SystemExit` above 1e-3 N. Evidence: `python tools/linkage.py` on HEAD prints `week 2 model reconstruction: worst row error 4.42e+00 N` and exits without producing a report. With the pre-week-3 `numbers.json` restored the same script prints `5.24e-05 N` and reproduces every published figure exactly (0.0154 m offset, 58.58/143.23 transmission, 1.1951 rms, 15.0061 N peak, 0.1371 Nm carrier, 148.03/86.54 swept radii, the whole vector map). The solver is correct; it is self-poisoning. The plan's stated point for task 2, "keep the small calculation script used to solve it", and the repo's "reproducible rather than asserted" framing are both defeated for week 4 onward.

**2. Five documents claim in the present tense that running the script does something it now cannot.** `03-pitch-and-vectoring.md:10-13` ("Run it with no arguments for the report"); `04-thrust-and-power.md`, Azimuthal load distribution ("running that script with no arguments reproduces the week 2 sinusoid table to 5.2e-5 N on every row before it moves on"); `progress/week-3.md:45-47`; `decisions.md` D41; `handoff.md:119-120`. All were true before `--write` ran and are false against the committed tree. `tools/linkage.py:35` additionally states 5.3e-5 N where the run prints 5.24e-05 and every other document says 5.2e-5.

**3. D38, a frozen decision, rests on a carrier torque the delivered sweep does not produce, and overstates its own margin by 1.7x.** `decisions.md:832` says the sweep shows 111.6 mm "sitting at 0.297 Nm of carrier torque"; `python tools/linkage.py --sweep` gives **0.3240 Nm** for L4 24.4 / L3 111.6, in a row whose other two figures (mu_min 40.97, rms 2.668) match D38 exactly, so it is the right row. `decisions.md:836` then says "Four times the torque ... is the number that decided it"; the real ratio is 0.3240/0.1371 = **2.36x**. The same line claims "At 111.6 mm the two servos together cannot hold the carrier on half of their stall torque"; recomputing gives a servo margin of exactly **1.000** on half stall, so they hold it with no margin rather than failing. `journal.md:218` goes further with "a servo that can hold about a tenth of that", which is off by roughly 3x even taking the stated torque at face value. 0.297 Nm is repeated at `03-pitch-and-vectoring.md:65`, `journal.md:232` and `handoff.md:117`, and is in no gated key.

**4. The plan's packaging deliverable is a dimensioned sketch and no sketch was produced; the progress file rewrote the task to match.** Plan task 7 (stage-1/plan.md:363-365): "**Draw** the swept linkage envelope, blade clearance, shaft supports, bearings, motor and transmission, actuator, ESC, controller, wiring and mounting points ... Dimensioned sketches are enough. No CAD." The plan names it twice more, at line 176 ("packaging sketch") and line 529 ("Dimensioned moving-envelope sketches"). `09-packaging-and-integration.md` contains three tables and prose and zero figures, images or ASCII layouts, and the built PDF has none. `progress/week-3.md:26-27` restates the task as "Package the moving mechanism, with the swept envelope, interfaces and the reaction torque path", dropping the verb and the sketch, then declares "All eight ran". `check.py` gates only headings and word count here, so nothing catches it. This is the 5 percent packaging criterion.

**5. Plan task 4 requires a named controller and none is named; the progress file dropped that word too.** Plan stage-1/plan.md:347-348: "Tie those to a named actuator **and controller**." The actuator is named (Corona DS-929MG class, `03-pitch-and-vectoring.md:276`). The controller appears only as "the offset controller board" (`09-packaging-and-integration.md:65`) and `performance.controller_power_W = 2.0`; no part, class or supplier anywhere in the diff. `progress/week-3.md:22-23` restates the task as "on a named actuator", omitting the controller.

**6. The new lateral-load column is unprotected: dropping it leaves every gate green.** `check_lateral_loads` (tools/check.py:1270-1291) returns `True` whenever any row's `lateral_force_N` is missing, `ROW_SPECS["aero_azimuthal_loads"]` (tools/check.py:615) still requires only `("azimuth_deg", "normal_force_N")`, and `pitch.peak_lateral_force_N` is absent from week3's `require_positive` list (tools/check.py:1295-1301). Deleting the column and the stated peak passes `--week 3` and `--week 4` while removing the 10.10 N per-blade instantaneous side load that `03-pitch-and-vectoring.md:260-263` and `handoff.md:86` hand to week 4 as a bearing and frame demand. The docstring calls this deliberate ("a week 2 table without the column is left alone"), but week 3 is the week that added the column and nothing requires it to stay.

**7. The vectoring reserve, one of the week's headline conclusions, rests on a figure's axis tick labels.** The plan (stage-1/plan.md:355-357) says "the measured 10 to 35 degree literature range", and `literature.md:235` records "Adams 2013 measured the resultant tilted 15 to 35 degrees ..., Sirohi about 10 degrees, Benedict 30 degrees". `03-pitch-and-vectoring.md:224-226`, `journal.md`, `handoff.md:122` and the submission (`cycloprop-stage1.md:81`) instead assert "Benedict's figure 2.33 gives the resultant phase between 10 and 45 degrees". In `reference/benedict2010-extract.txt:4895-4937` the only "10 ... 45" is the sequence of y-axis tick labels for Figure 2.33; the extract carries no plotted values. That widened band is exactly what produces the "17.5 degrees either way" and "120 degrees of authority becomes 85 degrees usable" conclusion carried into the handoff and the submission.

**8. The new force-map tracking gate cannot fail for anything the solver produces.** `solve` (tools/linkage.py:511-528) evaluates each command by rotating the schedule and re-settling the inflow together, and the model is exactly rotationally equivariant, so the stored `vector_map` has `resultant_N` = 18.0000 at all five commands and `resultant_direction_deg` identical to `phase_command_deg` to 4 decimals. `check_vector_map`'s "the force direction turns with the phase command" (tools/check.py:1255-1266) therefore holds by construction. `03-pitch-and-vectoring.md:207-216` and D42 are admirably honest that the table "is a statement about the model's symmetry ... not a measurement of force magnitude", but D42 and `handoff.md:125-127` then present the gate as a strengthening ("the vectoring gate now tests the force map") when against the real generator it has no discriminating power. It only catches hand-written tables.

**9. D44's corrected packaging figures use different arithmetic than the week 2 table they claim to reuse.** `01-configuration.md:35-37` gives each rotor its own 20 mm clearance, and its table (400 mm for two rotors, 490 for three) is `n*(2R+20)+40`. D44 says "Applying the swept diameter to the same rule gives 356 mm for one rotor, 491 for two and 585 for three"; 491 and 585 only come from `n*D_swept + 20 + 40` (2*215.3+60 = 490.6; 3*174.9+60 = 584.8). Under week 2's actual rule they are 510.6 and 624.8. Repeated at `09-packaging-and-integration.md:17-18`. The ordering conclusion survives either way, and none of these numbers is in `numbers.json`, so no gate touches them.

**10. D40 misstates the band its structural conclusion rests on.** `decisions.md:875-877`: "it happens whenever L3 minus L2 falls inside the band L1 minus L4 to L1 plus L4, which for this link set is 89.6 mm to 134.4 mm against an actual 89.6 mm." L1 - L4 = 110.0 - 24.4 = **85.6** mm, not 89.6. As written the actual value sits exactly on the boundary, which would make the single-ended drive a knife-edge case rather than the structural certainty D40 claims; with the correct band it sits 4 mm inside. The symbolic version at `03-pitch-and-vectoring.md:95` is correct.

**11. Two documents state that the week 3 gate is green; on the committed tree it exits 1.** `python tools/check.py --week 3` fails with "every completed week carries a finished audit: week 3 has no audit file". `progress/week-3.md:103` claims "exit 0, cumulative over weeks 1 to 3" and `handoff.md:147` claims "Week 3 leaves all three green". `check_audits_exist` (tools/check.py:1676-1684) iterates `x <= target` over `done_set()`, so once the progress file carries `STATUS: WEEK-COMPLETE` the week's own audit is demanded, contradicting both its own docstring ("The week being gated right now is mid-flight and its audit does not exist yet") and `.claude/weekly-loop.md` ("The week being gated right now is exempt"). The code-versus-config mismatch is pre-existing, but the two green claims are false as committed. Related: `handoff.md:23` lists `stage-1/audit/week-3.md` under "Read these first" as "the week 3 fresh-context audit, verbatim, and what was done about each finding"; that file does not exist and nothing has been done about any finding. `--global` and `test_gates.py` do both exit 0 (115 self-tests, count verified).

**12. Two codemap Gotcha lines overstate safety constraints, and one describes a tool that runs.** (a) The `numbers.json` entry says "The pitch, schedule, vector map and azimuthal load blocks are written by `tools/linkage.py --write` and hand editing any of them breaks the loop closure test in test_gates.py"; `loop_residual` is called only on `d["pitch_schedule"]` inside `linkage_selftests`, so hand-editing `vector_map`, `aero_azimuthal_loads` or the `pitch` scalars does not touch it. (b) The `test_gates.py` entry says "`linkage_selftests` is the only part that touches the real repo"; `REAL_PDF` (tools/test_gates.py:29) is the real `reference/cycloprop-problem-statement.pdf`, copied into throwaway trees at tools/test_gates.py:1376. (c) The `tools/linkage.py` entry's Gotcha ("It reconstructs week 2's load model first and stops if that no longer reproduces") describes a runnable tool, which per finding 1 it no longer is. Everything else I checked in the codemap is accurate: every source file in the diff has an entry, the check.py/test_gates/03/09/submission/pdf/progress entries match current content, the `Used by:` lines are right, and the 115 = `len(CASES) + 22 + len(extra)` arithmetic holds.

**13. Load-bearing constants live in `linkage.py` instead of `numbers.json`, against the project's "only place a number is defined" rule.** `CARRIER_GEAR_MM = 40.0` and `SERVO_GEAR_MM = 60.0` (tools/linkage.py:87-88) are, in the script's own comment, "the whole claim behind the phase authority", and neither is stored; the submission quotes "a 60 mm sector gear onto a 40 mm ring" and both numbers fail the coverage audit. `BLADE_PARTS_G` (tools/linkage.py:68) duplicates a per-part build-up that exists only as prose in `02-rotor-sizing.md:89-90`; it alone determines `blade_cg_pct_chord = 39.92`, and therefore the 2.1201 Nm moment and 101.82 N link load that D43 and `handoff.md:71-77` hand week 4 as a mass trade. It will not follow a week 4 change to the blade, and no gate can see the drift. Same class: `SERVO_MASS_G`, `SERVO_SPEED_S_PER_60DEG`, `SERVO_CURRENT_A`, `SERVO_USABLE_FRACTION`, `STALL_CAP_DEG`, `MOUNT_POINTS` and the six packaging allowances at tools/linkage.py:91-97.

**14. The submission draft fails the week 5 coverage gate on 10 numbers, one of which is a gate defect, not a writing defect.** Running `check_numeric_coverage` on `stage-1/submission/cycloprop-stage1.md` gives: `5: 25mm` (the pandoc `geometry: margin=25mm` front matter, not narrative at all), `52/53: 17.10 N`, `55: 4.8 g`, `66: 125.4 mm`, `75: 12.5 g`, `75: 60 mm`, `76: 40 mm`, `90: 17.1 N`, `121: 29.4 g`. The 17.10 N failures are a `dim_of_key` defect (tools/check.py:490-496): it matches units only as a key *suffix*, so `performance.thrust_N_conservative = 17.0992` is never collected and the design's own conservative thrust cannot trace. Debt 9 of the progress file honestly discloses that this gate has not been run; the count and the root cause are what week 4 and 5 need.

**15. Three smaller doc-versus-code slips.** (a) D42 says of the five new attack cases that "each was confirmed to fail on the gate it targets rather than incidentally"; replaying each mutation through `check_vector_map`/`check_lateral_loads` shows `command_outside_the_authority` trips two gates, the authority check and the tracking check. The other four are clean single-gate hits. (b) D42 and `handoff.md:150` count "three force map checks and two lateral load checks"; `check_vector_map` emits four reports, the undocumented one being "every mapped command produces a force". (c) `progress/week-3.md:92` says "gained five checks", same undercount. None of this loosens anything; the diff to `check.py` is additive only, as claimed.

**16. `write_numbers` writes CRLF into a repo that declares `eol=lf`, and replaces whole blocks rather than updating them.** `NUMBERS.write_text(...)` (tools/linkage.py:728) opens in text mode with the platform newline, so on Windows all 988 lines of `stage-1/design/numbers.json` are CRLF on disk while `.gitattributes` declares `* text=auto eol=lf` and sibling markdown is LF. Git normalization hides it in `git status`, so the tree looks clean while a `git checkout` of that file silently rewrites every line; `newline="\n"` fixes it. Separately, `write_numbers` assigns `data["packaging"]` and `data["aero_azimuthal_loads"]` wholesale, so any key a later week adds to those blocks by hand is deleted by the next `--write`.

## What I verified as sound

The linkage work itself reproduces exactly when the input file is restored, and it is genuinely good: the loop closure, Grashof classification, transmission angle, clearances, phase delay and rms residual all check out, the cycle mean vertical force is still 6.0000 N per blade so week 2's thrust gate survives the rerun, no `mass_envelope_g` line or `results` value moved (verified key by key), and the only value changed outside week 3's own blocks is `blade_load_peak_to_mean` 2.374 to 2.501, which no gate reads (week 4's 4.0 floor reads `structure.blade_load_factor`, a different key, so there is no cross-week break there). `loop_residual` in `test_gates.py` is the strongest new test in the repo: it is independent of the solver, it confirms 6.8e-08 m closure on the published rows, and one degree of hand editing shows as 3.8e-04 m. The PDF claims all check: 5 pages, 45,054 bytes, all seven required headings and all six spot probes present. `--global` passes, no dashes, no AI attribution. Week 3 also delivered structural quantities the plan assigns to week 4 (blade pitch inertia, blade pitching moment, pitch link force, carrier radial force); that is extra rather than missing, and it is disclosed as debts 1 to 3.

Cannot certify: approach correctness, statistical validity of results, anything requiring the blocked or external resources.
Findings: 16

---

## What was done about each finding

**1. Fixed.** `check_week2_model` compared its reconstruction against the live
`aero_azimuthal_loads`, which `--write` had already replaced, so the script disabled itself the
first time it succeeded. The week 2 published table is now a 36 value constant,
`WEEK2_PUBLISHED_LOADS`, carried in `tools/linkage.py` with the commit it was taken from. The
reconstruction check reads that and never reads `numbers.json` for it. `python tools/linkage.py`
runs on the committed tree and prints 5.24e-05 N again.

This was the worst finding in the set and it was invisible from inside the session, because the
script was only ever run before `--write` or in the same breath as it. The auditor found it by
replaying the tool against the pre-week-3 file, which is exactly the check a fresh context can
do and a working one will not think to.

**2. Fixed** by 1, and the docstring's 5.3e-5 corrected to 5.2e-5 so every statement of that
number matches.

**3. Fixed.** The 0.297 Nm figure is from a sweep run before the resultant magnitude
normalisation was corrected, and it never got refreshed. The delivered sweep gives 0.3240 Nm, a
ratio of 2.36 rather than four, and a servo margin of exactly 1.000 at 111.6 mm rather than a
failure. D45 records the correction, since the log is append only, and the derived claims in
`03-pitch-and-vectoring.md`, `journal.md` and `handoff.md` were corrected in place. The decision
itself stands: 105 mm still wins on every axis the sweep measures.

**4. Fixed.** Two dimensioned text layouts were added to `09-packaging-and-integration.md`, one
along the rotor axis and one in the rotor plane, carrying the swept annulus, the pitch plane
keep-out, both bearing stations, the belt end, the phasing carrier, the motor stack and the four
mount lugs. The progress file's task 7 line was restored to the plan's wording.

**5. Fixed.** The controller is named: a Matek Systems F411-WSE class board, 8.5 g in a 28 by 28
by 14 mm case with four servo outputs and a 3.5 A servo rail, taking the 6S pack directly. Its
evidence class is a supplier listing like the servo, and it is 0.5 g over the 8.0 g week 2
nominal and inside that line's 9.2 g conservative figure, which is debt 10. The progress file's
task 4 line was restored to the plan's wording.

**6. Fixed.** `lateral_force_N` is now a required field on `aero_azimuthal_loads` in `ROW_SPECS`,
and `pitch.peak_lateral_force_N` joined week 3's `require_positive` list. Two attack cases were
added: dropping the column, and dropping the stated peak. 115 self-tests to 117.

**7. Fixed.** The claim was widened past what our own extract supports. Benedict's figure 2.33
carries no plotted values in the text extract, only the axis labels, so the band is now stated as
the plan states it and as `literature.md` sources it: Sirohi about 10, Adams 15 to 35, Benedict's
twin 30, giving 10 to 35. What the Benedict text does support is quoted as text rather than as
numbers, that the tilt rises with rotational speed and with blade count. The trim residual falls
from 17.5 to 12.5 degrees and the worst case usable range rises from 85 to 95 degrees, and both
were corrected in `03-pitch-and-vectoring.md`, `handoff.md`, `progress/week-3.md`, the submission
and D45.

**8. Accepted, and the overclaim corrected.** The finding is right: against this solver the
tracking check cannot fail, because an axisymmetric rotor with a self-consistent inflow is
rotationally equivariant. What the check does catch is a hand-written or flat force table, which
is what the old two-scalar comparison let through, and that is now what D45 and the handoff claim
for it. No gate was removed.

**9. Fixed.** The week 2 rule gives each rotor its own 20 mm of clearance, so the cluster figures
under the swept diameter are 510.6 mm and 624.8 mm, not 491 and 585. Corrected in
`09-packaging-and-integration.md` and in D45. The ordering conclusion is unchanged and was
already unchanged under either arithmetic.

**10. Fixed** in D45. L1 minus L4 is 85.6 mm, so the band is 85.6 to 134.4 mm and the actual 89.6
mm sits 4 mm inside it rather than on the boundary.

**11. Fixed** by this file existing. `--week 3` exits 0 with the audit in place, which is the
state both documents describe. The underlying code-versus-config mismatch, that `check.py`
demands the current week's audit while `.claude/weekly-loop.md` says the current week is exempt,
is pre-existing, is harmless in the order the loop actually runs, and is recorded as a debt
rather than changed, because the config belongs to a person.

**12. Fixed.** All three Gotcha lines corrected: the loop closure test reads `pitch_schedule` and
only `pitch_schedule`, `REAL_PDF` is named as the second thing `test_gates.py` reads out of the
real repository, and the `linkage.py` entry no longer describes a behaviour finding 1 had
removed.

**13. Partly fixed.** The two gear diameters and the servo mass are now stored in `numbers.json`
and cited from the documents, so the phase authority claim traces. `BLADE_PARTS_G` and the
packaging allowances are not moved: they are inputs to a derivation rather than published
numbers, and moving them would put a dozen unchecked values into the schema for week 4 to trip
over. The drift risk the finding names is real and is carried as a debt, with the specific
instruction that week 4 has to re-run `tools/linkage.py` if it changes the blade build-up.

**14. Recorded as a debt with the root cause named.** Week 5 owns the submission gate and the
draft is a skeleton. Three of the ten failures were retired by storing the gear and servo mass
values under 13. The `dim_of_key` suffix defect that stops `performance.thrust_N_conservative`
from tracing is a real gate bug and is written into the debt list for week 5, which is the week
that has to make the submission pass.

**15. Fixed.** The counts are corrected in D45 and in place in `handoff.md` and
`progress/week-3.md`: six new checks, four of them in `check_vector_map`, and one of the five
attack cases trips two gates rather than one.

**16. Fixed.** `write_numbers` now writes with `newline="\\n"`. The wholesale block assignment is
left as it is and documented instead: `packaging`, `aero_azimuthal_loads`, `pitch_schedule`,
`vector_map` and `linkage_dimensions` are all wholly derived, so a hand-added key inside them
should not survive a re-solve, and the codemap Gotcha now says so.

AUDIT-COMPLETE
