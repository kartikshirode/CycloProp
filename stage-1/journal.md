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

## 31 August 2026, week 3, the linkage

The thing I was most worried about turned out to be the easy part, and something I had not
thought about at all ate most of the day.

Easy part first. Reconstructing week 2's azimuthal load model took twenty minutes, because
`04-thrust-and-power.md` had written down enough to rebuild it: 36 azimuths, a prescribed
sinusoid, uniform inflow from momentum theory, angle of attack as pitch less inflow angle capped
at 28 degrees, thin airfoil slope, scaled so the cycle mean matches thrust per blade. I wrote
four candidate readings of that description and scored each against the 36 stored numbers. One
of them reproduced the whole table to 5.2e-5 N. That is not a fit, it is an identification, and
it meant week 3 could rerun the model rather than replace it. Documents that say what they did
are worth the space they take.

Then the four-bar. Kellen names his four lengths on printed pages 55 and 56 and gives three of
them as numbers, so I scaled his ratios to a 110 mm radius, solved the offset by bisection on
peak to peak pitch travel, and got a working mechanism first try. Amplitude 40 degrees,
revolution closing on itself, Grashof double crank with the ground as the shortest link. I was
pleased with myself for about ten minutes.

Two things then went wrong at once. The pitch link passes 0.004 mm from the rotor axis, which is
not a clearance, it is a hole in the middle of the design. And the carrier torque came out at
0.3240 Nm, which two servos hold on exactly half their stall torque and not a newton metre more.

The first one I got wrong twice before getting it right. My first instinct was to shape the link
around the shaft, which is what Kellen did, and my second was to move the mechanism outboard,
which does not help because the carrier still needs the axis. What actually works is to admit
the pitch plane cannot have anything coaxial in it at all, put the belt on one end and the
phasing carrier on the other, and stop the shaft short. It is a cleaner machine than the one I
started drawing. It is also a constraint week 4 inherits whether it likes it or not.

The torque one I nearly solved the wrong way. My first move was a longer horn, on the reasoning
that a longer arm means less link force. It does, and the carrier torque goes up anyway, because
the offset grows with the horn and the torque scales on the offset. The sweep is in the script
now for exactly that reason: I would not have believed the answer without the table. What fixed
it was the pitch link, which I had assumed was fixed by Kellen's ratio and is not. 105 mm
instead of 111.6 mm takes the carrier torque from 0.3240 Nm to 0.1371 Nm, opens the transmission
angle by 18 degrees and halves the harmonic residual. Same horn, same radius, one link length.

The number I actually care about is the side force, and it is the one I am least happy with.
The model puts the resultant 11.98 degrees off the commanded direction, of which 11.00 comes
from the linkage and 0.98 from the aerodynamics. Sirohi, Adams and Benedict's twin put the whole
tilt between 10 and 35 degrees on rotors like this one, and Benedict's figure 2.33 says in words
that it rises with rpm and with blade count, so we sit high in that band. So
the aerodynamic half of my number is wrong by an order of magnitude and I know why: uniform
inflow, no wake return, no shed vorticity, no dynamic stall hysteresis. Every one of those feeds
the lateral component. I could have written 30 degrees into the design and called it a
correction. That would have looked better and meant less.

What I did instead is treat it as a bias with a band around it: index the carrier at assembly,
trim on the bench, and cost out the uncertainty. It costs 25 degrees of the 120, worst case,
which is the single biggest consumer of vectoring authority in the module and is now written
down as such.

Two smaller things. The vector map came out exactly one to one, magnitude flat at 18.000 N at
every command, and my first reaction was that I had made a mistake. I had not: an axisymmetric
rotor with a self-consistent inflow is rotationally equivariant, so the map has to be an exact
rotation. That makes it a weak piece of evidence dressed as a strong one, so I said so in the
document and then went and made the gate harder, because a table like that would have passed
the old check with the lateral column set to zero.

And the blade is not balanced. Centre of mass at 39.92 percent chord against a pitch axis at 30,
which on a cyclorotor puts a steady centrifugal moment on every blade and doubles the pitch link
load. I nearly added a nose weight to make my own numbers look better. It is week 4's trade, the
stored numbers are the unbalanced ones, and the script refuses to write the balanced case.

I did not stop at the end. A fresh-context read found sixteen things, and the one that mattered
was that the solver had disabled itself: `check_week2_model` compared its reconstruction against
the live azimuthal table, which `--write` replaces, so the script ran exactly once and then
refused. There is no way I catch that from inside a session where the only two ways I ever ran it
were before `--write` or in the same breath as it. The week 2 table is a constant in the file now.

Four figures inside frozen decisions were also wrong, all of them stale sweep numbers from before
I corrected the resultant normalisation, and the widest was calling a 2.36 times difference four
times. And I had quoted a band of 10 to 45 degrees for the side force off an axis label rather
than off a plotted value. That one is the least excusable, because the wider band made my own
uncertainty argument sound worse than the sources support, and I did not notice because it was
arguing against me. D45 carries all of it.
## 31 August 2026, week 4, structure and mass

This week died in the middle and got picked back up. The session running it hit an API failure
partway through and stopped, having written the solver, the numbers, three design documents and
a pile of gate changes, and having committed exactly none of it. Nothing was lost, because it
was all sitting in the working tree, but nothing was recorded either: no decisions, no progress
file, no handoff, no audit. The recovery was reading 786 lines of somebody else's uncommitted
work before touching any of it, then finishing the week from there. I did not restart it and I
did not rewrite what was already right.

What I did change in the inherited work was small and I want it written down. Three fixtures in
`test_gates.py` had gone stale against a gate the same session added, and one gate the session
added was arguably too clever, so the fix was to teach the fixture what a structure block now
contains rather than to soften the gate. The `02` blade build-up paragraph still said 29.4 g per
blade three paragraphs above a section explaining that week 4 had rebuilt the blade. The
`03` numbers block still declared the old servo torque, 1.3 percent out, which is inside the
gate's 2 percent display tolerance and therefore invisible. And the BOM called its date field
`quote_date`, which claims something that did not happen.

That last one is the thing I would defend hardest. Every price in the BOM is a guess at a
distributor list price. It is a decent guess, and the make against buy split and the lead times
are worth more to a reviewer than the rupee figures are, but a field called `quote_date` says a
supplier was asked and no supplier was asked. It is `priced_date` now, and the document says so
above the table in bold. D52.

The engineering itself came out better than I expected in one place and worse in another.

Better: the blade. Integrating the NACA 0020 section instead of assuming a shape factor gave a
perimeter of 2.090 chords against the 2.05 week 2 used, so the skin is heavier, and drawing the
root close-out as real fittings took a 4.53 g allowance to 6.65 g. That is only 2.3 g a blade,
but it is the kind of drift that turns into a failed budget if you find it in week 5. The
section itself is stiff: 51.1 Nm2 of EI, and skin wrinkling over the foam sets the allowable at
25.25 Nm, not the fibre.

Worse, or at least more interesting: the blade margin the gate had been checking since week 2 is
the wrong margin. Aerodynamic bending is 0.87 Nm and the section takes 25.25, so it reads 28.99
and it reads that whatever you do to the blade. Centrifugal bending is 8.04 Nm. Runco measured
centrifugal beating aerodynamic by 4.4 times on a much smaller rotor and this design is at 9.2,
which is the whole reason D16 exists, and the gate still could not see it. Combined and at a 1.2
overspeed, the blade margin is 1.97 and the attachment is 1.69. Those two are the design now.
Everything else in the module is over 3.

The mass closed and it closed without a fallback. 607.97 g nominal, 684.70 conservative, stacked
conservative T/W 2.5457 against a hard 2.5. Week 2 handed this week a case clearing by 4.8 g and
it now clears by 12.5. That reads like a win and it is a modest one: refinement bought 35.65 g of
growth allowance and gave 27.92 g of it straight back in real parts, because the gear pair week
3 found missing is 12.4 g and the drawn brackets and close-outs are most of the rest. Net 7.73
g.
The 2.75 target is still 50.9 g away and I am not going to reach it by trimming.

The balance decision was the one I expected to agonise over and it took ten minutes once the
number existed. Balancing the blade chordwise costs 35.47 g and takes the stacked case to 2.406,
under the limit. It buys a pitch link margin of 4.69 in place of 3.30. You do not spend a
requirement to improve a margin that already passes twice over. D46, and the three things that
could reopen it are named in the entry.

One process note. The two scripts now have a run order, linkage first then structure, because
linkage imports the blade build-up from structure and structure reads the pitch link load back
out. That is a cycle and it is resolved by hand, which I do not love. It is honest at least: the
alternative was leaving `BLADE_PARTS_G` as a hand copy that no gate could see going stale, which
is exactly the debt week 3 wrote down. Week 5 should not need to touch either script.

The audit found thirteen things and two of them stung. The balance trade, which I had just
finished calling an easy decision, was priced by multiplying the link load by 0.655. That is
the week 3 balanced-to-unbalanced ratio, on the week 2 blade, hardcoded, and it sat one line
under a docstring explaining that the blade had changed. The real balanced link load is 74.62
N and the margin 4.69, not 69.4 N and 5.04, and the wrong pair had reached five documents
including the decision entry. The decision itself survives, since 2.406 is under 2.5 either
way, but I wrote a number I had not computed and then repeated it everywhere. It comes from
the solver now.

The other one: `structure.py` wrote `numbers.json` with the platform newline, so it put CRLF
back into a file `linkage.py` had just written LF, in a repository that declares eol=lf. Git
normalises on the way in, so `git status` was clean and `git diff` was clean and the working
tree file was 1520 bytes bigger than the blob. My own claim that the file reproduces byte for
byte was only true after git had touched it. `linkage.py` carries a comment about that exact
trap, three lines long, written in week 3. I read that file this week and still wrote the bug
into its sibling.

Eleven more, all fair, all fixed or recorded. Two claims that overreached, one margin in an
eight row table that no gate was reading, an arithmetic slip in the mass decomposition that
did not sum to its own stated net, and a material row crediting the epoxy with a margin
nothing computes. D53 carries the corrections that land inside frozen entries.
