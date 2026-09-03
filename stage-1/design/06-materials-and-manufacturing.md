# Materials and manufacturing

Required Stage 1 item 6, and the manufacturing half of the 10 percent cost and manufacturability
criterion. Every material here was chosen because a structural calculation in
`08-structure-and-loads.md` needed an allowable, and every allowable that document uses is
defined once, in the `MATERIALS` table at the top of `tools/structure.py`. Prose and calculation
therefore cannot disagree about what the epoxy is worth.

The module is 20 bought lines and 5 made ones. Nothing in it needs a process a university lab or
a job shop in an Indian metro cannot run, and the one part with no Indian stockist is called out
below.

## Material selection

Six materials carry load. The right hand column is the margin each one decides, so a reader can
work backwards from any number in the structures document to the property it rests on. Five of
the six have one. The adhesive does not, and that is the honest state of it: no bond line
demand, allowable or margin is computed anywhere in week 4, and the structures document lists
continuous bond lines among its stated assumptions. The 8 MPa is quoted here because the joint
list is what sizes the bonds at Stage 2 and the allowable it will be sized against ought to be
on the record now.

| Material | Where | Density | Modulus | Allowable | The margin it sets |
| --- | --- | --- | --- | --- | --- |
| Rohacell 51 IG class PMI foam | blade core, 88 percent fill | 52 kg/m3 | 70 MPa, 19 MPa shear | 0.8 MPa | blade bending, through skin wrinkling |
| 60 gsm 2x2 carbon twill, 2 plies | blade skin, 0.142 mm cured | 1550 kg/m3 | 60 GPa | 400 MPa | blade bending, 3.00 and 2.08 |
| roll wrapped CFRP tube | spar, pitch links, rotor shaft, frame | 1550 kg/m3 | 130 GPa | 700 MPa, 55 MPa shear | shaft torsion 16.18, combined 9.90 |
| 7075-T6 aluminium | horns, root fittings, brackets, blocks, lugs | 2810 kg/m3 | 71.7 GPa | 400 MPa | pitch link path, 3.29 |
| 6061-T6 aluminium | pulleys, carrier ring gear, sector gear | 2700 kg/m3 | 68.9 GPa | 240 MPa | none, these are stiffness parts |
| Araldite 2011 class epoxy paste | shaft plugs, root fittings, block bonds | 1050 kg/m3 | | 8 MPa shear | none yet, see below |

**The foam is a structural material here and not a filler.** Skin wrinkling over a soft core is
what limits the blade, at 215.3 MPa, and that stress is half the cube root of the product of
three moduli: the skin's 60 GPa and the core's 70 MPa and 19 MPa. Two of the three belong to the
foam. Drop to a 32 kg/m3 grade and the wrinkling stress falls by roughly a quarter, which takes
the combined blade margin at overspeed from 2.08 to 1.64. That still clears the 1.5 floor, and
this section used to say it did not. The grade is part of the structure either way and a
substitution means a recalculation, which is the point that survives.

The laminate's own 400 MPa never gets reached. Neither does the spar's 700 MPa, which would
carry 63.19 Nm on its own against the 25.2528 Nm the section is signed off at. Both are quoted
so a reader can see which one governs.

Allowables carry their process knockdown already, so the margins that come out of them are
safety factors and not a second helping of the same conservatism. The paste adhesive is the
clearest case. 8 MPa is a quarter of the published lap shear for that class, which covers a hand
mixed bond line with an uncontrolled thickness and no post cure.

**Where this evidence is thin.** These are published typical values for the material classes,
taken from manufacturer data for the class and not from a certificate for a specific batch. No
coupon has been tested. For 7075-T6 and 6061-T6 that is a small risk, since both are stocked to
a standard. For the foam, the laminate and the paste it is a real one, because cured properties
depend on the layup and on the resin fraction a hand wet layup achieves.

Which of the two is worth testing first was worked out rather than assumed, and the answer is not
the one this section carried until now. Skin wrinkling over the foam sets the blade allowable, at
half the cube root of the three moduli, and the allowable moment is that stress times EI over the
skin modulus. Lower the skin modulus and the wrinkling stress falls as its cube root while EI over
the skin modulus rises, because the spar and the foam terms stay where they are. Sweep the skin
from 0.5 of its published value to all of it and the worst overspeed margin anywhere in that band
is 2.0739, against 2.0839 at the published value. Under 1 percent across a 2 to 1 range.

The foam is the sensitive one, because its modulus and its shear modulus both sit inside the same
cube root. Knock the pair down together and the allowable moves as the two thirds power, and the
overspeed margin reaches 1.5 at 0.6144 of the published foam properties. The realistic version of
that is a grade substitution rather than a shortfall, and it is milder: on Rohacell 31 IG instead
of 51 IG the blade weighs 28.057 g rather than 31.75, so the centrifugal demand falls with the
allowable and the overspeed margin lands at 1.6351. It still clears.

So the blade is a foam limited structure, not a laminate limited one, and both floors are gated.
Coupon testing is Stage 2 work and it is listed at the end.

## Manufacturing

Every part, its stock form, how it gets made, the one tolerance that matters and how it joins to
what sits next to it.

| Part | Material and stock | Process | Key tolerance | Joins by | Make or buy |
| --- | --- | --- | --- | --- | --- |
| blade core | PMI foam block, 20 mm | CNC profiled in two halves, spar channel cut | section profile 0.15 mm | bonded to the skin in the mould | make |
| blade skin | 60 gsm twill, wet layup | 2 plies in a machined two part mould, vacuum bagged, room temperature cure | mould split line 0.1 mm | co-cured onto the core | make |
| blade spar | 8.71 mm CFRP tube | cut to span, abraded | bond gap 0.1 mm | paste adhesive into the core channel | buy stock |
| root fittings | 7075-T6 bar | turned, bored to the spar | bore fit 0.02 mm | bonded over the spar, then pinned | make |
| spider arms | CFRP plate, 1.5 mm | CNC routed, 6 off | pitch circle 0.05 mm | bolted to the boss, bonded at the bracket | make |
| hub bosses | 7075-T6 bar | turned and milled, reamed bore | bore to shaft 0.015 mm | clamped on the shaft | make |
| root brackets | 7075-T6 plate | CNC, clevis form | pin bore 0.02 mm | bolted to the arm | make |
| pitch horns | 7075-T6 plate, 4 mm | CNC, 3 off | radius 0.05 mm | bonded and pinned into the root fitting | make |
| pitch links | 4 mm CFRP tube | cut, rod ends bonded in | free length 0.05 mm | rod end ball into horn and post | make from stock |
| carrier ring and sector gear | 6061-T6 bar | turned, then gear cut as job work | backlash 0.05 mm | bolted, running on 2 bearings | make |
| rotor shaft | 16 mm CFRP tube | cut to 340 mm | journal 15 mm h6 | plugs bonded in, journals ground after | make from stock |
| shaft end plugs | 7075-T6 bar | turned | interference 0.03 mm | bonded into the tube | make |
| pulleys | HTD-3M blanks in 6061 | bored and faced from a stock blank | bore 0.015 mm | clamped, one grub screw each | buy and modify |
| bearing blocks | 7075-T6 plate, 9 mm | CNC, bore in one setup | bore 0.010 mm | bolted to the frame tubes | make |
| motor plate and lugs | 7075-T6 plate | CNC, one setup | hole pattern 0.1 mm | bolted | make |
| frame tubes | 8 mm CFRP tube | cut square | length 0.2 mm | clamped into the blocks | buy stock |

The 3 CNC job lines in the cost table cover 6 part families between them, so a shop quotes them
as batches instead of as singles. The smaller turned and milled parts, the root fittings, hub
bosses, pitch horns and shaft end plugs, are not separate job lines: their machining sits inside
those same 3 jobs and their metal inside the 7075 stock line. The gear pair is the only job that
needs a cutter nobody local keeps on the shelf. Everything else is turning, milling or routing.

**Assembly order.** It matters, because two of these joints cannot be reworked once cured.

1. Bond the shaft plugs into the tube, then grind both journals in one setup. Grinding after
   bonding is what makes the two journals concentric, and doing it the other way round is how a
   bonded shaft ends up with 0.1 mm of run out that nothing takes back out
2. Build the 3 blades: core, spar, skin, cure, trim, then bond and pin the root fittings and the
   horns. Weigh each blade as it leaves the mould
3. Mate the spiders to the shaft, then hang the blades on their pitch bearings through the root
   brackets
4. Fit the main bearings and the bearing blocks to the frame tubes and drop the rotor in
5. Fit the phasing carrier, its 2 support bearings and the offset post, then the 3 pitch links.
   Rod ends are adjustable, so link lengths get set here against the schedule and not at the
   drawing
6. Motor, plate, pulleys, belt, tensioner. Belt tension goes last, because tensioning pulls the
   motor plate along a slot
7. ESC, controller, servos, harness

**What gets measured before it spins.** A rotor at 2337 rpm with a 209 N pull on every blade is
not a thing to power up hopefully.

- Blade masses matched inside 0.5 g across the set of 3. On the 110 mm radius that residual is
  about 3.5 N of once per revolution bearing force, which the 61802s absorb without noticing.
  The unbalance limit that ought to back that number up is a Stage 2 calculation and it is not
  set here
- Shaft journal run out under 0.02 mm on the assembly jig with a dial indicator, and rotor
  radial run out at the blade tips under 0.5 mm
- Pitch angle checked against the solved schedule at 12 azimuths, by hand rotation. What matters
  is peak to peak travel, 79.9 degrees, because the link length sets it and the rod ends can
  correct it
- The rotor turned by hand through 2 full revolutions with the servos at each end of their
  travel, watching for a link going over centre. The worst transmission angle in the design is
  135.68 degrees, which is 44.32 degrees from a right angle read folded, and it wants feeling
  rather than assuming
- Belt tension by span deflection, and a static pull test on one blade attachment to 340 N,
  which is above the overspeed centrifugal load of 301.192 N
- First spin staged at 600, then 1200, then 1800, then 2337 rpm, with current draw logged at
  every step against the predicted 19.29 A

## Cost

Priced 31 August 2026 in Indian rupees. **These are indicative prices at distributor list level
and they are not obtained quotations.** Nobody was contacted, no listing was fetched during week
4, and the source column names the distributor a part would be bought from and not one that has
quoted for it. Confirming them is Stage 2 work and it is carried as a debt. The field in
`numbers.json` is `priced_date` for that reason.

| Item | Make or buy | Qty | Unit INR | Line INR | Lead | Likely source |
| --- | --- | --- | --- | --- | --- | --- |
| T-Motor Antigravity MN5006 KV450 | buy | 1 | 8500 | 8500 | 3 wk | Quadkopters, New Delhi |
| 40 A 8S brushless controller | buy | 1 | 3600 | 3600 | 2 wk | Robu.in, Pune |
| 20 g class digital metal gear servo | buy | 2 | 1900 | 3800 | 2 wk | Robu.in, Pune |
| Matek F411-WSE class controller board | buy | 1 | 3900 | 3900 | 3 wk | Quadkopters, New Delhi |
| 693ZZ miniature bearing | buy | 12 | 60 | 720 | 1 wk | local bearing house, Mumbai |
| MR128ZZ miniature bearing | buy | 2 | 90 | 180 | 1 wk | local bearing house, Mumbai |
| 61802 deep groove bearing | buy | 2 | 240 | 480 | 1 wk | local bearing house, Mumbai |
| M3 aluminium bodied rod end | buy | 6 | 180 | 1080 | 2 wk | Robu.in, Pune |
| HTD-3M belt, 9 mm wide, 375 mm | buy | 1 | 470 | 470 | 2 wk | Powergear, Coimbatore |
| HTD-3M pulley blank, 16 tooth | buy | 1 | 650 | 650 | 2 wk | Powergear, Coimbatore |
| HTD-3M pulley blank, 68 tooth | buy | 1 | 1600 | 1600 | 2 wk | Powergear, Coimbatore |
| Rohacell 51 IG block, 300 by 150 by 20 mm | buy | 1 | 2600 | 2600 | 4 wk | importer landed price, no Indian stockist found |
| 60 gsm carbon twill, 1 m2 | buy | 1 | 1400 | 1400 | 2 wk | Composites Today, Chennai |
| epoxy laminating resin and hardener, 500 g | buy | 1 | 1600 | 1600 | 1 wk | Composites Today, Chennai |
| Araldite 2011 paste adhesive, 50 ml | buy | 1 | 950 | 950 | 1 wk | Huntsman distributor, Mumbai |
| CFRP tube stock, four diameters | buy | 1 | 2900 | 2900 | 3 wk | Carbon Fiber India, Coimbatore |
| 7075-T6 bar and plate stock | buy | 1 | 2200 | 2200 | 2 wk | metal stockist, Mumbai |
| 6061-T6 bar stock | buy | 1 | 700 | 700 | 1 wk | metal stockist, Mumbai |
| M3 fasteners, washers and threaded inserts | buy | 1 | 900 | 900 | 1 wk | fastener stockist, Mumbai |
| silicone wire, connectors and heatshrink | buy | 1 | 900 | 900 | 1 wk | Robu.in, Pune |
| blade mould, two halves from tooling board | make | 1 | 9000 | 9000 | 3 wk | CNC job work against the section drawing |
| spider arms and root brackets, CNC job work | make | 1 | 6500 | 6500 | 2 wk | CNC job work, 7075 and CFRP plate |
| bearing blocks and motor mount plate, CNC job work | make | 1 | 4800 | 4800 | 2 wk | CNC job work against the block and plate drawings, 7075 |
| carrier ring gear and servo sector gear | make | 1 | 5500 | 5500 | 3 wk | gear cutting job work, 6061 |
| rotor assembly and balancing jig | make | 1 | 3000 | 3000 | 2 wk | aluminium extrusion and a dial indicator mount |

Bought parts and material come to 39130 INR, tooling and fabrication to 28800, and the module
totals 67930 INR. Longest single lead is 4 weeks.

**The five lines above 4500 INR, and what each one rests on.** Together they are 50 percent of
the total, so they are the ones worth defending. The motor at 8500 is the one component in the
module read off a manufacturer's datasheet, and 8500 is the published Indian retail figure for
that part. The blade mould at 9000 is a shop rate for machining 2 halves out of tooling board
against the section drawing, estimated from the volume and the setup instead of quoted. The 3
CNC lines at 6500, 5500 and 4800 are shop rates for a batch of parts each. Of those, the gear
pair is the one that could move most, because gear cutting at a quantity of one is priced by
setup and not by metal.

**Bought against made.** 58 percent of the money is bought parts and 42 percent is tooling and
job work, and the split flatters the module a little: the mould and the jig are one time costs
that a second unit does not pay. A second rotor costs about 55930 INR, because 12000 of that
tooling does not repeat. The 3 CNC job lines do.

**What drives the schedule.** The 4 week Rohacell import is the critical path and it is the only
line with no Indian source. Ordering it first is the whole mitigation. Every 3 week item, the
motor, the controller board, the CFRP tube stock and the gear cutting, sits inside it. If the
foam slips, a 30 kg/m3 EPS core is not a drop in substitute, since the wrinkling calculation
above depends on the core moduli, so the fallback is a thicker skin and a rerun.

## Mass reserve

The budget carries a visible 15.00 g reserve on the frame and mounting group, which is 2.2
percent of the 677.91 g nominal module. It sits on that group because the frame is the least
developed part of the design and week 2 said so first, and it covers gussets, cable clamps, the
servo bracket and the ESC tray. None of those is drawn.

That reserve is separate from the conservative column. 763.24 g against 677.91 is 85.33 g of
growth allowance, itemised line by line at a rate set by what each line is made of, and the
thrust to weight requirement is tested against the conservative figure. The module therefore
carries its uncertainty twice: once as an undrawn hardware allowance inside the nominal budget,
and once as a per line growth rate over the top of it.

## What Stage 2 owes this section

- **Coupon data, foam first.** A sandwich wrinkling coupon on the delivered foam, because the
  blade allowable moves as the two thirds power of the foam properties and reaches its floor at
  0.6144 of them. Then the certificate for the delivered grade. The laminate panel comes after,
  for areal mass and for the deflection and wind up numbers, since a skin shortfall barely
  touches the strength margin. Plus a bond shear coupon
- **Real quotations.** Every price here is indicative. The 5 lines above 4500 INR need written
  quotes, and the gear cutting needs a shop that has seen the drawing
- **A balance tolerance.** The jig is budgeted. The acceptance number behind it is not calculated
- **A mould trial.** A first blade out of a wet layup mould usually comes out heavy, and the
  blade lines are 14.0 percent of the module

## Numbers used

- results.total_mass_g = 677.91
- results.mass_g_conservative = 763.24
- results.bom_bought_inr = 39130
- results.bom_tooling_inr = 28800
- results.bom_total_inr = 67930
- results.bom_longest_lead_weeks = 4
- structure.blade_allowable_Nm = 25.2528
- structure.blade_ei_Nm2 = 51.115
- structure.blade_attachment_allowable_N = 781.148
- structure.pitch_link_allowable_N = 474.074
- structure.shaft_allowable_Nm = 24.9563
- structure.centrifugal_load_overspeed_N = 301.192
- structure.blade_combined_margin = 3.0008
- structure.blade_combined_margin_overspeed = 2.0839
- structure.pitch_link_margin = 3.3015
- structure.blade_wrinkle_stress_MPa = 215.2638
- structure.blade_allow_skin_Nm = 25.2528
- structure.blade_allow_spar_Nm = 63.1857
- structure.blade_skin_modulus_GPa = 60.0
- structure.blade_foam_modulus_MPa = 70.0
- structure.blade_foam_shear_MPa = 19.0
- structure.blade_skin_band_low = 0.5
- structure.blade_skin_band_worst_margin = 2.0739
- structure.blade_foam_knockdown_at_floor = 0.6144
- structure.blade_foam_downgrade_margin = 1.6351
- structure.blade_foam_downgrade_blade_g = 28.057