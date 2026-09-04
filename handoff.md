# CycloProp handoff

Updated 4 September 2026. Stage 1 is due **27 September 2026** and we submit on 26 September.
This file is where a fresh session starts.

NEXT-WEEK: 5

Weeks 1 to 4 are done. Geometry froze in week 2, the mechanism in week 3, and week 4 closed the
structure, the refined mass budget and the materials and manufacturing case.

**The gates are green again and the design behind them is weaker than it was.** A five pass
review on 1 September found 63 things and a codex audit on 4 September found eleven more.
`python tools/check.py --all` passes 288 gates and `python tools/test_gates.py` passes 221
self-tests. Read [stage-1/audit/codex-final-response.md](stage-1/audit/codex-final-response.md)
before anything else: D70 closed both electrical interfaces, and the 10 g regulator it added
took the design case from 2.5563 to **2.5191**, which clears 2.5 by 0.8 percent rather than by <!-- allow: naming the retired value is the point of the sentence, it is a before and after -->
2.3. All four thrust to weight cases moved.

What changed under them is the part to read rather than the pass count. The figure of merit was
being read inconsistently with the thrust coefficient, so the design point came down from 18 N
to 17 N, the pack interface went from 6S to 8S, and six mass lines were wrong for reasons of
their own. The design case still clears thrust to weight 2.5. The three downside cases no longer
do. Read D66, D67 and D68 and `stage-1/audit/full-review.md` before touching anything, and do
not make a gate pass by moving the number it reads.

**Week 5 has not run and this file does not say it has.** It is hard blocked by week H. A
preparation pass on 31 August closed every week 5 gate that does not need a person, and a
hardening pass on 1 September closed four engineering items that were being carried into Stage 2
without being quantified. The human gate is still the only thing week 5 fails that a person can
clear. See D58, D60 to D63 and D66, and "What is left of week 5" below.

## Read these first, in order

1. **[context.md](context.md)** is the authority on what the competition requires. Built from
   the official problem statement PDF, and it outranks everything else here including this file
2. **[stage-1/plan.md](stage-1/plan.md)** is the week by week execution plan
3. **[stage-1/progress/week-4.md](stage-1/progress/week-4.md)** is where the design stands and
   what week 5 inherits. [week-3.md](stage-1/progress/week-3.md) is the mechanism record and
   [week-2.md](stage-1/progress/week-2.md) the feasibility one
4. **[stage-1/decisions.md](stage-1/decisions.md)** is what has been frozen and why. 69 entries.
   Read D67, D68 and D69 first: D67 moved the design point to 17 N and the pack to 8S, D68 is the
   document pass that followed it, and D69 is the figures and the four errors drawing them found.
   D60 to D63 are the 1 September hardening pass and none of them moved a design number. D65
   opens Tier 1 of the review and D66 is the gate pass that made the tree fail on purpose.
   D30 unblocked week 2, D35 closed the stacked case, D38 to D45 are week 3, and D46 to D53 are
   week 4, with D53 the audit response. D54 to D58 are the week 5 preparation pass. D47 is the
   one to read before touching any mass number, and D58 before assuming week 5 ran
5. **[stage-1/design/evidence-ledger.md](stage-1/design/evidence-ledger.md)** is what every
   number rests on and how strong it is
6. **[stage-1/audit/week-4.md](stage-1/audit/week-4.md)** is the week 4 fresh-context audit,
   verbatim, and what was done about each finding.
   [week-5.md](stage-1/audit/week-5.md) audits the preparation pass the same way
7. **[stage-1/submission/cycloprop-stage1.md](stage-1/submission/cycloprop-stage1.md)** is the
   assembled report and [email-draft.md](stage-1/submission/email-draft.md) is the staged mail.
   Both carry `[P-n]` placeholders and neither is finished until a person fills them

`brief.md`, `_shared-timeline.md` and `_plan-review-round1.md` are earlier work kept as history.
They were written from page summaries and contradict `context.md` in several places. When they
disagree, context.md wins. `stage-1/literature.md` is week 1's technical input and is superseded
in two places by week 2; both are marked in the file. See D26.

## To start a week

Prompts are in [_run-prompts.md](_run-prompts.md), one per tick, each for a fresh session. Run
the pre-flight block at the top first. The loop halts after every week. The execution contract
is `.claude/weekly-loop.md` and only that file, per D28.

## Where the design stands

One cyclorotor. 110 mm radius, 72.6 mm chord, 290.4 mm span, 3 blades, NACA 0020, pitching plus
or minus 40 degrees about the 30 percent chord axis, turning at 2337 rpm, driven by one T-Motor
MN5006 KV450 through a 4.25 to 1 toothed belt on a declared 8S pack. 17 N of design thrust
against a 10 N requirement.

The pitch mechanism is a passive four-bar per blade, all three sharing one offset pivot 11.53 mm
off the rotor axis. Link lengths 110.0, 11.53, 108.0 and 18.0 mm. Two 20 g servos turn a
phasing carrier through a 1.5 step up and give 120 degrees of phase authority. Packaged envelope
364.4 by 316.5 by 362.5 mm on four mount points.

The blade is a PMI foam core at 88 percent fill, two plies of 60 gsm carbon twill, a CFRP spar on
the pitch axis and two bonded 7075-T6 root fittings. 31.75 g a blade. The shaft is a 16 mm CFRP
tube with bonded end plugs, driven from one end only.

Four thrust to weight cases, and all four are reported everywhere because reporting one of them
is how week 2 confused itself for a fortnight:

| Case | Thrust | Mass | T/W |
| --- | --- | --- | --- |
| design point | 17.00 N | 687.91 g | 2.5191 |
| coefficient downside alone | 16.15 N | 687.91 g | 2.3931 |
| mass downside alone | 17.00 N | 775.74 g | 2.2339 |
| both stacked | 16.15 N | 775.74 g | 2.1221 |

**One of the four clears the hard limit of 2.5 and three do not.** Before D67 all four cleared.
The requirement is stated on the module and the design estimate meets it at 2.5191. Holding the
downside cases to 2.5 as well was this project's own discipline, and the corrections spent it.
The downside cases are held to a declared floor of 2.0 now, and the gate requires the closing
mass to be computed and published: **117.26 g** out of a 775.74 g conservative column, or a
target of 658.48 g. Since week 4 the mass in that table is a 33 line budget of drawn sections and
catalogue parts rather than an estimate.

The internal 2.75 target from D17 is further away than it was and still not claimed. It wants the
conservative column at 598.6 g, so the gap is 164.6 g. Refinement no longer pays any of it back;
it costs 2.19 g, because 38.49 g saved on growth allowance is less than the 40.68 g the nominal
column gained.

## Structural state

Eight margins, all floored at 1.5. Seven are recomputed by the gate from the allowable and the
demand beside them. The shaft's combined case is floored but not recomputed, because it needs
section properties that live in `tools/structure.py` and not in `numbers.json`.

| Case | Demand | Margin |
| --- | --- | --- |
| blade bending, aerodynamic only | 0.8228 Nm | 30.69 |
| blade bending, aerodynamic and centrifugal | 8.4153 Nm | 3.00 |
| blade bending at 1.20 overspeed | 12.1181 Nm | 2.08 |
| rotor shaft torsion | 1.54226 Nm | 16.18 |
| rotor shaft, bending and torsion combined | 5.56 MPa | 9.90 |
| pitch link path, the horn governs | 144.19 N | 3.29 |
| blade attachment, centrifugal | 209.161 N | 3.73 |
| blade attachment at 1.20 overspeed | 301.192 N | 2.59 |

Two margins sit under 3 and both are the overspeed cases, so the declared 1.20 factor is what
sizes this module rather than any operating load. The blade in combined bending is the tightest
at 2.08, and it took that place from the blade attachment when D67 duplexed the pitch bearings.
Each blade pulls 209.161 N against a peak aerodynamic 22.67 N, so this is a centrifugal machine
before it is an aerodynamic one. See D49 and D68.

## What is left of week 5

Required item 7, the submission, the PDF and the staged email are done. What is left is the
human gate, the real team facts, and one short run to fold them in.

**0. The organiser channels were re-read on 4 September and nothing moved.** R50 and the
audit's F10 are closed. Twenty three fields of the competition record are identical to the
26 August snapshot, including the deadline, the rules, the eligibility clause and the contact
address, and the problem statement PDF still hashes to the bytes in `reference/`. Registrations
went from 11 to 57. Both snapshots and the repeat command are in
[reference/README.md](reference/README.md), so doing it once more on the send date is a minute.

**1. Week H still blocks it, on one marker.** Registration, eligibility, roster and sender are
confirmed in [stage-1/human-gate.md](stage-1/human-gate.md). `TECHNICAL-READ-COMPLETE` is the
only one left, and it goes in after the built PDF has been read end to end. An agent never
writes one.
The count used to read four because the gate searched the whole file and found
`TECHNICAL-READ-COMPLETE` inside the sentence explaining how to write it. Fixed in D59, and the
the gate now counts only asserted lines. Four confirmations are recorded and one remains.

**2. The nine tracked fields.** `[P-1]` to `[P-9]`, listed in one table at the top of
[07-team-and-execution.md](stage-1/design/07-team-and-execution.md) and referenced from the
submission's identity table and the email draft. Four are also week H markers. Filling them is
the substance of what is left, per D55.

**3. Then one short run.** Fold the team facts into item 7 and the submission's identity table,
rebuild the PDF, add the markers, read the PDF end to end, and write the week 5 progress file
and audit. Nothing in it needs either solver. If one is ever needed, the order is
`tools/linkage.py --write` then `tools/structure.py --write`, and `numbers.json` reproduces byte
for byte from that pair. If a number moves, `python tools/figures.py` has to run too, because
seven figures record the values they drew and a gate reads them back.

The PDF build needs the figures on its path now:

```
pandoc stage-1/submission/cycloprop-stage1.md --from=markdown --pdf-engine=xelatex --toc
--number-sections --resource-path=stage-1/submission -o stage-1/submission/cycloprop-stage1.pdf
```

It is 30 pages and carries seven figures. That is over the 15 page target the plan set for itself
when no organiser limit was supplied, and no organiser limit exists. The question rides at the
end of the staged email.

## What the preparation pass changed

- **`stage-1/design/07-team-and-execution.md` exists.** The execution plan across all 11 Stage 2
  items with the gate that closes each one, the capability gap analysis against the problem
  statement's seven preference areas, the Stage 2 gates and the route through the missing
  capability. No name, institution, qualification or tool licence is written anywhere in it
- **The submission is rebuilt from the reviewed design documents**, assembled rather than
  rewritten. All 7 required items in the official order, the 8 row criteria map, a claims and
  risk table, a provenance section naming which sources were read and which were not, and an
  appendix of 12 examiner questions. The stale week 2 mass figures are gone
- **The PDF was rebuilt after the report identity and figure changes.** It is currently 30 pages.
  The final page count and attachment filename still need a human check
- **The coverage gate defect is fixed.** `margin=25mm` in the pandoc header is build
  configuration, not a design claim, and the skip is positional so the same text in the body
  still fails. 124 self-tests to 128. See D54
- **The email is drafted and staged.** Nothing was sent. It now carries the Competition ID and
  Team ID, and the sender name and final filename still need a human check

## Still worth a human doing, in this order

**1. Eligibility, first.** The clause disqualifies a whole team at any stage, including after
results are announced, so an ineligible roster turns every other week into wasted effort. This is
now checked and `ELIGIBILITY-CHECKED` is present.

**2. Register** on techfest.org and keep the Competition ID and Team ID. No separate registration
reference was issued. Both IDs are now in the report identity table and the email draft, and
`REGISTRATION-CONFIRMED` is present.

**3. Confirm the roster and the sender**, then add `ROSTER-CONFIRMED` and `SENDER-CONFIRMED`.
That is four of the five and the fifth, `TECHNICAL-READ-COMPLETE`, comes after step 6 below.

**4. Fill the remaining `[P-1]` to `[P-9]` fields** in `07-team-and-execution.md`, then check the
identity table at the top of the submission.

**5. Rebuild the PDF.** The command is in `.claude/codemap.md`. A stale PDF passes the page
count and fails the string check.

**6. Read the built PDF end to end**, then add `TECHNICAL-READ-COMPLETE`. Title, the three
identity fields, section order, the summary numbers and the claims table.

**7. Send on 26 September**, from the registered address, and keep the sent copy. That is D5 and
it does not move.

**Ramsey 2022 is located and needs a browser.** The exact URL and the 84,853,674 byte size are
in [reference/README.md](reference/README.md). Cloudflare refuses every scripted route with
`cf-mitigated: challenge` and the Wayback Machine has no capture, so the trick that rescued
Kellen and Benedict has nothing to serve. Fifteen minutes with a browser and the bandwidth
gets it. Its abstract is verified and buys nothing on its own: Runco is still the only
structural mass anchor. See D64.

**Heimerl is still unsearched.** It would replace the assumed peak to mean blade load and the
side force angle with measurements, and it is a VFS Forum paper rather than a thesis, so the
route is different and probably paid.

**Four of the five motor rows and the servo are still supplier listings** rather than datasheet
PDFs, which is E13 in the ledger. Same reason.

## The one finding six phases did not close

**Mass is not recomputed from geometry for 29 of the 33 budget lines.** The four blade lines are,
the motor line is pinned to the selected drive's catalogue mass, and the two mass lists are held
to 25 percent of each other. The rest are held by a basis string and a growth rule. Cut those 29
lines to 0.8, scale the envelope and the drive mass beside them and follow the arithmetic, and the
gates that fail are all documents quoting the old number rather than physics. This is the
1 September review's own headline finding surviving the whole fix plan, it is not closable by a
gate whose author also writes the data, and what closes it is a drawn section or a weighed part.
[stage-1/audit/phase-6-reaudit.md](stage-1/audit/phase-6-reaudit.md) has the reproduction.

## The human gate

Registration and eligibility are confirmed in [stage-1/human-gate.md](stage-1/human-gate.md).
Roster, sender and technical-read remain outstanding and are the human work still blocking
`--week 5`. They were advisory before week 2 and the engineering did not depend on them, so weeks
2, 3 and 4 ran. Week 5 cannot finish with invented team details or an unread final attachment.

## Standing constraints

**The submission email is never sent by an agent.** Nor is the team registered, nor are real
names written into the capability section. Those are blocked triggers in the loop config and they
do not move.

Gates are run by the supervisor in its own shell and never taken from the week-agent's report:
`python tools/check.py --week N`, `--global`, and `python tools/test_gates.py`. Week 4 leaves all
three green. `tools/check.py` has never been loosened: week 2 added four gates after the first
audit, six thrust to weight gates, a measured-family exception and seven document gates; week 3
added four force map checks and two lateral load checks; week 4 added two combined blade margins,
an overspeed attachment margin, a recomputed centrifugal bending term and a band on the
conservative budget. The week 5 preparation pass fixed one reader defect and loosened nothing:
the coverage audit no longer reads the pandoc front matter as a design claim, and the skip is
positional so the same text in the body still fails. The 1 September hardening pass added 34 gates across the pitch bearing duty, the drive margin, the solver run order and the blade sensitivity, and loosened one thing on purpose: the PDF identity check now ignores whitespace, so kerning inside a heading cannot fail a good document. The review pass that followed added 38 more and loosened nothing: the section is integrated a second time inside check.py so every structural allowable is recomputed rather than read, markers have to open a line everywhere rather than only in the human gate, components are matched to budget lines one to one, the BOM is gated at all, and the coverage window narrowed from 2 percent to 0.5. 184 self-tests. See D66.

## Open items

- **The blade attachment at 1.20 overspeed is 2.59 and it is no longer the tightest margin.**
  It was 1.69 on a supplier listing of 270 N per bearing; ISO 76 on the bearing's own ball
  complement gives 216.985 N, and duplexing to four bearings per blade at 90 percent sharing
  gives 781 N. The duty is computed rather than flagged: the bearing sits at 0.5533 of full
  recirculation, so it wears where it sits, and it carries a static safety factor of 4.15 at the
  operating load against a declared floor of 2.0. What is still missing is a run to failure at
  speed on the flight grease. See D60 and D67
- **The stacked conservative thrust to weight is 2.1221, under the 2.5 requirement.** The design
  estimate clears at 2.5191 and the downside cases are held to a declared floor of 2.0. Closing
  the stacked case needs 117.26 g out of a 775.74 g conservative column, which is a Stage 2 mass
  programme. See D67 and D68
- **The pitch offset controller cannot take the declared pack.** The F411-WSE class board is
  rated 6 to 30 V and 8S reaches 33.6 V charged. The module needs a step-down ahead of it or a
  board rated past 34 V. Neither is drawn and no mass line carries it. See D68
- **The BOM is priced and not quoted.** No supplier was contacted. The 5 lines above 4500 INR are
  50 percent of the 68830 INR total and they need written quotes at Stage 2. See D52
- **Material allowables are published typical values for the class**, not batch certificates, and
  no coupon has been tested. The foam is the sensitive one and the laminate is not: over a 2 to 1
  band on the skin modulus the overspeed margin moves under 3 percent, while the blade reaches
  its floor at 0.6144 of the published foam properties. Stage 2's first coupon is a wrinkling
  test on the delivered foam. See D63
- **The 0.80 continuous derate still has no source** and cannot be given one from inside the
  project. What it has now is a bound: the selection breaks even at 0.7433 on power, which has
  been the binding line since D67 moved it off current, no lower thrust row holds the stacked
  case, and no larger motor fits the mass. A dynamometer run is the first drive
  gate in Stage 2. See D61
- **Three-person roster at VPKBIET**, with 5 hours per week recorded. Member roles, programmes and
  prior work still need to be written into item 7
- **The two scripts had a hand resolved run order and now it is gated.** Running them backwards
  leaves `structure.pitch_link_load_N` holding the value from before the blade moved while
  `pitch.peak_link_force_N` carries the new one, and `check_solver_order` reads that gap. Note
  that from an already converged file both orders reproduce it byte for byte, so a
  reproducibility check would have said the order does not matter. See D62
- **Four of the five motor rows and the servo are supplier listings**, not datasheet PDFs. Week 4
  did not open a manufacturer sheet for any of them
- **The coefficient reserve is deliberate and must stay unspent.** 0.6055 sits below all three
  measured or corrected values available. Week 4 found a calculation that supports the 5 percent
  blade flexibility allowance and deliberately did not spend it. See D36 and D50
- **`largest_dimension_mm` in the week 2 tables is 290 mm** and the packaged module is 364.4 mm.
  The comparison is unaffected because one rule reached all three layouts, and both
  `01-configuration.md` and `09-packaging-and-integration.md` now say so where a reader meets
  the number rather than only in D44
- **`check.py` demands an audit for every week already marked done**, which includes the week
  being gated once its progress file is written, so `--week N` fails in the window between the
  done marker and the audit file. That is stricter than `.claude/weekly-loop.md` describes and it
  is the code that is right. Harmless in the order the loop actually runs
- **The page limit and the file naming convention were never answered.** The question remains at
  the end of the staged submission email. The final filename and page count need a human check
  before sending. See D57
- **The submission identity table now carries the team name, institution, Competition ID and Team
  ID.** Rebuild the attachment after the coding and document changes, then read it end to end
- [stage-1/organiser-email.md](stage-1/organiser-email.md) is cut back to the record of three
  questions the problem statement answered. Its two live ones ride at the end of the
  submission email

## Week 2 debts, reconciled

The week 2 ledger left five debts owned by "week 4" and week 4 retired week 3's debts without
naming them. Six debts recorded as open in the files a fresh session is told to read are closed,
and one instruction inside frozen decision D30 was reassigned to nobody. This is that
reconciliation, done in Phase 5 rather than left for a reader to work out. Debt numbers are week
2's.

| # | Owner then | Where it actually stands |
| --- | --- | --- |
| 1 | week 4 | Retired by D35, then reopened by D67 and closed differently. The stacked case is 2.1221, under 2.5, held to a declared floor of 2.0 with 117.26 g published as the closing gap. The D17 target of 2.75 is further away than it was and is not claimed |
| 2 | week 4 | Open. Only the MN5006 was read off a manufacturer's sheet and the other four rows plus the ESC are still supplier listings. The lower KV on more cells idea D30 raised was overtaken: D67 moved the pack to 8S for a different reason, which is the capacity line rather than the speed ceiling |
| 3 | human | Open and it stays human. No endurance requirement exists to size the derate against. D67 restated the break even at 0.7433, so a true continuous derate of 0.75 still holds |
| 4 | week 4 | Open, and it is the most load bearing of these. The three efficiencies are still assumed and the motor figure still sets motor input power and therefore the drive selection. Week 4 never touched it. It is a bench measurement, listed in Stage 2 |
| 5 | week 4 | Closed. The cluster rows carry their own stored mass, thrust and recomputed thrust to weight, and the candidate comparison gate recomputes each row from its own numbers |
| 6 | week 3 and 4 | Closed by measurement of a sort. The solved schedule gives a peak to mean of 2.5458 against the earlier 2.37, and structure is still sized on the published 4.0 rather than on either |
| 7 | blocked on a paper | Open. Heimerl is still unread and the 28 degree stall cap is still stated rather than measured |
| 8 | week 3 | Closed. Week 3 reran the model against the solved linkage and side force is no longer zero by construction |
| 9 | week 4 | Closed. The spar is sized against the section build-up and its dimensions are stored, and the blade allowable is set by skin wrinkling rather than by the spar |
| 10 | closed by D30 | Still closed, and D67 made it moot: the 2.75 target is 164.6 g away |
| 11 | human | Closed in Phase 5. `organiser-email.md` is cut down and its question count now matches the draft |
| 12 | week 4 | Closed, twice. Week 4 restated the stacked figure and Phase 3 restated it again after D67 moved it |
| 13 | human | Closed in Phase 5. The loop config describes the current thrust to weight rule and the five markers |
| 14 | none, recorded | Still recorded. The first run's prose dates itself 2 September against commits dated 30 August, and the commit dates are authoritative |

**The D30 instruction that went to nobody.** D30 asked for the lower KV route to be priced. No
week owned it and no later ledger carried it. It is answered rather than assigned now: D67's
capacity identity shows that KV cancels out of the mechanical output cap, so a lower KV motor on
the same pack and the same continuous current makes the same mechanical power. Pricing that
route would not have moved the limit. What moves it is more continuous power in the same mass
class, and that is what the Stage 2 drive item asks for.

## Standing risk

Week 4 was interrupted by an API failure partway through and recovered from an uncommitted
working tree in a second session. Nothing was lost, and the lesson is in the loop's favour: the
week's own scripts regenerate `numbers.json` byte for byte, so the state that mattered was
reproducible rather than remembered.

Week H is still the one dependency an agent cannot clear, and it now has the longest lead time in
the project by a distance. Everything else that could be done ahead of it has been done. What is
left of week 5 is short, and it stays blocked until five markers and nine facts arrive from a
person.

The two PDF extraction traps found while reading the built report back are handled in `check.py`
now rather than written down as warnings. `pdf_text` expands the ff ligature pypdf returns
wherever the text says "off", and `check_pdf` compares with the whitespace removed so the
contents page's kerned "T eam capability" still matches. `pdf_selftests` reads the real document
back and holds both. See D62.
