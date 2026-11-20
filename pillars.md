# Pillars (Nov 20, 2026)

What the game is, and what every other spec answers to. When combat_spec, dive_spec or loop_spec disagree with this, this wins, and the other doc gets fixed.

**Status key.** **Locked** means agreed in alignment (Nov 12 and Nov 20, including the starting three, kits, pace targets, and the upgrade parts and status shapes in Part 5c). **Open** means not yet decided.

---

## Part 1: The Game in One Line (Locked direction; wording tunes)

*A Norse fight-run: speak three runes at the Gate, weave a dive through the places they open, and win weakness-puzzle fights with a party of three whose words grow every run.*

- **It's a roguelike of fights.** SMT's grandchild in the fights (weaknesses, Bonus Rounds, the satisfaction of clearing trash with a strong All-move), Slay the Spire's in the run (a map of choices, a build that grows, a reset at the end).
- **What makes it not a clone:** the move grammar (moves are *spoken* from roots, tiers and manners, and grow by grammar), the board (rows and ranges), a party of three as your character, and the tapestry the dive weaves.

## Part 2: The Pillars (Locked)

1. **The fight is a puzzle you can read.** Weaknesses, intents, rows and range are visible or learnable; winning is reading them well. Trash fights are short (two or three rounds) and a good All-move clears them with a feels-good release.
2. **The words grow, the party is the build.** Each run, your three heroes' moves are mutated, replaced and lent by weapons; the build is what those words become, and how the three heroes' words work together.
3. **The party is the combo engine.** Three heroes are three sources of synergy (one Chills, another's Hrim hits Chilled targets harder). This is the killer app: a single-character deckbuilder can't do it.
4. **The runes choose your puzzle.** The three runes you speak choose the places, so the families and weaknesses you'll face. You draft toward what you know is coming.
5. **The dive is woven.** The map is a tapestry that fills in as you walk; at the end it's the story of your dive, kept in a hall of every dive you've woven.

## Part 3: Why Someone Plays (Locked)

| Timescale | What keeps you playing |
|---|---|
| A fight | The weakness puzzle; the Bonus Round; the All-move that clears the room |
| A run | Routing on the tapestry (is the elite path worth it?), growing your words, the push-on-or-go-home gamble |
| Across runs | Unlocking classes and their talismans; new tomes, Omens and places in the pool; harder dives; the hall of tapestries |

## Part 4: Characters, Not Hires (Locked)

- **Your "character" is a party of three heroes,** chosen at the Gate from the classes you've unlocked. The classes are the characters: no proper names needed.
- **Fixed power.** No levelling. Each class has hand-tuned stats at one power level (somewhere around level 10 to 20; the sim settles it), and enemies are tuned against that. Stats are shown read-only, so you can see the Berserker isn't the Brennumar.
- **Unlocks:** start with **three classes**, the classic trio: **Vasara** (the fighter: a shield-hammer tank), **Ullar** (the ranger: the bridge), **Brennumar** (the wizard: the introduction to magic). **The Dagskald is the first unlock:** players who've dived without a healer feel exactly what it gives. More classes unlock by doing things.
- **No duplicates:** each class is an individual; a party is three different classes. (Later, maybe: a class's alternate focus, such as a glass-cannon Brennumar; class talismans already cover much of this.)
- **People persist, words reset.** What a run gives (moves, weapons, talismans, Omens, the pouch) ends with the run. What persists is the meta: unlocked classes, unlocked talismans, the pool, the bestiary, the tapestries.
- **The Company stays, as the meta hub:** where you unlock classes and talismans, store each class's state and customisation, and hang the tapestries. Not hiring, wages or debt (see Part 10).

## Part 5: Moves (Locked)

- **Four move slots per hero.** A class **starts with two** (a Dagskald: a weak Ray and a weak Heal), leaving room to grow.
- **Universal actions take no slot, and are named in plain English** (they're UI verbs): Defend, **Meditate** (a nominal MP recovery, free; **magicals only**: martial techniques cost HP, so martials lean on magicals and items), items, moving rows, Flee.
- **The tongue is for what you learn, carve or carry.** Moves are spoken in it (Eld, Naglskott, Egga). A stronger Meditate a magical can learn is ***Djupanda*** ("deep breath").
- **Learning a fifth move means forgetting one.** One screen for it, shared by tomes and weapons.
- **Mutations** change a move by grammar: a tier (Halv, base, Mer, Jatte), a target (one, row, all), a manner (Snar: Swift; Tung: Heavy; Bid: Patient; Jarf: Reckless; Drif: the flurry), a rider (a status). Three starting Elds can grow apart: one into Alleld, one into a Swift Eld, one into an Eld that burns.
- **The upgrade parts, the cap, capstones and the status shapes** are in Part 5c.
- **Mutations are forks, by default.** Balance first: a step up costs something (MP, a wind-up, acting last), and a free version is weaker (Halveld). But the rule bends on purpose: feels-good where it can, feels-bad where it must, and a few deliberately spiky ("pear-shaped") combos for players to find.
- **Tomes are locked by weapon and school,** not by class name: a Spett tome says "stabbing weapons"; a Gro tome says "the Jord school". New classes slot in without rewriting tomes.

### Starting kits (the first three)

| Class | Weapon | Move 1 | Move 2 |
|---|---|---|---|
| Vasara | Hammer (Crush, Short) | **Krosh** (a hammer blow; renamed from Kross) | **Egga** (Taunt: draws fire). English "egg on" is from Old Norse *eggja*, "to incite" |
| Ullar | Bow (Pierce, Long) | **Skott** (a shot) | **Naglskott** (a pinning shot: inflicts Pinned) |
| Brennumar | (school: Eld) | **Eld** (single-target fire) | **Reyk** (smoke: lowers Accuracy) |

- **Nagl** is a **rider prefix**, like Blot (Blotskar: may Bleed): Nagl + a root may Pin. Naglskott, Naglspett (a thrust that pins). It's a mutation you can carve. (*Nagl*: Old Norse for a fingernail, as in Naglfar; *nagli*, a metal nail.)
- **Pinned** is a new status: **slowed and rooted** (one Speed stage down for a few rounds, and it can't change rows), **with no Frozen chain** (unlike Hrim's Chilled). Nagl is a prefix any stabbing weapon can carry.
- **Cover belongs to the tank:** **Lya** ("I am guarding you": it takes everything aimed at one ally). An Ullar who steps to the front doesn't gain it. **Holding the line stays positional:** short-range attacks only reach the front row, so anyone standing in front shields the rear from them until they fall (Medium attacks from the enemy front, Long attacks and spells still reach the rear).

### Naming rule
**Words must be easy for English speakers to say, remember and share.** Prefer simple coinages (Lya, Egga, Nagl) over faithful forms with hard clusters (*hlíf*, *hr-*, *þ*). The quarry inspires; it doesn't dictate spelling.

**The seam rule:** where a prefix ends with the letter the root begins with, the doubled letter collapses: Brak + Krosh = **Brakrosh**, Auk + Kraft = **Aukraft**. Prefixes keep one spelling: **Blot, Flok** (one letter each).

## Part 5b: Power and Pace (Locked targets; the sim tunes)

Power is set by **how long fights last**, not by a level: tune stats until these hold.

| Enemy tier | Hits from the party to kill one | With all three attacking | Hits it needs to kill one hero | What the fight should cost, played well |
|---|---|---|---|---|
| Trash | 3 | One round per unit (an All-move makes a pack 1-2 rounds) | 6-7 | ~10-15% of the party's HP, a little MP |
| Regular | 6+ | 2 rounds | 5 | ~20-25% |
| Elite | 12+ | 4 rounds (~5-6 with tactical turns) | 4 | ~40-50%, maybe an item |
| Boss | 18+ | 6 rounds (~8-9 with tactical turns) | 3 | Most of what you have; it kills if you misplay |

- **The dive is the opponent,** not any one fight: HP carries room to room, so trash exists to tax you.
- **Enemy levers on top:** tactical moves (heals, stat changes), retinues and adds that a boss can replenish, Bonus Rounds, extra actions.
- **Camps sustain:** a party without a healer must be able to reach the end. **Challenge and gatekeep (checks for proper play), never forbid by difficulty.**

## Part 5c: Upgrades, Statuses and What They Answer (Locked Nov 20, except where marked)

### The upgrade parts
| Part | What it does | Where it comes from |
|---|---|---|
| **Tier: Halv, base, Mer, Jatte, Ur** | One ladder everywhere: **Mer** is more (a bigger hit, a deeper stage, a longer Pin, an extra verse); **Jatte** is the next rung | Mer is carved. **Jatte is rare: found, not carved.** **Ur is gear-only** (weapons, talismans) |
| **Styng** | Adds damage (to a status move, it adds a hit: Styngnaglskott) | Carved |
| **Lonn** | The upgrade path that **adds the move's designated rider** (a status, or a single stat stage) | Carved. Named by the rider's own prefix (Skott + Bleeding = **Blotskott**); a rider with no prefix (a stat stage) keeps Lonn in the name (Lonnpeka, Lonnegga) |
| **Target, manner** | One/row/all (Flok, All); Snar, Tung, Bid, Jarf, Drif (Part 5) | Carved, found, or bestowed |

- **A move is its built-in effect plus one rider slot.** Lonn fills it; a rider weapon fills it only if it's empty (Part 6).
- **A Lonn rider never duplicates a sibling verb's whole job** (Lonnlak cleanses one status; Skolja is the Cleanse verb).
- **Every move has designated riders.** Lonn offers only those. A move with no sensible one has no Lonn branch (Eld has no Styngeld).

### The cap and capstones
- **A move carries at most two upgrade parts.** Within the cap, a move keeps its **spoken name** (Merblotskott, Flokblotskott): the grammar is the joy, so it stays readable.
- **A rider's spoken part belongs to the verb, not the status** (Nov 20): Sundered is Brak on Krosh (Brakrosh) and Lonn on Peka (Lonnpeka); Blinded is Blinda on Sol (Blindasol) and Lonn on Egga (Lonnegga). Lonn shows only where the rider has no part of its own.
- **Styng adds 70% of the tier's power** to a move with no damage of its own; **Lonn never weakens a hit** (its price is the cost).
- **Bynames:** a move within the cap whose spoken name runs past 15 letters gets a name of its own (Merstyngnaglskott is **Geirskott**). Once the mutation session sets which parts each verb accepts, every reachable long name needs one.
- **Capstones are the named peaks beyond the cap:** rare, found rather than carved, one or a few per class (Tusensplitter, Pilskur, Hasin, Holm, Skogsbrand: classes.md). Naming is only combining legal parts and naming the result for effect.

### The noticeable-change rule
- **A part is offered only if it changes play in a way the player notices.** (Magic: the Gathering's lesson: if nobody notices, it's a dud.) Duration counts for control effects (a longer Pin is noticed; a part with nothing to notice is shelved, as Merpeka was until Marked became a counter).

### The reward mix
- **Each choose-one-of-three mixes kinds,** in the spirit of Magic's draft order (BREAD: bombs, removal, evasion, aggression; then duds): not three of the same, rarely a dud, and **often one build-around** (a part or move that pays off a signature the party already has).

### Two status shapes
Players learn two shapes, once, and every status uses one:

| Shape | Rule | Uses it |
|---|---|---|
| **Build** | Each application adds a stack (Mer adds two), **cap three**; **loses one at the end of each round it isn't refreshed** | Blinded (Reyk), Sundered (struck), Kvad (sung) |
| **Fade** | **100%, then 50%, then 20%, then out;** its feeder can reset it | Scorched (damage per tick; Sveda resets it) |

**A named debuff is a stat-stage aura.** Blinded *N* means *N* ACC stages down; Sundered *N*, *N* DEF stages down. The move confers the status; the status confers the stages. "Reyk, Reyk, Reyk" is Blinded 3 (-3 ACC); Mereyk adds two at once.

**One counter per stat, from −3 to +3; up and down cancel** (as in Pokémon and SMT). A target shows one badge per stat: Feeble 3 plus an Aukraft is Feeble 2; a Meraukraft on Feeble 1 is Mighty 1. The counter moves one step toward zero at the end of each round nobody pushed it.

| Stat | Down | Up |
|---|---|---|
| ATK | **Feeble** | **Mighty** |
| DEF | **Sundered** | **Fortified** |
| ACC | **Blinded** | **Keen** |
| EVA | **Marked** | **Nimble** |
| SPD | **Slowed** | **Quick** |

**Cleansing lifts lowered stats to neutral** and leaves raised ones alone (Skolja: every harmful status and every lowered stat; Lonnlak: one of them). So a Feeble 3 hero can be fixed two ways: Aukraft steps it up (and can overshoot into Mighty), Skolja resets it to zero.

**Marked is the EVA-down counter** (Marked *N* = *N* EVA stages down), not a yes/no "can't dodge". In the engine, Marked 2 already removes grazes and Marked 3 adds crits, so "can't dodge" is what Marked 2 does. Merpeka (+2) has something to notice, so it's off the shelf.

**One stat, one named status:** ACC down is only ever **Blinded**; DEF down is only ever **Sundered** (*sunder*, ON *sundr*, "apart"; renamed from Cracked); ATK down is only ever **Feeble** (not "Weakened": in a weakness game, "Weak" already means an affinity). The stat grammar names the moves, the statuses are what you wear: Nedhitt confers Blinded, Nedskold Sundered, Nedkraft Feeble. Riders that lower those stats confer the status (Lonnegga: Blinded; Lonnpeka: Sundered). 

**A counter is its own stacks plus its sources.** Statuses that do something else as well add to a stat's counter while they last: Pinned (+1 Slowed, and rooted) and Chilled (+1 Slowed, and toward Frozen). Direct stacks decay as usual; a source's stack lasts as long as its source. The total caps at 3 and cancels with the opposite as usual. **The badge shows the total; hover lists the sources** ("Slowed 2: Pinned 1, Chilled 1"). Pinned and Chilled keep their own badges, since each answers a different question (can it move? is it near Frozen?).

**Frozen uses the fade shape** (Joseph, Nov 20): **its next action is lost for sure; the one after is lost on a 50% roll; the one after that on 20%; then it thaws.** A failed roll means it thaws and acts.
- **Counted in actions, not rounds,** like Bound, so a freeze landed after the target has acted still costs it a turn.
- **No refreeze while Frozen** (unlike Scorch's reset), or two ice users lock a target forever. Fire you feed; ice you can't. (A dedicated move that extends Frozen: shelved.)
- **Shatter stays:** any hit breaks Frozen for 1.5× damage (as now). So the choice is hold them, or cash them in.
- **The icon shows the odds** (100 / 50 / 20): the readable puzzle (Part 2).

**Bosses are immune to turn-enders** (Frozen, Stunned, Bound) for now; weaknesses already earn the Bonus Round. Revisit if bosses turn out overpowered.

### Keywords on the screen
- **Speed-group keywords** (combat_spec Part 3), printed on move cards in the keyword colour:

| Group | Keyword | Who |
|---|---|---|
| +3 | **First** | Defend, Lya, Egga: "acts before nearly every other move" |
| +2 | (none) | Rare authored exceptions |
| +1 | **Swift** | Snar moves, Move, Swap |
| 0 | (none) | Normal |
| −1 | **Late** *(proposed; not "Slow", which collides with Slowed)* | Slow moves; anyone Feared |
| −2 | **Heavy** | Tung moves (already Tung's English name) |
| −3 | **Last** | Authored exceptions |

- **A move's manners set its group, and they combine:** Bid alone releases at 0; Bid + Tung (a meteor: Bidtungeld) winds up, then releases Heavy at −2. A wind-up breaks only to turn-enders (Stunned, Frozen, Bound) and death, not to ordinary hits.
- **Move text names its statuses, and each name is hoverable** for its definition ("Apply Scorched and Feeble."), as Slay the Spire and Magic do with keywords. The definition lives once, in the glossary, not in every move.

### Enemies the signatures answer
- **The places field the problems the signatures solve:** evasive things for Marked; armoured things for Sundered; things that shift rows or flee for Pinned; packs for Scorch and the All-moves; long fights for Kvad. The runes then tell you which answers to draft toward (Pillar 4).

## Part 6: Weapons (Locked)

- **A weapon has two halves:**
  - **Its family** sets damage type and range, and never changes: a Bow is always Pierce, Long. Ranges are Short, Medium and Long.
  - **Its skin** (Warbow, Repeating Crossbow, Trapper's Bow) carries stats (+ATK) and, sometimes, a move.
- **A weapon's move belongs to the weapon.** Equipping a Repeating Crossbow opens the forget/learn screen ("choose a move to replace with Drifskott"), or fills an empty slot. Swap it for a stronger, move-less Warbow and Drifskott leaves with it: you've traded a move for the Warbow's ATK, and left a hole to patch with a tome. That's the trade-off.
- **Tomes teach a move for the run; weapons lend one while you carry them.**
- **Rider weapons (rarer):** a weapon may add a rider to **attacks that have no rider**, and nothing else: the Eitr Greatsword says "adds Poison to attacks with no status effect". A Freezing move keeps its Freeze and gains nothing. Weapons never touch tier, target or manner.
- **Basic starting weapons** (Bow, Stikk...) grant no move.
- **Everything resets** with the run.

## Part 7: Talismans and Omens (Locked)

- **Talisman:** what **one hero** carries. **One per hero.** Class talismans are unlocked in the Company; some reshape a class's starting kit (Hades' "aspects": a Brennumar talisman that swaps his starting Eld and Reyk for a different build).
- **Omen:** the **party's** luck, good or bad, party-wide. Rule-bending effects in the spirit of Slay the Spire's relics ("the first spell each fight is free", "Bonus Rounds restore MP"). In the lore: the party's *hamingja*.
- **Where Omens come from:**
  - **Elites: one Omen.** The reason to take the elite path.
  - **Bosses: choose one of three.**
  - **Events: sometimes,** often with a cost (a cursed Omen is a good event).
  - **The merchant: one or two,** at a high price.
  - **Not from regular fights.**

## Part 8: Rewards and What They Cost (Locked)

No new currency: the three channels each cost something different.

| Where | What you get | What it costs |
|---|---|---|
| After a fight | Choose one of three: a tome, a mutation, or marks. **The three are mixed by kind** (Part 5c) | Nothing: you earned it |
| Elite / boss | An Omen (a boss: choose one of three) | The fight |
| Rest | **Rest** (heal) **or Carve** (carve one mutation into a move) | The rest itself: carving means not healing |
| Merchant | Tomes, mutations, weapons, talismans, an Omen or two | Marks |
| Event bestowers | A piece of grammar spoken into a move (a swift stranger grants Snar; a berserker grants Drif) | Something odd: HP, a curse, a wound |

## Part 9: The Pouch (Locked for v1)

- **One shared pouch, three slots:** each hero contributes one. **No stacking** in v1. Every Life draught is precious.
- **No armor in v1.** Later, perhaps: armor that changes affinities ("resists Vatn, weak to Crush"), a bet on the route the runes chose. Weapons first.

## Part 10: The Words (Locked)

| Word | Means |
|---|---|
| **Runes** | Words. The Gate's place keys, and the mutations you **carve** into moves at rest |
| **Talisman** | What one hero carries |
| **Omen** | The party's luck, good or bad (*hamingja* in the lore) |
| **Tome** | Teaches a move for the run |
| **Lots** | How events are cast (*hlutr*: a lot, a thing, an amulet) |
| **Egga, Lya, Nagl** | Taunt, Cover, the Pin prefix (Part 5) |
| **Pinned** | Slowed and rooted: one Speed stage down, can't change rows, no Frozen chain |
| **Marked** | EVA down by stage; Marked 2 is "can't dodge" (anyone's hits benefit) |
| **Mighty, Fortified, Keen, Nimble** | ATK, DEF, ACC, EVA up by stage; one counter per stat with the downs (Part 5c) |
| **Blinded, Sundered, Feeble** | ACC, DEF, ATK down by stage, the build shape (Part 5c) |
| **Scorched** | A fire you feed: 100, 50, 20, out (Part 5c) |
| **Mer, Jatte, Ur** | The tier ladder: more, the next rung (found), the gear-only top (Part 5c) |
| **Styng** | Adds damage (Part 5c) |
| **Lonn** | The upgrade path that adds a move's designated rider (Part 5c) |

Candidate lore words, unused for now: *taufr* (a charm, sorcery), *gripr* / *dýrgripr* (a treasure, an heirloom).

## Part 11: What This Changes Elsewhere

- **loop_spec.md:** the city's economy (the Diver's licence on credit, wages, debt, the Register of hirelings, the seven-tick day) is **set aside**, not deleted: it's a second game before the first is fun. The Company remains as the meta hub. Contracts, rumours and the Gate's runes remain useful as unlock and event material.
- **dive_spec.md:** updated the same day (Nov 20): seven-column legs, elites in the journey, a boss per place, the camp before the boss, Omens and the reward channels.
- **combat_spec.md:** heroes leave levelling for fixed stats; four slots plus universal actions; Meditate is new; weapon moves and rider auras are new.
- **The sim:** classes get fixed stat blocks and starting kits; the move compiler gains mutations, weapon moves and rider auras; dive.py carries the run.

## Part 12: What It Isn't (Locked)

- **Not a monster collector.** You don't recruit enemies.
- **Not a city manager** (for now). No wages, debt or hiring.
- **Not an RPG that levels.** Power comes from words, weapons, talismans and Omens within a run.
- **Not a card battler.** Fights are a JRPG menu: every move in your four slots is available, limited by MP and HP. No hand, no draw.

## Open Questions

- **The power level:** the sim finds the stats that meet Part 5b's tables.
- **The unlock order** after the Dagskald.
- **The mutation list and costs:** per move, which of Mer, Styng, Lonn and Jatte it accepts and its designated riders; per class, the capstones (the mutation session, classes.md Part 7).
- **The other stats under the one-stat rule** (MAT, MDF, SPD): named when a class first needs one. SPD is now Slowed/Quick.
- **Starting kits** for the other nine classes (the first three are in Part 5).
- **Meditate's number** (how much MP), and whether martials use it too.
