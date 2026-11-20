# Project Notes

A roll-up of the project as of November 7, 2026. The design lives in four specs: **spellbook.md** (what's possible through magic and skills), **bestiary.md** (the enemies), **combat_spec.md** (the fights), and **loop_spec.md** (the city, the day, the Gate, money). The working engine lives in **sim/**, the art in **art_res64/**, and the tools that made the art in **art_work/**.

---

## Where We Are

**The game, in one breath.** A long-settled Norse-tinted city with an English love of paperwork, and one wild thing left: the Rune Gate, which opens on monsters and treasure when spoken to with three runes. You're a new diver with a licence on credit (10,000 marks), recruiting hirelings in the Inn and the Tavern, learning rune words from rumours, taking one-dive contracts, and paying the Board's collector every seventh day.

**The fights (built in the sim).** SMT-style affinities and Bonus Rounds; a 3×2 board with protection and reach; speed groups; a martial grammar (Skar, Kross, Spett, Skott) with manners (Snar, Tung, Bid, Jarf, Drif) and a word compiler that builds and scores every word; rotation, Cover, and painted spots; the Mogel chain, the Draugr crawl, the Bein pile. A fight streams out as events (sim/events.md) for the front-end. 56 tests pass.

**The enemies.** Ande (spirits), Mogel (slimes), Draugr, the Beinar (by job: Beinbryn, Beinorv, Beinseidr), Drattr, Djur, the Oskorei. The encounter composer rolls packs by habitat (Barrow, Wildwood, Rapids) with a ranged toggle.

**The art (Resurrect 64).** The side wizard (17 frames, Joseph's animation), Ande and Mogel in every element and size, the Barrow's undead (Draugr ladder in three tints and sizes, Joseph's four Beinar starters, the Hunt archer), martial hit effects (Joseph's slash, crush 2, pierce 2, and a coded slash), dungeon walls, floors and Cainos dressing, the font and text box. Board mocks of the Barrow.

**Context.** ISEKAI, the earlier Company crawler, was lost when both backups failed. Its design decisions survive, and this project could become its continuation. **Keep backups:** the whole project is in project_backup_2026-11-07.zip.

---

## How We Got Here

1. **The spark:** a video on the morphemes in SMT and Persona spell names. The idea was to build the same kind of grammar from Old Norse, Germanic, PIE, and Uralic roots.
2. **Schools:** four elements, each with a child element, plus a Light/Dark pair. The school is what you study; the element is what the spell does.
3. **The Swede test:** Swedish friends reviewed the names. That locked the roots, the tier ladder, All-, and the spelling rules.
4. **Element personalities:** each element turns different knobs (power, efficiency, variance, spread, rider).
5. **Characters:** a character sheet from an earlier game supplied genes, Personality, Star Sign, attributes, and stages.
6. **Affinity:** SMT's ladder minus Repel, the two cycles, and tempo on weakness, which became the Bonus Round.
7. **The zodiac:** 4 × 3 elemental pairs gave exactly 12 signs, then a naming pass across the language quarries.
8. **Classes:** a 12-class martial grid condensed to 6; 6 casters named for their jobs.
9. **Battle economy:** loadouts, gear rules, free Halv spells, and HP costs for martials.
10. **Effects:** stat lines, status roots, the status list, Helvad, and Lokavad.
11. **Game modes:** the loadout RPG, card battler, and auto-battler; Erfi as a rite; Communion parked.
12. **Encounter v0:** genes to stats, the damage formula, Graze/Hit/Crit, riders, and healing.
13. **Sim v0 and v1:** the first run showed short, deadly fights; the second pass tuned HP, crits, and training.

---

## Design Principles That Emerged

These came up repeatedly and now act as rules of thumb:

- **Name the job, not the element.** Class names avoid spell roots.
- **The Swede test:** a Swedish speaker should hear a name and think "that sounds right."
- **Parents are pure; children carry riders.** Every child element counters its parent's predator.
- **Riders are chancy bonuses; dedicated lines are the reliable version.**
- **Free means plain damage.** Free spells never heal, never apply statuses, never kill outright.
- **Signature weapon moves can never be learned,** so "crazy move or better stats" stays a real choice.
- **Bonus Rounds are outside time.** Only numbered rounds tick durations.
- **DEF and MDF control damage; ACC and EVA control consistency and tempo.**
- **One roll decides Graze, Hit, or Crit.** Nothing misses outright.
- **Measure everything against an average person.** Good HP is +20%; a decent armor is worth about one stage.

---

## Things Learned

**From the design work**
- **The math produced the structures:** 4 × 3 elemental pairs make exactly 12 signs, and 3 × 2 martial pairs make exactly 6 martial classes, mirroring the zodiac's martial half.
- **Tiers double as level scaling.** Fixed costs per tier against a growing MP pool make old spells cheap and your top tier always expensive.
- **Stages compound.** Two cheap single-stage buffs nearly double a fight's length.
- **ACC and EVA stages barely move damage** (about 5% per step), which is why they became the consistency-and-tempo family.

**From the sim**
- **The skeleton holds.** Declaring, turn order, affinity, the cycles, and Bonus Rounds carry a full fight.
- **Training has more leverage than genes.** Because damage is attack ÷ defense, every trained point raises damage directly. Two points per level more than doubled win rates, so the default is now one.
- **The original HP made fights 2–3 rounds long,** with characters dying in round 1. HP ×2.75 brought fights to about 7 rounds.
- **Crits as Bonus Round triggers made Bonus Rounds nearly constant.** With crits removed, they still come about once every two rounds, from Weak hits alone.
- **The original tier powers let Ur one-shot an equal,** which led to the compressed powers (10 / 20 / 28 / 38 / 50).
- **A healer is the strongest class in a party of three.** Dagskald tops nearly every run.
- **MP now matters.** Casters finish fights with about 12–15% MP left.
- **Most people are lumpy.** The median gap between a person's best and worst attribute is 13 at level 1, growing about half a point per level (66 at level 100 before class tilt, 114 with it).
- **Split-stat classes are never anyone's natural best fit.** A single great gene beats the average of two, so Hersir and Huskarl are made from well-rounded people rather than born.
- **CON, SPD, and WIL have no class that uses them as a main stat.** They help everyone instead.
- **Odd births produce about four-fifths of a natural fit's output,** whatever the class tilt. Duds are real but modest.
- **Anything that moves points into an attack stat is power creep.** The 50% class tilt raised party output by about 27%, so HP and creatures had to be retuned (HP ×3, creature growth 0.45).
- **A 6-slot pack of full-strength spirits is twice a party of 3** (six actions against three). Making each slot "half a hero" (HP and MAT ×0.5) gives fair fights.
- **Boss fights are much harder than swarms:** at level 30 the party wins about 83% against swarms but 45% against packs with a Drott. Healing matters most in boss fights; Dagskald wins 72% of them while most classes win 33–48%.
- **Spirits only have elemental affinities, so martials never hit a weakness.** They earn no Bonus Rounds and deal about half a caster's output against spirits.
- **Complementary families work as designed.** At level 30, Slash classes (Hersir 61%, Huskarl 69%) and Brennumar (72%) shine against Draugr; Crush classes (Vasara 61%) shine against Bein; Dagskald's Sol is strong against both. Matching a weakness is worth roughly 20–40 points of win rate.
- **The Bein are the hardest family** (40% at level 30), because they resist two of the three martial types.
- **The Drattr completed the martial triangle.** At level 30, Ullar wins 69% against them (4.6 Weak hits per fight) and Lundar's Jord 73%. Pierce classes finally have prey.
- **Dagskald's lead is partly matchup.** Against the Drattr (no Sol weakness), it drops to 54%, below several classes. Its dominance elsewhere comes from undead being weak to Sol.
- **The Oskorei escalate as designed, maybe too steeply.** At level 30, the party wins Tier 1 100%, Tier 2 93%, Tier 3 31%, and Tier 4 32%. Tiers 1 and 2 are tutorials; Tier 3, the reverse mirror, is the real wall.
- **Found and fixed a sim bug:** when a unit couldn't afford its chosen move, it fell back to its first move and cast it for free, even if that move cost MP. Spirits and enemy casters were getting free spells once dry. The fix made spirits too easy (88%), so the Ande got their own settings (MAT ×0.65, MP ×2). Physical families weren't affected.
- **Halv fodder was a quarter of a hero, not half.** Raising Halv HP to half a hero (and giving every rank an All move one step up) made fodder harder to clear but not more dangerous: Tier 1 of the Hunt is still won 99% of the time, because fodder's damage didn't change. Random family packs got about 5–10 points harder overall.
- **Fodder threat comes from the body, not the move.** Halv-rank enemies now keep Halv moves but have doubled STR and INT. That turned Hunt Tier 1 from a free win into a warm-up (99% → 85% at level 30, 68% at level 10) and smoothed the ladder (85 / 67 / 33 / 28%). Random packs got harder too (30–45% at level 30), so overall difficulty may want easing.
- **Balance bodies by value, not by raw numbers.** The first family bodies cancelled their pluses and minuses one-for-one, and the Draugr became much harder (43% → 26%) while the Bein became much easier (29% → 54%). SPD is cheap in this turn order, and DEF or MDF only stops half the threats. Weighting HP and attack at 1, DEF and MDF at 0.5, and SPD and WIL at 0.25 brought the families together (34–44% at level 30) while keeping their shapes.
- **SPD now shifts the Graze roll** (every 25% faster is ±1 net stage, capped at ±2). That made SPD worth about half a point in the body math instead of a quarter, so the Draugr (slow) got more HP and the Djur (fast) less. Families sit at 33–46% at level 30, with Djur fights the shortest (median 4 rounds, 3 at level 60).
- **Cleanse is rarely worth casting** (about 0.03 casts per Drattr fight), because the party inflicts few statuses. It will matter against status-heavy parties.
- **The Seidar recovered** once Sol-school spirits existed to hit (39% → 54% at level 30).
- **The board's party edge is protection, not missing AI** (Nov 7). Rotation and Cover moved win rates by about 3 points; letting melee reach the Rear erased the edge. One ranged unit in a pack doesn't undo it either: what counts is the share of a pack that can reach the Rear.
- **The sim AI can't see tempo.** Tung (late, heavier) looked strong and Snar (first, lighter) weak only because nothing punishes going last or rewards going first yet; both were trimmed (×1.2, ×0.9) until the AI can.
- **Bid had to cost two rounds to mean anything.** With the next round free it was just a late attack; locked for a round, it needs ×2.6 to break even with two plain hits.
- **The Barrow's folklore rules cost the party 10–14 points** (crawl, pile, guardian Cover), landing the Barrow near its pre-board targets.
- **The test setup can masquerade as balance.** Creatures that gained DEF but not MDF made martials look much weaker than casters, and a creature set with no Natt or Aska weakness made the Seidar look broken. Check the harness before blaming a class.

---

## Things to Test

- **The Seidar:** add creatures weak to Natt or Aska, and teach the AI to value curses. The Seidar is last in every run.
- **Oskorei tuning:** Tiers 1 and 2 are trivial and Tier 3 is a wall; Jakthund could become 2-cost Djur in Tier 2, or Tier 3 could lose some HP.
- **Who uses Bann and Skolja on the party side:** both exist only on enemies so far (Seidar and Dagskald are natural candidates).
- **Fight length at level 10 against Ande** is long (median 13 rounds).
- **Undead fight length and difficulty:** undead fights run about 5 rounds and are harder than spirit fights; the Bein may resist too much.
- **Drott cost:** whether a Drott should cost more than 3, or have less HP, given how hard boss packs are.
- **Recruit-board frequency:** Dagskald shows up in about 15% of recruits because no other class feeds on WIS, while Hersir shows up in under 6%.
- **A Bonus Round cap:** one entry per side per round, compared with the current rule.
- **Level drift:** fights run about 8 rounds at level 10 and about 5 at level 60.
- **All- variants:** only ×1.5 cost / ×0.75 power is implemented; ×2 cost at full power hasn't been run.
- **Stage stacking:** whether a cap on combined stages is needed.
- **Null and Absorb:** the Bonus Round rules are in use but not confirmed.
- **Hersir and Nalarbani survival:** whether HP costs leave them too fragile.
- **Star Sign attribute pairs:** currently placeholders; measure their effect once designed.
- **Genes:** compare gene-0 and gene-31 recruits directly.
- **The AI:** a quick turn-evaluation method (n-ply lookahead if needed) so it values statuses and healing sensibly.

---

## Things to Possibly Tune

| Knob | Current value | Watch for |
|---|---|---|
| HP multiplier | ×3 | Fight length (target about 7 rounds) |
| Level factor | 0.6 + Level/20 | Drift in fight length across levels |
| Tier powers | 10 / 20 / 28 / 38 / 50 | Hits to down an equal |
| Tier MP costs | free / 8 / 16 / 32 | MP left at fight's end |
| All- | ×1.5 cost, ×0.75 power | Area spells dominating |
| Element multipliers | Eld ×1.15 power ×1.25 cost, Vatn ×0.75 cost, Jord ×0.70 cost, and so on | Class spread |
| Rider chances | 20 / 30 / 40 / 50% | How often statuses appear |
| Status-line chances | 50 / 75 / 90% | Whether status classes pull their weight |
| WIL contest cap | ×0.5 to ×1.5 | Status reliability |
| Poison and Bleed | 8% of max HP | DoT relevance at the new HP scale |
| Healing | 1.5× a base hit | Healer dominance |
| Graze / Crit base | 20% / 5% | Feel of rolls |
| Gene growth | 0.6 + gene/50 per level | Recruit quality |
| Personality | ±20% growth | Birth-sheet impact |
| Star Sign | ±10% of highest attribute | Birth-sheet impact |
| Class tilt | 50% | How far a class reshapes a body; power creep |
| Class fit exponent | 9 (about two in three natural fits) | Share of odd births; recruit-board variety |
| Training | 1 point per level | Leverage over genes |
| Creature growth and strike power | 0.45 per level; Power 16 | Difficulty (not balance) |
| Enemy HP and damage scale | HP ×0.5; physical families' STR and INT ×0.6 (×0.5 before the board) | Fairness of a 6-slot pack; comes down if packs gain reach |
| Manners | Snar ×0.9 +1 group; Tung ×1.2 −2; Bid ×2.6 over two rounds; Jarf ×0.7, ×1.5 cost, 25% crit at ×3; Drif ×0.5 a hit, coin-flip chain to 4; a manner on Halv costs 4 | Each within 2 points of plain |
| Painted spots | ×0.5 on landing, ×0.5 a round for 3 rounds | Mogel fights |
| Barrow rules | Crawl at 35%; pile 2 rounds, back at 50%; guardians cover under 50% at ×2 | Barrow difficulty |
| Ande MAT and MP | MAT ×0.65, MP ×2 | Spirit fights (pure casters) |
| Enemy Ur cost | 48 MP | Oskorei leader difficulty |
| Halv body | ×2 STR and INT | Fodder threat |
| Family bodies | See bestiary Part 1 | Family feel; the value weights are estimates |
| Speed shift | ±1 stage per 25% faster, cap ±2 | Value of SPD |
| Spirit rank HP | 0.6 / 1 / 2 / 2.5 / 3.5 | Boss vs. swarm difficulty |
| Encounter budget | 6 slots | Difficulty |
| Helvad chance | 25% base | Death magic's sting |
| Mogel re-form share | 35% of the smaller body's HP | Mogel fight length (12 rounds at level 10) |
| Mogel body | HP 0.95, SPD 0.8 | Pays for the chain's extra lives |
| Composer faces and weights | Uniform among the faces that fit | Pack size and boss frequency |

---

## Places Left to Go

**Done on November 7** (details in the specs)
- Speed groups; the board; the martial grammar and manners; the word compiler; Swap, rotation and Cover; the retune (the board's party edge is protection, so physical enemy damage is ×1.2); habitats and the ranged rule; the Mogel's slime paint; engine events with intents and reasons; the Barrow rules (crawl, pile, Beinar jobs, element Beinseidr); the loop designed (loop_spec.md).
- Art: the undead converted and laddered, Joseph's Beinar starters, the martial hit effects at tuned cadences.
- **Nov 8, death:** Dying with 5 breaths (one a round, one a hit), Wounded (−25% max HP and MP, cleared by Rest), Dead (Mead or Mervakna); the Vakna ladder split between the Dying and the Dead; the Surgeon's Kit (as Halvakna); the City Infirmary for a main character who comes home dead (a fee, or onto the loan); dead hirelings away a week; healing between fights.
- **Nov 8, settled:** the toll (25 at grade H, rising with grade), wages (40 a dive, the same again at Midnight, bartered loot with no change given), Scry (a tick to enter, each summoned paid their day's wage up front), Carve Runes (one rune per stat, +5%, one choice per rest room), the slice's eight runes and the specials' modifiers, recruit levels (a ramp, then 2–3 behind), the late fee (10%), Wounded held (heroes are Down or Up; no deaths in the slice), a wipe (lose the dive's loot, wake Up).
- **Nov 8: loop_spec v2.** Licence 20,000 marks at 400 a week (about a year, not meant to be finished in the demo); money anchors (a fight 25, a Life Draught 50, the worst weapon 100, lodging 30); three legs of five rooms (fight in, three of chance, elite out); rest rooms with Rest, Organize, Carve Runes; the Midnight negotiation with hirelings; per-hero 3-slot Pouches, the Haul, the Quest Ledger; Norse-flavoured English items and the Diver's Supply; a Register of eleven at the start plus two recruits a day; two specials of the day; the Trainer's arc and a challenge arc for the demo; the barest slice (loop_spec Part 13).
- Decisions: the front-end is **a browser page published as an artifact** (engine via Pyodide, canvas), shareable by link. The day has **seven ticks**, and Rest ends it. The slice's spine is **the licence debt**. Jordkross and Blastskar are patch spells, not a blanket rule.

**The build order** (Joseph, Nov 7)
1. **The end-to-end fight in the browser:** the board, sprites, the text box, the turn bar, intents with hover prose, commands, hit effects, all driven by the event stream.
2. **Rooms and the animation around fights:** walking in, the shift into the board, the victory cheer, loot.
3. **The dungeon assembler:** combinatorial rooms, hooked to the Rune Gate. This is the real test: if it works, a lot follows.
4. **The city loop** (loop_spec Part 11): the Inn, the Tavern, the Town Square and its Board, the Gate, fourteen days.
5. **Packaging.**
Art comes in between, wherever the build needs it ("a skeleton crew").

**Loose ends (started or promised, not finished)**
- ~~Engine work before the browser fight~~ done (Nov 8): fixed unit ids; items as moves; Dying (5 breaths), Wounded (−25% max HP and MP), Dead; the Vakna ladder; Surgeon's Kit and Mead of Waking; finishing blows weighed by breaths left.
- **Dive difficulty:** the sim's family tuning is for comparisons (25–55% single-fight wins). A ten-fight dive needs about 90% per regular fight and 70% per elite; set it in the dungeon assembler (pack budgets, levels). Without a revive in the party, about half of falls end in death; a full pouch is worth 20–26 points in a fight.
- **Beinar animations:** Joseph's four Beinar are idle frames only. The fight needs at least attack, hit and down for each, or the skeleton sheet's frames with weapon overlays as a stand-in. *Blocks step 1 for the Barrow; Ande and Mogel can carry the first fight.*
- **Jordkross:** written into the spellbook (Proposed), not in the sim. Until it is, Rear bone piles almost always stand again.
- **Taunt** isn't in the sim; Cover and Taunt names (Skydd, Eggja) are pending.
- **Enemy Mark-bid wind-ups:** none yet (the Mogel's paint is Mark without Bid).
- **Shared move definitions:** enemy moves moving onto the hero words with English display names, done for new moves, not for the old enemy lists.
- **The Hunt:** the archer is converted; the Hunt's pack, its clock, and its Oskorei kits for the Barrow aren't wired together.
- **The damage knob** (SPIRIT_DMG_SCALE 0.6) stands in for enemy reach; revisit once packs lean further toward reach.
- **AI blind spots:** it rarely spends Crush on piles, doesn't value going first (Snar) or punish going last (Tung), and doesn't react to wind-ups beyond Defend, Cover and Swap.
- **The Rapids with ranged excluded** roll six Halvdrattr: needs a rank or budget rule if used.
- **Effects:** the defend ring is small for a body; the coded slash's tip is flat; white effects may vanish on white bone (a 7f708a outline is the fix if it shows).
- **Beinseidr orbs** read weakly in Aska, Blast and Reyk.
- **Later, not forgotten:** the JSON export of data tables and the Godot port spec; the room art stock-take; 48 and 64px walls; the chest animation; back sprites; Elder or Younger Futhark for runes.

**Art the build will ask for** (Joseph)
- Beinar attack, hit and down frames; the Gandraugr casting pose; a boss (the Stormogel or a Draugr Drott).
- Room pieces: wall caps, the exit props (open edge, iron door, gilded door, crack, stairs), the rune glyphs and the gate screen, the map screen, intent icons.
- For the city: one header picture per place (Inn, Tavern, Town Square, Gate).
- Insect glue creatures; the Surtland goals below.

**Next up (sim)**
1. Fix the Seidar test conditions (creature coverage and AI curse valuation).
2. Try the Bonus Round cap.
3. Smooth level drift.
4. Improve the AI's turn evaluation.

**Design**
- The loop's numbers (toll, lodging, wages, installments, contract pay), how far behind you recruits roll, what Scrying and a wipe cost, the slice's rune set and first rumour seeds (loop_spec Open Questions).
- Later spines: licence grades as guild rank (H up to S), crafting, a story.
- Class trees: which spells, skills, and lines each class gets.
- Martial skill families beyond Blot, with HP-cost ladders.
- Party size: you plus two hirelings for now (it may chafe that a third of the party never changes).
- Star Sign attribute pairs.
- Whether stat stages last the battle or expire.
- Status cures and items; gear beyond weapons.
- Whether the Berserker can pay past the HP limit.
- Repel as a possible sixth affinity step.
- A Sámi speaker's check on the names.

**Art goals: the Surtland (the Eld area; draft)**
- Basalt-column wall module (hexagonal columns), from the warm-stone recolor.
- Lava seams: the crack decals in the flame ramp (f79617, f9c22b), with a 2-frame glow.
- Ember light pools (the existing light pool) and drifting embers (a recolored bdragon effect).
- Slag heaps and cooled-lava props; charred, torn banners (banner_torn, recolored).
- A brazier or forge prop; obsidian shards (Natt ramp with a bright spec).
- A landmark for the boss room: a giant's flaming sword driven into the floor (Surtr's).
- Creatures: Eld and Reyk Mogel exist; Joseph's insect glue (ember beetles, ash moths) would fill the gaps.

**Art (paused)**
- The wolf and snow leopard face swap (a feline howl and a wolf crouch).
- School recolors for the animals.
- Menu screens using the watercolor backgrounds.

**In the pocket:** Smed, Sten, Skog/Skogar, Drengar, Regin, Tapio, Blodsbroder, and the six pocketed martial classes.

---

## Files

| File | What it is |
|---|---|
| combat_spec.md | Combat spec v1, the build-to for the slice: the round, speed groups, the board, reach, Move/Swap, protection, Skott, revive, items, Flee, enemy rules |
| spellbook.md | The rules, and every move in the game (Parts 1–10, ending in the Move Catalog) |
| bestiary.md | Every enemy family: ranks, kits, affinities, lore, stat blocks, and sim results |
| sim/catalog.py | Regenerates the move catalog and stat blocks from the data |
| sim/data.py | Every number and table the sim uses |
| sim/engine.py | The battle engine |
| sim/run.py | The runner: `python3 run.py [fights] [hp_mult] [training] [nolog]` |
| sim/roster.py | Rolls recruits and shows the population: `python3 roster.py` |
| sim/run_spirits.py | Party vs. spirit packs: `python3 run_spirits.py [fights] [hp_scale] [dmg_scale] [nolog]` |
| sim/run_families.py | Party vs. each family (Ande, Draugr, Bein, mixed Undead): `python3 run_families.py [fights] [nolog]` |
| sim/out_families.txt | Family results, with a logged undead fight |
| sim/composer.py | The encounter composer: catalog, gates, biomes, rules, placement. `python3 composer.py` prints sample rolls |
| sim/grammar.py | The word compiler: any word to a full move, plus the plain-English enemy name; `python3 grammar.py` prints the assessment (out_grammar.txt) |
| sim/manner_check.py | A/B: martial root skills swapped for each manner: `python3 manner_check.py [fights] [level]` (out_manners_10.txt, out_manners_30.txt) |
| sim/rotation_check.py | A/B: the board with and without rotation and Cover, against the no-board targets: `python3 rotation_check.py [fights]` (out_rotation.txt) |
| sim/board_decomp.py, sim/knob_sweep.py | Which board rule makes the party edge, and how big a knob closes it (out_knob_10.txt, out_knob_30.txt) |
| sim/habitat_check.py, sim/paint_check.py | Habitat packs under the ranged rule, board and knob (out_habitats_10/30.txt); slime paint on vs off (out_paint.txt) |
| loop_spec.md | The build-to for the city, the day, recruitment, runes, contracts, the Gate, and money |
| sim/events.md | The event stream a fight emits (`Battle(..., events=True)`): kinds and fields, for the front-end and the port |
| sim/barrow_check.py | Barrow packs with the folklore rules on and off (out_barrow.txt) |
| sim/run_mogel.py | Party vs. composed packs (Mogel, Ande, mixed): `python3 run_mogel.py [fights]` |
| sim/out_mogel.txt, sim/out_mogel_drawn.txt | Composer results, all ranks and drawn units only |
| art_res64/ (and art_res64.zip) | Every sprite in Resurrect 64, in folders, with sheets, previews, mocks; README.txt documents each set and its license |
| art_work/ | The art workspace: tools/ (every converter and mock script; run as `python3 -I tools/<script>.py <art_work> ...`), the extracted sources (ws*/, pack/, bg/), and sources/ (every file Joseph attached) |
| project_backup_2026-11-07.zip | Everything above in one file |
| sim/out_v2.txt, sim/out_spirits.txt | Latest results against creatures and against spirits, each with a logged fight |
| wizard_schools.png | The wizard in all six school colors |
| sol_watercolor_gold.png | The Sol background |
| Wizard_1.aseprite, First_Animals_1.aseprite, five watercolors | The original art sources |

## Fight Lab, Nov 8 (fight_lab_spec.md v3)
- **Engine steps built:** begin/phase/awaiting/options/submit/commit/inspect/preview_order; fight() is the same loop. 320 fixed-seed fights identical to before (regress.py). Fixed: Bonus Round entrants came out of a set (order depended on memory addresses).
- **New:** Flee rolls its chance; retarget/fizzle/flee_failed events; heroes' Guard; Cover in martial slots; Battle letters duplicate names.
- **knowledge.py:** what the Company remembers (affinities per family/rank/element on first hit; HP at 20 kills, MP at 40, per family/rank; once per body).
- **lab.py + fight_lab/index.html:** the lab page, published (Pyodide shipped beside it; stdlib as JSON, zipped in the page). HTML board for now; canvas art is step 4.
- Tests: 92 passing (test_steps, test_knowledge new).

## Nov 8, evening: the Fight Lab screen (roll-up)
**Where we are:** the Fight Lab is published (an artifact) and playable on the real canvas screen. Build steps 1-4 done, 5 mostly done; next is step 6, playback.

**Done today, after the engine work:**
- **Recorder:** every fight saved to the page's own database (seed, party, pack, every order, text log, Joseph's note); `sim/replay.py` replays one exactly. Found and fixed: float seeds hash differently on 32-bit Pyodide (`hash32.py` reads early records).
- **Engine:** the tie coin is flipped once per unit per phase (turn bar is exact; party wins 38.0% -> 39.0% over 4,500 fights, noise); `plain()` writes one line for every move (Joseph's scale: Halv weak, base average, Mer high, Jatte great); player orders carry no AI reasoning; intents carry kind, element, reach, shape, direction.
- **Rules call:** Bein piles left at the end of a fight don't keep it going; loot and walk away (open idea: uncrushed piles rising later in a dive).
- **Screen:** 320x180 canvas, whole-number scale; Joseph's tracker (face chips, gold next, A/B twins); text box keeps its size: moves 2x3 left, utilities 2x3 right (Fight in the sixth slot); clicking a move turns the left half into its card; watercolour fill at display resolution, tinted per area, one crop per fight, running into every notch of the cord.
- **Joseph's art wired in:** the cord frame (every corner as drawn, rearing beasts, knotted bottoms, attached heads for popups; sizes snap to the 4 px twist); 16x16 intent badges on the hover plate and Inspect; 9x9 intent icons in his 12x12 frame at each unit's feet, facing the foe (rust = aimed at a hero, stone = not, blue = a hero's order); magic's sparkle tinted per element (12).
- **Board, roomier:** 44 px cells, one slab between armies, floor lifted 14 px (lanes 24/26/31), the Rear 6 px further back, intents just clear of each body, text box narrowed 6 px a side so its beasts sit fully in frame.

**Next (build order):**
1. **Step 6, playback:** Joseph's hit effects on the target, hit-stop, Draugr falls and Beinar collapses, Move steps, floaters on a rhythm, the tracker sliding chips off as units act.
2. Finish step 5: drag the tracker; Repeat last round.
3. Step 7, check: Auto results on the page vs the sim; a scripted play-through with screenshots.
4. Then the dungeon assembler (dive calibration: ~90% regular, ~70% elite), rooms, city loop.

**Open asks for Joseph (art):** icons 8 (pick?), 10/11 (smash), 14/15/16 (shields, ring), 18 (?: hidden intents?); icons for move/swap, wind-up, flee; the finer period-2 cord (style or leftover?); a 13x13 intent frame if any 9x9 icon looks cramped; hand-drawn 8x8 faces later; Djur and Drattr sprites; martial classes still wear caster colours.

**Files:** `fight_lab/` (index.html, screen.js, assets/, sim/, py/), `fight_lab_spec.md` v3, `sim/lab.py`, `sim/knowledge.py`, `sim/replay.py`, `sim/regress.py`, `art_work/tools/build_lab_assets.py`, `art_work/tools/screen_bg.py`; Joseph's sources in `art_res64/ui/` (cord_frame, intent_icons_9, intent_frame_12, intents 16x16) and `art_res64/backgrounds/watercolor_*.png`.

## Nov 9: icons, playback, step 7 (roll-up)
**Where we are:** Fight Lab build steps 1-7 done. Next: the 32R stand-in mapping (Joseph curates), then the dungeon assembler.

- **Icons:** Joseph's 13x13 frame; melee Pierce = stab; Guard = rune shield; Cover = banded shield; Move/Swap = boot with speed lines; Flee = boot with dust cloud; wind-ups loop the three aura frames; "?" for unreadable intents (not wired yet). The HAL boxes were a loader miss on elided Ande file names (fixed: 24 Ande).
- **Art direction (Joseph, Nov 9):** every creature static, life from code motions; 32rogues (Seth Boyles) shifted to Res64 (`art_work/tools/rogues_res64.py`, one palette map + hand FIX table; sheets in `art_res64/rogues/`) as stand-ins and bases; Joseph replaces over time (Drattr pass 1 in `art_res64/drattr_1.aseprite`).
- **Fight with missing orders:** confirm, then unordered heroes Halv-strike (spread random, `lab.autofill`, recorded). Replaces Repeat.
- **Playback:** the MOTION table in screen.js; effects atlas `fight_lab/assets/fx.png` (`art_work/tools/build_fx.py`); hit-stop on a virtual clock; Space skips.
- **Step 7 check (all pass):** 48 page Auto fights (even levels: party 13, enemy 35) replay natively line for line; 96 random-order fights through the page's Python and playback, every event kind, no page errors, all replay; a scripted click-through (move card, targets, Guard, Move, Inspect, Pouch, confirm, Bonus Round, Dying) replays. Tools: `sim/check_page.py`, `sim/checks/` (s7a/s7b/s7c scripts, records, `playthrough_sheet.png`).
- **Open (Joseph):** once every hero has an order, the menu still acts on the last hero, so one stray click on Flee replaces their order and ends the fight on success. Options: Flee asks first, or the menu lets go of the hero once all are ordered.

## Nov 9-10: 32R art and the Drattr court (roll-up)
**Where we are:** Fight Lab steps 1-7 done and published (version 21). The 32R stand-ins are in for the Beinar (bone-tint ranks: white, aged, red, earth), Drattr pass 1 is in the Lab, and the Mogel are matte (two brightest tones backfilled). Leg 1 of the Drattr court is built in the sim; Leg 2 (the Lab page) is next. Then the dungeon assembler.

- **UI:** long move and item names clip with a "." (the move card shows the full name); Flee's chance at full size, no "%".
- **Jobs and Types:** a rank may carry a job key, so several jobs share one shown name (three different "Drattr"); creatures and heroes have a Type (Martial/Magical); the Type points the family's attack lean ("swap", value-neutral; the agreed ±0.15 "tilt" is a knob: it cost Wildwood 12 points).
- **Enemy move options:** names on any move, row/column shapes with falloff (Skewer 100/50), split hits shown N+M (Twin Slash), Drif on enemies (Swift Strikes), two-stat moves (Feeding Frenzy), MP-share costs (Splash, 3-4 casts at any level), once-per-fight moves and job swaps.
- **Net Throw:** Bound (lose the next action; kills a wind-up), group +1, sure, Cover catches it, once per fight, then the thrower becomes the spear job; the AI values it by the action it cancels and marks targets (no double-taps).
- **The court:** Halvdrattr (Nip, Splash), Drattr (Young, Shield, Swords, Spear, Net), Stordrattr (Angler, Princeling, Mystic), Forsdrattr (Queen). Sprites from Joseph's drattr_1 sheet (20 frames).
- **Data:** Rapids party wins 44% -> 35% at L10, 44% -> 40% at L30 (the Type swap and Splash each about -7 at L10). Left in, to tune by feel once there's a loop. The Queen shows in about half of Rapids fights (the only 3-cost Drattr).
- **Tests:** 113 pass (test_drattr new).
- **Open:** Leg 2 (atlas, per-move frames, the net's fade, Bound swirl in net colours, N+M on screen, chest icon for Net Throw); the net Drattr's spear needs a lighter value; Beinar mage cast pose; Spett, not Halvspett, for the spear (reminder).
- **Nov 10, heroes:** Joseph's 32R picks are the heroes (heroes_1.aseprite), one or more looks per class, mirrored, lying down when Dying. Spearmen (18, 20) banked for a spear class. School uniforms (robe recolours per school) queued.
- **Nov 10, Leg 2:** the Drattr court on the page (sprites by job, move frames for the mystic, princeling, queen and the bone-mage, the net's swap and fade, Bound's green swirl, N+M floaters, the chest as Net Throw's intent); HP bars slide off faces in front of them.
- **Nov 10, range from weapons:** WEAPONS (type, range: Short/Medium/Long); each martial class carries one (Ullar Bow, Nalarbani Stikk, Hersir Greatsword, Huskarl Axe, Berserker Club, Vasara Hammer); a root uses its weapon's range only in its own weapons (ROOT_WEAPONS), else the root's own (Short; Skott is bows only). Enemies: rank or move weapons (Beinar bows, the Hunt's bows and javelins, Drattr spears and trident); teeth, horns and claws are Short. The move card shows RANGE SHORT/MEDIUM/LONG. Fingerprint: Barrow fights without a Nalarbani identical (94/94). Tests: 121.
- **Nov 10-11, the dive map:** dive_spec.md (the tapestry: the Gate as a picture stone, the dive woven as you walk, lots for events; legs, sight 2, spoils woven in, rooms, the icons). The agent's tapestry.py (Res64 + 4: 18141a, 232339, 7a5c40, 717a94) in art_work/tapestry/agent; art_work/tapestry/tapestry_v2.py puts Joseph's icons on it (full colour on the open map, three-tone wool once woven), the longship sailing in, white-only ink outlines, sparse weft dashes, rune-coloured bands (Yr wine, Logr blue, Bjarkan green, Kaun red), the cairn for the fallen. Next: dive.py (the rules), then the tapestry in the Lab.

## Nov 12-20: the game, named (roll-up)
- **pillars.md** (new, Nov 20) is what every spec answers to: a Norse fight-run; a party of three classes as your character (fixed stats, no levelling, three classes unlocked to start); four move slots (two to start) plus universal Defend, Meditate, items, moving and Flee; mutations as forks by default; weapons (family: type and range; skin: stats and maybe a move that belongs to the weapon; rider-only auras); one Talisman per hero; party-wide Omens (elites, bosses, events, the merchant); rewards without a new currency; one shared three-slot pouch; no armor in v1. Words: runes (words, carved), Talisman, Omen, tome, lots.
- **dive_spec.md v1.1:** seven-column legs (entry fight, five route columns, boss), elites optional in the routes (not in the first two), a camp before every boss, one boss per place, the final boss bigger.
- **loop_spec.md:** the city economy set aside; the Company kept as the meta hub.
- **Open:** duplicates in a party; the power level; the starting three classes; the mutation list; the twelve starting kits; Meditate's number.
- **Nov 20, classes.md (new):** fantasy -> verbs -> basic moves; one signature mechanic per class that touches another's. Brennumar locked (Eld, Reyk, Sveda/Scorched 100-50-20 reset by Sveda and flared by wind, smoke Vanish, cash-ins, Aukseid and Djupanda as a Bid-style wind-up). Drafts: Ullar (Pinned; Flokskott, Banskott, Skrida, Aukhitt), Vasara (Cracked, Pierce finds the cracks; Egga, Lya, Brakkross, Aukskold, Hevn), Dagskald (the Song, Kvad: held regen that grows by verse; Lak, Sol, Skolja, Vakna, Aukkraft; first unlock by finishing without a healer).
- **Nov 20, classes.md full pass (all four Locked):** a move is its effect plus one rider slot; upgrade parts (tier ladder Halv/base/Mer/Jatte/Ur, Jatte found, Ur gear-only; Styng adds damage; Lonn adds the designated rider, named by the rider's prefix: Blotskott); two-part cap, named capstones beyond it (Tusensplitter, Pilskur, Hasin, Holm, Skogsbrand); the noticeable-change rule; the reward mix (BREAD plus a build-around); the seam rule (Brakrosh, Aukraft). Brennumar: Reyk and Sveda no-damage. Ullar: Pinned = slowed and rooted; Marked (Peka) = can't dodge; Banskott on Pinned only; Skrida swaps with an ally; Steady dropped. Vasara: Kross -> Krosh; Cracked builds per blow, decays when not struck; Bidhevn. Dagskald: Kvad builds by verse (cap 3, decays unsung); Sol's rider Blinded; Lonnlak cleanses one. Two status shapes in pillars Part 5c: build (Cracked, Kvad) and fade (Scorched; Frozen proposed: lose the next action, then 50%, then 20%, counted in actions, no refreeze, shatter stays). Backups: classes_before_fullpass.md, pillars_before_fullpass.md. Next: the Skurmar, then the mutation session.
- **Nov 20, statuses:** a named debuff is a stat-stage aura (Blinded N = -N ACC; Sundered N = -N DEF, renamed from Cracked; both the build shape); Blinded loses its EVA part (Marked owns can't-dodge). One stat, one named status; side-effect overlaps (Pinned/Chilled SPD) don't stack, the strongest counts. Lonnegga confers Blinded, Lonnpeka Sundered. Frozen: the fade shape on actions (100/50/20), no refreeze, Shatter stays. Bosses immune to Frozen, Stunned, Bound for now.
- **Nov 20, Feeble:** ATK down is the status Feeble (not Weakened: "Weak" is an affinity). Ned moves confer the named statuses (Nedhitt Blinded, Nedskold Sundered, Nedkraft Feeble). Lonnsveda: Scorched and Feeble. Move text names statuses as hoverable keywords.
- **Nov 20, stat counters:** one counter per stat (-3..+3), up and down cancel, decays toward zero when not pushed. Names: Feeble/Mighty (ATK), Sundered/Fortified (DEF), Blinded/Keen (ACC), Nimble (EVA up). Cleansing lifts lowered stats to zero. Marked = the EVA-down counter (Merpeka returns), approved. Hobbled held for a plain SPD-down. Vasara's verb Brace -> Fortify.
- **Nov 20, Skurmar (classes.md Part 7):** the Weather-Witch, pure tempo. Blast (two light hits, flares Scorched), Knyta (ties knots, cap 3, no decay, carried between rooms; holding: Blast up, Blixt can't graze, half a Meditate of MP), Blixt (Stun only on Lonnblixt), Kuling/Storm/Orkan (found untie spells costing knots plus MP), Kasta/Svepa (push/pull; swap and bump; Pinned is a wall), Byr (party Quick). Stats: Slowed/Quick; a counter = own stacks + sources, hover lists sources. Speed-group keywords: First (+3), Swift (+1), Late (-1, proposed), Heavy (-2), Last (-3). Manners combine for groups (Bid + Tung = a Heavy release); wind-ups break only to turn-enders and death.
- **Nov 20, refactor_plan.md:** the code review and the plan to bring the sim to the five classes. Waves: 0 housekeeping (git, a fixed-hero fingerprint); 1 the status engine (pure refactor to an identical fingerprint, then counters and the build/fade/pool shapes); 2 one compiler for every move plus the cost anchors (refactor, then Styng/Lonn/designated riders/cap/capstones/keywords); 3 class sheets, kits, Meditate, Egga, then sweep Layer 1 picks the level; 4 the signatures, each with its AI value; 5 leg scaling and sweep.py; 6 the page. Found: MP is about twice as tight as the 1/16 target today; Taunt has a speed group but no rules; the release is pinned to group 0; riders live on elements (heroes go explicit, enemies keep theirs).
- **Nov 20, git:** the project is a local git repo (main, first commit e181690); the 36 *_before_* copies are in attic/; ignored: Pyodide (fight_lab/py), caches, dotfolders, project_backup zips. Needs a remote (Joseph's GitHub) to outlive this workspace. Class affinities agreed: magicals by school, martials weapon weakness + one authored elemental weakness and resistance.
- **Nov 20, Wave 0 done:** sim/fingerprint.py (288 fixed-party fights, deterministic across hash seeds; baseline 19b3946c in checks/fp_base.sha1; the 20 MB JSON stays out of git). Catches a 0.1 change to SHATTER_MULT at the exact event. GitHub push refused for jensen-117/norse_game (app access); history stays local until connected.
- **Nov 20, Wave 1a done:** statuses are rows in data.STATUSES (duration, reapply, stats/pick, tick, skip, flags, shatter, chain); engine reads them (status_stat, tick_statuses, skips, has_flag). Fingerprint 19b3946c identical; regress.py n=60 identical (02d06c81); 125 tests; Lab copy synced and a Lab fight runs. Pushed to github.com/jensen-117/norse_game.
- **Nov 20, Wave 1b done:** counters (-3..+3, named, cancel, decay when not pushed), Blinded = ACC counter (no EVA), status moves stack by tier, Frozen fades by action (100/50/20, no refreeze, thaw event), bosses immune to Frozen/Stunned/Bound, enemy stat moves push counters. Family win rates unchanged within noise. 135 tests; page Auto 48 fights clean. Fingerprint baseline now checks/fp_1b.sha1. Screen.js narrates immune and thaw.
- **Nov 20, Wave 2a done:** words.py (naming, act, roots, TARGETS/MANNERS/RIDERS, compile_move); every engine builder and grammar.compile_word compile through it. move_golden.py: 4,535 moves and kits identical; fingerprint 8c8e46cc identical; regress identical; 138 tests; page 48 Auto fights clean. index.html SIM list and lab.py engine hash include words.py (the next Lab publish must include it).
