# Week 1: requirements and literature

Dates: 26 August to 1 September 2026. Executed 26 August, outside the loop, before the loop config existed.

**Two statements below were superseded later the same day by rounds 2 and 3 of review, and are left in place because this is a record of the week rather than a live document.** The 408 g budget is not confirmed as a fixed number; it is the ceiling at exactly 10 N and it moves with design thrust, so the current figure is 407 g at 10 N. And the conclusion that the module must be one larger rotor only rules out copying a published rotor five times, not every cluster. Current readings are in [../../context.md](../../context.md) and [../decisions.md](../decisions.md).

STATUS: WEEK-COMPLETE

## What the week was meant to produce

A parameter table built from published cyclorotor work, with geometry against measured thrust, replacing the table that had come from search summaries.

## What it actually produced

The literature work, plus a requirements document nobody had planned for, because the official problem statement turned out to exist.

**[../../context.md](../../context.md)** carries every requirement, quoted from the source. The Techfest competition page renders client side and gives a fetcher nothing, so the page had been read through summaries. The data actually sits at `https://techfest.org/api/compis/` as plain JSON, and the record for `compi_id == "cycloprop"` has a `probStatement` field pointing at a problem statement PDF. That PDF is saved at [../../reference/cycloprop-problem-statement.pdf](../../reference/cycloprop-problem-statement.pdf).

**[../literature.md](../literature.md)** carries the rebuilt parameter table. Four sources read in full, two recorded from summaries and marked as such.

## What the problem statement changed

- Stage 1 requires 7 items, not the 5 every document in this repo listed. Power, thrust-to-weight as a stated result, and a team capability and execution plan were all missing
- Thrust vectoring is a requirement and carries 15 percent. Nothing here had mentioned it
- The thrust-to-weight ratio is measured on the complete module, quoted directly, so the 408 g budget is confirmed and sizing is unblocked. This had been the one blocking open question
- Eight evaluation criteria, not nine. They sum to 100, so the PDF is right and the site FAQ is stale
- Stage 1 carries no money during the work. The 1 lakh arrives after results, to fund Stage 2. The contradiction recorded in the shared timeline was a misreading

## What the literature changed

- The old table was wrong in most rows. 700 rpm had no source, 24 rpm was junk, the chord-to-radius figures were two studies conflated, and "1.3 in radius" was a 1.3 inch chord
- The 95 W power anchor was low by about 60 percent. Two measured routes both give 152 to 161 W aerodynamic, so 230 to 250 W electrical
- Repeating a published MAV rotor to reach 10 N needs 485 g of rotor against a 408 g budget, so the module has to be one larger rotor
- Holding a fixed shape family at fixed thrust pins Reynolds near 100,000 whatever radius is chosen. That lands in the band the Texas A&M study covers
- Measured lateral force is comparable to vertical force, and Benedict's twin sat 30 degrees off vertical at its operating point

## Debts carried forward

- Three papers unread. The Texas A&M UAV-scale thesis is the only study in our Reynolds band and the repository refuses direct requests. Week 2 leans on a search summary of it, whose internal consistency checks out but which has not been opened
- The organiser email at [../organiser-email.md](../organiser-email.md) is now mostly answered by the problem statement and should be cut down or dropped
- Weekly hours and team size are still unknown, which is the input most likely to invalidate the schedule

## Gates

`python tools/check.py --week 1` exits 0.
