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
| **Litel-** (Ande and Mogel) | 1 | ×1.2 | Base single, Allhalv |
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
| **Mogel** | 0.95 | 1.0 | 1.0 | 1.0 | 1.0 | 0.8 | 1.0 | Soft and slow, but they come back smaller (the chain is priced into the body) |

### Procedural vs. Fixed

- **Procedural families** (Ande, Mogel, Draugr, Bein, Drattr, Djur) are packs filled to the budget. Ande and Mogel packs are rolled by the **encounter composer** (Part 9), usually themed to a biome's elements.
- **Fixed formations** (the Oskorei) are authored encounters that escalate by tier.

---

## Part 2: Families at a Glance

| Family | Kind | Deals | Weak to | Resists | Hunted best by (level 30 win rate) |
|---|---|---|---|---|---|
| **Ande** | Elemental spirits | Their element | Their school's weaknesses | Their school | Dagskald 51%, Ullar 33%, Skurmar 29% |
| **Draugr** | The saga dead | Slash, Crush | Slash, Eld, Sol | Crush, Natt, Aska | Brennumar 73%, Dagskald 57%, Hersir 47% |
| **Bein** | Skeletons | Slash, Pierce | Crush, Sol | Slash, Pierce, Natt, Aska | Dagskald 70%, Vasara 63%, Hafrunar 54% |
| **Drattr** | Hunted water creatures | Crush, Vatn, Hrim | Pierce, Jord, Reyk | Slash, Vatn, Hrim | Ullar 55%, Lundar 53%, Dagskald 48% |
| **Djur** | Forest beasts | Pierce, Slash | Pierce, Eld | Crush, Gro | Brennumar 73%, Nalarbani 56%, Ullar 51% |
| **Mogel** | Living mould (slimes) | Crush, their element | Slash, their school's weaknesses | Pierce; absorb their own element | Hersir 41%, Dagskald 39%, Huskarl 35% |
| **Oskorei** | The Wild Hunt | Slash, Crush, Pierce, Blast, Blixt | Eld, Gro, plus each hunter's martial weakness | Blast, Blixt | Brennumar 60%, Ullar 55%, Dagskald 54% |

**The martial triangle:** Slash hunts Draugr (and cuts the Mogel), Crush hunts Bein, and Pierce hunts Drattr (and Djur).

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

**The crawl (Locked; numbers tune).** A Draugr killed by anything but Slash or Eld doesn't stay down: it falls and **crawls on** at 35% HP, in its cell, with only its Claw. Behead it (Slash) or burn it (Eld) and it stays dead; the crawl happens once. The sheet's crawl frames are this form.

**Art:** the Gandalf Hardcore zombie in Res64 (art_res64/undead/draugr): corpse-pale Halvdraugr (cut, 32px), death-blue Draugr (38) and Stordraugr (stretched, 44), and the Forndraugr in blood-red rags (44). The Gandraugr casts on a held frame until it has its own pose.

### Bein (the Beinar)

Skeletons by job, like a weak Oskorei: each one patches another family's weakness. ON *bein*, Swedish *ben*, "bone"; *Beinar*, the bone-folk.

- **Deals:** Slash, Crush, and Pierce (old swords, shield bashes, arrows); the Beinseidr cast
- **Weak to:** Crush, Sol
- **Resists:** Slash and Pierce (nothing to cut; arrows pass through the ribs), Natt, Aska

| Job | Ranks | Moves | Patches |
|---|---|---|---|
| **Beinbryn** (ON *brynja*, "mail-coat"): sword and shield | Halvbeinbryn, Beinbryn, Storbeinbryn | Rusty Blade / Old Sword (Slash), Shield Bash (Crush), Aukskold | A shield-bearer: **Covers** allies under half HP, twice as keenly as anyone else. Stands in front of a Mogel and takes the Slash meant for it. |
| **Beinorv** (ON *ǫrvar*, "arrows"): bow | Halvbeinorv, Beinorv, Storbeinorv | Arrow (Pierce, reaches anywhere), Volley (row), Barbed Arrow (Bleeding) | Reach: gives the melee-only Draugr a way into our Rear. Stands in the Rear. |
| **Beinseidr**: staff and orb | Halv-, base, Stor- (Halvnattbeinseidr, Askabeinseidr...) | A spell of its element, Nid, Allaukstav (MDF up for all) at Stor | Magic. Adopts an element (Natt, Aska, Eld, Hrim, Blixt; never Sol); its orb, eyes and chest rune take that element's ramp. |
| **Fornbein**: the Drott, the red shield-king | Fornbein | Jatte Old Sword, Mer Shield Bash, Allaukskold, Ogn | |

**The pile (Locked; numbers tune).** A Bein killed by anything but Crush **falls into a pile of bones** and stands up again 2 rounds later at 50% HP, in its cell (or the nearest free one). A Crush blow on the pile scatters it for good, and a Crush kill never leaves one. Melee reaches a pile only in the Front, or in the Rear once the Front is empty; it happens once. **If only piles are left, the fight is over** (Joseph, Nov 8: the bones can't gather themselves fast enough; you loot and walk away). The pile bites only mid-fight, so the lesson is "kill the bones last, or bring Crush." *(Open idea, later: piles left uncrushed in a dive's first leg could rise and wander into a room on the way out.)*
- **Sim:** about one pile a fight; the party AI scatters few of them (it seldom has a Crush move in reach), so most stand again. Piles in the Rear stand again almost always, because melee can't reach them: the Beinorv and Beinseidr get a second life. (Open: should Jord, stone, also crush bones, so casters have an answer?)

**The Barrow rules together** (crawl, piles, guardian Cover; 800 fights, the board on, knob 0.6): party wins drop from 34% to 24% at level 10 and from 50% to 38% at level 30. That lands near the Barrow's no-board targets (27%, 42%); the Barrow is a little harder than the other habitats, which suits a slice's first place.

**Art:** Joseph's four starters (sword and shield, mage, short bow, longbow) in Res64 (art_res64/undead/beinar): plain bone Halv (cut, 32px), cool aged bone base (38) and Stor (stretched, 44), blood-red Drott (44). Idle frames only so far.

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

## Part 8: The Mogel (Living Mould)

The physical half of a spirit pack. The Ande are casters who keep to the Rear; the Mogel are slimes that hold the Front, engulf with Crush, and carry one element in their bodies. **Mogel** is Swedish *mögel*, "mould" (written without the ö, by the spelling rules). Every Swede will read it as mould, which is exactly the joke: the dungeon's damp, given an appetite.

### Naming

**[Rank] + Element + mogel**, using the usual seam rules: Halveldmogel, Litelvatnmogel, Storaskamogel, Hrimogel (the m's merge), Litelakmogel (the l's merge). **The olive slime is the Jord one,** because mould is earth, and since Nov 21 it says so like every other: Halvjordmogel, Liteljordmogel, Jordmogel, Storjordmogel, Drottjordmogel (Stormogel read as storm). Bare **Mogel** is the family's name.

### Affinities

| | |
|---|---|
| **Weak to** | **Slash** (it cuts them), plus their school's weaknesses (an Eldmogel is weak to Vatn and Blixt) |
| **Neutral** | Crush |
| **Resists** | **Pierce** (it passes straight through) |
| **Absorbs** | **Their own element** (an Eldmogel drinks Eld) |

### The Chain (the folklore rule)

**Killing a Mogel drops it one size; only the smallest one truly dies.**

- **Any 32px Mogel** (Mogel, Stor, Drott) bursts and **re-forms as a Litelmogel** (24px) of the same element, in the same cell.
- **A Litelmogel** re-forms as a **Halvmogel** (16px).
- **A Halvmogel** dies, popping into an 8px droplet that vanishes.
- **Each re-formed body has 35% of its normal HP** and acts as its new rank (one action a round). If it shrank mid-round, it loses any actions it had queued.
- **One rank's cost pays for its whole chain.** A 2-cost Mogel is about 520 HP at level 30, then roughly 110 more as a Litel and 90 as a Halv. The body's lower HP and SPD (above) pay for the extra lives.
- **No splitting:** the smaller slime stays in the cell it died in, so the board never gains units and only one target ever needs re-picking. Each death plays into the next size's **surprise** pose: 32 to 24, 24 to 16, and 16 to the 8px droplet.

### Ranks and Kits

Enemy strikes are free; spells cost MP. **Engulf** is single-target Crush, **Splatter** is All Crush, **Withdraw** is Defend, and **Reabsorb** is the Drott's self-heal (Merlak on itself). Lakmogel heal with Lak instead of attacking with it.

**Slime paint (Mogel, Stor, Drott; Draft numbers):** the Mogel charges (the breathe-in is the tell) and shoots slime that coats one of our spots: **Mark + its element** at its spell tier (Markeld, Markmervatn, Markjattenatt), shouted as "Fire Slime!", "Water Slime!". It reaches anywhere, so it is also the Mogel's way into our Rear.
- **When it lands,** whoever stands on the spot takes ×0.5 of the move's damage.
- **At the start of each of the next 3 rounds,** whoever stands there takes ×0.5 again. Affinity is ignored for now (element damage only), and Cover can't take it: it hits a place, not a body.
- **The answer is to step off** (a Move within the row, +1). One coat per spot at a time; a fresh coat resets the 3 rounds. Lakmogel don't paint.
- **Sim:** about 1 coat and 2 ticks a fight against drawn Mogel packs; it costs the party 1–3 points of win rate.

| Rank | Art | Cost | HP | Engulf | Element spell | Splatter | Extra |
|---|---|---|---|---|---|---|---|
| **Halv** | 16px | 1 | ×1 | Halv | Halv (free) | — | Halv body (×2 STR/INT) |
| **Litel** | 24px | 1 | ×1.2 | Base | Halv (free) | — | — |
| *(none)* | 32px | 2 | ×2 | Base | Base | Halv | Withdraw |
| **Stor** | 32px + an item inside (a skull) | 2 | ×2.5 | Mer | Mer | Base | Withdraw |
| **Drott** | 32px + an item inside (a swallowed crown) | 3 | ×3.5 | Jatte | Jatte | Mer | Reabsorb |

**Example, the Eld line:** Halveldmogel (Engulf, Halveld) · Liteleldmogel (Engulf, Halveld) · Eldmogel (Engulf, Splatter, Eld, Withdraw) · Storeldmogel (Mer Engulf, Splatter, Mereld, Withdraw) · Drotteldmogel (Jatte Engulf, Mer Splatter, Jatteld, Reabsorb).

### Numbers (level 30, Eldmogel line)

| Rank | Cost | HP | Re-forms with | ATK | DEF / MDF | SPD |
|---|---|---|---|---|---|---|
| Halveldmogel | 1 | 260 | (dies) | 51 | 51 / 51 | 35 |
| Liteleldmogel | 1 | 313 | 91 as a Halv | 26 | 51 / 51 | 35 |
| Eldmogel | 2 | 521 | 110 as a Litel | 26 | 51 / 51 | 35 |
| Storeldmogel | 2 | 651 | 110 as a Litel | 26 | 51 / 51 | 35 |
| Drotteldmogel | 3 | 912 | 110 as a Litel | 26 | 51 / 51 | 35 |

### Art

Joseph's slime, converted to Resurrect 64 at **32, 24, 16, and 8 pixels** (Mogel, Litel, Halv, and the death droplet), eleven frames each (idle ×2, surprise, breathe-in ×2, hit ×2, withdraw, cast ×3), in all twelve element ramps (`art_res64/slimes/`). Animations: idle, hit, defend (withdraw), **charge** (the breathe-in stretch, the telegraph for a big move), cast, and surprise (the re-form pop). Stor and Drott reuse the 32px body with an item drawn inside it; those overlays aren't drawn yet.

---

## Part 9: The Encounter Composer

Procedural packs are rolled by one small machine (`sim/composer.py`) that fills a slot budget from a tagged catalog. It's Joseph's d3 idea, generalised.

**The catalog** lists every unit with tags: family, rank, element, school, cost, role (Front or Rear), whether its art exists, a weight, and **ranged** (it has a damage move that reaches our Rear from anywhere: a spell, a bow, a throw). It holds the Ande and the Mogel in every element, and the Draugr, Bein, Drattr, and Djur by rank: 137 entries.

**How a pack is rolled:**

1. **Gates narrow the catalog:** any tag, such as family, element, school, rank, or **art only** (just the units we can draw). A **biome is a named gate:** Eldhall is Eld and Reyk; the Mire is Jord, Gro, and Vatn. A freeform roll picks a biome first.
2. **Roll a cost.** The faces are 1, 2, and 3, minus any that can't work: the cost is more than the budget left, nothing that costs that much survives the gates, a rule forbids it, or it would leave a remainder that can't be filled exactly. Then roll among the faces left.
3. **Pick a unit of that cost** from the gated catalog, weighted.
4. **Repeat until the budget is spent.**

**Rolling the cost first, then the unit,** keeps big units appearing even when the gates leave many small ones; picking units directly would drown the 3-costs.

**Habitats** are where the folklore families live. A habitat gate keeps its home families at every rank, plus Ande and Mogel of its elements as guests (each guest entry weighs 0.1 against a home entry's 1.0). Mogel fit everywhere, one flavour per place.

| Habitat | Home families | Guest elements (Ande, Mogel) |
|---|---|---|
| **Barrow** | Draugr, Bein | Natt, Aska |
| **Wildwood** | Djur | Gro, Jord |
| **Rapids** | Drattr | Vatn, Hrim |

**Rules are toggles:** the budget (6 by default; 3 for a small fight), a unit cap (never more than the 6 cells), banned costs ("no 1-costs"), per-cost caps ("only one 3-cost"), family minimums and maximums ("at least one Mogel and one Ande"), per-family weights, and **ranged**: `include` re-rolls until the pack has at least one unit that reaches our Rear, `exclude` gates them all out (the pure-melee pack), unset takes whatever rolls. The fit check means a rule set that can't be satisfied is caught before a pack is half-built (for example, no 1-costs with 5 slots left and no 3-cost allowed).

**The mirror (Nov 23, agreed; not built):** most packs reserve one reach slot per three units (rounded up), within the budget, seated in the Rear; Regular rooms and up always (but a rare brute room), Trash half the time. Ande and Mogel are the glue families: they lend reach to the Drattr, Draugr and Djur. Full rule: beinar_pilot.md Part 2, section 8. Parked families and reach-as-culture (the woodfolk, the Wyrms' spit, the Drattr blowgun): beinar_pilot.md Part 5.

**Placement:** biggest units choose first. Front-liners (Mogel) fill the Front row, casters (Ande) the Rear; overflow spills into the other row, and the Front is never left empty while the Rear holds someone.

**Sample rolls** (art only):

| Gate | Front | Rear |
|---|---|---|
| Eldhall | Eldmogel, Halvreykmogel, Halveldmogel | Halveldande, Halvreykmogel |
| Mire, all ranks, one 3-cost | Drottmogel, Mogel, Litelmogel | — |
| At least one of each family | Blastmogel, Lakmogel | Reykande |
| Small fight (budget 3) | Vatnmogel | Halvblixtande |

### Composer Sim Results

3 random recruits against composed packs, each pack gated to a rolled biome (1,500 fights per row at levels 10, 30 and 60; 1,200 per row for the drawn-only table).

**All ranks:**

| Pack | Level 10 | Level 30 | Level 60 | Median length (level 30) |
|---|---|---|---|---|
| Mogel only | 16% | 28% | 45% | 8 rounds |
| Ande only | 37% | 29% | 42% | 7 rounds |
| Mixed (at least one of each) | 20% | 29% | 42% | 7 rounds |

**Drawn units only** (Halv, Litel and base Mogel; Halv and base Ande), the likely vertical slice:

| Pack | Level 5 | Level 10 | Level 20 | Level 30 | Median length (level 10) |
|---|---|---|---|---|---|
| Mogel | 24% | 35% | 49% | 59% | 12 rounds |
| Ande | 25% | 35% | 48% | 52% | 8 rounds |
| Mixed | 20% | 34% | 48% | 56% | 9 rounds |

- **The two families are matched** at every level once the gates are the same.
- **The chain makes Mogel fights longer:** about 3 re-forms a fight, and 12 rounds at level 10 against 8 for the Ande. Two knobs if that drags in play: a smaller re-form share, or a chain that stops at the Litel (only the 32px ones shrink).
- **Mogel at level 10 with all ranks is too hard (16%),** because Stor and Drott ranks hit with Mer and Jatte moves before the party has them. The fix is a gate, not a nerf: early floors roll drawn ranks only.
- **The triangle shows up:** against Mogel-only packs, Hersir (Slash) wins 41% and Nalarbani (Pierce) 14%.
- **The composer runs harder than the old Ande picker** (29% against 33–41% at level 30), because rolling cost first brings more 3-costs. Difficulty is the budget and the face weights.

**Habitats and the ranged rule** (`sim/habitat_check.py`, 800 fights per cell, party wins):

| Habitat, ranged | L10 no board | L10 board | L10 board, knob 0.6 | L30 no board | L30 board | L30 board, knob 0.6 |
|---|---|---|---|---|---|---|
| Barrow, unset | 27% | 39% | 26% | 42% | 54% | 45% |
| Barrow, include | 27% | 38% | 27% | 41% | 52% | 44% |
| Barrow, exclude | 22% | 41% | 29% | 37% | 54% | 46% |
| Wildwood, unset | 21% | 36% | 28% | 38% | 50% | 38% |
| Wildwood, include | 25% | 34% | 25% | 38% | 50% | 38% |
| Wildwood, exclude | 21% | 39% | 29% | 34% | 52% | 38% |
| Rapids, unset | 18% | 32% | 24% | 29% | 40% | 30% |
| Rapids, include | 15% | 32% | 20% | 29% | 42% | 32% |
| Rapids, exclude | 52% | 77% | 72% | 70% | 91% | 87% |

- **One reach unit doesn't give back what the board takes.** Include and exclude differ by only 2–3 points on the board, because one ranged unit is a small share of a pack's damage; the rest still can't touch our casters. Protection is about the *share* of a pack that reaches the Rear, not whether any of it does.
- **So the damage knob stays at 0.6**, which puts every habitat back near its no-board rate. The ranged rule stays as a design toggle: who patches whose weakness, and the pure-melee easy pack.
- **Rapids with no ranged unit is six Halvdrattr** (the only Drattr rank without spells): a very easy pack. Exclude there needs a budget or rank rule if it's ever used.

---

## Part 10: Stat Blocks

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
| Halvdraugr | 1 | 329 | 65 | 51 / 46 | 44 | 26 | 58 | 26 | 8.8 |
| Draugr | 2 | 658 | 32 | 51 / 46 | 44 | 26 | 58 | 52 | 17.6 |
| Stordraugr | 2 | 823 | 32 | 51 / 46 | 44 | 36 | 58 | 72 | 22.0 |
| Forndraugr | 3 | 1152 | 32 | 51 / 46 | 44 | 49 | 81 | 147 | 30.8 |
| Gandraugr | 2 | 658 | 32 | 51 / 46 | 44 | 36 | 0 | 72 | 17.6 |

**Bein**

| Unit | Actions | HP | Attack stat | DEF / MDF | SPD | Best single | Best All (3 heroes) | Threat per round | Neutral hero hits to down |
|---|---|---|---|---|---|---|---|---|---|
| Halvbeinbryn | 1 | 247 | 62 | 72 / 46 | 44 | 26 | 0 | 26 | 10.2 |
| Beinbryn | 2 | 494 | 31 | 72 / 46 | 44 | 26 | 0 | 52 | 20.5 |
| Storbeinbryn | 2 | 617 | 31 | 72 / 46 | 44 | 36 | 0 | 73 | 25.6 |
| Halvbeinorv | 1 | 247 | 62 | 72 / 46 | 44 | 26 | 0 | 26 | 10.2 |
| Beinorv | 2 | 494 | 31 | 72 / 46 | 44 | 26 | 29 | 52 | 20.5 |
| Storbeinorv | 2 | 617 | 31 | 72 / 46 | 44 | 36 | 58 | 73 | 25.6 |
| Halvnattbeinseidr | 1 | 247 | 62 | 72 / 46 | 44 | 26 | 0 | 26 | 10.2 |
| Nattbeinseidr | 2 | 494 | 31 | 72 / 46 | 44 | 26 | 0 | 52 | 20.5 |
| Stornattbeinseidr | 2 | 617 | 31 | 72 / 46 | 44 | 36 | 0 | 73 | 25.6 |
| Fornbein | 3 | 864 | 31 | 72 / 46 | 44 | 49 | 0 | 148 | 35.8 |

**Drattr**

| Unit | Actions | HP | Attack stat | DEF / MDF | SPD | Best single | Best All (3 heroes) | Threat per round | Neutral hero hits to down |
|---|---|---|---|---|---|---|---|---|---|
| Halvdrattr | 1 | 302 | 68 | 41 / 62 | 44 | 30 | 0 | 30 | 7.1 |
| Drattr (Young) | 2 | 603 | 34 | 41 / 62 | 44 | 30 | 0 | 60 | 14.3 |
| Drattr (Shield) | 2 | 603 | 34 | 41 / 62 | 44 | 30 | 0 | 60 | 14.3 |
| Drattr (Swords) | 2 | 603 | 34 | 41 / 62 | 44 | 30 | 0 | 60 | 14.3 |
| Drattr (Spear) | 2 | 603 | 34 | 41 / 62 | 44 | 30 | 0 | 60 | 14.3 |
| Drattr (Net) | 2 | 603 | 34 | 41 / 62 | 44 | 30 | 0 | 60 | 14.3 |
| Stordrattr (Angler) | 2 | 754 | 34 | 41 / 62 | 44 | 42 | 0 | 85 | 17.9 |
| Stordrattr (Princeling) | 2 | 754 | 34 | 41 / 62 | 44 | 25 | 0 | 49 | 17.9 |
| Stordrattr (Mystic) | 2 | 754 | 34 | 41 / 62 | 44 | 42 | 0 | 85 | 17.9 |
| Forsdrattr (Queen) | 3 | 1056 | 34 | 41 / 62 | 44 | 57 | 95 | 172 | 25.0 |

**Djur**

| Unit | Actions | HP | Attack stat | DEF / MDF | SPD | Best single | Best All (3 heroes) | Threat per round | Neutral hero hits to down |
|---|---|---|---|---|---|---|---|---|---|
| Halvdjur | 1 | 192 | 80 | 46 / 41 | 44 | 38 | 85 | 38 | 5.4 |
| Djur | 2 | 384 | 40 | 46 / 41 | 44 | 38 | 85 | 75 | 10.8 |
| Stordjur | 2 | 480 | 40 | 46 / 41 | 44 | 53 | 85 | 105 | 13.5 |
| Forndjur | 3 | 672 | 40 | 46 / 41 | 44 | 71 | 118 | 214 | 18.9 |

**Oskorei**

| Unit | Actions | HP | Attack stat | DEF / MDF | SPD | Best single | Best All (3 heroes) | Threat per round | Neutral hero hits to down |
|---|---|---|---|---|---|---|---|---|---|
| T1 Halvoskorei Axe | 1 | 274 | 62 | 51 / 46 | 44 | 27 | 56 | 27 | 8.1 |
| T1 Halvoskorei Hammer | 1 | 274 | 62 | 51 / 46 | 44 | 27 | 56 | 27 | 8.1 |
| T1 Halvoskorei Bow | 1 | 274 | 62 | 51 / 46 | 44 | 27 | 56 | 27 | 8.1 |
| T1 Jakthund | 1 | 192 | 80 | 46 / 41 | 44 | 38 | 85 | 38 | 5.4 |
| T2 Ryttar | 2 | 548 | 31 | 51 / 46 | 44 | 27 | 62 | 55 | 16.2 |
| T2 Hornblasar | 2 | 548 | 31 | 51 / 46 | 44 | 34 | 56 | 69 | 16.2 |
| T2 Jakthund | 1 | 192 | 80 | 46 / 41 | 44 | 38 | 85 | 38 | 5.4 |
| T3 Storoskorei Greatsword | 2 | 685 | 31 | 51 / 46 | 44 | 38 | 62 | 77 | 20.3 |
| T3 Storoskorei Stiletto | 2 | 685 | 31 | 51 / 46 | 44 | 38 | 0 | 77 | 20.3 |
| T3 Storoskorei Maul | 2 | 685 | 31 | 51 / 46 | 44 | 48 | 0 | 96 | 20.3 |
| T4 Huntmaster | 3 | 960 | 31 | 51 / 46 | 44 | 62 | 87 | 185 | 28.4 |
| T4 Storm-caller | 3 | 960 | 31 | 51 / 46 | 44 | 86 | 78 | 257 | 28.4 |

---

## Part 11: Sim Results

Win rate when each class is in the party, at level 30 (1,500 fights per family), with family bodies and the speed shift applied. Weak hits per fight in parentheses.

| Class | Ande | Draugr | Bein | Drattr | Djur | Oskorei |
|---|---|---|---|---|---|---|
| Brennumar | 25% (0.9) | 73% (6.9) | 52% (0.0) | 24% (0.6) | 73% (3.7) | 60% (4.3) |
| Dagskald | 51% (0.9) | 57% (6.0) | 70% (5.0) | 48% (0.0) | 39% (0.0) | 54% (0.0) |
| Hafrunar | 26% (1.2) | 40% (0.0) | 54% (0.0) | 25% (0.0) | 42% (0.0) | 47% (0.0) |
| Lundar | 26% (0.8) | 33% (0.0) | 49% (0.0) | 53% (6.6) | 43% (0.0) | 49% (1.1) |
| Seidar | 14% (0.5) | 22% (0.0) | 27% (0.0) | 23% (0.0) | 30% (0.0) | 37% (0.0) |
| Skurmar | 29% (1.1) | 35% (0.0) | 49% (0.0) | 29% (0.0) | 41% (0.0) | 38% (0.0) |
| Berserker | 26% (0.0) | 22% (0.0) | 45% (2.3) | 29% (0.0) | 25% (0.0) | 33% (0.7) |
| Hersir | 23% (0.0) | 47% (3.3) | 27% (0.0) | 18% (0.0) | 20% (0.0) | 30% (0.7) |
| Huskarl | 25% (0.0) | 45% (2.9) | 30% (0.0) | 18% (0.0) | 40% (0.0) | 44% (0.9) |
| Nalarbani | 28% (0.0) | 30% (0.0) | 36% (0.0) | 42% (2.9) | 56% (2.8) | 49% (2.2) |
| Ullar | 33% (0.0) | 28% (0.0) | 36% (0.0) | 55% (4.7) | 51% (3.9) | 55% (2.5) |
| Vasara | 25% (0.0) | 39% (0.0) | 63% (4.3) | 32% (0.0) | 26% (0.0) | 42% (0.8) |

Overall party win rates at level 30: Ande 29%, Draugr 39%, Bein 47%, Drattr 35%, Djur 41%, Oskorei 46%. Oskorei by tier: T1 76%   T2 66%   T3 18%   T4 19%. Absolute difficulty is a knob; the comparisons are what count.

---|---|---|---|---|---|---|
| Brennumar | 25% (0.9) | 73% (6.9) | 52% (0.0) | 24% (0.6) | 73% (3.7) | 60% (4.3) |
| Dagskald | 51% (0.9) | 57% (6.0) | 70% (5.0) | 48% (0.0) | 39% (0.0) | 54% (0.0) |
| Hafrunar | 26% (1.2) | 40% (0.0) | 54% (0.0) | 25% (0.0) | 42% (0.0) | 47% (0.0) |
| Lundar | 26% (0.8) | 33% (0.0) | 49% (0.0) | 53% (6.6) | 43% (0.0) | 49% (1.1) |
| Seidar | 14% (0.5) | 22% (0.0) | 27% (0.0) | 23% (0.0) | 30% (0.0) | 37% (0.0) |
| Skurmar | 29% (1.1) | 35% (0.0) | 49% (0.0) | 29% (0.0) | 41% (0.0) | 38% (0.0) |
| Berserker | 26% (0.0) | 22% (0.0) | 45% (2.3) | 29% (0.0) | 25% (0.0) | 33% (0.7) |
| Hersir | 23% (0.0) | 47% (3.3) | 27% (0.0) | 18% (0.0) | 20% (0.0) | 30% (0.7) |
| Huskarl | 25% (0.0) | 45% (2.9) | 30% (0.0) | 18% (0.0) | 40% (0.0) | 44% (0.9) |
| Nalarbani | 28% (0.0) | 30% (0.0) | 36% (0.0) | 42% (2.9) | 56% (2.8) | 49% (2.2) |
| Ullar | 33% (0.0) | 28% (0.0) | 36% (0.0) | 55% (4.7) | 51% (3.9) | 55% (2.5) |
| Vasara | 25% (0.0) | 39% (0.0) | 63% (4.3) | 32% (0.0) | 26% (0.0) | 42% (0.8) |

Overall party win rates at level 30: Ande 29%, Draugr 39%, Bein 47%, Drattr 35%, Djur 41%, Oskorei 46%. Oskorei by tier: T1 76%   T2 66%   T3 18%   T4 19%. Absolute difficulty is a knob; the comparisons are what count.

---|---|---|---|---|---|---|
| Brennumar | 25% (0.9) | 73% (6.9) | 52% (0.0) | 24% (0.6) | 73% (3.7) | 60% (4.3) |
| Dagskald | 51% (0.9) | 57% (6.0) | 70% (5.0) | 48% (0.0) | 39% (0.0) | 54% (0.0) |
| Hafrunar | 26% (1.2) | 40% (0.0) | 54% (0.0) | 25% (0.0) | 42% (0.0) | 47% (0.0) |
| Lundar | 26% (0.8) | 33% (0.0) | 49% (0.0) | 53% (6.6) | 43% (0.0) | 49% (1.1) |
| Seidar | 14% (0.5) | 22% (0.0) | 27% (0.0) | 23% (0.0) | 30% (0.0) | 37% (0.0) |
| Skurmar | 29% (1.1) | 35% (0.0) | 49% (0.0) | 29% (0.0) | 41% (0.0) | 38% (0.0) |
| Berserker | 26% (0.0) | 22% (0.0) | 45% (2.3) | 29% (0.0) | 25% (0.0) | 33% (0.7) |
| Hersir | 23% (0.0) | 47% (3.3) | 27% (0.0) | 18% (0.0) | 20% (0.0) | 30% (0.7) |
| Huskarl | 25% (0.0) | 45% (2.9) | 30% (0.0) | 18% (0.0) | 40% (0.0) | 44% (0.9) |
| Nalarbani | 28% (0.0) | 30% (0.0) | 36% (0.0) | 42% (2.9) | 56% (2.8) | 49% (2.2) |
| Ullar | 33% (0.0) | 28% (0.0) | 36% (0.0) | 55% (4.7) | 51% (3.9) | 55% (2.5) |
| Vasara | 25% (0.0) | 39% (0.0) | 63% (4.3) | 32% (0.0) | 26% (0.0) | 42% (0.8) |

Overall party win rates at level 30: Ande 29%, Draugr 39%, Bein 47%, Drattr 35%, Djur 41%, Oskorei 46%. Oskorei by tier: T1 76%   T2 66%   T3 18%   T4 19%. Absolute difficulty is a knob; the comparisons are what count.

---|---|---|---|---|---|---|
| Brennumar | 27% (0.6) | 80% (6.1) | 39% (0.0) | 23% (0.6) | 64% (3.5) | 63% (4.3) |
| Dagskald | 52% (1.1) | 76% (4.2) | 65% (3.3) | 53% (0.0) | 38% (0.0) | 59% (0.0) |
| Hafrunar | 28% (1.3) | 49% (0.0) | 42% (0.0) | 27% (0.0) | 43% (0.0) | 47% (0.0) |
| Lundar | 28% (0.8) | 48% (0.0) | 50% (0.0) | 55% (6.4) | 41% (0.0) | 49% (1.2) |
| Seidar | 17% (0.6) | 32% (0.0) | 20% (0.0) | 24% (0.0) | 29% (0.0) | 41% (0.0) |
| Skurmar | 29% (1.2) | 50% (0.0) | 39% (0.0) | 33% (0.0) | 40% (0.0) | 43% (0.0) |
| Berserker | 26% (0.0) | 31% (0.0) | 36% (1.7) | 28% (0.0) | 20% (0.0) | 37% (0.7) |
| Hersir | 23% (0.0) | 52% (3.1) | 21% (0.0) | 25% (0.0) | 20% (0.0) | 38% (0.9) |
| Huskarl | 28% (0.0) | 51% (2.6) | 34% (0.0) | 18% (0.0) | 35% (0.0) | 46% (1.1) |
| Nalarbani | 22% (0.0) | 36% (0.0) | 34% (0.0) | 39% (2.7) | 55% (2.7) | 55% (2.1) |
| Ullar | 35% (0.0) | 39% (0.0) | 24% (0.0) | 50% (4.7) | 49% (3.9) | 52% (2.8) |
| Vasara | 24% (0.0) | 46% (0.0) | 36% (3.3) | 34% (0.0) | 28% (0.0) | 43% (0.8) |

Overall party win rates at level 30: Ande 30%, Draugr 50%, Bein 38%, Drattr 36%, Djur 39%, Oskorei 49%. Oskorei by tier: T1 83%   T2 70%   T3 18%   T4 23%. Absolute difficulty is a knob; the comparisons are what count.

---|---|---|---|---|---|---|
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
- **Slagg:** a molten forge-slime, a Mogel unique tied to the pocketed smith root (Smed).
- **A true 48px Drottmogel,** if the item-inside overlay isn't enough.

---

## Open Questions

- **Bein as role units** (Joseph, Nov 7): the Bein become something like weak Oskorei, each one patching another family's weakness. Draft names: **Beinorv** (bone arrow; ON *ǫrvar*, "arrows"), the archer that gives the Draugr reach; **Beinbryn** (bone mail; ON *brynja*, "mail-coat"), a Slash-resistant wall that Covers, so it can soak the Mogel's Slash weakness and give Ande packs a Front; **Beinseidr**, a lich-like caster, as a possible third.
- **Insect glue creatures** (Joseph to draw): small units that fit any habitat and patch gaps, like the Djur's lack of reach.

- **Overall difficulty:** Halv bodies made random packs harder (29–43% at level 30). One difficulty setting can ease everything without changing the shapes.
- **Stat values:** the value weights behind the bodies (HP and attack 1, DEF, MDF, and SPD 0.5, WIL 0.25) are estimates.
- **Oskorei Tier 3:** the reverse mirror is a wall (33%); consider less HP or 2-cost Djur in Tier 2 to smooth the climb.
- **The Bein:** resisting both Slash and Pierce may be one resistance too many.
- **Undead fight length:** about 5 rounds, shorter than spirit fights.
- **Cleanse (Skolja):** rarely cast, because the party inflicts few statuses; revisit once status-heavy classes exist.
- **Art:** Litel, Stor, and Drott spirit sprites; the Stor and Drott Mogel overlays (a skull, a crown); everything for the other families.
- **Mogel fight length:** the chain adds about 3 re-forms a fight (12 rounds at level 10). Knobs: the 35% re-form share, or a chain that stops at the Litel.
- **Composer weights:** every face and unit is equally likely today. Weights per rank or per biome are the next difficulty lever.
- **Composer catalog:** only the Ande and the Mogel are in it; the other families still use their own fillers.
