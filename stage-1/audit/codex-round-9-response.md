RESPONSE-COMPLETE

# Answering the 23 September audit

Written 23 September 2026, against the audit committed at `59ad408` in
[codex-final.md](codex-final.md). That file held the 4 September audit until this one replaced
it; the answer to the older version is [codex-final-response.md](codex-final-response.md).

Every finding was checked against the tree before anything was changed. All eight held up. That is
worse than the last round, where two needed arguing with, and it is the right kind of worse: this
audit found things in the evaluator facing document, where they cost marks, rather than in the
repository around it.

## What the eight findings turned into

| | Finding | What checking it found | State |
| --- | --- | --- | --- |
| F1 | Item 7 is still a template, while the roster marker says confirmed | Right. The report and the marker disagree, and only a person can make them agree | Open, needs the team facts |
| F2 | The staged email quotes pre-D70 results and a placeholder | Right, and it was my miss: the D70 resync never touched the email | Fixed, except the sender name |
| F3 | The criteria map claims all four thrust to weight cases pass | Right, and it is the worst sentence the report carried | Fixed |
| F4 | Stale kinematic, aerodynamic and power values in the attachment | Right on every count, and there were more than it listed | Fixed, and gated |
| F5 | The project did not meet its own margin contract | Right. The report says so now, in those terms | Reframed, not redefined |
| F6 | The nominal pass is too thin for the mass evidence behind it | Right. Its suggested paragraph is in the report, adapted | Fixed |
| F7 | The literature trail cannot be followed from the attachment | Right | Fixed, with a locator table |
| F8 | The audit context file is stale after D70 | Right | Fixed with the round 10 files |

## F3 and F4, and why the gates let them through

The criteria map row read "a 33 line budget and four cases, all clearing the limit", directly
under a results table saying three of the four miss. That is the sentence an evaluator scoring
the thrust to weight criterion reads first, and it made the disclosed downside table look like a
disclaimer that the scorecard then ignored. It reads now: a 34 line budget and four cases, the
design case clearing 2.5 by 0.8 percent and all three downside cases missing, with the closing
mass published.

The stale values fall into three groups, and each one explains a different gap:

- **Declarations inside the tolerance.** Appendix B declared a peak to mean of 2.501 against a
  stored 2.5458, and a pitch link margin of 3.3015 against 3.2878. The declaration gate compared at
  the 2 percent display tolerance, so 1.76 and 0.42 percent passed. A declaration is a machine
  readable copy and should match at the precision it is written, so it does now. Of 324
  declarations across ten documents, five failed the stricter rule, and all five were those two
  values.
- **Prose the retired list did not know about.** A transmission angle of 58.58, a side force split
  of 11.00 and 0.978, module power at 516.6. The transmission angle one inverted a conclusion: the
  report said the obtuse end sits outside the conventional band of 40 to 140, when the corrected
  range, 53.88 to 135.68, is inside it at both ends. All three are on the retired list now.
- **Rounded copies the D70 resync could not see.** It substituted exact tokens, so a table
  printing 2.1569 as 2.157 or 677.91 as 678 g kept the old number. That left the whole
  configuration comparison in `01-configuration.md`, four rows of the radius sweep in
  `02-rotor-sizing.md`, two stacked ratios in the report's own comparison table, and the gap to
  the 2.75 target in three files. The report also said the single rotor wins its decision metric
  by 36 percent where the design notes and the arithmetic both say 23.

That third group was not in the audit. It came out of a near miss scan run after the listed fixes:
every number in live prose with two or more decimals, checked against every stored value, printing
the ones within 5 percent of a stored value without matching it at their written precision. Most
of what it prints is unrelated quantities that happen to sit close, which is why it is a diagnostic
a person reads rather than a gate. It is at the bottom of this file.

## F5 and F6, the framing

The audit asked for two things that pull the same way. Stop presenting the result as a pass with
reassurance attached, and stop leaning on the 2.0 floor this project set itself after its own 2.5
rule broke.

Both are done in the report. The summary now says the design point is a preliminary pass on 2.5
by 0.8 percent and not a margin anybody should rely on. The mass section says the estimate behind
it is not accurate to 0.8 percent, that either downside alone takes it under 2.5, that the project
set out to hold every downside case to 2.5 and a correction broke that, and that Stage 2 treats
658.48 g on the conservative column as a gate. The claims table and the balance trade no longer
mention the floor.

The floor still exists inside `tools/check.py` as a screen, and the design documents still carry
it, because it does real work there: it is what stops a future edit from quietly publishing a
stacked case of 1.4. What changed is that the evaluator facing document no longer offers it as
comfort.

What was not done is edit the week 2 and week 4 progress files, which record those weeks as
complete under the rule in force at the time. They are history, and the audit's point is made
where it belongs, in the report and in D71.

## F2, and the question that was in the wrong email

The email quoted 2.5563 and 2.1569, from before D70. It quotes the current figures now and calls
the design case a preliminary pass by 0.8 percent, so it cannot be read against an attachment that
says something more cautious.

The audit's second point was sharper than the first. The page limit question sat at the end of the
submission email, which means it would be asked on 26 September and answered after there was any
time to act. It is now its own short email, staged in `../organiser-email.md` to be sent as soon as
possible. If the answer is a limit under 32 pages, that file gives a cut order. The submission
email keeps only an offer to resend.

## F7, the reference list

Eight numbered references with authors, titles, venues, years and, where the repository holds
one, a handle URL. The two unread works are named with their full titles and marked unread.
Nothing was guessed: where the repository does not hold a volume, a page range or a DOI, the
entry leaves it out and says why. A locator table follows it, giving the table, section, figure or
printed page for each of twelve borrowed numbers. The report grew from 30 pages to 32.

## Is it 60 out of 100

The arithmetic is right. The eight scores sum to 60.

Unlike the 4 September audit, most of this one's deductions were for errors in the document
rather than for the design being a Stage 1 design, and most of those are fixed tonight. The
presentation score of 5 out of 10 was driven by the false criteria map row, the stale numbers, the
placeholders and the references, and three of those four are gone. The kinematics and packaging
scores each lost something to a stale value that is now corrected. The thrust to weight score of 6
out of 15 is physics and framing, and only the framing moved.

No new score is claimed here. The round 10 verification pass exists to say whether these fixes
landed, and a score from the person who made them would be worth nothing.

## What is left

1. **Item 7 and the sender name.** Real names, roles, programmes, prior work, tool access,
   facilities and a real owner on each Stage 2 row. This is also what makes `ROSTER-CONFIRMED`
   true of the report and not only of the marker file
2. **The format question**, sent today or tomorrow from the registered address
3. **Round 10**, a narrow Codex verification pass on the diff since `59ad408`, prepared in
   `_codex-prompt.md` and `_codex-context.md` at the repository root
4. **The technical read**, then `TECHNICAL-READ-COMPLETE`, then the send on 26 September

## The near miss scan

Kept here because it found what the audit did not, and because it should run again after the
team facts go in. Run it from the repository root with a list of documents as arguments. It
reads `stage-1/design/numbers.json` and `tools/check.py` and writes nothing.

```python
import io, json, re, sys, pathlib
sys.path.insert(0, "tools")
import check
data = json.load(io.open("stage-1/design/numbers.json", encoding="utf-8"))
stored = []
def walk(o):
    if isinstance(o, dict): [walk(v) for v in o.values()]
    elif isinstance(o, list): [walk(v) for v in o]
    elif isinstance(o, (int, float)) and not isinstance(o, bool) and o: stored.append(float(o))
walk(data)
tok = re.compile(r"(?<![\w.,])(\d+\.\d{2,})(?![\w.]|\.\d)")
for rel in sys.argv[1:]:
    text = re.split(r"##\s*Numbers used", pathlib.Path(rel).read_text(encoding="utf-8"), 1)[0]
    for i, line in enumerate(text.splitlines(), 1):
        if check.allow_reason(line): continue
        for m in tok.finditer(line):
            v, dp = float(m.group(1)), len(m.group(1).split(".")[1])
            if any(abs(v - s) <= 0.5 * 10 ** -dp + 1e-9 for s in stored): continue
            near = min(stored, key=lambda s: abs(s - v) / abs(s))
            if 0.001 < abs(near - v) / abs(near) < 0.05:
                print(f"{rel}:{i} {m.group(1)} near {near}")
```
