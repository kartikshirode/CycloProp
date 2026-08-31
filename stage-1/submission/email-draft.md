# Stage 1 submission email, drafted and staged

**Staged, not sent.** Sending anything to the organisers is a blocked trigger for every agent in
this repository under D5, and it stays a human action. Nothing below has been transmitted
anywhere. A person sends it on 26 September 2026, a day before the deadline, from the registered
address, and keeps the sent message as the record.

Two things have to be filled in before it goes. Both are marked in the draft and both are
listed under "Before you press send".

## The draft

```
To: pushpak_gc2026@aero.iitb.ac.in
Subject: PUSHPAK Grand Challenge Stage 1 submission, CycloProp cyclorotor module, [REGISTRATION REFERENCE]

Dear PUSHPAK Grand Challenge team,

Please find attached our Stage 1 preliminary design submission for the PUSHPAK
Grand Challenge, covering the design of an indigenous cycloidal rotor propulsion
module.

Registration reference: [REGISTRATION REFERENCE]
Team: [TEAM NAME]
Institution: [INSTITUTION]
Contact: [SENDER NAME AND EMAIL]

The attachment is cycloprop-stage1.pdf, a 21 page report. It covers all seven
required Stage 1 items in the order the problem statement lists them, and it adds
a map from each of the eight published evaluation criteria to the section that
answers it, a claims and risk table, and an appendix of examiner questions with
answers.

The module is a single cycloidal rotor with three blades, passive four-bar cyclic
pitch and thrust vectoring by rotation of the pitch offset. Design thrust is 18.0 N
against the 10 N requirement, and thrust to weight is 3.018 at the design point,
falling to 2.5457 when the conservative mass budget and the low thrust coefficient
are applied together.

One question, if it is easy to answer. The problem statement does not state a page
limit or a file naming convention for the Stage 1 report, so the attachment is
named for the module and the main body is kept to 15 pages with the appendices
after it. If either is wrong for your process, we will resend in whatever form
you prefer.

Thank you for organising the challenge.

Regards,
[SENDER NAME]
[TEAM NAME]
[INSTITUTION]
```

## Before you press send

1. **Replace `[REGISTRATION REFERENCE]`**, in the subject line and in the body. It is the
   reference techfest.org issues at registration, and the problem statement expects the
   submission to quote it. Nobody has recorded it yet, which is why it is a placeholder rather
   than a number: an agent inventing one would be inventing a fact about the team. It is also
   `REGISTRATION-CONFIRMED` in `../human-gate.md` and `[P-7]` in the report
2. **Replace `[TEAM NAME]`, `[INSTITUTION]` and `[SENDER NAME AND EMAIL]`.** Same reason. These
   are `[P-1]`, `[P-2]` and `[P-6]`
3. **Fill the same three fields in the report's own identity table** at the top of
   `cycloprop-stage1.md`, then rebuild the PDF. The report ships with them blank and marked, and
   a reviewer opening a submission whose first table says "to be completed" will read the rest of
   it differently
4. **Rebuild the attachment after any edit.** The command is in `.claude/codemap.md` and it is
   pandoc through xelatex. A stale PDF passes the page count and fails the gate that reads the
   file back
5. **Read the built PDF end to end**, then add `TECHNICAL-READ-COMPLETE` to `../human-gate.md`.
   Check the title, the three identity fields, the section order, the numbers in the summary and
   the claims table. That marker is the last thing before staging is finished and only a person
   can add it
6. **Send from the registered address**, on 26 September 2026, and keep the sent copy

## What the email deliberately does not do

It does not claim a result nobody has measured. The three numbers in it are the ones the report
leads with and each one is recomputed by the gate script from the stored geometry rather than
typed. It does not describe the design as validated, tested or CAE supported, because none of
those is true at Stage 1 and the report says so on its second page.

The page limit question is asked once, at the end, and framed so it needs no reply. It was
worth asking in early September and it was not sent then, so asking it beside the submission is
the last cheap chance to get the format right.
