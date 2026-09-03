# Stage 1 submission email, drafted and staged

**Staged, not sent.** Sending anything to the organisers is a blocked trigger for every agent in
this repository under D5, and it stays a human action. Nothing below has been transmitted
anywhere. A person sends it on 26 September 2026, a day before the deadline, from the registered
address, and keeps the sent message as the record.

The Competition ID and Team ID are recorded below. The sender name and the remaining team
details still need a last check before it goes.

## The draft

```
To: pushpak_gc2026@aero.iitb.ac.in
Subject: PUSHPAK Grand Challenge Stage 1 submission, CycloProp cyclorotor module, CP-439436FADAD2, TM-5A7C41AF909

Dear PUSHPAK Grand Challenge team,

Please find attached our Stage 1 preliminary design submission for the PUSHPAK
Grand Challenge, covering the design of an indigenous cycloidal rotor propulsion
module.

Competition ID: CP-439436FADAD2
Team ID: TM-5A7C41AF909
Team: Kalash, 3 members
Institution: VPKBIET
Contact: [SENDER NAME], kartikshirode123@gmail.com

The attachment is cycloprop-stage1.pdf. It covers all seven
required Stage 1 items in the order the problem statement lists them, and it adds
a map from each of the eight published evaluation criteria to the section that
answers it, a claims and risk table, and an appendix of examiner questions with
answers.

The module is a single cycloidal rotor with three blades, passive four-bar cyclic
pitch and thrust vectoring by rotation of the pitch offset. Design thrust is 17.0 N
against the 10 N requirement, and thrust to weight is 2.5563 at the design point,
above the 2.5 target. It falls to 2.1569 when the conservative mass budget and the
low thrust coefficient are applied together, and the report says what closing that
would take rather than leaving it implied.

One question, if it is easy to answer. The problem statement does not state a page
limit or a file naming convention for the Stage 1 report. If either is wrong for your process, we
will resend in whatever form you prefer.

Thank you for organising the challenge.

Regards,
[SENDER NAME]
Kalash
VPKBIET
```

## Before you press send

1. **Keep both identifiers**, in the subject line and in the body. The site provides a Competition
   ID and a Team ID, not a separate registration reference. They are `REGISTRATION-CONFIRMED` in
   `../human-gate.md` and correspond to `[P-7]` in the team form
2. **Replace `[SENDER NAME]`** with the person who will send the message. The sender address is
   `kartikshirode123@gmail.com`; send only from the registered address
3. **Check the report identity table** at the top of `cycloprop-stage1.md`, then rebuild the PDF.
   The team, institution and both IDs must match this draft
4. **Rebuild the attachment after any edit.** The command is in `.claude/codemap.md` and it is
   pandoc through xelatex. A stale PDF passes the page count and fails the gate that reads the
   file back
5. **Read the built PDF end to end**, then add `TECHNICAL-READ-COMPLETE` to `../human-gate.md`.
   Check the title, the team, the institution, both IDs, the section order, the numbers in the
   summary and the claims table. That marker is the last thing before staging is finished and only
   a person can add it
6. **Send from the registered address**, on 26 September 2026, and keep the sent copy

## What the email deliberately does not do

It does not claim a result nobody has measured. The three numbers in it are the ones the report
leads with and each one is recomputed by the gate script from the stored geometry rather than
typed. It does not describe the design as validated, tested or CAE supported, because none of
those is true at Stage 1 and the report says so on its second page.

The page limit question is asked once, at the end, and framed so it needs no reply. It was
worth asking in early September and it was not sent then, so asking it beside the submission is
the last cheap chance to get the format right.
