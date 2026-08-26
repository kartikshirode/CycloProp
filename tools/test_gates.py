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
RHO, NU, G = 1.225, 1.5e-5, 9.81

FILLER = ("The rotor operates in a curvilinear flowfield so each chordwise station sees "
          "its own angle of attack, which is why simple blade element estimates carry a "
          "caveat here and why the published analytical tools overpredict thrust away "
          "from their design point. ") * 30


def honest_numbers():
    R, nb = 0.14, 3
    c, S = 0.66 * R, 2.64 * R
    ct, ct_low = 0.607, 0.516
    area = nb * c * S
    thrust = 13.0
    u = math.sqrt(thrust / (ct * 0.5 * RHO * area))
    rpm = u / R * 60 / (2 * math.pi)
    t_cons = ct_low * 0.5 * RHO * u * u * area
    ap, eff = 118.0, (0.92, 0.80, 0.95)

    budget = [
        {"item": "blades, 3 off", "mass_g": 108.0,
         "basis": "cfrp skin over foam core, volume times density with a layup allowance"},
        {"item": "endplates and frame", "mass_g": 74.0,
         "basis": "scaled from the Benedict quad rotor structure at this diameter"},
        {"item": "pitch linkage and offset disk", "mass_g": 33.0,
         "basis": "part count times unit mass from the four bar layout drawing"},
        {"item": "hub and shaft", "mass_g": 44.0,
         "basis": "7075 tube sized by the shaft torque margin calculation"},
        {"item": "bearings", "mass_g": 17.0,
         "basis": "supplier datasheet masses for the selected bore sizes"},
        {"item": "motor", "mass_g": 62.0,
         "basis": "supplier datasheet for a motor rated above continuous electrical power"},
        {"item": "esc and wiring", "mass_g": 21.0,
         "basis": "supplier datasheet plus a measured harness allowance"},
        {"item": "actuators, 2 off", "mass_g": 18.0,
         "basis": "supplier datasheet for the amplitude and phase servos"},
        {"item": "mounting hardware and fasteners", "mass_g": 23.0,
         "basis": "fastener count times unit mass with a bracket allowance"},
    ]
    total = sum(b["mass_g"] for b in budget)
    blade_mass = 0.108 / 3
    fc = blade_mass * (rpm * 2 * math.pi / 60) ** 2 * R

    envelope = [
        {"item": "blades", "nominal_g": 108.0, "conservative_g": 122.0,
         "basis": "cfrp skin over foam core, volume times density with a layup allowance"},
        {"item": "frame and endplates", "nominal_g": 74.0, "conservative_g": 83.0,
         "basis": "scaled from the Benedict quad rotor structure at this diameter"},
        {"item": "pitch mechanism", "nominal_g": 33.0, "conservative_g": 38.0,
         "basis": "part count times unit mass from the four bar layout drawing"},
        {"item": "motor and drive", "nominal_g": 106.0, "conservative_g": 116.0,
         "basis": "supplier datasheet plus hub, shaft, bearings and transmission"},
        {"item": "actuators", "nominal_g": 18.0, "conservative_g": 21.0,
         "basis": "supplier datasheet for the amplitude and phase servos"},
        {"item": "mounting hardware", "nominal_g": 61.0, "conservative_g": 60.0,
         "basis": "fastener count times unit mass with a bracket and harness allowance"},
    ]
    env_nom = sum(e["nominal_g"] for e in envelope)
    m_cons = sum(e["conservative_g"] for e in envelope)

    tare = 13.0
    shaft = ap + tare
    elec = shaft / (eff[0] * eff[1] * eff[2])
    act_p, ctl_p = 6.0, 2.0
    blade_dem, shaft_dem = 6.4, 1.9
    blade_all, shaft_all = 13.4, 6.5

    return {
        "geometry": {"radius_m": R, "chord_m": c, "span_m": S, "blades": nb,
                     "airfoil": "NACA 0020", "pitch_amplitude_deg": 40,
                     "pitch_axis_pct_chord": 25},
        "operating": {"rpm": rpm, "tip_speed_ms": u, "reynolds": u * c / NU},
        "performance": {"thrust_N": thrust, "blade_area_coeff": ct,
                        "blade_area_coeff_low": ct_low, "thrust_N_conservative": t_cons,
                        "aero_power_W": ap, "tare_power_W": tare,
                        "electrical_power_W": elec,
                        "actuator_power_W": act_p, "controller_power_W": ctl_p,
                        "module_electrical_power_W": elec + act_p + ctl_p},
        "efficiency": {"transmission": eff[0], "motor": eff[1], "esc": eff[2]},
        "power_by_radius": [{"radius_m": r, "aero_power_W": ap * 0.14 / r}
                            for r in (0.10, 0.12, 0.14, 0.16)],
        "pitch": {"mechanism": "passive four-bar", "offset_m": 0.024,
                  "phase_delay_deg": 9.0, "vector_range_deg": 360.0,
                  "actuator_count": 2, "actuator_mass_g": 18.0,
                  "side_force_tilt_deg": 28.0},
        "packaging": {"envelope_length_mm": 400, "envelope_width_mm": 300,
                      "envelope_height_mm": 300, "mount_points": 4},
        "structure": {"blade_mass_kg": blade_mass, "centrifugal_load_N": fc,
                      "blade_root_bending_Nm": blade_dem, "shaft_torque_Nm": shaft_dem,
                      "blade_allowable_Nm": blade_all, "shaft_allowable_Nm": shaft_all,
                      "blade_margin": blade_all / blade_dem,
                      "shaft_margin": shaft_all / shaft_dem},
        "mass_envelope_g": envelope,
        "mass_budget_g": budget,
        "sources": {"performance": {
            "blade_area_coeff": "derived from the Benedict 2010 quad rotor at its hover point",
            "blade_area_coeff_low": "lower bound from the spread across blade count and airfoil in Benedict 2010"}},
        "results": {"total_mass_g": total, "weight_N": total / 1000 * G,
                    "thrust_to_weight": thrust / (total / 1000 * G),
                    "mass_envelope_g": env_nom, "mass_g_conservative": m_cons,
                    "thrust_to_weight_conservative": t_cons / (m_cons / 1000 * G)},
    }


def doc(path, headings, numbers=(), words=600):
    body = [f"# {headings[0]}", "", FILLER[:words * 6], ""]
    for h in headings[1:]:
        body += [f"## {h}", "", FILLER[:words * 3], ""]
    if numbers:
        body += ["## Numbers used", ""] + [f"- {k} = {v}" for k, v in numbers] + [""]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(body), encoding="utf-8")


def pitch_doc(path, numbers):
    rows = ["| azimuth | pitch |", "| --- | --- |"]
    for i in range(36):
        a = i * 10
        rows.append(f"| {a} | {40 * math.cos(math.radians(a)):.2f} |")
    body = ["# Pitch mechanism", "", FILLER[:2000], "", "## Kinematics", "",
            FILLER[:1500], "", "## Pitch schedule", ""] + rows + [
        "", "## Thrust vectoring", "", FILLER[:1500], "", "## Side force", "",
        FILLER[:1200], "", "## Numbers used", ""] + [f"- {k} = {v}" for k, v in numbers]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(body), encoding="utf-8")


def build(root, data, upto=4):
    d = Path(root)
    doc(d / "context.md", ["Context", "Stage 1: the seven required items",
                           "Evaluation criteria", "The thrust-to-weight basis, settled"])
    doc(d / "stage-1" / "plan.md", ["Plan", "Calendar"])
    doc(d / "stage-1" / "literature.md",
        ["Literature", "Geometry and measured performance", "Published mass breakdowns"])
    (d / "stage-1" / "design").mkdir(parents=True, exist_ok=True)
    (d / "stage-1" / "design" / "numbers.json").write_text(
        json.dumps(data, indent=2), encoding="utf-8")

    g = d / "stage-1" / "design"
    if upto >= 2:
        doc(g / "01-configuration.md", ["Configuration", "Why this configuration"],
            [("geometry.blades", data["geometry"]["blades"])])
        doc(g / "02-rotor-sizing.md", ["Rotor sizing", "Shape family", "Radius"],
            [("geometry.radius_m", data["geometry"]["radius_m"])])
        doc(g / "04-thrust-and-power.md", ["Thrust", "Power", "Sensitivity"],
            [("performance.thrust_N", round(data["performance"]["thrust_N"], 2))])
    if upto >= 3:
        pitch_doc(g / "03-pitch-and-vectoring.md",
                  [("pitch.vector_range_deg", data["pitch"]["vector_range_deg"])])
        doc(g / "09-packaging-and-integration.md",
            ["Package envelope", "Mounting", "Drivetrain", "Interfaces"],
            [("packaging.mount_points", data["packaging"]["mount_points"])])
    if upto >= 4:
        doc(g / "05-mass-and-tw.md", ["Mass budget", "Thrust-to-weight", "Margin"],
            [("results.total_mass_g", data["results"]["total_mass_g"])])
        doc(g / "06-materials-and-manufacturing.md",
            ["Material selection", "Manufacturing", "Cost"],
            [("results.total_mass_g", data["results"]["total_mass_g"])])
        doc(g / "08-structure-and-loads.md",
            ["Load cases", "Blade", "Shaft", "Margins"],
            [("structure.blade_margin", data["structure"]["blade_margin"])])
    return d


def run(root, week):
    r = subprocess.run([sys.executable, str(CHECK), "--week", str(week), "--root", str(root)],
                       capture_output=True, text=True)
    return r.returncode, r.stdout


CASES = []


def case(name, expect_pass, mutate=None, upto=4, week=4):
    CASES.append((name, expect_pass, mutate, upto, week))


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


def main():
    failures = []
    for name, expect_pass, mutate, upto, week in CASES:
        tmp = tempfile.mkdtemp(prefix="cyclo-gate-")
        try:
            data = honest_numbers()
            if mutate:
                data = mutate(data)
            build(tmp, data, upto)
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
            + str(round(data["performance"]["thrust_N"], 2)),
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

    print()
    if failures:
        print(f"{len(failures)} case(s) behaved wrongly")
        for name, out in failures:
            print(f"\n===== {name} =====\n{out}")
        return 1
    print(f"All {len(CASES) + 3} gate self-tests behaved as expected.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
