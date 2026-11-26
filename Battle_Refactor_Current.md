# Battle Refactor: Current

**What this is:** the record of where the battle system is going, why, what the game does today, and the gap between them. It reconciles the IDE session's design record (`battle_system_adr.md`, branch `docs/battle-system-adr`, Nov 23) with the design conversation that reviewed it (Nov 23-24, Joseph and Claude). **Where an older doc states a rule this one changes, this one wins;** those docs carry a one-line pointer here.

**Scope:** the new game only (`profile="new"`). Old-game fights stay byte-identical (fingerprints, `regress.py`, the move golden), as they have through every wave.

**Status key:** **Decided** (agreed, not built), **Built**, **Open** (needs design), **Notes** (progression thinking, not locked).

---

## Part 1: Direction, and why

The battle is a conversation between tactical JRPGs (SMT, Persona, Etrian Odyssey) and roguelikes (Slay the Spire, Into the Breach, Darkest Dungeon, Spelunky). Each decision below answers to these five aims.

1. **The stat tug-of-war.** Setup lasts the whole fight, so buffing and debuffing are real investments: three turns of preparation in a twelve-round boss fight, none in a three-round trash fight. Setup is answered by counter-setup, counter magic and items, never by a timer quietly undoing it. *(Nocturne's lasting buffs and resets, made legible by roguelike intents.)*
2. **Attrition across a dive.** No free sustain: no universal Meditate, no free attacks, heals that don't refill the run. HP and MP are carried from room to room; Rests, draughts and choices carry the run. A party that ignores a dimension of the game (stats, sustain, reach) pays for it, and finds what it lacks in the Pouch.
3. **Legible odds.** You can always see the roll: a clean hit at neutral, crits when ahead, grazes when behind. Nothing fails silently at neutral; a 50% graze keeps a bad position moving forward instead of switching it off.
4. **Foes are characters.** Each family, and each job within it, has habits: moves made for it, and the times and places it likes to use them. Players learn a family by what it does ("Mogel want you Blinded"). Foes don't pay costs as heroes do; their identity is their kit and their wants.
5. **Scarce, personal growth.** A run grows a few moves deep, not every move wide. Growth is a choice against recovery (the Rest), so each run's build is its own: one signature move carved deep, a few useful ones beside it.

---

## Part 2: The decisions

Each entry: **Direction** (what and why), **Today** (what the code and docs do now), **Toward implementation** (notes, not pseudocode).

### D1. Accuracy: the crit and graze ladder (Built Nov 24, Wave A; IDE ADR-01)

**Direction.** The net is the attacker's ACC minus the target's EVA, from −3 to +3.

| Net | Graze | Crit | Clean |
|---|---|---|---|
| +3 / +2 / +1 | 0 | 100% / 66% / 33% | the rest |
| 0 | 0 | 5% | 95% |
| −1 / −2 / −3 | 50% / 75% / 100% | 5% of what doesn't graze | the rest |

- **No whiffs.** A graze deals 50%, carries no riders, no flare, and **earns no Bonus Round**. A status-only move that grazes is shrugged off.
- **Status moves land for certain at neutral** (the hidden 20% fail is gone). Crits ×1.5.
- *Why:* every stack of Keen, Marked, Blinded and Evasive now means something; ACC owns crits, EVA owns grazes, DEF owns damage. A graze is a floor, not an off switch.
- *Cost, accepted:* damage at neutral rises about 11% (a neutral hit averaged 0.93 of a clean one; now 1.03), on both sides: one retune. "Miss!" goes; Evasive reads as glancing blows. ±3 is absolute: Blinded 3 lands no statuses, Evasive 3 takes half damage and no riders, until it's answered.

**Today.** `Battle.odds` (Nov 21, Wave 7 A): neutral graze `GRAZE_BASE` 0.20, crit `CRIT_BASE` 0.05 plus DEX; ahead, a crit `AHEAD_CRIT` 1/3 and no graze; behind, a whiff `WHIFF_CHANCE` 1/3, then the plain roll. A status move rolls like a hit (Nov 22), so at neutral it fails on the 20% graze. `land()` grants a Bonus Round on a weak hit **even when it grazed** (engine.py, the `aff == "weak"` branch after the hit).

**Toward implementation.** `odds`, `roll`, `expected_roll_mult`, `land`, `flurry`, `status_lands`, `knot_hold` and the AI's valuations. The whiff's text and float go; the page's MISS float goes. Retune the yardstick once (neutral damage up ~11%). Tests: neutral statuses land; a graze strips riders and the Bonus Round; ±3 at 100%. The page's odds readout shows the new table.

### D2. Stats persist, and the pairs combine (Built Nov 24, Wave B; IDE ADR-02)

**Direction.**
- **Stats persist for the fight** and wash when it ends. No end-of-round decay. Opposite moves cancel step for step (clamped −3 to +3).
- **Five counters, combined:** Mighty / Feeble (ATK and MAT), **Fortified** / Sundered (DEF and MDF), Quick / Slowed (SPD), Keen / Blinded (ACC), Evasive / Marked (EVA). Waxing, Waning, Hexed and Warded retire. Bodies keep separate base stats (the Bein's high DEF, the Ande's high MDF still route damage); only the counters combine, so the Vasara's Sundered helps the Brennumar too.
- **The curve stays:** ×1.33 / 1.67 / 2.0 up, ×0.75 / 0.6 / 0.5 down. Mighty 3 against Sundered 3 is ×4: the payoff for three turns of setup, telegraphed and answerable. Kept, and measured.
- **No rider cap.** A damage rider (Brakrosh's Sundered) lands a step on every clean hit and can take a target to 3. Costing carries it: Brakrosh is 32 HP for 0.6 of a Krosh against Krosh's 16 HP for 1.0. Measured (Nov 24): in a 1700-HP boss room it shortens the fight ~18% (one Brakrosh) to ~27% (three); in Fodder it's wasted and Halvkrosh is the right call. The curve gives its own diminishing returns (+33%, +25%, +20% a step). *Look at the circumstances that produce a configuration before inventing a rule against it.*
- *Why:* setup that lasts is a decision; setup that decays is upkeep. Foes' big debuff turns become telegraphed threats you prepare for (Joseph's example: a Hexer whose Weaken and Debilitate sweep the party; you hold Mighty 3 and Fortified 3, or Skolja ready).
- **Twinned offense verbs** (carried from the IDE ADR, not yet re-discussed): Aukseid a selfish caster ramp (self Mighty, candidate +2), Aukraft the ally or party +1.

**Today.** `STAT_NAMES` plus `NEW_GAME_STAT_NAMES` (seven pairs, Waxing/Waning/Hexed/Warded named in the new game). `end_round` walks every untouched stat one step toward 0 (the staircase, Nov 22). Aukraft pushes ATK, Aukseid MAT. classes.md's Sundered (Vasara) decays when she stops hitting; the Ullar's Lonnpeka refreshes it.

**Toward implementation.** `Unit.stages`, `raw_damage` (one offense counter, one defense counter, read by physical and magical alike), `end_round` (no stat decay), `counter_name`, `counter_value`, `status_stat`, `BUNDLES`, words.py's stat verbs, gloss and audit, `screen.js`'s counter sets. **Lonnskolja** (lifts lowered stats to 0) becomes the key counter spell; **Song** keeps its own decay (it's a counter that fades when nobody sings: a song stops). The Vasara's Sundered signature is lost as written: see O2.

### D3. Held stats (Built Nov 24, Wave B)

**Direction.** One primitive, **one rule for every hold** (Nov 24): a move sets a stat to a level for N rounds and records how far it moved it. **While it holds, pushes that hurt the bearer are blocked and pushes that help still land** (on all five counters, positive helps the bearer). **On expiry or removal, the hold's own change is undone, clamped to −3..+3.** Skolja cleanses harmful holds; Stabilize dispels helpful ones. **A unit with a held stat can't be targeted by another hold on that stat** (excluded when aiming: no refreshes, no stacking, so a hold can't be kept up forever).

| Move | Holds | For |
|---|---|---|
| **Gyllenlykt** | EVA at +3 | 3 rounds |
| **Disarm** | Feeble 3 (offense at −3) | 3 rounds |
| **Steadfast** | DEF where it is | N rounds |

- *Why:* three moves, one rule. A held stat is bounded (it can't snowball), reads clearly, and restores honestly: an enemy's Disarm on a debuffed hero doesn't quietly cleanse them when it ends, and on a buffed hero it doesn't quietly wipe their Mighty.
- **Gyllenlykt** under D1 is very strong (3 rounds of every hit grazing: half damage, no statuses, no riders, no Bonus Rounds against that hero); **start at 20 MP** (up from 16 MP, to tamp down spam; re-checked when built).
- **How it plays out** (Joseph's worked cases): **Disarm** drops offense to −3, blocks Feeble, lets Mighty push back (Mighty 3 lifts −3 to 0; a second reaches Mighty 3 even while Disarmed); on expiry or Skolja the recorded drop is added back, so Feeble 2 before comes back as Feeble 2, Mighty 3 before as Mighty 3, and a hero who fought up to Mighty 3 stays there. **Steadfast** moves DEF by 0, blocks Sundered, allows Fortified (a Steadfast hero can still Aukskold). **Gyllenlykt** raises EVA to +3 and blocks Marked; a foe's own Keen still cuts the net from the attacker's side, so the lantern is unshakeable, not untouchable. A move can still print a different ending as its price ("takes all your EVA with it"); the default is the undo.
- **This replaces the IDE ADR-06's Gyllenlykt as a tile** (no burst, ~64 MP). Tile paint stays open for the Mogel (O4).

**Today.** Gyllenlykt is Lak with Lonn: a heal and Evasive 3 (the printed rider), which decays by the staircase. Disarmed is a bundle (ATK −1 and MAT −1 a stack, cap 3). Steadfast is a bundle (DEF +1 a stack; never Late, never shoved; a wall).

**Toward implementation.** A `held` record on the unit per stat (level, rounds, the recorded change, harmful or helpful for the cleanse and the dispel). Stat changes check it first: negative pushes blocked, positive land. Targeting excludes a unit whose stat is already held by a hold on that stat (the menu greys it; the AI never picks it). It ticks at round end like an ailment and restores on expiry or cleanse. Steadfast no longer blocks Late or shoves (Fear on a Steadfast hero still makes them Late; their DEF doesn't move).

### D4. Bundles are shorthand (Built Nov 24, Wave B)

**Direction.** A bundle is a label on a move: it applies its parts, then each part lives by its own rule. Stat parts persist (D2); ailment parts tick their rounds. There is no bundle status left to track or oppose.

- **Feared** = Late for its rounds, and Sundered 1. (Late is the one primitive: Reeling is Late only.)
- **Cursed** = Sundered 1 and Poisoned (was MDF −1).
- **Venom** = Poisoned and Bleeding (unchanged).
- **Disarmed** becomes Disarm, a held stat (D3). **Steadfast** becomes a held stat (D3).
- New moves compose freely: *Sticky Slime* (a Mogel spit: Bound, then Late for 3 rounds) is two existing parts, no new rule.

**Today.** `BUNDLES` in data.py are statuses with stat parts that scale with their rounds and step down like ailments; Feared and Steadfast pull against each other stack for stack (`BUNDLE_OPPOSITE`).

**Toward implementation.** `apply_status` expands a bundle into its parts; `BUNDLE_OPPOSITE` and the bundle stat path in `status_stat` go. The page shows the parts, not the label (the move's card keeps the label).

### D5. Guard (Built Nov 24, Wave A; IDE ADR-08)

**Direction.** Guard halves damage **and a weak hit on a Guarding target earns no Bonus Round.** Guard does nothing to stats: stats are answered by counter magic, opposite moves and items. *Why:* a telegraphed weakness intent becomes a three-way puzzle for every hero (kill or interrupt it, Cover it with a resistant tank, or Guard to deny the tempo).

**Today.** `land()` halves damage for `t.defending`, then grants the Bonus Round on a weak hit regardless.

**Toward implementation.** Gate `self.eligible.add` on `not t.defending` in `land`, `flurry` and `status_lands`. The AI values a weak hit on a Guarding hero without the Bonus Round.

### D6. No forced Advance (Built Nov 24, Wave A; IDE ADR-09)

**Direction.** When a side's Front falls, nobody loses a turn stepping up. The empty Front already exposes the Rear (`eff_front`); a melee unit left in the Rear hits at half (`REAR_MELEE_MULT`) until it **chooses** to step up. *Why:* the formation already punishes a collapse; confiscating the turn on top of that takes away the crisis turn.

**Today.** `plan_phase` runs `advancers` before the unit decides.

**Toward implementation.** Skip `advancers` in the new game, both sides. The AI needs a rule to step up when it's melee in an exposed Rear (or its foes will sit there at half). The page shows a Rear melee unit as exposed. Old tests that assert auto-advance stay under the old profile.

### D7. Code leaks (Built Nov 24, Wave A, but the paint line; IDE review)

- `preview_order` doesn't share `order`'s tie-break (an exact SPD tie goes to the party): one sort key.
- `knot_hold` still prices grazes by the old formula (`GRAZE_BASE − STEP × net`): read `odds()`.
- A graze on a weakness earns a Bonus Round (D1 and D5 fix it).
- When nothing is affordable, the AI's `declare` falls back to `u.actions[0]` and the turn is skipped as "spent" (engine.py, the end of the AI's option scoring): fall back to **Guard** (Joseph's catch).
- `paint` on a whiff emits a 0-damage hit (moot once D1 removes whiffs; check the graze path).

### D8. Sustain (Built Nov 24, Wave C; IDE ADR-04, amended)

**Direction.**
- **Meditate goes as a universal action, and returns as a found move, *Anda*** ("breathe"; Meditate's tongue name, the brother word of the Ande, the living breath). **Djupanda** is its Bid form: Anda plus Bid, spoken by its byname (as Geirskott is); the planned **Waterfall Rune** talisman (gloss: "Meditate becomes Djupanda") does it for free. Anda acts at normal speed and restores less; Djupanda winds up and restores more. The Anda line is sketched in Part 4.
- **Universal Meditate goes.** Magicals carry big pools (100-200 MP) and meter them across rooms with Rests, Spirit Draughts and found moves. *Why:* a guaranteed refill means MP is never a resource; casters now feel the room-to-room tension martials feel in HP.
- **Djupanda is found, not universal**: a Bid (wind up, then release next round), strong in long boss fights where the party protects the caster, costly in short ones. (The IDE ADR's "Late" release is dropped: Late on a Bid adds almost nothing but a slightly later release, Joseph.)
- **The Skurmar's Knots 3** restores a small amount of MP each turn, no longer "half a Meditate." The amount stays below a Blast's cost (the Nov 21 lesson: 9 MP a round was free Blasts forever).
- **Lak heals 75 for 12 MP** (was 100 for 8). *Why:* a heal about the size of one Regular hit (~75) trades even for a turn, so healing is never automatic and never dead; a full 200-MP bar heals about 1,250 (16 casts), under one Rest, where it was about 2,500 (1.6 Rests). The turn choice becomes heal, or buff and debuff so the fight ends sooner. Row and party heals scale by the reach rules (Floklak about 30-ish a head in a boss fight is the feel). **Refactor plan Phase C's "heals at 1.2 (Lak ~125)" is retired.**
- **The Halv is an ordinary kit move**: 4 HP or 2 MP, cheap and never free, competing for the four slots. Most likely acquired by carving your main move down, or a future talisman that turns your starter into its Halv. **The auto-filled Halv goes:** an empty slot stays empty until you pack or carve something.
- **The sharp edge, accepted:** a caster at 0 MP has no spell attack (even Halveld costs 2 MP) unless they cross-pollinated into an HP-cost martial move (future): drink a Spirit Draught, use `Djupanda`/`Meditate` if found, Guard, or wait. The pools are large; the numbers tune it.

**Today.** `can_meditate` gives every new-game magical Meditate (`MEDITATE_SHARE` 0.15 of max MP); `screen.js` reserves a menu slot for it. Djupanda is a free Bid any magical can carry (`DJUPANDA_SHARE` 0.40), in the Brennumar's leg-3 kit. `LAK_CLEAN` 100; Lak costs 8 MP. `build_hero` drops the class's Halv (`BASIC_VERB`) into a free slot of `KIT_SLOTS`. classes.md: the Skurmar's Knots 3 deepens his Meditate and Djupanda.

**Toward implementation.** `can_meditate` off; the menu's slot goes; `LAK_CLEAN` 75 and Lak's cost 12; `build_hero` stops filling; kits re-checked (a leg-1 kit of two or three intentional starters and empty slots); Knots 3's MP amount; Djupanda's release group. Ensure `Battle.declare()` (not just `autofill()`) falls back cleanly to `Guard` when a caster has 0 MP instead of returning `u.actions[0]` and skipping as `"spent"`. The gauntlet needs Rest rooms (D9) before its numbers mean anything for casters.

### D9. The per-hero Rest (Decided; new, Nov 24; the Rest itself built in Wave C, the screen waits for the dive)

**Direction.** At a Rest, **each hero** chooses Rest or Carve. Rest restores (the IDE ADR's 2/3 of max HP and MP is the starting number) and raises the Down; Carve mutates one of that hero's moves and heals nothing. *Why:* growth costs one hero's recovery, not the party's, and it opens meta-play: keep the Vasara safe in the Rear so she can carve.

**The screen** (Joseph): the campfire backdrop; three hero panels, each with a campfire and a rune to click; each Rest panel previews what it would heal; an "everyone rests" shortcut; **Continue…** (the same lock-in-then-resolve rhythm as a fight round). The resting heroes get their green +NN floats in the background while the screen moves to the carvers, left to right: pick the move, pick the mutation, confirm, the next carver, then back to the tapestry.

**Today.** dive_spec and pillars: a Rest room is Rest **or** Carve for the party; the column before each boss is always a camp. The dive isn't built; the gauntlet has no Rests.

**Toward implementation.** A Rest step in `gauntlet.py` (per hero: the AI rests whoever is hurt) so caster parties are measured fairly. The screen waits for the dive's UI.

### D10. Intercession (Decided Nov 23; Cover built Nov 24, the pilot's step 1)

Lya is intercession (I protect someone you might fire at); Egga is Taunt (I draw your fire). In the new game, **Lya takes one interception, then the stance ends**; Merlya takes 2 (Jatte 3, foe bosses); Lonnlya is Fortified 1, then Cover (foes: Cover, Hi-Cover, Great Cover, Bulwark, Hi-Bulwark). One coverer per ally; a whole move is one interception; rows and All aren't caught. Lya keeps 8 HP. **Foes get intercession, never Taunt.**

**Built (Nov 24).** `data.COVERS_BY_TIER` (Halv and Base 1, Mer 2, Jatte 3: the foes' Great Cover; heroes carve Lya up to Mer); `Unit.cover_left`; `Battle.covers`; `intercept` spends one a move and the last ends the stance ("The cover on Dagskald is spent."); the round's start clears it. **Lonnlya** compiles: Lya's designated rider is Fortified 1, pushed on the coverer first (16 HP, the Lonn step's doubling: check with the costing pass, O3). The card and the cover line say how many hits ("covers Dagskald (the next hit)"). The AI values a Merlya a half more. Old game: the round-long Cover, untouched. `test_cover.py`.

**What it showed:** nothing moved (the gauntlet 195 / 50 / 26, the calibration rooms the same), because **almost nobody Covers**: in 300 Elite and Boss fights the heroes Covered 0 times and the foes 27. The shared scorer only Covers an ally under 30% from a healthy front-liner. Using Cover is the Beinbryn brain's job (the pilot's step 3); heroes' Lya is the player's.

### D11. Foes are characters (Decided; Nov 24)

**Direction.**
- **Foes have habits, as data:** a unit *wants* a hero at a level of something (`wants: {"Blinded": 1}`) and uses the move that gets it there until it's true; clear it and the habit returns. This is the brains' goal-with-UNTIL (beinar_pilot Part 2). Mixed teams coordinate for free: the Mogel want Blinded 1, the Leshi want 2, so the Leshi keep pressing after the Mogel are satisfied.
- **Custom moves made for a family** are welcome (*Mogel Spray*: no cost, one target, no damage, Blinded 1). We have all the pieces and arrange them as we please.
- **Foes don't pay costs as heroes do**, and needn't: trash is swept away in a few rounds. Their kits are where control lives: a twist that leaves a lasting stat is a kit choice, made on purpose.
- **The boss reset** (IDE ADR-03: a telegraphed, turn-costing self-cleanse or party-leveller at Normal or Late speed) becomes a **Stabilize** move in the team plans (beinar_pilot Part 2 section 7), not a separate AI system.

**Today.** Generated foe kits (Ande, Mogel) take their child element's Styng form automatically (Styngreyk: a certain Blinded on a clean hit), which under D2 leaves lasting stats. The Beinar pilot's hand-made kits and brains are designed, not built. The mirror is built (Nov 23).

**Toward implementation.** With the pilot's brains: `wants` as a rule type; the pilot's kits checked against D1-D4; the generated Ande and Mogel kits reviewed in the enemy pass.

### D13. The fuse, Withered, and one clock (Built Nov 24, Wave D)

**Why.** Joseph's run lost the Regular room to an Aska twist (a Curse, so a lasting Sundered) on top of poison that only ever got worse. Damage ailments grew without limit and gave no reason to build or juggle them.

**The rule.**
- **One clock for every stacked ailment.** A stack nobody adds to drops one at round end, never the round it lands. The number is both how long it lasts untouched and, for the ones that escalate, how hot it burns.
- **The fuse:** a tick is a top share of max HP through FADE (3: all of it, 2: half, 1: a fifth). **Poison 12 / 6 / 2.4%**, bites at round start. **Bleeding 14 / 7 / 2.8%**, bites only when its bearer acts (any action), and still drops at round end when they don't. **The top is capped at a clean Krosh (`KROSH_CLEAN`, 104), for anyone, and the shape applies under the cap**, so a boss's size can't turn a poison into an execution and every height still doubles the one below: a 1700-HP boss burns 104 / 52 / 21 (the review's catch: capping after the shape made 2 and 3 both 104).
- **Withered is Aska's twist** (the Curse stays on dedicated Curse moves, seen and telegraphed: Aska's status move, Jattenid, Beinseidr). Withered 1: healing halved; 2: blocked; 3: reversed (healing hurts). Withered Bein piles don't rise.
- **The AI values the fuse** (a tick's total over the rounds it will last, `fuse_total`) and Withered (worth most against a team that heals or a Bein team); its heals and songs are discounted by the target's Withered.
- **Lak's log shows the numbers** (`Brennumar casts Lak, healing Vasara (+75)`), in the new game.

**Built.** `data.FUSE_TOP`, `WITHERED_HEAL`, `CHILD_TWIST["Aska"]`, Withered in `STACKED_AILMENTS` and `STATUSES`. `Battle.fuse_tick`, `fuse_total`, `heal_factor`, `mend` (one door for every heal: Lak, songs, items) and `burned` (a reversed heal is its own `withered` event, told after the cast, and can down; a heal event never carries a negative amount; a blocked one says `(blocked)` and the page floats a grey 0). `tick_piles` skips Withered piles. Tests: `test_wave_d.py`. Old fights identical.

**The review of Wave D (Nov 24), fixed:** the AI's potions now read Withered (it would have used a Strong Life Draught on a Withered 3 ally: a 1000-HP wound); single-target Gyllenlykt's light counts only beside a real heal; Gyllenlykt holds nothing on an ally its heal just downed; the page draws a reversed heal as a wound (it showed a green `+-75`); the cap moved onto the top. Feel check for play: a Bleed 1 is 10-12 HP on a Regular, a primer until it's fed.

### D14. How an effect lasts: two fields (Agreed Nov 24, Joseph; the rounds row built with the pilot's kits)

**The rule.** Not everything has to be permanent, or on the clock. A timed effect is customized for feel, as data, by answering two questions:

| What makes it fade | All at once | One step at a time |
|---|---|---|
| **Never (the fight)** | a plain stat move (D2) | |
| **Rounds** | **Rally**: Mighty 2 for 3 rounds | the ailment clock (D13) |
| **Its bearer's attack** | "Mighty 3 until you swing" | "Fortified 3, one off per attack you make" |
| **Being hit** | a ward that breaks | a shell that chips |

- **What it gave is what it takes back,** never past 0: an opposing push eats into it first. Rally on Mighty 0 Nedkraft'd to 1 ends at 0; Rally on Mighty 1 (to 3) ends at Mighty 1.
- **No second one while it's up** (no Rally while a Rally is on), unless its data says otherwise.
- **A window isn't a hold:** a D3 hold locks a stat (lowering pushes fail); a window only times a push, and pushes against it land.
- **A whole move is one use** (as with Cover): a flurry spends "until you attack" once.
- **Every timed effect shows on the board** with its trigger and count, like the hold tags. A badge the player can't read is a rule they can't play around: the only real limit on how many shapes there are. New rows are added when a move needs them, not up front.
- Rally, Pinned's window and the holds go through this one path (the pilot's step 2).

**Built (Nov 24), the rounds-and-all-at-once cell:** a window is a hold without its lock (`Battle.hold(..., lock=False, push=n)`): the same record, tick, "no second while it's up" and board tag; `push` lets pushes against it land; `release` takes back what it gave, never past 0. The Inspect card says "raised, N rounds (then it's taken back)". A window's `ai_rest` is the AI's wait after one closes (`Battle.rested`; Rally 2: Joseph, a behaviour, not a rule). The other rows wait for a move that needs them. **Window ailments** (`WINDOW_AILMENTS`: Pinned, Silenced) land for their printed rounds and can't be added to while on, heroes' Pins too (Joseph). Silenced stacked before this (I'd said it didn't; it does now).

### D12. Already built under this direction

- **The mirror** (Nov 23): packs reserve reach slots within budget; on for the new game's rooms. beinar_pilot Part 2 section 8.
- **The status rules** (Nov 22) still stand except where D1-D4 replace them: ailments (stacks, caps, rounds, never dropping the round they land), parents hit and children twist, Frozen replacing Chilled (single-target chills only), boss immunities, Skolja and Lonnskolja, a printed size winning over the tier. **Replaced:** the stat staircase (D2), the split stat names (D2), bundles as statuses (D4), whiffs (D1).

---

## Part 3: Open (needs design)

### O1. The stack economy

Moves relate to stacks in seven ways:

| Kind | What it does | Example |
|---|---|---|
| **Build** | adds stacks | Brakrosh |
| **Cash-in** | needs a stack, or scales with stacks, without using them | Fangskott (needs Pinned); Hevn (hits she took) |
| **Spend** | uses stacks up for a payoff | the Vasara eating Sundered (O2) |
| **Regular** | any hit, simply better against the stacks there | any hit on a Sundered target |
| **Convert** | turns one stack into another | Fortified into Mighty ("the shield becomes the hammer"); a niche inverter (Fortified 3 becomes Sundered 3, Feeble 3 becomes Mighty 3); Scorched or Chilled into something new |
| **Steal** | moves a stack from the target to yourself | take their Mighty: for tricky classes |
| **Answer** | pays off on events | Hevn (hits taken since her last turn) |

- **A move pays in at most two of three currencies:** price (HP or MP), stacks (spent), time (a Bid wind-up, a Tung strike acting last, making yourself Late). A *required* stack is a condition, not a payment.
- **"Spend a stack" wants one shared grammar piece** every class talks to (the Vasara eats Sundered, the Ullar Marked, the Brennumar Scorched). It needs a word: a naming session.
- **A cash-in on your own stacks** (Joseph, as a shape, numbers not set): a move stronger than a Krosh that returns a share of its damage to the user as recoil, and hits harder for each Sundered on *you*. "Might kill you, will melt them," and a crit build beside it melts faster. Numbers to work out: from ×1.33 to ×2 over three levels is about +22% a level. Whether its bonuses multiply with Mighty or add (Mighty 3 with three levels: ×2.67 multiplied, ×2.33 added) is decided with it.

### O2. The Vasara's Sundered signature

D2 ends "the one she keeps hitting stays at three," and the Ullar's refresh of it. Direction (Joseph): design into the new space. Her signature moves to **eating** Sundered stacks (a Krosh branch that spends a stack for a special attack; the mirror image spends her own Fortified). The Ullar likewise could spend Marked (Fangskott already cashes in on Pinned).

### O3. Two-curve costing (IDE ADR-07)

Output and reach (Mer, Flok, All, Styng) stay steep; tactical sidegrades (Tung, Bid, Jar, Drif, a modest Snar) cheap, their drawback being their cost; Lonn not taxed twice (0.6 power **and** ×2 price). **Watch `rider_price` here** (Joseph, Nov 24): it's a flat step, so Allgyllenlykt costs 104 against Alllak's 96: only 8 more to hold EVA +3 on the whole party for 3 rounds. **Jar takes full power (1.0) and a gentle-to-zero cost** (Nov 24): it earns its place only at +1 and +2 (EV 1.25 and 1.50 against a normal hit's 1.17 and 1.33; dead even at −1, 0 and +3), so Jarf's old 0.7 power and ×1.5 price would make it strictly worse everywhere. Awkward extremes (Allblotskott) become Pouch items rather than hero carves. Belongs with the audit's open question (23 carves past the ladder), and with D2's costing role for riders.

### O4. Tile paint (IDE ADR-06, less Gyllenlykt)

Typed cell effects: the Mogel's empty-tile, occupied-tile and row paints with a cap of about three slimed cells, later caltrops. Built with the Mogel's enemy pass; the page draws tiles then.

### O5. The Wild Hunt (Agreed direction; IDE ADR-05)

`combat_spec` already has the **Hunt clock** (dive-level pressure turning future rooms into Hunt fights), and inside a single room stalling needs a hard stop so players can't loop Djupanda and heals forever once the clock maxes out. **Direction (agreed Nov 24):** **non-boss rooms only.** Diegetic float-text warnings (Strike 1: cold and fog; Strike 2: a hunting horn; no HUD badge), then on Strike 3 a **mid-fight Wild Hunt intrusion**: the Oskorei ride through and kill or scatter the room's remaining foes, replacing the enemy board with high-damage, lowish-HP spectral Hunters (`no_flee`) that must be killed to end the fight. **The intrusion forfeits the room's spoils** (scattered foes drop nothing) **and pays less than a real Hunt fight** (scraps at most), so stalling on purpose to farm Hunt loot never pays: an intrusion is a survival tax; real Hunt rooms keep their Ur materials and charms. It kills stall-farming immediately, avoids board-slot overflow, and keeps the Hunt terrifying. The stall-tick threshold and how it feeds the dive clock settle when built.

### O6. Rests in the gauntlet, and the four-family enemy pass

The gauntlet's per-hero Rest (D9). The enemy pass restores family bodies' HP (classes.md: "families are all plain for now; their deviations are the enemy pass"); the IDE ADR-10's family notes (the Draugr's telegraphed haymaker wind-ups waking up Guard, Cover and Stun; the Mogel's paint; the Ande as all-reach glue) fold into it beside beinar_pilot Parts 3 and 4.

### O7. The ailment shapes (Nov 24, with Wave D)

Every ailment should be one of **three shapes**, so a player reads it at a glance:

| Shape | How it works | Today |
|---|---|---|
| **Escalating tick** | the fuse: hotter at 3, burns down | Poison, Bleeding |
| **Threshold pop** | builds quietly, then something happens at a count | Frozen (a second chill) |
| **Countdown window** | lasts N rounds, then something happens or ends | holds (D3), Withered's steps |

Ideas waiting their turn, each with an owner:
- **Skuld** (countdown debt): a mark that comes due after N rounds (the Norns' "what is owed"). A countdown window with a payoff.
- **Drain** as a keyword: a third of the damage dealt comes back as HP. First home: the Draugr's **Death Bite**.
- **Sleep** only with its own payoff and its own owner: **Svefnthorn** (the sleep-thorn). No free skip-a-turn; Sleep comes with a reason to wake it (a big hit) or to keep it.
- **Charged**: goes to the Skurmar's card pass.
- **Tangled**: the Leshi's.
- **The missing hero dispel:** heroes can't remove a foe's helpful hold or buff. A gap for the class passes.

---

## Part 4: Progression notes (not locked)

- **Method:** lay the system bare before locking anything: every morpheme, every move coded to a class, every permutation. Design the **Vasara's web of moves**, then the **Brennumar's**, and gate from what they show. The tool: a **Growth view** in the Grammar Library, generated by the compiler (roots, then each one-carve fork, then the second), each edge marked keep, cut or maybe by Joseph. Those marks become the gating tables. (The Vasara today has 103 legal words: Krosh 53, Hevn 27, Egga 11, Aukskold 10, Lya 2.)
- **Gating is data:** per root, "from here, these carves." The grammar decides what a word *is*; the table decides what's reachable next.
- **Scarcity is intended.** A run holds about 3-6 Rests for the whole party, plus Event carves: one deep signature move a run, a few shallower ones.
- **Rewards:** after a fight, one of three (a tome, a mutation, or marks); later legs may offer moves already carved (a Reyk in leg 2, a Styngreyk in leg 3). Carving at the Rest (D9).
- **The Vasara:** *the Anvil: covers allies, takes the hits, debilitates with the hammer.* Moves in five groups: **Strike** (Krosh, the mace: break), **Shield bash** (**Stot**, new: control: Stun, Tung, shoves, Late), **Protect** (Egga, Lya), **Brace** (Aukskold), **Answer** (Hevn). She **starts with Krosh, Egga and Stot**, one slot open for a find. Found as hammer and shield tomes: Lya, Aukskold, Hevn.
- **Stot, the shield (decided Nov 25, Joseph; not built).** Egga controls who they hit, Lya what gets through; the shield controls **whether they act at all**. **Stot:** 0.6 of a Krosh (12), **50% Stun**, normal speed, **12 HP**. Its forks by manner: **Tungstot** (Late, after the foe has acted: a sure Stun on its *next round's* action, so it breaks a wound-up blow before it lands) and **Snarstot** (before they act: 50%, interrupting this round). **Bosses are immune** to Stun, and Stot doesn't hide a Stagger for them ("immune is immune"; other moves do Late). Later carves from Stot, each new engine work: **the shove** (push a Front foe back) and **Parry** (an early stance that answers a blow with a double Krosh).
- **Stun becomes one flip, everywhere (decided Nov 25):** if it lands, the foe **loses its next action**. Today it's two: it lands, then each action flips 50% to lose it (up to 3 rounds), so it almost always costs one action but nobody knows which. A tank's control has to answer *a* threat. It strengthens Lonnblixt's Stun too (the costing pass, O3).
- **A run as the Vasara, played forward (Joseph, Nov 25):** she starts with Krosh, Egga and Stot, one slot open. After each fight the party picks one of three rewards (tomes from her schools, Krosh, Egga, Lya, Stot, Aukskold, Hevn, interleaved with the others', marks, the occasional quest item); a Rest lets one hero carve (Krosh to Merkrosh, replacing it). Notes: with one pick a fight across three heroes, one hero sees a tome maybe a fight in three, so the carves carry the run's identity (and the reward table might favour an empty slot); a school's base move should be interesting on sight (Joseph: "Aukskold, not the coolest thing"); the safe carve (Mer) is the baseline the interesting ones must beat somewhere.
- **The webs go hero by hero,** the Vasara first (the Growth view).
- **Krosh's forks** (sketch): Merkrosh (power), Halvkrosh (cheap), Brakrosh (break), Flokrosh (a row-crush: a dead end, and strong), Drifkrosh, Jarkrosh, Bidkrosh; Brakrosh onward to Snarbrakrosh or Tungbrakrosh; Halvkrosh onward by a manner (Halvsnarkrosh, Halvdrifkrosh compile today; Styng doesn't apply to damage verbs). Jattekrosh found or carved: not settled.
- **Jarf becomes Jar** (Jarkrosh, Jarskar, Jarspett, Drifjarskar): **degraded accuracy where every non-Graze is a Crit** (no clean hits). Scales cleanly along the D1 ladder: `−2/−3` = `100%` Graze / `0%` Crit; `−1` = `75%` Graze / `25%` Crit; **`0` (neutral) = `50%` Graze / `50%` Crit** (`1.00×` EV, high swing); **`+1` = `25%` Graze / `75%` Crit** (`1.25×` EV); **`+2/+3` = `0%` Graze / `100%` Crit** (`1.50×` EV). So `Keen`/`Marked` + `Jar` scales smoothly through `+1` and `+2`. Today Jarf is 0.7 power, ×1.5 cost, +20% crit chance, crits ×3; Jar is full power on the gentle cost curve (O3).
- **Anda takes only Bid for now** (Joseph's Wave C review, Nov 24): a free move that grows for free is strictly better (Snaranda, Meranda), so `VERBS["Anda"]["only"]` refuses everything but Bid until Meranda has its price in HP. Djupanda is a root name, so later parts attach to it (Merdjupanda).
- **The Anda line** (sketch, Nov 24; numbers as shares of max MP so every caster scales; Joseph's figures for the Brennumar's 150 in brackets): **Anda**, normal speed, about 13% (≈20); **Djupanda** (Anda + Bid), about a third (≈50): a Bid costs two turns, so it must beat two Andas (≈40), which is why the middle can't sit near 32; **a drawback form above Djupanda** (≈65), paid in something other than tempo. Candidates for that payment: **HP** (a Mer Anda priced in HP, since a free move has no other lever for Mer); **Blotanda** (Anda's rider is Bleeding, and Anda targets the caster, so the bleed lands on them); **a self-hold** (a trance: Disarm on yourself, or Sundered held at −3 for 3 rounds: bounded by D3, where a plain persistent Sundered 3 would last the whole fight). An MP song (a Kvad for MP) is a Dagskald idea for Phase C.
- **The shared core:** build the common spine, then let each class have its conversation with it, dipping into places that make it unique.

---

## Part 5: Order of work

1. **This record**, and pointers from the docs it supersedes. *(Nov 24.)*
2. **Wave A: built (Nov 24).** D1 accuracy, D5 Guard, D6 no forced Advance, D7 leaks. `data.CRIT_BY_NET`, `GRAZE_BY_NET`; `Battle.odds` the ladder (no whiffs; DEX keeps its small touch on the 5% base crit); a graze or a Guarding target earns no Bonus Round (`land`, `flurry`, `status_lands`); no `advancers` in the new game (the AI's step-up option already scores taking an empty Front); `knot_hold` reads `odds`; `preview_order` shares `order`'s tie-break; nothing affordable Guards. Tests: `test_wave7a.py` (the ladder, a graze as a floor, Guard, no forced Advance, the Guard fallback), `test_status_rules.py`, `test_wave4a.py`; 408 pass. Old fights identical (fingerprint 288, regress 3bdf6771deb1, golden 4535). Glossary and audit wording updated. **Measured** (150 mirrored rooms a kind, Dagskald, Skurmar, Vasara at leg 2; before / after): Elite 97% / 98% won in 8.4 / 6.8 rounds, end HP Vasara 40% / 39%, Skurmar 71% / 69%, Dagskald 90% / 89%; Boss 96% / 94% in 11.2 / 9.9 rounds, 33% / 34%, 61% / 59%, 79% / 77%; the gauntlet's Elite cleared 81 of 191 / 73 of 194. **As predicted, fights are shorter (both sides hit about 11% harder) and where the damage lands barely moved.** The yardstick retune waits for Wave B (one retune, not two).
3. **Wave B: built (Nov 24).** D2, D3, D4. `data.COMBINED_STAT` (MAT is ATK, MDF is DEF, in the new game: `Unit.stage`, `counter_name`, `push`, `counter_value`), `SHORTHAND` (Feared: Reeling and Sundered; Cursed: Sundered and Poisoned; Venom: Poisoned and Bleeding; parts scale with the stacks), `HOLDS` (Disarmed: offense at −3 for 3 rounds, harmful; Steadfast: DEF where it is for its stacks' rounds, helpful) and `HOLD_ROUNDS` (Gyllenlykt holds EVA at its printed +3 for 3). `Battle.hold`, `release`, `release_all`; `push` refuses a lowering push on a held stat; a hold on a held stat fizzles, aimed (`capped`) or landing (Joseph's heads-up: Cover, rows, two Disarms), never refreshes. Holds tick like ailments, lift on expiry, Skolja (harmful), a fall, and a new fight. No stat staircase in the new game; a new fight washes stats. Steadfast no longer stops Late or shoves. The AI: the weakness tempo bonus scaled by the chance not to graze (Joseph's review); counters and holds valued through the same paths. The Lab shows holds as badges with rounds. Glossary and audit updated (Waxing, Waning, Hexed, Warded retired). Tests: `test_status_rules.py` (persistence, combined counters, a clean new fight, the old staircase kept; shorthand; holds: Joseph's three Disarm cases, rounds, no second hold, Steadfast, Gyllenlykt, Skolja), `test_wave7a.py` (Joseph's hero-side Advance check); 413 pass; old fights identical.
   - **Measured** (150 mirrored rooms a kind, Dagskald, Skurmar, Vasara at leg 2; Wave A / Wave B): Elite won 98% / 100% in 6.8 / 5.9 rounds, end HP Vasara 39% / 29%, Skurmar 69% / 71%, Dagskald 89% / 92%; **Boss won 94% / 88% in 9.9 / 6.0 rounds**, Vasara 34% / 26%, Skurmar 59% / 52%, Dagskald 77% / 77%. The gauntlet (the AI's floor): Elite cleared 73 of 194 / 58 of 186, Boss 13 of 73 / 4 of 58.
   - **Why:** both sides' stat changes now last. Heroes Sunder foes constantly (492 Sundered landings in 150 Elite fights, mostly Brakrosh): fights are shorter. In boss rooms, foes' **generated shorthand moves** now leave permanent Sundered on heroes: the Forndjur's Merogn (Feared 2: Sundered 2, kept) 114 times in 150 fights, the Forndraugr's Jattenid (Cursed 3) 32, the Fornbein's Ogn 27; heroes end boss fights at DEF −0.81 on average. This is the "foes don't pay costs" footgun (Part 3 note under D11), arriving on the old generated boss kits. Against Joseph's damage picture the calibration rooms moved **toward** it (Elite: the tank near 25-30%; Boss: the tank ~25%, a second hero ~50%), while the AI-played gauntlet got harder.
   - **Joseph's review of Wave B (Nov 24), fixed:** holds drawn on the board (a tag and rounds left under the counters, red when harmful) and on the Inspect card; `held` and `unheld` narrated; `legal` doesn't offer a pure hold (Disarm, Steadfast) at a held stat (Gyllenlykt, a heal, still aims: its heal matters); the dead, the down and the piled carry no holds, and the round's end ticks only the living (`gauntlet.settle` clears them too); a shorthand that can't land says nothing; a stat move says when a hold blocks it; the AI values a raising hold (the sign fix); the retired names left the page. Tests in `test_status_rules.py` (`WaveBReview`); 422 pass; old fights identical.
   - **D11's floor, built:** `DEFAULT_WANT` 1 and `Battle.wanted`: a foe stops lowering a hero's stat once it's at the foe's want (its `wants`, else 1), shorthand counted by its stat parts (Joseph: so a Fear isn't recast for its Late alone); a counter rider adds no extra value there either. Heroes' AI untouched.
   - **What the want showed:** almost nothing moved (Sundered landings on heroes in 150 boss fights 212 to 194; Boss rooms the same). **The bosses weren't spamming.** The Forndjur's Merogn lands about 0.8 times a fight, but a Mer Fear puts Sundered 2 on a hero in one cast and a Jatte Curse Sundered 3, past any want, for the rest of the fight. That is D2 working as designed (a boss's big debuff turn lasts), and the answers exist in the rules (Fortify pushing back, Lonnskolja, items) but **not in the leg-2 kits the gauntlet and the calibration rooms use** (the Vasara carries no Aukskold, the Dagskald no Lonnskolja). So the open question moves to the kits: hero kits carrying an answer (Wave C re-checks kits), and boss kits' Mer and Jatte shorthand sizes (the enemy pass).
4. **Wave C: built (Nov 24).** D8 and D9's Rest. Meditate isn't universal (`can_meditate` is False); **Anda** is a found verb (13% of max MP now; `ANDA_SHARE`, the AI's unit for MP) and **Djupanda** is its byname with Bid (the Bid manner scales a windfall's amount: x2.6, about a third; the Brennumar's leg-3 kit carries it); the Waterfall Rune stays planned. **Lak** 75 for 12 MP; **Gyllenlykt 20** (Joseph's number) through one new data field, `rider_price` (a verb may print its rider's step as a flat price instead of a doubling; O3 may generalize it). Song heals follow Lak (about a quarter less; `KVAD_SHARE` can restore them). No Halv filled in (`build_hero`); test heroes pack their Halv explicitly. The knots: three held, `KNOT_MP_ROUND` (4% of max MP, 4 of the Skurmar's 100, under a Blast's 6) at each round's start; `recovery` no longer deepens a breath; `knot_hold` prices the trickle; Knyta's text. `engine.rest` (D9): 2/3 of HP and MP back (`REST_SHARE`), Wounded heals with its whole pools restored (stored when it's cut: Joseph's pre-flight catch), the Dying stand, the dead stay dead; the gauntlet camps before the Boss (everyone rests). **Kits answer a lasting debuff:** the leg-2 Dagskald carries Lonnskolja. The AI's stat moves (Joseph's pre-flight): lifting a drop scores most, each step above zero less. Carved manners spell in one order whatever order they're carved in (the workbench already did; `Tungbideld`). Tests: `test_wave_c.py` and updates; 426 pass; old fights identical.
   - **Measured** (Wave B fixes / Wave C; fresh rooms, Dagskald, Skurmar, Vasara at leg 2): Elite 5.9 / 5.6 rounds, Vasara 29% / 24%, Skurmar 71% / 70%, Dagskald 92% / 92%; Boss won 89% / 91%, Vasara 26% / 24%, Skurmar 53% / 48%, Dagskald 77% / 79%. **The gauntlet** (the AI's floor, carrying HP and MP through four rooms): Regulars cleared 187 / 175 of 240, Elite 60 of 187 / 36 of 175, **Boss 4 of 60 / 18 of 36** (the camp before the boss). Sustain is now the run's problem, as D8 meant: the Elite room, met with no Rest since the start, is where runs end.
   - **What the AI does with it:** in 150 boss fights the Dagskald casts Sol 962 times, Lak 22, Lonnskolja 30; heroes still end boss fights at DEF −0.7. The answer is in the kit now, but the AI values lifting a lasting drop like a passing one (half a reference hit a step). Under persistence a lift is worth the rest of the fight: the brains' job (valuing a cleanse by the fight's remaining rounds), noted for the pilot.
- **The Lab's run (Nov 24, Joseph):** a gauntlet you play. The Run panel: a place, the adds (+2 Trash or Regular in every fight room but the Regular one, which has its own two), a run number (room i of run n is rolled from `Random(RUN_SEED + 10n + i)`). Trash, Regular, Elite, a camp (each hero Rests or not: D9's screen in miniature, carving waits for the dive), the Boss; HP, MP, the pouch, Wounded and the dead carry. Each room's record carries the party as it walked in (`carry`), and `replay.py` rebuilds it: every room replays exactly. `settle` moved into the engine (one rule for the gauntlet and the Lab). `test_lab_run.py`; `checks/s_run.py` plays a whole run in the browser.
- **Wave D: built (Nov 24).** D13: the fuse (Poison 12 / 6 / 2.4%, Bleeding 14 / 7 / 2.8%, capped at a clean Krosh), one clock, Bleeding bites on action, Withered as Aska's twist, the Curse back on its own moves, the AI's fuse and Withered values, Lak's numbers in the log. 441 tests pass; old fights identical (regress 3bdf6771deb1, fingerprint 288, golden 4535).
   - **Measured** (Wave C / Wave D): the gauntlet's Regulars cleared 175 / 193 of 240, Elite 36 of 175 / 50 of 193, Boss 18 of 36 / 24 of 50 (after the review's fixes and the cap on the top: 195, 50, 26). Calibration rooms: Elite, the Vasara ends at 24% / 27%; Boss, Vasara 24% / 26%, Skurmar 48% / 50%. **The Regular room stops being a run killer** (Aska no longer leaves a lasting Sundered); the Elite is still where runs end.
5. **The Beinar pilot resumes** (Nov 24: step 1, Cover, built: D10; step 2, the kits, built: beinar_pilot.md "Step 2, built"; step 3, the brains, built Nov 25: "Step 3, built") (beinar_pilot.md, "What the build needs"): D10 intercession, the kits, the brains and team plans with D11's wants and the reset as Stabilize; then the gauntlet against Joseph's damage picture and his calibration fights *(scope calibration here to Leg 1, or pull O3 rider/`Gyllenlykt` costing ahead of Leg 2–3 calibration so Legs 2–3 aren't tuned twice)*.
6. **Then:** the enemy pass (O6), tile paint (O4), costing (O3), the Hunt clock (O5), and progression (Part 4: the Growth view, the Vasara and Brennumar webs).

Each wave: old fights byte-identical, the tests, the gauntlet and sweep before and after, the Lab republished, then Joseph plays. D1 and D2 land before the brains because the brains' valuations and the calibration read them.

---

## Sources

- The IDE design record: `battle_system_adr.md` on branch `docs/battle-system-adr` (commit 45a623d), kept there as history.
- The review: this conversation, Nov 23-24 (Joseph and Claude).
- Superseded rules, by pointer: classes.md (Sundered's decay, Gyllenlykt's Evasive, the Skurmar's Meditate knots), beinar_pilot.md Part 1 (the stat staircase, bundles as statuses), pillars.md (Meditate as universal), refactor_plan.md Phase C (heals at 1.2).
