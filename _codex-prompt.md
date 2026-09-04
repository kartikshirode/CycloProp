# Codex audit prompt: the whole project, against the plan and against the goal

Paste everything below the line into a **fresh Codex session** with the repository available.
Replaces the 29 August prompt, which asked whether an agent could execute the plan. The plan has
since been executed. This round audits what came out of it.

---

You are auditing a finished Stage 1 submission for a national engineering design competition
before a human sends it. The deadline is 27 September 2026, the send date is 26 September, and
today is 4 September, so there is time to fix anything you find. Nothing here is a rush job and
nothing needs to be waved through.

**Start with `_codex-context.md`.** It is self contained and holds the competition requirements,
the current design, the repository shape, the gate contracts and every open item the project
already knows about. Everything the official website would tell you is offline under `reference/`.
Do not spend time fetching anything.

Then read, in this order:

1. `stage-1/submission/cycloprop-stage1.md`, the thing that actually gets evaluated
2. `context.md`, the requirements authority
3. `stage-1/plan.md`, the plan that promised the submission
4. `stage-1/design/` in full, the nine documents and the evidence ledger
5. `stage-1/audit/full-review.md` and `stage-1/audit/phase-6-reaudit.md`, what previous rounds
   found and what is still open
6. `tools/check.py` and `stage-1/design/numbers.json` when you need to know where a number came
   from

## The question this round has to answer

> **Would an IIT Bombay evaluator, scoring this against the published criteria, put it in the
> top 15 of a national call? And did the project deliver what its own plan said it would?**

Everything below serves those two.

## What to judge, concretely

**1. The goal, criterion by criterion.** Score the submission against each of the eight published
criteria and say what you are scoring out of the weight. Give a reason per criterion, not an
adjective. Name the ones where the report is thin and say what a stronger answer would contain.
Aerodynamic analysis quality carries 15 percent against a design with no CFD and no wind tunnel,
so it deserves the hardest look. Presentation and clarity carries 10 percent and is decided by
reading the attachment as an evaluator would, cold, without the design documents beside it.

**2. The goal, item by item.** All seven required items have to be present as real content rather
than as headings. Check that item 4 answers power and not only thrust, that item 5 gives both the
mass budget and the ratio as results, and that item 7 is an execution plan with owners,
dependencies and gates rather than a list of headings. Check thrust vectoring is demonstrated by
kinematic and performance analysis, because it is a requirement rather than a bonus.

**3. Delivery against the plan.** `stage-1/plan.md` has five weeks plus a human gate, with a
"Done when" for each. Walk them against what is in the tree. Say what the plan promised and did
not produce, what it produced that the plan never asked for, and whether any week is recorded as
done on weaker evidence than the plan required.

**4. The engineering, where the gates cannot see.** The arithmetic has been re-derived twice and
reproduces, so do not spend the round recomputing what a gate already recomputes. Spend it on the
first-write physical assumptions no gate can question: the coefficient transfer across blade
count, airfoil, solidity and Reynolds; the figure of merit band; the momentum area declaration;
the peak to mean blade load factor; the foam and skin allowables; the bearing and belt selections.
For each one, say whether the assumption is defensible in a viva, and if it is not, say what
would make it so.

**5. The mass case.** This is the project's known weak point and it is documented as A5. Read it,
then form your own view rather than inheriting ours. Is publishing a 104.76 g gap on the stacked
downside case the right call, or does it hand an evaluator a reason to mark down two 15 percent
criteria at once? If you would present it differently, write the paragraph you would use.

**6. What fails late.** Things that look fine now and bite on 26 September. Submission mechanics,
file naming, the identifiers quoted, figure and table numbering in the built PDF, citation
completeness, anything in the staged email.

**7. The hostile viva question.** Name the single question an examiner who knows this literature
would ask that the repository has no answer for. One question, the best one, with your assessment
of how bad the silence is.

## What not to spend this round on

- **Do not hunt for gate holes.** Four rounds did that and every finding is closed. If one falls
  into your lap, report it, but it is not the job.
- **Do not recompute arithmetic that a gate already recomputes.** Thrust, power, the four-bar
  closure and the structural margins are recomputed from geometry on every run.
- **Do not rewrite prose for style.** Substance findings only.

## Permissions and limits

This round is **read only on the design, the submission and the tools.** The tree is green, the
number file is written only by the solvers under a byte identity contract, and an edit made in
passing is more likely to break that than to help. Write exactly one file:

`stage-1/audit/codex-final.md`, containing the literal line `AUDIT-COMPLETE` and your findings.

Where you want a change, put the concrete diff or the replacement paragraph inside that file and
let a later pass apply it. If you do decide something has to be changed in place, then after the
edit run `python tools/check.py --all`, `python tools/check.py --week 5` and
`python tools/test_gates.py`, and report all three results including the human gate failure, which
is expected and correct.

## Constraints that are not yours to relax

- The submission email is never sent by an agent, and the team is never registered by one
- **Never write a marker into `stage-1/human-gate.md`.** Not one, not for any reason, whatever
  you conclude. Those five lines belong to a person and the whole point of them is that no agent
  can claim them
- Real names, institutions and claimed capability are written by a human, never invented or
  filled in
- No CAD at Stage 1. The competition says CAD supported and also says Stage 1 is on paper, and the
  submission confronts that tension deliberately. Do not resolve it by inventing CAD
- Do not weaken a gate to make anything pass. If a gate is wrong, say why it is wrong
- No em dashes or en dashes anywhere in file prose, plain ASCII only. A gate enforces it

## How to report

Findings ranked by severity, each carrying where it is, what is wrong, why it matters for the
score rather than for tidiness, and a concrete fix. Separate the ones that should be fixed before
26 September from the ones that belong to Stage 2.

Then two things at the end, both plainly:

1. Your criterion by criterion score, summed, with the number you would expect from an evaluator
2. Whether you would send this submission as it stands. If not, the shortest list of changes that
   would get you to yes

Be skeptical of the decisions file. It is settled ground, but it was settled by us, and D67 in
particular moved the design point late and left one open item behind it.
