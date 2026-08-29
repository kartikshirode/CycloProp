# CycloProp: full context for a fresh reviewer

Written 29 August 2026. **Read this first and you will not need to fetch anything.** The
competition website is a JavaScript app that serves nothing to a fetcher, so everything
below was pulled once from the official sources and is kept in the repository. Do not spend
time re-fetching it.

## Where the authoritative sources live, all offline in this repo

| File | What it is |
| --- | --- |
| `reference/cycloprop-problem-statement.pdf` | The official problem statement, 12 pages |
| `reference/cycloprop-problem-statement.txt` | Plain text of the same |
| `reference/techfest-api-cycloprop.json` | The raw competition record from the Techfest API, carrying the about, structure, timeline, rules and FAQ fields |
| `context.md` | Requirements distilled from those, and the authority on what the competition wants |

For anyone who does need to refresh it later: the page at `techfest.org/competitions/cycloprop`
renders client side. The data is at `https://techfest.org/api/compis/`, a plain JSON list of
15 competitions; filter on `compi_id == "cycloprop"` and the `probStatement` field holds the
PDF URL.

## What the competition asks for

**PUSHPAK Grand Challenge 2026**, MeitY-funded, run by IIT Bombay. The CycloProp track wants
an indigenous **cycloidal rotor propulsion module** for drone use. The end goal is not a
prototype, it is a **build-ready design**. Stage 1 is preliminary design on paper, submitted
by email.

Hard targets:

| Parameter | Requirement |
| --- | --- |
| Thrust | At least 10 N |
| Thrust to weight | Strictly greater than 2.5 |
| Rotor type | Cycloidal, with blade pitch variation |
| Thrust vectoring | Demonstrated by kinematic and performance analysis |
| Design support | CAD and CAE supported |

**The definition that governs everything**, quoted from the problem statement: the thrust to
weight ratio is measured on "the complete cyclorotor module, including rotor blades, frame,
pitch mechanism, motor, actuator, and associated mounting hardware".

No battery, no avionics, no airframe are counted. Nothing can be pushed onto a vehicle to
make the ratio work, and nothing published measures a module on exactly that line.

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

Five criteria carry 15% each and four of those five are engineering analysis.
Manufacturability at 10% outweighs CAD quality at 5%.

### Dates

| Milestone | Date |
| --- | --- |
| Stage 1 deadline | on or before 27 September 2026 |
| Stage 1 results | 2 October 2026 |
| Stage 2 window | 3 October to 2 December 2026 |
| Finale at Techfest | 16 to 18 December 2026 |

We submit 26 September. Today is 29 August, so 28 days remain.

One clause worth knowing: anyone attached to the PUSHPAK Project, the Drone Centre, or the
organising and host institutions is ineligible, and it disqualifies an entire team at any
stage **including after results are announced**.

## Because the requirement is "at least" 10 N, thrust is a free variable

The two targets together set a mass ceiling that moves with design thrust. Floors rounded
down, because the inequality is strict:

| Design thrust | Mass ceiling for T/W > 2.5 |
| --- | --- |
| 10 N | 407 g |
| 12 N | 489 g |
| 13 N | 530 g |
| 15 N | 611 g |

Raising thrust is a real lever and not a free one. Within a fixed shape family at fixed
radius, 10 N to 13 N buys 30 percent more mass ceiling and costs 14 percent more rpm, 30
percent more centrifugal load and 48 percent more ideal power.

## Where the project actually is

**Week 1 of 5 is done.** It produced the requirements document and a literature rebuild from
primary sources. **No engineering has been done yet**: 0 of 78 parameters in
`stage-1/design/numbers.json` are filled, and none of the 9 design documents exist.

One person is doing this, solo, alongside another project.

The human tasks, registration and the eligibility check and the roster and naming who sends,
are all outstanding and are tracked in `stage-1/human-gate.md` with four status markers. They
hard-block week 5.

## The central engineering problem

Re-cut onto the competition's module boundary, the best published design gives a module
thrust to weight of **2.13** against the 2.5 required, so the gap is about 17 percent.

That number comes from Runco and Benedict's 70 g quad-cyclocopter, 2023: 8.2 g of module per
rotor carrying 16.9 gf by design and a flight-demonstrated 17.5 gf. It is also the **least**
optimistic of the available benchmarks, because its 8.2 g already includes the servo the
module boundary requires, while the older Sirohi figure excludes an entire electronics and
servos line. Benedict 2010 and Sirohi 2007 give 1.69 and 1.80 on the same boundary and are
correct for those designs; they were simply not the best point available.

The published record settles one half of the argument against us: blade weight per unit
thrust is **scale invariant** and blade stress rises monotonically under geometric
similarity, so scale buys aerodynamic efficiency and nothing on blade mass. What remains is
fixed masses amortising over roughly 5 times the thrust, plus materials.

The highest-risk assumption is a blade-area thrust coefficient of **0.607**, taken from a
single measured point on a 4-blade NACA 0010 rotor at c/R 0.433 and Reynolds near 35,000, and
applied to a 3-blade NACA 0020 family at c/R 0.66 and Reynolds near 100,000. Blade count,
airfoil, solidity and Reynolds all move at once. The Reynolds part of the transfer is
defensible; the configuration part is not de-risked by anything.

## How the work is executed and gated

The plan runs one week per tick under a supervised loop. A fresh agent does the week, then a
supervisor runs mechanical gates in its own shell and never trusts the agent's self-report.
The gate script is `tools/check.py`, with 68 self-tests in `tools/test_gates.py`.

Two properties matter more than the gate list:

**Hard limits apply to recomputed values, never stored ones.** Thrust comes from the
geometry, weight from the mass lines, T/W from both. An earlier version compared stored
headline numbers against the limits within a 2 percent tolerance, which let a 1.9 percent
overstatement of thrust and a 1.9 percent understatement of mass compound into a design that
missed both targets and passed everything.

**One gate asks whether the design could exist, and the rest only check self-consistency.**
That one is the momentum bound: aerodynamic power must clear the ideal induced power over a
declared area no larger than the projected 2R times span, with a figure of merit between 0.20
and 0.75. Before it existed the gates certified 13.5 N of thrust produced by 1 W, with every
stored number in perfect agreement.

## The fourteen frozen decisions

Full text in `stage-1/decisions.md`. Treat these as settled ground rather than open
questions, and challenge one only with a reason.

| | Decision |
| --- | --- |
| D1 | `context.md` outranks the earlier documents |
| D2 | The module is one larger rotor, not a cluster. **Provisional**, weakened by D8, and week 2 must re-test it |
| D3 | Numbers live in one file and prose cites them |
| D4 | No CAD at Stage 1 |
| D5 | The submission email is never sent by an agent |
| D6 | Design thrust is a free variable above 10 N |
| D7 | Hard limits apply to recomputed values, never stored ones |
| D8 | The module T/W gap is the project's main risk |
| D9 | A paper design has to clear a physical bound, not only its own arithmetic |
| D10 | Design thrust is frozen as a table in week 2, not reopened in week 4 |
| D11 | The T/W case rests on fixed masses, not on blade scaling |
| D12 | The borrowed coefficient is valid only inside the solidity band it was measured in |
| D13 | The feasibility case starts from 2.1, not from 1.69 |
| D14 | The three-point mass series bounds the argument, it does not fit a law |

## What is open, and honestly

- **Week H is outstanding** and due within days. Eligibility first
- **Three papers are identified but not read.** Heimerl et al., VFS 77th Forum, would convert
  the blade load factor and the side force angle from simulated to measured. Kellen 2019
  would give a measured thrust coefficient in our own Reynolds band and retire most of the
  coefficient risk. Ramsey 2022 would give a 25 kg mass breakdown. All three sit behind a
  Cloudflare JavaScript challenge, so they need a human with a browser
- **The 17 percent gap is argued, not proven.** Week 2 either closes it or reports that it
  cannot, and geometry does not freeze unless a conservative case clears both targets on its
  own
- **Two allocation choices are undecided**: whether ESCs count as module hardware, and what
  share of structure counts as mounting. Both move the benchmark

## Review history, so a fresh round does not repeat one

Six rounds so far. Rounds 2 to 4 attacked the gates and found ways to fool them, all closed.
Round 5 was a goal-based audit and found 8 real issues including 2 blockers, all closed. Round
6 was external technical research; its central finding was wrong on arithmetic, was caught,
and the corrected version reset the benchmark from 1.69 to 2.13.

The gates have been mined hard. What has never been reviewed is whether an agent can actually
execute this plan and produce something an IIT Bombay evaluator would believe.
