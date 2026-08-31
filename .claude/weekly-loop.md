# Weekly loop config: CycloProp Stage 1

Per-repo config for the `weekly-loop` skill. One tick runs one plan week.

This is a design and writing project, not a code project, so the gates are document integrity and arithmetic consistency rather than unit tests on product code. They are real: the numbers in the submission have to reproduce from the stored geometry, so a week cannot pass by writing a flattering number into prose. The gate script itself does have a test suite, at `tools/test_gates.py`.

## Paths

```
repo_path:      c:/Users/Kartik/Documents/Kartik/EDU/Local/Projects/Techfest/PUSHPAK-Grand-Challenge/CycloProp
plan_file:      stage-1/plan.md
handoff_file:   handoff.md
context_file:   context.md
progress_dir:   stage-1/progress
progress_file:  stage-1/progress/week-{N}.md
audit_dir:      stage-1/audit
audit_file:     stage-1/audit/week-{N}.md
decisions_file: stage-1/decisions.md
journal_file:   stage-1/journal.md
numbers_file:   stage-1/design/numbers.json
sentinel_path:  .claude/weekly-loop-sentinel.json
```

The sentinel is gitignored on purpose. If it were tracked, the clean-tree gate would fail every tick.

## Gate commands

Every one of these runs in the supervisor's own shell after the week-agent finishes. Exit code 0 is the only thing that counts.

```
python tools/check.py --week {N}
python tools/check.py --global
```

`--week {N}` validates that week's deliverable files exist with their required sections, that `numbers.json` carries the keys that week is responsible for, and that the arithmetic reproduces. `--global` runs the style and attribution checks over every markdown file we wrote.

What the arithmetic gate actually checks, so nobody assumes it is decorative: tip speed against rpm and radius, Reynolds against tip speed and chord, thrust against geometry and the blade-area coefficient, electrical power against aerodynamic power and the efficiency chain, the mass lines against the stated total, weight against mass, thrust-to-weight against both, and centrifugal load against blade mass, speed and radius.

Two properties matter more than the list.

**Hard limits are applied to recomputed values, never stored ones.** An earlier version compared stored headline numbers against the limits while only checking consistency to 2 percent, which let a 1.9 percent overstatement of thrust and a 1.9 percent understatement of mass compound into a design that missed both targets and passed every gate. Internal arithmetic now has to reproduce to 0.5 percent, and the limits are tested against what the geometry and the mass lines actually give.

**There is no 408 g gate.** 408 g is only the ceiling when thrust is exactly 10 N, and the requirement is at least 10 N. The gate tests the real requirement: recomputed thrust at or above 10 N, and recomputed T/W above 2.5.

Since D30 that limit is applied to four cases rather than one. Week 2 gates the design case, the mass downside on its own and the coefficient downside on its own, and it states the stacked case where both apply together. The stacked case is gated hard in week 4 instead, against a budget built from real sections. D33 then found that the week 4 test was reading a single stored scalar and rebuilt it: every `mass_budget_g` line carries its own `conservative_g`, no line may shrink under growth, and `results.mass_g_conservative` has to equal their sum. Read D30 and D33 before touching any of it.

**One gate asks whether the design is physically possible, and the rest only check that the arithmetic agrees with itself.** That one is the momentum bound in week 2. Aerodynamic power must sit at or above the ideal induced power over a declared area no larger than 2R times span, and the resulting figure of merit must land between 0.20 and 0.75. Before it existed the gate certified 13.5 N produced by 1 W, with every stored number in perfect agreement. Week 4 carries the structural half of the same idea: per-blade mass, shaft torque and blade root bending are recomputed from the design rather than read back from where they were asserted.

Weeks are cumulative, so `--week 4` reruns 1 through 3 and a later week cannot pass by breaking an earlier one. The gates have their own test suite at `tools/test_gates.py`, which builds throwaway trees and checks that an honest design passes while a long list of specific attacks fail. Run it after changing `check.py`, and add cases when you add a gate.

## Markers

```
done_marker:      STATUS: WEEK-COMPLETE
audit_marker:     AUDIT-COMPLETE
next_week_marker: NEXT-WEEK: {N_plus_1}
```

The done marker goes in the week's progress file, the audit marker at the end of the week's audit file, and the next-week marker as a literal line in `handoff.md`.

## Checkpoints

```
checkpoint_every: 1
human_gate_advisory_before_week: 2
human_gate_required_before_week: 5
```

The plan's week H holds the human tasks: registration, the eligibility check, the roster and who sends the submission. They are **advisory before week 2**, since the engineering does not depend on them, and a **hard block on week 5**, which cannot write a real capability section or stage a submission without them. If week H is outstanding when week 2 starts, run week 2 and record the gap. If it is outstanding when week 5 starts, report BLOCKED.

That block is now mechanical rather than advisory. `stage-1/human-gate.md` carries four status markers, `REGISTRATION-CONFIRMED`, `ELIGIBILITY-CHECKED`, `ROSTER-CONFIRMED` and `SENDER-CONFIRMED`, and week 5 fails until a human has added all four. An agent never writes them. They are status only and no personal details belong in that file.

The weekly audit is also a gate now. Every week already marked done has to carry `stage-1/audit/week-N.md` containing `AUDIT-COMPLETE`, checked in `check.py` rather than only by the supervisor. The week being gated right now is exempt, since its audit does not exist yet. This matters because the audit is the stated mitigation for everything the gates deliberately do not check: whether the prose says anything, whether a mass basis is real, whether a source is strong enough. That mitigation used to be named in this file and enforced nowhere.

**Set to 1 deliberately, so the loop halts after every week.** Nothing here has run a tick yet, and the first few weeks are worth reading before the next one builds on them. Weeks 2 and 4 also carry decision gates that are judgment calls rather than mechanical ones, so full autopilot to the deadline was never the right trade on a submission that only gets made once. Raise it to 2 once a couple of weeks have come back clean and the shape of the output is known.

## Blocked triggers

Stop the week and report BLOCKED, with unblock steps, on any of these. Do not work around them.

- **Sending anything to the organisers.** The Stage 1 submission email, or any other mail to pushpak_gc2026@aero.iitb.ac.in, is a human action. Draft it, stage it, never send it. This holds even in week 5 when the plan says "submit"
- **Registering the team** on techfest.org, or entering anyone's personal details
- **Naming real people, institutions or capabilities** in the team capability section. Week 5 writes the structure and leaves the specifics for the human, because inventing a team is fabrication
- **The mass budget will not close** after the week 4 fallback has been tried, meaning the second radius carried out of week 2 also fails T/W. That is a design finding and needs a human decision, not a fudged line
- **A thrust to weight case that is not the stacked one fails 2.5.** The design case, the mass downside alone and the coefficient downside alone are each hard gates in week 2. If any of the three fails, geometry does not freeze. Work the fallbacks in the plan first, in order; if none closes, stop and report rather than trimming an assumption until the number appears. The stacked case is no longer a week 2 blocker: it is stated, and a miss has to hand week 4 a computed mass target. See D30
- **The human gate markers are missing when week 5 starts**, including `TECHNICAL-READ-COMPLETE`, which a person adds only after opening the built PDF and reading it end to end
- **The refined week 4 budget leaves the stacked conservative case under 2.5.** This is where the hard stacked test now lives, on real sections and catalogue parts rather than assumed ones. Week 4 works its own fallbacks first. If the refined budget still misses, stop and report. See D30, which moved this gate out of week 2
- **A paper that is a hard dependency for the week.** Stop and report. A paper that is only supporting evidence is not a blocker: record the gap, carry on with what is available, and state the limitation in the progress file. Today the three unread papers are supporting evidence, not hard dependencies, so week 2 runs

## Rules digest

From the global CLAUDE.md, and binding on every week-agent:

- No em dash or en dash in any prose written to a file. Comma, semicolon, "and", or a new sentence. Plain hyphen for ranges. The `--global` gate enforces this
- Invoke the `humanizer` skill before writing prose to any file. It owns tone and the AI-detection patterns
- Commit at the end of the week. Split substantial work into 3 or more commits by concern. Invoke the `git-commits` skill for the procedure
- Never push, amend, force, branch, tag, open a PR, or rewrite history
- Never add a Co-Authored-By line, an AI or model trailer, or a "generated by" line. The `--global` gate greps for these
- No emoji anywhere

Project specific:

- **Week 2 has four feasibility gates a week-agent will otherwise trip blind.** Aerodynamic power must clear the momentum bound over a declared area no larger than 2R times span, with a figure of merit between 0.20 and 0.75, and Kellen measured 0.6 at UAV scale. A second power estimate from published power loading has to agree within 35 percent. A `thrust_sensitivity` table of 3 or more rows must reproduce each row's mass ceiling and ideal power and contain the chosen design thrust. Solidity must sit inside 0.30 to 0.40, which is the band Kellen measured the shape family in, and the low thrust coefficient has to answer a stated blade deflection loss rather than a comfortable percentage
- **Week 4 sizes the blade against centrifugal load, not only aerodynamic load.** Centrifugal beat aerodynamic by 4.4 times in Runco's measurements, so the blade attachment carries its own margin against the recomputed centrifugal force, and the aerodynamic peak to mean factor is at least 4.0. Every budget line names the envelope line it `refines`, and each component group stays within 25 percent of it
- `stage-1/design/numbers.json` is the only place a number is defined. Prose cites it through a `## Numbers used` block listing `dotted.key = value`, and the gate checks each one. Never restate a number from memory
- The submission gets a further audit: every number in its narrative carrying a physical unit has to match a computed value **in the same dimension**, so 400 N does not pass because 400 happens to be a millimetre dimension. Quoted blocks are exempt. Tables are not, unless an `<!-- allow-table: reason -->` marker sits on the line above, which is for reproducing other people's published data. The reason is mandatory. The ceiling counts numbers rather than markers: across the whole document, at most 4 dimensioned numbers may sit inside an exempt region without tracing to `numbers.json`. A number that does trace costs nothing, so quoting the problem statement is free
- Every `mass_budget_g` line in week 4 carries a `refines` field naming the week 2 `mass_envelope_g` line it came from, spelled the same way. The gate groups the budget by that field and checks each envelope line survives the refinement within 25 percent
- `context.md` outranks every other document on what the competition requires. If a week's work seems to conflict with the plan, check context.md before deciding the plan is right
- No CAD at Stage 1. It is not asked for and it is not scored until Stage 2
- Do not reopen a frozen decision silently. Reopening is a numbered entry in the decisions file with the reason

## Codemap

This repo is documents, not code, so codemap entries describe what each file is for and what depends on it. Keep entries short. Skip the PDFs and the JSON dumps under `reference/`, which are downloaded source material and do not change.
