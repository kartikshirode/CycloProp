AUDIT-COMPLETE

# Final Stage 1 audit

Audit date: 4 September 2026

I checked the context, prompt, plan, design notes, evidence ledger, literature log, submission draft, email draft, handoff, decisions, journal, figures and the calculation scripts. I also ran the repo checks.

`python tools/check.py --all` passes all 279 gates. `python tools/test_gates.py` passes all 212 self-tests. `python tools/check.py --week 5` fails one check only: the human technical-read marker is still outstanding. That is a real stop, not a script problem.

## Verdict

The package is a serious Stage 1 paper, but I would not send it in its current state. The main reason is not page polish. The selected MN5006 motor is listed as a 4-6S motor while the design interface is 8S. The report also has an unresolved 6-30 V controller against a charged 8S pack at 33.6 V. Those are interface and safety problems in the chosen drive, not small documentation slips.

There is good engineering work here: the mechanism closes, the load path is described, the power chain is reproducible and the report is candid about missing CFD, FEA, coupons and tests. The nominal case clears the T/W requirement by only 0.0563. The conservative stacked case does not clear it, and its mass is not yet closed from geometry or weighing. With the electrical issues open and the human team fields still unfilled, this is a no-send as-is. After the blockers are resolved, it becomes a credible preliminary entry, but I would still expect the final top-15 decision to depend on Stage 2 evidence.

## Findings that must be fixed before 26 September

### F1. Blocker: motor voltage rating conflicts with the declared pack

Where: `stage-1/design/evidence-ledger.md:50`, `stage-1/design/numbers.json` E12 and drive block, `stage-1/design/04-thrust-and-power.md`, `stage-1/design/09-packaging-and-integration.md:138`, and the submission power section.

E12 records the selected T-Motor Antigravity MN5006 KV450 as 650 W, 26 A, 106 g and 4-6S. The design now declares 8S, which is 29.6 V nominal and 33.6 V fully charged. The solver therefore shows a clean 8S current and speed calculation, but the catalogue rating itself does not say that the motor may be used on 8S. The 8S ESC line does not fix the motor rating.

This can invalidate the selected drive, its thermal derate and the 483.2 W mechanical claim. A hostile reviewer will ask why an out-of-range motor is the part that makes the design close.

Fix before send: obtain written manufacturer confirmation for this exact motor at the proposed voltage, or select an 8S-rated motor and rerun speed, current, torque, thermal derate, power and mass. Keep the old row as a rejected candidate if useful, but do not call it selected until the voltage is supported.

### F2. Blocker: human completion and item 7 are not actually closed

Where: `stage-1/human-gate.md`, `stage-1/design/07-team-and-execution.md:46-57`, the Stage 2 ownership table at lines 118-128 and `stage-1/submission/email-draft.md:66`.

Registration, eligibility, roster and sender markers are now present in the gate file. The technical-read marker remains pending, so week 5 correctly fails. The report still contains `[P-1]` through `[P-9]` placeholders for names, roles, programmes, prior work, tools, weekly time and facilities. Every Stage 2 row still has `[P-1]` as owner. The email still contains `[SENDER NAME]`.

The paper has a team execution structure, but it does not yet prove team capability. These fields belong to the human sender. Fill them with real facts, rebuild the PDF, read the built PDF end to end and then add the exact technical-read marker. Recheck the official competition page, email address, IDs, deadline and file rules in a browser before sending. I did not alter the human gate.

### F3. High: servo margin is inconsistent in the attachment

Where: `stage-1/submission/cycloprop-stage1.md:273-274` versus `stage-1/submission/cycloprop-stage1.md:957`, `stage-1/design/03-pitch-and-vectoring.md:334` and `stage-1/design/08-structure-and-loads.md`.

The prose says the two servos have a margin of 2.33. The current corrected calculation is 1.982. The 2.33 figure is the old inverted gear-ratio result that the design notes already fixed.

Fix the paragraph and any generated text from the same source, then rebuild and run the checks. A reviewer finding two margins in one attachment will question the linkage calculation even though the current JSON is consistent.

### F4. High: T/W is a nominal pass with an unclosed mass risk

The reported nominal case is 17 N at 677.91 g, giving T/W 2.5563. The low-coefficient case is 16.1493 N. The conservative stacked case is 15.3 N at 763.24 g, giving T/W 2.1569 and missing 2.5 by 104.76 g. Only the nominal, mass-only downside and coefficient-only downside clear the hard threshold. The mass sheet is better than the old blanket-rate table, but 29 of 33 lines are still growth or consistency assumptions rather than drawn CAD mass or weighed parts.

The wording should be explicit:

> The nominal estimate clears the required module T/W at 2.5563. The conservative stacked case does not: it is 2.1569 and would need 104.76 g removed to reach 2.5. The design is a preliminary nominal pass with an unclosed mass risk, not a proven T/W pass. Stage 2 must replace the assumption-based lines with drawn or weighed evidence.

Do not bury this gap under the 2.0 screening floor. It is the largest scoring weakness after the drive compatibility issue.

### F5. High: root attachment margin is not a bond margin

Where: `stage-1/design/08-structure-and-loads.md`, especially the attachment margin, and the submission structural section.

The bearing static margins are useful: the four 693ZZ bearings per blade and 90 percent sharing give a static screen above 2.5 at overspeed. That does not qualify the bonded root fitting. The root sees roughly 301 N centrifugal load, plus cyclic aerodynamic load, but no adhesive shear area, peel, stress concentration or fatigue calculation is shown. The report calls this an attachment margin when the calculation is mainly a bearing capacity check.

Fix the label now so it says bearing-only, or add a preliminary bond area and failure-mode calculation. Stage 2 needs a coupon, root detail, local FEA and a cyclic test. The same applies to the belt tooth and pulley load rating, which is screened by geometry and a factor but not by a supplier life or torque curve.

### F6. High: pitch controller input is over the stated voltage range

Where: `stage-1/design/03-pitch-and-vectoring.md:205-214`, `stage-1/design/09-packaging-and-integration.md:127-130` and the context open-items list.

The Matek F411-WSE class controller is listed at 6-30 V. A full 8S pack is 33.6 V. There is no regulator, regulator mass, heat loss, wiring change or alternate board in the current budget.

Fix before send by choosing a controller rated above the full pack voltage, or adding a named regulator with current rating, mass, power loss and packaging. Rerun the electrical and mass totals. This is separate from the motor voltage problem.

### F7. Medium: live evidence files still carry retired numbers and statuses

Where: `stage-1/design/evidence-ledger.md:182-188`, `stage-1/literature.md` near the opening status and S5 note, and `stage-1/design/04-thrust-and-power.md` in the figure-of-merit paragraph.

The live evidence ledger still says the stacked case is 2.517, the mass is 692.4 g and the gap is 58.6 g. The current results are 2.1569, 763.24 g and 104.76 g. The ledger also says E18 and E19 are Kellen measurements, but E18 is the measured Kellen value and E19 is a derived Benedict value. The literature opening still says Kellen is summary-only and could not be downloaded, while later text says both Kellen and Benedict were retrieved and read. The power note still says the thesis body is unread even though the current ledger treats the relevant Kellen rows as measured.

These are not historical records in the decisions log. They are live evidence and handoff files. Update them together after the human state is settled. Preserve the old values in historical progress and decision entries.

### F8. Medium: packaging has a stale shaft size and a loose torque statement

Where: `stage-1/design/09-packaging-and-integration.md:59`, `:111-113` and `:158`.

The ASCII layout labels a 14 mm rotor shaft while the current design uses a 16 mm shaft. The interface table says reaction torque is motor torque times belt ratio. That omits the 0.93 belt efficiency. The actual current rotor torque is about 1.54226 N m. If the intent is a conservative mount load, label the larger number as conservative and state the efficiency assumption.

### F9. Medium: source taxonomy and a few claims overstate the evidence

Where: `stage-1/submission/cycloprop-stage1.md:184-187`, `:638`, `:734-745` and the evidence ledger.

The attachment says five evidence classes are used. The project ledger defines seven and uses measured, derived, transferred, summary, downside and catalogue. The low coefficient is a downside case, and motor and BOM values are catalogue data. The viva answer calls the 0.6648, 0.7211 and 0.8114 values three independent values, but they come from two studies, with two Benedict-derived values. The BOM says five expensive lines are 52 percent of the total; the current materials file and current total give about 50.5 percent.

Use the actual class names, say three values from two studies and correct the percentage. These are easy credibility wins.

### F10. Medium: official channels and limits need a final human check

The address, IDs, deadline and page/file rules were not rechecked in the current audit run. The draft email asks about page limit and naming but the plan also calls for confirming the competition and team IDs. A human should check the official page or organiser channel on the day of send and record the answer in the handoff. The attachment is 30 pages. The plan's 15-page figure is an internal target, not a confirmed organiser limit, so this needs confirmation rather than an assumed cut.

### F11. Low: figures are numbered, tables are not

The PDF has seven numbered figures with captions. I found no numbered table labels. This is not a technical blocker, but adding table numbers and cross-references would make a 30-page attachment easier to interrogate if time remains.

## Seven required Stage 1 items

| Item | What is present | Audit judgement |
| --- | --- | --- |
| 1. Configuration and concept | Three layout candidates, one rotor selection, envelope, interfaces and integration description | Delivered. The stale 14 mm shaft label needs correction. |
| 2. Rotor sizing and performance basis | Radius sweep, solidity, Reynolds number, coefficient scenarios and literature comparison | Delivered as a paper estimate. The coefficient transfer and FM are still low-confidence. |
| 3. Pitch mechanism and vectoring | Four-bar closure, 37-row schedule, servo sizing and five-command vector map | Delivered strongly on kinematics. Hardware friction and actual vector authority remain untested. |
| 4. Thrust and power | Momentum floor, figure-of-merit route, Benedict cross-check, azimuthal model and drive screen | Delivered with honest assumptions. Motor and controller voltage compatibility is open. |
| 5. Mass and T/W | 33-line budget, four cases, mass growth classes and explicit stacked miss | Delivered, but not closed from geometry or weighing. The stacked miss must stay prominent. |
| 6. Structure and loads | Eight margins, blade load path, bearing screen, foam sensitivity and missing-work list | Delivered as preliminary beam and static checks. Bond, fatigue, modal, belt and local joint work remain. |
| 7. Team capability and execution | Stage 2 dependency table, gates and build/test plan | Structure delivered. Human names, roles, tools, facilities and owners are still placeholders. |

## Delivery against the plan

| Plan block | Delivery | Gap |
| --- | --- | --- |
| Week 1 | Requirements, official PDF extraction, literature table and source notes | Literature file opening status is stale. Official channels need one final recheck. |
| Human H | Registration, eligibility, roster and sender markers partly confirmed | Technical read is pending. Real team facts are not in item 7 or the email. |
| Week 2 | Configuration comparison, sizing, thrust, power, drive shortlist, evidence ledger | The live ledger still has retired stacked-case numbers. |
| Week 3 | Linkage, pitch schedule, vector map, integration prose, item 7 structure and PDF build | Shaft sketch label and table numbering need attention. |
| Week 4 | Structure, materials, manufacturing, BOM, mass and T/W cases | Mass closure, bond qualification and electrical compatibility remain open. |
| Week 5 | Seven sections, criteria map, claims and risks, 12 viva questions, PDF and email draft | The human gate is not complete. Servo prose, source taxonomy and a few percentages are stale. |

The project also produced useful extra assurance: seven reproducible figures, a six-phase review trail, a 36-point azimuthal model, four mass/TW cases, a 37-row pitch schedule and 212 gate self-tests. Those extras improve traceability, but they do not replace the missing motor confirmation, team facts or physical tests.

## Engineering assumptions and viva position

| Assumption | Current defence | What would settle it |
| --- | --- | --- |
| CT 0.6055 transfer | It is below Kellen's 0.6648 value on a 1.1 percent shape-family match and inside the reported Reynolds band. It is still transferred, not measured at this design point. | Matched CFD, then a load-cell test. |
| FM 0.5215 | Scaled from Kellen's 0.6 while holding power coefficient fixed. That is a bookkeeping estimate, not a measured design FM. | Read the matched Kellen curves and validate with power and thrust data. |
| Momentum area 2R times span | A valid ideal induced-power floor for the projected area. It is not proof of the actual streamtube or total power. | Test or a validated flow model. |
| Peak-to-mean blade load factor 4 | A conservative screen around a summary-only 3 to 4 range; the own model gives about 2.55. | Heimerl source check and transient CFD or instrumented load data. |
| Foam and skin allowables | The wrinkling equation and class properties make a useful paper screen. Local defects, adhesive and batch spread are missing. | Coupon panels made with the planned process, then local structural analysis. |
| Bearings | ISO76 static capacity with 90 percent sharing gives useful static margins. The duty is oscillating at about 38.95 Hz and no false-brinelling or life rating is shown. | Supplier oscillating rating, grease check and bench duty test. |
| Belt and shaft | Geometry, tension and a 1.4 side-load factor are calculated. Tooth rating, wrap, pretension and fatigue life are not. | Vendor data and a loaded spin test. |
| Vector map | Kinematic closure and symmetry make the map reproducible. It is not a measured thrust vector under inflow. | Multibody model with joint friction, then thrust-vector measurement. |

The single question most likely to expose the current weakness is:

> Your selected MN5006 is specified for 4-6S, so why does the final interface put it on 8S, and what manufacturer evidence says the 650 W, 26 A and 180 second ratings still apply?

The honest answer today is that there is no such evidence in the package. That makes the issue a blocker, not a Stage 2 footnote.

## Criterion scores

| Criterion | Score | Reason |
| --- | ---: | --- |
| 10 N thrust feasibility | 10 / 15 | Good momentum, FM and cross-check routes. No direct CFD or test, and the nominal coefficient is transferred. |
| T/W above 2.5 | 7 / 15 | Nominal 2.5563 clears thinly. All stacked conservative cases miss, and the mass is not physically closed. |
| Kinematics and vectoring | 12 / 15 | Closed four-bar math, schedule, actuator sizing and vector map are the strongest section. Hardware authority is untested. |
| Aerodynamic analysis | 7 / 15 | Several useful routes and a load model, but key values are assumed or transferred. |
| Structural analysis | 9 / 15 | Load paths and static screens are clear. Bond, fatigue, modal, local FEA and belt life are missing. |
| Manufacturability, material and cost | 7 / 10 | Detailed process and BOM. Prices are indicative, quotes are absent and electrical parts are unresolved. |
| CAD, integration and packaging | 3 / 5 | Envelope and interfaces are usable for Stage 1. No CAD is expected yet, but the shaft and torque text need repair. |
| Presentation, viva and clarity | 7 / 10 | Good section structure, figures and hostile questions. Placeholder team facts, 30 pages and stale figures reduce trust. |
| **Total** | **62 / 100** | **Strong paper preparation, not a top-15-ready final claim as it stands.** |

## Stage 2 work that should stay visible

Stage 2 needs to close the mass from CAD and scales, confirm the motor and controller voltage, build the blade and root with a coupon route, qualify the adhesive joint, obtain oscillating bearing and belt data, run multibody and CFD models, test thrust and power, measure the vector, collect supplier quotes and execute the staged spin plan. The report already names most of these dependencies. The owners and facilities are the part still missing.

## Send decision

No, not as it stands.

The shortest path to a defensible send is:

1. Human fills the team and sender fields, checks the official channel and reads the built PDF, then adds `TECHNICAL-READ-COMPLETE`.
2. Resolve both 8S electrical interfaces: the MN5006 motor rating and the F411-WSE input, with updated power, mass and BOM numbers.
3. Correct the servo margin, live evidence ledger, literature status, source classes, independence wording and cost percentage.
4. Rename or qualify the attachment margin and state the stacked T/W miss plainly.
5. Rebuild the PDF, rerun all gates, and send only after week 5 exits cleanly.
