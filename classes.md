# Classes (Nov 20, 2026: full pass)

The first four classes (the vertical slice), designed the same way: **fantasy → verbs → basic moves → the places mutations act on.** Answers to **pillars.md** (characters, not hires; four move slots, two to start; mutations by grammar; the upgrade parts and status shapes in Part 5c).

**Status key.** **Locked** means agreed in conversation (Nov 20). **Proposed** means Claude's suggestion, not yet confirmed. **Settles in the mutation session** means the shape is agreed and the exact parts or numbers aren't. New words are marked *coined*, with their sources so we can check them.

---

## Part 1: The Model (Locked)

- **A class is a fantasy, and the fantasy names its verbs.** Each class has **five or six verbs** (jobs). Two are its **starting kit**; the rest turn up during a run as basic moves (tomes, rewards, weapons), and every one of them can be mutated.
- **Basics are verbs, not elements.** Two roots with every mutation is a big combinatorial space but a thin strategic one: builds differ by *what jobs a hero does*, not by how hard.
- **A move is its built-in effect plus one rider slot.** A status move (Reyk, Sveda, Naglskott) *is* its effect; Lonn fills the rider slot with a second, designated one.
- **One signature mechanic per class,** and it **touches at least one other class's** (a designed synergy). Emergent synergies come on top. One per class also caps the cost: each new status is an icon, a line of text, and AI that knows how to value it.
- **Every move has designated riders.** Lonn offers only those (pillars Part 5c). A move without a sensible rider simply has no Lonn branch: Eld has no Styngeld, and a part that does nothing noticeable is shelved.
- **One catalog, two routes.** Every move has a value from its parts. A rare move you *find* is a pre-mutated one: an Alleld tome is the same move you could grow by carving All onto Eld. Rarity follows value: plain verbs common, two-part moves uncommon, capstones rare.
- **Unlocks by deed:** each class unlocks when you do something that class would value (pillars Part 4).

---

## Part 2: Brennumar (Locked)

*The Tactical Arsonist: burns and vanishes.* Eld school (child: Reyk). Weapon class: Brand. Magical: uses MP, Meditates. **Unlocked from the start.**

| Verb | Job | Basic move | Lonn rider | Notes |
|---|---|---|---|---|
| **Strike** | Fire damage | **Eld** | **Scorched** | Starting kit. No Styng: Eld *is* the damage |
| **Blind** | Lower their Accuracy | **Reyk** (no damage): inflicts **Blinded** | **Eitr** (poisoned smoke) | Starting kit. One Blinded stack; Mereyk two; Jattereyk to the cap |
| **Burn** | Damage over time | **Sveda** (no damage): leaves **Scorched**; **its tier sets the blow** | **Feeble** (a burned arm) → **Lonnsveda**: "Apply Scorched and Feeble." Alternatives: Ogn, Reyk | Swedish *sveda*, "to singe, scorch" (ON *svíða*). Sveda is also a rider prefix |
| **Vanish** | Protect your side with smoke | A defensive Reyk: Nimble for one, a row, or all; plus a strong, expensive single-target "evade everything for one turn" | Settles in the mutation session | The "vanishes" half of his fantasy |
| **Cash in** | Pay off a setup | One move that **consumes Scorched** for burst; one that hits **Blinded** targets harder | Settles in the mutation session | Closed loops on his own verbs |
| **Stoke** | His own tempo | **Aukseid** (+1 MAT on himself), **Djupanda** | | Djupanda: "deep breath" |

**Reyk against a Reyk-weak target** always lands, adds an extra Blinded stack, and still earns the Bonus Round: the weakness puzzle pays status moves too.

**Blinded** (the build shape, pillars Part 5c): Blinded *N* is *N* ACC stages down, cap three, losing a stack at the end of each round it isn't refreshed. "Reyk, Reyk, Reyk" is Blinded 3. (Today's engine Blinded also lowers EVA; that goes, since can't-dodge is Marked's job.)

**Signature mechanic: Scorched** (the fade shape, pillars Part 5c).
- A fire you feed: **100% of its damage on the first tick, then 50%, then 20%, then out** (an ember).
- **Its damage is the caster's, not a share of the target's HP** (Nov 20): when it lands, one Eld hit at the Sveda's tier, from his MAT against the target's MDF and its Eld affinity, × 0.6 (a knob). So it's about one hit spread over three rounds, and a boss's size doesn't feed it. *Percentages of max HP belong to Eitr (stacking poison, 2/4/6%: next, after the bug-fix checkpoint).*
- **Sveda again starts it over** (reset, not stack), **with its own blow**: a cheaper Sveda over a hotter burn burns at the cheaper tier.
- **Hit by wind (Blast), a Scorched target flares back to 100%,** keeping its blow. It touches the **Skurmar**: a Brennumar and a Skurmar in the back row become a forge, and a free Halvblast can keep a fire going as long as he spends his turns on it.
- Not poison: poison is a clock (patience); Scorch is a fire you feed (tempo).

**Djupanda** (any magical can learn it): a **wind-up**, using the Bid manner's machinery. Declare it, spend the next turn building ("Djupanda..."), and a large MP windfall lands. **It can be interrupted** (Stun, Frozen, the Drattr's net), so it rewards keeping the caster safe. Mutations: target an ally at a reduced rate, a bigger windfall, a Swift version that's smaller but harder to interrupt.

**Capstone:** ***Skogsbrand*** ("forest fire"): All + Mer + Styng + Lonn on Sveda, the whole field set burning.

---

## Part 3: Ullar (Locked)

*The Hunter: pins the prey, and finishes it from afar.* Bowman: kills from range, helpless once a blade reaches him. Weapon: Bow (Pierce, Long). Martial: techniques cost HP. Weak to Slash. **Unlocked from the start.** Name: Ullr, god of the bow, skis and the hunt.

| Verb | Job | Basic move | Lonn rider | Notes |
|---|---|---|---|---|
| **Shoot** | Damage at range | **Skott** | **Bleeding** → **Blotskott** | Starting kit. Merblotskott, Flokblotskott keep their spoken names |
| **Pin** | Slow it and root it | **Naglskott** (no damage): inflicts **Pinned** | Settles in the mutation session | Starting kit. **Styng** adds damage (Styngnaglskott); **Mer** makes a longer Pin. Mer + Styng is ***Geirskott*** (ON *geirr*, "spear": a pike-length shaft that pins the leg), a byname |
| **Mark** | Strip its defences | **Peka** (*coined*: Swedish *peka*, "to point"): inflicts **Marked** | **Sundered** → **Lonnpeka** (he points out the gap) | Styngpeka adds damage. Merpeka: Marked 2 in one shot |
| **Volley** | Hit many | **Flokskott** | (as Skott) | Exists |
| **Finish** | Pay off a setup | **Banskott** (*coined*: ON *bani*, "death, slayer," + skott): **x1.5 against a Pinned target** | | His cash-in |
| **Put down** | Finish the wounded | **Avliva** (Swedish, "to put down": what a hunter does for wounded prey): **x2 against a foe under half HP** | | Single-target. Later: conditional riders of this kind |
| **Glide** | Escape his weakness | **Skrida** (Swedish *skrida*, "to glide"; ON *skríða*, as in the ancient "gliding Finns" on skis): **Swift**; **aimed at a cell, like Move** (Nov 20): an empty cell, he steps there; an ally's, the two swap places; Move's rules hold (never empty the Front, no Pinned ally). Gain Nimble either way | | Merskrida: Nimble 2. Ullr is the god of skis |

**Steady is dropped** (Aukhitt gave him nothing to notice).

**Nagl is a prefix any stabbing weapon can carry** (Naglskott, Naglspett): a pin travels with points, not with the Ullar.

**Signature mechanic: Pinned** (new status).
- **Slowed and rooted:** one Speed stage down for a few rounds, **and it can't change rows.** No Frozen chain (unlike Chilled). **Decided (Nov 20): it locks the cell,** the simplest version: no Move, Swap, Advance or Skrida (lanes too), and no one can swap with it. Pull them to the Front and Pin them there. Cover moves no one, for heroes or enemies, so a Pinned unit still Covers. Two rounds, three at Mer.
- **Touches:** the **Vasara's** Taunt (a Pinned enemy can't step out of reach of her hammer), and his own Banskott.

**Second status: Marked** (shared: anyone's hits benefit).
- **Marked is the EVA-down counter** (pillars Part 5c): Marked *N* is *N* Evasion stages down. **Marked 2 can't dodge** (no grazes); Marked 3 adds crits. "Can't dodge" moved here from Pinned, so each status does one clear thing.
- **Touches everyone,** the **Brennumar** most: his Reyks, Svedas and cash-ins land on a target that can't dodge.

**Capstones:**
- ***Tusensplitter*** ("a thousand splinters", Swedish): Drif + Mer + Blot + Skott, a bleeding flurry.
- ***Pilskur*** ("arrow-shower", Swedish *pil* + *skur*): All + Mer + Blot + Skott. It echoes the Skurmar's squall.
- ***Hasin*** (ON *hásin*, the hock-sinew, the hamstring): a heavy Styng + Nagl + Bleeding: "shot the prey in the leg."

---

## Part 4: Vasara (Locked)

*The Anvil: takes the blows meant for others, and answers with the hammer.* Shield-hammer: the shield takes cuts and blows; points slip past the rim. Weapon: Hammer (Crush, Short). Martial. Weak to Pierce. **Unlocked from the start.** Name: Finnish *vasara*, "hammer."

| Verb | Job | Basic move | Lonn rider | Notes |
|---|---|---|---|---|
| **Strike** | Crush damage | **Krosh** (renamed from Kross) | **Sundered** → **Brakrosh** | Starting kit |
| **Taunt** | Draw fire | **Egga** (from ON *eggja*, "to incite": the source of English "egg on"): **targets one foe (Flok: a row); its single-target attacks this round must go to her**, if they can reach her | **Blinded** → **Lonnegga**: the taunted foes are Blinded as she casts it | Starting kit. First (acts before nearly everything). Styngegga adds a strike |
| **Guard** | Take one ally's hits | **Lya** (Cover) | | The tank owns Cover (pillars Part 5) |
| **Sunder** | Break their armour | **Brakrosh** (*coined*: Swedish/ON *brak*, "a crash, a crack," + krosh; the doubled k collapses at the seam): inflicts **Sundered** | | Brak is a rider prefix, like Blot and Nagl |
| **Fortify** | Harden the line | **Aukskold** (confers Fortified): herself, then by mutation a row, then all (a shield wall) | | Exists in the stat grammar |
| **Answer** | Pay off taking hits | **Hevn** (Norwegian *hevn*, "revenge"; ON *hefnd*): strikes back harder for every hit she took since her last turn | | Her cash-in: closes the loop with Egga and Lya |

**Bidhevn** (Hevn with the Bid manner): she sets her feet and **absorbs a full round, then releases double.** The Patient manner was made for her. *Decided (Nov 20): double an equally primed Hevn (Hevn's own x2 for Bid, not Bid's x2.6), so at most x4 an unprimed Hevn. Hevn counts the attacks that hurt her since her last action opportunity (acted, lost to a stun, or a Bonus Round's), +25% each, up to +100%.*

**Signature mechanic: Sundered** (the build shape, pillars Part 5c).
- **Each cracking blow adds a stage, up to three;** each stage is one DEF stage down.
- **At the end of every round it wasn't struck, it loses a stage.** So the enemy she keeps hitting stays at three, and the ones she neglects decay. (Engine: a "struck this round" flag.)
- **Touches the Ullar:** **Pierce finds the gaps.** Pierce hits on a Sundered target deal extra damage. **The Ullar's Lonnpeka also confers it:** without her, a stack for his own arrows; with her, he refreshes her three while she Taunts or Guards, so it doesn't decay. A **Swift Brakrosh lands before the Ullar's arrows in the same round:** the fighter opens the armour and the ranger shoots through it in one turn.
- Her Taunt and Answer also touch everyone: the more the enemy hits her, the less it hits the back row, and the harder she answers.

**Capstone:** ***Holm*** (from *holmgang*, the duel fought on an islet): Egga's peak, grown from Styngegga, a taunt that becomes a challenge and strikes. The exact parts settle in the mutation session.

---

## Part 5: Dagskald (Locked)

*The Skald: sings the party whole, and smites with daylight.* Sol school (child: Lak, healing). Weapon class: Instrument (harps, flutes, horns, the Bronze Age *lur*). Magical. **The first unlock.** Name: Swedish *dag*, "day," + skald. Germanic healing magic was sung (*galdr*, from *gala*, "to chant").

| Verb | Job | Basic move | Lonn rider | Notes |
|---|---|---|---|---|
| **Mend** | Heal | **Lak**: one ally; **Flok** a row, **All** the party (Nov 20), each scaled like damage | **Nimble**, spoken Sol → **Solak** ("light-mending": the light makes them harder to hit; Nov 20, replacing "cleanse one", which needed an order players would have to memorise). Floksolak, Allsolak, Mersolak (Nimble 2) | Starting kit. **Heals read WIS** in the new game (Nov 20): the healer's own lever, apart from attack magic's MAT |
| **Smite** | Daylight damage | **Sol** (a weak Ray) | **Blinded**, spoken Blinda → **Blindasol** | Starting kit. Not Scorched: that stays the Brennumar's |
| **Sing** | Sustained healing that grows | **Kvad** (Norwegian/Danish *kvad*, "a lay, a poem"; ON *kvæði*) | | His signature (below). Merkvad adds two verses |
| **Cleanse** | Clear statuses | **Skolja** (Swedish *skölja*, "to rinse") | | Clears every harmful status and lifts every lowered stat to neutral: cleansing is wholly Skolja's job (no cleanse-one: if one returns, the badges sit worst-first and it clears the front one, so the order is on screen) |
| **Wake** | Bring back the Dying | **Vakna** (Swedish *vakna*, "to wake"): revive a Dying ally | | |
| **Inspire** | Lift the party | **Aukraft** (+1 ATK; the doubled k collapses at the seam): one ally, then by mutation all (a battle-song) | **+1 DEF** → **Lonnaukraft** (ATK and DEF up) | Stat grammar: Kraft is ATK |

**Signature mechanic: the Song, Kvad** (the build shape, pillars Part 5c).
- **Each singing adds a verse** (Merkvad adds two), **up to three.** The party heals every round: **verse × base.** *As built (Nov 20, Joseph): **Song is a counter on the ally**, the math of Fortified. Kvad adds a stack to one ally (Merkvad two, Flokvad one to a row, Allkvad one to everyone), up to three; at each round's start Song heals for each stack (a single Kvad's stack: 4/9 of his Base Lak at his WIS; Flokvad and Allkvad their reach's share), and a round nobody sang to them, it loses a stack. So he builds it, then plays whack-a-mole: three Kvads bank the tank at three, one Allkvad a round holds the party. Each ally's Song remembers the last singer's heal. It outlives a fallen singer and fades; falling clears it from the fallen. Measured, not trimmed: the sweep decides.*
- **At the end of every round he doesn't sing, it loses a verse.**
- So each turn he chooses: advance the song, hold it at three (which costs his turn), or let it fade while he does something else (a Djupanda, a Vakna). A real tempo game.
- **Touches the Vasara:** Lya and Egga keep the singer singing, and **Kvad on the Vasara loops with Egga and Hevn**: she draws the hits, the song keeps her up, and every hit she survives feeds her answer.
- **Unlock by deed:** finish a leg (or a whole dive) without a healer.

---

## Part 6: How the Four Touch

| Signature | Its partner | What happens |
|---|---|---|
| **Scorched** (Brennumar) | The Skurmar's wind | A wind hit flares the Scorch back to 100%. *(The Skurmar is the fifth class: Part 7.)* |
| **Pinned** (Ullar) | The Vasara | A Pinned enemy can't leave her hammer's reach |
| **Marked** (Ullar) | Everyone; the Brennumar most | A Marked target can't dodge, so status moves and cash-ins land |
| **Sundered** (Vasara) | The Ullar | Pierce finds the gaps; a Swift Brakrosh opens them in the same round |
| **Blinded** (Dagskald's Sol) | The Brennumar | Sol can set up his Blinded cash-in |
| **Song** (Dagskald) | The Vasara | Her protection keeps the song growing; Kvad, Egga and Hevn loop |

Any three of the four make a party with at least one designed synergy.

---

## Part 7: Skurmar (Locked effects; numbers unpriced)

*The Weather-Witch: ties the wind in knots, and lets it loose.* Blast school (child: Blixt). Weapon class: Stav (the seeress's staff, found in real völva graves). Magical. Pure tempo: he banks turns and spends them. From the sailors' tales of Finnish and Sámi wizards who sold wind tied in three knots: one for a breeze, two for a gale, three for a storm.

| Verb | Job | Basic move | Notes |
|---|---|---|---|
| **Gust** | Wind damage | **Blast**: two light hits | Starting kit. Every wind hit flares Scorched back to 100% |
| **Tie** | Store the wind | **Knyta** (Swedish *knyta*, ON *knýta*, "to tie"): no damage, ties a knot; Merknyta ties two | Starting kit |
| **Bolt** | Lightning | **Blixt**: wild, high-swing damage. **Lonnblixt** adds Stunned (bosses immune) | Plain Blixt has no Stun: its rider slot is open |
| **Untie** | Spend the wind | **Kuling**, **Storm**, **Orkan** (the Swedish wind scale): separate spells, found, each rarer and stronger. Each costs knots (1, 2, 3) **on top of** MP, and can be mutated (Merorkan: still 3 knots, more MP) | Kuling: a light wind on all. Storm: a strong wind on all. Orkan: a strong wind on all, then lightning on all |
| **Sweep** | Move the enemy | **Kasta** (push; ON *kasta*, the source of "cast") and **Svepa** (pull; "to sweep"): no damage; Styng adds the battering | Displacement |
| **Fair wind** | Party tempo | **Medvind** (Swedish and Norwegian, "tailwind"; literally "with-wind"): one ally gains Quick; Flok a row, All the party (Flokmedvind, Allmedvind) | Renamed from Byr (it read as "beer") |

**Signature mechanic: Knots.**
- **Knyta ties knots, up to three. They don't decay; they're spent** (a pool he holds, not a status on a target). **Knots carry between rooms** (to test for power).
- **Holding pays, and it builds up:** Knots 1: Blast hits harder. Knots 2: Blixt can't graze. Knots 3: half a Meditate's MP back each turn.
- **Spending pays more:** the untie spells. Holding all three costs three of his four slots; without them he's still a stronger witch while he holds.

**Kasta and Svepa:** a target pushed or pulled into an occupied space **swaps with the occupant, and both take bump damage.** **A Pinned target can't be moved: it's a wall** (slam another into it: the bump without the swap). Later: ground hazards.

**Touches:**
- **The Brennumar (the forge):** wind flares Scorched; Orkan flares every Scorch on the field.
- **The Vasara:** Svepa pulls a rear caster into her hammer's reach; Egga holds it there.
- **The Ullar:** a Pinned enemy is a wall for Kasta.

**Unlock by deed:** wipe out a whole pack with one All-move.

**As built (Wave 4c, Nov 20):** knots are a pool on the Skurmar (`u.knots`), tied a knot a tier by Knyta (Merknyta two), spent by Kuling, Storm and Orkan (1, 2, 3: a spell spends what it costs, so Orkan always leaves none) on top of MP. **Knots are this fight's (Nov 21, Joseph):** they start at none every fight and don't carry; prepping between fights is the player's to arrange, not a class's. Held, 1+ makes Blast hit x1.25, 2+ means Blixt never grazes, and **3 is the wind-witch's focus: his Meditate and Djupanda restore half a Meditate more** (Meditate 15% to 22.5% of max MP, Djupanda 40% to 47.5%; moves, not items). No MP on its own (it was 9 MP a round, more than a Blast costs: free Blasts for the rest of the fight). Orkan: the wind on all, then an All Blixt at its tier on everyone still standing. A class verb's riders are its own, so plain Blixt never Stuns; Lonnblixt rolls Stunned (bosses immune). Kasta and Svepa shove a foe a row back or forward in its lane; into an occupied cell the two swap and both are slammed: each takes 5% of its own max HP plus 5% of the other's (Nov 20, Joseph: relative to both bodies, so small things are bowled over by big ones); a Pinned unit is a wall (not moved; a foe shoved into it is slammed with it and stays); past the edge it isn't offered. Styngkasta and Styngsvepa batter first with a gust (Blast), and Cover takes them whole.

**Open:** the numbers (knot bonuses, the untie spells' power and MP); the capstone.

---

## Part 7b: The Yardstick (Nov 21: the level-50 soft launch)

Heroes first, against a fixed measure; enemies are built back from it. Level 50 is the soft launch: every number here is authored, not derived. Targets only until the hero pass applies them; `sim/yardstick.py` measures today against them (`yardstick_report.md`).

**The measure is the Vasara's hammer.** Damage doesn't roll: a hit is a fixed amount, varied only by a graze (20%, half), a crit (~5%, x1.5) and affinity. A clean Krosh on a plain foe is about **104**. That's the melee standard; magic should land near it.

**Hero pools** (a 50 grid; martial MP is a low floor that talismans can raise: an "Odinseye Effigy" adding 50 MP is the kind of trade a talisman should offer):

| Class | HP | MP | Identity |
|---|---|---|---|
| Vasara | 1000 | 50 | Front tank; pays HP for his moves; no Meditate |
| Ullar | 600 | 50 | Rear sniper; pays HP; MP only for moves he picks up |
| Brennumar | 500 | 150 | Fragile, the deepest pool |
| Dagskald | 700 | 200 | Sturdy enough to stay up; the pool to top up the party |
| Skurmar | 600 | 100 | Sturdier than Brennumar, shallower; knots deepen his Meditate and Djupanda |

**Foe HP by tier**, set by hammer blows, not by doubling (hits-to-kill counts whole hits, so HP sits against multiples of 104):

| Tier | Krosh hits | HP |
|---|---|---|
| Trash | 2; 1 with one ATK stage (139 > 130); 3 on a graze | 130 |
| Regular | 4-5 | 450 |
| Elite | 9-10: "right there next to my tank" | 950 |
| Boss | about 5 rounds of the whole party; longer in practice (adds, heals, buffs) | 1700 |

A Flok-and-talisman build that invested hard (about +2 or +3) sweeps a row of Trash.

**The other side:** a foe's normal hit takes 10-12% of a mid hero's HP (60-72 on 600); a wind-up 30-40% (180-240). A mid hero falls in about 6-8 normal hits; the Vasara is the deliberate tank, about 14. Families are deliberate deviations from the plain foe (the Beinar's DEF, the Ande's MDF, the Djur's bite).

**The plain foe** (the measuring dummy): no affinities, no body quirks, DEF = MDF (CON = WIS = 60), other attributes average.

**Locked (Nov 21):**
- **Pools** as above, except martial MP is **0**. The way in is a talisman (an "Odinseye Effigy": +50 MP, about 16 casts of a 3 and 8 of a 6). Martials don't Meditate, so a spellblade refills only through items and omens. A hero with no MP pool simply doesn't get anything that reads one (one helper for "how much of the pool is missing", which is nothing when there's no pool).
- **Power, as a share of a clean Krosh (104):** martial melee 1.0; ranged 0.75; magic base 0.9 (a weakness hit, 135, one-shots Trash; a neutral one doesn't); Halv 0.5 of its base; a rider x0.6; Mer x1.67 (Mer and a rider land back at 1.0); a row 0.75 a target, an All 0.6 a target.
- **Cost = the rung x 2^steps.** HP ladder: Halv **4**, minor (no damage) **8**, base **16**, then 32, 64, 128. MP ladder: Halv **2**, minor **3**, base **6**, then 12, 24, 48. Steps: a rider +1, Mer +1, Styng +1, Snar +1, Flok +2, All +3; **a knot spent pays one step** (the untie spells). Halv is cheaper per point than base on both sides: the efficient, slow choice.
- **Past the top of the ladder, a move becomes an item.** Allblottskott is the Shrapnel Bomb: found or bought, a pouch slot, fixed power.
- **The last-HP rule:** a move is usable while its cost is at most twice your current HP; paying more than you have drops you (to Dying: a body on the floor, the rows shift, the party's damage falls). At 1 HP even Halv (4) is locked.
- **One ladder per resource; the pools do the weighting.** Ullar pays the Vasara's numbers out of 600 HP; the Skurmar gets fewer casts than Brennumar, the Dagskald more.

## Part 7c: Every Kit Move on the Rules (Nov 21, agreed with Joseph)

**Applied (Nov 21, the hero pass; option B: heroes only, today's foes unchanged until the enemy pass).** Pools, the ladder, power shares and the names are in the engine (`data.py`: HERO_POOLS, KROSH_CLEAN, LAK_CLEAN, CLASS_SHARE, CLASS_TIER, RIDER_SHARE, COST_LADDER, HALV_COST, ROOT_NAMES; each verb's `cost`). Also in: the last-HP rule (the menu shows the cost in red and "LAST SWING"; the AI never spends its last HP) and martial heroes with no MP pool. As built: Styng's added hit is 0.7 of the class's base hit (Genomskott: ~55); an All untie spell takes the All share (0.6). The rider's 0.6 applies to heals too (Joseph, Nov 21): Solak heals 60. Names (Nov 21): Daska is the striking taunt (Egga + Styng); the Blinding one is Rodegga. Skimra (Swedish *skimra*, to shimmer) is Lak + Nimble 3, was Solak; its twin, Strala (to beam: a Dagskald spell that Marks), waits on the dodge question. Rungs given to verbs outside the kits (Joseph: fine as they are): Avliva 16, Skrida 8, Aukskold 8, Skolja 6, Vakna 6, Kasta 6, Svepa 6, Medvind 3, Aukseid 3.

**The ladder** is one list for both resources: 2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64, 96, 128. A step doubles; curation may move a move a **half-step** (x1.5) when its role calls for it, so every price stays on the list. A move's rung comes from its kind (Halv, minor, base); its parts add steps; a knot spent pays one. Past what a hero can pay, it becomes an item.

**Element power**, from the magic base of 0.9: Eld 0.9; Blast 0.9 in two hits (cheaper, less reliable); Blixt **1.0 at 8 MP** (the tiring, spiky one); Sol 0.9; the rest 0.9 until they're designed. Reyk deals no damage of its own (0.6 for Styngreyk's added hit).

**Naming.** The rules build the name; curation renames when a name is long or hard to say (Banskott stays: two syllables that sound good). Two ways, both composing with Mer, Snar, Flok:
- **A rider with its own word**, in front of the root: Brak-rosh, Blot-skott, **Lam**-sveda (Feeble: lame), **Stel**-blixt (Stunned: stiff), **Rod**-egga (Blinded: seeing red). A player can learn the parts: "lam" is Feeble, "stel" is Stun. A rider's word belongs to its verb: Blinded is Blinda on Sol (dazzled) and Rod on Egga (rage).
- **A new word for the whole move**, parts attaching to it: **Daska** (Egga + Styng: Swedish *daska*, to smack: the taunt that strikes; with Rod, Rodaska), **Genomskott** (Naglskott + Styng: a through-shot that Pins), **Genomskoda** (Peka + rider: Swedish *genomskada*, to see through someone). Genom- is a soft family (a later spear class might get a Genomspett).

| Class | Leg | Move | Parts | Cost | Power (clean on the plain foe) | Today |
|---|---|---|---|---|---|---|
| Vasara | 1 | Halvkrosh | Halv | 4 HP | 0.5 (52) | free, 52 |
| Vasara | 1 | Krosh | base | 16 HP | 1.0 (104) | 28 HP, 104 |
| Vasara | 1 | Egga | minor | 8 HP | taunt | 28 HP |
| Vasara | 2 | Brakrosh | rider | 32 HP | 0.6 (62), Sundered | 42 HP, 104 |
| Vasara | 2 | Lya | minor | 8 HP | cover (a later Lonnlya, e.g. Fortified then cover, at 16) | free |
| Vasara | 3 | Snarbrakrosh | Snar, rider | 64 HP | 0.6 (62), first, Sundered | 63 HP, 93 |
| Vasara | 3 | Rodegga | Egga + rider (Rod: blind with rage) | 16 HP | taunt + Blinded | Lonnegga, 42 HP |
| Vasara | 3 | Hevn | base | 16 HP | 1.0, +25% a hit taken | 28 HP |
| Ullar | 1 | Halvskott | Halv | 4 HP | 0.375 (39) | free, 99 |
| Ullar | 1 | Skott | base | 16 HP | 0.75 (78) | 17 HP, 199 |
| Ullar | 1 | Naglskott | minor | 8 HP | Pinned | 17 HP |
| Ullar | 2 | Blotskott | rider | 32 HP | 0.45 (47), Bleeding | 25 HP |
| Ullar | 2 | Peka | minor | 8 HP | Marked | 17 HP |
| Ullar | 3 | Merblotskott | Mer, rider | 64 HP | 0.75 (78), Bleeding | 38 HP, 278 |
| Ullar | 3 | Genomskott | Naglskott + Styng | 16 HP | Pinned + Styng's hit | Styngnaglskott, 25 HP |
| Ullar | 3 | Genomskoda | Peka + rider | 16 HP | Marked + Sundered | Lonnpeka, 25 HP |
| Ullar | 3 | Banskott | base | 16 HP | 0.75, x on the Pinned | 17 HP |
| Brennumar | 1 | Halveld | Halv | 2 MP | 0.45 (47) | free, 124 |
| Brennumar | 1 | Eld | base | 6 MP | 0.9 (94) | 7 MP, 248 |
| Brennumar | 1 | Reyk | minor | 3 MP | Blinded | 7 MP |
| Brennumar | 2 | Sveda | base (it damages, over time) | 6 MP | Scorched | 7 MP |
| Brennumar | 2 | Alleld | All | 48 MP | 0.54 (56) a target: trade his MP for the party's HP | 19 MP |
| Brennumar | 3 | Mereld | Mer | 12 MP | 1.5 (156) | 12 MP, 347 |
| Brennumar | 3 | Lamsveda | Sveda + rider | 12 MP | Scorched + Feeble | Lonnsveda, 12 MP |
| Brennumar | 3 | Djupanda | windfall | free | MP back | free |
| Dagskald | 1 | Halvsol | Halv | 2 MP | 0.45 (47) | free, 75 |
| Dagskald | 1 | Sol | base | 6 MP | 0.9 (94) | 12 MP, 149 |
| Dagskald | 1 | Lak | base, a half-step up | 8 MP | heals ~100 (one Krosh: 1.5 foe hits) | 12 MP |
| Dagskald | 2 | Kvad | base | 6 MP | a Song stack: singing is the efficient heal | 12 MP |
| Dagskald | 3 | Skimra | Lak + rider (the shimmer: was Solak) | 16 MP | heals 60 (the rider's 0.6) + Nimble 3: the panic button | Solak, 19 MP |
| Dagskald | 3 | Merkvad | Mer | 12 MP | +2 stacks | 19 MP |
| Dagskald | 3 | Allaukraft | minor, All | 24 MP | ATK up, everyone | 31 MP |
| Skurmar | 1 | Halvblast | Halv | 2 MP | 0.45 (47) | free, 86 |
| Skurmar | 1 | Blast | base | 6 MP | 0.9 (94), two hits | 7 MP, 172 |
| Skurmar | 1 | Knyta | minor | 3 MP | one knot | 7 MP |
| Skurmar | 2 | Kuling | All, 1 knot | 24 MP | 0.54 (56) a target | 12 MP |
| Skurmar | 2 | Blixt | base, a half-step up | 8 MP | 1.0 (104) | 7 MP |
| Skurmar | 3 | Merknyta | minor, Mer | 6 MP | two knots | 12 MP |
| Skurmar | 3 | Storm | Mer, All, 2 knots | 24 MP | 0.9 (94) a target | 19 MP, 180 |
| Skurmar | 3 | Stelblixt | Blixt + rider | 16 MP | 0.6 (62), Stunned | Lonnblixt, 12 MP, 238 |
| (Skurmar) | - | Orkan | Mer, All, follow, 3 knots | 24 MP | Storm + an All Blixt | - |

Past the ladder: a Flok Stelblixt is 64 MP (out of reach on a 100 pool); an All one (128) and Allblottskott are items (the Shrapnel Bomb).

---

## Part 8: What Comes Next

1. **A mutation session:** for each move, which of Mer, Styng, Lonn and Jatte it accepts, its designated riders, and each class's capstones and their parts.
2. **Stats** tuned to the pace tables (pillars Part 5b).
3. **The refactor:** fixed stat blocks and starting kits; Pinned, Marked, Sundered, Kvad, Egga, Lya, Meditate; weapon moves and rider auras; Kross → Krosh; then dive.py, then the tapestry in the Lab.

## Open Questions

- **Scorch's partner in the slice.** The Skurmar is the fifth class, not in the first four. Give Scorch a second touch inside the four, or let the forge arrive with the Skurmar?
- **The Song's numbers:** the base heal per verse. If it feels thin, raise the base before the cap.
- ~~**Hevn's cap**~~ Decided (Nov 20): +25% an attack, cap +100%; Bidhevn doubles an equally primed Hevn.
- **The Reyk spirits** need rebalancing once Reyk is a no-damage status spell.
- **The numbers everywhere:** ticks, stages, durations, costs: the sim tunes them against the pace tables.
- **The other eight classes:** the same treatment, as they're unlocked; the unlock order and conditions.
