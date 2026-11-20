# Classes (Draft, Nov 20, 2026)

The first four classes, designed the same way: **fantasy → verbs → basic moves → the places mutations act on.** Answers to **pillars.md** (characters, not hires; four move slots, two to start; mutations by grammar).

**Status key.** **Locked** means agreed (the Brennumar, Nov 20). **Draft** means Claude's proposal, for Joseph to react to. New words are marked *coined*; their sources are given so we can check them.

---

## Part 1: The Model (Locked)

- **A class is a fantasy, and the fantasy names its verbs.** Each class has **five or six verbs** (jobs). Two are its **starting kit**; the rest turn up during a run as basic moves (tomes, rewards, weapons), and every one of them can be mutated.
- **Basics are verbs, not elements.** Two roots with every mutation is a big combinatorial space but a thin strategic one: builds differ by *what jobs a hero does*, not by how hard.
- **One signature mechanic per class,** and it **touches at least one other class's** (a designed synergy). Emergent synergies come on top. One per class also caps the cost: each new status is an icon, a line of text, and AI that knows how to value it.
- **One catalog, two routes.** Every move has a value from its parts (the grammar already prices power and cost per part). A rare move you *find* is a pre-mutated one: an Alleld tome is the same move you could grow by carving All onto Eld. Rarity follows value: plain verbs common, two-part moves uncommon, three-part rare.
- **Unlocks by deed:** each class unlocks when you do something that class would value (pillars Part 4).

---

## Part 2: Brennumar (Locked)

*The Tactical Arsonist: burns and vanishes.* Eld school (child: Reyk). Weapon class: Brand. Magical: uses MP, Meditates. **Unlocked from the start.**

| Verb | Job | Basic move | Notes |
|---|---|---|---|
| **Strike** | Fire damage | **Eld** | Starting kit |
| **Blind** | Lower their Accuracy | **Reyk** | Starting kit (smoke) |
| **Burn** | Damage over time | **Sveda**: a weak Eld that leaves **Scorched** | Swedish *sveda*, "to singe, scorch" (ON *svíða*) |
| **Vanish** | Protect your side with smoke | A defensive Reyk: Evasion up for one, a row, or all; plus a strong, expensive single-target "evade everything for one turn" | The "vanishes" half of his fantasy |
| **Cash in** | Pay off a setup | One move that **consumes Scorched** for burst; one that hits **Blinded** targets harder | Closed loops on his own verbs |
| **Stoke** | His own tempo | **Aukseid** (+1 MAT on himself), **Djupanda** | Djupanda: "deep breath" |

**Signature mechanic: Scorched.**
- A fire you feed: **100% of its damage on the first tick, then 50%, then 20%, then out** (an ember).
- **Sveda moves reset it to 100%** (reset, not stack).
- **Hit by wind (Blast), a Scorched target flares back to 100%.** It touches the **Skurmar**: a Brennumar and a Skurmar in the back row become a forge.
- Not poison: poison is a clock (patience); Scorch is a fire you feed (tempo).

**Djupanda** (any magical can learn it): a **wind-up**, using the Bid manner's machinery. Declare it, spend the next turn building ("Djupanda..."), and a large MP windfall lands. **It can be interrupted** (Stun, Frozen, the Drattr's net), so it rewards keeping the caster safe. Mutations: target an ally at a reduced rate, a bigger windfall, a Swift version that's smaller but harder to interrupt.

---

## Part 3: Ullar (Draft)

*The Hunter: pins the prey, and finishes it from afar.* Bowman: kills from range, helpless once a blade reaches him. Weapon: Bow (Pierce, Long). Martial: techniques cost HP. Weak to Slash. **Unlocked from the start.** Name: Ullr, god of the bow, skis and the hunt.

| Verb | Job | Basic move | Notes |
|---|---|---|---|
| **Shoot** | Damage at range | **Skott** | Starting kit |
| **Pin** | Slow it and hold it still | **Naglskott** (inflicts **Pinned**) | Starting kit. Nagl is a rider prefix, like Blot |
| **Volley** | Hit many | **Flokskott** | Exists |
| **Finish** | Pay off a setup | **Banskott** (*coined*: ON *bani*, "death, slayer," + skott): hits **Pinned** targets harder, and harder still below half HP | His cash-in |
| **Glide** | Escape his weakness | **Skrida** (Swedish *skrida*, "to glide"; ON *skríða*, as in the ancient "gliding Finns" on skis): step to the Rear and gain Evasion for a turn | Ullr is the god of skis. Answers "helpless once a blade reaches him" |
| **Steady** | His own tempo | **Aukhitt** (+1 ACC on himself) | Stat grammar: Hitt is ACC |

**Signature mechanic: Pinned** (new status).
- **One Speed stage down for a few rounds, with no Frozen chain** (unlike Chilled).
- **Proposed addition:** a Pinned target **can't dodge, and can't change rows.** That makes Pin "the hunted prey": it can't flee the front, and every hit lands.
- **Touches:** everyone whose moves roll to hit or to land, the **Brennumar** most of all (his Blinds, Scorches and cash-ins land on a target that can't dodge). And the **Vasara's** Taunt: a Pinned enemy can't step out of reach of her hammer.

---

## Part 4: Vasara (Draft)

*The Anvil: takes the blows meant for others, and answers with the hammer.* Shield-hammer: the shield takes cuts and blows; points slip past the rim. Weapon: Hammer (Crush, Short). Martial. Weak to Pierce. **Unlocked from the start.** Name: Finnish *vasara*, "hammer."

| Verb | Job | Basic move | Notes |
|---|---|---|---|
| **Strike** | Crush damage | **Kross** | Starting kit |
| **Taunt** | Draw fire | **Egga** (from ON *eggja*, "to incite": the source of English "egg on") | Starting kit. Acts in the fastest group |
| **Guard** | Take one ally's hits | **Lya** (Cover) | The tank owns Cover (pillars Part 5) |
| **Crack** | Break their armour | **Brakkross** (*coined*: Swedish/ON *brak*, "a crash, a crack," + kross): inflicts **Cracked** | Brak is a rider prefix, like Blot and Nagl |
| **Brace** | Harden the line | **Aukskold** (+1 DEF): herself, then by mutation a row, then all (a shield wall) | Exists in the stat grammar |
| **Answer** | Pay off taking hits | **Hevn** (Norwegian *hevn*, "revenge"; ON *hefnd*): strikes back harder for every hit she took since her last turn | Her cash-in: closes the loop with Egga and Lya |

**Signature mechanic: Cracked** (new status).
- **Each cracking blow lowers the target's DEF one stage, stacking to three.** Distinct from a plain Nedskold: it stacks blow by blow, and it has a partner.
- **Touches the Ullar:** **Pierce finds the cracks.** Pierce hits on a Cracked target deal extra damage (or crit more). The fighter opens the armour; the ranger finishes through it.
- Her Taunt and Answer also touch everyone: the more the enemy hits her, the less it hits the back row, and the harder she answers.

---

## Part 5: Dagskald (Draft)

*The Skald: sings the party whole, and smites with daylight.* Sol school (child: Lak, healing). Weapon class: Instrument (harps, flutes, horns, the Bronze Age *lur*). Magical. **The first unlock.** Name: Swedish *dag*, "day," + skald. Germanic healing magic was sung (*galdr*, from *gala*, "to chant").

| Verb | Job | Basic move | Notes |
|---|---|---|---|
| **Mend** | Heal | **Lak** | Starting kit |
| **Smite** | Daylight damage | **Sol** (a weak Ray) | Starting kit |
| **Sing** | Sustained healing that grows | **Kvad** (Norwegian/Danish *kvad*, "a lay, a poem"; ON *kvæði*): see below | His signature |
| **Cleanse** | Clear statuses | **Skolja** | Exists (Swedish *skölja*, "to rinse") |
| **Wake** | Bring back the Dying | **Vakna** (Swedish *vakna*, "to wake"): revive a Dying ally | |
| **Inspire** | Lift the party | **Aukkraft** (+1 ATK): one ally, then by mutation all (a battle-song) | Stat grammar: Kraft is ATK |

**Signature mechanic: the Song (Kvad).**
- **A held song:** while he keeps singing, the party regenerates HP every round, and **each round he keeps it up adds a verse**, so it grows (one verse, two, three).
- **It ends if he does anything else, or is interrupted** (Stun, Silence, Frozen, the net).
- **Touches the Vasara:** Lya and Egga keep the singer safe, and the longer she protects him, the bigger the song. And **Djupanda**: both are risky, interruptible, "keep me safe" plays, so a party that builds around protecting its back row gets paid twice.
- **Unlock by deed:** finish a leg (or a whole dive) without a healer.

---

## Part 6: How the Four Touch

| Signature | Its partner | What happens |
|---|---|---|
| **Scorched** (Brennumar) | The Skurmar's wind | A wind hit flares the Scorch back to 100%. *(The Skurmar isn't in the first four; in the slice, Scorch's partner is missing: see Open Questions.)* |
| **Pinned** (Ullar) | Everyone; the Brennumar most | A Pinned target can't dodge, so status rolls and cash-ins land |
| **Cracked** (Vasara) | The Ullar | Pierce finds the cracks |
| **Song** (Dagskald) | The Vasara | Her protection grows his song |

Any three of the four make a party with at least one designed synergy.

---

## Open Questions

- **Scorch's partner in the slice.** The Skurmar isn't in the first four. Give Scorch a second touch inside the four (say, the Vasara's hammer on a Scorched target scatters embers onto its row), or accept that the forge arrives with the Skurmar?
- **Pinned's extras:** "can't dodge" and "can't change rows" are proposals. Too strong together?
- **Cracked vs Nedskold:** is a stacking, partnered DEF break different enough from the plain stat line?
- **The Song's numbers:** regen per verse, maximum verses.
- **Hevn's cap:** how much damage "every hit she took" can add.
- **The numbers everywhere:** tick values, stages, durations, costs: the sim tunes them against the pace tables (pillars Part 5b).
- **The other eight classes:** the same treatment, as they're unlocked.
