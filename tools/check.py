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
import subprocess
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
MIN_MARGIN = 1.5

# A "conservative" case has to actually be conservative. Shaving 0.01 percent off the
# coefficient and calling it a lower bound satisfies an inequality and nothing else.
CONSERVATIVE_COEFF_MAX_RATIO = 0.90   # low coefficient at most 90 percent of nominal
CONSERVATIVE_MASS_MIN_RATIO = 1.05    # conservative mass at least 5 percent heavier

MODULE_COMPONENTS = ["blade", "frame", "pitch", "motor", "actuator", "mount"]

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
    """Numeric only. A string in a numeric field is a deferral dressed as a value,
    which is exactly what a Stage 1 paper design must not be allowed to ship."""
    bad = []
    for k in keys:
        v = dotted(data, k)
        if v is None:
            bad.append(f"{k} missing")
        elif num(data, k) is None:
            bad.append(f"{k}={v!r} is not a finite positive number")
    return report(not bad, label, "; ".join(bad[:6]) if bad else "")


def require_text(data, keys, label, min_chars=3):
    bad = []
    for k in keys:
        v = dotted(data, k)
        if not isinstance(v, str) or len(v.strip()) < min_chars:
            bad.append(f"{k}={v!r}")
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

    ap, tare = num(data, "performance.aero_power_W"), num(data, "performance.tare_power_W")
    if ap and tare:
        out["shaft_power_W"] = ap + tare
        chain = [num(data, f"efficiency.{k}") for k in ("transmission", "motor", "esc")]
        if all(chain):
            out["electrical_power_W"] = out["shaft_power_W"] / (chain[0] * chain[1] * chain[2])
            act = num(data, "performance.actuator_power_W")
            ctl = num(data, "performance.controller_power_W")
            if act and ctl:
                out["module_electrical_power_W"] = out["electrical_power_W"] + act + ctl

    for tag, dem, allow in (("blade_margin", "structure.blade_root_bending_Nm",
                             "structure.blade_allowable_Nm"),
                            ("shaft_margin", "structure.shaft_torque_Nm",
                             "structure.shaft_allowable_Nm")):
        d_, a_ = num(data, dem), num(data, allow)
        if d_ and a_:
            out[tag] = a_ / d_

    env = dotted(data, "mass_envelope_g")
    if isinstance(env, list) and env:
        try:
            out["mass_envelope_total_g"] = sum(float(b["nominal_g"]) for b in env)
            out["mass_envelope_conservative_g"] = sum(float(b["conservative_g"]) for b in env)
        except (TypeError, ValueError, KeyError):
            pass

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


# --------------------------------------------------- narrative numeric coverage

# Numbers that legitimately appear in prose without living in numbers.json: the
# competition requirements themselves, the rubric weights, and the published figures we
# cite. Anything else carrying a physical unit has to be a value we actually computed.
COVERAGE_ALLOW = {10.0, 2.5, 100.0, 5.0, 15.0}
UNIT_NUM = re.compile(r"(?<![\w.])(\d+(?:\.\d+)?)\s*(N|W|kW|g|kg|rpm|mm|m/s|deg)(?![\w])")
ALLOW_LINE = re.compile(r"<!--\s*allow\s*-->")


def collect_values(node, out):
    if isinstance(node, dict):
        for v in node.values():
            collect_values(v, out)
    elif isinstance(node, list):
        for v in node:
            collect_values(v, out)
    elif isinstance(node, (int, float)) and not isinstance(node, bool):
        out.add(float(node))


def check_numeric_coverage(rel, data):
    """Every number with a physical unit in the submission narrative has to trace to
    numbers.json, be a competition constant, or be explicitly allowed on its line.
    Scoped to the submission only: the design files are working documents, this is the
    thing that gets evaluated. Ambiguous cases get an inline allow comment and a human
    look at the final checkpoint."""
    p = ROOT / rel
    if not p.is_file():
        return False
    known = set(COVERAGE_ALLOW)
    collect_values(data, known)
    rounded = set()
    for v in known:
        for nd in (0, 1, 2):
            rounded.add(round(v, nd))
    known |= rounded

    unmatched = []
    for i, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
        stripped = line.strip()
        if stripped.startswith(">") or stripped.startswith("|") or ALLOW_LINE.search(line):
            continue                      # quotations, tables of published data, opt-outs
        for m in UNIT_NUM.finditer(line):
            val = float(m.group(1))
            if not any(abs(val - k) <= max(DISPLAY_TOL * abs(k), 1e-9) for k in known):
                unmatched.append(f"{i}: {m.group(0)}")
    return report(not unmatched, f"{rel} narrative numbers all trace to numbers.json",
                  f"{len(unmatched)} untraced: " + "; ".join(unmatched[:5]) if unmatched else "")


def check_pdf(rel):
    p = ROOT / rel
    if not report(p.is_file(), f"{rel} exists"):
        return False
    try:
        out = subprocess.run(["pdfinfo", str(p)], capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.SubprocessError) as e:
        return report(False, f"{rel} is a readable PDF", f"pdfinfo failed: {e}")
    if out.returncode != 0:
        return report(False, f"{rel} is a readable PDF", out.stderr.strip()[:120])
    pages = 0
    for line in out.stdout.splitlines():
        if line.lower().startswith("pages:"):
            pages = int(line.split(":", 1)[1].strip())
    return report(pages >= 4, f"{rel} is a readable PDF with 4 or more pages",
                  f"{pages} pages")


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
        "performance.tare_power_W", "performance.actuator_power_W",
        "performance.controller_power_W", "performance.module_electrical_power_W",
        "efficiency.transmission", "efficiency.motor", "efficiency.esc",
        "results.mass_g_conservative",
    ], "week2: numbers.json carries the week 2 schema as positive finite values")
    ok &= require_text(data, ["geometry.airfoil"], "week2: airfoil is named")
    ok &= require_text(data, ["sources.performance.blade_area_coeff",
                              "sources.performance.blade_area_coeff_low"],
                       "week2: both thrust coefficients carry a source record", 20)

    # The week 2 envelope is a coarse component list, not two scalars.
    env = dotted(data, "mass_envelope_g")
    ok &= report(isinstance(env, list) and len(env) >= 6,
                 "week2: mass envelope is a component list of 6 or more lines",
                 f"found {len(env) if isinstance(env, list) else type(env).__name__}")
    if isinstance(env, list) and env:
        bad = []
        for b in env:
            if not isinstance(b, dict):
                bad.append(repr(b)[:30]); continue
            for f in ("nominal_g", "conservative_g"):
                v = b.get(f)
                if not isinstance(v, (int, float)) or isinstance(v, bool) or v <= 0:
                    bad.append(f"{b.get('item','?')}.{f}={v!r}")
            if len(str(b.get("basis", "")).strip()) < MIN_BASIS_CHARS:
                bad.append(f"{b.get('item','?')} basis too thin")
        ok &= report(not bad, "week2: every envelope line has nominal, conservative and basis",
                     "; ".join(bad[:5]) if bad else "")
        names = " ".join(str(b.get("item", "")).lower() for b in env if isinstance(b, dict))
        absent = [x for x in MODULE_COMPONENTS if x not in names]
        ok &= report(not absent, "week2: envelope covers every component in the module boundary",
                     "missing: " + ", ".join(absent) if absent else "")

    sweep = dotted(data, "power_by_radius")

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
        ok &= report(cl <= cn * CONSERVATIVE_COEFF_MAX_RATIO,
                     f"week2: the low coefficient is at most {CONSERVATIVE_COEFF_MAX_RATIO:.0%} of nominal",
                     f"low {cl} vs nominal {cn}, ratio {cl / cn:.3f}")

    # Feasibility envelope: the conservative mass must still clear T/W at conservative thrust.
    mc, tc = num(data, "results.mass_g_conservative"), r.get("thrust_N_conservative")
    if mc and "mass_envelope_total_g" in r:
        ok &= report(close(r["mass_envelope_total_g"], num(data, "results.mass_envelope_g"))
                     if num(data, "results.mass_envelope_g") else True,
                     "week2: stated envelope total matches the component lines")
        ok &= report(mc >= r["mass_envelope_total_g"] * CONSERVATIVE_MASS_MIN_RATIO,
                     f"week2: conservative mass is at least {CONSERVATIVE_MASS_MIN_RATIO:.0%} of nominal",
                     f"{mc:.1f} g vs envelope {r['mass_envelope_total_g']:.1f} g")
        ok &= report(close(mc, r["mass_envelope_conservative_g"], DISPLAY_TOL),
                     "week2: conservative mass matches the conservative envelope lines",
                     f"lines give {r.get('mass_envelope_conservative_g', 0):.1f} g")
    if mc and tc:
        tw = tc / (mc / 1000.0 * G)
        ok &= report(tw > TW_MINIMUM,
                     "week2: conservative mass and thrust still clear T/W 2.5",
                     f"T/W {tw:.3f} at {tc:.2f} N and {mc:.0f} g")
        note("week2: planning mass ceiling at this thrust",
             f"{tc / (TW_MINIMUM * G) * 1000:.0f} g "
             f"({PLANNING_MASS_AT_10N_G:.0f} g would apply only at exactly 10 N)")

    if "electrical_power_W" in r:
        ok &= report(close(num(data, "performance.electrical_power_W"), r["electrical_power_W"]),
                     "week2: rotor electrical power reproduces from shaft power and the chain",
                     f"computed {r['electrical_power_W']:.1f} W")
    if "module_electrical_power_W" in r:
        ok &= report(close(num(data, "performance.module_electrical_power_W"),
                           r["module_electrical_power_W"]),
                     "week2: module electrical power adds actuator and controller draw",
                     f"computed {r['module_electrical_power_W']:.1f} W")
    chain = [num(data, f"efficiency.{k}") for k in ("transmission", "motor", "esc")]
    for e in chain:
        if e and not 0 < e <= 1:
            ok &= report(False, "week2: efficiencies are fractions between 0 and 1", str(e))

    ok &= report(isinstance(sweep, list) and len(sweep) >= 3,
                 "week2: power is evaluated across at least 3 candidate radii",
                 f"found {len(sweep) if isinstance(sweep, list) else 0}")
    if isinstance(sweep, list) and sweep:
        radii, bad = [], []
        for row in sweep:
            if not isinstance(row, dict):
                bad.append(repr(row)[:30]); continue
            r_, p_ = row.get("radius_m"), row.get("aero_power_W")
            for tag, v in (("radius_m", r_), ("aero_power_W", p_)):
                if not isinstance(v, (int, float)) or isinstance(v, bool) or v <= 0:
                    bad.append(f"{tag}={v!r}")
            if isinstance(r_, (int, float)):
                radii.append(float(r_))
        ok &= report(not bad, "week2: every sweep row has a positive radius and power",
                     "; ".join(bad[:5]) if bad else "")
        ok &= report(len(set(radii)) == len(radii) and len(set(radii)) >= 3,
                     "week2: sweep radii are distinct", f"{sorted(set(radii))}")

    for rel, heads in [
        ("stage-1/design/01-configuration.md",
         ["Configuration", "Why this configuration", "Numbers used"]),
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
    ok &= require_text(data, ["pitch.mechanism"], "week3: pitch mechanism is named", 6)

    rel = "stage-1/design/03-pitch-and-vectoring.md"
    ok &= require_headings(rel, ["Pitch mechanism", "Kinematics", "Pitch schedule",
                                 "Thrust vectoring", "Side force", "Numbers used"])
    ok &= require_substance(rel, 500)
    ok &= check_declared_numbers(rel, data)

    p = ROOT / rel
    if p.is_file():
        m = re.search(r"#{2,}\s*Pitch schedule.*?\n(.*?)(\n#{2,}\s|\Z)",
                      p.read_text(encoding="utf-8"), re.S | re.I)
        az, pitches, malformed, seen_data = [], [], 0, False
        if m:
            for l in m.group(1).splitlines():
                if not l.strip().startswith("|") or set(l.strip()) <= set("|- :"):
                    continue                      # not a row, or the separator
                cells = [c.strip() for c in l.strip().strip("|").split("|")]
                try:
                    az.append(float(cells[0]))
                    pitches.append(float(cells[1]))
                    seen_data = True
                except (ValueError, IndexError):
                    if seen_data:                 # a header before any data row is fine
                        malformed += 1
        ok &= report(malformed == 0, "week3: every pitch schedule row is numeric",
                     f"{malformed} malformed rows")
        amp = num(data, "geometry.pitch_amplitude_deg")
        if pitches and amp:
            over = [p_ for p_ in pitches if abs(p_) > amp * 1.02]
            ok &= report(not over,
                         "week3: no scheduled pitch angle exceeds the stated amplitude",
                         f"{len(over)} rows over {amp} deg")
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
        "structure.blade_mass_kg", "structure.centrifugal_load_N",
        "structure.blade_root_bending_Nm", "structure.shaft_torque_Nm",
        "structure.blade_allowable_Nm", "structure.shaft_allowable_Nm",
        "structure.blade_margin", "structure.shaft_margin",
    ], "week4: numbers.json carries the structural schema")

    # Margins are derived from allowable over demand, never asserted.
    for tag in ("blade_margin", "shaft_margin"):
        v, computed = num(data, f"structure.{tag}"), r.get(tag)
        if computed is not None:
            ok &= report(close(v, computed),
                         f"week4: {tag} reproduces from allowable over demand",
                         f"computed {computed:.3f}, stated {v}")
            ok &= report(computed >= MIN_MARGIN,
                         f"week4: {tag} is at least {MIN_MARGIN}", f"{computed:.3f}")

    # Centrifugal load is the one structural number checkable from first principles.
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

    ok &= check_numeric_coverage("stage-1/submission/cycloprop-stage1.md", data)
    ok &= check_pdf("stage-1/submission/cycloprop-stage1.pdf")

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
