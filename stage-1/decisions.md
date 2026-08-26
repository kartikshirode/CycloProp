# Decisions

Numbered, append only. Reopening an earlier decision means a new entry that says which one it supersedes and why, never an edit in place.

## D1: context.md outranks the earlier documents

26 August 2026, week 1.

`brief.md`, `handoff.md` and `_shared-timeline.md` were written from summaries of a page that serves no content to a fetcher. The problem statement PDF contradicts them in several places. Rather than edit every file and risk leaving one stale, `context.md` is the single authority on requirements and the others are left as history.

## D2: the module is one larger rotor, not a cluster of small ones

26 August 2026, week 1. Provisional, confirmed in week 2.

Benedict's flight-weight 6 inch rotor masses 96 g and carries 1.98 N. Reaching 10 N by repeating it takes 5.04 rotors, which is 485 g of rotor alone against a 408 g budget for the entire module. A cluster cannot close. The aerodynamic side supports the same answer, since non-dimensional thrust holds while torque and power fall as Reynolds number rises.

## D3: numbers live in one file

26 August 2026, week 1.

Every quantity the submission states is defined in `stage-1/design/numbers.json` and cited from prose through a `## Numbers used` block. The gate recomputes the arithmetic and fails on disagreement. Chosen because the failure mode on a design document written across five weeks is a number that drifts between sections, and that is exactly what a viva finds.

## D4: no CAD at Stage 1

26 August 2026, week 1.

The problem statement does not ask for it and CAD quality carries 5 percent, scored on the Stage 2 and 3 package. Five criteria at 15 percent each are analysis. Modelling time now is taken from those.

## D5: the submission email is never sent by an agent

26 August 2026, week 1.

Outward facing, irreversible, and it represents a team to a national programme. The loop drafts and stages it. A human sends it. Recorded as a blocked trigger in the loop config.
