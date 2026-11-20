# The Spellbook

A spell-naming system and soft battle frame in the spirit of SMT, Persona, Final Fantasy, Dragon Quest, and Pokémon, built from Norse, Swedish, and broader Germanic roots, with Uralic (Finnish, Sámi) and Proto-Indo-European consulted along the way.

**This is the spellbook: what's possible through magic and skills,** plus the rules that make them work. Its companion, **bestiary.md**, covers the bodies that deliver them.

The goal isn't strict etymology. A Swedish speaker should hear a name and think *"yeah, that sounds right,"* and an English speaker should be able to learn the ladder the way you learn *Crack → Crackle → Kacrack → Kacrackle*.

**Status key:** sections marked **Locked** are agreed. Sections marked **Draft** are working proposals, open to push and pull.

---

## Part 1: Naming

### Three Registers (Locked)

Players always know which kind of word they're looking at:

| Register | Language | Examples |
|---|---|---|
| **Spells and proper nouns** | The old language | Spells (Eld, Nedskold); classes (Brennumar); signs (Arin); rites (Erfi) |
| **Statuses** | Plain English | Frozen, Cursed, Disarmed |
| **Items** | English with Norse flavor | Surtsstafr, Rán's Net, Hedge Wizard's Leather Strip |

You cast Hrim, and the enemy is *Frozen*. The magic words are what you say; the status is what everyone sees happen.

### Spelling Rules (Locked)

1. **No special letters.** *Jätte* becomes Jatte, *läka* becomes Lak.
2. **Identical letters at a seam merge.** Halv + vatn = Halvatn, All + lak = Allak, Auk + kraft = Aukraft.
3. **When two different vowels meet, the second one wins.** Jatte + aska = Jattaska.
4. **Names end like names** (signs and other proper names). Two syllables with an open or soft ending (Mierka, Otso, Myyra) reads as a name; one syllable reads as a thing.
5. **Class names take the agent ending -ar** (or *-mar*, our compressed form of Old Norse *-maðr*, "man"). If a root names a thing, -ar makes it a person: Holm → Holmgar, Glima → Glimar, Ullr → Ullar. (From Swedish *-are* and Old Norse *-ari*, as in *riddare*.) Well-known words like Berserker are left alone.
6. **Class names avoid spell roots.** Names like Eldreyk or Jordskald would half-read as spells. Name the job, not the element.

Inventing words is allowed. The spells already do it (Jatteld and Allurnatt exist in no language). An old, punchy word massaged with morphemes is fair game, as long as it passes these rules and the Swede test.

### In the Pocket

Words held for later use:

- **Smed** (smith), **Sten** (stone): bespoke spells, such as weapon signature moves
- **Skog** (forest) → **Skogar** (from ON *skógarmaðr*, "outlaw"): if a knife-and-skulk Rogue returns
- **Drengar** (from ON *drengr*, the honorable warrior): an earned honor title or rank
- **Regin** (ON "the divine powers"): an Ur-tier item or a title
- **Tapio** (the Finnish forest king): an item name, such as Tapio's Sickle
- **Six martial classes** (Geiras, Stikkar, Maekir, Holmgar, Atgeir, Glimar): possible advanced or prestige classes (Part 6)
- **Blodsbroder** (Swedish *blodsbröder*, "blood brothers"; ON *fóstbrœðralag*): the name for Communion, if it returns (Part 8)

---

## Part 2: The Spellbook

### The Schools (Locked)

Four elemental schools plus a Light/Dark pair. Each school teaches a core element and a child element: a related form that is its own damage type, learned through the parent school.

| School | Element | Child | How the child arises |
|---|---|---|---|
| **Eld** | Fire | **Reyk** (Smoke) | Fire burns and gives off smoke |
| **Vatn** | Water | **Hrim** (Ice) | Water freezes into rime |
| **Blast** | Wind | **Blixt** (Lightning) | Wind whips up the storm that brings lightning |
| **Jord** | Earth | **Gro** (Nature) | Earth nurtures growth |
| **Sol** | Light | **Lak** (Healing) | Light makes whole |
| **Natt** | Dark | **Aska** (Decay) | What remains when something burns down |

A child element shifts its parent's role rather than just adding damage. **Blast** and **Blixt** share their *Bl-* by happy accident, which gives them a family resemblance; the pattern isn't forced elsewhere.

#### Roots

| Root | Meaning | Source |
|---|---|---|
| Eld | fire | Old Norse *eldr*, Swedish *eld* |
| Reyk | smoke | Old Norse *reykr* (as in Reykjavík, "smoky bay"), Swedish *rök* |
| Vatn | water | Old Norse *vatn*, Swedish *vatten* |
| Hrim | rime, frost | Old Norse *hrím*, Swedish *rimfrost* |
| Blast | wind | Swedish *blåst* ("windy weather," from *blåsa*, "to blow") |
| Blixt | lightning | Swedish *blixt* |
| Jord | earth | Old Norse *jörð*, Swedish *jord* |
| Gro | growth, nature | Swedish *gro*, "to sprout, germinate" |
| Sol | sun, light | Old Norse *sól*, Swedish *sol* |
| Lak | healing | Swedish *läka*, "to heal" |
| Natt | night, dark | Swedish *natt* |
| Aska | ash, decay | Swedish and Old Norse *aska* |

### Grammar (Locked)

Every damage spell is built from up to three pieces, always in this order:

```
[Target] + [Tier] + Root
   All-  +  Jatte- + Blixt   =  Alljatteblixt  ("Strong Lightning, hits all")
```

#### Tiers

| Tier | Prefix | Meaning | Example |
|---|---|---|---|
| Weak | **Halv-** | Swedish *halv*, "half" | Halveld |
| Base | — | — | Eld |
| Moderate | **Mer-** | Swedish *mer*, "more" | Mereld |
| Strong | **Jatte-** | Swedish *jätte*, "giant" (also an everyday intensifier, as in *jättebra*) | Jatteld |
| Strongest | **Ur-** | Swedish *ur-*, "primal, original" (as in *urtid*, "primeval time") | Ureld |

**One tier per spell.** Tiers never stack.

**Ur** spells are never learned. They exist only on gear (Part 6).

#### Targeting

| Target | Prefix | Example |
|---|---|---|
| Single | — | Blixt |
| All | **All-** | Allblixt |

All- always comes first, so it's the first thing you read, like SMT's *Ma-*.

#### Free Halv

- **Free Halvs are offensive damage only.** Any Halv that does something else (healing, a status, a debuff) costs MP.
- **Halvlak** costs MP and heals half as much as Lak. Healing is never free.
- **Riders begin at the base tier.** A free Halv deals plain damage, so nothing stacks for free.
- Wherever a free Halv comes from (slotted, weapon, or accessory), it costs nothing.
- Whether a non-damage family gets a Halv tier at all is a curation call, family by family.

### The Full Grid (Locked names; curation happens in class trees)

Every combination is recorded for posterity. Which ones a class actually gets is decided when designing class trees.

#### Single Target

| Root | Halv | Base | Mer | Jatte | Ur |
|---|---|---|---|---|---|
| Eld | Halveld | Eld | Mereld | Jatteld | Ureld |
| Reyk | Halvreyk | Reyk | Mereyk | Jattereyk | Ureyk |
| Vatn | Halvatn | Vatn | Mervatn | Jattevatn | Urvatn |
| Hrim | Halvhrim | Hrim | Merhrim | Jattehrim | Urhrim |
| Blast | Halvblast | Blast | Merblast | Jatteblast | Urblast |
| Blixt | Halvblixt | Blixt | Merblixt | Jatteblixt | Urblixt |
| Jord | Halvjord | Jord | Merjord | Jattejord | Urjord |
| Gro | Halvgro | Gro | Mergro | Jattegro | Urgro |
| Sol | Halvsol | Sol | Mersol | Jattesol | Ursol |
| Lak | Halvlak | Lak | Merlak | Jattelak | Urlak |
| Natt | Halvnatt | Natt | Mernatt | Jattenatt | Urnatt |
| Aska | Halvaska | Aska | Meraska | Jattaska | Uraska |

#### All Targets

| Root | Halv | Base | Mer | Jatte | Ur |
|---|---|---|---|---|---|
| Eld | Allhalveld | Alleld | Allmereld | Alljatteld | Allureld |
| Reyk | Allhalvreyk | Allreyk | Allmereyk | Alljattereyk | Allureyk |
| Vatn | Allhalvatn | Allvatn | Allmervatn | Alljattevatn | Allurvatn |
| Hrim | Allhalvhrim | Allhrim | Allmerhrim | Alljattehrim | Allurhrim |
| Blast | Allhalvblast | Allblast | Allmerblast | Alljatteblast | Allurblast |
| Blixt | Allhalvblixt | Allblixt | Allmerblixt | Alljatteblixt | Allurblixt |
| Jord | Allhalvjord | Alljord | Allmerjord | Alljattejord | Allurjord |
| Gro | Allhalvgro | Allgro | Allmergro | Alljattegro | Allurgro |
| Sol | Allhalvsol | Allsol | Allmersol | Alljattesol | Allursol |
| Lak | Allhalvlak | Allak | Allmerlak | Alljattelak | Allurlak |
| Natt | Allhalvnatt | Allnatt | Allmernatt | Alljattenatt | Allurnatt |
| Aska | Allhalvaska | Allaska | Allmeraska | Alljattaska | Alluraska |

That's **120 spells** from **12 roots** and **5 prefixes**.

### Stat Lines (Locked)

Buffs and debuffs that move stat stages. They add a **direction** to the grammar:

```
[Target] + [Tier] + Direction + Root
   All-  +  Mer-  +   Auk-    + Vig   =  Allmeraukvig  ("Whole team, +2 evasion")
```

| Stat | Root | Read |
|---|---|---|
| ATK | **Kraft** | Swedish *kraft*, "force" |
| DEF | **Skold** | Swedish *sköld*, "shield" |
| MAT | **Seid** | ON *seiðr*, "sorcery" (Swedish *sejd*) |
| MDF | **Stav** | "Stave," as in *galdrastafir*, the protective Icelandic magic staves |
| ACC | **Hitt** | Reads as English "hit"; Swedish/ON *hitta*, "to find, to hit" |
| EVA | **Vig** | Swedish *vig*, "nimble" |
| SPD± | **Rask** | ON *röskr*, Swedish *rask*, "quick" |

| Direction | Prefix | Source |
|---|---|---|
| Up | **Auk-** | ON *auka*, "to increase" (Swedish *öka*) |
| Down | **Ned-** | Swedish *ned*, "down" |

- **Tier sets how many stages:** base is 1, Mer is 2, Jatte is 3.
- **No Halv tier** (there's no half a stage). Ur versions live on gear.
- Stat lines are **guaranteed**, unlike statuses.

| | Up (team) | Down (enemy) |
|---|---|---|
| ±1 | Aukskold | Nedskold |
| ±2 | Meraukskold | Mernedskold |
| ±3 | Jatteaukskold | Jattenedskold |
| All, ±2 | Allmeraukskold | Allmernedskold |

### Status Roots (Locked model)

Statuses aren't owned by schools. They're **their own roots in a shared grab bag**, handed out to classes by curation. A class gets a status line because it rhymes with the class fantasy, not because a school owns it.

- **Tier sets the odds** of the effect landing, and **All-** sets how many targets.
- **Statuses take no direction.** Auk and Ned are only for stat lines.
- Status Halvs, if they exist, cost MP.

| Root | Inflicts | Source |
|---|---|---|
| **Eitr** | Poisoned | ON *eitr*, "venom" (Swedish *etter*). Venom from the rivers Élivágar formed the first giant, Ymir; at Ragnarök, Thor dies of the world serpent's venom. |
| **Mogl** | Disarmed | Swedish *mögel*, "mold": rot that eats things, not people |
| **Blinda** | Blinded | Swedish *blinda*, "to blind" |
| **Nid** | Cursed | ON *níð*; the *níðstǫng* was a rune-carved "scorn-pole" raised to curse an enemy. Swedish *nid* still means a malicious lampoon. |
| **Ogn** | Feared | ON *ógn*, "terror, dread" |
| **Helvad** | Death (chance) | Hel, the death goddess, + Swedish *vad*, "a bet." Swedish *hel* also means "whole," so a Swede hears "all-in." |
| **Bann** | Silenced | ON and Swedish *bann*, "ban, prohibition." Reads as restrictive. |
| **Skolja** | (Cleanse) | Swedish *skölja*, "to rinse." Washes away an ally's statuses and lowered stages. |

Every status line follows the same grid pattern. Eitr, for example:

| | Halv | Base | Mer | Jatte | Ur |
|---|---|---|---|---|---|
| Single | Halveitr | Eitr | Mereitr | Jatteitr | Ureitr |
| All | Allhalveitr | Alleitr | Allmereitr | Alljatteitr | Allureitr |

**Helvad** is a straight chance-of-death line, like SMT's Mudo. It exists, but it's rarely handed out and lives mostly on gear.

**Lokavad** ("Loki's wager") is a bespoke signature spell, not a line: a high chance to instantly kill, but if it fails, the caster dies. Loki once bet his own head in a wager with the dwarf Brokkr and lost, escaping only by arguing that the dwarf had no claim to his neck.

### Martial Skill Families (Draft)

- **Blot** inflicts Bleeding. From ON *blót*, the pagan blood-sacrifice (Swedish *blod*, "blood"). Assigned to the growth patterns of certain martial classes, mostly Slash and Pierce.
- Other families are still to be designed: flat-HP-cost ladders such as cheap and weak, always-first, last-but-heavy, and pay-more-for-more.

### Costs (Locked)

Every spell, skill, and line carries a cost tag:

| Cost | Suits | Example |
|---|---|---|
| **MP** | Casters, and anyone dipping in through gear | Eitr, Blinda |
| **HP** | Martials; anything paid in blood | Blot |
| **MP + HP** | Hybrid builds and dramatic moves | A desperate spell that costs both |

Everyone has both pools, so a martial wearing an MP-cost accessory spell draws on a small MP pool, and WIS becomes a real choice for martials.

---

## Part 3: Elements and Statuses (Draft)

### Element Personalities

Elements aren't reskins of damage. Each one turns different **knobs**: power (damage per cast), efficiency (damage per mana), variance (how swingy), spread (how many All- spells), and rider (the extra effect).

| Element | Role | Power | Efficiency | Variance | Spread | Rider |
|---|---|---|---|---|---|---|
| Eld | Glass cannon: burns hot, runs out | Highest | Low | Low | Mid | — |
| Reyk | Smoke: patches Fire's weakness | Low | Mid | Low | Mid | Accuracy down |
| Vatn | Mirrors Fire: nearly as hard, cheaper, wins long fights | High | High | Low | Mid | — |
| Hrim | Keeps Water's power, adds control | High | Mid | Low | Mid | Chill → Freeze |
| Blast | Weak, spreadable, multi-hit gusts | Low | High | Low | Very high | — |
| Blixt | Spiky single target, almost no All- spells | Very high | Low | Very high | Very low | Stun |
| Jord | Reliable: cheapest, zero variance, every slot filled | Mid | Highest | None | Full | — |
| Gro | Owns time: thorns, entangle, venom | Low upfront | Mid | Low | Mid | Damage over time |
| Sol | Smite, strong against Dark and undead | — | — | — | — | — |
| Lak | Healing only; All- becomes a party heal | — | — | — | — | — |
| Natt | **Shadow** damage | — | — | — | — | — |
| Aska | **Decay:** small Natt damage | Low | — | — | — | Chance to Curse (rolls Nid) |

**Damage shapes:** Eld and Blixt land one big hit, Blast lands several small ones (a way around evasion), Gro lands damage over several turns, and Jord is the steady middle.

**Riders vs. lines:** riders on damage spells are low-chance bonuses. The reliable version of an effect comes from a dedicated line (stat line or status root). Tier scales a rider's *chance*, not its size. Whether a rider lands could be a contest of caster WIL vs. target WIL.

**Parents are pure, children carry riders.** Eld, Vatn, Blast, Jord, Sol, and Natt deal clean damage (or healing). Their children add the extra effect: Reyk's accuracy down, Hrim's Chill, Blixt's Stun, Gro's damage over time, Aska's Curse.

### Statuses

| Status | Source | Effect |
|---|---|---|
| **Poisoned** | Eitr | Damage at the start of each numbered round |
| **Bleeding** | Blot (martial) | Damage when the character goes to act, then a death check |
| **Chilled** | Hrim rider | −1 SPD± |
| **Frozen** | Hrim on a Chilled target | Lose turns for a duration rolled when Frozen lands. Any damage breaks it and deals a bonus **Shatter**. |
| **Disarmed** | Mogl | Weapon off for N rounds, as if unequipped: lose its stat bonuses and signature move. The class tree still works. |
| **Stunned** | Blixt rider | Lasts N rounds. Each time the character acts, a chance to lose that action. Clears the first time it costs one, so it never costs more than one action. |
| **Blinded** | Blinda | −1 ACC and −1 EVA (can't aim *or* dodge) |
| **Cursed** | Nid; Aska rider | Two random stage-downs among ATK, MAT, DEF, MDF (duplicates allowed, so a −2 on one stat is possible) for N rounds; Ur adds duration. Can't be re-cursed while Cursed. |
| **Feared** | Ogn | Acts last. Feared characters rank among themselves by SPD. |
| **Silenced** | Bann | Can't use anything that costs MP. Free moves (free Halvs and strikes) still work. |

**Notes**
- **Freezing is earned:** no dedicated Frozen line exists. Frozen comes only from Hrim on a Chilled target, plus bespoke gear such as a "Freeze in Place" signature. Lost turns are the strongest effect in a turn-based game, so freezing takes setup.
- **Chill (draft):** a chance on any Hrim hit, guaranteed on a Weak hit.
- **Frozen vs. Stunned:** Frozen takes setup, costs several turns for certain, and can be broken. Stunned is instant but costs at most one action.
- **Shatter** is a real decision: keep the enemy frozen to skip its turns, or cash in for the burst.
- **Poisoned vs. Bleeding:** Poison comes from magic and ticks with time. Bleed comes from blades and punishes acting.

---

## Part 4: Affinity and Turns (Locked)

### Two Layers

- **MDF** is a number: how much magic hurts in general.
- **Affinity** is a category per element: what happens when you're hit with that particular element.

### The Ladder

Borrowed from SMT's affinity system, minus its Repel step.

| Affinity | Damage | Tempo |
|---|---|---|
| Weak | ×1.5 | Attacker earns a place in the **Bonus Round** |
| Normal | ×1 | — |
| Resist | ×0.5 | — |
| Null | 0 | Attacker **loses** tempo |
| Absorb | Heals target | Attacker **loses** more tempo |

There is a **single Weak level.** No stacked 2× tier. **Repel** (bounces the spell back) is held in reserve as a possible rare sixth step.

### Turn Structure

*Superseded for the slice by **combat_spec.md** (Parts 2 and 3): intents, speed groups, and Fear dropping actions to the −1 group.*

1. **Declare:** everyone chooses an action before the round starts.
2. **Resolve by SPD:** actions happen in SPD order. If someone's SPD changes before they act, they're re-ranked.
3. **Feared** characters act last, ranked among themselves by SPD.

### The Bonus Round

- Everyone who scored a **Weak!** hit during the round, on either side, joins a **Bonus Round** after it.
- The Bonus Round works like a normal round (declare, then resolve by SPD), but only those who hit a weakness take part.
- **No chaining:** a Weak hit in a Bonus Round doesn't earn another. A new Bonus Round only comes from the next numbered round.
- **Anything goes:** attack, defend, heal, use an item.
- **Bonus Rounds are outside time.** Only numbered rounds tick durations, so Poison doesn't tick twice and Frozen enemies don't thaw early.
- **Bleeding still triggers,** because it fires on acting, not on time passing. **Stunned** still rolls when you act.

### Inheritance

Affinity is **school-wide by default.** A creature that resists Eld resists Reyk too, and the reverse. Overrides are deliberate exceptions: a water elemental might resist Vatn but be weak to Hrim, because it freezes solid.

### The Two Cycles

- **Outer cycle (parents):** Vatn → Eld → Blast → Jord → Vatn. Water douses fire, fire eats the air, wind erodes earth, earth dams water.
- **Inner cycle (children):** Hrim → Gro → Blixt → Reyk → Hrim.

**Every child element counters its parent's predator.** A Fire user facing a water creature switches to Reyk. A Wind user facing fire switches to Blixt.

| School | Resists | Weak to |
|---|---|---|
| Eld (Eld, Reyk) | Eld, Reyk | Vatn, Blixt |
| Vatn (Vatn, Hrim) | Vatn, Hrim | Jord, Reyk |
| Blast (Blast, Blixt) | Blast, Blixt | Eld, Gro |
| Jord (Jord, Gro) | Jord, Gro | Blast, Hrim |

**Sol and Natt** sit outside the cycle and are each weak to the other.

### Martial Damage Types

Physical attacks carry one of three types: **Crush, Pierce, Slash.** These form a grid of authored class identities rather than a cycle (Part 6).

---

## Part 5: Characters (Draft)

### Birth

Characters are born, roll their traits, and then the player meets (and may recruit) them. They're born with their class in hand and never change it. Recruiting is the real game: reading a roll and deciding whether it's worth hiring.

**Birth order:** genes (base attributes) → Personality → Star Sign → Class.

- **Personality** changes how a character develops: one boosted attribute and one reduced (7 × 6 = **42 personalities**, no neutral option). Example: Brave is +STR / −SPD.
- **Star Sign** changes the *shape* of current attributes and sets one axis of affinity (Part 7). Its attribute bonus and penalty equal 10% of the character's highest base attribute, calculated from base attributes after Personality but before the sign itself, excluding equipment, with an explicit minimum attribute value.
- After birth, the player develops the character: weapon upgrades, new skills and spells from the class tree, and points allocated on level-up.

### Attributes

STR, CON, SPD, DEX, WIL, INT, WIS.

Proposed mapping to combat stats:

| Attribute | Drives |
|---|---|
| STR | ATK |
| CON | Max HP, DEF |
| SPD | Turn order, EVA |
| DEX | ACC, crit chance |
| INT | MAT (spell power) |
| WIS | Max MP, MDF |
| WIL | Status resistance and rider chance |

### Stage Effects

Combat stats that can be staged: **ATK, DEF, MAT, MDF, ACC, EVA, SPD±** (labeled SPD± to tell it apart from the SPD attribute).

The scale runs **−5 to +5**, 11 stages including 0. Stages move combat stats, never the underlying attributes.

Proposed multipliers: **(3 + n) / 3** for buffs and **3 / (3 − n)** for debuffs. That gives +5 = ×2.67 and −5 = ×0.375, strong enough to matter with no single cast ending a fight, and buffs and debuffs mirror each other.

### Weapon Scaling (inherited from an earlier game; to be remapped onto the class roster)

| Weapon | Scaling | Channel |
|---|---|---|
| Maul, Club | STR 100 | ATK |
| Warhammer | STR 75 / CON 25 | ATK |
| Sword & Shield | STR 50 / CON 50 | ATK |
| Greatsword | STR 50 / DEX 50 | ATK |
| Spear | STR 50 / SPD 50 | ATK |
| Daggers | DEX 50 / SPD 50 | ATK |
| Bow | DEX 100 | ATK |
| Elemental focus | INT 100 | MAT |
| Natt focus | INT 50 / WIL 50 | MAT |
| Sol focus | WIS 100 | MAT |

Pure scaling has a high ceiling but is fragile to bad rolls; split scaling is forgiving.

---

## Part 6: Classes

### Class Rules (Locked)

- **The class absorbs the weapon.** It sets damage type, stat scaling, weapon class, and one axis of affinity.
- **Caster classes** carry elemental affinities: resist their home school, weak to its predators. They take their *martial* resist and weakness from the Star Sign.
- **Martial classes** carry martial affinities: a damage type and a different weakness. They take their *elemental* resist and weakness from the Star Sign.

### Loadouts and Trees (Locked)

- **The tree lives on the person.** A class unlocks its spells or skills as it grows. A maxed character has its whole tree available. Class trees top out at **Jatte**.
- **Battle loadout:** 4 chosen slots, plus up to 1 from the weapon and 1 from an accessory, for a maximum of 6.
- **No basic attack.** Free Halvs (casters) and free strikes (martials) fill that role. A caster who slots four expensive spells can run dry; that's a deliberate risk.

### Gear (Locked)

- **Weapon class is the category; items are named freely.** Brennumars wield Brands: Initiate's Brand, Burning Branch, Surtsstafr.
- **Weapons are class-locked by weapon class.** Only Brennumars wield Brands.
- **Weapon signature moves** work only while equipped and can **never be learned,** so "crazy move or better stats" stays a real decision for the whole game. Pocket words (Smed, Sten) and one-offs like Heat Weapon or Freeze in Place are natural signature moves.
- **Ur spells exist only on gear.** Ur gear carries a class tag (for example, *Class: Brennumar*), and nobody else can use it.
- **Draft:** weapon moves deepen the class; accessory moves reach outside it (a Lak ring for a Brennumar, a Halveld necklace for a Huskarl).

### Resources (Locked)

- **Casters spend MP.** Offensive damage Halvs are free.
- **Martials spend HP.** Skills have a flat HP cost, set when each skill is made. A skill can be used only if current HP is **greater than** its cost: at 11 HP a 10 HP skill takes you to 1; at 10 or less it's unavailable.
- **Martial free strike:** 0 HP, weak, deals the class's damage type. The martial equivalent of a free Halv.
- **Lak is the martials' fuel.** Healing refills what they spend, so healers and martials depend on each other.
- **Open:** whether the Berserker can pay past the HP limit and drop to 1, or into death.

### Martial Roster (Locked)

The six martial classes cover every pairing where the damage dealt differs from the weakness: 3 × 2 = **6 classes**. That's the same arithmetic as the zodiac's martial half, so the two systems mirror each other. Each damage type appears twice, and each weakness appears twice. Six martials and six casters make a healthy test bed.

| | Weak to Slash | Weak to Pierce | Weak to Crush |
|---|---|---|---|
| **Does Pierce** | Ullar | — | Nalarbani |
| **Does Slash** | — | Hersir | Huskarl |
| **Does Crush** | Berserker | Vasara | — |

| Class | Concept | Name source |
|---|---|---|
| **Ullar** | Bowman. Kills from range; helpless once a blade reaches them. | Ullr, the Norse god of the bow, skis, and the hunt, + -ar |
| **Nalarbani** | Stiletto, the knight-killer. Slips cuts and points, folds under a heavy blow. | ON *nál* ("needle") + -ar + *-bani* ("slayer"). In Norse, *-bani* names the victim, so it reads "slayer of needle-men." |
| **Hersir** | Champion of the people. Two-handed greatsword, no shield, so arrows and spears get through. | ON *hersir*, a district war-leader |
| **Huskarl** | Axe and mail coat. Mail stops cuts, but blows go straight through. | ON *húskarl*, household warrior |
| **Berserker** | Club or maul, bare-chested, cut to pieces if a blade gets in. | ON *berserkr*, "bear-shirt" |
| **Vasara** | Shield-hammer. The shield takes cuts and blows; points slip past the rim. | Finnish *vasara*, "hammer," traced to an old Indo-Iranian loan related to Sanskrit *vajra* |

### Pocketed Martial Classes

These six left the active roster when it condensed. Any skills and content they would have had are open to the six active classes. They may return later as advanced or prestige classes.

| Class | Was | Concept | Name source |
|---|---|---|---|
| **Geiras** | Pierce / Slash | Pikeman. Huge reach; helpless once a blade gets inside. | ON *geirr*, "spear" (coined) |
| **Stikkar** | Pierce / Pierce | Rapier fighter. The only thing that beats a rapier is another rapier. | *stikk-*, the stab (Swedish *sticka*), + -ar |
| **Maekir** | Slash / — | Blademaster. One sword, parries everything. | ON *mækir*, poetic "sword" |
| **Holmgar** | Slash / Slash | Duelist. Lives by the sword. | ON *hólmganga*, the island duel, + -ar; echoes Holger Danske |
| **Atgeir** | Crush / — | Ironclad. Full plate and halberd. | ON *atgeirr*, Gunnar's nearly unbeatable polearm in *Njáls saga* |
| **Glimar** | Crush / Crush | Wrestler. Traps blades and turns points, but a heavy blow lands on the body. | ON *glíma*, Norse folk wrestling, + -ar. Thor lost a wrestling match only to Elli, Old Age herself. |

### Caster Roster (Locked)

| School | Class | Concept | Weapon class | Resists | Weak to |
|---|---|---|---|---|---|
| Eld | **Brennumar** | The Tactical Arsonist: burns and vanishes | **Brand** | Eld, Reyk | Vatn, Blixt |
| Vatn | **Hafrunar** | The patient attritionist: wears you down, holds you in ice | **Net** | Vatn, Hrim | Jord, Reyk |
| Blast | **Skurmar** | The storm-caller: gusts that spread, lightning that strikes | **Knotted Cord** | Blast, Blixt | Eld, Gro |
| Jord | **Lundar** | The grove-keeper: reliable earth, patient growth | **Tool** | Jord, Gro | Blast, Hrim |
| Sol | **Dagskald** | The singer-healer: mends with song, smites with daylight | **Instrument** | Sol | Natt |
| Natt | **Seidar** | The sorcerer of shadow and decay: curses, fear, death on the side | **Staff** | Natt | Sol |

| Class | Name source | Example items |
|---|---|---|
| **Brennumar** | ON *brennumenn*, "burners": the men who carried out saga house-burnings, such as the Burning of Njál | Initiate's Brand, Burning Branch, *Surtsstafr* ("Surtr's Stave"). Brand from ON *brandr*, a burning stick. |
| **Hafrunar** | ON *haf* ("the open sea") + *rúnar* ("runes, secrets"): "sea-secrets." Hafrún is a real Icelandic name. | Fisher's Net, Drowned Man's Seine, **Rán's Net** (the sea goddess drowns sailors in her net) |
| **Skurmar** | ON *skúr*, Swedish *skur*, "squall," + -mar | Hedge Wizard's Leather Strip, Sailor's Three-Knot Cord, **The Fourth Knot**. Norse sailors believed Finnish and Sámi sorcerers sold wind tied in knots: one for a breeze, two for a strong wind, three for a storm. |
| **Lundar** | ON *lundr*, Swedish *lund*, "grove." Germanic peoples worshipped in sacred groves, as at Uppsala. | Sickles, picks, and other tools; Tapio's Sickle |
| **Dagskald** | Swedish *dag*, "day," + skald. Germanic healing magic was sung (*galdr*, from *gala*, "to chant"). | Harps (ON *harpa*), flutes, horns; the Bronze Age *lur* |
| **Seidar** | ON *seiðr*, the shadowy, disreputable Norse sorcery of divination, curses, and bending minds | Staffs. *Vǫlva* ("seeress") is usually explained as "staff-carrier," from *vǫlr*, and seeresses were buried with iron staffs. Helvad and Lokavad live on a few rare staffs. |

**Example Brennumar build:** status kit of Eitr, Mereitr, and Alleitr; loadout of Allhalveld, Allhalvreyk, Allmereld, Jatteld.

---

## Part 7: The Zodiac (Locked)

Each sign resists one of the four parent elements and is weak to a different one. There are exactly 4 × 3 = **12** such pairs, so every pairing gets exactly one sign. Children inherit as usual (Resist Blast also covers Blixt). The martial half works the same way: 3 × 2 = 6 pairs, each appearing on two signs.

Characters read the half their class doesn't cover.

| # | Sign | Image | Resists | Weak to | Martial (Resist / Weak) | Family | Source |
|---|---|---|---|---|---|---|---|
| 1 | **Arin** | Hearth | Eld | Vatn | Slash / Pierce | Natural | ON *arinn*; also echoes Sámi *árran* |
| 2 | **Kerti** | Candle | Eld | Blast | Crush / Slash | Inverted | ON *kerti* |
| 3 | **Eimyr** | Ember | Eld | Jord | Pierce / Crush | Crossed | ON *eimyrja* |
| 4 | **Mierka** | Fog | Vatn | Eld | Pierce / Slash | Inverted | Northern Sámi *mierká* |
| 5 | **Knarr** | Ship | Vatn | Blast | Slash / Crush | Crossed | ON *knǫrr*, cargo ship |
| 6 | **Johka** | River | Vatn | Jord | Crush / Pierce | Natural | Northern Sámi *johka*; Finnish *joki* |
| 7 | **Bjark** | Birch | Blast | Eld | Slash / Crush | Natural | ON *bjǫrk*; the rune ᛒ, *berkanan* |
| 8 | **Varde** | Cairn | Blast | Vatn | Crush / Pierce | Crossed | ON *varða*, Swedish *varde* |
| 9 | **Hrafn** | Raven | Blast | Jord | Pierce / Slash | Inverted | ON *hrafn* |
| 10 | **Otso** | Bear | Jord | Eld | Crush / Slash | Crossed | Finnish *otso*, a poetic avoidance name |
| 11 | **Myyra** | Mole | Jord | Vatn | Pierce / Crush | Inverted | Finnish *myyrä* ("vole"; *maamyyrä*, the mole) |
| 12 | **Bauta** | Standing Stone | Jord | Blast | Slash / Pierce | Natural | ON *bautasteinn*, memorial stone |

### Families

- **Natural:** weak to their element's predator in the outer cycle. They behave like a creature of that school.
- **Inverted:** weak to their element's *prey*. The odd births: the Candle is fire beaten by the very wind fire normally eats.
- **Crossed:** weak to an element outside the predator-prey line.

Grouped by what they resist, the signs form four groups of three, mirroring how the Western zodiac groups its signs by element.

### Lore Notes

- **Otso** is fitting because the bear's name was taboo across the north. *Björn* means "the brown one," and Finnish poetry calls the bear *mesikämmen*, "honey-paw."
- **Arin** works in two worlds: Norse *arinn* and Sámi *árran* both mean hearth. They're unrelated, but they sound alike.
- The Sámi forms should get a check from a speaker before anything ships.

---

## Part 8: Game Modes (Draft)

The system could support several games. No mode is chosen yet; the plan is to iterate, then build a Python simulation.

### Shared Foundation

- **A Company** hires rolled characters (birth sheets: genes, Personality, Star Sign, class) and fields **3** at a time.
- Characters grow through their class's unlock track and survive (or don't) across expeditions.
- Gear can carry a **rank tag** alongside the class tag: a new hire can't use certain gear until they reach that rank.
- This could also become the continuation of ISEKAI, the earlier Company crawler, if wanted.

### Mode A: Loadout RPG

The Pokémon, SMT, and Dragon Quest model.

- Each class learns about **20 curated moves** on a track from level 1 to 100, starting with its free strike or free Halv.
- Before an expedition, pick **4**, plus up to **2** from gear (Part 6).
- 20 options feeding 4 slots leaves room for 3 or 4 distinct builds per class.
- Uses the economy as written: MP, free Halv, flat HP costs.

### Mode B: Card Battler

Slay the Spire structure, with three adventurers.

- **Starter deck (9 cards):** Attack ×3 (the free strike, or a free Halv for casters), Defend ×3 (DEF up for this turn), Special ×3 (class-specific). Example Seidar specials: Natt, Aska, Blinda.
- **The class unlock track** adds cards that compete for the Special 3.
- **Each round, each character draws 3 and plays 1.** The other two go to the graveyard; the deck recycles on deck-out. A 9-card deck cycles every three rounds.
- **Controls:** click a card, drag to a target or area, release; repeat for each character; press Fight!; watch the round resolve in SPD order.
- **Runs:** a node map; each node fades to a battle or event screen. Party on the left facing right, enemies on the right facing left.
- **Costs stay:** casters drain MP, martials pay HP. Percent costs fit this mode:
  - **% of max HP** (default) is a real cost and pairs with the "current HP must exceed the cost" rule.
  - **% of current HP** can never kill and gets cheaper as you're hurt; reserved for specific cards, such as a Berserker's desperation move.
  - Percent costs mean CON buys a bigger pool, not more uses, unlike the flat costs in Mode A.
- **Bonus Round:** a character who hits a weakness plays one of the two cards they *didn't* pick, before those cards go to the graveyard.
- Jatte and Ur cards are held back by rarity and deck slots rather than MP alone.

### Mode C: Auto-Battler

A Super Auto Pets–style shop and merge game.

- **Each unit has one line:** its class's tier ladder. Combining duplicates steps it up: Halveld → Eld → Mereld → Jatteld.
- **One branch per unit:** go *deeper* (higher tier, one target), go *wider* (All-), or branch into the child element. Because parents are pure and children carry riders, branching into Reyk or Hrim is how a unit gains its rider.
- **Martials:** the line is their strike; the branch is one skill family (such as Blot for Bleeding).
- **Birth sheets make the shop interesting:** two Brennumars differ by sign and Personality, so team building means reading affinities and stacking signs.
- **Bonus Round** shows up as a visible "Weak!" extra action.
- Also the accoutrements of the genre: mutators, +1s, curses.
- **Doubles as a headless balance simulator:** run thousands of fights to check whether Blixt is too spiky or Jord too reliable.

### Rites

Out-of-combat rituals between characters.

**Combine** (auto-battler): the everyday same-class merge. Two portraits collide, there's a shine, one remains, and its tier steps up. Light and frequent.

**Erfi** (ON *erfi*, the feast at which an heir formally took up the inheritance):
- **Card battler:** a character who retires leaves one card to a chosen heir. The card competes for the heir's Special 3, so the deck stays at 9. Each heir can inherit **at most twice**. Defends stay off-limits except at dedicated deck-thinning events.
- **Auto-battler:** the rare cross-class merge, where the parent absorbs the other's ability. It gets a heavier animation, so it feels like a rite rather than routine.
- **Cross-class cards cap at Mer.**

**Communion** (parked):
- If it returns: a rare event where, for something like 1,000g, two characters each swap one Special card permanently.
- Both get a **communion flag** and can never do it again. The cross-class Mer cap applies.
- Name if it returns: **Blodsbroder**. In *Gísla saga*, sworn brothers mix their blood in the earth beneath a raised strip of turf.

### The Choice Bucket

Every mode shares the same tension: **dump** a character, **power them up**, or **merge** them into someone else. The birth sheets are what make that a real decision.

---

## Part 9: Encounter v0 (Draft numbers, approved for testing)

These are the numbers the Python sim runs on (`sim/data.py`, `sim/engine.py`, `sim/run.py`). Every one is a knob.

### Attributes

- **Genes** roll 0–31 per attribute.
- **Attribute** = 10 + gene/2 at level 1, growing (0.6 + gene/50) per level. A gene of 0 grows 0.6 per level; a gene of 31 grows about 1.22.
- **Personality:** the boosted attribute grows 20% faster, the reduced one 20% slower.
- **Class arrival (weighted random):** after genes, Personality, and Star Sign, the class is rolled with chances weighted toward the body it suits (each class's fit raised to the 9th power). About two in three recruits are natural fits; the rest are odd births, which produce about four-fifths of a natural fit's output.
- **Class tilt:** a class makes the attributes that feed its weapon grow up to 50% faster (split by weight), and every other attribute grows slightly slower to pay for it.
- **Training:** 1 point per level (current default). The alternative, 2 points per level with no more than 1 into the same attribute, more than doubled win rates in testing, so it's held in reserve.
- **Star Sign:** ±10% of the highest attribute, applied after Personality and training. Which attributes each sign shifts is a placeholder.
- Fractions are kept internally; whole numbers are shown.

### Derived Stats

- **HP** = 3 × (20 + 2×CON + 2×Level). The ×3 is tuned so fights at level 30 last about 7 rounds. **MP** = 10 + WIS + Level.
- **ATK and MAT are class-weighted;** DEF = CON, MDF = WIS. DEX raises crit chance; SPD sets turn order.

| Class | ATK / MAT weights |
|---|---|
| Brennumar, Hafrunar, Skurmar, Lundar | MAT: INT |
| Dagskald | MAT: WIS |
| Seidar | MAT: INT 50 / WIL 50 |
| Ullar | ATK: DEX |
| Nalarbani | ATK: DEX 50 / SPD 50 |
| Hersir | ATK: STR 50 / DEX 50 |
| Huskarl | ATK: STR 75 / CON 25 |
| Berserker | ATK: STR |
| Vasara | ATK: STR 50 / CON 50 |

**Reference people** (all genes equal, no Personality, Sign, or training; HP shown before the ×3):

| Level | Gene 0: attribute / HP / MP | Average (15.5) | Gene 31 |
|---|---|---|---|
| 1 | 10 / 42 / 21 | 18 / 58 / 29 | 26 / 73 / 36 |
| 10 | 15 / 71 / 35 | 26 / 92 / 46 | 36 / 113 / 56 |
| 50 | 39 / 199 / 99 | 62 / 245 / 122 | 85 / 291 / 145 |
| 100 | 69 / 359 / 179 | 108 / 436 / 218 | 146 / 513 / 256 |

### Damage

**Damage = Power × element multiplier × (attack ÷ defense) × (0.6 + Level/20) × affinity × roll result × variance.** Physical moves use ATK vs. DEF; magic uses MAT vs. MDF. Defending halves damage taken that round.

The level factor keeps the anchor steady: **a base spell takes about four hits to down an equal** at every level.

| Tier | Power | MP cost | Learned from |
|---|---|---|---|
| Halv | 10 | Free (damage only) | Level 1 |
| Base | 20 | 8 | Level 1 |
| Mer | 28 | 16 | Level 20 |
| Jatte | 38 | 32 | Level 50 |
| Ur | 50 | Gear-priced | Gear only |

- **All-:** ×1.5 cost, ×0.75 power per target.
- **Halvlak:** costs 4 MP, heals half as much as Lak.
- **Martial HP skills** mirror the ladder: 8 / 16 / 32 HP. The free strike has Power 10.

| Element | Power | Cost | Notes |
|---|---|---|---|
| Eld | ×1.15 | ×1.25 | Hits hardest |
| Reyk | ×0.80 | ×1.00 | Rider: −1 ACC |
| Vatn | ×1.00 | ×0.75 | Efficient |
| Hrim | ×1.00 | ×1.00 | Rider: Chill → Freeze |
| Blast | ×0.45 per hit, 2 hits | ×0.75 | Each hit rolls separately |
| Blixt | ×1.25 | ×1.25 | ±40% variance; rider: Stun |
| Jord | ×1.00 | ×0.70 | No variance |
| Gro | ×0.70 | ×1.00 | Rider: Poison |
| Sol, Natt | ×1.00 | ×1.00 | — |
| Aska | ×0.60 | ×1.00 | Rider: Curse |

Default variance is ±10%.

### Graze / Hit / Crit

Every attack connects; one roll decides how well.

- **Base:** Graze 20% (×0.5 damage, no riders), Hit 75%, Crit 5% (×1.5 damage). Only Weak hits earn a Bonus Round; crits just deal damage.
- **Net stage** = attacker's ACC stage − defender's EVA stage, capped at ±5. Each step moves 10% between Graze and Hit. Past +2, each further step adds 5% Crit.
- **DEX bonus:** +DEX/20 % crit chance, taken from Hit.
- **Speed shift:** compare the attacker's effective SPD (body, SPD± stages, and Chilled included) with the defender's. Every 25% faster is +1 net stage, capped at ±2; the slower side gets the matching minus. It applies to spells as well as strikes. Fast units hit cleaner and are harder to hit cleanly; Aukrask, Nedrask, and Chilled now affect consistency as well as turn order.

| Net stage | Graze | Hit | Crit | Expected damage |
|---|---|---|---|---|
| −5 | 70% | 25% | 5% | ×0.68 |
| −2 | 40% | 55% | 5% | ×0.83 |
| 0 | 20% | 75% | 5% | ×0.93 |
| +2 | 0% | 95% | 5% | ×1.03 |
| +5 | 0% | 80% | 20% | ×1.10 |

**DEF and MDF stages control damage. ACC and EVA stages control consistency and tempo** (riders and crits). SPD feeds consistency too, through the speed shift.

### Riders, Status Lines, Stat Lines

- **Riders** roll only on Hit or Crit. Base chance by tier: Base 20%, Mer 30%, Jatte 40%, Ur 50%. Free Halvs carry no riders.
- **WIL contest:** every rider and status chance is multiplied by caster WIL ÷ target WIL, capped between ×0.5 and ×1.5.
- **Chill** is guaranteed on a Weak Hrim hit and lasts **2–4 rounds**. Hrim against a Chilled target rolls for **Freeze**, which lasts **1–3 rounds**.
- **Status lines** (Eitr, Nid, Ogn, Blinda) use the same roll; a Graze fails. Chance by tier: Base 50%, Mer 75%, Jatte 90%.
- **Stat lines** (Auk, Ned) are guaranteed and last the whole battle.

### Status Numbers

| Status | Number |
|---|---|
| Poisoned | 8% of max HP at the start of each numbered round |
| Bleeding | 8% of max HP when the character goes to act, then a death check |
| Chilled | −1 SPD± for 2–4 rounds |
| Frozen | 1–3 rounds; the breaking hit deals ×1.5 (Shatter) |
| Stunned | 50% chance to lose an action; clears after costing one |
| Others | 3 numbered rounds |

### Healing

- An average healer's base Lak restores about **1.5× a base hit.** One healer outpaces one attacker; two attackers outpace one healer.
- Healing scales with the healer's MAT against the average for their level, plus the level factor.
- Healing never rolls.

### Also in Use for Testing

- **Null:** the attacker is barred from this round's Bonus Round. **Absorb:** also gives the target a Bonus Round entry.
- **KO:** 0 HP is down; a side wins when the other is fully down.
- **AI:** weighted toward expected damage, weaknesses, kills, and heals for allies below half HP; 80% best choice, 20% one of the top three.
- **Enemies:** six families (Ande, Draugr, Bein, Drattr, Djur, Oskorei), described in **bestiary.md**. The original six test creatures (Frost Wolf, Bog Archer, Ember Beetle, Grave Hound, Gale Harpy, Stone Troll) remain in the sim.

---
## Part 10: Move Catalog

Every move in the game, in one place. The **bestiary.md** companion shows which bodies carry them.

### Magic

- **Damage spells:** 12 roots × 5 tiers × single or All (the full grid, Part 2). Ur spells exist only on gear.
- **Healing:** the Lak line (Halvlak costs 4 MP; healing is never free).
- **Stat lines:** 7 roots × Auk/Ned × tier (Part 2).
- **Status and utility roots:** Eitr, Mogl, Blinda, Nid, Ogn, Helvad, Bann, and Skolja (Part 2).
- **Bespoke:** Lokavad, the high-risk death wager; Smed, Sten, and other signature moves still to be made.

### Party Martial Skills

Paid in HP by the hero who uses them (Part 6).

| Skill | Tier | Power | Cost | Notes | Used by |
|---|---|---|---|---|---|
| Strike | Halv | 10 | Free | The class's damage type | Every martial |
| Power Strike | Base | 20 | 8 HP | | Every martial |
| Great Strike | Mer | 28 | 16 HP | From level 20 | Every martial |
| Crushing Blow | Jatte | 38 | 32 HP | From level 50 | Every martial |
| Blot | Base | 14 | 8 HP | Can inflict Bleeding | Hersir, Nalarbani |
| Volley | Base | 15 each | 12 HP | Hits all enemies | Ullar |
| Reckless Strike | Base | 32 | 25% of current HP | Can't kill its user | Berserker |
| Aukskold | Base | +1 DEF | 8 MP | A stat line, not a strike | Huskarl, Vasara |

### Enemy Physical Moves

Free for enemies. Moves that can inflict a status have 70% of normal power.

| Move | Type | Tier | Power | Targets | Extra | Used by |
|---|---|---|---|---|---|---|
| Hammer | Crush | Halv | 10 | Single |  | Halvoskorei Hammer |
| Tail Slap | Crush | Halv | 10 | Single |  | Halvdrattr |
| Thrash | Crush | Halv | 8 each | All |  | Halvdrattr |
| Barrow Fist | Crush | Base | 20 | Single |  | Draugr |
| Ride Down | Crush | Base | 20 | Single |  | Ryttar |
| Tail Slap | Crush | Base | 20 | Single |  | Drattr |
| Trample | Crush | Base | 15 each | All |  | Ryttar |
| Barrow Fist | Crush | Mer | 28 | Single |  | Stordraugr |
| Breach | Crush | Mer | 28 | Single |  | Stordrattr |
| Maul | Crush | Mer | 28 | Single |  | Storoskorei Maul |
| Barrow Fist | Crush | Jatte | 38 | Single |  | Forndraugr |
| Falls Crash | Crush | Jatte | 38 | Single |  | Forsdrattr |
| Arrow | Pierce | Halv | 10 | Single |  | Halvoskorei Bow |
| Bite | Pierce | Halv | 10 | Single |  | Halvdjur |
| Bone Jab | Pierce | Halv | 10 | Single |  | Halvbein |
| Pack Snap | Pierce | Halv | 8 each | All |  | Halvdjur |
| Volley | Pierce | Halv | 8 each | All |  | Halvbein |
| Bite | Pierce | Base | 20 | Single |  | Djur |
| Blot | Pierce | Base | 14 | Single | Can inflict Bleeding | Storoskorei Stiletto |
| Spear | Pierce | Base | 20 | Single |  | Bein |
| Volley | Pierce | Base | 15 each | All |  | Bein, Storbein |
| Barbed Arrow | Pierce | Mer | 20 | Single | Can inflict Bleeding | Fornbein |
| Gore | Pierce | Mer | 28 | Single |  | Stordjur |
| Rain of Spears | Pierce | Mer | 21 each | All |  | Huntmaster |
| Spear | Pierce | Mer | 28 | Single |  | Storbein |
| Stiletto | Pierce | Mer | 28 | Single |  | Storoskorei Stiletto |
| Volley | Pierce | Mer | 21 each | All |  | Fornbein |
| Gore | Pierce | Jatte | 38 | Single |  | Forndjur |
| Axe | Slash | Halv | 10 | Single |  | Halvoskorei Axe |
| Claw | Slash | Halv | 10 | Single |  | Halvdraugr |
| Rake | Slash | Halv | 8 each | All |  | Halvdraugr |
| Blot | Slash | Base | 14 | Single | Can inflict Bleeding | Stordraugr |
| Cleave | Slash | Base | 15 each | All |  | Storoskorei Greatsword |
| Grave Axe | Slash | Base | 20 | Single |  | Draugr |
| Old Sword | Slash | Base | 20 | Single |  | Bein |
| Pack Rush | Slash | Base | 15 each | All |  | Djur, Stordjur |
| Rend | Slash | Base | 20 | Single |  | Djur |
| Spectral Blade | Slash | Base | 20 | Single |  | Ryttar |
| Sweep | Slash | Base | 15 each | All |  | Draugr, Stordraugr |
| Grave Axe | Slash | Mer | 28 | Single |  | Stordraugr |
| Greatsword | Slash | Mer | 28 | Single |  | Storoskorei Greatsword |
| Old Sword | Slash | Mer | 28 | Single |  | Storbein |
| Pack Rush | Slash | Mer | 21 each | All |  | Forndjur |
| Rend | Slash | Mer | 20 | Single | Can inflict Bleeding | Stordjur |
| Sweep | Slash | Mer | 21 each | All |  | Forndraugr |
| Hunt's Edge | Slash | Jatte | 38 | Single |  | Huntmaster |
| Old Sword | Slash | Jatte | 38 | Single |  | Fornbein |

### Status Effects in Brief

Poisoned, Bleeding, Chilled, Frozen, Disarmed (simplified for now: −1 ATK and −1 MAT), Stunned, Blinded, Cursed, Feared, Silenced, and death (Helvad). Full rules are in Part 3.

---

## Open Questions

**The big ones**
- **Tune from the sim:** fight length, Bonus Round frequency, training leverage, status play.
- **Choose the game:** loadout RPG, card battler, or auto-battler (Part 8).
- **Class trees:** which spells, skills, stat lines, and status lines each class actually gets. This is where the curation happens.
- **Martial skills:** Blot exists; the other skill families and their flat-HP-cost ladders don't yet.
- **Party size.**

**Smaller gaps**
- **Strip buffs:** homeless now that Mogl does Disarmed. A possible future status root (a dispel), if the game needs one.
- **Stat-stage duration:** do Auk and Ned stages last the whole battle, or expire after N rounds?
- **Status durations and cures:** N for each status, plus the items that cure them (antidotes, bandages).
- **Star Sign attribute shaping:** which attributes each sign raises and lowers.
- **Gear beyond weapons:** accessories exist as a slot, but there's nothing else yet, such as armor.

**Parked**
- Tuning numbers (damage, costs, rider odds, status durations)
- Remapping the weapon-scaling table onto the class roster
- Whether the Berserker can pay past the HP limit
- Repel as a sixth affinity step
- A Sámi speaker's check on the names
