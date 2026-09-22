# CycloProp: context for round 10, the verification pass

Written 23 September 2026. The submission goes to the organisers on 26 September, against a
27 September deadline. **Read this and you will not need to fetch anything.** Every official source
is offline under `reference/`, and the organiser record was pulled again on 23 September.

This replaces the 4 September version, which described the design before D70 and became one of
the findings of round 9. Round 9 ran on 23 September, scored the submission 60 out of 100, and
every one of its eight findings held up. Seven were fixed that night. This round checks the fixes.

## Where the authoritative sources live

| File | What it is |
| --- | --- |
| `reference/cycloprop-problem-statement.pdf` | The official problem statement. Byte identical to the live copy on 23 September |
| `reference/cycloprop-problem-statement.txt` | Plain text of the same |
| `reference/techfest-api-cycloprop.json` | The competition record on 26 August |
| `reference/techfest-api-cycloprop-4sep.json` | The same record on 4 September, kept beside the first |
| `context.md` | Requirements distilled from those. It outranks every other file here |

On 23 September, 25 of the record's 26 fields were unchanged from 4 September. The one that moved
is registrations, from 57 to 301, against 15 Stage 1 slots.

## What the competition asks for

**PUSHPAK Grand Challenge 2026**, MeitY funded, run by IIT Bombay. An indigenous **cycloidal rotor
propulsion module** for drone use, at least 10 N of thrust and a thrust to weight ratio strictly
above 2.5, with thrust vectoring demonstrated by kinematic and performance analysis. Stage 1 is a
preliminary design on paper, submitted by email to `pushpak_gc2026@aero.iitb.ac.in`.

Thrust to weight is measured on "the complete cyclorotor module, including rotor blades, frame,
pitch mechanism, motor, actuator, and associated mounting hardware". No battery and no airframe.

The seven required items, in order: concept and configuration; preliminary rotor sizing; blade
arrangement and pitch control; estimated thrust and power; estimated module weight and thrust to
weight; initial material and manufacturing approach; team capability and execution plan.

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

The problem statement attaches these to the final evaluation and publishes no separate Stage 1
rubric. Nothing published states a page limit or a file naming convention.

## The design as it stands

Every number is stored in `stage-1/design/numbers.json` and recomputed by gate. Nothing in that
file moved on 23 September; round 9's fixes were all to documents.

| | |
| --- | --- |
| Rotor | 110 mm radius, 290.4 mm span, 3 blades, NACA 0020, 72.6 mm chord, c/R 0.66 |
| Pitch | plus or minus 40 degrees, axis at 30 percent chord, four-bar per blade on a shared offset pivot |
| Transmission angle | 53.88 to 135.68 degrees, inside the 40 to 140 band at both ends, 44.32 worst folded |
| Side force | 9.078 degrees from the offset direction, 7.75 from the linkage and 1.33 from the aerodynamics |
| Operating point | 2337.04 rpm, chord Reynolds 130,296, solidity 0.3151 |
| Thrust | 17.0 N design, 16.1493 N on the low coefficient |
| Power | 339.7 W aerodynamic, 483.2 W at the motor, 518.0 W at the module including a 1.4118 W regulator loss |
| Drive | MN5006 KV450 on a 4.25 to 1 belt, 8S pack. Windings see 23.2293 V against 25.2 V for six cells charged |
| Controller | F411-WSE class board behind a 10.0 g step down regulator rated 42 V in, 12 V out |
| Mass | 687.91 g nominal, 775.74 g conservative, 34 budget lines |
| Thrust to weight | 2.5191 design, 2.3931 coefficient downside, 2.2339 mass downside, 2.1221 stacked |
| Closing mass | 117.26 g off the conservative column, a gate of 658.48 g |
| Cost | 68,830 INR |

**How the report now frames that result**, per D71: a preliminary nominal pass by 0.8 percent on
a mass estimate that is not accurate to 0.8 percent, with all three downside cases missing. The
2.0 floor this project set itself after its own 2.5 downside rule broke is gone from the
evaluator facing text. It stays in `tools/check.py` as a screen.

## What round 9 found and what was done

Round 9's audit is `stage-1/audit/codex-final.md`, committed at `59ad408`. The answer, finding by
finding, is `stage-1/audit/codex-round-9-response.md`.

| | Round 9 finding | Done, in which commit |
| --- | --- | --- |
| F1 | Item 7 is a template | Not done. Needs the team facts from a person |
| F2 | The email quotes pre-D70 results and a placeholder | `0e6a5e3`. Results current; sender name still a placeholder; format question moved to its own email |
| F3 | The criteria map claims all four thrust to weight cases pass | `93b1b60` |
| F4 | Stale kinematic, aerodynamic and power values in the attachment | `93b1b60`, `2b90454`, `36235d9` |
| F5 | The project's own margin contract was not met | `93b1b60`, stated in the report in those terms |
| F6 | The nominal pass is too thin for its mass evidence | `93b1b60`, the audit's suggested paragraph adapted |
| F7 | No usable reference list | `93b1b60`, eight references and a locator table |
| F8 | This file was stale | This file |

Beyond the listed findings, a near miss scan found rounded copies the D70 resync had missed
because it matched exact tokens: the whole configuration table in `01-configuration.md`, four
rows of the radius sweep in `02-rotor-sizing.md`, two stacked ratios in the report's own
comparison table, the gap to the 2.75 target in three files, and a "wins by 36 percent" where the
arithmetic says 23. All moved in `2b90454` and `93b1b60`.

## Repository shape

| Path | What it holds |
| --- | --- |
| `stage-1/submission/cycloprop-stage1.md` | The attachment source. 32 pages built |
| `stage-1/submission/cycloprop-stage1.pdf` | The built attachment, rebuilt 23 September |
| `stage-1/submission/email-draft.md` | The staged submission email. Never sent by an agent |
| `stage-1/organiser-email.md` | The staged format question, to go before the submission |
| `stage-1/design/01` to `09`, `evidence-ledger.md`, `numbers.json` | The design record |
| `stage-1/decisions.md` | 71 decisions. D67, D70 and D71 matter most here |
| `stage-1/human-gate.md` | Five markers. Four present, `TECHNICAL-READ-COMPLETE` outstanding |
| `tools/check.py` | 289 gates on the cumulative tree |
| `tools/test_gates.py` | 223 self-tests, each an attack the gates must catch or allow. Writes only to temporary directories |
| `tools/linkage.py`, `tools/structure.py`, `tools/figures.py` | The solvers and the figure renderer |

## Contracts worth knowing

- **Declarations match at the precision they are written.** `- key = 2.501` claims three decimals
  and is held to three. This changed on 23 September; it was a 2 percent tolerance before
- **Retired values.** `RETIRED_VALUES` in `check.py` lists every number this project published and
  superseded. No live document may quote one without an allow marker carrying a written reason.
  `decisions.md`, `journal.md`, `progress/` and `audit/` are outside it on purpose
- **Solver order** is `tools/linkage.py --write` then `tools/structure.py --write`, and
  `numbers.json` must reproduce byte for byte. Nothing in this round should need either
- **No em dashes or en dashes** anywhere in file prose

## What the gates cannot see

They recompute the physics and hold every declared number, but they read prose only for tokens.
A sentence can carry a current number and a false claim about it. That is how the criteria map
said "all clearing the limit" under a table showing three of four miss, with every gate green. A
person reading beside the data is still the only check on meaning.

Mass is the weak half and says so: 29 of 34 lines rest on a basis string rather than a drawn
section or a weighed part, and no gate can close that.

## Review history

Rounds 2 to 4 attacked the gates. Round 5 was goal based. Round 6 was external research. Round 7
asked whether the plan could be executed. A five pass review on 1 September raised 64 findings,
all closed. Round 8 on 4 September scored 62 and found the electrical interfaces, fixed as D70.
Round 9 on 23 September scored 60 and found the document errors above. This is round 10, and it
exists to check that round 9's fixes landed and broke nothing, three days before a person sends
the result.
