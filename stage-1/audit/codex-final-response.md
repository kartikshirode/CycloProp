RESPONSE-COMPLETE

# Answering the codex audit

**This answers the 4 September audit, which is at commit `1b331cb`.** The 23 September audit
replaced it in `codex-final.md`, and its answer is
[codex-round-9-response.md](codex-round-9-response.md). The F numbers below refer to the older
audit and do not match the current file.

Written 4 September 2026, against [codex-final.md](codex-final.md). Every finding was checked
before it was acted on, because an audit is evidence and not a verdict, and two of the eleven
turned out to need arguing with rather than fixing. The tree it left behind passes 288 gates and
221 self-tests, and the report is rebuilt at 30 pages.

## What the eleven findings turned into

| | Finding | What checking it found | State |
| --- | --- | --- | --- |
| F1 | The MN5006 is catalogued 4 to 6S and the design declares 8S | Half right, and the half it got right is the important half | Answered and gated, D70 |
| F2 | Item 7 and the email still carry placeholders | Right. Nothing here can fill them | Open, and only a person closes it |
| F3 | The servo margin is 2.33 in the prose and 1.982 in the data | Right, and worse than reported: the two sit in the same document | Fixed |
| F4 | The stacked case misses and should say so plainly | Right, and it now misses by more | Fixed, and the number moved |
| F5 | The attachment margin is a bearing check wearing a joint's name | Right | Fixed |
| F6 | The pitch controller is over its input rating on a charged pack | Right, and it was a note rather than a design | Fixed, D70 |
| F7 | Live evidence files carry retired numbers and statuses | Right on all four counts | Fixed, and gated so it cannot recur |
| F8 | A 14 mm shaft in a 16 mm design, and a reaction torque missing the belt efficiency | Right | Fixed |
| F9 | Five evidence classes named where seven are used, three values called independent, a cost share of 52 percent | Right on all three | Fixed |
| F10 | Nobody has rechecked the official channels | Right that nobody had. It turned out to be doable from here after all | Closed, nothing that governs the submission has moved |
| F11 | Figures are numbered and tables are not | Right, and declined for now with a reason | Recorded |

## F1, which is the one worth reading

The audit called the motor a blocker: a part catalogued 4 to 6S carrying an 8S design, with no
manufacturer evidence that its 650 W and 26 A ratings still apply. It was right that nothing in
the repository recorded a cell range at all, which is why no gate could see it and why the answer
had never been written down.

It is wrong that the motor is out of range, and the correction is a number rather than an
opinion. An ESC is a buck converter, so the windings never see the pack. What they see is the
back EMF plus the resistive drop, and at 9932.4 rpm on a KV of 450 with 19.2876 A through
60 mOhm that is 23.2293 V. Six cells off the charger are 25.2 V. The motor sits inside its own
catalogue window at the design point, and the pack sits outside it because a 6S pack sags under
this current to less than the windings ask for. Those are two different sentences and the report
now carries both.

What survives of the finding, and it is real, is that the published ratings came from a
manufacturer test on 6S and no written confirmation at this duty exists. That is a Stage 2 gate
in the report rather than a footnote, alongside the ESC switching losses the assumed 0.95 does
not separately account for.

The gate that stops this recurring is `check_drive_voltage`. It recomputes the terminal voltage
from rpm, KV and the draw, holds it under the catalogue ceiling, and requires the thrust and
power document to state what the windings see whenever the declared pack sits above the motor's
printed range. A pack over the motor with silence in the document fails. Seven self-tests cover
it, one of which is the audit's own attack.

## F6, which cost the design case a third of its margin

The pitch controller has been sitting across a charged 8S pack 3.6 V over its rating since D67,
carried as an open item in two documents, with no part drawn and no mass line behind it. The
audit was right to call that a blocker and right that a note is not a design.

It has a regulator now: rated at least 42 V in against the 33.6 V it will see, 12 V out at 1 A,
which lands in the middle of the board's 6 to 30 V window rather than at an edge. It carries the
servo rail behind the board as well, so its conversion loss of 1.4118 W is a module electrical
draw. No supplier listing has been read for a specific part, so it is 10.0 g nominal on the
allowance growth class, and evidence row E20 says exactly that.

The cost is visible and it is the most important number in this response:

| | Before | After |
| --- | --- | --- |
| Module mass, nominal | 677.9 g | 687.91 g |
| Module mass, conservative | 763.2 g | 775.74 g |
| Design case thrust to weight | 2.5563 | **2.5191** |
| Coefficient downside alone | 2.4284 | 2.3931 |
| Mass downside alone | 2.2705 | 2.2339 |
| Both stacked | 2.1569 | **2.1221** |
| Mass to carry the stacked case over 2.5 | 104.76 g | 117.26 g |

The requirement is still met on the design case and the margin on it is now 0.8 percent rather
than 2.3. That is worse and it is honest, and the alternative was a controller rated past 34 V
that needs a catalogue nobody here can reach.

## F4, where the audit and this project agree and the wording still changed

The audit asked for the stacked miss to be stated plainly rather than buried under the 2.0
screening floor. The report already published the closing mass rather than claiming a pass, so
the disagreement is narrower than it reads, but the paragraph is sharper now and the number in it
is larger.

One correction to the finding itself. It gives the stacked case as 15.3 N at 763.24 g. The
conservative thrust is 16.1493 N, and 16.1493 over 763.24 g is where 2.1569 came from. The 15.3
looks like the conservative thrust with the blade deflection loss applied a second time.

## F3, F7, F8 and F9, which are the same failure four times over

Every one of these is a number that was true when it was written and stopped being true without
anything noticing:

- The report's prose said the servo margin was 2.33 while its own declaration block, eleven pages
  later in the same file, said 1.982
- The drive paragraph said the design draws 0.704 of the published power and 0.7927 of the
  current, and that the current fraction is where the selection breaks even. D67 moved the
  binding line to power. The claims table on the next page already said 0.7433 on power
- The evidence ledger called two rows measured when four are, named E18 and E19 as Kellen's
  measurements when the pair is E17 and E18, and quoted a stacked case of 2.517 with a mass gap
  from before D67
- The literature file still said the Kellen thesis could not be downloaded, three days after a
  second attempt got it and the ledger began reading figures off its plots
- The packaging sketch drew a 14 mm shaft against the 16 mm the solver builds
- The report named five evidence classes where the ledger defines seven, called three
  coefficient values independent when two of them come out of Benedict 2010, and put the five
  expensive bill of materials lines at 52 percent of a total where they are 49.8

None of these was catchable by the existing gates and the reason is structural.
`check_numeric_coverage` matches a number followed by a unit, which is the right scope for it,
so every dimensionless figure in the list above was invisible. This is the fourth round in which
a person reading has found one, and reading is not a mechanism.

`check_retired_values` is the mechanism. Every value this project has published and superseded is
listed in `check.py` with what it used to be, and no live document may quote one. It is an exact
token match rather than a band, so there is nothing to tune and there are no false positives to
argue about; a number that legitimately repeats a retired one takes the same allow marker every
other deliberate near miss takes, with a written reason on the line. `decisions.md`,
`journal.md`, `progress/` and `audit/` sit outside it on purpose, because a superseded number
there is the record working correctly.

It found three more the moment it ran, and one of them was in `handoff.md`, which is the file a
fresh session is told to read first.

## Three the audit did not raise

Turning its findings into fixes surfaced three more, and they belong on the record beside them:

**The balance trade in the report was priced on numbers that had moved twice.** It gave the
balanced pitch link margin as 4.69 where the design notes say 6.20, and the ballasted stacked
case as 2.406 where it is 2.0292. The conclusion survives, because the trade is declined on the
load path rather than on the mass, but two of its three numbers were wrong.

**The selected configuration candidate had drifted from the envelope it is supposed to equal.**
The gate compares them at a 2 percent display tolerance and the drift was 1.55 percent, so it
passed. Adding the regulator to one list and not the other would have widened it to 3 percent and
failed, which is how it came to light. Both lists carry the part now.

**The radius sweep quoted the design mass at the design radius and would not have followed it.**
The 110 mm row is tied to the week 4 budget and nothing recomputes it, so it kept 677.91 g and a
thrust to weight of 2.5563 while the results block moved. Every row carries the new part.

## F11, declined for now, with the reason

The seven figures are numbered by pandoc and the tables are not, and the audit is right that a
30 page attachment is easier to interrogate with numbered tables. Adding captions to twenty five
markdown tables changes the pagination of a document that is already twice its own page target,
three weeks before it is sent, to buy an evaluator a cross reference they can also get from the
section heading. If the page question comes back from the organisers with an answer, this is the
first thing to do while the document is open anyway.

## Is it 62 out of 100

The arithmetic is right: the eight criterion scores sum to 62, and the two lowest are thrust to
weight at 7 of 15 and aerodynamic analysis at 7 of 15.

The rubric it is scored against is the question. The problem statement attaches those eight
criteria to "the detailed design report, CAE-supported evidence, final presentation, and viva
during the Techfest evaluation", and publishes no separate Stage 1 rubric. Scoring a Stage 1
paper against them means marking it down for having no CFD, no coupons and no test data, which is
what Stage 1 is. Read as a prediction of the final score if nothing else happened, 62 is fair.
Read as a shortlisting signal against other Stage 1 papers, which is what the 2 October decision
actually is, it is pessimistic, because every entrant is in the same position on measured
evidence.

What the number does get right is where this submission is weakest, and both of its 7s point at
real things. The design case clears 2.5 by 0.8 percent and all three downside cases miss. The
coefficient the whole thrust case rests on is transferred across a change of blade count,
airfoil, solidity and Reynolds, and nothing measured on this hardware exists. Neither of those is
closed by better writing.

## What is left

One item, and it is not an agent's to close:

1. **The human fields.** Item 7 carries `[P-1]` through `[P-9]`, every Stage 2 row names `[P-1]`
   as owner, and the email says `[SENDER NAME]`. Real names, roles, programmes, tools and
   facilities go in, then the PDF is rebuilt and read end to end, then `TECHNICAL-READ-COMPLETE`
   goes into `human-gate.md`. It is the last of the five markers.
## F10 and R50, closed the same afternoon

The audit said a human with a browser had to re-read the organiser's channels. It was right that
nobody had done it since 26 August and wrong that it needed a person, because the competition
page is a JavaScript shell and the readable source is the API behind it, which answers plain
curl. No browser tool is connected to this session and none was needed.

The whole record was pulled and diffed field by field against the 26 August snapshot. Twenty
three fields are identical, including every one that governs the submission: the timeline with
its 27 September deadline, the rules, the structure text carrying the eligibility clause, the
FAQ, the contact address, the team size and the problem statement URL. The PDF at that URL is
byte identical to the copy in `reference/`, 206,463 bytes to the same sha256, so the document
this project is built on has not changed a character.

Three fields moved and none is a requirement. Registrations went from 11 to 57, which is worth
knowing rather than acting on: 15 Stage 1 slots against a field that is at least 57 and still
open. The sponsor image and link were cleared to null.

The second snapshot sits at `reference/techfest-api-cycloprop-4sep.json` beside the first rather
than over it, and `reference/README.md` carries the one line command to repeat the check. Doing
it once more on the send date costs a minute now that both snapshots and the diff exist.

One thing the re-read confirms by absence. No page limit and no file naming convention is
published anywhere: not in the rules, the FAQ, the structure text or the problem statement. The
question at the end of the staged email is the only route to an answer, which settles the page
count argument in F11's favour rather than against it.
