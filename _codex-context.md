# CycloProp: full context for the final audit

Written 4 September 2026. **Read this and you will not need to fetch anything.** The competition
website is a JavaScript app that serves nothing to a fetcher, so every official source was pulled
once and lives in the repository under `reference/`.

This replaces the 29 August version, which described a project where 0 of 78 parameters were
filled and none of the design documents existed. All of that is stale now. The engineering is
done, the submission is built, and this round is the last look before a person sends it.

## Where the authoritative sources live, all offline in this repo

| File | What it is |
| --- | --- |
| `reference/cycloprop-problem-statement.pdf` | The official problem statement, 12 pages |
| `reference/cycloprop-problem-statement.txt` | Plain text of the same |
| `reference/techfest-api-cycloprop.json` | The raw competition record from the Techfest API, carrying about, structure, timeline, rules and FAQ |
| `context.md` | Requirements distilled from those. It is the authority on what the competition wants and outranks every other file here |

Anyone refreshing this later: `techfest.org/competitions/cycloprop` renders client side. The data
is at `https://techfest.org/api/compis/`, a plain JSON list of 15 competitions. Filter on
`compi_id == "cycloprop"` and the `probStatement` field holds the PDF URL.

## What the competition asks for

**PUSHPAK Grand Challenge 2026**, MeitY funded, run by IIT Bombay. The CycloProp track wants an
indigenous **cycloidal rotor propulsion module** for drone use. The end goal is a build ready
design rather than a prototype. Stage 1 is preliminary design on paper, submitted by email.

| Parameter | Requirement |
| --- | --- |
| Thrust | At least 10 N |
| Thrust to weight | Strictly greater than 2.5 |
| Rotor type | Cycloidal, with blade pitch variation |
| Thrust vectoring | Demonstrated by kinematic and performance analysis |
| Design support | CAD and CAE supported |

**The definition that governs everything**, quoted: the thrust to weight ratio is measured on
"the complete cyclorotor module, including rotor blades, frame, pitch mechanism, motor, actuator,
and associated mounting hardware". No battery, no avionics, no airframe. Nothing can be pushed
onto a vehicle to make the ratio work, and nothing published measures a module on exactly that
line.

### The seven required Stage 1 items, quoted

> 1. Cyclorotor concept and configuration.
> 2. Preliminary rotor sizing.
> 3. Blade arrangement and pitch-control concept.
> 4. Estimated thrust and power requirement.
> 5. Estimated module weight and thrust-to-weight ratio.
> 6. Initial material and manufacturing approach.
> 7. Team capability and execution plan.

### The eight evaluation criteria, summing to 100

| Criterion | Weight |
| --- | --- |
| Feasibility of achieving 10 N thrust | 15% |
| Feasibility of achieving thrust-to-weight ratio greater than 2.5 | 15% |
| Kinematic design of blade-pitch and thrust-vectoring mechanism | 15% |
| Aerodynamic analysis or simulation quality | 15% |
| Structural design and strength assessment | 15% |
| Manufacturability, material selection, and cost realism | 10% |
| CAD quality, integration readiness, and packaging | 5% |
| Presentation, viva, and technical clarity | 10% |

Four of the five 15% criteria are engineering analysis. Manufacturability at 10% outweighs CAD
quality at 5%, and CAD is explicitly not a Stage 1 deliverable, which is a tension the submission
confronts in writing rather than assuming away.

### Dates

| Milestone | Date |
| --- | --- |
| Stage 1 deadline | on or before 27 September 2026 |
| Stage 1 results | 2 October 2026 |
| Stage 2 window | 3 October to 2 December 2026 |
| Finale at Techfest | 16 to 18 December 2026 |

We send on 26 September. Today is 4 September, so 22 days remain against work measured in hours.
The schedule is not the risk any more.

One clause worth knowing: anyone attached to the PUSHPAK Project, the Drone Centre, or the
organising and host institutions is ineligible, and it disqualifies a whole team at any stage
**including after results are announced**. That check is done.

## Where the project actually is

Weeks 1 to 4 are complete, each with a progress file and an audit file. Week 5 produced
everything that does not need a person: the assembled submission, the criteria map, the claims
and risk table, the hostile viva pass, seven figures, the built PDF and a staged email that no
agent will ever send. A five pass review on 1 September raised 64 findings and a six phase fix
plan closed 63. The re-audit that followed is at `stage-1/audit/phase-6-reaudit.md`.

Verify the baseline yourself before reading anything else. These are the current outputs:

```
python tools/check.py --all      ->  All gates passed.          (279 PASS)
python tools/check.py --week 5   ->  FAILED: 1 gate(s)          (308 PASS, the human gate)
python tools/test_gates.py       ->  All 212 gate self-tests behaved as expected.
```

The one failure is correct, and it is the only thing between here and a sendable submission.
`stage-1/human-gate.md` carries five status markers. Registration and eligibility are confirmed
in the file. Roster and sender were confirmed by the human on 4 September and those two marker
lines are his to add; the gate stays red until he adds them. The technical read is calendared for
25 September. **No agent may write any of those markers, whatever it finds.**

## The design as it stands

Every number below is stored in `stage-1/design/numbers.json`, 1,258 leaf values across 22
sections, and recomputed by gate rather than proofread.

| | |
| --- | --- |
| Rotor | 110 mm radius frozen, 290.4 mm span, 3 blades, NACA 0020, chord 72.6 mm at c/R 0.66 |
| Pitch | plus or minus 40 degrees, axis at 30 percent chord, four-bar linkage, offset controlled vectoring |
| Operating point | 2337.04 rpm, tip speed 26.92 m/s, chord Reynolds 130,296, solidity 0.3151 |
| Thrust | 17.0 N design, 16.15 N on the low coefficient case |
| Coefficient | blade area C_T 0.6055, low case 0.5752 |
| Power | 339.7 W aerodynamic, 483.2 W at the motor terminals, 516.6 W at the module |
| Figure of merit | 0.5215 |
| Drive | T-Motor Antigravity MN5006 KV450, 106 g, 4.25:1 belt on a 68 tooth rotor pulley, 8S pack |
| Drive margins | 483.2 W of 520 W continuous, 19.29 A of 20.8 A, 0.3902 of 0.4414 Nm, 9932 of 12799 rpm |
| Mass | 677.91 g nominal, 763.24 g conservative |
| Thrust to weight | 2.5563 design, 2.1569 stacked worst case |
| Cost | 67,930 INR, longest lead 4 weeks |

The drive binds on **power**, at 93 percent of the continuous rating. It does not fit on 6S at
any belt ratio, because the mechanical output a motor can make is the speed rule times the loaded
pack voltage times the continuous current, and KV cancels out of that product. That is why the
pack interface is 8S, and it is also what caused the one open electrical item below.

**The downside cases are the part to read.** The design case clears 2.5. The coefficient downside
gives 2.4284, the mass downside 2.2705 and the stacked case 2.1569, all under the requirement and
all above a declared floor of 2.0. The submission publishes 104.76 g as the mass that would have
to come out to close the stacked case, rather than claiming the stacked case passes. Whether that
is honesty an evaluator rewards or a gap an evaluator punishes is a fair thing for this round to
have an opinion about.

## The central engineering problem

Re-cut onto the competition's module boundary, the best published design gives a module thrust to
weight of **2.13** against the 2.5 required. That comes from Runco and Benedict's 70 g
quad-cyclocopter, 2023, and it is the least optimistic of the available benchmarks, because its
8.2 g per rotor already includes the servo the boundary demands. Benedict 2010 and Sirohi 2007
give 1.69 and 1.80 on the same boundary.

The published record settles half the argument against us. Blade weight per unit thrust is scale
invariant and blade stress rises monotonically under geometric similarity, so scale buys
aerodynamic efficiency and nothing on blade mass. What remains is fixed masses amortising over
roughly 5 times the thrust, plus materials.

**The highest risk assumption is still the coefficient transfer.** The blade area thrust
coefficient of 0.6055 comes from measured points on a rotor at a different blade count, airfoil,
solidity and Reynolds. The Reynolds part of that transfer is defensible. The configuration part
is not de-risked by anything, and no CFD and no wind tunnel sits behind it. A hostile examiner
starts here.

## How the repository is shaped

| Path | What it holds |
| --- | --- |
| `context.md` | The requirements authority |
| `handoff.md` | Where a fresh session starts, and the current state summary |
| `stage-1/plan.md` | The week by week execution plan, one half of what this round audits against |
| `stage-1/decisions.md` | 69 numbered frozen decisions. Superseded ones are kept rather than edited |
| `stage-1/journal.md` | Session by session record |
| `stage-1/literature.md` | 15 sources, the verified parameter table, the published mass breakdowns |
| `stage-1/design/01 to 09` | The nine design documents |
| `stage-1/design/numbers.json` | Every published number, written only by the solvers |
| `stage-1/design/evidence-ledger.md` | What every headline claim rests on |
| `stage-1/submission/cycloprop-stage1.md` | The attachment, 12,217 words |
| `stage-1/submission/cycloprop-stage1.pdf` | 30 pages, 7 embedded figures, pandoc through xelatex |
| `stage-1/submission/figures/` | Seven vector PDFs plus `manifest.json`, all rendered from `numbers.json` |
| `stage-1/submission/email-draft.md` | Staged, never sent |
| `stage-1/human-gate.md` | The five human markers |
| `stage-1/progress/`, `stage-1/audit/` | Week records and audits, plus `full-review.md` and `phase-6-reaudit.md` |
| `tools/check.py` | 3,593 lines of gates |
| `tools/test_gates.py` | 3,392 lines, 212 self-tests, each an attack the gates have to catch or allow |
| `tools/linkage.py`, `tools/structure.py` | The solvers that write `numbers.json` |
| `tools/figures.py` | Renders the seven figures, importing the solvers so geometry is never redrawn |

## Contracts that are easy to break by accident

- **Solver order.** `python tools/linkage.py --write` then `python tools/structure.py --write`.
  Running them the other way round, or hand editing `numbers.json`, breaks the byte identity self
  test. The file is written with `indent=2`, `ensure_ascii=False`, a trailing newline and Unix
  line endings, and it has to reproduce byte for byte.
- **Prose cites, never states.** Design documents carry a `## Numbers used` block and the gates
  match every declared value against `numbers.json` at a 2 percent display tolerance.
- **The untraced number ratchet.** `DESIGN_UNTRACED_CEILING` is one way. It can fall and it
  cannot grow, so new prose quoting a number from nowhere fails the tree.
- **Allow markers.** A deliberate near miss carries an allow comment on its line and the reason
  has to be a real reason. That mechanism exists so nobody tunes a threshold until the tree goes
  green.
- **No em dashes or en dashes anywhere in file prose.** A gate enforces it.

## What the gates hold, and what they cannot

Thrust, power and the structural margins are recomputed from geometry on every run and refuse to
be flattered. An auditor inflating the coefficient by 30 percent was caught by four independent
gates at once. One gate asks whether the design could exist at all rather than whether it agrees
with itself: aerodynamic power has to clear the ideal induced power over a declared area no
larger than the projected 2R times span, at a figure of merit between 0.20 and 0.75.

Mass is the weak half and the project says so in writing. Four blade lines are recomputed from
the section and the moduli, the motor line is pinned to the selected drive's catalogue mass, and
per blade mass follows from the blade budget and the blade count. The other 29 lines rest on a
basis string, a self consistency band between two lists the same author writes, and a growth
rule. A careful consistent 0.80 scaling of the non-blade lines fails 11 gates, and all 11 are
documents quoting the old number rather than physics. That is finding A5, and it is not closable
by a gate whose author also writes the data.

## The 69 decisions, and which ones carry this round

Full text in `stage-1/decisions.md`. Treat them as settled ground and challenge one only with a
reason.

- **D67** moved the design point from 18 N to 17 N and the pack from 6S to 8S, after the figure
  of merit was found to be read inconsistently with the thrust coefficient
- **D68** is the document pass that followed D67, and **D69** the figures plus the four errors
  drawing them exposed
- **D7** hard limits apply to recomputed values, never stored ones
- **D9** a paper design has to clear a physical bound, not only its own arithmetic
- **D11** the T/W case rests on fixed masses amortising, not on blade scaling
- **D12** the borrowed coefficient is valid only inside the solidity band it was measured in
- **D47** read this before touching any mass number
- **D5** the submission email is never sent by an agent

## What is open, honestly

1. **The mass case, finding A5.** Described above. Stage 2 closes it with a drawn section per
   line or a weighed part, and nothing else does.
2. **The pitch offset controller cannot take the declared pack.** The F411-WSE class board is
   rated 6 to 30 V and 8S reaches 33.6 V charged. It is written as an open item in
   `03-pitch-and-vectoring.md` and `09-packaging-and-integration.md`, with no part drawn and no
   mass line carrying a step-down. D67 caused it and D67 did not chase it. This is the only
   genuine engineering hole left and it costs a few grams the T/W case can absorb.
3. **R50, nobody has re-checked the organiser's official channels** between the 26 August
   requirements snapshot and the send date, and the problem statement reserves the right to
   change any stage. It needs a person with a browser.
4. **Three papers are identified and unread**, all behind a Cloudflare challenge. Heimerl et al.,
   VFS 77th Forum, would convert the blade peak to mean load factor and the side force angle from
   simulated to measured. Kellen 2019 would give a measured coefficient inside our own Reynolds
   band and retire most of the transfer risk. Ramsey 2022 would give a 25 kg mass breakdown.
5. **The attachment runs 30 pages** against a 15 page target this project set for itself when no
   organiser limit was published. No organiser limit exists. The question rides at the end of the
   staged email.

## Review history, so this round does not repeat one

Rounds 2 to 4 attacked the gates and found ways to fool them, all closed. Round 5 was a goal
based audit, 8 issues including 2 blockers, all closed. Round 6 was external technical research
whose central finding was wrong on arithmetic, was caught, and reset the benchmark from 1.69 to
2.13. Round 7 asked whether an agent could execute the plan at all. The 1 September five pass
review raised 64 findings and six fix phases closed 63.

The gates have been mined hard across four rounds, and the arithmetic has been independently
re-derived twice, roughly sixty quantities each time, reproducing to five or six figures. What
has never been reviewed is the finished thing as a whole, against the plan that promised it and
against what IIT Bombay actually asked for.
