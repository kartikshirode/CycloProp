# Audit: week 1

Week 1 ran on 26 August 2026, before the loop config existed, so this is a self-audit rather than the independent read a loop week gets. Recorded so the file exists and so week 2's agent knows the difference.

## Plan against delivered

The plan asked for a parameter table rebuilt from source PDFs. Delivered, in `stage-1/literature.md`, with four sources read in full and two marked as summary only.

Not planned but delivered: `context.md`, because the official problem statement was found and it contradicted the repo in ways that would have wasted weeks 2 to 5. Scope change is recorded as decision D1.

## Findings

**1. Two sources in the parameter table were never opened.** The Texas A&M UAV-scale thesis is the closest published work to our design point and the table row for it is built from a search summary. Its three shape numbers are internally consistent, which is evidence but not verification. Week 2's default shape family rests on it. Carried as a debt, flagged in the file and in the handoff.

**2. The blade-area coefficient of 0.607 is derived here, not published.** It comes from Benedict's quad rotor hover requirement divided by tip dynamic pressure and blade area. Week 2 sizes off it. The derivation is stated in `literature.md` so it can be checked or replaced, but it is a single-point anchor and the sizing should not pretend otherwise.

**3. Sirohi's stated power loading and Benedict's differ by roughly 4x.** Both are described as high-thrust asymptotes. They are measured over different thrust ranges, which explains it, and `literature.md` says so. The lower figure was used. Worth re-checking if week 2's power number looks wrong.

**4. Two documents now disagree with `context.md` and were deliberately left alone.** `brief.md` and `_shared-timeline.md` still say five Stage 1 items and describe a funding contradiction that does not exist. The authority order handles it, but a reader who opens the wrong file first is misled. Accepted rather than fixed, on the grounds that editing history files creates a worse problem than an authority note solves.

**5. The old parameter table is still recoverable from git history.** `plan.md` warns against reusing it. That is the only mitigation available short of rewriting history, which is banned.

Findings: 5

AUDIT-COMPLETE
