> **Editorial note added 27 August 2026, not part of the original return.** The Problem 1
> headline below, that Runco 2023 re-cuts to a module T/W of 1.0 to 1.2 and that the gap is
> a thrust-density rather than a mass-fraction problem, is **withdrawn**. It rested on 10 gf
> per rotor, which is the older 1 inch rotor quoted in passing; the aircraft's rotor is
> 16.9 gf and it hovered at 70 g on four of them. The corrected re-cut is 2.13, and the
> corrected reading is in `stage-1/literature.md` and decision D13. Everything else here
> stands. Kept as received rather than rewritten, because it is evidence.

# Cycloidal Rotor Aerodynamics & Mass Properties: Evidence Review for PUSHPAK CycloProp Stage 1

*Scope: evidence, numbers, and provenance for the three problems in the brief. Every numeric finding carries source, measured configuration, and a MEASURED / SIMULATED / PREDICTED tag. Points where the published record contradicts an assumption in the brief are flagged in bold. Stated gaps are given where no source exists rather than inferred.*

## TL;DR
- **No published cyclorotor mass breakdown, re-cut onto the competition's module boundary, reaches T/W 2.5**; the closest *measured* evidence tops out near 1.7–1.8. Critically, the single most mass-optimised cyclocopter (Runco & Benedict 70 g, 2023) re-cuts **worse** (~1.0–1.2), not better, because it runs at Re ≈ 18,600 where per-rotor thrust is only ~10 gf. The gap is a **thrust-density (Reynolds/scale) problem, not a mass-fraction problem** — copying mass-optimised micro rotors does not close it.
- The published record **confirms the counterargument the brief "could not dismiss"**: Shrestha & Benedict (JAHS 2022, SIMULATED + validated) show blade weight per unit thrust is scale-invariant and blade stress rises monotonically — so scale alone does not shrink blade-mass fraction. It **also confirms the favourable half**: non-dimensional thrust stays ~flat with Reynolds number while torque and power fall sharply (Re 10⁴→10⁵). Net: the gap must be closed by fixed-mass amortisation + materials/stress management, with aerodynamic efficiency (not blade mass) improving with scale.
- Thicker airfoils help cyclorotors at every scale (**NACA 0020 at UAV scale is well-supported**), and thrust vectoring is thoroughly documented (Adams β = 15–35°; Sirohi ~10°; Runco flight-demonstrated), so the vectoring and blade-pitch Stage 1 sections are on solid ground. The genuinely thin evidence is (a) any published cyclorotor that **states and meets a T/W target** — none exists — and (b) an openly tabulated **blade-area thrust-coefficient spread** — the raw values sit inside primary figures. Both gaps are real and worth stating in your submission.

---

## Key Findings

**Problem 1 (module T/W):** The best-mass-optimised published cyclocopter (Runco & Benedict 2023, 70 g quad, open access) has a full sub-system breakdown but operates at Re ≈ 18,600 with ~10 gf per rotor; re-cut onto the module boundary it yields ~1.0–1.2, **below** Benedict 2010's 1.69. The decisive scaling datapoint is Shrestha & Benedict (JAHS 2022): it validates both the brief's counterargument (blade mass/thrust scale-invariant; stress rises) and the favourable claim (non-dimensional thrust flat vs Re; power falls).

**Problem 2 (0.607 transfer):** Multiple non-dimensionalisations coexist (blade planform area, rectangular projected/swept area, disk loading). Reynolds-invariance of non-dimensional thrust (validated CFD) makes transferring a *thrust* coefficient across Re 35k→100k defensible; the residual risk is the simultaneous change in blade count, airfoil, and c/R (solidity + virtual camber), which the Re-invariance does **not** de-risk.

**Problem 3 (inaccessible papers):** All three located. Kellen 2019 confirms the baseline geometry and figure of merit 0.6; Runco 2023 (open access) yields the full mass table; Adams 2013 (open-access PDF) yields the cam mechanism, kinematics, and 5 g blade mass.

---

## Details

### PROBLEM 1 — THE MODULE THRUST-TO-WEIGHT GAP

#### 1.1 / 1.2 — Runco & Benedict 2023, "Design, development, and flight testing of a 70-gram micro quad-cyclocopter," *Int. J. Micro Air Vehicles* 15, DOI 10.1177/17568293231189999 (open access, CC BY-NC)
Per the abstract, the 70-g vehicle "is the lightest quad-cyclocopter developed to date by an order of magnitude and only the second to achieve forward flight," with eight independent control parameters. **Full sub-system weight breakdown (Table 3, MEASURED):**

| Component | Weight (g) | % |
|---|---|---|
| Motors + Transmission | 13.4 | 19 |
| Digital Servos | 5.0 | 7 |
| Cyclorotors (4×; blades+frames+pitch linkages) | 14.4 | 21 |
| Structure + Wires | 13.1 | 19 |
| LiHV Batteries | 18.4 | 26 |
| Electronics | 5.7 | 8 |
| **Total** | **70** | 100 |

Configuration (MEASURED/design): 4 cyclorotors, radius 1.3 in, 4000 RPM, Re ≈ 18,600 (75% span), c/R 0.8, elliptical flat-plate blades, ±45° symmetric pitch, blade aspect ratio 1.62, ≈0.12 g per blade. Each rotor designed for 10 gf; total design thrust 68 gf. Maximum thrust with the upgraded 2S electronics was **not measured** (test-stand vibration limits).

**Re-cut onto the module boundary (my calculation from Table 3):** per rotor ≈ cyclorotor 3.6 g + motor/transmission 3.35 g + servo 1.25 g = 8.2 g of "module" mechanism, plus a share of the 13.1 g structure+wires for mounting. Thrust ≈ 10 gf (0.098 N) per rotor. **Module T/W ≈ 1.2 excluding mounting hardware, and below 1.0 once a mounting share is added.**

> **CONTRADICTION TO FLAG.** The brief expected the 70 g design to be "the single most useful data point" for closing the gap. It is highly useful — but in the *opposite* direction to what was hoped. It proves the tare/structure fraction is already solved in the literature (mass optimisation is not the bottleneck), yet at ultra-low Re the per-rotor thrust is so small that module T/W is ~1.0–1.2 — **worse** than Benedict 2010's 1.69. The takeaway: the gap is fundamentally a **thrust-density (Reynolds/scale)** problem. Replicating a mass-optimised micro rotor makes T/W worse, not better.

#### 1.1 — Other groups (IAT21/CROP, Korean, full-scale)
- **IAT21 D-Dalus / CROP (Xisto et al. 2016):** L3 rotor, six NACA 0016 blades, c/R 0.5, span-to-diameter 1.0, large scale (payloads > 100 kg). Published data is thrust/power vs RPM (IAT21 MEASURED; Xisto SIMULATED). No module-boundary mass breakdown bettering 1.8 is extractable — this is a manned-scale machine.
- **Gibbens/Bosch (via Sirohi 2007):** "The rotor had a span of 4 ft, a diameter of 4 ft and six blades of chord 1 ft with a NACA 0012 airfoil. A maximum power loading of 10.88 lb/HP was recorded, and the rotor operated at a maximum Reynolds number of around 730,000" (MEASURED, full-scale). No MAV-comparable mass breakdown.
- **Korean groups (Yun, Hwang, Kim — Seoul National / Konkuk / KAIST lineage):** 50 kg-class VTOL UAV concepts and 0.8 m rotors (Kim: NACA 0012, chord 0.15 m, up to 600 RPM, Re ≈ 260,000, MEASURED). No module mass breakdown better than 1.8 located.

> **CONCLUSION (1.1):** No published cyclorotor mass breakdown re-cuts onto this module boundary above ~1.8. Large-scale work does not help, because it publishes performance (thrust/power/power-loading), not MAV-comparable component masses.

#### 1.3 — Mass scaling law
**Shrestha, Benedict et al., "Understanding Upward Scalability of Cycloidal Rotors for Large-Scale UAS Applications," JAHS 67(4), Oct 2022** (2D CFD + lower-order aeroelastic model, validated against UAV-scale experiment at max chord Re = 2×10⁵; optimisation spans 1–1000 lb thrust). Verbatim findings:
- (SIMULATED, validated) "The CFD results show that the **nondimensional thrust remains almost unchanged with increasing Reynolds number**, while the nondimensional torque and power decrease significantly from Re=10⁴ to 10⁵, which clearly shows that the cycloidal rotor scales up favorably from thrust production and aerodynamic efficiency standpoints."
- (SIMULATED) "as the cyclorotor size is increased, the **blade weight per unit thrust remains constant**; however, the **blade stress increases monotonically** if the rotor geometry is kept similar. This monotonic increase in the blade stress is found to be **independent of the blade structural design**."

> This is the single most important scaling result for your case. It **simultaneously** supports your favourable scale argument (efficiency/power improve with Re) **and** the counterargument you could not dismiss (blade-mass-per-thrust is scale-invariant, stress climbs). Practical consequence: the gap cannot be closed by blade scaling — it must come from the non-blade fixed-mass fraction amortising over 5× the thrust, plus materials/stress management on the blades. An explicit multi-point mass-per-newton scaling curve does not exist in the literature as a single published law; the three anchor points you can assemble (Runco micro ~Re 18.6k; Benedict/Sirohi MAV ~Re 17–35k; Kellen UAV ~Re 100–300k) support "aerodynamic efficiency improves with scale, blade mass fraction does not."

#### 1.4 — Blade mass per unit span, CFRP over foam
This construction is exactly what the field already uses — the user's material assumption is standard, not aggressive:
- **Sirohi 2007:** blades = carbon-fibre composite wrapped around a foam core, NACA 0010, 6 in span, 1 in chord; components weighed/balanced to 0.01 g (MEASURED).
- **Adams 2013:** single-layer carbon prepreg over foam core with rectangular cut-outs, **8 g → 5 g per blade** with negligible stiffness-to-weight penalty; 50 µm Mylar heat-shrink skin (MEASURED).
- **Runco 2023 (micro):** unidirectional-CF elliptical flat-plate blade with 3 µm Mylar skin, ≈0.12 g at 1.68 in span (MEASURED).
- **General CFRP laminate density:** 1.4–1.9 g/cm³ (≈1400–1900 g/m² per mm thickness).

> **GAP:** a clean g/m figure for CFRP-skin-over-foam blades in the 100–400 mm span band is not published as such; the closest measured anchors are Adams (5 g per blade at ~9-in-class span) and Sirohi/Runco. Your CFRP assumption is credible; document the specific layup and cite Adams for the achievable strength-to-weight.

#### 1.5 — Any cyclorotor stating AND meeting a T/W target
> **GAP CONFIRMED.** No published cyclorotor design states a thrust-to-weight target and reports whether it met it. Designs are built to fly and measure (Benedict, Runco, Adams, Kellen) or to map parametric performance (Xisto, Hu). The user's inability to find one is correct and worth stating explicitly.

#### 1.6 — Is 2.5 in line with propellers, and where did the number come from?
Conventional small electric propulsion at the ~10 N class routinely achieves motor+prop thrust-to-*component*-weight far above 2.5 (hobby motors producing ~1 kg thrust at tens of grams motor mass; FPV builds routinely design to 4:1–5:1 all-up). So **2.5 is unremarkable for propellers but aggressive for cyclorotors**, whose large rotating cage imposes a mass penalty explicitly noted by Xisto and others.
On origin/clarifications: Techfest (IIT Bombay) describes CycloProp as "A national, MeitY-funded challenge to design a build-ready cycloidal rotor module for drones." The PUSHPAK mission is documented — "Backed by a grant-in-aid of Rs. 82.7 crore, Pushpak brings together seven top-tier institutions… will run for four years," MeitY-launched, IIT Bombay-led.
> **GAP:** I could not locate a public copy of the CycloProp *problem statement* itself, nor any organiser FAQ/corrigendum or public commentary on the derivation of the 2.5 figure. The module-boundary definition and mass ceilings in the brief could not be independently verified against a public source.

---

### PROBLEM 2 — THE THRUST COEFFICIENT TRANSFER

#### 2.1 — Is blade-area the right reference? Conversion
No single convention dominates the field:
- **Kellen 2019** reports thrust per unit **blade (planform) area**.
- **Benedict 2010** uses a **blade-area** coefficient (source of the 0.607).
- **Xisto 2016** uses **disk loading** on the rectangular projected area A = span × 2R.
- **Sirohi 2007** defines a time-averaged blade area; **helicopter C_T/σ** appears in adjacent rotor work.

**Explicit conversion.** With A_blade = N·c·span and A_proj = span·2R,
C_T,proj = C_T,blade × (A_blade/A_proj) = C_T,blade × (N·c)/(2R) = C_T,blade × (N/2)·(c/R).
For the target family (N = 3, c/R 0.66): factor = 1.5 × 0.66 = **0.99** — so for *this specific geometry* the blade-area and projected-area coefficients are numerically almost identical (a coincidence of the chosen shape, not a general identity). **Always state which area a quoted coefficient uses before transferring it**, and apply the (N/2)(c/R) factor when moving between blade-area and projected-area conventions.

#### 2.2 — Published spread of the coefficient
> **GAP:** an openly tabulated blade-area C_T across blade count/airfoil/solidity/Re is **not** extractable from accessible secondary sources — the raw values live inside the primary parametric figures (Benedict 2010; Kellen 2019; Hu 2015/2019). What is established directionally:
- Thrust per unit blade area **drops steeply as blade number rises** (Kellen, MEASURED).
- (Alsabri et al., *Aerospace* MDPI 13(9):765, 2025, 2D URANS, blade number 2–8, solidity 0.24–0.60, 26 points): "At fixed rotational speed, **increasing solidity raises both the thrust and power coefficients and lowers power loading**." Peak-to-mean thrust ratios of 3–4 for 2- and 3-bladed rotors (a structural-load design constraint invisible in cycle-averaged numbers — relevant to your blade sizing).
- Optimal solidity range **0.30–0.40** (Kellen, MEASURED).

> The 0.516 placeholder (85% of nominal) is a reasonable caution but is not anchored to a published lower bound. The defensible statement: the coefficient is configuration-sensitive at roughly the ±10–20% level from solidity/airfoil/blade-count changes, while Reynolds contributes little (see 2.3). If your final solidity leaves the 0.30–0.40 measured-optimal band, re-derive rather than transfer.

#### 2.3 — Behaviour between Re 35,000 and 100,000
Validated CFD (Shrestha & Benedict 2022) and the Benedict aeroelastic model (validated Re 80k–200k) indicate **non-dimensional thrust is approximately Reynolds-invariant across this band while power falls**. Transferring a *thrust* coefficient from Re ~35,000 to ~100,000 is therefore defensible for the thrust term.
> The residual risk is **not** Reynolds — it is the simultaneous change in blade count (4→3), airfoil (0010→0020), and c/R (0.433→0.66), which move solidity and virtual camber and are **not** de-risked by Re-invariance. This is the honest caveat to carry into your sizing.

#### 2.4 — NACA 0010 → 0020: lift slope and stall
Across scales, thicker sections help cyclorotors:
- **MAV scale (Benedict 2010 PhD, MEASURED):** "Among the three NACA sections (NACA 0006, NACA 0010 and NACA 0015)… NACA 0015 had the highest power loading followed by NACA 0010 and then NACA 0006… The chordwise optimum pitching axis location was approximately 25–35% of the blade chord." All NACA sections beat flat plates. Tradeoff to note: a later surrogate-model study reports NACA 0010 gave the *highest thrust* at all pitch amplitudes while NACA 0015 gave the best *power loading* — thicker favours efficiency/stall margin, thinner can favour peak thrust.
- **UAV scale (Kellen 2019, MEASURED):** airfoil thickness up to **25% chord** efficiently generated thrust, and thicker airfoils gave efficient operation over a **wider range of pitch amplitudes** — direct support for NACA 0020 at the user's scale.
- **Large scale (Xisto 2016, SIMULATED):** "airfoil thickness significantly affects the rotor performance; such a result is partly in contrast with previous findings for small- and micro-scale configurations." NACA 0018 shrank the top-position separation bubble to near-zero vs NACA 0006 (higher stall angle), raising power loading.

> **CONFIRMS the brief.** Going 0010→0020 should preserve or improve stall margin and power loading under the continuously varying AoA (thicker delays dynamic-stall separation), at the possible cost of a slightly lower *peak* thrust coefficient. Virtual camber/incidence from curvilinear flow makes the top blade see negative equivalent camber (Xisto) — thickness buys margin exactly where separation first appears.

#### 2.5 — Validated hover-thrust models (with error direction)
- **Sirohi 2007:** double-multiple-streamtube + indicial/Wagner unsteady aero; validated against a 6-in rotor at Re ~17,000. Simple, design-oriented (DMST).
- **Benedict et al. 2011 aeroelastic:** validated Re 80,000–200,000; blade as slender beam, 2D aero.
- **Xisto 2016:** semi-empirical analytical (Garrick/Theodorsen-based with empirical velocity-scaling function E) + 2D URANS. **Key caveat matching the brief:** CFD **over-predicts thrust and under-predicts power** (attributed to neglected 3D endplate losses and un-modelled parasite frame power); the analytical model matches on-design but **fails off-design**.
- **Halder & Benedict 2018/2019:** free-wake nonlinear aeroelastic model validated against **instantaneous** blade forces (not just time-averaged) — the most rigorous, capturing dynamic virtual camber, leading-edge vortex, and shed wake.

> **Error direction to plan around:** simple tools are optimistic on **both** axes off-design (over-predict thrust, under-predict power) — the wrong way for the user. Size with margin, prefer your measured power routes (152–161 W at the blade, already cross-validated) and a validated aeroelastic model for cross-checks.

#### 2.6 — Side force / thrust vectoring
- **Adams 2013 (MEASURED):** the resultant thrust vector "is tilted in the direction of rotation by an angle (denoted by β) of **15–35°** depending on the pitching amplitude and rotational velocity"; the cam is pre-positioned to counter this for pure vertical thrust. Servos gave 0–55° pitch amplitude and **360° thrust vectoring**.
- **Sirohi 2007 (MEASURED):** resultant thrust direction lags/leads the eccentricity (offset) direction by ~**10°**; mapped for pitch 0–40° and eccentricity −50° to +50° at 800 RPM.
- **Benedict twin-cyclocopter (per brief):** resultant 30° off vertical, corrected by rotating the pitch offset 30°.
- **Runco 2023 (MEASURED, flight):** commanded thrust-vector phase Φ up to −14° produced −1.4 m/s; independent thrust-vectoring vs body-pitch translation demonstrated; full eight-parameter over-actuation.

> The off-axis angle **grows with pitch amplitude and varies with RPM/Reynolds**. Any "10 N" claim must state the resultant direction. The phase-angle→thrust-direction map, **with the RPM-dependent β offset**, IS the kinematic + performance vectoring analysis the competition requires — build it from Adams (β 15–35°) and Sirohi (~10°).
> **GAP:** a single published curve of resultant-angle vs pitch amplitude *and* phase *and* Reynolds does not exist; assemble it from Adams (amplitude/RPM dependence) + Sirohi (eccentricity sweep) + the brief's Benedict 30° point.

---

### PROBLEM 3 — PAPERS THE USER COULD NOT ACCESS

#### 3.1 — Kellen, Adam John, "Performance Measurements on a UAV-Scale Cycloidal Rotor in Hover," MS thesis, Texas A&M University, 2019 (handle 1969.1/184958)
Author and title **confirmed**. Full-text PDF is legitimately open access via the TAMU OAKTrust repository (`KELLEN-THESIS-2019.pdf`, 33.7 MB) and a CORE mirror. From the thesis abstract and companion papers (Kellen & Benedict, AHS 73rd/74th Forums 2017/2018; Halder, Kellen & Benedict, VFS 75th Forum 2019):
- 37 unique configurations; **optimal at Re 200,000 — c/R 0.66, 3 blades, blade aspect ratio (span/chord) 4, NACA 0020, rotor aspect ratio (span/diameter) 1.33, ±40° cyclic pitch, figure of merit 0.6** (MEASURED).
- The brief's consistency check holds by construction: c/R 0.66 × AR 4 → span 2.64R → rotor AR 1.32 ≈ 1.33.
- Optimal **solidity range 0.30–0.40**; airfoil thickness up to 25%c efficient, thicker → wider usable pitch range.
- Thrust referenced on a **per-unit-blade-area** basis (consistent with the brief's premise).
- 17-lb dual-rotor technology demonstrator with a novel **split-blade** design; gimbal, tethered, and free-flight demonstrated.

> **CONFIRMS the brief's baseline geometry.** Note: the "0.67 figure of merit" that surfaces in searches belongs to *other* papers (a MAV-rotor CFD study), **not** Kellen's cyclorotor — the thesis states **0.6**.
> **GAP (could not extract from open sources):** the exact numeric blade-area C_T value, measured power loading in N/W, per-rotor thrust in N, RPM at the optimum, and dimensional radius/span — these require the thesis body figures. The thrust-vs-Re behaviour is answered via the validated CFD (non-dimensional thrust ~flat with Re; 2.3 above). To obtain the missing numbers, open the thesis body directly (CORE mirror or OAKTrust download).

#### 3.2 — Runco & Benedict 2023 (70 g quad)
Fully mined above (1.1/1.2); open access (CC BY-NC). Table 3 mass breakdown and Re ≈ 18,600 / ~10 gf-per-rotor operating point are the operative numbers.

#### 3.3 — Adams, Benedict, Hrishikeshavan, Chopra 2013, "Design, Development, and Flight Test of a Small-Scale Cyclogyro UAV Utilizing a Novel Cam-Based Passive Blade Pitching Mechanism," IJMAV 5(2):145–162 (open-access PDF)
535 g cyclogyro: two cyclorotors + horizontal tail rotor (9-in GWS 3-blade prop, AXI 2208/34 motor). **This is the closest published passive-pitching mechanism and is directly serviceable for your Stage 1 blade-pitch section.**
- **Cam geometry (MEASURED design):** passive, centrifugally driven. Blade CG placed *behind* the pitch axis so centrifugal force presses a cam-bearing against the inside of a cam ring slightly larger than the rotor; the cam-bearing rolls along the cam profile, setting blade pitch vs azimuth. A **circular cam** gives sinusoidal (hover-optimal) pitching; a **3D cam** (each axial cross-section a different 2D profile) generates curtate/prolate schedules for forward flight. Cam translated in Y/Z by two servos per rotor → controls both **pitch amplitude (0–55°)** and **phase (360° vectoring)**.
- **Achieved pitch schedule:** sinusoidal, operating amplitude **45°**; thrust-vector phase offset **β = 15–35°**.
- **Mechanism mass detail:** blades = single-layer carbon prepreg over foam core with rectangular cut-outs, **8 g → 5 g per blade**, 50 µm Mylar skin; cams SLA plastic reinforced with unidirectional CF thread; Delrin blade attachments; carbon-fibre/birch sandwich fuselage. Power: 78 g 11.1 V 45C 850 mAh (rotors + tail) + separate 15 g 1-cell (servos/processor); 3 g GINA processor.

---

## Recommendations

1. **Reframe Problem 1 around thrust density, not mass optimisation.** The Runco 70 g re-cut proves the tare fraction is already solved in the literature but that ultra-low-Re micro rotors give only ~1.0–1.2 module T/W. Anchor your case for reaching 2.5 on **operating near Re ~100,000** (where non-dimensional thrust holds and power falls — Shrestha & Benedict 2022) **plus amortising fixed non-blade masses** (bearings, ESC, linkages, motor) over ~5× the thrust. Do **not** claim scale shrinks blade-mass-per-thrust — the record says it is scale-invariant; concede this and move blade-mass savings onto materials/stress management (thinner CFRP skins, optimised cut-outs à la Adams).

2. **Treat the 0.607 transfer as defensible on Reynolds but risky on configuration.** Cite Re-invariance of non-dimensional thrust to justify carrying a thrust coefficient from Re 35k→100k, but run sizing with an explicit **sensitivity band** for the blade-count/airfoil/solidity change (order ±10–20%), not a single 15% haircut. **Threshold to revisit:** if your solidity leaves the measured-optimal **0.30–0.40** band, re-derive rather than transfer. Also carry the **peak-to-mean blade thrust ratio of 3–4** (Alsabri 2025) into blade structural sizing — cycle-averaged C_T hides it.

3. **Adopt NACA 0020 with confidence.** UAV-scale (Kellen: ≤25%c efficient, wider pitch range) and large-scale (Xisto: thickness raises power loading) both support it; document the modest peak-thrust-vs-power-loading tradeoff and the virtual-camber rationale (thickness buys margin at the top blade where separation first appears).

4. **Build the vectoring section on Adams β = 15–35° and Sirohi ~10°.** Present the phase-angle→thrust-direction map *with the RPM-dependent β offset* as your kinematic + performance analysis, and state the resultant thrust direction for every thrust number (the module must demonstrate vectoring by kinematic and performance analysis — this is exactly that).

5. **Size with margin against optimistic models.** Simple analytical/CFD tools over-predict thrust and under-predict power off-design (Xisto). Prefer your two agreeing measured power routes (152–161 W at the blade) and a validated aeroelastic model (Halder/Benedict) for cross-checks; treat DMST/analytical outputs as upper bounds on thrust and lower bounds on power.

6. **State the two genuine gaps explicitly in your submission** — no published cyclorotor states-and-meets a T/W target, and no tabulated blade-area C_T spread is openly available. Naming these bounds what is and isn't known strengthens credibility and pre-empts a reviewer assuming you missed them.

**Benchmarks that would change the plan:** if you can open the Kellen thesis body and extract a measured blade-area C_T for the 3-blade/NACA 0020/c/R 0.66 optimum, replace the transferred 0.607 with it directly (same family, same Re band) — that single number would retire most of Problem 2's risk. If your assembled mass budget cannot get the non-blade fixed masses below ~40% of the 400–530 g ceiling at 10–13 N, the T/W > 2.5 target is not reachable at your chosen radius and you should either raise thrust (larger radius, more power) or reduce the fixed-mass count (single motor per module, passive Adams-style pitch instead of per-blade servos).

---

## Caveats
- The Runco module re-cut (~1.0–1.2) is **my calculation** from Table 3 with an assumed mounting share; treat the exact figure as indicative, not measured — per-rotor structure/mounting allocation is not itemised in the paper.
- Kellen's exact blade-area C_T value, measured power loading (N/W), per-rotor thrust (N), and RPM at the optimum could **not** be extracted from open sources; they require the thesis body figures. The geometry, FM 0.6, solidity band (0.30–0.40), and airfoil finding (≤25%c efficient) are confirmed from the abstract and companion papers.
- Reynolds-invariance of non-dimensional thrust is a **SIMULATED (CFD) result validated against experiment**, not a directly transcribed measured Re-sweep table.
- The PUSHPAK CycloProp **problem statement itself** and any organiser clarification/corrigendum could not be found online; the module-boundary definition and mass ceilings in the brief are taken as given and could not be independently verified against a public source. Techfest's one-line description ("build-ready cycloidal rotor module for drones") is the only public framing located.
- Several key numeric plots (Benedict 2010 parametric C_T; Kellen figures; Hu airfoil-thickness curves) sit inside the primary figures and were characterised **directionally**, not transcribed value-by-value.