# The Bestiary

The companion to **spellbook.md**. The spellbook describes what's possible through magic and skills; the bestiary describes **the bodies that deliver them**: every enemy family, its ranks, kits, affinities, lore, and numbers.

**Status key:** everything here is **Draft**, tuned against the Python sim (`sim/`), and ready for first playtests.

---

## Part 1: How Enemies Work

### The Slot Budget

- **Cost = slots = actions per round.** A cost-2 unit acts twice each round; a cost-3 unit acts three times.
- **A normal encounter fills 6 slots,** against a party of 3. The budget can rise or fall for difficulty.
- **Multi-action order:** everyone's first actions resolve before anyone's second, then everyone's third.
- **Bonus Rounds:** an enemy that hits a weakness earns one bonus action, just like a hero.

### Ranks

Every family uses the same ladder, so players learn it once. Ranks borrow the spell tier words players already know.

| Rank | Cost | HP | Typical kit |
|---|---|---|---|
| **Halv-** (fodder) | 1 | ×1 | Halv single, Allhalv |
| **Litel-** (Ande only) | 1 | ×1.2 | Base single, Allhalv |
| *(base)* | 2 | ×2 | Base single, base All, one extra |
| **Stor-** | 2 | ×2.5 | Mer single, base All, two extras |
| **Forn-** / **Drott-** / family title | 3 | ×3.5 | Jatte single, Mer All, a sovereign move |
| **Ur-** | 6 | — | In the pocket: ultra bosses |

**Every rank carries an All move one step up from where it started:** Halv ranks get Allhalv, standard ranks get the base All.

### Bodies

- **Each slot is "half a hero":** enemy HP ×0.5, and physical families' STR and INT ×0.5, so a 6-slot pack is a fair fight for 3 heroes.
- **Halv bodies hit hard:** Halv-rank enemies keep their Halv moves, but their bodies double their STR and INT. Fodder threatens like a standard unit and dies like fodder.
- **The Ande are pure casters** with no free strikes to fall back on, so they get MAT ×0.65 and double MP pools.
- **Enemies never pay HP.** Physical moves are free; spells and statuses cost MP.
- Every enemy has average genes, plus 0.25 extra growth per level in STR, INT, CON, and WIS.
- **Family bodies** reshape each rank without changing its total value. They multiply combat stats, balanced by what each stat is worth: a point of HP or ATK/MAT counts fully, DEF, MDF, and SPD count half (SPD sets turn order and shifts the Graze roll), and WIL counts a quarter. Stats a family never uses stay at 1.0, so they can't be dumped for free power.

| Family | HP | ATK | MAT | DEF | MDF | SPD | WIL | The feel |
|---|---|---|---|---|---|---|---|---|
| **Draugr** | 1.2 | 1.05 | 0.9 | 1.0 | 0.9 | **0.6** | 1.0 | Heavy, hard-hitting, slow: they act after you |
| **Bein** | 0.9 | 1.0 | — | **1.4** | 0.9 | 0.8 | 1.2 | Armored but brittle; statuses land poorly |
| **Drattr** | 1.1 | 0.9 | 1.1 | 0.8 | **1.2** | 1.0 | 0.9 | Slippery and soaked: soft to steel, hard to hurt with magic |
| **Djur** | 0.7 | **1.3** | — | 0.9 | 0.8 | **1.4** | 0.8 | Fast, hard-hitting, fragile, easily scared |
| **Ande** | 0.9 | — | 1.1 | 0.8 | **1.3** | 1.0 | 0.9 | Magic made flesh: shrug off spells, fold to steel |
| **Oskorei** | 1.0 | 1.0 | 1.0 | 1.0 | 0.9 | 1.1 | 1.0 | People like you, plus horses |

### Procedural vs. Fixed

- **Procedural families** (Ande, Draugr, Bein, Drattr, Djur) are packs filled to the budget with random ranks. Ande packs are themed to one or two elements.
- **Fixed formations** (the Oskorei) are authored encounters that escalate by tier.

---

## Part 2: Families at a Glance

| Family | Kind | Deals | Weak to | Resists | Hunted best by (level 30 win rate) |
|---|---|---|---|---|---|
| **Ande** | Elemental spirits | Their element | Their school's weaknesses | Their school | Dagskald 54%, Ullar 41%, Lundar 32% |
| **Draugr** | The saga dead | Slash, Crush | Slash, Eld, Sol | Crush, Natt, Aska | Brennumar 68%, Dagskald 65%, Huskarl 58% |
| **Bein** | Skeletons | Slash, Pierce | Crush, Sol | Slash, Pierce, Natt, Aska | Dagskald 73%, Brennumar 50%, Hafrunar 50% |
| **Drattr** | Hunted water creatures | Crush, Vatn, Hrim | Pierce, Jord, Reyk | Slash, Vatn, Hrim | Ullar 65%, Lundar 51%, Dagskald 44% |
| **Djur** | Forest beasts | Pierce, Slash | Pierce, Eld | Crush, Gro | Brennumar 67%, Nalarbani 55%, Ullar 54% |
| **Oskorei** | The Wild Hunt | Slash, Crush, Pierce, Blast, Blixt | Eld, Gro, plus each hunter's martial weakness | Blast, Blixt | Brennumar 68%, Ullar 61%, Nalarbani 59% |

**The martial triangle:** Slash hunts Draugr, Crush hunts Bein, and Pierce hunts Drattr (and Djur).

---

## Part 3: The Ande (Elemental Spirits)

A procedural family of elemental spirits: stat blobs that give the heroes something to swing at, and the sim a full test bestiary. **Ande** is Swedish *ande*, "spirit" (ON *andi*, "breath, spirit," from PIE \*h₂enh₁-, "to breathe," the root of Latin *animus*). In Swedish, *-ande* is also the "-ing" ending, so **Eldande** reads as "the burning one," **Blastande** as "the blowing one," and **Lakande** is literally "healing."

### Naming

**[Rank] + Element + ande**, using the usual seam rules: Liteleldande, Storeykande, Litelaskande. Gro keeps its vowel (**Groande**, not "Grande").

### Ranks

**Cost = slots = actions per round.** An encounter fills a **6-slot budget**. Every rank carries an All move one step up from where it started: Halv ranks get Allhalv, standard ranks get the base All. Everyone's first actions resolve before anyone's second.

| Rank | Meaning | Cost | HP | Moves |
|---|---|---|---|---|
| **Halv** | Wisp | 1 | ×1 | Halv single, Allhalv |
| **Litel** | The annoying little ones | 1 | ×1.2 | Base single, Allhalv |
| *(none)* | Standard spirit | 2 | ×2 | Base single, All (base), U1 |
| **Stor** | The heroes | 2 | ×2.5 | Mer single, All (base), U1, U2 |
| **Drott** | Sovereign (ON *dróttinn*, "lord"; Swedish *drottning*, "queen") | 3 | ×3.5 | Jatte single, Allmer, U1, U3 |

6-cost ultra bosses are in the pocket.

### Kits

**U1** is the sibling element (parents carry their child; children carry their parent). **U2** is a status or debuff. **U3** is the Drott's sovereign move. Statuses and stat moves use the rank's tier.

| Spirit | U1 | U2 | U3 (Drott only) |
|---|---|---|---|
| Eldande | Reyk | Eitr | Meraukseid (+2 MAT) |
| Reykande | Eld | Blinda | Mernedhitt (−2 ACC) |
| Vatnande | Hrim | Mogl (Disarmed) | Meraukstav (+2 MDF) |
| Hrimande | Vatn | Nedrask | Meraukskold (+2 DEF) |
| Blastande | Blixt | Nedhitt | Meraukvig (+2 EVA) |
| Blixtande | Blast | Ogn | Meraukrask (+2 SPD) |
| Jordande | Gro | Nedrask | Meraukskold (+2 DEF) |
| Groande | Jord | Eitr | Merlak |
| Solande | Lak | Blinda | Meraukstav (+2 MDF) |
| Lakande | Sol (its only damage) | Aukskold | Meraukstav (+2 MDF) |
| Nattande | Aska | Ogn | Jatteblinda |
| Askande | Natt | Nid | **Helvad** (the only spirit with death magic) |

**Example, the Eldande line:** Halveldande (Halveld, Allhalveld) · Liteleldande (Eld, Allhalveld) · Eldande (Eld, Alleld, Reyk) · Storeldande (Mereld, Alleld, Mereyk, Mereitr) · Drotteldande (Jatteld, Allmereld, Jattereyk, Meraukseid).

**Art:** the Halvande sprite exists (16×16, four frames: flicker, flicker, squash, stretch), recolored into all twelve elements (halvande_families.png). The standard Ande sprite also exists (16×32, seven frames: five sways, a squash, and a stretch), recolored into all twelve elements (ande_families.png and an animated preview). Litel, Stor, and Drott still need art.

---

## Part 4: The Undead

Two martial families that complement each other: **Slash fighters hunt draugr, Crush fighters hunt skeletons.** Their top rank is **Forn-**, from Old Norse *forn*, "ancient" (Swedish *fornnordisk*). **Urdraugr** is in the pocket as a 6-slot boss.

### Draugr

The saga dead. You end a draugr by **cutting off its head and burning the body**, and Glámr in *Grettis saga* cursed Grettir with a fear of the dark when he was killed.

- **Deals:** Slash and Crush (claws, grave-goods axes)
- **Weak to:** Slash (beheading), Eld (burning), Sol
- **Resists:** Crush (bloated and heavy), Natt, Aska

| Rank | Moves |
|---|---|
| Halvdraugr | Claw (Slash), Rake (Allhalv Slash) |
| Draugr | Grave Axe (Slash), Barrow Fist (Crush), Sweep (All Slash), Ogn |
| Stordraugr | Mer Grave Axe and Barrow Fist, Sweep (All Slash), Blot (Bleeding) |
| Forndraugr | Jatte Barrow Fist, Mer Sweep, Merogn, Jattenid |
| **Gandraugr** (caster) | Mernatt, Merhrim, Ogn, Nid. ON *gandr*, a magic staff or spirit; draugar were said to command weather and fog. |

### Bein

Skeletons in formation: volleys and shield walls. ON *bein*, Swedish *ben*, "bone."

- **Deals:** Slash and Pierce (old swords, spears, arrows)
- **Weak to:** Crush, Sol
- **Resists:** Slash and Pierce (nothing to cut; arrows pass through the ribs), Natt, Aska

| Rank | Moves |
|---|---|
| Halvbein | Bone Jab (Pierce), Allhalv Volley (Pierce) |
| Bein | Old Sword (Slash), Spear (Pierce), All Volley (Pierce) |
| Storbein | Mer Old Sword and Spear, All Volley, Aukskold |
| Fornbein | Jatte Old Sword, Mer All Volley, Barbed Arrow (Bleeding), Allaukskold |

Skralla ("rattling") and Tork ("desiccated") are held for individual skeleton types.

---

## Part 5: The Drattr (the Catch)

Hunted water creatures: **weak to the spear.** Old Norse *dráttr* means "a pull, a haul" (modern Icelandic *dráttur* is used for a catch of fish), and Swedish *fors* means rapids. Swedish *ljuster*, the fish spear used for torch-fishing at night, is the reason for the Pierce weakness.

- **Deals:** Crush (tail slams), Vatn for steady damage, a little Hrim
- **Weak to:** Pierce, Jord, Reyk
- **Resists:** Slash (slippery scales), Vatn, Hrim
- **Cleanses** with Vatn's ebb and flow, using a new grab-bag root, **Skolja** (Swedish *skölja*, "to rinse"), which washes away an ally's statuses and lowered stages.

| Rank | Cost | Moves |
|---|---|---|
| Halvdrattr | 1 | Tail Slap (Crush), Thrash (Allhalv Crush) |
| Drattr | 2 | Tail Slap (Crush), Vatn, Allvatn, Skolja |
| Stordrattr | 2 | Breach (Mer Crush), Mervatn, Allvatn, Hrim |
| Forsdrattr | 3 | Falls Crash (Jatte Crush), Jattevatn, Allmervatn, Allskolja |

**Reserved uniques:** **Näcken** (the fiddle-playing water spirit; Finnish *näkki*), **Bäckahästen** (the brook horse that drowns its riders), and **the Loki-salmon**, from the myth where Loki hid as a salmon in Fránangr's waterfall until the gods netted him and Thor caught him by the tail.

---

## Part 6: The Djur (the Beasts)

Forest animals, and the Wild Hunt's hounds. Swedish *djur*, "animal," from ON *dýr*, the same word as English "deer." Hunted with spear and arrow.

- **Deals:** Pierce and Slash (bites, tusks, antlers, claws)
- **Weak to:** Pierce, Eld
- **Resists:** Crush (thick hide and fur), Gro

| Rank | Cost | Moves |
|---|---|---|
| Halvdjur (*Jakthund*, "hunting hound," when with the Hunt) | 1 | Bite (Pierce), Pack Snap (Allhalv Pierce) |
| Djur | 2 | Bite (Pierce), Rend (Slash), Pack Rush (All Slash), Ogn (howl) |
| Stordjur | 2 | Gore (Mer Pierce), Rend (Mer Slash, Bleeding), Pack Rush (All Slash) |
| Forndjur | 3 | Gore (Jatte Pierce), Pack Rush (Mer, All), Merogn, Allaukraft (frenzy) |

---

## Part 7: The Oskorei (the Wild Hunt)

A human faction drawn from the Wild Hunt (*Odens jakt* in Sweden, *Oskoreia* in Norway; the name is variously explained as "Asgard's ride" or "the terrible ride"). Unlike the procedural families, the Oskorei come in **fixed formations** that escalate by tier.

- **Every hunter is Blast school** (resists Blast and Blixt, weak to Eld and Gro), plus the martial weakness of the class it mirrors.
- **The Hunt Horn:** while a horn-bearer lives, every enemy in the formation gets +1 ACC. That makes the horn-bearer the priority target.
- **The mirror puzzle:** Tier 1 fields one cycle of your own martial classes; Tier 3 fields the *reverse* cycle, so a lesson learned in Tier 1 has to be unlearned.

| Tier | Formation | Slots |
|---|---|---|
| 1. Halvoskorei | Mirror Huskarl (Axe: Slash, weak to Crush), Vasara (Hammer: Crush, weak to Pierce), and Ullar (Bow: Pierce, weak to Slash), each with Allhalvblast, plus three Jakthund | 6 |
| 2. Oskorei | **Ryttar** (Swedish *ryttare*, "rider": Ride Down, Spectral Blade, Trample (All Crush), Aukskold; weak to Pierce, like cavalry against spears) and **Hornblasar** (Swedish *hornblåsare*, "horn-blower," the same root as Blast: Blast, Blixt, Allblast, Bann; carries the horn), plus two Jakthund | 6 |
| 3. Storoskorei | Mirror Hersir (Greatsword: Slash, weak to Pierce), Nalarbani (Stiletto: Pierce, weak to Crush, with Blot), and Berserker (Maul: Crush, weak to Slash, with Merblixt and Nedskold) | 6 |
| 4. The leaders | **Huntmaster** (Jatte Slash, Rain of Spears, Merogn, **Urblast**; carries a horn) and **Storm-caller** (**Urblixt**, Allmerblast, Merbann, Allmeraukrask; carries a horn) | 6 |

**The leaders carry Ur gear,** which makes them the first place players meet Ur spells, and a natural source of Ur gear as loot. Enemy Ur spells cost 48 MP.

**Party win rate by tier** (level 30): Tier 1 84%, Tier 2 72%, Tier 3 33%, Tier 4 31%. Tier 3, the reverse mirror, is the wall.

---

## Part 8: Stat Blocks

Generated from the sim's data (`sim/catalog.py`), with family bodies applied.

Level 30. The average hero has 505 HP, 44 in every attribute, and deals about 39 per base hit. Damage columns are expected damage against that hero. "Hits to down" ignores affinities.

**Ande** (Eld shown; every element has the same numbers with its own moves)

| Unit | Actions | HP | Attack stat | DEF / MDF | SPD | Best single | Best All (3 heroes) | Threat per round | Neutral hero hits to down |
|---|---|---|---|---|---|---|---|---|---|
| Halveldande | 1 | 247 | 73 | 41 / 67 | 44 | 38 | 85 | 38 | 5.8 |
| Liteleldande | 1 | 296 | 44 | 41 / 67 | 44 | 38 | 42 | 38 | 7.0 |
| Eldande | 2 | 494 | 44 | 41 / 67 | 44 | 38 | 85 | 75 | 11.7 |
| Storeldande | 2 | 617 | 44 | 41 / 67 | 44 | 53 | 85 | 105 | 14.6 |
| Drotteldande | 3 | 864 | 44 | 41 / 67 | 44 | 72 | 119 | 215 | 20.5 |

**Draugr**

| Unit | Actions | HP | Attack stat | DEF / MDF | SPD | Best single | Best All (3 heroes) | Threat per round | Neutral hero hits to down |
|---|---|---|---|---|---|---|---|---|---|
| Halvdraugr | 1 | 329 | 54 | 51 / 46 | 44 | 21 | 48 | 21 | 8.8 |
| Draugr | 2 | 658 | 27 | 51 / 46 | 44 | 21 | 48 | 43 | 17.6 |
| Stordraugr | 2 | 823 | 27 | 51 / 46 | 44 | 30 | 48 | 60 | 22.0 |
| Forndraugr | 3 | 1152 | 27 | 51 / 46 | 44 | 41 | 68 | 122 | 30.8 |
| Gandraugr | 2 | 658 | 27 | 51 / 46 | 44 | 26 | 0 | 52 | 17.6 |

**Bein**

| Unit | Actions | HP | Attack stat | DEF / MDF | SPD | Best single | Best All (3 heroes) | Threat per round | Neutral hero hits to down |
|---|---|---|---|---|---|---|---|---|---|
| Halvbein | 1 | 247 | 51 | 72 / 46 | 44 | 22 | 49 | 22 | 10.2 |
| Bein | 2 | 494 | 26 | 72 / 46 | 44 | 22 | 49 | 43 | 20.5 |
| Storbein | 2 | 617 | 26 | 72 / 46 | 44 | 30 | 49 | 61 | 25.6 |
| Fornbein | 3 | 864 | 26 | 72 / 46 | 44 | 41 | 68 | 123 | 35.8 |

**Drattr**

| Unit | Actions | HP | Attack stat | DEF / MDF | SPD | Best single | Best All (3 heroes) | Threat per round | Neutral hero hits to down |
|---|---|---|---|---|---|---|---|---|---|
| Halvdrattr | 1 | 302 | 57 | 41 / 62 | 44 | 21 | 46 | 21 | 7.1 |
| Drattr | 2 | 603 | 28 | 41 / 62 | 44 | 25 | 57 | 50 | 14.3 |
| Stordrattr | 2 | 754 | 28 | 41 / 62 | 44 | 35 | 57 | 70 | 17.9 |
| Forsdrattr | 3 | 1056 | 28 | 41 / 62 | 44 | 48 | 79 | 143 | 25.0 |

**Djur**

| Unit | Actions | HP | Attack stat | DEF / MDF | SPD | Best single | Best All (3 heroes) | Threat per round | Neutral hero hits to down |
|---|---|---|---|---|---|---|---|---|---|
| Halvdjur | 1 | 192 | 67 | 46 / 41 | 44 | 31 | 71 | 31 | 5.4 |
| Djur | 2 | 384 | 33 | 46 / 41 | 44 | 31 | 71 | 63 | 10.8 |
| Stordjur | 2 | 480 | 33 | 46 / 41 | 44 | 44 | 71 | 88 | 13.5 |
| Forndjur | 3 | 672 | 33 | 46 / 41 | 44 | 60 | 99 | 179 | 18.9 |

**Oskorei**

| Unit | Actions | HP | Attack stat | DEF / MDF | SPD | Best single | Best All (3 heroes) | Threat per round | Neutral hero hits to down |
|---|---|---|---|---|---|---|---|---|---|
| T1 Halvoskorei Axe | 1 | 274 | 51 | 51 / 46 | 44 | 23 | 46 | 23 | 8.1 |
| T1 Halvoskorei Hammer | 1 | 274 | 51 | 51 / 46 | 44 | 23 | 46 | 23 | 8.1 |
| T1 Halvoskorei Bow | 1 | 274 | 51 | 51 / 46 | 44 | 23 | 46 | 23 | 8.1 |
| T1 Jakthund | 1 | 192 | 67 | 46 / 41 | 44 | 31 | 71 | 31 | 5.4 |
| T2 Ryttar | 2 | 548 | 26 | 51 / 46 | 44 | 23 | 51 | 46 | 16.2 |
| T2 Hornblasar | 2 | 548 | 26 | 51 / 46 | 44 | 29 | 46 | 57 | 16.2 |
| T2 Jakthund | 1 | 192 | 67 | 46 / 41 | 44 | 31 | 71 | 31 | 5.4 |
| T3 Storoskorei Greatsword | 2 | 685 | 26 | 51 / 46 | 44 | 32 | 51 | 64 | 20.3 |
| T3 Storoskorei Stiletto | 2 | 685 | 26 | 51 / 46 | 44 | 32 | 0 | 64 | 20.3 |
| T3 Storoskorei Maul | 2 | 685 | 26 | 51 / 46 | 44 | 40 | 0 | 80 | 20.3 |
| T4 Huntmaster | 3 | 960 | 26 | 51 / 46 | 44 | 51 | 72 | 154 | 28.4 |
| T4 Storm-caller | 3 | 960 | 26 | 51 / 46 | 44 | 72 | 65 | 215 | 28.4 |

---

## Part 9: Sim Results

Win rate when each class is in the party, at level 30 (1,500 fights per family), with family bodies and the speed shift applied. Weak hits per fight in parentheses.

| Class | Ande | Draugr | Bein | Drattr | Djur | Oskorei |
|---|---|---|---|---|---|---|
| Brennumar | 24% (0.6) | 68% (5.3) | 50% (0.0) | 26% (0.6) | 67% (3.5) | 68% (4.4) |
| Dagskald | 54% (1.0) | 65% (3.6) | 73% (3.3) | 44% (0.0) | 38% (0.0) | 57% (0.0) |
| Hafrunar | 28% (1.0) | 44% (0.0) | 50% (0.0) | 22% (0.0) | 43% (0.0) | 53% (0.0) |
| Lundar | 32% (0.7) | 46% (0.0) | 49% (0.0) | 51% (6.6) | 39% (0.0) | 53% (1.1) |
| Seidar | 17% (0.9) | 36% (0.0) | 29% (0.0) | 22% (0.0) | 29% (0.0) | 41% (0.0) |
| Skurmar | 29% (1.2) | 43% (0.0) | 48% (0.0) | 32% (0.0) | 38% (0.0) | 42% (0.0) |
| Berserker | 29% (0.0) | 27% (0.0) | 42% (1.9) | 30% (0.0) | 20% (0.0) | 41% (0.7) |
| Hersir | 32% (0.0) | 53% (3.8) | 34% (0.0) | 23% (0.0) | 28% (0.0) | 38% (1.8) |
| Huskarl | 31% (0.0) | 58% (3.4) | 27% (0.0) | 21% (0.0) | 39% (0.0) | 48% (2.2) |
| Nalarbani | 31% (0.0) | 34% (0.0) | 41% (0.0) | 37% (2.5) | 55% (2.9) | 59% (2.3) |
| Ullar | 41% (0.0) | 36% (0.0) | 30% (0.0) | 65% (5.4) | 54% (3.3) | 61% (2.4) |
| Vasara | 32% (0.0) | 33% (0.0) | 48% (3.9) | 34% (0.0) | 32% (0.0) | 44% (0.8) |

Overall party win rates at level 30: Ande 33%, Draugr 46%, Bein 45%, Drattr 36%, Djur 41%, Oskorei 51%. Oskorei by tier: T1 85%   T2 71%   T3 25%   T4 27%. Absolute difficulty is a knob; the comparisons are what count.

---|---|---|---|---|---|---|
| Brennumar | 30% (0.9) | 66% (5.2) | 48% (0.0) | 31% (0.6) | 65% (3.6) | 72% (4.7) |
| Dagskald | 57% (0.9) | 65% (3.4) | 69% (3.0) | 45% (0.0) | 39% (0.0) | 66% (0.0) |
| Hafrunar | 31% (1.3) | 36% (0.0) | 50% (0.0) | 28% (0.0) | 36% (0.0) | 57% (0.0) |
| Lundar | 32% (0.9) | 34% (0.0) | 48% (0.0) | 48% (6.6) | 38% (0.0) | 59% (1.1) |
| Seidar | 18% (0.6) | 25% (0.0) | 29% (0.0) | 22% (0.0) | 26% (0.0) | 43% (0.0) |
| Skurmar | 28% (1.1) | 40% (0.0) | 44% (0.0) | 29% (0.0) | 36% (0.0) | 47% (0.0) |
| Berserker | 29% (0.0) | 26% (0.0) | 44% (1.9) | 34% (0.0) | 19% (0.0) | 45% (0.7) |
| Hersir | 29% (0.0) | 49% (3.6) | 32% (0.0) | 23% (0.0) | 31% (0.0) | 45% (1.9) |
| Huskarl | 33% (0.0) | 56% (3.4) | 28% (0.0) | 21% (0.0) | 36% (0.0) | 56% (2.0) |
| Nalarbani | 28% (0.0) | 28% (0.0) | 36% (0.0) | 35% (2.5) | 54% (3.1) | 64% (2.4) |
| Ullar | 41% (0.0) | 34% (0.0) | 30% (0.0) | 68% (5.1) | 53% (3.5) | 68% (2.5) |
| Vasara | 34% (0.0) | 31% (0.0) | 46% (4.0) | 36% (0.0) | 29% (0.0) | 45% (0.9) |

Overall party win rates at level 30: Ande 34%, Draugr 41%, Bein 44%, Drattr 36%, Djur 39%, Oskorei 57%. Oskorei by tier: T1 86%   T2 71%   T3 35%   T4 34%. Absolute difficulty is a knob; the comparisons are what count.

---|---|---|---|---|---|---|
| Brennumar | 45% (0.7) | **63%** (5.2) | 31% (0) | 38% (0.9) | **55%** (5.4) | **66%** (5.2) |
| Dagskald | **69%** (0.7) | **60%** (3.4) | **48%** (3.3) | 52% (0) | 39% (0) | 62% (0) |
| Hafrunar | 38% (1.3) | 40% (0) | 33% (0) | 27% (0) | 33% (0) | 50% (0) |
| Lundar | 44% (0.8) | 36% (0) | 28% (0) | **65%** (5.8) | 30% (0) | 51% (1.0) |
| Seidar | 23% (0.6) | 25% (0) | 16% (0) | 25% (0) | 20% (0) | 45% (0) |
| Skurmar | 38% (1.3) | 40% (0) | 25% (0) | 38% (0) | 31% (0) | 49% (0) |
| Berserker | 32% (0) | 30% (0) | 29% (1.9) | 29% (0) | 18% (0) | 47% (0.7) |
| Hersir | 26% (0) | 50% (3.5) | 19% (0) | 32% (0) | 20% (0) | 42% (1.9) |
| Huskarl | 34% (0) | **59%** (3.2) | 18% (0) | 27% (0) | 30% (0) | 57% (2.1) |
| Nalarbani | 33% (0) | 37% (0) | 21% (0) | 38% (2.1) | 44% (4.0) | 60% (2.6) |
| Ullar | 42% (0) | 32% (0) | 21% (0) | **66%** (5.8) | **50%** (5.0) | **72%** (3.5) |
| Vasara | 37% (0) | 34% (0) | **43%** (3.9) | 40% (0) | 21% (0) | 51% (0.9) |

Overall party win rates at level 30: Ande 41%, Draugr 43%, Bein 29%, Drattr 41%, Djur 33%, Oskorei 55%. Absolute difficulty is a knob; the comparisons are what count.

---

## Reserved and Pocketed

- **Uniques:** Näcken, Bäckahästen, and the Loki-salmon (Drattr); the Huntmaster and Storm-caller already exist as Oskorei leaders.
- **6-slot ultra bosses:** Urdraugr, and Ur-rank versions of other families.
- **Skeleton types:** Skralla ("rattling") and Tork ("desiccated").
- **Bespoke spirits:** to be added on top of the procedural Ande.
- **Future families:** whatever completes new matchups (for example, a family weak to Natt or Aska beyond the Sol-school Ande).

---

## Open Questions

- **Overall difficulty:** Halv bodies made random packs harder (29–43% at level 30). One difficulty setting can ease everything without changing the shapes.
- **Stat values:** the value weights behind the bodies (HP and attack 1, DEF, MDF, and SPD 0.5, WIL 0.25) are estimates.
- **Oskorei Tier 3:** the reverse mirror is a wall (33%); consider less HP or 2-cost Djur in Tier 2 to smooth the climb.
- **The Bein:** resisting both Slash and Pierce may be one resistance too many.
- **Undead fight length:** about 5 rounds, shorter than spirit fights.
- **Cleanse (Skolja):** rarely cast, because the party inflicts few statuses; revisit once status-heavy classes exist.
- **Art:** Litel, standard, Stor, and Drott spirit sprites; everything for the other families.
