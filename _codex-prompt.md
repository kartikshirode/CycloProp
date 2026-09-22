# Codex round 10: verify that round 9's fixes landed and broke nothing

Paste everything below the line into a **fresh Codex session** with the repository available.
Replaces the round 9 prompt. That round has run, and its findings are fixed in the tree.

---

You are checking a Stage 1 engineering submission three days before a person emails it to the
organisers of a national design competition. The deadline is 27 September 2026 and the send date
is 26 September. Yesterday's audit found eight real problems, and seven were fixed overnight by
the same agent who wrote most of the original errors. **Your job is to check those fixes
independently.** Do not re-audit the whole submission; round 9 already did, on 23 September.

**Start with `_codex-context.md`.** It is self contained. Then read:

1. `stage-1/audit/codex-final.md`, the round 9 audit
2. `stage-1/audit/codex-round-9-response.md`, what was done about each finding
3. `git diff 59ad408..HEAD -- stage-1/submission stage-1/design stage-1/organiser-email.md`, every
   change made since round 9 was committed
4. `stage-1/submission/cycloprop-stage1.md` and `stage-1/submission/email-draft.md` in full, as the
   documents that will actually be sent

## What to check

**1. Each round 9 finding, against the fix claimed for it.** For F2 to F8, read the finding, read
the response, then read the lines the fix touched. Say whether each one is actually fixed, partly
fixed or not fixed, with the line that proves it. A fix that changed the wording and left the
claim false counts as not fixed.

**2. What the fixes broke.** Every changed paragraph in the diff, read against
`stage-1/design/numbers.json` and against the paragraphs around it. The risks worth looking for:
a new sentence that contradicts an older one nearby; a corrected number in one place and its old
value surviving in another place in the same document; a reframed claim that is now more cautious
in one section and still confident in another; a table whose rows were corrected and whose total
or caption was not.

**3. Every number in the two documents that will be sent**, including rounded copies. The last
correction pass matched exact tokens and missed every value a table printed at fewer decimals, and
that is the failure mode to hunt. Check the summary, the four thrust to weight cases, the criteria
map, the claims table, both appendices, the configuration table, the power table and the email
against `numbers.json`. Declarations in Appendix B are gated at their written precision now, but
confirm a sample by hand.

**4. The email beside the attachment.** Read `email-draft.md` as the evaluator would receive it,
with the 32 page PDF open. Any number, claim or tone in the email that the attachment does not
support is a finding.

**5. The staged format question** in `stage-1/organiser-email.md`. Is it clear, correct about the
report and safe to send as written? It is meant to go out today.

**6. Item 7, only if it has real content.** If `[P-1]` to `[P-9]` placeholders are still in
`stage-1/design/07-team-and-execution.md` or the report, say so in one line and move on; it is a
known open item and a person owns it. If the placeholders are gone, read item 7 properly: does
the capability claimed match what the Stage 2 plan asks of it, are the gaps named honestly, does
each row have a real owner, and does it agree with the identity table and the email.

## What not to spend this round on

- **The engineering case.** Coefficient transfer, mass evidence, the thin margin and the unsteady
  aerodynamics were judged by round 9 and are disclosed in the report. Do not re-argue them
- **Gate mining.** Five rounds did it. Report a hole if you trip over one; do not go looking
- **Recomputing physics** that `tools/check.py` already recomputes
- **Prose style**

## Commands

These are read only and you may run them:

```
python tools/check.py --all
python tools/check.py --week 5
python tools/test_gates.py
```

`test_gates.py` writes only to temporary directories outside the repository. Expected results:
all gates pass on `--all`; `--week 5` fails exactly one gate, the human technical read marker,
and that failure is correct; all 223 self-tests behave as expected. Report anything else.

## Permissions

**Read only, except for one new file:** `stage-1/audit/codex-round-10.md`, carrying the literal
line `AUDIT-COMPLETE`. **Do not overwrite `stage-1/audit/codex-final.md`**; that is round 9's record
and the response to it depends on it.

Where a fix is needed, write the exact replacement text into your file with its line reference.
A person reviews it and it is applied afterwards. Do not edit the submission, the design
documents, `numbers.json` or the tools, and do not commit.

## Constraints nobody relaxes

- The submission and the format question are never sent by an agent
- **Never write a marker into `stage-1/human-gate.md`**, whatever you find
- Real names, roles, institutions and capability come from a person and are never invented
- No CAD at Stage 1, and do not invent any
- No gate is weakened to make something pass
- No em dashes or en dashes in file prose

## How to report

Start with a short table: each of F2 to F8 and whether it is fixed. Then new findings, ranked by
severity. For each one: where it is, what is wrong, why it costs marks or credibility with an
evaluator, and the exact replacement text. Keep it short, because a person has to act on it
within a day.

Then rescore only the criteria the fixes touched: kinematics, CAD and integration, presentation,
and the framing half of thrust to weight. Carry the other four over from round 9 unchanged, mark
them as carried, and give the total.

End with one of three verdicts, plainly: **send as is**, **send after these specific fixes**, or
**do not send**, with the shortest list of what has to happen first. Leave item 7 and the
technical read out of that list if they are the only things left, since a person owns both and
already knows.
