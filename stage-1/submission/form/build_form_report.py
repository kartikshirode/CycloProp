"""Fill the organisers' Stage 1 report template from numbers.json.

The Google Form asks for one zip holding a report "as per template shared". This script opens
that template, writes every section from the same numbers.json the rest of the project reads,
draws the three figures the template asks for that the project did not have, and exports a PDF
through Word.

    python stage-1/submission/form/build_form_report.py
"""
import copy
import json
import math
import subprocess
import sys
from pathlib import Path

import docx
from docx.shared import Mm, Pt
from docx.text.paragraph import Paragraph
from docx.table import Table

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
TEMPLATE = ROOT / "Report Template - Grand challenge 2 .docx"
NUMBERS = ROOT / "stage-1" / "design" / "numbers.json"
FIGSRC = ROOT / "stage-1" / "submission" / "figures"
BUILD = HERE / "build"
OUT_STEM = "CycloProp_TM-5A7C41AF909_Stage1_Report"

TEAM = {
    "team_id": "TM-5A7C41AF909",
    "competition_id": "CP-439436FADAD2",
    "team_name": "Kalash",
    "institution": "VPKBIET",
    "category": "UG",
    "leader": "Kartik Shirode",
    "members": "Kartik Shirode (team leader), Mandar Wagh, Aditya Shilalkar. All B.Tech third year",
    "mentor": "None at Stage 1",
    "email": "kartikshirode123@gmail.com",
    "phone": "9823376032",
    "design_name": "Kalash CR-1",
    "date": "27 September 2026",
}

D = json.loads(NUMBERS.read_text(encoding="utf-8"))


def g(path):
    node = D
    for part in path.split("."):
        node = node[int(part)] if isinstance(node, list) else node[part]
    return node


def f(x, dp):
    return f"{x:,.{dp}f}"


# ------------------------------------------------------------------ derived, all from D

RHO = 1.225
T = g("performance.thrust_N")
T_LOW = g("performance.thrust_N_conservative")
RPM = g("operating.rpm")
U = g("operating.tip_speed_ms")
RE = g("operating.reynolds")
P_AERO = g("performance.aero_power_W")
P_TARE = g("performance.tare_power_W")
P_SHAFT = P_AERO + P_TARE
Q_ROTOR = g("structure.shaft_torque_Nm")
P_ESC_IN = g("performance.electrical_power_W")
P_MODULE = g("performance.module_electrical_power_W")
P_MOTOR_IN = g("performance.motor_input_W")
ETA = D["efficiency"]
M_NOM = g("results.total_mass_g")
M_CON = g("results.mass_g_conservative")
TW = g("results.thrust_to_weight")
TW_STACK = g("results.thrust_to_weight_conservative")
W_N = g("results.weight_N")
G0 = W_N / (M_NOM / 1000.0)
TW_COEF = T_LOW / W_N
TW_MASS = T / (M_CON / 1000.0 * G0)
MU = RHO * U * g("geometry.chord_m") / RE
SENS = D["thrust_sensitivity"]
SCHED = [r["pitch_deg"] for r in D["pitch_schedule"]]
PITCH_MAX, PITCH_MIN = max(SCHED), min(SCHED)
ARC_MM = (g("pitch.servo_gear_mm") / 2.0) * math.radians(g("pitch.servo_travel_deg"))
BLADE_STRESS = g("structure.blade_combined_Nm") / g("structure.blade_allowable_Nm") \
    * g("structure.blade_wrinkle_stress_MPa")
CFRP_TAU_MPA = 55.0
SHAFT_STRESS = CFRP_TAU_MPA / g("structure.shaft_combined_margin")
AL7075_MPA = 400.0
HORN_STRESS = AL7075_MPA * g("structure.pitch_link_load_N") / g("structure.pitch_link_allowable_N")
CONFIGS = D["configuration_candidates"]

for name, a, b in [("ideal power", T ** 1.5 / math.sqrt(2 * RHO * g("performance.momentum_area_m2")),
                    g("performance.ideal_power_W")),
                   ("thrust from coefficient",
                    g("performance.blade_area_coeff") * 0.5 * RHO * U ** 2 * g("performance.blade_area_m2"), T),
                   ("shaft torque", P_SHAFT / (RPM * 2 * math.pi / 60), Q_ROTOR),
                   ("ESC input", P_SHAFT / (ETA["transmission"] * ETA["motor"] * ETA["esc"]), P_ESC_IN)]:
    assert abs(a - b) / b < 2e-3, (name, a, b)

MASS_GROUPS = [
    ("Blades", ["blade foam cores, 3 off", "blade skins, 3 off", "blade spar tubes, 3 off",
                "blade root close-outs, 3 blades"], "3", "per blade",
     "PMI foam core at 52 kg/m3 and 88% fill, 2 plies of 60 gsm carbon twill, an 8.71 mm CFRP "
     "spar on the pitch axis and two 7075-T6 root fittings, integrated over the NACA 0020 section"),
    ("Blade hubs", ["rotor spider arms, 6 off", "rotor hub bosses, 2 off",
                    "root attachment brackets, 6 off"], "2 hub sets", "per set",
     "6 CFRP spider arms of 14 x 1.5 mm, 2 split 7075-T6 bosses of 22 mm OD, 6 7075-T6 clevis "
     "brackets"),
    ("Shaft", ["rotor shaft tube", "shaft end plugs, 2 off"], "1", "",
     "Roll wrapped CFRP tube, 16 mm OD, 1.5 mm wall, 340 mm, with bonded 7075-T6 end plugs "
     "forming the 15 mm journals"),
    ("Bearings", ["main bearings, 2 off", "pitch bearings, 12 off",
                  "carrier support bearings, 2 off"], "16", "",
     "2 x 61802 main (8.0 g each), 12 x 693ZZ pitch (1.3 g each), 2 x MR128ZZ carrier (2.2 g "
     "each), supplier listings"),
    ("Frame", ["bearing blocks, 2 off", "frame tubes, 4 off", "motor mount plate",
               "frame and mount design reserve"], "1", "",
     "2 machined 7075-T6 bearing blocks, 4 CFRP tubes of 8 mm OD, a 2.5 mm 7075-T6 motor plate, "
     "and a visible 15.0 g reserve for gussets, clamps and trays not yet drawn"),
    ("Pitch mechanism", ["pitch links with rod ends, 3 off", "pitch horns, 3 off",
                         "offset pivot post and pin", "phasing carrier ring, 40 mm gear",
                         "servo sector gear, 60 mm"], "1 set", "",
     "3 CFRP pitch links with rod ends, 3 7075-T6 horns, the offset post, a 6061-T6 carrier ring "
     "with its 40 mm gear and the 60 mm sector gear"),
    ("Actuator", ["vectoring actuator servos, 2 off"], "2", "20.00 g",
     "20 g class digital metal gear servos, supplier listing"),
    ("Motor", ["motor, MN5006 KV450"], "1", "106.00 g",
     "T-Motor MN5006 KV450 datasheet, with cable"),
    ("ESC", ["esc, 40 A 8S class"], "1", "19.50 g", "40 A 8S class ESC with leads, supplier listing"),
    ("Fasteners", ["fasteners and threaded inserts", "structural adhesive at module joints"],
     "about 40", "", "M3 screws, washers and threaded inserts, plus epoxy paste at the bonded "
     "joints. Both are allowances"),
    ("Mounting hardware", ["airframe mount lugs, 4 off"], "4", "1.80 g",
     "7075-T6 lugs at the 4 airframe mount points"),
    ("Transmission", ["rotor belt pulley, 68 tooth", "motor belt pulley, 16 tooth", "drive belt",
                      "belt tensioner and bracket"], "1 set", "",
     "HTD-3M 16 and 68 tooth 6061-T6 pulleys, 9 mm by 375 mm belt, idler tensioner. 4.25 to 1"),
    ("Other", ["pitch offset controller", "controller step down regulator",
               "module wiring harness"], "3", "",
     "8.5 g controller board, 10.0 g step down regulator allowance, 25.2 g wiring harness "
     "allowance"),
]


def mass_groups():
    lines = {r["item"]: r for r in D["mass_budget_g"]}
    used = [i for _, items, *_ in MASS_GROUPS for i in items]
    assert sorted(used) == sorted(lines), "every budget line in exactly one group"
    rows = []
    for name, items, qty, unit, basis in MASS_GROUPS:
        nom = sum(lines[i]["mass_g"] for i in items)
        con = sum(lines[i]["conservative_g"] for i in items)
        if unit == "per blade":
            unit = f"{nom / 3:.2f} g"
        elif unit == "per set":
            unit = f"{nom / 2:.2f} g"
        rows.append((name, qty, unit or "-", nom, con, basis))
    assert abs(sum(r[3] for r in rows) - M_NOM) < 0.02
    assert abs(sum(r[4] for r in rows) - M_CON) < 0.05
    return rows


# ----------------------------------------------------------------------------- figures


def pdf_png(name):
    out = BUILD / name
    subprocess.run(["pdftoppm", "-r", "220", "-png", "-singlefile",
                    str(FIGSRC / f"{name}.pdf"), str(out)], check=True)
    return BUILD / f"{name}.png"


def fig_concepts():
    fig, axes = plt.subplots(1, 3, figsize=(7.2, 2.6))
    layouts = [(1, 110), (2, 80), (3, 65)]
    for ax, (n, r_mm), cfg in zip(axes, layouts, CONFIGS):
        ax.set_aspect("equal")
        ax.axis("off")
        gap = 20
        xs = [i * (2 * r_mm + gap) for i in range(n)]
        for x in xs:
            ax.add_patch(Circle((x, 0), r_mm, fill=False, lw=1.2, color="#1f3b57"))
            for k in range(3):
                a = math.radians(90 + 120 * k)
                ax.plot([x + 0.7 * r_mm * math.cos(a), x + r_mm * math.cos(a)],
                        [0.7 * r_mm * math.sin(a), r_mm * math.sin(a)], color="#b5651d", lw=3)
            ax.plot([x], [0], marker="o", ms=3, color="#1f3b57")
        span = xs[-1] + 2 * r_mm
        ax.set_xlim(-r_mm - 10, xs[-1] + r_mm + 10)
        ax.set_ylim(-260, 150)
        ax.text(span / 2 - r_mm, -150,
                f"{n} x R {r_mm} mm, {cfg['rpm']:.0f} rpm\n"
                f"Re {cfg['reynolds']:,.0f}\n"
                f"mass {cfg['module_mass_g']:.0f} g, T/W {cfg['module_tw']:.2f}\n"
                f"stacked downside T/W {cfg['module_tw_conservative']:.2f}",
                ha="center", va="top", fontsize=6.8)
    fig.suptitle("End views to a common scale, 17.0 N total thrust in each", fontsize=8)
    out = BUILD / "fig-concepts.png"
    fig.savefig(out, dpi=220, bbox_inches="tight")
    plt.close(fig)
    return out


def fig_rpm():
    n0 = RPM
    ns = [1700 + 10 * i for i in range(100)]
    fig, (a, b) = plt.subplots(1, 2, figsize=(7.2, 2.8), layout="constrained")
    a.plot(ns, [T * (n / n0) ** 2 for n in ns], color="#1f3b57", lw=1.2,
           label="T = 17.0 (n / 2337)^2")
    a.plot(ns, [T_LOW * (n / n0) ** 2 for n in ns], color="#1f3b57", lw=0.8, ls="--",
           label="low coefficient, 5% loss")
    a.axhline(10, color="grey", lw=0.8, ls=":")
    a.text(1710, 10.3, "10 N requirement", fontsize=6.5, color="grey")
    for r in SENS:
        a.plot(r["rpm"], r["thrust_N"], "o", ms=3.5, color="#b5651d")
    a.set_xlabel("rotor speed, rpm", fontsize=7.5)
    a.set_ylabel("thrust, N", fontsize=7.5)
    a.legend(fontsize=6.2, loc="upper left")
    a.tick_params(labelsize=7)
    p0 = P_MOTOR_IN
    b.plot(ns, [p0 * (n / n0) ** 3 for n in ns], color="#1f3b57", lw=1.2,
           label="motor input, P ~ n^3")
    b.axhline(520.0, color="#a33", lw=0.8, ls="--")
    b.text(1710, 528, "MN5006 derated continuous, 520 W", fontsize=6.5, color="#a33")
    for r in SENS:
        b.plot(r["rpm"], r["motor_input_W"], "o", ms=3.5, color="#b5651d")
    b.plot(RPM, P_MOTOR_IN, "s", ms=5, mfc="none", color="#1f3b57")
    b.text(RPM + 20, P_MOTOR_IN - 40, f"design\n{P_MOTOR_IN:.1f} W", fontsize=6.5)
    b.set_xlabel("rotor speed, rpm", fontsize=7.5)
    b.set_ylabel("power, W", fontsize=7.5)
    b.legend(fontsize=6.2, loc="upper left")
    b.tick_params(labelsize=7)
    out = BUILD / "fig-rpm.png"
    fig.savefig(out, dpi=220)
    plt.close(fig)
    return out


def fig_powerflow():
    fig, ax = plt.subplots(figsize=(8.6, 2.6))
    ax.axis("off")
    ax.set_xlim(0, 102)
    ax.set_ylim(0, 34)
    motor_out = P_MOTOR_IN * ETA["motor"]
    boxes = [
        (1, f"8S pack\n{P_MODULE:.1f} W\nat the module"),
        (18, f"ESC\neff {ETA['esc']:.2f}\nin {P_ESC_IN:.1f} W"),
        (35, f"Motor\neff {ETA['motor']:.2f}\nin {P_MOTOR_IN:.1f} W"),
        (52, f"Belt 4.25:1\neff {ETA['transmission']:.2f}\nin {motor_out:.1f} W"),
        (69, f"Rotor shaft\n{P_SHAFT:.1f} W\n{Q_ROTOR:.3f} Nm, {RPM:.0f} rpm"),
        (86, f"Blades {P_AERO:.1f} W\nrotor tare\n{P_TARE:.1f} W"),
    ]
    for x, text in boxes:
        ax.add_patch(FancyBboxPatch((x, 17), 14.5, 13, boxstyle="round,pad=0.4",
                                    fc="#eef3f8", ec="#1f3b57", lw=0.9))
        ax.text(x + 7.25, 23.5, text, ha="center", va="center", fontsize=6.0)
    for x, _ in boxes[:-1]:
        ax.annotate("", xy=(x + 16.6, 23.5), xytext=(x + 15.0, 23.5),
                    arrowprops=dict(arrowstyle="->", color="#1f3b57", lw=0.9))
    reg = g("performance.regulator_loss_W")
    ax.add_patch(FancyBboxPatch((18, 2), 30, 9, boxstyle="round,pad=0.4",
                                fc="#fbf1e6", ec="#b5651d", lw=0.9))
    ax.text(33, 6.5, f"Step down regulator, 0.85, loss {reg:.2f} W\n"
                     f"controller {g('performance.controller_power_W'):.1f} W, "
                     f"2 servos {g('performance.actuator_power_W'):.1f} W",
            ha="center", va="center", fontsize=6.4)
    ax.annotate("", xy=(18, 8), xytext=(7.5, 16.6),
                arrowprops=dict(arrowstyle="->", color="#b5651d", lw=0.9))
    out = BUILD / "fig-powerflow.png"
    fig.savefig(out, dpi=220, bbox_inches="tight")
    plt.close(fig)
    return out


# ------------------------------------------------------------------------ docx helpers


class Report:
    def __init__(self, path):
        self.doc = docx.Document(str(path))
        self.body = self.doc.element.body

    def blocks(self):
        for el in self.body.iterchildren():
            tag = el.tag.split("}")[1]
            if tag == "p":
                yield Paragraph(el, self.doc)
            elif tag == "tbl":
                yield Table(el, self.doc)

    def tables(self):
        return [b for b in self.blocks() if isinstance(b, Table)]

    def para(self, text, nth=None):
        hits = [b for b in self.blocks() if isinstance(b, Paragraph) and b.text.strip() == text]
        if nth is None:
            assert len(hits) == 1, (text, len(hits))
            return hits[0]
        return hits[nth]

    @staticmethod
    def _clear(p):
        for r in list(p.runs):
            r._r.getparent().remove(r._r)

    def answer(self, label, texts, nth=None):
        """Write the answer into the empty paragraph that follows a bold label."""
        if isinstance(texts, str):
            texts = [texts]
        lab = self.para(label, nth)
        slot = Paragraph(lab._p.getnext(), self.doc)
        assert slot.text.strip() == "", label
        anchor = slot
        for i, t in enumerate(texts):
            if i:
                new = copy.deepcopy(slot._p)
                anchor._p.addnext(new)
                anchor = Paragraph(new, self.doc)
            self._clear(anchor)
            anchor.add_run(t)
        return anchor

    def paragraph_after(self, element, text="", italic=False, size=None):
        ref = self.para_template()
        new = copy.deepcopy(ref)
        element.addnext(new)
        p = Paragraph(new, self.doc)
        self._clear(p)
        if text:
            r = p.add_run(text)
            r.italic = italic
            if size:
                r.font.size = Pt(size)
        return p

    def para_template(self):
        lab = self.para("Design name:")
        return lab._p.getnext()

    @staticmethod
    def cell(c, text, bold=False, size=9):
        for p in c.paragraphs[1:]:
            p._p.getparent().remove(p._p)
        p = c.paragraphs[0]
        Report._clear(p)
        for i, line in enumerate(str(text).split("\n")):
            if i:
                p = c.add_paragraph()
            r = p.add_run(line)
            r.font.name = "Verdana"
            r.font.size = Pt(size)
            r.bold = bold

    @staticmethod
    def picture(c, path, caption, width_mm=150):
        for p in c.paragraphs[1:]:
            p._p.getparent().remove(p._p)
        p = c.paragraphs[0]
        Report._clear(p)
        p.add_run().add_picture(str(path), width=Mm(width_mm))
        cap = c.add_paragraph()
        r = cap.add_run(caption)
        r.italic = True
        r.font.name = "Verdana"
        r.font.size = Pt(8)

    @staticmethod
    def label(c):
        return c.text.replace("*", "").strip().lower()

    def fill_rows(self, table, rows, first_col=1):
        """rows maps the row label in column 0 to the values for the following columns."""
        done = set()
        for row in table.rows:
            key = self.label(row.cells[0])
            for want, values in rows.items():
                if key == want.lower():
                    for j, v in enumerate(values):
                        self.cell(row.cells[first_col + j], v)
                    done.add(want)
        missing = set(rows) - done
        assert not missing, missing

    @staticmethod
    def add_row_after(table, idx):
        tr = copy.deepcopy(table.rows[idx]._tr)
        table.rows[idx]._tr.addnext(tr)
        return table.rows[idx + 1]

    def fill_grid(self, table, start, data):
        """Write rows of values from row `start`, adding rows by copying the last one."""
        for i, values in enumerate(data):
            r = start + i
            if r >= len(table.rows) or self._is_image_row(table.rows[r]):
                self.add_row_after(table, r - 1)
            for j, v in enumerate(values):
                self.cell(table.rows[r].cells[j], v)

    @staticmethod
    def _is_image_row(row):
        return "insert" in row.cells[0].text.lower()

    def image_cell(self, table, path, caption, width_mm=150):
        for row in table.rows:
            for c in row.cells:
                if "insert" in c.text.lower():
                    self.picture(c, path, caption, width_mm)
                    return
        raise AssertionError("no image slot")

    def numbered(self, first_number, items, renumber_from=1):
        """The template's numbered lines are literal '1.' runs; fill them in place."""
        paras = [b for b in self.blocks() if isinstance(b, Paragraph)]
        start = [i for i, p in enumerate(paras) if p.text.strip() == f"{first_number}."]
        assert len(start) == 1, first_number
        i0 = start[0]
        slots = paras[i0:i0 + len(items)]
        for k, (p, text) in enumerate(zip(slots, items)):
            assert p.text.strip().rstrip(".").isdigit(), p.text
            p.runs[0].text = f"{renumber_from + k}."
            p.runs[-1].text = " " + text


# ---------------------------------------------------------------------------- content


def build():
    BUILD.mkdir(parents=True, exist_ok=True)
    figs = {n: pdf_png(n) for n in ["fig-arrangement", "fig-linkage", "fig-pitch-schedule",
                                     "fig-vector-map", "fig-blade-section", "fig-mass",
                                     "fig-blade-load"]}
    figs["fig-concepts"] = fig_concepts()
    figs["fig-rpm"] = fig_rpm()
    figs["fig-powerflow"] = fig_powerflow()

    rep = Report(TEMPLATE)
    tb = rep.tables()
    assert len(tb) == 36, len(tb)

    # Title block
    sub = rep.para("Stage 1 - Preliminary Engineering Design Report Template")
    sub.runs[0].text = "Stage 1 - Preliminary Engineering Design Report"
    for r in sub.runs[1:]:
        r.text = ""
    intro = rep.para("This template is intended for the preliminary engineering design submission. "
                     "Participants should provide concise, technically defensible information "
                     "supported by calculations, CAD views, plots, references, and assumptions "
                     "wherever applicable.")
    Report._clear(intro)
    intro.add_run(f"{TEAM['design_name']}, a single cyclorotor propulsion module. Team "
                  f"{TEAM['team_name']}, {TEAM['institution']}. Team ID {TEAM['team_id']}.")

    # Team and submission information
    rep.fill_rows(tb[0], {
        "Team ID": [TEAM["team_id"]],
        "Team Name": [TEAM["team_name"]],
        "Institution / Organization": [f"{TEAM['institution']} (category: {TEAM['category']})"],
        "Team Leader": [TEAM["leader"]],
        "Team Members": [TEAM["members"]],
        "Faculty / Industry Mentor, if any": [TEAM["mentor"]],
        "Email Address": [TEAM["email"]],
        "Contact Number": [TEAM["phone"]],
        "Proposed Design Name": [TEAM["design_name"]],
        "Date of Submission": [TEAM["date"]],
    })

    # 1.1
    rep.answer("Design name:", TEAM["design_name"])
    rep.answer("Brief description of the proposed configuration:", [
        f"One cycloidal rotor, 220.0 mm in diameter and {g('geometry.span_m') * 1000:.1f} mm "
        f"wide, with 3 NACA 0020 blades of {g('geometry.chord_m') * 1000:.1f} mm chord. Each "
        f"blade pitches plus or minus 40 degrees about its 30 percent chord point through its own "
        f"passive four-bar linkage, and all three linkages share one offset pivot "
        f"{g('pitch.offset_m') * 1000:.2f} mm from the rotor axis.",
        f"Turning that offset about the rotor axis turns the thrust vector. Two 20 g servos do "
        f"it through a phasing carrier outside the rotor, so nothing on the rotor is actuated. A "
        f"T-Motor MN5006 KV450 drives the rotor at {RPM:.0f} rpm through a 4.25 to 1 toothed "
        f"belt from an 8S pack. Design thrust is {T:.1f} N.",
    ])
    rep.image_cell(tb[1], figs["fig-arrangement"],
                   "Figure 1. General arrangement. Rotor plane (left) and side view (right). "
                   "Swept diameter 296.5 mm, packaged envelope 364.4 x 316.5 x 362.5 mm on 4 "
                   "mount points.")

    # 1.2
    rep.fill_rows(tb[2], {
        "Rotor diameter": ["220.0 (296.5 swept by the pitching blades)"],
        "Rotor width": [f"{g('geometry.span_m') * 1000:.1f}"],
        "Number of blades": ["3"],
        "Blade chord": [f"{g('geometry.chord_m') * 1000:.1f}"],
        "Blade profile / airfoil": ["NACA 0020"],
        "Operating RPM": [f"{RPM:.0f}"],
        "Blade pitch range": ["-40 to +40"],
        "Pitch amplitude": ["40"],
        "Estimated thrust": [f"{T:.1f} ({T_LOW:.2f} on the low coefficient)"],
        "Estimated shaft power": [f"{P_SHAFT:.1f}"],
        "Estimated electrical power": [f"{P_MODULE:.1f} at the module"],
        "Estimated module mass": [f"{M_NOM / 1000:.3f} ({M_CON / 1000:.3f} conservative)"],
        "Estimated thrust-to-weight ratio": [f"{TW:.4f} ({TW_STACK:.4f} worst case)"],
        "Estimated maximum thrust-vectoring angle": ["+/- 60 (120 of authority)"],
    })

    # 1.3
    rep.answer("Principal design features:", [
        "One rotor rather than a cluster. On a common model it gives the lowest module mass and "
        "the best thrust to weight of the three layouts we compared (section 3).",
        "Passive cyclic pitch. A four-bar per blade sets the 40 degree amplitude from one "
        "11.53 mm offset, and no actuator rides on the rotor.",
        "Thrust vectoring by rotating that offset: 120 degrees of authority from 2 servos "
        "through a 1.5 step up gear pair.",
        f"Sandwich blades of PMI foam, 2 plies of 60 gsm carbon twill and a CFRP spar on the "
        f"pitch axis, {g('structure.blade_mass_kg') * 1000:.2f} g each.",
        "Every number in this report comes out of Python scripts reading one data file, and a "
        "checking script recomputes them, so geometry, performance and mass stay consistent.",
    ])
    rep.answer("Key design innovation / distinguishing feature:", [
        "The pitch schedule and the thrust direction come from the same linkage. The offset "
        "length sets the amplitude and its direction sets the phase, so vectoring needs one small "
        "rotation of a carrier that doesn't spin with the rotor.",
        "The linkage solution also decided the drivetrain. The solved pitch links pass within "
        f"{g('pitch.axis_keepout_mm')} mm of the rotor axis, so no shaft can run through that "
        "plane, and the rotor is driven from one end only.",
    ])
    rep.answer("Expected performance:",
               f"{T:.1f} N at {RPM:.0f} rpm for {P_MODULE:.1f} W at the module. The mass budget "
               f"is {M_NOM:.2f} g, so thrust to weight is {TW:.4f} at the design point. With the "
               f"conservative mass and a 5 percent thrust loss for blade flexibility applied "
               f"together it falls to {TW_STACK:.4f}.")
    rep.answer("Principal technical challenges identified:", [
        f"1. Thrust to weight clears 2.5 by only 0.8 percent, on a mass estimate that isn't "
        f"accurate to 0.8 percent. Closing the worst case needs {g('results.mass_to_close_stacked_g')} g.",
        "2. The thrust coefficient is transferred from published rotors of the same shape "
        "family, not measured on this one.",
        "3. The motor runs at 93 percent of a derated continuous power rating.",
        "4. The quasi steady model almost certainly under-predicts side force, which costs "
        "vectoring authority.",
    ])

    # 2.1
    rep.fill_rows(tb[3], {
        "Thrust": [f"{T:.1f} N design, {T_LOW:.4f} N with a 5% blade flexibility loss"],
        "Thrust-to-weight ratio": [f"{TW:.4f} design. {TW_STACK:.4f} with both downsides. "
                                   f"Stage 2 gate: conservative mass under "
                                   f"{g('results.mass_target_week4_g')} g"],
        "Rotor type": ["Single cyclorotor, 3 blades, passive four-bar cyclic pitch, +/-40 deg"],
        "Thrust vectoring": ["120 deg of direction authority by rotating the pitch offset"],
        "Design approach": ["Closed form analysis in Python from one data file. CAD, CFD and "
                            "FEA are Stage 2 items"],
        "Final objective": ["Geometry frozen at Stage 1. Stage 2 turns it into CAD, drawings, a "
                            "verified mass and a spin test plan"],
    }, first_col=2)

    # 2.2
    over = D["power_by_radius"][0]
    rep.fill_rows(tb[4], {
        "Rotor diameter": ["220.0 mm", f"Smallest radius the selected motor holds continuously. "
                           f"At 100 mm the motor would need {over['motor_input_W']:.1f} W "
                           f"against 520.0 W derated continuous"],
        "Rotor width": ["290.4 mm", "4 chords, blade aspect ratio 4, from Kellen's UAV scale "
                        "optimum shape family [1]"],
        "Number of blades": ["3", "At fixed solidity fewer blades give more thrust [2], and 3 "
                             "is Kellen's optimum for this Reynolds band [1]"],
        "Blade chord": ["72.6 mm", f"Chord to radius 0.66, Kellen's optimum. Solidity "
                        f"{g('performance.solidity')}, inside the 0.30 to 0.40 band he measured"],
        "Blade profile / airfoil": ["NACA 0020", "Thick symmetric section. Efficient at this "
                                    "Reynolds number and deep enough for a real spar"],
        "Operating RPM": [f"{RPM:.0f}", f"The speed at which a blade area coefficient of "
                          f"{g('performance.blade_area_coeff')} gives {T:.1f} N. Chord Reynolds "
                          f"{RE:,.0f}, inside Kellen's 100,000 to 300,000"],
        "Mean blade pitch": ["0 deg", "The horn to chord angle, -102.50 deg, is chosen so the "
                             "cycle mean pitch is zero"],
        "Pitch amplitude": ["40 deg", "Kellen's optimum for this shape family [1]"],
        "Maximum vectoring angle": ["+/-60 deg", "80 deg of servo travel through a 1.5 step up "
                                    "gives 120 deg of carrier rotation"],
        "Target power": [f"{P_MODULE:.1f} W", f"Motor input {P_MOTOR_IN:.1f} W against the "
                         f"MN5006's 520 W derated continuous rating"],
        "Target module mass": ["under 693 g", f"The mass at which 17.0 N gives exactly 2.5. "
                               f"Budget {M_NOM:.2f} g nominal, {M_CON:.2f} g conservative"],
    })

    # 2.3
    rep.fill_grid(tb[5], 1, [
        ["1", f"Blade area thrust coefficient {g('performance.blade_area_coeff')}, held below "
              f"the 0.6648 Kellen measured on this shape family", "[1], [2]. Deliberately low"],
        ["2", f"Figure of merit {g('performance.figure_of_merit')}: Kellen's 0.6 scaled to our "
              f"lower coefficient by (0.6055 / 0.6648)^1.5", "[1]"],
        ["3", f"Efficiencies: belt {ETA['transmission']}, motor {ETA['motor']}, ESC "
              f"{ETA['esc']}. Rotor tare 10 percent of shaft power",
         "Efficiencies assumed; tare from [2]"],
        ["4", "Motor 180 s ratings derated to 0.80 for continuous duty",
         "Judgement. The problem statement sets no endurance to size it against"],
        ["5", "Hover at sea level, ISA air, density 1.225 kg/m3, no freestream", "Standard"],
        ["6", "Blade loads at 4.0 times the mean, a 1.20 overspeed case, every margin floored "
              "at 1.5", "Top of the published 3 to 4 range [8]"],
        ["7", "Material allowables are published class values", "No coupon tests yet"],
        ["8", "Mass growth by line class: 8% catalogue, 12% machined, 15% calculated, 25% "
              "allowance", "Set before the total was known"],
    ])

    # 3.1
    c1, c2, c3 = CONFIGS
    rep.fill_rows(tb[6], {
        "Concept name": ["Single rotor, 3 blades, R 110 mm", "Two rotors, 3 blades each, R 80 mm",
                         "Three rotors, 3 blades each, R 65 mm"],
        "Operating principle": [f"One rotor makes all 17.0 N at {c1['rpm']:.0f} rpm",
                                f"Each rotor makes 8.5 N at {c2['rpm']:.0f} rpm",
                                f"Each rotor makes 5.67 N at {c3['rpm']:.0f} rpm"],
        "Advantages": [f"Least hardware: one shaft, one mechanism, one belt. Chord Reynolds "
                       f"{c1['reynolds']:,.0f}, inside the measured band. Lowest mass",
                       f"Smaller rotors. Aerodynamic power {c2['aero_power_W']} W, 3% lower. "
                       f"Differential thrust possible",
                       f"Smallest rotors. Aerodynamic power {c3['aero_power_W']} W. Most "
                       f"control options"],
        "Limitations": [f"Largest single rotor and the most torque, {c1['rotor_torque_Nm']} Nm, "
                        f"so it needs a belt reduction",
                        f"Hardware doubles. Reynolds {c2['reynolds']:,.0f}, below the measured "
                        f"band. 400 mm largest dimension",
                        f"Hardware triples. Reynolds {c3['reynolds']:,.0f}. 490 mm largest "
                        f"dimension, three mechanisms to phase together"],
        "Expected performance": [f"{c1['module_mass_g']} g, T/W {c1['module_tw']}, stacked "
                                 f"downside {c1['module_tw_conservative']}",
                                 f"{c2['module_mass_g']} g, T/W {c2['module_tw']}, stacked "
                                 f"downside {c2['module_tw_conservative']}",
                                 f"{c3['module_mass_g']} g, T/W {c3['module_tw']}, stacked "
                                 f"downside {c3['module_tw_conservative']}"],
    })
    rep.image_cell(tb[6], figs["fig-concepts"],
                   "Figure 2. The three layouts, end views to one scale. Masses are the early "
                   "mass envelope applied the same way to all three; the refined budget in "
                   "section 8 applies to the selected concept only.")

    # 3.2
    matrix = [("Thrust potential", 15, 5, 3, 2), ("Power requirement", 10, 4, 5, 5),
              ("Mass", 20, 5, 3, 1), ("Pitch-control capability", 10, 5, 3, 2),
              ("Thrust-vectoring capability", 10, 4, 4, 4), ("Structural feasibility", 10, 4, 4, 4),
              ("Manufacturability", 10, 5, 3, 2), ("Mechanism complexity", 10, 5, 3, 2),
              ("Cost", 5, 5, 3, 2)]
    assert sum(m[1] for m in matrix) == 100
    totals = [sum(m[1] * m[k] for m in matrix) / 5 for k in (2, 3, 4)]
    rep.fill_rows(tb[7], {m[0]: [str(m[1]), str(m[2]), str(m[3]), str(m[4])] for m in matrix})
    rep.fill_rows(tb[7], {"Total": ["100", f"{totals[0]:.0f}", f"{totals[1]:.0f}",
                                    f"{totals[2]:.0f}"]})
    rep.answer("Selected concept:", "Concept 1, the single rotor.")
    rep.answer("Basis for selection:", [
        f"It wins the criterion the challenge makes hard, module thrust to weight, by 23 percent "
        f"on the stacked downside case ({c1['module_tw_conservative']} against "
        f"{c2['module_tw_conservative']}), and it wins every other column apart from "
        f"aerodynamic power, where the clusters are about 3 percent better. Splitting the thrust "
        f"splits the aerodynamics but not the hardware: 7 of the 13 mass envelope lines multiply "
        f"by rotor count. Every disputed assumption was set in the clusters' favour, with no wake "
        f"interaction, one shared motor and controller, and the same coefficient despite their "
        f"lower Reynolds number.",
        f"Scores are 1 to 5 and the total is the weighted sum out of 100: {totals[0]:.0f}, "
        f"{totals[1]:.0f} and {totals[2]:.0f}. The thrust, power and mass rows follow the numbers "
        f"in 3.1. The other rows are our judgement and are marked as such here.",
    ])
    rep.answer("Key trade-offs:",
               f"A single rotor needs {Q_ROTOR:.3f} Nm at {RPM:.0f} rpm, more than any outrunner "
               f"in this mass class gives directly, so it carries a belt reduction. It also has "
               f"the largest swept diameter, 296.5 mm, which sets the envelope. We accept both "
               f"for about {c2['module_mass_g'] - c1['module_mass_g']:.0f} g less module mass "
               f"than the twin.")

    # 4.1
    rep.fill_rows(tb[8], {
        "Rotor architecture": ["Single cyclorotor. Blades parallel to the rotation axis, pinned "
                               "at both ends to CFRP spider arms on 7075-T6 hub bosses, on a "
                               "CFRP shaft driven from one end"],
        "Number of blades": ["3"],
        "Direction of rotation": ["Counter-clockwise, looking along the axis from the non-drive "
                                  "end"],
        "Rotor diameter": ["220.0 mm to the pitch axes. 296.5 mm swept by the pitching blades"],
        "Rotor width": ["290.4 mm blade span"],
        "Blade spacing": ["120 deg in azimuth"],
        "Operating RPM": [f"{RPM:.0f} rpm, tip speed {U:.2f} m/s"],
    })
    rep.image_cell(tb[8], figs["fig-blade-section"],
                   f"Figure 3. Blade section, NACA 0020 at 72.6 mm chord on an "
                   f"{g('structure.blade_spar_od_mm')} mm spar at 30 percent chord, which is "
                   f"also the pitch axis. Overall rotor dimensions are in Figure 1.")

    # 4.2
    re_low = RE * SENS[0]["rpm"] / RPM
    rep.fill_rows(tb[9], {
        "Airfoil / blade profile": ["NACA 0020", "--", "Kellen's shape family [1]"],
        "Chord": ["72.6", "mm", "Chord to radius 0.66"],
        "Thickness": [f"{0.2 * g('geometry.chord_m') * 1000:.2f}", "mm", "20% of chord"],
        "Blade length": ["290.4", "mm", "Aspect ratio 4"],
        "Pitch range": ["-40 to +40", "deg",
                        f"Solved schedule reaches +{PITCH_MAX:.2f} and {PITCH_MIN:.2f}"],
        "Pitch amplitude": ["40", "deg", "Set by the 11.53 mm offset"],
        "Blade twist, if any": ["0 built", "deg",
                                f"{g('performance.blade_twist_deg')} under aerodynamic load; "
                                f"{g('structure.blade_windup_deg')} wind up at the free end from "
                                f"the centrifugal pitching moment"],
        "Estimated blade mass": [f"{g('structure.blade_mass_kg') * 1000:.2f}", "g",
                                 "Integrated from the section: core, skins, spar, 2 root fittings"],
    })
    rep.answer("Reason for blade-profile selection:",
               "Thick symmetric sections hold their performance at chord Reynolds numbers near "
               "130,000, and 20 percent thickness gives a 14.5 mm deep section: room for an "
               "8.71 mm spar on the pitch axis inside a closed foam and skin cell. It is "
               "symmetric because the blade pitches both ways through 40 degrees. The curved "
               "flow at chord to radius 0.66 gives it virtual camber, which is already inside "
               "the coefficient we transfer, since Kellen measured it on the same shape family.")
    rep.answer("Expected operating Reynolds-number range:",
               f"{RE:,.0f} at the design point, from 1.225 kg/m3, {U:.2f} m/s and 72.6 mm "
               f"chord. Over the operating cases in 5.4 it runs from about {re_low:,.0f} to "
               f"{RE:,.0f}, inside Kellen's measured 100,000 to 300,000.")

    # 5.1
    for p in rep.blocks():
        if isinstance(p, Paragraph) and p.text.startswith("☐"):
            if any(k in p.text for k in ("Analytical", "Blade Element", "Published")):
                p.runs[0].text = p.runs[0].text.replace("☐", "☒")
    rep.fill_rows(tb[10], {
        "Software / calculation tool": ["Python 3 with NumPy and Matplotlib. tools/linkage.py "
                                        "(kinematics and loads), tools/structure.py (structure and "
                                        "mass), tools/check.py (recomputes and checks every "
                                        "number). All inputs and results in numbers.json"],
        "Operating condition": [f"Hover, {T:.1f} N at {RPM:.0f} rpm, no freestream"],
        "Air density": ["1.225 kg/m3"],
        "Atmospheric conditions": [f"ISA sea level. Viscosity {MU:.3e} Pa s, as implied by the "
                                   f"stored Reynolds number"],
        "Other assumptions": ["Uniform induced inflow, quasi steady blade forces, no wake "
                              "interaction, no dynamic stall beyond an incidence cap"],
    })

    # 5.2
    rep.answer("Calculation methodology:", nth=0, texts=
               "Thrust comes from a blade area thrust coefficient measured on this shape family, "
               "not from a blade element model, because at chord to radius 0.66 a blade element "
               "model without a curvilinear flow correction is less trustworthy than the "
               "measurement. Power comes from momentum theory and a figure of merit, checked "
               "by a second route through a published power loading. Blade loads come from a "
               "36 point quasi steady azimuthal model run on the solved pitch schedule.")
    rep.answer("Governing equations used:", [
        "T = C_Tb x 0.5 rho u^2 x (N c b), with u = Omega R and N c b the blade area",
        "P_ideal = T^1.5 / sqrt(2 rho A), with A = 2 R b the projected area; induced velocity "
        "v_i = sqrt(T / (2 rho A)), inflow ratio lambda = v_i / u",
        "FM = 0.6 x (C_Tb / 0.6648)^1.5; P_aero = P_ideal / FM; P_shaft = P_aero / 0.9 (10% tare)",
        "P_elec = P_shaft / (eff_belt x eff_motor x eff_ESC); Q = P_shaft / Omega; Re = rho u c / mu",
        "Azimuthal load: F(psi) = 2 pi alpha x (u_t^2 + u_p^2), alpha = theta(psi) - atan(u_p / u_t), "
        "alpha capped at 28 deg",
    ])
    rep.answer("Blade loading assumptions:",
               f"Mean vertical force {T / 3:.4f} N per blade. The azimuthal model gives a peak of "
               f"14.4260 N, a peak to mean of {g('performance.blade_load_peak_to_mean')}. A quasi "
               f"steady model under-predicts the peak, so the structure is sized on "
               f"{g('structure.blade_load_factor')}, the top of the published 3 to 4 range [8]. "
               f"The blade is not chordwise balanced: its centre of mass sits at "
               f"{g('pitch.blade_cg_pct_chord')}% chord against a 30% pitch axis, and the pitch "
               f"loads carry that.")
    rep.answer("Airfoil data / aerodynamic coefficients used:",
               f"Blade area thrust coefficient {g('performance.blade_area_coeff')} nominal and "
               f"{g('performance.blade_area_coeff_low')} low (5% flexibility loss). It is "
               f"bracketed by 0.6648 measured by Kellen on this shape family [1], 0.7211 "
               f"recomputed from Benedict's quad rotor hover point [2] and 0.8114 from his twin "
               f"rotor, which we treat as an upside only. The load model uses a thin airfoil "
               f"lift slope of 2 pi per radian, scaled to the measured mean.")

    # 5.3
    rep.fill_rows(tb[11], {
        "Tip speed": [f"{U:.2f}"],
        "Reynolds number": [f"{RE:,.0f}"],
        "Swept area": [f"{g('performance.momentum_area_m2')} (projected, 2R x b)"],
        "Estimated blade loading": [f"{g('performance.blade_area_coeff')} (blade area thrust "
                                    f"coefficient)"],
        "Estimated thrust": [f"{T:.1f}"],
        "Estimated torque": [f"{Q_ROTOR:.3f}"],
        "Estimated shaft power": [f"{P_SHAFT:.1f}"],
        "Estimated electrical power": [f"{P_MODULE:.1f}"],
    })
    rep.answer("Thrust estimation methodology and calculation:",
               f"T = {g('performance.blade_area_coeff')} x 0.5 x 1.225 x {U:.2f}^2 x "
               f"{g('performance.blade_area_m2')} = {T:.1f} N, where 0.06325 m2 is 3 blades of "
               f"72.6 by 290.4 mm. The low case takes 5 percent off for blade flexibility, "
               f"{T_LOW:.4f} N. Both clear 10 N on their own.")
    rep.answer("Power estimation methodology and calculation:",
               f"Ideal power over the projected area of {g('performance.momentum_area_m2')} m2 is "
               f"17.0^1.5 / sqrt(2 x 1.225 x {g('performance.momentum_area_m2')}) = "
               f"{g('performance.ideal_power_W'):.1f} W, with induced velocity "
               f"{g('performance.induced_velocity_ms'):.2f} m/s and inflow ratio "
               f"{g('performance.inflow_ratio')}. Over a figure of merit of "
               f"{g('performance.figure_of_merit')} that is {P_AERO:.1f} W at the blades. A 10 "
               f"percent rotor tare, {P_TARE:.1f} W, gives {P_SHAFT:.1f} W at the shaft, "
               f"{Q_ROTOR:.3f} Nm at {RPM:.0f} rpm. Through the belt, motor and ESC that is "
               f"{P_ESC_IN:.1f} W at the ESC, and the servos, controller and regulator loss take "
               f"the module to {P_MODULE:.1f} W. A second route through Benedict's measured power "
               f"loading of 0.062 N/W gives {g('performance.aero_power_W_published'):.1f} W at the "
               f"blades, 19.3 percent lower. We carry the higher one.")
    rep.answer("Expected aerodynamic efficiency / figure of merit, if applicable:",
               f"Figure of merit {g('performance.figure_of_merit')}, Kellen's measured 0.6 scaled "
               f"down to our lower coefficient so the same caution isn't spent twice. Power "
               f"loading at the module is {T / P_MODULE:.4f} N/W.")

    # 5.4
    rows54 = []
    for r in SENS[:4]:
        note = " (design point)" if abs(r["thrust_N"] - T) < 1e-9 else ""
        over = "; over the 520 W rating" if r["motor_input_W"] > 520 else ""
        rows54.append([f"{r['thrust_N']:.0f} N case{note}", f"{r['rpm']:.0f}",
                       "+/-40 deg, mean 0", f"{r['thrust_N']:.1f} N",
                       f"{r['motor_input_W']:.1f} W motor input{over}"])
    for i, row in enumerate(rows54):
        row[0] = f"Case {i + 1}: {row[0]}"
    rep.fill_grid(tb[12], 1, rows54)
    rep.image_cell(tb[12], figs["fig-rpm"],
                   "Figure 4. Thrust and motor input power against rotor speed at fixed pitch "
                   "schedule. Points are the stored sensitivity rows (13, 16, 17, 18 and 20 N). "
                   "Above the design point the motor runs out of continuous power, which is why "
                   "the design stops at 17.0 N.")

    # 6.1
    rep.fill_rows(tb[13], {
        "Mechanism description": ["Passive four-bar per blade: rotor arm L1 110.0 mm, offset "
                                  "link L2 11.53 mm (ground), pitch link L3 108.0 mm, horn L4 "
                                  "18.0 mm. All three blades share one offset pivot. Double "
                                  "crank by Grashof (11.53 + 110.0 < 18.0 + 108.0)"],
        "Actuation method": ["Rotor rotation drives the pitch. The actuators only rotate the "
                             "offset direction, through a phasing carrier that doesn't spin"],
        "Actuator type": ["Digital metal gear servos, 20 g class, 3.9 kgf cm stall, on 60 mm "
                          "sector gears driving a 40 mm carrier ring (1.5 step up), set 180 deg "
                          "apart to preload the mesh"],
        "Number of actuators": ["2"],
        "Expected actuator force / torque": [
            f"Carrier torque {g('pitch.carrier_torque_Nm')} Nm peak at 3 per rev, "
            f"{g('pitch.servo_torque_Nm')} Nm per servo against half of stall, margin "
            f"{g('pitch.servo_torque_margin')}. Peak pitch link force "
            f"{g('pitch.peak_link_force_N')} N"],
        "Pitch-control range": ["Amplitude fixed at +/-40 deg by L2. Phase commandable over "
                                "120 deg (+/-60)"],
    })
    rep.image_cell(tb[13], figs["fig-linkage"],
                   "Figure 5. Four-bar pitch kinematics at four azimuths. Transmission angle "
                   "53.88 to 135.68 deg, worst 44.32 deg read folded.")

    # 6.2
    rep.answer("Rotor azimuth definition:",
               "Azimuth psi is measured from the offset link direction, rotor turning "
               "counter-clockwise viewed from the non-drive end. Module vertical sits 9.08 deg "
               "further round, which trims out the cycle mean side force at zero command.")
    rep.answer("Pitch-angle relationship:", [
        "Solved from loop closure rather than prescribed: R u(psi) + a u(alpha) + l u(gamma) = "
        "e u(phi), and pitch theta = alpha - psi - theta_0.",
        f"It stays close to theta = 40 cos(psi - 90 - phi_c - 7.75) deg, with an rms deviation "
        f"of {g('pitch.schedule_rms_residual_deg')} deg. That deviation is what the load model "
        f"runs on and is where part of the side force comes from.",
    ])
    rep.answer("Definition of variables:",
               "R = 110.0 mm rotor arm; a = 18.0 mm horn; l = 108.0 mm pitch link; e = 11.53 mm "
               "offset; u(x) the unit vector at angle x; psi blade azimuth; alpha horn direction "
               "and gamma pitch link direction in the fixed frame; phi offset direction; phi_c "
               "the vector command; theta_0 = -102.50 deg, the fixed horn to chord angle.")
    rep.image_cell(tb[14], figs["fig-pitch-schedule"],
                   "Figure 6. Blade pitch against azimuth from the solved four-bar, against the "
                   "40 deg sinusoid. Peak pitch lags the offset direction by 7.75 deg.")

    # 6.3
    rep.fill_rows(tb[15], {
        "Degrees of freedom": ["1 per blade, driven by rotor rotation; 1 control input, the "
                               "offset direction"],
        "Maximum pitch angle": [f"+{PITCH_MAX:.2f}"],
        "Minimum pitch angle": [f"{PITCH_MIN:.2f}"],
        "Pitch amplitude": [f"40 ({PITCH_MAX - PITCH_MIN:.1f} peak to peak)"],
        "Phase angle": [f"{g('pitch.phase_delay_deg')} linkage lag; command range +/-60"],
        "Maximum actuator displacement": [f"{ARC_MM:.1f} (80 deg servo rotation at the 60 mm "
                                          f"sector gear)"],
        "Estimated actuator force / torque": [f"{g('pitch.servo_torque_Nm')} Nm per servo "
                                              f"({g('pitch.carrier_torque_Nm')} Nm at the carrier)"],
    })

    # 6.4
    rep.answer("Description of how cyclic blade pitch produces thrust vectoring:",
               "Each blade's incidence follows the geometry of its four-bar, so blades on one "
               "side of the rotor run at positive pitch and blades on the other side at "
               "negative, and the cycle averaged force points roughly along the offset "
               "direction. Turning the offset pivot about the rotor axis turns the whole pitch "
               "schedule with it, and the resultant turns by the same angle.")
    rep.answer("Expected maximum vectoring angle:",
               "+/-60 deg from the trimmed zero, 120 deg of authority. Measured side force on "
               "similar rotors runs 10 to 35 deg [3], [7], far above our model's 9.078 deg. "
               "Indexing the carrier zero at the middle of that band, we expect roughly four "
               "fifths of the authority to stay usable.")
    rep.answer("Control parameter(s):",
               "Phase command (offset direction) sets the thrust direction. Rotor speed through "
               "the ESC sets the magnitude. Amplitude is fixed by geometry.")
    rep.answer("Expected relationship between control input and thrust direction:",
               "One to one in the model: direction equals command and the magnitude stays 17.0 N "
               "at every command. That comes from the model's rotational symmetry and is not a "
               "measurement. The 9.078 deg tilt at zero command (7.75 deg linkage lag, about "
               "1.33 deg aerodynamic) is a bias removed by indexing, and because the tilt moves "
               "with rpm, a magnitude change needs a small phase correction.")
    vm = D["vector_map"]
    rows64 = []
    for i, r in enumerate(vm):
        side = "vertical" if r["phase_command_deg"] == 0 else (
            f"{abs(r['resultant_direction_deg']):.0f} deg "
            f"{'left' if r['resultant_direction_deg'] < 0 else 'right'} of vertical")
        rows64.append([str(i + 1), "0 deg", "40 deg", f"{r['phase_command_deg']:+.0f} deg",
                       f"{r['resultant_N']:.1f} N",
                       f"{side}: {r['vertical_force_N']:.2f} N up, "
                       f"{r['lateral_force_N']:+.2f} N lateral"])
    rep.fill_grid(tb[16], 1, rows64)
    rep.image_cell(tb[16], figs["fig-vector-map"],
                   "Figure 7. Thrust vector map. The flat 17.0 N magnitude is the model's "
                   "symmetry, not a measured result. At zero command the resultant sits 9.078 "
                   "deg off the offset direction.")

    # 7.1
    mn = [c for c in D["drive_candidates"] if c["selected"]][0]
    rep.fill_rows(tb[17], {
        "Motor manufacturer / model": ["T-Motor Antigravity MN5006 KV450"],
        "KV rating": ["450 rpm/V"],
        "Operating voltage": [f"8S pack: {g('performance.pack_voltage_nominal_V')} V nominal, "
                              f"{g('performance.pack_voltage_loaded_V')} V loaded, "
                              f"{g('performance.pack_voltage_charged_V')} V charged. The windings "
                              f"see {g('performance.motor_terminal_voltage_V')} V at the design "
                              f"point, inside the 4-6S catalogue window of 25.2 V"],
        "Rated / maximum current": [f"{mn['peak_current_180s_A']} A for 180 s; "
                                    f"{mn['continuous_current_A']} A continuous after the 0.80 "
                                    f"derate; {g('performance.motor_input_current_A')} A at the "
                                    f"design point"],
        "Maximum power": [f"{mn['max_power_180s_W']:.0f} W for 180 s; "
                          f"{mn['continuous_power_W']:.0f} W derated continuous; "
                          f"{P_MOTOR_IN:.1f} W at the design point"],
        "Motor mass": [f"{mn['mass_g']:.0f} g with cable"],
        "Selection basis": ["The only one of 5 screened motors that holds power, torque "
                            f"({g('performance.motor_torque_Nm')} of {mn['continuous_torque_Nm']} "
                            f"Nm), current and speed ({g('performance.motor_rpm'):.0f} of "
                            f"{g('performance.motor_speed_ceiling_rpm'):.0f} rpm) at once, all "
                            f"on continuous ratings"],
        "Pitch actuator model": ["Digital metal gear servo, 20 g class, from a supplier listing. "
                                 "The exact part is fixed against a datasheet in Stage 2"],
        "Pitch actuator rating": [f"3.9 kgf cm ({g('pitch.servo_stall_torque_Nm')} Nm) stall at "
                                  f"6 V; slew {g('pitch.slew_time_s')} s over the range"],
        "Pitch actuator mass": ["20.0 g each, 40.0 g for 2"],
    })

    # 7.2
    groups = {r[0]: r for r in mass_groups()}
    rep.fill_rows(tb[18], {
        "Motor": ["T-Motor MN5006 KV450", "106.0 g", "650 W, 26 A for 180 s",
                  "Datasheet; holds the design point continuously"],
        "ESC": ["40 A 8S class brushless ESC", "19.5 g", "40 A, 8S",
                "Above the 19.29 A design current and the 33.6 V charged pack"],
        "Pitch actuator": ["2 x 20 g digital metal gear servo", "40.0 g", "0.3825 Nm stall",
                           f"Margin {g('pitch.servo_torque_margin')} on the carrier ripple"],
        "Bearings": ["2 x 61802 main, 12 x 693ZZ pitch, 2 x MR128ZZ carrier",
                     f"{groups['Bearings'][3]:.1f} g",
                     f"693ZZ C0 {g('structure.pitch_bearing_c0_iso_N')} N by ISO 76",
                     "Pitch bearings duplexed, 4 per blade, for the centrifugal pull"],
        "Shaft": ["CFRP tube 16 x 1.5 mm, 340 mm, bonded 7075-T6 plugs",
                  f"{groups['Shaft'][3]:.1f} g", f"{g('structure.shaft_allowable_Nm')} Nm torsion",
                  f"Torsion margin {g('structure.shaft_margin'):.2f}"],
        "Controller / electronics": ["Matek F411-WSE class board, plus a step down regulator "
                                     "42 V in, 12 V out", "18.5 g",
                                     "Board 6-30 V input", "The 8S pack exceeds the board's "
                                     "30 V, so the regulator is required"],
        "Other": ["HTD-3M belt, 16 and 68 tooth pulleys, 4.25:1, tensioner",
                  f"{groups['Transmission'][3]:.1f} g", "efficiency 0.93 assumed",
                  f"The rotor needs {Q_ROTOR:.3f} Nm; the motor gives {g('performance.motor_torque_Nm')}"],
    })

    # 7.3
    rep.fill_rows(tb[19], {
        "Estimated aerodynamic power": [f"{P_AERO:.1f}"],
        "Estimated shaft power": [f"{P_SHAFT:.1f}"],
        "Estimated electrical power": [f"{P_MODULE:.1f} (module); {P_ESC_IN:.1f} at the ESC"],
        "Estimated maximum current": [f"{g('performance.motor_input_current_A'):.2f} (motor, "
                                      f"design point)"],
        "Assumed motor efficiency": [f"{ETA['motor'] * 100:.0f}"],
        "Assumed mechanical efficiency": [f"{ETA['transmission'] * 100:.0f} (belt)"],
        "Assumed ESC efficiency": [f"{ETA['esc'] * 100:.0f}"],
    })
    rep.image_cell(tb[19], figs["fig-powerflow"],
                   "Figure 8. Power flow at the design point, from the pack to the blades.")

    # 8.1
    rows81 = mass_groups()
    t20 = tb[20]
    other_idx = [i for i, r in enumerate(t20.rows) if Report.label(r.cells[0]) == "other"][0]
    trans = Report.add_row_after(t20, other_idx - 1)
    Report.cell(trans.cells[0], "Transmission", bold=True)
    for row in t20.rows[1:]:
        key = Report.label(row.cells[0])
        if key == "total":
            Report.cell(row.cells[1], "34 lines")
            Report.cell(row.cells[2], "-")
            Report.cell(row.cells[3], f"{M_NOM:.2f} g", bold=True)
            Report.cell(row.cells[4], f"Conservative column {M_CON:.2f} g (+"
                                      f"{(M_CON / M_NOM - 1) * 100:.1f}%)")
            continue
        match = [r for r in rows81 if r[0].lower() == key]
        assert match, key
        name, qty, unit, nom, con, basis = match[0]
        Report.cell(row.cells[1], qty)
        Report.cell(row.cells[2], unit)
        Report.cell(row.cells[3], f"{nom:.2f} g")
        Report.cell(row.cells[4], basis)
    p = rep.paragraph_after(t20._tbl)
    p.add_run().add_picture(str(figs["fig-mass"]), width=Mm(150))
    rep.paragraph_after(p._p, "Figure 9. Module mass by group, nominal and conservative. The full "
                              "34 line budget is in the supporting files.", italic=True, size=8)

    # 8.2
    rep.fill_rows(tb[21], {
        "Estimated maximum thrust": [f"{T:.1f} (design)"],
        "Estimated module mass": [f"{M_NOM / 1000:.5f}"],
        "Estimated module weight": [f"{W_N:.4f}"],
        "Estimated T/W ratio": [f"{TW:.4f}"],
        "Estimated uncertainty / confidence": [f"{TW_STACK:.2f} to {TW:.2f} across the four "
                                               f"cases below. Medium confidence"],
    })
    rep.answer("Basis of thrust estimate:",
               f"Blade area coefficient {g('performance.blade_area_coeff')} held below Kellen's "
               f"measured 0.6648 on this shape family, at {RPM:.0f} rpm (section 5.3). The low "
               f"case, {T_LOW:.4f} N, takes 5 percent off for blade flexibility, most of which is "
               f"the calculated {g('structure.blade_windup_deg')} deg torsional wind up.")
    rep.answer("Basis of mass estimate:", [
        "34 budget lines, each a drawn section, a catalogue part or a stated allowance, with "
        "growth by line class. It is not yet CAD mass properties or weighed parts.",
        f"Four cases are reported because they tell different stories. Design point: {T:.1f} N "
        f"on {M_NOM:.2f} g gives {TW:.4f}. Low coefficient alone: {TW_COEF:.4f}. Conservative "
        f"mass alone: {TW_MASS:.4f}. Both together: {TW_STACK:.4f}.",
        f"This is a preliminary pass with an open compliance risk. The design point clears 2.5 by "
        f"0.8 percent and the mass estimate isn't accurate to 0.8 percent. The conservative "
        f"column would have to lose {g('results.mass_to_close_stacked_g')} g for the worst case "
        f"to clear 2.5, so Stage 2 treats {g('results.mass_target_week4_g')} g on that column as "
        f"a gate and replaces the estimate with CAD mass properties, weighed parts and a thrust "
        f"test.",
    ])

    # 9.1
    rep.answer("Structural arrangement:",
               "Three sandwich blades pinned at both ends through root fittings and pitch "
               "bearings to clevis brackets on six CFRP spider arms, clamped to the CFRP shaft "
               "by two 7075-T6 split bosses. The shaft runs in two 61802 bearings in 7075-T6 "
               "blocks on four CFRP frame tubes, with the motor on a 7075-T6 plate below and four "
               "lugs to the airframe.")
    rep.answer("Critical load-bearing components:",
               f"The blade in combined centrifugal and aerodynamic bending; the root fittings and "
               f"pitch bearings, which carry {g('structure.centrifugal_load_N')} N of centrifugal "
               f"pull per blade; the pitch horn at {g('structure.pitch_link_load_N')} N of link "
               f"force; the rotor shaft at {Q_ROTOR:.3f} Nm plus a "
               f"{g('structure.shaft_side_load_N')} N belt side load.")
    rep.answer("Principal load paths:", [
        "Centrifugal: blade, root fittings, pitch bearings, root brackets, spider arms, hub boss.",
        "Thrust and reaction torque: hub boss, shaft, main bearings, bearing blocks, frame "
        "tubes, 4 mount lugs.",
        "Pitch control: horn, pitch link, offset post, carrier bearings, frame.",
    ])

    # 9.2
    rep.fill_rows(tb[22], {
        "Blade": ["PMI foam core, 2 ply carbon twill skin, CFRP spar",
                  f"{g('structure.blade_combined_Nm')} Nm combined bending "
                  f"({g('structure.blade_combined_overspeed_Nm')} at 1.20 overspeed)",
                  f"{BLADE_STRESS:.1f} MPa, skin",
                  f"{g('structure.blade_wrinkle_stress_MPa'):.1f} MPa, skin wrinkling",
                  f"{g('structure.blade_combined_margin'):.2f} "
                  f"({g('structure.blade_combined_margin_overspeed'):.2f} at overspeed)"],
        "Shaft": ["CFRP tube 16 x 1.5 mm",
                  f"{Q_ROTOR:.3f} Nm torque + {g('structure.shaft_bending_Nm'):.3f} Nm bending",
                  f"{SHAFT_STRESS:.2f} MPa combined shear", f"{CFRP_TAU_MPA:.0f} MPa shear",
                  f"{g('structure.shaft_combined_margin'):.2f}"],
        "Frame": ["CFRP tubes, 7075-T6 blocks and lugs", "worst lug about 13.4 N",
                  "not computed", "5.8 kN lug net section",
                  "over 100; stiffness governs, not strength"],
        "Hub": ["7075-T6 boss, 693ZZ root bearings",
                f"{g('structure.centrifugal_load_N')} N per blade "
                f"({g('structure.centrifugal_load_overspeed_N')} at overspeed)",
                "load check on bearing rating",
                f"{g('structure.blade_attachment_allowable_N')} N (4 bearings, ISO 76)",
                f"{g('structure.blade_attachment_margin'):.2f} "
                f"({g('structure.blade_attachment_margin_overspeed'):.2f} at overspeed)"],
        "Pitch linkage": ["7075-T6 horn, CFRP link", f"{g('structure.pitch_link_load_N')} N",
                          f"{HORN_STRESS:.1f} MPa, horn", f"{AL7075_MPA:.0f} MPa (7075-T6)",
                          f"{g('structure.pitch_link_margin'):.2f}"],
    })
    rep.answer("Calculation methodology:", nth=1, texts=
               f"Closed form, in tools/structure.py. Beam bending on the blade section integrated "
               f"from its own ordinates (EI {g('structure.blade_ei_Nm2')} Nm2, GJ "
               f"{g('structure.blade_gj_Nm2')} Nm2), with the skin wrinkling stress 0.5 x "
               f"(E_skin E_core G_core)^(1/3). Thin wall torsion and combined shear on the shaft, "
               f"net section bending on the horn, and the ISO 76 static rating for the bearings. "
               f"FOS is allowable over demand. Stresses in the table are the demand scaled onto "
               f"the governing allowable.")
    rep.answer("Principal assumptions:",
               "Blade load factor 4.0 on the mean aerodynamic force; a 1.20 overspeed case; "
               "published class allowables with no coupon; a floor of 1.5 on every margin.")
    rep.answer("Critical loading condition:",
               f"1.20 overspeed, about {RPM * 1.2:.0f} rpm, with the 4.0 aerodynamic peak on "
               f"top: blade combined bending {g('structure.blade_combined_overspeed_Nm')} Nm, FOS "
               f"{g('structure.blade_combined_margin_overspeed'):.2f}, the lowest in the module.")
    rep.answer("Preliminary conclusion:",
               f"All eight computed margins clear 1.5 and the two lowest are both overspeed "
               f"cases. Centrifugal pull, {g('structure.centrifugal_load_N')} N per blade, is 9.2 "
               f"times the mean aerodynamic force, so this rotor is a centrifugal machine first. "
               f"Not yet analysed: the bonded root joint itself, fatigue, the shaft's critical "
               f"speed and stress concentrations. Those are Stage 2 FEA and coupon work.")

    # 10.1
    rep.fill_rows(tb[23], {
        "Blade": ["PMI foam (Rohacell 51 IG class) core, 2 plies of 60 gsm carbon twill",
                  "Foam 52 kg/m3, E 70 MPa, G 19 MPa; skin E 60 GPa",
                  "Skin wrinkling over the core sets the blade allowable, so the foam is "
                  "structural; light enough to keep centrifugal load down"],
        "Frame": ["CFRP tube, 8 mm OD; 7075-T6 blocks and lugs",
                  "CFRP E 130 GPa, 1550 kg/m3; 7075-T6 400 MPa, 2810 kg/m3",
                  "Stiffness per gram for the tubes; machinable bores for the blocks"],
        "Shaft": ["Roll wrapped CFRP tube with bonded 7075-T6 plugs",
                  "Shear allowable 55 MPa, 1550 kg/m3",
                  "Torsion margin 16.18 at 36 g; metal only at the journals"],
        "Hub": ["7075-T6 split boss, CFRP spider arms", "400 MPa, 2810 kg/m3",
                "Clamps on the tube without crushing it; carries the root brackets"],
        "Pitch mechanism": ["6061-T6 carrier ring and sector gear; 693ZZ and MR128ZZ bearings",
                            "240 MPa, 2700 kg/m3", "Stiffness parts, easy to machine and "
                            "gear cut"],
        "Linkages": ["CFRP tube 4 mm OD pitch links with rod ends; 7075-T6 horns",
                     "7075-T6 400 MPa", "The horn governs the link path at FOS 3.29"],
    })

    # 10.2
    rep.fill_rows(tb[24], {
        "Blade": ["CNC profiled foam halves with the spar channel cut; 2 plies wet laid in a "
                  "machined two part mould, vacuum bagged, room temperature cure; 7075-T6 root "
                  "fittings bonded and pinned",
                  "Mould quality and blade mass matched within 0.5 g across the set"],
        "Frame": ["CFRP tubes cut to length; bearing blocks CNC milled with both bores in one "
                  "setup; bolted", "Bearing bore alignment, 0.010 mm"],
        "Shaft": ["Plugs bonded into the tube first, then both journals ground in one setup",
                  "Journal run out under 0.02 mm; grinding after bonding keeps them concentric"],
        "Hub": ["Turned and milled 7075-T6 boss, reamed bore; spider arms CNC routed from 1.5 mm "
                "CFRP plate", "Bore to shaft 0.015 mm; clamp without crushing the tube"],
        "Pitch mechanism": ["Turned 6061-T6 carrier and sector gear, gear teeth cut as job work; "
                            "CNC 7075-T6 horns and post; rod ends bought",
                            "Backlash 0.05 mm; pitch checked against the solved schedule at 12 "
                            "azimuths"],
    })
    rep.answer("Expected manufacturing constraints:",
               "The PMI foam is a 4 week import with no Indian stockist, and it gates the build, "
               "so it is ordered first. The gear pair is the only job needing a cutter a local "
               "shop won't keep, and at a quantity of one it is priced by setup. Two joints, the "
               "shaft plugs and the blade root, can't be reworked once cured.")
    rep.answer("Availability of materials/components:",
               f"Motor, servos, bearings, belt, ESC and CFRP tube are stocked by Indian "
               f"distributors. The bill of materials totals "
               f"{g('results.bom_total_inr'):,} INR ({g('results.bom_bought_inr'):,} bought parts "
               f"and material, {g('results.bom_tooling_inr'):,} tooling and fabrication), at "
               f"distributor list prices. Nothing has been quoted yet.")
    rep.answer("Preliminary assembly approach:",
               "Bond the shaft plugs and grind the journals; build and weigh the 3 blades; mate "
               "the spiders to the shaft and hang the blades on their pitch bearings; fit the "
               "main bearings and blocks to the frame and drop the rotor in; fit the carrier, "
               "offset post and pitch links, setting link lengths against the schedule; then "
               "motor, pulleys and belt, tensioned last; then ESC, controller, servos and "
               "harness. Before any spin: blade masses matched, run out measured, pitch checked "
               "at 12 azimuths, a static pull on one attachment above 301 N, and a first spin in "
               "four steps with current logged.")

    # 11
    rep.image_cell(tb[25], figs["fig-arrangement"],
                   "Figure 10. System layout (same drawing as Figure 1). No CAD model exists at "
                   "Stage 1; every dimension here is solved in the scripts and CAD is Stage 2 "
                   "item 1.")
    rep.fill_rows(tb[26], {
        "Overall length": ["364.4 (along the rotor axis)"],
        "Overall width": ["316.5"],
        "Overall height": ["362.5 (includes the 46 mm motor stack)"],
        "Rotor diameter": ["220.0 (296.5 swept)"],
        "Rotor width": ["290.4"],
        "Mounting dimensions": ["4 lugs on a 320 x 240 pattern"],
        "Motor envelope": ["46 axial stack below the rotor, on the drive end plate"],
        "Actuator envelope": ["Non-drive end: 16 axial phasing carrier bay; 2 servo cases on "
                              "the frame, not yet dimensioned"],
    })
    rep.fill_rows(tb[27], {
        "Motor arrangement": ["One outrunner under the rotor at the drive end, belt up to a 68 "
                              "tooth rotor pulley"],
        "Bearing arrangement": ["2 x 61802 on the shaft end plugs in 7075-T6 blocks; 12 x "
                                "693ZZ at the blade roots; 2 x MR128ZZ carrying the carrier"],
        "Pitch mechanism": ["All at the non-drive end: offset post from the phasing carrier, "
                            "3 pitch links to the horns"],
        "Actuator arrangement": ["2 servos 180 deg apart on sector gears, outside everything "
                                 "that rotates"],
        "Mounting interface": ["4 lugs in the plane of the rotor axis. 4 rather than 3 because "
                               f"the airframe sees {Q_ROTOR:.3f} Nm of steady reaction torque"],
        "Potential interference": [f"The pitch links pass {g('pitch.axis_keepout_mm')} mm from "
                                   f"the rotor axis, so nothing coaxial may sit in that plane. "
                                   f"Blade sweep annulus 86.92 to 148.25 mm kept clear. "
                                   f"Neighbour clearance {g('pitch.neighbour_clearance_mm')} mm"],
        "Assembly considerations": ["Bonded joints first, then rotor into frame, mechanism, "
                                    "drive and electronics last"],
        "Maintenance/accessibility": ["Carrier and servos come off the non-drive end without "
                                      "disturbing the rotor; belt reachable at the drive end; "
                                      "each blade comes out once its link is unpinned"],
        "Critical dimensions/tolerances": ["Journal run out 0.02 mm; bearing bores 0.010 mm; "
                                           "pitch link free length 0.05 mm; gear backlash 0.05 mm"],
    })

    # 12.1
    rep.fill_grid(tb[28], 1, [
        ["Thrust below 17.0 N", "Transferred coefficient wrong for this rotor; high inflow "
         f"ratio {g('performance.inflow_ratio')}", "T/W under 2.5; 10 N still met at 16.15 N",
         "Medium", "High", "Transient CFD, then a load cell run"],
        ["Mass growth", "Wet layup blades come out heavy; undrawn frame parts use up the 15 g "
         "reserve", "T/W under 2.5 (margin is 0.8%)", "High", "High",
         f"CAD mass properties, weighed parts, {g('results.mass_target_week4_g')} g gate"],
        ["Motor overheats in continuous running", "0.80 derate has no source; motor at 93% of "
         "it", "Lower thrust or a heavier motor", "Medium", "Medium",
         "Dynamometer run at working current, early in Stage 2"],
        ["Pitch bearing wear (false brinelling)", "80 deg oscillation, balls never recirculate "
         "(ratio 0.5533)", "Pitch play, loss of schedule", "Medium", "Medium",
         "Run to failure at speed on the flight grease"],
        ["Side force larger than modelled", "Quasi steady model; measured 10 to 35 deg on "
         "similar rotors", "About a fifth of vectoring authority lost", "High", "Low",
         "Index carrier zero; load cell calibration across speed"],
        ["Blade root joint failure", f"{g('structure.centrifugal_load_overspeed_N')} N through a "
         "bonded joint not yet qualified", "Blade release", "Low", "High",
         "Bond shear coupons, static pull above 301 N before any spin, spin behind a guard"],
        ["Foam supply delay", "4 week import, no Indian source", "Build slips", "Medium",
         "Medium", "Order first; fallback is a thicker skin and a rerun"],
    ])

    # 12.2
    rep.numbered(1, [
        "Does the transferred coefficient hold on this rotor at inflow ratio 0.3871? Transient "
        "CFD and a load cell run.",
        "How large is the real side force, and how does it move with rpm? It sets usable "
        "vectoring authority.",
        "What life do the 693ZZ pitch bearings have in 80 deg oscillation at 39 Hz?",
        "How strong is the bonded blade root in shear, peel and 3 per rev fatigue?",
        "Where is the shaft's first bending mode against 2337 rpm, and does the MN5006 hold its "
        "rating at the 8S duty?",
    ])

    # 13.1
    rep.fill_grid(tb[29], 1, [
        ["V1", "29-31 Aug 2026", "Geometry frozen: R 110 mm, 3 blades, 18 N design, 6S pack, "
         "3.5:1 belt", "Kellen's shape family and the week 2 radius sweep",
         "580.05 g, T/W 3.1633 design, 2.2525 stacked"],
        ["V2", "1 Sep 2026", "Figure of merit corrected 0.6 to 0.5215; design 17 N; pack 8S; belt "
         "4.25:1; 20 g servos; four-bar 18 x 108 mm; pitch bearings doubled; six mass lines "
         "redrawn", "FM must scale with the lowered coefficient; at 6S the motor capped at 392 W "
         "against 406 W needed", "677.91 g, T/W 2.5563 design, 2.1569 stacked"],
        ["V3", "4 Sep 2026", "10 g step down regulator added for the pitch controller",
         "The controller is rated 6 to 30 V and a charged 8S pack reaches 33.6 V",
         f"{M_NOM:.2f} g, T/W {TW:.4f} design, {TW_STACK:.4f} stacked"],
    ])

    # 13.2
    t30 = tb[30]
    dec = {1: ["Design thrust and pack voltage after the power correction",
               "Keep 18 N on a bigger motor; drop thrust on the same motor; raise the pack "
               "voltage",
               "17 N on the MN5006, 8S pack, 4.25:1 belt",
               "Output power a motor can give is capped at the speed rule x loaded pack voltage x "
               "continuous current, and KV cancels, so gearing can't move it. 8S lifts the cap; "
               "17 N is where every drive line keeps 7% or better",
               "At 8S the cap is 532.4 W against 405.9 W wanted. Motor at 483.2 of 520 W, 19.29 of "
               "20.8 A, 0.3902 of 0.4414 Nm, 9932 of 12799 rpm"],
           2: ["Should the blade be chordwise balanced?",
               "Balance with nose ballast at the pitch axis; leave it unbalanced",
               "Leave it unbalanced",
               "Balancing lifts the pitch link margin from 3.29 to 6.20 but costs mass on a "
               "case that already misses",
               "Balancing takes the stacked T/W from 2.1221 to 2.0292; the unbalanced link path "
               "still clears at 3.29"]}
    block = 0
    k = 0
    for row in t30.rows:
        lab = Report.label(row.cells[0])
        if lab == "item":
            block += 1
            k = 0
            continue
        Report.cell(row.cells[1], dec[block][k])
        k += 1

    # 13.3
    rep.numbered(6, [
        "Thrust and the side force rest on a transferred coefficient and a quasi steady model. "
        "Nothing has been measured on this rotor.",
        "Mass is a line by line estimate, not CAD mass properties or weighed parts, and the "
        "pass at the design point is 0.8 percent.",
        "No CAD, FEA or CFD exists yet. Structure is closed form and the root joint, fatigue "
        "and rotor dynamics are not analysed.",
        "The efficiency chain and the motor derate are assumed, and the motor figure is the "
        "sensitive one.",
        "The team is three programmers. Fabrication and testing experience has to come from "
        "new members, a mentor or the workshop.",
    ])

    # 14
    refs = [
        ["Kellen, A. J. Performance Measurements on a UAV-Scale Cycloidal Rotor in Hover. MS "
         "thesis, Texas A&M University, 2019", "https://hdl.handle.net/1969.1/184958",
         "Shape family; coefficient 0.6648; FM 0.6; solidity and Reynolds bands; horn length"],
        ["Benedict, M. Fundamental Understanding of the Cycloidal-Rotor Concept for Micro Air "
         "Vehicle Applications. PhD dissertation, University of Maryland, 2010",
         "https://hdl.handle.net/1903/11257",
         "Coefficients 0.7211 and 0.8114; power loading 0.062 N/W; 10% tare; blade count"],
        ["Sirohi, J., Parsons, E. and Chopra, I. Hover performance of a cycloidal rotor for a "
         "micro air vehicle. J. American Helicopter Society, 2007", "journal article",
         "Side force angle, about 10 deg"],
        ["Xisto, C., Leger, J., Pascoa, J. et al. Parametric analysis of a large-scale cycloidal "
         "rotor in hovering conditions. J. Aerospace Engineering, 2016", "journal article",
         "Parametric context for blade number and pitch"],
        ["Runco, C. and Benedict, M. Design, development, and flight testing of a 70-gram micro "
         "quad-cyclocopter. Int. J. Micro Air Vehicles 15, 2023", "open access",
         "Module T/W benchmark; centrifugal to aerodynamic load ratio"],
        ["Shrestha, E., Benedict, M. et al. Understanding upward scalability of cycloidal rotors "
         "for large-scale UAS applications. JAHS 67(4), 2022", "journal article (summary read)",
         "Reynolds invariance; blade mass scaling"],
        ["Adams, Z., Benedict, M., Hrishikeshavan, V. and Chopra, I. Design, development, and "
         "flight test of a small-scale cyclogyro UAV utilizing a novel cam-based passive blade "
         "pitching mechanism. Int. J. Micro Air Vehicles 5(2), 2013", "journal article (summary "
         "read)", "Side force 15 to 35 deg"],
        ["Alsabri, A. A. M. et al. Independent effects of blade number and solidity on "
         "cyclorotor hover performance. Aerospace 13(9), 765, 2026",
         "https://doi.org/10.3390/aerospace13090765 (summary read)",
         "Peak to mean blade load 3 to 4"],
        ["T-Motor Antigravity MN5006 KV450 datasheet", "manufacturer datasheet (PDF)",
         "650 W / 26 A for 180 s, 106 g, 60 mOhm, 4-6S"],
        ["ISO 76, Rolling bearings: static load ratings", "standard",
         "693ZZ static rating, 216.985 N"],
    ]
    rep.fill_grid(tb[31], 1, [[str(i + 1)] + r for i, r in enumerate(refs)])

    # 15
    rep.fill_grid(tb[32], 1, [
        ["Claude (Anthropic), used through Claude Code",
         "Writing and checking the Python calculation scripts, drafting report text, reading "
         "and summarising sources, internal design reviews",
         "Extensive. Most of the calculation code and text was produced with it under the "
         "team's direction. Every number is recomputed by the scripts from one data file, and "
         "the team takes responsibility for all of it"],
        ["OpenAI Codex", "Independent audits of the report against the problem statement",
         "Several review rounds. Each finding was checked, then fixed or answered in the design "
         "record"],
        ["Python 3, NumPy, Matplotlib", "All calculations and figures", "Open source libraries"],
        ["Pandoc, XeLaTeX, Microsoft Word", "Document preparation", "Formatting only"],
    ])
    rep.fill_rows(tb[33], {"Team Leader:": [TEAM["leader"]], "Date:": [TEAM["date"]]})

    # 16
    rep.fill_rows(tb[34], {
        "Rotor diameter": ["220.0"], "Rotor width": ["290.4"], "Number of blades": ["3"],
        "Blade chord": ["72.6"], "Operating RPM": [f"{RPM:.0f}"],
        "Maximum blade pitch": [f"{PITCH_MAX:.2f}"], "Pitch amplitude": ["40"],
        "Maximum vectoring angle": ["+/-60"], "Estimated thrust": [f"{T:.1f}"],
        "Estimated torque": [f"{Q_ROTOR:.3f}"], "Estimated shaft power": [f"{P_SHAFT:.1f}"],
        "Estimated electrical power": [f"{P_MODULE:.1f}"],
        "Estimated module mass": [f"{M_NOM / 1000:.3f}"],
        "Estimated T/W ratio": [f"{TW:.4f}"],
        "Primary blade material": ["PMI foam core, carbon twill skin, CFRP spar"],
        "Primary frame material": ["CFRP tube and 7075-T6"],
        "Motor": ["T-Motor MN5006 KV450"],
        "Pitch actuator": ["2 x 20 g digital metal gear servo"],
    })
    rep.answer("Why is the proposed design expected to meet the 10 N thrust requirement?",
               f"Design thrust is {T:.1f} N on a coefficient held below the value measured on "
               f"this shape family, at a Reynolds number inside the measured band. Even with 5 "
               f"percent off for blade flexibility it is {T_LOW:.2f} N, 61 percent above the "
               f"requirement. The motor holds the design point on continuous ratings.")
    rep.answer("Why is the proposed design expected to achieve T/W > 2.5?",
               f"At the design point it does, at {TW:.4f}, but only by 0.8 percent, so we don't "
               f"claim it with confidence. The three downside cases fall to {TW_COEF:.2f}, "
               f"{TW_MASS:.2f} and {TW_STACK:.2f}. We publish the {g('results.mass_to_close_stacked_g')} g "
               f"that would close the worst case, and Stage 2 replaces the estimate with measured "
               f"mass and thrust before anything else. The routes to more margin are a measured "
               f"coefficient and a lower KV motor on more cells.")
    rep.numbered(11, [
        f"The blade area coefficient {g('performance.blade_area_coeff')} transfers to this rotor.",
        "The mass budget holds: 34 lines with growth by class, nothing yet weighed.",
        "The efficiency chain (0.93, 0.84, 0.95) and the 0.80 motor derate.",
    ])
    rep.numbered(14, [
        "Measured thrust and side force on this rotor.",
        "Measured module mass, starting from CAD mass properties.",
        "Strength and life of the bonded blade root and the oscillating pitch bearings.",
    ])
    rep.answer("Overall assessment of Stage 1 design readiness:",
               "Preliminary design closed on paper. Geometry, kinematics, loads, mass, power and "
               "cost are consistent with each other and recomputed from one file. It is not "
               "build ready: thrust to weight is an open compliance risk, and CAD, CFD, FEA and "
               "testing are the first Stage 2 work.")

    # Appendices
    app_a = rep.para("Attach detailed hand calculations, spreadsheet outputs, MATLAB/Python "
                     "calculations, or other supporting engineering calculations.")
    p = rep.paragraph_after(app_a._p,
                            "Supporting files in the zip, folder 03_Calculations: "
                            "stage-1/design/numbers.json holds every input and result; "
                            "tools/linkage.py solves the four-bar, the pitch schedule, the "
                            "aerodynamic loads and the vector map; tools/structure.py builds the "
                            "blade section, the margins and the mass budget. Both are plain "
                            "Python 3 with no third party packages. Running python "
                            "tools/linkage.py --write and then python tools/structure.py --write "
                            "regenerates numbers.json byte for byte. The 32 page detailed design "
                            "note in folder 02_Detailed_Design_Note carries every calculation in "
                            "prose.")
    q = rep.paragraph_after(p._p)
    q.add_run().add_picture(str(figs["fig-blade-load"]), width=Mm(150))
    rep.paragraph_after(q._p, "Figure A1. Blade force against azimuth on the solved pitch "
                              "schedule. Peak 14.4260 N against a mean of 5.6667 N.",
                        italic=True, size=8)
    app_b = rep.para("Attach additional CAD views, drawings, dimensions, and component layouts.")
    rep.paragraph_after(app_b._p,
                        "No CAD model exists at Stage 1. The dimensioned layout is Figure 1, the "
                        "blade section Figure 3 and the linkage Figure 5, all drawn from the same "
                        "numbers file. The packaging and interface definition is in "
                        "04_Design_Record/09-packaging-and-integration.md.")
    app_c = rep.para("Attach preliminary sketches, earlier design versions, calculation "
                     "iterations, design-review records, photographs, or other evidence of "
                     "design development.")
    rep.paragraph_after(app_c._p,
                        "Folder 04_Design_Record holds the design documents for each item, the "
                        "evidence ledger that grades every borrowed number, and the decision "
                        "log, 72 dated entries recording each change in section 13.1 and why it "
                        "was made.")
    app_d = rep.para("Attach additional papers, datasheets, technical reports, standards, and "
                     "other sources.")
    rep.paragraph_after(app_d._p,
                        "Not read and not used as evidence, listed for Stage 2: Ramsey, R. A., "
                        "Development and Flight Testing of a 25-Kilogram Quad-Cyclocopter, MS "
                        "thesis, Texas A&M, 2022; Heimerl, Halder, Benedict et al., Experimental "
                        "and Computational Investigation of a UAV-Scale Cycloidal Rotor in "
                        "Forward Flight, VFS 77th Annual Forum, which measured "
                        "instantaneous blade forces.")

    out_docx = HERE / f"{OUT_STEM}.docx"
    rep.doc.core_properties.author = TEAM["team_name"]
    rep.doc.core_properties.title = f"{TEAM['design_name']} Stage 1 report"
    rep.doc.save(str(out_docx))
    print("wrote", out_docx)
    return out_docx


def export_pdf(path):
    from docx2pdf import convert
    out = path.with_suffix(".pdf")
    convert(str(path), str(out))
    print("wrote", out)
    return out


if __name__ == "__main__":
    d = build()
    if "--no-pdf" not in sys.argv:
        export_pdf(d)
