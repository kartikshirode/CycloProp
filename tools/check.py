#!/usr/bin/env python3
"""Mechanical gates for the CycloProp Stage 1 weekly loop.

Usage:
    python tools/check.py --week N     validate weeks 1..N cumulatively
    python tools/check.py --all        validate every week up to the highest one done
    python tools/check.py --global     global checks only

Exit code 0 means pass. Anything else means at least one gate failed.

Design rules this file enforces, and why:

* Hard competition limits are applied to RECOMPUTED values, never to stored ones.
  Storing a slightly optimistic thrust and a slightly optimistic mass used to let two
  errors inside tolerance compound into a design that missed both targets.
* There is no fixed 408 g limit. 408 g is only the ceiling when thrust is exactly 10 N.
  The actual requirement is thrust at or above 10 N and T/W above 2.5, so that is what
  gets checked, and heavier modules are legal if they produce more thrust.
* A conservative case must also clear both targets. Stage 1 numbers are paper estimates
  and the coefficient behind them is transferred across a geometry change.
* Weeks are cumulative. Week 4 cannot pass by breaking week 2.
"""

import argparse
import json
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NUMBERS = PROGRESS_DIR = None      # set by set_root(), called from main()


def set_root(path):
    """Point the gates at a different tree. Used by tools/test_gates.py so the
    self-test never touches the real repo."""
    global ROOT, NUMBERS, PROGRESS_DIR
    ROOT = Path(path).resolve()
    NUMBERS = ROOT / "stage-1" / "design" / "numbers.json"
    PROGRESS_DIR = ROOT / "stage-1" / "progress"
DONE_MARKER = "STATUS: WEEK-COMPLETE"

RHO = 1.225
NU = 1.5e-5
G = 9.81

TOL = 0.005              # internal arithmetic must reproduce to 0.5 percent
DISPLAY_TOL = 0.02       # numbers quoted in prose may be rounded to 2 percent

THRUST_MINIMUM_N = 10.0
TW_MINIMUM = 2.5
PLANNING_MASS_AT_10N_G = 408.0   # reported for reference, never gated

MIN_BASIS_CHARS = 25     # a basis field has to say something
MIN_MASS_LINE_G = 0.5    # no vanishing components

VERBATIM_DIRS = {"reference"}
RULES_FILES = {".claude/weekly-loop.md"}
BANNED_ATTRIBUTION = ["co-authored-by", "generated with claude", "claude opus", "anthropic"]

FAILURES = []


def report(ok, label, detail=""):
    print(("PASS  " if ok else "FAIL  ") + label + (("  " + detail) if detail else ""))
    if not ok:
        FAILURES.append(label + (("  " + detail) if detail else ""))
    return bool(ok)


def note(label, detail=""):
    print("note  " + label + (("  " + detail) if detail else ""))


def md_files():
    for p in sorted(ROOT.rglob("*.md")):
        rel = p.relative_to(ROOT)
        if (rel.parts and rel.parts[0] in VERBATIM_DIRS) or ".git" in rel.parts:
            continue
        yield p


# ---------------------------------------------------------------- global gates

def check_global():
    ok = True
    for label, test in [
        ("global: no em or en dashes in prose", lambda ch: ch in "—–"),
        ("global: prose is plain ASCII", lambda ch: ord(ch) > 127),
    ]:
        bad = []
        for p in md_files():
            for i, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
                if any(test(ch) for ch in line):
                    bad.append(f"{p.relative_to(ROOT).as_posix()}:{i}")
        ok &= report(not bad, label,
                     f"{len(bad)} hits: {', '.join(bad[:5])}" if bad else "")

    bad = []
    for p in md_files():
        rel = p.relative_to(ROOT).as_posix()
        if rel in RULES_FILES:
            continue                    # these files name the strings in order to ban them
        low = p.read_text(encoding="utf-8").lower()
        bad += [f"{rel} contains '{s}'" for s in BANNED_ATTRIBUTION if s in low]
    ok &= report(not bad, "global: no AI attribution in tracked prose",
                 "; ".join(bad[:3]) if bad else "")

    for rel in ["context.md", "stage-1/plan.md", "stage-1/literature.md"]:
        ok &= report((ROOT / rel).is_file(), f"global: {rel} exists")
    return ok


# ------------------------------------------------------------- numbers helpers

def load_numbers():
    if not NUMBERS.is_file():
        return None
    try:
        return json.loads(NUMBERS.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        report(False, "numbers.json parses", str(e))
        return None


def dotted(data, path):
    cur = data
    for part in path.split("."):
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            return None
    return cur


def num(data, path):
    """Return a finite positive number, or None. Rejects bools, strings and zero."""
    v = dotted(data, path)
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        return None
    if not math.isfinite(v) or v <= 0:
        return None
    return float(v)


def close(a, b, tol=TOL):
    if a is None or b is None:
        return False
    a, b = float(a), float(b)
    return abs(a - b) <= tol * abs(b) if b else abs(a) < 1e-12


def require_positive(data, keys, label):
    bad = []
    for k in keys:
        v = dotted(data, k)
        if v is None:
            bad.append(f"{k} missing")
        elif isinstance(v, str):
            if not v.strip():
                bad.append(f"{k} empty")
        elif num(data, k) is None:
            bad.append(f"{k}={v} not a finite positive number")
    return report(not bad, label, "; ".join(bad[:6]) if bad else "")


HEADING = re.compile(r"^#{1,6}\s+(.*\S)\s*$", re.M)


def require_headings(rel, headings):
    """Headings must be real markdown headings, not words buried in a sentence."""
    p = ROOT / rel
    if not p.is_file():
        return report(False, f"{rel} exists")
    found = [h.lower() for h in HEADING.findall(p.read_text(encoding="utf-8"))]
    missing = [h for h in headings if not any(h.lower() in f for f in found)]
    return report(not missing, f"{rel} has required sections",
                  "missing headings: " + "; ".join(missing) if missing else "")


def require_substance(rel, min_words=400):
    p = ROOT / rel
    if not p.is_file():
        return False
    body = [l for l in p.read_text(encoding="utf-8").splitlines()
            if not l.startswith("#")]
    words = len(" ".join(body).split())
    return report(words >= min_words, f"{rel} is not a stub",
                  f"{words} words, need {min_words}")


NUM_DECL = re.compile(r"^\s*-\s*([A-Za-z0-9_.]+)\s*=\s*([-+0-9.eE]+)\s*$")


def check_declared_numbers(rel, data):
    p = ROOT / rel
    if not p.is_file():
        return False                    # require_headings already reported it
    text = p.read_text(encoding="utf-8")
    m = re.search(r"##\s*Numbers used\s*(.*?)(\n##\s|\Z)", text, re.S | re.I)
    if not m:
        return report(False, f"{rel} has a 'Numbers used' section")
    decls = [d for d in (NUM_DECL.match(l) for l in m.group(1).splitlines()) if d]
    if not decls:
        return report(False, f"{rel} declares at least one number")
    bad = []
    for d in decls:
        key, val = d.group(1), float(d.group(2))
        actual = dotted(data, key)
        if actual is None:
            bad.append(f"{key} not in numbers.json")
        elif not close(val, actual, DISPLAY_TOL):
            bad.append(f"{key} says {val}, numbers.json has {actual}")
    return report(not bad, f"{rel} numbers agree with numbers.json",
                  "; ".join(bad[:4]) if bad else f"{len(decls)} checked")


# -------------------------------------------------------------- physics recompute

def recompute(data):
    """Return the values derived from stored geometry and mass lines. These, not the
    stored headline numbers, are what the hard limits are applied to."""
    out = {}
    R, c, S = num(data, "geometry.radius_m"), num(data, "geometry.chord_m"), num(data, "geometry.span_m")
    nb, rpm = num(data, "geometry.blades"), num(data, "operating.rpm")
    if None not in (R, c, S, nb, rpm):
        u = rpm * 2 * math.pi / 60 * R
        out["tip_speed_ms"] = u
        out["reynolds"] = u * c / NU
        out["blade_area_m2"] = nb * c * S
        for tag, key in (("thrust_N", "performance.blade_area_coeff"),
                         ("thrust_N_conservative", "performance.blade_area_coeff_low")):
            ct = num(data, key)
            if ct is not None:
                out[tag] = ct * 0.5 * RHO * u * u * out["blade_area_m2"]

    budget = dotted(data, "mass_budget_g")
    if isinstance(budget, list) and budget:
        try:
            out["total_mass_g"] = sum(float(b.get("mass_g", 0)) for b in budget)
        except (TypeError, ValueError):
            pass
    mc = num(data, "results.mass_g_conservative")
    for tag, m_key, t_key in (("thrust_to_weight", "total_mass_g", "thrust_N"),
                              ("thrust_to_weight_conservative", None, "thrust_N_conservative")):
        m = out.get(m_key) if m_key else mc
        t = out.get(t_key)
        if m and t:
            out[tag] = t / (m / 1000.0 * G)
    return out


# ------------------------------------------------------------------ week gates

def week1(data):
    ok = True
    ok &= require_headings("context.md", [
        "Stage 1: the seven required items", "Evaluation criteria",
        "The thrust-to-weight basis, settled",
    ])
    ok &= require_headings("stage-1/literature.md", [
        "Geometry and measured performance", "Published mass breakdowns",
    ])
    return ok


def week2(data):
    ok = True
    ok &= require_positive(data, [
        "geometry.radius_m", "geometry.chord_m", "geometry.span_m", "geometry.blades",
        "geometry.pitch_amplitude_deg", "geometry.pitch_axis_pct_chord",
        "operating.rpm", "operating.tip_speed_ms", "operating.reynolds",
        "performance.thrust_N", "performance.blade_area_coeff",
        "performance.blade_area_coeff_low", "performance.thrust_N_conservative",
        "performance.aero_power_W", "performance.electrical_power_W",
        "efficiency.transmission", "efficiency.motor", "efficiency.esc",
        "results.mass_envelope_g", "results.mass_g_conservative",
    ], "week2: numbers.json carries the week 2 schema as positive finite values")
    ok &= report(bool(str(dotted(data, "geometry.airfoil") or "").strip()),
                 "week2: airfoil is named")

    r = recompute(data)

    for stored, computed, label in [
        ("operating.tip_speed_ms", "tip_speed_ms", "tip speed from rpm and radius"),
        ("operating.reynolds", "reynolds", "Reynolds from tip speed and chord"),
        ("performance.thrust_N", "thrust_N", "thrust from geometry and coefficient"),
        ("performance.thrust_N_conservative", "thrust_N_conservative",
         "conservative thrust from the low coefficient"),
    ]:
        if computed in r:
            ok &= report(close(num(data, stored), r[computed]),
                         f"week2: {label} reproduces",
                         f"computed {r[computed]:.4g}, stored {dotted(data, stored)}")

    # Hard limits on RECOMPUTED thrust, both nominal and conservative.
    for key, label in [("thrust_N", "nominal"), ("thrust_N_conservative", "conservative")]:
        t = r.get(key)
        ok &= report(t is not None and t >= THRUST_MINIMUM_N,
                     f"week2: {label} thrust clears 10 N",
                     f"{t:.3f} N" if t else "not computable")

    cl, cn = num(data, "performance.blade_area_coeff_low"), num(data, "performance.blade_area_coeff")
    if cl and cn:
        ok &= report(cl < cn, "week2: the conservative coefficient is actually lower",
                     f"low {cl} vs nominal {cn}")

    # Feasibility envelope: the conservative mass must still clear T/W at conservative thrust.
    mc, tc = num(data, "results.mass_g_conservative"), r.get("thrust_N_conservative")
    if mc and tc:
        tw = tc / (mc / 1000.0 * G)
        ok &= report(tw > TW_MINIMUM,
                     "week2: conservative mass and thrust still clear T/W 2.5",
                     f"T/W {tw:.3f} at {tc:.2f} N and {mc:.0f} g")
        note("week2: planning mass ceiling at this thrust",
             f"{tc / (TW_MINIMUM * G) * 1000:.0f} g "
             f"({PLANNING_MASS_AT_10N_G:.0f} g would apply only at exactly 10 N)")

    ap = num(data, "performance.aero_power_W")
    chain = [num(data, f"efficiency.{k}") for k in ("transmission", "motor", "esc")]
    if ap and all(chain):
        ok &= report(close(num(data, "performance.electrical_power_W"),
                           ap / (chain[0] * chain[1] * chain[2])),
                     "week2: electrical power reproduces from aero power and the chain",
                     f"computed {ap / (chain[0] * chain[1] * chain[2]):.1f} W")
    for e in chain:
        if e and not 0 < e <= 1:
            ok &= report(False, "week2: efficiencies are fractions between 0 and 1", str(e))

    sweep = dotted(data, "power_by_radius")
    ok &= report(isinstance(sweep, list) and len(sweep) >= 3,
                 "week2: power is evaluated across at least 3 candidate radii",
                 f"found {len(sweep) if isinstance(sweep, list) else 0}")

    for rel, heads in [
        ("stage-1/design/01-configuration.md",
         ["Configuration", "Why one rotor", "Numbers used"]),
        ("stage-1/design/02-rotor-sizing.md",
         ["Rotor sizing", "Shape family", "Radius", "Numbers used"]),
        ("stage-1/design/04-thrust-and-power.md",
         ["Thrust", "Power", "Sensitivity", "Numbers used"]),
    ]:
        ok &= require_headings(rel, heads)
        ok &= require_substance(rel)
        ok &= check_declared_numbers(rel, data)
    return ok


def week3(data):
    ok = True
    ok &= require_positive(data, [
        "pitch.offset_m", "pitch.phase_delay_deg", "pitch.vector_range_deg",
        "pitch.actuator_count", "pitch.actuator_mass_g", "pitch.side_force_tilt_deg",
        "packaging.envelope_length_mm", "packaging.envelope_width_mm",
        "packaging.envelope_height_mm", "packaging.mount_points",
    ], "week3: numbers.json carries the pitch and packaging schema")
    ok &= report(bool(str(dotted(data, "pitch.mechanism") or "").strip()),
                 "week3: pitch mechanism is named")

    rel = "stage-1/design/03-pitch-and-vectoring.md"
    ok &= require_headings(rel, ["Pitch mechanism", "Kinematics", "Pitch schedule",
                                 "Thrust vectoring", "Side force", "Numbers used"])
    ok &= require_substance(rel, 500)
    ok &= check_declared_numbers(rel, data)

    p = ROOT / rel
    if p.is_file():
        m = re.search(r"#{2,}\s*Pitch schedule.*?\n(.*?)(\n#{2,}\s|\Z)",
                      p.read_text(encoding="utf-8"), re.S | re.I)
        az = []
        if m:
            for l in m.group(1).splitlines():
                cell = re.match(r"^\s*\|\s*(-?\d+(?:\.\d+)?)\s*\|", l)
                if cell:
                    az.append(float(cell.group(1)))
        uniq = sorted(set(az))
        ok &= report(len(uniq) >= 24,
                     "week3: pitch schedule has 24 or more distinct azimuths",
                     f"{len(uniq)} distinct out of {len(az)} rows")
        if uniq:
            ok &= report(max(uniq) - min(uniq) >= 300,
                         "week3: pitch schedule spans the revolution",
                         f"{min(uniq):.0f} to {max(uniq):.0f} deg")

    rel = "stage-1/design/09-packaging-and-integration.md"
    ok &= require_headings(rel, ["Package envelope", "Mounting", "Drivetrain",
                                 "Interfaces", "Numbers used"])
    ok &= require_substance(rel, 300)
    ok &= check_declared_numbers(rel, data)
    return ok


def week4(data):
    ok = True
    budget = dotted(data, "mass_budget_g")
    ok &= report(isinstance(budget, list) and len(budget) >= 8,
                 "week4: mass budget has 8 or more line items",
                 f"found {len(budget) if isinstance(budget, list) else 0}")

    if isinstance(budget, list) and budget:
        thin = [b.get("item", "?") for b in budget
                if len(str(b.get("basis", "")).strip()) < MIN_BASIS_CHARS]
        ok &= report(not thin, f"week4: every mass line states a basis of {MIN_BASIS_CHARS}+ chars",
                     "thin: " + ", ".join(thin[:5]) if thin else "")
        tiny = [b.get("item", "?") for b in budget
                if not isinstance(b.get("mass_g"), (int, float))
                or float(b.get("mass_g", 0)) < MIN_MASS_LINE_G]
        ok &= report(not tiny, f"week4: no mass line below {MIN_MASS_LINE_G} g",
                     "; ".join(tiny[:5]) if tiny else "")
        names = " ".join(str(b.get("item", "")).lower() for b in budget)
        absent = [x for x in ["blade", "frame", "pitch", "motor", "actuator", "mount"]
                  if x not in names]
        ok &= report(not absent, "week4: budget covers every component the problem statement names",
                     "missing: " + ", ".join(absent) if absent else "")

    r = recompute(data)
    if "total_mass_g" in r:
        ok &= report(close(num(data, "results.total_mass_g"), r["total_mass_g"]),
                     "week4: mass lines sum to the stated total",
                     f"computed {r['total_mass_g']:.2f} g")
        ok &= report(close(num(data, "results.weight_N"), r["total_mass_g"] / 1000 * G),
                     "week4: weight reproduces from summed mass")

    mc = num(data, "results.mass_g_conservative")
    if mc and "total_mass_g" in r:
        ok &= report(mc >= r["total_mass_g"],
                     "week4: the conservative mass is not lighter than the budget",
                     f"conservative {mc:.1f} g vs budget {r['total_mass_g']:.1f} g")

    # The competition requirement, applied to recomputed values only.
    for key, label in [("thrust_to_weight", "nominal"),
                       ("thrust_to_weight_conservative", "conservative")]:
        tw = r.get(key)
        ok &= report(tw is not None and tw > TW_MINIMUM,
                     f"week4: {label} T/W clears 2.5",
                     f"{tw:.3f}" if tw else "not computable")
        if tw is not None:
            ok &= report(close(num(data, f"results.{key}"), tw),
                         f"week4: stated {label} T/W matches the recomputed one")

    ok &= require_positive(data, [
        "structure.centrifugal_load_N", "structure.blade_root_bending_Nm",
        "structure.shaft_torque_Nm", "structure.blade_margin", "structure.shaft_margin",
    ], "week4: numbers.json carries the structural schema")
    for k in ("structure.blade_margin", "structure.shaft_margin"):
        v = num(data, k)
        if v is not None:
            ok &= report(v >= 1.5, f"week4: {k.split('.')[1]} is at least 1.5", f"{v}")

    # Centrifugal load is the one structural number that can be checked independently.
    R, rpm = num(data, "geometry.radius_m"), num(data, "operating.rpm")
    mb = num(data, "structure.blade_mass_kg")
    if None not in (R, rpm, mb):
        fc = mb * (rpm * 2 * math.pi / 60) ** 2 * R
        ok &= report(close(num(data, "structure.centrifugal_load_N"), fc, DISPLAY_TOL),
                     "week4: centrifugal load reproduces from blade mass, speed and radius",
                     f"computed {fc:.1f} N")

    for rel, heads in [
        ("stage-1/design/05-mass-and-tw.md",
         ["Mass budget", "Thrust-to-weight", "Margin", "Numbers used"]),
        ("stage-1/design/06-materials-and-manufacturing.md",
         ["Material selection", "Manufacturing", "Cost", "Numbers used"]),
        ("stage-1/design/08-structure-and-loads.md",
         ["Load cases", "Blade", "Shaft", "Margins", "Numbers used"]),
    ]:
        ok &= require_headings(rel, heads)
        ok &= require_substance(rel)
        ok &= check_declared_numbers(rel, data)
    return ok


REQUIRED_ITEMS = [
    "Cyclorotor concept and configuration",
    "Preliminary rotor sizing",
    "Blade arrangement and pitch-control concept",
    "Estimated thrust and power requirement",
    "Estimated module weight and thrust-to-weight ratio",
    "Initial material and manufacturing approach",
    "Team capability and execution plan",
]

CRITERIA_KEYS = ["10 N thrust", "thrust-to-weight", "kinematic", "aerodynamic",
                 "structural", "manufactur", "packaging", "presentation"]


def week5(data):
    ok = True
    ok &= require_headings("stage-1/design/07-team-and-execution.md",
                           ["Team capability", "Execution plan", "Stage 2"])

    sub = ROOT / "stage-1" / "submission" / "cycloprop-stage1.md"
    if not report(sub.is_file(), "week5: submission source exists"):
        return False
    text = sub.read_text(encoding="utf-8")

    heads = [h.lower() for h in HEADING.findall(text)]
    missing = [it for it in REQUIRED_ITEMS if not any(it.lower() in h for h in heads)]
    ok &= report(not missing, "week5: all 7 required items are top-level sections",
                 "missing: " + "; ".join(missing) if missing else "")

    low = text.lower()
    absent = [k for k in CRITERIA_KEYS if k not in low]
    ok &= report(not absent, "week5: the criteria map covers all 8 criteria",
                 "missing: " + ", ".join(absent) if absent else "")

    ok &= require_substance("stage-1/submission/cycloprop-stage1.md", 2500)
    ok &= check_declared_numbers("stage-1/submission/cycloprop-stage1.md", data)

    pdf = ROOT / "stage-1" / "submission" / "cycloprop-stage1.pdf"
    ok &= report(pdf.is_file() and pdf.stat().st_size > 50_000,
                 "week5: a PDF attachment is built and non-trivial",
                 f"{pdf.stat().st_size} bytes" if pdf.is_file() else "absent")

    draft = ROOT / "stage-1" / "submission" / "email-draft.md"
    ok &= report(draft.is_file(), "week5: the email is drafted and staged for a human to send")
    if draft.is_file():
        d = draft.read_text(encoding="utf-8").lower()
        ok &= report("attachment" in d and "cycloprop-stage1.pdf" in d,
                     "week5: the email names the attachment")
    return ok


WEEKS = {1: week1, 2: week2, 3: week3, 4: week4, 5: week5}


def highest_done():
    best = 0
    if PROGRESS_DIR.is_dir():
        for p in PROGRESS_DIR.glob("week-*.md"):
            m = re.search(r"week-(\d+)", p.name)
            if m and DONE_MARKER in p.read_text(encoding="utf-8"):
                best = max(best, int(m.group(1)))
    return best


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--week", type=int)
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--global", dest="glob", action="store_true")
    ap.add_argument("--root", default=str(Path(__file__).resolve().parent.parent))
    args = ap.parse_args()

    set_root(args.root)
    check_global()
    if args.glob:
        return finish()

    target = args.week or (highest_done() if args.all else 1)
    if target not in WEEKS:
        report(False, f"week {target} is not in the plan")
        return finish()

    data = load_numbers()
    if data is None and target >= 2:
        report(False, "numbers.json exists and parses")
        return finish()

    # Cumulative: later weeks may not pass by breaking earlier ones.
    for w in range(1, target + 1):
        print(f"--- week {w} ---")
        WEEKS[w](data)
    return finish()


def finish():
    print()
    if FAILURES:
        print(f"FAILED: {len(FAILURES)} gate(s)")
        for f in FAILURES:
            print("  - " + f)
        return 1
    print("All gates passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
