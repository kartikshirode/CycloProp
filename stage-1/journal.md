# Session journal

Newest last. One entry per working session.

## 26 August 2026, week 1

Started from the handoff, which said week 1 was literature and that the existing parameter table could not be trusted.

Pulled four papers as full text. The Sirohi and Xisto PDFs came straight down. Benedict's dissertation was too large for the fetcher and needed a direct download, then `pdftotext`. The Shrestha paper came from the publisher's own full-text page. Three more are still shut: the Texas A&M thesis repository refuses requests, and two journal papers are paywalled.

The old table turned out to be worse than the handoff guessed. Most rows were wrong, and one of them was a units slip that had turned a 1.3 inch chord into a 1.3 inch radius.

Then went looking for the competition page to check the deliverable list, and found that techfest.org is a React app that serves a fetcher nothing but a title. The content sits behind `https://techfest.org/api/compis/`, which took working through the JS bundle to find. That record has a `probStatement` field, and the PDF at the end of it is the document the whole repo had been assuming did not exist. It answered the blocking thrust-to-weight question in one sentence and added two Stage 1 deliverables nobody knew about.

Rewrote the plan around the seven real deliverables, built the loop config and the gate script, and tested the gates by feeding them fabricated numbers to confirm they reject them.

Ended the day with sizing unblocked and week 2 ready to run.

## 2 September 2026, week 2

Built the evidence ledger first, which turned out to matter more than expected. Recomputing
the 0.607 thrust coefficient from Benedict's quad rotor gave 0.6055, so the number the repo
has been carrying is right to a quarter of a percent. Running the same recompute on his twin
rotor, which has 3 blades like ours, gave 0.8114. Tempting, and not usable: the twin sits at a
solidity of 0.159, miles outside the band D12 gates on.

Then the sizing. Wrote a coupled model over radius and thrust, with a component mass build-up
rather than percentages, and swept it. The first version had a frame line of 270 g because I
had picked 50 by 3 mm solid CFRP rails without thinking about it. Fixed that to a tube and
bearing block frame and the line came down to 80 g, which is the only place in the week where
I changed a modelling choice after seeing what it did to the answer, and it was because the
first choice was wrong rather than because the second one was flattering.

The result did not close. Conservative thrust to weight peaks at 2.389 at 20 N and 115 mm,
against a hard limit of 2.5 and an internal target of 2.75. Worked the fallbacks in the plan's
order. Higher thrust rows peak at 20 N because the drive shortlist runs out at 555 W. The
radius sweep peaks at 115 mm. The cluster comparison went the other way entirely, with two
rotors at 1.795 and three at 1.434, so D2 is confirmed properly now instead of provisionally.
Revisiting the shape family gets to 2.481 at blade aspect ratio 6, which is outside the family
the coefficient came from, so it buys a number by making the transfer worse.

Spent a while checking whether the model was just pessimistic before calling it. Our rotor
group is 24 percent heavier than Runco's scaled geometrically, and our nominal thrust to
weight is 56 percent above the best published module on the same boundary. So the model is not
being harsh. The conservative case is simply stacking a 15 percent thrust haircut on an 18
percent mass growth, and 0.85 over 1.18 is 0.72, so nominal has to reach 3.8 for conservative
to reach 2.75. Nothing published supports 3.8.

The useful part of the answer is how close it is. 32 g of conservative mass separates 2.389
from the hard limit. That is inside the noise of a coarse envelope, which is exactly why it
goes to a person rather than getting rounded into compliance. And the single cheapest thing
that moves it is Kellen's measured coefficient, which is two minutes in a browser and would
put the conservative case near 2.68.

Ran the drive numbers properly too. The MN3510 KV700 sits at 92 percent of continuous power
and 87 percent of continuous torque at 6 to 1, which is a continuous operating point rather
than a peak one, and that was worth checking before naming it anywhere.

Gates end the week with exactly one failure, the T/W line. Everything else reproduces.
