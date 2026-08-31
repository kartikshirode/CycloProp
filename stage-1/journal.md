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

Spent a while checking whether the model was just pessimistic before calling it. Nominal
thrust to weight lands well above the best published module on the same boundary, so the model
is not being harsh. The conservative case is simply stacking a 15 percent thrust haircut on an 18
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

## 2 September 2026, week 2, after the audit

The audit came back with 18 findings and about half of them were real problems rather than
tidying. Three worth writing down, because each one changed a number.

**I had the Reynolds argument backwards and used it to win a comparison.** The design sat at Re
134,000 and I wrote in three places that this was inside the band the coefficient transfer is
supported over. It is not. The support is Shrestha's 10,000 to 100,000. I had swapped in
Kellen's study band of 100,000 to 300,000, which is where the figure of merit and the solidity
optimum live, not the coefficient. Worse, I used the same wrong claim to say the cluster rows
were flattered, when in fact the clusters sit closer to the supported band than the single rotor
does. The single rotor still wins by 36 percent, so the conclusion held, but the argument for it
was wrong at exactly the point it was doing work.

The interesting part is that it cannot be fixed by choosing a different radius. Conservative
thrust has to clear 10 N and the haircut is 15 percent, so design thrust cannot go below 11.76
N, and Re goes with the square root of thrust. Every compliant point in this family is outside
the band. That is D25 and it is now one of the reasons the week does not freeze.

**The conservative mass column was not following its own stated rule.** I had written that
catalogue parts take 15 percent and computed sections take 20 to 25, then given the blades and
the shaft the catalogue rate. Both are built entirely from assumed geometry. Fixing that cost
0.025 of conservative thrust to weight in a week whose whole finding was a small miss.

**The drive shortlist was wrong in two directions at once and this turned into the week's most
useful result.** I had missed two lighter and stronger real motors, and I had read "Max. Power
(180s)" as a continuous rating when it is a three minute maximum. Fixing the second cost more
than the first gained. But checking power, torque and attainable speed together instead of power
alone showed something nobody had noticed: conservative thrust to weight keeps improving as the
rotor shrinks, and it is the motor that stops it. The 100 mm row would give 2.376. No shortlist
motor can hold it, because the torque wants a belt ratio the KV450 cannot spin to on 6S. So the
radius is 110 mm because that is the smallest a named drive can turn, not because the physics
wants it there.

That reframes the whole block. The design is drive limited, not aerodynamics limited and not
structure limited, and the cheapest unblock is a catalogue search plus one paper rather than a
redesign.

Also fixed: E7 was labelled measured in a ledger whose own headline says nothing is, the low
coefficient's 5 percent was described as derived from the blade section when the section
actually says it should be under 1 percent, three mass lines were called fixed when their own
basis says they scale, and the journal entry above claimed our rotor group was 24 percent
heavier than Runco scaled geometrically. That last one I cannot reproduce and have removed. The
comparison that does hold is the module thrust to weight, 3.163 nominal against Runco's 2.13.

Added four gates to `check.py` because the audit was right that three of the lists week 2 fills
had numbers nothing read. A 36 row table of arbitrary positive values passed the azimuthal check
identically to a calibrated one. Twelve self-tests went in with them and the suite is 89 now.

Final answer 2.252 against a hard limit of 2.5. Every audit fix moved it down except the motor
work, which is the right direction for a week that started by finding the number it wanted.

## 31 August 2026, week 2, second run and the freeze

Came back to a week that had already done its work and stopped one number short. The call it
stopped for arrived as D30, so this run was small: compute the mass target, freeze the geometry
in the documents, close the week.

The target itself is one line of arithmetic. Conservative thrust over 2.5 times gravity, 623.88
g, and the gate recomputes it and rejects anything that misses by half a percent. What took the
time was working out what to say about it. A target that says "week 4 finds 68.5 g" is a
paragraph pretending to be a plan, so I went through the envelope line by line to see where the
grams could plausibly come from. Eight lines carry a 20 or 25 percent growth rate on an assumed
basis and hold 86.4 g between them. Retire those to a uniform 10 percent and you get 45.7 g
back, which is two thirds of the gap and not the whole thing. Worth writing down, because the
first honest answer is that the mass route alone probably does not close it.

Then I noticed the other direction and it changed the entry. If Kellen's coefficient comes in
at or above 0.6055, the transfer allowance retires, conservative thrust goes to 17.1 N, and the
mass that clears 2.5 becomes 697.2 g. The module already weighs 692.4 g in the conservative
column. So the whole target disappears rather than shrinks, and week 4 might be solving a
problem that a browser session deletes. That is now the first line of D31 and the second item
on the human list.

The documents needed more editing than the numbers did. Four files described the freeze as
pending and one of them, the evidence ledger, published the freeze rule that D30 then changed.
I left the original rule visible and wrote the change underneath it rather than editing the
rule in place, because a ledger that quietly shows the new rule is worse than no ledger. Same
reasoning behind D32: every document that quotes 3.163 also carries 2.252 from here on. Five
documents will repeat themselves a bit. Better than a Stage 2 team building to the headline and
finding out from a scale.

One thing I did not do: reopen anything. The coefficient, the derate, the speed rule, the
growth rates, the drive and the two frozen tables are all exactly where the first run left
them. D30 says so explicitly and it is the part of the entry worth taking seriously, because
the easy version of this week was to shave two percent off a growth rate and call it a design.

Late addition, same day. A gate landed while this was running: a coefficient scenario classed
measured, taken on this design's own solidity and chord to radius and not undercutting the
nominal, now drops the transfer haircut floor from 10 percent to 5. Nothing in `numbers.json` is
classed measured, so the floor in force is still 10 and not one number here moved. It is the
mechanism D23 described, sitting ready. Whoever gets Kellen open pays for the reading and gets
the retirement, and the gate will not accept a measurement on somebody else's shape family in
its place.


## 31 August 2026, the evidence pass

Both theses came out of the Wayback Machine in about a minute each, after two weeks of the live
routes refusing. OAKTrust is still behind its Cloudflare challenge and DRUM was serving a
maintenance page, but `web.archive.org` had captures of both bitstreams and the `id_` flag hands
back the original bytes instead of a rewritten wrapper. That was the whole trick. Two weeks of
"needs a person with a browser" for a URL prefix.

Kellen tabulates no coefficients, which I had half expected. CT/sigma only exists inside his
figures. Rather than squint at a plot I pulled the vector paths out of the PDF, so the axis
calibration is the tick geometry and the data points are the polyline vertices matplotlib wrote.
Fig 3.25 and Fig 3.28 are two separately drawn figures of the same measurement and they came out
at 1.04424 and 1.04428.

What I liked about the day was the checking. Agreement between two figures only proves I can
read a plot twice. So I took CP/sigma off a third figure and closed the figure of merit:
CT^1.5/(sqrt(2) CP) gives 0.595 against the 0.6 Kellen states in his own section 3.3 for exactly
that rotor. Then power loading at the 60 N/m2 disk loading his text names for Fig 3.27 came out
at 0.1202 against the 0.1201 plotted. Neither closure depends on the span, so neither could be
rescued by guessing the rotor right. At that point I believed the number.

Benedict was the uncomfortable one. I went in to confirm the basis under 0.6055 and found the
basis was invented. 1.98 N at 2000 rpm is not in the dissertation anywhere: 1.98 N is the 809
gram vehicle weight over four, and 2000 rpm is the twin rotor. The quad's real point is 1.91 N at
1800 rpm, printed twice, which gives 0.7211. Two mistakes pulling opposite ways, netting 16
percent low. It reproduced perfectly every time anybody checked it, which is exactly why it
survived a pull and two audits. Checking that arithmetic reproduces is not the same as checking
that the inputs exist.

I did not raise the coefficient. Every measured value available sits above 0.6055 and raising it
would push thrust, rpm, torque, the drive and half the mass lines upward to buy margin nothing is
asking for. So it stays, and D36 says it stays on purpose now rather than by luck.

The other thing worth recording is that I stopped for twenty minutes in the middle. `git status`
came back dirty with nine files I had not touched, and a file went from clean to modified while I
was watching, so there were two of us writing the same repository. I backed my own numbers.json
edit out, checked key by key that I had not clobbered anything, moved my new files to the
scratchpad, and reported instead of finishing. It cost half an hour. Overwriting somebody's
uncommitted work would have cost more, and there is no way to get it back.
