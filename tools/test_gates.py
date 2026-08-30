#!/usr/bin/env python3
"""Self-test for tools/check.py.

Builds throwaway repo trees in a temp directory and asserts that the gates pass an
honest design and reject specific attacks. Never touches the real repo.

    python tools/test_gates.py

Exit 0 means every case behaved as expected.
"""

import json
import math
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

CHECK = Path(__file__).resolve().parent / "check.py"
REAL_PDF = CHECK.parent.parent / "reference" / "cycloprop-problem-statement.pdf"
RHO, NU, G = 1.225, 1.5e-5, 9.81

FILLER = ("The rotor operates in a curvilinear flowfield so each chordwise station sees "
          "its own angle of attack, which is why simple blade element estimates carry a "
          "caveat here and why the published analytical tools overpredict thrust away "
          "from their design point. ") * 30


def schedule_points(amp, phase, step=10):
    """The pitch schedule the fixture writes and measures itself against. A pure cosine
    would fit the harmonic model exactly and leave a zero residual, which is not what a
    four-bar produces, so a small third harmonic rides on it."""
    pts = []
    for i in range(int(360 / step) + 1):
        az = i * step
        phi = math.radians(az - 90.0 - phase)
        pts.append((float(az), 0.98 * amp * math.cos(phi) + 0.02 * amp * math.cos(3 * phi)))
    return pts


def honest_numbers():
    R, nb = 0.14, 3
    c, S = 0.66 * R, 2.64 * R
    ct, ct_low, defl_loss = 0.607, 0.515, 0.15
    area = nb * c * S
    thrust = 13.5
    u = math.sqrt(thrust / (ct * 0.5 * RHO * area))
    rpm = u / R * 60 / (2 * math.pi)
    t_cons = ct_low * 0.5 * RHO * u * u * area
    # Aerodynamic power now has to clear the momentum bound and land at a figure of merit
    # a cyclorotor could actually reach. The old 118 W implied 0.84, which no cyclorotor
    # has ever reached, and the gate had nothing to say about it.
    mom_area = 2 * R * S
    ideal = thrust ** 1.5 / math.sqrt(2 * RHO * mom_area)
    ap, eff = 175.0, (0.92, 0.80, 0.95)
    fm = ideal / ap
    pl_ref = 0.070
    ap_pub = thrust / pl_ref
    spread = abs(ap - ap_pub) / ap

    budget = [
        {"item": "blades, 3 off", "mass_g": 108.0, "refines": "blades",
         "basis": "cfrp skin over foam core, volume times density with a layup allowance"},
        {"item": "endplates and frame", "mass_g": 74.0, "refines": "frame and endplates",
         "basis": "scaled from the Benedict quad rotor structure at this diameter"},
        {"item": "pitch linkage and offset disk", "mass_g": 33.0, "refines": "pitch mechanism",
         "basis": "part count times unit mass from the four bar layout drawing"},
        {"item": "hub and shaft", "mass_g": 44.0, "refines": "motor and drive",
         "basis": "7075 tube sized by the shaft torque margin calculation"},
        {"item": "bearings", "mass_g": 17.0, "refines": "motor and drive",
         "basis": "supplier datasheet masses for the selected bore sizes"},
        {"item": "motor", "mass_g": 62.0, "refines": "motor and drive",
         "basis": "supplier datasheet for a motor rated above continuous electrical power"},
        {"item": "esc and wiring", "mass_g": 21.0, "refines": "mounting hardware",
         "basis": "supplier datasheet plus a measured harness allowance"},
        {"item": "actuators, 2 off", "mass_g": 18.0, "refines": "actuators",
         "basis": "supplier datasheet for the amplitude and phase servos"},
        {"item": "mounting hardware and fasteners", "mass_g": 23.0, "refines": "mounting hardware",
         "basis": "fastener count times unit mass with a bracket allowance"},
    ]
    total = sum(b["mass_g"] for b in budget)
    omega = rpm * 2 * math.pi / 60
    # Per-blade mass is the blade budget over the blade count, not a free number.
    blade_mass = sum(b["mass_g"] for b in budget if "blade" in b["item"]) / 1000.0 / nb
    fc = blade_mass * omega ** 2 * R

    envelope = [
        {"item": "blades", "nominal_g": 108.0, "scaling_class": "geometry", "conservative_g": 122.0,
         "basis": "cfrp skin over foam core, volume times density with a layup allowance"},
        {"item": "frame and endplates", "nominal_g": 74.0, "scaling_class": "geometry", "conservative_g": 83.0,
         "basis": "scaled from the Benedict quad rotor structure at this diameter"},
        {"item": "pitch mechanism", "nominal_g": 33.0, "scaling_class": "geometry", "conservative_g": 38.0,
         "basis": "part count times unit mass from the four bar layout drawing"},
        {"item": "motor and drive", "nominal_g": 123.0, "scaling_class": "power", "conservative_g": 135.0,
         "basis": "supplier datasheet plus hub, shaft, bearings and transmission"},
        {"item": "actuators", "nominal_g": 18.0, "scaling_class": "fixed", "conservative_g": 21.0,
         "basis": "supplier datasheet for the amplitude and phase servos"},
        {"item": "mounting hardware", "nominal_g": 44.0, "scaling_class": "fixed", "conservative_g": 49.0,
         "basis": "fastener count times unit mass with a harness and bracket allowance"},
    ]
    env_nom = sum(e["nominal_g"] for e in envelope)
    m_cons = sum(e["conservative_g"] for e in envelope)

    tare = 13.0
    shaft = ap + tare
    elec = shaft / (eff[0] * eff[1] * eff[2])
    act_p, ctl_p = 6.0, 2.0

    # Structural demands derived from the design rather than asserted beside it.
    ratio, lever, load_factor = 2.0, S / 4, 4.0
    shaft_dem = shaft / omega
    blade_dem = thrust / nb * lever * load_factor
    blade_all, shaft_all = blade_dem * 2.9, shaft_dem * 3.0
    link_dem, link_all = 42.0, 95.0
    att_all = fc * 2.2

    # The azimuthal table is a distribution of the thrust, so its cycle mean has to
    # reproduce thrust per blade. A shape alone used to satisfy the gate.
    raw_az = [(a, abs(math.cos(math.radians(a))) + 0.12) for a in range(0, 360, 10)]
    az_scale = (thrust / nb) / (sum(v for _, v in raw_az) / len(raw_az))
    azimuthal = [(a, v * az_scale) for a, v in raw_az]

    amp, phase = 40, 9.0
    pts = schedule_points(amp, phase)
    model = [amp * math.cos(math.radians(a - 90.0 - phase)) for a, _ in pts]
    rms = math.sqrt(sum((p - m) ** 2 for (_, p), m in zip(pts, model)) / len(pts))

    sensitivity = [
        {"thrust_N": t,
         "mass_ceiling_g": math.floor(t / (2.5 * G) * 1000.0),
         "ideal_power_W": t ** 1.5 / math.sqrt(2 * RHO * mom_area),
         "rpm": rpm * math.sqrt(t / thrust)}
        for t in (10.0, 12.0, thrust)
    ]

    return {
        "geometry": {"radius_m": R, "chord_m": c, "span_m": S, "blades": nb,
                     "airfoil": "NACA 0020", "pitch_amplitude_deg": amp,
                     "pitch_axis_pct_chord": 25},
        "operating": {"rpm": rpm, "tip_speed_ms": u, "reynolds": u * c / NU},
        "performance": {"thrust_N": thrust, "blade_area_coeff": ct,
                        "blade_area_coeff_low": ct_low, "thrust_N_conservative": t_cons,
                        "aero_power_W": ap, "tare_power_W": tare,
                        "electrical_power_W": elec,
                        "actuator_power_W": act_p, "controller_power_W": ctl_p,
                        "module_electrical_power_W": elec + act_p + ctl_p,
                        "momentum_area_m2": mom_area, "ideal_power_W": ideal,
                        "figure_of_merit": fm, "power_loading_ref_N_per_W": pl_ref,
                        "aero_power_W_published": ap_pub, "power_spread": spread,
                        "blade_deflection_thrust_loss": defl_loss},
        "efficiency": {"transmission": eff[0], "motor": eff[1], "esc": eff[2]},
        "power_by_radius": [{"radius_m": r, "aero_power_W": ap * 0.14 / r}
                            for r in (0.10, 0.12, 0.14, 0.16)],
        "thrust_sensitivity": sensitivity,
        "configuration_candidates": [
            {"config": "single rotor", "rotors": 1, "module_mass_g": env_nom,
             "thrust_N": thrust, "module_tw": thrust / (env_nom / 1000 * G),
             "module_tw_conservative": t_cons / (m_cons / 1000 * G), "selected": True},
            {"config": "two rotor cluster", "rotors": 2, "module_mass_g": 470.0,
             "thrust_N": thrust, "module_tw": thrust / (0.470 * G),
             "module_tw_conservative": t_cons / (0.540 * G), "selected": False},
            {"config": "three rotor cluster", "rotors": 3, "module_mass_g": 540.0,
             "thrust_N": thrust, "module_tw": thrust / (0.540 * G),
             "module_tw_conservative": t_cons / (0.620 * G), "selected": False}],
        "coefficient_scenarios": [
            {"name": "nominal", "blade_area_coeff": ct, "evidence_class": "derived",
             "basis": "Benedict 2010 quad rotor at its hover point, transferred"},
            {"name": "downside", "blade_area_coeff": ct_low, "evidence_class": "downside",
             "basis": "nominal reduced by the stated blade deflection loss"},
            {"name": "upside", "blade_area_coeff": ct * 1.05, "evidence_class": "derived",
             "basis": "thicker section benefit reported at UAV scale"}],
        "aero_azimuthal_loads": [
            {"azimuth_deg": a, "normal_force_N": v} for a, v in azimuthal],
        "drive_candidates": [
            {"name": "outrunner A", "continuous_power_W": 320.0, "kv": 400,
             "continuous_current_A": 67.0, "continuous_torque_Nm": 9.5493 / 400 * 67.0,
             "mass_g": 62.0, "selected": True},
            {"name": "outrunner B", "continuous_power_W": 400.0, "kv": 350,
             "continuous_current_A": 77.0, "continuous_torque_Nm": 9.5493 / 350 * 77.0,
             "mass_g": 88.0, "selected": False}],
        "linkage_dimensions": [
            {"link": "crank", "length_mm": 24.0}, {"link": "coupler", "length_mm": 61.0},
            {"link": "rocker", "length_mm": 33.0}, {"link": "ground", "length_mm": 70.0}],
        "pitch_schedule": [{"azimuth_deg": a, "pitch_deg": pv} for a, pv in pts],
        "vector_map": [
            {"phase_command_deg": ph, "vertical_force_N": thrust * math.cos(math.radians(ph)),
             "lateral_force_N": thrust * math.sin(math.radians(ph))}
            for ph in (0.0, 30.0, 60.0)],
        "pitch": {"mechanism": "passive four-bar", "offset_m": 0.024,
                  "phase_delay_deg": phase, "vector_range_deg": 360.0,
                  "phase_authority_deg": 360.0, "schedule_rms_residual_deg": rms,
                  "actuator_count": 2, "actuator_mass_g": 18.0,
                  "side_force_tilt_deg": 28.0},
        "packaging": {"envelope_length_mm": 400, "envelope_width_mm": 300,
                      "envelope_height_mm": 300, "mount_points": 4},
        "structure": {"blade_mass_kg": blade_mass, "centrifugal_load_N": fc,
                      "blade_root_bending_Nm": blade_dem, "shaft_torque_Nm": shaft_dem,
                      "blade_allowable_Nm": blade_all, "shaft_allowable_Nm": shaft_all,
                      "blade_margin": blade_all / blade_dem,
                      "shaft_margin": shaft_all / shaft_dem,
                      "transmission_ratio": ratio,
                      "torque_reference": "rotor shaft, upstream of the 2 to 1 reduction",
                      "blade_load_lever_m": lever, "blade_load_factor": load_factor,
                      "pitch_link_load_N": link_dem, "pitch_link_allowable_N": link_all,
                      "pitch_link_margin": link_all / link_dem,
                      "blade_attachment_allowable_N": att_all,
                      "blade_attachment_margin": att_all / fc},
        "mass_envelope_g": envelope,
        "mass_budget_g": budget,
        "sources": {
            "performance": {
                "blade_area_coeff": "derived from the Benedict 2010 quad rotor at its hover point",
                "blade_area_coeff_low": "lower bound from the spread across blade count and airfoil in Benedict 2010",
                "momentum_area_m2": "projected frontal area, 2R times span, the closure Benedict uses for cyclorotors",
                "power_loading_ref_N_per_W": "measured power loading from the Benedict 2010 rig at its hover point",
                "blade_deflection_thrust_loss": "thrust loss from blade deflection at the chosen skin thickness, bounded against Benedict and Chopra"},
            "structure": {
                "blade_root_bending_Nm": "thrust per blade over a quarter span lever with a peak to mean factor of 2",
                "shaft_torque_Nm": "shaft power divided by rotor angular speed at the design point",
                "pitch_link_load_N": "four bar link load from the offset disk reaction at peak pitching moment"}},
        "results": {"total_mass_g": total, "weight_N": total / 1000 * G,
                    "thrust_to_weight": thrust / (total / 1000 * G),
                    "mass_envelope_g": env_nom, "mass_g_conservative": m_cons,
                    "thrust_to_weight_conservative": t_cons / (m_cons / 1000 * G)},
    }


def rnd(v, n):
    """Adversarial fixtures put strings in numeric fields on purpose, so the
    builder must not choke before the gate gets a chance to reject them."""
    return round(v, n) if isinstance(v, (int, float)) and not isinstance(v, bool) else v


def doc(path, headings, numbers=(), words=600):
    body = [f"# {headings[0]}", "", FILLER[:words * 6], ""]
    for h in headings[1:]:
        body += [f"## {h}", "", FILLER[:words * 3], ""]
    numbers = [(k, v) for k, v in numbers if v is not None]
    if numbers:
        body += ["## Numbers used", ""] + [f"- {k} = {v}" for k, v in numbers] + [""]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(body), encoding="utf-8")


def pitch_doc(path, numbers, points=None):
    rows = ["| azimuth | pitch |", "| --- | --- |"]
    for a, p in (points if points is not None else schedule_points(40, 9.0)):
        rows.append(f"| {a:.0f} | {p:.2f} |")
    body = ["# Pitch mechanism", "", FILLER[:2000], "", "## Kinematics", "",
            FILLER[:1500], "", "## Pitch schedule", ""] + rows + [
        "", "## Thrust vectoring", "", FILLER[:1500], "", "## Side force", "",
        FILLER[:1200], "", "## Numbers used", ""] + [f"- {k} = {v}" for k, v in numbers]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(body), encoding="utf-8")


REQUIRED_ITEMS = [
    "Cyclorotor concept and configuration",
    "Preliminary rotor sizing",
    "Blade arrangement and pitch-control concept",
    "Estimated thrust and power requirement",
    "Estimated module weight and thrust-to-weight ratio",
    "Initial material and manufacturing approach",
    "Team capability and execution plan",
]

CRITERIA_ROWS = [
    ("10 N thrust capability", "Estimated thrust and power requirement"),
    ("thrust-to-weight above 2.5", "Estimated module weight and thrust-to-weight ratio"),
    ("kinematic analysis of pitching and vectoring", "Blade arrangement and pitch-control concept"),
    ("aerodynamic analysis", "Estimated thrust and power requirement"),
    ("structural analysis", "Estimated module weight and thrust-to-weight ratio"),
    ("manufacturability", "Initial material and manufacturing approach"),
    ("packaging and integration", "Cyclorotor concept and configuration"),
    ("presentation quality", "Team capability and execution plan"),
]


def make_pdf(path, pages):
    """A real multi-page PDF, written by hand so the fixture does not need pandoc. The
    week 5 gate now reads the attachment back, so copying an unrelated PDF no longer
    stands in for building one."""
    def esc(s):
        return s.replace("\\", r"\\").replace("(", r"\(").replace(")", r"\)")

    objs = ["<< /Type /Catalog /Pages 2 0 R >>", "",
            "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>"]
    page_ids = [4 + 2 * i for i in range(len(pages))]
    objs[1] = (f"<< /Type /Pages /Count {len(pages)} /Kids "
               f"[{' '.join(f'{i} 0 R' for i in page_ids)}] >>")
    for i, lines in enumerate(pages):
        objs.append(f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources "
                    f"<< /Font << /F1 3 0 R >> >> /Contents {5 + 2 * i} 0 R >>")
        stream = ("BT /F1 11 Tf 54 740 Td 15 TL\n"
                  + "\n".join(f"({esc(l)}) Tj T*" for l in lines) + "\nET")
        objs.append(f"<< /Length {len(stream)} >>\nstream\n{stream}\nendstream")

    out, offsets = "%PDF-1.4\n", []
    for i, o in enumerate(objs, 1):
        offsets.append(len(out))
        out += f"{i} 0 obj\n{o}\nendobj\n"
    start = len(out)
    out += f"xref\n0 {len(objs) + 1}\n0000000000 65535 f \n"
    out += "".join(f"{o:010d} 00000 n \n" for o in offsets)
    out += f"trailer\n<< /Size {len(objs) + 1} /Root 1 0 R >>\nstartxref\n{start}\n%%EOF\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(out.encode("latin-1"))


def submission_doc(path, data, rows=None, items=None):
    """A submission that clears every week 5 gate. Nothing had ever built one, so the
    criteria map had never been exercised on a document meant to pass."""
    body = ["# CycloProp Stage 1 submission", ""]
    for h in (items if items is not None else REQUIRED_ITEMS):
        body += [f"## {h}", "", FILLER[:2600], ""]
    body += ["## Evaluation criteria map", "",
             "| Criterion | Where it is answered |", "| --- | --- |"]
    for crit, where in (rows if rows is not None else CRITERIA_ROWS):
        body.append(f"| {crit} | {where} |")
    perf, geo = data["performance"], data["geometry"]
    body += ["", "## Numbers used", "",
             f"- performance.thrust_N = {rnd(perf['thrust_N'], 2)}",
             f"- geometry.radius_m = {geo['radius_m']}",
             f"- results.thrust_to_weight = {rnd(data['results']['thrust_to_weight'], 3)}", ""]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(body), encoding="utf-8")


def build(root, data, upto=4):
    d = Path(root)
    doc(d / "context.md", ["Context", "Stage 1: the seven required items",
                           "Evaluation criteria", "The thrust-to-weight basis, settled"])
    doc(d / "stage-1" / "plan.md", ["Plan", "Calendar"])
    doc(d / "stage-1" / "design" / "evidence-ledger.md",
        ["Evidence ledger", "Selection rules"])
    doc(d / "stage-1" / "literature.md",
        ["Literature", "Geometry and measured performance", "Published mass breakdowns"])
    (d / "stage-1" / "design").mkdir(parents=True, exist_ok=True)
    (d / "stage-1" / "design" / "numbers.json").write_text(
        json.dumps(data, indent=2), encoding="utf-8")

    g = d / "stage-1" / "design"
    if upto >= 2:
        geo, perf = data["geometry"], data["performance"]
        doc(g / "01-configuration.md", ["Configuration", "Why this configuration"],
            [("geometry.blades", geo["blades"]), ("geometry.radius_m", geo["radius_m"]),
             ("geometry.span_m", rnd(geo["span_m"], 4))])
        doc(g / "02-rotor-sizing.md", ["Rotor sizing", "Shape family", "Radius"],
            [("geometry.radius_m", geo["radius_m"]), ("geometry.chord_m", rnd(geo["chord_m"], 4)),
             ("operating.rpm", rnd(data["operating"]["rpm"], 1))])
        doc(g / "04-thrust-and-power.md", ["Thrust", "Power", "Sensitivity"],
            [("performance.thrust_N", rnd(perf["thrust_N"], 2)),
             ("performance.aero_power_W", perf["aero_power_W"]),
             ("performance.module_electrical_power_W", rnd(perf["module_electrical_power_W"], 1))])
    if upto >= 3:
        pit, pack = data["pitch"], data["packaging"]
        pitch_doc(g / "03-pitch-and-vectoring.md",
                  [("pitch.vector_range_deg", pit["vector_range_deg"]),
                   ("pitch.offset_m", pit["offset_m"]),
                   ("pitch.phase_delay_deg", pit["phase_delay_deg"])])
        doc(g / "09-packaging-and-integration.md",
            ["Package envelope", "Mounting", "Drivetrain", "Interfaces"],
            [("packaging.mount_points", pack["mount_points"]),
             ("packaging.envelope_length_mm", pack["envelope_length_mm"]),
             ("packaging.envelope_height_mm", pack["envelope_height_mm"])])
    if upto >= 4:
        res, st = data["results"], data["structure"]
        doc(g / "05-mass-and-tw.md", ["Mass budget", "Thrust-to-weight", "Margin"],
            [("results.total_mass_g", res["total_mass_g"]),
             ("results.weight_N", rnd(res["weight_N"], 3)),
             ("results.thrust_to_weight", rnd(res["thrust_to_weight"], 3))])
        doc(g / "06-materials-and-manufacturing.md",
            ["Material selection", "Manufacturing", "Cost"],
            [("results.total_mass_g", res["total_mass_g"]),
             ("results.mass_envelope_g", res.get("mass_envelope_g")),
             ("results.mass_g_conservative", res.get("mass_g_conservative"))])
        doc(g / "08-structure-and-loads.md",
            ["Load cases", "Blade", "Shaft", "Margins"],
            [("structure.blade_margin", rnd(st["blade_margin"], 3)),
             ("structure.shaft_margin", rnd(st["shaft_margin"], 3)),
             ("structure.centrifugal_load_N", rnd(st["centrifugal_load_N"], 2))])
    if upto >= 5:
        doc(g / "07-team-and-execution.md", ["Team capability", "Execution plan", "Stage 2"])
        sub = d / "stage-1" / "submission"
        submission_doc(sub / "cycloprop-stage1.md", data)
        build_pdf_from(sub / "cycloprop-stage1.md", sub / "cycloprop-stage1.pdf")
        (sub / "email-draft.md").write_text(
            "\n".join(["# Stage 1 submission email", "",
                       "To: pushpak_gc2026@aero.iitb.ac.in",
                       "Subject: PUSHPAK Grand Challenge, CycloProp Stage 1", "",
                       "The attachment is cycloprop-stage1.pdf and it carries the full",
                       "design report for the module.", ""]), encoding="utf-8")
        (d / "stage-1" / "human-gate.md").write_text(
            "\n".join(["# Week H", "", "REGISTRATION-CONFIRMED", "ELIGIBILITY-CHECKED",
                       "ROSTER-CONFIRMED", "SENDER-CONFIRMED",
                       "TECHNICAL-READ-COMPLETE", ""]), encoding="utf-8")
    return d


def build_pdf_from(md, pdf):
    """Stands in for the pandoc build: every heading and every declared number reaches the
    attachment, which is what the identity gate reads back."""
    lines = [l.lstrip("# ").rstrip() for l in md.read_text(encoding="utf-8").splitlines()
             if l.startswith("#") or l.strip().startswith("- ")]
    pages = [lines[i:i + 6] or ["(blank)"] for i in range(0, max(len(lines), 1), 6)]
    while len(pages) < 4:
        pages.append(["CycloProp Stage 1, continued"])
    make_pdf(pdf, pages)


def run(root, week):
    r = subprocess.run([sys.executable, str(CHECK), "--week", str(week), "--root", str(root)],
                       capture_output=True, text=True)
    return r.returncode, r.stdout


CASES = []


def case(name, expect_pass, mutate=None, upto=4, week=4, tweak=None):
    """mutate edits numbers.json before the tree is built. tweak edits the built tree,
    for attacks that live in the prose rather than in the data."""
    CASES.append((name, expect_pass, mutate, upto, week, tweak))


case("honest design passes weeks 1 to 4", True)
case("honest design passes week 2 alone", True, upto=2, week=2)


def f3_exploit(d):
    """Two errors of 1.9 percent in opposite directions. Passed the old 2 percent gate."""
    d["performance"]["thrust_N"] *= 1.019          # overstate thrust
    d["results"]["total_mass_g"] *= 0.981          # understate mass
    d["results"]["weight_N"] = d["results"]["total_mass_g"] / 1000 * G
    d["results"]["thrust_to_weight"] = d["performance"]["thrust_N"] / d["results"]["weight_N"]
    return d


case("F3 compounding tolerance exploit is rejected", False, f3_exploit)


def thin_conservative(d):
    d["performance"]["blade_area_coeff_low"] = d["performance"]["blade_area_coeff"]
    d["performance"]["thrust_N_conservative"] = d["performance"]["thrust_N"]
    return d


case("conservative coefficient equal to nominal is rejected", False, thin_conservative, week=2)


def heavy(d):
    for b in d["mass_budget_g"]:
        b["mass_g"] *= 1.9
    t = sum(b["mass_g"] for b in d["mass_budget_g"])
    d["results"].update(total_mass_g=t, weight_N=t / 1000 * G,
                        thrust_to_weight=d["performance"]["thrust_N"] / (t / 1000 * G),
                        mass_g_conservative=t * 1.1,
                        thrust_to_weight_conservative=d["performance"]["thrust_N_conservative"]
                        / (t * 1.1 / 1000 * G))
    return d


case("a module too heavy for T/W 2.5 is rejected", False, heavy)


def thin_basis(d):
    d["mass_budget_g"][0]["basis"] = "est."
    return d


case("a one-word mass basis is rejected", False, thin_basis)


def tiny_line(d):
    d["mass_budget_g"][2]["mass_g"] = 0.01
    t = sum(b["mass_g"] for b in d["mass_budget_g"])
    d["results"]["total_mass_g"] = t
    d["results"]["weight_N"] = t / 1000 * G
    d["results"]["thrust_to_weight"] = d["performance"]["thrust_N"] / (t / 1000 * G)
    return d


case("a vanishing mass line is rejected", False, tiny_line)


def zero_actuators(d):
    d["pitch"]["actuator_count"] = 0
    return d


case("zero actuators is rejected", False, zero_actuators, week=3)


def weak_margin(d):
    d["structure"]["blade_margin"] = 1.05
    return d


case("a structural margin below 1.5 is rejected", False, weak_margin)


# ---- round 3 adversarial cases -------------------------------------------------

def text_in_week3_numerics(d):
    for k in ("offset_m", "phase_delay_deg", "actuator_mass_g", "side_force_tilt_deg"):
        d["pitch"][k] = "to be confirmed in stage 2"
    for k in ("envelope_length_mm", "envelope_width_mm", "envelope_height_mm"):
        d["packaging"][k] = "tbd"
    return d


case("text in week 3 numeric fields is rejected", False, text_in_week3_numerics, week=3)


def text_in_week4_numerics(d):
    for k in ("centrifugal_load_N", "blade_root_bending_Nm", "shaft_torque_Nm", "shaft_margin"):
        d["structure"][k] = "see stage 2"
    return d


case("text in week 4 structural fields is rejected", False, text_in_week4_numerics)


def text_efficiencies_and_empty_sweep(d):
    for k in ("transmission", "motor", "esc"):
        d["efficiency"][k] = "typical"
    d["power_by_radius"] = [{}, {}, {}]
    return d


case("text efficiencies and empty sweep rows are rejected", False,
     text_efficiencies_and_empty_sweep, week=2)


def trivial_conservatism(d):
    d["performance"]["blade_area_coeff_low"] = d["performance"]["blade_area_coeff"] * 0.9999
    d["performance"]["thrust_N_conservative"] = d["performance"]["thrust_N"] * 0.9999
    d["results"]["mass_g_conservative"] = d["results"]["total_mass_g"]
    return d


case("a conservative case that is not meaningfully conservative is rejected", False,
     trivial_conservatism, week=2)


def scalar_envelope(d):
    d["mass_envelope_g"] = 400.0                     # scalar, not a component list
    return d


case("a week 2 mass envelope that is not a component list is rejected", False,
     scalar_envelope, week=2)


def stated_not_derived_margin(d):
    d["structure"]["blade_margin"] = 9.9             # does not follow from allowable / demand
    return d


case("a structural margin that does not follow from allowable over demand is rejected",
     False, stated_not_derived_margin)


def lighter_conservative_line(d):
    d["mass_envelope_g"][0]["conservative_g"] = d["mass_envelope_g"][0]["nominal_g"] - 5
    return d


case("an envelope line lighter in the conservative column is rejected", False,
     lighter_conservative_line, week=2)


def thin_envelope_margin(d):
    for e in d["mass_envelope_g"]:
        e["conservative_g"] = e["nominal_g"] * 1.03      # 3 percent, rule wants 5
    d["results"]["mass_g_conservative"] = sum(e["conservative_g"] for e in d["mass_envelope_g"])
    return d


case("a conservative column only 3 percent above nominal is rejected", False,
     thin_envelope_margin, week=2)


def missing_envelope_total(d):
    d["results"].pop("mass_envelope_g", None)
    return d


case("a missing nominal envelope total is rejected", False, missing_envelope_total, week=2)


def flat_power_sweep(d):
    d["power_by_radius"] = [{"radius_m": r, "aero_power_W": 1.0}
                            for r in (0.10, 0.12, 0.14, 0.16)]
    return d


case("a power sweep that does not vary with radius is rejected", False,
     flat_power_sweep, week=2)


def sweep_without_chosen_radius(d):
    d["power_by_radius"] = [{"radius_m": r, "aero_power_W": 118.0 * 0.14 / r}
                            for r in (0.10, 0.12, 0.16)]
    return d


case("a sweep that omits the chosen radius is rejected", False,
     sweep_without_chosen_radius, week=2)


def budget_drifts_from_envelope(d):
    for b in d["mass_budget_g"]:
        b["mass_g"] *= 0.6                    # a silent redesign, not a refinement
    t = sum(b["mass_g"] for b in d["mass_budget_g"])
    d["results"].update(total_mass_g=t, weight_N=t / 1000 * G,
                        thrust_to_weight=d["performance"]["thrust_N"] / (t / 1000 * G))
    return d


case("a week 4 budget that drifts from the week 2 envelope is rejected", False,
     budget_drifts_from_envelope)


# ---- round 5 adversarial cases -------------------------------------------------

def sweep_off_design_point(d):
    """A curve with the right 1/R shape that does not pass through the design power."""
    d["power_by_radius"] = [{"radius_m": r, "aero_power_W": 50.0 * 0.14 / r}
                            for r in (0.10, 0.12, 0.14, 0.16)]
    return d


case("a power sweep not anchored to the design point is rejected", False,
     sweep_off_design_point, week=2)


def component_redesign_at_constant_total(d):
    """Everything into the blades, every other line at the minimum legal mass, total
    preserved. The old total-only continuity check passed this."""
    budget = d["mass_budget_g"]
    freed = sum(b["mass_g"] for b in budget[1:]) - 0.5 * len(budget[1:])
    for b in budget[1:]:
        b["mass_g"] = 0.5
    budget[0]["mass_g"] += freed
    return d


case("a component redesign that preserves the total is rejected", False,
     component_redesign_at_constant_total)


def budget_line_refines_nothing(d):
    d["mass_budget_g"][3]["refines"] = "a group that is not in the envelope"
    return d


case("a mass line refining no envelope line is rejected", False, budget_line_refines_nothing)


def duplicate_envelope_names(d):
    d["mass_envelope_g"][1]["item"] = d["mass_envelope_g"][0]["item"]
    return d


case("two envelope lines sharing one name is rejected", False, duplicate_envelope_names,
     week=2)


# ---- round 6: the goal audit, where green gates did not mean feasible ----------

def thrust_from_one_watt(d):
    """13.5 N of thrust produced by 1 W of aerodynamic power. Every stored value agrees
    with every other stored value, and the design is impossible."""
    p, eff = d["performance"], d["efficiency"]
    p["aero_power_W"], p["tare_power_W"] = 1.0, 0.1
    elec = 1.1 / (eff["transmission"] * eff["motor"] * eff["esc"])
    p["electrical_power_W"] = elec
    p["module_electrical_power_W"] = elec + p["actuator_power_W"] + p["controller_power_W"]
    p["figure_of_merit"] = p["ideal_power_W"] / 1.0
    p["power_spread"] = abs(1.0 - p["aero_power_W_published"]) / 1.0
    d["power_by_radius"] = [{"radius_m": r, "aero_power_W": 1.0 * 0.14 / r}
                            for r in (0.10, 0.12, 0.14, 0.16)]
    return d


case("thrust produced by one watt is rejected", False, thrust_from_one_watt, week=2)


def inflated_momentum_area(d):
    """Softening the bound by claiming a bigger disk than the rotor presents."""
    p = d["performance"]
    p["momentum_area_m2"] *= 4.0
    p["ideal_power_W"] = p["thrust_N"] ** 1.5 / math.sqrt(2 * RHO * p["momentum_area_m2"])
    p["figure_of_merit"] = p["ideal_power_W"] / p["aero_power_W"]
    return d


case("a momentum area larger than the projected area is rejected", False,
     inflated_momentum_area, week=2)


def disconnected_structure(d):
    """1 g blades beside a 108 g blade budget, with loads to match and margins of 2."""
    st = d["structure"]
    st["blade_mass_kg"] = 0.001
    st["blade_root_bending_Nm"] = st["shaft_torque_Nm"] = 0.001
    st["blade_allowable_Nm"] = st["shaft_allowable_Nm"] = 0.002
    st["blade_margin"] = st["shaft_margin"] = 2.0
    st["centrifugal_load_N"] = 0.001 * (d["operating"]["rpm"] * 2 * math.pi / 60) ** 2 \
        * d["geometry"]["radius_m"]
    return d


case("structural loads disconnected from the design are rejected", False,
     disconnected_structure)


def asserted_shaft_torque(d):
    """Shaft torque a reviewer can recompute from power and speed in ten seconds."""
    d["structure"]["shaft_torque_Nm"] *= 0.4
    d["structure"]["shaft_margin"] = (d["structure"]["shaft_allowable_Nm"]
                                      / d["structure"]["shaft_torque_Nm"])
    return d


case("shaft torque that does not follow from power and speed is rejected", False,
     asserted_shaft_torque)


def fractional_hardware(d):
    d["pitch"]["actuator_count"] = 0.5
    d["packaging"]["mount_points"] = 0.1
    return d


case("half an actuator and a tenth of a mount point are rejected", False,
     fractional_hardware, week=3)


def flat_pitch_schedule(root, data):
    """A 37 point schedule spanning the revolution with no pitching motion in it."""
    pitch_doc(root / "stage-1" / "design" / "03-pitch-and-vectoring.md",
              [("pitch.vector_range_deg", data["pitch"]["vector_range_deg"]),
               ("pitch.offset_m", data["pitch"]["offset_m"]),
               ("pitch.phase_delay_deg", data["pitch"]["phase_delay_deg"])],
              points=[(a, 0.0) for a, _ in schedule_points(40, 9.0)])


case("a pitch schedule with no motion in it is rejected", False, week=3, upto=3,
     tweak=flat_pitch_schedule)


def wrong_phase_in_schedule(root, data):
    """The table shows one phase and the stated number claims another."""
    pitch_doc(root / "stage-1" / "design" / "03-pitch-and-vectoring.md",
              [("pitch.vector_range_deg", data["pitch"]["vector_range_deg"]),
               ("pitch.offset_m", data["pitch"]["offset_m"]),
               ("pitch.phase_delay_deg", data["pitch"]["phase_delay_deg"])],
              points=schedule_points(40, 70.0))


case("a stated phase delay the schedule does not show is rejected", False, week=3, upto=3,
     tweak=wrong_phase_in_schedule)


def vectoring_beyond_authority(d):
    d["pitch"]["phase_authority_deg"] = 90.0     # the mechanism, against a claimed 360
    return d


case("a vectoring range wider than the mechanism allows is rejected", False,
     vectoring_beyond_authority, week=3)


def thrust_not_prequalified(d):
    d["thrust_sensitivity"] = [r for r in d["thrust_sensitivity"] if r["thrust_N"] != 13.5]
    d["thrust_sensitivity"].append({"thrust_N": 11.0,
                                    "mass_ceiling_g": math.floor(11.0 / (2.5 * G) * 1000.0),
                                    "ideal_power_W": 11.0 ** 1.5 / math.sqrt(
                                        2 * RHO * d["performance"]["momentum_area_m2"]),
                                    "rpm": 1150.0})
    return d


case("a design thrust outside the sensitivity table is rejected", False,
     thrust_not_prequalified, week=2)


def wrong_mass_ceiling(d):
    d["thrust_sensitivity"][0]["mass_ceiling_g"] = 600.0
    return d


case("a sensitivity row whose mass ceiling does not follow is rejected", False,
     wrong_mass_ceiling, week=2)


# ---- round 7: schema added by review with no gate behind it --------------------

def empty_candidate_list(d):
    d["configuration_candidates"] = []
    return d


case("a configuration comparison with no candidates is rejected", False,
     empty_candidate_list, week=2)


def one_coefficient_scenario(d):
    d["coefficient_scenarios"] = d["coefficient_scenarios"][:1]
    return d


case("a single coefficient scenario is rejected", False, one_coefficient_scenario, week=2)


def unlabelled_scenario(d):
    d["coefficient_scenarios"][1]["evidence_class"] = "published lower bound"
    return d


case("a downside scenario dressed as a published bound is rejected", False,
     unlabelled_scenario, week=2)


def envelope_without_scaling_class(d):
    for e in d["mass_envelope_g"]:
        e.pop("scaling_class", None)
    return d


case("a mass envelope with no scaling class is rejected", False,
     envelope_without_scaling_class, week=2)


def motor_called_fixed(d):
    for e in d["mass_envelope_g"]:
        if "motor" in e["item"]:
            e["scaling_class"] = "constant"      # not one of the three allowed classes
    return d


case("a scaling class outside the three allowed is rejected", False,
     motor_called_fixed, week=2)


def two_phase_commands(d):
    d["vector_map"] = d["vector_map"][:2]
    return d


case("a vector map with fewer than three phase commands is rejected", False,
     two_phase_commands, week=3)


def incomplete_drive_row(d):
    d["drive_candidates"][0].pop("continuous_torque_Nm")
    return d


case("a drive candidate with no continuous torque is rejected", False,
     incomplete_drive_row, week=2)


# ---- week 2 selection gates, added after the week 2 audit -------------------------
# Before these, a 36 row table of arbitrary positive numbers satisfied the azimuthal
# check identically to a calibrated one, and nothing asked whether the drive the design
# names could actually hold the design point.


def azimuthal_not_calibrated(d):
    d["aero_azimuthal_loads"] = [{"azimuth_deg": r["azimuth_deg"], "normal_force_N": 1.0}
                                 for r in d["aero_azimuthal_loads"]]
    return d


case("an azimuthal table that does not average to the design thrust is rejected", False,
     azimuthal_not_calibrated, week=2)


def azimuthal_ten_percent_high(d):
    for r in d["aero_azimuthal_loads"]:
        r["normal_force_N"] *= 1.10
    return d


case("an azimuthal table overstated by 10 percent is rejected", False,
     azimuthal_ten_percent_high, week=2)


def two_drives_selected(d):
    for x in d["drive_candidates"]:
        x["selected"] = True
    return d


case("two drive candidates marked selected is rejected", False, two_drives_selected,
     week=2)


def no_drive_selected(d):
    for x in d["drive_candidates"]:
        x["selected"] = False
    return d


case("a drive shortlist with nothing selected is rejected", False, no_drive_selected,
     week=2)


def drive_under_continuous_rating(d):
    sel = [x for x in d["drive_candidates"] if x["selected"]][0]
    sel["continuous_power_W"] = 90.0
    return d


case("a selected drive below the continuous power the design point needs is rejected",
     False, drive_under_continuous_rating, week=2)


def drive_torque_not_from_kv(d):
    d["drive_candidates"][0]["continuous_torque_Nm"] *= 1.4
    return d


case("a continuous torque that does not follow from KV and current is rejected", False,
     drive_torque_not_from_kv, week=2)


def drive_without_kv(d):
    d["drive_candidates"][0].pop("kv")
    return d


case("a drive candidate with no KV is rejected", False, drive_without_kv, week=2)


def two_candidates_selected(d):
    for x in d["configuration_candidates"]:
        x["selected"] = True
    return d


case("two configuration candidates marked selected is rejected", False,
     two_candidates_selected, week=2)


def no_candidate_selected(d):
    for x in d["configuration_candidates"]:
        x["selected"] = False
    return d


case("a candidate comparison with nothing selected is rejected", False,
     no_candidate_selected, week=2)


def selected_candidate_loses(d):
    d["configuration_candidates"][1]["module_tw_conservative"] = \
        d["configuration_candidates"][0]["module_tw_conservative"] * 1.2
    return d


case("a selected candidate that loses on conservative T/W is rejected", False,
     selected_candidate_loses, week=2)


def candidate_mass_off_envelope(d):
    sel = [x for x in d["configuration_candidates"] if x["selected"]][0]
    sel["module_mass_g"] *= 0.85
    return d


case("a selected candidate whose mass is not the envelope total is rejected", False,
     candidate_mass_off_envelope, week=2)


def candidates_without_conservative_tw(d):
    for x in d["configuration_candidates"]:
        x.pop("module_tw_conservative", None)
    return d


case("a candidate table with no conservative T/W is rejected", False,
     candidates_without_conservative_tw, week=2)



def no_evidence_ledger(root, data):
    (root / "stage-1" / "design" / "evidence-ledger.md").unlink()


case("week 2 without an evidence ledger is rejected", False, week=2, upto=2,
     tweak=no_evidence_ledger)


def technical_read_outstanding(root, data):
    p = root / "stage-1" / "human-gate.md"
    p.write_text(p.read_text(encoding="utf-8")
                 .replace("TECHNICAL-READ-COMPLETE", "TECHNICAL-READ-PENDING"),
                 encoding="utf-8")


case("staging before a human has read the PDF is rejected", False, upto=5, week=5,
     tweak=technical_read_outstanding)


# ---- week 5, which nothing had ever exercised on a passing document ------------

SUB = "stage-1/submission/cycloprop-stage1.md"

case("an honest submission passes weeks 1 to 5", True, upto=5, week=5)


def short_criteria_table(root, data):
    submission_doc(root / SUB, data, rows=CRITERIA_ROWS[:7])


case("a criteria map covering only 7 criteria is rejected", False, upto=5, week=5,
     tweak=short_criteria_table)


def criteria_prose_not_table(root, data):
    """The eight criteria named in a paragraph rather than mapped in a table."""
    text = (root / SUB).read_text(encoding="utf-8")
    kept = [l for l in text.splitlines() if not l.strip().startswith("|")]
    kept.insert(kept.index("## Evaluation criteria map") + 1,
                "This report answers " + ", ".join(c for c, _ in CRITERIA_ROWS) + ".")
    (root / SUB).write_text("\n".join(kept), encoding="utf-8")


case("criteria named in prose instead of mapped in a table is rejected", False,
     upto=5, week=5, tweak=criteria_prose_not_table)


def missing_required_item(root, data):
    submission_doc(root / SUB, data, items=REQUIRED_ITEMS[:6])


case("a submission missing one of the 7 required items is rejected", False,
     upto=5, week=5, tweak=missing_required_item)


def duplicate_declarations(root, data):
    """Three declarations, one key. The count used to be satisfied by repetition."""
    text = (root / SUB).read_text(encoding="utf-8")
    head = text.split("## Numbers used")[0]
    (root / SUB).write_text(
        head + "## Numbers used\n\n" +
        "\n".join([f"- geometry.radius_m = {data['geometry']['radius_m']}"] * 3) + "\n",
        encoding="utf-8")


case("three copies of one number do not count as three numbers", False,
     upto=5, week=5, tweak=duplicate_declarations)


def unsent_email_missing(root, data):
    (root / "stage-1" / "submission" / "email-draft.md").unlink()


case("a submission with no staged email is rejected", False, upto=5, week=5,
     tweak=unsent_email_missing)


def unrelated_pdf(root, data):
    """The attachment is what gets evaluated. This was the passing fixture until now:
    a complete markdown report beside the competition's own problem statement."""
    shutil.copy(REAL_PDF, root / "stage-1" / "submission" / "cycloprop-stage1.pdf")


case("an unrelated PDF attached as the submission is rejected", False, upto=5, week=5,
     tweak=unrelated_pdf)


def stale_pdf(root, data):
    """A PDF built from an earlier draft, missing a section the markdown now carries."""
    md = root / SUB
    text = md.read_text(encoding="utf-8")
    md.write_text(text.replace("## " + REQUIRED_ITEMS[3], "## Thrust and power, old title"),
                  encoding="utf-8")
    build_pdf_from(md, root / "stage-1" / "submission" / "cycloprop-stage1.pdf")
    md.write_text(text, encoding="utf-8")


case("a PDF built from an earlier draft is rejected", False, upto=5, week=5, tweak=stale_pdf)


def email_without_recipient(root, data):
    p = root / "stage-1" / "submission" / "email-draft.md"
    p.write_text(p.read_text(encoding="utf-8")
                 .replace("To: pushpak_gc2026@aero.iitb.ac.in", "To: the organisers"),
                 encoding="utf-8")


case("a staged email that names no recipient is rejected", False, upto=5, week=5,
     tweak=email_without_recipient)


def human_gate_outstanding(root, data):
    p = root / "stage-1" / "human-gate.md"
    p.write_text(p.read_text(encoding="utf-8").replace("ELIGIBILITY-CHECKED", "eligibility: tbd"),
                 encoding="utf-8")


case("week 5 with the eligibility check outstanding is rejected", False, upto=5, week=5,
     tweak=human_gate_outstanding)


def criteria_named_only_in_prose(root, data):
    """Eight junk rows in the table and the eight real criteria in a sentence beside it."""
    junk = [(f"criterion {i}", f"section {i}") for i in range(8)]
    submission_doc(root / SUB, data, rows=junk)
    p = root / SUB
    t = p.read_text(encoding="utf-8").replace(
        "## Evaluation criteria map",
        "## Evaluation criteria map\n\nThis report answers "
        + ", ".join(c for c, _ in CRITERIA_ROWS) + ".\n")
    p.write_text(t, encoding="utf-8")


case("criteria named beside the table instead of in it is rejected", False,
     upto=5, week=5, tweak=criteria_named_only_in_prose)


def main():
    failures = []
    for name, expect_pass, mutate, upto, week, tweak in CASES:
        tmp = tempfile.mkdtemp(prefix="cyclo-gate-")
        try:
            data = honest_numbers()
            if mutate:
                data = mutate(data)
            build(tmp, data, upto)
            if tweak:
                tweak(Path(tmp), data)
            code, out = run(tmp, week)
            got_pass = code == 0
            ok = got_pass == expect_pass
            print(("ok    " if ok else "BROKE ") + name +
                  f"   [expected {'pass' if expect_pass else 'fail'}, got "
                  f"{'pass' if got_pass else 'fail'}]")
            if not ok:
                failures.append((name, out))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    # Stub attack: real headings, no substance.
    tmp = tempfile.mkdtemp(prefix="cyclo-gate-")
    try:
        data = honest_numbers()
        build(tmp, data, 2)
        for f in ("01-configuration.md", "02-rotor-sizing.md", "04-thrust-and-power.md"):
            p = Path(tmp) / "stage-1" / "design" / f
            head = [l for l in p.read_text(encoding="utf-8").splitlines()
                    if l.startswith("#") or l.startswith("- ")]
            p.write_text("\n".join(head), encoding="utf-8")
        code, out = run(tmp, 2)
        ok = code != 0
        print(("ok    " if ok else "BROKE ") + "heading-only stub files are rejected"
              f"   [expected fail, got {'pass' if code == 0 else 'fail'}]")
        if not ok:
            failures.append(("stub files", out))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # Missing numbers.json must not let a late week through.
    tmp = tempfile.mkdtemp(prefix="cyclo-gate-")
    try:
        build(tmp, honest_numbers(), 4)
        (Path(tmp) / "stage-1" / "design" / "numbers.json").unlink()
        code, out = run(tmp, 4)
        ok = code != 0
        print(("ok    " if ok else "BROKE ") + "deleting numbers.json is rejected"
              f"   [expected fail, got {'pass' if code == 0 else 'fail'}]")
        if not ok:
            failures.append(("missing numbers.json", out))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # F7: a number invented in the narrative, outside any Numbers used block.
    tmp = tempfile.mkdtemp(prefix="cyclo-gate-")
    try:
        data = honest_numbers()
        build(tmp, data, 2)
        sub = Path(tmp) / "stage-1" / "submission"
        sub.mkdir(parents=True, exist_ok=True)
        body = chr(10).join([
            "# Submission", "",
            "The module produces 999 N of thrust at the design point.", "",
            "## Numbers used", "",
            "- performance.thrust_N = "
            + str(rnd(data["performance"]["thrust_N"], 2)),
        ])
        (sub / "cycloprop-stage1.md").write_text(body, encoding="utf-8")
        sys.path.insert(0, str(CHECK.parent))
        import importlib
        import check as chk
        importlib.reload(chk)
        chk.set_root(tmp)
        chk.FAILURES.clear()
        chk.check_numeric_coverage("stage-1/submission/cycloprop-stage1.md", data)
        ok = bool(chk.FAILURES)
        print(("ok    " if ok else "BROKE ") + "a number invented in the narrative is rejected"
              f"   [expected fail, got {'fail' if ok else 'pass'}]")
        if not ok:
            failures.append(("narrative number", "999 N passed the coverage audit"))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # PDF path: a real PDF, a renamed text file, and a too-short PDF.
    import importlib
    sys.path.insert(0, str(CHECK.parent))
    import check as chk
    importlib.reload(chk)
    real = Path(__file__).resolve().parent.parent / "reference" / "cycloprop-problem-statement.pdf"
    tmp = tempfile.mkdtemp(prefix="cyclo-gate-")
    try:
        shutil.copy(real, Path(tmp) / "good.pdf")
        (Path(tmp) / "fake.pdf").write_text("not a pdf at all", encoding="utf-8")
        chk.set_root(tmp)
        for name, path, want_pass in [("a real PDF is accepted", "good.pdf", True),
                                      ("a renamed text file is rejected", "fake.pdf", False),
                                      ("a PDF under the page floor is rejected", "good.pdf", False)]:
            chk.FAILURES.clear()
            chk.check_pdf(path, min_pages=4 if want_pass or "text" in name else 99)
            got = not chk.FAILURES
            ok = got == want_pass
            print(("ok    " if ok else "BROKE ") + name +
                  f"   [expected {'pass' if want_pass else 'fail'}, got {'pass' if got else 'fail'}]")
            if not ok:
                failures.append((name, ""))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # Audit escapes: they must state a reason and there is a ceiling on them.
    tmp = tempfile.mkdtemp(prefix="cyclo-gate-")
    try:
        data = honest_numbers()
        chk.set_root(tmp)
        good = "<!-- allow-table: measured data reproduced from Benedict 2010 -->"
        inline = "<!-- allow: reproducing a published row -->"
        probes = [
            ("a bare escape with no reason is rejected", "<!-- allow -->", False),
            ("an escape with a stated reason is accepted", good, True),
            # The ceiling counts hidden numbers, so these three all breach it with one
            # marker each. Counting markers let every one of them through.
            ("one inline marker hiding six numbers is rejected",
             "thrust 991 N 992 N 993 N 994 N 995 N 996 N " + inline, False),
            ("one table marker hiding twenty rows is rejected",
             chr(10).join([good] + [f"| {900 + i} N |" for i in range(20)]), False),
            ("a blockquote hiding six numbers is rejected",
             chr(10).join([f"> the module gave {900 + i} N" for i in range(6)]), False),
            ("an inline marker hiding two numbers is accepted",
             "thrust 991 N and 992 N " + inline, True),
            ("scientific notation is not invisible to the audit", "thrust of 9.99e2 N", False),
        ]
        for name, text, want_pass in probes:
            (Path(tmp) / "t.md").write_text(text, encoding="utf-8")
            chk.FAILURES.clear()
            chk.check_numeric_coverage("t.md", data)
            got = not chk.FAILURES
            ok = got == want_pass
            print(("ok    " if ok else "BROKE ") + name +
                  f"   [expected {'pass' if want_pass else 'fail'}, got {'pass' if got else 'fail'}]")
            if not ok:
                failures.append((name, ""))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # Unit awareness: value alone is not enough.
    tmp = tempfile.mkdtemp(prefix="cyclo-gate-")
    try:
        data = honest_numbers()
        chk.set_root(tmp)
        probes = [("produces 400 N of thrust", False), ("Envelope is 400 mm long.", True),
                  ("A force of -10 N acts.", False), ("At least 10 N.", True),
                  ("| 999 N |", False)]
        for text, want_pass in probes:
            (Path(tmp) / "t.md").write_text(text, encoding="utf-8")
            chk.FAILURES.clear()
            chk.check_numeric_coverage("t.md", data)
            got = not chk.FAILURES
            ok = got == want_pass
            print(("ok    " if ok else "BROKE ") + f"coverage: {text!r}" +
                  f"   [expected {'pass' if want_pass else 'fail'}, got {'pass' if got else 'fail'}]")
            if not ok:
                failures.append((text, ""))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # --all has to notice a deleted progress file, including the highest one. The
    # progress files cannot police their own maximum, so the handoff marker is the witness.
    def run_all(root):
        r = subprocess.run([sys.executable, str(CHECK), "--all", "--root", str(root)],
                           capture_output=True, text=True)
        return r.returncode == 0, r.stdout

    probes = [("--all passes with every progress file present", None, None, True),
              ("--all fails when the highest progress file is deleted", 4, None, False),
              ("--all fails when a middle progress file is deleted", 3, None, False),
              ("--all fails when a completed week has no audit", None, 2, False),
              ("--all fails on two NEXT-WEEK markers", None, None, False, "double")]
    for name, drop, no_audit, want_pass, *extra in probes:
        tmp = tempfile.mkdtemp(prefix="cyclo-gate-")
        try:
            build(tmp, honest_numbers(), 4)
            hand = ["# Handoff", "", "NEXT-WEEK: 5", ""]
            if extra and extra[0] == "double":
                hand += ["NEXT-WEEK: 3", ""]
            (Path(tmp) / "handoff.md").write_text("\n".join(hand), encoding="utf-8")
            prog = Path(tmp) / "stage-1" / "progress"
            audit = Path(tmp) / "stage-1" / "audit"
            prog.mkdir(parents=True, exist_ok=True)
            audit.mkdir(parents=True, exist_ok=True)
            for w in range(1, 5):
                if w == drop:
                    continue
                (prog / f"week-{w}.md").write_text(
                    f"# Week {w}\n\nSTATUS: WEEK-COMPLETE\n", encoding="utf-8")
                if w != no_audit:
                    (audit / f"week-{w}.md").write_text(
                        f"# Week {w} audit\n\nAUDIT-COMPLETE\n", encoding="utf-8")
            got_pass, out = run_all(tmp)
            ok = got_pass == want_pass
            print(("ok    " if ok else "BROKE ") + name +
                  f"   [expected {'pass' if want_pass else 'fail'}, "
                  f"got {'pass' if got_pass else 'fail'}]")
            if not ok:
                failures.append((name, out))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    print()
    if failures:
        print(f"{len(failures)} case(s) behaved wrongly")
        for name, out in failures:
            print(f"\n===== {name} =====\n{out}")
        return 1
    print(f"All {len(CASES) + 22} gate self-tests behaved as expected.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
