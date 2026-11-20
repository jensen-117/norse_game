# Refactor Plan: the Five Classes (Nov 20, 2026)

Brings the sim and the Fight Lab from the game we had (recruits who level) to the game in **pillars.md** and **classes.md** (five fixed classes, words that grow by grammar, statuses with shapes). Ends with the level sweep. Backed by a read of the whole sim (engine.py 1,850 lines, data.py, grammar.py, lab.py, composer.py), 121 tests passing, the Lab's copy identical.

---

## 1. Why Go

- **The design is settled, the code is not.** The sim still models the old game: heroes are *born* (random genes, a Personality, a star sign), *level*, and get kits by level. None of the five classes' signatures exist in the engine.
- **The sweep needs the new game.** Pricing the power level against the pace tables only means something with the real kits, statuses and costs.
- **Built once, used everywhere.** The status shapes, the stat counters and the word compiler serve enemies too (a Drattr can Sunder, a boss can sing). Every later class is mostly data.
- **The Lab is the playtest.** Joseph feels the classes in the Lab; the sweep only says whether the numbers hold.

## 2. Where We Are (the code review)

### What's solid, and stays

| Piece | Where | Why it's reusable |
|---|---|---|
| The fight loop and step API | `Battle.begin / plan_phase / resolve_phase / commit` | The Lab and the sim already share it; nothing in the redesign changes its shape |
| Events | `Battle.emit` | Every new mechanic is a new event kind; the page draws from them |
| Speed groups | `group_of`, `order`, `SPEED_GROUP_BY_KIND` | Already the combat_spec ladder (+3 protection, +1 Snar, −2 Tung) |
| The seam rule | `join_morphemes` | Already merges a doubled letter (Brak + Krosh = Brakrosh, Auk + Kraft = Aukraft) and lets vowel meet vowel |
| The word compiler | `grammar.compile_word` | Parts as data rows (targets, manners, riders), names from parts, an English name, a value (`ev`) and a flagger (`assess`). The right foundation |
| Wind-ups | `bide`, the release in `plan_phase`, the lost-wind-up check in `resolve` | Djupanda, Bidhevn and the meteor reuse it as is |
| Cover, Move, Swap | `resolve` (kinds cover, move) | Lya is Cover; Skrida and Kasta/Svepa build on the swap code |
| Cleanse lifting lowered stats | `resolve`, kind cleanse | Already sets negative stages to 0: exactly the agreed rule |
| Shares of a bar | `price_shares` (Splash's `mp_share`) | The cost anchors are this, for heroes, for MP and HP |
| The board, reach, the Dying, the pouch, items | throughout | Unchanged |
| Fingerprints and tests | `regress.py`, 121 tests | The safety net for "refactor first, change second" |

### What's in the way

| Problem | Where | What it blocks |
|---|---|---|
| **Heroes are born, not built.** Random genes, Personality and star sign; stats by `attr_at(level)`; HP and MP by level formulas; affinities partly from the sign | `birth`, `natural_attrs`, `Unit.__init__` (maxhp, maxmp) | Fixed characters |
| **Kits come by level** (`top_tier`, Mer at 20, Jatte at 50) and are hand-built per class | `loadout` | Starting kits, kit snapshots |
| **Three ways to build a move:** hand builders (`damage_spell`, `status_spell`, `stat_spell`, `skill`...), the compiler (damage only), and enemy rows (`family_move`) | engine.py top, grammar.py, `_family_move` | One source of truth for moves |
| **Riders live on elements** (Reyk: AccDown, Hrim: Chilled, Blixt: Stunned, Gro: Poisoned) and fire by tier chance | `ELEMENT[...]["rider"]`, `riders` | "Plain moves have no rider; Lonn adds the designated one" |
| **Statuses are a bare dict of timers,** and what each does is scattered: stat effects hard-coded in `stage`, skips in `resolve`, ticks in `next_round` and `resolve` (Bleeding), expiry in `end_round` | `Unit.stage`, `resolve` (lines ~732–750), `next_round`, `end_round`, `apply_status` | Build, fade and pool shapes; stacks; sources; decay |
| **Stages run −5..+5,** stack forever, never decay, and are separate from statuses | `Unit.stages`, `stat` kind in `resolve` | One counter per stat, −3..+3, cancelling, decaying |
| **Costs are flat** (8/16/32) against a bar of `10 + WIS + level`: at level 15 a Brennumar has 72 MP and Eld costs 10 (**about 1/7** of the bar; a plain base spell 1/9), against the **1/16** target: about twice as tight | `TIER_COST`, `Unit.__init__` | The cost anchors |
| **The release is pinned to group 0** | `plan_phase`: `dict(ba, _release=True, cost=0, group=0)` | A Heavy (−2) meteor |
| **Taunt has a speed group but no rules** | `SPEED_GROUP_BY_KIND["taunt"]`, nothing else | Egga |
| **No Meditate** | | The magicals' economy |
| **40 `*_before_*.py` backups** in sim/, and no git | sim/ | A refactor this size wants history, not copies |

## 3. Where We Want to Be

- **A hero is a class sheet plus four words.** The sheet holds fixed stats (frozen at the chosen level), HP and MP bars, weapon, affinities. The words are compiled from parts; a kit snapshot (leg 1, 2, 3) is a list of word specs.
- **A move is a word spec, compiled once.** `{verb: "Skott", tier: "Mer", lonn: True}` → Merblotskott, with its power, cost (a share of the hero's own bar), speed group, keywords, rider and plain text. The compiler enforces the two-part cap and names capstones.
- **A status is a row in a table.** Its shape (timed, build, fade, pool, flag), what it does to stats, how it decays, whether it's harmful. The engine reads the row; it doesn't know Scorched by name.
- **A stat is one counter, −3..+3,** its own stacks plus its sources, named (Feeble/Mighty, Sundered/Fortified, Blinded/Keen, Marked/Nimble, Slowed/Quick), decaying toward zero when not pushed.
- **The five signatures work in the sim and on the page:** Scorched, Pinned, Marked, Sundered, the Song, Knots, plus Egga, Lya, Hevn, Djupanda, Kasta/Svepa, Byr, Frozen's fade.
- **One script runs the sweep** and writes a report against the pace tables, per leg, per class, per party.

## 4. How We Get There: the Waves

**The rule for every wave: refactor first, change second.** Where a wave rebuilds something that already works, it first reproduces today's fights exactly (fingerprint identical), and only then changes behaviour, measured. Each wave ends green: tests pass, the Lab runs, the Lab's copy is synced.

### Wave 0: housekeeping (small)
- **Git** for the project (sim, fight_lab, specs, art tools); move the `*_before_*` copies into `sim/attic/` (or drop them once git holds the history). *Joseph's call.*
- **Done (Nov 20): `sim/fingerprint.py`**, a fixed-party fingerprint (288 fights: four parties, three places, levels 10 and 30; baseline hash in `sim/checks/fp_base.sha1`). `check` names the first fight and event that differs. Was: **a fixed-hero fingerprint:** `regress.py` hires random recruits; add a variant with a fixed party built by the old `birth` path with fixed seeds, so Waves 1–2 can prove "nothing changed".

### Wave 1: the status engine (large; the foundation)
**1a. Pure refactor (fingerprint identical).** **Done (Nov 20):** `STATUSES` and `SKIP_ORDER` in data.py; the engine reads rows for stat effects (`status_stat`), applying (`apply_status`), ticks (`tick_statuses`), skips (`skips`), flags (`has_flag`, `silenced`), Shatter, Fear's group and the Chilled→Frozen chain. Fingerprint identical (288 fights), regress.py identical (480), 125 tests.
- `STATUSES` table in data.py: every current status as a row (Poisoned, Bleeding, Stunned, Chilled, Frozen, Bound, Feared, Blinded, Cursed, Disarmed, Silenced), with its current behaviour expressed as data (`shape="timed"`, its stat sources, its skip rule, its tick).
- A small status layer on `Unit` (or a `StatusBook` it owns): `add`, `has`, `stacks`, `sources(stat)`, and three hooks the engine calls: `on_round_start` (ticks: Poisoned), `on_action` (skips: Bound, Frozen, Stunned; Bleeding), `on_round_end` (expiry).
- `stage(stat)` reads sources from the table instead of hard-coding Chilled, Blinded, Cursed, Disarmed.
- **Done when:** the fixed-hero fingerprint and `regress.py` match byte for byte.

**1b. The new rules (measured).**
- **Stat counters:** −3..+3, named by `STAT_NAMES`, own stacks plus sources (the badge total), cancelling, decaying one step at the end of a round nobody pushed them; Mer pushes two. MAT and MDF stay unnamed counters for now.
- **Shapes:** *build* (Sundered by blows, the Song by singing: add, cap 3, lose one when not refreshed; needs a per-round "struck" or "refreshed" flag), *fade* (Scorched: 100/50/20 of its tick at round start, reset by its feeder, flared by wind; Frozen: lose the next action, then 50%, then 20%, counted in actions, no refreeze), *pool* (Knots: no decay, spent).
- **Blinded** loses its EVA part. **Marked** is the EVA counter. **Pinned** and **Chilled** add Slowed as sources.
- **Boss immunity** to Frozen, Stunned, Bound (rank Drott).
- **Enemy stat moves** (the Beinbryn's DEF up, the Angler's Lure, Feeding Frenzy) now push counters: a behaviour change for enemies, so measure family win rates before and after.
- **Done when:** tests for every shape and rule (`test_statuses.py`), and the family tables moved only where expected.

### Wave 2: one compiler, and the cost anchors (large)
**2a. Pure refactor.** The hand builders (`damage_spell`, `heal_spell`, `status_spell`, `stat_spell`, `cleanse_spell`, `skill`, `strike`) become thin wrappers over the compiler, so every hero and enemy move comes from one place. **Done when:** fingerprints identical.

**2b. The new grammar.**
- **Word specs for every kind,** not just damage: status (Reyk, Naglskott, Peka), stat (Aukraft, Aukskold, Byr), heal (Lak), cleanse (Skolja), song (Kvad), knot (Knyta), untie (Kuling, Storm, Orkan), displace (Kasta, Svepa), taunt (Egga), cover (Lya), glide (Skrida), wind-up gain (Djupanda).
- **The parts:** the tier ladder (Halv, base, Mer, Jatte; Ur on gear), **Styng** (adds damage, or a hit to a status move), **Lonn** (adds the verb's **designated rider**, named by the rider's prefix: Blot, Nagl, Brak, Sveda; else "Lonn"), targets (Flok, All), manners (Snar, Tung, Bid, Jarf, Drif).
- **`DESIGNATED_RIDERS`** per verb (classes.md tables) and **`RIDER_PREFIX`** per status. **Hero moves carry an explicit rider;** the element riders stay only as the enemy default, so enemy kits don't change.
- **The two-part cap** enforced; **`CAPSTONES`** maps over-cap part sets to their names (Tusensplitter, Pilskur, Hasin, Holm, Skogsbrand).
- **Costs as shares** of the hero's own bar: `MP_BASE_SHARE = 1/16`, `HP_BASE_SHARE = 1/36`; parts multiply; Halv is free. `price_shares` generalised to set every hero cost once the sheet is known. **The check:** compiled costs land near the ladders (MP: 1/16, 1/10, 1/6, ~1/4; HP: 1/36, 1/24, 1/16, ~1/10).
- **Speed-group keywords:** `KEYWORDS` (First +3, Swift +1, Late −1, Heavy −2, Last −3) and the release group from the manners (Bid + Tung releases Heavy).
- **Done when:** `test_compiler.py`: every kit move in classes.md compiles **to the spelling in classes.md**, caps hold, costs land on the ladder, enemy fingerprints identical.

### Wave 3: class sheets and kits (medium)
- **`CLASS_SHEETS`** for the five: kind, weapon, school, stat weights, affinities, HP and MP bars, starting kit; a `level` knob until the sweep freezes it.
- **`KITS`**: the leg 1, 2 and 3 snapshots (agreed Nov 20).
- **`build_hero(cls, kit="leg1", level=None)`** replaces `birth` for the new game (`birth` stays for the old runners until they're retired).
- **Universal actions:** **Meditate** (`MEDITATE_SHARE`, magicals only, group 0), **Egga** (taunt: the protection group; single-target enemy moves that can reach her go to her; the AI knows), **Lya** (Cover, already in).
- **The Lab:** `make_party` takes a class and a kit snapshot; the hero card shows the sheet.
- **Then: sweep Layer 1** (hit counts by class, tier and level) picks the level, which sets the MP and HP bars (rounded: 70, not 67).

### Wave 4: the signatures (large)
One mechanic at a time, each with its test and its AI valuation:
- **Brennumar:** Reyk and Sveda as no-damage status moves; **a weak hit by a status move lands for sure, adds a stack, and earns the Bonus Round**; Scorched; Djupanda (Bid machinery, gives MP).
- **Ullar:** Pinned (rooted: no row changes, a wall for Kasta); Marked; Banskott (pays only on Pinned); Skrida (glide either way, swap with an ally, Swift, Nimble).
- **Vasara:** Sundered by blows (Pierce bonus on Sundered targets); Hevn (counts hits taken since her last turn; Bidhevn absorbs a round, releases double).
- **Dagskald:** Kvad (verses on the singer, party heal at round start: verses × base); Lonnlak cleanses one; Sol's Lonn: Blinded.
- **Skurmar:** Knots (pool on the caster; passives by count; carried between rooms: a field the dive keeps); Kuling, Storm, Orkan (knot cost plus MP); Kasta and Svepa (forced moves: swap and bump, Pinned is a wall); Byr (party Quick); Blixt's Stun only on Lonnblixt.
- **The AI:** each mechanic gets a value in `declare` (what a stack, a knot, a verse is worth). **The sweep can only be as good as the AI**: Layer 2 numbers are a floor for tempo classes like the Skurmar.
- **Done when:** each mechanic has a test, and a scripted Lab fight shows it.

### Wave 5: legs and the sweep (medium)
- **`LEG_SCALE = [1.0, 1.1, 1.2]`** applied where the composer spawns (`composer.spawn(placed, level, scale)`).
- **`sweep.py`:** the starting three, then the Dagskald and the Skurmar each swapped in; legs 1–3 with their kits and scales; every place. Reports hits to kill and to be killed per tier (Halv, base, Stor, Drott), rounds per fight, and HP and MP spent per fight, against pillars Part 5b. Writes `sweep_report.md`.
- **Then:** freeze the level, round the bars, write the stat blocks into `CLASS_SHEETS`.

### Wave 6: the page (medium; can overlap Wave 4)
- Badges with counts (Sundered 2, Knots 3, the Song's verses) and a hover that lists sources and the glossary line; keywords in the keyword colour on move cards; Pinned, Marked, Scorched, Feeble and the rest as icons (Joseph's art; stand-ins first); new event kinds (stack, decay, flare, knot, untie, bump, taunt, meditate).
- Publish the Lab when Wave 4's first class plays end to end.

## 5. Functions to Build (brainstorm)

**data.py:** `STATUSES`, `STAT_NAMES`, `KEYWORDS`, `CLASS_SHEETS`, `KITS`, `DESIGNATED_RIDERS`, `RIDER_PREFIX`, `CAPSTONES`, `PARTS` (Styng, Lonn) beside `TARGETS` and `MANNERS`, `MP_BASE_SHARE`, `HP_BASE_SHARE`, `MEDITATE_SHARE`, `FADE = (1.0, 0.5, 0.2)`, `STACK_CAP = 3`, `LEG_SCALE`, `BOSS_IMMUNE`.

**engine.py**
- Status layer: `add_status(u, name, stacks=1, src=None)`, `refresh`, `stacks(u, name)`, `stat_total(u, stat)` (own plus sources, clamped −3..+3), `sources(u, stat)` (for the hover), `on_round_start`, `on_action` (returns "skip" or "go"), `on_round_end` (decay the unrefreshed, expire the timed).
- `stage(stat)` becomes `stat_total`; `stat` resolve pushes counters.
- `build_hero`, `price_bars(u)` (the generalised `price_shares`).
- Kinds in `resolve`: `meditate`, `taunt`, `song`, `knot`, `untie`, `displace`, `glide`; `forced_move(t, cell)` with `bump`.
- `hits_taken` on Unit (Hevn), reset at its turn; `struck_this_round` (Sundered).
- `release_group(a)` from manners.
- `plain()` grows keyword and stack text; `inspect()` returns stacks and sources.
- AI: `value_status(u, f, name, stacks)`, `value_knot`, `value_verse`, `value_taunt` inside `declare`.

**grammar.py:** `compile(spec)` for every kind; `parts_of(spec)`, `check_cap(spec)`, `capstone_name(spec)`, `cost_share(spec)`; `name_of` extended (Lonn naming by prefix); `assess` extended to every kind (the flagger finds free upgrades and broken combos as before).

**lab.py:** `make_party` by class and kit; `hero_card` from the sheet. **composer.py:** `spawn(..., scale)`. **sweep.py** (new). **Tests:** `test_statuses.py`, `test_compiler.py`, `test_classes.py`, `test_signatures.py`.

## 6. Decisions Before or During a Wave

| Decision | Blocks | Claude's proposal |
|---|---|---|
| Git, and the `*_before_*` copies | Wave 0 | **Done (Nov 20):** a local repo; copies in `attic/`. Needs a remote to survive this workspace |
| **Class affinities without star signs** | Wave 3 | **Agreed (Nov 20):** magicals take their school's; martials their weapon weakness plus one authored elemental weakness and resistance per class |
| Do status moves still roll to land? | Wave 4 | Yes, as now (graze, then the tier's chance × WIL), except a weak target: always lands, +1 stack, Bonus Round |
| Lonnegga's Blinded: on whom? | Wave 4 | On each foe that strikes her this round (the taunted swing wild) |
| Hevn's power per hit and cap | Wave 4 | +25% per hit, cap +100% (a knob; the sweep tunes) |
| Kvad's base, the knot passives, Meditate's share | Wave 4 | Knobs at placeholder values; the sweep tunes |
| Enemy stat moves under the new counters | Wave 1b | Convert them, measure, and accept small shifts |

## 7. Out of Scope Here

dive.py and the tapestry in the Lab (next, after the sweep); the other seven classes; weapons with moves and rider auras, talismans, Omens (they're run power on top of the classes; the sweep prices the classes bare); Joseph's art for the new badges.
