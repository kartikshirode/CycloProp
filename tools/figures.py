#!/usr/bin/env python3
"""Render the Stage 1 figures from numbers.json.

Usage:
    python tools/figures.py            render every figure and rewrite the manifest
    python tools/figures.py --list     name the figures and the values each one draws

Nothing here invents geometry. The four-bar comes from tools/linkage.py, the blade section
comes from tools/check.py, and every dimension is read out of numbers.json. That is the
whole point of the file: a figure is a number the reader can see, so it has to be held to
the same source as a number the reader can quote.

Each figure declares the stored values it drew and those go into figures/manifest.json.
The gate reads the manifest back against numbers.json, so a figure that was rendered before
a number moved fails the same way a stale sentence does. Regenerating is the only fix.
"""

import argparse
import json
import math
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Wedge

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check                       # noqa: E402  blade section and its constants
import linkage                     # noqa: E402  the four-bar that the schedule came from

ROOT = Path(__file__).resolve().parent.parent
NUMBERS = ROOT / "stage-1" / "design" / "numbers.json"
FIGDIR = ROOT / "stage-1" / "submission" / "figures"
MANIFEST = FIGDIR / "manifest.json"

# Vector PDF, because the reader zooms into a linkage diagram and a raster gives up. The
# fixed metadata is what keeps a re-render from showing as a diff when nothing changed.
SAVE = {"format": "pdf", "bbox_inches": "tight", "pad_inches": 0.02,
        "metadata": {"CreationDate": None, "Producer": "cycloprop tools/figures.py",
                     "Creator": "cycloprop tools/figures.py"}}

INK = "#1a1a1a"
ACCENT = "#b4462a"
COOL = "#2a5d8f"
MUTED = "#8a8a8a"
FILL = "#e8e2d8"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 8,
    "axes.edgecolor": INK,
    "axes.labelcolor": INK,
    "text.color": INK,
    "xtick.color": INK,
    "ytick.color": INK,
    "axes.linewidth": 0.6,
    "grid.linewidth": 0.4,
    "grid.color": "#cccccc",
    "lines.linewidth": 1.1,
    "legend.frameon": False,
    "figure.dpi": 200,
    "pdf.fonttype": 42,
})


def dotted(data, path):
    node = data
    for part in path.split("."):
        if isinstance(node, list):
            node = node[int(part)]
        elif isinstance(node, dict) and part in node:
            node = node[part]
        else:
            raise KeyError(path)
    return node


def rotor_axes(ax, span_mm=None):
    ax.set_aspect("equal")
    ax.axis("off")


def dim_line(ax, x0, y0, x1, y1, label, off=0.0, colour=MUTED, fs=6.5):
    """A dimension the reader can check against the caption."""
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="<->", color=colour, lw=0.5,
                                shrinkA=0, shrinkB=0))
    mx, my = (x0 + x1) / 2.0, (y0 + y1) / 2.0
    rot = 90 if abs(x1 - x0) < 1e-9 else 0
    ax.text(mx, my + off, label, ha="center", va="center", fontsize=fs,
            color=colour, rotation=rot,
            bbox=dict(fc="white", ec="none", pad=0.8))


# --------------------------------------------------------------------------- geometry


def four_bar():
    """The solved linkage, exactly as tools/linkage.py sets it up."""
    d = json.loads(NUMBERS.read_text(encoding="utf-8"))
    R = dotted(d, "geometry.radius_m")
    e = dotted(d, "pitch.offset_m")
    a = dotted(d, "pitch.horn_m")
    l = dotted(d, "pitch.pitch_link_m")
    phi = linkage.OFFSET_AZIMUTH_DEG
    branch = 1.0
    a0 = linkage.construction_angle(e, phi, a, l, R, branch)
    return d, R, e, a, l, phi, branch, a0


def blade_outline(chord_m, pitch_deg, cx, cy, axis_frac=0.30, n=120):
    """The NACA 0020 the section is drawn on, placed at a pitch angle about its axis."""
    xs, ys = [], []
    for i in range(n + 1):
        x = i / n
        xs.append(x)
        ys.append(check.naca_half_thickness(x))
    upper = list(zip(xs, ys))
    lower = list(zip(reversed(xs), [-y for y in reversed(ys)]))
    pts = upper + lower
    t = math.radians(pitch_deg)
    out = []
    for x, y in pts:
        px = (x - axis_frac) * chord_m
        py = y * chord_m
        out.append((cx + px * math.cos(t) - py * math.sin(t),
                    cy + px * math.sin(t) + py * math.cos(t)))
    return out


# ---------------------------------------------------------------------------- figures


def fig_arrangement():
    d, R, e, a, l, phi, branch, a0 = four_bar()
    R_mm = R * 1000.0
    chord = dotted(d, "geometry.chord_m") * 1000.0
    span = dotted(d, "geometry.span_m") * 1000.0
    blades = int(dotted(d, "geometry.blades"))
    r_out = dotted(d, "pitch.swept_outer_radius_mm")
    r_in = dotted(d, "pitch.swept_inner_radius_mm")
    L = dotted(d, "packaging.envelope_length_mm")
    W = dotted(d, "packaging.envelope_width_mm")
    H = dotted(d, "packaging.envelope_height_mm")
    mounts = int(dotted(d, "packaging.mount_points"))

    fig, (ax, bx) = plt.subplots(1, 2, figsize=(7.4, 3.9),
                                 gridspec_kw={"width_ratios": [1.0, 1.12]})

    # ---- rotor plane, looking along the axis
    rotor_axes(ax)
    motor = linkage.MOTOR_STACK_MM
    ax.add_patch(Rectangle((-W / 2, -W / 2 - motor), W, H, fc="none", ec=INK,
                           lw=0.8, ls=(0, (5, 3))))
    ax.add_patch(Wedge((0, 0), r_out, 0, 360, width=r_out - r_in,
                       fc=FILL, ec=MUTED, lw=0.4, alpha=0.8))
    ax.add_patch(Circle((0, 0), R_mm, fc="none", ec=MUTED, lw=0.5, ls=(0, (2, 2))))

    for k in range(blades):
        psi = 2 * math.pi * k / blades + math.radians(30.0)
        px, py = R_mm * math.cos(psi), R_mm * math.sin(psi)
        pitch = linkage.wrap180(math.degrees(
            linkage.raw_pitch(psi, e, math.radians(phi), a, l, R, branch)) - a0)
        poly = blade_outline(chord, math.degrees(psi) + 90.0 + pitch, px, py)
        ax.add_patch(plt.Polygon(poly, closed=True, fc=ACCENT, ec=INK, lw=0.5, alpha=0.85))
        ax.plot([0, px], [0, py], color=MUTED, lw=0.5)
        ax.plot([px], [py], "o", ms=2.0, color=INK)

    ex, ey = e * 1000.0 * math.cos(math.radians(phi)), e * 1000.0 * math.sin(math.radians(phi))
    ax.plot([ex], [ey], "o", ms=3.4, color=COOL)
    ax.annotate(f"offset pivot\n{e * 1000:.2f} mm", (ex, ey), (-58, -22),
                textcoords="offset points", fontsize=6.2, color=COOL,
                arrowprops=dict(arrowstyle="-", color=COOL, lw=0.5))
    ax.plot([0], [0], "+", ms=7, color=INK, mew=0.9)

    ax.add_patch(Rectangle((-24, -W / 2 - motor + 4), 48, motor - 6,
                           fc="#dcdcdc", ec=INK, lw=0.6))
    ax.text(0, -W / 2 - motor / 2 + 2, "motor", ha="center", va="center", fontsize=6.2)

    for sx in (-1, 1):
        ax.plot([sx * W / 2], [-W / 2 - motor], "s", ms=3, color=COOL)
    dim_line(ax, -W / 2, W / 2 + 16, W / 2, W / 2 + 16, f"{W:.1f} mm")
    dim_line(ax, W / 2 + 20, -W / 2 - motor, W / 2 + 20, W / 2, f"{H:.1f} mm")
    ax.text(0, (r_out + r_in) / 2, f"swept {2 * r_out:.1f} mm dia", ha="center",
            va="center", fontsize=6.2, color=MUTED)
    ax.set_title("rotor plane", fontsize=8)
    ax.set_xlim(-W / 2 - 34, W / 2 + 44)
    ax.set_ylim(-W / 2 - motor - 20, W / 2 + 30)

    # ---- along the rotor plane, showing the axial stack
    rotor_axes(bx)
    sp, bb = linkage.SIDE_PLATE_MM, linkage.BEARING_BLOCK_MM
    carrier, pulley = linkage.PHASING_CARRIER_MM, linkage.PULLEY_AND_BELT_MM
    x0 = -L / 2
    bx.add_patch(Rectangle((x0, -W / 2 - motor), L, H, fc="none", ec=INK, lw=0.8,
                           ls=(0, (5, 3))))
    blade_x0 = x0 + pulley + sp + bb
    # Blades project onto this view at R*sin(psi), so three of them land on two heights and
    # drawing all three would read as a mistake rather than as a projection. The swept band
    # is what the reader needs here, with one blade in it to give the band a cause.
    for y0 in (r_in, -r_out):
        bx.add_patch(Rectangle((blade_x0, y0), span, r_out - r_in, fc=FILL, ec=MUTED,
                               lw=0.4, alpha=0.8))
    for yy in (R_mm, -R_mm):
        bx.plot([blade_x0, blade_x0 + span], [yy, yy], color=MUTED, lw=0.5,
                ls=(0, (2, 2)))
    bx.add_patch(Rectangle((blade_x0, R_mm - chord / 8), span, chord / 4,
                           fc=ACCENT, ec=INK, lw=0.5))
    bx.text(blade_x0 + span / 2, R_mm + chord / 4 + 4,
            f"blade at ψ 90°, {blades} off", ha="center", fontsize=6.0,
            color=ACCENT)
    bx.add_patch(Rectangle((x0, -8), L, 16, fc="#dcdcdc", ec=INK, lw=0.5))
    bx.text(0, 0, "rotor shaft", ha="center", va="center", fontsize=6.2)
    for xx, w, lab in ((x0, pulley, "belt"), (x0 + pulley, sp + bb, "bearing block"),
                       (x0 + L - carrier - sp - bb, sp + bb, "bearing block"),
                       (x0 + L - carrier, carrier, "carrier")):
        bx.add_patch(Rectangle((xx, -r_out * 0.72), w, r_out * 1.44, fc="#f0ede8",
                               ec=COOL, lw=0.5))
        bx.text(xx + w / 2, -r_in * 0.52, lab, ha="center", va="center", fontsize=5.6,
                color=COOL, rotation=90)
    bx.add_patch(Rectangle((x0 + L / 2 - 46, -W / 2 - motor + 4), 92, motor - 6,
                           fc="#dcdcdc", ec=INK, lw=0.6))
    bx.text(x0 + L / 2, -W / 2 - motor / 2 + 2, "motor and mount plate",
            ha="center", va="center", fontsize=6.0)
    for i in range(mounts):
        bx.plot([x0 + 30 + i * (L - 60) / (mounts - 1)], [-W / 2 - motor], "s",
                ms=3, color=COOL)
    bx.text(0, -W / 2 - motor - 12, f"{mounts} airframe mount points", ha="center",
            fontsize=6.2, color=COOL)
    dim_line(bx, blade_x0, r_out + 16, blade_x0 + span, r_out + 16, f"span {span:.1f} mm")
    dim_line(bx, x0, r_out + 34, x0 + L, r_out + 34, f"{L:.1f} mm")
    bx.set_title("along the rotor plane", fontsize=8)
    bx.set_xlim(x0 - 16, x0 + L + 16)
    bx.set_ylim(-W / 2 - motor - 24, W / 2 + 36)

    values = {"geometry.radius_m": R, "geometry.chord_m": chord / 1000.0,
              "geometry.span_m": span / 1000.0, "geometry.blades": blades,
              "packaging.envelope_length_mm": L, "packaging.envelope_width_mm": W,
              "packaging.envelope_height_mm": H, "packaging.mount_points": mounts,
              "packaging.swept_diameter_mm": 2 * r_out,
              "pitch.swept_outer_radius_mm": r_out, "pitch.swept_inner_radius_mm": r_in,
              "pitch.offset_m": e}
    cap = (f"Module general arrangement. Rotor radius {R_mm:.0f} mm, {blades} blades of "
           f"{chord:.1f} mm chord and {span:.1f} mm span, swept diameter "
           f"{2 * r_out:.1f} mm, packaged envelope {L:.1f} by {W:.1f} by {H:.1f} mm on "
           f"{mounts} mount points.")
    return fig, values, cap


def fig_linkage():
    d, R, e, a, l, phi, branch, a0 = four_bar()
    R_mm, e_mm, a_mm, l_mm = R * 1000, e * 1000, a * 1000, l * 1000
    worst = dotted(d, "pitch.transmission_angle_worst_folded_deg")
    tmin = dotted(d, "pitch.transmission_angle_min_deg")
    tmax = dotted(d, "pitch.transmission_angle_max_deg")
    keep = dotted(d, "pitch.axis_keepout_mm")
    amp = dotted(d, "geometry.pitch_amplitude_deg")

    fig, ax = plt.subplots(figsize=(4.6, 4.4))
    rotor_axes(ax)
    ex, ey = e_mm * math.cos(math.radians(phi)), e_mm * math.sin(math.radians(phi))

    ax.add_patch(Circle((0, 0), R_mm, fc="none", ec=MUTED, lw=0.5, ls=(0, (2, 2))))
    fine = [i * 2.0 for i in range(180)]
    hx = [R_mm * math.cos(math.radians(p)) + a_mm * math.cos(
        linkage.horn_angle(math.radians(p), e, math.radians(phi), a, l, R, branch))
        for p in fine]
    hy = [R_mm * math.sin(math.radians(p)) + a_mm * math.sin(
        linkage.horn_angle(math.radians(p), e, math.radians(phi), a, l, R, branch))
        for p in fine]
    ax.plot(hx + [hx[0]], hy + [hy[0]], color=MUTED, lw=0.5, ls=(0, (1, 2)))

    for psi_deg, shade in ((0.0, 1.0), (90.0, 0.72), (180.0, 0.52), (270.0, 0.34)):
        psi = math.radians(psi_deg)
        px, py = R_mm * math.cos(psi), R_mm * math.sin(psi)
        alpha = linkage.horn_angle(psi, e, math.radians(phi), a, l, R, branch)
        tx, ty = px + a_mm * math.cos(alpha), py + a_mm * math.sin(alpha)
        pitch = linkage.wrap180(math.degrees(alpha - psi) - a0)
        ax.plot([0, px], [0, py], color=INK, lw=1.0, alpha=shade)
        ax.plot([px, tx], [py, ty], color=ACCENT, lw=1.6, alpha=shade,
                solid_capstyle="round")
        ax.plot([tx, ex], [ty, ey], color=COOL, lw=1.0, alpha=shade)
        ax.plot([px], [py], "o", ms=3.2, color=INK, alpha=shade)
        poly = blade_outline(dotted(d, "geometry.chord_m") * 1000.0,
                             psi_deg + 90.0 + pitch, px, py)
        ax.add_patch(plt.Polygon(poly, closed=True, fc=ACCENT, ec=INK, lw=0.4,
                                 alpha=0.22 * shade + 0.12))
        # Station labels go radially outward so they never land on the mechanism, whatever
        # the azimuth. Placing them at a fixed pixel offset put two of them on the links.
        lx, ly = R_mm * 1.30 * math.cos(psi), R_mm * 1.30 * math.sin(psi)
        ax.text(lx, ly, f"ψ {psi_deg:.0f}°\nθ {pitch:+.1f}°", ha="center", va="center",
                fontsize=6.2, alpha=max(shade, 0.6))
        if psi_deg == 0.0:
            horn_label = ((px + tx) / 2, (py + ty) / 2)
            link_label = ((tx + ex) / 2, (ty + ey) / 2)

    ax.plot([0, ex], [0, ey], color=COOL, lw=2.0)
    ax.plot([ex], [ey], "o", ms=4.4, color=COOL)
    ax.plot([0], [0], "+", ms=8, color=INK, mew=1.0)
    ax.annotate(f"L2 offset {e_mm:.2f} mm", (ex / 2, ey / 2), (-104, 30),
                textcoords="offset points", fontsize=6.4, color=COOL,
                arrowprops=dict(arrowstyle="-", color=COOL, lw=0.5))
    ax.text(R_mm * 0.10, -R_mm * 0.30, f"L1 rotor arm {R_mm:.1f} mm", fontsize=6.4,
            color=INK)
    ax.annotate(f"L3 pitch link {l_mm:.1f} mm", link_label, (-40, -34),
                textcoords="offset points", fontsize=6.4, color=COOL, ha="center",
                arrowprops=dict(arrowstyle="-", color=COOL, lw=0.5))
    ax.annotate(f"L4 horn {a_mm:.1f} mm", horn_label, (24, -30),
                textcoords="offset points", fontsize=6.4, color=ACCENT, ha="center",
                arrowprops=dict(arrowstyle="-", color=ACCENT, lw=0.5))
    ax.set_title(f"passive four-bar, one per blade, ±{amp:.0f}° pitch",
                 fontsize=8)
    ax.text(0, -R_mm * 1.68,
            f"transmission angle {tmin:.2f}° to {tmax:.2f}°, worst "
            f"{worst:.2f}° read folded\naxis keep-out {keep:.3f} mm",
            ha="center", fontsize=6.4, color=MUTED)
    lim = R_mm * 1.52
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim * 1.22, lim)

    values = {"geometry.radius_m": R, "pitch.offset_m": e, "pitch.horn_m": a,
              "pitch.pitch_link_m": l, "geometry.pitch_amplitude_deg": amp,
              "pitch.transmission_angle_min_deg": tmin,
              "pitch.transmission_angle_max_deg": tmax,
              "pitch.transmission_angle_worst_folded_deg": worst,
              "pitch.axis_keepout_mm": keep}
    cap = (f"Four-bar pitch kinematics at four azimuths. L1 {R_mm:.1f} mm rotor arm, L2 "
           f"{e_mm:.2f} mm offset, L3 {l_mm:.1f} mm pitch link, L4 {a_mm:.1f} mm horn. "
           f"The dotted path is the horn tip locus. Transmission angle runs {tmin:.2f} to "
           f"{tmax:.2f} degrees, worst {worst:.2f} degrees read folded.")
    return fig, values, cap


def fig_pitch_schedule():
    d = json.loads(NUMBERS.read_text(encoding="utf-8"))
    rows = d["pitch_schedule"]
    amp = dotted(d, "geometry.pitch_amplitude_deg")
    delay = dotted(d, "pitch.phase_delay_deg")
    rms = dotted(d, "pitch.schedule_rms_residual_deg")
    az = [r["azimuth_deg"] for r in rows]
    th = [r["pitch_deg"] for r in rows]
    model = [amp * math.cos(math.radians(x - 90.0 - delay)) for x in az]

    fig, (ax, rx) = plt.subplots(2, 1, figsize=(6.4, 3.6), sharex=True,
                                 gridspec_kw={"height_ratios": [3, 1]})
    ax.axhline(0, color=MUTED, lw=0.5)
    ax.plot(az, model, color=COOL, lw=1.0, ls=(0, (4, 2)),
            label=f"sinusoid, {amp:.0f}° at {delay:.2f}° delay")
    ax.plot(az, th, color=ACCENT, lw=1.4, label="four-bar loop closure")
    ax.set_ylabel("blade pitch, degrees")
    ax.legend(fontsize=6.6, loc="upper right")
    ax.grid(True, alpha=0.5)
    for y, lab in ((amp, "+"), (-amp, "-")):
        ax.axhline(y, color=MUTED, lw=0.4, ls=(0, (1, 3)))
    ax.set_title("blade pitch against azimuth", fontsize=8)

    rx.axhline(0, color=MUTED, lw=0.5)
    rx.plot(az, [t - m for t, m in zip(th, model)], color=INK, lw=1.0)
    rx.set_ylabel("residual, deg", fontsize=7)
    rx.set_xlabel("azimuth ψ, degrees")
    rx.set_xlim(0, 360)
    rx.set_xticks(range(0, 361, 45))
    rx.grid(True, alpha=0.5)
    rx.text(0.99, 0.06, f"rms {rms:.4f}°", transform=rx.transAxes,
            ha="right", fontsize=6.4, color=MUTED)

    values = {"geometry.pitch_amplitude_deg": amp, "pitch.phase_delay_deg": delay,
              "pitch.schedule_rms_residual_deg": rms,
              "pitch_schedule.0.pitch_deg": rows[0]["pitch_deg"],
              "pitch_schedule.9.pitch_deg": rows[9]["pitch_deg"],
              "pitch_schedule.18.pitch_deg": rows[18]["pitch_deg"]}
    cap = (f"Blade pitch schedule from the solved four-bar, against the {amp:.0f} degree "
           f"sinusoid it is usually assumed to be. The mechanism is not sinusoidal and the "
           f"residual is what the load model runs on, rms {rms:.4f} degrees, peak pitch "
           f"delayed {delay:.2f} degrees past the offset direction.")
    return fig, values, cap


def fig_blade_load():
    d = json.loads(NUMBERS.read_text(encoding="utf-8"))
    rows = d["aero_azimuthal_loads"]
    az = [r["azimuth_deg"] for r in rows]
    n = [r["normal_force_N"] for r in rows]
    lat = [r["lateral_force_N"] for r in rows]
    # Neither the peak nor the mean is stored on its own. The ratio between them is, and
    # the mean is thrust over blades by definition, so both come back out of the row set
    # the ratio was computed from rather than out of a second copy of the number.
    peak = max(n for n in [r["normal_force_N"] for r in rows])
    mean = dotted(d, "performance.thrust_N") / dotted(d, "geometry.blades")
    ratio = dotted(d, "performance.blade_load_peak_to_mean")

    fig, ax = plt.subplots(figsize=(6.4, 3.2))
    ax.axhline(0, color=MUTED, lw=0.5)
    ax.plot(az + [360], n + [n[0]], color=ACCENT, lw=1.4, label="vertical, per blade")
    ax.plot(az + [360], lat + [lat[0]], color=COOL, lw=1.1, label="lateral, per blade")
    ax.axhline(mean, color=INK, lw=0.7, ls=(0, (4, 2)),
               label=f"cycle mean {mean:.4f} N")
    ax.annotate(f"peak {peak:.4f} N", (az[n.index(max(n))], max(n)), (10, -12),
                textcoords="offset points", fontsize=6.6, color=ACCENT)
    ax.set_xlabel("azimuth ψ, degrees")
    ax.set_ylabel("force, N")
    ax.set_xlim(0, 360)
    ax.set_xticks(range(0, 361, 45))
    ax.grid(True, alpha=0.5)
    ax.legend(fontsize=6.6, loc="lower right", ncols=2)
    ax.set_title(f"blade force through one revolution, peak to mean {ratio:.4f}",
                 fontsize=8)

    values = {"performance.thrust_N": dotted(d, "performance.thrust_N"),
              "geometry.blades": int(dotted(d, "geometry.blades")),
              "performance.blade_load_peak_to_mean": ratio,
              "aero_azimuthal_loads.0.normal_force_N": n[0],
              "aero_azimuthal_loads.9.normal_force_N": n[9],
              "aero_azimuthal_loads.18.normal_force_N": n[18]}
    cap = (f"Blade force against azimuth on the solved pitch schedule. Peak vertical "
           f"{peak:.4f} N against a cycle mean of {mean:.4f} N, a peak to mean of "
           f"{ratio:.4f}, which is what the structure is sized on rather than the mean.")
    return fig, values, cap


def fig_vector_map():
    d = json.loads(NUMBERS.read_text(encoding="utf-8"))
    rows = d["vector_map"]
    rng = dotted(d, "pitch.vector_range_deg")
    auth = dotted(d, "pitch.phase_authority_deg")
    tilt = dotted(d, "pitch.side_force_tilt_deg")
    thrust = dotted(d, "performance.thrust_N")

    fig, (ax, bx) = plt.subplots(1, 2, figsize=(7.2, 3.3), layout="constrained",
                                 gridspec_kw={"width_ratios": [1.0, 1.04]})
    ax.set_aspect("equal")
    top = max(r["resultant_N"] for r in rows)
    ax.add_patch(Wedge((0, 0), top, 90 - rng / 2, 90 + rng / 2, fc=FILL, ec=MUTED,
                       lw=0.4, alpha=0.7))
    for r in rows:
        ax.annotate("", xy=(r["lateral_force_N"], r["vertical_force_N"]), xytext=(0, 0),
                    arrowprops=dict(arrowstyle="-|>", color=ACCENT, lw=1.2,
                                    shrinkA=0, shrinkB=0))
        lab = 1.13
        ax.text(r["lateral_force_N"] * lab, r["vertical_force_N"] * lab,
                f"{r['phase_command_deg']:+.0f}°", fontsize=6.2, ha="center",
                va="center", color=INK)
    ax.axhline(0, color=MUTED, lw=0.5)
    ax.axvline(0, color=MUTED, lw=0.5)
    ax.set_xlabel("lateral force, N")
    ax.set_ylabel("vertical force, N")
    ax.set_title(f"{rng:.0f}° of thrust direction", fontsize=8)
    ax.grid(True, alpha=0.4)
    # annotate() does not extend the data limits, so the arrows have to be given room by
    # hand. Without this the axes sized themselves on the wedge and clipped every vector
    # but the upright one.
    ax.set_xlim(-top * 1.30, top * 1.30)
    ax.set_ylim(-top * 0.16, top * 1.30)

    cmd = [r["phase_command_deg"] for r in rows]
    res = [r["resultant_direction_deg"] for r in rows]
    mag = [r["resultant_N"] for r in rows]
    bx.plot(cmd, cmd, color=MUTED, lw=0.6, ls=(0, (3, 2)), label="one to one")
    bx.plot(cmd, res, "o-", color=COOL, ms=3.6, label="resultant direction")
    bx.set_xlabel("phase command, degrees")
    bx.set_ylabel("resultant direction, degrees", color=COOL)
    bx.grid(True, alpha=0.5)
    bx.legend(fontsize=6.4, loc="upper left")
    cx = bx.twinx()
    cx.plot(cmd, mag, "s--", color=ACCENT, ms=3.0, lw=0.9)
    cx.set_ylabel("resultant magnitude, N", color=ACCENT)
    cx.tick_params(colors=ACCENT)
    cx.set_ylim(thrust * 0.90, thrust * 1.10)
    cx.text(0.98, 0.08, f"magnitude flat at {mag[0]:.4f} N", transform=cx.transAxes,
            ha="right", fontsize=6.2, color=ACCENT)
    bx.set_title(f"direction against command, {auth:.0f}° of authority",
                 fontsize=8)

    values = {"pitch.vector_range_deg": rng, "pitch.phase_authority_deg": auth,
              "pitch.side_force_tilt_deg": tilt, "performance.thrust_N": thrust,
              "vector_map.0.resultant_N": rows[0]["resultant_N"],
              "vector_map.2.resultant_N": rows[2]["resultant_N"],
              "vector_map.4.resultant_N": rows[4]["resultant_N"],
              "vector_map.0.lateral_force_N": rows[0]["lateral_force_N"],
              "vector_map.0.resultant_direction_deg": rows[0]["resultant_direction_deg"],
              "vector_map.4.resultant_direction_deg": rows[4]["resultant_direction_deg"]}
    cap = (f"Thrust vector map. Left, the resultant at each phase command, spanning "
           f"{rng:.0f} degrees. Right, direction against command on a one to one line. "
           f"The magnitude is flat at {mag[0]:.4f} N across the sweep, and that is the "
           f"load model being rotationally equivariant rather than a measured result: "
           f"turning the schedule and the inflow together turns the whole solution and "
           f"preserves its size. At zero command the resultant already sits "
           f"{tilt:.3f} degrees off the offset direction, which is a lag in the "
           f"aerodynamics and not a commanded tilt.")
    return fig, values, cap


def fig_blade_section():
    d = json.loads(NUMBERS.read_text(encoding="utf-8"))
    chord = dotted(d, "geometry.chord_m")
    axis = dotted(d, "geometry.pitch_axis_pct_chord") / 100.0
    ei = dotted(d, "structure.blade_ei_Nm2")
    gj = dotted(d, "structure.blade_gj_Nm2")
    allow = dotted(d, "structure.blade_allowable_Nm")
    wrinkle = dotted(d, "structure.blade_wrinkle_stress_MPa")
    combined = dotted(d, "structure.blade_combined_Nm")
    chord_mm = chord * 1000.0
    spar_od = check.BLADE_SPAR_DIA_FRAC * chord_mm
    wall = check.BLADE_SPAR_WALL_M * 1000.0

    fig, ax = plt.subplots(figsize=(6.6, 2.3))
    ax.set_aspect("equal")
    xs = [i / 300 for i in range(301)]
    yt = [check.naca_half_thickness(x) * chord_mm for x in xs]
    xm = [(x - axis) * chord_mm for x in xs]
    ax.fill_between(xm, yt, [-y for y in yt], fc=FILL, ec="none")
    ax.plot(xm, yt, color=INK, lw=1.0)
    ax.plot(xm, [-y for y in yt], color=INK, lw=1.0)
    ax.plot([xm[0], xm[-1]], [0, 0], color=MUTED, lw=0.5, ls=(0, (4, 2)))

    ax.add_patch(Circle((0, 0), spar_od / 2, fc="white", ec=COOL, lw=1.2))
    ax.add_patch(Circle((0, 0), spar_od / 2 - wall, fc="white", ec=COOL, lw=0.8))
    ax.plot([0], [0], "+", ms=8, color=ACCENT, mew=1.1)
    ax.annotate(f"pitch axis at {axis * 100:.0f}% chord\nspar {spar_od:.3f} mm od, "
                f"{wall:.1f} mm wall", (0, 0), (-26, 34), textcoords="offset points",
                fontsize=6.4, color=COOL,
                arrowprops=dict(arrowstyle="-", color=COOL, lw=0.5))
    ax.annotate(f"two ply skin, {check.BLADE_SKIN_AREAL_KG_M2 * 1000:.0f} g/m² cured",
                (xm[190], yt[190]), (10, 22), textcoords="offset points", fontsize=6.4,
                arrowprops=dict(arrowstyle="-", color=INK, lw=0.5))
    ax.annotate(f"foam core, {check.BLADE_FOAM_RHO:.0f} kg/m³, "
                f"{check.BLADE_FOAM_FILL * 100:.0f}% fill",
                (xm[70], -yt[70]), (-40, -20), textcoords="offset points", fontsize=6.4,
                arrowprops=dict(arrowstyle="-", color=INK, lw=0.5))
    dim_line(ax, xm[0], -chord_mm * 0.235, xm[-1], -chord_mm * 0.235,
             f"chord {chord_mm:.1f} mm")
    ax.set_title(f"{dotted(d, 'geometry.airfoil')} blade section, EI {ei:.3f} Nm², "
                 f"GJ {gj:.4f} Nm²", fontsize=8)
    ax.axis("off")
    ax.set_xlim(xm[0] - 6, xm[-1] + 6)
    ax.set_ylim(-chord_mm * 0.30, chord_mm * 0.24)

    values = {"geometry.chord_m": chord, "geometry.pitch_axis_pct_chord": axis * 100,
              "structure.blade_ei_Nm2": ei, "structure.blade_gj_Nm2": gj,
              "structure.blade_allowable_Nm": allow,
              "structure.blade_wrinkle_stress_MPa": wrinkle,
              "structure.blade_combined_Nm": combined}
    cap = (f"Blade section. {dotted(d, 'geometry.airfoil')} at {chord_mm:.1f} mm chord on "
           f"a {spar_od:.3f} mm spar tube at {axis * 100:.0f} percent chord, which is also "
           f"the pitch axis. EI {ei:.3f} Nm2 and GJ {gj:.4f} Nm2 come from this section, "
           f"and so does the {allow:.4f} Nm allowable that the {combined:.4f} Nm combined "
           f"root moment is held against. Skin wrinkling governs at "
           f"{wrinkle:.4f} MPa.")
    return fig, values, cap


def fig_mass():
    d = json.loads(NUMBERS.read_text(encoding="utf-8"))
    rows = d["mass_budget_g"]
    groups = {}
    for r in rows:
        g = groups.setdefault(r["refines"], [0.0, 0.0, 0])
        g[0] += r["mass_g"]
        g[1] += r["conservative_g"]
        g[2] += 1
    order = sorted(groups.items(), key=lambda kv: kv[1][0])
    nom_total = sum(r["mass_g"] for r in rows)
    con_total = sum(r["conservative_g"] for r in rows)
    tw = dotted(d, "results.thrust_to_weight")
    tw_stacked = dotted(d, "results.thrust_to_weight_conservative")

    fig, ax = plt.subplots(figsize=(6.6, 4.0))
    ys = range(len(order))
    ax.barh([y + 0.19 for y in ys], [v[0] for _, v in order], height=0.36,
            color=ACCENT, label=f"nominal, {nom_total:.2f} g")
    ax.barh([y - 0.19 for y in ys], [v[1] for _, v in order], height=0.36,
            color=COOL, alpha=0.75, label=f"conservative, {con_total:.2f} g")
    for i, (name, v) in enumerate(order):
        ax.text(v[1] + 1.4, i, f"{v[0]:.2f} / {v[1]:.2f}", va="center", fontsize=6.0,
                color=MUTED)
    ax.set_yticks(list(ys))
    ax.set_yticklabels([f"{k}  ({v[2]})" for k, v in order], fontsize=6.8)
    ax.set_xlabel("mass, g")
    ax.set_xlim(0, max(v[1] for _, v in order) * 1.28)
    ax.grid(True, axis="x", alpha=0.5)
    ax.legend(fontsize=6.8, loc="lower right")
    ax.set_title(f"module mass by group, {len(rows)} drawn lines\n"
                 f"thrust to weight {tw:.4f} design, {tw_stacked:.4f} stacked",
                 fontsize=8)

    values = {"results.thrust_to_weight": tw,
              "results.thrust_to_weight_conservative": tw_stacked,
              "results.total_mass_g": nom_total,
              "results.mass_g_conservative": con_total}
    cap = (f"Module mass by group. {len(rows)} drawn lines totalling {nom_total:.2f} g "
           f"nominal and {con_total:.2f} g conservative, with the line count per group in "
           f"brackets. Thrust to weight is {tw:.4f} at the design point and "
           f"{tw_stacked:.4f} with the coefficient and mass downsides stacked.")
    return fig, values, cap


FIGURES = [
    ("fig-arrangement", "Module general arrangement", fig_arrangement),
    ("fig-linkage", "Four-bar pitch kinematics", fig_linkage),
    ("fig-pitch-schedule", "Blade pitch schedule", fig_pitch_schedule),
    ("fig-blade-load", "Azimuthal blade load", fig_blade_load),
    ("fig-vector-map", "Thrust vector map", fig_vector_map),
    ("fig-blade-section", "Blade section", fig_blade_section),
    ("fig-mass", "Module mass breakdown", fig_mass),
]


def render(list_only=False):
    FIGDIR.mkdir(parents=True, exist_ok=True)
    manifest = []
    for fid, title, fn in FIGURES:
        fig, values, cap = fn()
        rel = f"figures/{fid}.pdf"
        if not list_only:
            fig.savefig(FIGDIR / f"{fid}.pdf", **SAVE)
        plt.close(fig)
        manifest.append({"id": fid, "title": title, "file": rel, "caption": cap,
                         "values": {k: round(v, 6) if isinstance(v, float) else v
                                    for k, v in values.items()}})
        print(f"{fid:20s} {len(values):2d} values  {title}")
    if not list_only:
        MANIFEST.write_text(json.dumps(
            {"_note": "Written by tools/figures.py. Every value is a dotted path into "
                      "numbers.json as it stood when the figure was drawn, and check.py "
                      "reads them back, so a stale figure fails a gate.",
             "figures": manifest}, indent=1) + "\n", encoding="utf-8", newline="\n")
        print(f"\n{len(manifest)} figures and a manifest in {FIGDIR}")
    return manifest


def main():
    ap = argparse.ArgumentParser(description="render the Stage 1 figures")
    ap.add_argument("--list", action="store_true", help="name them without rendering")
    args = ap.parse_args()
    render(list_only=args.list)
    return 0


if __name__ == "__main__":
    sys.exit(main())
