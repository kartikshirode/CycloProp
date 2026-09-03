# Phase 6: the re-audit, against the fixed tree

Run 4 September 2026, after Phases 1 to 5 of the plan in [full-review.md](full-review.md). The
five passes of the 1 September review were re-run against the corrected repository, at 279 gate
passes and 212 self-tests. A fix nobody attacked is a fix nobody has tested, so the attacks are
reproduced below rather than described.

AUDIT-COMPLETE

**Findings: 7.** Four were fixed during the audit, one is a false positive that earned an escape
marker, one is a standing hole the six phases narrowed and did not close, and one needs a person.

## What the five passes were, and what came back

| Pass | Result |
| --- | --- |
| Alignment against the problem statement | Clean. All 7 required items present, the criteria map covers all 8 criteria, the CAD clause is confronted rather than assumed away, confidentiality is claimed |
| Delivery against `plan.md` | Clean except the page target. Weeks 1 to 4 complete, week 5 delivered everything except what needs a roster |
| Adversarial attack on `tools/check.py` | Two findings, A1 and A5. One gate defect and one standing hole |
| Independent re-derivation of the engineering | Clean. 33 quantities re-derived from geometry with no reference to the stored values, all 33 reproduce |
| Cross-document consistency | Three findings, A2 to A4. Five stale values in live documents, and one false positive |

## A1: the break even derate was measured against the wrong line

`check.py` compared the declared derate against the current fraction of the 180 second rating.
The comment above it said the break even IS the current fraction, and that was true when it was
written. D67 moved the binding line to power, so the true break even became 0.7433 against a
current fraction of 0.7418, and the gate was reading the smaller of the two. A declared derate of
0.7425 would have cleared a check on the line that no longer binds.

It reads the worst of the four now and names which one. The severity is lower than it looks:
other gates compare motor input power against the continuous rating directly, so a derate inside
that window would still have been caught somewhere. What the defect actually produced was a wrong
published number, which is A2.

## A2: the evidence ledger still quoted the pre-D67 break even

E15 said the selection breaks even at 0.7927 and called it the fraction of the 180 second current
the design draws. The submission says 0.7433 and calls it power. Two live documents, three files
apart, disagreeing about the number that decides whether the drive is selectable. Phase 3
corrected the submission and never reached the ledger.

## A3: chord Reynolds is invisible to the coverage audit

The submission carried 134,074 in its rotor sizing table and the evidence ledger carried it
twice, three weeks after the radius sweep settled the design at 130,296. Every gate was green
throughout, and the reason is structural rather than an oversight: `check_numeric_coverage`
matches a number followed by a unit, which is the right scope for it, and Reynolds carries no
unit. So do solidity, figure of merit, every margin and thrust to weight. Those four have gates
that name them. Reynolds had none.

`check_reynolds_stated` closes it on a near miss rule. A document quoting a Reynolds within ten
percent of this design's own is quoting a stale copy of it, because the other Reynolds numbers in
this repository are other people's rotors at 186,000 and 31,600 and are nowhere near. A near miss
that is deliberate takes the same allow marker every other near miss takes, which is a written
reason rather than a threshold tuned until the tree went green.

## A4: two more stale values in live documents

`handoff.md` said the blade reaches its floor at 0.6689 of the published foam properties. The
stored figure is 0.6144 and has been since D67. A sweep of the whole tree for every value this
session superseded returned 90 hits, and 85 of them are in `decisions.md`, `journal.md`,
`progress/` and the earlier audits, where a superseded number is the record working correctly.
The five in live documents were the two Reynolds, the break even, this one, and the submission's
table cell.

## A5: mass is still not recomputed from geometry, and that was the review's headline finding

The 1 September review found that halving every mass line together passed every gate at a
reported thrust to weight of 6.881. Six phases later that exact attack fails on 15 gates. It is
worth being precise about why, because the improvement is smaller than the number suggests.

Reproduce it:

```
cut every non-blade budget line to 0.80, scale the week 2 envelope beside it,
scale the selected drive's catalogue mass, then follow the arithmetic into results
```

That gives 561.39 g, a design thrust to weight of 3.0869 and a stacked case of 2.6032, and it
fails 11 gates. Every one of those 11 is a document quoting the old number or a thrust floor that
was not carried through. None of them is physics. An attacker who edited the documents too would
pass.

What genuinely changed is narrower than the count implies and it is real. The four blade lines
are recomputed from the section and the moduli, so the attack has to exclude them. The motor line
is pinned to the selected drive's own catalogue mass. The two lists are held to 25 percent of each
other per component. Per-blade mass is recomputed from the blade budget and the blade count. That
is why the attack has to be careful and consistent rather than crude.

The remaining 29 lines are still held by a basis string, a self-consistency band between two
lists the same author writes, and a growth rule. Phase 5 made the basis string harder to fake,
which found five bill of materials rows that named a vendor and never said what kind of price it
was, but a basis is still prose.

**This is not closed and it is not closable by a gate.** The gate and the data have the same
author, and no amount of internal consistency distinguishes a module that weighs 678 g from one
that is claimed to. What would close it is a drawn section per line, which is 29 pieces of work
and is Stage 2, or a weighed part, which is also Stage 2. Recording it here rather than bolting on
a threshold, because a gate that catches an 0.80 scaling and misses an 0.90 one buys confidence
rather than safety, and this project has been wrong in that direction before.

## A6: the false positive, and why it kept its number

`02-rotor-sizing.md` says Reynolds at 15.76 N of thrust is 125,500. That is 3.7 percent from the
design point, well inside the near miss band, and it is a different operating point rather than a
stale copy. It carries an allow marker giving that reason. This is the first use of that escape
for a dimensionless number and the mechanism is the one the repository already uses for
dimensioned ones.

## A7: nobody has re-checked the official channels, and nobody can from here

R50 from the original review. Nothing has re-read the organiser's official channels between the
26 August requirements snapshot and the send date, and the problem statement reserves the right to
change any stage. No phase picked this up because no agent can do it: it needs a person with a
browser. It belongs beside the human gate markers and it is the cheapest item on that list.

## The page count, which is a delivery finding rather than a defect

The plan's week 5 set a 15 page target for the attachment when no organiser limit was supplied.
The report is 30 pages, having grown from 21 through the corrections and then the figures. No
organiser limit exists, the question rides at the end of the staged email, and cutting a report in
half to hit a target this project set for itself would be the wrong trade against the presentation
and clarity criterion. Recorded, not acted on.

## Where the tree stands

`python tools/check.py --all` passes 279 gates. `python tools/test_gates.py` passes 212
self-tests. `python tools/check.py --week 5` fails one gate and it is the human gate, with
ROSTER-CONFIRMED, SENDER-CONFIRMED and TECHNICAL-READ-COMPLETE outstanding. The attachment is 30
pages and carries seven figures, each of them rendered from `numbers.json` and held to it.

Of the 64 findings the 1 September review raised, 63 are closed. The one that is not is A5 above,
which is the same finding this audit ends on, and it is the honest state of the mass case.
