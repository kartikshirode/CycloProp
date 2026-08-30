# Week 2: configuration, sizing, thrust, power, feasibility

**STATUS: BLOCKED.** The conservative case does not clear thrust to weight 2.5, so geometry
does not freeze. This file is not marked week-complete on purpose, and the week 2 gate fails on
exactly one line, which is the line that carries the decision.

Run 2 September 2026 against the config at `.claude/weekly-loop.md`. See D24 on why that one
and not the Codex file.

## What the week was meant to produce

Required Stage 1 items 1, 2 and 4, plus the feasibility envelope that decides whether the
design closes at all. Seven work packages: evidence ledger and selection rules, common
candidates, the thrust and power model with coefficient scenarios, the drive and blade section,
the coupled comparison, a frozen design point, and the audit.

## What it actually produced

Everything except the freeze.

- `stage-1/design/evidence-ledger.md`, 16 numbered evidence rows with class, source, exact
  basis, area convention, source geometry, source Reynolds number and use, plus the selection
  rules written before any candidate was scored
- `stage-1/design/01-configuration.md`, the single rotor against redesigned 2 and 3 rotor
  clusters on one common model, with the packaging rule stated and the cluster mass build-up
  written out
- `stage-1/design/02-rotor-sizing.md`, shape family, coefficient recompute, blade section and
  stiffness closure, the radius sweep, the mass envelope and the verdict
- `stage-1/design/04-thrust-and-power.md`, thrust, the 36 point azimuthal load distribution,
  power closed three ways, the named drive on a derated continuous rating, and the sensitivity
  table
- `stage-1/design/numbers.json`, the full week 2 block: 24 performance scalars, 7 geometry, 3
  operating, 3 efficiency, plus `power_by_radius` at 5 radii, 3 configuration candidates, 4
  coefficient scenarios, 36 azimuthal load rows, 5 drive candidates, 13 mass envelope lines and
  4 sensitivity rows
- Four new gates in `tools/check.py` with 12 matching self-tests, which the audit asked for
- D18 to D27 in `stage-1/decisions.md`
- `stage-1/audit/week-2.md`, 18 findings, 15 fixed and 3 carried as debts

## The result

| | Value | Target | Verdict |
| --- | --- | --- | --- |
| conservative thrust to weight | 2.252 | above 2.5 | miss by 69 g of module mass |
| against the internal target | 2.252 | 2.75 | miss by 125 g |
| nominal thrust to weight | 3.163 | none | 49 percent above the best published module |
| nominal thrust | 18.0 N | at or above 10 N | clears |
| conservative thrust | 15.30 N | at or above 10 N | clears |
| figure of merit | 0.60 | 0.20 to 0.75 | clears, and matches what Kellen reports |
| two power routes | 9.8 percent apart | within 35 percent | clears |
| solidity | 0.3151 | 0.30 to 0.40 | clears |
| chord Reynolds | 134,000 | inside 10,000 to 100,000 for the transfer | **fails, and cannot pass. See D25** |

Candidate geometry, not frozen: 110 mm radius, 72.6 mm chord, 290.4 mm span, 3 blades, NACA
0020, plus or minus 40 degrees, 2405 rpm. Second candidate radius carried forward is 120 mm,
which costs 0.12 of conservative thrust to weight and buys 38 W and 384 rpm.

## Why it does not close, in one paragraph

The conservative case multiplies two independent penalties. Thrust drops to 85 percent because
the coefficient is transferred across a change of blade count, airfoil and chord ratio at once,
and now across a Reynolds extrapolation as well. Mass rises to 119 percent because the
structural lines come from assumed sections rather than weighed parts. 0.85 over 1.19 is 0.71,
so a nominal thrust to weight of 3.86 is needed to put the conservative case at 2.75, and 3.51
to put it at 2.5. The best published module on the same boundary is Runco at 2.13. This design
reaches 3.163 nominal, already a 49 percent improvement on the record, and it is not enough.

## The fallbacks, worked in the plan's order

**1. Higher precomputed thrust row.** Swept 13 to 24 N. Conservative thrust to weight rises with
thrust because the geometry-scaled mass lines do not move, then turns over when the drive runs
out.

| Design thrust | Best radius | Conservative T/W |
| --- | --- | --- |
| 13 N | 80 mm | 1.949 |
| 14 N | 80 mm | 2.088 |
| 16 N | 100 mm | 2.134 |
| 18 N | 110 mm | **2.252** |
| 20 N | 135 mm | 2.157 |
| 22 N | 155 mm | 2.094 |
| 24 N | 175 mm | 2.012 |

**2. Along the coupled radius table.** Swept 75 to 200 mm at each thrust. At 18 N:

| Radius | Motor input | Drive fits | Conservative T/W |
| --- | --- | --- | --- |
| 100 mm | 503 W | no | 2.376 |
| 110 mm | 458 W | yes, 3.5 to 1 | **2.252** |
| 120 mm | 419 W | yes, 4.0 to 1 | 2.134 |
| 130 mm | 387 W | yes, 4.5 to 1 | 2.019 |
| 140 mm | 360 W | yes, 4.5 to 1 | 1.909 |

**3. Reject duplicated hardware, return to the single rotor branch.** Already there. The cluster
comparison went the other way: 1.659 for two rotors and 1.323 for three, on assumptions set in
the cluster's favour throughout. Nothing to recover.

**4. Revisit the shape family.** Swept chord ratio 0.63 to 0.836 and blade aspect ratio 3 to 6,
holding solidity inside the reported band. The best was about 4 percent better than the
baseline family, at a blade aspect ratio of 6, and it is not bankable because it leaves the
family the coefficient was measured in. Buying a number by weakening the evidence behind it is
not a fallback.

None closed it. Reporting rather than trimming, per the blocked trigger.

## What would close it

Ranked by leverage. The first two are cheap and neither needs a design change.

**1. Kellen's measured thrust coefficient.** If it lands at or above the transferred 0.6055 for
this shape family in this Reynolds band, the 10 percent configuration-transfer allowance
retires, the haircut drops from 15 percent to 5, and conservative thrust to weight moves to
**2.518** at the current design point with nothing else changed. That clears the hard limit and
still misses the 2.75 internal target, so it turns a blocked week into a red one needing a
margin call. It also settles D25, because Kellen measured in the band this design actually sits
in. Two minutes in a browser. See D23.

**2. A lighter drive, which is the finding the audit turned up.** The design is **drive
limited**, not aerodynamics limited and not structure limited. Conservative thrust to weight
keeps rising as the radius falls, and the 100 mm row gives 2.376, but no shortlist motor holds
it: the rotor torque wants a belt ratio the KV450 cannot spin to on a 6S pack, and the motor
that has the speed does not have the torque.

Working backwards from that row, the drive would have to deliver 503 W continuously at **78 g
or less** to clear 2.5 there, which is 6.5 W per gram of continuous specific power. The best
part in the shortlist is the MN4006 at 5.3 W per gram and the selected MN5006 is at 4.9. So
this is a 22 percent improvement on the best catalogue part found, not a certainty, and it
needs the speed headroom as well as the power. Worth a proper search before anything else is
redesigned.

**Levers 1 and 2 together are what reach the internal target.** With Kellen's coefficient in
hand the 100 mm row tolerates a 141 g motor to clear 2.5 and an 86 g motor to clear **2.75**.
An 86 g part at 503 W continuous is 5.9 W per gram, which is much closer to what the catalogue
already does. Neither lever alone reaches 2.75; the pair does.

**3. A decision on the conservative mass allowance.** Week 2 uses 15 percent on catalogue parts,
20 percent on anything computed from an assumed section, and 25 percent on the module frame,
averaging 19.4 percent. At a uniform 10 percent the conservative case reaches 2.44 and still
misses. At a uniform 5 percent it reaches 2.56. With Kellen's coefficient and a uniform 10
percent it reaches 2.73, still short of the internal target. This is a smaller lever than it
looks and it is a judgement about how much a paper mass estimate grows, so it belongs to a
person.

**4. Weighed hardware.** The softest lines are the rotor shaft's torque allowance at 18 g per
Nm, the fastener and bonded joint line at 22 g, and the wiring harness at 16 g. Together they
carry about 98 g of the 692 g conservative total.

**5. Ramsey 2022.** A 25 kg subsystem mass table would give a second real anchor for the
structural lines. There is currently one, Runco, four orders of magnitude smaller.

## What changed

- **D2 is no longer provisional.** The cluster comparison it asked for has been run on a common
  boundary and the single rotor wins by 36 percent on conservative thrust to weight
- **The 0.607 coefficient is now 0.6055 and recomputed rather than quoted.** Same number to a
  quarter of a percent, now reproducible from Benedict's published figures in one line
- **The two open allocations are closed.** ESCs are module hardware and mounting counts in full,
  both settled against us and both settled before scoring
- **The design is drive limited.** Radius is set by the smallest rotor a named motor can hold
  continuously, not by where the aerodynamics or the structure want to be
- **Almost nothing in this module is fixed mass.** Sorted honestly, one 8 g controller board.
  D11 and D13 rest the feasibility case on fixed hardware amortising over more thrust, and
  there is very little of it to amortise
- **The Reynolds transfer is an extrapolation and cannot be made otherwise** inside this shape
  family, because the conservative thrust gate forces design thrust above 11.76 N. See D25
- **Kellen has been reclassified** from supporting evidence to a hard dependency for the freeze

## Debts carried forward

| # | Debt | Owner |
| --- | --- | --- |
| 1 | Two files each claim to be the loop execution contract. `stage-1/plan.md` names `.codex/weekly-loop.md`; this tick ran against `.claude/weekly-loop.md` on the launching human's instruction. The plan was deliberately not edited. See D24 | human |
| 2 | Four of the five motor rows and the ESC came from supplier listings rather than datasheet PDFs. Only the MN5006 was read off the manufacturer's sheet. Week 4 confirms the rest | week 4 |
| 3 | The 0.80 continuous derate on a 180 s rating has no source, because the problem statement states no endurance requirement to size it against. A stated hover duration would turn a judgement into a calculation | human |
| 4 | The three efficiencies, 0.93 belt, 0.84 motor, 0.95 ESC, are assumed. The motor figure is the sensitive one: at 0.78 the motor input rises to 493 W and eats most of the drive margin | week 4 |
| 5 | The cluster mass build-up is written out in prose in `01-configuration.md` but only its totals are in `numbers.json`, so a reader can follow it and a gate cannot check it | week 4 |
| 6 | The azimuthal model gives a peak to mean blade load of 2.37 against a published 3 to 4. The model has no wake return, no shed vorticity and no dynamic stall overshoot, so it under-predicts the peak. Week 4 uses 4.0 regardless, per D16 | week 3 and 4 |
| 7 | The 28 degree stall cap in the azimuthal model is stated, not measured. Heimerl would replace it | blocked on a paper |
| 8 | Side force is zero in the azimuthal model by construction, because the prescribed schedule has no phase offset. Week 3 reruns it against the solved linkage | week 3 |
| 9 | The blade spar is sized geometrically at 0.12 chord diameter with a 0.5 mm wall. Week 4 sizes it against centrifugal load, which at 2405 rpm is the load that governs | week 4 |
| 10 | `stage-1/organiser-email.md` is still mostly answered by the problem statement and should be cut down or dropped | human |

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
  the optimum. Now the second highest leverage item on the list. See D23 and D25
- **Heimerl, Halder, Benedict et al.**, VFS 77th Forum, cyclorotor in forward flight. Wanted:
  the measured blade peak to mean load factor and the side force angle against pitch offset.
  Answers debts 6 and 7 and feeds week 3's vectoring section
- **Ramsey 2022**, handle 1969.1/198531, item `692efcdd-c56a-4c7a-b507-f3e673986b51`. Wanted:
  the 25 kg subsystem mass table and any blade mass or deflection figures

Week 2 ran without all three and disclosed it, which is what the config asks for supporting
evidence. Kellen has stopped being supporting evidence.

## Gate state at the end of the week

```
python tools/check.py --week 2   1 failure, the T/W decision line
python tools/check.py --global   pass
python tools/test_gates.py       89 of 89 self-tests behaved as expected
```

The single failure reads:

    FAIL  week2: conservative mass and thrust still clear T/W 2.5
          T/W 2.253 at 15.30 N and 692 g

Every other gate passes, including all four feasibility gates: the momentum floor with a figure
of merit of 0.60, the second power route agreeing to 9.8 percent, the four row sensitivity
table reproducing each ceiling and ideal power, and solidity at 0.3151 inside the reported band
with the low coefficient answering a stated deflection loss.

**`tools/check.py` was changed, and only to make it stricter.** Four gates were added after the
audit found that three of the lists week 2 fills carried numbers nothing read: a 36 row table
of arbitrary positive values satisfied the azimuthal check identically to a calibrated one, and
nothing asked whether the named drive could hold the design point. The new gates require the
azimuthal loads to average to the recomputed thrust, exactly one drive to be selected with its
continuous rating covering the recomputed motor input, continuous torque to follow from KV and
current, and exactly one configuration candidate to be selected and to be the one that wins on
conservative thrust to weight. Twelve self-tests were added with them, one per attack, and the
suite went from 77 to 89. No tolerance, bound or limit was loosened.

## What week 3 needs to know

Week 3 cannot start on a frozen geometry, because there is not one. Three options and the
choice is a person's:

1. Pull Kellen. If the measured coefficient is at or above 0.6055 the case moves to 2.518 at
   the current geometry, which is compliant and still red
2. Search for a drive delivering about 503 W continuously at 78 g, which would move the design
   to a 100 mm radius and clear 2.5 on its own. With Kellen in hand the same row tolerates 86 g
   and clears 2.75, and that pair is the only route to the internal target this week found
3. Accept the finding and tell Stage 2

If week 3 has to start anyway to protect the calendar, start it on the 110 mm candidate and
accept that a later geometry change costs a week 3 rerun, because link lengths, offset geometry,
the pitch schedule and gearing all move with radius. The 120 mm second candidate exists for
exactly that reason and it is insurance, not a free option.
