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
to what it recomputed. Week 3 added `check_vector_map`, `check_lateral_loads` and the `snum`
reader for signed values, and week 2 added `check_week2_selection`, `measured_shape_family`,
`check_conservative_budget` and `states_value` over `WEEK2_DOCS`. Week 4 added
`budget_conservative_total`, two combined blade margins, an overspeed attachment margin, a
recomputed centrifugal bending term, `MIN_OVERSPEED`, a 25 percent band on the conservative
budget and a floor on `shaft_combined_margin`. Week 5 added `front_matter_lines` and nothing
else.
Used by: the supervisor after every week tick, and tools/test_gates.py
Gotcha: hard limits never touch stored headline values. `num` returns None for zero and for
negatives, so any signed quantity has to go through `snum` or half the table vanishes silently.
Two gates are conditional on a result rather than fixed: the week 4 mass target, and the
coefficient floor, which drops from 10 percent to 5 only for a scenario classed measured on this
design's own solidity and chord to radius. `budget_conservative_total` is a third: while
`mass_budget_g` has 8 or more complete lines, `results.mass_g_conservative` is checked against
the budget, and against the week 2 envelope only before that. See D47. `blade_margin` is
aerodynamic bending alone and is deliberately not the gating one, because centrifugal bending is
9.2 times larger here; `blade_combined_margin` and the two overspeed margins are.
`shaft_combined_margin` is the one margin it floors without recomputing, because that needs shaft
section properties which live in tools/structure.py. It does not recompute the four-bar;
test_gates does. `check_numeric_coverage` skips a delimited YAML block at the top of a file and
nothing else: the skip is positional, so `margin=25mm` in the body still fails, and an opening
`---` with no closing one counts as no front matter so a stray rule cannot hide a document. See
D54.


### tools/test_gates.py
Self-tests for check.py. Builds throwaway trees and checks an honest design passes while
specific attacks fail, then runs `linkage_selftests` read-only over the real numbers.json. 128
checks, and that total is `len(ANNOUNCED)`, counted at the one print prefix every self-test line
goes out through, not kept beside the loops. Week 2 took it from 77, week 3 from 104, week 4
from 117, and week 5 from 124 with the front matter cases.
Used by: run by hand after any change to check.py, linkage.py or structure.py
Gotcha: `honest_numbers()` is the fixture every case mutates, so a new required field in
check.py has to be added there first or every case fails at once. That is exactly how week 4
broke 4 cases. Its blade allowable is derived from the combined overspeed case, not from
aerodynamic bending, so the combined margins clear their floor the way the real design's do. Its
vector_map spans 300 degrees on purpose, because the week 3 evidence gate rejects commands
clustered near zero. `_rescale_mass` moves the budget's conservative column with the envelope's
by default, since D47 binds the stated scalar to whichever list is live;
`chosen_conservative_mass` passes `scale_budget=False` because it wants them to disagree. Two
things read the real repository: `linkage_selftests`, which reads numbers.json and never writes,
and `REAL_PDF`, which copies the problem statement into throwaway trees. `linkage_selftests`
returns an empty list on a tree from before week 3 so the suite still runs there.


### stage-1/design/numbers.json
Single definition point for every number the submission states.
Holds: geometry, operating point, performance and power chain, efficiency chain, power by
radius, the candidate and scenario tables, azimuthal loads, mass envelope, sources, thrust
sensitivity, and since week 3 the pitch block, linkage_dimensions, pitch_schedule, vector_map
and packaging. Week 4 filled structure, mass_budget_g at 33 lines, bom at 25 lines and the
remaining results including the four bom totals.
Used by: every stage-1/design/*.md through its Numbers used block, tools/check.py,
tools/linkage.py, tools/structure.py
Gotcha: prose never restates a number, it cites the dotted key. The pitch, schedule, vector map,
linkage, packaging and azimuthal blocks are written wholesale by `tools/linkage.py --write`, and
structure, mass_budget_g, bom and the results block by `tools/structure.py --write`, so a
hand-added key inside any of them is deleted by the next run. Only `pitch_schedule` is protected
against hand editing, by the loop closure test in test_gates.py. `aero_azimuthal_loads` rows
carry `lateral_force_N` since week 3 and both its cycle mean and its peak are gated. Every
mass_envelope_g line carries a scaling_class; mass_budget_g rows carry conservative_g and
`refines`. bom rows carry `priced_date`, not quote_date, because nothing was quoted, and no bom
field name ends in a unit suffix, so the week 5 coverage gate does not read a rupee figure as a
force. See D33, D41, D47 and D52.


### stage-1/design/evidence-ledger.md
Week 2 deliverable. 19 numbered evidence rows with class, source, exact basis, area convention,
source geometry, source Reynolds and use, followed by the selection rules and the packaging
assumption, all fixed before any candidate was scored. The freeze rule it published sits next
to the D30 rule that replaced it rather than being edited in place.
Used by: the three week 2 design documents, and the week 2 audit
Gotcha: the gate checks only that the two headings exist, so the honesty of the classes is
an audit matter. Four rows are class measured since 31 August, all of them Kellen's
measurements on Kellen's rotor, which is this design's shape family to within 1.1 percent and
not this design. E1, the coefficient the design is built on, is still not one of them. E7 is a
real measurement on somebody else's rotor and stays transferred for that reason.

### stage-1/design/01-configuration.md
Required Stage 1 item 1. The frozen single rotor against redesigned 2 and 3 rotor clusters on one
common model, the stated packaging rule, the cluster mass build-up, and the blade count, airfoil
and drive topology choices.
Used by: week 3 packaging and the week 5 submission
Gotcha: needs the headings Configuration, Why this configuration and Numbers used, at least 400
words of body, and 3 or more distinct declared numbers matching numbers.json to 2 percent. D32
also requires the stacked figure wherever it states the 3.163 design case, and `states_value`
ignores the Numbers used block. That figure is 2.5457 since week 4 refined the budget, not the
2.517 week 2 wrote. Its packaging rule uses 2R and understates the module, which D44 corrects
without reopening the comparison.


### stage-1/design/02-rotor-sizing.md
Required Stage 1 item 2. Shape family, the coefficient recompute, blade section and stiffness
closure, the radius sweep, the mass envelope, and the four case verdict that freezes geometry.
Since D35 all four cases clear 2.5 and the week 4 mass target is gone.
Used by: week 4's mass budget, which refines every mass_envelope_g line by name
Gotcha: needs the headings Rotor sizing, Shape family, Radius and Numbers used. The mass
envelope line names here are what week 4's `refines` fields have to match, spelled the same way.
Its blade section figures are week 4's rebuild and its blade build-up paragraph keeps the week 2
estimate beside them, on purpose; the stiffness closure now rests on torsional wind up rather
than on bending, per D50. The four case table mixes columns since D47: nominal from the week 2
envelope, conservative from the refined budget, and it says so under the table.

### stage-1/design/04-thrust-and-power.md
Required Stage 1 item 4. Thrust from the coefficient route, the 36 point azimuthal load
distribution, power closed by momentum floor then figure of merit then published power loading,
the drive on a derated continuous rating, and the frozen thrust sensitivity table.
Used by: week 4's structural loads, and tools/linkage.py reconstructs its load model from the
prose in the Azimuthal load distribution section
Gotcha: needs the headings Thrust, Power, Sensitivity and Numbers used. Week 4 may select a row
from the sensitivity table and may not invent a new design thrust; it selected none and kept 18
N. The azimuthal section was rewritten in week 3 against the solved schedule, so it now tabulates
the full revolution and carries a lateral column. One load model lives here, not two. Its radius
sweep column still reads 2.517 for the chosen row, because the sweep is built on the week 2
envelope applied to all five radii, and the text says why. See D41 and D47.


### stage-1/progress/week-2.md
Week 2 progress record across both runs: what was produced, the four T/W cases, the fallbacks
that were worked, 14 debts and what week 3 inherits.
Used by: check.py counts a week as done only if this file carries STATUS: WEEK-COMPLETE
Gotcha: it carries that marker as of the second run. Debt 1 is the 68.5 g mass target and debt
12 is week 4 restating the stacked figure in the three design documents when the mass moves.
Dates in first-run prose read 2 September; the commits say 30 August.

### stage-1/decisions.md
Numbered append-only decision log, D1 to D58. Reopening an earlier entry means a new entry saying
which one it supersedes.
Used by: every week agent as settled ground
Gotcha: D27 supersedes figures in D18, D20, D21 and D22, and D30 supersedes the freeze rule in
D17. D30 is the entry to read before touching week 2 or any mass work. D35 to D37 are the
evidence pass. D38 to D44 are week 3: D40 constrains the shaft, D41 supersedes week 2's azimuthal
table, D42 records the gate change, and D43 hands week 4 a mass trade. D46 to D53 are week 4:
D46 closes D43 against balancing, D47 moves the conservative mass onto the refined budget and is
the one to read before touching a mass number, D48 retires the duplicated blade constant, D49
declares the overspeed case, D50 keeps the 5 percent allowance while giving it a calculation, D51
records the gate change and D52 says the BOM is priced and not quoted. D53 is the audit response
and it corrects the balanced pitch link figures inside D46 and withdraws one sentence of D51.
D54 to D58 are the week 5 preparation pass: D54 records the front matter gate fix, D55 sets the
P-1 to P-9 placeholder scheme, D56 is why the submission carries 33 budget lines instead of group
totals, D57 is the page target, and D58 says the pass prepared week 5 and did not run it.


### stage-1/journal.md
Short narrative note per working session, newest last. Eight entries, the last one being the week
5 preparation pass.
Used by: nothing mechanical, it is the record of what actually happened
Gotcha: no gate reads it, so it is the one place that can say a model was wrong the first time.


### handoff.md
Where a fresh session starts. Current state, the frozen geometry and mechanism, the eight
structural margins, what the preparation pass changed, what is left of week 5, the ordered human
list and open items.
Used by: check.py greps it for the NEXT-WEEK marker, which is the external witness for how many
weeks are finished
Gotcha: exactly one NEXT-WEEK line and it still reads 5, because the preparation pass did not
complete week 5 and must not read as if it had. Two markers fail the gate, so the number never
appears twice at the start of a line. Its four-case T/W table is the one a reader meets first, so
it moves whenever the coefficient or the mass does, and week 4 moved the mass.


### tools/linkage.py
Week 3 solver. Closes the four-bar per blade, bisects the offset length for the frozen pitch
amplitude, reruns the week 2 azimuthal load model on the solved schedule with a self-consistent
inflow, sizes the vectoring actuator and computes the swept envelope. `--sweep` prints the horn
and pitch link table the design point came from, `--balanced` shows the chordwise balance case.
Used by: run by hand; `--write` is what fills the pitch, schedule, vector map, azimuthal load and
packaging blocks of numbers.json, and tools/test_gates.py imports nothing from it
Gotcha: `--write` refuses the balanced case, because that blade does not exist yet, and writes
LF because the default here is CRLF against a repo that declares eol=lf. It reconstructs week 2's
load model first, against the `WEEK2_PUBLISHED_LOADS` constant and never against the live table,
because `--write` replaces that table and an earlier version compared the reconstruction with its
own output. `BLADE_PARTS_G` is gone since week 4: the blade build-up is imported from
tools/structure.py, so run this script first and structure.py second whenever the blade section
moves. `check_solver_order` in check.py enforces that now, by reading whether the pitch link load
this script solved is the one structure.py stored. See D48 and D62.

### stage-1/design/03-pitch-and-vectoring.md
Required Stage 1 item 3 and the whole 15 percent kinematics and vectoring criterion. Topology,
loop closure, link table, Grashof and transmission angle, the 37 row solved schedule, the phase
authority arithmetic, the force vector map and the side force argument.
Used by: the week 5 submission, and week 4 for the pitch link and blade balance loads
Gotcha: needs the headings Pitch mechanism, Kinematics, Pitch schedule, Thrust vectoring, Side
force and Numbers used, and 500 words of body. The Pitch schedule section must hold exactly one
markdown table: check.py parses every pipe row in it as schedule data. Its mechanism loads moved
about 1 percent in week 4 when the blade stopped being an estimate, and three of its open items
are answered rather than handed forward. See D48.

### stage-1/design/09-packaging-and-integration.md
Week 3 deliverable, the integration half of the 5 percent packaging criterion. Swept envelope,
the module dimensions as a sum of named parts, the mount and reaction torque path, the
drivetrain layout and both interface tables.
Used by: the week 5 submission
Gotcha: needs the headings Package envelope, Mounting, Drivetrain, Interfaces and Numbers used,
and 300 words. Its swept diameter of 296.1 mm is what D44 says the week 2 packaging rule missed.

### stage-1/submission/cycloprop-stage1.md
The submission source, rebuilt in the week 5 preparation pass from the reviewed design documents.
A pandoc front matter block, an identity table carrying three placeholders, a summary, the seven
required items as top-level headings, the 8 row criteria map, a claims and risk table, a
provenance section, appendix A of 12 examiner questions and appendix B with the Numbers used
block. 99 declared numbers.
Used by: pandoc, and check.py at week 5 for headings, criteria rows, substance and numeric coverage
Gotcha: the heading text has to keep matching REQUIRED_ITEMS in check.py word for word, and
`## Numbers used` needs two hashes or `check_declared_numbers` does not find it. The criteria map
must stay the first heading containing "criteri" and its table must sit directly under it, because
`section_under` stops at the next heading. Its mass table is the 33 stored budget lines rather
than group totals: group sums exist in no file and eight of them passed the coverage audit only by
landing within 2 percent of an unrelated stored mass. See D56. One allow comment is used in the
whole document, on published side force angles, and it hides 3 of the 4 numbers the ceiling
permits. `[P-1]`, `[P-2]` and `[P-7]` in the identity table are for a person.

### stage-1/submission/cycloprop-stage1.pdf
The built PDF, committed because check.py reads it at week 5 and the attachment is what gets
evaluated. 21 pages: 1 of title and contents, 15 of body through the sources section, then the two
appendices.
Used by: check.py at week 5, which reads it with pypdf and looks for this submission's own strings
Gotcha: rebuild it whenever the source changes, with
`pandoc stage-1/submission/cycloprop-stage1.md --from=markdown --pdf-engine=xelatex --toc
--number-sections -o stage-1/submission/cycloprop-stage1.pdf`. A stale PDF passes the page count
and fails the string check. Two extraction traps were found reading it back and both are handled
in check.py now rather than at each call site: pypdf returns one ff ligature character wherever
the text says "off", which `pdf_text` expands, and the contents entry extracts as "T eam
capability" from kerning while the body heading extracts cleanly, which `check_pdf` survives by
comparing with the whitespace taken out. `pdf_selftests` in tools/test_gates.py reads the real
file back and holds both. Check the xelatex log for overfull lines after any edit; a long
unbreakable token such as the organiser address beside a code span caused the two that were
fixed.

### stage-1/submission/email-draft.md
The staged submission email. Drafted, never sent, per D5. Carries the recipient, a subject line,
the attachment name, the three team placeholders, the registration reference placeholder and a six
step list of what a person does before pressing send.
Used by: check.py at week 5, which requires the file and greps it for the attachment name, the
organiser address, the word attachment and a subject line
Gotcha: the registration reference is `[REGISTRATION REFERENCE]` in both the subject and the body
and it is also `[P-7]`. The two live organiser questions from stage-1/organiser-email.md moved
here, framed so they need no reply.

### stage-1/design/07-team-and-execution.md
Required Stage 1 item 7, written in the week 5 preparation pass. Nine placeholders tagged `[P-1]`
to `[P-9]` in one table at the top, the roster section, the capability table against the problem
statement's seven preference areas, four stated gaps, the Stage 2 schedule across all 11 required
items with a closing gate each, the Stage 2 gates and the route through the missing capability.
Used by: the week 5 submission, which condenses it into item 7
Gotcha: needs the headings Team capability, Execution plan and Stage 2, though the title alone
satisfies two of the three, so the real constraint is D5 rather than the gate: no name,
institution, qualification, tool licence or capability claim about a person may be written here.
Claims in the file are about the Stage 1 work, which is checkable. Four of the nine placeholders
are also week H markers and the table says which. See D55.

### tools/structure.py
Week 4 solver. Integrates the NACA 0020 section from its ordinate polynomial, builds the blade
from foam, skin, spar and root fittings, sizes the shaft, the pitch load path, the attachment and
the frame, computes all 8 margins, and builds the 33 line mass budget and the 25 line BOM.
`--write` puts structure, mass_budget_g, bom and the results block into numbers.json, `--bom`
prints the costed table and `--balance` prices the chordwise balance D43 left open.
Used by: run by hand; tools/linkage.py imports `blade_parts_g` from it for the pitch loads
Gotcha: geometry, speed and thrust are read back out of numbers.json and no week 4 number is
ever read back in, so a rerun cannot confirm its own output. Run tools/linkage.py --write first
when the blade section moves, then this, which reads the pitch link load back. The wrong order
leaves structure.pitch_link_load_N holding the value from before the blade moved while
pitch.peak_link_force_N carries the new one, and `check_solver_order` reads that gap. From an
already converged file both orders reproduce it byte for byte, which is why reproducibility alone
is not the test. It writes with `newline="\n"` and `ensure_ascii=False` to match linkage.py, and it
must: it writes the same file second, so the platform default here put CRLF back into a file
linkage.py had just written LF and git normalised the evidence away. `--balance` calls
`linkage.solve` through a deferred import, because linkage imports this module at load time, and
because the ratio it used to scale by went stale the moment the blade changed. `MATERIALS` at the top is the only place a material allowable is defined and
06-materials-and-manufacturing.md cites it rather than restating it. Budget line names carry the
word "blade" only when they are blade mass, because check.py derives per-blade mass by summing
every line whose item name contains it, so "pitch bearings" may not become "blade pitch
bearings". BOM prices are indicative, which is why the field is `priced_date`. See D52.

### stage-1/design/05-mass-and-tw.md
Required Stage 1 item 5. The 33 line refined budget with its growth classes, the per group
continuity table against the week 2 envelope with a reason for every group over 10 percent, the
four thrust to weight cases, the 2.75 gap and the balance trade that was declined.
Used by: the week 5 submission, and 02-rotor-sizing.md points at it for the refined budget
Gotcha: needs the headings Mass budget, Thrust-to-weight, Margin and Numbers used, and 400 words.
Its budget table is a copy of `mass_budget_g` for a human reader; the gate reads the JSON, so a
hand edit here changes nothing and is a lie by the next run of tools/structure.py.

### stage-1/design/06-materials-and-manufacturing.md
Required Stage 1 item 6 and the manufacturing half of the 10 percent cost criterion. Six load
carrying materials each tied to the margin it decides, a per part process and tolerance table,
the assembly order, the 6 pre-spin measurements, the costed BOM and the mass reserve.
Used by: the week 5 submission
Gotcha: needs the headings Material selection, Manufacturing, Cost and Numbers used, and 400
words. The material properties are quoted from `MATERIALS` in tools/structure.py and are not in
numbers.json, which is deliberate: they are inputs to the calculation rather than results of it,
and 08-structure-and-loads.md does the same. Its cost table states in bold that the prices are
indicative and not quotations, and that sentence is load bearing. See D52.

### stage-1/design/08-structure-and-loads.md
The 15 percent structural criterion, which had no section before week 4. Two load cases,
operating and a declared 1.20 overspeed, the blade section and its three demands, the shaft and
its combined case, the pitch load path with the element that governs it, the frame and mount
path, all 8 margins and the analyses Stage 2 owes.
Used by: the week 5 submission, and 06-materials-and-manufacturing.md works backwards from its
margins to the properties they rest on
Gotcha: needs the headings Load cases, Blade, Shaft, Margins and Numbers used, and 400 words. It
declares 35 numbers, the largest block in the repository, and every one is recomputed by the gate
or derived by tools/structure.py. The offset post, the mount lug and the second moment figures in
its prose are worked in the document and are not in numbers.json, so the week 5 coverage gate
will not trace them if they are copied into the submission verbatim.

### stage-1/progress/week-4.md
Week 4 progress record: the 7 tasks, the structural results, the refined budget, what the
recovery corrected, 10 debts and the 7 week 3 debts this week retired.
Used by: check.py counts a week as done only if this file carries STATUS: WEEK-COMPLETE
Gotcha: it carries that marker, which is why check.py then demands stage-1/audit/week-4.md. It is
the only file that records the API failure the week was interrupted by, alongside the journal.

### stage-1/audit/week-4.md
The week 4 audit: one fresh-context read-only pass, verbatim, followed by what was done about
each finding.
Used by: check.py at every later week, which requires an audit file with its marker for each week
already marked done
Gotcha: must contain the literal line AUDIT-COMPLETE and end with the "Findings: N" line, which
is grepped. Findings are reproduced word for word rather than summarised.

### stage-1/progress/week-3.md
Week 3 progress record: the eight tasks, the solved mechanism, the load model rerun, the PDF
command and its readback, 9 debts and what week 4 inherits.
Used by: check.py counts a week as done only if this file carries STATUS: WEEK-COMPLETE
Gotcha: it carries that marker, which is why check.py then demands stage-1/audit/week-3.md.


### stage-1/audit/week-3.md
The week 3 audit: one fresh-context read-only pass, 16 findings, verbatim, followed by what was
done about each.
Used by: check.py at every later week, which requires an audit file with its marker for each week
already marked done
Gotcha: must contain the literal line AUDIT-COMPLETE and end with the "Findings: N" line, which
is grepped. The findings are reproduced word for word rather than summarised, so the corrections
they triggered live in D45 and in the response section below them.

### reference/
Primary sources. The problem statement PDF and its text, the API payload it came from, and the
machine text extracts of Kellen 2019 and Benedict 2010 with a README giving the handle, the
Wayback URL that worked, a curl line and the sha256 of each PDF.
Used by: context.md is built from the problem statement; the evidence ledger cites the two
theses by printed page
Gotcha: the two thesis PDFs are deliberately not committed, 52 MB against a repository of
about 2.2 MB, so the extracts plus a hash stand in for them. `check.py` skips this whole
directory in the style and ASCII gates, because the extracts are somebody else's words and
rewriting incoming evidence to match our own house style would damage it.

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
Gotcha: it describes the four case thrust to weight split and the D33 rebuild since the tick that
opened week 3. A non-stacked case under 2.5 stops week 2; the stacked case stops week 4 instead,
on the refined budget. It belongs to a person, so a week agent reports rather than edits.


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
Gotcha: it named the Codex config as the contract until D28 reversed that, and its week 2
decision gate is the pre-D30 rule with a supersession note under it. The week 2 "Done when"
list is stale in the same way and check.py is what governs.

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
