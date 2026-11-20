# Combat Spec v1

The build-to for the vertical slice's fights. It sits beside **spellbook.md** (what's possible through magic and skills) and **bestiary.md** (the bodies that deliver it). Where this spec and the spellbook disagree, **this spec wins**; the spellbook's Part 4 turn structure is replaced by Part 2 below.

**Status key.** **Locked** means agreed in alignment. **Proposed** means a default chosen to make the spec buildable; it holds until playtesting says otherwise. Numbers marked *(tune)* are starting values for the sim.

---

## Part 1: The Shape of a Fight

- **Three heroes against an enemy pack.** Packs fill a slot budget, 6 by default (bestiary Part 1). Cost = slots = actions per round.
- **Each side stands on a fixed 3×2 board:** a Front row and a Rear row of three spots each.
- **A fight ends** when one side has no one standing. A party wipe is a loss; what a loss costs the Company belongs to the campaign layer, not this spec.
- **Nothing is hidden about the order of a round:** every unit's intent and the turn order are on screen before anything resolves. Enemy affinities are hidden until discovered.

---

## Part 2: The Round (Locked)

1. **Intents.** Every enemy declares its action and target. Each shows as an icon plus a short reason phrase over the enemy ("Engulf → Seidar: she's alone in the Front").
2. **Orders.** The player gives each hero an action and target, with the intents and the turn-order bar in view.
3. **Resolve.** Actions resolve by **speed group**, highest first (Part 3). Within a group, everyone's first actions go before anyone's second (cost 2 and 3 units), then higher SPD, then a coin flip. **Each unit's coin is flipped once, when the round is planned** (Nov 8), so the turn-order bar shows the order that will actually happen. The order is re-ranked after every action, so a unit that is Feared or Chilled mid-round moves. (Flipping once changed party wins by about a point in 4,500 fights: noise.)
4. **Bonus Round.** Everyone who hit a **Weak!** this round, on either side, gets one more action in a Bonus Round (spellbook Part 4): no chaining, and crits don't earn one. Hitting a Null or an Absorb bars you from it, and an Absorb gives the target an entry. It uses the same speed groups.
5. **End of round.** Durations tick (numbered rounds only), Poison ticks at the start of the next round, Defend and Cover lapse.

---

## Part 3: Speed Groups (Locked)

| Group | Who acts here | Notes |
|---|---|---|
| **+3** | **Protection only:** Defend, Cover, Taunt | Immune to Fear. Protection is always in place before anyone swings. |
| **+2** | Rare ultra-priority moves | Authored exceptions (a boss's opener, a Hunt Horn blast). |
| **+1** | Priority moves, including **Move and Swap**, and every **Snar-** move | A fast retreat beats a normal-speed attack. |
| **0** | Normal: attacks, spells, items, Flee; **Bid-** releases | Almost everything. A Bid- move winds up in its own round; the next round the user is locked and the move fires here. |
| **−1** | Slow moves; **anyone Feared** | Fear pushes a unit's actions down to −1, unless they're already lower. |
| **−2** | Heavy moves: every **Tung-** move | Wind-ups and big telegraphed strikes. |
| **−3** | Dead last | Authored exceptions. |

- **SPD only compares within a group.** A slow Defend still beats the fastest attack.
- **Statuses act on groups:** Fear drops an action to −1 (+3 protection is immune). Stunned and Frozen act as the spellbook says (lose the action or can't act). Chilled lowers SPD within the group.
- **SPD still matters on the roll:** every 25% faster than the target shifts the Graze/Hit/Crit roll one stage, capped at ±2 (spellbook Part 9).

---

## Part 4: Information (Locked)

- **Intent:** an icon for the action type (strike, spell, status, protect, move, item, flee) plus a short reason phrase. The phrase is a dev tool first; later it becomes barks in the unit's voice.
- **Turn-order bar:** the round's resolution order, grouped by speed group, updated live when something re-ranks (a unit is Feared, Chilled, or killed).
- **Affinities are hidden until discovered.** The first time an element or damage type hits an enemy kind, its result (Weak, Resist, Null, Absorb) is shown and remembered for that kind. *(Proposed:* discovery persists across fights, per enemy kind, in the Company's bestiary.*)*
- **HP:** heroes show numbers. *(Proposed:* enemies show a bar without numbers.*)*

---

## Part 5: The Board (Locked)

- **Six discrete spots per side:** three lanes × (Front, Rear). Each unit occupies one spot. Spots stay where they are: when a row empties, nothing slides forward.
- **On screen,** each spot is one floor slab. The slabs are always there; the UI only lights them when it matters (a Move preview, a target).
- **Footprint is separate from cost.** Every unit takes one spot by default, whatever it costs. Long bodies (a serpent, a living island) are a future authored trait.
- **Placement at the start of a fight:** heroes stand where the party's formation puts them. Enemies are placed by the composer: Front-liners (Mogel) fill the Front, casters (Ande) the Rear, and the Front is never empty while the Rear holds someone (bestiary Part 9).

---

## Part 6: Reach and Targeting (Locked)

### Reach

| Attack | From your Front | From your Rear |
|---|---|---|
| **Melee** (Slash, Crush) | Enemy Front, full damage | Enemy Front, **50%** |
| **Reach** (Pierce) | Enemy Front and Rear, full | Enemy Front, full |
| **Ranged** (spells, the Skott family) | Anywhere, full | Anywhere, full |

- **Protection:** while anyone stands in a side's Front row, its Rear can't be targeted by melee.
- **Exposure:** if a side's Front row is empty, its Rear counts as its Front for targeting. The front falls, the casters are exposed, and someone has to step up.

### Shapes

**Every basic attack hits one target.** Damage types differ by reach (above) and by what they hunt (the martial triangle, bestiary Part 2), not by shape. **Shapes belong to skills:**

| Shape | Who carries it | Damage per target *(tune)* |
|---|---|---|
| **One target** | Every basic attack, every damage type | ×1.0 |
| **Row** | **Flok-** skills: Flokskar (the cleave), Flokskott (the volley) | ×0.75 |
| **Column** (the target and the spot behind it) | **Udd**, a spear special (held) | ×0.85 |
| **Anywhere** | The **Skott** line (bows) | ×1.0 |
| **All-** (the whole side) | Spells; Allskott (reserved); the Mogel's Splatter (everyone in reach) | ×0.75 |

Names follow the martial grammar (spellbook Part 2): Skar, Kross, Spett, Skott, with the same tiers and prefixes as spells.

- **Spells ignore rows and protection.** That's why casters live in the Rear but are never fully safe there.
- **Lanes are mostly cosmetic.** Only column skills (and Cover's choice of ally) care which lane you're in.
- **Row spells don't exist yet.** If they come, they take **Flok-**, like the martial row skills.

### Retargeting

- **If a target is gone when the action resolves** (dead, or moved out of reach), the action **retargets within the same row**. If that row is empty or out of reach, it goes to the nearest legal row.
- **If nothing is legal, the action fizzles.** *(Proposed:* a fizzled action costs nothing.*)*

---

## Part 7: Move and Swap (Locked)

- **Move** to an empty spot on your side, or **Swap** with an ally (contextual: choosing an occupied spot swaps). **Only the mover spends the action.**
- **Speed group +1:** a fast retreat beats normal-speed attacks, but priority moves and faster enemies can still catch you.
- **Statuses apply normally:** Feared drops it to −1, Stunned can lose it, Frozen can't move, Chilled is slower within the group.
- **Enemies Advance.** When an enemy side's Front empties, enemy scripts step Rear units forward, and the intent shows it.

---

## Part 8: Protection (Locked, names pending)

| Action | Group | Effect |
|---|---|---|
| **Defend** | +3 | Halves damage taken until the end of the round. |
| **Cover** (candidate name *Skydd*, Swedish "protection") | +3 | Choose one ally. Until the end of the round, **single-target** hits aimed at that ally strike you instead. Rows, columns, and All- still hit everyone. |
| **Taunt** (candidate name *Eggja*, ON "to incite"; the root of English "egg on") | +3 | Re-points every enemy single-target intent that can legally reach you onto you, for this round. The intents update on screen. |

- **Animation:** Defend goes straight to the guard pose. Taunt plays the yell (arms up, eyes open), then settles into the guard. Cover runs to the ally's lane, then guards.
- **A covering unit takes the hit at full damage** (Locked). Cover and Defend are separate actions; only a unit with two actions can do both.
- **Cover runs into the ally's spot,** so the hit's reach is checked against the ally, not the coverer: a front-liner covering from the Rear still takes a melee blow aimed at a Front ally.
- **A wind-up is answered here.** A hero's Bid tracks its target, so the enemy's answers are Defend, Cover, Swap the target out (a melee Bid re-checks reach when it fires, then retargets by the normal rules), or breaking the bider. Enemy wind-ups are Mark-bids aimed at a spot, so the player's answer is to get out of it, or put a Defending tank in it.

---

## Part 9: The Skott Family (Locked name; numbers tune)

**Skott** (Swedish "shot") is a single-target, full-range martial attack for archer and thrower types: the one weapon move that reaches the enemy Rear from your own Rear.

| Move | Tier | Notes |
|---|---|---|
| Halvskott | Halv | Free |
| Skott | Base | HP cost, like every martial skill |
| Merskott | Mer | |
| Jatteskott | Jätte | |
| Urskott | Ur | Bow gear only |

- Speed group 0. A −1 group is held in reserve as a knob if Rear archers dominate.
- Damage type is Pierce, single-target (it doesn't continue down the column).

---

## Part 10: Dying, Wounded, Dead (Locked Nov 8; numbers tune)

Heroes only; enemies fall by their own folklore (bestiary).

| State | How you get there | What gets you out |
|---|---|---|
| **Up** | — | — |
| **Dying** | HP hits 0 | A **Surgeon's Kit** or Halvakna or Vakna: Up, no Wound. The fight ends with you Dying: **stabilised at 1 HP, Wounded**. The last breath goes: **Dead**. |
| **Wounded** | Being stabilised, or raised from the Dead | **Rest** (a rest room's Rest, or a night's rest in the city). Falling while Wounded: **Dead** at once. |
| **Dead** | The last breath, or falling while Wounded | The **Mead of Waking** or Mervakna and up: Up at low HP, Wounded. Otherwise, the city (loop_spec Part 8). |

- **Breaths.** A Dying hero has **5 breaths**, shown as pips. One goes at the end of each round (not the round they fell in), and one with each hit they take. They can't act; allies can reach them.
- **Finishing blows are a choice, and you see it coming.** An enemy may spend its action on a Dying hero; it shows as an intent ("The Draugr turns on fallen Vasara"), and the AI weighs it by the breaths left, so it chases kills rather than chipping. Area attacks pass over the fallen. Reach is as for anyone: the Front, or the Rear once the Front is empty.
- **Wounded** cuts max HP and MP by 25% until rested, so you feel it even at full. Scars wait for the campaign layer.
- **A fallen body doesn't protect.** A Dying or Dead hero in the Front leaves the Front empty for protection and exposure, and blocks no one's movement. When they stand, they take their own spot if it's free, or the nearest free one.
- **Between fights**, where you choose the next room, you can use items and spells (heal, revive) from the party menu.

### Revive: the Vakna Ladder

| Spell | Reaches | Stands up at | Wounded |
|---|---|---|---|
| Halvakna | the Dying | 1 HP | No |
| Vakna | the Dying | 1 HP + 20% of max | No |
| Mervakna | the Dead | 1 HP | Yes |
| Jattevakna | the Dead | 1 HP + 20% of max | Yes |
| Urvakna | the Dead | full | No (gear only) |

Revive spells cost MP like their tier (Halvakna as Halvlak, 4 MP: healing is never free); a revived hero acts from the next round. The **Surgeon's Kit** works as Halvakna, the **Mead of Waking** as Mervakna.

**Sim (Nov 8, Barrow packs, no revives in the party):** the Dying rules cost the enemy tempo (finishing blows) and move win rates by 0–5 points. But about half of all falls end in death when no one carries a revive, and a full pouch (a Kit, two Life Draughts, three Firecrackers) is worth 20–26 points of win rate in a single fight. See the note on dive difficulty in Part 15.

---

## Part 11: Items (Locked list, Proposed numbers)

Using an item costs the hero's action, in speed group 0, from that hero's own **Pouch** (3 slots; loop_spec Parts 10–11 have the full list, stacks, and prices). An item is a move with a fixed power rather than a stat, so anyone can use one.

| Item | Effect *(tune)* |
|---|---|
| Small Life Draught, Life Draught, Strong Life Draught | Restores HP (a Halv, base, and Mer heal) |
| Spirit Draught (Small, plain, Strong) | Restores MP |
| Mead of Waking | As Halvakna |
| Antidote, Bandage | Cures Poisoned, Bleeding |
| Pocket Sand, Blinding Powder | ACC down one stage: one target, a row |
| Firecracker, Thunderpot, Great Thunderpot | Affinity-free damage: one target, all, all |
| Throwing Knife, Axe, Hammer | Pierce, Slash, Crush at one target, by metal tier |
| Smoke Pot | Leave the fight for certain (not the Hunt's Tiers 3 and 4) |
| Caltrops, Rán's Net | Paint a spot; a chance to Stun (later) |

---

## Part 12: Flee (Locked)

- **Flee** is an action in speed group 0. The chance depends on the party's SPD against the enemies' *(proposed:* 50% at even SPD, ±10% per 25% faster or slower, capped 10–90%*)*.
- **You can't flee Hunt Tiers 3 and 4** (the Oskorei).

---

## Part 13: Enemies (Locked)

### Scripted Patterns

Enemies follow short scripts per family and rank (the sim's scoring AI is the stand-in), always shown through intents. Telegraphed big moves use a wind-up the player can read: the Mogel's breathe-in stretch, a −2 heavy group.

### Folklore Rules

Each family breaks one rule, so each teaches one lesson.

| Family | Rule | The lesson |
|---|---|---|
| **Draugr** | Rise again unless burned (Eld) or beheaded (a Slash kill) | Finish them properly |
| **Bein** | Reassemble unless Crushed | Bring a hammer |
| **Drattr** | Submerge (untargetable for a round) | Time your strikes |
| **Djur** | Flee when their leader falls | Kill the alpha |
| **Mogel** | Shrink a size on death until the Halvmogel dies; Slash cuts them, Pierce passes through | Use an edge, not a point |
| **Oskorei** | Hunt Horn: +1 ACC while a horn-bearer lives | Silence the horn |

The Mogel rule is in the sim; the others are design, not yet simulated.

### The Composer

Procedural packs come from the encounter composer (bestiary Part 9): gates (biome, family, rank, art only), a cost roll that only offers faces that still fit, toggle rules, and placement by role.

---

## Part 14: Layered Introduction (Locked)

The slice teaches one system per fight, in this order *(proposed sequence)*:

1. **Hit things:** a lone Mogel; the basic Halv attack and Spell only.
2. **Weakness:** a single-element pack; the first Weak! and the first Bonus Round.
3. **The board:** Ande in the Rear behind a Mogel Front; reach and exposure.
4. **Protection:** a big telegraphed hit (the breathe-in); Defend, then Cover.
5. **Moving:** a Front that will crumble; Move and Swap.
6. **Everything:** composer packs from a rolled biome.

---

## Part 15: The Slice

- **Heroes:** three wizards standing in for every class (side sprite: idle, hit, spell, run, charge, bomb, cast, defend, defend-hit, taunt, downed).
- **Enemies:** the Ande and the Mogel, drawn ranks only (Halv, Litel, base), from the composer.
- **Rooms:** the Neutral, Vatn, and Eld dungeon looks (area stone, dressing, light pools), each with its rune on the text box.
- **UI:** the bevelled text box, the turn-order bar, intents, the board slabs lit for Move and targeting.

### Sim status

| In the sim | Not yet |
|---|---|
| Affinities, Bonus Round, Graze/Hit/Crit, speed shift, statuses, riders, healing, multi-action order, family bodies, the Mogel chain, the composer, **speed groups** (Defend at +3, Fear to −1), **the board** (formation, reach, protection, exposure, Advance, shapes for skills), **the word compiler and manners** (Snar, Tung, Bid, Jarf, Drif), **Swap, Move, Cover, and the rotation AI**, **painted spots** (the Mogel's slime paint), **habitats and the ranged rule** in the composer | Taunt, revive, items, Flee, intents, enemy wind-ups (Mark-bids) |

**Speed groups are in** (`sim/test_speed_groups.py`, `sim/speed_check.py`). Across every family at levels 10 and 30, no Defend is hit before it lands any more (it used to happen up to 2 times a fight against Mogel), and win rates moved only within noise. That's partly because the sim's AI rarely defends: heroes only at under 25% HP, so Defend's real value will show in human play. Mogel Withdraw now blocks about twice the damage.

**The board is in** (`sim/test_board.py`, `sim/board_check.py`). It shifts balance toward the party, by 0 to 18 points depending on the family:

| Pack (level 30) | No board | Board |
|---|---|---|
| Ande | 37% | 31% |
| Ande, drawn ranks | 54% | 55% |
| Mogel, drawn ranks | 54% | 67% |
| Bein | 42% | 51% |
| Drattr | 33% | 49% |
| Djur | 39% | 53% |
| Oskorei | 50% | 60% |
| Draugr | 44% | 62% |

- **Why:** packs of 4 to 6 units overflow into their Rear, where melee hits at 50% and can't reach our casters behind our Front. Hero casters are Downed less (64% to 51% of fights at level 30). All-caster packs (Ande) barely change, because spells ignore rows.
**Rotation and Cover are in** (`sim/test_rotation.py`, `sim/rotation_check.py`). The AI scores them like any other option, for both sides: a hurt Front unit (under 40%) swaps with a healthy melee unit (over 60%) behind it, a Rear melee unit steps into an empty Front spot, a caster in the Front falls back, a healthy front-liner Covers a badly hurt Front ally, and anyone a visible wind-up is aimed at gets Defend, Cover, or Swap. One rescue per hurt ally per round.

- **Rotation barely moves the balance** (within about 3 points). Enemies swap or cover about 0.1–0.5 times a fight, the Mogel 2–3 times. Heroes almost never do: a three-hero party has no spare melee in its Rear.
- **The board's party edge is protection, not missing AI.** Turning off one rule at a time at level 30: melee from the Rear at full damage changes nothing, but letting melee reach the Rear brings every family back to its no-board rate. Our casters behind our Front are safe from melee, and most families are mostly melee.
- **Enemy bows now follow the hero rule** (Volley, Barbed Arrow, Arrow, Rain of Spears reach anywhere, like Skott).
- **Retuned:** enemy damage for the physical families ×1.2 (`SPIRIT_DMG_SCALE` 0.5 → 0.6). Every family is now within about 4 points of its no-board rate, except the Draugr at level 10 (+8):

| Pack | Target L10 (no board) | Now L10 | Target L30 (no board) | Now L30 |
|---|---|---|---|---|
| Ande | 25% | 29% | 31% | 31% |
| Draugr | 30% | 38% | 44% | 49% |
| Bein | 25% | 22% | 42% | 37% |
| Drattr | 20% | 26% | 32% | 34% |
| Djur | 24% | 29% | 37% | 39% |
| Oskorei | 38% | 42% | 51% | 49% |
| Mogel, drawn | 32% | 30% | 53% | 52% |
| Ande, drawn | 30% | 31% | 51% | 52% |

- **The design gap behind the knob:** melee-only families have no answer to a protected Rear. The knob makes them hit harder everywhere instead. The truer fix is one reach answer per family, from its folklore (open question below); the Draugr, the most melee-only, need it most.

**Habitats and the ranged rule are in** (bestiary Part 9). Packs that mix families (Barrow: Draugr, Bein, and Natt or Aska guests) work, but **one reach unit in a pack doesn't give back what the board takes**: include and exclude differ by 2–3 points. What matters is the share of a pack's damage that can reach our Rear. The damage knob stays at 0.6; the ranged rule stays as a design toggle.

**Painted spots are in** for the Mogel (bestiary Part 8): a coat hits whoever stands there, then ticks for 3 rounds; the AI steps off. It costs the party 1–3 points against Mogel packs.

**Events are in** (`sim/events.md`): with `events=True` a fight is a list of plain dicts (start, intents with a reason code and a plain-English why, order, act, hit, falls, end), JSON-ready for the browser front-end and the same shapes for the Godot port.

**The Barrow's rules are in** (bestiary Part 4): the Draugr crawl, the Bein pile, the Beinar jobs (Beinbryn covers, Beinorv shoots, Beinseidr casts in an element), and the Barrow catalog matching the art.

**Dying, Wounded, Dead, items as moves, and fixed unit ids are in** (Nov 8; Part 10, sim/test_dying.py).
- **Our sim difficulty is a comparison setting, not campaign difficulty.** Families are tuned so a random party wins 25–55% of single fights, which is right for comparing families and classes. A dive is about ten fights in a row: at those rates no one finishes one. The dungeon assembler has to set its own difficulty, roughly 90% for a regular fight and 70% for an elite, through pack budgets and levels.

**The loop is designed** (loop_spec.md). **Next:** the end-to-end fight in the browser (a published page: the engine via Pyodide, a canvas, the event stream), then rooms and the animation around fights, then the dungeon assembler.

---

## Part 16: Rooms and the Map (Aspirational)

The shape of a run around the fights. **Recorded as direction, not yet built.** Before it's built we take stock of the art: list what exists, identify the gaps, and either convert, build, or draw what's missing.

### The Map

- **Forward only, like Slay the Spire.** Each room has one to four exits forward and none back. No backtracking.
- **The map screen shows each next room's type** (fight, treasure, event, rest, elite, boss) for planning. Contents stay hidden until you walk in.
- **Rune Gates seed the graph:** three runes shape the rooms on the way to the exit.

### The Rune Gate (Agreed direction, Nov 7)

- **Every gate dungeon is threefold.** Each rune governs its own third and tints the other two lightly, so a gate reads as a journey (Kaun · Logr · Yr: fire, then water, then the grave).
- **Runes are levers,** taken from their old meanings: place (Kaun → Eld and the Surtland, Logr → Vatn and the Rapids, Is → Hrim, Hagall → storm, Bjarkan → the Wildwood, Yr → the Barrow, Sol → Sol), rooms (Fe → treasure, Reid → a longer road, Oss → shrines, Madr → people, Ar → rest), threat (Tyr → more fights, Thurs → elites, Naud → a faster Hunt that pays more, Ur → beasts).
- **Repeats are allowed;** three of one rune is a *pure* gate, the deepest form of that place, possibly with its own boss.
- **Runes are root words.** The spells invoke their meaning, so a rune sharing a name with a tier or a school is fine. Younger Futhark (Old Norse) or Elder Futhark (Proto-Germanic, the z-heavy names: Kaunaz, Laguz, Hagalaz) is still open.
- **Named seeds:** invented words can name a hand-authored gate. Quests and rumours tell of "Something Something Something" at the Rune Gate; learning the words unlocks them, and trying them opens that custom dungeon. Runes are also collected (Hunt fights pay rune charms).
- **The Hunt is the Oskorei:** when the Hunt clock catches you, the Wild Hunt rides in.

### The Hunt Clock

- **The Hunt moves 1 step per room you enter,** plus 1 more for every 5 numbered rounds a fight runs past the first 5 (Bonus Rounds don't count). Playing well (weaknesses, Bonus Rounds, quick fights) holds it off.
- **When it catches you,** the next room that isn't a rest or the boss becomes a **Hunt fight.**
- **Guard against a death spiral:** Hunt fights pay well (Ur materials, rune charms), so being caught is a hard spike, not a penalty on a penalty.
- **The Hunt marker is visible on the map,** moving along your trail.

### Rooms

- **A room is a one-screen strip** (320 px), not part of a continuous level. Moving between rooms is a cut, so rooms don't need to connect.
- **Built from modules:** a left cap, two or three wall segments, a right cap; dressed with props by area tags; lit with palette-safe light pools. Walls are 64 px in dungeons and 48 px in ordinary rooms, built in 16 px courses.
- **You always enter from the left.**
- **Exits are props that say what's behind them** (first pass), and the map agrees:

| Exit | Leads to |
|---|---|
| The open right edge | The main path |
| Iron door | A fight |
| Gilded door | Treasure |
| Crack in the wall | An event or secret |
| Stairs down | An elite |

- Doors are about 48 px tall and sit in the back wall, so four exits and the board fit across the screen.

### One Room, Two Framings

- **Exploring:** a flat side view. The party travels as one sprite, the **leader** (whoever stands Front in the top lane; the next hero takes over if they're Downed). The room shows one enemy, the pack's biggest unit, so you can read the threat before walking in.
- **Walking into an occupied room starts its fight.** The choice was made at the door.
- **The shift:** the wall stays; the floor becomes the slab board. The other two heroes step out of the leader into their cells, and the pack steps out of its avatar. Each family can step out its own way: smaller Mogel ooze out of the big one, Ande flicker out of the lantern light, Draugr climb out of the floor.
- **Victory:** everyone cheers (arms up, eyes open) and holds until the player dismisses the EXP and loot screen. The heroes run back into the leader, the view flattens, and the leader runs to the chosen exit.
- **Between rooms:** run to the exit, the camera drifts a little, fade to black, fade in on the leader running into the next room.

### Kept Out For Now

Backtracking; stacked floors and stairs as walkable space; back-facing sprites for doors; the procedural room assembler (hand-placed rooms first, until the fight loop is fun).

### The Slice Map

A short forward map with one fork: roughly fight, event, fight, treasure, then a boss slime.

---

## Open Questions

- Final names for Cover and Taunt (*Skydd*, *Eggja*).
- **Reach through composition, not per-family moves** (Joseph): mixed packs patch each other (Draugr with Bein archers; insect glue units to come). One ranged unit isn't enough to undo the board's edge, so the damage knob stays at 0.6 unless packs lean further toward reach.
- **Intents on hover:** an always-on intent (icon and phrase) plus hover prose saying what the enemy will do and why.
- Shape multipliers for Slash and Pierce, once the board is in the sim.
- Whether enemy HP shows as a bar or stays hidden.
- What a party wipe costs the Company.
- The Drattr's submerge and the Draugr's rise, in numbers.
