# Roles and Trios (Nov 21: draft for Joseph's mark-up)

Three heroes, twelve classes. A trio is a third of the party per pick, so it should spell a strategy. We don't need all 220 trios to work: we name the ones that make sense and enable them on purpose. The gauntlet (`sim/gauntlet.py`) checks each named trio.

## The rules

1. **No role lives in only one class.** Every role below appears in at least two classes, in different flavors. Today the Dagskald is the only healer, and the starting three (no healer) never beat a Boss in the gauntlet: every good trio would become "two picks plus the Dagskald".
2. **Each class has one main role and one second role.** The second role is what lets a trio cover its gaps.
3. **The specialist gets a premium.** The Dagskald stays in charge of healing: his Lak and Kvad heal at **1.2** of a Krosh (Lak ~125, a Song stack ~55), the one class above 1.0. Other sustain comes in other shapes (prevention, drain, stitches, cleansing), not as a second Lak.
4. **Sustain isn't only heals.** HP you never lose is sustain too: wards (Fortified), Nimble, Cover and taunts, killing fast, stealing life back.

## The roles

| Role | What it does | Examples in the rules today |
|---|---|---|
| **Front** | Holds the line: taunts, Cover, high HP and DEF | Egga, Lya, the Vasara's 1000 HP |
| **Sustain** | Keeps the party standing: heals, wards, drain, cleansing, stitches | Lak, Kvad, Gyllenlykt |
| **Control** | Denies the foe's turns or space: Pin, Stun, Freeze, push and pull, Blind | Naglskott, Stelblixt, Kasta, Svepa, Reyk |
| **Burst** | Kills one target fast | Mereld, Merblotskott, Hevn |
| **Area** | Hits rows or everyone; spreads a burn | Alleld, Kuling, Storm, Scorch |
| **Setup** | Makes the party's hits land harder: Marked, Sundered, Feeble, ATK up, knots | Peka, Brakrosh, Lamsveda, Allaukraft |

## The chart

Built: the five with kits. Proposed: the seven without (first guesses, to be designed).

| Class | Kind | Main role | Second role | Sustain it brings | Status |
|---|---|---|---|---|---|
| **Vasara** (Hammer) | martial | Front | Setup (Sundered) | Cover, taunts, 1000 HP | built |
| **Ullar** (Bow) | martial | Burst (ranged) | Control (Pin, Mark) | none | built |
| **Brennumar** (Eld) | magic | Area (Scorch) | Burst (Mereld) | none (Feeble softens foes) | built |
| **Dagskald** (Sol) | magic | Sustain (heals, 1.2) | Setup (Song, ATK up) | Lak, Kvad, Gyllenlykt | built |
| **Skurmar** (Blast) | magic | Area (wind) | Control (shoves, Stun) | none (Nimble through Medvind later) | built |
| **Huskarl** (Axe and shield) | martial | Front (the second anvil) | Setup (Slash, cleaving rows) | Cover, Fortified on himself | proposed |
| **Nalarbani** (Stikk, the needle) | martial | Sustain (the field surgeon) | Burst (Pierce, Bleed) | Sava: Mending on an ally; Lonnsava also stops Bleeding | proposed |
| **Lundar** (Jord) | magic | Sustain (wards) | Front-from-the-rear (stone) | Fortified, stoneskin, wards on a row | proposed |
| **Seidar** (Natt) | magic | Setup (curses) | Sustain (drain) | life stolen back to the party | proposed |
| **Hafrunar** (Vatn) | magic | Control (Chill, Freeze) | Sustain (cleansing, tides) | removes statuses; a slow tide heal | proposed |
| **Hersir** (Greatsword) | martial | Burst (the duelist) | Area (sweeping Slash) | none | proposed |
| **Berserker** (Club) | martial | Burst (all-in) | Front (soaks by rage) | heals on a kill | proposed |

Coverage with the proposals (main or second role): Front 4 (Vasara, Huskarl, Lundar, Berserker), Sustain 5 (Dagskald, Nalarbani, Lundar, Seidar, Hafrunar: heals, stitches, wards, drain, cleansing), Control 3, Burst 5, Area 3, Setup 4. No role in only one class.

## The field surgeon's stitches (Joseph's Mend, on the Nalarbani)

- **Sava** (to save; to sew): gives an ally **Mending 3**. Mending heals half a Song stack at each round's start (about 28 with the Dagskald's 1.2, so about 85 over its three rounds) and fades a stack a round. It can't be stacked or refreshed: cast it again only after it runs out.
- **Cost:** the minor rung, **8 HP**. A martial pays to heal, which is fair: the real price is the turn he doesn't attack. It nets about +77 over three rounds, under a Lak (~125 at once) but spread out and on his HP.
- **Lonnsava** (16 HP): Mending and the end of Bleeding. Stitches.
- Why a class move and not a universal martial action: a self-heal every martial carries erodes both the Dagskald's job and the surgeon's.

## Named trios (the ones we promise to make work)

| Trio | Who | Plan | Weak to |
|---|---|---|---|
| **The Witch's Circle** | Brennumar, Skurmar, Dagskald | Wind flares Scorch (built: every Blast on a burning foe stokes Brennumar's fire); everyone hit at once; the Dagskald wards with Gyllenlykt and the Song | No front: needs its wards to hold |
| **The Shield Wall** | Vasara, Huskarl, Dagskald | Two anvils hold the front while the Song keeps them standing | Slow; little area damage |
| **The Hunt** | Ullar, Nalarbani, Seidar | Pin, Mark, Bleed and pick off; stitches and drain carry it | Crowds; anything that rushes the rear |
| **The Storm-Anvil** | Vasara, Skurmar, Lundar | Gusts shove foes into each other (bumps hurt both); the hammer Sunders what's left in front; stone wards | Slow to kill a single big target |
| **The Rush** | Berserker, Hersir, Seidar | All offense; kills fast and drains back | Glass; a bad start snowballs |
| **The Long Winter** | Hafrunar, Lundar, Vasara | Freeze the line, ward the line, outlast everything | Low damage; long fights |
| **The Surgery** | Vasara, Ullar, Nalarbani | The starting martials with a medic: the starting three without needing magic | Area damage; MP-free, so Wounded bites |

## What this asks next

- Joseph's mark-up: the roles, the chart's guesses, the trios worth promising.
- The Dagskald at 1.2 (Lak ~125): agree, and when.
- The surgeon: the Nalarbani as Sava's home, or a new class.
- Then the seven kits get designed to fill the chart, and the gauntlet gets one row per named trio as each becomes buildable.
