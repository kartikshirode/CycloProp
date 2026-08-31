# Codemap

File level index for CycloProp Stage 1. This repository is documents rather than code, so
entries say what each file is for and what depends on it. Started in week 2, so it is
incomplete on purpose: it covers the gate scripts, the plan and the loop configs, and
everything week 2 touched, and it grows one week at a time. A file with no entry here has
simply not been touched since the map started.

## How the repository is shaped

Requirements come from the official problem statement PDF under `reference/`, distilled into
`context.md`, which outranks every other document on what the competition wants.
`stage-1/plan.md` says what happens in which week. `stage-1/design/numbers.json` is the single
place a number is defined; design documents cite it through a `## Numbers used` block and
`tools/check.py` recomputes the physics from the stored geometry rather than trusting the
stored headline. A week is gated by `python tools/check.py --week N`, which is cumulative, and
by `--global` for style and attribution across every markdown file we wrote.

Four artifacts end every week: the progress file, the audit file, the handoff with its
NEXT-WEEK marker bumped, and a numbered entry in decisions plus a note in the journal. The
audit is itself a gate, because it is the stated mitigation for everything the mechanical
gates deliberately cannot check.

## Entries

### tools/check.py
The gate script. Recomputes tip speed, Reynolds, thrust, power chain, mass totals, thrust to
weight and structural demands from stored geometry and mass lines, then applies the hard limits
to what it recomputed. Week 2 added `check_week2_selection`, split the one stacked T/W gate into
six including the conditional `results.mass_target_week4_g` pair, and added `states_value` over
`WEEK2_DOCS` for D32.
Used by: the supervisor after every week tick, and tools/test_gates.py
Gotcha: hard limits never touch stored headline values, and the mass target gate is the only
one whose requirement depends on a result: it asks for nothing when the stacked case clears 2.5
and recomputes the target when it misses. Week 2's momentum floor is the one gate that asks
whether the design could physically exist rather than whether it agrees with itself.

### tools/test_gates.py
Self-tests for check.py. Builds throwaway trees and checks an honest design passes while
specific attacks fail. 98 checks after week 2 added 12, then 7, then 3.
Used by: run by hand after any change to check.py
Gotcha: `honest_numbers()` is the fixture every case mutates, so a new required field in
check.py has to be added there first or every case fails at once. `_rescale_mass` moves the
envelope, the stated totals and every candidate row together, because one T/W case cannot be
moved on its own without tripping a gate the test was not aiming at.

### stage-1/design/numbers.json
Single definition point for every number the submission states.
Holds: geometry, operating point, performance and power chain, efficiency chain, power by
radius, configuration candidates, coefficient scenarios, azimuthal loads, drive candidates,
mass envelope, sources, thrust sensitivity, and the two conservative results. Week 3 fills
pitch, linkage, schedule, vector map and packaging; week 4 fills structure, the mass budget
and the three remaining results, which are still null.
Used by: every stage-1/design/*.md through its Numbers used block, tools/check.py
Gotcha: prose never restates a number, it cites the dotted key. Every mass_envelope_g line
carries a scaling_class of geometry, power or fixed, because the drive is not a fixed mass.
`results.mass_target_week4_g` exists only because the stacked case misses 2.5, and the gate
recomputes it rather than trusting it.

### stage-1/design/evidence-ledger.md
Week 2 deliverable. 16 numbered evidence rows with class, source, exact basis, area convention,
source geometry, source Reynolds and use, followed by the selection rules and the packaging
assumption, all fixed before any candidate was scored. The freeze rule it published sits next
to the D30 rule that replaced it rather than being edited in place.
Used by: the three week 2 design documents, and the week 2 audit
Gotcha: the gate checks only that the two headings exist, so the honesty of the classes is
an audit matter. Nothing here is class measured; E7 is a real measurement on somebody else's
rotor and is labelled transferred for that reason.

### stage-1/design/01-configuration.md
Required Stage 1 item 1. The frozen single rotor against redesigned 2 and 3 rotor clusters on
one common model, the stated packaging rule, the cluster mass build-up, and the blade count,
airfoil and drive topology choices.
Used by: week 3 packaging and the week 5 submission
Gotcha: needs the headings Configuration, Why this configuration and Numbers used, at least 400
words of body, and 3 or more distinct declared numbers matching numbers.json to 2 percent. D32
also requires the stacked 2.252 wherever it states the 3.163 design case.

### stage-1/design/02-rotor-sizing.md
Required Stage 1 item 2. Shape family, the coefficient recompute, blade section and stiffness
closure, the radius sweep, the mass envelope, and the four case verdict that freezes geometry
and states the 623.9 g week 4 mass target.
Used by: week 4's mass budget, which refines every mass_envelope_g line by name
Gotcha: needs the headings Rotor sizing, Shape family, Radius and Numbers used. The mass
envelope line names here are what week 4's `refines` fields have to match, spelled the same
way.

### stage-1/design/04-thrust-and-power.md
Required Stage 1 item 4. Thrust from the coefficient route, the 36 point azimuthal load
distribution, power closed by momentum floor then figure of merit then published power
loading, the drive on a derated continuous rating, and the frozen thrust sensitivity table.
Used by: week 3's rerun of the load model against the solved schedule, week 4's structural loads
Gotcha: needs the headings Thrust, Power, Sensitivity and Numbers used. Week 4 may select a row
from the sensitivity table and may not invent a new design thrust. The azimuthal distribution
here has zero side force by construction, so week 3 reruns it rather than citing it.

### stage-1/progress/week-2.md
Week 2 progress record across both runs: what was produced, the four T/W cases, the fallbacks
that were worked, the debts and what week 3 inherits.
Used by: check.py counts a week as done only if this file carries STATUS: WEEK-COMPLETE
Gotcha: it carries that marker as of the second run. Debt 1 is the 68.5 g mass target and week
4 owns it.

### stage-1/decisions.md
Numbered append-only decision log, D1 to D32. Reopening an earlier entry means a new entry
saying which one it supersedes.
Used by: every week agent as settled ground
Gotcha: D27 supersedes the figures in D18, D20, D21 and D22, and D30 supersedes the freeze rule
in D17 and answers D22. D30 is the entry to read before touching week 2 or any week 4 mass
work, because it is where the hard stacked T/W test moved to.

### stage-1/journal.md
Short narrative note per working session, newest last. Four entries, the last one being the
week 2 freeze.
Used by: nothing mechanical, it is the record of what actually happened
Gotcha: no gate reads it, so it is the one place that can say a model was wrong the first time.

### handoff.md
Where a fresh session starts. Current state, the frozen geometry, what week 3 inherits, the
human list and open items.
Used by: check.py greps it for the NEXT-WEEK marker, which is the external witness for how
many weeks are finished
Gotcha: exactly one NEXT-WEEK line and it now reads 3. Two markers fail the gate, so the number
never appears twice at the start of a line.

### stage-1/human-gate.md
Week H task list and its five status markers. Registration, eligibility, roster, sender and
the technical read.
Used by: check.py at week 5, which fails until all five markers are present
Gotcha: an agent never writes a marker. They are status only and no personal details belong in
the file.

### .claude/weekly-loop.md
The execution contract for every runner, per D28: paths, gate commands, markers, checkpoints,
blocked triggers and the rules digest.
Used by: the weekly-loop skill and every week agent, and .codex/weekly-loop.md defers to it
Gotcha: the thrust to weight blocked triggers were rewritten for D30. A non-stacked case under
2.5 stops week 2; the stacked case stops week 4 instead, on the refined budget.

### .codex/weekly-loop.md
Runner-specific stub. Says it is not the contract, points at the Claude config, and carries
only its own sentinel path so a dead tick under one runner is not read as partial work by the
other.
Used by: a Codex runner, which takes everything else from the Claude config
Gotcha: it still needs one human confirmation before a Codex tick runs.

### stage-1/plan.md
The week by week execution plan: scope files, tasks, done-when gates and decision gates, one
section per week.
Used by: every week agent as the definition of its week, and by the audit, which checks
delivered work against it
Gotcha: it named the Codex config as the contract until D28 reversed that. Its week 2 decision
gate is the pre-D30 rule, and D30 is what actually governs the freeze.

### stage-1/audit/week-2.md
The week 2 audit: two fresh-context read-only passes, 18 findings from the blocked run and a
second pass over the freeze, both verbatim, each followed by what was done about it.
Used by: check.py at every later week, which requires an audit file with its marker for each
week already marked done
Gotcha: must contain the literal line AUDIT-COMPLETE, and the findings are reproduced word for
word rather than summarised.

### stage-1/literature.md
Week 1's technical input: source table with a status column, geometry and measured
performance, published mass breakdowns re-cut onto the module boundary, and the external
research round.
Used by: the evidence ledger, and week 1's own gate checks two of its headings
Gotcha: superseded in two places by week 2 and annotated in place rather than rewritten. Its
first-cut sizing table is a 10 N design point, not the 18 N one week 2 carries. See D26.
