# The Spellbook

A spell-naming system in the spirit of SMT, Persona, Final Fantasy, and Dragon Quest, built from Norse, Swedish, and broader Germanic roots (with Uralic and PIE consulted along the way). The goal isn't strict etymology. A Swedish speaker should hear a spell and think *"yeah, that sounds right,"* and an English speaker should be able to learn the ladder the way you learn *Crack → Crackle → Kacrack → Kacrackle*.

Every spell is built from up to three pieces:

```
[Target] + [Tier] + Root
   All-  +  Jatte- + Blixt   =  Alljatteblixt  ("Strong Lightning, hits all")
```

---

## The Schools

Four elemental schools plus a Light/Dark pair. Each school teaches a core element and a child element: a related form that is its own damage type, learned through the parent school.

| School | Element | Child | How the child arises |
|---|---|---|---|
| **Eld** | Fire | **Reyk** (Smoke) | Fire burns and gives off smoke |
| **Vatn** | Water | **Hrim** (Ice) | Water freezes into rime |
| **Blast** | Wind | **Blixt** (Lightning) | Wind whips up the storm that brings lightning |
| **Jord** | Earth | **Gro** (Nature) | Earth nurtures growth |
| **Sol** | Light | **Lak** (Healing) | Light makes whole |
| **Natt** | Dark | **Aska** (Death) | What remains when a life burns down |

**Roles at a glance**
- **Eld** is fast, high-damage burn. **Reyk** patches Fire's weakness with tricks: blinding, obscuring, disrupting.
- A child element shifts its parent's role rather than just adding damage.
- **Blast** and **Blixt** share their *Bl-* by happy accident, which gives them a family resemblance.

### Roots

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
| Aska | ash, death | Swedish and Old Norse *aska* |

### Reserved

Held back for bespoke, one-off spells (Heat Weapon, Freeze in Place, and similar) rather than full elements:

- **Smed**: smith (Swedish *smed*); candidate home for weapon-heating and forge effects under Eld
- **Sten**: stone
- **Skog**: forest

---

## Grammar

### Tiers

| Tier | Prefix | Meaning | Example |
|---|---|---|---|
| Weak | **Halv-** | Swedish *halv*, "half" | Halveld |
| Base | — | — | Eld |
| Moderate | **Mer-** | Swedish *mer*, "more" | Mereld |
| Strong | **Jatte-** | Swedish *jätte*, "giant" (also an everyday intensifier, as in *jättebra*) | Jatteld |
| Strongest | **Ur-** | Swedish *ur-*, "primal, original" (as in *urtid*, "primeval time") | Ureld |

**Halv** is the half-cast: cheap and weak. It's where fledgling wizards start, and it's the tier any class can learn. A Tank who puts a few points into Eld caps out at Halveld, which is just enough to surprise an enemy when it makes sense to put the sword away.

### Targeting

| Target | Prefix | Example |
|---|---|---|
| Single | — | Blixt |
| All | **All-** | Allblixt |

### Order

Target comes first, then tier, then root. All- is always the first thing you read, like SMT's *Ma-*.

> Allmereld = All + Mer + Eld = "Moderate Fire, hits all"

### Spelling Rules

1. **No special letters.** *Jätte* becomes Jatte, *läka* becomes Lak.
2. **Identical letters at a seam merge.** Halv + vatn = Halvatn, All + lak = Allak, Ur + reyk = Ureyk.
3. **When two different vowels meet, the second one wins.** Jatte + aska = Jattaska.

---

## The Full Grid

### Single Target

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

### All Targets

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

---

## Open Questions

- **Pruning:** not every cell needs to exist. Which combinations get cut (for example, no All- version of the strongest Death spell)?
- **Allhalv- length:** cheap area-clearing is a good job for it, but do the names read too long?
- **Bespoke spells:** Smed, Sten, Skog, and one-offs like Heat Weapon or Freeze in Place.
- **Buffs and debuffs:** not designed yet. They need their own morphemes, in the same spirit.
