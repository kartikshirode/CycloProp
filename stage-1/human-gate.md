# Week H: the human gate

The tasks in this file are not loop work. An agent cannot do any of them and must not
claim any of them are done. Week 5 is a hard block on all four.

Each item is confirmed by adding its marker on its own line in the status block at the
bottom. The markers are status only. **No personal details go in this file**, no names, no
enrolment numbers, no contact details. Those live wherever the registration form wants
them, and the repository stays free of them.

## What has to happen

**1. Eligibility check, first.** Do this before anything else, including registration. The
clause disqualifies a whole team at any stage, including after results are announced, so an
ineligible roster turns every other week into wasted effort. Check every member against the
clause quoted in [../context.md](../context.md) before the team is fixed.

**2. Registration** on techfest.org, and keep the registration reference. The submission
email is expected to quote it.

**3. Roster confirmed.** Currently one person, confirmed 27 August. If that is still true at week 5, the capability section is written for a solo entry.
Week 5 writes the team capability section around real capability, and the problem
statement's preference list reads like a spec for it. Structure comes from the agent, the
substance comes from you.

**4. Sender confirmed.** Who sends the submission on 26 September, from which address.
Sending is a blocked trigger for every agent in this repo, so a person has to own it.

## Two questions worth asking the organisers

Both are cheap now and expensive on 26 September. They are in
[organiser-email.md](organiser-email.md) and neither is answered by the problem statement:

- Is there a page limit on the Stage 1 report, and a preferred file naming convention
- What registration reference should the submission quote, and in what format

## Also before week 5

Run one real PDF build from a draft, `pandoc` through `xelatex`, by 15 September. Week 3
owns this smoke build. The gate reads the final attachment back and checks it carries this
submission's sections and numbers, but it cannot catch a toolchain problem before a file
exists.

The human technical read happens on 25 September. Replace
`TECHNICAL-READ-PENDING` below with `TECHNICAL-READ-COMPLETE` only after opening the final
PDF and checking the title, team details, registration reference, figures and main design
claims. This fifth marker does not block the start of week 5. It blocks final staging.

## Status

Add each marker below on its own line as it is confirmed. Week 5 fails until the first four
are present, and final staging fails without the fifth.

REGISTRATION-PENDING
ELIGIBILITY-PENDING
ROSTER-PENDING
SENDER-PENDING
TECHNICAL-READ-PENDING
