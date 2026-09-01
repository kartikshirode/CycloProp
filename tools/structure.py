#!/usr/bin/env python3
"""Week 4 structure, material allowables and refined mass budget for CycloProp.

    python tools/structure.py              print the whole calculation
    python tools/structure.py --write      write it into stage-1/design/numbers.json
    python tools/structure.py --bom        print the costed BOM as a markdown table
    python tools/structure.py --balance    price the chordwise balance mass D43 left open

Run order matters when the blade section changes. `tools/linkage.py` imports the blade
build-up from here, so run `python tools/linkage.py --write` first to refresh the pitch
loads against the new blade, then `python tools/structure.py --write`, which reads the
pitch link load back.

The point of this file is the same as tools/linkage.py: every structural number and every
mass line in the submission comes out of a calculation somebody else can rerun, instead of
being typed into numbers.json and defended in prose. Geometry, speed and thrust are read
back from numbers.json, so the script cannot drift away from the frozen design.

Three things here are load bearing and easy to break.

The blade section is integrated numerically from the NACA 0020 ordinate polynomial, not
from a shape factor. Skin, spar and foam each contribute to EI about the chord axis, and
the skin sets the allowable because a 0.142 mm laminate over foam wrinkles long before the
fibre fails.

Centrifugal load is the big term. At 2405 rpm each blade pulls 220 N against a peak
aerodynamic 24 N, so the blade attachment and the blade bending case are both sized on it,
and the overspeed case is what actually decides them.

The mass budget lines carry the word "blade" only when they are blade mass. check.py
derives per-blade mass by summing every budget line whose item name contains "blade", so
"pitch bearings" may not be called "blade pitch bearings" without corrupting the
centrifugal load that follows from it.
"""

import argparse
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NUMBERS = ROOT / "stage-1" / "design" / "numbers.json"

G = 9.81

# --------------------------------------------------------------- materials
# density kg/m3, modulus Pa, allowable stress Pa. Allowables are ultimate figures with the
# process knockdown already in them, so the margin that comes out is a safety factor and
# not a second helping of the same conservatism.
MATERIALS = {
    "pmi_foam": {
        "name": "Rohacell 51 IG class PMI foam",
        "rho": 52.0, "E": 70e6, "Gm": 19e6, "sigma": 0.8e6,
        "note": "closed cell PMI at 52 kg/m3, the grade the week 2 blade line assumed"},
    "cf_twill": {
        "name": "2x2 carbon twill, 60 gsm, 2 plies in epoxy",
        "rho": 1550.0, "E": 60e9, "Gm": 4.0e9, "sigma": 400e6,
        "note": "balanced 0/90 laminate, 0.22 kg/m2 cured, 0.142 mm thick"},
    "cfrp_tube": {
        "name": "roll wrapped CFRP tube, unidirectional with a plus minus 45 outer ply",
        "rho": 1550.0, "E": 130e9, "Gm": 5.0e9, "sigma": 700e6, "tau": 55e6,
        "note": "spar, pitch links, rotor shaft and frame tubes all come from this stock"},
    "al7075": {
        "name": "7075-T6 aluminium",
        "rho": 2810.0, "E": 71.7e9, "sigma": 400e6, "tau": 230e6,
        "note": "machined fittings, brackets, horns, bosses and bearing housings"},
    "al6061": {
        "name": "6061-T6 aluminium",
        "rho": 2700.0, "E": 68.9e9, "sigma": 240e6,
        "note": "pulleys and the phasing carrier ring, where strength is not the driver"},
    "epoxy_paste": {
        "name": "Araldite 2011 class toughened epoxy paste",
        "rho": 1050.0, "sigma": 20e6, "tau": 8e6,
        "note": "structural bond lines, allowable is a quarter of the published lap shear"},
}

# Blade build, unchanged from the week 2 description in 02-rotor-sizing.md except that the
# root close-out is now two drawn fittings and a measured bond line rather than one lumped
# allowance.
FOAM_FILL = 0.88               # fraction of the section the core fills
SKIN_AREAL_KG_M2 = 0.22
SKIN_THICK_M = 0.22 / 1550.0   # cured laminate thickness that areal mass implies
SPAR_DIA_FRAC = 0.12           # spar tube outer diameter as a fraction of chord
SPAR_WALL_M = 0.0005
ROOT_FITTING_OD_M = 0.014
ROOT_FITTING_LEN_M = 0.010
BOND_LINE_G_PER_BLADE = 1.35

# Bearings and catalogue hardware. Masses and ratings are supplier listings, the same
# evidence class as four of the five week 2 motor rows.
PITCH_BEARING = {"name": "693ZZ, 3 by 8 by 4 mm", "mass_g": 1.30, "c0_N": 270.0,
                 "bore_mm": 3.0, "od_mm": 8.0, "ball_mm": 1.5875, "balls": 7}

# The pitch bearing does not rotate. It swings through pitch_bearing_travel_deg once per
# revolution under a centrifugal pull whose direction is fixed in the arm, which is the
# textbook false brinelling arrangement and a static rating says nothing about it. The
# duty is worked out in bearing_duty() rather than assumed away.
PITCH_BEARING_S0_FLOOR = 2.0
BALL_FRICTION_MU = 0.0015
PLAIN_LINER_MU = 0.08
CARRIER_BEARING = {"name": "MR128ZZ, 8 by 12 by 3.5 mm", "mass_g": 2.20, "c0_N": 620.0}
MAIN_BEARING = {"name": "61802, 15 by 24 by 5 mm", "mass_g": 8.00, "c0_N": 2320.0}
ROD_END = {"name": "M3 aluminium bodied ball rod end", "mass_g": 1.60, "static_N": 600.0}

# Pitch horn section, sized here rather than assumed: the horn is the weakest link in the
# pitch load path and it is what decides whether the blade has to be balanced.
HORN_WIDTH_M = 0.008
HORN_THICK_M = 0.004

# Pitch link tube.
LINK_OD_M = 0.004
LINK_WALL_M = 0.0005

# Rotor shaft. D40 stops it inboard of the pitch plane and drives it from one end, so it
# cannot be carried out to an outboard bearing on the mechanism side.
SHAFT_OD_M = 0.016
SHAFT_WALL_M = 0.0015
SHAFT_LEN_M = 0.340
SHAFT_PLUG_DRIVE_LEN_M = 0.030
SHAFT_PLUG_CARRIER_LEN_M = 0.020
PULLEY_OVERHANG_M = 0.030      # drive bearing to belt pulley mid plane
BELT_SHAFT_LOAD_FACTOR = 1.4   # HTD shaft load against effective tension

# Belt drive, 3.5 to 1 on HTD-3M.
MOTOR_TEETH = 16
ROTOR_TEETH = 56
BELT_PITCH_MM = 3.0
BELT_WIDTH_MM = 9.0
BELT_LEN_MM = 300.0
BELT_G_PER_100MM = 3.4

# Spider arms, six of them, one per blade end.
ARM_W_M = 0.014
ARM_T_M = 0.0015

OVERSPEED = 1.20               # declared overspeed on rotor speed
GEAR_BACKLASH_M = 0.00005      # tooth backlash used to bound the carrier phase jitter


def naca_half_thickness(x, t=0.20):
    """Half thickness of a symmetric 4 digit section at chord fraction x."""
    return 5 * t * (0.2969 * math.sqrt(x) - 0.1260 * x - 0.3516 * x * x
                    + 0.2843 * x ** 3 - 0.1015 * x ** 4)


def section_properties(chord_m, n=2000):
    """Integrate the NACA 0020 section once and hand back everything the blade needs.

    Areas and second moments are per unit span. `i_chord` is bending about the chord line,
    which is the axis the aerodynamic and centrifugal loads both bend the blade about, and
    it is the weak one. `skin_y2_ds` is the shell integral the skin's stiffness comes from,
    kept separate so the skin thickness can change without redoing the geometry."""
    area = 0.0
    i_chord_solid = 0.0        # I of the filled section about the chord line
    skin_len = 0.0
    skin_y2_ds = 0.0
    y_max = 0.0
    prev = None
    for i in range(n + 1):
        x = i / n
        yt = naca_half_thickness(x) * chord_m
        xs = x * chord_m
        y_max = max(y_max, yt)
        if prev is not None:
            dx = xs - prev[0]
            ym = 0.5 * (yt + prev[1])
            area += 2.0 * ym * dx
            # I about the chord line for the strip, 2 * y^3 / 3
            i_chord_solid += (2.0 / 3.0) * (0.5 * (yt ** 3 + prev[1] ** 3)) * dx
            ds = math.hypot(dx, yt - prev[1])
            skin_len += 2.0 * ds
            skin_y2_ds += 2.0 * (0.5 * (yt * yt + prev[1] * prev[1])) * ds
        prev = (xs, yt)
    return {"area_m2": area, "i_chord_solid_m4": i_chord_solid,
            "perimeter_m": skin_len, "skin_y2_ds_m3": skin_y2_ds, "y_max_m": y_max}


def tube(od_m, wall_m):
    """Area, second moment and polar second moment of a thin walled circular tube."""
    id_m = od_m - 2 * wall_m
    a = math.pi / 4.0 * (od_m ** 2 - id_m ** 2)
    i = math.pi / 64.0 * (od_m ** 4 - id_m ** 4)
    return {"area_m2": a, "i_m4": i, "j_m4": 2 * i, "id_m": id_m}


def blade(chord_m, span_m):
    """Blade masses, stiffnesses and allowable bending moment, from the section up."""
    sec = section_properties(chord_m)
    foam = MATERIALS["pmi_foam"]
    skin = MATERIALS["cf_twill"]
    spar_mat = MATERIALS["cfrp_tube"]
    al = MATERIALS["al7075"]

    m_foam = sec["area_m2"] * FOAM_FILL * span_m * foam["rho"] * 1000.0
    m_skin = sec["perimeter_m"] * span_m * SKIN_AREAL_KG_M2 * 1000.0
    spar = tube(SPAR_DIA_FRAC * chord_m, SPAR_WALL_M)
    m_spar = spar["area_m2"] * span_m * spar_mat["rho"] * 1000.0

    fit = tube(ROOT_FITTING_OD_M, (ROOT_FITTING_OD_M - SPAR_DIA_FRAC * chord_m) / 2.0)
    m_fitting = fit["area_m2"] * ROOT_FITTING_LEN_M * al["rho"] * 1000.0
    m_close_out = 2 * m_fitting + BOND_LINE_G_PER_BLADE

    # Bending about the chord line. The foam is inside the skin, so its second moment is
    # the filled section's; the error from double counting the skin's own volume is under
    # a percent and it runs the safe way.
    i_skin = SKIN_THICK_M * sec["skin_y2_ds_m3"]
    i_foam = sec["i_chord_solid_m4"] * FOAM_FILL
    ei = skin["E"] * i_skin + spar_mat["E"] * spar["i_m4"] + foam["E"] * i_foam

    # Skin wrinkling over the foam is what limits the section, not fibre strength. The
    # classic sandwich result, 0.5 times the cube root of the three moduli.
    sigma_wrinkle = 0.5 * (skin["E"] * foam["E"] * foam["Gm"]) ** (1.0 / 3.0)
    sigma_skin = min(sigma_wrinkle, skin["sigma"])
    m_allow_skin = sigma_skin * ei / (skin["E"] * sec["y_max_m"])
    m_allow_spar = spar_mat["sigma"] * ei / (spar_mat["E"] * SPAR_DIA_FRAC * chord_m / 2.0)

    # Torsion, Bredt Batho on the single closed cell the skin makes.
    gj = 4.0 * sec["area_m2"] ** 2 * skin["Gm"] / (sec["perimeter_m"] / SKIN_THICK_M)

    return {
        "section": sec, "spar": spar,
        "m_foam_g": m_foam, "m_skin_g": m_skin, "m_spar_g": m_spar,
        "m_fitting_g": m_fitting, "m_close_out_g": m_close_out,
        "mass_g": m_foam + m_skin + m_spar + m_close_out,
        "ei_Nm2": ei, "gj_Nm2": gj,
        "sigma_wrinkle_Pa": sigma_wrinkle, "sigma_skin_Pa": sigma_skin,
        "m_allow_Nm": min(m_allow_skin, m_allow_spar),
        "m_allow_skin_Nm": m_allow_skin, "m_allow_spar_Nm": m_allow_spar,
    }


def build(data):
    """Everything week 4 computes, in one dictionary. Nothing here reads a week 4 number
    back out of numbers.json, so rerunning the script cannot confirm its own output."""
    geo, op, perf = data["geometry"], data["operating"], data["performance"]
    R = float(geo["radius_m"])
    chord = float(geo["chord_m"])
    span = float(geo["span_m"])
    nb = int(geo["blades"])
    rpm = float(op["rpm"])
    omega = rpm * 2 * math.pi / 60.0
    thrust = float(perf["thrust_N"])
    shaft_power = float(perf["aero_power_W"]) + float(perf["tare_power_W"])
    belt_ratio = float(perf["belt_ratio"])
    load_factor = 4.0                       # D16, the top of the published 3 to 4 range

    bl = blade(chord, span)
    al, al6, cfrp, epoxy = (MATERIALS["al7075"], MATERIALS["al6061"],
                            MATERIALS["cfrp_tube"], MATERIALS["epoxy_paste"])

    # ---------------------------------------------------------------- mass budget
    arm_g = ARM_W_M * ARM_T_M * R * cfrp["rho"] * 1000.0
    boss = tube(0.020, 0.003)
    boss_g = boss["area_m2"] * 0.016 * al["rho"] * 1000.0
    bracket_g = 3.00
    link_tube = tube(LINK_OD_M, LINK_WALL_M)
    link_g = link_tube["area_m2"] * float(data["pitch"]["pitch_link_m"]) * cfrp["rho"] * 1000.0
    horn_g = HORN_WIDTH_M * HORN_THICK_M * float(data["pitch"]["horn_m"]) * al["rho"] * 1000.0
    shaft = tube(SHAFT_OD_M, SHAFT_WALL_M)
    shaft_tube_g = shaft["area_m2"] * SHAFT_LEN_M * cfrp["rho"] * 1000.0
    plug_area = math.pi / 4.0 * (shaft["id_m"] - 0.0005) ** 2
    plug_g = plug_area * (SHAFT_PLUG_DRIVE_LEN_M + SHAFT_PLUG_CARRIER_LEN_M) * al["rho"] * 1000.0
    frame_tube = tube(0.008, 0.001)
    frame_tube_g = frame_tube["area_m2"] * 0.340 * cfrp["rho"] * 1000.0

    rotor_pd_mm = ROTOR_TEETH * BELT_PITCH_MM / math.pi
    motor_pd_mm = MOTOR_TEETH * BELT_PITCH_MM / math.pi
    # Rotor pulley as a rim, a lightened web and a hub, in 6061.
    rim = math.pi / 4.0 * ((rotor_pd_mm + 0.5) ** 2 - (rotor_pd_mm - 7.0) ** 2) * 10.0
    web = math.pi / 4.0 * ((rotor_pd_mm - 7.0) ** 2 - 24.0 ** 2) * 2.0 * 0.60
    hub = math.pi / 4.0 * (24.0 ** 2 - 16.0 ** 2) * 12.0
    rotor_pulley_g = (rim + web + hub) * al6["rho"] / 1e6
    motor_pulley_g = (math.pi / 4.0 * ((motor_pd_mm + 1.0) ** 2 - 5.0 ** 2) * 13.0
                      * al6["rho"] / 1e6)
    belt_g = BELT_LEN_MM / 100.0 * BELT_G_PER_100MM

    budget = [
        ("blade foam cores, 3 off", nb * bl["m_foam_g"], "blades", "calculated",
         f"{MATERIALS['pmi_foam']['name']} at {MATERIALS['pmi_foam']['rho']:.0f} kg/m3 "
         f"filling {FOAM_FILL:.0%} of the integrated NACA 0020 section over the "
         f"{span * 1000:.1f} mm span, three blades"),
        ("blade skins, 3 off", nb * bl["m_skin_g"], "blades", "calculated",
         f"two plies of 60 gsm carbon twill at {SKIN_AREAL_KG_M2} kg/m2 cured, over the "
         f"integrated section perimeter of {bl['section']['perimeter_m'] * 1000:.1f} mm, "
         f"three blades"),
        ("blade spar tubes, 3 off", nb * bl["m_spar_g"], "blades", "calculated",
         f"CFRP tube of {SPAR_DIA_FRAC * chord * 1000:.2f} mm outer diameter and "
         f"{SPAR_WALL_M * 1000:.1f} mm wall on the pitch axis, full span, three blades"),
        ("blade root close-outs, 3 blades", nb * bl["m_close_out_g"], "blades", "machined",
         f"two 7075-T6 root fittings per blade, {ROOT_FITTING_OD_M * 1000:.0f} mm outer "
         f"diameter over the spar and {ROOT_FITTING_LEN_M * 1000:.0f} mm long, plus "
         f"{BOND_LINE_G_PER_BLADE} g of paste adhesive at the spar and closure seams"),

        ("rotor spider arms, 6 off", 6 * arm_g, "rotor frame and hubs", "calculated",
         f"CFRP bar of {ARM_W_M * 1000:.0f} by {ARM_T_M * 1000:.1f} mm section over the "
         f"{R * 1000:.0f} mm rotor radius, two spiders of three arms"),
        ("rotor hub bosses, 2 off", 2 * boss_g, "rotor frame and hubs", "machined",
         "7075-T6 boss, 20 mm outer diameter, 14 mm bore, 16 mm long, clamping each "
         "spider to the shaft"),
        ("root attachment brackets, 6 off", 6 * bracket_g, "rotor frame and hubs", "machined",
         "7075-T6 clevis carrying the blade root fitting into the spider arm, sized on "
         "the recomputed centrifugal pull at the declared overspeed"),

        ("pitch bearings, 6 off", 6 * PITCH_BEARING["mass_g"], "pitch mechanism", "catalogue",
         f"{PITCH_BEARING['name']}, supplier listing, static rating "
         f"{PITCH_BEARING['c0_N']:.0f} N each, two per blade"),
        ("pitch links with rod ends, 3 off", nb * (link_g + 2 * ROD_END["mass_g"]),
         "pitch mechanism", "catalogue",
         f"CFRP tube of {LINK_OD_M * 1000:.0f} mm outer diameter and "
         f"{LINK_WALL_M * 1000:.1f} mm wall at the solved 105.0 mm length, with two "
         f"{ROD_END['name']}s per link"),
        ("pitch horns, 3 off", nb * horn_g, "pitch mechanism", "machined",
         f"7075-T6 arm of {HORN_WIDTH_M * 1000:.0f} by {HORN_THICK_M * 1000:.0f} mm "
         f"section at the 24.4 mm horn radius, thickness set by its own bending margin"),
        ("offset pivot post and pin", 6.50, "pitch mechanism", "machined",
         "7075-T6 post of 8 mm diameter reaching 40 mm from the phasing carrier to the "
         "common offset pivot, with the three link eyes and the pivot pin"),
        ("phasing carrier ring, 40 mm gear", 7.90, "pitch mechanism", "machined",
         "6061-T6 ring with an integral 40 mm pitch diameter gear, 3 mm web, running on "
         "the carrier bearings outboard of the rotor"),
        ("servo sector gear, 60 mm", 4.50, "pitch mechanism", "machined",
         "6061-T6 sector of a 60 mm pitch diameter gear, 2 mm face, spanning the 80 "
         "degrees of servo travel that the 1.5 step up turns into 120 of carrier"),
        ("carrier support bearings, 2 off", 2 * CARRIER_BEARING["mass_g"],
         "pitch mechanism", "catalogue",
         f"{CARRIER_BEARING['name']}, supplier listing, carrying the "
         f"{float(data['pitch']['carrier_radial_force_N']):.2f} N radial pull the "
         f"three pitch links put into the offset post"),

        ("rotor shaft tube", shaft_tube_g, "rotor shaft", "calculated",
         f"roll wrapped CFRP tube, {SHAFT_OD_M * 1000:.0f} mm outer diameter and "
         f"{SHAFT_WALL_M * 1000:.1f} mm wall, {SHAFT_LEN_M * 1000:.0f} mm long over the "
         f"span and the drive extension"),
        ("shaft end plugs, 2 off", plug_g, "rotor shaft", "machined",
         f"7075-T6 plugs bonded into the tube, {SHAFT_PLUG_DRIVE_LEN_M * 1000:.0f} mm at "
         f"the drive end and {SHAFT_PLUG_CARRIER_LEN_M * 1000:.0f} mm at the carrier end, "
         f"turned to the 15 mm bearing journals"),

        ("main bearings, 2 off", 2 * MAIN_BEARING["mass_g"], "main bearings", "catalogue",
         f"{MAIN_BEARING['name']} deep groove, supplier listing, one at each rotor "
         f"station on the shaft end plugs"),

        ("bearing blocks, 2 off", 16.00, "frame and mounting hardware", "machined",
         "7075-T6 housing, 34 by 28 by 9 mm with a 24 mm bore, bolted to the frame tubes "
         "and carrying the main bearings"),
        ("frame tubes, 4 off", 4 * frame_tube_g, "frame and mounting hardware", "calculated",
         "CFRP tube of 8 mm outer diameter and 1 mm wall, 340 mm long, spanning the "
         "packaged envelope between the two bearing blocks"),
        ("motor mount plate", 8.00, "frame and mounting hardware", "machined",
         "2.5 mm 7075-T6 plate, 55 by 45 mm with the belt slot and lightening cutouts, "
         "carrying the MN5006 and taking the belt reaction"),
        ("airframe mount lugs, 4 off", 7.20, "frame and mounting hardware", "machined",
         "7075-T6 lug at each of the four mount points named in the packaging document, "
         "1.8 g each"),
        ("frame and mount design reserve", 15.00, "frame and mounting hardware", "allowance",
         "unallocated hardware on the least developed group in the module: gussets, cable "
         "clamps, the servo bracket and the ESC tray, none of which is drawn yet"),

        ("motor, MN5006 KV450", 106.00, "motor", "catalogue",
         "T-Motor Antigravity MN5006 KV450 from the supplier datasheet, 106 g including "
         "leads, the only week 2 drive row read off a manufacturer sheet"),

        ("rotor belt pulley, 56 tooth", rotor_pulley_g, "transmission", "machined",
         f"6061-T6 HTD-3M pulley, {rotor_pd_mm:.1f} mm pitch diameter, 10 mm rim with a "
         f"lightened 2 mm web, on the shaft drive end"),
        ("motor belt pulley, 16 tooth", motor_pulley_g, "transmission", "machined",
         f"6061-T6 HTD-3M pulley, {motor_pd_mm:.1f} mm pitch diameter, giving the 3.5 to "
         f"1 ratio week 2 selected"),
        ("drive belt", belt_g, "transmission", "catalogue",
         f"HTD-3M toothed belt, {BELT_WIDTH_MM:.0f} mm wide and {BELT_LEN_MM:.0f} mm "
         f"long, supplier listing at {BELT_G_PER_100MM} g per 100 mm"),
        ("belt tensioner and bracket", 6.00, "transmission", "machined",
         "idler pulley on an eccentric bracket at the motor plate, setting belt "
         "pretension at build and holding it with one screw"),

        ("esc, 40 A 6S class", 19.50, "esc", "catalogue",
         "brushless controller rated above the 20.61 A the design point draws, supplier "
         "listing, 19.5 g with leads and heatshrink"),

        ("vectoring actuator servos, 2 off", 25.00, "vectoring actuator", "catalogue",
         "two Corona DS-929MG class digital metal gear servos at 12.5 g, supplier "
         "listing, driving the phasing carrier 180 degrees apart"),

        ("pitch offset controller", 8.50, "pitch offset controller", "catalogue",
         "Matek F411-WSE class flight controller board, supplier listing, 8.5 g against "
         "the 8.0 g week 2 carried, which is the debt week 3 left open"),

        ("module wiring harness", 15.60, "module wiring harness", "allowance",
         "14 AWG silicone power leads over 600 mm at 16 g/m, plus servo and signal "
         "wiring and the connectors at the module boundary"),

        ("fasteners and threaded inserts", 14.00, "fasteners and bonded joints", "allowance",
         "40 M3 screws, washers and threaded inserts at the frame, bearing block, motor "
         "plate and mount lug joints, 0.35 g average"),
        ("structural adhesive at module joints", 7.50, "fasteners and bonded joints",
         "allowance",
         f"{epoxy['name']} at the shaft plugs, bearing block bonds and bracket joints, "
         f"bond areas taken from the joint list"),
    ]

    # ------------------------------------------------------- conservative column
    # The rate is set by what the line's basis is, before the total is looked at. D33
    # bans a single growth rate picked after seeing the target, and the way to respect
    # that is to classify first.
    RATES = {"catalogue": 0.08, "machined": 0.12, "calculated": 0.15, "allowance": 0.25}

    rows = []
    for item, mass, refines, cls, basis in budget:
        rows.append({"item": item, "mass_g": round(mass, 2),
                     "conservative_g": round(mass * (1 + RATES[cls]), 2),
                     "basis": basis + f". Growth class {cls}, {RATES[cls]:.0%}",
                     "refines": refines})
    total = sum(r["mass_g"] for r in rows)
    total_cons = sum(r["conservative_g"] for r in rows)

    # ------------------------------------------------------------------ loads
    blade_mass_kg = sum(r["mass_g"] for r in rows if "blade" in r["item"].lower()) / 1000.0 / nb
    fc = blade_mass_kg * omega ** 2 * R
    fc_over = fc * OVERSPEED ** 2
    lever = span / 8.0                      # uniformly loaded, held at both spiders
    aero_peak_N = thrust / nb * load_factor
    m_aero = aero_peak_N * lever
    m_cf = fc * lever
    m_aero_over = aero_peak_N * OVERSPEED ** 2 * lever
    m_cf_over = fc_over * lever

    shaft_torque = shaft_power / omega
    motor_torque = shaft_power / (omega * belt_ratio * float(data["efficiency"]["transmission"]))

    shaft_allow = cfrp["tau"] * shaft["j_m4"] / (SHAFT_OD_M / 2.0)
    rotor_pulley_r = rotor_pd_mm / 2000.0
    belt_tension = shaft_torque / rotor_pulley_r
    shaft_side_load = belt_tension * BELT_SHAFT_LOAD_FACTOR
    shaft_bending = shaft_side_load * PULLEY_OVERHANG_M
    sigma_shaft = shaft_bending * (SHAFT_OD_M / 2.0) / shaft["i_m4"]
    tau_shaft = shaft_torque * (SHAFT_OD_M / 2.0) / shaft["j_m4"]
    tau_combined = math.hypot(sigma_shaft / 2.0, tau_shaft)

    # Pitch load path. The horn is the weakest element, so it sets the allowable and it is
    # what decides whether the unbalanced blade of D43 has to be balanced.
    horn_z = HORN_WIDTH_M * HORN_THICK_M ** 2 / 6.0
    horn_allow_N = al["sigma"] * horn_z / float(data["pitch"]["horn_m"])
    link_buckling_N = (math.pi ** 2 * cfrp["E"] * link_tube["i_m4"]
                       / float(data["pitch"]["pitch_link_m"]) ** 2)
    link_allow = min(horn_allow_N, ROD_END["static_N"], link_buckling_N)
    link_load = float(data["pitch"]["peak_link_force_N"])

    attach_allow = 2 * PITCH_BEARING["c0_N"]

    # Blade torsional wind up under the centrifugal pitching moment. The blade is driven
    # in pitch from one end only, so the far end lags, and that lag is a real part of the
    # blade flexibility loss the low thrust coefficient carries.
    blade_moment = float(data["pitch"]["peak_blade_moment_Nm"])
    windup_rad = blade_moment * span / (2.0 * bl["gj_Nm2"])

    # Bending deflection and aerodynamic twist at the week 3 peak blade load, which is the
    # same reference load week 2 used, so the two are comparable.
    peak_blade_N = thrust / nb * float(perf["blade_load_peak_to_mean"])
    tip_defl_m = 5.0 * peak_blade_N * span ** 3 / (384.0 * bl["ei_Nm2"])
    aero_moment = peak_blade_N * (float(geo["pitch_axis_pct_chord"]) - 25.0) / 100.0 * chord
    aero_twist_rad = aero_moment * span / (8.0 * bl["gj_Nm2"])

    # Carrier ripple. At 3 per revolution the servo loop cannot answer it, so the phase
    # jitter is bounded by gear backlash rather than by holding torque.
    jitter_deg = math.degrees(2 * GEAR_BACKLASH_M / (40.0 / 1000.0))

    return {
        "blade": bl, "rows": rows, "total_g": total, "total_cons_g": total_cons,
        "omega": omega, "blade_mass_kg": blade_mass_kg,
        "fc_N": fc, "fc_over_N": fc_over, "lever_m": lever, "load_factor": load_factor,
        "aero_peak_N": aero_peak_N, "m_aero_Nm": m_aero, "m_cf_Nm": m_cf,
        "m_aero_over_Nm": m_aero_over, "m_cf_over_Nm": m_cf_over,
        "shaft_torque_Nm": shaft_torque, "motor_torque_Nm": motor_torque,
        "shaft_allow_Nm": shaft_allow, "shaft": shaft,
        "belt_tension_N": belt_tension, "shaft_side_load_N": shaft_side_load,
        "shaft_bending_Nm": shaft_bending, "tau_combined_Pa": tau_combined,
        "horn_allow_N": horn_allow_N, "link_buckling_N": link_buckling_N,
        "link_allow_N": link_allow, "link_load_N": link_load,
        "attach_allow_N": attach_allow,
        "windup_deg": math.degrees(windup_rad),
        "tip_defl_mm": tip_defl_m * 1000.0,
        "aero_twist_deg": math.degrees(aero_twist_rad),
        "peak_blade_N": peak_blade_N,
        "jitter_deg": jitter_deg,
        "rotor_pd_mm": rotor_pd_mm, "motor_pd_mm": motor_pd_mm,
        "thrust_N": thrust, "shaft_power_W": shaft_power, "belt_ratio": belt_ratio,
        "nb": nb, "R": R, "span": span, "chord": chord,
    }


def bearing_duty(data, b):
    """Oscillating duty on the blade pitch bearings, which the static rating misses.

    Two things decide whether a swinging ball bearing wears out on its own contact spots
    instead of rolling onto fresh raceway. The first is how far the ball set travels. For
    a stationary outer ring the cage turns at (1 - d/Dm)/2 of the inner ring angle, so a
    generous 80 degrees of blade pitch moves the balls by less than 30. The second is the
    ball spacing, 360 over the ball count. When the cage swing falls short of the spacing
    every ball stays inside its own arc for the life of the machine, grease stops being
    dragged back into the contact, and the failure mode is false brinelling rather than
    fatigue.

    Both numbers come from catalogue geometry, so the ratio is computed and stored rather
    than argued. The ball count is the one soft input: 7 is the usual complement for this
    size and the conclusion survives 6 or 8, because the critical amplitude stays above
    120 degrees in all three cases and the mechanism only gives 80.

    Friction is the other half of the question, because it decides what the alternative
    costs. A deep groove ball bearing gives back roughly a tenth of a watt across all six.
    A PTFE fabric lined plain bearing, which is what an oscillating aerospace joint uses
    and is immune to the wear mode above, costs about fifty times that, and at 40 swings a
    second the sliding distance is what turns the trade around."""
    brg = PITCH_BEARING
    pitch_dia = (brg["bore_mm"] + brg["od_mm"]) / 2.0
    gamma = brg["ball_mm"] / pitch_dia
    cage_ratio = (1.0 - gamma) / 2.0
    travel = float(data["pitch"]["pitch_bearing_travel_deg"])
    cage_swing = cage_ratio * travel
    spacing = 360.0 / brg["balls"]
    # Full swing at which the cage carries every ball onto its neighbour's track.
    crit_travel = spacing / cage_ratio

    # Load per bearing at the operating point, not at the declared overspeed. Overspeed is
    # a strength case and it is already gated on the static rating. Wear is a duty case and
    # it accumulates at the speed the machine actually runs at.
    load_N = b["fc_N"] / 2.0
    s0 = brg["c0_N"] / load_N

    rev_hz = float(data["operating"]["rpm"]) / 60.0
    amp_rad = math.radians(travel / 2.0)
    omega = 2.0 * math.pi * rev_hz
    mean_rate = (2.0 / math.pi) * amp_rad * omega          # mean |dtheta/dt| over a cycle
    ball_torque = 0.5 * BALL_FRICTION_MU * load_N * brg["bore_mm"] / 1000.0
    plain_torque = PLAIN_LINER_MU * load_N * brg["bore_mm"] / 2000.0
    count = 2 * int(data["geometry"]["blades"])
    shaft_power = b["shaft_power_W"]
    return {
        "balls": brg["balls"],
        "ball_mm": brg["ball_mm"],
        "pitch_dia_mm": pitch_dia,
        "cage_ratio": cage_ratio,
        "cage_swing_deg": cage_swing,
        "ball_spacing_deg": spacing,
        "recirculation_ratio": cage_swing / spacing,
        "recirculation_travel_deg": crit_travel,
        "load_N": load_N,
        "s0": s0,
        "oscillation_hz": rev_hz,
        "sliding_mm_per_s": 4.0 * amp_rad * brg["bore_mm"] / 2.0 * rev_hz,
        "friction_W": count * ball_torque * mean_rate,
        "friction_frac": count * ball_torque * mean_rate / shaft_power,
        "plain_friction_W": count * plain_torque * mean_rate,
        "plain_friction_frac": count * plain_torque * mean_rate / shaft_power,
    }


def margins(b):
    return {
        "blade_margin": b["blade"]["m_allow_Nm"] / b["m_aero_Nm"],
        "blade_combined_margin": b["blade"]["m_allow_Nm"] / (b["m_aero_Nm"] + b["m_cf_Nm"]),
        "blade_combined_margin_overspeed":
            b["blade"]["m_allow_Nm"] / (b["m_aero_over_Nm"] + b["m_cf_over_Nm"]),
        "shaft_margin": b["shaft_allow_Nm"] / b["shaft_torque_Nm"],
        "shaft_combined_margin": MATERIALS["cfrp_tube"]["tau"] / b["tau_combined_Pa"],
        "pitch_link_margin": b["link_allow_N"] / b["link_load_N"],
        "blade_attachment_margin": b["attach_allow_N"] / b["fc_N"],
        "blade_attachment_margin_overspeed": b["attach_allow_N"] / b["fc_over_N"],
    }


# --------------------------------------------------------------------- costed BOM
# Priced 31 August 2026 in Indian rupees at distributor list level, from Indian
# distributors where one carries the part and from an importer's landed price where none
# does. Lead times are working weeks from order. Anything marked make is job work at a
# local shop against a drawing, so its cost is a shop rate rather than a catalogue price.
#
# These are indicative prices and not obtained quotations. No supplier was contacted and
# no listing was fetched, which is why the field is priced_date rather than quote_date and
# why the source column names the distributor a part would be bought from rather than one
# that has quoted for it. Confirming them is a Stage 2 task and it is carried as a debt.
PRICED_DATE = "31 August 2026"
BOM = [
    # (item, category, qty, unit_cost_inr, lead_weeks, make_or_buy, source)
    ("T-Motor Antigravity MN5006 KV450", "drive", 1, 8500, 3, "buy",
     "Quadkopters, New Delhi, manufacturer datasheet price"),
    ("40 A 6S brushless controller", "drive", 1, 3200, 2, "buy", "Robu.in, Pune"),
    ("Corona DS-929MG class servo", "drive", 2, 1450, 2, "buy", "Robu.in, Pune"),
    ("Matek F411-WSE class controller board", "drive", 1, 3900, 3, "buy",
     "Quadkopters, New Delhi"),
    ("693ZZ miniature bearing", "hardware", 6, 60, 1, "buy", "local bearing house, Mumbai"),
    ("MR128ZZ miniature bearing", "hardware", 2, 90, 1, "buy", "local bearing house, Mumbai"),
    ("61802 deep groove bearing", "hardware", 2, 240, 1, "buy", "local bearing house, Mumbai"),
    ("M3 aluminium bodied rod end", "hardware", 6, 180, 2, "buy", "Robu.in, Pune"),
    ("HTD-3M belt, 9 mm wide, 300 mm", "drive", 1, 420, 2, "buy", "Powergear, Coimbatore"),
    ("HTD-3M pulley blank, 16 tooth", "drive", 1, 650, 2, "buy", "Powergear, Coimbatore"),
    ("HTD-3M pulley blank, 56 tooth", "drive", 1, 1250, 2, "buy", "Powergear, Coimbatore"),
    ("Rohacell 51 IG block, 300 by 150 by 20 mm", "material", 1, 2600, 4, "buy",
     "importer landed price, no Indian stockist found"),
    ("60 gsm carbon twill, 1 m2", "material", 1, 1400, 2, "buy", "Composites Today, Chennai"),
    ("epoxy laminating resin and hardener, 500 g", "material", 1, 1600, 1, "buy",
     "Composites Today, Chennai"),
    ("Araldite 2011 paste adhesive, 50 ml", "material", 1, 950, 1, "buy",
     "Huntsman distributor, Mumbai"),
    ("CFRP tube stock, four diameters", "material", 1, 2900, 3, "buy",
     "Carbon Fiber India, Coimbatore"),
    ("7075-T6 bar and plate stock", "material", 1, 2200, 2, "buy", "metal stockist, Mumbai"),
    ("6061-T6 bar stock", "material", 1, 700, 1, "buy", "metal stockist, Mumbai"),
    ("M3 fasteners, washers and threaded inserts", "hardware", 1, 900, 1, "buy",
     "fastener stockist, Mumbai"),
    ("silicone wire, connectors and heatshrink", "hardware", 1, 800, 1, "buy", "Robu.in, Pune"),
    ("blade mould, two halves from tooling board", "tooling", 1, 9000, 3, "make",
     "CNC job work against the section drawing"),
    ("spider arms and root brackets, CNC job work", "fabricated", 1, 6500, 2, "make",
     "CNC job work, 7075 and CFRP plate"),
    ("bearing blocks and motor mount plate, CNC job work", "fabricated", 1, 4800, 2, "make",
     "CNC job work, 7075 plate"),
    ("carrier ring gear and servo sector gear", "fabricated", 1, 5500, 3, "make",
     "gear cutting job work, 6061"),
    ("rotor assembly and balancing jig", "tooling", 1, 3000, 2, "make",
     "aluminium extrusion and a dial indicator mount"),
]


def bom_rows():
    rows = []
    for item, cat, qty, unit, weeks, mob, source in BOM:
        rows.append({"item": item, "category": cat, "qty": qty,
                     "unit_cost_inr": unit, "line_cost_inr": qty * unit,
                     "lead_time_weeks": weeks, "make_or_buy": mob,
                     "source": source, "priced_date": PRICED_DATE})
    return rows


def bom_report():
    rows = bom_rows()
    print("| Item | Make or buy | Qty | Unit INR | Line INR | Lead | Likely source, "
          "priced " + PRICED_DATE + " |")
    print("| --- | --- | --- | --- | --- | --- | --- |")
    for r in rows:
        print(f"| {r['item']} | {r['make_or_buy']} | {r['qty']} | {r['unit_cost_inr']} | "
              f"{r['line_cost_inr']} | {r['lead_time_weeks']} wk | {r['source']} |")
    buy = sum(r["line_cost_inr"] for r in rows if r["make_or_buy"] == "buy")
    make = sum(r["line_cost_inr"] for r in rows if r["make_or_buy"] == "make")
    print()
    print(f"  bought parts and material {buy} INR")
    print(f"  tooling and fabrication   {make} INR")
    print(f"  total                     {buy + make} INR")
    print(f"  longest lead              {max(r['lead_time_weeks'] for r in rows)} weeks")
    return rows, buy, make


def balance_report(data, b):
    """What a chordwise balance mass would cost, which is the trade D43 handed week 4.

    The blade centre of mass sits aft of the pitch axis, so centrifugal force gives a
    steady moment that doubles the peak pitch link load. Moving the centre onto the axis
    means lead at the nose, and lead at the nose is module mass against a thrust to weight
    case that has no room in it."""
    cg_pct = float(data["pitch"]["blade_cg_pct_chord"])
    axis_pct = float(data["geometry"]["pitch_axis_pct_chord"])
    chord = b["chord"]
    nose_pct = 5.0                       # a balance slug cannot sit forward of this
    arm_cg = (cg_pct - axis_pct) / 100.0 * chord
    arm_nose = (axis_pct - nose_pct) / 100.0 * chord
    m_blade = b["blade_mass_kg"] * 1000.0
    m_bal = m_blade * arm_cg / arm_nose
    added = m_bal * b["nb"]
    nom = b["total_g"] + added
    cons = b["total_cons_g"] + added * 1.12
    tc = float(data["performance"]["thrust_N_conservative"])
    # The balanced link load comes from the solver, not from a ratio. An earlier version
    # scaled the unbalanced load by 0.655, which was the week 3 balanced-to-unbalanced
    # ratio on the week 2 blade, and it survived the blade changing underneath it. The
    # import is deferred because tools/linkage.py imports this module at load time.
    import linkage
    bal = linkage.solve(data, balanced=True)
    link_bal = bal["peak_link_force_N"]
    print()
    print("=== chordwise balance trade, D43 ===")
    print(f"  centre of mass at {cg_pct:.2f} pct chord, axis at {axis_pct:.1f}, "
          f"offset {arm_cg * 1000:.3f} mm")
    print(f"  balance slug at {nose_pct:.0f} pct chord needs {m_bal:.2f} g per blade, "
          f"{added:.2f} g for the set")
    print(f"  module goes {b['total_g']:.2f} -> {nom:.2f} g nominal, "
          f"{b['total_cons_g']:.2f} -> {cons:.2f} g conservative")
    print(f"  conservative T/W {tc / (b['total_cons_g'] / 1000.0 * G):.4f} -> "
          f"{tc / (cons / 1000.0 * G):.4f} against a hard limit of 2.5")
    print(f"  blade pitching moment would fall to {bal['peak_blade_moment_Nm']:.4f} Nm")
    print(f"  pitch link would fall to {link_bal:.2f} N, "
          f"margin {b['link_allow_N'] / link_bal:.2f} "
          f"against the {b['link_allow_N'] / b['link_load_N']:.2f} it already has")


def report(data):
    b = build(data)
    m = margins(b)
    bl = b["blade"]
    print("=== blade section ===")
    print(f"  section area        {bl['section']['area_m2'] * 1e6:9.2f} mm2")
    print(f"  perimeter           {bl['section']['perimeter_m'] * 1000:9.2f} mm")
    print(f"  half thickness      {bl['section']['y_max_m'] * 1000:9.3f} mm")
    print(f"  foam / skin / spar  {bl['m_foam_g']:.2f} / {bl['m_skin_g']:.2f} / {bl['m_spar_g']:.2f} g")
    print(f"  close out           {bl['m_close_out_g']:9.2f} g")
    print(f"  blade mass          {bl['mass_g']:9.2f} g")
    print(f"  EI                  {bl['ei_Nm2']:9.2f} Nm2")
    print(f"  GJ                  {bl['gj_Nm2']:9.2f} Nm2")
    print(f"  wrinkling stress    {bl['sigma_wrinkle_Pa'] / 1e6:9.1f} MPa")
    print(f"  allowable moment    {bl['m_allow_Nm']:9.2f} Nm "
          f"(skin {bl['m_allow_skin_Nm']:.2f}, spar {bl['m_allow_spar_Nm']:.2f})")
    print()
    print("=== loads ===")
    print(f"  per blade mass      {b['blade_mass_kg'] * 1000:9.2f} g")
    print(f"  centrifugal         {b['fc_N']:9.2f} N   overspeed {b['fc_over_N']:.2f} N")
    print(f"  aero peak per blade {b['aero_peak_N']:9.2f} N   lever {b['lever_m'] * 1000:.2f} mm")
    print(f"  aero bending        {b['m_aero_Nm']:9.4f} Nm")
    print(f"  centrifugal bending {b['m_cf_Nm']:9.4f} Nm")
    print(f"  rotor shaft torque  {b['shaft_torque_Nm']:9.4f} Nm  allowable {b['shaft_allow_Nm']:.3f}")
    print(f"  motor shaft torque  {b['motor_torque_Nm']:9.4f} Nm")
    print(f"  belt tension        {b['belt_tension_N']:9.2f} N   side load {b['shaft_side_load_N']:.2f} N")
    print(f"  shaft bending       {b['shaft_bending_Nm']:9.4f} Nm  combined shear "
          f"{b['tau_combined_Pa'] / 1e6:.2f} MPa")
    print(f"  pitch link          {b['link_load_N']:9.2f} N   allowable {b['link_allow_N']:.2f} N "
          f"(horn {b['horn_allow_N']:.1f}, buckling {b['link_buckling_N']:.1f})")
    print(f"  attachment allow    {b['attach_allow_N']:9.2f} N")
    print(f"  blade wind up       {b['windup_deg']:9.3f} deg")
    print(f"  tip deflection      {b['tip_defl_mm']:9.4f} mm at {b['peak_blade_N']:.2f} N")
    print(f"  aero twist          {b['aero_twist_deg']:9.4f} deg")
    print(f"  carrier jitter      {b['jitter_deg']:9.3f} deg")
    print()
    print("=== margins ===")
    for k, v in m.items():
        print(f"  {k:36s} {v:8.3f}")
    print()
    print("=== pitch bearing oscillating duty ===")
    bd = bearing_duty(data, b)
    print(f"  cage swing          {bd['cage_swing_deg']:9.3f} deg of {bd['ball_spacing_deg']:.2f} "
          f"deg ball spacing, ratio {bd['recirculation_ratio']:.4f}")
    print(f"  full recirculation  {bd['recirculation_travel_deg']:9.2f} deg of travel, "
          f"mechanism gives {float(data['pitch']['pitch_bearing_travel_deg']):.1f}")
    print(f"  static safety       {bd['s0']:9.4f} at {bd['load_N']:.2f} N per bearing, "
          f"floor {PITCH_BEARING_S0_FLOOR:.1f}")
    print(f"  oscillation         {bd['oscillation_hz']:9.3f} Hz, sliding "
          f"{bd['sliding_mm_per_s']:.1f} mm/s at the bore")
    print(f"  friction, all six   {bd['friction_W']:9.4f} W  "
          f"{bd['friction_frac'] * 100:.3f} percent of shaft power")
    print(f"  plain bearing swap  {bd['plain_friction_W']:9.4f} W  "
          f"{bd['plain_friction_frac'] * 100:.3f} percent, the fallback if it frets")
    print()
    print("=== mass budget ===")
    groups = {}
    for r in b["rows"]:
        print(f"  {r['item']:38s} {r['mass_g']:8.2f} {r['conservative_g']:8.2f}  <- {r['refines']}")
        g = groups.setdefault(r["refines"], [0.0, 0.0])
        g[0] += r["mass_g"]
        g[1] += r["conservative_g"]
    print(f"  {'TOTAL':38s} {b['total_g']:8.2f} {b['total_cons_g']:8.2f}")
    print()
    print("=== group continuity against the week 2 envelope ===")
    env = {e["item"]: e for e in data["mass_envelope_g"]}
    for k, (nom, cons) in groups.items():
        e = env[k]
        drift = (nom - e["nominal_g"]) / e["nominal_g"]
        print(f"  {k:32s} budget {nom:7.2f} vs envelope {e['nominal_g']:7.2f}  {drift:+7.1%}"
              f"   cons {cons:7.2f} vs {e['conservative_g']:7.2f}")
    missing = [k for k in env if k not in groups]
    print(f"  envelope lines with nothing refining them: {missing or 'none'}")
    print()
    tw = b["thrust_N"] / (b["total_g"] / 1000.0 * G)
    tc = float(data["performance"]["thrust_N_conservative"])
    twc = tc / (b["total_cons_g"] / 1000.0 * G)
    print("=== thrust to weight ===")
    print(f"  nominal       {b['thrust_N']:.2f} N / {b['total_g']:.2f} g = {tw:.4f}")
    print(f"  conservative  {tc:.4f} N / {b['total_cons_g']:.2f} g = {twc:.4f}")
    print(f"  week 2 envelope conservative column was "
          f"{sum(e['conservative_g'] for e in data['mass_envelope_g']):.2f} g")
    print(f"  D17 target 2.75 wants {tc / (2.75 * G) * 1000:.1f} g")
    return b, m


def write(data, b, m):
    bd = bearing_duty(data, b)
    st = data.setdefault("structure", {})
    st.update({
        "blade_mass_kg": round(b["blade_mass_kg"], 6),
        "centrifugal_load_N": round(b["fc_N"], 3),
        "overspeed_factor": OVERSPEED,
        "centrifugal_load_overspeed_N": round(b["fc_over_N"], 3),
        "blade_root_bending_Nm": round(b["m_aero_Nm"], 5),
        "blade_centrifugal_bending_Nm": round(b["m_cf_Nm"], 5),
        "blade_allowable_Nm": round(b["blade"]["m_allow_Nm"], 4),
        "blade_ei_Nm2": round(b["blade"]["ei_Nm2"], 3),
        "blade_gj_Nm2": round(b["blade"]["gj_Nm2"], 4),
        "blade_windup_deg": round(b["windup_deg"], 4),
        "blade_margin": round(b["blade"]["m_allow_Nm"] / b["m_aero_Nm"], 4),
        "blade_combined_margin": round(m["blade_combined_margin"], 4),
        "blade_combined_margin_overspeed": round(m["blade_combined_margin_overspeed"], 4),
        "shaft_torque_Nm": round(b["shaft_torque_Nm"], 5),
        "shaft_allowable_Nm": round(b["shaft_allow_Nm"], 4),
        "shaft_margin": round(m["shaft_margin"], 4),
        "shaft_bending_Nm": round(b["shaft_bending_Nm"], 5),
        "shaft_combined_margin": round(m["shaft_combined_margin"], 4),
        "transmission_ratio": b["belt_ratio"],
        "motor_shaft_torque_Nm": round(b["motor_torque_Nm"], 5),
        "blade_load_lever_m": round(b["lever_m"], 6),
        "blade_load_factor": b["load_factor"],
        "pitch_link_load_N": round(b["link_load_N"], 3),
        "pitch_link_allowable_N": round(b["link_allow_N"], 3),
        "pitch_link_margin": round(m["pitch_link_margin"], 4),
        "blade_attachment_allowable_N": round(b["attach_allow_N"], 3),
        "blade_attachment_margin": round(m["blade_attachment_margin"], 4),
        "blade_attachment_margin_overspeed": round(m["blade_attachment_margin_overspeed"], 4),
        "carrier_phase_jitter_deg": round(b["jitter_deg"], 4),
        "pitch_bearing_balls": bd["balls"],
        "pitch_bearing_ball_mm": bd["ball_mm"],
        "pitch_bearing_pitch_diameter_mm": bd["pitch_dia_mm"],
        "pitch_bearing_cage_swing_deg": round(bd["cage_swing_deg"], 4),
        "pitch_bearing_ball_spacing_deg": round(bd["ball_spacing_deg"], 4),
        "pitch_bearing_recirculation_ratio": round(bd["recirculation_ratio"], 4),
        "pitch_bearing_recirculation_travel_deg": round(bd["recirculation_travel_deg"], 3),
        "pitch_bearing_load_N": round(bd["load_N"], 4),
        "pitch_bearing_static_safety": round(bd["s0"], 4),
        "pitch_bearing_static_safety_floor": PITCH_BEARING_S0_FLOOR,
        "pitch_bearing_oscillation_hz": round(bd["oscillation_hz"], 4),
        "pitch_bearing_friction_W": round(bd["friction_W"], 4),
        "pitch_bearing_plain_alternative_W": round(bd["plain_friction_W"], 4),
        "torque_reference": (
            "rotor shaft, downstream of the 3.5 to 1 belt reduction. The motor shaft "
            "carries motor_shaft_torque_Nm, which is this figure divided by the ratio and "
            "by the 0.93 belt efficiency"),
    })
    data["mass_budget_g"] = b["rows"]
    rows = bom_rows()
    data["bom"] = rows
    src = data["sources"].setdefault("structure", {})
    src.update({
        "blade_root_bending_Nm": (
            "aerodynamic bending at mid span. The blade is held at both spiders, so a "
            "uniformly distributed peak load gives a lever of span over 8, 36.30 mm. The "
            "load is thrust per blade times the 4.0 peak to mean factor D16 sets, which is "
            "the top of the published 3 to 4 range because that range is simulated. The "
            "rerun week 3 model gives 2.501 and is not used here"),
        "shaft_torque_Nm": (
            "aerodynamic power plus tare, divided by rotor angular speed at 2404.79 rpm. "
            "This is the rotor shaft, downstream of the 3.5 to 1 belt reduction. It "
            "reproduces the rotor_torque_Nm week 2 published in the sensitivity table"),
        "pitch_link_load_N": (
            "peak pitch link force from the week 3 four-bar solution, rerun in "
            "tools/linkage.py against the week 4 blade. The blade is not chordwise "
            "balanced, so this is the unbalanced figure per D43, and the centrifugal "
            "pitching moment on the 9.31 percent chord offset is most of it"),
        "blade_allowable_Nm": (
            "bending capacity of the closed cell section about the chord line, from the "
            "integrated NACA 0020 ordinates. The skin governs at 215 MPa of wrinkling "
            "stress over the foam, not at the 400 MPa laminate allowable, and the spar "
            "would take 63.2 Nm before the skin takes 25.3"),
        "blade_attachment_allowable_N": (
            "two 693ZZ pitch bearings per blade at a 270 N static rating each, supplier "
            "listing. They are the softest element in the path from the blade to the "
            "spider arm, softer than the bonded root fitting or the bracket bolts"),
        "pitch_bearing_recirculation_ratio": (
            "cage swing over ball spacing for the 693ZZ at the 80 degrees of pitch travel "
            "the four-bar gives. Cage swing is (1 - d/Dm)/2 of the inner ring angle with a "
            "stationary outer ring, d and Dm from catalogue geometry and a 7 ball "
            "complement. Below 1.0 each ball stays inside its own arc, so the wear mode is "
            "false brinelling and not fatigue. The ratio only reaches 1.0 at 144.6 degrees "
            "of travel, which no cyclorotor pitch schedule asks for, so the regime cannot "
            "be tuned out and has to be carried"),
        "pitch_bearing_static_safety": (
            "693ZZ static rating over the centrifugal pull per bearing at the operating "
            "speed, which is where wear accumulates. The overspeed case is strength and it "
            "is gated separately on blade_attachment_margin_overspeed. The 2.0 floor is a "
            "declared rule for a bearing that does not fully recirculate, in the same "
            "class of judgement as overspeed_factor, and Stage 2 closes it with a run to "
            "failure rather than with a catalogue number"),
        "pitch_bearing_friction_W": (
            "0.5 x mu x P x d summed over six bearings at the mean swing rate, mu taken at "
            "0.0015 for a deep groove ball bearing. It is under a tenth of a percent of "
            "rotor shaft power, which is why it sits outside the power budget rather than "
            "inside it. The PTFE fabric lined plain bearing that would be immune to the "
            "wear mode costs pitch_bearing_plain_alternative_W instead, on a 0.08 liner "
            "friction coefficient, and that is the trade Stage 2 makes"),
        "overspeed_factor": (
            "20 percent over the design rotor speed, covering ESC control overshoot and a "
            "gust transient. The problem statement sets no endurance or speed schedule, so "
            "this is a declared case rather than a derived one"),
    })
    perf = data["performance"]
    perf["blade_tip_deflection_mm"] = round(b["tip_defl_mm"], 4)
    perf["blade_twist_deg"] = round(b["aero_twist_deg"], 4)
    res = data["results"]
    res["total_mass_g"] = round(b["total_g"], 2)
    res["weight_N"] = round(b["total_g"] / 1000.0 * G, 4)
    res["thrust_to_weight"] = round(b["thrust_N"] / (b["total_g"] / 1000.0 * G), 4)
    res["mass_g_conservative"] = round(b["total_cons_g"], 2)
    res["thrust_to_weight_conservative"] = round(
        float(perf["thrust_N_conservative"]) / (b["total_cons_g"] / 1000.0 * G), 4)
    res["bom_bought_inr"] = sum(r["line_cost_inr"] for r in rows if r["make_or_buy"] == "buy")
    res["bom_tooling_inr"] = sum(r["line_cost_inr"] for r in rows if r["make_or_buy"] == "make")
    res["bom_total_inr"] = res["bom_bought_inr"] + res["bom_tooling_inr"]
    res["bom_longest_lead_weeks"] = max(r["lead_time_weeks"] for r in rows)
    # newline is forced to LF and ensure_ascii matched to tools/linkage.py, because
    # the two scripts write this same file in sequence and the second one wins. The
    # platform default put CRLF back into a file linkage.py had just written as LF,
    # against a repository that declares eol=lf. Git normalises it on the way in, so
    # the damage never showed up in git status.
    NUMBERS.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n",
                       encoding="utf-8", newline="\n")
    print(f"\nwrote {NUMBERS}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--bom", action="store_true")
    ap.add_argument("--balance", action="store_true")
    args = ap.parse_args()
    data = json.loads(NUMBERS.read_text(encoding="utf-8"))
    if args.bom:
        bom_report()
        return
    b, m = report(data)
    if args.balance:
        balance_report(data, b)
    if args.write:
        write(data, b, m)


if __name__ == "__main__":
    main()
