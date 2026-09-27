"""Build the design record and the contents page as PDFs for the upload.

    python stage-1/submission/form/build_record_pdf.py
"""
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
BUILD = HERE / "build"
DESIGN = ROOT / "stage-1" / "design"

DOCS = [
    ("01-configuration.md", "Cyclorotor concept and configuration"),
    ("02-rotor-sizing.md", "Preliminary rotor sizing"),
    ("03-pitch-and-vectoring.md", "Blade arrangement, pitch control and thrust vectoring"),
    ("04-thrust-and-power.md", "Estimated thrust and power"),
    ("05-mass-and-tw.md", "Module mass and thrust to weight"),
    ("06-materials-and-manufacturing.md", "Materials and manufacturing"),
    ("07-team-and-execution.md", "Team capability and execution plan"),
    ("08-structure-and-loads.md", "Structure and loads"),
    ("09-packaging-and-integration.md", "Packaging and integration"),
    ("evidence-ledger.md", "Evidence ledger"),
]
LANDSCAPE = {"evidence-ledger.md"}

PANDOC = ["pandoc", "--from=markdown-yaml_metadata_block", "--pdf-engine=xelatex",
          "-V", "geometry:margin=20mm", "-V", "fontsize=10pt", "-V", "colorlinks=true",
          "-V", "mainfont=Calibri", "-V", "monofont=Consolas"]


def clean(text, title):
    # the machine readable declaration block closes every file; the report carries the values
    text = re.split(r"(?m)^## Numbers used\s*$", text)[0]
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    # links point at sibling markdown files that are now chapters of one PDF
    text = re.sub(r"\[([^\]]+)\]\((?!http)[^)]*\)", r"\1", text)
    lines = text.splitlines()
    if lines and lines[0].startswith("# "):
        lines[0] = f"# {title}"
    # every heading one level down would lose the chapter break, so keep the file's own levels
    return "\n".join(lines).rstrip() + "\n\n\\newpage\n\n"


def record():
    parts = ["---\ntitle: \"Kalash CR-1, Stage 1 design record\"\n"
             "subtitle: \"CycloProp: Advanced UAV Propulsion Challenge. Team Kalash, VPKBIET, "
             "TM-5A7C41AF909\"\n"
             "date: \"27 September 2026\"\n---\n\n"
             "The working documents behind the Stage 1 report, one chapter per design item, "
             "and the evidence ledger that grades every borrowed number. Numbers here are the "
             "same ones the report quotes; both are generated from one data file. References to "
             "numbered decisions (D1 to D73) point at the project decision log, available on "
             "request.\n\n\\newpage\n\n"]
    for name, title in DOCS:
        if name not in LANDSCAPE:
            parts.append(clean((DESIGN / name).read_text(encoding="utf-8"), title))
    src = BUILD / "design-record.md"
    src.write_text("".join(parts), encoding="utf-8")
    main = BUILD / "record-main.pdf"
    subprocess.run(PANDOC + ["--toc", "--toc-depth=1", "--from=markdown", str(src), "-o",
                             str(main)], check=True)
    wide = BUILD / "record-ledger.pdf"
    lsrc = BUILD / "ledger.md"
    lsrc.write_text(clean((DESIGN / "evidence-ledger.md").read_text(encoding="utf-8"),
                          "Evidence ledger"), encoding="utf-8")
    cmd = [c if c != "fontsize=10pt" else "fontsize=9pt" for c in PANDOC]
    cmd = [c if c != "geometry:margin=20mm" else "geometry:landscape,margin=12mm" for c in cmd]
    subprocess.run(cmd + ["--from=markdown", str(lsrc), "-o", str(wide)], check=True)
    from pypdf import PdfWriter
    out = BUILD / "CycloProp_Stage1_Design_Record.pdf"
    w = PdfWriter()
    for f in (main, wide):
        w.append(str(f))
    w.write(str(out))
    return out


def index():
    md = """---
title: "Kalash CR-1: Stage 1 submission contents"
subtitle: "CycloProp: Advanced UAV Propulsion Challenge. Team Kalash, VPKBIET"
---

| | |
| --- | --- |
| Team ID | TM-5A7C41AF909 |
| Team | Kalash: Kartik Shirode (team leader), Mandar Wagh, Aditya Shilalkar |
| Institution | VPKBIET, undergraduate |
| Contact | kartikshirode123@gmail.com, 9823376032 |

## What is in this zip

| Folder | File | What it is |
| ---------- | ------------------------------ | ------------------------------ |
| 01 Report | Stage1_Report.pdf | **The Stage 1 report, on the organisers' template. Start here** |
| 01 Report | Stage1_Report.docx | The same report as an editable Word file |
| 02 Design note | Detailed_Design_Note.pdf | 32 pages: every calculation behind the report, the claims and risk table, examiner questions |
| 03 Design record | Design_Record.pdf | The working design documents, one chapter per item, and the evidence ledger |
| 04 Calculations | README.pdf, tools, numbers.json | The two Python solvers and the data file they write. Running them reproduces every number |
| 05 Figures | fig-*.png | Every figure in the report at full resolution |

## Headline numbers

| | |
| --- | --- |
| Configuration | single cyclorotor, 3 blades, NACA 0020, 220 mm diameter, 290.4 mm span |
| Pitch and vectoring | passive four-bar per blade, +/-40 deg; 120 deg of vector authority from 2 servos |
| Design thrust | 17.0 N at 2337 rpm (16.15 N on the low coefficient) |
| Power | 518.0 W at the module |
| Module mass | 687.91 g nominal, 775.74 g conservative |
| Thrust to weight | 2.5191 design point; 2.1221 with both downsides stacked |
| Cost | 68,830 INR indicative |
"""
    src = BUILD / "index.md"
    src.write_text(md, encoding="utf-8")
    out = BUILD / "00_Contents.pdf"
    subprocess.run(PANDOC + ["--from=markdown", str(src), "-o", str(out)], check=True)
    return out


def readme_pdf():
    txt = (HERE / "calculations-README.txt").read_text(encoding="utf-8")
    src = BUILD / "readme.md"
    src.write_text("---\ntitle: \"Stage 1 calculations: how to run them\"\n---\n\n```\n"
                   + txt + "```\n", encoding="utf-8")
    out = BUILD / "README.pdf"
    subprocess.run(PANDOC + ["--from=markdown", str(src), "-o", str(out)], check=True)
    return out


def figures_png():
    figs = ROOT / "stage-1" / "submission" / "figures"
    for p in sorted(figs.glob("*.pdf")):
        subprocess.run(["pdftoppm", "-r", "250", "-png", "-singlefile", str(p),
                        str(BUILD / p.stem)], check=True)


if __name__ == "__main__":
    BUILD.mkdir(exist_ok=True)
    for f in (record(), index(), readme_pdf()):
        print("wrote", f)
    figures_png()
