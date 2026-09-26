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
FILES = {
    f"01_Report/{REPORT}.pdf": HERE / f"{REPORT}.pdf",
    f"01_Report/{REPORT}.docx": HERE / f"{REPORT}.docx",
    "02_Detailed_Design_Note/CycloProp_Stage1_Detailed_Design_Note.pdf":
        S / "submission" / "cycloprop-stage1.pdf",
    "03_Calculations/README.txt": HERE / "calculations-README.txt",
    "03_Calculations/tools/linkage.py": ROOT / "tools" / "linkage.py",
    "03_Calculations/tools/structure.py": ROOT / "tools" / "structure.py",
    "03_Calculations/stage-1/design/numbers.json": S / "design" / "numbers.json",
    "04_Design_Record/evidence-ledger.md": S / "design" / "evidence-ledger.md",
}
for p in sorted((S / "design").glob("0*.md")):
    FILES[f"04_Design_Record/{p.name}"] = p
for p in sorted((S / "submission" / "figures").glob("*.pdf")):
    FILES[f"05_Figures/{p.name}"] = p
for p in sorted((HERE / "build").glob("fig-*.png")):
    if p.stem in ("fig-concepts", "fig-rpm", "fig-powerflow"):
        FILES[f"05_Figures/{p.name}"] = p

out = HERE / NAME
missing = [str(v) for v in FILES.values() if not v.is_file()]
assert not missing, missing
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    for arc, src in sorted(FILES.items()):
        z.write(src, arc)
print(f"{out.name}: {len(FILES)} files, {out.stat().st_size / 1e6:.2f} MB")
for arc in sorted(FILES):
    print("  ", arc)
