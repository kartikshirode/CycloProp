"""Assemble the Google Form upload: one zip named Grand Challenge Title_Team ID.

    python stage-1/submission/form/make_zip.py
"""
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
NAME = "CycloProp Advanced UAV Propulsion Challenge_TM-5A7C41AF909.zip"
REPORT = "CycloProp_TM-5A7C41AF909_Stage1_Report"

S = ROOT / "stage-1"
B = HERE / "build"
FILES = {
    "00_Contents.pdf": B / "00_Contents.pdf",
    f"01_Report/{REPORT}.pdf": HERE / f"{REPORT}.pdf",
    f"01_Report/{REPORT}.docx": HERE / f"{REPORT}.docx",
    "02_Detailed_Design_Note/CycloProp_Stage1_Detailed_Design_Note.pdf":
        S / "submission" / "cycloprop-stage1.pdf",
    "03_Design_Record/CycloProp_Stage1_Design_Record.pdf": B / "CycloProp_Stage1_Design_Record.pdf",
    "04_Calculations/README.pdf": B / "README.pdf",
    "04_Calculations/tools/linkage.py": ROOT / "tools" / "linkage.py",
    "04_Calculations/tools/structure.py": ROOT / "tools" / "structure.py",
    "04_Calculations/stage-1/design/numbers.json": S / "design" / "numbers.json",
}
ORDER = ["fig-arrangement", "fig-concepts", "fig-blade-section", "fig-rpm", "fig-linkage",
         "fig-pitch-schedule", "fig-vector-map", "fig-powerflow", "fig-mass", "fig-blade-load"]
for i, stem in enumerate(ORDER, 1):
    FILES[f"05_Figures/Figure_{i:02d}_{stem[4:]}.png" if i < 10 else "05_Figures/Figure_A1_blade-load.png"] = B / f"{stem}.png"

out = HERE / NAME
missing = [str(v) for v in FILES.values() if not v.is_file()]
assert not missing, missing
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    for arc, src in sorted(FILES.items()):
        z.write(src, arc)
print(f"{out.name}: {len(FILES)} files, {out.stat().st_size / 1e6:.2f} MB")
for arc in sorted(FILES):
    print("  ", arc)
