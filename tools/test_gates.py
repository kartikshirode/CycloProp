#!/usr/bin/env python3
"""Self-test for tools/check.py, plus a read-only pass over the stored linkage.

Most of this builds throwaway repo trees in a temp directory and asserts that the gates
pass an honest design and reject specific attacks. Nothing in that part writes to the real
repo.

`linkage_selftests` is the exception and it reads the real `numbers.json`. It exists
because `check.py` deliberately does not recompute the four-bar, so without it the claim
that every published pitch row comes from the stated loop closure would rest on the weekly
audit alone. It reads and never writes.

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

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check as gates       # noqa: E402  the fixture builds its blade the way the gate reads it

CHECK = Path(__file__).resolve().parent / "check.py"
REPO = CHECK.parent.parent
REPO_NUMBERS = REPO / "stage-1" / "design" / "numbers.json"
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

    # The blade is no longer a chosen number. check.py integrates the published section
    # and recomputes the allowable from it, so a fixture that asserts 108 g and a made up
    # allowable is not an honest tree any more, it is a tree that would fail. It builds
    # itself from the same section instead, and the attacks below move one piece at a time.
    moduli = {"blade_skin_modulus_GPa": 60.0, "blade_foam_modulus_MPa": 70.0,
              "blade_foam_shear_MPa": 19.0}
    seed = {"geometry": {"chord_m": c, "span_m": S}, "structure": dict(moduli)}
    bl = gates.blade_section(seed)
    blade_line_g = round(nb * bl["mass_g"], 4)

    budget = [
        {"item": "blades, 3 off", "mass_g": blade_line_g, "refines": "blades",
         "basis": "cfrp skin over foam core, volume times density with a layup allowance"},
        {"item": "endplates and frame", "mass_g": 33.0, "refines": "frame and endplates",
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
    # The conservative column is built line by line, not chosen. 12 percent on every line
    # sums to exactly the envelope's conservative total, so both weeks agree.
    for b in budget:
        b["conservative_g"] = round(b["mass_g"] * 1.12, 4)
    total = sum(b["mass_g"] for b in budget)
    omega = rpm * 2 * math.pi / 60
    # Per-blade mass is the blade budget over the blade count, not a free number.
    blade_mass = sum(b["mass_g"] for b in budget if "blade" in b["item"]) / 1000.0 / nb
    fc = blade_mass * omega ** 2 * R

    envelope = [
        {"item": "blades", "nominal_g": blade_line_g, "scaling_class": "geometry",
         "conservative_g": round(blade_line_g * 1.12, 4),
         "basis": "cfrp skin over foam core, volume times density with a layup allowance"},
        {"item": "frame and endplates", "nominal_g": 33.0, "scaling_class": "geometry", "conservative_g": 37.0,
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

    # Drive margin. The 180 second datasheet figures and the one derate that turns them
    # into continuous ones, then the fractions of each the design point actually draws.
    # Laid out the way tools/structure.py derives them so the honest tree passes.
    derate, ratio_belt, v_nom, res_ohm, kv_sel = 0.80, 2.0, 22.2, 0.05, 400
    m_in_W = shaft / (eff[0] * eff[1])
    # Current follows the torque the motor shaft has to make, through Kt, with the idle
    # current the datasheet publishes added on. Input power over pack voltage is the draw
    # of an ideal resistor and it runs low by roughly the efficiency.
    shaft_dem = shaft / omega
    motor_dem = shaft_dem / (ratio_belt * eff[0])
    idle_A = 0.9
    m_in_A = motor_dem / (9.5493 / kv_sel) + idle_A
    m_rpm = rpm * ratio_belt
    peak_W, peak_A = 320.0 / derate, 67.0 / derate
    v_load = v_nom - m_in_A * res_ohm
    ceiling_rpm = kv_sel * v_load

    # Structural demands derived from the design rather than asserted beside it.
    ratio, lever, load_factor = 2.0, S / 4, 4.0
    overspeed = 1.2
    blade_dem = thrust / nb * lever * load_factor
    # Centrifugal bending is the larger of the two spanwise loads on a cyclorotor and it
    # goes as the square of rotor speed, so an honest section is sized on both of them
    # together at the declared overspeed rather than on the aerodynamic case alone. That
    # leaves blade_margin comfortable and the combined margins tight, which is the shape
    # the real design has as well.
    cf_dem = fc * lever
    fc_over = fc * overspeed ** 2
    combined_over = (blade_dem + cf_dem) * overspeed ** 2
    blade_all = bl["allow_Nm"]

    # Shaft, horn and link allowables all come off published sections now, so the fixture
    # takes them from the same place rather than picking a multiple of the demand.
    sh = gates.thin_tube(gates.SHAFT_OD_M, gates.SHAFT_WALL_M)
    shaft_all = gates.SPAR_TAU_PA * sh["j_m4"] / (gates.SHAFT_OD_M / 2.0)
    shaft_bend = 2.0
    tau_comb = math.hypot(shaft_bend * (gates.SHAFT_OD_M / 2.0) / sh["i_m4"] / 2.0,
                          shaft_dem * (gates.SHAFT_OD_M / 2.0) / sh["j_m4"])
    horn_m, link_m = 0.0244, 0.105
    link_all = min(gates.AL_SIGMA_PA * gates.HORN_W_M * gates.HORN_T_M ** 2 / 6.0 / horn_m,
                   gates.ROD_END_STATIC_N,
                   math.pi ** 2 * gates.SPAR_E_PA
                   * gates.thin_tube(gates.LINK_OD_M, gates.LINK_WALL_M)["i_m4"] / link_m ** 2)
    link_dem = 42.0
    # Two pitch bearings hold each blade and the rating they are held to is the one ISO 76
    # gives for this ball complement, not a supplier listing.
    brg_c0 = gates.ISO76_F0 * 7 * 1.5875 ** 2
    att_all = 2 * brg_c0

    e_skin, e_foam, g_foam = 60.0, 70.0, 19.0
    wrinkle = bl["wrinkle_Pa"] / 1e6

    # The two sensitivity sweeps, run here the way check.py runs them.
    band_low = 0.5
    band_worst = min(gates.blade_section(seed, skin_factor=band_low
                                        + (1.0 - band_low) * i / 200.0)["allow_Nm"]
                     for i in range(201)) / combined_over
    _lo, _hi = 0.02, 1.0
    for _ in range(60):
        _mid = 0.5 * (_lo + _hi)
        _b = gates.blade_section(seed, foam_factor=_mid)
        _d = (blade_dem + _b["mass_g"] / 1000.0 * omega ** 2 * R * lever) * overspeed ** 2
        if _b["allow_Nm"] / _d < 1.5:
            _lo = _mid
        else:
            _hi = _mid
    knockdown = 0.5 * (_lo + _hi)
    dg_e, dg_g, dg_rho = 36.0, 13.0, 32.0
    dg_b = gates.blade_section(seed, foam_factor=dg_e / e_foam, foam_rho=dg_rho)
    dg_sec = dg_b["section"]
    dg_ei = (e_skin * 1e9 * gates.BLADE_SKIN_AREAL_KG_M2 / gates.BLADE_SKIN_RHO
             * dg_sec["skin_y2_ds_m3"]
             + gates.SPAR_E_PA * gates.thin_tube(gates.BLADE_SPAR_DIA_FRAC * c,
                                                 gates.BLADE_SPAR_WALL_M)["i_m4"]
             + dg_e * 1e6 * dg_sec["i_chord_m4"] * gates.BLADE_FOAM_FILL)
    dg_wr = 0.5 * (e_skin * 1e9 * dg_e * 1e6 * dg_g * 1e6) ** (1.0 / 3.0)
    dg_allow = min(min(dg_wr, gates.SKIN_SIGMA_PA) * dg_ei / (e_skin * 1e9 * dg_sec["y_max_m"]),
                   gates.SPAR_SIGMA_PA * dg_ei
                   / (gates.SPAR_E_PA * gates.BLADE_SPAR_DIA_FRAC * c / 2.0))
    dg_dem = (blade_dem + dg_b["mass_g"] / 1000.0 * omega ** 2 * R * lever) * overspeed ** 2
    dg_margin = dg_allow / dg_dem

    # Pitch bearing oscillating duty, laid out the way tools/structure.py computes it. The
    # bearing swings 80 degrees once a revolution instead of turning, so the cage moves a
    # third of that and every ball stays inside its own arc. The fixture is honest, which
    # here means the recirculation ratio is under 1 and the static safety factor at the
    # operating load clears the 2.0 floor that follows from it.
    brg_z, brg_ball, brg_pd, brg_travel = 7, 1.5875, 5.5, 80.0
    brg_cage = (1.0 - brg_ball / brg_pd) / 2.0
    brg_swing, brg_spacing = brg_cage * brg_travel, 360.0 / brg_z
    brg_rate = (2.0 / math.pi) * math.radians(brg_travel / 2.0) * omega
    brg_fric = 2 * nb * 0.5 * 0.0015 * (fc / 2.0) * 0.003 * brg_rate

    # The azimuthal table is a distribution of the thrust, so its cycle mean has to
    # reproduce thrust per blade. A shape alone used to satisfy the gate.
    raw_az = [(a, abs(math.cos(math.radians(a))) + 0.12) for a in range(0, 360, 10)]
    az_scale = (thrust / nb) / (sum(v for _, v in raw_az) / len(raw_az))
    azimuthal = [(a, v * az_scale) for a, v in raw_az]
    # A lateral column with the cycle mean trimmed out, the way week 3 leaves it once the
    # solved schedule replaces the phase-free sinusoid. Peak is what the gate reads back.
    lateral = [(a, 0.9 * v * az_scale * math.sin(math.radians(2.0 * a))) for a, v in raw_az]
    peak_lat = max(abs(v) for _, v in lateral)

    amp, phase = 40, 9.0
    pts = schedule_points(amp, phase)
    model = [amp * math.cos(math.radians(a - 90.0 - phase)) for a, _ in pts]
    rms = math.sqrt(sum((p - m) ** 2 for (_, p), m in zip(pts, model)) / len(pts))

    # Deflection, twist and wind up all come off the two stiffnesses the section gives.
    ptm = 2.5
    peak_blade = thrust / nb * ptm
    tip_defl_mm = 5.0 * peak_blade * S ** 3 / (384.0 * bl["ei_Nm2"]) * 1000.0
    twist_deg = math.degrees(peak_blade * (35.0 - 25.0) / 100.0 * c * S / (8.0 * bl["gj_Nm2"]))
    peak_moment = 2.0
    windup_deg = math.degrees(peak_moment * S / (2.0 * bl["gj_Nm2"]))

    # The gear pair steps the carrier angle up, so the servo supplies more torque than the
    # carrier and not less, and the margin is taken on half of stall.
    carrier_t, step_up, servo_travel, stall_t = 0.10, 1.5, 240.0, 0.40
    servo_t = carrier_t * step_up / 2
    servo_margin = stall_t * 0.5 / servo_t

    bom = [
        {"item": "outrunner A", "category": "drive", "qty": 1, "unit_cost_inr": 8000,
         "line_cost_inr": 8000, "lead_time_weeks": 3, "make_or_buy": "buy",
         "source": "distributor listing, priced at list level", "priced_date": "1 August 2026"},
        {"item": "brushless controller", "category": "drive", "qty": 1,
         "unit_cost_inr": 3000, "line_cost_inr": 3000, "lead_time_weeks": 2,
         "make_or_buy": "buy", "source": "distributor listing, priced at list level",
         "priced_date": "1 August 2026"},
        {"item": "pitch servos", "category": "hardware", "qty": 2, "unit_cost_inr": 1500,
         "line_cost_inr": 3000, "lead_time_weeks": 2, "make_or_buy": "buy",
         "source": "distributor listing, priced at list level", "priced_date": "1 August 2026"},
        {"item": "carbon and foam stock", "category": "material", "qty": 1,
         "unit_cost_inr": 6000, "line_cost_inr": 6000, "lead_time_weeks": 2,
         "make_or_buy": "buy", "source": "composite supplier list price, landed",
         "priced_date": "1 August 2026"},
        {"item": "blade moulds", "category": "tooling", "qty": 2, "unit_cost_inr": 5000,
         "line_cost_inr": 10000, "lead_time_weeks": 4, "make_or_buy": "make",
         "source": "shop rate for a machined aluminium mould pair",
         "priced_date": "1 August 2026"},
        {"item": "machined fittings", "category": "fabricated", "qty": 1,
         "unit_cost_inr": 7000, "line_cost_inr": 7000, "lead_time_weeks": 3,
         "make_or_buy": "make", "source": "shop rate for CNC job work against a drawing",
         "priced_date": "1 August 2026"},
    ]
    bom_bought = sum(r["line_cost_inr"] for r in bom if r["make_or_buy"] == "buy")
    bom_made = sum(r["line_cost_inr"] for r in bom if r["make_or_buy"] == "make")

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
                     "pitch_axis_pct_chord": 35},
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
                        "blade_deflection_thrust_loss": defl_loss,
                        "blade_load_peak_to_mean": ptm,
                        "blade_tip_deflection_mm": tip_defl_mm,
                        "blade_twist_deg": twist_deg,
                        "motor_torque_Nm": motor_dem,
                        "motor_idle_current_A": idle_A,
                        "motor_input_W": m_in_W, "motor_input_current_A": m_in_A,
                        "motor_rpm": m_rpm, "belt_ratio": ratio_belt,
                        "motor_derate": derate,
                        "motor_current_frac_180s": m_in_A / peak_A,
                        "motor_power_frac_180s": m_in_W / peak_W,
                        "pack_voltage_nominal_V": v_nom,
                        "pack_voltage_loaded_V": v_load,
                        "motor_speed_ceiling_rpm": ceiling_rpm,
                        "motor_speed_rule": 0.90,
                        "motor_rpm_frac_ceiling": m_rpm / ceiling_rpm,
                        "thrust_floor_stacked_N": 2.5 * (m_cons / 1000.0) * G / (ct_low / ct)},
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
            {"azimuth_deg": a, "normal_force_N": v, "lateral_force_N": lv}
            for (a, v), (_, lv) in zip(azimuthal, lateral)],
        "drive_candidates": [
            {"name": "outrunner A", "continuous_power_W": 320.0, "kv": 400,
             "continuous_current_A": 67.0, "continuous_torque_Nm": 9.5493 / 400 * 67.0,
             "max_power_180s_W": 320.0 / derate, "peak_current_180s_A": 67.0 / derate,
             "internal_resistance_ohm": res_ohm,
             "mass_g": 62.0, "selected": True,
             "basis": "supplier listing for an outrunner in this power class",
             "verdict": "selected, covers the design point on its continuous rating"},
            {"name": "outrunner B", "continuous_power_W": 400.0, "kv": 350,
             "continuous_current_A": 77.0, "continuous_torque_Nm": 9.5493 / 350 * 77.0,
             "max_power_180s_W": 400.0 / derate, "peak_current_180s_A": 77.0 / derate,
             "internal_resistance_ohm": 0.06,
             "mass_g": 88.0, "selected": False}],
        "linkage_dimensions": [
            {"link": "crank", "length_mm": 24.0}, {"link": "coupler", "length_mm": 61.0},
            {"link": "rocker", "length_mm": 33.0}, {"link": "ground", "length_mm": 70.0}],
        "pitch_schedule": [{"azimuth_deg": a, "pitch_deg": pv} for a, pv in pts],
        "vector_map": [
            {"phase_command_deg": ph, "vertical_force_N": thrust * math.cos(math.radians(ph)),
             "lateral_force_N": thrust * math.sin(math.radians(ph))}
            for ph in (-150.0, -75.0, 0.0, 75.0, 150.0)],
        "pitch": {"mechanism": "passive four-bar", "offset_m": 0.024,
                  "phase_delay_deg": phase, "vector_range_deg": 360.0,
                  "phase_authority_deg": 360.0, "schedule_rms_residual_deg": rms,
                  "actuator_count": 2, "actuator_mass_g": 18.0,
                  "side_force_tilt_deg": 28.0, "peak_lateral_force_N": peak_lat,
                  "pitch_bearing_travel_deg": 80.0,
                  "horn_m": horn_m, "pitch_link_m": link_m,
                  "construction_angle_deg": -110.0,
                  "carrier_torque_Nm": carrier_t, "gear_step_up": step_up,
                  "servo_torque_Nm": servo_t, "servo_stall_torque_Nm": stall_t,
                  "servo_travel_deg": servo_travel, "servo_torque_margin": servo_margin,
                  "carrier_gear_mm": 40.0, "servo_gear_mm": 60.0, "servo_mass_g": 9.0,
                  "transmission_angle_min_deg": 60.0, "transmission_angle_max_deg": 120.0,
                  "axis_keepout_mm": 0.5, "neighbour_clearance_mm": 40.0,
                  "carrier_radial_force_N": 60.0,
                  "swept_outer_radius_mm": 190.0, "swept_inner_radius_mm": 95.0,
                  "slew_time_s": 0.2, "actuator_draw_W": act_p,
                  "blade_pitch_inertia_kgm2": 1.5e-05, "blade_cg_pct_chord": 39.0,
                  "peak_blade_moment_Nm": peak_moment,
                  # The pitch link load crosses from tools/linkage.py into
                  # tools/structure.py, so the two sides have to agree or the solvers ran
                  # in the wrong order.
                  "peak_link_force_N": link_dem},
        "packaging": {"envelope_length_mm": 400, "envelope_width_mm": 300,
                      "envelope_height_mm": 300, "mount_points": 4,
                      "swept_diameter_mm": 380.0},
        "bom": bom,
        "structure": {"blade_mass_kg": blade_mass, "centrifugal_load_N": fc,
                      "blade_root_bending_Nm": blade_dem, "shaft_torque_Nm": shaft_dem,
                      "blade_allowable_Nm": blade_all, "shaft_allowable_Nm": shaft_all,
                      "blade_ei_Nm2": bl["ei_Nm2"], "blade_gj_Nm2": bl["gj_Nm2"],
                      "blade_windup_deg": windup_deg, "shaft_bending_Nm": shaft_bend,
                      "motor_shaft_torque_Nm": motor_dem,
                      "carrier_phase_jitter_deg": 0.15,
                      "blade_margin": blade_all / blade_dem,
                      "shaft_margin": shaft_all / shaft_dem,
                      "transmission_ratio": ratio,
                      "torque_reference": "rotor shaft, upstream of the 2 to 1 reduction",
                      "blade_load_lever_m": lever, "blade_load_factor": load_factor,
                      "pitch_link_load_N": link_dem, "pitch_link_allowable_N": link_all,
                      "pitch_link_margin": link_all / link_dem,
                      "blade_attachment_allowable_N": att_all,
                      "blade_attachment_margin": att_all / fc,
                      "overspeed_factor": overspeed,
                      "centrifugal_load_overspeed_N": fc_over,
                      "blade_attachment_margin_overspeed": att_all / fc_over,
                      "blade_centrifugal_bending_Nm": cf_dem,
                      "blade_combined_margin": blade_all / (blade_dem + cf_dem),
                      "blade_combined_margin_overspeed": blade_all / combined_over,
                      # Combined bending and torsion is always worse than torsion alone.
                      # check.py floors this one without recomputing it, because the shaft
                      # section properties are not in numbers.json.
                      "shaft_combined_margin": gates.SPAR_TAU_PA / tau_comb,
                      # The oscillating duty on the pitch bearings. The fixture computes
                      # it the way tools/structure.py does so the honest tree passes, and
                      # the attacks below break one link at a time.
                      "pitch_bearing_balls": brg_z,
                      "pitch_bearing_ball_mm": brg_ball,
                      "pitch_bearing_pitch_diameter_mm": brg_pd,
                      "pitch_bearing_cage_swing_deg": brg_swing,
                      "pitch_bearing_ball_spacing_deg": brg_spacing,
                      "pitch_bearing_recirculation_ratio": brg_swing / brg_spacing,
                      "pitch_bearing_recirculation_travel_deg": brg_spacing / brg_cage,
                      "pitch_bearing_load_N": fc / 2.0,
                      "pitch_bearing_static_safety": att_all / 2.0 / (fc / 2.0),
                      "pitch_bearing_static_safety_floor": 2.0,
                      "pitch_bearing_oscillation_hz": rpm / 60.0,
                      "pitch_bearing_friction_W": brg_fric,
                      "pitch_bearing_plain_alternative_W": brg_fric * 53.0,
                      # Which material property the blade allowable turns on. The wrinkling
                      # stress is recomputed by the gate from the three moduli beside it;
                      # the two sweeps are floored, because they need the integrated
                      # section that lives in tools/structure.py.
                      "blade_skin_modulus_GPa": e_skin, "blade_foam_modulus_MPa": e_foam,
                      "blade_foam_shear_MPa": g_foam,
                      "blade_wrinkle_stress_MPa": wrinkle,
                      "blade_allow_skin_Nm": bl["allow_skin_Nm"],
                      "blade_allow_spar_Nm": bl["allow_spar_Nm"],
                      "blade_skin_band_low": band_low,
                      "blade_skin_band_worst_margin": band_worst,
                      "blade_foam_knockdown_at_floor": knockdown,
                      "blade_foam_downgrade_margin": dg_margin,
                      "blade_foam_downgrade_blade_g": dg_b["mass_g"],
                      "blade_foam_downgrade_modulus_MPa": dg_e,
                      "blade_foam_downgrade_shear_MPa": dg_g,
                      "blade_foam_downgrade_density_kgm3": dg_rho},
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
        "results": {"bom_bought_inr": bom_bought, "bom_tooling_inr": bom_made,
                    "bom_total_inr": bom_bought + bom_made,
                    "bom_longest_lead_weeks": max(r["lead_time_weeks"] for r in bom),
                    "total_mass_g": total, "weight_N": total / 1000 * G,
                    "thrust_to_weight": thrust / (total / 1000 * G),
                    "mass_envelope_g": env_nom, "mass_g_conservative": m_cons,
                    "thrust_to_weight_conservative": t_cons / (m_cons / 1000 * G)},
    }


def rnd(v, n):
    """Adversarial fixtures put strings in numeric fields on purpose, so the
    builder must not choke before the gate gets a chance to reject them."""
    return round(v, n) if isinstance(v, (int, float)) and not isinstance(v, bool) else v


def doc(path, headings, numbers=(), words=600, says=()):
    body = [f"# {headings[0]}", "", FILLER[:words * 6], ""]
    for s in says:
        body += [s, ""]
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
        # D32: every week 2 document states the stacked conservative T/W in its narrative,
        # not only in the declaration block, because the declaration block is not what a
        # reader sees. `states_value` cuts the block off before it looks.
        stacked = ("results.thrust_to_weight_conservative",
                   rnd(data["results"].get("thrust_to_weight_conservative"), 4))
        says = [f"Stacked conservative thrust to weight is {stacked[1]} against the design "
                f"case, and the difference is the two downside allowances multiplying."]
        doc(g / "01-configuration.md", ["Configuration", "Why this configuration"],
            [("geometry.blades", geo["blades"]), ("geometry.radius_m", geo["radius_m"]),
             ("geometry.span_m", rnd(geo["span_m"], 4)), stacked], says=says)
        doc(g / "02-rotor-sizing.md", ["Rotor sizing", "Shape family", "Radius"],
            [("geometry.radius_m", geo["radius_m"]), ("geometry.chord_m", rnd(geo["chord_m"], 4)),
             ("operating.rpm", rnd(data["operating"]["rpm"], 1)), stacked], says=says)
        doc(g / "04-thrust-and-power.md", ["Thrust", "Power", "Sensitivity"],
            [("performance.thrust_N", rnd(perf["thrust_N"], 2)),
             ("performance.aero_power_W", perf["aero_power_W"]),
             ("performance.module_electrical_power_W", rnd(perf["module_electrical_power_W"], 1)),
             stacked], says=says)
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
        doc(g / "07-team-and-execution.md", ["Team capability", "Execution plan", "Stage 2"],
            [("geometry.radius_m", data["geometry"]["radius_m"]),
             ("operating.rpm", rnd(data["operating"]["rpm"], 2)),
             ("performance.thrust_N", rnd(data["performance"]["thrust_N"], 2))])
        sub = d / "stage-1" / "submission"
        submission_doc(sub / "cycloprop-stage1.md", data)
        build_pdf_from(sub / "cycloprop-stage1.md", sub / "cycloprop-stage1.pdf")
        (sub / "email-draft.md").write_text(
            "\n".join(["# Stage 1 submission email", "",
                       "To: pushpak_gc2026@aero.iitb.ac.in",
                       "Subject: PUSHPAK Grand Challenge, CycloProp Stage 1", "",
                       "The attachment is cycloprop-stage1.pdf and it carries the full",
                       "design report for the module.", ""]), encoding="utf-8")
        # Shaped like the real file: instructions that name the markers, then a status block
        # that carries them. The gate reads the block alone, so prose above it naming a marker
        # must not count as a person having written one.
        (d / "stage-1" / "human-gate.md").write_text(
            "\n".join(["# Week H", "",
                       "Replace TECHNICAL-READ-PENDING with TECHNICAL-READ-COMPLETE only",
                       "after opening the built PDF and reading it end to end.", "",
                       "## Status", "",
                       "REGISTRATION-CONFIRMED", "ELIGIBILITY-CHECKED",
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


# Every self-test line printed by this file, cases and probes alike, appends here first.
# The closing total is len(ANNOUNCED), so it is counted and not kept by hand. The constant
# it replaced had drifted one behind what the run actually printed and nothing noticed.
ANNOUNCED = []

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


def _measured(d, sigma=0.3151, c_over_r=0.66, coeff=None, drop=()):
    """Append a measured coefficient scenario for this design's own shape family. The
    fixture geometry is sigma 0.3151 and c/R 0.66, so the defaults match it."""
    cf = (d["performance"]["blade_area_coeff"] * 1.1 if coeff is None else coeff)
    row = {"name": "Kellen 2019 config 8", "evidence_class": "measured",
           "blade_area_coeff": cf,
           # Figure of merit and thrust coefficient came off one rotor at one operating
           # point, so the row carries both. This design takes a coefficient below the
           # measured one, and the figure of merit that follows is the measured one scaled
           # by that ratio to the power of one and a half.
           "figure_of_merit": round(d["performance"]["figure_of_merit"]
                                    / (d["performance"]["blade_area_coeff"] / cf) ** 1.5, 6),
           "solidity": sigma, "chord_to_radius": c_over_r,
           "basis": "measured on a three bladed NACA 0020 rotor at the same solidity "
                    "and chord to radius, read off the published sweep"}
    for k in drop:
        row.pop(k, None)
    d["coefficient_scenarios"].append(row)
    return d


def _haircut_5pct(d):
    """Only the deflection allowance left, so the low coefficient sits at 95 percent of
    nominal. The deflection loss and every number downstream of the conservative thrust
    move with it, or the case fails on a gate it was not aiming at."""
    d["performance"]["blade_area_coeff_low"] = round(d["performance"]["blade_area_coeff"] * 0.95, 6)
    d["performance"]["blade_deflection_thrust_loss"] = 0.05
    t_cons = d["performance"]["thrust_N"] * 0.95
    d["performance"]["thrust_N_conservative"] = t_cons
    d["results"]["thrust_to_weight_conservative"] = (
        t_cons / (d["results"]["mass_g_conservative"] / 1000 * G))
    return d


def five_pct_no_measurement(d):
    return _haircut_5pct(d)


case("a 5 percent haircut with nothing measured is rejected",
     False, five_pct_no_measurement, upto=2, week=2)


def five_pct_measured_family(d):
    return _measured(_haircut_5pct(d))


case("a 5 percent haircut passes once this shape family is measured",
     True, five_pct_measured_family, upto=2, week=2)


def five_pct_other_family(d):
    """Measured, but on a rotor at half the solidity. It buys nothing."""
    return _measured(_haircut_5pct(d), sigma=0.159, c_over_r=0.333)


case("a measurement on a different shape family does not buy the 5 percent floor",
     False, five_pct_other_family, upto=2, week=2)


def five_pct_undercuts_nominal(d):
    """Measured on the right family, but below the nominal coefficient it is meant to
    support, so it cannot retire the transfer allowance."""
    return _measured(_haircut_5pct(d), coeff=d["performance"]["blade_area_coeff"] * 0.9)


case("a measurement under the nominal coefficient does not buy the 5 percent floor",
     False, five_pct_undercuts_nominal, upto=2, week=2)


def five_pct_undeclared_geometry(d):
    """Measured and favourable, but it never says what was measured, so it fails closed."""
    return _measured(_haircut_5pct(d), drop=("solidity", "chord_to_radius"))


case("a measured scenario with no declared geometry fails closed",
     False, five_pct_undeclared_geometry, upto=2, week=2)


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


def _rescale_mass(d, nom_factor, cons_factor, target=None, target_note=True,
                  scale_budget=True):
    """Move the mass envelope so one chosen T/W case lands where a test wants it, keeping
    every other mass gate consistent. The envelope lines, the stated totals, the selected
    candidate row and the losing rows all have to move together or the test fails on a
    gate it was not aiming at.

    The refined budget moves with the envelope by default. Since D33 the stated
    conservative mass is the sum of the budget's own conservative lines once that budget
    exists, so a fixture that moves the envelope and leaves the budget behind is not a
    heavier design, it is a design whose two mass lists disagree, and it fails on that
    instead of on the case the test was aiming at. `chosen_conservative_mass` is the one
    caller that wants them to disagree, and it says so."""
    for e in d["mass_envelope_g"]:
        e["nominal_g"] = round(e["nominal_g"] * nom_factor, 4)
        e["conservative_g"] = round(e["conservative_g"] * cons_factor, 4)
    if scale_budget:
        # Only the conservative column, because that is the one bound to a stated scalar.
        # The nominal budget column is what per-blade mass and the centrifugal load are
        # derived from, so scaling it would move the structure block underneath a test
        # that is about mass, and every caller here runs at week 2 where the nominal
        # budget column is not read at all.
        for b in d["mass_budget_g"]:
            b["conservative_g"] = round(b["conservative_g"] * cons_factor, 4)
    nom = sum(e["nominal_g"] for e in d["mass_envelope_g"])
    cons = sum(e["conservative_g"] for e in d["mass_envelope_g"])
    tn = d["performance"]["thrust_N"]
    tc = d["performance"]["thrust_N_conservative"]
    tw_cons = tc / (cons / 1000 * G)
    d["results"]["mass_envelope_g"] = nom
    d["results"]["mass_g_conservative"] = cons
    d["results"]["thrust_to_weight_conservative"] = tw_cons
    for i, c in enumerate(d["configuration_candidates"]):
        if c.get("selected"):
            c["module_mass_g"] = nom
            c["module_tw"] = tn / (nom / 1000 * G)
            c["module_tw_conservative"] = tw_cons
        else:
            c["module_tw_conservative"] = tw_cons * (0.83 if i == 1 else 0.72)
    if target is not None:
        d["results"]["mass_target_week4_g"] = target
        d["sources"].setdefault("results", {})["mass_target_week4_g"] = (
            "the conservative mass that clears the limit at the conservative thrust, "
            "carried into the week 4 budget as the reduction to find line by line"
            if target_note else "week 4")
    return d


def _target(d):
    return d["performance"]["thrust_N_conservative"] / (2.5 * G) * 1000


def stacked_miss(d):
    """Conservative mass at 500 g against a 400 g nominal. The stacked downside misses
    2.5, and the design case and both single downsides still clear it."""
    return _rescale_mass(d, 1.0, 500.0 / 448.0, target=_target(d))


case("a stacked downside miss passes week 2 with a week 4 mass target",
     True, stacked_miss, upto=2, week=2)


def stacked_miss_no_target(d):
    return _rescale_mass(d, 1.0, 500.0 / 448.0)


case("a stacked downside miss with no mass target is rejected",
     False, stacked_miss_no_target, upto=2, week=2)


def stacked_miss_wrong_target(d):
    return _rescale_mass(d, 1.0, 500.0 / 448.0, target=_target(d) * 1.15)


case("a stacked downside miss with an inflated mass target is rejected",
     False, stacked_miss_wrong_target, upto=2, week=2)


def stacked_miss_bare_target(d):
    return _rescale_mass(d, 1.0, 500.0 / 448.0, target=_target(d), target_note=False)


case("a mass target with no retirement path is rejected",
     False, stacked_miss_bare_target, upto=2, week=2)


def drop_stacked_tw(root, data):
    """D32: take the stacked figure out of one week 2 document's narrative and leave the
    declaration block alone, which is the way a document actually goes stale. Every stored
    number still reproduces, so only the document rule can catch this."""
    p = root / "stage-1" / "design" / "02-rotor-sizing.md"
    keep = [l for l in p.read_text(encoding="utf-8").splitlines()
            if not l.startswith("Stacked conservative thrust to weight")]
    p.write_text(chr(10).join(keep), encoding="utf-8")


case("a week 2 document that drops the stacked T/W from its prose is rejected",
     False, upto=2, week=2, tweak=drop_stacked_tw)


def chosen_conservative_mass(d):
    """D33. The week 4 stacked test reads results.mass_g_conservative. Here the envelope
    and the stated total are moved together, so every week 2 gate still passes and the
    conservative T/W improves, while the refined budget's own conservative lines are left
    where they were. Only the sum rule notices."""
    return _rescale_mass(d, 1.0, 420.0 / 448.0, scale_budget=False)


case("a week 4 conservative mass the budget lines do not give is rejected",
     False, chosen_conservative_mass, upto=4, week=4)


def shrinking_budget_line(d):
    """One line grows less than nothing under the conservative column, paid for by the
    line next to it, so the total still sums."""
    d["mass_budget_g"][0]["conservative_g"] = round(d["mass_budget_g"][0]["mass_g"] * 0.8, 4)
    d["mass_budget_g"][1]["conservative_g"] = round(
        d["mass_budget_g"][1]["conservative_g"]
        + d["mass_budget_g"][0]["mass_g"] * 0.32, 4)
    return d


case("a budget line that shrinks under conservative growth is rejected",
     False, shrinking_budget_line, upto=4, week=4)


def design_case_short(d):
    """The whole envelope half again heavier, so even the design case misses the limit."""
    return _rescale_mass(d, 1.5, 1.5)


case("a design case under T/W 2.5 is rejected", False, design_case_short, upto=2, week=2)


def mass_downside_short(d):
    """Nominal untouched so the design case still clears. Conservative at 600 g, which the
    mass downside on its own cannot carry."""
    return _rescale_mass(d, 1.0, 600.0 / 448.0, target=_target(d))


case("a mass downside alone under T/W 2.5 is rejected",
     False, mass_downside_short, upto=2, week=2)


def coeff_downside_short(d):
    """Nominal at 500 g and conservative at 540 g. The design case and the mass downside
    both clear, the coefficient downside on its own does not."""
    return _rescale_mass(d, 500.0 / 400.0, 540.0 / 448.0, target=_target(d))


case("a coefficient downside alone under T/W 2.5 is rejected",
     False, coeff_downside_short, upto=2, week=2)


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


# ---- round 4, the week 4 structural cases ---------------------------------------
# Everything below stores a self-consistent structure block on purpose. Each one would
# have passed every margin gate that existed before week 4, because each one is wrong in
# a way that only the case week 4 added can see.

def aero_only_blade(d):
    """A section sized on aerodynamic bending alone, with every stored margin reproducing
    from what sits beside it. On a cyclorotor that is the small load: centrifugal bending
    is nine times it here, so the section is about half of what the blade needs and
    `blade_margin` still reads a healthy 2.9. Only the combined case can say so."""
    st = d["structure"]
    st["blade_allowable_Nm"] = st["blade_root_bending_Nm"] * 2.9
    st["blade_margin"] = 2.9
    st["blade_combined_margin"] = st["blade_allowable_Nm"] / (
        st["blade_root_bending_Nm"] + st["blade_centrifugal_bending_Nm"])
    st["blade_combined_margin_overspeed"] = (st["blade_combined_margin"]
                                             / st["overspeed_factor"] ** 2)
    return d


case("a blade sized on aerodynamic bending alone is rejected", False, aero_only_blade)


def token_overspeed(d):
    """An overspeed of 1.001 satisfies the inequality and covers nothing. Every derived
    overspeed value is recomputed from it, so the design is internally consistent and the
    only thing wrong with it is that the declared case is not a case."""
    st = d["structure"]
    st["overspeed_factor"] = 1.001
    sq = 1.001 ** 2
    st["centrifugal_load_overspeed_N"] = st["centrifugal_load_N"] * sq
    st["blade_attachment_margin_overspeed"] = (st["blade_attachment_allowable_N"]
                                               / st["centrifugal_load_overspeed_N"])
    st["blade_combined_margin_overspeed"] = st["blade_allowable_Nm"] / (
        (st["blade_root_bending_Nm"] + st["blade_centrifugal_bending_Nm"]) * sq)
    return d


case("a token overspeed of 1.001 is rejected", False, token_overspeed)


def asserted_centrifugal_bending(d):
    """Centrifugal bending written down rather than taken from the recomputed centrifugal
    load and the same lever the aerodynamic case uses. Halved, it lifts the combined
    margin by two thirds, and both combined margins still reproduce from the numbers
    stored next to them, so the derivation check is the only witness."""
    st = d["structure"]
    st["blade_centrifugal_bending_Nm"] *= 0.5
    st["blade_combined_margin"] = st["blade_allowable_Nm"] / (
        st["blade_root_bending_Nm"] + st["blade_centrifugal_bending_Nm"])
    st["blade_combined_margin_overspeed"] = (st["blade_combined_margin"]
                                             / st["overspeed_factor"] ** 2)
    return d


case("centrifugal bending that does not follow from the load and the lever is rejected",
     False, asserted_centrifugal_bending)


def asserted_recirculation_ratio(d):
    """The ratio written down as 1.2 while the cage swing and the ball spacing beside it
    still say 0.55. Claiming full recirculation is how the oscillating floor gets switched
    off, so the ratio is derived from the two numbers under it and never read."""
    d["structure"]["pitch_bearing_recirculation_ratio"] = 1.2
    return d


case("a recirculation ratio the cage swing does not give is rejected",
     False, asserted_recirculation_ratio)


def impossible_ball_complement(d):
    """The honest way to reach a ratio of 1.0 with everything reproducing: more balls, so
    the spacing shrinks under the cage swing. 13 of them need 20.6 mm of a 17.3 mm pitch
    circle, which is the only thing standing between this fixture and a passing tree."""
    st = d["structure"]
    st["pitch_bearing_balls"] = 13
    st["pitch_bearing_ball_spacing_deg"] = 360.0 / 13
    st["pitch_bearing_recirculation_ratio"] = (st["pitch_bearing_cage_swing_deg"]
                                               / st["pitch_bearing_ball_spacing_deg"])
    cage = st["pitch_bearing_cage_swing_deg"] / 80.0
    st["pitch_bearing_recirculation_travel_deg"] = st["pitch_bearing_ball_spacing_deg"] / cage
    return d


case("a ball count that will not fit on the pitch circle is rejected",
     False, impossible_ball_complement)


def lowered_oscillating_floor(d):
    """A floor a later week can lower is not a floor. Everything else here is honest."""
    d["structure"]["pitch_bearing_static_safety_floor"] = 1.5
    return d


case("an oscillating static safety floor below 2.0 is rejected", False,
     lowered_oscillating_floor)


def asserted_cage_swing(d):
    """Cage swing halved and the ratio kept consistent with it, so the recirculation
    check and the floor both read healthy. Only the derivation from the ball geometry and
    the frozen pitch travel can see it."""
    st = d["structure"]
    st["pitch_bearing_cage_swing_deg"] *= 0.5
    st["pitch_bearing_recirculation_ratio"] = (st["pitch_bearing_cage_swing_deg"]
                                               / st["pitch_bearing_ball_spacing_deg"])
    return d


case("a cage swing that does not follow from the ball geometry is rejected",
     False, asserted_cage_swing)


def bearing_friction_off_the_budget(d):
    """Friction big enough to be a power line, still sitting outside the power budget. A
    bearing swap is exactly how this happens, because the plain bearing that fixes the
    wear mode costs fifty times what the ball bearing does."""
    d["structure"]["pitch_bearing_friction_W"] = 10.0
    d["structure"]["pitch_bearing_plain_alternative_W"] = 530.0
    return d


case("pitch bearing friction large enough to be a budget line is rejected",
     False, bearing_friction_off_the_budget)


def wear_floor_missed_under_a_low_overspeed(d):
    """The one shape where the oscillating floor is the binding constraint. At the design
    1.20 overspeed a 1.5 strength margin already implies a static safety factor of 2.16,
    so the wear floor never bites. Drop the declared overspeed to 1.10 and it does: this
    tree clears every strength margin, clears the overspeed case at 1.60, and still runs
    the pitch bearing at 1.936 against a floor of 2.0."""
    st = d["structure"]
    ov, fc = 1.10, st["centrifugal_load_N"]
    st["overspeed_factor"] = ov
    st["centrifugal_load_overspeed_N"] = fc * ov ** 2
    st["blade_attachment_allowable_N"] = fc * ov ** 2 * 1.6
    st["blade_attachment_margin"] = st["blade_attachment_allowable_N"] / fc
    st["blade_attachment_margin_overspeed"] = 1.6
    st["blade_combined_margin_overspeed"] = st["blade_allowable_Nm"] / (
        (st["blade_root_bending_Nm"] + st["blade_centrifugal_bending_Nm"]) * ov ** 2)
    st["pitch_bearing_static_safety"] = (st["blade_attachment_allowable_N"] / 2.0
                                         / st["pitch_bearing_load_N"])
    return d


case("a pitch bearing that clears strength and misses the wear floor is rejected",
     False, wear_floor_missed_under_a_low_overspeed)


def one_derate_for_the_winner(d):
    """The loser derated harder than the winner. Both rows stay self consistent on their
    own terms, the winner still covers the design point, and the comparison is rigged.
    Nothing checked that the same derate reached every row until now."""
    x = d["drive_candidates"][1]
    x["continuous_power_W"] = x["max_power_180s_W"] * 0.70
    x["continuous_current_A"] = x["peak_current_180s_A"] * 0.70
    x["continuous_torque_Nm"] = 9.5493 / x["kv"] * x["continuous_current_A"]
    return d


case("a shortlist with a different derate on each row is rejected", False,
     one_derate_for_the_winner)


def design_point_outgrows_the_drive(d):
    """A design point that has grown past the derate it was chosen under. Power still fits,
    which is what the older gate reads, and current does not. The fixture recomputes the
    voltage drop and the speed fraction off the higher current, so the speed rule still
    passes and the current gate is the only thing left standing."""
    p, x = d["performance"], d["drive_candidates"][0]
    p["motor_input_current_A"] = 70.0
    p["motor_current_frac_180s"] = 70.0 / x["peak_current_180s_A"]
    p["pack_voltage_loaded_V"] = (p["pack_voltage_nominal_V"]
                                  - 70.0 * x["internal_resistance_ohm"])
    p["motor_speed_ceiling_rpm"] = x["kv"] * p["pack_voltage_loaded_V"]
    p["motor_rpm_frac_ceiling"] = p["motor_rpm"] / p["motor_speed_ceiling_rpm"]
    return d


case("a design point drawing more than the derate allows is rejected", False,
     design_point_outgrows_the_drive)


def asserted_thrust_floor(d):
    """The stacked thrust floor written down low, so the design thrust clears it with room
    it does not have. This is the number that stops the design point being lowered to give
    the drive some air, so an asserted one is worth nothing."""
    d["performance"]["thrust_floor_stacked_N"] = 8.0
    return d


case("a stacked thrust floor the conservative mass does not give is rejected", False,
     asserted_thrust_floor)


def loosened_speed_rule(d):
    """The 90 percent motor speed rule relaxed to 95. It is the rule that emptied the
    100 mm radius row in week 2, and until now it lived in prose where nothing could
    check it."""
    d["performance"]["motor_speed_rule"] = 0.95
    return d


case("a motor speed rule looser than 90 percent is rejected", False, loosened_speed_rule)


def asserted_speed_ceiling(d):
    """A speed ceiling raised by a fifth with the fraction kept consistent with it, so the
    design looks comfortable against the rule. Only KV times the loaded pack voltage can
    say otherwise."""
    p = d["performance"]
    p["motor_speed_ceiling_rpm"] *= 1.2
    p["motor_rpm_frac_ceiling"] = p["motor_rpm"] / p["motor_speed_ceiling_rpm"]
    return d


case("a motor speed ceiling that KV and the pack do not give is rejected", False,
     asserted_speed_ceiling)


def asserted_wrinkling_stress(d):
    """The wrinkling stress written down 20 percent high, with nothing else moved. It is the
    stress that sets the blade allowable and it used to live only inside the solver, where a
    material change could not be seen from outside."""
    d["structure"]["blade_wrinkle_stress_MPa"] *= 1.2
    return d


case("a skin wrinkling stress the three moduli do not give is rejected", False,
     asserted_wrinkling_stress)


def spar_claimed_to_govern(d):
    """A spar allowable stated below the skin one, so the reported blade allowable is no
    longer the weaker of the two. Both numbers stay positive and plausible."""
    d["structure"]["blade_allow_spar_Nm"] = d["structure"]["blade_allow_skin_Nm"] * 0.5
    return d


case("a blade allowable that is not the weaker of the two paths is rejected", False,
     spar_claimed_to_govern)


def skin_band_dips_under_the_floor(d):
    """A skin modulus band whose worst point falls under 1.5 while the design point itself
    is comfortable. This is the shape a real material substitution has, and the design point
    margin alone cannot see it."""
    d["structure"]["blade_skin_band_worst_margin"] = 1.3
    return d


case("a skin modulus band that dips under the floor is rejected", False,
     skin_band_dips_under_the_floor)


def foam_downgrade_breaks_the_blade(d):
    """The lighter foam grade a shop substitutes when the specified one is off the shelf,
    taking the blade under the floor. Nothing about the design point changes."""
    d["structure"]["blade_foam_downgrade_margin"] = 1.42
    return d


case("a foam grade substitution that breaks the blade is rejected", False,
     foam_downgrade_breaks_the_blade)


def narrow_skin_band(d):
    """A band swept from 0.95 of the published modulus, which finds nothing and reports a
    healthy worst case. The band has to reach far enough down to be worth sweeping."""
    d["structure"]["blade_skin_band_low"] = 0.95
    return d


case("a skin modulus band too narrow to find anything is rejected", False, narrow_skin_band)


def solvers_run_backwards(d):
    """What tools/structure.py leaves behind when it runs before tools/linkage.py: the pitch
    link load from before the blade moved, sitting beside the one linkage.py then solved.
    Every margin on that load still reproduces from it, so the only witness is that the two
    sides of the handover disagree."""
    d["structure"]["pitch_link_load_N"] *= 0.95
    d["structure"]["pitch_link_margin"] = (d["structure"]["pitch_link_allowable_N"]
                                           / d["structure"]["pitch_link_load_N"])
    return d


case("a numbers.json written with the solvers run backwards is rejected", False,
     solvers_run_backwards)


def conservative_column_off_the_envelope(d):
    """The refined conservative column and the week 2 conservative envelope 28 percent
    apart. Every nominal line still sits inside its own 25 percent band, the stated scalar
    still sums to the budget lines, no line shrinks under growth, and both thrust to
    weight cases still clear, so the only rule left is the distance between the two
    columns. The fixture opens the gap by inflating the envelope rather than by deflating
    the budget, because the budget's floor of 105 percent of its own nominal puts the low
    side out of reach at these masses. The gate reads the distance either way."""
    for e in d["mass_envelope_g"]:
        e["conservative_g"] = round(e["conservative_g"] * 620.0 / 448.0, 4)
    return d


case("a conservative budget that walks away from the week 2 envelope is rejected",
     False, conservative_column_off_the_envelope)


def weak_shaft_combined_margin(d):
    """The one stated margin check.py cannot recompute, because the shaft section
    properties live in the solver and not in numbers.json. It still has a floor, and a
    margin the gate has nothing at all to say about is a decorative row in a table that
    claims every row is gated."""
    d["structure"]["shaft_combined_margin"] = 1.2
    return d


case("a shaft combined margin below the floor is rejected", False,
     weak_shaft_combined_margin)


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


def force_map_that_never_turns(d):
    """Same claimed range, same commands, and a force that points the same way at all of
    them. Comparing vector_range_deg with phase_authority_deg cannot see this."""
    for r in d["vector_map"]:
        r["vertical_force_N"] = d["performance"]["thrust_N"]
        r["lateral_force_N"] = 0.0
    return d


case("a force map whose direction never turns is rejected", False,
     force_map_that_never_turns, week=3)


def force_map_clustered_at_zero(d):
    """Three commands within 10 degrees of each other, offered as evidence for 360."""
    thrust = d["performance"]["thrust_N"]
    d["vector_map"] = [
        {"phase_command_deg": ph,
         "vertical_force_N": thrust * math.cos(math.radians(ph)),
         "lateral_force_N": thrust * math.sin(math.radians(ph))}
        for ph in (0.0, 5.0, 10.0)]
    return d


case("a force map clustered at one command cannot evidence the claimed range", False,
     force_map_clustered_at_zero, week=3)


def command_outside_the_authority(d):
    """Commands the mechanism cannot reach, mapped as though it could."""
    thrust = d["performance"]["thrust_N"]
    d["vector_map"] = [
        {"phase_command_deg": ph,
         "vertical_force_N": thrust * math.cos(math.radians(ph)),
         "lateral_force_N": thrust * math.sin(math.radians(ph))}
        for ph in (-200.0, 0.0, 200.0)]
    return d


case("a mapped phase command outside the mechanism's authority is rejected", False,
     command_outside_the_authority, week=3)


def overstated_peak_lateral(d):
    d["pitch"]["peak_lateral_force_N"] *= 1.5
    return d


case("a peak lateral force the load table does not show is rejected", False,
     overstated_peak_lateral, week=3)


def untrimmed_lateral_column(d):
    """A side force left where it fell, with the stated peak moved to match so only the
    trim gate can catch it."""
    bias = 0.3 * sum(r["normal_force_N"] for r in d["aero_azimuthal_loads"]) / len(
        d["aero_azimuthal_loads"])
    for r in d["aero_azimuthal_loads"]:
        r["lateral_force_N"] += bias
    d["pitch"]["peak_lateral_force_N"] = max(
        abs(r["lateral_force_N"]) for r in d["aero_azimuthal_loads"])
    return d


case("a lateral load column that does not average out is rejected", False,
     untrimmed_lateral_column, week=3)


def lateral_column_deleted(d):
    """Week 3 added the column and week 4 inherits the load off it. Dropping it used to
    leave every gate green, because the check that reads it skipped a table without it."""
    for r in d["aero_azimuthal_loads"]:
        del r["lateral_force_N"]
    del d["pitch"]["peak_lateral_force_N"]
    return d


case("deleting the lateral load column is rejected", False, lateral_column_deleted, week=3)


def peak_lateral_deleted(d):
    del d["pitch"]["peak_lateral_force_N"]
    return d


case("a missing peak lateral force is rejected", False, peak_lateral_deleted, week=3)


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


def marker_only_in_the_instructions(root, data):
    """Status block says PENDING while the prose above it explains how to write the CONFIRMED
    form. A whole-file substring search passed this, so the marker gating final staging was
    satisfied by the sentence telling a person to write it later."""
    p = root / "stage-1" / "human-gate.md"
    head, sep, status = p.read_text(encoding="utf-8").partition("## Status")
    p.write_text(head + sep + status.replace("TECHNICAL-READ-COMPLETE",
                                             "TECHNICAL-READ-PENDING"), encoding="utf-8")


case("a marker named only in the instructions does not count as confirmed",
     False, upto=5, week=5, tweak=marker_only_in_the_instructions)


def status_block_removed(root, data):
    """No status heading at all. Fails closed rather than falling back to the whole file."""
    p = root / "stage-1" / "human-gate.md"
    p.write_text(p.read_text(encoding="utf-8").replace("## Status", "Markers"), encoding="utf-8")


case("a human gate file with no status block is rejected",
     False, upto=5, week=5, tweak=status_block_removed)


def marker_buried_in_a_sentence(root, data):
    """Present inside the block, but as part of a sentence rather than on its own line."""
    p = root / "stage-1" / "human-gate.md"
    p.write_text(p.read_text(encoding="utf-8").replace(
        "\nROSTER-CONFIRMED", "\nthe roster is ROSTER-CONFIRMED as of today"), encoding="utf-8")


case("a marker buried in a sentence does not count as confirmed",
     False, upto=5, week=5, tweak=marker_buried_in_a_sentence)


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


def stub_item_seven(root, data):
    """Three headings and nothing under them. This passed week 5 until item 7 got the
    substance floor every other design document already had."""
    (root / "stage-1" / "design" / "07-team-and-execution.md").write_text(
        chr(10).join(["# Team capability", "", "## Execution plan", "", "## Stage 2", ""]),
        encoding="utf-8")


case("item 7 as three headings and no content is rejected", False, upto=5, week=5,
     tweak=stub_item_seven)


def item_seven_number_off(root, data):
    """A declared value that is not the one in numbers.json."""
    p = root / "stage-1" / "design" / "07-team-and-execution.md"
    p.write_text(p.read_text(encoding="utf-8").replace(
        f"- geometry.radius_m = {data['geometry']['radius_m']}",
        f"- geometry.radius_m = {data['geometry']['radius_m'] * 1.5}"), encoding="utf-8")


case("item 7 declaring a number numbers.json does not have is rejected", False,
     upto=5, week=5, tweak=item_seven_number_off)


def front_matter_on_the_submission(root, data):
    """The real submission opens with a pandoc header, and `geometry: margin=25mm` in it
    used to be reported as a length the design had not justified. Whole-week version of
    the coverage probes further down."""
    p = root / SUB
    p.write_text('---\ntitle: "CycloProp Stage 1"\ngeometry: margin=25mm\n'
                 'fontsize: 11pt\n---\n\n' + p.read_text(encoding="utf-8"),
                 encoding="utf-8")


case("a submission carrying a pandoc front matter block passes", True,
     upto=5, week=5, tweak=front_matter_on_the_submission)


def pdf_selftests():
    """Read the built submission back the way check.py does.

    xelatex sets "off" as one ligature glyph and pypdf returns it that way, so a gate
    string carrying a double f would miss on a perfectly good PDF. The contents page also
    puts a space inside "Team" from kerning while the body heading extracts cleanly. Both
    are handled in check.py rather than worked around at each call site, and this is the
    check that they stay handled. Reads the real file and never writes."""
    pdf = REPO / "stage-1" / "submission" / "cycloprop-stage1.pdf"
    if not pdf.is_file():
        return [("the built submission is present to read back", False, "no PDF")]
    sys.path.insert(0, str(CHECK.parent))
    import check as chk
    pages, text = chk.pdf_text(pdf)
    left = [g for g in chk.LIGATURES if g in text]
    out = [("the PDF reader hands back no ligature glyphs", not left,
            "clean" if not left else f"{len(left)} glyph(s) survived")]
    out.append(("a double f word is findable in the extracted text", "off" in text,
                "found" if "off" in text else "the ligature is still one character"))
    flat = "".join(text.split()).lower()
    want = "".join("Team capability and execution plan".split()).lower()
    out.append(("a heading broken by kerning still matches", want in flat,
                f"{pages} pages read"))
    return out


def solver_selftests():
    """Rerun the two solvers against copies of the repository and see what comes back.

    `numbers.json` is written by tools/linkage.py and then by tools/structure.py, in that
    order, because linkage.py imports the blade build-up from structure.py and structure.py
    reads the pitch link load back. The order was resolved by hand, written into two
    docstrings, and checked nowhere.

    Three things get checked. The pair reproduces the committed file byte for byte, which
    catches a hand edit and a stale run at once. From that converged file the reverse order
    reproduces it too, because each script is sitting on its own fixed point, so a
    reproducibility check on its own would say the order does not matter. Move the chord two
    millimetres and it does: the reverse order leaves structure.pitch_link_load_N at the
    value from before the blade moved while pitch.peak_link_force_N carries the new one.
    That gap is what check_solver_order reads, and the third case is that the gate sees it.

    Both scripts resolve their paths from __file__, so each copy keeps the shape of the
    repository. Nothing here writes to the real one."""
    out = []
    real = REPO_NUMBERS.read_bytes()
    tmp = tempfile.mkdtemp(prefix="cyclo-solver-")

    def run_pair(where, order, chord=None):
        root = Path(tmp) / where
        (root / "tools").mkdir(parents=True)
        (root / "stage-1" / "design").mkdir(parents=True)
        for f in ("linkage.py", "structure.py"):
            shutil.copy2(CHECK.parent / f, root / "tools" / f)
        target = root / "stage-1" / "design" / "numbers.json"
        if chord is None:
            target.write_bytes(real)
        else:
            d = json.loads(real.decode("utf-8"))
            d["geometry"]["chord_m"] = chord
            target.write_text(json.dumps(d, indent=2, ensure_ascii=False) + chr(10),
                              encoding="utf-8", newline=chr(10))
        for script in order:
            r = subprocess.run([sys.executable, str(root / "tools" / script), "--write"],
                               capture_output=True, text=True)
            if r.returncode != 0:
                return None, f"{script} exited {r.returncode}: {r.stderr.strip()[:120]}"
        return target, None

    try:
        fwd, err = run_pair("converged-forward", ("linkage.py", "structure.py"))
        same = err is None and fwd.read_bytes() == real
        out.append(("the two solvers reproduce numbers.json byte for byte", same,
                    err or ("identical" if same else "differs from the committed file")))

        rev, err = run_pair("converged-reverse", ("structure.py", "linkage.py"))
        same = err is None and rev.read_bytes() == real
        out.append(("from a converged file the order makes no difference", same,
                    err or ("identical, which is why reproducibility is not the test"
                            if same else "differs")))

        moved, err = run_pair("moved-reverse", ("structure.py", "linkage.py"), chord=0.0740)
        gap = None
        if err is None:
            d = json.loads(moved.read_text(encoding="utf-8"))
            gap = (d["structure"]["pitch_link_load_N"], d["pitch"]["peak_link_force_N"])
        caught = gap is not None and abs(gap[0] - gap[1]) > 1e-6
        out.append(("with the chord moved, the wrong order leaves a gap the gate reads",
                    caught, err or (f"{gap[0]} N beside {gap[1]} N" if gap else "no gap")))

        ok_fwd, err = run_pair("moved-forward", ("linkage.py", "structure.py"), chord=0.0740)
        clean = None
        if err is None:
            d = json.loads(ok_fwd.read_text(encoding="utf-8"))
            clean = (d["structure"]["pitch_link_load_N"], d["pitch"]["peak_link_force_N"])
        agreed = clean is not None and abs(clean[0] - clean[1]) < 1e-6
        out.append(("with the chord moved, the documented order closes it", agreed,
                    err or (f"{clean[0]} N on both sides" if clean else "no values")))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return out


def loop_residual(rows, R, e, a, l, alpha0, phi_deg=90.0):
    """Worst distance by which the pitch link fails to reach the offset pivot.

    Deliberately independent of `linkage.py`: it puts the horn where the published pitch
    angle says it is, then asks whether the link still spans the gap. A hand-written table
    does not survive it. One degree of edit on one row shows up as 0.37 mm.
    """
    ex, ey = e * math.cos(math.radians(phi_deg)), e * math.sin(math.radians(phi_deg))
    worst = 0.0
    for r in rows:
        az = r["azimuth_deg"]
        psi, alpha = math.radians(az), math.radians(r["pitch_deg"] + az + alpha0)
        hx = R * math.cos(psi) + a * math.cos(alpha)
        hy = R * math.sin(psi) + a * math.sin(alpha)
        worst = max(worst, abs(math.hypot(hx - ex, hy - ey) - l))
    return worst


# --------------------------------------------------------------------------------------
# The 1 September gates. Every one of these passed before the gate beside it was written,
# and most of them are the review's own findings turned into fixtures.


def blade_allowable_raised(d):
    """Raise the blade allowable and every margin that hangs off it, leaving the section
    and the moduli where they are. The old gate compared the allowable against two other
    stored numbers, so raising all three together was free."""
    st = d["structure"]
    for k in ("blade_allowable_Nm", "blade_allow_skin_Nm", "blade_allow_spar_Nm"):
        st[k] *= 1.30
    for k in ("blade_margin", "blade_combined_margin", "blade_combined_margin_overspeed",
              "blade_skin_band_worst_margin", "blade_foam_downgrade_margin"):
        st[k] *= 1.30
    return d


case("a blade allowable raised above its own section is rejected", False,
     blade_allowable_raised)


def foam_a_thousand_times_softer(d):
    """Foam three orders of magnitude softer, with the wrinkling stress moved consistently
    so the one gate that did recompute stays satisfied. The allowable stays put, because
    nothing connected the section to it, and the blade still reported a 2.0 overspeed
    margin."""
    st = d["structure"]
    st["blade_foam_modulus_MPa"] /= 1000.0
    st["blade_foam_shear_MPa"] /= 1000.0
    st["blade_wrinkle_stress_MPa"] /= 100.0
    return d


case("foam a thousand times softer with the allowable held is rejected", False,
     foam_a_thousand_times_softer)


def shaft_allowable_inflated(d):
    st = d["structure"]
    st["shaft_allowable_Nm"] *= 1.5
    st["shaft_margin"] = st["shaft_allowable_Nm"] / st["shaft_torque_Nm"]
    return d


case("a shaft allowable that does not come from the tube is rejected", False,
     shaft_allowable_inflated)


def link_allowable_inflated(d):
    st = d["structure"]
    st["pitch_link_allowable_N"] *= 1.5
    st["pitch_link_margin"] = st["pitch_link_allowable_N"] / st["pitch_link_load_N"]
    return d


case("a pitch link allowable that does not come from the horn is rejected", False,
     link_allowable_inflated)


def attachment_on_an_unnamed_listing(d):
    """A supplier listing 24 percent above what ISO 76 gives for this ball complement. It
    carries the tightest margin in the module and no supplier is named."""
    st = d["structure"]
    st["blade_attachment_allowable_N"] = 2 * 270.0
    st["blade_attachment_margin"] = 540.0 / st["centrifugal_load_N"]
    st["blade_attachment_margin_overspeed"] = 540.0 / st["centrifugal_load_overspeed_N"]
    st["pitch_bearing_static_safety"] = 270.0 / st["pitch_bearing_load_N"]
    return d


case("an attachment rating above what ISO 76 gives is rejected", False,
     attachment_on_an_unnamed_listing)


def current_from_power_over_volts(d):
    """The quotient a spreadsheet reaches for. It is the draw of an ideal resistor and it
    runs low by roughly the efficiency, which is exactly the direction that flatters a
    drive selection."""
    p = d["performance"]
    amps = p["motor_input_W"] / p["pack_voltage_nominal_V"]
    p["motor_input_current_A"] = amps
    sel = [x for x in d["drive_candidates"] if x.get("selected")][0]
    p["motor_current_frac_180s"] = amps / sel["peak_current_180s_A"]
    p["pack_voltage_loaded_V"] = (p["pack_voltage_nominal_V"]
                                  - amps * sel["internal_resistance_ohm"])
    p["motor_speed_ceiling_rpm"] = sel["kv"] * p["pack_voltage_loaded_V"]
    p["motor_rpm_frac_ceiling"] = p["motor_rpm"] / p["motor_speed_ceiling_rpm"]
    return d


case("motor current taken as input power over pack voltage is rejected", False,
     current_from_power_over_volts)


def idle_current_dropped(d):
    p = d["performance"]
    p["motor_input_current_A"] -= p.pop("motor_idle_current_A")
    sel = [x for x in d["drive_candidates"] if x.get("selected")][0]
    p["motor_current_frac_180s"] = p["motor_input_current_A"] / sel["peak_current_180s_A"]
    p["pack_voltage_loaded_V"] = (p["pack_voltage_nominal_V"] - p["motor_input_current_A"]
                                  * sel["internal_resistance_ohm"])
    p["motor_speed_ceiling_rpm"] = sel["kv"] * p["pack_voltage_loaded_V"]
    p["motor_rpm_frac_ceiling"] = p["motor_rpm"] / p["motor_speed_ceiling_rpm"]
    return d


case("dropping the published idle current from the draw is rejected", False,
     idle_current_dropped)


def torque_above_the_continuous_rating(d):
    sel = [x for x in d["drive_candidates"] if x.get("selected")][0]
    tq = sel["continuous_torque_Nm"] * 1.15
    d["structure"]["motor_shaft_torque_Nm"] = tq
    d["performance"]["motor_torque_Nm"] = tq
    d["performance"]["motor_input_current_A"] = (tq / (9.5493 / sel["kv"])
                                                 + d["performance"]["motor_idle_current_A"])
    return d


case("a motor shaft torque above the continuous rating is rejected", False,
     torque_above_the_continuous_rating)


def servo_torque_divided_by_the_ratio(d):
    """The gear pair steps the carrier angle up, so it steps the servo torque up too. This
    divides, which is the direction that makes a 1.04 margin read 2.33."""
    p = d["pitch"]
    p["servo_torque_Nm"] = p["carrier_torque_Nm"] / p["gear_step_up"] / p["actuator_count"]
    p["servo_torque_margin"] = p["servo_stall_torque_Nm"] * 0.5 / p["servo_torque_Nm"]
    return d


case("a servo torque divided by the gear ratio instead of multiplied is rejected", False,
     servo_torque_divided_by_the_ratio)


def servo_margin_on_full_stall(d):
    p = d["pitch"]
    p["servo_torque_margin"] = p["servo_stall_torque_Nm"] / p["servo_torque_Nm"]
    return d


case("a servo margin taken on full stall instead of half is rejected", False,
     servo_margin_on_full_stall)


def transmission_angle_too_tight(d):
    d["pitch"]["transmission_angle_max_deg"] = 145.0
    return d


case("a four-bar transmission angle inside 40 degrees is rejected", False,
     transmission_angle_too_tight)


def fm_held_while_the_coefficient_is_cut(d):
    """Take the thrust coefficient below the rotor it was measured on and keep that rotor's
    figure of merit. The two came off one operating point and they are not independent, so
    this spends the thrust conservatism a second time as a power optimism."""
    d = _measured(d)
    src = d["coefficient_scenarios"][-1]
    d["performance"]["figure_of_merit"] = src["figure_of_merit"]
    d["performance"]["aero_power_W"] = (d["performance"]["ideal_power_W"]
                                        / src["figure_of_merit"])
    return d


case("a figure of merit held while the coefficient is cut is rejected", False,
     fm_held_while_the_coefficient_is_cut, upto=2, week=2)


def one_line_covering_two_components(d):
    """One budget line named for two components at once. Under a substring search over the
    joined names this satisfied motor AND mount, so a module with no motor in it passed the
    gate whose only job is to stop that."""
    for b in d["mass_budget_g"]:
        if b["item"] == "motor":
            b["item"] = "motor mount bracket and fasteners"
        elif b["item"] == "mounting hardware and fasteners":
            b["item"] = "harness and fasteners"
    return d


case("one budget line standing in for two components is rejected", False,
     one_line_covering_two_components)


def drive_selected_but_not_carried(d):
    """A 900 g motor selected, and the budget still carrying the 62 g one. mass_g was
    required by the row shape and read by nothing."""
    for x in d["drive_candidates"]:
        if x.get("selected"):
            x["mass_g"] = 900.0
    return d


case("a selected drive the budget does not carry is rejected", False,
     drive_selected_but_not_carried)


def bom_line_cost_does_not_multiply(d):
    d["bom"][2]["line_cost_inr"] = 1500
    return d


case("a BOM line cost that does not multiply out is rejected", False,
     bom_line_cost_does_not_multiply)


def bom_total_asserted(d):
    d["results"]["bom_total_inr"] = 20000
    return d


case("a BOM total that does not sum the rows is rejected", False, bom_total_asserted)


def bom_source_says_nothing(d):
    d["bom"][0]["source"] = "a shop"
    return d


case("a BOM row whose source names no origin is rejected", False, bom_source_says_nothing)


def candidate_tw_inflated(d):
    """The winner's own thrust to weight, raised. Neither column was ever recomputed from
    the row's own mass and thrust, so the worst of three could be declared the winner."""
    for x in d["configuration_candidates"]:
        if x.get("selected"):
            x["module_tw_conservative"] *= 1.25
            x["module_tw"] *= 1.25
    return d


case("a candidate thrust to weight that does not come from its own row is rejected", False,
     candidate_tw_inflated, upto=2, week=2)


def chain_shaved_four_times(d):
    """Four links, each shaved by 1.95 percent, each comparing against the previous stored
    value. Under the old 2 percent allowance every link passed and the overspeed margin came
    out 5 percent better than the geometry supports."""
    st = d["structure"]
    st["blade_mass_kg"] *= 0.9805
    st["centrifugal_load_N"] *= 0.9805 ** 2
    st["blade_centrifugal_bending_Nm"] *= 0.9805 ** 3
    st["centrifugal_load_overspeed_N"] *= 0.9805 ** 3
    return d


case("a structural chain shaved 1.95 percent at every link is rejected", False,
     chain_shaved_four_times)


def swept_diameter_deleted(d):
    """Delete the key and the gate that reads it vanishes with it. Week 2 protects its block
    with a schema list and the later blocks did not copy the pattern."""
    d["packaging"].pop("swept_diameter_mm")
    return d


case("deleting a stored key to make its gate disappear is rejected", False,
     swept_diameter_deleted)


def linkage_selftests():
    """Read-only checks that the stored week 3 numbers still come from the mechanism.

    Returns a list of (name, ok, detail). A tree with no numbers.json at all is genuinely
    before week 3 and skips, which is the one case this may be silent about.

    A tree that HAS a numbers.json and is missing a link dimension does not skip. It used to:
    the whole suite returned an empty list and reported success, so deleting one of the five
    dimensions switched off the four-bar closure check and nothing said so. Three of those
    five were required by no gate either, which is now fixed in week3.
    """
    if not REPO_NUMBERS.is_file():
        return []
    d = json.loads(REPO_NUMBERS.read_text(encoding="utf-8"))
    p, g = d.get("pitch") or {}, d.get("geometry") or {}
    rows = d.get("pitch_schedule") or []
    need = ("offset_m", "horn_m", "pitch_link_m", "construction_angle_deg",
            "phase_delay_deg")
    absent = [k for k in need if p.get(k) is None]
    if not rows or absent:
        return [("the four-bar closure check has the dimensions it needs", False,
                 ("no pitch_schedule rows" if not rows else
                  "pitch is missing " + ", ".join(absent))
                 + ", so the closure check cannot run and this is a failure rather than "
                   "a skip")]

    args = (g["radius_m"], p["offset_m"], p["horn_m"], p["pitch_link_m"],
            p["construction_angle_deg"])
    out = []
    res = loop_residual(rows, *args)
    out.append(("every published pitch row closes the four-bar loop", res < 1e-6,
                f"worst {res:.2e} m"))

    edited = [dict(r) for r in rows]
    edited[len(edited) // 3]["pitch_deg"] += 1.0
    bad = loop_residual(edited, *args)
    out.append(("one degree of hand editing breaks that closure", bad > 1e-5,
                f"worst {bad:.2e} m"))

    amp = g.get("pitch_amplitude_deg")
    cosine = [{"azimuth_deg": r["azimuth_deg"],
               "pitch_deg": amp * math.cos(math.radians(
                   r["azimuth_deg"] - 90.0 - p["phase_delay_deg"]))} for r in rows]
    cos_res = loop_residual(cosine, *args)
    out.append(("a target cosine is not a linkage solution", cos_res > 1e-5,
                f"worst {cos_res:.2e} m"))

    if p.get("servo_travel_deg") and p.get("gear_step_up"):
        want = p["servo_travel_deg"] * p["gear_step_up"]
        out.append(("phase authority is servo travel times the gear ratio",
                    abs(p["phase_authority_deg"] - want) < 1e-6,
                    f"{p['phase_authority_deg']} deg against {want:.1f}"))
    if p.get("actuator_mass_g") is not None:
        env = [x for x in d.get("mass_envelope_g") or []
               if x.get("item") == "vectoring actuator"]
        if env:
            out.append(("the actuator mass matches the week 2 envelope line",
                        abs(p["actuator_mass_g"] - env[0]["nominal_g"]) < 1e-6,
                        f"{p['actuator_mass_g']} g against {env[0]['nominal_g']} g"))
    if p.get("carrier_torque_Nm") and p.get("servo_torque_Nm"):
        want = p["carrier_torque_Nm"] / p["gear_step_up"] / p["actuator_count"]
        out.append(("servo torque follows from the carrier torque it holds",
                    abs(want - p["servo_torque_Nm"]) < 5e-4,
                    f"{p['servo_torque_Nm']} Nm against {want:.4f}"))
    return out


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
            ANNOUNCED.append(1)
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
        ANNOUNCED.append(1)
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
        ANNOUNCED.append(1)
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
        ANNOUNCED.append(1)
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
            ANNOUNCED.append(1)
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
            ANNOUNCED.append(1)
            print(("ok    " if ok else "BROKE ") + name +
                  f"   [expected {'pass' if want_pass else 'fail'}, got {'pass' if got else 'fail'}]")
            if not ok:
                failures.append((name, ""))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # Front matter is build configuration and the audit skips it. The point of the last
    # two probes is that the skip is positional: the same setting written into the body
    # is a claim, and a real untraced number in the body still fails with a front matter
    # block sitting above it.
    tmp = tempfile.mkdtemp(prefix="cyclo-gate-")
    try:
        data = honest_numbers()
        chk.set_root(tmp)
        fm = chr(10).join(["---", 'title: "CycloProp Stage 1"', "geometry: margin=25mm",
                           "fontsize: 11pt", "---", ""])
        probes = [
            ("a page margin in the front matter is not a design claim",
             fm + chr(10) + "The requirement is at least 10 N.", True),
            ("an untraced number in the body still fails under front matter",
             fm + chr(10) + "The module produces 999 N of thrust.", False),
            ("the same margin setting in the body is a claim and fails",
             "The page is set with margin=25mm in the body text.", False),
            # An opening delimiter with no closing one is not front matter, so the setting
            # under it is read as a claim and fails. Without this rule a stray rule on line
            # 1 hides a whole document.
            ("an unterminated opening delimiter is not front matter",
             chr(10).join(["---", "geometry: margin=25mm", "", "Body text follows."]), False),
            # No blank line under the closing delimiter. If the block length were one line
            # long the body line would be skipped and this would pass.
            ("the line straight under the closing delimiter is still body",
             fm.rstrip(chr(10)) + chr(10) + "The module produces 999 N of thrust.", False),
        ]
        for name, text, want_pass in probes:
            (Path(tmp) / "t.md").write_text(text, encoding="utf-8")
            chk.FAILURES.clear()
            chk.check_numeric_coverage("t.md", data)
            got = not chk.FAILURES
            ok = got == want_pass
            ANNOUNCED.append(1)
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
        # The last one is the qualifier rule. A key whose unit suffix is followed by a
        # word, thrust_N_conservative, mass_g_conservative, is still a force and still a
        # mass, and while the match ran only at the end of the key the submission's own
        # conservative thrust could not trace to the number that produced it.
        amp = data["geometry"]["pitch_amplitude_deg"]
        probes = [("produces 400 N of thrust", False), ("Envelope is 400 mm long.", True),
                  ("A force of -10 N acts.", False), ("At least 10 N.", True),
                  ("| 999 N |", False),
                  (f"The conservative case gives "
                   f"{data['performance']['thrust_N_conservative']:.2f} N.", True),
                  # Angles written as words. "deg" sat before "degrees" in the alternation,
                  # so the matcher took the short branch, failed its own lookahead on the
                  # "r", and read no angle in the document at all.
                  ("The blade pitches 999 degrees.", False),
                  ("A 999 degree amplitude.", False),
                  (f"The blade pitches plus or minus {amp} degrees.", True)]
        for text, want_pass in probes:
            (Path(tmp) / "t.md").write_text(text, encoding="utf-8")
            chk.FAILURES.clear()
            chk.check_numeric_coverage("t.md", data)
            got = not chk.FAILURES
            ok = got == want_pass
            ANNOUNCED.append(1)
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
              ("--all fails on two NEXT-WEEK markers", None, None, False, "double"),
              # The marker sweep. Both of these passed a whole-file substring search, which
              # is how an audit file could satisfy its own gate by explaining the marker.
              ("--all fails when a progress file only quotes the done marker",
               None, None, False, "quote-done"),
              ("--all fails when an audit only quotes the audit marker",
               None, None, False, "quote-audit")]
    for name, drop, no_audit, want_pass, *extra in probes:
        mode = extra[0] if extra else None
        tmp = tempfile.mkdtemp(prefix="cyclo-gate-")
        try:
            build(tmp, honest_numbers(), 4)
            hand = ["# Handoff", "", "NEXT-WEEK: 5", ""]
            if mode == "double":
                hand += ["NEXT-WEEK: 3", ""]
            (Path(tmp) / "handoff.md").write_text("\n".join(hand), encoding="utf-8")
            prog = Path(tmp) / "stage-1" / "progress"
            audit = Path(tmp) / "stage-1" / "audit"
            prog.mkdir(parents=True, exist_ok=True)
            audit.mkdir(parents=True, exist_ok=True)
            for w in range(1, 5):
                if w == drop:
                    continue
                done_line = "STATUS: WEEK-COMPLETE"
                if mode == "quote-done" and w == 3:
                    done_line = ("The week is closed once somebody writes "
                                 "STATUS: WEEK-COMPLETE at the top of this file.")
                (prog / f"week-{w}.md").write_text(
                    f"# Week {w}\n\n{done_line}\n", encoding="utf-8")
                audit_line = "AUDIT-COMPLETE"
                if mode == "quote-audit" and w == 4:
                    audit_line = ("The protocol asks for a sign off line reading "
                                  "AUDIT-COMPLETE and this file does not carry one.")
                if w != no_audit:
                    (audit / f"week-{w}.md").write_text(
                        f"# Week {w} audit\n\n{audit_line}\n", encoding="utf-8")
            got_pass, out = run_all(tmp)
            ok = got_pass == want_pass
            ANNOUNCED.append(1)
            print(("ok    " if ok else "BROKE ") + name +
                  f"   [expected {'pass' if want_pass else 'fail'}, "
                  f"got {'pass' if got_pass else 'fail'}]")
            if not ok:
                failures.append((name, out))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    extra = linkage_selftests() + solver_selftests() + pdf_selftests()
    for name, ok, detail in extra:
        ANNOUNCED.append(1)
        print(("ok    " if ok else "BROKE ") + name + f"   [{detail}]")
        if not ok:
            failures.append((name, detail))

    print()
    if failures:
        print(f"{len(failures)} case(s) behaved wrongly")
        for name, out in failures:
            print(f"\n===== {name} =====\n{out}")
        return 1
    print(f"All {len(ANNOUNCED)} gate self-tests behaved as expected.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
