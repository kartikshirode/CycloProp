# CycloProp, team Kalash

Our entry for the CycloProp challenge in the PUSHPAK Grand Challenge 2026: a single cyclorotor module called Kalash CR-1. Stage 1 went in on 27 September 2026 as Team ID TM-5A7C41AF909. Stage 1 results come out on 2 October, and if we qualify, the Stage 2 work runs from 3 October to 2 December.

## What's here

| Path | What it is |
| --- | --- |
| `context.md` | Everything the challenge asks for, read from the official problem statement. It has a section on what Stage 2 will demand |
| `stage-1/design/` | The design, one file per item, plus the evidence ledger and `numbers.json`, the one data file every number comes from |
| `stage-1/decisions.md` | The decision log. The design files cite it as D1 to D73 |
| `stage-1/literature.md` | Sources we read and what we took from each |
| `stage-1/submission/` | The zip exactly as submitted, the design note source and the figures |
| `tools/` | The solvers (`linkage.py`, `structure.py`), the figure script and `check.py` |
| `tools/hpc/` | Slurm jobs that install and run OpenFOAM on the Baramati cluster |
| `compute.md` | Cluster access and what was measured on it |
| `reference/` | Problem statement, the organisers' terms, thesis text extracts |

## Rerunning the numbers

You need Python 3 (tested on 3.12). The solvers use nothing outside the standard library.

```
python tools/linkage.py --write
python tools/structure.py --write
python tools/check.py --global
```

The first two rewrite `stage-1/design/numbers.json`. If nothing in the design changed, git shows no diff. `check.py --global` checks that the design files, the design note and the data file still agree. Its `--week` gates belonged to the Stage 1 schedule and won't pass any more, since those progress files are gone. `tools/figures.py` redraws the figures and also needs matplotlib.

## Older material

The Stage 1 audit rounds, weekly progress notes, journal, plan, handoff and report builders were removed after submission. They're still in git history; the last commit that has all of them is `bd20373`.
