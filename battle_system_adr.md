# Battle System Design Record & Refactor Plan (Meeting Minutes + ADRs)

**Date:** 2026-11-23  
**Scope:** Core combat system (`profile="new"`), move grammar costing, sustain & attrition, tile-paint layer, and the 4-family enemy vertical slice  
**Status:** Proposed — captured from systems review & design alignment session (prior to implementation)

---

## 1. Meeting Minutes & Genre Thesis

### Goal ("The Conversation")
This battle system is an intentional dialogue between **tactical JRPGs** (*SMT*/*Persona*, *Etrian Odyssey*, classic party synergies and folklore bestiaries) and **roguelikes/roguelites** (*Slay the Spire*, *Into the Breach*, *Darkest Dungeon*, *Spelunky*):

* **What it keeps from RPGs:** 3-hero party formation, elemental/weapon affinities, persistent stat tug-of-war, status ailments, Pouch items, and folklore-driven monster families with distinct mechanical rules.
* **What it brings from roguelikes:** Legible enemy intents and turn-order preview, deterministic neutral baselines (no hidden failure taxes), real room-to-room attrition with out-of-battle Rest nodes (`2/3` max HP/MP per hero), 4-slot build-crafting via mutating Norse/Swedish grammar words (1–2 mutating moves per hero + mutated run finds), and an anti-stall clock tied to the world's lore.

### Key Clarifications Captured
1. **The grammar is an exploration & mutation space, not an unrestricted player crafting bench.** Awkward or extreme combinations (e.g., `Allblotskott`) are better expressed as single-use **Pouch items** (*Shrapnel Bomb*), while heroes run tight 4-slot kits that mutate across a run.
2. **Out-of-battle Rest nodes (`2/3` max HP/MP per hero) + Pouch draughts** are part of the intended dive loop (not yet modeled in `sim/gauntlet.py`), which allows healing to be treated primarily as an in-battle / tactical concern rather than an infinite out-of-combat top-up.
3. **Enemies are simpler than heroes by design** — 2–3 focused moves that form team puzzles and subvert the party's default plan. We lock the mechanical stories of the **4 core drawn families (`Beinar`, `Draugr`, `Mogel`, `Ande`)** first before expanding `Djur` or `Drattr`.
4. **Numbers remain testable hypotheses.** Specific spell costs, heal values, and enemy HP deviations will be validated in `sim/yardstick.py`, `sim/sweep.py`, `sim/gauntlet.py`, and Fight Lab playtests once implemented.

---

## 2. Architecture Decision Records (ADRs)

### ADR-01: Model A Accuracy — Deterministic Neutral + Symmetric Graze / Crit Ladder
* **Status:** Agreed
* **Decision:**
  * Accuracy is governed by `net = attacker.ACC - target.EVA` (clamped `-3..+3`, with `SPD` staying out of accuracy):
    * **Neutral (`net == 0`):** `0%` Graze, `5%` Crit, `95%` Clean Hit — mirrored identically for heroes and enemies. Pure status moves land **100%** at neutral.
    * **Ahead (`+1 / +2 / +3`, `Keen` / `Marked`):** `0%` Graze, **`33% / 66% / 100%` Crit** (`1.5×` damage; `Jarf` crit bonus still stacks on top).
    * **Behind (`-1 / -2 / -3`, `Blinded` / `Evasive`):** **`50% / 75% / 100%` Graze**, no full 0-damage whiffs.
  * **Graze effect:** Deals **`50%` damage**, suppresses move riders and `flare`, and **does not earn a Weakness Bonus Round**. Pure status moves fail ("shrug off") when grazed. Non-grazed hits when Behind keep the `5%` base crit chance.
* **Pros:**
  * Eliminates feels-bad 0-damage "off-buttons" and the hidden 20% neutral fail rate on status moves.
  * Every stack `1, 2, 3` scales meaningfully, matching the rest of the counter system.
  * Gives `Blinded`/`Evasive` a distinct job from `Feeble` (strips riders, statuses, and Bonus Rounds, not just raw damage).
  * `5%` neutral crit teaches players organically in Room 1 that crits exist and hints at `Keen`/`Marked`/`Jarf` builds.
* **Cons / Risks:**
  * Removes the visceral "Miss!" dodge fantasy from `Evasive`/`Blinded` (traded deliberately for roguelike reliability).
  * `Blinded 3` (`100%` Graze) blocks pure status moves completely until countered by `Keen`, `Marked`, `Cleanse`, or `Sure`-hit moves (`Blixt` at 2 knots).
* **Why:** Roguelike tactics break down when buttons silently fail at neutral or lock a party into 75%-miss coin flips with no counter drafted. A `50%`-damage Graze floor preserves forward progress while still punishing unaddressed `Blinded`/`Evasive` stacks.

---

### ADR-02: Unified, Fight-Persistent Stat Pairs (`MIT`/`FBL`, `WRD`/`SND`, `QCK`/`SLW`, `ACC`/`EVA`)
* **Status:** Agreed
* **Decision:**
  * Collapse physical and magical stat pairs into unified Offense and Defense counters:
    * **Offense (`ATK` + `MAT`):** `Mighty` / `Feeble` (`MIT` / `FBL`)
    * **Defense (`DEF` + `MDF`):** `Warded` / `Sundered` (`WRD` / `SND`)
    * **Speed (`SPD`):** `Quick` / `Slowed` (`QCK` / `SLW`)
    * **Accuracy / Evasion:** `Keen` / `Blinded` (`ACC`) and `Evasive` / `Marked` (`EVA`)
  * Keep the existing `stage_mult` curve (`+1/+2/+3 = ×1.33 / ×1.67 / ×2.0`; `-1/-2/-3 = ×0.75 / ×0.60 / ×0.50`).
  * **All stat counters persist for the duration of the fight** (no end-of-round auto-decay). Opposing moves cancel step-for-step (`clamp(old + delta, -3, +3)`).
  * **Twinned offense verbs:** `Aukseid` becomes a selfish caster ramp (self-only `Mighty`, candidate `+2` steps); `Aukraft` remains an ally/party `+1` step `Mighty` buff (HP or MP cost depending on the class body carrying it).
* **Pros:**
  * Cuts 14 stat names down to 10 (only 4 core pairs) and stops penalizing mixed martial+magical parties (`Vasara`'s `Sundered` now boosts `Brennumar` and `Skurmar` too).
  * Makes 1-stack setup moves actually pay off over multi-turn fights and turns `Mighty` vs. `Feeble` into a real tug-of-war.
  * Uniform persistence rule across every counter — zero split decay semantics to memorize.
* **Cons / Risks:**
  * `Mighty 3` (`×2.0`) + `Sundered 3` (`÷0.5`) = `×4.0` damage for the rest of the fight; requires Boss/Elite reset counterplay (ADR-03).
  * `Cursed` (`MDF -1` + `Poisoned`) and `Disarmed` (`ATK -1, MAT -1`) bundles in `sim/data.py` need updating to map cleanly onto unified `Warded`/`Sundered` and `Mighty`/`Feeble`.
* **Why:** Classic RPG buffing feels good when setup lasts long enough to matter and helps the whole team. Removing auto-decay makes buffs, debuffs, opposing counters, and `Lonnskolja` genuinely consequential.

---

### ADR-03: Telegraphed, Action-Costing Boss & Elite Stat-Reset Moves
* **Status:** Agreed
* **Decision:**
  * Bosses (and designated Elites) monitor board stat pressure: when **≥3 total debuff stacks** sit on the boss *or* **≥2 buff stacks** sit on any hero, the boss may declare a reset action:
    * Self-cleanse (`Shake Off Hexes` — clears debuffs/ailments on itself), or
    * Party stat-leveler (`Howl Away Might` — resets hero stat buffs to `0`).
  * **Crucial rules:** The reset **costs the boss its turn**, is **telegraphed in intents**, and resolves at **`Normal` or `Late` speed** (never `First`, never a free passive).
* **Pros:**
  * Prevents persistent `+3/-3` stacking from turning bosses into trivial one-shots.
  * Turns boss thresholds into a puzzle: players can deliberately *bait* the boss into burning its action on a reset instead of dropping a haymaker, and still get one final burst round before a `Normal`/`Late` reset fires.
* **Cons / Risks:**
  * Requires careful AI cooldown/threshold tuning so a boss doesn't get stuck in a boring infinite reset loop every other turn.
* **Why:** Borrows *SMT*'s Dekaja/Dekunda tension and upgrades it with roguelike intent legibility so counterplay feels earned rather than punitive.

---

### ADR-04: Sustain Rebalance — Remove Universal `Meditate`, Move `Djupanda` to Run Rewards, Tune `Dagskald`
* **Status:** Agreed
* **Decision:**
  * **Remove universal `Meditate`** from magical hero bodies. Casters meter their MP across rooms using their pool (`100–200 MP`), Spirit Draughts, and out-of-battle Rest nodes (`2/3` HP/MP).
  * **`Djupanda` becomes a run-reward move** for magicals: a clunky **Late `Bid`** (R1 wind-up → R2 Late release for MP recovery). Strong in real multi-round Boss fights where the team protects the caster; risky to loop in Fodder rooms because it advances the Wild Hunt stall clock (ADR-05).
  * **Re-tune `Dagskald`** toward designated support rather than an auto-include heal battery: reduce burst `Lak` healing (candidate ~50% of current `LAK_CLEAN`), leaning harder on `Kvad` (Song HoT), `Aukraft`, `Skolja`, `Vakna`, and the expensive `Gyllenlykt` Pillar of Light (ADR-06). Spread lighter sustain/mitigation across future classes.
* **Pros:**
  * Gives magical classes the same room-to-room resource tension martials already face with HP.
  * Eliminates 90% of the infinite-stall exploit naturally and makes Pouch draughts and Rest nodes matter.
  * Reduces the "Dagskald tax" so healerless parties aren't a trap once Rests are factored in.
* **Cons / Risks:**
  * Without Rest nodes simulated in `sim/gauntlet.py`, gauntlet clear rates for caster-heavy parties will drop until Rests are modeled in the gauntlet runner too.
  * Casters running dry in long Boss rooms must still have a safe floor (`Halv` low-cost attack or Guard/Items).
* **Why:** Free, infinite MP recovery breaks roguelike attrition. Making MP recovery something you *find*, *pack*, or *Rest for* aligns casters with the run loop.

---

### ADR-05: Wild Hunt 3-Strike Diegetic Anti-Stall
* **Status:** Agreed
* **Decision:**
  * Track cumulative **stall rounds** per non-Boss room (a round where no Boss is present and negligible/zero damage is dealt to remaining foes, e.g. `< 5%` of remaining enemy HP).
  * **No HUD badge or meter** — communicate strictly through diegetic float/log text:
    * **Strike 1:** Cold/fog warning (e.g., *"The air turns bitter cold..."*)
    * **Strike 2:** Horn warning (e.g., *"A hunting horn echoes in the fog!"*)
    * **Strike 3:** A **spectral-green Wild Hunt (Oskorei)** unit/team joins the fight and sets `no_flee = True`, forcing lethal pressure to end the room.
* **Pros:**
  * Closes the remaining `Djupanda` + `Lak` stall-farming loophole cleanly without punishing honest defensive play in tough fights.
  * Zero HUD clutter; turns an existing Norse folklore faction (`OSKOREI_TIERS`) into a memorable roguelike clock (a la *Spelunky*'s Ghost).
* **Cons / Risks:**
  * Threshold needs care so a player legitimately reviving/stabilizing for 1–2 turns doesn't hit Strike 3 accidentally (cumulative 3-strike buffer with clear Strike 2 horn warning mitigates this).
* **Why:** Lets sustain and support moves stay genuinely useful in combat without allowing players to farm weak enemies back to 100% HP/MP between rooms.

---

### ADR-06: Unified Tile-Paint Layer (`Gyllenlykt` Pillar of Light + Mogel 3-Paint Trio + Future Caltrops)
* **Status:** Agreed
* **Decision:**
  * Elevate `Battle.spots` into a first-class, bidirectional tile-effect system supporting both hostile and friendly cells, rendered in Fight Lab:
    1. **`Gyllenlykt` (Dagskald's Pillar of Light):** True **coup-de-grâce** support move — priced high so only **~3 casts fit in Dagskald's 200-MP bar (~64 MP)**. Paints an ally's tile for **3 turns** (yellow/white-yellow hero tint + light pillar while standing on it): grants a **round-start HoT** (like `Kvad`) and **`+3 EVA` (100% Graze)** *only while occupying that tile*. No upfront burst heal; no bespoke `Evasive` timer flag. Allies can `Swap` into the light; enemies can shove heroes off it or paint over it.
    2. **Mogel 3-Paint Trio:** Distribute three distinct paint behaviors across Mogel ranks:
       * *Empty-tile paint:* denies an unoccupied hero cell (blocks safe swaps/moves).
       * *Occupied-tile paint:* hits on landing + 3-round countdown tick, forcing a `Move`/`Swap`/`Skrida`.
       * *Row paint (Elite/Boss):* coats an entire row for 3 rounds as the extreme spatial crisis.
       * **Board cap (~3 slimed tiles):** Once ~3 tiles on the hero side are slimed, Mogel AI skips painting and switches to direct attacks/abilities.
    3. **Future reuse:** Same primitive supports Oskorei caltrops or other ground traps.
* **Pros:**
  * One compact engine & art primitive unlocks hostile DoTs, hostile traps, and friendly sanctuaries.
  * Solves `Gyllenlykt`'s balance cleanly: awesome, iconic, costly (~3 per bar), interactive via `Swap`/shove/overwrite, and leaves persistent `Evasive` completely uniform.
  * Tile cap guarantees Mogel packs create *choices* (`Move` to clean cells) instead of an inescapable 6-tile swamp.
* **Cons / Risks:**
  * Requires exposing `spots` in `sim/lab.py` and adding tile + tint rendering to `fight_lab/screen.js` (currently `screen.js` only logs `"paint"` text).
  * Need clear overwrite rules when slime lands on Pillar of Light or vice versa (last paint wins is simplest and most tactical).
* **Why:** Makes the 2×3 board *breathe* — moving and swapping become proactive offensive and defensive tools rather than static row placement.

---

### ADR-07: Two-Curve Costing + Pouch Items as the Extreme-Grammar Outlet
* **Status:** Agreed (exact multipliers to tune in testing)
* **Decision:**
  * Replace the single uniform `cost * 2 ** steps` multiplier in `sim/words.py` with a **two-curve pricing model**:
    * **Steep curve (Output & Reach):** `Mer`, `Flok`, `All`, and `Styng` stay genuinely taxing so big AoEs (like `Alleld` at ~`48 MP`, ~3 casts per Brennumar's 150-MP bar) remain scarce, high-impact decisions.
    * **Gentle curve (Tactical Sidegrades):** Trade-off manners (`Tung`, `Bid`, `Jarf`, `Drif`) carry minimal/zero extra cost (their tempo or variance drawback *is* their cost); `Snar` carries a modest step; `Lonn` riders are **no longer double-taxed** with both a `-40%` damage cut (`RIDER_SHARE = 0.6`) and a `×2` cost spike.
  * **Pouch outlet:** Awkward or extreme grammar combinations (`Allblotskott`, massive multi-modifier nukes) are excluded from normal hero carving and surfaced as consumable **Pouch items** (*Shrapnel Bomb*, etc.).
* **Pros:**
  * Makes 1- and 2-part hero mutations (`Brakrosh`, `Snarbrakrosh`, `Merblotskott`, `Bidkrosh`) exciting roguelike build upgrades instead of self-punishing HP drains.
  * Preserves the scarcity of full-board nukes (`Alleld`) and makes Pouch items feel like rule-breaking tools.
* **Cons / Risks:**
  * Will require a fresh tuning pass across `sim/yardstick.py`, `sim/sweep.py`, and `sim/audit.py` to confirm no carved move dominates every slot.
* **Why:** If run progression revolves around 1–2 mutating core moves per hero, carving a tactical sidegrade must feel like unlocking a build identity, not taking a predatory tax.

---

### ADR-08: `Guard` Denies Weakness Bonus Rounds (and Future `Lya` Sharing)
* **Status:** Agreed
* **Decision:**
  * When a target is `defending` (`Guard`), incoming damage is halved **and** hitting its weakness **does not grant the attacker a Bonus Round**.
  * Keep `Lya` (Cover) open for future sharing onto select classes or gear (with distinct class flavor/cost so `Vasara` retains her anchor tank identity).
* **Pros:**
  * Turns telegraphed enemy weakness intents into a crisp 3-way roguelike puzzle: *kill/interrupt*, *Cover (`Lya`) with a resistant tank*, or *`Guard` to eat half damage and deny tempo*.
  * Smooths out biome-vs-party affinity RNG without diluting the power of weaknesses.
* **Cons / Risks:**
  * Slightly weakens enemy tempo in rooms where the player actively reads intents (which is the point — rewards skill!). Enemy AI should still account for `Guard` appropriately if needed.
* **Why:** Classic *Persona*/*SMT* counterplay that makes visible intents meaningfully interactive for every hero, not just the tank.

---

### ADR-09: Remove Forced `Advance` Turn-Stealing
* **Status:** Agreed
* **Decision:**
  * Remove the automatic `Advance` action override in `Battle.plan_phase` for **both** player-controlled heroes and enemies when a side's Front row collapses.
  * Continue relying on `Battle.eff_front` so an empty Front automatically exposes the Rear to enemy/hero melee reach.
* **Pros:**
  * Restores full player agency during crisis turns (e.g., stabilizing a Dying hero, Guarding, or finishing the boss instead of losing your turn to an involuntary step).
  * Stops enemy Rear melee units from wasting their turns auto-advancing when their Front dies.
* **Cons / Risks:**
  * Melee heroes left in an exposed Rear still take the `REAR_MELEE_MULT` (`0.5×`) damage penalty on `Short` strikes until they *choose* to step forward — worth ensuring the UI clearly shows they are in the Rear (and exposed).
* **Why:** Exposure already enforces the formation penalty when the Front falls; confiscating a unit's entire turn on top of that violates tactical agency.

---

### ADR-10: 4-Family Enemy Core Vertical Slice (`Beinar`, `Draugr`, `Mogel`, `Ande`)
* **Status:** Agreed (mechanical stories locked prior to code)
* **Decision:**
  * Focus the enemy pass on mixing the **4 drawn families** as distinct tactical puzzle pieces, restoring `FAMILY_BODIES` HP multipliers (`TIER_HP[tier] * body["HP"]`) instead of flatlining every family to identical tier HP:
    1. **Beinar *(Bone Wall — Weak: `Crush`, `Sol`; Resist: `Slash`, `Pierce`, `Natt`, `Aska`; HP `0.9`, DEF `1.4`)***: Subverts *"snipe the backline first."* `Beinbryn` Covers `Beinorv` (Long bow) & `Beinseidr` (rear caster); downed Bein drop 2-round bone piles unless scattered with `Crush`. `Fornbein` buffs `Warded` + carries a boss reset.
    2. **Draugr *(Barrow Bruisers — Weak: `Slash`, `Eld`, `Sol`; Resist: `Crush`, `Natt`, `Aska`; HP `1.2`, SPD `0.6`)***: Subverts *"let Vasara flatten the Front."* Slow heavy bruisers adding **telegraphed `Bid` haymakers** (30–40% hero HP + `Feared`/`Bleeding`) that wake up `Guard`, `Cover`, `Stun`, and `Swap`-dodge; crawl back at `35%` HP unless killed by `Slash`/`Eld`. `Forndraugr` adds row `Bid` + boss reset.
    3. **Mogel *(Living Mould — Weak: `Slash` + school weak; Resist: `Pierce`; Absorb: own element; HP `0.95`, SPD `0.8`)***: Subverts *"park in optimal rows and spam elemental AoE."* Uses the 3-paint trio (empty / occupied / row, ~3-tile cap), absorbs own element (stealing a Bonus Round!), and splits down ranks on death (`Mogel → Litel → Halv`).
    4. **Ande *(Elemental Glue — High MDF `1.3`, Low DEF `0.8`, Rear; opposing elemental weaknesses)***: Subverts *"turtle behind Frontline DEF and ignore Rear."* All-ranged elemental casters carrying child-element twists (`Blinded`, `Chilled`→`Frozen`, `Poisoned`, `Cursed`) and `Stor`/`Drott` stat buffs/resets.
  * Allow these 4 families to intermingle in rooms (via `sim/composer.py` gates/habitats) to produce layered multi-family puzzles.
* **Pros:**
  * Activates idle engine systems (`Bid` wind-ups, interrupts, `Cover`/`Guard` vs. wind-ups, tile movement, mixed damage-type routing) using sprites that already exist.
  * Restoring `FAMILY_BODIES` HP stops glass-cannon families from getting free durability.
* **Cons / Risks:**
  * Mixed-family packs require re-validating room difficulty in `sim/sweep.py` and `sim/gauntlet.py`.
* **Why:** Simple 2–3 move enemies create deep roguelike puzzles when each family asks a different question and rooms combine two questions at once.

---

## 3. Current-Reality vs. Target Code Comparison & Refactor Cost

> **Cross-cutting note:** `sim/engine.py` currently maintains two rules profiles (`"new"` vs. `"legacy"`) via ~25+ `if self.new_game:` checks so legacy regression fingerprints (`sim/regress.py`) stay frozen. Every change below should stay cleanly scoped to `profile="new"` (or explicitly decide when to retire `"legacy"`), and `fight_lab/sim/` must remain synced with `sim/` (`sim/test_lab_parity.py`).

| ADR | Current Reality in Code | Target Behavior | Primary Touchpoints | Refactor Cost | Key Risks / Notes |
|---|---|---|---|---|---|
| **ADR-01** Accuracy (Model A + Graze) | `engine.py` `odds()` / `roll()` / `expected_roll_mult()`: neutral `20%` Graze + `5%+DEX` Crit; Ahead (`≥1`) flat `33%` Crit; Behind (`≤-1`) `33%` Whiff + residual Graze. Pure status moves fail on neutral `20%` Graze (`status_lands()`). | Neutral `0%` Graze / `5%` Crit (statuses `100%`). Ahead `+1/+2/+3` = `33%/66%/100%` Crit. Behind `-1/-2/-3` = `50%/75%/100%` Graze (`50%` dmg, no riders, no Bonus Round; statuses shrug off). | `sim/data.py`, `sim/engine.py` (`odds`, `roll`, `expected_roll_mult`, `land`, `flurry`, `status_lands`, `knot_hold`), `sim/test_status_rules.py`, `sim/test_wave7a.py` | **Small–Medium** | `land()` and `flurry()` currently grant Bonus Rounds even on a Graze if `aff == "weak"` — must gate Bonus Round on non-graze! Also fixes `knot_hold()` legacy graze drift. |
| **ADR-02** Unified Persistent Stats | `data.py` `STAT_NAMES` + `NEW_GAME_STAT_NAMES`: 7 pairs (ATK/DEF/MAT/MDF/SPD/ACC/EVA). `engine.py` `end_round()` steps every untouched `u.stages` toward 0 every round. `Aukseid` pushes `MAT`, `Aukraft` pushes `ATK`. | 5 counter slots (unified Offense `MIT`/`FBL`, unified Defense `WRD`/`SND`, `QCK`/`SLW`, `ACC`, `EVA`), **no auto-decay** in `end_round()`. Update `BUNDLES` (`Cursed`, `Disarmed`), `Aukseid` (+2 self), `Aukraft` (+1 ally/party). | `sim/data.py`, `sim/engine.py` (`Unit.stages`, `raw_damage`, `end_round`, `counter_name`, `counter_value`), `sim/words.py`, `sim/gloss.py`, `sim/audit.py`, `fight_lab/screen.js` (`UP`/`UPS` sets), `sim/test_statuses.py`, `sim/test_status_rules.py` | **Medium–Large** | Widest ripple across tests, glossary, AI `counter_value()`, and `screen.js` icon labels (`Fortified`/`Waxing` → `Warded`/`Mighty`). Straightforward mechanically, just touches many files. |
| **ADR-03** Boss Reset Actions | No boss/elite stat-reset move or threshold AI exists. | Add self-cleanse & hero-stat-leveler enemy moves; AI triggers at `≥3` boss debuffs or `≥2` hero buffs, telegraphed in intents, resolving `Normal`/`Late`. | `sim/data.py` (boss/elite rows), `sim/engine.py` (`resolve`, `declare`, `reason`, `intent`), `sim/test_statuses.py` / new boss test | **Small–Medium** | Cleanly additive; add a mild cooldown or post-reset guard so AI doesn't loop resets unnecessarily. |
| **ADR-04** Sustain (`Meditate` / `Djupanda` / `Dagskald`) | `engine.py` `can_meditate()` grants universal `Meditate` to all new-game magicals; `screen.js` reserves 6th menu slot for `o.meditate`; `Djupanda` is `Bid` normal-group free MP (`40%`); `LAK_CLEAN = 100`. | `can_meditate()` off by default; `Djupanda` becomes Late `Bid` (`release_group = -1`) run-reward move; reduce `LAK_CLEAN` (~50) and tune `Dagskald` kits; add optional Rest step to `sim/gauntlet.py`. | `sim/data.py`, `sim/engine.py` (`can_meditate`, `options`, `declare`), `fight_lab/screen.js`, `sim/gauntlet.py`, `sim/test_wave4a.py`, `sim/test_wave7a.py` | **Small–Medium** | Removing universal `Meditate` simplifies `options()` and `screen.js`; update `test_wave4a` / `test_wave7a` expectations. |
| **ADR-05** Wild Hunt 3-Strike Anti-Stall | `OSKOREI_TIERS` and `Battle.no_flee` already exist in `data.py`/`engine.py`, but no stall tracker or mid-fight reinforcement spawn exists. | Track cumulative stall rounds in non-Boss rooms on `Battle`; emit float-text warnings on Strikes 1 & 2; on Strike 3 spawn spectral Oskorei into open enemy cells and set `no_flee = True`. | `sim/engine.py` (`Battle.__init__`, `end_round`, `next_round`, mid-fight unit registration in `units`/`uid_of`/`by_uid`), `sim/lab.py`, `fight_lab/screen.js` (dynamic unit entry) | **Medium** | Mid-fight spawning (`uid_of`, `by_uid`, `board` state in `lab.py` & `screen.js`) is the main new plumbing — `Battle` currently assumes `self.units` is fixed at `__init__`. |
| **ADR-06** Unified Tile-Paint (`Gyllenlykt` + Mogel Trio) | `engine.py` `self.spots` only handles hostile `Mark-` occupied-cell slime (`SPOT_IMPACT`, `SPOT_TICK`, `SPOT_ROUNDS=3`); `Gyllenlykt` is `Lak + Lonn` instant heal + `EVA +3` stage. `lab.py` doesn't send `spots`; `screen.js` doesn't draw tiles. | Generalize `spots` into typed tile effects (`slime`, `lantern`, future `caltrops`): `Gyllenlykt` (~64 MP) paints 3-turn ally tile (round-start HoT + `+3 EVA` while occupying cell, no burst); Mogel gets empty/occupied/row paint + ~3-tile cap. Expose `spots` in `lab.py` and render slime-line + Pillar of Light tint in `screen.js`. | `sim/data.py`, `sim/words.py`, `sim/engine.py` (`spots`, `paint`, `tick_spots`, `net_stage`, `declare`), `sim/lab.py` (`_state`), `fight_lab/screen.js`, `sim/test_wave4b.py`, `sim/test_board.py` | **Medium–Large** | Biggest visual + engine feature. Check `net_stage()` reading tile EVA bonus cleanly without mutating persistent `u.stages["EVA"]`. Also fixes `paint` emitting 0-dmg hit on whiff. |
| **ADR-07** Two-Curve Costing | `words.py` `compile_verb()` prices everything on `v["cost"] * 2 ** steps` (`COST_LADDER`), and `Lonn` also cuts power/heal by `RIDER_SHARE = 0.6`. 23 legal carves exceed `128`. | Split cost formula into steep output/reach curve (`Mer`/`Flok`/`All`/`Styng`, preserving ~`48 MP` `Alleld`) and gentle sidegrade curve (`Tung`/`Bid`/`Jarf`/`Drif`/`Snar`/`Lonn`, removing double-tax on `Lonn`). Move extreme combos to `ITEMS`. | `sim/data.py`, `sim/words.py` (`compile_verb`), `sim/lexicon.py`, `sim/audit.py`, `sim/test_compiler.py`, `sim/test_wave7a.py`, `sim/test_wave7b.py` | **Small–Medium** | Very localized in `words.py` + `data.py`, then regenerate `grammar_book/lexicon.json` & `audit.json` and update price assertions in tests. |
| **ADR-08** `Guard` Blocks Bonus Rounds | `engine.py` `land()` checks `t.defending` for `0.5×` damage, then unconditionally grants `self.eligible.add(u)` on `aff == "weak"`. | Suppress `self.eligible.add(u)` when `t.defending` is True (both in `land()` and `flurry()`, and optionally `status_lands()`). | `sim/engine.py` (`land`, `flurry`, `status_lands`), `sim/test_steps.py` / new test | **Small** | Tiny, surgical code change (~5 lines) with high tactical payoff. |
| **ADR-09** Remove Forced `Advance` | `engine.py` `plan_phase()` runs `if k == 0 and u in advancers:` before `self.controls(u)` and `self.declare(u)`, confiscating Rear melee turns. | Disable `advancers` turn-override in `new_game` (for both sides); keep `eff_front()` Rear exposure. | `sim/engine.py` (`plan_phase`, `advancers`), `sim/test_board.py`, `sim/test_rotation.py` | **Small** | Tiny code change; update `test_board.py` / `test_rotation.py` tests that explicitly assert auto-advance behavior (keeping legacy tests green under `profile="legacy"`). |
| **ADR-10** 4-Family Enemy Core | `engine.py` `new_game_enemy()` overwrites `e.maxhp = TIER_HP[tier]` (erasing `FAMILY_BODIES` HP). Zero catalogued foes have `Bid` moves; habitats separate `Barrow` (`Draugr`/`Bein`) from `Mogel`/`Ande` guests (`GUEST_WEIGHT=0.10`). | Apply `TIER_HP[tier] * e.b("HP")`; add Draugr `Bid` haymakers, Mogel 3-paint moves, boss resets; update `composer.py` mixed-room pools/weights for the 4-family slice; recalibrate `sweep.py`/`yardstick.py`. | `sim/data.py`, `sim/engine.py` (`new_game_enemy`), `sim/composer.py`, `sim/yardstick.py`, `sim/sweep.py`, `sim/gauntlet.py`, `sim/test_mirror.py`, `sim/test_habitats.py` | **Medium** | Mostly data + encounter composition tuning; re-run `yardstick.py`, `sweep.py`, and `gauntlet.py` to verify hit counts and room costs. |

### Incidental Code Leaks to Sweep Up Along the Way
Spotted during the code review — cheap to fix inside the relevant waves:
1. **`preview_order` tie-break mismatch** (`sim/engine.py`): `order()` breaks SPD ties in favor of `"party"` in `new_game`, but `preview_order()` omits the side tie-breaker and sorts straight to `self.coin`. Share one sort key.
2. **`knot_hold` legacy graze drift** (`sim/engine.py`): AI `knot_hold()` still computes `max(0.0, GRAZE_BASE - STEP * net_stage)` instead of calling `self.odds()`.
3. **`paint` whiff event** (`sim/engine.py`): Under ADR-01 whiffs disappear, and under ADR-06 `paint` should cleanly handle graze (`50%` impact damage, tile still painted or grazed per rule) rather than emitting a 0-damage `"hit"`.

---

## 4. Phased Bridge Plan (Current Reality → Target Design)

Ordered by dependency so every wave leaves the 30 `sim/test_*.py` suites, `sim/test_lab_parity.py`, `sim/yardstick.py`, and `fight_lab/` green and testable on its own:

### Wave A — Core Combat Rules & Agency (Low Risk, High Feel Impact)
* **Includes:** ADR-01 (Model A Accuracy + Graze), ADR-08 (`Guard` denies Bonus Round), ADR-09 (Remove forced `Advance`), plus incidental fixes (`preview_order` tie-break, `knot_hold` odds).
* **Verify:** Unit tests for neutral 100% status landing, Graze stripping riders/Bonus Rounds, `Guard` denying enemy Bonus Rounds, and collapsed-Front Rear exposure without turn loss. Check `yardstick.py` & `sweep.py` deltas.

### Wave B — Unified Persistent Stat Ladder & Boss Resets
* **Includes:** ADR-02 (Unified `MIT`/`FBL`, `WRD`/`SND`, `QCK`/`SLW`, persistent `ACC`/`EVA`; update `BUNDLES`, `Aukseid`/`Aukraft`, `screen.js` counter sets, `gloss.py`/`audit.py`), ADR-03 (Boss/Elite telegraphed reset moves + AI trigger).
* **Verify:** Status/counter tests, `lexicon.py --check`, `audit.py`, and boss-fight AI logs confirming bosses spend turns resetting at threshold.

### Wave C — Two-Curve Costing & Sustain Rebalance
* **Includes:** ADR-07 (Two-curve costing in `words.py`, remove `Lonn` double-tax, add Pouch item equivalents like *Shrapnel Bomb*), ADR-04 (remove universal `Meditate`, make `Djupanda` Late `Bid`, tune `Dagskald` burst `Lak`, add 2/3 Rest-node simulation option to `gauntlet.py`).
* **Verify:** Regenerate `grammar_book/lexicon.json` & `audit.json` (confirm "past the ladder" drops dramatically while `Alleld` stays ~3/bar); run `gauntlet.py` comparing Dagskald vs. non-Dagskald parties with Rests.

### Wave D — Unified Tile-Paint Layer (`Gyllenlykt` + Mogel Trio) & Fight Lab Rendering
* **Includes:** ADR-06 (typed `spots` with `Gyllenlykt` Pillar of Light ~64 MP / 3-turn HoT + `+3 EVA`, Mogel empty/occupied/row paint + ~3-tile cap), `lab.py` `spots` payload, and `fight_lab/screen.js` rendering (slime-line, tick blink, Pillar of Light yellow/white-yellow hero tint).
* **Verify:** Board/tile tests (overwrite rules, swapping into/out of Pillar of Light, Mogel 3-tile cap), `test_lab_parity.py`, and `sim/checks/s_smoke.py` visual smoke check.

### Wave E — 4-Family Enemy Core Pass & Mixed Rooms
* **Includes:** ADR-10 (restore `FAMILY_BODIES` HP multipliers, Draugr `Bid` haymakers, Beinar/Draugr/Mogel/Ande kit polish, mixed-family composer rooms).
* **Verify:** Full `yardstick.py`, `sweep.py`, and `gauntlet.py` regeneration + human Fight Lab playtest (`calib_gap.py`).

### Wave F — Wild Hunt 3-Strike Anti-Stall
* **Includes:** ADR-05 (cumulative non-Boss stall tracker, Strikes 1–2 float text, Strike 3 mid-fight spectral Oskorei reinforcement plumbing in `engine.py`, `lab.py`, and `screen.js`).
* **Verify:** Dedicated stall-test fights confirming (a) honest tough fights don't trip Strike 3, and (b) healing loops spawn Oskorei on Strike 3 with `no_flee`.

---

## 5. Art & Visual Asset Backlog (From Session)

Captured for future drawing/recoloring — placeholder sprites can stand in during Waves A–F:
1. **Mogel Slime-Line:** Recolorable ground puddle/line strip placed under a hero's feet (tinted to the Mogel's element) + colored flash/blink on the hero when tick damage fires.
2. **`Gyllenlykt` Pillar of Light:** Soft yellow / white-yellow vertical light overlay on the blessed tile, tinting whichever hero currently stands there while the 3-turn tile is active.
3. **Wild Hunt Spectral Oskorei:** Recolored spectral-green variants of existing Resurrect 64 sprites (e.g., swordsman/archer/hound) so anti-stall reinforcements read immediately on sight.
4. **Future `Djur` Family (Post-4-Family Slice):** Nordic fauna roster (e.g., `Lodjur`, `Varg`, `Galt`, `Bjorn` — pinning, bleeding bites, shoves, binds) once the 4-family core is humming.
