#!/usr/bin/env python3
"""Mechanical gates for the CycloProp Stage 1 weekly loop.

Usage:
    python tools/check.py --week N     validate week N deliverables
    python tools/check.py --all        validate every week whose progress file is done
    python tools/check.py --global     global checks only

Exit code 0 means pass. Anything else means at least one gate failed.
Every check prints one PASS or FAIL line so the supervisor can paste the output.
"""

import argparse
import json
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NUMBERS = ROOT / "stage-1" / "design" / "numbers.json"
PROGRESS_DIR = ROOT / "stage-1" / "progress"
DONE_MARKER = "STATUS: WEEK-COMPLETE"

RHO = 1.225
NU = 1.5e-5
G = 9.81
TOL = 0.02          # 2 percent relative tolerance on recomputed arithmetic
MASS_LIMIT_G = 408.0
TW_MINIMUM = 2.5
THRUST_MINIMUM_N = 10.0

# Directories holding material we did not write. Excluded from prose style checks.
VERBATIM_DIRS = {"reference"}

FAILURES = []


def report(ok, label, detail=""):
    print(("PASS  " if ok else "FAIL  ") + label + (("  " + detail) if detail else ""))
    if not ok:
        FAILURES.append(label + (("  " + detail) if detail else ""))
    return ok


def md_files():
    for p in sorted(ROOT.rglob("*.md")):
        rel = p.relative_to(ROOT)
        if rel.parts and rel.parts[0] in VERBATIM_DIRS:
            continue
        if ".git" in rel.parts:
            continue
        yield p


# ---------------------------------------------------------------- global gates

# Files that quote the banned strings in order to forbid them.
RULES_FILES = {".claude/weekly-loop.md"}

BANNED_ATTRIBUTION = [
    "co-authored-by",
    "generated with claude",
    "claude opus",
    "anthropic",
]


def check_global():
    ok = True

    bad = []
    for p in md_files():
        for i, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
            for ch in line:
                if ch in "—–":
                    bad.append(f"{p.relative_to(ROOT)}:{i}")
                    break
    ok &= report(not bad, "global: no em or en dashes in prose",
                 f"{len(bad)} hits: {', '.join(bad[:5])}" if bad else "")

    bad = []
    for p in md_files():
        for i, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
            for ch in line:
                if ord(ch) > 127:
                    bad.append(f"{p.relative_to(ROOT)}:{i} U+{ord(ch):04X}")
                    break
    ok &= report(not bad, "global: prose is plain ASCII",
                 f"{len(bad)} hits: {', '.join(bad[:5])}" if bad else "")

    bad = []
    for p in md_files():
        rel = p.relative_to(ROOT).as_posix()
        if rel in RULES_FILES:
            continue        # these files name the banned strings in order to ban them
        low = p.read_text(encoding="utf-8").lower()
        for s in BANNED_ATTRIBUTION:
            if s in low:
                bad.append(f"{rel} contains '{s}'")
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


def close(a, b, tol=TOL):
    if a is None or b is None:
        return False
    try:
        a, b = float(a), float(b)
    except (TypeError, ValueError):
        return False
    if b == 0:
        return abs(a) < 1e-9
    return abs(a - b) / abs(b) <= tol


def require_keys(data, keys, label):
    missing = [k for k in keys if dotted(data, k) is None]
    return report(not missing, label, "missing: " + ", ".join(missing) if missing else "")


def require_headings(rel, headings):
    p = ROOT / rel
    if not p.is_file():
        return report(False, f"{rel} exists")
    text = p.read_text(encoding="utf-8")
    missing = [h for h in headings if h.lower() not in text.lower()]
    return report(not missing, f"{rel} has required sections",
                  "missing: " + "; ".join(missing) if missing else "")


NUM_DECL = re.compile(r"^\s*-\s*([A-Za-z0-9_.]+)\s*=\s*([-+0-9.eE]+)\s*$")


def check_declared_numbers(rel, data):
    """Each design file ends with a '## Numbers used' list of 'key = value'
    lines keyed by dotted path into numbers.json. Keeps prose and data in sync."""
    p = ROOT / rel
    if not p.is_file():
        return False        # require_headings already reported the missing file
    text = p.read_text(encoding="utf-8")
    m = re.search(r"##\s*Numbers used\s*(.*?)(\n##\s|\Z)", text, re.S | re.I)
    if not m:
        return report(False, f"{rel} has a 'Numbers used' section")
    decls = [NUM_DECL.match(l) for l in m.group(1).splitlines()]
    decls = [d for d in decls if d]
    if not decls:
        return report(False, f"{rel} declares at least one number")
    bad = []
    for d in decls:
        key, val = d.group(1), float(d.group(2))
        actual = dotted(data, key)
        if actual is None:
            bad.append(f"{key} not in numbers.json")
        elif not close(val, actual):
            bad.append(f"{key} says {val}, numbers.json has {actual}")
    return report(not bad, f"{rel} numbers agree with numbers.json",
                  "; ".join(bad[:4]) if bad else f"{len(decls)} checked")


# ------------------------------------------------------------------ week gates

def week1():
    ok = True
    ok &= report((ROOT / "context.md").is_file(), "week1: context.md exists")
    ok &= report((ROOT / "stage-1" / "literature.md").is_file(), "week1: literature.md exists")
    ok &= require_headings("context.md", [
        "Stage 1: the seven required items",
        "Evaluation criteria",
        "The thrust-to-weight basis, settled",
    ])
    ok &= require_headings("stage-1/literature.md", [
        "Geometry and measured performance",
        "Published mass breakdowns",
    ])
    return ok


def week2(data):
    ok = True
    if data is None:
        return report(False, "week2: numbers.json exists and parses")

    keys = [
        "geometry.radius_m", "geometry.chord_m", "geometry.span_m", "geometry.blades",
        "geometry.airfoil", "geometry.pitch_amplitude_deg",
        "operating.rpm", "operating.tip_speed_ms", "operating.reynolds",
        "performance.thrust_N", "performance.blade_area_coeff",
        "performance.aero_power_W", "performance.electrical_power_W",
        "efficiency.transmission", "efficiency.motor", "efficiency.esc",
    ]
    ok &= require_keys(data, keys, "week2: numbers.json carries the week 2 schema")

    R = dotted(data, "geometry.radius_m")
    c = dotted(data, "geometry.chord_m")
    S = dotted(data, "geometry.span_m")
    nb = dotted(data, "geometry.blades")
    rpm = dotted(data, "operating.rpm")

    if None not in (R, c, S, nb, rpm):
        u = rpm * 2 * math.pi / 60 * R
        ok &= report(close(dotted(data, "operating.tip_speed_ms"), u),
                     "week2: tip speed reproduces from rpm and radius",
                     f"computed {u:.3f} m/s")
        re_n = u * c / NU
        ok &= report(close(dotted(data, "operating.reynolds"), re_n),
                     "week2: Reynolds reproduces from tip speed and chord",
                     f"computed {re_n:.0f}")
        ct = dotted(data, "performance.blade_area_coeff")
        if ct is not None:
            t = ct * 0.5 * RHO * u * u * nb * c * S
            ok &= report(close(dotted(data, "performance.thrust_N"), t),
                         "week2: thrust reproduces from geometry and coefficient",
                         f"computed {t:.3f} N")

    thrust = dotted(data, "performance.thrust_N")
    ok &= report(thrust is not None and thrust >= THRUST_MINIMUM_N,
                 "week2: thrust meets the 10 N requirement",
                 f"{thrust} N" if thrust is not None else "")

    ap = dotted(data, "performance.aero_power_W")
    chain = [dotted(data, f"efficiency.{k}") for k in ("transmission", "motor", "esc")]
    if ap is not None and None not in chain:
        ep = ap / (chain[0] * chain[1] * chain[2])
        ok &= report(close(dotted(data, "performance.electrical_power_W"), ep),
                     "week2: electrical power reproduces from aero power and the chain",
                     f"computed {ep:.1f} W")

    for rel, heads in [
        ("stage-1/design/01-configuration.md",
         ["Configuration", "Why one rotor", "Numbers used"]),
        ("stage-1/design/02-rotor-sizing.md",
         ["Rotor sizing", "Shape family", "Radius", "Numbers used"]),
        ("stage-1/design/04-thrust-and-power.md",
         ["Thrust", "Power", "Numbers used"]),
    ]:
        ok &= require_headings(rel, heads)
        ok &= check_declared_numbers(rel, data)
    return ok


def week3(data):
    ok = True
    if data is None:
        return report(False, "week3: numbers.json exists and parses")
    ok &= require_keys(data, [
        "pitch.mechanism", "pitch.offset_m", "pitch.phase_delay_deg",
        "pitch.vector_range_deg", "pitch.actuator_count", "pitch.actuator_mass_g",
        "pitch.side_force_tilt_deg",
    ], "week3: numbers.json carries the pitch and vectoring schema")

    rel = "stage-1/design/03-pitch-and-vectoring.md"
    ok &= require_headings(rel, [
        "Pitch mechanism", "Kinematics", "Thrust vectoring",
        "Side force", "Numbers used",
    ])
    ok &= check_declared_numbers(rel, data)

    p = ROOT / rel
    if p.is_file():
        text = p.read_text(encoding="utf-8")
        m = re.search(r"##+\s*Pitch schedule.*?\n(.*?)(\n##\s|\Z)", text, re.S | re.I)
        rows = 0
        if m:
            rows = len([l for l in m.group(1).splitlines()
                        if re.match(r"^\s*\|\s*-?\d", l)])
        ok &= report(rows >= 24, "week3: pitch schedule table has 24 or more azimuth rows",
                     f"found {rows}")

    vr = dotted(data, "pitch.vector_range_deg")
    ok &= report(isinstance(vr, (int, float)) and vr > 0,
                 "week3: thrust vector range is a number", str(vr))
    return ok


def week4(data):
    ok = True
    if data is None:
        return report(False, "week4: numbers.json exists and parses")

    budget = dotted(data, "mass_budget_g")
    ok &= report(isinstance(budget, list) and len(budget) >= 8,
                 "week4: mass budget has 8 or more line items",
                 f"found {len(budget) if isinstance(budget, list) else 0}")

    if isinstance(budget, list) and budget:
        nobasis = [b.get("item", "?") for b in budget
                   if not str(b.get("basis", "")).strip()]
        ok &= report(not nobasis, "week4: every mass line states a basis",
                     "missing: " + ", ".join(nobasis[:5]) if nobasis else "")

        required_lines = ["blade", "frame", "pitch", "motor", "actuator", "mount"]
        names = " ".join(str(b.get("item", "")).lower() for b in budget)
        absent = [r for r in required_lines if r not in names]
        ok &= report(not absent,
                     "week4: budget covers every component the problem statement names",
                     "missing: " + ", ".join(absent) if absent else "")

        total = sum(float(b.get("mass_g", 0)) for b in budget)
        stated = dotted(data, "results.total_mass_g")
        ok &= report(close(stated, total), "week4: mass lines sum to the stated total",
                     f"computed {total:.1f} g, stated {stated}")
        ok &= report(stated is not None and stated < MASS_LIMIT_G,
                     f"week4: module mass is under {MASS_LIMIT_G:.0f} g",
                     f"{stated} g" if stated is not None else "")

        thrust = dotted(data, "performance.thrust_N")
        if stated is not None and thrust is not None:
            w = stated / 1000.0 * G
            ok &= report(close(dotted(data, "results.weight_N"), w),
                         "week4: weight reproduces from mass", f"computed {w:.3f} N")
            tw = thrust / w
            ok &= report(close(dotted(data, "results.thrust_to_weight"), tw),
                         "week4: T/W reproduces from thrust and weight",
                         f"computed {tw:.3f}")
            ok &= report(tw > TW_MINIMUM, "week4: T/W clears 2.5", f"{tw:.3f}")

    for rel, heads in [
        ("stage-1/design/05-mass-and-tw.md",
         ["Mass budget", "Thrust-to-weight", "Margin", "Numbers used"]),
        ("stage-1/design/06-materials-and-manufacturing.md",
         ["Material selection", "Manufacturing", "Cost", "Numbers used"]),
    ]:
        ok &= require_headings(rel, heads)
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


def week5(data):
    ok = True
    ok &= require_headings("stage-1/design/07-team-and-execution.md",
                           ["Team capability", "Execution plan", "Stage 2"])

    sub = ROOT / "stage-1" / "submission" / "cycloprop-stage1.md"
    if not report(sub.is_file(), "week5: submission document exists"):
        return False
    text = sub.read_text(encoding="utf-8")

    missing = [it for it in REQUIRED_ITEMS if it.lower() not in text.lower()]
    ok &= report(not missing, "week5: all 7 required items are present as sections",
                 "missing: " + "; ".join(missing) if missing else "")

    ok &= report(re.search(r"evaluation criteria|criteria map", text, re.I) is not None,
                 "week5: submission carries the criteria map")

    if data:
        ok &= check_declared_numbers("stage-1/submission/cycloprop-stage1.md", data)
    return ok


WEEKS = {1: lambda d: week1(), 2: week2, 3: week3, 4: week4, 5: week5}


def done_weeks():
    out = []
    if PROGRESS_DIR.is_dir():
        for p in sorted(PROGRESS_DIR.glob("week-*.md")):
            m = re.search(r"week-(\d+)", p.name)
            if m and DONE_MARKER in p.read_text(encoding="utf-8"):
                out.append(int(m.group(1)))
    return sorted(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--week", type=int)
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--global", dest="glob", action="store_true")
    args = ap.parse_args()

    check_global()

    if not args.glob:
        data = load_numbers()
        targets = []
        if args.week:
            targets = [args.week]
        elif args.all:
            targets = done_weeks() or [1]
        for w in targets:
            if w not in WEEKS:
                report(False, f"week {w} is not in the plan")
                continue
            print(f"--- week {w} ---")
            WEEKS[w](data)

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
