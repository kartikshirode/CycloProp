# Week 2: configuration, sizing, thrust, power, feasibility

**STATUS: BLOCKED.** The conservative case does not clear thrust to weight 2.5, so geometry
does not freeze. This file is not marked week-complete on purpose, and the week 2 gate fails
on exactly one line, which is the line that carries the decision.

Run 2 September 2026 against the config at `.claude/weekly-loop.md`. See D24 on why that one
and not the Codex file.

## What the week was meant to produce

Required Stage 1 items 1, 2 and 4, plus the feasibility envelope that decides whether the
design closes at all. Seven work packages: evidence ledger and selection rules, common
candidates, the thrust and power model with coefficient scenarios, the drive and blade
section, the coupled comparison, a frozen design point, and the audit.

## What it actually produced

Everything except the freeze.

- `stage-1/design/evidence-ledger.md`, 14 numbered evidence rows with class, source, exact
  basis, area convention, source geometry, source Reynolds number and use, plus the selection
  rules written before any candidate was scored
- `stage-1/design/01-configuration.md`, the single rotor against redesigned 2 and 3 rotor
  clusters on one common model
- `stage-1/design/02-rotor-sizing.md`, shape family, coefficient recompute, blade section and
  stiffness closure, the radius sweep, the mass envelope and the verdict
- `stage-1/design/04-thrust-and-power.md`, thrust, the 36 point azimuthal load distribution,
  power closed three ways, the named drive on its continuous rating, and the sensitivity table
- `stage-1/design/numbers.json`, the full week 2 block: 26 performance scalars, 7 geometry, 3
  operating, 3 efficiency, plus `power_by_radius` at 5 radii, 3 configuration candidates, 4
  coefficient scenarios, 36 azimuthal load rows, 3 drive candidates, 11 mass envelope lines
  and 4 sensitivity rows
- D18 to D24 in `stage-1/decisions.md`

## The result

| | Value | Target | Verdict |
| --- | --- | --- | --- |
| conservative thrust to weight | 2.389 | above 2.5 | miss by 32 g of module mass |
| against the internal target | 2.389 | 2.75 | miss by 95 g |
| nominal thrust to weight | 3.318 | no target | 56 percent above the best published module |
| nominal thrust | 20.0 N | at or above 10 N | clears |
| conservative thrust | 17.0 N | at or above 10 N | clears |
| figure of merit | 0.60 | 0.20 to 0.75 | clears, and matches what Kellen measured |
| two power routes | 10.5 percent apart | within 35 percent | clears |
| solidity | 0.3151 | 0.30 to 0.40 | clears |

Candidate geometry, not frozen: 115 mm radius, 75.9 mm chord, 303.6 mm span, 3 blades, NACA
0020, plus or minus 40 degrees, 2319 rpm, chord Reynolds 141,000. Second candidate radius
carried forward is 125 mm, which costs 0.09 of conservative thrust to weight and buys 43 W and
356 rpm.

## Why it does not close, in one paragraph

The conservative case multiplies two independent penalties. Thrust drops to 85 percent because
the coefficient is transferred across a change of blade count, airfoil and chord ratio at
once. Mass rises to 118 percent because the structural lines come from assumed sections rather
than weighed parts. 0.85 over 1.18 is 0.72, so a nominal thrust to weight of 3.82 is needed to
put the conservative case at 2.75, and 3.47 to put it at 2.5. The best published module on the
same boundary is Runco at 2.13. We reach 3.318 nominal on fixed-mass amortisation, which is
already a 56 percent improvement on the record, and it is not enough.

## The fallbacks, worked in the plan's order

1. **Higher precomputed thrust row.** Swept 12 to 26 N. Conservative thrust to weight rises
   with thrust because the geometry-scaled mass lines do not move, then turns over at 20 N
   when the drive shortlist runs out at 555 W continuous. Peak 2.389.
2. **Along the coupled radius table.** Swept 70 to 150 mm. Bounded below by the two power
   routes diverging past 35 percent and by the drive shortlist, bounded above by blade and
   frame mass growth overtaking the motor saving. Peak at 115 mm, same 2.389.
3. **Reject duplicated hardware, return to the single rotor branch.** Already there. The
   cluster comparison went the other way: 1.795 for two rotors, 1.434 for three, on
   assumptions set in the cluster's favour throughout. Nothing to recover here.
4. **Revisit the shape family.** Swept chord ratio 0.63 to 0.836 and blade aspect ratio 3 to
   6, holding solidity inside the measured band. Best is 2.481 at aspect ratio 6, still short
   of 2.5, and it is not bankable because it leaves the family the coefficient was measured
   in. Buying a number by weakening the evidence behind it is not a fallback.

None closed it. Reporting rather than trimming, per the blocked trigger.

## What would close it

Ranked by leverage, and the first one is cheap.

1. **Kellen's measured thrust coefficient.** If it lands at or above the transferred value for
   this shape family in this Reynolds band, the 10 percent configuration-transfer allowance
   retires and the haircut drops from 15 percent to 5. Conservative thrust to weight moves to
   roughly 2.68. That clears the hard limit and still sits under the 2.75 internal target, so
   it converts a blocked week into a red one needing a margin decision. See D23
2. **A decision on the conservative mass allowance.** At a uniform 10 percent growth instead of
   the line by line 15 to 25 percent used here, the conservative case reaches 2.564 and clears
   the hard limit. That is a judgement about how much a paper mass estimate grows, and it
   belongs to a person, not to the agent that wants the number
3. **Weighed hardware.** The three softest lines in the envelope are the main shaft torque
   allowance at 18 g per Nm, the actuator controller and wiring at 25 g, and fasteners and
   bonded joints at 22 g. All three are round allowances rather than build-ups, and together
   they carry about 75 g of the 725 g conservative total
4. **Ramsey 2022.** A 25 kg subsystem mass table would give a second real anchor for the
   structural lines. Currently there is one, Runco, at four orders of magnitude smaller

## What changed

- **D2 is no longer provisional.** The cluster comparison it asked for has been run on a
  common boundary and the single rotor wins by 33 percent on conservative thrust to weight
- **The 0.607 coefficient is now 0.6055 and recomputed rather than quoted.** Same number to a
  quarter of a percent, and now reproducible from Benedict's published figures in one line
- **The two open allocations are closed.** ESCs are module hardware and mounting counts in
  full, both settled against us, both settled before scoring
- **The low coefficient has a construction.** 5 percent flexibility sized against a computed
  section stiffness plus 10 percent configuration transfer, added not compounded
- **Kellen has been reclassified** from supporting evidence to a hard dependency for the
  freeze decision

## Debts carried forward

| # | Debt | Owner |
| --- | --- | --- |
| 1 | Two files each claim to be the loop execution contract. `stage-1/plan.md` names `.codex/weekly-loop.md`; this tick ran against `.claude/weekly-loop.md` on the launching human's instruction. The plan was deliberately not edited. See D24 | human |
| 2 | Motor and ESC figures came from supplier listings this week rather than manufacturer datasheet PDFs. Week 4 confirms each before the submission quotes it | week 4 |
| 3 | The azimuthal model gives a peak to mean blade load of 2.37 against a published 3 to 4. The model has no wake return, no shed vorticity and no dynamic stall overshoot, so it under-predicts the peak. Week 4 uses 4.0 regardless, per D16 | week 3 and 4 |
| 4 | The 28 degree stall cap in the azimuthal model is stated, not measured. Heimerl would replace it | blocked on a paper |
| 5 | Side force is zero in the azimuthal model by construction, because the prescribed schedule has no phase offset. Week 3 reruns it against the solved linkage | week 3 |
| 6 | Three envelope lines are round allowances rather than build-ups: shaft torque allowance, controller and wiring, fasteners and joints | week 4 |
| 7 | The blade spar is sized geometrically at 0.12 chord diameter with a 0.5 mm wall. Week 4 sizes it against centrifugal load, which at 2319 rpm is the load that actually governs | week 4 |
| 8 | `stage-1/organiser-email.md` is still mostly answered by the problem statement and should be cut down or dropped | human |

## Week H gap

All four blocking markers in `stage-1/human-gate.md` are still PENDING, along with the fifth:
`REGISTRATION-PENDING`, `ELIGIBILITY-PENDING`, `ROSTER-PENDING`, `SENDER-PENDING`,
`TECHNICAL-READ-PENDING`. Week H is advisory before week 2 and the engineering genuinely did
not depend on the roster, so week 2 ran and this records the gap. It becomes a hard block on
week 5. The eligibility check is still the one worth doing first, because the clause
disqualifies a whole team at any stage including after results.

## Evidence gap: three unread papers

All three sit behind the same Cloudflare JavaScript challenge on the Texas A&M repository. A
user agent string does not pass it; a real browser passes it in about two seconds.

- **Kellen 2019**, handle 1969.1/184958, item `a4c62d38-3778-44f4-b398-cdcba283fa06`. Wanted:
  the measured blade-area thrust coefficient, power loading in N/W, per-rotor thrust and rpm at
  the optimum. This is the one that decides the week. See D23
- **Heimerl, Halder, Benedict et al.**, VFS 77th Forum, cyclorotor in forward flight. Wanted:
  the measured blade peak to mean load factor and the side force angle against pitch offset.
  Answers debts 3 and 4 and feeds week 3's vectoring section
- **Ramsey 2022**, handle 1969.1/198531, item `692efcdd-c56a-4c7a-b507-f3e673986b51`. Wanted:
  the 25 kg subsystem mass table and any blade mass or deflection figures

Week 2 ran without all three and disclosed it, which is what the config asks for supporting
evidence. Kellen has stopped being supporting evidence.

## Gate state at the end of the week

```
python tools/check.py --week 2   1 failure, the T/W decision line
python tools/check.py --global   pass
python tools/test_gates.py       77 of 77 self-tests behaved as expected
```

The single failure reads:

    FAIL  week2: conservative mass and thrust still clear T/W 2.5
          T/W 2.389 at 17.00 N and 725 g

Every other gate passes, including all four feasibility gates: the momentum floor with a
figure of merit of 0.60, the second power route agreeing to 10.5 percent, the four row
sensitivity table reproducing each ceiling and ideal power, and solidity at 0.3151 inside the
measured band with the low coefficient answering a stated deflection loss.

`tools/check.py` was not modified. No tolerance, bound or limit was touched.

## What week 3 needs to know

Week 3 cannot start on a frozen geometry, because there is not one. Two options, and the
choice is a person's:

1. Somebody pulls Kellen, the coefficient comes back at or above 0.6055, week 2 reruns in
   about an hour on the new evidence and week 3 starts on a red but compliant point
2. Somebody rules on the conservative mass allowance, which either closes it at 2.564 or
   confirms the block

If week 3 has to start anyway to protect the calendar, start it on the 115 mm candidate and
accept that a later geometry change costs a week 3 rerun, because link lengths, offset
geometry, the pitch schedule and gearing all move with radius. The second candidate at 125 mm
exists for exactly that reason and it is insurance, not a free option.
