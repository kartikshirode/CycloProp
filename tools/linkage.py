#!/usr/bin/env python3
"""Solve the week 3 pitch linkage and rerun the week 2 azimuthal load model against it.

Run it with no arguments for a report, or with --write to push the solved values into
`stage-1/design/numbers.json`. Nothing here is fitted to a target. The offset length comes
out of a bisection on the pitch amplitude, the thrust direction comes out of a fixed point
on the inflow, and every schedule row comes from the same loop closure.

Topology follows Kellen 2019 sections 2.1.1.2 and 4.1.1.2, which name four fixed lengths:
L1 is the rotor radius, L2 the offset link from the rotor axis to the common offset pivot,
L3 the pitch link, L4 the pitch horn from the blade pitch axis to the pitch link pin. One
four-bar per blade, all three sharing the same ground link O to E.

Loop, per blade, closing at the offset pivot:

    R*u(psi) + a*u(alpha) + l*u(gamma) = e*u(phi)

with u(x) the unit vector at angle x, psi the blade azimuth, alpha the horn direction in
the fixed frame and gamma the pitch link direction. Solving it is a circle intersection.
The horn tip sits at distance a from the pitch axis and distance l from the offset pivot,
so with D = E - P, d = |D| and delta = arg(D),

    cos(alpha - delta) = (a^2 + d^2 - l^2) / (2*a*d)

which has two roots. The sign is the assembly mode and it is held for the whole
revolution. Blade pitch is alpha - psi - alpha0, where alpha0 is the construction angle
between the horn and the chord, set so the cycle mean pitch is zero.

Azimuth is measured from the offset link, so psi = 90 degrees is the direction the offset
points. That makes `pitch.phase_delay_deg` the mechanism's own lag from its command to the
pitch peak, and it leaves the aerodynamic tilt as a separate number instead of folding the
two together. Module vertical sits at 90 plus that tilt.

The aero model is week 2's, reconstructed from `04-thrust-and-power.md` and checked against
the stored table to 5.2e-5 N per row on every one of the 36 rows. Quasi-steady, uniform
inflow, thin airfoil slope, blade force taken normal to the local tangent. Week 3 changes
two things: the schedule it is fed, and the inflow direction, which now follows the
resultant instead of being pinned to the module vertical.
"""

import argparse
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import structure                                          # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
NUMBERS = ROOT / "stage-1" / "design" / "numbers.json"

# The horn started as Kellen's ratio scaled to this radius, L1 9 in and L4 2 in on his
# built cyclocopter, printed page 55, and the link was chosen off the sweep under --sweep.
# Both moved on 1 September, because the sweep was reading the wrong thing.
#
# A transmission angle of 143 degrees is as bad as one of 37. The useful quantity is the
# deviation from a right angle, so the constraint is on min(mu, 180 - mu), and the old
# 24.4 by 105.0 row folds to 36.77 degrees while its printed minimum of 58.58 looked
# comfortable. 18.0 by 108.0 is what the corrected sweep picks and it is better on every
# column at once: the worst folded angle is 44.34 degrees, the carrier torque the actuator
# holds falls from 0.1389 to 0.1363 Nm, and the schedule fits the harmonic to 1.141 degrees
# rather than 1.195. Nothing was traded for it.
#
# The pitch link force rises with the shorter horn, and the horn's own bending allowable
# rises in exactly the same proportion, so the pitch link margin does not move. L2 is
# variable on Kellen's vehicle, a linear servo sets it, so the offset here is solved.
HORN_OVER_RADIUS = 18.0 / 110.0
LINK_OVER_RADIUS = 108.0 / 110.0
SWEEP_HORN_MM = (18.0, 20.0, 22.0, 24.4, 26.0, 30.0, 36.0)
SWEEP_LINK_MM = (100.0, 105.0, 108.0, 111.6, 118.0)
TRANSMISSION_FLOOR_DEG = 40.0     # standard four-bar practice, and the sweep's constraint

# The azimuthal load table week 2 published, frozen here at commit 1e1e15f. It is the
# reference the model reconstruction is checked against, and it is carried as a constant
# rather than read from numbers.json because --write replaces that table with the week 3
# one. Reading the live table made the script pass once and then disable itself.
WEEK2_PUBLISHED_THRUST_N = 18.0   # the design point the table below was published at
WEEK2_PUBLISHED_LOADS = [
    (0, 0.0), (10, 0.7483), (20, 2.8299), (30, 5.7943), (40, 9.0109), (50, 11.8165),
    (60, 13.6651), (70, 14.243), (80, 13.521), (90, 11.7337), (100, 9.2966), (110,
    6.6858), (120, 4.318), (130, 2.4624), (140, 1.208), (150, 0.4889), (160, 0.1506),
    (170, 0.0272), (180, 0.0), (190, 0.0272), (200, 0.1506), (210, 0.4889), (220,
    1.208), (230, 2.4624), (240, 4.318), (250, 6.6858), (260, 9.2966), (270, 11.7337),
    (280, 13.521), (290, 14.243), (300, 13.6651), (310, 11.8165), (320, 9.0109), (330,
    5.7943), (340, 2.8299), (350, 0.7483),
]

SCHEDULE_STEP_DEG = 10.0          # 36 rows, the same azimuths week 2 used
FINE_STEP_DEG = 0.25              # what the extrema, clearances and derivatives use
STALL_CAP_DEG = 28.0              # week 2's stand-in for dynamic stall delay
OFFSET_AZIMUTH_DEG = 90.0         # azimuth reference: psi = 90 is the offset direction

# Blade build-up. This used to be a hand copy of the week 2 masses, which week 3 recorded
# as a debt because nothing made it follow a change to the blade. It now comes from
# `tools/structure.py`, the same integration that builds the week 4 blade budget lines, so
# the pitch loads and the mass budget cannot disagree about what a blade weighs. Stations
# are the chordwise centre of each part as a fraction of chord.
SPAR_STATION = 0.30               # spar tube on the pitch axis
FITTING_STATION = 0.30            # root fittings on the pitch axis
AERO_CENTRE_PCT = 25.0            # thin airfoil, quarter chord


def blade_parts_g(chord_m, span_m):
    """Part masses of one blade, in grams, keyed by the station they sit at."""
    bl = structure.blade(chord_m, span_m)
    return {"foam": bl["m_foam_g"], "skin": bl["m_skin_g"], "spar": bl["m_spar_g"],
            "bond and fittings": bl["m_close_out_g"]}

# Actuator, a 20 g class digital metal gear servo. Supplier listing rather than a
# manufacturer datasheet, the same evidence class as four of the five week 2 drive rows.
#
# It used to be a 12.5 g class part at 2.2 kgf.cm, and that was sized against a servo
# torque computed with the gear ratio applied backwards. The gear pair steps the carrier
# ANGLE up, which is what the phase authority already claims, and angle amplification at
# the output is torque multiplication at the input. Corrected, the small servo holds 96
# percent of half its stall torque against a ripple that reverses three times a revolution.
# This one holds 53 percent of half stall. It costs 7.5 g each. See D67.
SERVO_MASS_G = 20.0
SERVO_STALL_TORQUE_NM = 0.3825    # 3.9 kgf.cm at 6 V
SERVO_TRAVEL_DEG = 80.0           # 40 degrees per side over a 400 us pulse excursion
SERVO_SPEED_S_PER_60DEG = 0.13    # at 6 V
SERVO_CURRENT_A = 0.35            # at 6 V
SERVO_COUNT = 2                   # both drive the phasing carrier, 180 degrees apart
SERVO_USABLE_FRACTION = 0.50      # holding torque allowed against the stall figure

# The gear pair between the phase servo and the phasing carrier. The ratio is not free:
# the carrier is a ring around the rotor axis and has to clear the offset post, so its
# pitch diameter has a floor, and any step up means the servo's sector gear is the larger
# of the two. These two diameters are the whole claim behind the phase authority.
CARRIER_GEAR_MM = 40.0
SERVO_GEAR_MM = 60.0

# Packaging allowances. Each is a named part, so the envelope is a sum and not an estimate.
SIDE_PLATE_MM = 8.0
BEARING_BLOCK_MM = 12.0
PHASING_CARRIER_MM = 16.0         # non drive end, outboard of the rotor
PULLEY_AND_BELT_MM = 18.0         # drive end
FRAME_CLEARANCE_MM = 10.0         # rotor sweep to frame tube, in the rotor plane
MOTOR_STACK_MM = 46.0             # MN5006 body plus its mount plate, below the rotor
MOUNT_POINTS = 4


def u(angle_rad):
    return math.cos(angle_rad), math.sin(angle_rad)


def wrap180(deg):
    return (deg + 180.0) % 360.0 - 180.0


def fine_azimuths():
    return [i * FINE_STEP_DEG for i in range(int(round(360.0 / FINE_STEP_DEG)))]


# ----------------------------------------------------------------- linkage kinematics


def horn_angle(psi, e, phi, a, l, R, branch):
    """Fixed frame direction of the pitch horn, or None where the loop cannot close."""
    px, py = (R * c for c in u(psi))
    ex, ey = (e * c for c in u(phi))
    dx, dy = ex - px, ey - py
    d = math.hypot(dx, dy)
    if d == 0.0:
        return None
    k = (a * a + d * d - l * l) / (2.0 * a * d)
    if abs(k) > 1.0:
        return None
    return math.atan2(dy, dx) + branch * math.acos(k)


def raw_pitch(psi, e, phi, a, l, R, branch):
    alpha = horn_angle(psi, e, phi, a, l, R, branch)
    return None if alpha is None else alpha - psi


def schedule(azimuths_deg, e, phi_deg, a, l, R, branch, alpha0):
    """Pitch in degrees at each azimuth, from the loop closure and nothing else."""
    phi = math.radians(phi_deg)
    out = []
    for az in azimuths_deg:
        r = raw_pitch(math.radians(az), e, phi, a, l, R, branch)
        if r is None:
            return None
        out.append(wrap180(math.degrees(r) - alpha0))
    return out


def construction_angle(e, phi_deg, a, l, R, branch, n=1440):
    """alpha0, the fixed horn to chord angle, set so the cycle mean pitch is zero.

    Averaged on the unit circle rather than on raw degrees, because the raw value sits
    near 270 and a naive mean would wrap through the branch cut.
    """
    phi = math.radians(phi_deg)
    sx = sy = 0.0
    for i in range(n):
        r = raw_pitch(2.0 * math.pi * i / n, e, phi, a, l, R, branch)
        if r is None:
            return None
        sx += math.cos(r)
        sy += math.sin(r)
    return math.degrees(math.atan2(sy, sx))


def amplitude(e, phi_deg, a, l, R, branch):
    """Half the peak to peak pitch travel over one revolution."""
    a0 = construction_angle(e, phi_deg, a, l, R, branch)
    if a0 is None:
        return None
    s = schedule(fine_azimuths(), e, phi_deg, a, l, R, branch, a0)
    return None if s is None else (max(s) - min(s)) / 2.0


def solve_offset(target_amp_deg, a, l, R, branch, lo=0.001, hi=None):
    """Bisect the offset length that gives the frozen pitch amplitude.

    The upper bracket is where the four-bar jams. The horn tip circle, radius a about the
    pitch axis, has to meet the pitch link circle, radius l about the offset pivot, at
    every rotor position, and the two extremes of their centre distance are R + e and
    R - e. That gives R + e - a <= l <= R - e + a, so e may not exceed either
    R + a - l or l + a - R.
    """
    if hi is None:
        hi = 0.98 * min(R + a - l, l + a - R)
    f_lo, f_hi = amplitude(lo, 0.0, a, l, R, branch), amplitude(hi, 0.0, a, l, R, branch)
    if f_lo is None or f_hi is None:
        raise SystemExit("offset bracket does not close the loop")
    if not (f_lo <= target_amp_deg <= f_hi):
        raise SystemExit(f"amplitude {target_amp_deg} outside [{f_lo:.3f}, {f_hi:.3f}]")
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        f = amplitude(mid, 0.0, a, l, R, branch)
        if f is None or f >= target_amp_deg:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)


def grashof(e, R, a, l):
    s, q, p, L = sorted([e, R, a, l])
    return {
        "shortest_mm": s * 1000.0, "longest_mm": L * 1000.0,
        "s_plus_l_mm": (s + L) * 1000.0, "p_plus_q_mm": (p + q) * 1000.0,
        "grashof": s + L <= p + q, "shortest_is_ground": abs(s - e) < 1e-12,
    }


def segment_distance(p, q, point=(0.0, 0.0)):
    px, py = p[0] - point[0], p[1] - point[1]
    qx, qy = q[0] - point[0], q[1] - point[1]
    vx, vy = qx - px, qy - py
    ll = vx * vx + vy * vy
    t = 0.0 if ll == 0.0 else max(0.0, min(1.0, -(px * vx + py * vy) / ll))
    return math.hypot(px + t * vx, py + t * vy)


def geometry_trace(e, phi_deg, a, l, R, branch, blades):
    """Every quantity that needs the linkage evaluated at every rotor position."""
    phi = math.radians(phi_deg)
    ex, ey = (e * c for c in u(phi))
    a0 = construction_angle(e, phi_deg, a, l, R, branch)
    rows = []
    for az_deg in fine_azimuths():
        psi = math.radians(az_deg)
        alpha = horn_angle(psi, e, phi, a, l, R, branch)
        if alpha is None:
            return None
        px, py = (R * c for c in u(psi))
        hx, hy = px + a * math.cos(alpha), py + a * math.sin(alpha)
        v1 = (px - hx, py - hy)                       # horn, tip back to the pitch axis
        v2 = (ex - hx, ey - hy)                       # pitch link, tip to the offset pivot
        n1, n2 = math.hypot(*v1), math.hypot(*v2)
        cosmu = (v1[0] * v2[0] + v1[1] * v2[1]) / (n1 * n2)
        link_dir = math.atan2(ey - hy, ex - hx)
        neighbours = [segment_distance((hx, hy), (ex, ey),
                                       tuple(R * c for c in u(psi + 2 * math.pi * k / blades)))
                      for k in range(1, int(blades))]
        rows.append({
            "az": az_deg, "psi": psi, "alpha": alpha,
            "pitch_deg": wrap180(math.degrees(alpha - psi) - a0),
            "mu_deg": math.degrees(math.acos(max(-1.0, min(1.0, cosmu)))),
            "link_dir": link_dir,
            "moment_arm": a * math.sin(link_dir - alpha),
            "axis_gap": segment_distance((hx, hy), (ex, ey)),
            "neighbour_gap": min(neighbours),
        })
    return a0, rows


# ----------------------------------------------------------------------- blade section


def naca_half_thickness(x, t=0.20):
    return 5.0 * t * (0.2969 * math.sqrt(x) - 0.1260 * x - 0.3516 * x * x
                      + 0.2843 * x ** 3 - 0.1015 * x ** 4)


def section_properties(chord_m, axis_frac, n=2000):
    """Area centroid, perimeter centroid and the two second moments about the pitch axis.

    Returned per unit mass with a uniform area density, so scaling by the real blade mass
    is a multiplication. `s` runs along the chord from the pitch axis towards the leading
    edge, `n` normal to it.
    """
    area = mx = i_ss = i_nn = 0.0
    per = per_x = 0.0
    prev = None
    for i in range(n + 1):
        x = i / n
        yt = naca_half_thickness(x) * chord_m
        s = (axis_frac - x) * chord_m
        if i:
            dx = chord_m / n
            area += 2.0 * yt * dx
            mx += 2.0 * yt * dx * s
            i_ss += 2.0 * yt * dx * s * s
            i_nn += (2.0 / 3.0) * yt ** 3 * dx
            seg = math.hypot(dx, yt - prev)
            per += 2.0 * seg
            per_x += 2.0 * seg * s
        prev = yt
    return {
        "area_m2": area,
        "area_centroid_pct": axis_frac * 100.0 - (mx / area) / chord_m * 100.0,
        "perimeter_centroid_pct": axis_frac * 100.0 - (per_x / per) / chord_m * 100.0,
        "i_ss_over_area": i_ss / area, "i_nn_over_area": i_nn / area,
    }


def blade_inertia(chord_m, span_m, axis_frac, blade_mass_kg):
    """Pitch inertia about the pitch axis and the chordwise offset of the blade centre.

    Uniform area density inside the section for the second moments. The centre of mass
    uses the part build-up instead, because the skin sits on the perimeter and the spar
    sits on the axis, and that moves the centre forward of the pure area centroid.
    """
    sec = section_properties(chord_m, axis_frac)
    i_p = blade_mass_kg * (sec["i_ss_over_area"] + sec["i_nn_over_area"])
    stations = {
        "foam": sec["area_centroid_pct"] / 100.0,
        "skin": sec["perimeter_centroid_pct"] / 100.0,
        "spar": SPAR_STATION,
        "bond and fittings": FITTING_STATION,
    }
    parts = blade_parts_g(chord_m, span_m)
    total = sum(parts.values())
    cg_frac = sum(parts[k] * stations[k] for k in parts) / total
    return {
        "i_p_kgm2": i_p,
        "i_ss_kgm2": blade_mass_kg * sec["i_ss_over_area"],
        "i_nn_kgm2": blade_mass_kg * sec["i_nn_over_area"],
        "cg_pct_chord": cg_frac * 100.0,
        "cg_offset_m": (axis_frac - cg_frac) * chord_m,
        "section": sec,
    }


def swept_radii(chord_m, axis_frac, rows, R):
    """Outer and inner radius of the volume the pitching blades sweep."""
    section = []
    for i in range(41):
        x = i / 40.0
        yt = naca_half_thickness(x) * chord_m
        s = (axis_frac - x) * chord_m
        section += [(s, yt), (s, -yt)]
    r_out, r_in = 0.0, 1e9
    for row in rows:
        psi, th = row["psi"], math.radians(row["pitch_deg"])
        cx, cy = u(psi + math.pi / 2.0 + th)
        nx, ny = u(psi + math.pi + th)
        bx, by = (R * c for c in u(psi))
        for s, n in section:
            r = math.hypot(bx + s * cx + n * nx, by + s * cy + n * ny)
            r_out, r_in = max(r_out, r), min(r_in, r)
    return r_out, r_in


# ---------------------------------------------------------------------------- aero model


def blade_forces(pitches_deg, azimuths_deg, tip_speed, induced, thrust_dir_deg):
    """Week 2's quasi-steady model, with the inflow direction free.

    The inflow is a uniform vector of magnitude `induced` pointing opposite
    `thrust_dir_deg`. That is what makes the model rotationally equivariant: rotate the
    schedule and the inflow together and the whole solution rotates with them.
    """
    out = []
    tau = math.radians(thrust_dir_deg)
    cap = math.radians(STALL_CAP_DEG)
    for az, th in zip(azimuths_deg, pitches_deg):
        psi = math.radians(az)
        ut = tip_speed + induced * math.sin(tau - psi)
        up = induced * math.cos(tau - psi)
        alpha = math.radians(th) - math.atan2(up, ut)
        out.append((ut * ut + up * up) * 2.0 * math.pi * max(-cap, min(cap, alpha)))
    return out


def cycle_resultant(pitches_deg, azimuths_deg, tip_speed, induced, thrust_dir_deg):
    f = blade_forces(pitches_deg, azimuths_deg, tip_speed, induced, thrust_dir_deg)
    n = len(azimuths_deg)
    fx = sum(v * math.cos(math.radians(az)) for v, az in zip(f, azimuths_deg)) / n
    fy = sum(v * math.sin(math.radians(az)) for v, az in zip(f, azimuths_deg)) / n
    return fx, fy, f


def settle_inflow(pitches_deg, azimuths_deg, tip_speed, induced, seed=90.0):
    """Fixed point where the inflow opposes the resultant it helped produce."""
    tau = seed
    for _ in range(400):
        fx, fy, _ = cycle_resultant(pitches_deg, azimuths_deg, tip_speed, induced, tau)
        step = wrap180(math.degrees(math.atan2(fy, fx)) - tau)
        if abs(step) < 1e-10:
            return tau
        tau += 0.5 * step
    return tau


# ------------------------------------------------------------------------ pitch loading


def pitch_loads(rows, omega, R, inertia, chord_m, axis_frac, forces_N, balanced):
    """Blade pitching moment, pitch link force and the torque the phasing carrier holds.

    Three moments about the blade pitch axis. The blade's own angular acceleration, which
    for a once per revolution schedule is order I*A*omega^2. The centrifugal moment, which
    on a cyclorotor acts in the section plane because the rotor axis runs parallel to the
    span, and which splits into a term on the chordwise offset of the blade centre of mass
    and a term on the difference of the two section second moments. And the aerodynamic
    moment about the axis, from the quarter chord offset.

    The default is the blade the week 2 build-up actually gives, whose centre of mass sits
    aft of the pitch axis. Passing balanced=True moves it onto the axis and shows what a
    chordwise balance would buy, which is a week 4 decision and not a stored number.
    """
    i_p = inertia["i_p_kgm2"]
    di = inertia["i_ss_kgm2"] - inertia["i_nn_kgm2"]
    m_b = inertia["blade_mass_kg"]
    cg = 0.0 if balanced else inertia["cg_offset_m"]
    arm = (axis_frac - AERO_CENTRE_PCT / 100.0) * chord_m

    th = [math.radians(r["pitch_deg"]) for r in rows]
    n = len(th)
    step = math.radians(FINE_STEP_DEG)
    out = []
    for i, r in enumerate(rows):
        d2 = (th[(i + 1) % n] - 2.0 * th[i] + th[i - 1]) / (step * step)
        m_inertia = i_p * omega * omega * d2
        m_cf = omega * omega * (0.5 * di * math.sin(2.0 * th[i])
                                - R * m_b * cg * math.cos(th[i]))
        m_aero = forces_N[i] * arm
        moment = m_inertia - m_cf - m_aero
        link_force = moment / r["moment_arm"]
        out.append({"moment_Nm": moment, "link_force_N": link_force,
                    "m_inertia_Nm": m_inertia, "m_cf_Nm": m_cf, "m_aero_Nm": m_aero})
    return out


def carrier_torque(rows, loads, e, phi_deg, blades):
    """Torque about the rotor axis at the offset pivot, and the radial force with it.

    The torque is what the phase servo holds. The radial component is what the offset
    length servo holds, since that one drives along the offset link.

    Each pitch link is a two force member, so the pin at the offset pivot takes its force
    along the link. The three blades sit 120 degrees apart, which cancels most of the once
    per revolution content and leaves the mean plus a three per revolution ripple.
    """
    phi = math.radians(phi_deg)
    n = len(rows)
    offset = int(round(n / blades))
    series, radial = [], []
    for i in range(n):
        t = f = 0.0
        for k in range(int(blades)):
            j = (i + k * offset) % n
            t += -e * loads[j]["link_force_N"] * math.sin(rows[j]["link_dir"] - phi)
            f += -loads[j]["link_force_N"] * math.cos(rows[j]["link_dir"] - phi)
        series.append(t)
        radial.append(f)
    return series, radial


# ------------------------------------------------------------------------------- solve


def solve(data, balanced=False):
    g, o, p = data["geometry"], data["operating"], data["performance"]
    R, chord, span = g["radius_m"], g["chord_m"], g["span_m"]
    blades = g["blades"]
    axis_frac = g["pitch_axis_pct_chord"] / 100.0
    amp_target = g["pitch_amplitude_deg"]
    tip, thrust = o["tip_speed_ms"], p["thrust_N"]
    induced = p["induced_velocity_ms"]
    omega = o["rpm"] * 2.0 * math.pi / 60.0
    # The blade the section build-up actually gives, not the week 2 envelope line. Those
    # two agreed until week 4 drew the root close-out, and the pitch loads follow the
    # blade rather than the estimate of it.
    blade_mass = sum(blade_parts_g(chord, span).values()) / 1000.0

    a = round(HORN_OVER_RADIUS * R * 1000.0, 1) / 1000.0
    l = round(LINK_OVER_RADIUS * R * 1000.0, 1) / 1000.0
    branch = 1.0

    e = round(solve_offset(amp_target, a, l, R, branch) * 1000.0, 2) / 1000.0
    phi = OFFSET_AZIMUTH_DEG
    a0, rows = geometry_trace(e, phi, a, l, R, branch, blades)

    fine_pitch = [r["pitch_deg"] for r in rows]
    solved_amp = (max(fine_pitch) - min(fine_pitch)) / 2.0
    peak_az = rows[fine_pitch.index(max(fine_pitch))]["az"]
    phase_delay = wrap180(peak_az - 90.0)

    az = [i * SCHEDULE_STEP_DEG for i in range(int(round(360.0 / SCHEDULE_STEP_DEG)))]
    coarse = schedule(az + [360.0], e, phi, a, l, R, branch, a0)
    model = [amp_target * math.cos(math.radians(x - 90.0 - phase_delay)) for x in az]
    rms = math.sqrt(sum((s - m) ** 2 for s, m in zip(coarse[:-1], model)) / len(model))

    # Load model on the solved schedule. The inflow settles onto the resultant, and the
    # forces are then resolved in module axes with vertical along that resultant.
    tau = settle_inflow(coarse[:-1], az, tip, induced)
    fx_r, fy_r, raw = cycle_resultant(coarse[:-1], az, tip, induced, tau)
    scale = (thrust / blades) / math.hypot(fx_r, fy_r)
    load_rows = []
    for az_deg, r in zip(az, raw):
        d = math.radians(az_deg - tau)
        load_rows.append({"azimuth_deg": az_deg,
                          "normal_force_N": round(r * scale * math.cos(d), 4),
                          "lateral_force_N": round(r * scale * math.sin(d), 4)})
    mean_v = sum(x["normal_force_N"] for x in load_rows) / len(load_rows)
    mean_l = sum(x["lateral_force_N"] for x in load_rows) / len(load_rows)
    peak_v = max(x["normal_force_N"] for x in load_rows)
    peak_lat = max(abs(x["lateral_force_N"]) for x in load_rows)
    tilt = wrap180(tau - OFFSET_AZIMUTH_DEG)

    # Pitching loads want the force on the fine grid, so rebuild it there at the same
    # scale rather than interpolating the 36 row table.
    fine_az = [r["az"] for r in rows]
    fine_force = [v * scale for v in
                  blade_forces(fine_pitch, fine_az, tip, induced, tau)]
    inertia = blade_inertia(chord, span, axis_frac, blade_mass)
    inertia["blade_mass_kg"] = blade_mass
    loads = pitch_loads(rows, omega, R, inertia, chord, axis_frac, fine_force, balanced)
    torque, radial_series = carrier_torque(rows, loads, e, phi, blades)
    hold = max(abs(t) for t in torque)
    radial = max(abs(t) for t in radial_series) * 1.0
    step_up = SERVO_GEAR_MM / CARRIER_GEAR_MM
    # Multiplied, not divided. Line 538 below turns SERVO_TRAVEL_DEG into
    # SERVO_TRAVEL_DEG * step_up of carrier phase, so the carrier turns further than the
    # servo does, and a gear pair that amplifies angle at the output multiplies torque at
    # the input. Dividing here reported 0.0463 Nm where the servos each supply 0.1022, and
    # turned an actuator margin of 1.04 into 2.33.
    servo_torque = hold * step_up / SERVO_COUNT

    r_out, r_in = swept_radii(chord, axis_frac, rows, R)
    authority = SERVO_TRAVEL_DEG * step_up

    vector = []
    for cmd in (-authority / 2.0, -authority / 4.0, 0.0, authority / 4.0, authority / 2.0):
        s_cmd = schedule(az, e, phi + cmd, a, l, R, branch,
                         construction_angle(e, phi + cmd, a, l, R, branch))
        tau_c = settle_inflow(s_cmd, az, tip, induced, seed=tau + cmd)
        fxc, fyc, _ = cycle_resultant(s_cmd, az, tip, induced, tau_c)
        mag = math.hypot(fxc, fyc) * scale * blades
        turn = wrap180(tau_c - tau)
        vector.append({
            "phase_command_deg": round(cmd, 3),
            "servo_angle_deg": round(cmd / step_up, 3),
            "vertical_force_N": round(mag * math.cos(math.radians(turn)), 4),
            "lateral_force_N": round(mag * math.sin(math.radians(turn)), 4),
            "resultant_N": round(mag, 4),
            "resultant_direction_deg": round(turn, 4),
        })

    return {
        "R": R, "a": a, "l": l, "e": e, "branch": branch, "phi": phi, "alpha0": a0,
        "azimuths": az, "schedule": coarse, "schedule_az": az + [360.0],
        "solved_amplitude_deg": solved_amp, "peak_azimuth_deg": peak_az,
        "phase_delay_deg": phase_delay, "rms_residual_deg": rms,
        "grashof": grashof(e, R, a, l),
        "transmission_min_deg": min(r["mu_deg"] for r in rows),
        "transmission_max_deg": max(r["mu_deg"] for r in rows),
        "pitch_travel_deg": max(fine_pitch) - min(fine_pitch),
        "axis_gap_mm": min(r["axis_gap"] for r in rows) * 1000.0,
        "neighbour_gap_mm": min(r["neighbour_gap"] for r in rows) * 1000.0,
        "rows": load_rows, "mean_vertical_N": mean_v, "mean_lateral_N": mean_l,
        "peak_vertical_N": peak_v, "peak_lateral_N": peak_lat,
        "peak_to_mean": peak_v / mean_v,
        "thrust_direction_deg": tau, "side_force_tilt_deg": tilt,
        "swept_outer_mm": r_out * 1000.0, "swept_inner_mm": r_in * 1000.0,
        "inertia": inertia,
        "peak_link_force_N": max(abs(x["link_force_N"]) for x in loads),
        "peak_blade_moment_Nm": max(abs(x["moment_Nm"]) for x in loads),
        "carrier_torque_Nm": hold,
        "carrier_torque_mean_Nm": sum(torque) / len(torque),
        "carrier_radial_N": radial,
        "gear_step_up": step_up,
        "servo_torque_Nm": servo_torque,
        "servo_margin": SERVO_STALL_TORQUE_NM * SERVO_USABLE_FRACTION / servo_torque,
        "phase_authority_deg": authority,
        "slew_time_s": (SERVO_TRAVEL_DEG / 60.0) * SERVO_SPEED_S_PER_60DEG,
        "actuator_power_W": SERVO_COUNT * 6.0 * SERVO_CURRENT_A,
        "envelope_length_mm": (span * 1000.0 + 2.0 * (SIDE_PLATE_MM + BEARING_BLOCK_MM)
                               + PHASING_CARRIER_MM + PULLEY_AND_BELT_MM),
        "envelope_width_mm": 2.0 * r_out * 1000.0 + 2.0 * FRAME_CLEARANCE_MM,
        "envelope_height_mm": 2.0 * r_out * 1000.0 + 2.0 * FRAME_CLEARANCE_MM
                              + MOTOR_STACK_MM,
        "vector_map": vector,
    }


def report(s):
    print("Linkage")
    print(f"  L1 rotor arm       {s['R'] * 1000:8.2f} mm  frozen by week 2")
    print(f"  L2 offset link     {s['e'] * 1000:8.2f} mm  solved for the pitch amplitude")
    print(f"  L3 pitch link      {s['l'] * 1000:8.2f} mm")
    print(f"  L4 pitch horn      {s['a'] * 1000:8.2f} mm")
    print(f"  construction angle {s['alpha0']:8.2f} deg, assembly mode "
          f"{'open' if s['branch'] > 0 else 'crossed'}")
    g = s["grashof"]
    print(f"  Grashof {g['grashof']}, s+l {g['s_plus_l_mm']:.2f} <= p+q "
          f"{g['p_plus_q_mm']:.2f}, ground is the shortest link {g['shortest_is_ground']}")
    worst = min(s["transmission_min_deg"], 180.0 - s["transmission_max_deg"])
    print(f"  transmission angle {s['transmission_min_deg']:.2f} to "
          f"{s['transmission_max_deg']:.2f} deg, worst deviation from a right angle "
          f"leaves {worst:.2f}")
    print(f"  pitch bearing travel {s['pitch_travel_deg']:.2f} deg")
    print(f"  pitch link closest approach to the rotor axis {s['axis_gap_mm']:.3f} mm")
    print(f"  pitch link closest approach to a neighbouring pitch axis "
          f"{s['neighbour_gap_mm']:.2f} mm")
    print()
    print("Schedule")
    print(f"  amplitude {s['solved_amplitude_deg']:.4f} deg, peak at "
          f"{s['peak_azimuth_deg']:.2f} deg, phase delay {s['phase_delay_deg']:.3f} deg")
    print(f"  rms residual against the harmonic {s['rms_residual_deg']:.4f} deg")
    print(f"  closure {s['schedule'][0]:.5f} at 0 against {s['schedule'][-1]:.5f} at 360")
    print()
    print("Loads")
    print(f"  cycle mean vertical {s['mean_vertical_N']:.4f} N per blade, lateral "
          f"{s['mean_lateral_N']:.2e} N")
    print(f"  peak vertical {s['peak_vertical_N']:.4f} N, peak instantaneous lateral "
          f"{s['peak_lateral_N']:.4f} N, peak to mean {s['peak_to_mean']:.4f}")
    print(f"  resultant at {s['thrust_direction_deg']:.3f} deg, so the model tilt is "
          f"{s['side_force_tilt_deg']:.3f} deg off the offset direction")
    i = s["inertia"]
    print(f"  blade pitch inertia {i['i_p_kgm2']:.3e} kg m2, centre of mass at "
          f"{i['cg_pct_chord']:.2f} pct chord")
    print(f"  peak blade pitching moment {s['peak_blade_moment_Nm']:.4f} Nm, peak pitch "
          f"link force {s['peak_link_force_N']:.2f} N")
    print()
    print("Actuator")
    print(f"  carrier torque peak {s['carrier_torque_Nm']:.4f} Nm, mean "
          f"{s['carrier_torque_mean_Nm']:.4f} Nm")
    print(f"  servo torque {s['servo_torque_Nm']:.4f} Nm each at a {s['gear_step_up']:.2f} "
          f"step up across {SERVO_COUNT} servos, margin {s['servo_margin']:.2f} on half stall")
    print(f"  radial pin force {s['carrier_radial_N']:.2f} N into the offset strut, "
          f"which is structure and not an actuator")
    print(f"  phase authority {s['phase_authority_deg']:.1f} deg, slew "
          f"{s['slew_time_s']:.3f} s end to end, draw {s['actuator_power_W']:.1f} W")
    print()
    print("Packaging")
    print(f"  swept radius {s['swept_outer_mm']:.2f} mm outer, {s['swept_inner_mm']:.2f} "
          f"mm inner")
    print(f"  envelope {s['envelope_length_mm']:.1f} x {s['envelope_width_mm']:.1f} x "
          f"{s['envelope_height_mm']:.1f} mm")
    print()
    print("Vector map, module axes with vertical along the design resultant")
    for r in s["vector_map"]:
        print(f"  cmd {r['phase_command_deg']:+7.1f} (servo {r['servo_angle_deg']:+6.1f}) "
              f"-> vertical {r['vertical_force_N']:7.3f} N, lateral "
              f"{r['lateral_force_N']:8.3f} N, resultant {r['resultant_N']:7.3f} N at "
              f"{r['resultant_direction_deg']:+7.3f} deg")


def sweep(data):
    """The table the pitch link length was chosen off. Printed rather than asserted."""
    global HORN_OVER_RADIUS, LINK_OVER_RADIUS
    keep = (HORN_OVER_RADIUS, LINK_OVER_RADIUS)
    R = data["geometry"]["radius_m"]
    print(f"{'L4_mm':>6} {'L3_mm':>7} {'L2_mm':>7} {'mu_min':>7} {'mu_max':>7} "
          f"{'sin_min':>8} {'T_car_Nm':>9} {'rms_deg':>8} {'ok':>4}")
    for l_mm in SWEEP_LINK_MM:
        for a_mm in SWEEP_HORN_MM:
            HORN_OVER_RADIUS, LINK_OVER_RADIUS = a_mm / (R * 1000.0), l_mm / (R * 1000.0)
            try:
                s = solve(data)
            except SystemExit as exc:
                print(f"{a_mm:6.1f} {l_mm:7.1f}  {exc}")
                continue
            smin = min(math.sin(math.radians(s["transmission_min_deg"])),
                       math.sin(math.radians(s["transmission_max_deg"])))
            # The folded angle, not the printed minimum. 143 degrees is as far from a right
            # angle as 37 is, and the column that says so was already being computed and
            # then ignored by the verdict beside it.
            ok = smin >= math.sin(math.radians(TRANSMISSION_FLOOR_DEG))
            print(f"{a_mm:6.1f} {l_mm:7.1f} {s['e'] * 1000:7.2f} "
                  f"{s['transmission_min_deg']:7.2f} {s['transmission_max_deg']:7.2f} "
                  f"{smin:8.4f} {s['carrier_torque_Nm']:9.4f} "
                  f"{s['rms_residual_deg']:8.3f} {str(ok):>4}")
    HORN_OVER_RADIUS, LINK_OVER_RADIUS = keep


def check_week2_model(data):
    """The reconstruction is only worth anything if it reproduces week 2's own table.

    Checked against `WEEK2_PUBLISHED_LOADS` and never against the live table, because
    `--write` replaces the live one and an earlier version of this function compared the
    reconstruction with its own output. That made the script run exactly once.

    Scaled to the thrust the stored table was published at rather than to the design point,
    so the check reads the SHAPE of the distribution. It compared against the live design
    thrust until 1 September, which meant moving the design point failed a check about
    whether the aerodynamic model still reproduces, and those are different questions.
    """
    o, p, g = data["operating"], data["performance"], data["geometry"]
    az = [a for a, _ in WEEK2_PUBLISHED_LOADS]
    stored = [v for _, v in WEEK2_PUBLISHED_LOADS]
    sched = [g["pitch_amplitude_deg"] * math.sin(math.radians(x)) for x in az]
    _, fy, raw = cycle_resultant(sched, az, o["tip_speed_ms"],
                                 p["induced_velocity_ms"], 90.0)
    scale = (WEEK2_PUBLISHED_THRUST_N / g["blades"]) / fy
    got = [r * scale * math.sin(math.radians(x)) for r, x in zip(raw, az)]
    return max(abs(x - y) for x, y in zip(got, stored))


def write_numbers(data, s):
    mm = lambda x: round(x * 1000.0, 2)
    data["pitch"].update({
        "mechanism": "passive cyclic four-bar, one per blade, sharing a common offset pivot",
        "offset_m": round(s["e"], 5),
        "horn_m": round(s["a"], 5),
        "pitch_link_m": round(s["l"], 5),
        "construction_angle_deg": round(s["alpha0"], 3),
        "phase_delay_deg": round(s["phase_delay_deg"], 3),
        "schedule_rms_residual_deg": round(s["rms_residual_deg"], 4),
        "transmission_angle_min_deg": round(s["transmission_min_deg"], 2),
        "transmission_angle_max_deg": round(s["transmission_max_deg"], 2),
        "axis_keepout_mm": round(s["axis_gap_mm"], 3),
        "neighbour_clearance_mm": round(s["neighbour_gap_mm"], 2),
        "pitch_bearing_travel_deg": round(s["pitch_travel_deg"], 2),
        "blade_pitch_inertia_kgm2": round(s["inertia"]["i_p_kgm2"], 9),
        "blade_cg_pct_chord": round(s["inertia"]["cg_pct_chord"], 2),
        "peak_blade_moment_Nm": round(s["peak_blade_moment_Nm"], 4),
        "peak_link_force_N": round(s["peak_link_force_N"], 2),
        "carrier_torque_Nm": round(s["carrier_torque_Nm"], 4),
        "gear_step_up": round(s["gear_step_up"], 4),
        "carrier_gear_mm": CARRIER_GEAR_MM,
        "servo_gear_mm": SERVO_GEAR_MM,
        "servo_mass_g": SERVO_MASS_G,
        "servo_torque_Nm": round(s["servo_torque_Nm"], 4),
        "servo_stall_torque_Nm": SERVO_STALL_TORQUE_NM,
        "servo_travel_deg": SERVO_TRAVEL_DEG,
        "servo_torque_margin": round(s["servo_margin"], 3),
        "slew_time_s": round(s["slew_time_s"], 4),
        "actuator_draw_W": round(s["actuator_power_W"], 3),
        "carrier_radial_force_N": round(s["carrier_radial_N"], 2),
        "phase_authority_deg": round(s["phase_authority_deg"], 2),
        "vector_range_deg": round(s["phase_authority_deg"], 2),
        "actuator_count": SERVO_COUNT,
        "actuator_mass_g": SERVO_COUNT * SERVO_MASS_G,
        "side_force_tilt_deg": round(abs(s["side_force_tilt_deg"]), 3),
        "peak_lateral_force_N": round(s["peak_lateral_N"], 4),
        "swept_outer_radius_mm": round(s["swept_outer_mm"], 2),
        "swept_inner_radius_mm": round(s["swept_inner_mm"], 2),
    })
    data["linkage_dimensions"] = [
        {"link": "L1 rotor arm, rotor axis to blade pitch axis", "length_mm": mm(s["R"]),
         "role": "input crank, frozen by the week 2 radius"},
        {"link": "L2 offset link, rotor axis to offset pivot", "length_mm": mm(s["e"]),
         "role": "ground link, its length sets the amplitude and its direction the phase"},
        {"link": "L3 pitch link, offset pivot to horn tip", "length_mm": mm(s["l"]),
         "role": "output crank, scaled 9.133/9 off Kellen's built vehicle"},
        {"link": "L4 pitch horn, blade pitch axis to link pin", "length_mm": mm(s["a"]),
         "role": "coupler, scaled 2/9 off Kellen's built vehicle"},
        {"link": "pitch link closest approach to the rotor axis",
         "length_mm": round(s["axis_gap_mm"], 3),
         "role": "keep-out, nothing on the axis may sit in the pitch plane"},
        {"link": "pitch link closest approach to a neighbouring pitch axis",
         "length_mm": round(s["neighbour_gap_mm"], 2),
         "role": "clearance against the next blade's root fitting"},
    ]
    data["pitch_schedule"] = [{"azimuth_deg": az, "pitch_deg": round(th, 4)}
                              for az, th in zip(s["schedule_az"], s["schedule"])]
    data["vector_map"] = s["vector_map"]
    data["aero_azimuthal_loads"] = s["rows"]
    data["performance"]["blade_load_peak_to_mean"] = round(s["peak_to_mean"], 4)
    data["packaging"] = {
        "envelope_length_mm": round(s["envelope_length_mm"], 1),
        "envelope_width_mm": round(s["envelope_width_mm"], 1),
        "envelope_height_mm": round(s["envelope_height_mm"], 1),
        "mount_points": MOUNT_POINTS,
        "swept_diameter_mm": round(2.0 * s["swept_outer_mm"], 1),
    }
    # newline="\n" on purpose. .gitattributes declares eol=lf, and the default here is the
    # platform newline, which puts CRLF into a file every sibling document writes as LF.
    # Git normalises it on the way in, so the damage does not show up in git status.
    NUMBERS.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n",
                       encoding="utf-8", newline="\n")


def main():
    ap = argparse.ArgumentParser(description="solve the week 3 pitch linkage")
    ap.add_argument("--write", action="store_true",
                    help="write the solved values into stage-1/design/numbers.json")
    ap.add_argument("--sweep", action="store_true",
                    help="print the horn and pitch link sweep the design point came from")
    ap.add_argument("--balanced", action="store_true",
                    help="show what moving the blade centre of mass onto the pitch axis buys")
    args = ap.parse_args()

    data = json.loads(NUMBERS.read_text(encoding="utf-8"))
    err = check_week2_model(data)
    print(f"week 2 model reconstruction: worst row error {err:.2e} N\n")
    if err > 1e-3:
        raise SystemExit("the reconstruction does not reproduce week 2's stored table")
    if args.sweep:
        sweep(data)
        print()
    s = solve(data, balanced=args.balanced)
    report(s)
    if args.write:
        if args.balanced:
            raise SystemExit("refusing to store the balanced case, it is a target and not "
                             "the blade the week 2 build-up describes")
        write_numbers(data, s)
        print("\nwrote stage-1/design/numbers.json")


if __name__ == "__main__":
    main()
