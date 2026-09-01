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
MIN_MARGIN = 1.5
MIN_DECLARED_NUMBERS = 3
GROUP_DRIFT_MAX = 0.25   # week 4 refines week 2's envelope, per component and in total
MIN_BUDGET_LINES = 8     # below this the refined budget is not a budget

# The rotor is speed controlled and centrifugal load goes as the square of speed, so a
# structure signed off at exactly the design rpm has no answer for control overshoot. The
# overspeed case has to be declared and it has to be worth declaring: 1.001 satisfies an
# inequality and nothing else.
MIN_OVERSPEED = 1.10

# Momentum theory gives the power no rotor can beat. Applied to a cyclorotor the standard
# closure is the projected frontal area, 2R times span, so the area may not be inflated
# past that to soften the bound. A figure of merit is ideal over actual: above 0.75 is not
# a cyclorotor result, and below 0.20 usually means an arithmetic error rather than a bad
# rotor. Without this floor the gate certified 13.5 N produced by 1 W.
FM_MAX = 0.75
FM_MIN = 0.20

# Kellen 2019 measured the optimum for this shape family at a solidity of 0.30 to 0.40.
# The 0.607 coefficient is transferred into that family, and the transfer is only
# defensible inside the band it was measured in. Leaving the band means re-deriving the
# coefficient, not carrying it across and hoping.
SOLIDITY_MIN, SOLIDITY_MAX = 0.30, 0.40

# Peak blade thrust runs 3 to 4 times the cycle mean on 2 and 3 bladed rotors, which a
# cycle-averaged coefficient hides completely. The range is simulated, so take the top of
# it rather than the bottom. Heimerl et al. measured instantaneous blade forces across
# Re 30,000 to 100,000, which brackets our band; replace this with their measured figure
# when that paper is in hand. Aero peak is not the whole story either: at Runco's scale
# centrifugal load beat aerodynamic load by 4.4 times, so the blade attachment gets its own
# margin against the recomputed centrifugal force.
MIN_BLADE_LOAD_FACTOR = 4.0
MAX_POWER_SPREAD = 0.35   # primary estimate against the published power-loading route
MIN_BLADES = 2
MIN_MOUNT_POINTS = 2

# Setting pitch.vector_range_deg equal to pitch.phase_authority_deg is a claim that thrust
# direction follows the phase command one to one. Comparing those two scalars only checks
# that the same number was written twice, so the force table is asked as well: how far the
# commands reach, whether they sit inside what the mechanism can drive, and whether the
# direction the forces imply turns with the command instead of sitting still.
VECTOR_TRACKING_TOL_DEG = 15.0
VECTOR_EVIDENCE_FRACTION = 0.5   # commands must cover half the claimed range
LATERAL_TRIM_FRACTION = 0.05     # cycle mean lateral against cycle mean vertical

# A "conservative" case has to actually be conservative. Shaving 0.01 percent off the
# coefficient and calling it a lower bound satisfies an inequality and nothing else.
CONSERVATIVE_COEFF_MAX_RATIO = 0.90   # low coefficient at most 90 percent of nominal
MEASURED_COEFF_MAX_RATIO = 0.95       # floor once this shape family has been measured
SHAPE_FAMILY_TOL = 0.10               # how close a measured rotor sits to this one
CONSERVATIVE_MASS_MIN_RATIO = 1.05    # conservative mass at least 5 percent heavier

MODULE_COMPONENTS = ["blade", "frame", "pitch", "motor", "actuator", "mount"]

VERBATIM_DIRS = {"reference"}
# Documents written by someone else and kept as received. The style rules exist so our own
# prose reads as ours; rewriting incoming evidence to satisfy them would damage it.
VERBATIM_FILES = {"_research.md"}
RULES_FILES = {".claude/weekly-loop.md"}
BANNED_ATTRIBUTION = ["co-authored-by", "generated with claude", "claude opus", "anthropic"]

FAILURES = []


def report(ok, label, detail="", fail_detail=None):
    """`detail` is true on both branches. `fail_detail` describes the failure and is only
    printed when the check fails: a passing line that reads "the chosen radius appears in
    the sweep  0.11 not among [0.1, 0.11, ...]" is a contradiction sitting in exactly the
    place a person reads gate output."""
    shown = detail if ok or fail_detail is None else fail_detail
    print(("PASS  " if ok else "FAIL  ") + label + (("  " + shown) if shown else ""))
    if not ok:
        FAILURES.append(label + (("  " + shown) if shown else ""))
    return bool(ok)


def note(label, detail=""):
    print("note  " + label + (("  " + detail) if detail else ""))


def md_files():
    for p in sorted(ROOT.rglob("*.md")):
        rel = p.relative_to(ROOT)
        if (rel.parts and rel.parts[0] in VERBATIM_DIRS) or ".git" in rel.parts:
            continue
        if rel.as_posix() in VERBATIM_FILES:
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


def snum(data, path):
    """Return any finite number, or None. The same guards as `num` without the sign rule,
    for quantities that are legitimately zero or negative: phase commands, lateral forces,
    phase angles. Using `num` on those silently drops half the table."""
    v = dotted(data, path)
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        return None
    return v if math.isfinite(v) else None


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


def require_integer(data, keys, label, minimum=1):
    """Hardware comes in whole units. Half an actuator and a tenth of a mount point both
    satisfied a positive-number check, and neither feeds an equation that would catch it."""
    bad = []
    for k in keys:
        v = num(data, k)
        if v is None:
            bad.append(f"{k}={dotted(data, k)!r}")
        elif abs(v - round(v)) > 1e-9:
            bad.append(f"{k}={v} is not a whole number")
        elif v < minimum:
            bad.append(f"{k}={v:.0f} is below {minimum}")
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
NUM_TOKEN = re.compile(r"\d+\.\d+")


def states_value(rel, value, tol=TOL):
    """True when the document's narrative quotes this value, at any rounding inside `tol`.
    Matching numeric tokens rather than one formatted string means 2.25, 2.252 and 2.2525
    all count, which is what a document written by a person actually looks like.

    The `## Numbers used` block is cut off first. A declaration is machine-readable and a
    reader skimming the prose never sees it, so a document whose only copy of the number
    sits in that block has not said the thing this gate exists to make it say."""
    p = ROOT / rel
    if not p.is_file() or value is None:
        return False
    narrative = re.split(r"##\s*Numbers used", p.read_text(encoding="utf-8"),
                         maxsplit=1, flags=re.I)[0]
    for m in NUM_TOKEN.finditer(narrative):
        if close(float(m.group()), value, tol):
            return True
    return False


def check_declared_numbers(rel, data):
    p = ROOT / rel
    if not p.is_file():
        return False                    # require_headings already reported it
    text = p.read_text(encoding="utf-8")
    m = re.search(r"##\s*Numbers used\s*(.*?)(\n##\s|\Z)", text, re.S | re.I)
    if not m:
        return report(False, f"{rel} has a 'Numbers used' section")
    decls = [d for d in (NUM_DECL.match(l) for l in m.group(1).splitlines()) if d]
    # Distinct keys. Three copies of one radius is one number written three times.
    distinct = {d.group(1) for d in decls}
    if len(distinct) < MIN_DECLARED_NUMBERS:
        return report(False, f"{rel} declares at least {MIN_DECLARED_NUMBERS} distinct numbers",
                      f"{len(decls)} declarations covering {len(distinct)} key(s)")
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

    # Momentum floor. Uses recomputed thrust, so an optimistic stored thrust cannot buy a
    # softer bound, and the declared area, so the closure being used is visible.
    area = num(data, "performance.momentum_area_m2")
    if area and "thrust_N" in out:
        out["ideal_power_W"] = out["thrust_N"] ** 1.5 / math.sqrt(2 * RHO * area)
        if R and S:
            out["momentum_area_max_m2"] = 2 * R * S
    ap0 = num(data, "performance.aero_power_W")
    if ap0 and "ideal_power_W" in out:
        out["figure_of_merit"] = out["ideal_power_W"] / ap0

    # Second route: published power loading, which is an independent closure rather than
    # the same equation rearranged.
    pl = num(data, "performance.power_loading_ref_N_per_W")
    if pl and "thrust_N" in out:
        out["aero_power_W_published"] = out["thrust_N"] / pl
        if ap0:
            out["power_spread"] = abs(ap0 - out["aero_power_W_published"]) / ap0

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
                             "structure.shaft_allowable_Nm"),
                            ("pitch_link_margin", "structure.pitch_link_load_N",
                             "structure.pitch_link_allowable_N")):
        d_, a_ = num(data, dem), num(data, allow)
        if d_ and a_:
            out[tag] = a_ / d_

    # Structural demands are derived, not asserted. A reviewer recomputes rotor shaft
    # torque from shaft power and speed in about ten seconds, so the gate does it first.
    ratio = num(data, "structure.transmission_ratio")
    if "shaft_power_W" in out and rpm and ratio:
        omega = rpm * 2 * math.pi / 60
        out["rotor_omega_rad_s"] = omega
        out["shaft_torque_Nm_derived"] = out["shaft_power_W"] / omega
        out["motor_torque_Nm_derived"] = out["shaft_power_W"] / (omega * ratio)

    # Per-blade mass follows from the blade mass budget and the blade count. It used to be
    # an independent number, so a 1 g blade could sit beside a 108 g blade budget.
    budget_rows = dotted(data, "mass_budget_g")
    if isinstance(budget_rows, list) and nb:
        blade_g = sum(float(b["mass_g"]) for b in budget_rows
                      if isinstance(b, dict) and "blade" in str(b.get("item", "")).lower()
                      and isinstance(b.get("mass_g"), (int, float))
                      and not isinstance(b.get("mass_g"), bool))
        if blade_g > 0:
            out["blade_mass_kg_derived"] = blade_g / 1000.0 / nb

    over = num(data, "structure.overspeed_factor")
    if None not in (R, rpm, mb_stored := num(data, "structure.blade_mass_kg")):
        fc = mb_stored * (rpm * 2 * math.pi / 60) ** 2 * R
        out["centrifugal_load_N_derived"] = fc
        att = num(data, "structure.blade_attachment_allowable_N")
        if att:
            out["blade_attachment_margin"] = att / fc
        if over:
            # Centrifugal load goes as the square of speed, so the overspeed case is not a
            # rounding on the design one. Runco measured centrifugal beating aerodynamic by
            # 4.4 times at the design point; the declared overspeed is where the blade
            # attachment is actually decided.
            out["centrifugal_load_overspeed_N_derived"] = fc * over ** 2
            if att:
                out["blade_attachment_margin_overspeed"] = att / (fc * over ** 2)

    lever, lf = num(data, "structure.blade_load_lever_m"), num(data, "structure.blade_load_factor")
    if lever and lf and nb and "thrust_N" in out:
        out["blade_root_bending_Nm_derived"] = out["thrust_N"] / nb * lever * lf
    fc_stored = num(data, "structure.centrifugal_load_N")
    if lever and fc_stored:
        out["blade_centrifugal_bending_Nm_derived"] = fc_stored * lever

    # The gated blade margin is aerodynamic bending alone, and on a cyclorotor that is the
    # smaller of the two spanwise loads. The section has to carry both at once, so the
    # combined case gets its own margin and its own overspeed version.
    b_all = num(data, "structure.blade_allowable_Nm")
    b_aero = num(data, "structure.blade_root_bending_Nm")
    b_cf = num(data, "structure.blade_centrifugal_bending_Nm")
    if b_all and b_aero and b_cf:
        out["blade_combined_margin"] = b_all / (b_aero + b_cf)
        if over:
            out["blade_combined_margin_overspeed"] = b_all / ((b_aero + b_cf) * over ** 2)

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

# A number in prose is only traceable if its VALUE and its DIMENSION both match something
# we computed. Matching on value alone let "400 N" pass because 400 was a packaging
# dimension in millimetres.
#
# Canonical units: force N, power W, mass g, length m, angle deg, torque Nm, speed m/s,
# rotation rpm.
KEY_UNITS = [("_Nm", ("torque", 1.0)), ("_ms", ("speed", 1.0)), ("_mm", ("length", 0.001)),
             ("_kg", ("mass", 1000.0)), ("_deg", ("angle", 1.0)), ("_rpm", ("rot", 1.0)),
             ("_N", ("force", 1.0)), ("_W", ("power", 1.0)), ("_g", ("mass", 1.0)),
             ("_m", ("length", 1.0))]
PROSE_UNITS = {"kW": ("power", 1000.0), "kg": ("mass", 1000.0), "mm": ("length", 0.001),
               "Nm": ("torque", 1.0), "m/s": ("speed", 1.0), "rpm": ("rot", 1.0),
               "degrees": ("angle", 1.0), "degree": ("angle", 1.0), "deg": ("angle", 1.0),
               "N": ("force", 1.0), "W": ("power", 1.0),
               "g": ("mass", 1.0), "m": ("length", 1.0)}

# The one dimensioned constant that belongs in prose without being a computed value.
COVERAGE_ALLOW = {(10.0, "force")}

# Scientific notation is included because 9.99e2 N is a fabricated number that the plain
# pattern walked straight past.
# The decimal grammar covers 999, 999.5, .999, 999. and 9.99e2, because every form the
# matcher did not recognise was a number nobody was checking.
# "degrees" and "degree" come before "deg" in the alternation and it matters: the regex
# takes the first branch that matches, so with "deg" first, "40 degrees" matched "deg",
# failed the lookahead on the "r", and left the number unaudited. The submission writes
# angles out in words, so that one ordering hid every angle claim in the document.
UNIT_NUM = re.compile(
    r"(?<![\w.])(-?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?)\s*"
    r"(kW|kg|mm|Nm|m/s|rpm|degrees|degree|deg|N|W|g|m)(?![\w/])")
# An escape has to say why it exists, and the ceiling counts the NUMBERS it hides rather
# than the markers themselves. One marker can cover a whole line or a whole table, so
# counting markers measured the wrong thing.
ANY_ALLOW = re.compile(r"<!--\s*allow(-table)?\s*:?(.*?)-->")
MIN_ALLOW_REASON = 15
MAX_UNCHECKED_NUMBERS = 4


def allow_reason(line, table=False):
    """A stated reason has to contain 15 characters of actual reason. Counting characters
    in the pattern let 15 spaces through, which is a bare escape wearing a hat."""
    for m in ANY_ALLOW.finditer(line):
        if bool(m.group(1)) == table and len(m.group(2).strip()) >= MIN_ALLOW_REASON:
            return True
    return False


# A unit suffix is often followed by a qualifier: thrust_N_conservative is a force,
# mass_g_conservative is a mass, aero_power_W_published is a power. Matching the unit only
# at the very end of the key meant none of those registered as a computed value, so the
# submission's own conservative thrust of 17.10 N could not trace to the number that
# produced it. Week 3 found this on the draft and recorded it; the fix is to peel the
# qualifiers off before matching, not to widen the match, which would let
# power_loading_ref_N_per_W be read as two different dimensions.
KEY_QUALIFIERS = {"conservative", "low", "high", "published", "derived", "nominal",
                  "min", "max", "total", "design", "stated", "corrected"}


def dim_of_key(key):
    if key == "rpm":
        return ("rot", 1.0)
    parts = key.split("_")
    while len(parts) > 1 and parts[-1].lower() in KEY_QUALIFIERS:
        parts.pop()
    trimmed = "_".join(parts)
    for suffix, du in KEY_UNITS:
        if trimmed.endswith(suffix):
            return du
    return None


def front_matter_lines(text):
    """How many leading lines belong to a pandoc YAML front matter block. 0 when there is
    none.

    That block is build configuration: a page margin, a font size, a title, a toc flag. It
    is not a claim about the design, so the coverage audit has no business reading
    `margin=25mm` as a length somebody has to justify from `numbers.json`. Skipping it is
    positional and not a string exemption, so the same text in the body still fails.

    An opening `---` with no closing delimiter counts as no front matter. Otherwise a stray
    horizontal rule on line 1 would hide an entire document from the audit."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return 0
    for i, line in enumerate(lines[1:], 2):
        if line.strip() in ("---", "..."):
            return i
    return 0


def collect_dimensioned(node, out, key=""):
    if isinstance(node, dict):
        for k, v in node.items():
            collect_dimensioned(v, out, k)
    elif isinstance(node, list):
        for v in node:
            collect_dimensioned(v, out, key)
    elif isinstance(node, (int, float)) and not isinstance(node, bool):
        du = dim_of_key(key)
        if du:
            out.add((float(node) * du[1], du[0]))


def check_numeric_coverage(rel, data):
    """Every number in the submission narrative that carries a physical unit has to match
    a computed value in the same dimension, be the 10 N requirement, or sit inside an
    exempt region: a blockquote, an allow-line, or an allow-table.

    The YAML front matter block is not narrative at all and is skipped before any of that,
    per `front_matter_lines`.

    Exempt does not mean free. A number inside an exempt region that still fails to trace
    counts against a hard ceiling, because the promise being kept here is that at most a
    handful of numbers in the submission are unchecked by anything. Counting markers let
    one marker hide a twenty-row table and kept that promise only on paper."""
    p = ROOT / rel
    if not p.is_file():
        return False
    known = set(COVERAGE_ALLOW)
    collect_dimensioned(data, known)

    text = p.read_text(encoding="utf-8")
    bare = [m.group(0) for m in ANY_ALLOW.finditer(text)
            if len(m.group(2).strip()) < MIN_ALLOW_REASON]
    ok = report(not bare, f"{rel} every audit escape states a reason",
                "; ".join(bare[:3]) if bare else "")

    front_matter = front_matter_lines(text)
    unmatched, unchecked, table_exempt = [], [], False
    for i, line in enumerate(text.splitlines(), 1):
        if i <= front_matter:
            continue                       # build configuration, not a technical claim
        stripped = line.strip()
        if allow_reason(line, table=True):
            table_exempt = True
            continue
        is_table = stripped.startswith("|")
        if not is_table and stripped:
            table_exempt = False
        exempt = (stripped.startswith(">") or allow_reason(line)
                  or (is_table and table_exempt))
        for m in UNIT_NUM.finditer(line):
            val, unit = float(m.group(1)), m.group(2)
            dim, scale = PROSE_UNITS[unit]
            canon = val * scale
            if any(d == dim and abs(canon - k) <= max(DISPLAY_TOL * abs(k), 1e-12)
                   for k, d in known):
                continue                       # traces, so an exemption costs nothing
            (unchecked if exempt else unmatched).append(f"{i}: {m.group(0)}")
    ok &= report(not unmatched, f"{rel} narrative numbers all trace to numbers.json",
                 f"{len(unmatched)} untraced: " + "; ".join(unmatched[:5]) if unmatched else "")
    ok &= report(len(unchecked) <= MAX_UNCHECKED_NUMBERS,
                 f"{rel} exempts at most {MAX_UNCHECKED_NUMBERS} untraceable numbers",
                 f"{len(unchecked)} exempted: " + "; ".join(unchecked[:6])
                 if unchecked else "")
    return ok


def section_under(text, keyword):
    """Lines under the first heading containing keyword, up to the next heading.
    Written as a line walk so the pattern carries no newline escapes."""
    out, capturing = [], False
    for line in text.splitlines():
        if line.startswith("#"):
            if capturing:
                break
            capturing = keyword.lower() in line.lower()
            continue
        if capturing:
            out.append(line)
    return out if capturing or out else None


LIGATURES = {"\ufb00": "ff", "\ufb01": "fi", "\ufb02": "fl", "\ufb03": "ffi",
             "\ufb04": "ffl", "\ufb05": "st", "\ufb06": "st"}


def pdf_text(path):
    """Read with pypdf rather than shelling out to pdfinfo, which resolves to whatever
    happens to be on PATH and is not guaranteed to be a working poppler build.

    xelatex sets ligatures as single glyphs and pypdf hands them back that way, so the
    word "off" comes out as one character followed by an f and no search for it can
    match. Expanding them here means the caller never has to know."""
    import pypdf
    reader = pypdf.PdfReader(str(path))
    text = "\n".join(pg.extract_text() or "" for pg in reader.pages)
    for glyph, plain in LIGATURES.items():
        text = text.replace(glyph, plain)
    return len(reader.pages), text


def check_pdf(rel, min_pages=4, must_contain=()):
    """The attachment is what gets evaluated, so it has to be THIS submission. Page count
    and readability alone accepted an unrelated PDF: the week 5 fixture passed while
    attaching the competition's own problem statement."""
    p = ROOT / rel
    if not report(p.is_file(), f"{rel} exists"):
        return False
    try:
        pages, text = pdf_text(p)
    except Exception as e:
        return report(False, f"{rel} is a readable PDF", f"{type(e).__name__}: {e}")
    ok = report(pages >= min_pages, f"{rel} is a readable PDF with {min_pages}+ pages",
                f"{pages} pages")
    if must_contain:
        # Compared with the whitespace taken out entirely, not merely collapsed. Kerning
        # puts a space inside a word on the contents page, so "Team capability" extracts
        # as "T eam capability" there while the same heading in the body comes out clean.
        # A gate that fails on a correctly built PDF is worse than one that tolerates a
        # space, and the strings being matched are long enough that dropping whitespace
        # cannot make an unrelated document look like this one.
        flat = "".join(text.split()).lower()
        absent = [s for s in must_contain if "".join(s.split()).lower() not in flat]
        ok &= report(not absent, f"{rel} is built from this submission, not another document",
                     f"{len(absent)} expected string(s) absent: "
                     + "; ".join(absent[:4]) if absent else "")
    return ok


# ------------------------------------------------------------------ week gates


ROW_SPECS = {
    # key: (min_rows, required fields, owning week). Added after a review supplied these
    # lists to the schema with no row shape and no gate, which is how an unchecked number
    # gets into a submission.
    "configuration_candidates": (3, ("config", "module_mass_g", "thrust_N"), 2),
    "coefficient_scenarios": (3, ("name", "blade_area_coeff", "basis", "evidence_class"), 2),
    "aero_azimuthal_loads": (24, ("azimuth_deg", "normal_force_N",
                              "lateral_force_N"), 2),
    "drive_candidates": (2, ("name", "continuous_power_W", "continuous_torque_Nm", "mass_g"), 2),
    "linkage_dimensions": (4, ("link", "length_mm"), 3),
    "pitch_schedule": (24, ("azimuth_deg", "pitch_deg"), 3),
    "vector_map": (3, ("phase_command_deg", "vertical_force_N", "lateral_force_N"), 3),
}
EVIDENCE_CLASSES = {"measured", "derived", "downside"}
SCALING_CLASSES = {"geometry", "power", "fixed"}


def require_rows(data, key, week):
    """A list in the schema that no gate reads is a place to keep a number nobody checks."""
    min_rows, fields, _ = ROW_SPECS[key]
    rows = dotted(data, key)
    if not report(isinstance(rows, list) and len(rows) >= min_rows,
                  f"week{week}: {key} has {min_rows} or more rows",
                  f"found {len(rows) if isinstance(rows, list) else type(rows).__name__}"):
        return False
    bad = []
    for i, r in enumerate(rows):
        if not isinstance(r, dict):
            bad.append(f"row {i} is not an object"); continue
        for f in fields:
            v = r.get(f)
            if v is None or (isinstance(v, str) and not v.strip()):
                bad.append(f"row {i} missing {f}")
    return report(not bad, f"week{week}: every {key} row is complete",
                  "; ".join(bad[:5]) if bad else f"{len(rows)} rows")


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


def check_thrust_sensitivity(data, r):
    """Week 2 freezes what raising thrust actually costs, so week 4 cannot treat it as a
    free knob on the numerator of T/W. Within the fixed shape family, raising thrust from
    10 N to 13 N buys 30 percent of mass ceiling and spends 14 percent more rpm, 30 percent
    more centrifugal load and 48 percent more ideal power. That can move the motor, the
    transmission, the thermal case and the structure, none of which fits in week 4."""
    rows = dotted(data, "thrust_sensitivity")
    ok = report(isinstance(rows, list) and len(rows) >= 3,
                "week2: a thrust sensitivity table covers at least 3 candidate thrusts",
                f"found {len(rows) if isinstance(rows, list) else 0}")
    if not (isinstance(rows, list) and rows):
        return ok

    area = num(data, "performance.momentum_area_m2")
    bad, thrusts = [], []
    for row in rows:
        if not isinstance(row, dict):
            bad.append(repr(row)[:30]); continue
        vals = {}
        for f in ("thrust_N", "mass_ceiling_g", "ideal_power_W", "rpm"):
            v = row.get(f)
            if not isinstance(v, (int, float)) or isinstance(v, bool) or v <= 0:
                bad.append(f"{row.get('thrust_N', '?')} N row: {f}={v!r}")
            else:
                vals[f] = float(v)
        if len(vals) < 4:
            continue
        thrusts.append(vals["thrust_N"])
        # The ceiling is what T/W above 2.5 allows, floored because the inequality is strict.
        ceiling = math.floor(vals["thrust_N"] / (TW_MINIMUM * G) * 1000.0)
        if abs(vals["mass_ceiling_g"] - ceiling) > 1.0:
            bad.append(f"{vals['thrust_N']} N: ceiling {vals['mass_ceiling_g']} g, "
                       f"the inequality gives {ceiling} g")
        if area:
            ideal = vals["thrust_N"] ** 1.5 / math.sqrt(2 * RHO * area)
            if not close(vals["ideal_power_W"], ideal, DISPLAY_TOL):
                bad.append(f"{vals['thrust_N']} N: ideal power {vals['ideal_power_W']} W, "
                           f"momentum gives {ideal:.1f} W")
    ok &= report(not bad, "week2: every sensitivity row reproduces its ceiling and ideal power",
                 "; ".join(bad[:4]) if bad else "")

    design = num(data, "performance.thrust_N")
    if design and thrusts:
        ok &= report(any(close(design, t, DISPLAY_TOL) for t in thrusts),
                     "week2: the design thrust is one of the prequalified rows",
                     f"{design} N, rows {sorted(thrusts)}",
                     fail_detail=f"{design} N not among {sorted(thrusts)}")
    return ok


def measured_shape_family(data, sigma, c_over_r, nominal):
    """The measured coefficient scenario, if any, that was taken on this design's own shape
    family. Returns the scenario or None. Fails closed: a scenario that does not declare its
    solidity and chord to radius cannot match, so the narrow floor stays out of reach unless
    somebody wrote down what was actually measured."""
    if not sigma or not c_over_r or not nominal:
        return None
    for s in data.get("coefficient_scenarios") or []:
        if not isinstance(s, dict) or s.get("evidence_class") != "measured":
            continue
        sg, cr, co = s.get("solidity"), s.get("chord_to_radius"), s.get("blade_area_coeff")
        if not all(isinstance(v, (int, float)) and not isinstance(v, bool) and v > 0
                   for v in (sg, cr, co)):
            continue
        if (abs(sg - sigma) <= SHAPE_FAMILY_TOL * sigma
                and abs(cr - c_over_r) <= SHAPE_FAMILY_TOL * c_over_r
                and co >= nominal):
            return s
    return None


def check_week2_selection(data, r):
    """Three of the lists week 2 fills carried numbers that no gate read. A drive that
    cannot hold the design point continuously, a candidate table whose winner is not the
    row the stated first metric picks, and an azimuthal distribution that does not average
    to the thrust it claims to be distributing all passed a shape check and nothing else.

    Added in week 2 after an audit pointed out that a 36 row table of arbitrary positive
    numbers satisfied the azimuthal gate identically to a real one."""
    ok = True
    nb, thrust = num(data, "geometry.blades"), r.get("thrust_N")

    # The azimuthal table distributes the thrust, so its cycle mean has to reproduce it.
    rows = dotted(data, "aero_azimuthal_loads")
    if isinstance(rows, list) and rows and nb and thrust:
        vals = [x.get("normal_force_N") for x in rows if isinstance(x, dict)]
        if vals and all(isinstance(v, (int, float)) and not isinstance(v, bool)
                        for v in vals):
            mean = sum(vals) / len(vals)
            ok &= report(close(mean * nb, thrust, DISPLAY_TOL),
                         "week2: the azimuthal loads average to the design thrust",
                         f"{len(vals)} rows, mean {mean:.4f} N times {nb:.0f} blades gives "
                         f"{mean * nb:.3f} N against a recomputed {thrust:.3f} N")

    # Exactly one drive is selected, its continuous rating covers the recomputed motor
    # input power, and its continuous torque follows from KV and continuous current
    # rather than being asserted beside them.
    drives = dotted(data, "drive_candidates")
    if isinstance(drives, list) and drives:
        sel = [x for x in drives if isinstance(x, dict) and x.get("selected") is True]
        ok &= report(len(sel) == 1, "week2: exactly one drive candidate is selected",
                     f"{len(sel)} of {len(drives)} rows marked selected")
        bad = []
        for x in drives:
            if not isinstance(x, dict):
                continue
            kv, ia, tq = x.get("kv"), x.get("continuous_current_A"), x.get("continuous_torque_Nm")
            if not all(isinstance(v, (int, float)) and not isinstance(v, bool) and v > 0
                       for v in (kv, ia, tq)):
                bad.append(f"{x.get('name', '?')} has no KV and continuous current")
            else:
                want = 9.5493 / kv * ia
                if abs(tq - want) > 0.05 * want:
                    bad.append(f"{x.get('name', '?')} states {tq} Nm against {want:.4f} Nm "
                               "from KV and continuous current")
        ok &= report(not bad,
                     "week2: continuous torque follows from KV and continuous current",
                     "; ".join(bad[:3]) if bad else f"{len(drives)} candidates")
        chain = [num(data, "efficiency.transmission"), num(data, "efficiency.motor")]
        if len(sel) == 1 and "shaft_power_W" in r and all(chain):
            need = r["shaft_power_W"] / (chain[0] * chain[1])
            cp = sel[0].get("continuous_power_W")
            ok &= report(isinstance(cp, (int, float)) and not isinstance(cp, bool)
                         and cp >= need,
                         "week2: the selected drive covers the design point on its "
                         "continuous rating",
                         f"{need:.1f} W wanted at the motor terminals against a rated {cp} W")

    # The candidate comparison has to be won by the row the stated first metric picks,
    # and the winner's mass has to be the envelope the rest of the week is built on.
    cands = dotted(data, "configuration_candidates")
    if isinstance(cands, list) and cands:
        sel = [x for x in cands if isinstance(x, dict) and x.get("selected") is True]
        ok &= report(len(sel) == 1,
                     "week2: exactly one configuration candidate is selected",
                     f"{len(sel)} of {len(cands)} rows marked selected")
        tws = [x.get("module_tw_conservative") for x in cands if isinstance(x, dict)]
        good = bool(tws) and all(isinstance(v, (int, float)) and not isinstance(v, bool)
                                 and v > 0 for v in tws)
        ok &= report(good, "week2: every configuration candidate carries a conservative "
                           "thrust to weight", "" if good else f"{tws}")
        if good and len(sel) == 1:
            ok &= report(sel[0].get("module_tw_conservative") >= max(tws) - 1e-9,
                         "week2: the selected candidate wins on conservative thrust to weight",
                         f"selected {sel[0].get('module_tw_conservative')}, "
                         f"best on the table {max(tws)}")
        if len(sel) == 1:
            env_total, mm = num(data, "results.mass_envelope_g"), sel[0].get("module_mass_g")
            if env_total and isinstance(mm, (int, float)) and not isinstance(mm, bool):
                ok &= report(close(mm, env_total, DISPLAY_TOL),
                             "week2: the selected candidate mass is the envelope total",
                             f"candidate row says {mm} g, the envelope lines give {env_total} g")
    return ok


WEEK2_DOCS = [
    ("stage-1/design/01-configuration.md",
     ["Configuration", "Why this configuration", "Numbers used"]),
    ("stage-1/design/02-rotor-sizing.md",
     ["Rotor sizing", "Shape family", "Radius", "Numbers used"]),
    ("stage-1/design/04-thrust-and-power.md",
     ["Thrust", "Power", "Sensitivity", "Numbers used"]),
]

def week2(data):
    ok = True
    ok &= require_positive(data, [
        "geometry.radius_m", "geometry.chord_m", "geometry.span_m", "geometry.blades",
        "geometry.pitch_amplitude_deg", "geometry.pitch_axis_pct_chord",
        "operating.rpm", "operating.tip_speed_ms", "operating.reynolds",
        "performance.thrust_N", "performance.blade_area_coeff",
        "performance.blade_area_coeff_low", "performance.thrust_N_conservative",
        "performance.blade_deflection_thrust_loss",
        "performance.aero_power_W", "performance.electrical_power_W",
        "performance.tare_power_W", "performance.actuator_power_W",
        "performance.controller_power_W", "performance.module_electrical_power_W",
        "efficiency.transmission", "efficiency.motor", "efficiency.esc",
        "results.mass_g_conservative",
    ], "week2: numbers.json carries the week 2 schema as positive finite values")
    ok &= require_integer(data, ["geometry.blades"], "week2: blades come in whole units",
                          MIN_BLADES)
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
        bad, lighter = [], []
        for b in env:
            if not isinstance(b, dict):
                bad.append(repr(b)[:30]); continue
            vals = {}
            for f in ("nominal_g", "conservative_g"):
                v = b.get(f)
                if not isinstance(v, (int, float)) or isinstance(v, bool) or v <= 0:
                    bad.append(f"{b.get('item','?')}.{f}={v!r}")
                else:
                    vals[f] = float(v)
            if len(str(b.get("basis", "")).strip()) < MIN_BASIS_CHARS:
                bad.append(f"{b.get('item','?')} basis too thin")
            # D15: the drive is not a fixed mass, so every line says how it scales.
            if str(b.get("scaling_class")) not in SCALING_CLASSES:
                bad.append(f"{b.get('item','?')} scaling_class={b.get('scaling_class')!r}")
            if len(vals) == 2 and vals["conservative_g"] < vals["nominal_g"]:
                lighter.append(b.get("item", "?"))
        ok &= report(not lighter,
                     "week2: no envelope line is lighter in the conservative column",
                     ", ".join(lighter[:5]) if lighter else "")
        ok &= report(not bad, "week2: every envelope line has nominal, conservative and basis",
                     "; ".join(bad[:5]) if bad else "")
        items = [str(b.get("item", "")).strip().lower() for b in env if isinstance(b, dict)]
        names = " ".join(items)
        absent = [x for x in MODULE_COMPONENTS if x not in names]
        ok &= report(not absent, "week2: envelope covers every component in the module boundary",
                     "missing: " + ", ".join(absent) if absent else "")
        # Week 4's budget lines point back at these names, so two lines sharing one name
        # would merge two components into a single group nobody can tell apart.
        ok &= report(len(set(items)) == len(items) and "" not in items,
                     "week2: envelope line names are distinct and non-empty",
                     f"{len(items)} lines, {len(set(items))} distinct")

    for key, (_, _, w) in ROW_SPECS.items():
        if w == 2:
            ok &= require_rows(data, key, 2)
    ok &= require_headings("stage-1/design/evidence-ledger.md",
                           ["Evidence ledger", "Selection rules"])
    scen = dotted(data, "coefficient_scenarios")
    if isinstance(scen, list) and scen:
        bad = [str(s.get("evidence_class")) for s in scen if isinstance(s, dict)
               and str(s.get("evidence_class")) not in EVIDENCE_CLASSES]
        ok &= report(not bad,
                     "week2: every coefficient scenario is labelled measured, derived or downside",
                     "; ".join(bad[:4]) if bad else "")

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

    # Solidity decides whether the borrowed thrust coefficient is transferable at all.
    R_, c_, nb_ = num(data, "geometry.radius_m"), num(data, "geometry.chord_m"), num(data, "geometry.blades")
    if R_ and c_ and nb_:
        sigma = nb_ * c_ / (2 * math.pi * R_)
        ok &= report(SOLIDITY_MIN <= sigma <= SOLIDITY_MAX,
                     f"week2: solidity is inside the measured optimum band "
                     f"{SOLIDITY_MIN} to {SOLIDITY_MAX}",
                     f"sigma {sigma:.4f}, so the transferred coefficient needs re-deriving")

    cl, cn = num(data, "performance.blade_area_coeff_low"), num(data, "performance.blade_area_coeff")
    if cl and cn:
        # The 10 percent floor exists because a transferred coefficient carries an
        # unmeasured configuration change. A measurement on this design's own shape family
        # retires that part of the haircut and nothing else, so the floor drops to 5 and
        # the deflection allowance below still has to be answered. The match is deliberately
        # narrow: same solidity, same chord to radius, and a measured value that does not
        # undercut the nominal one. A measurement on a different rotor buys nothing.
        match = measured_shape_family(data, sigma if R_ and c_ and nb_ else None,
                                      c_ / R_ if R_ and c_ else None, cn)
        floor = MEASURED_COEFF_MAX_RATIO if match else CONSERVATIVE_COEFF_MAX_RATIO
        detail = f"low {cl} vs nominal {cn}, ratio {cl / cn:.3f}"
        if match:
            detail += f", floor {floor:.0%} because {match.get('name')} measured this family"
        ok &= report(cl <= cn * floor * (1 + TOL),
                     f"week2: the low coefficient is at most {floor:.0%} of nominal", detail)
        # Blade deflection is the one published mechanism for losing thrust against the
        # coefficient, and Benedict and Chopra put it as high as 40 percent. A haircut
        # picked for comfort is not a bound; the low value has to answer a stated loss.
        loss = num(data, "performance.blade_deflection_thrust_loss")
        if loss:
            ok &= report(loss < 1.0 and cl <= cn * (1 - loss) * (1 + TOL),
                         "week2: the low coefficient covers the stated blade deflection loss",
                         f"loss {loss:.0%} allows at most {cn * (1 - loss):.4f}, low is {cl}")
    ok &= require_text(data, ["sources.performance.blade_deflection_thrust_loss"],
                       "week2: the deflection loss cites the stiffness case behind it", 20)

    # Feasibility envelope: the conservative mass must still clear T/W at conservative thrust.
    mc, tc = num(data, "results.mass_g_conservative"), r.get("thrust_N_conservative")
    ok &= require_positive(data, ["results.mass_envelope_g"],
                           "week2: the nominal envelope total is stated")
    if "mass_envelope_total_g" in r:
        nom, cons = r["mass_envelope_total_g"], r["mass_envelope_conservative_g"]
        ok &= report(close(num(data, "results.mass_envelope_g"), nom),
                     "week2: stated envelope total matches the nominal lines",
                     f"lines give {nom:.1f} g")
        # The 5 percent rule applies to the recomputed column, not to a stated headline
        # that tolerance could absorb the difference from.
        ok &= report(cons >= nom * CONSERVATIVE_MASS_MIN_RATIO,
                     f"week2: conservative lines total at least {CONSERVATIVE_MASS_MIN_RATIO:.0%} of nominal",
                     f"{cons:.1f} g vs {nom:.1f} g, ratio {cons / nom:.3f}" if nom else "")
        if mc:
            refined = budget_conservative_total(data)
            want = cons if refined is None else refined
            basis = ("the conservative envelope lines" if refined is None
                     else "the refined budget lines")
            ok &= report(close(mc, want),
                         f"week2: conservative mass matches {basis}",
                         f"lines give {want:.1f} g, stated {mc:.1f} g")
    if mc and tc:
        tw = tc / (mc / 1000.0 * G)
        mn_tot, tn = num(data, "results.mass_envelope_g"), r.get("thrust_N")

        # Four T/W cases, not one. The design case and each downside taken on its own are
        # hard gates here. The stacked case, meaning the low coefficient and the high mass
        # column together, is stated here and gated hard in week 4 instead. The reason is
        # what the week 2 mass column is made of: eight of its thirteen lines carry a
        # blanket 20 or 25 percent growth rate, six of those on a basis that says the
        # section is assumed rather than weighed or quoted. Freezing or
        # refusing to freeze geometry on a number built that way tests the growth rates
        # rather than the design. Week 4 replaces those lines with real sections and
        # catalogue parts, and `week4: conservative T/W clears 2.5` already applies the
        # same limit to that refined budget. See D30.
        if mn_tot and tn:
            for label, thrust, mass in [
                    ("the design case", tn, mn_tot),
                    ("the mass downside alone", tn, mc),
                    ("the coefficient downside alone", tc, mn_tot)]:
                case_tw = thrust / (mass / 1000.0 * G)
                ok &= report(case_tw > TW_MINIMUM,
                             f"week2: {label} clears T/W 2.5",
                             f"T/W {case_tw:.3f} at {thrust:.2f} N and {mass:.0f} g")

        ok &= report(close(num(data, "results.thrust_to_weight_conservative"), tw),
                     "week2: the stacked downside T/W is stated and reproduces",
                     f"T/W {tw:.3f} at {tc:.2f} N and {mc:.0f} g")

        # D32. Week 2 spent most of its length reporting one thrust to weight when the
        # data held four, and the design case is the flattering one. Every week 2 document
        # has to carry the stacked figure, so a reader cannot meet 3.163 without meeting
        # 2.252 on the same page. Presence, not a conditional on the design number: which
        # numeric token in a document is a thrust to weight is not something a regex knows.
        for rel, _heads in WEEK2_DOCS:
            ok &= report(states_value(rel, tw),
                         f"week2: {rel} states the stacked conservative T/W",
                         f"T/W {tw:.3f}",
                         fail_detail=f"no number within {TOL:.1%} of {tw:.4f} in the "
                                     f"narrative. Either it states the design case alone, "
                                     f"or a later week moved the conservative mass and "
                                     f"this document still quotes the old figure. See D34")

        # A miss is allowed to pass week 2 only if it hands week 4 an arithmetic target
        # rather than a paragraph. The target is the conservative mass that would clear the
        # limit at this conservative thrust, and the gate recomputes it.
        if tw > TW_MINIMUM:
            report(True, "week2: the stacked downside clears T/W 2.5 as well",
                   f"T/W {tw:.3f} at {tc:.2f} N and {mc:.0f} g")
        else:
            target = tc / (TW_MINIMUM * G) * 1000.0
            stated = num(data, "results.mass_target_week4_g")
            ok &= report(stated is not None and close(stated, target),
                         "week2: a stacked downside miss hands week 4 a mass target",
                         f"target {target:.1f} g, {mc - target:.1f} g below the "
                         f"conservative {mc:.1f} g",
                         fail_detail=f"stacked T/W {tw:.3f} misses {TW_MINIMUM}, so "
                                     f"results.mass_target_week4_g has to be "
                                     f"{target:.1f} g, found {stated}")
            ok &= require_text(data, ["sources.results.mass_target_week4_g"],
                               "week2: the mass target says how the shortfall retires", 40)

        note("week2: planning mass ceiling at this thrust",
             f"{tc / (TW_MINIMUM * G) * 1000:.0f} g "
             f"({PLANNING_MASS_AT_10N_G:.0f} g would apply only at exactly 10 N)")

    # ---- the physical floor under the power estimate -----------------------------
    # Everything else in week 2 checks that stored arithmetic agrees with itself. This is
    # the only gate that asks whether the thrust and power pair could exist at all.
    ok &= require_positive(data, ["performance.momentum_area_m2", "performance.ideal_power_W",
                                  "performance.figure_of_merit",
                                  "performance.power_loading_ref_N_per_W",
                                  "performance.aero_power_W_published",
                                  "performance.power_spread"],
                           "week2: the power estimate carries a momentum bound and a second route")
    ok &= require_text(data, ["sources.performance.momentum_area_m2",
                              "sources.performance.power_loading_ref_N_per_W"],
                       "week2: the momentum closure and the published power loading cite a source", 20)
    if "ideal_power_W" in r:
        ok &= report(close(num(data, "performance.ideal_power_W"), r["ideal_power_W"]),
                     "week2: ideal power reproduces from thrust and the declared area",
                     f"computed {r['ideal_power_W']:.2f} W")
        if "momentum_area_max_m2" in r:
            ok &= report(num(data, "performance.momentum_area_m2")
                         <= r["momentum_area_max_m2"] * (1 + DISPLAY_TOL),
                         "week2: the momentum area is not inflated past the projected area",
                         f"declared {num(data, 'performance.momentum_area_m2'):.4f} m2, "
                         f"2R times span is {r['momentum_area_max_m2']:.4f} m2")
        ap_ = num(data, "performance.aero_power_W")
        ok &= report(ap_ is not None and ap_ >= r["ideal_power_W"],
                     "week2: aerodynamic power is at or above the momentum bound",
                     f"{ap_} W against an ideal {r['ideal_power_W']:.2f} W" if ap_ else "")
    if "figure_of_merit" in r:
        fm = r["figure_of_merit"]
        ok &= report(close(num(data, "performance.figure_of_merit"), fm),
                     "week2: figure of merit reproduces from ideal over actual power",
                     f"computed {fm:.3f}")
        ok &= report(FM_MIN <= fm <= FM_MAX,
                     f"week2: figure of merit is between {FM_MIN} and {FM_MAX}",
                     f"{fm:.3f}")
    if "aero_power_W_published" in r:
        ok &= report(close(num(data, "performance.aero_power_W_published"),
                           r["aero_power_W_published"]),
                     "week2: the published-power-loading route reproduces from thrust",
                     f"computed {r['aero_power_W_published']:.2f} W")
    if "power_spread" in r:
        ok &= report(close(num(data, "performance.power_spread"), r["power_spread"], DISPLAY_TOL),
                     "week2: the stated spread between the two power routes reproduces",
                     f"computed {r['power_spread']:.3f}")
        ok &= report(r["power_spread"] <= MAX_POWER_SPREAD,
                     f"week2: the two power routes agree within {MAX_POWER_SPREAD:.0%}",
                     f"spread {r['power_spread']:.1%}")

    # Thrust is a free variable, so the sensitivity of everything to it gets frozen here.
    # Week 4 may only pick a row from this table, never invent a new thrust under deadline.
    ok &= check_thrust_sensitivity(data, r)
    ok &= check_week2_selection(data, r)

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

        rows = sorted(((float(x["radius_m"]), float(x["aero_power_W"])) for x in sweep
                       if isinstance(x, dict)
                       and isinstance(x.get("radius_m"), (int, float))
                       and isinstance(x.get("aero_power_W"), (int, float))),
                      key=lambda t: t[0])
        if len(rows) >= 3:
            falling = all(b[1] < a[1] for a, b in zip(rows, rows[1:]))
            ok &= report(falling,
                         "week2: power falls as radius rises, as a fixed shape family requires",
                         "; ".join(f"{r_:.3f}m={p_:.1f}W" for r_, p_ in rows))
            pr = [r_ * p_ for r_, p_ in rows]
            spread = max(pr) / min(pr) if min(pr) else 999
            ok &= report(spread <= 1.5,
                         "week2: power times radius is roughly constant, so P scales near 1/R",
                         f"spread {spread:.2f}")
            chosen = num(data, "geometry.radius_m")
            if chosen:
                at_chosen = [p_ for r_, p_ in rows if abs(chosen - r_) <= 1e-6]
                ok &= report(bool(at_chosen), "week2: the chosen radius appears in the sweep",
                             f"{chosen} m, sweep {[r_ for r_, _ in rows]}",
                             fail_detail=f"{chosen} not among {[r_ for r_, _ in rows]}")
                # A sweep that is not anchored to the design point is a separate curve
                # that happens to have the right shape. It has to pass through the
                # aerodynamic power the rest of the week is built on.
                if at_chosen:
                    ok &= report(close(num(data, "performance.aero_power_W"), at_chosen[0]),
                                 "week2: the sweep row at the chosen radius is the design power",
                                 f"sweep {at_chosen[0]:.2f} W, "
                                 f"stored {dotted(data, 'performance.aero_power_W')}")

    for rel, heads in WEEK2_DOCS:
        ok &= require_headings(rel, heads)
        ok &= require_substance(rel)
        ok &= check_declared_numbers(rel, data)
    return ok


def check_pitch_motion(data, az, pitches):
    """A table that spans 360 degrees is not evidence of pitching. This one asks whether
    the mechanism actually moves: real extrema in both directions, the stated amplitude
    reached, the revolution closing, and the stated phase delay recoverable from the table
    rather than asserted next to it. Kinematics and vectoring carry 15 percent together."""
    amp = num(data, "geometry.pitch_amplitude_deg")
    phase = num(data, "pitch.phase_delay_deg")
    if not (pitches and amp and len(az) == len(pitches)):
        return True
    hi, lo = max(pitches), min(pitches)
    ok = report(hi >= amp * 0.9 and lo <= -amp * 0.9,
                "week3: the schedule reaches the stated amplitude in both directions",
                f"peak {hi:.1f} deg, trough {lo:.1f} deg against an amplitude of {amp} deg")
    ok &= report(abs((hi - lo) - 2 * amp) <= 0.15 * 2 * amp,
                 "week3: peak to peak travel matches twice the stated amplitude",
                 f"{hi - lo:.1f} deg against {2 * amp:.1f} deg")

    # Periodic closure, only when the table actually carries both ends.
    ends = {round(a) % 360: p for a, p in zip(az, pitches)}
    first = [p for a, p in zip(az, pitches) if abs(a - min(az)) < 1e-6]
    last = [p for a, p in zip(az, pitches) if abs(a - max(az)) < 1e-6]
    if max(az) - min(az) >= 360 - 1e-6 and first and last:
        ok &= report(abs(first[0] - last[0]) <= 0.02 * amp,
                     "week3: the schedule closes on itself over a revolution",
                     f"{first[0]:.2f} deg at {min(az):.0f} against {last[0]:.2f} deg "
                     f"at {max(az):.0f}")

    # The phase delay is where the side force comes from, so it has to be in the table.
    if phase is not None:
        peak_az = az[pitches.index(hi)]
        implied = (peak_az - 90.0) % 360.0
        if implied > 180:
            implied -= 360.0
        gap = abs(implied - phase)
        ok &= report(gap <= 10.0,
                     "week3: the stated phase delay is the one the schedule shows",
                     f"peak at {peak_az:.0f} deg implies {implied:.1f} deg, "
                     f"pitch.phase_delay_deg says {phase}")

        # Residual against the harmonic the four-bar is meant to approximate. A real
        # linkage is not a pure cosine, so the cap is loose; a flat table is not.
        stated = num(data, "pitch.schedule_rms_residual_deg")
        model = [amp * math.cos(math.radians(a - 90.0 - phase)) for a in az]
        rms = math.sqrt(sum((p - m) ** 2 for p, m in zip(pitches, model)) / len(pitches))
        if stated is not None:
            ok &= report(close(stated, rms, DISPLAY_TOL) or abs(stated - rms) <= 0.05,
                         "week3: the stated fit residual reproduces from the table",
                         f"computed {rms:.3f} deg, stated {stated}")
        ok &= report(rms <= 0.25 * amp,
                     "week3: the schedule tracks the harmonic model it claims to follow",
                     f"rms residual {rms:.2f} deg against an amplitude of {amp} deg")

    # Vectoring follows from how far the offset direction can be driven, one to one.
    # It used to be a number asserted beside the mechanism with nothing tying them.
    auth, rng = num(data, "pitch.phase_authority_deg"), num(data, "pitch.vector_range_deg")
    if auth and rng:
        ok &= report(close(rng, auth, DISPLAY_TOL),
                     "week3: the vectoring range is the phase authority of the mechanism",
                     f"range {rng} deg against an authority of {auth} deg")
    return ok


def check_vector_map(data):
    """Does the force table support the vectoring claim, or only sit next to it?

    A design can pass the scalar comparison with three commands clustered at zero and a
    360 degree claim beside them, or with a table whose lateral column never moves. Both
    are answered here, and neither costs an honest design anything.
    """
    rows = [r for r in (dotted(data, "vector_map") or []) if isinstance(r, dict)]
    rng, auth = num(data, "pitch.vector_range_deg"), num(data, "pitch.phase_authority_deg")
    if not (rows and rng and auth):
        return True
    pts = []
    for r in rows:
        cmd, v, lat = (snum(r, "phase_command_deg"), snum(r, "vertical_force_N"),
                       snum(r, "lateral_force_N"))
        if cmd is None or v is None or lat is None:
            return True                  # require_rows already reported the row shape
        pts.append((cmd, v, lat))
    pts.sort()

    half = auth / 2.0
    outside = [f"{c:.0f}" for c, _, _ in pts if abs(c) > half * (1 + DISPLAY_TOL)]
    ok = report(not outside,
                "week3: every mapped phase command sits inside the mechanism's authority",
                f"{len(pts)} commands inside plus or minus {half:.0f} deg",
                fail_detail=f"outside plus or minus {half:.0f} deg: " + ", ".join(outside[:5]))

    span = pts[-1][0] - pts[0][0]
    ok &= report(span >= VECTOR_EVIDENCE_FRACTION * rng,
                 "week3: the force map covers enough of the claimed range to evidence it",
                 f"commands span {span:.0f} deg against a claimed {rng:.0f} deg")

    dead = [f"{c:.0f}" for c, v, lat in pts if math.hypot(v, lat) <= 0]
    if not report(not dead, "week3: every mapped command produces a force",
                  f"{len(pts)} commands carry force",
                  fail_detail="no force at commands " + ", ".join(dead[:5])):
        return False

    dirs = [math.degrees(math.atan2(lat, v)) for _, v, lat in pts]
    bad = []
    for (c0, _, _), (c1, _, _), d0, d1 in zip(pts, pts[1:], dirs, dirs[1:]):
        turn = (d1 - d0 + 180.0) % 360.0 - 180.0
        if abs(turn - (c1 - c0)) > VECTOR_TRACKING_TOL_DEG:
            bad.append(f"{c0:.0f} to {c1:.0f} deg of command turned the force {turn:.1f} deg")
    return ok & report(not bad, "week3: the force direction turns with the phase command",
                       "; ".join(bad[:3]) if bad else f"{len(pts)} commands tracked")


def check_lateral_loads(data):
    """Week 3 reruns the azimuthal model against the solved schedule, and that is where the
    side force stops being zero by construction. Once the table carries a lateral column,
    the stated peak has to come out of it and the cycle mean has to be the trimmed one the
    design claims. A week 2 table without the column is left alone."""
    rows = [r for r in (dotted(data, "aero_azimuthal_loads") or []) if isinstance(r, dict)]
    lat = [snum(r, "lateral_force_N") for r in rows]
    vert = [snum(r, "normal_force_N") for r in rows]
    if not rows or any(v is None for v in lat) or any(v is None for v in vert):
        return True
    mean_lat, mean_v = sum(lat) / len(lat), sum(vert) / len(vert)
    ok = report(abs(mean_lat) <= LATERAL_TRIM_FRACTION * abs(mean_v),
                "week3: the cycle mean lateral force is trimmed out",
                f"mean lateral {mean_lat:.4f} N against a mean vertical {mean_v:.4f} N")
    stated = snum(data, "pitch.peak_lateral_force_N")
    if stated is not None:
        peak = max(abs(v) for v in lat)
        ok &= report(close(stated, peak, DISPLAY_TOL),
                     "week3: the stated peak lateral force reproduces from the table",
                     f"the table gives {peak:.4f} N, stated {stated}")
    return ok


def week3(data):
    ok = True
    ok &= require_positive(data, [
        "pitch.offset_m", "pitch.phase_delay_deg", "pitch.vector_range_deg",
        "pitch.actuator_count", "pitch.actuator_mass_g", "pitch.side_force_tilt_deg",
        "pitch.peak_lateral_force_N",
        "packaging.envelope_length_mm", "packaging.envelope_width_mm",
        "packaging.envelope_height_mm", "packaging.mount_points",
        "pitch.phase_authority_deg", "pitch.schedule_rms_residual_deg",
    ], "week3: numbers.json carries the pitch and packaging schema")
    for key, (_, _, w) in ROW_SPECS.items():
        if w == 3:
            ok &= require_rows(data, key, 3)
    ok &= require_integer(data, ["pitch.actuator_count"], "week3: actuators come in whole units")
    ok &= require_integer(data, ["packaging.mount_points"],
                          "week3: mount points come in whole units", MIN_MOUNT_POINTS)
    ok &= require_text(data, ["pitch.mechanism"], "week3: pitch mechanism is named", 6)
    ok &= check_vector_map(data)
    ok &= check_lateral_loads(data)

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
        ok &= check_pitch_motion(data, az, pitches)

    rel = "stage-1/design/09-packaging-and-integration.md"
    ok &= require_headings(rel, ["Package envelope", "Mounting", "Drivetrain",
                                 "Interfaces", "Numbers used"])
    ok &= require_substance(rel, 300)
    ok &= check_declared_numbers(rel, data)
    return ok


def budget_conservative_total(data):
    """The refined week 4 budget's conservative column, or None while it does not exist.

    Week 2's conservative module mass comes from the envelope, because the envelope is the
    only component list it has. The moment week 4 refines the budget line by line, the same
    scalar comes from there instead, which is what D31 and D34 both say happens: D31 expects
    the assumed growth rates to retire against real sections, and D34 warns the week 2
    documents that the stacked figure will move under them when they do.

    Binding `results.mass_g_conservative` to the envelope for ever pinned the refined column
    to the estimate it exists to replace, to half a percent. Nothing is unbound by moving it:
    whichever column is live, the scalar has to equal a sum of per-line figures, and the week
    4 gates apply the stricter set of rules to the budget. An incomplete column returns None
    so the week 4 shape gates report it rather than this one falling over."""
    rows = dotted(data, "mass_budget_g")
    if not (isinstance(rows, list) and len(rows) >= MIN_BUDGET_LINES):
        return None
    vals = [num(r, "conservative_g") for r in rows if isinstance(r, dict)]
    if len(vals) != len(rows) or any(v is None for v in vals):
        return None
    return sum(vals)


def check_conservative_budget(data, budget_total):
    """The hard stacked thrust to weight test lives in week 4, on the refined budget. It
    reads `results.mass_g_conservative`, so while that stays one stored scalar the test can
    be passed by choosing a growth rate rather than by refining a mass, which is the exact
    move the blocked trigger forbids and the reason D30 gave for moving the test here.

    So the conservative column is built the way the nominal one is. Every budget line
    carries its own conservative figure, no line gets lighter under growth, the stated
    total is their sum, and the aggregate growth is at least what week 2 required of the
    envelope. See D33."""
    budget = dotted(data, "mass_budget_g")
    if not (isinstance(budget, list) and budget):
        return True                     # the shape gates above already reported this
    rows = [b for b in budget if isinstance(b, dict)]
    missing = [str(b.get("item", "?")) for b in rows if num(b, "conservative_g") is None]
    if not report(not missing, "week4: every budget line carries a conservative figure",
                  "; ".join(missing[:5]) if missing else f"{len(rows)} lines"):
        return False

    shrunk = [f"{b.get('item', '?')}: {b['conservative_g']} g against {b.get('mass_g')} g"
              for b in rows
              if num(b, "mass_g") is not None
              and float(b["conservative_g"]) < float(b["mass_g"]) * (1 - TOL)]
    ok = report(not shrunk, "week4: no budget line is lighter in the conservative column",
                "; ".join(shrunk[:4]) if shrunk else "")

    total = sum(float(b["conservative_g"]) for b in rows)
    stated = num(data, "results.mass_g_conservative")
    ok &= report(close(stated, total),
                 "week4: the conservative mass is the sum of the budget lines",
                 f"lines give {total:.1f} g",
                 fail_detail=f"lines give {total:.1f} g, results.mass_g_conservative says "
                             f"{stated}, so the conservative column was chosen rather "
                             f"than built")
    if budget_total:
        ok &= report(total >= budget_total * CONSERVATIVE_MASS_MIN_RATIO,
                     f"week4: the conservative budget is at least "
                     f"{CONSERVATIVE_MASS_MIN_RATIO:.0%} of nominal",
                     f"{total:.1f} g vs {budget_total:.1f} g, "
                     f"ratio {total / budget_total:.3f}")

    # The refined column is allowed to move off the week 2 envelope's, which is the whole
    # point of refining it, but not to walk away from it. The nominal columns are already
    # held to this band per component and in total, and leaving the conservative one free
    # would let a week 4 budget claim a module its own estimate never described.
    env_cons = None
    env = dotted(data, "mass_envelope_g")
    if isinstance(env, list) and env:
        vals = [num(e, "conservative_g") for e in env if isinstance(e, dict)]
        if vals and all(v is not None for v in vals):
            env_cons = sum(vals)
    if env_cons:
        drift = abs(total - env_cons) / env_cons
        ok &= report(drift <= GROUP_DRIFT_MAX,
                     f"week4: the conservative budget is within {GROUP_DRIFT_MAX:.0%} of "
                     f"the week 2 conservative envelope",
                     f"budget {total:.1f} g vs envelope {env_cons:.1f} g, drift {drift:.1%}")
    return ok


def check_budget_continuity(data):
    """Week 4 refines week 2's envelope. Comparing only the totals let the whole budget
    move into the blades while every other component collapsed to the minimum legal line,
    because the sum was preserved. Each budget line therefore names the envelope line it
    refines, and each envelope line has to survive the refinement.

    The mapping is declared rather than guessed. Matching on words fails honestly: an
    envelope line called "motor and drive" is refined by a hub, a shaft, bearings and a
    motor, and no keyword rule gets that right without inventing failures."""
    env, budget = dotted(data, "mass_envelope_g"), dotted(data, "mass_budget_g")
    if not (isinstance(env, list) and env and isinstance(budget, list) and budget):
        return True                     # the shape gates above already reported this

    groups = {}
    for e in env:
        if isinstance(e, dict) and isinstance(e.get("nominal_g"), (int, float)):
            groups[str(e.get("item", "")).strip().lower()] = [float(e["nominal_g"]), 0.0]

    ok, orphan = True, []
    for b in budget:
        if not isinstance(b, dict):
            continue
        key = str(b.get("refines", "")).strip().lower()
        mass = b.get("mass_g")
        if key not in groups:
            orphan.append(f"{b.get('item', '?')} refines {b.get('refines')!r}")
        elif isinstance(mass, (int, float)) and not isinstance(mass, bool):
            groups[key][1] += float(mass)
    ok &= report(not orphan,
                 "week4: every mass line names the envelope line it refines",
                 "; ".join(orphan[:5]) if orphan else "")

    empty = [k for k, (_, got) in groups.items() if got <= 0]
    ok &= report(not empty, "week4: no envelope line vanishes from the refined budget",
                 "nothing refines: " + ", ".join(empty[:5]) if empty else "")

    drifted = [f"{k}: envelope {want:.1f} g, budget {got:.1f} g "
               f"({abs(got - want) / want:.0%})"
               for k, (want, got) in sorted(groups.items())
               if want > 0 and got > 0 and abs(got - want) / want > GROUP_DRIFT_MAX]
    ok &= report(not drifted,
                 f"week4: each component stays within {GROUP_DRIFT_MAX:.0%} of its envelope line",
                 "; ".join(drifted[:4]) if drifted else "")
    return ok


def check_solver_order(data):
    """The two solvers have a run order and this is what enforces it.

    tools/linkage.py imports the blade build-up from tools/structure.py, and structure.py
    reads the pitch link load that linkage.py solved. So linkage.py goes first. The order
    was resolved by hand, written into two docstrings, and checked nowhere, which week 4
    carried as an open item.

    Running them the wrong way round leaves a fingerprint. structure.py picks up the pitch
    link load from before the blade moved, writes it into structure.pitch_link_load_N, and
    then linkage.py overwrites pitch.peak_link_force_N with the new one. The two disagree,
    and they cannot disagree in a file written in the right order because the second script
    copies the first one across. Perturb the chord by two millimetres and the reverse order
    leaves 105.93 N beside 111.3 N.

    From a converged file both orders reproduce it byte for byte, since each script is at
    its own fixed point, so a reproducibility check alone would say the order does not
    matter. It matters the moment anything moves."""
    link = num(data, "structure.pitch_link_load_N")
    peak = num(data, "pitch.peak_link_force_N")
    if link is None or peak is None:
        return report(False, "week4: the pitch link load crosses between the two solvers",
                      "structure.pitch_link_load_N or pitch.peak_link_force_N is missing")
    return report(close(link, peak, DISPLAY_TOL),
                  "week4: the solvers ran in the documented order",
                  f"structure has {link} N against the {peak} N linkage solved. "
                  "Run tools/linkage.py --write first, then tools/structure.py --write"
                  if not close(link, peak, DISPLAY_TOL) else f"{link} N on both sides")


MOTOR_SPEED_RULE_MAX = 0.90


def check_drive_margin(data):
    """What the 0.80 continuous derate costs, gated rather than argued.

    The derate has no source. It cannot be given one from inside the project, so the thing
    to hold instead is the consequence, and there are four parts to that.

    One derate for every candidate. A shortlist where the winner is derated at 0.80 and the
    losers at 0.70 is a rigged comparison, and nothing stopped it before.

    The fraction of the published 180 second current the design draws is the derate at
    which the selection breaks even. It is gated against the datasheet figure so it cannot
    drift, and it is the number that says how much of the risk is real.

    The design point cannot be lowered to relieve the drive. The stacked thrust to weight
    case needs thrust_floor_stacked_N, no lower row of the sensitivity table clears it, and
    the floor is recomputed here from the conservative mass rather than read.

    Speed is the fourth piece and it is older. The 90 percent rule week 2 screened belt
    ratios with, the one that emptied the 100 mm radius row, was written into prose and
    checked nowhere until now."""
    ok = True
    drives = dotted(data, "drive_candidates")
    derate = num(data, "performance.motor_derate")
    if not isinstance(drives, list) or not drives or derate is None:
        return report(False, "week4: the drive derate and the candidate list are stated",
                      "performance.motor_derate or drive_candidates is missing")
    bad = []
    for x in drives:
        if not isinstance(x, dict):
            continue
        name = x.get("name", "?")
        for peak, cont, unit in [("max_power_180s_W", "continuous_power_W", "W"),
                                 ("peak_current_180s_A", "continuous_current_A", "A")]:
            pv, cv = x.get(peak), x.get(cont)
            if not all(isinstance(v, (int, float)) and not isinstance(v, bool) and v > 0
                       for v in (pv, cv)):
                bad.append(f"{name} has no {peak} and {cont}")
            elif not close(cv, pv * derate, DISPLAY_TOL):
                bad.append(f"{name}: {cv} {unit} against {pv * derate:.3f} {unit} "
                           f"at the declared derate")
    ok &= report(not bad, "week4: every candidate is derated by the one declared factor",
                 "; ".join(bad[:3]) if bad else f"{len(drives)} candidates at {derate}")

    sel = [x for x in drives if isinstance(x, dict) and x.get("selected") is True]
    if len(sel) == 1:
        d = sel[0]
        amps = num(data, "performance.motor_input_current_A")
        watts = num(data, "performance.motor_input_W")
        cf = num(data, "performance.motor_current_frac_180s")
        pf = num(data, "performance.motor_power_frac_180s")
        peak_a, peak_w = d.get("peak_current_180s_A"), d.get("max_power_180s_W")
        if None not in (amps, watts, cf, pf) and peak_a and peak_w:
            ok &= report(close(cf, amps / peak_a, DISPLAY_TOL),
                         "week4: the current fraction of the 180 second peak reproduces",
                         f"{amps} A of {peak_a} A gives {amps / peak_a:.4f}, stated {cf}")
            ok &= report(close(pf, watts / peak_w, DISPLAY_TOL),
                         "week4: the power fraction of the 180 second maximum reproduces",
                         f"{watts} W of {peak_w} W gives {watts / peak_w:.4f}, stated {pf}")
            # The break even derate IS the current fraction. Once the declared derate falls
            # under it the selection no longer covers the design point.
            ok &= report(derate >= cf,
                         "week4: the declared derate still covers the design point",
                         f"derate {derate} against a break even of {cf:.4f}, "
                         f"{(derate - cf) * 100:.2f} points of room")

        # Speed. KV times the pack voltage after the resistive drop, and the design has to
        # sit under the declared fraction of it.
        v_nom = num(data, "performance.pack_voltage_nominal_V")
        v_load = num(data, "performance.pack_voltage_loaded_V")
        ceil = num(data, "performance.motor_speed_ceiling_rpm")
        rule = num(data, "performance.motor_speed_rule")
        frac = num(data, "performance.motor_rpm_frac_ceiling")
        rpm = num(data, "performance.motor_rpm")
        res, kv = d.get("internal_resistance_ohm"), d.get("kv")
        if None not in (v_nom, v_load, ceil, rule, frac, rpm, amps) and res and kv:
            ok &= report(close(v_load, v_nom - amps * res, DISPLAY_TOL),
                         "week4: the loaded pack voltage reproduces from the resistive drop",
                         f"{v_nom} V less {amps * res:.4f} V gives {v_nom - amps * res:.4f} V")
            ok &= report(close(ceil, kv * v_load, DISPLAY_TOL),
                         "week4: the motor speed ceiling reproduces from KV and that voltage",
                         f"computed {kv * v_load:.1f} rpm, stated {ceil}")
            ok &= report(close(frac, rpm / ceil, DISPLAY_TOL),
                         "week4: the speed fraction reproduces",
                         f"{rpm} of {ceil} rpm gives {rpm / ceil:.4f}, stated {frac}")
            ok &= report(rule <= MOTOR_SPEED_RULE_MAX,
                         "week4: the motor speed rule is no looser than "
                         f"{MOTOR_SPEED_RULE_MAX}", f"declared {rule}")
            ok &= report(frac < rule, "week4: the design sits under the motor speed rule",
                         f"{frac:.4f} against {rule}")

    # The thrust floor. This is the gate that stops the design point being lowered to give
    # the drive room, which is the cheapest way out of everything above and would take the
    # stacked thrust to weight case with it.
    floor = num(data, "performance.thrust_floor_stacked_N")
    thrust = num(data, "performance.thrust_N")
    lo = num(data, "performance.blade_area_coeff_low")
    nom = num(data, "performance.blade_area_coeff")
    mc = num(data, "results.mass_g_conservative")
    if None not in (floor, thrust, lo, nom, mc):
        want = TW_MINIMUM * (mc / 1000.0) * G / (lo / nom)
        ok &= report(close(floor, want, DISPLAY_TOL),
                     "week4: the stacked thrust floor reproduces from the conservative mass",
                     f"computed {want:.4f} N, stated {floor}")
        ok &= report(thrust >= floor,
                     "week4: the design thrust clears the stacked thrust floor",
                     f"{thrust} N against {floor} N")
        rows = dotted(data, "thrust_sensitivity")
        if isinstance(rows, list):
            below = [r.get("thrust_N") for r in rows
                     if isinstance(r, dict)
                     and isinstance(r.get("thrust_N"), (int, float))
                     and r["thrust_N"] < thrust]
            clear = [t for t in below if t >= floor]
            report(True, "week4: no lower sensitivity row clears the stacked floor"
                   if not clear else "week4: a lower sensitivity row would also clear",
                   f"{len(below)} row(s) below the design point, {len(clear)} of them clear")
    return ok


PITCH_BEARING_S0_FLOOR = 2.0
BEARING_FRICTION_MAX_FRAC = 0.01


def check_pitch_bearing_duty(data):
    """The tightest margin in the module is a bearing static rating, and a static rating is
    the wrong yardstick for a bearing that swings instead of turning.

    Every number here is recomputed from catalogue geometry and the frozen pitch travel, so
    the regime cannot be asserted in prose and left there. The gate with teeth is the last
    one: a bearing whose cage swing falls short of the ball spacing never rolls onto fresh
    raceway, and once that is true the static safety factor at the OPERATING load has to
    clear 2.0 rather than the 1.5 the strength cases carry. The floor itself is gated too,
    because a floor a later week can lower is not a floor."""
    ok = True
    g = lambda k: num(data, "structure." + k)
    balls, ball_mm, pd = g("pitch_bearing_balls"), g("pitch_bearing_ball_mm"),         g("pitch_bearing_pitch_diameter_mm")
    swing, spacing = g("pitch_bearing_cage_swing_deg"), g("pitch_bearing_ball_spacing_deg")
    ratio, crit = g("pitch_bearing_recirculation_ratio"), g("pitch_bearing_recirculation_travel_deg")
    travel = num(data, "pitch.pitch_bearing_travel_deg")
    if None in (balls, ball_mm, pd, swing, spacing, ratio, crit, travel):
        return report(False, "week4: the pitch bearing oscillating duty is stated",
                      "structure is missing one of the pitch_bearing_ fields")

    cage_ratio = (1.0 - ball_mm / pd) / 2.0
    ok &= report(close(swing, cage_ratio * travel, DISPLAY_TOL),
                 "week4: the cage swing follows from the ball geometry and the pitch travel",
                 f"computed {cage_ratio * travel:.4f} deg, stated {swing}")
    ok &= report(close(spacing, 360.0 / balls, DISPLAY_TOL),
                 "week4: the ball spacing follows from the ball count",
                 f"computed {360.0 / balls:.4f} deg over {balls:.0f} balls")
    # Ball count is the one soft input, and inflating it is the cheap way to claim the
    # bearing recirculates. The balls have to fit around the pitch circle, so the claim
    # is bounded by geometry rather than taken on trust.
    ok &= report(balls * ball_mm <= math.pi * pd,
                 "week4: the ball complement fits around the pitch circle",
                 f"{balls:.0f} balls of {ball_mm} mm need {balls * ball_mm:.2f} mm "
                 f"of a {math.pi * pd:.2f} mm pitch circle")
    ok &= report(close(ratio, swing / spacing, DISPLAY_TOL),
                 "week4: the recirculation ratio is cage swing over ball spacing",
                 f"computed {swing / spacing:.4f}, stated {ratio}")
    ok &= report(close(crit, spacing / cage_ratio, DISPLAY_TOL),
                 "week4: the travel that would give full recirculation is stated",
                 f"{crit:.1f} deg against {travel:.1f} deg of mechanism travel")

    # Load per bearing, and the static safety factor built on it. Both are derived from
    # numbers the rest of week 4 already gates, so a bearing swap cannot move one alone.
    fc, allow = g("centrifugal_load_N"), g("blade_attachment_allowable_N")
    load, s0 = g("pitch_bearing_load_N"), g("pitch_bearing_static_safety")
    if None not in (fc, allow, load, s0):
        ok &= report(close(load, fc / 2.0, DISPLAY_TOL),
                     "week4: the pitch bearing load is half the centrifugal pull",
                     f"computed {fc / 2.0:.4f} N per bearing, two per blade")
        ok &= report(close(s0, allow / 2.0 / load, DISPLAY_TOL),
                     "week4: the static safety factor reproduces from the rating and the load",
                     f"computed {allow / 2.0 / load:.4f}, stated {s0}")

    floor = g("pitch_bearing_static_safety_floor")
    ok &= report(floor is not None and floor >= PITCH_BEARING_S0_FLOOR,
                 "week4: the oscillating static safety floor is at least 2.0",
                 f"declared {floor}" if floor is not None else "not declared")
    if ratio < 1.0 and floor is not None and s0 is not None:
        ok &= report(s0 >= floor,
                     "week4: a bearing that never recirculates clears the oscillating floor",
                     f"{s0:.4f} against {floor}, ratio {ratio:.4f} of full recirculation")
    else:
        report(True, "week4: the pitch bearing recirculates, so the strength floor governs",
               f"ratio {ratio:.4f}")

    # Friction stays out of the power budget only while it is small enough to round away.
    # If a bearing change pushes it past a percent of shaft power it becomes a budget line.
    fw, pw = g("pitch_bearing_friction_W"), num(data, "performance.aero_power_W")
    tare = num(data, "performance.tare_power_W")
    if None not in (fw, pw, tare):
        frac = fw / (pw + tare)
        ok &= report(frac < BEARING_FRICTION_MAX_FRAC,
                     "week4: pitch bearing friction is small enough to leave out of the budget",
                     f"{fw:.4f} W, {frac * 100:.3f} percent of {pw + tare:.2f} W of shaft power")
    alt = g("pitch_bearing_plain_alternative_W")
    ok &= report(alt is not None and fw is not None and alt > fw,
                 "week4: the plain bearing fallback is costed against the ball bearing",
                 f"{alt} W against {fw} W" if alt is not None else "not costed")
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

    env_nom = num(data, "results.mass_envelope_g")
    if env_nom and "total_mass_g" in r:
        drift = abs(r["total_mass_g"] - env_nom) / env_nom
        ok &= report(drift <= GROUP_DRIFT_MAX,
                     f"week4: the refined budget is within {GROUP_DRIFT_MAX:.0%} of the week 2 envelope",
                     f"budget {r['total_mass_g']:.1f} g vs envelope {env_nom:.1f} g, "
                     f"drift {drift:.1%}")
    ok &= check_budget_continuity(data)

    mc = num(data, "results.mass_g_conservative")
    if mc and "total_mass_g" in r:
        ok &= report(mc >= r["total_mass_g"],
                     "week4: the conservative mass is not lighter than the budget",
                     f"conservative {mc:.1f} g vs budget {r['total_mass_g']:.1f} g")
        ok &= check_conservative_budget(data, r["total_mass_g"])

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
        "structure.transmission_ratio", "structure.blade_load_lever_m",
        "structure.blade_load_factor", "structure.pitch_link_load_N",
        "structure.pitch_link_allowable_N", "structure.pitch_link_margin",
        "structure.blade_attachment_allowable_N", "structure.blade_attachment_margin",
        "structure.blade_centrifugal_bending_Nm", "structure.blade_combined_margin",
        "structure.overspeed_factor", "structure.centrifugal_load_overspeed_N",
        "structure.blade_attachment_margin_overspeed",
        "structure.blade_combined_margin_overspeed",
    ], "week4: numbers.json carries the structural schema")
    ov = num(data, "structure.overspeed_factor")
    if ov:
        ok &= report(ov >= MIN_OVERSPEED,
                     f"week4: the declared overspeed is at least {MIN_OVERSPEED}",
                     f"{ov}, and centrifugal load goes as the square of it")
    lf_ = num(data, "structure.blade_load_factor")
    if lf_:
        ok &= report(lf_ >= MIN_BLADE_LOAD_FACTOR,
                     f"week4: the blade load factor is at least {MIN_BLADE_LOAD_FACTOR}",
                     f"{lf_}, against a measured peak to mean of 3 to 4 on 3 bladed rotors")
    ok &= require_text(data, ["structure.torque_reference",
                              "sources.structure.blade_root_bending_Nm",
                              "sources.structure.shaft_torque_Nm",
                              "sources.structure.pitch_link_load_N"],
                       "week4: every structural demand names the calculation behind it", 20)

    # Demands are derived from the design, not asserted next to it. A 1 g blade used to sit
    # happily beside a 108 g blade budget because nothing connected the two.
    for stated, computed, label in [
        ("structure.blade_mass_kg", "blade_mass_kg_derived",
         "per-blade mass follows from the blade budget and the blade count"),
        ("structure.shaft_torque_Nm", "shaft_torque_Nm_derived",
         "rotor shaft torque follows from shaft power and rotor speed"),
        ("structure.blade_root_bending_Nm", "blade_root_bending_Nm_derived",
         "blade root bending follows from thrust per blade, lever arm and load factor"),
        ("structure.blade_centrifugal_bending_Nm", "blade_centrifugal_bending_Nm_derived",
         "blade centrifugal bending follows from the centrifugal load and the same lever"),
        ("structure.centrifugal_load_overspeed_N", "centrifugal_load_overspeed_N_derived",
         "the overspeed centrifugal load follows from the declared overspeed squared"),
    ]:
        if computed in r:
            ok &= report(close(num(data, stated), r[computed], DISPLAY_TOL),
                         f"week4: {label}",
                         f"computed {r[computed]:.4g}, stated {dotted(data, stated)}")

    # Margins are derived from allowable over demand, never asserted.
    for tag in ("blade_margin", "shaft_margin", "pitch_link_margin",
                "blade_attachment_margin", "blade_combined_margin",
                "blade_combined_margin_overspeed", "blade_attachment_margin_overspeed"):
        v, computed = num(data, f"structure.{tag}"), r.get(tag)
        if computed is not None:
            ok &= report(close(v, computed),
                         f"week4: {tag} reproduces from allowable over demand",
                         f"computed {computed:.3f}, stated {v}")
            ok &= report(computed >= MIN_MARGIN,
                         f"week4: {tag} is at least {MIN_MARGIN}", f"{computed:.3f}")

    # The shaft's combined bending and torsion margin is the one margin the design states
    # that this file cannot recompute, because it needs the shaft section properties and
    # those live in tools/structure.py rather than in numbers.json. The floor still
    # applies. Stating a margin the gate had nothing at all to say about is how an
    # eight-row margin table ends up with seven gated rows and one decorative one.
    sc = num(data, "structure.shaft_combined_margin")
    if sc is not None:
        ok &= report(sc >= MIN_MARGIN,
                     f"week4: shaft_combined_margin is at least {MIN_MARGIN}",
                     f"{sc:.3f}, floored but not recomputed here")

    # Centrifugal load is the one structural number checkable from first principles.
    R, rpm = num(data, "geometry.radius_m"), num(data, "operating.rpm")
    mb = num(data, "structure.blade_mass_kg")
    if None not in (R, rpm, mb):
        fc = mb * (rpm * 2 * math.pi / 60) ** 2 * R
        ok &= report(close(num(data, "structure.centrifugal_load_N"), fc, DISPLAY_TOL),
                     "week4: centrifugal load reproduces from blade mass, speed and radius",
                     f"computed {fc:.1f} N")

    ok &= check_pitch_bearing_duty(data)
    ok &= check_drive_margin(data)
    ok &= check_solver_order(data)

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
    # Every other design document carries a substance floor and a declaration check. Item 7
    # had only its headings, so three heading lines and nothing under them passed week 5.
    ok &= require_substance("stage-1/design/07-team-and-execution.md")
    ok &= check_declared_numbers("stage-1/design/07-team-and-execution.md", data)

    sub = ROOT / "stage-1" / "submission" / "cycloprop-stage1.md"
    if not report(sub.is_file(), "week5: submission source exists"):
        return False
    text = sub.read_text(encoding="utf-8")

    heads = [h.lower() for h in HEADING.findall(text)]
    missing = [it for it in REQUIRED_ITEMS if not any(it.lower() in h for h in heads)]
    ok &= report(not missing, "week5: all 7 required items are top-level sections",
                 "missing: " + "; ".join(missing) if missing else "")

    block = section_under(text, "criteri")
    if block is None:
        ok &= report(False, "week5: the submission has a criteria map section")
    else:
        # Count data rows, not lines. The separator row is not a criterion and neither
        # is the header, so a table of 8 criteria is 10 lines. A real markdown table has
        # that separator, and the criteria have to be IN the rows: reading the whole
        # section let eight junk rows pass beside a sentence that named the eight criteria.
        pipes = [l.strip() for l in block if l.strip().startswith("|")]
        sep = [l for l in pipes if set(l) <= set("|- :") and "-" in l]
        ok &= report(bool(sep), "week5: the criteria map is a real markdown table",
                     fail_detail="no header separator row")
        rows = [l for l in pipes if l not in sep]
        data_rows = rows[1:] if sep else []
        ok &= report(len(data_rows) >= len(CRITERIA_KEYS),
                     f"week5: the criteria map is a table of {len(CRITERIA_KEYS)} criteria",
                     f"{len(data_rows)} data rows under the header")
        low = " ".join(data_rows).lower()
        absent = [k for k in CRITERIA_KEYS if k.lower() not in low]
        ok &= report(not absent, f"week5: the criteria map covers all {len(CRITERIA_KEYS)} criteria",
                     "missing from the table rows: " + ", ".join(absent) if absent else "")

    ok &= require_substance("stage-1/submission/cycloprop-stage1.md", 2500)
    ok &= check_declared_numbers("stage-1/submission/cycloprop-stage1.md", data)

    ok &= check_numeric_coverage("stage-1/submission/cycloprop-stage1.md", data)

    # The PDF has to be this document. Its own required sections and a few of its declared
    # values are the cheapest identity evidence that survives a rebuild.
    want = list(REQUIRED_ITEMS)
    decl = re.search(r"##\s*Numbers used\s*(.*?)(\n##\s|\Z)", text, re.S | re.I)
    if decl:
        for d in [m for m in (NUM_DECL.match(l) for l in decl.group(1).splitlines()) if m][:3]:
            want.append(d.group(2).rstrip("0").rstrip(".") if "." in d.group(2) else d.group(2))
    ok &= check_pdf("stage-1/submission/cycloprop-stage1.pdf", must_contain=want)

    ok &= check_human_gate()

    draft = ROOT / "stage-1" / "submission" / "email-draft.md"
    ok &= report(draft.is_file(), "week5: the email is drafted and staged for a human to send")
    if draft.is_file():
        d = draft.read_text(encoding="utf-8").lower()
        # Naming the organiser in a draft is not sending to them. Sending stays a blocked
        # trigger; this only stops a finished draft going to nobody in particular.
        for needle, label in [("cycloprop-stage1.pdf", "names the attachment"),
                              ("attachment", "says there is an attachment"),
                              ("pushpak_gc2026@aero.iitb.ac.in", "names the organiser address"),
                              ("subject", "carries a subject line")]:
            ok &= report(needle in d, f"week5: the staged email {label}")
    return ok


WEEKS = {1: week1, 2: week2, 3: week3, 4: week4, 5: week5}


AUDIT_MARKER = "AUDIT-COMPLETE"
HUMAN_GATE_MARKERS = ["REGISTRATION-CONFIRMED", "ELIGIBILITY-CHECKED",
                      "ROSTER-CONFIRMED", "SENDER-CONFIRMED",
                      "TECHNICAL-READ-COMPLETE"]
HUMAN_GATE_FILE = "stage-1/human-gate.md"
HUMAN_GATE_STATUS_HEADING = "## Status"


def check_audits_exist(target):
    """The accepted judgment gaps around prose quality, mass bases and source strength are
    supposed to be caught by the weekly audit. That mitigation was named in the config and
    enforced nowhere in this script, so a week could be green with no audit written.

    Only weeks already marked done are required to carry one. The week being gated right
    now is mid-flight and its audit does not exist yet."""
    done = done_set()
    missing = []
    for w in sorted(x for x in done if x <= target):
        p = ROOT / "stage-1" / "audit" / f"week-{w}.md"
        if not p.is_file():
            missing.append(f"week {w} has no audit file")
        elif AUDIT_MARKER not in p.read_text(encoding="utf-8"):
            missing.append(f"week {w} audit has no {AUDIT_MARKER}")
    return report(not missing, "every completed week carries a finished audit",
                  "; ".join(missing[:4]) if missing else f"{len(done)} week(s) audited")


def check_human_gate():
    """Week H is a human task list and week 5 is a hard block on it. These are status
    markers a person writes, never personal details, and never anything an agent may
    assert on their behalf."""
    p = ROOT / HUMAN_GATE_FILE
    if not p.is_file():
        return report(False, "week5: the human gate file exists",
                      f"{HUMAN_GATE_FILE} is missing")
    text = p.read_text(encoding="utf-8")
    # Read the status block only, and require the marker to be the whole line. Searching the
    # file for the substring passed TECHNICAL-READ-COMPLETE the moment the instructions above
    # explained how to write it, so the marker gating final staging was already satisfied by
    # the sentence telling a person to write it later. The other four survived that only
    # because their prose happened to spell the PENDING form.
    head, sep, status = text.partition(HUMAN_GATE_STATUS_HEADING)
    if not sep:
        return report(False, "week5: the human gate file has a status block",
                      f"{HUMAN_GATE_FILE} has no '{HUMAN_GATE_STATUS_HEADING}' heading")
    written = {ln.strip() for ln in status.splitlines()}
    absent = [m for m in HUMAN_GATE_MARKERS if m not in written]
    return report(not absent, "week5: the human gate is confirmed before anything is staged",
                  "outstanding: " + ", ".join(absent) if absent else "")


def done_set():
    out = set()
    if PROGRESS_DIR.is_dir():
        for p in PROGRESS_DIR.glob("week-*.md"):
            m = re.search(r"week-(\d+)", p.name)
            if m and DONE_MARKER in p.read_text(encoding="utf-8"):
                out.add(int(m.group(1)))
    return out


NEXT_WEEK = re.compile(r"^NEXT-WEEK:\s*(\d+)\s*$", re.M)


def expected_done():
    """How many weeks the handoff claims are finished. The progress files cannot police
    their own highest entry: deleting week-4.md just lowers the maximum, and a gap check
    over 1..max never looks above it. The handoff marker is the external witness, and it
    is the same marker the supervisor already greps for."""
    p = ROOT / "handoff.md"
    found = NEXT_WEEK.findall(p.read_text(encoding="utf-8")) if p.is_file() else []
    # Exactly one. Two markers and the first wins silently, which is a way for the handoff
    # to say one thing to the gate and another to the reader.
    if not report(len(found) == 1, "handoff.md carries exactly one NEXT-WEEK marker",
                  f"{len(found)} found, so a deleted progress file would be invisible"):
        return None
    return int(found[0]) - 1


def highest_done():
    done = done_set()
    best = max(done) if done else 0
    exp = expected_done()
    if exp is not None:
        best = max(best, min(exp, max(WEEKS)))
    # A gap means a progress file was removed or a week never finished. --all would
    # otherwise silently stop short of it. The supervisor gates week N itself, so this
    # only has to be visible, but it does have to be visible.
    missing = [w for w in range(1, best + 1) if w not in done]
    if missing:
        report(False, "progress files run without gaps",
               "no done marker for week(s) " + ", ".join(map(str, missing)))
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
    check_audits_exist(target)
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
